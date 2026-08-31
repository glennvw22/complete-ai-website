#!/usr/bin/env python3
"""Dagelijkse lead-run voor Complete AI.

Gebruik:
    python3 leads/run.py                      # vandaag, standaard 100 leads
    python3 leads/run.py --aantal 150
    python3 leads/run.py --datum 2026-09-04   # herhaalbaar, voor testen
    python3 leads/run.py --geen-kvk           # sla KVK-verrijking over
    python3 leads/run.py --diagnose           # alleen bronnen testen

Schrijft naar leads/uitvoer/<datum>/ (bewust NIET in git: het is een openbare
repository en dit zijn bedrijfsgegevens).
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import os
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))

import bron_osm                      # noqa: E402
import catalogus                     # noqa: E402
import kvk as kvk_mod                # noqa: E402
import score as score_mod            # noqa: E402
import website_check                 # noqa: E402

UITVOER = HIER / "uitvoer"

CSV_KOLOMMEN = [
    "score", "zekerheid", "beste_dienst", "baan", "bedrijf", "gemeente", "land",
    "branche", "telefoon", "email", "website", "website_status", "rechtsvorm",
    "kvk_nummer", "sbi", "adres", "signalen", "osm_id",
]


def log(*args):
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- diagnose
def diagnose(kvk_client: kvk_mod.KvkClient) -> dict:
    """Beantwoordt in een keer: werken mijn bronnen vandaag, ja of nee."""
    uitslag = {}

    proef = catalogus.BRANCHE_OP_SLEUTEL["kapsalon"]
    bedrijven, fouten = bron_osm.haal_bedrijven(["Zwolle"], proef, "NL", logger=log)
    uitslag["osm"] = {
        "werkt": bool(bedrijven),
        "aantal": len(bedrijven),
        "fouten": fouten[:3],
        "uitleg": (f"OpenStreetMap werkt: {len(bedrijven)} kapsalons in Zwolle."
                   if bedrijven else
                   "OpenStreetMap onbereikbaar - zonder deze bron is er geen bulklijst."),
    }

    werkt, bericht = kvk_client.zelftest()
    uitslag["kvk"] = {"werkt": werkt, "uitleg": bericht}

    rapport = website_check.controleer("https://complete-ai.nl")
    uitslag["websitecheck"] = {
        "werkt": rapport.bereikbaar,
        "uitleg": (f"Websitecheck werkt (complete-ai.nl gaf status {rapport.status})."
                   if rapport.bereikbaar else
                   f"Websitecheck kan niet naar buiten: {rapport.fout}"),
    }
    return uitslag


# ---------------------------------------------------------------- hoofdrun
def draai(datum: _dt.date, aantal: int, gebruik_kvk: bool,
          kvk_diepte: int, gemeenten_per_dag: int) -> dict:
    terrein = catalogus.territorium_voor(datum, gemeenten_per_dag=gemeenten_per_dag)
    kvk_client = kvk_mod.KvkClient() if gebruik_kvk else kvk_mod.KvkClient(sleutel="")
    kvk_werkt, kvk_bericht = kvk_client.zelftest()

    log(f"[plan] {terrein.datum} {terrein.land} | {terrein.branche.naam} "
        f"| {', '.join(terrein.gemeenten)}")

    bedrijven, osm_fouten = bron_osm.haal_bedrijven(
        list(terrein.gemeenten), terrein.branche, terrein.land, logger=log
    )

    # Als het terrein te dun is, breiden we uit naar het volgende blok in
    # plaats van met lege handen te stoppen.
    extra_dagen = 0
    while len(bedrijven) < aantal * 1.5 and extra_dagen < 6:
        extra_dagen += 2 if terrein.land == "NL" else 2
        buur = catalogus.territorium_voor(
            datum + _dt.timedelta(days=extra_dagen), gemeenten_per_dag=gemeenten_per_dag
        )
        if buur.land != terrein.land:
            continue
        log(f"[uitbreiding] te weinig bedrijven ({len(bedrijven)}), "
            f"erbij: {', '.join(buur.gemeenten)}")
        extra, fouten = bron_osm.haal_bedrijven(
            list(buur.gemeenten), terrein.branche, terrein.land, logger=log
        )
        osm_fouten += fouten
        bekend = {(b.naam.lower(), b.adres.lower()) for b in bedrijven}
        bedrijven += [b for b in extra
                      if (b.naam.lower(), b.adres.lower()) not in bekend]
        if not extra:
            break

    log(f"[bron] {len(bedrijven)} bedrijven uit OpenStreetMap")

    # Websites parallel controleren.
    urls = [b.website for b in bedrijven if b.website]
    log(f"[web] {len(urls)} websites controleren")
    site_rapporten = website_check.controleer_veel(urls) if urls else {}

    # Voorlopige score zonder KVK, om te bepalen wie de KVK-calls waard is.
    voorlopig = []
    for bedrijf in bedrijven:
        site = site_rapporten.get(website_check._normaliseer(bedrijf.website)) \
            if bedrijf.website else None
        beoordeling = score_mod.beoordeel(bedrijf, site, None, terrein.branche)
        voorlopig.append((bedrijf, site, beoordeling))
    voorlopig.sort(key=lambda r: -r[2].score)

    # KVK alleen voor de kop van de lijst: elke call kost geld.
    definitief = []
    kvk_gedaan = 0
    for index, (bedrijf, site, _) in enumerate(voorlopig):
        resultaat = None
        if kvk_werkt and terrein.land == "NL" and index < kvk_diepte:
            resultaat = kvk_client.zoek(bedrijf.naam, bedrijf.gemeente)
            kvk_gedaan += 1
        beoordeling = score_mod.beoordeel(bedrijf, site, resultaat, terrein.branche)
        definitief.append((bedrijf, site, resultaat, beoordeling))
    definitief.sort(key=lambda r: -r[3].score)

    log(f"[kvk] {kvk_gedaan} bedrijven verrijkt ({kvk_bericht})")

    return {
        "terrein": terrein,
        "rijen": definitief[:aantal],
        "totaal_gevonden": len(bedrijven),
        "osm_fouten": osm_fouten,
        "kvk_werkt": kvk_werkt,
        "kvk_bericht": kvk_bericht,
        "kvk_gedaan": kvk_gedaan,
    }


def naar_rij(bedrijf, site, kvk_resultaat, beoordeling) -> dict:
    website_status = "geen website bekend"
    if bedrijf.website and site is not None:
        if not site.bereikbaar:
            website_status = f"onbereikbaar ({site.fout})"
        elif site.alleen_social:
            website_status = "alleen social"
        elif site.geparkeerd:
            website_status = "geparkeerd/in aanbouw"
        else:
            kenmerken = []
            kenmerken.append("https" if site.https else "GEEN https")
            kenmerken.append("mobiel" if site.mobiel_geschikt else "NIET mobiel")
            if site.copyright_jaar:
                kenmerken.append(f"(c) {site.copyright_jaar}")
            kenmerken.append(f"{site.laadtijd_ms} ms")
            website_status = ", ".join(kenmerken)
    elif bedrijf.website:
        website_status = "niet gecontroleerd"

    return {
        "score": beoordeling.score,
        "zekerheid": beoordeling.zekerheid,
        "beste_dienst": score_mod.dienstnaam(beoordeling.beste_dienst),
        "baan": kvk_resultaat.baan if kvk_resultaat else "MAIL",
        "bedrijf": bedrijf.naam,
        "gemeente": bedrijf.gemeente,
        "land": bedrijf.land,
        "branche": bedrijf.branche,
        "telefoon": bedrijf.telefoon,
        "email": bedrijf.email,
        "website": bedrijf.website,
        "website_status": website_status,
        "rechtsvorm": kvk_resultaat.rechtsvorm if kvk_resultaat else "",
        "kvk_nummer": kvk_resultaat.kvk_nummer if kvk_resultaat else "",
        "sbi": (f"{kvk_resultaat.sbi} {kvk_resultaat.sbi_omschrijving}".strip()
                if kvk_resultaat else ""),
        "adres": bedrijf.adres,
        "signalen": beoordeling.redenen,
        "osm_id": bedrijf.osm_id,
    }


def schrijf(uitslag: dict, map_pad: Path) -> dict:
    map_pad.mkdir(parents=True, exist_ok=True)
    rijen = [naar_rij(*r) for r in uitslag["rijen"]]

    csv_pad = map_pad / "leads.csv"
    with csv_pad.open("w", newline="", encoding="utf-8") as bestand:
        schrijver = csv.DictWriter(bestand, fieldnames=CSV_KOLOMMEN)
        schrijver.writeheader()
        schrijver.writerows(rijen)

    per_dienst: dict[str, int] = {}
    for rij in rijen:
        per_dienst[rij["beste_dienst"]] = per_dienst.get(rij["beste_dienst"], 0) + 1

    terrein = uitslag["terrein"]
    samenvatting = {
        "datum": str(terrein.datum),
        "land": terrein.land,
        "branche": terrein.branche.naam,
        "gemeenten": list(terrein.gemeenten),
        "cyclus_dagen": terrein.cyclus_dagen,
        "bedrijven_uit_bron": uitslag["totaal_gevonden"],
        "leads_geleverd": len(rijen),
        "per_dienst": per_dienst,
        "bel_leads": sum(1 for r in rijen if r["baan"] == "BEL"),
        "mail_leads": sum(1 for r in rijen if r["baan"] == "MAIL"),
        "zekerheid_hoog": sum(1 for r in rijen if r["zekerheid"] == "hoog"),
        "kvk_werkt": uitslag["kvk_werkt"],
        "kvk_bericht": uitslag["kvk_bericht"],
        "kvk_verrijkt": uitslag["kvk_gedaan"],
        "osm_fouten": uitslag["osm_fouten"][:5],
        "csv": str(csv_pad),
    }
    (map_pad / "samenvatting.json").write_text(
        json.dumps(samenvatting, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (map_pad / "leads.json").write_text(
        json.dumps(rijen, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return samenvatting


def main() -> int:
    ontleder = argparse.ArgumentParser(description="Lead-run Complete AI")
    ontleder.add_argument("--datum", default="")
    ontleder.add_argument("--aantal", type=int, default=100)
    ontleder.add_argument("--gemeenten", type=int, default=4)
    ontleder.add_argument("--kvk-diepte", type=int, default=40,
                          help="voor hoeveel topleads KVK wordt geraadpleegd")
    ontleder.add_argument("--geen-kvk", action="store_true")
    ontleder.add_argument("--diagnose", action="store_true")
    argumenten = ontleder.parse_args()

    if argumenten.diagnose:
        uitslag = diagnose(kvk_mod.KvkClient())
        print(json.dumps(uitslag, ensure_ascii=False, indent=2))
        return 0 if uitslag["osm"]["werkt"] else 1

    datum = (_dt.date.fromisoformat(argumenten.datum) if argumenten.datum
             else _dt.date.today())
    uitslag = draai(datum, argumenten.aantal, not argumenten.geen_kvk,
                    argumenten.kvk_diepte, argumenten.gemeenten)
    samenvatting = schrijf(uitslag, UITVOER / str(datum))
    print(json.dumps(samenvatting, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
