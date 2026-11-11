"""Korte, pakkende tekst van de dienst- en gidspagina's (Glenn, 11-10-2026: herschrijf alles korter en pakkender).
Per pagina: de onderdelen (inhoud), de vragen en de slotregel. Alles andere (kop, voet, structuurdata) komt uit bouw-paginas.py."""

def _sectie(sid, label, h2, intro, kern):
    i = f"\n        <p>{intro}</p>" if intro else ""
    return f'''<section id="{sid}">
    <div class="wrap">
      <div class="sectiekop reveal">
        <p class="label"><i></i>{label}</p>
        <h2>{h2}</h2>{i}
      </div>
      {kern}
    </div>
  </section>
  '''

def pijn(sid, label, h2, intro, items):
    a = "\n        ".join(f'<article><span class="nr">{n:02d}</span><p>{t}</p><small>{x}</small></article>' for n, (t, x) in enumerate(items, 1))
    return _sectie(sid, label, h2, intro, f'<div class="pijn reveal">\n        {a}\n      </div>')

def krijgt(sid, label, h2, intro, items):
    a = "\n        ".join(f'<article><h3>{t}</h3><p>{x}</p></article>' for t, x in items)
    return _sectie(sid, label, h2, intro, f'<div class="krijgt reveal">\n        {a}\n      </div>')

def route(sid, label, h2, intro, items):
    a = "\n        ".join(f'<div class="fase"><i>Stap {n}</i><b>{t}</b><p>{x}</p></div>' for n, (t, x) in enumerate(items, 1))
    return _sectie(sid, label, h2, intro, f'<div class="route reveal">\n        {a}\n      </div>')

def proza(sid, label, h2, tekst):
    return _sectie(sid, label, h2, "", f'<div class="proza reveal">\n        {tekst}\n      </div>')

KORT = {}

# ───────────────────────── websites ─────────────────────────
KORT["websites.html"] = dict(
 inhoud=(
  pijn("herkenbaar", "De situatie", "Een mooie site brengt nog geen klanten.", "Dit zien wij terug bij een bestaande website.", [
   ("Niet bijgehouden", "Teksten, openingstijden en diensten zijn verouderd."),
   ("Traag op mobiel", "Wie wacht op een pagina, haakt af. Google noemt 2,5 seconden als grens."),
   ("Geen vervolgstap", "De bezoeker kijkt rond en vertrekt zonder contact op te nemen."),
   ("Wijzigingen duren te lang", "Daardoor blijven ze uit en veroudert de site.")]) +
  krijgt("wat-u-krijgt", "Wat u krijgt", "Alles in één keer geregeld.", "Eén aanspreekpunt, en aan het eind staat er iets dat af is.", [
   ("Ontwerp op maat", "Geen sjabloon met een logo erin, maar een ontwerp dat uw bedrijf en klanten volgt."),
   ("Mobiel eerst", "Ontworpen op telefoonformaat. Google beoordeelt de mobiele versie."),
   ("Snel", "Geen zware paginabouwers. Deze pagina laadt in ongeveer 0,7 seconde; dat is de norm."),
   ("Teksten die kloppen", "Geschreven na één gesprek, in uw taal en voor uw klant."),
   ("Gekoppeld aan uw werk", 'Contactformulier, agenda en berichten komen rechtstreeks bij u binnen, ook via <a href="whatsapp-automatisering.html">WhatsApp</a>.'),
   ("Hosting en onderhoud", "Hosting, back-ups, updates en kleine wijzigingen zitten in het maandbedrag. Maandelijks opzegbaar.")]) +
  route("twee-weken", "Werkwijze", "Van eerste gesprek tot live in twee weken.", "", [
   ("Intake", "Een half uur. Kosteloos en vrijblijvend."),
   ("Voorstel", "Binnen één werkdag op papier, met één vaste prijs."),
   ("Teksten", "Eén gesprek. Daaruit schrijven wij alles."),
   ("Bouwen", "U kijkt mee via een link en stuurt gaandeweg bij."),
   ("Live", "Wij koppelen domein en e-mail en nemen alles met u door.")]) +
  proza("maatwerk", "Maatwerk of sjabloon", "Sjabloon of maatwerk?", '<p>Een sjabloon is een kant-en-klaar ontwerp met uw inhoud erin. Maatwerk volgt uit uw bedrijf en kan precies wat u nodig heeft, zoals online boeken. Wij bouwen maatwerk en houden het licht, zodat het snel blijft. Wilt u meer dan een website, dan sluiten <a href="automatisering.html">automatisering</a> van uw klantcontact en de <a href="ai-telefonist.html">AI-telefonist</a> daarop aan.</p>')),
 vragen=[
  ("Wat kost het om een website te laten maken?", "Dat hangt af van het aantal pagina’s, de functies, wie de teksten en het beeld levert en het onderhoud. Daarom noemen wij vooraf geen bedrag. Na de intake ligt er binnen één werkdag een voorstel met één vaste prijs."),
  ("Hoe lang duurt het?", "Van akkoord tot live één tot twee weken, inclusief teksten."),
  ("Wat moet ik zelf aanleveren?", "Een half uur voor de intake, één gesprek voor de teksten en foto’s van uw werk, team en locatie."),
  ("Kan ik zelf iets wijzigen?", "Kleine wijzigingen doen wij, binnen één werkdag. Wilt u zelf wijzigen, dan bespreken we dat vooraf."),
  ("Zit ik vast aan een contract?", "Nee. Het maandbedrag voor hosting en onderhoud is maandelijks opzegbaar.")],
 slot_kop="Wat kan uw website opleveren?",
 slot_tekst="In een half uur nemen we door wat er nu staat en waar het misloopt. Binnen één werkdag volgt een voorstel met één vaste prijs.",
)

