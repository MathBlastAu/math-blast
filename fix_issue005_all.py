#!/usr/bin/env python3
"""Fix Issue 5: Pillow images for Q1,Q3,Q7,Q8,Q9,Q10 + HTML fixes (JS bug, Q7/Q8 questions, Q4 story)."""

from PIL import Image, ImageDraw, ImageFont
import os, random, re

BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast"
OUT  = os.path.join(BASE, "images")

BG     = (13, 6, 48)
PURPLE = (160, 60, 255)
CYAN   = (0, 200, 255)
GOLD   = (255, 185, 0)
GREEN  = (0, 220, 100)
RED    = (255, 80, 80)
WHITE  = (255, 255, 255)
GREY   = (80, 70, 120)
ORANGE = (255, 140, 0)

def fnt(size, bold=False):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
              else "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def stars(draw, w, h, n=50):
    random.seed(13)
    for _ in range(n):
        x, y = random.randint(0,w), random.randint(0,h)
        r = random.choice([1,1,2])
        draw.ellipse([x-r,y-r,x+r,y+r], fill=(255,255,255,random.randint(60,180)))

def tick(d, px, cy, h=28, col=WHITE, lw=5):
    d.line([(px,cy-h),(px,cy+h)], fill=col, width=lw)

def dot(d, px, cy, col, r=12):
    for sp in [r+8,r+4]: d.ellipse([px-sp,cy-sp,px+sp,cy+sp], fill=(*col,50))
    d.ellipse([px-r,cy-r,px+r,cy+r], fill=col)

def line_base(d, lx, rx, cy, w=8):
    d.line([(lx,cy),(rx,cy)], fill=CYAN, width=w)
    d.polygon([(rx,cy),(rx-18,cy-9),(rx-18,cy+9)], fill=CYAN)

def lbl(d, px, cy, txt, col, off=50, sz=56, bold=True):
    f = fnt(sz, bold)
    w = d.textlength(txt, font=f)
    d.text((px-w/2, cy+off), txt, fill=col, font=f)

def save(img, name):
    img.convert("RGB").save(f"{OUT}/{name}")
    print(f"  ✅ {name}")

def new_img(w=1024, h=640):
    img = Image.new("RGBA", (w,h), BG)
    d = ImageDraw.Draw(img, "RGBA")
    stars(d, w, h)
    return img, d


# ── Q1: Prize wheel — 8 sections, 3 highlighted, is it > or < ½? ──────────────
def make_q1():
    import math
    W, H = 1024, 640
    img, d = new_img(W, H)

    cx, cy, r = 320, 300, 220
    n = 8
    for i in range(n):
        start = 360/n * i - 90
        end   = start + 360/n
        col = PURPLE if i < 3 else (30, 15, 60)
        # draw slice
        d.pieslice([cx-r, cy-r, cx+r, cy+r], start=start, end=end, fill=col, outline=CYAN, width=3)

    # Section labels
    for i in range(n):
        angle = math.radians(360/n * i - 90 + 360/n/2)
        tx = cx + int((r*0.65) * math.cos(angle))
        ty = cy + int((r*0.65) * math.sin(angle))
        col = WHITE if i < 3 else GREY
        f = fnt(36, True)
        w = d.textlength(str(i+1), font=f)
        d.text((tx-w/2, ty-18), str(i+1), fill=col, font=f)

    # Centre dot
    d.ellipse([cx-15,cy-15,cx+15,cy+15], fill=WHITE)

    # Right side: fraction display
    # 3/8
    d.text((700, 160), "3", fill=PURPLE, font=fnt(160, True), anchor="mm")
    d.line([(580, 240), (820, 240)], fill=WHITE, width=6)
    d.text((700, 340), "8", fill=PURPLE, font=fnt(160, True), anchor="mm")

    # Half marker
    d.text((700, 460), "vs  ½", fill=GOLD, font=fnt(60, True), anchor="mm")
    d.text((700, 530), "more or less?", fill=GREY, font=fnt(36), anchor="mm")

    save(img, "q1-issue005.png")


