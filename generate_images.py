#!/usr/bin/env python3
import os
import base64
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

OUTPUT_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PHANTOM = (
    "The Fraction Phantom: a tall, slender humanoid silhouette made entirely of glowing translucent cyan-blue light. "
    "Its body is composed of floating glowing horizontal bars with numerals above and below each bar — they drift and rearrange "
    "slowly like a living equation. No face, just a faint blue glow where eyes would be. Wears no clothing — the glowing bars ARE its form."
)

STYLE = "Pixar-style 3D CGI, dark moody lighting, cyan rim light, deep navy shadows, volumetric haze, cinematic composition."

JAKE = (
    "Jake: 10-year-old boy, short messy brown hair, bright green eyes, freckles, "
    "orange space suit with silver trim, blue visor helmet, red rocket patch."
)

images = [
    {
        "filename": "ch5-phantom-appears.png",
        "prompt": (
            f"{PHANTOM} "
            "The Fraction Phantom flickers to life as a hologram above a space station communications panel — "
            "a flat glowing console with buttons and screens in a dark, metallic deep-space interior. "
            f"{JAKE} Jake stands nearby in his orange spacesuit, staring at the Phantom with wide eyes and open mouth. "
            "The Phantom hovers calmly and precisely above the panel. Holographic blue light radiates from it. "
            f"{STYLE}"
        )
    },
    {
        "filename": "ch3-issue003.png",
        "prompt": (
            f"{PHANTOM} "
            "The Fraction Phantom appears dramatically at a bustling asteroid market space station — "
            "colourful market stalls line a curved space-station corridor, vendors and alien traders visible, "
            "price tags displayed on glowing signs above goods. "
            f"{JAKE} Jake spots the Phantom moving between market stalls, looking alert and surprised. "
            "The Phantom glows brightly against the vivid, busy market backdrop. "
            f"{STYLE}"
        )
    },
    {
        "filename": "cliffhanger-issue004.png",
        "prompt": (
            f"{PHANTOM} "
            "The Fraction Phantom appears as a holographic message on a space station intercom screen mounted on a dark corridor wall. "
            "The holographic Phantom stands on the screen, one arm outstretched, pointing directly toward the viewer. "
            "Dramatic blue glow fills the dark station corridor. Shadows are deep. Tension is high. "
            f"{JAKE} Jake stands in the corridor looking at the screen, expression alarmed. "
            f"{STYLE}"
        )
    },
    {
        "filename": "ch3-issue006.png",
        "prompt": (
            f"{PHANTOM} "
            "Jake and the Fraction Phantom face each other in debate inside the Fraction Core — "
            "a pulsing spherical chamber made entirely of light, with glowing curved walls radiating energy. "
            f"{JAKE} Jake gestures with both hands making an argument, expression passionate. "
            "The Fraction Phantom stands calmly opposite, glowing bars drifting across its body. "
            "Two glowing rectangular bar diagrams float in the air between them, each representing a different sized spaceship. "
            f"{STYLE}"
        )
    },
    {
        "filename": "cliffhanger-issue006.png",
        "prompt": (
            f"{PHANTOM} "
            "The Fraction Phantom stands alone inside the Fraction Core — a breathtaking pulsing sphere of light "
            "deep in the Zephyr Nebula. The Phantom pauses in a contemplative pose, looking inward. "
            "Glowing number lines radiate outward from the sphere walls like spokes of light. "
            "Nebula gas and stars are visible beyond the sphere. Dramatic wide shot. "
            f"{STYLE}"
        )
    },
    {
        "filename": "ch1-issue007.png",
        "prompt": (
            f"{PHANTOM} "
            f"{JAKE} Jake stands confidently before the Fraction Phantom inside the Fraction Core — "
            "a pulsing spherical chamber of light. Jake holds up a glowing rectangular bar diagram showing "
            "two spaceships of different sizes side by side. The Fraction Phantom observes attentively, "
            "leaning slightly forward. Glowing numeral-and-bar elements float around them. "
            f"{STYLE}"
        )
    },
    {
        "filename": "ch2-issue007.png",
        "prompt": (
            f"{PHANTOM} "
            "The Fraction Phantom projects a large holographic display — a glowing data table "
            "showing rows and columns with ship names, numerals, and glowing bar diagrams representing "
            "fractions taken from various spaceships. "
            f"{JAKE} Jake stands nearby studying the holographic records carefully, brow furrowed in concentration. "
            "The Phantom stands beside the projection, looking at its own data with a neutral pose. "
            f"{STYLE}"
        )
    },
    {
        "filename": "ch3-issue007.png",
        "prompt": (
            f"{PHANTOM} "
            "The Fraction Phantom works at a glowing holographic workstation inside the Fraction Core — "
            "a pulsing spherical chamber of light. The Phantom's hands interact with floating glowing diagrams "
            "and bar model visuals swirling around it as it redesigns its fairness system. "
            f"{JAKE} Jake watches from nearby, expression hopeful and curious. "
            f"{STYLE}"
        )
    },
    {
        "filename": "ch5-issue007.png",
        "prompt": (
            f"{PHANTOM} "
            "The Fraction Phantom stands tall in the centre of the Fraction Core, arms raised wide, "
            "broadcasting a golden repair signal — warm golden light radiating outward in waves through the nebula. "
            f"{JAKE} Jake stands beside the Phantom, smiling broadly, holding a gold star medal up in one hand. "
            "Triumphant scene. Warm gold and cyan light mix beautifully. The atmosphere is celebratory and uplifting. "
            f"{STYLE}"
        )
    },
    {
        "filename": "cliffhanger-issue007.png",
        "prompt": (
            f"{PHANTOM} "
            "The Fraction Phantom is transformed — now the Fraction Keeper. Same tall slender silhouette, "
            "same glowing bars-and-numerals body — but now radiating warm golden light alongside the cyan blue. "
            "Gold and cyan glow together from its form. It stands proudly in the centre of the nebula, "
            "stars and swirling light patterns all around it. Majestic, hopeful, transformed. "
            "Wide epic shot showing the nebula and stars as a backdrop. "
            f"{STYLE}"
        )
    },
]

results = {"success": [], "failed": []}

for i, img in enumerate(images, 1):
    filename = img["filename"]
    prompt = img["prompt"]
    out_path = os.path.join(OUTPUT_DIR, filename)
    print(f"[{i}/10] Generating {filename}...")
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            quality="high",
            n=1,
        )
        b64_data = response.data[0].b64_json
        image_bytes = base64.b64decode(b64_data)
        with open(out_path, "wb") as f:
            f.write(image_bytes)
        print(f"  ✅ Saved: {out_path}")
        results["success"].append(filename)
    except Exception as e:
        print(f"  ❌ FAILED {filename}: {e}")
        results["failed"].append({"file": filename, "error": str(e)})

print("\n=== SUMMARY ===")
print(f"Saved ({len(results['success'])}): {results['success']}")
if results["failed"]:
    print(f"Failed ({len(results['failed'])}): {results['failed']}")
else:
    print("No failures.")
