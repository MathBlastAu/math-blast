#!/usr/bin/env python3
"""Jungle Issue 7 images — The Great Sharing. All five villages together. Tangle's finale."""
from openai import OpenAI
import base64, os, time

client = OpenAI()
DEST = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/issue007/'
os.makedirs(DEST, exist_ok=True)

BLAZE = (
    "10-year-old girl named Blaze: short practical dark hair, warm olive-tan skin, "
    "teal/cyan fitted jumpsuit with purple accent panels on shoulders and sides, "
    "bright yellow lightning bolt badge prominently on her left chest, "
    "glowing cyan holographic device strapped to left wrist, "
    "Disney Pixar CGI 3D animation style, vibrant saturated colours, expressive eyes, clean polished render"
)
SPROCKETS = (
    "tiny cobalt-blue alien creatures about knee-height, smooth round heads with exactly three thin antennae, "
    "large round expressive eyes, small stubby arms and legs, some wearing tiny leaf tunics, "
    "Disney Pixar CGI 3D animation style, cobalt-blue skin"
)
PIP = (
    "Chief Pip: a small cobalt-blue Sprocket, three thin antennae, large round wise eyes, "
    "wearing a tiny ceremonial leaf cloak, standing upright with dignified posture, "
    "Disney Pixar CGI 3D animation style"
)
TANGLE = (
    "Tangle: an enormous mysterious creature made entirely of thick natural earthy vines and woody branches, "
    "natural brown and dark green tones throughout, vines twisted and organic, "
    "large and gentle-looking, Disney Pixar CGI 3D animation style, "
    "no rainbow colours, no neon, natural jungle palette only"
)
SETTING = (
    "the Verdant Canopy jungle: a large beautiful clearing surrounded by ancient trees, "
    "golden warm light, Disney Pixar CGI 3D animation style, rich colour, cinematic quality"
)
VINES = "natural earthy brown vines with dark green accents, warm muted tones, natural jungle palette"
NO_ANSWERS = "Do NOT show any numbers, equations, division symbols, or answers written anywhere in the scene itself."

def gen(filename, prompt, size="1024x1024", retries=2):
    path = DEST + filename
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        print(f"  ⏭  {filename}"); return True
    print(f"  ⏳ {filename}...")
    for attempt in range(retries + 1):
        try:
            r = client.images.generate(model="gpt-image-1", prompt=prompt, size=size)
            data = base64.b64decode(r.data[0].b64_json)
            with open(path, 'wb') as f: f.write(data)
            print(f"  ✅ {filename} ({len(data):,} bytes)")
            time.sleep(12); return True
        except Exception as e:
            print(f"  ❌ attempt {attempt+1}: {e}")
            if attempt < retries: time.sleep(20)
    return False

print("\n── Chapter images (1536×1024) ──")

gen('ch1-all-villages.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"A massive gathering in {SETTING}: hundreds of {SPROCKETS} filling the clearing from all five villages. "
    f"{PIP} stands at the front on a small raised root. "
    f"{TANGLE} stands at the very back, enormous and still. "
    f"{BLAZE} stands to the side, looking out at the gathering with wonder. "
    f"Mood: historic, emotional, joyful.", size="1536x1024")

gen('ch2-village-allocation.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{PIP} stands beside a large leaf scroll showing the village allocations. "
    f"Five groups of {SPROCKETS} are visible, each group a different size. "
    f"In front of each group: a different pile of food items, proportional to group size. "
    f"{NO_ANSWERS} "
    f"Mood: methodical, fair, thoughtful.", size="1536x1024")

gen('ch3-tangle-bridges.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{TANGLE} is building a vine bridge between two jungle platforms, carrying bundles of {VINES}. "
    f"Two completed bridges visible behind it. {SPROCKETS} watch from the platforms. "
    f"Mood: purposeful, redemptive, Tangle using its gift for others.", size="1536x1024")

