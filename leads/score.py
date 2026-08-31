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
class Beoordeling:
    signalen: list[Signaal] = field(default_factory=list)
    score: int = 0
    beste_dienst: str = ""
    zekerheid: str = "laag"     # hoog / midden / laag
    bereikbaar: bool = False

    @property
    def redenen(self) -> str:
        return " | ".join(f"{s.reden}" for s in self.signalen[:4])


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
        elif not site.bereikbaar:
            signalen.append(Signaal("website", 90,
                f"Website is onbereikbaar ({site.fout or 'geen antwoord'})"))
        else:
            gebreken, punten = [], 0
            if not site.https or site.ssl_fout:
                gebreken.append("geen werkend SSL-slotje")
                punten += 30
            if not site.mobiel_geschikt:
                gebreken.append("niet gebouwd voor mobiel")
                punten += 28
            if site.laadtijd_ms > 4000:
                gebreken.append(f"traag ({site.laadtijd_ms} ms)")
                punten += 16
            if site.copyright_jaar and HUIDIG_JAAR - site.copyright_jaar >= 3:
                gebreken.append(f"copyright staat nog op {site.copyright_jaar}")
                punten += 18
            if site.verouderde_techniek:
                gebreken.append("verouderde bouwer: " + ", ".join(site.verouderde_techniek))
                punten += 14
            if gebreken:
                signalen.append(Signaal("website", min(punten, 74),
                    "Site heeft " + ", ".join(gebreken)))

    # ---------------- 2. VINDBAARHEID (SEO) ----------------
    if site is not None and site.bereikbaar and not site.alleen_social:
        seo_gebreken, punten = [], 0
        if not site.heeft_meta_omschrijving:
            seo_gebreken.append("geen omschrijving voor Google")
            punten += 22
        if not site.heeft_structuurdata:
            seo_gebreken.append("geen structuurdata")
            punten += 18
        if not site.heeft_titel:
            seo_gebreken.append("geen paginatitel")
            punten += 25
        if seo_gebreken:
            signalen.append(Signaal("seo", min(punten, 62),
                "Vindbaarheid: " + ", ".join(seo_gebreken)))
    elif heeft_site_tag is False:
        signalen.append(Signaal("seo", 55,
            "Zonder eigen site is het bedrijf in Google vrijwel onvindbaar",
            hard=False))

    # ---------------- 3. AI-TELEFONIST ----------------
    if bedrijf.telefoon:
        beldruk_punten = int(branche.beldruk * 55)
        reden = f"Telefoon is de hoofdingang in deze branche ({branche.naam.lower()})"
        if not bedrijf.openingstijden:
            beldruk_punten += 8
        elif "24/7" not in bedrijf.openingstijden:
            beldruk_punten += 12
            reden += "; buiten openingstijden gaat de telefoon nu niet op"
        if branche.beldruk >= 0.85:
            signalen.append(Signaal("telefonist", min(beldruk_punten, 72), reden, hard=False))

    # ---------------- 4. AUTOMATISERING ----------------
    if branche.online_afspraak:
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
    if branche.sleutel in ("installatie", "bouw", "garage", "hovenier", "transport"):
        if site is None or not site.bereikbaar or (site and not site.heeft_meta_omschrijving):
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

    harde = sum(1 for s in beoordeling.signalen if s.hard)
    if harde >= 2 and beoordeling.bereikbaar:
        beoordeling.zekerheid = "hoog"
    elif harde >= 1 or beoordeling.bereikbaar:
        beoordeling.zekerheid = "midden"

    return beoordeling


def dienstnaam(sleutel: str) -> str:
    return DIENSTEN.get(sleutel, sleutel)
