# Math Blast — Production Workflow

Last updated: 2026-03-29. Refined across Space Arc (7 issues) + Jungle Arc (7 issues).

---

## The Pipeline (per issue)

### Step 1 — Story & Coverage Map (before writing anything)
1. Read the arc storyboard for the issue
2. Read the previous issue's cliffhanger — open with a direct callback
3. Write the full HTML story text
4. **Map every paragraph to an audio clip** before writing a single script — this is non-negotiable
5. Run the question accuracy check (verify every answer manually)

### Step 2 — Production Rules (apply before generating)
- **TTS read-aloud scan:** read every audio script aloud mentally — catch em-dashes (`—`), colons mid-sentence, parentheses. Replace with natural speech equivalents (commas, short pauses)
- **Paragraph standalone rule:** every paragraph on screen must make sense without the quiz question. If it only works as a lead-in to a question, move it to the Q block setup text
- **No math symbols in image prompts:** describe visually ("25 rows of 4", not "÷4"). No answers, equations, or numbers in scene images — holographic label only
- **No answers in images:** include `"Do NOT show any numbers, equations, division symbols, or answers written anywhere in the scene itself."` in every question image prompt
- **Vine/creature colour rule (Jungle):** always specify `natural earthy brown vines, NOT rainbow, NOT neon` — AI defaults to rainbow without this

### Step 3 — Build (parallel)
Run audio generation and image generation **simultaneously**:
```bash
python3 gen_[arc][issue]_audio.py &
OPENAI_API_KEY="..." python3 gen_[arc][issue]_images.py &
```
While those run, write the **next issue's HTML**.

### Step 4 — Preflight
Before deploying, always run:
```bash
python3 preflight.py [issue-file].html
```
Must pass with **0 errors**. Warnings about sound directory path are false positives for jungle issues — ignore.

### Step 5 — Deploy
```bash
git add [issue].html images/[arc]/issue00X/ sounds/[arc]/issue00X/
git commit -m "[Arc] Issue X — [Title] (production complete)"
git push origin main
```

### Step 6 — Review
Art reviews at www.math-blast.com.au/[issue-file].html (~2 min propagation after push).

### Step 7 — Fix & Approve
- Fix issues, push fixes, wait for propagation
- When approved: `git tag [arc]-00X-approved && git push origin [arc]-00X-approved`

---

## Audio Script Rules

| Rule | Why |
|------|-----|
| Replace all em-dashes with commas | TTS stumbles on `—` |
| No colons mid-sentence | TTS over-pauses |
| Trailing comma on final sentence of a clip | Prevents audio bleed into next clip |
| Scripts verbatim from HTML screen text | Sync between audio and visual |
| Narrator covers every paragraph | No silent text on screen |

## Image Prompt Rules

| Rule | Why |
|------|-----|
| `Disney Pixar CGI 3D animation style` on every prompt | Consistency |
| Character constants defined at top of gen script | Consistent appearance |
| No math symbols, no answers in scene | AI can't render counts reliably |
| Holographic cyan label = only place for labels | Clean educational look |
| Chapter images: `size="1536x1024"` | Widescreen cinematic |
| Question images: `size="1024x1024"` | Square, focused |
| `retries=2` on every gen call | Handles API timeouts gracefully |
| 12s sleep between images | Stays within rate limits |

## unlockAtIndex Pattern

Quiz unlocks when question audio **starts** (not when full player finishes).
- Set `unlockAtIndex` = index of the question clip in the player files array
- e.g. player with 4 clips where clip[3] is the question: `unlockAtIndex=3`

## Feedback Audio Pattern

- Q1: always `feedback-correct-1.mp3` ("Pre-launch check passed" / "That's it. Round up to save the last Sprocket.")
- Q2–Q10: cycle through `feedback-correct-2` to `feedback-correct-6`
- Wrong: random choice between `feedback-wrong-1` and `feedback-wrong-2`
- Answer clip plays after celebrate clip: `playFile(celebFile, () => playFile(answerAudio[qId], null))`

