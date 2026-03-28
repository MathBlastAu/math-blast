#!/usr/bin/env python3
"""Generate jungle-themed WAV sound files for Math Blast Jungle Issue #1."""

import numpy as np
from scipy.io import wavfile
import os

RATE = 44100
OUT_DIR = "/Users/leohiem/.openclaw/workspace/projects/math-blast/sounds/jungle"
os.makedirs(OUT_DIR, exist_ok=True)

def marimba(freq, start, duration, vol=0.6, rate=RATE):
    """Marimba-like: sine with fast attack and exponential decay."""
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * freq * t)
    # Fast attack (0.001s), exponential decay
    attack_samples = int(0.001 * rate)
    envelope = np.exp(-t / 0.25)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    return wave * envelope * vol

def bird_chirp(f_start, f_end, duration, vol=0.4, rate=RATE):
    """Fast sine frequency sweep - bird chirp."""
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    freq = np.linspace(f_start, f_end, len(t))
    wave = np.sin(2 * np.pi * np.cumsum(freq) / rate)
    envelope = np.exp(-t / (duration * 0.5))
    return wave * envelope * vol

def percussion(freq, duration, vol=0.5, rate=RATE):
    """Short percussive sine burst."""
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t / 0.03)
    return wave * envelope * vol

def rustling(duration, vol=0.15, rate=RATE):
    """White noise filtered for rustling sound."""
    samples = int(rate * duration)
    noise = np.random.randn(samples)
    # Simple low-pass filter
    from numpy.fft import rfft, irfft
    fft = rfft(noise)
    freqs = np.linspace(0, rate/2, len(fft))
    fft[freqs > 2000] *= 0.1
    noise = irfft(fft, samples)
    envelope = np.exp(-np.linspace(0, duration, samples) / (duration * 0.4))
    return noise * envelope * vol

def mix(*arrays, total_len=None):
    """Mix multiple arrays of different lengths."""
    if total_len is None:
        total_len = max(len(a) for a in arrays)
    result = np.zeros(total_len)
    for a in arrays:
        n = min(len(a), total_len)
        result[:n] += a[:n]
    return result

def pad(arr, total_samples):
    out = np.zeros(total_samples)
    n = min(len(arr), total_samples)
    out[:n] = arr[:n]
    return out

def delay(arr, delay_secs, rate=RATE):
    """Add silence before the array."""
    silence = np.zeros(int(delay_secs * rate))
    return np.concatenate([silence, arr])

def save(filename, audio, rate=RATE):
    # Normalize and convert to int16
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.85
    audio_int16 = (audio * 32767).astype(np.int16)
    path = os.path.join(OUT_DIR, filename)
    wavfile.write(path, rate, audio_int16)
    print(f"Saved: {path}")

# ============================================================
# 1. jungle-launch.wav (~2.5s)
# Exotic bird call + jungle ambience, then whoosh through vines
# ============================================================
total = int(2.5 * RATE)

# Bird calls at the start
bird1 = delay(bird_chirp(2200, 3000, 0.08, 0.5), 0.0)
bird2 = delay(bird_chirp(1800, 2800, 0.08, 0.4), 0.12)
bird3 = delay(bird_chirp(2500, 1800, 0.08, 0.35), 0.28)

# Marimba percussion hits - exotic rhythm
mar1 = delay(marimba(400, 0, 0.3, 0.5), 0.0)
mar2 = delay(marimba(533, 0, 0.3, 0.45), 0.2)
mar3 = delay(marimba(320, 0, 0.3, 0.4), 0.4)

# Percussion drums
perc1 = delay(percussion(120, 0.06, 0.4), 0.0)
perc2 = delay(percussion(100, 0.06, 0.35), 0.3)

# Whoosh through vines - rising noise sweep
t_whoosh = np.linspace(0, 1.2, int(1.2 * RATE))
whoosh_freq = np.linspace(200, 2000, len(t_whoosh))
whoosh = np.sin(2 * np.pi * np.cumsum(whoosh_freq) / RATE) * 0.3
noise_whoosh = np.random.randn(len(t_whoosh)) * 0.15
whoosh_env = np.exp(-((t_whoosh - 0.6)**2) / 0.15)  # bell curve
whoosh_full = (whoosh + noise_whoosh) * whoosh_env
whoosh_delayed = delay(whoosh_full, 1.2)

# More bird calls near the end
bird4 = delay(bird_chirp(2000, 3200, 0.1, 0.45), 2.0)
bird5 = delay(bird_chirp(1600, 2400, 0.08, 0.3), 2.2)

launch = mix(bird1, bird2, bird3, bird4, bird5,
             mar1, mar2, mar3,
             perc1, perc2,
             whoosh_delayed,
             total_len=total)
save("jungle-launch.wav", launch)

# ============================================================
# 2. jungle-correct.wav (~0.8s)
# Bright marimba ding - 3 ascending notes, warm and wooden
# ============================================================
total = int(0.8 * RATE)

# Three ascending marimba notes
note1 = delay(marimba(523, 0, 0.5, 0.65), 0.0)   # C5
note2 = delay(marimba(659, 0, 0.5, 0.65), 0.18)  # E5
note3 = delay(marimba(784, 0, 0.6, 0.7), 0.36)   # G5

# Harmonics for warmth
harm1 = delay(marimba(1046, 0, 0.3, 0.25), 0.0)
harm2 = delay(marimba(1318, 0, 0.3, 0.2), 0.18)
harm3 = delay(marimba(1568, 0, 0.35, 0.22), 0.36)

