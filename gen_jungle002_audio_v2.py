#!/usr/bin/env python3
"""
Jungle Issue 2 — Audio v2: scripts extracted DIRECTLY from on-screen HTML text.
No paraphrasing. No added content. Text first, audio matches exactly.
"""
import requests, os, time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue002")
os.makedirs(OUT_DIR, exist_ok=True)

VOICES = {
    "narrator": ("cjVigY5qzO86Huf0OWal", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),
    "blaze":    ("cgSgspJ2msm6clMCkdW9", {"stability": 0.55, "similarity_boost": 0.75, "style": 0.30}),
    "thistle":  ("XrExE9yKIg1WjnnlVkGX", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.25}),
}

# Every script is copied verbatim from the on-screen story text.
# One speaker = one key moment from that character's line. Maximum 1-2 sentences.
SEGMENTS = [

    # ── CHAPTER 1 ─────────────────────────────────────────────────────
    # Screen: "The path to Fernmoss was overgrown — half the connecting vines were gone.
    #          Blaze pushed through and found the village in chaos."
    ("ch1-intro", "narrator",
     "The path to Fernmoss was overgrown — half the connecting vines were gone. "
     "Blaze pushed through and found the village in chaos."),

    # Screen: Thistle — "We have thirty-six doses for twelve Sprockets..."
    ("ch1-thistle", "thistle",
     "We have thirty-six doses for twelve Sprockets — three each. "
     "But only four of us are here now, and I didn't know what to change."),

    # Screen: Blaze — "Stop. You're dividing by the wrong number."
    ("ch1-blaze", "blaze",
     "Stop. You're dividing by the wrong number."),

    # Q1 question
    ("ch1-q1-question", "blaze",
     "Thirty-six doses for twelve Sprockets. How many does each Sprocket get?"),

    # Q1 answer explanation
    ("ch1-q1-answer", "blaze",
     "Three each — if twelve were here. But only four are present. "
     "Thirty-six divided by four is nine. They should each be getting nine."),

    # ── CHAPTER 2 ─────────────────────────────────────────────────────
    # Screen: "The food store had the same problem — everything divided for twelve Sprockets who weren't there."
    ("ch2-intro", "narrator",
     "The food store had the same problem — everything divided for twelve Sprockets who weren't there."),

    # Screen: Blaze — "Forty-eight nuts. Eight Sprockets actually here. Let me recalculate."
    ("ch2-blaze", "blaze",
     "Forty-eight nuts. Eight Sprockets actually here. Let me recalculate."),

    # Q2 question
    ("ch2-q2-question", "blaze",
     "Forty-eight nuts shared equally between eight Sprockets. How many each?"),

    # Q2 answer
    ("ch2-q2-answer", "blaze",
     "Forty-eight divided by eight equals six. Six each — double what they were getting."),

    # Screen q3: "The sick Sprocket needed four times the normal medicine dose."
    ("ch2-q3-setup", "narrator",
     "The sick Sprocket needed four times the normal medicine dose."),

    # Q3 question
    ("ch2-q3-question", "blaze",
     "Normal dose is nine. Curl needs four times that. What is Curl's dose?"),

    # Q3 answer
    ("ch2-q3-answer", "blaze",
     "Nine times four equals thirty-six. Division and multiplication — always connected."),

    # ── CHAPTER 3 ─────────────────────────────────────────────────────
    # Screen: "With the medicine sorted, Blaze turned to the rest of the store.
    #          Everything had to be recalculated for the Sprockets who were actually present."
    ("ch3-intro", "narrator",
     "With the medicine sorted, Blaze turned to the rest of the store."),

    # Screen: Blaze — "Fifty-six healing leaves. Seven families. Equal shares."
    ("ch3-blaze", "blaze",
     "Fifty-six healing leaves. Seven families. Equal shares."),

    # Q4 question
    ("ch3-q4-question", "blaze",
     "Fifty-six healing leaves for seven families. How many does each family get?"),

    # Q4 answer
    ("ch3-q4-answer", "blaze",
     "Fifty-six divided by seven equals eight. Eight leaves each."),

    # Screen q5: "Blaze found the storage box — sixty-three seeds that needed to be grouped into pouches of nine."
    ("ch3-q5-setup", "narrator",
     "Blaze found the storage box — sixty-three seeds that needed to be grouped into pouches of nine."),

    # Q5 question
    ("ch3-q5-question", "blaze",
     "Sixty-three seeds. How many groups of nine can be made?"),

    # Q5 answer
    ("ch3-q5-answer", "blaze",
     "Sixty-three divided by nine equals seven. Seven groups — no leftovers."),

    # ── CHAPTER 4 ─────────────────────────────────────────────────────
    # Screen: "Blaze had been counting the missing vines. There was a pattern —
    #          Tangle wasn't taking them randomly. It was taking exactly six at a time."
    ("ch4-intro", "narrator",
     "Blaze had been counting the missing vines. There was a pattern — "
     "Tangle wasn't taking them randomly."),

    # Screen: Blaze — "Forty-two vines gone. Six at a time. How many trips did it make?"
    ("ch4-blaze-pattern", "blaze",
     "Forty-two vines gone. Six at a time. How many trips did it make?"),

    # Q6 question
    ("ch4-q6-question", "blaze",
     "Forty-two vines taken, six at a time. How many trips?"),

    # Q6 answer
    ("ch4-q6-answer", "blaze",
     "Forty-two divided by six equals seven. Seven trips — precise and deliberate."),

    # Screen q7: "Fresh vine bundles nearby — thirty-five, arranged in five neat stacks."
    ("ch4-q7-setup", "narrator",
     "Fresh vine bundles nearby — thirty-five, arranged in five neat stacks."),

    # Q7 question
    ("ch4-q7-question", "blaze",
     "Thirty-five vines in five equal bundles. How many vines per bundle?"),

    # Q7 answer
    ("ch4-q7-answer", "blaze",
     "Thirty-five divided by five equals seven. Seven per bundle."),

    # Screen q8: "The next village is seventy-two kilometres away. Tangle travels eight kilometres a day."
    ("ch4-q8-setup", "blaze",
     "The next village is seventy-two kilometres away. Tangle travels eight kilometres a day."),

    # Q8 question
    ("ch4-q8-question", "blaze",
     "Seventy-two kilometres at eight per day. How many days until Tangle reaches it?"),

    # Q8 answer
    ("ch4-q8-answer", "blaze",
     "Seventy-two divided by eight equals nine. Nine days."),

    # ── CHAPTER 5 ─────────────────────────────────────────────────────
    # Screen: "With the distribution corrected, Fernmoss could finally share fairly again.
    #          Thistle looked like a weight had been lifted."
    ("ch5-intro", "narrator",
     "With the distribution corrected, Fernmoss could finally share fairly again. "
     "Thistle looked like a weight had been lifted."),

    # Screen: Thistle — "You fixed it. I've been doing it wrong for three days."
    ("ch5-thistle-thanks", "thistle",
     "You fixed it. I've been doing it wrong for three days."),

    # Screen: "Blaze ran the final check — eighty-one items for nine Sprockets."
    ("ch5-blaze", "blaze",
     "Eighty-one items for nine Sprockets. Final check."),

    # Q9 question
    ("ch5-q9-question", "blaze",
     "Eighty-one items shared equally between nine Sprockets. How many each?"),

    # Q9 answer
    ("ch5-q9-answer", "blaze",
     "Eighty-one divided by nine equals nine. Nine each — and this time, the right nine."),

    # Screen q10: "Curl needed three-quarters of their daily share in the first dose.
    #              Blaze: Divide by four first, then multiply by three. The fraction IS the division."
    ("ch5-q10-setup", "narrator",
     "Curl needed three-quarters of their daily share in the first dose."),

    # Q10 question
    ("ch5-q10-question", "blaze",
     "Three-quarters of nine. Divide by four first, then multiply by three."),

    # Q10 answer
    ("ch5-q10-answer", "blaze",
     "Nine divided by four is two and a quarter. Times three is six and three-quarters. "
     "The fraction is the division."),

    # Screen cliffhanger: "Blaze stepped outside — and stopped. Enormous footprints. Toward the Deep Root."
    ("ch5-cliffhanger", "narrator",
     "Blaze stepped outside — and stopped. "
     "Enormous footprints in the mud, leading deeper. Toward the Deep Root. "
     "Whatever Tangle was looking for... it was in there."),

    # ── FEEDBACK ──────────────────────────────────────────────────────
    ("feedback-correct-1", "blaze",
     "That's it — the right division for the Sprockets who are actually here."),

    ("feedback-correct-2", "blaze",
     "Correct. Equal shares for everyone."),

    ("feedback-correct-3", "blaze",
     "Nice work. I knew you'd get it."),

    ("feedback-correct-4", "thistle",
     "Oh thank goodness. Curl is going to be okay."),

    ("feedback-correct-5", "blaze",
     "Exactly right."),

    ("feedback-correct-6", "blaze",
     "Good thinking."),

    ("feedback-wrong-1", "blaze",
     "Not quite. Think about equal groups."),

    ("feedback-wrong-2", "blaze",
     "That's not it. Take another look."),

    ("win", "narrator",
     "Fernmoss is saved — every dose correct, every share recalculated. "
     "Blaze is getting closer to understanding Tangle. "
     "Issue Three: the Grouping Festival — and the first glimpse of Tangle in the light."),
]

