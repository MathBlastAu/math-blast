#!/usr/bin/env python3
"""Generate all images for Ocean Issue 004."""
import requests, base64, os, time

api_key = "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"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/ocean/issue004"
os.makedirs(BASE, exist_ok=True)

MARINA = "10-year-old girl, warm brown skin, dark eyes, dark hair in practical bun, deep teal research suit with white trim and wave emblem on chest, clear dome visor pulled back, amber wrist datapad, lean swimmer's build, determined expression"
FLICK = "small juvenile manta ray, deep navy blue body, electric cyan chevron markings on underbelly, glowing cyan wing-tips, two small twitching antenna fins above eyes, slightly translucent wing edges, hovering in water"
ELDER_LUMA = "small crab-like creature, deep burgundy-red shell with etched geometric patterns, large round amber eyes, pale gold sea-silk mantle draped over shell, black coral staff with glowing amber stone, four walking legs, three-fingered hands, wise dignified bearing"

images = [
    ("ch1-deep-trench-descent.png",
     f"{MARINA} and {FLICK} descending into deep ocean trench, water darkening from deep blue to near black below, faint blue-green bioluminescent glow far below, cinematic and awe-inspiring, sense of great depth, photorealistic digital art"),
    ("ch2-whale-full-reveal.png",
     f"enormous ancient whale, dark charcoal body, bioluminescent blue-green spots arranged in grid rows, large gentle violet eyes, {MARINA} and {FLICK} tiny figures in comparison, vast deep ocean, majestic and awe-inspiring full reveal shot, photorealistic digital art"),
    ("ch3-whale-spots-closeup.png",
     "close-up of enormous whale flank, bioluminescent blue-green spots arranged in neat grid-like rows, deep ocean background, spectacular detail, dark charcoal skin, no text, photorealistic digital art"),
    ("ch4-marina-calculating.png",
     f"{MARINA} studying glowing amber wrist datapad with intense focus, {FLICK} hovering anxiously beside her, enormous whale silhouette visible in dark water background, tense and focused atmosphere, photorealistic digital art"),
    ("ch5-lattice-lighting.png",
     "vast ocean floor grid of amber signal stones all activating and glowing bright simultaneously, wave of light spreading across the ocean floor, bioluminescent coral city visible in background, triumphant and beautiful, photorealistic digital art"),
    ("finale-luminos-celebration.png",
     f"bioluminescent coral city Luminos fully lit and glowing, small crab-like Coralfolk figures celebrating, lights and colours everywhere, {MARINA} and {FLICK} in foreground watching with joy, {ELDER_LUMA} beside {MARINA} extending small three-fingered hand holding a glowing amber signal stone, triumphant and warm scene, photorealistic digital art"),
    ("q1-whale-spots.png",
     "close section of whale skin, bioluminescent spots in three clear rows of six spots each, dark deep ocean background, no text, digital illustration"),
    ("q2-whale-spots.png",
     "whale flank section, bioluminescent spots in five rows of six spots each, deep ocean, no text, digital illustration"),
    ("q3-whale-spots.png",
     "whale skin section, bioluminescent spots in four rows of seven spots each, dark ocean background, no text, digital illustration"),
    ("q4-whale-spots.png",
     "whale flank, bioluminescent spots in six rows of seven spots each, deep ocean, no text, digital illustration"),
    ("q5-whale-spots.png",
     "whale skin section, bioluminescent spots in three rows of eight spots each, dark deep ocean, no text, digital illustration"),
    ("q6-lattice-signal.png",
     "five rows of eight glowing amber signal stones on ocean floor, activation wave spreading through them, light traveling from left to right, no text, digital illustration"),
    ("q7-lattice-signal.png",
     "seven rows of six glowing amber signal stones, all activating in sequence, ocean floor, no text, digital illustration"),
    ("q8-lattice-signal.png",
     "four rows of eight glowing amber signal stones, wave of activation visible, underwater ocean floor scene, no text, digital illustration"),
    ("q9-lattice-signal.png",
     "six rows of six glowing amber signal stones, all glowing brightly, ocean floor, bioluminescent scene, no text, digital illustration"),
    ("q10-whale-farewell.png",
     "enormous whale silhouette departing into deep ocean, bioluminescent spots in eight rows visible on body, deep midnight blue water, awe-inspiring farewell scene, no text, digital illustration"),
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
