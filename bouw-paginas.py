#!/usr/bin/env python3
"""Genereert de dienstpagina's van Complete AI uit één sjabloon.

Kop, voet, navigatie en structuurdata staan hier één keer, zodat ze op
elke pagina identiek zijn. Inhoud per pagina staat onderaan in PAGINAS.
Draaien met:  python3 bouw-paginas.py
"""
import json, html, os

DOMEIN = "https://complete-ai.nl"

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
    <a class="merk" href="index.html" aria-label="Complete AI, naar de homepage">
      {MERK_SVG.format(id='mg')}
      <b>Complete<span> AI</span></b>
    </a>
    <nav class="menu">{links}
    </nav>
    <a class="knop knop-vol" href="index.html#contact">Plan een nulmeting</a>
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
        <p style="max-width:38ch">Websites, vindbaarheid, advertenties, automatisering en AI-telefonie voor ondernemers in Nederland en België.</p>
      </div>
      <div>
        <h4>Diensten</h4>
        <ul>
          <li><a href="websites.html">Websites</a></li>
          <li><a href="index.html#diensten">Vindbaarheid — SEO</a></li>
          <li><a href="index.html#diensten">Adverteren — SEA</a></li>
          <li><a href="automatisering.html">Automatisering</a></li>
          <li><a href="ai-telefonist.html">AI-telefonist</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:glenn@complete-ai.nl">glenn@complete-ai.nl</a></li>
          <li><a href="index.html#contact">Plan een nulmeting</a></li>
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
    graaf = [
        {"@type": "Service",
         "@id": f"{DOMEIN}/{p['bestand']}#dienst",
         "name": p["dienst"],
         "description": p["omschrijving"],
         "serviceType": p["dienst"],
         "provider": {"@type": "Organization", "@id": f"{DOMEIN}/#organisatie", "name": "Complete AI"},
         "areaServed": [{"@type": "Country", "name": "Nederland"}, {"@type": "Country", "name": "België"}],
         "url": f"{DOMEIN}/{p['bestand']}"},
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
        <h2>Wat ondernemers hierover vragen.</h2>
      </div>
      <div class="vragen reveal">
        {items}
      </div>
    </div>
  </section>"""


def verder_html(huidig):
    kaarten = [k for k in VERDER if k[0] != huidig]
    blokken = "\n        ".join(
        f'<a href="{h}"><em>{e}</em><b>{t}</b><span>{o}</span></a>' for h, e, t, o in kaarten)
    return f"""
  <hr class="streep">

  <section id="verder">
    <div class="wrap">
      <div class="sectiekop reveal">
        <p class="label"><i></i>Verder kijken</p>
        <h2>Dit hangt er meestal mee samen.</h2>
      </div>
      <div class="verder reveal">
        {blokken}
      </div>
    </div>
  </section>"""


VERDER = [
    ("websites.html", "Dienst", "Websites",
     "Een site die klanten oplevert, live in één tot twee weken."),
    ("automatisering.html", "Dienst", "Automatisering",
     "Facturen, orders en herinneringen die vanzelf gaan."),
    ("ai-telefonist.html", "Dienst", "AI-telefonist",
     "Neemt op als jij niet kunt — 's avonds, weekend, drukte."),
    ("index.html#diensten", "Homepage", "Alles wat we doen",
     "Ook vindbaarheid in Google en advertenties die renderen."),
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
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='%233D6DFF'/%3E%3Cstop offset='1' stop-color='%2325D8C4'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='8' fill='%230A0C13'/%3E%3Cpath d='M6 10h4M6 16h4M6 22h4' stroke='url(%23g)' stroke-width='2' stroke-linecap='round' opacity='.55'/%3E%3Cpath d='M12 16h14' stroke='url(%23g)' stroke-width='2.5' stroke-linecap='round'/%3E%3Ccircle cx='12' cy='16' r='2.5' fill='url(%23g)'/%3E%3C/svg%3E">

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
        <a class="knop knop-vol" href="index.html#contact">Plan een gratis nulmeting {PIJL}</a>
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
        <a class="knop knop-vol" href="index.html#contact">Plan een gratis nulmeting {PIJL}</a>
      </div>
    </div>
  </section>
{verder_html(p['bestand'])}
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
