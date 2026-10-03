#!/usr/bin/env python3
"""Voorraadronde voor de vaste voorraad belbare NL-leads (stap 6, 2-10-2026).

Glenn, 2-10-2026: "minimaal 100 leads per dag die je kunt bellen, pas op het moment dat ik bel, zodat er weer nieuwe leads bijkomen."
Dit is de NL-pijplijn die de voorraad aanvult. De volgorde is bewust anders dan die van run.py (daar eerst KVK, dan de rest):

    1. kandidaten uit OpenStreetMap (gratis): alle toegestane branches, geen tandzorg, geen bekende keten, alleen met telefoonnummer,
       en geen kandidaat die het dashboard al kent
    2. de rechtspersoon, GRATIS bevestigd met de KVK Zoeken API (zie rechtspersoon_gratis hieronder): een regel van het type rechtspersoon met
       hetzelfde KVK-nummer, de geregistreerde naam draagt de wettelijke aanduiding B.V. of N.V., en precies één actieve vestiging
    3. de websitecheck (gratis, HTTP) en de import in het dashboard met baan BEL
       -> daarna doet het dashboard de rest: de websitekeuring in een echte Chrome met de redenen (keuring-dagelijks), de visuele
          bevestiging, de zoekcontrole van het huidige domein, de open-check, de ketenherkenning, het belbaar-bewijs per lead.

De BETAALDE Basisprofiel-bevraging (KVK, EUR 0,02) staat NERGENS in deze pijplijn. Er is voor dit script ook geen schakelaar die hem aanzet.
(Glenn gaf op 2-10-2026 eenmalig akkoord voor een plafond van EUR 10, alleen voor kandidaten met een sterke reden en alleen als de gratis route
niet volstaat; de gratis route volstaat voor BV en NV. De voorraadtaak gebruikt hem nooit.)

Gebruik:
    python3 leads/voorraad.py --gebieden 6                 een ronde over 6 nieuwe gebieden (branche x gemeenteblok)
    python3 leads/voorraad.py --gebieden 6 --geen-post     schrijf de CSV, verstuur niet
    python3 leads/voorraad.py --tijd-minuten 40            stop met nieuwe gebieden als de ronde zo lang loopt
    python3 leads/voorraad.py --status                     toon welke gebieden al gedaan zijn

Schrijft per ronde naar leads/uitvoer/voorraad/ en bewaart welke gebieden gedaan zijn in
~/Documents/Claude/Projects/Complete-AI/klantenjacht/voorraad/gebieden.json (hervatten kan altijd).
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import os
import re
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))

import belbaar as belbaar_mod       # noqa: E402
import bron_osm                      # noqa: E402
import catalogus                     # noqa: E402
import dashboard                     # noqa: E402
import ketens as ketens_mod          # noqa: E402
import kvk as kvk_mod                # noqa: E402
import run as run_mod                # noqa: E402
import score as score_mod            # noqa: E402
import website_check                 # noqa: E402

UITVOER = HIER / "uitvoer" / "voorraad"
STAND_MAP = Path.home() / "Documents/Claude/Projects/Complete-AI/klantenjacht/voorraad"
GEBIEDEN_PAD = STAND_MAP / "gebieden.json"
GEMEENTEN_PAD = STAND_MAP / "gemeenten_nl.json"   # alle gemeenten van PDOK/CBS (2-10-2026); de rotatie van de dagelijkse run kent er maar 163
STANDAARD_BLOKGROOTTE = 4

# Waar de meeste sterke redenen zitten (gemeten op de NL-leads van 2-10-2026: garage 7 van 20 betrouwbaar, kapsalon 2 van 26, horeca 7 van 134):
# een garage of kapsalon met alleen telefonisch boeken is de duidelijkste reden. Daarna de rest.
BRANCHE_VOLGORDE = (
    "garage", "kapsalon", "zorg", "sport", "horeca", "installatie", "bouw",
    "hovenier", "detailhandel", "zakelijk", "transport", "gastvrij",
)

# Verfijnde branches voor de uitbreiding van 3-10-2026 (installateurs, kappers en schoonheidssalons, fysiotherapie, rijscholen): alleen de OSM-tags die
# bij de afspraakbranche horen, onder de bestaande branchesleutel (de rest van het dashboard kent alleen die sleutels). De gedaan-sleutel in
# gebieden.json is de run-sleutel (installateur, kapper, fysio, rijschool), zodat de volledige branches (installatie, kapsalon, zorg, sport) hun eigen
# voortgang houden. Geen tandzorg, geen opticiens of huisartsen, geen tatoeage- of massagestudio's, geen groothandel (shop=trade).
EXTRA_BRANCHES: dict[str, "catalogus.Branche"] = {
    "installateur": catalogus.Branche(
        sleutel="installatie", naam="Installateurs (cv, loodgieter, elektra, airco)",
        osm=(("craft", "plumber"), ("craft", "electrician"), ("craft", "hvac"), ("craft", "gasfitter")),
        beldruk=1.0, online_afspraak=False, dienst_focus=("telefonist", "website", "sea", "seo"), sbi=("4322", "4321")),
    "kapper": catalogus.Branche(
        sleutel="kapsalon", naam="Kappers en schoonheidssalons",
        osm=(("shop", "hairdresser"), ("shop", "beauty"), ("shop", "nails")),
        beldruk=0.85, online_afspraak=True, dienst_focus=("website", "automatisering", "social", "seo"), sbi=("9602",)),
    "fysio": catalogus.Branche(
        sleutel="zorg", naam="Fysiotherapie", osm=(("healthcare", "physiotherapist"),),
        beldruk=1.0, online_afspraak=True, dienst_focus=("telefonist", "automatisering", "website", "seo"), sbi=("8690",)),
    "rijschool": catalogus.Branche(
        sleutel="sport", naam="Rijscholen", osm=(("amenity", "driving_school"),),
        beldruk=0.75, online_afspraak=True, dienst_focus=("automatisering", "website", "social", "seo"), sbi=("8553",)),
}
RUN_SLEUTEL = {id(b): k for k, b in EXTRA_BRANCHES.items()}


def branche_op_sleutel(sl: str):
    return EXTRA_BRANCHES.get(sl) or catalogus.BRANCHE_OP_SLEUTEL[sl]


# De wettelijke aanduiding in de geregistreerde naam van een BV of NV. Zelfde regels als kvkNaamIsBvOfNv in jarvis-dashboard/lib/belbaar-bewijs.ts
BV_NV_NAAM = re.compile(r"(^|[\s,.(])(b\.?\s?v|n\.?\s?v|besloten vennootschap|naamloze vennootschap)\.?(?=$|[\s,)])", re.I)
GEEN_BV_NAAM = re.compile(r"\b(v\.?\s?o\.?\s?f\.?|c\.?\s?v\.?|maatschap|eenmanszaak|stichting|vereniging)\b", re.I)


# ------------------------------------------------------------------ voorfilter op de eigen site (gratis, HTTP)
# De websitekeuring in een echte Chrome kost een halve minuut per site. Wat de voorpagina al verraadt, hoeft niet gekeurd en niet geimporteerd: een formule of netwerk van garages,
# een landelijke keten of meerdere vestigingen, een autohandel zonder werkplaats, en een site met een afspraakknop of boekplatform (dan geldt "afspraak zonder online boeken" niet).
# Een bedrijf zonder website valt hier nooit af. Elke afvaller krijgt zijn reden in het ronde-overzicht; er wordt niets definitiefs mee gemarkeerd (de gebieden en kandidaten zijn gratis).
FORMULE_RE = re.compile(r"(car[\s-]?team|bosch\s+car\s+service|auto[\s-]?first|autocrew|autotaalglas|vakgarage|asn\s+autoschade|autoschade\s+service\s+nederland|schadeherstel\s?friesland|profile\s+tyrecenter|euromaster|verg[oö]lst|kwik[\s-]?fit|maxxglas|carglass|master\s+garage|garage\s+select|rob\s+peetoom|jean\s+louis\s+david|anwb\s+rijopleiding|technische\s+unie)", re.I)
VESTIGINGEN_RE = re.compile(r"((?:\d+|twee|drie|vier|vijf|zes|zeven|acht|negen|tien|meerdere|diverse)\s+(?:vestigingen|filialen|locaties|winkels|showrooms)|onze\s+(?:vestigingen|filialen)|meer\s+dan\s+\d+\s+(?:winkels|vestigingen)|vestigingen\s+in\s+[A-Z])", re.I)
BOEKKNOP_RE = re.compile(r"<(a|button)\b([^>]*)>([\s\S]{0,300}?)</\1>", re.I)
BOEKWOORD_RE = re.compile(r"(afspraak|boek(?:en|ing)?\b|reserv|plan\s+(?:een|je|uw)|maak\s+(?:een|je|uw)|inschrijv|aanmeld|proefles"
                          r"|storing\w*\s+(?:melden|doorgeven|aanmelden|opgeven)|meld\w*\s+(?:een\s+|uw\s+|je\s+)?(?:storing|schade|defect|lekkage)"
                          r"|(?:onderhoud|service|reparatie|inspectie|keuring|schade|monteur|opname|advies)\w*\s+(?:aanvragen|aanvraag|inplannen|plannen|boeken))", re.I)
BOEKPLATFORM_RE = re.compile(r"(calendly|planity|treatwell|fresha|booksy|setmore|salonized|salonkee|onlineafspraken|simplybook|bookingkit|afspraakplanner|reservio|resengo|timify|appointlet|garageplanner|werkplaatsplanner|mijngarage)", re.I)


def voorfilter_site(url: str) -> str | None:
    """Geeft een reden om dit bedrijf niet te keuren en niet te importeren, of None."""
    status, _eind, body, _ssl = website_check._lees(url, timeout=12)
    if status != 200 or not body:
        return None
    html = body.decode("utf-8", "replace")
    tekst = re.sub(r"<[^>]+>", " ", re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", html))
    tekst = re.sub(r"\s+", " ", tekst)
    m = FORMULE_RE.search(tekst)
    if m:
        return f"formule of netwerk op de site: {m.group(1)}"
    m = VESTIGINGEN_RE.search(tekst)
    if m:
        return f"meerdere vestigingen op de site: {m.group(1)}"
    if BOEKPLATFORM_RE.search(html):
        return "boekplatform op de site"
    for k in BOEKKNOP_RE.finditer(html):
        knoptekst = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", k.group(3))).strip()
        if not knoptekst or len(knoptekst) > 60 or not BOEKWOORD_RE.search(knoptekst):
            continue
        href = (re.search(r"href=[\"']([^\"']*)", k.group(2), re.I) or [None, ""])[1]
        if href.lower().startswith(("tel:", "mailto:", "whatsapp:")):
            continue
        return f"knop of link '{knoptekst[:40]}' naar een afspraak of boeking"
    laag = tekst.lower()
    if "occasion" in laag and not re.search(r"werkplaats|onderhoud|reparatie|apk|schade|banden|monteur", laag):
        return "autohandel zonder werkplaats"
    return None


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


def _norm(tekst: str) -> str:
    tekst = unicodedata.normalize("NFKD", tekst or "")
    tekst = "".join(t for t in tekst if not unicodedata.combining(t))
    return " ".join(re.findall(r"[a-z0-9]+", tekst.lower()))


def kvk_naam_is_bv_of_nv(naam: str) -> str | None:
    n = (naam or "").strip()
    if not n or GEEN_BV_NAAM.search(n):
        return None
    m = BV_NV_NAAM.search(n)
    if not m:
        return None
    return "Naamloze Vennootschap" if re.match(r"(n\.?\s?v|naamloze)", m.group(2), re.I) else "Besloten Vennootschap"


# ------------------------------------------------------------------ gebieden
def lees_gebieden() -> dict:
    try:
        return json.loads(GEBIEDEN_PAD.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"gedaan": [], "rondes": 0}


def schrijf_gebieden(stand: dict) -> None:
    GEBIEDEN_PAD.parent.mkdir(parents=True, exist_ok=True)
    GEBIEDEN_PAD.write_text(json.dumps(stand, ensure_ascii=False, indent=1), encoding="utf-8")


def alle_blokken() -> list[tuple[str, ...]]:
    """De blokken van de dagelijkse rotatie (163 gemeenten) plus de overige gemeenten uit de PDOK-lijst, in blokken van vier."""
    blokken = list(catalogus.gemeente_blokken("NL", STANDAARD_BLOKGROOTTE))
    bekend = {g for b in blokken for g in b}
    try:
        extra = [g for g in json.loads(GEMEENTEN_PAD.read_text(encoding="utf-8"))["gemeenten"] if g not in bekend and '"' not in g]
    except (OSError, ValueError, KeyError):
        extra = []
    blokken += [tuple(extra[i:i + STANDAARD_BLOKGROOTTE]) for i in range(0, len(extra), STANDAARD_BLOKGROOTTE)]
    return blokken


def sleutel_van(branche, blok) -> str:
    return f"{RUN_SLEUTEL.get(id(branche), branche.sleutel)}|{','.join(blok)}"


def seed_historie(stand: dict) -> None:
    """De gebieden die de dagelijkse leadsmachine al heeft afgezocht (territorium_voor per NL-dag sinds 3-9-2026) staan als gedaan: de kandidaten van
    daar kent het dashboard al (osm-id), dus opnieuw afzoeken kost tijd en levert niets."""
    if stand.get("historie_geseed"):
        return
    gedaan = set(stand.get("gedaan", []))
    dag = _dt.date(2026, 9, 3)
    while dag <= _dt.date(2026, 10, 2):
        try:
            terrein = catalogus.territorium_voor(dag, STANDAARD_BLOKGROOTTE, land="NL")
            gedaan.add(sleutel_van(terrein.branche, terrein.gemeenten))
        except Exception:  # noqa: BLE001
            pass
        dag += _dt.timedelta(days=1)
    stand["gedaan"] = sorted(gedaan)
    stand["historie_geseed"] = True
    schrijf_gebieden(stand)


def volgende_gebieden(aantal: int, stand: dict, branches: list[str]):
    """De volgende (branche, gemeenteblok)-combinaties die nog niet gedaan zijn, in de volgorde van BRANCHE_VOLGORDE, dan blok voor blok.
    Een blok loopt steeds verder, zodat een branche eerst over heel Nederland gaat voordat de volgende begint? Nee: één blok per branche per slag,
    zodat elke ronde een mengsel is van branches (een mengsel geeft meer verschillende redenen)."""
    blokken = alle_blokken()
    gedaan = set(stand.get("gedaan", []))
    gekozen = []
    # per branche een eigen pointer over de blokken: de eerste nog niet gedane
    per_branche = {}
    for sl in branches:
        branche = branche_op_sleutel(sl)
        per_branche[sl] = [b for b in blokken if sleutel_van(branche, b) not in gedaan]
    while len(gekozen) < aantal and any(per_branche.values()):
        for sl in branches:
            if per_branche[sl] and len(gekozen) < aantal:
                gekozen.append((branche_op_sleutel(sl), per_branche[sl].pop(0)))
    return gekozen


# ------------------------------------------------------------------ dashboard
def _dashboard_get(pad: str) -> dict:
    basis = os.environ.get("DASHBOARD_URL", "https://complete-ai-production.up.railway.app").rstrip("/")
    sleutel = os.environ.get("LEADS_IMPORT_SLEUTEL", "") or kvk_mod._uit_kluis("LEADS_IMPORT_SLEUTEL")
    verzoek = urllib.request.Request(basis + pad, headers={"x-leads-sleutel": sleutel})
    with urllib.request.urlopen(verzoek, timeout=120) as antwoord:
        return json.loads(antwoord.read().decode("utf-8"))


def bekende_in_dashboard() -> tuple[set[str], set[str]]:
    try:
        j = _dashboard_get("/api/leads/voorraad?lijst=bekend")
        return set(j.get("osm", [])), set(str(x) for x in j.get("kvk", []))
    except Exception as fout:  # noqa: BLE001
        log(f"[dashboard] bekende leads niet op te halen ({type(fout).__name__}: {fout}); ga door zonder dubbelcontrole op het dashboard")
        return set(), set()


# ------------------------------------------------------------------ KVK, gratis
def _significante_tokens(naam: str) -> set[str]:
    generiek = set(getattr(ketens_mod, "_GENERIEKE_WOORDEN", ())) | {"garage", "autobedrijf", "autoschade", "kapsalon", "kapper", "kappers", "salon", "bv", "nv", "b", "v", "van", "de", "het", "den", "der", "en",
                                                                      "rijschool", "autorijschool", "rijopleiding", "rijopleidingen", "fysiotherapie", "fysio", "fysiotherapeut", "praktijk", "installatie", "installatiebedrijf",
                                                                      "installatietechniek", "installateur", "techniek", "elektro", "elektrotechniek", "loodgieter", "loodgietersbedrijf", "schoonheidssalon",
                                                                      "schoonheidsinstituut", "nagelstudio", "beautysalon", "beauty", "hairstyling", "haarstudio", "bandencentrale", "carrosserie"}
    return {w for w in _norm(naam).split() if len(w) >= 4 and w not in generiek}


def kvk_op_adres(client: kvk_mod.KvkClient, bedrijf) -> kvk_mod.KvkResultaat | None:
    """Terugval als de naam niet matcht: wie staat op dit adres in het handelsregister? Alleen een hoofdvestiging waarvan de naam minstens één
    betekenisvol woord met de naam van de kandidaat deelt telt (een gelijk adres alleen is geen bewijs: Boerenbond en Pets Place, 17-9-2026)."""
    postcode = re.sub(r"\s", "", bedrijf.postcode or "").upper()
    nummer = re.match(r"\d+", (bedrijf.huisnummer or "").strip())
    if not postcode or not nummer:
        return None
    data, fout = client._get(kvk_mod.ZOEKEN, {"postcode": postcode, "huisnummer": nummer.group(0), "resultatenPerPagina": 20})
    if fout or not data:
        return None
    eigen = _significante_tokens(bedrijf.naam)
    for r in data.get("resultaten") or []:
        if r.get("type") != "hoofdvestiging" or not r.get("kvkNummer"):
            continue
        if eigen & _significante_tokens(r.get("naam", "")):
            res = kvk_mod.KvkResultaat(gevonden=True, kvk_nummer=str(r["kvkNummer"]), handelsnaam=r.get("naam", ""), zoek_type="hoofdvestiging", bron="zoeken")
            return res
    return None


# Een beheer-, holding- of vastgoedmaatschappij drijft de zaak meestal niet zelf (Sampermans Beheer B.V. naast Autobandencentrale Sampermans B.V., 2-10-2026).
# Zelfde regel als kvkNaamIsHolding in jarvis-dashboard/lib/belbaar-bewijs.ts.
HOLDING_RE = re.compile(r"\b(beheer|holding|participaties?|vastgoed|investeringen|management)\b", re.I)


def exploitant_zoeken(client: kvk_mod.KvkClient, bedrijf, holding_nr: str) -> kvk_mod.KvkResultaat | None:
    """De naam gaf een holding: zoek op naam en plaats een hoofdvestiging van een andere, niet-holding BV met minstens één betekenisvol woord gelijk
    aan de kandidaat en (als de straat bekend is) in dezelfde straat."""
    data, fout = client._get(kvk_mod.ZOEKEN, {"naam": bedrijf.naam, "plaats": bedrijf.gemeente, "resultatenPerPagina": 20})
    if fout or not data:
        return None
    eigen = _significante_tokens(bedrijf.naam)
    for r in data.get("resultaten") or []:
        if r.get("type") != "hoofdvestiging" or not r.get("kvkNummer") or str(r["kvkNummer"]) == holding_nr:
            continue
        naam = r.get("naam", "")
        if HOLDING_RE.search(naam) or not kvk_naam_is_bv_of_nv(naam):
            continue
        adres = (r.get("adres") or {}).get("binnenlandsAdres") or {}
        if bedrijf.straat and adres.get("straatnaam") and _norm(adres["straatnaam"]) != _norm(bedrijf.straat):
            continue
        if eigen & _significante_tokens(naam):
            return kvk_mod.KvkResultaat(gevonden=True, kvk_nummer=str(r["kvkNummer"]), handelsnaam=naam, zoek_type="hoofdvestiging", bron="zoeken")
    return None


def rechtspersoon_gratis(client: kvk_mod.KvkClient, bedrijf, bekend_kvk: set[str], gezien_kvk: set[str]) -> tuple[kvk_mod.KvkResultaat | None, str]:
    """De gratis route. Geeft (resultaat, "") bij een bevestigde BV/NV met één vestiging, anders (None, reden).

    Bewijsregel (gemeten op 2-10-2026 tegen 90 leads met bekende rechtsvorm, 82 van 83 BV's slagen, alle stichtingen en verenigingen niet):
      - de Zoeken API (v2) geeft bij ?kvkNummer=X een regel type 'rechtspersoon' met hetzelfde KVK-nummer;
      - de in KVK geregistreerde naam van die rechtspersoon draagt de wettelijke aanduiding B.V. of N.V. (een V.O.F., C.V. en maatschap hebben OOK een
        rechtspersoon-regel, zonder die aanduiding; een eenmanszaak heeft er geen);
      - er is precies één actieve vestiging, op de plaats (en straat) van de kandidaat.
    Een naam met "B.V." in OpenStreetMap of in de lead telt NIET: het gaat om de naam die KVK zelf bij de rechtspersoon bewaart.
    """
    res = client.zoek(bedrijf.naam, bedrijf.gemeente, met_basisprofiel=False)
    if not res.gevonden:
        res = kvk_op_adres(client, bedrijf)
        if res is None:
            return None, "niet in KVK op naam en plaats, ook niet op adres"
    if res.zoek_type == "nevenvestiging":
        return None, "nevenvestiging (filiaal)"
    nr = res.kvk_nummer
    if not nr:
        return None, "geen KVK-nummer"
    if nr in bekend_kvk or nr in gezien_kvk:
        return None, "KVK-nummer al bekend (dubbel)"
    data, fout = client._get(kvk_mod.ZOEKEN, {"kvkNummer": nr, "resultatenPerPagina": 50})
    if fout or not data:
        return None, f"KVK-nummer niet op te zoeken ({fout or 'leeg'})"
    regels = [r for r in (data.get("resultaten") or []) if str(r.get("kvkNummer")) == nr]
    rp = next((r for r in regels if r.get("type") == "rechtspersoon"), None)
    if not rp:
        return None, "geen rechtspersoon-regel (eenmanszaak of niet bevestigd)"
    if HOLDING_RE.search(rp.get("naam", "")):
        alt = exploitant_zoeken(client, bedrijf, nr)
        if alt is None:
            return None, f"alleen een beheer- of holdingmaatschappij gevonden ({rp.get('naam', '')})"
        res = alt
        nr = res.kvk_nummer
        if nr in bekend_kvk or nr in gezien_kvk:
            return None, "KVK-nummer al bekend (dubbel)"
        data, fout = client._get(kvk_mod.ZOEKEN, {"kvkNummer": nr, "resultatenPerPagina": 50})
        if fout or not data:
            return None, f"KVK-nummer niet op te zoeken ({fout or 'leeg'})"
        regels = [r for r in (data.get("resultaten") or []) if str(r.get("kvkNummer")) == nr]
        rp = next((r for r in regels if r.get("type") == "rechtspersoon"), None)
        if not rp or HOLDING_RE.search(rp.get("naam", "")):
            return None, "geen rechtspersoon-regel bij de exploitant"
    vorm = kvk_naam_is_bv_of_nv(rp.get("naam", ""))
    if not vorm:
        return None, f"geregistreerde naam draagt geen B.V./N.V. ({rp.get('naam', '')})"
    vestigingen = [r for r in regels if r.get("vestigingsnummer")]
    if len(vestigingen) != 1:
        return None, f"{len(vestigingen)} actieve vestigingen"
    hoofd = vestigingen[0]
    adres = (hoofd.get("adres") or {}).get("binnenlandsAdres") or {}
    if _norm(adres.get("plaats", "")) != _norm(bedrijf.gemeente) and _norm(adres.get("plaats", "")) != _norm(bedrijf.plaats):
        return None, f"KVK-vestiging staat in {adres.get('plaats', '?')}, kandidaat in {bedrijf.gemeente}"
    if bedrijf.straat and adres.get("straatnaam") and _norm(adres["straatnaam"]) != _norm(bedrijf.straat):
        return None, f"andere straat ({adres.get('straatnaam')} tegenover {bedrijf.straat})"
    res.rechtsvorm = vorm
    res.is_rechtspersoon = True
    res.vestigingen = 1
    res.bron = "zoeken"
    res.handelsnaam = hoofd.get("naam") or res.handelsnaam
    return res, ""


# ------------------------------------------------------------------ een ronde
def draai_ronde(gebieden, geen_post: bool, tijd_minuten: float | None) -> dict:
    t0 = time.time()
    tel = {"gebieden": 0, "osm_kandidaten": 0, "met_telefoon": 0, "al_bekend": 0, "tandzorg": 0, "keten_naam": 0, "keten_oogst": 0,
           "kvk_gezocht": 0, "kvk_afgevallen": {}, "bv_een_vestiging": 0, "keten_spreiding": 0, "geleverd": 0, "osm_fouten": 0}
    bekend_osm, bekend_kvk = bekende_in_dashboard()
    stand = lees_gebieden()
    bedrijven = []
    gezien = set()
    for branche, blok in gebieden:
        if tijd_minuten and (time.time() - t0) / 60 > tijd_minuten:
            log(f"[tijd] {tijd_minuten} minuten bereikt: geen nieuwe gebieden meer")
            break
        gevonden, fouten = bron_osm.haal_bedrijven(list(blok), branche, "NL", logger=log)
        tel["osm_fouten"] += len(fouten)
        if fouten and not gevonden:
            # geen gebied als gedaan markeren als de bron faalde: het komt een volgende keer opnieuw aan de beurt
            log(f"[bron] {branche.sleutel} {blok[0]}...: mislukt ({fouten[:1]})")
            continue
        nieuw = 0
        for b in gevonden:
            sleutel = (b.naam.lower(), b.adres.lower())
            if sleutel in gezien:
                continue
            gezien.add(sleutel)
            bedrijven.append(b)
            nieuw += 1
        tel["gebieden"] += 1
        stand["gedaan"].append(sleutel_van(branche, blok))
        schrijf_gebieden(stand)
        log(f"[bron] +{nieuw} uit {branche.sleutel} {', '.join(blok)} (totaal {len(bedrijven)})")
    tel["osm_kandidaten"] = len(bedrijven)

    # 1. gratis filters: telefoon, al bekend, tandzorg, keten op naam, keten door spreiding in de oogst
    met_nummer = [b for b in bedrijven if b.telefoon]
    tel["met_telefoon"] = len(met_nummer)
    nieuwe = [b for b in met_nummer if b.osm_id not in bekend_osm]
    tel["al_bekend"] = len(met_nummer) - len(nieuwe)
    oogst_index = ketens_mod.bouw_oogst_index(bedrijven)
    oogst_domein_index = ketens_mod.bouw_oogst_domein_index(bedrijven)
    kandidaten = []
    for b in nieuwe:
        if catalogus.is_tandzorg(b):
            tel["tandzorg"] += 1
        elif ketens_mod.is_landelijke_keten(b.naam):
            tel["keten_naam"] += 1
        elif ketens_mod.is_landelijke_spreiding_in_oogst(oogst_index, b.naam, oogst_domein_index):
            tel["keten_oogst"] += 1
        else:
            kandidaten.append(b)
    log(f"[filter] {len(kandidaten)} kandidaten over van {len(nieuwe)} nieuwe met telefoon")

    # 2. de rechtspersoon, gratis
    client = kvk_mod.KvkClient()
    werkt, bericht = client.zelftest()
    if not werkt:
        log(f"[kvk] werkt niet: {bericht}")
        return {"fout": f"KVK werkt niet: {bericht}", **tel}
    gezien_kvk: set[str] = set()
    bevestigd = []
    uitkomsten: list[dict] = []
    for i, b in enumerate(kandidaten, 1):
        if tijd_minuten and (time.time() - t0) / 60 > tijd_minuten * 1.5:
            log("[tijd] ruim over de tijd: stop met zoeken in KVK; wat bevestigd is gaat mee")
            break
        res, reden = rechtspersoon_gratis(client, b, bekend_kvk, gezien_kvk)
        tel["kvk_gezocht"] += 1
        uitkomsten.append({"osm_id": b.osm_id, "naam": b.naam, "plaats": b.gemeente, "branche": b.branche, "adres": b.adres, "uitkomst": reden or "bevestigd", "kvk": getattr(res, "kvk_nummer", "") if res else ""})
        if res is None:
            tel["kvk_afgevallen"][reden.split(" (")[0].split(",")[0]] = tel["kvk_afgevallen"].get(reden.split(" (")[0].split(",")[0], 0) + 1
            continue
        # laag 2 (gratis): dezelfde naam landelijk verspreid over meer vestigingen onder eigen rechtspersonen (Tuinland)
        if ketens_mod.is_landelijke_spreiding(client, res.handelsnaam or b.naam, b.gemeente):
            tel["keten_spreiding"] += 1
            continue
        gezien_kvk.add(res.kvk_nummer)
        bevestigd.append((b, res))
        tel["bv_een_vestiging"] += 1
        if i % 50 == 0:
            log(f"[kvk] {i}/{len(kandidaten)} gezocht, {len(bevestigd)} bevestigd")
    log(f"[kvk] {tel['kvk_gezocht']} gratis zoekopdrachten, {len(bevestigd)} bevestigde BV/NV met één vestiging")

    # 2b. voorfilter op de eigen site: formule, meerdere vestigingen, boekknop, autohandel
    tel["voorfilter_afgevallen"] = {}
    behouden = []
    websites = [b.website for b, _ in bevestigd if b.website]
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=8) as pool:
        uitslag = dict(zip(websites, pool.map(lambda u: (lambda: voorfilter_site(u))() if u else None, websites)))
    for b, res in bevestigd:
        reden = uitslag.get(b.website) if b.website else None
        if reden:
            kort = reden.split(":")[0]
            tel["voorfilter_afgevallen"][kort] = tel["voorfilter_afgevallen"].get(kort, 0) + 1
            uitkomsten.append({"osm_id": b.osm_id, "naam": b.naam, "plaats": b.gemeente, "voorfilter": reden})
            continue
        behouden.append((b, res))
    log(f"[voorfilter] {len(bevestigd) - len(behouden)} van {len(bevestigd)} afgevallen op de eigen site: {tel['voorfilter_afgevallen']}")
    bevestigd = behouden

    # 3. websitecheck (gratis) en rijen
    urls = [b.website for b, _ in bevestigd if b.website]
    rapporten = website_check.controleer_veel(urls) if urls else {}
    rijen = []
    for b, res in bevestigd:
        site = rapporten.get(website_check._normaliseer(b.website)) if b.website else None
        if not b.email and site and site.emails:
            b.email = site.emails[0]
        branche = catalogus.BRANCHE_OP_SLEUTEL.get(b.branche) or next((x for x in catalogus.BRANCHES if x.naam == b.branche), None)
        if branche is None:
            continue
        beoordeling = score_mod.beoordeel(b, site, res, branche)
        belbaarheid = belbaar_mod.beoordeel_belbaarheid(b, res, None, None)
        if not belbaarheid.mag_bellen:
            continue
        rij = run_mod.naar_rij(b, site, res, beoordeling, belbaarheid)
        rijen.append(rij)
    tel["geleverd"] = len(rijen)

    UITVOER.mkdir(parents=True, exist_ok=True)
    stand = lees_gebieden()
    stand["rondes"] = stand.get("rondes", 0) + 1
    schrijf_gebieden(stand)
    naam = f"ronde-{stand['rondes']:03d}-{_dt.datetime.now().strftime('%Y%m%d-%H%M')}"
    csv_pad = UITVOER / f"{naam}.csv"
    with csv_pad.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=run_mod.CSV_KOLOMMEN)
        w.writeheader()
        w.writerows(rijen)
    samenvatting = {"ronde": stand["rondes"], "minuten": round((time.time() - t0) / 60, 1), "csv": str(csv_pad), "kvk_betaald": 0, **tel}
    (UITVOER / f"{naam}.json").write_text(json.dumps(samenvatting, ensure_ascii=False, indent=1), encoding="utf-8")
    (UITVOER / f"{naam}-kandidaten.jsonl").write_text("\n".join(json.dumps(u, ensure_ascii=False) for u in uitkomsten), encoding="utf-8")
    if geen_post:
        log("[post] overgeslagen (--geen-post)")
    elif rijen:
        dashboard.stuur_naar_dashboard(str(csv_pad))
    return samenvatting


def main() -> int:
    # de koppeling met het dashboard: adres en sleutel (de sleutel komt uit de sleutelkluis en wordt nooit getoond)
    os.environ.setdefault("DASHBOARD_URL", "https://complete-ai-production.up.railway.app")
    if not os.environ.get("LEADS_IMPORT_SLEUTEL"):
        os.environ["LEADS_IMPORT_SLEUTEL"] = kvk_mod._uit_kluis("LEADS_IMPORT_SLEUTEL")
    p = argparse.ArgumentParser(description="Voorraadronde NL (gratis rechtspersoon-bewijs)")
    p.add_argument("--gebieden", type=int, default=6, help="hoeveel nieuwe gebieden (branche x gemeenteblok) in deze ronde")
    p.add_argument("--branches", default=",".join(BRANCHE_VOLGORDE), help="komma-gescheiden, in volgorde van voorkeur")
    p.add_argument("--tijd-minuten", type=float, default=None, help="stop met nieuwe gebieden na zoveel minuten")
    p.add_argument("--geen-post", action="store_true")
    p.add_argument("--status", action="store_true")
    a = p.parse_args()

    stand = lees_gebieden()
    seed_historie(stand)
    if a.status:
        print(json.dumps({"gebieden_gedaan": len(stand.get("gedaan", [])), "rondes": stand.get("rondes", 0)}, indent=1))
        return 0
    branches = [b.strip() for b in a.branches.split(",") if b.strip()]
    for b in branches:
        if b not in catalogus.BRANCHE_OP_SLEUTEL and b not in EXTRA_BRANCHES:
            print(f"onbekende branche {b!r}; kies uit {', '.join(list(catalogus.BRANCHE_OP_SLEUTEL) + list(EXTRA_BRANCHES))}", file=sys.stderr)
            return 2
    gebieden = volgende_gebieden(a.gebieden, stand, branches)
    if not gebieden:
        print(json.dumps({"fout": "alle gebieden zijn gedaan"}))
        return 1
    log(f"[plan] {len(gebieden)} gebieden: " + "; ".join(f"{b.sleutel} {bl[0]}..." for b, bl in gebieden))
    samenvatting = draai_ronde(gebieden, a.geen_post, a.tijd_minuten)
    print(json.dumps(samenvatting, ensure_ascii=False, indent=1))
    return 0 if "fout" not in samenvatting else 1


if __name__ == "__main__":
    raise SystemExit(main())
