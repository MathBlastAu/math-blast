import openai, os, time, requests, base64, subprocess

# Load API key from zshrc
result = subprocess.run(['zsh', '-c', 'source ~/.zshrc && echo $OPENAI_API_KEY'], capture_output=True, text=True)
api_key = result.stdout.strip()
print(f"API key loaded: {'yes' if api_key else 'NO - MISSING'}")

client = openai.OpenAI(api_key=api_key)
ref_path = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/ch1-crashed-rocket.png'
out_dir = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/'
gh_headers = {"Authorization": "token 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"}

def save_image(result, filename):
    item = result.data[0]
    path = out_dir + filename
    # gpt-image-1 returns b64_json by default
    if hasattr(item, 'b64_json') and item.b64_json:
        with open(path, 'wb') as f:
            f.write(base64.b64decode(item.b64_json))
    elif hasattr(item, 'url') and item.url:
        r = requests.get(item.url)
        with open(path, 'wb') as f:
            f.write(r.content)
    else:
        raise ValueError(f"No image data in response: {item}")
    print(f"Saved {filename}")
    return path

def upload(local_path, github_name):
    r = requests.get(f"https://api.github.com/repos/MathBlastAu/math-blast/contents/images/{github_name}", headers=gh_headers)
    sha = r.json().get("sha") if r.status_code == 200 else None
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    body = {"message": f"Preview: {github_name}", "content": content}
    if sha: body["sha"] = sha
    resp = requests.put(f"https://api.github.com/repos/MathBlastAu/math-blast/contents/images/{github_name}", json=body, headers=gh_headers)
    print(f"Uploaded {github_name}: HTTP {resp.status_code}")
    return resp.status_code

# Q4 - pizza only, no Jake
print("Generating q4...")
r = client.images.generate(
    model="gpt-image-1",
    prompt="A single large round pizza cut into exactly 4 equal quarters with clean straight cuts, seen from directly above, Pixar 3D animation style, bright warm colours, one slice slightly pulled apart to show the division, simple clean background, child-friendly illustration",
    size="1024x1024"
)
path = save_image(r, "q4-preview.png")
upload(path, "q4-preview.png")
time.sleep(13)

# Q5 - Jake + clock with no answer shown
print("Generating q5...")
r = client.images.edit(
    model="gpt-image-1",
    image=open(ref_path, 'rb'),
    prompt="Jake — a 10-year-old boy with short messy brown hair, bright green eyes, light freckles, orange space suit with silver trim, red rocket patch on left shoulder — stands in a spacecraft cockpit pointing at a large round wall clock. The clock face shows only two hands (no numbers), with the short hand just past the 3 position and the long hand pointing straight at the 3. A large glowing question mark floats beside the clock. Pixar 3D animation style, vibrant colours, soft warm lighting, child-friendly",
    size="1024x1024"
)
path = save_image(r, "q5-preview.png")
upload(path, "q5-preview.png")
time.sleep(13)

# Q6 - Jake + countdown timer, no answer times shown
print("Generating q6...")
r = client.images.edit(
    model="gpt-image-1",
    image=open(ref_path, 'rb'),
    prompt="Jake — a 10-year-old boy with short messy brown hair, bright green eyes, light freckles, orange space suit with silver trim, red rocket patch on left shoulder — sits urgently at a spacecraft control panel. A large red digital countdown display shows '30:00' with warning lights flashing around it and a LAUNCH WINDOW label. No other clock times are visible. He looks focused and urgent. Pixar 3D animation style, vibrant colours, dramatic lighting, child-friendly",
    size="1024x1024"
)
path = save_image(r, "q6-preview.png")
upload(path, "q6-preview.png")
time.sleep(13)

# Q10 - Jake + dashboard showing problem but NOT the answer
print("Generating q10...")
r = client.images.edit(
    model="gpt-image-1",
    image=open(ref_path, 'rb'),
    prompt="Jake — a 10-year-old boy with short messy brown hair, bright green eyes, light freckles, orange space suit with silver trim, red rocket patch on left shoulder — looks urgently at a spacecraft dashboard showing two panels: one glowing panel reads 'RE-ENTRY: 4:10' with an Earth icon, another shows 'WARM-UP: 35 MIN' with a flame icon, and a third panel shows 'START TIME: ?' with a question mark. Earth glows through the window behind him. Pixar 3D animation style, vibrant colours, dramatic warm lighting, child-friendly",
    size="1024x1024"
)
path = save_image(r, "q10-preview.png")
upload(path, "q10-preview.png")

print("All done!")
