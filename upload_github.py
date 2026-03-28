import base64, json, urllib.request, urllib.error

TOKEN = "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"
REPO = "MathBlastAu/math-blast"
FILE_PATH = "images/gpt4o-test-result.png"
LOCAL_PATH = "/Users/leohiem/.openclaw/workspace/projects/math-blast/images/gpt4o-test-result.png"
API_URL = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

headers = {
    "Authorization": f"token {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "MathBlast-Uploader"
}

# Get existing SHA
sha = None
try:
    req = urllib.request.Request(API_URL, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        sha = data.get("sha")
        print(f"Existing file SHA: {sha}")
except urllib.error.HTTPError as e:
    if e.code == 404:
        print("File doesn't exist yet, will create")
    else:
        print(f"Error getting SHA: {e}")

# Read and encode image
with open(LOCAL_PATH, 'rb') as f:
    content = base64.b64encode(f.read()).decode()

payload = {
    "message": "Add gpt-image-1 test result",
    "content": content
}
if sha:
    payload["sha"] = sha

req = urllib.request.Request(
    API_URL,
    data=json.dumps(payload).encode(),
    headers=headers,
    method="PUT"
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print(f"Upload success! URL: {result.get('content', {}).get('html_url', 'unknown')}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Upload failed: {e.code} - {body}")
