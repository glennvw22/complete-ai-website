#!/usr/bin/env python3
"""Genereert sitemap.xml uit de echte git-historie van elke pagina, zodat
lastmod nooit meer stil achterblijft bij een wijziging. Draaien na elke
inhoudelijke wijziging, samen met bouw-paginas.py:  python3 bouw-sitemap.py
"""
import subprocess
from pathlib import Path

DOMEIN = "https://complete-ai.nl"
MAP = Path(__file__).resolve().parent

# (bestand, priority) — volgorde en gewicht zoals op 29-8-2026 vastgesteld:
# home > diensten > gids > branches/case > privacy.
PAGINAS = [
    ("index.html", "1.0"),
    ("websites.html", "0.9"),
    ("automatisering.html", "0.9"),
    ("ai-telefonist.html", "0.9"),
    ("social-media.html", "0.9"),
    ("ai-voor-kapsalons.html", "0.7"),
    ("ai-voor-garagebedrijven.html", "0.7"),
    ("ai-voor-de-horeca.html", "0.7"),
    ("ai-voor-bouw-en-installatie.html", "0.7"),
    ("case-aronza.html", "0.7"),
    ("ai-voor-uw-bedrijf.html", "0.8"),
    ("privacy.html", "0.3"),
]


def laatste_wijziging(bestand):
    """Datum van de laatste commit die dit bestand raakte. Ongecommitte
    wijzigingen (nog niet gepusht) tellen als vandaag."""
    status = subprocess.run(["git", "status", "--porcelain", "--", bestand],
                             cwd=MAP, capture_output=True, text=True).stdout
    if status.strip():
        from datetime import date
        return date.today().isoformat()
    uit = subprocess.run(
        ["git", "log", "-1", "--format=%cd", "--date=format:%Y-%m-%d", "--", bestand],
        cwd=MAP, capture_output=True, text=True).stdout.strip()
    return uit or "2026-08-29"


def bouw():
    regels = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for bestand, prioriteit in PAGINAS:
        loc = f"{DOMEIN}/" if bestand == "index.html" else f"{DOMEIN}/{bestand}"
        lastmod = laatste_wijziging(bestand)
        regels.append("  <url>")
        regels.append(f"    <loc>{loc}</loc>")
        regels.append(f"    <lastmod>{lastmod}</lastmod>")
        regels.append("    <changefreq>monthly</changefreq>")
        regels.append(f"    <priority>{prioriteit}</priority>")
        regels.append("  </url>")
    regels.append("</urlset>")
    regels.append("")
    (MAP / "sitemap.xml").write_text("\n".join(regels), encoding="utf-8")
    print(f"sitemap.xml geschreven, {len(PAGINAS)} pagina's")


if __name__ == "__main__":
    bouw()
