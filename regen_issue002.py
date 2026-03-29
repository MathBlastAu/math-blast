#!/usr/bin/env python3
import os, sys, time, base64, json, requests
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
GH_TOKEN = ""REDACTED""
GH_REPO  = "MathBlastAu/math-blast"
IMAGES_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"
REFERENCE  = f"{IMAGES_DIR}/ch1-crashed-rocket.png"

JAKE = "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles across nose and cheeks, orange space suit with silver trim, blue visor helmet with red rocket patch on chest)"
BOLT = "Bolt (small boxy silver robot, glowing green eyes, chest speaker grille, chunky metal legs)"
STYLE = "Pixar/Disney 3D animation style, vibrant saturated colours, cinematic lighting, space adventure theme, kid-friendly, high detail"

IMAGES = [
    # (filename, size, use_edit, prompt)
    ("ch1-robot-factory.png", "1792x1024", False,
     f"{JAKE} stands open-mouthed at the entrance of a massive alien robot factory built into Saturn's rings, golden rings arcing overhead, rows of dormant robots visible inside, {STYLE}."),
    ("ch2-robot-factory.png", "1792x1024", False,
     f"{JAKE} and {BOLT} walk along a vast factory assembly floor with rows of robot parts arranged in neat grids and arrays, golden overhead lighting, {STYLE}."),
    ("ch3-robot-factory.png", "1792x1024", False,
     f"{JAKE} and {BOLT} stand before a massive glowing energy core reactor, Jake's hand on a control panel, sparks of light shooting upward, dramatic lighting, {STYLE}."),
    ("ch4-robot-factory.png", "1792x1024", False,
     f"Hundreds of small cute boxy silver robots with glowing green eyes march in perfect rows and columns across a vast factory floor, {JAKE} watches from a catwalk above with mouth open in amazement, dramatic wide angle, {STYLE}."),
    ("ch5-robot-factory.png", "1792x1024", False,
     f"{JAKE} and Bolt (small boxy silver robot with glowing golden upgrade aura, chest speaker grille, chunky metal legs) celebrate together in a glass-walled control room overlooking a fully running robot factory, golden light streaming in, holographic displays everywhere, warm triumphant lighting, {STYLE}."),

    ("q1-issue002.png", "1024x1024", True,
     f"{JAKE} holds up 8 glowing cylindrical fuel pods, each divided into 4 glowing quarter-sections, in a space setting, {STYLE}."),
    ("q2-issue002.png", "1024x1024", False,
     f"A neat 3-by-4 grid array of 12 small cute silver robots with glowing green eyes arranged in 3 rows of 4 columns on a factory floor, viewed from slightly above, clean and clear layout showing the array structure, {STYLE}."),
    ("q3-issue002.png", "1024x1024", False,
     f"A neat 5-by-6 grid array of 30 glowing circuit boards arranged in 5 rows of 6 columns on a factory shelf, viewed from slightly above, each board glowing blue-green, clean and clear grid layout, {STYLE}."),
    ("q4-issue002.png", "1024x1024", False,
     f"A neat 4-by-7 grid array of 28 glowing purple power cells arranged in 4 rows of 7 columns in a storage rack, viewed from slightly above, clean and clear layout showing the array, {STYLE}."),
    ("q5-issue002.png", "1024x1024", True,
     f"{JAKE} supervises 3 small boxy transport robots each carrying a stack of 8 supply crates, arranged side by side, {STYLE}."),
    ("q6-issue002.png", "1024x1024", True,
     f"{JAKE} looks up at a multi-storey factory building with 6 clearly labelled floors, each floor visible with 9 robotic arms extending from the walls, {STYLE}."),
    ("q7-issue002.png", "1024x1024", False,
     f"A sci-fi digital display screen showing a robot activation counter: 12 robots activating per minute, 3-minute timer countdown, total count showing 36, small cute silver robots appearing on screen, vibrant glowing colours, dramatic lighting, {STYLE}."),
    ("q8-issue002.png", "1024x1024", True,
     f"{JAKE} stands at a factory assembly station with 2 robots being built on the workbench in front of him, a display showing '24 bolts per robot', bolts scattered across the bench, {STYLE}."),
    ("q9-issue002.png", "1024x1024", False,
     f"A top-down view of a rectangular factory floor grid exactly 8 tiles long and 7 tiles wide, each square tile clearly visible, the full 56-tile area glowing with soft blue light, clean overhead perspective showing the full rectangle, {STYLE}."),
    ("q10-issue002.png", "1024x1024", True,
     f"{JAKE} at a factory control panel with two floor displays: Floor 1 showing a 3-by-5 grid of 15 glowing robots, Floor 2 showing a 4-by-4 grid of 16 glowing robots, dramatic control room setting, {STYLE}."),
]

def gh_upload(filename, filepath):
    url = f"https://api.github.com/repos/{GH_REPO}/contents/images/{filename}"
    headers = {"Authorization": f"token {GH_TOKEN}"}
    # Get existing SHA if file exists
    r = requests.get(url, headers=headers)
    sha = r.json().get("sha") if r.status_code == 200 else None
    with open(filepath, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    payload = {"message": f"Regen Issue #2 image: {filename}", "content": content}
    if sha:
        payload["sha"] = sha
    r = requests.put(url, headers=headers, json=payload)
    return r.status_code in (200, 201)

results = []
for i, (fname, size, use_edit, prompt) in enumerate(IMAGES):
    print(f"[{i+1}/15] {fname} ({'edit' if use_edit else 'generate'}) ...", flush=True)
    outpath = f"{IMAGES_DIR}/{fname}"
    try:
        if use_edit:
            with open(REFERENCE, "rb") as ref:
                resp = client.images.edit(
                    model="gpt-image-1",
                    image=ref,
                    prompt=prompt,
                    size=size,
                )
        else:
            resp = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size=size,
            )
        img_data = base64.b64decode(resp.data[0].b64_json)
        with open(outpath, "wb") as f:
            f.write(img_data)
        print(f"  Saved locally. Uploading to GitHub...", flush=True)
        ok = gh_upload(fname, outpath)
        status = "✅ OK" if ok else "⚠️ upload failed"
        print(f"  GitHub: {status}", flush=True)
        results.append((fname, status))
    except Exception as e:
        print(f"  ❌ ERROR: {e}", flush=True)
        results.append((fname, f"❌ {e}"))

    if i < len(IMAGES) - 1:
        print(f"  Waiting 15s...", flush=True)
        time.sleep(15)

print("\n=== SUMMARY ===", flush=True)
for fname, status in results:
    print(f"  {status}  {fname}", flush=True)
print("Done.", flush=True)