# ───────────────────────── automatisering ─────────────────────────
KORT["automatisering.html"] = dict(
 inhoud=(
  proza("korte-antwoord", "Het korte antwoord", "Wat is automatisering voor bedrijven?", '<p>Automatisering voor bedrijven is software die terugkerende stappen uitvoert: een telefoontje opnemen, een WhatsApp-bericht beantwoorden, een offerte opvolgen, een factuur versturen. Dat past bij werk dat elke week terugkomt, een vaste volgorde heeft en een uitkomst geeft die u kunt controleren. Een overzicht per afdeling staat bij de <a href="bedrijfsprocessen-automatiseren-voorbeelden.html">voorbeelden</a>.</p>') +
  pijn("herkenbaar", "De situatie", "Werk dat tijd kost en niets oplevert.", "", [
   ("Overtypen", "Dezelfde gegevens gaan van de mail naar het systeem naar de factuur."),
   ("Opvolgen vergeten", "Een offerte blijft liggen, een betaling blijft uit."),
   ("Berichten blijven liggen", "Telefoon, WhatsApp en mail komen op drie plekken binnen."),
   ("Alles hangt aan u", "Zodra u uitvalt, staat het werk stil.")]) +
  krijgt("wat-er-kan", "Wat wij automatiseren", "Zes onderdelen van uw bedrijf, afzonderlijk of samen.", "Wij beginnen bij het onderdeel dat de meeste uren kost.", [
   ("Klantcontact", 'De <a href="ai-telefonist.html">AI-telefonist</a> neemt op, <a href="whatsapp-automatisering.html">WhatsApp-berichten</a> worden beantwoord, gemiste oproepen worden terugbelverzoeken en een vragen-assistent op uw website antwoordt direct.'),
   ("Verkoop en offertes", "Aanvragen komen in één lijst. Offertes worden opgesteld, verstuurd, digitaal ondertekend en opgevolgd. Materiaal, uren en marge rekent u door in één calculatie."),
   ("Planning", "Klanten boeken zelf online, met herinnering vooraf. Vrijgekomen plekken gaan naar de wachtlijst. Klussen, routes en werkbonnen staan op de telefoon."),
   ("Facturen en geld", "Facturen worden gemaakt en verstuurd, trage betalers krijgen een herinnering. Klanten betalen via een link, bonnetjes gaan met een foto de boekhouding in en de btw staat klaar."),
   ("Klanten en reviews", "Klantenbestand met historie, een logboek van elk bericht en gesprek per klant, een klantportaal en een verzoek om een beoordeling na afloop."),
   ("Overzicht", "Omzet en kerncijfers op één scherm, elke week vanzelf een overzicht en met één klik een export naar Excel, PDF of uw boekhouder.")]) +
  route("werkwijze", "Werkwijze", "Beginnen waar de winst het grootst is.", "", [
   ("Intake", "Een half uur: welke taken komen elke week terug, en wat mag nooit zonder uw akkoord de deur uit?"),
   ("Voorstel", "Binnen één werkdag op papier, met één vaste prijs."),
   ("Inrichten", "De eerste automatisering draait binnen enkele werkdagen."),
   ("Uitbreiden", "Pas als het werkt, voegen we een volgend onderdeel toe.")]) +
  proza("koppelingen", "Koppelingen", "Wij vervangen uw systemen niet.", '<p>Wij sluiten aan op wat u gebruikt: uw boekhouding, uw agenda, WhatsApp en uw telefonie. Welke koppeling past, bepalen we in de intake.</p>')),
 vragen=[
  ("Wat kost automatisering?", 'Dat hangt af van het aantal processen, de koppelingen en het onderhoud. Daarom staat hier geen bedrag. Lees <a href="wat-kost-automatisering.html">waar de kosten van afhangen</a>.'),
  ("Moet ik mijn systemen vervangen?", "Nee. Wij koppelen aan wat u al gebruikt."),
  ("Welke bedrijven kunnen hun werk automatiseren?", "Elk bedrijf met werk dat elke week terugkomt: aanvragen, offertes, afspraken, facturen en berichten. De intake laat zien waar het meeste te winnen is."),
  ("Wat als er iets misgaat?", "U bepaalt vooraf wat zonder uw akkoord de deur uitgaat. Het overige loopt automatisch en is terug te lezen."),
  ("Zit ik vast aan een contract?", "Nee. Het onderhoud is maandelijks opzegbaar.")],
 slot_kop="Waar gaat bij u tijd verloren?",
 slot_tekst="In een half uur brengen we dat in kaart. Binnen één werkdag volgt een voorstel met één vaste prijs.",
)

