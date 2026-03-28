#!/usr/bin/env python3
"""Generate all 15 Math Blast Issue #1 images with consistent Jake character description."""

import os
import sys
import time
import json
import base64
import requests
from pathlib import Path

# Load API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY not set")
    sys.exit(1)

IMAGES_DIR = Path("/Users/leohiem/.openclaw/workspace/projects/math-blast/images")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

GITHUB_TOKEN = "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"
GITHUB_REPO = "MathBlastAu/math-blast"

# Locked character description
JAKE = "a 10-year-old boy with short messy brown hair, bright green eyes, light freckles across his nose, wearing a bright orange space suit with silver trim, a blue reflective visor helmet (visor up when indoors/close-up), and a small red rocket patch on his left shoulder"

# Style anchor
STYLE = "Pixar 3D animation style, vibrant colours, soft warm lighting, child-friendly, cinematic quality, white background elements avoided"

# Chapter images (1792x1024 = landscape)
chapter_images = [
    {
        "filename": "ch1-crashed-rocket.png",
        "size": "1792x1024",
        "prompt": f"Jake — {JAKE} — floats in zero gravity inside a damaged spacecraft cockpit, looking worried but determined at a cracked control panel with sparking wires. Stars visible through a cracked windshield. Bolt, a small silver robot with glowing blue eyes and a friendly round face, hovers beside him. {STYLE}"
    },
    {
        "filename": "ch2-alien-feast.png",
        "size": "1792x1024",
        "prompt": f"Jake — {JAKE} — stands in a colourful alien marketplace on a space station, surrounded by bizarre exotic alien fruits and foods on floating market stalls. Several friendly alien creatures with multiple arms wave at him. Bolt the small silver robot stands beside Jake looking curious. {STYLE}"
    },
    {
        "filename": "ch3-launch-window.png",
        "size": "1792x1024",
        "prompt": f"Jake — {JAKE} — sits at a glowing mission control console, pointing at a holographic countdown clock showing 12:45. The room has a large window showing stars and a planet in the distance. Bolt the small silver robot points at the clock too. {STYLE}"
    },
    {
        "filename": "ch4-asteroid-belt.png",
        "size": "1792x1024",
        "prompt": f"Jake — {JAKE} — pilots a small orange spacecraft through a dramatic asteroid belt, hands on controls, looking focused and excited. Large rocky asteroids of various sizes float around the ship. Bolt the silver robot is co-pilot, gripping the seat. {STYLE}"
    },
    {
        "filename": "ch5-earth-landing.png",
        "size": "1792x1024",
        "prompt": f"Jake — {JAKE} — stands triumphantly on a landing pad, arms raised in victory, with a blue and green Earth visible behind him through a glass dome. Bolt the silver robot does a little celebration dance beside him. Mission complete banner visible. {STYLE}"
    },
]

