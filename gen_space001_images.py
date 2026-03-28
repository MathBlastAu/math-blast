#!/usr/bin/env python3
"""
Generate all 15 images for Space Issue 1 — "The Missing Quarter"
Setting: Kepler Station, a refuelling depot orbiting a red dwarf star
Characters: Jake Nova, Fuel Officer Priya, Fraction Phantom
"""
from openai import OpenAI
import base64, os, time

client = OpenAI()
DEST = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/images/")
os.makedirs(DEST, exist_ok=True)

JAKE = (
    "10-year-old boy named Jake: short messy brown hair, warm fair skin, "
    "bright orange space cadet jumpsuit with silver accent panels, "
    "a small rocket badge on his left chest, "
    "slightly scuffed boots, an expression that's always a mix of determination and mild chaos, "
    "Disney Pixar CGI 3D animation style, vibrant colours, expressive eyes"
)

PRIYA = (
    "adult woman named Priya: mid-40s, Indian-Australian appearance, dark hair tied back practically, "
    "authoritative navy-blue fuel officer uniform with gold rank insignia, "
    "no-nonsense expression, competent and direct, "
    "Disney Pixar CGI 3D animation style"
)

SETTING = (
    "futuristic space station refuelling depot called Kepler Station, "
    "orbiting a deep red dwarf star visible through large observation windows, "
    "industrial but sleek — large cylindrical fuel tanks with glowing fraction displays, "
    "holographic readout panels, docking clamps holding cargo ships, "
    "warm amber and blue lighting, Disney Pixar CGI 3D animation style"
)

def gen(filename, prompt, size="1024x1024", retries=2):
    path = DEST + filename
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        print(f"  ⏭  {filename} exists")
        return True
    print(f"  ⏳ {filename}...")
    for attempt in range(retries + 1):
        try:
            r = client.images.generate(model="gpt-image-1", prompt=prompt, size=size)
            data = base64.b64decode(r.data[0].b64_json)
            with open(path, 'wb') as f:
                f.write(data)
            print(f"  ✅ {filename} ({len(data):,} bytes)")
            time.sleep(12)
            return True
        except Exception as e:
            print(f"  ❌ attempt {attempt+1}: {e}")
            if attempt < retries: time.sleep(20)
    return False

print("\n── Chapter images (1536×1024) ──")

gen('ch1-kepler-docking.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{JAKE}, expression: focused and slightly nervous, stepping off a small shuttle into a busy docking bay. "
    f"He holds a fuel inspector badge and looks at a glowing holographic fuel gauge showing fraction readings. "
    f"{SETTING}. Three large cargo ships visible at docking clamps, their fuel indicators blinking orange. "
    f"Dramatic red dwarf star glow through the observation windows.",
    size="1536x1024")

gen('ch2-tank-bay.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{JAKE} and {PRIYA} stand in a vast tank bay. "
    f"{JAKE}, expression: concentrating hard, notebook out, pointing at a large cylindrical fuel tank with a glowing fraction display. "
    f"{PRIYA} stands beside him with arms crossed, watching intently. "
    f"{SETTING}. Three large tanks visible, each with different glowing fraction readout displays — no specific numbers shown. "
    f"Holographic fuel readout panels float in the air.",
    size="1536x1024")

gen('ch3-phantom-log.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{PRIYA} holds a glowing holographic printout, expression: grim and suspicious. "
    f"{JAKE} leans in to read it, expression: eyes wide with realisation. "
    f"The printout shows fuel transfer logs — glowing lines of data but no readable text. "
    f"{SETTING}. Slightly darker lighting, mysterious atmosphere. "
    f"A faint ghostly blue shimmer on a nearby screen hints at something strange.",
    size="1536x1024")

gen('ch4-fuel-allocation.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. "
    f"{JAKE}, expression: determined problem-solving face, arms spread wide gesturing between two different fuel tanks. "
    f"A holographic screen above him shows two tanks with fraction bars — no specific numbers. "
    f"Two cargo ships visible through the observation window. "
    f"{SETTING}. Urgent atmosphere, orange warning lights glowing on the waiting ships.",
    size="1536x1024")

gen('ch5-phantom-appears.png',
    f"Disney Pixar CGI 3D animation. Wide cinematic landscape. Night/dark atmosphere. "
    f"{JAKE} stands alone at a communications panel, expression: stunned and alert. "
    f"Before him, a holographic figure has appeared — translucent electric blue, "
    f"made entirely of glowing fraction bars and number lines that shift and float, "
    f"vaguely humanoid in shape, calm and precise in posture. "
    f"This is the Fraction Phantom. "
    f"{SETTING} at night. Deep shadows, the Phantom's blue glow illuminating Jake's face. "
    f"Dramatic, mysterious, slightly eerie.",
    size="1536x1024")

