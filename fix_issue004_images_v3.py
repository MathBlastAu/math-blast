#!/usr/bin/env python3
"""Issue 4 images v3 — BIG number lines, no question text, clean and readable."""

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
DARK   = (20, 10, 60)

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

def stars(draw, w, h, n=60):
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

def label(draw, px, cy, txt, col, offset=50, sz=56, bold=True):
    f = fnt(sz, bold)
    w = draw.textlength(txt, font=f)
    draw.text((px - w/2, cy + offset), txt, fill=col, font=f)

def dot(draw, px, cy, col, r=12):
    for sp in [r+8, r+4]:
        draw.ellipse([px-sp, cy-sp, px+sp, cy+sp], fill=(*col, 50))
    draw.ellipse([px-r, cy-r, px+r, cy+r], fill=col)

def save(img, name):
    img.convert("RGB").save(f"{OUT}/{name}")
    print(f"  ✅ {name}")


# ── Q1: Number line 0→1, ½ shown in wrong place (at ¾), ? at correct position ──
def make_q1():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H, 40)

    lx, rx, cy = 60, 940, 280

    line_base(d, lx, rx, cy)

    # 0 and 1
    for fv, lbl in [(0, "0"), (1.0, "1")]:
        px = lx + fv * (rx - lx)
        tick(d, px, cy, 36, WHITE, 6)
        label(d, px, cy, lbl, WHITE, 50, 64, True)

    # ¼ and ¾ faint reference ticks
    for fv, lbl in [(0.25, "¼"), (0.75, "¾")]:
        px = lx + fv * (rx - lx)
        tick(d, px, cy, 18, GREY, 3)
        label(d, px, cy, lbl, GREY, 50, 44, False)

    # ½ placed at ¾ — shown in RED with X
    wrong_px = lx + 0.75 * (rx - lx)
    tick(d, wrong_px, cy, 44, RED, 6)
    label(d, wrong_px, cy, "½ ✗", RED, -100, 64, True)

    # Correct position — ? marker at 0.5
    correct_px = lx + 0.5 * (rx - lx)
    tick(d, correct_px, cy, 36, GOLD, 5)
    dot(d, correct_px, cy, GOLD, 14)
    label(d, correct_px, cy, "?", GOLD, 50, 72, True)

    save(img, "q1-issue004.png")


# ── Q2: Number line 0→1, 4 equal sections, ? at ¼ ──
def make_q2():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H, 40)

    lx, rx, cy = 60, 940, 280
    line_base(d, lx, rx, cy)

    seg = (rx - lx) / 4
    lbls = ["0", "?", "½", "¾", "1"]
    cols = [WHITE, GOLD, GREY, GREY, WHITE]
    for i in range(5):
        px = lx + i * seg
        col = cols[i]
        h = 40 if i == 1 else 28
        lw = 6 if i in [0, 4] else (6 if i == 1 else 4)
        tick(d, px, cy, h, col, lw)
        label(d, px, cy, lbls[i], col, 50, 64 if i == 1 else 52, True)

    # Big glowing dot at ¼
    qpx = lx + seg
    dot(d, qpx, cy, GOLD, 16)

    save(img, "q2-issue004.png")


# ── Q3: Number line 0→1, 2/3 and 3/4 placed close — which is bigger? ──
def make_q3():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H, 40)

    lx, rx, cy = 60, 940, 280
    line_base(d, lx, rx, cy)

    for fv, lbl in [(0, "0"), (1.0, "1")]:
        px = lx + fv * (rx - lx)
        tick(d, px, cy, 36, WHITE, 6)
        label(d, px, cy, lbl, WHITE, 50, 64, True)

    # 2/3 and 3/4
    for fv, lbl, col in [(2/3, "2/3", PURPLE), (0.75, "3/4", CYAN)]:
        px = lx + fv * (rx - lx)
        tick(d, px, cy, 44, col, 6)
        dot(d, px, cy, col, 14)
        # Label above the line
        f = fnt(64, True)
        w = d.textlength(lbl, font=f)
        d.text((px - w/2, cy - 110), lbl, fill=col, font=f)

    # Double-headed arrow between them showing "close"
    px1 = lx + (2/3) * (rx - lx)
    px2 = lx + 0.75 * (rx - lx)
    mid = (px1 + px2) // 2
    ay = cy + 80
    d.line([(px1+4, ay), (px2-4, ay)], fill=GOLD, width=4)
    d.polygon([(px1+4, ay), (px1+18, ay-7), (px1+18, ay+7)], fill=GOLD)
    d.polygon([(px2-4, ay), (px2-18, ay-7), (px2-18, ay+7)], fill=GOLD)

    save(img, "q3-issue004.png")


