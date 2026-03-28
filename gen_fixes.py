#!/usr/bin/env python3
"""Fix audio and image issues for Issue 1 narrated edition."""

import os, json, time, urllib.request, urllib.error, base64

API_KEY    = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
OPENAI_KEY = open(os.path.expanduser("~/.openclaw/workspace/credentials/google-token-art.json")).read() if False else None

# Get OpenAI key from env
import subprocess
OPENAI_KEY = subprocess.check_output("source ~/.zshrc 2>/dev/null; echo $OPENAI_API_KEY", shell=True, executable='/bin/zsh').decode().strip()

MODEL  = "eleven_turbo_v2_5"
ANDREW = "BTEPH6wbWkb66Dys0ry6"
GEORGE = "JBFqnCBsd6RMkjVDRZzb"
NAR    = {"stability": 0.55, "similarity_boost": 0.75}
JAKE   = {"stability": 0.50, "similarity_boost": 0.78}

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "sounds", "issue001")
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "images")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

def gen_audio(filename, voice_id, settings, text, force=False):
    out = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(out) and not force:
        print(f"  ✓ {filename} (exists)")
        return True
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({"text": text, "model_id": MODEL, "voice_settings": settings}).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "xi-api-key": API_KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"
    })
    try:
        with urllib.request.urlopen(req) as r: data = r.read()
        open(out, 'wb').write(data)
        print(f"  ✅ {filename} ({len(data)//1024}kb)")
        return True
    except urllib.error.HTTPError as e:
        print(f"  ❌ {filename}: {e.code} — {e.read().decode()[:100]}")
        return False

def gen_image(filename, prompt, force=False):
    out = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(out) and not force:
        print(f"  ✓ {filename} (exists)")
        return True
    url = "https://api.openai.com/v1/images/generations"
    payload = json.dumps({
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard",
        "response_format": "b64_json"
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        img_data = base64.b64decode(data['data'][0]['b64_json'])
        open(out, 'wb').write(img_data)
        print(f"  ✅ {filename} ({len(img_data)//1024}kb)")
        return True
    except Exception as e:
        print(f"  ❌ {filename}: {e}")
        return False

print("=== FIX 1 & 3: New varied feedback audio ===")
# Generate 6 generic correct responses so cycling never repeats a wrong context
feedback_lines = [
    ("feedback-correct-1.mp3", "Pre-launch check passed! Great work!"),  # Q1 specific - keep
    ("feedback-correct-2.mp3", "Brilliant! Nice work, space cadet!"),
    ("feedback-correct-3.mp3", "That's correct! Outstanding!"),
    ("feedback-correct-4.mp3", "Perfect! You've got this!"),
    ("feedback-correct-5.mp3", "Excellent work, cadet!"),
    ("feedback-correct-6.mp3", "Spot on! Mission continues!"),
]
for fname, text in feedback_lines:
    gen_audio(fname, ANDREW, JAKE, text, force=True)
    time.sleep(0.3)

print("\n=== FIX 5: New win narration ===")
gen_audio("win.mp3", GEORGE, NAR,
    "Mission complete! Jake's rocket touched down on Earth with a perfect landing — "
    "and it was all thanks to YOU! Amazing work, space cadet. "
    "See you at Jake's next adventure, when he discovers a robot factory "
    "hidden in the rings of Saturn!", force=True)
time.sleep(0.3)

print("\n=== FIX 2: Q5 clock image (3:15) ===")
gen_image("q5-issue001-fixed.png",
    "A clear, simple analog clock showing exactly 3:15 (quarter past three). "
    "The short hour hand points just past the 3, the long minute hand points directly at the 3. "
    "Clean white clock face, bold black numbers, dark background, space theme, "
    "cartoon style suitable for children aged 7-10. No text labels.", force=True)
time.sleep(1)

print("\n=== FIX 4: Aliens image for chapter 2 ===")
gen_image("ch2-alien-feast-fixed.png",
    "Three small friendly green aliens sharing a giant glowing pizza with a young boy astronaut in an orange space suit. "
    "The tallest alien wears a tiny purple crown and is bowing. The scene is on an alien planet with a purple sky. "
    "Cartoon style, vibrant colors, fun and friendly, suitable for children aged 7-10. "
    "The aliens have big eyes, small bodies, and look happy and quirky.", force=True)

print("\nDone!")