# ───────────────────────── ai-telefonist ─────────────────────────
KORT["ai-telefonist.html"] = dict(
 inhoud=(
  proza("wat-is-het", "Uitleg", "Een gesprek in plaats van een voicemail.", '<p>Een AI-telefonist voert het telefoongesprek zelf. Hij verstaat wat de beller vraagt en antwoordt in gesproken Nederlands. Aan het eind staat vast wat is afgesproken: een bestelling in de orderlijst, een terugbelnotitie met de vraag erin, of een gesprek dat naar u is doorgeschakeld. Bij een voicemail blijft de beller met zijn vraag zitten.</p>') +
  pijn("herkenbaar", "De situatie", "Elk gemist gesprek is een klant die de volgende belt.", "", [
   ("Buiten openingstijden", "De telefoon gaat op het moment dat u niet kunt opnemen."),
   ("Tijdens drukte", "Wie aan het werk is, kan niet bellen."),
   ("Verkopers", "Ongewenste gesprekken kosten tijd."),
   ("Geen overzicht", "Wat er is gevraagd, staat nergens genoteerd.")]) +
  krijgt("zo-klinkt-het", "Wat hij doet", "Wat de AI-telefonist voor u afhandelt.", "", [
   ("Opnemen", "Op uw eigen nummer, buiten openingstijden en tijdens drukte."),
   ("Vastleggen", "Bestellingen en vragen komen gestructureerd in uw lijst."),
   ("Inplannen", "Afspraken gaan rechtstreeks in uw agenda."),
   ("Doorschakelen", "Urgente gesprekken gaan direct naar u."),
   ("Meertalig", "Nederlands, en waar nodig Vlaams, Frans en Engels."),
   ("Terug te lezen", "Van elk gesprek is een transcript beschikbaar.")]) +
  route("agenda-doorschakelen", "Werkwijze", "Binnen twee weken operationeel.", "", [
   ("Intake", "Wat mag hij zelfstandig afhandelen en wat gaat altijd naar u?"),
   ("Inrichten", "Uw nummer, uw gegevens en uw agenda worden gekoppeld."),
   ("Meekijken", "De eerste weken kijken wij mee en sturen wij bij.")]) +
  proza("veiligheid-avg", "Veiligheid en regels", "Veilig en volgens de regels.", '<p>Een telefoongesprek bevat persoonsgegevens. Daarom leggen wij vóór de start een verwerkersovereenkomst vast, zoals de AVG voorschrijft. Uw gegevens blijven van u en worden nooit doorverkocht. Sinds 2 augustus 2026 moet duidelijk zijn dat een beller met AI te maken heeft (artikel 50 van de AI-verordening). De AI-telefonist meldt zich daarom als digitale assistent. Meer over de techniek staat bij <a href="ai-agent-voor-uw-bedrijf.html">AI-agents</a>.</p>')),
 vragen=[
  ("Wat als de AI-telefonist iets verkeerd doet?", "U bepaalt vooraf wat hij zelfstandig afhandelt. Van elk gesprek is een transcript, en de eerste weken kijken wij mee."),
  ("Hoort de beller dat het AI is?", "Ja. Hij meldt zich als digitale assistent van uw bedrijf."),
  ("Werkt het op mijn eigen nummer?", "Ja. Hij neemt op uw nummer op, buiten openingstijden en tijdens drukte."),
  ("Wat kost het?", "Dat hangt af van uw situatie. Na de intake volgt binnen één werkdag een voorstel met één vaste prijs."),
  ("Zit ik vast aan een contract?", "Nee. Het abonnement is maandelijks opzegbaar.")],
 slot_kop="Wilt u horen hoe het klinkt?",
 slot_tekst="In een half uur nemen we uw situatie door. U hoort daarna hoe uw telefonist klinkt.",
)