# ── Q4: Number line 0→1, 1/3 and 2/3 marked, equal-gap brackets ──
def make_q4():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H, 40)

    lx, rx, cy = 60, 940, 300
    line_base(d, lx, rx, cy)

    for fv, lbl, col in [(0, "0", WHITE), (1/3, "1/3", PURPLE), (2/3, "2/3", CYAN), (1.0, "1", WHITE)]:
        px = lx + fv * (rx - lx)
        h = 44 if fv in [1/3, 2/3] else 32
        tick(d, px, cy, h, col, 6)
        label(d, px, cy, lbl, col, 52, 64, True)
        if fv in [1/3, 2/3]:
            dot(d, px, cy, col, 14)

    # Equal-gap brackets above
    gap = (rx - lx) / 3
    by = cy - 80
    f = fnt(36, True)
    for i in range(3):
        x1 = lx + i * gap
        x2 = x1 + gap
        mx = (x1 + x2) / 2
        d.line([(x1+6, by), (x2-6, by)], fill=GOLD, width=3)
        d.line([(x1+6, by), (x1+6, by+12)], fill=GOLD, width=3)
        d.line([(x2-6, by), (x2-6, by+12)], fill=GOLD, width=3)
        w = d.textlength("equal", font=f)
        d.text((mx - w/2, by - 42), "equal", fill=GOLD, font=f)

    save(img, "q4-issue004.png")


# ── Q6: 5 boxes representing quarters — no answer shown ──
def make_q6():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H, 40)

    # Large fraction display
    f_big = fnt(200, True)
    # Draw 5/4
    d.text((512, 200), "5", fill=PURPLE, font=f_big, anchor="mm")
    d.line([(220, 260), (800, 260)], fill=WHITE, width=8)
    d.text((512, 400), "4", fill=PURPLE, font=f_big, anchor="mm")

    # 5 boxes at bottom
    bw, bh = 160, 90
    gap = 12
    total = 5 * bw + 4 * gap
    sx = (W - total) // 2
    by = 500
    f_box = fnt(40, True)
    for i in range(5):
        x1 = sx + i * (bw + gap)
        col = PURPLE if i < 4 else CYAN
        d.rounded_rectangle([x1, by, x1+bw, by+bh], radius=12, fill=(20, 10, 60), outline=col, width=4)
        w = d.textlength("¼", font=f_box)
        d.text((x1 + bw/2 - w/2, by + bh/2 - 22), "¼", fill=col, font=f_box)

    save(img, "q6-issue004.png")


# ── Q7: Number line 0→2, 4 fractions as coloured dots (no fraction labels on line) ──
def make_q7():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H, 40)

    lx, rx, cy = 40, 980, 260
    line_base(d, lx, rx, cy)

    # 0, 1, 2 major ticks
    for fv, lbl in [(0, "0"), (1, "1"), (2, "2")]:
        px = lx + (fv/2) * (rx - lx)
        tick(d, px, cy, 40, WHITE, 6)
        label(d, px, cy, lbl, WHITE, 52, 68, True)

    # Minor quarter ticks (faint)
    for i in range(1, 8):
        if i % 4 != 0:
            px = lx + (i/8) * (rx - lx)
            tick(d, px, cy, 14, GREY, 2)

    # 4 fraction dots — just coloured, labelled ABOVE line
    fracs = [(0.5, "½", PURPLE), (0.75, "¾", PURPLE), (1.25, "5/4", CYAN), (1.75, "7/4", CYAN)]
    for fv, lbl, col in fracs:
        px = lx + (fv/2) * (rx - lx)
        dot(d, px, cy, col, 18)
        f = fnt(52, True)
        w = d.textlength(lbl, font=f)
        d.text((px - w/2, cy - 90), lbl, fill=col, font=f)

    save(img, "q7-issue004.png")


# ── Q8: Number line 0→2, ALL quarter steps with step numbers ──
def make_q8():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H, 40)

    lx, rx, cy = 40, 980, 300
    line_base(d, lx, rx, cy)

    # 0 and 2 anchors
    for fv, lbl in [(0, "0"), (2, "2")]:
        px = lx + (fv/2) * (rx - lx)
        tick(d, px, cy, 40, WHITE, 6)
        label(d, px, cy, lbl, WHITE, 52, 64, True)

    # 1 midpoint
    px1 = lx + 0.5 * (rx - lx)
    tick(d, px1, cy, 36, GOLD, 5)
    label(d, px1, cy, "1", GOLD, 52, 64, True)

    # All 9 quarter marks
    lbls   = ["0", "¼", "½", "¾", "1", "5/4", "6/4", "7/4", "2"]
    cols   = [WHITE, PURPLE, PURPLE, PURPLE, GOLD, CYAN, CYAN, CYAN, WHITE]
    for i in range(9):
        px = lx + (i/8) * (rx - lx)
        col = cols[i]
        h = 36 if col in [GOLD, WHITE] else 28
        tick(d, px, cy, h, col, 5)
        dot(d, px, cy, col, 9)
        f = fnt(36, True)
        w = d.textlength(lbls[i], font=f)
        d.text((px - w/2, cy + 44), lbls[i], fill=col, font=f)

    # Step arrows above
    f_step = fnt(28, True)
    for i in range(8):
        x1 = lx + (i/8) * (rx - lx) + 8
        x2 = lx + ((i+1)/8) * (rx - lx) - 8
        ay = cy - 55
        d.line([(x1, ay), (x2, ay)], fill=GOLD, width=3)
        d.polygon([(x2, ay), (x2-10, ay-5), (x2-10, ay+5)], fill=GOLD)
        mx = (x1 + x2) / 2
        w = d.textlength(str(i+1), font=f_step)
        d.text((mx - w/2, ay - 36), str(i+1), fill=GOLD, font=f_step)

    save(img, "q8-issue004.png")


