"""Landelijke/internationale ketens herkennen — drie lagen, allemaal gratis.

Aanleiding laag 1 (17/18-9-2026): `belbaar.is_filiaal()` herkent alleen een
officieel geregistreerde KVK-NEVENVESTIGING. Bij controle van de
dashboard-database bleken er 13 leads te staan die overduidelijk landelijke
ketens/filialen zijn (Boerenbond, C&A, Kwik-Fit x3, Van Mossel x2, Tesla,
Basic-Fit, Pets Place, SnowWorld Amsterdam, Lucardi x2) — GEEN van die 13
stond geregistreerd als KVK-nevenvestiging; ze staan allemaal apart,
zelfstandig ingeschreven (elke vestiging vaak als eigen rechtspersoon of
franchisenemer). `is_filiaal()` mist dit type dus volledig. Laag 1
(`is_landelijke_keten`, hieronder) vult dat gat met een expliciete naamlijst
— instant, geen API-aanroep nodig, maar bewust kort: alleen namen waarvan
zeker is dat het een keten is.

**Aanleiding laag 2 (18-9-2026): een naamlijst is precies het probleem, niet
de oplossing.** Tuinland (Groningen én Zwolle, twee losse KVK-nummers, dus
ook door de bestaande dubbel-kvk-check niet gevangen) stond niet op de lijst
en kwam gewoon weer door. Glenn, letterlijk: "niet alleen voor de boerenbond
... ik vroeg niet om alleen de boerenbond te fixen." Een vaste lijst is
altijd onvolledig — er is altijd een volgende keten die er niet op staat.

Laag 2 (`is_landelijke_spreiding`, onderaan dit bestand) lost dat structureel
op: een GRATIS landelijke naamzoekopdracht (kvk.zoek_landelijk, geen
plaats-filter) telt hoeveel ANDERE plaatsen een KVK-treffer hebben met
hetzelfde merk in de naam. Geen vaste lijst meer nodig — werkt voor elke
toekomstige keten, ook eentje waar we nog nooit van gehoord hebben. Getest
tegen echte KVK-data (18-9-2026): "Tuinland" -> 6+ verschillende plaatsen
(keten), "Kapsalon Jansen" -> 2 (Astrid Jansen, Monique Jansen, Rob Jansen
zijn gewoon andere, toevallig gelijknamige kapsalons, geen keten — de
naamzoekopdracht van de KVK matcht los op woorden, dus "Jansen" alleen is
geen betrouwbaar signaal; er moet een AANEENGESLOTEN woordreeks matchen,
zie `_bevat_subreeks`).

**Aanleiding laag 3 (18-9-2026, zelfde dag): laag 2 werkt niet voor België.**
Glenn vroeg expliciet: "pas het ook toe op België." Maar de KBO Public
Search (kbo.py) ondersteunt geen landelijke naamzoekopdracht zonder
plaats-afbakening — "zonder postcode of gemeente is een fonetische
naamzoekopdracht niet te vertrouwen" staat letterlijk in kbo.py, met het
bewijs erbij ("Barber" gaf 200+ treffers door heel België). Er is dus geen
Belgisch equivalent van kvk.zoek_landelijk te bouwen zonder zelf, tegen de
eigen regels van die gratis overheidsdienst in, tientallen steden na te
gaan.

Laag 3 (`landelijke_spreiding_in_oogst`, onderaan) lost dit anders op: de
leadsmachine scant sowieso al tientallen gemeenten per dag (zie
catalogus.jachtvolgorde). Een landelijke keten die in meerdere van die
gemeenten een vestiging heeft, staat dus vaak al MEERDERE KEREN in de
OpenStreetMap-oogst van diezelfde dag — dat kost geen enkele extra
netwerkaanroep, het is puur tellen in wat er toch al binnenkomt. Land-
onafhankelijk, dus dit werkt voor NL én BE tegelijk. Zwakker dan laag 2 (een
keten die vandaag maar op één gescande locatie voorkomt, wordt gemist -
mogelijk pas een andere dag gevangen als die andere stad dan wél aan de
beurt is), maar het enige gratis signaal dat voor België beschikbaar is.
Retroactief tegen de bestaande database getest (18-9-2026, met dezelfde
"zelfde naam >=3 plaatsen"-logica): Aveve (10x), Bel&Bo (9x), Horta (4x),
ZEB (3x) - allemaal landelijke Belgische ketens, geen van alle op een lijst.

Alle drie lagen zijn puur een KOSTENfilter, net als is_filiaal() in
belbaar.py: een filiaal van een keten heeft op die locatie geen lokale
besluitvormer met budget voor website, telefonist of automatisering, dus is
het geen bruikbare lead — ongeacht wat de KVK/KBO over de juridische
structuur zegt. Bij twijfel niet uitsluiten: een gemiste uitsluiting kost op
zijn hoogst twee cent (een basisprofiel dat overbodig blijkt); een
onterechte uitsluiting kost een echte lead.
"""
from __future__ import annotations

