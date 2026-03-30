#!/usr/bin/env python3
"""Generate all audio for Ocean Arc issues 1-4 using ElevenLabs TTS."""
import os, requests, time
from pathlib import Path

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
BASE = Path(__file__).parent
BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# Voice IDs
ERIC    = "cjVigY5qzO86Huf0OWal"   # narrator
JESSICA = "cgSgspJ2msm6clMCkdW9"   # Marina
BILL    = "pqHfZKP75CvOlQylNhV4"   # Elder Luma

ERIC_SETTINGS    = {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}
JESSICA_SETTINGS = {"stability": 0.55, "similarity_boost": 0.80, "style": 0.25, "use_speaker_boost": True}
BILL_SETTINGS    = {"stability": 0.65, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True}

MODEL = "eleven_turbo_v2_5"

def E(fname, text): return (fname, ERIC, ERIC_SETTINGS, text)
def J(fname, text): return (fname, JESSICA, JESSICA_SETTINGS, text)
def B(fname, text): return (fname, BILL, BILL_SETTINGS, text)

AUDIO = {
    "issue001": [
        # Chapter 1
        E("ch1-approach.mp3",
          "Marina pressed her nose against the cold porthole of the research sub. Outside, the ocean was endless midnight blue, so deep it seemed solid. Flick hovered beside her, antenna fins pointing straight up with curiosity. They had been diving for three hours when the signal found them."),
        E("ch1-city.mp3",
          "It began as a faint pattern of flashing lights, pulsing through the dark water. Flick's wing-tips flared bright cyan. This was no ordinary light. Marina checked her amber datapad. The pattern was repeating, and it was mathematical. She set a new course, following the signal."),
        E("ch1-arrival.mp3",
          "What appeared from the darkness took Marina's breath away. A city, built entirely from living coral, glowing in shades of orange and pink and teal. Streets of bioluminescent light, and creatures moving purposefully along them. The great Coralfolk city of Luminos. And it was sending a distress call."),
        E("ch1-q1-question.mp3",
          "The Coralfolk keep fish in equal groups. If there are two groups of fish pens, and each pen holds three fish, how many fish are there altogether?"),
        E("ch1-q1-answer.mp3",
          "Two groups of three equals six! Two equal groups of three fish makes six fish in total. That is multiplication, groups of equal size added together."),

        # Chapter 2
        E("ch2-intro.mp3",
          "A small creature approached the sub's airlock, moving with deliberate, measured steps. Its shell was deep burgundy-red, etched with geometric patterns. It carried a black coral staff topped with a glowing amber stone. This was Elder Luma, keeper of the Lattice."),
        B("ch2-luma.mp3",
          "You came. The Lattice sensed you were different, a mathematical mind. We have been sending distress signals for three tide-cycles, hoping someone would understand the pattern. Something is wrong with the Lattice, and I fear we cannot fix it alone."),
        E("ch2-lattice.mp3",
          "Elder Luma led Marina through the glowing streets of Luminos. The Coralfolk, small crab-like beings no taller than Marina's knee, stepped aside with respectful nods. Flick darted ahead, delighted by everything."),
        E("ch2-q2-question.mp3",
          "The Coralfolk keep their fish in separate pens. If there are four groups of pens, and each group holds two fish, how many fish altogether?"),
        E("ch2-q2-answer.mp3",
          "Four groups of two equals eight! Four equal groups with two fish each gives us eight fish. Count in twos, two, four, six, eight!"),
        E("ch2-q3-setup.mp3",
          "Elder Luma pointed to three large pens on the far side of the Lattice field. Each pen held exactly five fish, their scales catching the bioluminescent light."),
        E("ch2-q3-question.mp3",
          "How many fish are there in three groups of five?"),
        E("ch2-q3-answer.mp3",
          "Three groups of five equals fifteen! Count in fives, five, ten, fifteen. Three jumps of five gets you to fifteen!"),

        # Chapter 3
        E("ch3-intro.mp3",
          "Elder Luma sat beside the Lattice stones and explained how they worked. Each stone could send a signal to its neighbouring stones, and the number of neighbours it signalled was always the same. Equal groups, every time."),
        B("ch3-luma.mp3",
          "We call it the Ripple. One stone sends to three. Those three each send to three more. Always the same number. Always in equal groups. This is what makes the Lattice reliable. This is what has kept Luminos connected to all the other cities for a thousand tides."),
        J("ch3-marina.mp3",
          "So if every stone sends to the same number of other stones, the message spreads in a predictable pattern. Like multiplication. That is what you are using. Groups of the same size!"),
        E("ch3-q4-question.mp3",
          "If five groups of pens each hold exactly two fish, how many fish are there altogether?"),
        E("ch3-q4-answer.mp3",
          "Five groups of two equals ten! Count in twos, two, four, six, eight, ten. Five jumps of two gives you ten!"),
        E("ch3-q5-setup.mp3",
          "Marina spotted another section of fish pens nearby. There were two large groups, each holding six fish. Flick pointed at them with one glowing wing-tip."),
        E("ch3-q5-question.mp3",
          "How many fish are there in two groups of six?"),
        E("ch3-q5-answer.mp3",
          "Two groups of six equals twelve! Start at six, then add six more. Six plus six equals twelve!"),

        # Chapter 4
        E("ch4-intro.mp3",
          "Marina pulled up her amber wrist datapad and began making notes. Flick hovered at her shoulder, wing-tips pulsing with steady cyan light. Each stone in the Lattice sent its signal to four neighbouring stones, without exception."),
        E("ch4-datapad.mp3",
          "Four groups of four. Elder Luma watched Marina work through the numbers, nodding slowly."),
        B("ch4-luma.mp3",
          "You see it. The Ripple is built entirely from equal groups. Every calculation in the Lattice is multiplication. If you understand groups of, you understand everything about how Luminos works. And perhaps, how it can be repaired."),
        E("ch4-q6-question.mp3",
          "There are four groups of stones in one section of the Lattice. Each group has four stones. How many stones in this section altogether?"),
        E("ch4-q6-answer.mp3",
          "Four groups of four equals sixteen! Count in fours, four, eight, twelve, sixteen. Four jumps of four reaches sixteen Lattice stones!"),
        E("ch4-q7-setup.mp3",
          "The next Lattice section had three groups of stones, with six stones in each group. Marina marked them carefully on her datapad."),
        E("ch4-q7-question.mp3",
          "How many stones are there in three groups of six?"),
        E("ch4-q7-answer.mp3",
          "Three groups of six equals eighteen! Count in sixes, six, twelve, eighteen. Three jumps of six reaches eighteen!"),
        E("ch4-q8-setup.mp3",
          "The final section Marina checked had five groups of stones, each group holding exactly four stones. Flick's wing-tips pulsed in rhythm as Marina counted."),
        E("ch4-q8-question.mp3",
          "How many stones in five groups of four?"),
        E("ch4-q8-answer.mp3",
          "Five groups of four equals twenty! Count in fours, four, eight, twelve, sixteen, twenty. Five jumps of four gives you twenty!"),

        # Chapter 5
        E("ch5-intro.mp3",
          "Then something changed. A vibration moved through the ocean floor. Not a sound exactly, more of a feeling, a deep and rhythmic pulse that Marina felt in her chest before she heard it with her ears. The Lattice stones began to flicker. The Coralfolk around them froze, antenna fins pressed flat against their shells."),
        B("ch5-hum.mp3",
          "The Hum. It has begun again. Something enormous is down there, in the deep water below the Lattice floor. We do not know what it is. We have not seen it. But we can feel it."),
        E("ch5-luma.mp3",
          "Marina stared down at the flickering stones. Her datapad was full of calculations. She understood groups of now. But whatever was making that hum, down in the darkness, she had a feeling the real work was just beginning."),
        E("ch5-q9-question.mp3",
          "While the Lattice flickers, Marina works quickly. In two groups of stones that still work, there are seven stones in each group. How many working stones are there?"),
        E("ch5-q9-answer.mp3",
          "Two groups of seven equals fourteen! Think, seven plus seven equals fourteen. Two groups of seven!"),
        E("ch5-q10-setup.mp3",
          "A smaller cluster of stones glows steadily nearby. There are three groups, each holding three stones. The very last section to check before the hum gets louder."),
        E("ch5-q10-question.mp3",
          "How many stones in three groups of three?"),
        E("ch5-q10-answer.mp3",
          "Three groups of three equals nine! Count in threes, three, six, nine. Three jumps of three gets you to nine!"),
        E("ch5-cliffhanger.mp3",
          "Marina stared into the dark water below the Lattice floor. Deep, deep below, in water so black it had no bottom, something was moving. A faint rhythmic glow pulsed in the blackness. Not random. Not scattered. Arranged in a pattern. Like rows. Like groups. Like something that understood mathematics. Enormous. Patient. Ancient. Elder Luma, Marina whispered, I think whatever is down there, it is not broken. I think it is trying to communicate. The hum deepened. The Lattice stones flickered once more. And far, far below, the glow pulsed on."),

        # Shared feedback audio (copy from sounds/jungle/issue007)
        E("feedback-correct-1.mp3",
          "Pre-launch check passed!"),
        E("feedback-correct-2.mp3",
          "Great work!"),
        E("feedback-correct-3.mp3",
          "Brilliant!"),
        E("feedback-correct-4.mp3",
          "Excellent!"),
        E("feedback-correct-5.mp3",
          "Fantastic!"),
        E("feedback-correct-6.mp3",
          "Amazing!"),
        E("feedback-wrong-1.mp3",
          "Not quite, try again!"),
        E("feedback-wrong-2.mp3",
          "Hmm, have another go!"),
        E("win.mp3",
          "Mission complete! The Lattice of Luminos thanks you!"),
    ],

    "issue002": [
        # Chapter 1
        E("ch1-intro.mp3",
          "The next morning, Elder Luma sent a guide. Wren was young for a Coralfolk keeper, nervous and eager, the amber patterns on her shell still bright and unfaded. She led Marina and Flick out through the edge of Luminos and into the vast open fields of the outer Lattice."),
        E("ch1-outer.mp3",
          "Out here, the ocean floor was almost flat. Row after row of glowing signal stones stretched as far as Marina could see, arranged in a grid that disappeared into the dark water ahead. Flick darted between the rows, antenna fins pointing in every direction at once."),
        B("ch1-wren.mp3",
          "The Lattice is largest out here. We count the stones by skipping. It is the fastest way, and the way that matches how the signal travels. You will see."),
        E("ch1-q1-question.mp3",
          "Wren counts every second stone. The pattern starts, two, four, six, then two blanks. What are the next two numbers?"),
        E("ch1-q1-answer.mp3",
          "Eight and ten! Counting by twos, two, four, six, eight, ten. The pattern goes up by two each time!"),

        # Chapter 2
        E("ch2-intro.mp3",
          "Wren moved along the first row of stones, touching every second one. Marina matched her step for step."),
        B("ch2-wren.mp3",
          "When you count by twos, you are not just skipping. You are counting groups of two. Five skips is five groups of two. Five times two."),
        J("ch2-marina.mp3",
          "So skip counting is multiplication. Counting by fives is the same as multiplying by five. Counting by tens is multiplying by ten."),
        E("ch2-q2-question.mp3",
          "Wren counts by twos, two, four, six, eight, ten. That is five skips of two, or five times two. What is five times two?"),
        E("ch2-q2-answer.mp3",
          "Five times two equals ten! Five jumps of two gets you to ten. Skip counting by twos five times!"),
        E("ch2-q3-setup.mp3",
          "The next section of stones was arranged in groups of five. Wren began counting, five, ten, fifteen, then paused, letting Marina fill in the rest."),
        E("ch2-q3-question.mp3",
          "Count by fives, five, ten, fifteen, then two blanks. What are the next two numbers?"),
        E("ch2-q3-answer.mp3",
          "Twenty and twenty-five! Counting by fives, five, ten, fifteen, twenty, twenty-five. Each step jumps by five!"),

        # Chapter 3
        E("ch3-intro.mp3",
          "The outer field opened up into the largest section of all. The stones here stretched on and on, arranged in long rows of ten. Marina craned her neck to see the far end, but the glow simply faded into dark water in the distance."),
        B("ch3-wren.mp3",
          "This is the main transmission grid. Thousands of stones, in groups of ten. We count by tens out here because a single signal can jump ten stones at once."),
        J("ch3-marina.mp3",
          "Marina knelt down to study her datapad. Groups of ten were easy to count. Ten, twenty, thirty. The signal would be easy to track. But something in the pattern looked wrong. Three sections were glowing steadily, but the fourth was dark. Something was interrupting the flow."),
        E("ch3-q4-question.mp3",
          "Marina checks a section with stones in groups of five. There are four groups. What is four times five?"),
        E("ch3-q4-answer.mp3",
          "Four times five equals twenty! Count in fives, five, ten, fifteen, twenty. Four jumps of five gets you to twenty!"),
        E("ch3-q5-setup.mp3",
          "Marina looks at the main transmission grid. Groups of ten stretch ahead. She counts by tens, ten, twenty, then three blanks. How far does the signal reach across this section?"),
        E("ch3-q5-question.mp3",
          "Count by tens, ten, twenty, then three blanks. What are the next three numbers?"),
        E("ch3-q5-answer.mp3",
          "Thirty, forty, fifty! Count by tens, ten, twenty, thirty, forty, fifty. Each jump adds ten!"),

        # Chapter 4
        E("ch4-intro.mp3",
          "Marina's wrist datapad mapped the fault line. The disruption started at a specific cluster of stones, and the skip-count pattern broke there. Instead of jumping by tens, the signal was jumping by irregular amounts. Something down below was throwing it off."),
        E("ch4-datapad.mp3",
          "Flick pressed close to Wren, wing-tips flaring with concern. Wren reached out a small three-fingered hand and patted Flick's underbelly. It helped a little."),
        J("ch4-marina.mp3",
          "We can work out how many stones should be active in each section. If I know the number of groups and how many in each group, I can calculate the total and compare it to what's actually glowing. That will show us exactly where the fault is."),
        E("ch4-q6-question.mp3",
          "Marina checks a section with three groups of ten stones each. What is three times ten?"),
        E("ch4-q6-answer.mp3",
          "Three times ten equals thirty! Think, ten, twenty, thirty. Three jumps of ten gets you to thirty!"),
        E("ch4-q7-setup.mp3",
          "Marina finds a section with six groups, each group containing two stones. She marks it on her datapad."),
        E("ch4-q7-question.mp3",
          "How many stones in six times two?"),
        E("ch4-q7-answer.mp3",
          "Six times two equals twelve! Count in twos six times, two, four, six, eight, ten, twelve. Six jumps of two reaches twelve!"),
        E("ch4-q8-setup.mp3",
          "The next section, seven groups of five stones each. Wren marks the glow pattern while Marina calculates."),
        E("ch4-q8-question.mp3",
          "How many stones in seven times five?"),
        E("ch4-q8-answer.mp3",
          "Seven times five equals thirty-five! Count in fives, five, ten, fifteen, twenty, twenty-five, thirty, thirty-five. Seven jumps of five reaches thirty-five!"),

        # Chapter 5
        E("ch5-intro.mp3",
          "Marina was mid-calculation when the light changed. The filtered shafts of blue that reached down from the surface, far above, dimmed suddenly. A shadow moved across the ocean floor. Enormous. Silent. Moving slowly and deliberately from east to west."),
        E("ch5-shadow.mp3",
          "Flick went completely still. Even Flick's antenna fins were flat against its body. Wren pressed herself against a nearby stone and did not move."),
        E("ch5-freeze.mp3",
          "The shadow passed. The light returned. Marina released a breath she had not known she was holding. Then the shadow came back."),
        E("ch5-q9-question.mp3",
          "While waiting for the shadow to pass, Marina calculates one more section, nine groups of two stones. What is nine times two?"),
        E("ch5-q9-answer.mp3",
          "Nine times two equals eighteen! Count in twos all the way up, two, four, six, eight, ten, twelve, fourteen, sixteen, eighteen. Nine jumps of two reaches eighteen!"),
        E("ch5-q10-setup.mp3",
          "The last calculation on Marina's datapad, the main transmission grid fault spans eight groups of ten stones. That is the size of the disruption."),
        E("ch5-q10-question.mp3",
          "The fault zone spans eight groups of ten stones each. What is eight times ten?"),
        E("ch5-q10-answer.mp3",
          "Eight times ten equals eighty! Count in tens, ten, twenty, thirty, forty, fifty, sixty, seventy, eighty. Eight jumps of ten reaches eighty!"),
        E("ch5-cliffhanger.mp3",
          "Marina and Wren stood frozen, both of them looking upward. The shadow had come back. Larger this time, or perhaps closer. It moved with slow, deliberate patience, blotting out the filtered light until the ocean floor around them was near-black. Wren, Marina said, very quietly, what kind of creature makes a shadow that big? Wren was silent for a long moment. When she finally spoke, her voice was barely above a whisper. In all my lifetimes of working the Lattice, and all the records of all the keepers before me, nothing that size has ever been seen. Not once. Not in living memory. The shadow passed. Below the ocean floor, the deep rhythmic hum continued, patient as a heartbeat."),

        E("feedback-correct-1.mp3", "Pre-launch check passed!"),
        E("feedback-correct-2.mp3", "Great work!"),
        E("feedback-correct-3.mp3", "Brilliant!"),
        E("feedback-correct-4.mp3", "Excellent!"),
        E("feedback-correct-5.mp3", "Fantastic!"),
        E("feedback-correct-6.mp3", "Amazing!"),
        E("feedback-wrong-1.mp3", "Not quite, try again!"),
        E("feedback-wrong-2.mp3", "Hmm, have another go!"),
        E("win.mp3", "Excellent work! The skip-count pattern is cracked!"),
    ],

    "issue003": [
        # Chapter 1
        E("ch1-intro.mp3",
          "Elder Luma led Marina through the deep water beyond Luminos, to a place where an ancient shipwreck rested on the ocean floor. The ship was enormous, half-buried, its wooden beams encrusted with hundreds of years of coral growth."),
        E("ch1-archive.mp3",
          "Inside, teal and gold light filtered through the open portholes and broken hull, casting long patterns across a grid of glowing stone tablets."),
        B("ch1-luma.mp3",
          "The Archive. We have kept records here since before any Coralfolk alive can remember. Every event of importance in the Luminous Deep is stored on a stone tablet and placed in this grid. To find any record, you navigate by rows and columns."),
        E("ch1-q1-question.mp3",
          "The Archive entrance has a small grid of stone tablets arranged in three rows with four tablets in each row. How many tablets altogether?"),
        E("ch1-q1-answer.mp3",
          "Three rows of four equals twelve. Three rows with four tablets in each row gives twelve tablets altogether!"),

        # Chapter 2
        E("ch2-intro.mp3",
          "Marina ran her hand along the first row of tablets. Four tablets. She counted the rows. Three. Twelve tablets in this section. Then she tilted her head and looked at it differently. What if she counted the columns instead? Three tablets per column. Four columns. Still twelve."),
        B("ch2-luma.mp3",
          "You found it. The Coralfolk have known this for a thousand tides. We call it the Mirror Truth. Three rows of four is the same count as four rows of three. The grid does not change, only the direction you read it. This is why the Lattice is so reliable. You can always check your count by turning it around."),
        J("ch2-marina.mp3",
          "So three times four equals four times three. They are always the same. It does not matter which order you multiply."),
        E("ch2-q2-question.mp3",
          "The same grid, read in a different direction, four rows with three tablets in each row. How many tablets altogether?"),
        E("ch2-q2-answer.mp3",
          "The Mirror Truth! Four rows of three also equals twelve. The grid is the same, just read from a different direction."),
        E("ch2-q3-setup.mp3",
          "Marina moves to a deeper section of the Archive. The grid here has two rows with seven tablets in each row. She reads them left to right."),
        E("ch2-q3-question.mp3",
          "How many tablets in two rows of seven?"),
        E("ch2-q3-answer.mp3",
          "Two rows of seven equals fourteen! Think, seven tablets in row one, plus seven more in row two. Seven plus seven equals fourteen."),

        # Chapter 3
        E("ch3-intro.mp3",
          "They moved deeper into the Archive, past grid after grid of stone tablets. Elder Luma navigated by memory, counting rows and columns under his breath. The light here was dimmer, the colour shifting to deep gold where the teal bioluminescence could not reach."),
        B("ch3-luma.mp3",
          "The record we need is in the seventh section. Section seven has five rows and three columns. Count to the third row, second column. That is where we find records of things that have never been seen before."),
        J("ch3-marina.mp3",
          "Marina used her datapad to navigate. Rows and columns, like a map. Like the Lattice, but made of knowledge instead of light. She worked through each section systematically, calculating the total tablets as she went to keep track of her position."),
        E("ch3-q4-question.mp3",
          "Now read the same two-rows-of-seven grid as columns. Seven rows with two tablets in each row. How many tablets?"),
        E("ch3-q4-answer.mp3",
          "Mirror Truth again! Seven rows of two also equals fourteen. The total never changes, only the direction you count."),
        E("ch3-q5-setup.mp3",
          "Section four of the Archive, five rows of three tablets each. Marina checks her count before moving on."),
        E("ch3-q5-question.mp3",
          "How many tablets in five rows of three?"),
        E("ch3-q5-answer.mp3",
          "Five rows of three equals fifteen! Count in threes, three, six, nine, twelve, fifteen. Five jumps of three reaches fifteen!"),

        # Chapter 4
        E("ch4-intro.mp3",
          "The tablet Elder Luma had described glowed faintly with ancient light. Marina read the old-script characters while Elder Luma translated in a low, careful voice. The record described a creature. Vast beyond imagining. Dark body, patterned with bioluminescent spots arranged in rows and columns."),
        B("ch4-luma.mp3",
          "The Resonance Whale. It last appeared seven hundred tides ago. The record says the Lattice failed completely for three tide-cycles while the Whale rested in the deep trench. The Coralfolk could do nothing until it left of its own accord."),
        J("ch4-marina.mp3",
          "Wait. This says the Whale's spots are arranged in grids. Rows and columns. The same pattern as the Lattice. Maybe there is a way to communicate with it."),
        E("ch4-q6-question.mp3",
          "The same section, read the other way, three rows of five tablets each. How many tablets?"),
        E("ch4-q6-answer.mp3",
          "Three rows of five also equals fifteen. That is the Mirror Truth in action!"),
        E("ch4-q7-setup.mp3",
          "Another section of the Archive records important grid patterns. This one has four rows of six tablets each."),
        E("ch4-q7-question.mp3",
          "How many tablets in four rows of six?"),
        E("ch4-q7-answer.mp3",
          "Four rows of six equals twenty-four! Count in sixes, six, twelve, eighteen, twenty-four. Four jumps of six reaches twenty-four!"),
        E("ch4-q8-setup.mp3",
          "And the Mirror Truth, the same grid of twenty-four tablets, read as six rows of four tablets each. The total never changes, only the direction."),
        E("ch4-q8-question.mp3",
          "How many tablets in six rows of four?"),
        E("ch4-q8-answer.mp3",
          "Six rows of four also equals twenty-four! Same grid, same total, different direction."),

        # Chapter 5
        E("ch5-intro.mp3",
          "Elder Luma read in silence for a long time. Marina waited, running calculations on her datapad. The Whale's spots were arranged in grids, five rows of five. That was twenty-five spots per cluster. And each cluster pulsed. The pulse was the signal."),
        J("ch5-marina.mp3",
          "If we could match the Whale's own pattern, and send it back to the Whale through the Lattice stones, perhaps the Whale would understand it as a greeting. Not a threat. Not interference. A greeting."),
        E("ch5-luma.mp3",
          "Elder Luma looked at her for a long moment. Then he looked at the porthole in the side of the shipwreck. Marina followed his gaze."),
        E("ch5-q9-question.mp3",
          "The Whale's bioluminescent spots are arranged in a grid, five rows of five spots each per cluster. How many spots in one cluster?"),
        E("ch5-q9-answer.mp3",
          "Five rows of five equals twenty-five! Five by five is a perfect square array, twenty-five spots per cluster."),
        E("ch5-q10-setup.mp3",
          "One last array in the Archive record, the Whale's largest spot grid, used for long-distance signalling. The old record shows three rows of eight spots each."),
        E("ch5-q10-question.mp3",
          "The Whale's long-distance spot grid, three rows of eight spots. How many spots altogether?"),
        E("ch5-q10-answer.mp3",
          "Three rows of eight equals twenty-four! Count in eights, eight, sixteen, twenty-four. Three jumps of eight reaches twenty-four!"),
        E("ch5-cliffhanger.mp3",
          "The old porthole of the shipwreck lit up. Not with filtered surface light. With bioluminescence. Blue-green and patterned, moving in slow deliberate pulses. A vast fin passed the glass, so large it blocked out the entire porthole for three long seconds. And then the spots. Rows of them. Columns of them. The same grid pattern Marina had just been reading from the ancient record. Alive. Present. Right outside the window. Marina pressed her palm against the glass. The bioluminescent spots pulsed once in response. Elder Luma, she whispered, it can see us. Elder Luma was completely still. He said nothing. But his amber eyes held something Marina had not seen in them before. Not worry. Hope."),

        E("feedback-correct-1.mp3", "Pre-launch check passed!"),
        E("feedback-correct-2.mp3", "Great work!"),
        E("feedback-correct-3.mp3", "Brilliant!"),
        E("feedback-correct-4.mp3", "Excellent!"),
        E("feedback-correct-5.mp3", "Fantastic!"),
        E("feedback-correct-6.mp3", "Amazing!"),
        E("feedback-wrong-1.mp3", "Not quite, try again!"),
        E("feedback-wrong-2.mp3", "Hmm, have another go!"),
        E("win.mp3", "The Archive has revealed its secrets! Excellent work!"),
    ],

    "issue004": [
        # Chapter 1
        E("ch1-intro.mp3",
          "Marina and Flick descended beyond the Lattice floor, into the deep trench below. The light from Luminos faded. The ocean became a kind of black that felt almost solid. Flick's wing-tips were the only light, pulsing steady cyan in the dark."),
        E("ch1-descent.mp3",
          "They had been descending for twenty minutes when they saw the first sign. A faint blue-green glow, far below. Arranged in rows. In columns. Like an array but alive, moving slowly, rhythmically."),
        E("ch1-glow.mp3",
          "Pulsing. The same pattern Marina had read about in the Archive. The same pattern on the tablet outside the shipwreck window."),
        E("ch1-q1-question.mp3",
          "Marina sees the first cluster of the Whale's bioluminescent spots. There are three rows with six spots in each row. What is three times six?"),
        E("ch1-q1-answer.mp3",
          "Three times six equals eighteen! Count in sixes, six, twelve, eighteen. Three jumps of six gets you to eighteen!"),

        # Chapter 2
        E("ch2-reveal.mp3",
          "Then the whole Whale came into view. It was enormous in a way Marina had never experienced. Not big the way a large ship is big, where you can see the whole of it at once. Big the way a mountain is big, where it keeps going even when you think it should stop."),
        E("ch2-whale.mp3",
          "Dark charcoal grey, nearly black, covered from fin-tip to tail in glowing blue-green spots arranged in perfect grids. Its eyes, large as Marina's entire sub, were gentle and violet-dark and looking directly at her."),
        E("ch2-flick.mp3",
          "Flick did not run. Flick hovered perfectly still, wing-tips glowing at their steadiest, most serene. Marina felt the deep rhythmic pulse of the Whale's bioelectric field through the water. Not threatening. Not angry. Just present. Bewildered. Ancient. Lonely."),
        E("ch2-q2-question.mp3",
          "Marina counts a section of the Whale's spots, five rows of six. What is five times six?"),
        E("ch2-q2-answer.mp3",
          "Five times six equals thirty! Count in sixes, six, twelve, eighteen, twenty-four, thirty. Five jumps of six reaches thirty!"),
        E("ch2-q3-setup.mp3",
          "On the Whale's left flank, Marina counts another spot section. This section has four rows with seven spots in each row."),
        E("ch2-q3-question.mp3",
          "How many spots in four times seven?"),
        E("ch2-q3-answer.mp3",
          "Four times seven equals twenty-eight! Count in sevens, seven, fourteen, twenty-one, twenty-eight. Four jumps of seven gets you to twenty-eight!"),

        # Chapter 3
        E("ch3-intro.mp3",
          "Marina had her datapad out now, recording the pulse pattern. The Whale's bioelectric field was not random. It pulsed in sequences. Groups of six, then seven, then eight. Over and over. The same multiplication pattern cycling through, like a song that kept repeating."),
        J("ch3-marina.mp3",
          "It is not disrupting the Lattice on purpose. It woke up and felt the Lattice field, and its own field interacted with it. The Whale does not understand why the stones are dark. It is confused and distressed and it keeps sending its own signal louder, trying to get an answer."),
        E("ch3-flick.mp3",
          "Flick drifted toward the Whale, antenna fins up, wing-tips at their gentlest cyan. The Whale's great eye tracked Flick with something that looked very much like curiosity."),
        E("ch3-q4-question.mp3",
          "Marina identifies the Whale's central pulse cluster, six rows of seven spots. What is six times seven?"),
        E("ch3-q4-answer.mp3",
          "Six times seven equals forty-two! Count in sevens, seven, fourteen, twenty-one, twenty-eight, thirty-five, forty-two. Six jumps of seven reaches forty-two!"),
        E("ch3-q5-setup.mp3",
          "The pulse shifts to the eight-pattern. Marina sees a section with three rows of eight spots each. This section pulses brightest when the Whale seems most distressed."),
        E("ch3-q5-question.mp3",
          "How many spots in three times eight?"),
        E("ch3-q5-answer.mp3",
          "Three times eight equals twenty-four! Count in eights, eight, sixteen, twenty-four. Three jumps of eight gets you to twenty-four!"),

        # Chapter 4
        E("ch4-intro.mp3",
          "Marina worked fast. Her datapad captured the Whale's full pulse sequence. Flick, bonded to the datapad, could carry the signal to the right Lattice stones. But first Marina had to calculate exactly which stone groupings needed to light up, and in what sequence."),
        J("ch4-marina.mp3",
          "Flick, I need you to be brave. I need you to carry this signal up through the water, to the Lattice field above us, and pulse it to the right stones. In the right pattern. Exactly as I calculate it."),
        E("ch4-flick.mp3",
          "Flick's antenna fins pointed straight up. Wing-tips pulsed cyan once, firmly. Ready."),
        E("ch4-q6-question.mp3",
          "To recalibrate the Lattice, Marina needs to match the signal to five rows of eight stones pulsing at once. What is five times eight?"),
        E("ch4-q6-answer.mp3",
          "Five times eight equals forty! Count in eights, eight, sixteen, twenty-four, thirty-two, forty. Five jumps of eight reaches forty!"),
        E("ch4-q7-setup.mp3",
          "The second part of the signal sequence, seven groups of six stones need to activate in the next pulse. Marina writes the calculation quickly."),
        E("ch4-q7-question.mp3",
          "What is seven times six?"),
        E("ch4-q7-answer.mp3",
          "Seven times six equals forty-two! Count in sixes, six, twelve, eighteen, twenty-four, thirty, thirty-six, forty-two. Seven jumps of six reaches forty-two!"),
        E("ch4-q8-setup.mp3",
          "The third part of the signal, four groups of eight stones. This is the part that matches the Whale's strongest pulse. Marina checks the calculation twice."),
        E("ch4-q8-question.mp3",
          "What is four times eight?"),
        E("ch4-q8-answer.mp3",
          "Four times eight equals thirty-two! Count in eights, eight, sixteen, twenty-four, thirty-two. Four jumps of eight gets you to thirty-two!"),

        # Chapter 5
        E("ch5-intro.mp3",
          "Flick went. Not fast, not reckless, but with a purpose Marina had never seen in the little manta ray before. Up through the dark water, carrying the calculated signal, wing-tips burning cyan brighter than Marina had ever seen them."),
        E("ch5-flick.mp3",
          "The Lattice stones began to light up. One section, then the next, then the next, spreading out across the ocean floor in the exact pattern Marina had calculated. And as the Lattice came back to life, its light reached down into the trench below."),
        E("ch5-lattice.mp3",
          "The Whale went still. Its bioelectric pulse slowed. Marina watched its great eye move across the newly glowing Lattice field, reading the pattern Flick had carried up. Then the Whale's spots changed colour. Warmer. Softer. And the deep rhythmic hum faded to silence."),
        E("ch5-q9-question.mp3",
          "The Lattice reactivation ripple spreads through six groups of six stones at a time. What is six times six?"),
        E("ch5-q9-answer.mp3",
          "Six times six equals thirty-six! Count in sixes, six, twelve, eighteen, twenty-four, thirty, thirty-six. Six jumps of six reaches thirty-six!"),
        E("ch5-q10-setup.mp3",
          "The last calculation, the Whale's farewell pattern. Eight groups of seven spots. This is the pattern that means it is leaving peacefully."),
        E("ch5-q10-question.mp3",
          "The Whale's farewell pattern, eight groups of seven spots. What is eight times seven?"),
        E("ch5-q10-answer.mp3",
          "Eight times seven equals fifty-six! Count in sevens all the way, seven, fourteen, twenty-one, twenty-eight, thirty-five, forty-two, forty-nine, fifty-six. Eight jumps of seven reaches fifty-six!"),
        E("ch5-finale.mp3",
          "When Marina and Flick surfaced back into Luminos, every Lattice stone in the city was glowing at full brightness. The Coralfolk lined the streets, hundreds of them, their shells reflecting amber and teal light in every direction. They did not cheer the way humans cheer. They communicated through the Lattice, rippling bioluminescent patterns from stone to stone, from city to city across the whole of the Luminous Deep. A celebration that could be felt for a thousand tide-lengths in every direction. Elder Luma was waiting at the entrance. He held something in one small three-fingered hand. A single signal stone, warm amber, glowing steadily. This stone, he said, is tuned to the Lattice of Luminos. When you need us, hold it and send the pattern. We will know it is you. We will know you understand the Ripple. Marina took the stone carefully. Flick pressed close against her side, antenna fins up, wing-tips pulsing in the steadiest, most contented pattern Marina had ever seen. Thank you, Elder Luma, she said. For trusting me. Elder Luma turned and walked back into the city, staff tapping on the coral floor. Somewhere, far below, the Whale continued its journey into deeper water. Its hum faded to nothing. And the Lattice glowed on, steady and true."),

        E("feedback-correct-1.mp3", "Pre-launch check passed!"),
        E("feedback-correct-2.mp3", "Great work!"),
        E("feedback-correct-3.mp3", "Brilliant!"),
        E("feedback-correct-4.mp3", "Excellent!"),
        E("feedback-correct-5.mp3", "Fantastic!"),
        E("feedback-correct-6.mp3", "Amazing!"),
        E("feedback-wrong-1.mp3", "Not quite, try again!"),
        E("feedback-wrong-2.mp3", "Hmm, have another go!"),
        E("win.mp3", "Arc complete! The Lattice of Luminos is restored! You are a true Mathematical Explorer!"),
    ],
}

