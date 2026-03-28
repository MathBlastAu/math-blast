#!/usr/bin/env python3
"""Generate all 15 images for Math Blast Issue #2"""

import os
import sys
import time
import base64
import json
import requests
from pathlib import Path
from openai import OpenAI

# Config
IMAGES_DIR = Path("/Users/leohiem/.openclaw/workspace/projects/math-blast/images")
REFERENCE_IMAGE = IMAGES_DIR / "ch1-crashed-rocket.png"
GITHUB_TOKEN = "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"
GITHUB_REPO = "MathBlastAu/math-blast"
RATE_LIMIT_SECONDS = 15

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def save_image(data_b64: str, filepath: Path):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    img_bytes = base64.b64decode(data_b64)
    with open(filepath, "wb") as f:
        f.write(img_bytes)
    print(f"  Saved: {filepath.name} ({len(img_bytes)} bytes)")

def upload_to_github(filepath: Path, filename: str):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/images/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Get existing SHA
    r = requests.get(url, headers=headers)
    sha = None
    if r.status_code == 200:
        sha = r.json().get("sha")

    with open(filepath, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()

    payload = {
        "message": f"Regenerate {filename} for Issue #2",
        "content": content_b64
    }
    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=headers, json=payload)
    if r.status_code in (200, 201):
        print(f"  GitHub: {filename} uploaded OK (status {r.status_code})")
        return True
    else:
        print(f"  GitHub ERROR {r.status_code}: {r.text[:200]}")
        return False

def generate_image(filename: str, prompt: str, size: str, use_edit: bool = False):
    print(f"\n[{filename}] Generating ({size}, edit={use_edit})...")
    try:
        if use_edit:
            with open(REFERENCE_IMAGE, "rb") as ref:
                response = client.images.edit(
                    model="gpt-image-1",
                    image=ref,
                    prompt=prompt,
                    size=size
                )
        else:
            response = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size=size
            )
        
        data_b64 = response.data[0].b64_json
        filepath = IMAGES_DIR / filename
        save_image(data_b64, filepath)
        ok = upload_to_github(filepath, filename)
        return ok
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