# ── Q3: Fuel gauge showing Jake's fuel + 1/4+1/2 addition ─────────────────────
def make_q3():
    W, H = 1024, 640
    img, d = new_img(W, H)

    # Left: Jake's fuel gauge (2/8 remaining)
    gx, gy, gw, gh = 80, 120, 180, 380
    d.rounded_rectangle([gx,gy,gx+gw,gy+gh], radius=12, outline=CYAN, width=4, fill=(20,10,50))
    # 8 segments
    seg = gh//8
    for i in range(8):
        y1 = gy + gh - (i+1)*seg
        y2 = gy + gh - i*seg
        col = CYAN if i < 2 else (30,15,60)
        d.rounded_rectangle([gx+6,y1+2,gx+gw-6,y2-2], radius=4, fill=col)
    f = fnt(32, True)
    w = d.textlength("2/8", font=f)
    d.text((gx+gw/2-w/2, gy+gh+12), "2/8", fill=CYAN, font=f)
    d.text((gx+gw/2, gy-30), "Jake", fill=GREY, font=fnt(28), anchor="mm")

    # Centre: addition
    d.text((390, 220), "1/4", fill=PURPLE, font=fnt(90, True), anchor="mm")
    d.text((390, 320), "+", fill=WHITE, font=fnt(70, True), anchor="mm")
    d.text((390, 420), "1/2", fill=GOLD, font=fnt(90, True), anchor="mm")
    d.text((390, 510), "= ?", fill=GREEN, font=fnt(70, True), anchor="mm")

    # Right: Ship Beta gauge (7/8 needed)
    gx2 = 680
    d.rounded_rectangle([gx2,gy,gx2+gw,gy+gh], radius=12, outline=RED, width=4, fill=(20,10,50))
    for i in range(8):
        y1 = gy + gh - (i+1)*seg
        y2 = gy + gh - i*seg
        col = RED if i < 7 else (30,15,60)
        d.rounded_rectangle([gx2+6,y1+2,gx2+gw-6,y2-2], radius=4, fill=col)
    w = d.textlength("7/8", font=f)
    d.text((gx2+gw/2-w/2, gy+gh+12), "7/8", fill=RED, font=f)
    d.text((gx2+gw/2, gy-30), "Beta needs", fill=GREY, font=fnt(28), anchor="mm")

    save(img, "q3-issue005.png")


# ── Q7: Number line 0→1 with eighths, which bigger: 5/6 or 7/8? ───────────────
def make_q7():
    W, H = 1024, 640
    img, d = new_img(W, H)

    lx, rx, cy = 60, 940, 310
    line_base(d, lx, rx, cy)

    # 0 and 1
    for fv, lb in [(0,"0"),(1,"1")]:
        px = lx + fv*(rx-lx)
        tick(d, px, cy, 36, WHITE, 6)
        lbl(d, px, cy, lb, WHITE, 48, 64, True)

    # 8ths ticks (faint)
    for i in range(1,8):
        px = lx + (i/8)*(rx-lx)
        tick(d, px, cy, 14, GREY, 2)

    # 5/6 ≈ 0.833 and 7/8 = 0.875 — show as coloured dots with labels above
    for fv, lb, col in [(5/6,"5/6",PURPLE),(7/8,"7/8",CYAN)]:
        px = lx + fv*(rx-lx)
        tick(d, px, cy, 44, col, 6)
        dot(d, px, cy, col, 16)
        f = fnt(64, True)
        w = d.textlength(lb, font=f)
        d.text((px-w/2, cy-110), lb, fill=col, font=f)

    # Arrow between them
    px1 = lx + (5/6)*(rx-lx)
    px2 = lx + (7/8)*(rx-lx)
    ay = cy + 80
    d.line([(px1+4,ay),(px2-4,ay)], fill=GOLD, width=4)
    d.polygon([(px2-4,ay),(px2-18,ay-7),(px2-18,ay+7)], fill=GOLD)

    save(img, "q7-issue005.png")


