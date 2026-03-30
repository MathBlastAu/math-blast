#!/usr/bin/env python3
"""
Math Blast Pre-Flight Check
Run before sending any issue for review.
Usage: python3 preflight.py issue-007-narrated.html
"""

import re, os, sys, json, hashlib, struct, wave

BASE = os.path.dirname(os.path.abspath(__file__))

def mp3_duration(path):
    """Estimate MP3 duration in seconds by scanning frame headers."""
    try:
        with open(path, 'rb') as f:
            data = f.read()
        # Skip ID3 tag if present
        offset = 0
        if data[:3] == b'ID3':
            id3_size = ((data[6] & 0x7f) << 21 | (data[7] & 0x7f) << 14 |
                        (data[8] & 0x7f) << 7  | (data[9] & 0x7f))
            offset = 10 + id3_size
        # Find first valid MP3 frame header
        sample_rates = {0: 44100, 1: 48000, 2: 32000}
        bitrates_v1_l3 = {1:32,2:40,3:48,4:56,5:64,6:80,7:96,8:112,9:128,10:160,11:192,12:224,13:256,14:320}
        total_frames = 0; total_duration = 0.0
        i = offset
        while i < len(data) - 4:
            if data[i] == 0xff and (data[i+1] & 0xe0) == 0xe0:
                b1 = data[i+1]; b2 = data[i+2]
                version = (b1 >> 3) & 0x3
                layer = (b1 >> 1) & 0x3
                bitrate_idx = (b2 >> 4) & 0xf
                sr_idx = (b2 >> 2) & 0x3
                padding = (b2 >> 1) & 0x1
                if version == 3 and layer == 1 and bitrate_idx in bitrates_v1_l3 and sr_idx in sample_rates:
                    br = bitrates_v1_l3[bitrate_idx] * 1000
                    sr = sample_rates[sr_idx]
                    frame_size = 144 * br // sr + padding
                    if frame_size > 0:
                        total_duration += 1152 / sr
                        total_frames += 1
                        i += frame_size
                        if total_frames > 200:  # enough sample
                            break
                        continue
            i += 1
        if total_frames > 0:
            # Extrapolate from sampled frames
            file_size = len(data) - offset
            avg_frame = (i - offset) / total_frames
            est_frames = file_size / avg_frame if avg_frame > 0 else total_frames
            return (est_frames / total_frames) * total_duration
        return None
    except Exception:
        return None

# ── Colours for terminal output ───────────────────────────────────────────────
RED   = "\033[91m"; GREEN = "\033[92m"; YELLOW = "\033[93m"
CYAN  = "\033[96m"; BOLD  = "\033[1m";  RESET  = "\033[0m"
OK    = f"{GREEN}✅{RESET}"; FAIL = f"{RED}❌{RESET}"; WARN = f"{YELLOW}⚠️ {RESET}"

errors = []; warnings = []; passes = []

def ok(msg):  passes.append(msg);   print(f"  {OK}  {msg}")
def err(msg): errors.append(msg);   print(f"  {FAIL}  {RED}{msg}{RESET}")
def warn(msg):warnings.append(msg); print(f"  {WARN}  {YELLOW}{msg}{RESET}")

def section(title):
    print(f"\n{BOLD}{CYAN}── {title} ──{RESET}")


