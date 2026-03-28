#!/usr/bin/env python3
"""
Generate all narration audio for Jungle Issue 1 — "Welcome to the Canopy"
Cast: Eric (narrator), Jessica (Blaze), Bill (Chief Pip), Charlie (Doz)
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

# (filename, character, text)
SEGMENTS = [

    # ── CHAPTER 1 — Crash into the Canopy ────────────────────────────
    ("ch1-intro", "narrator",
     "Deep in the Verdant Canopy, where ancient trees grew so tall their tops scraped the clouds, "
     "there lived a tribe of small, clever creatures called the Sprockets. "
     "Their whole civilisation ran on one rule: everything must be shared equally. "
     "Every berry, every leaf, every drop of dew — divided perfectly, every single day. "
     "And on one perfectly ordinary morning — a girl named Blaze came crashing through the canopy."),

    ("ch1-blaze-arrival", "blaze",
     "Okay. That was not how I planned to land. "
     "Give me five seconds. "
     "Right — I'm in a treetop village, there are small blue creatures staring at me, "
     "and I appear to have landed in someone's berry basket. "
     "I've already calculated that this is going to be an interesting day."),

    ("ch1-pip-welcome", "pip",
     "Welcome, explorer! I am Chief Pip of Branchwick. "
     "We do not often receive visitors who fall from the sky. "
     "But you are here, and the Sprocket way is to share. "
     "Tonight we prepare the evening feast — but our berry counter, Doz, has wandered off again. "
     "We cannot begin until the harvest is divided correctly. "
     "It is the Sprocket law."),

    ("ch1-blaze-response", "blaze",
     "Dividing the harvest. Got it. I can do that. "
     "Show me what you've got."),

    ("ch1-q1-setup", "narrator",
     "Chief Pip pointed to a small wooden bowl. "
     "Inside were twelve bright red welcome-berries — the ones given to every visitor as a greeting gift. "
     "Three visitors had arrived the week before, and each one needed to receive exactly the same number."),

    ("ch1-q1-question", "blaze",
     "Twelve welcome-berries. Three visitors. Each one gets the same amount. "
     "How many berries does each visitor get? "
     "Think about it — if you shared twelve between three people equally, what would each person receive?"),

    ("ch1-q1-answer", "blaze",
     "Twelve divided by three equals four. "
     "Each visitor gets four welcome-berries. "
     "Chief Pip nodded — that is correct. The greeting ritual could begin."),

    # ── CHAPTER 2 — The Berry Harvest ────────────────────────────────
    ("ch2-intro", "narrator",
     "Blaze followed Chief Pip to the harvest platform — a wide, flat surface woven from branches "
     "high in the tallest tree. "
     "Two enormous baskets sat waiting. Tonight's feast depended on what was inside."),

    ("ch2-blaze-inspect", "blaze",
     "Okay. First basket — glow-berries. I'm counting... twenty-four. "
     "Four Sprocket families. Same amount for each family — that's the rule, right? "
     "Right. Let me work this out."),

    ("ch2-q2-question", "blaze",
     "Twenty-four glow-berries, shared equally between four families. "
     "How many berries does each family get? "
     "Try drawing it out if it helps — four groups, twenty-four berries shared between them."),

    ("ch2-q2-answer", "blaze",
     "Twenty-four divided by four equals six. "
     "Each family gets six glow-berries. "
     "And you can check it the other way — four groups of six is twenty-four. That's the fact family working both ways."),

    ("ch2-q3-setup", "narrator",
     "Chief Pip pointed to the second basket — filled with pale, glowing moon-figs. "
     "Blaze counted carefully."),

    ("ch2-q3-question", "blaze",
     "Eighteen moon-figs. Six families this time. Equal shares again. "
     "How many does each family get? "
     "And when you've got your answer — what multiplication fact proves it's right?"),

    ("ch2-q3-answer", "blaze",
     "Eighteen divided by six equals three. Each family gets three moon-figs. "
     "And the multiplication that proves it? Six times three equals eighteen. "
     "That's the fact family — division and multiplication, two sides of the same thing."),

    # ── CHAPTER 3 — The Missing Doz ──────────────────────────────────
    ("ch3-intro", "narrator",
     "With the main harvest divided, Blaze went looking for Doz. "
     "Chief Pip had said the berry counter wandered off — but nobody seemed worried. "
     "Apparently, this happened a lot. "
     "Blaze found Doz in the very next tree, perched on a branch and staring at something extraordinary."),

    ("ch3-doz-discovery", "doz",
     "Oh! Oh oh oh — you found me! Did you see it though?! The vines!! "
     "They're all tangled up in a huge massive pile and I couldn't get past and I tried counting them "
     "but there are SO many and I kept losing my place and — "
     "wait, who are you? Are you the new explorer? "
     "Chief Pip said an explorer was coming but I didn't think you'd be — "
     "sorry, what were we talking about?"),

    ("ch3-blaze-doz", "blaze",
     "The vines. You were talking about the vines. "
     "And yes — I can see them. That is a very large tangle. "
     "But first — the Sprocket medic needs help. We'll come back to the vines."),

    ("ch3-q4-setup", "narrator",
     "The village medic, a small Sprocket named Fernleaf, had twenty healing leaves to sort into pouches. "
     "Each pouch needed exactly five leaves — not four, not six. Five. "
     "It was a different kind of division — not sharing among people, but grouping into sets."),

    ("ch3-q4-question", "blaze",
     "Twenty healing leaves. Each pouch holds five leaves. "
     "How many pouches can Fernleaf make? "
     "This one's about groups — how many groups of five fit into twenty?"),

    ("ch3-q4-answer", "blaze",
     "Twenty divided by five equals four. Fernleaf can make four pouches. "
     "That's grouping — instead of sharing among people, we're making groups of a set size. "
     "Same division, different question."),

    ("ch3-q5-question", "blaze",
     "Fernleaf has more leaves to sort. Fifteen this time, in groups of three. "
     "How many groups of three can she make from fifteen? "
     "And when you've got your answer, can you write the whole fact family — all four number sentences?"),

    ("ch3-q5-answer", "blaze",
     "Fifteen divided by three equals five — five groups. "
     "The full fact family: three times five equals fifteen. Five times three equals fifteen. "
     "Fifteen divided by three equals five. Fifteen divided by five equals three. "
     "Four facts, two numbers, one family."),

    # ── CHAPTER 4 — The Feast Begins ─────────────────────────────────
    ("ch4-intro", "narrator",
     "The feast preparations were almost complete. Smoke rose from the cooking platform. "
     "The whole village of Branchwick gathered in the great tree hollow — "
     "every Sprocket family, every elder, every child. "
     "But the cook, a round Sprocket named Burble, was stuck. "
     "The final ingredients weren't divided yet, and nothing could be cooked until they were."),

    ("ch4-blaze-steps-up", "blaze",
     "Right. I've got this. What do you need divided?"),

    ("ch4-pip-explains", "pip",
     "The fire-nuts — thirty-six of them, for nine Sprockets at the main table. "
     "The bark-bread — thirty-two pieces, for eight Sprockets at the elder table. "
     "And... Chief Pip would like to know something. A hypothetical. "
     "What if there had been five families instead of four tonight? "
     "How many glow-berries each, from the original twenty-four?"),

    ("ch4-q6-question", "blaze",
     "First things first — thirty-six fire-nuts for nine Sprockets. "
     "Equal shares. How many fire-nuts does each Sprocket get?"),

    ("ch4-q6-answer", "blaze",
     "Thirty-six divided by nine equals four. Four fire-nuts each. "),

    ("ch4-q7-question", "blaze",
     "Thirty-two pieces of bark-bread for eight Sprockets. "
     "How many pieces each? "
     "And when you work it out — notice anything interesting about the answer?"),

    ("ch4-q7-answer", "blaze",
     "Thirty-two divided by eight equals four. Four pieces each. "
     "Same answer as the fire-nuts — even though the numbers were different. "
     "That's a pattern worth remembering. Different divisions can lead to the same result."),

    ("ch4-q8-question", "blaze",
     "Now for Chief Pip's hypothetical. "
     "Twenty-four glow-berries. But imagine there were five families instead of four. "
     "Twenty-four divided by five — what do you get? "
     "Heads up: this one doesn't divide evenly."),

    ("ch4-q8-answer", "blaze",
     "Twenty-four divided by five is four, with four left over. "
     "Four remainder four. "
     "Chief Pip nodded thoughtfully. In Sprocket tradition, the leftover goes to the village medic — "
     "always kept for emergencies. Every remainder has a home."),

    # ── CHAPTER 5 — Tangle's First Footprint ─────────────────────────
    ("ch5-intro", "narrator",
     "The feast was everything Chief Pip had promised. "
     "Glowing berries, warm bark-bread, fire-nuts roasted over the cooking flames. "
     "Every Sprocket family received exactly their equal share — and for the first time in days, "
     "the village was completely full and completely happy. "
     "But Blaze couldn't stop thinking about those vines. "
     "After the feast, while the Sprockets sang their evening songs, she went back to look."),

    ("ch5-blaze-investigates", "blaze",
     "Seven bundles. Someone — or something — arranged these. "
     "Twenty-eight vines in total, grouped into seven neat bundles. "
     "That's not random. That's intentional."),

    ("ch5-q9-question", "blaze",
     "Twenty-eight vines, arranged in seven equal bundles. "
     "How many vines are in each bundle?"),

    ("ch5-q9-answer", "blaze",
     "Twenty-eight divided by seven equals four. Four vines per bundle. "
     "Whatever made these — it likes groups of four. "
     "And then Blaze looked down."),

    ("ch5-footprint", "narrator",
     "In the soft mud at the base of the tree — an enormous footprint. "
     "Bigger than Blaze's whole body. "
     "Five toes, each one pressing deep into the ground. "
     "Whatever left this print was very, very large. "
     "And it had been standing right here, watching the village."),

    ("ch5-q10-question", "blaze",
     "One more for tonight — Chief Pip's planning ahead for tomorrow. "
     "The village has forty-five food items for six families. "
     "Forty-five divided by six — what does each family get, and what happens to the remainder? "
     "Remember: in Branchwick, remainders always go somewhere useful."),

    ("ch5-q10-answer", "blaze",
     "Forty-five divided by six is seven remainder three. "
     "Each family gets seven food items, and the three left over go to Fernleaf the medic — "
     "emergency rations, just in case. "
     "Every remainder has a purpose."),

    ("ch5-cliffhanger", "narrator",
     "That night, as Branchwick slept, more vines went missing from the path to Fernmoss. "
     "A Sprocket family who had gone to visit the neighbouring village... hadn't come back. "
     "And deep in the jungle, something enormous moved silently through the trees — "
     "gathering vines, bundle by bundle, four at a time. "
     "The mystery of the Verdant Canopy had only just begun."),

    # ── WIN / FEEDBACK ─────────────────────────────────────────────────
    ("feedback-correct-1", "blaze",
     "That's it! Divided perfectly — the Sprocket way."),

    ("feedback-correct-2", "blaze",
     "Correct! Equal shares for everyone."),

    ("feedback-correct-3", "blaze",
     "Nice work. I knew you'd get it."),

    ("feedback-correct-4", "pip",
     "Perfectly divided! You honour the Sprocket tradition, explorer."),

    ("feedback-correct-5", "doz",
     "Yes yes yes!! That's right! Can we celebrate?! Can we?!"),

    ("feedback-correct-6", "blaze",
     "There it is. Exactly right."),

    ("feedback-wrong-1", "blaze",
     "Not quite — try again. Think about how many equal groups you need."),

    ("feedback-wrong-2", "blaze",
     "Hmm. That's not it. Take another look — the numbers are there, you just need to put them together."),

    ("win", "narrator",
     "The feast of Branchwick was saved — divided perfectly, every share equal, every remainder accounted for. "
     "Blaze had done it. And somewhere in the jungle, a mystery was waiting. "
     "Issue Two: Dividing in the Dark."),
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
    time.sleep(0.3)  # gentle rate limiting

print(f"\n✅ Done. Check {OUT_DIR}")
