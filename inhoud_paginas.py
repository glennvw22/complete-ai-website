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
    "Niet per se. Voldoet een bestaande site, dan ligt de winst elders: in vindbaarheid, of in het automatiseren van de administratie. Dat hoort u in de intake, ook wanneer de conclusie is dat u niets bij Complete AI hoeft af te nemen."),
   ("Ik heb geen teksten en geen goede foto's. Is dat een probleem?",
    "Nee, dat is eerder regel dan uitzondering. De teksten schrijven wij op basis van één gesprek waarin we doorvragen op wat u doet en voor wie. Voor beeldmateriaal werken we met wat er is, aangevuld met professionele beelden; is fotografie nodig, dan hoort u dat vooraf."),
   ("Kan ik later zelf wijzigingen doorvoeren?",
    "Ja. Kleine wijzigingen — een tekst, een prijs, openingstijden — vallen onder het onderhoud: één bericht en het is dezelfde dag geregeld. Wilt u het liever zelf doen, dan richten wij dat zo in dat het zonder technische kennis kan."),
   ("Hoe zit het met hosting en onderhoud?",
    "Dat valt onder het maandbedrag: hosting, back-ups, updates, het SSL-certificaat en kleine wijzigingen. Geen losse facturen van drie partijen. Maandelijks opzegbaar."),
   ("Waarom duurt het hier twee weken en elders twee maanden?",
    "Omdat er geen accountmanager, projectleider of tussenlaag tussen zit: u spreekt de persoon die het bouwt. En omdat een groot deel van wat wij inzetten al gebouwd en getest is; wij beginnen niet bij nul."),
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
            ("Intake", "Een half uur om vast te stellen wat er nu staat, wie de klanten zijn en waar het misloopt. Kosteloos en vrijblijvend."),
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
 "titel": "Bedrijfsprocessen automatiseren | Complete AI",
 "beschrijving": "Facturen, orders, herinneringen en reviews die zonder tussenkomst verlopen. Een groot deel draait al, waardoor het binnen enkele werkdagen operationeel is.",
 "omschrijving": "Automatisering van terugkerend werk voor lokale ondernemers: orderintake, facturatie, betaalherinneringen, afspraken, reviews en een dashboard met uw cijfers.",
 "ogen": "Automatisering",
 "h1": 'Terugkerend werk dat <span class="glans">zichzelf afhandelt</span>.',
 "lead": "Facturen opstellen, bevestigingen versturen, betalingen opvolgen, reviews aanvragen. Werk dat moet gebeuren maar geen omzet oplevert. Dat kan geautomatiseerd worden — en omdat een groot deel van wat wij inzetten al operationeel is, staat het binnen enkele werkdagen.",
 "levertijd": "Live binnen enkele werkdagen",
 "uitkomsten": [
     ("17", "automatiseringen die vandaag al draaien en getest zijn"),
     ("Dagen", "in plaats van maanden, omdat wij niet bij nul beginnen"),
     ("0", "handelingen van uw kant zodra het draait"),
 ],
 "slot_kop": "Waar gaat uw tijd naartoe?",
 "slot_tekst": "In een half uur brengen wij in kaart waar de week in gaat zitten. Drie terugkerende taken eisen het grootste deel op. Daar beginnen we; de rest volgt wanneer u dat wilt.",
 "vragen": [
   ("Moet ik mijn huidige systemen vervangen?",
    "Nee. Wij sluiten aan op wat er al in gebruik is: de boekhouding, de agenda, de telefonie. Adviseren wij iets te beëindigen, dan is dat omdat het kosten veroorzaakt zonder rendement — met de onderbouwing erbij."),
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
          "Vier situaties die wij bij ondernemers terugzien.",
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
            ("Intake", "Een half uur om vast te stellen waar de week in gaat zitten. Het zijn drie taken die het grootste deel opeisen."),
            ("Voorstel", "Welke onderdelen wij inzetten, wat het kost en wanneer het staat. Eén vaste prijs, geen nacalculatie."),
            ("Inrichten", "Wij richten de onderdelen in met uw gegevens, huisstijl en werkwijze. Dagen, geen maanden."),
            ("Nazorg", "De eerste weken kijken wij mee en sturen we bij. Daarna ziet u alleen nog het resultaat."),
          ]), "werkwijze"),

]),
},

