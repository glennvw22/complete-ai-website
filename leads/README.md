# Lead-machine Complete AI

Deterministische leadselectie voor Complete AI (NL + Vlaanderen). Vervangt de
twee oude "leads agent"-routines, die elke dag opnieuw vanaf nul het internet
afzochten en daardoor de ene dag 40 leads opleverden en de andere dag niets.

## Wat er mis was met de oude opzet

| Probleem | Gevolg |
|---|---|
| Twee routines, allebei om 09:00 NL | Dubbel werk, dubbele meldingen, geen gedeelde administratie |
| v2 draaide op een klein model; runs duurden 2 tot 3 minuten | Onmogelijk om 50 leads echt na te trekken |
| Bedrijven zoeken via zoekmachine-snippets en bedrijvengidsen | Gidsen blokkeren bots; op een slechte dag komt er niets terug |
| Stapel harde filters (50-150 reviews **en** 4,0+ **en** geen moderne site **en** contact vindbaar) | Eén ontbrekend gegeven en de lead valt weg. Vandaar de lege dagen |
| Geheugenbestand in `/home/claude/` | De container is per run nieuw, dus het bestand was elke dag weer leeg: geen echte ontdubbeling |
| Eén koopreden: "slechte website" | Het bredere aanbod van Complete AI werd niet verkocht |
| KVK API werd nergens aangeroepen | De koppeling deed inderdaad niets |

## Hoe het nu werkt

```
territorium (deterministisch)
        |
        v
OpenStreetMap / Overpass  ->  honderden bedrijven per gemeente,
        |                     met naam, adres, telefoon en website-tag
        v
websitecheck (parallel)   ->  bereikbaar? https? mobiel? traag? verouderd?
        |                     online afspraak? structuurdata? copyrightjaar?
        v
KVK-verrijking (top-N)    ->  rechtsvorm, SBI, KVK-nummer -> BEL- of MAIL-baan
        |
        v
scoring op zes diensten   ->  gerangschikte lijst + "dit verkoop je hier"
```

### De rol van KVK, precies

De KVK **Zoeken** API zoekt op naam, KVK-nummer, postcode+huisnummer, plaats en
straat. Er is **geen filter op SBI-code of branche**. Je kunt dus niet vragen
"geef alle kappers in Zwolle". De KVK API is daarmee ongeschikt als *bron* van
leads — dat is de reden dat er in de praktijk niets zinnigs mee gebeurde.

Waar KVK wél onmisbaar is: de **Basisprofiel** API geeft per KVK-nummer de
rechtsvorm, de SBI-activiteiten en het aantal vestigingen. De rechtsvorm bepaalt
of een bedrijf koud gebeld mag worden (rechtspersoon) of alleen gemaild
(eenmanszaak, vof, maatschap). Zonder KVK gaat elke lead naar de mailbaan, want
bij twijfel niet bellen.

Zet daarom `KVK_API_KEY` in de omgeving van de routine. Zonder sleutel draait
alles gewoon door, maar meldt de run bovenaan dat KVK niet beschikbaar is in
plaats van dat stil te laten.

### Alleen belbare leads

De lijst bevat uitsluitend bedrijven die je zonder nadenken mag draaien.

- **Nederland**: alleen rechtspersonen (BV, NV, stichting, vereniging,
  coöperatie), bevestigd door de rechtsvorm uit het KVK-basisprofiel.
  Eenmanszaken, vof's, cv's en maatschappen vallen af; dat zijn natuurlijke
  personen en die koud bellen levert klachten op. Blijft de rechtsvorm
  onbekend, dan valt het bedrijf óók af — bij twijfel niet bellen.
- **Vlaanderen**: zakelijk bellen mag, met "DNCM-scrub vereist" in de kolom
  `let_op`.
- Zonder telefoonnummer geen lead, en ook geen betaalde KVK-bevraging.

Gevolg: van de kandidaten uit de bron valt in Nederland een fors deel af. De
pijplijn haalt daarom zes keer zoveel kandidaten op als er leads nodig zijn.

### Quota in plaats van alleen sorteren

Puur op score sorteren geeft een lijst met honderd bedrijven zonder website en
nooit een AI-telefonist. Daarom worden eerst de quota gevuld
(`--min-website`, standaard 50; `--min-telefonist` en `--min-automatisering`,
standaard 15) en pas daarna wordt aangevuld op score. Wordt een quotum niet
gehaald, dan staat dat als tekort in `samenvatting.json` in plaats van
stilzwijgend te verdwijnen.

