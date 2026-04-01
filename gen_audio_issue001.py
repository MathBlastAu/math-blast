#!/usr/bin/env python3
"""
Re-generate all Crystal Compass Issue 1 audio with new locked voice IDs.
"""
import os
import json
import time
import requests

API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
if not API_KEY:
    raise SystemExit("ELEVENLABS_API_KEY not set")

AUDIO_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/audio/crystal-compass/issue-001"
MODEL = "eleven_turbo_v2_5"

# Voice IDs
ALICE  = "Xb7hH8MSUJpSbSDYk0k2"   # Narrator
LAURA  = "FGY2WhTYpPnrIDTdsKH5"   # Miss Zara
ISLA   = "MUzMONRCyBSA0l61GzC2"   # CC-Isla
PRIYA  = "Qs8eI0FA8ZWoy7VJQK0C"   # CC-Priya
ZOE    = "x6KItt3dczXfR55FonpL"   # CC-Zoe
AMARA  = "uOwZUqvORJmMLzgFFB5A"   # CC-Amara

VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.3,
    "use_speaker_boost": True
}

# (filename, voice_id, text)
AUDIO_FILES = [
    # ── CHAPTER 1 ──────────────────────────────────────────────────────────
    ("ch1-intro.mp3", ALICE,
     "It was the last day of term at Methodist Ladies College. The four friends had one last job to do."),

    ("ch1-miss-zara.mp3", LAURA,
     "Girls, would you return these books to the old library? The one in the east wing."),

    ("ch1-library.mp3", ALICE,
     "The library was warm and quiet. Golden light filled the room. Nobody else was there."),

    ("ch1-priya-spots.mp3", PRIYA,
     "Wait, look at that. Something is glowing on that shelf."),

    ("ch1-isla-reaches.mp3", ISLA,
     "Let me see! I want to open it!"),

    ("ch1-zoe-wait.mp3", ZOE,
     "Wait. We should open it carefully."),

    ("ch1-compass-reveal.mp3", ALICE,
     "Inside the box was a beautiful compass. It glowed with soft cyan light. The needle spun and spun. It would not stop."),

    ("ch1-q1-question.mp3", ALICE,
     "The compass face shows a number. It has two tens and three ones. What number is that?"),

    # ── CHAPTER 2 ──────────────────────────────────────────────────────────
    ("ch2-intro.mp3", ALICE,
     "Amara picked up the compass. The glow flickered. Numbers appeared on the face, but they looked wrong."),

    ("ch2-amara.mp3", AMARA,
     "The numbers look all mixed up. Like they are in the wrong order."),

    ("ch2-zoe-studies.mp3", ZOE,
     "I think I understand. The numbers need to be in the right place."),

    ("ch2-zoe-explains.mp3", ZOE,
     "Tens go here. Ones go here. If the digits are in the wrong place, the whole number changes. Everything changes."),

    ("ch2-q2-question.mp3", ALICE,
     "The compass shows four tens and seven ones. What number is that?"),

    ("ch2-q3-intro.mp3", ALICE,
     "Now the compass changes. The digits swap around. Look carefully at the new number. Zoe says, the four and the seven have swapped places. But is the number bigger or smaller now?"),

    ("ch2-q3-question.mp3", ALICE,
     "The compass now shows seven tens and four ones. What number is that? Is it bigger or smaller than 47?"),

    # ── CHAPTER 3 ──────────────────────────────────────────────────────────
    ("ch3-intro.mp3", ALICE,
     "The girls sat at a big library table. Priya pulled out her notebook. She loved finding patterns."),

    ("ch3-priya-notebook.mp3", PRIYA,
     "Let us figure out the rules. We test the numbers one by one."),

    ("ch3-compass-responds.mp3", ALICE,
     "Every time the tens and ones were right, the compass glowed brighter. Every time they mixed them up, the light faded."),

    ("ch3-priya-language.mp3", PRIYA,
     "It is like a language. Numbers have an order. They have a place where they belong."),

    ("ch3-amara.mp3", AMARA,
     "Then we need to learn to speak it. Come on, let us keep going!"),

    ("ch3-q4-question.mp3", ALICE,
     "The compass shows five tens and zero ones. What number is that?"),

    ("ch3-q5-question.mp3", ALICE,
     "The compass changes again. Now there are no tens at all, just ones. The compass shows zero tens and eight ones. What number is that?"),

    ("ch3-q6-question.mp3", ALICE,
     "The compass spins and settles on a new number. It shows six tens and three ones. What number is that?"),

    ("ch3-q7-intro.mp3", ALICE,
     "The compass glows brighter. Two numbers flash side by side on its face."),

    ("ch3-q7-isla.mp3", ISLA,
     "Look at these. Same digits. But in different places!"),

    ("ch3-q7-question.mp3", ALICE,
     "The compass shows two numbers, 38 and 83. Which number is bigger?"),

    ("ch3-q8-intro.mp3", ALICE,
     "Now three numbers appear on the compass face at once. They need to be sorted."),

    ("ch3-q8-priya.mp3", PRIYA,
     "Smallest first, biggest last. Look at the tens first!"),

    ("ch3-q8-question.mp3", ALICE,
     "The compass shows three numbers, 52, 25, and 55. Put them in order from smallest to biggest."),

    # ── CHAPTER 4 ──────────────────────────────────────────────────────────
    ("ch4-intro.mp3", ALICE,
     "Suddenly the compass light began to fade. The glow pulsed, weaker and weaker."),

    ("ch4-amara-panic.mp3", AMARA,
     "It is going out! The light is fading!"),

    ("ch4-numbers-flash.mp3", ALICE,
     "Numbers flashed on the compass face, fast and urgent."),

    ("ch4-zoe-urgent.mp3", ZOE,
     "It needs answers. Right now. Quickly! There is no time to think too long."),

    ("ch4-compass-blazes.mp3", ALICE,
     "The compass blazed gold. The needle locked in place. It pointed straight at the far wall."),

    ("ch4-isla-door.mp3", ISLA,
     "There is a door! Right there in the wall! I never saw that door before!"),

    # ── CHAPTER 5 ──────────────────────────────────────────────────────────
    ("ch5-intro.mp3", ALICE,
     "The girls walked slowly toward it. The door was wooden and old, covered in carved patterns. The compass pulled toward it like a magnet."),

    ("ch5-compass-pulls.mp3", ALICE,
     "Zoe reached out and touched the handle."),

    ("ch5-zoe-handle.mp3", ZOE,
     "It is warm."),

    ("ch5-nod.mp3", ALICE,
     "She looked at the others. They nodded. She turned the handle. The door swung open."),

    ("ch5-forest.mp3", ALICE,
     "Beyond it was a forest. But not a normal forest. The trees glowed. The leaves shimmered cyan and purple. And the lights pulsed in a pattern."),

    ("ch5-priya.mp3", PRIYA,
     "What is this place?"),

    ("ch5-amara.mp3", AMARA,
     "I do not know. But I think we are meant to find out."),

    ("ch5-q10-question.mp3", ALICE,
     "Before they step through, the compass shows one more number. It has nine tens and one one. What number is that?"),

    # ── CLIFFHANGER ────────────────────────────────────────────────────────
    ("cliffhanger.mp3", ALICE,
     "The compass glowed in Zoe's hand. The forest waited beyond the door. The lights in the trees pulsed in a pattern, a pattern that looked almost like numbers. The adventure of The Crystal Compass had only just begun."),

    # ── SPEED ROUND QUESTIONS ───────────────────────────────────────────────
    ("sr-q1-question.mp3", ALICE,
     "Which is bigger, 38 or 83?"),

    ("sr-q2-question.mp3", ALICE,
     "Two tens and nine ones. What is the number?"),

    ("sr-q3-question.mp3", ALICE,
     "Which is smaller, 61 or 16?"),

    ("sr-q4-question.mp3", ALICE,
     "Five tens and five ones. What is the number?"),

    ("sr-q5-question.mp3", ALICE,
     "Put in order, smallest first. 42, 24, 44."),

    # ── FEEDBACK ───────────────────────────────────────────────────────────
    ("feedback-correct-1.mp3", ALICE,
     "Yes! That is correct!"),

    ("feedback-correct-2.mp3", ALICE,
     "Brilliant work!"),

    ("feedback-correct-3.mp3", ALICE,
     "You got it! Well done!"),

    ("feedback-correct-4.mp3", ALICE,
     "Amazing! Keep going!"),

    ("feedback-correct-5.mp3", ALICE,
     "Fantastic! That is right!"),

    ("feedback-correct-6.mp3", ALICE,
     "Perfect! The compass glows brighter!"),

    ("feedback-speed-correct.mp3", ALICE,
     "Yes! Nice and quick!"),

    ("feedback-speed-wrong.mp3", ALICE,
     "Not quite! Watch the timer!"),

    ("feedback-wrong-1.mp3", ALICE,
     "Not quite. Try again!"),

    ("feedback-wrong-2.mp3", ALICE,
     "Hmm, not right. Have another go!"),

    # ── WIN ────────────────────────────────────────────────────────────────
    ("win.mp3", ALICE,
     "Adventure complete! You helped unlock the Crystal Compass! The door to the magical forest is open!"),
]


def generate(filename, voice_id, text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": text,
        "model_id": MODEL,
        "voice_settings": VOICE_SETTINGS
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    if resp.status_code == 200:
        out_path = os.path.join(AUDIO_DIR, filename)
        with open(out_path, "wb") as f:
            f.write(resp.content)
        return True, None
    else:
        return False, f"HTTP {resp.status_code}: {resp.text[:200]}"


errors = []
success = 0

print(f"Generating {len(AUDIO_FILES)} audio files...")
for i, (fname, vid, txt) in enumerate(AUDIO_FILES, 1):
    print(f"[{i:02d}/{len(AUDIO_FILES)}] {fname}...", end=" ", flush=True)
    ok, err = generate(fname, vid, txt)
    if ok:
        print("✓")
        success += 1
    else:
        print(f"✗ {err}")
        errors.append((fname, err))
    time.sleep(0.4)  # be gentle with rate limits

print(f"\n=== DONE: {success}/{len(AUDIO_FILES)} generated ===")
if errors:
    print(f"\nErrors ({len(errors)}):")
    for fname, err in errors:
        print(f"  {fname}: {err}")
else:
    print("No errors!")
