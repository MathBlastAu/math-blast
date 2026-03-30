#!/usr/bin/env python3
"""Generate all images for Ocean Issue 003."""
import requests, base64, os, time

api_key = "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"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/ocean/issue003"
os.makedirs(BASE, exist_ok=True)

MARINA = "10-year-old girl, warm brown skin, dark eyes, dark hair in practical bun, deep teal research suit with white trim and wave emblem on chest, clear dome visor pulled back, amber wrist datapad, lean swimmer's build, determined expression"
FLICK = "small juvenile manta ray, deep navy blue body, electric cyan chevron markings on underbelly, glowing cyan wing-tips, two small twitching antenna fins above eyes, slightly translucent wing edges, hovering in water"
ELDER_LUMA = "small crab-like creature, deep burgundy-red shell with etched geometric patterns, large round amber eyes, pale gold sea-silk mantle draped over shell, black coral staff with glowing amber stone, four walking legs, three-fingered hands, wise dignified bearing"

images = [
    ("ch1-archive-approach.png",
     f"{ELDER_LUMA} leading {MARINA} and {FLICK} toward a massive ancient shipwreck covered in coral and bioluminescent growth, deep teal and gold light emanating from inside, dramatic underwater scene, photorealistic digital art"),
    ("ch2-marina-scanning.png",
     f"{MARINA} inside ancient shipwreck library, looking at vast grid of glowing stone tablets arranged in rows and columns, {ELDER_LUMA} beside her pointing with black coral staff, deep teal and gold light, wooden beams encrusted with coral, photorealistic digital art"),
    ("ch3-tablet-grid.png",
     "interior of ancient shipwreck, vast grid of glowing stone tablets in neat rows and columns, close shot showing the array clearly, deep teal and gold bioluminescent light, coral-encrusted wooden beams, majestic and ancient, photorealistic digital art"),
    ("ch4-ancient-record.png",
     f"{MARINA} kneeling reading a glowing stone tablet, her face lit by the teal light, {ELDER_LUMA} watching gravely, ancient abstract patterns on the tablet no readable text, deep teal light, sense of important discovery, photorealistic digital art"),
    ("ch5-luma-knowing.png",
     f"close portrait of {ELDER_LUMA}, large amber eyes grave and knowing, black coral staff held firmly, pale gold mantle, deep teal light of the Archive behind, serious and wise expression, photorealistic digital art"),
    ("cliffhanger-archive-window.png",
     f"interior of ancient shipwreck Archive, {MARINA} and {ELDER_LUMA} looking through a large porthole window, outside the window an enormous dark fin silhouette passing through dark water, rows of bioluminescent spots visible on the creature, tense atmosphere, photorealistic digital art"),
    ("q1-tablet-array.png",
     "grid of glowing stone tablets on shipwreck wall, arranged in three rows of four tablets each, clearly visible rows and columns, deep teal light, no text on tablets, digital illustration"),
    ("q2-tablet-array.png",
     "grid of glowing stone tablets, four rows of three tablets each, clearly visible rows and columns, ancient shipwreck interior, deep teal light, no text, digital illustration"),
    ("q3-tablet-array.png",
     "grid of glowing stone tablets, two rows of seven tablets each, clearly visible, shipwreck library, no text, digital illustration"),
    ("q4-tablet-array.png",
     "grid of glowing stone tablets, seven rows of two tablets each, clearly visible rows and columns, no text, digital illustration"),
    ("q5-tablet-array.png",
     "grid of glowing stone tablets, five rows of three tablets each, clearly visible, ancient shipwreck interior, no text, digital illustration"),
    ("q6-tablet-array.png",
     "grid of glowing stone tablets, three rows of five tablets each, clearly visible, shipwreck library, no text, digital illustration"),
    ("q7-tablet-array.png",
     "grid of glowing stone tablets, four rows of six tablets each, clearly visible rows and columns, deep teal light, no text, digital illustration"),
    ("q8-tablet-array.png",
     "grid of glowing stone tablets, six rows of four tablets each, clearly visible, ancient shipwreck, no text, digital illustration"),
    ("q9-whale-spots.png",
     "close view of enormous whale skin surface, bioluminescent spots arranged in a grid pattern, five rows of five spots each, deep ocean blue, no text, digital illustration"),
    ("q10-whale-spots.png",
     "enormous whale tail or flank, bioluminescent spots in three rows of eight clearly visible, deep ocean scene, no text, awe-inspiring scale, digital illustration"),
]

errors = []
for fname, prompt in images:
    out_path = os.path.join(BASE, fname)
    if os.path.exists(out_path):
        print(f"  SKIP (exists): {fname}")
        continue
    payload = {"model": "gpt-image-1", "prompt": prompt, "size": "1536x1024", "quality": "medium", "n": 1}
    for attempt in range(3):
        try:
            resp = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=payload, timeout=120)
            data = resp.json()
            if "data" in data and data["data"]:
                img_bytes = base64.b64decode(data["data"][0]["b64_json"])
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  OK: {fname} ({len(img_bytes)} bytes)")
                break
            else:
                print(f"  API error attempt {attempt+1}: {data}")
                if attempt < 2: time.sleep(5)
        except Exception as e:
            print(f"  Exception attempt {attempt+1}: {e}")
            if attempt < 2: time.sleep(5)
    else:
        errors.append(fname)
    time.sleep(1)

print(f"\nDone. Errors: {errors}")
