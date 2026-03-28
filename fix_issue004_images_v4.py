#!/usr/bin/env python3
"""Fix 3 specific images: Q7 (strip fraction labels), Q8 (strip step numbers), Q10 (strip Phantom text)."""

from PIL import Image, ImageDraw, ImageFont
import os, random

OUT = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"

BG     = (13, 6, 48)
PURPLE = (160, 60, 255)
CYAN   = (0, 200, 255)
GOLD   = (255, 185, 0)
GREEN  = (0, 220, 100)
RED    = (255, 80, 80)
WHITE  = (255, 255, 255)
GREY   = (80, 70, 120)

def fnt(size, bold=False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def stars(draw, w, h, n=40):
    random.seed(7)
    for _ in range(n):
        x, y = random.randint(0, w), random.randint(0, h)
        r = random.choice([1, 1, 2])
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, random.randint(60, 180)))

def line_base(draw, lx, rx, cy, width=8):
    draw.line([(lx, cy), (rx, cy)], fill=CYAN, width=width)
    draw.polygon([(rx, cy), (rx-18, cy-9), (rx-18, cy+9)], fill=CYAN)

def tick(draw, px, cy, h=30, col=WHITE, lw=5):
    draw.line([(px, cy-h), (px, cy+h)], fill=col, width=lw)

def dot(draw, px, cy, col, r=12):
    for sp in [r+8, r+4]:
        draw.ellipse([px-sp, cy-sp, px+sp, cy+sp], fill=(*col, 50))
    draw.ellipse([px-r, cy-r, px+r, cy+r], fill=col)

def save(img, name):
    img.convert("RGB").save(f"{OUT}/{name}")
    print(f"  ✅ {name}")


# ── Q7: Number line 0→2, 4 coloured dots — NO fraction labels, just coloured bubbles ──
def make_q7():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    lx, rx, cy = 40, 980, 320
    line_base(d, lx, rx, cy)

    # 0, 1, 2 only
    for fv, lbl in [(0, "0"), (1, "1"), (2, "2")]:
        px = lx + (fv/2) * (rx - lx)
        tick(d, px, cy, 40, WHITE, 6)
        f = fnt(72, True)
        w = d.textlength(lbl, font=f)
        d.text((px - w/2, cy + 52), lbl, fill=WHITE, font=f)

    # Minor quarter ticks (faint, no labels)
    for i in range(1, 8):
        if i % 4 != 0:
            px = lx + (i/8) * (rx - lx)
            tick(d, px, cy, 14, GREY, 2)

    # 4 coloured bubbles — NO labels
    fracs = [(0.5, PURPLE), (0.75, PURPLE), (1.25, CYAN), (1.75, CYAN)]
    for fv, col in fracs:
        px = lx + (fv/2) * (rx - lx)
        dot(d, px, cy, col, 22)

    save(img, "q7-issue004.png")


# ── Q8: Number line 0→2, all quarter steps — NO step numbers, NO small fraction labels ──
def make_q8():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    lx, rx, cy = 40, 980, 310
    line_base(d, lx, rx, cy)

    # Only 0, 1, 2 labelled (big, clear)
    for fv, lbl, col in [(0, "0", WHITE), (1.0, "1", GOLD), (2.0, "2", WHITE)]:
        px = lx + (fv/2) * (rx - lx)
        tick(d, px, cy, 44, col, 7)
        f = fnt(72, True)
        w = d.textlength(lbl, font=f)
        d.text((px - w/2, cy + 56), lbl, fill=col, font=f)

    # All 9 quarter marks — coloured dots, NO text labels
    cols = [WHITE, PURPLE, PURPLE, PURPLE, GOLD, CYAN, CYAN, CYAN, WHITE]
    for i in range(9):
        px = lx + (i/8) * (rx - lx)
        col = cols[i]
        h = 38 if col in [GOLD, WHITE] else 26
        tick(d, px, cy, h, col, 5)
        dot(d, px, cy, col, 10)

    # Step arrows above — just arrows, no numbers
    for i in range(8):
        x1 = lx + (i/8) * (rx - lx) + 10
        x2 = lx + ((i+1)/8) * (rx - lx) - 10
        ay = cy - 60
        d.line([(x1, ay), (x2, ay)], fill=GOLD, width=3)
        d.polygon([(x2, ay), (x2-10, ay-5), (x2-10, ay+5)], fill=GOLD)

    save(img, "q8-issue004.png")


# ── Q10: Number line 0→2 with gap — NO Phantom text, just the visual gap ──
def make_q10():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H)

    lx, rx, cy = 40, 980, 280
    line_base(d, lx, rx, cy)

    for fv, lbl, col in [(0, "0", WHITE), (1, "1", GOLD), (2, "2", WHITE)]:
        px = lx + (fv/2) * (rx - lx)
        tick(d, px, cy, 40, col, 6)
        f = fnt(64, True)
        w = d.textlength(lbl, font=f)
        d.text((px - w/2, cy + 50), lbl, fill=col, font=f)

    marks = [
        (0.25, "¼", GREY), (0.5, "½", GREY),
        (0.75, "¾", GREEN), (1.25, "5/4", GREEN),
        (1.5, "6/4", GREY), (1.75, "7/4", GREY),
    ]
    for fv, lbl, col in marks:
        px = lx + (fv/2) * (rx - lx)
        h = 40 if col == GREEN else 22
        lw = 5 if col == GREEN else 3
        tick(d, px, cy, h, col, lw)
        if col == GREEN:
            dot(d, px, cy, col, 12)
        f = fnt(44 if col == GREEN else 34, True)
        w = d.textlength(lbl, font=f)
        d.text((px - w/2, cy + 48), lbl, fill=col, font=f)

    # The removed marker — red box with ?
    gap_px = lx + (1.0/2) * (rx - lx)
    d.rounded_rectangle([gap_px-34, cy-44, gap_px+34, cy+44], radius=12,
                         fill=(255, 80, 80, 60), outline=RED, width=5)
    f_q = fnt(80, True)
    w = d.textlength("?", font=f_q)
    d.text((gap_px - w/2, cy - 40), "?", fill=RED, font=f_q)

    save(img, "q10-issue004.png")


if __name__ == "__main__":
    print("Fixing Q7, Q8, Q10 images...")
    make_q7()
    make_q8()
    make_q10()
    print("Done!")
