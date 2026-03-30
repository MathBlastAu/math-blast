#!/usr/bin/env python3
"""
Regenerate all Ocean Arc images for Issues 2, 3, and 4
with Pixar-style art direction + hybrid whale spot approach.
"""

import requests, base64, time, io, os
from PIL import Image, ImageDraw, ImageFilter

API_KEY = "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"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/ocean"

STYLE = "Pixar-style 3D CGI, stylised cartoon characters with large expressive eyes, dark moody underwater environment, cinematic low-key lighting, strong cyan and amber rim lights, bioluminescent elements casting coloured light, deep navy and blue-black shadows, warm amber practical light sources, detailed underwater coral architecture, volumetric underwater haze with light rays filtering from above, adventurous wonder-filled mood, high detail, 16:9 cinematic composition"

MARINA = "10-year-old girl, warm brown skin, dark brown eyes, dark hair pulled back, full underwater dive suit in deep teal with white trim and wave emblem on chest, clear full-face diving helmet with interior amber glow, amber wrist datapad on suit arm, lean build, determined expression"
FLICK = "small juvenile manta ray, deep navy blue body, electric cyan chevron markings on underbelly, glowing cyan wing-tips, two small twitching antenna fins above eyes, slightly translucent wing edges"
ELDER_LUMA = "small crab-like creature, deep burgundy-red shell with etched geometric patterns, large round amber eyes, pale gold sea-silk mantle draped over shell, black coral staff with glowing amber stone, four walking legs, three-fingered hands, wise dignified bearing"
WREN = "small young crab-like creature, bright amber shell with fresh unfaded patterns, large curious eyes, no mantle, nervous eager energy"
CORALFOLK = "small crab-like creatures with colourful shells, large round expressive eyes, four walking legs, three-fingered hands"

errors = []
success_count = 0

def gen_image(prompt, output_path):
    global success_count
    payload = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1536x1024",
        "quality": "medium",
        "n": 1
    }
    for attempt in range(3):
        try:
            resp = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=HEADERS, json=payload, timeout=120
            )
            data = resp.json()
            if "data" not in data:
                msg = data.get('error', {}).get('message', str(data))
                print(f"  ❌ ERROR ({attempt+1}/3): {msg}")
                if attempt < 2:
                    time.sleep(5)
                    continue
                errors.append(f"{os.path.basename(output_path)}: {msg}")
                return False
            img_bytes = base64.b64decode(data["data"][0]["b64_json"])
            with open(output_path, "wb") as f:
                f.write(img_bytes)
            kb = len(img_bytes) // 1024
            print(f"  ✅ {os.path.basename(output_path)} ({kb}KB)")
            success_count += 1
            time.sleep(1)
            return True
        except Exception as e:
            print(f"  ❌ EXCEPTION ({attempt+1}/3): {e}")
            if attempt < 2:
                time.sleep(5)
    errors.append(f"{os.path.basename(output_path)}: failed after 3 attempts")
    return False


