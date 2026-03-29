#!/usr/bin/env python3
"""Generate missing ch2-pip-harvest.mp3 for Jungle Issue 1"""
import requests, os

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue001")

# Chief Pip — Bill voice
VOICE_ID = "pqHfZKP75CvOlQylNhV4"
SETTINGS = {"stability": 0.65, "similarity_boost": 0.70, "style": 0.25}

TEXT = (
    "Four Sprocket families. "
    "Each must receive exactly the same amount — not one berry more, not one less. "
    "It is the Sprocket way. "
    "We have divided the harvest equally for ten thousand years. "
    "It is how we survive. It is how we thrive."
)

out_path = os.path.join(OUT_DIR, "ch2-pip-harvest.mp3")
r = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
    headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
    json={"text": TEXT, "model_id": "eleven_turbo_v2_5", "voice_settings": SETTINGS}
)
if r.status_code == 200:
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"✅ ch2-pip-harvest.mp3 ({len(r.content):,}b)")
else:
    print(f"❌ {r.status_code}: {r.text[:200]}")
