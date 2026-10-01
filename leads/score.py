"""Scoring: van één criterium naar zes koopsignalen.

De oude routine had één vraag: "heeft dit bedrijf een slechte website?" Als het
antwoord nee was, viel de lead weg. Dat is de reden dat er dagen waren zonder
leads en dat het aanbod van Complete AI maar voor een fractie werd verkocht.

Hier krijgt elk bedrijf per DIENST een signaalscore. Een bedrijf met een
prima website kan nog steeds een uitstekende lead zijn voor de AI-telefonist of
voor automatisering. Er wordt niet meer hard weggegooid: er wordt gerangschikt,
met een eerlijke zekerheidsmarkering erbij.
"""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field

from catalogus import Branche, DIENSTEN

HUIDIG_JAAR = _dt.date.today().year


@dataclass
class Signaal:
    dienst: str          # sleutel uit DIENSTEN
    punten: int          # 0-100, hoe sterk dit koopsignaal is
    reden: str           # in gewoon Nederlands, gaat zo het gesprek in
    hard: bool = True    # False = afgeleid/aanname, niet keihard aangetoond


@dataclass
class Warmte:
    """Aanwijzingen dat dit bedrijf NU met het onderwerp bezig is.

    Belangrijk om eerlijk over te zijn: wie er op internet naar "website laten
    maken" heeft gezocht, is niet te achterhalen. Zoekgedrag van bedrijven is
    geen openbare data; dat is precies wat je bij Google Ads koopt. Wat hier
    staat zijn waarneembare sporen die dezelfde kant op wijzen.
    """
    punten: int = 0
    redenen: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        if self.punten >= 45:
            return "warm"
        if self.punten >= 20:
            return "lauw"
        return "koud"


@dataclass
class Beoordeling:
    signalen: list[Signaal] = field(default_factory=list)
    score: int = 0
    beste_dienst: str = ""
    zekerheid: str = "laag"     # hoog / midden / laag
    bereikbaar: bool = False
    warmte: Warmte = field(default_factory=Warmte)

    @property
    def redenen(self) -> str:
        return " | ".join(f"{s.reden}" for s in self.signalen[:4])

    @property
    def alle_redenen(self) -> str:
        """Elke reden, genummerd - dit is wat Glenn voor zich heeft bij het bellen."""
        return " ".join(
            f"{i}. {s.reden} [{DIENSTEN.get(s.dienst, s.dienst)}]"
            for i, s in enumerate(self.signalen, 1)
        )

    @property
    def diensten_op_volgorde(self) -> list[str]:
        gezien, uit = set(), []
        for s in self.signalen:
            if s.dienst not in gezien:
                gezien.add(s.dienst)
                uit.append(s.dienst)
        return uit

    def heeft_dienst(self, sleutel: str) -> bool:
        return any(s.dienst == sleutel for s in self.signalen)

    @property
    def website_gat(self) -> bool:
        """Geen website, een website die niet werkt of een gebrek heeft - de klassieke ingang."""
        return any(s.dienst == "website" for s in self.signalen)


