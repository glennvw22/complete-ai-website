"""KVK-koppeling: Zoeken API + Basisprofiel API.

WAT DE KVK API WEL EN NIET KAN - dit is de kern van de verwarring tot nu toe:

  * De Zoeken API zoekt op NAAM, KVK-NUMMER, POSTCODE+HUISNUMMER, PLAATS en
    STRAAT. Er is GEEN filter op SBI-code of branche. Je kunt dus NIET vragen
    "geef alle kappers in Zwolle". De KVK API is daarmee ongeschikt als BRON
    van leads.
  * De Basisprofiel API geeft, per KVK-nummer, wel de rechtsvorm, de
    SBI-activiteiten, handelsnamen, adres en vestigingen. Dat is precies wat je
    nodig hebt om een lead te VERRIJKEN en te bepalen of je mag bellen.

Daarom is de rol van KVK in deze machine: verrijking en compliance, niet
sourcing. De bedrijven komen uit OpenStreetMap, de rechtsvorm komt uit KVK.

Sleutel: zet KVK_API_KEY in de omgeving. Zonder sleutel degradeert alles netjes
en meldt de run dat expliciet, in plaats van stil door te gaan.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

BASIS = "https://api.kvk.nl/api"
ZOEKEN = f"{BASIS}/v2/zoeken"
BASISPROFIEL = f"{BASIS}/v1/basisprofielen"

# Rechtsvormen die als rechtspersoon gelden: die mag je koud bellen.
RECHTSPERSOON_SPOREN = (
    "besloten vennootschap", "naamloze vennootschap", "stichting",
    "vereniging", "cooperatie", "coöperatie", "onderlinge waarborg",
    "europese", "publiekrechtelijke",
)
NATUURLIJK_SPOREN = (
    "eenmanszaak", "vennootschap onder firma", "commanditaire vennootschap",
    "maatschap",
)


@dataclass
class KvkResultaat:
    gevonden: bool = False
    kvk_nummer: str = ""
    handelsnaam: str = ""
    rechtsvorm: str = ""
    is_rechtspersoon: bool | None = None   # None = onbekend
    sbi: str = ""
    sbi_omschrijving: str = ""
    vestigingen: int = 0
    fout: str = ""

    @property
    def baan(self) -> str:
        if self.is_rechtspersoon is True:
            return "BEL"
        # Natuurlijk persoon en onbekend gaan allebei naar de mailbaan:
        # bij twijfel niet bellen.
        return "MAIL"


class KvkClient:
    def __init__(self, sleutel: str | None = None, pauze_s: float = 0.35):
        self.sleutel = sleutel if sleutel is not None else os.environ.get("KVK_API_KEY", "")
        self.pauze_s = pauze_s
        self.beschikbaar = bool(self.sleutel)
        self.laatste_fout = "" if self.beschikbaar else "KVK_API_KEY niet gezet"
        self._cache: dict[str, KvkResultaat] = {}

    # -- laag niveau ------------------------------------------------------
    def _get(self, url: str, params: dict) -> tuple[dict | None, str]:
        if not self.beschikbaar:
            return None, "geen API-sleutel"
        volledig = f"{url}?{urllib.parse.urlencode(params)}" if params else url
        verzoek = urllib.request.Request(
            volledig,
            headers={"apikey": self.sleutel, "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(verzoek, timeout=25) as antwoord:
                return json.loads(antwoord.read().decode("utf-8", "replace")), ""
        except urllib.error.HTTPError as fout:
            lichaam = ""
            try:
                lichaam = fout.read().decode("utf-8", "replace")[:300]
            except Exception:
                pass
            return None, f"HTTP {fout.code}: {lichaam or fout.reason}"
        except (urllib.error.URLError, TimeoutError, OSError) as fout:
            return None, f"{type(fout).__name__}: {fout}"
        except json.JSONDecodeError as fout:
            return None, f"ongeldige JSON: {fout}"
        finally:
            time.sleep(self.pauze_s)

    # -- zelftest ---------------------------------------------------------
    def zelftest(self) -> tuple[bool, str]:
        """Een echte call, zodat een run keihard kan melden of KVK werkt."""
        if not self.beschikbaar:
            return False, "KVK_API_KEY ontbreekt in de omgeving van deze routine."
        data, fout = self._get(ZOEKEN, {"naam": "Kamer van Koophandel",
                                        "pagina": 1, "resultatenPerPagina": 1})
        if fout:
            uitleg = {
                "401": "sleutel afgewezen (401) - verkeerde of verlopen API-key.",
                "403": "toegang geweigerd (403) - key heeft geen recht op deze API.",
                "429": "te veel verzoeken (429) - limiet bereikt.",
            }
            for code, tekst in uitleg.items():
                if f"HTTP {code}" in fout:
                    return False, tekst
            return False, f"KVK onbereikbaar: {fout}"
        aantal = (data or {}).get("totaal", 0)
        return True, f"KVK API werkt (testzoekopdracht gaf {aantal} treffers)."

    # -- verrijking -------------------------------------------------------
    def zoek(self, naam: str, plaats: str = "") -> KvkResultaat:
        cachesleutel = f"{naam}|{plaats}".lower()
        if cachesleutel in self._cache:
            return self._cache[cachesleutel]

        resultaat = KvkResultaat()
        if not self.beschikbaar:
            resultaat.fout = self.laatste_fout
            self._cache[cachesleutel] = resultaat
            return resultaat

        params = {"naam": naam, "pagina": 1, "resultatenPerPagina": 5}
        if plaats:
            params["plaats"] = plaats
        data, fout = self._get(ZOEKEN, params)
        if fout or not data:
            resultaat.fout = fout or "leeg antwoord"
            self._cache[cachesleutel] = resultaat
            return resultaat

        treffers = data.get("resultaten") or []
        if not treffers:
            resultaat.fout = "geen treffer op naam+plaats"
            self._cache[cachesleutel] = resultaat
            return resultaat

        beste = sorted(treffers, key=lambda t: _rang(t, plaats))[0]
        resultaat.gevonden = True
        resultaat.kvk_nummer = str(beste.get("kvkNummer", "") or "")
        resultaat.handelsnaam = beste.get("naam", "") or ""

        if resultaat.kvk_nummer:
            self._vul_basisprofiel(resultaat)

        self._cache[cachesleutel] = resultaat
        return resultaat

    def _vul_basisprofiel(self, resultaat: KvkResultaat) -> None:
        data, fout = self._get(f"{BASISPROFIEL}/{resultaat.kvk_nummer}", {})
        if fout or not data:
            resultaat.fout = f"basisprofiel: {fout or 'leeg'}"
            return

        resultaat.rechtsvorm = _pak_rechtsvorm(data)
        resultaat.is_rechtspersoon = classificeer_rechtsvorm(resultaat.rechtsvorm)

        activiteiten = data.get("sbiActiviteiten") or []
        if activiteiten and isinstance(activiteiten[0], dict):
            eerste = activiteiten[0]
            resultaat.sbi = str(eerste.get("sbiCode", "") or "")
            resultaat.sbi_omschrijving = eerste.get("sbiOmschrijving", "") or ""

        aantal = data.get("aantalVestigingen")
        if isinstance(aantal, int):
            resultaat.vestigingen = aantal


def _rang(treffer: dict, plaats: str) -> tuple:
    """Voorkeur voor de hoofdvestiging in de gezochte plaats."""
    zelfde_plaats = 0 if (treffer.get("plaats") or "").lower() == plaats.lower() else 1
    hoofd = 0 if treffer.get("type") == "hoofdvestiging" else 1
    return (zelfde_plaats, hoofd)


def _pak_rechtsvorm(data: dict) -> str:
    """De rechtsvorm heeft in de KVK-antwoorden meerdere plekken gehad.

    We proberen ze in volgorde in plaats van op een enkel pad te gokken, zodat
    een schemawijziging niet stilletjes alle leads op 'onbekend' zet.
    """
    kandidaten = [
        data.get("rechtsvorm"),
        data.get("juridischeRechtsvorm"),
        (data.get("materieleRegistratie") or {}).get("rechtsvorm")
        if isinstance(data.get("materieleRegistratie"), dict) else None,
    ]
    embedded = data.get("_embedded")
    if isinstance(embedded, dict):
        hoofd = embedded.get("hoofdvestiging")
        if isinstance(hoofd, dict):
            kandidaten.append(hoofd.get("rechtsvorm"))
    for kandidaat in kandidaten:
        if isinstance(kandidaat, str) and kandidaat.strip():
            return kandidaat.strip()
    return ""


def classificeer_rechtsvorm(rechtsvorm: str) -> bool | None:
    """True = rechtspersoon (bellen mag), False = natuurlijk persoon, None = onbekend."""
    if not rechtsvorm:
        return None
    laag = rechtsvorm.lower()
    for spoor in NATUURLIJK_SPOREN:
        if spoor in laag:
            return False
    for spoor in RECHTSPERSOON_SPOREN:
        if spoor in laag:
            return True
    return None
