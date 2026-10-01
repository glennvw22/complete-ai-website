"""Catalogus: branches, gemeenten en de deterministische territoriumrotatie.

Alles hier is pure data + pure functies, zodat het zonder netwerk testbaar is.
"""
from __future__ import annotations

import datetime as _dt
import re
import unicodedata
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
    # Geen tandartsen (Glenn, 1-10-2026): amenity=dentist en SBI 8623 staan hier
    # bewust niet meer in, en tandzorg wordt in de samenstelling ook op naam,
    # tags, SBI en websitedomein overgeslagen (zie is_tandzorg hieronder).
    Branche("zorg", "Fysio, huisartsen, opticiens en praktijken",
            (("amenity", "doctors"),
             ("healthcare", "physiotherapist"), ("healthcare", "psychotherapist"),
             ("shop", "optician"), ("healthcare", "podiatrist")),
            beldruk=1.0, online_afspraak=True,
            dienst_focus=("telefonist", "automatisering", "website", "seo"),
            sbi=("8621", "8691")),
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
# Branches die Glenn niet wil: tandzorg (1-10-2026, "geen enkele tandzorg- of
# tandartspraktijk in mijn leadslijst"). Onder tandarts valt: tandarts,
# tandartsenpraktijk, tandzorg, mondzorg, mondhygienist, orthodontist/
# orthodontie, implantologie, kaakchirurg, tandprothetica/tandtechniek,
# tandheelkundig centrum. Dezelfde regel staat in het dashboard
# (lib/betrouwbaar.ts, herkenUitgeslotenBranche), dat een lead uit tandzorg
# ook zelf nog uitsluit.
# --------------------------------------------------------------------------
TANDZORG_STAMMEN = (
    "tandarts", "tandzorg", "mondzorg", "mondhygien", "orthodont", "implantolog",
    "kaakchirurg", "mondkaak", "stomatolog", "tandprothet", "tandtechn", "tandlab",
    "tandheelkund", "parodont", "endodont", "gebitsprothe", "kunstgebit",
)
# Engels en Frans (Vlaanderen); "dental" niet binnen accidental/incidental/occidental.
_TANDZORG_VREEMD = re.compile(r"(?<!acci)(?<!inci)(?<!occi)dental|dentist|dentaire")
# Websites waarvan naam en domein het niet verraden maar die bevestigd tandzorg
# zijn (1-10-2026, paginatitel); gelijk aan de lijst in het dashboard.
BEKENDE_TANDZORG_DOMEINEN = (
    "lovadent.be", "uwmond.be", "orthogroep.be", "greetmulier.be",
    "tppkamstra.nl", "tand41.be", "mozo-wieze.be",
)
_OSM_TANDZORG = re.compile(
    r"(amenity|healthcare)\s*=\s*dentist\b"
    r"|healthcare:speciality\s*=[^;]*(dentist|orthodontics|oral_surgery|prosthodontics|endodontics|periodontics)",
    re.I)


def _woorden(tekst: str) -> list[str]:
    zonder = unicodedata.normalize("NFKD", tekst or "")
    zonder = "".join(c for c in zonder if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", zonder.lower())


def _heeft_tandzorgwoord(tekst: str) -> bool:
    return any(
        any(stam in woord for stam in TANDZORG_STAMMEN) or _TANDZORG_VREEMD.search(woord)
        for woord in _woorden(tekst)
    )


def _host(url: str) -> str:
    kaal = re.sub(r"^[a-z][a-z0-9+.-]*://", "", (url or "").strip().lower())
    return re.sub(r"^www\.", "", kaal.split("/")[0].split("?")[0])


def tandzorg_signalen(naam: str = "", branche: str = "", sbi: str = "", website: str = "",
                      email: str = "", osm_tags: dict | str | None = None) -> list[str]:
    """Waarop dit bedrijf als tandzorg is herkend (leeg = geen tandzorg)."""
    signalen: list[str] = []
    if _heeft_tandzorgwoord(naam):
        signalen.append("naam")
    if _heeft_tandzorgwoord(branche):
        signalen.append("branche")
    kaal = re.sub(r"\.", "", sbi or "")
    if re.search(r"(?<!\d)8623\d{0,2}(?!\d)", kaal) or _heeft_tandzorgwoord(sbi):
        signalen.append("sbi")
    host = _host(website)
    if host and any(_heeft_tandzorgwoord(label) for label in host.split(".")):
        signalen.append("websitedomein")
    if host and any(host == d or host.endswith("." + d) for d in BEKENDE_TANDZORG_DOMEINEN):
        signalen.append("bekende praktijk")
    mail_domein = (email or "").strip().lower().rpartition("@")[2]
    if mail_domein and any(_heeft_tandzorgwoord(label) for label in mail_domein.split(".")):
        signalen.append("e-maildomein")
    if isinstance(osm_tags, dict):
        osm_tags = ";".join(f"{k}={v}" for k, v in osm_tags.items())
    if osm_tags and _OSM_TANDZORG.search(osm_tags):
        signalen.append("osm-tag")
    return signalen


def is_tandzorg(bedrijf, kvk_resultaat=None) -> bool:
    """Is dit een tandzorg- of tandartspraktijk? Voor een Bedrijf uit bron_osm
    (naam, branche, website, email, osm_tags) en een optioneel KvkResultaat
    (sbi, sbi_omschrijving, handelsnaam)."""
    sbi = ""
    handelsnaam = ""
    if kvk_resultaat is not None:
        sbi = f"{getattr(kvk_resultaat, 'sbi', '')} {getattr(kvk_resultaat, 'sbi_omschrijving', '')}"
        handelsnaam = getattr(kvk_resultaat, "handelsnaam", "") or ""
    return bool(tandzorg_signalen(
        naam=f"{getattr(bedrijf, 'naam', '')} {handelsnaam}",
        sbi=sbi,
        website=getattr(bedrijf, "website", ""),
        email=getattr(bedrijf, "email", ""),
        osm_tags=getattr(bedrijf, "osm_tags", None),
    ))


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


def gemeente_blokken(land: str, gemeenten_per_dag: int = 4) -> list[tuple[str, ...]]:
    """Deel de gemeenten van een land op in blokken van vaste grootte."""
    pool = GEMEENTEN_NL if land == "NL" else GEMEENTEN_BE
    return [tuple(pool[i:i + gemeenten_per_dag])
            for i in range(0, len(pool), gemeenten_per_dag)]


def jachtvolgorde(terrein: Territorium, gemeenten_per_dag: int = 4):
    """De volgorde waarin gebieden worden afgezocht als er meer nodig is.

    Begint bij het terrein van vandaag en loopt dan verder: eerst dezelfde
    branche in aangrenzende gemeenteblokken, daarna de volgende branches. Zo
    blijft de dag herkenbaar (een branche waar je je op kunt voorbereiden),
    maar loop je nooit leeg omdat een gemeente te klein was.
    """
    blokken = gemeente_blokken(terrein.land, gemeenten_per_dag)
    if not blokken:
        return
    start_blok = 0
    for index, blok in enumerate(blokken):
        if blok and blok[0] == terrein.gemeenten[0]:
            start_blok = index
            break

    branche_index = BRANCHES.index(terrein.branche)
    branches = [BRANCHES[(branche_index + i) % len(BRANCHES)]
                for i in range(len(BRANCHES))]

    for branche in branches:
        for stap in range(len(blokken)):
            yield branche, blokken[(start_blok + stap) % len(blokken)]
