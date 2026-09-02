# Werken bij Saltz Producement — wat er nog ingevuld moet worden

De pagina is af en werkt. Wat er nog niet in staat, zijn de gegevens die
alleen Saltz zelf kent. Zolang die er niet in staan, toont de pagina
bovenaan een gele balk met **Concept**. Die verdwijnt vanzelf zodra je stap 6
doet.

Vul nooit iets in wat niet klopt. Een sollicitant die op het loon of het
rooster afkomt en tijdens het telefoongesprek iets anders hoort, is niet
alleen weg — die vertelt het ook door. In een dorp als Breskens is dat het
duurste wat je kunt doen.

---

## 1. Contactgegevens — 2 minuten, en het belangrijkste

Deze staan als attribuut op de `<body>`-regel van **drie** bestanden:
`index.html`, `en.html` en `bedankt.html`.

```html
data-whatsapp="31612345678"        ← landcode zonder + of 0, geen spaties
data-telefoon="+31612345678"       ← nummer waarop je gebeld wilt worden
data-mail="werkenbij@saltz.nl"     ← hier komen de formulieren binnen
```

Gebruik voor WhatsApp bij voorkeur een **WhatsApp Business**-nummer, niet een
privételefoon. Dan kun je een automatisch welkomstbericht en openingstijden
instellen, en kunnen meerdere mensen meelezen.

## 2. E-mailadres activeren bij FormSubmit — 1 keer, 2 minuten

Het formulier verstuurt via formsubmit.co. Dat adres moet één keer bevestigd
worden:

1. Vul stap 1 in en zet de pagina online.
2. Vul het formulier zelf één keer in en verstuur het.
3. Op `werkenbij@saltz.nl` komt een mail van FormSubmit met een activatielink.
   Klik die aan.
4. Vanaf dan komt elke sollicitatie binnen in de mailbox.

Vergeet stap 4 niet te testen vanaf een telefoon.

## 3. Een seintje op je telefoon (optioneel, sterk aan te raden)

Een sollicitatie die drie uur in een mailbox blijft liggen, is vaak al weg —
die persoon appt ondertussen de volgende werkgever. Wil je direct een melding,
zet dan het Make-webhookadres erbij op de `<body>`-regel:

```html
data-hook="https://hook.eu1.make.com/xxxxxxxxxxxx"
```

Dezelfde constructie als op complete-ai.nl: Make stuurt het door naar Telegram
of WhatsApp. De mail blijft daarnaast gewoon aankomen; twee routes die
onafhankelijk van elkaar werken.

## 4. De harde gegevens op de pagina

Alle plekken staan in de HTML gemarkeerd met `<!-- INVULLEN: ... -->`.
Zoek daarop en je hebt ze alle vijf. Let op: wat je in `index.html` wijzigt,
moet je ook in `en.html` wijzigen.

| Wat | Waar | Staat er nu |
|---|---|---|
| Uurloon | cijferstrook + JobPosting-blok | € 14,50 – € 16,20 |
| Uren per week | cijferstrook | 32 – 40 |
| Rooster en werktijden | cijferstrook | dagdienst 07:00 – 16:00 |
| Reiskostenvergoeding | cijferstrook | € 0,23/km vanaf 5 km |
| Bezoekadres + postcode | voettekst + JobPosting-blok | "INVULLEN" |
| KvK-nummer | voettekst | ontbreekt |

Klopt het rooster niet — draaien jullie bijvoorbeeld twee ploegen — pas dan
ook de tekst "vast rooster" in de kop aan. Ploegentoeslag is een sterk
argument; als die er is, hoort die in de cijferstrook.

## 5. De teksten die over jullie gaan

Loop deze drie blokken langs en maak ze waar bij Saltz. Ze verkopen de baan,
dus ze moeten kloppen:

- **"Wat wij ertegenover zetten"** — zes kaarten. Beloof alleen wat in het
  contract staat. Wat jullie níet bieden, haal je weg; een kaart minder is
  beter dan een belofte die je niet nakomt.
- **"Wat we wél en niet vragen"** — vooral de rechterkolom is het hele punt
  van deze pagina. Ieder vinkje dat je daar kunt bijzetten, levert
  sollicitaties op.
- **De veelgestelde vragen** — controleer vooral het antwoord over het
  uitzendbureau en dat over België. Daar wordt het meest op afgehaakt.

## 6. De gele conceptbalk weghalen

Klopt alles? Haal dan `data-concept="ja"` weg uit de `<body>`-regel van
`index.html` en `en.html`. De balk verdwijnt.

## 7. Vindbaar in Google (Google for Jobs)

Op de Nederlandse pagina staat een blok gestructureerde gegevens. Daarmee
komt de vacature in de vacaturebalk bovenaan Google — gratis verkeer waar
anderen per klik voor betalen. Voorwaarden:

- `datePosted` en `validThrough` op echte datums zetten. Een vacature die
  "verlopen" is, verdwijnt uit Google. Zet `validThrough` maximaal een half
  jaar vooruit en verleng hem als de vacature open blijft.
- Het adres en het uurloon in dat blok moeten **precies** hetzelfde zijn als
  wat er zichtbaar op de pagina staat.
- Controleer het daarna op `search.google.com/test/rich-results`.
- Meld de pagina aan in Google Search Console. Zonder aanmelding duurt het
  weken voordat Google hem vindt.

De Engelse pagina heeft dit blok bewust niet: dezelfde vacature twee keer
aanmelden telt als dubbele melding.

## 8. Waar de pagina komt te staan

Nu staat alles in de map `werken-bij-saltz/`. Dat betekent:

- **Meteen bruikbaar** op `complete-ai.nl/werken-bij-saltz/`.
- **Verhuizen naar een eigen domein** (bijvoorbeeld `werkenbijsaltz.nl`) kan
  door de map te uploaden en klaar. Alle verwijzingen binnen de pagina zijn
  relatief. Pas dan alleen de vier `canonical`- en `hreflang`-regels bovenin
  `index.html` en `en.html` aan naar het nieuwe adres.

Een eigen domein is op termijn beter: een wervingspagina op het domein van je
websitebouwer wekt vragen bij sollicitanten, en Saltz houdt het dan zelf in
handen.

## 9. Testen voordat je adverteert

1. Open de pagina op je eigen telefoon, niet op een laptop. Negen van de tien
   sollicitanten komen via een telefoon binnen.
2. Druk op de WhatsApp-knop: opent WhatsApp met het bericht er al in?
3. Vul het formulier in: kom je op de bedankpagina en komt de mail binnen?
4. Druk op "Bellen" in de balk onderin: gaat je telefoon rinkelen?
5. Laat iemand die niet in de logistiek werkt de pagina lezen. Snapt die
   binnen tien seconden wat de baan is, wat het betaalt en hoe je reageert?

---

## Bestanden

| Bestand | Wat het is |
|---|---|
| `index.html` | de Nederlandse pagina |
| `en.html` | de Engelse pagina |
| `bedankt.html` + `bedankt.js` | bedankpagina na het formulier, ook het conversiepunt voor advertenties |
| `stijl.css` | de vormgeving |
| `script.js` | knoppen, formulier, herkomstmeting |
| `archivo.woff2` | het lettertype, zelf gehost — geen externe verbindingen |
| `advertentieteksten.md` | kant-en-klare advertenties en een plan om verkeer te krijgen |

De pagina laadt niets van buitenaf: geen Google Fonts, geen bibliotheken,
geen trackers. Dat is snel op een telefoon met slecht bereik in de polder, en
het scheelt een cookiebanner.
