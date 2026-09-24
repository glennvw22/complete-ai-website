#!/usr/bin/env python3
"""SEO-poort voor complete-ai.nl. Draaien na bouw-paginas.py en bouw-sitemap.py:

    python3 seo-poort.py

Controleert elke pagina op de eisen voor vindbaarheid én op de huisregels van
Glenn. Eindigt met een foutcode zolang er een FOUT staat, zodat een publicatie
niet doorgaat met een gebroken pagina. WAARSCHUWING is een advies, geen stop.

FOUT:    geen bedragen op de site; geen verboden woorden en namen; precies één h1;
         canonical klopt; pagina staat in de sitemap; elke afbeelding heeft alt;
         geen "je/jij/jouw" in de lopende tekst (formele u-vorm); titel niet
         langer dan 70 tekens; beschrijving niet langer dan 200 tekens.
Uit zoektermen.json per pagina: zoekterm in titel, h1 en eerste 140 woorden,
         minimum aantal woorden, vragen, interne links en externe bronlinks.
WAARSCHUWING: titel langer dan 60 of beschrijving buiten 110-160 tekens;
         minder dan 3 contextuele links in de hoofdtekst; h1 zonder onderwerp.
"""
import re, sys, glob, os
from html.parser import HTMLParser

HIER = os.path.dirname(os.path.abspath(__file__))
OVERSLAAN = ("google", "meta-app", "404")
JURIDISCH = ("privacy.html", "voorwaarden.html", "gegevens-verwijderen.html")  # vestigingsadres is hier wettelijk

# Wat Glenn heeft verboden (zie Klantcontact — Toon, Grenzen en complete-ai.md).
VERBODEN = [
    (r"€|\b\d[\d.,]*\s*euro\b|\beuro\s*\d", "bedrag (geen prijzen op de site; 'tot op de euro' mag)"),
    (r"\bvanaf\s+\d", "vanaf-prijs"),
    (r"\b(doorgaans|meestal|vrijwel|zelden|regelmatig|veelal)\b|(?<!hoe )\bvaak\b", "slap woord in een belofte of claim ('hoe vaak' als vraagwoord mag)"),
    (r"in de meeste gevallen", "slappe formulering"),
    (r"Bergen op Zoom", "lokale positionering (uitdrukkelijk verwijderd op 29-8-2026)"),
    (r"\bnulmeting\b", "het heet intake"),
]

# Namen die nooit publiek mogen staan (oude bedrijfsnaam, klanten die niet genoemd
# mogen worden) staan NIET in dit bestand: de site-repo is openbaar. Ze staan in
# ~/.config/complete-ai/verboden-namen.txt, één patroon per regel.
PRIVE_LIJST = os.path.expanduser("~/.config/complete-ai/verboden-namen.txt")


def prive_patronen():
    if not os.path.exists(PRIVE_LIJST):
        return None
    uit = []
    for regel in open(PRIVE_LIJST, encoding="utf-8"):
        regel = regel.strip()
        if regel and not regel.startswith("#"):
            uit.append((regel, "naam die niet publiek mag staan"))
    return uit
JE_VORM = r"\b(je|jij|jouw|jou)\b"


PRIVE = prive_patronen()
try:
    import json
    ZOEK = json.load(open(os.path.join(HIER, "zoektermen.json"), encoding="utf-8"))
except Exception:
    ZOEK = {}


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.skip = 0; s.text = []; s.h1 = []; s.cur = None
        s.title = ""; s.intitle = False; s.meta = {}; s.canon = None
        s.imgs = 0; s.noalt = 0; s.links_main = 0; s.inmain = 0; s.excl = 0
        s.extern = 0; s.vragen = 0
    def handle_starttag(s, t, a):
        a = dict(a)
        if t in ("script", "style", "noscript", "svg"): s.skip += 1
        if t == "title": s.intitle = True
        if t == "h1": s.cur = "h1"; s.h1.append("")
        if t == "main": s.inmain += 1
        if t in ("header", "footer", "nav"): s.excl += 1
        if t == "meta":
            n = (a.get("name") or a.get("property") or "").lower()
            if n: s.meta[n] = a.get("content", "")
        if t == "link" and a.get("rel") == "canonical": s.canon = a.get("href")
        if t == "img":
            s.imgs += 1
            if "alt" not in a: s.noalt += 1
        if t == "summary" and s.inmain: s.vragen += 1
        if t == "a" and s.inmain and not s.excl and a.get("href", "").startswith("http"):
            s.extern += 1
        if t == "a" and s.inmain and not s.excl:
            h = a.get("href", "")
            if h.endswith(".html") or "#" in h: s.links_main += 1
    def handle_endtag(s, t):
        if t in ("script", "style", "noscript", "svg"): s.skip = max(0, s.skip - 1)
        if t == "title": s.intitle = False
        if t == "h1": s.cur = None
        if t == "main": s.inmain = max(0, s.inmain - 1)
        if t in ("header", "footer", "nav"): s.excl = max(0, s.excl - 1)
    def handle_data(s, d):
        if s.intitle: s.title += d
        if s.skip: return
        if s.cur == "h1": s.h1[-1] += d
        if s.inmain and not s.excl: s.text.append(d)


