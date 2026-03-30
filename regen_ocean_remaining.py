#!/usr/bin/env python3
"""Continue Issue 4 remaining images: q3-q5 whale spots + q6-q10 lattice signals"""

import requests, base64, time, io, os
from PIL import Image, ImageDraw, ImageFilter

API_KEY = "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"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/ocean"
STYLE = "Pixar-style 3D CGI, stylised cartoon characters with large expressive eyes, dark moody underwater environment, cinematic low-key lighting, strong cyan and amber rim lights, bioluminescent elements casting coloured light, deep navy and blue-black shadows, warm amber practical light sources, detailed underwater coral architecture, volumetric underwater haze with light rays filtering from above, adventurous wonder-filled mood, high detail, 16:9 cinematic composition"

errors = []
success_count = 0

def gen_image(prompt, output_path):
    global success_count
    payload = {"model": "gpt-image-1", "prompt": prompt, "size": "1536x1024", "quality": "medium", "n": 1}
    for attempt in range(3):
        try:
            resp = requests.post("https://api.openai.com/v1/images/generations", headers=HEADERS, json=payload, timeout=120)
            data = resp.json()
            if "data" not in data:
                msg = data.get('error', {}).get('message', str(data))
                print(f"  ❌ ERROR ({attempt+1}/3): {msg}")
                if attempt < 2:
                    time.sleep(5)
                    continue
                errors.append(f"{os.path.basename(output_path)}: {msg}")
                return False
            img_bytes = base64.b64decode(data["data"][0]["b64_json"])
            with open(output_path, "wb") as f:
                f.write(img_bytes)
            print(f"  ✅ {os.path.basename(output_path)} ({len(img_bytes)//1024}KB)")
            success_count += 1
            time.sleep(1)
            return True
        except Exception as e:
            print(f"  ❌ EXCEPTION ({attempt+1}/3): {e}")
            if attempt < 2:
                time.sleep(5)
    errors.append(f"{os.path.basename(output_path)}: failed after 3 attempts")
    return False

def make_whale_spots(rows, cols, output_path):
    global success_count
    print(f"  🐋 Generating base whale for {os.path.basename(output_path)} ({rows}×{cols}={rows*cols})...")
    prompt = "close-up of enormous whale flank, dark charcoal grey skin with subtle texture, deep dark ocean background, dramatic cinematic lighting, no spots, no markings, Pixar-style 3D CGI, dark moody underwater, cinematic lighting, cyan rim light, high detail, 16:9"
    payload = {"model": "gpt-image-1", "prompt": prompt, "size": "1536x1024", "quality": "medium", "n": 1}
    for attempt in range(3):
        try:
            resp = requests.post("https://api.openai.com/v1/images/generations", headers=HEADERS, json=payload, timeout=120)
            data = resp.json()
            if "data" not in data:
                msg = data.get('error', {}).get('message', str(data))
                print(f"  ❌ ERROR ({attempt+1}/3): {msg}")
                if attempt < 2:
                    time.sleep(5)
                    continue
                errors.append(f"{os.path.basename(output_path)}: {msg}")
                return False
            img_bytes = base64.b64decode(data["data"][0]["b64_json"])
            break
        except Exception as e:
            print(f"  ❌ EXCEPTION ({attempt+1}/3): {e}")
            if attempt < 2:
                time.sleep(5)
            else:
                errors.append(f"{os.path.basename(output_path)}: failed after 3 attempts")
                return False

    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    W, H = img.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    spot_r = 22
    h_gap = W // (cols + 1)
    v_gap = H // (rows + 1)
    for r in range(rows):
        for c in range(cols):
            cx = h_gap * (c + 1)
            cy = v_gap * (r + 1)
            draw.ellipse([cx-spot_r*2, cy-spot_r*2, cx+spot_r*2, cy+spot_r*2], fill=(0, 220, 180, 40))
            draw.ellipse([cx-spot_r-4, cy-spot_r-4, cx+spot_r+4, cy+spot_r+4], fill=(0, 240, 200, 100))
            draw.ellipse([cx-spot_r, cy-spot_r, cx+spot_r, cy+spot_r], fill=(80, 255, 220, 230))
            draw.ellipse([cx-8, cy-8, cx+8, cy+8], fill=(200, 255, 245, 255))
    overlay = overlay.filter(ImageFilter.GaussianBlur(2))
    result = Image.alpha_composite(img, overlay).convert("RGB")
    result.save(output_path)
    print(f"  ✅ {os.path.basename(output_path)} ({rows}×{cols} = {rows*cols} spots)")
    success_count += 1
    time.sleep(1)
    return True

i4 = f"{BASE}/issue004"

print("ISSUE 4 — Remaining whale spot images (q3-q5)")
make_whale_spots(4, 7, f"{i4}/q3-whale-spots.png")
make_whale_spots(6, 7, f"{i4}/q4-whale-spots.png")
make_whale_spots(3, 8, f"{i4}/q5-whale-spots.png")

print("\nISSUE 4 — Lattice signal images (q6-q10)")
LATTICE_PROMPT = f"glowing amber signal stones on ocean floor activating in sequence, wave of light traveling through the grid, ocean floor, no text, {STYLE}"
for i in range(6, 11):
    gen_image(LATTICE_PROMPT, f"{i4}/q{i}-lattice-signal.png")

print(f"\nDONE — {success_count} images generated")
if errors:
    print(f"❌ {len(errors)} errors:")
    for e in errors:
        print(f"  - {e}")
else:
    print("✅ No errors!")
