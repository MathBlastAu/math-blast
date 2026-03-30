#!/usr/bin/env python3
"""Jungle Issue 4 audio — scripts verbatim from HTML. Every paragraph covered."""
import requests, os, time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue004")
os.makedirs(OUT_DIR, exist_ok=True)

VOICES = {
    "narrator": ("cjVigY5qzO86Huf0OWal", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),
    "blaze":    ("cgSgspJ2msm6clMCkdW9", {"stability": 0.55, "similarity_boost": 0.75, "style": 0.30}),
    "keeper":   ("pqHfZKP75CvOlQylNhV4", {"stability": 0.70, "similarity_boost": 0.70, "style": 0.15}),
}

SEGMENTS = [
    # CH1 — Para 1: trail recap
    ("ch1-intro", "narrator",
     "Blaze had been following the trail of clues. Footprints in Branchwick. Wrong divisions in Fernmoss. "
     "Tangle learning grouping patterns at the Cascade Festival. "
     "Each one pointing deeper into the jungle, and now she was here."),
    # CH1 — Para 2: Array Forest description
    ("ch1-forest", "narrator",
     "The Array Forest was the most sacred site in the Verdant Canopy: "
     "trees planted in perfect rectangular rows and columns by ancient Sprocket mathematicians. "
     "But someone had moved through it. Rows were broken. Trees were missing from their positions."),
    # CH1 — Para 3: Keeper Moss
    ("ch1-keeper", "keeper",
     "If we cannot verify the arrays, our entire history is lost. "
     "Twenty-four trees, four equal rows. Can you tell me how many per row?"),
    ("ch1-q1-question", "blaze", "Twenty-four trees in four equal rows. How many trees per row?"),
    ("ch1-q1-answer", "blaze", "Twenty-four divided by four equals six. Six trees per row. The first array is verified."),

    # CH2 — Para 1: working row by row
    ("ch2-intro", "narrator",
     "Blaze worked through the forest with Keeper Moss, checking each array against the ancient records. "
     "Every tree in its place, or it wasn't."),
    # CH2 — Para 2: second array, third array, vine bundles
    ("ch2-arrays", "narrator",
     "The second array: thirty-five trees in five equal rows. "
     "The third: forty-eight trees in six equal rows. "
     "As she worked, Blaze kept noticing something. Vine bundles, left behind. Always in groups of twelve."),
    # CH2 — Para 3: Blaze murmurs
    ("ch2-blaze", "blaze",
     "Twelve again. Whatever has been through here, it has left its signature."),
    ("ch2-q2-question", "blaze", "Thirty-five trees in five equal rows. How many trees per row?"),
    ("ch2-q2-answer", "blaze", "Thirty-five divided by five equals seven. Seven trees per row."),
    # Q3 setup
    ("ch2-q3-setup", "narrator", "The third array: forty-eight trees in six equal rows."),
    ("ch2-q3-question", "blaze", "Forty-eight trees in six equal rows. How many trees per row?"),
    ("ch2-q3-answer", "blaze", "Forty-eight divided by six equals eight. Eight trees per row. And vine bundles again, always groups of twelve."),

    # CH3 — Para 1: prestige arrays intro
    ("ch3-intro", "narrator",
     "At the heart of the forest stood the prestige arrays, the oldest and most precise plantings of all. "
     "These were the ones Keeper Moss feared most for."),
    # CH3 — Para 2: 96 and 84 trees
    ("ch3-arrays", "narrator",
     "The first prestige array: ninety-six trees in eight rows. "
     "The second: eighty-four trees in seven rows. "
     "Keeper Moss watched anxiously as Blaze worked through the calculations."),
    # CH3 — Para 3: Blaze surprised
    ("ch3-blaze", "blaze",
     "Both come out the same. Twelve per row each time. That cannot be a coincidence."),
    ("ch3-q4-question", "blaze", "Ninety-six trees in eight equal rows. How many trees per row?"),
    ("ch3-q4-answer", "blaze", "Ninety-six divided by eight equals twelve. Twelve per row in the prestige planting."),
    # Q5 setup
    ("ch3-q5-setup", "narrator", "The second prestige array: eighty-four trees in seven rows."),
    ("ch3-q5-question", "blaze", "Eighty-four trees in seven equal rows. How many trees per row?"),
    ("ch3-q5-answer", "blaze", "Eighty-four divided by seven equals twelve. Both prestige arrays, twelve per row each time."),

    # CH4 — Para 1: vine array found
    ("ch4-intro", "narrator",
     "And then Blaze saw it. Not a tree array, a vine array. "
     "One hundred and thirty-two vines, arranged in eleven neat bundles. "
     "Twelve per bundle. Perfectly formed."),
    # CH4 — Para 2: crouches down, realises
    ("ch4-blaze", "narrator",
     "She crouched down slowly. This was not damage. This was creation. "
     "Whatever had been moving through the Array Forest wasn't disturbing it. It was adding to it."),
    # CH4 — Para 3: Tangle at edge
    ("ch4-tangle", "narrator",
     "At the far edge of the clearing, something enormous shifted in the shadows. "
     "Blaze stayed very still."),
    ("ch4-q6-question", "blaze", "One hundred and thirty-two vines in eleven equal bundles. How many vines per bundle?"),
    ("ch4-q6-answer", "blaze", "One hundred and thirty-two divided by eleven equals twelve. Tangle always makes groups of twelve."),
    # Q7 setup
    ("ch4-q7-setup", "narrator",
     "The vine array stretched further than Blaze first thought. Seventy-two vines in total, in rows of twelve."),
    ("ch4-q7-question", "blaze", "Seventy-two vines in rows of twelve. How many rows?"),
    ("ch4-q7-answer", "blaze", "Seventy-two divided by twelve equals six. Six rows in Tangle's vine array."),
    # Q8 setup
    ("ch4-q8-setup", "narrator",
     "As Blaze watched, Tangle added one more row of twelve vines. The array now held eighty-four vines in total."),
    ("ch4-q8-question", "blaze", "Tangle adds a row of twelve. Total vines: eighty-four. Eighty-four in rows of twelve. How many rows now?"),
    ("ch4-q8-answer", "blaze", "Eighty-four divided by twelve equals seven. One more row, seven rows total."),

    # CH5 — Para 1: Keeper ready, Blaze watching
    ("ch5-intro", "narrator",
     "Keeper Moss was ready to declare the records restored. "
     "But Blaze hadn't moved. She was still watching the edge of the clearing."),
    # CH5 — Para 2: reaches out hand
    ("ch5-hand", "narrator",
     "Then she did something that surprised even herself. She reached out her hand."),
    # CH5 — Para 3: Tangle moves forward, drops bundle
    ("ch5-tangle-gift", "narrator",
     "The enormous shape didn't run. Slowly, very slowly, it moved forward. "
     "And then it set something down at her feet. A bundle of twelve vines, perfectly tied."),
    # CH5 — Para 4: Blaze speaks
    ("ch5-blaze", "blaze",
     "It's been trying to help. This whole time. It just didn't know how."),
    ("ch5-q9-question", "blaze", "One hundred and fifty-six vines in rows of twelve. How many rows?"),
    ("ch5-q9-answer", "blaze", "One hundred and fifty-six divided by twelve equals thirteen. Thirteen rows."),
    # Q10 setup
    ("ch5-q10-setup", "narrator",
     "Tangle's greatest collection: one hundred and sixty-eight vines, arranged in rows of twelve."),
    ("ch5-q10-question", "blaze", "One hundred and sixty-eight vines in rows of twelve. How many rows?"),
    ("ch5-q10-answer", "blaze",
     "One hundred and sixty-eight divided by twelve equals fourteen. "
     "Fourteen rows. Tangle's greatest array. And it looked back."),
    # Cliffhanger
    ("ch5-cliffhanger", "narrator",
     "Blaze held the bundle of twelve vines. Tangle had already turned and was moving back into the deep forest. "
     "But it stopped. And looked back. "
     "It had never done that before."),

    # Feedback
    ("feedback-correct-1", "blaze", "That's it. The first array is verified."),
    ("feedback-correct-2", "blaze", "Correct. Every row accounted for."),
    ("feedback-correct-3", "blaze", "Nice work. Right every time."),
    ("feedback-correct-4", "keeper", "The records confirm it. Well done, explorer."),
    ("feedback-correct-5", "blaze", "Exactly right."),
    ("feedback-correct-6", "blaze", "Perfect."),
    ("feedback-wrong-1", "blaze", "Not quite. Think: how many in each row?"),
    ("feedback-wrong-2", "blaze", "That's not it. Try again."),
    ("win", "narrator",
     "The Array Forest is restored, every tree in its place, every record verified. "
     "And Blaze has finally made contact. Tangle looked back. Something has changed between them. "
     "Join us for Issue Five, Split Ridge, where Tangle brings back the vines it took "
     "and discovers what remainders feel like."),
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
