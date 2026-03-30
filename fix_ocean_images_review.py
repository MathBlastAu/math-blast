#!/usr/bin/env python3
"""
Regenerate specific images for Ocean Arc post-review
"""
import os
import time
import base64
import requests

OPENAI_API_KEY = "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"
IMG_BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/ocean"

MARINA = "10-year-old girl, warm brown skin, dark eyes, dark hair in practical bun, full underwater dive suit in deep teal with white trim and wave emblem on chest, clear full-face diving helmet, amber wrist datapad on suit arm, determined expression, swimming or floating underwater"
FLICK = "small juvenile manta ray, deep navy blue body, electric cyan chevron markings on underbelly, glowing cyan wing-tips, two small twitching antenna fins above eyes, slightly translucent wing edges, hovering in water"
ELDER_LUMA = "small crab-like creature, deep burgundy-red shell with etched geometric patterns, large round amber eyes, pale gold sea-silk mantle draped over shell, black coral staff with glowing amber stone, four walking legs, three-fingered hands, wise dignified bearing"
WREN = "small young crab-like creature, bright amber shell with fresh unfaded patterns, large curious eyes, no mantle, nervous eager energy"

images = [
    # ISSUE 1 images
    (f"{IMG_BASE}/issue001/ch1-sub-approaching-luminos.png",
     "small yellow-orange research submarine with round porthole windows moving through deep indigo underwater, approaching a distant bioluminescent coral city with glowing teal and orange coral towers, cinematic underwater establishing shot, submarine seen from outside, no characters visible outside the sub, dramatic underwater lighting"),

    (f"{IMG_BASE}/issue001/ch3-elder-luma-lattice.png",
     f"deep indigo underwater scene, grid of glowing amber signal stones arranged on ocean floor, {ELDER_LUMA} gesturing toward the stones with one hand, {MARINA} watching attentively, {FLICK} hovering nearby, bioluminescent coral city visible in background, cinematic underwater scene, warm amber and teal lighting"),

    (f"{IMG_BASE}/issue001/ch5-lattice-flickering.png",
     f"grid of amber signal stones on ocean floor, some stones dark and flickering while others glow, small crab-like Coralfolk figures with worried expressions looking at the stones, deep indigo water above, sense of malfunction and tension, bioluminescent underwater scene, cinematic composition, teal and amber colors"),

    (f"{IMG_BASE}/issue001/cliffhanger-deep-glow.png",
     "view looking down into a vast dark ocean trench from above, midnight blue water fading to absolute black below, faint rhythmic blue-green bioluminescent glow pulsing far below in the darkness arranged in patterns, sense of enormous ancient presence, mysterious and awe-inspiring, no characters visible, deep ocean atmosphere, cinematic"),

    # ISSUE 2 images
    (f"{IMG_BASE}/issue002/ch2-wren-counting.png",
     f"{MARINA} walking alongside a long row of glowing amber signal stones on ocean floor, {WREN} reaching out to touch every second stone with one hand, {FLICK} hovering above them watching, rows of stones stretching ahead into deep midnight blue water, cinematic underwater scene, warm amber and teal lighting"),
]


def generate_image(out_path, prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard",
        "response_format": "b64_json"
    }
    for attempt in range(3):
        try:
            r = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload,
                timeout=120
            )
            if r.status_code == 200:
                data = r.json()
                b64 = data["data"][0].get("b64_json")
                if b64:
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    with open(out_path, "wb") as f:
                        f.write(base64.b64decode(b64))
                    print(f"  ✅ {os.path.basename(out_path)}")
                    return True
                else:
                    url = data["data"][0].get("url")
                    if url:
                        img_r = requests.get(url, timeout=60)
                        if img_r.status_code == 200:
                            os.makedirs(os.path.dirname(out_path), exist_ok=True)
                            with open(out_path, "wb") as f:
                                f.write(img_r.content)
                            print(f"  ✅ {os.path.basename(out_path)} (url)")
                            return True
                print(f"  ❌ No image data in response")
                return False
            elif r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 30))
                print(f"  ⏳ Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ❌ HTTP {r.status_code}: {r.text[:300]}")
                return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            if attempt < 2:
                time.sleep(5)
    return False


def main():
    print(f"Generating {len(images)} images...\n")
    ok = 0
    fail = 0
    for out_path, prompt in images:
        print(f"  [{os.path.basename(out_path)}]")
        if generate_image(out_path, prompt):
            ok += 1
        else:
            fail += 1
        time.sleep(2)

    print(f"\n✅ {ok} generated, ❌ {fail} failed")


if __name__ == "__main__":
    main()
