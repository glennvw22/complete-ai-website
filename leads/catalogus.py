"""Catalogus: branches, gemeenten en de deterministische territoriumrotatie.

Alles hier is pure data + pure functies, zodat het zonder netwerk testbaar is.
"""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# Diensten van Complete AI. Elke branche en elk koopsignaal wijst hiernaar,
# zodat elke lead eindigt met "dit verkoop je hier".
# --------------------------------------------------------------------------
DIENSTEN = {
    "website": "Website (nieuw of vervanging)",
    "seo": "Vindbaarheid in Google (SEO)",
    "sea": "Advertenties (SEA / Meta)",
    "automatisering": "Automatisering van terugkerend werk",
    "telefonist": "AI-telefonist",
    "social": "Social media",
}


@dataclass(frozen=True)
class Branche:
    sleutel: str
    naam: str
    # OSM-selectors: lijst van (tag, waarde) die als aparte query-regels gaan.
    osm: tuple[tuple[str, str], ...]
    # Hoe hard is de telefoon de levensader? 0-1. Stuurt de AI-telefonist-pitch.
    beldruk: float
    # Hoort online afspraak/bestellen erbij? Stuurt de automatiserings-pitch.
    online_afspraak: bool
    # Waar dit type bedrijf doorgaans het meeste aan heeft, in volgorde.
    dienst_focus: tuple[str, ...]
    # Indicatieve SBI-codes, voor KVK-verrijking en controle.
    sbi: tuple[str, ...] = ()


BRANCHES: tuple[Branche, ...] = (
    Branche("horeca", "Restaurants, cafés en eetgelegenheden",
            (("amenity", "restaurant"), ("amenity", "cafe"), ("amenity", "fast_food"),
             ("amenity", "pub"), ("amenity", "bar")),
            beldruk=0.9, online_afspraak=True,
            dienst_focus=("website", "telefonist", "seo", "social"),
            sbi=("5610", "5630")),
    Branche("kapsalon", "Kapsalons, schoonheidssalons en nagelstudio's",
            (("shop", "hairdresser"), ("shop", "beauty"), ("shop", "massage"),
             ("shop", "nails"), ("shop", "tattoo")),
            beldruk=0.85, online_afspraak=True,
            dienst_focus=("website", "automatisering", "social", "seo"),
            sbi=("9602",)),
    Branche("installatie", "Loodgieters, installateurs en elektriciens",
            (("craft", "plumber"), ("craft", "electrician"), ("craft", "hvac"),
             ("shop", "trade"), ("craft", "gasfitter")),
            beldruk=1.0, online_afspraak=False,
            dienst_focus=("telefonist", "website", "sea", "seo"),
            sbi=("4322", "4321")),
    Branche("bouw", "Aannemers, klusbedrijven, schilders en dakdekkers",
            (("craft", "builder"), ("craft", "carpenter"), ("craft", "painter"),
             ("craft", "roofer"), ("craft", "plasterer"), ("craft", "stonemason")),
            beldruk=0.8, online_afspraak=False,
            dienst_focus=("website", "seo", "sea", "telefonist"),
            sbi=("4120", "4334", "4391")),
    Branche("hovenier", "Hoveniers, schoonmaak en onderhoud",
            (("craft", "gardener"), ("shop", "garden_centre"),
             ("craft", "window_construction"), ("office", "cleaning")),
            beldruk=0.7, online_afspraak=False,
            dienst_focus=("website", "seo", "automatisering", "sea"),
            sbi=("8130", "8121")),
    Branche("garage", "Garages, autoschade en banden",
            (("shop", "car_repair"), ("shop", "car"), ("shop", "tyres"),
             ("shop", "car_parts"), ("shop", "motorcycle_repair")),
            beldruk=0.95, online_afspraak=True,
            dienst_focus=("telefonist", "website", "automatisering", "seo"),
            sbi=("4520", "4532")),
    Branche("zorg", "Tandartsen, fysio, huisartsen en praktijken",
            (("amenity", "dentist"), ("amenity", "doctors"),
             ("healthcare", "physiotherapist"), ("healthcare", "psychotherapist"),
             ("shop", "optician"), ("healthcare", "podiatrist")),
            beldruk=1.0, online_afspraak=True,
            dienst_focus=("telefonist", "automatisering", "website", "seo"),
            sbi=("8623", "8621", "8691")),
    Branche("detailhandel", "Speciaalzaken en lokale winkels",
            (("shop", "bakery"), ("shop", "butcher"), ("shop", "florist"),
             ("shop", "furniture"), ("shop", "bicycle"), ("shop", "jewelry"),
             ("shop", "shoes"), ("shop", "clothes")),
            beldruk=0.5, online_afspraak=False,
            dienst_focus=("website", "social", "seo", "sea"),
            sbi=("4776", "4771", "4722")),
    Branche("zakelijk", "Advies, administratie, makelaars en juridisch",
            (("office", "accountant"), ("office", "estate_agent"),
             ("office", "lawyer"), ("office", "insurance"),
             ("office", "financial"), ("office", "consulting")),
            beldruk=0.8, online_afspraak=True,
            dienst_focus=("automatisering", "website", "seo", "telefonist"),
            sbi=("6920", "6831", "6910")),
    Branche("sport", "Sportscholen, dierenzorg en vrijetijd",
            (("leisure", "fitness_centre"), ("amenity", "veterinary"),
             ("shop", "pet"), ("leisure", "sports_centre"),
             ("amenity", "driving_school")),
            beldruk=0.75, online_afspraak=True,
            dienst_focus=("automatisering", "website", "social", "seo"),
            sbi=("9313", "7500")),
    Branche("transport", "Transport, verhuizers, taxi en opslag",
            (("office", "moving_company"), ("amenity", "taxi"),
             ("shop", "storage_rental"), ("office", "logistics")),
            beldruk=0.9, online_afspraak=False,
            dienst_focus=("telefonist", "website", "automatisering", "sea"),
            sbi=("4941", "4932")),
    Branche("gastvrij", "Hotels, B&B's en groepsaccommodaties",
            (("tourism", "hotel"), ("tourism", "guest_house"),
             ("tourism", "bed_and_breakfast"), ("tourism", "apartment")),
            beldruk=0.85, online_afspraak=True,
            dienst_focus=("website", "automatisering", "seo", "telefonist"),
            sbi=("5510", "5520")),
)

