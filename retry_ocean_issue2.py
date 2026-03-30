#!/usr/bin/env python3
"""Retry failed images for Ocean Issue 002 with correct quality param."""
import requests, base64, os, time

api_key = "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"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/ocean/issue002"
os.makedirs(BASE, exist_ok=True)

MARINA = "10-year-old girl, warm brown skin, dark eyes, dark hair in practical bun, deep teal research suit with white trim and wave emblem on chest, clear dome visor pulled back, amber wrist datapad, lean swimmer's build, determined expression"
FLICK = "small juvenile manta ray, deep navy blue body, electric cyan chevron markings on underbelly, glowing cyan wing-tips, two small twitching antenna fins above eyes, slightly translucent wing edges, hovering in water"
WREN = "small young crab-like creature, bright amber shell with fresh unfaded patterns, large curious eyes, no mantle, moves with nervous eager energy"

images = [
    ("ch2-wren-counting.png",
     f"{WREN} touching every second glowing amber stone in a row, {MARINA} walking alongside watching, {FLICK} hovering above, rows of stones stretching ahead, midnight blue ocean, photorealistic digital art"),
    ("ch5-shadow-overhead.png",
     f"underwater looking up, {MARINA} and {WREN} and {FLICK} small figures on ocean floor, enormous dark shadow passing overhead through the water above, ominous silhouette, deep blue water, photorealistic digital art"),
    ("cliffhanger-shadow-returns.png",
     f"underwater scene, enormous dark shadow visible through water above, {MARINA} and {WREN} looking up frozen and stunned, {FLICK} wing-tips bright with alarm, midnight blue water, tense atmosphere, photorealistic digital art"),
    ("q1-skip-count-2s.png",
     "row of glowing amber stones on ocean floor, every second stone brighter than the others, alternating bright and dim pattern, forming a clear skip pattern, no text, digital illustration"),
    ("q2-five-times-two.png",
     "five pairs of glowing amber signal stones on ocean floor, each pair clearly separated, vivid underwater scene, no text, digital illustration"),
    ("q3-skip-count-5s.png",
     "row of glowing amber stones, every fifth stone much brighter, skip counting pattern visible, underwater ocean floor, no text, digital illustration"),
    ("q4-four-times-five.png",
     "four groups of glowing amber signal stones, each group containing five stones arranged in a line, clearly separated groups, ocean floor, no text, digital illustration"),
    ("q5-skip-count-10s.png",
     "long row of glowing amber stones, stones glowing in groups, every tenth stone brightest, wide ocean floor scene, no text, digital illustration"),
    ("q6-three-times-ten.png",
     "three clusters of glowing amber signal stones on ocean floor, each cluster contains ten stones, clearly separated, midnight blue water, no text, digital illustration"),
    ("q7-six-times-two.png",
     "six pairs of glowing amber signal stones on ocean floor, each pair separated, clean underwater scene, no text, digital illustration"),
    ("q8-seven-times-five.png",
     "seven groups of glowing amber signal stones, each group of five in a row, clearly separated, ocean floor, no text, digital illustration"),
    ("q9-nine-times-two.png",
     "nine pairs of glowing amber signal stones on ocean floor, each pair clearly visible, bioluminescent underwater scene, no text, digital illustration"),
    ("q10-eight-times-ten.png",
     "eight clusters of glowing amber signal stones, each cluster of ten clearly grouped, wide ocean floor scene, midnight blue water, no text, digital illustration"),
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
