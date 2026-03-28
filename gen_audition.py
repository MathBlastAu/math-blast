#!/usr/bin/env python3
"""Generate voice audition samples for Math Blast."""

import os, json, time
import urllib.request, urllib.error

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
MODEL   = "eleven_turbo_v2_5"
OUT_DIR = os.path.join(os.path.dirname(__file__), "sounds", "audition")
os.makedirs(OUT_DIR, exist_ok=True)

NARRATOR_LINE = "Jake the astronaut cadet was hurtling through the Zorblax Nebula — munching a space sandwich and humming to himself — when BANG! CRASH! CLONK! His rocket had smashed straight into Planet Zog! Through the smoke and sparks, Jake stumbled out and inspected the damage."

JAKE_LINE = "Let me calculate this carefully... if each row has 6 crystals, and I need 24 total, then I need 4 rows! Pre-launch check: passed!"

ALIEN_LINE = "Greetings, Space Human! I am Bloop. These are Zibble and Mork. We must share food before you leave. It is the Zog Law!"

VOICES = {
    "narrator": [
        ("george",  "JBFqnCBsd6RMkjVDRZzb", "George — Warm Storyteller"),
        ("brian",   "nPczCjzI2devNBz1zQrb", "Brian — Deep & Comforting"),
        ("daniel",  "onwK4e9ZLuTAKqWW03F9", "Daniel — Steady Broadcaster"),
        ("matilda", "XrExE9yKIg1WjnnlVkGX", "Matilda — Professional"),
        ("jessica", "cgSgspJ2msm6clMCkdW9", "Jessica — Playful & Warm"),
    ],
    "jake": [
        ("charlie", "IKne3meq5aSn9XLyUdCD", "Charlie — Energetic"),
        ("liam",    "TX3LPaxmHKxFdv7VOQHJ", "Liam — Social & Fun"),
        ("will",    "bIHbv24MWmeRgasZH58o", "Will — Relaxed Optimist"),
    ],
    "alien": [
        ("callum",  "N2lVS1w4EtoT3dr4eOWO", "Callum — Husky Trickster"),
        ("harry",   "SOYHLrjzK2X1ezoPC6cr", "Harry — Fierce & Bold"),
        ("eric",    "cjVigY5qzO86Huf0OWal", "Eric — Smooth & Sly"),
    ],
}

LINES = {
    "narrator": NARRATOR_LINE,
    "jake":     JAKE_LINE,
    "alien":    ALIEN_LINE,
}

def generate(filename, voice_id, text):
    out_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(out_path):
        print(f"  ✓ {filename} (cached)")
        return True
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
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
        print(f"  ✅ {filename} ({len(data)//1024}kb)")
        return True
    except urllib.error.HTTPError as e:
        print(f"  ❌ {filename}: {e.code} — {e.read().decode()[:100]}")
        return False

total = ok = 0
for role, voice_list in VOICES.items():
    print(f"\n── {role.upper()} ──")
    for key, vid, label in voice_list:
        fname = f"{role}-{key}.mp3"
        success = generate(fname, vid, LINES[role])
        if success: ok += 1
        total += 1
        time.sleep(0.3)

print(f"\nDone: {ok}/{total} → {OUT_DIR}")