BRANCHE_OP_SLEUTEL = {b.sleutel: b for b in BRANCHES}


# --------------------------------------------------------------------------
# Gemeenten. Namen zoals ze in OpenStreetMap als admin_level 8 (NL) /
# admin_level 8 (BE) voorkomen.
# --------------------------------------------------------------------------
GEMEENTEN_NL: tuple[str, ...] = (
    "Almelo", "Almere", "Alkmaar", "Alphen aan den Rijn", "Amersfoort", "Amstelveen",
    "Apeldoorn", "Arnhem", "Assen", "Barneveld", "Bergen op Zoom", "Best", "Beverwijk",
    "Breda", "Bunschoten", "Capelle aan den IJssel", "Castricum", "Delft", "Den Helder",
    "Deventer", "Doetinchem", "Dordrecht", "Drachten", "Ede", "Eindhoven", "Emmen",
    "Enschede", "Epe", "Etten-Leur", "Franekeradeel", "Geldrop-Mierlo", "Gouda",
    "Groningen", "Haarlem", "Harderwijk", "Hardenberg", "Heerenveen", "Heerhugowaard",
    "Heerlen", "Helmond", "Hengelo", "Hilversum", "Hoogeveen", "Hoorn", "Houten",
    "Huizen", "IJsselstein", "Kampen", "Katwijk", "Kerkrade", "Leeuwarden", "Leiden",
    "Leidschendam-Voorburg", "Lelystad", "Maassluis", "Maastricht", "Meppel",
    "Middelburg", "Nieuwegein", "Nijkerk", "Nijmegen", "Noordoostpolder", "Oldenzaal",
    "Oosterhout", "Oss", "Papendrecht", "Purmerend", "Raalte", "Rheden", "Ridderkerk",
    "Rijssen-Holten", "Rijswijk", "Roermond", "Roosendaal", "Rozendaal", "Schiedam",
    "Sittard-Geleen", "Sneek", "Soest", "Spijkenisse", "Stadskanaal", "Steenwijkerland",
    "Terneuzen", "Tiel", "Tilburg", "Uden", "Utrecht", "Veenendaal", "Veghel", "Veldhoven",
    "Velsen", "Venlo", "Venray", "Vlaardingen", "Vlissingen", "Waalwijk", "Wageningen",
    "Weert", "Weesp", "Wijchen", "Winterswijk", "Woerden", "Zaanstad", "Zeist",
    "Zevenaar", "Zoetermeer", "Zutphen", "Zwijndrecht", "Zwolle", "'s-Hertogenbosch",
    "Goes", "Gorinchem", "Culemborg", "Barendrecht", "Bodegraven-Reeuwijk", "Boxtel",
    "Brunssum", "Bergeijk", "Coevorden", "Dronten", "Duiven", "Elburg", "Ermelo",
    "Geldermalsen", "Gennep", "Gilze en Rijen", "Goirle", "Halderberge", "Hattem",
    "Heemskerk", "Heemstede", "Heiloo", "Hellevoetsluis", "Hendrik-Ido-Ambacht",
    "Leusden", "Lisse", "Lochem", "Maarssen", "Medemblik", "Moerdijk", "Naarden",
    "Nieuwkoop", "Nunspeet", "Oldebroek", "Ommen", "Oud-Beijerland", "Putten",
    "Rhenen", "Sliedrecht", "Someren", "Son en Breugel", "Stein", "Tubbergen",
    "Urk", "Valkenswaard", "Voorschoten", "Vught", "Waalre", "Wierden", "Woudenberg",
    "Zaltbommel", "Zandvoort", "Zundert",
)

