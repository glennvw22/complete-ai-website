# De onderbouwingsagent

> Deze pagina hoort in de kluis onder **Koud bellen**. De kluis staat op de
> MacBook en was vanuit deze sessie niet bereikbaar, dus staat hij hier.
> Zet hem over en verwijs ernaar vanuit de hoofdstukpagina.

Een agent die per bedrijf op de **eigen website van dat bedrijf** bewijs
zoekt, en alleen prospects klaarzet waarvan hij dat bewijs letterlijk kan
aanwijzen. Hij verstuurt niets en hij bevraagt geen betaalde bron.

## Waarom hij bestaat

Wat we hadden, leidde de onderbouwing af uit **ontbrekende gegevens**. In
`score.py` wordt "geen website bekend" een koopsignaal, terwijl dat alleen
betekent dat OpenStreetMap geen website-tag had. Op 7 september 2026 bleek
dat minstens 1 op de 6 van die bedrijven gewoon een werkende website had.
Glenn daarover: "Wij gaan geen mensen bellen over websites die gewoon een
prima website hebben."

Diezelfde onderbouwing komt ongefilterd in de koude mail terecht:
`lib/koude-oogst.ts` zet `onderbouwing: lead.waarom_lead` in het koude
contact, en `{{onderbouwing}}` staat in de mailtekst.

Deze agent draait die volgorde om: eerst bewijs, dan pas een bewering.

## Hoe hij werkt

Vaste volgorde, geen taalmodel dat beslist wat de volgende stap is:

1. **Lead lezen** uit `leads.json`/`leads.csv` of uit een losse `--site`.
2. **Dossier ophalen** (`bewijs.py`): de homepagina plus hooguit drie
   contact- of colofonpagina's van het bedrijf zelf. `robots.txt` wordt
   gerespecteerd. De **platte tekst wordt bewaard**, want anders valt er
   achteraf niets na te kijken. Dit is het verschil met `website_check.py`,
   dat alleen een oordeel teruggeeft en de pagina weggooit.
3. **Signalen verzamelen** (`signalen.py`), in twee soorten:
   - *aanwezig*: staat er letterlijk, met citaat, bron-URL en bron-datum.
   - *afwezig*: ontbreekt op de gelezen pagina's. De zin noemt altijd
     welke pagina's dat waren.
4. **Rechtsvorm en adres** van diezelfde site halen. Een KvK-nummer en een
   rechtsvorm staan bij een net bedrijf gewoon in de voettekst of op de
   privacypagina. Dat is gratis, en het is bewijs met een bron.
5. **De poort** (`poort.py`). Zeven controles, alles moet slagen.
6. **Onderbouwing schrijven** uit hooguit twee bewezen zinnen.
7. **Klaarzetten**: een bestand, en met `--echt` een POST naar het
   bestaande `/api/leads/import`.

## De poort

| Controle | Wat hij tegenhoudt |
|---|---|
| Citaat terugzoeken | Elke aanwezigheidsclaim moet letterlijk op een opgehaalde pagina staan. Anders: verzonnen of verouderd. |
| Bron verplicht | Geen bron-URL of bron-datum bij een signaal: eruit. |
| Afwezigheid is geen pitch | Een prospect met alleen maar "dit ontbreekt" valt af. Dit is precies de fout van 7 september. |
| Rechtspersoon bewezen | Alleen een rechtsvorm die hard op de eigen site staat. Eenmanszaak, vof en maatschap vallen af, en een onbekende rechtsvorm ook. |
| Onpersoonlijk adres | Via `belbaar.onpersoonlijk_adres()`, dezelfde regel als bij bellen. Geen `henk@`. |
| Adres hoort bij de site | Het domein van het adres moet bij de gelezen pagina horen, en de pagina moet er een zijn die wij zelf gelezen hebben. |
| Toon | Geen gedachtestreepjes, geen percentages, geen jij-vorm, niet openen met "AI" of onze eigen naam, hoogstens 320 tekens. |

Bij twijfel valt een prospect af, met de reden erbij in `rapport.json`.
Een lege wachtrij is beter dan een verkeerde mail.

## Wat er in de mail terechtkomt

Alleen zinnen uit *aanwezige* signalen. Afwezigheidssignalen staan wel in
het rapport, zodat wij ze zien, maar gaan nooit naar een prospect. Daarmee
kan er per definitie niets in een mail staan wat wij niet met een citaat
kunnen aanwijzen.

`categorie` wordt het **aanbodonderdeel** waar het bewijs naar wijst, in de
volgorde telefonist, automatisering, website, seo, social, sea. Dat is een
verschil met vandaag: `lib/koude-oogst.ts` zet daar nu `lead.branche` in,
waardoor de campagne op branche wordt gekozen en niet op wat het bedrijf
mist.

## Draaien