def controleer(pad, in_sitemap):
    naam = os.path.basename(pad)
    h = open(pad, encoding="utf-8").read()
    p = P(); p.feed(h)
    fouten, waarsch = [], []
    tekst = " ".join(p.text)
    if PRIVE is None:
        waarsch.append("privélijst met verboden namen niet gevonden, die controle is overgeslagen")
    # verboden woorden en bedragen in de zichtbare tekst en in title/description
    zichtbaar = tekst + " " + p.title + " " + p.meta.get("description", "")
    for rx, wat in VERBODEN + (PRIVE or []):
        if rx == r"Bergen op Zoom" and naam in JURIDISCH: continue
        for m in re.finditer(rx, zichtbaar, re.I):
            i = max(0, m.start() - 40)
            fouten.append(f"verboden: {wat}: …{zichtbaar[i:m.end()+30].strip()}…")
            break
    if naam not in JURIDISCH:
        m = re.search(JE_VORM, tekst, re.I)
        if m:
            i = max(0, m.start() - 40)
            fouten.append(f"je-vorm in de tekst (het is u): …{tekst[i:m.end()+30].strip()}…")
    tl = len(p.title.strip()); dl = len(p.meta.get("description", ""))
    if tl > 70: fouten.append(f"titel {tl} tekens (max 70)")
    elif tl > 60: waarsch.append(f"titel {tl} tekens, Google knipt af rond 60")
    if dl > 200: fouten.append(f"beschrijving {dl} tekens (max 200)")
    elif dl > 160 or dl < 110: waarsch.append(f"beschrijving {dl} tekens (richtlijn 110-160)")
    if len(p.h1) != 1: fouten.append(f"{len(p.h1)} h1-koppen, moet er precies één zijn")
    verwacht = "https://complete-ai.nl/" if naam == "index.html" else f"https://complete-ai.nl/{naam}"
    if p.canon != verwacht: fouten.append(f"canonical {p.canon} ≠ {verwacht}")
    if naam not in in_sitemap: fouten.append("staat niet in sitemap.xml")
    eis = ZOEK.get(naam)
    if eis:
        woorden = len(re.findall(r"\w+", tekst))
        varianten = [v.lower() for v in eis["varianten"]]
        titel_l = p.title.lower().replace("—", " ").replace("-", " ")
        varianten_n = [v.replace("-", " ") for v in varianten]
        if not any(v in titel_l for v in varianten_n):
            fouten.append(f"zoekterm '{eis['zoekterm']}' (of variant) staat niet in de titel")
        eerste = " ".join(re.findall(r"\w[\w'-]*", tekst.lower())[:140]).replace("-", " ")
        if not any(v in eerste for v in varianten_n):
            fouten.append(f"zoekterm '{eis['zoekterm']}' (of variant) staat niet in de eerste 140 woorden")
        h1_l = (p.h1[0] if p.h1 else "").lower().replace("-", " ")
        if naam != "index.html" and not any(v in h1_l for v in varianten_n):
            fouten.append(f"zoekterm '{eis['zoekterm']}' (of variant) staat niet in de h1")
        if woorden < eis["min_woorden"]: fouten.append(f"{woorden} woorden, minimaal {eis['min_woorden']}")
        if p.vragen < eis["min_vragen"]: fouten.append(f"{p.vragen} vragen in de vragenlijst, minimaal {eis['min_vragen']}")
        if p.links_main < eis["min_intern"]: fouten.append(f"{p.links_main} interne links in de hoofdtekst, minimaal {eis['min_intern']}")
        if p.extern < eis["min_extern"]: fouten.append(f"{p.extern} externe bronlinks, minimaal {eis['min_extern']}")
    if p.noalt: fouten.append(f"{p.noalt} afbeelding(en) zonder alt")
    if p.links_main < 3 and naam not in JURIDISCH:
        waarsch.append(f"{p.links_main} contextuele links in de hoofdtekst (richtlijn: minstens 3)")
    return naam, fouten, waarsch, len(re.findall(r"\w+", tekst))


def main():
    sm = open(os.path.join(HIER, "sitemap.xml"), encoding="utf-8").read()
    in_sitemap = {"index.html" if u.rstrip("/").endswith("complete-ai.nl") else u.split("/")[-1]
                  for u in re.findall(r"<loc>([^<]+)</loc>", sm)}
    paginas = sorted(f for f in glob.glob(os.path.join(HIER, "*.html"))
                     if not os.path.basename(f).startswith(OVERSLAAN))
    fout_totaal = 0
    for pad in paginas:
        naam, fouten, waarsch, woorden = controleer(pad, in_sitemap)
        status = "FOUT" if fouten else ("let op" if waarsch else "ok")
        print(f"{status:6} {naam:52} {woorden:5d} woorden")
        for f in fouten: print(f"         FOUT: {f}")
        for w in waarsch: print(f"         let op: {w}")
        fout_totaal += len(fouten)
    print(f"\n{len(paginas)} pagina's gecontroleerd, {fout_totaal} fout(en).")
    sys.exit(1 if fout_totaal else 0)


if __name__ == "__main__":
    main()
