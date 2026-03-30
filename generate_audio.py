#!/usr/bin/env python3
"""Generate all audio files for Math Blast Ocean Issue 1 using ElevenLabs API."""

import subprocess
import os
import time
import json

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUTPUT_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/audio/ocean/issue001"

# Voice configs
ERIC   = {"voice_id": "cjVigY5qzO86Huf0OWal", "stability": 0.5,  "similarity_boost": 0.75, "style": 0.2}
JESSICA= {"voice_id": "cgSgspJ2msm6clMCkdW9", "stability": 0.55, "similarity_boost": 0.80, "style": 0.25}
BILL   = {"voice_id": "pqHfZKP75CvOlQylNhV4", "stability": 0.65, "similarity_boost": 0.75, "style": 0.15}

# Old files to delete
OLD_FILES = [
    "ch1-approach.mp3", "ch1-city.mp3", "ch1-arrival.mp3", "ch1-luma-welcome.mp3",
    "ch2-intro.mp3", "ch2-luma.mp3", "ch2-lattice.mp3", "ch2-city.mp3",
    "ch3-intro.mp3", "ch3-luma.mp3", "ch3-marina.mp3", "ch3-map.mp3", "ch3-luma2.mp3",
    "ch4-intro.mp3", "ch4-datapad.mp3", "ch4-marina.mp3", "ch4-luma.mp3",
    "ch5-intro.mp3", "ch5-hum.mp3", "ch5-marina.mp3", "ch5-luma.mp3",
]

# Files to generate: (filename, voice_config, text)
FILES = [
    # Chapter story audio
    ("ch1-approach.mp3", ERIC,
     "The sub broke through the thermal layer and Luminos appeared below them, and Marina forgot to breathe. She had seen cities before. She had never seen anything like this. Coral towers in amber and teal, glowing from the inside out. Coralfolk moving through wide streets like a living tide, hundreds of them, shells catching the soft light. Schools of silver fish weaved between the towers in perfect formation. Flick pressed against the porthole beside her, antenna fins pointed in six directions at once."),

    ("ch1-arrival.mp3", ERIC,
     "Marina docked the sub, suited up, and stepped out into the water. The city sounds surrounded her immediately, a low harmonic hum that seemed to come from the stones in the streets themselves, steady and rhythmic, almost like breathing."),

    ("ch1-luma-welcome.mp3", BILL,
     "Welcome to Luminos."),

    ("ch2-intro.mp3", ERIC,
     "The Coralfolk who met them at the dock was not there to give them a tour. Elder Luma was ancient, even by Coralfolk reckoning, his shell etched deep with a thousand tides of patterns. He had been watching for an outside arrival. He led Marina and Flick through the market streets at a fast clip, past stalls piled with glowing supplies, past groups of Coralfolk children who stopped and stared at the strange tall visitor in the dive suit."),

    ("ch2-city.mp3", ERIC,
     "Marina caught glimpses as she passed: vendors arranging goods in careful equal rows, keeper groups moving through the outer streets in organised pairs, fish schools looping the towers in tight equal clusters. Everything in Luminos moved in patterns. Equal groups. She could feel it."),

    ("ch2-luma.mp3", BILL,
     "Three outer cities have gone dark. No signals in. No signals out. The families inside cannot reach their relatives. My people are frightened. And the dark is spreading."),

    ("ch3-intro.mp3", ERIC,
     "The Signal Tower stood at the centre of Luminos, taller than all the coral towers around it, humming with a deep, steady energy."),

    ("ch3-luma.mp3", BILL,
     "The Lattice sends messages in equal groups. Stone to stone. Group by group. When it works, a message from Luminos reaches every city in the deep within minutes."),

    ("ch3-map.mp3", ERIC,
     "Three sections of the map were dark. And the edge of the dark was moving slowly outward, one stone group at a time."),

    ("ch3-luma2.mp3", BILL,
     "If we do not find the cause, Luminos itself will go silent."),

    ("ch4-intro.mp3", ERIC,
     "Marina studied the pattern on the map. The dark sections weren't random. They spread outward from a single point, somewhere deep below the Lattice floor. Something down there was interfering with the signal."),

    ("ch4-marina.mp3", JESSICA,
     "I can calculate which stone groups should be active. If I compare what should be glowing to what actually is, I can find exactly where the fault starts. But I need to understand how the groups work."),

    ("ch4-luma.mp3", BILL,
     "Then let us count. Together."),

    ("ch5-intro.mp3", ERIC,
     "Marina was mid-calculation when the floor vibrated. Not an earthquake. A sound. Deep, rhythmic, patient, coming from somewhere far below the city. The Lattice stones in the Signal Tower flickered once. Then twice. The hum in the streets, the steady breathing sound Marina had noticed when she first arrived, changed pitch. Deepened. Elder Luma went completely still. Every Coralfolk in the Signal Tower stopped moving."),

    ("ch5-marina.mp3", JESSICA,
     "Elder Luma, what was that?"),

    ("ch5-luma.mp3", BILL,
     "It has not done that in ten thousand tides."),

    # Question setup audio
    ("ch2-q3-setup.mp3", ERIC,
     "Marina spots a row of market stalls, each one stocked with equal amounts of glowing goods."),

    ("ch3-q5-setup.mp3", ERIC,
     "The coral tower beside the Signal Tower has glowing windows arranged in equal groups on each level."),

    ("ch4-q7-setup.mp3", ERIC,
     "Marina watches three keeper groups heading out to check the outer Lattice stones."),

    ("ch4-q8-setup.mp3", ERIC,
     "The Signal Tower lanterns hang in five equal groups along each walkway."),

    ("ch5-q10-setup.mp3", ERIC,
     "Marina's final calculation: stone clusters that have gone dark, counted in groups of three."),

    # Question audio
    ("ch1-q1-question.mp3", ERIC,
     "At the docking bay, 2 groups of Coralfolk are unloading supplies, with 3 in each group. How many Coralfolk altogether? 2 groups of 3."),

    ("ch2-q2-question.mp3", ERIC,
     "A school of fish loops the towers in 4 tight groups, with 2 fish in each group. How many fish in the school? 4 groups of 2."),

    ("ch2-q3-question.mp3", ERIC,
     "The market has 3 stalls in a row, each stall stocked with 5 glowing items. How many items altogether? 3 groups of 5."),

    ("ch3-q4-question.mp3", ERIC,
     "5 keeper groups head out to the Lattice, with 2 keepers in each group. How many keepers in total? 5 groups of 2."),

    ("ch3-q5-question.mp3", ERIC,
     "The coral tower has 2 levels, with 6 glowing windows on each level. How many windows altogether? 2 groups of 6."),

    ("ch4-q6-question.mp3", ERIC,
     "4 clusters of signal stones line the outer field, with 4 stones in each cluster. How many stones altogether? 4 groups of 4."),

    ("ch4-q7-question.mp3", ERIC,
     "3 keeper groups head out, with 6 keepers in each group. How many keepers altogether? 3 groups of 6."),

    ("ch4-q8-question.mp3", ERIC,
     "5 walkways in the Signal Tower, each with 4 lanterns. How many lanterns in total? 5 groups of 4."),

    ("ch5-q9-question.mp3", ERIC,
     "2 groups of Coralfolk gather at the Signal Tower to watch the flickering stones, with 7 in each group. How many Coralfolk watching? 2 groups of 7."),

    ("ch5-q10-question.mp3", ERIC,
     "Marina's final count: 3 clusters of dark signal stones, with 3 stones in each cluster. How many stones have gone dark? 3 groups of 3."),

    # Answer audio
    ("ch1-q1-answer.mp3", ERIC,
     "That's right! 2 groups of 3 equals 6 Coralfolk at the dock. Equal groups is exactly how multiplication works!"),

    ("ch2-q2-answer.mp3", ERIC,
     "Correct! 4 groups of 2 equals 8 fish in the school. The fish always move in equal groups through Luminos."),

    ("ch2-q3-answer.mp3", ERIC,
     "Right! 3 groups of 5 equals 15 items. The market vendors always stock in equal amounts."),

    ("ch3-q4-answer.mp3", ERIC,
     "Yes! 5 groups of 2 equals 10 keepers heading out to check the Lattice."),

    ("ch3-q5-answer.mp3", ERIC,
     "Correct! 2 groups of 6 equals 12 glowing windows in the tower."),

    ("ch4-q6-answer.mp3", ERIC,
     "Right! 4 groups of 4 equals 16 signal stones in the outer field."),

    ("ch4-q7-answer.mp3", ERIC,
     "Yes! 3 groups of 6 equals 18 keepers. The Lattice needs every one of them."),

    ("ch4-q8-answer.mp3", ERIC,
     "Correct! 5 groups of 4 equals 20 lanterns lighting the Signal Tower."),

    ("ch5-q9-answer.mp3", ERIC,
     "Right! 2 groups of 7 equals 14 Coralfolk. The whole city is watching now."),

    ("ch5-q10-answer.mp3", ERIC,
     "You got it! 3 groups of 3 equals 9 dark stones. Marina marks the last cluster. Now, what is making that hum?"),
]


