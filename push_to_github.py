#!/usr/bin/env python3
"""Push specified files to GitHub via Contents API."""

import base64
import json
import urllib.request
import urllib.error
import os
import time

REPO = "MathBlastAu/math-blast"
BASE_URL = f"https://api.github.com/repos/{REPO}/contents"
AUTH = "Basic TWF0aEJsYXN0QXU6TWF0aEJsYXN0MjAyNg=="
LOCAL_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast"

FILES = [
    "issue-001-v3.html",
    "issue-002-v1.html",
    "index.html",
    "sound-picker.html",
    "sounds/correct-2.wav",
    "sounds/wrong-3.wav",
    "sounds/next-4.wav",
    "sounds/transition-4.wav",
    "sounds/launch-1.wav",
    "sounds/win-1.wav",
    "sounds/win-2.wav",
    "sounds/win-3.wav",
    "sounds/win-4.wav",
    "images/blaze-concept.png",
]

def get_file_sha(path):
    """Get existing file SHA from GitHub, or None if not found."""
    url = f"{BASE_URL}/{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": AUTH,
        "Accept": "application/vnd.github+json",
        "User-Agent": "MathBlastPusher/1.0"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return data.get("sha")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise

def push_file(path, local_path):
    """Push a file to GitHub."""
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")
    
    sha = get_file_sha(path)
    
    payload = {
        "message": f"Update {path}",
        "content": content,
    }
    if sha:
        payload["sha"] = sha
    
    url = f"{BASE_URL}/{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PUT", headers={
        "Authorization": AUTH,
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "MathBlastPusher/1.0"
    })
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            action = "Updated" if sha else "Created"
            print(f"✅ {action}: {path}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"❌ FAILED: {path} — HTTP {e.code}: {body[:200]}")
        return False

results = {"success": [], "failed": []}

for i, file_path in enumerate(FILES):
    local = os.path.join(LOCAL_DIR, file_path)
    if not os.path.exists(local):
        print(f"⚠️  MISSING locally: {file_path}")
        results["failed"].append(file_path)
        continue
    
    ok = push_file(file_path, local)
    if ok:
        results["success"].append(file_path)
    else:
        results["failed"].append(file_path)
    
    # Small delay between files to avoid rate limits
    if i < len(FILES) - 1:
        time.sleep(0.5)

print("\n--- SUMMARY ---")
print(f"✅ Pushed ({len(results['success'])}): {', '.join(results['success'])}")
print(f"❌ Failed ({len(results['failed'])}): {', '.join(results['failed'])}")
