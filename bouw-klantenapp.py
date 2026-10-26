#!/usr/bin/env python3
"""Genereert klantenapp.html: de vindbare startpagina voor klanten van Complete AI.

Wie zoekt op "Complete AI klantenportaal" of "klantenapp" komt hier uit, en gaat
vandaar door naar de klantenapp (mijn.complete-ai.nl) of het klantportaal
(portaal.complete-ai.nl). Die twee inlogpagina's zelf staan niet in Google;
deze pagina wel.

Kop, voet en de beveiligingsregels in de <head> komen uit bouw-paginas.py, zodat
ze op elke pagina gelijk blijven. Draaien na bouw-paginas.py en vóór bouw-sitemap.py:

    python3 bouw-klantenapp.py
"""
import html
import importlib.util
import json
import os

HIER = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bouw_paginas", os.path.join(HIER, "bouw-paginas.py"))
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

BESTAND = "klantenapp.html"
URL = f"{bp.DOMEIN}/{BESTAND}"
KLANTENAPP = "https://mijn.complete-ai.nl"
PORTAAL = "https://portaal.complete-ai.nl"

TITEL = "Klantenapp en klantportaal: inloggen | Complete AI"
BESCHRIJVING = ("Inloggen op de klantenapp of het klantportaal van Complete AI. U leest hoe u inlogt, "
                "de klantenapp op uw telefoon zet en waar u hulp vindt.")

VRAGEN = [
    ("Ik heb geen uitnodiging ontvangen. Wat moet ik doen?",
     "Kijk eerst in uw map met ongewenste e-mail. Staat de uitnodiging daar ook niet, stuur dan een bericht naar "
     '<a href="mailto:glenn@complete-ai.nl">glenn@complete-ai.nl</a> met de naam van uw bedrijf. U ontvangt dan een nieuwe uitnodiging.'),
    ("Ik kan niet meer inloggen. Wat nu?",
     "In de klantenapp vraagt u op het inlogscherm een nieuwe code aan. Die komt per e-mail en is korte tijd geldig. "
     "Voor het klantportaal gebruikt u de uitnodigingslink uit uw e-mail opnieuw. Lukt het niet, "
     'mail dan naar <a href="mailto:glenn@complete-ai.nl">glenn@complete-ai.nl</a>.'),
    ("Is de klantenapp een app uit de App Store of Google Play?",
     "Nee. De klantenapp werkt in uw browser en u zet hem met één handeling op het beginscherm van uw telefoon of computer. "
     "Hoe dat gaat, leest u in het stuk over het beginscherm hierboven."),
    ("Zijn mijn gegevens veilig?",
     "Elke klant ziet alleen zijn eigen gegevens. Dat is in de database zelf vastgelegd en wordt getest. "
     "De gegevens staan op servers in Europa. In de klantenapp kunt u onder Instellingen extra beveiliging met een verificatiecode aanzetten."),
    ("Waarom heet de klantenapp Mijn Complete AI?",
     "Zo ziet u de naam op het inlogscherm en in uw browser. Na het inloggen ziet u uw eigen bedrijfsnaam, uw logo en uw kleuren."),
]


def kop():
    """De <head>, letterlijk uit de generator van de dienstpagina's, met eigen titel en adres."""
    bron = open(os.path.join(HIER, "bouw-paginas.py"), encoding="utf-8").read()
    start = bron.index("def bouw(p):")
    begin = bron.index("<!doctype html>", start)
    eind = bron.index("{schema(p)}", start)
    sjabloon = bron[begin:eind]
    waarden = {
        "{html.escape(p['titel'])}": html.escape(TITEL),
        "{html.escape(p['beschrijving'])}": html.escape(BESCHRIJVING),
        "{DOMEIN}/{p['bestand']}": URL,
        "{DOMEIN}": bp.DOMEIN,
        "{CSS_V}": bp.CSS_V,
    }
    for sleutel, waarde in waarden.items():
        sjabloon = sjabloon.replace(sleutel, waarde)
    assert "{" not in sjabloon.replace("{}", ""), "de kop van bouw-paginas.py heeft een onbekende plek erbij gekregen"
    return sjabloon


def structuurdata():
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{URL}#pagina",
                "url": URL,
                "name": TITEL,
                "description": BESCHRIJVING,
                "inLanguage": "nl-NL",
                "isPartOf": {"@id": f"{bp.DOMEIN}/#website"},
                "publisher": {"@type": "Organization", "@id": f"{bp.DOMEIN}/#organisatie", "name": "Complete AI"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Complete AI", "item": f"{bp.DOMEIN}/"},
                    {"@type": "ListItem", "position": 2, "name": "Klantenapp en klantportaal", "item": URL},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": v,
                     "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re_tags(a))}}
                    for v, a in VRAGEN
                ],
            },
        ],
    }
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>"


def re_tags(tekst):
    import re
    return re.sub(r"<[^>]+>", "", tekst)


