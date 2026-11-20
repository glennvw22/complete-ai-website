# -*- coding: utf-8 -*-
"""Pagina's op zoekopdrachten van kopers (19-11-2026, naar aanleiding van de reel over Search Console, zoekopdrachten van kopers en pagina's daarvoor).
Elke pagina antwoordt één vraag die een ondernemer in Google typt vlak voor hij iets inkoopt. De zoekzinnen komen uit de automatische aanvulling
van Google (suggest, 19-11-2026). Alle beweringen over Complete AI komen uit bestaande pagina's van de site; feiten over de wereld uit een bron
die is gelezen en onderaan de pagina staat. Geen bedragen, geen klantnamen, formele u-vorm.

Wordt aan PAGINAS toegevoegd onderaan inhoud_paginas.py."""
from inhoud_kort import proza, pijn, krijgt, route


def bron(tekst, url, toelichting):
    return f'<li><a href="{url}" target="_blank" rel="noopener">{tekst}</a>. {toelichting}</li>'


def bronnen_blok(items):
    lijst = "".join(bron(*b) for b in items)
    return proza("bronnen", "Bronnen", "Waar deze pagina op berust.",
                 f'<p>Wat hier over regels en functies staat, komt uit deze bronnen.</p><ul>{lijst}</ul>')


