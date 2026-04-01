#!/bin/bash
# Audio generation script for Crystal Compass Issue 2
# Voice IDs:
# Narrator (Alice): Xb7hH8MSUJpSbSDYk0k2
# Miss Zara: FGY2WhTYpPnrIDTdsKH5
# Isla: MUzMONRCyBSA0l61GzC2
# Priya: Qs8eI0FA8ZWoy7VJQK0C
# Zoe: x6KItt3dczXfR55FonpL
# Amara: uOwZUqvORJmMLzgFFB5A

set -e
OUTDIR="/Users/leohiem/.openclaw/workspace/projects/math-blast/audio/crystal-compass/issue-002"
API_KEY="${ELEVENLABS_API_KEY}"
MODEL="eleven_turbo_v2_5"

generate() {
  local voice_id="$1"
  local filename="$2"
  local text="$3"
  local outfile="$OUTDIR/$filename"
  
  if [ -f "$outfile" ]; then
    echo "SKIP: $filename (exists)"
    return 0
  fi
  
  echo "GEN: $filename"
  curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/$voice_id" \
    -H "xi-api-key: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"text\":\"$text\",\"model_id\":\"$MODEL\",\"voice_settings\":{\"stability\":0.5,\"similarity_boost\":0.75,\"style\":0.3}}" \
    -o "$outfile"
  sleep 0.5
}

# VOICE IDs
NARRATOR="Xb7hH8MSUJpSbSDYk0k2"
ISLA="MUzMONRCyBSA0l61GzC2"
PRIYA="Qs8eI0FA8ZWoy7VJQK0C"
ZOE="x6KItt3dczXfR55FonpL"
AMARA="uOwZUqvORJmMLzgFFB5A"

# ── CHAPTER 1 ──────────────────────────────────────────────
generate "$NARRATOR" "ch1-intro.mp3" "The girls stepped through the door. The library disappeared behind them. All around them, glowing trees and floating lights filled the air."
generate "$AMARA" "ch1-amara-beautiful.mp3" "It is beautiful."
generate "$NARRATOR" "ch1-priya-stares.mp3" "Priya stared at the lights. Something about them felt familiar. The compass hummed softly in Zoe's hand. It was pointing deeper into the forest."
generate "$NARRATOR" "ch1-q1-question.mp3" "Look at the lights. They flash in a pattern. Two, four, six, eight. What comes next?"

# ── CHAPTER 2 ──────────────────────────────────────────────
generate "$PRIYA" "ch2-priya-stop.mp3" "Stop. Look at the lights."
generate "$NARRATOR" "ch2-groups.mp3" "They pulsed in groups. Two at a time. Then five at a time."
generate "$PRIYA" "ch2-priya-pattern.mp3" "It is a pattern! They are counting!"
generate "$ISLA" "ch2-isla-what.mp3" "Counting what?"
generate "$PRIYA" "ch2-priya-follow.mp3" "I do not know yet. But if we follow the pattern, maybe we find out."
generate "$NARRATOR" "ch2-compass-twitch.mp3" "She started counting along with the lights. The compass needle twitched. It was responding."
generate "$NARRATOR" "ch2-q2-question.mp3" "The lights flash again. Ten, twelve, fourteen, blank, eighteen. What is missing?"
generate "$NARRATOR" "ch2-q3-intro.mp3" "Now the lights change. They pulse in a new pattern."
generate "$NARRATOR" "ch2-q3-question.mp3" "Five, ten, fifteen, blank, twenty-five. What number is missing?"
generate "$NARRATOR" "ch2-q4-intro.mp3" "Another group of lights begins to pulse."
generate "$NARRATOR" "ch2-q4-question.mp3" "Thirty, thirty-five, blank, forty-five, fifty. What number is missing?"

# ── CHAPTER 3 ──────────────────────────────────────────────
generate "$NARRATOR" "ch3-intro.mp3" "The path ended at a glowing river. Stepping stones crossed to the other side. Each stone had a number on it. But some numbers were missing."
generate "$ZOE" "ch3-zoe-step.mp3" "We have to step on the right stones. In the right order."
generate "$ISLA" "ch3-isla-or-what.mp3" "Or what?"
generate "$NARRATOR" "ch3-red-water.mp3" "The water glowed an ominous red below the wrong stones."
generate "$AMARA" "ch3-amara-nope.mp3" "Let us not find out."
generate "$NARRATOR" "ch3-q5-question.mp3" "The stones count by tens. Ten, twenty, blank, forty, fifty. Which stone is missing?"
generate "$NARRATOR" "ch3-q6-intro.mp3" "They cross the first row. A second row of stones stretches ahead."
generate "$NARRATOR" "ch3-q6-question.mp3" "Forty, fifty, sixty, blank, eighty. Which stone is missing?"
generate "$NARRATOR" "ch3-q7-intro.mp3" "One last row stands between them and the other side."
generate "$NARRATOR" "ch3-q7-question.mp3" "Twenty-two, twenty-four, twenty-six, blank, thirty. Which stone is missing?"

