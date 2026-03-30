#!/usr/bin/env python3
"""Fix Jungle Issue 4 — regen garbled audio clips."""
import requests, os, time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue004")

VOICES = {
    "narrator": ("cjVigY5qzO86Huf0OWal", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),
    "blaze":    ("cgSgspJ2msm6clMCkdW9", {"stability": 0.55, "similarity_boost": 0.75, "style": 0.30}),
}

# The two garbled clips — trailing comma adds a natural pause before clip ends
FIXES = [
    # Item 1: ch2-arrays ends with garble — "Always in groups of twelve."
    ("ch2-arrays", "narrator",
     "The second array: thirty-five trees in five equal rows. "
     "The third: forty-eight trees in six equal rows. "
     "As she worked, Blaze kept noticing something. Vine bundles, left behind. Always in groups of twelve,"),

    # Item 2: ch3-blaze ends with garble — "That cannot be a coincidence."
    ("ch3-blaze", "blaze",
     "Both come out the same. Twelve per row each time. That cannot be a coincidence,"),
]

def generate(filename, character, text):
    out_path = os.path.join(OUT_DIR, f"{filename}.mp3")
    # Force regen — delete existing
    if os.path.exists(out_path):
        os.remove(out_path)
        print(f"  🗑  Deleted old {filename}.mp3")
    voice_id, settings = VOICES[character]
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={"text": text, "model_id": "eleven_turbo_v2_5", "voice_settings": settings}
    )
    if r.status_code == 200:
        with open(out_path, "wb") as f: f.write(r.content)
        print(f"  ✅ {filename}.mp3 ({len(r.content):,}b)")
        return True
    elif r.status_code == 429:
        print(f"  ⏳ Rate limited, waiting 15s...")
        time.sleep(15)
        return generate(filename, character, text)
    else:
        print(f"  ❌ {filename}: {r.status_code} {r.text[:120]}")
        return False

print(f"Regenerating {len(FIXES)} garbled clips\n")
for filename, character, text in FIXES:
    print(f"  {character}: {filename}")
    generate(filename, character, text)
    time.sleep(1)
print("\n✅ Done.")
