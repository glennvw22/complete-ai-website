"""Welke koopsignalen we uit de eigen website van het bedrijf mogen halen.

Twee soorten, en het verschil is het hele punt van deze module:

* **aanwezig** — er staat iets letterlijk op de pagina. Het citaat is het
  bewijs; `poort.py` zoekt het achteraf terug. Dit is het enige soort dat
  een pitch mag dragen.
* **afwezig** — iets ontbreekt op de pagina's die we hebben gelezen. Dat
  is zwakker bewijs: we hebben niet de hele website gezien. Zo'n signaal
  mag daarom nooit alleen staan, en de zin noemt altijd welke pagina's
  zijn gelezen, zodat een mens het kan nakijken.

De oude machine maakte precies die fout wél: "geen website bekend" (een
ontbrekende tag in OpenStreetMap) werd een verkoopargument voor een
nieuwe website, ook bij bedrijven die een prima website hadden.
"""
from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass

AANWEZIG = "aanwezig"
AFWEZIG = "afwezig"

# Markeringen voor online afspraak/bestellen. Dezelfde sporen als
# website_check.AFSPRAAK_SPOREN, plus een paar boekingsplatforms.
AFSPRAAK_SPOREN = (
    "afspraak maken", "afspraak inplannen", "online afspraak", "reserveer",
    "reserveren", "boek nu", "online boeken", "booking", "bestel online",
    "bestellen", "offerte aanvragen", "plan een", "agenda", "calendly",
    "salonized", "treatwell", "formitable", "resengo", "thuisbezorgd",
    "planity", "trengo", "appointlet",
)

VEROUDERDE_PLATFORMEN = (
    "powered by jimdo", "gemaakt met jimdo", "wix.com", "powered by wix",
    "weebly", "webnode", "jouwweb", "mijnwebwinkel", "powered by blogger",
)

RECHTSPERSOON_VORMEN = ("b.v.", "bv", "n.v.", "nv", "b.v", "besloten vennootschap",
                        "naamloze vennootschap", "coöperatie", "stichting", "vereniging")
NIET_RECHTSPERSOON_VORMEN = ("eenmanszaak", "v.o.f.", "vof", "vennootschap onder firma",
                             "maatschap", "commanditaire vennootschap", "c.v.")

_KVK = re.compile(r"\bk\.?v\.?k\.?(?:[-\s]?nummer)?\s*:?\s*(\d{8})\b", re.I)
_COPYRIGHT = re.compile(r"(©|&copy;|copyright)\s*(?:\d{4}\s*[-–]\s*)?(20\d{2})", re.I)


@dataclass(frozen=True)
class Signaal:
    """Eén bevinding over één bedrijf, met het bewijs erbij."""

    sleutel: str
    dienst: str          # sleutel uit catalogus.DIENSTEN
    soort: str           # AANWEZIG of AFWEZIG
    zin: str             # de zin zoals hij in de onderbouwing terechtkomt
    citaat: str          # letterlijk van de pagina (leeg bij AFWEZIG)
    bron_url: str
    bron_datum: str


def _knip(tekst: str, treffer: re.Match | int, ruimte: int = 60) -> str:
    """Een leesbaar citaat rond een treffer, op woordgrenzen afgekapt."""
    positie = treffer.start() if isinstance(treffer, re.Match) else treffer
    start = max(0, positie - ruimte)
    eind = min(len(tekst), positie + ruimte)
    stuk = tekst[start:eind].strip()
    return re.sub(r"\s+", " ", stuk)


def _zoek(tekst: str, naald: str) -> int:
    return tekst.lower().find(naald.lower())


def kvk_nummer_uit_tekst(tekst: str) -> tuple[str, str] | None:
    """(nummer, citaat) als er een KvK-nummer op de pagina staat."""
    treffer = _KVK.search(tekst)
    if not treffer:
        return None
    return treffer.group(1), _knip(tekst, treffer, 45)


def _zonder_punten(tekst: str) -> str:
    """"B.V." en "BV" zijn hetzelfde woord; punten weghalen scheelt regels."""
    return tekst.replace(".", "")


