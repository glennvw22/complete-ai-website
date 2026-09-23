"""Tests voor de onderbouwingsagent. Geen netwerk: alle pagina's zijn vast.

Draaien:  python3 leads/test_onderbouwing.py
"""
from __future__ import annotations

import datetime as _dt
import sys
import unittest
from pathlib import Path

_HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(_HIER))
sys.path.insert(0, str(_HIER.parent))

from onderbouwing import bewijs, poort, signalen as sig, verstuur  # noqa: E402
from onderbouwing.agent import (beoordeel_bedrijf, kies_categorie,  # noqa: E402
                                naar_contactrij, schrijf_onderbouwing, zoek_adres)

VANDAAG = _dt.date(2026, 9, 23)

GOEDE_SITE = """
<html><body>
<h1>Kapsalon De Kam</h1>
<p>Bel ons voor een afspraak op 038 123 4567. Wij zijn telefonisch bereikbaar
van dinsdag tot zaterdag.</p>
<p>Wegens drukte nemen wij niet altijd direct op.</p>
<footer>Kapsalon De Kam B.V. | KvK 12345678 | info@dekam-voorbeeld.nl
&copy; 2019</footer>
</body></html>
"""

EENMANSZAAK_SITE = """
<html><body><h1>Salon Lisa</h1>
<p>Bel ons voor een afspraak.</p>
<footer>Salon Lisa eenmanszaak, KvK 87654321, info@salonlisa-voorbeeld.nl</footer>
</body></html>
"""

PERSOONLIJK_ADRES_SITE = """
<html><body><h1>Garage Jansen</h1><p>Bel gerust voor een afspraak.</p>
<footer>Garage Jansen B.V., KvK 11112222, henk@garagejansen-voorbeeld.nl</footer>
</body></html>
"""

NETTE_SITE = """
<html><body><h1>Tandarts Brug</h1>
<p>Maak hier <a href="/afspraak">online een afspraak</a>: afspraak maken kan
24 uur per dag.</p>
<footer>Tandarts Brug B.V., KvK 33334444, info@tandartsbrug-voorbeeld.nl
&copy; 2026</footer></body></html>
"""


def _dossier(html: str, url: str = "https://dekam-voorbeeld.nl/") -> bewijs.Dossier:
    pagina = bewijs.Pagina(url=url, bereikbaar=True, status=200,
                           tekst=bewijs.naar_tekst(html), html_bytes=len(html))
    return bewijs.Dossier(start_url=url, paginas=[pagina])


class TestBewijs(unittest.TestCase):
    def test_tekst_blijft_bewaard_en_citaat_is_terug_te_vinden(self):
        dossier = _dossier(GOEDE_SITE)
        self.assertIn("bel ons voor een afspraak", dossier.bereikbare[0].tekst.lower())
        self.assertIsNotNone(dossier.vind("Bel ons voor een afspraak"))

    def test_verzonnen_citaat_wordt_niet_gevonden(self):
        self.assertIsNone(_dossier(GOEDE_SITE).vind("wij zoeken een AI-telefonist"))