# ── CHAPTER 4 ──────────────────────────────────────────────
generate "$NARRATOR" "ch4-intro.mp3" "They made it across. The path led to a huge stone door. Carved into it was a row of circles, like a number line. Isla tried to push the door. It did not move."
generate "$NARRATOR" "ch4-rumble.mp3" "Then, a rumble. The river behind them was rising. Water crept up the bank toward their feet."
generate "$PRIYA" "ch4-priya-fast.mp3" "The door needs patterns! Fast! The river is rising!"

# Speed round questions
generate "$NARRATOR" "sr-q1-question.mp3" "Zero, ten, twenty, blank, forty. What is missing?"
generate "$NARRATOR" "sr-q2-question.mp3" "Fifteen, twenty, twenty-five, blank. What comes next?"
generate "$NARRATOR" "sr-q3-question.mp3" "Six, eight, ten, blank. What comes next?"
generate "$NARRATOR" "sr-q4-question.mp3" "Fifty, sixty, blank, eighty. What is missing?"
generate "$NARRATOR" "sr-q5-question.mp3" "Thirty-five, forty, blank, fifty. What is missing?"

# Chapter 4 ending (after speed round)
generate "$NARRATOR" "ch4-door-opens.mp3" "The door rumbled and swung open just in time. They tumbled through, laughing and breathless."

# ── CHAPTER 5 ──────────────────────────────────────────────
generate "$NARRATOR" "ch5-intro.mp3" "Cool mountain air rushed in. The compass spun and pointed upward. They looked up. The mountain was enormous."
generate "$NARRATOR" "ch5-steps.mp3" "Stone steps wound all the way to the top. Each step had a number carved into it, glowing faintly."
generate "$ISLA" "ch5-isla-climb.mp3" "We have to climb."
generate "$AMARA" "ch5-amara-laugh.mp3" "Of course she is."
generate "$NARRATOR" "ch5-q8-intro.mp3" "Before they begin to climb, the compass shows one more challenge."
generate "$NARRATOR" "ch5-q8-question.mp3" "Count by twos. Start at zero, finish at twenty. How many jumps is that?"

# ── CLIFFHANGER ──────────────────────────────────────────────
generate "$NARRATOR" "cliffhanger.mp3" "The door swung shut behind them. The mountain loomed above. Each step glowed with a number. The compass pointed straight up. And Isla was already climbing. To reach the crystal at the top, they would have to count every step. The adventure of The Crystal Compass was only getting bigger."

# ── WIN ──────────────────────────────────────────────────────
generate "$NARRATOR" "win.mp3" "Amazing work! You helped the girls cross the glowing forest, unlock the stone door, and reach the mountain. You are a skip counting superstar!"

# ── CORRECT EXPLANATIONS (all 10 questions) ─────────────────
generate "$NARRATOR" "q1-correct.mp3" "Yes! The lights count by twos. Two, four, six, eight, ten. You added two each time. Well done!"
generate "$NARRATOR" "q2-correct.mp3" "That is right! Ten, twelve, fourteen, sixteen, eighteen. Each number goes up by two. The missing one was sixteen!"
generate "$NARRATOR" "q3-correct.mp3" "Perfect! Five, ten, fifteen, twenty, twenty-five. You counted by fives. The missing number was twenty!"
generate "$NARRATOR" "q4-correct.mp3" "Excellent! Thirty, thirty-five, forty, forty-five, fifty. Counting by fives. The missing number was forty!"
generate "$NARRATOR" "q5-correct.mp3" "Well done! Ten, twenty, thirty, forty, fifty. Counting by tens. The missing stone was thirty!"
generate "$NARRATOR" "q6-correct.mp3" "Great job! Forty, fifty, sixty, seventy, eighty. Counting by tens. The missing stone was seventy!"
generate "$NARRATOR" "q7-correct.mp3" "Brilliant! Twenty-two, twenty-four, twenty-six, twenty-eight, thirty. Counting by twos. The missing stone was twenty-eight!"
generate "$NARRATOR" "q8-correct.mp3" "Amazing! Zero to twenty, counting by twos, takes exactly ten jumps. Zero, two, four, six, eight, ten, twelve, fourteen, sixteen, eighteen, twenty. That is ten steps!"

echo "All audio files generated!"
ls -la "$OUTDIR"/*.mp3 | wc -l
