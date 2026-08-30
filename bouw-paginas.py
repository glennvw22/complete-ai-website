#!/usr/bin/env python3
"""Genereert de dienstpagina's van Complete AI uit één sjabloon.

Kop, voet, navigatie en structuurdata staan hier één keer, zodat ze op
elke pagina identiek zijn. Inhoud per pagina staat onderaan in PAGINAS.
Draaien met:  python3 bouw-paginas.py
"""
import json, html, os, hashlib, re


def stempel(bestand):
    """Korte afdruk van de inhoud. Verandert het bestand, dan verandert de URL,
    en haalt elke browser hem opnieuw op in plaats van de oude uit zijn cache."""
    pad = os.path.join(os.path.dirname(os.path.abspath(__file__)), bestand)
    with open(pad, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


CSS_V = stempel("stijl.css")
JS_V = stempel("script.js")

DOMEIN = "https://complete-ai.nl"


MERK_SVG = """<svg viewBox="0 0 32 32" aria-hidden="true">
        <rect x="2.34" y="2.34" width="27.32" height="27.32" rx="8.8" fill="none" stroke="#2E7BFF" stroke-width="1.68"/>
        <path d="M10.57 16L21.43 10.06M10.57 16L21.43 21.94M21.43 10.06V21.94" stroke="#2E7BFF" stroke-width="1.34" stroke-linecap="round" fill="none"/>
        <circle cx="10.57" cy="16" r="2.58" fill="#6FA2FF"/>
        <circle cx="21.43" cy="10.06" r="2.58" fill="#6FA2FF"/>
        <circle cx="21.43" cy="21.94" r="2.58" fill="#6FA2FF"/>
      </svg>"""

NAV = [("websites.html", "Websites"),
       ("automatisering.html", "Automatisering"),
       ("ai-telefonist.html", "AI-telefonist"),
       ("social-media.html", "Social media"),
       ("index.html#pakketten", "Pakketten"),
       ("index.html#over", "Over Glenn")]

KLOK = ('<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" '
        'stroke-width="1.6" stroke-linecap="round"><circle cx="8" cy="8" r="6.2"/>'
        '<path d="M8 4.6V8l2.4 1.5"/></svg>')

PIJL = ('<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" '
        'stroke-width="2.2"><path d="M2 8h11M9 4l4 4-4 4"/></svg>')


def kop_html(actief):
    stukjes = []
    for h, t in NAV:
        huidig = ' aria-current="page"' if h == actief else ''
        stukjes.append('\n      <a href="%s"%s>%s</a>' % (h, huidig, t))
    links = "".join(stukjes)
    return f"""<header class="balk" id="balk">
  <div class="wrap">
    <button type="button" class="menuknop" id="menuknop" aria-expanded="false" aria-controls="mobielmenu" aria-label="Menu openen">
      <span></span><span></span><span></span>
    </button>
    <a class="merk" href="index.html" aria-label="Complete AI, naar de homepage">
      {MERK_SVG}
      <b>Complete<span> AI</span></b>
    </a>
    <nav class="menu">{links}
    </nav>
    <a class="knop knop-vol" href="index.html#contact">Plan een intake</a>
  </div>
  <div class="mobiel-waas" id="mobielwaas"></div>
  <div class="mobiel" id="mobielmenu">
    <a class="knop knop-vol mm-actie" href="index.html#contact">Plan een gratis intake</a>
    <p class="mm-kop">Diensten</p>
    <ul class="mm-lijst">
      <li><a href="websites.html">Websites<span>Live in 1 tot 2 weken</span></a></li>
      <li><a href="index.html#diensten">Vindbaarheid — SEO<span>Lokale SEO en het Google-bedrijfsprofiel</span></a></li>
      <li><a href="index.html#diensten">Adverteren — SEA<span>Google Ads en Meta, op aanvraag</span></a></li>
      <li><a href="automatisering.html">Automatisering<span>Live binnen enkele werkdagen</span></a></li>
      <li><a href="ai-telefonist.html">AI-telefonist<span>Operationeel binnen 2 weken</span></a></li>
      <li><a href="social-media.html">Social media<span>Eerste bericht binnen een week</span></a></li>
    </ul>
    <p class="mm-kop">Meer</p>
    <ul class="mm-lijst">
      <li><a href="index.html#pakketten">Pakketten<span>Stel zelf een pakket samen</span></a></li>
      <li><a href="index.html#over">Over Glenn<span>Wie u aan de lijn krijgt</span></a></li>
    </ul>
    <p class="mm-voet">glenn@complete-ai.nl · Nederland &amp; België</p>
  </div>
</header>"""


VOET = f"""<footer>
  <div class="wrap">
    <div class="voet">
      <div>
        <a class="merk" href="index.html" aria-label="Complete AI">
          {MERK_SVG}
          <b>Complete<span> AI</span></b>
        </a>
        <p style="max-width:38ch">Websites, vindbaarheid, advertenties, automatisering en AI-telefonie voor ondernemers in Nederland en België.</p>
      </div>
      <div>
        <p class="voetkop">Diensten</p>
        <ul>
          <li><a href="websites.html">Websites</a></li>
          <li><a href="index.html#diensten">Vindbaarheid — SEO</a></li>
          <li><a href="index.html#diensten">Adverteren — SEA</a></li>
          <li><a href="automatisering.html">Automatisering</a></li>
          <li><a href="ai-telefonist.html">AI-telefonist</a></li>
          <li><a href="social-media.html">Social media</a></li>
          <li><a href="case-aronza.html">Klantcase: Aronza</a></li>
          <li><a href="ai-voor-uw-bedrijf.html">Gids: AI voor uw bedrijf</a></li>
        </ul>
      </div>
      <div>
        <p class="voetkop">Contact</p>
        <ul>
          <li><a href="mailto:glenn@complete-ai.nl">glenn@complete-ai.nl</a></li>
          <li><a href="index.html#contact">Plan een intake</a></li>
          <li><a href="index.html#vragen">Veelgestelde vragen</a></li>
          <li><a href="privacy.html">Privacyverklaring</a></li>
        </ul>
      </div>
    </div>
    <!-- VERVANG: KvK- en btw-nummer invullen zodra de inschrijving rond is (wettelijk verplicht) -->
    <div class="slot">
      <span>© <span id="jaar">2026</span> Complete AI</span>
      <span>Nederland &amp; België</span>
      <span><a href="privacy.html">Privacyverklaring</a></span>
    </div>
  </div>
</footer>"""


def schema(p):
    hoofd = ({"@type": "Article",
              "@id": f"{DOMEIN}/{p['bestand']}#case",
              "headline": p["dienst"],
              "description": p["omschrijving"],
              "author": {"@type": "Organization", "@id": f"{DOMEIN}/#organisatie", "name": "Complete AI"},
              "publisher": {"@type": "Organization", "@id": f"{DOMEIN}/#organisatie", "name": "Complete AI"},
              "inLanguage": "nl-NL",
              "datePublished": "2026-08-27",
              "dateModified": "2026-08-27",
              "image": f"{DOMEIN}/og-complete-ai.jpg",
              "url": f"{DOMEIN}/{p['bestand']}"}
             if p.get("soort") == "case" else
             {"@type": "Service",
              "@id": f"{DOMEIN}/{p['bestand']}#dienst",
              "name": p["dienst"],
              "description": p["omschrijving"],
              "serviceType": p["dienst"],
              "provider": {"@type": "Organization", "@id": f"{DOMEIN}/#organisatie",
                           "name": "Complete AI"},
              "areaServed": [{"@type": "Country", "name": "Nederland"},
                             {"@type": "Country", "name": "België"}],
              "url": f"{DOMEIN}/{p['bestand']}"})
    graaf = [
        hoofd,
        {"@type": "BreadcrumbList",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Complete AI", "item": f"{DOMEIN}/"},
             {"@type": "ListItem", "position": 2, "name": p["dienst"], "item": f"{DOMEIN}/{p['bestand']}"}]},
    ]
    if p.get("vragen"):
        graaf.append({"@type": "FAQPage", "@id": f"{DOMEIN}/{p['bestand']}#vragen",
                      "mainEntity": [{"@type": "Question", "name": v,
                                      "acceptedAnswer": {"@type": "Answer", "text": a}}
                                     for v, a in p["vragen"]]})
    return ('<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@graph": graaf},
                         ensure_ascii=False, indent=2) + '\n</script>')