gen('ch4-dry-season.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"A large cave storeroom in {SETTING} filled with glowing water pods stacked in neat groups. "
    f"{PIP} stands with a leaf ledger. {SPROCKETS} form a queue. "
    f"The light is more muted, hinting at the Dry Season to come. "
    f"Mood: serious, careful, survival.", size="1536x1024")

gen('ch5-tangle-array.png',
    f"Disney Pixar CGI 3D animation. Wide aerial/elevated cinematic view. "
    f"Hundreds of {SPROCKETS} arranged in a perfect rectangular array on the jungle floor, "
    f"many neat equal rows, all standing still. "
    f"{TANGLE} stands at the side, having just finished arranging them. "
    f"Mood: breathtaking, mathematical, beautiful.", size="1536x1024")

print("\n── Question images (1024×1024) ──")

gen('q1-share-360.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Many {SPROCKETS} in rows, each holding a small bundle of food items. "
    f"{NO_ANSWERS} "
    f"Holographic label '360 divided by 120' in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q2-fernmoss-share.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A group of twenty-four {SPROCKETS} standing together labelled Fernmoss, "
    f"with a pile of food items in front of them. "
    f"To the side: a visual showing they are one fifth of all five groups. "
    f"{NO_ANSWERS} "
    f"Holographic label 'one fifth of 360' in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q3-split-ridge-share.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A group of thirty {SPROCKETS} standing together labelled Split Ridge, "
    f"with a larger pile of food in front of them than Fernmoss. "
    f"Visual showing they are one quarter of all groups. "
    f"{NO_ANSWERS} "
    f"Holographic label 'one quarter of 360' in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q4-bridges-240.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Five rope bridges side by side. "
    f"Below them: bundles of {VINES}, five equal stacks of forty-eight vines each. "
    f"{NO_ANSWERS} "
    f"Holographic label '240 divided by 48' in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q5-building-days.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A simple two-day timeline. Day 1: three bridges shown complete. Day 2: two bridges shown. "
    f"Five bridges total. "
    f"{NO_ANSWERS} "
    f"Holographic label '5 divided by 3' in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q6-pods-504.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A large collection of glowing water pods arranged in seven equal groups. "
    f"Each group has the same number of pods. "
    f"{NO_ANSWERS} "
    f"Holographic label '504 divided by 7' in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q7-monthly-72.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Seventy-two water pods arranged in four equal groups, one per month. "
    f"Each group identical. "
    f"{NO_ANSWERS} "
    f"Holographic label '72 divided by 4' in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q8-branchwick-18.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Eighteen water pods arranged in five groups on the ground. "
    f"Three groups of three, two groups of four — showing the remainder handled as extras. "
    f"{NO_ANSWERS} "
    f"Holographic label '18 divided by 5' in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q9-verify-360.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Five piles of food items labelled with their village names. "
    f"An arrow showing all five piles being combined into one large pile. "
    f"{NO_ANSWERS} "
    f"Holographic label '72 + 90 + 54 + 63 + 81' in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q10-boss-480.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. Boss challenge feel. "
    f"Hundreds of {SPROCKETS} arranged in a perfect rectangular grid: many rows of sixteen. "
    f"Dramatic golden light, impressive scale, seen from slightly above. "
    f"{NO_ANSWERS} "
    f"Holographic label '480 divided by 16' in cyan, glowing. "
    f"{SETTING}. Epic educational composition.")

gen('finale-honorary-sprocket.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. Warm golden light. "
    f"{PIP} stands at the front of a massive gathering of {SPROCKETS} in a perfect array. "
    f"He extends his tiny antenna toward {TANGLE} who stands at the back, enormous and still. "
    f"Tangle has just placed a bundle of {VINES} on the ground as a gift. "
    f"The moment is ceremonial, joyful, emotional. Every Sprocket is looking at Tangle. "
    f"Mood: triumphant, warm, the end of a long journey.", size="1536x1024")

print("\n─── COMPLETE ───")