def delete_old_files():
    print("=== Deleting old files ===")
    for fname in OLD_FILES:
        fpath = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(fpath):
            os.remove(fpath)
            print(f"  Deleted: {fname}")
        else:
            print(f"  Not found (skip): {fname}")


def generate_file(filename, voice, text):
    output_path = os.path.join(OUTPUT_DIR, filename)
    payload = json.dumps({
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": voice["stability"],
            "similarity_boost": voice["similarity_boost"],
            "style": voice["style"]
        }
    })
    cmd = [
        "curl", "-s", "-X", "POST",
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice['voice_id']}",
        "-H", f"xi-api-key: {API_KEY}",
        "-H", "Content-Type: application/json",
        "-d", payload,
        "--output", output_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        return False, f"curl error: {result.stderr.decode()}"
    if not os.path.exists(output_path):
        return False, "file not created"
    size = os.path.getsize(output_path)
    if size == 0:
        return False, "file is empty (0 bytes)"
    return True, size


def main():
    delete_old_files()
    print(f"\n=== Generating {len(FILES)} audio files ===\n")

    results = []
    for i, (filename, voice, text) in enumerate(FILES, 1):
        print(f"[{i:02d}/{len(FILES)}] Generating {filename}...", end=" ", flush=True)
        success, info = generate_file(filename, voice, text)
        if success:
            print(f"OK ({info:,} bytes)")
            results.append((filename, True, info))
        else:
            print(f"FAILED: {info}")
            results.append((filename, False, info))
        if i < len(FILES):
            time.sleep(0.5)

    print("\n=== SUMMARY ===")
    succeeded = [(f, s) for f, ok, s in results if ok]
    failed    = [(f, s) for f, ok, s in results if not ok]

    print(f"\n✅ Succeeded: {len(succeeded)}/{len(FILES)}")
    for fname, size in succeeded:
        print(f"   {fname}: {size:,} bytes")

    if failed:
        print(f"\n❌ Failed: {len(failed)}/{len(FILES)}")
        for fname, reason in failed:
            print(f"   {fname}: {reason}")
    else:
        print("\nAll files generated successfully!")


if __name__ == "__main__":
    main()