def vragen_html(vragen):
    if not vragen:
        return ""
    items = "\n        ".join(
        f"<details><summary>{html.escape(v)}</summary><p>{a}</p></details>" for v, a in vragen)
    return f"""
  <hr class="streep">

  <section id="vragen">
    <div class="wrap">
      <div class="sectiekop reveal">
        <p class="label"><i></i>Veelgestelde vragen</p>
        <h2>Antwoord op de vragen die het vaakst gesteld worden.</h2>
      </div>
      <div class="vragen reveal">
        {items}
      </div>
    </div>
  </section>"""


def verder_html(pagina):
    huidig = pagina["bestand"]
    lijst = BRANCHE_VERDER if pagina.get("groep") == "branche" else VERDER
    kaarten = [k for k in lijst if k[0] != huidig]
    blokken = "\n        ".join(
        f'<a href="{h}"><em>{e}</em><b>{t}</b><span>{o}</span></a>' for h, e, t, o in kaarten)
    return f"""
  <hr class="streep">

  <section id="verder">
    <div class="wrap">
      <div class="sectiekop reveal">
        <p class="label"><i></i>Meer diensten</p>
        <h2>Gerelateerde diensten.</h2>
      </div>
      <div class="verder reveal">
        {blokken}
      </div>
    </div>
  </section>"""


