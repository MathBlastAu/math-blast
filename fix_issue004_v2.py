#!/usr/bin/env python3
"""Fix Issue 4 images — clean Pillow style matching Issues 1-3 (no answer text, no repeated question)."""

from PIL import Image, ImageDraw, ImageFont
import os, random

OUT = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"

# ── Colours ──────────────────────────────────────────────────────────────────
BG     = (13, 6, 48)
PURPLE = (160, 60, 255)
CYAN   = (0, 200, 255)
GOLD   = (255, 185, 0)
GREEN  = (0, 220, 100)
RED    = (255, 80, 80)
WHITE  = (255, 255, 255)
GREY   = (100, 90, 140)
PINK   = (255, 100, 220)
DARK   = (20, 10, 60)

def font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def stars(draw, w, h, n=80):
    random.seed(42)
    for _ in range(n):
        x, y = random.randint(0, w), random.randint(0, h)
        r = random.choice([1, 1, 2])
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, random.randint(80, 200)))

def panel(draw, x1, y1, x2, y2, col=DARK, radius=14):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=col, outline=PURPLE, width=2)

def number_line(draw, lx, rx, cy, lo=0.0, hi=1.0, marks=None, font_size=30):
    """Draw a number line. marks = list of (fraction_value_0to1_of_range, label, colour)"""
    draw.line([(lx, cy), (rx, cy)], fill=CYAN, width=5)
    # arrowhead
    draw.polygon([(rx, cy), (rx-14, cy-7), (rx-14, cy+7)], fill=CYAN)
    f = font(font_size, bold=True)
    if marks:
        span = rx - lx
        val_range = hi - lo
        for fv, lbl, col in marks:
            px = lx + ((fv - lo) / val_range) * span
            draw.line([(px, cy-22), (px, cy+22)], fill=col, width=4)
            w = draw.textlength(lbl, font=f)
            draw.text((px - w/2, cy + 32), lbl, fill=col, font=f)

def save(img, name):
    img.convert("RGB").save(f"{OUT}/{name}")
    print(f"  ✅ {name}")


