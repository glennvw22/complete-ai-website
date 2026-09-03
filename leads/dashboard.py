"""Verstuurt de zojuist geschreven leadlijst naar het Complete AI-dashboard.

Los bestand (in plaats van een functie middenin run.py) zodat de
HTTP-koppeling apart leesbaar, testbaar en uit te zetten is. Alleen
standaardbibliotheek — geen nieuwe dependency, zelfde aanpak als de rest van
leads/ (vergelijk kvk.py voor hetzelfde patroon: sleutel uit de omgeving,
niets versturen als die ontbreekt).

Benodigde omgevingsvariabelen (zie leads/README.md):
    DASHBOARD_URL         basis-URL van het dashboard, zonder pad,
                           bv. "https://dashboard.complete-ai.nl"
    LEADS_IMPORT_SLEUTEL  dezelfde geheime sleutel als LEADS_IMPORT_SLEUTEL
                           op de dashboardserver (header x-leads-sleutel)

Ontbreekt een van beide, dan wordt deze stap overgeslagen met een duidelijke
logregel — dat is bewust geen fout: de leads staan dan al veilig lokaal
(leads.csv/leads.json), dus een nog niet ingestelde koppeling mag de rest
van de dagrun niet blokkeren. Hetzelfde geldt voor netwerkfouten tijdens het
versturen zelf: die worden gelogd, nooit doorgegeven als crash.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import urllib.error
import urllib.request

# De importroute accepteert tot 20.000 rijen per aanroep (zie
# app/api/leads/import/route.ts, MAX_RIJEN_PER_IMPORT) — 200 blijft daar ver
# onder en houdt één mislukte portie klein t.o.v. een hele dagrun.
PORTIE_GROOTTE = 200
TIMEOUT_SECONDEN = 60


def log(*args) -> None:
    print("[dashboard]", *args, file=sys.stderr, flush=True)


def _lees_rijen(pad_naar_csv) -> list[dict]:
    with open(pad_naar_csv, newline="", encoding="utf-8") as bestand:
        return list(csv.DictReader(bestand))


def _verstuur_portie(url: str, sleutel: str, portie: list[dict]) -> None:
    payload = json.dumps({"rijen": portie}).encode("utf-8")
    verzoek = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json", "x-leads-sleutel": sleutel},
    )

    try:
        with urllib.request.urlopen(verzoek, timeout=TIMEOUT_SECONDEN) as antwoord:
            lichaam = antwoord.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as fout:
        try:
            lichaam = fout.read().decode("utf-8", errors="replace")
        except Exception:
            lichaam = ""
        log(f"portie van {len(portie)} mislukt (HTTP {fout.code}): {lichaam[:300]}")
        return
    except Exception as fout:
        # Nooit crashen op een netwerkfout — de leads staan al lokaal veilig
        # in leads.csv/leads.json, dus loggen en doorgaan met de rest.
        log(f"portie van {len(portie)} mislukt: {type(fout).__name__}: {fout}")
        return

    try:
        antwoord_json = json.loads(lichaam)
    except ValueError:
        log(f"portie van {len(portie)} verstuurd, maar antwoord is geen JSON: {lichaam[:300]}")
        return

    if not antwoord_json.get("ok", False):
        log(f"portie van {len(portie)} afgewezen door dashboard: "
            f"{antwoord_json.get('fout', '(geen foutmelding)')}")
        return

    log(f"portie van {len(portie)} verwerkt — "
        f"toegevoegd {antwoord_json.get('toegevoegd', '?')}, "
        f"bijgewerkt {antwoord_json.get('bijgewerkt', '?')}, "
        f"geblokkeerd {antwoord_json.get('geblokkeerd', '?')}, "
        f"overgeslagen {antwoord_json.get('overgeslagen', '?')}")


def stuur_naar_dashboard(pad_naar_csv) -> None:
    """Leest leads.csv en post 'm in porties van 200 rijen naar het dashboard.

    Slaat de stap over (met een duidelijke logregel) als DASHBOARD_URL of
    LEADS_IMPORT_SLEUTEL niet gezet is, en crasht nooit op een netwerk- of
    leesfout — dit is bewust de allerlaatste stap van de dagrun, ná
    schrijf(), zodat er hoe dan ook al niets verloren is als deze stap
    faalt.
    """
    basis_url = os.environ.get("DASHBOARD_URL", "").strip()
    sleutel = os.environ.get("LEADS_IMPORT_SLEUTEL", "").strip()
    if not basis_url or not sleutel:
        log("DASHBOARD_URL of LEADS_IMPORT_SLEUTEL niet gezet; stap overgeslagen "
            "(de leads staan wel gewoon lokaal in leads.csv/leads.json)")
        return

    try:
        rijen = _lees_rijen(pad_naar_csv)
    except Exception as fout:
        log(f"kon {pad_naar_csv} niet lezen, stap overgeslagen: "
            f"{type(fout).__name__}: {fout}")
        return

    if not rijen:
        log(f"{pad_naar_csv} bevat geen rijen; niets te versturen")
        return

    url = basis_url.rstrip("/") + "/api/leads/import"
    log(f"{len(rijen)} rijen versturen naar {url} in porties van {PORTIE_GROOTTE}")

    for start in range(0, len(rijen), PORTIE_GROOTTE):
        portie = rijen[start:start + PORTIE_GROOTTE]
        _verstuur_portie(url, sleutel, portie)
