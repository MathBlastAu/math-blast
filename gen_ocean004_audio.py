#!/usr/bin/env python3
"""Generate all audio files for Ocean Issue 004."""
import subprocess, os, json as j

APIKEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/audio/ocean/issue004"
os.makedirs(BASE, exist_ok=True)

ERIC = "cjVigY5qzO86Huf0OWal"
JESSICA = "cgSgspJ2msm6clMCkdW9"
BILL = "pqHfZKP75CvOlQylNhV4"

def tts(voice_id, text, out_path, stability=0.5, similarity=0.75, style=0.2):
    if os.path.exists(out_path):
        print(f"  SKIP (exists): {os.path.basename(out_path)}")
        return True
    text = text.replace("—", ",").replace("–", ",")
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {"stability": stability, "similarity_boost": similarity, "style": style}
    }
    cmd = [
        "curl", "-s", "-X", "POST",
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        "-H", f"xi-api-key: {APIKEY}",
        "-H", "Content-Type: application/json",
        "-d", j.dumps(payload),
        "--output", out_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"  OK: {os.path.basename(out_path)}")
        return True
    else:
        print(f"  FAIL: {os.path.basename(out_path)}, rc={result.returncode}")
        if os.path.exists(out_path): os.remove(out_path)
        return False

files = [
    # Chapter 1 - The Deep Trench
    (ERIC, "Marina and Flick descended beyond the Lattice floor, into the deep trench below. The light from Luminos faded. The ocean became a kind of black that felt almost solid. Flick's wing-tips were the only light, pulsing steady cyan in the dark.", "ch1-intro.mp3"),
    (ERIC, "They had been descending for twenty minutes when they saw the first sign. A faint blue-green glow, far below. Arranged in rows. In columns.", "ch1-descent.mp3"),
    (ERIC, "Like an array but alive, moving slowly, rhythmically. Pulsing. The same pattern Marina had read about in the Archive.", "ch1-glow.mp3"),
    (ERIC, "Marina sees the first cluster of the Whale's bioluminescent spots. There are three rows with six spots in each row. What is three times six?", "ch1-q1-question.mp3"),
    (ERIC, "That's right, eighteen! Three rows of six glowing spots. Three times six equals eighteen. The Whale's first pulse is confirmed!", "ch1-q1-answer.mp3"),

    # Chapter 2 - The Reveal
    (ERIC, "Then the whole Whale came into view. It was enormous in a way Marina had never experienced. Not big the way a large ship is big. Big the way a mountain is big, where it keeps going even when you think it should stop.", "ch2-reveal.mp3"),
    (ERIC, "Dark charcoal grey, nearly black, covered from fin-tip to tail in glowing blue-green spots arranged in perfect grids. Its eyes, large as Marina's entire sub, were gentle and violet-dark and looking directly at her.", "ch2-whale.mp3"),
    (ERIC, "Flick did not run. Flick hovered perfectly still, wing-tips glowing at their steadiest, most serene. Marina felt the deep rhythmic pulse of the Whale's bioelectric field through the water. Not threatening. Not angry. Just present. Bewildered. Ancient. Lonely.", "ch2-flick.mp3"),
    (ERIC, "Marina counts a section of the Whale's spots: five rows of six. What is five times six?", "ch2-q2-question.mp3"),
    (ERIC, "Correct! Five times six equals thirty. Five rows of six, that is thirty spots in this section!", "ch2-q2-answer.mp3"),
    (ERIC, "On the Whale's left flank, Marina counts another spot section. This section has four rows with seven spots in each row.", "ch2-q3-setup.mp3"),
    (ERIC, "How many spots in four times seven?", "ch2-q3-question.mp3"),
    (ERIC, "Right! Four times seven equals twenty-eight. Four rows of seven spots on the Whale's left flank.", "ch2-q3-answer.mp3"),

    # Chapter 3 - The Pattern
    (ERIC, "Marina had her datapad out now, recording the pulse pattern. The Whale's bioelectric field was not random. It pulsed in sequences. Groups of six, then seven, then eight. Over and over. The same multiplication pattern cycling through, like a song that kept repeating.", "ch3-intro.mp3"),
    (JESSICA, "It isn't disrupting the Lattice on purpose. It woke up and felt the Lattice field, and its own field interacted with it. The Whale doesn't understand why the stones are dark. It's confused and distressed and it keeps sending its own signal louder, trying to get an answer. The Lattice going dark is making the Whale send harder.", "ch3-marina.mp3", 0.55, 0.80, 0.25),
    (ERIC, "Flick drifted toward the Whale, antenna fins up, wing-tips at their gentlest cyan. The Whale's great eye tracked Flick with something that looked very much like curiosity.", "ch3-flick.mp3"),
    (ERIC, "Marina identifies the Whale's central pulse cluster: six rows of seven spots. What is six times seven?", "ch3-q4-question.mp3"),
    (ERIC, "Yes! Six times seven equals forty-two. Six rows of seven, that is forty-two spots in the central cluster!", "ch3-q4-answer.mp3"),
    (ERIC, "The pulse shifts to the eight-pattern. Marina sees a section with three rows of eight spots each. This section pulses brightest when the Whale seems most distressed.", "ch3-q5-setup.mp3"),
    (ERIC, "How many spots in three times eight?", "ch3-q5-question.mp3"),
    (ERIC, "Correct! Three times eight equals twenty-four. Three rows of eight, twenty-four spots in the distress section.", "ch3-q5-answer.mp3"),

    # Chapter 4 - The Signal
    (ERIC, "Marina worked fast. Her datapad captured the Whale's full pulse sequence. Flick, bonded to the datapad, could carry the signal to the right Lattice stones. But first Marina had to calculate exactly which stone groupings needed to light up, and in what sequence.", "ch4-intro.mp3"),
    (JESSICA, "Flick, I need you to be brave. I need you to carry this signal up through the water, to the Lattice field above us, and pulse it to the right stones. In the right pattern. Exactly as I calculate it.", "ch4-marina.mp3", 0.55, 0.80, 0.25),
    (ERIC, "Flick's antenna fins pointed straight up. Wing-tips pulsed cyan once, firmly. Ready.", "ch4-flick.mp3"),
    (ERIC, "To recalibrate the Lattice, Marina needs to match the signal to five rows of eight stones pulsing at once. What is five times eight?", "ch4-q6-question.mp3"),
    (ERIC, "Yes! Five times eight equals forty. Forty stones need to pulse at once in the first signal step!", "ch4-q6-answer.mp3"),
    (ERIC, "The second part of the signal sequence: seven groups of six stones need to activate in the next pulse. Marina writes the calculation quickly.", "ch4-q7-setup.mp3"),
    (ERIC, "What is seven times six?", "ch4-q7-question.mp3"),
    (ERIC, "Right! Seven times six equals forty-two. Forty-two stones in the second part of the signal.", "ch4-q7-answer.mp3"),
    (ERIC, "The third part of the signal: four groups of eight stones. This is the part that matches the Whale's strongest pulse. Marina checks the calculation twice.", "ch4-q8-setup.mp3"),
    (ERIC, "What is four times eight?", "ch4-q8-question.mp3"),
    (ERIC, "Correct! Four times eight equals thirty-two. Thirty-two stones, the heart of the Whale's own pulse pattern.", "ch4-q8-answer.mp3"),

    # Chapter 5 - The Lattice Lights Up
    (ERIC, "Flick went. Not fast, not reckless, but with a purpose Marina had never seen in the little manta ray before. Up through the dark water, carrying the calculated signal, wing-tips burning cyan brighter than Marina had ever seen them.", "ch5-intro.mp3"),
    (ERIC, "The Lattice stones began to light up. One section, then the next, then the next, spreading out across the ocean floor in the exact pattern Marina had calculated.", "ch5-flick.mp3"),
    (ERIC, "The Whale went still. Its bioelectric pulse slowed. Marina watched its great eye move across the newly glowing Lattice field, reading the pattern Flick had carried up. Then the Whale's spots changed colour. Warmer. Softer. And the deep rhythmic hum faded to silence.", "ch5-lattice.mp3"),
    (ERIC, "The Lattice reactivation ripple spreads through six groups of six stones at a time. What is six times six?", "ch5-q9-question.mp3"),
    (ERIC, "Yes! Six times six equals thirty-six. Thirty-six stones lighting up in each ripple as the Lattice wakes up!", "ch5-q9-answer.mp3"),
    (ERIC, "The final pulse of the Whale's signature, the one that signals it is leaving peacefully: eight groups of seven spots. Marina reads it, and smiles.", "ch5-q10-setup.mp3"),
    (ERIC, "The Whale's farewell pattern: eight groups of seven spots. What is eight times seven?", "ch5-q10-question.mp3"),
    (ERIC, "Arc complete! Eight times seven equals fifty-six. The Whale's farewell pattern, perfectly read. The Lattice is restored and the Luminous Deep is at peace!", "ch5-q10-answer.mp3"),

    # Finale
    (ERIC, "When Marina and Flick surfaced back into Luminos, every Lattice stone in the city was glowing at full brightness. The Coralfolk lined the streets, hundreds of them, their shells reflecting amber and teal light in every direction. A celebration that could be felt for a thousand tide-lengths in every direction.", "ch5-finale.mp3"),

    # Win
    (ERIC, "Outstanding! You helped Marina decode the Resonance Whale's pulse pattern and saved the entire Luminous Deep. You've mastered multiplication from groups all the way through to times six, seven, and eight. The Ocean Arc is complete. Well done, mathematician!", "win.mp3"),
]

errors = []
for item in files:
    if len(item) == 3:
        voice, text, fname = item
        stab, sim, sty = 0.5, 0.75, 0.2
    else:
        voice, text, fname, stab, sim, sty = item
    ok = tts(voice, text, os.path.join(BASE, fname), stab, sim, sty)
    if not ok:
        errors.append(fname)

print(f"\nDone. Errors: {errors}")