### Warmte: wat wel en niet kan

Bij elke lead staat een warmte-inschatting met de sporen die eraan ten
grondslag liggen: een geparkeerd domein of "binnenkort online", een website die
het niet doet, wel een socialpagina maar geen site, geen online
afspraakmogelijkheid, meerdere vestigingen.

Wat **niet** kan: achterhalen wie er op internet naar "website laten maken"
heeft gezocht. Zoekgedrag van bedrijven is geen openbare data — dat is precies
wat je bij Google Ads koopt. De warmtesignalen hierboven zijn waarneembare
sporen die dezelfde kant op wijzen, geen zoekintentie.

### De zes koopsignalen

Elk bedrijf wordt op zes assen beoordeeld, elk gekoppeld aan een dienst:

1. **Website** — geen site, alleen social, geparkeerd, onbereikbaar, geen SSL,
   niet mobiel, traag, oud copyrightjaar, verouderde bouwer
2. **Vindbaarheid (SEO)** — geen paginatitel, geen omschrijving voor Google,
   geen structuurdata
3. **AI-telefonist** — hoge belintensiteit in de branche, beperkte
   openingstijden
4. **Automatisering** — geen online afspraak- of bestelmogelijkheid in een
   branche waar dat hoort
5. **Social** — geen socialkanaal in een branche die daarvan leeft
6. **Advertenties** — spoed- en offertebranches zonder vindbaarheid

Een bedrijf met een prima website is dus nog steeds een lead, bijvoorbeeld voor
de AI-telefonist. Er wordt niet meer hard weggegooid maar gerangschikt, met een
zekerheidsmarkering (hoog / midden / laag) erbij. Daarom kan er geen lege dag
meer zijn.

## Gebruik

```bash
python3 leads/run.py --diagnose                 # werken de bronnen vandaag?
python3 leads/run.py --land NL --aantal 100     # dagelijkse belllijst
python3 leads/run.py --land NL --aantal 100 --min-website 50 \
        --min-telefonist 20 --min-automatisering 20 --kvk-budget 600
python3 leads/run.py --branche installatie      # branche zelf kiezen
python3 leads/test_logica.py                    # alle logica, zonder netwerk
```

`--land NL` forceert Nederland. Zonder die vlag wisselt de rotatie per dag
tussen Nederland en Vlaanderen, en Vlaamse leads moeten eerst langs de
DNCM-lijst voordat je mag bellen.

**Kosten.** Elke KVK-basisprofielbevraging kost ongeveer 2 cent. Om honderd
belbare Nederlandse leads te vinden zijn er al snel 300 tot 600 nodig, dus reken
op 6 tot 12 euro per dag. `--kvk-budget` zet het plafond; de run meldt achteraf
wat hij verbruikt heeft.

Uitvoer komt in `leads/uitvoer/<datum>/` als `leads.csv`, `leads.json` en
`samenvatting.json`.

## Belangrijk: geen leaddata in deze repository

`leads/uitvoer/` staat in `.gitignore`. Deze repository is **openbaar** (het is
de bron van complete-ai.nl). Bedrijfsgegevens, telefoonnummers en e-mailadressen
horen daar niet in. De dagelijkse lijsten gaan naar Google Drive; alleen de code
staat hier.

## Territoriumrotatie

Het jachtgebied volgt uit de datum, zonder willekeur en zonder geheugen:
even dagen Nederland, oneven dagen Vlaanderen; elke dag een andere branche; het
gemeenteblok schuift elke twaalf ronden op. Elke combinatie van branche en
gemeenteblok komt precies één keer voorbij voordat er iets herhaalt — ruim
900 dagen voor Nederland en ruim 400 voor Vlaanderen.

## Wat nog niet getest is

De netwerkkant (Overpass, KVK, het ophalen van websites) kon in de
ontwikkelomgeving niet worden uitgeprobeerd: die container mag niet naar buiten.
Alle logica eromheen is wel getest met `test_logica.py`. Draai daarom
`python3 leads/run.py --diagnose` als eerste in de omgeving van de routine: die
geeft in één keer antwoord op de vraag welke bronnen daar werkelijk werken.
