#!/usr/bin/env python3
"""Dagelijkse lead-run voor Complete AI.

Gebruik:
    python3 leads/run.py                      # vandaag, standaard 50 leads
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
import dashboard                     # noqa: E402
import dncm as dncm_mod              # noqa: E402
import kbo as kbo_mod                # noqa: E402
import kvk as kvk_mod                # noqa: E402
import samenstelling as samen_mod    # noqa: E402
import score as score_mod            # noqa: E402
import status as status_mod          # noqa: E402
import website_check                 # noqa: E402

UITVOER = HIER / "uitvoer"

CSV_KOLOMMEN = [
    "score", "warmte", "bedrijf", "telefoon", "plaats", "land", "branche",
    "verkoop_primair", "verkoop_secundair", "waarom_lead", "waarom_warm",
    "baan", "bellen_mag", "bellen_grond", "let_op", "rechtsvorm", "kvk_nummer",
    "website", "website_status", "email", "adres", "sbi", "vestigingen",
    "opgericht", "medewerkers", "zekerheid", "osm_id",
    "status", "notitie", "laatst_gebeld",
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
          quota: samen_mod.Quota | None = None, max_gebieden: int = 30) -> dict:
    terrein = catalogus.territorium_voor(
        datum, gemeenten_per_dag=gemeenten_per_dag, land=land, branche_sleutel=branche
    )
    quota = quota or samen_mod.Quota()
    kvk_client = kvk_mod.KvkClient() if gebruik_kvk else kvk_mod.KvkClient(sleutel="")
    kvk_werkt, kvk_bericht = kvk_client.zelftest()
    dncm_client = dncm_mod.DncmClient()
    kbo_client = kbo_mod.KboClient()

    log(f"[plan] {terrein.datum} {terrein.land} | {terrein.branche.naam} "
        f"| {', '.join(terrein.gemeenten)}")

    if terrein.land == "NL" and not kvk_werkt:
        log("[let op] KVK werkt niet; zonder rechtsvorm is geen enkele "
            "Nederlandse lead belbaar.")
    if terrein.land == "BE" and not dncm_client.beschikbaar:
        log("[let op] DNCM_API_SLEUTEL niet gezet; Belgische leads krijgen de "
            "oude waarschuwing mee en moeten in het dashboard met de hand "
            "tegen donotcallme.be afgevinkt worden.")

    # 1. Bron. Er is een ruime overmaat nodig: in Nederland valt het grootste
    #    deel af op rechtsvorm, dus je hebt veel meer kandidaten dan leads
    #    nodig. We lopen de jachtvolgorde af tot er genoeg bedrijven MET
    #    telefoonnummer zijn - zonder nummer wordt het toch nooit een bellead.
    nodig = aantal * 8 if terrein.land == "NL" else aantal * 3
    bedrijven: list = []
    osm_fouten: list[str] = []
    gezien: set = set()
    gebieden: list[str] = []

    for branche, blok in catalogus.jachtvolgorde(terrein, gemeenten_per_dag):
        met_nummer_nu = sum(1 for b in bedrijven if b.telefoon)
        if met_nummer_nu >= nodig or len(gebieden) >= max_gebieden:
            break
        gevonden, fouten = bron_osm.haal_bedrijven(
            list(blok), branche, terrein.land, logger=log
        )
        osm_fouten += fouten
        nieuw_aantal = 0
        for bedrijf in gevonden:
            sleutel = (bedrijf.naam.lower(), bedrijf.adres.lower())
            if sleutel in gezien:
                continue
            gezien.add(sleutel)
            bedrijven.append(bedrijf)
            nieuw_aantal += 1
        gebieden.append(f"{branche.sleutel}: {', '.join(blok)}")
        log(f"[bron] +{nieuw_aantal} uit {branche.sleutel} {blok[0]}... "
            f"(totaal {len(bedrijven)}, met nummer {met_nummer_nu + nieuw_aantal})")

    log(f"[bron] {len(bedrijven)} kandidaten uit OpenStreetMap")

    # KBO kan alleen op postcode afbakenen en OSM heeft die bij ongeveer de
    # helft van de bedrijven niet. Leer ze daarom uit deze partij zelf, vóór
    # de opzoekingen beginnen — zie kbo.py.
    kbo_client.leer_postcodes(bedrijven)

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

    # Staat er geen e-mailadres in OpenStreetMap, maar wel een op de eigen
    # site die we net toch al ophaalden, neem die dan over. Zonder adres valt
    # een Belgische lead af, en dat is zonde van een bedrijf dat gewoon een
    # info@ op zijn contactpagina heeft staan.
    uit_site = 0
    for bedrijf in met_nummer:
        if bedrijf.email:
            continue
        site = site_van(bedrijf)
        if site and site.emails:
            bedrijf.email = site.emails[0]
            uit_site += 1
    if uit_site:
        log(f"[web] {uit_site} e-mailadressen overgenomen van de eigen website")

    # 4. Voorlopige score, om de KVK-bevragingen op de beste kandidaten te richten.
    voorlopig = []
    for bedrijf in met_nummer:
        site = site_van(bedrijf)
        voorlopig.append((bedrijf, site,
                          score_mod.beoordeel(bedrijf, site, None, terrein.branche)))
    voorlopig.sort(key=lambda r: -r[2].score)

    # 5. KVK, in twee stappen - 18-9-2026, op uitdrukkelijk verzoek van Glenn
    #    na de Boerenbond-Roosendaal-ontdekking: we betaalden voor het
    #    basisprofiel van AL wat een telefoonnummer had, ook filialen van
    #    ketens die er toch nooit in hadden gehoord. Dat is nu andersom:
    #
    #    Fase 1 (GRATIS, Zoeken API): kvk-nummer + hoofd/nevenvestiging voor
    #    iedere kandidaat. Kost niets, dus geen budget-check nodig.
    #    Fase 2 (BETAALD, Basisprofiel): alleen voor wie fase 1 doorstaat -
    #    geen filiaal, geen kvk-nummer dat deze ronde al voorbijkwam - en
    #    alleen tot kvk_budget op is. Dat budget staat daarom nu ook veel
    #    lager (zie --kvk-budget): het hoeft alleen nog de shortlist te
    #    dekken, niet meer alles met een telefoonnummer.
    kandidaten, belbaar_gevonden = [], 0
    kvk_zoek_gedaan, kvk_basis_gedaan, afgevallen_filiaal = 0, 0, 0
    kvk_gezien_nummers: set[str] = set()
    dncm_gedaan, dncm_geblokkeerd = 0, 0
    kbo_rechtspersonen = 0
    streef = int(aantal * 1.6)
    for bedrijf, site, _ in voorlopig:
        resultaat = None
        if (kvk_werkt and belbaar_mod.kandidaat_voor_kvk(bedrijf)
                and belbaar_gevonden < streef):
            # Fase 1: gratis, dus geen budget-plafond - alleen streef, om niet
            # door te zoeken zodra we toch al genoeg hebben.
            resultaat = kvk_client.zoek(bedrijf.naam, bedrijf.gemeente,
                                        met_basisprofiel=False)
            kvk_zoek_gedaan += 1
            if resultaat.gevonden and (
                belbaar_mod.is_filiaal(resultaat)
                or resultaat.kvk_nummer in kvk_gezien_nummers
            ):
                afgevallen_filiaal += 1
                # Geen basisprofiel voor deze: resultaat blijft zonder
                # bevestigde rechtsvorm, dus beoordeel_belbaarheid() hieronder
                # zet 'm vanzelf op AF. Niet apart afhandelen hier.
            elif resultaat.gevonden and kvk_basis_gedaan < kvk_budget:
                # Fase 2: alleen nu de betaalde stap.
                kvk_client.verrijk_met_basisprofiel(resultaat)
                kvk_basis_gedaan += 1
                if resultaat.kvk_nummer:
                    kvk_gezien_nummers.add(resultaat.kvk_nummer)
                if kvk_basis_gedaan % 25 == 0:
                    log(f"[kvk] {kvk_basis_gedaan} basisprofielen bevraagd, "
                        f"{belbaar_gevonden} belbaar")
        dncm_resultaat = None
        if (bedrijf.land == "BE" and bedrijf.telefoon and dncm_client.beschikbaar
                and belbaar_gevonden < streef):
            dncm_resultaat = dncm_client.check_nummer(bedrijf.telefoon)
            dncm_gedaan += 1
            if dncm_resultaat.op_lijst:
                dncm_geblokkeerd += 1
        # KBO is gratis, dus elke Belgische kandidaat die iets te benaderen
        # heeft wordt opgezocht. Zonder rechtsvorm is er geen grond om te
        # bellen én geen grond om te mailen, dus dit bepaalt of de lead
        # bestaat.
        # Géén plafond op het aantal KBO-opzoekingen. Dat stond er eerst wel,
        # gekoppeld aan het belquotum (streef * 2) — maar dat quotum gaat over
        # de BEL-baan en KBO vult juist de MAIL-baan. Gemeten 13-9-2026: 60
        # gebieden gaven 597 kandidaten met nummer maar bleven op 77 leads
        # steken doordat dit plafond de opzoekingen afkapte. De echte rem zit
        # al eerder: alleen bedrijven met een onpersoonlijk e-mailadres worden
        # opgezocht, en KBO kost niets.
        kbo_resultaat = None
        if belbaar_mod.kandidaat_voor_kbo(bedrijf, dncm_client.beschikbaar):
            kbo_resultaat = kbo_client.zoek_bedrijf(bedrijf)
            if kbo_resultaat.gevonden and kbo_resultaat.is_rechtspersoon:
                kbo_rechtspersonen += 1
        beoordeling = score_mod.beoordeel(bedrijf, site, resultaat, terrein.branche)
        belbaarheid = belbaar_mod.beoordeel_belbaarheid(
            bedrijf, resultaat, dncm_resultaat, kbo_resultaat)
        if belbaarheid.mag_bellen:
            belbaar_gevonden += 1
        kandidaten.append((bedrijf, site, resultaat, beoordeling, belbaarheid))

    log(f"[kvk] {kvk_zoek_gedaan} gratis zoekopdrachten, {kvk_basis_gedaan} betaalde "
        f"basisprofielen, {afgevallen_filiaal} filialen/dubbele kvk-nummers gratis "
        f"afgevangen, {belbaar_gevonden} belbare bedrijven ({kvk_bericht})")
    if dncm_gedaan:
        log(f"[dncm] {dncm_gedaan} nummers automatisch tegen de DNCM-lijst "
            f"gecontroleerd, {dncm_geblokkeerd} stonden erop en zijn geblokkeerd")
    if kbo_client.bevragingen:
        log(f"[kbo] {kbo_client.bevragingen} gratis opzoekingen, "
            f"{kbo_rechtspersonen} rechtspersonen gevonden")

    # 6. Samenstellen met quota.
    uitslag_samen = samen_mod.stel_samen(kandidaten, aantal, quota)

    return {
        "terrein": terrein,
        "rijen": uitslag_samen.gekozen,
        "samenstelling": uitslag_samen,
        "totaal_gevonden": len(bedrijven),
        "met_nummer": len(met_nummer),
        "gebieden": gebieden,
        "osm_fouten": osm_fouten,
        "kvk_werkt": kvk_werkt,
        "kvk_bericht": kvk_bericht,
        "kvk_zoek_gedaan": kvk_zoek_gedaan,
        "kvk_basis_gedaan": kvk_basis_gedaan,
        "afgevallen_filiaal": afgevallen_filiaal,
        "quota": quota,
    }


def naar_rij(bedrijf, site, kvk_resultaat, beoordeling, belbaarheid) -> dict:
    # LET OP bij het wijzigen van deze exacte tekst: het belscherm in het
    # dashboard (jarvis-dashboard, components/bellen/Gespreksadvies.tsx,
    # constante WEBSITE_ONBEVESTIGD) matcht hier letterlijk op om een
    # veiligheidswaarschuwing te tonen ("dit is een aanname, geen meting -
    # vraag het na"). Verander je deze string, verander hem dan ook daar,
    # anders verdwijnt die waarschuwing stilletjes zonder dat iemand het merkt.
    website_status = "geen website bekend"
    if bedrijf.website and site is not None:
        if site.geblokkeerd:
            website_status = f"niet te controleren: {site.fout}"
        elif not site.bereikbaar:
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
        "baan": getattr(belbaarheid, "baan", ""),
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
        "vestigingen": kvk_resultaat.vestigingen if kvk_resultaat else None,
        "opgericht": kvk_resultaat.oprichtingsdatum if kvk_resultaat else "",
        "medewerkers": kvk_resultaat.medewerkers if kvk_resultaat else None,
        "zekerheid": beoordeling.zekerheid,
        "osm_id": bedrijf.osm_id,
        # Kolommen om in te vullen tijdens het bellen. Ze staan al in de CSV
        # zodat de bellijst en het dashboard dezelfde vorm inlezen.
        "status": status_mod.BEGINSTATUS,
        "notitie": "",
        "laatst_gebeld": "",
    }


def schrijf(uitslag: dict, map_pad: Path) -> dict:
    map_pad.mkdir(parents=True, exist_ok=True)
    rijen = [naar_rij(*r) for r in uitslag["rijen"]]

    csv_pad = map_pad / "leads.csv"
    with csv_pad.open("w", newline="", encoding="utf-8") as bestand:
        schrijver = csv.DictWriter(bestand, fieldnames=CSV_KOLOMMEN)
        schrijver.writeheader()
        schrijver.writerows(rijen)

    # De MAIL-baan in een eigen bestand: dit zijn geen belleads en ze horen
    # dus niet in de bellijst, maar weggooien is precies wat de Belgische
    # stroom kostte. Zie belbaar.py voor wie hier terechtkomt.
    mail_rijen = [naar_rij(*r) for r in uitslag["samenstelling"].mailbaan]
    mail_pad = map_pad / "mailbaan.csv"
    with mail_pad.open("w", newline="", encoding="utf-8") as bestand:
        schrijver = csv.DictWriter(bestand, fieldnames=CSV_KOLOMMEN)
        schrijver.writeheader()
        schrijver.writerows(mail_rijen)

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
        "gebieden_afgezocht": uitslag.get("gebieden", []),
        "kandidaten_uit_bron": uitslag["totaal_gevonden"],
        "kandidaten_met_telefoon": uitslag["met_nummer"],
        "leads_geleverd": len(rijen),
        "mailbaan_geleverd": len(mail_rijen),
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
        "afgevallen_zonder_koopsignaal": samen.afgevallen_zonder_reden,
        "afgevallen_filiaal_of_dubbel_kvk": uitslag["afgevallen_filiaal"],
        "redenen_afgevallen": samen.redenen_afgevallen,
        "kvk_werkt": uitslag["kvk_werkt"],
        "kvk_bericht": uitslag["kvk_bericht"],
        # Gratis (Zoeken) en betaald (Basisprofiel) bewust apart: alleen de
        # tweede kost geld. Vóór 18-9-2026 stond hier één geteld aantal dat in
        # werkelijkheid alleen de (toen nog altijd-betaalde) stap was.
        "kvk_zoekopdrachten_gratis": uitslag["kvk_zoek_gedaan"],
        "kvk_basisprofielen_betaald": uitslag["kvk_basis_gedaan"],
        "kvk_kosten_indicatie_eur": round(uitslag["kvk_basis_gedaan"] * 0.02, 2),
        "osm_fouten": uitslag["osm_fouten"][:5],
        "csv": str(csv_pad),
        "mailbaan_csv": str(mail_pad) if mail_rijen else "",
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
    # 50, niet 150 - vaste afspraak sinds 18-9-2026: kwaliteit boven volume,
    # zie leads/samenstelling.py Quota voor de bijbehorende verdeling.
    ontleder.add_argument("--aantal", type=int, default=50)
    ontleder.add_argument("--gemeenten", type=int, default=4)
    ontleder.add_argument("--max-gebieden", type=int, default=30,
                          help="hoeveel branche x gemeenteblok-combinaties maximaal")
    # Was 900. Dat dekte vroeger IEDERE kandidaat met een telefoonnummer, want
    # de betaalde basisprofiel-stap gebeurde toen voor alles. Sinds de
    # tweefasenstructuur hierboven (gratis zoeken -> filiaal/dubbel-kvk eruit
    # -> pas dan betaald basisprofiel) hoeft dit budget alleen nog de
    # shortlist te dekken: ruwweg aantal * 1.6 aan kandidaten die de gratis
    # filters doorstaan. 150 is een eerste inschatting bij aantal=50, geen
    # gemeten getal - bijstellen na de eerste --geen-post testrun.
    ontleder.add_argument("--kvk-budget", type=int, default=150,
                          help="maximaal aantal BETAALDE KVK-basisprofielen "
                               "(ca. 2 cent per stuk; de gratis zoekstap telt hier niet in mee)")
    ontleder.add_argument("--min-website", type=int, default=30,
                          help="minimaal aantal leads met geen/slechte website")
    ontleder.add_argument("--min-telefonist", type=int, default=10)
    ontleder.add_argument("--min-automatisering", type=int, default=10)
    ontleder.add_argument("--land", choices=["NL", "BE"], default=None,
                          help="overschrijf de rotatie; NL als je vandaag wilt bellen")
    ontleder.add_argument("--branche", default=None,
                          help="overschrijf de branche, bv. installatie of horeca")
    ontleder.add_argument("--geen-kvk", action="store_true")
    ontleder.add_argument("--diagnose", action="store_true")
    ontleder.add_argument("--geen-post", action="store_true",
                          help="schrijf de CSV maar verstuur nog niet naar het dashboard — "
                               "gebruikt door de dagelijkse routine, die tussen het schrijven "
                               "en het versturen eerst controleert of 'geen website bekend' "
                               "(een aanname bij ontbrekende data, geen meting) ook echt klopt. "
                               "Versturen daarna met: python3 -c \"import sys; "
                               "sys.path.insert(0,'leads'); import dashboard; "
                               "dashboard.stuur_naar_dashboard('<pad-naar-leads.csv>')\"")
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
                    land=argumenten.land, branche=argumenten.branche, quota=quota,
                    max_gebieden=argumenten.max_gebieden)
    samenvatting = schrijf(uitslag, UITVOER / str(datum))
    if argumenten.geen_post:
        log(f"[post] overgeslagen (--geen-post) — CSV staat klaar op {samenvatting['csv']}, "
            "nog niet verstuurd naar het dashboard")
    else:
        dashboard.stuur_naar_dashboard(samenvatting["csv"])
        # De mailbaan gaat mee dezelfde route in: het zijn gewone leads, alleen
        # met baan=MAIL, en het dashboard weet daardoor dat ze benaderd mogen
        # worden per e-mail maar (nog) niet gebeld. Zonder deze regel blijven
        # ze op de schijf staan en is de Belgische stroom alsnog onzichtbaar.
        if samenvatting.get("mailbaan_csv"):
            dashboard.stuur_naar_dashboard(samenvatting["mailbaan_csv"])
    print(json.dumps(samenvatting, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
