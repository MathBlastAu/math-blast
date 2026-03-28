from openai import OpenAI
import base64, os, time

client = OpenAI()
os.makedirs('/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle', exist_ok=True)

def generate(filename, prompt, size="1536x1024"):
    path = f'/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/{filename}'
    if os.path.exists(path):
        print(f"⏭️  {filename} already exists, skipping")
        return True
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size
        )
        img_data = base64.b64decode(response.data[0].b64_json)
        with open(path, 'wb') as f:
            f.write(img_data)
        print(f"✅ {filename}")
        time.sleep(12)
        return True
    except Exception as e:
        print(f"❌ {filename}: {e}")
        return False

results = {}

results['ch1-crash-landing.png'] = generate(
    'ch1-crash-landing.png',
    "Disney Pixar style illustration. A 10-year-old girl named Blaze — short dark hair, warm olive skin, teal/cyan jumpsuit with purple panels and a lightning bolt badge, glowing cyan wrist device — swings on a jungle vine that is snapping. She's falling gracefully into a lush alien jungle canopy. Enormous ancient trees, glowing blue-green plants, fireflies, golden light filtering through leaves. Below her, tiny bright blue alien creatures (Sprockets) with three antennae look up in surprise. Wide cinematic scene, vibrant colours, adventure and wonder."
)

results['ch2-berry-harvest.png'] = generate(
    'ch2-berry-harvest.png',
    "Disney Pixar style illustration. Blaze (10-year-old girl, short dark hair, olive skin, teal jumpsuit with purple panels and lightning bolt badge, cyan wrist device glowing) kneels on a giant tree platform surrounded by baskets of glowing multicoloured berries. She's sorting them carefully into groups, her wrist device projecting a holographic division equation. Tiny bright blue Sprocket aliens (three antennae) watch with curious expressions. Lush jungle canopy background with golden light, alien plants, and fireflies."
)

results['ch3-missing-doz.png'] = generate(
    'ch3-missing-doz.png',
    "Disney Pixar style illustration. Blaze (10-year-old girl, teal jumpsuit with purple accents, lightning bolt badge, olive skin, dark short hair, glowing cyan wrist device) stands at the edge of a jungle tree platform, staring at a massive tangle of colourful vines blocking a pathway. A tiny blue Sprocket alien (three antennae, bright blue, small) stands beside her pointing at the vines, looking worried. Mysterious jungle atmosphere, deep shadows, glowing plants, sense of something strange and large having been here."
)

results['ch4-feast-begins.png'] = generate(
    'ch4-feast-begins.png',
    "Disney Pixar style illustration. A magical jungle feast scene on a giant tree platform high in the canopy. Blaze (10-year-old girl, teal jumpsuit with purple panels, lightning bolt badge, olive skin, dark hair, cyan wrist device) stands confidently at the centre of long wooden tables covered in glowing jungle foods — fire-nuts, bark-bread, glowing berries. Dozens of tiny bright blue Sprocket aliens with three antennae celebrate around her. Warm golden light, fireflies, lush jungle canopy below."
)

results['ch5-tangle-footprint.png'] = generate(
    'ch5-tangle-footprint.png',
    "Disney Pixar style illustration. Night scene. Blaze (10-year-old girl, teal jumpsuit with purple panels, lightning bolt badge, olive skin, dark short hair, cyan wrist device illuminating her face) crouches at the edge of a jungle tree platform, shining light from her wrist device onto an enormous mysterious footprint in the bark — far larger than a human foot, with strange pattern markings. Deep jungle night around her, bioluminescent plants glowing blue-green, sense of mystery and adventure."
)

print("\n=== SUMMARY ===")
for name, ok in results.items():
    print(f"{'✅' if ok else '❌'} {name}")