import re
import unicodedata

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kvk import KvkClient

# Canonieke ketennamen. De matchfunctie hieronder is ongevoelig voor
# hoofdletters, spaties, koppeltekens en het weglaten van een spatie (dus
# "Kwik-Fit", "Kwik Fit" en "KwikFit" worden alle drie herkend — dat zijn de
# drie schrijfwijzen die in de praktijk zijn aangetroffen op 17/18-9-2026).
LANDELIJKE_KETENS: tuple[str, ...] = (
    # De 13 leads van 17/18-9-2026:
    "Boerenbond",
    "C&A",
    "Kwik-Fit",
    "Van Mossel",
    "Tesla",
    "Basic-Fit",
    "Pets Place",
    "SnowWorld",
    "Lucardi",
    # Andere landelijke NL-ketens waarvan de naam ondubbelzinnig is:
    "Hunkemöller",
    "Zeeman",
    "Action",
    "Bruna",
    "Etos",
    "Kruidvat",
    # Gevonden 19-9-2026 bij het opsporen van dubbele naam+plaats-rijen in de
    # hele wachtrij (niet ketendetectie zelf, maar het bracht deze twee wel
    # aan het licht): "JBC" (Mechelen, bevestigd via jbc.be) en "Eye Wish"
    # (Hoorn/IJsselstein/Voorburg, bevestigd via eyewish.nl - een landelijke
    # opticienketen). "Mango" (bevestigd via shop.mango.com, Utrecht/Gent) is
    # bewust NIET toegevoegd: dat is een te gewoon woord (fruit, veel losse
    # horeca/kleine bedrijven heten toevallig ook zo - "Spicy Mango", "The
    # Mango Dream", "Mango Mobility" stonden allemaal tussen de KVK-treffers)
    # en zou hier valse treffers geven. Die twee Mango-leads zijn met de hand
    # verwijderd, niet via deze lijst.
    "JBC",
    "Eye Wish",
)


def _tokens(naam: str) -> list[str]:
    """Woorden van een naam, kleine letters, zonder leestekens of accenten.

    "C&A" -> ["c", "a"], "Kwik-Fit" -> ["kwik", "fit"],
    "Hunkemöller" -> ["hunkemoller"].
    """
    naam = unicodedata.normalize("NFKD", naam or "")
    naam = "".join(teken for teken in naam if not unicodedata.combining(teken))
    return re.findall(r"[a-z0-9]+", naam.lower())


def _bevat_subreeks(haystack: list[str], needle: tuple[str, ...]) -> bool:
    """Komt `needle` als aaneengesloten reeks voor in `haystack`?"""
    n = len(needle)
    if n == 0 or n > len(haystack):
        return False
    return any(tuple(haystack[i:i + n]) == needle for i in range(len(haystack) - n + 1))


# Voorbewerkt bij het importeren, niet bij elke aanroep.
_KETEN_TOKENS: tuple[tuple[str, ...], ...] = tuple(tuple(_tokens(k)) for k in LANDELIJKE_KETENS)
_KETEN_AANEEN: tuple[str, ...] = tuple("".join(t) for t in _KETEN_TOKENS)


