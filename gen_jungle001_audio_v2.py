#!/usr/bin/env python3
"""
Jungle Issue 1 — Audio v2: TIGHT scripts matching on-screen text exactly.
Each segment is 1-3 short sentences max. No extra narration.
unlockAtIndex wired: quiz unlocks when question clip STARTS.
"""
import requests, os, time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue001")
os.makedirs(OUT_DIR, exist_ok=True)

VOICES = {
    "narrator": ("cjVigY5qzO86Huf0OWal", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),
    "blaze":    ("cgSgspJ2msm6clMCkdW9", {"stability": 0.55, "similarity_boost": 0.75, "style": 0.30}),
    "pip":      ("pqHfZKP75CvOlQylNhV4", {"stability": 0.65, "similarity_boost": 0.70, "style": 0.25}),
    "doz":      ("IKne3meq5aSn9XLyUdCD", {"stability": 0.45, "similarity_boost": 0.70, "style": 0.50}),
}

# All segments match on-screen text exactly — short and tight.
SEGMENTS = [

    # ── CHAPTER 1 ─────────────────────────────────────────────────────
    # On screen: "Deep in the Verdant Canopy... Everything must be shared equally."
    ("ch1-intro", "narrator",
     "Deep in the Verdant Canopy — a vast jungle where ancient trees touched the clouds — "
     "lived the Sprockets: small, clever creatures whose whole civilisation ran on one rule. "
     "Everything must be shared equally."),

    # On screen: Blaze dialogue — "Okay. That was not how I planned to land..."
    ("ch1-blaze-arrival", "blaze",
     "Okay. That was not how I planned to land. Give me five seconds. "
     "Treetop village, small blue creatures staring, and I appear to have landed in someone's berry basket. "
     "I've already calculated that this is going to be an interesting day."),

    # On screen: Pip dialogue — "Welcome, explorer!..."
    ("ch1-pip-welcome", "pip",
     "Welcome, explorer! I am Chief Pip of Branchwick. "
     "Tonight we share the harvest — as we have for ten thousand years. "
     "But our berry counter, Doz, has wandered off again. "
     "We cannot begin until the harvest is divided correctly. It is the Sprocket law."),

    # Q1 question — unlocks quiz
    ("ch1-q1-question", "blaze",
     "Chief Pip has twelve welcome-berries to share equally between three visitors. "
     "How many berries does each visitor get?"),

    # ── CHAPTER 2 ─────────────────────────────────────────────────────
    # On screen: "Blaze followed Chief Pip to the harvest platform..."
    ("ch2-intro", "narrator",
     "Blaze followed Chief Pip to the harvest platform — "
     "a wide surface woven from branches high in the tallest tree. "
     "Two enormous baskets sat waiting."),

    # On screen: Pip dialogue — "Four Sprocket families..."
    ("ch2-pip-harvest", "pip",
     "Four Sprocket families. Each must receive exactly the same amount — "
     "not one berry more, not one less. It is the Sprocket way."),

    # On screen: Blaze dialogue — "Got it... Twenty-four glow-berries."
    ("ch2-blaze-inspect", "blaze",
     "Got it. Twenty-four glow-berries. Four families. Let me work this out."),

    # Q2 question — unlocks quiz
    ("ch2-q2-question", "blaze",
     "Twenty-four glow-berries, shared equally between four families. "
     "How many berries does each family get?"),

    # Q2 answer → then q3 story plays
    ("ch2-q2-answer", "blaze",
     "Twenty-four divided by four equals six. Six berries per family. "
     "You can check it both ways — four times six is twenty-four."),

    # Q3 story (on screen: "Chief Pip pointed to the second basket — moon-figs.")
    ("ch2-q3-setup", "narrator",
     "Chief Pip pointed to the second basket — filled with pale, glowing moon-figs."),

    # Q3 question — unlocks quiz
    ("ch2-q3-question", "blaze",
     "Eighteen moon-figs. Six families this time. "
     "How many does each family get? And what multiplication fact proves your answer?"),

    # Q3 answer
    ("ch2-q3-answer", "blaze",
     "Eighteen divided by six equals three. And six times three equals eighteen — that's the fact family."),

    # ── CHAPTER 3 ─────────────────────────────────────────────────────
    # On screen: "Blaze went looking for Doz. She found the berry counter..."
    ("ch3-intro", "narrator",
     "Blaze went looking for Doz. She found the berry counter in the very next tree — "
     "perched on a branch, staring at something extraordinary."),

    # On screen: Doz dialogue
    ("ch3-doz-discovery", "doz",
     "Oh! Oh oh oh — the vines! Did you see the vines?! "
     "They're all tangled up and I couldn't count the berries because I kept losing my place and — "
     "wait, who are you?!"),

    # On screen: Blaze dialogue — "The vines. And yes..."
    ("ch3-blaze-doz", "blaze",
     "The vines. And yes — I can see them. That is a very large tangle. "
     "But first — the Sprocket medic needs help."),

    # Q4 question — unlocks quiz
    ("ch3-q4-question", "blaze",
     "The village medic has twenty healing leaves. "
     "She wants to put them into pouches of five. How many pouches can she make?"),

    # Q4 answer
    ("ch3-q4-answer", "blaze",
     "Twenty divided by five equals four. Four pouches. "
     "This is grouping — how many groups of five fit into twenty?"),

    # Q5 story (on screen: "Fernleaf wasn't finished...")
    ("ch3-q5-setup", "narrator",
     "Fernleaf wasn't finished. She tipped a second pile of leaves onto the bench."),

    # Q5 question — unlocks quiz
    ("ch3-q5-question", "blaze",
     "Fifteen leaves this time, in groups of three. "
     "How many groups? And write the whole fact family — all four number sentences."),

    # Q5 answer
    ("ch3-q5-answer", "blaze",
     "Fifteen divided by three equals five groups. "
     "Fact family: three times five, five times three, fifteen divided by three, fifteen divided by five."),

    # ── CHAPTER 4 ─────────────────────────────────────────────────────
    # On screen: "The feast preparations were almost complete..."
    ("ch4-intro", "narrator",
     "The feast preparations were almost complete. Smoke rose from the cooking platform. "
     "The whole village of Branchwick gathered. "
     "But the cook, Burble, was stuck — the final ingredients weren't divided yet."),

    # On screen: Blaze dialogue
    ("ch4-blaze-steps-up", "blaze",
     "Right. I've got this. What do you need divided?"),

    # On screen: Pip dialogue — "The fire-nuts..."
    ("ch4-pip-explains", "pip",
     "The fire-nuts — thirty-six, for nine Sprockets at the main table. "
     "The bark-bread — thirty-two pieces, for eight Sprockets at the elder table. "
     "And — what if there had been five families instead of four tonight? "
     "How many glow-berries each, from the original twenty-four?"),

    # Q6 question — unlocks quiz
    ("ch4-q6-question", "blaze",
     "Thirty-six fire-nuts for nine Sprockets. How many fire-nuts each?"),

    # Q6 answer
    ("ch4-q6-answer", "blaze",
     "Thirty-six divided by nine equals four. Four fire-nuts each."),

    # Q7 story (on screen: "Blaze moved to the elder's table...")
    ("ch4-q7-setup", "narrator",
     "Blaze moved to the elder's table. The cook Burble slid a basket of bark-bread toward her."),

    # Q7 question — unlocks quiz
    ("ch4-q7-question", "blaze",
     "Thirty-two pieces of bark-bread for eight Sprockets. "
     "How many pieces each? And notice anything interesting about the answer?"),

    # Q7 answer
    ("ch4-q7-answer", "blaze",
     "Thirty-two divided by eight equals four. Same answer as the fire-nuts — different numbers, same result. That's a pattern."),

    # Q8 story (on screen: "Chief Pip stroked his antennae thoughtfully...")
    ("ch4-q8-setup", "pip",
     "One more question, explorer. What if there had been five families tonight instead of four? "
     "Twenty-four glow-berries between five families — how many each?"),

    # Q8 question — unlocks quiz
    ("ch4-q8-question", "blaze",
     "Twenty-four glow-berries between five families. Heads up — this one doesn't divide evenly."),

    # Q8 answer
    ("ch4-q8-answer", "blaze",
     "Twenty-four divided by five is four remainder four. "
     "In Branchwick, the leftovers go to the medic. Every remainder has a home."),

    # ── CHAPTER 5 ─────────────────────────────────────────────────────
    # On screen: "The feast was everything... But Blaze couldn't stop thinking about those vines."
    ("ch5-intro", "narrator",
     "The feast was everything Chief Pip had promised. "
     "Every Sprocket family received exactly their equal share. "
     "But Blaze couldn't stop thinking about those vines."),

    # On screen: Blaze dialogue — "Seven bundles..."
    ("ch5-blaze-investigates", "blaze",
     "Seven bundles. Someone — or something — arranged these. "
     "Twenty-eight vines, grouped into seven neat bundles. That's not random. That's intentional."),

    # Q9 question — unlocks quiz
    ("ch5-q9-question", "blaze",
     "Twenty-eight vines arranged in seven equal bundles. How many vines in each bundle?"),

    # Q9 answer
    ("ch5-q9-answer", "blaze",
     "Twenty-eight divided by seven equals four. Four vines per bundle. Whatever made these really likes groups of four."),

    # On screen: "And then she looked down. In the soft mud — an enormous footprint."
    ("ch5-footprint", "narrator",
     "And then she looked down. In the soft mud — an enormous footprint. "
     "Bigger than Blaze's whole body. "
     "Whatever had been standing here was very, very large. And it had been watching the village."),

    # Q10 story (on screen: "Chief Pip appeared at Blaze's shoulder...")
    ("ch5-q10-setup", "pip",
     "One more, explorer — I am planning tomorrow's meal. "
     "The village has forty-five food items for six families. What does each family get?"),

    # Q10 question — unlocks quiz
    ("ch5-q10-question", "blaze",
     "Forty-five food items for six families. There's a remainder — and remember, in Branchwick, remainders always go somewhere useful."),

    # Q10 answer
    ("ch5-q10-answer", "blaze",
     "Forty-five divided by six is seven remainder three. "
     "Seven items each — and the three extras go to Fernleaf as emergency rations."),

    # Cliffhanger
    ("ch5-cliffhanger", "narrator",
     "That night, as Branchwick slept, more vines went missing from the path to Fernmoss. "
     "A Sprocket family who had gone to visit the neighbouring village... hadn't come back. "
     "And deep in the jungle, something enormous moved silently through the trees — "
     "gathering vines, bundle by bundle, four at a time. "
     "The mystery of the Verdant Canopy had only just begun."),

    # ── FEEDBACK ──────────────────────────────────────────────────────
    ("feedback-correct-1", "blaze",
     "That's it! Divided perfectly — the Sprocket way."),

    ("feedback-correct-2", "blaze",
     "Correct! Equal shares for everyone."),

    ("feedback-correct-3", "blaze",
     "Nice work. I knew you'd get it."),

    ("feedback-correct-4", "pip",
     "Perfectly divided! You honour the Sprocket tradition, explorer."),

    ("feedback-correct-5", "doz",
     "Yes yes yes!! That's right! Can we celebrate?!"),

    ("feedback-correct-6", "blaze",
     "There it is. Exactly right."),

    ("feedback-wrong-1", "blaze",
     "Not quite — try again. Think about equal groups."),

    ("feedback-wrong-2", "blaze",
     "Hmm. That's not it. Take another look."),

    ("win", "narrator",
     "The feast of Branchwick was saved — every share equal, every remainder accounted for. "
     "And somewhere in the jungle, a mystery was waiting. Issue Two: Dividing in the Dark."),
]

