"""Korte versie van de dienst- en gidspagina's (Glenn, 11-10-2026: korter en pakkender). De volledige tekst blijft in inhoud_paginas.py staan; hier staat
welke onderdelen op de site komen en hoeveel vragen. Terugzetten = deze lijst leeg laten of een onderdeel toevoegen."""
import re
from inhoud_kort import KORT
HOUD = {
 "websites.html": ["herkenbaar", "wat-u-krijgt", "twee-weken", "maatwerk"],
 "automatisering.html": ["korte-antwoord", "herkenbaar", "wat-er-kan", "werkwijze", "koppelingen"],
 "ai-telefonist.html": ["wat-is-het", "herkenbaar", "zo-klinkt-het", "agenda-doorschakelen", "veiligheid-avg", "de-wet"],
 "social-media.html": ["herkenbaar", "uitbesteden", "wat-u-krijgt", "goedkeuring", "werkwijze"],
 "vindbaarheid-seo.html": ["herkenbaar", "wat-u-krijgt", "werkwijze", "fouten", "rapportage"],
 "adverteren.html": ["herkenbaar", "wat-u-krijgt", "waarom-op-aanvraag", "voorstel", "werkwijze", "rapportage"],
 "ai-voor-uw-bedrijf.html": ["kort-antwoord", "wat-is-ai", "kiezen", "beginnen", "grens"],
 "bedrijfsprocessen-automatiseren-voorbeelden.html": ["wat-is-een-bedrijfsproces", "klanten-verkoop", "financien", "herkennen", "waar-begint-u"],
 "wat-is-workflow-automatisering.html": ["korte-antwoord", "taak-workflow-proces", "opbrengst", "beginnen-meten"],
 "ai-agent-voor-uw-bedrijf.html": ["wat-is-het", "taken", "de-wet", "beginnen"],
 "wat-kost-automatisering.html": ["korte-antwoord", "factoren", "voorbeeld", "voorstel", "laag-houden"],
}
AANTAL_VRAGEN = 5

def inkorten(paginas):
    # eerst de herschreven korte tekst over de lange heen zetten (inhoud_kort.py)
    for p in paginas:
        k = KORT.get(p["bestand"])
        if k:
            for veld, waarde in k.items(): p[veld] = waarde
            HOUD.pop(p["bestand"], None)
    weg = {}                                                    # pagina -> ids van onderdelen die er niet meer zijn
    for p in paginas:
        houd = HOUD.get(p["bestand"])
        if houd: weg[p["bestand"]] = {i for i in re.findall(r'<section id="([^"]+)"', p["inhoud"]) if i not in houd}
    for p in paginas:
        houd = HOUD.get(p["bestand"])
        if not houd: continue
        def naar(m):
            return m.group(0) if m.group(1) in houd else ""
        p["inhoud"] = re.sub(r'<section id="([^"]+)"[^>]*>.*?</section>\s*', naar, p["inhoud"], flags=re.S)
        p["vragen"] = list(p["vragen"])[:AANTAL_VRAGEN]
    # verwijzingen naar onderdelen die er niet meer zijn: een link op dezelfde pagina wordt gewone tekst, een link naar een andere pagina verwijst naar de pagina zelf
    for p in paginas:
        def zelf(m):
            return m.group(2) if m.group(1) in weg.get(p["bestand"], ()) else m.group(0)
        p["inhoud"] = re.sub(r'<a href="#([^"]+)"[^>]*>(.*?)</a>', zelf, p["inhoud"], flags=re.S)
        def anders(m):
            return f'href="{m.group(1)}"' if m.group(2) in weg.get(m.group(1), ()) else m.group(0)
        p["inhoud"] = re.sub(r'href="([a-z0-9\-]+\.html)#([^"]+)"', anders, p["inhoud"])
        p["vragen"] = [(q, re.sub(r'href="([a-z0-9\-]+\.html)#([^"]+)"', anders, re.sub(r'<a href="#([^"]+)"[^>]*>(.*?)</a>', zelf, a, flags=re.S))) for q, a in p["vragen"]]
        for k, v in list(p.items()):
            if isinstance(v, str) and k not in ("inhoud", "bestand"):
                v = re.sub(r'<a href="#([^"]+)"[^>]*>(.*?)</a>', zelf, v, flags=re.S)
                p[k] = re.sub(r'href="([a-z0-9\-]+\.html)#([^"]+)"', anders, v)
    return paginas