# Image definitions
IMAGES = [
    # Chapter images (widescreen 1792x1024)
    {
        "filename": "ch1-robot-factory.png",
        "size": "1792x1024",
        "use_edit": False,
        "prompt": "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) stands open-mouthed at the entrance of a massive alien robot factory built into Saturn's rings, golden rings arcing overhead, rows of dormant robots inside, Pixar/Disney 3D animation style, vibrant colours, cinematic lighting, space adventure."
    },
    {
        "filename": "ch2-robot-factory.png",
        "size": "1792x1024",
        "use_edit": False,
        "prompt": "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) and Bolt (small boxy silver robot, glowing green eyes, chest speaker grille, chunky metal legs) walk along a vast factory assembly floor with rows of robot parts arranged in neat grids and arrays, golden overhead lighting, Pixar/Disney 3D animation style, vibrant colours, cinematic space adventure."
    },
    {
        "filename": "ch3-robot-factory.png",
        "size": "1792x1024",
        "use_edit": False,
        "prompt": "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) and Bolt (small boxy silver robot, glowing green eyes, chest speaker grille, chunky metal legs) stand before a massive glowing energy core reactor, Jake's hand on a control panel, sparks of light shooting upward, Pixar/Disney 3D animation style, dramatic lighting, vibrant colours, space factory setting."
    },
    {
        "filename": "ch4-robot-factory.png",
        "size": "1792x1024",
        "use_edit": False,
        "prompt": "Hundreds of small cute boxy silver robots with glowing green eyes march in perfect rows and columns across a vast factory floor, Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) watches from a catwalk above with mouth open in amazement, Pixar/Disney 3D animation style, vibrant colours, dramatic wide angle."
    },
    {
        "filename": "ch5-robot-factory.png",
        "size": "1792x1024",
        "use_edit": False,
        "prompt": "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) and Bolt (small boxy silver robot with glowing golden upgrade aura, chest speaker grille, chunky metal legs) celebrate together in a glass-walled control room overlooking a fully running robot factory, golden light streaming in, holographic displays everywhere, Pixar/Disney 3D animation style, warm triumphant lighting, space adventure."
    },
    # Question images (square 1024x1024)
    {
        "filename": "q1-issue002.png",
        "size": "1024x1024",
        "use_edit": True,
        "prompt": "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) holds up 8 glowing cylindrical fuel pods, each divided into 4 glowing quarter-sections, in a space setting, Pixar/Disney 3D animation style, vibrant colours."
    },
    {
        "filename": "q2-issue002.png",
        "size": "1024x1024",
        "use_edit": False,
        "prompt": "A neat 3-by-4 grid array of 12 small cute silver robots with glowing green eyes arranged in 3 rows of 4 columns on a factory floor, viewed from slightly above, clean and clear layout showing the array structure, Pixar/Disney 3D animation style, vibrant colours, space factory setting."
    },
    {
        "filename": "q3-issue002.png",
        "size": "1024x1024",
        "use_edit": False,
        "prompt": "A neat 5-by-6 grid array of 30 glowing circuit boards arranged in 5 rows of 6 columns on a factory shelf, viewed from slightly above, each board glowing blue-green, clean and clear grid layout, Pixar/Disney 3D animation style, vibrant colours."
    },
    {
        "filename": "q4-issue002.png",
        "size": "1024x1024",
        "use_edit": False,
        "prompt": "A neat 4-by-7 grid array of 28 glowing purple power cells arranged in 4 rows of 7 columns in a storage rack, viewed from slightly above, clean and clear layout showing the array, Pixar/Disney 3D animation style, vibrant colours, space factory setting."
    },
    {
        "filename": "q5-issue002.png",
        "size": "1024x1024",
        "use_edit": True,
        "prompt": "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) supervises 3 small boxy transport robots each carrying a stack of 8 supply crates, arranged side by side, Pixar/Disney 3D animation style, vibrant colours, space factory setting."
    },
    {
        "filename": "q6-issue002.png",
        "size": "1024x1024",
        "use_edit": True,
        "prompt": "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) looks up at a multi-storey factory building with 6 clearly labelled floors, each floor visible with 9 robotic arms extending from the walls, Pixar/Disney 3D animation style, vibrant colours, space setting."
    },
    {
        "filename": "q7-issue002.png",
        "size": "1024x1024",
        "use_edit": False,
        "prompt": "A sci-fi digital display screen showing a robot activation counter: 12 robots activating per minute, with a 3-minute timer countdown and a total count rapidly climbing to 36, small cute silver robots appearing on screen, Pixar/Disney 3D animation style, vibrant glowing colours, dramatic lighting."
    },
    {
        "filename": "q8-issue002.png",
        "size": "1024x1024",
        "use_edit": True,
        "prompt": "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) stands at a factory assembly station with 2 robots being built on the workbench in front of him, a display showing 24 bolts per robot, bolts scattered across the bench, Pixar/Disney 3D animation style, vibrant colours, space factory setting."
    },
    {
        "filename": "q9-issue002.png",
        "size": "1024x1024",
        "use_edit": False,
        "prompt": "A top-down view of a rectangular factory floor grid exactly 8 tiles long and 7 tiles wide, each square tile clearly visible and numbered, the full 56-tile area glowing with soft blue light, clean overhead perspective showing the full rectangle, Pixar/Disney 3D animation style, vibrant colours."
    },
    {
        "filename": "q10-issue002.png",
        "size": "1024x1024",
        "use_edit": True,
        "prompt": "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) at a factory control panel with two floor displays: Floor 1 showing a 3-by-5 grid of 15 glowing robots, Floor 2 showing a 4-by-4 grid of 16 glowing robots, dramatic control room setting, Pixar/Disney 3D animation style, vibrant colours."
    },
]

results = {}

for i, img in enumerate(IMAGES):
    if i > 0:
        print(f"\nWaiting {RATE_LIMIT_SECONDS}s before next image...")
        time.sleep(RATE_LIMIT_SECONDS)
    
    ok = generate_image(img["filename"], img["prompt"], img["size"], img["use_edit"])
    results[img["filename"]] = "OK" if ok else "FAILED"

print("\n\n=== RESULTS ===")
for fname, status in results.items():
    print(f"  {status}: {fname}")

succeeded = sum(1 for s in results.values() if s == "OK")
failed = sum(1 for s in results.values() if s == "FAILED")
print(f"\nTotal: {succeeded} succeeded, {failed} failed")

# Save results for the HTML update step
with open("/tmp/gen_results.json", "w") as f:
    json.dump(results, f)
