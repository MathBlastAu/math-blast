#!/usr/bin/env python3
import os
import time
import base64
import json
import requests

API_KEY = os.environ.get("OPENAI_API_KEY")
OUTDIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/crystal-compass/issue-002"

HEIGHT_CONSTRAINT = "All four girls are exactly the same height and have identical body proportions — consistent child scale across the whole group. No girl is smaller or shorter than the others."

images = [
    {
        "filename": "ch1-forest-entrance.png",
        "prompt": f"Four school girls step into an enchanted glowing forest for the first time, looking up in wonder. Left to right: Isla (Caucasian, wild curly auburn-red hair, bright green eyes), Priya (South Asian, long dark plait, large round purple glasses), Zoe (East Asian, short neat black bob), Amara (African heritage, natural hair puff with yellow headband). All wearing white blouse open collar NO TIE, navy pleated skirt, navy blazer with gold crest badge, white knee socks, black school shoes. Wide-angle view showing all four girls clearly in foreground. {HEIGHT_CONSTRAINT} Background: midnight blue glowing forest, enormous cyan and purple bioluminescent trees, soft mist at ground level, floating lights pulse gently. Mood: wonder and amazement. Pixar-style 3D CGI animation, polished feature-film render quality, child proportions with slightly oversized heads (1:3.5 head-to-body ratio), large glossy expressive eyes with specular highlights, soft button noses, rounded features. Expressions are animated-feature-poster intensity — clear and readable but NOT rubber-hose extreme. Dual lighting: warm amber key light from above-behind, cool cyan magical fill from below. Shallow depth-of-field backgrounds. High-quality subsurface scattering on skin."
    },
    {
        "filename": "ch2-priya-pattern.png",
        "prompt": f"Priya (South Asian girl, long dark hair in single plait, large round purple glasses) stands in the foreground of a glowing enchanted forest, pointing excitedly at pulsing cyan lights in the trees, open notebook in her other hand. Excited but composed expression — NOT exaggerated. Behind her: Isla (Caucasian, wild curly auburn-red hair), Zoe (East Asian, short neat black bob), Amara (African heritage, natural hair puff with yellow headband), all watching Priya with interest. All four girls wearing white blouse open collar NO TIE, navy pleated skirt, navy blazer with gold crest badge. {HEIGHT_CONSTRAINT} Background: midnight blue glowing forest, cyan and purple trees, floating lights. Pixar-style 3D CGI animation, polished feature-film render quality, child proportions with slightly oversized heads (1:3.5 head-to-body ratio), large glossy expressive eyes with specular highlights, soft button noses, rounded features. Expressions are animated-feature-poster intensity — clear and readable but NOT rubber-hose extreme. Dual lighting: warm amber key light from above-behind, cool cyan magical fill from below. Shallow depth-of-field backgrounds. High-quality subsurface scattering on skin."
    },
    {
        "filename": "ch3-river-stones.png",
        "prompt": f"Four school girls stand at the edge of a wide glowing river in an enchanted forest, looking across at stepping stones that stretch to the other side. Left to right: Isla (Caucasian, wild curly auburn-red hair, bright green eyes), Priya (South Asian, long dark plait, large round purple glasses), Zoe (East Asian, short neat black bob), Amara (African heritage, natural hair puff with yellow headband). All wearing white blouse open collar NO TIE, navy pleated skirt, navy blazer with gold crest badge, white knee socks, black school shoes. {HEIGHT_CONSTRAINT} The stepping stones are round flat rocks — some glowing gold (safe), some dark with ominous red glow from water beneath (unsafe). NO numbers or text on the stones. Magical shimmering water. Mood: adventurous, slightly tense. Pixar-style 3D CGI animation, polished feature-film render quality, child proportions with slightly oversized heads (1:3.5 head-to-body ratio), large glossy expressive eyes with specular highlights, soft button noses, rounded features. Expressions are animated-feature-poster intensity — clear and readable but NOT rubber-hose extreme. Dual lighting: warm amber key light from above-behind, cool cyan magical fill from below. Shallow depth-of-field backgrounds. High-quality subsurface scattering on skin."
    },
    {
        "filename": "ch4-door-water.png",
        "prompt": f"Priya (South Asian girl, long dark hair in single plait, large round purple glasses) in the foreground pressing her hands against a massive ancient stone door carved with circular patterns, urgent determined expression. Behind her: Isla (Caucasian, wild curly auburn-red hair), Zoe (East Asian, short neat black bob), Amara (African heritage, natural hair puff with yellow headband) — all wearing white blouse open collar NO TIE, navy pleated skirt, navy blazer with gold crest badge — all glancing back in alarm as glowing turquoise water rises up behind them. The stone door glows warmly as it begins to open. {HEIGHT_CONSTRAINT} Dramatic urgent mood. Pixar-style 3D CGI animation, polished feature-film render quality, child proportions with slightly oversized heads (1:3.5 head-to-body ratio), large glossy expressive eyes with specular highlights, soft button noses, rounded features. Expressions are animated-feature-poster intensity — clear and readable but NOT rubber-hose extreme. Dual lighting: warm amber key light from above-behind, cool cyan magical fill from below. Shallow depth-of-field backgrounds. High-quality subsurface scattering on skin."
    },
    {
        "filename": "win-screen.png",
        "prompt": f"Four school girls celebrating joyfully in a glowing enchanted forest. Left to right: Isla (Caucasian, wild curly auburn-red hair, bright green eyes, arms raised and grinning), Priya (South Asian, long dark plait, large round purple glasses, jumping with delight), Zoe (East Asian, short neat black bob, rare warm big smile), Amara (African heritage, natural hair puff with yellow headband, arms wide open, beaming). All wearing white blouse open collar NO TIE, navy pleated skirt, navy blazer with gold crest badge, white knee socks, black school shoes. {HEIGHT_CONSTRAINT} Background: glowing cyan and purple forest, celebratory light arcs and sparkles all around. Triumphant joyful mood. Pixar-style 3D CGI animation, polished feature-film render quality, child proportions with slightly oversized heads (1:3.5 head-to-body ratio), large glossy expressive eyes with specular highlights, soft button noses, rounded features. Expressions are animated-feature-poster intensity — clear and readable but NOT rubber-hose extreme. Dual lighting: warm amber key light from above-behind, cool cyan magical fill from below. Shallow depth-of-field backgrounds. High-quality subsurface scattering on skin."
    }
]

