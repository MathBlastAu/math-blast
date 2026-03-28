#!/usr/bin/env python3
"""Generate all chapter + question images for Issues 2-7."""

import os, base64, time
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
IMAGES_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"
REFERENCE  = f"{IMAGES_DIR}/ch1-crashed-rocket.png"

JAKE  = "Jake (10-year-old boy, short messy brown hair, bright green eyes, freckles, orange space suit with silver trim, blue visor helmet with red rocket patch)"
STYLE = "Pixar/Disney 3D animation style, vibrant saturated colours, cinematic lighting, space adventure theme, kid-friendly, high detail"
PHANTOM = "the Fraction Phantom (a towering holographic figure made entirely of glowing blue fraction bars and number lines, shifting and rearranging like living mathematics)"

IMAGES = [
    # ── ISSUE 2 — Fog Nebula ───────────────────────────────────
    ("ch1-issue002.png", "1536x1024", f"{JAKE} pilots his rocket deep inside a massive swirling purple-blue fog nebula, visibility near zero, instrument panels glowing with fraction readouts, eerie beautiful lighting, {STYLE}."),
    ("ch2-issue002.png", "1536x1024", f"{JAKE} in his cockpit making radio contact with the SS Meridian — a damaged freighter visible through the fog, distress lights flashing, both ships floating in the purple nebula, {STYLE}."),
    ("ch3-issue002.png", "1536x1024", f"{JAKE} and the Meridian crew share floating glowing fuel pods between two ships in open space inside the nebula, pods arranged in equal groups, wonder on their faces, {STYLE}."),
    ("ch4-issue002.png", "1536x1024", f"{JAKE} studies a holographic navigation display showing three glowing routes through a dense nebula, each route labelled with a fraction, intense focus on his face, {STYLE}."),
    ("ch5-issue002.png", "1536x1024", f"{JAKE} and the SS Meridian emerge from the purple fog nebula into glorious open space, both ships side by side, stars brilliant ahead, triumphant lighting, {STYLE}."),

    ("q1-issue002.png", "1024x1024", f"A holographic display showing a nebula divided into 6 equal glowing sectors, 2 of them lit up bright, the other 4 dimmer, fraction readout visible, space theme, {STYLE}."),
    ("q2-issue002.png", "1024x1024", f"A fuel gauge display showing a tank with 5 equal sections, only 2 sections glowing with fuel, 3 empty sections visible, space ship instrument panel, {STYLE}."),
    ("q3-issue002.png", "1024x1024", f"A fuel gauge display showing 5 sections with 2 full, then 1 section being drained to show only 1 section remaining, clear visual before and after, {STYLE}."),
    ("q4-issue002.png", "1024x1024", f"{JAKE} dividing 12 glowing spherical fuel pods into 2 equal groups of 6, one group floating toward his ship, one group toward the Meridian, {STYLE}."),
    ("q5-issue002.png", "1024x1024", f"6 glowing fuel pods arranged in a row, one third of them (2 pods) glowing differently in an emergency reserve box, the other 4 in the main supply, {STYLE}."),
    ("q6-issue002.png", "1024x1024", f"A holographic map showing two routes through a nebula — Route A covering a shorter arc, Route B covering a longer arc, fractions labelled, {STYLE}."),
    ("q7-issue002.png", "1024x1024", f"A journey progress display showing a route with 3 quarters completed in bright colour and 1 quarter remaining in dim colour, space navigation panel, {STYLE}."),
    ("q8-issue002.png", "1024x1024", f"A holographic timer showing 12 minutes beside a fraction bar divided into quarters, 3 sections filled representing the journey completed, 1 empty section remaining, {STYLE}."),
    ("q9-issue002.png", "1024x1024", f"9 glowing fuel pods being divided equally between 3 ships — Jake's ship, the Meridian, and a third rescue vessel — 3 pods floating to each, {STYLE}."),
    ("q10-issue002.png", "1024x1024", f"A holographic equation display showing fraction calculations with 1 quarter and 1 third, glowing mathematical notation, space computer interface, {STYLE}."),

    # ── ISSUE 3 — Asteroid Market ──────────────────────────────
    ("ch1-issue003.png", "1536x1024", f"{JAKE} arrives at a bustling space market carved inside a giant asteroid — stalls cut into glowing rock walls, holographic price tags, alien and human traders everywhere, {STYLE}."),
    ("ch2-issue003.png", "1536x1024", f"{JAKE} and a 10-year-old Japanese boy (Kenji, market apron, clever eyes) study fraction records on a holographic ledger together, stalls in background, {STYLE}."),
    ("ch3-issue003.png", "1536x1024", f"{JAKE} draws a large fraction wall on the asteroid market wall in chalk — rows of fractions showing equivalences, traders gathering to watch, {STYLE}."),
    ("ch4-issue003.png", "1536x1024", f"{JAKE} hides behind a market stall watching {PHANTOM} approach a fuel vendor, Jake ready to intervene, dramatic lighting, {STYLE}."),
    ("ch5-issue003.png", "1536x1024", f"{PHANTOM} shows {JAKE} its own fraction wall — a massive holographic display of equivalent fractions, the Phantom gesturing proudly, Jake looking thoughtful, {STYLE}."),

    ("q1-issue003.png", "1024x1024", f"Two fraction bars side by side — one showing 1 half, one showing 2 quarters — both clearly equal in length, space market background, {STYLE}."),
    ("q2-issue003.png", "1024x1024", f"Two fraction bars — one showing 2 sixths, one showing 1 third — both equal in length, equivalent fractions display, {STYLE}."),
    ("q3-issue003.png", "1024x1024", f"Two fraction bars — one showing 3 sixths, one showing 2 quarters — both equal to 1 half, glowing equivalence display, {STYLE}."),
    ("q4-issue003.png", "1024x1024", f"A fraction wall display showing the 3 quarters row with two equivalent fractions highlighted in gold, {STYLE}."),
    ("q5-issue003.png", "1024x1024", f"A number line from 0 to 1 with four fraction markers — 1 half, 3 sixths, 4 eighths, 2 quarters — all landing on the exact same point, glowing, {STYLE}."),
    ("q6-issue003.png", "1024x1024", f"A holographic fraction display showing 5 tenths with an arrow pointing to its simplified form, space market setting, {STYLE}."),
    ("q7-issue003.png", "1024x1024", f"A holographic fraction display showing 6 eighths with simplification arrows, {STYLE}."),
    ("q8-issue003.png", "1024x1024", f"Four fraction tokens — 1 quarter, 1 half, 3 quarters, 1 eighth — being arranged on a number line from smallest to largest, {STYLE}."),
    ("q9-issue003.png", "1024x1024", f"Two fuel ships side by side — Ship A (large) and Ship B (small) — each with a fraction bar showing 1 half full, but clearly different real amounts of fuel, {STYLE}."),
    ("q10-issue003.png", "1024x1024", f"Two fuel tanks side by side — one holding 16 units (half = 8 shaded), one holding 8 units (half = 4 shaded) — showing same fraction, different amounts, {STYLE}."),

    # ── ISSUE 4 — Number Line Station ─────────────────────────
    ("ch1-issue004.png", "1536x1024", f"{JAKE} races through a space station corridor shaped like a giant number line — fraction markers glowing on the walls from 0 to 1, some clearly in wrong positions, alarm lights flashing, {STYLE}."),
    ("ch2-issue004.png", "1536x1024", f"{JAKE} carefully repositions glowing fraction markers on the station's number line wall — 1 quarter and 3 quarters glowing as he places them correctly, focus and urgency on his face, {STYLE}."),
    ("ch3-issue004.png", "1536x1024", f"{JAKE} studies two fraction markers — 2 thirds and 3 quarters — placed very close together on the number line, comparing them carefully, {STYLE}."),
    ("ch4-issue004.png", "1536x1024", f"{PHANTOM} speaks through a glowing intercom panel showing fraction markers beyond the number 1 — improper fractions 5 quarters and 7 quarters visible, {JAKE} looking surprised, {STYLE}."),
    ("ch5-issue004.png", "1536x1024", f"{JAKE} installs the final fraction marker on the station's number line — all markers now glowing correctly from 0 to 2, three ships visible through a window with corrected navigation beams, {STYLE}."),

    ("q1-issue004.png", "1024x1024", f"A number line from 0 to 1 with the 1 half marker shown in the wrong position (near 3 quarters), an arrow showing where it should go, {STYLE}."),
    ("q2-issue004.png", "1024x1024", f"A number line from 0 to 1 with a question mark at the 1 quarter position, the correct position indicated, {STYLE}."),
    ("q3-issue004.png", "1024x1024", f"A number line from 0 to 1 showing 2 thirds and 3 quarters being placed, with a magnified view showing which is larger, {STYLE}."),
    ("q4-issue004.png", "1024x1024", f"A number line from 0 to 1 with 1 third and 2 thirds marked, showing three equal spaces between 0, 1 third, 2 thirds, and 1, {STYLE}."),
    ("q5-issue004.png", "1024x1024", f"A number line from 0 to 2 with 5 quarters marked just past the number 1, glowing blue, showing it sits between 1 and 2, {STYLE}."),
    ("q6-issue004.png", "1024x1024", f"A fraction conversion display showing 5 quarters being rewritten as 1 and 1 quarter, with fraction bar diagrams, {STYLE}."),
    ("q7-issue004.png", "1024x1024", f"A number line from 0 to 2 with four fractions being placed: 1 half, 3 quarters, 5 quarters, and 7 quarters, {STYLE}."),
    ("q8-issue004.png", "1024x1024", f"A number line from 0 to 2 with all quarter markers shown — 0, 1 quarter, 2 quarters, 3 quarters, 1, 5 quarters, 6 quarters, 7 quarters, 2 — each glowing, {STYLE}."),
    ("q9-issue004.png", "1024x1024", f"A number line with a missing marker between 3 quarters and 5 quarters, a question mark in the gap, {STYLE}."),
    ("q10-issue004.png", "1024x1024", f"A fraction display showing 4 quarters equals 1 whole, with a fraction bar and the equation 4 divided by 4 equals 1, {STYLE}."),

    # ── ISSUE 5 — Fraction Fair ────────────────────────────────
    ("ch1-issue005.png", "1536x1024", f"{JAKE} arrives at a spectacular space carnival — the Fraction Fair — with glowing rides, stalls, and prize wheels, all decorated with fraction symbols, set against a starfield, {STYLE}."),
    ("ch2-issue005.png", "1536x1024", f"{JAKE} at a Fuel Allocation game stall, holographic fuel gauges showing fractions, Jake calculating carefully with his notebook, {STYLE}."),
    ("ch3-issue005.png", "1536x1024", f"{PHANTOM} on a carnival stage demonstrating its fairness algorithm — giving every ship 1 quarter of a fuel tank, two very different sized ships receiving visually different amounts despite the same fraction, {JAKE} watching from the crowd, {STYLE}."),
    ("ch4-issue005.png", "1536x1024", f"{JAKE} racing through a fraction ordering challenge at the fair — fraction tokens flying, a finish line glowing ahead, competitive energy, {STYLE}."),
    ("ch5-issue005.png", "1536x1024", f"{JAKE} reaches {PHANTOM}'s control terminal — a glowing blue panel covered in fraction locks, Jake triumphantly entering the answer, the terminal beginning to open, {STYLE}."),

    ("q1-issue005.png", "1024x1024", f"A carnival prize wheel divided into 8 equal sections, 3 sections highlighted in gold where Jake landed, 5 sections dimmer, carnival fair setting, {STYLE}."),
    ("q2-issue005.png", "1024x1024", f"A fuel gauge showing 5 eighths full, with 3 eighths being transferred to Ship Alpha, resulting in 2 eighths remaining, clear before and after, {STYLE}."),
    ("q3-issue005.png", "1024x1024", f"Two fraction bars being added — 1 quarter and 1 half — showing them combining into 3 quarters, and a comparison to 7 eighths, {STYLE}."),
    ("q4-issue005.png", "1024x1024", f"Two fuel ships at a carnival fuelling station — a large ship receiving 1 quarter of a big tank, a small ship receiving 1 quarter of a small tank, same fraction sign but clearly different amounts, {STYLE}."),
    ("q5-issue005.png", "1024x1024", f"A small ship with an 8-unit tank, 1 quarter of it highlighted showing only 2 units, fraction display above, {STYLE}."),
    ("q6-issue005.png", "1024x1024", f"Four fraction tokens at a carnival racing track — 3 eighths, 5 eighths, 1 eighth, 7 eighths — being lined up from smallest to largest, {STYLE}."),
    ("q7-issue005.png", "1024x1024", f"Two fraction bars side by side — 5 sixths and 7 eighths — showing which is larger, comparison display, {STYLE}."),
    ("q8-issue005.png", "1024x1024", f"A fraction number line showing 3 eighths plus 2 eighths equals 5 eighths, with a gap to reach 1 whole indicated by a question mark, {STYLE}."),
    ("q9-issue005.png", "1024x1024", f"Three fraction tokens — 1 quarter, 2 quarters, 3 quarters — being added together, total shown as 6 quarters, then converted to 1 and 1 half, {STYLE}."),
    ("q10-issue005.png", "1024x1024", f"A number line from 0 to 2 showing 5 eighths marked, with a question mark showing what needs to be added to reach exactly 2, {STYLE}."),

    # ── ISSUE 6 — Fraction Core ────────────────────────────────
    ("ch1-issue006.png", "1536x1024", f"{JAKE}'s rocket flies through the breathtaking Zephyr Nebula — fractions hang in the air as glowing light bars and number lines woven through purple-gold gas clouds, the Fraction Core pulsing blue at the centre, {STYLE}."),
    ("ch2-issue006.png", "1536x1024", f"{JAKE} navigates using holographic fraction signals — mixed numbers and improper fractions glowing on his navigation panel, the Core getting closer, {STYLE}."),
    ("ch3-issue006.png", "1536x1024", f"{PHANTOM} presents a test to {JAKE} — three different sized ships, each losing the same fraction of fuel, but visually different real amounts being drained, {STYLE}."),
    ("ch4-issue006.png", "1536x1024", f"{JAKE} navigates a glowing logic maze inside the nebula — four branching routes each labelled with fraction calculations, dramatic lighting, {STYLE}."),
    ("ch5-issue006.png", "1536x1024", f"{JAKE} floats before {PHANTOM} in full form inside the Fraction Core — the Phantom enormous and made of shifting fraction bars, Jake small but determined, a moment of genuine confrontation, {STYLE}."),

    ("q1-issue006.png", "1024x1024", f"A number line from 1 to 2 with three mixed numbers marked — 1 and 1 quarter, 1 and 1 half, 1 and 3 quarters — glowing between the 1 and 2 markers, {STYLE}."),
    ("q2-issue006.png", "1024x1024", f"A fraction conversion display showing 1 and 3 quarters being rewritten as 7 quarters, with fraction bar diagrams, {STYLE}."),
    ("q3-issue006.png", "1024x1024", f"A fraction display showing 11 quarters being rewritten as 2 and 3 quarters, with grouping diagrams showing 4 quarters per whole, {STYLE}."),
    ("q4-issue006.png", "1024x1024", f"A fuel tank holding 24 units with 1 third (8 units) highlighted as the amount taken, clear visual proportions, {STYLE}."),
    ("q5-issue006.png", "1024x1024", f"Two tanks side by side — one with 24 units, one with 18 units — both showing 1 third taken, but clearly different absolute amounts drained, {STYLE}."),
    ("q6-issue006.png", "1024x1024", f"A journey path of 28 units with 3 quarters (21 units) shaded and 1 quarter (7 units) remaining, clear distance display, {STYLE}."),
    ("q7-issue006.png", "1024x1024", f"A 28-unit journey route with 21 units completed and 7 units remaining, space navigation display, {STYLE}."),
    ("q8-issue006.png", "1024x1024", f"Two time bars — 3 quarters of an hour and 1 quarter of an hour — combining to make 1 full hour, clock and fraction display, {STYLE}."),
    ("q9-issue006.png", "1024x1024", f"15 fuel station icons arranged in a grid with 1 fifth of each highlighted, mathematical display showing the total fraction taken across all stations, {STYLE}."),
    ("q10-issue006.png", "1024x1024", f"Three calculation displays side by side — 2 thirds of 24 units, 3 quarters of 16 units, 1 half of 12 units — with results and a total, {STYLE}."),

    # ── ISSUE 7 — The Fair Share Solution ─────────────────────
    ("ch1-issue007.png", "1536x1024", f"{JAKE} stands before {PHANTOM} inside the Fraction Core, holding an open notebook, ready to present his evidence — the Phantom still and attentive for the first time, {STYLE}."),
    ("ch2-issue007.png", "1536x1024", f"{JAKE} shows {PHANTOM} a number line demonstration — two number lines of different scales side by side showing 1 half of each, revealing different absolute amounts, {STYLE}."),
    ("ch3-issue007.png", "1536x1024", f"{PHANTOM}'s form shifts — its fraction bars reorganising into a new pattern — as realisation spreads across the Fraction Core, the atmosphere changing from tense to contemplative, {STYLE}."),
    ("ch4-issue007.png", "1536x1024", f"{PHANTOM} broadcasts a new fairness signal across the galaxy — ships of all sizes shown receiving different amounts to reach the same fill level, the galaxy responding, lights returning to stations, {STYLE}."),
    ("ch5-issue007.png", "1536x1024", f"{JAKE} receives the Star of Equal Shares medal from {PHANTOM} — now the Fraction Keeper, its form settled and calm, inside a glowing Fraction Core, triumphant warm lighting, {STYLE}."),

    ("q1-issue007.png", "1024x1024", f"Two fuel tanks side by side — Tank A holding 20 units (10 shaded as half full), Tank B holding 10 units (5 shaded as half full) — same fraction, clearly different amounts, {STYLE}."),
    ("q2-issue007.png", "1024x1024", f"Two fraction bars of the same length — one divided into halves (1 half shaded), one divided into thirds (1 third shaded) — clearly showing 1 half is more, {STYLE}."),
    ("q3-issue007.png", "1024x1024", f"A fuel tank holding 40 units with 1 quarter (10 units) highlighted as the amount lost at Kepler Station, {STYLE}."),
    ("q4-issue007.png", "1024x1024", f"Two tanks — Kepler (40 units, 10 lost) and Vega (16 units, 4 lost) — both showing 1 quarter taken but clearly different losses, comparison display, {STYLE}."),
    ("q5-issue007.png", "1024x1024", f"A 32-unit fuel tank with 3 quarters (24 units) highlighted as the target fill level, empty base shown, {STYLE}."),
    ("q6-issue007.png", "1024x1024", f"A 24-unit fuel tank with 3 quarters highlighted, showing 18 units needed to fill to 3 quarters from empty, {STYLE}."),
    ("q7-issue007.png", "1024x1024", f"A 16-unit tank shown half full (8 units) with an arrow showing the extra 4 units needed to reach 3 quarters, clear before and after display, {STYLE}."),
    ("q8-issue007.png", "1024x1024", f"Three fuel top-up displays — 1 quarter tank, 1 half tank, 3 quarters tank — arranged from smallest to largest, space distribution centre, {STYLE}."),
    ("q9-issue007.png", "1024x1024", f"Station A: a 40-unit tank at 1 quarter full (10 units shaded), needs to reach 3 quarters (30 units shaded), showing 20 units needed, {STYLE}."),
    ("q10-issue007.png", "1024x1024", f"Two stations side by side — Station A needing 20 units, Station B needing 10 units — a total of 30 units, with 60 units available shown, 30 left over, {STYLE}."),
]

def gen(filename, size, prompt):
    out = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(out):
        print(f"  ✓ {filename} (cached)")
        return True
    try:
        resp = client.images.generate(model="gpt-image-1", prompt=prompt, size=size, quality="high")
        img = base64.b64decode(resp.data[0].b64_json)
        open(out, "wb").write(img)
        print(f"  ✅ {filename} ({len(img)//1024}kb)")
        return True
    except Exception as e:
        print(f"  ❌ {filename}: {e}")
        return False

ok = total = 0
for fname, size, prompt in IMAGES:
    if gen(fname, size, prompt): ok += 1
    total += 1
    time.sleep(1.5)  # rate limit

print(f"\nDone: {ok}/{total} images generated")
