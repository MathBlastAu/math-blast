#!/usr/bin/env python3
"""
Math Blast Build Script
- Task 1: Generate 10 question images for Issue #1, create v3 HTML with Y3/Y4 badges
- Task 2: Generate 15 images for Issue #2, create Issue #2 HTML
- Push everything to GitHub
"""

import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error

# Config
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GITHUB_TOKEN = "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"
GITHUB_REPO = "MathBlastAu/math-blast"
IMAGES_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"
PROJECT_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast"

os.makedirs(IMAGES_DIR, exist_ok=True)

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def generate_image(prompt, filename, size="1024x1024", retries=2):
    """Generate image with DALL-E 3, save as PNG, return True on success."""
    filepath = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        log(f"  SKIP (exists): {filename}")
        return True
    
    log(f"  Generating: {filename}")
    
    for attempt in range(retries):
        try:
            payload = json.dumps({
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": size,
                "response_format": "b64_json"
            }).encode()
            
            req = urllib.request.Request(
                "https://api.openai.com/v1/images/generations",
                data=payload,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                }
            )
            
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
                img_data = base64.b64decode(result["data"][0]["b64_json"])
                with open(filepath, "wb") as f:
                    f.write(img_data)
                log(f"  Saved: {filename} ({len(img_data)//1024}KB)")
                return True
                
        except Exception as e:
            log(f"  ERROR attempt {attempt+1}: {e}")
            if attempt < retries - 1:
                log("  Retrying in 30s...")
                time.sleep(30)
    
    log(f"  FAILED: {filename}")
    return False

