"""De onderbouwingsagent: per bedrijf zoeken, bewijzen, en pas dan klaarzetten.

Wat hij doet, in vaste volgorde (geen taalmodel beslist dit, net als bij
Harvey: een beslissing die uit de gegevens volgt kost geen denkwerk):

    1. lead lezen  ->  2. eigen website ophalen  ->  3. signalen bewijzen
    ->  4. rechtsvorm en adres van de eigen site halen  ->  5. POORT
    ->  6. onderbouwing schrijven  ->  7. klaarzetten in de wachtrij

Stap 5 is het verschil met wat we hadden. Alles wat de poort niet kan
bewijzen valt af, met de reden erbij, zichtbaar in het rapport.

Wat hij NIET doet: mailen, bellen, iets versturen, of een betaalde bron
bevragen. Hij zet klaar; een mens kijkt ernaar.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

_HIER = Path(__file__).resolve().parent
if str(_HIER.parent) not in sys.path:      # zodat `leads/`-modules vindbaar zijn
    sys.path.insert(0, str(_HIER.parent))

from belbaar import onpersoonlijk_adres            # noqa: E402  (bestaande regel hergebruiken)

from . import bewijs as bewijs_mod                 # noqa: E402
from . import poort as poort_mod                   # noqa: E402
from . import signalen as sig                      # noqa: E402
from . import verstuur as verstuur_mod             # noqa: E402

# Welk onderdeel van ons aanbod wint als er meerdere signalen zijn.
# Hoogste eerst: waar het snelst geld blijft liggen.
DIENST_VOLGORDE = ("telefonist", "automatisering", "website", "seo", "social", "sea")
MAX_ZINNEN_IN_MAIL = 2

_EMAIL = re.compile(r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b", re.I)
_ONZIN = ("example.com", "domain.com", "sentry.io", "wixpress.com", "@2x", ".png", ".jpg")


@dataclass
class Uitslag:
    """Wat de agent van één bedrijf vond, doorgelaten of niet."""

    bedrijf: str
    website: str
    doorgelaten: bool
    categorie: str = ""
    onderbouwing: str = ""
    email: str = ""
    bron_url: str = ""
    bron_datum: str = ""
    rechtsvorm: str = ""
    signalen: list[dict] = field(default_factory=list)
    gelezen_paginas: list[str] = field(default_factory=list)
    redenen_afgewezen: list[str] = field(default_factory=list)


def zoek_adres(dossier) -> tuple[str, str]:
    """(adres, bron_url) — alleen adressen die zichtbaar op de site staan.

    Een adres dat uitsluitend in een `mailto:`-link zit en nergens leesbaar
    op de pagina, nemen we bewust niet mee: dan kan de poort het citaat niet
    terugvinden, en dat is precies de regel die we niet willen uithollen.
    """
    beste: tuple[int, str, str] | None = None
    voorkeur = ("info", "contact", "mail", "hallo", "welkom", "administratie")
    for pagina in dossier.bereikbare:
        for treffer in _EMAIL.finditer(pagina.tekst):
            adres = treffer.group(0).lower()
            if any(rommel in adres for rommel in _ONZIN):
                continue
            if not onpersoonlijk_adres(adres):
                continue
            lokaal = adres.split("@", 1)[0]
            rang = voorkeur.index(lokaal) if lokaal in voorkeur else len(voorkeur)
            if beste is None or rang < beste[0]:
                beste = (rang, adres, pagina.url)
    return (beste[1], beste[2]) if beste else ("", "")


def kies_categorie(gevonden: list[sig.Signaal]) -> str:
    """Het aanbodonderdeel waar de bewezen signalen naar wijzen."""
    aanwezig = [s for s in gevonden if s.soort == sig.AANWEZIG]
    for dienst in DIENST_VOLGORDE:
        if any(s.dienst == dienst for s in aanwezig):
            return dienst
    return ""


def schrijf_onderbouwing(gevonden: list[sig.Signaal]) -> str:
    """Eén of twee zinnen, uitsluitend uit signalen die letterlijk bewezen zijn.

    Afwezigheidssignalen komen hier nooit in. Ze staan wel in het rapport,
    zodat wij ze zien, maar wij sturen niemand een mail over iets wat wij
    niet hebben zien staan.
    """
    aanwezig = [s for s in gevonden if s.soort == sig.AANWEZIG]
    op_volgorde = sorted(
        aanwezig,
        key=lambda s: DIENST_VOLGORDE.index(s.dienst) if s.dienst in DIENST_VOLGORDE else 99)
    zinnen = []
    for signaal in op_volgorde[:MAX_ZINNEN_IN_MAIL]:
        zin = signaal.zin.strip()
        zinnen.append(zin[0].upper() + zin[1:] if zin else zin)
    return " ".join(z.rstrip(".") + "." for z in zinnen)


def beoordeel_bedrijf(bedrijf: str, website: str,
                      uitgesloten: set[str] | None = None,
                      vandaag: _dt.date | None = None, dossier=None) -> Uitslag:
    """De hele keten voor één bedrijf. `dossier` meegeven scheelt netwerk in tests."""
    vandaag = vandaag or _dt.date.today()
    uitslag = Uitslag(bedrijf=bedrijf, website=website, doorgelaten=False)

    if dossier is None:
        dossier = bewijs_mod.haal_dossier(website)
    uitslag.gelezen_paginas = list(dossier.bezochte_urls)

    if not dossier.bereikbare:
        uitslag.redenen_afgewezen.append(
            dossier.fout or "geen enkele pagina van de eigen site kon gelezen worden")
        return uitslag

    gevonden = sig.verzamel(dossier, bedrijfsnaam=bedrijf, vandaag=vandaag)
    uitslag.signalen = [asdict(s) for s in gevonden]

    adres, bron_url = zoek_adres(dossier)
    uitslag.email, uitslag.bron_url = adres, bron_url
    uitslag.bron_datum = vandaag.isoformat() if adres else ""

    rechtsvorm, rechtsvorm_citaat = "", ""
    for pagina in dossier.bereikbare:
        uitkomst = sig.rechtsvorm_uit_tekst(pagina.tekst, bedrijf)
        if uitkomst:
            rechtsvorm, rechtsvorm_citaat = uitkomst
            break
    uitslag.rechtsvorm = rechtsvorm

    categorie = kies_categorie(gevonden)
    onderbouwing = schrijf_onderbouwing(gevonden)

    oordeel = poort_mod.beoordeel(
        poort_mod.controleer_bewijs(gevonden, dossier),
        poort_mod.controleer_wet(adres, rechtsvorm or None, rechtsvorm_citaat,
                                 bron_url, dossier, onpersoonlijk_adres),
        poort_mod.controleer_toon(onderbouwing),
        poort_mod.controleer_uitsluiting(adres, uitgesloten or set()),
    )
    if not categorie:
        oordeel.weiger("geen aanbodonderdeel aan te wijzen op grond van het bewijs")

    uitslag.doorgelaten = oordeel.doorgelaten
    uitslag.redenen_afgewezen = oordeel.redenen
    if oordeel.doorgelaten:
        uitslag.categorie = categorie
        uitslag.onderbouwing = onderbouwing
    return uitslag


def naar_contactrij(uitslag: Uitslag, branche: str, plaats: str, land: str,
                    lead_id=None) -> dict:
    """Precies de vorm die het dashboard verwacht (KoudeContactInvoerRij)."""
    return {
        "bedrijf": uitslag.bedrijf,
        "email": uitslag.email,
        "website": uitslag.website,
        "bron_url": uitslag.bron_url,
        "bron_datum": uitslag.bron_datum,
        "branche": branche,
        "plaats": plaats,
        "land": land,
        "categorie": uitslag.categorie,
        "onderbouwing": uitslag.onderbouwing,
        "lead_id": lead_id,
    }


def _lees_leads(pad: Path) -> list[dict]:
    if pad.suffix.lower() == ".json":
        data = json.loads(pad.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else data.get("rijen", [])
    with pad.open(encoding="utf-8-sig", newline="") as bestand:
        return list(csv.DictReader(bestand))


def draai(leads: list[dict], uitgesloten: set[str] | None = None,
          maximum: int = 25, vandaag: _dt.date | None = None,
          logger=print) -> dict:
    vandaag = vandaag or _dt.date.today()
    contacten, leadrijen, rapport = [], [], []
    behandeld = 0
    for lead in leads:
        if behandeld >= maximum:
            break
        website = (lead.get("website") or "").strip()
        bedrijf = (lead.get("bedrijf") or "").strip()
        if not website or not bedrijf:
            continue
        behandeld += 1
        logger(f"  [{behandeld}] {bedrijf} — {website}")
        uitslag = beoordeel_bedrijf(bedrijf=bedrijf, website=website,
                                    uitgesloten=uitgesloten, vandaag=vandaag)
        rapport.append(asdict(uitslag))
        if uitslag.doorgelaten:
            contacten.append(naar_contactrij(uitslag, lead.get("branche", ""),
                                             lead.get("plaats", ""),
                                             (lead.get("land") or "NL").upper(),
                                             lead.get("id") or lead.get("lead_id")))
            leadrijen.append(verstuur_mod.naar_leadrij(uitslag, lead))
            logger(f"      door de poort: {uitslag.categorie} | {uitslag.onderbouwing}")
        else:
            logger(f"      afgewezen: {'; '.join(uitslag.redenen_afgewezen)}")
    return {"datum": vandaag.isoformat(), "behandeld": behandeld,
            "doorgelaten": len(contacten), "contacten": contacten,
            "leadrijen": leadrijen, "rapport": rapport}


def main(argv: list[str] | None = None) -> int:
    ontleder = argparse.ArgumentParser(
        description="Zoekt per bedrijf bewijs op de eigen website en zet alleen "
                    "onderbouwde prospects klaar. Verstuurt nooit iets.")
    ontleder.add_argument("--leads", type=Path, help="leads.json of leads.csv")
    ontleder.add_argument("--site", help="losse website om te toetsen")
    ontleder.add_argument("--bedrijf", default="", help="bedrijfsnaam bij --site")
    ontleder.add_argument("--uit", type=Path, help="map om de uitvoer in te schrijven")
    ontleder.add_argument("--max", type=int, default=25, dest="maximum")
    ontleder.add_argument("--uitsluitingen", type=Path,
                          help="bestand met één uitgesloten e-mailadres per regel")
    ontleder.add_argument("--echt", action="store_true",
                          help="stuur de doorgelaten prospects echt naar het "
                               "dashboard (standaard is droogloop)")
    argumenten = ontleder.parse_args(argv)

    if argumenten.site:
        leads = [{"bedrijf": argumenten.bedrijf or argumenten.site, "website": argumenten.site}]
    elif argumenten.leads:
        leads = _lees_leads(argumenten.leads)
    else:
        ontleder.error("geef --leads of --site")
        return 2

    uitgesloten: set[str] = set()
    if argumenten.uitsluitingen:
        uitgesloten = {regel.strip().lower()
                       for regel in argumenten.uitsluitingen.read_text(
                           encoding="utf-8").splitlines() if regel.strip()}
        print(f"Uitsluitingslijst: {len(uitgesloten)} adressen")

    print(f"Onderbouwingsagent: {len(leads)} leads, maximaal {argumenten.maximum}")
    uitslag = draai(leads, uitgesloten=uitgesloten, maximum=argumenten.maximum)
    print(f"\nBehandeld: {uitslag['behandeld']} | door de poort: {uitslag['doorgelaten']}")

    if argumenten.uit:
        argumenten.uit.mkdir(parents=True, exist_ok=True)
        (argumenten.uit / "koude-contacten.json").write_text(
            json.dumps({"rijen": uitslag["contacten"]}, ensure_ascii=False, indent=1),
            encoding="utf-8")
        (argumenten.uit / "rapport.json").write_text(
            json.dumps(uitslag["rapport"], ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Geschreven naar {argumenten.uit}")

    # Naar het dashboard gaat de LEADrij (waarom_lead, baan, osm_id), niet de
    # koude-contactrij: /api/leads/import ontdubbelt op osm_id en weigert
    # leads die op klant of niet_bellen staan.
    print(verstuur_mod.verstuur({"rijen": uitslag["leadrijen"]}, echt=argumenten.echt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
