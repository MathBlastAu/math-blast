#!/usr/bin/env python3
"""
Generate all Space Issue 1 question images programmatically using Pillow.
Step 1: Generate one AI background per question type (no bars, no counts, no characters)
Step 2: Overlay precise fuel gauge diagrams using Pillow
"""
from openai import OpenAI
import base64, os, time
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

client = OpenAI()
IMG_DIR = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/images/")
BG_DIR  = os.path.expanduser("~/.openclaw/workspace/projects/math-blast/images/space_bg/")
os.makedirs(BG_DIR, exist_ok=True)

# ── COLOURS ────────────────────────────────────────────────────────────────
GREEN      = (50, 220, 100)
GREEN_GLOW = (80, 255, 140)
RED        = (220, 60, 60)
RED_GLOW   = (255, 100, 80)
DARK       = (20, 15, 45)
EMPTY      = (40, 35, 70)
BORDER     = (120, 100, 200)
GOLD       = (255, 210, 60)
BLUE_GLOW  = (100, 160, 255)
WHITE      = (255, 255, 255)
BG_PANEL   = (15, 10, 35, 220)  # semi-transparent dark panel

SIZE = 1024

def get_font(size=36, bold=False):
    try:
        if bold:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except:
        return ImageFont.load_default()

def gen_bg(filename, prompt):
    path = BG_DIR + filename
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        print(f"  ⏭ bg/{filename} exists")
        return path
    print(f"  🌌 bg/{filename}...")
    try:
        r = client.images.generate(model="gpt-image-1", prompt=prompt, size="1024x1024")
        data = base64.b64decode(r.data[0].b64_json)
        with open(path, 'wb') as f: f.write(data)
        print(f"  ✅ ({len(data):,}b)")
        time.sleep(12)
        return path
    except Exception as e:
        print(f"  ❌ {e}"); return None

def load_bg(path):
    if path and os.path.exists(path):
        return Image.open(path).convert("RGBA").resize((SIZE, SIZE))
    # fallback: dark gradient
    img = Image.new("RGBA", (SIZE, SIZE), (10, 5, 30, 255))
    return img

def add_dark_panel(img, x, y, w, h, radius=20):
    """Add a semi-transparent dark panel."""
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=(10, 5, 30, 200))
    return Image.alpha_composite(img, overlay)

def draw_gauge_bar(img, x, y, w, h, total, filled, fill_color=GREEN, empty_color=EMPTY, border_color=BORDER, radius=8):
    """Draw a horizontal segmented fuel gauge bar."""
    d = ImageDraw.Draw(img)
    gap = 4
    seg_w = (w - gap * (total - 1)) / total
    for i in range(total):
        sx = x + i * (seg_w + gap)
        color = fill_color if i < filled else empty_color
        # segment
        d.rounded_rectangle([sx, y, sx+seg_w, y+h], radius=radius, fill=color)
        # border
        d.rounded_rectangle([sx, y, sx+seg_w, y+h], radius=radius, outline=border_color, width=2)
    # outer border
    d.rounded_rectangle([x-3, y-3, x+w+3, y+h+3], radius=radius+3, outline=BORDER, width=2)

def draw_gauge_bar_glow(draw, img, x, y, w, h, total, filled, fill_color=GREEN):
    """Draw gauge with glow effect on filled sections."""
    draw_gauge_bar(img, x, y, w, h, total, filled, fill_color)

