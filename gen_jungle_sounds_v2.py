#!/usr/bin/env python3
"""Generate 24 jungle sound variants for Math Blast."""

import numpy as np
from scipy.io import wavfile
import os

SR = 44100
OUT_DIR = os.path.join(os.path.dirname(__file__), "sounds", "jungle")
os.makedirs(OUT_DIR, exist_ok=True)

# ── helpers ───────────────────────────────────────────────────────────────────

def save(name, arr):
    arr = arr / (np.max(np.abs(arr)) + 1e-9)
    arr = np.clip(arr * 0.80, -1.0, 1.0)
    out = (arr * 32767).astype(np.int16)
    path = os.path.join(OUT_DIR, name)
    wavfile.write(path, SR, out)
    print(f"  ✓ {name}")

def silence(dur): return np.zeros(int(SR * dur))

def mix(*arrays):
    length = max(len(a) for a in arrays)
    out = np.zeros(length)
    for a in arrays:
        out[:len(a)] += a
    return out

def note_freq(name):
    notes = {'C4':261.63,'D4':293.66,'E4':329.63,'F4':349.23,'G4':392.00,
             'A4':440.00,'B4':493.88,'C5':523.25,'D5':587.33,'E5':659.25,
             'F5':698.46,'G5':783.99,'A5':880.00,'B5':987.77,'C6':1046.50}
    return notes[name]

# ── instrument builders ───────────────────────────────────────────────────────

def marimba(freq, dur=0.35, amp=1.0):
    """Warm wooden marimba: sine + triangle, fast attack, exponential decay."""
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    attack = 0.001
    wave = (np.sin(2 * np.pi * freq * t) * 0.7 +
            np.sign(np.sin(2 * np.pi * freq * t)) * np.abs(np.sin(2 * np.pi * freq * t)) * 0.3)
    env_attack = np.clip(t / attack, 0, 1)
    env_decay = np.exp(-t / (dur * 0.35))
    env = env_attack * env_decay
    return wave * env * amp

def marimba_note(name, dur=0.35, amp=1.0):
    return marimba(note_freq(name), dur, amp)

def bird_chirp(start_hz=1800, end_hz=3200, dur=0.08, amp=1.0):
    """Fast sine frequency sweep."""
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    freq = np.linspace(start_hz, end_hz, len(t))
    wave = np.sin(2 * np.pi * np.cumsum(freq) / SR)
    env = np.exp(-t * 12) * np.sin(np.pi * t / dur)
    return wave * np.maximum(env, 0) * amp

def frog(freq=280, dur=0.25, lfo_rate=14, amp=1.0):
    """Sine with LFO wobble."""
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    lfo = 1.0 + 0.3 * np.sin(2 * np.pi * lfo_rate * t)
    wave = np.sin(2 * np.pi * freq * t * lfo)
    env = np.exp(-t / (dur * 0.6))
    return wave * env * amp

def wooden_drum(freq=160, dur=0.15, amp=1.0):
    """Short low sine burst."""
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    wave = np.sin(2 * np.pi * freq * t)
    env = np.exp(-t / 0.05)
    return wave * env * amp

def percussion(freq=100, dur=0.08, amp=1.0):
    """Short low sine burst, shorter than drum."""
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    wave = np.sin(2 * np.pi * freq * t)
    env = np.exp(-t / 0.025)
    return wave * env * amp

def freq_sweep(start_hz, end_hz, dur=0.5, amp=1.0):
    """Rising/falling sine sweep."""
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    freq = np.linspace(start_hz, end_hz, len(t))
    wave = np.sin(2 * np.pi * np.cumsum(freq) / SR)
    env = np.clip(t / 0.01, 0, 1) * np.clip((dur - t) / 0.05, 0, 1)
    return wave * env * amp

def low_hum(freq=80, dur=0.5, amp=0.4):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    wave = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 1.5 * t)
    env = np.clip(t / (dur * 0.3), 0, 1) * np.clip((dur - t) / (dur * 0.1), 0, 1)
    return wave * env * amp

def concat(*arrays):
    return np.concatenate(arrays)

def at(arr, offset_sec, total_dur):
    """Place arr at offset within a total_dur buffer."""
    out = np.zeros(int(SR * total_dur))
    start = int(SR * offset_sec)
    end = start + len(arr)
    if end > len(out):
        arr = arr[:len(out) - start]
        end = len(out)
    out[start:end] += arr
    return out