# Tiny bird chirp at the end
bird_end = delay(bird_chirp(2200, 2800, 0.06, 0.25), 0.6)

correct = mix(note1, note2, note3, harm1, harm2, harm3, bird_end, total_len=total)
save("jungle-correct.wav", correct)

# ============================================================
# 3. jungle-wrong.wav (~0.6s)
# Gentle descending "boop boop" like a frog/critter saying no
# ============================================================
total = int(0.6 * RATE)

# Two descending warm notes - frog-like
boop1 = delay(marimba(350, 0, 0.35, 0.55), 0.0)
boop2 = delay(marimba(260, 0, 0.38, 0.5), 0.22)

# Slight harmonics for warmth
h1 = delay(marimba(700, 0, 0.2, 0.15), 0.0)
h2 = delay(marimba(520, 0, 0.22, 0.12), 0.22)

wrong = mix(boop1, boop2, h1, h2, total_len=total)
save("jungle-wrong.wav", wrong)

# ============================================================
# 4. jungle-next.wav (~0.4s)
# Single soft marimba tap + light rustling
# ============================================================
total = int(0.4 * RATE)

tap = marimba(660, 0, 0.35, 0.55)  # E5
tap_harm = marimba(1320, 0, 0.2, 0.18)
rust = rustling(0.3, 0.12)

nxt = mix(tap, tap_harm, rust, total_len=total)
save("jungle-next.wav", nxt)

# ============================================================
# 5. jungle-transition.wav (~1.5s)
# Rising exotic arpeggio like climbing vines - 5-6 ascending notes + bird finish
# ============================================================
total = int(1.5 * RATE)

# Pentatonic-ish ascending arpeggio
notes_freqs = [330, 392, 494, 587, 740, 880]
notes_delays = [0.0, 0.18, 0.36, 0.54, 0.72, 0.90]
notes_vol =    [0.5, 0.55, 0.55, 0.6, 0.62, 0.65]

all_notes = []
for f, d, v in zip(notes_freqs, notes_delays, notes_vol):
    all_notes.append(delay(marimba(f, 0, 0.45, v), d))
    # Harmonic
    all_notes.append(delay(marimba(f*2, 0, 0.25, v*0.25), d))

# Bird finish at the top
bird_finish = delay(bird_chirp(1800, 3000, 0.12, 0.5), 1.1)
bird_finish2 = delay(bird_chirp(2400, 1600, 0.08, 0.3), 1.28)

transition = mix(*all_notes, bird_finish, bird_finish2, total_len=total)
save("jungle-transition.wav", transition)

# ============================================================
# 6. jungle-win.wav (~3.5s)
# Full tropical celebration! Marimba melody + percussion + birds + chord
# ============================================================
total = int(3.5 * RATE)

# Opening fanfare - marimba runs
fanfare_notes = [
    (392, 0.0, 0.5),   # G4
    (523, 0.15, 0.5),  # C5
    (659, 0.30, 0.5),  # E5
    (784, 0.45, 0.5),  # G5
    (1047,0.60, 0.7),  # C6 - landing!
]
fan_arr = [delay(marimba(f, 0, 0.5, 0.65), d) for f, d, _ in fanfare_notes]

# Percussion rhythm throughout
perc_times = [0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, 3.2]
perc_arr = [delay(percussion(120, 0.05, 0.4), t) for t in perc_times]
perc_accent = [delay(percussion(200, 0.04, 0.5), t) for t in [0.6, 1.2, 1.8, 2.4, 3.0]]

# Second melody run - celebration
mel2_notes = [
    (784, 1.2, 0.65),
    (880, 1.38, 0.65),
    (988, 1.56, 0.65),
    (1047,1.74, 0.65),
    (1175,1.92, 0.7),
    (1319,2.10, 0.7),
]
mel2_arr = [delay(marimba(f, 0, 0.5, v), d) for f, d, v in mel2_notes]

# Harmony layer
harm_notes = [
    (659, 0.0, 0.4),
    (784, 0.15, 0.4),
    (988, 0.30, 0.4),
    (1175,0.45, 0.4),
    (1319,0.60, 0.5),
]
harm_arr = [delay(marimba(f, 0, 0.5, 0.3), d) for f, d, _ in harm_notes]

# Bird calls scattered throughout
birds_win = [
    delay(bird_chirp(2000, 3000, 0.08, 0.45), 0.1),
    delay(bird_chirp(1600, 2600, 0.08, 0.35), 0.55),
    delay(bird_chirp(2500, 1800, 0.07, 0.3),  1.05),
    delay(bird_chirp(1800, 2800, 0.08, 0.4),  1.55),
    delay(bird_chirp(2200, 3200, 0.10, 0.45), 2.05),
    delay(bird_chirp(1600, 2400, 0.08, 0.35), 2.55),
    delay(bird_chirp(2800, 3500, 0.08, 0.4),  3.05),
]

# Final triumphant chord (sustained)
chord_freqs = [523, 659, 784, 1047]  # C major chord
chord_arr = [delay(marimba(f, 0, 1.2, 0.5), 2.4) for f in chord_freqs]
chord_harm = [delay(marimba(f*2, 0, 0.8, 0.15), 2.4) for f in chord_freqs]

# Rustling throughout
rust_win = delay(rustling(3.0, 0.08), 0.2)

win = mix(*fan_arr, *perc_arr, *perc_accent,
          *mel2_arr, *harm_arr, *birds_win,
          *chord_arr, *chord_harm,
          rust_win,
          total_len=total)
save("jungle-win.wav", win)

print("\n✅ All 6 jungle sound files generated successfully!")