def is_landelijke_keten(naam: str) -> bool:
    """Is dit (vermoedelijk) een vestiging van een bekende landelijke keten?

    Twee manieren om te matchen, allebei op woordniveau in plaats van los
    tekst-in-tekst zoeken (dat zou "Actionfoto Zwolle" ten onrechte aan
    "Action" koppelen):

    1. De woorden van de keten komen als aaneengesloten reeks voor in de
       woorden van de bedrijfsnaam — dekt spaties én koppeltekens, en een
       plaatsnaam erachter ("Kwik-Fit Almere", "Kwik Fit Almere").
    2. Voor een keten van meerdere woorden: staat er, als los AANEENGESCHREVEN
       woord, exact de samengevoegde ketennaam ("KwikFit") tussen de woorden
       van de bedrijfsnaam? Dekt de derde schrijfwijze zonder spatie of
       streepje. Alleen voor ketens van 2+ woorden: bij een keten van één
       woord (bv. "Tesla") is dit gelijk aan punt 1 hierboven en voegt het
       niets toe.

    Bij twijfel: geen match. Geen enkele losse-letter- of deelwoordmatch (dus
    "Capsalon Anna" matcht NIET met "C&A").
    """
    tokens = _tokens(naam)
    if not tokens:
        return False
    for keten_tokens, keten_aaneen in zip(_KETEN_TOKENS, _KETEN_AANEEN):
        if _bevat_subreeks(tokens, keten_tokens):
            return True
        if len(keten_tokens) > 1 and keten_aaneen in tokens:
            return True
    return False


# ── laag 2: dynamische herkenning, geen naamlijst nodig ─────────────────────

# 4+ andere plaatsen met hetzelfde merk (in het patroon "<merk> <plaats>")
# = keten. Niet lager: een veelvoorkomende Nederlandse achternaam levert
# op zichzelf al een paar toevallige "<achternaam> <stad>"-treffers op,
# zonder dat het één keten is. Getest tegen echte KVK-data 18-9-2026:
# Tuinland en Boerenbond zitten ruim boven de 4 (6 en 16), "Kapsalon
# Jansen" bleef op 2-3 steken. "Van Eijck Roosendaal" kwam op 5 uit - dat
# kán een keten zijn, kan ook toeval zijn (een veelvoorkomende achternaam);
# bij die onzekerheid is uitsluiten hier bewust de keuze, zie de
# moduledocstring voor waarom.
LANDELIJKE_SPREIDING_DREMPEL = 4


def _plaats_van_treffer(treffer: dict) -> str:
    """Zelfde als kvk._plaats_van_treffer — hier gekopieerd in plaats van
    geïmporteerd, want dat veldpad (adres.binnenlandsAdres.plaats) is
    KVK-antwoordformaat, geen kvk.py-interne zaak, en dit bestand hoeft verder
    niets van kvk.py te weten dan de KvkClient die het meekrijgt."""
    adres = treffer.get("adres")
    if not isinstance(adres, dict):
        return ""
    for sleutel in ("binnenlandsAdres", "buitenlandsAdres"):
        deel = adres.get(sleutel)
        if isinstance(deel, dict) and deel.get("plaats"):
            return str(deel["plaats"]).strip()
    return ""


def _merk_tokens(naam: str, eigen_plaats: str) -> tuple[str, ...]:
    """De woorden van de naam die vermoedelijk het MERK zijn, niet de plaats.

    "Tuinland Zwolle" met eigen_plaats "Zwolle" -> ("tuinland",): de
    plaatsnaam op het eind is duidelijk een locatie-suffix, geen deel van het
    merk. "Kapsalon Jansen" met eigen_plaats "Lichtenvoorde" -> geen
    overlap, dus blijft de hele naam staan: ("kapsalon", "jansen")."""
    tokens = _tokens(naam)
    plaats_tokens = _tokens(eigen_plaats)
    if plaats_tokens and len(tokens) > len(plaats_tokens) \
            and tokens[-len(plaats_tokens):] == plaats_tokens:
        tokens = tokens[:-len(plaats_tokens)]
    return tuple(tokens)


