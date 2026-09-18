#!/usr/bin/env python3
"""Offline tests: alle logica zonder netwerk, met verzonnen voorbeeldbedrijven.

Draaien:  python3 leads/test_logica.py
"""
from __future__ import annotations

import datetime as _dt
import json
import sys
import tempfile
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))

import belbaar as belbaar_mod
import bron_osm
import catalogus
import dncm as dncm_mod
import kbo as kbo_mod
import ketens as ketens_mod
import kvk as kvk_mod
import run as run_mod
import samenstelling as samen_mod
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
def test_overschrijven():
    print("\nLand en branche overschrijven")
    d = _dt.date(2026, 9, 3)
    vanzelf = catalogus.territorium_voor(d)
    geforceerd = catalogus.territorium_voor(d, land="NL")
    bevestig(geforceerd.land == "NL", "land NL forceren werkt")
    bevestig(vanzelf.branche == geforceerd.branche,
             "de branche verandert niet als je alleen het land forceert")
    bevestig(all(g in catalogus.GEMEENTEN_NL for g in geforceerd.gemeenten),
             "geforceerd NL levert alleen Nederlandse gemeenten")

    met_branche = catalogus.territorium_voor(d, land="NL", branche_sleutel="horeca")
    bevestig(met_branche.branche.sleutel == "horeca", "branche forceren werkt")

    try:
        catalogus.territorium_voor(d, branche_sleutel="bestaat-niet")
        bevestig(False, "onbekende branche geeft een duidelijke fout")
    except ValueError as fout:
        bevestig("onbekende branche" in str(fout),
                 "onbekende branche geeft een duidelijke fout")

    zelfde = catalogus.territorium_voor(d, land="BE")
    bevestig(all(g in catalogus.GEMEENTEN_BE for g in zelfde.gemeenten),
             "geforceerd BE levert alleen Vlaamse gemeenten")


def test_query():
    print("\nOverpass-query")
    branche = catalogus.BRANCHE_OP_SLEUTEL["kapsalon"]
    q = bron_osm.bouw_query(["Zwolle", "Kampen"], branche)
    bevestig('area["name"="Zwolle"]' in q, "gemeente komt in de query")
    bevestig("hairdresser" in q, "branchetag komt in de query")
    # Tags met dezelfde sleutel horen samengevoegd tot een regex: een aparte
    # regel per tag is een aparte gebiedsdoorloop, en vier gemeenten maal vijf
    # tags maakte de query zo zwaar dat Overpass hem afkapte met een 504.
    sleutels = {tag for tag, _ in branche.osm}
    bevestig(q.count("nwr(area.") == 2 * len(sleutels),
             "elke gemeente x elke tagsleutel geeft een queryregel")
    bevestig(q.count("nwr(area.") < 2 * len(branche.osm),
             "dat zijn er minder dan een regel per losse tag")
    for _, waarde in branche.osm:
        bevestig(waarde in q, f"waarde {waarde} zit in de samengevoegde regex")
    bevestig(q.strip().endswith("out center tags;"), "query vraagt tags op")


def test_dode_spiegel():
    print("\nGeblokkeerde spiegel overslaan")
    bevestig(bron_osm._onbereikbaar(OSError("[Errno 104] Connection reset by peer")),
             "een reset betekent: onbereikbaar, niet nog eens proberen")
    bevestig(bron_osm._onbereikbaar(OSError("Connection refused")),
             "een geweigerde verbinding ook")
    bevestig(not bron_osm._onbereikbaar(TimeoutError("The read operation timed out")),
             "een trage spiegel is NIET onbereikbaar en verdient een nieuwe poging")
    bevestig(not bron_osm._onbereikbaar(OSError("HTTP Error 504: Gateway Timeout")),
             "een overbelaste spiegel evenmin")


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


