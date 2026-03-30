#!/usr/bin/env python3
"""Generate missing audio files for Ocean Issue 003."""
import subprocess, os, json

APIKEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/audio/ocean/issue003"
os.makedirs(BASE, exist_ok=True)

ERIC = "cjVigY5qzO86Huf0OWal"
JESSICA = "cgSgspJ2msm6clMCkdW9"
BILL = "pqHfZKP75CvOlQylNhV4"

def tts(voice_id, text, out_path, stability=0.5, similarity=0.75, style=0.2):
    if os.path.exists(out_path):
        print(f"  SKIP (exists): {out_path}")
        return True
    text = text.replace("—", ",").replace("–", ",")
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": style
        }
    }
    import json as j
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
    # Missing from issue003: ch4-q8-answer, ch5 chapter files, ch5 question files, win.mp3
    # ch4-q8-answer
    (ERIC, "That's right, six rows of four! Six times four equals twenty-four, and the Mirror Truth shows us that four times six is exactly the same. Twenty-four tablets, whichever way you count them.", "ch4-q8-answer.mp3"),
    # ch5 chapter
    (ERIC, "Elder Luma read in silence for a long time. Marina waited, running calculations on her datapad. The Whale's spots were arranged in grids, five rows of five. That was twenty-five spots per cluster. And each cluster pulsed. The pulse was the signal.", "ch5-intro.mp3"),
    (JESSICA, "If we could match the Whale's own pattern and send it back to the Whale through the Lattice stones, perhaps the Whale would understand it as a greeting. Not a threat. Not interference. A greeting.", "ch5-marina.mp3"),
    (BILL, "The Archive holds all records. But some things in the deep cannot be found in records. Only in the meeting of them.", "ch5-luma.mp3"),
    # ch5 questions
    (ERIC, "The Whale's bioluminescent spots are arranged in a grid: five rows of five spots each per cluster. How many spots in one cluster?", "ch5-q9-question.mp3"),
    (ERIC, "That's right, twenty-five! Five rows of five is a perfect square array. Five times five equals twenty-five spots per cluster.", "ch5-q9-answer.mp3"),
    (ERIC, "One last array in the Archive record, the Whale's largest spot grid, used for long-distance signalling. The old record shows three rows of eight spots each.", "ch5-q10-setup.mp3"),
    (ERIC, "The Whale's long-distance spot grid: three rows of eight spots. How many spots altogether?", "ch5-q10-question.mp3"),
    (ERIC, "Amazing work! Three rows of eight equals twenty-four spots. Marina has the Whale's signalling pattern. Now she must use it to make contact!", "ch5-q10-answer.mp3"),
    # cliffhanger
    (ERIC, "The old porthole of the shipwreck lit up. Not with filtered surface light. With bioluminescence. Blue-green and patterned, moving in slow, deliberate pulses. A vast fin passed the glass, so large it blocked out the entire porthole for three long seconds. And then the spots. Rows of them. Columns of them. The same grid pattern Marina had just been reading from the ancient record. Alive. Present. Right outside the window. Marina pressed her palm against the glass. The bioluminescent spots pulsed once in response.", "ch5-cliffhanger.mp3"),
    (JESSICA, "Elder Luma, it can see us.", "ch5-marina-whisper.mp3"),
    # win
    (ERIC, "Incredible work! You've mastered rows, columns, and the Mirror Truth. Arrays are just multiplication in disguise, and now the Resonance Whale is right outside the Archive window. The deepest challenge yet awaits in issue four!", "win.mp3"),
]

errors = []
for voice, text, fname in files:
    ok = tts(voice, text, os.path.join(BASE, fname))
    if not ok:
        errors.append(fname)

print(f"\nDone. Errors: {errors}")
