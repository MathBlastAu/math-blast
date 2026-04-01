#!/bin/bash
# Image generation for Crystal Compass Issue 2
OUTDIR="/Users/leohiem/.openclaw/workspace/projects/math-blast/images/crystal-compass/issue-002"
API_KEY="${OPENAI_API_KEY}"

generate_image() {
  local filename="$1"
  local prompt="$2"
  local outfile="$OUTDIR/$filename"
  
  if [ -f "$outfile" ]; then
    echo "SKIP: $filename (exists)"
    return 0
  fi
  
  echo "GEN IMAGE: $filename"
  
  response=$(curl -s -X POST "https://api.openai.com/v1/images/generations" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"gpt-image-1\",\"prompt\":$(echo "$prompt" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'),\"size\":\"1024x1024\",\"quality\":\"medium\",\"n\":1}")
  
  # Check for error
  if echo "$response" | grep -q '"error"'; then
    echo "ERROR for $filename: $response"
    return 1
  fi
  
  # Extract base64 and save
  echo "$response" | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
b64 = data['data'][0]['b64_json']
with open('$outfile', 'wb') as f:
    f.write(base64.b64decode(b64))
print('Saved: $outfile')
"
  sleep 1
}

STYLE="Pixar-style 3D CGI animation, exaggerated cartoon proportions, large head relative to body, big expressive eyes, vibrant saturated jewel-tone colours, bold clear single emotion per character, animated feature film style, magical lighting, clean storybook illustration"
CHARS="Isla (Caucasian girl, wild curly auburn-red hair, green eyes, bold smirk), Priya (South Asian girl, long dark hair in plait, large round purple glasses), Zoe (East Asian girl, short neat black bob, calm composed expression), Amara (African heritage girl, large natural hair puff with yellow headband, big warm smile) — all wearing white blouse, navy pleated skirt, navy blazer with crest badge, white knee socks, black school shoes"
FOREST="midnight blue background, glowing cyan and purple trees, pulsing lights, soft mist at ground level"

# Image 1: Forest entrance
generate_image "ch1-forest-entrance.png" "Four distinct school girls step into an enchanted glowing forest for the first time — $CHARS. All four girls in foreground, looking up in wonder at enormous cyan and purple glowing trees. Mist swirls at their feet. $FOREST. Wide-angle view showing all four girls clearly. $STYLE"

# Image 2: Priya pattern
generate_image "ch2-priya-pattern.png" "Priya (South Asian girl, long dark hair in plait, large round purple glasses) stands in the foreground pointing excitedly at pulsing cyan lights in glowing trees, notebook open in her other hand, huge excited expression. Behind her, Isla (Caucasian, wild curly auburn-red hair, green eyes, bold smirk), Zoe (East Asian, short neat black bob, calm expression), and Amara (African heritage, large natural hair puff with yellow headband, warm smile) all wearing white blouse, navy pleated skirt, navy blazer with crest badge — all watching Priya. $FOREST. $STYLE"

# Image 3: River stones
generate_image "ch3-river-stones.png" "Four school girls at the edge of a magical glowing river — Isla (Caucasian, wild curly auburn-red hair, green eyes, bold smirk), Priya (South Asian, long dark hair in plait, large round purple glasses), Zoe (East Asian, short neat black bob, calm expression), Amara (African heritage, large natural hair puff with yellow headband, warm smile) — all wearing white blouse, navy pleated skirt, navy blazer with crest badge, white knee socks, black school shoes. Numbered stepping stones stretch across the river, some glowing gold and some dark. Magical shimmering water with ominous red glow below the dark stones. Dramatic, adventurous mood. $STYLE"

# Image 4: Door and rising water
generate_image "ch4-door-water.png" "Priya (South Asian girl, long dark hair in plait, large round purple glasses) in the foreground frantically tracing carved circle patterns on a massive ancient stone door, urgent panicked expression. Behind her: Isla (Caucasian, wild curly auburn-red hair), Zoe (East Asian, short neat black bob), Amara (African heritage, large natural hair puff with yellow headband) — all wearing navy school uniforms, all looking behind them in panic as glowing magical water rises up the bank toward their feet. Stone door beginning to glow. Urgent dramatic scene. $STYLE"

# Image 5: Mountain base (cliffhanger)
generate_image "ch5-mountain-base.png" "Four school girls arrive at the base of a huge glowing magical mountain at night — Isla (Caucasian, wild curly auburn-red hair, green eyes, bold smirk) is already one step ahead on the first glowing stone step, looking back at the others confidently. Behind her: Priya (South Asian, long dark hair in plait, large round purple glasses), Zoe (East Asian, short neat black bob), Amara (African heritage, large natural hair puff with yellow headband) — all wearing white blouse, navy pleated skirt, navy blazer with crest badge. Stone steps with glowing numbers spiral upward into clouds. Dramatic cliffhanger mood, looking up into mystery. $STYLE"

# Image 6: Win screen celebration
generate_image "win-screen.png" "Four school girls celebrating joyfully in a glowing magical forest — Isla (Caucasian, wild curly auburn-red hair, green eyes, huge grin, arms raised), Priya (South Asian, long dark hair in plait, large round purple glasses, jumping with excitement), Zoe (East Asian, short neat black bob, rare big smile, arms up), Amara (African heritage, large natural hair puff with yellow headband, biggest warmest smile, arms raised high) — all wearing white blouse, navy pleated skirt, navy blazer with crest badge, white knee socks, black school shoes. Cyan and purple pulsing lights celebrate around them. Triumphant, joyful, celebratory mood. $STYLE"

echo "All images generated!"
ls -la "$OUTDIR"/*.png 2>/dev/null | wc -l