# Question images (1024x1024)
question_images = [
    {
        "filename": "q1-issue001.png",
        "size": "1024x1024",
        "prompt": f"A glowing futuristic computer screen in a spacecraft cockpit showing a skip-counting sequence: large glowing numbers 5, 10, 15, then a blank glowing box, then 25, then another blank glowing box. The numbers glow bright blue and yellow. Jake — {JAKE} — peers at the screen with a curious expression. {STYLE}"
    },
    {
        "filename": "q2-issue001.png",
        "size": "1024x1024",
        "prompt": f"Four neat rows of 6 shining blue fuel crystals each arranged on the floor of a spacecraft engine room, totalling 24 crystals. Jake — {JAKE} — kneels down counting them with a notebook and pencil in hand. The crystals glow with a magical blue light. {STYLE}"
    },
    {
        "filename": "q3-issue001.png",
        "size": "1024x1024",
        "prompt": f"A large glowing alien pizza on a floating table in a colourful space station, clearly divided into 4 equal slices. Four characters sit around the table: Jake — {JAKE} — and three small friendly green alien creatures. One slice is highlighted for each character. {STYLE}"
    },
    {
        "filename": "q4-issue001.png",
        "size": "1024x1024",
        "prompt": f"A close-up of a glowing circular pizza divided into 8 equal slices on a space station table. One quarter of the pizza (two slices) is labelled 'Mork's share', and one of those two slices is further highlighted showing half of that quarter eaten. A small green alien character looks satisfied. {STYLE}"
    },
    {
        "filename": "q5-issue001.png",
        "size": "1024x1024",
        "prompt": f"A large clear analogue clock face floating as a hologram in a spacecraft cockpit, showing exactly 3:15 — the short hour hand just past the 3, the long minute hand pointing straight at the 3. The clock glows with soft golden light. Jake — {JAKE} — studies it carefully with a focused expression. {STYLE}"
    },
    {
        "filename": "q6-issue001.png",
        "size": "1024x1024",
        "prompt": f"Two holographic analogue clocks side by side in a spacecraft cockpit — the first showing 3:15 and the second showing 3:45 with an arrow and '+30 min' label between them. Jake — {JAKE} — looks urgently at the clocks, ready to launch. A countdown timer blinks in the background. {STYLE}"
    },
    {
        "filename": "q7-issue001.png",
        "size": "1024x1024",
        "prompt": f"Six large rocky asteroids floating in space, each one clearly labelled '7 light-seconds wide' with a glowing measurement line across it. The asteroids are dramatic and varied in size but all clearly marked. A small orange spacecraft (Jake's) is visible approaching from the left. {STYLE}"
    },
    {
        "filename": "q8-issue001.png",
        "size": "1024x1024",
        "prompt": f"36 shiny golden star-coins arranged in a neat pile in a spacecraft storage bay, with 4 small piles being counted out equally — 9 coins per pile. Each pile is next to a small green alien figurine. Jake — {JAKE} — oversees the counting with a smile. {STYLE}"
    },
    {
        "filename": "q9-issue001.png",
        "size": "1024x1024",
        "prompt": f"A convoy of rockets in deep space: 3 original rockets at the front, then 4 space stations each with 7 new rockets joining, making 31 total. The rockets are colourful and cartoonish, arranged in a clear visual sequence. Jake — {JAKE} — watches from his cockpit window looking excited. {STYLE}"
    },
    {
        "filename": "q10-issue001.png",
        "size": "1024x1024",
        "prompt": f"Two holographic clocks in a spacecraft cockpit: first clock shows 3:35 labelled 'START warm-up now', second clock shows 4:10 labelled 'Re-entry window opens'. A glowing '35 min' arrow connects them. Jake — {JAKE} — sits at the controls looking intense and determined, Earth visible through the window. {STYLE}"
    },
]

all_images = chapter_images + question_images

def generate_image(prompt, size, filename):
    """Generate an image using DALL-E 3 and save it locally."""
    print(f"\n🎨 Generating: {filename}")
    print(f"   Size: {size}")
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": "standard",
        "response_format": "url"
    }
    
    for attempt in range(2):
        try:
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                image_url = data["data"][0]["url"]
                
                # Download the image
                img_response = requests.get(image_url, timeout=60)
                img_response.raise_for_status()
                
                filepath = IMAGES_DIR / filename
                with open(filepath, "wb") as f:
                    f.write(img_response.content)
                
                print(f"   ✅ Saved: {filepath} ({len(img_response.content)} bytes)")
                return True
            else:
                print(f"   ❌ API error {response.status_code}: {response.text[:200]}")
                if attempt == 0:
                    print("   ⏳ Waiting 30s before retry...")
                    time.sleep(30)
                    
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            if attempt == 0:
                print("   ⏳ Waiting 30s before retry...")
                time.sleep(30)
    
    return False

