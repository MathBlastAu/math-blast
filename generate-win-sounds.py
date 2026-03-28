#!/usr/bin/env python3
"""
Generate proper win/celebration jingle WAV files for Math Blast.
Uses numpy to synthesize multi-instrument, melodic fanfares.
"""

import numpy as np
from scipy.io import wavfile
import os

DEST = "/Users/leohiem/.openclaw/workspace/projects/math-blast/sounds"
SR = 44100  # sample rate

def note(freq, duration, sr=SR, wave='sine', attack=0.01, release=0.1, vol=0.6):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    if wave == 'sine':
        w = np.sin(2 * np.pi * freq * t)
    elif wave == 'square':
        w = np.sign(np.sin(2 * np.pi * freq * t)) * 0.4
    elif wave == 'triangle':
        w = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
    elif wave == 'sawtooth':
        w = 2 * (t * freq - np.floor(t * freq + 0.5))
    else:
        w = np.sin(2 * np.pi * freq * t)
    
    # Envelope
    env = np.ones_like(t)
    atk_samples = int(attack * sr)
    rel_samples = int(release * sr)
    if atk_samples > 0:
        env[:atk_samples] = np.linspace(0, 1, atk_samples)
    if rel_samples > 0 and rel_samples < len(env):
        env[-rel_samples:] = np.linspace(1, 0, rel_samples)
    
    return w * env * vol

def mix(tracks, sr=SR):
    max_len = max(len(t) for t in tracks)
    result = np.zeros(max_len)
    for t in tracks:
        result[:len(t)] += t
    # Normalize to prevent clipping
    peak = np.max(np.abs(result))
    if peak > 0.95:
        result = result / peak * 0.95
    return result

def save(filename, audio, sr=SR):
    path = os.path.join(DEST, filename)
    audio_int16 = (audio * 32767).astype(np.int16)
    wavfile.write(path, sr, audio_int16)
    print(f"✅ Saved: {filename} ({len(audio)/sr:.1f}s)")

def at(track, offset_sec, sr=SR):
    """Offset a track by adding silence at the start."""
    silence = np.zeros(int(offset_sec * sr))
    return np.concatenate([silence, track])

# Note frequencies
C4=261.63; D4=293.66; E4=329.63; F4=349.23; G4=392.00; A4=440.00; B4=493.88
C5=523.25; D5=587.33; E5=659.25; F5=698.46; G5=783.99; A5=880.00; B5=987.77
C6=1046.50; E6=1318.51; G6=1567.98
C3=130.81; G3=196.00; E3=164.81

# ============================================================
# WIN-1: "Space Fanfare" — triumphant, orchestral-ish, 3.5s
# C major: C-E-G-C rise then full chord celebration
# ============================================================
def make_win1():
    # Rising brass-like intro (square waves)
    rise = [
        at(note(C4, 0.15, wave='square', vol=0.5, release=0.05), 0.0),
        at(note(E4, 0.15, wave='square', vol=0.5, release=0.05), 0.15),
        at(note(G4, 0.15, wave='square', vol=0.5, release=0.05), 0.30),
        at(note(C5, 0.20, wave='square', vol=0.55, release=0.05), 0.45),
    ]
    # Big landing chord (triangle for warmth)
    chord = [
        at(note(C5, 0.8, wave='triangle', vol=0.55, attack=0.02, release=0.3), 0.70),
        at(note(E5, 0.8, wave='triangle', vol=0.50, attack=0.03, release=0.3), 0.72),
        at(note(G5, 0.8, wave='triangle', vol=0.45, attack=0.04, release=0.3), 0.74),
    ]
    # Celebratory melodic run
    run = [
        at(note(C5, 0.10, wave='sine', vol=0.5, release=0.04), 1.55),
        at(note(D5, 0.10, wave='sine', vol=0.5, release=0.04), 1.66),
        at(note(E5, 0.10, wave='sine', vol=0.5, release=0.04), 1.77),
        at(note(G5, 0.10, wave='sine', vol=0.55, release=0.04), 1.88),
        at(note(A5, 0.10, wave='sine', vol=0.55, release=0.04), 1.99),
        at(note(C6, 0.55, wave='sine', vol=0.6, attack=0.02, release=0.3), 2.10),
    ]
    # Bass underneath
    bass = [
        at(note(C3, 1.5, wave='sine', vol=0.4, attack=0.05, release=0.4), 0.65),
        at(note(G3, 0.8, wave='sine', vol=0.35, attack=0.05, release=0.3), 2.0),
    ]
    # Sparkle (high pitched quick pings)
    sparkle = [
        at(note(C6, 0.12, wave='sine', vol=0.3, release=0.08), t)
        for t in [1.55, 1.70, 1.85, 2.00, 2.10, 2.20, 2.35, 2.50, 2.65]
    ]
    all_tracks = rise + chord + run + bass + sparkle
    return mix(all_tracks)

