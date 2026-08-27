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
 "h1": 'Een website die <span class="glans">klanten oplevert</span>. Niet alleen een mooie.',
 "lead": "De meeste sites zien er prima uit en doen verder niets. Ze staan er, ze worden niet gevonden, en er belt niemand naar aanleiding van. Wij bouwen sites waar wél iets uit komt — en we doen er één tot twee weken over in plaats van twee maanden.",
 "levertijd": "Live in 1 tot 2 weken",
 "uitkomsten": [
     ("0,7 s", "laadtijd van deze pagina — dat is de norm die we ook voor jou aanhouden"),
     ("83%", "van je bezoekers komt op een telefoon; daar ontwerpen we als eerste voor"),
     ("1–2 wk", "van akkoord tot live, inclusief teksten en beeld"),
 ],
 "slot_kop": "Benieuwd wat er van jouw site te maken valt?",
 "slot_tekst": "In een half uur kijken we samen naar wat je nu hebt, wie je klanten zijn en waar het misgaat. Je krijgt een eerlijk advies mee — ook als dat is dat je site prima is en de winst ergens anders zit.",
 "vragen": [
   ("Moet ik van mijn huidige website af?",
    "Niet per se. Soms is je bestaande site prima en zit de winst ergens anders: in vindbaarheid, of in het automatiseren van je administratie. Dat hoor je eerlijk in de nulmeting, ook als het antwoord is dat je niets bij mij hoeft af te nemen."),
   ("Ik heb geen teksten en geen goede foto's. Is dat een probleem?",
    "Nee, dat is eerder regel dan uitzondering. De teksten schrijf ik op basis van één gesprek waarin ik doorvraag op wat je doet en voor wie. Voor beeld werken we met wat je hebt, aangevuld met professionele beelden; is fotografie nodig, dan zeg ik dat vooraf."),
   ("Kan ik later zelf dingen aanpassen?",
    "Ja. Kleine wijzigingen — een tekst, een prijs, openingstijden — zitten bij het onderhoud in: je appt of belt en het is dezelfde dag geregeld. Wil je liever zelf in de knoppen, dan richten we dat zo in dat je het zonder technische kennis kunt."),
   ("Hoe zit het met hosting en onderhoud?",
    "Dat zit in het maandbedrag: hosting, back-ups, updates, het SSL-certificaat en kleine wijzigingen. Je krijgt geen aparte rekeningen van drie partijen. Maandelijks opzegbaar."),
   ("Waarom kan het bij jullie in twee weken en elders in twee maanden?",
    "Omdat er geen accountmanager, projectleider en tussenlaag tussen zit. Je spreekt de persoon die het bouwt. En omdat veel van wat we inzetten al staat en getest is; we beginnen zelden bij nul."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("Herkenbaar?", "Een mooie site is niet hetzelfde als een site die werkt.",
          "Dit zijn de vier dingen die we het vaakst tegenkomen als we naar een bestaande site kijken.",
          pijnblok([
            ("Je wordt niet gevonden", "Je staat online, maar wie niet je bedrijfsnaam intypt komt je nooit tegen."),
            ("Hij laadt traag op een telefoon", "En daar komt het overgrote deel van je bezoekers vandaan. Elke seconde kost je mensen."),
            ("Er is niets te doen", "Geen duidelijke volgende stap, dus kijkt iemand rond en klikt weg."),
            ("Aanpassen kost een e-mail en een week", "Waardoor je het niet meer doet en de site langzaam veroudert."),
          ]), "herkenbaar"),

   sectie("Wat je krijgt", "Alles wat er nodig is, in één keer geregeld.",
          "Geen losse onderdelen die je zelf moet samenbrengen. Je hebt één aanspreekpunt en aan het eind staat er iets dat af is.",
          krijgtblok([
            ("Ontwerp op maat", "Geen sjabloon met jouw logo erin. Het ontwerp volgt jouw zaak, je klanten en wat je wilt bereiken."),
            ("Mobiel eerst", "We ontwerpen op de telefoon en werken omhoog naar de laptop, niet andersom. Dat is waar je bezoekers zitten."),
            ("Snelheid als uitgangspunt", "Geen zware bouwers of tientallen plug-ins. Deze pagina laadt in ongeveer 0,7 seconde; dat is de norm die we aanhouden."),
            ("Teksten die kloppen", "Geschreven op basis van één gesprek. In jouw taal, gericht op de klant die je wilt hebben."),
            ("Vindbaar vanaf dag één", "Nette structuur, sitemap, structuurdata en een Google-bedrijfsprofiel dat volledig staat."),
            ("Formulier dat aankomt", "Klinkt vanzelfsprekend. Het is de meest voorkomende fout die we op bestaande sites vinden."),
            ("Veilig en zonder waarschuwingen", "HTTPS met een certificaat dat zichzelf verlengt, geen database en geen inlogscherm — dus niets te hacken."),
            ("Hosting en onderhoud", "Inbegrepen in het maandbedrag. Kleine wijzigingen ook. Maandelijks opzegbaar."),
          ]), "wat-je-krijgt"),

   sectie("Zo gaat het", "Van eerste gesprek tot live in vier stappen.",
          "Je hoeft niets voor te bereiden. Het enige wat ik van je nodig heb is een half uur en een eerlijk verhaal over hoe het nu loopt.",
          routeblok([
            ("Nulmeting", "Een half uur samen kijken naar wat je nu hebt, wie je klanten zijn en waar het misgaat. Gratis en vrijblijvend."),
            ("Voorstel", "Binnen één werkdag op papier: wat we bouwen, wat het kost, wanneer het staat. Eén vaste prijs."),
            ("Bouwen", "Je krijgt na een paar dagen een link om mee te kijken. Aanpassingen doen we onderweg, niet pas aan het eind."),
            ("Live", "We zetten hem live, koppelen je domein en e-mail, en ik loop het met je door tot je ermee overweg kunt."),
          ]), "werkwijze"),

   sectie("Bewijs", "Deze pagina is er zelf een voorbeeld van.",
          "Je hoeft niet op mijn woord af te gaan — je kijkt er nu naar.",
          eerlijkblok(
            "Wat je hier kunt controleren",
            "Alles wat ik hierboven beloof, is op deze pagina zelf te meten:",
            ["De site laadt in ongeveer <strong>0,7 seconde</strong>, ook op een telefoon.",
             "Er zit <strong>geen cookiebanner</strong> in, omdat er geen tracking op staat die je gedrag volgt.",
             "Het slotje in je adresbalk is <strong>groen en geldig</strong> — geen waarschuwingen.",
             "Verklein dit venster tot telefoonformaat: alles blijft leesbaar en bruikbaar.",
             "Deze site is <strong>in één nacht gebouwd</strong>. Voor een klant nemen we er meer tijd voor, maar het geeft aan waar het tempo vandaan komt."]),
          "bewijs"),
 ]),
},

