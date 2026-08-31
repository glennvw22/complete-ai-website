# Instellen — wat er moet gebeuren voordat de lead-machine draait

Op 31 augustus 2026 is in de omgeving van de routine gemeten wat er werkelijk
kan. Uitkomst: **de routine kon het internet niet op.** Dat is de hoofdoorzaak
van de wisselende opbrengst, niet de prompt.

| Bron | Status gemeten in `env_01HGeSKxbCmFdkoHcQt96rpM` ("Default") |
|---|---|
| Overpass / OpenStreetMap | geblokkeerd door het netwerkbeleid |
| Websites van bedrijven ophalen | geblokkeerd door het netwerkbeleid |
| KVK API | geen sleutel aanwezig, en host zou ook geblokkeerd zijn |
| GitHub | werkt (loopt via een eigen proxy, staat los van het netwerkbeleid) |
| WebSearch | werkt (loopt via Anthropic, niet via het netwerk van de container) |

De omgeving staat op netwerkniveau **Trusted**: alleen pakketbronnen, GitHub en
cloud-SDK's. Elke andere host valt eruit. De oude routine kon dus alleen met
zoekresultaat-fragmenten werken en nooit iets natrekken — precies het gedrag dat
je zag.

## Stap 1 — Netwerktoegang openzetten

Ga naar [claude.ai/code](https://claude.ai/code), open de omgeving **Default**
ter bewerking en zet **Network access** op **Custom**. Vink
"Also include default list of common package managers" aan en zet in
**Allowed domains** één domein per regel:

```
overpass-api.de
overpass.kumi.systems
overpass.osm.ch
api.kvk.nl
```

Wil je dat de machine ook de websites van de bedrijven zelf kan beoordelen — en
dat is waar een groot deel van de waarde zit — dan kan dat niet met een
allowlist, want dat zijn duizenden verschillende domeinen. Zet **Network
access** dan op **Full**.

Aanbeveling: **Full**. Zonder dat blijft de websitekwaliteitscheck leeg en val je
terug op alleen "staat er een website-tag in de bron, ja of nee".

## Stap 2 — De KVK-sleutel terugvinden en instellen

Je sleutel staat in het KVK Developer Portal, niet in je gewone KVK-account. Het
is een apart account met een eigen gebruikersnaam en wachtwoord.

1. Log in op **<https://developers.kvk.nl/nl/login>**
2. Ga naar **Mijn API-keys** in het portaal. Daar staan je sleutel(s) en je
   verbruik. Je kunt er ook een extra sleutel aanvragen.
3. Overzicht van je API's en aanvragen: <https://developers.kvk.nl/nl/apis> en
   <https://developers.kvk.nl/nl/apply-for-apis>

Controleer welke API's op je sleutel staan. Voor deze machine heb je nodig:

- **Zoeken API** (gratis) — om van naam + plaats naar een KVK-nummer te komen
- **Basisprofiel API** — voor de rechtsvorm; die bepaalt of je koud mag bellen.
  Deze kost ongeveer € 6,40 per maand per sleutel plus € 0,02 per bevraging.
  Bij 40 verrijkingen per dag is dat ruwweg € 25 per maand.

Zet de sleutel daarna op één van deze twee manieren in de omgeving:

**Route A — omgevingsvariabele (simpel).** In de omgevingsinstellingen bij
**Environment variables**:

```
KVK_API_KEY=jouw-sleutel-hier
```

**Route B — API-credential (veiliger, aanbevolen).** Bij **API credentials** in
dezelfde dialoog: **Add credential**, met

- **Allowed websites**: `api.kvk.nl`
- **Custom headers**: naam `apikey`, prefix leeg, waarde is je sleutel

De sleutel komt dan nooit in de sessie terecht; de proxy plakt hem erop nadat
het verzoek de container verlaten heeft. Zet bij route B ook de variabele
`KVK_VIA_PROXY=1`, zodat de code weet dat hij zelf geen header hoeft mee te
sturen.

## Stap 3 — De oude routines uitzetten

Twee oude routines draaien allebei om 09:00 en leveren dubbel werk:

- `leads agent` (`trig_01653QypYLwqbDvxeHgDUNuW`)
- `Leads agent v2 (verbeterd)` (`trig_01BRx2KEsjJkiYqth1DsoSYu`)

Deze zijn buiten Claude om aangemaakt en kunnen alleen door jou zelf worden
uitgezet, in je Routines-overzicht.

## Stap 4 — Controleren

Draai in een sessie in die omgeving:

```bash
python3 leads/run.py --diagnose
```

Dat geeft in één keer antwoord: werkt Overpass, werkt KVK, werkt de
websitecheck. Alle drie op `true` betekent dat de machine volledig kan draaien.
