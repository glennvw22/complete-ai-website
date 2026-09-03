"""Wie mag je bellen, en wie absoluut niet.

De regel voor Nederland: koud bellen mag alleen naar rechtspersonen. Een
eenmanszaak, vof, cv of maatschap geldt als natuurlijk persoon en valt onder het
bel-me-niet-regime; die bellen levert klachten en boetes op. In Vlaanderen mag
zakelijk bellen wel, mits de DNCM-lijst vooraf geschoond is.

Dit bestand is bewust streng: alles waarvan we het NIET zeker weten valt af.
Een lijst die je zonder nadenken kunt afbellen is meer waard dan een langere
lijst waar je bij elke regel moet twijfelen.
"""
from __future__ import annotations

from dataclasses import dataclass

# Uit het KVK-antwoord: deze typen inschrijving zijn rechtspersonen.
ZOEKTYPE_RECHTSPERSOON = ("rechtspersoon",)


@dataclass
class Beloordeel:
    mag_bellen: bool
    reden: str
    let_op: str = ""


def beoordeel_belbaarheid(bedrijf, kvk_resultaat) -> Beloordeel:
    """bedrijf: bron_osm.Bedrijf, kvk_resultaat: kvk.KvkResultaat of None."""
    if not bedrijf.telefoon:
        return Beloordeel(False, "geen telefoonnummer gevonden")

    if bedrijf.land == "BE":
        return Beloordeel(
            True,
            "Belgisch bedrijf met telefoonnummer; zakelijk bellen is toegestaan",
            let_op="DNCM-scrub vereist vóór bellen (donotcallme.be)",
        )

    # Nederland: rechtspersoon of niet bellen.
    if kvk_resultaat is None or not kvk_resultaat.gevonden:
        return Beloordeel(False, "niet in KVK teruggevonden, rechtsvorm onbekend")

    if kvk_resultaat.is_rechtspersoon is True:
        return Beloordeel(
            True, f"rechtspersoon ({kvk_resultaat.rechtsvorm}) — koud bellen toegestaan"
        )
    if kvk_resultaat.is_rechtspersoon is False:
        return Beloordeel(
            False, f"natuurlijk persoon ({kvk_resultaat.rechtsvorm}) — niet bellen"
        )

    # Rechtsvorm onbekend, maar de gratis zoekstap zei wel 'rechtspersoon'.
    # Dat is een aanwijzing, geen bewijs: te zwak om op te bellen.
    if kvk_resultaat.zoek_type in ZOEKTYPE_RECHTSPERSOON:
        return Beloordeel(
            False,
            "KVK noemt het een rechtspersoon maar de rechtsvorm is niet opgehaald — "
            "te onzeker om te bellen",
        )
    return Beloordeel(False, "rechtsvorm onbekend — bij twijfel niet bellen")


def kandidaat_voor_kvk(bedrijf) -> bool:
    """Is het de moeite waard om hier een betaalde KVK-bevraging aan te wagen?

    Zonder telefoonnummer wordt het toch nooit een belbare lead, dus dan is de
    bevraging weggegooid geld.
    """
    return bool(bedrijf.telefoon) and bedrijf.land == "NL"