GEMEENTEN_BE: tuple[str, ...] = (
    "Aalst", "Aarschot", "Antwerpen", "Beringen", "Beveren", "Bilzen", "Blankenberge",
    "Boom", "Bornem", "Brasschaat", "Brugge", "Deinze", "Dendermonde", "Diest",
    "Diksmuide", "Dilbeek", "Eeklo", "Evergem", "Genk", "Gent", "Geel", "Geraardsbergen",
    "Halle", "Harelbeke", "Hasselt", "Heist-op-den-Berg", "Herentals", "Hoogstraten",
    "Ieper", "Izegem", "Knokke-Heist", "Kortrijk", "Lanaken", "Lebbeke", "Leuven",
    "Lier", "Lokeren", "Lommel", "Maaseik", "Machelen", "Mechelen", "Menen", "Mol",
    "Ninove", "Oostende", "Oudenaarde", "Overijse", "Poperinge", "Roeselare",
    "Ronse", "Schoten", "Sint-Niklaas", "Sint-Truiden", "Temse", "Tervuren",
    "Tielt", "Tienen", "Tongeren", "Torhout", "Turnhout", "Veurne", "Vilvoorde",
    "Waregem", "Wetteren", "Wevelgem", "Willebroek", "Zaventem", "Zele", "Zottegem",
    "Zwevegem",
)


@dataclass(frozen=True)
class Territorium:
    datum: _dt.date
    land: str          # "NL" of "BE"
    gemeenten: tuple[str, ...]
    branche: Branche
    cyclus_dagen: int  # na hoeveel dagen dit terrein pas terugkomt


_EPOCH = _dt.date(2026, 1, 1)


def territorium_voor(datum: _dt.date, gemeenten_per_dag: int = 4,
                    land: str | None = None,
                    branche_sleutel: str | None = None) -> Territorium:
    """Kies deterministisch het jachtgebied van vandaag.

    Geen willekeur en geen geheugen nodig: dezelfde datum geeft altijd dezelfde
    combinatie, en de cyclus is zo lang dat terrein jarenlang niet terugkeert.

    `land` en `branche_sleutel` overschrijven de rotatie. Dat is nodig omdat de
    twee markten verschillende belregels hebben: Belgische leads moeten eerst
    langs de DNCM-lijst voordat je mag bellen, dus wie vandaag wil bellen kiest
    NL. Het terrein blijft ook dan deterministisch uit de datum volgen.
    """
    dag = (datum - _EPOCH).days
    if land in ("NL", "BE"):
        gekozen_land = land
    else:
        # Even dagen Nederland, oneven dagen Vlaanderen: beide markten blijven lopen.
        gekozen_land = "NL" if dag % 2 == 0 else "BE"
    land = gekozen_land
    pool = GEMEENTEN_NL if land == "NL" else GEMEENTEN_BE
    ronde = dag // 2  # hoeveelste dag binnen dit land

    blokken = max(1, len(pool) // gemeenten_per_dag)

    # De branche loopt in de binnenste ring, het gemeenteblok in de buitenste.
    # Gevolg: elke dag een andere branche (zodat het belwerk afwisselend blijft
    # en niet drie maanden achter elkaar hoveniers is), en elk paar
    # (branche, blok) komt precies een keer voorbij voordat er iets herhaalt.
    branche = BRANCHES[ronde % len(BRANCHES)]
    if branche_sleutel:
        if branche_sleutel not in BRANCHE_OP_SLEUTEL:
            raise ValueError(
                f"onbekende branche {branche_sleutel!r}; kies uit: "
                + ", ".join(BRANCHE_OP_SLEUTEL)
            )
        branche = BRANCHE_OP_SLEUTEL[branche_sleutel]
    blok = (ronde // len(BRANCHES)) % blokken

    start = (blok * gemeenten_per_dag) % len(pool)
    gemeenten = tuple(pool[(start + i) % len(pool)] for i in range(gemeenten_per_dag))

    return Territorium(
        datum=datum,
        land=land,
        gemeenten=gemeenten,
        branche=branche,
        cyclus_dagen=blokken * len(BRANCHES) * 2,
    )
