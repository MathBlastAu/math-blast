#!/usr/bin/env python3
import requests, os

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.dirname(__file__)

LINE = "I've already calculated that. The jungle has a pattern — everything here does. We just need to find it."

# Young female voices only
VOICES = {
    "sarah":   "EXAVITQu4vr4xnSDxMaL",   # Mature, Reassuring, Confident · young
    "jessica": "cgSgspJ2msm6clMCkdW9",   # Playful, Bright, Warm · young
    "laura":   "FGY2WhTYpPnrIDTdsKH5",   # Enthusiast, Quirky Attitude · young
}

SETTINGS = {"stability": 0.55, "similarity_boost": 0.75, "style": 0.3}

for name, vid in VOICES.items():
    out_path = os.path.join(OUT_DIR, f"blaze-{name}.mp3")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"  ⏭  blaze-{name} already exists, skipping")
        continue
    print(f"  Generating blaze-{name}...")
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={"text": LINE, "model_id": "eleven_turbo_v2_5", "voice_settings": SETTINGS}
    )
    if r.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(r.content)
        print(f"  ✅ blaze-{name}.mp3 ({len(r.content):,} bytes)")
    else:
        print(f"  ❌ {r.status_code}: {r.text[:120]}")

print("Done.")