class TestSignalen(unittest.TestCase):
    def test_aanwezige_signalen_krijgen_een_citaat_bron_en_datum(self):
        gevonden = sig.verzamel(_dossier(GOEDE_SITE), "Kapsalon De Kam", VANDAAG)
        aanwezig = [s for s in gevonden if s.soort == sig.AANWEZIG]
        self.assertTrue(aanwezig)
        for signaal in aanwezig:
            self.assertTrue(signaal.citaat.strip(), signaal.sleutel)
            self.assertTrue(signaal.bron_url)
            self.assertEqual(signaal.bron_datum, "2026-09-23")

    def test_oud_copyright_telt_wel_en_recent_niet(self):
        oud = {s.sleutel for s in sig.verzamel(_dossier(GOEDE_SITE), "", VANDAAG)}
        nieuw = {s.sleutel for s in sig.verzamel(_dossier(NETTE_SITE, "https://tandartsbrug-voorbeeld.nl/"), "", VANDAAG)}
        self.assertIn("oud_copyright", oud)
        self.assertNotIn("oud_copyright", nieuw)

    def test_afwezigheidssignaal_noemt_de_gelezen_paginas(self):
        gevonden = sig.verzamel(_dossier(GOEDE_SITE), "", VANDAAG)
        afwezig = [s for s in gevonden if s.soort == sig.AFWEZIG]
        self.assertEqual(len(afwezig), 1)
        self.assertIn("https://dekam-voorbeeld.nl/", afwezig[0].zin)

    def test_site_met_online_afspraak_krijgt_geen_afwezigheidssignaal(self):
        gevonden = sig.verzamel(_dossier(NETTE_SITE, "https://tandartsbrug-voorbeeld.nl/"), "", VANDAAG)
        self.assertFalse([s for s in gevonden if s.soort == sig.AFWEZIG])

    def test_rechtsvorm_eenmanszaak_wordt_herkend_als_niet_rechtspersoon(self):
        uitkomst = sig.rechtsvorm_uit_tekst(
            bewijs.naar_tekst(EENMANSZAAK_SITE), "Salon Lisa")
        self.assertIsNotNone(uitkomst)
        self.assertFalse(sig.is_rechtspersoon(uitkomst[0]))

    def test_rechtsvorm_bv_wordt_herkend_als_rechtspersoon(self):
        uitkomst = sig.rechtsvorm_uit_tekst(
            bewijs.naar_tekst(GOEDE_SITE), "Kapsalon De Kam")
        self.assertIsNotNone(uitkomst)
        self.assertTrue(sig.is_rechtspersoon(uitkomst[0]))


class TestPoort(unittest.TestCase):
    def test_poort_weigert_een_verzonnen_citaat(self):
        dossier = _dossier(GOEDE_SITE)
        verzonnen = sig.Signaal("verzonnen", "telefonist", sig.AANWEZIG,
                                "zij zoeken een telefonist",
                                "wij zoeken dringend een AI-telefonist",
                                "https://voorbeeld.nl/", "2026-09-23")
        oordeel = poort.controleer_bewijs([verzonnen], dossier)
        self.assertFalse(oordeel.doorgelaten)
        self.assertIn("staat op geen enkele opgehaalde pagina", " ".join(oordeel.redenen))

    def test_poort_weigert_pitch_die_alleen_op_afwezigheid_steunt(self):
        dossier = _dossier(NETTE_SITE, "https://tandartsbrug-voorbeeld.nl/")
        alleen_afwezig = [sig.Signaal("geen_online_afspraak", "automatisering", sig.AFWEZIG,
                                      f"op de 1 pagina's ({dossier.start_url}) staat niets",
                                      "", dossier.start_url, "2026-09-23")]
        oordeel = poort.controleer_bewijs(alleen_afwezig, dossier)
        self.assertFalse(oordeel.doorgelaten)
        self.assertIn("letterlijk kunnen aanwijzen", " ".join(oordeel.redenen))

    def test_toon_weigert_gedachtestreepje_percentage_en_jijvorm(self):
        self.assertFalse(poort.controleer_toon("Uw site is oud — dat kost klanten.").doorgelaten)
        self.assertFalse(poort.controleer_toon("Dit levert 30% meer afspraken op.").doorgelaten)
        self.assertFalse(poort.controleer_toon("Op je site staat nog 2019.").doorgelaten)
        self.assertTrue(poort.controleer_toon("Onderaan de site staat nog 2019.").doorgelaten)

    def test_toon_weigert_opening_met_ai(self):
        self.assertFalse(poort.controleer_toon("AI kan uw telefoon opnemen.").doorgelaten)

    def test_uitsluitingslijst_blokkeert(self):
        oordeel = poort.controleer_uitsluiting("info@x.nl", {"INFO@X.NL"})
        self.assertFalse(oordeel.doorgelaten)


