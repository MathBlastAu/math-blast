#!/usr/bin/env python3
"""Generate full Issue 1 narration audio — George (narrator), Andrew (Jake), River (aliens)."""

import os, json, time
import urllib.request, urllib.error

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
MODEL   = "eleven_turbo_v2_5"
OUT_DIR = os.path.join(os.path.dirname(__file__), "sounds", "issue001")
os.makedirs(OUT_DIR, exist_ok=True)

GEORGE  = "JBFqnCBsd6RMkjVDRZzb"  # Narrator
ANDREW  = "BTEPH6wbWkb66Dys0ry6"  # Jake
RIVER   = "SAz9YHcvj6GT2YYXdXww"  # Aliens

NAR  = {"stability": 0.55, "similarity_boost": 0.75}
JAKE = {"stability": 0.50, "similarity_boost": 0.78}
ALIEN= {"stability": 0.18, "similarity_boost": 0.32, "style": 0.85}  # Pushed for alien effect

SEGMENTS = [
    # ── CHAPTER 1 ─────────────────────────────────────────────
    ("ch1-intro.mp3", GEORGE, NAR,
     "Jake the astronaut cadet was hurtling through the Zorblax Nebula — munching a space sandwich and humming to himself — when BANG! CRASH! CLONK! His rocket had smashed straight into Planet Zog! Through the smoke and sparks, Jake stumbled out and inspected the damage. But first — his training kicked in. Before any mission, his computer always ran a Pre-Launch Check. Even crashed on an alien planet, the rules were the rules."),

    ("ch1-q1-question.mp3", GEORGE, NAR,
     "The mission computer is counting down fuel reserves: 5, 10, 15... blank... 25... blank. What are the two missing numbers?"),

    ("ch1-q2-story.mp3", GEORGE, NAR,
     "With the computer check complete, Jake turned to the real problem. The engine room was a mess — fuel crystals scattered everywhere! He needed exactly 24 crystals to launch, arranged in rows of 6. Jake grabbed his maths notebook..."),

    ("ch1-q2-jake.mp3", ANDREW, JAKE,
     "Let me work this out carefully. 24 crystals, rows of 6... I need to think about my times tables here."),

    ("ch1-q2-question.mp3", GEORGE, NAR,
     "Jake needs 24 fuel crystals. They come in rows of 6. How many rows does he need to collect?"),

    # ── CHAPTER 2 ─────────────────────────────────────────────
    ("ch2-intro-nar.mp3", GEORGE, NAR,
     "Before Jake could fire up the engines, three small green aliens waddled over. The tallest one — wearing a tiny purple crown — bowed deeply."),

    ("ch2-bloop.mp3", RIVER, ALIEN,
     "Greetings, Space Human! I am Bloop. These are Zibble and Mork. We must share food before you leave. It is the Zog Law."),

    ("ch2-intro-end.mp3", GEORGE, NAR,
     "A giant glowing pizza appeared from nowhere. There were 4 of them altogether, and Bloop insisted everyone got an equal share."),

    ("ch2-q3-question.mp3", GEORGE, NAR,
     "4 friends share 1 pizza equally. What fraction does each person get?"),

    ("ch2-q4-story-nar.mp3", GEORGE, NAR,
     "Mork looked at his slice thoughtfully and pushed most of it toward Jake."),

    ("ch2-q4-mork.mp3", RIVER, ALIEN,
     "Mork not hungry. Mork eat only half of Mork's slice."),

    ("ch2-q4-story-end.mp3", GEORGE, NAR,
     "Jake wondered: if Mork's slice was one quarter of the whole pizza, and Mork only ate half of that — what fraction of the whole pizza did Mork eat?"),

    ("ch2-q4-question.mp3", GEORGE, NAR,
     "Mork's slice is one quarter of the pizza. Mork eats half of his slice. What fraction of the whole pizza did Mork eat?"),

    # ── CHAPTER 3 ─────────────────────────────────────────────
    ("ch3-intro-nar.mp3", GEORGE, NAR,
     "Jake was climbing back to his rocket when Mork suddenly grabbed his arm."),

    ("ch3-mork.mp3", RIVER, ALIEN,
     "Wait! Launch Window is critical! Leave too early or too late and you will be TRAPPED in the Zog Gravitational Loop for 47 years!"),

    ("ch3-intro-end.mp3", GEORGE, NAR,
     "Jake peered at the cockpit clock. He had to read it correctly — there was no room for error."),

    ("ch3-q5-question.mp3", GEORGE, NAR,
     "The short hand is just past the 3. The long hand points at the 3. What time does the clock show?"),

    ("ch3-q6-story.mp3", GEORGE, NAR,
     "The Launch Window closes in exactly 30 minutes, Mork warned. It was 3:15 now. Jake sprinted to the rocket, buckled his helmet, and punched the pre-launch sequence."),

    ("ch3-q6-jake.mp3", ANDREW, JAKE,
     "I need to be off the ground by... 3:15 plus 30 minutes. I need to calculate this!"),

    ("ch3-q6-question.mp3", GEORGE, NAR,
     "It is 3:15 now. The Launch Window closes in 30 minutes. What time must Jake launch by?"),

    # ── CHAPTER 4 ─────────────────────────────────────────────
    ("ch4-intro.mp3", GEORGE, NAR,
     "WHOOOOSH! Jake blasted off just in time. Ahead lay the Zorblax Asteroid Belt — a stretch of spinning space rocks every pilot dreaded. To get through safely, Jake had to calculate his exact route."),

    ("ch4-q7-question.mp3", GEORGE, NAR,
     "There are 6 asteroids in Jake's path. Each one is 7 light-seconds wide. How many light-seconds does Jake need to cross in total?"),

    ("ch4-q8-story.mp3", GEORGE, NAR,
     "Jake emerged from the asteroid belt — barely! He checked the storage bay. He had brought 36 star-coins to share equally between his 4 Zogling friends. Better calculate it now before he landed back on Earth."),

    ("ch4-q8-jake.mp3", ANDREW, JAKE,
     "36 star-coins, 4 friends... I need to divide them equally. Let me think..."),

    ("ch4-q8-question.mp3", GEORGE, NAR,
     "Jake has 36 star-coins. He shares them equally between 4 friends. How many coins does each friend get?"),

    # ── CHAPTER 5 ─────────────────────────────────────────────
    ("ch5-intro.mp3", GEORGE, NAR,
     "Earth was in sight! The blue-green marble shimmered through the cockpit window. But Mission Control crackled over the radio."),

    ("ch5-mission-control.mp3", RIVER, ALIEN,
     "Cadet Jake — two final anomalies before landing. Solve them to clear your re-entry path. Over."),

    ("ch5-nar-end.mp3", GEORGE, NAR,
     "Two problems. Then home. Jake reached for his notebook one last time."),

    ("ch5-q9-question.mp3", GEORGE, NAR,
     "Jake passes 4 space stations. At each station, 7 new rockets join his convoy. He started with 3 rockets already. How many rockets are in the convoy altogether?"),

    ("ch5-q10-story.mp3", GEORGE, NAR,
     "Mission Control again."),

    ("ch5-mission-control-2.mp3", RIVER, ALIEN,
     "Re-entry window opens at 4:10. Your heat shield takes exactly 35 minutes to warm up. What time do you need to start warming it up?"),

    ("ch5-q10-jake.mp3", ANDREW, JAKE,
     "Jake stared at the clock. The final maths problem of the whole mission. Get it right and I'll be home for dinner."),

    ("ch5-q10-question.mp3", GEORGE, NAR,
     "Re-entry window opens at 4:10. Heat shield warm-up takes 35 minutes. What time must Jake start the warm-up?"),

    # ── FEEDBACK ──────────────────────────────────────────────
    ("feedback-correct-1.mp3", ANDREW, JAKE, "Yes! That's it! Pre-launch check passed!"),
    ("feedback-correct-2.mp3", ANDREW, JAKE, "Brilliant! Nice work, space cadet!"),
    ("feedback-correct-3.mp3", ANDREW, JAKE, "Got it! Let's keep going!"),
    ("feedback-wrong-1.mp3",   ANDREW, JAKE, "Hmm, not quite. Let me think about this again..."),
    ("feedback-wrong-2.mp3",   ANDREW, JAKE, "Not this time — give it another go!"),

    # ── WIN ───────────────────────────────────────────────────
    ("win.mp3", GEORGE, NAR,
     "Mission complete! Jake's rocket touched down on Earth with a perfect landing — and it was all thanks to YOU! You solved every single challenge across five chapters, from Planet Zog all the way home. You're a true space cadet. See you in Issue 2!"),
]

def generate(filename, voice_id, settings, text):
    out_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(out_path):
        print(f"  ✓ {filename} (cached)")
        return True
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": settings
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
        print(f"  ❌ {filename}: HTTP {e.code} — {body[:150]}")
        return False

print(f"Generating {len(SEGMENTS)} audio segments for Issue 1...\n")
ok = 0
for fname, voice, settings, text in SEGMENTS:
    if generate(fname, voice, settings, text): ok += 1
    time.sleep(0.35)

print(f"\n{'='*50}")
print(f"Done: {ok}/{len(SEGMENTS)} segments generated")
print(f"Output: {OUT_DIR}")
total_size = sum(os.path.getsize(os.path.join(OUT_DIR, f)) for f in os.listdir(OUT_DIR) if f.endswith('.mp3'))
print(f"Total size: {total_size//1024//1024}MB ({total_size//1024}KB)")
