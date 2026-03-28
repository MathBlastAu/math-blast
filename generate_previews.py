#!/usr/bin/env python3
import os
import time
import base64
import requests
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

IMAGES_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"
JAKE_REF = os.path.join(IMAGES_DIR, "ch1-crashed-rocket.png")
GITHUB_TOKEN = "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"
REPO = "MathBlastAu/math-blast"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

def save_image(response, filename):
    path = os.path.join(IMAGES_DIR, filename)
    item = response.data[0]
    if hasattr(item, 'b64_json') and item.b64_json:
        image_data = base64.b64decode(item.b64_json)
        with open(path, "wb") as f:
            f.write(image_data)
    elif hasattr(item, 'url') and item.url:
        r = requests.get(item.url)
        with open(path, "wb") as f:
            f.write(r.content)
    else:
        raise ValueError(f"No image data in response: {item}")
    print(f"Saved: {path}")
    return path

def upload_to_github(local_path, github_filename):
    url = f"https://api.github.com/repos/{REPO}/contents/images/{github_filename}"
    r = requests.get(url, headers=headers)
    sha = r.json().get("sha") if r.status_code == 200 else None
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    body = {"message": f"Preview: {github_filename}", "content": content}
    if sha:
        body["sha"] = sha
    resp = requests.put(url, json=body, headers=headers)
    print(f"{github_filename}: HTTP {resp.status_code}")
    return resp.status_code

# ── q4: Pizza fractions (no Jake) ──────────────────────────────────────────
print("\n=== Generating q4-preview.png (pizza fractions) ===")
resp = client.images.generate(
    model="gpt-image-1",
    prompt="A single large round pizza cut into exactly 4 equal quarters with clean straight cuts, seen from directly above, Pixar 3D animation style, bright warm colours, one slice slightly pulled apart to show the division, simple clean background, child-friendly illustration",
    size="1024x1024"
)
q4_path = save_image(resp, "q4-preview.png")
upload_to_github(q4_path, "q4-preview.png")

print("Sleeping 13 seconds...")
time.sleep(13)

# ── q5: Telling the time (Jake + clock, no answer) ─────────────────────────
print("\n=== Generating q5-preview.png (telling the time) ===")
with open(JAKE_REF, "rb") as f:
    resp = client.images.edit(
        model="gpt-image-1",
        image=f,
        prompt="Jake — a 10-year-old boy with short messy brown hair, bright green eyes, light freckles, orange space suit with silver trim, red rocket patch on left shoulder — stands in a spacecraft cockpit pointing at a large glowing circular clock on the wall. The clock face shows only the two clock hands (no numbers on the face), with the short hand just past the 3 position and the long hand pointing straight at the 3. A large glowing question mark floats beside the clock. Pixar 3D animation style, vibrant colours, soft warm lighting, child-friendly",
        size="1024x1024"
    )
q5_path = save_image(resp, "q5-preview.png")
upload_to_github(q5_path, "q5-preview.png")

print("Sleeping 13 seconds...")
time.sleep(13)

# ── q6: Launch countdown (Jake, 30:00 timer, no answer) ────────────────────
print("\n=== Generating q6-preview.png (launch countdown) ===")
with open(JAKE_REF, "rb") as f:
    resp = client.images.edit(
        model="gpt-image-1",
        image=f,
        prompt="Jake — a 10-year-old boy with short messy brown hair, bright green eyes, light freckles, orange space suit with silver trim, red rocket patch on left shoulder — sits urgently at a spacecraft control panel with a large red digital countdown timer on the screen showing '30:00', warning lights flashing, a launch window graphic visible but no specific clock times shown. He looks focused and in a hurry. Pixar 3D animation style, vibrant colours, dramatic lighting, child-friendly",
        size="1024x1024"
    )
q6_path = save_image(resp, "q6-preview.png")
upload_to_github(q6_path, "q6-preview.png")

print("Sleeping 13 seconds...")
time.sleep(13)

# ── q10: Heat shield warm-up (Jake, panels, no start time answer) ───────────
print("\n=== Generating q10-preview.png (heat shield warm-up) ===")
with open(JAKE_REF, "rb") as f:
    resp = client.images.edit(
        model="gpt-image-1",
        image=f,
        prompt="Jake — a 10-year-old boy with short messy brown hair, bright green eyes, light freckles, orange space suit with silver trim, red rocket patch on left shoulder — looks urgently at a spacecraft dashboard showing two panels: one glowing panel reads 'RE-ENTRY WINDOW: 4:10' with an Earth icon, another panel shows 'HEAT SHIELD WARM-UP: 35 MIN' with a flame icon, and a third panel shows 'START TIME: ?' with a question mark. Earth is visible glowing through the window behind him. Pixar 3D animation style, vibrant colours, dramatic warm lighting, child-friendly",
        size="1024x1024"
    )
q10_path = save_image(resp, "q10-preview.png")
upload_to_github(q10_path, "q10-preview.png")

print("\n=== All done! ===")
print("Preview URLs (allow 1-2 min for GitHub Pages):")
print("  https://mathblastau.github.io/math-blast/images/q4-preview.png")
print("  https://mathblastau.github.io/math-blast/images/q5-preview.png")
print("  https://mathblastau.github.io/math-blast/images/q6-preview.png")
print("  https://mathblastau.github.io/math-blast/images/q10-preview.png")