```bash
cd leads
python3 -m onderbouwing.agent --site https://voorbeeld.nl --bedrijf "Voorbeeld BV"
python3 -m onderbouwing.agent --branche installatie --gemeenten "Houten,Kampen" --max 40 --uit uitvoer/<datum>/onderbouwing
python3 -m onderbouwing.agent --leads uitvoer/2026-09-23/leads.json --uit uitvoer/2026-09-23 --max 25
```

Standaard is het droogloop: er wordt niets verstuurd. Met `--echt` gaat het
naar `$DASHBOARD_URL/api/leads/import` met de header `x-leads-sleutel`,
dezelfde afspraak als `leads/dashboard.py`. Zonder `DASHBOARD_URL` of
zonder `LEADS_IMPORT_SLEUTEL` gebeurt er niets.

Tests: `python3 leads/test_onderbouwing.py` (25 stuks, zonder netwerk).

## Hoe het aansluit op wat er al staat

De agent zet de bewezen onderbouwing in `waarom_lead` en `baan` op `MAIL`.
`lib/koude-oogst.ts` neemt `waarom_lead` al over als `onderbouwing` en zet
er zelf `bron_url` en `bron_datum` bij. Aan de dashboardkant hoeft daarvoor
dus niets te veranderen.

Ontdubbeling hoeft hier ook niet nagebouwd te worden: `/api/leads/import`
matcht op `osm_id` en weigert leads met status `klant` of `niet_bellen`.

## Veiligheid

De agent haalt adressen op die uit een leadbestand komen, en volgt
omleidingen van websites van derden. Beide zijn niet te vertrouwen. Daarom
toetst `bewijs.controleer_adres()` elk adres voordat er verbinding wordt
gemaakt, ook bij elke omleiding: alleen http en https, alleen poort 80 en
443, en de hostnaam mag niet naar een privé-, loopback-, link-local- of
gereserveerd IP wijzen. Zonder die toets kan een regel in een leadbestand
(`"website": "http://169.254.169.254/latest/meta-data/"`) of een omleiding
vanaf een bedrijfssite de agent ons eigen netwerk in sturen.

Restrisico dat we bewust laten liggen: tussen de controle en het verbinden
kan een DNS-antwoord in theorie veranderen. Dat dichttimmeren vraagt om
zelf op het gecontroleerde IP verbinden, en dat weegt hier niet op tegen
de complexiteit.

De sleutel `LEADS_IMPORT_SLEUTEL` gaat alleen mee als header en komt in
geen enkele logregel of uitvoerbestand terecht.

## Eerste live run (24 september 2026)

Kapsalons in Houten, Huizen, IJsselstein en Kampen: 55 bedrijven uit
OpenStreetMap, 30 met een eigen website, 25 getoetst, **0 door de poort**.
De redenen, per stuk in `rapport.json`: vooral gmail-adressen en geen
rechtsvorm op de site. Kapsalons zijn meestal eenmanszaken, en die mogen we
zonder opt-in niet mailen. Voor koude mail is dit dus een zwakke branche.

Dezelfde run liet zien dat de leadsmachine zonder KVK in Nederland niets
levert (272 kandidaten, 0 leads): zonder KVK is geen enkel bedrijf als
rechtspersoon bevestigd. De agent haalt die bevestiging gratis van de eigen
site, waar de rechtsvorm er staat.

Installatiebedrijven in Houten, Huizen, IJsselstein, Kampen, Katwijk en
Leiden: 20 bedrijven, 18 met eigen website, **1 door de poort**: STB B.V.,
`info@stb.eu`. Bewijs: "STB© 2023" in de voettekst van stb.eu, en
"Bedrijfsnaam: STB B.V. KVK-nummer: 17074021" op hun privacypagina. Filialen
op één domein (BMN, Warmteservice, Jongeneel) vallen sindsdien af als keten.

Overpass bereiken: in een cloudcontainer lukte alleen de spiegel
`maps.mail.ru`; `bron_osm.SPIEGELS` probeert die al als eerste.

## Wat nog open staat

1. **Categorie op aanbod in plaats van branche.** Eén regel in
   `lib/koude-oogst.ts` (`categorie: lead.branche`) zou `verkoop_primair`
   moeten gebruiken als die gevuld is. Zolang dat niet gebeurt, kiest het
   dashboard de campagne nog op branche.
2. **Bellen blijft KVK-werk.** De rechtsvorm van de eigen site is genoeg om
   te mogen mailen, maar `belbaar.py` eist voor bellen een KVK-bevestiging.
   Daarom zet de agent `bellen_mag` op `NEE` en `baan` op `MAIL`.
3. **Adressen die alleen in een `mailto:`-link staan** worden niet gebruikt,
   want dan is het citaat niet terug te vinden in de bewaarde tekst. Dat
   kost wat adressen en houdt de regel heel.
