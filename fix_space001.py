#!/usr/bin/env python3
"""Fix all Space Issue 1 audio and image issues."""
import requests, os, time, base64
from openai import OpenAI

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
AUDIO_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/sounds/issue001/")
IMG_DIR   = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/images/")
client = OpenAI()

VOICES = {
    "jake":     ("BTEPH6wbWkb66Dys0ry6", {"stability": 0.55, "similarity_boost": 0.80, "style": 0.35}),
    "narrator": ("JBFqnCBsd6RMkjVDRZzb", {"stability": 0.60, "similarity_boost": 0.75, "style": 0.20}),
}

def gen_audio(filename, character, text, force=False):
    path = AUDIO_DIR + filename + ".mp3"
    if os.path.exists(path) and not force:
        os.remove(path)  # always regenerate for fixes
    voice_id, settings = VOICES[character]
    print(f"  🎙 {filename}...")
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={"text": text, "model_id": "eleven_turbo_v2_5", "voice_settings": settings}
    )
    if r.status_code == 200:
        with open(path, "wb") as f: f.write(r.content)
        print(f"  ✅ {filename}.mp3 ({len(r.content):,}b)")
    else:
        print(f"  ❌ {r.status_code}: {r.text[:80]}")
    time.sleep(1)

def gen_img(filename, prompt, size="1024x1024", force=True):
    path = IMG_DIR + filename
    if os.path.exists(path) and not force: print(f"  ⏭ {filename}"); return
    print(f"  🖼 {filename}...")
    try:
        r = client.images.generate(model="gpt-image-1", prompt=prompt, size=size)
        data = base64.b64decode(r.data[0].b64_json)
        with open(path, 'wb') as f: f.write(data)
        print(f"  ✅ {filename} ({len(data):,}b)")
        time.sleep(12)
    except Exception as e:
        print(f"  ❌ {e}")

JAKE = (
    "10-year-old boy named Jake: short messy brown hair, warm fair skin, "
    "bright orange space cadet jumpsuit with silver accent panels, rocket badge on chest, "
    "Disney Pixar CGI 3D animation style"
)
PRIYA = (
    "adult woman named Priya: mid-40s, Indian-Australian, dark hair tied back, "
    "navy-blue fuel officer uniform with gold rank insignia, "
    "Disney Pixar CGI 3D animation style"
)
SETTING = (
    "futuristic Kepler Station space refuelling depot, large observation windows showing a red dwarf star, "
    "industrial fuel tanks with glowing displays, Disney Pixar CGI 3D animation style"
)

print("\n=== AUDIO FIXES ===")

# Fix 1: Regenerate Jake clips with voice artifact — use a longer lead-in pause workaround
gen_audio("ch1-jake-arrival", "jake",
    "Alright, alright — I've got this. Kepler Station, Fuel Inspection Mission, first solo assignment. Let's see what we're dealing with.")

gen_audio("ch1-jake-response", "jake",
    "Fractions I can do. Let me start with my own ship's gauge — if I can read that, I can read anything. My tank is divided into 4 equal sections. Let me check how many are full.")

# Fix 3: Missing ch2 Jake clip
gen_audio("ch2-jake-calculates", "jake",
    "Let me calculate this carefully.")

# Fix 8: Regenerate win with corrected text
gen_audio("win", "narrator",
    "Jake Nova had cracked the fuel mystery at Kepler Station — every gauge read, every fraction calculated. "
    "Join us for Issue Two, when Jake tracks the stolen fuel into the Fog Nebula. "
    "The Fraction Phantom is out there. And it's only just getting started.")

print("\n=== IMAGE FIXES ===")

# Fix 2: q1 — MUST show exactly 4 equal rectangular sections, 1 filled
gen_img("q1-issue001.png",
    "Flat clean digital illustration. A simple horizontal rectangular fuel gauge bar. "
    "The bar is divided into EXACTLY 4 equal vertical sections by thin white lines. "
    "The LEFTMOST 1 section is filled solid bright green. "
    "The remaining 3 sections on the right are empty dark grey. "
    "Jake (10-year-old boy in orange space jumpsuit, Disney Pixar CGI style) stands beside it pointing at it. "
    "Clean white background with subtle space station elements. No text, no numbers, no labels in the image.")

# Fix 4: q3 — MUST show exactly 8 sections, 3 filled
gen_img("q3-issue001.png",
    "Flat clean digital illustration. A simple horizontal rectangular fuel gauge bar. "
    "The bar is divided into EXACTLY 8 equal vertical sections by thin white lines. "
    "The LEFTMOST 3 sections are filled solid bright green. "
    "The remaining 5 sections on the right are empty dark grey. "
    "Jake (10-year-old boy in orange space jumpsuit, Disney Pixar CGI style) studies it with a thoughtful expression. "
    "Clean space station background. No text, no numbers, no fraction labels anywhere in the image.")

# Fix 5: q4 — show before (4/4 full) and after (3/4 full) side by side
gen_img("q4-issue001.png",
    "Flat clean digital illustration. Two horizontal rectangular fuel gauge bars side by side, labelled BEFORE and AFTER with small arrows. "
    "LEFT bar (BEFORE): divided into EXACTLY 4 equal sections, ALL 4 sections filled bright green. "
    "RIGHT bar (AFTER): divided into EXACTLY 4 equal sections, only 3 sections filled green, 1 section on the right is empty dark grey with a red glow indicating removal. "
    "A small glowing red arrow between the two bars shows something was removed. "
    "Jake (Disney Pixar CGI style orange jumpsuit) looks at it with wide eyes. "
    "No fraction numbers or text visible. Space station background.")

# Fix 6 (second): q5 — show before (2/4) and after (1/4) side by side  
gen_img("q5-issue001.png",
    "Flat clean digital illustration. Two horizontal rectangular fuel gauge bars side by side. "
    "LEFT bar (BEFORE): divided into EXACTLY 4 equal sections, 2 sections on the left filled bright green, 2 sections on the right empty dark grey. "
    "RIGHT bar (AFTER): divided into EXACTLY 4 equal sections, only 1 section on the left filled green, 3 sections empty dark grey with red glow indicating removal. "
    "A glowing red arrow between the two shows something was taken. "
    "Jake (Disney Pixar CGI orange jumpsuit) looks surprised and thoughtful. "
    "No fraction numbers or text visible. Space station background.")

# Fix 7: q9 — show 3 separate tanks each with 1 section removed from 4
gen_img("q9-issue001.png",
    "Flat clean digital illustration. Three identical horizontal rectangular fuel gauge bars stacked vertically. "
    "Each bar is divided into EXACTLY 4 equal sections. "
    "In each bar, 3 sections are filled bright green and 1 section (the rightmost) is highlighted red/removed. "
    "The 3 removed sections are shown collected together with a glowing arrow pointing to a single combined bar on the side. "
    "Jake (Disney Pixar CGI orange jumpsuit) counts the removed sections on his fingers. "
    "No fraction numbers or text visible. Space station background.")

# Fix 6 (first): ch5 opening needs a NEW image — Priya handing Jake the printout
gen_img("ch5-printout.png",
    "Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{PRIYA} holds a glowing holographic printout showing transfer log data (glowing lines, no readable text). "
    f"Her expression is grim and serious. "
    f"{JAKE} leans in to read it, expression: stomach-dropping realisation, eyes wide. "
    f"{SETTING}. "
    "The printout casts a blue glow on both their faces. Dramatic atmosphere, slightly dark lighting.",
    size="1536x1024")

print("\nAll fixes done.")
