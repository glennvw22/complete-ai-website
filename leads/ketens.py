"""Landelijke/internationale ketens herkennen — twee lagen, allebei gratis.

Aanleiding laag 1 (17/18-9-2026): `belbaar.is_filiaal()` herkent alleen een
officieel geregistreerde KVK-NEVENVESTIGING. Bij controle van de
dashboard-database bleken er 13 leads te staan die overduidelijk landelijke
ketens/filialen zijn (Boerenbond, C&A, Kwik-Fit x3, Van Mossel x2, Tesla,
Basic-Fit, Pets Place, SnowWorld Amsterdam, Lucardi x2) — GEEN van die 13
stond geregistreerd als KVK-nevenvestiging; ze staan allemaal apart,
zelfstandig ingeschreven (elke vestiging vaak als eigen rechtspersoon of
franchisenemer). `is_filiaal()` mist dit type dus volledig. Laag 1
(`is_landelijke_keten`, hieronder) vult dat gat met een expliciete naamlijst
— instant, geen API-aanroep nodig, maar bewust kort: alleen namen waarvan
zeker is dat het een keten is.

**Aanleiding laag 2 (18-9-2026): een naamlijst is precies het probleem, niet
de oplossing.** Tuinland (Groningen én Zwolle, twee losse KVK-nummers, dus
ook door de bestaande dubbel-kvk-check niet gevangen) stond niet op de lijst
en kwam gewoon weer door. Glenn, letterlijk: "niet alleen voor de boerenbond
... ik vroeg niet om alleen de boerenbond te fixen." Een vaste lijst is
altijd onvolledig — er is altijd een volgende keten die er niet op staat.

Laag 2 (`is_landelijke_spreiding`, onderaan dit bestand) lost dat structureel
op: een GRATIS landelijke naamzoekopdracht (kvk.zoek_landelijk, geen
plaats-filter) telt hoeveel ANDERE plaatsen een KVK-treffer hebben met
hetzelfde merk in de naam. Geen vaste lijst meer nodig — werkt voor elke
toekomstige keten, ook eentje waar we nog nooit van gehoord hebben. Getest
tegen echte KVK-data (18-9-2026): "Tuinland" -> 6+ verschillende plaatsen
(keten), "Kapsalon Jansen" -> 2 (Astrid Jansen, Monique Jansen, Rob Jansen
zijn gewoon andere, toevallig gelijknamige kapsalons, geen keten — de
naamzoekopdracht van de KVK matcht los op woorden, dus "Jansen" alleen is
geen betrouwbaar signaal; er moet een AANEENGESLOTEN woordreeks matchen,
zie `_bevat_subreeks`).

Beide lagen zijn puur een KOSTENfilter, net als is_filiaal() in belbaar.py:
een filiaal van een keten heeft op die locatie geen lokale besluitvormer met
budget voor website, telefonist of automatisering, dus is het geen bruikbare
lead — ongeacht wat de KVK over de juridische structuur zegt. Bij twijfel
niet uitsluiten: een gemiste uitsluiting kost twee cent (een basisprofiel dat
overbodig blijkt); een onterechte uitsluiting kost een echte lead.
"""
from __future__ import annotations

import re
import unicodedata

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kvk import KvkClient

# Canonieke ketennamen. De matchfunctie hieronder is ongevoelig voor
# hoofdletters, spaties, koppeltekens en het weglaten van een spatie (dus
# "Kwik-Fit", "Kwik Fit" en "KwikFit" worden alle drie herkend — dat zijn de
# drie schrijfwijzen die in de praktijk zijn aangetroffen op 17/18-9-2026).
LANDELIJKE_KETENS: tuple[str, ...] = (
    # De 13 leads van 17/18-9-2026:
    "Boerenbond",
    "C&A",
    "Kwik-Fit",
    "Van Mossel",
    "Tesla",
    "Basic-Fit",
    "Pets Place",
    "SnowWorld",
    "Lucardi",
    # Andere landelijke NL-ketens waarvan de naam ondubbelzinnig is:
    "Hunkemöller",
    "Zeeman",
    "Action",
    "Bruna",
    "Etos",
    "Kruidvat",
)


def _tokens(naam: str) -> list[str]:
    """Woorden van een naam, kleine letters, zonder leestekens of accenten.

    "C&A" -> ["c", "a"], "Kwik-Fit" -> ["kwik", "fit"],
    "Hunkemöller" -> ["hunkemoller"].
    """
    naam = unicodedata.normalize("NFKD", naam or "")
    naam = "".join(teken for teken in naam if not unicodedata.combining(teken))
    return re.findall(r"[a-z0-9]+", naam.lower())


