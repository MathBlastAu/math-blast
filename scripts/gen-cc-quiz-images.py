#!/usr/bin/env python3
"""Generate place value block diagrams for Crystal Compass quiz questions using Pillow"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/crystal-compass/issue-001"
os.makedirs(OUT_DIR, exist_ok=True)

# Colour palette
BG_COLOUR = (255, 220, 130)        # warm amber background
TEN_COLOUR = (212, 160, 20)        # gold for tens columns
TEN_OUTLINE = (160, 110, 0)
ONE_COLOUR = (0, 200, 210)         # cyan for ones squares
ONE_OUTLINE = (0, 140, 160)
TEXT_COLOUR = (80, 40, 0)          # dark brown text
LABEL_BG = (255, 240, 180)

def make_place_value_image(tens, ones, filename, title=None):
    W, H = 480, 340
    img = Image.new("RGB", (W, H), BG_COLOUR)
    draw = ImageDraw.Draw(img)

    # Title
    if title:
        draw.text((W//2, 18), title, fill=TEXT_COLOUR, anchor="mt")

    # Draw tens columns (tall rectangles stacked)
    ten_w, ten_h = 36, 28
    ten_x_start = 60
    ten_y_start = 240
    ten_spacing = 46

    draw.text((ten_x_start + (tens * ten_spacing) // 2 if tens > 0 else ten_x_start + 20,
               260), "Tens", fill=TEXT_COLOUR, anchor="mt")

    for i in range(tens):
        x = ten_x_start + i * ten_spacing
        # Stack 10 small blocks per ten column
        for j in range(10):
            y = ten_y_start - j * (ten_h + 2)
            draw.rectangle([x, y, x + ten_w, y + ten_h], fill=TEN_COLOUR, outline=TEN_OUTLINE, width=2)
            # Small line detail
            draw.line([(x+4, y+ten_h//2), (x+ten_w-4, y+ten_h//2)], fill=TEN_OUTLINE, width=1)

    # Draw ones squares
    one_w, one_h = 32, 32
    one_x_start = 280
    one_y_start = 240
    one_spacing = 40

    if ones > 0:
        draw.text((one_x_start + min(ones, 3) * one_spacing // 2,
                   260), "Ones", fill=TEXT_COLOUR, anchor="mt")

    for i in range(ones):
        col = i % 3
        row = i // 3
        x = one_x_start + col * one_spacing
        y = one_y_start - row * (one_h + 4)
        draw.rectangle([x, y, x + one_w, y + one_h], fill=ONE_COLOUR, outline=ONE_OUTLINE, width=2)

    # Number answer area (shown as blank with dashes)
    draw.rectangle([W//2 - 50, 270, W//2 + 50, 310], fill=LABEL_BG, outline=TEXT_COLOUR, width=2)
    draw.text((W//2, 290), f"{tens} tens  +  {ones} ones  =  ?", fill=TEXT_COLOUR, anchor="mm")

    out_path = os.path.join(OUT_DIR, filename)
    img.save(out_path)
    print(f"Saved: {filename}")

# Generate quiz images for the main questions
quiz_images = [
    (2, 3, "q1-cc-issue001.png", "Q1: What number is this?"),
    (4, 7, "q2-cc-issue001.png", "Q2: What number is this?"),
    (7, 4, "q3-cc-issue001.png", "Q3: What number is this?"),
    (5, 0, "q4-cc-issue001.png", "Q4: What number is this?"),
    (0, 8, "q5-cc-issue001.png", "Q5: What number is this?"),
    (6, 3, "q6-cc-issue001.png", "Q6: What number is this?"),
    (9, 1, "q9-cc-issue001.png", "Q9: What number is this?"),
    (10, 0, "q10-cc-issue001.png", "Q10: 10 tens = ?"),
]

for tens, ones, fname, title in quiz_images:
    make_place_value_image(tens, ones, fname, title)

print("All quiz images done!")