def test_kvk_antwoord_lezen():
    """Regressietest op het echte antwoordformaat van de KVK.

    Hier ging het een keer helemaal mis: de rechtsvorm werd in
    _embedded.hoofdvestiging gezocht terwijl de KVK hem bij de EIGENAAR van de
    inschrijving zet. Dat gaf geen foutmelding maar een lege rechtsvorm, en dus
    een hele dag leads die allemaal afvielen op "bij twijfel niet bellen".
    """
    print("\nKVK-antwoord lezen")
    basisprofiel = {
        "kvkNummer": "34367595",
        "naam": "WMR Loodgieters B.V.",
        "sbiActiviteiten": [{"sbiCode": "43221", "sbiOmschrijving": "Loodgieterswerk",
                             "indHoofdactiviteit": "Ja"}],
        "_embedded": {
            "eigenaar": {"rsin": "1", "rechtsvorm": "Besloten Vennootschap",
                         "uitgebreideRechtsvorm": "Besloten Vennootschap"},
            "hoofdvestiging": {"vestigingsnummer": "1", "eersteHandelsnaam": "WMR"},
        },
    }
    bevestig(kvk_mod._pak_rechtsvorm(basisprofiel) == "Besloten Vennootschap",
             "rechtsvorm wordt bij de eigenaar gevonden, niet bij de vestiging")
    bevestig(kvk_mod.classificeer_rechtsvorm(
        kvk_mod._pak_rechtsvorm(basisprofiel)) is True,
        "en die telt als rechtspersoon, dus belbaar")

    eenmanszaak = {"_embedded": {"eigenaar": {"rechtsvorm": "Eenmanszaak"}}}
    bevestig(kvk_mod.classificeer_rechtsvorm(
        kvk_mod._pak_rechtsvorm(eenmanszaak)) is False,
        "een eenmanszaak blijft een natuurlijk persoon")

    bevestig(kvk_mod._pak_rechtsvorm({"_embedded": {"eigenaar": {}}}) == "",
             "ontbrekende rechtsvorm geeft leeg en niet een gok")

    # De plaats van een zoektreffer zit genest onder adres.binnenlandsAdres.
    treffer = {"kvkNummer": "1", "naam": "Kapsalon Jansen", "type": "hoofdvestiging",
               "adres": {"binnenlandsAdres": {"type": "bezoekadres",
                                              "straatnaam": "Dorpsstraat",
                                              "plaats": "Zwolle"}}}
    bevestig(kvk_mod._plaats_van_treffer(treffer) == "Zwolle",
             "plaats uit genest adres gelezen")
    elders = dict(treffer, adres={"binnenlandsAdres": {"plaats": "Kampen"}})
    bevestig(kvk_mod._rang(treffer, "Kapsalon Jansen", "Zwolle")
             < kvk_mod._rang(elders, "Kapsalon Jansen", "Zwolle"),
             "de vestiging in de gezochte plaats gaat voor")


