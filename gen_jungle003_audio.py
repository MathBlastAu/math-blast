#!/usr/bin/env python3
"""
Jungle Issue 3 — Audio gen: scripts extracted DIRECTLY from on-screen HTML text.
Every paragraph covered. Cast: Eric (narrator), Jessica (Blaze), Bill (Elder Splash), Charlie (Ripple)
"""
import requests, os, time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue003")
os.makedirs(OUT_DIR, exist_ok=True)

VOICES = {
    "narrator": ("cjVigY5qzO86Huf0OWal", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),
    "blaze":    ("cgSgspJ2msm6clMCkdW9", {"stability": 0.55, "similarity_boost": 0.75, "style": 0.30}),
    "elder":    ("pqHfZKP75CvOlQylNhV4", {"stability": 0.68, "similarity_boost": 0.70, "style": 0.20}),  # Bill — measured, formal
    "ripple":   ("IKne3meq5aSn9XLyUdCD", {"stability": 0.45, "similarity_boost": 0.70, "style": 0.50}),  # Charlie — energetic
}

SEGMENTS = [
    # ── CHAPTER 1 ─────────────────────────────────────────────────────
    # Para 1: "The path from Fernmoss led Blaze through the mist — ...glowing with soft rainbow light."
    ("ch1-intro", "narrator",
     "The path from Fernmoss led Blaze through the mist — and suddenly the trees opened up to reveal "
     "Cascade Clearing: a wide, misty waterfall clearing in the middle-canopy, glowing with soft rainbow light."),

    # Para 2: "The Splash-Sprockets were everywhere...nothing was ready."
    ("ch1-chaos", "narrator",
     "The Splash-Sprockets were everywhere, rushing in every direction. "
     "A century-old festival was about to begin — and nothing was ready."),

    # Para 3: Elder dialogue
    ("ch1-elder", "elder",
     "You! Explorer! Can you count in groups? "
     "Everything for the festival must be arranged in exact group sizes. Not shared. Grouped. "
     "We have sixty lanterns and they must go in groups of ten."),

    # Q1 question
    ("ch1-q1-question", "blaze",
     "Sixty lanterns in groups of ten. How many groups?"),

    # Q1 answer
    ("ch1-q1-answer", "blaze",
     "Sixty divided by ten equals six. Six groups of ten lanterns — the festival entrance is ready."),

    # ── CHAPTER 2 ─────────────────────────────────────────────────────
    # Para 1: "The lanterns were sorted...both in unorganised heaps."
    ("ch2-intro", "narrator",
     "The lanterns were sorted. Blaze moved to the next table — "
     "ribbon-flowers and sparkle-stones, both in unorganised heaps."),

    # Para 2: Blaze counting ribbon-flowers
    ("ch2-blaze", "blaze",
     "Forty-five ribbon-flowers. Groups of nine. Let me work this out."),

    # Para 3: "The sparkle-stones were next...for the display arches."
    ("ch2-sparkle", "narrator",
     "The sparkle-stones were next — seventy-two of them, cool and glittering in her hands. "
     "They needed to go in groups of eight for the display arches."),

    # Q2 question
    ("ch2-q2-question", "blaze",
     "Forty-five ribbon-flowers in groups of nine. How many groups?"),

    # Q2 answer
    ("ch2-q2-answer", "blaze",
     "Forty-five divided by nine equals five. Five groups of nine ribbon-flowers."),

    # Q3 setup: "The sparkle-stones were next — seventy-two, for the display arches. Groups of eight."
    ("ch2-q3-setup", "narrator",
     "The sparkle-stones were next — seventy-two of them, for the display arches. Groups of eight."),

    # Q3 question
    ("ch2-q3-question", "blaze",
     "Seventy-two sparkle-stones in groups of eight. How many groups?"),

    # Q3 answer
    ("ch2-q3-answer", "blaze",
     "Seventy-two divided by eight equals nine. Nine groups of eight sparkle-stones for the display arches."),

    # ── CHAPTER 3 ─────────────────────────────────────────────────────
    # Para 1: "While Blaze worked, a Splash-Sprocket named Ripple came running over, breathless."
    ("ch3-intro", "narrator",
     "While Blaze worked, a Splash-Sprocket named Ripple came running over, breathless."),

    # Para 2: Ripple dialogue
    ("ch3-ripple", "ripple",
     "Explorer! There's something strange near the waterfall — "
     "a huge pile of vines, all bundled up. Eighty-four of them, in neat groups of twelve!"),

    # Para 3: "Blaze went to look...She found a second cache...ninety-six vines, arranged in groups of six."
    ("ch3-blaze-looks", "narrator",
     "Blaze went to look. The bundles were perfect — seven of them, identical. This was not random. "
     "She found a second cache deeper in the clearing: ninety-six vines, arranged in groups of six."),

    # Para 4: Blaze speaks
    ("ch3-blaze-realises", "blaze",
     "It's organising. Not destroying. Grouping — just like us."),

    # Q4 question
    ("ch3-q4-question", "blaze",
     "Eighty-four vines bundled in groups of twelve. How many bundles?"),

    # Q4 answer
    ("ch3-q4-answer", "blaze",
     "Eighty-four divided by twelve equals seven. Seven bundles — and Tangle always uses groups of twelve."),

    # Q5 setup: "A second cache — ninety-six vines, arranged in groups of six."
    ("ch3-q5-setup", "narrator",
     "A second cache deeper in the clearing: ninety-six vines, arranged in groups of six."),

    # Q5 question
    ("ch3-q5-question", "blaze",
     "Ninety-six vines in groups of six. How many groups?"),

    # Q5 answer
    ("ch3-q5-answer", "blaze",
     "Ninety-six divided by six equals sixteen. Sixteen groups. Tangle is grouping, not destroying."),

    # ── CHAPTER 4 ─────────────────────────────────────────────────────
    # Para 1: "The Elder appeared before Blaze with a challenge in their eyes."
    ("ch4-intro", "narrator",
     "The Elder appeared before Blaze with a challenge in their eyes."),

    # Para 2: Elder challenge dialogue
    ("ch4-elder", "elder",
     "Explorer. A competition. One hundred festival items. "
     "First: arrange them in groups of four. How many groups? "
     "Then — same one hundred items, groups of five. Which arrangement gives more groups?"),

    # Para 3: "The last challenge: fifty-seven celebration berries...fifty-seven didn't divide evenly."
    ("ch4-last-challenge", "narrator",
     "The last challenge: fifty-seven celebration berries for the half-berry ceremony. "
     "Groups of eight — but fifty-seven didn't divide evenly."),

    # Q6 question
    ("ch4-q6-question", "blaze",
     "One hundred festival items in groups of four. How many groups?"),

    # Q6 answer
    ("ch4-q6-answer", "blaze",
     "One hundred divided by four equals twenty-five. Twenty-five groups of four."),

    # Q7 setup: Elder — same 100, groups of 5
    ("ch4-q7-setup", "elder",
     "Same one hundred items. Now groups of five. How many groups — and which gives more?"),

    # Q7 question
    ("ch4-q7-question", "blaze",
     "One hundred items in groups of five. How many groups? And which gives more — groups of four or groups of five?"),

    # Q7 answer
    ("ch4-q7-answer", "blaze",
     "One hundred divided by five equals twenty. Groups of four give more — twenty-five versus twenty. "
     "Smaller group size means more groups."),

    # Q8 setup: "The last challenge — fifty-seven celebration berries, groups of eight."
    ("ch4-q8-setup", "narrator",
     "The last challenge: fifty-seven celebration berries for the half-berry ceremony. Groups of eight."),

    # Q8 question
    ("ch4-q8-question", "blaze",
     "Fifty-seven celebration berries in groups of eight. How many complete groups — and how many are left over?"),

    # Q8 answer
    ("ch4-q8-answer", "blaze",
     "Fifty-seven divided by eight is seven remainder one. "
     "Seven complete groups, with one berry left over for the half-berry ceremony."),

    # ── CHAPTER 5 ─────────────────────────────────────────────────────
    # Para 1: "Blaze had answered every challenge. The Elder nodded slowly..."
    ("ch5-intro", "narrator",
     "Blaze had answered every challenge. "
     "The Elder nodded slowly — the closest thing a Splash-Sprocket did to applause."),

    # Para 2: Elder — one final test
    ("ch5-elder-final", "elder",
     "One final test. One hundred and fifty-six sparkle-stones. Groups of twelve. How many groups?"),

    # Para 3: "Then the Elder raised one more question...Two hundred sparkle-stones...group size was unknown."
    ("ch5-200-stones", "narrator",
     "Then the Elder raised one more question — the hardest yet. "
     "Two hundred sparkle-stones, laid out in a long row. "
     "The Elder wanted exactly twenty-five groups. But the group size was unknown."),

    # Para 4: Blaze — work backwards
    ("ch5-blaze-backwards", "blaze",
     "Work backwards. Two hundred divided by twenty-five tells you the group size."),

    # Q9 question
    ("ch5-q9-question", "blaze",
     "One hundred and fifty-six sparkle-stones in groups of twelve. How many groups?"),

    # Q9 answer
    ("ch5-q9-answer", "blaze",
     "One hundred and fifty-six divided by twelve equals thirteen. Thirteen groups of twelve sparkle-stones."),

    # Q10 setup: both paragraphs from story-q10s
    ("ch5-q10-setup", "narrator",
     "Two hundred sparkle-stones. The Elder wants exactly twenty-five groups. The group size is unknown."),

    # Q10 question
    ("ch5-q10-question", "blaze",
     "Two hundred divided by question mark equals twenty-five. What is the group size?"),

    # Q10 answer
    ("ch5-q10-answer", "blaze",
     "Two hundred divided by twenty-five equals eight. "
     "Working backwards — if you want twenty-five groups from two hundred, each group must be eight."),

    # Cliffhanger
    ("ch5-cliffhanger", "narrator",
     "At the edge of the clearing, half-hidden in the shadows — something enormous watched. "
     "Its vine bundles were arranged in the same grouping patterns as the festival lanterns. "
     "Six per bundle. Ten per bundle. It had been watching the whole time. "
     "It wasn't threatening. It was learning."),

    # ── FEEDBACK ──────────────────────────────────────────────────────
    ("feedback-correct-1", "blaze",
     "That's it! The festival can begin."),
    ("feedback-correct-2", "blaze",
     "Correct! Grouped perfectly."),
    ("feedback-correct-3", "blaze",
     "Nice work. Right every time."),
    ("feedback-correct-4", "elder",
     "Impressive. You understand grouping."),
    ("feedback-correct-5", "ripple",
     "Yes yes yes! That's exactly right!"),
    ("feedback-correct-6", "blaze",
     "Exactly right."),
    ("feedback-wrong-1", "blaze",
     "Not quite. Think about how many groups fit."),
    ("feedback-wrong-2", "blaze",
     "That's not it. Try again."),
    ("win", "narrator",
     "The festival of Cascade Clearing is saved — every lantern grouped, every stone arranged. "
     "And Tangle was watching the whole time, learning. "
     "Join us for Issue Four — the Array Forest, where Blaze finally reaches out her hand."),
]

def generate(filename, character, text):
    out_path = os.path.join(OUT_DIR, f"{filename}.mp3")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"  ⏭  {filename}")
        return True
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
        print(f"  ⏳ Rate limited — waiting 15s...")
        time.sleep(15)
        return generate(filename, character, text)
    else:
        print(f"  ❌ {filename}: {r.status_code} {r.text[:120]}")
        return False

print(f"Generating {len(SEGMENTS)} segments\n")
for i, (filename, character, text) in enumerate(SEGMENTS, 1):
    print(f"[{i}/{len(SEGMENTS)}] {character}: {filename}")
    generate(filename, character, text)
    time.sleep(0.3)
print(f"\n✅ Done.")
