"""Doorgelaten prospects naar het bestaande dashboard sturen.

Geen nieuw kanaal: dit gebruikt het endpoint dat er al is,
`POST /api/leads/import` met de header `x-leads-sleutel` — hetzelfde pad
dat `leads/dashboard.py` gebruikt. Daar zit de ontdubbeling op `osm_id`
al in, en leads met status `klant` of `niet_bellen` worden daar
geweigerd; die regels hoeven hier dus niet nagebouwd te worden.

De truc waardoor er aan de dashboardkant niets hoeft te veranderen:
`lib/koude-oogst.ts` zet `onderbouwing: lead.waarom_lead` in het koude
contact. Zetten wij onze bewezen onderbouwing in `waarom_lead`, dan komt
precies die tekst in de wachtrij terecht, met de bron-URL en bron-datum
die de oogst er zelf bij zet.

Wat hier bewust NIET gebeurt: versturen van e-mail, en standaard ook geen
POST. `--echt` is nodig om iets te verzenden, en zonder sleutel gebeurt er
sowieso niets.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

_HIER = Path(__file__).resolve().parent
if str(_HIER.parent) not in sys.path:
    sys.path.insert(0, str(_HIER.parent))

from catalogus import DIENSTEN                      # noqa: E402

# Zelfde afspraak als leads/dashboard.py: de basis-URL komt uit de omgeving,
# nooit uit een vaste waarde hier. Staat hij niet, dan gebeurt er niets.
BASIS_ENV = "DASHBOARD_URL"
SLEUTEL_ENV = "LEADS_IMPORT_SLEUTEL"
PAD = "/api/leads/import"
BEWEZEN_VOORVOEGSEL = "bewezen via eigen site"


def naar_leadrij(uitslag, lead: dict) -> dict:
    """De rij zoals `/api/leads/import` hem verwacht (LeadInvoerRij).

    Alleen velden die wij daadwerkelijk bewezen hebben. `status` en
    `notitie` sturen we niet mee: die horen bij het dashboard en worden
    bij een update met rust gelaten.
    """
    return {
        "bedrijf": uitslag.bedrijf,
        "website": uitslag.website,
        "email": uitslag.email,
        "branche": lead.get("branche", ""),
        "plaats": lead.get("plaats", ""),
        "land": (lead.get("land") or "NL").upper(),
        "osm_id": lead.get("osm_id", ""),
        # run.py schrijft hier het label, niet de sleutel; dat houden we aan.
        "verkoop_primair": DIENSTEN.get(uitslag.categorie, uitslag.categorie),
        "waarom_lead": uitslag.onderbouwing,
        "rechtsvorm": uitslag.rechtsvorm,
        # Het dashboard herkent bewezen leads aan dit voorvoegsel
        # (lib/koude-categorie.ts, BEWEZEN_VOORVOEGSEL). Alleen die mogen naar
        # een campagne voor een aanbodonderdeel.
        "website_status": (f"{BEWEZEN_VOORVOEGSEL} op {uitslag.bron_datum} "
                           f"({len(uitslag.gelezen_paginas)} pagina's)"),
        "zekerheid": "hoog",
        "baan": "MAIL",
        "bellen_mag": "NEE",
        "bellen_grond": "alleen gemaild op grond van bewezen signalen; bellen vereist KVK-bevestiging",
    }


def bouw_lichaam(uitslagen, leads_op_naam: dict) -> dict:
    """Alleen doorgelaten prospects, nooit de afgewezen."""
    rijen = [naar_leadrij(u, leads_op_naam.get(u.bedrijf, {}))
             for u in uitslagen if u.doorgelaten]
    return {"rijen": rijen}


def verstuur(lichaam: dict, url: str = "", sleutel: str = "", echt: bool = False,
             logger=print) -> dict:
    """POST naar het dashboard. Zonder `echt=True` gebeurt er niets."""
    basis = (os.environ.get(BASIS_ENV, "") or "").strip().rstrip("/")
    url = url or (basis + PAD if basis else "")
    sleutel = sleutel or os.environ.get(SLEUTEL_ENV, "")
    aantal = len(lichaam.get("rijen", []))

    if not echt:
        bestemming = url or f"(geen {BASIS_ENV} gezet)"
        logger(f"Droogloop: {aantal} rijen NIET verstuurd naar {bestemming}")
        return {"verstuurd": False, "reden": "droogloop", "rijen": aantal}
    if not url:
        logger(f"Geen {BASIS_ENV} gezet, dus niets verstuurd.")
        return {"verstuurd": False, "reden": f"geen {BASIS_ENV}", "rijen": aantal}
    if not sleutel:
        logger(f"Geen {SLEUTEL_ENV} gezet, dus niets verstuurd.")
        return {"verstuurd": False, "reden": "geen sleutel", "rijen": aantal}
    if aantal == 0:
        return {"verstuurd": False, "reden": "niets doorgelaten", "rijen": 0}

    verzoek = urllib.request.Request(
        url, data=json.dumps(lichaam).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json", "x-leads-sleutel": sleutel})
    try:
        with urllib.request.urlopen(verzoek, timeout=60) as antwoord:
            uitslag = json.loads(antwoord.read().decode("utf-8"))
        logger(f"Verstuurd: {uitslag}")
        return {"verstuurd": True, "antwoord": uitslag, "rijen": aantal}
    except urllib.error.HTTPError as fout:
        return {"verstuurd": False, "reden": f"HTTP {fout.code}: {fout.read()[:200]!r}",
                "rijen": aantal}
    except Exception as fout:
        return {"verstuurd": False, "reden": f"{type(fout).__name__}: {fout}", "rijen": aantal}