# ───────────────────────── whatsapp-automatisering ─────────────────────────
KORT["whatsapp-automatisering.html"] = dict(
 inhoud=(
  proza("wat-is-het", "Uitleg", "Wat is WhatsApp-automatisering?", '<p>WhatsApp-automatisering handelt berichten van klanten af zonder dat u erbij hoeft te zijn. Een assistent beantwoordt veelgestelde vragen, legt afspraken vast, stuurt herinneringen en volgt offertes op. Heeft een bericht een mens nodig, dan zet hij het met de vraag erbij door naar u. Elk bericht komt in het logboek van de klant, naast telefoon en mail.</p>') +
  pijn("herkenbaar", "De situatie", "Berichten blijven liggen terwijl u aan het werk bent.", "", [
   ("Buiten kantooruren", "Een vraag om 21.00 uur krijgt pas de volgende dag antwoord."),
   ("Dezelfde vragen", "Openingstijden, werkwijze en beschikbaarheid, elke week opnieuw."),
   ("Op meerdere plekken", "Berichten staan op een telefoon, in de mail en in een notitie."),
   ("Herinneringen vergeten", "Een afspraak of offerte wordt niet opgevolgd.")]) +
  krijgt("wat-hij-doet", "Wat hij doet", "Wat de WhatsApp-assistent voor u afhandelt.", "", [
   ("Antwoorden", "Veelgestelde vragen krijgen direct antwoord, ook buiten openingstijden."),
   ("Afspraken", "Bevestiging en herinnering gaan uit, en de afspraak staat in uw agenda."),
   ("Offertes opvolgen", "Blijft een reactie uit, dan volgt een vriendelijk bericht."),
   ("Doorzetten naar u", "Wat een mens nodig heeft, komt met de vraag erbij bij u terecht."),
   ("Eén overzicht", "Alle berichten staan per klant bij elkaar, met telefoon en mail erbij."),
   ("Terugbelverzoeken", 'Gemiste oproepen worden een lijstje, samen met de <a href="ai-telefonist.html">AI-telefonist</a>.')]) +
  route("werkwijze", "Werkwijze", "Van intake tot meekijken.", "", [
   ("Intake", "Welke vragen komen steeds terug, en wat mag nooit zonder uw akkoord de deur uit?"),
   ("Koppelen", "Uw eigen WhatsApp-nummer wordt gekoppeld. Het account blijft van u."),
   ("Meekijken", "De eerste weken lezen wij mee en sturen wij bij.")]) +
  proza("regels", "Toestemming en privacy", "Berichten sturen met toestemming.", '<p>Een bericht dat u zelf aan een klant start, vraagt om toestemming van die klant. Wij leggen die toestemming vast. Omdat berichten persoonsgegevens bevatten, regelen wij vóór de start een verwerkersovereenkomst, zoals de AVG voorschrijft. Meer over het geheel van klantcontact staat bij <a href="automatisering.html">automatisering</a>.</p>')),
 vragen=[
  ("Wat is WhatsApp-automatisering voor bedrijven?", "Software die WhatsApp-berichten van klanten afhandelt: vragen beantwoorden, afspraken vastleggen, herinneringen sturen en offertes opvolgen. Wat een mens nodig heeft, gaat naar u door."),
  ("Kan ik mijn eigen WhatsApp-nummer houden?", "Ja. Het account blijft van u. Welke koppeling bij uw situatie past, bepalen we in de intake."),
  ("Wat als de assistent iets niet weet?", "Dan verzint hij niets. Hij zet de vraag voor u klaar, zodat niemand hoeft te raden wat de klant bedoelde."),
  ("Wat kost het?", "Dat hangt af van uw situatie. Na de intake volgt binnen één werkdag een voorstel met één vaste prijs."),
  ("Zit ik vast aan een contract?", "Nee. Het abonnement is maandelijks opzegbaar.")],
 slot_kop="Welke vragen krijgt u elke week?",
 slot_tekst="In een half uur nemen we uw berichten door. Binnen één werkdag volgt een voorstel met één vaste prijs.",
)

