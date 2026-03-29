#!/usr/bin/env python3
"""Issue 6 — all Pillow images. Big fonts, fill the canvas, no answer text."""

from PIL import Image, ImageDraw, ImageFont
import os, random, math

OUT = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"
BG=(13,6,48); PURPLE=(160,60,255); CYAN=(0,200,255); GOLD=(255,185,0)
GREEN=(0,220,100); RED=(255,80,80); WHITE=(255,255,255); GREY=(80,70,120)

def fnt(size, bold=False):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
              else "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def stars(d,w,h,n=50):
    random.seed(42)
    for _ in range(n):
        x,y=random.randint(0,w),random.randint(0,h)
        r=random.choice([1,1,2])
        d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255,random.randint(60,180)))

def new_img(w=1024,h=640):
    img=Image.new("RGBA",(w,h),BG); d=ImageDraw.Draw(img,"RGBA"); stars(d,w,h); return img,d

def tick(d,px,cy,h=30,col=WHITE,lw=5): d.line([(px,cy-h),(px,cy+h)],fill=col,width=lw)
def dot(d,px,cy,col,r=14):
    for sp in [r+8,r+4]: d.ellipse([px-sp,cy-sp,px+sp,cy+sp],fill=(*col,50))
    d.ellipse([px-r,cy-r,px+r,cy+r],fill=col)
def nline(d,lx,rx,cy,w=8):
    d.line([(lx,cy),(rx,cy)],fill=CYAN,width=w)
    d.polygon([(rx,cy),(rx-20,cy-10),(rx-20,cy+10)],fill=CYAN)
def save(img,name):
    img.convert("RGB").save(f"{OUT}/{name}"); print(f"  ✅ {name}")

