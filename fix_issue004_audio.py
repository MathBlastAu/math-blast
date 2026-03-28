#!/usr/bin/env python3
"""Regenerate specific audio files for Issue 4 that have wrong voices or content."""

import os, time, urllib.request, urllib.error, json

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
MODEL   = "eleven_turbo_v2_5"
BASE    = "/Users/leohiem/.openclaw/workspace/projects/math-blast/sounds/issue004"

RIVER  = "SAz9YHcvj6GT2YYXdXww"   # Phantom voice
ANDREW = "BTEPH6wbWkb66Dys0ry6"   # Jake voice
GEORGE = "JBFqnCBsd6RMkjVDRZzb"   # Narrator voice

# ALIEN settings = River with the spooky Phantom effect
ALIEN = {"stability": 0.18, "similarity_boost": 0.32, "style": 0.85}
JAKE  = {"stability": 0.50, "similarity_boost": 0.78}
NAR   = {"stability": 0.55, "similarity_boost": 0.75}

files_to_gen = [
    # (filename, voice_id, voice_settings, text)

    # Issue #3: ch3-phantom — Phantom speaking through intercom (wrong voice currently)
    ("ch3-phantom.mp3", RIVER, ALIEN,
     "You fix my corrections. But you have not considered: what lies beyond 1? "
     "I have added my own markers there. Markers for fractions that are MORE than one whole."),

    # Issue #11: ch5-phantom — Phantom's missing marker speech (wrong voice)
    ("ch5-phantom.mp3", RIVER, ALIEN,
     "I removed the marker between 3 quarters and 5 quarters because it is NOT a fraction. "
     "It is a whole number. Tell me: what marker did I remove — and am I correct?"),

    # Issue #12: ch5-phantom-end — Phantom's closing line (not playing)
    ("ch5-phantom-end.mp3", RIVER, ALIEN,
     "You understand the number line. Then come find me at the Fraction Fair. If you reach me, I will listen."),

    # Issue #2: feedback-correct-1 — fix "pre-launch check passed" artifact
    ("feedback-correct-1.mp3", GEORGE, NAR,
     "Correct! Nice work, space cadet. The first marker is back in place!"),

    # Issue #7: ch3-jake — Jake's realisation about 5/4 (not playing currently)
    ("ch3-jake.mp3", ANDREW, JAKE,
     "5 quarters equals 1 and 1 quarter. So it sits just past the 1 mark. That actually makes sense..."),
]

def gen(filename, voice_id, voice_settings, text):
    out_path = os.path.join(BASE, filename)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": voice_settings
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            audio = resp.read()
        with open(out_path, "wb") as f:
            f.write(audio)
        print(f"✅ {filename} ({len(audio):,} bytes)")
        return True
    except urllib.error.HTTPError as e:
        body = e.read()
        print(f"❌ {filename} — HTTP {e.code}: {body[:200]}")
        return False
    except Exception as e:
        print(f"❌ {filename} — {e}")
        return False

if __name__ == "__main__":
    for fname, vid, vsettings, text in files_to_gen:
        ok = gen(fname, vid, vsettings, text)
        if ok:
            time.sleep(1.5)  # rate limit buffer
    print("\nDone!")
