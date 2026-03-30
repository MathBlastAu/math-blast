#!/usr/bin/env python3
"""Jungle Issue 6 audio — The Deep Root. Scripts verbatim from HTML."""
import requests, os, time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue006")
os.makedirs(OUT_DIR, exist_ok=True)

VOICES = {
    "narrator": ("cjVigY5qzO86Huf0OWal", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),
    "blaze":    ("cgSgspJ2msm6clMCkdW9", {"stability": 0.55, "similarity_boost": 0.75, "style": 0.30}),
    "tangle":   ("N2lVS1w4EtoT3dr4eOWO", {"stability": 0.85, "similarity_boost": 0.30, "style": 0.55}),
}

SEGMENTS = [
    # CH1 — Para 1: arc recap, Blaze followed Tangle
    ("ch1-intro", "narrator",
     "Tangle had given back every vine. It had sat outside Split Ridge, patient and still. "
     "And when Blaze finally walked toward it, it simply turned and walked deeper into the jungle. An invitation."),
    # CH1 — Para 2: the Deep Root, sculptures everywhere
    ("ch1-deep-root", "narrator",
     "She had followed for two hours before the jungle changed. "
     "The trees here were older, enormous, their roots above ground like walls. "
     "And between them, everywhere she looked: sculptures. "
     "Vine structures of extraordinary complexity, arranged in perfect rows and columns. "
     "Arrays of hundreds. Spirals that followed exact patterns. "
     "This was the Deep Root, and Tangle had lived here, alone, for a very long time."),
    # CH1 — Para 3: the largest sculpture
    ("ch1-sculpture", "narrator",
     "The largest sculpture she had ever seen filled the entire clearing. "
     "One hundred and forty-four vines, arranged in twelve perfect rows."),
    ("ch1-q1-question", "blaze", "One hundred and forty-four vines in twelve equal rows. How many vines per row?"),
    ("ch1-q1-answer", "blaze", "One hundred and forty-four divided by twelve equals twelve. Twelve vines per row. Tangle's favourite number,"),

    # CH2 — Para 1: Sprockets heard, not trapped, just lost
    ("ch2-intro", "narrator",
     "Then she heard them. Voices, small, blue, and extremely relieved. "
     "The missing Sprockets were here. Not trapped, not hurt. "
     "Just utterly lost among the most beautiful sculptures they had ever seen, "
     "following one to the next until they had no idea how far they'd come."),
    # CH2 — Para 2: 60 in 5 areas, and 84 deeper in
    ("ch2-sprockets", "narrator",
     "Sixty Sprockets, scattered across five areas of the Deep Root. "
     "For safe travel back through the narrow jungle paths, they needed to be organised into equal groups. "
     "Then, further in, one group had followed a sculpture trail all the way to the heart of the forest. "
     "Eighty-four Sprockets, needing to cross a vine bridge that could only take seven at a time."),
    ("ch2-q2-question", "blaze", "Sixty Sprockets in five equal groups. How many Sprockets per group?"),
    ("ch2-q2-answer", "blaze", "Sixty divided by five equals twelve. Twelve Sprockets per group. Safe to travel."),
    # Q3 setup
    ("ch2-q3-setup", "narrator",
     "The deeper group: eighty-four Sprockets, and a vine bridge that could only take seven at a time."),
    ("ch2-q3-question", "blaze", "Eighty-four Sprockets, seven at a time on the bridge. How many crossings?"),
    ("ch2-q3-answer", "blaze", "Eighty-four divided by seven equals twelve. Twelve crossings. Twelve again."),

    # CH3 — Para 1: Blaze sits with Tangle
    ("ch3-intro", "narrator",
     "Blaze found Tangle at the centre of the Deep Root, surrounded by its sculptures. "
     "She sat down across from it. No more chasing. Just being present."),
    # CH3 — Para 2: lays vines, gestures equal sharing
    ("ch3-sharing", "narrator",
     "She laid twelve vines on the ground between them. "
     "Then she divided them into two equal groups of six, slid one group toward Tangle and kept one. "
     "Tangle watched. She did it again with a larger pile, six equal groups. "
     "Each time, she gestured: one for you, one for me. One for you, one for me. Equal."),
    # CH3 — Para 3: Tangle makes a sound
    ("ch3-tangle-moment", "narrator",
     "Tangle was completely still. "
     "Then it made a sound, low, resonant, like the deepest root of the oldest tree in the forest. "
     "It had understood."),
    # Tangle's first sound — minimal, deep, significant
    ("tangle-hum", "tangle", "..."),
    ("ch3-q4-question", "blaze", "Tangle has one hundred and fifty-six short vines to share with the villages. Each village gets a bundle of twelve. How many villages can receive a bundle?"),
    ("ch3-q4-answer", "blaze", "One hundred and fifty-six divided by twelve equals thirteen. Thirteen bundles for thirteen villages."),
    # Q5 setup
    ("ch3-q5-setup", "narrator",
     "But there are fifteen villages in the Verdant Canopy. Thirteen bundles isn't enough. "
     "Fifteen villages times twelve vines each is one hundred and eighty vines. "
     "Tangle has one hundred and fifty-six. "
     "How many more bundles does it need to collect?"),
    ("ch3-q5-question", "blaze", "Fifteen villages need bundles of twelve. Tangle has one hundred and fifty-six vines, that's thirteen bundles. How many more bundles does Tangle need?"),
    ("ch3-q5-answer", "blaze", "Fifteen minus thirteen is two. Two more bundles of twelve. Twenty-four more vines."),

    # CH4 — Para 1: 252 vines in a cave
    ("ch4-intro", "narrator",
     "Tangle led Blaze to a separate cave at the edge of the Deep Root. "
     "Inside: a collection of two hundred and fifty-two vines, all perfectly preserved. Tangle's oldest store."),
    # CH4 — Para 2: different ways to share
    ("ch4-groups", "narrator",
     "Blaze could see immediately that this collection could be shared many different ways. "
     "Six villages each receiving a bundle, or seven villages each receiving a bundle. "
     "The group size would change the number of bundles. Smaller groups, more bundles. Larger groups, fewer bundles."),
    # CH4 — Para 3: Blaze speaks
    ("ch4-blaze", "blaze",
     "This is the thing about division. Changing the group size changes everything. Let's work out both."),
    ("ch4-q6-question", "blaze", "Two hundred and fifty-two vines divided into groups of six. How many groups?"),
    ("ch4-q6-answer", "blaze", "Two hundred and fifty-two divided by six equals forty-two. Forty-two groups."),
    # Q7 setup
    ("ch4-q7-setup", "narrator", "Now try the same two hundred and fifty-two vines, but in groups of seven."),
    ("ch4-q7-question", "blaze", "Two hundred and fifty-two vines divided into groups of seven. How many groups?"),
    ("ch4-q7-answer", "blaze", "Two hundred and fifty-two divided by seven equals thirty-six. Thirty-six groups, fewer than dividing by six."),
    # Q8 setup
    ("ch4-q8-setup", "narrator",
     "Two hundred and fifty-two divided by six gave forty-two groups. "
     "Two hundred and fifty-two divided by seven gave thirty-six groups. "
     "Dividing by a smaller number gives a bigger result. Tangle watched carefully."),
    ("ch4-q8-question", "blaze", "Which division gives the bigger answer: two hundred and fifty-two divided by six, or two hundred and fifty-two divided by seven?"),
    ("ch4-q8-answer", "blaze", "Two hundred and fifty-two divided by six equals forty-two. That's the bigger answer. Smaller divisor, bigger result."),

    # CH5 — Para 1: Tangle leads to clearing, promise
    ("ch5-intro", "narrator",
     "Tangle had a promise to make. Not in words. In action. "
     "It led Blaze to an open clearing, far from every vine path, far from every village connection. "
     "A blank canvas. Its vines would go here, and only here."),
    # CH5 — Para 2: the clearing, 13 rows of 9
    ("ch5-clearing", "narrator",
     "The clearing was perfect for a large sculpture: thirteen rows, each nine positions wide. "
     "One hundred and seventeen positions in total. Tangle began immediately. "
     "It knew exactly what it wanted to make."),
    # CH5 — Para 3: the enormous secret sculpture
    ("ch5-reveal", "narrator",
     "And then it showed her what it had been making in secret, at the very centre of the Deep Root, "
     "for longer than any Sprocket had been alive. "
     "Something so large it could only be seen from above the canopy."),
    ("ch5-q9-question", "blaze", "The clearing has one hundred and seventeen positions in rows of nine. How many rows does the clearing have?"),
    ("ch5-q9-answer", "blaze", "One hundred and seventeen divided by nine equals thirteen. Thirteen rows."),
    # Q10 setup
    ("ch5-q10-setup", "narrator",
     "Tangle's first clearing sculpture: two hundred and eighty-eight vines, arranged in rows of twelve. "
     "Its favourite number. How many rows would the new sculpture have?"),
    ("ch5-q10-question", "blaze", "Two hundred and eighty-eight vines in rows of twelve. How many rows?"),
    ("ch5-q10-answer", "blaze",
     "Two hundred and eighty-eight divided by twelve equals twenty-four. Twenty-four rows. "
     "Tangle's first clearing sculpture."),
    # Cliffhanger
    ("ch5-cliffhanger", "narrator",
     "Tangle led Blaze to a place where the canopy opened up, and she could see down into the Deep Root from above. "
     "And there it was. An enormous vine sculpture covering hundreds of square metres of jungle floor. "
     "Equally spaced. Perfectly scaled. A pattern that repeated, and repeated, and repeated, always in the same direction. "
     "A number line. Not just any number line. Tangle's number line. "
     "Built one vine at a time, across centuries, without anyone to show it how. "
     "Tangle had been doing mathematics its whole life. It just didn't know that's what it was called."),

    # Feedback
    ("feedback-correct-1", "blaze", "That's it. Twelve again. Always twelve with Tangle."),
    ("feedback-correct-2", "blaze", "Correct. Equal groups for safe travel."),
    ("feedback-correct-3", "blaze", "Nice work. Right on the first try."),
    ("feedback-correct-4", "blaze", "Exactly right."),
    ("feedback-correct-5", "blaze", "Perfect."),
    ("feedback-correct-6", "blaze", "That's it."),
    ("feedback-wrong-1", "blaze", "Not quite. Think about how many groups fit."),
    ("feedback-wrong-2", "blaze", "That's not it. Try again."),
    ("win", "narrator",
     "The truth is out. Tangle didn't know the vines connected the villages. It was making art. "
     "Mathematical art, alone, for centuries. And now it finally has someone to share it with. "
     "Join us for Issue Seven, the Great Sharing, where all five villages reunite "
     "and Tangle finally gets to use its gift for others."),
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