# ───────────────────────── gidsen ─────────────────────────
KORT["ai-voor-uw-bedrijf.html"] = dict(
 inhoud=(
  proza("kort-antwoord", "Het korte antwoord", "Wat kan AI voor uw bedrijf?", '<p>AI neemt werk over dat elke week terugkomt: gegevens verwerken, de telefoon en berichten beantwoorden, herinneringen versturen en cijfers bijhouden. Wat het voor u kan doen, hangt af van dat werk. Bij Aronza, het e-commercebedrijf van de oprichter, ging de administratie zo van vier tot zes uur per week naar nul. Lees de <a href="case-aronza.html">klantcase</a>.</p>') +
  krijgt("wat-is-ai", "Wat is AI", "Drie manieren waarop AI werkt voor een mkb-bedrijf.", "", [
   ("Gegevens verwerken", "Facturen, bonnen en orders worden gelezen, geordend en vastgelegd."),
   ("Communiceren", 'Telefoon en berichten worden beantwoord, zoals bij de <a href="ai-telefonist.html">AI-telefonist</a>.'),
   ("Opvolgen", "Herinneringen en vervolgstappen gaan op tijd uit, zonder dat u eraan denkt.")]) +
  route("beginnen", "Beginnen", "Zo begint u zonder risico.", "", [
   ("Kies één taak", "Neem een week op wat terugkomt en kies wat de meeste uren kost."),
   ("Stel grenzen", "Bepaal wat nooit zonder uw akkoord de deur uitgaat."),
   ("Begin klein", "Laat één onderdeel draaien voor u het volgende toevoegt."),
   ("Meet", "Kijk na een maand wat het scheelt.")]) +
  proza("grens", "De grens", "Wat AI niet voor u beslist.", '<p>U bepaalt wat zonder uw akkoord de deur uitgaat. Wij leggen dat vooraf vast. Wilt u weten welke onderdelen er bestaan, kijk dan bij <a href="automatisering.html">automatisering</a> of lees <a href="ai-agent-voor-uw-bedrijf.html">wat een AI-agent is</a>.</p>')),
 vragen=[
  ("Is AI iets voor een klein bedrijf?", "Ja, als er werk is dat elke week terugkomt."),
  ("Wat moet ik doen om te beginnen?", "Een gesprek van een half uur. Daaruit volgt waar het meeste te winnen is."),
  ("Wat als AI iets verkeerd doet?", "U bepaalt vooraf wat zelfstandig gebeurt. Alles is terug te lezen."),
  ("Wat kost het?", "Dat hangt af van uw situatie. Na de intake volgt een voorstel met één vaste prijs."),
  ("Is mijn data veilig?", "Uw gegevens blijven van u. Wij leggen de afspraken vast in een verwerkersovereenkomst.")],
 slot_kop="Wat kan AI in uw situatie?",
 slot_tekst="In een half uur nemen we uw werk door. U ontvangt een eerlijk advies, ook als het kleiner uitvalt dan u hoopte.",
)

