# Math Blast — Production Rules
*Non-negotiable standards. Lock these in. Never reinvent.*

---

## Images

### The Working Pattern (DO NOT CHANGE)
- Use `gen_jungle001_images.py` as the template for every new image gen script
- Define `BLAZE`, `SPROCKETS`, `SETTING` (and any new character constants) ONCE at the top
- Inject those constants into EVERY prompt — no exceptions
- Use `client = OpenAI()` with the `openai` Python library — not raw `requests`
- Use `model="gpt-image-1"`, `size="1536x1024"` for chapter images, `"1024x1024"` for question images
- Run the script locally — do NOT delegate image generation to a sub-agent with a loose brief
- The script skips existing files by default — set `force=True` only when explicitly redoing

### Locked Character Constants (Jungle Arc)
```
BLAZE = "10-year-old girl named Blaze: short practical dark hair, warm olive-tan skin,
teal/cyan fitted jumpsuit with purple accent panels on shoulders and sides,
bright yellow lightning bolt badge prominently on her left chest,
glowing cyan holographic device strapped to left wrist,
Disney Pixar CGI 3D animation style, vibrant saturated colours,
expressive eyes, clean polished render"

SPROCKETS = "tiny cobalt-blue alien creatures about knee-height,
smooth round heads with exactly three thin antennae,
large round expressive eyes, small stubby arms and legs,
some wearing tiny leaf tunics or aprons,
Disney Pixar CGI 3D animation style, same cobalt-blue skin in every image"

SETTING_FERNMOSS = "lower-canopy jungle village called Fernmoss: built among enormous glowing
blue-purple bioluminescent mushrooms, misty soft light, hanging moss, fireflies,
warm blue-green glow, Disney Pixar CGI 3D animation style, rich colour, cinematic quality"

SETTING_JUNGLE = "alien jungle canopy world: enormous ancient trees with platforms and rope bridges,
bioluminescent blue-green plants glowing softly, warm golden light filtering through giant
tropical leaves, fireflies drifting through the air,
Disney Pixar CGI 3D animation style, rich colour, cinematic quality"
```

---

## Audio

### The Working Pattern (DO NOT CHANGE)
1. **Write HTML story text first** — this is the master
2. **Extract audio scripts verbatim from screen text** — no paraphrasing, no additions
3. Max 1–2 sentences per clip per character
4. Run audio gen locally using `gen_jungle00X_audio_v2.py` pattern
5. **Commit audio files explicitly** — they don't auto-stage

### Narrator Coverage Check (mandatory before generating)
Before writing audio scripts, do this for every chapter:
1. List every paragraph in the `story-text` div
2. Assign each paragraph to a clip (narrator or character)
3. Any paragraph with no assigned clip = missing audio — fix it before generating
4. Each narrator paragraph = one Eric clip. Don't combine two narrator paragraphs if a character line falls between them.

### Question Accuracy Check (mandatory)
Before finalising each question, confirm all 4 of these match:
- Question text (the numbers/operation shown)
- Answer options (correct answer matches the question)
- Image prompt (shows the right numbers and setup)
- Audio script (reads the same question as screen text)

If any one of these four doesn't match the others — fix before generating.

### Audio Sequence (locked)
On correct answer: **celebration clip → explanation clip**
- Celebration: `feedback-correct-X.mp3` plays first
- Explanation: `ch5-q9-answer.mp3` etc plays second (chained via callback)

### unlockAtIndex (non-negotiable)
- Must be stored in `playerConfigs` — not just passed as parameter
- `setupPlayer` function must include: `unlockAtIndex: unlockAtIndex ?? files.length`
- Set to the index of the question clip so quiz unlocks when question STARTS playing

### Cliffhanger Pattern
- Q10 answer plays on correct answer (NOT in `showCliffhanger`)
- `showCliffhanger` auto-triggers the narration player only — no answer audio
- Cliffhanger always gets its own unique image — never reuse a chapter image

---

## HTML Structure

### Per-chapter player setup
```js
setupPlayer('ch1',
  ['ch1-intro.mp3','ch1-character.mp3','ch1-q1-question.mp3'],
  ['📖 Eric narrating...','⚡ Blaze speaking...','⚡ Blaze — puzzle time!'],
  'story-ch1','lock-q1',null,2);  // unlockAtIndex=2 (question clip index)
```

