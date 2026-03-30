#!/usr/bin/env python3
"""Fix Jungle Issue 4 images — Q6 vine colours, Q7 no vines, cliffhanger Tangle inconsistency."""
from openai import OpenAI
import base64, os, time

client = OpenAI()
DEST = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/issue004/'

BLAZE = (
    "10-year-old girl named Blaze: short practical dark hair, warm olive-tan skin, "
    "teal/cyan fitted jumpsuit with purple accent panels on shoulders and sides, "
    "bright yellow lightning bolt badge prominently on her left chest, "
    "glowing cyan holographic device strapped to left wrist, "
    "Disney Pixar CGI 3D animation style, vibrant saturated colours, expressive eyes, clean polished render"
)
SETTING = (
    "the Array Forest: an ancient sacred jungle grove where enormous trees grow in mathematically "
    "perfect rectangular rows and columns, dappled golden light through dense canopy, "
    "moss-covered ground, ancient and reverent atmosphere, "
    "Disney Pixar CGI 3D animation style, rich colour, cinematic quality"
)
# Tangle consistent with Issue 3 — large creature made of natural earthy vines/branches
TANGLE = (
    "Tangle: an enormous mysterious creature made entirely of thick natural earthy vines and woody branches, "
    "natural brown and dark green tones, no bright colours, no rainbow, the vines are twisted and organic, "
    "the creature is large and gentle-looking but shy, not threatening, "
    "Disney Pixar CGI 3D animation style"
)
# Vine colour rule — natural earthy tones, NOT rainbow
VINE_COLOUR = (
    "natural earthy brown vines with dark green leaves, warm muted tones, "
    "NOT rainbow coloured, NOT neon, natural jungle palette"
)

def gen(filename, prompt, size="1024x1024"):
    path = DEST + filename
    # Force regen
    if os.path.exists(path):
        os.remove(path)
        print(f"  🗑  Deleted old {filename}")
    print(f"  ⏳ {filename}...")
    for attempt in range(3):
        try:
            r = client.images.generate(model="gpt-image-1", prompt=prompt, size=size)
            data = base64.b64decode(r.data[0].b64_json)
            with open(path, 'wb') as f: f.write(data)
            print(f"  ✅ {filename} ({len(data):,} bytes)")
            time.sleep(12)
            return True
        except Exception as e:
            print(f"  ❌ attempt {attempt+1}: {e}")
            if attempt < 2: time.sleep(20)
    return False

print("\n── Fixing 3 images ──\n")

# Q6 — vine array, wrong rainbow colours → natural earthy brown vines
gen('q6-vine-array-132.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 132 {VINE_COLOUR} arranged in 11 neat bundles of 12 on the forest floor. "
    f"Each bundle neatly tied with a leaf tie. Holographic '132 divided by 11' label in cyan. "
    f"{SETTING}. Clean educational composition.")

# Q7 — showed no vines at all, must show actual vines in rows
gen('q7-vine-rows-72.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 72 {VINE_COLOUR} laid out in a clear rectangular grid on the forest floor: 6 rows of 12 vines. "
    f"Each row clearly separated by a small gap. Individual vines visible and countable. "
    f"Holographic label reads '72 vines in rows of 12 — how many rows?' in cyan. "
    f"{SETTING}. Clean educational composition, vines prominent and obvious in the scene.")

# Cliffhanger — Tangle not consistent with Issue 3 design
gen('cliffhanger-tangle-gift.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. Twilight, golden-green dappled light. "
    f"{BLAZE} stands in the foreground of {SETTING}, holding a small bundle of natural brown vines. "
    f"{TANGLE} is moving away into the deep forest, but has stopped and turned its large vine-made head to look back at Blaze. "
    f"The moment feels significant and tender. Between them the light is soft and warm. "
    f"Mood: emotional, a turning point, connection just made. No rainbow colours anywhere.", size="1536x1024")

print("\n─── COMPLETE ───")
