"""Pagina's van het bedrijf zelf ophalen en de tekst bewaren.

WAAROM DIT BESTAAT
------------------
`website_check.py` geeft alleen een oordeel terug (booleans en labels) en
gooit de opgehaalde pagina weg. Daardoor kan niemand achteraf nagaan
waarop een bewering steunt. Op 7 september 2026 bleek wat dat kost: bij
een steekproef van 231 leads met "geen website bekend" had minstens 1 op
de 6 gewoon een werkende website, en de machine adviseerde daar een
nieuwe website. Glenn: "Wij gaan geen mensen bellen over websites die
gewoon een prima website hebben."

Deze module bewaart daarom per opgehaalde pagina de platte tekst, zodat
`poort.py` elke bewering letterlijk kan terugzoeken. Wat niet in een
bewaarde pagina staat, mag niet beweerd worden.

Alleen standaardbibliotheek, net als de rest van leads/. Geen kosten:
gewone HTTP GET naar de website van het bedrijf zelf, robots.txt wordt
gerespecteerd.
"""
from __future__ import annotations

import gzip
import ipaddress
import re
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from dataclasses import dataclass, field

USER_AGENT = "CompleteAI-onderbouwing/1.0 (+https://complete-ai.nl)"
TIMEOUT_S = 12
MAX_BYTES = 400_000
# Homepagina plus de pagina's waar een bedrijf zijn gegevens kwijt kan.
# Meer dan dit is niet beleefd en levert zelden nieuw bewijs op.
CONTACTPADEN = ("/contact", "/contact.html", "/over-ons", "/algemene-voorwaarden",
                "/disclaimer", "/privacy", "/colofon")
MAX_PAGINAS = 4
MAX_OMLEIDINGEN = 4
TOEGESTANE_POORTEN = (80, 443)

_SCRIPT_STIJL = re.compile(r"<(script|style|noscript)\b.*?</\1>", re.I | re.S)
_TAG = re.compile(r"<[^>]+>")
_WITRUIMTE = re.compile(r"[ \t\r\f\v]+")
_LEGE_REGELS = re.compile(r"\n{3,}")


@dataclass(frozen=True)
class Pagina:
    """Eén opgehaalde pagina, met de tekst bewaard."""

    url: str
    bereikbaar: bool
    status: int = 0
    tekst: str = ""
    html_bytes: int = 0
    fout: str = ""

    def bevat(self, citaat: str) -> bool:
        """Staat dit citaat letterlijk (hoofdletterongevoelig) op deze pagina?"""
        if not citaat or not self.tekst:
            return False
        return _normaliseer(citaat) in _normaliseer(self.tekst)


@dataclass
class Dossier:
    """Alles wat we van één bedrijf hebben opgehaald, plus de mislukkingen."""

    start_url: str
    paginas: list[Pagina] = field(default_factory=list)
    robots_verbiedt: bool = False
    fout: str = ""

    @property
    def bereikbare(self) -> list[Pagina]:
        return [p for p in self.paginas if p.bereikbaar and p.tekst]

    @property
    def bezochte_urls(self) -> tuple[str, ...]:
        return tuple(p.url for p in self.bereikbare)

    def vind(self, citaat: str) -> Pagina | None:
        """De eerste bereikbare pagina waar dit citaat letterlijk op staat."""
        for pagina in self.bereikbare:
            if pagina.bevat(citaat):
                return pagina
        return None


def _normaliseer(tekst: str) -> str:
    """Kleine letters, en alle witruimte tot één spatie.

    Ook regeleinden en vaste spaties: een citaat mag niet afketsen op de
    plek waar de opmaak toevallig een regel afbreekt.
    """
    schoon = tekst.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", schoon).strip().lower()


def naar_tekst(html: str) -> str:
    """Platte tekst uit HTML, met de leesvolgorde intact."""
    zonder = _SCRIPT_STIJL.sub(" ", html)
    zonder = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</h[1-6]>", "\n", zonder, flags=re.I)
    plat = _TAG.sub(" ", zonder)
    plat = (plat.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"')
                .replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">")
                .replace("&copy;", "©"))
    plat = _WITRUIMTE.sub(" ", plat)
    return _LEGE_REGELS.sub("\n\n", plat).strip()


class OnveiligAdres(Exception):
    """De URL wijst niet naar het open internet."""


def _adres_is_openbaar(host: str) -> bool:
    """Weigert loopback, privénetwerken en link-local (cloud-metadata).

    Zonder deze controle kan een leadbestand of een omleiding van een
    bedrijfssite de agent laten praten met iets binnen ons eigen netwerk.
    Let op: dit toetst bij elke aanvraag opnieuw, maar verbindt daarna via
    de hostnaam. Tussen toets en verbinding kan een DNS-antwoord in theorie
    wijzigen; dat restrisico accepteren we hier bewust.
    """
    try:
        adressen = socket.getaddrinfo(host, None)
    except OSError:
        return False
    if not adressen:
        return False
    for gegevens in adressen:
        rauw = gegevens[4][0].split("%")[0]
        try:
            ip = ipaddress.ip_address(rauw)
        except ValueError:
            return False
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast or ip.is_unspecified):
            return False
    return True


def controleer_adres(url: str) -> None:
    """Gooit OnveiligAdres als deze URL niet opgehaald mag worden."""
    ontleed = urllib.parse.urlsplit(url)
    if ontleed.scheme not in ("http", "https"):
        raise OnveiligAdres(f"schema '{ontleed.scheme}' niet toegestaan")
    if not ontleed.hostname:
        raise OnveiligAdres("geen hostnaam in de URL")
    poort = ontleed.port or (443 if ontleed.scheme == "https" else 80)
    if poort not in TOEGESTANE_POORTEN:
        raise OnveiligAdres(f"poort {poort} niet toegestaan")
    if not _adres_is_openbaar(ontleed.hostname):
        raise OnveiligAdres(f"'{ontleed.hostname}' wijst niet naar het open internet")


