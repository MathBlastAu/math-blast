#!/usr/bin/env python3
"""Regenerate missing/failed images and upload all 15 to GitHub"""

import os
import time
import base64
import json
import requests
from pathlib import Path
from openai import OpenAI

IMAGES_DIR = Path("/Users/leohiem/.openclaw/workspace/projects/math-blast/images")
REFERENCE_IMAGE = IMAGES_DIR / "ch1-crashed-rocket.png"
GITHUB_TOKEN = "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"
GITHUB_REPO = "MathBlastAu/math-blast"
RATE_LIMIT_SECONDS = 15

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def save_image(data_b64: str, filepath: Path):
    img_bytes = base64.b64decode(data_b64)
    with open(filepath, "wb") as f:
        f.write(img_bytes)
    print(f"  Saved: {filepath.name} ({len(img_bytes)/1024:.0f}KB)")

def upload_to_github(filepath: Path, filename: str):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/images/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    r = requests.get(url, headers=headers)
    sha = r.json().get("sha") if r.status_code == 200 else None

    with open(filepath, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()

    payload = {"message": f"Regen Issue #2: {filename}", "content": content_b64}
    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=headers, json=payload)
    if r.status_code in (200, 201):
        print(f"  GitHub OK ({r.status_code}): {filename}")
        return True
    else:
        print(f"  GitHub ERROR {r.status_code}: {r.text[:200]}")
        return False

def generate_and_upload(filename: str, prompt: str, size: str, use_edit: bool = False):
    print(f"\n[GENERATE] {filename} ({size}, edit={use_edit})")
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
        return upload_to_github(filepath, filename)
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def upload_existing(filename: str):
    filepath = IMAGES_DIR / filename
    if not filepath.exists():
        print(f"  MISSING locally: {filename}")
        return False
    print(f"\n[UPLOAD] {filename}")
    return upload_to_github(filepath, filename)

results = {}

# === STEP 1: Regenerate ch images (use 1536x1024 — gpt-image-1 valid widescreen size) ===
ch_images = [
    ("ch1-robot-factory.png", "1536x1024", False,
     "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) stands open-mouthed at the entrance of a massive alien robot factory built into Saturn's rings, golden rings arcing overhead, rows of dormant robots inside, Pixar/Disney 3D animation style, vibrant colours, cinematic lighting, space adventure."),
    ("ch2-robot-factory.png", "1536x1024", False,
     "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) and Bolt (small boxy silver robot, glowing green eyes, chest speaker grille, chunky metal legs) walk along a vast factory assembly floor with rows of robot parts arranged in neat grids and arrays, golden overhead lighting, Pixar/Disney 3D animation style, vibrant colours, cinematic space adventure."),
    ("ch3-robot-factory.png", "1536x1024", False,
     "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) and Bolt (small boxy silver robot, glowing green eyes, chest speaker grille, chunky metal legs) stand before a massive glowing energy core reactor, Jake's hand on a control panel, sparks of light shooting upward, Pixar/Disney 3D animation style, dramatic lighting, vibrant colours, space factory setting."),
    ("ch4-robot-factory.png", "1536x1024", False,
     "Hundreds of small cute boxy silver robots with glowing green eyes march in perfect rows and columns across a vast factory floor, Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) watches from a catwalk above with mouth open in amazement, Pixar/Disney 3D animation style, vibrant colours, dramatic wide angle."),
    ("ch5-robot-factory.png", "1536x1024", False,
     "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) and Bolt (small boxy silver robot with glowing golden upgrade aura, chest speaker grille, chunky metal legs) celebrate together in a glass-walled control room overlooking a fully running robot factory, golden light streaming in, holographic displays everywhere, Pixar/Disney 3D animation style, warm triumphant lighting, space adventure."),
]

print("=== Generating ch1-ch5 (widescreen 1536x1024) ===")
for i, (fname, size, edit, prompt) in enumerate(ch_images):
    if i > 0:
        print(f"Waiting {RATE_LIMIT_SECONDS}s...")
        time.sleep(RATE_LIMIT_SECONDS)
    ok = generate_and_upload(fname, prompt, size, edit)
    results[fname] = "OK" if ok else "FAILED"

# === STEP 2: Regenerate q9 and q10 ===
q_missing = [
    ("q9-issue002.png", "1024x1024", False,
     "A top-down view of a rectangular factory floor grid exactly 8 tiles long and 7 tiles wide, each square tile clearly visible and numbered, the full 56-tile area glowing with soft blue light, clean overhead perspective showing the full rectangle, Pixar/Disney 3D animation style, vibrant colours."),
    ("q10-issue002.png", "1024x1024", True,
     "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch) at a factory control panel with two floor displays: Floor 1 showing a 3-by-5 grid of 15 glowing robots, Floor 2 showing a 4-by-4 grid of 16 glowing robots, dramatic control room setting, Pixar/Disney 3D animation style, vibrant colours."),
]

print("\n=== Generating q9-q10 ===")
for fname, size, edit, prompt in q_missing:
    print(f"Waiting {RATE_LIMIT_SECONDS}s...")
    time.sleep(RATE_LIMIT_SECONDS)
    ok = generate_and_upload(fname, prompt, size, edit)
    results[fname] = "OK" if ok else "FAILED"

# === STEP 3: Upload q1-q8 (already generated, just need GitHub upload) ===
q_existing = [
    "q1-issue002.png", "q2-issue002.png", "q3-issue002.png", "q4-issue002.png",
    "q5-issue002.png", "q6-issue002.png", "q7-issue002.png", "q8-issue002.png",
]

print("\n=== Uploading existing q1-q8 to GitHub ===")
for fname in q_existing:
    ok = upload_existing(fname)
    results[fname] = "OK" if ok else "FAILED"
    time.sleep(2)  # small delay between uploads

# Final report
print("\n\n=== FINAL RESULTS ===")
for fname in ["ch1-robot-factory.png","ch2-robot-factory.png","ch3-robot-factory.png",
              "ch4-robot-factory.png","ch5-robot-factory.png",
              "q1-issue002.png","q2-issue002.png","q3-issue002.png","q4-issue002.png",
              "q5-issue002.png","q6-issue002.png","q7-issue002.png","q8-issue002.png",
              "q9-issue002.png","q10-issue002.png"]:
    print(f"  {results.get(fname,'SKIPPED'):6s}: {fname}")

succeeded = sum(1 for s in results.values() if s == "OK")
print(f"\n{succeeded}/{len(results)} images OK")

with open("/tmp/gen_results.json", "w") as f:
    json.dump(results, f)