---

## Arc Structure Template

Each arc = 7 issues:
- **Issues 1–2:** Introduce the world and core math concept (entry level)
- **Issues 3–4:** Deepen the concept (grouping, arrays, larger numbers)
- **Issues 5–6:** Complexity + emotional arc peak (remainders, reverse operations, antagonist reveal)
- **Issue 7:** Resolution + celebration (multi-step, proportional, arc wrap-up)

Each issue = 5 chapters, 10 questions:
- Ch1: 1 question (warm-up)
- Ch2: 2 questions (Q2 + Q3 block)
- Ch3: 2 questions (Q4 + Q5 block)
- Ch4: 3 questions (Q6 + Q7 block + Q8 block)
- Ch5: 2 questions (Q9 + Q10 block) → cliffhanger → win screen

---

## File Structure (per arc)

```
projects/math-blast/
  [arc]-00X-narrated.html
  sounds/[arc]/issue00X/
    ch1-intro.mp3
    ch1-[clip].mp3
    ch1-q1-question.mp3
    ch1-q1-answer.mp3
    ch2-intro.mp3
    ... (one clip per paragraph + one per question/answer)
    ch2-q3-setup.mp3       ← Q-block setup clips
    ch2-q3-question.mp3
    feedback-correct-1.mp3 through 6
    feedback-wrong-1.mp3, 2
    win.mp3
  images/[arc]/issue00X/
    ch1-[scene].png        ← 1536×1024
    ch2-[scene].png
    ... (5 chapter + 1 cliffhanger + 10 question images)
    cliffhanger-[scene].png
    q1-[description].png   ← 1024×1024
    ...
    q10-boss-[description].png
  gen_[arc]00X_audio.py
  gen_[arc]00X_images.py
```

---

## Naming Conventions

- Tags: `[arc]-00X-approved` (e.g. `jungle-007-approved`)
- Commits: `[Arc] Issue X — [Title] (production complete)`
- Fix commits: `[Arc] Issue X fixes: [list of what changed]`
- HTML: `[arc]-00X-narrated.html`
- Sounds: `sounds/jungle/issue00X/` or `sounds/issue00X/` (space arc)
- Images: `images/jungle/issue00X/` or `images/ch[X]-[desc].png` (space arc)

---

## Voice Cast

### Space Arc
| Character | Voice ID | Model | Notes |
|-----------|----------|-------|-------|
| George (narrator) | — | eleven_turbo_v2_5 | stability 0.60 |
| Andrew (Jake) | — | eleven_turbo_v2_5 | stability 0.55 |
| River (Priya/Phantom) | — | eleven_multilingual_v2 | stability 0.80, similarity 0.60, style 0.10 |

### Jungle Arc
| Character | Voice ID | Model | Notes |
|-----------|----------|-------|-------|
| Eric (narrator) | cjVigY5qzO86Huf0OWal | eleven_turbo_v2_5 | stability 0.60, sim 0.75, style 0.20 |
| Jessica (Blaze) | cgSgspJ2msm6clMCkdW9 | eleven_turbo_v2_5 | stability 0.55, sim 0.75, style 0.30 |
| Bill (Chief Pip/Keeper Moss/Elder Splash) | pqHfZKP75CvOlQylNhV4 | eleven_turbo_v2_5 | stability 0.70, sim 0.70, style 0.15 |
| Charlie (Doz) | IKne3meq5aSn9XLyUdCD | eleven_turbo_v2_5 | energetic young Australian |
| Callum (Tangle) | N2lVS1w4EtoT3dr4eOWO | eleven_multilingual_v2 | stability 0.85, sim 0.30, style 0.55 — use sparingly |

---

## Quality Metrics (target)

By following this workflow, target is **≤3 fixes per issue** after Art's review.
- Issue 4: 8 fixes (baseline)
- Issue 5: 8 fixes (audio bleed + image issues)
- Issue 6: 7 fixes
- Issue 7: 2 fixes ✅ (target achieved)
