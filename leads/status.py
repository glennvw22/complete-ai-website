"""Het statusmodel van de bellijst.

Eén vaste woordenlijst voor de lead-machine, de bellijst-pagina en straks de
dashboard-app. Als die drie verschillende woorden gebruiken voor hetzelfde,
klopt de rapportage nooit meer. Daarom staat het hier, op één plek.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Status:
    sleutel: str
    label: str
    uitleg: str
    # Telt deze status als afgehandeld? Zo ja, verdwijnt de lead uit de werklijst.
    afgehandeld: bool
    # Mag deze lead ooit opnieuw gebeld worden?
    opnieuw_bellen: bool


STATUSSEN: tuple[Status, ...] = (
    Status("nieuw", "Nieuw",
           "Nog niet gebeld", afgehandeld=False, opnieuw_bellen=True),
    Status("geen_gehoor", "Geen gehoor",
           "Gebeld, niemand opgenomen", afgehandeld=False, opnieuw_bellen=True),
    Status("terugbellen", "Terugbellen",
           "Gesproken, maar op een ander moment verder", afgehandeld=False,
           opnieuw_bellen=True),
    Status("geinteresseerd", "Geïnteresseerd",
           "Wil meer weten", afgehandeld=False, opnieuw_bellen=True),
    Status("afspraak", "Afspraak",
           "Afspraak of demo ingepland", afgehandeld=False, opnieuw_bellen=True),
    Status("klant", "Klant",
           "Verkocht", afgehandeld=True, opnieuw_bellen=False),
    Status("niet_geinteresseerd", "Niet geïnteresseerd",
           "Gesproken, geen interesse", afgehandeld=True, opnieuw_bellen=True),
    Status("niet_bellen", "Niet meer bellen",
           "Heeft gevraagd niet meer gebeld te worden - dit is bindend",
           afgehandeld=True, opnieuw_bellen=False),
)

OP_SLEUTEL = {s.sleutel: s for s in STATUSSEN}
BEGINSTATUS = "nieuw"

# Deze twee mogen nooit opnieuw op de bellijst komen, ook niet in een latere run.
BLOKKERENDE_STATUSSEN = tuple(s.sleutel for s in STATUSSEN if not s.opnieuw_bellen)


def geldig(sleutel: str) -> bool:
    return sleutel in OP_SLEUTEL


def mag_opnieuw(sleutel: str) -> bool:
    """Mag een bedrijf met deze status nog eens op de lijst verschijnen?"""
    status = OP_SLEUTEL.get(sleutel)
    return status.opnieuw_bellen if status else True
