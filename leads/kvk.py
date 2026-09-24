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
import re
import time
import unicodedata
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
    oprichtingsdatum: str = ""   # ruwe KVK-datumstring, alleen uit basisprofiel
    medewerkers: int | None = None  # totaalWerkzamePersonen, alleen uit basisprofiel
    zoek_type: str = ""      # 'hoofdvestiging' / 'rechtspersoon' / 'nevenvestiging'
    bron: str = ""           # 'zoeken' (gratis) of 'basisprofiel' (betaald)
    fout: str = ""

    @property
    def baan(self) -> str:
        if self.is_rechtspersoon is True:
            return "BEL"
        # Natuurlijk persoon en onbekend gaan allebei naar de mailbaan:
        # bij twijfel niet bellen.
        return "MAIL"


# --------------------------------------------------------------------------
# De sleutelkluis op de machine zelf.
#
# Dit bestand is de ENIGE plek waar de KVK-sleutel hoort te staan. Reden:
# de leadroutine draait als geplande taak op de Mac van Glenn, niet in een
# cloud-omgeving. Een sleutel die in een cloudsessie is gezet, is bij de
# volgende sessie weg - en dat is precies wat er maandenlang gebeurde: de
# oude foutmelding stuurde naar "de cloud-omgeving van deze routine",
# terwijl de routine lokaal draait. Elke week opnieuw invullen dus.
#
# Door het bestand hier zelf te lezen hoeft geen enkele routine, sessie of
# shell de sleutel nog te exporteren. Zet hem er een keer in en het werkt,
# ook als iemand run.py met de hand start.
#
# Het bestand staat bewust BUITEN deze repository (die is openbaar) en heeft
# rechten 600. Alleen het pad staat hier; de sleutel nooit.
SLEUTELKLUIS = os.path.expanduser("~/.config/complete-ai/.env")


def _uit_kluis(naam: str) -> str:
    """Lees een variabele uit de sleutelkluis. Nooit een fout, altijd een
    string: ontbreekt het bestand of de regel, dan is het antwoord leeg en
    meldt de zelftest dat verderop netjes."""
    try:
        with open(SLEUTELKLUIS, "r", encoding="utf-8") as bestand:
            for regel in bestand:
                regel = regel.strip()
                if not regel or regel.startswith("#") or "=" not in regel:
                    continue
                sleutel, _, waarde = regel.partition("=")
                if sleutel.strip() == naam:
                    # aanhalingstekens eromheen zijn gebruikelijk in .env-bestanden
                    return waarde.strip().strip('"').strip("'")
    except OSError:
        pass
    return ""


