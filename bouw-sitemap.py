#!/usr/bin/env python3
"""Genereert sitemap.xml met een lastmod die klopt.

Google gebruikt <lastmod> alleen als die "consistently and verifiably accurate"
is (developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
Een datum uit git is dat niet: elke commit die een pagina raakt, ook een
nieuwe stempel, verschuift alle pagina's naar dezelfde dag. Daarom hier: de
datum verandert alleen wanneer de inhoud binnen <main> echt verandert. Van die
inhoud (tekst én links) bewaart sitemap-stand.json een afdruk per pagina.
<priority> en <changefreq> worden door Google genegeerd en staan er niet meer in.

Draaien na bouw-paginas.py:  python3 bouw-sitemap.py
"""
import hashlib, json, re, subprocess
from datetime import date
from pathlib import Path

DOMEIN = "https://complete-ai.nl"
MAP = Path(__file__).resolve().parent
STAND = MAP / "sitemap-stand.json"

PAGINAS = [
    "index.html", "websites.html", "automatisering.html", "ai-telefonist.html",
    "social-media.html", "vindbaarheid-seo.html", "adverteren.html",
    "bedrijfsprocessen-automatiseren-voorbeelden.html",
    "ai-voor-kapsalons.html", "ai-voor-garagebedrijven.html", "ai-voor-de-horeca.html",
    "ai-voor-bouw-en-installatie.html", "case-aronza.html", "ai-voor-uw-bedrijf.html",
    "privacy.html", "voorwaarden.html", "gegevens-verwijderen.html",
]


def afdruk(html):
    m = re.search(r"<main>(.*?)</main>", html, re.S)
    inhoud = re.sub(r"\s+", " ", m.group(1) if m else html)
    return hashlib.sha1(inhoud.encode("utf-8")).hexdigest()[:12]


def git(*args):
    r = subprocess.run(["git", *args], cwd=MAP, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def beginstand():
    """Eerste keer: de afdruk en datum van wat nu live staat (HEAD)."""
    oud_sitemap = git("show", "HEAD:sitemap.xml") or ""
    datums = dict(re.findall(r"<loc>https://complete-ai\.nl/?([^<]*)</loc>\s*<lastmod>([^<]+)</lastmod>", oud_sitemap))
    stand = {}
    for bestand in PAGINAS:
        html = git("show", f"HEAD:{bestand}")
        if html is None:
            continue
        sleutel = "" if bestand == "index.html" else bestand
        stand[bestand] = {"afdruk": afdruk(html), "lastmod": datums.get(sleutel, "2026-08-29")}
    return stand


def bouw():
    stand = json.loads(STAND.read_text()) if STAND.exists() else beginstand()
    vandaag = date.today().isoformat()
    regels = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for bestand in PAGINAS:
        nu = afdruk((MAP / bestand).read_text(encoding="utf-8"))
        oud = stand.get(bestand)
        lastmod = oud["lastmod"] if oud and oud["afdruk"] == nu else vandaag
        stand[bestand] = {"afdruk": nu, "lastmod": lastmod}
        loc = f"{DOMEIN}/" if bestand == "index.html" else f"{DOMEIN}/{bestand}"
        regels += ["  <url>", f"    <loc>{loc}</loc>", f"    <lastmod>{lastmod}</lastmod>", "  </url>"]
    regels += ["</urlset>", ""]
    (MAP / "sitemap.xml").write_text("\n".join(regels), encoding="utf-8")
    STAND.write_text(json.dumps(stand, indent=1, ensure_ascii=False) + "\n")
    print(f"sitemap.xml geschreven, {len(PAGINAS)} pagina's")


if __name__ == "__main__":
    bouw()