# ───────────────────────────── AI-TELEFONIST ─────────────────────────────
{
 "bestand": "ai-telefonist.html",
 "dienst": "AI-telefonist",
 "titel": "AI-telefonist die 24/7 opneemt | Complete AI",
 "beschrijving": "Een Nederlandstalige AI die opneemt wanneer u dat niet kunt: 's avonds, in het weekend of tijdens drukte. Neemt bestellingen aan en filtert verkopers.",
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
    "Nederlands als basis, en waar zinvol ook Vlaams, Frans en Engels. Voor bedrijven in de grensstreek is dat doorslaggevend."),
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
            ("Intake", "Wanneer gaat de telefoon, wat wordt er gevraagd, en wat mag hij zelfstandig afhandelen? Een half uur."),
            ("Inrichten", "Wij vullen hem met uw assortiment, levertijden en toon. U leest mee en corrigeert."),
            ("Proefdraaien", "Eerst naast de bestaande lijn, zodat u hoort hoe hij functioneert zonder risico."),
            ("Live en bijsturen", "Hij wordt geactiveerd buiten openingstijden en tijdens drukte. De eerste weken luisteren wij mee en scherpen we aan."),
          ]), "werkwijze"),

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
 "soort": "case",
 "dienst": "AI voor uw bedrijf",
 "titel": "AI in uw bedrijf: wat kan het concreet? | Complete AI",
 "beschrijving": "Welke taken AI vandaag echt kan overnemen in een klein bedrijf, wat het oplevert en hoe lang het duurt. Met cijfers uit een implementatie die sinds mei draait.",
 "omschrijving": "Praktische gids: welke bedrijfstaken AI vandaag kan overnemen bij een mkb-bedrijf, wat dat oplevert en hoe lang het duurt.",
 "ogen": "Gids",
 "h1": 'AI in uw bedrijf: <span class="glans">wat kan het concreet?</span>',
 "lead": "Het korte antwoord: AI neemt vandaag vooral terugkerend administratief werk over — facturen opstellen en opvolgen, kosten registreren, orders verwerken, afspraken bevestigen, de telefoon aannemen buiten kantooruren. Bij een klein bedrijf gaat het al snel om vier tot zes uur per week. Wat AI in 2026 níet betrouwbaar doet, staat verderop op deze pagina.",
 "levertijd": "Leestijd ongeveer 6 minuten",
 "uitkomsten": [
     ("4–6 uur", "per week aan administratie — wat een implementatie sinds mei 2026 daadwerkelijk wegneemt"),
     ("Dagen", "in plaats van maanden, als u begint bij bestaande onderdelen"),
     ("3", "processen waar u het beste begint, en waarom juist die"),
 ],
 "slot_kop": "Benieuwd wat er in uw situatie mogelijk is?",
 "slot_tekst": "In een half uur brengen wij in kaart welke taken bij u de meeste tijd kosten en welke daarvan realistisch te automatiseren zijn. Blijkt dat er weinig te halen valt, dan hoort u dat ook.",
 "vragen": [
   ("Hoe kan ik AI zakelijk gebruiken?",
    "Voor een klein bedrijf zit de winst niet in een groot AI-project, maar in het automatiseren van terugkerende taken die nu handmatig gebeuren. De drie waar de meeste ondernemers beginnen zijn facturatie met automatische opvolging, orderverwerking uit alle kanalen in één lijst, en telefonische bereikbaarheid buiten kantooruren. Die drie zijn concreet, meetbaar en binnen dagen tot weken in te richten."),
   ("Hoe kan ik AI in mijn bedrijf implementeren?",
    "In fasen, te beginnen bij één proces. Breng eerst in kaart waar uw tijd naartoe gaat — drie taken eisen het grootste deel op. Automatiseer daar één van, laat hem een paar weken draaien en meet of het klopt. Pas daarna de volgende. Een grote gelijktijdige invoering mislukt vaker en is duurder te herstellen."),
   ("Welke AI-toepassingen zijn er voor bedrijven?",
    "Voor mkb-bedrijven zijn dit de toepassingen die vandaag daadwerkelijk werken: automatische facturatie en betaalherinneringen, kosten- en btw-registratie, orderintake uit telefoon, e-mail en WhatsApp in één lijst, voorraadbeheer dat meebeweegt, afspraakherinneringen, automatisch om reviews vragen, en een AI-telefonist die buiten openingstijden opneemt. Welke daarvan bij u het meeste oplevert, hangt af van waar nu de meeste tijd in gaat zitten."),
   ("Hoe kan ik mijn boekhouding automatiseren?",
    "Niet in één keer, maar in drie stappen. Eerst de facturatie: facturen automatisch opstellen op basis van de order en openstaande posten automatisch opvolgen. Daarna de kosten: uitgaven bij binnenkomst registreren en categoriseren, zodat de btw-aangifte geen inhaalslag meer is. Als laatste de koppeling met uw boekhoudpakket. Stap één en twee leveren het grootste deel van de tijdwinst op."),
   ("Wat kost het om dit te laten bouwen?",
    "Dat hangt volledig af van welke processen u wilt automatiseren en hoe uw bedrijf werkt. Een standaardprijs zou voor het ene bedrijf te hoog en voor het andere te laag uitvallen. Na een intake van een half uur ligt er één vaste prijs op papier: eenmalig voor de bouw en een vast maandbedrag voor onderhoud."),
   ("Is AI gratis te gebruiken?",
    "Losse hulpmiddelen zoals ChatGPT hebben gratis varianten, en daar kunt u prima teksten mee schrijven of vragen mee uitzoeken. Wat niet gratis is, is het koppelen daarvan aan uw eigen systemen zodat het werk daadwerkelijk zonder tussenkomst verloopt. Dat vraagt inrichting, onderhoud en toezicht — en dat is precies waar het verschil zit tussen een handig hulpmiddel en werk dat u niet meer hoeft te doen."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("Het korte antwoord", "Begin bij het werk dat elke week terugkomt.",
          "De vraag is niet óf AI iets kan betekenen, maar wáár u begint. Voor een klein bedrijf is dat hetzelfde: de taken die wekelijks terugkomen, geen omzet opleveren en toch moeten gebeuren.",
          voorbeeldblok([
            ("Facturatie en opvolging", "Facturen opstellen op basis van de order, versturen, en openstaande posten automatisch opvolgen. De grootste enkele tijdpost én het snelst terugverdiend."),
            ("Kosten en btw", "Uitgaven bij binnenkomst registreren en categoriseren, zodat de kwartaalaangifte geen inhaalslag meer is."),
            ("Orderverwerking", "Bestellingen uit telefoon, e-mail, WhatsApp en webshop komen samen in één lijst, zonder overtypen."),
            ("Telefonische bereikbaarheid", "Een AI-telefonist neemt op buiten openingstijden en tijdens drukte, noteert de bestelling en filtert verkopers eruit."),
            ("Afspraken en herinneringen", "Klanten boeken zelf, krijgen automatisch een bevestiging en een herinnering vóór de afspraak."),
            ("Reviews verzamelen", "Na een geslaagde levering automatisch om een beoordeling vragen — goed voor uw vindbaarheid in Google Maps."),
          ]), "kort-antwoord"),

   sectie("Wat het oplevert", "Cijfers uit een implementatie die nu draait.",
          "Elke pagina over dit onderwerp belooft tijdwinst zonder één getal te noemen. Daarom deze: dit zijn de werkelijke uitkomsten van een bedrijf waar de administratieve afhandeling volledig is geautomatiseerd.",
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
      <p class="prijsnoot reveal">Dit is de implementatie bij Aronza, het e-commercebedrijf van de oprichter van Complete AI. Sinds de ingebruikname begin mei 2026 heeft de opzet geen enkele keer gefaald. Dat het een eigen bedrijf is, staat er bewust bij — <a href="case-aronza.html">de volledige case leest u hier</a>.</p>""",
          "wat-het-oplevert"),

sectie("Zo begint u", "Drie stappen, en waarom juist die volgorde.",
          "De volgorde is belangrijker dan de techniek. Wie met het grootste project begint, ziet het langst niets gebeuren.",
          routeblok([
            ("Meet waar de tijd heen gaat", "Houd één week bij wat u aan terugkerend werk doet. Drie taken eisen het grootste deel op. Zonder deze stap automatiseert u het verkeerde."),
            ("Automatiseer er één", "Begin bij de taak met de meeste uren en de minste uitzonderingen — in de praktijk is dat facturatie. Laat hem enkele weken draaien en controleer of het klopt."),
            ("Breid uit vanaf wat werkt", "Pas als de eerste aantoonbaar draait, komt de volgende. Zo blijft de investering beheersbaar en weet u bij elke stap of het rendeert."),
          ]), "zo-begint-u"),
 ]),
},

# ───────────────────────────── KAPSALONS ─────────────────────────────
{
 "bestand": "ai-voor-kapsalons.html",
 "groep": "branche",
 "dienst": "AI voor kapsalons",
 "titel": "Automatisering en AI voor kapsalons — afspraken, telefoon, no-shows | Complete AI",
 "beschrijving": "De telefoon gaat terwijl u knipt, en no-shows kosten een half uur omzet. Online afspraken, automatische herinneringen en een AI-telefonist die tijdens de behandeling opneemt en inplant.",
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
 "titel": "Automatisering en AI voor garagebedrijven — APK, telefoon, planning | Complete AI",
 "beschrijving": "APK-herinneringen die vanzelf de deur uit gaan, een telefoon die wordt opgenomen terwijl u onder een auto ligt, en klanten die automatisch horen dat hun auto klaar staat.",
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
 "titel": "Automatisering en AI voor de horeca — reserveringen, telefoon, no-shows | Complete AI",
 "beschrijving": "De telefoon gaat midden in de service. Reserveringen die vanzelf binnenkomen, bevestigingen en herinneringen tegen no-shows, en een AI-telefonist die opneemt wanneer de zaak vol staat.",
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
 "titel": "Automatisering en AI voor bouw en installatie — offertes, telefoon, facturen | Complete AI",
 "beschrijving": "Bellen vanaf de steiger kan niet, en offertes schrijven gebeurt \u2019s avonds. Een AI-telefonist die aanvragen aanneemt, offertes die klaarstaan en facturen die vanzelf de deur uit gaan.",
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
 "titel": "Social media uitbesteden — elke week zichtbaar, zonder dat het u tijd kost | Complete AI",
 "beschrijving": "Uw Google-bedrijfsprofiel en social media wekelijks bijgehouden, in uw huisstijl. U stuurt af en toe een foto, wij doen de rest. Maandelijks opzegbaar.",
 "omschrijving": "Social media en Google-bedrijfsprofiel wekelijks bijgehouden voor lokale bedrijven: berichten in uw huisstijl, reviews beantwoord, en een maandrapport over vindbaarheid in plaats van over likes.",
 "ogen": "Social media",
 "h1": 'Elke week zichtbaar, <span class="glans">zonder dat het u tijd kost</span>.',
 "lead": "De meeste bedrijfsaccounts staan stil. Niet uit onwil, maar omdat er altijd iets urgenters is. Het gevolg is een profiel waarvan de laatste post maanden oud is, terwijl de concurrent twee straten verderop elke week iets plaatst en daardoor bovenaan staat wanneer iemand in de buurt zoekt. Complete AI neemt dat ritme over: uw Google-bedrijfsprofiel en uw social media, wekelijks bijgehouden, in uw huisstijl.",
 "levertijd": "Eerste bericht binnen een week",
 "uitkomsten": [
     ("1 uur", "eenmalig \u2014 dat is alles wat wij van uw kant nodig hebben om te beginnen"),
     ("5 min", "per maand om de kalender goed te keuren, en dat mag later vervallen"),
     ("7/7", "er wordt geplaatst, ook in vakanties en drukke weken"),
 ],
 "slot_kop": "Hoe zichtbaar bent u nu eigenlijk?",
 "slot_tekst": "In een half uur kijken we samen naar uw bedrijfsprofiel, uw bestaande accounts en wat de bedrijven om u heen doen. U krijgt een eerlijk beeld van waar u staat \u2014 ook wanneer de conclusie is dat u hier niets voor nodig heeft.",
 "vragen": [
   ("Ik heb geen tijd om foto\u2019s aan te leveren. Werkt het dan wel?",
    "Ja, maar minder goed, en dat zeggen we liever vooraf. Zonder eigen beeldmateriaal maken wij berichten op basis van uw diensten, het seizoen en veelgestelde vragen; dat houdt uw profiel actueel, en daar komt het grootste deel van de vindbaarheid vandaan. E\u00e9n foto per week tilt het van correct naar overtuigend. Daarom is het versturen zo eenvoudig mogelijk gemaakt: een appje, verder niets."),
   ("Moet ik mijn wachtwoorden afgeven?",
    "Nee, en dat zouden wij ook niet willen. Wij krijgen toegang via de offici\u00eble beheeromgevingen van Google en Meta, waar u ons als beheerder toevoegt. Uw accounts blijven van u, wij kunnen alleen wat u ons toestaat, en u trekt die toegang in \u00e9\u00e9n handeling weer in."),
   ("Wat als ik het niet eens ben met een bericht?",
    "U ziet de kalender voordat er iets naar buiten gaat en geeft in diezelfde link aan wat er anders moet. Er gaat niets ongezien de deur uit, tenzij u zelf aangeeft dat die stap mag vervallen."),
   ("Krijg ik hier meer klanten van?",
    "Wij sturen op zichtbaarheid, en dat is precies wat u maandelijks terugziet: hoe vaak u in Google bent getoond, op welke zoekopdrachten, hoe vaak er vanaf uw profiel is gebeld en hoe vaak er een route naar u is aangevraagd. Dat zijn de cijfers die tot klanten leiden, en die staan in het rapport."),
   ("Waarom leggen jullie zoveel nadruk op Google en niet op Instagram?",
    "Omdat daar het verschil zit tussen zichtbaar zijn en vermaakt worden. Een bericht op Instagram bereikt vooral mensen die u al kennen. Uw Google-bedrijfsprofiel bereikt mensen die op dit moment zoeken naar wat u verkoopt. Wij doen allebei, maar het rapport gaat over het tweede."),
   ("Wordt dit met kunstmatige intelligentie gemaakt?",
    "Deels, en dat is precies waarom het haalbaar en vol te houden is. De opzet, de teksten en het opmaken van beeld gebeuren geautomatiseerd; de keuzes over wat er wordt verteld, over uw vak en uw klanten, komen uit het inrichtingsgesprek en uit wat u aanlevert. Wat er niet gebeurt: verzonnen klantverhalen, verzonnen reviews, of beelden van mensen en panden die niet bestaan."),
   ("Kan ik ermee stoppen?",
    "Maandelijks opzegbaar. De profielen, de merkkit en alles wat er geplaatst is, blijven van u."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("De situatie", "Het is geen gebrek aan wil. Het is een gebrek aan ritme.",
          "Social media vraagt geen groot talent, maar wekelijkse aandacht \u2014 en dat is precies wat een ondernemer met een volle agenda niet structureel kan opbrengen.",
          pijnblok([
            ("Het account staat stil", "De laatste post is van maanden geleden. Dat leest als een bedrijf waar het rustig is."),
            ("Vijf berichten in \u00e9\u00e9n week, daarna niets", "Zichtbaarheid komt van regelmaat, niet van vlagen."),
            ("Het bedrijfsprofiel is nooit meer aangeraakt", "Terwijl Google juist daar op actualiteit let bij de vraag wie er in de buurtresultaten bovenaan komt."),
            ("Er ligt genoeg materiaal, het komt er nooit uit", "De foto\u2019s van het mooiste werk staan op de telefoon en blijven daar."),
          ]), "herkenbaar"),

   sectie("De keuze erachter", "Likes zijn geen doel. Gevonden worden wel.",
          "Dit is waar deze dienst op rust, en het is meteen het onderscheid met elk goedkoop postpakket. Wij doen allebei, maar wij zijn eerlijk over waar de opbrengst zit.",
          voorbeeldblok([
            ("Een bericht op Instagram", "Bereikt vooral mensen die u al volgen. Prettig voor het vertrouwen, maar het levert weinig mensen op die u nog niet kenden."),
            ("Een bericht op uw Google-bedrijfsprofiel", "Houdt uw profiel actueel. Google weegt die actualiteit mee bij de vraag wie er bovenaan komt wanneer iemand in de buurt zoekt naar wat u verkoopt."),
            ("Waarom wij allebei doen", "De zichtbare buitenkant is wat u zelf elke dag ziet, en waar u het vertrouwen aan ontleent dat er iets gebeurt. Het maandrapport gaat over het andere: vindbaarheid."),
          ]), "de-keuze"),

   sectie("Wat u krijgt", "Het ritme wordt overgenomen, de accounts blijven van u.",
          "U kiest wat u nodig heeft. Wat er al goed loopt, laten wij staan.",
          krijgtblok([
            ("Google-bedrijfsprofiel bijgehouden", "Wekelijks een update, aanbieding of foto. Dit is het onderdeel dat aantoonbaar met vindbaarheid te maken heeft."),
            ("Berichten in uw huisstijl", "Uw kleuren, uw lettertype, uw manier van praten. Een profiel dat er als \u00e9\u00e9n geheel uitziet."),
            ("Een WhatsApp-nummer voor uw foto\u2019s", "U stuurt een foto van een afgerond werk, wij maken er het bericht van. Meer hoeft u niet te doen."),
            ("Vaste rubrieken in plaats van losse invallen", "Klus in beeld, de vraag van de week, seizoen, team, review. Zo blijft het gevarieerd en herkenbaar."),
            ("Vooraf zichtbaar, achteraf verantwoord", "U ziet de maand vooruit en keurt hem in vijf minuten goed. Achteraf krijgt u een rapport."),
            ("Reviews beantwoord", "Binnen \u00e9\u00e9n dag, ook de kritische. Juist daar kijken mensen naar."),
            ("Uw accounts blijven van u", "Wij werken via de offici\u00eble beheeromgevingen. Geen wachtwoorden, en u trekt de toegang in \u00e9\u00e9n handeling weer in."),
            ("Maandelijks opzegbaar", "Geen jaarcontract. Wat er staat, blijft van u."),
          ]), "wat-u-krijgt"),

   sectie("De voerlijn", "Het eenvoudigste onderdeel, en tegelijk het belangrijkste.",
          "Zonder invoer van uw kant maakt elk systeem \u2014 hoe geavanceerd ook \u2014 inwisselbare praatjes. E\u00e9n foto per week is genoeg om dat te voorkomen. Daarom is het versturen zo eenvoudig mogelijk gemaakt.",
          routeblok([
            ("U stuurt een foto", "Een afgerond werk, een volle zaak, een nieuwe levering, een tevreden klant. Naar \u00e9\u00e9n WhatsApp-nummer. Geen tekst, geen uitleg, geen inlogscherm."),
            ("Wij maken er het bericht van", "Bijsnijden, opknappen, tekst erbij, in uw huisstijl. Uw eigen beeld krijgt altijd voorrang boven gegenereerd beeld."),
            ("Het staat op het juiste moment op de juiste kanalen", "Geplaatst op de tijden die in uw branche werken, zeven dagen per week. Mislukt een plaatsing, dan wordt hij opnieuw aangeboden en merkt u er niets van."),
          ]), "voerlijn"),

   sectie("De inhoud", "Berichten worden niet verzonnen, maar uit vaste rubrieken opgebouwd.",
          "Dat voorkomt dat alles op elkaar gaat lijken, en het maakt de dienst maand na maand voorspelbaar. Welke rubrieken passen en in welke verhouding, verschilt per bedrijf: een garagebedrijf heeft een andere mix dan een kapsalon.",
          voorbeeldblok([
            ("Klus in beeld", "Een afgerond werk, een voor-en-na, een geleverd product. Het enige bewijs dat telt: wat u werkelijk doet."),
            ("De vraag van de week", "E\u00e9n veelgestelde klantvraag, beantwoord. Letterlijk wat iemand in Google intypt."),
            ("Aanbieding of actie", "Een tijdelijk aanbod, ook los te plaatsen als Google-aanbieding. Directe aanleiding tot contact."),
            ("Seizoen en agenda", "Weer, feestdagen, vakanties, lokale evenementen. Sluit aan bij waar mensen op dat moment mee bezig zijn."),
            ("Team en achter de schermen", "Wie er werkt en hoe het eraan toegaat. Bij lokale bedrijven het best gelezen type bericht."),
            ("Review uitgelicht", "Een echte klantreactie, netjes vormgegeven. Sociale bewijskracht zonder zelf te hoeven opscheppen."),
            ("Tip van de vakman", "Praktisch advies uit het vak. Positioneert u als degene die het weet."),
            ("Mythe ontkracht", "Een hardnekkig misverstand uit uw branche rechtzetten. Levert de meeste reacties op."),
          ]), "rubrieken"),

   sectie("Kanalen", "Waar het geplaatst wordt, en waarom.",
          "Voor kanalen die hier niet staan geldt: vragen kan altijd, maar wij nemen niets op wat wij niet betrouwbaar kunnen leveren.",
          voorbeeldblok([
            ("Google-bedrijfsprofiel", "Updates, aanbiedingen, evenementen, foto\u2019s en reviewreacties. De kern van de dienst; hier zit de meetbare opbrengst."),
            ("Instagram", "Afbeelding, carrousel, korte video en Story. Vereist een zakelijk account dat aan een Facebook-pagina gekoppeld is \u2014 dat regelen wij."),
            ("Facebook-pagina", "Tekst, beeld, video en links. Voor veel branches nog altijd het kanaal waar de klanten daadwerkelijk zitten."),
            ("LinkedIn-bedrijfspagina", "Berichten en documenten. Alleen zinvol wanneer u aan zakelijke klanten levert."),
            ("TikTok", "Video, op verzoek en in overleg. Vraagt een aparte goedkeuringsprocedure en een ander soort inhoud."),
            ("Pinterest", "Pins. Alleen bij interieur, bouw, horeca en mode; daarbuiten levert het te weinig op."),
          ]), "kanalen"),

   sectie("Vertrekpunten", "Drie niveaus waar dit begint.",
          "Net als bij de pakketten op de homepage: dit zijn vertrekpunten, geen menukaart. Het aantal kanalen, de frequentie en de hoeveelheid werk verschillen per bedrijf, en de samenstelling volgt uit de intake.",
          krijgtblok([
            ("Zichtbaar blijven", "Voor de eenmanszaak die vooral gevonden wil worden. Google-bedrijfsprofiel wekelijks bijgehouden, \u00e9\u00e9n social kanaal met een paar berichten per week, de voerlijn via WhatsApp en een maandrapport over vindbaarheid. Past bij: hovenier, klusbedrijf, praktijk, adviseur."),
            ("Zichtbaar zijn", "Voor het bedrijf met personeel dat er verzorgd op wil staan. Meerdere kanalen, hogere frequentie, korte video\u2019s per maand, reviews die beantwoord worden en een kwartaalgesprek. Past bij: kapsalon, garagebedrijf, restaurant, makelaar, praktijk."),
            ("De eerste zijn in de regio", "Voor wie lokaal de bekendste wil worden. Dagelijkse aanwezigheid op alle kanalen, wekelijkse video, volledige profieloptimalisatie, reviewbeheer, en de koppeling naar advertenties zodat het beste bericht ook bij nieuwe mensen terechtkomt. Past bij: bedrijven met meerdere vestigingen of een lopend advertentiebudget."),
          ]), "vertrekpunten"),

   sectie("Werkwijze", "Van intake tot een ritme dat vanzelf doorloopt.",
          "Voorbereiding is niet nodig. Wat wij vragen is een half uur, en daarna \u00e9\u00e9n gesprek van ongeveer een uur.",
          routeblok([
            ("Intake", "Een half uur waarin we kijken wat er nu staat: het bedrijfsprofiel, de bestaande accounts, en wat de concurrent in de buurt doet. Kosteloos en vrijblijvend. U hoort ook wanneer de winst ergens anders ligt."),
            ("Inrichting", "\u00c9\u00e9n gesprek van ongeveer een uur over uw diensten, uw klanten, uw manier van praten en wat er absoluut niet gezegd mag worden. Daarna zetten wij de profielen op orde en maken wij de merkkit."),
            ("Eerste maand", "U ontvangt de kalender van de eerste maand ter goedkeuring, plus het WhatsApp-nummer waar u foto\u2019s naartoe stuurt. Vanaf dat moment loopt het."),
            ("Doorlopend", "Elke maand een kalender vooraf en een rapport achteraf, in gewone taal. Maandelijks opzegbaar."),
          ]), "werkwijze"),

   sectie("Uw aandeel", "Wat u zelf moet doen \u2014 en dat is werkelijk alles.",
          "Dit is het bezwaar dat iedereen heeft, dus staat het er zwart op wit. Geen wachtwoorden afgeven, geen inlogschermen, geen software leren.",
          voorbeeldblok([
            ("Eenmalig ongeveer een uur", "Het inrichtingsgesprek. Daarna hoeft dat niet meer."),
            ("Vijf minuten per maand", "De kalender goedkeuren. Merkt u na een paar maanden dat u toch altijd akkoord geeft, dan mag die stap vervallen."),
            ("Af en toe een foto", "Naar \u00e9\u00e9n WhatsApp-nummer. Geen verplichting en geen minimum \u2014 hoe meer u stuurt, hoe persoonlijker het wordt."),
          ]), "uw-aandeel"),

]),
},

]
