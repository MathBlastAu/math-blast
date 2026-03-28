#!/usr/bin/env python3
"""Fix Issue 4 audio — correct Phantom voice (River, calm/precise, not ALIEN)."""

import os, time, json, urllib.request, urllib.error

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
MODEL   = "eleven_turbo_v2_5"
BASE    = "/Users/leohiem/.openclaw/workspace/projects/math-blast/sounds/issue004"

RIVER  = "SAz9YHcvj6GT2YYXdXww"
GEORGE = "JBFqnCBsd6RMkjVDRZzb"
ANDREW = "BTEPH6wbWkb66Dys0ry6"

# CORRECT Phantom voice — calm, precise AI (from gen_space001_audio.py)
PHANTOM = {"stability": 0.80, "similarity_boost": 0.60, "style": 0.10}
NAR     = {"stability": 0.55, "similarity_boost": 0.75}
JAKE    = {"stability": 0.50, "similarity_boost": 0.78}

files_to_fix = [
    # Item 5 & 6: ch3-phantom — Phantom through intercom (wrong voice previously)
    ("ch3-phantom.mp3", RIVER, PHANTOM,
     "You fix my corrections. But you have not considered: what lies beyond 1? "
     "I have added my own markers there. Markers for fractions that are MORE than one whole."),

    # Item 7: ch3-jake — Jake's realisation (was not playing)
    ("ch3-jake.mp3", ANDREW, JAKE,
     "5 quarters equals 1 and 1 quarter. So it sits just past the 1 mark. That actually makes sense..."),

    # Item 9 & 11: ch5-phantom — Phantom's missing marker speech (wrong voice)
    ("ch5-phantom.mp3", RIVER, PHANTOM,
     "I removed the marker between 3 quarters and 5 quarters because it is NOT a fraction. "
     "It is a whole number. Tell me: what marker did I remove — and am I correct?"),

    # Item 12: ch5-phantom-end — Phantom's closing line (not playing + wrong voice)
    ("ch5-phantom-end.mp3", RIVER, PHANTOM,
     "You understand the number line. Then come find me at the Fraction Fair. If you reach me, I will listen."),

    # Item 2: feedback-correct-1 — fix "pre-launch" artefact
    ("feedback-correct-1.mp3", GEORGE, NAR,
     "Correct! The first marker is back in place. Well done, space cadet!"),
]

def gen(filename, voice_id, voice_settings, text):
    out_path = os.path.join(BASE, filename)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": voice_settings
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            audio = resp.read()
        with open(out_path, "wb") as f:
            f.write(audio)
        print(f"  ✅ {filename} ({len(audio):,} bytes)")
        return True
    except urllib.error.HTTPError as e:
        print(f"  ❌ {filename} — HTTP {e.code}: {e.read()[:200]}")
        return False
    except Exception as e:
        print(f"  ❌ {filename} — {e}")
        return False

if __name__ == "__main__":
    print("Fixing Issue 4 audio (correct Phantom voice)...")
    for fname, vid, vsettings, text in files_to_fix:
        gen(fname, vid, vsettings, text)
        time.sleep(1.5)
    print("\nDone!")
