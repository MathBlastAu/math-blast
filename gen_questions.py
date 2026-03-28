#!/usr/bin/env python3
from openai import OpenAI
from PIL import Image
import base64, os, time, io

client = OpenAI()

ref = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/ch1-crash-landing.png'
out_dir = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/'

def load_rgba_png(path):
    """Load image, convert to RGBA, resize to 1024x1024, return as PNG bytes."""
    img = Image.open(path).convert("RGBA").resize((1024, 1024))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def generate_with_ref(filename, prompt, ref_path, size="1024x1024"):
    """Use images.edit with reference for character consistency."""
    ref_bytes = load_rgba_png(ref_path)
    image_tuple = ('reference.png', ref_bytes, 'image/png')
    
    response = client.images.edit(
        model="dall-e-2",
        image=image_tuple,
        prompt=prompt,
        size=size,
        response_format="b64_json"
    )
    img_data = base64.b64decode(response.data[0].b64_json)
    path = os.path.join(out_dir, filename)
    with open(path, 'wb') as f:
        f.write(img_data)
    print(f"✅ {filename}")
    time.sleep(13)

questions = [
    ("q1-welcome-berries.png", "Disney Pixar style. Keep the girl character exactly as shown in the reference image. She holds a basket of exactly 12 small glowing round berries. Three tiny bright blue alien creatures with three antennae each stand in front of her, hands outstretched. Her glowing cyan wrist device projects a holographic '12 ÷ 3 = ?' display. Warm jungle canopy setting, golden light, fireflies, magical atmosphere."),
    ("q2-glow-berries.png", "Disney Pixar style. Close-up scene in a jungle canopy. 24 glowing round berries are arranged in exactly 4 equal groups of 6 on a large tropical leaf. The girl from the reference image (teal jumpsuit, lightning bolt badge) points at the groups from the side, her glowing cyan wrist device showing '24 ÷ 4 = ?'. 4 small woven baskets sit nearby. Warm golden light, jungle background."),
    ("q3-moon-figs.png", "Disney Pixar style. A wooden table in the jungle canopy. Exactly 18 small crescent-shaped glowing fruit (moon-figs) are arranged in 6 neat rows of 3 each. The girl from the reference image stands beside the table, her cyan wrist device projecting a holographic display showing '18 ÷ 6 = ?' and '6 × ? = 18'. Clear, educational, warm jungle colours."),
    ("q4-healing-pouches.png", "Disney Pixar style. A tiny bright blue alien with exactly three antennae, wearing a small leaf apron, holds 20 small glowing green healing leaves. Nearby are exactly 4 small pouches, each containing 5 leaves. The girl from the reference image stands nearby, her cyan wrist device showing '20 ÷ 5 = ? pouches'. Jungle canopy setting, warm dappled light."),
    ("q5-leaf-groups.png", "Disney Pixar style. On a jungle platform, exactly 15 leaves are clearly arranged in 5 separate groups of 3. The girl from the reference image crouches beside them, her cyan wrist device projecting a glowing holographic fact family: '15÷3=5, 15÷5=3, 3×5=15, 5×3=15'. Clear visual grouping, warm jungle colours."),
    ("q6-fire-nuts.png", "Disney Pixar style. A jungle feast platform. Exactly 9 tiny bright blue alien creatures with three antennae each sit in a row, each with a small bowl in front of them. A pile of 36 small glowing orange fire-nuts sits in the centre. The girl from the reference image stands to one side, her cyan wrist device showing '36 ÷ 9 = ?'. Warm orange glow, jungle canopy background."),
    ("q7-bark-bread.png", "Disney Pixar style. Exactly 32 small flat pieces of bark-bread arranged in neat rows on a giant leaf. Exactly 8 tiny blue alien creatures with three antennae wait beside it. The girl from the reference image points at them, her cyan wrist device showing '32 ÷ 8 = ?' alongside '36 ÷ 9 = 4' with a highlight showing 'Both = 4!'. Warm jungle setting."),
    ("q8-remainder.png", "Disney Pixar style. The girl from the reference image looks curiously at 24 berries being divided: 5 equal groups of 4 are arranged, with 4 leftover berries sitting alone in the middle. A tiny blue alien with three antennae (wearing a leaf apron, the medic) looks hopefully at the leftover berries. The girl's wrist device shows '24 ÷ 5 = 4 remainder 4'. Warm jungle colours, curious and problem-solving atmosphere."),
    ("q9-vine-bundles.png", "Disney Pixar style. The girl from the reference image crouches at the edge of a dark jungle platform, examining 28 cut vines that have been tied into exactly 7 neat bundles of 4 vines each. Her expression is focused and slightly suspicious. Her cyan wrist device glows showing '28 ÷ 7 = ?'. Dark moody jungle background, bioluminescent plants, mysterious atmosphere."),
    ("q10-boss-round.png", "Disney Pixar style. A tiny bright blue alien with three antennae and a small leaf crown (Chief Pip) stands before a large platform with 45 food items spread across it, gesturing to 6 areas each marked with a small leaf flag. The girl from the reference image stands beside him, her cyan wrist device showing '45 ÷ 6 = 7 remainder 3'. 7 items are visible in each of the 6 areas, with 3 items leftover to one side. Warm jungle setting, big-challenge atmosphere."),
]

failed = []
for filename, prompt in questions:
    try:
        print(f"Generating {filename}...")
        generate_with_ref(filename, prompt, ref)
    except Exception as e:
        print(f"❌ {filename}: {e}")
        failed.append((filename, str(e)))

print("\n=== DONE ===")
if failed:
    print("Failed:")
    for f, e in failed:
        print(f"  {f}: {e}")
else:
    print("All 10 images generated successfully!")
