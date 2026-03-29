#!/usr/bin/env python3
"""Issue 7 — all Pillow question images. Big, clear, no answers shown."""

from PIL import Image, ImageDraw, ImageFont
import os, random

OUT = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"
BG=(13,6,48); PURPLE=(160,60,255); CYAN=(0,200,255); GOLD=(255,185,0)
GREEN=(0,220,100); RED=(255,80,80); WHITE=(255,255,255); GREY=(80,70,120)
ORANGE=(255,140,0)

def fnt(size, bold=False):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
              else "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def stars(d,w,h,n=50):
    random.seed(99)
    for _ in range(n):
        x,y=random.randint(0,w),random.randint(0,h)
        r=random.choice([1,1,2])
        d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255,random.randint(60,180)))

def new_img(w=1024,h=640):
    img=Image.new("RGBA",(w,h),BG); d=ImageDraw.Draw(img,"RGBA"); stars(d,w,h); return img,d

def tick(d,px,cy,h=28,col=WHITE,lw=5): d.line([(px,cy-h),(px,cy+h)],fill=col,width=lw)
def dot(d,px,cy,col,r=14):
    for sp in [r+8,r+4]: d.ellipse([px-sp,cy-sp,px+sp,cy+sp],fill=(*col,50))
    d.ellipse([px-r,cy-r,px+r,cy+r],fill=col)
def nline(d,lx,rx,cy,w=8):
    d.line([(lx,cy),(rx,cy)],fill=CYAN,width=w)
    d.polygon([(rx,cy),(rx-20,cy-10),(rx-20,cy+10)],fill=CYAN)