# ── Q9: Number line 0→2, gap between ¾ and 5/4 with ? ──
def make_q9():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H, 40)

    lx, rx, cy = 40, 980, 280
    line_base(d, lx, rx, cy)

    for fv, lbl in [(0, "0"), (1, "1"), (2, "2")]:
        px = lx + (fv/2) * (rx - lx)
        tick(d, px, cy, 36, WHITE, 6)
        label(d, px, cy, lbl, WHITE, 50, 64, True)

    marks = [
        (0.25, "¼", GREY), (0.5, "½", GREY),
        (0.75, "¾", GREEN), (1.25, "5/4", GREEN),
        (1.5, "6/4", GREY), (1.75, "7/4", GREY),
    ]
    for fv, lbl, col in marks:
        px = lx + (fv/2) * (rx - lx)
        h = 38 if col == GREEN else 22
        lw = 5 if col == GREEN else 3
        tick(d, px, cy, h, col, lw)
        if col == GREEN:
            dot(d, px, cy, col, 12)
        f = fnt(44 if col == GREEN else 34, True)
        w = d.textlength(lbl, font=f)
        d.text((px - w/2, cy + 46), lbl, fill=col, font=f)

    # Gap at 1.0 — highlighted in red
    gap_px = lx + (1.0/2) * (rx - lx)
    d.rounded_rectangle([gap_px-32, cy-42, gap_px+32, cy+42], radius=12,
                         fill=(255, 80, 80, 60), outline=RED, width=4)
    f_q = fnt(72, True)
    w = d.textlength("?", font=f_q)
    d.text((gap_px - w/2, cy - 36), "?", fill=RED, font=f_q)

    save(img, "q9-issue004.png")


# ── Q10: Number line 0→2 with gap — boss challenge ──
def make_q10():
    W, H = 1024, 640
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, W, H, 40)

    lx, rx, cy = 40, 980, 240
    line_base(d, lx, rx, cy)

    for fv, lbl in [(0, "0"), (1, "1"), (2, "2")]:
        px = lx + (fv/2) * (rx - lx)
        tick(d, px, cy, 36, WHITE, 6)
        label(d, px, cy, lbl, WHITE, 48, 64, True)

    marks = [
        (0.25, "¼", GREY), (0.5, "½", GREY),
        (0.75, "¾", GREEN), (1.25, "5/4", GREEN),
        (1.5, "6/4", GREY), (1.75, "7/4", GREY),
    ]
    for fv, lbl, col in marks:
        px = lx + (fv/2) * (rx - lx)
        h = 38 if col == GREEN else 22
        lw = 5 if col == GREEN else 3
        tick(d, px, cy, h, col, lw)
        if col == GREEN:
            dot(d, px, cy, col, 12)
        f = fnt(44 if col == GREEN else 34, True)
        w = d.textlength(lbl, font=f)
        d.text((px - w/2, cy + 46), lbl, fill=col, font=f)

    # Removed marker
    gap_px = lx + (1.0/2) * (rx - lx)
    d.rounded_rectangle([gap_px-32, cy-42, gap_px+32, cy+42], radius=12,
                         fill=(255, 80, 80, 60), outline=RED, width=4)
    f_q = fnt(72, True)
    w = d.textlength("?", font=f_q)
    d.text((gap_px - w/2, cy - 36), "?", fill=RED, font=f_q)

    # Phantom's message below
    f_msg = fnt(36, True)
    msg = '"4/4 is a whole number, not a fraction."'
    w = d.textlength(msg, font=f_msg)
    d.text(((W - w)//2, cy + 160), msg, fill=(170, 100, 255), font=f_msg)

    save(img, "q10-issue004.png")


if __name__ == "__main__":
    print("Generating Issue 4 images v3 (big lines, no question text)...")
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
