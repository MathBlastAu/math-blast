#!/usr/bin/env python3
"""
Fix Ocean Arc - Post-review fixes for all 4 issues
Generates audio files with correct voice assignments
"""
import os
import json
import time
import requests

ELEVENLABS_API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"

ERIC_ID    = "cjVigY5qzO86Huf0OWal"
JESSICA_ID = "cgSgspJ2msm6clMCkdW9"
BILL_ID    = "pqHfZKP75CvOlQylNhV4"

ERIC_SETTINGS    = {"stability": 0.5,  "similarity_boost": 0.75, "style": 0.2,  "use_speaker_boost": True}
JESSICA_SETTINGS = {"stability": 0.55, "similarity_boost": 0.80, "style": 0.25, "use_speaker_boost": True}
BILL_SETTINGS    = {"stability": 0.65, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True}
WREN_SETTINGS    = {"stability": 0.70, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True}  # Eric voice, Wren settings

E = lambda f, t: (f, ERIC_ID,    ERIC_SETTINGS,    t)
J = lambda f, t: (f, JESSICA_ID, JESSICA_SETTINGS, t)
B = lambda f, t: (f, BILL_ID,    BILL_SETTINGS,    t)
W = lambda f, t: (f, ERIC_ID,    WREN_SETTINGS,    t)  # Wren uses Eric voice ID

AUDIO_BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/audio/ocean"

# ALL AUDIO ITEMS TO GENERATE
items = []

# ============================================================
# ALL ISSUES — feedback-correct-1.mp3 (ocean-appropriate Q1 feedback)
# ============================================================
feedback_text = "Signal confirmed! First check complete. The Lattice is counting on you!"
for issue in ["issue001", "issue002", "issue003", "issue004"]:
    items.append(E(f"{AUDIO_BASE}/{issue}/feedback-correct-1.mp3", feedback_text))

# ============================================================
# ISSUE 1 — Cliffhanger split into 3 files
# ============================================================
items.extend([
    E(f"{AUDIO_BASE}/issue001/ch5-cliffhanger-narrate.mp3",
      "Marina stared into the dark water below the Lattice floor. Deep, deep below, in water so black it had no bottom, something was moving. A faint rhythmic glow pulsed in the blackness. Not random. Not scattered. Arranged in a pattern. Like rows. Like groups. Like something that understood mathematics. Enormous. Patient. Ancient."),
    J(f"{AUDIO_BASE}/issue001/ch5-cliffhanger-marina.mp3",
      "Elder Luma, I think whatever is down there, it isn't broken. I think it's trying to communicate."),
    E(f"{AUDIO_BASE}/issue001/ch5-cliffhanger-outro.mp3",
      "The hum deepened. The Lattice stones flickered once more. And far, far below, the glow pulsed on."),
])

# ============================================================
# ISSUE 1 — Win screen narration
# ============================================================
items.append(E(f"{AUDIO_BASE}/issue001/win.mp3",
    "You made it to Luminos and helped Marina understand the Lattice. Groups of equal size, equal groups, that's what multiplication is. And something down in the deep is using that same pattern. Join us for the next issue: The Ripple Pattern, follow Marina to the outer Lattice fields and discover skip counting!"))

# ============================================================
# ISSUE 2 — Re-record ch1-wren.mp3 with Wren voice
# ============================================================
items.append(W(f"{AUDIO_BASE}/issue002/ch1-wren.mp3",
    "The Lattice is largest out here. We count the stones by skipping. It is the fastest way, and the way that matches how the signal travels. You will see."))

# ============================================================
# ISSUE 2 — ch2 voice fixes
# ============================================================
items.extend([
    W(f"{AUDIO_BASE}/issue002/ch2-wren.mp3",
      "When you count by twos, you are not just skipping. You are counting groups of two. Five skips is five groups of two. Five times two."),
    J(f"{AUDIO_BASE}/issue002/ch2-marina.mp3",
      "So skip counting is multiplication. Counting by fives is the same as multiplying by five. Counting by tens is multiplying by ten."),
    W(f"{AUDIO_BASE}/issue002/ch2-wren-confirm.mp3",
      "Exactly. The Lattice uses this to send signals fast. When a stone sends to two stones, and those two each send to two more, the count doubles every step. Skip by skip, group by group."),
])

# ============================================================
# ISSUE 2 — ch3-wren.mp3 with Wren voice
# ============================================================
items.append(W(f"{AUDIO_BASE}/issue002/ch3-wren.mp3",
    "This is the main transmission grid. Thousands of stones, in groups of ten. We count by tens out here because a single signal can jump ten stones at once."))