def test_kvk_dedupe_op_naam():
    """Regressietest voor de matching-bug van 17/18-9-2026: Boerenbond (ID
    508) en Pets Place (ID 1303) in de dashboard-database bleken hetzelfde
    KVK-nummer (09165890) te hebben onder twee verschillende bedrijfsnamen.
    Oorzaak: _rang() sorteerde treffers alleen op vestigingsadres/-type, nooit
    op de naam van de treffer zelf - dus won een compleet ander bedrijf op
    hetzelfde (voormalige) adres de rangschikking. Nu moet elke koppeling een
    harde naam-match hebben."""
    print("\nKVK: geen dedupe-koppeling zonder harde naam-match")

    bevestig(kvk_mod._naam_matcht("Pets Place", "Pets Place Nederland B.V."),
             "naam plus rechtsvormstaart telt als match")
    bevestig(kvk_mod._naam_matcht("Pets Place", "PETS PLACE"),
             "hoofdletters maken niets uit")
    bevestig(not kvk_mod._naam_matcht("Boerenbond", "Pets Place"),
             "twee losse bedrijfsnamen zijn geen match")
    bevestig(not kvk_mod._naam_matcht("", "Pets Place"), "lege gezochte naam is geen match")
    bevestig(not kvk_mod._naam_matcht("Pets Place", ""), "lege treffernaam is geen match")

    # _rang: een treffer met de juiste naam moet winnen van een treffer met
    # een andere naam op hetzelfde adres.
    juiste_naam = {"naam": "Pets Place", "type": "hoofdvestiging",
                    "adres": {"binnenlandsAdres": {"plaats": "Roosendaal"}}}
    andere_naam_zelfde_adres = {"naam": "Vorige Huurder B.V.", "type": "hoofdvestiging",
                                 "adres": {"binnenlandsAdres": {"plaats": "Roosendaal"}}}
    bevestig(kvk_mod._rang(juiste_naam, "Pets Place", "Roosendaal")
             < kvk_mod._rang(andere_naam_zelfde_adres, "Pets Place", "Roosendaal"),
             "de treffer met de juiste naam wint, ook al staat de ander op hetzelfde adres")

    # End-to-end via zoek(): de KVK Zoeken API geeft voor twee verschillende
    # bedrijfsnamen op hetzelfde (voormalige) adres allebei alleen het
    # bedrijf terug dat er ooit zat - precies de Boerenbond/Pets Place-bug.
    def antwoord_alleen_vorige_huurder(url, params):
        if url != kvk_mod.ZOEKEN:
            return None, "onverwacht endpoint in test"
        return {"totaal": 1, "resultaten": [
            {"kvkNummer": "09165890", "naam": "Vorige Huurder B.V.",
             "type": "hoofdvestiging",
             "adres": {"binnenlandsAdres": {"plaats": "Roosendaal"}}},
        ]}, ""

    client = kvk_mod.KvkClient(sleutel="test-sleutel")
    client._get = antwoord_alleen_vorige_huurder

    boerenbond = client.zoek("Boerenbond", "Roosendaal", met_basisprofiel=False)
    pets_place = client.zoek("Pets Place", "Roosendaal", met_basisprofiel=False)
    bevestig(not boerenbond.gevonden,
             "Boerenbond krijgt GEEN KVK-nummer toegewezen zonder naam-match")
    bevestig(not pets_place.gevonden,
             "Pets Place krijgt GEEN KVK-nummer toegewezen zonder naam-match")
    bevestig(boerenbond.kvk_nummer == "" and pets_place.kvk_nummer == "",
             "geen van beide krijgt het KVK-nummer van de vorige huurder (09165890)")
    bevestig(boerenbond.fout and pets_place.fout,
             "een geweigerde koppeling meldt een reden in plaats van stil te falen")

    # Zet meerdere treffers neer, waarvan er één wél de juiste naam heeft maar
    # NIET het beste adres/vestigingstype - die moet nu toch winnen.
    def antwoord_meerdere_treffers(url, params):
        if url != kvk_mod.ZOEKEN:
            return None, "onverwacht endpoint in test"
        return {"totaal": 2, "resultaten": [
            {"kvkNummer": "11111111", "naam": "Ander Bedrijf B.V.",
             "type": "hoofdvestiging",
             "adres": {"binnenlandsAdres": {"plaats": "Roosendaal"}}},
            {"kvkNummer": "22222222", "naam": "Pets Place Nederland B.V.",
             "type": "nevenvestiging",
             "adres": {"binnenlandsAdres": {"plaats": "Amsterdam"}}},
        ]}, ""

    client2 = kvk_mod.KvkClient(sleutel="test-sleutel")
    client2._get = antwoord_meerdere_treffers
    juist = client2.zoek("Pets Place", "Roosendaal", met_basisprofiel=False)
    bevestig(juist.gevonden and juist.kvk_nummer == "22222222",
             "bij meerdere treffers wint de juiste naam, ook al klopt het adres niet")


