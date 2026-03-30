#!/usr/bin/env python3
"""Jungle Issue 7 audio — The Great Sharing. Scripts verbatim from HTML."""
import requests, os, time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue007")
os.makedirs(OUT_DIR, exist_ok=True)

VOICES = {
    "narrator": ("cjVigY5qzO86Huf0OWal", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),
    "blaze":    ("cgSgspJ2msm6clMCkdW9", {"stability": 0.55, "similarity_boost": 0.75, "style": 0.30}),
    "pip":      ("pqHfZKP75CvOlQylNhV4", {"stability": 0.70, "similarity_boost": 0.70, "style": 0.15}),
    "tangle":   ("N2lVS1w4EtoT3dr4eOWO", {"stability": 0.85, "similarity_boost": 0.30, "style": 0.55}),
}

SEGMENTS = [
    # CH1 — Para 1: Tangle led them home, all villages together
    ("ch1-intro", "narrator",
     "Tangle had led them all home. Every missing Sprocket, from the Deep Root, from the narrow paths, "
     "from the far side of Split Ridge. Vine by vine, patient as it had always been, "
     "it had rebuilt every bridge it had taken down. "
     "And now, for the first time in centuries, all five villages stood together in a single clearing."),
    # CH1 — Para 2: 120 Sprockets, Chief Pip, Tangle at back
    ("ch1-gathering", "narrator",
     "One hundred and twenty Sprockets. Five villages: Branchwick, Fernmoss, the Cascade Clearing, "
     "the Array Forest settlement, and Split Ridge. "
     "Chief Pip stood at the front, antenna vibrating with emotion. "
     "Tangle stood at the back, enormous, still, watching."),
    # CH1 — Para 3: the food store
    ("ch1-food", "narrator",
     "The first order of business: the food store. "
     "Three hundred and sixty items, to be shared equally among all one hundred and twenty Sprockets."),
    ("ch1-q1-question", "blaze", "Three hundred and sixty food items shared equally between one hundred and twenty Sprockets. How many items per Sprocket?"),
    ("ch1-q1-answer", "blaze", "Three hundred and sixty divided by one hundred and twenty equals three. Three items each. The Great Share begins."),

    # CH2 — Para 1: fair vs equal, proportional sharing
    ("ch2-intro", "narrator",
     "Three items each was the starting point. But Chief Pip had a harder question. "
     "Each village had a different number of Sprockets. "
     "If the food was truly fair, each village should receive an amount proportional to its size, "
     "not just an equal number."),
    # CH2 — Para 2: Fernmoss 1/5, Split Ridge 1/4
    ("ch2-shares", "narrator",
     "Fernmoss had twenty-four Sprockets, one fifth of the total population. "
     "So Fernmoss should receive one fifth of the food. "
     "Split Ridge had thirty Sprockets, one quarter of the total. And so on."),
    # CH2 — Para 3: Chief Pip speaks
    ("ch2-pip", "pip",
     "Not the same for everyone. The right amount for everyone."),
    ("ch2-q2-question", "blaze", "Fernmoss has twenty-four of one hundred and twenty Sprockets, that's one fifth of the total. What is one fifth of three hundred and sixty?"),
    ("ch2-q2-answer", "blaze", "Three hundred and sixty divided by five equals seventy-two. Fernmoss gets seventy-two items."),
    # Q3 setup
    ("ch2-q3-setup", "narrator",
     "Split Ridge: thirty of one hundred and twenty Sprockets, one quarter of the total population. "
     "One quarter of three hundred and sixty items."),
    ("ch2-q3-question", "blaze", "Split Ridge has one quarter of the total population. What is one quarter of three hundred and sixty?"),
    ("ch2-q3-answer", "blaze", "Three hundred and sixty divided by four equals ninety. Split Ridge gets ninety items."),

    # CH3 — Para 1: Tangle counting bridges, 240 vines exact
    ("ch3-intro", "narrator",
     "While the food was being distributed, Tangle was already working. "
     "It had counted the broken bridges: five in total, each needing forty-eight vines. "
     "Two hundred and forty vines exactly. Tangle had two hundred and forty. "
     "A perfect match. No remainder."),
    # CH3 — Para 2: three per day timeline
    ("ch3-timeline", "narrator",
     "Then came the timeline. The village builders could complete three bridges per day. "
     "Five bridges across two days, three on day one, two on day two. "
     "Not perfectly equal across the days, but the work would be done."),
    # CH3 — Para 3: Blaze speaks
    ("ch3-blaze", "blaze",
     "You've been planning this."),
    ("ch3-q4-question", "blaze", "Five bridges, each needing forty-eight vines. Tangle has two hundred and forty vines. Two hundred and forty divided by forty-eight. How many bridges can be built?"),
    ("ch3-q4-answer", "blaze", "Two hundred and forty divided by forty-eight equals five. A perfect match, exactly enough for all five bridges."),
    # Q5 setup
    ("ch3-q5-setup", "narrator",
     "The builders can complete three bridges per day. There are five bridges to build. "
     "How many full days for the first three, and how many bridges on day two?"),
    ("ch3-q5-question", "blaze", "Five bridges, three per day. How many full days, and how many bridges are left on day two?"),
    ("ch3-q5-answer", "blaze", "Five divided by three is one remainder two. Three bridges on day one, two bridges on day two."),

    # CH4 — Para 1: Dry Season, 504 pods, 7 villages
    ("ch4-intro", "narrator",
     "The Dry Season was coming. Every Sprocket knew it, the weeks when the jungle went silent "
     "and the water pods were all that kept the tribe alive. "
     "Chief Pip pulled out the ledger. "
     "Five hundred and four water pods for seven villages. The distribution had to be perfect."),
    # CH4 — Para 2: each share lasts 4 months, Branchwick 5 families
    ("ch4-calculation", "narrator",
     "Each village's share would need to last four months. "
     "Branchwick had five families who would need to divide their monthly share between them. "
     "At every level, the same question: how many for each?"),
    # CH4 — Para 3: Chief Pip speaks
    ("ch4-pip", "pip",
     "Division keeps us alive. It always has."),
    ("ch4-q6-question", "blaze", "Five hundred and four water pods for seven villages. How many pods per village?"),
    ("ch4-q6-answer", "blaze", "Five hundred and four divided by seven equals seventy-two. Seventy-two pods per village."),
    # Q7 setup
    ("ch4-q7-setup", "narrator", "Each village gets seventy-two pods to last four months. How many pods per month?"),
    ("ch4-q7-question", "blaze", "Seventy-two pods, four months. How many pods per month?"),
    ("ch4-q7-answer", "blaze", "Seventy-two divided by four equals eighteen. Eighteen pods per month."),
    # Q8 setup
    ("ch4-q8-setup", "narrator",
     "Branchwick has five families. Their monthly supply is eighteen pods. "
     "That doesn't divide evenly, so some families get three pods and some get four."),
    ("ch4-q8-question", "blaze", "Branchwick: eighteen pods for five families. How many whole pods per family, and how many are left over?"),
    ("ch4-q8-answer", "blaze", "Eighteen divided by five is three remainder three. Three pods for two families, four pods for three families."),

    # CH5 — Para 1: distribution done, shares verified
    ("ch5-intro", "narrator",
     "When the distribution was done, Chief Pip made a calculation. Blaze helped. "
     "All five village shares added to three hundred and sixty, the total. "
     "Fernmoss seventy-two, Split Ridge ninety, Cascade fifty-four, "
     "Array Forest sixty-three, Branchwick eighty-one. "
     "Every item accounted for. Not equal amounts, but fair ones. Proportional. And the sum was perfect."),
    # CH5 — Para 2: Tangle moves Sprockets row by row
    ("ch5-tangle", "narrator",
     "Then Tangle did something no one expected. It began moving the Sprockets. "
     "Not roughly, precisely. Guiding each one gently to a position, then the next, then the next. "
     "Row by row. When it was finished, four hundred and eighty Sprockets stood in a perfect rectangular array."),
    # CH5 — Para 3: thirty rows of sixteen
    ("ch5-array", "narrator",
     "Thirty rows of sixteen. A multiplication array. "
     "And from above, anyone could see what it was: "
     "the same pattern as Tangle's sculptures, but made of living things. "
     "Tangle had arranged the whole reunion into a piece of mathematics."),
    ("ch5-q9-question", "blaze", "The five village shares were seventy-two, ninety, fifty-four, sixty-three, and eighty-one. Do they add up to three hundred and sixty?"),
    ("ch5-q9-answer", "blaze", "Seventy-two plus ninety plus fifty-four plus sixty-three plus eighty-one equals three hundred and sixty. Every item accounted for. The distribution was perfect."),
    # Q10 setup
    ("ch5-q10-setup", "narrator",
     "Tangle's final array: four hundred and eighty Sprockets, arranged in rows of sixteen."),
    ("ch5-q10-question", "blaze", "Four hundred and eighty Sprockets in rows of sixteen. How many rows?"),
    ("ch5-q10-answer", "blaze",
     "Four hundred and eighty divided by sixteen equals thirty. "
     "Thirty rows. Tangle's greatest array, and it's made of living things."),
    # Finale — replaces cliffhanger for final issue
    ("ch5-finale", "narrator",
     "Chief Pip stood at the front of the array, thirty rows of sixteen, "
     "every Sprocket in the Verdant Canopy standing perfectly still. "
     "Tangle, he said, loud enough for all to hear, "
     "you built us a number line. You counted every vine. You organised us into an array. "
     "You have been doing mathematics your whole life, "
     "and you have done more for this tribe today than any Sprocket alive. "
     "By unanimous decision, you are an Honorary Sprocket. Welcome home. "
     "Tangle set down a bundle of twelve vines. "
     "And for the first time, it wasn't a question. It wasn't confusion. It was a gift."),

    # Feedback
    ("feedback-correct-1", "blaze", "That's it. Three items each. The share begins."),
    ("feedback-correct-2", "blaze", "Correct. Fair means the right amount, not the same amount."),
    ("feedback-correct-3", "blaze", "Nice work. Right on the first try."),
    ("feedback-correct-4", "pip", "The ledger confirms it. Well done."),
    ("feedback-correct-5", "blaze", "Exactly right."),
    ("feedback-correct-6", "blaze", "Perfect."),
    ("feedback-wrong-1", "blaze", "Not quite. Think carefully about how many groups fit."),
    ("feedback-wrong-2", "blaze", "That's not it. Try again."),
    ("win", "narrator",
     "The Verdant Canopy is whole again. Tangle found its place. The Sprockets found their numbers. "
     "And you mastered division. "
     "The jungle runs on equal sharing, and now so do you."),
]

def generate(filename, character, text):
    out_path = os.path.join(OUT_DIR, f"{filename}.mp3")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"  ⏭  {filename}"); return True
    voice_id, settings = VOICES[character]
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={"text": text, "model_id": "eleven_turbo_v2_5", "voice_settings": settings}
    )
    if r.status_code == 200:
        with open(out_path, "wb") as f: f.write(r.content)
        print(f"  ✅ {filename}.mp3 ({len(r.content):,}b)"); return True
    elif r.status_code == 429:
        print(f"  ⏳ Rate limited, waiting 15s..."); time.sleep(15)
        return generate(filename, character, text)
    else:
        print(f"  ❌ {filename}: {r.status_code} {r.text[:100]}"); return False

print(f"Generating {len(SEGMENTS)} segments\n")
for i, (filename, character, text) in enumerate(SEGMENTS, 1):
    print(f"[{i}/{len(SEGMENTS)}] {character}: {filename}")
    generate(filename, character, text)
    time.sleep(0.3)
print("\n✅ Done.")