def _vorm_in(omgeving: str, vormen) -> str | None:
    """Zoekt een rechtsvorm als los woord, punten genegeerd.

    Let op: "bv" is in het Nederlands ook de afkorting van "bijvoorbeeld".
    Daarom kijken we alleen vlak naast de bedrijfsnaam of naast het
    KvK-nummer; daar staat die afkorting vrijwel nooit.
    """
    kaal = _zonder_punten(omgeving)
    for vorm in vormen:
        if re.search(rf"\b{re.escape(_zonder_punten(vorm))}\b", kaal):
            return vorm
    return None


def rechtsvorm_uit_tekst(tekst: str, bedrijfsnaam: str = "") -> tuple[str, str] | None:
    """(rechtsvorm, citaat) — alleen als de vorm hard op de pagina staat.

    Zoekt eerst naast de bedrijfsnaam (het sterkste bewijs), dan naast een
    KvK-nummer. Een losse "bv" ergens in een lopende zin telt niet: dat is
    te vaak een afkorting of de rechtsvorm van een leverancier.
    """
    laag = tekst.lower()
    naam = (bedrijfsnaam or "").strip().lower()
    if naam:
        positie = laag.find(naam)
        if positie >= 0:
            omgeving = laag[positie:positie + len(naam) + 30]
            gevonden = (_vorm_in(omgeving, NIET_RECHTSPERSOON_VORMEN)
                        or _vorm_in(omgeving, RECHTSPERSOON_VORMEN))
            if gevonden:
                return gevonden, _knip(tekst, positie, 70)

    kvk = _KVK.search(tekst)
    if kvk:
        omgeving = laag[max(0, kvk.start() - 120):kvk.end() + 120]
        gevonden = (_vorm_in(omgeving, NIET_RECHTSPERSOON_VORMEN)
                    or _vorm_in(omgeving, RECHTSPERSOON_VORMEN))
        if gevonden:
            return gevonden, _knip(tekst, kvk, 110)
    return None


def is_rechtspersoon(vorm: str) -> bool:
    kaal = _zonder_punten((vorm or "").lower())
    return kaal in {_zonder_punten(v.lower()) for v in RECHTSPERSOON_VORMEN}


# --- losse detectoren: elk geeft (zin, citaat) of None -------------------

# Zin per zoekterm, zodat de bewering nooit meer zegt dan het citaat laat zien.
_TELEFOON_SPOREN = (
    ("bel ons voor een afspraak", "op de site staat dat afspraken telefonisch gemaakt worden"),
    ("bel voor een afspraak", "op de site staat dat afspraken telefonisch gemaakt worden"),
    ("maak telefonisch een afspraak", "op de site staat dat afspraken telefonisch gemaakt worden"),
    ("afspraak maken? bel", "op de site staat dat afspraken telefonisch gemaakt worden"),
    ("neem telefonisch contact", "de site verwijst voor contact naar de telefoon"),
    ("bel gerust", "de site verwijst voor contact naar de telefoon"),
    ("telefonisch bereikbaar", "de site noemt telefonische bereikbaarheid"),
)


def _telefoon_is_ingang(tekst: str) -> tuple[str, str] | None:
    for naald, zin in _TELEFOON_SPOREN:
        positie = _zoek(tekst, naald)
        if positie >= 0:
            return (zin, _knip(tekst, positie))
    return None


def _terugbelbelofte(tekst: str) -> tuple[str, str] | None:
    for naald in ("wij bellen u terug", "we bellen u terug", "wij nemen telefonisch contact",
                  "u wordt teruggebeld", "dan bellen wij u"):
        positie = _zoek(tekst, naald)
        if positie >= 0:
            return ("de site belooft terugbellen, dus die belletjes moeten ergens vandaan komen",
                    _knip(tekst, positie))
    return None


def _drukte(tekst: str) -> tuple[str, str] | None:
    for naald in ("wegens drukte", "vanwege drukte", "niet altijd bereikbaar",
                  "wij zijn druk", "door drukte", "helaas niet altijd"):
        positie = _zoek(tekst, naald)
        if positie >= 0:
            return ("de site meldt zelf dat de telefoon niet altijd opgenomen wordt",
                    _knip(tekst, positie))
    return None