# ══════════════════════════════════════════════════════════════════════════════
# Q1 — Number line 0→1, half marker in wrong spot, no answer revealed
# ══════════════════════════════════════════════════════════════════════════════
def make_q1():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    # Title
    d.text((W//2, 80), "Number Line: 0 to 1", fill=GOLD, font=font(44, True), anchor="mm")

    lx, rx, cy = 80, 920, 380

    # Main line + 0 and 1 ticks
    d.line([(lx, cy), (rx, cy)], fill=CYAN, width=5)
    d.polygon([(rx, cy), (rx-14, cy-7), (rx-14, cy+7)], fill=CYAN)

    for fv, lbl, col in [(0.0, "0", WHITE), (1.0, "1", WHITE)]:
        px = lx + fv * (rx - lx)
        d.line([(px, cy-24), (px, cy+24)], fill=col, width=4)
        d.text((px, cy+36), lbl, fill=col, font=font(32, True), anchor="mt")

    # ½ marker placed at ¾ position (wrong) — shown in red with question mark
    wrong_px = lx + 0.75 * (rx - lx)
    d.line([(wrong_px, cy-30), (wrong_px, cy+30)], fill=RED, width=4)
    d.text((wrong_px, cy - 60), "½  ?", fill=RED, font=font(36, True), anchor="mm")
    d.text((wrong_px, cy - 26), "← moved!", fill=RED, font=font(22), anchor="mm")

    # ¼ and ¾ reference ticks (faint)
    for fv, lbl in [(0.25, "¼"), (0.5, "?"), (0.75, "¾")]:
        px = lx + fv * (rx - lx)
        col = GREY if fv != 0.5 else GOLD
        d.line([(px, cy-14), (px, cy+14)], fill=col, width=2)
        d.text((px, cy+36), lbl, fill=col, font=font(28), anchor="mt")

    # Instruction panel
    panel(d, 60, 560, 960, 720)
    d.text((512, 610), "The Phantom moved the ½ marker to the wrong place.", fill=WHITE, font=font(30), anchor="mm")
    d.text((512, 660), "Where should ½ actually sit?", fill=CYAN, font=font(36, True), anchor="mm")
    d.text((512, 710), "Think: halfway between 0 and 1.", fill=GREY, font=font(26), anchor="mm")

    save(img, "q1-issue004.png")


# ══════════════════════════════════════════════════════════════════════════════
# Q2 — Number line 0→1, where does ¼ go? (no answer revealed)
# ══════════════════════════════════════════════════════════════════════════════
def make_q2():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    d.text((W//2, 80), "Number Line: 0 to 1", fill=GOLD, font=font(44, True), anchor="mm")

    lx, rx, cy = 80, 920, 380
    d.line([(lx, cy), (rx, cy)], fill=CYAN, width=5)
    d.polygon([(rx, cy), (rx-14, cy-7), (rx-14, cy+7)], fill=CYAN)

    # 0 and 1
    for fv, lbl in [(0.0, "0"), (1.0, "1")]:
        px = lx + fv * (rx - lx)
        d.line([(px, cy-24), (px, cy+24)], fill=WHITE, width=4)
        d.text((px, cy+36), lbl, fill=WHITE, font=font(32, True), anchor="mt")

    # 4 equal segments shown
    seg = (rx - lx) / 4
    for i in range(5):
        px = lx + i * seg
        col = PURPLE if i == 1 else GREY
        lbl = ["0", "?", "½", "¾", "1"][i]
        lw = 4 if i == 1 else 2
        d.line([(px, cy - (24 if i == 1 else 14)), (px, cy + (24 if i == 1 else 14))], fill=col, width=lw)
        d.text((px, cy + 36), lbl, fill=col, font=font(30, True), anchor="mt")

    # Highlight the question mark position with a glow
    qpx = lx + seg
    for sp in [20, 12, 6]:
        d.ellipse([qpx-sp, cy-sp, qpx+sp, cy+sp], fill=(160, 60, 255, 40))
    d.ellipse([qpx-9, cy-9, qpx+9, cy+9], fill=PURPLE)

    panel(d, 60, 560, 960, 720)
    d.text((512, 610), "The line is split into 4 equal parts.", fill=WHITE, font=font(30), anchor="mm")
    d.text((512, 660), "Where does ¼ sit on the number line?", fill=CYAN, font=font(36, True), anchor="mm")
    d.text((512, 710), "Count: 1 jump from 0.", fill=GREY, font=font(26), anchor="mm")

    save(img, "q2-issue004.png")


# ══════════════════════════════════════════════════════════════════════════════
# Q3 — Number line showing 2/3 and 3/4 placed close together (Jake fixing)
# ══════════════════════════════════════════════════════════════════════════════
def make_q3():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    d.text((W//2, 80), "Comparing 2/3 and 3/4", fill=GOLD, font=font(44, True), anchor="mm")

    lx, rx, cy = 80, 920, 340
    d.line([(lx, cy), (rx, cy)], fill=CYAN, width=5)
    d.polygon([(rx, cy), (rx-14, cy-7), (rx-14, cy+7)], fill=CYAN)

    for fv, lbl in [(0.0, "0"), (1.0, "1")]:
        px = lx + fv * (rx - lx)
        d.line([(px, cy-24), (px, cy+24)], fill=WHITE, width=4)
        d.text((px, cy+36), lbl, fill=WHITE, font=font(32, True), anchor="mt")

    # 2/3 ≈ 0.667, 3/4 = 0.75 — placed very close together
    for fv, lbl, col in [(2/3, "2/3", PURPLE), (0.75, "3/4", CYAN)]:
        px = lx + fv * (rx - lx)
        d.line([(px, cy-28), (px, cy+28)], fill=col, width=4)
        d.text((px, cy-52), lbl, fill=col, font=font(34, True), anchor="mm")

    # Arrow showing they're very close
    px1 = lx + (2/3) * (rx - lx)
    px2 = lx + 0.75 * (rx - lx)
    d.line([(px1, cy + 80), (px2, cy + 80)], fill=GOLD, width=3)
    d.text(((px1+px2)//2, cy + 110), "close together!", fill=GOLD, font=font(26, True), anchor="mm")

    panel(d, 60, 580, 960, 740)
    d.text((512, 630), "The Phantom placed 2/3 and 3/4 almost in the same spot.", fill=WHITE, font=font(28), anchor="mm")
    d.text((512, 680), "Which is larger — 2/3 or 3/4?", fill=CYAN, font=font(36, True), anchor="mm")
    d.text((512, 730), "Which sits further along the line?", fill=GREY, font=font(26), anchor="mm")

    save(img, "q3-issue004.png")


# ══════════════════════════════════════════════════════════════════════════════
# Q4 — Number line 0→1 with 1/3 and 2/3, equal spacing (no answer labelled)
# ══════════════════════════════════════════════════════════════════════════════
def make_q4():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    d.text((W//2, 80), "Placing Thirds", fill=GOLD, font=font(44, True), anchor="mm")

    lx, rx, cy = 80, 920, 360
    d.line([(lx, cy), (rx, cy)], fill=CYAN, width=5)
    d.polygon([(rx, cy), (rx-14, cy-7), (rx-14, cy+7)], fill=CYAN)

    for fv, lbl, col in [(0.0, "0", WHITE), (1/3, "1/3", PURPLE), (2/3, "2/3", CYAN), (1.0, "1", WHITE)]:
        px = lx + fv * (rx - lx)
        lw = 4 if fv in [1/3, 2/3] else 3
        h = 28 if fv in [1/3, 2/3] else 22
        d.line([(px, cy-h), (px, cy+h)], fill=col, width=lw)
        d.text((px, cy+36), lbl, fill=col, font=font(32, True), anchor="mt")

    # Show the 3 equal sections with bracket indicators
    gap = (rx - lx) / 3
    for i in range(3):
        x1 = lx + i * gap
        x2 = x1 + gap
        mx = (x1 + x2) / 2
        # bracket
        d.line([(x1+4, cy-70), (x2-4, cy-70)], fill=GOLD, width=2)
        d.line([(x1+4, cy-70), (x1+4, cy-60)], fill=GOLD, width=2)
        d.line([(x2-4, cy-70), (x2-4, cy-60)], fill=GOLD, width=2)
        d.text((mx, cy-90), "equal", fill=GOLD, font=font(22), anchor="mm")

    panel(d, 60, 590, 960, 760)
    d.text((512, 640), "Place 1/3 and 2/3 on the number line.", fill=WHITE, font=font(30), anchor="mm")
    d.text((512, 690), "What do you notice about the gaps?", fill=CYAN, font=font(36, True), anchor="mm")
    d.text((512, 740), "Are they equal, or different?", fill=GREY, font=font(26), anchor="mm")

    save(img, "q4-issue004.png")


# ══════════════════════════════════════════════════════════════════════════════
# Q6 — 5/4 as a mixed number — show fraction, no answer
# ══════════════════════════════════════════════════════════════════════════════
def make_q6():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    d.text((W//2, 80), "Convert to a Mixed Number", fill=GOLD, font=font(44, True), anchor="mm")

    # Large 5/4 display
    panel(d, 300, 160, 720, 440)
    d.text((512, 250), "5", fill=PURPLE, font=font(130, True), anchor="mm")
    d.line([(340, 305), (680, 305)], fill=WHITE, width=5)
    d.text((512, 400), "4", fill=PURPLE, font=font(130, True), anchor="mm")

    # Arrow  =  ?
    d.text((512, 500), "=  ?  wholes  and  ?  quarters", fill=CYAN, font=font(36, True), anchor="mm")

    # 5 empty boxes representing quarters
    bx, by, bh = 100, 590, 65
    bw = (W - 200) / 5
    for i in range(5):
        x1 = bx + i * bw
        col = PURPLE if i < 4 else CYAN
        d.rounded_rectangle([x1+4, by, x1+bw-4, by+bh], radius=10, fill=(30, 10, 70), outline=col, width=3)
        d.text((x1 + bw/2, by + bh/2), "1/4", fill=col, font=font(26, True), anchor="mm")

    d.text((W//2, 700), "Each box = 1 quarter", fill=GREY, font=font(28), anchor="mm")
    d.text((W//2, 760), "How many whole groups of 4 fit in 5?", fill=WHITE, font=font(30), anchor="mm")
    d.text((W//2, 820), "What is left over?", fill=GREY, font=font(28), anchor="mm")

    save(img, "q6-issue004.png")


# ══════════════════════════════════════════════════════════════════════════════
# Q7 — Number line 0→2, place 4 fractions (no answer labels on the dots)
# ══════════════════════════════════════════════════════════════════════════════
def make_q7():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    d.text((W//2, 70), "Order from Smallest to Largest", fill=GOLD, font=font(40, True), anchor="mm")
    d.text((W//2, 125), "½  ·  ¾  ·  5/4  ·  7/4", fill=CYAN, font=font(46, True), anchor="mm")

    lx, rx, cy = 60, 940, 360
    d.line([(lx, cy), (rx, cy)], fill=CYAN, width=5)
    d.polygon([(rx, cy), (rx-14, cy-7), (rx-14, cy+7)], fill=CYAN)

    # Major ticks: 0, 1, 2
    for fv, lbl in [(0, "0"), (1, "1"), (2, "2")]:
        px = lx + (fv/2) * (rx - lx)
        d.line([(px, cy-28), (px, cy+28)], fill=WHITE, width=4)
        d.text((px, cy+38), lbl, fill=WHITE, font=font(32, True), anchor="mt")

    # Quarter ticks (unlabelled, faint)
    for i in range(9):
        fv = i / 8
        px = lx + fv * (rx - lx)
        is_major = (i % 4 == 0)
        if not is_major:
            d.line([(px, cy-10), (px, cy+10)], fill=GREY, width=2)

    # The 4 fractions as question-mark dots
    fracs = [(0.5, "½", PURPLE), (0.75, "¾", PURPLE), (1.25, "5/4", CYAN), (1.75, "7/4", CYAN)]
    for fv, lbl, col in fracs:
        px = lx + (fv/2) * (rx - lx)
        for sp in [14, 8]:
            d.ellipse([px-sp, cy-sp, px+sp, cy+sp], fill=(*col, 60))
        d.ellipse([px-8, cy-8, px+8, cy+8], fill=col)

    panel(d, 60, 580, 960, 750)
    d.text((512, 625), "These 4 fractions need to be ordered smallest → largest.", fill=WHITE, font=font(28), anchor="mm")
    d.text((512, 675), "Which are less than 1?  Which are greater than 1?", fill=CYAN, font=font(32, True), anchor="mm")
    d.text((512, 725), "Place them on the number line above.", fill=GREY, font=font(26), anchor="mm")

    save(img, "q7-issue004.png")


# ══════════════════════════════════════════════════════════════════════════════
# Q8 — Number line 0→2, count in steps of ¼ (steps shown, no "8 steps" label)
# ══════════════════════════════════════════════════════════════════════════════
def make_q8():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    d.text((W//2, 70), "Count in steps of ¼", fill=GOLD, font=font(44, True), anchor="mm")
    d.text((W//2, 125), "from 0 to 2", fill=CYAN, font=font(38, True), anchor="mm")

    lx, rx, cy = 60, 940, 340
    d.line([(lx, cy), (rx, cy)], fill=CYAN, width=5)
    d.polygon([(rx, cy), (rx-14, cy-7), (rx-14, cy+7)], fill=CYAN)

    # All 9 marks (0 through 8/4)
    lbls = ["0", "1/4", "2/4", "3/4", "4/4", "5/4", "6/4", "7/4", "8/4"]
    cols = [WHITE, PURPLE, PURPLE, PURPLE, GOLD, CYAN, CYAN, CYAN, GOLD]
    for i in range(9):
        px = lx + (i/8) * (rx - lx)
        col = cols[i]
        h = 28 if col in [GOLD, WHITE] else 22
        d.line([(px, cy-h), (px, cy+h)], fill=col, width=4)
        d.ellipse([px-7, cy-7, px+7, cy+7], fill=col)
        w = d.textlength(lbls[i], font=font(24, True))
        d.text((px - w/2, cy + 38), lbls[i], fill=col, font=font(24, True))

    # Step arrows between each pair
    for i in range(8):
        x1 = lx + (i/8) * (rx - lx) + 10
        x2 = lx + ((i+1)/8) * (rx - lx) - 10
        my = cy - 55
        d.line([(x1, my), (x2, my)], fill=GOLD, width=2)
        d.polygon([(x2, my), (x2-8, my-4), (x2-8, my+4)], fill=GOLD)

    panel(d, 60, 590, 960, 760)
    d.text((512, 640), "Each arrow = one step of ¼.", fill=WHITE, font=font(30), anchor="mm")
    d.text((512, 690), "How many steps from 0 to 2?", fill=CYAN, font=font(36, True), anchor="mm")
    d.text((512, 740), "(Don't count the starting 0!)", fill=GREY, font=font(26), anchor="mm")

    save(img, "q8-issue004.png")


# ══════════════════════════════════════════════════════════════════════════════
# Q9 — Number line 0→2 with gap between ¾ and 5/4 (question mark in gap)
# ══════════════════════════════════════════════════════════════════════════════
def make_q9():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    d.text((W//2, 70), "Find the Missing Marker", fill=GOLD, font=font(44, True), anchor="mm")

    lx, rx, cy = 60, 940, 360
    d.line([(lx, cy), (rx, cy)], fill=CYAN, width=5)
    d.polygon([(rx, cy), (rx-14, cy-7), (rx-14, cy+7)], fill=CYAN)

    marks = [
        (0, "0", WHITE), (0.25, "¼", GREY), (0.5, "½", GREY),
        (0.75, "¾", GREEN), (1.0, "?", RED), (1.25, "5/4", GREEN),
        (1.5, "6/4", GREY), (1.75, "7/4", GREY), (2.0, "2", WHITE)
    ]
    for fv, lbl, col in marks:
        px = lx + (fv/2) * (rx - lx)
        lw = 4 if lbl == "?" else 3
        h = 30 if lbl in ["¾", "?", "5/4"] else 16
        d.line([(px, cy-h), (px, cy+h)], fill=col, width=lw)
        w = d.textlength(lbl, font=font(30, True))
        d.text((px - w/2, cy + 38), lbl, fill=col, font=font(30, True))

    # Highlight the gap
    gap_px = lx + (1.0/2) * (rx - lx)
    d.rounded_rectangle([gap_px-30, cy-38, gap_px+30, cy+38], radius=10,
                         fill=(255, 80, 80, 50), outline=RED, width=3)

    # Phantom note
    panel(d, 60, 570, 960, 720)
    d.text((512, 615), "The Phantom removed this marker and wrote:", fill=GREY, font=font(26), anchor="mm")
    d.text((512, 665), '"This is not a fraction — it is a whole number."', fill=RED, font=font(30, True), anchor="mm")
    d.text((512, 715), "What fraction is missing — and is the Phantom right?", fill=CYAN, font=font(28, True), anchor="mm")

    save(img, "q9-issue004.png")


# ══════════════════════════════════════════════════════════════════════════════
# Q10 — 4/4 = 1, number line with gap, Phantom's claim (no answer shown)
# ══════════════════════════════════════════════════════════════════════════════
def make_q10():
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    d.text((W//2, 70), "Boss Challenge — The Missing Marker", fill=PINK, font=font(38, True), anchor="mm")

    lx, rx, cy = 60, 940, 310
    d.line([(lx, cy), (rx, cy)], fill=CYAN, width=5)
    d.polygon([(rx, cy), (rx-14, cy-7), (rx-14, cy+7)], fill=CYAN)

    marks = [
        (0, "0", WHITE), (0.25, "¼", GREY), (0.5, "½", GREY),
        (0.75, "¾", GREEN), (1.0, "?", RED), (1.25, "5/4", GREEN),
        (1.5, "6/4", GREY), (1.75, "7/4", GREY), (2.0, "2", WHITE)
    ]
    for fv, lbl, col in marks:
        px = lx + (fv/2) * (rx - lx)
        h = 28 if lbl in ["¾", "?", "5/4"] else 16
        d.line([(px, cy-h), (px, cy+h)], fill=col, width=(4 if lbl == "?" else 3))
        w = d.textlength(lbl, font=font(28, True))
        d.text((px - w/2, cy+34), lbl, fill=col, font=font(28, True))

    gap_px = lx + (1.0/2) * (rx - lx)
    d.rounded_rectangle([gap_px-28, cy-34, gap_px+28, cy+34], radius=10,
                         fill=(255, 80, 80, 50), outline=RED, width=3)
    d.text((gap_px, cy-60), "REMOVED!", fill=RED, font=font(22, True), anchor="mm")

    # Phantom note box
    panel(d, 50, 440, 970, 600)
    d.text((512, 488), "Phantom's note:", fill=GREY, font=font(24), anchor="mm")
    d.text((512, 540), '"4/4 is not a fraction. It is a whole number."', fill=RED, font=font(28, True), anchor="mm")

    # Question box
    panel(d, 50, 630, 970, 790)
    d.text((512, 680), "What fraction did the Phantom remove?", fill=WHITE, font=font(30, True), anchor="mm")
    d.text((512, 730), "What does it equal as a whole number?", fill=CYAN, font=font(30, True), anchor="mm")
    d.text((512, 775), "And is the Phantom's argument correct?", fill=GOLD, font=font(28, True), anchor="mm")

    save(img, "q10-issue004.png")


if __name__ == "__main__":
    print("Generating Issue 4 images (v2)...")
    make_q1()
    make_q2()
    make_q3()
    make_q4()
    make_q6()
    make_q7()
    make_q8()
    make_q9()
    make_q10()
    print("\nAll done!")
