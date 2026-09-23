"""DNCM-koppeling: checkt automatisch of een Belgisch telefoonnummer op de
Bel-Me-Niet-Meer lijst (donotcallme.be, wetgeving via Boek VI/XIV WER) staat.

Zonder deze koppeling (geen DNCM_API_SLEUTEL) blijft het oude gedrag: elke
Belgische lead krijgt de waarschuwing "DNCM-scrub vereist" mee in `let_op` en
moet in het dashboard met de hand afgevinkt worden vóór er gebeld wordt (zie
jarvis-dashboard/lib/belcontrole.ts). Met een werkende sleutel bevraagt deze
module de lijst zelf, per nummer, en vervalt dat handmatige vinkje: een lead
die niet op de lijst blijkt te staan komt direct als "vrij" in het dashboard,
een lead die er wél op staat wordt hier al hard geblokkeerd (net als een
Nederlandse eenmanszaak) en komt nooit als belbaar aan.

De DNCM-lijst is alleen te bevragen met een betaalde 'Adverteerder'-licentie
bij DNCM VZW (donotcallme.be/nl/licenties) — een account aanmaken en die
licentie kopen kan alleen Glenn zelf (zie Grenzen — Wat je nooit voor Glenn
doet). Ga daarna in dat account naar de optie "Integratie via API"; die geeft
een unieke "Secret Key". Zet die als DNCM_API_SLEUTEL in de sleutelkluis,
zelfde bestand en aanpak als KVK_API_KEY (zie kvk.py en INSTELLEN.md).

Het exacte verzoekformaat (eindpunt, headers, antwoord) van die API staat pas
ná activering in het account zelf — dat is dus nog niet in dit bestand
ingevuld. _bevraag() hieronder is de ene, duidelijk gemarkeerde plek waar dat
verzoek moet komen; tot die tijd geeft check_nummer() altijd "onbekend"
terug (nooit stilzwijgend "niet op de lijst"), dus valt alles automatisch
terug op de bestaande handmatige controle in het dashboard.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass

# Harde grens van DNCM zelf voor API-gebruik, zie hun FAQ "API gebruik : zijn
# er bepaalde begrenzingen op het gebruik van de API?" — 20 checks/minuut.
MAX_PER_MINUUT = 20

# Zelfde sleutelkluis als kvk.py — één bestand met alle lokale sleutels,
# buiten deze (openbare) repository, rechten 600.
SLEUTELKLUIS = os.path.expanduser("~/.config/complete-ai/.env")


def _uit_kluis(naam: str) -> str:
    """Lees een variabele uit de sleutelkluis. Nooit een fout, altijd een
    string: ontbreekt het bestand of de regel, dan is het antwoord leeg."""
    try:
        with open(SLEUTELKLUIS, "r", encoding="utf-8") as bestand:
            for regel in bestand:
                regel = regel.strip()
                if not regel or regel.startswith("#") or "=" not in regel:
                    continue
                sleutel, _, waarde = regel.partition("=")
                if sleutel.strip() == naam:
                    return waarde.strip().strip('"').strip("'")
    except OSError:
        pass
    return ""


@dataclass
class DncmResultaat:
    gevonden: bool  # kon de lijst daadwerkelijk bevraagd worden?
    op_lijst: bool | None = None  # None = onbekend/niet bevraagd
    fout: str = ""


class DncmClient:
    def __init__(self, sleutel: str | None = None):
        """Waar de sleutel vandaan komt, in deze volgorde:

        1. Meegegeven aan de constructor (voor tests).
        2. `DNCM_API_SLEUTEL` als omgevingsvariabele.
        3. `DNCM_API_SLEUTEL` uit de sleutelkluis ~/.config/complete-ai/.env.
        """
        if sleutel is not None:
            self.sleutel = sleutel
        else:
            self.sleutel = os.environ.get("DNCM_API_SLEUTEL", "") or _uit_kluis("DNCM_API_SLEUTEL")
        self.beschikbaar = bool(self.sleutel)
        self._laatste_aanroepen: list[float] = []
        self._cache: dict[str, DncmResultaat] = {}

    def _wacht_voor_ratelimiet(self) -> None:
        nu = time.monotonic()
        self._laatste_aanroepen = [t for t in self._laatste_aanroepen if nu - t < 60]
        if len(self._laatste_aanroepen) >= MAX_PER_MINUUT:
            wacht = 60 - (nu - self._laatste_aanroepen[0]) + 0.1
            if wacht > 0:
                time.sleep(wacht)
        self._laatste_aanroepen.append(time.monotonic())

    def check_nummer(self, telefoonnummer: str) -> DncmResultaat:
        """Bevraagt de DNCM-lijst voor één nummer. Crasht nooit: een fout in
        de koppeling betekent "onbekend", niet "niet op de lijst" — bij
        twijfel niet automatisch vrijgeven, precies zoals belbaar.py dat ook
        voor de KVK-rechtsvorm doet."""
        if not self.beschikbaar:
            return DncmResultaat(gevonden=False, fout="geen DNCM_API_SLEUTEL gezet")
        if not telefoonnummer:
            return DncmResultaat(gevonden=False, fout="geen telefoonnummer")
        if telefoonnummer in self._cache:
            return self._cache[telefoonnummer]
        self._wacht_voor_ratelimiet()
        try:
            resultaat = self._bevraag(telefoonnummer)
        except Exception as fout:
            resultaat = DncmResultaat(gevonden=False, fout=f"{type(fout).__name__}: {fout}")
        self._cache[telefoonnummer] = resultaat
        return resultaat

    # -- laag niveau --------------------------------------------------------
    def _bevraag(self, telefoonnummer: str) -> DncmResultaat:
        # TODO(Glenn, na aanschaf licentie + activeren "Integratie via API"):
        # vul hier het echte HTTP-verzoek in. Het eindpunt, de manier van
        # authenticeren met de Secret Key en het antwoordformaat staan in het
        # DNCM-account zelf (Instellingen → Integratie via API), niet publiek
        # gedocumenteerd — vandaar dat dit hier nog niet is ingevuld in
        # plaats van gegokt. Tot dan geeft dit altijd "onbekend" terug.
        raise NotImplementedError(
            "DNCM-eindpunt nog niet ingevuld in dncm.py — zie de TODO in _bevraag()"
        )
