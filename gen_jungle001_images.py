#!/usr/bin/env python3
"""
Regenerate ALL 15 images for Jungle Issue 1 in a single consistent batch.
Blaze character, Sprocket design and setting are defined ONCE and reused everywhere.
"""
from openai import OpenAI
import base64, os, time

client = OpenAI()
DEST = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/'
os.makedirs(DEST, exist_ok=True)

# ── LOCKED CHARACTER & SETTING DEFINITIONS ─────────────────────────────────
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

SETTING = (
    "alien jungle canopy world: enormous ancient trees with platforms and rope bridges, "
    "bioluminescent blue-green plants glowing softly, "
    "warm golden light filtering through giant tropical leaves, "
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
# CHAPTER IMAGES — 1536×1024 (wide cinematic)
# ══════════════════════════════════════════════════════════════════════════════

print("\n── Chapter images (1536×1024) ──")

results['ch1-crash-landing.png'] = gen(
    'ch1-crash-landing.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: eyes wide with wonder and surprise, mouth open in an O shape, "
    f"swinging wildly on a snapping jungle vine, arms flung out, body mid-swing. "
    f"Below her, several {SPROCKETS} look up in shock with arms raised. "
    f"{SETTING}. Adventure and wonder mood.",
    size="1536x1024"
)

results['ch2-berry-harvest.png'] = gen(
    'ch2-berry-harvest.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: focused and determined, eyes narrowed in concentration, "
    f"kneeling on a tree platform sorting glowing multicoloured berries into equal groups on a large leaf. "
    f"Several {SPROCKETS} watch her curiously. Her wrist device projects a glowing holographic division equation. "
    f"{SETTING}. Two large woven baskets nearby.",
    size="1536x1024"
)

results['ch3-missing-doz.png'] = gen(
    'ch3-missing-doz.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: cautious and suspicious, eyebrow raised, leaning back slightly, "
    f"standing at the edge of a tree platform staring at a massive colourful tangle of vines blocking the pathway. "
    f"One {SPROCKETS} stands beside her pointing at the vines in panic. "
    f"{SETTING}. Deep mysterious shadows beyond the vine tangle.",
    size="1536x1024"
)

results['ch4-feast-begins.png'] = gen(
    'ch4-feast-begins.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: triumphant grin, both arms raised in celebration, "
    f"standing at the centre of a magical jungle feast on a wide treetop platform. "
    f"Long wooden tables covered in glowing jungle foods. "
    f"Dozens of {SPROCKETS} celebrate around her, dancing and cheering. "
    f"{SETTING}. Warm golden firefly light, festive and joyful.",
    size="1536x1024"
)

results['ch5-tangle-footprint.png'] = gen(
    'ch5-tangle-footprint.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. Night scene. "
    f"{BLAZE}, expression: alert and scanning, standing upright, "
    f"her glowing cyan wrist device held out illuminating a massive mysterious footprint in the soft mud — "
    f"far larger than a human foot, with deep swirling impressions. "
    f"{SETTING} at night. Deep shadows, bioluminescent plants glowing blue-green. Eerie and mysterious mood.",
    size="1536x1024"
)

# ══════════════════════════════════════════════════════════════════════════════
# QUESTION IMAGES — 1024×1024
# ══════════════════════════════════════════════════════════════════════════════

print("\n── Question images (1024×1024) ──")

results['q1-welcome-berries.png'] = gen(
    'q1-welcome-berries.png',
    f"Disney Pixar CGI 3D animation. "
    f"{BLAZE}, expression: confident, one hand on hip, slight knowing smirk, "
    f"holding a woven basket with exactly 12 small round glowing berries inside. "
    f"Exactly 3 {SPROCKETS} stand before her with arms outstretched eagerly. "
    f"Her wrist device projects a holographic '12 ÷ 3 = ?' in glowing cyan. "
    f"{SETTING}. Warm welcoming light."
)

results['q2-glow-berries.png'] = gen(
    'q2-glow-berries.png',
    f"Disney Pixar CGI 3D animation. "
    f"{BLAZE}, expression: serious instructional face, arm extended pointing, "
    f"indicating exactly 24 glowing round berries arranged into 4 distinct equal groups of 6 on a giant leaf. "
    f"Four small woven baskets nearby. "
    f"Her wrist device displays holographic '24 ÷ 4 = ?'. "
    f"{SETTING}."
)

results['q3-moon-figs.png'] = gen(
    'q3-moon-figs.png',
    f"Disney Pixar CGI 3D animation. "
    f"{BLAZE}, expression: clever 'aha!' face, finger raised in realisation, eyes bright, "
    f"beside a wooden table displaying exactly 18 small crescent-shaped glowing golden fruit "
    f"in 6 neat equal rows of 3. "
    f"Her wrist device shows '18 ÷ 6 = ?' holographic display. "
    f"{SETTING}."
)

results['q4-healing-pouches.png'] = gen(
    'q4-healing-pouches.png',
    f"Disney Pixar CGI 3D animation. "
    f"{BLAZE}, expression: arms crossed, small satisfied smile, watching approvingly. "
    f"One {SPROCKETS} wearing a tiny leaf apron (the medic) holds exactly 20 small glowing green healing leaves. "
    f"Beside the medic: 4 small leaf pouches clearly containing 5 leaves each. "
    f"Her wrist device shows '20 ÷ 5 = ?' in cyan holographic text. "
    f"{SETTING}."
)

results['q5-leaf-groups.png'] = gen(
    'q5-leaf-groups.png',
    f"Disney Pixar CGI 3D animation. "
    f"{BLAZE}, expression: crouched low, peering closely with intense concentration, "
    f"examining exactly 15 green leaves clearly arranged in 5 separate groups of 3 on a wooden jungle platform. "
    f"Her wrist device projects a glowing holographic fact family: '15÷3=5, 15÷5=3, 3×5=15, 5×3=15'. "
    f"{SETTING}."
)

results['q6-fire-nuts.png'] = gen(
    'q6-fire-nuts.png',
    f"Disney Pixar CGI 3D animation. "
    f"{BLAZE}, expression: head tilted, finger to chin, thoughtful puzzlement, "
    f"standing beside a feast table where exactly 9 {SPROCKETS} sit in a row, each with an empty bowl. "
    f"A pile of 36 small glowing orange fire-nuts sits in the centre of the table. "
    f"Her wrist device shows '36 ÷ 9 = ?' in warm orange holographic glow. "
    f"{SETTING}."
)

results['q7-bark-bread.png'] = gen(
    'q7-bark-bread.png',
    f"Disney Pixar CGI 3D animation. "
    f"{BLAZE}, expression: eyebrows raised in surprised delight, small gasp, pointing excitedly, "
    f"indicating exactly 32 small flat round pieces of bark-bread in neat rows on a leaf. "
    f"Exactly 8 {SPROCKETS} stand waiting beside them. "
    f"Her wrist device shows '32 ÷ 8 = 4' with a second line 'Same as 36÷9 = 4!' glowing in cyan. "
    f"{SETTING}."
)

results['q8-remainder.png'] = gen(
    'q8-remainder.png',
    f"Disney Pixar CGI 3D animation. "
    f"{BLAZE}, expression: tilting head thoughtfully, looking curious and careful, kneeling down, "
    f"beside a wooden platform showing exactly 24 berries divided into 5 groups of 4 "
    f"with 4 extra berries set aside inside a glowing holographic ring labelled 'remainder'. "
    f"One {SPROCKETS} wearing a leaf apron looks hopefully at the leftover berries. "
    f"Her wrist device shows '24 ÷ 5 = 4 r4'. "
    f"{SETTING}."
)

results['q9-vine-bundles.png'] = gen(
    'q9-vine-bundles.png',
    f"Disney Pixar CGI 3D animation. Night scene. "
    f"{BLAZE}, expression: crouching with a cautious suspicious narrowed look, "
    f"examining exactly 28 vines tied into 7 neat equal bundles of 4 laid in a row on a dark jungle platform. "
    f"Her cyan wrist device casts blue light on her face and shows '28 ÷ 7 = ?'. "
    f"{SETTING} at night. Bioluminescent plants glowing. Mysterious, tense mood."
)

results['q10-boss-round.png'] = gen(
    'q10-boss-round.png',
    f"Disney Pixar CGI 3D animation. "
    f"{BLAZE}, expression: standing tall and confident in a heroic stance, "
    f"beside one {SPROCKETS} wearing a tiny leaf crown (Chief Pip) gesturing grandly. "
    f"A feast platform in front of them divided into 6 areas each containing exactly 7 food items, "
    f"with 3 separate items set aside in a small glowing circle. "
    f"Her wrist device shows '45 ÷ 6 = 7 remainder 3' in bold holographic text. "
    f"{SETTING}. Dramatic warm lighting, big final-challenge atmosphere."
)

# ══════════════════════════════════════════════════════════════════════════════
print("\n─── COMPLETE ───")
passed = [k for k,v in results.items() if v]
failed = [k for k,v in results.items() if not v]
print(f"✅ {len(passed)}/15 images generated")
if failed:
    print(f"❌ Failed: {', '.join(failed)}")