KORT["bedrijfsprocessen-automatiseren-voorbeelden.html"] = dict(
 inhoud=(
  proza("wat-is-een-bedrijfsproces", "Uitleg", "Wat is een bedrijfsproces?", '<p>Een bedrijfsproces is een vaste reeks stappen met een uitkomst, zoals een order verwerken of een factuur versturen. Het komt terug, heeft een vaste volgorde en een uitkomst die u kunt controleren. Daar past <a href="automatisering.html">automatisering</a> bij.</p>') +
  krijgt("klanten-verkoop", "Voorbeelden", "Per onderdeel van uw bedrijf.", "", [
   ("Klanten en verkoop", "Aanvragen uit alle kanalen komen in één lijst. De offerte staat binnen één werkdag klaar en wordt automatisch opgevolgd."),
   ("Planning", "Klanten plannen zelf in, ook buiten openingstijden. Bevestiging en herinnering gaan vooraf uit."),
   ("Bereikbaarheid", 'De <a href="ai-telefonist.html">AI-telefonist</a> neemt op en legt vast wat nodig is.'),
   ("Financiën", "De factuur volgt automatisch na afronding. Betaalherinneringen gaan uit zonder ongemakkelijk telefoontje."),
   ("Boekhouding", "Bonnen en kosten gaan rechtstreeks de boekhouding in."),
   ("Marketing", "Klanten krijgen na afloop een verzoek om een beoordeling.")]) +
  route("herkennen", "Herkennen", "Welk proces komt het eerst in aanmerking?", "", [
   ("Het komt terug", "Het gebeurt elke week of vaker."),
   ("De volgorde staat vast", "Er is een begin, stappen en een uitkomst."),
   ("U kunt het controleren", "Een fout is snel te zien."),
   ("Het kost uren", "Neem een week lang op hoeveel.")]) +
  proza("waar-begint-u", "Beginnen", "Waar begint u?", '<p>Kies het proces dat de meeste uren kost en begin daar. Wat het kost, hangt af van het werk, zie <a href="wat-kost-automatisering.html">wat automatisering kost</a>. Wilt u eerst het begrip scherp, lees dan <a href="wat-is-workflow-automatisering.html">wat workflow automatisering is</a>.</p>')),
 vragen=[
  ("Welke processen kan ik het best automatiseren?", "Processen die terugkomen, een vaste volgorde hebben en een controleerbare uitkomst geven."),
  ("Waar begin ik?", "Bij het proces dat de meeste uren kost."),
  ("Moet ik mijn systemen vervangen?", "Nee. Wij koppelen aan wat u gebruikt."),
  ("Hoe snel draait de eerste automatisering?", "Binnen enkele werkdagen."),
  ("Wat kost het?", "Dat hangt af van het werk. Na de intake volgt een voorstel met één vaste prijs.")],
 slot_kop="Welk proces kost u de meeste tijd?",
 slot_tekst="In een half uur zoeken we dat uit. Binnen één werkdag volgt een voorstel.",
)