def test_filiaal_en_leeftijd():
    """Regressietest voor de wijziging van 18-9-2026 (aanleiding: Boerenbond
    Roosendaal kreeg score 100 terwijl het een filiaal van een keten met 70+
    winkels is): filialen mogen geen betaald basisprofiel meer kosten, en
    bedrijfsleeftijd geeft nu een warmtebonus terwijl 'meerdere vestigingen'
    er geen meer geeft."""
    print("\nFiliaalfilter en bedrijfsleeftijd")

    nevenvestiging = kvk_mod.KvkResultaat(gevonden=True, kvk_nummer="1",
                                           zoek_type="nevenvestiging")
    hoofdvestiging = kvk_mod.KvkResultaat(gevonden=True, kvk_nummer="2",
                                           zoek_type="hoofdvestiging")
    niet_gevonden = kvk_mod.KvkResultaat(gevonden=False)

    bevestig(belbaar_mod.is_filiaal(nevenvestiging) is True,
             "nevenvestiging wordt herkend als filiaal")
    bevestig(belbaar_mod.is_filiaal(hoofdvestiging) is False,
             "hoofdvestiging is geen filiaal")
    bevestig(belbaar_mod.is_filiaal(niet_gevonden) is False,
             "niet gevonden is geen filiaal (er is gewoon niets bekend)")
    bevestig(belbaar_mod.is_filiaal(None) is False,
             "geen kvk-resultaat is geen filiaal")

    # Basisprofiel-antwoordformaat - het exacte veldpad is (nog) niet met een
    # echte aanroep bevestigd, zie de docstrings in kvk.py. Deze test dekt het
    # pad dat de KVK-ontwikkelaarsdocumentatie noemt.
    profiel = {
        "materieleRegistratie": {"datumAanvang": "20200315"},
        "totaalWerkzamePersonen": 3,
    }
    bevestig(kvk_mod._pak_oprichtingsdatum(profiel) == "20200315",
             "oprichtingsdatum uit materieleRegistratie.datumAanvang gelezen")
    bevestig(kvk_mod._pak_medewerkers(profiel) == 3,
             "medewerkers uit totaalWerkzamePersonen gelezen")
    bevestig(kvk_mod._pak_oprichtingsdatum({}) == "",
             "ontbrekende oprichtingsdatum geeft leeg, geen gok")
    bevestig(kvk_mod._pak_medewerkers({}) is None,
             "ontbrekend medewerkersaantal geeft None, geen verzonnen 0")

    kapsalon = catalogus.BRANCHE_OP_SLEUTEL["kapsalon"]
    bedrijf = _bedrijf(telefoon="038-1234567")
    dit_jaar = _dt.date.today().year

    kvk_jong = kvk_mod.KvkResultaat(gevonden=True, is_rechtspersoon=True,
                                     oprichtingsdatum=f"{dit_jaar - 3}0101")
    beoordeling_jong = score_mod.beoordeel(bedrijf, None, kvk_jong, kapsalon)
    bevestig(any("relatief jong" in r for r in beoordeling_jong.warmte.redenen),
             "3 jaar oud bedrijf krijgt de jong-bedrijf warmtebonus")

    kvk_oud = kvk_mod.KvkResultaat(gevonden=True, is_rechtspersoon=True,
                                    oprichtingsdatum=f"{dit_jaar - 25}0101")
    beoordeling_oud = score_mod.beoordeel(bedrijf, None, kvk_oud, kapsalon)
    bevestig(not any("relatief jong" in r for r in beoordeling_oud.warmte.redenen),
             "25 jaar oud bedrijf krijgt geen jong-bedrijf bonus")

    # De oude bug: >1 vestiging gaf altijd +20 warmtepunten ("groeiend bedrijf
    # met budget"). Nu mag dat veld geen enkel verschil meer maken - filialen
    # worden al eerder (is_filiaal, kostenfilter) uitgesloten.
    kvk_veel_vestigingen = kvk_mod.KvkResultaat(gevonden=True, is_rechtspersoon=True,
                                                 vestigingen=70)
    beoordeling_veel = score_mod.beoordeel(bedrijf, None, kvk_veel_vestigingen, kapsalon)
    bevestig(not any("vestiging" in r for r in beoordeling_veel.warmte.redenen),
             "aantal vestigingen geeft geen warmtepunten meer (was de Boerenbond-bug)")