class TestAgent(unittest.TestCase):
    def test_goed_bedrijf_komt_erdoor_met_onderbouwing_en_categorie(self):
        uitslag = beoordeel_bedrijf("Kapsalon De Kam", "https://voorbeeld.nl/",
                                    vandaag=VANDAAG, dossier=_dossier(GOEDE_SITE))
        self.assertTrue(uitslag.doorgelaten, uitslag.redenen_afgewezen)
        self.assertEqual(uitslag.categorie, "telefonist")
        self.assertEqual(uitslag.email, "info@dekam-voorbeeld.nl")
        self.assertEqual(uitslag.bron_url, "https://dekam-voorbeeld.nl/")
        self.assertEqual(uitslag.bron_datum, "2026-09-23")
        self.assertTrue(uitslag.onderbouwing.endswith("."))

    def test_onderbouwing_bevat_nooit_een_afwezigheidszin(self):
        uitslag = beoordeel_bedrijf("Kapsalon De Kam", "https://voorbeeld.nl/",
                                    vandaag=VANDAAG, dossier=_dossier(GOEDE_SITE))
        self.assertNotIn("gelezen hebben", uitslag.onderbouwing)
        self.assertNotIn("https://", uitslag.onderbouwing)

    def test_eenmanszaak_wordt_geweigerd(self):
        uitslag = beoordeel_bedrijf("Salon Lisa", "https://voorbeeld.nl/",
                                    vandaag=VANDAAG, dossier=_dossier(EENMANSZAAK_SITE, "https://salonlisa-voorbeeld.nl/"))
        self.assertFalse(uitslag.doorgelaten)
        self.assertIn("geen rechtspersoon", " ".join(uitslag.redenen_afgewezen))

    def test_persoonlijk_adres_wordt_geweigerd(self):
        uitslag = beoordeel_bedrijf("Garage Jansen", "https://voorbeeld.nl/",
                                    vandaag=VANDAAG, dossier=_dossier(PERSOONLIJK_ADRES_SITE, "https://garagejansen-voorbeeld.nl/"))
        self.assertFalse(uitslag.doorgelaten)
        self.assertIn("geen e-mailadres gevonden", " ".join(uitslag.redenen_afgewezen))

    def test_nette_site_zonder_koopsignaal_wordt_geweigerd(self):
        uitslag = beoordeel_bedrijf("Tandarts Brug", "https://voorbeeld.nl/",
                                    vandaag=VANDAAG, dossier=_dossier(NETTE_SITE, "https://tandartsbrug-voorbeeld.nl/"))
        self.assertFalse(uitslag.doorgelaten)

    def test_onbereikbare_site_levert_niets_op(self):
        leeg = bewijs.Dossier(start_url="https://voorbeeld.nl/", fout="HTTP 404")
        uitslag = beoordeel_bedrijf("X", "https://voorbeeld.nl/", vandaag=VANDAAG, dossier=leeg)
        self.assertFalse(uitslag.doorgelaten)
        self.assertIn("HTTP 404", " ".join(uitslag.redenen_afgewezen))

    def test_contactrij_heeft_precies_de_velden_van_het_dashboard(self):
        uitslag = beoordeel_bedrijf("Kapsalon De Kam", "https://voorbeeld.nl/",
                                    vandaag=VANDAAG, dossier=_dossier(GOEDE_SITE))
        rij = naar_contactrij(uitslag, "kapsalon", "Zwolle", "NL", 42)
        self.assertEqual(set(rij), {"bedrijf", "email", "website", "bron_url", "bron_datum",
                                    "branche", "plaats", "land", "categorie",
                                    "onderbouwing", "lead_id"})
        self.assertTrue(rij["bron_url"] and rij["bron_datum"])