VERDER = [
    ("websites.html", "Dienst", "Websites",
     "Een site die klanten oplevert, live binnen één tot twee weken."),
    ("automatisering.html", "Dienst", "Automatisering",
     "Facturen, orders en herinneringen zonder tussenkomst."),
    ("ai-telefonist.html", "Dienst", "AI-telefonist",
     "Neemt op wanneer u dat niet kunt: 's avonds, weekend, drukte."),
    ("social-media.html", "Dienst", "Social media",
     "Elke week zichtbaar, zonder dat het u tijd kost."),
    ("case-aronza.html", "Klantcase", "Aronza",
     "Vier tot zes uur administratie per week teruggebracht tot nul."),
    ("ai-voor-uw-bedrijf.html", "Gids", "AI voor uw bedrijf",
     "Welke taken AI vandaag echt kan overnemen — en waar de grens ligt."),
    ("index.html#diensten", "Homepage", "Alle diensten",
     "Ook vindbaarheid in Google en advertenties die renderen."),
]

# Branchepagina's wijzen naar elkaar en naar de twee diensten die daar
# het meest spelen; de volledige dienstenlijst staat in de voet.
BRANCHE_VERDER = [
    ("ai-voor-kapsalons.html", "Branche", "Kapsalons",
     "Afspraken, herinneringen en een telefoon die opneemt tijdens de behandeling."),
    ("ai-voor-garagebedrijven.html", "Branche", "Garagebedrijven",
     "APK-herinneringen, planning en statusberichten zonder handwerk."),
    ("ai-voor-de-horeca.html", "Branche", "Horeca",
     "Reserveringen en afhaalbestellingen, ook midden in de service."),
    ("ai-voor-bouw-en-installatie.html", "Branche", "Bouw &amp; installatie",
     "Aanvragen vastleggen tijdens het werk, offertes en facturen zonder avondwerk."),
    ("ai-telefonist.html", "Dienst", "AI-telefonist",
     "Het onderdeel dat in elke branche als eerste terugkomt."),
    ("social-media.html", "Dienst", "Social media",
     "Wekelijks zichtbaar in uw branche, zonder eigen tijd."),
]