def test_ketens():
    """Regressietest voor de vondst van 17/18-9-2026: 13 leads in de
    dashboard-database bleken overduidelijk filialen van landelijke ketens
    (Boerenbond, C&A, Kwik-Fit x3, Van Mossel x2, Tesla, Basic-Fit, Pets
    Place, SnowWorld Amsterdam, Lucardi x2), maar GEEN daarvan stond
    geregistreerd als KVK-nevenvestiging - belbaar.is_filiaal() mist dit
    type dus volledig. ketens.py vult dat gat met naamherkenning."""
    print("\nKetens-uitsluiting op naam")

    # De drie schrijfwijzen van Kwik-Fit die in de praktijk zijn aangetroffen.
    bevestig(ketens_mod.is_landelijke_keten("Kwik-Fit Almere"), "Kwik-Fit met streepje")
    bevestig(ketens_mod.is_landelijke_keten("Kwik Fit Almere"), "Kwik Fit met spatie")
    bevestig(ketens_mod.is_landelijke_keten("KwikFit Almere"), "KwikFit aaneengeschreven")

    # De overige 8 uit de 13 gevonden leads (Kwik-Fit hierboven al gedekt).
    for naam in ("Boerenbond Roosendaal", "C&A Utrecht", "Van Mossel Peugeot",
                 "Tesla Amsterdam", "Basic-Fit Zwolle", "Pets Place",
                 "SnowWorld Amsterdam", "Lucardi Juweliers"):
        bevestig(ketens_mod.is_landelijke_keten(naam), f"{naam} wordt herkend als keten")

    # Een paar andere landelijke ketens die er zelf bij zijn gezet.
    for naam in ("Hunkemöller Rotterdam", "Zeeman", "Action Nieuwerkerk",
                 "Bruna Boekhandel", "Etos Drogist", "Kruidvat"):
        bevestig(ketens_mod.is_landelijke_keten(naam), f"{naam} wordt herkend als keten")

    # Geen enkele lokale zelfstandige mag hierdoor ten onrechte wegvallen -
    # vooral belangrijk rond de korte/ambigue namen (C&A, Action).
    for naam in ("Kapsalon Jansen", "Loodgietersbedrijf De Vries",
                 "Capsalon Anna", "Actionfoto Zwolle", "Willy's Autobanden"):
        bevestig(not ketens_mod.is_landelijke_keten(naam),
                 f"{naam} is GEEN keten en mag niet worden uitgesloten")

    bevestig(not ketens_mod.is_landelijke_keten(""), "lege naam is geen keten")
    bevestig(not ketens_mod.is_landelijke_keten(None), "None als naam crasht niet")

    # Dezelfde soort uitkomst als is_filiaal(): geen betaalde KVK-bevraging,
    # en de lead valt af (AF), niet naar de mailbaan.
    oordeel = belbaar_mod.keten_beoordeling()
    bevestig(oordeel.baan == belbaar_mod.AF, "een herkende keten komt op AF, niet MAIL")
    bevestig(not oordeel.mag_bellen, "een herkende keten mag niet gebeld worden")


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
def test_belbaarheid():
    print("\nBelbaarheid (regelgeving)")
    bv = kvk_mod.KvkResultaat(gevonden=True, rechtsvorm="Besloten Vennootschap",
                              is_rechtspersoon=True)
    ez = kvk_mod.KvkResultaat(gevonden=True, rechtsvorm="Eenmanszaak",
                              is_rechtspersoon=False)
    onbekend = kvk_mod.KvkResultaat(gevonden=True, zoek_type="rechtspersoon")

    bevestig(belbaar_mod.beoordeel_belbaarheid(_bedrijf(telefoon="038-1"), bv).mag_bellen,
             "NL rechtspersoon met nummer mag gebeld worden")
    bevestig(not belbaar_mod.beoordeel_belbaarheid(_bedrijf(telefoon="038-1"), ez).mag_bellen,
             "NL eenmanszaak mag NIET gebeld worden")
    bevestig(not belbaar_mod.beoordeel_belbaarheid(_bedrijf(telefoon="038-1"), onbekend).mag_bellen,
             "NL met onbekende rechtsvorm valt af, ook bij een aanwijzing")
    bevestig(not belbaar_mod.beoordeel_belbaarheid(_bedrijf(telefoon="038-1"), None).mag_bellen,
             "NL zonder KVK-treffer valt af")
    bevestig(not belbaar_mod.beoordeel_belbaarheid(_bedrijf(), bv).mag_bellen,
             "zonder telefoonnummer geen bellead")

    bevestig(belbaar_mod.beoordeel_belbaarheid(_bedrijf(telefoon="038-1"), bv).baan == belbaar_mod.BEL,
             "NL rechtspersoon komt op de BEL-baan")
    bevestig(belbaar_mod.beoordeel_belbaarheid(_bedrijf(telefoon="038-1"), ez).baan == belbaar_mod.AF,
             "NL eenmanszaak valt af, ook voor mail (openstaande vraag in de kluis)")