def pagina():
    return f"""{kop()}{structuurdata()}
</head>
<body>

{bp.kop_html(BESTAND)}

<main>
  <div class="paginakop">
    <div class="wrap">
      <nav class="kruimels" aria-label="Kruimelpad">
        <a href="index.html">Complete AI</a><span>→</span><span>Klantenapp en klantportaal</span>
      </nav>
      <p class="label" style="margin-top:1.6rem"><i></i>Voor klanten van Complete AI</p>
      <h1>Inloggen op uw klantenapp of klantportaal</h1>
      <p class="lead">Dit is de startpagina voor klanten van Complete AI. Kies hieronder uw omgeving en log in.
      Heeft u nog geen toegang, dan ontvangt u die van ons per uitnodiging.</p>
    </div>
  </div>

  <hr class="streep">

  <section id="inloggen">
    <div class="wrap">
      <div class="sectiekop reveal">
        <p class="label"><i></i>Kies uw omgeving</p>
        <h2>Waar wilt u naartoe?</h2>
      </div>
      <div class="verder reveal">
        <a href="{KLANTENAPP}" rel="noopener"><em>Klantenapp</em><b>Mijn Complete AI</b><span>Uw dagelijkse werk op één plek, met de onderdelen die u bij ons afneemt, zoals klanten, offertes, werkbonnen, facturen en planning. U logt in met uw e-mailadres en een code die u per e-mail ontvangt.</span></a>
        <a href="{PORTAAL}" rel="noopener"><em>Klantportaal</em><b>De voortgang van uw project</b><span>Zie hoe uw project ervoor staat: de planning, wat wij van u nodig hebben, afspraken, documenten en updates. U logt in met uw eigen wachtwoord.</span></a>
      </div>
    </div>
  </section>

  <hr class="streep">

  <section id="verschil">
    <div class="wrap">
      <div class="sectiekop reveal">
        <p class="label"><i></i>Het verschil</p>
        <h2>Klantenapp of klantportaal?</h2>
      </div>
      <div class="proza reveal">
        <p>De <b>klantenapp</b> is uw werkomgeving. U gebruikt hem voor het werk van uw eigen bedrijf. Wat u erin ziet hangt af van wat u bij ons afneemt, bijvoorbeeld <a href="automatisering.html">automatisering</a> of de <a href="ai-telefonist.html">AI-telefonist</a>.</p>
        <p>Het <b>klantportaal</b> is uw inkijk in ons werk. U volgt daar hoe de bouw van uw website of app vordert en wat wij van u nodig hebben. Heeft u beide, dan logt u op twee plekken in. Dat is bewust gescheiden.</p>
      </div>
    </div>
  </section>

  <hr class="streep">

  <section id="eerste-keer">
    <div class="wrap">
      <div class="sectiekop reveal">
        <p class="label"><i></i>Uw eerste keer</p>
        <h2>Zo logt u voor het eerst in.</h2>
      </div>
      <div class="proza reveal">
        <ol>
          <li><b>Open de uitnodiging.</b> U ontvangt die van ons per e-mail of per bericht, met een persoonlijke link.</li>
          <li><b>Volg de link.</b> In de klantenapp vult u uw e-mailadres in en de code die u per e-mail krijgt. In het klantportaal kiest u zelf een wachtwoord.</li>
          <li><b>Klaar.</b> Een volgende keer gaat u rechtstreeks naar de klantenapp of het klantportaal hierboven.</li>
        </ol>
      </div>
    </div>
  </section>

  <hr class="streep">

  <section id="beginscherm">
    <div class="wrap">
      <div class="sectiekop reveal">
        <p class="label"><i></i>Op uw beginscherm</p>
        <h2>De klantenapp op uw telefoon of computer zetten.</h2>
      </div>
      <div class="proza reveal">
        <p>De klantenapp werkt in uw browser. U kunt hem als snelkoppeling op het beginscherm zetten, zodat hij opent als een gewone app.</p>
        <ul>
          <li><b>iPhone of iPad:</b> open de klantenapp in Safari, tik op de deelknop en kies Zet op beginscherm.</li>
          <li><b>Android:</b> open de klantenapp in Chrome, tik op het menu met de drie puntjes en kies App installeren of Toevoegen aan startscherm.</li>
          <li><b>Computer:</b> open de klantenapp in Chrome of Edge en klik in de adresbalk op het installatiesymbool.</li>
        </ul>
      </div>
    </div>
  </section>
{bp.vragen_html(VRAGEN)}

  <hr class="streep">

  <section id="afsluiting">
    <div class="wrap">
      <div class="slotblok reveal">
        <h2>Nog geen klant van Complete AI?</h2>
        <p>Wilt u ook een eigen klantenapp voor uw bedrijf? Bekijk onze <a href="pakketten.html">pakketten</a> of plan een gratis intake.</p>
        <a class="knop knop-vol" href="index.html#contact">Plan een gratis intake {bp.PIJL}</a>
      </div>
    </div>
  </section>
</main>

{bp.VOET}

<script src="script.js?v={bp.JS_V}" defer></script>
</body>
</html>
"""


if __name__ == "__main__":
    pad = os.path.join(HIER, BESTAND)
    with open(pad, "w", encoding="utf-8") as f:
        f.write(pagina())
    print(f"  {BESTAND:24} {os.path.getsize(pad)//1024} kB")
