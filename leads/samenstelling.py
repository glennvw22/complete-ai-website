"""De dagelijkse lijst samenstellen met quota per dienst.

Alleen op score sorteren geeft een eenzijdige lijst: dan staan er honderd
bedrijven zonder website in en verkoop je nooit een AI-telefonist. Hier worden
eerst de quota gevuld, en pas daarna wordt de rest op score aangevuld.

Elke geselecteerde lead is belbaar. Dat is geen voorkeur maar een harde eis:
een lijst waar niet-belbare bedrijven tussen zitten, is een lijst waarbij je bij
elke regel moet nadenken of je die mag draaien.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Quota:
    """Hoeveel leads er minimaal van elk soort in de lijst moeten."""
    website: int = 50
    telefonist: int = 15
    automatisering: int = 15

    def als_dict(self) -> dict[str, int]:
        return {
            "website": self.website,
            "telefonist": self.telefonist,
            "automatisering": self.automatisering,
        }


@dataclass
class Samenstelling:
    gekozen: list = field(default_factory=list)
    per_quotum: dict = field(default_factory=dict)
    tekorten: dict = field(default_factory=dict)
    afgevallen_niet_belbaar: int = 0
    afgevallen_zonder_reden: int = 0
    redenen_afgevallen: dict = field(default_factory=dict)


def stel_samen(kandidaten: list, aantal: int, quota: Quota) -> Samenstelling:
    """kandidaten: lijst van (bedrijf, site, kvk, beoordeling, belbaarheid).

    Werkwijze: eerst per quotum de best scorende belbare leads die aan dat
    quotum voldoen, daarna aanvullen op score tot het gewenste aantal.
    """
    uitslag = Samenstelling()

    belbaar_lijst = []
    for rij in kandidaten:
        belbaarheid, beoordeling = rij[4], rij[3]
        if not belbaarheid.mag_bellen:
            uitslag.afgevallen_niet_belbaar += 1
            sleutel = belbaarheid.reden.split(" (")[0]
            uitslag.redenen_afgevallen[sleutel] = \
                uitslag.redenen_afgevallen.get(sleutel, 0) + 1
            continue
        # Harde ondergrens: een bedrijf zonder enig koopsignaal is geen lead.
        # Een moderne site, online boeken, goed bereikbaar - daar hebben we
        # niets te verkopen, en zo iemand bellen verspilt Glenns tijd.
        if not beoordeling.signalen:
            uitslag.afgevallen_zonder_reden += 1
            continue
        belbaar_lijst.append(rij)

    belbaar_lijst.sort(key=lambda r: (-r[3].score, -r[3].warmte.punten))

    gekozen_ids: set[str] = set()

    def pak(voorwaarde, hoeveel: int) -> int:
        genomen = 0
        for rij in belbaar_lijst:
            if genomen >= hoeveel or len(gekozen_ids) >= aantal:
                break
            if rij[0].osm_id in gekozen_ids:
                continue
            if voorwaarde(rij[3]):
                gekozen_ids.add(rij[0].osm_id)
                uitslag.gekozen.append(rij)
                genomen += 1
        return genomen

    gewenst = quota.als_dict()
    gehaald = {
        "website": pak(lambda b: b.website_gat, gewenst["website"]),
        "telefonist": pak(lambda b: b.heeft_dienst("telefonist"), gewenst["telefonist"]),
        "automatisering": pak(lambda b: b.heeft_dienst("automatisering"),
                              gewenst["automatisering"]),
    }
    uitslag.per_quotum = gehaald
    uitslag.tekorten = {
        sleutel: gewenst[sleutel] - gehaald[sleutel]
        for sleutel in gewenst
        if gehaald[sleutel] < gewenst[sleutel]
    }

    # Aanvullen op score tot het gewenste aantal.
    pak(lambda b: True, aantal)

    uitslag.gekozen.sort(key=lambda r: (-r[3].score, -r[3].warmte.punten))
    return uitslag
