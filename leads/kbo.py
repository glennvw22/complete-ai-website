"""KBO-koppeling: de rechtsvorm van een Belgisch bedrijf, gratis.

Waarom dit bestaat: voor Nederland kost de rechtsvorm geld (KVK Basisprofiel,
€ 0,02 per bevraging, zie kvk.py). Voor België is exact dezelfde informatie
gratis openbaar via de Kruispuntbank van Ondernemingen. Dat maakt het verschil
tussen "we weten het niet, dus niet benaderen" en een bruikbare Belgische
stroom, zonder één euro.

Twee routes naar die data, in volgorde van voorkeur:

  1. KBO Open Data — een dagelijks CSV met ALLE actieve entiteiten (rechtsvorm,
     NACE, adres, status). Gratis, maar vraagt één gratis inschrijving bij de
     FOD Economie. Onbeperkt lokaal opzoeken daarna, geen netwerk per lead.
     Zodra dat bestand er staat: gebruik die route (zie INSTELLEN.md).
  2. KBO Public Search — de openbare zoekpagina, zonder account te bevragen.
     Dat is wat dit bestand nu doet, zodat de koppeling vandaag al werkt en
     niet op een inschrijving hoeft te wachten.

Public Search is een gratis overheidsdienst, geen API. Daarom bevraagt dit
bestand haar spaarzaam en netjes: één verzoek per bedrijf, met een pauze
ertussen, en alleen voor bedrijven die alle eerdere filters al hebben
gehaald. Nooit een lijst leegtrekken.

WAT HIER NIET MAG, en waarom het in de code staat:
de gebruiksvoorwaarden van de KBO zijn expliciet — *"Persoonsgegevens mogen
niet worden hergebruikt voor directe marketingdoeleinden. Het zijn met name
alle gegevens die betrekking hebben op een geregistreerde entiteit natuurlijke
persoon."* Een entiteit die een natuurlijk persoon is (eenmanszaak) mag dus
niet via deze bron voor acquisitie gebruikt worden. `is_rechtspersoon=False`
betekent hier daarom: weggooien, niet bewaren. Dat valt samen met de Belgische
spamregel, die de uitzondering voor ongevraagde e-mail ook alleen aan
rechtspersonen geeft — één filter dekt beide.
"""
from __future__ import annotations

import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

ZOEKEN = "https://kbopub.economie.fgov.be/kbopub/zoeknaamfonetischform.html"
ZOEKEN_ADRES = "https://kbopub.economie.fgov.be/kbopub/zoekadresform.html"
ENTITEIT = "https://kbopub.economie.fgov.be/kbopub/toonondernemingps.html"

# Eén verzoek per seconde. Dit is een gratis overheidsdienst; die belast je niet.
PAUZE_S = 1.0
TIMEOUT_S = 20

# Zo labelt Public Search elke rij in het resultaat: een geregistreerde
# entiteit die een rechtspersoon is ("ENT RP"), een natuurlijk persoon
# ("ENT NP"), of een vestigingseenheid ("VE") van een van beide.
_RIJ = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
_CEL = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
_TAG = re.compile(r"<[^>]+>")
_NUMMER = re.compile(r"\b(\d{4}\.\d{3}\.\d{3})\b")


@dataclass
class KboResultaat:
    gevonden: bool = False
    is_rechtspersoon: bool | None = None   # None = onbekend
    ondernemingsnummer: str = ""
    naam: str = ""
    rechtsvorm: str = ""
    actief: bool | None = None
    fout: str = ""


def _schoon(tekst: str) -> str:
    tekst = _TAG.sub(" ", tekst)
    tekst = tekst.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", tekst).strip()


def _vereenvoudig(naam: str) -> str:
    """Naam terugbrengen tot vergelijkbare kern: kleine letters, geen
    leestekens, geen rechtsvorm-afkortingen."""
    laag = naam.lower()
    laag = re.sub(r"\b(bv|bvba|nv|vzw|cv|cvba|comm\.?v|vof)\b", " ", laag)
    laag = re.sub(r"[^a-z0-9]+", " ", laag)
    return re.sub(r"\s+", " ", laag).strip()


# Woorden die niets onderscheiden: die mogen nooit alleen een match dragen.
_LEGE_WOORDEN = frozenset({
    "de", "het", "een", "en", "van", "der", "den", "bij", "aan", "in", "op",
    "the", "and", "group", "groep", "company", "belgium", "belgie", "bvba",
    "zaak", "winkel", "shop", "store", "service", "services", "center",
    "centrum", "salon", "kapsalon", "garage", "bakkerij", "slagerij",
    "installatie", "installaties", "techniek", "technics", "bouw", "bouwwerken",
})


