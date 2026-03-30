import requests, base64, time, os

api_key = "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"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

def gen_image(prompt, output_path, retries=3):
    for attempt in range(1, retries+1):
        payload = {"model": "gpt-image-1", "prompt": prompt, "size": "1536x1024", "quality": "medium", "n": 1}
        resp = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=payload)
        data = resp.json()
        if "data" in data:
            img_bytes = base64.b64decode(data["data"][0]["b64_json"])
            with open(output_path, "wb") as f:
                f.write(img_bytes)
            print(f"Generated: {output_path} ({len(img_bytes)} bytes)")
            return True
        else:
            print(f"  Attempt {attempt} ERROR: {data.get('error', {}).get('message', data)}")
            if attempt < retries:
                wait = 10 * attempt
                print(f"  Waiting {wait}s before retry...")
                time.sleep(wait)
    return False

# Only retry the ones that failed (skip q2 which already succeeded)
images = [
    (
        "images/ocean/issue001/q1-coralfolk-dock.png",
        "bioluminescent coral docking bay underwater, two clearly separated groups of small crab-like Coralfolk creatures unloading glowing supply crates, three creatures in each group, vivid orange and teal coral architecture, deep indigo water, no text, no numbers"
    ),
    (
        "images/ocean/issue001/q3-market-stalls.png",
        "underwater coral market, three separate market stalls side by side, each stall displaying five identical glowing items arranged neatly, small Coralfolk vendor at each stall, vivid teal and amber coral architecture, no text, no numbers"
    ),
    (
        "images/ocean/issue001/q4-keeper-groups.png",
        "underwater ocean floor, five clearly separated pairs of small crab-like Coralfolk keeper creatures walking in the same direction toward glowing signal stones in distance, two keepers per group, deep indigo water, bioluminescent coral city background, no text"
    ),
    (
        "images/ocean/issue001/q5-coral-windows.png",
        "tall glowing coral tower underwater, two levels clearly visible, six glowing circular windows on each level, windows glowing warm amber from inside, deep indigo water, dramatic vertical composition, no text, no numbers"
    ),
    (
        "images/ocean/issue001/q6-signal-stones.png",
        "ocean floor, four clearly separated clusters of glowing amber signal stones, four stones in each cluster, deep midnight blue water, bioluminescent atmosphere, no text, no numbers"
    ),
    (
        "images/ocean/issue001/q7-keeper-pairs.png",
        "ocean floor near Signal Tower, three clearly separated groups of small Coralfolk keeper creatures, six keepers in each group walking together, vivid coral city in background, deep indigo water, no text"
    ),
    (
        "images/ocean/issue001/q8-coral-lanterns.png",
        "interior of coral Signal Tower, five walkways visible each strung with four glowing amber lanterns in a line, warm amber light, ornate coral architecture, dramatic perspective, no text, no numbers"
    ),
    (
        "images/ocean/issue001/q9-coralfolk-gathering.png",
        "interior of coral Signal Tower, two clearly separated groups of small Coralfolk creatures gathered watching the flickering signal map, seven creatures in each group, teal and amber glow, concerned expressions, no text"
    ),
    (
        "images/ocean/issue001/q10-dark-stone-clusters.png",
        "ocean floor, three clearly separated clusters of signal stones that have gone dark, three dark stones per cluster, surrounded by still-glowing amber stones, deep midnight blue water, sense of creeping darkness, no text"
    ),
]

results = []
for i, (output_path, prompt) in enumerate(images):
    # Skip if already exists
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        size = os.path.getsize(output_path)
        print(f"[SKIP] {output_path} already exists ({size} bytes)")
        results.append((output_path, True))
        continue
    print(f"\n[{i+1}/{len(images)}] Generating {output_path}...")
    success = gen_image(prompt, output_path)
    results.append((output_path, success))
    if i < len(images) - 1:
        print("Sleeping 5s...")
        time.sleep(5)

print("\n=== SUMMARY ===")
for path, ok in results:
    status = "OK" if ok else "FAILED"
    if ok and os.path.exists(path):
        size = os.path.getsize(path)
        print(f"[{status}] {path} ({size} bytes)")
    else:
        print(f"[{status}] {path}")
