#!/usr/bin/env python3
"""Fix Jungle Issue 5 — audio clips, images."""
import requests, os, time, base64
from openai import OpenAI

# ── AUDIO ────────────────────────────────────────────────────
API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
AUDIO_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/jungle/issue005")

VOICES = {
    "narrator": ("cjVigY5qzO86Huf0OWal", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),
    "blaze":    ("cgSgspJ2msm6clMCkdW9", {"stability": 0.55, "similarity_boost": 0.75, "style": 0.30}),
    "crag":     ("pqHfZKP75CvOlQylNhV4", {"stability": 0.75, "similarity_boost": 0.70, "style": 0.10}),
}

# NEW/FIXED audio clips
AUDIO_FIXES = [
    # Item 2: Split ch2-blaze into Crag asking + Blaze responding
    # New clip: Elder Crag asks the question
    ("ch2-crag-rocks", "crag",
     "What's two-fifths of a rock?"),
    # Blaze responds only
    ("ch2-blaze", "blaze",
     "Ask me a harder one."),

    # Item 5: ch4-q7-setup was missing second sentence
    ("ch4-q7-setup", "narrator",
     "Thirty-one Sprockets, spread across four bridges. "
     "They need to cross in roughly equal groups. "
     "Three bridges carry seven Sprockets each, and one bridge carries the last four."),

    # Item 6: answer clip had the wrong explanation — fix it
    ("ch4-q7-answer", "blaze",
     "Thirty-one divided by four is seven remainder three. "
     "Seven per bridge on four of them, and three on the last one."),

    # Item 8: ch5-intro wasn't matching screen — missing "good day" and "hated even numbers" lines
    ("ch5-intro", "narrator",
     "The rescue was complete. Every Sprocket was safe on the platform, the bridges were holding, "
     "and Elder Crag had reluctantly conceded that remainders were sometimes useful. "
     "A good day at Split Ridge."),
    ("ch5-starfruit", "narrator",
     "The rescued Sprockets had brought a gift from their side of the ridge: "
     "forty-three star-fruits for the whole village of seven families. "
     "Another remainder problem. "
     "Blaze was beginning to think Split Ridge had been built by someone who hated even numbers."),
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
IMG_DIR = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/issue005/'

SPROCKETS = (
    "tiny cobalt-blue alien creatures about knee-height, smooth round heads with exactly three thin antennae, "
    "large round expressive eyes, small stubby arms and legs, "
    "Disney Pixar CGI 3D animation style, cobalt-blue skin"
)
SETTING = (
    "Split Ridge: a rugged cliff-face jungle village with rope bridges connecting stone platforms, "
    "Disney Pixar CGI 3D animation style, rich colour"
)
VINES = "natural earthy brown vines with dark green accents, warm muted tones, natural jungle palette"

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

print(f"\n── Image fixes (4 images) ──\n")

# Item 1: Q1 — no fractions/answers shown, exactly 13 Sprockets waiting, raft holds 4 (show first 4 boarding)
gen_image('q1-raft-13.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly thirteen {SPROCKETS} standing on a rocky ledge. "
    f"A simple wooden raft at the water's edge, with room for exactly four Sprockets. "
    f"Four Sprockets are boarding the raft, nine are waiting behind them in a queue. "
    f"No numbers written in the scene, no fraction symbols, no answers shown. "
    f"Holographic label '13 divided by 4' in cyan above the scene. "
    f"{SETTING}. Clean educational composition.")

# Item 3: Q3 — exactly 19 fire-nuts, 6 groups of 3 plus 1 leftover
gen_image('q3-firenuts-19.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly nineteen small glowing orange fire-nuts on a rocky surface. "
    f"Arranged as six groups of three nuts, with exactly one nut sitting separately to the side. "
    f"Each group clearly separated by a small gap. "
    f"No numbers written in the scene. "
    f"Holographic label '19 divided by 6' in cyan. "
    f"{SETTING}. Clean educational composition.")

# Item 4: Q5 — show 10 groups of 5 vines but do NOT show the number 10 or the answer
gen_image('q5-vines-50-groups5.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly fifty {VINES} laid out in a clear rectangular grid on rocky ground: ten rows of five vines. "
    f"All groups perfectly equal, no vines left over. "
    f"Do NOT show any numbers written in the scene. Do NOT show the number 10 anywhere. "
    f"Holographic label '50 vines in groups of 5' in cyan only. "
    f"{SETTING}. Clean educational composition.")

# Item 7: Q8 — simple bridge scene, 8 Sprockets crossing, division label in corner only
gen_image('q8-crossing-time.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A single rope bridge in {SETTING} with exactly eight {SPROCKETS} walking across it side by side. "
    f"On the left platform: a queue of remaining Sprockets waiting to cross. "
    f"Simple, clear, one bridge only. "
    f"Holographic label '31 divided by 8' in the corner in cyan. "
    f"Clean educational composition, focus on the bridge and the eight crossing Sprockets.")

print("\n─── COMPLETE ───")
