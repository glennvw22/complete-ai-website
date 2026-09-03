"""Bulkbron: bedrijven ophalen uit OpenStreetMap via de Overpass API.

Waarom OSM en niet Google/zoekmachines: dit is een deterministische bron die
per gemeente honderden bedrijven teruggeeft met naam, adres, telefoon en - het
belangrijkste voor ons - of er wel of geen website-tag is. Dat maakt "vind 100
bedrijven zonder goede website" een query in plaats van een gok.

Alleen stdlib, zodat dit in elke container draait.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field

from catalogus import Branche

# Volgorde = snelste eerst. Let op: neem hier alleen spiegels op met de HELE
# planeet. Een regionaal extract (overpass.osm.ch draait alleen Zwitserland)
# antwoordt op een Nederlandse query met HTTP 200 en nul elementen, en dat is
# erger dan een foutmelding: het ziet eruit alsof de bron werkt.
SPIEGELS = (
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass-api.de/api/interpreter",
)

USER_AGENT = "Complete-AI-leadmachine/1.0 (+https://complete-ai.nl)"

QUERY_TIMEOUT = 180     # wat we de Overpass-server zelf gunnen
OPHAAL_TIMEOUT = 240    # hoe lang wij op de verbinding wachten
PAUZE = 3               # basispauze tussen pogingen, loopt op per poging

# Tags waaronder een website kan zitten, in volgorde van betrouwbaarheid.
WEBSITE_TAGS = ("website", "contact:website", "url", "website:official")
SOCIAL_TAGS = ("contact:facebook", "facebook", "contact:instagram", "instagram")
TELEFOON_TAGS = ("phone", "contact:phone", "contact:mobile")
EMAIL_TAGS = ("email", "contact:email")


@dataclass
class Bedrijf:
    osm_id: str
    naam: str
    gemeente: str
    land: str
    branche: str
    straat: str = ""
    huisnummer: str = ""
    postcode: str = ""
    plaats: str = ""
    telefoon: str = ""
    email: str = ""
    website: str = ""
    social: str = ""
    openingstijden: str = ""
    osm_tags: dict = field(default_factory=dict)

    @property
    def adres(self) -> str:
        deel = " ".join(x for x in (self.straat, self.huisnummer) if x)
        return ", ".join(x for x in (deel, f"{self.postcode} {self.plaats}".strip()) if x)

    def als_dict(self) -> dict:
        d = asdict(self)
        d["adres"] = self.adres
        return d


def bouw_query(gemeenten: list[str], branche: Branche, timeout: int = QUERY_TIMEOUT) -> str:
    regels = []
    for i, gemeente in enumerate(gemeenten):
        gebied = f".g{i}"
        regels.append(
            f'area["name"="{gemeente}"]["boundary"="administrative"]'
            f'["admin_level"~"^(8|7)$"]->{gebied};'
        )
    binnen = []
    for i, _ in enumerate(gemeenten):
        for tag, waarde in branche.osm:
            binnen.append(f'  nwr(area.g{i})["{tag}"="{waarde}"];')
    return (
        f"[out:json][timeout:{timeout}];\n"
        + "\n".join(regels)
        + "\n(\n"
        + "\n".join(binnen)
        + "\n);\nout center tags;\n"
    )


def _eerste(tags: dict, sleutels) -> str:
    for s in sleutels:
        waarde = tags.get(s)
        if waarde:
            return str(waarde).strip()
    return ""


def _element_naar_bedrijf(el: dict, gemeente_hint: str, land: str, branche: str) -> Bedrijf | None:
    tags = el.get("tags") or {}
    naam = (tags.get("name") or tags.get("operator") or "").strip()
    if not naam:
        # Zonder naam kun je niet bellen, niet mailen en niet verrijken.
        return None
    plaats = (tags.get("addr:city") or tags.get("addr:place") or "").strip()
    return Bedrijf(
        osm_id=f"{el.get('type', '?')}/{el.get('id', '?')}",
        naam=naam,
        gemeente=plaats or gemeente_hint,
        land=land,
        branche=branche,
        straat=(tags.get("addr:street") or "").strip(),
        huisnummer=(tags.get("addr:housenumber") or "").strip(),
        postcode=(tags.get("addr:postcode") or "").strip(),
        plaats=plaats,
        telefoon=_eerste(tags, TELEFOON_TAGS),
        email=_eerste(tags, EMAIL_TAGS),
        website=_eerste(tags, WEBSITE_TAGS),
        social=_eerste(tags, SOCIAL_TAGS),
        openingstijden=(tags.get("opening_hours") or "").strip(),
        osm_tags=tags,
    )


def _vraag_spiegels(
    query: str, fouten: list[str], pogingen_per_spiegel: int, logger
) -> list[dict] | None:
    """Stuur een query naar de spiegels tot er een antwoordt.

    Geeft de elementen terug, of None als geen enkele spiegel een bruikbaar
    antwoord gaf. Een lege lijst is dus iets anders dan None: dat is een
    spiegel die wel werkte maar niets vond.
    """
    data = urllib.parse.urlencode({"data": query}).encode()

    for spiegel in SPIEGELS:
        for poging in range(1, pogingen_per_spiegel + 1):
            wachten = PAUZE * poging
            try:
                verzoek = urllib.request.Request(
                    spiegel, data=data, headers={"User-Agent": USER_AGENT}
                )
                with urllib.request.urlopen(verzoek, timeout=OPHAAL_TIMEOUT) as antwoord:
                    rauw = json.loads(antwoord.read().decode("utf-8", "replace"))
            except urllib.error.HTTPError as fout:
                # 429 = te veel verzoeken, 504 = spiegel overbelast. Allebei
                # gaan over met tijd, dus daar wachten we langer voor.
                if fout.code in (429, 502, 503, 504):
                    wachten = PAUZE * poging * 4
                fouten.append(f"{spiegel} poging {poging}: HTTP {fout.code}")
                time.sleep(wachten)
                continue
            except (urllib.error.URLError, TimeoutError, OSError,
                    json.JSONDecodeError) as fout:
                fouten.append(f"{spiegel} poging {poging}: {type(fout).__name__}: {fout}")
                time.sleep(wachten)
                continue

            # Overpass meldt een mislukte query niet met een foutcode maar met
            # een remark in een verder geldig JSON-antwoord.
            opmerking = str(rauw.get("remark") or "").strip()
            if opmerking:
                fouten.append(f"{spiegel} poging {poging}: {opmerking}")
                time.sleep(wachten * 2)
                continue

            return rauw.get("elements", [])

    return None


def _elementen_naar_bedrijven(
    elementen: list[dict], gemeente_hint: str, land: str, branche: Branche,
    gezien: set,
) -> list[Bedrijf]:
    bedrijven = []
    for el in elementen:
        bedrijf = _element_naar_bedrijf(el, gemeente_hint, land, branche.sleutel)
        if bedrijf is None:
            continue
        # Dubbele vestigingen op naam+adres binnen een run wegfilteren.
        sleutel = (bedrijf.naam.lower(), bedrijf.adres.lower())
        if sleutel in gezien:
            continue
        gezien.add(sleutel)
        bedrijven.append(bedrijf)
    return bedrijven


def haal_bedrijven(
    gemeenten: list[str],
    branche: Branche,
    land: str,
    pogingen_per_spiegel: int = 2,
    logger=print,
) -> tuple[list[Bedrijf], list[str]]:
    """Haal alle bedrijven van deze branche in deze gemeenten op.

    Eerst een query voor het hele blok gemeenten. Lukt dat niet, of komt er
    niets uit, dan opnieuw per gemeente: die queries zijn een stuk lichter en
    een enkele gemeente die de spiegel niet aankan gooit dan niet het hele
    blok weg.

    Geeft (bedrijven, foutmeldingen) terug. Faalt nooit hard: als alle spiegels
    plat liggen krijg je een lege lijst plus de reden, zodat de routine dat
    eerlijk kan melden in plaats van stil niets op te leveren.
    """
    fouten: list[str] = []
    gezien: set = set()

    elementen = _vraag_spiegels(
        bouw_query(gemeenten, branche), fouten, pogingen_per_spiegel, logger
    )
    if elementen:
        bedrijven = _elementen_naar_bedrijven(
            elementen, gemeenten[0], land, branche, gezien
        )
        logger(f"[osm] {len(bedrijven)} bedrijven voor {branche.sleutel} "
               f"in {', '.join(gemeenten)}")
        return bedrijven, fouten

    if len(gemeenten) == 1:
        logger(f"[osm] niets voor {branche.sleutel} in {gemeenten[0]}")
        return [], fouten

    logger(f"[osm] blokquery leverde niets op voor {branche.sleutel}; "
           f"nu per gemeente")
    bedrijven = []
    for gemeente in gemeenten:
        deel = _vraag_spiegels(
            bouw_query([gemeente], branche), fouten, pogingen_per_spiegel, logger
        )
        if not deel:
            continue
        bedrijven += _elementen_naar_bedrijven(deel, gemeente, land, branche, gezien)
    logger(f"[osm] {len(bedrijven)} bedrijven voor {branche.sleutel} "
           f"(per gemeente opgehaald)")
    return bedrijven, fouten
