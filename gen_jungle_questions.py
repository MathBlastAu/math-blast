from openai import OpenAI
import base64, os, time

client = OpenAI()
DEST = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/'

os.makedirs(DEST, exist_ok=True)

BLAZE = "10-year-old girl named Blaze, short practical dark hair, warm olive-tan skin, teal/cyan fitted jumpsuit with purple accent panels, yellow lightning bolt badge on chest, glowing cyan holographic device on left wrist, confident posture, slight smirk, Disney Pixar CGI animation style"
SPROCKET = "tiny cobalt-blue alien creature, smooth round head, exactly three thin antennae on top of head, large expressive eyes, small stubby arms, Disney Pixar CGI style"
SETTING = "alien jungle canopy, giant ancient trees, glowing bioluminescent plants, warm golden light through leaves, fireflies, wooden tree platforms"

def gen(filename, prompt):
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )
        img_data = base64.b64decode(response.data[0].b64_json)
        with open(DEST + filename, 'wb') as f:
            f.write(img_data)
        print(f"✅ {filename}")
        time.sleep(13)
    except Exception as e:
        print(f"❌ {filename}: {e}")

images = [
    ("q1-welcome-berries.png", f"Disney Pixar CGI animation style. {BLAZE} holds a woven basket containing exactly 12 small glowing round berries. Three {SPROCKET}s stand in front of her with hands outstretched eagerly. Her wrist device projects a holographic '12 ÷ 3 = ?' display in glowing cyan. {SETTING}, warm golden light, magical atmosphere. Educational illustration."),
    ("q2-glow-berries.png", f"Disney Pixar CGI animation style. {BLAZE} points at 24 glowing round berries arranged in exactly 4 equal groups of 6 on a large tropical leaf on a wooden jungle platform. Her wrist device shows a holographic '24 ÷ 4 = ?'. Four small woven baskets sit nearby. {SETTING}. Clear and educational."),
    ("q3-moon-figs.png", f"Disney Pixar CGI animation style. {BLAZE} stands beside a wooden jungle table. On the table: exactly 18 small crescent-shaped glowing golden fruit arranged in 6 neat rows of 3 each. Her wrist device projects '18 ÷ 6 = ?' and '6 × ? = 18' in holographic cyan text. {SETTING}. Clear, educational illustration."),
    ("q4-healing-pouches.png", f"Disney Pixar CGI animation style. A {SPROCKET} wearing a tiny leaf apron (the medic) holds 20 small glowing green healing leaves. To the side: exactly 4 small leaf pouches, each containing 5 leaves. {BLAZE} stands nearby, her wrist device showing '20 ÷ 5 = ? pouches'. {SETTING}, warm dappled light."),
    ("q5-leaf-groups.png", f"Disney Pixar CGI animation style. {BLAZE} crouches on a wooden jungle platform beside exactly 15 green leaves clearly arranged in 5 separate groups of 3. Her wrist device projects a glowing holographic box showing the fact family: '15÷3=5 / 15÷5=3 / 3×5=15 / 5×3=15'. {SETTING}. Clear visual grouping, educational."),
    ("q6-fire-nuts.png", f"Disney Pixar CGI animation style. Exactly 9 {SPROCKET}s sit in a row on a feast platform, each with a small empty bowl. A pile of 36 small glowing orange fire-nuts (like tiny fiery pebbles) sits in the centre of the table. {BLAZE} stands to one side, her wrist device showing '36 ÷ 9 = ?'. {SETTING}, warm orange glow."),
    ("q7-bark-bread.png", f"Disney Pixar CGI animation style. Exactly 32 small flat round pieces of bark-bread are arranged in 4 rows of 8 on a giant leaf. Exactly 8 {SPROCKET}s stand waiting beside it. {BLAZE} points at the arrangement, her wrist device showing '32 ÷ 8 = 4' with a glowing highlight box showing 'Same as 36÷9! Both = 4'. {SETTING}."),
    ("q8-remainder.png", f"Disney Pixar CGI animation style. {BLAZE} looks curiously at a wooden platform showing 24 berries: 5 groups of 4 are neatly arranged, but 4 extra berries sit alone in the middle circled by a glowing holographic ring. A {SPROCKET} wearing a leaf apron looks hopefully at the leftover berries. Wrist device shows '24 ÷ 5 = 4 remainder 4'. {SETTING}, problem-solving mood."),
    ("q9-vine-bundles.png", f"Disney Pixar CGI animation style. {BLAZE} crouches at the edge of a jungle platform at night, her wrist device casting cyan light. She examines 28 cut vines tied into exactly 7 neat bundles of 4 vines each laid out in a row. Her expression is focused and suspicious. Wrist device shows '28 ÷ 7 = ?'. Dark bioluminescent jungle night, mysterious atmosphere."),
    ("q10-boss-round.png", f"Disney Pixar CGI animation style. A {SPROCKET} wearing a tiny leaf crown (Chief Pip) gestures grandly at a large feast platform with 45 food items divided into 6 areas each marked with a small leaf flag — exactly 7 items in each area and 3 leftover items to one side. {BLAZE} stands beside Chief Pip, her wrist device showing '45 ÷ 6 = 7 remainder 3'. {SETTING}, dramatic big-challenge atmosphere."),
]

for filename, prompt in images:
    gen(filename, prompt)

print("Done!")
