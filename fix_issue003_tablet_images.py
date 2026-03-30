#!/usr/bin/env python3
"""Regenerate q2 and q4 tablet array images for ocean issue 003.
q2: 4 rows × 3 cols (NOT 3×4) - commutativity demo
q4: 7 rows × 2 cols (NOT 3×4) - commutativity demo
"""
import requests, base64, time, os

api_key = "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"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/ocean/issue003"

STYLE = "dark moody underwater environment, cinematic teal and gold lighting, deep navy water, high detail, 16:9"

images = [
    ("q2-tablet-array.png",
     # Emphasize TALL (more rows than columns) layout, landscape ratio
     "Ancient shipwreck library wall with glowing stone tablets arranged in EXACTLY 4 rows and 3 columns (FOUR horizontal rows, THREE tablets in each row). The 4 rows are clearly distinct horizontal bands stacked vertically. Each row has exactly 3 tablets side by side. Total: 12 tablets arranged 4-tall by 3-wide. Teal and amber bioluminescent glow, dark wood background, no text on tablets. " + STYLE),
    ("q4-tablet-array.png",
     # Very tall narrow layout
     "Ancient shipwreck library wall with glowing stone tablets in EXACTLY 7 rows and 2 columns (SEVEN horizontal rows stacked from top to bottom, with exactly TWO tablets side by side in each row). This creates a tall, narrow grid that is much taller than it is wide. Total: 14 tablets. Each row has only 2 tablets. Teal and amber bioluminescent glow, dark wood background, no text on tablets. " + STYLE),
]

for fname, prompt in images:
    out_path = os.path.join(BASE, fname)
    print(f"Generating {fname}...")
    payload = {"model": "gpt-image-1", "prompt": prompt, "size": "1536x1024", "quality": "medium", "n": 1}
    for attempt in range(3):
        try:
            resp = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=payload, timeout=120)
            data = resp.json()
            if "data" in data and data["data"]:
                img_bytes = base64.b64decode(data["data"][0]["b64_json"])
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  ✅ {fname} ({len(img_bytes)//1024}KB)")
                break
            else:
                print(f"  ❌ API error attempt {attempt+1}: {data}")
                if attempt < 2:
                    time.sleep(5)
        except Exception as e:
            print(f"  ❌ Exception attempt {attempt+1}: {e}")
            if attempt < 2:
                time.sleep(5)
    time.sleep(2)

print("\nDone.")