def test_belbaarheid_belgie():
    print("\nBelbaarheid België (DNCM, KBO, opt-in)")
    rp = kbo_mod.KboResultaat(gevonden=True, is_rechtspersoon=True,
                              rechtsvorm="Besloten Vennootschap")
    np_ = kbo_mod.KboResultaat(gevonden=True, is_rechtspersoon=False)
    kbo_onbekend = kbo_mod.KboResultaat(gevonden=False, fout="niet teruggevonden")

    def be(**kw):
        velden = dict(land="BE", telefoon="09-1")
        velden.update(kw)
        return _bedrijf(**velden)

    # Zonder enige verrijking: niets is vastgesteld, dus niets mag.
    kaal = belbaar_mod.beoordeel_belbaarheid(be(), None)
    bevestig(kaal.baan == belbaar_mod.AF,
             "BE zonder KBO en zonder opt-in valt af — geen grond om te bellen of te mailen")

    # Rechtspersoon + onpersoonlijk adres = mailbaar, nog niet belbaar.
    mailbaar = belbaar_mod.beoordeel_belbaarheid(
        be(email="info@zaak.be"), None, kbo_resultaat=rp)
    bevestig(mailbaar.baan == belbaar_mod.MAIL, "BE rechtspersoon met info@ komt op de MAIL-baan")
    bevestig(not mailbaar.mag_bellen, "een MAIL-lead mag niet gebeld worden")
    bevestig(mailbaar.mag_mailen, "een MAIL-lead mag wel gemaild worden")

    # Persoonlijk adres mag niet ongevraagd gemaild worden.
    persoonlijk = belbaar_mod.beoordeel_belbaarheid(
        be(email="jan.peeters@zaak.be"), None, kbo_resultaat=rp)
    bevestig(persoonlijk.baan == belbaar_mod.AF,
             "BE rechtspersoon met persoonlijk adres valt af — geen grond voor ongevraagde mail")

    # Natuurlijk persoon: noch bellen noch mailen.
    natuurlijk = belbaar_mod.beoordeel_belbaarheid(
        be(email="info@zaak.be"), None, kbo_resultaat=np_)
    bevestig(natuurlijk.baan == belbaar_mod.AF, "BE natuurlijk persoon valt af")

    onbekend_kbo = belbaar_mod.beoordeel_belbaarheid(
        be(email="info@zaak.be"), None, kbo_resultaat=kbo_onbekend)
    bevestig(onbekend_kbo.baan == belbaar_mod.AF, "BE zonder KBO-treffer valt af")

    # Een geldige, gedateerde opt-in gaat vóór de DNCM-lijst.
    vandaag = _dt.date.today()
    met_optin = belbaar_mod.beoordeel_belbaarheid(
        be(email="info@zaak.be"), None, kbo_resultaat=rp,
        opt_in_datum=vandaag - _dt.timedelta(days=3))
    bevestig(met_optin.baan == belbaar_mod.BEL and met_optin.mag_bellen,
             "BE met verse opt-in mag gebeld worden, zonder de lijst te kopen")

    verlopen = belbaar_mod.beoordeel_belbaarheid(
        be(email="info@zaak.be"), None, kbo_resultaat=rp,
        opt_in_datum=vandaag - _dt.timedelta(days=belbaar_mod.OPT_IN_GELDIG_DAGEN + 1))
    bevestig(verlopen.baan == belbaar_mod.MAIL,
             "een verlopen opt-in zakt terug naar de MAIL-baan, niet naar BEL")

    # Met een werkende (betaalde) DNCM-koppeling beslist de lijst zelf.
    niet_op_lijst = dncm_mod.DncmResultaat(gevonden=True, op_lijst=False)
    op_lijst = dncm_mod.DncmResultaat(gevonden=True, op_lijst=True)
    bevestig(belbaar_mod.beoordeel_belbaarheid(be(), None, niet_op_lijst).mag_bellen,
             "BE niet op de DNCM-lijst mag gebeld worden")
    bevestig(not belbaar_mod.beoordeel_belbaarheid(be(), None, op_lijst).mag_bellen,
             "BE op de DNCM-lijst mag NIET gebeld worden")

    # De adrescheck zelf.
    bevestig(belbaar_mod.onpersoonlijk_adres("info@zaak.be"), "info@ is onpersoonlijk")
    bevestig(belbaar_mod.onpersoonlijk_adres("contact-be@zaak.be"), "contact-be@ is onpersoonlijk")
    bevestig(not belbaar_mod.onpersoonlijk_adres("jan@zaak.be"), "jan@ is persoonlijk")
    bevestig(not belbaar_mod.onpersoonlijk_adres(""), "leeg adres is niet mailbaar")


