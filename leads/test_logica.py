#!/usr/bin/env python3
"""Offline tests: alle logica zonder netwerk, met verzonnen voorbeeldbedrijven.

Draaien:  python3 leads/test_logica.py
"""
from __future__ import annotations

import datetime as _dt
import sys
import tempfile
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))

import bron_osm
import catalogus
import kvk as kvk_mod
import run as run_mod
import score as score_mod
import website_check

MISLUKT: list[str] = []


def bevestig(voorwaarde, omschrijving):
    if voorwaarde:
        print(f"  OK   {omschrijving}")
    else:
        print(f"  FOUT {omschrijving}")
        MISLUKT.append(omschrijving)


# --------------------------------------------------------------- rotatie
def test_rotatie():
    print("\nRotatie / territorium")
    start = _dt.date(2026, 9, 1)
    gezien = set()
    for i in range(400):
        t = catalogus.territorium_voor(start + _dt.timedelta(days=i))
        gezien.add((t.land, t.branche.sleutel, t.gemeenten))
    bevestig(len(gezien) == 400, f"400 dagen geven 400 unieke gebieden (nu {len(gezien)})")

    a = catalogus.territorium_voor(_dt.date(2026, 9, 1))
    b = catalogus.territorium_voor(_dt.date(2026, 9, 1))
    bevestig(a == b, "zelfde datum geeft altijd hetzelfde gebied (reproduceerbaar)")

    landen = {catalogus.territorium_voor(start + _dt.timedelta(days=i)).land
              for i in range(10)}
    bevestig(landen == {"NL", "BE"}, "beide markten komen aan bod")

    branches = {catalogus.territorium_voor(start + _dt.timedelta(days=i)).branche.sleutel
                for i in range(60)}
    bevestig(len(branches) >= 10,
             f"binnen 60 dagen minstens 10 branches (nu {len(branches)})")


# --------------------------------------------------------------- overpass
def test_query():
    print("\nOverpass-query")
    branche = catalogus.BRANCHE_OP_SLEUTEL["kapsalon"]
    q = bron_osm.bouw_query(["Zwolle", "Kampen"], branche)
    bevestig('area["name"="Zwolle"]' in q, "gemeente komt in de query")
    bevestig('["shop"="hairdresser"]' in q, "branchetag komt in de query")
    bevestig(q.count("nwr(area.") == 2 * len(branche.osm),
             "elke gemeente x elke tag geeft een queryregel")
    bevestig(q.strip().endswith("out center tags;"), "query vraagt tags op")


def test_element_parsing():
    print("\nParsen van OSM-elementen")
    el = {
        "type": "node", "id": 42,
        "tags": {"name": "Kapsalon Jansen", "shop": "hairdresser",
                 "addr:street": "Dorpsstraat", "addr:housenumber": "12",
                 "addr:postcode": "8011 AA", "addr:city": "Zwolle",
                 "contact:phone": "+31 38 123 4567",
                 "contact:website": "http://kapsalonjansen.nl",
                 "opening_hours": "Tu-Sa 09:00-17:00"},
    }
    b = bron_osm._element_naar_bedrijf(el, "Zwolle", "NL", "kapsalon")
    bevestig(b is not None and b.naam == "Kapsalon Jansen", "naam gelezen")
    bevestig(b.telefoon == "+31 38 123 4567", "telefoon uit contact:phone gelezen")
    bevestig(b.website == "http://kapsalonjansen.nl", "website uit contact:website gelezen")
    bevestig(b.adres == "Dorpsstraat 12, 8011 AA Zwolle", f"adres samengesteld: {b.adres}")

    zonder_naam = bron_osm._element_naar_bedrijf(
        {"type": "node", "id": 1, "tags": {"shop": "hairdresser"}}, "Zwolle", "NL", "kapsalon")
    bevestig(zonder_naam is None, "bedrijf zonder naam wordt overgeslagen")


# --------------------------------------------------------------- scoring
def _bedrijf(**kw):
    basis = dict(osm_id="node/1", naam="Testbedrijf", gemeente="Zwolle", land="NL",
                 branche="kapsalon")
    basis.update(kw)
    return bron_osm.Bedrijf(**basis)


