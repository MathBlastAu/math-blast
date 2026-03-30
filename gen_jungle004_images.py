#!/usr/bin/env python3
"""Jungle Issue 4 images — locked constants, same pattern as Issues 1-3."""
from openai import OpenAI
import base64, os, time

client = OpenAI()
DEST = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/issue004/'
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
    "large round expressive eyes, small stubby arms and legs, some wearing tiny leaf tunics or aprons, "
    "Disney Pixar CGI 3D animation style, same cobalt-blue skin in every image"
)
KEEPER = (
    "one specific Sprocket named Keeper Moss: same cobalt-blue skin, three thin antennae, "
    "large round expressive eyes, wearing a small scholarly robe made of pressed leaves, "
    "carrying a rolled-up scroll, expression always anxious and scholarly, "
    "Disney Pixar CGI 3D animation style"
)
SETTING = (
    "the Array Forest: an ancient sacred jungle grove where enormous trees grow in mathematically "
    "perfect rectangular rows and columns, dappled golden light through dense canopy, "
    "moss-covered ground, ancient and reverent atmosphere, "
    "Disney Pixar CGI 3D animation style, rich colour, cinematic quality"
)

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

results = {}
print("\n── Chapter images (1536×1024) ──")

results['ch1-array-forest-arrival.png'] = gen('ch1-array-forest-arrival.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression: determined and focused, stepping into {SETTING}. "
    f"Several tree rows are visibly disrupted, gaps where trees should be. "
    f"{KEEPER} stands at the entrance holding a large leaf scroll, antennae drooping with worry. "
    f"Mood: sacred but disturbed.", size="1536x1024")

results['ch2-checking-arrays.png'] = gen('ch2-checking-arrays.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE} and {KEEPER} walk between rows of trees in {SETTING}, "
    f"Blaze's wrist device glowing as she checks each row against Keeper's scroll. "
    f"In the foreground: vine bundles of exactly twelve, left on the ground. "
    f"Expression: methodical and increasingly curious.", size="1536x1024")

results['ch3-prestige-arrays.png'] = gen('ch3-prestige-arrays.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"The heart of {SETTING}: larger, older, more majestic trees in perfect rectangular arrays. "
    f"{BLAZE} kneels examining the base of one enormous tree, wrist device projecting a holographic grid. "
    f"{KEEPER} stands clutching scroll, expression deeply relieved. "
    f"Mood: ancient, reverent, discovery.", size="1536x1024")

results['ch4-tangle-array.png'] = gen('ch4-tangle-array.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"A clearing in {SETTING}. "
    f"On the ground: an extraordinary array of vines arranged in eleven neat bundles of twelve, "
    f"perfectly formed, clearly intentional. "
    f"{BLAZE} crouches nearby, expression: awe and realisation. "
    f"At the very edge of the frame in deep shadow: the outline of something enormous made of vines. "
    f"Mood: discovery and wonder.", size="1536x1024")

results['ch5-blaze-reaches-out.png'] = gen('ch5-blaze-reaches-out.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE} standing at the edge of a clearing in {SETTING}, arm extended, reaching out her hand. "
    f"Facing her: the enormous silhouette of Tangle, a creature made entirely of colourful vines, "
    f"just visible in the dappled light, not threatening but uncertain. "
    f"Between them on the ground: a small bundle of twelve vines. "
    f"Mood: tender, significant, a turning point.", size="1536x1024")

print("\n── Question images (1024×1024) ──")

results['q1-array-24.png'] = gen('q1-array-24.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A perfect rectangular array of exactly 24 small glowing trees: 4 rows of 6. "
    f"Each row clearly distinct. Holographic '24 divided by 4' label in cyan. "
    f"{SETTING}. Clean educational composition.")

results['q2-array-35.png'] = gen('q2-array-35.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A perfect rectangular array of exactly 35 small glowing trees: 5 rows of 7. "
    f"Each row clearly distinct. Holographic '35 divided by 5' label in cyan. "
    f"{SETTING}. Clean educational composition.")

results['q3-array-48.png'] = gen('q3-array-48.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A perfect rectangular array of exactly 48 small glowing trees: 6 rows of 8. "
    f"Each row clearly distinct. Holographic '48 divided by 6' label in cyan. "
    f"{SETTING}. Clean educational composition.")

results['q4-array-96.png'] = gen('q4-array-96.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A large rectangular array of exactly 96 ancient trees: 8 rows of 12. "
    f"Majestic and ancient. Holographic '96 divided by 8' label in cyan. "
    f"{SETTING}. Clean educational composition.")

results['q5-array-84.png'] = gen('q5-array-84.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A large rectangular array of exactly 84 ancient trees: 7 rows of 12. "
    f"Majestic and ancient. Holographic '84 divided by 7' label in cyan. "
    f"{SETTING}. Clean educational composition.")

results['q6-vine-array-132.png'] = gen('q6-vine-array-132.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 132 colourful vines arranged in 11 neat bundles of 12 on the forest floor. "
    f"Each bundle tied with a leaf. Holographic '132 divided by 11' label in cyan. "
    f"{SETTING}. Clean educational composition.")

results['q7-vine-rows-72.png'] = gen('q7-vine-rows-72.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 72 vines arranged in a rectangular grid: 6 rows of 12. "
    f"Each row clearly separated. Holographic '72 divided by 12 equals how many rows' label in cyan. "
    f"{SETTING}. Clean educational composition.")

results['q8-vine-rows-84.png'] = gen('q8-vine-rows-84.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 84 vines in a rectangular grid: 7 rows of 12. "
    f"The bottom row glows brighter, indicating it was just added. "
    f"Holographic '84 divided by 12 equals how many rows' label in cyan. "
    f"{SETTING}. Clean educational composition.")

results['q9-vine-rows-156.png'] = gen('q9-vine-rows-156.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly 156 vines in a rectangular grid: 13 rows of 12. "
    f"Each row clearly distinct. Holographic '156 divided by 12' label in cyan. "
    f"{SETTING}. Clean educational composition.")

results['q10-boss-array-168.png'] = gen('q10-boss-array-168.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. Boss challenge feel. "
    f"Exactly 168 colourful vines in a magnificent rectangular array: 14 rows of 12. "
    f"Dramatic golden light, impressive scale. "
    f"Holographic '168 divided by 12 equals how many rows' label in cyan, glowing. "
    f"{SETTING}. Epic educational composition.")

results['cliffhanger-tangle-gift.png'] = gen('cliffhanger-tangle-gift.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. Twilight, golden-green light. "
    f"{BLAZE} stands holding a small bundle of twelve vines. "
    f"Tangle, an enormous creature made of colourful vines, is moving away into the deep forest. "
    f"But it has stopped and turned its head to look back. "
    f"The moment feels significant, a connection just made. "
    f"{SETTING}. Tender, beautiful, mysterious.", size="1536x1024")

print("\n─── COMPLETE ───")
passed = [k for k, v in results.items() if v]
failed = [k for k, v in results.items() if not v]
print(f"✅ {len(passed)}/17 generated")
if failed: print(f"❌ Failed: {', '.join(failed)}")
