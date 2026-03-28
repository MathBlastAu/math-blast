#!/usr/bin/env python3
"""Regenerate all 15 Math Blast Issue #1 images using gpt-image-1."""

import openai
import os
import time
import requests
import base64

client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])

IMAGES_DIR = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/'
REFERENCE_IMG = IMAGES_DIR + 'ch1-crashed-rocket.png'
GITHUB_TOKEN = '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'
GITHUB_REPO = 'MathBlastAu/math-blast'

JAKE = "Jake, a 10-year-old boy with short messy brown hair, bright green eyes, light freckles across his nose, bright orange space suit with silver trim, red rocket patch on left shoulder"
BOLT = "Bolt, a small friendly silver robot with glowing blue eyes, round head, and chunky cartoon proportions"
STYLE = "Pixar 3D animation style, vibrant colours, soft warm lighting, child-friendly, cinematic quality"

def save_image(result, filename):
    """Save image from API result to disk."""
    import base64 as b64
    path = IMAGES_DIR + filename
    image_data = b64.b64decode(result.data[0].b64_json)
    with open(path, 'wb') as f:
        f.write(image_data)
    print(f"  ✅ Saved {filename} ({len(image_data)//1024}KB)")
    return path

def generate_with_jake(prompt, filename, size="1024x1024"):
    """Generate image using reference image for Jake consistency."""
    print(f"\n🎨 Generating {filename} (with Jake reference, size={size})...")
    try:
        with open(REFERENCE_IMG, 'rb') as ref:
            result = client.images.edit(
                model="gpt-image-1",
                image=ref,
                prompt=prompt,
                size=size
            )
        return save_image(result, filename)
    except Exception as e:
        print(f"  ⚠️  Error: {e}")
        if "1536x1024" in size:
            print(f"  ↩️  Retrying with 1024x1024...")
            time.sleep(5)
            with open(REFERENCE_IMG, 'rb') as ref:
                result = client.images.edit(
                    model="gpt-image-1",
                    image=ref,
                    prompt=prompt,
                    size="1024x1024"
                )
            return save_image(result, filename)
        raise

def generate_scene(prompt, filename, size="1024x1024"):
    """Generate a pure scene/object image without Jake reference."""
    print(f"\n🎨 Generating {filename} (scene, size={size})...")
    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size,
            quality="high"
        )
        return save_image(result, filename)
    except Exception as e:
        print(f"  ⚠️  Error: {e}")
        if "1536x1024" in size:
            print(f"  ↩️  Retrying with 1024x1024...")
            time.sleep(5)
            result = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1024",
                quality="high"
            )
            return save_image(result, filename)
        raise

def upload_to_github(local_path, filename):
    """Upload image to GitHub, getting SHA first if file exists."""
    print(f"  📤 Uploading {filename} to GitHub...")
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/images/{filename}"
    
    r = requests.get(url, headers=headers)
    sha = r.json().get("sha") if r.status_code == 200 else None
    
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    
    body = {
        "message": f"Regen {filename} with gpt-image-1 character consistency",
        "content": content
    }
    if sha:
        body["sha"] = sha
    
    resp = requests.put(url, json=body, headers=headers)
    if resp.status_code in (200, 201):
        print(f"  ✅ Uploaded {filename} to GitHub")
    else:
        print(f"  ❌ Upload failed for {filename}: {resp.status_code} {resp.text[:200]}")

def sleep_between_calls(seconds=13):
    print(f"  ⏳ Waiting {seconds}s (rate limit)...")
    time.sleep(seconds)