# Vastgesteld 18-9-2026, ná het live draaien van landelijke_spreiding tegen de
# echte database: "Mixed Hockey Club Purmerend" (8 andere plaatsen) en
# "Dierenkliniek Oosterhout" (4) haalden de drempel, maar zijn GEEN ketens -
# het zijn acht verschillende, onafhankelijke hockeyverenigingen en een
# stuk of wat losse dierenklinieken die toevallig dezelfde generieke
# categorie-naam ("Mixed Hockey Club <eigen plaats>", "Dierenkliniek <eigen
# plaats>") gebruiken. Hetzelfde probleem als "Van Eijck" (een veelvoorkomende
# achternaam), maar dan met een categorie-woord in plaats van een achternaam.
# Deze lijst vangt dat af: is het HELE merk (na het strippen van de plaats)
# opgebouwd uit alleen dit soort woorden, dan is spreiding geen betrouwbaar
# signaal en wordt er niet geteld. Bewust een lijst van CATEGORIEËN
# (rechtsvorm, sport, zorg, horeca-type), niet van merknamen - dat is een
# kleine, stabiele, taalkundige lijst die niet meegroeit zoals een
# ketennamenlijst dat wel zou doen.
_GENERIEKE_WOORDEN = frozenset({
    "de", "het", "een", "en", "van", "der", "den", "bij", "aan", "in", "op",
    "the", "and", "group", "groep", "company", "bv", "bvba", "vof", "nv",
    "zaak", "winkel", "shop", "store", "service", "services", "center",
    "centrum", "salon", "kapsalon", "garage", "bakkerij", "slagerij",
    "installatie", "installaties", "techniek", "technics", "bouw",
    "bouwwerken", "praktijk", "kliniek", "dierenkliniek", "artsenpraktijk",
    "huisartsenpraktijk", "tandartsenpraktijk", "fysiotherapie",
    "fysiopraktijk", "apotheek", "makelaardij", "advocatenkantoor",
    "notariskantoor", "accountantskantoor", "kroeg", "café", "cafe",
    "restaurant", "eetcafe", "snackbar", "cafetaria", "hotel", "pension",
    "club", "vereniging", "sportvereniging", "hockey", "voetbal", "korfbal",
    "tennis", "handbal", "volleybal", "atletiek", "gymnastiek", "zwemclub",
    "wielerclub", "sport", "sportclub", "sportschool",
    "mixed", "dames", "heren", "jeugd", "junioren", "senioren",
})

# Vastgesteld 19-9-2026: Glenn vond zelf nog "Olie&Zo" (zie hieronder, apart
# opgelost) en bij het herscannen van de HELE wachtrij (niet meer alleen de
# eerder verwijderde 162) bleken er meteen weer nieuwe generieke-categorie-
# fout-positieven bij te zitten die 18-9 nog niet was tegengekomen:
# "Huisartsenpost Hengelo" (elke regio heeft zijn EIGEN, onafhankelijke
# huisartsenpost), "Tandheelkundig Centrum X"/"Mondzorg X"/"Tandzorg X"/
# "Implantologie X" (allemaal generieke tandheelkunde-categorieën, losse
# praktijken), "Autoschade X" (generieke branche, net als "Autoschade de
# Jong" - een persoonsnaam erachter), "Klimcentrum X" (elk klimcentrum heeft
# een eigen naam: Bjoeks, Arque, Neoliet - "klimcentrum" zelf is de
# categorie), "Discus" (een siervis, veel losse dierenwinkels/aquariumzaken
# heten zo), "De Troubadour"/"De Lindenhof"/"De Poort" (veelgebruikte,
# generieke Nederlandse namen voor horeca/instellingen - bleken bij controle
# elk aan compleet ongerelateerde bedrijven te horen, tot een logopediepraktijk
# en een huisartsenpraktijk aan toe).
_GENERIEKE_WOORDEN_UITGEBREID_19_9 = frozenset({
    "huisartsenpost", "tandheelkundig", "mondzorg", "tandzorg",
    "implantologie", "autoschade", "klimcentrum", "discus", "troubadour",
    "lindenhof", "poort",
})
_GENERIEKE_WOORDEN = _GENERIEKE_WOORDEN | _GENERIEKE_WOORDEN_UITGEBREID_19_9


