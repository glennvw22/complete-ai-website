"""Wie mag je bellen, wie mag je mailen, en wie helemaal niet.

Elke lead krijgt hier één baan:

    BEL   mag nu gebeld worden
    MAIL  mag nu gemaild worden, nog niet gebeld
    AF    valt af, om een reden die erbij staat

Dit bestand is bewust streng: alles waarvan we het NIET zeker weten valt af.
Een lijst die je zonder nadenken kunt afbellen is meer waard dan een langere
lijst waar je bij elke regel moet twijfelen.

NEDERLAND — koud bellen mag alleen naar rechtspersonen (bv, nv, stichting,
vereniging, coöperatie), bevestigd met de rechtsvorm uit het KVK-basisprofiel.
Een eenmanszaak, vof, cv of maatschap is een natuurlijk persoon en valt onder
het bel-me-niet-regime. Die gaan hier NIET naar de mailbaan: of koude e-mail
naar een NL-eenmanszaak zonder opt-in mag, is in de kluis een openstaande
vraag met twee bronnen die elkaar tegenspreken. Niet aannemen — dus AF tot dat
beslecht is.

BELGIË — zakelijk bellen mag, maar alleen na het schonen van de DNCM-lijst
(donotcallme.be), en die lijst is voor derden alleen tegen betaling te
raadplegen. Nagezocht 13-9-2026 bij vier onafhankelijke bronnen; er is geen
gratis route en geen vrijstelling voor kleine bedrijven. Complete AI gaat geen
nieuwe vaste lasten aan, dus telefoon is hier niet de eerste stap. Wat wél
gratis en wettelijk kan:

  1. KBO zegt gratis of een Belgisch bedrijf een rechtspersoon is (kbo.py).
  2. Naar een ONPERSOONLIJK adres van een Belgische rechtspersoon mag
     ongevraagde commerciële e-mail zonder voorafgaande toestemming
     (art. XII.13 WER + KB 4-4-2003). Dus: MAIL-baan.
  3. Geeft dat bedrijf daarna een expliciete, gedateerde opt-in voor telefoon,
     dan mag er gebeld worden — ook als het nummer op de DNCM-lijst staat.
     DNCM zegt dat zelf: *"Wanneer een abonnee zich op de Bel-Me-Niet-Meer
     lijst inschrijft en nadien een opt-in geeft, dan is het de opt-in die
     prioritair is."* Dus: BEL, zonder de lijst ooit te hoeven kopen.

Let op de richting van die laatste regel: de LAATSTE handeling van de abonnee
is beslissend. Een opt-in is dus geen eeuwig recht — zie opt_in_geldig().
"""
from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass

# Uit het KVK-antwoord: deze typen inschrijving zijn rechtspersonen.
ZOEKTYPE_RECHTSPERSOON = ("rechtspersoon",)

BEL, MAIL, AF = "BEL", "MAIL", "AF"

# Hoe lang een telefonische opt-in meegaat. Omdat de laatste handeling van de
# abonnee voorgaat, kan iemand zich ná zijn opt-in alsnog op de DNCM-lijst
# zetten; zonder licentie zien wij dat niet. Daarom een korte houdbaarheid:
# bel snel na de opt-in, of vraag opnieuw. 90 dagen is een eigen keuze, geen
# wettelijke termijn — als daar ooit een bron voor is, vervang deze regel.
OPT_IN_GELDIG_DAGEN = 90

# Alleen deze voorvoegsels gelden als onpersoonlijk adres van een organisatie.
# Bewust een korte lijst: bij twijfel is het adres persoonlijk en mag het niet.
ONPERSOONLIJKE_VOORVOEGSELS = frozenset({
    "info", "contact", "hello", "hallo", "sales", "verkoop", "office",
    "kantoor", "admin", "administratie", "boekhouding", "mail", "post",
    "welkom", "onthaal", "reservatie", "reservaties", "boeking", "boekingen",
    "shop", "winkel", "salon", "praktijk", "balie", "klantendienst",
    "klantenservice", "support", "service", "team", "bestellingen",
})