def make_whale_spots(rows, cols, output_path):
    global success_count
    print(f"  🐋 Generating base whale for {os.path.basename(output_path)} ({rows}×{cols}={rows*cols} spots)...")
    prompt = "close-up of enormous whale flank, dark charcoal grey skin with subtle texture, deep dark ocean background, dramatic cinematic lighting, no spots, no markings, Pixar-style 3D CGI, dark moody underwater, cinematic lighting, cyan rim light, high detail, 16:9"
    payload = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1536x1024",
        "quality": "medium",
        "n": 1
    }
    for attempt in range(3):
        try:
            resp = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=HEADERS, json=payload, timeout=120
            )
            data = resp.json()
            if "data" not in data:
                msg = data.get('error', {}).get('message', str(data))
                print(f"  ❌ ERROR ({attempt+1}/3): {msg}")
                if attempt < 2:
                    time.sleep(5)
                    continue
                errors.append(f"{os.path.basename(output_path)}: {msg}")
                return False
            img_bytes = base64.b64decode(data["data"][0]["b64_json"])
            break
        except Exception as e:
            print(f"  ❌ EXCEPTION ({attempt+1}/3): {e}")
            if attempt < 2:
                time.sleep(5)
            else:
                errors.append(f"{os.path.basename(output_path)}: failed after 3 attempts")
                return False

    # Overlay spots
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    W, H = img.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    spot_r = 22
    h_gap = W // (cols + 1)
    v_gap = H // (rows + 1)

    for r in range(rows):
        for c in range(cols):
            cx = h_gap * (c + 1)
            cy = v_gap * (r + 1)
            draw.ellipse([cx-spot_r*2, cy-spot_r*2, cx+spot_r*2, cy+spot_r*2], fill=(0, 220, 180, 40))
            draw.ellipse([cx-spot_r-4, cy-spot_r-4, cx+spot_r+4, cy+spot_r+4], fill=(0, 240, 200, 100))
            draw.ellipse([cx-spot_r, cy-spot_r, cx+spot_r, cy+spot_r], fill=(80, 255, 220, 230))
            draw.ellipse([cx-8, cy-8, cx+8, cy+8], fill=(200, 255, 245, 255))

    overlay = overlay.filter(ImageFilter.GaussianBlur(2))
    result = Image.alpha_composite(img, overlay).convert("RGB")
    result.save(output_path)
    print(f"  ✅ {os.path.basename(output_path)} ({rows}×{cols} = {rows*cols} spots)")
    success_count += 1
    time.sleep(1)
    return True


# ─── ISSUE 2 ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("ISSUE 2 — Chapter images")
print("="*60)

i2 = f"{BASE}/issue002"

gen_image(
    f"vast ocean floor stretching to dark horizon, long rows of glowing amber signal stones arranged in a grid, {MARINA} and {FLICK} and {WREN} as small figures walking among the stones, midnight blue water, shafts of light from above, wide cinematic shot, {STYLE}",
    f"{i2}/ch1-outer-lattice-fields.png"
)
gen_image(
    f"{WREN} reaching out to touch a glowing amber signal stone in a row, {MARINA} walking alongside watching intently, {FLICK} hovering above them, rows of glowing stones stretching ahead into deep midnight blue water, cinematic underwater scene, {STYLE}",
    f"{i2}/ch2-wren-counting.png"
)
gen_image(
    f"enormous grid of glowing amber signal stones on ocean floor stretching to horizon, deep midnight blue water, bioluminescent glow, wide establishing shot conveying vast scale, no characters, {STYLE}",
    f"{i2}/ch3-vast-stone-grid.png"
)
gen_image(
    f"{MARINA} kneeling studying her glowing amber wrist datapad, {WREN} watching beside her with curious expression, {FLICK} wing-tips flaring with concern, rows of signal stones around them, one section of stones noticeably dark and dead, {STYLE}",
    f"{i2}/ch4-marina-wren-datapad.png"
)
gen_image(
    f"underwater view looking upward, {MARINA} and {WREN} and {FLICK} as small figures on ocean floor below, enormous dark ominous shadow silhouette passing through the water far above them, deep blue water, dramatic contrast between tiny figures and massive shadow, {STYLE}",
    f"{i2}/ch5-shadow-overhead.png"
)
gen_image(
    f"{MARINA} and {WREN} standing frozen on ocean floor both looking upward with wide eyes, {FLICK} wing-tips blazing bright cyan with alarm, enormous dark shadow visible above blotting out the filtered light, near-darkness on the ocean floor, tense and dramatic, {STYLE}",
    f"{i2}/cliffhanger-shadow-returns.png"
)

print("\nISSUE 2 — Quiz images")
print("-"*40)

