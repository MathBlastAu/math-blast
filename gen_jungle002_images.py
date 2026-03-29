#!/usr/bin/env python3
"""
Generate ALL 16 images for Jungle Issue 2 — "The Fernmoss Muddle"
Same pattern as gen_jungle001_images.py — locked character constants injected into every prompt.
"""
from openai import OpenAI
import base64, os, time

client = OpenAI()
DEST = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/issue002/'
os.makedirs(DEST, exist_ok=True)

# ── LOCKED CHARACTER & SETTING DEFINITIONS (identical to Issue 1) ───────────
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

THISTLE = (
    "one specific Sprocket named Thistle: same cobalt-blue skin, three thin antennae, "
    "large round expressive eyes, wearing a small white leaf apron, "
    "expression always worried or relieved, Disney Pixar CGI 3D animation style"
)

CURL = (
    "one tiny Sprocket named Curl: same cobalt-blue skin, three thin antennae, "
    "large round expressive eyes, clearly unwell — droopy antennae, pale blue tinge, "
    "lying on a soft leaf-bed, Disney Pixar CGI 3D animation style"
)

SETTING_FERNMOSS = (
    "lower-canopy jungle village called Fernmoss: built among enormous glowing blue-purple bioluminescent mushrooms, "
    "misty soft light, hanging moss, fireflies, warm blue-green glow, "
    "Disney Pixar CGI 3D animation style, rich colour, cinematic quality"
)

SETTING_JUNGLE = (
    "alien jungle canopy world: enormous ancient trees with platforms and rope bridges, "
    "bioluminescent blue-green plants glowing softly, "
    "warm golden light filtering through giant tropical leaves, "
    "fireflies drifting through the air, "
    "Disney Pixar CGI 3D animation style, rich colour, cinematic quality"
)

def gen(filename, prompt, size="1024x1024", retries=2):
    path = DEST + filename
    print(f"  ⏳ {filename} ...")
    for attempt in range(retries + 1):
        try:
            r = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size=size
            )
            data = base64.b64decode(r.data[0].b64_json)
            with open(path, 'wb') as f:
                f.write(data)
            print(f"  ✅ {filename} ({len(data):,} bytes)")
            time.sleep(12)
            return True
        except Exception as e:
            print(f"  ❌ attempt {attempt+1}: {e}")
            if attempt < retries:
                time.sleep(20)
    return False

results = {}

# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER IMAGES — 1536×1024
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Chapter images (1536×1024) ──")

results['ch1-fernmoss-arrival.png'] = gen(
    'ch1-fernmoss-arrival.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: alert and concerned, pushing through overgrown vines into a village. "
    f"{THISTLE} stands in the foreground holding a clipboard of records, antennae drooping with worry. "
    f"Small glowing medicine bottles scattered on a shelf behind Thistle. "
    f"{SETTING_FERNMOSS}. Mood: something is wrong here.",
    size="1536x1024"
)

results['ch2-food-store.png'] = gen(
    'ch2-food-store.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: focused and determined, kneeling beside large woven baskets of nuts and seeds, "
    f"counting items carefully. Her wrist device projects a glowing holographic tally. "
    f"In the background on a leaf-bed: {CURL}. "
    f"{SETTING_FERNMOSS}. Warm mushroom glow, medical-hut feel.",
    size="1536x1024"
)

results['ch3-counting-store.png'] = gen(
    'ch3-counting-store.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: methodical, sorting through wooden storage boxes on shelves "
    f"containing organised piles of seeds and leaves. "
    f"Her wrist device displays a running holographic tally. "
    f"Jungle canopy visible through gaps in the hut walls. "
    f"{SETTING_FERNMOSS}.",
    size="1536x1024"
)

results['ch4-vine-pattern.png'] = gen(
    'ch4-vine-pattern.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: crouching with narrowed eyes, intensely suspicious, "
    f"pointing at the jungle floor where several vines have been cut and arranged in neat groups of 6. "
    f"Large mysterious footprints visible between the groups. "
    f"{SETTING_JUNGLE}. Dappled light, slightly ominous mood.",
    size="1536x1024"
)

results['ch5-distribution-fixed.png'] = gen(
    'ch5-distribution-fixed.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: warm satisfied smile, arms crossed, standing to one side. "
    f"A group of 8 {SPROCKETS} each holding identical portions of colourful jungle food, "
    f"looking happy and relieved. {THISTLE} has antennae perked up with relief. "
    f"{CURL} visible sitting up on a leaf-bed looking better. "
    f"{SETTING_FERNMOSS}. Celebratory warm glow.",
    size="1536x1024"
)

# ══════════════════════════════════════════════════════════════════════════════
# QUESTION IMAGES — 1024×1024
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Question images (1024×1024) ──")

results['q1-medicine-doses.png'] = gen(
    'q1-medicine-doses.png',
    f"Disney Pixar CGI 3D animation. "
    f"A shelf of exactly 12 small glowing medicine bottles. "
    f"In front of the shelf stand exactly 4 {SPROCKETS}, each with empty hands outstretched. "
    f"The mismatch between 12 bottles and 4 Sprockets is visually obvious. "
    f"A holographic '36 ÷ 12 = ?' floats in cyan above. "
    f"{SETTING_FERNMOSS}."
)

