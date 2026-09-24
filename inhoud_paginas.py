# -*- coding: utf-8 -*-
"""De inhoud van de dienstpagina's. Alleen hier aanpassen, daarna
`python3 bouw-paginas.py` draaien om de HTML opnieuw te genereren."""


def sectie(kop_label, kop, intro, body, ident=""):
    id_attr = f' id="{ident}"' if ident else ""
    return f"""  <section{id_attr}>
    <div class="wrap">
      <div class="sectiekop reveal">
        <p class="label"><i></i>{kop_label}</p>
        <h2>{kop}</h2>
        <p>{intro}</p>
      </div>
{body}
    </div>
  </section>"""


def pijnblok(items):
    kaarten = "".join(
        f'\n        <article><span class="nr">{i:02d}</span><p>{t}</p><small>{o}</small></article>'
        for i, (t, o) in enumerate(items, 1))
    return f'      <div class="pijn reveal">{kaarten}\n      </div>'


def krijgtblok(items):
    kaarten = "".join(f'\n        <article><h3>{t}</h3><p>{o}</p></article>' for t, o in items)
    return f'      <div class="krijgt reveal">{kaarten}\n      </div>'


def voorbeeldblok(items):
    kaarten = "".join(f'\n        <div class="voorbeeld"><b>{t}</b><span>{o}</span></div>' for t, o in items)
    return f'      <div class="voorbeelden reveal">{kaarten}\n      </div>'


def routeblok(items):
    fasen = "".join(
        f'\n        <div class="fase"><i>Stap {i}</i><b>{t}</b><p>{o}</p></div>'
        for i, (t, o) in enumerate(items, 1))
    return f'      <div class="route reveal">{fasen}\n      </div>'


def eerlijkblok(kop, inleiding, punten):
    lijst = "".join(f"\n          <li>{p}</li>" for p in punten)
    return (f'      <div class="eerlijk reveal">\n        <h3>{kop}</h3>\n'
            f'        <p>{inleiding}</p>\n        <ul>{lijst}\n        </ul>\n      </div>')


def plaatsenblok(items):
    kaarten = "".join(f'\n        <div class="voorbeeld"><b>{t}</b><span>{o}</span></div>' for t, o in items)
    return f'      <div class="voorbeelden reveal">{kaarten}\n      </div>'


def proza(kop_label, kop, body, ident="", intro=""):
    """Lopende tekst: koppen (h3), alinea's, lijsten, tabellen, met gewone links.
    `body` is HTML met <h3>, <p>, <ul>, <ol>, <table> in <div class="tabelwrap">."""
    id_attr = f' id="{ident}"' if ident else ""
    intro_html = f"\n        <p>{intro}</p>" if intro else ""
    return f"""  <section{id_attr}>
    <div class="wrap">
      <div class="sectiekop reveal">
        <p class="label"><i></i>{kop_label}</p>
        <h2>{kop}</h2>{intro_html}
      </div>
      <div class="proza reveal">
{body}
      </div>
    </div>
  </section>"""


def inhoudsopgave(items):
    """items: [(sectie-id, tekst)]. Sprongmarkeringen naar de secties op deze pagina."""
    lijst = "".join(f'\n          <li><a href="#{i}">{t}</a></li>' for i, t in items)
    return f"""  <section id="inhoud">
    <div class="wrap">
      <nav class="inhoud reveal" aria-label="Inhoud van deze pagina">
        <p class="label"><i></i>In deze pagina</p>
        <ol>{lijst}
        </ol>
      </nav>
    </div>
  </section>"""


def bronnen(items, intro="Waar de feiten op deze pagina vandaan komen."):
    """items: [(tekst, url, toelichting)]. Externe verwijzingen naar gezaghebbende bronnen."""
    lijst = "".join(
        f'\n          <li><a href="{u}" rel="noopener" target="_blank">{t}</a><span>{o}</span></li>'
        for t, u, o in items)
    return f"""  <section id="bronnen" class="bronnen">
    <div class="wrap">
      <div class="sectiekop reveal">
        <p class="label"><i></i>Bronnen</p>
        <h2>Bronnen en verder lezen.</h2>
        <p>{intro}</p>
      </div>
      <ul class="reveal">{lijst}
      </ul>
    </div>
  </section>"""


# ══════════════════════════════════════════════════════════════════
PAGINAS = [

# ─────────────────────────────── WEBSITES ───────────────────────────────
{
 "bestand": "websites.html",
 "dienst": "Websites",
 "titel": "Website laten maken voor het mkb, all-in | Complete AI",
 "beschrijving": "Website laten maken voor uw mkb-bedrijf, all-in: ontwerp, teksten en bouw, met hosting en onderhoud in een vast maandbedrag. Live in 1 tot 2 weken.",
 "omschrijving": "Websites op maat voor mkb-bedrijven: ontwerp, teksten, techniek, vindbaarheid en hosting. All-in, met onderhoud in een vast maandbedrag. Live binnen één tot twee weken.",
 "ogen": "Websites",
 "h1": 'Website laten maken voor het mkb: <span class="glans">all-in en live in 1 tot 2 weken</span>.',
 "lead": "Een website laten maken voor het mkb kan all-in: ontwerp, teksten en bouw eenmalig, en hosting, back-ups, updates en kleine wijzigingen in een vast maandbedrag. Complete AI zet uw site binnen één tot twee weken live, snel op mobiel en vindbaar vanaf de eerste dag. U spreekt tot het einde de persoon die hem bouwt.",
 "levertijd": "Live in 1 tot 2 weken",
 "gewijzigd": "2026-09-24",
 "uitkomsten": [
     ("0,7 s", "laadtijd van deze pagina; dezelfde norm geldt voor uw site"),
     ("0", "cookiebanners: er staat geen tracking op die er een vereist"),
     ("1–2 wk", "van akkoord tot live, inclusief teksten"),
 ],
 "slot_kop": "Wat kan uw website in uw situatie opleveren?",
 "slot_tekst": "In een half uur nemen we door wat er nu staat, wie uw klanten zijn en waar het misloopt. Binnen één werkdag ligt er een voorstel op papier met één vaste prijs. U ontvangt een onderbouwd advies, ook wanneer de conclusie is dat de site voldoet en de winst elders ligt.",
 "vragen": [
   ("Wat kost het om een website te laten maken?",
    "Dat hangt af van vier dingen: het aantal pagina’s, de functies zoals online boeken of meertaligheid, wie de teksten en het beeld levert en het onderhoud daarna. Daarom noemen wij vooraf geen bedrag. Na een intake van een half uur ligt er binnen één werkdag één vaste prijs op papier, zonder nacalculatie."),
   ("Wat kost het om een simpele website te laten maken?",
    "Een simpele website heeft weinig pagina’s, geen functies buiten een contactformulier en teksten en beeld die u zelf aanlevert. Wat dat kost, staat na de intake vast op papier. Komen er online boeken, meerdere talen of extra pagina’s bij, dan is het een andere opdracht en ziet u dat terug in het voorstel."),
   ("Wat kost een zakelijke website?",
    "Een zakelijke website is meer dan een visitekaartje: hij moet vindbaar zijn en aanvragen opleveren. De kosten volgen uit de omvang: pagina’s, functies, teksten, beeld en onderhoud. Zonder gesprek noemen wij geen bedrag. In de intake bepalen we wat de site moet doen, daarna volgt het voorstel met één vaste prijs."),
   ("Wat is een all-in website en wat zit erin?",
    "All-in betekent dat ontwerp, teksten en bouw eenmalig zijn geregeld en dat hosting, back-ups, updates, het SSL-certificaat en kleine wijzigingen in een vast maandbedrag zitten. Zo krijgt u geen losse facturen van drie partijen. Het maandbedrag is maandelijks opzegbaar. Vraag bij elke aanbieder wat er precies onder all-in valt."),
   ("Wilt u een mkb-website op maat laten maken? Hoe werkt dat?",
    "Ja, dat kan. Op maat betekent dat ontwerp en teksten uw bedrijf volgen, en niet een sjabloon met een logo. In een intake van een half uur bepalen we wat de site moet doen. Binnen één werkdag volgt het voorstel, en binnen één tot twee weken na akkoord staat de site live."),
   ("Kan ChatGPT een website maken?",
    "Ja, ChatGPT en AI-bouwers maken een opzet met tekst en opmaak. Het werk erna blijft: uw gegevens controleren, domein en hosting regelen, vindbaarheid instellen en onderhoud. Wilt u dat iemand daar verantwoordelijk voor is, dan bouwt Complete AI de site en blijft Glenn van Wijngaarden uw aanspreekpunt."),
   ("Hoe lang duurt het om een website te laten maken, en waarom kan het in twee weken?",
    "Van akkoord tot live duurt het één tot twee weken. Het kan zo snel omdat er geen accountmanager of projectleider tussen zit, u spreekt de persoon die bouwt, en omdat de technische onderdelen al gebouwd en getest zijn. Komen er functies bij of levert u beeld later aan, dan verschuift de planning en hoort u dat vooraf."),
   ("Moet ik van mijn huidige website af?",
    "Niet per se. Voldoet een bestaande site, dan ligt de winst elders: in vindbaarheid, of in het automatiseren van de administratie. Dat hoort u in de intake, ook wanneer de conclusie is dat u niets bij Complete AI hoeft af te nemen."),
   ("Ik heb geen teksten en geen goede foto’s. Is dat een probleem?",
    "Nee, dat is geen bezwaar. De teksten schrijven wij op basis van één gesprek waarin we doorvragen op wat u doet en voor wie. Voor beeldmateriaal werken we met wat er is, aangevuld met professionele beelden. Is fotografie nodig, dan hoort u dat vooraf."),
   ("Kan ik later zelf wijzigingen doorvoeren?",
    "Ja. Kleine wijzigingen, zoals een tekst, een prijs of openingstijden, vallen onder het maandbedrag: u stuurt één bericht en krijgt binnen één werkdag reactie. Wilt u het liever zelf doen, dan richten wij dat zo in dat het zonder technische kennis kan."),
   ("Heb ik een cookiebanner nodig?",
    "Een cookiebanner is nodig zodra een site tracking-cookies plaatst, want daarvoor is toestemming vereist. Onze websites bevatten geen tracking die dat vraagt, dus deze site heeft geen banner. Komt er later tracking bij, bijvoorbeeld voor advertenties, dan bespreken wij vooraf wat dat betekent."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   inhoudsopgave([
     ("herkenbaar", "Wat er bij bestaande sites misloopt"),
     ("wat-u-krijgt", "Wat u krijgt"),
     ("kosten", "Wat bepaalt wat een website kost?"),
     ("all-in", "Wat hoort er bij een all-in maandbedrag?"),
     ("twee-weken", "Hoe verloopt een traject van twee weken?"),
     ("snelheid", "Snelheid en mobiel"),
     ("vindbaar", "Vindbaar vanaf dag één"),
     ("ai", "Website laten maken door AI"),
     ("maatwerk", "Maatwerk of sjabloon"),
     ("eigen-praktijk", "Uit eigen praktijk"),
     ("bronnen", "Bronnen"),
   ]),

   sectie("De situatie", "Representatief zijn en resultaat opleveren zijn twee verschillende zaken.",
          "Vier bevindingen die wij bij een bestaande site terugzien.",
          pijnblok([
            ("Niet vindbaar", "De site staat online, maar wie niet de bedrijfsnaam intypt komt hem nooit tegen."),
            ("Trage laadtijd op mobiel", "Een pagina die op een telefoon traag laadt, laat bezoekers wachten. Google noemt 2,5 seconden als grens voor de hoofdinhoud."),
            ("Geen duidelijke vervolgstap", "Een bezoeker kijkt rond, vindt geen aanleiding tot contact en verlaat de site."),
            ("Wijzigingen duren te lang", "Waardoor ze uitblijven en de site geleidelijk veroudert."),
          ]), "herkenbaar"),

   sectie("Wat u krijgt", "Alles wat nodig is, in één keer geregeld.",
          "Geen losse onderdelen die u zelf moet samenbrengen. Eén aanspreekpunt, en aan het eind staat er iets dat af is.",
          krijgtblok([
            ("Ontwerp op maat", "Geen sjabloon met een logo erin. Het ontwerp volgt uw bedrijf, uw klanten en uw doelstelling."),
            ("Mobiel eerst", "Wij ontwerpen op telefoonformaat en werken omhoog naar de laptop, niet andersom. Google gebruikt de mobiele versie van een pagina om die op te nemen en te beoordelen."),
            ("Snelheid als uitgangspunt", "Geen zware paginabouwers of tientallen plug-ins. Deze pagina laadt in ongeveer 0,7 seconde; dat is de norm."),
            ("Teksten die kloppen", "Geschreven op basis van één gesprek, in uw taal en gericht op de klant die u wilt bereiken."),
            ("Vindbaar vanaf dag één", "Correcte structuur, sitemap, structuurdata en een volledig ingericht Google-bedrijfsprofiel."),
            ("Formulier dat aankomt", "Een formulier dat werkt lijkt vanzelfsprekend. Toch verdwijnt een aanvraag zodra het onderweg misgaat, zonder dat iemand het merkt. Wij zorgen dat het formulier aankomt."),
            ("Veilig en zonder waarschuwingen", "HTTPS met een certificaat dat zichzelf verlengt. Een statische site heeft geen database en geen inlogscherm dat aangevallen kan worden."),
            ("Hosting en onderhoud", "Hosting, back-ups, updates en het SSL-certificaat zitten in het maandbedrag, evenals kleine wijzigingen. Maandelijks opzegbaar."),
          ]), "wat-u-krijgt"),

   proza("Kosten", "Wat bepaalt wat een website kost?", """        <h3>De vijf onderdelen die de omvang bepalen</h3>
        <p>Een website is geen product met een vaste omvang. Vijf onderdelen bepalen hoeveel werk erin zit, en daarmee wat een voorstel omvat.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Onderdeel</th><th>Wat het bepaalt, en wat u kunt doen</th></tr></thead>
          <tbody>
            <tr><td><strong>Aantal pagina’s</strong></td><td>Elke pagina heeft een eigen ontwerp, een eigen tekst en een eigen doel in Google. Een pagina per dienst die u verkoopt, een pagina over uw bedrijf en een contactpagina vormen de kern.<br><strong>Voorbereiding:</strong> Maak een lijst van de diensten die u werkelijk wilt verkopen. Wat daar niet op staat, kan later.</td></tr>
            <tr><td><strong>Functies</strong></td><td>Online boeken of meertaligheid zijn elk een eigen stuk techniek dat gebouwd, getest en onderhouden moet worden.<br><strong>Voorbereiding:</strong> Beschrijf wat de site op de eerste dag moet kunnen. Een functie die pas over een half jaar nodig is, hoeft er nu niet in.</td></tr>
            <tr><td><strong>Teksten</strong></td><td>Wie ze schrijft en hoeveel gesprekken of rondes daarvoor nodig zijn. Bij Complete AI schrijven wij de teksten op basis van één gesprek.<br><strong>Voorbereiding:</strong> Bedenk wat uw bedrijf onderscheidt en welke vragen klanten stellen. Dat is de invoer voor dat gesprek.</td></tr>
            <tr><td><strong>Beeld</strong></td><td>Eigen foto’s, aangevuld met professioneel beeld, of een fotograaf. Is fotografie nodig, dan hoort u dat vooraf.<br><strong>Voorbereiding:</strong> Verzamel foto’s van uw werk, uw team en uw locatie, ook als ze niet perfect zijn.</td></tr>
            <tr><td><strong>Onderhoud na oplevering</strong></td><td>Hosting, back-ups, updates en kleine wijzigingen zijn terugkerend werk. Bij een all-in zitten ze in het maandbedrag.<br><strong>Voorbereiding:</strong> Vraag bij elk voorstel wat er onder onderhoud valt. De volgende sectie geeft de vragen.</td></tr>
          </tbody>
        </table></div>
        <h3>Wat een simpele website is</h3>
        <p>Een simpele website heeft weinig pagina’s, geen functies buiten een contactformulier en teksten en beeld die u zelf aanlevert. Wat dat kost, hangt nog steeds af van de vijf onderdelen hierboven. Komen er online boeken, meerdere talen of extra pagina’s bij, dan is het een andere opdracht. Dat ziet u terug in het voorstel. Online boeken is ook los in te richten, zie <a href="automatisering.html">automatisering</a>.</p>
        <h3>Waarom een bedrag zonder gesprek weinig zegt</h3>
        <p>Een bedrag zonder gesprek berust op aannames over deze vijf onderdelen. Twee aanbieders kunnen dan hetzelfde bedrag noemen voor een verschillende site, of een verschillend bedrag voor dezelfde site. Vergelijk voorstellen daarom op inhoud: hoeveel pagina’s, welke functies, wie de teksten schrijft, welk beeld erbij zit en wat er na oplevering gebeurt.</p>
        <h3>Hoe een voorstel bij Complete AI tot stand komt</h3>
        <ol>
          <li><strong>Intake.</strong> Een half uur over wat u doet, wie uw klanten zijn en wat de site moet opleveren. Kosteloos en vrijblijvend.</li>
          <li><strong>Voorstel.</strong> Binnen één werkdag ligt er een voorstel op papier: wat wij bouwen, wanneer het staat en één vaste prijs zonder nacalculatie. Die prijs bestaat uit een eenmalig deel voor de bouw en een vast maandbedrag voor onderhoud en bijsturing.</li>
          <li><strong>Uw keuze.</strong> U beslist of u het voorstel accepteert. Blijkt dat uw bestaande site voldoet, dan hoort u dat in de intake.</li>
        </ol>
        <div class="noot"><p>Wilt u vooraf een indruk? Vertel in de <a href="index.html#contact">intake</a> welke pagina’s en functies u in gedachten heeft. Binnen één werkdag weet u waar uw wensen uitkomen.</p></div>""", "kosten"),

   proza("All-in", "Wat hoort er bij een all-in maandbedrag?", """        <p>All-in zegt niets over wat erin zit. Het is een woord van de aanbieder, en wat eronder valt staat in het voorstel. Vraag daarom altijd wat er precies onder valt.</p>
        <h3>Wat bij Complete AI in het maandbedrag zit</h3>
        <ul>
          <li><strong>Hosting.</strong> De site staat op een server die wij regelen. U hoeft geen aparte hostingpartij te kiezen of te betalen.</li>
          <li><strong>Back-ups.</strong> Een kopie van de site, zodat een fout hersteld kan worden.</li>
          <li><strong>Updates.</strong> Het bijwerken van de techniek onder de site is ons werk, niet het uwe.</li>
          <li><strong>SSL-certificaat.</strong> De site draait op HTTPS, met een certificaat dat zichzelf verlengt.</li>
          <li><strong>Kleine wijzigingen.</strong> Een tekst, een prijs of openingstijden: u stuurt één bericht en krijgt binnen één werkdag reactie.</li>
          <li><strong>Maandelijks opzegbaar.</strong> Zonder langlopende verplichting.</li>
        </ul>
        <p>Ontwerp, teksten en bouw vallen niet in het maandbedrag. Die zitten in het eenmalige deel van de prijs. Daarom staat er in het voorstel altijd beide.</p>
        <h3>Zes vragen die u aan elke aanbieder stelt</h3>
        <div class="tabelwrap"><table>
          <thead><tr><th>Vraag</th><th>Waarom, en hoe het bij Complete AI is</th></tr></thead>
          <tbody>
            <tr><td><strong>Wat valt onder het maandbedrag, en wat niet?</strong></td><td>Hosting, back-ups, updates en beveiliging zijn terugkerend werk. Valt een van de vier erbuiten, dan komt er een tweede rekening.<br><strong>Bij Complete AI:</strong> Hosting, back-ups, updates, SSL en kleine wijzigingen zitten erin.</td></tr>
            <tr><td><strong>Wat is een kleine wijziging?</strong></td><td>Een tekst of openingstijd is klein. Een nieuwe pagina of functie is dat mogelijk niet. Leg de grens vast met voorbeelden.<br><strong>Bij Complete AI:</strong> Een tekst, een prijs of openingstijden. Bij twijfel hoort u dat in het voorstel.</td></tr>
            <tr><td><strong>Hoe snel wordt er gereageerd?</strong></td><td>Een fout op uw site kost bezoekers zolang hij bestaat. De reactietijd bepaalt hoe lang dat duurt.<br><strong>Bij Complete AI:</strong> Reactie binnen één werkdag.</td></tr>
            <tr><td><strong>Op wiens naam staat het domein?</strong></td><td>De domeinnaam is uw adres op internet. Staat hij op naam van de bouwer, dan hangt uw adres aan die bouwer.<br><strong>Bij Complete AI:</strong> Stel deze vraag in de intake. Het antwoord legt u vast in het voorstel.</td></tr>
            <tr><td><strong>Wat krijgt u mee als u opzegt?</strong></td><td>Teksten, beelden en de site zelf zijn waarde die u heeft betaald. Vraag in welk formaat u ze meekrijgt.<br><strong>Bij Complete AI:</strong> Stel deze vraag in de intake. Het antwoord legt u vast in het voorstel.</td></tr>
            <tr><td><strong>Hoe lang zit u vast?</strong></td><td>Een lang contract maakt overstappen duur, ook als de dienst tegenvalt.<br><strong>Bij Complete AI:</strong> Maandelijks opzegbaar.</td></tr>
          </tbody>
        </table></div>""", "all-in"),

   sectie("Werkwijze", "Hoe verloopt een traject van twee weken?",
          "Voorbereiding is niet nodig. Wij beginnen met een half uur en een open beeld van hoe het nu loopt.",
          routeblok([
            ("Intake", "Een half uur om vast te stellen wat er nu staat, wie de klanten zijn en waar het misloopt. Kosteloos en vrijblijvend."),
            ("Voorstel", "Binnen één werkdag op papier: wat we bouwen, wat het kost en wanneer het staat. Eén vaste prijs."),
            ("Teksten", "Eén gesprek waarin wij doorvragen op wat u doet en voor wie. Daaruit schrijven wij de teksten."),
            ("Bouwen", "Na enkele dagen ontvangt u een link om mee te kijken. Aanpassingen verwerken we gaandeweg, niet pas bij oplevering."),
            ("Oplevering", "Wij zetten de site live, koppelen domein en e-mail, en nemen alles met u door tot u ermee overweg kunt."),
          ]) + """
      <div class="proza reveal">
        <h3>Wat wij van u nodig hebben</h3>
        <ul>
          <li>Een half uur voor de intake en één gesprek voor de teksten.</li>
          <li>Beeld dat er al is: foto’s van uw werk, uw team en uw locatie.</li>
          <li>Uw reactie op de link waarmee u meekijkt. Hoe sneller die komt, hoe sneller de site staat.</li>
          <li>Uw akkoord bij de oplevering.</li>
        </ul>
        <h3>Wat de doorlooptijd bepaalt</h3>
        <p>De twee weken lopen van akkoord tot live. De planning verschuift wanneer een van drie dingen verandert: het aantal pagina’s en functies, het tempo waarin u reageert en de beschikbaarheid van beeld. Vraagt iets meer tijd dan ingeschat, dan hoort u dat vooraf en niet achteraf.</p>
        <p>Het tempo komt ook uit de manier van werken. Er zit geen accountmanager of projectleider tussen: u spreekt de persoon die bouwt. En een groot deel van wat wij inzetten is al gebouwd en getest, dus wij beginnen niet bij nul.</p>
      </div>""", "twee-weken"),

   proza("Snelheid en mobiel", "Wat is een snelle website, en waarom telt mobiel zwaarder?", """        <h3>Wat Google meet</h3>
        <p>Google beoordeelt paginabeleving met drie waarden, de Core Web Vitals. Ze beschrijven wat een bezoeker ervaart, niet wat de bouwer verwacht. De grenzen hieronder noemt Google zelf.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Waarde</th><th>Wat het meet</th><th>Grens voor een goede beleving</th></tr></thead>
          <tbody>
            <tr><td><strong>Largest Contentful Paint (LCP)</strong></td><td>Hoe snel de hoofdinhoud van de pagina zichtbaar is.</td><td>Binnen 2,5 seconden nadat de pagina begint te laden.</td></tr>
            <tr><td><strong>Interaction to Next Paint (INP)</strong></td><td>Hoe snel de pagina reageert op een tik of klik.</td><td>200 milliseconden of minder.</td></tr>
            <tr><td><strong>Cumulative Layout Shift (CLS)</strong></td><td>Of de pagina blijft staan terwijl hij laadt, of dat de inhoud verspringt.</td><td>0,1 of lager.</td></tr>
          </tbody>
        </table></div>
        <p>Google raadt aan dit te meten bij echte bezoeken, voor mobiel en desktop apart, en te kijken naar het niveau waar drie van de vier bezoeken aan voldoen (het 75e percentiel). Meetgereedschap rekent een pagina als geslaagd wanneer alle drie de waarden aan de grens voldoen.</p>
        <div class="noot"><p>Snelheid vervangt goede inhoud niet. Google schrijft dat goede scores niet garanderen dat een pagina bovenaan komt. Waar veel pagina’s dezelfde vraag goed beantwoorden, kan een goede paginabeleving wel het verschil maken.</p></div>
        <h3>Waarom mobiel eerst</h3>
        <p>Google gebruikt de mobiele versie van een site om pagina’s op te nemen en te beoordelen. Dat heet mobile-first indexing. Google raadt responsive design aan: dezelfde pagina, die zich aanpast aan het scherm. Wij ontwerpen daarom op telefoonformaat en werken omhoog naar de laptop.</p>
        <h3>Hoe u het zelf nagaat</h3>
        <p>De drie waarden zijn voor elke site na te lezen in PageSpeed Insights en in het Core Web Vitals-rapport van Search Console. Google noemt beide als meetgereedschap. Vraag een aanbieder dus niet om een belofte, maar om de meetwaarden van een site die hij eerder bouwde.</p>
        <h3>Wat wij daarvoor laten</h3>
        <p>Wij bouwen zonder zware paginabouwers en zonder tientallen plug-ins. Scripts van derden die de laadtijd verlengen en niets toevoegen, laten wij weg. Dat volgt Googles eigen advies: verwijder een script van een derde dat de pagina vertraagt zonder duidelijke waarde. Deze pagina laadt in ongeveer 0,7 seconde.</p>""", "snelheid"),

   proza("Vindbaarheid", "Wat betekent vindbaar vanaf dag één?", """        <p>Vindbaar vanaf de eerste dag betekent dat Google uw pagina’s kan vinden, lezen en begrijpen op het moment dat de site live gaat. Het betekent niet dat u er meteen bovenaan staat. Een nieuwe site heeft tijd nodig om door Google te worden opgepakt.</p>
        <h3>Wat er bij oplevering klaarstaat</h3>
        <ul>
          <li><strong>Structuur.</strong> Een pagina per dienst, elk met een eigen titel, een eigen beschrijving, één hoofdkop en een kruimelpad. Zo weet Google waar elke pagina over gaat.</li>
          <li><strong>Sitemap.</strong> Een bestand dat Google laat zien welke pagina’s er zijn. Google noemt een sitemap nuttig voor een nieuwe site met weinig verwijzingen van andere sites, omdat Google zulke pagina’s anders mogelijk niet ontdekt.</li>
          <li><strong>Structuurdata.</strong> Een gestandaardiseerde manier om Google te vertellen wat een pagina is. Het kan leiden tot een uitgebreider zoekresultaat, maar een garantie geeft Google niet. Structuurdata beschrijft alleen wat op de pagina zichtbaar is.</li>
          <li><strong>Google-bedrijfsprofiel.</strong> Volledig ingericht met openingstijden, diensten en foto’s. Volgens Google is een bedrijf met volledige en juiste gegevens eerder te zien in lokale zoekresultaten.</li>
          <li><strong>Snel en mobiel.</strong> De grenzen uit de vorige sectie zijn het uitgangspunt, niet een latere verbetering.</li>
        </ul>
        <h3>Wat daarna komt</h3>
        <p>Een site die te vinden is, is de basis. Pagina’s die de vragen van klanten beantwoorden, de meting in Search Console en een maandrapport zijn doorlopend werk. Dat staat bij <a href="vindbaarheid-seo.html">vindbaarheid (SEO)</a>. Het wekelijkse onderhoud van uw profiel valt onder <a href="social-media.html">social media</a>. Wilt u advertenties naast de gewone zoekresultaten, dan leest u dat bij <a href="adverteren.html">adverteren</a>.</p>""", "vindbaar"),

   proza("Website laten maken door AI", "Website laten maken door AI: kan ChatGPT of een AI-bouwer dat?", """        <p>Ja. Een AI-bouwer of een chatbot maakt snel een opzet met tekst en opmaak. Dat is een bruikbare manier om te zien wat u wilt, en voor een eerste concept of een eenvoudige eigen pagina kan het genoeg zijn. De vraag is wat er na die opzet nog moet gebeuren.</p>
        <h3>Wat er na de opzet nog moet gebeuren</h3>
        <div class="tabelwrap"><table>
          <thead><tr><th>Stap</th><th>Waarom het ertoe doet</th></tr></thead>
          <tbody>
            <tr><td><strong>Uw gegevens controleren</strong></td><td>Een AI kent uw bedrijf niet. Wat er staat over uw diensten, werkgebied en werkwijze moet u zelf nalopen. Google vraagt bij automatisch gemaakte inhoud om aandacht voor juistheid, kwaliteit en relevantie, ook in titels, beschrijvingen en structuurdata.</td></tr>
            <tr><td><strong>Eigen inzicht toevoegen</strong></td><td>Google noemt als toetsvraag of inhoud eigen ervaring en diepgang laat zien. Een tekst zonder invoer van u is algemeen en kan zo door elk ander bedrijf zijn gepubliceerd.</td></tr>
            <tr><td><strong>Domein, hosting en e-mail regelen</strong></td><td>Vraag na of ze zijn inbegrepen, wie ze beheert en wat er met uw adres gebeurt als u stopt.</td></tr>
            <tr><td><strong>Vindbaarheid instellen</strong></td><td>Titels en beschrijvingen per pagina, een sitemap, structuurdata en controle in Search Console. Zonder die stappen weet Google mogelijk niet welke pagina’s er zijn.</td></tr>
            <tr><td><strong>Privacy en cookies nagaan</strong></td><td>Voor tracking-cookies is toestemming nodig, voor functionele cookies niet. Welke scripts laadt de site, en waar komt een aanvraag terecht?</td></tr>
            <tr><td><strong>Onderhoud en aanspreekpunt regelen</strong></td><td>Wie wijzigt een tekst, wie bewaakt updates en bij wie meldt u een storing?</td></tr>
          </tbody>
        </table></div>
        <h3>Wat Google zegt over inhoud die met AI is gemaakt</h3>
        <p>Google sluit het niet uit. Volgens Google kan generatieve AI nuttig zijn om een onderwerp te onderzoeken en om structuur aan te brengen in eigen inhoud. Veel pagina’s maken zonder waarde voor bezoekers kan wel in strijd zijn met de spamregels. Daarom telt vooral of de inhoud juist is en bezoekers helpt.</p>
        <h3>Wanneer AI genoeg is en wanneer niet</h3>
        <p>Het is genoeg wanneer de site vooral iets toont, geen aanvragen hoeft op te leveren en u zelf tijd heeft voor de controles hierboven. Het is niet genoeg wanneer de site aanvragen moet opleveren en u iemand zoekt die verantwoordelijk is voor het geheel.</p>
        <p>Bij Complete AI is dat één persoon: Glenn van Wijngaarden bouwt de site, zet hem live en blijft uw aanspreekpunt. Wij beginnen met een gesprek over uw bedrijf, omdat de teksten daaruit voortkomen. Blijkt in de <a href="index.html#contact">intake</a> dat een eenvoudigere oplossing volstaat, dan hoort u dat ook.</p>""", "ai"),

   proza("Maatwerk of sjabloon", "Maatwerk of sjabloon: wat past bij uw bedrijf?", """        <p>Een sjabloon is een kant-en-klaar ontwerp dat u vult met eigen teksten en beeld. Maatwerk is een ontwerp dat uit uw bedrijf volgt. Beide zijn te verdedigen. De keuze hangt af van wat de site moet doen.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Onderdeel</th><th>Sjabloon</th><th>Op maat</th></tr></thead>
          <tbody>
            <tr><td><strong>Startpunt</strong></td><td>Een bestaand ontwerp waar u uw eigen inhoud in zet.</td><td>Een ontwerp dat volgt uit uw bedrijf, uw klanten en uw doel.</td></tr>
            <tr><td><strong>Uniek</strong></td><td>Hetzelfde sjabloon kan op andere sites staan.</td><td>Het ontwerp is er alleen voor uw bedrijf.</td></tr>
            <tr><td><strong>Functies</strong></td><td>Binnen wat het sjabloon biedt.</td><td>Gebouwd voor wat uw bedrijf nodig heeft, zoals online boeken.</td></tr>
            <tr><td><strong>Snelheid</strong></td><td>Hangt af van wat het sjabloon laadt. Meet het na met de tools uit de vorige sectie.</td><td>Licht gebouwd, zonder zware paginabouwers of tientallen plug-ins.</td></tr>
            <tr><td><strong>Beheer</strong></td><td>Zelf aan te passen met de editor van het systeem.</td><td>Kleine wijzigingen door ons, of zelf zonder technische kennis.</td></tr>
          </tbody>
        </table></div>
        <h3>Wanneer een sjabloon past</h3>
        <p>Wanneer u een eenvoudige site zoekt, die u zelf bijhoudt en die geen bijzondere functies vraagt, is een sjabloon een redelijke keuze. Let dan op de snelheid en op wie het onderhoud doet.</p>
        <h3>Wanneer maatwerk past</h3>
        <p>Wanneer de site zich moet onderscheiden, functies nodig heeft of snel moet blijven, past ontwerp op maat beter. Bij Complete AI is dat de norm: geen sjabloon met een logo erin.</p>
        <p>Op maat betekent bij ons dat ontwerp en teksten uw bedrijf volgen, terwijl de technische onderdelen eronder al gebouwd en getest zijn. Daardoor staat een site in één tot twee weken en niet pas na maanden bouwen.</p>""", "maatwerk"),

   proza("Uit eigen praktijk", "Deze site is de website die wij bouwen.", """        <p>Alles wat hierboven staat, is op deze site na te gaan. U hoeft niets op ons woord aan te nemen.</p>
        <h3>Wat er op deze site staat</h3>
        <ul>
          <li><strong>Statische pagina’s.</strong> Geen database en geen inlogscherm.</li>
          <li><strong>Laadtijd van ongeveer 0,7 seconde</strong>, ook op een telefoon.</li>
          <li><strong>Geen cookiebanner.</strong> De site plaatst geen tracking-cookies en gebruikt geen advertentienetwerken of analysediensten die gedrag volgen. Zie ook de <a href="privacy.html">privacyverklaring</a>.</li>
          <li><strong>Geen bestanden van derden bij het openen van een pagina.</strong> Lettertype, opmaak en script komen van dezelfde server.</li>
          <li><strong>Structuur per pagina.</strong> Elke dienstpagina heeft een eigen titel en beschrijving, één hoofdkop, een kruimelpad en structuurdata voor de pagina, het kruimelpad en de veelgestelde vragen. Alle pagina’s staan in de sitemap.</li>
          <li><strong>Eén sjabloon voor kop, navigatie en voet.</strong> Daardoor zijn ze op elke pagina gelijk. Voor publicatie loopt een controle die per pagina de titel, de kop, de canonical en de plaats in de sitemap nagaat.</li>
        </ul>
        <h3>Zelf nameten</h3>
        <p>Open deze pagina op uw telefoon, of verklein het venster op een laptop. Laat PageSpeed Insights de pagina meten, en bekijk in de bron van de pagina de structuurdata. Het certificaat in de adresbalk is geldig, zonder browserwaarschuwing. Dezelfde punten controleert u bij elke andere aanbieder.</p>
        <p>Wat wij voor Aronza, het e-commercebedrijf van de oprichter, hebben gebouwd, staat in de <a href="case-aronza.html">klantcase</a>.</p>""", "eigen-praktijk"),

   bronnen([
     ("Understanding Core Web Vitals and Google search results", "https://developers.google.com/search/docs/appearance/core-web-vitals", "Google Search Central. De drie meetwaarden en hun grenzen: LCP binnen 2,5 seconden, INP onder 200 milliseconden, CLS onder 0,1."),
     ("Web Vitals", "https://web.dev/articles/vitals", "Google, web.dev. Meting op het 75e percentiel van bezoeken, mobiel en desktop apart, en de tools waarin de waarden staan (PageSpeed Insights, Search Console)."),
     ("Understanding page experience in Google Search results", "https://developers.google.com/search/docs/appearance/page-experience", "Google Search Central. Goede Core Web Vitals garanderen geen topplaats; inhoud blijft leidend."),
     ("Mobile site and mobile-first indexing best practices", "https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing", "Google Search Central. Google gebruikt de mobiele versie voor indexering en beoordeling en raadt responsive design aan."),
     ("Learn about sitemaps", "https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview", "Google Search Central. Een sitemap helpt bij een nieuwe site met weinig externe verwijzingen."),
     ("Introduction to structured data markup in Google Search", "https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data", "Google Search Central. Wat structuurdata is en dat het alleen beschrijft wat zichtbaar is op de pagina."),
     ("Google Search’s guidance on using generative AI content on your website", "https://developers.google.com/search/docs/fundamentals/using-gen-ai-content", "Google Search Central. Generatieve AI is toegestaan; waarde voor bezoekers, juistheid en kwaliteit tellen."),
     ("Creating helpful, reliable, people-first content", "https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "Google Search Central. Inhoud met eigen ervaring en diepgang, en zonder feitelijke fouten."),
     ("Efficiently load third-party JavaScript", "https://web.dev/articles/efficiently-load-third-party-javascript", "Google, web.dev. Verwijder een script van een derde dat de pagina vertraagt zonder duidelijke waarde."),
     ("Tips to improve your local ranking on Google", "https://support.google.com/business/answer/7091", "Google Business Profile Help. Bedrijven met volledige en juiste gegevens komen eerder in lokale zoekresultaten."),
     ("Cookies", "https://www.autoriteitpersoonsgegevens.nl/themas/internet-slimme-apparaten/cookies", "Autoriteit Persoonsgegevens. Functionele cookies vragen geen toestemming, tracking-cookies wel."),
   ]),
 ]),
},

# ───────────────────────────── AUTOMATISERING ─────────────────────────────
{
 "bestand": "automatisering.html",
 "dienst": "Automatisering",
 "titel": "Bedrijfsprocessen automatiseren voor het mkb | Complete AI",
 "beschrijving": "Bedrijfsprocessen automatiseren voor het mkb: facturen, orders, afspraken en herinneringen zonder overtypen. Live binnen enkele werkdagen, met uw akkoord.",
 "omschrijving": "Automatisering van bedrijfsprocessen voor mkb-bedrijven: orderintake, facturatie, betaalherinneringen, afspraken, reviews en een dashboard met uw cijfers, gekoppeld aan boekhouding, agenda en telefonie.",
 "ogen": "Automatisering",
 "gewijzigd": "2026-09-24",
 "h1": 'Bedrijfsprocessen automatiseren: <span class="glans">terugkerend werk dat zichzelf afhandelt</span>.',
 "lead": """Bedrijfsprocessen automatiseren betekent dat software de terugkerende stappen van een proces uitvoert: een factuur opstellen, een afspraak bevestigen, een betaling opvolgen. U blijft met dezelfde systemen werken; het overtypen en het onthouden vallen weg. Complete AI richt dit in voor mkb-bedrijven in Nederland en België, koppelt het aan uw boekhouding, agenda en telefonie en heeft het binnen enkele werkdagen draaien.""",
 "levertijd": "Live binnen enkele werkdagen",
 "uitkomsten": [
     ("17", "automatiseringen die vandaag al draaien en getest zijn"),
     ("Dagen", "in plaats van maanden, omdat wij niet bij nul beginnen"),
     ("Uw akkoord", "bij alles wat naar een klant gaat, zolang u dat wilt"),
 ],
 "slot_kop": "Waar gaat uw tijd naartoe?",
 "slot_tekst": "In een half uur brengen wij in kaart waar de week in gaat zitten en welke taken de meeste uren kosten. Daar beginnen we; de rest volgt wanneer u dat wilt. U ontvangt een onderbouwd advies, ook wanneer de conclusie is dat er weinig te winnen valt.",
 "vragen": [
   ("Wat is bedrijfsprocessen automatiseren?",
    """Bedrijfsprocessen automatiseren is het laten uitvoeren van terugkerende stappen door software in plaats van door u of uw medewerkers. Denk aan een factuur die na een afgeronde order wordt opgesteld, of een herinnering bij een openstaande betaling. Welke processen zich lenen, leest u in de <a href="bedrijfsprocessen-automatiseren-voorbeelden.html">gids met voorbeelden per afdeling</a>."""),
   ("Hoe kan ik processen automatiseren?",
    """Begin met het proces dat de meeste uren kost en elke keer dezelfde stappen volgt, en automatiseer alleen dat. Laat het enkele weken draaien, controleer of de uitkomst klopt en kies dan het volgende. Bij Complete AI is dat de route van intake en voorstel naar inrichten en meekijken, zoals hierboven beschreven."""),
   ("Bedrijfsprocessen automatiseren met AI: hoe doet u dat?",
    """Gebruik AI voor de stappen waar taal in zit en vaste regels voor de rest. Een gesprek dat een bestelling wordt, of een vraag via WhatsApp, vraagt om AI; een factuur na een afgeronde order niet. Zo werkt de AI-telefonist van Complete AI. Wat naar een klant gaat, kan langs uw goedkeuring."""),
   ("Hoe kan ik automatiseren met AI?",
    """Op twee manieren: zelf, met losse AI-hulpmiddelen voor tekst en vragen, of via iemand die het aan uw systemen koppelt. Het eerste helpt bij losse taken, maar u blijft zelf de schakel tussen de systemen. Bij het tweede verloopt het werk zonder tussenkomst. Complete AI doet het tweede, met onderdelen die al draaien en getest zijn."""),
   ("Wat is het verschil tussen RPA en AI?",
    """RPA is software die handelingen op een scherm nabootst, zoals klikken en overtypen, volgens regels die vastliggen. AI herkent patronen in gegevens, ook in tekst en spraak, en kan werken met invoer die elke keer anders is. Ze vullen elkaar aan. Een vergelijking met bronnen staat in de <a href="bedrijfsprocessen-automatiseren-voorbeelden.html#regels-rpa-ai">gids over processen automatiseren</a>."""),
   ("Wat zijn voorbeelden van bedrijfsprocessen?",
    """Een offerte opvolgen, een afspraak inplannen, een factuur versturen, een order verwerken, verlof aanvragen en de voorraad bijhouden. Elk proces heeft een aanleiding, vaste stappen en een uitkomst. De gids <a href="bedrijfsprocessen-automatiseren-voorbeelden.html">Processen automatiseren: voorbeelden</a> loopt acht afdelingen door, met per proces wat er nu met de hand gebeurt en wat de automatisering overneemt."""),
   ("Moet ik mijn huidige systemen vervangen?",
    """Nee. Wij sluiten aan op wat u al gebruikt: de boekhouding, de agenda, de telefonie. Adviseren wij iets te beëindigen, dan is dat omdat het kosten veroorzaakt zonder rendement, met de onderbouwing erbij. Welke koppeling bij uw pakket past, bepalen we in de intake."""),
   ("Wat als de automatisering iets fout doet?",
    """Alles wat automatisch gebeurt is terug te zien en terug te draaien. Wij bouwen in stappen en kijken de eerste weken mee. Bij handelingen die naar buiten gaan, zoals een factuur of een bericht aan een klant, komt eerst een goedkeuringsstap tussen. Die stap kunt u later laten vervallen."""),
   ("Hoe kan het zo snel gaan als het maatwerk betreft?",
    """Omdat de onderdelen al bestaan. Het klantenbestand, de facturatie, de agenda en het omzetdashboard zijn gebouwd, getest en draaien in productie. Wij kiezen de juiste onderdelen, richten ze in met uw gegevens en koppelen ze aan elkaar. Dat kost dagen, geen maanden."""),
   ("Heb ik zelf toegang, of ben ik afhankelijk van Complete AI?",
    """U heeft zelf toegang en de gegevens blijven van u. Besluit u te stoppen, dan ontvangt u alles in een gangbaar bestandsformaat. Het abonnement is maandelijks opzegbaar. Complete AI werkt liever met klanten die blijven omdat het rendeert dan met klanten die vastzitten."""),
   ("Hoe is dit geregeld ten aanzien van klantgegevens en de AVG?",
    """Waar wij persoonsgegevens verwerken, leggen we dat vóór de start vast in een verwerkersovereenkomst, zoals de AVG voorschrijft. Uw gegevens blijven van u en worden nooit gedeeld of doorverkocht. Wat zo'n overeenkomst volgens de toezichthouder bevat, leest u bij <a href="#gegevens">veiligheid en gegevens</a>."""),
   ("Wat gebeurt er na de oplevering?",
    """Het onderhoud blijft onze verantwoordelijkheid. Eén bericht volstaat, zonder ticketsysteem, en u krijgt binnen één werkdag reactie. Kleine wijzigingen horen bij het maandbedrag. Daarnaast beoordelen we maandelijks samen de cijfers en kiest u wanneer het volgende onderdeel aan de beurt is. Het abonnement is maandelijks opzegbaar."""),
   ("Wat kost bedrijfsprocessen automatiseren?",
    """Dat hangt af van hoeveel processen u automatiseert, welke onderdelen daarvoor nodig zijn en aan welke systemen ze gekoppeld worden. Binnen één werkdag na de intake ligt er één vaste prijs op papier: eenmalig voor de bouw en een vast maandbedrag voor onderhoud en bijsturing. Er is geen nacalculatie."""),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   inhoudsopgave([
       ("korte-antwoord", "Wat bedrijfsprocessen automatiseren inhoudt"),
       ("ai-of-regels", "Wanneer AI, wanneer een vaste regel"),
       ("herkenbaar", "Herkent u dit?"),
       ("voorbeeld-order", "Eén order van telefoon tot beoordeling"),
       ("wat-er-kan", "Wat vandaag al draait"),
       ("werkwijze", "Hoe een traject verloopt"),
       ("intake", "Wat we in de intake bespreken"),
       ("koppelingen", "Waarmee het koppelt"),
       ("controle", "Wat vanzelf verloopt en wat bij u blijft"),
       ("gegevens", "Veiligheid en gegevens"),
       ("voor-wie", "Voor wie het past"),
       ("eigen-praktijk", "Uit eigen praktijk"),
   ]),

   proza("Het korte antwoord", "Wat houdt bedrijfsprocessen automatiseren in?",
         """        <p>Een bedrijfsproces is een ordening van activiteiten waarmee een bedrijf een product of dienst levert die voor de klant waarde heeft (zie <a href="https://nl.wikipedia.org/wiki/Bedrijfsproces" rel="noopener" target="_blank">Wikipedia</a>). Een order verwerken, een offerte opvolgen en een factuur versturen zijn drie voorbeelden. Elk heeft een begin, een vaste volgorde en een uitkomst.</p>
        <p>Bedrijfsprocessen automatiseren is het laten uitvoeren van die stappen door software, zodat niemand ze nog met de hand doet. Niet elk proces en niet elke stap komt daarvoor in aanmerking. Drie kenmerken wijzen het aan: het proces komt terug, de volgorde staat vast en u kunt de uitkomst controleren. Welke processen dat in een mkb-bedrijf zijn, staat per afdeling in de gids <a href="bedrijfsprocessen-automatiseren-voorbeelden.html">Processen automatiseren: voorbeelden</a>.</p>
        <p>Deze pagina gaat over de andere kant: wat Complete AI voor u inricht, hoe een traject verloopt, waaraan het koppelt en wat u zelf in de hand houdt.</p>""",
         "korte-antwoord"),

   proza("Techniek", "Bedrijfsprocessen automatiseren met AI: wanneer is AI nodig?",
         """        <p>AI is niet voor elke stap nodig, en dat is een voordeel. Waar de uitkomst elke keer hetzelfde hoort te zijn, is een vaste regel betrouwbaarder en beter te controleren dan een model dat een inschatting maakt. Een factuur die volgt op een afgeronde order is zo&#8217;n stap.</p>
        <p>AI komt in beeld waar taal en variatie een rol spelen: een telefoongesprek dat een bestelling wordt, een vraag die via WhatsApp binnenkomt. De <a href="ai-telefonist.html">AI-telefonist</a> is daar het voorbeeld van. Hij verstaat wat de beller vraagt en zet de bestelling daarna gestructureerd in de orderlijst.</p>
        <p>Het verschil tussen een vaste regel, RPA en AI, met bronnen en voorbeelden, staat in de gids <a href="bedrijfsprocessen-automatiseren-voorbeelden.html#regels-rpa-ai">Processen automatiseren: voorbeelden</a>. Wat AI in een klein bedrijf verder concreet doet, leest u in <a href="ai-voor-uw-bedrijf.html">AI in uw bedrijf</a>.</p>""",
         "ai-of-regels"),

   sectie("De situatie", "Werk dat moet gebeuren maar geen omzet oplevert.",
          "Vier situaties die wij bij ondernemers terugzien.",
          pijnblok([
            ("De administratie schuift naar de avond", "Als de zaak gesloten is en de werkdag er feitelijk op zit. Elke week opnieuw."),
            ("Bestellingen komen via alle kanalen binnen", "Telefoon, WhatsApp, e-mail en eventueel de webshop. De ondernemer is de plek waar het samenkomt."),
            ("Openstaande facturen blijven liggen", "Herinneren voelt ongemakkelijk, dus het wordt uitgesteld, en het geld komt later binnen."),
            ("Reviews worden niet gevraagd", "Er is simpelweg geen moment voor, terwijl beoordelingen nieuwe klanten helpen kiezen."),
          ]), "herkenbaar"),

   proza("Een voorbeeld", "Hoe ziet een geautomatiseerd proces eruit? Eén order als voorbeeld.",
         """        <p>Een proces is een keten van stappen. Het volgende voorbeeld toont hoe één bestelling door vier processen loopt, zonder dat iemand iets overtypt.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Moment en proces</th><th>Wat er gebeurt</th></tr></thead>
          <tbody>
            <tr><td><strong>22:41 &middot; Telefoon</strong></td><td>Een klant belt na sluitingstijd. De AI-telefonist neemt op en noteert de bestelling.</td></tr>
            <tr><td><strong>22:41 &middot; Order</strong></td><td>De bestelling staat in de centrale orderlijst.</td></tr>
            <tr><td><strong>22:42 &middot; Klantcontact</strong></td><td>De klant ontvangt een bevestiging.</td></tr>
            <tr><td><strong>05:30 &middot; Voorbereiding</strong></td><td>De pak- en laadlijst staat klaar.</td></tr>
            <tr><td><strong>16:10 &middot; Levering en factuur</strong></td><td>Na de levering wordt de factuur aangemaakt en geboekt.</td></tr>
            <tr><td><strong>18:00 &middot; Review</strong></td><td>De klant krijgt automatisch een verzoek om een beoordeling.</td></tr>
          </tbody>
        </table></div>
        <p>Dit is een voorbeeld en geen beschrijving van een bepaalde klant. Het laat zien waar de winst zit: de stappen werken op dezelfde gegevens. Heeft u een goedkeuringsstap ingesteld, dan gaan de factuur en het bericht pas de deur uit na uw akkoord, zoals beschreven bij <a href="#controle">wat vanzelf verloopt en wat bij u blijft</a>.</p>""",
         "voorbeeld-order"),

   sectie("Wat er kan", "Welke automatiseringen draaien vandaag al?",
          "Dit zijn geen plannen of ontwerpen. Het is software die bestaat, getest is en in productie draait: in totaal 17 automatiseringen. Samen bepalen we welke onderdelen in uw situatie zinvol zijn.",
          voorbeeldblok([
            ("Facturatie en betaalherinneringen", "Facturen maken en versturen, en trage betalers krijgen automatisch een vriendelijke herinnering die oploopt."),
            ("Offertes maken en opvolgen", "Offertes opstellen, versturen en zien wie er nog niet gereageerd heeft."),
            ("Klantenbestand", "Contactgegevens, historie en notities per klant. Geen losse notities en geen zoekwerk meer."),
            ("Online laten boeken", "Klanten plannen zelf een afspraak via een link, rechtstreeks in uw agenda."),
            ("Afspraakherinneringen", "Automatisch een bericht vóór de afspraak, zodat niemand de afspraak nog vergeet."),
            ("Terugkomberichten", "Een bericht zodra het tijd is voor een nieuwe afspraak. Genereert omzet zonder dat u hoeft te bellen."),
            ("Reviews verzamelen", "Na een geslaagde levering automatisch om een beoordeling vragen en die op de site tonen."),
            ("Omzetdashboard", "Omzet per dag, week of maand in duidelijke grafieken. Beslissen op cijfers in plaats van gevoel."),
            ("Kosten en btw", "Uitgaven op één plek, per categorie gerubriceerd, en de btw per kwartaal gereed voor de aangifte."),
            ("Winst, verlies en kasstroom", "Inzicht in wat er overblijft en of de liquiditeit de komende maanden onder druk komt."),
            ("Betaallinks", "Klanten rekenen direct online af via iDEAL, zonder handmatige overschrijvingen."),
            ("WhatsApp-assistent", "Automatische antwoorden op veelgestelde vragen, ook buiten openingstijden."),
          ]), "wat-er-kan"),

   sectie("Werkwijze", "Hoe een traject verloopt: van intake tot draaiend.",
          "Vijf stappen. Voor de eerste hoeft u niets voor te bereiden, en na het voorstel bepaalt u zelf of en hoe ver u gaat.",
          routeblok([
            ("Intake", "Een half uur, kosteloos en vrijblijvend. We stellen vast waar de week in gaat zitten en welke systemen u gebruikt. Daar beginnen we, nooit bij alles tegelijk."),
            ("Voorstel", "Binnen één werkdag op papier: welke onderdelen wij inzetten, wat er automatisch verloopt en wanneer het staat. Eén vaste prijs, geen nacalculatie."),
            ("Inrichten", "Wij richten de onderdelen in met uw gegevens, uw huisstijl en uw werkwijze en koppelen ze aan de boekhouding, agenda of telefonie die u al gebruikt. Dagen, geen maanden."),
            ("Meekijken", "De eerste weken kijken wij mee en sturen we bij. Wat naar een klant gaat, ziet u eerst. Alles wat automatisch gebeurt is terug te zien en terug te draaien."),
            ("Uitbreiden", "Draait het eerste onderdeel, dan kiest u het volgende. Elke fase levert op zichzelf resultaat op en u bepaalt wanneer de volgende volgt."),
          ]), "werkwijze"),

   proza("De intake", "Wat bespreken we in de intake?",
         """        <p>Voorbereiding is niet nodig. De intake duurt een half uur, kost niets en verplicht tot niets. We lopen vier vragen door.</p>
        <ol>
          <li><strong>Welke taken komen elke week terug, en wie doet ze?</strong> Zo zien we waar de uren zitten.</li>
          <li><strong>Welke systemen gebruikt u al?</strong> De boekhouding, de agenda, de telefonie en de manier waarop klanten u betalen.</li>
          <li><strong>Waar gaat het mis?</strong> Dubbel invoeren, vergeten op te volgen, betalingen die te laat binnenkomen.</li>
          <li><strong>Wat mag nooit zonder uw akkoord de deur uit?</strong> Daar komt een goedkeuringsstap.</li>
        </ol>
        <p>U ontvangt daarna binnen één werkdag een voorstel met één vaste prijs. Blijkt dat er weinig te winnen valt, dan hoort u dat ook. Wilt u zelf alvast nagaan waar uw tijd heen gaat, dan staat in de gids <a href="bedrijfsprocessen-automatiseren-voorbeelden.html#tijd-opnemen">hoe u vooraf een week opneemt</a>.</p>
        <h3>Wat vraagt het van u?</h3>
        <p>Een half uur voor de intake, uw akkoord op het voorstel en in de eerste weken uw goedkeuring op wat naar klanten gaat. Het inrichten doen wij. Na de oplevering blijft het onderhoud onze verantwoordelijkheid: één bericht volstaat, zonder ticketsysteem.</p>""",
         "intake"),

   sectie("Koppelingen", "Waarmee koppelt het?",
          "Wij vervangen uw systemen niet, wij sluiten aan op wat u gebruikt. Welke koppeling bij uw pakket past, bepalen we in de intake.",
          voorbeeldblok([
            ("Boekhouding", "Facturen worden opgesteld en verstuurd op basis van de order. Uitgaven worden vastgelegd en per categorie geordend, en de btw per kwartaal staat klaar voor de aangifte."),
            ("Agenda", "Klanten kiezen zelf een moment via een link en de afspraak staat in uw agenda. Een herinnering gaat vóór de afspraak automatisch uit."),
            ("Telefonie", """De AI-telefonist neemt op buiten openingstijden en tijdens drukte, noteert bestellingen en vragen en plant in via de agenda-koppeling. <a href="ai-telefonist.html">Alles over de AI-telefonist</a>."""),
            ("Betalen", "Klanten rekenen direct online af via iDEAL, of betalen vooraf een deel. Trage betalers krijgen automatisch een herinnering die oploopt."),
            ("WhatsApp", "Veelgestelde vragen worden automatisch beantwoord, ook buiten openingstijden."),
            ("Dashboard", "Omzet, kosten, winst en kasstroom uit dezelfde gegevens, samengebracht op één scherm."),
          ]), "koppelingen"),

   proza("Controle", "Wat verloopt vanzelf en waar houdt u de controle?",
         """        <p>Automatiseren betekent niet dat u niets meer ziet. U bepaalt per handeling hoeveel u zelf wilt zien voordat het gebeurt.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Soort handeling</th><th>Zo verloopt het, en uw controle</th></tr></thead>
          <tbody>
            <tr><td><strong>Binnen uw administratie.</strong> Een order raakt de voorraad, de factuur en het klantdossier; een uitgave wordt vastgelegd.</td><td>Het verloopt zonder tussenkomst en zonder overtypen. Alles is terug te zien en terug te draaien.</td></tr>
            <tr><td><strong>Naar buiten.</strong> Een factuur, een betaalherinnering, een bericht aan een klant.</td><td>Het wordt klaargezet volgens uw afspraken. Eerst komt een goedkeuringsstap, die later kan vervallen.</td></tr>
            <tr><td><strong>Beslissingen.</strong> De prijs van een offerte, een uitzondering, een kwestie met een klant.</td><td>Het blijft een menselijke afweging, bij u. De automatisering bereidt voor.</td></tr>
          </tbody>
        </table></div>
        <h3>Waarom de goedkeuringsstap vooraan staat</h3>
        <p>Een factuur of bericht dat is verstuurd, haalt u niet terug. Daarom ziet u in de eerste weken eerst wat er de deur uit gaat, en kijken wij mee. Klopt alles, en merkt u dat u telkens zonder aanpassing akkoord geeft, dan kan die stap vervallen. Dat kiest u zelf, per handeling.</p>
        <h3>Wat als er iets misgaat?</h3>
        <p>Elke automatische handeling is terug te zien en terug te draaien. We bouwen in stappen, zodat een fout in het eerste onderdeel zichtbaar wordt voordat het tweede erop voortbouwt. Bij Aronza is er sinds de ingebruikname begin mei 2026 geen storing geweest. Dat is een aanwijzing, geen garantie voor de toekomst.</p>""",
         "controle"),

   proza("Veiligheid en gegevens", "Hoe zijn uw gegevens geregeld?",
         """        <p>Automatiseren betekent dat gegevens door software lopen: namen, adressen, bestellingen, facturen. De AVG bepaalt wie daarvoor verantwoordelijk is en wat er schriftelijk moet worden vastgelegd.</p>
        <h3>Wie is waarvoor verantwoordelijk?</h3>
        <p>Volgens de <a href="https://autoriteitpersoonsgegevens.nl/nl/onderwerpen/algemene-informatie-avg/verantwoordelijke-en-verwerker" rel="noopener" target="_blank">Autoriteit Persoonsgegevens</a> is de organisatie die een andere partij inschakelt de verwerkingsverantwoordelijke. De partij die de gegevens alleen in opdracht verwerkt, is de verwerker. Voor de gegevens van uw klanten bent u dus zelf verantwoordelijk, en Complete AI verwerkt ze op uw instructies.</p>
        <h3>Een verwerkersovereenkomst vóór de start</h3>
        <p>De AVG schrijft voor dat verantwoordelijke en verwerker hun afspraken schriftelijk vastleggen (artikel 28, lid 3). Ontbreekt die overeenkomst, dan zijn beide partijen daarvoor aansprakelijk, schrijft de <a href="https://www.autoriteitpersoonsgegevens.nl/en/themes/basic-gdpr/gdpr-basics/processing-agreement" rel="noopener" target="_blank">Autoriteit Persoonsgegevens</a> (Engelstalige pagina). Wij regelen dat vóór de start, niet achteraf. Volgens de toezichthouder staan daar onder meer in:</p>
        <ul>
          <li>waarvoor de gegevens worden verwerkt, hoelang, en om welke soort gegevens het gaat;</li>
          <li>dat de verwerker alleen op uw schriftelijke instructies werkt en de gegevens niet voor eigen doelen gebruikt;</li>
          <li>geheimhouding en passende beveiliging;</li>
          <li>dat een andere partij alleen met uw voorafgaande schriftelijke toestemming wordt ingeschakeld;</li>
          <li>hulp bij vragen van betrokkenen en bij datalekken;</li>
          <li>dat de gegevens na afloop worden verwijderd of aan u teruggegeven.</li>
        </ul>
        <h3>Uw gegevens blijven van u</h3>
        <p>Uw gegevens worden nooit gedeeld of doorverkocht. U heeft zelf toegang. Besluit u te stoppen, dan ontvangt u alles in een gangbaar bestandsformaat. Het abonnement is maandelijks opzegbaar, zodat niets u aan Complete AI bindt behalve dat het rendeert.</p>""",
         "gegevens"),

   sectie("Voor wie", "Voor wie past dit?",
          "Het gaat om het soort bedrijf, niet om de branche: vakmensen aan het roer die zich met hun vak bezig willen houden. Dit zijn de bedrijven waarvoor wij het inrichten.",
          voorbeeldblok([
            ("Kapsalons", """Afspraken, herinneringen tegen no-shows en reviews die vanzelf binnenkomen. <a href="ai-voor-kapsalons.html">AI voor kapsalons</a>."""),
            ("Garagebedrijven", """APK-herinneringen, een statusbericht bij gereed en de factuur direct na de werkorder. <a href="ai-voor-garagebedrijven.html">AI voor garagebedrijven</a>."""),
            ("Horeca", """Online reserveren, bevestiging en herinnering, en reviews. <a href="ai-voor-de-horeca.html">AI voor de horeca</a>."""),
            ("Bouw en installatie", """Aanvragen vastleggen tijdens het werk, offerte-concepten, urenregistratie en facturatie. <a href="ai-voor-bouw-en-installatie.html">AI voor bouw en installatie</a>."""),
            ("Webshops en handel", """Order, voorraad, factuur en klantcontact als één keten, zoals bij Aronza. <a href="case-aronza.html">De klantcase</a>."""),
            ("Praktijken en zzp&#8217;ers", "Online boeken, afspraakherinneringen, facturatie en betaalherinneringen."),
          ]) + "\n" + eerlijkblok(
            "Wanneer automatiseren niet de eerste stap is",
            "Drie situaties waarin u eerst iets anders doet:",
            ["Het proces vraagt bij elke uitvoering een eigen afweging. Dat laat u bij uzelf; automatiseer de stappen eromheen.",
             "Niemand kan het proces uitleggen. Leg dan eerst vast wie wat doet en wanneer een stap klaar is.",
             "Het proces komt een paar keer per jaar voor. Het verdient zich dan langzaam terug; begin bij wat wekelijks terugkomt."]),
          "voor-wie"),

   sectie("Uit eigen praktijk", "Vijf processen als één keten, in een bedrijf dat dagelijks draait.",
          """Bij Aronza, het e-commercebedrijf van de oprichter van Complete AI, zijn facturatie, kostenregistratie, orderverwerking, voorraadbeheer en klantcontact geautomatiseerd. Ze draaien sinds begin mei 2026. <a href="case-aronza.html">De volledige klantcase leest u hier</a>.""",
          voorbeeldblok([
            ("Van vier tot zes uur naar nul", "De administratie kostte vier tot zes uur per week, buiten werktijd. Sinds de ingebruikname is dat nul."),
            ("Het werk verschuift naar de dag", "De administratie hoeft niet meer &#8217;s avonds te worden ingehaald. Dat scheelt in de praktijk meer dan de uren zelf."),
            ("Geld komt eerder binnen", "Openstaande facturen worden consequent opgevolgd, ook wanneer dat ongemakkelijk voelt. Een systeem houdt dat beter vol dan een mens."),
            ("Cijfers zijn actueel", "Kosten en omzet worden bij binnenkomst geregistreerd. Het beeld is op elk moment actueel in plaats van pas na de kwartaalafsluiting."),
            ("Geen storing sinds de ingebruikname", "Dat is geen garantie voor de toekomst. Daarom is elke automatische handeling terug te zien en terug te draaien."),
            ("Waarom dit voor u telt", "Dat automatiseringen bij u binnen enkele werkdagen kunnen staan, komt doordat ze hier al gebouwd, getest en in productie genomen zijn."),
          ]), "eigen-praktijk"),

   bronnen([
       ("Autoriteit Persoonsgegevens: verantwoordelijke en verwerker",
        "https://autoriteitpersoonsgegevens.nl/nl/onderwerpen/algemene-informatie-avg/verantwoordelijke-en-verwerker",
        "Wie verwerkingsverantwoordelijke is, wie verwerker, en dat een verwerkersovereenkomst verplicht is."),
       ("Autoriteit Persoonsgegevens: processing agreement (Engelstalig)",
        "https://www.autoriteitpersoonsgegevens.nl/en/themes/basic-gdpr/gdpr-basics/processing-agreement",
        "Wat er volgens artikel 28 AVG in een verwerkersovereenkomst staat."),
       ("Wikipedia: Bedrijfsproces",
        "https://nl.wikipedia.org/wiki/Bedrijfsproces",
        "Definitie van een bedrijfsproces en het verschil met een project."),
   ]),
 ]),
},

# ───────────────────────────── AI-TELEFONIST ─────────────────────────────
{
 "bestand": "ai-telefonist.html",
 "dienst": "AI-telefonist",
 "titel": "AI-telefonist: zo werkt het en wat de wet eist | Complete AI",
 "beschrijving": "Wat een AI-telefonist is, hoe een gesprek verloopt, wat hij overneemt van een receptionist en wat de AI-verordening sinds 2 augustus 2026 vraagt.",
 "omschrijving": "Nederlandstalige AI-telefonist die gesprekken aanneemt, bestellingen noteert, vragen beantwoordt, urgente gesprekken doorschakelt en verkopers eruit filtert.",
 "ogen": "AI-telefonist",
 "h1": 'De <span class="glans">AI-telefonist</span> die opneemt wanneer u dat niet kunt.',
 "lead": "Een AI-telefonist is software die uw telefoon aanneemt, in gewoon Nederlands met de beller praat en vastlegt wat die nodig heeft. Andere namen zijn AI-receptionist en telefoonassistent. Complete AI richt hem in op uw eigen nummer: hij neemt op buiten openingstijden en tijdens drukte, noteert bestellingen en vragen, filtert verkopers eruit en schakelt urgente gesprekken door.",
 "levertijd": "Operationeel binnen 2 weken",
 "gewijzigd": "2026-09-24",
 "uitkomsten": [
     ("24/7", "bereikbaar, ook in het weekend en op feestdagen"),
     ("2 wk", "van akkoord tot een werkende telefonist op uw nummer"),
     ("100%", "van de gesprekken vastgelegd met een transcript"),
 ],
 "slot_kop": "Hoeveel telefoontjes blijven er nu liggen?",
 "slot_tekst": "Een gemist telefoontje laat geen spoor achter, dus wat er nu blijft liggen is onbekend. In een half uur rekenen wij het door: hoe vaak gaat de telefoon op momenten dat er niemand kan opnemen, en wat vertegenwoordigt zo'n gesprek gemiddeld aan omzet. Daarna weet u ook wat hij voor u zou afhandelen en wat naar u doorgaat.",
 "vragen": [
   ("Wat is een AI-telefoonassistent?",
    "Een AI-telefoonassistent is software die een inkomend telefoongesprek aanneemt en zelf voert. Hij verstaat de beller, antwoordt in gewone taal en legt vast wat er nodig is: een bestelling, een afspraak of een terugbelnotitie. Andere namen zijn AI-telefonist en AI-receptionist. Bij voicemail blijft de beller met zijn vraag zitten, hier krijgt hij direct een antwoord."),
   ("Hoeveel kost een AI-telefonist of AI-agent?",
    "Dat hangt af van wat de telefonist afhandelt: alleen opnemen en noteren, of ook bestellingen, afspraken en koppelingen. Een bedrag vooraf zou voor het ene bedrijf te hoog zijn en voor het andere te laag. Bij Complete AI ligt er na de intake één vaste prijs op papier: eenmalig voor de bouw en een vast maandbedrag, zonder nacalculatie."),
   ("Is er een AI-receptionist in Nederland?",
    """Ja. De <a href="https://nos.nl/artikel/2625224-geen-twijfel-ai-telefonist-moet-zich-voortaan-direct-prijsgeven" rel="noopener" target="_blank">NOS</a> meldde op 2 augustus 2026 dat AI-receptionisten steeds vaker telefoons aannemen, onder meer bij een tandartspraktijk. Complete AI levert in Nederland en België een Nederlandstalige AI-telefonist voor het mkb, ook in het Vlaams, Frans en Engels waar dat nodig is."""),
   ("Moet een AI-telefonist zeggen dat hij een AI is?",
    """Ja, sinds 2 augustus 2026. Artikel 50 van de AI-verordening bepaalt dat AI-systemen die met mensen communiceren zo zijn ontworpen dat die mensen weten dat zij met een AI-systeem praten, uiterlijk bij het eerste contact. Dat hoeft niet als het voor een redelijk oplettend persoon al duidelijk is. <a href="#de-wet">De sectie over de wet</a> geeft de bronnen."""),
   ("Hoort een beller dat het geen mens is?",
    "Ja. De telefonist meldt zich als de digitale assistent van het bedrijf en doet zich niet anders voor. Dat werkt in de praktijk beter dan verhullen: bellers accepteren het zolang zij snel en correct worden geholpen. Hoe het gesprek begint, staat in het gespreksverloop op deze pagina."),
   ("Wat als hij een vraag niet weet?",
    "Dan verzint hij niets. Hij geeft aan het na te vragen en zet een terugbelnotitie klaar met de gestelde vraag, zodat niemand hoeft te raden wat de beller bedoelde. U bepaalt vooraf welke onderwerpen hij zelfstandig afhandelt en bij welke hij altijd doorschakelt."),
   ("Welke talen spreekt hij?",
    "Nederlands is de basis, en waar dat nodig is spreekt hij ook Vlaams, Frans en Engels. Welke talen voor uw bedrijf nodig zijn, hangt af van wie er belt: een bedrijf met klanten in Nederland en België heeft daar meer aan dan een bedrijf met alleen Nederlandse klanten."),
   ("Worden gesprekken vastgelegd, en hoe verhoudt zich dat tot de AVG?",
    "Van elk gesprek is een transcript beschikbaar, zodat terug te lezen is wat er gezegd is. Omdat daarbij persoonsgegevens van uw klanten worden verwerkt, leggen wij dat vóór de start vast in een verwerkersovereenkomst en informeert u uw bellers hierover. Daar ondersteunen wij u bij."),
   ("Vervangt dit mijn telefonische bezetting of ander personeel?",
    "Nee. Hij vangt op wat anders zou blijven liggen: de avonden, het weekend en de momenten dat er niemand kan opnemen. Urgente en complexe gesprekken gaan naar u door. Het gaat om de telefoontjes die nu verloren gaan, niet om de gesprekken die nu goed verlopen."),
   ("Kan ik mijn eigen telefoonnummer houden?",
    "Ja, hij werkt op uw eigen nummer. Hij neemt op buiten openingstijden en tijdens drukte. In de eerste fase draait hij naast de bestaande lijn, zodat u hoort hoe hij functioneert zonder risico. Daarna luisteren wij de eerste weken mee en scherpen we aan waar nodig."),
   ("Wat is het verschil met een antwoordservice?",
    """Een antwoordservice laat medewerkers van een externe dienst namens u opnemen, een AI-telefonist doet dat met software. Een medewerker voelt aan wat er speelt. De AI-telefonist neemt op elk uur op, legt elk gesprek gestructureerd vast en werkt met wat u vooraf hebt ingesteld. <a href="#vergelijking">De tabel</a> zet het per onderdeel naast elkaar."""),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   inhoudsopgave([
     ("wat-is-het", "Wat is een AI-telefonist?"),
     ("herkenbaar", "Waarom bedrijven de telefoon laten opnemen"),
     ("zo-klinkt-het", "Een gesprek, stap voor stap"),
     ("vergelijking", "Telefoon beantwoorden uitbesteden: de drie routes"),
     ("agenda-doorschakelen", "Agenda en doorschakelen"),
     ("branches", "Voor welke bedrijven"),
     ("eigen-praktijk", "Na het gesprek: uit eigen praktijk"),
     ("veiligheid-avg", "Veiligheid en AVG"),
     ("de-wet", "De AI-verordening en artikel 50"),
     ("werkwijze", "Werkwijze"),
     ("controle", "Controleren of het klopt"),
     ("kosten", "Wat het kost"),
     ("bronnen", "Bronnen"),
   ]),

   proza("Uitleg", "Wat is een AI-telefonist of AI-telefoonassistent?",
         """        <h3>Een gesprek in plaats van een keuzemenu</h3>
        <p>Een AI-telefonist verstaat wat een beller zegt, bepaalt wat er gevraagd wordt en antwoordt in gesproken Nederlands. Aan het eind van het gesprek staat vast wat er is afgesproken: een bestelling in de orderlijst, een terugbelnotitie met de vraag erin, of een gesprek dat naar u is doorgeschakeld. Bij voicemail blijft de beller met zijn vraag zitten. Bij de AI-telefonist krijgt hij een antwoord of een bevestiging.</p>

        <h3>Wat doet AI op de telefoon van een bedrijf?</h3>
        <p>Op een bedrijfslijn neemt AI het gesprek aan en doet wat u vooraf hebt vastgelegd. Hij neemt bestellingen en vragen op, beantwoordt vragen over levering en assortiment, filtert verkopers eruit en schakelt urgente gesprekken naar u door. Wat hij niet kan beantwoorden, legt hij vast in een terugbelnotitie.</p>

        <h3>Eén dienst, meerdere namen</h3>
        <p>AI-telefonist, AI-receptionist, telefoonassistent en digitale telefoniste beschrijven in de praktijk hetzelfde: een assistent die de telefoon aanneemt zonder dat een medewerker vrij hoeft te zijn. Op deze pagina heet hij AI-telefonist.</p>

        <h3>AI-receptionist in Nederland: wordt het al gebruikt?</h3>
        <p>Ja. <a href="https://nos.nl/artikel/2625224-geen-twijfel-ai-telefonist-moet-zich-voortaan-direct-prijsgeven" rel="noopener" target="_blank">De NOS</a> meldde op 2 augustus 2026 dat AI-receptionisten steeds vaker worden ingezet om telefoons aan te nemen, bijvoorbeeld door een tandartspraktijk met een tekort aan baliemedewerkers. Zoekt u een AI-receptionist in Nederland of België, dan is dit dezelfde dienst, in het Nederlands en waar nodig ook in het Vlaams, Frans en Engels. Over de regels waaraan dit sinds 2 augustus is gebonden, gaat <a href="#de-wet">de sectie over de AI-verordening</a>.</p>""",
         "wat-is-het",
         "Software die een telefoongesprek voert, in plaats van een keuzemenu of een voicemail."),

   sectie("De situatie", "Waarom bedrijven de telefoon laten opnemen door een ander.",
          "Elk telefoontje dat blijft liggen, is een klant die verder zoekt.",
          pijnblok([
            ("Opnemen onderbreekt het werk", "Opnemen betekent stoppen waar u mee bezig bent. Niet opnemen betekent mogelijk een order mislopen."),
            ("Na sluitingstijd is er niemand", "Terwijl juist dan gebeld wordt: laat op de avond, of vroeg in de ochtend voor aanvang van de dag."),
            ("Verkopers kosten tijd", "Wekelijks terugkerende gesprekken over zonnepanelen, energiecontracten en abonnementen."),
            ("Het verlies is onzichtbaar", "Een gemist telefoontje laat geen spoor achter. Merkbaar is alleen dat het rustiger is dan verwacht."),
          ]), "herkenbaar"),

   sectie("Gespreksverloop", "Een gesprek om 22:41, stap voor stap.",
          "Een voorbeeld van het patroon dat zich bij elk gesprek herhaalt.",
          """      <div class="uitgelicht reveal">
        <div class="tijdlijn">
          <div class="beurt hoogte"><span class="klok">22:41</span><span class="tekst">Een klant belt ruim na sluitingstijd. <b>De telefonist neemt op</b>, in het Nederlands, en meldt zich als de digitale assistent van het bedrijf.</span></div>
          <div class="beurt"><span class="klok">22:42</span><span class="tekst">Hij noteert wat er besteld wordt, controleert wat er mogelijk is en <b>beantwoordt vragen over levering</b> en assortiment.</span></div>
          <div class="beurt"><span class="klok">22:43</span><span class="tekst">Weet hij iets niet? Dan verzint hij niets, maar <b>zet hij een terugbelnotitie klaar</b> met de vraag erin.</span></div>
          <div class="beurt"><span class="klok">22:43</span><span class="tekst">Is het dringend of complex? Dan <b>schakelt hij naar u door</b>. Wat als dringend geldt, bepaalt u vooraf.</span></div>
          <div class="beurt hoogte"><span class="klok">22:44</span><span class="tekst">De order staat gestructureerd in de lijst, de klant heeft een bevestiging, en <b>er was geen handeling van u nodig</b>.</span></div>
          <div class="beurt"><span class="klok">morgen</span><span class="tekst">Een verkoper aan de lijn? <b>Die wordt eruit gefilterd</b> — u merkt er niets van, maar het gesprek is wel terug te lezen.</span></div>
        </div>
        <div class="kunde">
          <div><b>Nederlands</b><small>Ook Vlaams, Frans en Engels waar dat nodig is</small></div>
          <div><b>24 uur per dag</b><small>Weekend, feestdagen en midden in de drukte</small></div>
          <div><b>Altijd vastgelegd</b><small>Volledig transcript bij elk gesprek</small></div>
          <div><b>U houdt de regie</b><small>U bepaalt wat hij zelfstandig afhandelt en wat naar u doorgaat</small></div>
        </div>
      </div>""", "zo-klinkt-het"),

   proza("Vergelijking", "Telefoon beantwoorden uitbesteden: wat neemt de AI-telefonist over?",
         """        <div class="tabelwrap"><table>
          <thead><tr><th>Onderdeel</th><th>Receptionist</th><th>Antwoordservice</th><th>AI-telefonist</th></tr></thead>
          <tbody>
            <tr><td>Wie neemt op</td><td>Een eigen medewerker die uw bedrijf en uw klanten kent</td><td>Een medewerker van een externe dienst, die volgens uw afspraken opneemt</td><td>Software, ingericht met uw assortiment, levertijden en toon</td></tr>
            <tr><td>Beschikbaarheid</td><td>Binnen de werktijden van de medewerker, met vakantie en ziekte als onderbreking</td><td>Binnen de uren die u met de dienst afspreekt</td><td>Op elk uur, ook 's avonds, in het weekend en op feestdagen</td></tr>
            <tr><td>Tijdens drukte</td><td>Eén medewerker voert één gesprek tegelijk</td><td>Hangt af van de bezetting van de dienst</td><td>Neemt op wanneer u en uw team bezet zijn</td></tr>
            <tr><td>Gevoelige of complexe gesprekken</td><td>De medewerker beoordeelt en voelt aan wat er speelt</td><td>De medewerker werkt volgens de afspraken die u hebt vastgelegd</td><td>Wat u vooraf als dringend of complex aanmerkt, gaat naar u door</td></tr>
            <tr><td>Na het gesprek</td><td>De medewerker handelt af of draagt over</td><td>Een bericht of een doorverbinding</td><td>Een bestelling in de lijst, een terugbelnotitie met volledig transcript of een doorgeschakeld gesprek</td></tr>
            <tr><td>Talen</td><td>De talen die de medewerker spreekt</td><td>De talen die de dienst aanbiedt</td><td>Nederlands, en waar nodig Vlaams, Frans en Engels</td></tr>
            <tr><td>Agenda</td><td>De medewerker werkt in uw agenda</td><td>Verschilt per aanbieder</td><td>Via een agenda-koppeling</td></tr>
            <tr><td>Waar de kosten van afhangen</td><td>De loonkosten en de uren waarop de receptie bemand is</td><td>Het aantal gesprekken en de afspraken met de dienst</td><td>De inrichting en een vast maandbedrag: één vaste prijs na de intake</td></tr>
          </tbody>
        </table></div>

        <h3>Wat bij u en uw team blijft</h3>
        <ul>
          <li><strong>Gesprekken die dringend of complex zijn.</strong> U bepaalt vooraf wat daaronder valt. Die gesprekken gaan naar u door.</li>
          <li><strong>De grens van wat hij zelfstandig afhandelt.</strong> U bepaalt vooraf welke onderwerpen hij afhandelt en bij welke hij altijd doorschakelt.</li>
          <li><strong>Het terugbellen na een vraag die hij niet kon beantwoorden.</strong> Hij verzint niets en legt de vraag vast.</li>
          <li><strong>Het werk aan de balie.</strong> Een receptionist ontvangt ook bezoekers en houdt de balie bij. De AI-telefonist neemt het telefoonwerk over en werkt daarom naast een receptionist: hij neemt op wanneer zij er niet is of de lijn bezet is.</li>
        </ul>

        <h3>Welke route past bij welk bedrijf?</h3>
        <ul>
          <li>Een <strong>receptionist</strong> past bij een bedrijf met een balie en bezoekers, waar de telefoon één van meerdere taken is.</li>
          <li>Een <strong>antwoordservice</strong> past bij wie mensen aan de lijn wil zonder eigen personeel, en de gesprekken volgens vaste afspraken laat afhandelen.</li>
          <li>Een <strong>AI-telefonist</strong> past bij wie de telefoon buiten openingstijden en tijdens drukte wil laten opnemen, en wil dat wat er besteld of gevraagd wordt direct gestructureerd binnenkomt.</li>
        </ul>
        <p>De routes sluiten elkaar niet uit: een receptionist kan overdag opnemen en de AI-telefonist buiten openingstijden en tijdens drukte. Wat er met een bestelling of vraag daarna gebeurt, leest u bij <a href="automatisering.html">automatisering</a>.</p>""",
         "vergelijking",
         "Wie de telefoon wil laten beantwoorden, kiest uit drie routes: een receptionist, een antwoordservice of een AI-telefonist. De tabel vergelijkt ze op wat in de praktijk verschil maakt. Er staan geen bedragen in: wat u bij elke route betaalt, hangt af van de afspraken die u maakt."),

   proza("Agenda en doorschakelen", "Afspraken in uw agenda, en spoed direct naar uw telefoon.",
         """        <h3>Afspraken plannen in uw agenda</h3>
        <p>Vraagt een beller om een afspraak, dan plant de telefonist die in via de agenda-koppeling. Een kapsalon laat hem behandelingen inplannen, een garagebedrijf een APK-afspraak en een restaurant een tafel. Werkt u met een gangbaar afsprakensysteem, dan koppelen wij daaraan zodat alle afspraken op één plek blijven. Welke koppeling bij uw systeem past, bepalen we in de intake.</p>

        <h3>Spoed doorschakelen</h3>
        <p>U bepaalt vooraf wat als dringend geldt. Bij een installatiebedrijf is dat bijvoorbeeld een lekkage of een storing zonder warmte: zo'n gesprek schakelt hij direct door naar uw mobiel. Wat kan wachten, legt hij vast als terugbelverzoek met volledig transcript.</p>""",
         "agenda-doorschakelen",
         "Twee dingen bepalen hoe bruikbaar een AI-telefonist is: wat hij zelf regelt in uw agenda, en wat hij naar u doorzet."),

   sectie("Branches", "Voor welke bedrijven een AI-telefonist past.",
          "Overal waar de telefoon gaat terwijl niemand kan opnemen. Vier branches hebben een eigen pagina met uitgewerkte voorbeelden.",
          voorbeeldblok([
            ("Kapsalons", 'De telefoon gaat tijdens een behandeling. De telefonist neemt op en plant de afspraak in. <a href="ai-voor-kapsalons.html">Lees over kapsalons</a>.'),
            ("Garagebedrijven", 'De telefoon gaat terwijl u onder een auto ligt. Hij plant in en schakelt door wanneer het technisch wordt. <a href="ai-voor-garagebedrijven.html">Lees over garagebedrijven</a>.'),
            ("Horeca", 'Reserveringen en afhaalbestellingen, ook midden in de service. <a href="ai-voor-de-horeca.html">Lees over de horeca</a>.'),
            ("Bouw en installatie", 'Aanvragen vastleggen terwijl u op de steiger staat, en spoed direct doorschakelen. <a href="ai-voor-bouw-en-installatie.html">Lees over bouw en installatie</a>.'),
          ]), "branches"),

   proza("Uit eigen praktijk", "Na het gesprek: waar een bestelling terechtkomt.",
         """        <p>Een gesprek dat eindigt op een briefje levert vervolgwerk op. Daarom zet de telefonist een bestelling gestructureerd in de orderlijst, waar ook bestellingen uit andere kanalen binnenkomen, en krijgt de klant een bevestiging.</p>
        <p>Wat er met een order daarna gebeurt, draait sinds begin mei 2026 bij Aronza, het e-commercebedrijf van de oprichter van Complete AI. Daar raakt een binnenkomende order de voorraad, de factuur en het klantdossier zonder dat er iets wordt overgetypt. Sinds de ingebruikname is er geen storing geweest. Dat is geen garantie voor de toekomst, wel een aanwijzing dat de keten bestand is tegen dagelijkse belasting.</p>
        <p>Dat is ook de reden dat automatiseringen bij klanten binnen enkele werkdagen kunnen staan: 17 draaien vandaag al en zijn getest. De AI-telefonist vraagt meer afstemming en is binnen 2 weken operationeel. De volledige uitwerking van de keten leest u in <a href="case-aronza.html">de klantcase Aronza</a>.</p>""",
         "eigen-praktijk"),

   proza("Veiligheid en AVG", "Wat er met de gesprekken gebeurt, en wat de AVG daarover vraagt.",
         """        <h3>Eerst de verwerkersovereenkomst</h3>
        <p>Schakelt u een partij in die persoonsgegevens voor u verwerkt, dan eist de AVG een schriftelijke verwerkersovereenkomst (artikel 28, derde lid). Ontbreekt die, dan zijn volgens de <a href="https://www.autoriteitpersoonsgegevens.nl/themas/basis-avg/avg-algemeen/verwerkersovereenkomst" rel="noopener" target="_blank">Autoriteit Persoonsgegevens</a> beide partijen in overtreding. Complete AI legt dit vóór de start vast, niet achteraf. Uw gegevens blijven van u en worden nooit gedeeld of doorverkocht.</p>

        <h3>Wat de AP in zo'n overeenkomst verwacht</h3>
        <p>De AP noemt onderwerpen die in een verwerkersovereenkomst horen te staan. Ze vormen een bruikbare controlelijst voor elke leverancier:</p>
        <ul>
          <li>waarover de verwerking gaat, hoe lang ze duurt en om welke gegevens het gaat;</li>
          <li>dat de verwerker alleen op uw schriftelijke instructies werkt;</li>
          <li>geheimhouding door iedereen die bij de gegevens kan;</li>
          <li>passende beveiligingsmaatregelen;</li>
          <li>subverwerkers alleen met uw voorafgaande schriftelijke toestemming;</li>
          <li>hulp bij verzoeken van betrokkenen, zoals inzage en verwijdering;</li>
          <li>hulp bij datalekken;</li>
          <li>verwijdering of teruggave van de gegevens na afloop;</li>
          <li>medewerking aan controles.</li>
        </ul>

        <h3>Wat u zelf regelt</h3>
        <p>Als bedrijf bepaalt u waarvoor de gesprekken worden gebruikt. U bent daarmee de verwerkingsverantwoordelijke en blijft verantwoordelijk, ook wanneer de overeenkomst door de verwerker is opgesteld. Bovendien moet u uw klanten volgens de AP <a href="https://www.autoriteitpersoonsgegevens.nl/themas/algoritmes-ai/algoritmes-ai-en-de-avg" rel="noopener" target="_blank">informeren over wat u met hun gegevens doet</a> en waarom. Van elk gesprek is een transcript beschikbaar. Omdat daarbij persoonsgegevens van uw klanten worden verwerkt, informeert u uw bellers hierover. Daar ondersteunen wij u bij.</p>""",
         "veiligheid-avg",
         "Een telefoongesprek bevat persoonsgegevens: namen, nummers, adressen en wat iemand bestelt."),

   proza("De wet", "De AI-verordening: wat artikel 50 vraagt van een AI-telefonist.",
         """        <h3>Sinds wanneer geldt de regel?</h3>
        <p>De transparantieverplichtingen van artikel 50 van de AI-verordening zijn sinds 2 augustus 2026 van toepassing. De Europese Commissie publiceerde op 20 juli 2026 de <a href="https://www.itenrecht.nl/artikelen/definitieve-richtsnoeren-artikel-50-ai-verordening-transparantie-dit-zijn-de-9-belangrijkste-wijzigingen" rel="noopener" target="_blank">definitieve richtsnoeren</a> daarover. De <a href="https://www.autoriteitpersoonsgegevens.nl/actueel/transparantie-eisen-ai-gelden-vanaf-2-augustus-ap-adviseert-praktijkcode-te-ondertekenen" rel="noopener" target="_blank">Autoriteit Persoonsgegevens</a> schreef op 9 juli 2026 dat aanbieders en gebruikers van AI-systemen per 2 augustus 2026 duidelijk moeten maken wanneer mensen met AI te maken hebben. De <a href="https://nos.nl/artikel/2625224-geen-twijfel-ai-telefonist-moet-zich-voortaan-direct-prijsgeven" rel="noopener" target="_blank">NOS</a> meldde op 2 augustus dat dit ook geldt voor wie belt met een AI-receptionist.</p>

        <h3>Wat bepaalt artikel 50, eerste lid?</h3>
        <p>Het eerste lid richt zich tot de aanbieder van een AI-systeem dat bedoeld is voor directe interactie met mensen. Dat systeem moet zo zijn ontworpen dat de betrokken personen worden geïnformeerd dat zij met een AI-systeem communiceren. Is dat vanuit het oogpunt van een normaal geïnformeerde, redelijk oplettende persoon al duidelijk uit de omstandigheden en de context, dan hoeft het niet. Zie <a href="https://rijksictgilde.github.io/ai-verordening/hoofdstukken/hoofdstuk-4/a50/" rel="noopener" target="_blank">de tekst van artikel 50</a>.</p>
        <p>Volgens het vijfde lid moet de informatie uiterlijk bij de eerste interactie worden gegeven, op een duidelijke en te onderscheiden manier, en moet zij voldoen aan de toepasselijke toegankelijkheidseisen.</p>

        <h3>Wat zeggen de richtsnoeren over menselijke tussenkomst?</h3>
        <p>Volgens de samenvatting van IT &amp; Recht bepalen de definitieve richtsnoeren dat de mogelijkheid van menselijke tussenkomst niet mag worden gebruikt om de informatieplicht te omzeilen. Dat een gesprek naar een mens kan doorgaan, neemt de plicht om bekend te maken dat de beller met AI spreekt dus niet weg. Voor AI-agenten die taken uitvoeren, zoals het maken van boekingen, noemen de richtsnoeren daarnaast dat de agent moet aangeven namens wie hij handelt.</p>

        <h3>Vragen om aan elke leverancier te stellen</h3>
        <ul>
          <li>Hoe meldt de telefonist zich, en op welk moment in het gesprek?</li>
          <li>Wie is volgens de overeenkomst de aanbieder van het AI-systeem, en wie de gebruiker?</li>
          <li>Wat gebeurt er met de melding wanneer een gesprek naar een medewerker wordt doorgeschakeld?</li>
          <li>Welke verwerkersovereenkomst hoort erbij, en welke onderwerpen staan daarin?</li>
        </ul>
        <p>Hoe het gesprek bij de telefonist van Complete AI begint, leest u bij <a href="#zo-klinkt-het">het gespreksverloop</a>.</p>

        <div class="noot"><p>Dit is een weergave van openbare bronnen en geen juridisch advies. Of een bepaalde formulering in uw situatie voldoet, beoordeelt u bij voorkeur samen met een jurist. De bronnen staan onderaan deze pagina.</p></div>""",
         "de-wet",
         "Deze sectie geeft de verplichting weer zoals de bronnen haar beschrijven, feitelijk en zonder oordeel over een bepaald product."),

   sectie("Werkwijze", "Van akkoord tot een werkende telefonist in twee weken.",
          "Het meeste werk zit in het correct vullen van wat hij moet weten. Daarvoor hebben wij enkele keren kort uw input nodig.",
          routeblok([
            ("Intake", "Wanneer gaat de telefoon, wat wordt er gevraagd, en wat mag hij zelfstandig afhandelen? Een half uur."),
            ("Inrichten", "Wij vullen hem met uw assortiment, levertijden en toon. U leest mee en corrigeert."),
            ("Proefdraaien", "Eerst naast de bestaande lijn, zodat u hoort hoe hij functioneert zonder risico."),
            ("Live en bijsturen", "Hij wordt geactiveerd buiten openingstijden en tijdens drukte. De eerste weken luisteren wij mee en scherpen we aan."),
          ]), "werkwijze"),

   proza("Na de start", "Hoe u controleert of het klopt.",
         """        <p>Een AI-telefonist is zo goed als wat hij weet en wat er met zijn notities gebeurt. Daarom luisteren wij de eerste weken mee en scherpen we aan. Daarna kunt u zelf steekproeven doen, omdat van elk gesprek een transcript beschikbaar is.</p>
        <p>Vier vragen voor een steekproef:</p>
        <ol>
          <li>Staat in elke terugbelnotitie de vraag van de beller, zodat niemand hoeft te raden wat er bedoeld werd?</li>
          <li>Klopt de bestelling in de lijst met wat er in het transcript is gezegd?</li>
          <li>Waren de doorgeschakelde gesprekken terecht dringend, en zijn er dringende gesprekken blijven liggen?</li>
          <li>Welke vragen kon hij niet beantwoorden? Die horen bij wat hij moet weten.</li>
        </ol>""",
         "controle"),

   proza("Kosten", "Wat kost een AI-telefonist? Waar het van afhangt.",
         """        <h3>Waar de kosten van afhangen</h3>
        <p>Een voorstel wordt bepaald door wat de telefonist voor uw bedrijf afhandelt: alleen opnemen en noteren, of ook bestellingen en afspraken. Daarnaast tellen de koppelingen die daarvoor nodig zijn, zoals de agenda, de talen waarin hij spreekt en de momenten waarop hij opneemt.</p>

        <h3>Hoe het voorstel tot stand komt</h3>
        <p>In de intake van een half uur bepalen we wat hij moet afhandelen. Binnen één werkdag ligt er een voorstel met één vaste prijs: eenmalig voor de bouw en een vast maandbedrag, zonder nacalculatie. Het abonnement is maandelijks opzegbaar. Plan een <a href="index.html#contact">intake</a> om het voor uw situatie te laten doorrekenen.</p>

        <h3>Zo vergelijkt u aanbieders</h3>
        <p>Wilt u routes of aanbieders vergelijken, weet dan eerst hoeveel gesprekken er binnenkomen en op welke uren. Noteer daarom een week lang wanneer de telefoon gaat, wanneer niemand opneemt en waarover er wordt gebeld. Dat zijn ook de eerste vragen in onze intake.</p>""",
         "kosten",
         "Er staat geen bedrag op deze pagina, omdat een getal niet zou kloppen."),

   bronnen([
     ("Rijks ICT Gilde: artikel 50 van de AI-verordening",
      "https://rijksictgilde.github.io/ai-verordening/hoofdstukken/hoofdstuk-4/a50/",
      "De tekst van artikel 50 in het Nederlands: de informatieplicht bij directe interactie met mensen en het moment waarop de informatie moet worden gegeven."),
     ("NOS: AI-telefonist moet zich voortaan direct prijsgeven",
      "https://nos.nl/artikel/2625224-geen-twijfel-ai-telefonist-moet-zich-voortaan-direct-prijsgeven",
      "Nieuwsbericht van 2 augustus 2026 over de transparantieplicht en het gebruik van AI-receptionisten."),
     ("IT &amp; Recht: definitieve richtsnoeren artikel 50 AI-verordening",
      "https://www.itenrecht.nl/artikelen/definitieve-richtsnoeren-artikel-50-ai-verordening-transparantie-dit-zijn-de-9-belangrijkste-wijzigingen",
      "Samenvatting van de richtsnoeren van de Europese Commissie van 20 juli 2026, onder meer over menselijke tussenkomst en AI-agenten."),
     ("Autoriteit Persoonsgegevens: transparantie-eisen voor AI sinds 2 augustus 2026",
      "https://www.autoriteitpersoonsgegevens.nl/actueel/transparantie-eisen-ai-gelden-vanaf-2-augustus-ap-adviseert-praktijkcode-te-ondertekenen",
      "Bericht van 9 juli 2026 over de vier transparantieverplichtingen, waaronder duidelijk maken dat iemand met AI communiceert."),
     ("Autoriteit Persoonsgegevens: verwerkersovereenkomst",
      "https://www.autoriteitpersoonsgegevens.nl/themas/basis-avg/avg-algemeen/verwerkersovereenkomst",
      "Wanneer een verwerkersovereenkomst verplicht is en welke onderwerpen daarin worden vastgelegd."),
     ("Autoriteit Persoonsgegevens: algoritmes, AI en de AVG",
      "https://www.autoriteitpersoonsgegevens.nl/themas/algoritmes-ai/algoritmes-ai-en-de-avg",
      "Wat de AVG vraagt van bedrijven die AI inzetten met persoonsgegevens, waaronder informatie aan betrokkenen."),
   ]),
]),
},

# ───────────────────────── KLANTCASE: ARONZA ─────────────────────────
{
 "bestand": "case-aronza.html",
 "soort": "case",
 "dienst": "Klantcase: Aronza",
 "titel": "Klantcase Aronza: administratie automatisch | Complete AI",
 "beschrijving": "Bij Aronza zijn facturatie, kosten, orderverwerking, voorraad en klantcontact geautomatiseerd. Draait sinds mei 2026 zonder storing; administratietijd naar nul.",
 "omschrijving": "Klantcase: hoe bij Aronza de volledige financiële en administratieve afhandeling werd geautomatiseerd — facturatie, kosten, orderverwerking, voorraadbeheer en klantcontact.",
 "ogen": "Klantcase",
 "h1": 'Van <span class="glans">vier tot zes uur</span> administratie per week naar nul.',
 "lead": "Aronza is de eerste organisatie waar de volledige financiële en administratieve afhandeling is geautomatiseerd. Facturatie, kosten, orderverwerking, voorraadbeheer en klantcontact lopen sinds begin mei zonder tussenkomst. In die periode is er geen enkele storing geweest.",
 "levertijd": "Draait sinds begin mei 2026",
 "uitkomsten": [
     ("4–6 uur", "per week ging op aan administratie en facturatie — dat is nu nul"),
     ("5", "processen volledig geautomatiseerd, van factuur tot voorraad"),
     ("0", "storingen sinds de ingebruikname in mei"),
 ],
 "slot_kop": "Dezelfde processen draaien ook bij u.",
 "slot_tekst": "De onderdelen die bij Aronza draaien zijn niet uniek voor dat bedrijf. Facturatie, kostenregistratie, orderverwerking, voorraad en klantcontact zijn dezelfde processen die bij elke ondernemer tijd opeisen. In een half uur bepalen we welke daarvan bij u het meeste opleveren.",
 "vragen": [
   ("Is dit een echte case of een voorbeeld?",
    "Dit is een echte implementatie die dagelijks draait. Aronza is het e-commercebedrijf van de oprichter van Complete AI. Dat is bewust vermeld en niet verborgen: het is de reden dat wij precies weten wat deze systemen doen onder dagelijkse belasting, en waarom ze eerst hier zijn beproefd voordat ze bij klanten werden ingezet."),
   ("Waarom zou dit bij mijn bedrijf ook werken?",
    "Omdat de onderliggende processen hetzelfde zijn. Een factuur opstellen en opvolgen, kosten registreren en categoriseren, een order van binnenkomst naar verzending brengen, voorraad bijhouden en klanten op tijd antwoorden — dat gebeurt bij een vishandel, een garagebedrijf en een webshop op dezelfde manier. Wat verschilt zijn de gegevens en de uitzonderingen, en dat is precies wat wij inrichten."),
   ("Hoe lang duurde de implementatie?",
    "De onderdelen zijn gefaseerd in gebruik genomen, te beginnen bij facturatie en kosten. Voor een klant met een vergelijkbare situatie is de doorlooptijd enkele werkdagen per onderdeel, omdat de software al gebouwd en getest is."),
   ("Wat gebeurt er als er iets misgaat?",
    "In deze opzet is dat sinds de ingebruikname niet voorgekomen. Dat is geen garantie voor de toekomst, en daarom is elke automatische handeling terug te zien en terug te draaien. Bij handelingen die naar buiten gaan — een factuur, een bericht aan een klant — is instelbaar of er een goedkeuringsstap tussen zit."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("Uitgangssituatie", "Vier tot zes uur per week aan werk dat niets opleverde.",
          "Aronza is een e-commercebedrijf. Zoals bij elke handelsonderneming groeide de administratieve last mee met het aantal orders — en die last kwam volledig op één persoon terecht.",
          """      <div class="voor-na reveal">
        <div class="was">
          <h3>Vóór de automatisering</h3>
          <ul>
            <li>Wekelijks vier tot zes uur aan administratie en facturatie, buiten werktijd</li>
            <li>Facturen handmatig opstellen, versturen en nalopen op betaling</li>
            <li>Kosten achteraf verzamelen en categoriseren voor de aangifte</li>
            <li>Orders handmatig van binnenkomst naar verzending begeleiden</li>
            <li>Voorraad bijhouden in een apart overzicht dat snel achterliep</li>
            <li>Klantcontact tussen het andere werk door, met wisselende reactietijd</li>
          </ul>
        </div>
        <div class="nu">
          <h3>Sinds begin mei 2026</h3>
          <ul>
            <li>Geen wekelijkse administratietijd meer; de processen lopen zonder tussenkomst</li>
            <li>Facturen worden automatisch opgesteld, verstuurd en opgevolgd</li>
            <li>Kosten worden bij binnenkomst geregistreerd en gecategoriseerd</li>
            <li>Orders lopen van binnenkomst tot afhandeling door één keten</li>
            <li>Voorraadstanden worden automatisch bijgewerkt</li>
            <li>Klantcontact verloopt gestructureerd en met een vaste reactietijd</li>
          </ul>
        </div>
      </div>""", "uitgangssituatie"),

   sectie("De opzet", "Vijf processen, als één geheel ingericht.",
          "De winst zat niet in vijf losse hulpmiddelen naast elkaar, maar in het feit dat ze op dezelfde gegevens werken. Een order die binnenkomt raakt de voorraad, de factuur en het klantdossier zonder dat er iets overgetypt hoeft te worden.",
          voorbeeldblok([
            ("Facturatie", "Facturen worden opgesteld en verstuurd op basis van de order. Openstaande posten worden automatisch opgevolgd, zonder dat er iemand een herinnering hoeft te schrijven."),
            ("Kostenregistratie", "Uitgaven komen binnen, worden gecategoriseerd en staan direct op de juiste plaats. Aan het einde van het kwartaal is er geen inhaalslag meer nodig."),
            ("Orderverwerking", "Elke order doorloopt dezelfde route van binnenkomst tot afhandeling. Geen losse lijstjes, geen orders die tussen wal en schip vallen."),
            ("Voorraadbeheer", "Voorraadstanden bewegen mee met wat er verkocht en ingekocht wordt, zodat het overzicht klopt op het moment dat er een beslissing op genomen wordt."),
            ("Klantcontact", "Bevestigingen, statusberichten en veelgestelde vragen worden gestructureerd afgehandeld, met een voorspelbare reactietijd."),
          ]), "de-opzet"),

   sectie("Resultaat", "De tijdwinst is het minst interessante deel.",
          "Vier tot zes uur per week is een concreet getal, en dat alleen al rechtvaardigt de investering. Maar wat het in de praktijk verandert, gaat verder dan de klok.",
          krijgtblok([
            ("Werk verschuift naar de dag", "De administratie hoefde niet langer 's avonds ingehaald te worden. Dat is minder een tijdwinst dan een verschuiving van wanneer het werk plaatsvindt — en dat scheelt in de praktijk het meest."),
            ("Fouten nemen af", "Handmatig overtypen tussen order, factuur en voorraad is de plek waar fouten ontstaan. Door één keten te gebruiken verdwijnt die overdracht, en daarmee de fout."),
            ("Cijfers zijn actueel", "Omdat kosten en omzet bij binnenkomst worden geregistreerd, is het beeld op elk moment actueel in plaats van pas na de kwartaalafsluiting."),
            ("Geld komt eerder binnen", "Openstaande facturen worden consequent opgevolgd, ook wanneer dat ongemakkelijk voelt. Dat is precies het soort taak dat een systeem beter volhoudt dan een mens."),
            ("Groei kost geen extra uren", "Meer orders betekenden voorheen meer administratie. Die koppeling is doorbroken: het volume kan toenemen zonder dat de administratieve last meegroeit."),
            ("Stabiel sinds mei", "Sinds de ingebruikname begin mei 2026 heeft de opzet geen enkele keer gefaald. Dat is geen garantie voor de toekomst, wel een aanwijzing dat het bestand is tegen dagelijkse belasting."),
          ]), "resultaat"),

   sectie("Verantwoording", "Waarom deze case op deze site staat.",
          "Aronza is het e-commercebedrijf van de oprichter van Complete AI. Dat staat er bewust bij, en het werkt in uw voordeel.",
          krijgtblok([
            ("Een implementatie die echt draait", "Deze systemen draaien dagelijks in een bedrijf waar de gevolgen van een fout direct voelbaar zijn. Dat is een strengere test dan een demo-omgeving."),
            ("Het verklaart de doorlooptijd", "Dat automatiseringen bij klanten binnen enkele werkdagen kunnen staan, komt doordat ze hier al gebouwd, getest en in productie genomen zijn. Complete AI verkoopt geen software die het zelf niet gebruikt."),
          ]), "verantwoording"),
 ]),
},

# ──────────────────── GIDS: AI VOOR UW BEDRIJF ────────────────────
{
 "bestand": "ai-voor-uw-bedrijf.html",
 "soort": "gids",
 "dienst": "AI voor uw bedrijf",
 "titel": "Wat kan AI voor uw bedrijf? Gids voor het mkb | Complete AI",
 "beschrijving": "Wat AI in een mkb-bedrijf kan overnemen, hoe u kiest waar u begint en waar u zelf blijft beslissen. Met cijfers van het CBS en uit de praktijk bij Aronza.",
 "omschrijving": "Gids voor het mkb: wat AI voor een bedrijf kan overnemen, hoe u kiest waar u begint en waar de grens ligt, met cijfers van het CBS en de praktijk bij Aronza.",
 "ogen": "Gids",
 "h1": 'Wat kan AI voor uw bedrijf? <span class="glans">Een gids voor het mkb.</span>',
 "lead": "AI voor het mkb betekent in de praktijk dat software terugkerend werk overneemt: gegevens verwerken, de telefoon en berichten beantwoorden, herinneringen versturen en cijfers bijhouden. Wat AI voor uw bedrijf kan doen, hangt af van het werk dat elke week terugkomt. Bij Aronza, het e-commercebedrijf van de oprichter, ging de administratie zo van vier tot zes uur per week naar nul.",
 "levertijd": "Leestijd ongeveer 12 minuten",
 "gewijzigd": "2026-09-24",
 "uitkomsten": [
     ("4–6 uur", "administratie per week bij Aronza, sinds mei 2026 teruggebracht tot nul"),
     ("14%", "van de bedrijven met 2 tot 10 werkzame personen gebruikte in 2025 AI (CBS, voorlopig)"),
     ("1", "taak tegelijk automatiseren: zo ziet u bij elke stap wat het oplevert"),
 ],
 "slot_kop": "Benieuwd wat er in uw situatie mogelijk is?",
 "slot_tekst": "In een half uur brengen wij in kaart welke taken bij u de meeste tijd kosten en welke daarvan zich lenen voor AI. Blijkt dat er weinig te halen valt, dan hoort u dat ook.",
 "vragen": [
   ("Hoe kan ik AI gebruiken voor mijn werk?",
    "Begin bij het werk dat elke week terugkomt en geen omzet oplevert. Voor uw eigen teksten en uitzoekwerk volstaat een algemene AI-assistent. Voor facturen, orders en herinneringen is een automatisering nodig die aan uw systemen is gekoppeld. Drie plekken om te beginnen zijn facturatie met opvolging, orders uit alle kanalen in één lijst en telefonische bereikbaarheid buiten kantooruren."),
   ("Hoe kan ik AI in mijn bedrijf implementeren?",
    "In fasen, te beginnen bij één taak. Leg eerst een week vast waar uw tijd naartoe gaat en automatiseer daarna één taak. Laat die enkele weken draaien en controleer of het klopt. Pas dan volgt de volgende. Zo ziet u bij elke stap wat het oplevert en kunt u tussentijds bijsturen."),
   ("Welke AI is het beste voor bedrijven?",
    """Er is geen AI die voor elk bedrijf het beste is; het hangt af van de taak. Voor eenmalig schrijf- en zoekwerk past een algemene AI-assistent. Voor werk dat elke week terugkomt past een automatisering die aan uw eigen systemen is gekoppeld. Voor de telefoon past een <a href="ai-telefonist.html">AI-telefonist</a>. <a href="#kiezen">De tabel</a> zet het naast elkaar."""),
   ("Wat zijn drie voorbeelden van AI?",
    """Volgens het <a href="https://www.cbs.nl/nl-nl/nieuws/2025/50/bedrijven-gebruiken-ai-vaakst-voor-marketing-of-verkoop" rel="noopener" target="_blank">CBS</a> gebruiken bedrijven het vaakst AI die geschreven tekst analyseert, AI die tekst of spraak genereert en spraakherkenning. In de praktijk is dat een e-mail of factuur lezen, een antwoord schrijven of een telefoongesprek voeren en verstaan. In 2025 gebruikte respectievelijk 12, 8 en 6 procent van de bedrijven deze technieken."""),
   ("Is AI ook iets voor een klein bedrijf?",
    """Ja. Bij bedrijven met 2 tot 10 werkzame personen steeg het AI-gebruik volgens het <a href="https://www.cbs.nl/nl-nl/nieuws/2025/50/bedrijven-gebruiken-ai-vaakst-voor-marketing-of-verkoop" rel="noopener" target="_blank">CBS</a> van 7 procent in 2023 naar 14 procent in 2025 (voorlopige cijfers). Voor een klein bedrijf is één terugkerende taak een goed startpunt. Bij Aronza ging de administratie zo van vier tot zes uur per week naar nul."""),
   ("Welke AI-toepassingen zijn er voor bedrijven?",
    """Voor mkb-bedrijven zijn dit de toepassingen die vandaag werken: facturatie en betaalherinneringen, kosten- en btw-registratie, orders uit telefoon, e-mail en WhatsApp in één lijst, voorraadbeheer, afspraakherinneringen, reviews verzamelen en een AI-telefonist buiten openingstijden. De lijst per afdeling staat bij <a href="bedrijfsprocessen-automatiseren-voorbeelden.html">bedrijfsprocessen automatiseren</a>."""),
   ("Hoe kan ik mijn boekhouding automatiseren?",
    "In stappen, te beginnen bij facturatie: facturen automatisch opstellen op basis van de order en openstaande posten automatisch opvolgen. Daarna de kosten: uitgaven bij binnenkomst registreren en categoriseren, zodat de btw-aangifte geen inhaalslag meer is. Als laatste volgt de koppeling met uw boekhoudpakket. Bij Aronza is zo begonnen: met facturatie en kosten."),
   ("Wat kost het om dit te laten bouwen?",
    "Dat hangt af van welke taken u wilt automatiseren en hoe uw bedrijf werkt. Een standaardprijs zou voor het ene bedrijf te hoog en voor het andere te laag uitvallen. Na een intake van een half uur ligt er één vaste prijs op papier: eenmalig voor de bouw en een vast maandbedrag voor onderhoud."),
   ("Is AI gratis te gebruiken?",
    """Losse hulpmiddelen zoals ChatGPT hebben gratis varianten, waarmee u teksten schrijft of vragen uitzoekt. Niet gratis is het koppelen aan uw eigen systemen, zodat werk zonder tussenkomst verloopt. Dat vraagt inrichting, onderhoud en toezicht. Werkt u met persoonsgegevens, dan moet u volgens de <a href="https://www.autoriteitpersoonsgegevens.nl/themas/algoritmes-ai/algoritmes-ai-en-de-avg" rel="noopener" target="_blank">Autoriteit Persoonsgegevens</a> vooraf vaststellen of dat binnen de AVG kan."""),
   ("Welke regels gelden er voor AI in mijn bedrijf?",
    """Drie. Sinds 2 februari 2025 moeten organisaties die AI gebruiken zorgen dat hun medewerkers er genoeg van weten. De AVG geldt zodra er persoonsgegevens in het spel zijn. En sinds 2 augustus 2026 moet AI die met mensen communiceert dat bekendmaken. <a href="#regels">De sectie over regels</a> geeft de bronnen."""),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   inhoudsopgave([
     ("kort-antwoord", "Het korte antwoord: drie soorten werk"),
     ("wat-is-ai", "Wat is AI, en wat zijn drie voorbeelden?"),
     ("cijfers", "AI voor het mkb in cijfers"),
     ("eigen-praktijk", "Wat Aronza liet zien"),
     ("kiezen", "Welke AI past bij welke taak?"),
     ("beginnen", "Zo begint u"),
     ("grens", "Waar u zelf blijft beslissen"),
     ("regels", "Welke regels gelden er?"),
     ("bronnen", "Bronnen"),
   ]),

   sectie("Het korte antwoord", "Wat kan AI voor uw bedrijf? Drie soorten werk.",
          "AI neemt in een mkb-bedrijf werk over dat elke week terugkomt, een vaste volgorde heeft en geen omzet oplevert. Dat werk valt in drie soorten.",
          krijgtblok([
            ("Invoer en administratie", "Gegevens overnemen en verwerken zonder overtypen. Een order wordt een factuur, een uitgave wordt geregistreerd en gecategoriseerd, een openstaande factuur wordt opgevolgd. Bij Aronza is hier begonnen: met facturatie en kosten."),
            ("Contact met klanten", 'Gesprekken en berichten aannemen en beantwoorden: de telefoon buiten openingstijden, veelgestelde vragen via WhatsApp, een herinnering vóór de afspraak en een verzoek om een beoordeling na afloop. Voor de telefoon bestaat een eigen pagina over de <a href="ai-telefonist.html">AI-telefonist</a>.'),
            ("Overzicht", "Cijfers zonder zoeken: omzet per dag, week of maand, kosten per categorie, winst en kasstroom, en een melding wanneer er iets afwijkt. Zo beslist u op cijfers in plaats van op gevoel."),
          ]) + """
      <div class="proza reveal">
        <div class="noot"><p>Zoekt u de lijst per afdeling, met per proces wat er vanzelf kan verlopen? Die staat op <a href="bedrijfsprocessen-automatiseren-voorbeelden.html">Bedrijfsprocessen automatiseren: voorbeelden</a>. Deze gids beantwoordt een andere vraag: wat AI voor uw bedrijf kan betekenen, hoe u kiest en hoe u begint.</p></div>
      </div>""", "kort-antwoord"),

   proza("De basis", "Wat is AI, en wat zijn drie voorbeelden?",
         """        <h3>Wat is AI?</h3>
        <p>Het <a href="https://www.cbs.nl/nl-nl/longread/rapportages/2025/kenmerken-van-bedrijven-die-ai-technologie-gebruiken?onepage=true" rel="noopener" target="_blank">CBS</a> omschrijft AI als computersystemen die taken uitvoeren waar vroeger menselijke intelligentie voor nodig was. Het is dus geen enkel product, maar een verzameling technieken die elk een ander soort taak overnemen.</p>

        <h3>Wat zijn drie voorbeelden van AI in een bedrijf?</h3>
        <p>Het CBS vraagt bedrijven welke AI-technologieën zij gebruiken. In 2025 waren dit de drie meest genoemde:</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Techniek</th><th>Voorbeeld in een mkb-bedrijf</th><th>Bedrijven die het gebruiken, 2025</th></tr></thead>
          <tbody>
            <tr><td>Geschreven tekst analyseren</td><td>Een binnenkomende e-mail, aanvraag of factuur lezen en de gegevens eruit halen</td><td>12 procent</td></tr>
            <tr><td>Tekst of spraak genereren</td><td>Een antwoord of bevestiging schrijven, of een telefoongesprek voeren</td><td>8 procent</td></tr>
            <tr><td>Spraakherkenning</td><td>Gesproken woorden omzetten in tekst, bijvoorbeeld in een telefoongesprek</td><td>6 procent</td></tr>
          </tbody>
        </table></div>
        <p>Daarnaast noemt het CBS machine learning (4 procent) en robotgestuurde procesautomatisering (3 procent). Alle cijfers zijn voorlopig. In een mkb-bedrijf komen die drie neer op lezen, schrijven en verstaan.</p>""",
         "wat-is-ai",
         "Voor uw bedrijf telt niet de techniek, maar de taak die zij overneemt."),

   proza("Cijfers", "AI voor het mkb: hoeveel bedrijven gebruiken het al?",
         """        <p>Het CBS publiceerde op 12 december 2025 voorlopige cijfers over AI-gebruik in bedrijven met twee of meer werkzame personen. Kleine bedrijven zitten onderaan, maar de groei is er ook:</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Bedrijfsgrootte</th><th>2023</th><th>2024</th><th>2025</th></tr></thead>
          <tbody>
            <tr><td>2 tot 10 werkzame personen</td><td>7%</td><td>11%</td><td>14%</td></tr>
            <tr><td>10 tot 50 werkzame personen</td><td>11%</td><td>19%</td><td>27%</td></tr>
            <tr><td>50 tot 250 werkzame personen</td><td>20%</td><td>31%</td><td>45%</td></tr>
            <tr><td>Alle bedrijven met 2 of meer werkzame personen</td><td>8%</td><td>13%</td><td>17%</td></tr>
          </tbody>
        </table></div>
        <p>Bij bedrijven met 2 tot 10 werkzame personen verdubbelde het aandeel dus in twee jaar, van 7 naar 14 procent. Per sector verschilt het sterk: 12 procent in de handel, 7 procent in de bouwnijverheid en 6 procent in de horeca, tegen 54 procent in de informatie en communicatie. Voor <a href="ai-voor-bouw-en-installatie.html">bouw en installatie</a> en <a href="ai-voor-de-horeca.html">de horeca</a> staat een eigen pagina klaar.</p>
        <p>Van de bedrijven die AI gebruiken, doet 35 procent dat voor marketing of verkoop en 32 procent voor bedrijfsadministratie of bestuurstaken. Voor boekhouding, controle of financieel beheer is dat 17 procent.</p>

        <h3>Waarom driekwart geen AI gebruikt</h3>
        <p>Volgens het <a href="https://www.cbs.nl/nl-nl/nieuws/2025/50/bedrijven-gebruiken-ai-vaakst-voor-marketing-of-verkoop" rel="noopener" target="_blank">CBS</a> gebruikt driekwart van de bedrijven geen AI en heeft dat ook niet overwogen. Bedrijven die het wel overwogen maar niet gebruiken, noemen gebrek aan ervaring als belangrijkste reden (73 procent). Daarnaast noemt 49 procent privacy en 42 procent de juridische gevolgen, zoals aansprakelijkheid bij schade.</p>

        <h3>Wat er tegenover die bezwaren staat</h3>
        <ul>
          <li><strong>Gebrek aan ervaring:</strong> begin met één taak en kijk de eerste weken mee. Zie <a href="#beginnen">Zo begint u</a>.</li>
          <li><strong>Privacy:</strong> leg vooraf vast wie welke gegevens verwerkt, in een verwerkersovereenkomst. Zie <a href="#regels">de regels</a>.</li>
          <li><strong>Juridische gevolgen:</strong> er zijn drie regels die elk bedrijf raken, en ze zijn te overzien. Zie <a href="#regels">de regels</a>.</li>
        </ul>""",
         "cijfers"),

   sectie("Uit eigen praktijk", "Wat Aronza liet zien.",
          "Dit zijn de uitkomsten van Aronza, het e-commercebedrijf van de oprichter van Complete AI, waar de administratieve afhandeling volledig is geautomatiseerd.",
          """      <div class="voor-na reveal">
        <div class="was">
          <h3>Vóór</h3>
          <ul>
            <li>Vier tot zes uur per week aan administratie en facturatie, grotendeels buiten werktijd</li>
            <li>Facturen handmatig opstellen, versturen en nalopen</li>
            <li>Kosten achteraf verzamelen voor de aangifte</li>
            <li>Orders handmatig begeleiden van binnenkomst tot verzending</li>
            <li>Voorraadoverzicht dat structureel achterliep</li>
          </ul>
        </div>
        <div class="nu">
          <h3>Sinds mei 2026</h3>
          <ul>
            <li>Geen wekelijkse administratietijd meer</li>
            <li>Facturen worden opgesteld, verstuurd en opgevolgd zonder tussenkomst</li>
            <li>Kosten worden bij binnenkomst geregistreerd en gerubriceerd</li>
            <li>Orders lopen door één keten van binnenkomst tot afhandeling</li>
            <li>Voorraadstanden bewegen automatisch mee</li>
          </ul>
        </div>
      </div>
      <div class="proza reveal">
        <h3>Vier dingen die het bedrijf ons leerde</h3>
        <ol>
          <li><strong>De winst zat in de koppeling.</strong> Niet in vijf losse hulpmiddelen, maar in het feit dat ze op dezelfde gegevens werken. Een order raakt de voorraad, de factuur en het klantdossier zonder overtypen.</li>
          <li><strong>Begin bij facturatie en kosten.</strong> Zo zijn de onderdelen bij Aronza in gebruik genomen: gefaseerd, met facturatie en kosten als eerste.</li>
          <li><strong>Het werk verschuift naar overdag.</strong> De administratie hoeft niet meer 's avonds te worden ingehaald.</li>
          <li><strong>Alles blijft controleerbaar.</strong> Elke automatische handeling is terug te zien en terug te draaien. Bij handelingen die naar buiten gaan, zoals een factuur of een bericht aan een klant, is instelbaar of er een goedkeuringsstap tussen zit.</li>
        </ol>
        <p>Sinds de ingebruikname begin mei 2026 is er geen storing geweest. Dat is geen garantie voor de toekomst. Dat 17 automatiseringen vandaag al draaien en getest zijn, verklaart waarom ze bij klanten binnen enkele werkdagen kunnen staan. De volledige uitwerking leest u in <a href="case-aronza.html">de klantcase</a>.</p>
      </div>""", "eigen-praktijk"),

   proza("Kiezen", "Welke AI is het beste voor bedrijven? Kies op taak, niet op merk.",
         """        <div class="tabelwrap"><table>
          <thead><tr><th>Taak</th><th>Wat past</th><th>Waarom</th></tr></thead>
          <tbody>
            <tr><td>Eenmalig een tekst schrijven, iets uitzoeken of een vraag beantwoorden</td><td>Een algemene AI-assistent, zoals ChatGPT</td><td>U stelt de vraag, beoordeelt het antwoord en gebruikt het zelf. Er is geen koppeling met uw systemen nodig.</td></tr>
            <tr><td>Werk dat elke week terugkomt: facturen, orders, herinneringen</td><td>Automatisering met AI, gekoppeld aan uw eigen systemen</td><td>Het werk verloopt zonder dat iemand een opdracht geeft. Dat vraagt inrichting, onderhoud en toezicht.</td></tr>
            <tr><td>Telefoongesprekken buiten openingstijden of tijdens drukte</td><td>Een <a href="ai-telefonist.html">AI-telefonist</a></td><td>Hij voert het gesprek en legt vast wat er nodig is.</td></tr>
            <tr><td>Cijfers en overzicht</td><td>Een dashboard met uw eigen gegevens</td><td>Omzet, kosten en kasstroom staan op één plek en worden bijgewerkt.</td></tr>
          </tbody>
        </table></div>

        <h3>Vier vragen bij elke keuze</h3>
        <ol>
          <li>Welke taak neemt het over, en hoeveel uur per week kost die taak nu?</li>
          <li>Welke gegevens gaan erin, en waar worden ze bewaard?</li>
          <li>Wie controleert het resultaat, en hoe snel ziet u een fout?</li>
          <li>Wat gebeurt er als u stopt: krijgt u uw gegevens terug in een gangbaar bestandsformaat?</li>
        </ol>
        <p>Een merknaam beantwoordt geen van deze vragen. De antwoorden laten zien welk soort hulpmiddel bij welke taak past.</p>""",
         "kiezen",
         "Er is geen AI die voor elk bedrijf het beste is. Wat past, hangt af van de taak."),

   sectie("Beginnen", "Zo begint u: vier stappen.",
          "De volgorde is belangrijker dan de techniek. Wie met het grootste project begint, ziet het langst niets gebeuren.",
          routeblok([
            ("Meet een week", "Noteer een week lang welk terugkerend werk u doet, hoe lang het duurt en hoeveel uitzonderingen erin zitten. Drie taken eisen het grootste deel op. Zonder meting automatiseert u het verkeerde."),
            ("Kies één taak", "Kies de taak met de meeste uren, een vaste volgorde en een gevolg dat te overzien is als het misgaat. Bij Aronza was dat facturatie."),
            ("Laat hem draaien en kijk mee", "De eerste weken kijken wij mee en sturen we bij. Bij berichten naar klanten bepaalt u of er eerst een goedkeuring tussen zit."),
            ("Breid uit vanaf wat werkt", "Pas als de eerste taak aantoonbaar draait, komt de volgende. Zo blijft bij elke stap zichtbaar wat het oplevert."),
          ]) + """
      <div class="proza reveal">
        <h3>Wat u na vier weken controleert</h3>
        <ul>
          <li>Klopt wat er is verwerkt met wat u zelf had gedaan? Neem een steekproef.</li>
          <li>Hoeveel tijd kost de taak nu nog? Leg dat naast uw meting uit stap 1.</li>
          <li>Welke uitzonderingen kwamen langs, en zijn ze goed opgevangen?</li>
          <li>Wat merken klanten of leveranciers ervan?</li>
        </ul>
        <p>Wilt u dit niet alleen doen? Een <a href="index.html#contact">intake van een half uur</a> is kosteloos en vrijblijvend. Daarin bepalen we welke taak bij u het meeste oplevert.</p>
      </div>""", "beginnen"),

   proza("De grens", "Waar u zelf blijft beslissen.",
         """        <p>Ook een goed ingerichte automatisering kan iets fout doen. Daarom bouwen wij in stappen en kijken we de eerste weken mee. AI neemt uitvoering over, geen verantwoordelijkheid. Vier dingen houdt u bewust bij uzelf:</p>
        <ul>
          <li><strong>Wat naar buiten gaat.</strong> Bij een factuur of een bericht aan een klant kiest u of er eerst een goedkeuring tussen zit. Die stap kan later vervallen.</li>
          <li><strong>Prijzen en offertes.</strong> Een concept kan klaarstaan met uw standaardposten, maar u bepaalt de prijs.</li>
          <li><strong>Gesprekken die dringend of complex zijn.</strong> Een AI-telefonist schakelt die door. U bepaalt vooraf wat daaronder valt.</li>
          <li><strong>Wat de AI niet weet.</strong> Een goed ingerichte assistent verzint niets: hij legt de vraag vast in een terugbelnotitie.</li>
        </ul>
        <p>En de keuze om te stoppen blijft bij u. Alles wat automatisch gebeurt is terug te zien en terug te draaien, en de gegevens blijven van u. Bij stoppen ontvangt u alles in een gangbaar bestandsformaat.</p>""",
         "grens"),

   proza("Regels", "Welke regels gelden er voor AI in uw bedrijf?",
         """        <h3>AI-geletterdheid: sinds 2 februari 2025</h3>
        <p>Organisaties die AI-systemen gebruiken, moeten volgens de <a href="https://www.autoriteitpersoonsgegevens.nl/themas/algoritmes-ai/ai-verordening/ai-geletterdheid" rel="noopener" target="_blank">Autoriteit Persoonsgegevens</a> zorgen dat hun medewerkers genoeg weten en kunnen om AI verantwoord in te zetten. De wet zegt niet welke maatregelen dat zijn. De benodigde kennis hangt af van de situatie en de risico's.</p>

        <h3>Persoonsgegevens: de AVG</h3>
        <p>Verwerkt AI persoonsgegevens, dan moet u voldoen aan de AVG. De <a href="https://www.autoriteitpersoonsgegevens.nl/themas/algoritmes-ai/algoritmes-ai-en-de-avg/regels-bij-gebruik-van-ai-algoritmes" rel="noopener" target="_blank">AP</a> noemt onder meer een grondslag voor de verwerking, transparantie richting klanten, een vooraf vastgesteld doel, zo min mogelijk gegevens met vooraf vastgestelde bewaartermijnen, juiste gegevens en beveiliging. Schakelt u een partij in die de gegevens voor u verwerkt, dan hoort daar een schriftelijke <a href="https://www.autoriteitpersoonsgegevens.nl/themas/basis-avg/avg-algemeen/verwerkersovereenkomst" rel="noopener" target="_blank">verwerkersovereenkomst</a> bij. Complete AI legt dat vóór de start vast.</p>

        <h3>AI die met mensen communiceert: sinds 2 augustus 2026</h3>
        <p>Voor AI-systemen die rechtstreeks met mensen communiceren, zoals een chatbot of een AI-telefonist, geldt artikel 50 van de AI-verordening: mensen moeten weten dat zij met een AI-systeem te maken hebben, uiterlijk bij het eerste contact. De <a href="https://www.autoriteitpersoonsgegevens.nl/actueel/transparantie-eisen-ai-gelden-vanaf-2-augustus-ap-adviseert-praktijkcode-te-ondertekenen" rel="noopener" target="_blank">AP</a> noemt als voorbeeld dat duidelijk moet zijn dat een chatbot geen mens is. Wat de bronnen daarover zeggen, staat uitgewerkt op de pagina over de <a href="ai-telefonist.html#de-wet">AI-telefonist</a>.</p>

        <div class="noot"><p>Dit is een weergave van openbare bronnen en geen juridisch advies. Voor de toepassing op uw situatie kunt u terecht bij een jurist of bij de Autoriteit Persoonsgegevens.</p></div>""",
         "regels",
         "Drie regels raken elk mkb-bedrijf dat AI inzet. De bronnen staan onderaan deze pagina."),

   bronnen([
     ("CBS: Bedrijven gebruiken AI vaakst voor marketing of verkoop",
      "https://www.cbs.nl/nl-nl/nieuws/2025/50/bedrijven-gebruiken-ai-vaakst-voor-marketing-of-verkoop",
      "Voorlopige cijfers over AI-gebruik in 2025, naar bedrijfsgrootte, bedrijfstak en doel, en de redenen om AI niet te gebruiken. Gebaseerd op de enquête ICT-gebruik bij bedrijven."),
     ("CBS: Kenmerken van bedrijven die AI-technologie gebruiken",
      "https://www.cbs.nl/nl-nl/longread/rapportages/2025/kenmerken-van-bedrijven-die-ai-technologie-gebruiken?onepage=true",
      "Rapport uit 2025. De inleiding bevat de omschrijving van AI die op deze pagina wordt gebruikt."),
     ("Autoriteit Persoonsgegevens: AI-geletterdheid",
      "https://www.autoriteitpersoonsgegevens.nl/themas/algoritmes-ai/ai-verordening/ai-geletterdheid",
      "Wat de verplichting inhoudt en sinds wanneer ze geldt. De wet schrijft geen specifieke maatregelen voor."),
     ("Autoriteit Persoonsgegevens: regels bij gebruik van AI en algoritmes",
      "https://www.autoriteitpersoonsgegevens.nl/themas/algoritmes-ai/algoritmes-ai-en-de-avg/regels-bij-gebruik-van-ai-algoritmes",
      "De AVG-regels die gelden bij AI met persoonsgegevens: rechtmatigheid, transparantie, doelbinding, dataminimalisatie, juistheid en beveiliging."),
     ("Autoriteit Persoonsgegevens: verwerkersovereenkomst",
      "https://www.autoriteitpersoonsgegevens.nl/themas/basis-avg/avg-algemeen/verwerkersovereenkomst",
      "Wanneer een verwerkersovereenkomst verplicht is en welke onderwerpen daarin worden vastgelegd."),
     ("Autoriteit Persoonsgegevens: transparantie-eisen voor AI sinds 2 augustus 2026",
      "https://www.autoriteitpersoonsgegevens.nl/actueel/transparantie-eisen-ai-gelden-vanaf-2-augustus-ap-adviseert-praktijkcode-te-ondertekenen",
      "Bericht van 9 juli 2026 over de transparantieverplichtingen, waaronder duidelijk maken dat iemand met AI communiceert."),
   ]),
]),
},

# ───────────────────────────── KAPSALONS ─────────────────────────────
{
 "bestand": "ai-voor-kapsalons.html",
 "groep": "branche",
 "dienst": "AI voor kapsalons",
 "titel": "AI en automatisering voor kapsalons | Complete AI",
 "beschrijving": "Online afspraken, automatische herinneringen tegen no-shows en een AI-telefonist die tijdens de behandeling opneemt en inplant.",
 "omschrijving": "Automatisering voor kapsalons: online afspraken, automatische herinneringen tegen no-shows, een AI-telefonist die opneemt tijdens de behandeling en reviews die vanzelf binnenkomen.",
 "ogen": "Voor kapsalons",
 "h1": 'De telefoon gaat terwijl u knipt. <span class="glans">Iemand neemt op.</span>',
 "lead": "In een salon vallen twee dingen altijd samen: de klant in de stoel en de klant aan de telefoon. Aan \u00e9\u00e9n daarvan verdient u niets zolang u de andere helpt. Complete AI richt de salon zo in dat afspraken binnenkomen, worden bevestigd en worden nagekomen \u2014 zonder dat u de schaar hoeft neer te leggen.",
 "levertijd": "Afspraken binnen enkele werkdagen \u00b7 telefoon binnen 2 weken",
 "uitkomsten": [
     ("24/7", "afspraken maken, ook op de dagen dat de salon dicht is"),
     ("2\u00d7", "een herinnering vooraf: de dag ervoor en het uur ervoor"),
     ("0", "gemiste gesprekken tijdens een behandeling"),
 ],
 "slot_kop": "Een half uur, tussen twee klanten door.",
 "slot_tekst": "Wij komen langs of bellen op een rustig moment. In een half uur brengen we in kaart hoeveel afspraken u misloopt, hoeveel no-shows u heeft en wat daarvan op te lossen valt. Kosteloos, en u zit nergens aan vast.",
 "vragen": [
   ("Klinkt zo\u2019n AI-telefonist als een robot?",
    "Nee. Hij spreekt Nederlands met een natuurlijke stem, noemt de naam van uw salon en beantwoordt vragen over openingstijden, behandelingen en beschikbaarheid. Wie belt, merkt dat hij een assistent spreekt \u2014 net zoals bij een receptioniste \u2014 maar niet dat het gesprek stroef verloopt."),
   ("Wat gebeurt er als iemand iets vraagt wat hij niet weet?",
    "Dan schakelt hij door of noteert hij een terugbelverzoek, inclusief volledig transcript van het gesprek. U bepaalt vooraf welke onderwerpen doorgeschakeld moeten worden en welke hij zelf mag afhandelen."),
   ("Wij werken al met een afsprakensysteem. Kan dat blijven?",
    "Ja. Werkt u met een gangbaar salonsysteem, dan koppelen wij daaraan zodat alle afspraken op \u00e9\u00e9n plek blijven staan. Welke koppeling bij uw systeem past, bepalen we in de intake."),
   ("Helpt dit werkelijk tegen no-shows?",
    "Een herinnering vooraf is de enige maatregel waarvan het effect breed erkend wordt, en het kost u niets om hem te versturen omdat het automatisch gaat. Wij beloven geen percentage \u2014 dat verschilt per salon en per klantenkring \u2014 maar het aantal vergeten afspraken loopt aantoonbaar terug."),
   ("Hoe snel staat dit?",
    "Online afspraken en herinneringen zijn binnen enkele werkdagen operationeel. De AI-telefonist vraagt meer afstemming en staat binnen twee weken."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("De situatie", "Vier momenten waarop een salon omzet verliest.",
          "Geen daarvan komt door slecht werk. Ze komen doordat \u00e9\u00e9n persoon niet op twee plaatsen tegelijk kan zijn.",
          pijnblok([
            ("De telefoon tijdens een behandeling", "U kunt niet opnemen. Wie belt en niemand krijgt, belt de volgende salon."),
            ("No-shows", "Een leeg blok in de agenda is niet in te halen. Die tijd is weg."),
            ("Afspraken via vier kanalen", "Telefoon, WhatsApp, Instagram en aan de balie. Dubbele boekingen zijn dan een kwestie van tijd."),
            ("Reviews die uitblijven", "Tevreden klanten laten uit zichzelf geen beoordeling achter. Vragen vergeet u, want u staat te werken."),
          ]), "herkenbaar"),

   sectie("Wat wij inrichten", "Vijf onderdelen die het werk uit handen nemen.",
          "U kiest wat u nodig heeft. Elk onderdeel functioneert zelfstandig; samen sluiten ze op elkaar aan.",
          krijgtblok([
            ("Online afspraken, dag en nacht", "Klanten kiezen zelf een moment dat vrij is, ook \u2019s avonds en op maandag. De agenda blijft \u00e9\u00e9n agenda."),
            ("Een AI-telefonist die opneemt", "Neemt op wanneer u niet kunt, spreekt Nederlands, kent uw behandelingen en plant de afspraak direct in."),
            ("Herinnering vooraf", "De dag ervoor en kort van tevoren een bericht, met de mogelijkheid om te verzetten in plaats van niet te komen."),
            ("Reviews die binnenkomen", "Na de afspraak automatisch een verzoek om een beoordeling. Dat is precies wat u hoger in het kaartje van Google zet."),
            ("Terugkeermoment", "Zes tot acht weken na de laatste afspraak een vriendelijk bericht. Voor een salon is dit de eenvoudigste bron van extra omzet."),
          ]), "wat-wij-inrichten"),

   sectie("Voorbeelden", "Hoe dat er op een gewone dinsdag uitziet.",
          "Geen van deze handelingen kost u nog tijd zodra het staat.",
          voorbeeldblok([
            ("09:40 \u2014 telefoon tijdens een kleuring", "De AI-telefonist neemt op, noemt de salonnaam, hoort dat het om knippen gaat en plant donderdag 15:00 in."),
            ("12:15 \u2014 vraag via Instagram", "Beantwoord met de openingstijden en een link naar de agenda. U heeft het bericht niet eens gezien."),
            ("17:00 \u2014 herinneringen morgen", "Alle klanten van morgen krijgen een bericht. E\u00e9n verzet zelf naar volgende week; dat blok komt vrij en wordt opnieuw geboekt."),
            ("19:30 \u2014 review", "De klant van vanmiddag krijgt een verzoek om een beoordeling en laat er een achter."),
          ]), "voorbeelden"),

   sectie("Zichtbaarheid", "Wat social media in een salon doet.",
          "Product van de maand, de agenda van volgende week, een nieuwe medewerker, een tip over haar in de winter \u2014 en vooral beeld. <a href=\"social-media.html\">Zo werkt onze social-mediadienst</a>.",
          voorbeeldblok([
            ("Voor-en-na", "Een kleuring of coupe in beeld. Beeld is in deze branche het halve werk, en het ligt al op uw telefoon."),
            ("Google-aanbiedingen", "Werken hier uitzonderlijk goed, omdat mensen een kapper letterlijk in de kaart zoeken."),
            ("Een stilstaand profiel valt op", "Een salon waarvan de laatste post maanden oud is, wekt de indruk dat het er rustig is."),
          ]), "zichtbaarheid"),

]),
},

# ──────────────────────── GARAGEBEDRIJVEN ────────────────────────
{
 "bestand": "ai-voor-garagebedrijven.html",
 "groep": "branche",
 "dienst": "AI voor garagebedrijven",
 "titel": "AI en automatisering voor garages | Complete AI",
 "beschrijving": "APK-herinneringen die vanzelf verstuurd worden, een telefoon die wordt opgenomen terwijl u onder een auto ligt en klanten die horen dat hun auto klaar staat.",
 "omschrijving": "Automatisering voor garagebedrijven en autobedrijven: APK-herinneringen, online afspraken, een AI-telefonist voor in de werkplaats, statusberichten en facturatie zonder handwerk.",
 "ogen": "Voor garagebedrijven",
 "h1": 'U ligt onder een auto. <span class="glans">De telefoon wordt opgenomen.</span>',
 "lead": "In een werkplaats is de telefoon het lastigste apparaat dat er staat. Hij gaat wanneer u vuile handen heeft, en wie niemand krijgt belt de garage verderop. Complete AI zorgt dat gesprekken worden aangenomen, APK-klanten vanzelf terugkomen en de administratie meeloopt met het werk in plaats van erachteraan.",
 "levertijd": "Herinneringen binnen enkele werkdagen \u00b7 telefoon binnen 2 weken",
 "uitkomsten": [
     ("100%", "van de APK-klanten krijgt op tijd bericht, zonder dat iemand een lijst bijhoudt"),
     ("24/7", "bereikbaar, ook \u2019s avonds en in het weekend"),
     ("0", "handmatige stappen tussen werkorder en factuur"),
 ],
 "slot_kop": "Een half uur, aan de balie.",
 "slot_tekst": "Wij komen langs op een rustig moment en kijken mee met hoe het nu loopt: de telefoon, de planning, de APK-lijst en de facturatie. Daarna weet u waar de tijd verdwijnt. Kosteloos en vrijblijvend.",
 "vragen": [
   ("Wij werken met een garagepakket. Moet dat eruit?",
    "Nee, en dat zouden wij ook niet adviseren. Uw pakket blijft de basis; wij zetten er onderdelen omheen die het pakket zelf niet doet \u2014 de telefoon aannemen, klanten op tijd bereiken, statusberichten versturen. Waar koppelen mogelijk is, koppelen we."),
   ("Kan een AI-telefonist een technische vraag aan?",
    "Voor eenvoudige vragen wel: openingstijden, of een APK deze week nog kan, wat een beurt inhoudt. Wordt het technisch of gaat het om schade en garantie, dan schakelt hij door of noteert hij een terugbelverzoek met transcript. U bepaalt zelf waar die grens ligt."),
   ("Hoe komt de garage aan de APK-data?",
    "Uit uw eigen systeem of uit de klantenlijst die u al bijhoudt. Wij bouwen daar de herinnering omheen: een bericht ruim voor de vervaldatum, met een link om direct in te plannen. Wat er in uw administratie staat blijft leidend."),
   ("Krijgen klanten bericht als de auto klaar is?",
    "Ja, en dat is het onderdeel waar klanten het meest enthousiast over zijn. Zodra de werkorder op gereed staat, gaat er automatisch een bericht uit. Dat scheelt de balie een reeks telefoontjes per dag."),
   ("Hoe lang duurt het voordat dit staat?",
    "Herinneringen, statusberichten en facturatie zijn binnen enkele werkdagen operationeel. De AI-telefonist staat binnen twee weken, omdat we die eerst met u afstemmen en testen."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("De situatie", "Waar het in een werkplaats standaard misgaat.",
          "Niet door slordigheid, maar doordat het werk in de werkplaats en het werk aan de balie om dezelfde persoon vragen.",
          pijnblok([
            ("Gemiste gesprekken", "De telefoon gaat op het slechtst denkbare moment. Wie geen gehoor krijgt, belt de volgende garage."),
            ("APK-klanten die wegblijven", "De herinnering is afhankelijk van iemand die eraan denkt. Bij drukte blijft de lijst liggen."),
            ("De balie belt de hele dag", "\u201cUw auto staat klaar\u201d is tien keer per dag hetzelfde gesprek."),
            ("Facturen die achterlopen", "De werkorder is klaar, de factuur volgt dagen later. Dat kost rechtstreeks werkkapitaal."),
          ]), "herkenbaar"),

   sectie("Wat wij inrichten", "Vijf onderdelen, elk gericht op \u00e9\u00e9n knelpunt.",
          "U kiest welke u nodig heeft. Wat er al goed loopt, laten wij staan.",
          krijgtblok([
            ("APK-herinnering die vanzelf gaat", "Ruim voor de vervaldatum bericht, met een link om direct een moment te kiezen. Niemand hoeft een lijst bij te houden."),
            ("Een AI-telefonist voor de werkplaats", "Neemt op in het Nederlands, kent uw diensten, plant in en schakelt door wanneer het technisch wordt."),
            ("Online een afspraak maken", "Klanten kiezen zelf een moment binnen uw planning, ook buiten openingstijden."),
            ("Statusbericht bij gereed", "Zodra de werkorder gereed is, krijgt de klant automatisch bericht. Dat scheelt de balie tientallen gesprekken per week."),
            ("Factuur direct na afronding", "De factuur volgt op de werkorder, met een herinnering wanneer er niet wordt betaald. Zonder tussenkomst."),
          ]), "wat-wij-inrichten"),

   sectie("Voorbeelden", "Een doordeweekse dag in de werkplaats.",
          "Elk van deze handelingen gebeurt zonder dat iemand aan de balie staat.",
          voorbeeldblok([
            ("08:20 \u2014 telefoon terwijl u aan het werk bent", "De AI-telefonist neemt op, hoort dat het om een APK gaat en plant donderdagochtend in."),
            ("11:00 \u2014 APK-lijst voor volgende maand", "Alle klanten met een vervaldatum in november krijgen bericht. U heeft er niets voor gedaan."),
            ("15:30 \u2014 auto gereed", "De werkorder gaat op gereed; de klant krijgt direct bericht en komt om 17:00 langs."),
            ("17:05 \u2014 factuur", "De factuur staat in de mailbox van de klant voordat de auto de straat uit is."),
          ]), "voorbeelden"),

   sectie("Zichtbaarheid", "Wat social media bij een garage doet.",
          "Een binnengekomen inruil, een afgeronde reparatie, en de seizoensberichten die in deze branche vanzelf spreken. <a href=\"social-media.html\">Zo werkt onze social-mediadienst</a>.",
          voorbeeldblok([
            ("De klus die opviel", "Een inruil die net binnen is, of een reparatie waar iets bijzonders aan zat."),
            ("Reviews zijn hier doorslaggevend", "Mensen kiezen een garage op vertrouwen, en dat vertrouwen bouwt zich op in de reviews \u00e9n in de reactie daarop."),
            ("Seizoen en uitleg", "Banden wisselen bij de eerste vorst, de APK als herinneringsbericht, uitleg over waar die waarschuwingslamp voor staat."),
          ]), "zichtbaarheid"),

]),
},

# ─────────────────────────────── HORECA ───────────────────────────────
{
 "bestand": "ai-voor-de-horeca.html",
 "groep": "branche",
 "dienst": "AI voor de horeca",
 "titel": "AI en automatisering voor de horeca | Complete AI",
 "beschrijving": "Reserveringen die vanzelf binnenkomen, herinneringen tegen no-shows en een AI-telefonist die opneemt wanneer de zaak vol staat.",
 "omschrijving": "Automatisering voor restaurants, caf\u00e9s en afhaalzaken: online reserveren, een AI-telefonist tijdens de service, bevestiging en herinnering tegen no-shows, en reviews die vanzelf binnenkomen.",
 "ogen": "Voor de horeca",
 "h1": 'Midden in de service. <span class="glans">De telefoon wordt gewoon opgenomen.</span>',
 "lead": "Een gemiste reservering is geen administratieve kwestie maar een lege tafel. En het uur waarin de telefoon het vaakst gaat, is precies het uur waarin niemand hem kan aannemen. Complete AI zorgt dat reserveringen binnenkomen en worden nagekomen, ook wanneer de zaak vol staat.",
 "levertijd": "Reserveringen binnen enkele werkdagen \u00b7 telefoon binnen 2 weken",
 "uitkomsten": [
     ("24/7", "reserveringen aannemen, ook wanneer de zaak gesloten is"),
     ("2\u00d7", "bevestiging en herinnering, met de mogelijkheid zelf te annuleren"),
     ("0", "gemiste gesprekken tijdens de drukte"),
 ],
 "slot_kop": "Een half uur, buiten de service om.",
 "slot_tekst": "\u2019s Ochtends of op een sluitingsdag: wij komen langs en brengen in kaart hoeveel gesprekken u misloopt, hoeveel no-shows u heeft en wat daarvan te ondervangen valt. Kosteloos en vrijblijvend.",
 "vragen": [
   ("Wij hebben al een reserveringssysteem. Vervangt dit dat?",
    "Alleen als u dat wilt. Werkt uw systeem naar behoren, dan laten wij het staan en zorgen wij dat de telefoon en de bevestigingen erop aansluiten. De winst zit niet in een ander systeem, maar in de gesprekken die nu onbeantwoord blijven."),
   ("Kan een AI-telefonist ook afhaalbestellingen aannemen?",
    "Ja. Hij kent de kaart, neemt de bestelling op, controleert of alles beschikbaar is en noemt een afhaaltijd. Het gesprek komt in tekst binnen, zodat de keuken meteen kan beginnen."),
   ("Wat als de zaak volgeboekt is?",
    "Dan meldt hij dat, biedt een ander tijdstip of een andere dag aan en legt desgewenst een wachtlijstverzoek vast. Wat hij wel en niet mag toezeggen bepaalt u vooraf."),
   ("Helpt dit tegen no-shows?",
    "Ja. Een bevestiging en een herinnering met een annuleerknop is het middel dat structureel werkt: wie niet komt, laat het dan wél weten, en die tafel is opnieuw te vergeven. Hoeveel dat in uw zaak scheelt, ziet u terug in uw eigen cijfers."),
   ("Hoe snel staat dit?",
    "Online reserveren, bevestigingen en herinneringen zijn binnen enkele werkdagen operationeel. De AI-telefonist staat binnen twee weken."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("De situatie", "Waar in de horeca omzet weglekt.",
          "Alle vier hebben dezelfde oorzaak: de drukste uren zijn ook de uren waarin er niemand vrij is.",
          pijnblok([
            ("De telefoon tijdens de service", "Precies wanneer de zaak vol staat. Wie geen gehoor krijgt, reserveert ergens anders."),
            ("No-shows", "Een tafel die leeg blijft en te laat is om nog te vergeven."),
            ("Reserveringen via vier kanalen", "Telefoon, mail, Instagram en de deur. Zonder \u00e9\u00e9n overzicht gaat het vroeg of laat mis."),
            ("Reviews die uitblijven", "Voor een zaak die van vindbaarheid leeft, is dat een gemis dat direct in het kaartje van Google zichtbaar is."),
          ]), "herkenbaar"),

   sectie("Wat wij inrichten", "Vier onderdelen die de drukte opvangen.",
          "U bepaalt wat u nodig heeft. Wat al goed loopt, blijft staan.",
          krijgtblok([
            ("Online reserveren", "Gasten kiezen zelf een tafel en tijdstip binnen uw capaciteit, ook wanneer de zaak dicht is."),
            ("Een AI-telefonist tijdens de service", "Neemt op in het Nederlands, kent de openingstijden en de kaart, neemt reserveringen en afhaalbestellingen aan."),
            ("Bevestiging en herinnering", "Direct een bevestiging, en kort van tevoren een herinnering met een annuleerknop. Wie afzegt, maakt de tafel weer vrij."),
            ("Reviews die vanzelf binnenkomen", "Na het bezoek automatisch een verzoek om een beoordeling \u2014 het onderdeel dat het meest bijdraagt aan uw positie in Google."),
          ]), "wat-wij-inrichten"),

   sectie("Voorbeelden", "Een vrijdagavond.",
          "Geen van deze handelingen onderbreekt de service.",
          voorbeeldblok([
            ("18:45 \u2014 telefoon tijdens het eerste rondje", "De AI-telefonist neemt op, hoort dat het om vier personen om 20:30 gaat en boekt de tafel."),
            ("19:10 \u2014 afhaalbestelling", "Bestelling opgenomen, beschikbaarheid gecontroleerd, afhaaltijd genoemd. In tekst binnen bij de keuken."),
            ("21:00 \u2014 herinnering voor morgen", "Alle gasten van morgen krijgen bericht. E\u00e9n zegt af; die tafel gaat opnieuw open."),
            ("23:30 \u2014 review", "De gasten van vanavond krijgen een verzoek om een beoordeling."),
          ]), "voorbeelden"),

   sectie("Zichtbaarheid", "Wat social media in de horeca doet.",
          "Hier is het Google-bedrijfsprofiel bijna belangrijker dan de website. <a href=\"social-media.html\">Zo werkt onze social-mediadienst</a>.",
          voorbeeldblok([
            ("Het gerecht van vandaag", "De wisseling van de kaart, een volle zaak op vrijdagavond, een evenement dat eraan komt."),
            ("Mensen beslissen in de kaart", "Ze zoeken, kijken naar de foto\u2019s en de laatste berichten, en kiezen daar. Niet op uw website."),
            ("Foto\u2019s van vorig jaar kosten gasten", "Letterlijk. Gewijzigde openingstijden horen er om dezelfde reden meteen op te staan."),
          ]), "zichtbaarheid"),

]),
},

# ────────────────────── BOUW EN INSTALLATIE ──────────────────────
{
 "bestand": "ai-voor-bouw-en-installatie.html",
 "groep": "branche",
 "dienst": "AI voor bouw en installatie",
 "titel": "AI en automatisering voor bouw en installatie | Complete AI",
 "beschrijving": "Aanvragen aannemen terwijl u op de steiger staat, offertes die klaarstaan en facturen die vanzelf de deur uit gaan.",
 "omschrijving": "Automatisering voor aannemers, installateurs, loodgieters en klusbedrijven: een AI-telefonist tijdens het werk, aanvragen die direct worden vastgelegd, offertes, urenregistratie en facturatie zonder avondwerk.",
 "ogen": "Voor bouw &amp; installatie",
 "h1": 'U staat op de steiger. <span class="glans">De aanvraag wordt vastgelegd.</span>',
 "lead": "In de bouw en de installatietechniek is de telefoon een probleem met twee kanten: opnemen kan niet, en niet opnemen kost een opdracht. Daar bovenop komt het avondwerk \u2014 offertes, uren, facturen. Complete AI zorgt dat aanvragen binnenkomen terwijl u werkt en dat de papieren kant meeloopt in plaats van zich op te stapelen.",
 "levertijd": "Administratie binnen enkele werkdagen \u00b7 telefoon binnen 2 weken",
 "uitkomsten": [
     ("24/7", "bereikbaar, ook wanneer u op een dak of in een kruipruimte zit"),
     ("1 dag", "van aanvraag naar offerte, in plaats van een week"),
     ("0", "avonden per week aan facturen en herinneringen"),
 ],
 "slot_kop": "Een half uur, in de bus of aan de keukentafel.",
 "slot_tekst": "Wij komen langs of bellen op een moment dat het uitkomt. In een half uur brengen we in kaart hoeveel aanvragen u misloopt en hoeveel avonden per week aan administratie opgaan. Kosteloos en vrijblijvend.",
 "vragen": [
   ("Kan een AI-telefonist een spoedgeval herkennen?",
    "Ja, en dat is voor een installateur het belangrijkste onderdeel. U bepaalt vooraf welke situaties als spoed gelden \u2014 een lekkage, een storing zonder warmte \u2014 en die schakelt hij direct naar u door. Alles wat kan wachten, legt hij vast als terugbelverzoek met volledig transcript."),
   ("Schrijft het de offerte zelf?",
    "Niet zelfstandig, en dat zou ook niet verstandig zijn: u bepaalt de prijs. Wat het wel doet, is de aanvraag volledig uitvragen en een concept klaarzetten met de gegevens, het werk en uw standaardposten. U kijkt na, past aan en verstuurt. Dat scheelt het grootste deel van het avondwerk."),
   ("Wij werken met een boekhoudpakket. Blijft dat?",
    "Ja. Wij vervangen uw boekhouding niet, wij zorgen dat er niets met de hand ingevoerd hoeft te worden. Waar een koppeling mogelijk is leggen we die; waar dat niet kan, hoort u dat in de intake."),
   ("Hoe zit het met urenregistratie?",
    "Uren worden per project vastgelegd, met een eenvoudige handeling vanaf de telefoon. Aan het eind van het werk staan ze klaar voor de factuur, zodat er niets meer teruggezocht hoeft te worden."),
   ("Hoe snel staat dit?",
    "Offertes, urenregistratie, facturatie en herinneringen zijn binnen enkele werkdagen operationeel. De AI-telefonist staat binnen twee weken."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("De situatie", "Waar de dag van een vakman eindigt.",
          "Niet om vijf uur. De vier onderdelen hieronder zijn de reden.",
          pijnblok([
            ("Bellen kan niet tijdens het werk", "Op een dak, in een kruipruimte of met een machine aan. Wie geen gehoor krijgt, belt de volgende."),
            ("Offertes schrijven \u2019s avonds", "En hoe langer een offerte duurt, hoe kleiner de kans dat de opdracht nog van u is."),
            ("Uren die achteraf gereconstrueerd worden", "Wat betekent dat er uren verdwijnen die wel gemaakt zijn."),
            ("Facturen en herinneringen die blijven liggen", "De klus is af, het geld staat er niet. Dat kost rechtstreeks werkkapitaal."),
          ]), "herkenbaar"),

   sectie("Wat wij inrichten", "Vijf onderdelen die de avonden teruggeven.",
          "U kiest wat u nodig heeft. Elk onderdeel functioneert zelfstandig.",
          krijgtblok([
            ("Een AI-telefonist die aanvragen aanneemt", "Neemt op tijdens het werk, vraagt uit wat er aan de hand is, herkent spoed en schakelt die direct door."),
            ("Aanvraag meteen vastgelegd", "Naam, adres, aard van het werk en gewenste termijn komen als tekst binnen. U hoeft niets terug te bellen om te achterhalen waar het over ging."),
            ("Offerte binnen \u00e9\u00e9n dag", "Een concept staat klaar met uw standaardposten. U kijkt na, past aan, verstuurt \u2014 in plaats van vanaf niets te beginnen."),
            ("Urenregistratie per project", "Vastgelegd tijdens het werk, klaar voor de factuur. Zonder terugzoeken."),
            ("Facturatie en herinneringen", "De factuur volgt op de afgeronde klus, en wie niet betaalt krijgt automatisch een herinnering. Zonder ongemakkelijk telefoontje."),
          ]), "wat-wij-inrichten"),

   sectie("Voorbeelden", "Een gewone werkdag.",
          "Geen van deze handelingen onderbreekt het werk.",
          voorbeeldblok([
            ("10:15 \u2014 telefoon terwijl u op een dak staat", "De AI-telefonist neemt op, hoort dat het om een offerte voor een badkamer gaat en legt de aanvraag volledig vast."),
            ("10:40 \u2014 een lekkage", "Als spoed herkend en direct naar uw mobiel doorgeschakeld. Die neemt u wél aan."),
            ("16:50 \u2014 klus afgerond", "Uren staan al vast; de factuur gaat dezelfde dag de deur uit."),
            ("Vrijdag \u2014 openstaande posten", "Twee klanten hebben nog niet betaald. Beiden krijgen automatisch een herinnering."),
          ]), "voorbeelden"),

   sectie("Zichtbaarheid", "Wat social media bij een vakbedrijf doet.",
          "In deze branche is de klus in beeld niet een onderdeel van de dienst \u2014 het \u00eds de dienst. <a href=\"social-media.html\">Zo werkt onze social-mediadienst</a>.",
          voorbeeldblok([
            ("Voor, tijdens, na", "Het overtuigendste bewijs dat er bestaat, en u maakt die foto\u2019s toch al."),
            ("De vraag die iedereen stelt", "Over vergunningen, subsidies of doorlooptijd \u2014 precies wat mensen in Google intypen."),
            ("Het beste materiaal ligt ongebruikt", "Deze branche heeft de mooiste beelden liggen en gebruikt ze het minst. \u00c9\u00e9n appje per week lost dat op."),
          ]), "zichtbaarheid"),

]),
},

# ───────────────────────────── SOCIAL MEDIA ─────────────────────────────
{
 "bestand": "social-media.html",
 "dienst": "Social media",
 "titel": "Social media uitbesteden: wekelijks beheer | Complete AI",
 "beschrijving": "Social media beheer uitbesteden zonder uw accounts af te staan: berichten in uw huisstijl en een wekelijks bijgehouden Google-bedrijfsprofiel.",
 "omschrijving": "Social media uitbesteden voor lokale bedrijven: Google-bedrijfsprofiel en social media wekelijks bijgehouden, berichten in uw huisstijl vooraf ter goedkeuring, reviews beantwoord en een maandrapport over zichtbaarheid in plaats van over likes.",
 "ogen": "Social media",
 "h1": 'Social media uitbesteden: <span class="glans">elke week zichtbaar, zonder dat het u tijd kost</span>.',
 "lead": "Social media uitbesteden betekent dat iemand anders uw berichten bedenkt, opmaakt, plaatst en bijhoudt, terwijl de accounts van u blijven. Complete AI doet dat wekelijks voor uw Google-bedrijfsprofiel en uw social media, in uw huisstijl. U keurt de maand vooraf goed en stuurt af en toe een foto.",
 "levertijd": "Eerste bericht binnen een week",
 "gewijzigd": "2026-09-24",
 "uitkomsten": [
     ("1 uur", "eenmalig — dat is alles wat wij van uw kant nodig hebben om te beginnen"),
     ("5 min", "per maand om de kalender goed te keuren, en dat mag later vervallen"),
     ("7/7", "er wordt geplaatst, ook in vakanties en drukke weken"),
 ],
 "slot_kop": "Hoe zichtbaar bent u nu eigenlijk?",
 "slot_tekst": "In een half uur kijken we samen naar uw bedrijfsprofiel, uw bestaande accounts en wat de bedrijven om u heen doen. U krijgt een eerlijk beeld van waar u staat — ook wanneer de conclusie is dat u hier niets voor nodig heeft.",
 "vragen": [
   ("Wat kost social media uitbesteden?",
    "Dat hangt af van het aantal kanalen, het aantal berichten per week, video, het beantwoorden van reviews en een eventuele koppeling met advertenties. Daarom noemen wij geen bedrag vooraf. Na de intake ligt er één vaste prijs op papier, zonder nacalculatie. De dienst is maandelijks opzegbaar."),
   ("Wat is het uurtarief van een social media manager?",
    "Wij werken niet met een uurtarief. Een uurtarief zegt weinig zolang niet vaststaat hoeveel uur een maand kost. Na de intake ligt er één vaste prijs op papier, zonder nacalculatie, voor een afgesproken pakket. U weet dus vooraf wat er per maand staat en wat u daarvoor krijgt."),
   ("Hoe noemt u iemand die de social media van een bedrijf beheert?",
    "Zo iemand heet een social media manager, soms ook contentspecialist. Verwant is de functie social media specialist. De omgang met volgers heet community management. De taken zijn strategie, plannen en plaatsen, reageren op vragen en reacties, en rapporteren. Bij uitbesteden neemt een bureau of freelancer die taken over."),
   ("Hoeveel verdient een social media manager?",
    "Dat hangt af van ervaring en opleiding, en verschilt per dienstverband. Salarisoverzichten staan op vacaturesites; wij noemen hier geen bedragen. Bij uitbesteden speelt salaris geen rol: u betaalt voor een afgesproken pakket met één vaste prijs, zonder nacalculatie, en niet voor een medewerker in dienst."),
   ("Wat besteedt u precies uit als u social media uitbesteedt?",
    "U besteedt het ritme uit: het bedenken, opmaken en plaatsen van berichten, het bijhouden van uw Google-bedrijfsprofiel, het beantwoorden van reviews en het maandrapport. Van u blijven de accounts, de goedkeuring van de kalender en af en toe een foto. Uitbesteden werkt niet zonder invoer van u."),
   ("Welke kanalen beheert Complete AI?",
    "Het Google-bedrijfsprofiel, Instagram, een Facebook-pagina en een LinkedIn-bedrijfspagina. TikTok kan op verzoek en in overleg, Pinterest alleen bij interieur, bouw, horeca en mode. Het Google-bedrijfsprofiel is de kern van de dienst. Welke kanalen bij u passen, bepalen we in de intake."),
   ("Hoe snel staat het eerste bericht online?",
    "Het eerste bericht staat binnen een week. Daarvoor zijn een intake van een half uur en één inrichtingsgesprek van ongeveer een uur nodig. Daarna zetten wij de profielen op orde, maken de merkkit en sturen u de kalender van de eerste maand ter goedkeuring."),
   ("Ik heb geen tijd om foto’s aan te leveren. Werkt het dan wel?",
    "Ja, maar minder goed, en dat zeggen we liever vooraf. Zonder eigen beeldmateriaal maken wij berichten op basis van uw diensten, het seizoen en veelgestelde vragen; dat houdt uw profiel actueel. Eén foto per week tilt het van correct naar overtuigend. Daarom is het versturen zo eenvoudig mogelijk gemaakt: een appje, verder niets."),
   ("Moet ik mijn wachtwoorden afgeven?",
    "Nee, en dat zouden wij ook niet willen. Wij krijgen toegang via de officiële beheeromgevingen van Google en Meta, waar u ons als beheerder toevoegt. Uw accounts blijven van u, wij kunnen alleen wat u ons toestaat, en u trekt die toegang in één handeling weer in."),
   ("Wat als ik het niet eens ben met een bericht?",
    "U ziet de kalender voordat er iets naar buiten gaat en geeft in diezelfde link aan wat er anders moet. Er gaat niets ongezien de deur uit, tenzij u zelf aangeeft dat die stap mag vervallen. Het beoordelen kost ongeveer vijf minuten per maand."),
   ("Krijg ik hier meer klanten van?",
    "Wij sturen op zichtbaarheid, en dat is precies wat u maandelijks terugziet: hoe vaak u in Google bent getoond, op welke zoekopdrachten, hoe vaak er vanaf uw profiel is gebeld, hoe vaak er een route naar u is aangevraagd en hoe vaak er naar uw site is doorgeklikt. Dat zijn Googles eigen cijfers, en u kunt ze zelf nakijken."),
   ("Waarom legt Complete AI zoveel nadruk op Google en niet op Instagram?",
    "Omdat daar het verschil zit tussen zichtbaar zijn en vermaakt worden. Een bericht op Instagram staat in de tijdlijn van wie u volgt. Uw Google-bedrijfsprofiel staat er op het moment dat iemand zoekt naar uw bedrijf of naar wat u verkoopt. Wij doen allebei, maar het rapport gaat over het tweede."),
   ("Wordt dit met kunstmatige intelligentie gemaakt?",
    "Deels, en dat is waarom het vol te houden is. De opzet, de teksten en het opmaken van beeld gebeuren geautomatiseerd; de keuzes over wat er wordt verteld komen uit het inrichtingsgesprek en uit wat u aanlevert. Wat er niet gebeurt: verzonnen klantverhalen, verzonnen reviews, of beelden van mensen en panden die niet bestaan."),
   ("Kan ik ermee stoppen?",
    "Ja. De dienst is maandelijks opzegbaar en er is geen jaarcontract. De profielen, de merkkit en alles wat er geplaatst is, blijven van u."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   inhoudsopgave([
     ("herkenbaar", "Waarom accounts stilvallen"),
     ("uitbesteden", "Wat betekent social media uitbesteden?"),
     ("wat-u-krijgt", "Wat u krijgt"),
     ("goedkeuring", "Hoe werkt goedkeuring, en wat is uw aandeel?"),
     ("de-keuze", "Likes zijn geen doel"),
     ("google-bedrijfsprofiel", "Social media en het Google-bedrijfsprofiel"),
     ("voerlijn", "Van foto naar bericht"),
     ("rubrieken", "Vaste rubrieken"),
     ("kanalen", "Welke kanalen?"),
     ("resultaat", "Hoe wordt het resultaat gemeten?"),
     ("vertrekpunten", "Drie vertrekpunten"),
     ("kosten", "Wat kost social media uitbesteden?"),
     ("werkwijze", "Werkwijze"),
     ("social-media-manager", "Wat doet een social media manager?"),
     ("bronnen", "Bronnen"),
   ]),

   sectie("De situatie", "Het is geen gebrek aan wil. Het is een gebrek aan ritme.",
          "Social media beheer uitbesteden is zinvol wanneer het ritme ontbreekt en niet de wil. Social media vraagt geen groot talent, maar wekelijkse aandacht — en dat is precies wat een ondernemer met een volle agenda niet structureel kan opbrengen.",
          pijnblok([
            ("Het account staat stil", "De laatste post is van maanden geleden. Dat leest als een bedrijf waar het rustig is."),
            ("Vijf berichten in één week, daarna niets", "Zichtbaarheid komt van regelmaat, niet van vlagen."),
            ("Het bedrijfsprofiel is nooit meer aangeraakt", "Berichten op een Google-bedrijfsprofiel worden na zes maanden gearchiveerd, tenzij er een periode is ingesteld. Een profiel dat niemand bijhoudt, toont na verloop van tijd geen nieuws meer."),
            ("Er ligt genoeg materiaal, het komt er nooit uit", "De foto’s van het mooiste werk staan op de telefoon en blijven daar."),
          ]), "herkenbaar"),

   proza("Uitbesteden", "Wat betekent social media uitbesteden?", """        <p>Social media uitbesteden betekent dat een ander het ritme overneemt: het bedenken van de maand, het opmaken van de berichten, het plaatsen op de juiste momenten, het bijhouden van uw Google-bedrijfsprofiel, het beantwoorden van reviews en het rapport achteraf. Wat van u blijft, zijn uw accounts, uw akkoord en het beeld van uw eigen werk.</p>
        <h3>Zelf doen, iemand in dienst nemen of uitbesteden</h3>
        <div class="tabelwrap"><table>
          <thead><tr><th>Optie</th><th>Wat het van u vraagt</th><th>Bij vakantie, ziekte en drukte</th></tr></thead>
          <tbody>
            <tr><td><strong>Zelf doen</strong></td><td>Elke week tijd, naast uw eigenlijke werk. Geen vast verband.</td><td>Het stopt zodra het druk wordt.</td></tr>
            <tr><td><strong>Iemand in dienst</strong></td><td>Aansturen, en een dienstverband met alles wat daarbij hoort.</td><td>Het valt weg wanneer die persoon er niet is.</td></tr>
            <tr><td><strong>Uitbesteden</strong></td><td>Eenmalig ongeveer een uur, daarna vijf minuten per maand. Maandelijks opzegbaar.</td><td>Het ritme loopt door, ook in vakanties en drukke weken.</td></tr>
          </tbody>
        </table></div>
        <h3>Wat u niet uitbesteedt</h3>
        <p>Uw accounts blijven van u. U geeft akkoord op de kalender, zolang u dat wilt. En u levert af en toe een foto van wat u doet, omdat een bericht zonder eigen beeld algemener blijft. Uitbesteden werkt dus niet zonder invoer van u, maar die invoer is klein en staat vast: zie <a href="#goedkeuring">hoe goedkeuring werkt</a>.</p>
        <p>Het Google-bedrijfsprofiel hoort bij uw vindbaarheid in Google. Over het zoekverkeer zelf leest u meer bij <a href="vindbaarheid-seo.html">vindbaarheid (SEO)</a>.</p>""", "uitbesteden"),

   sectie("Wat u krijgt", "Het ritme wordt overgenomen, de accounts blijven van u.",
          "U kiest wat u nodig heeft. Wat er al goed loopt, laten wij staan.",
          krijgtblok([
            ("Google-bedrijfsprofiel bijgehouden", "Wekelijks een update, aanbieding of foto. Dit is het onderdeel dat direct in Google Search en Maps zichtbaar is, en waarvan Google zelf de cijfers geeft."),
            ("Berichten in uw huisstijl", "Uw kleuren, uw lettertype, uw manier van praten. Een profiel dat er als één geheel uitziet."),
            ("Een WhatsApp-nummer voor uw foto’s", "U stuurt een foto van een afgerond werk, wij maken er het bericht van. Meer hoeft u niet te doen."),
            ("Vaste rubrieken in plaats van losse invallen", "Klus in beeld, de vraag van de week, seizoen, team, review. Zo blijft het gevarieerd en herkenbaar."),
            ("Vooraf zichtbaar, achteraf verantwoord", "U ziet de maand vooruit en keurt hem in vijf minuten goed. Achteraf krijgt u een rapport."),
            ("Reviews beantwoord", "Binnen één werkdag, ook de kritische. Google noemt reageren op reviews een manier om te laten zien dat u feedback waardeert."),
            ("Uw accounts blijven van u", "Wij werken via de officiële beheeromgevingen. Geen wachtwoorden, en u trekt de toegang in één handeling weer in."),
            ("Maandelijks opzegbaar", "Geen jaarcontract. Wat er staat, blijft van u."),
          ]), "wat-u-krijgt"),

   proza("Goedkeuring", "Hoe werkt goedkeuring, en wat is uw aandeel?", """        <p>Er gaat niets ongezien de deur uit, tenzij u zelf aangeeft dat die stap mag vervallen. De volgorde is elke maand dezelfde.</p>
        <ol>
          <li><strong>Inrichting, eenmalig.</strong> Een gesprek van ongeveer een uur over uw diensten, uw klanten, uw manier van praten en wat er absoluut niet gezegd mag worden.</li>
          <li><strong>Kalender.</strong> U ontvangt de maand vooruit in één link, ter goedkeuring.</li>
          <li><strong>Uw reactie.</strong> Bent u het ergens niet mee eens, dan geeft u in diezelfde link aan wat er anders moet. Dat verwerken wij voordat er iets wordt geplaatst.</li>
          <li><strong>Plaatsing.</strong> Na uw akkoord staan de berichten op de juiste momenten op de juiste kanalen.</li>
          <li><strong>Rapport.</strong> Achteraf ontvangt u een rapport in gewone taal.</li>
        </ol>
        <h3>Wat u zelf doet, en dat is alles</h3>
        <ul>
          <li><strong>Eenmalig ongeveer een uur.</strong> Het inrichtingsgesprek. Daarna hoeft dat niet meer.</li>
          <li><strong>Vijf minuten per maand.</strong> De kalender goedkeuren. Merkt u na een paar maanden dat u toch altijd akkoord geeft, dan mag die stap vervallen.</li>
          <li><strong>Af en toe een foto.</strong> Naar één WhatsApp-nummer. Geen verplichting en geen minimum: hoe meer u stuurt, hoe persoonlijker het wordt.</li>
        </ul>
        <h3>Wat u niet hoeft te doen</h3>
        <p>Geen wachtwoorden afgeven, geen inlogschermen, geen software leren. Wij krijgen toegang via de officiële beheeromgevingen van Google en Meta, waar u ons als beheerder toevoegt. Die toegang trekt u in één handeling weer in.</p>""", "goedkeuring"),

   sectie("De keuze erachter", "Likes zijn geen doel. Gevonden worden wel.",
          "Dit is waar deze dienst op rust. Wij doen allebei, maar wij zijn eerlijk over waar de opbrengst zit.",
          voorbeeldblok([
            ("Een bericht op Instagram of Facebook", "Staat in de tijdlijn van wie u volgt. Prettig voor herkenning en vertrouwen bij mensen die u al kennen."),
            ("Een bericht op uw Google-bedrijfsprofiel", "Staat op uw profiel in Google Search en Maps, op het moment dat iemand naar uw bedrijf kijkt. Google beschrijft berichten als een manier om nieuws, aanbiedingen en evenementen direct aan klanten te tonen."),
            ("Waarom wij allebei doen", "De zichtbare buitenkant is wat u zelf elke dag ziet, en waar u het vertrouwen aan ontleent dat er iets gebeurt. Het maandrapport gaat over het andere: vindbaarheid."),
          ]), "de-keuze"),

   proza("Google-bedrijfsprofiel", "Hoe werkt social media samen met uw Google-bedrijfsprofiel?", """        <p>Uw Google-bedrijfsprofiel is de vermelding die Google toont in Search en Maps wanneer iemand naar uw bedrijf zoekt, of in de buurt zoekt naar wat u levert. Social media en het profiel dienen hetzelfde doel: gevonden worden en vertrouwen wekken. Daarom houden wij ze samen bij.</p>
        <h3>Wat Google over lokale zichtbaarheid zegt</h3>
        <p>Google noemt drie factoren voor lokale resultaten: relevantie, afstand en bekendheid. Bekendheid hangt onder meer af van het aantal verwijzingen van andere sites en het aantal reviews. Google raadt aan de gegevens volledig en juist te houden, te reageren op reviews en foto’s en video’s toe te voegen. Een betere plek in de lokale resultaten is bij Google niet aan te vragen of te betalen.</p>
        <h3>Wat berichten op het profiel doen</h3>
        <p>Google beschrijft berichten als een manier om nieuws, aanbiedingen en evenementen direct aan klanten te tonen in Search en Maps. Dat helpt bezoekers bij hun keuze. In Googles tips voor de lokale rangschikking komen berichten niet voor. Wij zien ze daarom als middel om klanten te informeren, niet om hoger te komen. Berichten worden na zes maanden gearchiveerd, tenzij er een periode is ingesteld. Een profiel met alleen oude berichten toont dus geen nieuws.</p>
        <h3>Wat wij wekelijks doen</h3>
        <ul>
          <li>Een update, aanbieding of foto op het profiel plaatsen.</li>
          <li>Reviews beantwoorden binnen één werkdag, ook de kritische.</li>
          <li>Openingstijden, foto’s en berichten actueel houden.</li>
        </ul>
        <h3>Wie doet wat</h3>
        <p>De inrichting van het profiel valt onder <a href="vindbaarheid-seo.html">vindbaarheid (SEO)</a>. Het wekelijkse onderhoud valt onder social media. Wilt u ook dat klanten na een levering vanzelf om een review worden gevraagd, dan hoort dat bij <a href="automatisering.html">automatisering</a>.</p>""", "google-bedrijfsprofiel"),

   sectie("De voerlijn", "Het eenvoudigste onderdeel, en tegelijk het belangrijkste.",
          "Zonder invoer van uw kant maakt elk systeem — hoe geavanceerd ook — inwisselbare praatjes. Eén foto per week is genoeg om dat te voorkomen. Daarom is het versturen zo eenvoudig mogelijk gemaakt.",
          routeblok([
            ("U stuurt een foto", "Een afgerond werk, een volle zaak, een nieuwe levering, een tevreden klant. Naar één WhatsApp-nummer. Geen tekst, geen uitleg, geen inlogscherm."),
            ("Wij maken er het bericht van", "Bijsnijden, opknappen, tekst erbij, in uw huisstijl. Uw eigen beeld krijgt altijd voorrang boven gegenereerd beeld."),
            ("Het staat op het juiste moment op de juiste kanalen", "Geplaatst op de tijden die in uw branche werken, zeven dagen per week. Mislukt een plaatsing, dan wordt hij opnieuw aangeboden en merkt u er niets van."),
          ]) + "\n" + eerlijkblok(
            "Wat er niet gebeurt",
            "Berichten worden niet verzonnen. Concreet:",
            ["Geen verzonnen klantverhalen.",
             "Geen verzonnen reviews.",
             "Geen beelden van mensen en panden die niet bestaan."]),
          "voerlijn"),

   sectie("De inhoud", "Berichten worden niet verzonnen, maar uit vaste rubrieken opgebouwd.",
          "Dat voorkomt dat alles op elkaar gaat lijken, en het maakt de dienst maand na maand voorspelbaar. Welke rubrieken passen en in welke verhouding, verschilt per bedrijf: een garagebedrijf heeft een andere mix dan een kapsalon.",
          voorbeeldblok([
            ("Klus in beeld", "Een afgerond werk, een voor-en-na, een geleverd product. Het enige bewijs dat telt: wat u werkelijk doet."),
            ("De vraag van de week", "Eén veelgestelde klantvraag, beantwoord. Letterlijk wat iemand in Google intypt."),
            ("Aanbieding of actie", "Een tijdelijk aanbod, ook los te plaatsen als Google-aanbieding. Directe aanleiding tot contact."),
            ("Seizoen en agenda", "Weer, feestdagen, vakanties, lokale evenementen. Sluit aan bij waar mensen op dat moment mee bezig zijn."),
            ("Team en achter de schermen", "Wie er werkt en hoe het eraan toegaat. Maakt een bedrijf herkenbaar."),
            ("Review uitgelicht", "Een echte klantreactie, netjes vormgegeven. Sociale bewijskracht zonder zelf te hoeven opscheppen."),
            ("Tip van de vakman", "Praktisch advies uit het vak. Positioneert u als degene die het weet."),
            ("Mythe ontkracht", "Een hardnekkig misverstand uit uw branche rechtzetten. Laat zien dat u het vak kent."),
          ]), "rubrieken"),

   sectie("Kanalen", "Waar het geplaatst wordt, en waarom.",
          "Andere kanalen kunt u altijd navragen. In het voorstel staan alleen kanalen die wij betrouwbaar bijhouden.",
          voorbeeldblok([
            ("Google-bedrijfsprofiel", "Updates, aanbiedingen, evenementen, foto’s en reviewreacties. De kern van de dienst; hier zit de meetbare opbrengst."),
            ("Instagram", "Afbeelding, carrousel, korte video en Story. Vereist een zakelijk account dat aan een Facebook-pagina gekoppeld is — dat regelen wij."),
            ("Facebook-pagina", "Tekst, beeld, video en links. Voor veel branches nog altijd het kanaal waar de klanten daadwerkelijk zitten."),
            ("LinkedIn-bedrijfspagina", "Berichten en documenten. Alleen zinvol wanneer u aan zakelijke klanten levert."),
            ("TikTok", "Video, op verzoek en in overleg. Vraagt een aparte goedkeuringsprocedure en een ander soort inhoud."),
            ("Pinterest", "Pins. Alleen bij interieur, bouw, horeca en mode; daarbuiten levert het te weinig op."),
          ]) + """
      <div class="proza reveal">
        <h3>Drie vragen om kanalen te kiezen</h3>
        <ol>
          <li><strong>Waar zoeken uw klanten naar u?</strong> Zoeken ze op het moment dat ze iets nodig hebben, zoals een garage, een kapper of een installateur, dan begint het bij het Google-bedrijfsprofiel.</li>
          <li><strong>Waar kennen uw klanten u al?</strong> Bestaande klanten volgen u op het kanaal waar zij u tegenkomen. Kijk waar uw klanten u nu al vinden of vragen stellen.</li>
          <li><strong>Levert u aan bedrijven of aan particulieren?</strong> Voor zakelijke klanten past LinkedIn. Voor particulieren begint het bij Google en bij Facebook of Instagram.</li>
        </ol>
        <p>Begin bij één of twee kanalen die u kunt volhouden. Een kanaal dat stilvalt, leest als een bedrijf waar het rustig is. Het aantal kanalen bepaalt ook mee de omvang van het voorstel.</p>
      </div>""", "kanalen"),

   proza("Meten", "Hoe wordt het resultaat van social media beheer gemeten?", """        <p>Wij meten op zichtbaarheid en op wat mensen daarna doen. Likes zijn geen doel. De cijfers komen uit de prestatiegegevens die Google zelf geeft voor uw Google-bedrijfsprofiel, en u kunt ze zelf nakijken.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Cijfer</th><th>Wat het zegt</th></tr></thead>
          <tbody>
            <tr><td><strong>Weergaven</strong></td><td>Hoeveel mensen uw profiel hebben bekeken in Google Search en Maps.</td></tr>
            <tr><td><strong>Zoekopdrachten</strong></td><td>Welke zoektermen mensen gebruikten waarbij uw profiel verscheen.</td></tr>
            <tr><td><strong>Telefoontjes</strong></td><td>Hoe vaak iemand op de belknop van uw profiel tikte.</td></tr>
            <tr><td><strong>Routeverzoeken</strong></td><td>Hoeveel mensen een route naar uw bedrijf vroegen.</td></tr>
            <tr><td><strong>Websiteklikken</strong></td><td>Hoe vaak iemand vanaf uw profiel doorklikte naar uw site.</td></tr>
          </tbody>
        </table></div>
        <p>Google toont deze gegevens alleen bij een geverifieerd profiel, en alleen de cijfers die op uw bedrijf van toepassing zijn. Kent uw profiel ook chatberichten, boekingen of aanbiedingen, dan komen die cijfers eveneens in het overzicht.</p>
        <h3>Wat u elke maand ontvangt</h3>
        <p>Vooraf de kalender, achteraf een rapport in gewone taal. Het rapport gaat over de cijfers hierboven en over wat er die maand is geplaatst, niet over likes.</p>
        <h3>Wat u van het resultaat mag verwachten</h3>
        <p>Google schrijft zelf dat een betere plek in de lokale resultaten niet aan te vragen of te betalen is. Wat wel te sturen is, staat ook bij Google: volledige en juiste gegevens, foto’s en video’s en reacties op reviews. Daarnaast houden wij de berichten bij, waarmee u nieuws en aanbiedingen direct in Google toont. Het rapport laat elke maand zien of de cijfers de goede kant op gaan.</p>""", "resultaat"),

   sectie("Vertrekpunten", "Drie niveaus waar dit begint.",
          "Net als bij de pakketten op de homepage: dit zijn vertrekpunten, geen menukaart. Het aantal kanalen, de frequentie en de hoeveelheid werk verschillen per bedrijf, en de samenstelling volgt uit de intake.",
          krijgtblok([
            ("Zichtbaar blijven", "Voor de eenmanszaak die vooral gevonden wil worden. Google-bedrijfsprofiel wekelijks bijgehouden, één social kanaal met een paar berichten per week, de voerlijn via WhatsApp en een maandrapport over vindbaarheid. Past bij: hovenier, klusbedrijf, praktijk, adviseur."),
            ("Zichtbaar zijn", "Voor het bedrijf met personeel dat er verzorgd op wil staan. Meerdere kanalen, hogere frequentie, korte video’s per maand, reviews die beantwoord worden en een kwartaalgesprek. Past bij: kapsalon, garagebedrijf, restaurant, makelaar, praktijk."),
            ("De eerste zijn in de regio", "Voor wie lokaal de bekendste wil worden. Dagelijkse aanwezigheid op alle kanalen, wekelijkse video, volledige profieloptimalisatie, reviewbeheer, en de koppeling naar advertenties zodat het beste bericht ook bij nieuwe mensen terechtkomt. Past bij: bedrijven met meerdere vestigingen of een lopend advertentiebudget."),
          ]), "vertrekpunten"),

   proza("Kosten", "Wat kost social media uitbesteden?", """        <p>Op deze pagina staan geen bedragen en geen uurtarief. Wat het kost, hangt af van wat u afneemt, en dat verschilt per bedrijf.</p>
        <h3>Wat de omvang bepaalt</h3>
        <ul>
          <li>Het aantal kanalen waarop wordt geplaatst.</li>
          <li>Het aantal berichten per week.</li>
          <li>Korte video’s, en hoeveel per maand.</li>
          <li>Het beantwoorden en beheren van reviews.</li>
          <li>Een koppeling met advertenties. Die gaat op aanvraag, zie <a href="adverteren.html">adverteren</a>; het budget betaalt u rechtstreeks aan Google of Meta.</li>
          <li>Een kwartaalgesprek naast het maandrapport.</li>
        </ul>
        <h3>Waarom geen uurtarief</h3>
        <p>Een uurtarief zegt weinig zolang niet vaststaat hoeveel uur een maand kost. Bij Complete AI ligt er na de intake één vaste prijs op papier, zonder nacalculatie. U weet vooraf wat er per maand staat.</p>
        <h3>Wat u bij elk voorstel naast elkaar legt</h3>
        <div class="tabelwrap"><table>
          <thead><tr><th>Vraag</th><th>Bij Complete AI</th></tr></thead>
          <tbody>
            <tr><td><strong>Hoeveel berichten, op welke kanalen?</strong></td><td>Volgt uit het vertrekpunt en staat in het voorstel.</td></tr>
            <tr><td><strong>Wie levert het beeld?</strong></td><td>U, via één WhatsApp-nummer. Uw eigen beeld krijgt voorrang boven gegenereerd beeld.</td></tr>
            <tr><td><strong>Ziet u de maand vooraf?</strong></td><td>Ja, in één link, met de ruimte om aan te geven wat er anders moet.</td></tr>
            <tr><td><strong>Van wie zijn de accounts?</strong></td><td>Van u. Toegang loopt via de officiële beheeromgevingen.</td></tr>
            <tr><td><strong>Wat staat er in het rapport?</strong></td><td>Zichtbaarheid en acties, elke maand.</td></tr>
            <tr><td><strong>Hoe lang zit u vast?</strong></td><td>Maandelijks opzegbaar. De profielen, de merkkit en alles wat is geplaatst blijven van u.</td></tr>
            <tr><td><strong>Zijn advertenties inbegrepen?</strong></td><td>Nee, die gaan op aanvraag.</td></tr>
          </tbody>
        </table></div>""", "kosten"),

   sectie("Werkwijze", "Van intake tot een ritme dat vanzelf doorloopt.",
          "Voorbereiding is niet nodig. Wat wij vragen is een half uur, en daarna één gesprek van ongeveer een uur.",
          routeblok([
            ("Intake", "Een half uur waarin we kijken wat er nu staat: het bedrijfsprofiel, de bestaande accounts, en wat de concurrent in de buurt doet. Kosteloos en vrijblijvend. U hoort ook wanneer de winst ergens anders ligt."),
            ("Inrichting", "Één gesprek van ongeveer een uur over uw diensten, uw klanten, uw manier van praten en wat er absoluut niet gezegd mag worden. Daarna zetten wij de profielen op orde en maken wij de merkkit."),
            ("Eerste maand", "U ontvangt de kalender van de eerste maand ter goedkeuring, plus het WhatsApp-nummer waar u foto’s naartoe stuurt. Vanaf dat moment loopt het."),
            ("Doorlopend", "Elke maand een kalender vooraf en een rapport achteraf, in gewone taal. Maandelijks opzegbaar."),
          ]), "werkwijze"),

   proza("Social media manager", "Wat doet een social media manager, en hoe noemt u zo iemand?", """        <p>Iemand die de social media van een bedrijf beheert, heet een social media manager, soms ook contentspecialist. Een verwante functie is social media specialist. Het onderdeel dat gaat over de omgang met volgers heet community management.</p>
        <h3>Wat zo iemand doet</h3>
        <p>De invulling verschilt per bedrijf. De taken die terugkomen:</p>
        <ul>
          <li>Samen met de opdrachtgever een strategie bepalen.</li>
          <li>De accounts beheren en trends vertalen naar ideeën voor berichten.</li>
          <li>Berichten inplannen en plaatsen.</li>
          <li>Vragen en reacties beantwoorden.</li>
          <li>De resultaten monitoren en erover rapporteren.</li>
        </ul>
        <h3>Wat dat bij uitbesteden betekent</h3>
        <p>Bij uitbesteden neemt een bureau of freelancer die taken over. Bij Complete AI is er één aanspreekpunt, Glenn van Wijngaarden. De opzet, de teksten en het opmaken van beeld gebeuren geautomatiseerd. De keuzes over wat er wordt verteld komen uit het inrichtingsgesprek en uit wat u aanlevert.</p>
        <h3>Loon en tarief</h3>
        <p>In loondienst hangt wat een social media manager verdient af van ervaring en opleiding. Salarisoverzichten staan op vacaturesites; wij noemen hier geen bedragen. Bij uitbesteden speelt geen salaris en geen uurtarief mee. U betaalt voor een afgesproken pakket, met één vaste prijs zonder nacalculatie.</p>""", "social-media-manager"),

   bronnen([
     ("Tips to improve your local ranking on Google", "https://support.google.com/business/answer/7091", "Google Business Profile Help. Relevantie, afstand en bekendheid; volledige en juiste gegevens, reacties op reviews, foto’s en video’s; een betere plek is niet aan te vragen of te betalen."),
     ("Create & manage posts on your Business Profile", "https://support.google.com/business/answer/7342169", "Google Business Profile Help. Berichten tonen nieuws, aanbiedingen en evenementen in Search en Maps; berichten ouder dan zes maanden worden gearchiveerd tenzij een periode is ingesteld."),
     ("Manage customer reviews", "https://support.google.com/business/answer/3474050", "Google Business Profile Help. Reageren op reviews laat zien dat u feedback waardeert."),
     ("Understand your Business Profile performance & insights", "https://support.google.com/business/answer/9918094", "Google Business Profile Help. De prestatiecijfers: weergaven, zoekopdrachten, telefoontjes, routeverzoeken, websiteklikken; alleen voor geverifieerde profielen."),
     ("Functieomschrijving voor Social Media Manager", "https://nl.indeed.com/personeel/functiebeschrijving/social-media-manager", "Indeed. Naam, alternatieve benaming contentspecialist en de taken van een social media manager."),
     ("Social media manager: salaris en functieomschrijving", "https://career.jobbird.com/nl/beroepengids/online-marketing/social-media-manager", "Jobbird. Community management, de verwante functie social media specialist en de factoren die het salaris bepalen (ervaring, opleiding)."),
   ]),
 ]),
},

# ───────────────────────────── VINDBAARHEID — SEO ─────────────────────────────
{
 "bestand": "vindbaarheid-seo.html",
 "dienst": "Vindbaarheid — SEO",
 "titel": "SEO voor mkb: hoger in Google komen | Complete AI",
 "beschrijving": "SEO voor mkb uitgelegd: hoe Google een pagina kiest, wat u zelf kunt doen en waar het werk van een specialist begint. Zonder beloftes over posities.",
 "omschrijving": "Zoekmachine-optimalisatie voor mkb-bedrijven: hoe Google een pagina kiest, de vier lagen van SEO, een nieuwe website in Google, het Google-bedrijfsprofiel en een vast maandrapport.",
 "ogen": "Vindbaarheid — SEO",
 "h1": 'SEO voor mkb: <span class="glans">beter gevonden worden in Google</span>, stap voor stap.',
 "lead": "SEO voor mkb is het werk waardoor Google uw pagina’s kan vinden, begrijpen en tonen bij de zoekopdrachten van uw klanten. U komt hoger in Google met een technisch gezonde site, inhoud die de vraag van de klant beantwoordt en tekenen dat uw bedrijf te vertrouwen is. Complete AI voert dit werk uit en meldt elke maand wat het opleverde.",
 "levertijd": "Doorlopend werk, met een vast maandrapport",
 "gepubliceerd": "2026-09-24",
 "gewijzigd": "2026-09-24",
 "uitkomsten": [
     ("Elke maand", "een vast rapport: wat er is gedaan en wat het opleverde"),
     ("Doorlopend", "SEO bouwt voort op eerder werk, het is geen eenmalige klus"),
     ("1", "aanspreekpunt voor de site, de inhoud en de meting"),
 ],
 "slot_kop": "Waar staat uw bedrijf nu in Google?",
 "slot_tekst": "In de intake kijken wij samen met u in Search Console en in de zoekresultaten zelf: welke pagina’s Google kent, op welke zoekopdrachten u verschijnt en waar de eerste winst zit. U ontvangt een onderbouwd advies, ook wanneer de conclusie is dat de basis op orde is.",
 "vragen": [
   ("Hoe komt u hoger in de Google-ranking?",
    "Door vier dingen op orde te brengen. Google moet uw pagina’s kunnen vinden en opnemen, de inhoud moet aansluiten op wat mensen intypen, andere sites en beoordelingen moeten laten zien dat uw bedrijf te vertrouwen is, en de site moet snel zijn op een telefoon. Zonder de eerste twee helpt de rest niet. Zie <a href=\"#vier-lagen\">de vier lagen</a>."),
   ("Hoe kunt u gevonden worden op Google?",
    "Begin met controleren of Google uw pagina’s al kent: zoek op site: gevolgd door uw domeinnaam. Staan uw pagina’s er niet, dan richt u Search Console in en dient u een sitemap in. Daarna volgen een aparte pagina per dienst, een unieke titel per pagina en een ingericht Google-bedrijfsprofiel. Lees ook <a href=\"#nieuwe-website\">waarom een nieuwe site tijd nodig heeft</a>."),
   ("Hoe komt u bij Google bovenaan te staan?",
    "Bovenaan komen kan niemand garanderen. Google schrijft zelf dat het geen betaling aanneemt om een site hoger te tonen en dat een bedrijf dat een eerste plaats garandeert, mijdt u beter. Wat u kunt doen, is uw pagina’s de beste beantwoording van een vraag maken. Betaalde advertenties staan wel bovenaan, maar zijn een andere route: zie <a href=\"adverteren.html\">adverteren</a>."),
   ("Waarom staat mijn nieuwe website nog niet in Google?",
    "Omdat Google een nieuwe site eerst moet vinden, bezoeken en opnemen. Dat kan volgens Google enkele dagen tot enkele weken duren, en opname is niet gegarandeerd. Controleer in Search Console of de pagina’s zijn gevonden en gecrawld, dien de sitemap in en zorg dat elke pagina een link heeft. Meer leest u bij <a href=\"#nieuwe-website\">nieuwe website in Google</a>."),
   ("Kunt u SEO zelf doen?",
    "De basis wel: een snelle site, een aparte pagina per dienst, duidelijke titels en een ingericht Google-bedrijfsprofiel. Google schrijft zelf dat een klein lokaal bedrijf waarschijnlijk een groot deel van het werk zelf kan doen. Het doorlopende deel kost tijd: uitzoeken wat klanten intypen, daar pagina’s voor schrijven, meten en bijsturen. Dat nemen wij over. Zie <a href=\"#zelf-of-specialist\">zelf doen of uitbesteden</a>."),
   ("Kunt u gratis hoger in Google komen?",
    "Ja, een plek in de gewone zoekresultaten kost niets. Google schrijft dat het nooit geld aanneemt om sites op te nemen of hoger te tonen. Wat het wel kost, is tijd: voor een snelle site, pagina’s die een vraag beantwoorden en het meten van het resultaat. Zie <a href=\"#zelf-of-specialist\">zelf doen of uitbesteden</a>."),
   ("Hoeveel kost SEO per maand?",
    "Het maandbedrag hangt af van de grootte van de markt waarin u gevonden wilt worden, het aantal pagina’s dat daarvoor nodig is en wat er technisch al staat. Na de intake ligt er één vast maandbedrag op papier, zonder nacalculatie. Een bedrag vooraf zou voor het ene bedrijf te hoog en voor het andere te laag zijn."),
   ("Hoe lang duurt het voordat SEO resultaat geeft?",
    "Google noemt geen vaste termijn: sommige wijzigingen werken binnen enkele uren door, andere pas na enkele maanden, en Google adviseert enkele weken te wachten voor u een wijziging beoordeelt. Een nieuwe site heeft meer tijd nodig dan een bestaande. Wij noemen daarom geen datum en geen positie. Het maandrapport laat zien of het de goede kant op gaat."),
   ("Kan ChatGPT SEO-teksten schrijven?",
    "Ja, maar zo’n tekst is alleen goed als hij iets toevoegt. Google schrijft dat generatieve AI nuttig is om een onderwerp uit te zoeken en structuur aan te brengen in eigen inhoud, maar dat veel pagina’s zonder toegevoegde waarde onder de spamregels vallen. Waarde komt uit uw eigen kennis, echte details en gecontroleerde feiten."),
   ("Wat is de beste gratis SEO-tool?",
    "Search Console, de gratis dienst van Google zelf. Die toont of Google uw pagina’s kan vinden en opnemen, op welke zoekopdrachten u verschijnt en hoe vaak er wordt geklikt. Voor snelheid en gebruikservaring is Lighthouse in de browser Chrome bruikbaar. Google beoordeelt en keurt geen SEO-tools van derden goed: leg hun adviezen naast de officiële richtlijnen."),
   ("Wat is het verschil tussen SEO en SEA?",
    "SEO gaat over de gewone, onbetaalde zoekresultaten: u verschijnt omdat Google uw pagina relevant vindt. SEA gaat over betaalde advertenties boven en naast die resultaten: u betaalt per klik. SEO bouwt langzaam op en blijft staan, advertenties werken direct en stoppen wanneer het budget stopt. Meer over de tweede route leest u bij <a href=\"adverteren.html\">adverteren</a>."),
   ("Hoort het Google-bedrijfsprofiel bij SEO?",
    "Ja, voor bedrijven die in Google Maps en in het vak naast de zoekresultaten gevonden willen worden. Het profiel toont openingstijden, diensten, foto’s en beoordelingen. Wij richten het volledig in. Het wekelijkse onderhoud, met berichten en reacties op beoordelingen, valt onder <a href=\"social-media.html\">social media</a>. Zie ook <a href=\"#lokaal-landelijk\">lokaal of landelijk gevonden worden</a>."),
   ("Kan mijn bedrijf via SEO ook genoemd worden in AI-antwoorden?",
    "Google zegt zelf dat het AI-overzicht geen aparte techniek vraagt: een pagina moet zijn opgenomen in Google en met een tekstfragment getoond mogen worden. Het werk aan SEO is dus ook het werk voor AI-antwoorden. Een garantie op een vermelding bestaat niet. Wat helpt is een pagina die de vraag direct beantwoordt, met een bron die te vertrouwen is."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   inhoudsopgave([
       ("hoe-google-kiest", "Hoe Google een pagina kiest"),
       ("vier-lagen", "De vier lagen van SEO"),
       ("herkenbaar", "Waar het bij bestaande sites misloopt"),
       ("nieuwe-website", "Een nieuwe website in Google"),
       ("lokaal-landelijk", "Lokaal of landelijk gevonden worden"),
       ("zelf-of-specialist", "Zelf doen of een specialist"),
       ("ai-overzicht", "SEO en het AI-overzicht"),
       ("eigen-praktijk", "Uit eigen praktijk"),
       ("fouten", "Veelgemaakte fouten"),
       ("rapportage", "Meten en rapporteren"),
       ("wat-u-krijgt", "Wat u krijgt"),
       ("werkwijze", "Werkwijze"),
       ("bronnen", "Bronnen"),
   ]),

   proza("Hoe Google kiest", "Hoe kiest Google welke pagina bovenaan komt?", """
        <h3>Drie stappen: vinden, opnemen, tonen</h3>
        <p>Google beschrijft zelf dat Zoeken in drie stappen werkt. Niet elke pagina komt door alle drie.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Stap</th><th>Wat Google doet, en wat dat voor uw site betekent</th></tr></thead>
          <tbody>
            <tr><td><strong>Vinden</strong> (crawlen)</td><td>Programma’s van Google, crawlers genoemd, zoeken pagina’s. Ze vinden ze via links op pagina’s die Google al kent en via een sitemap.<br><em>Voor uw site:</em> een pagina moet bereikbaar zijn en ergens naar verwijzen. Wat u blokkeert, wordt niet bezocht.</td></tr>
            <tr><td><strong>Opnemen</strong> (indexeren)</td><td>Google leest de tekst, de titel, de afbeeldingen en de video’s van de pagina en legt ze vast in zijn index. Het bepaalt ook of de pagina een kopie is van een andere.<br><em>Voor uw site:</em> een pagina die niet is opgenomen, kan op geen enkele zoekopdracht verschijnen.</td></tr>
            <tr><td><strong>Tonen</strong> (rangschikken)</td><td>Bij een zoekopdracht kiest Google uit de opgenomen pagina’s wat het beste past bij wat de zoeker bedoelt.<br><em>Voor uw site:</em> hier tellen de inhoud, de betrouwbaarheid van de site en de gebruikservaring.</td></tr>
          </tbody>
        </table></div>
        <p>Google is daarbij helder over twee dingen. Ook een pagina die alle richtlijnen volgt, wordt niet gegarandeerd bezocht, opgenomen of getoond. En Google neemt geen betaling aan om een site intensiever te bezoeken of hoger te tonen. Volgens <a href="https://developers.google.com/search/docs/fundamentals/how-search-works" rel="noopener" target="_blank">de uitleg van Google over hoe Zoeken werkt</a> heeft iedereen die iets anders beweert het mis.</p>

        <h3>Waar Google naar kijkt bij het kiezen</h3>
        <p>De rangschikking is bedoeld om behulpzame en betrouwbare informatie te belonen die voor mensen is geschreven, en niet inhoud die is gemaakt om de rangschikking te beïnvloeden. Google stelt daarvoor zelf <a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content" rel="noopener" target="_blank">toetsvragen voor behulpzame inhoud</a>, zoals:</p>
        <ul>
          <li>Bevat de pagina originele informatie, eigen onderzoek of eigen analyse?</li>
          <li>Geeft de pagina een volledige beschrijving van het onderwerp?</li>
          <li>Voegt de pagina iets toe in vergelijking met de andere pagina’s in de zoekresultaten?</li>
          <li>Is duidelijk wie de pagina heeft geschreven, en waarom?</li>
        </ul>
        <p>Voor een mkb-bedrijf komt dit neer op één vraag: weet iemand die uw pagina leest genoeg om zijn doel te bereiken? Google gebruikt die vraag zelf ook. De rest van deze pagina is daarop gebouwd.</p>
        <div class="noot"><p><strong>Over E-E-A-T.</strong> Google noemt ervaring, expertise, autoriteit en betrouwbaarheid (E-E-A-T) zelf geen rankingfactor. Het zijn de eigenschappen waaraan de systemen goede inhoud proberen te herkennen, en betrouwbaarheid weegt het zwaarst. Daarom noemt elke pagina van deze site zijn auteur en zijn datum, en staan de bronnen onderaan.</p></div>

        <h3>Wat SEO daarbinnen is</h3>
        <p>SEO, zoekmachine-optimalisatie, is het werk waarmee u zoekmachines helpt uw inhoud te begrijpen en waarmee u bezoekers helpt te beslissen of ze doorklikken. Het kost niets om in de gewone resultaten te verschijnen, schrijft Google, en advertenties op Google veranderen niets aan uw plek daarin. Wat wel tijd kost, is het werk eromheen. Dat werk is in te delen in vier lagen.</p>
""", "hoe-google-kiest", "Google is een geautomatiseerde zoekmachine. Er is geen medewerker die uw site beoordeelt en geen loket waar u een positie aanvraagt. Wat er wel is, staat in de eigen documentatie van Google, en die vormt de basis van deze pagina."),

   proza("De vier lagen", "De vier lagen van SEO, met voorbeelden.", """
        <div class="tabelwrap"><table>
          <thead><tr><th>Laag</th><th>De vraag die zij beantwoordt, en een voorbeeld van een probleem</th></tr></thead>
          <tbody>
            <tr><td><strong>Technisch</strong></td><td>Kan Google de pagina’s bereiken en lezen?<br><em>Probleem:</em> een instructie op de pagina die opname verbiedt.</td></tr>
            <tr><td><strong>Inhoud</strong></td><td>Beantwoordt de pagina de vraag die iemand intypt?<br><em>Probleem:</em> één pagina met de titel ‘Onze diensten’ voor zes verschillende vragen.</td></tr>
            <tr><td><strong>Autoriteit</strong></td><td>Is er reden om uw bedrijf te vertrouwen?<br><em>Probleem:</em> geen enkele andere site of beoordeling die het bedrijf noemt.</td></tr>
            <tr><td><strong>Gebruikservaring</strong></td><td>Is de pagina snel en prettig, vooral op een telefoon?<br><em>Probleem:</em> een pagina die verspringt terwijl u leest.</td></tr>
          </tbody>
        </table></div>

        <h3>Laag 1: technisch</h3>
        <p>Technisch gaat over de vraag of Google uw pagina’s kan bereiken, lezen en met rust laat. Vijf voorbeelden:</p>
        <ul>
          <li><strong>Een pagina is geblokkeerd.</strong> Sluit het bestand robots.txt een pagina uit, dan bezoekt Google hem niet. Staat er een noindex-instructie op, dan neemt Google hem niet op. Voor pagina’s die u niet in Google wilt, is dat de bedoeling. Op een pagina die er wel in moet staan, is het een fout die al het andere werk tenietdoet.</li>
          <li><strong>Een pagina heeft geen enkele link.</strong> Google vindt pagina’s vooral via links vanaf pagina’s die het al kent. Een pagina waar niets naar verwijst, wordt later of niet gevonden. Links in de lopende tekst en een sitemap lossen dat op.</li>
          <li><strong>Dezelfde inhoud staat op twee adressen.</strong> Google kiest dan zelf één adres om te tonen, de canonieke pagina. Gebruik één adres per pagina, stuur de andere door of wijs de voorkeur aan met een canonical.</li>
          <li><strong>De belangrijkste tekst staat niet als tekst op de pagina.</strong> Google adviseert belangrijke inhoud als tekst beschikbaar te maken, en dus niet alleen in een afbeelding of video.</li>
          <li><strong>Structuurdata die afwijkt van de zichtbare tekst.</strong> Structuurdata is code waarmee u Google extra uitleg geeft, bijvoorbeeld over de vragen op een pagina. Google vraagt dat die overeenkomt met wat de bezoeker leest.</li>
        </ul>
        <p>Een sitemap is niet verplicht, maar Google noemt hem nuttig bij een pas gelanceerde site. Bij een site die op deze punten goed is gebouwd, is de technische laag een controle in plaats van een project.</p>

        <h3>Laag 2: inhoud</h3>
        <p>Inhoud gaat over de vraag of een pagina antwoord geeft op wat iemand intypt. Vier keuzes bepalen dat.</p>
        <ul>
          <li><strong>Eén vraag of één dienst per pagina.</strong> Een pagina met de titel ‘Onze diensten’ beantwoordt geen zoekopdracht. Een voorbeeld: een installatiebedrijf dat cv-ketels, vloerverwarming en badkamers op één pagina zet, doet er beter aan elke dienst een eigen pagina te geven, met de vragen die klanten daarover stellen.</li>
          <li><strong>De woorden van de klant.</strong> Google merkt op dat deskundigen andere woorden gebruiken dan beginners, en dat het loont daarmee rekening te houden. Een klant schrijft ‘kraan lekt’ waar de vakman ‘reparatie van een mengkraan’ schrijft. Schrijf zoals de klant het zegt en zet de vaktaal erbij als uitleg. U hoeft niet elke variant op te sommen, want de taalsystemen van Google herkennen ook varianten.</li>
          <li><strong>Het antwoord bovenaan.</strong> De eerste zinnen van een pagina beantwoorden de vraag; daarna volgt de uitleg. Dat is prettig voor de lezer, en de lezer is degene voor wie Google de pagina kiest.</li>
          <li><strong>Een unieke titel en beschrijving per pagina.</strong> De titel is de kop van uw zoekresultaat. Google adviseert titels die uniek, beknopt en beschrijvend zijn en de inhoud juist weergeven. <a href="https://developers.google.com/search/docs/appearance/title-link" rel="noopener" target="_blank">Dezelfde titel op elke pagina</a> maakt voor de zoeker onzichtbaar welke pagina welke vraag beantwoordt.</li>
        </ul>
        <p>Er is geen ideale lengte. Google schrijft dat er geen woordenaantal bestaat waarmee een pagina hoger komt. Een pagina is lang genoeg wanneer de vraag volledig is beantwoord.</p>

        <h3>Laag 3: autoriteit</h3>
        <p>Autoriteit gaat over de vraag of er reden is om uw bedrijf te vertrouwen. Google kijkt daarvoor ook naar signalen buiten uw eigen site.</p>
        <ul>
          <li><strong>Links van andere sites.</strong> Google vindt het grootste deel van de nieuwe pagina’s via links, en verwijzingen naar uw site ontstaan volgens Google vanzelf naarmate de tijd verstrijkt. Een vermelding op de site van een brancheorganisatie of een leverancier waarmee u werkt, is zo’n verwijzing.</li>
          <li><strong>Beoordelingen.</strong> Bij lokale zoekopdrachten telt volgens Google mee hoeveel websites naar uw bedrijf verwijzen en hoeveel beoordelingen u heeft. Reageren op beoordelingen, ook op kritische, hoort daarbij.</li>
          <li><strong>Zichtbaar wie erachter zit.</strong> Google vraagt of een pagina een auteur noemt en of er achtergrond over die auteur te vinden is. Een naam, een functie en een datum bij elke pagina beantwoorden dat.</li>
          <li><strong>Bronnen.</strong> Google vraagt of een pagina duidelijk zijn bronnen noemt en aanwijzingen van deskundigheid geeft.</li>
        </ul>
        <p>Links kopen of ruilen werkt niet. Google rekent het kopen van links voor de rangschikking, buitensporig links ruilen en het aanmaken van links met geautomatiseerde programma’s tot <a href="https://developers.google.com/search/docs/essentials/spam-policies" rel="noopener" target="_blank">linkspam</a>. De gevolgen kunnen een lagere positie of verwijdering uit de index zijn. Wie u links aanbiedt, brengt uw site in gevaar.</p>

        <h3>Laag 4: gebruikservaring</h3>
        <p>Gebruikservaring gaat over de vraag of de pagina snel en prettig werkt, vooral op een telefoon. Google beoordeelt dat niet met één cijfer maar met een reeks aspecten. Drie daarvan zijn goed na te gaan:</p>
        <ul>
          <li><strong>Mobiel eerst.</strong> Google gebruikt de mobiele versie van een pagina om te indexeren en te rangschikken (<a href="https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing" rel="noopener" target="_blank">mobile-first indexing</a>). De inhoud moet op een telefoon dus volledig zijn.</li>
          <li><strong>Laden, reageren, stabiliteit.</strong> Google meet dit met de <a href="https://developers.google.com/search/docs/appearance/core-web-vitals" rel="noopener" target="_blank">Core Web Vitals</a>: het grootste element van de pagina hoort binnen 2,5 seconde te verschijnen, de reactie op een tik binnen 200 milliseconden, en de pagina verspringt nauwelijks (een score onder 0,1). Het rapport hierover staat in Search Console.</li>
          <li><strong>Beveiligde verbinding en geen storende schermen.</strong> Google vraagt in zijn uitleg over <a href="https://developers.google.com/search/docs/appearance/page-experience" rel="noopener" target="_blank">pagina-ervaring</a> of pagina’s via HTTPS worden aangeboden en of ze geen opdringerige tussenschermen tonen.</li>
        </ul>
        <p>Dit is de laag waar de bouw van de website het verschil maakt. Websites van Complete AI zijn mobiel eerst en als statische pagina’s gebouwd, en deze site laadt in ongeveer 0,7 seconde. Hoe dat werkt, leest u bij <a href="websites.html">websites</a>.</p>
""", "vier-lagen", "De volgorde is bewust. Een pagina die Google niet kan opnemen, wordt niet beter van een goede tekst, en een goede tekst op een trage site verliest bezoekers."),

   sectie("De situatie", "Waar het bij bestaande sites misloopt.",
          "Vier bevindingen die wij bij bestaande sites terugzien. De eerste twee horen bij de technische laag en de inhoud, de derde bij autoriteit, de vierde bij meten.",
          pijnblok([
            ("Google kent een deel van de pagina’s niet", "Pagina’s die niet zijn opgenomen kunnen op geen enkele zoekopdracht verschijnen. Dat is te zien in Search Console, maar daar kijkt niemand naar."),
            ("De pagina’s beantwoorden andere vragen dan klanten stellen", "Een pagina met de titel “Welkom” beantwoordt geen zoekopdracht. Klanten zoeken op een probleem of een vraag, niet op het menu van een bedrijf."),
            ("Anderen staan erboven met minder goede pagina’s", "Verwijzingen van andere sites en beoordelingen tellen mee als teken van betrouwbaarheid. Zonder die signalen kan een goede pagina onder een minder goede staan."),
            ("Niemand weet wat het oplevert", "Er is geen rapport, dus het is onduidelijk welke zoekopdrachten bezoek brengen en welke aanvragen daaruit komen."),
          ]), "herkenbaar"),

   proza("Nieuwe website", "Waarom een nieuwe website nog niet in Google staat.", """
        <h3>Wat er na de livegang gebeurt</h3>
        <p>Google moet een nieuwe site eerst vinden. Volgens de <a href="https://support.google.com/webmasters/answer/7440203" rel="noopener" target="_blank">hulp van Search Console</a> kan het een week duren voordat Google een nieuwe pagina of site begint te bezoeken en op te nemen. In zijn uitleg over <a href="https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl" rel="noopener" target="_blank">hercrawlen</a> noemt Google een bereik van enkele dagen tot enkele weken. Dat gaat over het bezoeken en opnemen van pagina’s, niet over de positie die ze daarna krijgen.</p>
        <ol>
          <li><strong>Google vindt de pagina</strong>, via een link of via een sitemap.</li>
          <li><strong>Google bezoekt de pagina</strong> en leest wat erop staat.</li>
          <li><strong>Google besluit of de pagina wordt opgenomen.</strong> Dat gaat niet vanzelf.</li>
          <li><strong>Een opgenomen pagina kan verschijnen.</strong> Of zij dat doet en waar, hangt af van de concurrentie op die zoekopdracht, van de zoeker en van het moment.</li>
        </ol>
        <p>Ook een opgenomen pagina staat niet in elk zoekresultaat. Google schrijft dat zoekresultaten worden aangepast aan de zoekgeschiedenis, de locatie en andere kenmerken van de zoeker, en dat een pagina die wel verschijnt niet altijd op dezelfde plek staat.</p>

        <h3>De twee meldingen die u in Search Console ziet</h3>
        <p>In het rapport Pagina-indexering van Search Console staan bij een nieuwe site twee statussen die om uitleg vragen. Zo leest u ze.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Status</th><th>Wat het volgens Google betekent, en wat u eraan doet</th></tr></thead>
          <tbody>
            <tr><td><strong>Gevonden, momenteel niet geïndexeerd</strong></td><td>Google kent de pagina, maar heeft hem nog niet bezocht.<br><em>Wat u doet:</em> controleer of de pagina in de sitemap staat en vanuit andere pagina’s is gelinkt. Verder is wachten de handeling.</td></tr>
            <tr><td><strong>Gecrawld, momenteel niet geïndexeerd</strong></td><td>Google heeft de pagina bezocht en niet opgenomen. Het kan later alsnog gebeuren, maar dat is niet zeker. Opnieuw indienen is niet nodig.<br><em>Wat u doet:</em> beoordeel of de pagina iets toevoegt aan wat er al staat. Maak hem completer, geef hem links vanaf andere pagina’s en geef Google tijd.</td></tr>
            <tr><td><strong>Geïndexeerd</strong></td><td>De pagina is opgenomen en komt in aanmerking om te worden getoond. Een garantie dat hij bij elke zoekopdracht verschijnt, is dat niet.<br><em>Wat u doet:</em> volg in het prestatierapport op welke zoekopdrachten hij verschijnt.</td></tr>
          </tbody>
        </table></div>
        <p>Niet elke pagina hoeft te worden opgenomen. Google schrijft dat pagina’s met een noindex-instructie, duplicaten en verwijderde pagina’s terecht buiten de index blijven. Het gaat erom dat de belangrijkste pagina’s erin staan.</p>

        <h3>Wat u eraan doet</h3>
        <ol>
          <li>Zoek in Google op <em>site:</em> gevolgd door uw domeinnaam. Zo ziet u welke pagina’s Google kent.</li>
          <li>Richt Search Console in en dien uw sitemap in. Google noemt een sitemap nuttig bij een pas gelanceerde site.</li>
          <li>Vraag met de URL-inspectietool indexering aan voor de belangrijkste pagina’s. Dezelfde pagina meerdere keren aanvragen maakt het niet sneller.</li>
          <li>Zorg dat elke pagina een link heeft vanaf andere pagina’s van uw site.</li>
          <li>Zorg dat elke pagina iets toevoegt aan wat er al bestaat. Google geeft aan dat zijn systemen de snelle opname van nuttige inhoud van hoge kwaliteit voorrang geven.</li>
          <li>Wacht enkele weken voor u conclusies trekt over een wijziging. Volgens Google werken sommige wijzigingen binnen enkele uren door en andere pas na enkele maanden.</li>
        </ol>

        <h3>Wat u beter niet doet</h3>
        <ul>
          <li>Links kopen om sneller in de index te komen. Dat valt onder linkspam.</li>
          <li>Pagina’s in bulk toevoegen of oude verwijderen om de site ‘vers’ te laten lijken. Google schrijft dat dat de rangschikking niet verbetert.</li>
          <li>De datum van een pagina aanpassen terwijl de inhoud gelijk blijft. Google noemt dat een waarschuwingssignaal.</li>
        </ul>
""", "nieuwe-website", "Een site die online staat, is nog geen site die Google heeft opgenomen. Dat verschil verklaart de eerste weken."),

   proza("Lokaal en landelijk", "Lokaal of landelijk gevonden worden: wat is het verschil?", """
        <h3>Wat Google onder lokaal verstaat</h3>
        <p>Zoekt iemand naar een bedrijf of een plek in de buurt, dan toont Google lokale resultaten in Google Maps en in Zoeken. Volgens de <a href="https://support.google.com/business/answer/7091" rel="noopener" target="_blank">hulp van het Google-bedrijfsprofiel</a> zijn die resultaten voornamelijk gebaseerd op drie dingen. Een betere lokale positie aanvragen of kopen kan niet.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Factor</th><th>Wat Google bedoelt, en wat u eraan kunt doen</th></tr></thead>
          <tbody>
            <tr><td><strong>Relevantie</strong></td><td>Hoe goed het bedrijfsprofiel overeenkomt met wat iemand zoekt.<br><em>Wat u doet:</em> een volledig profiel met de juiste categorie, uw diensten en uw openingstijden.</td></tr>
            <tr><td><strong>Afstand</strong></td><td>Hoe ver het bedrijf van de zoeker verwijderd is.<br><em>Wat u doet:</em> niets, want de plek van de zoeker bepaalt dit.</td></tr>
            <tr><td><strong>Prominentie</strong></td><td>Hoe bekend een bedrijf is. Hier tellen onder meer het aantal websites dat naar het bedrijf verwijst en het aantal beoordelingen mee.<br><em>Wat u doet:</em> beoordelingen vragen en beantwoorden, en verwijzingen van sites uit uw vak.</td></tr>
          </tbody>
        </table></div>

        <h3>Wat er in het bedrijfsprofiel hoort</h3>
        <p>Google noemt in dezelfde hulp welke onderdelen meetellen. Bedrijven met een complete en correcte profielinformatie hebben meer kans om bij lokale zoekopdrachten te worden getoond.</p>
        <ul>
          <li>Het profiel laten verifiëren, zodat Google weet dat u het bedrijf mag vertegenwoordigen.</li>
          <li>Het adres, wanneer klanten uw locatie kunnen bezoeken.</li>
          <li>De openingstijden, ook de afwijkende tijden.</li>
          <li>Het soort bedrijf, via de categorie.</li>
          <li>Foto’s en video’s van wat u levert.</li>
          <li>Reacties op beoordelingen.</li>
        </ul>
        <p>Zet er alleen in wat bij een dienst hoort die u werkelijk levert. Een dienst die u niet uitvoert, trekt zoekers die u niet kunt helpen, en het profiel is bedoeld om de best passende overeenkomst te tonen. Het wekelijkse onderhoud van het profiel, met berichten, foto’s en reacties op beoordelingen, valt onder <a href="social-media.html">social media</a>.</p>

        <h3>Wat er anders is bij landelijk gevonden worden</h3>
        <p>Bij een landelijke zoekopdracht speelt afstand geen rol. Dan telt wat uw pagina de zoeker biedt: inhoud, betrouwbaarheid en gebruikservaring. U concurreert bovendien met elk bedrijf dat dezelfde vraag beantwoordt, niet alleen met de bedrijven in uw omgeving. Dat pleit ervoor te kiezen: één vraag volledig beantwoorden in plaats van tien onderwerpen aanstippen.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Aspect</th><th>Lokaal en landelijk vergeleken</th></tr></thead>
          <tbody>
            <tr><td><strong>Waar Google het toont</strong></td><td><strong>Lokaal:</strong> Google Maps en Zoeken, waar lokale resultaten verschijnen voor wie in de buurt zoekt.<br><strong>Landelijk:</strong> de gewone zoekresultaten.</td></tr>
            <tr><td><strong>Wat zwaar weegt</strong></td><td><strong>Lokaal:</strong> relevantie, afstand en prominentie van het bedrijfsprofiel.<br><strong>Landelijk:</strong> de inhoud van de pagina, de betrouwbaarheid van de site en de gebruikservaring.</td></tr>
            <tr><td><strong>Wat u regelt</strong></td><td><strong>Lokaal:</strong> bedrijfsprofiel, beoordelingen en een pagina per dienst.<br><strong>Landelijk:</strong> pagina’s die één vraag volledig beantwoorden, met bronnen en een herkenbare auteur.</td></tr>
          </tbody>
        </table></div>

        <h3>Plaatsnamen opsommen helpt niet</h3>
        <p>Een blok tekst dat steden en regio’s opsomt waarop een pagina wil scoren, valt volgens de <a href="https://developers.google.com/search/docs/essentials/spam-policies" rel="noopener" target="_blank">spamregels van Google</a> onder keyword stuffing. Schrijf een aparte pagina voor een werkgebied alleen wanneer daar iets over te zeggen valt wat elders niet staat. Ook Complete AI noemt op zijn site geen lijst plaatsen, maar zijn werkgebied: Nederland en België.</p>
""", "lokaal-landelijk", "Voor een bedrijf met een werkgebied lopen twee routes naast elkaar: het Google-bedrijfsprofiel en de dienstpagina op uw site. Ze hebben elk hun eigen regels."),

   proza("Zelf of specialist", "SEO zelf doen of uitbesteden: waar begint het werk van een specialist?", """
        <h3>Wat u zelf kunt doen</h3>
        <p>Google schrijft in zijn uitleg <a href="https://developers.google.com/search/docs/fundamentals/do-i-need-seo" rel="noopener" target="_blank">Heeft u een SEO nodig?</a> dat een klein lokaal bedrijf waarschijnlijk een groot deel van het werk zelf kan doen. De <a href="https://developers.google.com/search/docs/fundamentals/seo-starter-guide" rel="noopener" target="_blank">SEO-starterhandleiding van Google</a> is daarvoor het uitgangspunt. Zelf te doen zijn:</p>
        <ul>
          <li>Search Console inrichten. Het is een gratis dienst van Google.</li>
          <li>Controleren welke pagina’s Google kent, met <em>site:</em> gevolgd door uw domeinnaam.</li>
          <li>Een aparte pagina per dienst maken, met een unieke titel.</li>
          <li>Het Google-bedrijfsprofiel invullen en beoordelingen beantwoorden.</li>
          <li>De snelheid op een telefoon nagaan, bijvoorbeeld met Lighthouse in Chrome.</li>
        </ul>

        <h3>Waar het werk van een specialist begint</h3>
        <p>Het werk dat tijd kost is het doorlopende deel. Daar begint de specialist:</p>
        <ul>
          <li><strong>Bepalen welke vraag elke pagina beantwoordt.</strong> Google noemt zoekwoordonderzoek zelf als dienst die SEO-specialisten leveren.</li>
          <li><strong>Uitzoeken waarom een pagina niet wordt opgenomen.</strong> De melding in Search Console is het begin. De oorzaak vraagt onderzoek.</li>
          <li><strong>Inhoud schrijven die iets toevoegt.</strong> Dat vraagt kennis van uw vak, en die haalt een specialist uit het gesprek met u.</li>
          <li><strong>Maandelijks meten en bijsturen.</strong> Een wijziging beoordelen kost tijd, en een positie zegt pas iets naast klikken en aanvragen.</li>
          <li><strong>Vanaf het begin meedenken.</strong> Google noemt een verbouwing of de lancering van een nieuwe site een goed moment om iemand in te schakelen, hoe eerder hoe beter. Dan wordt de site vanaf de bouw zoekmachinevriendelijk.</li>
        </ul>
        <p>Bij Complete AI valt dit werk onder één aanspreekpunt: de technische controle, het aanpassen van bestaande pagina’s, nieuwe inhoud op de vragen van klanten, het Google-bedrijfsprofiel en het vaste maandrapport. Wilt u een nieuwe site en SEO tegelijk, dan lopen ze in één traject; zie <a href="websites.html">websites laten maken</a>.</p>

        <h3>Waar u op let bij het kiezen van iemand</h3>
        <p>Google geeft in dezelfde uitleg een reeks toetsen. Wij leggen ze naast onze werkwijze, zodat u kunt nagaan of we ze halen.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>De toets van Google</th><th>Wat u daarvoor bij Complete AI ziet</th></tr></thead>
          <tbody>
            <tr><td>Wat verwacht de SEO te bereiken, in welk tijdsbestek, en hoe wordt succes gemeten?</td><td>Het maandrapport met cijfers uit Search Console. Positie en termijn worden niet toegezegd.</td></tr>
            <tr><td>Wordt gegarandeerd dat u eerste wordt? Dan liever iemand anders.</td><td>Er is geen garantie op een positie, omdat Google die niet geeft.</td></tr>
            <tr><td>Wordt uitgelegd wat er aan de site verandert en waarom?</td><td>In het voorstel en in het maandrapport staat wat er is gedaan en wat de volgende stap is.</td></tr>
            <tr><td>Verwijst de SEO naar de officiële documentatie van Google?</td><td>De bronnen onderaan deze pagina zijn de documentatie van Google zelf.</td></tr>
          </tbody>
        </table></div>
""", "zelf-of-specialist", "Het antwoord verschilt per bedrijf, en Google zelf geeft een genuanceerd antwoord. Hieronder staat wat u zelf kunt doen, waar een specialist iets toevoegt en waaraan u die herkent."),

   proza("SEO en AI", "SEO en het AI-overzicht van Google: is er iets anders nodig?", """
        <p>Nee. In zijn uitleg <a href="https://developers.google.com/search/docs/appearance/ai-features" rel="noopener" target="_blank">AI-functies en uw website</a> schrijft Google dat de best practices voor SEO ook gelden voor AI-overzichten en AI-modus, en dat er geen aanvullende eisen en geen speciale optimalisaties zijn om daarin te verschijnen. Wat Google wel noemt:</p>
        <ul>
          <li><strong>De technische eis.</strong> Een pagina moet zijn opgenomen in Google en met een tekstfragment mogen worden getoond. Er zijn geen aanvullende technische eisen.</li>
          <li><strong>Geen extra bestanden of markeringen.</strong> U hoeft geen nieuwe bestanden voor machines, geen AI-tekstbestanden en geen speciale schema.org-structuurdata toe te voegen.</li>
          <li><strong>De gewone basis.</strong> Crawlen toestaan in robots.txt, inhoud vindbaar maken met interne links, een goede pagina-ervaring bieden, belangrijke inhoud als tekst beschikbaar maken, en structuurdata laten overeenkomen met de zichtbare tekst.</li>
          <li><strong>Actuele bedrijfsgegevens.</strong> Google noemt ook dat de informatie in het bedrijfsprofiel actueel moet zijn.</li>
        </ul>
        <p>Google voegt eraan toe dat het AI-overzicht alleen verschijnt wanneer de systemen bepalen dat het iets toevoegt aan de gewone zoekresultaten, en dat opname en weergave nooit zijn gegarandeerd. Vermeldingen in AI-functies worden meegeteld in het prestatierapport van Search Console, onder het zoektype Web.</p>
        <div class="noot"><p><strong>Wees kritisch bij aanbieders van AEO of GEO.</strong> Google vraagt bij het inhuren van een SEO of diens advies over AI-ervaringen overeenkomt met de officiële richtlijnen van Google Search. Klopt het advies daar niet mee, dan betaalt u voor iets wat Google niet vraagt.</p></div>
        <p>Voor het werk van Complete AI betekent dit dat er geen aparte dienst voor AI-antwoorden bestaat. Het is hetzelfde werk als SEO: een pagina die de vraag in de eerste zinnen beantwoordt, een bron die te vertrouwen is en een site die Google kan opnemen. Een vermelding in een AI-antwoord is niet toe te zeggen.</p>
""", "ai-overzicht", "Bij sommige zoekopdrachten toont Google bovenaan een samenvatting, het AI-overzicht. De vraag voor een ondernemer is of daarvoor een andere aanpak nodig is."),

   proza("Uit eigen praktijk", "Uit eigen praktijk: zo is deze site opgezet.", """
        <p>Wat op deze pagina staat, past Complete AI op zijn eigen site toe. U kunt het nagaan door de paginabron van deze pagina te bekijken.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Wat</th><th>Hoe het op deze site is opgezet, en bij welke laag het hoort</th></tr></thead>
          <tbody>
            <tr><td><strong>Eén pagina per dienst</strong></td><td>Websites, vindbaarheid, adverteren, automatisering, AI-telefonist en social media hebben elk een eigen pagina, naast een klantcase, twee gidsen en pagina’s per branche. <em>(Inhoud)</em></td></tr>
            <tr><td><strong>Titel en beschrijving</strong></td><td>Elke pagina heeft een eigen titel en een eigen beschrijving, zodat de zoeker het verschil ziet. <em>(Inhoud)</em></td></tr>
            <tr><td><strong>Antwoord vooraan</strong></td><td>De eerste zinnen van elke dienstpagina beantwoorden de vraag. Onderaan staan de vragen die klanten stellen. <em>(Inhoud)</em></td></tr>
            <tr><td><strong>Auteur en datum</strong></td><td>Bovenaan elke dienstpagina, klantcase en gids staat wie de tekst heeft geschreven en wanneer hij is gepubliceerd. <em>(Autoriteit)</em></td></tr>
            <tr><td><strong>Structuurdata</strong></td><td>De vragen in de structuurdata zijn dezelfde als de vragen op de pagina, omdat beide uit hetzelfde bestand komen. <em>(Technisch)</em></td></tr>
            <tr><td><strong>Canonical en sitemap</strong></td><td>Elke pagina meldt zijn eigen adres als voorkeursadres, en het bestand sitemap.xml noemt alle pagina’s. <em>(Technisch)</em></td></tr>
            <tr><td><strong>Snel op een telefoon</strong></td><td>Statische pagina’s, mobiel eerst ontworpen. Deze site laadt in ongeveer 0,7 seconde. <em>(Gebruikservaring)</em></td></tr>
            <tr><td><strong>Geen cookiebanner</strong></td><td>Er staat geen tracking op die gedrag volgt. De cijfers voor SEO komen uit Search Console, dus uit de zoekgegevens van Google zelf. <em>(Gebruikservaring)</em></td></tr>
          </tbody>
        </table></div>
        <p>Bij een nieuwe klantsite hoort een deel van deze inrichting bij de bouw: een correcte structuur, een sitemap, structuurdata en een ingericht Google-bedrijfsprofiel. Een site die bij oplevering op deze punten klopt, hoeft ze niet achteraf te herstellen. Meer over de bouw leest u bij <a href="websites.html">websites</a>.</p>
""", "eigen-praktijk", "Een pagina over SEO die zelf niet aan SEO voldoet, is weinig waard."),

   sectie("Veelgemaakte fouten", "Acht fouten die SEO teniet doen.",
          "Zeven van de acht staan ook in de documentatie van Google. Bij de achtste, niet meten, volgt de reden uit wat Search Console laat zien.",
          krijgtblok([
            ("Zoekwoorden opstapelen", "Dezelfde woorden zo intensief herhalen dat het onnatuurlijk klinkt, valt onder keyword stuffing en is volgens Google in strijd met zijn spamregels. Een tekst is voor mensen geschreven."),
            ("Meta keywords invullen", "Google gebruikt de meta-tag met zoekwoorden niet. Tijd die u daaraan besteedt, is verloren."),
            ("Inhoud van anderen herschrijven", "Google vraagt of uw pagina iets toevoegt aan wat er al staat. Wie alleen herhaalt wat anderen schreven, voegt niets toe."),
            ("Links kopen of ruilen", "Linkspam is een overtreding van de spamregels van Google, met een lagere positie of verwijdering uit de index als mogelijk gevolg."),
            ("Schrijven naar een woordenaantal", "Google heeft geen voorkeur voor een aantal woorden. Een pagina is lang genoeg wanneer de vraag is beantwoord."),
            ("Pagina’s per ongeluk blokkeren", "Een noindex-instructie of een regel in robots.txt die per ongeluk op een pagina staat, houdt hem buiten Google. Controleer dat vóór de livegang."),
            ("Na twee weken alles omgooien", "Google adviseert enkele weken te wachten voor u een wijziging beoordeelt. Wie elke week iets anders probeert, weet niet meer wat werkte."),
            ("Niet meten", "Zonder Search Console weet u niet welke pagina’s Google kent en op welke zoekopdrachten u verschijnt. Dan wordt alles giswerk."),
          ]), "fouten"),

   proza("Meten en rapporteren", "Hoe wij meten en rapporteren.", """
        <h3>De cijfers komen uit Search Console</h3>
        <p><a href="https://support.google.com/webmasters/answer/9128668" rel="noopener" target="_blank">Search Console</a> is een gratis dienst van Google waarmee u de aanwezigheid van uw site in de zoekresultaten bijhoudt. Het <a href="https://support.google.com/webmasters/answer/7576553" rel="noopener" target="_blank">prestatierapport</a> toont vier cijfers, die u zelf kunt nazien:</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Cijfer</th><th>Wat het is</th></tr></thead>
          <tbody>
            <tr><td><strong>Vertoningen</strong></td><td>Hoe vaak uw site in zoekresultaten is getoond.</td></tr>
            <tr><td><strong>Klikken</strong></td><td>Hoe vaak iemand vanuit Google op uw site heeft geklikt.</td></tr>
            <tr><td><strong>CTR</strong></td><td>Het aantal klikken gedeeld door het aantal vertoningen.</td></tr>
            <tr><td><strong>Gemiddelde positie</strong></td><td>De gemiddelde positie van het hoogste resultaat van uw site.</td></tr>
          </tbody>
        </table></div>
        <p>De gegevens zijn uit te splitsen naar zoekopdracht, pagina, land en apparaat. Zo ziet u welke pagina bij welke vraag bezoek oplevert.</p>

        <h3>Wat een positie wel en niet zegt</h3>
        <p>Google waarschuwt zelf dat een zoekopdracht in uw lijst kan staan zonder dat u uw site ziet wanneer u dezelfde zoekopdracht uitvoert. Zoekresultaten hangen af van het moment, de plaats, het apparaat en de recente geschiedenis van de zoeker. Een gemiddelde positie is dus een richting en geen plek. Om die reden noemt Complete AI geen positie vooraf en zet het rapport de positie naast klikken en aanvragen.</p>

        <h3>Wat het maandrapport bevat</h3>
        <p>Alles komt uit bronnen waar u zelf inzicht in heeft:</p>
        <ul>
          <li>Het aantal pagina’s dat Google heeft <strong>opgenomen in de zoekresultaten</strong>, en welke nog niet.</li>
          <li>De <strong>zoekopdrachten</strong> waarop uw bedrijf verschijnt, met de gemiddelde positie per pagina.</li>
          <li>Het aantal <strong>klikken</strong> vanuit Google naar uw site.</li>
          <li>De <strong>aanvragen</strong> die daaruit voortkwamen, via formulier of e-mail.</li>
          <li>Wat er die maand is <strong>aangepast of toegevoegd</strong>, en wat de volgende stap is.</li>
        </ul>
        <p>Het rapport meldt wat er is gebeurd. Het zegt niet wat er zal gebeuren. Een klik is bovendien nog geen aanvraag, en een aanvraag is nog geen klant. Daarom staan ze afzonderlijk in het rapport. Komt er ook betaald adverteren bij, dan heeft dat een eigen maandrapport; zie <a href="adverteren.html">adverteren</a>.</p>
""", "rapportage", "Een rapport dat u kunt controleren, in plaats van een grafiek die u moet geloven."),

   sectie("Wat u krijgt", "Van meting tot inhoud, in één hand.",
          "Geen losse adviezen die u zelf moet uitvoeren. Wij doen het werk en laten elke maand zien wat het heeft opgeleverd.",
          krijgtblok([
            ("Meting vooraf", "Wij beginnen in Search Console en in de zoekresultaten zelf: welke pagina’s Google kent, waarvoor u verschijnt en wie er nu boven u staat."),
            ("Technische basis", "Indexering, sitemap, structuurdata, laadsnelheid en weergave op een telefoon. Alles wat Google nodig heeft om uw pagina’s te vinden en te begrijpen."),
            ("Bestaande pagina’s aanpassen", "Titels, koppen en teksten aangepast op de zoekopdrachten waarop de pagina moet verschijnen."),
            ("Inhoud op de vragen van klanten", "Nieuwe pagina’s die antwoord geven op wat klanten intypen, opgebouwd rond de vraag met het antwoord direct bovenaan."),
            ("Google-bedrijfsprofiel", "Volledig ingericht: openingstijden, diensten, foto’s en beoordelingen. Wat mensen zien in Google Maps en naast de zoekresultaten."),
            ("Vast maandrapport", "Wat er is gedaan, welke pagina’s Google heeft opgenomen, op welke zoekopdrachten u verschijnt en hoeveel aanvragen dat opleverde."),
          ]), "wat-u-krijgt"),

   sectie("Werkwijze", "Van eerste meting tot maandelijks bijsturen in vier stappen.",
          "Wij beginnen bij wat Google nu van uw bedrijf weet en werken van daaruit naar de zoekopdrachten die aanvragen opleveren.",
          routeblok([
            ("Intake", "Een half uur om vast te stellen wat u levert, aan wie, en welke zoekopdrachten daarbij horen. Kosteloos en vrijblijvend."),
            ("Meting en plan", "Wij lezen uw huidige situatie uit in Search Console en in de zoekresultaten en leggen op papier wat er gedaan wordt, in welke volgorde en met welk vast maandbedrag."),
            ("Uitvoeren", "Eerst de technische basis en de bestaande pagina’s, daarna nieuwe pagina’s op de vragen van uw klanten."),
            ("Rapporteren en bijsturen", "Elke maand een rapport met cijfers die u zelf in Google kunt nazien. Wat werkt krijgt meer aandacht, wat niet werkt wordt aangepast."),
          ]), "werkwijze"),

   bronnen([
       ("Google Search Central: SEO-starterhandleiding", "https://developers.google.com/search/docs/fundamentals/seo-starter-guide", "Hoe Google vindt en opneemt, titels en beschrijvingen, wat niet telt, hoe lang wijzigingen duren."),
       ("Google Search Central: behulpzame, betrouwbare inhoud voor mensen", "https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "De toetsvragen voor inhoud, E-E-A-T en ‘Wie, hoe en waarom’."),
       ("Google Search Central: hoe Google Zoeken werkt", "https://developers.google.com/search/docs/fundamentals/how-search-works", "De drie stappen crawlen, indexeren en tonen, en geen betaling voor een hogere positie."),
       ("Google Search Central: heeft u een SEO nodig?", "https://developers.google.com/search/docs/fundamentals/do-i-need-seo", "Zelf doen of uitbesteden, en waar u op let bij het kiezen van een specialist."),
       ("Search Console-hulp: het rapport Pagina-indexering", "https://support.google.com/webmasters/answer/7440203", "Nieuwe sites, de statussen ‘Gevonden’ en ‘Gecrawld, momenteel niet geïndexeerd’ en wat geïndexeerd wel en niet betekent."),
       ("Google Search Central: hercrawlen aanvragen", "https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl", "Hoe lang crawlen kan duren en waarom herhaald aanvragen niet sneller gaat."),
       ("Search Console-hulp: het prestatierapport", "https://support.google.com/webmasters/answer/7576553", "Vertoningen, klikken, CTR en gemiddelde positie, en waarom de positie per zoeker verschilt."),
       ("Google Search Central: AI-functies en uw website", "https://developers.google.com/search/docs/appearance/ai-features", "Geen aanvullende eisen voor het AI-overzicht en geen speciale markeringen."),
       ("Google-bedrijfsprofiel Help: uw positie in lokale zoekresultaten verbeteren", "https://support.google.com/business/answer/7091", "Relevantie, afstand en prominentie, en wat er in het profiel hoort."),
       ("Google Search Central: Core Web Vitals", "https://developers.google.com/search/docs/appearance/core-web-vitals", "De drempels voor laden, reactie en visuele stabiliteit."),
       ("Google Search Central: pagina-ervaring", "https://developers.google.com/search/docs/appearance/page-experience", "Beveiligde verbinding, weergave op mobiel, geen opdringerige tussenschermen en Lighthouse."),
       ("Google Search Central: mobile-first indexing", "https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing", "Google gebruikt de mobiele versie van een pagina om te indexeren en te rangschikken."),
       ("Google Search Central: spamregels voor Google Zoeken", "https://developers.google.com/search/docs/essentials/spam-policies", "Linkspam en keyword stuffing."),
       ("Google Search Central: titels in zoekresultaten", "https://developers.google.com/search/docs/appearance/title-link", "Waarom elke pagina een unieke, beschrijvende titel nodig heeft."),
       ("Google Search Central: generatieve AI en uw inhoud", "https://developers.google.com/search/docs/fundamentals/using-gen-ai-content", "Wanneer AI-inhoud onder de spamregels valt en waar het nuttig is."),
       ("Search Console-hulp: over Search Console", "https://support.google.com/webmasters/answer/9128668", "Wat de gratis dienst laat zien."),
   ]),
 ]),
},

# ───────────────────────────── ADVERTEREN — SEA ─────────────────────────────
{
 "bestand": "adverteren.html",
 "dienst": "Adverteren — SEA",
 "titel": "Google Ads laten beheren of uitbesteden | Complete AI",
 "beschrijving": "Google Ads laten beheren: hoe de veiling werkt, wat u vooraf regelt en hoe een voorstel tot stand komt. Meting tot op de euro, één aanspreekpunt.",
 "omschrijving": "Google Ads en Meta-advertenties voor mkb-bedrijven: hoe de veiling werkt, campagne opzetten, aanvragen meten en maandelijks bijsturen. Op aanvraag.",
 "ogen": "Adverteren — SEA",
 "h1": 'Google Ads laten beheren: <span class="glans">zichtbaar</span> op het moment dat iemand zoekt.',
 "lead": "Google Ads laten beheren of uitbesteden betekent dat een specialist uw zoekcampagne opzet, meet en bijstuurt, terwijl u het advertentiebudget rechtstreeks aan Google betaalt. Bij zoekadvertenties betaalt u per klik, en Google bepaalt bij elke zoekopdracht welke advertentie verschijnt. Complete AI voert dat beheer uit en koppelt de meting, zodat elke aanvraag te herleiden is tot een advertentie.",
 "levertijd": "Op aanvraag",
 "gepubliceerd": "2026-09-24",
 "gewijzigd": "2026-09-24",
 "uitkomsten": [
     ("Tot op de euro", "meetbaar: welke advertentie welke aanvraag opleverde"),
     ("Maandelijks", "bijgestuurd op wat de cijfers laten zien, geen ongerichte campagnes"),
     ("Na de intake", "weet u wat het kost en wat het redelijkerwijs kan opleveren"),
 ],
 "slot_kop": "Loont adverteren voor uw bedrijf?",
 "slot_tekst": "In de intake bekijken wij welke zoekopdrachten in uw markt bestaan, wie daar op biedt en of de rekening klopt. Blijkt dat adverteren nu niet loont, dan hoort u dat ook.",
 "vragen": [
   ("Hoe werkt adverteren op Google?",
    "U kiest de zoekopdrachten waarop uw advertentie mag verschijnen, schrijft de advertentie en bepaalt wat u per klik maximaal wilt betalen. Bij elke zoekopdracht houdt Google een veiling: het bod, de kwaliteit van advertentie en pagina en de context bepalen welke advertenties verschijnen en in welke volgorde. U betaalt wanneer iemand klikt. Lees <a href=\"#hoe-het-werkt\">hoe Google Ads werkt</a>."),
   ("Wat zijn de kosten van een Google Ads specialist?",
    "Die hangen af van uw branche, uw regio, wie er verder op dezelfde zoekwoorden biedt en wat u wilt bereiken. Daarom staat er geen bedrag op deze pagina. Na de intake ligt er één vaste prijs voor het beheer op papier, zonder nacalculatie. Het advertentiebudget betaalt u los daarvan aan Google of Meta. Zie <a href=\"#voorstel\">het voorstel</a>."),
   ("Wat kost Google Ads?",
    "Er zijn twee kostenposten: het advertentiebudget, dat u zelf bepaalt en rechtstreeks aan Google betaalt, en het beheer. Wat een klik kost, hangt af van uw branche en van wie er nog meer op dezelfde zoekopdracht biedt, want elke veiling valt anders uit. Daarom noemen wij vooraf geen bedrag. Na de intake hoort u wat er nodig is."),
   ("Wie kan mij helpen met Google Ads?",
    "Drie partijen: u zelf, een specialist of bureau, of de hulp van Google zelf. Zelf doen kost tijd voor opzet, meting en bijsturen. Een specialist neemt dat werk over. Bij Complete AI is dat één aanspreekpunt voor de campagne, de website en de meting, zodat niets tussen partijen blijft liggen. Vraag bij elke aanbieder hoe succes wordt gemeten."),
   ("Hoe kan Google Ads u helpen om uw bedrijfsdoelen te behalen?",
    "Door uw doel meetbaar te maken. U kiest wat u waardevol vindt, zoals een aanvraag via het formulier, een telefoongesprek of een aankoop, en Google Ads meet welke zoekwoorden en advertenties dat opleveren. Zo stuurt u uw uitgaven op aanvragen in plaats van op klikken. Welk doel bij uw bedrijf past, bepalen we in de intake."),
   ("Bestaat er gratis tegoed voor Google Ads?",
    "Google of zijn partners bieden op wisselende momenten promotietegoed aan, vooral aan nieuwe adverteerders, maar Google Support kan er geen op verzoek verstrekken. Het tegoed is geen cashback: u geeft eerst zelf uit aan advertenties, en de voorwaarden verschillen per aanbieding. Welke aanbieding voor u geldt, ziet u op de pagina Promoties in uw Google Ads-account."),
   ("Hoe weet ik of adverteren loont?",
    "Door aanvragen te meten in plaats van klikken. Wij richten conversietracking in, zodat elke aanvraag te herleiden is tot de advertentie waar hij vandaan kwam. U ziet dan wat een aanvraag kost en kunt dat naast wat een klant u oplevert leggen."),
   ("Wat is het verschil tussen SEA en SEO?",
    "SEA zijn betaalde advertenties: ze werken direct en stoppen wanneer het budget stopt. SEO is het werk aan de gewone zoekresultaten: het bouwt langzaam op en blijft staan. Ze vullen elkaar aan. Meer over de tweede route leest u bij <a href=\"vindbaarheid-seo.html\">vindbaarheid — SEO</a>."),
   ("Kan ik adverteren en SEO combineren?",
    "Ja. Advertenties laten snel zien welke zoekopdrachten aanvragen opleveren. Die inzichten gebruiken wij om pagina’s te schrijven die daarna ook zonder advertentie gevonden worden. Google schrijft dat adverteren de gewone zoekresultaten niet beïnvloedt, dus beide routes hebben hun eigen werk. Lees <a href=\"#samenhang\">hoe ze samenhangen</a>."),
   ("Moet ik adverteren op Google of op Facebook en Instagram?",
    "Dat hangt af van waar uw klant zich bevindt op het moment dat hij u nodig heeft. Op Google zoekt hij naar wat u levert. Op Facebook en Instagram bent u zichtbaar, en met retargeting bereikt u wie uw site al bezocht. Die groep moet eerst bestaan, dus de zoekcampagne komt logischerwijs eerst. Zie <a href=\"#zoek-of-meta\">zoekcampagne of Meta</a>."),
   ("Aan wie betaal ik het advertentiebudget?",
    "Rechtstreeks aan Google of Meta, niet aan Complete AI. Wij leveren het beheer: de opzet, de meting en het maandelijks bijsturen. U bepaalt het budget, en omdat u het aan Google of Meta betaalt, kunt u de uitgaven daar zelf naast ons maandrapport leggen."),
   ("Waarom staat er geen prijs op deze pagina?",
    "Omdat een getal u eerder zou misleiden dan helpen. Wat een advertentie kost en wat zij oplevert hangt af van uw branche, uw regio, wie er verder op dezelfde zoekwoorden biedt en wat u wilt bereiken. Na de intake hoort u wat er nodig is, onderbouwd met de cijfers van uw eigen markt."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   inhoudsopgave([
       ("hoe-het-werkt", "Hoe Google Ads werkt"),
       ("zoek-of-meta", "Zoekcampagne of Meta"),
       ("vooraf", "Wat u vooraf moet regelen"),
       ("herkenbaar", "Waar het bij bestaande campagnes misloopt"),
       ("wat-u-krijgt", "Wat u krijgt"),
       ("waarom-op-aanvraag", "Waarom er geen bedrag staat"),
       ("voorstel", "Van intake tot voorstel"),
       ("werkwijze", "Werkwijze"),
       ("samenhang", "Samenhang met SEO en de site"),
       ("eigen-praktijk", "Uit eigen praktijk"),
       ("rapportage", "Hoe wij rapporteren"),
       ("fouten", "Veelgemaakte fouten"),
       ("bronnen", "Bronnen"),
   ]),

   proza("Hoe het werkt", "Hoe werkt Google Ads: veiling, biedingen en kwaliteitsscore.", """
        <h3>De veiling in drie stappen</h3>
        <p>Zoekt iemand op Google, dan zoekt het systeem alle advertenties waarvan de zoekwoorden bij die zoekopdracht passen. Advertenties die niet geschikt zijn, bijvoorbeeld omdat ze een ander land targeten of zijn afgekeurd, vallen af. Van de rest kunnen alleen de advertenties verschijnen waarvan de advertentierangschikking hoog genoeg is. Dat beschrijft de <a href="https://support.google.com/google-ads/answer/142918?hl=nl" rel="noopener" target="_blank">hulp van Google Ads over de veiling</a>.</p>
        <p>Die veiling vindt bij elke zoekopdracht opnieuw plaats. De uitkomst verschilt daarom per keer. Google noemt het normaal dat de positie van een advertentie schommelt en dat een advertentie soms wel en soms niet verschijnt.</p>

        <h3>Wat de advertentierangschikking bepaalt</h3>
        <p>De advertentierangschikking is een reeks waarden, berekend uit meer dan het bod alleen. Google noemt <a href="https://support.google.com/google-ads/answer/6366577?hl=nl" rel="noopener" target="_blank">zes factoren</a>:</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Factor</th><th>Wat Google bedoelt</th></tr></thead>
          <tbody>
            <tr><td><strong>Uw bod</strong></td><td>Het maximumbedrag dat u bereid bent te betalen voor een klik. Wat u uiteindelijk betaalt, kan lager zijn.</td></tr>
            <tr><td><strong>Kwaliteit van advertentie en pagina</strong></td><td>De bruikbaarheid en relevantie van de advertentie en de landingspagina, wat de bezoeker na de klik verwacht, en het gemak waarmee hij zich op de pagina beweegt.</td></tr>
            <tr><td><strong>Verwacht effect van componenten</strong></td><td>Extra informatie in de advertentie, zoals een telefoonnummer of links naar pagina’s op uw site. Google schat het effect ervan.</td></tr>
            <tr><td><strong>Drempels voor rangschikking</strong></td><td>Minimale kwaliteitsdrempels waaraan een advertentie moet voldoen voor een bepaalde positie.</td></tr>
            <tr><td><strong>Context van de zoekopdracht</strong></td><td>De zoektermen, de locatie van de zoeker, het apparaat, het tijdstip en de andere advertenties op de pagina.</td></tr>
            <tr><td><strong>Concurrentiepositie</strong></td><td>Het verschil in rangschikking met andere adverteerders die om dezelfde plek strijden.</td></tr>
          </tbody>
        </table></div>
        <p>Het punt dat Google zelf het belangrijkste noemt: ook wanneer concurrenten hoger bieden, kunt u een hogere positie behalen tegen een lagere prijs, met zeer relevante zoekwoorden en advertenties. Een hoger bod is dus niet de enige route, en niet per se de goedkoopste.</p>

        <h3>Wat de kwaliteitsscore is, en wat niet</h3>
        <p>De <a href="https://support.google.com/google-ads/answer/6167118?hl=nl" rel="noopener" target="_blank">kwaliteitsscore</a> loopt van 1 tot 10 en wordt per zoekwoord gegeven. Zij is opgebouwd uit drie onderdelen: de verwachte klikfrequentie, de relevantie van de advertentie en de ervaring op de landingspagina. Elk onderdeel krijgt de beoordeling hoger dan gemiddeld, gemiddeld of lager dan gemiddeld, vergeleken met andere adverteerders op dezelfde zoekopdracht in de afgelopen 90 dagen.</p>
        <div class="noot"><p><strong>Twee punten die Google zelf benadrukt.</strong> De kwaliteitsscore is geen factor in de veiling, maar een diagnostisch hulpmiddel. En zij is geen prestatie-indicator die u moet optimaliseren. De kwaliteit van advertentie en pagina telt dus wel mee in de veiling, maar het cijfer is een samenvatting en geen doel. Het doel is het aantal aanvragen en wat ze kosten.</p></div>

        <h3>Biedingen: handmatig of automatisch</h3>
        <p>Google Ads kent <a href="https://support.google.com/google-ads/answer/2472725?hl=nl" rel="noopener" target="_blank">biedstrategieën per doel</a>: klikken, zichtbaarheid of conversies. Wie op aanvragen stuurt, kan Slim bieden gebruiken. Google past dan bij elke veiling het bod aan om zoveel mogelijk conversies te halen. Daarvoor moet de conversiemeting kloppen; Google noemt dat een belangrijk aandachtspunt. Een automatische strategie heeft daarna volgens Google een leerfase van 7 tot 14 dagen nodig, en Google adviseert in die periode geen frequente wijzigingen in budget, doelen of conversiedoelen aan te brengen, omdat elke wijziging de leerfase opnieuw laat beginnen.</p>

        <h3>Zoekwoorden en zoektypen</h3>
        <p>Een zoekwoord koppelt uw advertentie aan wat mensen intypen. Het <a href="https://support.google.com/google-ads/answer/7478529?hl=nl" rel="noopener" target="_blank">zoektype</a> bepaalt hoe dicht de zoekopdracht bij het zoekwoord moet liggen:</p>
        <ul>
          <li><strong>Breed</strong> is de standaard. De advertentie kan ook verschijnen bij gerelateerde zoekopdrachten waarin de directe betekenis van het zoekwoord niet voorkomt.</li>
          <li><strong>Woordgroep</strong> toont de advertentie bij zoekopdrachten die de betekenis van het zoekwoord omvatten.</li>
          <li><strong>Exact</strong> toont de advertentie bij zoekopdrachten met dezelfde betekenis of intentie. U houdt de meeste controle en bereikt de minste zoekopdrachten.</li>
        </ul>
        <p>Google noemt het essentieel om Slim bieden te gebruiken wanneer u breed zoeken inzet. Breed zoeken zonder goede meting en zonder uitsluitingen kan budget laten weglopen naar zoekopdrachten die niet bij uw bedrijf horen.</p>
""", "hoe-het-werkt", "Bij elke zoekopdracht houdt Google een veiling om te bepalen welke advertenties verschijnen en in welke volgorde. Wat daarin meetelt, staat in de hulp van Google Ads zelf."),

   proza("Zoeken of Meta", "Zoekcampagne of Meta-advertenties: welke past bij uw bedrijf?", """
        <div class="tabelwrap"><table>
          <thead><tr><th>Aspect</th><th>Google-zoekcampagne en Meta vergeleken</th></tr></thead>
          <tbody>
            <tr><td><strong>Wie u bereikt</strong></td><td><strong>Google:</strong> iemand die op dit moment zoekt naar wat u levert.<br><strong>Meta:</strong> iemand op Facebook of Instagram, en met retargeting iemand die uw site al bezocht.</td></tr>
            <tr><td><strong>Wanneer de advertentie verschijnt</strong></td><td><strong>Google:</strong> bij een zoekopdracht waar de veiling voor is gewonnen.<br><strong>Meta:</strong> wanneer de persoon zich in de doelgroep bevindt die u kiest.</td></tr>
            <tr><td><strong>Wat het vereist</strong></td><td><strong>Google:</strong> zoekwoorden, een advertentietekst en een pagina waar de klik op uitkomt.<br><strong>Meta:</strong> voor retargeting de Meta Pixel op uw site en bezoekers om uit te kiezen.</td></tr>
            <tr><td><strong>Waarvoor het dient</strong></td><td><strong>Google:</strong> vraag die er al is, van mensen die een aanbieder zoeken.<br><strong>Meta:</strong> zichtbaar blijven bij wie twijfelt of nog niet besloot.</td></tr>
            <tr><td><strong>Waar u op let</strong></td><td><strong>Google:</strong> wie er verder op dezelfde zoekwoorden biedt.<br><strong>Meta:</strong> zonder bezoek is er geen doelgroep om opnieuw te bereiken.</td></tr>
          </tbody>
        </table></div>

        <h3>Wat retargeting is</h3>
        <p>Meta beschrijft in zijn <a href="https://developers.facebook.com/docs/meta-pixel/implementation/custom-audiences" rel="noopener" target="_blank">documentatie over de Meta Pixel</a> dat u bezoekers van uw website kunt indelen in groepen op basis van wat ze op de site deden. Zulke groepen heten aangepaste doelgroepen. De basiscode van de Pixel moet daarvoor al op de site staan en gebeurtenissen registreren. Retargeting bereikt dus alleen wie eerder is geweest. Uw site moet eerst bezoek krijgen.</p>

        <h3>In welke volgorde</h3>
        <p>Omdat retargeting bezoekers nodig heeft, komt de route die bezoek oplevert eerst: de zoekcampagne, of de gewone vindbaarheid via <a href="vindbaarheid-seo.html">SEO</a>. Meta voegt zich daarna toe, voor wie de site heeft bekeken en nog twijfelt. Welke combinatie bij uw bedrijf past en in welke volgorde, bepalen we in de intake. Wij beginnen klein, meten alles en schalen op wat aantoonbaar werkt.</p>
""", "zoek-of-meta", "Google Ads en Meta bereiken mensen in een andere situatie. Dat verschil bepaalt waar u begint."),

   proza("Vooraf", "Wat u vooraf moet weten en regelen.", """
        <h3>1. Conversietracking: wat telt als resultaat</h3>
        <p>Een conversie is een handeling die voor u waarde heeft. Google noemt als voorbeelden een aankoop, een aanmelding en een telefoongesprek. U kiest zelf wat telt. Voor een bedrijf dat aanvragen wil, is dat het verstuurde formulier en het telefoongesprek vanuit de advertentie. Google kan gesprekken meten die rechtstreeks vanuit de advertentie komen, gesprekken naar het nummer op uw site en klikken op een telefoonnummer op de mobiele site.</p>
        <p>Volgens de hulp over <a href="https://support.google.com/google-ads/answer/1722022?hl=nl" rel="noopener" target="_blank">conversiemeting</a> ziet u zo welke zoekwoorden, advertenties en campagnes de waardevolle handelingen opleveren, kunt u het rendement van uw uitgaven beoordelen en kunnen automatische biedstrategieën erop sturen. Zonder meting weet u alleen hoeveel mensen klikten.</p>
        <p>Een aanvraag is nog geen klant. Wat een aanvraag kost en wat een klant u oplevert zijn twee verschillende cijfers, en het rendement blijkt pas uit de combinatie. Bespreek daarom in de intake wat een gemiddelde klant u oplevert.</p>

        <h3>2. Een landingspagina waar de klik op uitkomt</h3>
        <p>Na de klik beslist de pagina. De ervaring op de landingspagina is een van de drie onderdelen van de kwaliteitsscore: hoe relevant en nuttig de pagina is voor wie op de advertentie klikt. Drie eisen:</p>
        <ul>
          <li>De pagina sluit aan op de advertentie. Wie een advertentie over een dienst aanklikt, komt op de pagina over die dienst en niet op de homepage.</li>
          <li>De pagina laadt snel op een telefoon.</li>
          <li>De vervolgstap is duidelijk: een formulier, een telefoonnummer of een afspraak.</li>
        </ul>
        <p>Bij Complete AI is dit de website die hoort bij de campagne. Meer over hoe die wordt gebouwd, leest u bij <a href="websites.html">websites</a>.</p>

        <h3>3. Zoekwoorden met koopintentie</h3>
        <p>Niet elke zoekopdracht komt van iemand die iets wil afnemen. ‘Hoe werkt een cv-ketel’ is een vraag om uitleg. ‘Cv-ketel laten vervangen’ is een vraag om een aanbieder. Een campagne op zoekwoorden met koopintentie richt zich op het tweede soort. De uitleg-zoekopdrachten zijn geen slechte zoekers, maar ze horen bij gewone vindbaarheid en niet bij betaalde klikken. Zie <a href="vindbaarheid-seo.html">SEO voor mkb</a>.</p>

        <h3>4. Uitsluitingszoekwoorden</h3>
        <p>Met <a href="https://support.google.com/google-ads/answer/2453972?hl=nl" rel="noopener" target="_blank">uitsluitingszoekwoorden</a> houdt u zoekopdrachten buiten uw campagne die op uw zoekwoorden lijken maar iets anders bedoelen. Google geeft zelf het voorbeeld van een opticien die brillen verkoopt en ‘wc-bril’ en ‘duikbril’ uitsluit. Twee aandachtspunten uit die hulp: uitsluitingen gelden niet automatisch voor enkelvoud, meervoud en synoniemen, die voegt u zelf toe, en u kunt een lijst op accountniveau maken die voor alle zoekcampagnes in het account geldt.</p>
        <p>De lijst begint bij de opzet en groeit met wat de zoektermen laten zien. Daarom staat het bijsturen van de uitsluitingen in het maandelijkse werk.</p>

        <h3>5. Meten en toestemming van de bezoeker</h3>
        <p>Meten met de Google-tag of de Meta Pixel betekent dat er code op uw site staat die handelingen van bezoekers registreert. Plaatst die code cookies die gedrag volgen, dan moeten bezoekers daarvoor volgens de <a href="https://www.autoriteitpersoonsgegevens.nl/themas/internet-slimme-apparaten/cookies/tracking-cookies" rel="noopener" target="_blank">Autoriteit Persoonsgegevens</a> toestemming geven, met een duidelijke keuze om te weigeren. Hoe dat in uw situatie is ingericht, komt in de intake en in het voorstel aan bod. Deze site volgt geen bezoekers en heeft daarom geen cookiebanner nodig.</p>
""", "vooraf", "Vijf onderdelen bepalen of een campagne bruikbare cijfers geeft. Ze staan vóór het eerste bod."),

   sectie("De situatie", "Budget dat loopt zonder dat iemand weet wat het oplevert.",
          "Vier situaties die wij bij bestaande campagnes terugzien.",
          pijnblok([
            ("Klikken zonder aanvragen", "Het budget loopt en er komen bezoekers, maar niemand weet welke advertentie tot een aanvraag leidde."),
            ("Zoekwoorden die te breed zijn", "Advertenties op algemene termen trekken klikken van mensen die niet van plan zijn iets te kopen."),
            ("Een campagne die niemand bijstuurt", "Een campagne opzetten kost een middag. De winst zit in wat er de maanden erna wordt bijgestuurd."),
            ("Een klik naar een pagina die niet overtuigt", "De klik is betaald en de bezoeker vindt geen reden om contact op te nemen."),
          ]), "herkenbaar"),

   sectie("Wat u krijgt", "Een campagne die u kunt nalezen tot op de euro.",
          "Wij beginnen klein, meten alles en schalen op wat aantoonbaar werkt.",
          krijgtblok([
            ("Google Ads op koopintentie", "Advertenties op zoekopdrachten van mensen die een dienst zoeken en willen afnemen, niet op algemene termen."),
            ("Meta en retargeting", "Voor bezoekers die uw site hebben bekeken en nog twijfelen: zichtbaar blijven op Facebook en Instagram."),
            ("Conversietracking", "Formulieren en andere aanvragen worden gekoppeld aan de advertentie waar ze vandaan komen."),
            ("Een pagina waar de klik op uitkomt", "Advertentie en pagina sluiten op elkaar aan, met een duidelijke vervolgstap."),
            ("Maandelijks bijsturen", "Zoekwoorden, teksten en biedingen worden aangepast op wat de cijfers laten zien."),
            ("Eén aanspreekpunt", "Advertenties, site en meting bij dezelfde persoon, zodat niets tussen partijen blijft liggen."),
          ]), "wat-u-krijgt"),

   sectie("Waarom op aanvraag", "Waarom er geen bedrag op deze site staat.",
          "Bij de andere diensten kunnen wij vooraf zeggen wat er gebeurt en wanneer het staat. Bij adverteren hangt dat van uw markt af, en elke veiling van Google valt bij elke zoekopdracht anders uit.",
          eerlijkblok(
            "Wat het voorstel bepaalt",
            "Een getal op een pagina zou u eerder misleiden dan helpen. Vier verschillen tussen bedrijven maken een standaardvoorstel onbetrouwbaar, en om dezelfde reden staan er nergens op deze site bedragen:",
            ["<strong>Uw branche.</strong> Wat een klik kost verschilt sterk per sector.",
             "<strong>Uw regio.</strong> Het aantal zoekers en het aantal bieders verschilt per gebied.",
             "<strong>Uw concurrenten.</strong> Wie er verder op dezelfde zoekwoorden biedt bepaalt de prijs per klik.",
             "<strong>Uw doel.</strong> Aanvragen, afspraken of verkoop vragen een andere opzet."]),
          "waarom-op-aanvraag"),

   proza("Voorstel", "Van intake tot voorstel: hoe een advertentiecampagne tot stand komt.", """
        <h3>Wat in de intake aan bod komt</h3>
        <p>De intake duurt een half uur, is kosteloos en vrijblijvend. We bespreken:</p>
        <ol>
          <li>Wat u wilt bereiken: aanvragen, afspraken, telefoongesprekken of verkoop.</li>
          <li>Welke zoekopdrachten daarbij horen en wie daar al op biedt.</li>
          <li>Wat een aanvraag of klant u oplevert, want alleen dan is te beoordelen of adverteren loont.</li>
          <li>Wat uw website nu doet: waar een klik op uitkomt en of een aanvraag aankomt.</li>
          <li>Hoe gemeten wordt, inclusief de toestemming van de bezoeker.</li>
        </ol>

        <h3>Wat er in het voorstel staat</h3>
        <p>Na de intake volgt het voorstel: wat er nodig is, wat het kost en wat het redelijkerwijs kan opleveren, onderbouwd met de cijfers van uw eigen markt. Dat is de vaste werkwijze van Complete AI: één vaste prijs, zonder nacalculatie, gefaseerd opgebouwd. De campagne staat pas live wanneer u akkoord bent.</p>

        <h3>Twee kostenposten, twee ontvangers</h3>
        <div class="tabelwrap"><table>
          <thead><tr><th>Kostenpost</th><th>Wat het is, en aan wie u betaalt</th></tr></thead>
          <tbody>
            <tr><td><strong>Advertentiebudget</strong></td><td>Wat er wordt uitgegeven aan de klikken op uw advertenties. U bepaalt het; het voorstel onderbouwt wat er nodig is.<br><em>U betaalt:</em> rechtstreeks aan Google of Meta.</td></tr>
            <tr><td><strong>Beheer</strong></td><td>Het werk van Complete AI: opzet, meting, bijsturen en rapport. Eén vaste prijs na de intake.<br><em>U betaalt:</em> aan Complete AI.</td></tr>
          </tbody>
        </table></div>
        <p>Google noemt geen vast bedrag voor een klik: de uitkomst ontstaat bij elke veiling opnieuw, uit het bod, de kwaliteit en de concurrentie op dat moment. Daarom kan een betrouwbaar voorstel pas na de intake komen. De redenering staat ook op de <a href="index.html">homepage</a>, en de <a href="index.html#contact">intake plant u hier</a>.</p>
""", "voorstel", "Bij adverteren komt het voorstel na de intake, en het is onderbouwd met de markt waarin u adverteert."),

   sectie("Werkwijze", "Van eerste gesprek tot maandelijks bijsturen in vier stappen.",
          "Wij beginnen bij de vraag of adverteren in uw markt kan lonen, niet bij de campagne.",
          routeblok([
            ("Intake", "Een half uur om vast te stellen wat u wilt bereiken en welke zoekopdrachten daarbij horen. Kosteloos en vrijblijvend."),
            ("Voorstel", "Wat er nodig is, wat het kost en wat het redelijkerwijs kan opleveren, onderbouwd met de cijfers van uw eigen markt."),
            ("Opzetten", "Campagne, advertentieteksten, meting en de pagina waar de klik op uitkomt. Pas live wanneer u akkoord bent."),
            ("Bijsturen", "Elke maand een rapport met kosten per aanvraag, en aanpassingen op wat de cijfers laten zien."),
          ]), "werkwijze"),

   proza("Samenhang", "Adverteren, SEO en uw website: hoe ze samenhangen.", """
        <p>Advertenties, gewone zoekresultaten en de site richten zich op dezelfde zoeker. Vijf verbanden:</p>
        <ul>
          <li><strong>Advertenties beïnvloeden uw gewone positie niet.</strong> Google schrijft in <a href="https://developers.google.com/search/docs/fundamentals/do-i-need-seo" rel="noopener" target="_blank">zijn uitleg voor site-eigenaren</a> dat adverteren met Google geen effect heeft op de aanwezigheid van uw site in de gewone zoekresultaten. Een advertentie koopt dus geen SEO.</li>
          <li><strong>Advertenties leren u wat werkt.</strong> Ze laten snel zien welke zoekopdrachten aanvragen opleveren. Die inzichten gebruiken wij om pagina’s te schrijven die daarna ook zonder advertentie gevonden worden. Meer daarover bij <a href="vindbaarheid-seo.html">vindbaarheid — SEO</a>.</li>
          <li><strong>De site is de landingspagina.</strong> Wat een betaalde klik oplevert, hangt af van de pagina waarop hij uitkomt. Snel, mobiel eerst en met een duidelijke vervolgstap: zie <a href="websites.html">websites</a>.</li>
          <li><strong>Na de klik begint het werk.</strong> Een aanvraag die binnenkomt moet worden opgevolgd. Een offerte, een afspraak en een herinnering kunnen vanzelf verlopen; zie <a href="automatisering.html">automatisering</a>. En belt iemand na de klik op een moment dat niemand kan opnemen, dan neemt <a href="ai-telefonist.html">de AI-telefonist</a> op.</li>
          <li><strong>Een goed bericht bereikt meer mensen.</strong> Een <a href="social-media.html">social-mediabericht</a> dat goed werkt, kan als Meta-advertentie ook mensen bereiken die u nog niet volgen.</li>
        </ul>
""", "samenhang", "Wie adverteert, betaalt voor het bezoek. Wat er met dat bezoek gebeurt, bepaalt het rendement."),

   sectie("Uit eigen praktijk", "Uit eigen praktijk: wat er na de klik gebeurt.",
          "Bij Aronza, het e-commercebedrijf van de oprichter van Complete AI, lopen facturatie, kostenregistratie, orderverwerking, voorraadbeheer en klantcontact sinds begin mei 2026 op dezelfde gegevens. <a href=\"case-aronza.html\">De volledige case leest u hier</a>. Voor een adverteerder is dat het deel na de klik.",
          voorbeeldblok([
            ("Eén order, drie bijwerkingen", "Bij Aronza raakt een binnenkomende order de voorraad, de factuur en het klantdossier, zonder dat er iets wordt overgetypt. Een aanvraag na een klik hoeft dus niet in een mailbox te blijven liggen."),
            ("Offertes maken en opvolgen", "Een van de automatiseringen die vandaag al draaien en getest zijn: offertes opstellen, versturen en zien wie er nog niet heeft gereageerd."),
            ("Online een afspraak boeken", "Klanten plannen zelf een afspraak via een link, rechtstreeks in uw agenda."),
            ("Een telefoon die wordt opgenomen", "Neemt de AI-telefonist op buiten openingstijden en tijdens drukte, noteert hij de bestelling of de vraag en zet hij een terugbelnotitie klaar met volledig transcript."),
            ("Een pagina die snel laadt", "Websites van Complete AI zijn gebouwd om snel te zijn, mobiel eerst. Deze site laadt in ongeveer 0,7 seconde: de norm voor elke pagina waar een klik op uitkomt."),
          ]), "eigen-praktijk"),

   proza("Rapportage", "Hoe wij rapporteren: kosten per aanvraag in plaats van klikken.", """
        <p>Elke maand ontvangt u een rapport met de kosten per aanvraag, en de aanpassingen die daaruit volgden. Het rapport bevat:</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Cijfer</th><th>De vraag die het beantwoordt</th></tr></thead>
          <tbody>
            <tr><td><strong>Aanvragen per campagne en advertentie</strong></td><td>Welke advertentie leverde een formulier of een telefoongesprek op?</td></tr>
            <tr><td><strong>Kosten per aanvraag</strong></td><td>Wat kost een aanvraag, en hoe verhoudt dat zich tot wat een klant u oplevert?</td></tr>
            <tr><td><strong>Zoektermen</strong></td><td>Op welke zoekopdrachten zijn de advertenties getoond, en welke zijn uitgesloten?</td></tr>
            <tr><td><strong>Aanpassingen</strong></td><td>Welke zoekwoorden, teksten en biedingen zijn gewijzigd, en waarom?</td></tr>
            <tr><td><strong>Klikken en uitgaven</strong></td><td>Ter context. Klikken zeggen niets over aanvragen.</td></tr>
          </tbody>
        </table></div>
        <p>Omdat u het budget rechtstreeks aan Google of Meta betaalt, kunt u de uitgaven daar zelf naast het rapport leggen.</p>

        <h3>Waarom maandelijks en niet dagelijks</h3>
        <p>Wij sturen maandelijks bij. Dat past bij wat Google over automatische biedstrategieën schrijft: ze hebben een leerfase van 7 tot 14 dagen nodig en die begint opnieuw bij frequente wijzigingen in budget, doelen of conversiedoelen. Een campagne die elke dag wordt omgegooid, leert niets.</p>

        <h3>Wat het rapport niet doet</h3>
        <p>Het rapport meldt wat er is gebeurd. Het zegt niet wat er zal gebeuren. De positie van een advertentie schommelt volgens Google per veiling, en het aantal aanvragen hangt af van de markt. Het voorstel noemt daarom wat de campagne redelijkerwijs kan opleveren, en doet geen toezegging.</p>
""", "rapportage", "Klikken zijn makkelijk te tellen. Aanvragen en wat ze kosten zijn wat u nodig heeft om te beslissen."),

   sectie("Veelgemaakte fouten", "Acht fouten bij Google Ads.",
          "Zes van de acht staan in de documentatie van Google Ads. Eén volgt uit de regels van de Autoriteit Persoonsgegevens en één uit hoe een campagne werkt.",
          krijgtblok([
            ("Klikken tellen in plaats van aanvragen", "Klikken zeggen niets over aanvragen. Stuur op wat een aanvraag kost en wat een klant oplevert."),
            ("Alles als resultaat tellen", "Google laat u kiezen wat waardevol is. Telt u elke paginaweergave mee, dan stuurt een automatische biedstrategie op iets wat geen aanvraag is."),
            ("Zoekwoorden te breed en geen uitsluitingen", "Breed zoeken is de standaard en bereikt ook gerelateerde zoekopdrachten. Zonder uitsluitingszoekwoorden en goede meting loopt het budget naar zoekopdrachten die niet passen."),
            ("Adverteren op de homepage", "De ervaring op de landingspagina is een onderdeel van de kwaliteitsscore. Laat een advertentie over een dienst uitkomen op de pagina over die dienst."),
            ("De kwaliteitsscore als doel", "Google noemt de score een diagnostisch hulpmiddel en geen indicator die u moet optimaliseren. Het doel is een aanvraag."),
            ("Steeds wijzigen in de leerfase", "Frequente wijzigingen in budget, doelen of conversiedoelen laten de leerfase van 7 tot 14 dagen opnieuw beginnen."),
            ("Jagen op de eerste positie", "De positie schommelt per veiling, en een hogere positie kan ook met een lager bod door betere relevantie. Een positie is geen doel."),
            ("Meten zonder toestemming", "Tracking cookies vragen volgens de Autoriteit Persoonsgegevens om toestemming van de bezoeker. Regel dat vóór de eerste klik, niet erna."),
          ]), "fouten"),

   bronnen([
       ("Google Ads-hulp: veiling", "https://support.google.com/google-ads/answer/142918?hl=nl", "Hoe de veiling bij elke zoekopdracht werkt en waarom posities schommelen."),
       ("Google Ads-hulp: hoe de Google Ads-veiling werkt", "https://support.google.com/google-ads/answer/6366577?hl=nl", "De zes factoren die bepalen welke advertenties verschijnen, en dat concurrenten met een hoger bod niet altijd winnen."),
       ("Google Ads-hulp: advertentierangschikking", "https://support.google.com/google-ads/answer/1752122?hl=nl", "Wat de advertentierangschikking is en waaruit zij wordt berekend."),
       ("Google Ads-hulp: kwaliteitsscore voor zoekcampagnes", "https://support.google.com/google-ads/answer/6167118?hl=nl", "De schaal van 1 tot 10, de drie onderdelen en waarom de score een diagnostisch hulpmiddel is."),
       ("Google Ads-hulp: conversiemeting", "https://support.google.com/google-ads/answer/1722022?hl=nl", "Wat een conversie is, welke acties u kunt meten en de leerfase van Slim bieden."),
       ("Google Ads-hulp: biedstrategie op basis van doelen", "https://support.google.com/google-ads/answer/2472725?hl=nl", "Biedstrategieën per doel en het belang van juiste conversiemeting."),
       ("Google Ads-hulp: opties voor zoekwoordovereenkomsten", "https://support.google.com/google-ads/answer/7478529?hl=nl", "Breed, woordgroep en exact zoeken."),
       ("Google Ads-hulp: uitgesloten zoekwoorden", "https://support.google.com/google-ads/answer/2453972?hl=nl", "Hoe uitsluitingen werken, het voorbeeld van de opticien en lijsten op accountniveau."),
       ("Google Ads-hulp: verschillende typen promoties", "https://support.google.com/google-ads/answer/2393021?hl=nl", "Promotietegoed voor nieuwe adverteerders en wat Google Support wel en niet kan verstrekken."),
       ("Google Ads-hulp: over promoties", "https://support.google.com/google-ads/answer/6388096?hl=nl", "Promotietegoed is geen cashback of terugbetaling."),
       ("Google Search Central: heeft u een SEO nodig?", "https://developers.google.com/search/docs/fundamentals/do-i-need-seo", "Adverteren met Google heeft geen effect op de gewone zoekresultaten."),
       ("Autoriteit Persoonsgegevens: tracking cookies", "https://www.autoriteitpersoonsgegevens.nl/themas/internet-slimme-apparaten/cookies/tracking-cookies", "Toestemming voor tracking cookies en een duidelijke keuze om te weigeren."),
       ("Meta voor ontwikkelaars: aangepaste doelgroepen en de Meta Pixel", "https://developers.facebook.com/docs/meta-pixel/implementation/custom-audiences", "Bezoekers indelen in groepen op basis van gedrag op de site."),
   ]),
 ]),
},

# ─────────── GIDS: BEDRIJFSPROCESSEN AUTOMATISEREN — VOORBEELDEN ───────────
{
 "bestand": "bedrijfsprocessen-automatiseren-voorbeelden.html",
 "soort": "gids",
 "dienst": "Processen automatiseren: voorbeelden",
 "titel": "Processen automatiseren: voorbeelden & aanpak | Complete AI",
 "beschrijving": "Welke processen u kunt automatiseren, per afdeling: wat er nu met de hand gebeurt, wat de automatisering overneemt en hoe u kiest waar u begint.",
 "omschrijving": "Overzicht van processen die zich lenen voor automatisering in een mkb-bedrijf, per afdeling, met per proces wat er nu met de hand gebeurt en wat de automatisering overneemt.",
 "ogen": "Gids",
 "h1": 'Processen automatiseren: <span class="glans">welke processen lenen zich ervoor</span>?',
 "lead": """Processen automatiseren kan bij elk proces dat terugkomt, een vaste volgorde heeft en een uitkomst geeft die u kunt controleren, zoals een offerte opvolgen of een factuur versturen. In een mkb-bedrijf zijn dat de processen rond klanten, planning, geld, personeel, voorraad en cijfers, hieronder per afdeling uitgewerkt. Welke onderdelen Complete AI voor uw situatie inricht, volgt uit de intake: <a href="automatisering.html">zo werkt bedrijfsprocessen automatiseren bij ons</a>.""",
 "levertijd": "Leestijd ongeveer 17 minuten",
 "gepubliceerd": "2026-09-24",
 "gewijzigd": "2026-09-24",
 "uitkomsten": [
     ("8", "afdelingen, met per proces wat er nu met de hand gebeurt en wat de automatisering overneemt"),
     ("3", "kenmerken van een proces dat zich leent: herhaling, vaste volgorde, meetbare uitkomst"),
     ("1", "proces tegelijk: zo blijft zichtbaar wat elke stap oplevert"),
 ],
 "slot_kop": "Welke processen kosten bij u de meeste tijd?",
 "slot_tekst": "In een half uur brengen wij in kaart welke processen bij u het meest terugkomen en welke daarvan zich lenen voor automatisering. U ontvangt een onderbouwd advies, ook wanneer de conclusie is dat er weinig te winnen valt.",
 "vragen": [
   ("Wat zijn voorbeelden van bedrijfsprocessen?",
    """Een offerte opvolgen, een afspraak inplannen, een factuur versturen, een bestelling bij een leverancier plaatsen, verlof aanvragen en uren registreren zijn voorbeelden. Elk begint met een aanleiding, volgt vaste stappen en eindigt in een uitkomst. Acht afdelingen, met per proces wat er nu met de hand gebeurt, staan <a href="#klanten-verkoop">hierboven</a>."""),
   ("Wat zijn de drie soorten bedrijfsprocessen?",
    """Primaire, sturende en ondersteunende processen. Primaire processen leveren wat de klant koopt, sturende processen besturen de organisatie en ondersteunende processen maken het primaire proces mogelijk, zoals administratie, personeelszaken en inkoop. Deze indeling staat in de beschrijving van het begrip bedrijfsproces op Wikipedia; zie <a href="#wat-is-een-bedrijfsproces">wat is een bedrijfsproces</a>."""),
   ("Wat zijn de 4 belangrijkste kenmerken van processen?",
    """Een proces heeft een aanleiding, een reeks stappen in een vaste volgorde, een uitkomst en iemand die het uitvoert of ervoor verantwoordelijk is. Voor automatisering telt daarnaast dat het proces terugkomt en dat u de uitkomst kunt meten. Zo herkent u <a href="#herkennen">welk proces zich leent</a>."""),
   ("Hoe kan ik processen automatiseren?",
    """Kies het proces dat wekelijks terugkomt en de meeste uren kost, beschrijf de stappen zoals ze nu verlopen en laat software de herhaalbare stappen uitvoeren. Meet vooraf en achteraf dezelfde cijfers. Laat het enkele weken draaien voordat u het volgende proces kiest. Zo blijft zichtbaar wat elke stap oplevert."""),
   ("Wat zijn AI automations?",
    """AI-automatiseringen zijn automatiseringen waarin AI een stap uitvoert, zoals het verstaan van een telefoongesprek of het indelen van een vraag, terwijl vaste regels de rest afhandelen. IBM noemt dit intelligente automatisering. Automatisering alleen voert vastgelegde stappen uit; AI verwerkt taal en variatie. In de praktijk werken ze samen."""),
   ("Wat is het verschil tussen RPA en AI?",
    """RPA bootst handelingen op een scherm na volgens regels die vastliggen: klikken, invullen, kopiëren. AI herkent patronen in gegevens, ook in tekst en spraak, en werkt met invoer die elke keer anders is. IBM omschrijft het als procesgestuurd tegenover datagestuurd. Ze vullen elkaar aan; de <a href="#regels-rpa-ai">vergelijking</a> staat hierboven."""),
   ("Hoeveel tijd kan automatisering besparen?",
    """Dat verschilt per bedrijf en per proces. Bij Aronza, het e-commercebedrijf van de oprichter van Complete AI, ging de administratie van vier tot zes uur per week naar nul. Wat u kunt verwachten, bepaalt u door vooraf een week op te nemen wat de taken kosten. Hoe dat is opgebouwd leest u in <a href="case-aronza.html">de klantcase</a>."""),
   ("Welk proces automatiseer ik als eerste?",
    """Het proces dat wekelijks terugkomt, elke keer dezelfde stappen volgt en de meeste uren kost. Bij Aronza was dat de facturatie, samen met de kosten. Een factuur of bericht dat naar een klant gaat, krijgt eerst een goedkeuringsstap. Lukt het niet om te kiezen, dan doet de <a href="index.html#contact">intake</a> dat samen met u."""),
   ("Moet ik mijn huidige systemen vervangen?",
    """Nee. Automatisering sluit aan op wat u al gebruikt: de boekhouding, de agenda, de telefonie. Wij adviseren alleen iets te vervangen wanneer het kosten veroorzaakt zonder rendement, en dan met de onderbouwing erbij. Hoe dat in een traject verloopt, staat bij <a href="automatisering.html">bedrijfsprocessen automatiseren</a>."""),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   inhoudsopgave([
       ("wat-is-een-bedrijfsproces", "Wat is een bedrijfsproces?"),
       ("klanten-verkoop", "Klanten en verkoop"),
       ("planning-agenda", "Planning en agenda"),
       ("bereikbaarheid", "Bereikbaarheid"),
       ("financien", "Financiën"),
       ("personeel", "Personeel"),
       ("voorraad-inkoop", "Voorraad en inkoop"),
       ("marketing-groei", "Marketing en groei"),
       ("rapportage-inzicht", "Rapportage en inzicht"),
       ("herkennen", "Welk proces leent zich?"),
       ("tijd-opnemen", "Vooraf de tijd opnemen"),
       ("waar-begint-u", "Waar begint u"),
       ("regels-rpa-ai", "Regels, RPA of AI"),
       ("fouten", "Veelgemaakte fouten"),
       ("eigen-praktijk", "Uit eigen praktijk"),
   ]),

   proza("Begrippen", "Wat is een bedrijfsproces?",
         """        <p>Een bedrijfsproces is een ordening van activiteiten waarmee een bedrijf een product of dienst levert die voor de klant waarde heeft. <a href="https://nl.wikipedia.org/wiki/Bedrijfsproces" rel="noopener" target="_blank">Wikipedia</a> omschrijft het ook als een keten van activiteiten die aan elkaar gekoppeld zijn en door beslissingen worden gestuurd. Een proces komt steeds terug, een project heeft een begin en een einde. Dat maakt een proces geschikt voor automatisering: wat steeds op dezelfde manier terugkomt, richt u één keer in.</p>
        <h3>Wat zijn de drie soorten bedrijfsprocessen?</h3>
        <p>Er worden drie soorten onderscheiden. In een mkb-bedrijf zijn ze goed te herkennen.</p>
        <ul>
          <li><strong>Primaire processen</strong> leveren het resultaat waarvoor de klant betaalt. Bij een garage is dat de reparatie, bij een webshop de order die wordt verzonden.</li>
          <li><strong>Sturende processen</strong>, ook managementprocessen genoemd, besturen de organisatie en haar processen: doelen stellen, cijfers bekijken, bijsturen.</li>
          <li><strong>Ondersteunende processen</strong> maken het primaire proces mogelijk: administratie, personeelszaken, inkoop en ICT.</li>
        </ul>
        <p>De voorbeelden hieronder lopen door alle drie heen. Een offerte opvolgen hoort bij het primaire proces, facturatie en personeelsbeheer zijn ondersteunend, en het weekoverzicht van uw cijfers is een stuurproces.</p>
        <h3>Wat zijn voorbeelden van bedrijfsprocessen?</h3>
        <p>Een offerte opvolgen (<a href="#klanten-verkoop">klanten en verkoop</a>), een afspraak inplannen (<a href="#planning-agenda">planning</a>), een factuur versturen en de betaling opvolgen (<a href="#financien">financiën</a>), verlof aanvragen (<a href="#personeel">personeel</a>), voorraad bijhouden en bestellen (<a href="#voorraad-inkoop">voorraad en inkoop</a>) en een weekoverzicht maken (<a href="#rapportage-inzicht">rapportage</a>). Per proces staat hieronder wat er nu met de hand gebeurt en wat de automatisering overneemt.</p>
        <h3>Wat is procesautomatisering?</h3>
        <p>Procesautomatisering is het gebruik van software om herhaalde bedrijfsprocessen uit te voeren. <a href="https://www.ibm.com/think/topics/business-process-automation" rel="noopener" target="_blank">IBM</a> onderscheidt niveaus. Taakautomatisering neemt één handeling over, zoals het versturen van een bevestiging. Workflowautomatisering laat een reeks taken in de juiste volgorde verlopen. Procesautomatisering neemt een proces van begin tot eind over. Voor een mkb-bedrijf loopt de route in die volgorde: eerst één handeling, dan de keten eromheen, dan het hele proces.</p>""",
         "wat-is-een-bedrijfsproces"),

   sectie("Klanten en verkoop", "Klanten en verkoop: van eerste contact tot ondertekende offerte.",
          "Hier komt veel terugkerend werk samen. Een reactie die blijft liggen of een offerte waar niemand op terugkomt kost hier direct een opdracht.",
          voorbeeldblok([(t, f"<strong>Nu:</strong> {n}<br><strong>Automatisering:</strong> {a}") for t, n, a in [
            ("Klantenbestand", "Gegevens staan verspreid over mailboxen, notitieboekjes en spreadsheets. Wie iets zoekt, zoekt.", "Contactgegevens, historie en notities per klant staan op één plek en worden bijgewerkt door de andere processen."),
            ("Leads volgen", "Een aanvraag komt binnen via telefoon, mail of formulier en wordt onthouden of genoteerd. Opvolging hangt af van het geheugen.", "Aanvragen uit alle kanalen komen in één lijst met een status. U ziet wie opvolging nodig heeft; blijft een reactie uit, dan volgt vanzelf een herinnering."),
            ("Offertes maken en opvolgen", "Een offerte vanaf nul typen, versturen en later onthouden wie niet heeft gereageerd.", "Een concept staat klaar met uw standaardposten. U kijkt na, past aan en verstuurt, en ziet daarna wie nog niet heeft gereageerd."),
            ("Digitale handtekening", "Een offerte of bon uitprinten, laten tekenen en weer inscannen.", "Klanten tekenen op een telefoon of tablet, zonder uitprinten."),
            ("Terugkomberichten", "U onthoudt zelf wanneer een klant weer aan de beurt is, of vergeet het.", "Een bericht zodra het tijd is voor een nieuwe afspraak: omzet zonder dat u hoeft te bellen."),
            ("Klantportaal", "Klanten bellen of mailen om te vragen hoe het met hun opdracht staat.", "Klanten loggen zelf in en zien hun gegevens en de status van hun opdracht."),
          ]]) + """
      <div class="proza reveal">
        <div class="noot"><p><strong>Blijft bij u:</strong> de prijs van een offerte, het gesprek met een twijfelende klant en de afweging of een opdracht de moeite waard is.</p></div>
      </div>""", "klanten-verkoop"),

   sectie("Planning en agenda", "Planning en agenda: afspraken, uren en klussen zonder heen-en-weer bellen.",
          "Planning is een terugkerend proces bij uitstek: dezelfde stappen, elke dag opnieuw.",
          voorbeeldblok([(t, f"<strong>Nu:</strong> {n}<br><strong>Automatisering:</strong> {a}") for t, n, a in [
            ("Online boeken", "Heen en weer bellen of appen om een moment te vinden.", "Klanten kiezen zelf een vrij moment via een link. De afspraak staat direct in uw agenda."),
            ("Afspraakherinneringen", "U belt vooraf om te bevestigen, of het gebeurt niet en de klant komt niet.", "Vóór de afspraak gaat automatisch een bericht uit, zodat niemand de afspraak vergeet."),
            ("Wachtlijst opvullen", "Bij een afzegging belt u de lijst na, of de plek blijft leeg.", "Een vrijgekomen plek wordt automatisch aangeboden aan klanten op de wachtlijst."),
            ("Digitale werkbonnen", "Uren, materiaal en handtekening staan op papier en worden &#8217;s avonds overgetypt.", "Uren, materiaal, foto&#8217;s en handtekening worden ter plekke op de telefoon ingevuld."),
            ("Klus- en routeplanning", "De dag staat in uw hoofd of op een briefje, en informatie gaat telefonisch heen en weer.", "Klussen zijn per dag en adres ingepland, met alle informatie op de telefoon."),
            ("Urenregistratie en rooster", "Uren worden achteraf gereconstrueerd en het rooster staat in een spreadsheet.", "Gewerkte uren worden per klant of project vastgelegd en diensten voor medewerkers ingepland."),
          ]]) + """
      <div class="proza reveal">
        <div class="noot"><p><strong>Blijft bij u:</strong> de afweging welke klus voorgaat wanneer de planning krap is.</p></div>
      </div>""", "planning-agenda"),

   sectie("Bereikbaarheid en communicatie", "Bereikbaarheid: elke vraag krijgt een antwoord, ook wanneer u niet kunt opnemen.",
          "Een gemist telefoontje is een klant die de volgende belt. Dit zijn de processen die dat voorkomen.",
          voorbeeldblok([(t, f"<strong>Nu:</strong> {n}<br><strong>Automatisering:</strong> {a}") for t, n, a in [
            ("AI-telefonist", "Opnemen onderbreekt het werk. Na sluitingstijd of tijdens drukte blijft de telefoon onbeantwoord.", """Neemt op buiten openingstijden en tijdens drukte, noteert de vraag of de bestelling en schakelt urgente gesprekken door. <a href="ai-telefonist.html">Alles over de AI-telefonist</a>."""),
            ("WhatsApp-assistent", "Dezelfde vraag over openingstijden of levering wordt telkens opnieuw beantwoord.", "Veelgestelde vragen krijgen automatisch antwoord, ook buiten openingstijden."),
            ("Terugbelverzoeken", "Gemiste oproepen staan in een belgeschiedenis of op een briefje.", "Gemiste oproepen worden geordende terugbelverzoeken in één lijst."),
            ("Vragenassistent op uw website", "Een bezoeker met een vraag mailt of belt en wacht op antwoord.", "Veelgestelde vragen op de site worden direct beantwoord, zonder dat u erbij hoeft te zijn."),
          ]]) + """
      <div class="proza reveal">
        <div class="noot"><p><strong>Blijft bij u:</strong> gesprekken die persoonlijk contact vragen. Wat als urgent geldt, bepaalt u vooraf; die gesprekken schakelt de telefonist naar u door.</p></div>
      </div>""", "bereikbaarheid"),

   sectie("Financiën", "Financiën: facturen, kosten en btw zonder inhaalslag.",
          "De administratie die naar de avond schuift. Bij Aronza ging het om vier tot zes uur per week.",
          voorbeeldblok([(t, f"<strong>Nu:</strong> {n}<br><strong>Automatisering:</strong> {a}") for t, n, a in [
            ("Facturatie en betaalherinneringen", "Na afronding een factuur opstellen en versturen, daarna nalopen wie heeft betaald en een herinnering schrijven die ongemakkelijk voelt.", "De factuur volgt uit de order of werkorder en wordt verstuurd. Trage betalers krijgen een herinnering die oploopt."),
            ("Kosten en uitgaven", "Bonnen en rekeningen verzamelen en achteraf indelen.", "Alle uitgaven staan op één plek, per categorie geordend."),
            ("Bonnetjes fotograferen", "Het bonnetje gaat in een la en wordt later overgetypt.", "Een foto van het bonnetje en de uitgave staat in de administratie."),
            ("Btw-overzicht", "Aan het einde van het kwartaal de cijfers bij elkaar zoeken.", "De btw per kwartaal staat klaar voor de aangifte."),
            ("Betaallinks en aanbetalingen", "De klant maakt over en u controleert het bankafschrift.", "Klanten rekenen direct online af, of betalen vooraf een deel."),
            ("Winst, verlies en kasstroom", "Pas na de kwartaalafsluiting is duidelijk wat er overblijft.", "U ziet doorlopend wat er overblijft en of de komende maanden krap worden."),
          ]]) + """
      <div class="proza reveal">
        <div class="noot"><p><strong>Blijft bij u:</strong> het akkoord op een factuur die afwijkt van het gebruikelijke, zoals een korting of een deelbetaling.</p></div>
      </div>""", "financien"),

   sectie("Personeel", "Personeel: verlof, contracten en nieuwe collega&#8217;s zonder papierwerk.",
          "Zodra er meer dan één medewerker is, komt hier terugkerend werk vrij.",
          voorbeeldblok([(t, f"<strong>Nu:</strong> {n}<br><strong>Automatisering:</strong> {a}") for t, n, a in [
            ("Medewerkersbeheer", "Contracten liggen in een map, gegevens staan in een spreadsheet en documenten zitten in mailboxen.", "Gegevens, contracten en documenten per medewerker staan op één plek."),
            ("Verlof en ziekte", "Aanvragen komen per mail of app binnen en iemand houdt het saldo bij.", "Aanvragen, goedkeuren en het saldo bijhouden verlopen zonder mailwisseling."),
            ("Onboarding-checklists", "Bij elke nieuwe collega opnieuw bedenken wat er geregeld moet worden.", "Vaste stappen voor een nieuwe medewerker, elke keer hetzelfde en niets vergeten."),
          ]]) + """
      <div class="proza reveal">
        <div class="noot"><p><strong>Blijft bij u:</strong> de beoordeling van medewerkers, de gesprekken en de beslissingen over een contract.</p></div>
      </div>""", "personeel"),

   sectie("Voorraad en inkoop", "Voorraad en inkoop: weten wat er ligt en op tijd bestellen.",
          "Voor bedrijven met producten is dit het proces waar een tekort direct omzet kost. Bij Aronza bewegen de voorraadstanden mee met wat er verkocht en ingekocht wordt.",
          voorbeeldblok([(t, f"<strong>Nu:</strong> {n}<br><strong>Automatisering:</strong> {a}") for t, n, a in [
            ("Voorraadbeheer met seintje", "Voorraad tellen of schatten, en merken dat iets op is wanneer een klant erom vraagt.", "Altijd zicht op de voorraad, met een melding wanneer iets bijna op is."),
            ("Leveranciers en bestellingen", "Bestellingen per mail of telefoon, zonder overzicht van wat er onderweg is.", "Alle leveranciers en bestellingen staan overzichtelijk op één plek."),
            ("Scannen met de telefoon", "Aantallen op papier noteren en later invoeren.", "De voorraad wordt bijgewerkt door producten te scannen."),
            ("Houdbaarheid bewaken", "Datums controleren door langs de schappen te lopen.", "Een waarschuwing wanneer producten bijna over de datum zijn."),
          ]]) + """
      <div class="proza reveal">
        <div class="noot"><p><strong>Blijft bij u:</strong> de keuze wat u inkoopt, bij wie en in welke hoeveelheid.</p></div>
      </div>""", "voorraad-inkoop"),

   sectie("Marketing en groei", "Marketing en groei: zichtbaar blijven zonder er elke week aan te denken.",
          "Werk dat helpt om gevonden te worden en toch blijft liggen omdat er nooit een moment voor is.",
          voorbeeldblok([(t, f"<strong>Nu:</strong> {n}<br><strong>Automatisering:</strong> {a}") for t, n, a in [
            ("Beoordelingen verzamelen", "U weet dat beoordelingen helpen, maar erom vragen gebeurt niet in een drukke week.", "Na een geslaagde levering wordt automatisch om een beoordeling gevraagd en wordt die op de site getoond."),
            ("Social media vooruit plannen", "Er wordt gepost als er tijd is, en daarna weken niet.", """Berichten voor Facebook en Instagram worden vooraf ingepland. <a href="social-media.html">Meer over social media</a>."""),
            ("Nieuwsbrief en acties", "Een actie bedenken en de klantenlijst handmatig mailen, als het er van komt.", "Nieuwsbrieven en acties gaan op vaste momenten naar uw eigen klantenlijst."),
            ("Google-bedrijfsprofiel bijhouden", "Openingstijden en foto&#8217;s raken verouderd omdat niemand het profiel aanraakt.", """Openingstijden, foto&#8217;s en berichten op Google blijven actueel. <a href="vindbaarheid-seo.html">Meer over vindbaarheid</a>."""),
            ("Websitestatistieken", "Niemand weet hoeveel mensen de site bezoeken.", "U ziet hoeveel mensen de site bezoeken en wat ze daar doen."),
          ]]) + """
      <div class="proza reveal">
        <div class="noot"><p><strong>Blijft bij u:</strong> wat u aanbiedt, en het akkoord op wat er naar buiten gaat.</p></div>
      </div>""", "marketing-groei"),

   sectie("Rapportage en inzicht", "Rapportage: beslissen op cijfers in plaats van op gevoel.",
          "De cijfers zijn er al. Het gaat erom dat ze zonder zoeken op één plek staan.",
          voorbeeldblok([(t, f"<strong>Nu:</strong> {n}<br><strong>Automatisering:</strong> {a}") for t, n, a in [
            ("Omzetdashboard", "Omzet uit facturen optellen in een spreadsheet.", "Omzet per dag, week of maand in duidelijke grafieken."),
            ("Kerncijfers op één scherm", "Meerdere programma&#8217;s openen om de cijfers bij elkaar te zoeken.", "De belangrijkste cijfers van uw zaak staan op één scherm, zonder een rapport te openen."),
            ("Seintjes bij afwijkingen", "Een afwijking valt pas op bij de kwartaalcijfers.", "Een melding wanneer er iets opvalt in uw cijfers."),
            ("Weekoverzicht", "Een overzicht maken kost tijd en gebeurt niet elke week.", "Elke week vanzelf een kort overzicht van hoe de zaak draaide."),
            ("Export naar Excel, pdf of boekhouder", "Gegevens kopiëren, opmaken en doormailen.", "Gegevens gaan met één handeling naar Excel, pdf of uw boekhouder."),
          ]]) + """
      <div class="proza reveal">
        <div class="noot"><p><strong>Blijft bij u:</strong> de conclusies die u aan de cijfers verbindt.</p></div>
      </div>""", "rapportage-inzicht"),

   proza("Herkennen", "Hoe herkent u een proces dat zich leent voor automatisering?",
         """        <p>Drie kenmerken zijn genoeg om een proces te beoordelen. Volgens <a href="https://www.ibm.com/think/topics/business-process-automation" rel="noopener" target="_blank">IBM</a> zijn processen met herhaalde taken, een hoog volume en meerdere betrokkenen goede kandidaten. Voor een mkb-bedrijf komt dat neer op deze drie vragen.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Teken</th><th>Past</th><th>Past niet</th></tr></thead>
          <tbody>
            <tr><td><strong>Herhaling.</strong> Komt het wekelijks of vaker terug?</td><td>Een factuur na elke afgeronde klus.</td><td>Eén keer per jaar de verzekeringen vergelijken.</td></tr>
            <tr><td><strong>Vaste volgorde.</strong> Zijn de stappen elke keer dezelfde?</td><td>Order binnen, voorraad bij, factuur uit.</td><td>Een klacht waarbij u elke keer opnieuw afweegt wat te doen.</td></tr>
            <tr><td><strong>Meetbare uitkomst.</strong> Ziet u wanneer het klaar is en of het klopt?</td><td>Factuur verstuurd en betaald.</td><td>&#8220;Beter contact met klanten&#8221;: daar is geen einde aan te zien.</td></tr>
          </tbody>
        </table></div>
        <h3>Welke situaties wijzen op zo&#8217;n proces?</h3>
        <p>Herkent u een van deze vier situaties, dan zit er waarschijnlijk een proces achter dat zich leent:</p>
        <ul>
          <li>De administratie schuift naar de avond, elke week opnieuw.</li>
          <li>Een herinnering aan een klant wordt uitgesteld omdat het ongemakkelijk voelt.</li>
          <li>Aanvragen komen via meerdere kanalen binnen en niemand heeft het overzicht.</li>
          <li>Dezelfde gegevens worden op twee plekken ingetypt. Overtypen is waar fouten ontstaan.</li>
        </ul>""",
         "herkennen"),

   proza("Meten", "Hoe neemt u vooraf de tijd op?",
         """        <p>Zonder meting weet u achteraf niet wat de automatisering heeft opgeleverd. Volgens <a href="https://www.ibm.com/think/topics/business-process-automation" rel="noopener" target="_blank">IBM</a> stelt u per proces meetbare doelen, zoals een kortere doorlooptijd of minder fouten. Zo neemt u de tijd op in één gewone werkweek.</p>
        <ol>
          <li><strong>Kies een normale week.</strong> Niet de week van de btw-aangifte en niet de vakantieweek.</li>
          <li><strong>Noteer elke terugkerende handeling</strong> zodra u eraan begint en zodra u klaar bent. Een notitie op uw telefoon of een lijstje naast het toetsenbord volstaat.</li>
          <li><strong>Reken uit wat het per week kost.</strong> Aantal keer per week maal minuten per keer, gedeeld door zestig, geeft uren per week.</li>
          <li><strong>Tel de wachttijd mee.</strong> Een offerte die drie dagen blijft liggen kost geen minuten, maar wel een opdracht.</li>
          <li><strong>Sorteer op uren.</strong> De taken bovenaan zijn uw kandidaten. Leg ze naast de drie vragen bij <a href="#waar-begint-u">waar begint u</a>.</li>
          <li><strong>Meet na enkele weken hetzelfde, op dezelfde manier.</strong> Alleen dan is het verschil te zien.</li>
        </ol>
        <h3>Wat noteert u per handeling?</h3>
        <div class="tabelwrap"><table>
          <thead><tr><th>Kolom</th><th>Wat u invult, en waarom</th></tr></thead>
          <tbody>
            <tr><td><strong>Taak</strong></td><td>De handeling in gewone woorden, zoals &#8220;factuur maken na een afgeronde klus&#8221;. Zo zijn gelijke taken later te groeperen.</td></tr>
            <tr><td><strong>Keer per week</strong></td><td>Hoe vaak u de handeling doet. Herhaling bepaalt of automatiseren loont.</td></tr>
            <tr><td><strong>Minuten per keer</strong></td><td>Van begin tot eind, inclusief zoeken naar gegevens. Zoeken telt mee als werktijd.</td></tr>
            <tr><td><strong>Systeem of plek</strong></td><td>Boekhouding, agenda, WhatsApp, papier, spreadsheet. Zo ziet u waar u overtypt.</td></tr>
            <tr><td><strong>Wat ging er mis</strong></td><td>Een fout, iets vergeten, te laat. Fouten en vertraging horen bij wat het proces kost.</td></tr>
          </tbody>
        </table></div>
        <p>Bij Aronza kostte de administratie vier tot zes uur per week. Dat getal is het vertrekpunt van de <a href="case-aronza.html">klantcase</a>.</p>""",
         "tijd-opnemen"),

   sectie("Waar begint u", "Drie vragen bepalen welk proces het eerst aan de beurt is.",
          "Alles tegelijk automatiseren maakt onzichtbaar wat elke stap oplevert. Zet de kandidaten uit uw meting naast deze vragen en begin bij het proces dat op alle drie een goed antwoord heeft.",
          routeblok([
            ("Hoe vaak komt het terug?", "Een proces dat wekelijks terugkomt verdient zich sneller terug dan een proces dat één keer per jaar voorkomt."),
            ("Is de volgorde steeds hetzelfde?", "Hoe vaster de stappen, hoe betrouwbaarder de automatisering. Werk dat elke keer een afweging vraagt, laat u bij uzelf."),
            ("Wat gebeurt er als het fout gaat?", "Bij een factuur of bericht dat naar een klant gaat, komt eerst een goedkeuringsstap. Die kan later vervallen."),
          ]), "waar-begint-u"),

   proza("Techniek", "Processen automatiseren met AI, RPA of vaste regels: wat past waar?",
         """        <p>Drie begrippen komen door elkaar voor als het over automatiseren gaat. Ze beschrijven verschillende manieren om een stap over te nemen, en ze sluiten elkaar niet uit.</p>
        <div class="tabelwrap"><table>
          <thead><tr><th>Aanpak</th><th>Zo werkt het en waar het bij past</th></tr></thead>
          <tbody>
            <tr><td><strong>Vaste regel of koppeling</strong></td><td>Voert een afgesproken reeks stappen uit zodra er iets gebeurt. Dezelfde invoer geeft dezelfde uitkomst.<br><strong>Past bij</strong> werk waarvan de regels vaststaan: een factuur na een afgeronde order, een herinnering bij een openstaande betaling.</td></tr>
            <tr><td><strong>RPA</strong></td><td>Een software-robot die handelingen op een scherm nabootst: klikken, invullen, kopiëren.<br><strong>Past bij</strong> gegevens overnemen tussen programma&#8217;s die niet met elkaar kunnen praten.</td></tr>
            <tr><td><strong>AI</strong></td><td>Herkent patronen in gegevens, ook in tekst en spraak, en kan invoer aan die elke keer anders is.<br><strong>Past bij</strong> werk met taal: een gesprek dat een bestelling wordt, een vraag die een antwoord nodig heeft.</td></tr>
          </tbody>
        </table></div>
        <h3>Wat is het verschil tussen RPA en AI?</h3>
        <p>RPA is volgens <a href="https://nl.wikipedia.org/wiki/Robotic_process_automation" rel="noopener" target="_blank">Wikipedia</a> een techniek om bedrijfsprocessen te automatiseren met software-robots. De robot werkt via het scherm en bootst het handmatige proces na. <a href="https://www.ibm.com/think/topics/rpa" rel="noopener" target="_blank">IBM</a>, dat zelf RPA-software levert, vat het verschil kort samen: RPA is procesgestuurd, AI is datagestuurd. Een RPA-robot volgt alleen de stappen die een gebruiker heeft vastgelegd. AI herkent patronen in gegevens, vooral in ongestructureerde gegevens zoals tekst, en leert daarvan.</p>
        <p>In de praktijk vullen ze elkaar aan. Volgens IBM helpt AI de robot om meer taken volledig te automatiseren, en zorgt RPA dat wat AI herkent sneller wordt uitgevoerd. Een gesprek verstaan is werk voor AI; de bestelling daarna in de juiste systemen zetten is werk voor regels of RPA. RPA werkt op het scherm van bestaande programma&#8217;s en kan daardoor ook wanneer er geen rechtstreekse koppeling bestaat. Een platform dat rechtstreeks met de systemen koppelt, via een API, heeft volgens <a href="https://www.ibm.com/think/topics/business-process-automation" rel="noopener" target="_blank">IBM</a> een prestatievoordeel boven traditionele RPA, omdat het scherm niet hoeft te worden nagebootst.</p>
        <h3>Wat zijn AI automations?</h3>
        <p>Met AI-automatiseringen bedoelen we automatiseringen waarin AI één of meer stappen uitvoert, vooral het lezen, indelen of beantwoorden van taal, terwijl vaste regels de rest afhandelen. <a href="https://www.ibm.com/think/topics/business-process-automation" rel="noopener" target="_blank">IBM</a> noemt de combinatie van taak- en procesautomatisering met AI intelligente automatisering, bijvoorbeeld om tekst te interpreteren. Een voorbeeld uit onze eigen praktijk is de <a href="ai-telefonist.html">AI-telefonist</a>: AI verstaat het gesprek, de bestelling gaat daarna gestructureerd de orderlijst in.</p>
        <h3>Wat gebruiken Nederlandse bedrijven?</h3>
        <p>Volgens voorlopige cijfers van het <a href="https://www.cbs.nl/nl-nl/nieuws/2025/50/bedrijven-gebruiken-ai-vaakst-voor-marketing-of-verkoop" rel="noopener" target="_blank">CBS</a> gebruikte in 2025 17 procent van de bedrijven met twee of meer werkzame personen AI, tegen 8 procent in 2023. Bij bedrijven met 2 tot 10 werkzame personen was dat 14 procent, bij bedrijven met 10 tot 50 werkzame personen 27 procent. Van de bedrijven die AI gebruiken, zet 35 procent het in voor marketing of verkoop en 32 procent voor bedrijfsadministratie of bestuurstaken. Robotgestuurde procesautomatisering gebruikte 3 procent van de bedrijven.</p>
        <h3>Zelf doen, standaardsoftware of laten inrichten?</h3>
        <p>IBM adviseert waar het kan bestaande, kant-en-klare oplossingen te gebruiken, omdat die de invoering versnellen en de kosten drukken. Voor een mkb-bedrijf zijn er drie routes. U bouwt zelf met losse hulpmiddelen, wat past bij één afgebakende stap maar u tot de schakel tussen de systemen maakt. U gebruikt de automatisering die in uw boekhoud- of agendapakket zit, wat werkt voor wat dat pakket zelf doet. Of u laat onderdelen inrichten die al draaien en aan uw pakketten zijn gekoppeld. Het laatste is wat Complete AI doet, en daarom staat het binnen enkele werkdagen.</p>
        <div class="noot"><p><strong>Vuistregel:</strong> een vaste regel waar de uitkomst vaststaat, RPA waar twee programma&#8217;s niet met elkaar kunnen praten, en AI waar taal en variatie een rol spelen. De eenvoudigste aanpak die betrouwbaar werkt, verdient de voorkeur, omdat die het best te controleren is. Hoe AI in een klein bedrijf verder wordt ingezet, leest u in <a href="ai-voor-uw-bedrijf.html">AI in uw bedrijf</a>.</p></div>""",
         "regels-rpa-ai"),

   proza("Valkuilen", "Wat zijn veelgemaakte fouten bij de start?",
         """        <p>Negen fouten zijn te voorkomen door vooraf te kiezen.</p>
        <ol>
          <li><strong>Alles tegelijk willen automatiseren.</strong> Dan is niets af en ziet niemand wat wat oplevert. IBM adviseert bedrijven met weinig automatisering klein te beginnen, bij processen die vaart geven. Kies één proces, laat het enkele weken draaien en kies dan het volgende.</li>
          <li><strong>Beginnen bij de techniek.</strong> &#8220;We moeten iets met AI&#8221; is geen proces. Begin bij het knelpunt: welk werk kost de meeste uren?</li>
          <li><strong>Een proces automatiseren dat niemand kan uitleggen.</strong> Leg eerst vast welke taken erbij horen, wie verantwoordelijk is, wanneer een stap klaar is en wat er gebeurt als iets niet past, zoals een klant zonder e-mailadres of een order zonder voorraad. IBM noemt onvoldoende procesdocumentatie een obstakel bij procesautomatisering.</li>
          <li><strong>Zonder meting beginnen.</strong> Neem vooraf de tijd op, zoals hierboven beschreven, anders is de winst achteraf niet aan te tonen.</li>
          <li><strong>Geen goedkeuringsstap bij wat naar klanten gaat.</strong> Een factuur of bericht dat is verstuurd, haalt u niet terug. Laat de eerste weken alles eerst langs u gaan.</li>
          <li><strong>Slechte gegevens meenemen.</strong> Een dubbel klantenbestand blijft dubbel: automatisering geeft de fout sneller door. Ruim de gegevens op voordat u koppelt.</li>
          <li><strong>Medewerkers niet betrekken.</strong> Wie het werk nu doet, kent de uitzonderingen die op geen tekening staan. Laat hen de meetlijst invullen en het resultaat beoordelen. IBM noemt het betrekken van belanghebbenden en het opleiden van medewerkers als voorwaarden voor succes.</li>
          <li><strong>De gegevensregeling pas achteraf treffen.</strong> Zodra persoonsgegevens door de automatisering lopen, hoort er een verwerkersovereenkomst bij. Wat daarin staat, leest u bij <a href="automatisering.html#gegevens">veiligheid en gegevens</a>.</li>
          <li><strong>Na de start niet meekijken.</strong> De eerste weken laten zien wat de praktijk anders doet dan de tekening. Kijk mee en stuur bij.</li>
        </ol>""",
         "fouten"),

   sectie("Uit eigen praktijk", "Vijf processen als één keten, in een bedrijf dat dagelijks draait.",
          """Bij Aronza, het e-commercebedrijf van de oprichter van Complete AI, zit de winst niet in vijf losse hulpmiddelen naast elkaar. Facturatie, kostenregistratie, orderverwerking, voorraadbeheer en klantcontact werken op dezelfde gegevens en draaien sinds begin mei 2026. <a href="case-aronza.html">De volledige klantcase leest u hier</a>.""",
          voorbeeldblok([
            ("Eén order, drie bijwerkingen", "Een binnenkomende order raakt de voorraad, de factuur en het klantdossier zonder dat er iets wordt overgetypt."),
            ("Overtypen is waar fouten ontstaan", "Door één keten te gebruiken verdwijnt die overdracht, en daarmee de fout."),
            ("Groei kost geen extra uren", "Meer orders betekenden voorheen meer administratie. Die koppeling is doorbroken."),
            ("Van vier tot zes uur naar nul", "De administratie kostte vier tot zes uur per week, buiten werktijd. Sinds de ingebruikname begin mei 2026 is dat nul."),
            ("Begonnen bij facturatie en kosten", "De onderdelen zijn gefaseerd in gebruik genomen, te beginnen bij facturatie en kosten. Zo is bij elke stap te zien of het klopt."),
          ]), "eigen-praktijk"),

   bronnen([
       ("Wikipedia: Bedrijfsproces",
        "https://nl.wikipedia.org/wiki/Bedrijfsproces",
        "Definitie van een bedrijfsproces, het verschil met een project en de indeling in primaire, sturende en ondersteunende processen."),
       ("Wikipedia: Robotgestuurde procesautomatisering",
        "https://nl.wikipedia.org/wiki/Robotic_process_automation",
        "Omschrijving van RPA als automatiseren via de gebruikersinterface, door het handmatige proces na te bootsen."),
       ("IBM: What is business process automation? (Engelstalig)",
        "https://www.ibm.com/think/topics/business-process-automation",
        "Definitie en niveaus van procesautomatisering, kenmerken van goede kandidaten, meetbare doelen en het advies klein te beginnen."),
       ("IBM: What is robotic process automation? (Engelstalig)",
        "https://www.ibm.com/think/topics/rpa",
        "Het verschil tussen RPA (procesgestuurd) en AI (datagestuurd), en hoe ze elkaar aanvullen."),
       ("CBS: Bedrijven gebruiken AI vaakst voor marketing of verkoop",
        "https://www.cbs.nl/nl-nl/nieuws/2025/50/bedrijven-gebruiken-ai-vaakst-voor-marketing-of-verkoop",
        "Voorlopige cijfers over het gebruik van AI door Nederlandse bedrijven in 2025, naar bedrijfsgrootte en doel."),
   ]),
 ]),
},
]
