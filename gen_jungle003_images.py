#!/usr/bin/env python3
"""
Generate ALL 17 images for Jungle Issue 3 — "Grouping at the Waterfall"
Same pattern as gen_jungle001_images.py — locked character constants.
"""
from openai import OpenAI
import base64, os, time

client = OpenAI()
DEST = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/issue003/'
os.makedirs(DEST, exist_ok=True)

# ── LOCKED CONSTANTS (identical to Issues 1 & 2) ────────────────────────────
BLAZE = (
    "10-year-old girl named Blaze: short practical dark hair, warm olive-tan skin, "
    "teal/cyan fitted jumpsuit with purple accent panels on shoulders and sides, "
    "bright yellow lightning bolt badge prominently on her left chest, "
    "glowing cyan holographic device strapped to left wrist, "
    "Disney Pixar CGI 3D animation style, vibrant saturated colours, "
    "expressive eyes, clean polished render"
)

SPROCKETS = (
    "tiny cobalt-blue alien creatures about knee-height, "
    "smooth round heads with exactly three thin antennae, "
    "large round expressive eyes, small stubby arms and legs, "
    "some wearing tiny leaf tunics or aprons, "
    "Disney Pixar CGI 3D animation style, same cobalt-blue skin in every image"
)

ELDER = (
    "one specific Sprocket named Elder Splash: same cobalt-blue skin, three thin antennae, "
    "silver stripe on each antenna, large round expressive eyes, wearing a small ceremonial leaf robe, "
    "expression always measured and dignified, Disney Pixar CGI 3D animation style"
)

RIPPLE = (
    "one specific Sprocket named Ripple: same cobalt-blue skin, three thin antennae, "
    "large round expressive eyes, wearing a tiny blue tunic, "
    "expression always excited and breathless, Disney Pixar CGI 3D animation style"
)

SETTING_CASCADE = (
    "Cascade Clearing: a wide misty waterfall clearing in a jungle middle-canopy, "
    "soft rainbow light from the waterfall mist, hanging moss, glowing bioluminescent flowers, "
    "festival decorations — coloured lanterns, ribbon-flowers, sparkle-stones, "
    "Disney Pixar CGI 3D animation style, rich colour, cinematic quality"
)

SETTING_JUNGLE = (
    "alien jungle canopy world: enormous ancient trees with platforms and rope bridges, "
    "bioluminescent blue-green plants glowing softly, warm golden light filtering through giant tropical leaves, "
    "fireflies drifting through the air, "
    "Disney Pixar CGI 3D animation style, rich colour, cinematic quality"
)

def gen(filename, prompt, size="1024x1024", retries=2):
    path = DEST + filename
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        print(f"  ⏭  {filename} already exists — skipping")
        return True
    print(f"  ⏳ {filename} ...")
    for attempt in range(retries + 1):
        try:
            r = client.images.generate(model="gpt-image-1", prompt=prompt, size=size)
            data = base64.b64decode(r.data[0].b64_json)
            with open(path, 'wb') as f: f.write(data)
            print(f"  ✅ {filename} ({len(data):,} bytes)")
            time.sleep(12)
            return True
        except Exception as e:
            print(f"  ❌ attempt {attempt+1}: {e}")
            if attempt < retries: time.sleep(20)
    return False

results = {}

print("\n── Chapter images (1536×1024) ──")

results['ch1-cascade-arrival.png'] = gen(
    'ch1-cascade-arrival.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: awestruck, eyes wide, stepping through misty vines into an open clearing. "
    f"Before her: {SETTING_CASCADE}. "
    f"Dozens of {SPROCKETS} rush past in every direction, carrying lanterns and festival items. "
    f"{ELDER} stands tall in the foreground with silver-striped antennae, looking directly at Blaze. "
    f"Mood: wonder and chaos.",
    size="1536x1024"
)

results['ch2-festival-items.png'] = gen(
    'ch2-festival-items.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: focused and methodical, standing at a long table covered in "
    f"ribbon-flowers (pink, tied in bows) and glittering sparkle-stones. "
    f"She's counting and sorting items into groups. "
    f"{SPROCKETS} watch her eagerly. "
    f"{SETTING_CASCADE}. Warm festival light.",
    size="1536x1024"
)

results['ch3-tangle-bundles.png'] = gen(
    'ch3-tangle-bundles.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: crouching with intense curiosity, examining seven identical vine bundles "
    f"arranged in a perfect row near the waterfall. "
    f"{RIPPLE} stands beside her pointing excitedly. "
    f"The vine bundles are neat, deliberate, clearly not random. "
    f"In the misty background: the waterfall cascades. "
    f"{SETTING_CASCADE}. Slightly mysterious mood.",
    size="1536x1024"
)

results['ch4-elder-challenge.png'] = gen(
    'ch4-elder-challenge.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{ELDER} stands before {BLAZE} in a challenge pose — antennae raised, ceremonial robe billowing. "
    f"Between them: a long table with one hundred small festival items arranged in rows. "
    f"Other {SPROCKETS} watch from the sides. "
    f"{BLAZE}, expression: calm and confident, arms crossed. "
    f"{SETTING_CASCADE}. Dramatic challenge atmosphere.",
    size="1536x1024"
)

