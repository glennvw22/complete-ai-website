"""Websitecheck: van "heeft een site" naar "heeft een site die geld kost".

Dit is het hart van de nieuwe kwalificatie. De oude routine keek alleen of er
een website was. Hier meten we per site meerdere koopsignalen, elk gekoppeld
aan een dienst van Complete AI.
"""
from __future__ import annotations

import gzip
import re
import ssl
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, asdict

USER_AGENT = (
    "Mozilla/5.0 (compatible; Complete-AI-leadcheck/1.0; +https://complete-ai.nl)"
)

# Veel sites zetten een firewall voor alles wat zich als bot voorstelt. Die
# geven dan 403 of 429 terug terwijl de site het voor bezoekers prima doet.
# Bij zo'n code proberen we het nog een keer als gewone browser.
BROWSER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

# Codes die zeggen "ik laat jou niet binnen", niet "deze site is stuk".
BLOKKADE_CODES = (401, 403, 405, 406, 429, 999)

# Bouwers/technieken die op een verouderde of afgeknepen site wijzen.
VEROUDERDE_SPOREN = (
    ("jimdo", "Jimdo-site"),
    ("wix.com", "Wix"),
    ("weebly", "Weebly"),
    ("webnode", "Webnode"),
    ("jouwweb", "JouwWeb"),
    ("mijnwebwinkel", "Mijnwebwinkel"),
    ("frontpage", "Microsoft FrontPage"),
    ("dreamweaver", "Dreamweaver"),
    ("jquery-1.", "jQuery 1.x"),
    ("jquery/1.", "jQuery 1.x"),
    ("<frameset", "frames-layout"),
    ("flash", "Flash-resten"),
)

AFSPRAAK_SPOREN = (
    "afspraak", "reserveer", "reserveren", "boek nu", "online boeken", "booking",
    "bestellen", "bestel online", "offerte aanvragen", "plan een", "agenda",
    "calendly", "salonized", "treatwell", "formitable", "resengo", "thuisbezorgd",
)

SOCIAL_HOSTS = ("facebook.com", "instagram.com", "linktr.ee", "linktree",
                "linkedin.com", "tiktok.com")


@dataclass
class SiteRapport:
    url: str = ""
    bereikbaar: bool = False
    status: int = 0
    eindurl: str = ""
    https: bool = False
    ssl_fout: bool = False
    laadtijd_ms: int = 0
    mobiel_geschikt: bool = False       # viewport meta aanwezig
    heeft_titel: bool = False
    heeft_meta_omschrijving: bool = False
    heeft_structuurdata: bool = False   # schema.org / JSON-LD
    copyright_jaar: int = 0
    verouderde_techniek: tuple = ()
    online_afspraak: bool = False
    alleen_social: bool = False
    geparkeerd: bool = False
    geblokkeerd: bool = False           # firewall weert de controle, site zelf onbekend
    bytes_html: int = 0
    fout: str = ""

    def als_dict(self) -> dict:
        d = asdict(self)
        d["verouderde_techniek"] = ", ".join(self.verouderde_techniek)
        return d


def _normaliseer(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url.lstrip("/")
    return url


def _lees(url: str, timeout: int = 15,
          user_agent: str = USER_AGENT) -> tuple[int, str, bytes, bool]:
    """Geeft (status, eindurl, body, ssl_fout)."""
    context = ssl.create_default_context()
    verzoek = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "nl,en;q=0.8",
            "Accept-Encoding": "gzip",
        },
    )
    try:
        with urllib.request.urlopen(verzoek, timeout=timeout, context=context) as a:
            rauw = a.read(400_000)
            if a.headers.get("Content-Encoding") == "gzip":
                try:
                    rauw = gzip.decompress(rauw)
                except OSError:
                    pass
            return a.status, a.geturl(), rauw, False
    except urllib.error.HTTPError as fout:
        return fout.code, url, b"", False
    except ssl.SSLError:
        return 0, url, b"", True
    except urllib.error.URLError as fout:
        return 0, url, b"", isinstance(fout.reason, ssl.SSLError)