class KvkClient:
    def __init__(self, sleutel: str | None = None, pauze_s: float = 0.35,
                 via_proxy: bool | None = None):
        """Waar de sleutel vandaan komt, in deze volgorde:

        0. `sleutel=""` (lege string, niet None) betekent hard uit: run.py's
           `--geen-kvk` gebruikt dit om GEEN ENKELE aanvraag te doen, ook niet
           via de proxy. Dit is bewust een apart geval van "niet meegegeven"
           (`None`, punt 1 hieronder) — anders bleef in een omgeving met
           `KVK_VIA_PROXY=1` een "--geen-kvk"-run gewoon echte, betaalde
           basisprofielen ophalen omdat de proxy de sleutel toch opplakte.
           Precies dat gebeurde op 24-9-2026: de zelftest meldde "SLEUTEL
           AFGEWEZEN (401)" terwijl het verzoek zonder controle op
           `via_proxy` gewoon was uitgegaan.
        1. Meegegeven aan de constructor (voor tests).
        2. `KVK_API_KEY` als omgevingsvariabele.
        3. `KVK_API_KEY` uit de sleutelkluis ~/.config/complete-ai/.env.
           Dit is de vaste plek; zet hem daar en hij blijft staan.
        4. `KVK_VIA_PROXY=1` - de sleutel staat als API-credential op een
           cloud-omgeving en Anthropics proxy plakt de header erop nadat het
           verzoek de container verlaten heeft. Alleen zinvol voor runs die
           daadwerkelijk IN die cloud-omgeving draaien; de dagelijkse routine
           draait dat niet.
        """
        hard_uit = sleutel == ""
        if sleutel is not None:
            self.sleutel = sleutel
        else:
            self.sleutel = os.environ.get("KVK_API_KEY", "") or _uit_kluis("KVK_API_KEY")
        if hard_uit:
            self.via_proxy = False        # zie punt 0 hierboven: geen stille proxy-call
        elif via_proxy is not None:
            self.via_proxy = via_proxy
        else:
            vlag = (os.environ.get("KVK_VIA_PROXY", "") or _uit_kluis("KVK_VIA_PROXY")).strip()
            self.via_proxy = vlag in ("1", "ja", "true")
        self.pauze_s = pauze_s
        self.beschikbaar = bool(self.sleutel) or self.via_proxy
        if hard_uit:
            self.laatste_fout = "--geen-kvk: bewust uitgezet, geen aanvraag gedaan"
        elif self.beschikbaar:
            self.laatste_fout = ""
        else:
            self.laatste_fout = "KVK_API_KEY niet gezet en KVK_VIA_PROXY staat uit"
        self._cache: dict[str, KvkResultaat] = {}

    # -- laag niveau ------------------------------------------------------
    def _get(self, url: str, params: dict) -> tuple[dict | None, str]:
        if not self.beschikbaar:
            return None, "geen API-sleutel"
        volledig = f"{url}?{urllib.parse.urlencode(params)}" if params else url
        headers = {"Accept": "application/json"}
        if self.sleutel:
            headers["apikey"] = self.sleutel
        # Zonder eigen sleutel gaat het verzoek kaal de deur uit en zet de
        # proxy de header erop.
        verzoek = urllib.request.Request(volledig, headers=headers)
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
        if self.laatste_fout == "--geen-kvk: bewust uitgezet, geen aanvraag gedaan":
            return False, self.laatste_fout   # geen advies om een sleutel te zetten: dit is gewild
        if not self.beschikbaar:
            return False, (
                "Geen KVK-sleutel gevonden. Zet hem op de vaste plek en hij blijft staan:\n"
                f"    echo 'KVK_API_KEY=jouw-sleutel' >> {SLEUTELKLUIS}\n"
                f"    chmod 600 {SLEUTELKLUIS}\n"
                "Zet hem NIET in een cloud-omgeving: de dagelijkse leadroutine draait "
                "lokaal op deze machine, dus een sleutel in een cloudsessie is bij de "
                "volgende sessie weg. Controleer met: python3 leads/run.py --diagnose")
        data, fout = self._get(ZOEKEN, {"naam": "Kamer van Koophandel",
                                        "pagina": 1, "resultatenPerPagina": 1})
        if fout:
            uitleg = {
                "401": ("SLEUTEL AFGEWEZEN (401): de verbinding werkt wel, maar de "
                        "API-key wordt niet geaccepteerd. Verkeerde of verlopen key"
                        + (", of de proxy plakt de apikey-header er niet op"
                           if self.via_proxy and not self.sleutel else "") + "."),
                "403": ("TOEGANG GEWEIGERD (403): de verbinding werkt, maar deze key "
                        "heeft geen recht op deze API. Vraag de API aan in het "
                        "KVK Developer Portal."),
                "404": "NIET GEVONDEN (404): het eindpunt klopt niet.",
                "429": "LIMIET BEREIKT (429): te veel verzoeken.",
            }
            for code, tekst in uitleg.items():
                if f"HTTP {code}" in fout:
                    return False, tekst
            # Geen HTTP-antwoord betekent dat het verzoek de deur niet uit kwam.
            # Dat is een netwerkkwestie, niet een sleutelkwestie - en dat
            # onderscheid is precies wat we willen weten.
            return False, (
                "GEEN VERBINDING met api.kvk.nl - het verzoek kwam de container niet "
                "uit. Dit zegt NIETS over de geldigheid van de sleutel. Oorzaak: het "
                "netwerkbeleid van deze omgeving. Los op door de sleutel als "
                "API-credential op api.kvk.nl te zetten (die route omzeilt de "
                "allowlist), of door Network access op Full te zetten. "
                f"Technische fout: {fout}")
        aantal = (data or {}).get("totaal", 0)
        return True, f"KVK API werkt (testzoekopdracht gaf {aantal} treffers)."

    def zoek_landelijk(self, naam: str, resultaten: int = 20) -> list[dict]:
        """Gratis Zoeken-aanroep ZONDER plaats-filter: alle KVK-treffers op
        deze naam, in heel Nederland. Geen KvkResultaat (dat is een koppeling
        aan één bedrijf) maar de ruwe trefferlijst - dit is bedoeld om te
        TELLEN, niet om te koppelen. Zie ketens.landelijke_spreiding() voor
        waarvoor dit dient: een keten herkennen die niet op een vaste
        naamlijst staat en niet als KVK-nevenvestiging geregistreerd staat
        (18-9-2026, aanleiding: Tuinland — elke vestiging een eigen
        rechtspersoon, dus is_filiaal() en de vaste ketens-lijst misten het
        allebei)."""
        if not self.beschikbaar:
            return []
        params = {"naam": naam, "pagina": 1, "resultatenPerPagina": resultaten}
        data, fout = self._get(ZOEKEN, params)
        if fout or not data:
            return []
        return data.get("resultaten") or []

    # -- verrijking -------------------------------------------------------
    def zoek(self, naam: str, plaats: str = "",
             met_basisprofiel: bool = True) -> KvkResultaat:
        """Zoek een bedrijf op naam en plaats.

        De Zoeken API is gratis, het Basisprofiel kost per bevraging. Met
        `met_basisprofiel=False` doe je alleen de gratis stap; die geeft het
        KVK-nummer en het type inschrijving, genoeg voor een eerste schifting.
        """
        cachesleutel = f"{naam}|{plaats}|{met_basisprofiel}".lower()
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

        beste = sorted(treffers, key=lambda t: _rang(t, naam, plaats))[0]
        if not _naam_matcht(naam, beste.get("naam", "") or ""):
            # Geen enkele treffer had een naam die overeenkomt met de
            # zoekopdracht - de "beste" treffer hierboven won alleen op
            # plaats/vestigingstype. Dat gebeurde op 17/18-9-2026 met
            # "Boerenbond" en "Pets Place": twee verschillende bedrijfsnamen op
            # (ooit) hetzelfde adres kregen zo hetzelfde KVK-nummer. Zonder
            # harde naam-match is dit geen treffer, punt - bij twijfel niet
            # koppelen.
            resultaat.fout = "geen treffer met een overeenkomende bedrijfsnaam (alleen op adres/plaats)"
            self._cache[cachesleutel] = resultaat
            return resultaat
        resultaat.gevonden = True
        resultaat.kvk_nummer = str(beste.get("kvkNummer", "") or "")
        resultaat.handelsnaam = beste.get("naam", "") or ""
        resultaat.zoek_type = (beste.get("type") or "").lower()
        resultaat.bron = "zoeken"

        if resultaat.kvk_nummer and met_basisprofiel:
            self._vul_basisprofiel(resultaat)

        self._cache[cachesleutel] = resultaat
        return resultaat

    def verrijk_met_basisprofiel(self, resultaat: KvkResultaat) -> KvkResultaat:
        """Haalt het BETAALDE basisprofiel op voor een resultaat dat al uit de
        gratis zoekstap komt (resultaat.kvk_nummer is dus al bekend).

        Bewust een aparte methode in plaats van zoek(..., met_basisprofiel=True):
        zo is er in de aanroepende code (run.py) een harde knip tussen de gratis
        stap (altijd) en deze betaalde stap (alleen voor de voorgeselecteerde
        kandidaten die de gratis filters - o.a. nevenvestiging, zie belbaar.py
        is_filiaal() - al doorstaan zijn). Muteert resultaat in place en geeft
        het ook terug, voor het gemak van de aanroeper.
        """
        if not resultaat.kvk_nummer:
            resultaat.fout = "geen kvk-nummer bekend, basisprofiel overgeslagen"
            return resultaat
        self._vul_basisprofiel(resultaat)
        return resultaat

    def _vul_basisprofiel(self, resultaat: KvkResultaat) -> None:
        data, fout = self._get(f"{BASISPROFIEL}/{resultaat.kvk_nummer}", {})
        if fout or not data:
            resultaat.fout = f"basisprofiel: {fout or 'leeg'}"
            return

        resultaat.rechtsvorm = _pak_rechtsvorm(data)
        resultaat.is_rechtspersoon = classificeer_rechtsvorm(resultaat.rechtsvorm)
        resultaat.bron = "basisprofiel"

        activiteiten = data.get("sbiActiviteiten") or []
        if activiteiten and isinstance(activiteiten[0], dict):
            eerste = activiteiten[0]
            resultaat.sbi = str(eerste.get("sbiCode", "") or "")
            resultaat.sbi_omschrijving = eerste.get("sbiOmschrijving", "") or ""

        aantal = data.get("aantalVestigingen")
        if isinstance(aantal, int):
            resultaat.vestigingen = aantal

        resultaat.oprichtingsdatum = _pak_oprichtingsdatum(data)
        resultaat.medewerkers = _pak_medewerkers(data)


