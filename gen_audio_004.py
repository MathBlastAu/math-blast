import requests
import time

API_KEY = "sk_ced21f5abdcea4fc1c34d16e1d7a32cee707afc0b6a674fe"
BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"
BASE_PATH = "/Users/leohiem/.openclaw/workspace/projects/math-blast/audio/ocean/issue004/"

ERIC = "cjVigY5qzO86Huf0OWal"
JESSICA = "cgSgspJ2msm6clMCkdW9"
BILL = "pqHfZKP75CvOlQylNhV4"

def gen_audio(voice_id, text, filename, stability, similarity, style):
    url = f"{BASE_URL}/{voice_id}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": style
        }
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 200:
        with open(BASE_PATH + filename, "wb") as f:
            f.write(resp.content)
        print(f"✅ {filename}")
    else:
        print(f"❌ {filename}: {resp.status_code} {resp.text[:200]}")
    time.sleep(0.5)

files = [
    # A. feedback-correct-1.mp3
    (ERIC, "Signal confirmed! First check complete. The Lattice is counting on you!", "feedback-correct-1.mp3", 0.5, 0.75, 0.2),

    # B. ch3-marina-analysis.mp3
    (JESSICA, "It isn't disrupting the Lattice on purpose. It woke up and felt the Lattice field, and its own field interacted with it. The Whale doesn't understand why the stones are dark. It's confused and distressed and it keeps sending its own signal louder, trying to get an answer. The Lattice going dark is making the Whale send harder.", "ch3-marina-analysis.mp3", 0.55, 0.80, 0.25),

    # C. ch4-intro.mp3 (re-generate with full text)
    (ERIC, "Marina worked fast. Her datapad captured the Whale's full pulse sequence. Flick, bonded to the datapad, could carry the signal to the right Lattice stones. But first Marina had to calculate exactly which stone groupings needed to light up, and in what sequence. The calculations had to be right. There would be no second chance.", "ch4-intro.mp3", 0.5, 0.75, 0.2),

    # C. ch4-marina-briefing.mp3
    (JESSICA, "Flick, I need you to be brave. I need you to carry this signal up through the water, to the Lattice field above us, and pulse it to the right stones. In the right pattern. Exactly as I calculate it.", "ch4-marina-briefing.mp3", 0.55, 0.80, 0.25),

    # C. ch4-flick-ready.mp3
    (ERIC, "Flick's antenna fins pointed straight up. Wing-tips pulsed cyan once, firmly. Ready.", "ch4-flick-ready.mp3", 0.5, 0.75, 0.2),

    # D. ch5-finale-narrate.mp3
    (ERIC, "When Marina and Flick surfaced back into Luminos, every Lattice stone in the city was glowing at full brightness. The Coralfolk lined the streets, hundreds of them, their shells reflecting amber and teal light in every direction. They did not cheer the way humans cheer. They communicated through the Lattice, rippling glowing patterns from stone to stone, from city to city across the whole of the Luminous Deep. A celebration that could be felt for a thousand tide-lengths in every direction. Elder Luma was waiting at the entrance. He held something in one small three-fingered hand. A single signal stone, warm amber, glowing steadily.", "ch5-finale-narrate.mp3", 0.5, 0.75, 0.2),

    # D. ch5-finale-luma.mp3
    (BILL, "This stone is tuned to the Lattice of Luminos. When you need us, hold it and send the pattern. We will know it is you. We will know you understand the Ripple.", "ch5-finale-luma.mp3", 0.65, 0.75, 0.15),

    # D. ch5-finale-narrate2.mp3
    (ERIC, "Marina took the stone carefully. Flick pressed close against her side, antenna fins up, wing-tips pulsing in the steadiest, most contented pattern Marina had ever seen.", "ch5-finale-narrate2.mp3", 0.5, 0.75, 0.2),

    # D. ch5-finale-marina.mp3
    (JESSICA, "Thank you, Elder Luma. For trusting me.", "ch5-finale-marina.mp3", 0.55, 0.80, 0.25),

    # D. ch5-finale-outro.mp3
    (ERIC, "Elder Luma turned and walked back into the city, staff tapping on the coral floor. Somewhere, far below, the Whale continued its journey into deeper water. Its hum faded to nothing. And the Lattice glowed on, steady and true.", "ch5-finale-outro.mp3", 0.5, 0.75, 0.2),

    # E. win.mp3
    (ERIC, "You helped Marina calculate the Whale's pulse pattern and saved the Lattice. The Luminous Deep is at peace. And you mastered multiplication, from groups of, all the way through to times six, seven, and eight. The Luminous Deep will remember you. And Elder Luma's signal stone glows on your shelf.", "win.mp3", 0.5, 0.75, 0.2),
]

for args in files:
    gen_audio(*args)

print("All audio generation complete!")