def controleer(url: str) -> SiteRapport:
    genormaliseerd = _normaliseer(url)
    rapport = SiteRapport(url=genormaliseerd)
    if not genormaliseerd:
        return rapport

    if any(host in genormaliseerd.lower() for host in SOCIAL_HOSTS):
        rapport.alleen_social = True

    start = time.monotonic()
    status, eindurl, body, ssl_fout = _lees(genormaliseerd)

    # Faalt https? Probeer http: een site zonder werkend SSL is juist een koopsignaal.
    if status == 0 and genormaliseerd.startswith("https://"):
        status, eindurl, body, ssl_fout_http = _lees(
            "http://" + genormaliseerd.split("://", 1)[1]
        )
        ssl_fout = ssl_fout or ssl_fout_http

    # Weggestuurd omdat we ons als bot voorstelden? Dan zegt die code niets
    # over de site. Nog een keer, nu als gewone browser. De klok gaat opnieuw
    # aan, anders telt de geweigerde poging mee als laadtijd.
    if status in BLOKKADE_CODES:
        start = time.monotonic()
        status2, eindurl2, body2, ssl_fout2 = _lees(
            genormaliseerd, user_agent=BROWSER_AGENT
        )
        if status2 not in BLOKKADE_CODES and status2 != 0:
            status, eindurl, body, ssl_fout = status2, eindurl2, body2, ssl_fout2
        else:
            rapport.geblokkeerd = True

    rapport.laadtijd_ms = int((time.monotonic() - start) * 1000)
    rapport.status = status
    rapport.eindurl = eindurl
    rapport.ssl_fout = ssl_fout
    rapport.https = eindurl.startswith("https://") and not ssl_fout
    rapport.bytes_html = len(body)

    if status == 0 or not body:
        if rapport.geblokkeerd:
            rapport.fout = f"controle geweerd door de site (status {status})"
        else:
            rapport.fout = ("onbereikbaar of leeg" if status == 0
                            else f"status {status}")
        rapport.bereikbaar = status != 0 and 200 <= status < 400
        return rapport

    rapport.bereikbaar = 200 <= status < 400
    tekst = body.decode("utf-8", "replace")
    laag = tekst.lower()

    if any(host in eindurl.lower() for host in SOCIAL_HOSTS):
        rapport.alleen_social = True

    rapport.heeft_titel = bool(re.search(r"<title[^>]*>\s*\S", laag))
    rapport.heeft_meta_omschrijving = bool(
        re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'][^"\']{20,}', laag)
    )
    rapport.mobiel_geschikt = bool(re.search(r'<meta[^>]+name=["\']viewport["\']', laag))
    rapport.heeft_structuurdata = ("schema.org" in laag or "application/ld+json" in laag)
    rapport.online_afspraak = any(spoor in laag for spoor in AFSPRAAK_SPOREN)

    jaren = re.findall(r"(?:©|&copy;|copyright)[^0-9]{0,20}(20\d{2})", laag)
    jaren += re.findall(r"(20\d{2})\s*(?:©|&copy;)", laag)
    if jaren:
        rapport.copyright_jaar = max(int(j) for j in jaren)

    rapport.verouderde_techniek = tuple(
        label for spoor, label in VEROUDERDE_SPOREN if spoor in laag
    )

    # Geparkeerd/te koop domein: weinig inhoud plus typische bewoording.
    if len(body) < 6000 and any(
        s in laag for s in ("domein te koop", "this domain", "domain for sale",
                            "under construction", "in aanbouw", "coming soon",
                            "binnenkort online", "parkeerpagina")
    ):
        rapport.geparkeerd = True

    return rapport


def controleer_veel(urls: list[str], werkers: int = 12) -> dict[str, SiteRapport]:
    """Parallelle check. Netwerk is de bottleneck, dus threads volstaan."""
    uniek = [u for u in dict.fromkeys(urls) if u]
    if not uniek:
        return {}
    with ThreadPoolExecutor(max_workers=werkers) as pool:
        rapporten = list(pool.map(controleer, uniek))
    return dict(zip(uniek, rapporten))