def _plaats_van_treffer(treffer: dict) -> str:
    """De plaats zit in de Zoeken API niet op het hoogste niveau.

    Ze staat onder adres.binnenlandsAdres.plaats (of buitenlandsAdres). Op
    treffer["plaats"] gokken gaf altijd een lege string, waardoor elke treffer
    even goed leek en de sortering op plaats niets deed.
    """
    adres = treffer.get("adres")
    if not isinstance(adres, dict):
        return ""
    for sleutel in ("binnenlandsAdres", "buitenlandsAdres"):
        deel = adres.get(sleutel)
        if isinstance(deel, dict) and deel.get("plaats"):
            return str(deel["plaats"]).strip()
    return ""


def _normaliseer_naam(naam: str) -> str:
    """Kleine letters, geen accenten, geen leestekens - alleen de woorden."""
    naam = unicodedata.normalize("NFKD", naam or "")
    naam = "".join(teken for teken in naam if not unicodedata.combining(teken))
    return " ".join(re.findall(r"[a-z0-9]+", naam.lower()))


def _naam_matcht(gezocht: str, gevonden: str) -> bool:
    """Harde naam-match tussen de gezochte naam en een KVK-treffer.

    Bewust conservatief (bij twijfel geen match): gelijk, of de één zit
    volledig in de ander (dekt "Pets Place" tegen "Pets Place Nederland
    B.V." en andersom). GEEN gok op basis van adres of vestigingstype - dat
    was precies de bug van 17/18-9-2026 (zie _rang en zoek() hieronder)."""
    a = _normaliseer_naam(gezocht)
    b = _normaliseer_naam(gevonden)
    if not a or not b:
        return False
    return a == b or a in b or b in a