# ───────────────────────── offertes automatiseren ─────────────────────────
OFFERTES = {
 "bestand": "offertes-automatiseren.html",
 "soort": "gids",
 "dienst": "Offertes automatiseren",
 "titel": "Offertes automatiseren: aanvraag tot offerte | Complete AI",
 "beschrijving": "Offertes automatiseren: aanvragen in één lijst, een concept met uw eigen posten, digitaal ondertekend en opgevolgd. U beslist wat de deur uitgaat.",
 "omschrijving": "Offertes automatiseren voor bedrijven in Nederland en België: aanvragen in één lijst, een concept met uw eigen posten, digitaal ondertekenen en opvolgen. De prijs en de inhoud blijven van u.",
 "ogen": "Gids",
 "h1": 'Offertes automatiseren: <span class="glans">van aanvraag tot ondertekende offerte</span>.',
 "lead": 'Offertes automatiseren betekent dat een aanvraag vanzelf op de juiste plek komt, dat er een concept klaarstaat met uw eigen posten en dat de opvolging niet van uw geheugen afhangt. U controleert, past aan en verstuurt. Complete AI richt dat in voor bedrijven in Nederland en België, aansluitend op wat u al gebruikt.',
 "levertijd": "Live binnen enkele werkdagen",
 "uitkomsten": [
     ("Eén lijst", "aanvragen komen op één plek binnen"),
     ("Uw akkoord", "u bepaalt wat zonder uw akkoord de deur uitgaat"),
     ("Opvolging", "een offerte zonder reactie wordt vanzelf opgevolgd"),
 ],
 "slot_kop": "Hoeveel offertes schrijft u per maand?",
 "slot_tekst": "In een half uur nemen we uw werkwijze door. Binnen één werkdag volgt een voorstel met één vaste prijs.",
 "vragen": [
  ("Wat is offertes automatiseren?",
   "Het werk rond een offerte door software laten doen, terwijl u de prijs en de inhoud bepaalt. Een aanvraag komt in één lijst, er staat een concept klaar, de klant ondertekent digitaal en een offerte zonder reactie wordt opgevolgd."),
  ("Schrijft de software de offerte zelf?",
   "Niet zelfstandig, en dat zou ook niet verstandig zijn: u bepaalt de prijs. De software zet een concept klaar met de gegevens van de aanvraag en uw standaardposten. U kijkt na, past aan en verstuurt."),
  ("Wat moet er in een offerte staan?",
   "Volgens Ondernemersplein uw bedrijfsgegevens en die van de klant, de datum en een offertenummer, een samenvatting van de werkzaamheden, het tarief of de projectprijs, de geldigheidsduur, afspraken over een aanbetaling en een verwijzing naar uw algemene voorwaarden."),
  ("Is een offerte juridisch bindend?",
   "Volgens Ondernemersplein bestaat er geen verplichte vorm, maar is een offerte die de klant ondertekend terugstuurt een bindend contract. Twijfelt u over de inhoud van uw voorwaarden, laat ze dan juridisch toetsen."),
  ("Moet ik mijn bestaande programma vervangen?",
   "Nee. Wij vervangen uw systemen niet. Wij sluiten aan op wat u gebruikt. Welke koppeling past, bepalen we in de intake."),
  ("Wat kost offertes automatiseren?",
   "Dat hangt af van het aantal processen, de koppelingen en het onderhoud. Daarom staat hier geen bedrag. Na de intake volgt binnen één werkdag een voorstel met één vaste prijs. Lees <a href=\"wat-kost-automatisering.html\">waar de kosten van afhangen</a>."),
 ],
 "inhoud": (
  proza("korte-antwoord", "Het korte antwoord", "Wat is offertes automatiseren?",
        '<p>Offertes automatiseren is het werk rond een offerte door software laten doen, terwijl u zelf de prijs en de inhoud bepaalt. Een aanvraag komt in één lijst. Uit de gegevens van de aanvraag en uw standaardposten ontstaat een concept. U kijkt na en verstuurt. De klant ondertekent digitaal. Blijft een reactie uit, dan volgt een bericht. Het hoort bij de <a href="automatisering.html">automatisering van uw verkoop en administratie</a>.</p>') +
  pijn("herkenbaar", "De situatie", "Waar een offerte tijd kost.", "", [
   ("Beginnen bij nul", "Elke offerte begint opnieuw, ook als de klus lijkt op die van vorige maand."),
   ("Overtypen", "Naam, adres en omschrijving gaan van het bericht naar de offerte."),
   ("Opvolgen vergeten", "Een offerte blijft liggen en niemand belt terug."),
   ("Prijs en marge los", "Materiaal, uren en marge staan op drie plekken.")]) +
  krijgt("wat-er-kan", "Wat er kan", "Wat uit uw handen gaat.", "", [
   ("Aanvragen in één lijst", 'Wat de <a href="ai-telefonist.html">AI-telefonist</a> opneemt, staat er met naam, adres en aard van het werk bij.'),
   ("Een concept met uw posten", "Uw standaardposten staan klaar. U kijkt na, past aan en verstuurt."),
   ("Eén calculatie", "Materiaal, uren en marge rekent u door in één calculatie."),
   ("Digitaal ondertekenen", "De klant tekent online. Niets hoeft te worden afgedrukt."),
   ("Opvolgen", 'Reageert een klant niet, dan volgt een bericht, ook via <a href="whatsapp-automatisering.html">WhatsApp</a>.'),
   ("Naar de factuur", 'Na uitvoering staat de factuur klaar, zie <a href="facturen-automatisch-versturen.html">facturen automatisch versturen</a>.')]) +
  proza("wat-erin-hoort", "Inhoud", "Wat een offerte moet bevatten.",
        '<p>Voor een offerte bestaat geen verplichte vorm. Volgens <a href="https://ondernemersplein.overheid.nl/een-offerte-maken/" target="_blank" rel="noopener">Ondernemersplein</a>, het loket van de overheid voor ondernemers, hoort er wel een vaste inhoud in:</p>'
        '<ul><li>uw bedrijfsgegevens en die van de klant;</li><li>de datum en een offertenummer;</li><li>een samenvatting van de werkzaamheden;</li><li>het tarief of de projectprijs;</li><li>de geldigheidsduur;</li><li>afspraken over een eventuele aanbetaling;</li><li>een verwijzing naar uw algemene voorwaarden.</li></ul>'
        '<p>Zodra de klant de offerte ondertekend terugstuurt, is zij volgens dezelfde pagina een bindend contract. Een sjabloon dat deze onderdelen elke keer invult, voorkomt dat er één ontbreekt.</p>') +
  route("werkwijze", "Werkwijze", "Zo begint u.", "", [
   ("Intake", "Een half uur: hoe maakt u nu een offerte, en wat gaat nooit zonder uw akkoord de deur uit?"),
   ("Voorstel", "Binnen één werkdag op papier, met één vaste prijs."),
   ("Inrichten", "De eerste automatisering draait binnen enkele werkdagen."),
   ("Uitbreiden", "Pas als het werkt, voegen we een volgend onderdeel toe.")]) +
  proza("eigen-praktijk", "Uit eigen praktijk", "Eén keer invoeren, daarna doorlopen.",
        '<p>Bij Aronza, het e-commercebedrijf van de oprichter, werken de vijf processen op dezelfde gegevens: een order raakt voorraad, factuur en klantdossier zonder overtypen. Dat uitgangspunt nemen wij mee naar elke offerte die wij inrichten. Lees de <a href="case-aronza.html">klantcase</a>. Werkt u in de bouw of de installatietechniek, kijk dan bij <a href="ai-voor-bouw-en-installatie.html">AI en automatisering voor bouw en installatie</a>.</p>') +
  bronnen_blok([
   ("Een offerte maken, Ondernemersplein", "https://ondernemersplein.overheid.nl/een-offerte-maken/",
    "Inhoud van een offerte, geen verplichte vorm en de werking van een ondertekende offerte.")])),
}