NV_SITE = """
<html><body><h1>Handelshuis Vermeer</h1>
<p>Bel ons voor een afspraak.</p>
<footer>Handelshuis Vermeer N.V., KvK 55556666, info@vermeer-voorbeeld.nl
&copy; 2018</footer></body></html>
"""

TELEFOON_EN_BOEKEN_SITE = """
<html><body><h1>Praktijk Veld</h1>
<p>Wij zijn telefonisch bereikbaar van 9 tot 17 uur.</p>
<p>U kunt ook online een afspraak maken via onze agenda.</p>
<footer>Praktijk Veld B.V., KvK 77778888, info@praktijkveld-voorbeeld.nl
&copy; 2017</footer></body></html>
"""


class TestAdrescontrole(unittest.TestCase):
    """Uit de beveiligingsreview: de agent mag ons eigen netwerk niet in."""

    def test_intern_en_metadata_adres_worden_geweigerd(self):
        for adres in ("http://127.0.0.1/", "http://localhost/",
                      "http://169.254.169.254/latest/meta-data/",
                      "http://10.0.0.5:9200/_cat/indices", "http://192.168.1.1/"):
            with self.assertRaises(bewijs.OnveiligAdres, msg=adres):
                bewijs.controleer_adres(adres)

    def test_afwijkend_schema_en_poort_worden_geweigerd(self):
        with self.assertRaises(bewijs.OnveiligAdres):
            bewijs.controleer_adres("file:///etc/passwd")
        with self.assertRaises(bewijs.OnveiligAdres):
            bewijs.controleer_adres("http://voorbeeld.nl:6379/")

    def test_geweigerd_adres_levert_een_leeg_dossier_en_geen_uitzondering(self):
        dossier = bewijs.haal_dossier("http://127.0.0.1/")
        self.assertFalse(dossier.bereikbare)
        self.assertIn("geweigerd adres", dossier.fout)

    def test_bedrijf_met_intern_adres_komt_nooit_door_de_poort(self):
        uitslag = beoordeel_bedrijf("Kwaadaardig", "http://169.254.169.254/",
                                    vandaag=VANDAAG)
        self.assertFalse(uitslag.doorgelaten)


class TestNaReview(unittest.TestCase):
    """Gevallen die uit de code-review kwamen."""

    def test_nv_wordt_herkend_als_rechtspersoon(self):
        uitkomst = sig.rechtsvorm_uit_tekst(bewijs.naar_tekst(NV_SITE), "Handelshuis Vermeer")
        self.assertIsNotNone(uitkomst, "N.V. werd niet herkend")
        self.assertTrue(sig.is_rechtspersoon(uitkomst[0]))

    def test_nv_bedrijf_komt_door_de_poort(self):
        uitslag = beoordeel_bedrijf("Handelshuis Vermeer", "https://vermeer-voorbeeld.nl/",
                                    vandaag=VANDAAG,
                                    dossier=_dossier(NV_SITE, "https://vermeer-voorbeeld.nl/"))
        self.assertTrue(uitslag.doorgelaten, uitslag.redenen_afgewezen)

    def test_geen_telefoonclaim_als_de_site_online_boeken_aanbiedt(self):
        dossier = _dossier(TELEFOON_EN_BOEKEN_SITE, "https://praktijkveld-voorbeeld.nl/")
        sleutels = {s.sleutel for s in sig.verzamel(dossier, "Praktijk Veld", VANDAAG)}
        self.assertNotIn("telefoon_is_ingang", sleutels)
        uitslag = beoordeel_bedrijf("Praktijk Veld", "https://praktijkveld-voorbeeld.nl/",
                                    vandaag=VANDAAG, dossier=dossier)
        self.assertNotIn("telefonisch", uitslag.onderbouwing.lower())

    def test_opening_met_twee_woorden_wordt_geweigerd(self):
        self.assertFalse(poort.controleer_toon("Complete AI ziet dat uw site oud is.").doorgelaten)

    def test_draai_levert_leadrijen_met_waarom_lead_en_osm_id(self):
        from onderbouwing.agent import draai
        leads = [{"bedrijf": "Kapsalon De Kam", "website": "https://dekam-voorbeeld.nl/",
                  "branche": "kapsalon", "plaats": "Zwolle", "land": "NL",
                  "osm_id": "node/123"}]
        # Zonder netwerk: laat beoordeel_bedrijf het vaste dossier gebruiken.
        import onderbouwing.agent as agent_mod
        echt = agent_mod.bewijs_mod.haal_dossier
        agent_mod.bewijs_mod.haal_dossier = lambda url, **k: _dossier(GOEDE_SITE)
        try:
            uitslag = draai(leads, maximum=1, vandaag=VANDAAG, logger=lambda *_: None)
        finally:
            agent_mod.bewijs_mod.haal_dossier = echt
        self.assertEqual(len(uitslag["leadrijen"]), 1)
        rij = uitslag["leadrijen"][0]
        self.assertEqual(rij["osm_id"], "node/123")
        self.assertTrue(rij["waarom_lead"])
        self.assertEqual(rij["baan"], "MAIL")