def _bevat_subreeks(haystack: list[str], needle: tuple[str, ...]) -> bool:
    """Komt `needle` als aaneengesloten reeks voor in `haystack`?"""
    n = len(needle)
    if n == 0 or n > len(haystack):
        return False
    return any(tuple(haystack[i:i + n]) == needle for i in range(len(haystack) - n + 1))


# Voorbewerkt bij het importeren, niet bij elke aanroep.
_KETEN_TOKENS: tuple[tuple[str, ...], ...] = tuple(tuple(_tokens(k)) for k in LANDELIJKE_KETENS)
_KETEN_AANEEN: tuple[str, ...] = tuple("".join(t) for t in _KETEN_TOKENS)


def is_landelijke_keten(naam: str) -> bool:
    """Is dit (vermoedelijk) een vestiging van een bekende landelijke keten?

    Twee manieren om te matchen, allebei op woordniveau in plaats van los
    tekst-in-tekst zoeken (dat zou "Actionfoto Zwolle" ten onrechte aan
    "Action" koppelen):

    1. De woorden van de keten komen als aaneengesloten reeks voor in de
       woorden van de bedrijfsnaam — dekt spaties én koppeltekens, en een
       plaatsnaam erachter ("Kwik-Fit Almere", "Kwik Fit Almere").
    2. Voor een keten van meerdere woorden: staat er, als los AANEENGESCHREVEN
       woord, exact de samengevoegde ketennaam ("KwikFit") tussen de woorden
       van de bedrijfsnaam? Dekt de derde schrijfwijze zonder spatie of
       streepje. Alleen voor ketens van 2+ woorden: bij een keten van één
       woord (bv. "Tesla") is dit gelijk aan punt 1 hierboven en voegt het
       niets toe.

    Bij twijfel: geen match. Geen enkele losse-letter- of deelwoordmatch (dus
    "Capsalon Anna" matcht NIET met "C&A").
    """
    tokens = _tokens(naam)
    if not tokens:
        return False
    for keten_tokens, keten_aaneen in zip(_KETEN_TOKENS, _KETEN_AANEEN):
        if _bevat_subreeks(tokens, keten_tokens):
            return True
        if len(keten_tokens) > 1 and keten_aaneen in tokens:
            return True
    return False


# ── laag 2: dynamische herkenning, geen naamlijst nodig ─────────────────────

# 4+ andere plaatsen met hetzelfde merk (in het patroon "<merk> <plaats>")
# = keten. Niet lager: een veelvoorkomende Nederlandse achternaam levert
# op zichzelf al een paar toevallige "<achternaam> <stad>"-treffers op,
# zonder dat het één keten is. Getest tegen echte KVK-data 18-9-2026:
# Tuinland en Boerenbond zitten ruim boven de 4 (6 en 16), "Kapsalon
# Jansen" bleef op 2-3 steken. "Van Eijck Roosendaal" kwam op 5 uit - dat
# kán een keten zijn, kan ook toeval zijn (een veelvoorkomende achternaam);
# bij die onzekerheid is uitsluiten hier bewust de keuze, zie de
# moduledocstring voor waarom.
LANDELIJKE_SPREIDING_DREMPEL = 4


def _plaats_van_treffer(treffer: dict) -> str:
    """Zelfde als kvk._plaats_van_treffer — hier gekopieerd in plaats van
    geïmporteerd, want dat veldpad (adres.binnenlandsAdres.plaats) is
    KVK-antwoordformaat, geen kvk.py-interne zaak, en dit bestand hoeft verder
    niets van kvk.py te weten dan de KvkClient die het meekrijgt."""
    adres = treffer.get("adres")
    if not isinstance(adres, dict):
        return ""
    for sleutel in ("binnenlandsAdres", "buitenlandsAdres"):
        deel = adres.get(sleutel)
        if isinstance(deel, dict) and deel.get("plaats"):
            return str(deel["plaats"]).strip()
    return ""


