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
   ("Niet vindbaar", "Wie de bedrijfsnaam niet intypt, komt de site niet tegen."),
   ("Traag op mobiel", "Wie wacht op een pagina, haakt af. Google noemt 2,5 seconden als grens."),
   ("Geen vervolgstap", "De bezoeker kijkt rond en vertrekt zonder contact op te nemen."),
   ("Wijzigingen duren te lang", "Daardoor blijven ze uit en veroudert de site.")]) +
  krijgt("wat-u-krijgt", "Wat u krijgt", "Alles in één keer geregeld.", "Eén aanspreekpunt, en aan het eind staat er iets dat af is.", [
   ("Ontwerp op maat", "Geen sjabloon met een logo erin, maar een ontwerp dat uw bedrijf en klanten volgt."),
   ("Mobiel eerst", "Ontworpen op telefoonformaat. Google beoordeelt de mobiele versie."),
   ("Snel", "Geen zware paginabouwers. Deze pagina laadt in ongeveer 0,7 seconde; dat is de norm."),
   ("Teksten die kloppen", "Geschreven na één gesprek, in uw taal en voor uw klant."),
   ("Vindbaar vanaf dag één", 'Goede structuur en een ingericht Google-bedrijfsprofiel. Daarna groeit het met <a href="vindbaarheid-seo.html">SEO</a>.'),
   ("Hosting en onderhoud", "Hosting, back-ups, updates en kleine wijzigingen zitten in het maandbedrag. Maandelijks opzegbaar.")]) +
  route("twee-weken", "Werkwijze", "Van eerste gesprek tot live in twee weken.", "", [
   ("Intake", "Een half uur. Kosteloos en vrijblijvend."),
   ("Voorstel", "Binnen één werkdag op papier, met één vaste prijs."),
   ("Teksten", "Eén gesprek. Daaruit schrijven wij alles."),
   ("Bouwen", "U kijkt mee via een link en stuurt gaandeweg bij."),
   ("Live", "Wij koppelen domein en e-mail en nemen alles met u door.")]) +
  proza("maatwerk", "Maatwerk of sjabloon", "Sjabloon of maatwerk?", '<p>Een sjabloon is een kant-en-klaar ontwerp met uw inhoud erin. Maatwerk volgt uit uw bedrijf en kan precies wat u nodig heeft, zoals online boeken. Wij bouwen maatwerk en houden het licht, zodat het snel blijft. Wilt u meer dan een website, dan sluiten <a href="automatisering.html">automatisering</a>, <a href="social-media.html">social media</a> en de <a href="ai-telefonist.html">AI-telefonist</a> daarop aan.</p>')),
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
  proza("korte-antwoord", "Het korte antwoord", "Wat is bedrijfsprocessen automatiseren?", '<p>Een bedrijfsproces is een vaste reeks stappen met een uitkomst, zoals een order verwerken, een offerte opvolgen of een factuur versturen. Automatiseren betekent dat software die stappen uitvoert en niemand ze nog met de hand doet. Dat past bij werk dat terugkomt, een vaste volgorde heeft en een uitkomst geeft die u kunt controleren. Een overzicht per afdeling staat bij de <a href="bedrijfsprocessen-automatiseren-voorbeelden.html">voorbeelden</a>.</p>') +
  pijn("herkenbaar", "De situatie", "Werk dat tijd kost en niets oplevert.", "", [
   ("Overtypen", "Dezelfde gegevens gaan van de mail naar het systeem naar de factuur."),
   ("Opvolgen vergeten", "Een offerte blijft liggen, een betaling blijft uit."),
   ("Administratie in de avond", "Facturen en bevestigingen schuiven door naar na sluitingstijd."),
   ("Alles hangt aan u", "Zodra u uitvalt, staat het werk stil.")]) +
  krijgt("wat-er-kan", "Wat er kan", "Dit lossen wij op.", "Samen bepalen we welke onderdelen bij uw bedrijf passen.", [
   ("Facturen en betaalherinneringen", "Facturen maken en versturen. Trage betalers krijgen automatisch een vriendelijke herinnering."),
   ("Offertes opvolgen", "Offertes opstellen, versturen en zien wie nog niet gereageerd heeft."),
   ("Afspraken", "Klanten plannen zelf in via een link, rechtstreeks in uw agenda, met herinnering vooraf."),
   ("Klantenbestand", "Gegevens, historie en notities per klant op één plek."),
   ("Bonnen en kosten", "Uitgaven worden vastgelegd en geordend, de btw staat klaar voor de aangifte."),
   ("Aanvragen op één plek", "Orders en vragen uit alle kanalen komen in één lijst.")]) +
  route("werkwijze", "Werkwijze", "Beginnen waar de winst het grootst is.", "", [
   ("Intake", "Een half uur: welke taken komen elke week terug, en wat mag nooit zonder uw akkoord de deur uit?"),
   ("Voorstel", "Binnen één werkdag op papier, met één vaste prijs."),
   ("Inrichten", "De eerste automatisering draait binnen enkele werkdagen."),
   ("Uitbreiden", "Pas als het werkt, voegen we een volgend onderdeel toe.")]) +
  proza("koppelingen", "Koppelingen", "Wij vervangen uw systemen niet.", '<p>Wij sluiten aan op wat u gebruikt: uw boekhouding, uw agenda en uw telefonie. Voor de telefoon is er de <a href="ai-telefonist.html">AI-telefonist</a>. Welke koppeling past, bepalen we in de intake.</p>')),
 vragen=[
  ("Wat kost automatisering?", 'Dat hangt af van het aantal processen, de koppelingen en het onderhoud. Daarom staat hier geen bedrag. Lees <a href="wat-kost-automatisering.html">waar de kosten van afhangen</a>.'),
  ("Moet ik mijn systemen vervangen?", "Nee. Wij koppelen aan wat u al gebruikt."),
  ("Wat als er iets misgaat?", "U bepaalt vooraf wat zonder uw akkoord de deur uitgaat. Het overige loopt automatisch en is terug te lezen."),
  ("Hoe snel draait het?", "De eerste automatisering binnen enkele werkdagen."),
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

# ───────────────────────── social-media ─────────────────────────
KORT["social-media.html"] = dict(
 inhoud=(
  pijn("herkenbaar", "De situatie", "Tijd voor social media ontbreekt.", "", [
   ("Het blijft liggen", "Berichten komen er niet van tussen het werk."),
   ("Onregelmatig", "Af en toe iets plaatsen werkt niet."),
   ("Geen overzicht", "Wat het oplevert, is niet te zien."),
   ("Oud bedrijfsprofiel", "Uw Google-bedrijfsprofiel loopt achter.")]) +
  proza("uitbesteden", "Uitbesteden", "Wij nemen het volledig over.", '<p>Wij bedenken, maken en plaatsen uw berichten en houden uw Google-bedrijfsprofiel en sociale kanalen wekelijks bij, in uw huisstijl. De accounts blijven van u. Het eerste bericht staat binnen een week.</p>') +
  krijgt("wat-u-krijgt", "Wat u krijgt", "Wekelijks zichtbaar.", "", [
   ("Weekplanning", "Elke week verschijnt er iets, op de kanalen die bij u passen."),
   ("Uw huisstijl", "Beeld en toon sluiten aan op uw bedrijf."),
   ("Google-bedrijfsprofiel", "Berichten, foto’s en reacties blijven actueel."),
   ("Reviews", "Klanten worden gevraagd om een beoordeling."),
   ("Rapportage", "Elke maand ziet u wat het heeft opgeleverd."),
   ("Eigen accounts", "U houdt de toegang. Er is geen contract voor vast.")]) +
  route("goedkeuring", "Werkwijze", "Zo houdt u de regie.", "", [
   ("Intake", "Wat doet u, voor wie, en wat past bij u?"),
   ("Maandplanning", "U keurt de maand vooraf goed."),
   ("Plaatsen", "Wij plaatsen en reageren. U stuurt af en toe een foto."),
   ("Bijsturen", "Maandelijks kijken we wat werkt.")]) ),
 vragen=[
  ("Moet ik zelf iets aanleveren?", "Af en toe een foto. De rest regelen wij."),
  ("Kan ik berichten vooraf goedkeuren?", "Ja. U keurt de planning van de maand vooraf goed."),
  ("Van wie blijven de accounts?", "Van u. Wij werken met uw toegang."),
  ("Hoe snel staat het eerste bericht online?", "Binnen een week."),
  ("Wat kost het?", "Dat hangt af van de kanalen en de frequentie. Na de intake volgt binnen één werkdag een voorstel. Meer over <a href=\"vindbaarheid-seo.html\">vindbaarheid</a> en <a href=\"adverteren.html\">adverteren</a> vindt u op de andere pagina’s.")],
 slot_kop="Wekelijks zichtbaar, zonder dat het u tijd kost.",
 slot_tekst="In een half uur bepalen we wat bij uw bedrijf past. Binnen één werkdag volgt een voorstel.",
)

# ───────────────────────── vindbaarheid-seo ─────────────────────────
KORT["vindbaarheid-seo.html"] = dict(
 inhoud=(
  pijn("herkenbaar", "De situatie", "Goed aanbod, maar niet te vinden.", "", [
   ("Alleen op bedrijfsnaam", "Wie zoekt wat u levert, vindt een concurrent."),
   ("Onzichtbaar op mobiel", "Google beoordeelt de mobiele versie van uw site."),
   ("Geen vertrouwen", "Er zijn weinig beoordelingen en verwijzingen."),
   ("Geen overzicht", "Het is onduidelijk wat er verandert.")]) +
  krijgt("wat-u-krijgt", "Wat u krijgt", "Doorlopend werk, maandelijks inzichtelijk.", "", [
   ("Technisch gezonde site", "Google kan uw pagina’s vinden, opnemen en begrijpen."),
   ("Inhoud die antwoord geeft", "Pagina’s die aansluiten op wat uw klanten intypen."),
   ("Google-bedrijfsprofiel", "Compleet ingericht en bijgehouden."),
   ("Vertrouwen", "Beoordelingen en verwijzingen die laten zien dat u betrouwbaar bent."),
   ("Nieuwe website", 'Staat uw <a href="websites.html">website</a> in de weg, dan bouwen wij er een die vindbaar is.'),
   ("Maandrapport", "U leest elke maand wat het heeft opgeleverd.")]) +
  route("werkwijze", "Werkwijze", "Stap voor stap hoger.", "", [
   ("Intake", "Waar staat u nu, en welke zoekopdrachten tellen?"),
   ("Voorstel", "Binnen één werkdag op papier."),
   ("Op orde brengen", "Eerst de techniek, dan de inhoud, dan het vertrouwen."),
   ("Meten", "Maandelijks de cijfers en het volgende voorstel.")]) +
  proza("fouten", "Valkuilen", "Wat wij niet doen.", '<p>Wij beloven geen plek één en kopen geen verwijzingen. Zo’n belofte kan niemand waarmaken, en gekochte verwijzingen kunnen schade geven. Wel meten wij elke maand wat er verandert. Wilt u ook zichtbaar zijn zonder te wachten, dan kan dat met <a href="adverteren.html">adverteren</a>.</p>')),
 vragen=[
  ("Hoe komt u hoger in de Google-ranking?", "Door vier dingen op orde te brengen: Google moet uw pagina’s kunnen vinden en opnemen, de inhoud moet aansluiten op wat mensen intypen, en beoordelingen en verwijzingen moeten laten zien dat u te vertrouwen bent."),
  ("Hoe lang duurt het voordat ik resultaat zie?", "SEO is doorlopend werk. Wij melden elke maand wat er verandert."),
  ("Kan ik SEO zelf doen?", "Voor een deel wel. Wij nemen het schrijven, meten en bijsturen over."),
  ("Wat kost het?", "Dat hangt af van uw situatie. Na de intake volgt binnen één werkdag een voorstel."),
  ("Zit ik vast aan een contract?", "Nee. Het is maandelijks opzegbaar.")],
 slot_kop="Waar staat u nu in Google?",
 slot_tekst="In een half uur kijken we naar wat er staat en wat het meeste oplevert. Binnen één werkdag volgt een voorstel.",
)

# ───────────────────────── adverteren ─────────────────────────
KORT["adverteren.html"] = dict(
 inhoud=(
  pijn("herkenbaar", "De situatie", "Advertentiebudget zonder duidelijk resultaat.", "", [
   ("Betalen per klik", "Zonder meting weet u niet wat een klik oplevert."),
   ("Geen koppeling", "Een aanvraag is niet te herleiden tot een advertentie."),
   ("Zelf bijsturen", "Het kost tijd en kennis."),
   ("Onzekerheid", "Is het budget goed besteed?")]) +
  krijgt("wat-u-krijgt", "Wat u krijgt", "Een specialist, met meetbaar resultaat.", "", [
   ("Opzet", "Een zoekcampagne op de zoekopdrachten van uw klanten."),
   ("Meting", "Elke aanvraag is te herleiden tot een advertentie."),
   ("Bijsturen", "Wij verbeteren de campagne op basis van de cijfers."),
   ("Uw budget", "U betaalt het advertentiebudget rechtstreeks aan Google."),
   ("Meta", "Ook Meta-advertenties op aanvraag."),
   ("Rapportage", "Elke maand ziet u wat het heeft opgeleverd.")]) +
  proza("waarom-op-aanvraag", "Op aanvraag", "Waarom adverteren op aanvraag gaat.", '<p>Elke campagne is maatwerk: het hangt af van uw aanbod, uw regio en wat een klant waard is. Daarom stellen wij na de intake een voorstel op, en noemen wij geen bedrag vooraf. Wilt u eerst op de lange termijn gevonden worden, begin dan met <a href="vindbaarheid-seo.html">SEO</a>.</p>') +
  route("werkwijze", "Werkwijze", "Van intake tot meetbaar resultaat.", "", [
   ("Intake", "Wat levert een klant op en waar zoekt hij?"),
   ("Voorstel", "Binnen één werkdag op papier."),
   ("Live", "De campagne en de meting gaan samen live."),
   ("Bijsturen", "Maandelijks beoordelen we de cijfers.")]) ),
 vragen=[
  ("Wat kost Google Ads beheren?", "Het advertentiebudget betaalt u rechtstreeks aan Google. Het beheer volgt uit de intake, met een voorstel binnen één werkdag."),
  ("Wie bepaalt welke advertentie verschijnt?", "Google, per zoekopdracht. Wij sturen bij op de resultaten."),
  ("Kan ik de resultaten zien?", "Ja, elke maand in een rapportage."),
  ("Doen jullie ook Meta-advertenties?", "Ja, op aanvraag."),
  ("Zit ik vast aan een contract?", "Nee. Het is maandelijks opzegbaar.")],
 slot_kop="Zichtbaar op het moment dat iemand zoekt.",
 slot_tekst="In een half uur kijken we of adverteren bij u past. Binnen één werkdag volgt een voorstel. Meer over <a href=\"websites.html\">websites</a>.",
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
