#!/usr/bin/env python3
"""Fix remaining image issues — simpler, cleaner prompts focused on character consistency."""
from openai import OpenAI
import base64, os, time

client = OpenAI()
IMG_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/images/")

# Single locked Jake description used in EVERY prompt
JAKE = (
    "10-year-old boy Jake: short messy brown hair, warm fair skin, "
    "bright orange space cadet jumpsuit with silver accent panels and a small rocket badge on the chest, "
    "slightly scuffed boots, big expressive eyes, Disney Pixar CGI 3D animation style, "
    "vibrant saturated colours, clean polished render"
)

SETTING = (
    "clean futuristic space station interior, soft blue-grey walls, "
    "glowing holographic panels, Disney Pixar CGI 3D animation style"
)

def gen(filename, prompt, size="1024x1024"):
    path = IMG_DIR + filename
    print(f"  ⏳ {filename}...")
    try:
        r = client.images.generate(model="gpt-image-1", prompt=prompt, size=size)
        data = base64.b64decode(r.data[0].b64_json)
        with open(path, 'wb') as f: f.write(data)
        print(f"  ✅ {filename} ({len(data):,}b)")
        time.sleep(12)
    except Exception as e:
        print(f"  ❌ {e}")

# q4 — Jake pointing at TWO simple bar gauges side by side
# Keep it simple: Jake + two bars, no complex before/after story
gen("q4-issue001.png",
    f"{JAKE}, expression: pointing carefully with one finger, "
    f"standing beside a holographic display showing two horizontal bar gauges side by side. "
    f"Left gauge: a rectangular bar split into 4 equal sections, ALL 4 sections glowing bright green (completely full). "
    f"Right gauge: same rectangular bar split into 4 equal sections, only the LEFT 3 sections glowing green, the rightmost 1 section is dark/empty with a faint red outline. "
    f"The two gauges are clearly labelled with small arrows but NO fraction text or numbers anywhere. "
    f"{SETTING}.")

# q5 — Jake pointing at two bars: left=2 of 4 filled, right=1 of 4 filled
gen("q5-issue001.png",
    f"{JAKE}, expression: eyebrows raised, surprised realisation face, "
    f"beside a holographic display showing two horizontal bar gauges side by side. "
    f"Left gauge: rectangular bar with 4 equal sections, LEFT 2 sections glowing green, right 2 sections dark/empty. "
    f"Right gauge: same bar with 4 equal sections, only the LEFTMOST 1 section glowing green, the other 3 sections dark/empty with a faint red outline. "
    f"NO fraction numbers, NO text, NO labels anywhere in the image. "
    f"{SETTING}.")

# q8 — Jake beside exactly 6 glowing fuel pods arranged in 2 groups of 3
gen("q8-issue001.png",
    f"{JAKE}, expression: dividing/sharing gesture, arms spread to indicate splitting, "
    f"standing in front of a storage shelf showing EXACTLY 6 glowing cylindrical fuel pods arranged in a row. "
    f"The 6 pods are split into two equal groups of 3 by a glowing dotted line down the middle. "
    f"Each group of 3 pods has a small spaceship icon hovering above it. "
    f"EXACTLY 6 pods — count them: six individual glowing cylinders. "
    f"NO numbers or text visible. "
    f"{SETTING}.")

# q9 — Jake counting, 3 stacked bars each with 4 sections, rightmost removed
gen("q9-issue001.png",
    f"{JAKE}, expression: counting on fingers, focused, "
    f"beside a holographic display showing THREE identical horizontal bar gauges stacked vertically. "
    f"Each bar has EXACTLY 4 equal sections. "
    f"In each bar, the LEFT 3 sections glow bright green, and the RIGHTMOST 1 section glows red/is highlighted as removed. "
    f"A glowing arrow from each red section points to a single combined glowing shape on the right side showing the total removed. "
    f"NO numbers, NO fraction text anywhere. "
    f"{SETTING}.")

print("\nDone.")
