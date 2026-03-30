import requests, base64

api_key = "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"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
BASE = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/ocean/issue004/"

whale_base = "close section of whale skin, glowing blue-green bioluminescent spots arranged in a clean regular grid, clearly countable rows and columns, dark deep ocean background, no text, no numbers, no labels"

images = [
    ("q1-whale-spots.png", f"{whale_base}, three rows of six spots each"),
    ("q2-whale-spots.png", f"{whale_base}, five rows of six spots each"),
    ("q3-whale-spots.png", f"{whale_base}, four rows of seven spots each"),
    ("q4-whale-spots.png", f"{whale_base}, six rows of seven spots each"),
    ("q5-whale-spots.png", f"{whale_base}, three rows of eight spots each"),
    ("q9-lattice-signal.png", "six rows of six glowing amber signal stones, all glowing brightly, ocean floor scene, no text, no numbers, no labels"),
]

for filename, prompt in images:
    print(f"Generating {filename}...")
    payload = {"model": "gpt-image-1", "prompt": prompt, "size": "1536x1024", "quality": "medium", "n": 1}
    resp = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=payload)
    data = resp.json()
    if "data" in data and data["data"]:
        img_bytes = base64.b64decode(data["data"][0]["b64_json"])
        with open(BASE + filename, "wb") as f:
            f.write(img_bytes)
        print(f"  ✅ {filename} ({len(img_bytes)} bytes)")
    else:
        print(f"  ❌ {filename}: {data}")

print("All image generation complete!")