def bouw(p):
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(p['titel'])}</title>
<meta name="description" content="{html.escape(p['beschrijving'])}">
<link rel="canonical" href="{DOMEIN}/{p['bestand']}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#06070C">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; script-src 'self' 'unsafe-inline'; form-action 'self' mailto:; frame-ancestors 'none'; base-uri 'self'; object-src 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">

<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="Complete AI">
<meta property="og:url" content="{DOMEIN}/{p['bestand']}">
<meta property="og:title" content="{html.escape(p['titel'])}">
<meta property="og:description" content="{html.escape(p['beschrijving'])}">
<meta property="og:image" content="{DOMEIN}/og-complete-ai.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">

<link rel="preload" href="archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="stijl.css?v={CSS_V}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<link rel="apple-touch-icon" sizes="180x180" href="/favicon-180.png">
<link rel="manifest" href="/site.webmanifest">

{schema(p)}
</head>
<body>

{kop_html(p['bestand'])}

<main>
  <div class="paginakop">
    <div class="wrap">
      <nav class="kruimels" aria-label="Kruimelpad">
        <a href="index.html">Complete AI</a><span>→</span><span>{p['dienst']}</span>
      </nav>
      <p class="label" style="margin-top:1.6rem"><i></i>{p['ogen']}</p>
      <h1>{p['h1']}</h1>
      <p class="lead">{p['lead']}</p>
      <div class="kop-acties">
        <a class="knop knop-vol" href="index.html#contact">Plan een gratis intake {PIJL}</a>
        <span class="kop-tijd">{KLOK}{p['levertijd']}</span>
      </div>
      <div class="uitkomsten reveal">
        {"".join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in p['uitkomsten'])}
      </div>
    </div>
  </div>

  <hr class="streep">

{p['inhoud']}
{vragen_html(p.get('vragen'))}

  <hr class="streep">

  <section id="afsluiting">
    <div class="wrap">
      <div class="slotblok reveal">
        <h2>{p['slot_kop']}</h2>
        <p>{p['slot_tekst']}</p>
        <a class="knop knop-vol" href="index.html#contact">Plan een gratis intake {PIJL}</a>
      </div>
    </div>
  </section>
{verder_html(p)}
</main>

{VOET}

<script src="script.js?v={JS_V}" defer></script>
</body>
</html>
"""


if __name__ == "__main__":
    from inhoud_paginas import PAGINAS
    hier = os.path.dirname(os.path.abspath(__file__))
    for p in PAGINAS:
        pad = os.path.join(hier, p["bestand"])
        with open(pad, "w", encoding="utf-8") as f:
            f.write(bouw(p))
        print(f"  {p['bestand']:24} {os.path.getsize(pad)//1024} kB")

    # index.html en privacy.html worden met de hand onderhouden; hun
    # verwijzingen naar stijl en script krijgen hier hetzelfde stempel.
    for hand in ("index.html", "privacy.html"):
        pad = os.path.join(hier, hand)
        if not os.path.exists(pad):
            continue
        with open(pad, encoding="utf-8") as f:
            t = f.read()
        nieuw_t = re.sub(r'stijl\.css(\?v=[0-9a-f]+)?', "stijl.css?v=" + CSS_V, t)
        nieuw_t = re.sub(r'script\.js(\?v=[0-9a-f]+)?', "script.js?v=" + JS_V, nieuw_t)
        if nieuw_t != t:
            with open(pad, "w", encoding="utf-8") as f:
                f.write(nieuw_t)
            print(f"  {hand:24} stempel bijgewerkt")
    print(f"  stempels: stijl.css?v={CSS_V} · script.js?v={JS_V}")
