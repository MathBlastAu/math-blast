from openai import OpenAI
import base64, os, time

client = OpenAI()
DEST = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/'
os.makedirs(DEST, exist_ok=True)

B = "10-year-old girl named Blaze: short practical dark hair, warm olive-tan skin, teal/cyan fitted jumpsuit with purple accent panels on shoulders and sides, yellow lightning bolt badge on left chest, glowing cyan holographic device strapped to left wrist, Disney Pixar CGI animation style, vibrant colours"
S = "tiny cobalt-blue alien creatures about knee-height, smooth round heads, exactly three thin antennae sprouting from the top of their heads, large round expressive eyes, small stubby arms and legs, Disney Pixar CGI style"
SET = "alien jungle canopy setting, enormous ancient trees with glowing bioluminescent blue-green plants, warm golden light filtering through giant leaves, fireflies floating in the air, wooden platforms and rope bridges built between trees"

def gen(filename, prompt, size="1024x1024"):
    print(f"⏳ Generating {filename}...")
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size
        )
        img_data = base64.b64decode(response.data[0].b64_json)
        with open(DEST + filename, 'wb') as f:
            f.write(img_data)
        print(f"✅ {filename}")
        time.sleep(13)
        return True
    except Exception as e:
        print(f"❌ FAILED {filename}: {e}")
        return False

results = {}

results['q4-healing-pouches.png'] = gen(
    'q4-healing-pouches.png',
    f"Disney Pixar CGI animation style. {B}, expression: arms crossed, small satisfied smile, standing nearby as a {S} wearing a tiny leaf apron (the medic) holds 20 small glowing green healing leaves. Beside the medic: exactly 4 small leaf pouches each containing 5 leaves. Her wrist device shows '20 ÷ 5 = ? pouches'. {SET}, warm dappled light."
)

results['q5-leaf-groups.png'] = gen(
    'q5-leaf-groups.png',
    f"Disney Pixar CGI animation style. {B}, expression: crouched down low, peering closely at the ground with intense focus, beside exactly 15 green leaves clearly arranged in 5 separate groups of 3 on a wooden jungle platform. Her wrist device projects a glowing holographic box showing the fact family: '15÷3=5 / 15÷5=3 / 3×5=15 / 5×3=15'. {SET}."
)

results['q6-fire-nuts.png'] = gen(
    'q6-fire-nuts.png',
    f"Disney Pixar CGI animation style. {B}, expression: head tilted with finger to chin in thoughtful puzzlement, standing beside a feast table where exactly 9 {S} sit in a row each with a small bowl. A pile of 36 small glowing orange fire-nuts sits in the centre. Her wrist device shows '36 ÷ 9 = ?'. {SET}, warm orange glow from the fire-nuts."
)

results['q7-bark-bread.png'] = gen(
    'q7-bark-bread.png',
    f"Disney Pixar CGI animation style. {B}, expression: eyebrows raised in surprised delight, a small gasp expression, pointing at exactly 32 small flat round pieces of bark-bread arranged in 4 rows of 8 on a giant leaf. Exactly 8 {S} stand waiting beside it. Her wrist device shows '32 ÷ 8 = 4' with a glowing highlight 'Same as 36÷9! Both = 4!'. {SET}."
)

results['q8-remainder.png'] = gen(
    'q8-remainder.png',
    f"Disney Pixar CGI animation style. {B}, expression: head tilted to one side thinking carefully, kneeling beside a wooden platform showing 24 berries arranged in 5 groups of 4, with 4 extra berries sitting alone in the middle inside a glowing holographic ring. A {S} wearing a leaf apron looks hopefully at the leftover berries. Her wrist device shows '24 ÷ 5 = 4 remainder 4'. {SET}."
)

results['q9-vine-bundles.png'] = gen(
    'q9-vine-bundles.png',
    f"Disney Pixar CGI animation style. Night scene. {B}, expression: crouching with a cautious suspicious look, eyebrow raised, leaning over to examine 28 cut vines tied into exactly 7 neat bundles of 4 laid out in a row on a dark jungle platform. Her cyan wrist device casts blue light on her face. Wrist device shows '28 ÷ 7 = ?'. {SET} at night, bioluminescent plants glowing blue-green, mysterious mood."
)

results['q10-boss-round.png'] = gen(
    'q10-boss-round.png',
    f"Disney Pixar CGI animation style. {B}, expression: standing tall and brave in a protective stance, beside a {S} wearing a tiny leaf crown (Chief Pip) who gestures grandly at a large feast platform. The platform has 45 food items divided into 6 areas each marked with a small leaf flag — exactly 7 items in each area, with 3 items set aside. Her wrist device shows '45 ÷ 6 = 7 remainder 3'. {SET}, dramatic lighting, big-challenge atmosphere."
)

print("\n─── REMAINING BATCH COMPLETE ───")
passed = [k for k, v in results.items() if v]
failed = [k for k, v in results.items() if not v]
print(f"✅ Success: {len(passed)}/7")
if failed:
    print(f"❌ Failed:  {', '.join(failed)}")
else:
    print("All remaining images done!")
