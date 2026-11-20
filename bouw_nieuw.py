#!/usr/bin/env python3
"""Bouwt de nieuwe pagina's van Complete AI (12-11-2026).

Kop, voet en onderdelen staan hier één keer. Draaien, in de map site/:
    python3 bouw-nieuw.py

Schrijft: index.html, oplossingen.html, werkwijze.html, resultaten.html,
scan.html en over-ons.html. De bestaande dienstpagina's en gidsen worden door
bouw-paginas.py gebouwd en gebruiken dezelfde kop en voet (zie KOP en VOET).

Regels uit de kluis die hier gelden:
  - formele u-vorm, korte zinnen, geen gedachtestreepjes;
  - nergens een bedrag of percentage van ons, en geen verzonnen getal;
  - geen klantnamen of -adressen: cases zijn zonder naam;
  - niet aanbieden: SEO, adverteren, social media;
  - geen plaats van vestiging als verkoopargument.
"""
import hashlib, html, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
DOMEIN = "https://complete-ai.nl"
TEL = "+31 6 24 56 96 86"
TEL_LINK = "+31624569686"
MAIL = "glenn@complete-ai.nl"


def stempel(bestand):
    with open(os.path.join(HIER, bestand), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


def schrijf_schil_css():
    """nieuw-schil.css: alleen kopbalk, knoppen en voet, met eigen bereik. De oude pagina's (diensten,
    gidsen) laden dit naast stijl.css, zodat zij dezelfde kop en voet krijgen zonder dat de rest verschuift.
    Bron is nieuw.css zelf, zodat er één plek is waar kop en voet worden aangepast."""
    c = open(os.path.join(HIER, "nieuw.css"), encoding="utf-8").read()
    tokens = re.search(r":root\{(.*?)\}", c, re.S).group(1)
    def stuk(van, tot):
        i = c.index(van)
        j = c.index(tot, i + len(van))
        return c[i:j]
    delen = [
        stuk(".n-sr{", ".n-wrap{"),
        stuk(".n-wrap{", ".n-glans{"),
        stuk("/* ── kopbalk ── */", "/* ── secties en koppen ── */"),
        stuk("/* ── voet ── */", "/* ═════════════ de tijdverlies-scan"),
        stuk("@media (max-width:1100px){", "@media (max-width:900px){"),
    ]
    bereik = ".n-balk,.n-mobiel,.n-waas,.n-voet,.n-skip"
    kop = ("/* Gegenereerd door bouw_nieuw.py uit nieuw.css. Niet met de hand aanpassen. */\n"
           '@font-face{font-family:"Archivo";font-style:normal;font-weight:400 700;font-display:swap;src:url("archivo.woff2") format("woff2")}\n'
           + bereik + "{" + tokens + "}\n"
           ".n-balk,.n-balk *,.n-voet,.n-voet *,.n-mobiel,.n-mobiel *,.n-skip{box-sizing:border-box}\n"
           ".n-balk,.n-voet{font-family:var(--f);font-size:17px;line-height:1.62;color:var(--inkt);text-align:left}\n"
           ".n-voet{background:none}\n"
           ".n-balk a,.n-voet a,.n-mobiel a{color:inherit}\n"
           ".n-balk ul,.n-voet ul,.n-mobiel ul{list-style:none;margin:0;padding:0}\n"
           ".n-balk p,.n-voet p,.n-mobiel p{margin:0}\n"
           ".n-balk svg,.n-voet svg{display:block;max-width:100%}\n"
           ".n-balk button{font:inherit;color:inherit}\n")
    with open(os.path.join(HIER, "nieuw-schil.css"), "w", encoding="utf-8") as f:
        f.write(kop + "".join(delen))


schrijf_schil_css()
CSS_V, JS_V, SCAN_V, SCHIL_V = stempel("nieuw.css"), stempel("nieuw.js"), stempel("scan.js"), stempel("nieuw-schil.css")

ICON = {
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "kruis": '<path d="M6 6l12 12M18 6L6 18"/>',
    "pijl": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "doc": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
    "kist": '<path d="M3.5 8L12 4l8.5 4v8L12 20l-8.5-4z"/><path d="M3.5 8L12 12l8.5-4M12 12v8"/>',
    "klant": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c0-3.9 3.1-7 7-7s7 3.1 7 7"/>',
    "tel": '<path d="M6.5 3.5h3l1.5 4-2 1.5a11 11 0 005.5 5.5L16 12.5l4 1.5v3a2 2 0 01-2 2A15 15 0 014.5 5.5a2 2 0 012-2z"/>',
    "chat": '<path d="M4 5.5h16v10.5H10l-5.5 4v-4H4z"/>',
    "factuur": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
    "portaal": '<rect x="3" y="4.5" width="18" height="15" rx="2.5"/><path d="M3 9.5h18M7 14.5h5"/>',
    "agenda": '<rect x="4" y="5" width="16" height="15" rx="2.5"/><path d="M8 3v4M16 3v4M4 10h16"/>',
    "web": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="M3.5 7.5l8.5 6 8.5-6"/>',
    "zoek": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    "waarsch": '<path d="M12 4l9 16H3z"/><path d="M12 10v4.5M12 17.5v.01"/>',
    "maan": '<path d="M20 14.5A8 8 0 019.5 4a8 8 0 1010.5 10.5z"/>',
    "klok": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "slot": '<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 018 0v2.5"/>',
    "koppel": '<path d="M9.5 14.5l5-5M8 11l-2 2a3.5 3.5 0 005 5l2-2M16 13l2-2a3.5 3.5 0 00-5-5l-2 2"/>',
    "oog": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "tijdlijn": '<circle cx="6" cy="6" r="2"/><circle cx="6" cy="18" r="2"/><path d="M6 8v8M10 6h9M10 18h9M10 12h6"/>',
}


def ic(naam, klasse=""):
    k = f' class="{klasse}"' if klasse else ""
    return (f'<svg{k} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[naam]}</svg>')


MERK_SVG = """<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="2.34" y="2.34" width="27.32" height="27.32" rx="8.8" fill="none" stroke="#2E7BFF" stroke-width="1.68"/><path d="M10.57 16L21.43 10.06M10.57 16L21.43 21.94M21.43 10.06V21.94" stroke="#2E7BFF" stroke-width="1.34" stroke-linecap="round" fill="none"/><circle cx="10.57" cy="16" r="2.58" fill="#6FA2FF"/><circle cx="21.43" cy="10.06" r="2.58" fill="#6FA2FF"/><circle cx="21.43" cy="21.94" r="2.58" fill="#6FA2FF"/></svg>"""

NAV = [("oplossingen.html", "Oplossingen"),
       ("werkwijze.html", "Werkwijze"),
       ("resultaten.html", "Resultaten"),
       ("scan.html", "Tijdverlies-scan"),
       ("over-ons.html", "Over ons"),
       ("index.html#contact", "Contact")]

LADE = [("oplossingen.html", "Oplossingen", "Wat wij automatiseren"),
        ("werkwijze.html", "Werkwijze", "Van kennismaking tot live"),
        ("resultaten.html", "Resultaten", "Wat wij voor vakbedrijven bouwden"),
        ("scan.html", "Tijdverlies-scan", "Gratis, direct een uitslag"),
        ("ai-telefonist.html", "AI-telefonist", "Neemt op wanneer u dat niet kunt"),
        ("whatsapp-automatisering.html", "WhatsApp", "Berichten die zichzelf afhandelen"),
        ("websites.html", "Websites", "Live in één tot twee weken"),
        ("over-ons.html", "Over ons", "Wie u aan de lijn krijgt")]


def kop(actief=""):
    huidig = ' aria-current="page"'
    links = "".join(
        f'\n      <a href="{h}"{huidig if h == actief else ""}>{t}</a>' for h, t in NAV)
    lade = "".join(f'<li><a href="{h}">{t}<span>{o}</span></a></li>' for h, t, o in LADE)
    return f"""<a class="n-skip" href="#inhoud">Naar de inhoud</a>
<header class="n-balk" id="balk">
  <div class="n-wrap">
    <a class="n-merk" href="index.html" aria-label="Complete AI, naar de startpagina">{MERK_SVG}<b>Complete<span> AI</span></b></a>
    <nav class="n-menu" aria-label="Hoofdmenu">{links}
    </nav>
    <a class="n-knop n-knop-vol n-knop-klein" href="index.html#contact">Plan een kennismaking</a>
    <button type="button" class="n-menuknop" id="menuknop" aria-expanded="false" aria-controls="mobielmenu" aria-label="Menu openen"><span></span><span></span><span></span></button>
  </div>
  <div class="n-waas" id="mobielwaas"></div>
  <div class="n-mobiel" id="mobielmenu">
    <a class="n-knop n-knop-vol" href="index.html#contact">Plan een kennismaking</a>
    <ul>{lade}</ul>
    <p class="n-klein">{MAIL} · {TEL}</p>
  </div>
</header>"""


VOET = f"""<footer class="n-voet">
  <div class="n-wrap">
    <div class="n-voetraster">
      <div>
        <a class="n-merk" href="index.html" aria-label="Complete AI">{MERK_SVG}<b>Complete<span> AI</span></b></a>
        <p class="n-over-ons">Automatisering van administratie en klantcontact, een AI-telefonist en websites voor bedrijven in Nederland en Vlaanderen. Eén vast aanspreekpunt.</p>
      </div>
      <div>
        <p class="n-voetkop">Oplossingen</p>
        <ul>
          <li><a href="oplossingen.html">Alle oplossingen</a></li>
          <li><a href="ai-telefonist.html">AI-telefonist</a></li>
          <li><a href="whatsapp-automatisering.html">WhatsApp-automatisering</a></li>
          <li><a href="automatisering.html">Automatisering</a></li>
          <li><a href="websites.html">Websites</a></li>
          <li><a href="pakketten.html">Pakket samenstellen</a></li>
        </ul>
      </div>
      <div>
        <p class="n-voetkop">Over Complete AI</p>
        <ul>
          <li><a href="werkwijze.html">Werkwijze</a></li>
          <li><a href="resultaten.html">Resultaten</a></li>
          <li><a href="scan.html">Tijdverlies-scan</a></li>
          <li><a href="over-ons.html">Over ons</a></li>
          <li><a href="gidsen.html">Gidsen en tools</a></li>
        </ul>
      </div>
      <div>
        <p class="n-voetkop">Contact</p>
        <ul>
          <li><a href="mailto:{MAIL}">{MAIL}</a></li>
          <li><a href="tel:{TEL_LINK}">{TEL}</a></li>
          <li><a href="index.html#contact">Plan een kennismaking</a></li>
          <li><a href="klantenapp.html">Inloggen klantenapp</a></li>
          <li><a href="index.html#vragen">Veelgestelde vragen</a></li>
        </ul>
      </div>
    </div>
    <!-- VERVANG: btw-nummer toevoegen zodra dat bekend is. KvK staat er sinds 31-8-2026. -->
    <div class="n-slot">
      <span>&copy; <span id="jaar">2026</span> Complete AI</span>
      <span>KvK 98445235</span>
      <span>Nederland &amp; Vlaanderen</span>
      <a href="privacy.html">Privacyverklaring</a>
      <a href="voorwaarden.html">Algemene voorwaarden</a>
      <a href="gegevens-verwijderen.html">Gegevens verwijderen</a>
    </div>
  </div>
</footer>"""

CSP = ("default-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; "
       "script-src 'self'; form-action 'self' https://formsubmit.co; "
       "connect-src 'self' https://formsubmit.co https://complete-ai-production.up.railway.app; "
       "base-uri 'self'; object-src 'none'")


def pagina(bestand, titel, omschrijving, actief, inhoud, extra_js="", schema=None, og_titel=None, robots="index, follow"):
    pad = "" if bestand == "index.html" else bestand
    url = f"{DOMEIN}/{pad}"
    sch = ""
    if schema:
        sch = '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=1) + "\n</script>\n"
    js = f'<script src="scan.js?v={SCAN_V}" defer></script>\n' if extra_js == "scan" else ""
    t = html.escape(titel, quote=True)
    o = html.escape(omschrijving, quote=True)
    ot = html.escape(og_titel or titel, quote=True)
    doc = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{o}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#06070C">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="Complete AI">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{ot}">
<meta property="og:description" content="{o}">
<meta property="og:image" content="{DOMEIN}/og-complete-ai.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/favicon-180.png">
<link rel="manifest" href="/site.webmanifest">
{sch}<link rel="stylesheet" href="nieuw.css?v={CSS_V}">
<script src="nieuw.js?v={JS_V}" defer></script>
{js}</head>
<body>
{kop(actief)}
<main id="inhoud">
{inhoud}
</main>
{VOET}
</body>
</html>
"""
    with open(os.path.join(HIER, bestand), "w", encoding="utf-8") as f:
        f.write(doc)
    print("  geschreven:", bestand)


# ── herbruikbare onderdelen ───────────────────────────────────────────────

def sectiekop(boven, h2, p=""):
    pp = f"<p>{p}</p>" if p else ""
    return f'<div class="n-kop"><span class="n-boven">{boven}</span><h2>{h2}</h2>{pp}</div>'


def kaart(icoon, titel, tekst, link=None, linktekst="Meer lezen", sectie_id=""):
    i = f' id="{sectie_id}"' if sectie_id else ""
    if link:
        return (f'<a class="n-kaart" href="{link}"{i}><span class="n-ico">{ic(icoon)}</span><h3>{titel}</h3><p>{tekst}</p>'
                f'<span class="n-meer">{linktekst}{ic("pijl")}</span></a>')
    return f'<div class="n-kaart"{i}><span class="n-ico">{ic(icoon)}</span><h3>{titel}</h3><p>{tekst}</p></div>'


def lijst(items):
    return '<ul class="n-lijst">' + "".join(f"<li>{ic('check')}<span>{x}</span></li>" for x in items) + "</ul>"


def oproep(titel="Zullen we een keer kennismaken?", tekst=None, extra_knop=True):
    tekst = tekst or ("Wij kijken samen hoe het werk nu loopt en waar tijd verloren gaat. "
                      "Daarna weet u of automatisering iets is voor uw bedrijf. Ook als dat niet zo is.")
    knop2 = ('<a class="n-knop n-knop-lijn" href="scan.html">Doe de gratis tijdverlies-scan</a>') if extra_knop else ""
    return f"""<section class="n-sec"><div class="n-wrap"><div class="n-oproep">
  <div class="n-streep"></div>
  <h2>{titel}</h2>
  <p>{tekst}</p>
  <div class="n-acties"><a class="n-knop n-knop-vol" href="index.html#contact">Plan een kennismaking</a>{knop2}</div>
</div></div></section>"""


def paginakop(boven, h1, lead, acties=""):
    return f"""<section class="n-pagina"><div class="n-wrap">
  <span class="n-boven">{boven}</span>
  <h1>{h1}</h1>
  <p class="n-lead">{lead}</p>
  {acties}
</div></section>"""


def mock(titel, onder, badge, binnen, noot=""):
    n = f'<p class="n-voetnoot">{noot}</p>' if noot else ""
    return (f'<div class="n-mock"><div class="n-mock-kop"><div><b>{titel}</b><small>{onder}</small></div>'
            f'<span class="n-badge">{badge}</span></div>{binnen}{n}</div>')


def regels(rijen, totaal=None):
    x = "".join(f"<li><span>{a}</span><span>{b}</span></li>" for a, b in rijen)
    if totaal:
        x += f'<li class="n-totaal"><span>{totaal[0]}</span><span>{totaal[1]}</span></li>'
    return f'<ul class="n-regels">{x}</ul>'


FORMULIER = f"""<form class="n-form" id="contactformulier" data-verzend data-onderwerp="Kennismaking aanvragen" novalidate>
  <input type="text" name="_honey" class="n-honing" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="n-rij">
    <label>Naam<input type="text" name="naam" autocomplete="name" required></label>
    <label>Bedrijfsnaam<input type="text" name="bedrijf" autocomplete="organization" required></label>
  </div>
  <div class="n-rij">
    <label>Telefoonnummer<input type="tel" name="telefoon" autocomplete="tel" required></label>
    <label>E-mail (optioneel)<input type="email" name="email" autocomplete="email"></label>
  </div>
  <label>Waar loopt u tegenaan? (optioneel)
    <textarea name="bericht" placeholder="Bijvoorbeeld: offertes maken kost te veel avonden, of de telefoon gaat als niemand kan opnemen."></textarea>
  </label>
  <button class="n-knop n-knop-vol" type="submit">Plan een kennismaking</button>
  <p class="n-stand" role="status" hidden></p>
  <p class="n-of">Of doe eerst de <a href="scan.html">gratis tijdverlies-scan</a></p>
  <p class="n-klein">Uw gegevens gebruiken wij alleen om contact op te nemen. Nooit doorverkocht, en nooit voor nieuwsbrieven zonder uw uitdrukkelijke toestemming.</p>
</form>"""


def contactblok():
    return f"""<section class="n-sec" id="contact"><div class="n-wrap"><div class="n-contact">
  <div class="n-contact-tekst">
    <span class="n-boven">Contact</span>
    <h2>Ontdek eerst waar uw team tijd verliest</h2>
    <p>Laat uw gegevens achter. Wij bellen u binnen één werkdag terug en plannen een kennismaking, per videogesprek of bij u op locatie.</p>
    <div class="n-gegevens">
      <a href="tel:{TEL_LINK}">{ic('tel')}{TEL}</a>
      <a href="mailto:{MAIL}">{ic('mail')}{MAIL}</a>
    </div>
  </div>
  <div class="n-formkaart">{FORMULIER}</div>
</div></div></section>"""


VRAGEN = [
    ("Moeten wij onze huidige software vervangen?",
     "<p>Nee. De assistent werkt bovenop wat u nu gebruikt. Waar uw systeem het toelaat, koppelen wij direct. Anders automatiseren wij de stappen eromheen.</p>"
     "<p>Wilt u liever alles in één systeem? Dat kan ook, in onze eigen klantenapp.</p>"),
    ("Kost het niet veel tijd en moeite om dit in te voeren?",
     "<p>Wij bouwen en richten in. U levert gegevens aan via een vragenlijst in uw eigen portaal en kijkt het resultaat na. Wij bouwen in fasen, zodat er gaandeweg iets staat.</p>"
     "<p>Een website staat binnen één tot twee weken live, automatiseringen binnen enkele werkdagen en de AI-telefonist binnen twee weken.</p>"),
    ("Hoeveel tijd kan mijn bedrijf besparen?",
     "<p>Dat verschilt per bedrijf. Wij noemen vooraf geen percentage, want dat zou een gok zijn.</p>"
     "<p>In de intake vult u zelf in hoe vaak een taak voorkomt en hoeveel minuten die kost. Na dertig dagen meten wij opnieuw met dezelfde getallen. Wilt u nu al een eerste beeld? Doe de <a href=\"scan.html\">tijdverlies-scan</a>.</p>"),
    ("Wat als mijn medewerkers niet technisch zijn?",
     "<p>Daar bouwen wij voor. Uw medewerkers werken in een overzichtelijk scherm en doen vooral één ding: nakijken en goedkeuren. Wij leggen het uit aan iedereen die ermee werkt.</p>"),
    ("Wat kost het om onze processen te automatiseren?",
     "<p>Dat hangt af van wat u kiest. Wij noemen geen bedragen voordat wij uw situatie kennen. Na de kennismaking krijgt u een offerte met vaste bedragen, zonder verrassingen. De looptijd staat vooraf in die offerte.</p>"),
    ("Wat als de AI-telefonist iets verkeerd doet?",
     "<p>U bepaalt vooraf wat hij zelfstandig afhandelt en wat altijd naar u wordt doorgeschakeld. Van elk gesprek is een transcript terug te lezen, en de eerste weken kijken wij mee en sturen wij bij.</p>"),
    ("Hoe is de gegevensbeveiliging geregeld, en hoe zit het met de AVG?",
     "<p>Uw gegevens blijven van u. Waar wij persoonsgegevens verwerken, bijvoorbeeld bij telefoongesprekken, leggen wij dat vóór de start vast in een verwerkersovereenkomst, zoals de AVG voorschrijft.</p>"),
]


def vragenblok(kop_tekst="Veelgestelde vragen", intro=""):
    items = "".join(
        f'<details class="n-vraag"><summary>{q}</summary><div class="n-antwoord">{a}</div></details>' for q, a in VRAGEN)
    return f"""<section class="n-sec" id="vragen"><div class="n-wrap">
{sectiekop("Vragen", kop_tekst, intro)}
<div class="n-vragen">{items}</div>
</div></section>"""


def faq_schema():
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a.replace("</p><p>", " "))}}
        for q, a in VRAGEN]}


ORGANISATIE = {
    "@type": ["Organization", "ProfessionalService"], "@id": f"{DOMEIN}/#organisatie",
    "name": "Complete AI", "url": f"{DOMEIN}/", "logo": f"{DOMEIN}/favicon-512.png",
    "image": f"{DOMEIN}/og-complete-ai.jpg", "email": MAIL, "telephone": TEL_LINK,
    "identifier": {"@type": "PropertyValue", "propertyID": "KvK", "value": "98445235"},
    "founder": {"@type": "Person", "name": "Glenn van Wijngaarden"},
    "areaServed": [{"@type": "Country", "name": "Nederland"}, {"@type": "Country", "name": "België"}],
    "description": "Automatisering van administratie en klantcontact, een AI-telefonist en websites voor bedrijven in Nederland en Vlaanderen."}


# ═════════════════════════ STARTPAGINA ═════════════════════════

def startpagina():
    hero_mock = mock("Conceptofferte klaargezet", "Aanvraag 1047 · cv-ketel vervangen", "Klaar ter controle",
        '<ul class="n-stap-rij">'
        f'<li>{ic("check")}Aanvraag uit de mail uitgelezen</li>'
        f'<li>{ic("check")}Calculatie gemaakt met uw prijzen</li>'
        f'<li>{ic("check")}Materiaallijst klaargezet</li>'
        f'<li class="n-nu">{ic("oog")}U kijkt na en verstuurt</li></ul>',
        "Voorbeeld met verzonnen gegevens.")

    hero = f"""<section class="n-hero"><div class="n-wrap">
  <div class="n-hero-tekst">
    <span class="n-boven">Voor installatie-, bouw- en metaalbedrijven</span>
    <h1>Laat het terugkerende kantoorwerk <span class="n-glans">zichzelf doen</span></h1>
    <p class="n-lead">Complete AI bouwt automatisering voor bedrijven: assistenten die offertes klaarzetten, de administratie bijwerken en de telefoon en WhatsApp opvangen. U controleert. Wij zorgen dat het draait.</p>
    <div class="n-acties">
      <a class="n-knop n-knop-vol" href="#contact">Plan een kennismaking</a>
      <a class="n-knop n-knop-lijn" href="scan.html">Doe de gratis tijdverlies-scan</a>
    </div>
    <ul class="n-vink">
      <li>{ic('check')}Werkt bovenop uw huidige systemen</li>
      <li>{ic('check')}U keurt alles goed voordat het de deur uitgaat</li>
      <li>{ic('check')}Eén vast aanspreekpunt</li>
    </ul>
  </div>
  <div class="n-hero-beeld">{hero_mock}</div>
</div></section>"""

    verlies = [
        ("doc", "Offertes overtypen", "Een aanvraag komt binnen. Daarna rekent en typt iemand uren en materiaal over, terwijl de klant wacht."),
        ("zoek", "Zoeken naar informatie", "Mails, appjes en notities staan op verschillende plekken. Eerst zoeken, dan pas beginnen."),
        ("waarsch", "Fouten en herstelwerk", "Materiaal vergeten, een verkeerd bedrag of een afspraak die niet is doorgegeven. De monteur moet terug."),
        ("tel", "Gemiste oproepen", "Wie op een dak of onder een ketel staat, neemt niet op. De klant belt de volgende."),
        ("factuur", "Facturen die blijven liggen", "Een werkbon wordt pas dagen later een factuur en een betaalherinnering wordt vergeten."),
        ("maan", "Avondwerk", "Wat overdag blijft liggen, doet de eigenaar 's avonds of in het weekend."),
    ]
    probleem = f"""<section class="n-sec n-verlies" id="probleem"><div class="n-wrap">
{sectiekop("Het probleem", "Uw team verliest elke dag tijd aan werk dat niets oplevert",
 "Aan overtypen, zoeken en nabellen. Daardoor blijft er minder tijd over voor de klus zelf, terwijl nieuw personeel moeilijk te vinden is.")}
<div class="n-raster n-drie">{"".join(kaart(i, t, x) for i, t, x in verlies)}</div>
</div></section>"""

    over = f"""<section class="n-sec" id="over-ons"><div class="n-wrap"><div class="n-over">
  <div class="n-over-beeld"><img src="glenn-880.jpg" srcset="glenn-440.webp 440w, glenn-880.webp 880w" sizes="(max-width:900px) 340px, 380px" width="880" height="1100" alt="Glenn van Wijngaarden, oprichter van Complete AI" loading="lazy"></div>
  <div class="n-over-tekst">
    <span class="n-boven">Over Complete AI</span>
    <h2>Wij nemen het terugkerende werk over. U houdt de controle.</h2>
    <p>Een AI-medewerker is software die een vaste taak uitvoert, net als een collega. Hij werkt bovenop uw huidige systemen, maakt geen pauze en wordt door u of uw team gecontroleerd.</p>
    <p>Wij beginnen bij werk dat elke week terugkomt, een vaste volgorde heeft en een uitkomst geeft die u kunt nakijken. De klantenapp die wij daarvoor bouwen is in gebruik bij een metaalbedrijf en wordt ingericht voor een installatiebedrijf.</p>
    <div class="n-acties"><a class="n-knop n-knop-lijn" href="over-ons.html">Lees meer over ons</a></div>
  </div>
</div></div></section>"""

    flag_a = f"""<div class="n-oplossing" id="offertes">
  <div class="n-oplossing-tekst">
    <span class="n-nr">01 · Offertes</span>
    <h3>Van aanvraag naar offerte, zonder overtypen</h3>
    <p class="n-t">De assistent leest de aanvraag uit, rekent met uw eigen prijzen en zet een conceptofferte klaar. U kijkt na en verstuurt.</p>
    <div class="n-nunu">
      <div><small>Nu</small><p>Aanvragen overtypen en rekenen, terwijl de klant wacht</p></div>
      <div class="n-met"><small>Met Complete AI</small><p>De offerte staat klaar, u controleert en verstuurt</p></div>
    </div>
  </div>
  <div class="n-oplossing-beeld">{mock("Conceptofferte", "Aanvraag 1047 · cv-ketel vervangen", "Klaar ter controle",
      regels([("Cv-ketel vervangen", "1 stuk"), ("Leidingwerk en montage", "6 uur"), ("Materiaal", "12 regels")], ("Totaal excl. btw", "berekend")),
      "Voorbeeld met verzonnen gegevens.")}</div>
</div>"""
    flag_b = f"""<div class="n-oplossing n-om" id="materiaal">
  <div class="n-oplossing-tekst">
    <span class="n-nr">02 · Materiaal</span>
    <h3>Het juiste materiaal mee naar de klus</h3>
    <p class="n-t">Uit de offerte stelt de assistent een materiaallijst op, per leverancier gegroepeerd. U keurt goed, daarna gaat de bestelling als mail naar de leverancier.</p>
    <div class="n-nunu">
      <div><small>Nu</small><p>Materiaal vergeten, de monteur moet terug</p></div>
      <div class="n-met"><small>Met Complete AI</small><p>De lijst komt rechtstreeks uit de offerte</p></div>
    </div>
  </div>
  <div class="n-oplossing-beeld">{mock("Materiaallijst", "Project 1047 · 12 regels uit de offerte", "Ter goedkeuring",
      regels([("Ketel", "1x"), ("Rookgasafvoer", "1x"), ("Koperleiding", "15 m"), ("Montagebeugels", "4x"), ("En 8 regels meer", "")]),
      "Voorbeeld met verzonnen gegevens.")}</div>
</div>"""
    flag_c = f"""<div class="n-oplossing" id="dossier">
  <div class="n-oplossing-tekst">
    <span class="n-nr">03 · Klantdossier</span>
    <h3>Alles over een klant op één plek</h3>
    <p class="n-t">Mails, WhatsApp-berichten, telefoontjes, notities en werkbonnen komen per klant samen op één tijdlijn. Uw werkvoorbereider hoeft niet meer te zoeken of te bellen voordat hij kan beginnen.</p>
    <div class="n-nunu">
      <div><small>Nu</small><p>Informatie in mailboxen, appjes en het hoofd van de eigenaar</p></div>
      <div class="n-met"><small>Met Complete AI</small><p>Eén plek per klant, voor het hele team</p></div>
    </div>
  </div>
  <div class="n-oplossing-beeld">{mock("Voorbeeldklant", "Alles van deze week", "Op één plek",
      regels([("Mail: vraag over de planning", "ma"), ("WhatsApp: foto van de meterkast", "di"), ("Telefoon: terugbelverzoek", "di"), ("Werkbon: monteur klaar", "wo")]),
      "Voorbeeld met verzonnen gegevens.")}</div>
</div>"""

    meer = [
        ("tel", "AI-telefonist", "Neemt op wanneer u dat niet kunt, legt de aanvraag vast en plant een afspraak in.", "ai-telefonist.html", "Over de AI-telefonist"),
        ("chat", "WhatsApp-assistent", "Beantwoordt de vragen die steeds terugkomen, houdt berichten bij en zet door naar u.", "whatsapp-automatisering.html", "Over WhatsApp"),
        ("factuur", "Facturen en herinneringen", "Van werkbon naar factuur met controle op de wettelijke regels. Herinneringen staan op de juiste dag klaar.", "oplossingen.html#administratie", "Over facturatie"),
        ("portaal", "Klantportaal", "Uw klanten loggen in en zien hun eigen offerte, afspraak en dossier.", "oplossingen.html#overzicht", "Over het klantportaal"),
        ("agenda", "Agenda en afspraken", "Na het tekenen kiest de klant zelf een vrij moment uit uw agenda, in Outlook of Google.", "oplossingen.html#planning", "Over planning"),
        ("web", "Website op maat", "Een website die past bij uw bedrijf, live binnen één tot twee weken.", "websites.html", "Over websites"),
    ]
    oplossingen = f"""<section class="n-sec" id="oplossingen"><div class="n-wrap">
{sectiekop("Oplossingen", "Laat AI het terugkerende werk overnemen", "Per onderdeel apart of samen. U begint waar de winst het grootst is.")}
{flag_a}{flag_b}{flag_c}
<div style="height:clamp(36px,5vw,64px)"></div>
{sectiekop("Meer oplossingen", "Wat wij nog meer voor u regelen")}
<div class="n-raster n-drie">{"".join(kaart(i, t, x, l, lt) for i, t, x, l, lt in meer)}</div>
<div class="n-acties" style="justify-content:center;margin-top:40px"><a class="n-knop n-knop-lijn" href="oplossingen.html">Bekijk alle oplossingen</a></div>
</div></section>"""

    stappen = [
        ("01", "Kennismaking en intake", "Wij lopen uw werkdag door en meten wat tijd kost. Alleen uw eigen getallen, geen aannames van ons."),
        ("02", "Inrichten met uw eigen gegevens", "Uw prijzen, klanten en oude offertes gaan erin. U vult een vragenlijst in uw eigen portaal in."),
        ("03", "Proefdraaien op uw oude aanvragen", "Wij testen eerst op uw eigen oude aanvragen. U ziet per regel wat wij anders rekenen dan u. Alleen wat klopt gaat live."),
        ("04", "Live en meekijken", "Wij begeleiden de start, kijken de eerste weken mee en sturen bij. Na dertig dagen meten wij opnieuw."),
    ]
    werkwijze = f"""<section class="n-sec" id="werkwijze"><div class="n-wrap">
{sectiekop("Werkwijze", "Zo maken wij uw bedrijf efficiënter", "Vier stappen. Elke stap levert iets op dat u kunt zien.")}
<div class="n-raster n-vier">{"".join(f'<div class="n-kaart"><span class="n-nr">{n}</span><h3>{t}</h3><p>{x}</p></div>' for n, t, x in stappen)}</div>
<div class="n-acties" style="justify-content:center;margin-top:40px"><a class="n-knop n-knop-lijn" href="werkwijze.html">Bekijk de volledige werkwijze</a></div>
</div></section>"""

    zonder = ["Kostbare capaciteit blijft verloren gaan.", "De werkdruk blijft onnodig hoog en het werkplezier neemt af.",
              "Opdrachten gaan naar de concurrent die sneller een offerte stuurt.", "Fouten en herstelwerk blijven tijd en geld kosten.",
              "U blijft te veel tijd kwijt aan de dagelijkse bedrijfsvoering."]
    met = ["Meer capaciteit uit uw huidige team.", "Minder werkdruk en meer werkplezier voor uw medewerkers.",
           "Ruimte om meer werk aan te nemen zonder extra personeel.", "Minder fouten en minder herstelwerk.",
           "Meer rust en overzicht in uw bedrijfsvoering."]
    uls = lambda lst, i: "<ul>" + "".join(f"<li>{ic(i)}<span>{x}</span></li>" for x in lst) + "</ul>"
    resultaat = f"""<section class="n-sec n-vergelijk" id="resultaat"><div class="n-wrap">
{sectiekop("Het verschil", "Wat slimmere processen uw bedrijf opleveren")}
<div class="n-raster n-twee">
  <div class="n-kaart n-zonder"><h3>Zonder verandering</h3>{uls(zonder, "kruis")}</div>
  <div class="n-kaart n-met-kaart"><h3>Met Complete AI</h3>{uls(met, "check")}</div>
</div>
</div></section>"""

    cases = f"""<section class="n-sec" id="resultaten"><div class="n-wrap">
{sectiekop("Uit de praktijk", "Wat wij voor vakbedrijven bouwden", "Twee bedrijven, twee soorten werk. Wat er voor hen is ingericht, leest u hier.")}
<div class="n-raster n-twee">
  <div class="n-kaart n-case"><span class="n-tag">Installatiebedrijf</span><h3>Van offerte tot factuur, voor zonnepanelen, warmtepompen en laadpalen</h3>
    <p>Een klantenapp met dertien onderdelen, een prijsboek uit de oude offertes en een klantportaal voor de klanten van het bedrijf.</p>
    <a class="n-meer" href="resultaten.html#installatie">Bekijk wat er gebouwd is{ic('pijl')}</a></div>
  <div class="n-kaart n-case"><span class="n-tag">Metaalbedrijf</span><h3>Maatwerk in staal, rvs en aluminium, met vaste opmaak</h3>
    <p>Offertes en facturen in de eigen huisstijl, de Belgische factuurregels afgedwongen en de bestaande facturen overgenomen.</p>
    <a class="n-meer" href="resultaten.html#metaal">Bekijk wat er gebouwd is{ic('pijl')}</a></div>
</div>
</div></section>"""

    scan = f"""<section class="n-sec n-sec-kort"><div class="n-wrap"><div class="n-oproep">
  <div class="n-streep"></div>
  <h2>Hoeveel uur kost het kantoorwerk u per week?</h2>
  <p>Acht korte vragen. U ziet direct waar de tijd blijft, wat uw grootste tijdvreter is en wat u er het eerst aan doet.</p>
  <div class="n-acties"><a class="n-knop n-knop-vol" href="scan.html">Doe de gratis tijdverlies-scan</a></div>
  <p class="n-klein" style="margin-top:14px">Ongeveer twee minuten. Uw antwoorden blijven op uw eigen apparaat.</p>
</div></div></section>"""

    langs = oproep("Zullen we een keer kennismaken?")

    inhoud = hero + probleem + over + oplossingen + werkwijze + resultaat + cases + scan + contactblok() + vragenblok("Antwoord op de vragen die u nu heeft") + langs
    schema = {"@context": "https://schema.org", "@graph": [
        ORGANISATIE,
        {"@type": "WebSite", "@id": f"{DOMEIN}/#website", "url": f"{DOMEIN}/", "name": "Complete AI", "inLanguage": "nl-NL", "publisher": {"@id": f"{DOMEIN}/#organisatie"}},
        faq_schema()]}
    pagina("index.html", "Automatisering voor bedrijven en AI-telefonist | Complete AI",
           "Automatisering voor vakbedrijven: offertes die klaarstaan, administratie die zichzelf bijwerkt en een AI-telefonist die opneemt. Doe de gratis tijdverlies-scan.",
           "", inhoud, schema=schema)


# ═════════════════════════ OPLOSSINGEN ═════════════════════════

def oplossingenpagina():
    groepen = [
        ("offertes", "Aanvragen en offertes", "Van de eerste aanvraag tot een getekende offerte.", [
            ("zoek", "Aanvragen vastgelegd", "Een aanvraag per mail, formulier of telefoon wordt direct een lead met alle gegevens. Er valt niets tussendoor."),
            ("doc", "Calculatie met uw eigen prijzen", "Uw prijzen en oude offertes vormen een prijsboek. Daarmee rekent de assistent materiaal en uren door, zoals u dat zelf zou doen."),
            ("pijl", "Offertes die zichzelf opvolgen", "De offerte gaat met één klik de deur uit, met uw bijlagen en betaalschema. De klant tekent online en de opvolging staat op de juiste dag klaar.")]),
        ("planning", "Planning en uitvoering", "Wat er moet gebeuren, wie waar is en wat er klaarligt.", [
            ("agenda", "Klusplanning en agenda", "Eén overzicht van klussen en afspraken, gekoppeld aan Google Agenda of Outlook."),
            ("kist", "Materiaal klaargezet", "Uit de offerte of werkbon komt een materiaallijst per leverancier. U keurt goed, daarna gaat de bestelling als mail weg."),
            ("klok", "De klant kiest zelf een moment", "Na het tekenen krijgt de klant een paar vrije momenten uit uw agenda en kiest er zelf één. De afspraak staat vanzelf in uw agenda.")]),
        ("klantcontact", "Klantcontact", "Elke vraag van een klant, op elk kanaal, beantwoord door u.", [
            ("mail", "E-mailassistent", "Mails worden gesorteerd en voor de vragen die steeds terugkomen staat een conceptantwoord klaar. U leest mee en verstuurt."),
            ("chat", "WhatsApp-assistent", "Beantwoordt veelgestelde vragen met uw eigen antwoorden en zet door naar u als het ertoe doet."),
            ("tel", "AI-telefonist", "Neemt op wanneer u dat niet kunt, legt de aanvraag vast en plant een afspraak in. Elk gesprek is terug te lezen.")]),
        ("administratie", "Geld en administratie", "Werkbonnen, facturen en betalingen zonder overtikken.", [
            ("factuur", "Facturen die de wet aankunnen", "Van werkbon naar factuur, met controle op btw, verplichte teksten en de regels van Nederland en België."),
            ("klok", "Betaalherinneringen", "Open facturen krijgen op de juiste dag een herinnering klaargezet, in een toon die bij de klant past."),
            ("koppel", "Koppeling met uw boekhouding", "Uw klanten, facturen en prijzen komen uit de bestaande boekhouding in plaats van opnieuw ingevoerd te worden.")]),
        ("overzicht", "Overzicht en online", "Eén plek voor het team, een open deur voor uw klanten.", [
            ("tijdlijn", "Alles per klant op één tijdlijn", "Mail, telefoon, WhatsApp, notities en werkbonnen per klant. Niemand hoeft te zoeken of te bellen om te weten waar het staat."),
            ("portaal", "Klantportaal", "Uw klanten loggen in en zien hun eigen offerte, afspraak en dossier. Minder telefoontjes met de vraag hoe het ervoor staat."),
            ("web", "Website op maat", "Een website die past bij uw bedrijf en uw klanten, live binnen één tot twee weken.")]),
    ]
    links = {"AI-telefonist": "ai-telefonist.html", "WhatsApp-assistent": "whatsapp-automatisering.html", "Website op maat": "websites.html"}
    blokken = ""
    for sid, titel, intro, items in groepen:
        k = "".join(kaart(i, t, x, links.get(t), "Meer lezen") for i, t, x in items)
        blokken += f"""<section class="n-sec n-sec-kort" id="{sid}"><div class="n-wrap">
{sectiekop(titel, intro)}
<div class="n-raster n-drie">{k}</div>
</div></section>"""

    bijzonder = f"""<section class="n-sec"><div class="n-wrap">
{sectiekop("Zo bouwen wij het", "Wij vervangen uw systemen niet")}
<div class="n-raster n-drie">
{kaart("koppel", "Bovenop wat u heeft", "Waar uw boekhouding of agenda het toelaat, koppelen wij direct. Anders automatiseren wij de stappen eromheen.")}
{kaart("oog", "U keurt alles goed", "De assistent zet klaar, u kijkt na. Er gaat niets de deur uit zonder dat u het wilt.")}
{kaart("slot", "Uw gegevens blijven van u", "Waar wij persoonsgegevens verwerken, leggen wij dat vóór de start vast in een verwerkersovereenkomst.")}
</div>
</div></section>"""

    inhoud = (paginakop("Oplossingen", "Oplossingen voor het werk dat elke week terugkomt",
                        "Kies één onderdeel of laat ons het geheel overzien. Alles werkt bovenop uw huidige systemen en u houdt de controle.",
                        '<div class="n-acties"><a class="n-knop n-knop-vol" href="index.html#contact">Plan een kennismaking</a><a class="n-knop n-knop-lijn" href="scan.html">Doe de gratis tijdverlies-scan</a></div>')
              + blokken + bijzonder + oproep("Waar begint u het liefst?",
              "Wij kijken samen waar het meeste tijd verloren gaat en beginnen daar. Ook als dat betekent dat u maar één onderdeel afneemt."))
    pagina("oplossingen.html", "Oplossingen voor vakbedrijven | Complete AI",
           "Alle oplossingen van Complete AI: offertes, planning, klantcontact, administratie en een AI-telefonist. Werkt bovenop uw huidige systemen.",
           "oplossingen.html", inhoud)


# ═════════════════════════ WERKWIJZE ═════════════════════════

def werkwijzepagina():
    fasen = [
        ("01", "Kennismaking", "Kort na uw aanvraag", "Wij luisteren, lopen uw werkdag door en kijken waar tijd verloren gaat.",
         ["Per videogesprek of bij u op locatie.", "U hoort eerlijk of automatiseren iets voor u is, ook als de conclusie is dat u niets bij ons hoeft af te nemen.", "Wij noemen geen bedragen en geen percentages voordat wij uw situatie kennen."]),
        ("02", "Voorstel en overeenkomst", "Na de kennismaking", "U krijgt een offerte met vaste bedragen en een overeenkomst die u online tekent.",
         ["Duidelijk wat wij bouwen, wat het kost en wat de looptijd is.", "De verwerking van persoonsgegevens leggen wij vast in een verwerkersovereenkomst.", "Pas na uw handtekening komen er echte klantgegevens in de app."]),
        ("03", "Intake en inrichten", "In de eerste dagen na het tekenen", "U krijgt een eigen portaal. Daar vult u een vragenlijst in en ziet u hoe ver wij zijn.",
         ["Wij richten de app in met uw logo, uw kleuren en uw eigen prijzen.", "Uw klanten en oude offertes en facturen gaan erin, zodat u niet opnieuw begint.", "Offertes en facturen krijgen de opmaak die u nu al gebruikt."]),
        ("04", "Proefdraaien en live", "In de eerste twee weken", "Wij testen eerst op uw eigen oude aanvragen. U ziet per regel wat wij anders rekenen dan u. Alleen wat klopt gaat live.",
         ["Wat het systeem niet kan, zeggen wij erbij. Dat is een uitkomst, geen mislukking.", "Wij leggen het uit aan iedereen die ermee werkt.", "Waar het kan, zetten wij de eerste winst samen met u live."]),
        ("05", "Meekijken en meten", "Na dertig dagen", "Wij kijken de eerste weken mee en sturen bij. Na dertig dagen meten wij opnieuw, met dezelfde getallen als bij de intake.",
         ["U ziet wat het opleverde, in uw eigen cijfers.", "Samen kiezen wij de volgende stap uit uw eigen lijst.", "Eén vast aanspreekpunt, ook daarna."]),
    ]
    fb = "".join(f"""<div class="n-fase"><div class="n-fase-nr n-glans">{n}</div><div class="n-fase-in">
  <h3>{t}</h3><span class="n-fase-tijd">{tijd}</span><p>{p}</p>{lijst(l)}</div></div>""" for n, t, tijd, p, l in fasen)

    portaal = mock("Uw portaal", "Wat u in een oogopslag ziet", "Voorbeeld",
        regels([("Planning", "waar wij staan"), ("Opleveringen", "wat klaar is"), ("Aan te leveren", "wat wij van u nodig hebben"), ("Documenten", "alles op één plek"), ("Updates", "elke wijziging, kort uitgelegd")]),
        "Voorbeeld met verzonnen gegevens.")
    portaalblok = f"""<section class="n-sec"><div class="n-wrap"><div class="n-oplossing">
  <div class="n-oplossing-tekst">
    <span class="n-nr">Uw eigen portaal</span>
    <h3>U ziet altijd waar wij staan</h3>
    <p class="n-t">Elke klant krijgt een eigen portaal. Daar staat wat wij doen, wat wij van u nodig hebben en wat er veranderd is. U hoeft niet te bellen om te weten hoe het ervoor staat.</p>
    {lijst(["Elke wijziging aan uw app komt als korte update in uw portaal.", "Vragen aan u staan op één lijst, met de reden erbij.", "Uw documenten staan er veilig, op één plek."])}
  </div>
  <div class="n-oplossing-beeld">{portaal}</div>
</div></div></section>"""

    afspraken = f"""<section class="n-sec"><div class="n-wrap">
{sectiekop("Onze afspraken", "Wat u van ons mag verwachten")}
<div class="n-raster n-drie">
{kaart("oog", "Concept eerst", "De assistent zet klaar, u keurt goed. Pas wat aantoonbaar klopt, laten wij zelfstandig lopen, en alleen met uw akkoord.")}
{kaart("slot", "Uw gegevens blijven van u", "Offertes, klanten en teksten blijven te allen tijde uw eigendom. Wij leggen de verwerking vast voordat er iets draait.")}
{kaart("klant", "Geen gokcijfers", "Wij beloven vooraf geen percentage. U ziet na dertig dagen wat het opleverde, in uw eigen getallen.")}
</div>
</div></section>"""
    inhoud = (paginakop("Werkwijze", "Zo werken wij, van kennismaking tot een app die draait",
                        "Vijf stappen. Elke stap levert iets op dat u kunt zien, en u beslist bij elke stap of wij doorgaan.")
              + f'<section class="n-sec n-sec-kort"><div class="n-wrap" style="max-width:900px">{fb}</div></section>'
              + portaalblok + afspraken + oproep())
    pagina("werkwijze.html", "Werkwijze: van kennismaking tot live | Complete AI",
           "Zo werkt Complete AI: kennismaking, voorstel, intake, proefdraaien op uw eigen oude aanvragen en meten na dertig dagen. U houdt de controle.",
           "werkwijze.html", inhoud)


# ═════════════════════════ RESULTATEN ═════════════════════════

def resultatenpagina():
    def case(sid, tag, titel, intro, punten, onder):
        li = "".join(f"<li>{ic('check')}<span>{x}</span></li>" for x in punten)
        return f"""<div class="n-kaart n-case" id="{sid}"><span class="n-tag">{tag}</span><h3>{titel}</h3><p>{intro}</p><ul>{li}</ul><p class="n-let">{onder}</p></div>"""

    a = case("installatie", "Installatiebedrijf", "Van offerte tot factuur, voor zonnepanelen, warmtepompen en laadpalen",
             "Een bedrijf dat bij particulieren plaatst en veel offertes maakt. De klantenapp is ingericht met de eigen kleuren en het eigen logo.",
             ["Een klantenapp met dertien onderdelen, van klantenbestand tot facturatie.",
              "Het klantenbestand is uit de oude boekhouding overgezet, zodat niemand opnieuw begint.",
              "Een prijsboek opgebouwd uit de oude offertes en facturen, zodat nieuwe calculaties met eigen prijzen starten.",
              "Offertes met vaste bijlagen en betaalschema, en online tekenen door de klant.",
              "Na het tekenen kiest de klant zelf een vrij moment voor de schouw.",
              "Een klantportaal waarin de klanten van het bedrijf hun eigen dossier zien.",
              "Een AI-telefonist en een WhatsApp-assistent met vaste antwoorden, alleen op basis van wat het bedrijf zelf aanleverde."],
             "Stand november 2026: ingericht. De ingebruikname gebeurt in fasen, samen met de eigenaar.")
    b = case("metaal", "Metaalbedrijf", "Maatwerk in staal, rvs en aluminium, met vaste opmaak",
             "Een bedrijf met constructiewerk, leidingwerk en machinebouw in Vlaanderen. Het werkt van schets naar offerte, akkoord, materiaal en levering.",
             ["Vijftien onderdelen van de klantenapp, gekozen na een uitgebreide intake.",
              "Offerte, factuur en calculatie in de eigen, vaste opmaak van het bedrijf. Niemand kan die per ongeluk wijzigen.",
              "De Belgische factuurregels worden afgedwongen: officiële bedrijfsnaam, verplichte vermeldingen en een controle voordat een factuur wordt vastgelegd.",
              "De bestaande facturen zijn overgenomen, zodat de nummering gewoon doortelt."],
             "Eerste klant van Complete AI, sinds september 2026.")

    eerlijk = f"""<section class="n-sec n-sec-kort"><div class="n-wrap"><div class="n-kaart" style="max-width:860px;margin-inline:auto;text-align:center;align-items:center">
  <span class="n-ico">{ic('oog')}</span>
  <h3>Wanneer volgen de cijfers?</h3>
  <p>Wij zetten hier pas gemeten resultaten neer als het bedrijf na dertig dagen zelf zijn eigen getallen heeft ingevuld. Tot dan staat hier alleen wat er gebouwd is. Een percentage verzinnen wij niet.</p>
</div></div></section>"""
    inhoud = (paginakop("Resultaten", "Wat wij voor vakbedrijven bouwden",
                        "Twee bedrijven, twee soorten werk. Hieronder staat wat er voor hen is ingericht. De namen laten wij weg: het zijn hun gegevens. Hoe wij te werk gaan, leest u bij onze <a href=\"werkwijze.html\">werkwijze</a>.")
              + f'<section class="n-sec n-sec-kort"><div class="n-wrap"><div class="n-raster n-twee">{a}{b}</div></div></section>'
              + eerlijk + oproep("Wat bouwen wij voor u?"))
    pagina("resultaten.html", "Resultaten: wat wij voor vakbedrijven bouwden | Complete AI",
           "Wat Complete AI bouwde voor een installatiebedrijf en een metaalbedrijf: offertes, facturen, portaal en telefonist, zonder dat iemand hoeft over te typen.",
           "resultaten.html", inhoud)


# ═════════════════════════ OVER ONS ═════════════════════════

def overonspagina():
    vast = f"""<section class="n-sec n-sec-kort"><div class="n-wrap"><div class="n-over">
  <div class="n-over-beeld"><img src="glenn-880.jpg" srcset="glenn-440.webp 440w, glenn-880.webp 880w" sizes="(max-width:900px) 340px, 380px" width="880" height="1100" alt="Glenn van Wijngaarden, oprichter van Complete AI" loading="lazy"></div>
  <div class="n-over-tekst">
    <span class="n-boven">Oprichter</span>
    <h2>Glenn van Wijngaarden</h2>
    <p>Complete AI helpt bedrijven in Nederland en Vlaanderen het terugkerende werk te automatiseren: administratie, klantcontact en bereikbaarheid.</p>
    <p>Wij bouwen zelf, kiezen zelf wat bij uw bedrijf past en blijven na de oplevering betrokken. U spreekt altijd met dezelfde persoon, van de kennismaking tot de meting na dertig dagen.</p>
    <div class="n-gegevens"><a href="tel:{TEL_LINK}">{ic('tel')}{TEL}</a><a href="mailto:{MAIL}">{ic('mail')}{MAIL}</a></div>
  </div>
</div></div></section>"""
    waarden = f"""<section class="n-sec"><div class="n-wrap">
{sectiekop("Waar wij voor staan", "Drie dingen die wij altijd doen")}
<div class="n-raster n-drie">
{kaart("oog", "U houdt de controle", "Alles wat naar een klant gaat, ziet u eerst. Zelfstandig laten lopen doen wij pas als het aantoonbaar klopt, en alleen met uw akkoord.")}
{kaart("slot", "Uw gegevens blijven van u", "Wij verwerken gegevens volgens de AVG en leggen dat vóór de start vast in een verwerkersovereenkomst.")}
{kaart("klok", "Eerlijk over wat kan", "Past automatiseren nu niet bij u, dan zeggen wij dat. En wat het systeem niet kan, staat er altijd bij.")}
</div>
</div></section>"""
    inhoud = (paginakop("Over ons", "Eén vast aanspreekpunt voor uw automatisering",
                        "Geen wisselende gezichten en geen doorverwijzingen. Wie met u kennismaakt, bouwt ook mee.")
              + vast + waarden + oproep())
    schema = {"@context": "https://schema.org", "@graph": [ORGANISATIE]}
    pagina("over-ons.html", "Over Complete AI | Eén vast aanspreekpunt",
           "Complete AI automatiseert administratie en klantcontact van bedrijven in Nederland en Vlaanderen. U spreekt altijd met dezelfde persoon.",
           "over-ons.html", inhoud, schema=schema)


# ═════════════════════════ SCAN ═════════════════════════

def scanpagina():
    intro = f"""<div id="scan-kop"><section class="n-pagina"><div class="n-wrap">
  <span class="n-boven">Gratis tijdverlies-scan</span>
  <h1>Hoeveel uur kost het kantoorwerk u <span class="n-glans">per week?</span></h1>
  <p class="n-lead">Administratie, offertes, planning en klantcontact. In drie minuten ziet u waar de tijd blijft en wat u er het eerst aan doet.</p>
</div></section></div>
<div class="n-wrap"><div class="n-scan">
  <div id="scan-intro">
    <div class="n-kaart" style="align-items:center;text-align:center;padding:clamp(24px,4vw,40px)">
      <ul class="n-lijst" style="margin:0 0 1.4rem;text-align:left">
        <li>{ic('check')}<span>Hoeveel uur per week naar kantoorwerk gaat, per onderdeel, en wat dat per jaar is</span></li>
        <li>{ic('check')}<span>Uw grootste tijdvreter, met een eerste stap die u vandaag al kunt zetten</span></li>
        <li>{ic('check')}<span>Wat het voorwerk u kost als er meer klussen bij komen</span></li>
        <li>{ic('check')}<span>Een uitslag die u kunt bewaren als PDF of delen met uw team</span></li>
      </ul>
      <button type="button" class="n-knop n-knop-vol" id="scan-start">Start de scan {ic('pijl')}</button>
      <p class="n-klein" style="margin-top:14px">Zeven stappen · ongeveer drie minuten · uitslag direct op uw scherm</p>
      <p class="n-klein" style="margin-top:6px">Uw antwoorden blijven op uw eigen apparaat. U hoeft geen gegevens in te vullen om de uitslag te zien.</p>
    </div>
    <p class="n-klein" style="text-align:center;margin:22px auto 0;max-width:56ch">De uitslag is een schatting op basis van uw eigen antwoorden, geen belofte. Wilt u eerst weten hoe wij te werk gaan? Lees de <a href="werkwijze.html" style="text-decoration:underline">werkwijze</a>, bekijk de <a href="oplossingen.html" style="text-decoration:underline">oplossingen</a> of de <a href="ai-telefonist.html" style="text-decoration:underline">AI-telefonist</a>.</p>
  </div>
  <div id="scan-app" aria-live="polite"></div>
  <noscript><p class="n-stand mis" style="margin-top:20px">Voor de scan is JavaScript nodig. Wilt u liever bellen? Dat kan op {TEL}.</p></noscript>
</div></div>
<div style="height:var(--sec)"></div>"""
    pagina("scan.html", "Gratis tijdverlies-scan voor vakbedrijven | Complete AI",
           "Hoeveel uur kost het kantoorwerk u per week? Zeven stappen, uitslag direct op uw scherm: uw grootste tijdvreter, wat het per jaar is en een eerste stap.",
           "scan.html", intro, extra_js="scan")


# ═════════════════ JURIDISCHE PAGINA'S EN OUDE PAGINA'S IN DE NIEUWE KOP EN VOET ═════════════════

JURIDISCH = ["privacy.html", "voorwaarden.html", "gegevens-verwijderen.html"]


def juridisch(bestand):
    """Privacy, voorwaarden en gegevens verwijderen: dezelfde tekst, in de nieuwe vormgeving.
    De tekst zelf wordt uit het bestaande bestand gelezen en niet veranderd."""
    pad = os.path.join(HIER, bestand)
    t = open(pad, encoding="utf-8").read()
    titel = html.unescape(re.search(r"<title>(.*?)</title>", t, re.S).group(1))
    omschr = html.unescape(re.search(r'<meta name="description" content="(.*?)"', t).group(1))
    robots = re.search(r'name="robots" content="(.*?)"', t)
    inner = re.search(r"<main[^>]*>(.*)</main>", t, re.S).group(1).strip()
    inner = re.sub(r'^<div class="n-wrap n-tekst">\s*', "", inner)
    inner = re.sub(r"\s*</div>$", "", inner) if t.count('class="n-wrap n-tekst"') else inner
    # de oude pagina had een eigen wrap; die vervalt, de nieuwe wikkel komt ervoor in de plaats
    inner = re.sub(r'^<div class="wrap">\s*', "", inner)
    inner = re.sub(r"\s*</div>\s*$", "", inner) if t.count('<div class="wrap">') and not t.count('class="n-wrap n-tekst"') else inner
    pagina(bestand, titel, omschr, "", '<div class="n-wrap n-tekst">' + inner + "</div>",
           robots=robots.group(1) if robots else "index, follow")


def schil_wisselen(bestand):
    """Handmatig onderhouden pagina's met de oude kop en voet (klantenapp, pakketten): vervang alleen kop en
    voet door de nieuwe, voeg nieuw-schil.css toe, laat de rest staan."""
    pad = os.path.join(HIER, bestand)
    if not os.path.exists(pad):
        return
    t = open(pad, encoding="utf-8").read()
    t = re.sub(r'<a class="n-skip".*?</header>', lambda _m: kop(""), t, count=1, flags=re.S) if 'class="n-skip"' in t \
        else re.sub(r'<header class="balk".*?</header>', lambda _m: kop(""), t, count=1, flags=re.S)
    t = re.sub(r'<footer[^>]*>.*?</footer>', lambda _m: VOET, t, count=1, flags=re.S)
    t = re.sub(r'<link rel="stylesheet" href="nieuw-schil\.css(\?v=[0-9a-f]+)?">\s*', "", t)
    t = re.sub(r'(<link rel="stylesheet" href="/?stijl\.css[^>]*>)', lambda m_: m_.group(1) + f'\n<link rel="stylesheet" href="nieuw-schil.css?v={SCHIL_V}">', t, count=1)
    open(pad, "w", encoding="utf-8").write(t)
    print("  kop en voet vernieuwd:", bestand)


if __name__ == "__main__":
    print("Bouw de nieuwe pagina's:")
    startpagina(); oplossingenpagina(); werkwijzepagina(); resultatenpagina(); overonspagina(); scanpagina()
    for j in JURIDISCH:
        juridisch(j)
    for h in ("klantenapp.html", "pakketten.html"):
        schil_wisselen(h)
    print("klaar. stempels:", CSS_V, JS_V, SCAN_V, SCHIL_V)