def ramp_amp(arr, start_amp, end_amp):
    ramp = np.linspace(start_amp, end_amp, len(arr))
    return arr * ramp

# ── pentatonic scale helper ───────────────────────────────────────────────────

def penta_run(notes, gap=0.12, note_dur=0.28, amp=1.0):
    """Play pentatonic notes sequentially."""
    parts = []
    for i, n in enumerate(notes):
        parts.append(silence(gap * i))
        m = marimba_note(n, note_dur, amp)
        parts.append(m)
    return mix(*[at(marimba_note(n, note_dur, amp), gap * i, gap * len(notes) + note_dur)
                 for i, n in enumerate(notes)])

# ══════════════════════════════════════════════════════════════════════════════
# LAUNCH (2-3s)
# ══════════════════════════════════════════════════════════════════════════════

def launch_a():
    # 3 wooden drum beats building up → marimba ascending run → vine-whoosh
    d1 = ramp_amp(wooden_drum(140, 0.2, 1.0), 0.5, 0.5)
    d2 = ramp_amp(wooden_drum(150, 0.2, 1.0), 0.7, 0.7)
    d3 = ramp_amp(wooden_drum(160, 0.2, 1.2), 1.0, 1.0)
    run = penta_run(['C4','D4','F4','G4','A4'], gap=0.11, note_dur=0.22, amp=0.9)
    whoosh = freq_sweep(200, 800, 0.5, 0.7)
    total = 3.0
    out = (at(d1, 0.0, total) + at(d2, 0.35, total) + at(d3, 0.70, total) +
           at(run, 1.05, total) + at(whoosh, 2.1, total))
    save("jungle-launch-a.wav", out)

def launch_b():
    # 3 exotic bird chirps at different pitches → jungle drums → big marimba chord
    c1 = bird_chirp(1600, 2800, 0.09, 1.0)
    c2 = bird_chirp(2000, 3400, 0.08, 1.0)
    c3 = bird_chirp(1400, 2600, 0.10, 1.0)
    d1 = wooden_drum(150, 0.2, 1.0)
    d2 = wooden_drum(140, 0.2, 1.0)
    d3 = wooden_drum(160, 0.2, 1.0)
    chord = mix(marimba_note('C5', 1.0, 0.9),
                marimba_note('E5', 1.0, 0.8),
                marimba_note('G5', 1.0, 0.85))
    total = 2.8
    out = (at(c1, 0.0, total) + at(c2, 0.25, total) + at(c3, 0.50, total) +
           at(d1, 0.85, total) + at(d2, 1.15, total) + at(d3, 1.45, total) +
           at(chord, 1.75, total))
    save("jungle-launch-b.wav", out)

def launch_c():
    # Slow ambience build → burst of bird calls → triumphant marimba hit
    hum1 = low_hum(70, 0.9, 0.5)
    hum2 = low_hum(90, 0.9, 0.4)
    hum3 = low_hum(55, 0.9, 0.35)
    b1 = bird_chirp(1800, 3000, 0.08, 1.0)
    b2 = bird_chirp(2200, 3500, 0.07, 0.9)
    b3 = bird_chirp(1600, 2800, 0.09, 0.85)
    hit = mix(marimba_note('C5', 0.8, 1.0),
              marimba_note('G5', 0.8, 0.9),
              wooden_drum(160, 0.15, 0.8))
    total = 2.7
    out = (at(hum1, 0.0, total) + at(hum2, 0.1, total) + at(hum3, 0.2, total) +
           at(b1, 1.0, total) + at(b2, 1.1, total) + at(b3, 1.2, total) +
           at(hit, 1.7, total))
    save("jungle-launch-c.wav", out)

def launch_d():
    # Quick 2-beat drum → fast pentatonic marimba run → single bird call
    d1 = wooden_drum(155, 0.15, 1.0)
    d2 = wooden_drum(165, 0.15, 1.1)
    run = penta_run(['C4','E4','G4','A4','C5'], gap=0.09, note_dur=0.18, amp=0.9)
    chirp = bird_chirp(2000, 3200, 0.08, 1.0)
    total = 2.3
    out = at(d1, 0.0, total) + at(d2, 0.25, total) + at(run, 0.55, total) + at(chirp, 1.65, total)
    save("jungle-launch-d.wav", out)

