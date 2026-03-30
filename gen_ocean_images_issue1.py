#!/usr/bin/env python3
"""Generate all images for Ocean Issue 001."""
import requests, base64, os, time

api_key = "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"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/ocean/issue001"
os.makedirs(BASE, exist_ok=True)

MARINA = "10-year-old girl, warm brown skin, dark eyes, dark hair in practical bun, deep teal research suit with white trim and wave emblem on chest, clear dome visor pulled back, amber wrist datapad, lean swimmer's build, determined expression"
FLICK = "small juvenile manta ray, deep navy blue body, electric cyan chevron markings on underbelly, glowing cyan wing-tips, two small twitching antenna fins above eyes, slightly translucent wing edges, hovering in water"
ELDER_LUMA = "small crab-like creature, deep burgundy-red shell with etched geometric patterns, large round amber eyes, pale gold sea-silk mantle draped over shell, black coral staff with glowing amber stone, four walking legs, three-fingered hands, wise dignified bearing"

images = [
    ("ch1-sub-approaching-luminos.png",
     "small research submarine approaching a vast bioluminescent coral city, deep indigo ocean water, glowing teal and orange coral towers in distance, shafts of light from above, cinematic underwater scene, photorealistic digital art style"),
    ("ch2-luminos-exterior.png",
     "bioluminescent coral city exterior, vivid orange and pink coral towers, glowing teal light trails, small crab-like Coralfolk figures visible, deep indigo water, establishing wide shot, majestic and awe-inspiring, photorealistic digital art"),
    ("ch3-elder-luma-lattice.png",
     f"{ELDER_LUMA} gesturing toward grid of glowing amber signal stones on ocean floor, bioluminescent coral city background, {MARINA} watching attentively, {FLICK} hovering nearby, deep indigo water, photorealistic digital art"),
    ("ch4-marina-datapad.png",
     f"{MARINA} looking at glowing amber wrist datapad with focused expression, {FLICK} hovering beside her, deep ocean background with signal stones visible, photorealistic digital art"),
    ("ch5-lattice-flickering.png",
     "grid of amber signal stones on ocean floor, some stones going dark and flickering, small crab-like Coralfolk figures looking worried, deep indigo water, sense of tension and malfunction, photorealistic digital art"),
    ("cliffhanger-deep-glow.png",
     "vast dark ocean trench from above, midnight blue water fading to black, faint rhythmic blue-green glow pulsing from far below, sense of enormous presence, mysterious and awe-inspiring, photorealistic digital art"),
    ("q1-fish-groups.png",
     "three separate coral fish pens underwater, each pen containing four identical tropical fish, clearly separated by coral walls, vivid colours, clean educational scene, underwater world, no text, digital illustration"),
    ("q2-fish-groups.png",
     "four separate coral fish pens underwater, each pen containing two identical tropical fish, clearly separated, vivid colours, no text, digital illustration"),
    ("q3-fish-groups.png",
     "three separate coral fish pens underwater, each pen containing five identical tropical fish, clearly separated, vivid colours, no text, digital illustration"),
    ("q4-fish-groups.png",
     "five separate coral fish pens underwater, each pen containing two identical tropical fish, vivid colours, no text, digital illustration"),
    ("q5-fish-groups.png",
     "two separate coral fish pens underwater, each pen containing six identical tropical fish, vivid colours, no text, digital illustration"),
    ("q6-lattice-stones.png",
     "four groups of glowing amber signal stones on ocean floor, each group containing four stones, clearly separated groups, midnight blue water, no text, digital illustration"),
    ("q7-lattice-stones.png",
     "three groups of glowing amber signal stones on ocean floor, each group containing six stones, clearly separated groups, midnight blue water, no text, digital illustration"),
    ("q8-lattice-stones.png",
     "five groups of glowing amber signal stones on ocean floor, each group containing four stones, clearly separated groups, midnight blue water, no text, digital illustration"),
    ("q9-lattice-stones.png",
     "two groups of glowing amber signal stones on ocean floor, each group containing seven stones, clearly separated groups, midnight blue water, no text, digital illustration"),
    ("q10-lattice-stones.png",
     "three groups of glowing amber signal stones on ocean floor, each group containing three stones, clearly separated groups, midnight blue water, no text, digital illustration"),
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