def test_samenstelling():
    print("\nSamenstelling met quota")
    kapsalon = catalogus.BRANCHE_OP_SLEUTEL["kapsalon"]
    bv = kvk_mod.KvkResultaat(gevonden=True, rechtsvorm="Besloten Vennootschap",
                              is_rechtspersoon=True)
    ez = kvk_mod.KvkResultaat(gevonden=True, rechtsvorm="Eenmanszaak",
                              is_rechtspersoon=False)

    kandidaten = []
    for i in range(30):
        b = _bedrijf(osm_id=f"ok{i}", naam=f"OK{i}", telefoon="038-1")
        kandidaten.append((b, None, bv, score_mod.beoordeel(b, None, bv, kapsalon),
                           belbaar_mod.beoordeel_belbaarheid(b, bv)))
    for i in range(20):
        b = _bedrijf(osm_id=f"nee{i}", naam=f"NEE{i}", telefoon="038-2")
        kandidaten.append((b, None, ez, score_mod.beoordeel(b, None, ez, kapsalon),
                           belbaar_mod.beoordeel_belbaarheid(b, ez)))

    uitslag = samen_mod.stel_samen(kandidaten, 25, samen_mod.Quota(
        website=10, telefonist=5, automatisering=5))
    bevestig(len(uitslag.gekozen) == 25, f"25 leads gekozen (nu {len(uitslag.gekozen)})")
    bevestig(all(r[4].mag_bellen for r in uitslag.gekozen),
             "elke gekozen lead is belbaar")
    bevestig(not any(r[0].osm_id.startswith("nee") for r in uitslag.gekozen),
             "geen enkele eenmanszaak in de lijst")
    bevestig(uitslag.afgevallen_niet_belbaar == 20,
             f"20 afgevallen als niet-belbaar (nu {uitslag.afgevallen_niet_belbaar})")
    ids = [r[0].osm_id for r in uitslag.gekozen]
    bevestig(len(ids) == len(set(ids)), "geen dubbele leads")

    krap = samen_mod.stel_samen(kandidaten, 25, samen_mod.Quota(
        website=99, telefonist=0, automatisering=0))
    bevestig(krap.tekorten.get("website", 0) > 0,
             "een onhaalbaar quotum wordt als tekort gemeld in plaats van verzwegen")

    # Een bedrijf zonder enkel koopsignaal hoort er niet in, ook niet als de
    # lijst daardoor korter wordt dan gevraagd.
    perfect_site = website_check.SiteRapport(
        url="https://top.nl", bereikbaar=True, status=200, eindurl="https://top.nl",
        https=True, laadtijd_ms=200, mobiel_geschikt=True, heeft_titel=True,
        heeft_meta_omschrijving=True, heeft_structuurdata=True, copyright_jaar=2026,
        online_afspraak=True)
    installatie = catalogus.BRANCHE_OP_SLEUTEL["installatie"]
    geen_reden = _bedrijf(osm_id="perfect", branche="installatie",
                          telefoon="038-9", email="info@top.nl",
                          website="https://top.nl", social="https://facebook.com/t",
                          openingstijden="24/7")
    beoordeling = score_mod.beoordeel(geen_reden, perfect_site, bv, installatie)
    bevestig(not beoordeling.signalen,
             "een bedrijf dat niets mist heeft geen enkel koopsignaal")
    schoon = samen_mod.stel_samen(
        [(geen_reden, perfect_site, bv, beoordeling,
          belbaar_mod.beoordeel_belbaarheid(geen_reden, bv))],
        10, samen_mod.Quota(0, 0, 0))
    bevestig(len(schoon.gekozen) == 0,
             "zo'n bedrijf komt niet in de lijst, ook al is er ruimte")
    bevestig(schoon.afgevallen_zonder_reden == 1,
             "en het wordt geteld als afgevallen zonder koopsignaal")


