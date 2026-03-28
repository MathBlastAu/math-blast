#!/usr/bin/env python3
"""Generate ElevenLabs narration audio for Math Blast narrated prototype."""

import os, json, time
import urllib.request, urllib.error

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"

# Voice IDs
GEORGE  = "JBFqnCBsd6RMkjVDRZzb"  # Narrator
CHARLIE = "IKne3meq5aSn9XLyUdCD"  # Jake
CALLUM  = "N2lVS1w4EtoT3dr4eOWO"  # Aliens (Bloop/Mork)

OUT_DIR = os.path.join(os.path.dirname(__file__), "sounds", "narration")
os.makedirs(OUT_DIR, exist_ok=True)

# Each segment: (filename, voice_id, text)
SEGMENTS = [
    ("ch1-intro.mp3", GEORGE,
     "Jake the astronaut cadet was hurtling through the Zorblax Nebula — "
     "munching a space sandwich and humming to himself — when... BANG! CRASH! CLONK! "
     "His rocket had smashed straight into Planet Zog! "
     "Through the smoke and sparks, Jake stumbled out and inspected the damage. "
     "But first — his training kicked in. Before any mission, his computer always ran a Pre-Launch Check. "
     "Even crashed on an alien planet, the rules were the rules."),

    ("ch1-crystals.mp3", GEORGE,
     "With the computer check complete, Jake turned to the real problem. "
     "The engine room was a mess — fuel crystals scattered everywhere! "
     "He needed exactly 24 crystals to launch, arranged in rows of 6. "
     "Jake grabbed his maths notebook..."),

    ("ch2-intro-narration.mp3", GEORGE,
     "Before Jake could fire up the engines, three small green aliens waddled over. "
     "The tallest one — wearing a tiny purple crown — bowed deeply."),

    ("ch2-bloop-speech.mp3", CALLUM,
     "Greetings, Space Human! I am Bloop. These are Zibble and Mork. "
     "We must share food before you leave. It is the Zog Law."),

    ("ch2-intro-end.mp3", GEORGE,
     "A giant glowing pizza appeared from nowhere. "
     "There were 4 of them altogether, and Bloop insisted everyone got an equal share."),

    ("ch2-mork-narration.mp3", GEORGE,
     "Mork looked at his slice thoughtfully and pushed most of it toward Jake."),

    ("ch2-mork-speech.mp3", CALLUM,
     "Mork not hungry. Mork eat only half of Mork's slice."),

    ("ch2-mork-end.mp3", GEORGE,
     "Jake wondered: if Mork's slice was one quarter of the whole pizza, "
     "and Mork only ate half of that — what fraction of the whole pizza did Mork eat?"),

    ("ch3-narration.mp3", GEORGE,
     "Jake was climbing back to his rocket when Mork suddenly grabbed his arm."),

    ("ch3-mork-speech.mp3", CALLUM,
     "Wait! The Launch Window is critical! "
     "Leave too early or too late and you will be TRAPPED in the Zog Gravitational Loop for 47 years!"),

    ("ch3-end.mp3", GEORGE,
     "Jake peered at the cockpit clock. "
     "The Launch Window closes in exactly 30 minutes. It was 3:15 now. "
     "He had to work it out — fast."),

    # Question narrations
    ("q1-question.mp3", GEORGE,
     "The mission computer is counting down fuel reserves: "
     "5, 10, 15... blank... 25... blank. What are the two missing numbers?"),

    ("q2-question.mp3", GEORGE,
     "Jake needs 24 fuel crystals. They come in rows of 6. How many rows does he need?"),

    ("q3-question.mp3", GEORGE,
     "4 friends share 1 pizza equally. What fraction does each person get?"),

    ("q4-question.mp3", GEORGE,
     "Mork's slice is one quarter of the pizza. Mork eats half of his slice. "
     "What fraction of the whole pizza did Mork eat?"),

    ("q5-question.mp3", GEORGE,
     "It is 3:15 now. The Launch Window closes in 30 minutes. "
     "What time must Jake launch by?"),

    # Feedback
    ("correct.mp3", CHARLIE, "Correct! Nice work, space cadet!"),
    ("wrong.mp3",   CHARLIE, "Not quite — give it another go!"),
    ("win.mp3",     GEORGE,
     "Mission complete! Jake's rocket blasted off just in time — "
     "and it was all thanks to YOU! Amazing work, space cadet!"),
]

def generate(filename, voice_id, text):
    out_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(out_path):
        print(f"  ✓ {filename} (cached)")
        return True

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": text,
        "model_id": "eleven_turbo_v2_5",
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
        body = e.read().decode()
        print(f"  ❌ {filename}: HTTP {e.code} — {body[:200]}")
        return False

print(f"Generating {len(SEGMENTS)} audio segments...\n")
ok = 0
for fname, voice, text in SEGMENTS:
    success = generate(fname, voice, text)
    if success: ok += 1
    time.sleep(0.3)  # be kind to the API

print(f"\nDone: {ok}/{len(SEGMENTS)} generated → {OUT_DIR}")
