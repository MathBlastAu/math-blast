#!/usr/bin/env python3
"""Jungle Issue 6 images — The Deep Root. Ancient, atmospheric, mathematical art."""
from openai import OpenAI
import base64, os, time

client = OpenAI()
DEST = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/issue006/'
os.makedirs(DEST, exist_ok=True)

BLAZE = (
    "10-year-old girl named Blaze: short practical dark hair, warm olive-tan skin, "
    "teal/cyan fitted jumpsuit with purple accent panels on shoulders and sides, "
    "bright yellow lightning bolt badge prominently on her left chest, "
    "glowing cyan holographic device strapped to left wrist, "
    "Disney Pixar CGI 3D animation style, vibrant saturated colours, expressive eyes, clean polished render"
)
SPROCKETS = (
    "tiny cobalt-blue alien creatures about knee-height, smooth round heads with exactly three thin antennae, "
    "large round expressive eyes, small stubby arms and legs, "
    "Disney Pixar CGI 3D animation style, cobalt-blue skin"
)
TANGLE = (
    "Tangle: an enormous mysterious creature made entirely of thick natural earthy vines and woody branches, "
    "natural brown and dark green tones throughout, vines twisted and organic, "
    "large and gentle-looking but shy, Disney Pixar CGI 3D animation style, "
    "no rainbow colours, no neon, natural jungle palette only"
)
SETTING = (
    "the Deep Root: the ancient heart of the Verdant Canopy jungle, enormous trees with massive above-ground roots "
    "forming walls and corridors, dappled ancient golden-green light, moss-covered ground, "
    "extraordinary vine sculptures everywhere in perfect arrays and patterns, "
    "Disney Pixar CGI 3D animation style, rich atmospheric colour, cinematic quality"
)
VINES = (
    "natural earthy brown vines with dark green accents, warm muted tones, organic and natural, "
    "NOT rainbow, NOT neon, natural jungle palette"
)

def gen(filename, prompt, size="1024x1024", retries=2):
    path = DEST + filename
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        print(f"  ⏭  {filename}"); return True
    print(f"  ⏳ {filename}...")
    for attempt in range(retries + 1):
        try:
            r = client.images.generate(model="gpt-image-1", prompt=prompt, size=size)
            data = base64.b64decode(r.data[0].b64_json)
            with open(path, 'wb') as f: f.write(data)
            print(f"  ✅ {filename} ({len(data):,} bytes)")
            time.sleep(12); return True
        except Exception as e:
            print(f"  ❌ attempt {attempt+1}: {e}")
            if attempt < retries: time.sleep(20)
    return False

print("\n── Chapter images (1536×1024) ──")

gen('ch1-deep-root-arrival.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE} entering {SETTING} for the first time, following {TANGLE} ahead of her. "
    f"All around: vine sculptures of extraordinary complexity in perfect rectangular arrays. "
    f"Expression: awe and wonder. "
    f"Mood: ancient, beautiful, mysterious.", size="1536x1024")

gen('ch2-finding-sprockets.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"Many {SPROCKETS} scattered throughout {SETTING}, exploring the vine sculptures with delight. "
    f"{BLAZE} stands in the foreground looking relieved. "
    f"The Sprockets are not trapped, they look happy but very lost. "
    f"Mood: relief, warmth, a little chaotic.", size="1536x1024")

gen('ch3-teaching-sharing.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE} sitting cross-legged on the ground of {SETTING}, facing {TANGLE}. "
    f"Between them on the ground: {VINES} divided into two equal groups of six. "
    f"Blaze gestures toward Tangle's group. Tangle is very still, watching intently. "
    f"Mood: quiet, important, a turning point.", size="1536x1024")

gen('ch4-vine-collections.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"A large cave at the edge of {SETTING}, filled with {TANGLE}'s stored collection of {VINES}. "
    f"Piles and organised stacks of exactly two hundred and fifty-two vines. "
    f"{BLAZE} stands at the entrance with her wrist device glowing, calculating. "
    f"Mood: discovery, analytical.", size="1536x1024")

gen('ch5-new-clearing.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. Golden afternoon light. "
    f"{TANGLE} stands in a large open clearing surrounded by {SETTING}, "
    f"beginning to lay the first row of {VINES} for a new sculpture on the clearing floor. "
    f"{BLAZE} watches nearby, smiling. "
    f"This clearing is far from any vine paths or village connections. "
    f"Mood: hopeful, a new beginning.", size="1536x1024")

print("\n── Question images (1024×1024) ──")

gen('q1-sculpture-144.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A large rectangular array of exactly one hundred and forty-four {VINES} on the jungle floor: twelve rows of twelve. "
    f"Each row clearly distinct. Holographic '144 divided by 12' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q2-sprockets-60.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly sixty {SPROCKETS} standing in five clearly separated equal groups of twelve. "
    f"Each group has a small numbered flag above it. Holographic '60 divided by 5' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q3-bridge-84.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A narrow vine bridge in {SETTING} with exactly seven {SPROCKETS} crossing at a time. "
    f"Queue of remaining Sprockets waiting on one side. Holographic '84 divided by 7' label in cyan. "
    f"Clean educational composition.")

gen('q4-vines-156.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly one hundred and fifty-six {VINES} arranged in thirteen neat bundles of twelve on the jungle floor. "
    f"Each bundle tied with a leaf. Holographic '156 divided by 12' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q5-bundles-needed.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Thirteen completed vine bundles on the left, labelled. "
    f"Fifteen small Sprocket villages illustrated on the right with two highlighted as missing their bundles. "
    f"Holographic '15 minus 13 equals 2 more bundles' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q6-division-252-6.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Two hundred and fifty-two {VINES} organised in groups of six, showing forty-two groups total. "
    f"Groups arranged in neat rows. Holographic '252 divided by 6 equals 42' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q7-division-252-7.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Two hundred and fifty-two {VINES} organised in groups of seven, showing thirty-six groups total. "
    f"Groups arranged in neat rows, visibly fewer than in the previous question. "
    f"Holographic '252 divided by 7 equals 36' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q8-comparison.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Two side-by-side displays: left shows forty-two groups of six {VINES}, right shows thirty-six groups of seven vines. "
    f"Left side visibly has more groups. Holographic comparison label: '252 divided by 6 vs 252 divided by 7' in cyan. "
    f"{SETTING}. Clean educational comparison composition.")

gen('q9-clearing-117.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A rectangular clearing with exactly one hundred and seventeen positions marked in thirteen rows of nine. "
    f"Each position shown as a small circle on the ground. Holographic '117 divided by 9' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q10-boss-288.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. Boss challenge feel. "
    f"Exactly two hundred and eighty-eight {VINES} in a magnificent rectangular array on the jungle floor: twenty-four rows of twelve. "
    f"Dramatic ancient golden light, impressive scale. "
    f"Holographic '288 divided by 12 equals 24 rows' label in cyan, glowing. "
    f"{SETTING}. Epic educational composition.")

gen('cliffhanger-number-line.png',
    f"Disney Pixar CGI 3D animation. Wide aerial cinematic view looking down through the jungle canopy. "
    f"Visible on the jungle floor below: an enormous vine sculpture covering hundreds of square metres, "
    f"made of {VINES}, arranged in a perfectly regular equally-spaced pattern that repeats in one direction "
    f"like an enormous number line. The scale is extraordinary. "
    f"{BLAZE} is tiny in the corner, looking down at it with awe. "
    f"Mood: revelation, wonder, ancient mathematical beauty.", size="1536x1024")

print("\n─── COMPLETE ───")