# ══════════════════════════════════════════════════════════════════════════════
# CORRECT (0.7-1s)
# ══════════════════════════════════════════════════════════════════════════════

def correct_a():
    # C5-E5-G5 + bird chirp finish
    m1 = marimba_note('C5', 0.28, 1.0)
    m2 = marimba_note('E5', 0.28, 1.0)
    m3 = marimba_note('G5', 0.28, 1.0)
    chirp = bird_chirp(1900, 3100, 0.07, 0.9)
    total = 0.9
    out = at(m1, 0.0, total) + at(m2, 0.18, total) + at(m3, 0.36, total) + at(chirp, 0.65, total)
    save("jungle-correct-a.wav", out)

def correct_b():
    # 4-note bouncy arpeggio C5-D5-E5-G5
    notes = ['C5','D5','E5','G5']
    total = 0.85
    out = sum(at(marimba_note(n, 0.22, 1.0), 0.14 * i, total) for i, n in enumerate(notes))
    save("jungle-correct-b.wav", out)

def correct_c():
    # E5 then C6 "ta-da" + double bird chirp
    m1 = marimba_note('E5', 0.3, 1.0)
    m2 = marimba_note('C6', 0.4, 1.1)
    b1 = bird_chirp(1800, 3000, 0.07, 0.85)
    b2 = bird_chirp(2000, 3400, 0.07, 0.85)
    total = 0.95
    out = at(m1, 0.0, total) + at(m2, 0.22, total) + at(b1, 0.65, total) + at(b2, 0.78, total)
    save("jungle-correct-c.wav", out)

def correct_d():
    # G4-A4-C5 pentatonic run + wooden percussion tap
    m1 = marimba_note('G4', 0.25, 1.0)
    m2 = marimba_note('A4', 0.25, 1.0)
    m3 = marimba_note('C5', 0.28, 1.0)
    tap = percussion(100, 0.08, 0.8)
    total = 0.85
    out = at(m1, 0.0, total) + at(m2, 0.16, total) + at(m3, 0.32, total) + at(tap, 0.58, total)
    save("jungle-correct-d.wav", out)

# ══════════════════════════════════════════════════════════════════════════════
# WRONG (0.5-0.7s)
# ══════════════════════════════════════════════════════════════════════════════

def wrong_a():
    # Descending frog boop-boop 350Hz→200Hz
    f1 = frog(350, 0.22, 12, 1.0)
    f2 = frog(200, 0.22, 10, 0.9)
    total = 0.6
    out = at(f1, 0.0, total) + at(f2, 0.28, total)
    save("jungle-wrong-a.wav", out)

def wrong_b():
    # Single low bonk (120Hz) + descending slide 300→150Hz
    bonk = wooden_drum(120, 0.18, 1.1)
    slide = freq_sweep(300, 150, 0.3, 0.8)
    total = 0.65
    out = at(bonk, 0.0, total) + at(slide, 0.2, total)
    save("jungle-wrong-b.wav", out)

def wrong_c():
    # Two descending marimba notes E4→C4
    m1 = marimba_note('E4', 0.28, 1.0)
    m2 = marimba_note('C4', 0.28, 0.85)
    total = 0.65
    out = at(m1, 0.0, total) + at(m2, 0.25, total)
    save("jungle-wrong-c.wav", out)

def wrong_d():
    # Frog ribbit wobble 180Hz fast LFO
    f = frog(180, 0.5, 22, 1.0)
    save("jungle-wrong-d.wav", f)

# ══════════════════════════════════════════════════════════════════════════════
# NEXT QUESTION (0.3-0.5s)
# ══════════════════════════════════════════════════════════════════════════════

def next_a():
    # Single marimba tap G4 + quick bird chirp
    m = marimba_note('G4', 0.22, 1.0)
    chirp = bird_chirp(2000, 3200, 0.06, 0.85)
    total = 0.45
    out = at(m, 0.0, total) + at(chirp, 0.22, total)
    save("jungle-next-a.wav", out)

def next_b():
    # Two soft marimba notes C5-E5
    m1 = marimba_note('C5', 0.2, 0.9)
    m2 = marimba_note('E5', 0.2, 0.9)
    total = 0.4
    out = at(m1, 0.0, total) + at(m2, 0.17, total)
    save("jungle-next-b.wav", out)