# ── Q8: Show 3/8 + 2/8 = 5/8, gap to 8/8 ─────────────────────────────────────
def make_q8():
    W, H = 1024, 640
    img, d = new_img(W, H)

    lx, rx, cy = 60, 940, 300
    line_base(d, lx, rx, cy)

    # 0 and 1
    for fv, lb in [(0,"0"),(1,"1")]:
        px = lx + fv*(rx-lx)
        tick(d, px, cy, 36, WHITE, 6)
        lbl(d, px, cy, lb, WHITE, 48, 64, True)

    # 8 equal segments
    seg = (rx-lx)/8
    for i in range(9):
        px = lx + i*seg
        col = WHITE if i in [0,8] else GREY
        tick(d, px, cy, 14 if i not in [0,8] else 28, col, 3 if i not in [0,8] else 5)

    # 3/8 filled (purple)
    px3 = lx + (3/8)*(rx-lx)
    d.rounded_rectangle([lx+3, cy-22, px3-3, cy+22], radius=8, fill=(*PURPLE,180))
    f = fnt(44, True)
    w = d.textlength("3/8", font=f)
    d.text(((lx+px3)/2-w/2, cy-60), "3/8", fill=PURPLE, font=f)

    # +2/8 (gold)
    px5 = lx + (5/8)*(rx-lx)
    d.rounded_rectangle([px3+3, cy-22, px5-3, cy+22], radius=8, fill=(*GOLD,180))
    w = d.textlength("2/8", font=f)
    d.text(((px3+px5)/2-w/2, cy-60), "+2/8", fill=GOLD, font=f)

    # Gap to 1 (red, labelled ?)
    d.rounded_rectangle([px5+3, cy-22, lx+(rx-lx)-3, cy+22], radius=8, fill=(255,80,80,100), outline=RED, width=3)
    w = d.textlength("?", font=fnt(60,True))
    f2 = fnt(60, True)
    d.text(((px5+rx)/2-w/2, cy-40), "?", fill=RED, font=f2)

    # Total so far
    f3 = fnt(46, True)
    d.text((lx + (5/16)*(rx-lx), cy+70), "3/8 + 2/8 = 5/8", fill=WHITE, font=f3, anchor="mm")
    d.text((lx + (5/16)*(rx-lx), cy+130), "Need to reach 1 whole (8/8)", fill=GOLD, font=fnt(38), anchor="mm")

    save(img, "q8-issue005.png")


# ── Q9: Show 1/4 + 2/4 + 3/4, what is total? ─────────────────────────────────
def make_q9():
    W, H = 1024, 640
    img, d = new_img(W, H)

    # Three big fraction displays side by side
    fracs = [("1","4",PURPLE), ("2","4",GOLD), ("3","4",CYAN)]
    cx_list = [200, 512, 824]
    for (n, dn, col), cx in zip(fracs, cx_list):
        d.text((cx, 200), n, fill=col, font=fnt(180, True), anchor="mm")
        d.line([(cx-90, 270), (cx+90, 270)], fill=col, width=6)
        d.text((cx, 360), dn, fill=col, font=fnt(180, True), anchor="mm")

    # Plus signs between
    d.text((356, 280), "+", fill=WHITE, font=fnt(100, True), anchor="mm")
    d.text((668, 280), "+", fill=WHITE, font=fnt(100, True), anchor="mm")

    # = ? below
    d.text((512, 510), "= ?", fill=GREEN, font=fnt(90, True), anchor="mm")
    d.text((512, 590), "Write as a mixed number", fill=GREY, font=fnt(34), anchor="mm")

    save(img, "q9-issue005.png")