def test_scoring():
    print("\nScoring")
    kapsalon = catalogus.BRANCHE_OP_SLEUTEL["kapsalon"]
    installatie = catalogus.BRANCHE_OP_SLEUTEL["installatie"]

    geen_site = _bedrijf(telefoon="038-1234567")
    a = score_mod.beoordeel(geen_site, None, None, kapsalon)
    bevestig(a.beste_dienst == "website", "geen website -> website is de beste dienst")
    bevestig(a.score >= 80, f"geen website scoort hoog (nu {a.score})")

    goede_site = _bedrijf(telefoon="038-1234567", website="https://goed.nl")
    rapport_goed = website_check.SiteRapport(
        url="https://goed.nl", bereikbaar=True, status=200, eindurl="https://goed.nl",
        https=True, laadtijd_ms=400, mobiel_geschikt=True, heeft_titel=True,
        heeft_meta_omschrijving=True, heeft_structuurdata=True, copyright_jaar=2026,
        online_afspraak=True)
    b = score_mod.beoordeel(goede_site, rapport_goed, None, kapsalon)
    bevestig(b.score < a.score, f"prima site scoort lager dan geen site ({b.score} < {a.score})")

    slechte_site = _bedrijf(telefoon="038-1234567", website="http://oud.nl")
    rapport_slecht = website_check.SiteRapport(
        url="http://oud.nl", bereikbaar=True, status=200, eindurl="http://oud.nl",
        https=False, laadtijd_ms=6200, mobiel_geschikt=False, heeft_titel=True,
        copyright_jaar=2014, verouderde_techniek=("Wix",))
    c = score_mod.beoordeel(slechte_site, rapport_slecht, None, kapsalon)
    bevestig(c.beste_dienst == "website", "verouderde site -> website")
    bevestig(c.score > b.score, f"verouderde site scoort hoger dan goede ({c.score} > {b.score})")
    bevestig("SSL" in c.redenen or "https" in c.redenen.lower(),
             "de reden noemt het ontbrekende slotje")

    # De kern van de verbreding: goede site, toch een lead.
    loodgieter = _bedrijf(branche="installatie", telefoon="038-9999999",
                          website="https://prima-loodgieter.nl")
    d = score_mod.beoordeel(loodgieter, rapport_goed, None, installatie)
    bevestig(d.score > 0 and d.beste_dienst != "website",
             f"bedrijf met prima site blijft lead voor een andere dienst "
             f"({d.beste_dienst}, score {d.score})")
    bevestig(d.beste_dienst == "telefonist",
             f"loodgieter met goede site -> AI-telefonist (nu {d.beste_dienst})")

    onbereikbaar = _bedrijf()
    e = score_mod.beoordeel(onbereikbaar, None, None, kapsalon)
    bevestig(e.score < a.score, "zonder telefoon en mail zakt de score")
    bevestig(e.zekerheid != "hoog", "onbereikbare lead krijgt nooit zekerheid 'hoog'")

    kvk_bv = kvk_mod.KvkResultaat(gevonden=True, kvk_nummer="12345678",
                                  rechtsvorm="Besloten Vennootschap",
                                  is_rechtspersoon=True)
    f = score_mod.beoordeel(geen_site, None, kvk_bv, kapsalon)
    bevestig(f.score > a.score, f"bekende BV scoort hoger ({f.score} > {a.score})")
    bevestig(kvk_bv.baan == "BEL", "BV mag gebeld worden")
    bevestig(kvk_mod.KvkResultaat(gevonden=True, rechtsvorm="Eenmanszaak",
                                  is_rechtspersoon=False).baan == "MAIL",
             "eenmanszaak gaat naar de mailbaan")


def test_geen_lege_dag():
    print("\nGeen lege dagen meer")
    kapsalon = catalogus.BRANCHE_OP_SLEUTEL["kapsalon"]
    rapport_perfect = website_check.SiteRapport(
        url="https://x.nl", bereikbaar=True, status=200, eindurl="https://x.nl",
        https=True, laadtijd_ms=200, mobiel_geschikt=True, heeft_titel=True,
        heeft_meta_omschrijving=True, heeft_structuurdata=True, copyright_jaar=2026,
        online_afspraak=True)
    perfect = _bedrijf(telefoon="038-1", email="info@x.nl", website="https://x.nl",
                       social="https://facebook.com/x", openingstijden="24/7")
    uitslag = score_mod.beoordeel(perfect, rapport_perfect, None, kapsalon)
    bevestig(uitslag.score >= 0, "zelfs een perfect bedrijf crasht de scoring niet")
    print(f"       (perfect bedrijf: score {uitslag.score}, "
          f"signalen: {len(uitslag.signalen)})")


# --------------------------------------------------------------- uitvoer
def test_schrijven():
    print("\nWegschrijven van de uitvoer")
    kapsalon = catalogus.BRANCHE_OP_SLEUTEL["kapsalon"]
    rijen = []
    for i in range(3):
        b = _bedrijf(osm_id=f"node/{i}", naam=f"Bedrijf {i}", telefoon="038-1234567")
        beoordeling = score_mod.beoordeel(b, None, None, kapsalon)
        rijen.append((b, None, None, beoordeling))

    uitslag = {
        "terrein": catalogus.territorium_voor(_dt.date(2026, 9, 1)),
        "rijen": rijen, "totaal_gevonden": 3, "osm_fouten": [],
        "kvk_werkt": False, "kvk_bericht": "geen sleutel", "kvk_gedaan": 0,
    }
    with tempfile.TemporaryDirectory() as tijdelijk:
        samenvatting = run_mod.schrijf(uitslag, Path(tijdelijk) / "test")
        csv_pad = Path(samenvatting["csv"])
        bevestig(csv_pad.exists(), "CSV is weggeschreven")
        inhoud = csv_pad.read_text(encoding="utf-8")
        bevestig(inhoud.startswith("score,zekerheid,beste_dienst"), "CSV heeft kopregel")
        bevestig(len(inhoud.strip().splitlines()) == 4, "CSV heeft 3 leads + kop")
        bevestig(samenvatting["leads_geleverd"] == 3, "samenvatting telt de leads")
        bevestig(samenvatting["mail_leads"] == 3,
                 "zonder KVK gaat alles naar de mailbaan (bij twijfel niet bellen)")
        bevestig("per_dienst" in samenvatting and samenvatting["per_dienst"],
                 "samenvatting splitst per dienst")


def test_normaliseren():
    print("\nURL-normalisatie")
    bevestig(website_check._normaliseer("example.nl") == "https://example.nl",
             "kaal domein krijgt https")
    bevestig(website_check._normaliseer("http://a.be") == "http://a.be",
             "http blijft http")
    bevestig(website_check._normaliseer("  ") == "", "lege invoer geeft leeg")


if __name__ == "__main__":
    test_rotatie()
    test_query()
    test_element_parsing()
    test_scoring()
    test_geen_lege_dag()
    test_schrijven()
    test_normaliseren()
    print("\n" + ("ALLE TESTS GESLAAGD" if not MISLUKT
                  else f"{len(MISLUKT)} TEST(S) MISLUKT: " + "; ".join(MISLUKT)))
    raise SystemExit(1 if MISLUKT else 0)