@dataclass
class Beloordeel:
    mag_bellen: bool
    reden: str
    let_op: str = ""
    baan: str = AF
    mag_mailen: bool = False


def onpersoonlijk_adres(email: str) -> bool:
    """Is dit een onpersoonlijk adres van een organisatie (info@, contact@)?

    De Belgische uitzondering op het spamverbod geldt alleen voor zulke
    adressen; een persoonlijk adres (voornaam.achternaam@) is een
    persoonsgegeven en vraagt toestemming. Bij twijfel: nee.
    """
    email = (email or "").strip().lower()
    if not email or "@" not in email:
        return False
    lokaal = email.split("@", 1)[0]
    kern = re.split(r"[.\-_+]", lokaal)[0]
    return kern in ONPERSOONLIJKE_VOORVOEGSELS


def opt_in_geldig(opt_in_datum, vandaag=None) -> bool:
    """Is er een opt-in die nog meegaat? Geen datum = geen opt-in."""
    if not opt_in_datum:
        return False
    if isinstance(opt_in_datum, str):
        try:
            opt_in_datum = _dt.date.fromisoformat(opt_in_datum[:10])
        except ValueError:
            return False
    if isinstance(opt_in_datum, _dt.datetime):
        opt_in_datum = opt_in_datum.date()
    vandaag = vandaag or _dt.date.today()
    if opt_in_datum > vandaag:
        return False
    return (vandaag - opt_in_datum).days <= OPT_IN_GELDIG_DAGEN


def beoordeel_belbaarheid(bedrijf, kvk_resultaat, dncm_resultaat=None,
                          kbo_resultaat=None, opt_in_datum=None) -> Beloordeel:
    """bedrijf: bron_osm.Bedrijf. De overige argumenten zijn verrijkingen die
    ontbreken mogen; ontbreken betekent altijd "strenger", nooit "ruimer".

    kvk_resultaat  kvk.KvkResultaat of None   — NL, rechtsvorm
    dncm_resultaat dncm.DncmResultaat of None — BE, staat het nummer op de lijst
    kbo_resultaat  kbo.KboResultaat of None   — BE, is het een rechtspersoon
    opt_in_datum   date/str of None           — BE, expliciete toestemming
    """
    if bedrijf.land == "BE":
        return _beoordeel_be(bedrijf, dncm_resultaat, kbo_resultaat, opt_in_datum)
    return _beoordeel_nl(bedrijf, kvk_resultaat)


def _beoordeel_be(bedrijf, dncm_resultaat, kbo_resultaat, opt_in_datum) -> Beloordeel:
    # 1. Een geldige opt-in gaat vóór de DNCM-lijst. Dan mag er gebeld worden,
    #    ook zonder dat wij die lijst ooit hebben gezien.
    if bedrijf.telefoon and opt_in_geldig(opt_in_datum):
        return Beloordeel(
            True,
            "expliciete opt-in voor telefonisch contact, gedateerd — die gaat "
            "vóór de DNCM-lijst",
            baan=BEL, mag_mailen=True,
        )

    # 2. Is de lijst wél te bevragen (betaalde koppeling actief), dan beslist
    #    het antwoord daarvan.
    if bedrijf.telefoon and dncm_resultaat is not None and dncm_resultaat.gevonden:
        if dncm_resultaat.op_lijst:
            return Beloordeel(
                False, "staat op de DNCM-lijst (donotcallme.be) — niet bellen", baan=AF
            )
        return Beloordeel(
            True,
            "automatisch tegen de DNCM-lijst gecontroleerd (donotcallme.be) — "
            "niet gevonden, bellen mag",
            baan=BEL, mag_mailen=True,
        )

    # 3. Geen opt-in en geen lijst: bellen kan niet gegarandeerd worden.
    #    Dan is de vraag of dit bedrijf gemaild mag worden, en daarvoor moet
    #    het een rechtspersoon zijn met een onpersoonlijk adres.
    if kbo_resultaat is None or not kbo_resultaat.gevonden:
        return Beloordeel(
            False,
            "rechtsvorm niet in KBO teruggevonden — zonder rechtsvorm geen "
            "grond om te bellen of te mailen",
            baan=AF,
        )
    if kbo_resultaat.is_rechtspersoon is not True:
        return Beloordeel(
            False,
            "natuurlijk persoon volgens KBO — niet bellen zonder DNCM-controle, "
            "en niet mailen zonder opt-in",
            baan=AF,
        )
    if not onpersoonlijk_adres(bedrijf.email):
        return Beloordeel(
            False,
            f"rechtspersoon ({kbo_resultaat.rechtsvorm or 'vorm onbekend'}) maar geen "
            "onpersoonlijk e-mailadres — zonder info@-achtig adres geen grond "
            "om ongevraagd te mailen",
            baan=AF,
        )
    return Beloordeel(
        False,
        f"rechtspersoon ({kbo_resultaat.rechtsvorm or 'vorm onbekend'}) met "
        "onpersoonlijk adres — ongevraagde zakelijke e-mail mag; bellen pas na "
        "een expliciete opt-in",
        let_op="Nog niet bellen: eerst opt-in via e-mail vragen",
        baan=MAIL, mag_mailen=True,
    )