def draw_tank(d,cx,cy,tw,th,total,filled,col):
    d.rounded_rectangle([cx-tw//2,cy-th//2,cx+tw//2,cy+th//2],radius=10,outline=col,width=4,fill=(20,10,50))
    seg=th/total
    for i in range(total):
        y1=cy+th//2-(i+1)*seg; y2=cy+th//2-i*seg
        d.rounded_rectangle([cx-tw//2+5,int(y1)+2,cx+tw//2-5,int(y2)-2],radius=4,
                             fill=col if i<filled else (30,15,60))

def save(img,name): img.convert("RGB").save(f"{OUT}/{name}"); print(f"  ✅ {name}")


# ── Q1: Two tanks side by side — 20 units and 10 units, both ½ full ──────────
def make_q1():
    img,d=new_img()
    # Tank A: 20 units, 10 filled (½)
    draw_tank(d,270,300,180,400,10,5,CYAN)
    d.text((270,530),"20 units",fill=CYAN,font=fnt(52,True),anchor="mm")
    d.text((270,150),"Tank A",fill=CYAN,font=fnt(48,True),anchor="mm")
    d.text((270,200),"½ full",fill=GOLD,font=fnt(44,True),anchor="mm")
    d.text((270,580),"= ? units",fill=RED,font=fnt(48,True),anchor="mm")

    # vs
    d.text((512,310),"½",fill=GOLD,font=fnt(140,True),anchor="mm")
    d.text((512,440),"vs",fill=WHITE,font=fnt(60,True),anchor="mm")
    d.text((512,510),"½",fill=GOLD,font=fnt(140,True),anchor="mm")

    # Tank B: 10 units, 5 filled (½)
    draw_tank(d,754,300,140,300,10,5,PURPLE)
    d.text((754,480),"10 units",fill=PURPLE,font=fnt(52,True),anchor="mm")
    d.text((754,150),"Tank B",fill=PURPLE,font=fnt(48,True),anchor="mm")
    d.text((754,200),"½ full",fill=GOLD,font=fnt(44,True),anchor="mm")
    d.text((754,540),"= ? units",fill=RED,font=fnt(48,True),anchor="mm")

    save(img,"q1-issue007.png")


# ── Q2: Bar showing ½ vs ⅓ of same 12-unit bar ───────────────────────────────
def make_q2():
    img,d=new_img()
    # 12-unit bar — top: ½ shown
    bx,bw,bh=80,860,90; gap=24
    by1=180; by2=by1+bh+gap+bh+80

    # Row 1: ½ of 12
    d.text((512,by1-50),"½  of  12",fill=CYAN,font=fnt(60,True),anchor="mm")
    for i in range(12):
        x=bx+i*(bw//12); w=bw//12-2
        col=CYAN if i<6 else (30,15,60)
        d.rounded_rectangle([x,by1,x+w,by1+bh],radius=5,fill=col,outline=GREY,width=2)
    d.text((bx+bw//4,by1+bh+16),"6",fill=CYAN,font=fnt(44,True),anchor="mm")
    d.text((bx+bw//4*3,by1+bh+16),"",fill=GREY,font=fnt(44,True),anchor="mm")

    # Row 2: ⅓ of 12
    by2_label=by1+bh+80
    d.text((512,by2_label-10),"⅓  of  12",fill=PURPLE,font=fnt(60,True),anchor="mm")
    by2_bar=by2_label+50
    for i in range(12):
        x=bx+i*(bw//12); w=bw//12-2
        col=PURPLE if i<4 else (30,15,60)
        d.rounded_rectangle([x,by2_bar,x+w,by2_bar+bh],radius=5,fill=col,outline=GREY,width=2)
    d.text((bx+bw//6,by2_bar+bh+16),"4",fill=PURPLE,font=fnt(44,True),anchor="mm")

    d.text((512,600),"Which shows MORE?",fill=GOLD,font=fnt(56,True),anchor="mm")
    save(img,"q2-issue007.png")


# ── Q3: Kepler station 40-unit tank, 1/4 taken ───────────────────────────────
def make_q3():
    img,d=new_img()
    draw_tank(d,260,300,180,400,4,1,CYAN)
    d.text((260,530),"40 units",fill=CYAN,font=fnt(52,True),anchor="mm")
    d.text((260,140),"Kepler Station",fill=CYAN,font=fnt(44,True),anchor="mm")

    d.text((680,200),"1",fill=GOLD,font=fnt(180,True),anchor="mm")
    d.line([(560,280),(800,280)],fill=GOLD,width=7)
    d.text((680,380),"4",fill=GOLD,font=fnt(180,True),anchor="mm")
    d.text((680,490),"of 40  =  ?",fill=RED,font=fnt(80,True),anchor="mm")
    save(img,"q3-issue007.png")


# ── Q4: Vega station 16-unit tank, 1/4 taken — smaller tank ──────────────────
def make_q4():
    img,d=new_img()
    draw_tank(d,260,300,140,320,4,1,PURPLE)
    d.text((260,490),"16 units",fill=PURPLE,font=fnt(52,True),anchor="mm")
    d.text((260,140),"Station Vega",fill=PURPLE,font=fnt(44,True),anchor="mm")

    d.text((680,200),"1",fill=GOLD,font=fnt(180,True),anchor="mm")
    d.line([(560,280),(800,280)],fill=GOLD,width=7)
    d.text((680,380),"4",fill=GOLD,font=fnt(180,True),anchor="mm")
    d.text((680,490),"of 16  =  ?",fill=RED,font=fnt(80,True),anchor="mm")
    save(img,"q4-issue007.png")


# ── Q5: 32-unit tank → needs 3/4 full. How many units? ───────────────────────
def make_q5():
    img,d=new_img()
    # Tank empty → target = 3/4
    draw_tank(d,240,300,180,400,4,0,GREY)
    # Target line at 3/4
    target_y=300+200-int(300*0.75)  # 3/4 up from bottom
    d.line([(140,target_y+100),(360,target_y+100)],fill=GREEN,width=5)
    d.text((380,target_y+100),"← 3/4",fill=GREEN,font=fnt(50,True),anchor="lm")
    d.text((240,530),"32 units",fill=WHITE,font=fnt(52,True),anchor="mm")
    d.text((240,140),"New Algorithm",fill=GOLD,font=fnt(44,True),anchor="mm")

    d.text((700,220),"3/4",fill=GREEN,font=fnt(180,True),anchor="mm")
    d.text((700,420),"of 32  =  ?",fill=RED,font=fnt(80,True),anchor="mm")
    save(img,"q5-issue007.png")


# ── Q6: 24-unit tank → needs 3/4 full ────────────────────────────────────────
def make_q6():
    img,d=new_img()
    draw_tank(d,240,300,160,360,4,0,GREY)
    d.text((240,510),"24 units",fill=WHITE,font=fnt(52,True),anchor="mm")
    d.text((240,140),"New Algorithm",fill=GOLD,font=fnt(44,True),anchor="mm")

    d.text((700,220),"3/4",fill=GREEN,font=fnt(180,True),anchor="mm")
    d.text((700,420),"of 24  =  ?",fill=RED,font=fnt(80,True),anchor="mm")
    save(img,"q6-issue007.png")


# ── Q7: 16-unit tank at ½, needs to reach ¾. How many more? ──────────────────
def make_q7():
    img,d=new_img()
    # Tank at ½ (2 of 4 quarters filled)
    draw_tank(d,240,300,180,400,4,2,CYAN)

    # Target marker at ¾
    ty=300+200-int(400*0.75)
    d.line([(140,ty+100),(360,ty+100)],fill=GREEN,width=5)
    d.text((370,ty+100),"← 3/4",fill=GREEN,font=fnt(46,True),anchor="lm")

    # Current marker at ½ already shown by fill
    d.text((240,540),"16 units",fill=CYAN,font=fnt(52,True),anchor="mm")
    d.text((240,145),"Already at ½",fill=CYAN,font=fnt(44,True),anchor="mm")

    # Gap = ¼
    d.text((700,200),"½  →  ¾",fill=WHITE,font=fnt(90,True),anchor="mm")
    d.text((700,330),"gap  =  ¼",fill=GOLD,font=fnt(90,True),anchor="mm")
    d.text((700,460),"¼ of 16  =  ?",fill=RED,font=fnt(80,True),anchor="mm")
    save(img,"q7-issue007.png")


# ── Q8: Order ¼, ½, ¾ from least to most correction ─────────────────────────
def make_q8():
    img,d=new_img()
    # Three big tiles in scrambled order
    fracs=[("¼",PURPLE),("¾",GREEN),("½",GOLD)]
    xs=[180,512,844]
    for (fr,col),x in zip(fracs,xs):
        d.rounded_rectangle([x-120,140,x+120,440],radius=18,fill=(25,12,55),outline=col,width=4)
        d.text((x,290),fr,fill=col,font=fnt(180,True),anchor="mm")
        d.text((x,400),"tank",fill=col,font=fnt(40),anchor="mm")

    d.text((512,540),"Order:  LEAST  →  MOST",fill=GOLD,font=fnt(60,True),anchor="mm")
    save(img,"q8-issue007.png")


# ── Q9: Station A: 40-unit, at ¼, needs ¾. How many units to add? ────────────
def make_q9():
    img,d=new_img()
    # Tank at ¼ (1 of 4 filled)
    draw_tank(d,240,310,180,400,4,1,CYAN)

    # Target at ¾
    ty=310+200-int(400*0.75)
    d.line([(140,ty+100),(360,ty+100)],fill=GREEN,width=5)
    d.text((370,ty+100),"← ¾",fill=GREEN,font=fnt(46,True),anchor="lm")

    d.text((240,145),"Station A",fill=CYAN,font=fnt(48,True),anchor="mm")
    d.text((240,540),"40 units",fill=CYAN,font=fnt(52,True),anchor="mm")

    d.text((700,190),"¼  →  ¾",fill=WHITE,font=fnt(90,True),anchor="mm")
    d.text((700,310),"gap  =  ½",fill=GOLD,font=fnt(90,True),anchor="mm")
    d.text((700,430),"½ of 40  =  ?",fill=RED,font=fnt(80,True),anchor="mm")
    save(img,"q9-issue007.png")


# ── Q10: Station B: 20-unit, empty, needs ½. Do 60 units cover both? ─────────
def make_q10():
    img,d=new_img()
    # Station A summary (greyed)
    draw_tank(d,180,280,120,260,4,1,GREY)
    d.text((180,430),"A: 40u",fill=GREY,font=fnt(38,True),anchor="mm")
    d.text((180,472),"needs 20",fill=GREY,font=fnt(36),anchor="mm")

    # Station B — empty, target ½
    draw_tank(d,380,280,120,260,2,0,PURPLE)
    d.text((380,430),"B: 20u",fill=PURPLE,font=fnt(38,True),anchor="mm")
    d.text((380,472),"½ of 20  =  ?",fill=RED,font=fnt(36,True),anchor="mm")

    # 60 units available
    d.rounded_rectangle([560,160,960,580],radius=20,fill=(20,10,55),outline=GOLD,width=4)
    d.text((760,240),"60 units",fill=GOLD,font=fnt(90,True),anchor="mm")
    d.text((760,350),"available",fill=GOLD,font=fnt(56),anchor="mm")
    d.text((760,460),"A needs 20",fill=CYAN,font=fnt(50,True),anchor="mm")
    d.text((760,530),"B needs  ?",fill=RED,font=fnt(50,True),anchor="mm")

    save(img,"q10-issue007.png")


if __name__ == "__main__":
    print("Building Issue 7 images...")
    make_q1(); make_q2(); make_q3(); make_q4(); make_q5()
    make_q6(); make_q7(); make_q8(); make_q9(); make_q10()
    print("\nAll done!")