# ============================================================
# WIN-2: "Level Complete" — punchy, upbeat, 2.5s (shorter)
# ============================================================
def make_win2():
    # Quick ascending arpeggio
    arp = [
        at(note(E4, 0.12, wave='triangle', vol=0.6, release=0.05), 0.0),
        at(note(G4, 0.12, wave='triangle', vol=0.6, release=0.05), 0.12),
        at(note(C5, 0.12, wave='triangle', vol=0.65, release=0.05), 0.24),
        at(note(E5, 0.12, wave='triangle', vol=0.65, release=0.05), 0.36),
        at(note(G5, 0.50, wave='triangle', vol=0.70, attack=0.02, release=0.25), 0.48),
    ]
    # Harmony
    harmony = [
        at(note(C5, 0.50, wave='sine', vol=0.40, attack=0.03, release=0.25), 0.48),
    ]
    # Punchy second hit
    hit2 = [
        at(note(C5, 0.12, wave='square', vol=0.45, release=0.04), 1.10),
        at(note(E5, 0.12, wave='square', vol=0.45, release=0.04), 1.22),
        at(note(G5, 0.12, wave='square', vol=0.45, release=0.04), 1.34),
        at(note(C6, 0.55, wave='triangle', vol=0.60, attack=0.02, release=0.3), 1.46),
    ]
    bass = [
        at(note(C3, 0.6, wave='sine', vol=0.45, attack=0.03, release=0.2), 0.45),
        at(note(C3, 0.6, wave='sine', vol=0.40, attack=0.03, release=0.2), 1.40),
    ]
    all_tracks = arp + harmony + hit2 + bass
    return mix(all_tracks)

# ============================================================
# WIN-3: "Epic Victory" — big, multi-layered, 4s
# ============================================================
def make_win3():
    # Dramatic intro — 3 big hits
    hits = [
        at(note(C4, 0.20, wave='square', vol=0.55, release=0.08), 0.0),
        at(note(G4, 0.20, wave='square', vol=0.55, release=0.08), 0.25),
        at(note(C5, 0.25, wave='square', vol=0.60, release=0.08), 0.50),
    ]
    # Long sustained chord
    chord = [
        at(note(C5, 1.2, wave='triangle', vol=0.55, attack=0.03, release=0.4), 0.80),
        at(note(E5, 1.2, wave='triangle', vol=0.50, attack=0.04, release=0.4), 0.83),
        at(note(G5, 1.2, wave='triangle', vol=0.45, attack=0.05, release=0.4), 0.86),
        at(note(C6, 1.2, wave='sine', vol=0.40, attack=0.06, release=0.4), 0.89),
    ]
    # Triumphant melody
    melody = [
        at(note(G5, 0.15, wave='sine', vol=0.55, release=0.05), 2.10),
        at(note(A5, 0.15, wave='sine', vol=0.55, release=0.05), 2.26),
        at(note(B5, 0.15, wave='sine', vol=0.55, release=0.05), 2.42),
        at(note(C6, 0.20, wave='sine', vol=0.60, release=0.06), 2.58),
        at(note(G5, 0.12, wave='sine', vol=0.55, release=0.04), 2.82),
        at(note(E5, 0.12, wave='sine', vol=0.50, release=0.04), 2.96),
        at(note(C5, 0.80, wave='triangle', vol=0.60, attack=0.02, release=0.4), 3.10),
    ]
    # Bass line
    bass = [
        at(note(C3, 0.3, wave='sine', vol=0.50, release=0.1), 0.0),
        at(note(C3, 0.3, wave='sine', vol=0.50, release=0.1), 0.25),
        at(note(C3, 0.3, wave='sine', vol=0.50, release=0.1), 0.50),
        at(note(C3, 1.5, wave='sine', vol=0.45, attack=0.05, release=0.5), 0.78),
        at(note(G3, 1.0, wave='sine', vol=0.40, attack=0.05, release=0.4), 2.10),
        at(note(C3, 1.0, wave='sine', vol=0.45, attack=0.05, release=0.5), 3.05),
    ]
    # Sparkle shower
    sparkle_times = np.arange(2.1, 4.0, 0.12)
    sparkle = [at(note(C6 * (1 + 0.1*i%3), 0.10, wave='sine', vol=0.25, release=0.07), t)
               for i, t in enumerate(sparkle_times)]
    all_tracks = hits + chord + melody + bass + sparkle
    return mix(all_tracks)

# ============================================================
# WIN-4: "Bouncy Jingle" — fun, upbeat, child-friendly, 3s
# ============================================================
def make_win4():
    # Bouncy melody in C major — playful, quick notes
    melody_notes = [
        (C5, 0.10), (E5, 0.10), (G5, 0.10), (C6, 0.15),
        (G5, 0.10), (E5, 0.10), (G5, 0.10), (C6, 0.10),
        (A5, 0.10), (G5, 0.10), (E5, 0.10), (G5, 0.10),
        (C6, 0.55),
    ]
    melody = []
    t_offset = 0.0
    for freq, dur in melody_notes:
        melody.append(at(note(freq, dur, wave='triangle', vol=0.60, release=0.04), t_offset))
        t_offset += dur

    # Harmony (a third below)
    harmony_notes = [
        (E4, 0.40), (G4, 0.40), (E4, 0.40), (G4, 0.40),
        (E4, 0.70),
    ]
    harmony = []
    t_offset2 = 0.0
    for freq, dur in harmony_notes:
        harmony.append(at(note(freq, dur, wave='sine', vol=0.30, attack=0.02, release=0.1), t_offset2))
        t_offset2 += dur

    # Staccato bass hits
    bass_hits = [0.0, 0.40, 0.80, 1.20, 1.60, 2.00]
    bass = [at(note(C3, 0.18, wave='sine', vol=0.45, release=0.1), t) for t in bass_hits]

    # High sparkle every beat
    sparkle = [at(note(C6, 0.08, wave='sine', vol=0.25, release=0.05), t)
               for t in [0.40, 0.80, 1.20, 1.60, 2.00, 2.30, 2.55]]

    all_tracks = melody + harmony + bass + sparkle
    return mix(all_tracks)

# Generate all 4 win sounds
print("Generating win sounds...")
save("win-1.wav", make_win1())
save("win-2.wav", make_win2())
save("win-3.wav", make_win3())
save("win-4.wav", make_win4())
print("\nAll done! 🎉")