gen_image(f"row of glowing amber signal stones on ocean floor, every second stone dramatically brighter than the others creating a clear alternating bright-dim-bright-dim pattern, the bright stones pulse with extra intensity, midnight blue water, no text, {STYLE}", f"{i2}/q1-skip-count-2s.png")
gen_image(f"five clearly separated pairs of glowing amber signal stones on ocean floor, each pair close together with clear space between pairs, ten stones total, deep midnight blue water, no text, {STYLE}", f"{i2}/q2-five-times-two.png")
gen_image(f"long row of glowing amber stones on ocean floor, every fifth stone dramatically larger and brighter creating a clear rhythmic pattern, the bright stones cast pools of light, underwater ocean floor, no text, {STYLE}", f"{i2}/q3-skip-count-5s.png")
gen_image(f"four clearly separated clusters of glowing amber signal stones on ocean floor, each cluster contains five stones arranged in a cross pattern, twenty stones total, deep midnight blue water, no text, {STYLE}", f"{i2}/q4-four-times-five.png")
gen_image(f"long row of glowing amber stones, every tenth stone is huge and brilliant casting a wide pool of amber light, the pattern creates a dramatic rhythm across the ocean floor, wide scene, no text, {STYLE}", f"{i2}/q5-skip-count-10s.png")
gen_image(f"three clearly separated large clusters of glowing amber signal stones on ocean floor, each cluster is a tight group of ten stones, thirty stones total, midnight blue water, no text, {STYLE}", f"{i2}/q6-three-times-ten.png")
gen_image(f"six clearly separated pairs of glowing amber signal stones on ocean floor, each pair side by side with clear gaps between pairs, twelve stones total, deep midnight blue water, no text, {STYLE}", f"{i2}/q7-six-times-two.png")
gen_image(f"seven clearly separated groups of glowing amber signal stones, each group has five stones in a neat line, thirty-five stones total, ocean floor, no text, {STYLE}", f"{i2}/q8-seven-times-five.png")
gen_image(f"nine clearly separated pairs of glowing amber signal stones on ocean floor, each pair of two clearly grouped, eighteen stones total, bioluminescent underwater scene, no text, {STYLE}", f"{i2}/q9-nine-times-two.png")
gen_image(f"eight clearly separated large clusters of glowing amber signal stones, each cluster of ten stones glowing brightly, eighty stones total, wide ocean floor scene, midnight blue water, no text, {STYLE}", f"{i2}/q10-eight-times-ten.png")

# ─── ISSUE 3 ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("ISSUE 3 — Chapter images")
print("="*60)

i3 = f"{BASE}/issue003"

gen_image(
    f"{ELDER_LUMA} leading {MARINA} and {FLICK} toward a massive ancient shipwreck covered in coral and bioluminescent growth, dramatic teal and gold light emanating from inside the wreck, dark deep water surroundings, sense of ancient mystery, {STYLE}",
    f"{i3}/ch1-archive-approach.png"
)
gen_image(
    f"{MARINA} inside ancient shipwreck library, gazing at a vast grid of glowing stone tablets arranged in rows and columns on the walls, {ELDER_LUMA} beside her pointing upward with black coral staff, deep teal and gold light, wooden beams encrusted with coral, {STYLE}",
    f"{i3}/ch2-marina-scanning.png"
)
gen_image(
    f"interior of ancient shipwreck, vast grid of glowing stone tablets in neat rows and columns filling the wall, close dramatic shot showing the array, deep teal and gold bioluminescent light, coral-encrusted wooden beams, majestic and ancient, no text on tablets, {STYLE}",
    f"{i3}/ch3-tablet-grid.png"
)
gen_image(
    f"{MARINA} kneeling reading a single glowing stone tablet on the shipwreck floor, her face lit by teal light in awe and concentration, {ELDER_LUMA} watching gravely, ancient patterns on the tablet surface with no readable text, {STYLE}",
    f"{i3}/ch4-ancient-record.png"
)
gen_image(
    f"close dramatic portrait of {ELDER_LUMA}, large amber eyes grave and knowing, black coral staff held firmly, pale gold mantle glowing softly, deep teal light of the Archive behind, serious wise expression, {STYLE}",
    f"{i3}/ch5-luma-knowing.png"
)
gen_image(
    f"interior of ancient shipwreck Archive, {MARINA} and {ELDER_LUMA} both pressing close to a large circular porthole window, outside the window an enormous dark fin silhouette passing slowly through the dark water, rows of faint blue-green bioluminescent spots visible on the creature, tense dramatic atmosphere, {STYLE}",
    f"{i3}/cliffhanger-archive-window.png"
)

