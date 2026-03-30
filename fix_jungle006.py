#!/usr/bin/env python3
"""Fix Jungle Issue 6 — audio clips + images."""
import requests, os, time, base64
from openai import OpenAI

# ── AUDIO ────────────────────────────────────────────────────
API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
AUDIO_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue006")

VOICES = {
    "narrator": ("cjVigY5qzO86Huf0OWal", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),
    "blaze":    ("cgSgspJ2msm6clMCkdW9", {"stability": 0.55, "similarity_boost": 0.75, "style": 0.30}),
}

AUDIO_FIXES = [
    # Item 2: ch2-q3-setup — only narrated the setup, not the question part
    ("ch2-q3-setup", "narrator",
     "The deeper group: eighty-four Sprockets, "
     "and a vine bridge that could only take seven at a time."),

    # Item 6: ch4-q8-setup — incomplete, missing the key lesson line
    ("ch4-q8-setup", "narrator",
     "Two hundred and fifty-two divided by six gave forty-two groups. "
     "Two hundred and fifty-two divided by seven gave thirty-six groups. "
     "Dividing by a smaller number gives a bigger result. "
     "Tangle watched carefully. It was learning something new about its favourite thing,"),
]

def gen_audio(filename, character, text):
    out_path = os.path.join(AUDIO_DIR, f"{filename}.mp3")
    if os.path.exists(out_path):
        os.remove(out_path)
        print(f"  🗑  Deleted {filename}.mp3")
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
        print(f"  ⏳ Rate limited..."); time.sleep(15)
        return gen_audio(filename, character, text)
    else:
        print(f"  ❌ {filename}: {r.status_code} {r.text[:80]}"); return False

print(f"\n── Audio fixes ({len(AUDIO_FIXES)} clips) ──\n")
for filename, character, text in AUDIO_FIXES:
    print(f"  {character}: {filename}")
    gen_audio(filename, character, text)
    time.sleep(0.5)

# ── IMAGES ───────────────────────────────────────────────────
client = OpenAI()
IMG_DIR = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/issue006/'

SPROCKETS = (
    "tiny cobalt-blue alien creatures about knee-height, smooth round heads with exactly three thin antennae, "
    "large round expressive eyes, small stubby arms and legs, "
    "Disney Pixar CGI 3D animation style, cobalt-blue skin"
)
SETTING = (
    "the Deep Root: ancient jungle, enormous trees with above-ground roots, "
    "dappled golden-green light, moss-covered ground, "
    "Disney Pixar CGI 3D animation style, rich colour"
)
VINES = "natural earthy brown vines with dark green accents, warm muted tones, natural jungle palette"

# Rule: NO numbers, NO equations, NO answers visible anywhere in image. Holographic label only in cyan.
NO_ANSWERS = "Do NOT show any numbers, equations, division symbols, or answers written anywhere in the scene itself."

def gen_image(filename, prompt, size="1024x1024"):
    path = IMG_DIR + filename
    if os.path.exists(path):
        os.remove(path)
        print(f"  🗑  Deleted {filename}")
    print(f"  ⏳ {filename}...")
    for attempt in range(3):
        try:
            r = client.images.generate(model="gpt-image-1", prompt=prompt, size=size)
            data = base64.b64decode(r.data[0].b64_json)
            with open(path, 'wb') as f: f.write(data)
            print(f"  ✅ {filename} ({len(data):,} bytes)")
            time.sleep(12); return True
        except Exception as e:
            print(f"  ❌ attempt {attempt+1}: {e}")
            if attempt < 2: time.sleep(20)
    return False

print(f"\n── Image fixes (5 images) ──\n")

# Item 1: Q2 — 60 Sprockets in 5 groups, no numbers in scene
gen_image('q2-sprockets-60.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly sixty {SPROCKETS} standing in five clearly separated equal groups. "
    f"Each group of twelve Sprockets clustered together with a small gap between groups. "
    f"{NO_ANSWERS} "
    f"Holographic label '60 divided by 5' in cyan above the scene only. "
    f"{SETTING}. Clean educational composition.")

# Item 3: Q5 — 13 bundles made, 2 slots empty, no math/numbers in scene
gen_image('q5-bundles-needed.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Thirteen neat vine bundles on the left side of the scene. "
    f"Fifteen small Sprocket village icons on the right, two of them highlighted with a question mark above them showing they haven't received a bundle yet. "
    f"{NO_ANSWERS} "
    f"Holographic label '15 villages, 13 bundles — how many more?' in cyan only. "
    f"{SETTING}. Clean educational composition.")

# Item 4: Q6 — 252 vines in groups of 6, no answer shown
gen_image('q6-division-252-6.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A large collection of {VINES} arranged in many neat groups of six on the jungle floor. "
    f"Groups arranged in rows, clearly countable, all equal size. "
    f"{NO_ANSWERS} "
    f"Holographic label '252 divided by 6' in cyan only. "
    f"{SETTING}. Clean educational composition.")

# Item 5: Q7 — 252 vines in groups of 7, no answer shown
gen_image('q7-division-252-7.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A large collection of {VINES} arranged in many neat groups of seven on the jungle floor. "
    f"Groups in rows, visibly fewer groups than the previous arrangement. "
    f"{NO_ANSWERS} "
    f"Holographic label '252 divided by 7' in cyan only. "
    f"{SETTING}. Clean educational composition.")

# Item 7: Q10 — 288 vines in rows of 12, no answer shown
gen_image('q10-boss-288.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. Boss challenge feel. "
    f"A magnificent rectangular array of {VINES} on the jungle floor in rows of twelve. "
    f"Many rows, impressive scale, dramatic ancient golden light. "
    f"{NO_ANSWERS} "
    f"Holographic label '288 divided by 12' in cyan only, glowing. "
    f"{SETTING}. Epic educational composition.")

print("\n─── COMPLETE ───")