# =========================================================================
# IMAGES LIST
# =========================================================================
# Each entry: (filename, prompt, has_jake, size)
images = [
    # ---- CHAPTER IMAGES (wide format with Jake) ----
    (
        "ch1-crashed-rocket.png",
        f"{JAKE} floats in zero gravity inside a damaged spacecraft cockpit, looking worried but determined at a cracked control panel with sparking wires, stars visible through cracked windshield, {BOLT} hovers beside him. {STYLE}",
        True, "1536x1024"
    ),
    (
        "ch2-alien-feast.png",
        f"{JAKE} stands in a colourful alien marketplace on a space station, surrounded by bizarre exotic alien fruits on floating market stalls, friendly multi-armed alien creatures wave at him, {BOLT} stands beside Jake looking curious. {STYLE}",
        True, "1536x1024"
    ),
    (
        "ch3-launch-window.png",
        f"{JAKE} sits at a glowing mission control console, pointing at a holographic countdown clock showing 12:45, large window showing stars and a planet behind him, {BOLT} points at the clock too. {STYLE}",
        True, "1536x1024"
    ),
    (
        "ch4-asteroid-belt.png",
        f"{JAKE} pilots a small orange spacecraft through a dramatic asteroid belt, hands on controls, looking focused and excited, large rocky asteroids float around the ship, {BOLT} is co-pilot gripping the seat. {STYLE}",
        True, "1536x1024"
    ),
    (
        "ch5-earth-landing.png",
        f"{JAKE} stands triumphantly on a landing pad arms raised in victory, blue and green Earth visible behind him through a glass dome, {BOLT} does a little celebration dance beside him, mission complete banner visible. {STYLE}",
        True, "1536x1024"
    ),
    # ---- QUESTION IMAGES ----
    # Q1: Skip counting 5,10,15,__,25,__ — Jake at computer
    (
        "q1-issue001.png",
        f"{JAKE} looks at a glowing holographic mission computer screen showing the number sequence '5, 10, 15, ?, 25, ?' with fuel crystal icons next to each number, the question marks glowing orange, {BOLT} points at the screen curiously. {STYLE}",
        True, "1024x1024"
    ),
    # Q2: 24 fuel crystals in 4 rows of 6 — pure object
    (
        "q2-issue001.png",
        f"A clear visual arrangement of 24 glowing blue fuel crystals neatly arranged in 4 rows of 6 crystals each on a spacecraft floor, crystals sparkle and glow, space background visible, no characters, counting diagram style. {STYLE}",
        False, "1024x1024"
    ),
    # Q3: Pizza divided into 4 equal quarters — pure object
    (
        "q3-issue001.png",
        f"A large glowing alien space pizza cut into exactly 4 equal slices on a floating alien market stall, each slice identical with colourful alien toppings, one slice slightly separated to show it is 1/4, top-down view, bright colours. {STYLE}",
        False, "1024x1024"
    ),
    # Q4: Pizza showing 1/8 (half of 1/4) highlighted
    (
        "q4-issue001.png",
        f"A large alien pizza cut into 8 equal slices, one single slice highlighted in bright gold to show 1/8, with a visual diagram showing first the pizza split into 4 (quarters), then one quarter split in half, educational diagram style, colourful and clear. {STYLE}",
        False, "1024x1024"
    ),
    # Q5: Clock showing 3:15
    (
        "q5-issue001.png",
        f"A large clearly readable analog spacecraft cockpit clock showing exactly 3:15, the short hour hand just past the 3 and the long minute hand pointing at the 3, glowing digital-style clock face with clear numbers 1-12 around the face, blue glowing clock in a spacecraft dashboard. {STYLE}",
        False, "1024x1024"
    ),
    # Q6: Clock showing 3:45 (3:15 + 30 minutes)
    (
        "q6-issue001.png",
        f"Two glowing spacecraft cockpit clocks side by side, the left clock showing 3:15 and the right clock showing 3:45, a bright arrow between them labelled '+30 min', both clock faces very clear with hour and minute hands visible, educational time diagram style, space cockpit background. {STYLE}",
        False, "1024x1024"
    ),
    # Q7: 6 asteroids × 7 wide — show 6 asteroids with size labels
    (
        "q7-issue001.png",
        f"Six large rocky asteroids floating in a row in deep space, each asteroid has a glowing label showing '7 light-seconds', a small orange spacecraft flies toward them from the left, asteroids vary in texture and colour, dramatic space background. {STYLE}",
        False, "1024x1024"
    ),
    # Q8: 36 star-coins divided into 4 groups of 9 — Jake with coins
    (
        "q8-issue001.png",
        f"{JAKE} sits in the spacecraft storage bay surrounded by 36 shiny gold star-coins arranged in 4 equal groups of 9, each group clearly separated, coins sparkle with stars on their faces, Jake counts them with a smile. {STYLE}",
        True, "1024x1024"
    ),
    # Q9: Convoy of rockets — 4 stations × 7 rockets + 3 = 31 total
    (
        "q9-issue001.png",
        f"A dramatic space scene showing a convoy of rockets in space, 4 glowing space stations in a line with 7 small rockets launching from each station, plus 3 rockets at the front leading the convoy, stars and nebula in background, epic scale, birds-eye view. {STYLE}",
        False, "1024x1024"
    ),
    # Q10: Clock showing 3:35 (4:10 - 35 minutes = 3:35)
    (
        "q10-issue001.png",
        f"A large glowing spacecraft dashboard clock showing exactly 3:35, the short hour hand between 3 and 4 (closer to 4), the long minute hand pointing at the 7, below the clock a visual showing '4:10 minus 35 minutes equals 3:35', dramatic red warning light glowing around the clock showing urgency. {STYLE}",
        False, "1024x1024"
    ),
]

