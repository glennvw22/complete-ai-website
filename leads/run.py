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

import belbaar as belbaar_mod       # noqa: E402
import bron_osm                      # noqa: E402
import catalogus                     # noqa: E402
import kvk as kvk_mod                # noqa: E402
import samenstelling as samen_mod    # noqa: E402
import score as score_mod            # noqa: E402
import website_check                 # noqa: E402

UITVOER = HIER / "uitvoer"

CSV_KOLOMMEN = [
    "score", "warmte", "bedrijf", "telefoon", "plaats", "land", "branche",
    "verkoop_primair", "verkoop_secundair", "waarom_lead", "waarom_warm",
    "bellen_mag", "bellen_grond", "let_op", "rechtsvorm", "kvk_nummer",
    "website", "website_status", "email", "adres", "sbi", "zekerheid", "osm_id",
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
          kvk_budget: int, gemeenten_per_dag: int,
          land: str | None = None, branche: str | None = None,
          quota: samen_mod.Quota | None = None) -> dict:
    terrein = catalogus.territorium_voor(
        datum, gemeenten_per_dag=gemeenten_per_dag, land=land, branche_sleutel=branche
    )
    quota = quota or samen_mod.Quota()
    kvk_client = kvk_mod.KvkClient() if gebruik_kvk else kvk_mod.KvkClient(sleutel="")
    kvk_werkt, kvk_bericht = kvk_client.zelftest()

    log(f"[plan] {terrein.datum} {terrein.land} | {terrein.branche.naam} "
        f"| {', '.join(terrein.gemeenten)}")

    if terrein.land == "NL" and not kvk_werkt:
        log("[let op] KVK werkt niet; zonder rechtsvorm is geen enkele "
            "Nederlandse lead belbaar.")

    # 1. Bron. Er is een ruime overmaat nodig: in Nederland valt het grootste
    #    deel af op rechtsvorm, dus je hebt veel meer kandidaten dan leads nodig.
    bedrijven, osm_fouten = bron_osm.haal_bedrijven(
        list(terrein.gemeenten), terrein.branche, terrein.land, logger=log
    )
    nodig = aantal * 6 if terrein.land == "NL" else aantal * 2
    extra_dagen = 0
    while len(bedrijven) < nodig and extra_dagen < 40:
        extra_dagen += 2
        buur = catalogus.territorium_voor(
            datum + _dt.timedelta(days=extra_dagen),
            gemeenten_per_dag=gemeenten_per_dag,
            land=terrein.land, branche_sleutel=terrein.branche.sleutel,
        )
        log(f"[uitbreiding] {len(bedrijven)} van {nodig} kandidaten, "
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

    log(f"[bron] {len(bedrijven)} kandidaten uit OpenStreetMap")

    # 2. Zonder telefoonnummer wordt het nooit een belbare lead.
    met_nummer = [b for b in bedrijven if b.telefoon]
    log(f"[filter] {len(met_nummer)} daarvan hebben een telefoonnummer")

    # 3. Websites parallel beoordelen.
    urls = [b.website for b in met_nummer if b.website]
    log(f"[web] {len(urls)} websites controleren")
    site_rapporten = website_check.controleer_veel(urls) if urls else {}

    def site_van(bedrijf):
        if not bedrijf.website:
            return None
        return site_rapporten.get(website_check._normaliseer(bedrijf.website))

    # 4. Voorlopige score, om de KVK-bevragingen op de beste kandidaten te richten.
    voorlopig = []
    for bedrijf in met_nummer:
        site = site_van(bedrijf)
        voorlopig.append((bedrijf, site,
                          score_mod.beoordeel(bedrijf, site, None, terrein.branche)))
    voorlopig.sort(key=lambda r: -r[2].score)

    # 5. KVK: van hoog naar laag, tot er genoeg belbare leads zijn of het
    #    budget op is. Elke basisprofiel-bevraging kost geld, dus we stoppen
    #    zodra we genoeg hebben in plaats van de hele lijst af te gaan.
    kandidaten, kvk_gedaan, belbaar_gevonden = [], 0, 0
    streef = int(aantal * 1.6)
    for bedrijf, site, _ in voorlopig:
        resultaat = None
        if (kvk_werkt and belbaar_mod.kandidaat_voor_kvk(bedrijf)
                and kvk_gedaan < kvk_budget and belbaar_gevonden < streef):
            resultaat = kvk_client.zoek(bedrijf.naam, bedrijf.gemeente)
            kvk_gedaan += 1
            if kvk_gedaan % 25 == 0:
                log(f"[kvk] {kvk_gedaan} bevraagd, {belbaar_gevonden} belbaar")
        beoordeling = score_mod.beoordeel(bedrijf, site, resultaat, terrein.branche)
        belbaarheid = belbaar_mod.beoordeel_belbaarheid(bedrijf, resultaat)
        if belbaarheid.mag_bellen:
            belbaar_gevonden += 1
        kandidaten.append((bedrijf, site, resultaat, beoordeling, belbaarheid))

    log(f"[kvk] {kvk_gedaan} bevragingen, {belbaar_gevonden} belbare bedrijven "
        f"({kvk_bericht})")

    # 6. Samenstellen met quota.
    uitslag_samen = samen_mod.stel_samen(kandidaten, aantal, quota)

    return {
        "terrein": terrein,
        "rijen": uitslag_samen.gekozen,
        "samenstelling": uitslag_samen,
        "totaal_gevonden": len(bedrijven),
        "met_nummer": len(met_nummer),
        "osm_fouten": osm_fouten,
        "kvk_werkt": kvk_werkt,
        "kvk_bericht": kvk_bericht,
        "kvk_gedaan": kvk_gedaan,
        "quota": quota,
    }


def naar_rij(bedrijf, site, kvk_resultaat, beoordeling, belbaarheid) -> dict:
    website_status = "geen website bekend"
    if bedrijf.website and site is not None:
        if not site.bereikbaar:
            website_status = f"onbereikbaar ({site.fout})"
        elif site.alleen_social:
            website_status = "alleen social"
        elif site.geparkeerd:
            website_status = "geparkeerd/in aanbouw"
        else:
            kenmerken = ["https" if site.https else "GEEN https",
                         "mobiel" if site.mobiel_geschikt else "NIET mobiel"]
            if site.copyright_jaar:
                kenmerken.append(f"(c) {site.copyright_jaar}")
            kenmerken.append(f"{site.laadtijd_ms} ms")
            if site.verouderde_techniek:
                kenmerken.append("/".join(site.verouderde_techniek))
            website_status = ", ".join(kenmerken)
    elif bedrijf.website:
        website_status = "niet gecontroleerd"

    diensten = beoordeling.diensten_op_volgorde
    return {
        "score": beoordeling.score,
        "warmte": beoordeling.warmte.label,
        "bedrijf": bedrijf.naam,
        "telefoon": bedrijf.telefoon,
        "plaats": bedrijf.gemeente,
        "land": bedrijf.land,
        "branche": bedrijf.branche,
        "verkoop_primair": score_mod.dienstnaam(diensten[0]) if diensten else "",
        "verkoop_secundair": score_mod.dienstnaam(diensten[1]) if len(diensten) > 1 else "",
        "waarom_lead": beoordeling.alle_redenen,
        "waarom_warm": " ".join(f"{i}. {r}" for i, r
                                in enumerate(beoordeling.warmte.redenen, 1)),
        "bellen_mag": "JA" if belbaarheid.mag_bellen else "NEE",
        "bellen_grond": belbaarheid.reden,
        "let_op": belbaarheid.let_op,
        "rechtsvorm": kvk_resultaat.rechtsvorm if kvk_resultaat else "",
        "kvk_nummer": kvk_resultaat.kvk_nummer if kvk_resultaat else "",
        "website": bedrijf.website,
        "website_status": website_status,
        "email": bedrijf.email,
        "adres": bedrijf.adres,
        "sbi": (f"{kvk_resultaat.sbi} {kvk_resultaat.sbi_omschrijving}".strip()
                if kvk_resultaat else ""),
        "zekerheid": beoordeling.zekerheid,
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
        per_dienst[rij["verkoop_primair"]] = per_dienst.get(rij["verkoop_primair"], 0) + 1

    samen = uitslag["samenstelling"]
    terrein = uitslag["terrein"]
    samenvatting = {
        "datum": str(terrein.datum),
        "land": terrein.land,
        "branche": terrein.branche.naam,
        "gemeenten": list(terrein.gemeenten),
        "kandidaten_uit_bron": uitslag["totaal_gevonden"],
        "kandidaten_met_telefoon": uitslag["met_nummer"],
        "leads_geleverd": len(rijen),
        "alles_belbaar": all(r["bellen_mag"] == "JA" for r in rijen),
        "quota_gevraagd": uitslag["quota"].als_dict(),
        "quota_gehaald": samen.per_quotum,
        "quota_tekorten": samen.tekorten,
        "per_dienst": per_dienst,
        "warmte": {
            label: sum(1 for r in rijen if r["warmte"] == label)
            for label in ("warm", "lauw", "koud")
        },
        "afgevallen_niet_belbaar": samen.afgevallen_niet_belbaar,
        "redenen_afgevallen": samen.redenen_afgevallen,
        "kvk_werkt": uitslag["kvk_werkt"],
        "kvk_bericht": uitslag["kvk_bericht"],
        "kvk_bevragingen": uitslag["kvk_gedaan"],
        "kvk_kosten_indicatie_eur": round(uitslag["kvk_gedaan"] * 0.02, 2),
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
    ontleder.add_argument("--kvk-budget", type=int, default=400,
                          help="maximaal aantal KVK-bevragingen (ca. 2 cent per stuk)")
    ontleder.add_argument("--min-website", type=int, default=50,
                          help="minimaal aantal leads met geen/slechte website")
    ontleder.add_argument("--min-telefonist", type=int, default=15)
    ontleder.add_argument("--min-automatisering", type=int, default=15)
    ontleder.add_argument("--land", choices=["NL", "BE"], default=None,
                          help="overschrijf de rotatie; NL als je vandaag wilt bellen")
    ontleder.add_argument("--branche", default=None,
                          help="overschrijf de branche, bv. installatie of horeca")
    ontleder.add_argument("--geen-kvk", action="store_true")
    ontleder.add_argument("--diagnose", action="store_true")
    argumenten = ontleder.parse_args()

    if argumenten.diagnose:
        uitslag = diagnose(kvk_mod.KvkClient())
        print(json.dumps(uitslag, ensure_ascii=False, indent=2))
        return 0 if uitslag["osm"]["werkt"] else 1

    datum = (_dt.date.fromisoformat(argumenten.datum) if argumenten.datum
             else _dt.date.today())
    quota = samen_mod.Quota(website=argumenten.min_website,
                            telefonist=argumenten.min_telefonist,
                            automatisering=argumenten.min_automatisering)
    uitslag = draai(datum, argumenten.aantal, not argumenten.geen_kvk,
                    argumenten.kvk_budget, argumenten.gemeenten,
                    land=argumenten.land, branche=argumenten.branche, quota=quota)
    samenvatting = schrijf(uitslag, UITVOER / str(datum))
    print(json.dumps(samenvatting, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