def _rang(treffer: dict, naam: str, plaats: str) -> tuple:
    """Voorkeur voor een treffer wiens NAAM ook echt overeenkomt met de
    zoekopdracht, dan de hoofdvestiging, dan de gezochte plaats.

    Vóór 18-9-2026 keek deze functie alleen naar plaats en vestigingstype,
    NOOIT naar de naam van de treffer zelf. Zocht de KVK Zoeken API dan
    (bijvoorbeeld bij geen exacte naamtreffer) iets terug op basis van
    vestigingsadres, dan kon een treffer die niets met de gezochte naam te
    maken had toch als "beste" resultaat winnen - vastgesteld toen
    "Boerenbond" en "Pets Place" (ooit hetzelfde pand, andere huurder)
    hetzelfde KVK-nummer kregen toegewezen. De naam-match staat daarom nu
    voorop; zoek() hieronder wijst een treffer bovendien hard af als zelfs de
    beste van de reeks geen naam-match heeft."""
    treffer_naam = treffer.get("naam", "") or ""
    geen_naam_match = 0 if _naam_matcht(naam, treffer_naam) else 1
    gevonden_plaats = _plaats_van_treffer(treffer).lower()
    zelfde_plaats = 0 if gevonden_plaats and gevonden_plaats == plaats.lower() else 1
    hoofd = 0 if treffer.get("type") == "hoofdvestiging" else 1
    return (geen_naam_match, zelfde_plaats, hoofd)


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
        # Hier staat hij in werkelijkheid: de rechtsvorm hoort bij de EIGENAAR
        # van de inschrijving, niet bij de vestiging. Een vestiging heeft geen
        # eigen rechtsvorm, dus _embedded.hoofdvestiging leverde altijd niets
        # op en daarmee viel elke Nederlandse lead af op 'rechtsvorm onbekend'.
        eigenaar = embedded.get("eigenaar")
        if isinstance(eigenaar, dict):
            kandidaten.append(eigenaar.get("rechtsvorm"))
            kandidaten.append(eigenaar.get("uitgebreideRechtsvorm"))
        hoofd = embedded.get("hoofdvestiging")
        if isinstance(hoofd, dict):
            kandidaten.append(hoofd.get("rechtsvorm"))
    for kandidaat in kandidaten:
        if isinstance(kandidaat, str) and kandidaat.strip():
            return kandidaat.strip()
    return ""