results['ch5-tangle-watching.png'] = gen(
    'ch5-tangle-watching.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. Evening light. "
    f"The festival of Cascade Clearing is underway — lanterns glowing, Sprockets celebrating. "
    f"{BLAZE} stands with {ELDER}, both looking satisfied. "
    f"At the very edge of the frame, half-hidden in jungle shadows: "
    f"the silhouette of something enormous made of vines, watching. "
    f"Its own vine bundles arranged in grouping patterns that mirror the festival lanterns. "
    f"{SETTING_CASCADE}. Mood: joy with mystery.",
    size="1536x1024"
)

print("\n── Question images (1024×1024) ──")

results['q1-lanterns.png'] = gen(
    'q1-lanterns.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 60 glowing festival lanterns arranged in 6 neat groups of 10, "
    f"hanging in rows in a jungle clearing. Each group clearly distinct. "
    f"Holographic '60 ÷ 10 = ?' in cyan above. "
    f"{SETTING_CASCADE}. Clean educational composition."
)

results['q2-ribbon-flowers.png'] = gen(
    'q2-ribbon-flowers.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 45 pink ribbon-flowers arranged in 5 groups of 9 on a wooden festival table. "
    f"Each group tied together. Holographic '45 ÷ 9 = ?' in cyan above. "
    f"{SETTING_CASCADE}. Clean educational composition."
)

results['q3-sparkle-stones.png'] = gen(
    'q3-sparkle-stones.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 72 small glittering sparkle-stones in 9 groups of 8 on a velvet display cloth. "
    f"Each group clearly separated. Holographic '72 ÷ 8 = ?' in cyan above. "
    f"{SETTING_CASCADE}. Clean educational composition."
)

results['q4-vine-bundles-12.png'] = gen(
    'q4-vine-bundles-12.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 84 vines arranged in 7 neat bundles of 12, each tied with a leaf. "
    f"Arranged in a perfect row on a jungle floor. "
    f"Holographic '84 ÷ 12 = ?' in cyan above. "
    f"{SETTING_JUNGLE}. Clean educational composition."
)

results['q5-vine-bundles-6.png'] = gen(
    'q5-vine-bundles-6.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 96 vines in 16 groups of 6, neatly arranged on a jungle floor. "
    f"Each group of 6 clearly distinct. Holographic '96 ÷ 6 = ?' in cyan above. "
    f"{SETTING_JUNGLE}. Clean educational composition."
)

results['q6-groups-of-4.png'] = gen(
    'q6-groups-of-4.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 100 small colourful festival items arranged in 25 groups of 4 on a long table. "
    f"Each group clearly separated. Holographic '100 ÷ 4 = ?' in cyan above. "
    f"{SETTING_CASCADE}. Clean educational composition."
)

results['q7-groups-of-5.png'] = gen(
    'q7-groups-of-5.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Split image: left side shows 25 groups of 4 items (labelled '÷4'), "
    f"right side shows 20 groups of 5 items (labelled '÷5'). "
    f"The left side clearly has more groups. "
    f"Holographic '100 ÷ 5 = ?' in cyan above. "
    f"{SETTING_CASCADE}. Clean educational comparison."
)

results['q8-berry-groups.png'] = gen(
    'q8-berry-groups.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 57 small round celebration berries arranged in 7 complete groups of 8, "
    f"with 1 berry set apart in a small glowing circle labelled 'remainder'. "
    f"Holographic '57 ÷ 8 = 7 r?' in cyan above. "
    f"{SETTING_CASCADE}. Clean educational composition."
)

results['q9-sparkle-groups.png'] = gen(
    'q9-sparkle-groups.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 156 sparkle-stones arranged in 13 groups of 12 on a long display table. "
    f"Each group clearly separated and identical. "
    f"Holographic '156 ÷ 12 = ?' in cyan above. "
    f"{SETTING_CASCADE}. Clean educational composition."
)

results['q10-boss-backwards.png'] = gen(
    'q10-boss-backwards.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 200 sparkle-stones arranged in 25 groups. Group size unknown — shown with a '?' hologram. "
    f"A large cyan holographic equation: '200 ÷ ? = 25'. "
    f"An arrow points from 200 to 25 with label 'work backwards'. "
    f"{SETTING_CASCADE}. Boss challenge feel, dramatic lighting."
)

results['cliffhanger-tangle-shadow.png'] = gen(
    'cliffhanger-tangle-shadow.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. Evening scene. "
    f"The festival of Cascade Clearing glows warmly in the background — lanterns lit, "
    f"{SPROCKETS} celebrating. "
    f"At the very edge of the jungle in the foreground shadows: "
    f"the silhouette of an enormous vine-creature, barely visible. "
    f"Around it: vine bundles arranged in the same grouping patterns as the festival lanterns — "
    f"groups of 6, groups of 10. "
    f"It is watching. Not threatening. Learning. "
    f"{SETTING_JUNGLE} at dusk. Mysterious and beautiful.",
    size="1536x1024"
)

print("\n─── COMPLETE ───")
passed = [k for k, v in results.items() if v]
failed = [k for k, v in results.items() if not v]
print(f"✅ {len(passed)}/17 images generated")
if failed:
    print(f"❌ Failed: {', '.join(failed)}")