def _bepaal_warmte(bedrijf, site, kvk_resultaat, branche: Branche) -> Warmte:
    warmte = Warmte()

    def voeg_toe(punten: int, reden: str):
        warmte.punten += punten
        warmte.redenen.append(reden)

    if site is not None:
        if site.geparkeerd:
            voeg_toe(45, "Domein staat geparkeerd of 'binnenkort online' - ze zijn "
                         "er zelf al mee bezig maar komen er niet uit")
        if not site.bereikbaar and not site.geblokkeerd and bedrijf.website:
            voeg_toe(40, "De website die ze opgeven doet het niet - dat kost ze nu klanten")
        # Een copyrightjaar zegt niets over de site: dat staat hier sinds 1-10-2026
        # (websitekeuring in het dashboard) niet meer als reden. Wat telt is wat een
        # bezoeker ziet, en dat meet de keuring, in een echte Chrome.

    if bedrijf.social and not bedrijf.website:
        voeg_toe(30, "Wel actief op social, geen eigen site - ze investeren al in "
                     "online zichtbaarheid, alleen op de verkeerde plek")

    if bedrijf.email and not bedrijf.website:
        voeg_toe(15, "Heeft wel een zakelijk mailadres maar geen site")

    if branche.online_afspraak and site is not None and site.bereikbaar \
            and not site.online_afspraak:
        voeg_toe(20, "Klanten kunnen niet online boeken of bestellen, terwijl de "
                     "concurrent dat wel biedt")

    if branche.beldruk >= 0.9 and not bedrijf.openingstijden \
            and "24/7" not in (bedrijf.openingstijden or ""):
        voeg_toe(15, "Hoge belbranche zonder gepubliceerde openingstijden - "
                     "gemiste oproepen buiten kantooruren")

    # Vroeger stond hier: >1 vestiging = +20 punten, "groeiend bedrijf met
    # budget". Dat is precies omgekeerd gebleken (17/18-9-2026, n.a.v.
    # Boerenbond Roosendaal): een filiaal van een keten heeft geen
    # besluitvormer met marketingbudget op die locatie. Filialen worden nu al
    # vóór het basisprofiel uitgesloten (belbaar.is_filiaal, kostenfilter) en
    # aantal vestigingen krijgt daarom geen aparte score meer - een lead die
    # hier komt, is per definitie geen bekend filiaal meer.

    if kvk_resultaat is not None and kvk_resultaat.oprichtingsdatum:
        try:
            opgericht_jaar = int(kvk_resultaat.oprichtingsdatum[:4])
            leeftijd = HUIDIG_JAAR - opgericht_jaar
        except (ValueError, TypeError):
            leeftijd = None
        if leeftijd is not None and 1 <= leeftijd <= 10:
            voeg_toe(15, f"Bedrijf is {leeftijd} jaar oud (opgericht {opgericht_jaar}) - "
                         f"relatief jong, waarschijnlijk nog geen vaste marketingpartner")

    return warmte