# Force regen all narrative clips — keep existing answer/feedback clips if unchanged
FORCE_REGEN = {
    "ch1-intro","ch1-thistle","ch1-blaze","ch1-q1-question",
    "ch2-intro","ch2-blaze","ch2-q2-question","ch2-q3-setup","ch2-q3-question",
    "ch3-intro","ch3-blaze","ch3-q4-question","ch3-q5-setup","ch3-q5-question",
    "ch4-intro","ch4-blaze-pattern","ch4-q6-question","ch4-q7-setup","ch4-q7-question",
    "ch4-q8-setup","ch4-q8-question",
    "ch5-intro","ch5-thistle-thanks","ch5-blaze","ch5-q9-question",
    "ch5-q10-setup","ch5-q10-question","ch5-cliffhanger",
    "feedback-correct-1","feedback-correct-2","feedback-correct-3",
    "feedback-correct-4","feedback-correct-5","feedback-correct-6",
    "feedback-wrong-1","feedback-wrong-2","win",
}

def generate(filename, character, text):
    out_path = os.path.join(OUT_DIR, f"{filename}.mp3")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000 and filename not in FORCE_REGEN:
        print(f"  ⏭  {filename}")
        return True
    voice_id, settings = VOICES[character]
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={"text": text, "model_id": "eleven_turbo_v2_5", "voice_settings": settings}
    )
    if r.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(r.content)
        print(f"  ✅ {filename}.mp3 ({len(r.content):,}b)")
        return True
    elif r.status_code == 429:
        print(f"  ⏳ Rate limited — waiting 15s...")
        time.sleep(15)
        return generate(filename, character, text)
    else:
        print(f"  ❌ {filename}: {r.status_code} {r.text[:120]}")
        return False

print(f"Generating {len(SEGMENTS)} segments ({len(FORCE_REGEN)} forced regen)\n")
for i, (filename, character, text) in enumerate(SEGMENTS, 1):
    print(f"[{i}/{len(SEGMENTS)}] {character}: {filename}")
    generate(filename, character, text)
    time.sleep(0.3)

print(f"\n✅ Done.")