results['q2-nut-baskets.png'] = gen(
    'q2-nut-baskets.png',
    f"Disney Pixar CGI 3D animation. "
    f"Exactly 48 round glowing nuts arranged in 8 equal piles of 6 on a woven mat. "
    f"Each pile is clearly distinct, same size. "
    f"Holographic '48 ÷ 8 = ?' in cyan above. "
    f"{SETTING_FERNMOSS}. Clean educational composition."
)

results['q3-sick-sprocket.png'] = gen(
    'q3-sick-sprocket.png',
    f"Disney Pixar CGI 3D animation. "
    f"{CURL} lying on a soft leaf-bed looking unwell, droopy antennae. "
    f"Beside the bed: one normal-sized glowing medicine cup labelled '9', "
    f"and beside it a much larger glowing cup labelled '×4 = ?'. "
    f"Warm sympathetic blue mushroom light. "
    f"{SETTING_FERNMOSS}."
)

results['q4-healing-leaves.png'] = gen(
    'q4-healing-leaves.png',
    f"Disney Pixar CGI 3D animation. "
    f"Exactly 56 bright green glowing healing leaves arranged in 7 equal groups of 8 "
    f"on a wooden jungle surface. Each group clearly separated. "
    f"Holographic '56 ÷ 7 = ?' in cyan above. "
    f"{SETTING_FERNMOSS}. Clean educational composition."
)

results['q5-seed-groups.png'] = gen(
    'q5-seed-groups.png',
    f"Disney Pixar CGI 3D animation. "
    f"Exactly 63 small round glowing seeds in 7 neat circular piles of 9 "
    f"on a jungle floor surface. Each pile clearly distinct. "
    f"Holographic '63 ÷ 9 = ?' in cyan above. "
    f"{SETTING_FERNMOSS}. Clean educational composition."
)

results['q6-vine-trips.png'] = gen(
    'q6-vine-trips.png',
    f"Disney Pixar CGI 3D animation. "
    f"Exactly 42 vines arranged in 7 groups of 6 on a jungle floor. "
    f"Between each group of vines: a pair of large mysterious creature footprints in the mud, "
    f"suggesting 7 separate trips. "
    f"Holographic '42 ÷ 6 = ?' in cyan above. "
    f"{SETTING_JUNGLE}. Slightly mysterious mood."
)

results['q7-vine-bundles.png'] = gen(
    'q7-vine-bundles.png',
    f"Disney Pixar CGI 3D animation. "
    f"Exactly 35 green vines in 5 neat bundles of 7, each bundle tied with a leaf. "
    f"Arranged clearly on a jungle floor surface. "
    f"Holographic '35 ÷ 5 = ?' in cyan above. "
    f"{SETTING_JUNGLE}. Clean educational composition."
)

results['q8-vine-trail-map.png'] = gen(
    'q8-vine-trail-map.png',
    f"Disney Pixar CGI 3D animation style illustrated map. "
    f"Top-down view of a hand-drawn jungle map on parchment. "
    f"A vine trail connects two tree villages. The trail is divided into exactly 9 equal sections "
    f"each labelled '8 km'. A creature footprint marks the start. "
    f"Warm parchment tones with jungle green accents. Holographic border in cyan. "
    f"Clean map illustration style."
)

results['q9-resource-share.png'] = gen(
    'q9-resource-share.png',
    f"Disney Pixar CGI 3D animation. "
    f"Exactly 81 colourful glowing jungle fruits and nuts arranged in 9 equal piles of 9 "
    f"on a large woven mat. Each pile identical in contents and size. "
    f"Holographic '81 ÷ 9 = ?' in cyan above. "
    f"{SETTING_FERNMOSS}. Clean educational composition."
)

results['q10-boss-fraction.png'] = gen(
    'q10-boss-fraction.png',
    f"Disney Pixar CGI 3D animation. "
    f"Exactly 9 glowing jungle food items displayed in a clear row. "
    f"6 of them glow bright gold (highlighted as three-quarters). "
    f"3 of them are dimmer/faded. "
    f"A holographic '¾ of 9 = ?' floats in cyan above with '÷4 then ×3' shown as steps. "
    f"{SETTING_FERNMOSS}. Clean educational boss-challenge feel."
)

results['cliffhanger-deep-root.png'] = gen(
    'cliffhanger-deep-root.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. Night scene. "
    f"Dark jungle. In the far background, enormous ancient twisted trees loom — the Deep Root. "
    f"In the foreground mud: a trail of massive five-toed creature footprints leads toward the ancient trees. "
    f"Bioluminescent green moss glows along the footprint edges. "
    f"No people or creatures visible — just the footprints and the looming trees. "
    f"{SETTING_JUNGLE} at night. Mysterious, beautiful, slightly foreboding.",
    size="1536x1024"
)

# ══════════════════════════════════════════════════════════════════════════════
print("\n─── COMPLETE ───")
passed = [k for k, v in results.items() if v]
failed = [k for k, v in results.items() if not v]
print(f"✅ {len(passed)}/16 images generated")
if failed:
    print(f"❌ Failed: {', '.join(failed)}")