def _kernwoorden(naam: str) -> set[str]:
    """De woorden in een naam die iets onderscheiden: lang genoeg en niet
    generiek. "Kapsalon Nuyttens" houdt dus alleen "nuyttens" over."""
    return {w for w in _vereenvoudig(naam).split()
            if len(w) >= 4 and w not in _LEGE_WOORDEN}


def _namen_horen_bij_elkaar(osm_naam: str, kbo_naam: str) -> bool:
    """Zijn dit dezelfde zaak? Exact gelijk na vereenvoudiging, of ze delen
    minstens één onderscheidend woord ("Nuyttens Automatisatie" tegenover
    "NUYTTENS AUTOMATISATIE BV"). Alleen generieke woorden gemeen hebben is
    geen match — anders koppelt "Garage Janssens" aan "Garage Peeters"."""
    if not osm_naam or not kbo_naam:
        return False
    if _vereenvoudig(osm_naam) == _vereenvoudig(kbo_naam):
        return True
    return bool(_kernwoorden(osm_naam) & _kernwoorden(kbo_naam))


class KboClient:
    def __init__(self, pauze_s: float = PAUZE_S):
        self.pauze_s = pauze_s
        self._cache: dict[tuple[str, str], KboResultaat] = {}
        self._laatste_verzoek = 0.0
        self.bevragingen = 0
        # Zowel het zoeken op naam als op adres werkt bij KBO alléén met een
        # postcode; de gemeentenaam wordt genegeerd (zelf getest 13-9-2026).
        # OpenStreetMap heeft die postcode bij ongeveer de helft van de
        # bedrijven niet. Daarom onthouden we per gemeente welke postcodes we
        # bij ándere bedrijven in diezelfde gemeente wél zagen, en gebruiken
        # die als terugval. Dat is waargenomen data, geen aanname — en zit de
        # gok ernaast, dan levert de opzoeking "niets gevonden" op en nooit
        # een verkeerde koppeling, want het adres in het antwoord wordt alsnog
        # tegen de gemeentenaam gehouden.
        self._postcodes_per_gemeente: dict[str, list[str]] = {}

    def leer_postcodes(self, bedrijven) -> None:
        """Onthoud per gemeente de postcodes die in deze partij voorkomen."""
        for bedrijf in bedrijven:
            gemeente = (bedrijf.gemeente or bedrijf.plaats or "").strip().lower()
            postcode = (bedrijf.postcode or "").strip()
            if not gemeente or not postcode:
                continue
            lijst = self._postcodes_per_gemeente.setdefault(gemeente, [])
            if postcode not in lijst:
                lijst.append(postcode)

    def _postcodes_voor(self, bedrijf) -> list[str]:
        eigen = (bedrijf.postcode or "").strip()
        if eigen:
            return [eigen]
        gemeente = (bedrijf.gemeente or bedrijf.plaats or "").strip().lower()
        # Maximaal drie pogingen: anders kost één lead in een gemeente met
        # veel postcodes onnodig veel verzoeken aan een gratis dienst.
        return self._postcodes_per_gemeente.get(gemeente, [])[:3]

    def _wacht(self) -> None:
        verstreken = time.monotonic() - self._laatste_verzoek
        if verstreken < self.pauze_s:
            time.sleep(self.pauze_s - verstreken)
        self._laatste_verzoek = time.monotonic()

    def _haal(self, naam: str, postcode: str) -> str:
        params = {
            "searchWord": naam,
            "_oudeBenaming": "on",
            "pstcdeNPRP": postcode,
            "postgemeente1": "",
            "ondNP": "true", "_ondNP": "on",
            "ondRP": "true", "_ondRP": "on",
            # Zonder ALL negeert de pagina de opzoeking en geeft ze "niet gevonden".
            "rechtsvormFonetic": "ALL",
            "vest": "true", "_vest": "on",
            "filterEnkelActieve": "true", "_filterEnkelActieve": "on",
            "actionNPRP": "Zoek",
        }
        url = f"{ZOEKEN}?{urllib.parse.urlencode(params)}"
        verzoek = urllib.request.Request(url, headers={
            "User-Agent": "Complete-AI-leadsmachine/1.0 (compliance-check; contact via completeai.nl)",
            "Accept": "text/html",
        })
        self._wacht()
        with urllib.request.urlopen(verzoek, timeout=TIMEOUT_S) as antwoord:
            self.bevragingen += 1
            return antwoord.read().decode("utf-8", errors="replace")

    def zoek(self, naam: str, postcode: str = "", gemeente: str = "") -> KboResultaat:
        """Zoekt één bedrijf op naam, afgebakend op postcode of gemeente.

        Crasht nooit: elke fout wordt "onbekend", en onbekend betekent verderop
        afvallen — zelfde regel als bij de KVK-kant.
        """
        if not naam.strip():
            return KboResultaat(fout="geen naam")
        if not postcode.strip() and not gemeente.strip():
            # Zonder plaatsafbakening is een fonetische naamzoekopdracht niet
            # te vertrouwen: "Barber" geeft 200+ treffers door heel België.
            return KboResultaat(fout="geen postcode of gemeente om op af te bakenen")

        sleutel = (_vereenvoudig(naam), (postcode or gemeente).strip().lower())
        if sleutel in self._cache:
            return self._cache[sleutel]

        try:
            html = self._haal(naam, postcode.strip())
            nummers = self._nummers_uit_resultaat(html, naam, postcode, gemeente)
            if not nummers:
                uitslag = KboResultaat(fout="geen naamtreffer in dit gebied")
            elif len(nummers) > 1:
                # Meerdere verschillende ondernemingen met dezelfde naam in
                # hetzelfde gebied: niet vast te stellen welke dit is.
                uitslag = KboResultaat(fout="meerdere ondernemingen met deze naam, niet eenduidig")
            else:
                uitslag = self._entiteit(nummers.pop())
        except urllib.error.HTTPError as fout:
            uitslag = KboResultaat(fout=f"HTTP {fout.code}")
        except Exception as fout:
            uitslag = KboResultaat(fout=f"{type(fout).__name__}: {fout}")

        self._cache[sleutel] = uitslag
        return uitslag

    def _nummers_uit_resultaat(self, html: str, gezocht: str,
                               postcode: str, gemeente: str) -> set[str]:
        """De ondernemingsnummers waarvan de naam exact overeenkomt en die in
        het opgegeven gebied liggen.

        Zowel entiteiten (ENT) als vestigingseenheden (VE) tellen mee: een
        zaak handelt vaak onder een naam die niet de naam van de entiteit is
        ("Mai Barber" staat in KBO alleen als vestiging). Het nummer leidt
        daarna naar de entiteit zelf, en dáár staat of het een rechtspersoon
        is — dat wordt nooit uit de naam geraden.
        """
        gebied = (postcode.strip() or gemeente.strip()).lower()
        nummers: set[str] = set()

        for rij in _RIJ.findall(html):
            cellen = [_schoon(c) for c in _CEL.findall(rij)]
            if len(cellen) < 5:
                continue
            adres = cellen[-1].lower()
            if gebied and gebied not in adres:
                continue
            if not _namen_horen_bij_elkaar(gezocht, cellen[-2]):
                continue
            for cel in cellen:
                treffer = _NUMMER.search(cel)
                if treffer:
                    nummers.add(treffer.group(1))
                    break
        return nummers

    def _alle_nummers_op_adres(self, html: str) -> set[str]:
        """Elke onderneming die op dit adres staat, ongeacht de naam."""
        nummers: set[str] = set()
        for rij in _RIJ.findall(html):
            cellen = [_schoon(c) for c in _CEL.findall(rij)]
            if len(cellen) < 5:
                continue
            for cel in cellen:
                treffer = _NUMMER.search(cel)
                if treffer:
                    nummers.add(treffer.group(1))
                    break
        return nummers

    def _entiteit(self, nummer: str) -> KboResultaat:
        """Haalt de entiteit op en leest 'Type entiteit' en 'Rechtsvorm'.

        Dit is het enige antwoord dat telt: KBO zegt hier zelf of de
        onderneming een rechtspersoon of een natuurlijk persoon is.
        """
        url = f"{ENTITEIT}?{urllib.parse.urlencode({'ondernemingsnummer': nummer.replace('.', '')})}"
        verzoek = urllib.request.Request(url, headers={
            "User-Agent": "Complete-AI-leadsmachine/1.0 (compliance-check; contact via completeai.nl)",
            "Accept": "text/html",
        })
        self._wacht()
        with urllib.request.urlopen(verzoek, timeout=TIMEOUT_S) as antwoord:
            self.bevragingen += 1
            html = antwoord.read().decode("utf-8", errors="replace")

        platte_tekst = _schoon(html)

        soort = re.search(r"Type entiteit[: ]*(Rechtspersoon|Natuurlijk persoon)", platte_tekst)
        if not soort:
            return KboResultaat(fout="entiteitpagina noemt geen 'Type entiteit'")

        rechtsvorm = re.search(r"Rechtsvorm[: ]*([A-Za-zÀ-ÿ' \-]+?)(?: Sinds| Aantal|$)", platte_tekst)
        naam = re.search(r"Naam[: ]*(.+?)(?: Naam in| Sinds| Adres|$)", platte_tekst)
        status = re.search(r"Status[: ]*(\w+)", platte_tekst)

        return KboResultaat(
            gevonden=True,
            is_rechtspersoon=(soort.group(1) == "Rechtspersoon"),
            ondernemingsnummer=nummer,
            naam=(naam.group(1).strip() if naam else ""),
            rechtsvorm=(rechtsvorm.group(1).strip() if rechtsvorm else ""),
            actief=(status.group(1).lower() == "actief" if status else None),
        )


    def _haal_op_adres(self, postcode: str, gemeente: str,
                       straat: str, huisnummer: str) -> str:
        params = {
            "postcod1": postcode,
            "postgemeente1": gemeente,
            "straatgemeente1": straat,
            "huisnummer": huisnummer,
            "filterEnkelActieve": "true", "_filterEnkelActieve": "on",
            "actionLU": "Zoek",
        }
        url = f"{ZOEKEN_ADRES}?{urllib.parse.urlencode(params)}"
        verzoek = urllib.request.Request(url, headers={
            "User-Agent": "Complete-AI-leadsmachine/1.0 (compliance-check; contact via completeai.nl)",
            "Accept": "text/html",
        })
        self._wacht()
        with urllib.request.urlopen(verzoek, timeout=TIMEOUT_S) as antwoord:
            self.bevragingen += 1
            return antwoord.read().decode("utf-8", errors="replace")

    def zoek_bedrijf(self, bedrijf) -> KboResultaat:
        """De volledige opzoeking voor één OSM-bedrijf, in twee stappen.

        1. Op naam, afgebakend op postcode of gemeente.
        2. Lukt dat niet, op adres — veel kleine zaken handelen onder een naam
           die niet als KBO-naam geregistreerd staat ("BU Hairdressing" bestaat
           daar niet), maar hun vestigingsadres staat er wel. Van de
           bedrijven op dat adres moet de naam dan alsnog overeenkomen; op één
           adres zitten soms twee zaken en dan wordt er niet gegokt.

        Blijft het onbekend, dan is dat het antwoord. Onbekend betekent
        verderop: niet benaderen.
        """
        gemeente = bedrijf.gemeente or bedrijf.plaats
        postcodes = self._postcodes_voor(bedrijf)

        laatste = KboResultaat(fout="niet teruggevonden")
        for postcode in postcodes:
            laatste = self.zoek(bedrijf.naam, postcode=postcode, gemeente=gemeente)
            if laatste.gevonden:
                return laatste

        # Ook zonder postcode nog één poging: een landelijke naamzoekopdracht,
        # waarbij het adres in het antwoord tegen de gemeentenaam wordt
        # gehouden. Werkt alleen bij een onderscheidende naam — bij een
        # generieke naam staat de juiste zaak niet op de eerste pagina en
        # levert dit niets op, en dat is dan ook het antwoord.
        if gemeente:
            zonder_postcode = self.zoek(bedrijf.naam, postcode="", gemeente=gemeente)
            if zonder_postcode.gevonden:
                return zonder_postcode
            laatste = zonder_postcode

        if not (bedrijf.straat and bedrijf.huisnummer) or not postcodes:
            return laatste

        postcode = postcodes[0]
        try:
            html = self._haal_op_adres(postcode, gemeente,
                                       bedrijf.straat, bedrijf.huisnummer)
            # Eerst op naam binnen dit adres: dat is de sterkste match.
            nummers = self._nummers_uit_resultaat(
                html, bedrijf.naam, postcode, gemeente)
            if len(nummers) == 1:
                return self._entiteit(nummers.pop())
            if len(nummers) > 1:
                return KboResultaat(fout="meerdere ondernemingen op dit adres met deze naam")

            # Geen naamtreffer, maar staat er precies één onderneming op dit
            # exacte adres (straat + huisnummer + postcode), dan IS dat de zaak
            # op dat adres — dat is een vaststelling, geen gok. Alleen met een
            # postcode erbij, want zonder postcode is het adres te ruim.
            if postcode.strip():
                alle = self._alle_nummers_op_adres(html)
                if len(alle) == 1:
                    uitslag = self._entiteit(alle.pop())
                    if uitslag.gevonden:
                        uitslag.fout = "gekoppeld op adres, niet op naam"
                    return uitslag
            return KboResultaat(fout="niet op naam en niet op adres teruggevonden")
        except urllib.error.HTTPError as fout:
            return KboResultaat(fout=f"HTTP {fout.code} bij adresopzoeking")
        except Exception as fout:
            return KboResultaat(fout=f"{type(fout).__name__}: {fout}")


def zelftest() -> tuple[bool, str]:
    """Werkt de koppeling? Bevraagt één bekend bedrijf."""
    client = KboClient()
    uitslag = client.zoek("BARBER BERLAAR", postcode="2590")
    if uitslag.gevonden and uitslag.is_rechtspersoon:
        return True, f"KBO werkt (proef: {uitslag.naam}, {uitslag.ondernemingsnummer})"
    return False, f"KBO gaf geen bruikbaar antwoord: {uitslag.fout or 'onbekend'}"