FORCE_REGEN = {
    # These are new or need to match the tightened scripts — regenerate even if file exists
    "ch1-intro", "ch1-blaze-arrival", "ch1-pip-welcome", "ch1-q1-question",
    "ch2-intro", "ch2-pip-harvest", "ch2-blaze-inspect", "ch2-q2-question",
    "ch2-q3-setup", "ch2-q3-question",
    "ch3-intro", "ch3-doz-discovery", "ch3-blaze-doz", "ch3-q4-question",
    "ch3-q5-setup", "ch3-q5-question",
    "ch4-intro", "ch4-blaze-steps-up", "ch4-pip-explains", "ch4-q6-question",
    "ch4-q7-setup", "ch4-q7-question",
    "ch4-q8-setup", "ch4-q8-question",
    "ch5-intro", "ch5-blaze-investigates", "ch5-q9-question",
    "ch5-footprint", "ch5-q10-setup", "ch5-q10-question",
    "ch5-cliffhanger",
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

print(f"Generating {len(SEGMENTS)} segments (forcing {len(FORCE_REGEN)} regen)\n")
for i, (filename, character, text) in enumerate(SEGMENTS, 1):
    print(f"[{i}/{len(SEGMENTS)}] {character}: {filename}")
    generate(filename, character, text)
    time.sleep(0.3)

print(f"\n✅ Done.")