# ── Q10: Show 16/8 - 5/8 = ? ─────────────────────────────────────────────────
def make_q10():
    W, H = 1024, 640
    img, d = new_img(W, H)

    # Visual: number line 0 → 2
    lx, rx, cy = 60, 940, 240
    line_base(d, lx, rx, cy)

    for fv, lb, col in [(0,"0",WHITE),(1,"1",GOLD),(2,"2",WHITE)]:
        px = lx + (fv/2)*(rx-lx)
        tick(d, px, cy, 36, col, 6)
        lbl(d, px, cy, lb, col, 48, 64, True)

    # 8th ticks
    for i in range(1,16):
        if i%8 != 0:
            px = lx + (i/16)*(rx-lx)
            tick(d, px, cy, 12, GREY, 2)

    # 5/8 filled (existing)
    px58 = lx + (5/16)*(rx-lx)
    d.rounded_rectangle([lx+3, cy-20, px58-3, cy+20], radius=6, fill=(*PURPLE,180))
    f = fnt(42, True)
    d.text(((lx+px58)/2, cy-55), "5/8", fill=PURPLE, font=f, anchor="mm")

    # Gap to 2 (red, labelled ?)
    px2 = lx + (2/2)*(rx-lx)
    d.rounded_rectangle([px58+3, cy-20, px2-3, cy+20], radius=6, fill=(255,80,80,100), outline=RED, width=3)
    d.text(((px58+px2)/2, cy-55), "?", fill=RED, font=fnt(60,True), anchor="mm")

    # Equation
    d.text((512, 420), "5/8  +  ?  =  2", fill=WHITE, font=fnt(80, True), anchor="mm")
    d.text((512, 510), "2 wholes  =  16/8", fill=GOLD, font=fnt(50), anchor="mm")
    d.text((512, 580), "16/8  −  5/8  =  ?", fill=CYAN, font=fnt(50), anchor="mm")

    save(img, "q10-issue005.png")