def _te_generiek_voor_spreiding(merk: tuple[str, ...]) -> bool:
    """Bestaat dit merk volledig uit generieke categorie-woorden? Dan is
    spreiding onder die naam geen betrouwbaar signaal (zie hierboven) - een
    leeg merk telt ook als te generiek (niets om op te zoeken)."""
    return not merk or all(w in _GENERIEKE_WOORDEN for w in merk)


def landelijke_spreiding(kvk_client: "KvkClient", naam: str, eigen_plaats: str) -> int:
    """Hoeveel DISTINCTE andere plaatsen hebben een KVK-treffer die overduidelijk
    hetzelfde merk is als deze kandidaat, alleen in een andere plaats? Eén
    gratis Zoeken-aanroep zonder plaats-filter (kvk_client.zoek_landelijk),
    dus landelijk. Geeft 0 als er geen duidelijk merk is (bv. een naam die
    volledig uit de plaatsnaam bestaat) of als KVK niet beschikbaar is.

    Belangrijk: er wordt gezocht op het MERK alleen ("Tuinland"), niet op de
    volledige kandidaatnaam ("Tuinland Zwolle"). Live tegen de echte KVK API
    geprobeerd (18-9-2026): zoeken op "Tuinland Zwolle" gaf maar 1 treffer
    (alleen die ene vestiging zelf, de KVK Zoeken API is dan kennelijk te
    specifiek/exact), zoeken op "Tuinland" gaf 10 treffers over heel
    Nederland. Zonder deze correctie mist deze functie precies het geval
    waarvoor hij gebouwd is.

    Een treffer telt alleen mee als het merk aaneengesloten voorkomt (net als
    is_landelijke_keten hierboven) ÉN de rest van de treffernaam - alles
    ERVOOR en ERNA samen - leeg is, of de woorden van de eigen plaats van DIE
    treffer er allemaal IN VOORKOMEN (niet per se de hele rest hoeven te
    zijn). Zonder enige eis hier leek "Van Eijck Roosendaal" (een gewone
    garage) live op een keten met 16 vestigingen: de KVK Zoeken API vond ook
    "Van Eijck Fiscaal", "Osteopathie van Eijck" en "Van Eijck Loonbedrijf" -
    andere bedrijven die toevallig dezelfde (veelvoorkomende) achternaam in
    de naam hebben, geen filialen - geen van die drie noemt een plaatsnaam,
    dus die blijven met de subset-eis terecht buiten de telling.

    Vastgesteld 19-9-2026, ná "Olie&zo" (Boxtel/'s-Hertogenbosch, een
    regionale garageketen): de eerdere, strengere versie van deze eis - de
    rest moest EXACT de plaats zijn - miste vestigingen als "Olie&zo Garage
    Zaltbommel B.V." en "Olie&zo Van der Doelen Schijndel", waar de
    branche/franchisenemer een extra woord toevoegt NAAST de plaatsnaam.
    Vandaar nu een subset-eis in plaats van gelijkheid. Dit blijft een
    heuristiek, geen garantie: een veelvoorkomende achternaam kan in
    zeldzame gevallen alsnog een paar keer toevallig als "<achternaam>
    <stad>" voorkomen, en een informele plaatsnaam ("Den Bosch" voor
    's-Hertogenbosch) wordt niet herkend. Vandaar de vrij hoge drempel
    (LANDELIJKE_SPREIDING_DREMPEL).

    Vastgesteld 18-9-2026, ná een controlerun tegen de eigen database: is het
    HELE merk een generieke categorie-omschrijving (_te_generiek_voor_
    spreiding) - "Mixed Hockey Club", "Dierenkliniek" - dan wordt er
    helemaal niet geteld. Acht verschillende, onafhankelijke hockey-
    verenigingen heten allemaal "Mixed Hockey Club <eigen plaats>" zonder dat
    dat één keten is; hetzelfde patroon als de Van Eijck-achternaam
    hierboven, maar dan met een categoriewoord in plaats van een achternaam."""
    merk = _merk_tokens(naam, eigen_plaats)
    if _te_generiek_voor_spreiding(merk):
        return 0
    treffers = kvk_client.zoek_landelijk(" ".join(merk))
    plekken: set[str] = set()
    for treffer in treffers:
        treffer_tokens = _tokens(treffer.get("naam", "") or "")
        n = len(merk)
        rest = None
        for i in range(len(treffer_tokens) - n + 1):
            if tuple(treffer_tokens[i:i + n]) == merk:
                rest = treffer_tokens[:i] + treffer_tokens[i + n:]
                break
        if rest is None:
            continue
        treffer_plaats = _plaats_van_treffer(treffer)
        plaats_tokens = set(_tokens(treffer_plaats))
        # De rest mag leeg zijn, of de eigen plaats moet er ALS WOORDEN in
        # voorkomen (niet per se de HELE rest zijn) - vastgesteld 19-9-2026
        # met "Olie&zo": vestigingsnamen als "Olie&zo Garage Zaltbommel B.V."
        # of "Olie&zo Van der Doelen Schijndel" voegen een extra woord toe
        # (de branche, de naam van de franchisenemer) NAAST de plaatsnaam.
        # Eisen dat de rest EXACT de plaats is (de vorige, te strenge versie)
        # miste die twee en hield Olie&zo (Boxtel/'s-Hertogenbosch) daardoor
        # onder de drempel, terwijl "Olie&zo Groep B.V." - de moedernaam -
        # letterlijk in de resultaten stond. Blijft wél strikt genoeg om
        # "Van Eijck Fiscaal" en "Osteopathie van Eijck" (geen plaatsnaam
        # erbij, dus geen subset-match) buiten te houden.
        if rest and not (plaats_tokens and plaats_tokens.issubset(set(rest))):
            continue
        sleutel = treffer_plaats or str(treffer.get("kvkNummer", ""))
        if sleutel:
            plekken.add(sleutel.lower())
    return len(plekken)


