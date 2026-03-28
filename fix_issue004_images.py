#!/usr/bin/env python3
"""Regenerate images for Issue 4 that need fixing via Pillow (number lines)."""

from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"

# ── Colour palette ──────────────────────────────────────────────────────────
BG       = (13,  6,  48)   # dark space navy
BG2      = (20, 10, 60)    # slightly lighter panel
PURPLE   = (160,  60, 255)
CYAN     = (  0, 200, 255)
GOLD     = (255, 185,   0)
GREEN    = (  0, 220, 100)
RED      = (255,  80,  80)
WHITE    = (255, 255, 255)
GREY     = (100,  90, 140)
PINK     = (255, 100, 220)

def load_font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def star_bg(draw, w, h, n=80):
    import random; random.seed(42)
    for _ in range(n):
        x, y = random.randint(0,w), random.randint(0,h)
        r = random.choice([1,1,1,2])
        a = random.randint(80, 200)
        draw.ellipse([x-r,y-r,x+r,y+r], fill=(255,255,255,a))

def glow_rect(draw, x1, y1, x2, y2, col, radius=8):
    """Draw a rounded glowing rectangle."""
    r, g, b = col
    for spread in [12, 8, 4]:
        alpha = 40
        draw.rounded_rectangle([x1-spread, y1-spread, x2+spread, y2+spread],
                                radius=radius+spread, fill=(r, g, b, alpha))
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=col)

def draw_fraction(draw, x, y, num, den, colour, size=36, bold=True):
    """Draw a fraction as num/den stacked with a line between."""
    font_n = load_font(size, bold)
    font_d = load_font(size, bold)
    font_s = load_font(int(size*0.7))

    n_str = str(num)
    d_str = str(den)

    # measure widths
    n_w = draw.textlength(n_str, font=font_n)
    d_w = draw.textlength(d_str, font=font_d)
    max_w = max(n_w, d_w)
    line_pad = 6

    # numerator centred above line
    draw.text((x - n_w/2, y - size - 6), n_str, fill=colour, font=font_n)
    # fraction bar
    draw.line([(x - max_w/2 - line_pad, y), (x + max_w/2 + line_pad, y)], fill=colour, width=3)
    # denominator centred below line
    draw.text((x - d_w/2, y + 6), d_str, fill=colour, font=font_d)

