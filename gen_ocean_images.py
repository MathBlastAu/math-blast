#!/usr/bin/env python3
"""Generate all images for Ocean Arc issues 1-4."""
import os, base64, time, requests, json
from pathlib import Path

API_KEY = "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"
BASE = Path(__file__).parent

# CHARACTER TEMPLATES
MARINA = "10-year-old girl, warm brown skin, dark eyes, dark hair in practical bun, deep teal research suit with white trim and wave emblem on chest, clear dome visor pulled back, amber wrist datapad, lean swimmer's build, determined expression"
FLICK = "small juvenile manta ray, deep navy blue body, electric cyan chevron markings on underbelly, glowing cyan wing-tips, two small twitching antenna fins above eyes, slightly translucent wing edges, hovering in water"
ELDER_LUMA = "small crab-like creature, deep burgundy-red shell with etched geometric patterns, large round amber eyes, pale gold sea-silk mantle draped over shell, black coral staff with glowing amber stone, four walking legs, three-fingered hands, wise dignified bearing"
LUMINOS = "bioluminescent coral city, deep indigo water, vivid orange and pink coral towers, glowing teal light trails, Coralfolk figures"
OUTER_LATTICE = "vast ocean floor, grid of amber glowing stones, midnight blue water, scattered coral, shafts of filtered light from above"
ARCHIVE = "interior of ancient shipwreck, rows of glowing stone tablets in grid formation, deep teal and gold light, wooden beams encrusted with coral"
DEEP_TRENCH = "vast open dark water, midnight blue fading to black, enormous creature visible, bioluminescent spots in grid rows, awe-inspiring scale"

STYLE = "cinematic digital illustration, deep ocean atmosphere, bioluminescent lighting, vivid teal and cyan accents, dark navy background, no text, no numbers, no symbols, no equations, no letters"

