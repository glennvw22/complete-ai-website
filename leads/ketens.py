"""Bekende landelijke/internationale ketens — herkend aan de bedrijfsnaam,
zonder dat daar een KVK-bevraging (gratis of betaald) voor nodig is.

Aanleiding (17/18-9-2026): `belbaar.is_filiaal()` herkent alleen een officieel
geregistreerde KVK-NEVENVESTIGING. Bij controle van de dashboard-database
bleken er 13 leads te staan die overduidelijk landelijke ketens/filialen zijn
(Boerenbond, C&A, Kwik-Fit x3, Van Mossel x2, Tesla, Basic-Fit, Pets Place,
SnowWorld Amsterdam, Lucardi x2) — GEEN van die 13 stond geregistreerd als
KVK-nevenvestiging; ze staan allemaal apart, zelfstandig ingeschreven (elke
vestiging vaak als eigen rechtspersoon of franchisenemer). `is_filiaal()` mist
dit type dus volledig.

Dit bestand vult dat gat met een expliciete naamlijst. Puur een KOSTENfilter,
net als is_filiaal() in belbaar.py: een filiaal van een keten heeft op die
locatie geen lokale besluitvormer met budget voor website, telefonist of
automatisering, dus is het geen bruikbare lead — ongeacht wat de KVK over de
juridische structuur zegt.

Bewust een KORTE lijst. Alleen namen waarvan zeker is dat het een landelijke
keten is — geen gok. Twijfel je over een naam, zet 'm er niet bij: een gemiste
uitsluiting kost twee cent (een basisprofiel dat overbodig blijkt); een
onterechte uitsluiting kost een echte lead.
"""
from __future__ import annotations

import re
import unicodedata

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
