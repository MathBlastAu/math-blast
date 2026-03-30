#!/usr/bin/env python3
"""Generate all 16 Issue 002 images using OpenAI images/edits endpoint with style reference."""

import os
import base64
import json
import time
import requests

API_KEY = "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"
BASE_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast"
REF_IMAGE = os.path.join(BASE_DIR, "images/jungle/ch1-crash-landing.png")
OUT_DIR = os.path.join(BASE_DIR, "images/jungle/issue002")

IMAGES = [
    ("ch1-fernmoss-arrival.png", "Blaze arriving at a lower-canopy jungle village (Fernmoss) built among enormous glowing blue mushrooms. Bioluminescent light, misty atmosphere. A worried small blue Sprocket named Thistle stands among medicine bottles. Vibrant cartoon illustration style, same Blaze character (orange fire-robot) and Sprocket character design as the reference image. Same jungle art style as reference."),
    ("ch2-food-store.png", "Blaze inside a Fernmoss storage hut examining baskets of nuts and seeds. Warm mushroom glow lighting. A tiny sick Sprocket rests on a leaf-bed in the background. Vibrant cartoon illustration style, same Blaze character and Sprocket character design as the reference image. Same jungle art style as reference."),
    ("ch3-counting-store.png", "Blaze sorting through storage boxes in Fernmoss. Organised piles of seeds and leaves on shelves. Jungle canopy visible through gaps in the hut walls. Vibrant cartoon illustration style, same Blaze character and Sprocket character design as the reference image. Same jungle art style as reference."),
    ("ch4-vine-pattern.png", "Blaze crouching in the jungle studying a trail of missing vines on the ground. Pointing at something suspicious. Dappled jungle light, slightly ominous mood. Vibrant cartoon illustration style, same Blaze character design as the reference image. Same jungle art style as reference."),
    ("ch5-distribution-fixed.png", "Fernmoss Sprockets gathered together, each holding their correct equal share of food. Blaze stands to one side looking satisfied. Warm glowing mushroom light, celebratory scene. Vibrant cartoon illustration style, same Blaze character and multiple Sprocket character designs as the reference image. Same jungle art style as reference."),
    ("q1-medicine-doses.png", "A row of 12 small glowing medicine bottles on a shelf, with 4 Sprockets standing in front. Clear visual mismatch between 12 bottles and 4 recipients for educational purposes. Clean, educational illustration. Same Sprocket character style as the reference image. Jungle mushroom-glow background. Same art style as reference."),
    ("q2-nut-baskets.png", "48 round nuts being divided into 8 equal piles. Clean, clear educational image showing equal grouping of nuts. Jungle setting with warm lighting. Same art style as the reference image."),
    ("q3-sick-sprocket.png", "A small glowing medicine cup with visual indication of 4x dose (4 measures shown). A tiny unwell Sprocket in bed nearby. Warm, sympathetic lighting. Same Sprocket character style as the reference image. Same art style as reference."),
    ("q4-healing-leaves.png", "56 green healing leaves arranged in 7 equal groups of 8 leaves each. Clear rows on a wooden surface. Mushroom glow background. Educational, clean illustration. Same jungle art style as the reference image."),
    ("q5-seed-groups.png", "63 small seeds arranged in 7 groups of 9 seeds each. Seven neat circular piles on a jungle floor surface. Educational, clean illustration. Same jungle art style as the reference image."),
    ("q6-vine-trips.png", "42 vines arranged in 7 groups of 6 vines each, with creature footprint marks between each group. Jungle floor setting. Educational illustration showing clear grouping. Same jungle art style as the reference image."),
    ("q7-vine-bundles.png", "35 vines in 5 neat bundles tied with leaves. Jungle floor setting. Clear grouping of exactly 7 vines per bundle. Educational illustration. Same jungle art style as the reference image."),
    ("q8-vine-trail-map.png", "A top-down illustrated map view showing a vine trail between two jungle villages. Distance markers every 8 units along the trail. 9 sections visible. Illustrated map style. Same jungle art style as the reference image."),
    ("q9-resource-share.png", "81 colourful jungle fruits and nuts being divided into 9 equal piles of 9 items each. Clear, organised educational illustration. Same jungle art style as the reference image."),
    ("q10-boss-fraction.png", "9 jungle food items clearly displayed in a neat row, with 6 of them glowing or highlighted (representing the fraction 6/9 or 2/3). Clear fraction-of-a-set educational diagram. Same jungle art style as the reference image."),
    ("cliffhanger-deep-root.png", "Dark jungle night scene. Enormous ancient twisted trees in the deep background (the Deep Root). In the mud foreground, enormous vine-creature footprints trail toward the ancient trees. Mysterious and beautiful atmosphere. Same jungle art style as the reference image."),
]

def generate_image(filename, prompt, ref_bytes):
    out_path = os.path.join(OUT_DIR, filename)
    print(f"Generating: {filename}")
    
    files = {
        "image": ("reference.png", ref_bytes, "image/png"),
    }
    data = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1536x1024",
        "quality": "medium",
        "n": "1",
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }
    
    for attempt in range(3):
        try:
            resp = requests.post(
                "https://api.openai.com/v1/images/edits",
                headers=headers,
                files=files,
                data=data,
                timeout=120,
            )
            if resp.status_code == 200:
                result = resp.json()
                b64 = result["data"][0]["b64_json"]
                img_bytes = base64.b64decode(b64)
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                size_kb = len(img_bytes) // 1024
                print(f"  ✓ Saved {filename} ({size_kb}KB)")
                return True
            elif resp.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"  Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ERROR {resp.status_code}: {resp.text[:300]}")
                if attempt < 2:
                    time.sleep(10)
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < 2:
                time.sleep(10)
    
    return False

def main():
    print(f"Loading reference image: {REF_IMAGE}")
    with open(REF_IMAGE, "rb") as f:
        ref_bytes = f.read()
    print(f"Reference image loaded: {len(ref_bytes)} bytes")
    
    os.makedirs(OUT_DIR, exist_ok=True)
    
    results = []
    for i, (filename, prompt) in enumerate(IMAGES):
        success = generate_image(filename, prompt, ref_bytes)
        results.append((filename, success))
        # Small delay between requests to avoid rate limiting
        if i < len(IMAGES) - 1:
            time.sleep(3)
    
    print("\n=== RESULTS ===")
    success_count = 0
    for filename, success in results:
        status = "✓" if success else "✗"
        print(f"  {status} {filename}")
        if success:
            success_count += 1
    
    print(f"\n{success_count}/{len(IMAGES)} images generated successfully.")

if __name__ == "__main__":
    main()