def _merk_tokens(naam: str, eigen_plaats: str) -> tuple[str, ...]:
    """De woorden van de naam die vermoedelijk het MERK zijn, niet de plaats.

    "Tuinland Zwolle" met eigen_plaats "Zwolle" -> ("tuinland",): de
    plaatsnaam op het eind is duidelijk een locatie-suffix, geen deel van het
    merk. "Kapsalon Jansen" met eigen_plaats "Lichtenvoorde" -> geen
    overlap, dus blijft de hele naam staan: ("kapsalon", "jansen")."""
    tokens = _tokens(naam)
    plaats_tokens = _tokens(eigen_plaats)
    if plaats_tokens and len(tokens) > len(plaats_tokens) \
            and tokens[-len(plaats_tokens):] == plaats_tokens:
        tokens = tokens[:-len(plaats_tokens)]
    return tuple(tokens)


def landelijke_spreiding(kvk_client: "KvkClient", naam: str, eigen_plaats: str) -> int:
    """Hoeveel DISTINCTE andere plaatsen hebben een KVK-treffer die overduidelijk
    hetzelfde merk is als deze kandidaat, alleen in een andere plaats? Eén
    gratis Zoeken-aanroep zonder plaats-filter (kvk_client.zoek_landelijk),
    dus landelijk. Geeft 0 als er geen duidelijk merk is (bv. een naam die
    volledig uit de plaatsnaam bestaat) of als KVK niet beschikbaar is.

    Belangrijk: er wordt gezocht op het MERK alleen ("Tuinland"), niet op de
    volledige kandidaatnaam ("Tuinland Zwolle"). Live tegen de echte KVK API
    geprobeerd (18-9-2026): zoeken op "Tuinland Zwolle" gaf maar 1 treffer
    (alleen die ene vestiging zelf, de KVK Zoeken API is dan kennelijk te
    specifiek/exact), zoeken op "Tuinland" gaf 10 treffers over heel
    Nederland. Zonder deze correctie mist deze functie precies het geval
    waarvoor hij gebouwd is.

    Een treffer telt alleen mee als het merk aaneengesloten voorkomt (net als
    is_landelijke_keten hierboven) ÉN de rest van de treffernaam - alles
    ERVOOR en ERNA samen - leeg is of exact de eigen plaats van DIE treffer
    is (dus "<merk> <stad>", "<stad> <merk>" of kaal "<merk>"). Zonder die
    tweede eis leek "Van Eijck Roosendaal" (een gewone garage) live op een
    keten met 16 vestigingen: de KVK Zoeken API vond ook "Van Eijck Fiscaal",
    "Osteopathie van Eijck" en "Van Eijck Loonbedrijf" - andere bedrijven die
    toevallig dezelfde (veelvoorkomende) achternaam in de naam hebben, geen
    filialen. Met deze eis blijven alleen treffers over die het patroon
    "<merk> <eigen plaats>" volgen, wat een keten wél en toevallige
    naamgenoten meestal NIET doen. Dit is een heuristiek, geen garantie: een
    veelvoorkomende achternaam kan in zeldzame gevallen alsnog een paar keer
    toevallig als "<achternaam> <stad>" voorkomen. Vandaar de vrij hoge
    drempel (LANDELIJKE_SPREIDING_DREMPEL)."""
    merk = _merk_tokens(naam, eigen_plaats)
    if not merk:
        return 0
    treffers = kvk_client.zoek_landelijk(" ".join(merk))
    plekken: set[str] = set()
    for treffer in treffers:
        treffer_tokens = _tokens(treffer.get("naam", "") or "")
        n = len(merk)
        rest = None
        for i in range(len(treffer_tokens) - n + 1):
            if tuple(treffer_tokens[i:i + n]) == merk:
                rest = treffer_tokens[:i] + treffer_tokens[i + n:]
                break
        if rest is None:
            continue
        treffer_plaats = _plaats_van_treffer(treffer)
        if rest and tuple(rest) != tuple(_tokens(treffer_plaats)):
            continue
        sleutel = treffer_plaats or str(treffer.get("kvkNummer", ""))
        if sleutel:
            plekken.add(sleutel.lower())
    return len(plekken)


def is_landelijke_spreiding(kvk_client: "KvkClient", naam: str, eigen_plaats: str) -> bool:
    """Is dit (vermoedelijk) een filiaal van een keten die niet op de vaste
    lijst hierboven staat? Zie landelijke_spreiding() en de moduledocstring
    (aanleiding: Tuinland, 18-9-2026)."""
    return landelijke_spreiding(kvk_client, naam, eigen_plaats) >= LANDELIJKE_SPREIDING_DREMPEL