# ───────────────────────── facturen automatisch versturen ─────────────────────────
FACTUREN = {
 "bestand": "facturen-automatisch-versturen.html",
 "soort": "gids",
 "dienst": "Facturen automatisch versturen",
 "titel": "Facturen automatisch versturen | Complete AI",
 "beschrijving": "Facturen automatisch versturen: de factuur volgt op de afgeronde klus, wie achterloopt krijgt een herinnering en de btw staat klaar. U houdt het akkoord.",
 "omschrijving": "Facturen automatisch versturen voor bedrijven in Nederland en België: de factuur volgt op de afgeronde klus, klanten betalen via een link, achterstanden krijgen een herinnering en de btw staat klaar.",
 "ogen": "Gids",
 "h1": 'Facturen automatisch versturen: <span class="glans">de factuur volgt de klus</span>.',
 "lead": 'Facturen automatisch versturen betekent dat een factuur klaarstaat zodra het werk is afgerond, dat klanten via een link kunnen betalen en dat wie achterloopt een herinnering krijgt. U bepaalt wat zonder uw akkoord de deur uitgaat. Complete AI richt dat in voor bedrijven in Nederland en België.',
 "levertijd": "Live binnen enkele werkdagen",
 "uitkomsten": [
     ("Na de klus", "de factuur wordt gemaakt en verstuurd zodra het werk is afgerond"),
     ("Herinnering", "trage betalers krijgen vanzelf een bericht"),
     ("Btw klaar", "de btw staat klaar voor de aangifte"),
 ],
 "slot_kop": "Hoe laat gaan uw facturen nu de deur uit?",
 "slot_tekst": "In een half uur nemen we uw facturatie door. Binnen één werkdag volgt een voorstel met één vaste prijs.",
 "vragen": [
  ("Wat is facturen automatisch versturen?",
   "De factuur wordt gemaakt en verstuurd zodra een klus of order is afgerond, zonder dat u de gegevens opnieuw invoert. Klanten betalen via een link en wie achterloopt krijgt een herinnering."),
  ("Welke gegevens moeten op een factuur staan?",
   "Volgens de KVK onder meer uw btw-identificatienummer en het btw-tarief, het totaalbedrag exclusief en inclusief btw, uw KVK-nummer, de factuurdatum en een doorlopend factuurnummer, de leverdatum, naam en adres van u en uw klant, een omschrijving en het aantal producten of uren."),
  ("Gaat een factuur zonder mijn akkoord de deur uit?",
   "Dat bepaalt u. Wij leggen vooraf vast wat zonder uw akkoord de deur uitgaat. Het overige loopt automatisch en is terug te lezen."),
  ("Kan ik mijn boekhoudpakket houden?",
   "Ja. Wij vervangen uw boekhouding niet, wij zorgen dat er niets met de hand ingevoerd hoeft te worden. Waar een koppeling mogelijk is leggen we die. Waar dat niet kan, hoort u dat in de intake."),
  ("Hoe werkt een herinnering aan een klant die niet betaalt?",
   "Is een factuur na de afgesproken termijn niet betaald, dan krijgt de klant een herinnering. U hoeft niet zelf te bellen. U bepaalt vooraf welke berichten zonder uw akkoord uitgaan."),
  ("Wat kost facturen automatiseren?",
   "Dat hangt af van het aantal processen, de koppelingen en het onderhoud. Daarom staat hier geen bedrag. Na de intake volgt binnen één werkdag een voorstel met één vaste prijs. Lees <a href=\"wat-kost-automatisering.html\">waar de kosten van afhangen</a>."),
 ],
 "inhoud": (
  proza("korte-antwoord", "Het korte antwoord", "Wat is facturen automatisch versturen?",
        '<p>Facturen automatisch versturen is de factuur laten volgen op het werk. Zodra een klus of order is afgerond, wordt de factuur gemaakt en verstuurd. De klant betaalt via een link. Betaalt iemand niet op tijd, dan volgt een herinnering. De btw staat klaar voor de aangifte. Het is een onderdeel van de <a href="automatisering.html">automatisering van uw administratie</a>.</p>') +
  pijn("herkenbaar", "De situatie", "Waar facturen tijd kosten.", "", [
   ("Aan het eind van de week", "Het werk is af, de factuur volgt pas als u er tijd voor heeft."),
   ("Herinneren blijft liggen", "Wie niet betaalt, hoort pas weken later iets."),
   ("Bonnetjes in een la", "Kosten worden pas bij de boekhouder uitgezocht."),
   ("Btw op het laatste moment", "Het kwartaal sluit en de cijfers moeten nog bij elkaar.")]) +
  krijgt("wat-er-kan", "Wat er kan", "Wat de facturatie voor u doet.", "", [
   ("Factuur na de klus", "De factuur wordt gemaakt en verstuurd zodra het werk is afgerond."),
   ("Betalen via een link", "Klanten betalen via een link."),
   ("Herinnering", "Trage betalers krijgen een herinnering, zonder een ongemakkelijk telefoontje."),
   ("Bonnetjes met een foto", "Een foto van het bonnetje gaat de boekhouding in."),
   ("Btw klaar", "De btw staat klaar voor de aangifte."),
   ("Naar uw boekhouder", "Met één klik een export naar Excel, PDF of uw boekhouder.")]) +
  proza("wat-erop-hoort", "Inhoud", "Wat een factuur moet bevatten.",
        '<p>Anders dan bij een offerte zijn voor een factuur wel eisen gesteld. Volgens de <a href="https://www.kvk.nl/factuur" target="_blank" rel="noopener">KVK</a> staat er in elk geval op:</p>'
        '<ul><li>uw btw-identificatienummer en het btw-tarief dat voor het product of de dienst geldt;</li><li>het totaalbedrag, zowel exclusief als inclusief btw;</li><li>uw KVK-nummer;</li><li>de factuurdatum en een factuurnummer, doorlopend genummerd;</li><li>de datum waarop u de producten of diensten hebt geleverd;</li><li>uw eigen naam en adres en die van uw klant;</li><li>een omschrijving van de geleverde producten of diensten;</li><li>het aantal producten of uren dat u in rekening brengt.</li></ul>'
        '<p>Bij internationale zaken kan extra informatie nodig zijn. De facturatie die wij inrichten rekent met de regels van het land waar u gevestigd bent: Nederland of België.</p>') +
  route("werkwijze", "Werkwijze", "Zo begint u.", "", [
   ("Intake", "Een half uur: wanneer gaat een factuur nu de deur uit, en wat mag nooit zonder uw akkoord?"),
   ("Voorstel", "Binnen één werkdag op papier, met één vaste prijs."),
   ("Inrichten", "De eerste automatisering draait binnen enkele werkdagen."),
   ("Uitbreiden", "Pas als het werkt, voegen we een volgend onderdeel toe.")]) +
  proza("eigen-praktijk", "Uit eigen praktijk", "Facturatie bij Aronza.",
        '<p>Bij Aronza, het e-commercebedrijf van de oprichter, loopt de facturatie sinds begin mei 2026 automatisch, samen met kostenregistratie, orderverwerking, voorraadbeheer en klantcontact. De administratie ging van vier tot zes uur per week naar nul, en er is geen storing geweest sinds de ingebruikname. Lees de <a href="case-aronza.html">klantcase</a>. Wilt u eerst weten welk werk bij u terugkomt, lees dan over <a href="bedrijfsprocessen-automatiseren-voorbeelden.html">processen automatiseren</a> of over <a href="offertes-automatiseren.html">offertes automatiseren</a>.</p>') +
  bronnen_blok([
   ("Een factuur maken in 4 stappen, KVK", "https://www.kvk.nl/factuur",
    "Verplichte gegevens op een factuur.")])),
}