def is_landelijke_spreiding(kvk_client: "KvkClient", naam: str, eigen_plaats: str) -> bool:
    """Is dit (vermoedelijk) een filiaal van een keten die niet op de vaste
    lijst hierboven staat? Zie landelijke_spreiding() en de moduledocstring
    (aanleiding: Tuinland, 18-9-2026)."""
    return landelijke_spreiding(kvk_client, naam, eigen_plaats) >= LANDELIJKE_SPREIDING_DREMPEL


# ── laag 3: dezelfde-dag-oogst, land-onafhankelijk (NL én BE) ───────────────

# Vastgesteld 19-9-2026 bij de Belgische controle: de oogst van één dag is
# maar een STEEKPROEF van de gemeenten die vandaag toevallig aan de beurt
# waren (catalogus.jachtvolgorde), niet heel het land zoals bij laag 2 (KVK).
# Dezelfde drempel van 4 gebruiken is daardoor te hoog: "BRAX" en "Tommy
# Hilfiger" kwamen allebei maar 2x voor in de oogst, en zijn overduidelijk
# internationale ketens (bevestigd via hetzelfde website-domein op beide
# vestigingen: brax.com, tommy.com). Bij 2 is een exacte naam alleen niet
# genoeg bewijs - "Marc" kwam ook 2x voor, maar bleek een kapsalon in
# Mechelen (marcpatrick.be) en een compleet andere, ongerelateerde zaak
# in Gent (geen website) - toevallige naamgenoten, geen keten. Vandaar de
# lagere drempel hieronder, MAAR alleen als een tweede, onafhankelijk
# signaal het bevestigt: hetzelfde geregistreerde websitedomein op minstens
# twee van de vestigingen.
OOGST_SPREIDING_DREMPEL_MET_DOMEIN = 2


def _domein(website: str) -> str:
    """Het registreerbare domein uit een URL, zodat "https://eurotuin.be/"
    en "https://www.eurotuin.be/winkel" als dezelfde zaak herkend worden."""
    if not website:
        return ""
    zonder_schema = re.sub(r"^[a-z]+://", "", website.strip().lower())
    domein = zonder_schema.split("/")[0]
    if domein.startswith("www."):
        domein = domein[4:]
    return domein


