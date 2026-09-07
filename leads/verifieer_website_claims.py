"""Past echte zoekbevindingen toe op een net geschreven leads-CSV, vóór
verzending naar het dashboard.

WAAROM DIT BESTAAT
------------------
`website_status = "geen website bekend"` (zie run.py) betekent niet "we
hebben gecontroleerd en dit bedrijf heeft geen website" — het betekent
"de bronregistratie (OpenStreetMap) had geen website-adres voor dit
bedrijf". Dat is een aanname bij ontbrekende data, geen meting (score.py
markeert dit signaal zelf als `hard=False`).

Op 7 september 2026 bleek bij een steekproef van de destijds 231 leads met
deze status dat minstens 1 op de 6 gewoon een werkende website had —
onder meer Boerenbond in Roosendaal (boerenbond.nl). De machine adviseerde
daar dus "nieuwe website" tegen een bedrijf dat er al een heeft. Glenn:
"Wij gaan geen mensen bellen over websites die gewoon een prima website
hebben. Dat is dikke vette onzin."

Dit script lost het niet zelf op — dat kan niet zonder een echte
zoekopdracht, en dit is platte Python zonder een (betaalde) zoek-API. De
AGENT die de dagelijkse routine draait (leads-naar-dashboard) heeft die
zoekopdracht wel (WebSearch), en gebruikt dit script om zijn bevindingen
mechanisch en foutloos in de CSV te verwerken — zodat het handmatig
bewerken van CSV-rijen (foutgevoelig, makkelijk een kolom te verschuiven)
niet meer nodig is.

GEBRUIK
-------
    python3 leads/verifieer_website_claims.py <pad-naar-leads.csv> <pad-naar-verdicten.json>

verdicten.json is een lijst van objecten, één per gecontroleerd bedrijf:
    [
      {"osm_id": "node/123", "heeft_website": true, "url": "https://...",
       "zekerheid": "hoog", "toelichting": "eigen domein, laadt, toont bedrijfsinfo"},
      {"osm_id": "node/456", "heeft_website": false, "url": null,
       "zekerheid": "hoog", "toelichting": "geen enkel spoor, ook niet via zoekopdracht"},
      ...
    ]

Alleen rijen met status "geen website bekend" EN een osm_id dat in het
verdictenbestand voorkomt worden aangepast. Rijen met zekerheid "laag"
worden bewust NOOIT toegepast — bij twijfel blijft de voorzichtige,
onbevestigde status staan (die het belscherm apart markeert), in plaats
van een lead onterecht te laten vervallen op een onzekere conclusie.

Schrijft de CSV in-place terug; het origineel komt ernaast te staan als
<bestand>.voor-verificatie.bak.
"""
from __future__ import annotations

import csv
import datetime as _dt
import json
import shutil
import sys
from pathlib import Path

from catalogus import DIENSTEN

WEBSITE_DIENST = DIENSTEN["website"]
ONBEVESTIGD = "geen website bekend"


def _diensten_uit_waarom(waarom_lead: str) -> list[tuple[str, str]]:
    """Haalt (tekst, dienst) uit "1. tekst [dienst] 2. tekst [dienst] ..."."""
    import re

    stukken = re.split(r"(?=\d+\.\s)", waarom_lead.strip())
    resultaat = []
    for stuk in stukken:
        stuk = stuk.strip()
        if not stuk:
            continue
        match = re.match(r"\d+\.\s*(.*?)\s*\[([^\]]+)\]\s*$", stuk)
        if match:
            resultaat.append((match.group(1).strip(), match.group(2).strip()))
    return resultaat


def _herbouw_waarom(paren: list[tuple[str, str]]) -> str:
    return " ".join(f"{i}. {tekst} [{dienst}]" for i, (tekst, dienst) in enumerate(paren, start=1))


def verwerk_rij(rij: dict, verdict: dict, vandaag: str) -> dict:
    """Past één verdict toe op één CSV-rij. Geeft de (mogelijk gewijzigde) rij terug."""
    if rij.get("website_status") != ONBEVESTIGD:
        return rij  # niet het geval waar dit script over gaat, ongemoeid laten

    zekerheid = verdict.get("zekerheid")
    if zekerheid == "laag":
        return rij  # bij twijfel: niets aanpassen, de onzekere status blijft staan

    if verdict.get("heeft_website"):
        url = verdict.get("url") or ""
        if not url:
            return rij  # "heeft website" zonder URL is geen bruikbaar verdict, niets aanpassen

        paren = _diensten_uit_waarom(rij.get("waarom_lead", ""))
        overige = [(t, d) for (t, d) in paren if d != WEBSITE_DIENST]

        rij["waarom_lead"] = _herbouw_waarom(overige)
        # de eerstvolgende overgebleven dienst wordt primair, de daaropvolgende secundair
        rij["verkoop_primair"] = overige[0][1] if len(overige) >= 1 else ""
        rij["verkoop_secundair"] = overige[1][1] if len(overige) >= 2 else ""
        rij["website"] = url
        rij["website_status"] = (
            f"heeft wél een werkende website (bevestigd via zoekopdracht op {vandaag}) "
            "— websiteadvies daarom niet gegeven"
        )
    else:
        # confirmed negative: nu een meting/onderzoek, geen aanname meer.
        # De letterlijke tekst verandert bewust, zodat het belscherm
        # (components/bellen/Gespreksadvies.tsx, WEBSITE_ONBEVESTIGD) dit
        # niet meer als onbevestigd markeert.
        rij["website_status"] = f"geen website gevonden (bevestigd via zoekopdracht op {vandaag})"

    return rij


def main() -> int:
    if len(sys.argv) != 3:
        print("gebruik: python3 verifieer_website_claims.py <leads.csv> <verdicten.json>", file=sys.stderr)
        return 2

    csv_pad = Path(sys.argv[1])
    verdicten_pad = Path(sys.argv[2])
    vandaag = _dt.date.today().isoformat()

    with verdicten_pad.open(encoding="utf-8") as f:
        verdicten_lijst = json.load(f)
    verdicten = {v["osm_id"]: v for v in verdicten_lijst if v.get("osm_id")}

    with csv_pad.open(newline="", encoding="utf-8") as f:
        lezer = csv.DictReader(f)
        kolommen = lezer.fieldnames
        rijen = list(lezer)

    aangepast_naar_website = 0
    aangepast_bevestigd_geen = 0
    overgeslagen_laag = 0

    for rij in rijen:
        osm_id = rij.get("osm_id")
        if rij.get("website_status") != ONBEVESTIGD or osm_id not in verdicten:
            continue
        verdict = verdicten[osm_id]
        voor = rij.get("website_status")
        rij = verwerk_rij(rij, verdict, vandaag)
        if rij.get("website_status") == voor and verdict.get("zekerheid") == "laag":
            overgeslagen_laag += 1
        elif verdict.get("heeft_website"):
            aangepast_naar_website += 1
        else:
            aangepast_bevestigd_geen += 1

    backup_pad = csv_pad.with_suffix(csv_pad.suffix + ".voor-verificatie.bak")
    shutil.copyfile(csv_pad, backup_pad)

    with csv_pad.open("w", newline="", encoding="utf-8") as f:
        schrijver = csv.DictWriter(f, fieldnames=kolommen)
        schrijver.writeheader()
        schrijver.writerows(rijen)

    print(json.dumps({
        "gecontroleerd": len(verdicten),
        "bleek_wel_website_advies_aangepast": aangepast_naar_website,
        "bevestigd_geen_website": aangepast_bevestigd_geen,
        "overgeslagen_lage_zekerheid": overgeslagen_laag,
        "backup": str(backup_pad),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