print("\nISSUE 3 — Quiz tablet arrays")
print("-"*40)

TABLET_PROMPT = f"ancient shipwreck interior wall, glowing stone tablets in a neat grid, deep teal and gold bioluminescent light, wooden beams encrusted with coral, no text on tablets, {STYLE}"
for i in range(1, 9):
    gen_image(TABLET_PROMPT, f"{i3}/q{i}-tablet-array.png")

print("\nISSUE 3 — Quiz whale spots (hybrid)")
print("-"*40)

make_whale_spots(5, 5, f"{i3}/q9-whale-spots.png")
make_whale_spots(3, 8, f"{i3}/q10-whale-spots.png")

# ─── ISSUE 4 ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("ISSUE 4 — Chapter images")
print("="*60)

i4 = f"{BASE}/issue004"

gen_image(
    f"{MARINA} and {FLICK} descending into a vast deep ocean trench, water darkening dramatically from deep blue to near black below, faint blue-green bioluminescent glow pulsing far below, cinematic and awe-inspiring, sense of great depth and the unknown, {STYLE}",
    f"{i4}/ch1-deep-trench-descent.png"
)
gen_image(
    f"FULL REVEAL — enormous ancient whale, dark charcoal body, large gentle violet eyes, {MARINA} and {FLICK} tiny figures beside it emphasising its vast scale, deep ocean, majestic and awe-inspiring, the whale is clearly alive and aware but not threatening, {STYLE}",
    f"{i4}/ch2-whale-full-reveal.png"
)
gen_image(
    f"dramatic close-up of enormous whale flank, bioluminescent blue-green spots arranged in neat grid-like rows, deep ocean background, spectacular detail, dark charcoal skin glowing from within, no text, {STYLE}",
    f"{i4}/ch3-whale-spots-closeup.png"
)
gen_image(
    f"{MARINA} studying her glowing amber wrist datapad with intense focus and determination, {FLICK} hovering anxiously beside her, enormous whale silhouette visible as a vast dark presence in the water behind them, tense focused atmosphere, {STYLE}",
    f"{i4}/ch4-marina-calculating.png"
)
gen_image(
    f"vast ocean floor, grid of amber signal stones all activating and glowing bright simultaneously, wave of light spreading outward across the ocean floor, bioluminescent coral city visible in background, triumphant and beautiful, {STYLE}",
    f"{i4}/ch5-lattice-lighting.png"
)
gen_image(
    f"bioluminescent coral city Luminos fully lit at maximum brightness, {CORALFOLK} figures celebrating in the streets, lights and colours everywhere, {MARINA} and {FLICK} in foreground watching with joy, {ELDER_LUMA} beside {MARINA} extending one small three-fingered hand holding a glowing amber signal stone, warm triumphant scene, {STYLE}",
    f"{i4}/finale-luminos-celebration.png"
)

print("\nISSUE 4 — Quiz whale spots (hybrid)")
print("-"*40)

make_whale_spots(3, 6, f"{i4}/q1-whale-spots.png")
make_whale_spots(5, 6, f"{i4}/q2-whale-spots.png")
make_whale_spots(4, 7, f"{i4}/q3-whale-spots.png")
make_whale_spots(6, 7, f"{i4}/q4-whale-spots.png")
make_whale_spots(3, 8, f"{i4}/q5-whale-spots.png")

print("\nISSUE 4 — Quiz lattice signal images")
print("-"*40)

LATTICE_PROMPT = f"glowing amber signal stones on ocean floor activating in sequence, wave of light traveling through the grid, ocean floor, no text, {STYLE}"
for i in range(6, 11):
    gen_image(LATTICE_PROMPT, f"{i4}/q{i}-lattice-signal.png")

# ─── SUMMARY ──────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print(f"DONE — {success_count} images generated successfully")
if errors:
    print(f"\n❌ {len(errors)} ERRORS:")
    for e in errors:
        print(f"  - {e}")
else:
    print("✅ No errors!")
print("="*60)