class _GecontroleerdeOmleiding(urllib.request.HTTPRedirectHandler):
    """Volgt een omleiding alleen als het doel ook door de controle komt."""

    max_redirections = MAX_OMLEIDINGEN

    def redirect_request(self, verzoek, fp, code, msg, headers, nieuw_url):
        nieuw = super().redirect_request(verzoek, fp, code, msg, headers, nieuw_url)
        if nieuw is None:
            return None
        controleer_adres(nieuw.full_url)       # OnveiligAdres stopt het ophalen
        return nieuw


_OPENER = urllib.request.build_opener(_GecontroleerdeOmleiding())


def _normaliseer_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url.lstrip("/")
    return url


def _haal_op(url: str) -> Pagina:
    verzoek = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "nl,en;q=0.7",
        "Accept-Encoding": "gzip",
    })
    context = ssl.create_default_context()
    try:
        controleer_adres(url)
        with _OPENER.open(verzoek, timeout=TIMEOUT_S) as antwoord:
            ruw = antwoord.read(MAX_BYTES)
            if antwoord.headers.get("Content-Encoding") == "gzip":
                try:
                    ruw = gzip.decompress(ruw)
                except (OSError, EOFError):
                    # Afgekapt op MAX_BYTES: uitpakken wat er wél is, in plaats
                    # van de hele site als onleesbaar af te schrijven.
                    ontpakker = gzip.zlib.decompressobj(gzip.zlib.MAX_WBITS | 16)
                    try:
                        ruw = ontpakker.decompress(ruw)
                    except Exception:
                        pass
            html = ruw.decode("utf-8", errors="replace")
            return Pagina(url=antwoord.geturl() or url, bereikbaar=True,
                          status=getattr(antwoord, "status", 200) or 200,
                          tekst=naar_tekst(html), html_bytes=len(ruw))
    except OnveiligAdres as fout:
        return Pagina(url=url, bereikbaar=False, fout=f"geweigerd adres: {fout}")
    except urllib.error.HTTPError as fout:
        return Pagina(url=url, bereikbaar=False, status=fout.code, fout=f"HTTP {fout.code}")
    # socket.timeout valt sinds 3.10 onder OSError, maar niet onder URLError:
    # precies de kale uitzondering die eerder een hele dagrun liet crashen.
    except (urllib.error.URLError, ssl.SSLError, socket.timeout, OSError) as fout:
        return Pagina(url=url, bereikbaar=False, fout=f"{type(fout).__name__}: {fout}")
    except Exception as fout:  # nooit de hele run laten vallen op één site
        return Pagina(url=url, bereikbaar=False, fout=f"onverwacht: {type(fout).__name__}: {fout}")


def _lees_robots(basis: str) -> urllib.robotparser.RobotFileParser | None:
    """robots.txt ophalen mét timeout.

    `RobotFileParser.read()` gebruikt urlopen zonder timeout; één hangende
    host houdt dan de hele dagrun tegen. Daarom halen we het bestand zelf
    op en voeren we het aan de ontleder.
    """
    adres = urllib.parse.urljoin(basis, "/robots.txt")
    lezer = urllib.robotparser.RobotFileParser()
    lezer.set_url(adres)
    verzoek = urllib.request.Request(adres, headers={"User-Agent": USER_AGENT})
    try:
        controleer_adres(adres)
        with _OPENER.open(verzoek, timeout=TIMEOUT_S) as antwoord:
            tekst = antwoord.read(MAX_BYTES).decode("utf-8", errors="replace")
    except Exception:
        return None          # geen robots.txt of niet te lezen: dan mag het
    try:
        lezer.parse(tekst.splitlines())
    except Exception:
        return None
    return lezer


def _mag_van_robots(lezer, url: str) -> bool:
    """Bij twijfel: wél ophalen. Alleen een expliciet verbod telt."""
    if lezer is None:
        return True
    try:
        return lezer.can_fetch(USER_AGENT, url)
    except Exception:
        return True


def haal_dossier(website: str, max_paginas: int = MAX_PAGINAS) -> Dossier:
    """Homepagina plus hooguit drie contact-/colofonpagina's ophalen."""
    url = _normaliseer_url(website)
    if not url:
        return Dossier(start_url="", fout="geen website bekend")

    try:
        controleer_adres(url)
    except OnveiligAdres as fout:
        return Dossier(start_url=url, fout=f"geweigerd adres: {fout}")

    robots = _lees_robots(url)
    if not _mag_van_robots(robots, url):
        return Dossier(start_url=url, robots_verbiedt=True,
                       fout="robots.txt van het bedrijf verbiedt het ophalen")

    dossier = Dossier(start_url=url)
    home = _haal_op(url)
    dossier.paginas.append(home)
    if not home.bereikbaar:
        dossier.fout = home.fout
        return dossier

    basis = home.url
    for pad in CONTACTPADEN:
        if len(dossier.paginas) >= max_paginas:
            break
        vervolg = urllib.parse.urljoin(basis, pad)
        if any(p.url.rstrip("/") == vervolg.rstrip("/") for p in dossier.paginas):
            continue
        if not _mag_van_robots(robots, vervolg):
            continue          # elk pad apart toetsen, niet alleen de homepagina
        pagina = _haal_op(vervolg)
        if pagina.bereikbaar:
            dossier.paginas.append(pagina)
    return dossier
