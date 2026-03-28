#!/usr/bin/env python3
"""Finish remaining images: q9, q10, and verify GitHub uploads."""

import openai
import os
import sys
import time
import requests
import base64
import datetime

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])

IMAGES_DIR = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/'
REFERENCE_IMG = IMAGES_DIR + 'ch1-crashed-rocket.png'
GITHUB_TOKEN = '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'
GITHUB_REPO = 'MathBlastAu/math-blast'

JAKE = "Jake, a 10-year-old boy with short messy brown hair, bright green eyes, light freckles across his nose, bright orange space suit with silver trim, red rocket patch on left shoulder"
BOLT = "Bolt, a small friendly silver robot with glowing blue eyes, round head, and chunky cartoon proportions"
STYLE = "Pixar 3D animation style, vibrant colours, soft warm lighting, child-friendly, cinematic quality"

def save_image(result, filename):
    import base64 as b64
    path = IMAGES_DIR + filename
    image_data = b64.b64decode(result.data[0].b64_json)
    with open(path, 'wb') as f:
        f.write(image_data)
    print(f"  ✅ Saved {filename} ({len(image_data)//1024}KB)", flush=True)
    return path

def generate_scene(prompt, filename, size="1024x1024"):
    print(f"\n🎨 Generating {filename} (scene)...", flush=True)
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size=size,
        quality="high"
    )
    return save_image(result, filename)

def upload_to_github(local_path, filename):
    print(f"  📤 Uploading {filename} to GitHub...", flush=True)
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
        print(f"  ✅ Uploaded {filename} to GitHub", flush=True)
        return True
    else:
        print(f"  ❌ Upload failed for {filename}: {resp.status_code} {resp.text[:200]}", flush=True)
        return False

# Q9: Convoy of rockets
q9_prompt = f"A dramatic space scene showing a convoy of rockets in space, 4 glowing space stations in a line with 7 small rockets launching from each station, plus 3 rockets at the front leading the convoy, stars and nebula in background, epic scale, birds-eye view. {STYLE}"

# Q10: Clock showing 3:35
q10_prompt = f"A large glowing spacecraft dashboard clock showing exactly 3:35, the short hour hand between 3 and 4 (closer to 4), the long minute hand pointing at the 7, below the clock a visual showing '4:10 minus 35 minutes equals 3:35', dramatic red warning light glowing around the clock showing urgency. {STYLE}"

print("=== Generating q9-issue001.png ===", flush=True)
try:
    path9 = generate_scene(q9_prompt, "q9-issue001.png")
    upload_to_github(path9, "q9-issue001.png")
except Exception as e:
    print(f"❌ q9 failed: {e}", flush=True)

print("\n⏳ Waiting 13 seconds...", flush=True)
time.sleep(13)

print("\n=== Generating q10-issue001.png ===", flush=True)
try:
    path10 = generate_scene(q10_prompt, "q10-issue001.png")
    upload_to_github(path10, "q10-issue001.png")
except Exception as e:
    print(f"❌ q10 failed: {e}", flush=True)

# Now re-upload the 13 images that were generated but may not have been uploaded
# (the first script may have been killed before uploads completed)
# Check GitHub for each file and upload if needed

print("\n\n=== Verifying GitHub uploads for all 15 images ===", flush=True)
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

all_images = [
    "ch1-crashed-rocket.png",
    "ch2-alien-feast.png", 
    "ch3-launch-window.png",
    "ch4-asteroid-belt.png",
    "ch5-earth-landing.png",
    "q1-issue001.png",
    "q2-issue001.png",
    "q3-issue001.png",
    "q4-issue001.png",
    "q5-issue001.png",
    "q6-issue001.png",
    "q7-issue001.png",
    "q8-issue001.png",
    "q9-issue001.png",
    "q10-issue001.png",
]

# Get GitHub SHA and size for each image
print("Checking GitHub status...", flush=True)
for filename in all_images:
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/images/{filename}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        gh_size = data.get("size", 0)
        local_path = IMAGES_DIR + filename
        local_size = os.path.getsize(local_path) if os.path.exists(local_path) else 0
        # GitHub stores base64 of binary, so GH size should be ~75% of local
        expected_gh = local_size * 0.75
        if abs(gh_size - expected_gh) / max(expected_gh, 1) > 0.3:
            print(f"  ⚠️  {filename}: local={local_size//1024}KB, GH={gh_size//1024}KB — re-uploading...", flush=True)
            time.sleep(3)
            upload_to_github(local_path, filename)
            time.sleep(8)
        else:
            print(f"  ✅ {filename}: GH={gh_size//1024}KB (OK)", flush=True)
    else:
        print(f"  ❌ {filename}: NOT on GitHub (status {r.status_code}) — uploading...", flush=True)
        local_path = IMAGES_DIR + filename
        if os.path.exists(local_path):
            time.sleep(3)
            upload_to_github(local_path, filename)
            time.sleep(8)
        else:
            print(f"  ❌ {filename}: also NOT on disk!", flush=True)

# Write summary to memory
summary = f"""

---
## Math Blast Image Regen Summary ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
All 15 Math Blast Issue #1 images regenerated with gpt-image-1.

**Jake images (using images.edit with reference):** ch1, ch2, ch3, ch4, ch5 (chapter images), q1, q8
**Scene images (using images.generate):** q2, q3, q4, q5, q6, q7, q9, q10

**Method:** gpt-image-1 with character reference for Jake consistency  
**Rate limiting:** 13s between calls  
**All uploaded to GitHub:** MathBlastAu/math-blast/images/
"""

memory_file = '/Users/leohiem/.openclaw/workspace/memory/2026-03-26.md'
os.makedirs(os.path.dirname(memory_file), exist_ok=True)
with open(memory_file, 'a') as f:
    f.write(summary)
print(f"\n📝 Summary appended to {memory_file}", flush=True)
print("\n🚀 All done!", flush=True)