def _offerte_per_mail(tekst: str) -> tuple[str, str] | None:
    for naald in ("offerte aanvragen per mail", "mail ons voor een offerte",
                  "stuur een e-mail voor een offerte", "offerte per e-mail",
                  "vul het formulier in en wij"):
        positie = _zoek(tekst, naald)
        if positie >= 0:
            return ("aanvragen komen als los bericht binnen en moeten met de hand verwerkt worden",
                    _knip(tekst, positie))
    return None


def _verouderd_platform(tekst: str) -> tuple[str, str] | None:
    for naald in VEROUDERDE_PLATFORMEN:
        positie = _zoek(tekst, naald)
        if positie >= 0:
            return (f"de site draait zichtbaar op {naald.replace('powered by ', '').strip()}",
                    _knip(tekst, positie, 45))
    return None


def _oud_copyright(tekst: str, vandaag: _dt.date) -> tuple[str, str] | None:
    treffers = list(_COPYRIGHT.finditer(tekst))
    if not treffers:
        return None
    # Het hoogste jaar telt: een reeks "2019-2026" betekent niet verouderd.
    beste = max(treffers, key=lambda t: int(t.group(2)))
    jaar = int(beste.group(2))
    if vandaag.year - jaar < 3:
        return None
    return (f"onderaan de site staat nog {jaar}", _knip(tekst, beste, 40))


DETECTOREN = (
    ("telefoon_is_ingang", "telefonist", _telefoon_is_ingang),
    ("terugbelbelofte", "telefonist", _terugbelbelofte),
    ("drukte_gemeld", "telefonist", _drukte),
    ("offerte_met_de_hand", "automatisering", _offerte_per_mail),
    ("verouderd_platform", "website", _verouderd_platform),
)


def verzamel(dossier, bedrijfsnaam: str = "", vandaag: _dt.date | None = None) -> list[Signaal]:
    """Alle signalen die uit dit dossier te bewijzen zijn."""
    vandaag = vandaag or _dt.date.today()
    datum = vandaag.isoformat()
    gevonden: list[Signaal] = []
    gezien: set[str] = set()

    # Eerst vaststellen of er ergens online geboekt kan worden. Zo ja, dan
    # is "het gaat telefonisch" een bewering die de site zelf tegenspreekt.
    kan_online_boeken = any(_zoek(p.tekst, spoor) >= 0
                            for p in dossier.bereikbare for spoor in AFSPRAAK_SPOREN)

    for pagina in dossier.bereikbare:
        for sleutel, dienst, detector in DETECTOREN:
            if sleutel == "telefoon_is_ingang" and kan_online_boeken:
                continue
            if sleutel in gezien:
                continue
            uitslag = detector(pagina.tekst)
            if uitslag:
                zin, citaat = uitslag
                gezien.add(sleutel)
                gevonden.append(Signaal(sleutel, dienst, AANWEZIG, zin, citaat,
                                        pagina.url, datum))
        if "oud_copyright" not in gezien:
            uitslag = _oud_copyright(pagina.tekst, vandaag)
            if uitslag:
                zin, citaat = uitslag
                gezien.add("oud_copyright")
                gevonden.append(Signaal("oud_copyright", "website", AANWEZIG, zin, citaat,
                                        pagina.url, datum))

    # Afwezigheid: alleen met de gelezen pagina's er expliciet bij.
    bezocht = dossier.bezochte_urls
    if bezocht:
        if not kan_online_boeken:
            aantal = len(bezocht)
            zin = (f"op de {aantal} pagina's die wij gelezen hebben "
                   f"({', '.join(bezocht)}) staat geen mogelijkheid om online een "
                   f"afspraak te maken of te bestellen")
            gevonden.append(Signaal("geen_online_afspraak", "automatisering", AFWEZIG,
                                    zin, "", dossier.start_url, datum))
    return gevonden
