#!/usr/bin/env python3
"""Generate story images for Crystal Compass Issue 1"""
import os, requests, base64, json

API_KEY = os.environ.get("OPENAI_API_KEY")
OUT_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/crystal-compass/issue-001"
os.makedirs(OUT_DIR, exist_ok=True)

STYLE = "Pixar-style 3D CGI, warm amber and gold colour palette, soft cyan accent lighting, rich volumetric lighting, clean storybook atmosphere, characters in MLC school uniform (white button-up blouse, dark navy pleated skirt, navy blazer with crest badge, white knee-high socks, black school shoes)"

CHAR_ISLA = "a Caucasian girl with curly auburn-red hair, bright green eyes, a bold smirk, hands on hips"
CHAR_PRIYA = "a South Asian girl with a long dark plait, round purple glasses, a curious expression"
CHAR_ZOE = "an East Asian girl with a short neat black bob, composed warm expression"
CHAR_AMARA = "an African girl with natural curly hair in a puff, a yellow headband, a big warm smile"
CHAR_COMPASS = "an ornate golden compass with Celtic knotwork decoration, four coloured gems, glowing cyan face, spinning needle"

scenes = {
    "ch1-compass-found.png": f"""A warm cosy school library scene. Four schoolgirls, {CHAR_ISLA}, {CHAR_PRIYA}, {CHAR_ZOE}, and {CHAR_AMARA}, stand huddled excitedly around a round wooden table. On the table sits an open ornate wooden box. Inside the box is {CHAR_COMPASS}. Soft cyan light glows upward from the box, illuminating the girls faces with wonder. Background: tall dark-wood bookshelves lined with books, arched gothic windows with warm amber afternoon light streaming in, reading chairs, warm golden atmosphere. {STYLE}""",

    "ch2-zoe-studies.png": f"""A warm school library scene. {CHAR_ZOE} holds up {CHAR_COMPASS} in both hands, studying it closely with focused curious eyes. The compass glows cyan in her hands, casting blue light on her face. Behind her, {CHAR_ISLA}, {CHAR_PRIYA}, and {CHAR_AMARA} watch with interest. Dark wooden bookshelves in background, warm amber light. {STYLE}""",

    "ch3-priya-notebook.png": f"""A warm school library scene. {CHAR_PRIYA} sits at a wooden library table, writing enthusiastically in an open notebook with a pencil. In the centre of the table, {CHAR_COMPASS} glows with soft cyan light. Around the table, {CHAR_ISLA}, {CHAR_ZOE}, and {CHAR_AMARA} lean in with engaged, curious expressions. Books and papers scattered on table. Warm amber library light, dark wood shelves behind them. {STYLE}""",

    "ch4-compass-flickers.png": f"""A warm school library scene with an urgent atmosphere. {CHAR_COMPASS} sits on the table, its glow flickering weakly, pulsing between bright and dark. The four girls, {CHAR_ISLA}, {CHAR_PRIYA}, {CHAR_ZOE}, and {CHAR_AMARA}, look panicked and worried. Isla points at the compass urgently. Amara looks alarmed. Zoe looks focused and intense. The room lighting flickers slightly. Warm amber library, dark bookshelves. {STYLE}""",

    "ch5-door-opens.png": f"""A dramatic school library scene. In the background, a heavy arched wooden door has swung open in the library wall. Through the doorway glows a magical forest scene with trees that shimmer in cyan and purple light, their leaves luminescent and pulsing gently. Four girl silhouettes stand at the threshold of the doorway, looking into the glowing forest beyond with wonder. The contrast between the warm amber library interior and the magical cyan forest beyond is striking. {CHAR_COMPASS} is visible in one of the girls' hands, glowing. {STYLE}""",
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

results = {}
for filename, prompt in scenes.items():
    out_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(out_path):
        print(f"SKIP (exists): {filename}")
        results[filename] = "exists"
        continue
    print(f"Generating: {filename}")
    resp = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json={
            "model": "gpt-image-1",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "quality": "medium"
        },
        timeout=120
    )
    if resp.status_code != 200:
        print(f"ERROR {resp.status_code}: {resp.text[:300]}")
        results[filename] = f"error: {resp.status_code}"
        continue
    data = resp.json()
    img_b64 = data["data"][0]["b64_json"]
    img_bytes = base64.b64decode(img_b64)
    with open(out_path, "wb") as f:
        f.write(img_bytes)
    print(f"  Saved: {out_path} ({len(img_bytes)//1024}KB)")
    results[filename] = f"ok ({len(img_bytes)//1024}KB)"

print("\n=== RESULTS ===")
for k, v in results.items():
    print(f"  {k}: {v}")
