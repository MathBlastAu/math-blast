import openai, base64, os, sys

client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])

img_path = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/ch1-crashed-rocket.png'
out_path = '/Users/leohiem/.openclaw/workspace/projects/math-blast/images/gpt4o-test-result.png'

print("=== Test 1: images.edit with gpt-image-1 ===")
try:
    result = client.images.edit(
        model="gpt-image-1",
        image=open(img_path, 'rb'),
        prompt="Jake — the same 10-year-old boy with short messy brown hair, bright green eyes, light freckles, orange space suit with silver trim, red rocket patch on left shoulder — discovers a room full of multiplication arrays made of glowing alien crates arranged in 3 rows of 4. He looks excited pointing at them. Pixar 3D animation style, vibrant colours, soft warm lighting, child-friendly.",
        size="1024x1024"
    )
    print("Test 1 SUCCESS")
    # Save image
    if hasattr(result.data[0], 'b64_json') and result.data[0].b64_json:
        img_bytes = base64.b64decode(result.data[0].b64_json)
        with open(out_path, 'wb') as f:
            f.write(img_bytes)
        print(f"Saved to {out_path}")
    elif hasattr(result.data[0], 'url') and result.data[0].url:
        import urllib.request
        urllib.request.urlretrieve(result.data[0].url, out_path)
        print(f"Downloaded from URL and saved to {out_path}")
    print("METHOD:Test1-images.edit")
    sys.exit(0)
except Exception as e:
    print(f"Test 1 FAILED: {e}")

print("\n=== Test 2: responses API with gpt-4o ===")
try:
    with open(img_path, 'rb') as f:
        img_data = base64.b64encode(f.read()).decode()

    response = client.responses.create(
        model="gpt-4o",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_image", "image_url": f"data:image/png;base64,{img_data}"},
                {"type": "input_text", "text": "Using the character of Jake shown in this image (the boy in the orange space suit), generate a new illustration: Jake discovers a room full of multiplication arrays made of glowing alien crates arranged in 3 rows of 4. He looks excited pointing at them. Pixar 3D animation style, vibrant colours, soft warm lighting, child-friendly. Size: 1024x1024."}
            ]
        }],
        tools=[{"type": "image_generation", "size": "1024x1024", "quality": "medium"}]
    )
    print("Test 2 response received")
    # Extract image from response
    for item in response.output:
        print(f"  Output item type: {item.type}")
        if item.type == 'image_generation_call':
            img_bytes = base64.b64decode(item.result)
            with open(out_path, 'wb') as f:
                f.write(img_bytes)
            print(f"Saved to {out_path}")
            print("METHOD:Test2-responses-api")
            sys.exit(0)
    print("Test 2: No image found in response")
except Exception as e:
    print(f"Test 2 FAILED: {e}")

print("\n=== Test 3: gpt-image-1 text-only generation ===")
try:
    result = client.images.generate(
        model="gpt-image-1",
        prompt="Jake, a 10-year-old boy with short messy brown hair, bright green eyes, light freckles across his nose, wearing a bright orange space suit with silver trim and a red rocket patch on his left shoulder, discovers a room full of multiplication arrays made of glowing alien crates arranged in 3 rows of 4. He looks excited pointing at them. Pixar 3D animation style, vibrant colours, soft warm lighting, child-friendly.",
        size="1024x1024",
        output_format="b64_json"
    )
    print("Test 3 SUCCESS")
    img_bytes = base64.b64decode(result.data[0].b64_json)
    with open(out_path, 'wb') as f:
        f.write(img_bytes)
    print(f"Saved to {out_path}")
    print("METHOD:Test3-gpt-image-1-text-only")
    sys.exit(0)
except Exception as e:
    print(f"Test 3 FAILED: {e}")

print("ALL TESTS FAILED")
sys.exit(1)