# ───────────────────────────── AUTOMATISERING ─────────────────────────────
{
 "bestand": "automatisering.html",
 "dienst": "Automatisering",
 "titel": "Bedrijfsprocessen automatiseren — live in enkele werkdagen | Complete AI",
 "beschrijving": "Facturen, orders, herinneringen en reviews die vanzelf gaan. Veel van wat we inzetten draait al, dus het staat vaak binnen enkele werkdagen bij je.",
 "omschrijving": "Automatisering van terugkerend werk voor lokale ondernemers: orderintake, facturatie, betaalherinneringen, afspraken, reviews en een dashboard met je cijfers.",
 "ogen": "Automatisering",
 "h1": 'Het werk dat je <span class="glans">avonden opeet</span>, gaat vanzelf.',
 "lead": "Facturen maken, bevestigingen sturen, achter betalingen aan, om reviews vragen. Werk dat móet gebeuren maar niets oplevert. Dat kan de computer overnemen — en omdat veel van wat we inzetten al draait, staat het vaak binnen een paar werkdagen bij je.",
 "levertijd": "Vaak live binnen enkele werkdagen",
 "uitkomsten": [
     ("17", "automatiseringen die vandaag al draaien en getest zijn"),
     ("Dagen", "in plaats van maanden, omdat we zelden bij nul beginnen"),
     ("0", "handelingen van jou nadat het staat"),
 ],
 "slot_kop": "Wat kost jou de meeste tijd?",
 "slot_tekst": "In een half uur brengen we samen in kaart waar je week in gaat zitten. Vaak blijkt dat drie terugkerende taken het grootste deel opeten — daar beginnen we, en de rest kan altijd later.",
 "vragen": [
   ("Moet ik mijn huidige systemen weggooien?",
    "Nee. In de meeste gevallen sluiten we aan op wat je al gebruikt — je boekhouding, je agenda, je telefoon. Gooien we iets weg, dan is dat omdat het je geld kost zonder dat het iets doet, en dan zeg ik dat met redenen erbij."),
   ("Wat als de automatisering iets fout doet?",
    "Daarom bouwen we in stappen en kijken we de eerste weken mee. Alles wat automatisch gebeurt is terug te zien en terug te draaien. En bij dingen die de deur uit gaan — een factuur, een bericht aan een klant — bepaal jij of er nog een goedkeuring tussen zit."),
   ("Hoe kan het zo snel als het maatwerk is?",
    "Omdat de onderdelen al bestaan. Het klantenbestand, de facturatie, de agenda, het omzetdashboard: die zijn gebouwd, getest en draaien al. Wat we voor jou doen is ze kiezen, inrichten met jouw gegevens en aan elkaar knopen. Dat is dagen werk, geen maanden."),
   ("Kan ik er zelf bij, of ben ik afhankelijk van jullie?",
    "Je kunt er zelf bij, en de gegevens zijn van jou. Wil je later weg, dan krijg je alles mee in een gangbaar bestandsformaat. Ik werk liever met klanten die blijven omdat het werkt dan met klanten die vastzitten."),
   ("Hoe zit het met mijn klantgegevens en de AVG?",
    "Waar wij persoonsgegevens verwerken, leggen we dat vast in een verwerkersovereenkomst zoals de wet voorschrijft — vóór de start, niet achteraf. Je gegevens blijven van jou en worden nooit gedeeld of doorverkocht."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("Herkenbaar?", "Het werk na het werk.",
          "Je bent ondernemer geworden voor je vak. Niet voor dit deel.",
          pijnblok([
            ("De administratie doe je 's avonds", "Als de zaak dicht is en je eigenlijk klaar bent. Elke week weer."),
            ("Bestellingen komen overal binnen", "Telefoon, WhatsApp, mail, misschien de webshop. En jij bent de plek waar het samenkomt."),
            ("Je loopt achter je geld aan", "Facturen staan open, herinneringen sturen voelt vervelend, dus stel je het uit."),
            ("Reviews vraag je nooit", "Terwijl je weet dat ze je zouden helpen. Er is gewoon geen moment voor."),
          ]), "herkenbaar"),

   sectie("Wat er kan", "Een greep uit wat vandaag al draait.",
          "Dit zijn geen plannen of schermen die nog gebouwd moeten worden — dit is software die bestaat, getest is en bij klanten kan draaien. We kiezen samen welke onderdelen bij jou zinvol zijn.",
          voorbeeldblok([
            ("Facturatie en betaalherinneringen", "Facturen maken en versturen, en trage betalers krijgen automatisch een vriendelijke herinnering die oploopt."),
            ("Offertes maken en opvolgen", "Offertes opstellen, versturen en zien wie er nog niet gereageerd heeft."),
            ("Klantenbestand", "Contactgegevens, historie en notities per klant. Geen losse briefjes en zoeken in je telefoon meer."),
            ("Online laten boeken", "Klanten plannen zelf een afspraak via een link, direct in jouw agenda."),
            ("Afspraakherinneringen", "Automatisch een bericht vóór de afspraak, zodat er niemand meer vergeet te komen."),
            ("Terugkom-berichten", "Een berichtje als het tijd is voor een nieuwe afspraak. Zet omzet aan zonder te bellen."),
            ("Reviews verzamelen", "Na een geslaagde levering netjes om een beoordeling vragen, en ze op je site tonen."),
            ("Omzetdashboard", "Omzet per dag, week of maand in duidelijke grafieken. Beslissen op cijfers in plaats van gevoel."),
            ("Kosten en btw", "Uitgaven op één plek, netjes verdeeld, en de btw per kwartaal klaar voor de aangifte."),
            ("Winst, verlies en kasstroom", "Zie wat er overblijft en of het de komende maanden krap wordt."),
            ("Betaallinks", "Klanten direct online laten betalen via iDEAL, zonder gedoe met overschrijvingen."),
            ("WhatsApp-assistent", "Automatische antwoorden op veelgestelde vragen, ook buiten openingstijden."),
          ]), "wat-er-kan"),

   sectie("Zo gaat het", "We beginnen met de drie die het meeste kosten.",
          "Nooit alles tegelijk. Dat is niet alleen prettiger, het is ook goedkoper en je ziet sneller of het werkt.",
          routeblok([
            ("Nulmeting", "Een half uur samen kijken waar je week in gaat zitten. Meestal zijn het drie taken die het grootste deel opeten."),
            ("Voorstel", "Welke onderdelen we inzetten, wat het kost en wanneer het staat. Eén vaste prijs, geen uurtje-factuurtje."),
            ("Inrichten", "We zetten de onderdelen klaar met jouw gegevens, je huisstijl en je manier van werken. Dagen, geen maanden."),
            ("Meekijken", "De eerste weken kijken we mee en sturen we bij. Daarna merk je alleen nog dat het gebeurd is."),
          ]), "werkwijze"),

   sectie("Eerlijk", "Wat het nog niet doet.",
          "Liever nu duidelijk dan een teleurstelling achteraf.",
          eerlijkblok(
            "Drie dingen die een externe koppeling nodig hebben",
            "Deze onderdelen zijn volledig gebouwd tot aan de laatste stap, maar die laatste stap vraagt een account bij een externe partij. We regelen dat in fase twee, en je hoort het vooraf:",
            ["<strong>Echt versturen van e-mail en sms.</strong> Het bericht wordt volledig klaargezet met een kopieerknop; verzenden koppelen we aan zodra je provider erop staat.",
             "<strong>Automatisch incasseren.</strong> Betaallinks werken; automatische incasso vraagt een koppeling met Mollie of Stripe.",
             "<strong>Rechtstreekse koppeling met je boekhouding.</strong> Export naar Excel en pdf werkt vandaag; de directe koppeling met Moneybird of e-Boekhouden bouwen we op aanvraag."]),
          "eerlijk"),
 ]),
},

