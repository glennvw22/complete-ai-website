---
name: video-analyseren
description: Analyseer een video van Instagram, TikTok, YouTube, Facebook of X vanaf alleen een link. Gebruik dit zodra Glenn een videolink stuurt en wil weten wat erin gezegd of getoond wordt — bijvoorbeeld bij waarschuwingen over malware, nieuws, of iets dat hij gezien heeft. Werkt ook als de link niet direct bereikbaar is vanuit de sessie.
---

# Video's analyseren vanaf een link

Glenn stuurt een link naar een reel of video en wil weten wat erin staat.
Doe dit zelf, meteen, zonder er iets voor terug te vragen.

## Waarom dit nodig is

Twee dingen werken niet:

1. Claude kan geen video verwerken — alleen tekst en afbeeldingen.
2. De cloud-omgeving van Claude Code blokkeert `instagram.com`
   (en alle spiegelsites) op proxy-niveau met een 403.

**De oplossing:** de Higgsfield-sandbox. Dat is een Linux-machine met
internettoegang, ffmpeg, python3 en faster-whisper voorgeïnstalleerd.
Die kán Instagram bereiken. Getest en werkend op 3 september 2026 —
zonder inloggegevens of cookies.

## De werkwijze

Gebruik `mcp__Higgsfield__sandbox_exec`. Belangrijk: de sandbox wordt
ongeveer 10 seconden na een aanroep gewist, dus keten alles aan elkaar
in één opdracht met `&&`.

### Stap 1 — Video ophalen en audio uitschrijven

```bash
cd /home/user && pip install -q yt-dlp && \
yt-dlp -f "best[ext=mp4]/best" -o "video.%(ext)s" "<DE LINK>" 2>&1 | tail -3 && \
ffmpeg -y -i video.mp4 -vn -ac 1 -ar 16000 audio.wav 2>/dev/null && \
cat > tr.py <<'PY'
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, info = m.transcribe("audio.wav", beam_size=5)
with open("transcript.txt","w") as f:
    f.write("TAAL: %s (zekerheid %.2f)\n\n" % (info.language, info.language_probability))
    for s in segs:
        f.write("[%6.1fs] %s\n" % (s.start, s.text.strip()))
print("KLAAR")
PY
python3 tr.py && cat transcript.txt
```

Draai dit met `background: true` — het duurt 2 tot 5 minuten, vooral
door het downloaden van het Whisper-model. Pollen daarna met een korte
wachtlus op het `.exit`-bestand.

Het model `small` is genoeg voor Nederlands. Bij veel vaktermen of
slecht geluid: `medium`.

### Stap 2 — Beeld erbij, alleen als het nodig is

Staat de informatie in beeld en niet in de audio (bestandsnamen,
schermafbeeldingen, code), pak dan losse frames:

```bash
ffmpeg -y -i video.mp4 -vf fps=1/2 frame_%03d.png
```

Er zit **geen tesseract** in de sandbox. Om beeld te laten lezen:
upload de video met `media_upload` + `curl PUT` en draai daarna
`video_analysis_create` met het `video_input_id`. Dat geeft een
scène-voor-scène-analyse. Duurt 3 tot 5 minuten, pollen met
`video_analysis_status`.

Let op: `media_import_url` werkt **niet** met een Instagram-paginalink.
Die geeft HTML terug, geen video. Alleen een directe bestandslink werkt.

## Wat je daarna doet — dit is het echte werk

Een transcript is geen antwoord. Lever altijd deze drie dingen:

1. **Wat er gezegd wordt**, kort samengevat in gewone taal.
2. **Klopt het?** Controleer elke feitelijke bewering met `WebSearch`
   tegen echte bronnen. Een reel is geen bron. Noem versienummers,
   pakketnamen en datums die je hebt geverifieerd, en zeg het eerlijk
   als iets niet klopt of ouder nieuws is dan het lijkt.
3. **Raakt het Glenn?** Kijk zelf in zijn spullen: de website-repo,
   zijn Lovable-projecten (`mcp__Lovable__read_file` op `package.json`),
   en waar het verder van toepassing is. Geef een concreet oordeel:
   wel of niet geraakt, en wat hij moet doen.

Zonder stap 2 en 3 heb je alleen ondertiteling geleverd, geen antwoord.

## Waar je op moet letten

- Reels presenteren oud nieuws vaak als "vandaag". Zoek altijd de
  echte datum op.
- Veel reels zijn reclame vermomd als waarschuwing. Zeg het als dat zo is.
- Doe dit voor incidentele video's, niet massaal. Instagram staat
  geautomatiseerd downloaden niet toe in hun voorwaarden.