def github_upload(local_path, repo_path, commit_msg):
    """Upload a file to GitHub via Contents API."""
    filename = os.path.basename(local_path)
    with open(local_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()
    
    # Check if file already exists (need SHA for update)
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{repo_path}"
    sha = None
    try:
        req = urllib.request.Request(url, headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "User-Agent": "MathBlastBuilder"
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            existing = json.loads(resp.read())
            sha = existing.get("sha")
    except:
        pass
    
    payload = {"message": commit_msg, "content": content_b64}
    if sha:
        payload["sha"] = sha
    
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        method="PUT",
        headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "MathBlastBuilder"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            log(f"  GitHub upload OK: {repo_path}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read()
        log(f"  GitHub upload FAILED {repo_path}: {e.code} - {body[:200]}")
        return False

def github_upload_text(content_str, repo_path, commit_msg):
    """Upload text content to GitHub."""
    content_b64 = base64.b64encode(content_str.encode()).decode()
    
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{repo_path}"
    sha = None
    try:
        req = urllib.request.Request(url, headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "User-Agent": "MathBlastBuilder"
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            existing = json.loads(resp.read())
            sha = existing.get("sha")
    except:
        pass
    
    payload = {"message": commit_msg, "content": content_b64}
    if sha:
        payload["sha"] = sha
    
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        method="PUT",
        headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "MathBlastBuilder"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            log(f"  GitHub upload OK: {repo_path}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read()
        log(f"  GitHub upload FAILED {repo_path}: {e.code} - {body[:200]}")
        return False

# ======================================================================
# IMAGE PROMPTS
# ======================================================================

ISSUE1_IMAGES = [
    ("q1-issue001.png", "1024x1024",
     "Pixar-style 3D animated space adventure illustration. A futuristic rocket cockpit interior with a glowing blue computer screen showing a number countdown sequence: 5, 10, 15, blank space, 25, blank space. The numbers glow in bright yellow-green on a cosmic blue screen. Cute astronaut Jake in a white helmet visible in the background. Bright, colorful, child-friendly. No text overlay."),
    
    ("q2-issue001.png", "1024x1024",
     "Pixar-style 3D animated space illustration. On the rocky surface of a purple alien planet, 4 neat rows of 6 glowing cyan fuel crystals are arranged in a perfect grid (4 rows x 6 crystals = 24 total). Each crystal sparkles and glows. Cute astronaut Jake kneels next to them, looking happy. Stars visible in background. Bright, colorful, child-friendly. No text."),
    
    ("q3-issue001.png", "1024x1024",
     "Pixar-style 3D animated illustration. Astronaut Jake and three small cute green aliens (Bloop with a purple crown, Zibble, and Mork) sit around a floating glowing pizza in space. The pizza is clearly divided into exactly 4 equal slices. Each character has one slice in front of them. Joyful expressions, stars and nebulas in background. Bright, colorful, child-friendly. No text."),
    
    ("q4-issue001.png", "1024x1024",
     "Pixar-style 3D animated illustration. A cute small green alien called Mork holds one triangular pizza slice (labeled as 1/4 of a pizza). He has eaten only half of his slice, leaving a tiny piece. A thought bubble shows the pizza divided into 8 pieces with one tiny piece highlighted. Space setting with stars. Curious, charming expression on Mork's face. Bright, colorful, child-friendly. No text."),
    
    ("q5-issue001.png", "1024x1024",
     "Pixar-style 3D animated illustration. Close-up of a glowing futuristic analog clock mounted on a spaceship cockpit dashboard. The clock clearly shows 3:15 - short hand just past 3, long hand pointing at 3. The clock face glows green and purple. Dashboard buttons and stars visible in background. Astronaut Jake's hand pointing nervously at the clock. Bright, colorful, child-friendly. No text on clock face except numbers 1-12."),
    
    ("q6-issue001.png", "1024x1024",
     "Pixar-style 3D animated illustration. Jake's bright orange-and-white rocket sits on a purple alien planet launch pad, engines beginning to glow and fire up. A large glowing holographic countdown window display floats above showing a timer. Alien landscape with purple sky and stars. Jake visible in cockpit window giving thumbs up. Dramatic but fun atmosphere. Bright, colorful, child-friendly. No text."),
    
    ("q7-issue001.png", "1024x1024",
     "Pixar-style 3D animated illustration. In deep space, exactly 6 large dramatic spinning asteroids are lined up in a row blocking a spaceship's path. Each asteroid is rocky, cratered, and massive. Jake's small cute rocket approaches from the left side, looking tiny compared to the asteroids. Colorful nebula in background. Tense but fun atmosphere. Bright, colorful, child-friendly. No text."),
    
    ("q8-issue001.png", "1024x1024",
     "Pixar-style 3D animated illustration. Astronaut Jake stands in his spaceship cargo bay holding a pile of 36 shiny golden star-shaped coins. In front of him, 4 cute green aliens (Bloop, Zibble, Mork, and one more) stand in a line with outstretched little hands, eager to receive their equal share. Jake looks thoughtful, counting. Stars visible through a porthole window. Bright, colorful, child-friendly. No text."),
    
    ("q9-issue001.png", "1024x1024",
     "Pixar-style 3D animated illustration. A bird's-eye view of space showing 4 glowing space stations in a line, each with 7 small rockets docked around them like a flower pattern. Plus 3 more rockets flying nearby. All rockets form a grand convoy heading toward Earth (visible in background, small and glowing blue-green). Epic space convoy scene. Bright, colorful, child-friendly. No text."),
    
    ("q10-issue001.png", "1024x1024",
     "Pixar-style 3D animated illustration. Jake sits in his rocket cockpit, looking intently at a large glowing clock on the dashboard showing 4:10. His heat shield glowing orange through the windshield. Earth visible through the window - beautiful blue-green marble close up. Jake holds a maths notebook open with calculations. Dramatic but exciting final approach scene. Bright, colorful, child-friendly. No text."),
]

ISSUE2_CHAPTER_IMAGES = [
    ("ch1-robot-factory.png", "1792x1024",
     "Pixar-style 3D animated wide cinematic illustration. Astronaut Jake's bright orange-and-white rocket ship and his robot co-pilot Bolt (a cute round silver robot with glowing blue eyes) approach Saturn's magnificent rings in their small spacecraft. Saturn looms large and golden-yellow with beautiful ring bands. Stars and space dust sparkle. Epic space adventure mood. Bright, colorful, child-friendly. No text. Wide panoramic view."),
    
    ("ch2-robot-factory.png", "1792x1024",
     "Pixar-style 3D animated wide cinematic illustration. Interior of a vast alien robot factory hidden inside Saturn's rings. Enormous factory floor with dozens of dormant silver robots standing in neat rows and columns, all powered off with dark eyes. Dust motes float in shafts of amber light. Jake and Bolt (cute round silver robot) stand at the entrance looking amazed. Industrial alien machinery all around. Bright colors in an otherwise dark factory. Child-friendly. No text."),
    
    ("ch3-robot-factory.png", "1792x1024",
     "Pixar-style 3D animated wide cinematic illustration. The alien robot factory is beginning to power up! Machinery glows, sparks fly from old gears, conveyor belts start moving. Bright electric blue and orange sparks cascade from giant machines. Jake pulls a large lever while Bolt (cute round silver robot) watches with glowing excited eyes. Smoke and energy beams fill the air. Dramatic and exciting. Bright, colorful, child-friendly. No text."),
    
    ("ch4-robot-factory.png", "1792x1024",
     "Pixar-style 3D animated wide cinematic illustration. The factory floor is alive! An army of cute little silver robots march in perfect formation - rows and columns of robots with glowing eyes, marching in sync. Jake stands on an elevated platform conducting them like an orchestra. Bolt stands proudly beside Jake. Factory lights flash green. Epic and joyful scene. Bright, colorful, child-friendly. No text."),
    
    ("ch5-robot-factory.png", "1792x1024",
     "Pixar-style 3D animated wide cinematic illustration. The robot factory is fully operational and glorious! Assembly lines hum, robots work happily, lights glow green everywhere. At the center, Bolt the robot co-pilot stands on a pedestal getting an upgrade - his chest panel glows brilliant gold and white with new power. Jake watches proudly with arms crossed and a huge grin. Celebratory atmosphere with confetti and light beams. Bright, colorful, child-friendly. No text."),
]

ISSUE2_QUESTION_IMAGES = [
    ("q1-issue002.png", "1024x1024",
     "Pixar-style 3D animated illustration. Bolt the cute round silver robot holds up a glowing holographic display showing a fuel pod divided into 4 equal sections, with 1 section highlighted in bright yellow. Around him are 8 cylindrical glowing fuel pods on a shelf. He scratches his head with one metal arm, thinking. Robot factory background with soft lighting. Bright, colorful, child-friendly. No text."),
    
    ("q2-issue002.png", "1024x1024",
     "Pixar-style 3D animated illustration. Inside the robot factory, exactly 3 rows of 4 dormant silver robots stand in a perfect grid arrangement on the factory floor (3 rows × 4 columns = 12 robots total). They are inactive with closed eyes, covered in dust. Jake looks at them with a clipboard. The grid arrangement is very clear. Bright factory lighting. Bright, colorful, child-friendly. No text."),
    
    ("q3-issue002.png", "1024x1024",
     "Pixar-style 3D animated illustration. A tall metallic assembly rack in the robot factory showing exactly 5 rows of 6 glowing green circuit boards neatly arranged (5 rows × 6 boards = 30 total). Bolt the robot points at the rack excitedly. Shelves are organized and neat. Factory setting with warm orange ambient lighting. Bright, colorful, child-friendly. No text."),
    
    ("q4-issue002.png", "1024x1024",
     "Pixar-style 3D animated illustration. A large factory storage wall showing exactly 4 rows of 7 glowing blue cylindrical power cells in neat slots (4 rows × 7 columns = 28 total). Jake stands to the side counting them on his fingers. Power cells glow blue and pulse with energy. Industrial factory setting. Bright, colorful, child-friendly. No text."),
    
    ("q5-issue002.png", "1024x1024",
     "Pixar-style 3D animated illustration. Three cute boxy transport robots in the factory, each one carrying a stack of exactly 8 orange crates on their backs. The crates are piled neatly. Jake directs the robots with hand gestures. Factory floor with conveyor belts in background. Fun and busy atmosphere. Bright, colorful, child-friendly. No text."),
    
    ("q6-issue002.png", "1024x1024",
     "Pixar-style 3D animated illustration. A cross-section view of 6 factory floors stacked on top of each other like a building. Each floor has exactly 9 mechanical robotic arms extending from the ceiling, all with different tools and claws. Bolt the robot stands in the foreground looking up amazed at all the floors. Colorful factory with glowing indicators. Bright, colorful, child-friendly. No text."),
    
    ("q7-issue002.png", "1024x1024",
     "Pixar-style 3D animated illustration. A large digital factory clock on the wall shows 3 minutes passing. During each minute, 12 silver robots pop up from assembly bays with a spring-loaded bounce and glowing eyes switching on. Jake watches with excitement as more and more robots come online. Progress shown as waves of robot activation. Bright, colorful, child-friendly. No text."),
    
    ("q8-issue002.png", "1024x1024",
     "Pixar-style 3D animated illustration. Two groups of cute silver robots on an assembly line. Each group of robots (shown clearly as 2 batches) has a pile of exactly 24 small silver bolts next to them for assembly. Bolt the robot co-pilot manages a clipboard tracking the bolt inventory. Organized factory setting. Bright, colorful, child-friendly. No text."),
    
    ("q9-issue002.png", "1024x1024",
     "Pixar-style 3D animated illustration. A bird's-eye view of a rectangular factory floor perfectly tiled with glowing floor panels. The grid is clearly 8 tiles long and 7 tiles wide. Some tiles glow brightly and others are darker, making the grid very visible. Jake looks down from a catwalk above, sketching the floor plan. Geometric, clean, satisfying layout. Bright, colorful, child-friendly. No text."),
    
    ("q10-issue002.png", "1024x1024",
     "Pixar-style 3D animated illustration. Two factory floors side by side. Floor 1 shows 3 rows of 5 robots activating (15 robots, glowing green). Floor 2 shows 4 rows of 4 robots activating (16 robots, glowing blue). All robots have happy glowing eyes. Jake and Bolt celebrate in the center as the grand total of robots come online. Epic factory activation scene. Bright, colorful, child-friendly. No text."),
]

# ======================================================================
# TASK 1: Generate Issue #1 images
# ======================================================================

log("=" * 60)
log("TASK 1: Generating Issue #1 question images (10 total)")
log("=" * 60)

for i, (filename, size, prompt) in enumerate(ISSUE1_IMAGES):
    if i > 0:
        log(f"  Sleeping 13s (rate limit)...")
        time.sleep(13)
    generate_image(prompt, filename, size)

log("\nTask 1 images generated. Uploading to GitHub...")
for filename, size, prompt in ISSUE1_IMAGES:
    filepath = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(filepath):
        github_upload(filepath, f"images/{filename}", f"Add {filename}")
        time.sleep(1)  # small delay between uploads

# ======================================================================
# TASK 1: Create issue-001-v3.html
# ======================================================================

log("\nCreating issue-001-v3.html...")

# Read v2 as base
with open(os.path.join(PROJECT_DIR, "issue-001-v2.html"), "r") as f:
    html_v3 = f.read()

# Define badge info and image for each question
# Format: (question_id, year_level, badge_class)
BADGE_STYLE = """
  .yr-badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 900;
    padding: 3px 10px;
    border-radius: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-right: 6px;
  }
  .yr3 { background: rgba(0, 180, 80, 0.2); color: #00cc60; border: 1px solid #00cc60; }
  .yr4 { background: rgba(160, 50, 255, 0.2); color: #bb66ff; border: 1px solid #bb66ff; }
  .question-img {
    display: block;
    max-width: 300px;
    width: 100%;
    margin: 14px auto 18px;
    border-radius: 8px;
    border: 2px solid rgba(123, 47, 255, 0.3);
  }
"""

# Insert badge CSS before closing </style>
html_v3 = html_v3.replace("</style>", BADGE_STYLE + "\n</style>")

# Define patches for each question: (search_string, badge_html, img_filename)
# We'll inject badges into quiz-meta and images after .question divs

def make_badge(level):
    if level == 3:
        return '<span class="yr-badge yr3">Y3</span>'
    else:
        return '<span class="yr-badge yr4">Y4</span>'

def make_img(filename):
    url = f"https://mathblastau.github.io/math-blast/images/{filename}"
    return f'<img src="{url}" alt="Question illustration" class="question-img" />'

# Question badge and image patches
# (quiz_label_text, year_level, img_filename)
patches = [
    ("Warm-Up — Skip Counting", 3, "q1-issue001.png"),
    ("Question 2 — Times Tables", 3, "q2-issue001.png"),
    ("Question 3 — Fractions", 3, "q3-issue001.png"),
    ("Question 4 — Fractions", 4, "q4-issue001.png"),
    ("Question 5 — Telling the Time", 3, "q5-issue001.png"),
    ("Question 6 — Adding Time", 3, "q6-issue001.png"),
    ("Question 7 — Multiplication", 3, "q7-issue001.png"),
    ("Question 8 — Division", 3, "q8-issue001.png"),
    ("Question 9 — Mixed (Multiply then Add)", 4, "q9-issue001.png"),
    ("Question 10 — BOSS: Subtracting Time", 4, "q10-issue001.png"),
]

for label, year, img_file in patches:
    # Add badge to quiz-label div
    old_label = f'<div class="quiz-label">{label}</div>'
    new_label = f'<div class="quiz-label">{make_badge(year)} {label}</div>'
    html_v3 = html_v3.replace(old_label, new_label)
    
    # Add image after the .question div (before the .options div)
    # We'll look for: </div>\n      <div class="options"> pattern right after each question block
    # Actually, let's find the question div and insert image before options
    # Each question ends with </div> and is followed by options

# Insert images after .question div, before .options div
# Strategy: find each "class=\"question\"" block's closing </div> and insert image before <div class="options">
import re

for label, year, img_file in patches:
    # Find the quiz box that contains this label
    # Look for <div class="options"> that follows our specific quiz-label
    badge_label = f'<div class="quiz-label">{make_badge(year)} {label}</div>'
    
    # Find position of this label in the HTML
    pos = html_v3.find(badge_label)
    if pos == -1:
        log(f"  WARNING: Could not find label: {label}")
        continue
    
    # Find the </div> that closes the .question div (it comes after the label)
    # The .question div closes before <div class="options">
    after_label = html_v3[pos:]
    options_pos = after_label.find('<div class="options">')
    if options_pos == -1:
        log(f"  WARNING: Could not find options for: {label}")
        continue
    
    # Find the last </div> before options
    before_options = after_label[:options_pos]
    last_close_div = before_options.rfind('</div>')
    if last_close_div == -1:
        log(f"  WARNING: Could not find closing div for: {label}")
        continue
    
    # Insert image between </div> and <div class="options">
    insert_point = pos + last_close_div + len('</div>')
    img_html = '\n      ' + make_img(img_file)
    html_v3 = html_v3[:insert_point] + img_html + html_v3[insert_point:]

# Save v3
v3_path = os.path.join(PROJECT_DIR, "issue-001-v3.html")
with open(v3_path, "w") as f:
    f.write(html_v3)
log(f"  Saved: issue-001-v3.html ({os.path.getsize(v3_path)//1024}KB)")

# Push v3 to GitHub
github_upload_text(html_v3, "issue-001-v3.html", "Issue #1 v3: question images + Y3/Y4 badges")

# ======================================================================
# TASK 2: Generate Issue #2 images (15 total)
# ======================================================================

log("\n" + "=" * 60)
log("TASK 2: Generating Issue #2 images (15 total)")
log("=" * 60)

# Chapter images first (5 wide images)
log("\nGenerating chapter images...")
for i, (filename, size, prompt) in enumerate(ISSUE2_CHAPTER_IMAGES):
    if i > 0 or True:  # always sleep between calls
        log(f"  Sleeping 13s (rate limit)...")
        time.sleep(13)
    generate_image(prompt, filename, size)

# Question images (10)
log("\nGenerating question images...")
for i, (filename, size, prompt) in enumerate(ISSUE2_QUESTION_IMAGES):
    log(f"  Sleeping 13s (rate limit)...")
    time.sleep(13)
    generate_image(prompt, filename, size)

# Upload all Issue #2 images
log("\nUploading Issue #2 images to GitHub...")
all_issue2_images = ISSUE2_CHAPTER_IMAGES + ISSUE2_QUESTION_IMAGES
for filename, size, prompt in all_issue2_images:
    filepath = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(filepath):
        github_upload(filepath, f"images/{filename}", f"Add {filename}")
        time.sleep(1)

# ======================================================================
# TASK 2: Create issue-002-v1.html
# ======================================================================

log("\nCreating issue-002-v1.html...")

def make_badge_html(level):
    cls = "yr3" if level == 3 else "yr4"
    return f'<span class="yr-badge {cls}">Y{"3" if level == 3 else "4"}</span>'

def make_q_img(filename):
    url = f"https://mathblastau.github.io/math-blast/images/{filename}"
    return f'<img src="{url}" alt="Question illustration" class="question-img" />'

def make_ch_img(filename, alt):
    url = f"https://mathblastau.github.io/math-blast/images/{filename}"
    return f'<img class="chapter-img" src="{url}" alt="{alt}" />'

ISSUE2_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mission: Math Blast 🚀 — Issue #2: The Robot Factory</title>
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: #0d0630;
    font-family: 'Nunito', Arial, sans-serif;
    color: #fff;
    background-image: radial-gradient(ellipse at 50% 0%, rgba(120,0,255,0.2) 0%, transparent 70%);
    min-height: 100vh;
  }

  .starfield { position: fixed; top:0; left:0; right:0; bottom:0; pointer-events:none; z-index:0; overflow:hidden; }
  .star { position:absolute; width:2px; height:2px; background:white; border-radius:50%; opacity:0.6; animation:twinkle 3s infinite alternate; }
  @keyframes twinkle { from{opacity:0.2} to{opacity:0.9} }

  .wrapper { max-width:680px; margin:0 auto; position:relative; z-index:1; padding-bottom:60px; }

  /* TITLE SCREEN */
  .title-screen { text-align:center; padding:48px 24px 36px; }
  .rocket-emoji { font-size:72px; display:block; margin-bottom:16px; animation:float 3s ease-in-out infinite; }
  @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-14px)} }
  .title-screen h1 { font-size:42px; font-weight:900; line-height:1.1; text-shadow:0 0 24px rgba(180,100,255,0.8); }
  .title-screen h1 span { color:#ffdd00; }
  .issue-label { font-size:13px; font-weight:900; color:#aa77ff; letter-spacing:3px; text-transform:uppercase; margin:10px 0 4px; }
  .tagline { font-size:16px; color:#b090e0; margin-bottom:6px; }
  .meta { font-size:13px; color:#6655aa; margin-bottom:30px; }
  .start-btn {
    display:inline-block; background:linear-gradient(135deg,#7b2fff,#ff2fff);
    color:white; font-size:20px; font-weight:900; padding:18px 48px;
    border-radius:50px; border:none; cursor:pointer;
    box-shadow:0 6px 30px rgba(123,47,255,0.5);
    transition:transform 0.15s, box-shadow 0.15s; font-family:'Nunito',Arial,sans-serif;
  }
  .start-btn:hover { transform:scale(1.05); box-shadow:0 10px 40px rgba(123,47,255,0.7); }

  /* PROGRESS */
  .progress-wrap { padding:16px 24px 0; display:none; }
  .progress-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
  .progress-label { font-size:13px; color:#8877aa; font-weight:700; }
  .progress-score { font-size:13px; color:#ffdd00; font-weight:900; }
  .progress-bar { background:#1a0f30; border-radius:20px; height:14px; overflow:hidden; }
  .progress-fill { background:linear-gradient(90deg,#7b2fff,#ff2fff); height:100%; border-radius:20px; transition:width 0.5s ease; }

  /* CHAPTER */
  .chapter { display:none; padding:20px 20px 0; animation:fadeIn 0.4s ease; }
  .chapter.active { display:block; }
  @keyframes fadeIn { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }

  .chapter-badge {
    display:inline-block; background:linear-gradient(135deg,#7b2fff,#ff2fff);
    color:white; font-size:11px; font-weight:900; padding:5px 16px;
    border-radius:20px; letter-spacing:1px; text-transform:uppercase; margin-bottom:14px;
  }
  .chapter h2 { font-size:26px; font-weight:900; margin-bottom:16px; line-height:1.3; }

  .chapter-img {
    width:100%; border-radius:16px; display:block; margin-bottom:20px;
    border:3px solid rgba(180,100,255,0.4); box-shadow:0 8px 30px rgba(0,0,0,0.5);
    background:#1a0f30; min-height:180px; object-fit:cover;
  }

  .story-text {
    background:rgba(255,255,255,0.05); border-left:4px solid #7b2fff;
    border-radius:0 12px 12px 0; padding:18px 22px;
    font-size:16px; line-height:1.85; color:#ddd; margin-bottom:24px;
  }
  .story-text strong { color:#ffdd00; }
  .story-text em { color:#ff88ff; font-style:normal; font-weight:700; }

  /* QUIZ */
  .quiz-box {
    background:rgba(123,47,255,0.12); border:2px solid rgba(123,47,255,0.4);
    border-radius:16px; padding:22px; margin-bottom:20px;
  }
  .quiz-meta { display:flex; gap:8px; flex-wrap:wrap; align-items:center; margin-bottom:12px; }
  .difficulty { display:inline-block; font-size:11px; font-weight:900; padding:3px 10px; border-radius:10px; text-transform:uppercase; letter-spacing:1px; }
  .diff-warmup { background:rgba(100,200,255,0.2); color:#66ddff; border:1px solid #66ddff; }
  .diff-easy   { background:rgba(0,220,100,0.2);   color:#00dc64; border:1px solid #00dc64; }
  .diff-medium { background:rgba(255,200,0,0.2);   color:#ffcc00; border:1px solid #ffcc00; }
  .diff-hard   { background:rgba(255,80,80,0.2);   color:#ff8888; border:1px solid #ff8888; }
  .diff-boss   { background:rgba(255,0,200,0.2);   color:#ff44ee; border:1px solid #ff44ee; }
  .acara-tag { display:inline-block; font-size:10px; font-weight:700; padding:3px 10px; border-radius:10px; background:rgba(255,255,255,0.08); color:#9988cc; border:1px solid rgba(255,255,255,0.12); text-transform:uppercase; letter-spacing:0.5px; }

  .yr-badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 900;
    padding: 3px 10px;
    border-radius: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .yr3 { background: rgba(0, 180, 80, 0.2); color: #00cc60; border: 1px solid #00cc60; }
  .yr4 { background: rgba(160, 50, 255, 0.2); color: #bb66ff; border: 1px solid #bb66ff; }

  .quiz-icon { font-size:26px; display:block; margin-bottom:6px; }
  .quiz-label { font-size:12px; font-weight:900; color:#aa77ff; text-transform:uppercase; letter-spacing:2px; margin-bottom:10px; }
  .question { font-size:18px; font-weight:900; color:#fff; margin-bottom:18px; line-height:1.45; }

  .question-img {
    display: block;
    max-width: 300px;
    width: 100%;
    margin: 14px auto 18px;
    border-radius: 8px;
    border: 2px solid rgba(123, 47, 255, 0.3);
  }

  .options { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
  .opt-btn {
    background:rgba(255,255,255,0.07); border:2px solid rgba(255,255,255,0.15);
    color:#fff; font-family:'Nunito',Arial,sans-serif; font-size:17px; font-weight:700;
    padding:14px 10px; border-radius:12px; cursor:pointer; transition:all 0.15s;
  }
  .opt-btn:hover:not(:disabled) { background:rgba(123,47,255,0.3); border-color:#7b2fff; transform:scale(1.03); }
  .opt-btn.correct { background:rgba(0,220,100,0.2)!important; border-color:#00dc64!important; color:#00ff88!important; }
  .opt-btn.wrong   { background:rgba(255,50,50,0.2)!important;  border-color:#ff3232!important; color:#ff8888!important; animation:shake 0.4s; }
  @keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-6px)} 75%{transform:translateX(6px)} }

  .feedback { margin-top:16px; padding:14px 18px; border-radius:10px; font-size:15px; font-weight:700; display:none; line-height:1.5; }
  .feedback.show { display:block; }
  .feedback.good { background:rgba(0,220,100,0.15); border:2px solid #00dc64; color:#00ff88; }
  .feedback.bad  { background:rgba(255,50,50,0.15);  border:2px solid #ff3232; color:#ff9999; }

  .next-btn {
    display:none; width:100%; margin-top:16px;
    background:linear-gradient(135deg,#7b2fff,#ff2fff); color:white;
    font-family:'Nunito',Arial,sans-serif; font-size:18px; font-weight:900;
    padding:16px; border-radius:50px; border:none; cursor:pointer;
    box-shadow:0 4px 20px rgba(123,47,255,0.4); transition:transform 0.15s;
  }
  .next-btn:hover { transform:scale(1.03); }
  .next-btn.show { display:block; }

  /* ANIMATION OVERLAY */
  #anim-overlay {
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: 1000;
    background: rgba(0,0,0,0.7);
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  #anim-overlay.show { display: flex; }
  #anim-overlay lottie-player { width: 300px; height: 300px; }

  /* CHAPTER TRANSITION */
  .chapter-transition {
    display: none;
    text-align: center;
    padding: 20px;
  }
  .chapter-transition lottie-player { width: 120px; height: 120px; margin: 0 auto; }

  /* WIN SCREEN */
  #win-screen { display:none; text-align:center; padding:48px 24px 24px; animation:fadeIn 0.5s ease; }
  .trophy { font-size:80px; display:block; margin-bottom:16px; animation:bounce 0.8s ease infinite alternate; }
  @keyframes bounce { from{transform:scale(1)} to{transform:scale(1.15)} }
  #win-screen h2 { font-size:38px; font-weight:900; color:#ffdd00; text-shadow:0 0 24px rgba(255,220,0,0.5); margin-bottom:8px; }
  .win-score { font-size:22px; font-weight:900; color:#ff88ff; margin-bottom:16px; }
  .win-stars { font-size:36px; margin-bottom:20px; }
  #win-screen > p { font-size:17px; color:#c0a0ff; line-height:1.75; margin-bottom:20px; }
  .win-summary { background:rgba(255,255,255,0.05); border-radius:14px; padding:18px 20px; margin-bottom:24px; text-align:left; }
  .win-summary h3 { font-size:14px; color:#ffdd00; font-weight:900; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px; }
  .win-summary ul { list-style:none; }
  .win-summary li { font-size:14px; color:#c0a0ff; padding:4px 0; }
  #win-lottie { width: 300px; height: 300px; margin: 0 auto 20px; }
  .replay-btn {
    display:inline-block; background:linear-gradient(135deg,#ffdd00,#ff8800);
    color:#1a0630; font-family:'Nunito',Arial,sans-serif; font-size:18px; font-weight:900;
    padding:16px 40px; border-radius:50px; border:none; cursor:pointer;
    box-shadow:0 4px 20px rgba(255,220,0,0.3); transition:transform 0.15s; margin-bottom:16px;
  }
  .replay-btn:hover { transform:scale(1.04); }

  /* PARENT GUIDE */
  #parent-guide {
    display:none; margin:32px 20px 0; border-top:2px dashed rgba(255,255,255,0.15);
    padding-top:28px; animation:fadeIn 0.5s ease;
  }
  .pg-header { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; flex-wrap:wrap; gap:12px; }
  .pg-title { font-size:22px; font-weight:900; color:#ffdd00; }
  .pg-subtitle { font-size:13px; color:#8877aa; margin-top:4px; }
  .print-btn {
    background:rgba(255,255,255,0.08); border:2px solid rgba(255,255,255,0.2);
    color:#ddd; font-family:'Nunito',Arial,sans-serif; font-size:14px; font-weight:700;
    padding:8px 18px; border-radius:20px; cursor:pointer; transition:all 0.15s;
  }
  .print-btn:hover { background:rgba(255,255,255,0.15); }
  .pg-section { background:rgba(255,255,255,0.04); border-radius:14px; padding:18px 20px; margin-bottom:16px; }
  .pg-section h4 { font-size:14px; font-weight:900; color:#aa77ff; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px; }
  .pg-section p, .pg-section li { font-size:14px; color:#c0a0ff; line-height:1.7; }
  .pg-section ul { padding-left:16px; }
  .pg-section li { margin-bottom:6px; }
  .pg-row { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px; }
  .pg-card { background:rgba(255,255,255,0.04); border-radius:12px; padding:14px 16px; }
  .pg-card h5 { font-size:12px; font-weight:900; color:#7b2fff; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; }
  .pg-card p { font-size:13px; color:#c0a0ff; line-height:1.6; }
  .acara-table { width:100%; border-collapse:collapse; font-size:13px; }
  .acara-table th { text-align:left; color:#aa77ff; font-size:11px; text-transform:uppercase; letter-spacing:1px; padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.1); }
  .acara-table td { padding:7px 8px; color:#c0a0ff; border-bottom:1px solid rgba(255,255,255,0.05); vertical-align:top; }
  .acara-table tr:last-child td { border-bottom:none; }
  .strand-pill { display:inline-block; font-size:10px; font-weight:700; padding:2px 8px; border-radius:8px; background:rgba(123,47,255,0.25); color:#cc99ff; }

  @media print {
    body { background:white!important; color:#000!important; }
    .starfield, #title-screen, .progress-wrap, .chapter, #win-screen, #anim-overlay { display:none!important; }
    #parent-guide { display:block!important; margin:0; border-top:2px solid #ccc; }
    .print-btn { display:none; }
    .pg-section { border:1px solid #ddd; background:#f9f9f9; }
    .pg-section h4 { color:#333; }
    .pg-section p, .pg-section li, .pg-card p, .acara-table td { color:#333; }
    .pg-card h5 { color:#5500bb; }
    .acara-table th { color:#5500bb; }
    .strand-pill { background:#eee; color:#333; }
    .pg-title { color:#aa6600; }
  }
</style>
</head>
<body>

<div class="starfield" id="starfield"></div>

<!-- ANIMATION OVERLAY -->
<div id="anim-overlay">
  <lottie-player id="anim-player" src="" background="transparent" speed="1" autoplay></lottie-player>
</div>

<div class="wrapper">

  <!-- TITLE SCREEN -->
  <div id="title-screen" class="title-screen">
    <span class="rocket-emoji">🤖</span>
    <p class="issue-label">Issue #2</p>
    <h1>THE ROBOT<br><span>FACTORY</span></h1>
    <p class="tagline">Jake discovers an abandoned factory hidden in Saturn's rings!</p>
    <p class="meta">5 chapters · 10 challenges · ACARA-aligned · Year 3–4 content</p>
    <button class="start-btn" onclick="startGame()">🚀 START MISSION</button>
    <p style="font-size:12px;color:#443366;margin-top:20px;">For kids aged 8–10 &nbsp;·&nbsp; Year 3–4 focus</p>
  </div>

  <!-- PROGRESS BAR -->
  <div class="progress-wrap" id="progress-wrap">
    <div class="progress-top">
      <div class="progress-label" id="progress-label">Chapter 1 of 5</div>
      <div class="progress-score" id="progress-score">⭐ 0 / 10</div>
    </div>
    <div class="progress-bar"><div class="progress-fill" id="progress-fill" style="width:0%"></div></div>
  </div>

  <!-- ================================================================ -->
  <!--  CHAPTER 1 — BLAST FROM THE PAST + ARRIVAL                       -->
  <!-- ================================================================ -->
  <div class="chapter" id="chapter-1">
    <div style="padding:20px 0 0">
      <div class="chapter-badge">🔁 Chapter 1 — Approaching Saturn</div>
      <h2>Jake and Bolt Head for the Rings!</h2>
    </div>
    <img class="chapter-img" src="https://mathblastau.github.io/math-blast/images/ch1-robot-factory.png" alt="Jake and Bolt approaching Saturn's rings" />
    <div class="story-text">
      After his wild adventure on Planet Zog, Jake was back in space — this time with his new robot co-pilot, <em>Bolt</em>! Bolt was round, silver, and had glowing blue eyes that spun when he was excited. Right now, they were VERY excited. Ahead of them, glittering like a jewel, hung the magnificent rings of <strong>Saturn</strong>.<br><br>
      <em>"JAKE! JAKE! MY SENSORS DETECT AN ALIEN STRUCTURE HIDDEN IN THE RINGS! POSSIBILITY OF ROBOT FACTORY: 97.3%!"</em><br><br>
      Jake grinned and leaned forward. But first — Bolt's memory banks needed a quick warm-up. He'd been in sleep mode since the last mission.
    </div>

    <!-- Q1 — Blast from the Past (fractions review from Issue #1, Y3) -->
    <div class="quiz-box">
      <div class="quiz-meta">
        <span class="difficulty diff-warmup">🔁 Blast from the Past</span>
        <span class="acara-tag">Number · Year 3</span>
      </div>
      <span class="quiz-icon">🤖</span>
      <div class="quiz-label"><span class="yr-badge yr3">Y3</span> Warm-Up — Fractions Review</div>
      <div class="question">Bolt's fuel tank uses <strong>1/4 of one fuel pod</strong> per jump.<br>Jake has <strong>8 fuel pods</strong> in the cargo bay.<br><br>How many quarters are in 8 fuel pods altogether?</div>
      <img src="https://mathblastau.github.io/math-blast/images/q1-issue002.png" alt="Question illustration" class="question-img" />
      <div class="options">
        <button class="opt-btn" onclick="answer(this,false,'q1')">16</button>
        <button class="opt-btn" onclick="answer(this,true,'q1')">32</button>
        <button class="opt-btn" onclick="answer(this,false,'q1')">24</button>
        <button class="opt-btn" onclick="answer(this,false,'q1')">8</button>
      </div>
      <div class="feedback" id="feedback-q1"></div>
      <button class="next-btn" id="next-q1" onclick="showQ('q2')">Deeper into the Rings ➜</button>
    </div>

    <!-- Q2 — Y3 multiplication array -->
    <div id="q2-block" style="display:none">
      <div class="story-text">
        Jake and Bolt swooped through the outer rings and found it — a massive alien building, dark and silent, floating between two giant ice boulders. They docked their rocket and stepped inside. The factory floor was enormous. And everywhere Jake looked, there were <strong>dormant robots</strong>.
      </div>
      <div class="quiz-box">
        <div class="quiz-meta">
          <span class="difficulty diff-easy">⭐ Easy</span>
          <span class="acara-tag">Number · Year 3</span>
        </div>
        <span class="quiz-icon">🤖</span>
        <div class="quiz-label"><span class="yr-badge yr3">Y3</span> Question 2 — Multiplication Array</div>
        <div class="question">In the first room, dormant robots stand in <strong>3 rows of 4</strong>.<br>How many robots are there in total?</div>
        <img src="https://mathblastau.github.io/math-blast/images/q2-issue002.png" alt="Question illustration" class="question-img" />
        <div class="options">
          <button class="opt-btn" onclick="answer(this,false,'q2')">7</button>
          <button class="opt-btn" onclick="answer(this,false,'q2')">10</button>
          <button class="opt-btn" onclick="answer(this,true,'q2')">12</button>
          <button class="opt-btn" onclick="answer(this,false,'q2')">16</button>
        </div>
        <div class="feedback" id="feedback-q2"></div>
        <button class="next-btn" id="next-q2" onclick="nextChapter(2)">Enter the Factory ➜</button>
      </div>
    </div>
  </div>

  <!-- ================================================================ -->
  <!--  CHAPTER 2 — ARRAYS & MULTIPLICATION                              -->
  <!-- ================================================================ -->
  <div class="chapter" id="chapter-2">
    <div style="padding:20px 0 0">
      <div class="chapter-badge">🏭 Chapter 2 — The Assembly Floor</div>
      <h2>Rows and Rows of Sleeping Robots!</h2>
    </div>
    <img class="chapter-img" src="https://mathblastau.github.io/math-blast/images/ch2-robot-factory.png" alt="Inside the robot factory with rows of dormant robots" />
    <div class="story-text">
      The assembly floor stretched as far as Jake could see. Robots stood frozen in perfect grids — rows and columns of them, covered in dust. Bolt's eyes whirred as he scanned the room.<br><br>
      <em>"THERE ARE MANY COMPONENT RACKS, JAKE. TO RESTART THE FACTORY, WE MUST COUNT ALL THE PARTS!"</em>
    </div>

    <!-- Q3 — Y3 multiplication array -->
    <div class="quiz-box">
      <div class="quiz-meta">
        <span class="difficulty diff-easy">⭐ Easy</span>
        <span class="acara-tag">Number · Year 3</span>
      </div>
      <span class="quiz-icon">🔌</span>
      <div class="quiz-label"><span class="yr-badge yr3">Y3</span> Question 3 — Multiplication Array</div>
      <div class="question">On the component rack, circuit boards are stored in <strong>5 rows of 6</strong>.<br>How many circuit boards are there altogether?</div>
      <img src="https://mathblastau.github.io/math-blast/images/q3-issue002.png" alt="Question illustration" class="question-img" />
      <div class="options">
        <button class="opt-btn" onclick="answer(this,false,'q3')">25</button>
        <button class="opt-btn" onclick="answer(this,true,'q3')">30</button>
        <button class="opt-btn" onclick="answer(this,false,'q3')">35</button>
        <button class="opt-btn" onclick="answer(this,false,'q3')">11</button>
      </div>
      <div class="feedback" id="feedback-q3"></div>
      <button class="next-btn" id="next-q3" onclick="showQ('q4')">Next Question ➜</button>
    </div>

    <!-- Q4 — Y3 multiplication array -->
    <div id="q4-block" style="display:none">
      <div class="story-text">
        Jake found another storage bay — this one packed with glowing blue power cells, arranged neatly in a grid on the wall. <em>"These power the whole factory!"</em> Bolt buzzed excitedly.
      </div>
      <div class="quiz-box">
        <div class="quiz-meta">
          <span class="difficulty diff-easy">⭐ Easy</span>
          <span class="acara-tag">Number · Year 3</span>
        </div>
        <span class="quiz-icon">🔋</span>
        <div class="quiz-label"><span class="yr-badge yr3">Y3</span> Question 4 — Multiplication Array</div>
        <div class="question">Power cells are arranged in <strong>4 rows of 7</strong> on the wall.<br>How many power cells are there in total?</div>
        <img src="https://mathblastau.github.io/math-blast/images/q4-issue002.png" alt="Question illustration" class="question-img" />
        <div class="options">
          <button class="opt-btn" onclick="answer(this,false,'q4')">21</button>
          <button class="opt-btn" onclick="answer(this,false,'q4')">24</button>
          <button class="opt-btn" onclick="answer(this,true,'q4')">28</button>
          <button class="opt-btn" onclick="answer(this,false,'q4')">32</button>
        </div>
        <div class="feedback" id="feedback-q4"></div>
        <button class="next-btn" id="next-q4" onclick="nextChapter(3)">Power Up! ➜</button>
      </div>
    </div>
  </div>

  <!-- ================================================================ -->
  <!--  CHAPTER 3 — WORD PROBLEMS (Y3)                                   -->
  <!-- ================================================================ -->
  <div class="chapter" id="chapter-3">
    <div style="padding:20px 0 0">
      <div class="chapter-badge">⚡ Chapter 3 — Power Up!</div>
      <h2>The Factory Begins to Wake Up!</h2>
    </div>
    <img class="chapter-img" src="https://mathblastau.github.io/math-blast/images/ch3-robot-factory.png" alt="Factory machinery powering up with sparks" />
    <div class="story-text">
      Jake and Bolt hauled the power cells to the main reactor. Jake grabbed a giant lever — the kind that could only exist in an alien factory — and PULLED with all his might.<br><br>
      <em>KRZZZZZT! BZZZT! CLANG!</em><br><br>
      The lights flickered. Gears creaked. Conveyor belts lurched to life. The factory was waking up! But to get everything running properly, Jake had to solve the logistics of the supply chain.
    </div>

    <!-- Q5 — Y3 word problem -->
    <div class="quiz-box">
      <div class="quiz-meta">
        <span class="difficulty diff-medium">⭐⭐ Medium</span>
        <span class="acara-tag">Number · Year 3</span>
      </div>
      <span class="quiz-icon">📦</span>
      <div class="quiz-label"><span class="yr-badge yr3">Y3</span> Question 5 — Multiplication Word Problem</div>
      <div class="question">Jake needs to load supply crates onto transport bots.<br>He has <strong>3 transport bots</strong>, and each bot carries <strong>8 crates</strong>.<br>How many crates can they carry altogether?</div>
      <img src="https://mathblastau.github.io/math-blast/images/q5-issue002.png" alt="Question illustration" class="question-img" />
      <div class="options">
        <button class="opt-btn" onclick="answer(this,false,'q5')">11</button>
        <button class="opt-btn" onclick="answer(this,false,'q5')">18</button>
        <button class="opt-btn" onclick="answer(this,true,'q5')">24</button>
        <button class="opt-btn" onclick="answer(this,false,'q5')">32</button>
      </div>
      <div class="feedback" id="feedback-q5"></div>
      <button class="next-btn" id="next-q5" onclick="showQ('q6')">Next Question ➜</button>
    </div>

    <!-- Q6 — Y3 word problem -->
    <div id="q6-block" style="display:none">
      <div class="story-text">
        Bolt accessed the factory blueprint. <em>"JAKE! THE FACTORY HAS 6 SEPARATE FLOORS. EACH FLOOR HAS 9 ROBOTIC ARMS FOR ASSEMBLY."</em> Jake whistled. That was a LOT of arms.
      </div>
      <div class="quiz-box">
        <div class="quiz-meta">
          <span class="difficulty diff-medium">⭐⭐ Medium</span>
          <span class="acara-tag">Number · Year 3</span>
        </div>
        <span class="quiz-icon">🦾</span>
        <div class="quiz-label"><span class="yr-badge yr3">Y3</span> Question 6 — Multiplication Word Problem</div>
        <div class="question">The factory has <strong>6 floors</strong>.<br>Each floor has <strong>9 robotic arms</strong>.<br>How many robotic arms are there in total?</div>
        <img src="https://mathblastau.github.io/math-blast/images/q6-issue002.png" alt="Question illustration" class="question-img" />
        <div class="options">
          <button class="opt-btn" onclick="answer(this,false,'q6')">45</button>
          <button class="opt-btn" onclick="answer(this,false,'q6')">48</button>
          <button class="opt-btn" onclick="answer(this,true,'q6')">54</button>
          <button class="opt-btn" onclick="answer(this,false,'q6')">63</button>
        </div>
        <div class="feedback" id="feedback-q6"></div>
        <button class="next-btn" id="next-q6" onclick="nextChapter(4)">Robots, Assemble! ➜</button>
      </div>
    </div>
  </div>

  <!-- ================================================================ -->
  <!--  CHAPTER 4 — MULTI-DIGIT MULTIPLICATION (Y4)                      -->
  <!-- ================================================================ -->
  <div class="chapter" id="chapter-4">
    <div style="padding:20px 0 0">
      <div class="chapter-badge">🤖 Chapter 4 — The Robot Army</div>
      <h2>Robots Waking Up — By the Dozen!</h2>
    </div>
    <img class="chapter-img" src="https://mathblastau.github.io/math-blast/images/ch4-robot-factory.png" alt="Army of little robots marching in formation" />
    <div class="story-text">
      With the machinery running, something incredible happened. One by one — then ten by ten — the robots started powering up. Eyes glowing green. Heads swivelling. Little feet marching in perfect formation.<br><br>
      Jake watched, mouth open. <em>"Bolt... there are HUNDREDS of them!"</em><br><br>
      <em>"AFFIRMATIVE! ACTIVATING IN BATCHES. JAKE — YOU MUST COUNT THEM OR THE FACTORY CONTROLLER WILL SHUT DOWN!"</em>
    </div>

    <!-- Q7 — Y4 multi-digit multiplication -->
    <div class="quiz-box">
      <div class="quiz-meta">
        <span class="difficulty diff-hard">⭐⭐⭐ Hard</span>
        <span class="acara-tag">Number · Year 4</span>
      </div>
      <span class="quiz-icon">⏱️</span>
      <div class="quiz-label"><span class="yr-badge yr4">Y4</span> Question 7 — Multi-Digit Multiplication</div>
      <div class="question">Robots activate at a rate of <strong>12 robots per minute</strong>.<br>How many robots are active after <strong>3 minutes</strong>?</div>
      <img src="https://mathblastau.github.io/math-blast/images/q7-issue002.png" alt="Question illustration" class="question-img" />
      <div class="options">
        <button class="opt-btn" onclick="answer(this,false,'q7')">24</button>
        <button class="opt-btn" onclick="answer(this,false,'q7')">30</button>
        <button class="opt-btn" onclick="answer(this,true,'q7')">36</button>
        <button class="opt-btn" onclick="answer(this,false,'q7')">42</button>
      </div>
      <div class="feedback" id="feedback-q7"></div>
      <button class="next-btn" id="next-q7" onclick="showQ('q8')">Next Question ➜</button>
    </div>

    <!-- Q8 — Y4 multi-digit multiplication -->
    <div id="q8-block" style="display:none">
      <div class="story-text">
        The assembly line was putting together brand new robots too! Each robot needed exactly 24 bolts to be fully assembled. Jake was overseeing two batches.
      </div>
      <div class="quiz-box">
        <div class="quiz-meta">
          <span class="difficulty diff-hard">⭐⭐⭐ Hard</span>
          <span class="acara-tag">Number · Year 4</span>
        </div>
        <span class="quiz-icon">🔩</span>
        <div class="quiz-label"><span class="yr-badge yr4">Y4</span> Question 8 — Multi-Digit Multiplication</div>
        <div class="question">Each new robot needs <strong>24 bolts</strong> to assemble.<br>Jake is building <strong>2 batches</strong> of robots — but wait!<br>Each "batch" means <strong>1 robot</strong>... no wait — <strong>each batch = a set of robots needing 24 bolts.</strong><br><br>Jake has 2 batches. Each batch uses 24 bolts. How many bolts total?</div>
        <img src="https://mathblastau.github.io/math-blast/images/q8-issue002.png" alt="Question illustration" class="question-img" />
        <div class="options">
          <button class="opt-btn" onclick="answer(this,false,'q8')">26</button>
          <button class="opt-btn" onclick="answer(this,true,'q8')">48</button>
          <button class="opt-btn" onclick="answer(this,false,'q8')">42</button>
          <button class="opt-btn" onclick="answer(this,false,'q8')">36</button>
        </div>
        <div class="feedback" id="feedback-q8"></div>
        <button class="next-btn" id="next-q8" onclick="nextChapter(5)">Final Chapter ➜</button>
      </div>
    </div>
  </div>

  <!-- ================================================================ -->
  <!--  CHAPTER 5 — AREA + BOSS ROUND                                    -->
  <!-- ================================================================ -->
  <div class="chapter" id="chapter-5">
    <div style="padding:20px 0 0">
      <div class="chapter-badge">🔥 Chapter 5 — Factory Online!</div>
      <h2>Bolt Gets an Upgrade — Boss Round!</h2>
    </div>
    <img class="chapter-img" src="https://mathblastau.github.io/math-blast/images/ch5-robot-factory.png" alt="Factory fully running, Bolt getting an upgrade" />
    <div class="story-text">
      The factory roared to life! Every floor hummed with energy, every arm swung into action, every robot marched with purpose. Jake and Bolt stood in the control room at the very top.<br><br>
      <em>"JAKE! FACTORY IS AT 98% CAPACITY! THERE IS... ONE MORE UPGRADE SEQUENCE... FOR ME!"</em><br><br>
      Bolt's chest panel began to glow. A beautiful golden light pulsed outward. But to unlock the final upgrade, Jake had to solve two last maths challenges — the hardest yet.
    </div>

    <!-- Q9 — Y4 area as multiplication -->
    <div class="quiz-box">
      <div class="quiz-meta">
        <span class="difficulty diff-hard">⭐⭐⭐ Hard</span>
        <span class="acara-tag">Measurement · Year 4</span>
      </div>
      <span class="quiz-icon">📐</span>
      <div class="quiz-label"><span class="yr-badge yr4">Y4</span> Question 9 — Area as Multiplication</div>
      <div class="question">The main factory floor is rectangular.<br>It is <strong>8 tiles long</strong> and <strong>7 tiles wide</strong>.<br><br>What is the <strong>area</strong> of the factory floor in square tiles?</div>
      <img src="https://mathblastau.github.io/math-blast/images/q9-issue002.png" alt="Question illustration" class="question-img" />
      <div class="options">
        <button class="opt-btn" onclick="answer(this,false,'q9')">30</button>
        <button class="opt-btn" onclick="answer(this,false,'q9')">49</button>
        <button class="opt-btn" onclick="answer(this,true,'q9')">56</button>
        <button class="opt-btn" onclick="answer(this,false,'q9')">64</button>
      </div>
      <div class="feedback" id="feedback-q9"></div>
      <button class="next-btn" id="next-q9" onclick="showQ('q10')">Final Challenge ➜</button>
    </div>

    <!-- Q10 — Boss: multi-step multiplication + addition -->
    <div id="q10-block" style="display:none">
      <div class="story-text">
        <em>"FINAL UNLOCK SEQUENCE!"</em> Bolt announced. Two floors of robots needed to activate simultaneously. Jake had to calculate the TOTAL number to enter the exact code into the factory controller.
      </div>
      <div class="quiz-box">
        <div class="quiz-meta">
          <span class="difficulty diff-boss">👑 Boss Challenge</span>
          <span class="acara-tag">Number · Year 4</span>
        </div>
        <span class="quiz-icon">👑</span>
        <div class="quiz-label"><span class="yr-badge yr4">Y4</span> Question 10 — BOSS: Multi-Step</div>
        <div class="question">On <strong>Floor 1</strong>: <strong>3 rows of 5 robots</strong> activate.<br>On <strong>Floor 2</strong>: <strong>4 rows of 4 robots</strong> activate.<br><br>How many robots are activated in <strong>total</strong> across both floors?</div>
        <img src="https://mathblastau.github.io/math-blast/images/q10-issue002.png" alt="Question illustration" class="question-img" />
        <div class="options">
          <button class="opt-btn" onclick="answer(this,false,'q10')">28</button>
          <button class="opt-btn" onclick="answer(this,false,'q10')">35</button>
          <button class="opt-btn" onclick="answer(this,true,'q10')">31</button>
          <button class="opt-btn" onclick="answer(this,false,'q10')">40</button>
        </div>
        <div class="feedback" id="feedback-q10"></div>
        <button class="next-btn" id="next-q10" onclick="showWin()">🤖 FACTORY ONLINE!</button>
      </div>
    </div>
  </div>

  <!-- WIN SCREEN -->
  <div id="win-screen">
    <lottie-player id="win-lottie" src="https://assets9.lottiefiles.com/packages/lf20_obhph3t0.json" background="transparent" speed="1" loop autoplay style="width:300px;height:300px;margin:0 auto;display:block;"></lottie-player>
    <span class="trophy">🤖</span>
    <h2>FACTORY ONLINE!</h2>
    <div class="win-score" id="win-score">You scored 10 / 10!</div>
    <div class="win-stars" id="win-stars">⭐⭐⭐</div>
    <p>Bolt got his upgrade and the factory roared to life — thanks to <strong>YOU</strong>! 🏭🚀</p>
    <div class="win-summary">
      <h3>What You Mastered Today 🧠</h3>
      <ul>
        <li>✅ <strong>Fractions Review</strong> — quarters of 8 (Number, Y3)</li>
        <li>✅ <strong>Multiplication Arrays</strong> — 3×4, 5×6, 4×7 (Number, Y3)</li>
        <li>✅ <strong>Word Problems</strong> — 3×8, 6×9 (Number, Y3)</li>
        <li>✅ <strong>Multi-Digit Multiplication</strong> — 12×3, 24×2 (Number, Y4)</li>
        <li>✅ <strong>Area</strong> — 8×7 square tiles (Measurement, Y4)</li>
        <li>✅ <strong>Boss</strong> — (3×5) + (4×4) multi-step</li>
      </ul>
    </div>
    <p style="font-size:14px;color:#6655aa;margin-bottom:8px;">Issue #3 coming next week — Jake and Bolt follow the distress beacon into a <strong>black hole!</strong> 🌌</p>
    <button class="replay-btn" onclick="replayGame()">🔄 Play Again</button>
    <br>
    <button class="print-btn" onclick="showParentGuide()">📋 Parent Guide</button>
  </div>

  <!-- PARENT GUIDE -->
  <div id="parent-guide">
    <div class="pg-header">
      <div>
        <div class="pg-title">📋 Parent Guide — Issue #2</div>
        <div class="pg-subtitle">Mission: Math Blast · The Robot Factory · For parents of kids aged 8–10</div>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print This</button>
    </div>

    <div class="pg-section">
      <h4>What We Covered This Issue</h4>
      <table class="acara-table">
        <tr><th>Topic</th><th>ACARA Strand</th><th>Year Level</th><th>Question</th></tr>
        <tr><td>Fractions review — quarters of a whole number</td><td><span class="strand-pill">Number</span></td><td>Year 3</td><td>Q1 (Warm-Up)</td></tr>
        <tr><td>Multiplication — arrays (3×4)</td><td><span class="strand-pill">Number</span></td><td>Year 3</td><td>Q2</td></tr>
        <tr><td>Multiplication — arrays (5×6)</td><td><span class="strand-pill">Number</span></td><td>Year 3</td><td>Q3</td></tr>
        <tr><td>Multiplication — arrays (4×7)</td><td><span class="strand-pill">Number</span></td><td>Year 3</td><td>Q4</td></tr>
        <tr><td>Multiplication word problem (3×8)</td><td><span class="strand-pill">Number</span></td><td>Year 3</td><td>Q5</td></tr>
        <tr><td>Multiplication word problem (6×9)</td><td><span class="strand-pill">Number</span></td><td>Year 3</td><td>Q6</td></tr>
        <tr><td>Multi-digit multiplication (12×3)</td><td><span class="strand-pill">Number</span></td><td>Year 4</td><td>Q7</td></tr>
        <tr><td>Multi-digit multiplication (24×2)</td><td><span class="strand-pill">Number</span></td><td>Year 4</td><td>Q8</td></tr>
        <tr><td>Area as multiplication (8×7)</td><td><span class="strand-pill">Measurement</span></td><td>Year 4</td><td>Q9 ✨ New</td></tr>
        <tr><td>Multi-step: (3×5)+(4×4)</td><td><span class="strand-pill">Number</span></td><td>Year 4</td><td>Q10 👑 Boss</td></tr>
      </table>
    </div>

    <div class="pg-row">
      <div class="pg-card">
        <h5>✨ New This Issue</h5>
        <p><strong>Area as Multiplication</strong> — understanding that the area of a rectangle = length × width. A Year 4 Measurement skill. Use floor tiles, graph paper, or a room at home to make it concrete!</p>
      </div>
      <div class="pg-card">
        <h5>🔁 Spaced Review</h5>
        <p>Q1 revisited <strong>fractions</strong> from Issue #1. This spaced repetition approach helps lock in learning. Ask: "Do you remember how fractions worked from last week?"</p>
      </div>
    </div>

    <div class="pg-section">
      <h4>💬 Conversation Starters</h4>
      <ul>
        <li><strong>After Q2–Q4 (arrays):</strong> "Can you draw a 4×6 array? What about 6×4 — is it the same?" (Commutative property)</li>
        <li><strong>After Q7–Q8 (multi-digit):</strong> "How did you work out 12×3? Did you use a trick?" (Breaking into 10×3 + 2×3 = 36)</li>
        <li><strong>After Q9 (area):</strong> "What's the area of this table in hand-spans?" — actually measure it!</li>
        <li><strong>After Q10 (boss):</strong> "How many steps did this question have? Write them out — can you do it without a calculator?"</li>
      </ul>
    </div>

    <div class="pg-section">
      <h4>⚠️ Common Mistakes to Watch For</h4>
      <ul>
        <li><strong>Arrays (Q2–Q4):</strong> Kids sometimes add instead of multiply rows × columns. Reinforce: "rows times columns = total"</li>
        <li><strong>Multi-digit × 1-digit (Q7–Q8):</strong> Carrying errors are common. Encourage working it out step by step on paper.</li>
        <li><strong>Area (Q9):</strong> Confusing area with perimeter (adding sides vs multiplying). Tip: "Area fills the inside — we multiply."</li>
        <li><strong>Multi-step (Q10):</strong> Not writing down sub-answers. Encourage writing: "Floor 1 = ___. Floor 2 = ___. Total = ___."</li>
      </ul>
    </div>

    <div class="pg-section">
      <h4>📚 How This Aligns with School</h4>
      <p>This issue covers <strong>ACARA Australian Curriculum v9.0</strong>. Q1–Q6 are primarily <strong>Year 3 Number</strong> strand content. Q7–Q10 extend into <strong>Year 4 Number and Measurement</strong>. Year 3 students should aim for Q1–Q6 confidently; Year 4 students should tackle the full issue.</p>
    </div>

    <div class="pg-section">
      <h4>⏭️ Coming Up in Issue #3</h4>
      <p>Jake and Bolt follow a distress beacon into the depths of a black hole! New concept: <strong>division with remainders and larger numbers</strong> (Year 4). Arrays from this issue will return as a spaced review.</p>
    </div>

    <p style="font-size:12px;color:#443366;text-align:center;margin-top:20px;">Mission: Math Blast · Aligned to ACARA Australian Curriculum v9.0 · mathblast.com.au</p>
  </div>

</div><!-- /wrapper -->

<script>
  // Starfield
  const sf = document.getElementById('starfield');
  for (let i = 0; i < 90; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    s.style.left = Math.random() * 100 + '%';
    s.style.top = Math.random() * 100 + '%';
    s.style.animationDelay = Math.random() * 3 + 's';
    s.style.animationDuration = (2 + Math.random() * 3) + 's';
    sf.appendChild(s);
  }

  let score = 0;
  let questionsAnswered = 0;
  const totalQuestions = 10;

  const correctMsg = {
    q1:  "🎉 Yes! 8 fuel pods × 4 quarters each = 32 quarters. Bolt's memory banks are warmed up!",
    q2:  "🎉 Right! 3 × 4 = 12. Jake counted all 12 dormant robots in the first room.",
    q3:  "🎉 Correct! 5 × 6 = 30 circuit boards. The component rack is fully inventoried!",
    q4:  "🎉 Nailed it! 4 × 7 = 28 power cells. Enough to restart the factory!",
    q5:  "🎉 Spot on! 3 × 8 = 24 crates. The transport bots rumble forward!",
    q6:  "🎉 Yes! 6 × 9 = 54 robotic arms. That's a LOT of mechanical muscle!",
    q7:  "🎉 Correct! 12 × 3 = 36 robots. They're all blinking online!",
    q8:  "🎉 Right! 24 × 2 = 48 bolts. The assembly line is fully stocked!",
    q9:  "🎉 Perfect! 8 × 7 = 56 square tiles. Area = length × width!",
    q10: "🎉 BOSS CLEARED! Floor 1: 3×5=15. Floor 2: 4×4=16. Total: 15+16=31. FACTORY ONLINE! Bolt glows gold! 🤖✨"
  };

  const wrongMsg = {
    q1:  "❌ Think: each pod has 4 quarters. If there are 8 pods, how many quarters altogether? Multiply!",
    q2:  "❌ Count the rows times the columns: 3 rows × 4 robots per row = ?",
    q3:  "❌ Multiply rows × columns: 5 rows × 6 boards each = ?",
    q4:  "❌ 4 rows × 7 cells per row: try counting in 7s four times: 7, 14, 21, 28.",
    q5:  "❌ 3 bots × 8 crates each. Think: 3 groups of 8.",
    q6:  "❌ 6 floors × 9 arms: try 6 × 9. Count in 9s: 9, 18, 27, 36, 45, 54.",
    q7:  "❌ 12 robots per minute × 3 minutes. Break it: 10×3=30, 2×3=6, total=36.",
    q8:  "❌ 24 bolts × 2 batches. Double 24: 24+24=?",
    q9:  "❌ Area = length × width = 8 × 7. Count in 8s: 8, 16, 24, 32, 40, 48, 56.",
    q10: "❌ Two steps! Step 1: Floor 1 = 3×5 = 15. Step 2: Floor 2 = 4×4 = 16. Then add both together!"
  };

  function startGame() {
    document.getElementById('title-screen').style.display = 'none';
    document.getElementById('progress-wrap').style.display = 'block';
    showChapter(1);
  }

  function showChapter(n) {
    // Show chapter transition rocket animation for chapters 2-5
    if (n > 1) {
      showRocketTransition(function() {
        _doShowChapter(n);
      });
    } else {
      _doShowChapter(n);
    }
  }

  function _doShowChapter(n) {
    document.querySelectorAll('.chapter').forEach(c => c.classList.remove('active'));
    const ch = document.getElementById('chapter-' + n);
    if (ch) {
      ch.classList.add('active');
      updateProgress(n);
      window.scrollTo({top:0,behavior:'smooth'});
    }
  }

  function showRocketTransition(callback) {
    const overlay = document.getElementById('anim-overlay');
    const player = document.getElementById('anim-player');
    player.src = 'https://assets9.lottiefiles.com/packages/lf20_jR229r.json';
    overlay.classList.add('show');
    setTimeout(function() {
      overlay.classList.remove('show');
      if (callback) callback();
    }, 1500);
  }

  function showCorrectAnim(callback) {
    const overlay = document.getElementById('anim-overlay');
    const player = document.getElementById('anim-player');
    player.src = 'https://assets9.lottiefiles.com/packages/lf20_touohxv0.json';
    overlay.classList.add('show');
    setTimeout(function() {
      overlay.classList.remove('show');
      if (callback) callback();
    }, 2000);
  }

  function updateProgress(n) {
    const labels = ['',
      'Chapter 1 of 5 — Arrival at Saturn',
      'Chapter 2 of 5 — The Assembly Floor',
      'Chapter 3 of 5 — Power Up! ⚡',
      'Chapter 4 of 5 — Robot Army 🤖',
      'Chapter 5 of 5 — Boss Round 🔥'
    ];
    document.getElementById('progress-label').textContent = labels[n] || 'Chapter ' + n;
    document.getElementById('progress-fill').style.width = ((questionsAnswered/totalQuestions)*100) + '%';
    document.getElementById('progress-score').textContent = '⭐ ' + score + ' / ' + totalQuestions;
  }

  function showQ(qId) {
    const block = document.getElementById(qId + '-block');
    if (block) { block.style.display = 'block'; block.scrollIntoView({behavior:'smooth',block:'start'}); }
  }

  function answer(btn, correct, qId) {
    const quizBox = btn.closest('.quiz-box');
    quizBox.querySelectorAll('.opt-btn').forEach(b => b.disabled = true);
    const feedback = document.getElementById('feedback-' + qId);
    const nextBtn  = document.getElementById('next-' + qId);
    if (correct) {
      btn.classList.add('correct');
      score++; questionsAnswered++;
      feedback.className = 'feedback show good';
      feedback.innerHTML = correctMsg[qId];
      updateProgress(currentChapter());
      // Show celebration animation, then show next button
      showCorrectAnim(function() {
        nextBtn.classList.add('show');
      });
    } else {
      btn.classList.add('wrong');
      // Show wrong animation briefly
      const overlay = document.getElementById('anim-overlay');
      const player = document.getElementById('anim-player');
      player.src = 'https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json';
      overlay.classList.add('show');
      setTimeout(function() { overlay.classList.remove('show'); }, 1000);
      
      feedback.className = 'feedback show bad';
      feedback.innerHTML = wrongMsg[qId];
      setTimeout(() => {
        quizBox.querySelectorAll('.opt-btn').forEach(b => {
          if (!b.classList.contains('correct')) { b.disabled = false; b.classList.remove('wrong'); }
        });
        feedback.className = 'feedback';
      }, 2400);
    }
  }

  function currentChapter() {
    const active = document.querySelector('.chapter.active');
    return active ? parseInt(active.id.replace('chapter-','')) : 1;
  }

  function nextChapter(n) { showChapter(n); }

  function showWin() {
    document.querySelectorAll('.chapter').forEach(c => c.classList.remove('active'));
    document.getElementById('progress-wrap').style.display = 'none';
    const win = document.getElementById('win-screen');
    win.style.display = 'block';
    document.getElementById('win-score').textContent = 'You scored ' + score + ' / ' + totalQuestions + '!';
    document.getElementById('win-stars').textContent = score >= 9 ? '⭐⭐⭐' : score >= 6 ? '⭐⭐' : '⭐';
    window.scrollTo({top:0,behavior:'smooth'});
  }

  function showParentGuide() {
    document.getElementById('parent-guide').style.display = 'block';
    document.getElementById('parent-guide').scrollIntoView({behavior:'smooth'});
  }

  function replayGame() {
    score = 0; questionsAnswered = 0;
    document.getElementById('win-screen').style.display = 'none';
    document.getElementById('parent-guide').style.display = 'none';
    document.querySelectorAll('.opt-btn').forEach(b => { b.disabled=false; b.classList.remove('correct','wrong'); });
    document.querySelectorAll('.feedback').forEach(f => f.className = 'feedback');
    document.querySelectorAll('.next-btn').forEach(b => b.classList.remove('show'));
    ['q2','q4','q6','q8','q10'].forEach(id => {
      const block = document.getElementById(id + '-block');
      if (block) block.style.display = 'none';
    });
    document.getElementById('progress-wrap').style.display = 'none';
    document.getElementById('title-screen').style.display = 'block';
    window.scrollTo({top:0,behavior:'smooth'});
  }
</script>
</body>
</html>
'''

issue2_path = os.path.join(PROJECT_DIR, "issue-002-v1.html")
with open(issue2_path, "w") as f:
    f.write(ISSUE2_HTML)
log(f"  Saved: issue-002-v1.html ({os.path.getsize(issue2_path)//1024}KB)")

# Push issue-002-v1.html to GitHub
github_upload_text(ISSUE2_HTML, "issue-002-v1.html", "Issue #2: Robot Factory — animations, question images, Y3/Y4 badges")

# ======================================================================
# WRITE SUMMARY TO MEMORY
# ======================================================================

log("\nWriting summary to memory...")

summary = """
## Math Blast Build — 2026-03-25

### Task 1: Issue #1 Retrofit (v3)
- Generated 10 DALL-E 3 question images (q1-issue001.png through q10-issue001.png)
- Added Y3 (green) / Y4 (purple) curriculum badges to each question
- Inserted question images (max-width 300px, centered) below question text
- Saved as issue-001-v3.html (v2 kept intact)
- Pushed to GitHub: https://mathblastau.github.io/math-blast/issue-001-v3.html

### Task 2: Issue #2 Created
- Story: "The Robot Factory" — Saturn's rings, Jake + robot co-pilot Bolt
- 10 questions: fractions review (Y3), multiplication arrays (Y3), word problems (Y3), multi-digit mult (Y4), area (Y4), boss multi-step (Y4)
- Generated 5 chapter images (1792x1024) + 10 question images (1024x1024) = 15 images total
- Added Lottie animations: correct answer celebration, wrong answer feedback, chapter transition rocket, win screen
- Added Y3/Y4 badges to all questions
- Saved as issue-002-v1.html
- Pushed to GitHub: https://mathblastau.github.io/math-blast/issue-002-v1.html

### Live URLs (after GitHub Pages propagates ~1-5 min):
- https://mathblastau.github.io/math-blast/issue-001-v3.html
- https://mathblastau.github.io/math-blast/issue-002-v1.html
"""

memory_path = "/Users/leohiem/.openclaw/workspace/memory/2026-03-25.md"
os.makedirs(os.path.dirname(memory_path), exist_ok=True)
with open(memory_path, "a") as f:
    f.write(summary)
log("  Memory written.")

log("\n" + "=" * 60)
log("ALL TASKS COMPLETE!")
log("Issue #1 v3: https://mathblastau.github.io/math-blast/issue-001-v3.html")
log("Issue #2 v1: https://mathblastau.github.io/math-blast/issue-002-v1.html")
log("=" * 60)
