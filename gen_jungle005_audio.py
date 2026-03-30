#!/usr/bin/env python3
"""Jungle Issue 5 audio — scripts verbatim from HTML. Every paragraph covered."""
import requests, os, time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue005")
os.makedirs(OUT_DIR, exist_ok=True)

VOICES = {
    "narrator": ("cjVigY5qzO86Huf0OWal", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),
    "blaze":    ("cgSgspJ2msm6clMCkdW9", {"stability": 0.55, "similarity_boost": 0.75, "style": 0.30}),
    "crag":     ("pqHfZKP75CvOlQylNhV4", {"stability": 0.75, "similarity_boost": 0.70, "style": 0.10}),
}

SEGMENTS = [
    # CH1 — Para 1: arc recap — Tangle looked back
    ("ch1-intro", "narrator",
     "Tangle had looked back. That one moment changed everything. "
     "Footprints in Branchwick. Wrong divisions in Fernmoss. Grouping patterns at the Cascade Festival. "
     "Arrays in the sacred forest. And then, a bundle of twelve vines, placed at her feet. "
     "Whatever Tangle was, it was trying to reach her."),
    # CH1 — Para 2: Split Ridge terrain
    ("ch1-ridge", "narrator",
     "But right now, Blaze had a more urgent problem. "
     "Split Ridge was the most awkward village in the Verdant Canopy, "
     "carved into a cliff face, with platforms at different heights connected by rope bridges. "
     "Nothing here was regular. Nothing divided evenly. "
     "And thirteen Sprockets were stranded on the far side of a crumbling ledge, waiting for help."),
    # CH1 — Para 3: Elder Crag, the raft problem
    ("ch1-crag", "crag",
     "Each raft holds four. We have one raft. How many crossings do we need?"),
    ("ch1-q1-question", "blaze", "Thirteen Sprockets, and each raft holds four. How many crossings are needed to save everyone?"),
    ("ch1-q1-answer", "blaze", "Thirteen divided by four is three remainder one. Three crossings moves twelve, but that last Sprocket still needs saving. Four crossings."),

    # CH2 — Para 1: 22 rocks, equal shares, Split Ridge problem
    ("ch2-intro", "narrator",
     "The rescued Sprockets were safe on the platform. But now the real trouble started. "
     "Split Ridge ran entirely on equal shares, and equal shares at Split Ridge almost never came out perfectly."),
    # CH2 — Para 2: fire-nuts remainder tradition
    ("ch2-nuts", "narrator",
     "Twenty-two building rocks for five Sprocket families. Three families wanted to round up. "
     "One wanted to throw the extras off the cliff. Blaze had a better idea: "
     "split the leftover into fractions. Each family gets four rocks, "
     "and the two leftover rocks are shared between all five as two-fifths each."),
    # CH2 — Para 3: Blaze and Crag exchange
    ("ch2-blaze", "blaze",
     "What's two-fifths of a rock? Ask me a harder one."),
    ("ch2-q2-question", "blaze", "Twenty-two rocks shared between five families. How many whole rocks per family, and how many are left over?"),
    ("ch2-q2-answer", "blaze", "Twenty-two divided by five is four remainder two. Four rocks each, two left over."),
    # Q3 setup
    ("ch2-q3-setup", "narrator",
     "The cook's fire-nut supply: nineteen nuts for six Sprockets. "
     "By tradition at Split Ridge, the one leftover always goes to the eldest."),
    ("ch2-q3-question", "blaze", "Nineteen fire-nuts shared between six Sprockets. How many each, and how many left over?"),
    ("ch2-q3-answer", "blaze", "Nineteen divided by six is three remainder one. Three each, one left over for the eldest."),

    # CH3 — Para 1: Tangle arrives, ground shakes
    ("ch3-intro", "narrator",
     "The ground shook slightly. Then stopped. Then shook again. Blaze turned slowly. "
     "Tangle had followed her from the Array Forest all the way to Split Ridge."),
    # CH3 — Para 2: Tangle's 50 vines, groups of 8, distressed
    ("ch3-tangle", "narrator",
     "It stood at the edge of the cliff platform, carrying fifty vines in its trailing tendrils. "
     "It set them down and began arranging them into groups of eight. "
     "Seven groups of eight, and two left over. Tangle stopped. Stared at the two remaining vines. "
     "Did it again. Same result. The two leftover vines clearly distressed it."),
    # CH3 — Para 3: Blaze crouches down
    ("ch3-blaze", "blaze",
     "I know. Sometimes things just don't divide evenly. That's called a remainder. Watch."),
    ("ch3-q4-question", "blaze", "Tangle has fifty vines, in groups of eight. How many groups, and how many are left over?"),
    ("ch3-q4-answer", "blaze", "Fifty divided by eight is six remainder two. Six groups of eight is forty-eight. Two vines left over."),
    # Q5 setup
    ("ch3-q5-setup", "narrator",
     "Blaze showed Tangle: try groups of five instead of eight. "
     "She spread the fifty vines out evenly. Ten perfect groups. No vines left over. Tangle went very still."),
    ("ch3-q5-question", "blaze", "Now try fifty vines in groups of five. How many groups? Any left over?"),
    ("ch3-q5-answer", "blaze", "Fifty divided by five is ten, with nothing left over. Ten perfect groups. Sometimes a different group size makes all the difference."),

    # CH4 — Para 1: 27 planks, 4 bridges, 3 spare
    ("ch4-intro", "narrator",
     "The raft had solved the immediate problem. But the crumbling ledge wasn't going anywhere. "
     "Split Ridge needed proper rope bridges, "
     "and Elder Crag had twenty-seven planks stored in the supply cave. "
     "Each bridge needed six planks to be safe."),
    # CH4 — Para 2: four complete bridges, remainder is useful
    ("ch4-planks", "narrator",
     "Blaze did the calculation and smiled. Four complete bridges, with three planks to spare. "
     "Not enough for a fifth, but enough for four solid crossings. "
     "Sometimes a remainder is exactly what you need, it just can't be the answer on its own."),
    # CH4 — Para 3: 31 Sprockets, Blaze speaks
    ("ch4-cross", "blaze",
     "It won't divide evenly. It never does at Split Ridge. That's why we need to know what to do with the leftovers."),
    ("ch4-q6-question", "blaze", "Twenty-seven planks. Each bridge needs six. How many complete bridges, and how many planks are left over?"),
    ("ch4-q6-answer", "blaze", "Twenty-seven divided by six is four remainder three. Four complete bridges, three planks left over."),
    # Q7 setup
    ("ch4-q7-setup", "narrator",
     "Thirty-one Sprockets, spread across four bridges. They need to cross in roughly equal groups."),
    ("ch4-q7-question", "blaze", "Thirty-one Sprockets across four bridges. How many per bridge, and how many are left over for the last one?"),
    ("ch4-q7-answer", "blaze", "Thirty-one divided by four is seven remainder three. Seven per bridge on three of them, and four on the last one."),
    # Q8 setup
    ("ch4-q8-setup", "narrator",
     "The bridges could move eight Sprockets per minute. All thirty-one needed to cross. "
     "Blaze counted. Three minutes wouldn't be enough. You have to round up to save everyone."),
    ("ch4-q8-question", "blaze", "Thirty-one Sprockets, eight per minute. How many minutes to get everyone safely across?"),
    ("ch4-q8-answer", "blaze", "Thirty-one divided by eight is three remainder seven. Three minutes only moves twenty-four. "
     "Those seven are still waiting. Round up to four minutes."),

    # CH5 — Para 1: rescue complete, star-fruits
    ("ch5-intro", "narrator",
     "The rescue was complete. Every Sprocket was safe on the platform, the bridges were holding, "
     "and Elder Crag had reluctantly conceded that remainders were sometimes useful. "
     "The rescued Sprockets had brought a gift: forty-three star-fruits for the whole village of seven families. "
     "Another remainder problem."),
    # CH5 — Para 2: Tangle unloads all the vines
    ("ch5-tangle", "narrator",
     "But it was what happened next that stopped everyone. "
     "Tangle, which had been sitting quietly at the edge of the platform, stood up. "
     "And began unloading vines. Not fifty. Not a hundred. "
     "Vine after vine after vine, all the ones it had taken. All of them. "
     "Arranged in perfect groups of twelve, laid out along the clifftop."),
    # CH5 — Para 3: it was giving them back
    ("ch5-blaze", "narrator",
     "It was giving them back. "
     "Blaze looked at the rows of vine bundles. Then at Tangle. "
     "It hadn't taken the vines to cause harm. It had taken them because they were beautiful, "
     "and because it had never known there was anyone else to share them with. Now it did."),
    ("ch5-q9-question", "blaze", "Forty-three star-fruits for seven families. How many whole fruits per family, and how many are left over?"),
    ("ch5-q9-answer", "blaze", "Forty-three divided by seven is six remainder one. Six fruits each, one left over."),
    # Q10 setup
    ("ch5-q10-setup", "narrator",
     "The biggest share of all: one hundred units of food, divided as equally as possible between three cut-off villages. "
     "Not everything fits perfectly. But sometimes, almost equal is fair enough."),
    ("ch5-q10-question", "blaze", "One hundred units of food for three villages. How many does each village get, and how many are left over?"),
    ("ch5-q10-answer", "blaze",
     "One hundred divided by three is thirty-three remainder one. "
     "Two villages get thirty-three, one village gets thirty-four. "
     "Almost equal, and fair enough."),
    # Cliffhanger
    ("ch5-cliffhanger", "narrator",
     "When the last vine was laid down, Tangle stepped back. "
     "All the stolen vines, returned. Arranged in perfect groups of twelve along the clifftop. "
     "Then it sat down at the edge of the platform. Not leaving. Just waiting. "
     "It hadn't taken the vines to cause harm. "
     "It had taken them because they were beautiful, "
     "and because it had never known there was anyone else to share them with. Now it did."),

    # Feedback
    ("feedback-correct-1", "blaze", "That's it. Round up to save the last Sprocket."),
    ("feedback-correct-2", "blaze", "Correct. Four each, two left over."),
    ("feedback-correct-3", "blaze", "Nice work. Remainders matter here."),
    ("feedback-correct-4", "crag", "The ridge confirms it. Well counted, explorer."),
    ("feedback-correct-5", "blaze", "Exactly right."),
    ("feedback-correct-6", "blaze", "Perfect."),
    ("feedback-wrong-1", "blaze", "Not quite. Think about how many whole groups fit."),
    ("feedback-wrong-2", "blaze", "That's not it. Try again."),
    ("win", "narrator",
     "The bridges are built, the Sprockets are safe, and Tangle has given back everything it took. "
     "It just didn't know there was anyone to share with. Now it does. "
     "Join us for Issue Six, the Deep Root, where Tangle leads Blaze to its home "
     "and reveals the truth behind everything."),
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