def generate_audio(voice_id, voice_settings, text, out_path):
    if out_path.exists():
        print(f"  SKIP (exists): {out_path.name}")
        return True
    print(f"  GEN: {out_path.name}")
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": text,
        "model_id": MODEL,
        "voice_settings": voice_settings
    }
    url = f"{BASE_URL}/{voice_id}"
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        if r.status_code == 429:
            print(f"  RATE LIMIT, waiting 30s...")
            time.sleep(30)
            r = requests.post(url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(r.content)
        print(f"  OK: {out_path.name} ({len(r.content):,} bytes)")
        return True
    except Exception as e:
        print(f"  ERROR {out_path.name}: {e}")
        return False

if __name__ == "__main__":
    total = sum(len(v) for v in AUDIO.values())
    done = 0
    errors = []
    for issue, items in AUDIO.items():
        print(f"\n=== {issue.upper()} ===")
        audio_dir = BASE / "audio" / "ocean" / issue
        audio_dir.mkdir(parents=True, exist_ok=True)
        for fname, voice_id, voice_settings, text in items:
            out_path = audio_dir / fname
            ok = generate_audio(voice_id, voice_settings, text, out_path)
            done += 1
            if not ok:
                errors.append(f"{issue}/{fname}")
            time.sleep(0.5)  # be gentle with the API
    print(f"\n=== DONE: {done}/{total} ===")
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