results = []

for i, img in enumerate(images):
    filepath = os.path.join(OUTDIR, img["filename"])

    # Delete existing file
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Deleted existing: {img['filename']}")

    print(f"Generating {img['filename']} ({i+1}/5)...")

    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-image-1",
                "prompt": img["prompt"],
                "size": "1024x1024",
                "quality": "medium",
                "response_format": "b64_json",
                "n": 1
            },
            timeout=120
        )

        if response.status_code == 200:
            data = response.json()
            b64_data = data["data"][0]["b64_json"]
            img_bytes = base64.b64decode(b64_data)
            with open(filepath, "wb") as f:
                f.write(img_bytes)
            size_kb = len(img_bytes) // 1024
            print(f"  SUCCESS: Saved: {img['filename']} ({size_kb} KB)")
            results.append({"file": img["filename"], "status": "success", "size_kb": size_kb})
        else:
            print(f"  ERROR {response.status_code}: {response.text}")
            results.append({"file": img["filename"], "status": "error", "detail": response.text[:300]})

    except Exception as e:
        print(f"  EXCEPTION: {e}")
        results.append({"file": img["filename"], "status": "exception", "detail": str(e)})

    if i < len(images) - 1:
        print("  Sleeping 2s...")
        time.sleep(2)

print("\n=== FINAL RESULTS ===")
for r in results:
    print(json.dumps(r))

success = sum(1 for r in results if r["status"] == "success")
print(f"\n{success}/5 images generated successfully.")
