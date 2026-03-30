#!/usr/bin/env python3
"""Fix ch5-blaze.mp3 — trailing cliffhanger bleed."""
import requests, os, time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue005")
VOICE = ("cjVigY5qzO86Huf0OWal", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20})

# Slightly reworded ending + trailing comma to close cleanly before TTS can bleed
TEXT = (
    "It was giving them back. "
    "Blaze looked at the rows of vine bundles stretched along the clifftop, "
    "then back at Tangle. "
    "All this time, it hadn't meant any harm. "
    "It had taken the vines because they were beautiful, "
    "and because it had never known there was anyone else to share them with,"
)

path = os.path.join(OUT_DIR, "ch5-blaze.mp3")
if os.path.exists(path):
    os.remove(path)
    print("  🗑  Deleted ch5-blaze.mp3")

voice_id, settings = VOICE
r = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
    headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
    json={"text": TEXT, "model_id": "eleven_turbo_v2_5", "voice_settings": settings}
)
if r.status_code == 200:
    with open(path, "wb") as f: f.write(r.content)
    print(f"  ✅ ch5-blaze.mp3 ({len(r.content):,}b)")
else:
    print(f"  ❌ {r.status_code} {r.text[:100]}")