### Secondary Q blocks
- Q5, Q7, Q8, Q10 each need a setup clip before the question
- `showQ5Block()` etc: display block → scroll → `setTimeout(()=>togglePlayer('q5s'),400)`
- Do NOT play answer audio in showQ*Block — it fires on correct answer instead

---

## Process Order (every issue)

1. Read storyboard for the issue
2. Write all HTML story text (5 chapters)
3. Extract audio scripts verbatim from that text
4. Review both before generating anything
5. Write image gen script using locked constants from prior issue
6. Run image gen locally (not sub-agent)
7. Run audio gen locally
8. Build HTML with `unlockAtIndex` wired from the start
9. Commit everything (HTML + audio + images explicitly)
10. Run preflight script
11. Push → review → tag

---

## Characters (locked voices)

| Character | Arc | ElevenLabs ID | Settings |
|-----------|-----|---------------|----------|
| Eric (narrator) | Jungle | cjVigY5qzO86Huf0OWal | stability=0.60, similarity=0.75, style=0.20 |
| Blaze | Jungle | cgSgspJ2msm6clMCkdW9 | stability=0.55, similarity=0.75, style=0.30 |
| Chief Pip | Jungle | pqHfZKP75CvOlQylNhV4 | stability=0.65, similarity=0.70, style=0.25 |
| Doz | Jungle | IKne3meq5aSn9XLyUdCD | stability=0.45, similarity=0.70, style=0.50 |
| Thistle | Jungle | XrExE9yKIg1WjnnlVkGX | stability=0.60, similarity=0.75, style=0.25 |
| Tangle | Jungle | N2lVS1w4EtoT3dr4eOWO | stability=0.85, similarity=0.30, style=0.55 |
| George (narrator) | Space | JBFqnCBsd6RMkjVDRZzb | stability=0.55, similarity=0.75 |
| Andrew (Jake) | Space | BTEPH6wbWkb66Dys0ry6 | stability=0.50, similarity=0.78 |
| River (Phantom/aliens) | Space | SAz9YHcvj6GT2YYXdXww | stability=0.18, similarity=0.32, style=0.85 |

---

## Pre-Generation Script Review (mandatory)
Before running any audio gen script, read every line aloud mentally and check:
- **Em-dashes (—)** → replace with comma or "and" to avoid TTS pause
- **Colons mid-sentence** → replace with a full stop or comma
- **Parentheses** → remove or rewrite as natural speech
- **Abbreviations** → spell out (÷ → "divided by", × → "times")

## Story Text Paragraph Rule
Every paragraph in a `story-text` div must stand alone without the quiz question.
- If a paragraph only makes sense as a lead-in to the quiz → move it to the Q block setup clip instead
- Chapter story text = scene-setting and character moments only

## Image Prompt Rules
- **Never request mathematical symbols** in image prompts (÷, ×, /, =, fraction bars)
- Describe visually instead: "25 rows of 4 items" not "÷4"
- Holographic equation labels are fine (e.g. "holographic '60 ÷ 10 = ?' in cyan") — rendered as decoration, not as readable typography

## Lessons Learned (don't repeat)

- ❌ Don't delegate image gen to sub-agents — they write their own style descriptions and drift
- ❌ Don't use `/images/edits` for style consistency — it modifies the reference image, not the style
- ❌ Don't write audio scripts before the HTML text exists
- ❌ Don't truncate narrator clips to one sentence when the screen paragraph has two — cover the FULL paragraph
- ❌ Don't split a chapter's narrator text across multiple clips unless there's a character voice in between
- ❌ Don't forget to `git add sounds/` explicitly — audio files don't auto-stage
- ❌ Don't defer Q10 answer audio to `showCliffhanger` — it double-plays
- ❌ Don't put `unlockAtIndex` in `setupPlayer` call without storing it in `playerConfigs`
- ✅ Always check existing working scripts before building new ones
- ✅ Run image gen in background with enough timeout (600s+) for 16 images
- ✅ Commit and push audio + images together so GitHub Pages gets everything at once

---

*Created: 2026-03-29. Update this file whenever a new working pattern is established.*