def bouw_oogst_index(bedrijven) -> dict[str, set[str]]:
    """Groepeert de dagelijkse OpenStreetMap-oogst op genormaliseerde naam ->
    de gemeenten waarin die naam voorkomt. Eén keer bouwen per run (run.py),
    niet per kandidaat - dit is puur in-memory boekhouding over data die
    toch al binnen is, geen extra netwerkaanroep. Zie de moduledocstring
    (aanleiding laag 3, 18-9-2026: geen landelijke naamzoekopdracht mogelijk
    voor België)."""
    index: dict[str, set[str]] = {}
    for bedrijf in bedrijven:
        sleutel = " ".join(_tokens(bedrijf.naam))
        if not sleutel:
            continue
        gemeente = (bedrijf.gemeente or bedrijf.plaats or "").strip().lower()
        if not gemeente:
            continue
        index.setdefault(sleutel, set()).add(gemeente)
    return index


def bouw_oogst_domein_index(bedrijven) -> dict[str, dict[str, set[str]]]:
    """Per genormaliseerde naam: welk websitedomein hoort bij welke
    gemeenten? Zie OOGST_SPREIDING_DREMPEL_MET_DOMEIN hierboven voor
    waarom dit nodig is - een tweede, onafhankelijk signaal naast de
    naam+plaats-telling."""
    index: dict[str, dict[str, set[str]]] = {}
    for bedrijf in bedrijven:
        sleutel = " ".join(_tokens(bedrijf.naam))
        domein = _domein(getattr(bedrijf, "website", "") or "")
        if not sleutel or not domein:
            continue
        gemeente = (bedrijf.gemeente or bedrijf.plaats or "").strip().lower()
        if not gemeente:
            continue
        index.setdefault(sleutel, {}).setdefault(domein, set()).add(gemeente)
    return index


def landelijke_spreiding_in_oogst(oogst_index: dict[str, set[str]], naam: str) -> int:
    """Hoeveel DISTINCTE gemeenten heeft deze naam vandaag al opgeleverd,
    binnen dezelfde oogst? Zie bouw_oogst_index()."""
    sleutel = " ".join(_tokens(naam))
    if not sleutel:
        return 0
    return len(oogst_index.get(sleutel, set()))


def _zelfde_domein_op_meerdere_plekken(
    domein_index: dict[str, dict[str, set[str]]], naam: str
) -> bool:
    """Delen minstens twee vestigingen van deze naam hetzelfde websitedomein,
    op verschillende plaatsen? Zie OOGST_SPREIDING_DREMPEL_MET_DOMEIN."""
    sleutel = " ".join(_tokens(naam))
    domeinen = domein_index.get(sleutel)
    if not domeinen:
        return False
    return any(len(gemeenten) >= 2 for gemeenten in domeinen.values())


def is_landelijke_spreiding_in_oogst(
    oogst_index: dict[str, set[str]], naam: str,
    domein_index: dict[str, dict[str, set[str]]] | None = None,
) -> bool:
    """Is deze naam vandaag al genoeg keer opgedoken om als keten te gelden?
    Twee routes: de gewone drempel (LANDELIJKE_SPREIDING_DREMPEL, zoals
    laag 2), of - als er een domein_index is meegegeven - een lagere drempel
    (OOGST_SPREIDING_DREMPEL_MET_DOMEIN) mits minstens twee vestigingen
    hetzelfde websitedomein delen. domein_index is optioneel zodat oude
    aanroepen (en de tests van 18-9-2026) blijven werken."""
    aantal = landelijke_spreiding_in_oogst(oogst_index, naam)
    if aantal >= LANDELIJKE_SPREIDING_DREMPEL:
        return True
    if domein_index is None:
        return False
    return (aantal >= OOGST_SPREIDING_DREMPEL_MET_DOMEIN
            and _zelfde_domein_op_meerdere_plekken(domein_index, naam))