def beoordeel(bedrijf, site, kvk_resultaat, branche: Branche) -> Beoordeling:
    """bedrijf: bron_osm.Bedrijf, site: website_check.SiteRapport | None."""
    signalen: list[Signaal] = []
    heeft_site_tag = bool(bedrijf.website)

    # ---------------- 1. WEBSITE ----------------
    if not heeft_site_tag and not bedrijf.social:
        signalen.append(Signaal("website", 85,
            "Geen website en geen socialpagina gevonden in de bronregistratie",
            hard=False))
    elif not heeft_site_tag and bedrijf.social:
        signalen.append(Signaal("website", 78,
            "Alleen een socialpagina als online visitekaartje, geen eigen site",
            hard=False))
    elif site is not None:
        if site.alleen_social:
            signalen.append(Signaal("website", 78,
                "De 'website' verwijst naar een socialpagina, geen eigen site"))
        elif site.geparkeerd:
            signalen.append(Signaal("website", 88,
                "Domein staat geparkeerd of in aanbouw"))
        elif site.geblokkeerd:
            # De site weert onze controle, meer weten we niet. "Uw website doet
            # het niet" is dan een bewering die aan de telefoon onderuit gaat,
            # dus hier komt geen koopsignaal uit. Zit er verder niets, dan valt
            # de lead vanzelf af wegens gebrek aan aanleiding.
            pass
        elif not site.bereikbaar:
            signalen.append(Signaal("website", 90,
                f"Website is onbereikbaar ({site.fout or 'geen antwoord'})"))
        # Een site die bereikbaar is, geeft hier GEEN website-reden meer. Het SSL-slotje, de
        # viewport (mobiel), laadtijd, copyrightjaar en bouwer zijn geen reden (Glenn, 1-10-2026):
        # niemand ziet ze, en een site die op een telefoon werkt en genoeg vertelt kan ze allemaal
        # missen. Het oordeel over een bestaande site komt uit de websitekeuring in het dashboard
        # (geen_site, stuk, onbruikbaar_mobiel of mager, door een mens bevestigd).

    # ---------------- 2. VINDBAARHEID (SEO) ----------------
    # Geen signaal meer (1-10-2026): een ontbrekende meta-omschrijving, structuurdata of
    # paginatitel is geen aantoonbare reden dat dit bedrijf iets van ons nodig heeft, en
    # "zonder site onvindbaar" volgt uit het websiteoordeel, niet uit een eigen SEO-regel.

    # ---------------- 3. AI-TELEFONIST ----------------
    # Alleen een signaal als er een echt bereikbaarheidsgat is. Een bedrijf dat
    # 24/7 opneemt heeft geen probleem dat wij oplossen; die op de lijst zetten
    # is tijdverspilling aan de telefoon.
    if bedrijf.telefoon and branche.beldruk >= 0.85:
        altijd_bereikbaar = "24/7" in (bedrijf.openingstijden or "")
        if not altijd_bereikbaar:
            beldruk_punten = int(branche.beldruk * 55)
            if not bedrijf.openingstijden:
                beldruk_punten += 8
                reden = (f"Telefoon is de hoofdingang in deze branche "
                         f"({branche.naam.lower()}) en er staan nergens "
                         f"openingstijden - onduidelijk wanneer er opgenomen wordt")
            else:
                beldruk_punten += 12
                reden = (f"Telefoon is de hoofdingang in deze branche "
                         f"({branche.naam.lower()}); buiten openingstijden "
                         f"({bedrijf.openingstijden}) gaat de telefoon niet op")
            signalen.append(Signaal("telefonist", min(beldruk_punten, 72),
                                    reden, hard=False))

    # ---------------- 4. AUTOMATISERING ----------------
    if branche.online_afspraak and not (site is not None and site.geblokkeerd):
        if site is None or not site.bereikbaar:
            signalen.append(Signaal("automatisering", 52,
                "Afspraken/bestellingen lopen volledig handmatig: geen online kanaal",
                hard=False))
        elif not site.online_afspraak:
            signalen.append(Signaal("automatisering", 58,
                "Site heeft geen online afspraak- of bestelmogelijkheid; alles gaat per telefoon",
                ))

    # ---------------- 5. SOCIAL ----------------
    if not bedrijf.social and branche.sleutel in ("horeca", "kapsalon", "detailhandel",
                                                  "sport", "gastvrij"):
        signalen.append(Signaal("social", 45,
            "Geen socialkanaal gevonden in een branche die daarvan leeft", hard=False))

    # ---------------- 6. ADVERTENTIES ----------------
    if branche.sleutel in ("installatie", "bouw", "garage", "hovenier", "transport") \
            and not (site is not None and site.geblokkeerd):
        if site is None or not site.bereikbaar:
            signalen.append(Signaal("sea", 40,
                "Spoed- en offerteaanvragen gaan nu naar concurrenten die wel adverteren",
                hard=False))

    # ---------------- samenvatten ----------------
    beoordeling = Beoordeling(signalen=sorted(signalen, key=lambda s: -s.punten))
    beoordeling.bereikbaar = bool(bedrijf.telefoon or bedrijf.email)

    if beoordeling.signalen:
        sterkste = beoordeling.signalen[0]
        beoordeling.beste_dienst = sterkste.dienst

        # Het sterkste signaal bepaalt de basis. De overige signalen tellen
        # beperkt mee: drie koopredenen zijn meer waard dan een, maar niet drie
        # keer zoveel. De wegingen zijn zo gekozen dat 100 zeldzaam blijft -
        # anders staat de halve lijst op 100 en zegt de score niets meer.
        basis = int(sterkste.punten * 0.8)
        breedte = min(sum(s.punten for s in beoordeling.signalen[1:]) // 4, 20)
        rauw = basis + breedte

        # Bereikbaarheid en compliance wegen mee: een lead die je niet kunt
        # bereiken is geen lead.
        if bedrijf.telefoon:
            rauw += 8
        if bedrijf.email:
            rauw += 4
        if not beoordeling.bereikbaar:
            rauw -= 30
        if kvk_resultaat is not None and kvk_resultaat.gevonden:
            rauw += 5
            if kvk_resultaat.is_rechtspersoon:
                rauw += 5   # mag koud gebeld worden

        beoordeling.score = max(0, min(100, rauw))

    beoordeling.warmte = _bepaal_warmte(bedrijf, site, kvk_resultaat, branche)

    harde = sum(1 for s in beoordeling.signalen if s.hard)
    if harde >= 2 and beoordeling.bereikbaar:
        beoordeling.zekerheid = "hoog"
    elif harde >= 1 or beoordeling.bereikbaar:
        beoordeling.zekerheid = "midden"

    return beoordeling


def dienstnaam(sleutel: str) -> str:
    return DIENSTEN.get(sleutel, sleutel)