# ───────────────────────────── AI-TELEFONIST ─────────────────────────────
{
 "bestand": "ai-telefonist.html",
 "dienst": "AI-telefonist",
 "titel": "AI-telefonist die 24/7 opneemt — operationeel binnen 2 weken | Complete AI",
 "beschrijving": "Een Nederlandstalige AI die de telefoon opneemt als jij niet kunt: 's avonds, in het weekend of midden in de drukte. Neemt bestellingen aan en filtert verkopers eruit.",
 "omschrijving": "Nederlandstalige AI-telefonist die gesprekken aanneemt, bestellingen noteert, vragen beantwoordt, urgente gesprekken doorschakelt en cold callers eruit filtert.",
 "ogen": "AI-telefonist",
 "h1": 'De telefoon die <span class="glans">altijd</span> wordt opgenomen.',
 "lead": "Een gemist telefoontje is niet neutraal. Dat is een klant die de volgende belt. De AI-telefonist neemt op als jij niet kunt — 's avonds, in het weekend, of midden in de drukte — noteert de bestelling en zet hem netjes in je lijst.",
 "levertijd": "Operationeel binnen 2 weken",
 "uitkomsten": [
     ("24/7", "bereikbaar, ook in het weekend en op feestdagen"),
     ("2 wk", "van akkoord tot een werkende telefonist op je nummer"),
     ("100%", "van de gesprekken vastgelegd met een transcript"),
 ],
 "slot_kop": "Hoeveel telefoontjes mis je in een week?",
 "slot_tekst": "De meeste ondernemers weten het niet, want een gemist telefoontje laat geen spoor achter. In een half uur rekenen we het samen door: hoe vaak gaat de telefoon terwijl je niet kunt, en wat is zo'n gesprek gemiddeld waard.",
 "vragen": [
   ("Hoort een klant dat het geen mens is?",
    "Sommige mensen horen het, andere niet. Belangrijker is dat hij niet doet alsof: hij meldt zich als de digitale assistent van je zaak. Dat werkt in de praktijk beter dan verhullen — mensen accepteren het prima zolang ze snel en correct geholpen worden."),
   ("Wat als hij een vraag niet weet?",
    "Dan verzint hij niets. Hij zegt dat hij het navraagt en zet een terugbelnotitie klaar met wat er gevraagd is. Jij bepaalt vooraf welke onderwerpen hij zelf mag afhandelen en waarbij hij altijd naar jou doorschakelt."),
   ("Welke talen spreekt hij?",
    "Nederlands als basis, en waar dat zinvol is ook Vlaams, Frans en Engels. Voor bedrijven in de grensstreek is dat vaak precies het verschil."),
   ("Worden gesprekken opgenomen? Hoe zit dat met de AVG?",
    "Van elk gesprek is een transcript beschikbaar, zodat je kunt teruglezen wat er gezegd is. Omdat daarbij persoonsgegevens van jouw klanten verwerkt worden, leggen we dat vóór de start vast in een verwerkersovereenkomst en informeer je je bellers erover. We helpen je daarmee."),
   ("Vervangt dit mijn telefoon of mijn personeel?",
    "Nee. Hij vangt op wat anders zou blijven liggen: de avonden, het weekend, en de momenten dat je met je handen in het werk zit. Urgente en ingewikkelde gesprekken gaan gewoon naar jou. Het gaat om de telefoontjes die je nu kwijtraakt, niet om de gesprekken die je nu goed voert."),
   ("Kan hij ook uitbellen?",
    "Daar beginnen we bewust niet mee. Inkomend is waar de winst zit en waar het risico klein is. Uitbellen brengt bovendien regels met zich mee rond koude acquisitie waar je niet per ongeluk overheen wilt gaan."),
 ],
 "inhoud": "\n\n  <hr class=\"streep\">\n\n".join([
   sectie("Herkenbaar?", "De telefoon gaat altijd op het verkeerde moment.",
          "En elk telefoontje dat blijft liggen, is een klant die verder zoekt.",
          pijnblok([
            ("Je staat met je handen in het werk", "Opnemen betekent stoppen waar je mee bezig bent. Niet opnemen betekent misschien een order kwijt."),
            ("Na sluitingstijd is er niemand", "Terwijl juist dan gebeld wordt: 's avonds laat, of vroeg in de ochtend voordat de dag begint."),
            ("Verkopers vreten je tijd", "Elke week weer iemand met zonnepanelen of een nieuwe energiecontract."),
            ("Je weet niet wat je misloopt", "Een gemist telefoontje laat geen spoor achter. Je merkt alleen dat het rustiger is dan het zou moeten zijn."),
          ]), "herkenbaar"),

   sectie("Zo klinkt een avond", "Een gesprek van kwart voor elf, stap voor stap.",
          "Dit is geen verzonnen scenario maar het patroon zoals het in de praktijk verloopt.",
          """      <div class="uitgelicht reveal">
        <div class="tijdlijn">
          <div class="beurt hoogte"><span class="klok">22:41</span><span class="tekst">Een klant belt ver na sluitingstijd. <b>De telefonist neemt op</b>, in het Nederlands, en meldt zich als de assistent van je zaak.</span></div>
          <div class="beurt"><span class="klok">22:42</span><span class="tekst">Hij noteert wat er besteld wordt, controleert wat er mogelijk is en <b>beantwoordt vragen over levering</b> en assortiment.</span></div>
          <div class="beurt"><span class="klok">22:43</span><span class="tekst">Weet hij iets niet? Dan verzint hij niets, maar <b>zet hij een terugbelnotitie klaar</b> met de vraag erin.</span></div>
          <div class="beurt"><span class="klok">22:43</span><span class="tekst">Is het dringend of ingewikkeld? Dan <b>schakelt hij door naar jou</b>. Wat dringend is, bepaal jij vooraf.</span></div>
          <div class="beurt hoogte"><span class="klok">22:44</span><span class="tekst">De order staat gestructureerd in je lijst, de klant heeft een bevestiging, en <b>jij hebt niets hoeven doen</b>.</span></div>
          <div class="beurt"><span class="klok">morgen</span><span class="tekst">Een verkoper aan de lijn? <b>Die wordt eruit gefilterd</b> — je hoort er niets van, maar je kunt hem wel teruglezen.</span></div>
        </div>
        <div class="kunde">
          <div><b>Nederlands</b><small>Ook Vlaams, Frans en Engels waar dat nodig is</small></div>
          <div><b>24 uur per dag</b><small>Weekend, feestdagen en midden in de drukte</small></div>
          <div><b>Altijd vastgelegd</b><small>Volledig transcript bij elk gesprek</small></div>
          <div><b>Jij houdt de regie</b><small>Jij bepaalt wat hij zelf mag en wat naar jou gaat</small></div>
        </div>
      </div>""", "zo-klinkt-het"),

   sectie("Zo gaat het", "Van akkoord tot een werkende telefonist in twee weken.",
          "Het meeste werk zit in het goed vullen van wat hij moet weten. Daar heb ik jou een paar keer kort voor nodig.",
          routeblok([
            ("Nulmeting", "Wanneer gaat je telefoon, wat wordt er gevraagd, en wat mag hij zelf afhandelen? Een half uur."),
            ("Inrichten", "We vullen hem met jouw assortiment, je levertijden en je manier van praten. Jij leest mee en corrigeert."),
            ("Proefdraaien", "Eerst naast je bestaande lijn, zodat je hoort hoe hij het doet zonder dat er iets misgaat."),
            ("Live en bijsturen", "Hij gaat aan buiten je openingstijden of tijdens drukte. De eerste weken luisteren we mee en scherpen we aan."),
          ]), "werkwijze"),

   sectie("Eerlijk", "Wat hij niet doet.",
          "Een AI-telefonist die alles zou kunnen bestaat niet. Dit is waar de grens ligt.",
          eerlijkblok(
            "Vier dingen die hij bewust niet doet",
            "Niet omdat het technisch onmogelijk is, maar omdat het in de praktijk misgaat of onverstandig is:",
            ["<strong>Doen alsof hij een mens is.</strong> Hij meldt zich als digitale assistent. Verhullen werkt averechts zodra iemand het doorheeft.",
             "<strong>Verzinnen wat hij niet weet.</strong> Bij twijfel wordt het een terugbelnotitie, geen gok.",
             "<strong>Klachten en gevoelige gesprekken afhandelen.</strong> Die schakelt hij door. Een boze klant hoort een mens te krijgen.",
             "<strong>Uitbellen voor koude acquisitie.</strong> Daar beginnen we niet aan; de regels daaromheen zijn streng en de opbrengst is klein."]),
          "eerlijk"),
 ]),
},
]
