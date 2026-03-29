#!/usr/bin/env python3
"""
Jungle Issue 2 — Audio gen: tight scripts matching on-screen text exactly.
Cast: Eric (narrator), Jessica (Blaze), XrExE9yKIg1WjnnlVkGX (Thistle — new)
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

SEGMENTS = [

    # ── CHAPTER 1 — Dividing in the Dark ─────────────────────────────
    ("ch1-intro", "narrator",
     "The path to Fernmoss was overgrown — half the connecting vines were gone. "
     "Blaze pushed through and found the village in chaos."),

    ("ch1-thistle", "thistle",
     "We have thirty-six doses for twelve Sprockets — three each. That's what the record says. "
     "But only four of us are here now, and I didn't know what to change."),

    ("ch1-blaze", "blaze",
     "Stop. You're dividing by the wrong number. Only four of you are here."),

    ("ch1-q1-question", "blaze",
     "First — thirty-six doses between twelve Sprockets. How many each?"),

    ("ch1-q1-answer", "blaze",
     "Three each — if twelve were here. But only four are present. "
     "Thirty-six divided by four is nine. They should be getting nine doses each."),

    # ── CHAPTER 2 — Wrong Numbers, Wrong Shares ───────────────────────
    ("ch2-intro", "narrator",
     "The food store had the same problem — everything divided for twelve Sprockets who weren't there."),

    ("ch2-blaze", "blaze",
     "Forty-eight nuts. Eight Sprockets actually here. Let me recalculate."),

    ("ch2-q2-question", "blaze",
     "Forty-eight nuts for eight Sprockets. How many each?"),

    ("ch2-q2-answer", "blaze",
     "Forty-eight divided by eight equals six. Six each — double what they were getting."),

    ("ch2-q3-setup", "narrator",
     "The sick Sprocket, Curl, needed four times the normal dose of medicine."),

    ("ch2-q3-question", "blaze",
     "Normal dose is nine. Curl needs four times that. Nine times four equals what?"),

    ("ch2-q3-answer", "blaze",
     "Nine times four equals thirty-six. Division and multiplication — two sides of the same thing."),

    # ── CHAPTER 3 — Counting What's Left ─────────────────────────────
    ("ch3-intro", "narrator",
     "With the medicine sorted, Blaze turned to the rest of the store."),

    ("ch3-blaze", "blaze",
     "Fifty-six healing leaves. Seven families. Equal shares."),

    ("ch3-q4-question", "blaze",
     "Fifty-six leaves for seven families. How many does each family get?"),

    ("ch3-q4-answer", "blaze",
     "Fifty-six divided by seven equals eight. Eight leaves each."),

    ("ch3-q5-setup", "narrator",
     "Then Blaze found the storage box — sixty-three seeds, neatly stacked."),

    ("ch3-q5-question", "blaze",
     "Sixty-three seeds. How many groups of nine can be made?"),

    ("ch3-q5-answer", "blaze",
     "Sixty-three divided by nine equals seven. Seven groups — no leftovers."),

    # ── CHAPTER 4 — Tangle's Pattern ─────────────────────────────────
    ("ch4-intro", "narrator",
     "Blaze had been counting the missing vines. There was a pattern."),

    ("ch4-blaze-pattern", "blaze",
     "Forty-two vines gone. Six at a time. How many trips did it make?"),

    ("ch4-q6-question", "blaze",
     "Forty-two vines, six taken each trip. How many trips?"),

    ("ch4-q6-answer", "blaze",
     "Forty-two divided by six equals seven. Seven trips — precise and deliberate."),

    ("ch4-q7-setup", "narrator",
     "Fresh vine bundles nearby — thirty-five, arranged in five neat stacks."),

    ("ch4-q7-question", "blaze",
     "Thirty-five vines in five bundles. How many per bundle?"),

    ("ch4-q7-answer", "blaze",
     "Seven per bundle. Always the same. Tangle is very consistent."),

    ("ch4-q8-setup", "blaze",
     "The next village is seventy-two kilometres away. Tangle travels eight kilometres a day."),

    ("ch4-q8-question", "blaze",
     "Seventy-two kilometres at eight per day. How many days until Tangle reaches the next village?"),

    ("ch4-q8-answer", "blaze",
     "Seventy-two divided by eight equals nine. Nine days. We need to move faster than that."),

    # ── CHAPTER 5 — Fixed ─────────────────────────────────────────────
    ("ch5-intro", "narrator",
     "With the distribution corrected, Fernmoss could finally share fairly again."),

    ("ch5-blaze", "blaze",
     "Eighty-one items for nine Sprockets. Final check."),

    ("ch5-q9-question", "blaze",
     "Eighty-one items for nine Sprockets. How many each?"),

    ("ch5-q9-answer", "blaze",
     "Eighty-one divided by nine equals nine. Nine each — and this time, the right nine."),

    ("ch5-q10-setup", "narrator",
     "Curl had one more question. The sick Sprocket needed three-quarters of their share in the first dose."),

    ("ch5-q10-question", "blaze",
     "Three-quarters of nine. Boss challenge — divide by four, then multiply by three."),

    ("ch5-q10-answer", "blaze",
     "Nine divided by four is two and a quarter. Times three is six and three-quarters. "
     "The fraction IS the division."),

    ("ch5-cliffhanger", "narrator",
     "Outside, pressed deep into the mud — enormous footprints. "
     "Leading deeper into the jungle. Toward the Deep Root. "
     "Whatever Tangle was looking for... it was in there."),

    # ── THISTLE GOODBYE ───────────────────────────────────────────────
    ("ch5-thistle-thanks", "thistle",
     "You fixed it. I've been doing it wrong for three days. "
     "I didn't know what to do when the numbers changed."),

    # ── FEEDBACK ──────────────────────────────────────────────────────
    ("feedback-correct-1", "blaze",
     "That's it! Divided correctly — Fernmoss can finally share fairly."),

    ("feedback-correct-2", "blaze",
     "Correct! Equal shares for everyone."),

    ("feedback-correct-3", "blaze",
     "Nice work. I knew you'd get it."),

    ("feedback-correct-4", "thistle",
     "Oh thank goodness! That's the right answer — Curl is going to be okay!"),

    ("feedback-correct-5", "blaze",
     "There it is. Exactly right."),

    ("feedback-correct-6", "blaze",
     "Good thinking. Division and multiplication — always connected."),

    ("feedback-wrong-1", "blaze",
     "Not quite — try again. Think about equal groups."),

    ("feedback-wrong-2", "blaze",
     "Hmm. That's not it. Take another look."),

    ("win", "narrator",
     "Fernmoss is saved — every dose correct, every share recalculated. "
     "Blaze is getting closer to understanding Tangle. "
     "Issue Three: the Grouping Festival — and the first glimpse of Tangle in the light."),
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

print(f"Generating {len(SEGMENTS)} segments to {OUT_DIR}\n")
for i, (filename, character, text) in enumerate(SEGMENTS, 1):
    print(f"[{i}/{len(SEGMENTS)}] {character}: {filename}")
    generate(filename, character, text)
    time.sleep(0.3)

print(f"\n✅ Done.")
