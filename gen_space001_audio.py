#!/usr/bin/env python3
"""
Generate all narration audio for Space Issue 1 — "The Missing Quarter"
Setting: Kepler Station — a refuelling depot orbiting a red dwarf star
Story: Jake arrives to investigate fractional fuel theft by the Fraction Phantom
Cast: George (narrator), Andrew (Jake), River (Priya/Phantom)
"""
import requests, os, time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/issue001")
os.makedirs(OUT_DIR, exist_ok=True)

VOICES = {
    "narrator": ("JBFqnCBsd6RMkjVDRZzb", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),  # George
    "jake":     ("BTEPH6wbWkb66Dys0ry6", {"stability": 0.50, "similarity_boost": 0.75, "style": 0.40}),  # Andrew
    "priya":    ("SAz9YHcvj6GT2YYXdXww", {"stability": 0.65, "similarity_boost": 0.70, "style": 0.25}),  # River (no-nonsense officer)
    "phantom":  ("SAz9YHcvj6GT2YYXdXww", {"stability": 0.80, "similarity_boost": 0.60, "style": 0.10}),  # River (calm, precise AI)
}

SEGMENTS = [

    # ── CHAPTER 1 — Docking Bay Drama ────────────────────────────────
    ("ch1-intro", "narrator",
     "The Interstellar Fuel Network kept every ship in the galaxy moving. "
     "Hundreds of refuelling stations, thousands of tanks, millions of litres of fuel — "
     "all tracked, all measured, all accounted for. "
     "Until now. "
     "Jake Nova, Junior Fuel Inspector, docked at Kepler Station at 0600 hours — "
     "a busy depot orbiting a red dwarf star at the edge of the sector. "
     "Something was wrong with the fuel. And nobody could figure out what."),

    ("ch1-jake-arrival", "jake",
     "Alright, alright — I've got this. "
     "Kepler Station, Fuel Inspection Mission, first solo assignment. "
     "Let's see what we're dealing with."),

    ("ch1-priya-intro", "priya",
     "Inspector Nova. Good — you're here. I'm Fuel Officer Priya. "
     "We've got a problem. Our tanks are showing readings, but the readings are fractions "
     "and half my crew doesn't know what they mean in real terms. "
     "Three cargo ships are waiting to refuel. If we can't figure this out, "
     "those crews will be stranded in deep space."),

    ("ch1-jake-response", "jake",
     "Okay. Fractions I can do. Let me start with my own ship's gauge — "
     "if I can read that, I can read anything. "
     "My tank is divided into 4 equal sections. "
     "Let me check how many are full..."),

    ("ch1-q1-setup", "narrator",
     "Jake looked at the gauge on his own ship's control panel. "
     "The tank was divided into four equal sections, and exactly one section was highlighted in green."),

    ("ch1-q1-question", "jake",
     "My tank is divided into 4 equal parts. One part is full. "
     "What fraction of my tank is full? "
     "Remember — a fraction tells us how many parts out of the total."),

    ("ch1-q1-answer", "jake",
     "One out of four — that's one quarter. Written as a fraction: one over four. "
     "The bottom number tells you how many equal parts in total. "
     "The top number tells you how many are filled. "
     "Alright. Now let's read Kepler Station's tanks."),

    # ── CHAPTER 2 — Reading the Gauges ───────────────────────────────
    ("ch2-intro", "narrator",
     "Fuel Officer Priya led Jake to the main tank bay — "
     "a vast hangar lined with enormous cylindrical tanks, each one showing a glowing fraction display. "
     "Three ships were waiting at the docking clamps, their fuel lights blinking orange."),

    ("ch2-priya-tanks", "priya",
     "Tank A, Tank B, Tank C. Each one reads differently. "
     "I need to know exactly what fraction of fuel is in each one. "
     "Can you read them?"),

    ("ch2-q2-question", "jake",
     "Tank A. It's divided into 2 equal parts — and one part is full. "
     "What fraction is that? "
     "Draw the fraction bar in your head — two equal sections, one filled in."),

    ("ch2-q2-answer", "jake",
     "One out of two — one half. Written as one over two. "
     "Tank A is half full. Not bad — but is it enough? Let's check the others."),

    ("ch2-q3-setup", "narrator",
     "Jake moved to Tank B. This one was larger — and its display showed eight equal sections, "
     "with three of them lit up in green."),

    ("ch2-q3-question", "jake",
     "Tank B is divided into 8 equal sections. Three sections are full. "
     "What fraction of Tank B is full? "
     "And here's the important part — is that more or less than half?"),

    ("ch2-q3-answer", "jake",
     "Three out of eight — three eighths. "
     "Is that more or less than half? Well, half of eight is four. "
     "We only have three — so three eighths is less than half. "
     "Tank B is less than half full. That's a problem."),

    # ── CHAPTER 3 — The Phantom Clue ─────────────────────────────────
    ("ch3-intro", "narrator",
     "Priya had been checking the station logs while Jake read the gauges. "
     "She called him over, her expression grim."),

    ("ch3-priya-discovery", "priya",
     "Inspector Nova. Look at this. "
     "There's a ghost entry in the logs from last night — "
     "exactly one quarter of the fuel in each tank was transferred "
     "to an unknown destination. "
     "Whoever did this was... very precise."),

    ("ch3-jake-reaction", "jake",
     "One quarter from each tank? "
     "Let me work out what that means for Tank C..."),

    ("ch3-q4-setup", "narrator",
     "Tank C had been completely full before the transfer — "
     "all four sections lit up. Now it showed only three sections filled."),

    ("ch3-q4-question", "jake",
     "Tank C was completely full — four out of four sections. "
     "Now it shows three out of four. "
     "How many sections were taken? And what fraction went missing?"),

    ("ch3-q4-answer", "jake",
     "One section was taken. One out of four — one quarter. "
     "So the logs are right. Exactly one quarter was stolen from Tank C."),

    ("ch3-q5-setup", "narrator",
     "Jake checked Tank D. This one had only been half full before the transfer. "
     "Now it showed just one quarter remaining."),

    ("ch3-q5-question", "jake",
     "Here's where it gets interesting. Tank D was half full before — two out of four sections. "
     "Now it shows one quarter — one out of four sections. "
     "What fraction was taken from Tank D? "
     "Think carefully — it's the same fraction as Tank C, but Tank D was smaller to start with."),

    ("ch3-q5-answer", "jake",
     "One quarter was taken from Tank D too. "
     "But here's the thing — one quarter of a full tank is a lot more fuel than one quarter of a half-full tank. "
     "Same fraction. Different real amounts. "
     "That's going to matter."),

    # ── CHAPTER 4 — Enough to Launch? ────────────────────────────────
    ("ch4-intro", "narrator",
     "Three ships were waiting. "
     "Ship Orion needed a completely full tank to make its run. "
     "Ship Lyra only needed half a tank. "
     "Jake had to figure out if there was enough fuel to send them on their way."),

    ("ch4-jake-calculates", "jake",
     "Okay. Let me think about this. "
     "Tank A has one half. Tank C has three quarters. "
     "If I combine them... is that enough for a full tank?"),

    ("ch4-q6-question", "jake",
     "Ship Orion needs a full tank — four out of four. "
     "Tank A has one half. Tank C has three quarters. "
     "If we combine Tank A and Tank C, is that enough for Orion? "
     "How much do they have together?"),

    ("ch4-q6-answer", "jake",
     "One half is the same as two quarters. "
     "Two quarters plus three quarters equals five quarters. "
     "Five quarters is more than one whole tank — so yes! Orion has enough. "
     "Converting to the same denominator is the key."),

    ("ch4-q7-question", "jake",
     "Ship Lyra only needs half a tank — one half, or four eighths. "
     "Tank B has three eighths. "
     "Is three eighths more or less than one half? Does Lyra have enough?"),

    ("ch4-q7-answer", "jake",
     "Half a tank is four eighths. Tank B only has three eighths. "
     "Three eighths is less than four eighths — so no, Lyra doesn't have enough. "
     "She'll have to wait. "
     "Larger denominator doesn't mean larger fraction — that's the trap."),

    ("ch4-q8-question", "jake",
     "In the emergency store, there are 6 fuel pods. "
     "They need to be shared equally between 2 waiting ships. "
     "What fraction of the store does each ship get?"),

    ("ch4-q8-answer", "jake",
     "Six pods shared equally between two ships. "
     "Each ship gets three pods — that's one half of the store. "
     "Every ship gets one half."),

    # ── CHAPTER 5 — The First Clue ────────────────────────────────────
    ("ch5-intro", "narrator",
     "The ships were fuelled — some fully, some partially. The immediate crisis was managed. "
     "But Priya handed Jake a printout that made his stomach drop. "
     "The missing fuel hadn't just vanished. It had gone somewhere specific."),

    ("ch5-priya-printout", "priya",
     "The transfer logs are clear. Three tanks. Each drained by one quarter. "
     "The fuel was sent to Station Vega — far across the sector. "
     "And it happened over three separate nights. "
     "One quarter at a time."),

    ("ch5-jake-realises", "jake",
     "Three tanks, one quarter each. That's three quarter-portions total. "
     "And it happened three nights in a row, the same fraction each night... "
     "whoever did this is very, very methodical."),

    ("ch5-q9-question", "jake",
     "Three fuel tanks were each drained by one quarter. "
     "How many quarter-portions were taken in total? "
     "Think of it as: three groups of one quarter."),

    ("ch5-q9-answer", "jake",
     "Three groups of one quarter — three quarters. "
     "Three times one quarter equals three quarters. "
     "Three quarter-portions of fuel, all sent to Station Vega."),

    ("ch5-q10-question", "jake",
     "The missing fuel adds up to three quarters of a full tank. "
     "It was taken over three nights — the same fraction each night. "
     "What fraction was taken each night? "
     "Three quarters divided by three nights — what's one night's worth?"),

    ("ch5-q10-answer", "jake",
     "Three quarters divided by three equals one quarter. "
     "One quarter was taken each night, for three nights. "
     "Precise. Calculated. Deliberate."),

    ("ch5-cliffhanger", "narrator",
     "Jake was staring at the printout when the communications panel crackled. "
     "A holographic figure flickered to life — translucent blue, "
     "made entirely of shifting fraction bars and glowing number lines. "
     "It spoke in a calm, precise voice."),

    ("ch5-phantom", "phantom",
     "I have only been fair. "
     "Every station received exactly what they needed. "
     "Every fraction was calculated precisely. "
     "You will understand soon."),

    ("ch5-cliffhanger-end", "narrator",
     "Then it vanished. "
     "Jake stared at the empty panel for a long moment. "
     "The Fraction Phantom had made contact."),

    # ── FEEDBACK ─────────────────────────────────────────────────────
    ("feedback-correct-1", "jake",
     "Pre-launch check passed — that's exactly right!"),

    ("feedback-correct-2", "jake",
     "Yes! You've got it."),

    ("feedback-correct-3", "jake",
     "That's it — spot on!"),

    ("feedback-correct-4", "priya",
     "Correct. Good work, Inspector."),

    ("feedback-correct-5", "jake",
     "Nice one! The Fraction Phantom didn't count on you."),

    ("feedback-correct-6", "jake",
     "Nailed it."),

    ("feedback-wrong-1", "jake",
     "Not quite — try again. Think about how many equal parts there are, and how many are filled."),

    ("feedback-wrong-2", "jake",
     "Hmm, that's not it. Take another look — the numbers are there, you just need to put them together."),

    ("win", "narrator",
     "Jake Nova had read the gauges, fuelled the ships, and uncovered the first clue. "
     "The Fraction Phantom was out there — precise, methodical, and convinced it was being fair. "
     "The mystery of the missing quarter had only just begun. "
     "Issue Two: Fractions in the Fog Nebula."),
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

print(f"Generating {len(SEGMENTS)} segments...\n")
for i, (filename, character, text) in enumerate(SEGMENTS, 1):
    print(f"[{i}/{len(SEGMENTS)}] {character}: {filename}")
    generate(filename, character, text)
    time.sleep(0.3)

print(f"\n✅ Done.")
