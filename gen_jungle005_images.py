#!/usr/bin/env python3
"""Jungle Issue 5 images — Split Ridge. Natural earthy palette. Tangle consistent with Issue 3/4."""
from openai import OpenAI
import base64, os, time

client = OpenAI()
DEST = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/issue005/'
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
    "large round expressive eyes, small stubby arms and legs, some wearing tiny leaf tunics, "
    "Disney Pixar CGI 3D animation style, cobalt-blue skin"
)
CRAG = (
    "Elder Crag: a weathered older Sprocket, cobalt-blue skin, only two antennae instead of three, "
    "large round tired but wise eyes, wearing a battered leaf cloak, expression stoic and pragmatic, "
    "Disney Pixar CGI 3D animation style"
)
TANGLE = (
    "Tangle: an enormous mysterious creature made entirely of thick natural earthy vines and woody branches, "
    "natural brown and dark green tones throughout, the vines are twisted and organic looking, "
    "the creature is large and gentle-looking but shy, Disney Pixar CGI 3D animation style, "
    "no rainbow colours, no neon, natural jungle palette only"
)
SETTING = (
    "Split Ridge: a rugged cliff-face jungle village with rope bridges connecting stone platforms at different heights, "
    "jungle vines hanging down the cliff, warm afternoon light, rocky terrain, "
    "Disney Pixar CGI 3D animation style, rich colour, cinematic quality"
)
VINES = (
    "natural earthy brown vines with dark green accents, warm muted tones, "
    "organic and natural looking, NOT rainbow, NOT neon, natural jungle palette"
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

gen('ch1-split-ridge-arrival.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{BLAZE}, expression determined, arriving at {SETTING}. "
    f"In the distance on a lower platform: a group of tiny {SPROCKETS} stranded, looking up hopefully. "
    f"A wooden raft sits at the edge of the cliff. {CRAG} stands at the entrance with arms crossed. "
    f"Mood: urgent but manageable.", size="1536x1024")

gen('ch2-sharing-rocks.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"A platform in {SETTING}. Five groups of {SPROCKETS} each standing by their pile of building rocks. "
    f"Two rocks sit unclaimed in the centre, three Sprockets pointing at them arguing. "
    f"{BLAZE} crouches nearby with a patient expression, wrist device glowing. "
    f"Mood: lively, a little chaotic, warmly funny.", size="1536x1024")

gen('ch3-tangle-arrives.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{TANGLE} has arrived at {SETTING}, standing at the edge of the cliff platform. "
    f"It holds fifty {VINES} in its trailing tendrils. "
    f"On the ground in front of it: six neat groups of eight vines, plus two vines sitting alone to the side. "
    f"Tangle stares at the two leftover vines, posture communicating confusion and distress. "
    f"{BLAZE} crouches nearby, gentle expression. "
    f"Mood: tender, empathetic, a turning point.", size="1536x1024")

gen('ch4-bridge-building.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{SETTING}. {SPROCKETS} and {BLAZE} building four rope bridges across gaps in the cliff face. "
    f"Piles of wooden planks visible, some already laid out in groups of six. "
    f"Three planks sit separately to one side. "
    f"Mood: busy, productive, teamwork.", size="1536x1024")

gen('ch5-tangle-returns-vines.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. Golden late-afternoon light. "
    f"{TANGLE} stands on the platform of {SETTING}, carefully laying down {VINES} in perfect groups of twelve. "
    f"Rows and rows of vine bundles stretch along the clifftop. "
    f"{BLAZE} and {SPROCKETS} watch in silence, expressions moving from surprise to understanding. "
    f"Mood: quiet, moving, redemptive.", size="1536x1024")

print("\n── Question images (1024×1024) ──")

gen('q1-raft-13.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Thirteen {SPROCKETS} waiting on a rocky ledge. A small wooden raft can hold four. "
    f"First group of four is already on the raft. Holographic label '13 divided by 4' in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q2-rocks-22.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly twenty-two brown rocks arranged in five equal groups of four, with two rocks set apart. "
    f"Each group clearly separated. Holographic '22 divided by 5' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q3-firenuts-19.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly nineteen glowing fire-nuts arranged in six groups of three, with one nut set apart. "
    f"The single leftover nut sits near an older {CRAG}. Holographic '19 divided by 6' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q4-vines-50-groups8.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly fifty {VINES} arranged in six groups of eight on the ground, with two vines set apart and alone. "
    f"The two leftover vines are visually prominent. Holographic '50 divided by 8' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q5-vines-50-groups5.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly fifty {VINES} arranged in ten perfectly equal groups of five on the ground. No vines left over. "
    f"All groups identical and tidy. Holographic '50 divided by 5 equals 10' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q6-planks-27.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly twenty-seven wooden planks. Four groups of six planks neatly stacked, and three planks set to the side. "
    f"Holographic '27 divided by 6' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q7-sprockets-31.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly thirty-one {SPROCKETS} standing in four groups near four rope bridges. "
    f"Three bridges have seven Sprockets each. One bridge has four Sprockets. "
    f"Holographic '31 divided by 4' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q8-crossing-time.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"A rope bridge in {SETTING} with eight {SPROCKETS} crossing per minute. "
    f"Timeline showing minutes one through four, with groups of eight crossing in rows. "
    f"Last group is only seven Sprockets. Holographic '31 divided by 8' label in cyan. "
    f"Clean educational composition.")

gen('q9-starfruit-43.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. "
    f"Exactly forty-three glowing star-shaped fruits arranged in seven groups of six, with one fruit set apart. "
    f"Each group clearly distinct. Holographic '43 divided by 7' label in cyan. "
    f"{SETTING}. Clean educational composition.")

gen('q10-boss-100.png',
    f"Disney Pixar CGI 3D animation. Educational illustration. Boss challenge feel. "
    f"Exactly one hundred food supply boxes arranged in three groups: two groups of thirty-three, one group of thirty-four. "
    f"Three small Sprocket villages visible in the background. Dramatic golden light. "
    f"Holographic '100 divided by 3' label in cyan, glowing. "
    f"{SETTING}. Epic educational composition.")

gen('cliffhanger-tangle-watching.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. Warm golden twilight. "
    f"{TANGLE} sits at the edge of the cliff platform of {SETTING}, facing the village. "
    f"Along the clifftop: rows of {VINES} arranged in perfect groups of twelve, stretching as far as the eye can see. "
    f"{BLAZE} stands looking at them, small against the scale of the vine rows. "
    f"Mood: still, significant, something has changed.", size="1536x1024")

print("\n─── COMPLETE ───")