# ───────────────────────── whatsapp business automatisch antwoorden ─────────────────────────
WHATSAPP_ANTWOORDEN = {
 "bestand": "whatsapp-business-automatisch-antwoorden.html",
 "soort": "gids",
 "dienst": "WhatsApp Business automatisch antwoorden",
 "titel": "WhatsApp Business automatisch antwoorden | Complete AI",
 "beschrijving": "WhatsApp Business automatisch antwoorden: wat de gratis app zelf kan, waar die ophoudt en wanneer een assistent op uw eigen nummer meer voor u doet.",
 "omschrijving": "WhatsApp Business automatisch antwoorden: wat een begroeting, een afwezigheidsbericht en snelle antwoorden doen, waar de app ophoudt en wat een assistent op uw eigen nummer erbij afhandelt.",
 "ogen": "Gids",
 "h1": 'WhatsApp Business automatisch antwoorden: <span class="glans">wat de app kan en wat niet</span>.',
 "lead": 'Met de gratis WhatsApp Business-app stelt u zelf een begroeting en een afwezigheidsbericht in. Dat is automatisch antwoorden in zijn eenvoudigste vorm: vaste teksten. Sinds juni 2026 biedt Meta daarnaast een eigen AI-agent aan. Complete AI richt een assistent in op uw eigen nummer, die aan uw telefoon, offertes en planning hangt.',
 "levertijd": "Ingericht na een gratis intake",
 "uitkomsten": [
     ("Gratis", "begroeting, afwezigheidsbericht en snelle antwoorden zitten in de app"),
     ("Eigen nummer", "een assistent werkt op het WhatsApp-account dat van u blijft"),
     ("Uw akkoord", "u bepaalt wat zonder uw akkoord de deur uitgaat"),
 ],
 "slot_kop": "Welke vragen krijgt u elke week?",
 "slot_tekst": "In een half uur nemen we uw berichten door. Binnen één werkdag volgt een voorstel met één vaste prijs.",
 "vragen": [
  ("Kan WhatsApp Business automatisch antwoorden?",
   "Ja. De app heeft een begroeting, een afwezigheidsbericht en snelle antwoorden: vaste teksten. Sinds juni 2026 biedt Meta daarnaast een eigen AI-agent aan die vragen beantwoordt en afspraken boekt. Een assistent van Complete AI werkt op uw eigen nummer en hangt aan de rest van uw klantcontact."),
  ("Is er een AI-agent van WhatsApp zelf?",
   "Ja. Volgens TechCrunch maakte Meta de Meta Business Agent op 3 juni 2026 wereldwijd beschikbaar in WhatsApp. Hij beantwoordt klantvragen, beveelt producten aan, boekt afspraken en kwalificeert leads, en kan een gesprek aan een mens doorgeven. Of hij voor uw account beschikbaar is en onder welke voorwaarden, bepaalt Meta."),
  ("Hoe stelt u een begroeting in?",
   "Open in de WhatsApp Business-app het tabblad Tools en kies Begroeting. Schakel het verzenden in, pas de tekst aan, kies bij Ontvangers wie het bericht krijgt en tik op Opslaan. Het afwezigheidsbericht vindt u in hetzelfde tabblad."),
  ("Wanneer krijgt een klant de begroeting?",
   "Volgens het WhatsApp-helpcentrum wanneer een klant u voor het eerst een bericht stuurt, en opnieuw na 14 dagen inactiviteit in de chat. Heeft de klant u de afgelopen 14 dagen geschreven, dan volgt geen begroeting."),
  ("Werkt het ook als mijn telefoon uit staat?",
   "Nee. Volgens het WhatsApp-helpcentrum moet het toestel een actieve internetverbinding hebben om begroetingen te verzenden."),
  ("Kan ik mijn eigen WhatsApp-nummer houden?",
   "Ja. Het account blijft van u. Welke koppeling bij uw situatie past, bepalen we in de intake."),
  ("Wat kost het?",
   "Dat hangt af van uw situatie. Na de intake volgt binnen één werkdag een voorstel met één vaste prijs."),
 ],
 "inhoud": (
  proza("korte-antwoord", "Het korte antwoord", "Kan WhatsApp Business automatisch antwoorden?",
        '<p>Ja. De gratis WhatsApp Business-app stuurt een begroeting naar klanten die u voor het eerst schrijven, een afwezigheidsbericht wanneer u niet bereikbaar bent, en u kunt snelle antwoorden bewaren voor vragen die terugkomen. Het zijn vaste teksten. Een antwoord op een vraag, een afspraak of een opvolging valt buiten die drie functies. Daarvoor bestaan de <a href="#meta-agent">AI-agent van Meta</a> en <a href="whatsapp-automatisering.html">WhatsApp-automatisering</a> met een assistent van Complete AI.</p>') +
  krijgt("wat-de-app-kan", "Wat de app kan", "Drie functies in de gratis app.", "", [
   ("Begroeting", "Een bericht dat automatisch naar klanten gaat die u voor het eerst schrijven, en opnieuw na 14 dagen inactiviteit."),
   ("Afwezigheidsbericht", "Een vaste tekst wanneer u niet bereikbaar bent. U vindt hem in het tabblad Tools."),
   ("Snelle antwoorden", "Teksten die u zelf bewaart en in een gesprek kiest, voor vragen die steeds terugkomen.")]) +
  pijn("grens", "De grens", "Waar de drie vaste functies ophouden.", "", [
   ("Dezelfde tekst", "Iedereen krijgt hetzelfde bericht, wat hij ook vraagt."),
   ("Geen antwoord op een vraag", "Wie om openingstijden of beschikbaarheid vraagt, wacht op u."),
   ("Geen afspraak", "Een afspraak wordt niet vastgelegd of bevestigd."),
   ("Geen opvolging", "Een offerte zonder reactie blijft liggen."),
   ("Toestel moet online zijn", "Zonder internetverbinding op uw telefoon gaat er niets uit.")]) +
  proza("meta-agent", "De agent van Meta", "En de AI-agent van WhatsApp zelf?",
        '<p>Volgens <a href="https://www.techcrunch.com/2026/06/03/metas-ai-agent-for-whatsapp-business-is-now-available-globally/" target="_blank" rel="noopener">TechCrunch</a> maakte Meta de Meta Business Agent op 3 juni 2026 wereldwijd beschikbaar in WhatsApp. De agent beantwoordt klantvragen, beveelt producten aan, boekt afspraken en kwalificeert leads, en kan een vraag doorzetten naar een mens. Meta wil hem onderbrengen in sommige abonnementen van WhatsApp Business Premium.</p>'
        '<p>Volgens het <a href="https://faq.whatsapp.com/501866148528310/" target="_blank" rel="noopener">WhatsApp-helpcentrum</a> worden begroetingen automatisch uitgeschakeld zodra de Meta Business Agent is gekoppeld. De twee werken dus niet naast elkaar. U kiest tussen de vaste teksten van de app, de agent van Meta en een assistent van Complete AI.</p>') +
  krijgt("wat-een-assistent-doet", "Met een assistent", "Wat een assistent op uw nummer erbij doet.", "", [
   ("Antwoorden", "Veelgestelde vragen krijgen direct antwoord, ook buiten openingstijden."),
   ("Afspraken", "Bevestiging en herinnering gaan uit, en de afspraak staat in uw agenda."),
   ("Offertes opvolgen", 'Blijft een reactie uit, dan volgt een vriendelijk bericht, zie <a href="offertes-automatiseren.html">offertes automatiseren</a>.'),
   ("Doorzetten naar u", "Wat een mens nodig heeft, komt met de vraag erbij bij u terecht."),
   ("Eén overzicht", 'Alle berichten staan per klant bij elkaar, met telefoon en mail erbij, samen met de <a href="ai-telefonist.html">AI-telefonist</a>.')]) +
  proza("welke-past", "Kiezen", "Wanneer is de app genoeg?",
        '<p>Krijgt u weinig berichten en steeds dezelfde vraag, dan volstaat de app: stel de begroeting en het afwezigheidsbericht in. Komen er elke week berichten binnen die een antwoord, een afspraak of een opvolging vragen, dan neemt een assistent dat werk over. Wat een assistent van Complete AI toevoegt, is dat WhatsApp aan de rest van uw klantcontact hangt: de telefoon, de offertes en de planning, met alle berichten per klant bij elkaar. Dat hoort u in de intake, ook wanneer de conclusie is dat de app voor u genoeg is. Meer over <a href="automatisering.html">automatisering van klantcontact</a> staat bij de diensten.</p>') +
  proza("regels", "Toestemming en privacy", "Berichten sturen met toestemming.",
        '<p>Een bericht dat u zelf aan een klant start, vraagt om toestemming van die klant. Wij leggen die toestemming vast. Omdat berichten persoonsgegevens bevatten, regelen wij vóór de start een verwerkersovereenkomst, zoals de AVG voorschrijft.</p>') +
  bronnen_blok([
   ("Begroetingen gebruiken, WhatsApp-helpcentrum", "https://faq.whatsapp.com/501866148528310/",
    "Wanneer een begroeting wordt verzonden, de 14 dagen en de eis van een internetverbinding."),
   ("Het gebruiken van afwezigheidsberichten, WhatsApp-helpcentrum", "https://faq.whatsapp.com/2565868990219715/",
    "Het afwezigheidsbericht in de WhatsApp Business-app."),
   ("Het gebruik van snelle antwoorden, WhatsApp-helpcentrum", "https://faq.whatsapp.com/1791149784551042/",
    "Snelle antwoorden in de WhatsApp Business-app."),
   ("Meta’s AI agent for WhatsApp Business is now available globally, TechCrunch (3 juni 2026)", "https://www.techcrunch.com/2026/06/03/metas-ai-agent-for-whatsapp-business-is-now-available-globally/",
    "Wat de Meta Business Agent doet en wanneer hij beschikbaar kwam.")])),
}

KOPER = [OFFERTES, FACTUREN, WHATSAPP_ANTWOORDEN]