def draw_label(img, x, y, text, size=32, color=GOLD, center=False):
    d = ImageDraw.Draw(img)
    font = get_font(size)
    if center:
        bbox = d.textbbox((0,0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = x - tw // 2
    d.text((x, y), text, fill=color, font=font)

def draw_fuel_pod(img, cx, cy, r=28):
    """Draw a single glowing fuel pod (rounded rect)."""
    d = ImageDraw.Draw(img)
    # glow
    d.ellipse([cx-r-8, cy-r-8, cx+r+8, cy+r+8], fill=(50, 120, 255, 60))
    # body
    d.rounded_rectangle([cx-r, cy-r*2, cx+r, cy+r*2], radius=r, fill=(60, 100, 220))
    d.rounded_rectangle([cx-r, cy-r*2, cx+r, cy+r*2], radius=r, outline=(140, 180, 255), width=3)
    # shine
    d.ellipse([cx-r//2, cy-r*2+6, cx, cy-r//2], fill=(180, 210, 255, 120))

def save(img, filename):
    path = IMG_DIR + filename
    img = img.convert("RGB")
    img.save(path, "PNG")
    print(f"  💾 {filename}")

# ── GENERATE BACKGROUNDS ────────────────────────────────────────────────────
print("\n── Generating backgrounds ──")

BG_PROMPT = (
    "Futuristic space station interior background. Clean flat dark panel in the centre "
    "for overlaying content. Deep space visible through windows on the sides. "
    "Glowing blue and purple ambient lighting. Disney Pixar CGI style. "
    "No characters, no text, no gauges, no bars, no objects in the centre panel."
)

bg_single = gen_bg("single_gauge_bg.png", BG_PROMPT)
bg_double = gen_bg("double_gauge_bg.png", BG_PROMPT)
bg_pods   = gen_bg("pods_bg.png",
    "Futuristic space station storage bay background. Shelving units visible on sides. "
    "Clean flat dark surface in centre. Ambient blue glow. Disney Pixar CGI style. "
    "No characters, no text, no objects in centre.")

# ── BUILD QUESTION IMAGES ───────────────────────────────────────────────────
print("\n── Building question images ──")

BAR_Y   = 380   # vertical centre for single bar
BAR_H   = 90    # bar height
BAR_X   = 120   # left margin
BAR_W   = SIZE - 240  # bar width

# ── Q1: 4 sections, 1 filled ────────────────────────────────────────────────
img = load_bg(bg_single)
img = add_dark_panel(img, 80, 300, SIZE-160, 280)
draw_gauge_bar(img, BAR_X, BAR_Y, BAR_W, BAR_H, 4, 1)
draw_label(img, SIZE//2, BAR_Y-60, "Tank: 4 equal sections", 34, GOLD, center=True)
draw_label(img, SIZE//2, BAR_Y+BAR_H+20, "1 section is full", 32, WHITE, center=True)
save(img, "q1-issue001.png")

# ── Q2: 2 sections, 1 filled ────────────────────────────────────────────────
img = load_bg(bg_single)
img = add_dark_panel(img, 80, 300, SIZE-160, 280)
draw_label(img, SIZE//2, BAR_Y-70, "Tank A — 2 equal sections", 34, GOLD, center=True)
draw_gauge_bar(img, BAR_X, BAR_Y, BAR_W, BAR_H, 2, 1)
draw_label(img, SIZE//2, BAR_Y+BAR_H+20, "1 section is full", 32, WHITE, center=True)
save(img, "q2-issue001.png")

# ── Q3: 8 sections, 3 filled ────────────────────────────────────────────────
img = load_bg(bg_single)
img = add_dark_panel(img, 80, 300, SIZE-160, 280)
draw_label(img, SIZE//2, BAR_Y-70, "Tank B — 8 equal sections", 34, GOLD, center=True)
draw_gauge_bar(img, BAR_X, BAR_Y, BAR_W, BAR_H, 8, 3)
draw_label(img, SIZE//2, BAR_Y+BAR_H+20, "3 sections are full", 32, WHITE, center=True)
save(img, "q3-issue001.png")

# ── Q4: Two 4-section bars — BEFORE (4/4) and AFTER (3/4) ────────────────────
img = load_bg(bg_double)
img = add_dark_panel(img, 60, 220, SIZE-120, 500)
d = ImageDraw.Draw(img)
bw = (SIZE - 280) // 2
by = 380

# BEFORE label
draw_label(img, 60 + bw//2, 250, "BEFORE", 34, GOLD, center=True)
draw_gauge_bar(img, 60, by, bw, BAR_H, 4, 4)
draw_label(img, 60 + bw//2, by+BAR_H+16, "4 / 4 full", 28, GREEN_GLOW, center=True)

# Arrow
ax = SIZE//2
d.polygon([(ax-18, by+BAR_H//2-10),(ax+18, by+BAR_H//2),(ax-18, by+BAR_H//2+10)], fill=BLUE_GLOW)

# AFTER label
rx = SIZE//2 + 40
draw_label(img, rx + bw//2, 250, "AFTER", 34, GOLD, center=True)
draw_gauge_bar(img, rx, by, bw, BAR_H, 4, 3, fill_color=GREEN, empty_color=RED)
draw_label(img, rx + bw//2, by+BAR_H+16, "3 / 4 full", 28, GREEN_GLOW, center=True)

draw_label(img, SIZE//2, 580, "One section was removed", 32, RED_GLOW, center=True)
save(img, "q4-issue001.png")

# ── Q5: Two 4-section bars — BEFORE (2/4) and AFTER (1/4) ────────────────────
img = load_bg(bg_double)
img = add_dark_panel(img, 60, 220, SIZE-120, 500)
d = ImageDraw.Draw(img)

draw_label(img, 60 + bw//2, 250, "BEFORE", 34, GOLD, center=True)
draw_gauge_bar(img, 60, by, bw, BAR_H, 4, 2)
draw_label(img, 60 + bw//2, by+BAR_H+16, "2 / 4 full", 28, GREEN_GLOW, center=True)

d.polygon([(ax-18, by+BAR_H//2-10),(ax+18, by+BAR_H//2),(ax-18, by+BAR_H//2+10)], fill=BLUE_GLOW)

draw_label(img, rx + bw//2, 250, "AFTER", 34, GOLD, center=True)
draw_gauge_bar(img, rx, by, bw, BAR_H, 4, 1, fill_color=GREEN, empty_color=RED)
draw_label(img, rx + bw//2, by+BAR_H+16, "1 / 4 full", 28, GREEN_GLOW, center=True)

draw_label(img, SIZE//2, 580, "One section was removed", 32, RED_GLOW, center=True)
save(img, "q5-issue001.png")

# ── Q6: Adding 1/2 + 3/4 ─────────────────────────────────────────────────────
img = load_bg(bg_double)
img = add_dark_panel(img, 60, 160, SIZE-120, 600)
d = ImageDraw.Draw(img)
sw = (SIZE - 340) // 3
sy = 360

draw_label(img, 60 + sw//2, 200, "Tank A", 30, GOLD, center=True)
draw_gauge_bar(img, 60, sy, sw, BAR_H, 4, 2)  # 1/2 = 2/4
draw_label(img, 60 + sw//2, sy+BAR_H+14, "1/2 (= 2/4)", 26, WHITE, center=True)

mx = 60 + sw + 20
draw_label(img, mx+30, sy+BAR_H//2-16, "+", 56, WHITE)

draw_label(img, mx+90 + sw//2, 200, "Tank C", 30, GOLD, center=True)
draw_gauge_bar(img, mx+90, sy, sw, BAR_H, 4, 3)
draw_label(img, mx+90 + sw//2, sy+BAR_H+14, "3/4", 26, WHITE, center=True)

ex = mx+90+sw+20
draw_label(img, ex+24, sy+BAR_H//2-16, "=", 56, WHITE)

draw_label(img, ex+80 + sw//2, 200, "Combined", 30, GOLD, center=True)
draw_gauge_bar(img, ex+80, sy, sw, BAR_H, 4, 4)  # full + 1 extra shown
draw_label(img, ex+80 + sw//2, sy+BAR_H+14, "5/4 — more than full!", 24, GREEN_GLOW, center=True)

draw_label(img, SIZE//2, 570, "Does Orion have enough?", 32, GOLD, center=True)
save(img, "q6-issue001.png")

# ── Q7: Comparing 3/8 vs 4/8 ─────────────────────────────────────────────────
img = load_bg(bg_double)
img = add_dark_panel(img, 60, 200, SIZE-120, 540)
d = ImageDraw.Draw(img)
cw = (SIZE - 280) // 2
cy2 = 370

draw_label(img, 60 + cw//2, 230, "Tank B  —  3/8", 34, GOLD, center=True)
draw_gauge_bar(img, 60, cy2, cw, BAR_H, 8, 3)
draw_label(img, 60 + cw//2, cy2+BAR_H+14, "3 out of 8", 28, WHITE, center=True)

draw_label(img, SIZE//2, cy2+BAR_H//2-20, "vs", 44, WHITE, center=True)

rx2 = SIZE//2 + 40
draw_label(img, rx2 + cw//2, 230, "Half a tank  —  4/8", 34, GOLD, center=True)
draw_gauge_bar(img, rx2, cy2, cw, BAR_H, 8, 4, fill_color=(100, 160, 255))
draw_label(img, rx2 + cw//2, cy2+BAR_H+14, "4 out of 8  (= 1/2)", 28, WHITE, center=True)

draw_label(img, SIZE//2, 600, "Is 3/8 more or less than 1/2?", 30, GOLD, center=True)
save(img, "q7-issue001.png")

# ── Q8: Exactly 6 fuel pods in 2 groups of 3 ─────────────────────────────────
img = load_bg(bg_pods)
img = add_dark_panel(img, 60, 180, SIZE-120, 560)
d = ImageDraw.Draw(img)

pod_y   = 420
pod_gap = 110
group1_x = [160, 270, 380]
group2_x = [644, 754, 864]

for cx in group1_x:
    draw_fuel_pod(img, cx, pod_y)
for cx in group2_x:
    draw_fuel_pod(img, cx, pod_y)

# dividing line
d.line([(SIZE//2, pod_y-120), (SIZE//2, pod_y+120)], fill=(150, 150, 255), width=3)
# dashed middle marker
for y in range(pod_y-100, pod_y+100, 20):
    d.line([(SIZE//2-2, y), (SIZE//2+2, y)], fill=BLUE_GLOW, width=4)

draw_label(img, SIZE//4, 220, "6 fuel pods", 36, GOLD, center=True)
draw_label(img, SIZE//4, 620, "Ship 1", 30, WHITE, center=True)
draw_label(img, 3*SIZE//4, 620, "Ship 2", 30, WHITE, center=True)
draw_label(img, SIZE//2, 700, "Shared equally — what fraction each?", 28, WHITE, center=True)
save(img, "q8-issue001.png")

# ── Q9: 3 bars × 4 sections, 1 removed per bar ───────────────────────────────
img = load_bg(bg_single)
img = add_dark_panel(img, 60, 140, SIZE-180, 650)
d = ImageDraw.Draw(img)
bx = 80
bw9 = 680
bh9 = 70
gap9 = 30
ys = [200, 200+bh9+gap9, 200+2*(bh9+gap9)]

for i, by9 in enumerate(ys):
    draw_gauge_bar(img, bx, by9, bw9, bh9, 4, 3, fill_color=GREEN, empty_color=RED)
    draw_label(img, bx + bw9 + 16, by9 + bh9//2 - 16, f"Tank {i+1}", 26, GOLD)

# Combined arrow
total_y = ys[-1] + bh9 + 30
draw_label(img, SIZE//2, total_y, "3 × 1/4 taken  =  ?  total", 32, WHITE, center=True)

draw_label(img, SIZE//2, 140, "Each tank lost 1 section", 30, GOLD, center=True)
save(img, "q9-issue001.png")

# ── Q10: 3 nights timeline, 1/4 taken each night ─────────────────────────────
img = load_bg(bg_single)
img = add_dark_panel(img, 60, 120, SIZE-120, 700)
d = ImageDraw.Draw(img)
bw10 = 340
bh10 = 70
gap10 = 24
col_x = [80, 80, 80]
night_y = [200, 200+bh10+gap10, 200+2*(bh10+gap10)]
nights = ["Night 1", "Night 2", "Night 3"]

for i, (by10, label) in enumerate(zip(night_y, nights)):
    draw_label(img, bw10//2 + 80, by10-28, label, 26, GOLD, center=True)
    draw_gauge_bar(img, 80, by10, bw10, bh10, 4, 3, fill_color=GREEN, empty_color=RED)

# Arrow to total
ax10 = 80 + bw10 + 30
total_bar_y = night_y[1]
d.polygon([(ax10, total_bar_y+bh10//2-14),(ax10+36, total_bar_y+bh10//2),(ax10, total_bar_y+bh10//2+14)], fill=BLUE_GLOW)

tx = ax10 + 56
draw_label(img, tx + bw10//2 - 20, night_y[0]-28, "Total taken", 26, GOLD, center=True)
draw_gauge_bar(img, tx, night_y[0], bw10, bh10, 4, 3, fill_color=RED)
draw_label(img, tx + bw10//2 - 20, night_y[0]+bh10+10, "3/4 of a full tank", 26, WHITE, center=True)

draw_label(img, SIZE//2, 620, "Same fraction taken each night — which?", 28, GOLD, center=True)
save(img, "q10-issue001.png")

print("\n✅ All question images built.")