KORT["wat-is-workflow-automatisering.html"] = dict(
 inhoud=(
  proza("korte-antwoord", "Het korte antwoord", "Wat is workflow automatisering?", '<p>Een workflow is een vaste reeks stappen: een aanleiding, stappen, voorwaarden en een uitkomst. Een order die voorraad, factuur en klantdossier bijwerkt is een voorbeeld. Workflow automatisering laat software die stappen uitvoeren, zodat het werk vanzelf van de ene naar de volgende gaat. Voorbeelden per afdeling staan bij <a href="bedrijfsprocessen-automatiseren-voorbeelden.html">bedrijfsprocessen automatiseren</a>.</p>') +
  krijgt("taak-workflow-proces", "Begrippen", "Taak, workflow en proces.", "", [
   ("Taak", "Eén handeling, zoals een factuur versturen."),
   ("Workflow", "Een reeks stappen die samen een uitkomst geven."),
   ("Proces", "Het geheel van workflows rond één doel, zoals orderverwerking.")]) +
  krijgt("opbrengst", "Opbrengst", "Wat het oplevert.", "", [
   ("Tijd", "Het overtypen en onthouden vallen weg."),
   ("Minder fouten", "Elke stap verloopt op dezelfde manier."),
   ("Snelheid", "Een klant krijgt direct een bevestiging."),
   ("Overzicht", "Wat is gedaan, staat vast.")]) +
  route("beginnen-meten", "Beginnen", "Zo pakt u het aan.", "", [
   ("Kies één proces", "Het proces dat de meeste uren kost."),
   ("Zet het op papier", "Aanleiding, stappen, voorwaarden en uitkomst."),
   ("Automatiseer", "Eerst het stuk dat vaststaat. Behoud zelf de keuzes die oordeel vragen."),
   ("Meet", "Vergelijk de tijd voor en na.")]) ),
 vragen=[
  ("Wat is het verschil met RPA?", "RPA volgt vaste regels op het scherm na. AI herkent daarnaast patronen in gegevens. Ze werken ook samen."),
  ("Heb ik er een IT-afdeling voor nodig?", "Nee. Wij richten het in en koppelen aan uw systemen."),
  ("Hoe snel draait het?", "De eerste workflow binnen enkele werkdagen."),
  ("Wat kost het?", 'Dat hangt af van het werk. Zie <a href="wat-kost-automatisering.html">wat automatisering kost</a>.'),
  ("Wat als er iets misgaat?", "U bepaalt vooraf wat zonder uw akkoord de deur uitgaat.")],
 slot_kop="Welke workflow past bij u?",
 slot_tekst="In een half uur kijken we naar het werk dat terugkomt. Binnen één werkdag volgt een voorstel.",
)

KORT["ai-agent-voor-uw-bedrijf.html"] = dict(
 inhoud=(
  proza("wat-is-het", "Uitleg", "Wat is een AI-agent?", '<p>Een AI-agent is software waarin een taalmodel zelf bepaalt welke stappen een taak vraagt en welke koppelingen het gebruikt, zoals uw agenda of boekhouding. Voor een mkb-bedrijf is dat software die één afgebakende taak van u overneemt, zoals de telefoon opnemen en een afspraak inplannen. Een voorbeeld is de <a href="ai-telefonist.html">AI-telefonist</a>.</p>') +
  krijgt("taken", "Taken", "Wat een agent kan overnemen.", "", [
   ("Telefoon", "Opnemen, vragen beantwoorden en afspraken inplannen."),
   ("Berichten", "Aanvragen ontvangen, ordenen en beantwoorden."),
   ("Administratie", "Gegevens lezen, vastleggen en klaarzetten."),
   ("Opvolgen", "Herinneringen versturen en vervolgstappen bewaken.")]) +
  proza("de-wet", "Regels", "De regels die gelden.", '<p>Een agent die met mensen praat, moet zich bekendmaken als AI (artikel 50 van de AI-verordening, van toepassing sinds 2 augustus 2026). Verwerkt hij persoonsgegevens, dan eist de AVG een schriftelijke verwerkersovereenkomst. Complete AI legt dat vóór de start vast.</p>') +
  route("beginnen", "Beginnen", "Klein beginnen.", "", [
   ("Kies één taak", "Een afgebakende taak die elke week terugkomt."),
   ("Stel grenzen", "Wat gaat zonder uw akkoord de deur uit?"),
   ("Laat meekijken", "De eerste weken kijken wij mee."),
   ("Breid uit", "Pas als het werkt, volgt een volgende taak.")]) ),
 vragen=[
  ("Wat is het verschil met een chatbot?", "Een agent voert taken uit met uw systemen. Een chatbot beantwoordt vooral vragen."),
  ("Wat als de agent iets verkeerd doet?", "U bepaalt vooraf wat zelfstandig gebeurt. Alles is terug te lezen."),
  ("Wat heb ik nodig om te beginnen?", "Een gesprek van een half uur en één taak waarmee u wilt beginnen."),
  ("Is het veilig?", "Uw gegevens blijven van u. Wij leggen de afspraken vast in een verwerkersovereenkomst."),
  ("Wat kost het?", 'Dat hangt af van de taak. Zie <a href="wat-kost-automatisering.html">wat automatisering kost</a>.')],
 slot_kop="Welke taak kan een agent van u overnemen?",
 slot_tekst="In een half uur nemen we dat door. Binnen één werkdag volgt een voorstel. Zie ook <a href=\"ai-voor-uw-bedrijf.html\">wat AI voor uw bedrijf kan</a>.",
)