def _pak_oprichtingsdatum(data: dict) -> str:
    """Startdatum van de onderneming (materieleRegistratie).

    Net als bij rechtsvorm hierboven: het exacte veldpad in de KVK-respons is
    NIET bevestigd met een echte testaanroep (18-9-2026), alleen met de
    ontwikkelaarsdocumentatie die zegt dat materieleRegistratie een
    "start- en einddatum van de onderneming" bevat zonder de JSON-sleutel te
    noemen. Daarom hier, net als bij rechtsvorm, meerdere kandidaat-paden
    proberen in plaats van op één naam te gokken. Geeft "" als niets van dit
    alles een waarde oplevert - dan is de jong-bedrijf-bonus in score.py
    simpelweg niet van toepassing, in plaats van een verzonnen datum.
    """
    mat = data.get("materieleRegistratie")
    kandidaten = []
    if isinstance(mat, dict):
        kandidaten += [mat.get("datumAanvang"), mat.get("datumAanvangOnderneming"),
                       mat.get("startdatum")]
    kandidaten += [data.get("datumAanvang"), data.get("datumOprichting")]
    embedded = data.get("_embedded")
    if isinstance(embedded, dict):
        hoofd = embedded.get("hoofdvestiging")
        if isinstance(hoofd, dict):
            kandidaten.append(hoofd.get("datumAanvang"))
    for kandidaat in kandidaten:
        if isinstance(kandidaat, str) and kandidaat.strip():
            return kandidaat.strip()
    return ""


def _pak_medewerkers(data: dict) -> int | None:
    """Aantal werkzame personen, indien de basisprofiel-respons dat geeft.

    Zelfde voorbehoud als hierboven: veldpad niet met een echte aanroep
    geverifieerd, meerdere plekken geprobeerd. None (niet 0) als er niets
    gevonden is - 0 zou een echte meting suggereren die er niet is."""
    kandidaten = [data.get("totaalWerkzamePersonen")]
    embedded = data.get("_embedded")
    if isinstance(embedded, dict):
        hoofd = embedded.get("hoofdvestiging")
        if isinstance(hoofd, dict):
            kandidaten.append(hoofd.get("totaalWerkzamePersonen"))
    for kandidaat in kandidaten:
        if isinstance(kandidaat, int):
            return kandidaat
    return None


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
