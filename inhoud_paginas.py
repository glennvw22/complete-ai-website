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


# ══════════════════════════════════════════════════════════════════
PAGINAS = [

# ─────────────────────────────── WEBSITES ───────────────────────────────
{
 "bestand": "websites.html",
 "dienst": "Websites",
 "titel": "Website laten maken — live in 1 tot 2 weken | Complete AI",
 "beschrijving": "Een website die klanten oplevert in plaats van er alleen goed uitziet. Snel, mobielvriendelijk, gebouwd om gevonden te worden. Live binnen één tot twee weken.",
 "omschrijving": "Websites op maat voor lokale ondernemers: ontwerp, teksten, techniek, vindbaarheid en hosting. Live binnen één tot twee weken.",
 "ogen": "Websites",
 "h1": 'Een website die <span class="glans">klanten oplevert</span>, niet alleen indruk maakt.',
 "lead": "Veel bedrijfssites zien er verzorgd uit en leveren niets op. Ze staan online, worden niet gevonden, en er komt geen aanvraag uit. Complete AI bouwt sites die wél resultaat opleveren, met een doorlooptijd van één tot twee weken in plaats van twee maanden.",
 "levertijd": "Live in 1 tot 2 weken",
 "uitkomsten": [
     ("0,7 s", "laadtijd van deze pagina — dezelfde norm geldt voor uw site"),
     ("83%", "van de bezoekers komt binnen op een telefoon; daar ontwerpen we als eerste voor"),
     ("1–2 wk", "van akkoord tot live, inclusief teksten en beeld"),
 ],
 "slot_kop": "Wat uw huidige website kan opleveren.",
 "slot_tekst": "In een half uur nemen we door wat er nu staat, wie uw klanten zijn en waar het misloopt. U ontvangt een onderbouwd advies — ook wanneer de conclusie is dat de site voldoet en de winst elders ligt.",
 "vragen": [
   ("Moet ik van mijn huidige website af?",
    "Niet per se. Regelmatig voldoet een bestaande site prima en ligt de winst elders: in vindbaarheid, of in het automatiseren van de administratie. Dat hoort u in de nulmeting, ook wanneer de conclusie is dat u niets bij Complete AI hoeft af te nemen."),
   ("Ik heb geen teksten en geen goede foto's. Is dat een probleem?",
    "Nee, dat is eerder regel dan uitzondering. De teksten schrijven wij op basis van één gesprek waarin we doorvragen op wat u doet en voor wie. Voor beeldmateriaal werken we met wat er is, aangevuld met professionele beelden; is fotografie nodig, dan hoort u dat vooraf."),
   ("Kan ik later zelf wijzigingen doorvoeren?",
    "Ja. Kleine wijzigingen — een tekst, een prijs, openingstijden — vallen onder het onderhoud: één bericht en het is dezelfde dag geregeld. Wilt u het liever zelf doen, dan richten wij dat zo in dat het zonder technische kennis kan."),
   ("Hoe zit het met hosting en onderhoud?",
    "Dat valt onder het maandbedrag: hosting, back-ups, updates, het SSL-certificaat en kleine wijzigingen. Geen losse facturen van drie partijen. Maandelijks opzegbaar."),
   ("Waarom duurt het hier twee weken en elders twee maanden?",
    "Omdat er geen accountmanager, projectleider of tussenlaag tussen zit: u spreekt de persoon die het bouwt. En omdat een groot deel van wat wij inzetten al gebouwd en getest is; wij beginnen zelden bij nul."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("De situatie", "Representatief zijn en resultaat opleveren zijn twee verschillende zaken.",
          "Dit zijn de vier bevindingen die wij het vaakst doen bij een bestaande site.",
          pijnblok([
            ("Niet vindbaar", "De site staat online, maar wie niet de bedrijfsnaam intypt komt hem nooit tegen."),
            ("Trage laadtijd op mobiel", "Waar het overgrote deel van de bezoekers vandaan komt. Elke extra seconde kost bezoekers."),
            ("Geen duidelijke vervolgstap", "Een bezoeker kijkt rond, vindt geen aanleiding tot contact en verlaat de site."),
            ("Wijzigingen duren te lang", "Waardoor ze uitblijven en de site geleidelijk veroudert."),
          ]), "herkenbaar"),

   sectie("Wat u krijgt", "Alles wat nodig is, in één keer geregeld.",
          "Geen losse onderdelen die u zelf moet samenbrengen. Eén aanspreekpunt, en aan het eind staat er iets dat af is.",
          krijgtblok([
            ("Ontwerp op maat", "Geen sjabloon met een logo erin. Het ontwerp volgt uw bedrijf, uw klanten en uw doelstelling."),
            ("Mobiel eerst", "Wij ontwerpen op telefoonformaat en werken omhoog naar de laptop, niet andersom. Daar zitten de bezoekers."),
            ("Snelheid als uitgangspunt", "Geen zware paginabouwers of tientallen plug-ins. Deze pagina laadt in ongeveer 0,7 seconde; dat is de norm."),
            ("Teksten die kloppen", "Geschreven op basis van één gesprek, in uw taal en gericht op de klant die u wilt bereiken."),
            ("Vindbaar vanaf dag één", "Correcte structuur, sitemap, structuurdata en een volledig ingericht Google-bedrijfsprofiel."),
            ("Formulier dat aankomt", "Vanzelfsprekend in theorie. In de praktijk de meest voorkomende fout op bestaande sites."),
            ("Veilig en zonder waarschuwingen", "HTTPS met een certificaat dat zichzelf verlengt, geen database en geen inlogscherm — er is dus geen aanvalsoppervlak."),
            ("Hosting en onderhoud", "Inbegrepen in het maandbedrag, evenals kleine wijzigingen. Maandelijks opzegbaar."),
          ]), "wat-u-krijgt"),

   sectie("Werkwijze", "Van eerste gesprek tot oplevering in vier stappen.",
          "Voorbereiding is niet nodig. Het enige wat wij vragen is een half uur en een open beeld van hoe het nu loopt.",
          routeblok([
            ("Nulmeting", "Een half uur om vast te stellen wat er nu staat, wie de klanten zijn en waar het misloopt. Kosteloos en vrijblijvend."),
            ("Voorstel", "Binnen één werkdag op papier: wat we bouwen, wat het kost en wanneer het staat. Eén vaste prijs."),
            ("Bouwen", "Na enkele dagen ontvangt u een link om mee te kijken. Aanpassingen verwerken we gaandeweg, niet pas bij oplevering."),
            ("Oplevering", "Wij zetten de site live, koppelen domein en e-mail, en nemen alles met u door tot u ermee overweg kunt."),
          ]), "werkwijze"),

   sectie("Bewijs", "Deze pagina is zelf het bewijs.",
          "U hoeft niets op ons woord aan te nemen; u kijkt er op dit moment naar.",
          eerlijkblok(
            "Wat u hier zelf kunt controleren",
            "Alles wat hierboven staat, is op deze pagina zelf te controleren:",
            ["De pagina laadt in ongeveer <strong>0,7 seconde</strong>, ook op een telefoon.",
             "Er is <strong>geen cookiebanner</strong>, omdat er geen tracking op staat die gedrag volgt.",
             "Het certificaat in de adresbalk is <strong>geldig</strong> — geen browserwaarschuwingen.",
             "Verklein dit venster tot telefoonformaat: de pagina blijft leesbaar en bruikbaar.",
             "Deze site is <strong>binnen één etmaal gebouwd</strong>. Voor een opdracht nemen wij meer tijd, maar het illustreert waar het tempo vandaan komt."]),
          "bewijs"),
 ]),
},

# ───────────────────────────── AUTOMATISERING ─────────────────────────────
{
 "bestand": "automatisering.html",
 "dienst": "Automatisering",
 "titel": "Bedrijfsprocessen automatiseren — live in enkele werkdagen | Complete AI",
 "beschrijving": "Facturen, orders, herinneringen en reviews die zonder tussenkomst verlopen. Een groot deel van wat wij inzetten draait al, waardoor het vaak binnen enkele werkdagen operationeel is.",
 "omschrijving": "Automatisering van terugkerend werk voor lokale ondernemers: orderintake, facturatie, betaalherinneringen, afspraken, reviews en een dashboard met uw cijfers.",
 "ogen": "Automatisering",
 "h1": 'Terugkerend werk dat <span class="glans">zichzelf afhandelt</span>.',
 "lead": "Facturen opstellen, bevestigingen versturen, betalingen opvolgen, reviews aanvragen. Werk dat moet gebeuren maar geen omzet oplevert. Dat kan geautomatiseerd worden — en omdat een groot deel van wat wij inzetten al operationeel is, staat het vaak binnen enkele werkdagen.",
 "levertijd": "Vaak live binnen enkele werkdagen",
 "uitkomsten": [
     ("17", "automatiseringen die vandaag al draaien en getest zijn"),
     ("Dagen", "in plaats van maanden, omdat wij zelden bij nul beginnen"),
     ("0", "handelingen van uw kant zodra het draait"),
 ],
 "slot_kop": "Waar gaat uw tijd naartoe?",
 "slot_tekst": "In een half uur brengen wij in kaart waar de week in gaat zitten. Meestal blijken drie terugkerende taken het grootste deel op te eisen. Daar beginnen we; de rest volgt wanneer u dat wilt.",
 "vragen": [
   ("Moet ik mijn huidige systemen vervangen?",
    "Nee. In de meeste gevallen sluiten wij aan op wat er al in gebruik is: de boekhouding, de agenda, de telefonie. Adviseren wij iets te beëindigen, dan is dat omdat het kosten veroorzaakt zonder rendement — met de onderbouwing erbij."),
   ("Wat als de automatisering iets fout doet?",
    "Daarom bouwen wij in stappen en kijken we de eerste weken mee. Alles wat automatisch gebeurt is terug te zien en terug te draaien. Bij handelingen die naar buiten gaan — een factuur, een bericht aan een klant — bepaalt u of er een goedkeuringsstap tussen zit."),
   ("Hoe kan het zo snel gaan als het maatwerk betreft?",
    "Omdat de onderdelen al bestaan. Het klantenbestand, de facturatie, de agenda en het omzetdashboard zijn gebouwd, getest en draaien in productie. Wat wij doen is de juiste onderdelen kiezen, inrichten met uw gegevens en aan elkaar koppelen. Dat is een kwestie van dagen, niet van maanden."),
   ("Heb ik zelf toegang, of ben ik afhankelijk van Complete AI?",
    "U heeft zelf toegang en de gegevens blijven van u. Besluit u later te stoppen, dan ontvangt u alles in een gangbaar bestandsformaat. Complete AI werkt liever met klanten die blijven omdat het rendeert dan met klanten die vastzitten."),
   ("Hoe is dit geregeld ten aanzien van klantgegevens en de AVG?",
    "Waar wij persoonsgegevens verwerken, leggen we dat vast in een verwerkersovereenkomst zoals de wet voorschrijft — vóór de start, niet achteraf. Uw gegevens blijven van u en worden nooit gedeeld of doorverkocht."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("De situatie", "Werk dat moet gebeuren maar geen omzet oplevert.",
          "Vier situaties die wij bij vrijwel elke ondernemer terugzien.",
          pijnblok([
            ("De administratie schuift naar de avond", "Als de zaak gesloten is en de werkdag er feitelijk op zit. Elke week opnieuw."),
            ("Bestellingen komen via alle kanalen binnen", "Telefoon, WhatsApp, e-mail en eventueel de webshop. De ondernemer is de plek waar het samenkomt."),
            ("Openstaande facturen blijven liggen", "Herinneren voelt ongemakkelijk, dus het wordt uitgesteld — en het geld komt later binnen."),
            ("Reviews worden niet gevraagd", "Terwijl ze aantoonbaar helpen bij vindbaarheid en vertrouwen. Er is simpelweg geen moment voor."),
          ]), "herkenbaar"),

   sectie("Wat er kan", "Wat er vandaag al operationeel is.",
          "Dit zijn geen plannen of ontwerpen die nog gebouwd moeten worden. Dit is software die bestaat, getest is en bij klanten draait. Samen bepalen we welke onderdelen in uw situatie zinvol zijn.",
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

   sectie("Werkwijze", "We beginnen bij de drie processen die de meeste tijd kosten.",
          "Nooit alles tegelijk. Dat houdt de investering beheersbaar en maakt sneller zichtbaar of het rendeert.",
          routeblok([
            ("Nulmeting", "Een half uur om vast te stellen waar de week in gaat zitten. Meestal zijn het drie taken die het grootste deel opeisen."),
            ("Voorstel", "Welke onderdelen wij inzetten, wat het kost en wanneer het staat. Eén vaste prijs, geen nacalculatie."),
            ("Inrichten", "Wij richten de onderdelen in met uw gegevens, huisstijl en werkwijze. Dagen, geen maanden."),
            ("Nazorg", "De eerste weken kijken wij mee en sturen we bij. Daarna ziet u alleen nog het resultaat."),
          ]), "werkwijze"),

   sectie("Grenzen", "Wat het nog niet doet.",
          "Beter nu helder dan een teleurstelling achteraf.",
          eerlijkblok(
            "Drie onderdelen die een externe koppeling vereisen",
            "Deze onderdelen zijn volledig gebouwd tot aan de laatste stap. Die laatste stap vereist een account bij een externe partij; dat regelen wij in fase twee en u hoort het vooraf:",
            ["<strong>Daadwerkelijk versturen van e-mail en sms.</strong> Het bericht wordt volledig opgesteld en klaargezet; de verzending koppelen wij aan zodra de provider is ingericht.",
             "<strong>Automatisch incasseren.</strong> Betaallinks werken; automatische incasso vraagt een koppeling met Mollie of Stripe.",
             "<strong>Rechtstreekse koppeling met de boekhouding.</strong> Export naar Excel en pdf werkt vandaag; de directe koppeling met Moneybird of e-Boekhouden bouwen wij op aanvraag."]),
          "eerlijk"),
 ]),
},

# ───────────────────────────── AI-TELEFONIST ─────────────────────────────
{
 "bestand": "ai-telefonist.html",
 "dienst": "AI-telefonist",
 "titel": "AI-telefonist die 24/7 opneemt — operationeel binnen 2 weken | Complete AI",
 "beschrijving": "Een Nederlandstalige AI die de telefoon opneemt wanneer u dat niet kunt: 's avonds, in het weekend of tijdens drukte. Neemt bestellingen aan en filtert verkopers eruit.",
 "omschrijving": "Nederlandstalige AI-telefonist die gesprekken aanneemt, bestellingen noteert, vragen beantwoordt, urgente gesprekken doorschakelt en cold callers eruit filtert.",
 "ogen": "AI-telefonist",
 "h1": 'De telefoon die <span class="glans">altijd</span> wordt opgenomen.',
 "lead": "Een gemist telefoontje is geen neutrale gebeurtenis: het is een klant die de volgende belt. De AI-telefonist neemt op wanneer u dat niet kunt — 's avonds, in het weekend of tijdens drukte — noteert de bestelling en zet die gestructureerd in de orderlijst.",
 "levertijd": "Operationeel binnen 2 weken",
 "uitkomsten": [
     ("24/7", "bereikbaar, ook in het weekend en op feestdagen"),
     ("2 wk", "van akkoord tot een werkende telefonist op uw nummer"),
     ("100%", "van de gesprekken vastgelegd met een transcript"),
 ],
 "slot_kop": "Hoeveel telefoontjes blijven er nu liggen?",
 "slot_tekst": "De meeste ondernemers weten het niet, omdat een gemist telefoontje geen spoor achterlaat. In een half uur rekenen wij het door: hoe vaak gaat de telefoon op momenten dat er niemand kan opnemen, en wat vertegenwoordigt zo'n gesprek gemiddeld aan omzet.",
 "vragen": [
   ("Hoort een beller dat het geen mens is?",
    "Sommige bellers horen het, andere niet. Belangrijker is dat hij zich niet anders voordoet: hij meldt zich als de digitale assistent van het bedrijf. Dat werkt in de praktijk beter dan verhullen — bellers accepteren het zolang zij snel en correct geholpen worden."),
   ("Wat als hij een vraag niet weet?",
    "Dan verzint hij niets. Hij geeft aan het na te vragen en zet een terugbelnotitie klaar met de gestelde vraag. U bepaalt vooraf welke onderwerpen hij zelfstandig afhandelt en waarbij hij altijd doorschakelt."),
   ("Welke talen spreekt hij?",
    "Nederlands als basis, en waar zinvol ook Vlaams, Frans en Engels. Voor bedrijven in de grensstreek is dat vaak doorslaggevend."),
   ("Worden gesprekken vastgelegd, en hoe verhoudt zich dat tot de AVG?",
    "Van elk gesprek is een transcript beschikbaar, zodat terug te lezen is wat er gezegd is. Omdat daarbij persoonsgegevens van uw klanten worden verwerkt, leggen wij dat vóór de start vast in een verwerkersovereenkomst en informeert u uw bellers hierover. Daar ondersteunen wij u bij."),
   ("Vervangt dit mijn telefonische bezetting of ander personeel?",
    "Nee. Hij vangt op wat anders zou blijven liggen: de avonden, het weekend en de momenten dat er niemand kan opnemen. Urgente en complexe gesprekken gaan naar u door. Het gaat om de telefoontjes die nu verloren gaan, niet om de gesprekken die nu goed verlopen."),
   ("Kan hij ook uitbellen?",
    "Daar beginnen wij bewust niet mee. Bij inkomend verkeer ligt de winst en is het risico beperkt. Uitbellen valt bovendien onder de regelgeving voor koude acquisitie, die u niet ongewild wilt overtreden."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("De situatie", "Bereikbaarheid op de momenten dat het niet uitkomt.",
          "Elk telefoontje dat blijft liggen, is een klant die verder zoekt.",
          pijnblok([
            ("Opnemen onderbreekt het werk", "Opnemen betekent stoppen waar u mee bezig bent. Niet opnemen betekent mogelijk een order mislopen."),
            ("Na sluitingstijd is er niemand", "Terwijl juist dan gebeld wordt: laat op de avond, of vroeg in de ochtend voor aanvang van de dag."),
            ("Verkopers kosten tijd", "Wekelijks terugkerende gesprekken over zonnepanelen, energiecontracten en abonnementen."),
            ("Het verlies is onzichtbaar", "Een gemist telefoontje laat geen spoor achter. Merkbaar is alleen dat het rustiger is dan verwacht."),
          ]), "herkenbaar"),

   sectie("Gespreksverloop", "Een gesprek om 22:41, stap voor stap.",
          "Geen verzonnen scenario, maar het patroon zoals het in de praktijk verloopt.",
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

   sectie("Werkwijze", "Van akkoord tot een werkende telefonist in twee weken.",
          "Het meeste werk zit in het correct vullen van wat hij moet weten. Daarvoor hebben wij enkele keren kort uw input nodig.",
          routeblok([
            ("Nulmeting", "Wanneer gaat de telefoon, wat wordt er gevraagd, en wat mag hij zelfstandig afhandelen? Een half uur."),
            ("Inrichten", "Wij vullen hem met uw assortiment, levertijden en toon. U leest mee en corrigeert."),
            ("Proefdraaien", "Eerst naast de bestaande lijn, zodat u hoort hoe hij functioneert zonder risico."),
            ("Live en bijsturen", "Hij wordt geactiveerd buiten openingstijden en tijdens drukte. De eerste weken luisteren wij mee en scherpen we aan."),
          ]), "werkwijze"),

   sectie("Grenzen", "Wat hij niet doet.",
          "Een AI-telefonist die alles kan bestaat niet. Dit is waar de grens ligt.",
          eerlijkblok(
            "Vier zaken die hij bewust niet doet",
            "Niet omdat het technisch onmogelijk is, maar omdat het in de praktijk misgaat of onverstandig is:",
            ["<strong>Doen alsof hij een mens is.</strong> Hij meldt zich als digitale assistent. Verhullen werkt averechts zodra de beller het merkt.",
             "<strong>Verzinnen wat hij niet weet.</strong> Bij twijfel volgt een terugbelnotitie, geen aanname.",
             "<strong>Klachten en gevoelige gesprekken afhandelen.</strong> Die schakelt hij door. Een ontevreden klant hoort een mens te spreken.",
             "<strong>Uitbellen voor koude acquisitie.</strong> Daar beginnen wij niet aan: de regelgeving is streng en de opbrengst beperkt."]),
          "eerlijk"),
 ]),
},

# ───────────────────────── KLANTCASE: ARONZA ─────────────────────────
{
 "bestand": "case-aronza.html",
 "soort": "case",
 "dienst": "Klantcase: Aronza",
 "titel": "Klantcase Aronza — vier tot zes uur per week terug | Complete AI",
 "beschrijving": "Bij Aronza werden facturatie, kosten, orderverwerking, voorraad en klantcontact geautomatiseerd. Sinds begin mei draait het zonder één storing en is de wekelijkse administratietijd tot nul teruggebracht.",
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
 "slot_tekst": "De onderdelen die bij Aronza draaien zijn niet uniek voor dat bedrijf. Facturatie, kostenregistratie, orderverwerking, voorraad en klantcontact zijn dezelfde processen die bij vrijwel elke ondernemer tijd opeisen. In een half uur bepalen we welke daarvan bij u het meeste opleveren.",
 "vragen": [
   ("Is dit een echte case of een voorbeeld?",
    "Dit is een echte implementatie die dagelijks draait. Aronza is het e-commercebedrijf van de oprichter van Complete AI. Dat is bewust vermeld en niet verborgen: het is de reden dat wij precies weten wat deze systemen doen onder dagelijkse belasting, en waarom ze eerst hier zijn beproefd voordat ze bij klanten werden ingezet."),
   ("Waarom zou dit bij mijn bedrijf ook werken?",
    "Omdat de onderliggende processen hetzelfde zijn. Een factuur opstellen en opvolgen, kosten registreren en categoriseren, een order van binnenkomst naar verzending brengen, voorraad bijhouden en klanten op tijd antwoorden — dat gebeurt bij een vishandel, een garagebedrijf en een webshop op dezelfde manier. Wat verschilt zijn de gegevens en de uitzonderingen, en dat is precies wat wij inrichten."),
   ("Hoe lang duurde de implementatie?",
    "De onderdelen zijn gefaseerd in gebruik genomen, te beginnen bij facturatie en kosten. Voor een klant met een vergelijkbare situatie is de doorlooptijd doorgaans enkele werkdagen per onderdeel, omdat de software al gebouwd en getest is."),
   ("Wat gebeurt er als er iets misgaat?",
    "In deze opzet is dat sinds de ingebruikname niet voorgekomen. Dat is geen garantie voor de toekomst, en daarom is elke automatische handeling terug te zien en terug te draaien. Bij handelingen die naar buiten gaan — een factuur, een bericht aan een klant — is instelbaar of er een goedkeuringsstap tussen zit."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("Uitgangssituatie", "Vier tot zes uur per week aan werk dat niets opleverde.",
          "Aronza is een e-commercebedrijf. Zoals bij vrijwel elke handelsonderneming groeide de administratieve last mee met het aantal orders — en die last kwam volledig op één persoon terecht.",
          """      <div class="voor-na reveal">
        <div class="was">
          <h3>Vóór de automatisering</h3>
          <ul>
            <li>Wekelijks vier tot zes uur aan administratie en facturatie, meestal buiten werktijd</li>
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
          "Transparantie hoort hier bij, dus het staat er expliciet bij.",
          eerlijkblok(
            "Aronza is het eigen bedrijf van de oprichter",
            "Dat is bewust vermeld en niet weggelaten. Er zitten drie kanten aan:",
            ["<strong>Het is geen onafhankelijke referentie.</strong> Een case bij een externe klant weegt zwaarder, en die volgt zodra de eerste opdrachten zijn afgerond.",
             "<strong>Het is wél een echte implementatie.</strong> Deze systemen draaien dagelijks in een bedrijf waar de gevolgen van een fout direct voelbaar zijn. Dat is een strengere test dan een demo-omgeving.",
             "<strong>Het verklaart de doorlooptijd.</strong> Dat automatiseringen bij klanten binnen enkele werkdagen kunnen staan, komt doordat ze hier al gebouwd, getest en in productie genomen zijn. Complete AI verkoopt geen software die het zelf niet gebruikt."]),
          "verantwoording"),
 ]),
},
]