KORT["wat-kost-automatisering.html"] = dict(
 inhoud=(
  proza("korte-antwoord", "Het korte antwoord", "Wat kost automatisering?", '<p>Automatisering kost het werk om haar voor uw bedrijf in te richten, te koppelen, te testen en bij te houden. Dat verschilt per bedrijf, daarom staat hier geen bedrag. De kosten bestaan uit twee delen: een eenmalig deel voor het inrichten en een vast maandbedrag voor onderhoud en bijsturing. Zie ook <a href="automatisering.html">wat wij automatiseren</a>.</p>') +
  krijgt("factoren", "Factoren", "Vijf dingen bepalen het voorstel.", "", [
   ("Aantal processen", "Elk proces wordt apart ingericht en getest."),
   ("Koppelingen", "Hoe meer systemen, hoe meer werk."),
   ("Uitzonderingen", "Elke afwijking in uw werkwijze moet worden ingebouwd."),
   ("Goedkeuring", "Wat u zelf wilt goedkeuren, bouwen wij in."),
   ("Onderhoud", "Het maandbedrag voor bijsturen en onderhoud.")]) +
  route("voorstel", "Werkwijze", "Zo komt een voorstel tot stand.", "", [
   ("Intake", "Een half uur, kosteloos en vrijblijvend."),
   ("Voorstel", "Binnen één werkdag op papier, met één vaste prijs en zonder nacalculatie."),
   ("Uw keuze", "U beslist of en waarmee wij beginnen."),
   ("Uitbreiden", "Pas als het werkt, volgt een volgend onderdeel.")]) +
  proza("laag-houden", "Beheersen", "Zo houdt u de kosten beheersbaar.", '<p>Begin met één proces. Leg de aannames vast, en kies de goedkoopste route die betrouwbaar werkt. Ruim uw gegevens op voordat u koppelt. Een dubbel klantenbestand blijft dubbel. Neem een week lang op welke taken terugkomen, zie <a href="bedrijfsprocessen-automatiseren-voorbeelden.html">de voorbeelden</a>.</p>')),
 vragen=[
  ("Waarom staat er geen prijs?", "Het werk verschilt per bedrijf. Een bedrag zonder gesprek berust op aannames."),
  ("Hoe vergelijk ik voorstellen?", "Op inhoud: welke processen, welke koppelingen, wat onderhoud omvat en wat u zelf goedkeurt."),
  ("Is er nacalculatie?", "Nee. Een voorstel heeft één vaste prijs."),
  ("Zit ik vast aan een contract?", "Nee. Het onderhoud is maandelijks opzegbaar."),
  ("Wat kan ik vooraf doen?", "Neem een week lang op welke taken terugkomen en kies het proces dat de meeste uren kost.")],
 slot_kop="Wilt u een voorstel op maat?",
 slot_tekst="In een half uur nemen we uw situatie door. Binnen één werkdag volgt een voorstel met één vaste prijs.",
)