def draw_tank(d, cx, cy, w, h, units, filled, col):
    """Draw a fuel tank with filled units."""
    d.rounded_rectangle([cx-w//2,cy-h//2,cx+w//2,cy+h//2],radius=10,outline=col,width=4,fill=(20,10,50))
    seg=h/units
    for i in range(units):
        y1=cy+h//2-(i+1)*seg; y2=cy+h//2-i*seg
        d.rounded_rectangle([cx-w//2+5,int(y1)+2,cx+w//2-5,int(y2)-2],radius=4,
                            fill=col if i<filled else (30,15,60))

def spaceship(d,cx,cy,sc=1.0,col=CYAN):
    s=sc
    d.ellipse([cx-int(65*s),cy-int(26*s),cx+int(65*s),cy+int(26*s)],fill=col,outline=WHITE,width=3)
    d.polygon([(cx+int(65*s),cy),(cx+int(98*s),cy-int(11*s)),(cx+int(98*s),cy+int(11*s))],fill=WHITE)
    d.polygon([(cx-int(22*s),cy+int(22*s)),(cx-int(56*s),cy+int(56*s)),(cx+int(22*s),cy+int(26*s))],fill=col,outline=WHITE,width=2)
    d.polygon([(cx-int(22*s),cy-int(22*s)),(cx-int(56*s),cy-int(56*s)),(cx+int(22*s),cy-int(26*s))],fill=col,outline=WHITE,width=2)
    d.ellipse([cx-int(70*s),cy-int(9*s),cx-int(60*s),cy+int(9*s)],fill=GOLD)


# ── Q1: Number line 1→2 with 3 examples of fractions between 1 and 2 ─────────
def make_q1():
    img,d=new_img()
    lx,rx,cy=60,940,260
    nline(d,lx,rx,cy)
    for fv,lb,col in [(0,"1",WHITE),(1,"2",WHITE)]:
        px=lx+fv*(rx-lx)
        tick(d,px,cy,38,col,6)
        f=fnt(72,True); w=d.textlength(lb,font=f)
        d.text((px-w/2,cy+50),lb,fill=col,font=f)

    # 3 example positions (no labels — just show the region)
    for fv,col in [(0.25,PURPLE),(0.5,GOLD),(0.75,CYAN)]:
        px=lx+fv*(rx-lx)
        tick(d,px,cy,36,col,5)
        dot(d,px,cy,col,16)

    # Bracket showing the region
    d.line([(lx+10,cy-80),(rx-10,cy-80)],fill=GOLD,width=3)
    d.line([(lx+10,cy-80),(lx+10,cy-68)],fill=GOLD,width=3)
    d.line([(rx-10,cy-80),(rx-10,cy-68)],fill=GOLD,width=3)
    d.text((512,cy-115),"fractions live here",fill=GOLD,font=fnt(44,True),anchor="mm")

    # Show some examples as large text
    d.text((200,450),"1¼",fill=PURPLE,font=fnt(120,True),anchor="mm")
    d.text((512,450),"1½",fill=GOLD,font=fnt(120,True),anchor="mm")
    d.text((824,450),"1¾",fill=CYAN,font=fnt(120,True),anchor="mm")
    d.text((512,580),"Name THREE fractions between 1 and 2",fill=GREY,font=fnt(36),anchor="mm")
    save(img,"q1-issue006.png")


# ── Q2: 1¾ as improper fraction — big stacked display ────────────────────────
def make_q2():
    img,d=new_img()
    # Mixed number large on left
    d.text((220,200),"1",fill=WHITE,font=fnt(200,True),anchor="mm")
    d.text((340,160),"3",fill=GOLD,font=fnt(120,True),anchor="mm")
    d.line([(300,210),(420,210)],fill=GOLD,width=6)
    d.text((340,280),"4",fill=GOLD,font=fnt(120,True),anchor="mm")

    # Arrow
    d.text((512,220),"→",fill=WHITE,font=fnt(130,True),anchor="mm")

    # Improper fraction — just numerator as ?
    d.text((760,160),"?",fill=RED,font=fnt(200,True),anchor="mm")
    d.line([(660,290),(860,290)],fill=RED,width=6)
    d.text((760,400),"4",fill=RED,font=fnt(120,True),anchor="mm")

    d.text((512,540),"How many quarters altogether?",fill=GREY,font=fnt(42),anchor="mm")
    save(img,"q2-issue006.png")


# ── Q3: 11/4 as mixed number ─────────────────────────────────────────────────
def make_q3():
    img,d=new_img()
    # Big 11/4 on left
    d.text((240,180),"11",fill=PURPLE,font=fnt(200,True),anchor="mm")
    d.line([(110,270),(370,270)],fill=WHITE,width=7)
    d.text((240,380),"4",fill=PURPLE,font=fnt(200,True),anchor="mm")

    d.text((512,270),"→",fill=WHITE,font=fnt(130,True),anchor="mm")

    # Mixed number: ? wholes and ? quarters
    d.text((720,180),"?",fill=GOLD,font=fnt(200,True),anchor="mm")
    d.text((820,220),"?",fill=CYAN,font=fnt(100,True),anchor="mm")
    d.line([(800,275),(920,275)],fill=CYAN,width=5)
    d.text((860,330),"4",fill=CYAN,font=fnt(100,True),anchor="mm")

    d.text((512,540),"4 quarters = 1 whole. How many wholes in 11?",fill=GREY,font=fnt(36),anchor="mm")
    save(img,"q3-issue006.png")


# ── Q4: Spaceship 24-unit tank, 1/3 taken — ? units ─────────────────────────
def make_q4():
    img,d=new_img()
    spaceship(d,280,220,sc=1.9,col=CYAN)
    d.text((280,380),"24-unit tank",fill=CYAN,font=fnt(52,True),anchor="mm")

    # Tank with 1/3 highlighted (8 units)
    draw_tank(d,280,500,150,100,3,1,CYAN)
    d.text((280,570),"1/3  = ? units",fill=RED,font=fnt(46,True),anchor="mm")

    d.text((720,200),"1",fill=GOLD,font=fnt(180,True),anchor="mm")
    d.line([(620,275),(820,275)],fill=GOLD,width=7)
    d.text((720,370),"3",fill=GOLD,font=fnt(180,True),anchor="mm")
    d.text((720,490),"of  24  =  ?",fill=RED,font=fnt(80,True),anchor="mm")
    save(img,"q4-issue006.png")


# ── Q5: Spaceship 18-unit tank, 1/3 taken — ? units ─────────────────────────
def make_q5():
    img,d=new_img()
    spaceship(d,280,220,sc=1.4,col=PURPLE)
    d.text((280,360),"18-unit tank",fill=PURPLE,font=fnt(52,True),anchor="mm")

    draw_tank(d,280,480,130,90,3,1,PURPLE)
    d.text((280,555),"1/3  = ? units",fill=RED,font=fnt(46,True),anchor="mm")

    d.text((720,200),"1",fill=GOLD,font=fnt(180,True),anchor="mm")
    d.line([(620,275),(820,275)],fill=GOLD,width=7)
    d.text((720,370),"3",fill=GOLD,font=fnt(180,True),anchor="mm")
    d.text((720,490),"of  18  =  ?",fill=RED,font=fnt(80,True),anchor="mm")
    save(img,"q5-issue006.png")


# ── Q6: Journey 28 units, 3/4 of route — how many units? ─────────────────────
def make_q6():
    img,d=new_img()
    lx,rx,cy=60,940,280
    nline(d,lx,rx,cy)
    for fv,lb,col in [(0,"0",WHITE),(1,"28",WHITE)]:
        px=lx+fv*(rx-lx); tick(d,px,cy,36,col,6)
        f=fnt(64,True); w=d.textlength(lb,font=f)
        d.text((px-w/2,cy+48),lb,fill=col,font=f)

    # 3/4 mark
    px34=lx+0.75*(rx-lx)
    tick(d,px34,cy,44,PURPLE,6); dot(d,px34,cy,PURPLE,16)
    d.text((px34,cy-90),"3/4",fill=PURPLE,font=fnt(72,True),anchor="mm")

    # Filled bar showing 3/4
    d.rounded_rectangle([lx+4,cy-22,px34-4,cy+22],radius=8,fill=(*PURPLE,180))
    d.text(((lx+px34)/2,cy+100),"3/4 of 28 = ? units",fill=GOLD,font=fnt(60,True),anchor="mm")

    # Gap remainder
    d.rounded_rectangle([px34+4,cy-22,rx-4,cy+22],radius=8,fill=(30,15,60),outline=GREY,width=3)
    save(img,"q6-issue006.png")


# ── Q7: 3/4 of 28 units done, what fraction remains? ─────────────────────────
def make_q7():
    img,d=new_img()
    lx,rx,cy=60,940,280
    nline(d,lx,rx,cy)
    for fv,lb,col in [(0,"0",WHITE),(1,"28",WHITE)]:
        px=lx+fv*(rx-lx); tick(d,px,cy,36,col,6)
        f=fnt(64,True); w=d.textlength(lb,font=f)
        d.text((px-w/2,cy+48),lb,fill=col,font=f)

    px34=lx+0.75*(rx-lx)
    tick(d,px34,cy,44,PURPLE,6); dot(d,px34,cy,PURPLE,16)
    d.text((px34,cy-80),"3/4",fill=PURPLE,font=fnt(68,True),anchor="mm")

    # Done = purple fill
    d.rounded_rectangle([lx+4,cy-22,px34-4,cy+22],radius=8,fill=(*PURPLE,180))
    d.text(((lx+px34)/2,cy+90),"Done ✓",fill=PURPLE,font=fnt(50,True),anchor="mm")

    # Remaining = red gap with ?
    d.rounded_rectangle([px34+4,cy-22,rx-4,cy+22],radius=8,fill=(255,80,80,100),outline=RED,width=4)
    d.text(((px34+rx)/2,cy-80),"?",fill=RED,font=fnt(80,True),anchor="mm")
    d.text(((px34+rx)/2,cy+90),"? of 28 = ?",fill=RED,font=fnt(50,True),anchor="mm")
    save(img,"q7-issue006.png")


# ── Q8: ¾ hour + ¼ hour = total ──────────────────────────────────────────────
def make_q8():
    img,d=new_img()
    # Big simple addition
    d.text((210,220),"¾",fill=PURPLE,font=fnt(220,True),anchor="mm")
    d.text((210,370),"hour",fill=PURPLE,font=fnt(60,True),anchor="mm")
    d.text((512,260),"+",fill=WHITE,font=fnt(150,True),anchor="mm")
    d.text((812,220),"¼",fill=CYAN,font=fnt(220,True),anchor="mm")
    d.text((812,370),"hour",fill=CYAN,font=fnt(60,True),anchor="mm")
    d.line([(80,460),(940,460)],fill=WHITE,width=5)
    d.text((512,560),"= ?",fill=GOLD,font=fnt(120,True),anchor="mm")
    save(img,"q8-issue006.png")


# ── Q9: 1/5 × 15 stations = total as fraction of 1 station ──────────────────
def make_q9():
    img,d=new_img()
    # 15 small station icons in a grid
    cols,rows=5,3; sw=60; gap=20
    total_w=cols*(sw+gap)-gap; sx=(1024-total_w)//2; sy=80
    for i in range(15):
        r,c=divmod(i,cols)
        x=sx+c*(sw+gap); y=sy+r*(sw+gap+10)
        col=RED if i<3 else (40,20,80)  # 1/5 highlighted (3 of 15)
        d.rounded_rectangle([x,y,x+sw,y+sw],radius=8,fill=col,outline=CYAN,width=2)
        d.text((x+sw//2,y+sw//2),"S",fill=WHITE,font=fnt(28,True),anchor="mm")

    d.text((512,370),"15 stations  ×  1/5  =  ?",fill=WHITE,font=fnt(68,True),anchor="mm")
    d.text((512,460),"Express as a fraction of 1 station",fill=GREY,font=fnt(42),anchor="mm")
    d.text((170,200),"1/5",fill=RED,font=fnt(50,True),anchor="mm")
    d.text((170,240),"taken",fill=RED,font=fnt(36),anchor="mm")
    save(img,"q9-issue006.png")


# ── Q10: 3 calculations — 2/3×24 + 3/4×16 + 1/2×12 = ? ─────────────────────
def make_q10():
    img,d=new_img()
    # Three rows of calculations
    items=[
        ("2/3","×","24","=","?",PURPLE),
        ("3/4","×","16","=","?",CYAN),
        ("1/2","×","12","=","?",GOLD),
    ]
    ys=[140,280,420]
    for (fr,op,n,eq,ans,col),y in zip(items,ys):
        d.text((140,y),fr,fill=col,font=fnt(90,True),anchor="mm")
        d.text((280,y),op,fill=WHITE,font=fnt(80,True),anchor="mm")
        d.text((380,y),n,fill=WHITE,font=fnt(90,True),anchor="mm")
        d.text((480,y),eq,fill=WHITE,font=fnt(80,True),anchor="mm")
        d.text((560,y),ans,fill=RED,font=fnt(90,True),anchor="mm")

    d.line([(80,490),(700,490)],fill=WHITE,width=4)
    d.text((400,555),"Total  =  ?",fill=GOLD,font=fnt(80,True),anchor="mm")
    save(img,"q10-issue006.png")


if __name__ == "__main__":
    print("Building Issue 6 Pillow images...")
    make_q1(); make_q2(); make_q3(); make_q4(); make_q5()
    make_q6(); make_q7(); make_q8(); make_q9(); make_q10()
    print("\nAll done!")
