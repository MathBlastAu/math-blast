#!/usr/bin/env python3
"""Generate all narration audio for Issues 2-7 of the Space Fractions arc."""

import os, json, time, urllib.request, urllib.error

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
MODEL   = "eleven_turbo_v2_5"
BASE    = "/Users/leohiem/.openclaw/workspace/projects/math-blast/sounds"

GEORGE = "JBFqnCBsd6RMkjVDRZzb"
ANDREW = "BTEPH6wbWkb66Dys0ry6"
RIVER  = "SAz9YHcvj6GT2YYXdXww"

NAR   = {"stability": 0.55, "similarity_boost": 0.75}
JAKE  = {"stability": 0.50, "similarity_boost": 0.78}
ALIEN = {"stability": 0.18, "similarity_boost": 0.32, "style": 0.85}

def seg(f, v, s, t): return (f, v, s, t)
G = lambda f, t: seg(f, GEORGE, NAR, t)
J = lambda f, t: seg(f, ANDREW, JAKE, t)
A = lambda f, t: seg(f, RIVER, ALIEN, t)

ISSUES = {

# ══════════════════════════════════════════════════════
# ISSUE 2 — Fractions in the Fog Nebula
# ══════════════════════════════════════════════════════
"issue002": [
    G("ch1-intro.mp3", "Jake's instruments were going haywire. The Vela Fog Nebula swallowed his rocket like a cloud swallowing a moth. Visibility: zero. But his math-based instruments — those still worked perfectly."),
    G("ch1-q1-question.mp3", "The nebula is divided into 6 equal sectors. Jake has already passed through 2. What fraction of the nebula has he crossed?"),
    G("ch1-q2-story.mp3", "Deep in the fog, a faint signal crackled through the comms. It was the SS Meridian — stranded, fuel almost gone, crew rationing every last drop."),
    A("ch1-meridian.mp3", "Mayday, mayday! This is the SS Meridian. Our fuel tank has 5 equal sections. Only 2 remain. We cannot hold much longer!"),
    G("ch1-q2-question.mp3", "The Meridian's tank has 5 equal sections and 2 are left. What fraction of fuel do they have remaining?"),

    G("ch2-intro.mp3", "Jake punched in the coordinates and boosted toward the signal. He had to think fast — the Meridian was losing fuel by the minute."),
    A("ch2-meridian.mp3", "We will need to use one more section just to reach the rendezvous point. How much will we have left after that?"),
    G("ch2-q3-question.mp3", "The Meridian has 2 fifths of fuel. They use 1 section to reach Jake. What fraction is left?"),
    G("ch2-q4-story.mp3", "As Jake drew closer, his scanner picked up something incredible — a cloud of spare fuel pods, floating free in the nebula. Twelve of them, perfectly intact."),
    J("ch2-jake.mp3", "Twelve pods! If I split them equally with the Meridian, we each get half. But how many is that exactly?"),
    G("ch2-q4-question.mp3", "Jake finds 12 spare fuel pods and shares them equally with the Meridian. Half of 12 equals how many pods each?"),

    G("ch3-intro.mp3", "The Meridian's engineer, a sharp-eyed woman named Yusra, quickly stowed their share of pods. But she needed some in reserve — exactly one third — for emergencies."),
    G("ch3-q5-question.mp3", "The Meridian has 6 pods. Yusra keeps one third in emergency reserve. How many pods is one third of 6?"),
    G("ch3-q6-story.mp3", "Now came the hard part — navigating out. Three routes stretched ahead, each covering a different fraction of the total distance. Jake had to choose wisely."),
    J("ch3-jake.mp3", "Route A covers two thirds of the distance. Route B covers three quarters. Which gets us further? I need to think about this carefully..."),
    G("ch3-q6-question.mp3", "Route A covers 2 thirds of the total distance. Route B covers 3 quarters. Which route gets Jake and the Meridian further?"),

    G("ch4-intro.mp3", "They took Route B — the longer fraction, but the smarter choice. Three quarters of the way through, Jake checked the clock. The rest of the journey would take a fraction of the time already spent."),
    G("ch4-q7-question.mp3", "They have travelled 3 quarters of the route. What fraction of the route is still remaining?"),
    G("ch4-q8-story.mp3", "Three quarters of the route had taken 12 minutes. Jake needed to calculate the final stretch."),
    J("ch4-jake.mp3", "If three quarters took 12 minutes, then one quarter takes... let me work this out properly."),
    G("ch4-q8-question.mp3", "Three quarters of the journey takes 12 minutes. How long does one quarter of the journey take?"),

    G("ch5-intro.mp3", "Both ships burst out of the nebula into clear space. The Meridian crew cheered. But as they celebrated, the Meridian's pilot pulled up something on her star map — a glowing blue route, precise and mathematical."),
    A("ch5-meridian-pilot.mp3", "This route... no ship travelled it. Something else did. Something that moves through space using pure mathematics."),
    G("ch5-q9-question.mp3", "After sharing pods, Jake and the Meridian each have some. Combined with a third rescue ship, the total is 9 pods shared equally between 3 ships. One third of 9 equals how many pods each?"),
    G("ch5-q10-story.mp3", "Yusra had worked out the theft pattern. The Fraction Phantom hadn't just stolen from this nebula."),
    A("ch5-yusra.mp3", "Each station lost exactly one quarter of one third of their total fuel. I know the fraction — but what does it actually equal?"),
    G("ch5-q10-question.mp3", "Each station lost one quarter of one third of their fuel. What single fraction does one quarter of one third equal? This is the Boss Challenge!"),
    G("win.mp3", "Mission complete! Jake and the Meridian escaped the Fog Nebula — and you solved every fraction along the way. The Fraction Phantom is getting closer. See you in Issue 3, when Jake follows the trail to the Asteroid Market!"),
],

# ══════════════════════════════════════════════════════
# ISSUE 3 — The Equivalent Exchange
# ══════════════════════════════════════════════════════
"issue003": [
    G("ch1-intro.mp3", "The Asteroid Market was chaos. Stalls carved into rock walls, traders shouting, holographic price tags flickering in a dozen languages. And right in the middle of it all — a 10-year-old kid in a merchant's apron, looking very stressed."),
    A("ch1-kenji.mp3", "I am Kenji! Best trader in the whole asteroid belt — usually. But someone has been stealing my stock. They say they took 2 quarters. My records say they took 1 half. Are those even the same thing?"),
    G("ch1-q1-question.mp3", "Kenji says 1 half of his stock was taken. The thief's record says 2 quarters was taken. Are these the same amount? That is your warm-up question!"),
    G("ch1-q2-story.mp3", "Three more vendors came forward with similar complaints. Different fractions written in their records — but Jake suspected they were all describing the same amount."),
    J("ch1-jake.mp3", "Let me check these carefully. 2 sixths versus 1 third. They look different... but are they actually the same fraction?"),
    G("ch1-q2-question.mp3", "Vendor 2 lost 2 sixths. Vendor 3's record says 1 third was taken. Are 2 sixths and 1 third equivalent fractions?"),

    G("ch2-intro.mp3", "Jake grabbed a piece of chalk and started drawing on the trading post wall — a fraction wall, showing how different fractions could be equal amounts. The traders gathered round, fascinated."),
    G("ch2-q3-question.mp3", "Are 3 sixths and 2 quarters equivalent fractions? Both should equal 1 half — is that true?"),
    G("ch2-q4-story.mp3", "The pattern was clear — the Fraction Phantom was writing its thefts using different fraction names each time, to avoid detection. Clever. But Jake was onto it."),
    J("ch2-jake.mp3", "I need to find two fractions that are equivalent to 3 quarters. If I can identify the Phantom's disguises, I can prove it was the same thief each time."),
    G("ch2-q4-question.mp3", "Jake needs two fractions that are equivalent to 3 quarters. Can you find them?"),

    G("ch3-intro.mp3", "Jake ordered all the fractions on a number line on the wall. Something remarkable appeared — several fractions all landed on exactly the same point."),
    G("ch3-q5-question.mp3", "Place these fractions on a number line: 1 half, 3 sixths, 4 eighths, and 2 fourths. What do you notice about where they land?"),
    G("ch3-q6-story.mp3", "A new theft was about to happen. Jake had spotted the Phantom's next target — a large fuel manifest with 5 tenths listed for transfer. He had seconds to simplify it and warn the vendor."),
    J("ch3-jake.mp3", "5 tenths... I need its simplest form. Fast!"),
    G("ch3-q6-question.mp3", "The manifest shows 5 tenths. Write this fraction in its simplest form."),

    G("ch4-intro.mp3", "Another transaction: 6 eighths. Jake was building a map of all the Phantom's disguised thefts, putting each fraction in its simplest form to reveal the pattern."),
    G("ch4-q7-question.mp3", "The next theft is written as 6 eighths. What is 6 eighths in its simplest form?"),
    G("ch4-q8-story.mp3", "Four fractions. One ordering challenge. Jake had to arrange them to predict which tank was most at risk."),
    G("ch4-q8-question.mp3", "Order these fractions from smallest to largest: 1 quarter, 1 half, 3 quarters, 1 eighth."),

    G("ch5-intro.mp3", "And then — the Fraction Phantom appeared. Not to steal, but to show Jake its own fraction wall. It was proud of it."),
    A("ch5-phantom.mp3", "I took 2 quarters from one ship and 3 sixths from another. I was perfectly fair. The same fraction each time. Do you see?"),
    G("ch5-q9-question.mp3", "The Phantom took 2 quarters from Ship A and 3 sixths from Ship B. Did it take the same fraction from both?"),
    G("ch5-q10-story.mp3", "Jake had to show the Phantom something it had never considered. The same fraction — but completely different real amounts."),
    J("ch5-jake.mp3", "Ship A has 16 fuel units. Ship B has only 8. Both lost 1 half. But how many units did each actually lose?"),
    G("ch5-q10-question.mp3", "Boss Challenge! Ship A has 16 fuel units and loses 1 half. Ship B has 8 fuel units and loses 1 half. Did both ships lose the same NUMBER of units?"),
    A("ch5-phantom-end.mp3", "You say... the fractions are the same. But the amounts are different. Show me how that is possible."),
    G("win.mp3", "Outstanding work, space cadet! You proved that equivalent fractions can hide in plain sight — and you cracked the Phantom's disguise. See you in Issue 4, when the chase leads to Number Line Station!"),
],

# ══════════════════════════════════════════════════════
# ISSUE 4 — Race to Number Line Station
# ══════════════════════════════════════════════════════
"issue004": [
    G("ch1-intro.mp3", "Number Line Station was unlike anything Jake had ever seen — a space station shaped like a ruler, a kilometre long, with fraction markers glowing on the walls from zero to one. And right now, every single marker was in the wrong place."),
    J("ch1-jake.mp3", "The Phantom has moved 1 half to where 3 quarters should be! If ships navigate by these signals, they'll miscalculate their distances. I have to fix this — fast."),
    G("ch1-q1-question.mp3", "The Phantom has moved the 1 half marker to the wrong position. Where should 1 half actually sit on a number line from 0 to 1?"),
    G("ch1-q2-story.mp3", "Jake sprinted down the corridor, checking markers one by one. The 1 quarter marker was misplaced. The 3 quarters marker was completely missing. Three ships were relying on these signals right now."),
    G("ch1-q2-question.mp3", "Where should the 1 quarter marker sit on a number line from 0 to 1? Is it closer to 0 or to 1 half?"),

    G("ch2-intro.mp3", "Jake replaced the markers, one by one. But then he reached a tricky section — 2 thirds and 3 quarters, placed almost identically by the Phantom."),
    J("ch2-jake.mp3", "2 thirds versus 3 quarters. They look close — but which one is actually larger? I need to be precise here. One wrong signal and a ship crashes."),
    G("ch2-q3-question.mp3", "Which is larger — 2 thirds or 3 quarters? Place them correctly on the number line."),
    G("ch2-q4-story.mp3", "The thirds section of the number line had been completely scrambled. Jake needed to restore it — and notice something important about how thirds divide a line."),
    G("ch2-q4-question.mp3", "Place 1 third and 2 thirds on the number line. What do you notice about the gaps between 0, 1 third, 2 thirds, and 1?"),

    G("ch3-intro.mp3", "The Phantom's voice crackled through the station intercom. It had been watching."),
    A("ch3-phantom.mp3", "You fix my corrections. But you have not considered: what lies beyond 1? I have added my own markers there. Markers for fractions that are MORE than one whole."),
    G("ch3-q5-question.mp3", "The Phantom has placed 5 quarters on the number line. Where does 5 quarters sit? Is it between 0 and 1, or between 1 and 2?"),
    G("ch3-q6-story.mp3", "The Phantom's new markers introduced something Jake hadn't seen before — fractions greater than one, written as improper fractions, and as mixed numbers."),
    J("ch3-jake.mp3", "5 quarters equals 1 and 1 quarter. So it sits just past the 1 mark. That actually makes sense..."),
    G("ch3-q6-question.mp3", "Write 5 quarters as a mixed number. How many wholes and how many quarters is it?"),

    G("ch4-intro.mp3", "Jake had to order four fractions and place them correctly on the extended number line — from 0 all the way to 2."),
    G("ch4-q7-question.mp3", "Order these from smallest to largest and place on the number line from 0 to 2: 3 quarters, 5 quarters, 1 half, and 7 quarters."),
    G("ch4-q8-story.mp3", "With all markers fixed, Jake ran the final check — counting from 0 to 2 in steps of 1 quarter."),
    G("ch4-q8-question.mp3", "Count from 0 to 2 in steps of 1 quarter. What are all the fractions along the way?"),

    G("ch5-intro.mp3", "Jake fixed the last marker — and the three ships' navigation signals corrected instantly. Crisis averted. But the Phantom had left one final puzzle on the station wall, written in glowing blue light."),
    A("ch5-phantom.mp3", "I removed the marker between 3 quarters and 5 quarters because it is NOT a fraction. It is a whole number. Tell me: what marker did I remove — and am I correct?"),
    G("ch5-q9-question.mp3", "What fraction sits between 3 quarters and 5 quarters on the number line? And is it actually a fraction, or a whole number — or both?"),
    G("ch5-q10-story.mp3", "The Phantom had left a final message before vanishing."),
    A("ch5-phantom-end.mp3", "You understand the number line. Then come find me at the Fraction Fair. If you reach me, I will listen."),
    G("ch5-q10-question.mp3", "Boss Challenge! The Phantom removed 4 quarters from the number line. What is 4 quarters as a whole number? And what does this tell us about the relationship between fractions and whole numbers?"),
    G("win.mp3", "Incredible! You fixed every marker on Number Line Station and saved three ships from disaster. The Fraction Phantom is starting to question its own logic. See you at the Fraction Fair in Issue 5!"),
],

# ══════════════════════════════════════════════════════
# ISSUE 5 — Showdown at the Fraction Fair
# ══════════════════════════════════════════════════════
"issue005": [
    G("ch1-intro.mp3", "The Fraction Fair was the most extraordinary thing Jake had ever seen — a travelling space carnival where every ride, every prize, every transaction ran on fractions. And somewhere inside, the Fraction Phantom had built its redistribution terminal."),
    J("ch1-jake.mp3", "To get in, I need to solve the entry puzzle. A prize wheel — 8 equal sections. I landed on 3. What fraction did I win? And is that more or less than half?"),
    G("ch1-q1-question.mp3", "The prize wheel has 8 equal sections. Jake lands on 3 sections. What fraction did he win? Is 3 eighths more or less than 1 half?"),
    G("ch1-q2-story.mp3", "Inside, the first game was the Fuel Allocation challenge. Jake had 5 eighths of a tank. Ship Alpha needed 3 eighths. He had to give it — but how much would he have left?"),
    G("ch1-q2-question.mp3", "Jake has 5 eighths of fuel. He gives 3 eighths to Ship Alpha. What fraction does Jake have remaining?"),

    G("ch2-intro.mp3", "Ship Beta was next — it needed 7 eighths of a tank. Jake only had 2 eighths left. He needed to top up from the reserve: 1 quarter plus 1 half."),
    J("ch2-jake.mp3", "1 quarter plus 1 half. I need to add those fractions first. Then I'll know if we have enough for Beta."),
    G("ch2-q3-question.mp3", "Jake needs to add 1 quarter and 1 half together. What is 1 quarter plus 1 half? Is that enough to give Ship Beta 7 eighths?"),
    G("ch2-q4-story.mp3", "The Phantom had its own stage show — giving every ship 1 quarter of a full tank. It called this perfectly fair. Jake watched with growing frustration."),
    A("ch2-phantom.mp3", "I give each ship exactly 1 quarter. The same fraction. This is fairness. The big ship and the small ship — both receive 1 quarter. Equal treatment for all."),
    G("ch2-q4-question.mp3", "The big ship holds 40 units. The Phantom gives it 1 quarter. How many units is that?"),

    G("ch3-intro.mp3", "The small ship held only 8 units. The Phantom gave it 1 quarter too — the same fraction. But the same fraction of a different whole meant something very different."),
    G("ch3-q5-question.mp3", "The small ship holds 8 units. The Phantom gives it 1 quarter. How many units does the small ship receive?"),
    G("ch3-q6-story.mp3", "Jake had to win the Fraction Fair's ordering race to reach the Phantom's terminal. Four fractions, ordered fastest wins."),
    G("ch3-q6-question.mp3", "Order these fractions from smallest to largest: 3 eighths, 5 eighths, 1 eighth, and 7 eighths."),

    G("ch4-intro.mp3", "Round 2: which is bigger — 5 sixths or 7 eighths? Jake's answer would determine which path he took to the terminal."),
    G("ch4-q7-question.mp3", "Which fraction is larger — 5 sixths or 7 eighths? Think carefully — the denominators are different."),
    G("ch4-q8-story.mp3", "The final ordering challenge: Jake needed fractions that summed to exactly 1 whole. He had 3 eighths and 2 eighths already. What was missing?"),
    J("ch4-jake.mp3", "3 eighths plus 2 eighths is 5 eighths. To reach a whole, I need... 3 more eighths. So the missing fraction is 3 eighths!"),
    G("ch4-q8-question.mp3", "Jake has collected 3 eighths and 2 eighths. What fraction does he still need to make exactly 1 whole?"),

    G("ch5-intro.mp3", "Jake reached the Phantom's terminal. It had a fraction lock — three numbers that had to be added together and converted to a mixed number."),
    G("ch5-q9-question.mp3", "The terminal requires the answer to: 1 quarter plus 2 quarters plus 3 quarters. Add them together, then convert your answer to a mixed number."),
    G("ch5-q10-story.mp3", "One final lock. The hardest yet."),
    A("ch5-phantom.mp3", "What fraction, added to 5 eighths, makes exactly 2 wholes? Solve this — and the terminal opens."),
    G("ch5-q10-question.mp3", "Boss Challenge! What fraction do you need to add to 5 eighths to make exactly 2 wholes? Work it out step by step."),
    A("ch5-phantom-end.mp3", "The terminal is open. Inside you will find my location. Come to the Fraction Core — if you reach me, I will listen."),
    G("win.mp3", "You won the Fraction Fair and cracked the terminal! One more issue stands between Jake and the Fraction Phantom. See you in Issue 6 — the journey into the Fraction Core begins!"),
],

# ══════════════════════════════════════════════════════
# ISSUE 6 — Into the Fraction Core
# ══════════════════════════════════════════════════════
"issue006": [
    G("ch1-intro.mp3", "The Zephyr Nebula looked like nothing Jake had ever seen. Fractions hung in the air as visible light — glowing bars and number lines woven through the gas clouds like living mathematics. And at the centre, pulsing with blue light, was the Fraction Core."),
    A("ch1-phantom.mp3", "Before you enter, you must prove you understand what lies between 1 and 2. Not whole numbers. The fractions that live there. Name three of them."),
    G("ch1-q1-question.mp3", "The nebula's entry test: name three fractions that sit between 1 and 2 on a number line. They can be mixed numbers or improper fractions."),
    G("ch1-q2-story.mp3", "Jake passed the entry test. The nebula's light patterns shifted to guide him — but the signals were given as improper fractions and mixed numbers, and he had to convert between them to navigate."),
    G("ch1-q2-question.mp3", "A navigation signal reads 1 and 3 quarters. Write this as an improper fraction — how many quarters is that altogether?"),

    G("ch2-intro.mp3", "Another signal: 11 quarters. Jake needed it as a mixed number to plot his course correctly."),
    J("ch2-jake.mp3", "11 quarters. How many full wholes fit in 11 quarters? 4 quarters make 1 whole, so... 2 wholes with 3 quarters left over. That's 2 and 3 quarters."),
    G("ch2-q3-question.mp3", "Convert 11 quarters to a mixed number. How many wholes and how many quarters?"),
    G("ch2-q4-story.mp3", "The Phantom's voice filled the nebula. It was setting a test — not a navigation problem, but a fairness problem. Three ships, each losing the same fraction of fuel, but very different real amounts."),
    A("ch2-phantom.mp3", "Ship Kepler has a 24-unit tank. I took 1 third. Calculate what I took — in units, not fractions."),
    G("ch2-q4-question.mp3", "Ship Kepler has a 24-unit tank. The Phantom took 1 third of it. How many units did the Phantom actually take?"),

    G("ch3-intro.mp3", "Ship Vega had an 18-unit tank. The Phantom took 1 third from that too — the same fraction. But 1 third of 18 was not the same as 1 third of 24."),
    G("ch3-q5-question.mp3", "Ship Vega has an 18-unit tank. The Phantom took 1 third. How many units did the Phantom take from Vega?"),
    G("ch3-q6-story.mp3", "The Fraction Core was in sight. But to reach it, Jake had to navigate the Phantom's logic maze — four routes, each requiring a fraction of a quantity to calculate."),
    G("ch3-q6-question.mp3", "Route 3 quarters leads to the Core. The total journey is 28 units. How many units is 3 quarters of 28?"),

    G("ch4-intro.mp3", "After travelling 3 quarters of the journey, Jake checked the distance remaining."),
    J("ch4-jake.mp3", "If 3 quarters is 21 units, then the remaining 1 quarter must be... 7 units. I can do this!"),
    G("ch4-q7-question.mp3", "Jake has travelled 3 quarters of a 28-unit journey. How many units remain?"),
    G("ch4-q8-story.mp3", "The final calculation before the Core: combining the two parts of the journey into a whole."),
    G("ch4-q8-question.mp3", "Jake travels 3 quarters of an hour, then 1 quarter of an hour. What is the total journey time?"),

    G("ch5-intro.mp3", "The Fraction Core. Jake floated inside — and there it was. The Fraction Phantom in full form: a towering holographic figure made entirely of glowing fraction bars and number lines, shifting and rearranging itself like living mathematics."),
    A("ch5-phantom.mp3", "I have taken 1 fifth from 15 stations. I have been thorough. Tell me — what is the total I have taken, as a fraction of one full station's worth?"),
    G("ch5-q9-question.mp3", "The Phantom took 1 fifth from 15 stations. What is the total amount taken, expressed as a fraction of one full station?"),
    G("ch5-q10-story.mp3", "The Phantom recited its last redistribution — three stations, three fractions of quantities."),
    A("ch5-phantom.mp3-2", "My final redistribution: 2 thirds of 24 units, 3 quarters of 16 units, and 1 half of 12 units. Calculate the total I redistributed."),
    G("ch5-q10-question.mp3", "Boss Challenge! Calculate: 2 thirds of 24, plus 3 quarters of 16, plus 1 half of 12. What is the total the Phantom redistributed?"),
    A("ch5-phantom-end.mp3", "I did not consider... the size of the whole. I will need time to recalculate. Return tomorrow. Bring proof that fairness requires understanding the whole."),
    G("win.mp3", "You reached the Fraction Core and the Phantom is finally listening! One final issue to go — the most important of all. See you in Issue 7, when Jake teaches the Phantom the true meaning of fair shares!"),
],

# ══════════════════════════════════════════════════════
# ISSUE 7 — The Fair Share Solution
# ══════════════════════════════════════════════════════
"issue007": [
    G("ch1-intro.mp3", "Jake returned to the Fraction Core with a notebook full of evidence and a plan. The Fraction Phantom waited — still and quiet, its fraction bars barely shifting. This time, it was ready to listen."),
    J("ch1-jake.mp3", "I am going to show you something important. Two fuel tanks — one holds 20 units, one holds 10 units. Both tanks are exactly 1 half full. But are they holding the same amount? That is the question."),
    G("ch1-q1-question.mp3", "Tank A holds 20 units and is 1 half full. Tank B holds 10 units and is 1 half full. How many units is each tank actually holding?"),
    G("ch1-q2-story.mp3", "The Phantom studied the two tanks. Its fraction bars flickered with something like confusion."),
    A("ch1-phantom.mp3", "The fraction is identical. 1 half equals 1 half. And yet... the amounts are different. Show me on a number line. I need to see this."),
    G("ch1-q2-question.mp3", "Which shows more fuel: 1 half of a 12-unit bar, or 1 third of a 12-unit bar? Calculate both to find out."),

    G("ch2-intro.mp3", "Jake pulled up the Phantom's full theft record. Station by station — the same fraction taken, but wildly different real amounts lost, depending on the size of each station's total fuel."),
    G("ch2-q3-question.mp3", "Station Kepler had 40 units. The Phantom took 1 quarter. How many units did Kepler actually lose?"),
    G("ch2-q4-story.mp3", "Station Vega had only 16 units. The Phantom took 1 quarter from Vega too — the same fraction. But a very different number of units."),
    G("ch2-q4-question.mp3", "Station Vega had 16 units. The Phantom took 1 quarter. How many units did Vega lose?"),

    G("ch3-intro.mp3", "The Fraction Phantom was very still. Its fraction bars had stopped moving. It was processing something enormous — the realisation that its entire understanding of fairness was wrong."),
    A("ch3-phantom.mp3", "I see. Kepler lost 10 units. Vega lost 4 units. Same fraction. Enormously different losses. My algorithm... was not fair. It was the opposite of fair. I must correct this."),
    G("ch3-q5-question.mp3", "The Phantom wants to give every ship exactly enough to reach 3 quarters full. A ship with a 32-unit tank is currently empty. How many units does it need?"),
    G("ch3-q6-story.mp3", "A second ship, with a 24-unit tank, also needed topping up to 3 quarters."),
    G("ch3-q6-question.mp3", "A ship has a 24-unit tank and is currently empty. How many units does it need to reach 3 quarters full?"),

    G("ch4-intro.mp3", "A third ship was already half full — it just needed the extra top-up to 3 quarters. But this ship had a 16-unit tank. How much more did it need?"),
    J("ch4-jake.mp3", "The ship is already at 1 half. It needs to reach 3 quarters. The difference between 1 half and 3 quarters is 1 quarter. And 1 quarter of a 16-unit tank is..."),
    G("ch4-q7-question.mp3", "A ship has a 16-unit tank and is already 1 half full. How many more units does it need to reach 3 quarters full?"),
    G("ch4-q8-story.mp3", "The Phantom broadcast its new corrected algorithm across the galaxy. Three stations were about to receive fuel corrections — Jake needed to order them."),
    G("ch4-q8-question.mp3", "Three stations are receiving corrections: plus 1 quarter of a tank, plus 1 half of a tank, and plus 3 quarters of a tank. Order these from the smallest correction to the largest."),

    G("ch5-intro.mp3", "The Fraction Phantom stood before Jake one final time. Something had changed in it. The fraction bars that made up its form were no longer shifting randomly — they were arranging themselves into a perfect, fair distribution."),
    A("ch5-phantom.mp3", "I have 60 units to redistribute. Station A has a 40-unit tank, currently 1 quarter full, and needs to reach 3 quarters. Station B has a 20-unit tank, currently empty, and needs to reach 1 half. Calculate what each station needs — and tell me: do I have enough?"),
    G("ch5-q9-question.mp3", "Station A: 40-unit tank, currently 1 quarter full, needs to reach 3 quarters. How many units does Station A need?"),
    G("ch5-q10-story.mp3", "Station B needed its share too."),
    G("ch5-q10-question.mp3", "Boss Challenge! Station B has a 20-unit tank, currently empty, needs 1 half full. How many units does it need? And with 60 units total to give — do both stations get what they need?"),
    A("ch5-phantom-resolution.mp3", "Station A needs 20 units. Station B needs 10 units. Total: 30 units. You have 60. Yes. Both stations receive what they need — and 30 units remain for emergencies. This... is fairness. Not equal fractions. Equal outcomes."),
    G("ch5-resolution.mp3", "The Fraction Phantom restructured itself — its shifting fraction bars settling into clean, precise patterns. It became the Fraction Keeper: guardian of fair distribution across the galaxy. And Priya, at Kepler Station, sent a message."),
    A("win-priya.mp3", "Jake? This is Priya at Kepler Station. The tanks are full. All of them. Thank you."),
    G("win.mp3", "You did it! You helped Jake teach the Fraction Phantom the true meaning of fairness — and saved the entire Interstellar Fuel Network. The full Space Fractions arc is complete. Well done, space cadet. The galaxy thanks you!"),
],

}