# =========================================================================
# MAIN LOOP
# =========================================================================
results = []
for i, (filename, prompt, has_jake, size) in enumerate(images):
    print(f"\n{'='*60}")
    print(f"[{i+1}/{len(images)}] {filename}")
    
    try:
        if has_jake:
            local_path = generate_with_jake(prompt, filename, size)
        else:
            local_path = generate_scene(prompt, filename, size)
        
        upload_to_github(local_path, filename)
        results.append({"file": filename, "status": "✅ OK", "has_jake": has_jake})
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        results.append({"file": filename, "status": f"❌ FAILED: {str(e)[:100]}", "has_jake": has_jake})
    
    # Rate limiting: sleep between calls (skip after last image)
    if i < len(images) - 1:
        sleep_between_calls(13)

# =========================================================================
# SUMMARY
# =========================================================================
print("\n" + "="*60)
print("FINAL SUMMARY")
print("="*60)
jake_images = [r for r in results if r["has_jake"]]
scene_images = [r for r in results if not r["has_jake"]]

print(f"\nJake images ({len(jake_images)}):")
for r in jake_images:
    print(f"  {r['status']} {r['file']}")

print(f"\nScene images ({len(scene_images)}):")
for r in scene_images:
    print(f"  {r['status']} {r['file']}")

ok_count = sum(1 for r in results if "✅" in r["status"])
fail_count = sum(1 for r in results if "❌" in r["status"])
print(f"\nTotal: {ok_count}/{len(results)} succeeded, {fail_count} failed")

# Write summary to memory
import datetime
summary = f"""
## Math Blast Image Regeneration — gpt-image-1 with Character Consistency
**Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
**Task:** Regenerate all 15 images for Math Blast Issue #1

### Results
| File | Status | Jake? |
|------|--------|-------|
""" + "\n".join(f"| {r['file']} | {r['status']} | {'Yes' if r['has_jake'] else 'No'} |" for r in results) + f"""

**Jake images:** ch1-ch5 (5 chapter images), q1, q8 = 7 total
**Scene images:** q2, q3, q4, q5, q6, q7, q9, q10 = 8 total
**Method:** images.edit (Jake), images.generate (scenes), model=gpt-image-1
**Rate:** 13s between calls
**Succeeded:** {ok_count}/{len(results)}
"""

memory_file = '/Users/leohiem/.openclaw/workspace/memory/2026-03-26.md'
try:
    with open(memory_file, 'a') as f:
        f.write(summary)
    print(f"\n📝 Summary appended to {memory_file}")
except Exception as e:
    print(f"\n⚠️  Could not write memory: {e}")
    # Try creating it
    try:
        os.makedirs(os.path.dirname(memory_file), exist_ok=True)
        with open(memory_file, 'w') as f:
            f.write(f"# Memory: 2026-03-26\n{summary}")
        print(f"📝 Created {memory_file}")
    except Exception as e2:
        print(f"❌ Could not create memory file: {e2}")

print("\n🚀 Done!")