class TestVerstuur(unittest.TestCase):
    def _door(self):
        return beoordeel_bedrijf("Kapsalon De Kam", "https://dekam-voorbeeld.nl/",
                                 vandaag=VANDAAG, dossier=_dossier(GOEDE_SITE))

    def test_alleen_doorgelaten_prospects_komen_in_het_lichaam(self):
        door = self._door()
        af = beoordeel_bedrijf("Salon Lisa", "https://salonlisa-voorbeeld.nl/",
                               vandaag=VANDAAG,
                               dossier=_dossier(EENMANSZAAK_SITE, "https://salonlisa-voorbeeld.nl/"))
        lichaam = verstuur.bouw_lichaam([door, af], {"Kapsalon De Kam": {"branche": "kapsalon"}})
        self.assertEqual(len(lichaam["rijen"]), 1)
        self.assertEqual(lichaam["rijen"][0]["bedrijf"], "Kapsalon De Kam")

    def test_onderbouwing_belandt_in_waarom_lead(self):
        door = self._door()
        rij = verstuur.naar_leadrij(door, {"branche": "kapsalon", "plaats": "Zwolle"})
        self.assertEqual(rij["waarom_lead"], door.onderbouwing)
        self.assertEqual(rij["verkoop_primair"], "AI-telefonist")  # label, zoals run.py
        self.assertEqual(rij["baan"], "MAIL")
        self.assertEqual(rij["bellen_mag"], "NEE")

    def test_droogloop_verstuurt_niets(self):
        uitslag = verstuur.verstuur({"rijen": [{"bedrijf": "X"}]}, logger=lambda *_: None)
        self.assertFalse(uitslag["verstuurd"])
        self.assertEqual(uitslag["reden"], "droogloop")

    def test_zonder_dashboard_url_verstuurt_niets(self):
        uitslag = verstuur.verstuur({"rijen": [{"bedrijf": "X"}]}, url="", sleutel="geheim",
                                    echt=True, logger=lambda *_: None)
        self.assertFalse(uitslag["verstuurd"])
        self.assertEqual(uitslag["reden"], "geen DASHBOARD_URL")

    def test_zonder_sleutel_verstuurt_niets_ook_al_is_echt_gevraagd(self):
        uitslag = verstuur.verstuur({"rijen": [{"bedrijf": "X"}]},
                                    url="https://voorbeeld.invalid/api/leads/import",
                                    sleutel="", echt=True, logger=lambda *_: None)
        self.assertFalse(uitslag["verstuurd"])
        self.assertEqual(uitslag["reden"], "geen sleutel")


if __name__ == "__main__":
    unittest.main(verbosity=2)