def _beoordeel_nl(bedrijf, kvk_resultaat) -> Beloordeel:
    if not bedrijf.telefoon:
        return Beloordeel(False, "geen telefoonnummer gevonden", baan=AF)

    if kvk_resultaat is None or not kvk_resultaat.gevonden:
        return Beloordeel(False, "niet in KVK teruggevonden, rechtsvorm onbekend", baan=AF)

    if kvk_resultaat.is_rechtspersoon is True:
        return Beloordeel(
            True, f"rechtspersoon ({kvk_resultaat.rechtsvorm}) — koud bellen toegestaan",
            baan=BEL, mag_mailen=True,
        )
    if kvk_resultaat.is_rechtspersoon is False:
        return Beloordeel(
            False, f"natuurlijk persoon ({kvk_resultaat.rechtsvorm}) — niet bellen",
            baan=AF,
        )

    # Rechtsvorm onbekend, maar de gratis zoekstap zei wel 'rechtspersoon'.
    # Dat is een aanwijzing, geen bewijs: te zwak om op te bellen.
    if kvk_resultaat.zoek_type in ZOEKTYPE_RECHTSPERSOON:
        return Beloordeel(
            False,
            "KVK noemt het een rechtspersoon maar de rechtsvorm is niet opgehaald — "
            "te onzeker om te bellen",
            baan=AF,
        )
    return Beloordeel(False, "rechtsvorm onbekend — bij twijfel niet bellen", baan=AF)


def kandidaat_voor_kvk(bedrijf) -> bool:
    """Is het de moeite waard om hier een betaalde KVK-bevraging aan te wagen?

    Zonder telefoonnummer wordt het toch nooit een belbare lead, dus dan is de
    bevraging weggegooid geld.
    """
    return bool(bedrijf.telefoon) and bedrijf.land == "NL"


def kandidaat_voor_kbo(bedrijf, dncm_beschikbaar: bool = False) -> bool:
    """Loont een KBO-opzoeking?

    De opzoeking is gratis maar niet gratis in tijd: KBO Public Search wordt
    bewust op één verzoek per seconde bevraagd. Dus alleen opzoeken waar het
    tot een lead kán leiden.

    Zonder DNCM-koppeling loopt de enige weg naar een Belgische lead via een
    e-mail naar een onpersoonlijk adres — geen zo'n adres, geen lead, hoe
    netjes de rest ook is. Met een werkende DNCM-koppeling telt een
    telefoonnummer weer wel, want dan kan er rechtstreeks gebeld worden.
    """
    if bedrijf.land != "BE":
        return False
    if onpersoonlijk_adres(bedrijf.email):
        return True
    return dncm_beschikbaar and bool(bedrijf.telefoon)