def number_line(draw, lx, rx, y, ticks, labels, colour=CYAN, tick_h=18, label_y_offset=30, font_size=28):
    """Draw a number line from lx to rx at height y with ticks and labels."""
    # Main line
    draw.line([(lx, y), (rx, y)], fill=colour, width=4)
    # Arrowheads
    for dx in [6, 10]:
        draw.line([(rx-dx, y-dx//2), (rx, y), (rx-dx, y+dx//2)], fill=colour, width=3)

    font = load_font(font_size, bold=True)
    for frac_val, label_str, col in labels:
        px = lx + frac_val * (rx - lx)
        draw.line([(px, y-tick_h), (px, y+tick_h)], fill=col, width=3)
        w = draw.textlength(label_str, font=font)
        draw.text((px - w/2, y + label_y_offset), label_str, fill=col, font=font)


# ═══════════════════════════════════════════════════════════════════════════
# Q1 — Number line 0→1, ½ shown in wrong position (at ¾), arrow to correct
# ═══════════════════════════════════════════════════════════════════════════
def make_q1():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    star_bg(draw, W, H)

    # Title
    tf = load_font(42, bold=True)
    draw.text((W//2, 80), "Where should ½ go?", fill=GOLD, font=tf, anchor="mm")

    # Number line
    lx, rx, ly = 100, 900, 380
    # base line
    draw.line([(lx, ly), (rx, ly)], fill=CYAN, width=5)
    # arrow
    draw.polygon([(rx, ly), (rx-14, ly-8), (rx-14, ly+8)], fill=CYAN)

    font_tick = load_font(34, bold=True)
    font_sm   = load_font(26)

    # 0 tick
    draw.line([(lx, ly-22), (lx, ly+22)], fill=WHITE, width=4)
    draw.text((lx, ly+40), "0", fill=WHITE, font=font_tick, anchor="mt")

    # 1 tick
    draw.line([(rx, ly-22), (rx, ly+22)], fill=WHITE, width=4)
    draw.text((rx, ly+40), "1", fill=WHITE, font=font_tick, anchor="mt")

    # Wrong position: ½ at ¾
    wrong_x = lx + 0.75 * (rx - lx)
    draw.line([(wrong_x, ly-30), (wrong_x, ly+30)], fill=RED, width=4)
    draw.text((wrong_x, ly - 80), "½", fill=RED, font=load_font(38, bold=True), anchor="mm")
    draw.text((wrong_x, ly - 48), "✗ WRONG!", fill=RED, font=load_font(22), anchor="mm")

    # Correct position: ½ at 0.5
    correct_x = lx + 0.5 * (rx - lx)
    draw.line([(correct_x, ly-22), (correct_x, ly+22)], fill=GREEN, width=4)

    # Arrow from wrong to correct
    draw.line([(wrong_x, ly + 70), (correct_x, ly + 70)], fill=GOLD, width=4)
    draw.polygon([(correct_x, ly + 70), (correct_x + 14, ly + 62), (correct_x + 14, ly + 78)], fill=GOLD)
    draw.text(((wrong_x + correct_x) // 2, ly + 100), "belongs here!", fill=GOLD, font=load_font(28, bold=True), anchor="mm")

    # Midpoint label (green)
    draw.text((correct_x, ly + 140), "½", fill=GREEN, font=load_font(42, bold=True), anchor="mm")
    draw.text((correct_x, ly + 185), "exactly halfway", fill=GREEN, font=load_font(26), anchor="mm")

    # Question box
    qf = load_font(32, bold=True)
    draw.rounded_rectangle([60, 620, 960, 760], radius=18, fill=(40,20,80,220))
    draw.text((512, 660), "The Phantom put ½ in the wrong place.", fill=WHITE, font=load_font(28), anchor="mm")
    draw.text((512, 710), "Where should ½ actually sit?", fill=GOLD, font=qf, anchor="mm")

    img = img.convert("RGB")
    img.save(f"{OUT}/q1-issue004.png")
    print("✅ q1-issue004.png")


# ═══════════════════════════════════════════════════════════════════════════
# Q2 — Number line 0→1, where does ¼ go?
# ═══════════════════════════════════════════════════════════════════════════
def make_q2():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    star_bg(draw, W, H)

    draw.text((W//2, 80), "Where does ¼ belong?", fill=GOLD, font=load_font(42, bold=True), anchor="mm")

    lx, rx, ly = 100, 900, 340
    draw.line([(lx, ly), (rx, ly)], fill=CYAN, width=5)
    draw.polygon([(rx, ly), (rx-14, ly-8), (rx-14, ly+8)], fill=CYAN)

    font_tick = load_font(34, bold=True)

    # Ticks at 0, ¼, ½, ¾, 1
    ticks = [(0, "0", WHITE), (0.25, "¼", PURPLE), (0.5, "½", GREY), (0.75, "¾", GREY), (1.0, "1", WHITE)]
    for fv, lbl, col in ticks:
        px = lx + fv * (rx - lx)
        h = 28 if fv in [0.25, 0] else 18
        draw.line([(px, ly-h), (px, ly+h)], fill=col, width=4 if fv == 0.25 else 3)
        draw.text((px, ly + 40), lbl, fill=col, font=font_tick, anchor="mt")

    # Highlight ¼ position with glow
    qx = lx + 0.25 * (rx - lx)
    for spread in [16, 10, 5]:
        draw.ellipse([qx-spread, ly-spread, qx+spread, ly+spread], fill=(160,60,255, 60))
    draw.ellipse([qx-8, ly-8, qx+8, ly+8], fill=PURPLE)

    # Arrow pointing up to ¼
    draw.line([(qx, ly + 120), (qx, ly + 45)], fill=PURPLE, width=4)
    draw.polygon([(qx, ly + 45), (qx-8, ly+60), (qx+8, ly+60)], fill=PURPLE)
    draw.text((qx, ly + 155), "?", fill=PURPLE, font=load_font(72, bold=True), anchor="mm")

    # Show the 4 equal divisions
    draw.rounded_rectangle([60, 560, 960, 740], radius=16, fill=(20,10,55,220))
    draw.text((512, 600), "Divide the line into 4 equal parts.", fill=WHITE, font=load_font(28), anchor="mm")
    div_y = 660
    seg = (rx - lx) / 4
    for i in range(5):
        dx = lx + i * seg
        col = PURPLE if i == 1 else GREY
        draw.line([(dx, div_y - 20), (dx, div_y + 20)], fill=col, width=3)
        lbl = ["0", "1", "2", "3", "4"][i]
        draw.text((dx, div_y + 30), lbl, fill=col, font=load_font(24), anchor="mt")
    draw.text((512, 720), "¼ is the 1st mark — one jump from 0.", fill=GOLD, font=load_font(30, bold=True), anchor="mm")

    img = img.convert("RGB")
    img.save(f"{OUT}/q2-issue004.png")
    print("✅ q2-issue004.png")


# ═══════════════════════════════════════════════════════════════════════════
# Q4 — Number line 0→1, 1/3 and 2/3 with equal spacing highlighted
# ═══════════════════════════════════════════════════════════════════════════
def make_q4():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    star_bg(draw, W, H)

    draw.text((W//2, 80), "Placing 1/3 and 2/3", fill=GOLD, font=load_font(42, bold=True), anchor="mm")

    lx, rx, ly = 100, 880, 340
    draw.line([(lx, ly), (rx, ly)], fill=CYAN, width=5)
    draw.polygon([(rx, ly), (rx-14, ly-8), (rx-14, ly+8)], fill=CYAN)

    font_lbl = load_font(34, bold=True)
    thirds = [(0, "0", WHITE), (1/3, "1/3", PURPLE), (2/3, "2/3", CYAN), (1.0, "1", WHITE)]

    for fv, lbl, col in thirds:
        px = lx + fv * (rx - lx)
        h = 28 if fv not in [0, 1] else 22
        draw.line([(px, ly-h), (px, ly+h)], fill=col, width=4)
        draw.text((px, ly + 40), lbl, fill=col, font=font_lbl, anchor="mt")

    # Braces showing equal gaps
    gap = (rx - lx) / 3
    brace_y = ly - 70
    brace_col = GOLD
    for i in range(3):
        x1 = lx + i * gap
        x2 = x1 + gap
        mx = (x1 + x2) / 2
        draw.line([(x1+6, brace_y), (x2-6, brace_y)], fill=brace_col, width=3)
        draw.line([(x1+6, brace_y), (x1+6, brace_y+10)], fill=brace_col, width=3)
        draw.line([(x2-6, brace_y), (x2-6, brace_y+10)], fill=brace_col, width=3)
        draw.text((mx, brace_y - 24), "equal", fill=brace_col, font=load_font(22, bold=True), anchor="mm")

    # Info box
    draw.rounded_rectangle([60, 560, 960, 780], radius=16, fill=(20,10,55,220))
    draw.text((512, 610), "Thirds split the line into 3 EQUAL jumps.", fill=WHITE, font=load_font(30, bold=True), anchor="mm")
    draw.text((512, 665), "0 → 1/3 → 2/3 → 1", fill=CYAN, font=load_font(36, bold=True), anchor="mm")
    draw.text((512, 725), "What do you notice about the gaps?", fill=GOLD, font=load_font(28), anchor="mm")

    img = img.convert("RGB")
    img.save(f"{OUT}/q4-issue004.png")
    print("✅ q4-issue004.png")


# ═══════════════════════════════════════════════════════════════════════════
# Q7 — Number line 0→2, place 4 fractions: ½, ¾, 5/4, 7/4
# ═══════════════════════════════════════════════════════════════════════════
def make_q7():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    star_bg(draw, W, H)

    draw.text((W//2, 70), "Order from Smallest to Largest", fill=GOLD, font=load_font(38, bold=True), anchor="mm")
    draw.text((W//2, 120), "½ · ¾ · 5/4 · 7/4", fill=CYAN, font=load_font(44, bold=True), anchor="mm")

    lx, rx, ly = 60, 940, 360
    draw.line([(lx, ly), (rx, ly)], fill=CYAN, width=5)
    draw.polygon([(rx, ly), (rx-14, ly-8), (rx-14, ly+8)], fill=CYAN)

    font_lbl = load_font(28, bold=True)

    # Marks: 0, ½, ¾, 1, 5/4, 7/4, 2
    marks = [
        (0.0,  "0",   WHITE),
        (0.25, "¼",   GREY),
        (0.5,  "½",   PURPLE),
        (0.75, "¾",   PURPLE),
        (1.0,  "1",   WHITE),
        (1.25, "5/4", CYAN),
        (1.5,  "6/4", GREY),
        (1.75, "7/4", CYAN),
        (2.0,  "2",   WHITE),
    ]
    highlight = {0.5, 0.75, 1.25, 1.75}
    for fv, lbl, col in marks:
        px = lx + (fv / 2) * (rx - lx)
        h = 30 if fv in highlight else 16
        lw = 4 if fv in highlight else 2
        draw.line([(px, ly-h), (px, ly+h)], fill=col, width=lw)
        draw.text((px, ly + 36), lbl, fill=col, font=font_lbl, anchor="mt")

    # Dots on the highlighted fractions
    for fv, col in [(0.5, PURPLE), (0.75, PURPLE), (1.25, CYAN), (1.75, CYAN)]:
        px = lx + (fv / 2) * (rx - lx)
        draw.ellipse([px-9, ly-9, px+9, ly+9], fill=col)

    # Order row
    draw.rounded_rectangle([60, 560, 960, 760], radius=16, fill=(20,10,55,220))
    draw.text((512, 600), "Correct order (smallest → largest):", fill=WHITE, font=load_font(28), anchor="mm")
    draw.text((512, 660), "½  <  ¾  <  5/4  <  7/4", fill=GOLD, font=load_font(40, bold=True), anchor="mm")
    draw.text((512, 720), "Fractions < 1 come before fractions > 1", fill=CYAN, font=load_font(26), anchor="mm")

    img = img.convert("RGB")
    img.save(f"{OUT}/q7-issue004.png")
    print("✅ q7-issue004.png")


# ═══════════════════════════════════════════════════════════════════════════
# Q8 — Number line 0→2, ALL quarter markers lit up
# ═══════════════════════════════════════════════════════════════════════════
def make_q8():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    star_bg(draw, W, H)

    draw.text((W//2, 70), "Count from 0 to 2 in steps of ¼", fill=GOLD, font=load_font(38, bold=True), anchor="mm")

    lx, rx, ly = 60, 940, 320
    draw.line([(lx, ly), (rx, ly)], fill=CYAN, width=5)
    draw.polygon([(rx, ly), (rx-14, ly-8), (rx-14, ly+8)], fill=CYAN)

    font_lbl = load_font(26, bold=True)
    font_num  = load_font(22)

    quarters = [
        (0,   "0"),
        (1/8, "1/4"),
        (2/8, "2/4"),
        (3/8, "3/4"),
        (4/8, "4/4\n= 1"),
        (5/8, "5/4"),
        (6/8, "6/4"),
        (7/8, "7/4"),
        (1.0, "8/4\n= 2"),
    ]
    colours = [WHITE, PURPLE, PURPLE, PURPLE, GOLD, CYAN, CYAN, CYAN, GOLD]

    for (fv, lbl), col in zip(quarters, colours):
        px = lx + fv * (rx - lx)
        h = 32 if col in [GOLD, WHITE] else 24
        draw.line([(px, ly-h), (px, ly+h)], fill=col, width=4 if col != GREY else 2)
        # glow dot
        draw.ellipse([px-7, ly-7, px+7, ly+7], fill=col)
        # label (handle multiline)
        lines = lbl.split("\n")
        for j, line in enumerate(lines):
            w = draw.textlength(line, font=font_lbl)
            draw.text((px - w/2, ly + 40 + j*26), line, fill=col, font=font_lbl)

    # Step count indicators
    step_y = ly - 100
    for i in range(8):
        x1 = lx + (i/8) * (rx - lx)
        x2 = lx + ((i+1)/8) * (rx - lx)
        mx = (x1 + x2) / 2
        col = PURPLE if i < 4 else CYAN
        draw.line([(x1+4, step_y), (x2-4, step_y)], fill=col, width=2)
        draw.text((mx, step_y - 18), f"step {i+1}", fill=col, font=load_font(18), anchor="mm")

    # Answer box
    draw.rounded_rectangle([60, 600, 960, 780], radius=16, fill=(20,10,55,220))
    draw.text((512, 645), "8 steps of ¼ get from 0 all the way to 2", fill=WHITE, font=load_font(30, bold=True), anchor="mm")
    draw.text((512, 700), "How many steps are there in total?", fill=GOLD, font=load_font(34, bold=True), anchor="mm")
    draw.text((512, 750), "(Don't count the starting 0!)", fill=GREY, font=load_font(24), anchor="mm")

    img = img.convert("RGB")
    img.save(f"{OUT}/q8-issue004.png")
    print("✅ q8-issue004.png")


# ═══════════════════════════════════════════════════════════════════════════
# Q6 — Replace give-away image with a blank conversion question (no answer)
# ═══════════════════════════════════════════════════════════════════════════
def make_q6():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    star_bg(draw, W, H)

    draw.text((W//2, 80), "Convert the Improper Fraction!", fill=GOLD, font=load_font(40, bold=True), anchor="mm")

    # Show 5/4 large
    draw.rounded_rectangle([280, 160, 740, 460], radius=20, fill=(30,15,70,220))
    draw.text((512, 220), "5", fill=PURPLE, font=load_font(120, bold=True), anchor="mm")
    draw.line([(320, 310), (700, 310)], fill=WHITE, width=6)
    draw.text((512, 400), "4", fill=PURPLE, font=load_font(120, bold=True), anchor="mm")

    # Arrow →
    draw.text((512, 510), "=  ?  wholes  +  ?  quarters", fill=CYAN, font=load_font(36, bold=True), anchor="mm")

    # Hint: bar model (blank boxes)
    bx, by, bh = 120, 590, 70
    seg_w = (W - 240) / 4
    for i in range(4):
        x1 = bx + i * seg_w
        draw.rounded_rectangle([x1+4, by, x1+seg_w-4, by+bh], radius=10,
                                fill=(60,30,120), outline=PURPLE, width=3)
        draw.text((x1 + seg_w/2, by + bh/2), "1/4", fill=PURPLE, font=load_font(28, bold=True), anchor="mm")

    # 5th box
    draw.rounded_rectangle([bx + 4*seg_w + 4, by, bx + 4*seg_w + seg_w - 4, by+bh],
                            radius=10, fill=(0,60,40), outline=CYAN, width=3)
    draw.text((bx + 4*seg_w + seg_w/2, by + bh/2), "1/4", fill=CYAN, font=load_font(28, bold=True), anchor="mm")

    draw.text((W//2, 710), "5 quarters = how many wholes and quarters?", fill=GOLD, font=load_font(28, bold=True), anchor="mm")
    draw.text((W//2, 760), "Hint: 4/4 = 1 whole!", fill=GREEN, font=load_font(28), anchor="mm")

    img = img.convert("RGB")
    img.save(f"{OUT}/q6-issue004.png")
    print("✅ q6-issue004.png")


# ═══════════════════════════════════════════════════════════════════════════
# Q10 — 4/4 = 1: Fractions connect to whole numbers (no give-away style)
# ═══════════════════════════════════════════════════════════════════════════
def make_q10():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    star_bg(draw, W, H)

    draw.text((W//2, 75), "The Missing Marker — Boss Challenge", fill=PINK, font=load_font(36, bold=True), anchor="mm")

    # Number line 0→2 with gap between 3/4 and 5/4
    lx, rx, ly = 60, 940, 320
    draw.line([(lx, ly), (rx, ly)], fill=CYAN, width=5)
    draw.polygon([(rx, ly), (rx-14, ly-8), (rx-14, ly+8)], fill=CYAN)

    font_lbl = load_font(28, bold=True)
    marks = [(0,"0",WHITE),(0.25,"¼",GREY),(0.5,"½",GREY),(0.75,"¾",GREEN),(1.0,"?",RED),(1.25,"5/4",GREEN),(1.5,"6/4",GREY),(1.75,"7/4",GREY),(2.0,"2",WHITE)]
    for fv, lbl, col in marks:
        px = lx + (fv/2) * (rx - lx)
        h = 26 if lbl in ["¾","?","5/4"] else 16
        lw = 4 if lbl == "?" else 3
        draw.line([(px, ly-h), (px, ly+h)], fill=col, width=lw)
        draw.text((px, ly+36), lbl, fill=col, font=font_lbl, anchor="mt")

    # Gap highlight between ¾ and 5/4
    x_3q = lx + (0.75/2) * (rx - lx)
    x_5q = lx + (1.25/2) * (rx - lx)
    x_gap = lx + (1.0/2) * (rx - lx)
    draw.rounded_rectangle([x_gap-28, ly-35, x_gap+28, ly+35], radius=10,
                            fill=(255,80,80,60), outline=RED, width=3)
    draw.text((x_gap, ly - 70), "REMOVED!", fill=RED, font=load_font(22, bold=True), anchor="mm")

    # Phantom message box
    draw.rounded_rectangle([50, 430, 970, 590], radius=16, fill=(30,10,50,230))
    draw.text((512, 475), "The Phantom's note:", fill=GREY, font=load_font(24), anchor="mm")
    draw.text((512, 525), '"4/4 is a whole number, not a fraction."', fill=RED, font=load_font(28, bold=True), anchor="mm")

    # Question
    draw.rounded_rectangle([50, 620, 970, 780], radius=16, fill=(20,10,55,220))
    draw.text((512, 665), "What fraction did the Phantom remove?", fill=WHITE, font=load_font(30, bold=True), anchor="mm")
    draw.text((512, 715), "And is the Phantom RIGHT or WRONG?", fill=GOLD, font=load_font(34, bold=True), anchor="mm")

    img = img.convert("RGB")
    img.save(f"{OUT}/q10-issue004.png")
    print("✅ q10-issue004.png")


if __name__ == "__main__":
    make_q1()
    make_q2()
    make_q4()
    make_q6()
    make_q7()
    make_q8()
    make_q10()
    print("\nAll images done!")