def check(html_path):
    if not os.path.exists(html_path):
        print(f"{RED}File not found: {html_path}{RESET}"); sys.exit(1)

    with open(html_path) as f:
        html = f.read()

    # Derive issue number and sound dir
    m = re.search(r'issue-?0*(\d+)', os.path.basename(html_path))
    issue_num = m.group(1).zfill(3) if m else None
    # Try to find audio base from HTML const BASE declaration
    base_match = re.search(r"const BASE='([^']+)'", html)
    if base_match:
        sound_dir = os.path.join(BASE, base_match.group(1).rstrip('/'))
    elif issue_num:
        sound_dir = os.path.join(BASE, "sounds", f"issue{issue_num}")
    else:
        sound_dir = None
    img_dir   = os.path.join(BASE, "images")

    # ── 1. JS INFRASTRUCTURE ─────────────────────────────────────────────────
    section("JS Infrastructure")

    if "unlockAtIndex: unlockAtIndex ?? files.length" in html or \
       "unlockAtIndex:unlockAtIndex??files.length" in html or \
       "unlockAtIndex: unlockAtIndex??" in html:
        ok("playerConfigs includes unlockAtIndex")
    else:
        err("playerConfigs MISSING unlockAtIndex — quiz won't unlock while question plays")

    if "fileIdx===cfg.unlockAtIndex" in html or "fileIdx === cfg.unlockAtIndex" in html:
        ok("runPlayer has unlock-at-index injection")
    else:
        err("runPlayer MISSING unlock-at-index injection — quiz unlocks AFTER audio ends instead of when it starts")

    if "shuffleOptions" in html:
        if "shuffleOptions();" in html.split("function startGame")[1].split("}")[0]:
            ok("shuffleOptions() called in startGame()")
        else:
            err("shuffleOptions function exists but NOT called in startGame()")
    else:
        err("shuffleOptions() missing — correct answer will always appear in position 1")

    if "cliffhanger-screen" in html:
        ok("Cliffhanger screen present")
        if "showCliffhanger()" in html:
            ok("Q10 triggers showCliffhanger()")
        else:
            err("showCliffhanger() not wired to Q10 next button")
        cliff_img = re.search(r'cliffhanger-screen.*?<img src=\"([^\"]+)\"', html, re.DOTALL)
        if cliff_img:
            img_path = os.path.join(BASE, cliff_img.group(1))
            if os.path.exists(img_path):
                ok(f"Cliffhanger image exists: {cliff_img.group(1)}")
            else:
                err(f"Cliffhanger image MISSING: {cliff_img.group(1)}")
    else:
        err("Cliffhanger screen missing")

    if "win.mp3" in html:
        # Find everything between showWin(){ and the next top-level function
        win_fn = re.search(r"function showWin\(\)[^\n]*", html)
        if win_fn and "win.mp3" in win_fn.group(0):
            ok("win.mp3 plays in showWin() only")
        else:
            # Check multi-line version
            win_fn2 = re.search(r"function showWin\(\)(.*?)(?=\nfunction )", html, re.DOTALL)
            if win_fn2 and "win.mp3" in win_fn2.group(1):
                ok("win.mp3 plays in showWin() only")
            else:
                err("win.mp3 may be playing too early (not in showWin)")

    # ── 2. PLAYER SETUP ───────────────────────────────────────────────────────
    section("Player Setup")

    players = re.findall(
        r"setupPlayer\('(\w+)',\s*(\[[^\]]+\]),\s*(\[[^\]]+\]),\s*'([^']*)',\s*'([^']*)',\s*null,?\s*(\d+)?\s*\)\s*;",
        html
    )

    for pid, files_str, labels_str, story, lock, unlock_idx in players:
        files  = re.findall(r"'([^']+\.mp3)'", files_str)
        labels = re.findall(r"'([^']+)'", labels_str)
        n = len(files)
        idx = int(unlock_idx) if unlock_idx else None

        # unlockAtIndex present and correct (should be n-1 for question to show when it starts)
        if idx is None:
            err(f"Player '{pid}': unlockAtIndex MISSING")
        elif idx != n - 1:
            warn(f"Player '{pid}': unlockAtIndex={idx} but has {n} files (expected {n-1}). Check if intentional.")
        else:
            ok(f"Player '{pid}': {n} files, unlockAtIndex={idx} ✓")

        # Labels count matches files
        if len(labels) != n:
            err(f"Player '{pid}': {n} files but {len(labels)} labels")

        # Check audio files exist
        if sound_dir:
            for fname in files:
                fpath = os.path.join(sound_dir, fname)
                if not os.path.exists(fpath):
                    err(f"Player '{pid}': MISSING audio file: {fname}")

    # ── 3. STORY TEXT vs AUDIO SCRIPT ────────────────────────────────────────
    section("Story Text Alignment")

    # Extract audio texts from gen_arc_audio.py
    arc_path = os.path.join(BASE, "gen_arc_audio.py")
    audio_texts = {}
    if os.path.exists(arc_path) and issue_num:
        with open(arc_path) as f:
            arc = f.read()
        issue_key = f"issue{issue_num}"
        block = re.search(rf'"{issue_key}":\s*\[(.*?)(?=\n# ══|\Z)', arc, re.DOTALL)
        if block:
            for match in re.finditer(r'[GAJ]\("([^"]+\.mp3)",\s*"([^"]+)"\)', block.group(1)):
                audio_texts[match.group(1)] = match.group(2)
        # Map story panel IDs to their audio files
        panel_audio_map = {
            "story-ch1": ["ch1-intro.mp3"],
            "story-q2s": ["ch1-q2-story.mp3"],
            "story-ch2": ["ch2-intro.mp3"],
            "story-q4s": ["ch2-q4-story.mp3"],
            "story-ch3": ["ch3-intro.mp3"],
            "story-q6s": ["ch3-q6-story.mp3"],
            "story-ch4": ["ch4-intro.mp3"],
            "story-q8s": ["ch4-q8-story.mp3"],
            "story-ch5": ["ch5-intro.mp3"],
            "story-q10s": ["ch5-q10-story.mp3"],
        }
        panels = re.findall(r'id="(story-[^"]+)"[^>]*>(.*?)</div>', html, re.DOTALL)
        for pid, text in panels:
            clean_html = re.sub(r'<[^>]+>', '', text).strip()[:80]
            audio_file = panel_audio_map.get(pid, [None])[0]
            if audio_file and audio_file in audio_texts:
                audio_start = audio_texts[audio_file][:80]
                # Simple heuristic: first 30 chars should have some word overlap
                html_words  = set(re.findall(r'\b\w{4,}\b', clean_html.lower()))
                audio_words = set(re.findall(r'\b\w{4,}\b', audio_start.lower()))
                overlap = len(html_words & audio_words)
                if overlap >= 2:
                    ok(f"[{pid}] text aligns with {audio_file} ({overlap} words match)")
                else:
                    err(f"[{pid}] MISMATCH with {audio_file}:\n"
                        f"       HTML:  {clean_html[:70]}\n"
                        f"       AUDIO: {audio_start[:70]}")
            else:
                warn(f"[{pid}] no audio reference found to compare")

    # ── 4. ANSWER POSITIONS ──────────────────────────────────────────────────
    section("Answer Positions")

    all_first = True
    questions = re.findall(r'id="(quiz-q\d+)"(.*?)</div>\s*</div>', html, re.DOTALL)
    for qid, content in questions:
        opts = re.findall(r'onclick="answer\(this,(true|false),', content)
        if not opts:
            continue
        pos = opts.index('true') + 1 if 'true' in opts else None
        if pos == 1:
            all_first = False  # will be caught below
            warn(f"{qid}: correct answer is option 1 (will be randomised by shuffleOptions — OK if shuffle present)")
        else:
            ok(f"{qid}: correct answer is option {pos} (varied)")

    if all_first:
        if "shuffleOptions" in html:
            ok("All answers are option 1 — covered by shuffleOptions randomisation ✓")
        else:
            err("All answers are option 1 AND shuffleOptions is missing — kids will always see the answer first!")

    # ── 5. QUESTION-AUDIO ALIGNMENT ──────────────────────────────────────────
    section("Question–Audio Alignment")

    if os.path.exists(arc_path) and issue_num and block:
        q_audio = {}
        for match in re.finditer(r'[GAJ]\("(ch\d-q\d+-question\.mp3|ch\d-q\d+question\.mp3)",\s*"([^"]+)"\)', block.group(1)):
            q_audio[match.group(1)] = match.group(2)

        q_boxes = re.findall(r'id="quiz-(q\d+)"(.*?)</div>\s*</div>', html, re.DOTALL)
        for qid, content in q_boxes:
            qtext = re.search(r'class="question">(.*?)</div>', content, re.DOTALL)
            if not qtext: continue
            html_q = re.sub(r'<[^>]+>','',qtext.group(1)).strip()[:80]
            # Find matching audio file
            qnum = qid[1:]  # e.g. '1' from 'q1'
            for fname, atext in q_audio.items():
                if f"q{qnum}-question" in fname or f"q{qnum}question" in fname:
                    html_words  = set(re.findall(r'\b\w{4,}\b', html_q.lower()))
                    audio_words = set(re.findall(r'\b\w{4,}\b', atext[:80].lower()))
                    overlap = len(html_words & audio_words)
                    # Also normalise fractions: "3/4" → "quarters", "1/2" → "half" etc.
                    norm = lambda s: re.sub(r'1/4','quarter',re.sub(r'3/4','quarters',
                           re.sub(r'1/2','half',re.sub(r'1/3','third',
                           re.sub(r'2/3','thirds',re.sub(r'3/8','eighths',s))))))
                    html_words2  = set(re.findall(r'\b\w{4,}\b', norm(html_q).lower()))
                    audio_words2 = set(re.findall(r'\b\w{4,}\b', norm(atext[:80]).lower()))
                    overlap2 = len(html_words2 & audio_words2)
                    best = max(overlap, overlap2)
                    if best >= 2:
                        ok(f"{qid}: question text aligns with audio ({best} words)")
                    else:
                        err(f"{qid}: MISMATCH — HTML vs audio question:\n"
                            f"       HTML:  {html_q[:70]}\n"
                            f"       AUDIO: {atext[:70]}")
                    break

    # ── 6. IMAGES ─────────────────────────────────────────────────────────────
    section("Images")

    if issue_num:
        # Check all referenced images
        img_refs = re.findall(r'src="(images/[^"]+\.png)"', html)
        for ref in img_refs:
            fpath = os.path.join(BASE, ref)
            if os.path.exists(fpath):
                size = os.path.getsize(fpath)
                if size < 10_000:
                    err(f"Image suspiciously small ({size:,} bytes): {ref}")
                else:
                    ok(f"{ref} — {size:,} bytes")
            else:
                err(f"Image MISSING: {ref}")

    # ── 7. AUDIO FILES ────────────────────────────────────────────────────────
    section("Audio Files")

    if sound_dir and os.path.exists(sound_dir):
        # Get all mp3s referenced in players
        player_files = re.findall(r"'([^']+\.mp3)'", html)
        special = ['feedback-correct-1.mp3','feedback-correct-2.mp3','feedback-correct-3.mp3',
                   'feedback-correct-4.mp3','feedback-correct-5.mp3','feedback-correct-6.mp3',
                   'feedback-wrong-1.mp3','feedback-wrong-2.mp3','win.mp3']
        all_needed = set(player_files + special)
        # Also add cliff audio if present
        cliff_files = re.findall(r"playFile\('([^']+\.mp3)'", html)
        all_needed.update(cliff_files)

        missing = [f for f in all_needed if not os.path.exists(os.path.join(sound_dir, f))]
        present = [f for f in all_needed if os.path.exists(os.path.join(sound_dir, f))]

        ok(f"{len(present)} audio files present")
        for f in missing:
            err(f"MISSING audio: {f}")

        # ── Audio duration check for answer files ────────────────────────────
        # Answer confirmations: 2–6 seconds. Too short = garble/empty. Too long = verbose.
        answer_files = [f for f in all_needed if '-answer.mp3' in f]
        for af in sorted(answer_files):
            af_path = os.path.join(sound_dir, af)
            if not os.path.exists(af_path):
                continue
            duration = mp3_duration(af_path)
            if duration is None:
                warn(f"Could not read duration: {af}")
            elif duration < 1.5:
                err(f"Answer audio too short ({duration:.1f}s) — likely garble: {af}")
            elif duration > 7.0:
                warn(f"Answer audio too long ({duration:.1f}s) — may be verbose: {af}")
            else:
                ok(f"Answer audio duration OK ({duration:.1f}s): {af}")

        # Check feedback-correct-1 — flag if it's the pre-launch artifact from Issue 1
        fc1 = os.path.join(sound_dir, 'feedback-correct-1.mp3')
        i1_fc1 = os.path.join(BASE, 'sounds/issue001/feedback-correct-1.mp3')
        if os.path.exists(fc1) and os.path.exists(i1_fc1):
            if open(fc1,'rb').read() == open(i1_fc1,'rb').read():
                err("feedback-correct-1.mp3 is identical to Issue 1 'pre-launch check passed' — regenerate!")
            else:
                ok("feedback-correct-1.mp3 is issue-specific ✓")
    else:
        warn(f"Sound directory not found: {sound_dir}")

    # ── SUMMARY ───────────────────────────────────────────────────────────────
    print(f"\n{BOLD}{'═'*50}")
    print(f"  Pre-Flight Summary for {os.path.basename(html_path)}")
    print(f"{'═'*50}{RESET}")
    print(f"  {GREEN}{len(passes)} checks passed{RESET}")
    print(f"  {YELLOW}{len(warnings)} warnings{RESET}")
    print(f"  {RED}{len(errors)} errors{RESET}")

    if errors:
        print(f"\n{RED}{BOLD}  ❌ NOT READY FOR REVIEW — fix errors above first{RESET}")
        return False
    elif warnings:
        print(f"\n{YELLOW}{BOLD}  ⚠️  REVIEW WITH CAUTION — warnings present{RESET}")
        return True
    else:
        print(f"\n{GREEN}{BOLD}  ✅ ALL CLEAR — ready for review{RESET}")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{BOLD}Usage: python3 preflight.py <issue-file.html>{RESET}")
        print(f"Example: python3 preflight.py issue-007-narrated.html")
        sys.exit(1)

    html_path = sys.argv[1]
    if not os.path.isabs(html_path):
        html_path = os.path.join(BASE, html_path)

    ok_result = check(html_path)
    sys.exit(0 if ok_result else 1)
