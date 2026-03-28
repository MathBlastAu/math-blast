import os
import time
import base64
import requests
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

images_dir = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images"
github_token = "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"
repo = "MathBlastAu/math-blast"
headers = {"Authorization": f"token {github_token}"}

tasks = [
    {
        "filename": "q5-issue001.png",
        "prompt": "A glowing futuristic spaceship dashboard display screen showing the digital time '3:15' in large bright numbers, sci-fi holographic style, blue and orange glow, space station interior background. Pixar 3D animation style, vibrant colours, soft warm lighting, child-friendly, cinematic quality."
    },
    {
        "filename": "q6-issue001.png",
        "prompt": "A futuristic spaceship schedule board showing two digital time displays side by side: left screen shows '3:15' with a rocket launch icon, right screen shows '3:45' with an arrival icon, a glowing arrow between them labelled '? minutes', sci-fi holographic style, blue and orange glow. Pixar 3D animation style, vibrant colours, soft warm lighting, child-friendly, cinematic quality."
    }
]

for i, task in enumerate(tasks):
    filename = task["filename"]
    prompt = task["prompt"]
    local_path = os.path.join(images_dir, filename)

    print(f"Generating {filename}...")
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    # Save image
    image_data = base64.b64decode(response.data[0].b64_json)
    with open(local_path, "wb") as f:
        f.write(image_data)
    print(f"Saved {local_path} ({len(image_data)} bytes)")

    # Upload to GitHub
    r = requests.get(f"https://api.github.com/repos/{repo}/contents/images/{filename}", headers=headers)
    sha = r.json().get("sha") if r.status_code == 200 else None

    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    body = {"message": f"Fix clock images: use digital display for {filename}", "content": content}
    if sha:
        body["sha"] = sha

    put_r = requests.put(f"https://api.github.com/repos/{repo}/contents/images/{filename}", json=body, headers=headers)
    print(f"GitHub upload {filename}: {put_r.status_code} - {put_r.json().get('content', {}).get('name', put_r.text[:100])}")

    if i < len(tasks) - 1:
        print("Sleeping 13 seconds...")
        time.sleep(13)

print("Done!")
