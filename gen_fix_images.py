#!/usr/bin/env python3
"""Regenerate ch2 aliens image and q5 clock using gpt-image-1 with style reference."""

import os, base64
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

IMAGES_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"
REFERENCE  = f"{IMAGES_DIR}/ch1-crashed-rocket.png"

JAKE  = "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch)"
STYLE = "Pixar/Disney 3D animation style, vibrant saturated colours, cinematic lighting, space adventure theme, kid-friendly, high detail"

IMAGES = [
    # Chapter 2 — aliens and Jake sharing pizza
    ("ch2-alien-feast-fixed.png", "1536x1024",
     f"{JAKE} sits cross-legged on the ground of Planet Zog sharing a giant glowing pizza with three small friendly green aliens. "
     f"The tallest alien wears a tiny purple crown and is bowing. The other two aliens (Zibble and Mork) look excited about the pizza. "
     f"The pizza glows with magical light. Purple alien sky, strange plants in background, Jake's crashed rocket visible behind them. {STYLE}."),

    # Q5 — clock showing 3:15
    ("q5-issue001-fixed.png", "1024x1024",
     f"A large futuristic space-themed analog clock on the wall of a rocket cockpit showing exactly 3:15 (quarter past three). "
     f"The short hour hand points just past the 3, the long minute hand points directly at the 3. "
     f"The clock face is clearly lit, bold numbers, glowing purple trim. {JAKE} is visible in the cockpit looking at the clock urgently. {STYLE}."),
]

def gen(filename, size, prompt):
    out = os.path.join(IMAGES_DIR, filename)
    print(f"Generating {filename}...")
    with open(REFERENCE, "rb") as f:
        ref_data = f.read()
    try:
        resp = client.images.edit(
            model="gpt-image-1",
            image=open(REFERENCE, "rb"),
            prompt=prompt,
            size=size,
        )
        img = base64.b64decode(resp.data[0].b64_json)
        open(out, "wb").write(img)
        print(f"  ✅ {filename} ({len(img)//1024}kb)")
    except Exception as e:
        # Fall back to generate (no reference)
        print(f"  ⚠️  edit failed ({e}), trying generate...")
        try:
            resp = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size=size,
                quality="high",
            )
            img = base64.b64decode(resp.data[0].b64_json)
            open(out, "wb").write(img)
            print(f"  ✅ {filename} via generate ({len(img)//1024}kb)")
        except Exception as e2:
            print(f"  ❌ {filename}: {e2}")

for fname, size, prompt in IMAGES:
    gen(fname, size, prompt)

print("\nDone! Refresh the page to see updated images.")
