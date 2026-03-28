#!/usr/bin/env python3
"""Generate round 2 audition samples — younger Jake voices + more alien-sounding aliens."""

import os, json, time
import urllib.request, urllib.error

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
MODEL   = "eleven_turbo_v2_5"
OUT_DIR = os.path.join(os.path.dirname(__file__), "sounds", "audition")
os.makedirs(OUT_DIR, exist_ok=True)

JAKE_LINE  = "Let me calculate this carefully... if each row has 6 crystals, and I need 24 total, then I need 4 rows! Pre-launch check: passed!"
ALIEN_LINE = "Greetings, Space Human! I am Bloop. These are Zibble and Mork. We must share food before you leave. It is the Zog Law!"

SEGMENTS = [
    # Younger Jake candidates
    ("jake-alex.mp3",    "qHjcDL87pelA6RkUz0Ij", JAKE_LINE,
     {"stability": 0.45, "similarity_boost": 0.80, "style": 0.3},
     "Alex — Energetic Kid"),

    ("jake-johnny.mp3",  "8JVbfL6oEdmuxKn5DK2C", JAKE_LINE,
     {"stability": 0.5, "similarity_boost": 0.75},
     "Johnny Kid — Young British"),

    ("jake-elio.mp3",    "QZRlT5NqTgs34Uz6r1me", JAKE_LINE,
     {"stability": 0.5, "similarity_boost": 0.75},
     "Elio — Youthful & Warm"),

    # Alien variants — same voice (Callum) but with weirder settings
    ("alien-callum-weird.mp3", "N2lVS1w4EtoT3dr4eOWO", ALIEN_LINE,
     {"stability": 0.15, "similarity_boost": 0.30, "style": 0.8},
     "Callum — Very Alien (unstable/weird settings)"),

    # Different alien voice — Harry with weird settings
    ("alien-harry-weird.mp3",  "SOYHLrjzK2X1ezoPC6cr", ALIEN_LINE,
     {"stability": 0.2, "similarity_boost": 0.4, "style": 0.7},
     "Harry — Fierce Alien (pushed settings)"),

    # Kermy — frog/creature voice, could work for aliens
    ("alien-kermy.mp3",  "fO96OTVqTn6bBvyybd7U", ALIEN_LINE,
     {"stability": 0.4, "similarity_boost": 0.7},
     "Kermy — Creature/Froggy"),

    # River (neutral gender) with alien settings
    ("alien-river.mp3",  "SAz9YHcvj6GT2YYXdXww", ALIEN_LINE,
     {"stability": 0.2, "similarity_boost": 0.35, "style": 0.9},
     "River — Neutral/Robotic Alien"),
]

def generate(filename, voice_id, text, settings, label):
    out_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(out_path):
        print(f"  ✓ {filename} (cached)")
        return True
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": settings
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
        with open(out_path, 'wb') as f:
            f.write(data)
        print(f"  ✅ {filename} ({len(data)//1024}kb) — {label}")
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ❌ {filename}: {e.code} — {body[:120]}")
        return False

print(f"Generating {len(SEGMENTS)} samples...\n")
ok = 0
for fname, vid, text, settings, label in SEGMENTS:
    if generate(fname, vid, text, settings, label): ok += 1
    time.sleep(0.4)

print(f"\nDone: {ok}/{len(SEGMENTS)}")