# ============================================================
# ISSUE 2 — Cliffhanger split into 4 files
# ============================================================
items.extend([
    E(f"{AUDIO_BASE}/issue002/ch5-cf-narrate.mp3",
      "Marina and Wren stood frozen, both of them looking upward. The shadow had come back. Larger this time, or perhaps closer. It moved with slow, deliberate patience, blotting out the filtered light until the ocean floor around them was near-black."),
    J(f"{AUDIO_BASE}/issue002/ch5-cf-marina.mp3",
      "Wren, what kind of creature makes a shadow that big?"),
    W(f"{AUDIO_BASE}/issue002/ch5-cf-wren.mp3",
      "In all my lifetimes working the Lattice, and all the records of all the keepers before me, nothing that size has ever been seen. Not once. Not in living memory."),
    E(f"{AUDIO_BASE}/issue002/ch5-cf-outro.mp3",
      "The shadow passed. Below the ocean floor, the deep rhythmic hum continued, patient as a heartbeat."),
])

# ============================================================
# ISSUE 2 — Win screen
# ============================================================
items.append(E(f"{AUDIO_BASE}/issue002/win.mp3",
    "You helped Marina and Wren map the fault in the Lattice using skip counting. Skip counting by twos, fives, and tens is just multiplication in disguise. And something enormous is up there, above the Lattice. The next issue awaits: Rows and Columns!"))

# ============================================================
# ISSUES 3 & 4 — Review voice assignments
# Issue 3: ch5-luma.mp3 — check if it's Bill voice (it should be)
# Issue 3: ch5-marina.mp3 — check if it's Jessica voice
# These were generated correctly already but the cliffhanger needs splitting
# Issue 3 — Cliffhanger split (currently all Eric)
# ============================================================
items.extend([
    E(f"{AUDIO_BASE}/issue003/ch5-cf-narrate.mp3",
      "Elder Luma closed the Archive door behind them. Through the thick crystal window, the glow from the deep pulsed rhythmically, patient and vast. Marina pressed her hand against the glass."),
    J(f"{AUDIO_BASE}/issue003/ch5-cf-marina.mp3",
      "It's counting. Whatever it is, it's counting in rows and columns. Just like we were."),
    B(f"{AUDIO_BASE}/issue003/ch5-cf-luma.mp3",
      "The Archive has records going back ten thousand tides. Nothing in those records describes a creature that understands mathematics. Until now."),
    E(f"{AUDIO_BASE}/issue003/ch5-cf-outro.mp3",
      "The glow pulsed on. Below the Archive, below the Lattice, below everything they knew, something immense and patient was waiting."),
])

# Issue 3 — Win screen
items.append(E(f"{AUDIO_BASE}/issue003/win.mp3",
    "You helped Marina and Elder Luma decode the Archive records using rows and columns. Arrays are everywhere in mathematics, and something ancient in the deep uses them too. The next issue awaits: The Resonance Whale!"))

# ============================================================
# ISSUE 4 — Finale split + win
# ============================================================
items.extend([
    E(f"{AUDIO_BASE}/issue004/ch5-cf-narrate.mp3",
      "The Whale's song filled the entire Luminous Deep. Not a cry, not a warning. Something else. A pattern that repeated and built and grew, layer upon layer, until the ocean floor itself seemed to vibrate with it."),
    J(f"{AUDIO_BASE}/issue004/ch5-cf-marina.mp3",
      "It's multiplication. The whole song is multiplication. It's been trying to show us all along."),
    E(f"{AUDIO_BASE}/issue004/ch5-cf-outro.mp3",
      "Elder Luma placed a single glowing signal stone into Marina's palm. Small and warm and pulsing with the same rhythm as the Whale's song. A gift. A memory. A promise."),
])

items.append(E(f"{AUDIO_BASE}/issue004/win.mp3",
    "You did it! Marina solved the pattern of the Resonance Whale, and the Luminous Deep is singing again. The Whale is at peace, the Lattice glows, and Elder Luma has gifted Marina a signal stone to remember the deep. Thank you for joining the Ocean Arc. More adventures await in Math Blast!"))


def generate_audio(voice_id, voice_settings, text, out_path):
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": voice_settings
    }
    url = f"{BASE_URL}/{voice_id}"
    for attempt in range(3):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            if r.status_code == 200:
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, "wb") as f:
                    f.write(r.content)
                print(f"  ✅ {os.path.basename(out_path)}")
                return True
            elif r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 60))
                print(f"  ⏳ Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ❌ HTTP {r.status_code}: {r.text[:200]}")
                return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            if attempt < 2:
                time.sleep(5)
    return False


def main():
    print(f"Generating {len(items)} audio files...\n")
    ok = 0
    fail = 0
    for fname, voice_id, voice_settings, text in items:
        voice_name = "Eric" if voice_id == ERIC_ID and voice_settings == ERIC_SETTINGS else \
                     "Wren" if voice_id == ERIC_ID else \
                     "Jessica" if voice_id == JESSICA_ID else "Bill"
        print(f"  [{voice_name}] {os.path.basename(fname)}")
        if generate_audio(voice_id, voice_settings, text, fname):
            ok += 1
        else:
            fail += 1
        time.sleep(0.5)

    print(f"\n✅ {ok} generated, ❌ {fail} failed")


if __name__ == "__main__":
    main()