def test_schrijven():
    print("\nWegschrijven van de uitvoer")
    kapsalon = catalogus.BRANCHE_OP_SLEUTEL["kapsalon"]
    bv = kvk_mod.KvkResultaat(gevonden=True, kvk_nummer="12345678",
                              rechtsvorm="Besloten Vennootschap", is_rechtspersoon=True)
    kandidaten = []
    for i in range(3):
        b = _bedrijf(osm_id=f"node/{i}", naam=f"Bedrijf {i}", telefoon="038-1234567")
        kandidaten.append((b, None, bv, score_mod.beoordeel(b, None, bv, kapsalon),
                           belbaar_mod.beoordeel_belbaarheid(b, bv)))
    samen = samen_mod.stel_samen(kandidaten, 3, samen_mod.Quota(1, 1, 1))

    uitslag = {
        "terrein": catalogus.territorium_voor(_dt.date(2026, 9, 1), land="NL"),
        "rijen": samen.gekozen, "samenstelling": samen,
        "totaal_gevonden": 3, "met_nummer": 3, "osm_fouten": [],
        "kvk_werkt": True, "kvk_bericht": "ok",
        "kvk_zoek_gedaan": 3, "kvk_basis_gedaan": 3, "afgevallen_filiaal": 0,
        "quota": samen_mod.Quota(1, 1, 1),
    }
    with tempfile.TemporaryDirectory() as tijdelijk:
        samenvatting = run_mod.schrijf(uitslag, Path(tijdelijk) / "test")
        csv_pad = Path(samenvatting["csv"])
        bevestig(csv_pad.exists(), "CSV is weggeschreven")
        inhoud = csv_pad.read_text(encoding="utf-8")
        bevestig(inhoud.startswith("score,warmte,bedrijf,telefoon"),
                 "CSV begint met de kolommen die je bij het bellen nodig hebt")
        bevestig(len(inhoud.strip().splitlines()) == 4, "CSV heeft 3 leads + kop")
        bevestig(samenvatting["alles_belbaar"] is True,
                 "de samenvatting bevestigt dat alles belbaar is")
        bevestig("kvk_kosten_indicatie_eur" in samenvatting,
                 "de samenvatting noemt de KVK-kosten van de run")
        eerste = json.loads((Path(tijdelijk) / "test" / "leads.json").read_text())[0]
        bevestig(eerste["waarom_lead"].startswith("1. "),
                 "de redenen staan genummerd in de rij")
        bevestig(eerste["verkoop_primair"], "er staat een dienst om te verkopen bij")
        bevestig(eerste["bellen_mag"] == "JA", "bellen_mag staat op JA")


def test_normaliseren():
    print("\nURL-normalisatie")
    bevestig(website_check._normaliseer("example.nl") == "https://example.nl",
             "kaal domein krijgt https")
    bevestig(website_check._normaliseer("http://a.be") == "http://a.be",
             "http blijft http")
    bevestig(website_check._normaliseer("  ") == "", "lege invoer geeft leeg")


if __name__ == "__main__":
    test_rotatie()
    test_overschrijven()
    test_query()
    test_dode_spiegel()
    test_element_parsing()
    test_kvk_antwoord_lezen()
    test_kvk_dedupe_op_naam()
    test_filiaal_en_leeftijd()
    test_ketens()
    test_scoring()
    test_geen_lege_dag()
    test_belbaarheid()
    test_belbaarheid_belgie()
    test_samenstelling()
    test_schrijven()
    test_normaliseren()
    print("\n" + ("ALLE TESTS GESLAAGD" if not MISLUKT
                  else f"{len(MISLUKT)} TEST(S) MISLUKT: " + "; ".join(MISLUKT)))
    raise SystemExit(1 if MISLUKT else 0)