def next_c():
    # Wooden tap + short noise rustling
    tap = wooden_drum(170, 0.1, 1.0)
    t_noise = np.linspace(0, 0.15, int(SR * 0.15))
    noise = np.random.randn(len(t_noise)) * np.exp(-t_noise / 0.04) * 0.35
    total = 0.38
    out = at(tap, 0.0, total) + at(noise, 0.08, total)
    save("jungle-next-c.wav", out)

def next_d():
    # Quick ascending two-note marimba E4-G4
    m1 = marimba_note('E4', 0.18, 1.0)
    m2 = marimba_note('G4', 0.2, 1.0)
    total = 0.38
    out = at(m1, 0.0, total) + at(m2, 0.15, total)
    save("jungle-next-d.wav", out)

# ══════════════════════════════════════════════════════════════════════════════
# TRANSITION (1.5-2s)
# ══════════════════════════════════════════════════════════════════════════════

def transition_a():
    # 6-note pentatonic arpeggio C4-D4-F4-G4-A4-C5 + bird finish
    notes = ['C4','D4','F4','G4','A4','C5']
    total = 2.0
    out = sum(at(marimba_note(n, 0.4, 0.9), 0.19 * i, total) for i, n in enumerate(notes))
    chirp = bird_chirp(1900, 3100, 0.09, 0.9)
    out += at(chirp, 1.75, total)
    save("jungle-transition-a.wav", out)

def transition_b():
    # Marimba ascending run + 3 drum beats + bird call
    notes = ['C4','E4','G4','A4','C5']
    total = 2.0
    out = sum(at(marimba_note(n, 0.28, 0.85), 0.14 * i, total) for i, n in enumerate(notes))
    d1 = wooden_drum(145, 0.15, 0.9)
    d2 = wooden_drum(155, 0.15, 1.0)
    d3 = wooden_drum(165, 0.15, 1.1)
    out += at(d1, 0.82, total) + at(d2, 1.08, total) + at(d3, 1.34, total)
    chirp = bird_chirp(2000, 3300, 0.09, 0.9)
    out += at(chirp, 1.75, total)
    save("jungle-transition-b.wav", out)

def transition_c():
    # Slow marimba chord (3 notes together) → rising arpeggio
    chord = mix(marimba_note('C4', 0.7, 0.85),
                marimba_note('E4', 0.7, 0.75),
                marimba_note('G4', 0.7, 0.80))
    notes = ['C4','E4','G4','C5']
    total = 2.0
    out = at(chord, 0.0, total)
    for i, n in enumerate(notes):
        out += at(marimba_note(n, 0.3, 0.8), 0.85 + 0.23 * i, total)
    save("jungle-transition-c.wav", out)

def transition_d():
    # Jungle drums building (3 beats getting louder) → marimba fanfare 4 notes
    d1 = wooden_drum(140, 0.18, 0.6)
    d2 = wooden_drum(150, 0.18, 0.9)
    d3 = wooden_drum(160, 0.18, 1.2)
    notes = ['C4','E4','G4','C5']
    total = 2.0
    out = at(d1, 0.0, total) + at(d2, 0.35, total) + at(d3, 0.70, total)
    for i, n in enumerate(notes):
        out += at(marimba_note(n, 0.4, 0.9), 1.05 + 0.22 * i, total)
    save("jungle-transition-d.wav", out)

# ══════════════════════════════════════════════════════════════════════════════
# WIN (3-4s)
# ══════════════════════════════════════════════════════════════════════════════

def win_a():
    # Full jungle party — marimba melody + drum rhythm + bird calls + final big chord
    melody = ['C5','D5','E5','G5','A5','G5','E5','C5']
    total = 4.0
    out = np.zeros(int(SR * total))
    for i, n in enumerate(melody):
        out += at(marimba_note(n, 0.35, 0.85), 0.25 + 0.3 * i, total)
    # drum rhythm every 0.3s
    for i in range(10):
        freq = 140 + (i % 3) * 10
        out += at(wooden_drum(freq, 0.15, 0.6 + 0.04 * i), 0.1 + 0.3 * i, total)
    # bird calls scattered
    for t_pos, (s, e) in [(0.6, (1800, 3000)), (1.4, (2200, 3400)), (2.2, (1900, 3200)), (3.0, (2000, 3300))]:
        out += at(bird_chirp(s, e, 0.08, 0.7), t_pos, total)
    # final chord
    out += at(mix(marimba_note('C5', 1.2, 1.0), marimba_note('E5', 1.2, 0.9),
                  marimba_note('G5', 1.2, 0.95)), 3.0 - 0.2, total)
    save("jungle-win-a.wav", out)