IMAGES = {
    "issue001": [
        ("ch1-sub-approaching-luminos.png",
         f"A small research submarine with glowing porthole lights approaches a vast bioluminescent coral city in deep ocean water. The city glows with orange and pink coral towers and teal light trails. {LUMINOS}. {MARINA} is barely visible through the porthole. {FLICK} visible near the sub. {STYLE}"),
        ("ch2-luminos-exterior.png",
         f"Wide establishing shot of the Luminos coral city exterior, viewed from outside. {LUMINOS}. Coralfolk move purposefully through glowing teal streets. Deep indigo water surrounds the city. {STYLE}"),
        ("ch3-elder-luma-greeting.png",
         f"Close encounter: {ELDER_LUMA} greets {MARINA} at the entrance to Luminos. Elder Luma holds out a three-fingered hand in welcome. {FLICK} hovers nearby. Bioluminescent coral background. {LUMINOS}. {STYLE}"),
        ("ch3-elder-luma-lattice.png",
         f"{ELDER_LUMA} gestures at glowing amber signal stones embedded in the ocean floor. {MARINA} kneels to examine them closely. {FLICK} watches from nearby. {OUTER_LATTICE}. {STYLE}"),
        ("ch4-marina-datapad.png",
         f"{MARINA} studies glowing amber wrist datapad intently. {FLICK} hovers at her shoulder, wing-tips glowing cyan. Background shows rows of glowing Lattice stones. {OUTER_LATTICE}. {STYLE}"),
        ("ch5-lattice-flickering.png",
         f"A section of the Lattice signal stones flickers and goes dark, while others glow brightly. Coralfolk figures stand frozen, worried. {OUTER_LATTICE}. Deep ocean mood, tension in the light patterns. {STYLE}"),
        ("cliffhanger-deep-glow.png",
         f"Looking down into the darkest deep water below the ocean floor. Far below, a faint rhythmic bioluminescent glow pulses in a regular pattern, arranged in rows, barely visible in the blackness. The glow suggests something immense and ancient. Midnight blue fading to absolute black. {STYLE}"),
        ("q1-fish-groups.png",
         f"Two separate circular fish pens on the ocean floor, each containing exactly three small colourful fish. The pens are clearly separated with equal numbers. No text, no numbers. Underwater scene with coral and gentle light. {STYLE}"),
        ("q2-fish-groups.png",
         f"Four separate circular fish pens on the ocean floor, each containing exactly two small fish. Pens clearly separated, equal groups. Underwater coral scene. {STYLE}"),
        ("q3-fish-groups.png",
         f"Three separate square fish pens on the ocean floor, each containing exactly five small colourful fish. Equal groups, clearly separated. Underwater scene. {STYLE}"),
        ("q4-fish-groups.png",
         f"Five separate circular fish pens on the ocean floor, each with exactly two small fish. Equal groups of two, clearly separated. Underwater coral scene. {STYLE}"),
        ("q5-fish-groups.png",
         f"Two large circular fish pens side by side on the ocean floor, each containing exactly six colourful fish. Two equal groups of six. Underwater scene. {STYLE}"),
        ("q6-lattice-stones.png",
         f"Four groups of amber glowing signal stones on the ocean floor, each group containing exactly four stones arranged in a small cluster. Four equal groups of four, clearly separated. {OUTER_LATTICE}. {STYLE}"),
        ("q7-lattice-stones.png",
         f"Three groups of amber glowing signal stones on the ocean floor, each group containing exactly six stones. Three equal groups of six, clearly separated. {OUTER_LATTICE}. {STYLE}"),
        ("q8-lattice-stones.png",
         f"Five groups of amber glowing signal stones on the ocean floor, each group containing exactly four stones. Five equal groups of four, clearly separated. {OUTER_LATTICE}. {STYLE}"),
        ("q9-lattice-stones.png",
         f"Two groups of amber glowing signal stones, each group containing exactly seven stones arranged neatly. Two equal groups of seven. {OUTER_LATTICE}. {STYLE}"),
        ("q10-lattice-stones.png",
         f"Three small groups of amber glowing signal stones on the ocean floor, each group containing exactly three stones in a triangle. Three equal groups of three. {OUTER_LATTICE}. {STYLE}"),
    ],
    "issue002": [
        ("ch1-outer-lattice-fields.png",
         f"A small research submarine approaches the vast outer Lattice fields. The ocean floor stretches as far as can be seen, covered in a grid of glowing amber stones. {OUTER_LATTICE}. {STYLE}"),
        ("ch2-wren-introduction.png",
         f"A young Coralfolk keeper named Wren, similar to {ELDER_LUMA} but smaller and with brighter unfaded shell markings, stands beside a row of Lattice stones. {MARINA} leans forward with interest. {FLICK} hovers nearby. {OUTER_LATTICE}. {STYLE}"),
        ("ch3-vast-stone-grid.png",
         f"A sweeping wide-angle view of the vast outer Lattice field. Rows and rows of amber glowing stones extend to the horizon of the ocean floor. Some glow brightly, others are dark. Midnight blue water. {OUTER_LATTICE}. {STYLE}"),
        ("ch4-marina-wren-datapad.png",
         f"{MARINA} holds up her glowing amber wrist datapad showing a pattern of lines. A small Coralfolk keeper stands beside her pointing at the pattern. {OUTER_LATTICE}. {FLICK} watches. {STYLE}"),
        ("ch5-shadow-overhead.png",
         f"Looking upward from the ocean floor: an enormous dark shadow passes overhead, blocking out the filtered light that falls from above. The shadow is enormous, its edges barely visible. {MARINA} and a small Coralfolk figure stand looking up. {OUTER_LATTICE}. {STYLE}"),
        ("cliffhanger-shadow-returns.png",
         f"{MARINA} and a young Coralfolk keeper stand frozen, both staring upward. The enormous shadow has returned, larger this time. The filtered light above is almost completely blocked. Deep tension. {OUTER_LATTICE}. {STYLE}"),
        ("q1-skip-count-2s.png",
         f"A row of amber Lattice stones along the ocean floor. Every second stone glows brightly, the others are dim, creating a clear alternating skip-count pattern. No text or numbers. {OUTER_LATTICE}. {STYLE}"),
        ("q2-five-times-two.png",
         f"Five pairs of amber glowing Lattice stones on the ocean floor, arranged in a clear row with small gaps between each pair. Five groups of two stones. {OUTER_LATTICE}. {STYLE}"),
        ("q3-skip-count-5s.png",
         f"A long row of Lattice stones along the ocean floor. Every fifth stone glows brightly, with four dim stones between each glowing one. Clear skip-count-by-5 pattern. {OUTER_LATTICE}. {STYLE}"),
        ("q4-four-times-five.png",
         f"Four groups of five amber glowing Lattice stones on the ocean floor, each group clearly separated. Four equal groups of five stones. {OUTER_LATTICE}. {STYLE}"),
        ("q5-skip-count-10s.png",
         f"A very long row of Lattice stones. Every tenth stone glows brightly with nine dim ones between each lit stone. Clear skip-count-by-10 visual. {OUTER_LATTICE}. {STYLE}"),
        ("q6-three-times-ten.png",
         f"Three groups of ten amber glowing Lattice stones on the ocean floor, each group in a neat row of ten, clearly separated from the next group. {OUTER_LATTICE}. {STYLE}"),
        ("q7-six-times-two.png",
         f"Six pairs of amber glowing Lattice stones arranged in a row with gaps between each pair. Six equal groups of two. {OUTER_LATTICE}. {STYLE}"),
        ("q8-seven-times-five.png",
         f"Seven groups of five amber glowing Lattice stones, each group clearly separated. Seven equal groups of five stones. {OUTER_LATTICE}. {STYLE}"),
        ("q9-nine-times-two.png",
         f"Nine pairs of amber glowing Lattice stones arranged in a row, each pair clearly separated. Nine equal groups of two. {OUTER_LATTICE}. {STYLE}"),
        ("q10-eight-times-ten.png",
         f"Eight rows of ten amber glowing Lattice stones on the ocean floor, arranged in a clear grid pattern. Eight equal groups of ten. {OUTER_LATTICE}. {STYLE}"),
    ],
    "issue003": [
        ("ch1-archive-approach.png",
         f"{MARINA} and {ELDER_LUMA} swim toward the entrance of a massive ancient shipwreck half-buried in the ocean floor. The ship is encrusted with coral growth. Warm teal and gold light glows from inside. {ARCHIVE}. {STYLE}"),
        ("ch2-archive-interior.png",
         f"Grand interior of the Archive shipwreck. Rows and columns of glowing stone tablets fill the space in a perfect grid formation. {ARCHIVE}. Awe-inspiring scale. {STYLE}"),
        ("ch3-marina-scanning.png",
         f"{MARINA} moves carefully along a row of glowing stone tablets in the Archive, scanning them with her amber wrist datapad. {ELDER_LUMA} watches. {ARCHIVE}. {STYLE}"),
        ("ch3-tablet-grid.png",
         f"Close-up of the Archive tablet grid: glowing stone tablets arranged in perfect rows and columns. Deep teal and gold light. {ARCHIVE}. No text on any tablet. {STYLE}"),
        ("ch4-ancient-record.png",
         f"{MARINA} kneels reading a single glowing stone tablet, her face illuminated by its warm amber light. {ELDER_LUMA} stands beside her, watching gravely. {ARCHIVE}. {STYLE}"),
        ("ch4-whale-illustration.png",
         f"An ancient stylised illustration carved into a large stone tablet. It shows a massive whale shape with bioluminescent spots arranged in grid-like rows across its body. Ancient artistic style, no text. {ARCHIVE}. {STYLE}"),
        ("cliffhanger-archive-window.png",
         f"Looking at a large circular porthole window in the side of the shipwreck Archive. Outside the glass, a vast fin and rows of glowing blue-green spots pass slowly by, taking up the entire window. The scale is enormous. {MARINA} presses her hand to the glass. {STYLE}"),
        ("q1-tablet-array.png",
         f"Three rows of four glowing stone tablets each, arranged in a neat grid pattern in the Archive. Twelve tablets total in a 3x4 array. {ARCHIVE}. {STYLE}"),
        ("q2-tablet-array.png",
         f"Four rows of three glowing stone tablets each, arranged in a neat grid pattern. Same twelve tablets, different orientation. {ARCHIVE}. {STYLE}"),
        ("q3-tablet-array.png",
         f"Two rows of seven glowing stone tablets each, arranged in a horizontal grid pattern. {ARCHIVE}. {STYLE}"),
        ("q4-tablet-array.png",
         f"Seven rows of two glowing stone tablets each, arranged vertically. Same fourteen tablets shown as tall columns. {ARCHIVE}. {STYLE}"),
        ("q5-tablet-array.png",
         f"Five rows of three glowing stone tablets each, arranged in a neat grid. Fifteen tablets total. {ARCHIVE}. {STYLE}"),
        ("q6-tablet-array.png",
         f"Three rows of five glowing stone tablets each, arranged in a horizontal grid. Fifteen tablets, different orientation. {ARCHIVE}. {STYLE}"),
        ("q7-tablet-array.png",
         f"Four rows of six glowing stone tablets each, arranged in a neat grid. Twenty-four tablets total. {ARCHIVE}. {STYLE}"),
        ("q8-tablet-array.png",
         f"Six rows of four glowing stone tablets each, arranged in a neat grid. Same twenty-four tablets. {ARCHIVE}. {STYLE}"),
        ("q9-whale-spots.png",
         f"A close-up view of the ancient stone tablet illustration showing a section of the Whale with five rows of five bioluminescent spots each, arranged in a perfect grid pattern. Artistic, stylised. {ARCHIVE}. {STYLE}"),
        ("q10-whale-spots.png",
         f"An ancient stone tablet illustration showing three rows of eight bioluminescent spots arranged in a clean grid pattern across a whale's surface. No text. {ARCHIVE}. {STYLE}"),
        ("ch5-luma-knowing.png",
         f"{ELDER_LUMA} stands very still with an expression of grave recognition, amber eyes wide. In the background, warm bioluminescent light glows through a porthole window behind him. {ARCHIVE}. Emotional, significant moment. {STYLE}"),
    ],
    "issue004": [
        ("ch1-deep-trench-descent.png",
         f"{MARINA} in her research sub descends into the darkest deep water of the ocean. {FLICK} glows cyan beside the sub. Below, a faint blue-green bioluminescent glow hints at something enormous. {DEEP_TRENCH}. {STYLE}"),
        ("ch2-whale-glimpse.png",
         f"The first glimpse of the Resonance Whale in the deep dark water: rows of bioluminescent blue-green spots visible in the blackness, arranged in grid patterns. The creature's scale is suggested but not fully shown. {DEEP_TRENCH}. {STYLE}"),
        ("ch2-whale-full-reveal.png",
         f"The full reveal of the Resonance Whale. An enormous dark charcoal grey creature, vast beyond imagining, covered in bioluminescent blue-green spots arranged in perfect grid-like rows. One enormous violet eye looks directly forward. {MARINA}'s tiny sub is visible for scale. {DEEP_TRENCH}. Awe-inspiring, majestic, gentle. {STYLE}"),
        ("ch3-whale-spots-closeup.png",
         f"Close-up of the Resonance Whale's body surface, showing bioluminescent blue-green spots arranged in clear rows and columns, pulsing rhythmically. Dark charcoal grey skin between the spots. Beautiful and mathematical. {STYLE}"),
        ("ch4-marina-calculating.png",
         f"{MARINA} works intensely on her glowing amber wrist datapad, surrounded by the blue-green bioluminescent light of the Whale. {FLICK} hovers close beside her, wing-tips steady cyan. {DEEP_TRENCH}. {STYLE}"),
        ("ch4-flick-signal.png",
         f"{FLICK} races upward through dark water, wing-tips blazing bright cyan, carrying a glowing signal pulse. The little manta ray is surrounded by a trail of light. Far below, the Whale's bioluminescent glow is visible. {STYLE}"),
        ("ch5-lattice-lighting.png",
         f"The ocean floor lights up as section after section of the Lattice signal stones reactivate, spreading outward in a wave of amber glow. The pattern matches the Whale's grid. From above, it looks like a mathematical grid waking up. {OUTER_LATTICE}. {STYLE}"),
        ("finale-luminos-celebration.png",
         f"Luminos city glows at full brilliant brightness. Hundreds of Coralfolk line the glowing teal streets in celebration. {ELDER_LUMA} stands at the front, extending something small and glowing toward {MARINA}. {FLICK} hovers beside Marina. {LUMINOS}. Joyful, celebratory. {STYLE}"),
        ("q1-whale-spots.png",
         f"Three rows of six bioluminescent blue-green spots arranged in a clean grid pattern on dark ocean background. No text, no labels. {STYLE}"),
        ("q2-whale-spots.png",
         f"Five rows of six bioluminescent blue-green spots arranged in a clean grid pattern on dark ocean background. No text. {STYLE}"),
        ("q3-whale-spots.png",
         f"Four rows of seven bioluminescent blue-green spots arranged in a clean grid. Dark background. No text. {STYLE}"),
        ("q4-whale-spots.png",
         f"Six rows of seven bioluminescent blue-green spots arranged in a clean grid. Dark background. No text. {STYLE}"),
        ("q5-whale-spots.png",
         f"Three rows of eight bioluminescent blue-green spots arranged in a clean grid. Dark background. No text. {STYLE}"),
        ("q6-lattice-signal.png",
         f"Five rows of eight amber glowing Lattice signal stones, arranged in a clean grid on the ocean floor. {OUTER_LATTICE}. {STYLE}"),
        ("q7-lattice-signal.png",
         f"Seven groups of six amber glowing Lattice stones on the ocean floor, clearly separated in groups. {OUTER_LATTICE}. {STYLE}"),
        ("q8-lattice-signal.png",
         f"Four groups of eight amber glowing Lattice stones on the ocean floor, each group clearly separated. {OUTER_LATTICE}. {STYLE}"),
        ("q9-lattice-signal.png",
         f"Six groups of six amber glowing Lattice stones on the ocean floor arranged in a grid. {OUTER_LATTICE}. {STYLE}"),
        ("q10-whale-farewell.png",
         f"Eight rows of seven bioluminescent blue-green spots arranged in a beautiful clean grid pattern, softly glowing. The pattern feels peaceful and farewell-like. Dark ocean background. No text. {STYLE}"),
    ],
}

def generate_image(prompt, out_path):
    if out_path.exists():
        print(f"  SKIP (exists): {out_path.name}")
        return True
    print(f"  GEN: {out_path.name}")
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard",
        "response_format": "b64_json"
    }
    try:
        r = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        b64 = data["data"][0]["b64_json"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"  OK: {out_path.name}")
        return True
    except Exception as e:
        print(f"  ERROR {out_path.name}: {e}")
        return False

if __name__ == "__main__":
    total = sum(len(v) for v in IMAGES.values())
    done = 0
    errors = []
    for issue, items in IMAGES.items():
        print(f"\n=== {issue.upper()} ===")
        img_dir = BASE / "images" / "ocean" / issue
        img_dir.mkdir(parents=True, exist_ok=True)
        for fname, prompt in items:
            out_path = img_dir / fname
            ok = generate_image(prompt, out_path)
            done += 1
            if not ok:
                errors.append(f"{issue}/{fname}")
            time.sleep(0.5)
    print(f"\n=== DONE: {done}/{total} ===")
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
