"""De poort: niets komt erdoor zonder letterlijk bewijs in de invoer.

Harvey (het open-source voorbeeld) heeft zo'n poort wél voor de vorm van
een mail — lengte, verboden zinnen, één link — maar controleert nergens
of de feiten in die mail ergens vandaan komen. Dat is precies het gat dat
ons de vorige keer geld en geloofwaardigheid kostte.

Hier is de volgorde omgedraaid: een prospect komt de wachtrij niet in
tenzij elk van deze zeven controles slaagt. Bij twijfel valt hij af, met
de reden erbij. Een lege wachtrij is beter dan een verkeerde mail.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from . import signalen as sig

MAX_ONDERBOUWING = 320
# Geen gedachtestreepjes, geen beloftes in procenten, niet openen met "AI"
# of met onze eigen naam: huisregels uit de kluis, hier hard gemaakt.
_GEDACHTESTREEPJE = re.compile(r"\s[—–]\s")
_PROCENT = re.compile(r"\d+\s*(%|procent)", re.I)
_JIJVORM = re.compile(r"\b(je|jij|jouw|jou|jullie)\b", re.I)
_OPENING_VERBODEN = ("ai", "complete ai", "completeai")


@dataclass
class Oordeel:
    doorgelaten: bool
    redenen: list[str] = field(default_factory=list)

    def weiger(self, reden: str) -> "Oordeel":
        self.doorgelaten = False
        self.redenen.append(reden)
        return self


def _domein(adres_of_url: str) -> str:
    tekst = (adres_of_url or "").strip().lower()
    if "@" in tekst:
        tekst = tekst.rsplit("@", 1)[1]
    tekst = re.sub(r"^https?://", "", tekst).split("/")[0]
    return tekst[4:] if tekst.startswith("www.") else tekst


def controleer_bewijs(gevonden: list[sig.Signaal], dossier) -> Oordeel:
    """Elke aanwezigheidsclaim moet letterlijk terug te vinden zijn."""
    oordeel = Oordeel(True)
    aanwezig = [s for s in gevonden if s.soort == sig.AANWEZIG]

    for signaal in gevonden:
        if signaal.soort == sig.AANWEZIG:
            if not signaal.citaat.strip():
                oordeel.weiger(f"signaal '{signaal.sleutel}' heeft geen citaat")
                continue
            if dossier.vind(signaal.citaat) is None:
                oordeel.weiger(
                    f"citaat van '{signaal.sleutel}' staat op geen enkele opgehaalde "
                    f"pagina — mogelijk verzonnen of verouderd")
            elif not signaal.bron_url or not signaal.bron_datum:
                oordeel.weiger(f"signaal '{signaal.sleutel}' mist bron_url of bron_datum")
        else:
            if not dossier.bezochte_urls:
                oordeel.weiger(
                    f"afwezigheidssignaal '{signaal.sleutel}' terwijl er geen enkele "
                    f"pagina gelezen is")
            elif not all(u in signaal.zin for u in dossier.bezochte_urls):
                oordeel.weiger(
                    f"afwezigheidssignaal '{signaal.sleutel}' noemt niet welke pagina's "
                    f"gelezen zijn")

    if not aanwezig:
        oordeel.weiger(
            "geen enkel signaal dat we letterlijk kunnen aanwijzen; wat ontbreekt "
            "op een paar pagina's is geen reden om iemand te benaderen")
    return oordeel


def controleer_wet(email: str, rechtsvorm: str | None, rechtsvorm_citaat: str,
                   bron_url: str, dossier, onpersoonlijk_adres) -> Oordeel:
    """Mag dit bedrijf zonder opt-in een koude e-mail krijgen?

    `onpersoonlijk_adres` wordt meegegeven zodat we de bestaande regel uit
    belbaar.py hergebruiken in plaats van hem hier over te typen.
    """
    oordeel = Oordeel(True)
    adres = (email or "").strip().lower()

    if not adres:
        return oordeel.weiger("geen e-mailadres gevonden")
    if not onpersoonlijk_adres(adres):
        oordeel.weiger(f"'{adres}' is een persoonlijk adres; zonder opt-in mag dat niet")

    if not rechtsvorm:
        oordeel.weiger(
            "rechtsvorm staat niet op de eigen site; zonder bewijs dat dit een "
            "rechtspersoon is, niet mailen")
    elif not sig.is_rechtspersoon(rechtsvorm):
        oordeel.weiger(f"rechtsvorm '{rechtsvorm}' is geen rechtspersoon; niet mailen")
    elif not rechtsvorm_citaat.strip() or dossier.vind(rechtsvorm_citaat) is None:
        oordeel.weiger("bewijs voor de rechtsvorm is niet terug te vinden op de site")

    if not bron_url:
        oordeel.weiger("geen bron-URL bij het e-mailadres")
    elif bron_url not in dossier.bezochte_urls:
        oordeel.weiger("het adres komt niet van een pagina die wij zelf gelezen hebben")
    elif _domein(adres) != _domein(bron_url) and not _domein(adres).endswith(
            "." + _domein(bron_url)):
        oordeel.weiger(
            f"domein van het adres ({_domein(adres)}) hoort niet bij de site "
            f"({_domein(bron_url)})")
    return oordeel


def controleer_toon(onderbouwing: str) -> Oordeel:
    """De onderbouwing gaat als zin de mail in, dus de huisregels gelden."""
    oordeel = Oordeel(True)
    tekst = (onderbouwing or "").strip()

    if not tekst:
        return oordeel.weiger("lege onderbouwing")
    if len(tekst) > MAX_ONDERBOUWING:
        oordeel.weiger(f"onderbouwing is {len(tekst)} tekens, meer dan {MAX_ONDERBOUWING}")
    if _GEDACHTESTREEPJE.search(tekst):
        oordeel.weiger("onderbouwing bevat een gedachtestreepje")
    if _PROCENT.search(tekst):
        oordeel.weiger("onderbouwing belooft een percentage")
    if _JIJVORM.search(tekst):
        oordeel.weiger("onderbouwing gebruikt de jij-vorm in plaats van u")
    # Ook een opening van twee woorden ("Complete AI ...") moet eruit,
    # dus vergelijken we het begin van de zin, niet alleen het eerste woord.
    begin = re.sub(r"[^a-z ]", "", tekst.lower()).strip()
    for verboden in _OPENING_VERBODEN:
        if begin == verboden or begin.startswith(verboden + " "):
            oordeel.weiger(f"onderbouwing opent met '{verboden}'")
            break
    return oordeel


def controleer_uitsluiting(email: str, uitgesloten: set[str]) -> Oordeel:
    oordeel = Oordeel(True)
    if (email or "").strip().lower() in {u.strip().lower() for u in uitgesloten}:
        oordeel.weiger("adres staat op de uitsluitingslijst")
    return oordeel


def beoordeel(*oordelen: Oordeel) -> Oordeel:
    """Alle deeloordelen samen. Eén weigering is genoeg."""
    samen = Oordeel(True)
    for deel in oordelen:
        if not deel.doorgelaten:
            samen.doorgelaten = False
        samen.redenen.extend(deel.redenen)
    return samen