# Shared feedback for all issues
SHARED_FEEDBACK = [
    ("feedback-correct-1.mp3", ANDREW, JAKE, "Pre-launch check passed! Great work!"),
    ("feedback-correct-2.mp3", ANDREW, JAKE, "Brilliant! Nice work, space cadet!"),
    ("feedback-correct-3.mp3", ANDREW, JAKE, "That is correct! Outstanding!"),
    ("feedback-correct-4.mp3", ANDREW, JAKE, "Perfect! You have got this!"),
    ("feedback-correct-5.mp3", ANDREW, JAKE, "Excellent work, cadet!"),
    ("feedback-correct-6.mp3", ANDREW, JAKE, "Spot on! Mission continues!"),
    ("feedback-wrong-1.mp3",   ANDREW, JAKE, "Hmm, not quite. Let me think about this again..."),
    ("feedback-wrong-2.mp3",   ANDREW, JAKE, "Not this time — give it another go!"),
]

def generate(out_path, voice_id, settings, text):
    if os.path.exists(out_path):
        print(f"  ✓ {os.path.basename(out_path)} (cached)")
        return True
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({"text": text, "model_id": MODEL, "voice_settings": settings}).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "xi-api-key": API_KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"
    })
    try:
        with urllib.request.urlopen(req) as r: data = r.read()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        open(out_path, 'wb').write(data)
        print(f"  ✅ {os.path.basename(out_path)} ({len(data)//1024}kb)")
        return True
    except urllib.error.HTTPError as e:
        print(f"  ❌ {os.path.basename(out_path)}: {e.code} — {e.read().decode()[:80]}")
        return False

total_ok = total_all = 0

for issue_id, segments in ISSUES.items():
    issue_dir = os.path.join(BASE, issue_id)
    os.makedirs(issue_dir, exist_ok=True)
    print(f"\n{'='*50}\n{issue_id.upper()} — {len(segments)} segments\n{'='*50}")

    # Copy shared feedback if not present
    for fname, voice, settings, text in SHARED_FEEDBACK:
        out = os.path.join(issue_dir, fname)
        generate(out, voice, settings, text)
        time.sleep(0.25)

    for fname, voice, settings, text in segments:
        out = os.path.join(issue_dir, fname)
        ok = generate(out, voice, settings, text)
        if ok: total_ok += 1
        total_all += 1
        time.sleep(0.35)

print(f"\n{'='*50}")
print(f"COMPLETE: {total_ok}/{total_all} segments generated")
