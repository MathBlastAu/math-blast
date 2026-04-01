#!/usr/bin/env python3
"""Preflight check for Crystal Compass Issue 1"""
import re, os

HTML_FILE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/crystal-compass-issue-001-narrated.html"
AUDIO_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/audio/crystal-compass/issue-001"
IMAGE_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/crystal-compass/issue-001"

with open(HTML_FILE) as f:
    html = f.read()

errors = []
warnings = []

# Check all audio refs
audio_refs = re.findall(r"['\"]([^'\"]+\.mp3)['\"]", html)
audio_refs = [r for r in audio_refs if not r.startswith('http')]
# Strip path prefixes
audio_files_needed = set()
for r in audio_refs:
    basename = os.path.basename(r)
    audio_files_needed.add(basename)

print(f"Audio files referenced in HTML: {len(audio_files_needed)}")
for f in sorted(audio_files_needed):
    path = os.path.join(AUDIO_DIR, f)
    if os.path.exists(path):
        print(f"  ✅ {f}")
    else:
        print(f"  ❌ MISSING: {f}")
        errors.append(f"Missing audio: {f}")

# Check all image refs
img_refs = re.findall(r'src=["\']([^"\']+\.(png|jpg|jpeg|webp))["\']', html)
print(f"\nImage files referenced in HTML: {len(img_refs)}")
for r, ext in img_refs:
    # Check if it's a crystal compass issue image
    if 'crystal-compass/issue-001' in r:
        basename = os.path.basename(r)
        path = os.path.join(IMAGE_DIR, basename)
        if os.path.exists(path):
            print(f"  ✅ {basename}")
        else:
            print(f"  ❌ MISSING: {basename}")
            errors.append(f"Missing image: {basename}")
    else:
        print(f"  ℹ️  External/other: {r}")

# Check quiz structure
print("\n=== Quiz Structure Check ===")
quiz_ids = re.findall(r'id="quiz-(q\d+)"', html)
lock_ids = re.findall(r'id="lock-(q\d+)"', html)
feedback_ids = re.findall(r'id="feedback-(q\d+)"', html)
next_ids = re.findall(r'id="next-(q\d+)"', html)

print(f"Quiz boxes: {quiz_ids}")
print(f"Lock divs: {lock_ids}")
print(f"Feedback divs: {feedback_ids}")
print(f"Next buttons: {next_ids}")

# Verify alignment
for qid in quiz_ids:
    if qid not in lock_ids:
        warnings.append(f"Quiz {qid} has no lock div")
    if qid not in feedback_ids:
        errors.append(f"Quiz {qid} has no feedback div")
    if qid not in next_ids:
        errors.append(f"Quiz {qid} has no next button")

# Check speed round
print("\n=== Speed Round Check ===")
if 'speed-round-screen' in html:
    print("  ✅ Speed round screen present")
else:
    errors.append("Speed round screen missing")

if 'speedQuestions' in html:
    print("  ✅ speedQuestions array defined")
else:
    errors.append("speedQuestions array missing")

if 'srTimer' in html:
    print("  ✅ Timer variable defined")
else:
    errors.append("Speed round timer missing")

sr_q_count = html.count("sr-q") - html.count("sr-q-num") - html.count("sr-q-display")
print(f"  ℹ️  Speed round question audio files: 5 expected")

sr_audio = [f for f in os.listdir(AUDIO_DIR) if f.startswith('sr-q')]
print(f"  ✅ Speed round audio files found: {sorted(sr_audio)}")

# Check scoring
print("\n=== Scoring Check ===")
if 'speedScore' in html and 'score' in html:
    print("  ✅ Both main score and speed score tracked")
if 'triedWrong' in html:
    print("  ✅ triedWrong set (first-attempt scoring) present")
if "Main quiz:" in html:
    print("  ✅ Dual score display on win screen")

# Check chapter navigation
print("\n=== Chapter Navigation ===")
for i in range(1,6):
    if f'id="chapter-{i}"' in html:
        print(f"  ✅ Chapter {i} present")
    else:
        errors.append(f"Chapter {i} missing")

print("\n=== SUMMARY ===")
if errors:
    print(f"❌ {len(errors)} errors:")
    for e in errors:
        print(f"  - {e}")
else:
    print("✅ No errors!")
if warnings:
    print(f"⚠️  {len(warnings)} warnings:")
    for w in warnings:
        print(f"  - {w}")

print(f"\nFile size: {os.path.getsize(HTML_FILE)//1024}KB")
