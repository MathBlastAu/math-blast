#!/usr/bin/env python3
"""
Full cast auditions — wider accent variety for Narrator, Chief Pip, and Doz
"""
import requests, os, time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.dirname(__file__)

NARRATOR_LINE = "Deep in the Verdant Canopy, where ancient trees grew so tall their tops scraped the clouds, there lived a tribe of small, clever creatures called the Sprockets. And on one perfectly ordinary morning — a girl named Blaze came crashing through the canopy."

PIP_LINE = "Welcome, explorer! I am Chief Pip of Branchwick. Tonight we share the harvest — as we have for ten thousand years. But first... we must divide it correctly."

DOZ_LINE = "Oh! Oh oh oh — the vines! Did you see the vines?! They're all tangled up and I couldn't count the berries because I kept losing my place and — wait, how many did you say there were?"

AUDITIONS = [
    # ── NARRATOR (warm, engaging, sets the scene — NOT Blaze) ─────────
    # George: warm British storyteller (already used in Space arc — try for jungle too?)
    ("narrator-george",  "JBFqnCBsd6RMkjVDRZzb", NARRATOR_LINE, {"stability": 0.6, "similarity_boost": 0.75, "style": 0.2}),
    # Daniel: steady British broadcaster — authoritative, clear
    ("narrator-daniel",  "onwK4e9ZLuTAKqWW03F9", NARRATOR_LINE, {"stability": 0.6, "similarity_boost": 0.75, "style": 0.2}),
    # Brian: deep, resonant, comforting American
    ("narrator-brian",   "nPczCjzI2devNBz1zQrb", NARRATOR_LINE, {"stability": 0.6, "similarity_boost": 0.75, "style": 0.2}),
    # Eric: smooth, trustworthy American
    ("narrator-eric",    "cjVigY5qzO86Huf0OWal", NARRATOR_LINE, {"stability": 0.6, "similarity_boost": 0.75, "style": 0.2}),

    # ── CHIEF PIP (warm elder, ceremonial) ────────────────────────────
    # Already done: George, Bill, Brian
    # Adding accent variety:
    # Daniel: British broadcaster — more formal, regal
    ("pip-daniel",   "onwK4e9ZLuTAKqWW03F9", PIP_LINE, {"stability": 0.65, "similarity_boost": 0.7, "style": 0.2}),
    # Roger: laid-back, casual American — warmer, less formal
    ("pip-roger",    "CwhRBWXzGAHq8TQ4Fs17", PIP_LINE, {"stability": 0.65, "similarity_boost": 0.7, "style": 0.2}),
    # Chris: charming, down-to-earth American
    ("pip-chris",    "iP95p4xoKVk53GoZ742B", PIP_LINE, {"stability": 0.65, "similarity_boost": 0.7, "style": 0.2}),

    # ── DOZ (jittery, scatterbrained, young) ─────────────────────────
    # Already done: Liam, Will, Charlie
    # Adding accent variety:
    # Harry: fierce, energetic American young — more wild energy
    ("doz-harry",    "SOYHLrjzK2X1ezoPC6cr", DOZ_LINE, {"stability": 0.4, "similarity_boost": 0.7, "style": 0.55}),
    # Andrew: young, outgoing American
    ("doz-andrew",   "BTEPH6wbWkb66Dys0ry6", DOZ_LINE, {"stability": 0.4, "similarity_boost": 0.7, "style": 0.55}),
    # Johnny Kid: young British — different accent
    ("doz-johnny",   "8JVbfL6oEdmuxKn5DK2C", DOZ_LINE, {"stability": 0.4, "similarity_boost": 0.7, "style": 0.55}),
]

for filename, voice_id, text, settings in AUDITIONS:
    out_path = os.path.join(OUT_DIR, f"{filename}.mp3")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"  ⏭  {filename} already exists")
        continue
    print(f"  Generating {filename}...")
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={"text": text, "model_id": "eleven_turbo_v2_5", "voice_settings": settings}
    )
    if r.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(r.content)
        print(f"  ✅ {filename}.mp3 ({len(r.content):,} bytes)")
    elif r.status_code == 429:
        print(f"  ⏳ Rate limited, waiting 10s...")
        time.sleep(10)
    else:
        print(f"  ❌ {filename}: {r.status_code} {r.text[:120]}")

print("\nAll done.")