def get_github_sha(filename):
    """Get current SHA of file on GitHub (returns None if file doesn't exist)."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/images/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        return response.json().get("sha")
    return None

def upload_to_github(filename):
    """Upload a local image to GitHub."""
    filepath = IMAGES_DIR / filename
    
    if not filepath.exists():
        print(f"   ❌ File not found: {filepath}")
        return False
    
    print(f"\n📤 Uploading to GitHub: {filename}")
    
    with open(filepath, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode("utf-8")
    
    sha = get_github_sha(filename)
    if sha:
        print(f"   Found existing file SHA: {sha[:8]}...")
    else:
        print(f"   New file (no existing SHA)")
    
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/images/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json"
    }
    
    body = {
        "message": "Regenerate images with consistent Jake character",
        "content": content_b64
    }
    if sha:
        body["sha"] = sha
    
    for attempt in range(2):
        response = requests.put(url, headers=headers, json=body, timeout=60)
        if response.status_code in (200, 201):
            print(f"   ✅ Uploaded successfully")
            return True
        else:
            print(f"   ❌ GitHub upload error {response.status_code}: {response.text[:300]}")
            if attempt == 0:
                print("   ⏳ Waiting 10s before retry...")
                time.sleep(10)
    
    return False

def main():
    print("🚀 Math Blast Issue #1 — Image Regeneration")
    print(f"   Generating {len(all_images)} images total")
    print(f"   Images directory: {IMAGES_DIR}")
    
    generated = []
    failed = []
    
    for i, img in enumerate(all_images):
        success = generate_image(img["prompt"], img["size"], img["filename"])
        if success:
            generated.append(img["filename"])
        else:
            failed.append(img["filename"])
        
        # Sleep 13 seconds between ALL generation calls (except after the last one)
        if i < len(all_images) - 1:
            print(f"   ⏳ Sleeping 13 seconds (rate limit)...")
            time.sleep(13)
    
    print(f"\n\n📊 Generation Summary:")
    print(f"   ✅ Generated: {len(generated)}/{len(all_images)}")
    print(f"   ❌ Failed: {len(failed)}")
    if failed:
        print(f"   Failed files: {failed}")
    
    if not generated:
        print("No images generated, aborting upload.")
        sys.exit(1)
    
    # Upload all successfully generated images to GitHub
    print(f"\n\n🌐 Uploading {len(generated)} images to GitHub...")
    uploaded = []
    upload_failed = []
    
    for filename in generated:
        success = upload_to_github(filename)
        if success:
            uploaded.append(filename)
        else:
            upload_failed.append(filename)
        # Small delay between GitHub uploads
        time.sleep(2)
    
    print(f"\n\n📊 Upload Summary:")
    print(f"   ✅ Uploaded: {len(uploaded)}/{len(generated)}")
    print(f"   ❌ Failed: {len(upload_failed)}")
    if upload_failed:
        print(f"   Upload failed: {upload_failed}")
    
    # Write memory log
    memory_file = Path("/Users/leohiem/.openclaw/workspace/memory/2026-03-26.md")
    memory_file.parent.mkdir(parents=True, exist_ok=True)
    
    mode = "a" if memory_file.exists() else "w"
    with open(memory_file, mode) as f:
        f.write(f"\n\n## Math Blast — Image Regeneration (consistent Jake character)\n")
        f.write(f"- Regenerated all 15 images for Issue #1 with locked Jake character description\n")
        f.write(f"- Jake: 10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet, red rocket patch\n")
        f.write(f"- 5 chapter images (1792x1024): ch1 through ch5\n")
        f.write(f"- 10 question images (1024x1024): q1 through q10\n")
        f.write(f"- Generated: {len(generated)}/15 | Uploaded to GitHub: {len(uploaded)}/{len(generated)}\n")
        if failed:
            f.write(f"- Generation failures: {failed}\n")
        if upload_failed:
            f.write(f"- Upload failures: {upload_failed}\n")
        f.write(f"- Repo: https://github.com/{GITHUB_REPO}\n")
    
    print(f"\n\n✅ Done! Memory log updated at {memory_file}")
    
    if failed or upload_failed:
        sys.exit(1)

if __name__ == "__main__":
    main()
