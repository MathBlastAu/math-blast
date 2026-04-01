#!/usr/bin/env python3
"""Generate all audio for Crystal Compass Issue 1 via ElevenLabs API"""
import os, requests, json

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
OUT_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/audio/crystal-compass/issue-001"
os.makedirs(OUT_DIR, exist_ok=True)

# Voice IDs
ALICE = "Xb7hH8MSUJpSbSDYk0k2"    # narrator
LAURA = "FGY2WhTYpPnrIDTdsKH5"    # Miss Zara
JESSICA = "cgSgspJ2msm6clMCkdW9"  # Isla
SARAH = "EXAVITQu4vr4xnSDxMaL"   # Priya
MATILDA = "XrExE9yKIg1WjnnlVkGX"  # Zoe
BELLA = "hpp4J3VqNfWAUOO0d1Us"    # Amara

VOICE_SETTINGS = {"stability": 0.5, "similarity_boost": 0.75, "style": 0.3}

# All audio scripts
# Format: (filename, voice_id, text)
AUDIO_SCRIPTS = [
    # ─── CHAPTER 1 ───
    ("ch1-intro.mp3", ALICE,
     "It was the last day of term at Methodist Ladies' College. The four friends had one last job to do."),
    ("ch1-miss-zara.mp3", LAURA,
     "Girls, would you please return these books to the old library? The one in the east wing."),
    ("ch1-library.mp3", ALICE,
     "The library was warm and quiet. Golden light filled the room. Nobody else was there."),
    ("ch1-priya-spots.mp3", SARAH,
     "Wait, look at that. There's something on the shelf. Something is glowing."),
    ("ch1-isla-reaches.mp3", JESSICA,
     "Ooh, let me see it! I want to open it!"),
    ("ch1-zoe-wait.mp3", MATILDA,
     "Wait. We should open it carefully. We do not know what it is."),
    ("ch1-compass-reveal.mp3", ALICE,
     "Inside the box was a beautiful compass. It glowed with soft cyan light. The needle spun and spun. It would not stop."),
    ("ch1-q1-question.mp3", ALICE,
     "The compass face shows a number. It has two tens and three ones. What number is that?"),

    # ─── CHAPTER 2 ───
    ("ch2-intro.mp3", ALICE,
     "Amara picked up the compass. The glow flickered. Numbers appeared on the face, but they looked wrong."),
    ("ch2-amara.mp3", BELLA,
     "The numbers look all mixed up. Like they are in the wrong order."),
    ("ch2-zoe-studies.mp3", MATILDA,
     "I think I understand. The numbers need to be in the right place. Tens go here. Ones go here."),
    ("ch2-zoe-explains.mp3", MATILDA,
     "If the digits are in the wrong place, the whole number changes. Everything changes."),
    ("ch2-q2-question.mp3", ALICE,
     "The compass shows four tens and seven ones. What number is that?"),
    ("ch2-q3-intro.mp3", ALICE,
     "Now the compass changes. The digits swap around. Look carefully at the new number."),
    ("ch2-q3-question.mp3", ALICE,
     "Now the compass shows seven tens and four ones. What number is that? Is it bigger or smaller than forty seven?"),

    # ─── CHAPTER 3 ───
    ("ch3-intro.mp3", ALICE,
     "The girls sat at a big library table. Priya pulled out her notebook. She loved finding patterns."),
    ("ch3-priya-notebook.mp3", SARAH,
     "Let us figure out the rules. We test the numbers one by one."),
    ("ch3-compass-responds.mp3", ALICE,
     "Every time the tens and ones were right, the compass glowed brighter. Every time they mixed them up, the light faded."),
    ("ch3-priya-language.mp3", SARAH,
     "It is like a language. Numbers have an order. They have a place where they belong."),
    ("ch3-amara.mp3", BELLA,
     "Then we need to learn to speak it. Come on, let us keep going."),
    ("ch3-q4-question.mp3", ALICE,
     "The compass shows five tens and zero ones. What number is that?"),
    ("ch3-q5-question.mp3", ALICE,
     "Now it shows zero tens and eight ones. What number is that?"),
    ("ch3-q6-question.mp3", ALICE,
     "Now the compass shows six tens and three ones. What number is that?"),

    # ─── CHAPTER 4 ───
    ("ch4-intro.mp3", ALICE,
     "Suddenly the compass light began to fade. The glow pulsed, weaker and weaker."),
    ("ch4-amara-panic.mp3", BELLA,
     "It is going out! The light is fading! What do we do?"),
    ("ch4-zoe-urgent.mp3", MATILDA,
     "It needs answers. Right now. Quickly! There is no time to think."),
    ("ch4-numbers-flash.mp3", ALICE,
     "Numbers flashed on the compass face, fast and urgent. The compass was fading. Every second counted."),
    # Speed round questions (read by narrator, urgent tone)
    ("sr-q1-question.mp3", ALICE,
     "Quick! Which is bigger, thirty eight or eighty three?"),
    ("sr-q2-question.mp3", ALICE,
     "Two tens and nine ones. What is the number?"),
    ("sr-q3-question.mp3", ALICE,
     "Which is smaller, sixty one or sixteen?"),
    ("sr-q4-question.mp3", ALICE,
     "Five tens and five ones. What is the number?"),
    ("sr-q5-question.mp3", ALICE,
     "Put these numbers in order from smallest to biggest. Forty two, twenty four, forty four."),
    ("ch4-compass-blazes.mp3", ALICE,
     "The compass blazed gold. The needle locked in place. It pointed straight at the far wall."),
    ("ch4-isla-door.mp3", JESSICA,
     "There is a door! Right there in the wall! I never saw that door before!"),

    # ─── CHAPTER 5 ───
    ("ch5-intro.mp3", ALICE,
     "The girls walked slowly toward the door. It was wooden and old, covered in carved patterns."),
    ("ch5-compass-pulls.mp3", ALICE,
     "The compass pulled toward the door like a magnet. Something was calling them through."),
    ("ch5-zoe-handle.mp3", MATILDA,
     "The handle is warm. It is warm to touch."),
    ("ch5-nod.mp3", ALICE,
     "Zoe looked at the others. They nodded. She turned the handle. The door swung open."),
    ("ch5-forest.mp3", ALICE,
     "Beyond the door was a forest. But not a normal forest. The trees glowed. The leaves shimmered cyan and purple. And the lights pulsed in a pattern."),
    ("ch5-priya.mp3", SARAH,
     "What is this place? Where does this go?"),
    ("ch5-amara.mp3", BELLA,
     "I do not know. But I think we are meant to find out."),
    ("ch5-q10-question.mp3", ALICE,
     "Before they step through, the compass asks one last question. What number is made of ten tens?"),

    # ─── CLIFFHANGER ───
    ("cliffhanger.mp3", ALICE,
     "The compass glowed in Zoe's hand. The forest waited beyond the door. The adventure had only just begun."),

    # ─── FEEDBACK ───
    ("feedback-correct-1.mp3", ALICE,
     "That is right! Well done!"),
    ("feedback-correct-2.mp3", ALICE,
     "Yes! You got it!"),
    ("feedback-correct-3.mp3", ALICE,
     "Brilliant! The compass agrees!"),
    ("feedback-correct-4.mp3", ALICE,
     "Excellent work! Keep going!"),
    ("feedback-correct-5.mp3", ALICE,
     "Perfect! You are learning the language of numbers!"),
    ("feedback-correct-6.mp3", ALICE,
     "The compass glows a little brighter!"),
    ("feedback-wrong-1.mp3", ALICE,
     "Not quite. Try again. Think about the tens and the ones."),
    ("feedback-wrong-2.mp3", ALICE,
     "Hmm, not that one. Look at the number carefully and try again."),
    ("feedback-speed-correct.mp3", ALICE,
     "Yes!"),
    ("feedback-speed-wrong.mp3", ALICE,
     "The light fades a little more."),
    ("win.mp3", ALICE,
     "Amazing work! You helped Zoe and the girls unlock the compass. Place value is your superpower now!"),
]

def gen_audio(filename, voice_id, text):
    out_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(out_path):
        print(f"SKIP (exists): {filename}")
        return True
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": VOICE_SETTINGS
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        print(f"ERROR {filename}: {resp.status_code} {resp.text[:200]}")
        return False
    with open(out_path, "wb") as f:
        f.write(resp.content)
    print(f"OK: {filename} ({len(resp.content)//1024}KB)")
    return True

errors = []
for fname, voice, text in AUDIO_SCRIPTS:
    ok = gen_audio(fname, voice, text)
    if not ok:
        errors.append(fname)

print(f"\n=== DONE. Errors: {len(errors)} ===")
for e in errors:
    print(f"  FAILED: {e}")