# ── HTML FIXES ────────────────────────────────────────────────────────────────
def fix_html():
    path = os.path.join(BASE, "issue-005-narrated.html")
    with open(path) as f:
        html = f.read()
    original = html

    # FIX 1: playerConfigs missing unlockAtIndex
    html = html.replace(
        "playerConfigs[id] = { files, labels, storyId, lockId, onDone, active:false };",
        "playerConfigs[id] = { files, labels, storyId, lockId, onDone, unlockAtIndex: unlockAtIndex ?? files.length, active:false };"
    )
    # Also fix the runPlayer - inject unlock at index if not already there
    if 'fileIdx===cfg.unlockAtIndex' not in html and "fileIdx === cfg.unlockAtIndex" not in html:
        INJECT = (
            "if(fileIdx===cfg.unlockAtIndex){"
            "if(cfg.lockId){const lock=document.getElementById(cfg.lockId);if(lock)lock.style.display='none';}"
            "const quizId=cfg.lockId?cfg.lockId.replace('lock-','quiz-'):null;"
            "if(quizId){const quiz=document.getElementById(quizId);if(quiz&&!quiz.classList.contains('show')){"
            "quiz.classList.add('show');setTimeout(()=>quiz.scrollIntoView({behavior:'smooth',block:'nearest'}),200);}}"
            "}"
        )
        html = html.replace("const file=cfg.files[fileIdx];", INJECT + "const file=cfg.files[fileIdx];", 1)
        # Remove unlock from end-of-files block
        html = re.sub(
            r"if\(cfg\.lockId\)\{const lock=document\.getElementById\(cfg\.lockId\);if\(lock\)lock\.style\.display='none';\}"
            r"const quizId=cfg\.lockId\?cfg\.lockId\.replace\('lock-','quiz-'\):null;"
            r"if\(quizId\)\{const quiz=document\.getElementById\(quizId\);if\(quiz\)\{quiz\.classList\.add\('show'\);"
            r"setTimeout\(\(\)=>quiz\.scrollIntoView\(\{behavior:'smooth',block:'nearest'\}\),200\);\}\}\}",
            r"}",
            html
        )

    # FIX Q7 question text (currently has Q8's content — 3/8 + 2/8)
    # Q7 should ask: Which is larger, 5/6 or 7/8?
    html = re.sub(
        r'(<div class="quiz-label"><span class="yr-badge yr4">Y4</span> Question 7[^<]*</div>\s*<div class="question">).*?(</div>)',
        r'\1Which fraction is larger — <strong>5/6</strong> or <strong>7/8</strong>?<br><br>Think carefully — the denominators are different.\2',
        html, flags=re.DOTALL
    )
    # Fix Q7 correct answer (currently 3/8, should be 7/8 is bigger)
    # Find Q7 options and rewrite
    q7_old = re.search(r'(quiz-q7.*?)<div class="feedback"', html, re.DOTALL)
    if q7_old:
        q7_block = q7_old.group(0)
        new_opts = (
            '<button class="opt-btn" onclick="answer(this,true,\'q7\')">7/8 is larger</button>\n'
            '        <button class="opt-btn" onclick="answer(this,false,\'q7\')">5/6 is larger</button>\n'
            '        <button class="opt-btn" onclick="answer(this,false,\'q7\')">They are equal</button>\n'
            '        <button class="opt-btn" onclick="answer(this,false,\'q7\')">Cannot compare</button>\n'
            '        '
        )
        new_q7 = re.sub(r'<div class="options">.*?</div>', f'<div class="options">\n        {new_opts}</div>', q7_block, flags=re.DOTALL)
        html = html.replace(q7_old.group(0), new_q7, 1)

    # FIX Q8 question text (currently has Q9's content — 1/4+2/4+3/4)
    # Q8 should ask: Jake has 3/8 and 2/8, needs to make 1 whole. What fraction missing?
    html = re.sub(
        r'(<div class="quiz-label"><span class="yr-badge yr4">Y4</span> Question 8[^<]*</div>\s*<div class="question">).*?(</div>)',
        r'\1Jake has <strong>3/8</strong> and <strong>2/8</strong> fraction tokens.<br><br>He needs tokens that sum to exactly <strong>1 whole (8/8)</strong>.<br><br>What fraction does he still need?\2',
        html, flags=re.DOTALL
    )
    # Fix Q8 correct answer (currently "1 and 1/2", should be "3/8")
    q8_old = re.search(r'(quiz-q8.*?)<div class="feedback"', html, re.DOTALL)
    if q8_old:
        q8_block = q8_old.group(0)
        new_opts8 = (
            '<button class="opt-btn" onclick="answer(this,true,\'q8\')">3/8</button>\n'
            '          <button class="opt-btn" onclick="answer(this,false,\'q8\')">2/8</button>\n'
            '          <button class="opt-btn" onclick="answer(this,false,\'q8\')">5/8</button>\n'
            '          <button class="opt-btn" onclick="answer(this,false,\'q8\')">1/8</button>\n'
            '          '
        )
        new_q8 = re.sub(r'<div class="options">.*?</div>', f'<div class="options">\n          {new_opts8}</div>', q8_block, flags=re.DOTALL)
        html = html.replace(q8_old.group(0), new_q8, 1)

    # FIX correct/wrong messages for Q7 and Q8
    html = html.replace(
        "q7:'🎉 Right! 3/8 is the missing token that makes Jake's collection add up to exactly 1 whole (8/8). Token collected — door unlocked!'",
        "q7:'🎉 Right! 7/8 > 5/6. Convert to 24ths: 21/24 vs 20/24. 7/8 wins! Jake takes the faster route to the terminal.'"
    )
    html = html.replace(
        "q7:'❌ Add 3/8 + 2/8 = 5/8. You need 8/8 to make a whole. 8/8 − 5/8 = 3/8.'",
        "q7:'❌ Convert to 24ths: 5/6 = 20/24, 7/8 = 21/24. Which is bigger?'"
    )
    html = html.replace(
        "q8:'🎉 Correct! 1/4 + 2/4 + 3/4 = 6/4 = 1 and 2/4 = 1 and 1/2. Mixed number unlocked!'",
        "q8:'🎉 Correct! 3/8 + 2/8 = 5/8. To reach 8/8, Jake needs 3 more eighths. Token collected — door opens!'"
    )
    html = html.replace(
        "q8:'❌ Add: 1/4 + 2/4 + 3/4 = 6/4. Convert: 6/4 = 1 whole and 2/4 left = 1 and 1/2.'",
        "q8:'❌ 3/8 + 2/8 = 5/8. How many more eighths do you need to make 8/8 (= 1 whole)?'"
    )

    if html != original:
        with open(path, 'w') as f:
            f.write(html)
        print("  ✅ issue-005-narrated.html — fixed")
    else:
        print("  ⚠️  HTML unchanged — check manually")


if __name__ == "__main__":
    print("Building Issue 5 images...")
    make_q1()
    make_q3()
    make_q7()
    make_q8()
    make_q9()
    make_q10()
    print("\nFixing HTML...")
    fix_html()
    print("\nAll done!")