print("\n── Question images (1024×1024) ──")

gen('q1-issue001.png',
    f"Disney Pixar CGI 3D animation. "
    f"{JAKE}, expression: curious and focused, looking at a large holographic fuel gauge showing a tank divided into exactly 4 equal sections, with 1 section filled/glowing green and 3 sections empty/dark. "
    f"His wrist device points at it. No numbers or text visible anywhere in the image. "
    f"{SETTING}.")

gen('q2-issue001.png',
    f"Disney Pixar CGI 3D animation. "
    f"{JAKE}, expression: one finger raised in realisation, pointing at a large holographic fuel gauge showing a tank divided into exactly 2 equal sections with 1 section filled green. "
    f"A label 'Tank A' glows but no fraction numbers or text visible. "
    f"{SETTING}.")

gen('q3-issue001.png',
    f"Disney Pixar CGI 3D animation. "
    f"{JAKE}, expression: thoughtful comparison face, looking at a holographic fuel gauge showing a tank divided into 8 equal sections with 3 sections filled green. "
    f"His notebook is open showing a simple bar diagram. No numbers or text visible in the image. "
    f"Label 'Tank B' glows softly. {SETTING}.")

gen('q4-issue001.png',
    f"Disney Pixar CGI 3D animation. "
    f"{JAKE}, expression: pointing at two side-by-side holographic displays — "
    f"left display shows a tank with 4 sections all filled (before), "
    f"right display shows same tank with only 3 sections filled (after). "
    f"A faint glowing arrow between them suggests something was removed. "
    f"No numbers or text visible. Label 'Tank C' glows. {SETTING}.")

gen('q5-issue001.png',
    f"Disney Pixar CGI 3D animation. "
    f"{JAKE}, expression: eyebrows raised in an 'aha!' moment, looking at two side-by-side tank displays — "
    f"left: tank with 4 sections, 2 filled (half full, before), "
    f"right: same tank with only 1 section filled (quarter full, after). "
    f"Faint removal arrow between them. No numbers or text. Label 'Tank D'. {SETTING}.")

gen('q6-issue001.png',
    f"Disney Pixar CGI 3D animation. "
    f"{JAKE}, expression: combining two things together with hands, excited, "
    f"in front of a holographic display showing two separate tank bars — "
    f"one half-filled, one three-quarters filled — with a plus symbol and equals sign leading to a combined result bar. "
    f"A cargo ship labelled 'Orion' visible through the window. No numbers or fraction text visible. {SETTING}.")

gen('q7-issue001.png',
    f"Disney Pixar CGI 3D animation. "
    f"{JAKE}, expression: comparing carefully, holding up two fingers side by side, "
    f"looking at two holographic fraction bars side by side — one showing 3 out of 8 sections filled, one showing 4 out of 8 sections filled (but unlabelled). "
    f"A cargo ship 'Lyra' visible looking hopeful through the window. No fraction numbers or text. {SETTING}.")

gen('q8-issue001.png',
    f"Disney Pixar CGI 3D animation. "
    f"{JAKE}, expression: dividing/sharing gesture with hands, in front of a display showing 6 glowing fuel pods arranged in a row, "
    f"with a dotted line down the middle splitting them into 2 equal groups of 3. "
    f"Two small ships visible in the background. No numbers or text. {SETTING}.")

gen('q9-issue001.png',
    f"Disney Pixar CGI 3D animation. "
    f"{JAKE}, expression: counting carefully on his fingers, "
    f"beside a holographic display showing 3 separate fuel tank bars each with 1 out of 4 sections removed/highlighted red. "
    f"An equals sign leads to a combined bar showing the total removed. No fraction numbers or text visible. {SETTING}.")

gen('q10-issue001.png',
    f"Disney Pixar CGI 3D animation. "
    f"{JAKE}, expression: serious and focused, calculating, "
    f"beside a glowing timeline showing 3 nights with an equal fraction removed each night — "
    f"represented as 3 identical small tank bars each with the same section highlighted. "
    f"No numbers or text visible. Slightly ominous atmosphere, blue phantom shimmer in background. {SETTING}.")

print("\n─── COMPLETE ───")
