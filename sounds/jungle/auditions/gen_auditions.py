#!/usr/bin/env python3
"""
Audition generator for Jungle Arc Issue 1 cast.
Characters: Blaze (narrator/hero), Chief Pip, Doz
"""
import requests, os

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.dirname(__file__)

# Each entry: (filename, voice_id, text, settings)
AUDITIONS = [

    # ── BLAZE (narrator/hero) ─────────────────────────────────────────
    # Sharp, precise, warm. Confident. Thinks fast. British or neutral accent.
    ("blaze-lily",    "pFZP5JQG7iQjIQuC4Bku",
     "I've already calculated that. The jungle has a pattern — everything here does. We just need to find it.",
     {"stability": 0.55, "similarity_boost": 0.75, "style": 0.3}),

    ("blaze-alice",   "Xb7hH8MSUJpSbSDYk0k2",
     "I've already calculated that. The jungle has a pattern — everything here does. We just need to find it.",
     {"stability": 0.55, "similarity_boost": 0.75, "style": 0.3}),

    ("blaze-matilda", "XrExE9yKIg1WjnnlVkGX",
     "I've already calculated that. The jungle has a pattern — everything here does. We just need to find it.",
     {"stability": 0.55, "similarity_boost": 0.75, "style": 0.3}),

    ("blaze-sarah",   "EXAVITQu4vr4xnSDxMaL",
     "I've already calculated that. The jungle has a pattern — everything here does. We just need to find it.",
     {"stability": 0.55, "similarity_boost": 0.75, "style": 0.3}),

    ("blaze-jessica", "cgSgspJ2msm6clMCkdW9",
     "I've already calculated that. The jungle has a pattern — everything here does. We just need to find it.",
     {"stability": 0.55, "similarity_boost": 0.75, "style": 0.3}),

    # ── CHIEF PIP ─────────────────────────────────────────────────────
    # Tiny, bright blue Sprocket. Warm, ceremonial, slightly formal. Older feel.
    # Trying: George (warm storyteller), Bill (wise, mature), Brian (comforting)
    ("pip-george", "JBFqnCBsd6RMkjVDRZzb",
     "Welcome, explorer! I am Chief Pip of Branchwick. Tonight we share the harvest — as we have for ten thousand years. But first... we must divide it correctly.",
     {"stability": 0.65, "similarity_boost": 0.7, "style": 0.25}),

    ("pip-bill",   "pqHfZKP75CvOlQylNhV4",
     "Welcome, explorer! I am Chief Pip of Branchwick. Tonight we share the harvest — as we have for ten thousand years. But first... we must divide it correctly.",
     {"stability": 0.65, "similarity_boost": 0.7, "style": 0.25}),

    ("pip-brian",  "nPczCjzI2devNBz1zQrb",
     "Welcome, explorer! I am Chief Pip of Branchwick. Tonight we share the harvest — as we have for ten thousand years. But first... we must divide it correctly.",
     {"stability": 0.65, "similarity_boost": 0.7, "style": 0.25}),

    # ── DOZ ───────────────────────────────────────────────────────────
    # The berry-counter. Jittery, excitable, slightly scatterbrained. Young.
    # Trying: Liam (energetic), Will (relaxed optimist), Charlie (Australian, energetic)
    ("doz-liam",    "TX3LPaxmHKxFdv7VOQHJ",
     "Oh! Oh oh oh — the vines! Did you see the vines?! They're all tangled up and I couldn't count the berries because I kept losing my place and — wait, how many did you say there were?",
     {"stability": 0.45, "similarity_boost": 0.7, "style": 0.5}),

    ("doz-will",    "bIHbv24MWmeRgasZH58o",
     "Oh! Oh oh oh — the vines! Did you see the vines?! They're all tangled up and I couldn't count the berries because I kept losing my place and — wait, how many did you say there were?",
     {"stability": 0.45, "similarity_boost": 0.7, "style": 0.5}),

    ("doz-charlie", "IKne3meq5aSn9XLyUdCD",
     "Oh! Oh oh oh — the vines! Did you see the vines?! They're all tangled up and I couldn't count the berries because I kept losing my place and — wait, how many did you say there were?",
     {"stability": 0.45, "similarity_boost": 0.7, "style": 0.5}),
]

for filename, voice_id, text, settings in AUDITIONS:
    out_path = os.path.join(OUT_DIR, f"{filename}.mp3")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"  ⏭  {filename} already exists, skipping")
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
    else:
        print(f"  ❌ {filename}: {r.status_code} {r.text[:100]}")

print("\nDone.")
