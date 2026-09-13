# Instellen — wat er moet gebeuren voordat de lead-machine draait

Op 31 augustus 2026 is in de omgeving van de routine gemeten wat er werkelijk
kan. Uitkomst: **de routine kon het internet niet op.** Dat is de hoofdoorzaak
van de wisselende opbrengst, niet de prompt.

| Bron | Status gemeten in `env_01HGeSKxbCmFdkoHcQt96rpM` ("Default") |
|---|---|
| Overpass / OpenStreetMap | geblokkeerd door het netwerkbeleid |
| Websites van bedrijven ophalen | geblokkeerd door het netwerkbeleid |
| KVK API | sleutel hoort in ~/.config/complete-ai/.env; api.kvk.nl is vanaf de Mac bereikbaar (gemeten 6-9-2026) |
| GitHub | werkt (loopt via een eigen proxy, staat los van het netwerkbeleid) |
| WebSearch | werkt (loopt via Anthropic, niet via het netwerk van de container) |

De omgeving staat op netwerkniveau **Trusted**: alleen pakketbronnen, GitHub en
cloud-SDK's. Elke andere host valt eruit. De oude routine kon dus alleen met
zoekresultaat-fragmenten werken en nooit iets natrekken — precies het gedrag dat
je zag.

## Belangrijk: de KVK-route omzeilt het netwerkbeleid

Een host die je op een **API-credential** van de omgeving zet, is bereikbaar
ongeacht het netwerkniveau — dat verkeer gaat niet door de allowlist. Voor KVK
hoef je het netwerkbeleid dus NIET open te zetten: zet de sleutel als
API-credential op `api.kvk.nl` en die koppeling werkt meteen, ook op Trusted.

Het netwerkbeleid openzetten is alleen nodig voor de twee andere bronnen:
OpenStreetMap en het beoordelen van de websites van bedrijven zelf.

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

Zet de sleutel daarna op DE vaste plek — er is er maar één:

```
echo 'KVK_API_KEY=jouw-sleutel-hier' >> ~/.config/complete-ai/.env
chmod 600 ~/.config/complete-ai/.env
```

Dat is alles. `leads/kvk.py` leest dit bestand zelf, dus geen enkele routine,
sessie of shell hoeft de sleutel nog te exporteren. Controleer met:

```
python3 leads/run.py --diagnose
```

**Zet hem NIET in een cloud-omgeving.** Dat is jarenlang de fout geweest en de
oude tekst hier stuurde daar zelfs op aan. De dagelijkse leadroutine draait als
geplande taak op de Mac zelf (`~/.claude/scheduled-tasks/leads-naar-dashboard/`),
niet in de cloud. Een sleutel die in een cloudsessie is gezet, is bij de
volgende sessie weg — vandaar dat hij elke week opnieuw gevraagd werd. Het
bestand `~/.config/complete-ai/.env` heeft rechten 600, staat buiten deze
(openbare) repository en blijft staan.

De route via `KVK_VIA_PROXY=1` en een API-credential bestaat nog in de code en
is prima voor een run die daadwerkelijk ín een cloud-omgeving draait. Voor de
dagelijkse routine is die route niet van toepassing.

Een KVK-sleutel begint met een kleine letter `l`, gevolgd door hexadecimale
tekens — bijvoorbeeld `l7a4d9cdb...`. Die `l` hoort er dus bij; haal hem er niet
af. Neem de sleutel over met de kopieerknop in het portaal, niet met de hand.

## Stap 2b — DNCM_API_SLEUTEL: alleen als Glenn zelf ooit besluit dat de licentie het waard is

**Niet iets om uit te voeren of voor te stellen.** Er bleek geen gratis manier
te zijn om de Belgische DNCM-lijst te raadplegen (nagezocht 13-9-2026: DNCM
VZW's eigen FAQ, de wettelijke basis — KB 28-6-2015 —, de FOD Economie-pagina
en een brancheorganisatie zeggen alle drie hetzelfde: een licentie is de
wettelijk voorgeschreven weg, geen vrijstelling voor kleine bedrijven). Omdat
Complete AI geen nieuwe vaste lasten aangaat (zie de kluis, Grenzen — Geen
betaalde oplossingen), is een Belgisch bedrijf zonder deze sleutel gewoon
**niet belbaar** in `leads/belbaar.py` — geen waarschuwing-met-vinkje, want
dat is geen garantie. Dat is de huidige, bewuste, gratis stand van zaken.

Deze stap staat hier alleen als referentie voor het geval Glenn zelf, op enig
moment, besluit dat de licentie het waard is — dat is aan hem, niet iets om
opnieuw voor te leggen.

1. Ga naar **<https://www.donotcallme.be/nl/telemarketeers/>**, registreer
   Complete AI als bedrijf en maak een account aan (met 2-staps­verificatie via
   Google Authenticator).
2. Koop een licentie als **Adverteerder** (Complete AI belt voor haar eigen
   dienstverlening, niet namens een ander bedrijf — dat is geen "Service
   provider"/callcenter). Prijzen, live nagekeken op donotcallme.be/nl/licenties/
   op 12-9-2026, voor ≤ 250 medewerkers, excl. 21% btw:
   - € 60/maand — geen jaarverplichting, wordt niet automatisch verlengd.
   - € 600/jaar — wordt stilzwijgend verlengd tenzij je uiterlijk 1 maand vóór
     de vervaldatum opzegt.
3. Log in op het account en activeer **"Integratie via API"** (in je online
   account, bij het Bel-Me-Niet-Meer bestand). Dat toont een unieke
   **Secret Key**. Kopieer die.
4. Zet de sleutel op dezelfde vaste plek als de KVK-sleutel:
   ```
   echo 'DNCM_API_SLEUTEL=jouw-secret-key-hier' >> ~/.config/complete-ai/.env
   chmod 600 ~/.config/complete-ai/.env
   ```
5. Het exacte HTTP-verzoek (eindpunt, headers, antwoordformaat) van de API
   staat pas ná activering in je account zelf, niet publiek gedocumenteerd.
   `leads/dncm.py`, functie `_bevraag()`, heeft daarvoor een duidelijk
   gemarkeerde open plek — geef door wat daar staat (bijvoorbeeld een
   schermafbeelding van de API-documentatie in je account), dan wordt die ene
   functie afgemaakt. Tot dan geeft de sleutel alléén toegang; de koppeling
   zelf blijft "onbekend" en een Belgisch bedrijf blijft niet-belbaar — er
   verandert dus niets vanzelf door alleen de sleutel te zetten.

De DNCM-lijst kent, net als bij KVK, ook een limiet: **maximaal 20 checks per
minuut** — `leads/dncm.py` houdt zich daar zelf aan, dus dit vraagt geen
verdere actie.

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
