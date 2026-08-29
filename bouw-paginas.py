#!/usr/bin/env python3
"""Genereert de dienstpagina's van Complete AI uit één sjabloon.

Kop, voet, navigatie en structuurdata staan hier één keer, zodat ze op
elke pagina identiek zijn. Inhoud per pagina staat onderaan in PAGINAS.
Draaien met:  python3 bouw-paginas.py
"""
import json, html, os

DOMEIN = "https://complete-ai.nl"

# Vestigingsplaats. Staat hier één keer; wordt gebruikt in de structuurdata,
# de voet en de lokale pagina, zodat de gegevens overal identiek zijn (NAP).
PLAATS = "Bergen op Zoom"
ADRES = {"@type": "PostalAddress",
         "addressLocality": PLAATS,
         "addressRegion": "Noord-Brabant",
         "addressCountry": "NL"}
WERKGEBIED = ["Bergen op Zoom", "Halsteren", "Steenbergen", "Roosendaal", "Woensdrecht",
              "Hoogerheide", "Tholen", "Oud-Gastel", "Rucphen", "Etten-Leur", "Breda"]

MERK_SVG = """<svg viewBox="0 0 32 32" aria-hidden="true">
        <defs><linearGradient id="{id}" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#3D6DFF"/><stop offset="1" stop-color="#25D8C4"/>
        </linearGradient></defs>
        <rect width="32" height="32" rx="8" fill="#0E1119" stroke="#28304a"/>
        <path d="M6 10h4M6 16h4M6 22h4" stroke="url(#{id})" stroke-width="2" stroke-linecap="round" opacity=".5"/>
        <path d="M12 16h14" stroke="url(#{id})" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="12" cy="16" r="2.5" fill="url(#{id})"/>
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
      {MERK_SVG.format(id='mg')}
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
      <li><a href="automatisering.html">Automatisering<span>Vaak binnen enkele werkdagen</span></a></li>
      <li><a href="ai-telefonist.html">AI-telefonist<span>Operationeel binnen 2 weken</span></a></li>
      <li><a href="social-media.html">Social media<span>Eerste bericht binnen een week</span></a></li>
    </ul>
    <p class="mm-kop">Voor uw branche</p>
    <ul class="mm-lijst">
      <li><a href="ai-voor-kapsalons.html">Kapsalons<span>Afspraken, no-shows en de telefoon</span></a></li>
      <li><a href="ai-voor-garagebedrijven.html">Garagebedrijven<span>APK, planning en statusberichten</span></a></li>
      <li><a href="ai-voor-de-horeca.html">Horeca<span>Reserveringen, ook midden in de service</span></a></li>
      <li><a href="ai-voor-bouw-en-installatie.html">Bouw &amp; installatie<span>Aanvragen, offertes en facturen</span></a></li>
      <li><a href="bergen-op-zoom.html">Bergen op Zoom &amp; regio<span>Hier komen wij langs voor de intake</span></a></li>
    </ul>
    <p class="mm-kop">Meer</p>
    <ul class="mm-lijst">
      <li><a href="index.html#pakketten">Pakketten<span>Stel zelf een pakket samen</span></a></li>
      <li><a href="index.html#over">Over Glenn<span>Wie u aan de lijn krijgt</span></a></li>
      <li><a href="case-aronza.html">Klantcase: Aronza<span>Vier tot zes uur per week naar nul</span></a></li>
      <li><a href="ai-voor-uw-bedrijf.html">Gids: AI voor uw bedrijf<span>Wat AI vandaag echt kan overnemen</span></a></li>
      <li><a href="index.html#vragen">Veelgestelde vragen<span>Kort en zonder omhaal beantwoord</span></a></li>
    </ul>
    <p class="mm-voet">glenn@complete-ai.nl · Bergen op Zoom</p>
  </div>
</header>"""


VOET = f"""<footer>
  <div class="wrap">
    <div class="voet">
      <div>
        <a class="merk" href="index.html" aria-label="Complete AI">
          {MERK_SVG.format(id='mg2')}
          <b>Complete<span> AI</span></b>
        </a>
        <p style="max-width:38ch">Websites, vindbaarheid, advertenties, automatisering en AI-telefonie voor ondernemers in Nederland en België. Gevestigd in Bergen op Zoom.</p>
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
        <p class="voetkop">Voor uw branche</p>
        <ul>
          <li><a href="ai-voor-kapsalons.html">Kapsalons</a></li>
          <li><a href="ai-voor-garagebedrijven.html">Garagebedrijven</a></li>
          <li><a href="ai-voor-de-horeca.html">Horeca</a></li>
          <li><a href="ai-voor-bouw-en-installatie.html">Bouw &amp; installatie</a></li>
          <li><a href="bergen-op-zoom.html">Bergen op Zoom &amp; regio</a></li>
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
      <span>Bergen op Zoom · Nederland &amp; België</span>
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
                           "name": "Complete AI", "address": ADRES},
              "areaServed": ([{"@type": "City", "name": n} for n in WERKGEBIED]
                             if p.get("soort") == "lokaal" else
                             [{"@type": "Country", "name": "Nederland"},
                              {"@type": "Country", "name": "België"}]),
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
    ("bergen-op-zoom.html", "Regio", "Bergen op Zoom",
     "Gevestigd in West-Brabant; hier komen wij langs voor de intake."),
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
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; script-src 'self' 'unsafe-inline'; form-action 'self' mailto:; frame-ancestors 'none'; base-uri 'self'; object-src 'none'">
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

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=DM+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="stijl.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='%233D6DFF'/%3E%3Cstop offset='1' stop-color='%2325D8C4'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='8' fill='%230A0C13'/%3E%3Cpath d='M6 10h4M6 16h4M6 22h4' stroke='url(%23g)' stroke-width='2' stroke-linecap='round' opacity='.55'/%3E%3Cpath d='M12 16h14' stroke='url(%23g)' stroke-width='2.5' stroke-linecap='round'/%3E%3Ccircle cx='12' cy='16' r='2.5' fill='url(%23g)'/%3E%3C/svg%3E">

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

<script src="script.js" defer></script>
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