def win_b():
    # Triumphant fanfare — 4-note rising intro + big chord + celebratory run + bird chorus
    intro = ['C4','E4','G4','C5']
    total = 3.8
    out = np.zeros(int(SR * total))
    for i, n in enumerate(intro):
        out += at(marimba_note(n, 0.4, 0.9 + 0.05 * i), 0.0 + 0.3 * i, total)
    # big chord at 1.2s
    out += at(mix(marimba_note('C5', 0.9, 1.0), marimba_note('E5', 0.9, 0.9),
                  marimba_note('G5', 0.9, 0.95)), 1.2, total)
    # celebratory run
    run = ['G4','A4','C5','D5','E5','G5']
    for i, n in enumerate(run):
        out += at(marimba_note(n, 0.25, 0.8), 2.2 + 0.18 * i, total)
    # bird chorus
    for t_pos, (s, e) in [(0.5, (2000, 3300)), (1.0, (1800, 3000)), (2.0, (2200, 3500)), (3.2, (1900, 3100))]:
        out += at(bird_chirp(s, e, 0.08, 0.65), t_pos, total)
    save("jungle-win-b.wav", out)

def win_c():
    # Rhythmic jungle beat builds 1s → marimba melody → big layered finish
    total = 4.0
    out = np.zeros(int(SR * total))
    # build-up drums
    for i in range(5):
        amp = 0.5 + 0.1 * i
        out += at(wooden_drum(140 + i * 5, 0.18, amp), 0.18 * i, total)
    # marimba melody kicks in at 1s
    melody = ['C5','E5','G5','A5','C5','E5','G5']
    for i, n in enumerate(melody):
        out += at(marimba_note(n, 0.35, 0.85), 1.05 + 0.3 * i, total)
    # drums continue from 1s
    for i in range(8):
        out += at(wooden_drum(145 + (i % 4) * 5, 0.15, 0.8), 1.0 + 0.3 * i, total)
    # bird calls during melody
    for t_pos, (s, e) in [(1.5, (1800, 3000)), (2.4, (2100, 3300)), (3.2, (1900, 3200))]:
        out += at(bird_chirp(s, e, 0.08, 0.7), t_pos, total)
    # big finish
    out += at(mix(marimba_note('C5', 1.0, 1.0), marimba_note('E5', 1.0, 0.9),
                  marimba_note('G5', 1.0, 0.95), wooden_drum(160, 0.2, 1.0)), 3.2, total)
    save("jungle-win-c.wav", out)

def win_d():
    # Gentle pentatonic melody + soft drums + bird calls — peaceful joyful
    melody = ['C5','D5','E5','G5','A5','G5','E5','D5']
    total = 3.6
    out = np.zeros(int(SR * total))
    for i, n in enumerate(melody):
        out += at(marimba_note(n, 0.42, 0.75), 0.15 + 0.35 * i, total)
    # soft drums (quieter)
    for i in range(7):
        out += at(wooden_drum(135 + (i % 3) * 8, 0.14, 0.45), 0.3 + 0.45 * i, total)
    # bird calls — gentle
    for t_pos, (s, e) in [(0.8, (1800, 2900)), (1.8, (2000, 3100)), (2.8, (1700, 2800))]:
        out += at(bird_chirp(s, e, 0.08, 0.6), t_pos, total)
    save("jungle-win-d.wav", out)

# ══════════════════════════════════════════════════════════════════════════════
# RUN ALL
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎵 Generating jungle sounds...\n")

    print("🚀 LAUNCH:")
    launch_a(); launch_b(); launch_c(); launch_d()

    print("\n✅ CORRECT:")
    correct_a(); correct_b(); correct_c(); correct_d()

    print("\n❌ WRONG:")
    wrong_a(); wrong_b(); wrong_c(); wrong_d()

    print("\n➡️ NEXT:")
    next_a(); next_b(); next_c(); next_d()

    print("\n🌟 TRANSITION:")
    transition_a(); transition_b(); transition_c(); transition_d()

    print("\n🏆 WIN:")
    win_a(); win_b(); win_c(); win_d()

    print(f"\n✅ Done! 24 files saved to {OUT_DIR}")
