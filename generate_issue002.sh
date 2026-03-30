#!/bin/bash

API_KEY="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"
OUTPUT_DIR="/Users/leohiem/.openclaw/workspace/projects/math-blast/images/jungle/issue002"

generate_image() {
  local filename="$1"
  local prompt="$2"
  local output_path="$OUTPUT_DIR/$filename"
  
  echo "Generating: $filename..."
  
  response=$(curl -s -X POST "https://api.openai.com/v1/images/generations" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"gpt-image-1\",
      \"prompt\": $(echo "$prompt" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),
      \"size\": \"1536x1024\",
      \"quality\": \"medium\",
      \"n\": 1
    }")
  
  # Check for error
  if echo "$response" | python3 -c "import json,sys; d=json.load(sys.stdin); print('ERROR:', d.get('error',{}).get('message',''))" 2>/dev/null | grep -q "ERROR: ."; then
    echo "ERROR generating $filename:"
    echo "$response" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('error',{}).get('message','Unknown error'))"
    return 1
  fi
  
  # Extract b64_json and save
  echo "$response" | python3 -c "
import json, sys, base64
data = json.load(sys.stdin)
b64 = data['data'][0]['b64_json']
img_bytes = base64.b64decode(b64)
with open('$output_path', 'wb') as f:
    f.write(img_bytes)
print('Saved: $filename (' + str(len(img_bytes)) + ' bytes)')
"
  
  if [ $? -ne 0 ]; then
    echo "Failed to save $filename"
    echo "Response: $response" | head -c 500
    return 1
  fi
  
  return 0
}

# Image 1
generate_image "ch1-fernmoss-arrival.png" "Vibrant children's adventure illustration. A 10-year-old girl (Blaze — dark skin, short natural hair, orange explorer vest) arrives at a lower-canopy jungle village built among enormous glowing blue bioluminescent mushrooms. A small round-headed bright-blue Sprocket creature (knee height, large eyes, tiny antennae) stands looking worried amid small medicine bottles. Misty atmosphere, warm magical light. Painterly digital art style."

# Image 2
generate_image "ch2-food-store.png" "Vibrant children's adventure illustration. A 10-year-old girl (Blaze — dark skin, short natural hair, orange explorer vest) examines baskets of nuts and seeds inside a jungle storage hut lit by glowing blue mushrooms. In the background, a tiny bright-blue Sprocket creature rests on a leaf-bed, looking unwell. Warm mushroom glow, painterly digital art style."

# Image 3
generate_image "ch3-counting-store.png" "Vibrant children's adventure illustration. A 10-year-old girl (Blaze — dark skin, short natural hair, orange explorer vest) sorts through storage boxes on shelves filled with seeds and leaves. Ancient jungle canopy visible through gaps in the hut walls. Warm green light, painterly digital art style."

# Image 4
generate_image "ch4-vine-pattern.png" "Vibrant children's adventure illustration. A 10-year-old girl (Blaze — dark skin, short natural hair, orange explorer vest) crouches on a jungle floor, studying a trail of cut vines arranged in neat groups. She points at something on the ground. Dappled mysterious jungle light, slightly ominous mood. Painterly digital art style."

# Image 5
generate_image "ch5-distribution-fixed.png" "Vibrant children's adventure illustration. A group of small bright-blue Sprocket creatures (round heads, large eyes, tiny antennae, knee height) each holding their correct equal share of colourful jungle food. A 10-year-old girl (Blaze — dark skin, short natural hair, orange explorer vest) stands to one side looking satisfied. Warm glowing blue mushroom light, celebratory mood. Painterly digital art style."

# Image 6
generate_image "q1-medicine-doses.png" "Vibrant children's educational illustration. A shelf holds 12 small glowing medicine bottles. In front of the shelf stand exactly 4 small bright-blue Sprocket creatures (round heads, large eyes, tiny antennae). The mismatch between 12 bottles and 4 Sprockets is visually clear. Blue bioluminescent lighting, clean and clear composition. Painterly digital art style."

# Image 7
generate_image "q2-nut-baskets.png" "Vibrant children's educational illustration. 48 round nuts being divided into 8 equal piles on a jungle wooden surface. Each pile clearly contains 6 nuts. Clean, clear educational image showing equal grouping. Warm jungle colours, painterly digital art style."

# Image 8
generate_image "q3-sick-sprocket.png" "Vibrant children's educational illustration. A tiny bright-blue Sprocket creature (round head, large eyes, tiny antennae) lying in a leaf-bed looking unwell. Beside it, a glowing medicine cup. The scene conveys needing extra medicine. Warm sympathetic lighting, painterly digital art style."

# Image 9
generate_image "q4-healing-leaves.png" "Vibrant children's educational illustration. 56 bright green healing leaves arranged in 7 equal groups of 8 on a wooden jungle surface. Each group is clearly separated. Blue mushroom glow in background. Clean educational composition, painterly digital art style."

# Image 10
generate_image "q5-seed-groups.png" "Vibrant children's educational illustration. 63 small round seeds arranged in 7 neat circular piles of 9 on a jungle floor. Each pile is clearly distinct. Clean, clear grouping diagram. Warm jungle colours, painterly digital art style."

# Image 11
generate_image "q6-vine-trips.png" "Vibrant children's educational illustration. 42 vines arranged in 7 groups of 6 on a jungle floor. Between each group are large mysterious creature footprints suggesting repeated trips. Jungle setting, slightly mysterious mood. Painterly digital art style."

# Image 12
generate_image "q7-vine-bundles.png" "Vibrant children's educational illustration. 35 green vines neatly arranged in 5 equal bundles of 7, each tied with a leaf. Jungle floor setting. Clean, clear grouping. Warm jungle colours, painterly digital art style."

# Image 13
generate_image "q8-vine-trail-map.png" "Vibrant children's educational illustration. A hand-drawn style illustrated map showing a jungle vine trail between two tree villages. The trail is divided into 9 equal sections, each 8 units long. Distance markers visible. Top-down illustrated view, warm parchment colours with jungle green accents. Painterly digital art style."

# Image 14
generate_image "q9-resource-share.png" "Vibrant children's educational illustration. 81 colourful jungle fruits and nuts arranged in 9 equal piles of 9 on a woven mat. Each pile is clearly distinct and contains the same items. Clean educational composition, warm colours, painterly digital art style."

# Image 15
generate_image "q10-boss-fraction.png" "Vibrant children's educational illustration. 9 colourful jungle food items displayed in a row. 6 of them glow brightly (representing three-quarters), while 3 are dimmer. Clear visual fraction-of-a-set diagram. Clean educational composition, painterly digital art style."

# Image 16
generate_image "cliffhanger-deep-root.png" "Vibrant children's adventure illustration. Dark jungle night scene. In the far background, enormous ancient twisted trees loom — the Deep Root. In the foreground mud, a trail of massive vine-creature footprints (five-toed, enormous) leads toward the ancient trees. Bioluminescent green glow from moss. Mysterious, beautiful, slightly foreboding. No people or creatures visible. Painterly digital art style."

echo ""
echo "=== Generation Complete ==="
ls -la "$OUTPUT_DIR"/*.png 2>/dev/null | wc -l | xargs echo "Total PNG files:"
ls -la "$OUTPUT_DIR"/*.png 2>/dev/null
