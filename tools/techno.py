"""Original electronic music beds for VA Corporation reels (royalty-free, generated in code).

Every run gives a DIFFERENT track: the style, key, scale, tempo, drum groove, bassline,
melody, chords and synth sounds are all chosen/generated from --seed (or set them yourself).

Usage:
  python3 tools/techno.py OUT.wav --dur 10 --cuts 1.4,3.0,4.6,6.2 --reveal 8.2 --seed 4711
  python3 tools/techno.py OUT.wav --style synthwave --bpm 108 --dur 10 --seed 9
  python3 tools/techno.py --list            # show styles
Options:
  --style   auto (default: picked from the seed) or one of STYLES below
  --bpm     tempo; default = random inside the style's range
  --cuts    scene-change times in seconds (riser before, impact on each)
  --reveal  time of the brand/logo reveal (big impact + chord hit)
  --festive add sleigh bells and a bell melody (holiday season 1 Dec - 7 Jan)
The track starts with an impact on beat 1 at t=0 (no silent intro) and ends without a long
fade so the reel can loop. Prints a one-line description (style, key, bpm) for reels/LOG.md.
"""
import argparse, wave, sys
import numpy as np
from scipy.signal import lfilter

SR = 44100
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SCALES = {
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "harmonic minor": [0, 2, 3, 5, 7, 8, 11],
    "minor pentatonic": [0, 3, 5, 7, 10],
}

# ---------------------------------------------------------------- DSP helpers

def biquad(x, f, q=0.707, kind="lp"):
    f = float(np.clip(f, 20, SR * 0.45))
    w = 2 * np.pi * f / SR
    c, s = np.cos(w), np.sin(w)
    al = s / (2 * q)
    if kind == "lp":
        b = [(1 - c) / 2, 1 - c, (1 - c) / 2]
    elif kind == "hp":
        b = [(1 + c) / 2, -(1 + c), (1 + c) / 2]
    else:  # band-pass
        b = [al, 0, -al]
    a = [1 + al, -2 * c, 1 - al]
    return lfilter(np.array(b) / a[0], np.array(a) / a[0], x)


def env(n, a=0.003, d=0.15, s=0.0, r=0.05, length=None):
    """ADSR-ish envelope; length = gate time in seconds."""
    t = np.arange(n) / SR
    gate = length if length is not None else n / SR
    e = np.where(t < a, t / max(a, 1e-4), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4)))
    rel = np.clip(1 - (t - gate) / max(r, 1e-4), 0, 1)
    return e * np.where(t > gate, rel, 1)


def osc(kind, f, n, rng=None, detune=0.0):
    t = np.arange(n) / SR
    ph = (t * f) % 1.0
    if kind == "saw":
        return 2 * ph - 1
    if kind == "square":
        return np.where(ph < 0.5, 1.0, -1.0)
    if kind == "pulse":
        return np.where(ph < 0.25, 1.0, -1.0)
    if kind == "tri":
        return 4 * np.abs(ph - 0.5) - 1
    if kind == "sine":
        return np.sin(2 * np.pi * ph)
    if kind == "supersaw":
        out = np.zeros(n)
        for k, d in enumerate([-0.11, -0.06, -0.02, 0, 0.02, 0.06, 0.11]):
            out += 2 * ((t * f * (1 + d * 0.06) + k * 0.137) % 1.0) - 1
        return out / 4
    if kind == "fm":
        return np.sin(2 * np.pi * f * t + 2.2 * np.exp(-t * 6) * np.sin(2 * np.pi * f * 2 * t))
    if kind == "rhodes":
        e = np.exp(-t * 2.5)
        return (np.sin(2 * np.pi * f * t + 1.3 * e * np.sin(2 * np.pi * f * t)) * 0.8
                + 0.2 * np.sin(2 * np.pi * f * 4.0 * t) * np.exp(-t * 9))
    if kind == "organ":
        return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t) + 0.25 * np.sin(6 * np.pi * f * t)) / 1.75
    if kind == "reese":
        return ((2 * ((t * f * 0.995) % 1) - 1) + (2 * ((t * f * 1.006 + 0.3) % 1) - 1)) / 2
    return np.sin(2 * np.pi * ph)


def comb_reverb(x, mix=0.25, size=1.0, damp=3500):
    """Small Schroeder reverb, block-vectorised (fast)."""
    if mix <= 0:
        return x
    out = np.zeros(len(x) + int(SR * 1.2))
    src = np.concatenate([x, np.zeros(int(SR * 1.2))])
    for D, g in ((1557, 0.80), (1617, 0.79), (1491, 0.78), (1422, 0.77)):
        D = int(D * size)
        y = np.zeros_like(src)
        for k in range(0, len(src), D):
            prev = y[k - D:k] if k >= D else np.zeros(D)
            seg = src[k:k + D]
            y[k:k + len(seg)] = seg + g * prev[:len(seg)]
        out += y
    out = biquad(out / 4, damp, kind="lp")
    for D, g in ((225, 0.6), (556, 0.6)):
        y = np.zeros_like(out)
        xx = out
        for k in range(0, len(xx), D):
            xp = xx[k - D:k] if k >= D else np.zeros(D)
            yp = y[k - D:k] if k >= D else np.zeros(D)
            seg = xx[k:k + D]
            m = len(seg)
            y[k:k + m] = -g * seg + xp[:m] + g * yp[:m]
        out = y
    return x * (1 - mix * 0.5) + out[:len(x)] * mix


# ---------------------------------------------------------------- drums

def kick(kind="techno", rng=None):
    n = int((0.9 if kind in ("808", "hard") else 0.45) * SR)
    t = np.arange(n) / SR
    if kind == "808":
        f = 42 + 90 * np.exp(-t * 30)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6)
        return np.tanh(s * 1.4) * 0.95
    if kind == "hard":
        f = 48 + 170 * np.exp(-t * 34)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
        rumble = biquad(np.random.RandomState(11).randn(n) * np.exp(-t * 5), 90) * 0.9
        return np.tanh((s + rumble) * 3.2) * 0.9
    if kind == "punch":
        f = 55 + 220 * np.exp(-t * 55)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
        click = np.random.RandomState(1).randn(n) * np.exp(-t * 600) * 0.3
        return np.tanh((s + click) * 1.8) * 0.95
    f = 45 + 140 * np.exp(-t * 38)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    click = np.random.RandomState(1).randn(n) * np.exp(-t * 400) * 0.15
    return np.tanh((s + click) * 1.6) * 0.95


def noise_hit(length, hp, decay, gain, seed, bp=None):
    n = int(length * SR)
    x = np.random.RandomState(seed).randn(n)
    x = biquad(x, hp, kind="hp")
    if bp:
        x = biquad(x, bp, 1.2, kind="bp") * 3
    return x * np.exp(-np.arange(n) / SR * decay) * gain


def snare(kind="tight"):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (180 + 60 * np.exp(-t * 40)) * t) * np.exp(-t * 18) * 0.5
    nz = noise_hit(0.35, 1500, 14 if kind == "big" else 24, 0.45, 21)
    return np.tanh((body + nz) * 1.3) * 0.8


def clap():
    n = int(0.3 * SR)
    x = biquad(np.random.RandomState(3).randn(n), 1200, 0.9, kind="bp") * 2.5
    e = np.zeros(n)
    for d in (0, 0.011, 0.022, 0.031):
        i = int(d * SR)
        e[i:] += np.exp(-np.arange(n - i) / SR * (30 if d < 0.03 else 16))
    return x * e * 0.16


def drums(rng):
    return {
        "hc": noise_hit(0.05, 7000, 80, 0.11, 2),
        "ho": noise_hit(0.22, 6500, 15, 0.11, 4),
        "ride": noise_hit(0.4, 5000, 8, 0.045, 6, bp=7800),
        "shk": noise_hit(0.07, 5000, 50, 0.06, 8, bp=9000),
        "rim": noise_hit(0.04, 1800, 90, 0.35, 9, bp=2400),
        "clap": clap(),
        "snare": snare(),
        "snare_big": snare("big"),
        "perc": np.sin(2 * np.pi * np.cumsum(np.full(int(0.15 * SR), 420 + rng.randint(0, 300))) / SR)
                * np.exp(-np.arange(int(0.15 * SR)) / SR * 30) * 0.25,
    }


# ---------------------------------------------------------------- styles
# Patterns: 16 steps per bar ("x" hit, "o" accent/open, "." rest). Lists = variations picked by seed.
STYLES = {
    "acid_techno": dict(bpm=(126, 132), kick="techno", scale=["phrygian", "minor"], swing=0.0,
        drums={"hc": ["xxxxxxxxxxxxxxxx", "x.xxx.xxx.xxx.xx"], "ho": ["..x...x...x...x."], "clap": ["....x.......x..."]},
        bass=dict(kind="saw", cut=420, q=1.2, pattern=[".xxx.xxx.xxx.xxx", ".x.x.xxx.x.x.xxx"], octave=-2),
        lead=dict(kind="saw", acid=True, cut=(500, 3200), q=6.0, rate=2, octave=0),
        pad=None, reverb=0.12, duck=0.35),
    "melodic_techno": dict(bpm=(120, 126), kick="techno", scale=["minor", "harmonic minor", "dorian"], swing=0.0,
        drums={"hc": ["..x...x...x...x.", "x.x.x.x.x.x.x.x."], "ho": ["..o...o...o...o."], "clap": ["....x.......x..."], "shk": ["xxxxxxxxxxxxxxxx"]},
        bass=dict(kind="saw", cut=300, q=0.9, pattern=["..x...x...x...x.", ".xx..xx..xx..xx."], octave=-2),
        lead=dict(kind="fm", arp=True, cut=(2200, 5200), q=1.0, rate=1, octave=0),
        pad=dict(kind="supersaw", cut=1800), reverb=0.35, duck=0.55),
    "hard_techno": dict(bpm=(138, 148), kick="hard", scale=["phrygian", "minor"], swing=0.0,
        drums={"hc": ["..x...x...x...x."], "ho": ["..o...o...o...o."], "ride": ["x.x.x.x.x.x.x.x."], "clap": ["....x.......x...", "........x......."]},
        bass=None,
        lead=dict(kind="square", stab=True, cut=(900, 2600), q=3.0, rate=4, octave=-1),
        pad=None, reverb=0.18, duck=0.2),
    "minimal": dict(bpm=(124, 128), kick="punch", scale=["minor pentatonic", "dorian"], swing=0.12,
        drums={"hc": ["x.xxx.xxx.xxx.xx"], "rim": ["...x..x....x.x..", "..x..x...x...x.."], "clap": ["....x.......x..."], "perc": ["......x.......x.", ".......x.....x.."]},
        bass=dict(kind="sine", cut=600, q=0.8, pattern=["x..x..x...x..x..", ".x...x.x.x...x.."], octave=-2),
        lead=dict(kind="pulse", blip=True, cut=(1500, 3000), q=2.0, rate=2, octave=0),
        pad=None, reverb=0.22, duck=0.3),
    "trance": dict(bpm=(136, 140), kick="punch", scale=["minor", "harmonic minor"], swing=0.0,
        drums={"hc": ["..x...x...x...x."], "ho": ["..o...o...o...o."], "clap": ["....x.......x..."], "ride": ["xxxxxxxxxxxxxxxx"]},
        bass=dict(kind="saw", cut=500, q=0.9, pattern=[".xxx.xxx.xxx.xxx"], octave=-2),
        lead=dict(kind="supersaw", chords=True, cut=(2500, 6500), q=0.9, rate=2, octave=0, gate=True),
        pad=dict(kind="supersaw", cut=2500), reverb=0.38, duck=0.6),
    "synthwave": dict(bpm=(100, 112), kick="punch", scale=["minor", "dorian"], swing=0.0,
        drums={"hc": ["x.x.x.x.x.x.x.x."], "snare_big": ["....x.......x..."]},
        bass=dict(kind="saw", cut=700, q=1.0, pattern=["xxxxxxxxxxxxxxxx"], octave=-2, octaves=True),
        lead=dict(kind="square", melody=True, cut=(2500, 4500), q=1.0, rate=4, octave=1, vibrato=True),
        pad=dict(kind="supersaw", cut=1500), reverb=0.45, duck=0.35),
    "drum_and_bass": dict(bpm=(170, 176), kick="punch", scale=["minor", "phrygian"], swing=0.0,
        drums={"hc": ["x.x.x.x.x.xxx.x.", "xxxxx.xxxxxxx.xx"], "snare": ["....x.......x...", "....x.......x..x"]},
        kick_pattern=["x.........x.....", "x......x..x....."],
        bass=dict(kind="reese", cut=420, q=1.5, pattern=["x.......x.......", "x.....x...x....."], octave=-2, long=True),
        lead=dict(kind="fm", melody=True, cut=(3000, 6000), q=0.8, rate=4, octave=1),
        pad=dict(kind="supersaw", cut=1200), reverb=0.4, duck=0.5),
    "electro": dict(bpm=(124, 130), kick="808", scale=["phrygian", "minor"], swing=0.0,
        drums={"hc": ["x.x.x.x.x.x.x.x."], "clap": ["....x.......x..."], "rim": ["..x.....x..x...."]},
        kick_pattern=["x......x..x.....", "x.....x...x..x.."],
        bass=dict(kind="square", cut=800, q=2.5, pattern=["x..x..x...x.x...", "x.x...x..x..x..."], octave=-2),
        lead=dict(kind="square", arp=True, cut=(1800, 3800), q=3.0, rate=1, octave=0),
        pad=None, reverb=0.2, duck=0.25),
    "tech_house": dict(bpm=(122, 126), kick="punch", scale=["dorian", "minor"], swing=0.16,
        drums={"hc": ["x.xxx.xxx.xxx.xx"], "ho": ["..o...o...o...o."], "clap": ["....x.......x..."], "shk": ["xxxxxxxxxxxxxxxx"], "perc": ["..........x...x."]},
        bass=dict(kind="saw", cut=550, q=1.8, pattern=["..x.x..x..x.x..x", "...x..x...x..xx."], octave=-2),
        lead=dict(kind="organ", stab=True, cut=(1800, 3200), q=1.0, rate=4, octave=0, sevenths=True),
        pad=None, reverb=0.25, duck=0.45),
    "deep_house": dict(bpm=(118, 122), kick="techno", scale=["minor", "dorian"], swing=0.14,
        drums={"hc": ["x.x.x.x.x.x.x.x."], "ho": ["..o...o...o...o."], "rim": ["....x.......x...", "....x..x....x..."], "shk": ["xxxxxxxxxxxxxxxx"]},
        bass=dict(kind="sine", cut=500, q=0.8, pattern=["x.....x...x.....", "x..x......x..x..", "..x...x...x..x.."], octave=-2, long=True),
        lead=dict(kind="rhodes", stab=True, cut=(2200, 3800), q=0.8, rate=4, octave=0, sevenths=True),
        pad=dict(kind="supersaw", cut=1100), reverb=0.4, duck=0.45),
}

# ------------------------------------------------- acoustic styles (separate engine)
# Mozart (1756-1791) themes are public domain. Notes: (midi or None for rest, length in beats).
MOZART = {
    "eine_kleine_nachtmusik_k525": dict(bpm=132, beats=4, sound="strings", notes=[
        (67, 1), (None, .5), (62, .5), (67, 1), (None, .5), (62, .5), (67, .5), (62, .5), (67, .5), (71, .5), (74, 2),
        (72, 1), (None, .5), (69, .5), (72, 1), (None, .5), (69, .5), (72, .5), (69, .5), (66, .5), (69, .5), (62, 2)],
        chords=[[43, 55, 59, 62], [43, 55, 59, 62], [38, 54, 57, 60], [38, 54, 57, 60]]),
    "symphony_40_k550": dict(bpm=112, beats=4, sound="strings", notes=[
        (75, .5), (74, .5), (74, 1), (75, .5), (74, .5), (74, 1), (75, .5), (74, .5), (74, 1), (82, 1),
        (None, .5), (82, .5), (81, .5), (79, .5), (79, 1), (79, .5), (77, .5), (75, 1), (75, .5), (74, .5), (72, 1), (72, 1),
        (None, .5), (74, .5), (72, .5)],
        chords=[[43, 55, 58, 62], [43, 55, 58, 62], [43, 55, 60, 63], [38, 54, 57, 60]]),
    "sonata_k545": dict(bpm=118, beats=4, sound="piano", alberti=True, notes=[
        (72, 2), (76, 1), (79, 1), (71, 1.5), (72, .25), (74, .25), (72, 2), (81, 2), (79, 1), (84, 1), (79, 1), (77, 1), (76, 2)],
        chords=[[48, 55, 64], [43, 55, 65], [41, 53, 60], [43, 55, 64]]),
    "rondo_alla_turca_k331": dict(bpm=120, beats=2, sound="piano", notes=[
        (71, .25), (69, .25), (68, .25), (69, .25), (72, 1), (74, .25), (72, .25), (71, .25), (72, .25), (76, 1),
        (77, .25), (76, .25), (75, .25), (76, .25), (83, .25), (81, .25), (80, .25), (81, .25),
        (83, .25), (81, .25), (80, .25), (81, .25), (84, 1), (81, .5), (84, .5), (83, .5), (81, .5), (79, .5), (81, .5),
        (83, .5), (81, .5), (79, .5), (81, .5), (83, .5), (81, .5), (79, .5), (78, .5), (76, 1)],
        chords=[[45, 57, 60, 64], [45, 57, 60, 64], [45, 57, 60, 64], [40, 56, 59, 62]]),
}
ACOUSTIC = ("mozart", "accordion")


# ------------------------------------------------- acoustic instruments

def piano(f, length):
    n = int((length + 0.6) * SR); t = np.arange(n) / SR
    sig = np.zeros(n)
    for k in range(1, 9):
        fk = k * f * np.sqrt(1 + 0.0004 * k * k)
        if fk > SR * 0.45:
            break
        sig += np.sin(2 * np.pi * fk * t) * np.exp(-t * (1.1 + 0.0022 * f * k)) / k ** 1.3
    hn = noise_hit((n + 2) / SR, 1500, 120, 0.15, int(f) % 97)[:n]
    sig[:len(hn)] += hn
    rel = np.clip(1 - (t - length) / 0.25, 0, 1)
    return sig * np.where(t > length, rel, 1) * np.clip(t / 0.002, 0, 1) * 0.5


def strings(f, length, bright=2800):
    n = int((length + 0.35) * SR); t = np.arange(n) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.4 * t) * np.clip(t * 4, 0, 1)
    ph = np.cumsum(f * vib) / SR
    sig = sum(2 * ((ph * (1 + d) + o) % 1) - 1 for d, o in ((-0.003, 0), (0, .37), (0.003, .71))) / 3
    sig = biquad(biquad(sig, bright, 0.7), 180, kind="hp")
    att = np.clip(t / 0.06, 0, 1)
    rel = np.clip(1 - (t - length) / 0.3, 0, 1)
    return sig * att * np.where(t > length, rel, 1) * 0.45


def reed(f, length, musette=True):
    """Accordion / bayan reed voice: 2-3 slightly detuned reeds beating against each other."""
    n = int((length + 0.12) * SR); t = np.arange(n) / SR
    dets = (-0.0045, 0.0, 0.0045) if musette else (0.0, 0.0015)
    sig = np.zeros(n)
    for i, d in enumerate(dets):
        ph = (t * f * (1 + d) + i * 0.29) % 1
        sig += 0.65 * (2 * ph - 1) + 0.35 * np.where(ph < 0.42, 1.0, -1.0)
    sig /= len(dets)
    sig = biquad(sig, 3600, 0.7) + 0.6 * biquad(sig, 1150, 1.6, kind="bp")
    att = np.clip(t / 0.025, 0, 1)
    rel = np.clip(1 - (t - length) / 0.08, 0, 1)
    return sig * att * np.where(t > length, rel, 1) * 0.35


def timpani(gain=0.6):
    n = int(1.3 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (88 + 18 * np.exp(-t * 20)) * t) * np.exp(-t * 3.0)
    nz = np.zeros(n); h = noise_hit(1.3, 300, 25, 0.25, 41)[:n]; nz[:len(h)] = h
    return (s + nz) * gain


def m2f(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def build_acoustic(dur, bpm, cuts, reveal, seed, festive, style):
    rng = np.random.RandomState(seed)
    n_total = int(dur * SR)
    L = np.zeros(n_total); R = np.zeros(n_total)

    def add(sig, t0, pan=0.0, gain=1.0):
        i = int(t0 * SR)
        if i >= n_total or i < 0:
            return
        m = min(len(sig), n_total - i)
        L[i:i + m] += sig[:m] * gain * (1 - max(0, pan))
        R[i:i + m] += sig[:m] * gain * (1 + min(0, pan))

    if style == "mozart":
        name = list(MOZART)[seed % len(MOZART)]
        P = MOZART[name]
        transpose = int(rng.choice([0, 0, -2, 2, -3]))
        bpm = bpm or P["bpm"]
        beat = 60.0 / bpm
        bar = beat * P["beats"]
        lead = piano if P["sound"] == "piano" else strings
        t0, i = 0.0, 0
        theme_len = sum(b for _, b in P["notes"])
        while t0 < dur - 0.2:
            m, b = P["notes"][i % len(P["notes"])]
            if m is not None:
                add(lead(m2f(m + transpose), b * beat * 0.95), t0, pan=-0.1, gain=1.0 if lead is piano else 0.8)
            t0 += b * beat; i += 1
        nb = int(dur / bar) + 1
        for k in range(nb):
            ch = [c + transpose for c in P["chords"][k % len(P["chords"])]]
            b0 = k * bar
            if P.get("alberti"):
                order = [0, 2, 1, 2] * P["beats"]
                for j in range(P["beats"] * 2):
                    note = ch[order[j] % len(ch)]
                    add(piano(m2f(note + (12 if note < 50 and j else 0)), beat * 0.45), b0 + j * beat / 2, pan=0.15, gain=0.45)
            else:
                add(strings(m2f(ch[0]), bar * 0.98, 1400), b0, pan=0.25, gain=0.55)
                for c in ch[1:]:
                    add(strings(m2f(c), bar * 0.98, 1800), b0, pan=0.3, gain=0.28)
                for j in range(0, P["beats"], 2):
                    add(piano(m2f(ch[0] - 12 if ch[0] > 40 else ch[0]), beat * 0.3), b0 + j * beat, pan=0.1, gain=0.35)
        for c in cuts:
            add(timpani(0.35), c)
        last = [c + transpose for c in P["chords"][0]]
        for c in last + [last[0] + 12, last[-1] + 12]:
            add(strings(m2f(c), max(0.3, dur - reveal - 0.1), 3200), reveal, gain=0.45, pan=0.0)
        add(timpani(0.7), reveal)
        desc = f"style=mozart piece={name} transpose={transpose} bpm={int(bpm)} seed={seed}"
        rv, sz = 0.35, 1.2
    else:  # accordion / bayan
        form = ["waltz", "polka", "tango"][rng.randint(0, 3)]
        minor = rng.rand() < 0.65
        root = 57 + rng.randint(-4, 5)  # around A3
        sc = [0, 2, 3, 5, 7, 8, 11] if minor else [0, 2, 4, 5, 7, 9, 11]
        bpm = bpm or {"waltz": rng.randint(150, 176), "polka": rng.randint(112, 126), "tango": rng.randint(108, 118)}[form]
        beat = 60.0 / bpm
        beats = {"waltz": 3, "polka": 2, "tango": 4}[form]
        bar = beat * beats
        prog = [[0, 3, 4, 0], [0, 5, 3, 4], [0, 3, 0, 4], [0, 4, 5, 3]][rng.randint(0, 4)]
        bars_per = 2 if form == "waltz" else 1

        def deg_m(d, octv=0):
            o, k = divmod(d, 7)
            return root + 12 * (o + octv) + sc[k]

        def chord_deg(bar_i):
            return prog[(bar_i // bars_per) % len(prog)]

        rhythms = {"waltz": [[2, 1], [1, 1, 1], [3], [1.5, .5, 1]],
                   "polka": [[.5, .5, .5, .5], [1, .5, .5], [.5, .5, 1], [.25, .25, .5, 1]],
                   "tango": [[1.5, .5, 1, 1], [.75, .25, .5, .5, 2], [1, 1, .5, .5, 1], [1.5, 1.5, 1]]}[form]
        nb = int(dur / bar) + 1
        prev = 4
        for k in range(nb):
            b0 = k * bar
            cd = chord_deg(k)
            rh = rhythms[rng.randint(0, len(rhythms))] if k % 4 != 3 else [beats]
            tt = b0
            for j, r in enumerate(rh):
                if j == 0 or rng.rand() < 0.5:
                    target = cd + int(rng.choice([0, 2, 4, 7]))
                else:
                    target = prev + int(rng.choice([-1, 1, -2, 2]))
                if k % 4 == 3:
                    target = cd + (0 if (k // 4) % 2 else 2) + 7
                prev = int(np.clip(target, 2, 12))
                if tt < dur - 0.15:
                    add(reed(m2f(deg_m(prev, 1)), r * beat * 0.92), tt, pan=-0.15, gain=0.9)
                tt += r * beat
            bass = deg_m(cd, -2); fifth = deg_m(cd + 4, -2)
            tri = [deg_m(cd + x, -1) for x in (0, 2, 4)]
            if form == "waltz":
                hits = [(0, "b", bass), (1, "c", None), (2, "c", None)]
            elif form == "polka":
                hits = [(0, "b", bass), (.5, "c", None), (1, "b", fifth), (1.5, "c", None)]
            else:
                hits = [(0, "b", bass), (1.5, "b", fifth), (2, "c", None), (3, "c", None), (3.5, "c", None)]
            for off, kind, note in hits:
                ts = b0 + off * beat
                if ts >= dur - 0.1:
                    continue
                if kind == "b":
                    add(reed(m2f(note), beat * 0.45, musette=False), ts, pan=0.2, gain=0.8)
                else:
                    ch = sum(reed(m2f(x), beat * 0.22, musette=False) for x in tri) / 3
                    add(ch, ts, pan=0.25, gain=0.7)
        for c in cuts:
            add(reed(m2f(deg_m(chord_deg(int(c / bar)), -2)), beat * 0.4, False), c, gain=0.6)
        fin = [deg_m(x, 0) for x in (0, 2, 4, 7)]
        add(sum(reed(m2f(x), max(0.3, dur - reveal - 0.1)) for x in fin) / 3, reveal, gain=1.0)
        desc = f"style=accordion form={form} key={NOTE_NAMES[root % 12]} {'minor' if minor else 'major'} bpm={int(bpm)} seed={seed}"
        rv, sz = 0.22, 0.9

    if festive:
        sb = noise_hit(0.12, 5000, 45, 0.08, 5)
        b = 60.0 / bpm
        for i, t0 in enumerate(np.arange(0, dur - 0.3, b / 2)):
            add(sb, t0, pan=0.4 if i % 2 else -0.4, gain=0.8 if i % 2 else 0.5)
    L = comb_reverb(L, rv, sz); R = comb_reverb(R, rv, sz * 1.07)
    mix = np.stack([L, R], axis=1)
    mix = biquad(mix.T, 35, kind="hp").T
    mix /= max(1e-9, np.max(np.abs(mix)))
    rms = np.sqrt((mix ** 2).mean())
    mix = np.tanh(mix * min(3.0, max(1.0, 0.3 / max(rms, 1e-6))))  # gentle loudness match with the electronic styles
    fo = int(0.25 * SR)
    mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
    mix /= max(1e-9, np.max(np.abs(mix)))
    return mix * 0.89, desc


def pick(rng, seq):
    return seq[rng.randint(0, len(seq))]


def build(dur, bpm, cuts, reveal, seed, festive=False, style="auto"):
    if style in ACOUSTIC:
        return build_acoustic(dur, bpm, cuts, reveal, seed, festive, style)
    rng = np.random.RandomState(seed)
    names = list(STYLES)
    if style == "auto":
        style = names[seed % len(names)] if seed >= 0 else pick(rng, names)
    S = STYLES[style]
    if not bpm:
        bpm = float(rng.randint(S["bpm"][0], S["bpm"][1] + 1))
    root_pc = rng.randint(0, 12)
    scale_name = pick(rng, S["scale"])
    scale = SCALES[scale_name]
    base = 55.0 * 2 ** ((root_pc - 9) / 12)  # A1=55 Hz reference -> root in octave 1
    while base < 41:
        base *= 2

    def deg(d, octave=0):
        """Frequency of scale degree d (can be negative / > len)."""
        o, i = divmod(d, len(scale))
        return base * 2 ** (octave + 2 + o + scale[i] / 12)

    n_total = int(dur * SR)
    L = np.zeros(n_total); R = np.zeros(n_total)
    music_L = np.zeros(n_total); music_R = np.zeros(n_total)
    beat = 60.0 / bpm
    step = beat / 4
    steps = int(dur / step) + 1
    swing = S.get("swing", 0.0)

    def st(s):
        return s * step + (swing * step if s % 2 else 0.0)

    def add(sig, t0, pan=0.0, gain=1.0, bus="drum"):
        i = int(t0 * SR)
        if i >= n_total or i < 0:
            return
        m = min(len(sig), n_total - i)
        lt, rt = (L, R) if bus == "drum" else (music_L, music_R)
        lt[i:i + m] += sig[:m] * gain * (1 - max(0, pan))
        rt[i:i + m] += sig[:m] * gain * (1 + min(0, pan))

    # ---- chord progression (degrees of the scale, 1 chord per bar)
    progs = [[0, 5, 2, 6], [0, 3, 4, 0], [0, 6, 5, 4], [0, 2, 5, 3], [0, 4, 5, 3]]
    prog = pick(rng, progs)
    bar = beat * 4

    def chord_at(t):
        return prog[int(t / bar) % len(prog)]

    # ---- motif for melodies (generated, not fixed)
    motif_len = pick(rng, [4, 6, 8])
    motif = [int(x) for x in rng.choice([0, 1, 2, 3, 4, 5, 6, 7, -1, -2], size=motif_len)]
    rhythm = [int(x) for x in rng.choice([1, 1, 2, 2, 3], size=motif_len)]

    # ---- drums
    D = drums(rng)
    K = kick(S["kick"], rng)
    kpat = pick(rng, S["kick_pattern"]) if "kick_pattern" in S else "x...x...x...x..."
    dp = {k: pick(rng, v) for k, v in S["drums"].items()}
    kick_times = []
    for s in range(steps):
        t0 = st(s)
        if t0 > dur - 0.05:
            break
        if kpat[s % 16] == "x":
            add(K, t0, gain=1.0); kick_times.append(t0)
        for name, pat in dp.items():
            c = pat[s % 16]
            if c in "xo":
                pan = {"hc": -0.3, "ho": 0.25, "shk": 0.4, "rim": -0.2, "perc": 0.3, "ride": 0.15}.get(name, 0.0)
                add(D[name], t0, pan=pan, gain=(1.0 if c == "o" else 0.85) * (0.9 + 0.2 * rng.rand()))

    # ---- bass
    B = S.get("bass")
    if B:
        bpat = pick(rng, B["pattern"])
        for s in range(steps):
            t0 = st(s)
            if t0 > dur - 0.1 or bpat[s % 16] != "x":
                continue
            d = chord_at(t0)
            octv = B["octave"] + (1 if B.get("octaves") and s % 2 else 0)
            f = deg(d, octv)
            length = step * (3.5 if B.get("long") else 0.85)
            n = int((length + 0.08) * SR)
            sig = osc(B["kind"], f, n) * env(n, 0.004, length * 0.8, 0.5, 0.05, length)
            sig = biquad(sig, B["cut"] * (1 + 0.4 * rng.rand()), B["q"])
            add(sig, t0, gain=0.55 if B["kind"] != "sine" else 0.75, bus="music")

    # ---- lead / arp / stabs / chords
    Ld = S["lead"]
    lo, hi = Ld["cut"]
    k = 0
    for s in range(0, steps, Ld["rate"]):
        t0 = st(s)
        if t0 > dur - 0.25:
            break
        d = chord_at(t0)
        sweep = lo + (hi - lo) * (0.5 + 0.5 * np.sin(2 * np.pi * t0 / (bar * 2)))
        pan = 0.3 if k % 2 else -0.3
        if Ld.get("acid"):
            if rng.rand() < 0.25:
                k += 1; continue
            f = deg(d + motif[k % motif_len], Ld["octave"] - 1)
            n = int(step * Ld["rate"] * 0.9 * SR)
            sig = biquad(osc("saw", f, n), sweep, Ld["q"]) * env(n, 0.003, 0.12, 0.2, 0.03)
            add(np.tanh(sig * 2) * 0.22, t0, pan=pan, bus="music")
        elif Ld.get("arp"):
            tones = [0, 2, 4, 7, 4, 2] if k % 2 else [0, 2, 4, 2]
            f = deg(d + tones[k % len(tones)], Ld["octave"])
            n = int(0.22 * SR)
            sig = biquad(osc(Ld["kind"], f, n), sweep, Ld["q"]) * env(n, 0.002, 0.08, 0.0, 0.03)
            add(sig * 0.2, t0, pan=pan, bus="music")
        elif Ld.get("stab") or Ld.get("chords"):
            if Ld.get("stab") and rng.rand() < 0.35 and t0 > beat:
                k += 1; continue
            tones = [0, 2, 4, 6] if Ld.get("sevenths") else [0, 2, 4]
            n = int(step * (1.6 if Ld.get("gate") else 1.2) * SR)
            sig = sum(osc(Ld["kind"], deg(d + tt, Ld["octave"]), n) for tt in tones) / len(tones)
            sig = biquad(sig, sweep, Ld["q"]) * env(n, 0.003, 0.09, 0.15, 0.04)
            add(sig * 0.32, t0 + (step * 2 if Ld.get("gate") else 0), pan=pan * 0.5, bus="music")
        elif Ld.get("blip"):
            if rng.rand() < 0.45:
                k += 1; continue
            f = deg(d + motif[k % motif_len], Ld["octave"])
            n = int(0.09 * SR)
            sig = biquad(osc(Ld["kind"], f, n), sweep, Ld["q"]) * env(n, 0.001, 0.03, 0.0, 0.02)
            add(sig * 0.25, t0, pan=pan, bus="music")
        elif Ld.get("melody"):
            if t0 < bar * 0.5 and k == 0:
                pass
            f = deg(d + motif[k % motif_len], Ld["octave"])
            length = step * Ld["rate"] * rhythm[k % motif_len] * 0.9
            n = int((length + 0.1) * SR)
            sig = osc(Ld["kind"], f, n)
            if Ld.get("vibrato"):
                t = np.arange(n) / SR
                sig = np.sin(2 * np.pi * f * t + 0.18 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t * 3, 0, 1)) * 0.6 + sig * 0.4
            sig = biquad(sig, sweep, Ld["q"]) * env(n, 0.01, length, 0.6, 0.08, length)
            add(sig * 0.18, t0, pan=pan * 0.4, bus="music")
        k += 1

    # ---- pad (sustained chords)
    P = S.get("pad")
    if P:
        for b0 in np.arange(0, dur, bar):
            d = chord_at(b0 + 0.01)
            n = int(min(bar + 0.3, dur - b0 + 0.3) * SR)
            sig = sum(osc(P["kind"], deg(d + tt, -1), n) for tt in (0, 2, 4)) / 3
            sig = biquad(sig, P["cut"], 0.7) * env(n, 0.25, 1.0, 0.8, 0.3, n / SR - 0.3)
            add(sig * 0.16, b0, pan=-0.2, bus="music")
            add(sig * 0.16, b0 + 0.012, pan=0.2, bus="music")

    # ---- festive layer
    if festive:
        sb = noise_hit(0.12, 5000, 45, 0.10, 5)
        for s in range(steps):
            t0 = st(s)
            if t0 < dur - 0.3:
                add(sb, t0, pan=0.4 if s % 2 else -0.4, gain=0.9 if s % 4 == 2 else 0.6, bus="music")
        major = [0, 4, 7, 12, 7, 4, 9, 7]
        rel_major = base * 2 ** (3 / 12) * 8
        for i, t0 in enumerate(np.arange(0.0, dur - 0.6, beat * 2)):
            n = int(0.9 * SR); t = np.arange(n) / SR
            f = rel_major * 2 ** (major[i % 8] / 12)
            bell = sum(a * np.sin(2 * np.pi * f * m * t) for m, a in ((1, 1), (2.01, .5), (3.02, .28), (4.17, .15)))
            add(bell * np.exp(-t * 3.2) * 0.14, t0, pan=0.2 if i % 2 else -0.2, bus="music")

    # ---- sidechain duck the music bus on each kick, then reverb
    if kick_times and S.get("duck", 0) > 0:
        tt = np.arange(n_total) / SR
        idx = np.searchsorted(np.array(kick_times), tt, side="right") - 1
        since = np.where(idx >= 0, tt - np.array(kick_times)[np.clip(idx, 0, None)], 10)
        g = 1 - S["duck"] * np.exp(-since / 0.11)
        music_L *= g; music_R *= g
    rv = S.get("reverb", 0.2)
    music_L = comb_reverb(music_L, rv, 1.0); music_R = comb_reverb(music_R, rv, 1.07)
    L += music_L; R += music_R

    # ---- impacts: t=0 (hook), every cut, the reveal; risers before cuts
    def impact(t0, big=False):
        n = int(1.2 * SR); bt = np.arange(n) / SR
        boom = np.sin(2 * np.pi * (38 + 70 * np.exp(-bt * 9)) * bt) * np.exp(-bt * (2.6 if big else 4.5))
        crash = noise_hit(1.2, 3000, 3.2 if big else 6, 0.11 if big else 0.05, 31 + int(t0 * 10))
        add(boom, t0, gain=0.95 if big else 0.5)
        add(crash, t0, pan=0.1)
        if big:
            d = chord_at(t0)
            n2 = int(1.6 * SR)
            hit = sum(osc("supersaw", deg(d + x, 0), n2) for x in (0, 2, 4, 7)) / 4
            add(biquad(hit, 4000, 0.7) * env(n2, 0.002, 0.5, 0.0, 0.2) * 0.35, t0)

    def riser(t_end, length=0.7):
        t0 = max(0.0, t_end - length)
        n = int((t_end - t0) * SR)
        if n < 400:
            return
        x = np.random.RandomState(int(t_end * 100)).randn(n)
        out = np.zeros(n)
        chunks = 12
        for c in range(chunks):
            a, b = c * n // chunks, (c + 1) * n // chunks
            out[a:b] = biquad(x[a:b], 800 + 7000 * (c / chunks) ** 2, 2.0, kind="bp")
        add(out * np.linspace(0, 1, n) ** 2 * 0.22, t0, pan=-0.15)

    impact(0.0)
    for c in cuts:
        riser(c, 0.6); impact(c)
    riser(reveal, 0.9); impact(reveal, big=True)

    mix = np.stack([L, R], axis=1)
    mix = biquad(mix.T, 25, kind="hp").T  # remove DC / sub rumble
    mix = np.tanh(mix * 1.2)
    fo = int(0.25 * SR)  # short tail fade: the reel loops
    mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
    mix /= max(1e-9, np.max(np.abs(mix)))
    desc = f"style={style} key={NOTE_NAMES[root_pc]} {scale_name} bpm={int(bpm)} seed={seed}"
    return mix * 0.89, desc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?")
    ap.add_argument("--dur", type=float, default=10)
    ap.add_argument("--bpm", type=float, default=None)
    ap.add_argument("--cuts", default="")
    ap.add_argument("--reveal", type=float, default=None)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--style", default="auto", help="auto, mozart, accordion or one of: " + ", ".join(STYLES))
    ap.add_argument("--festive", action="store_true", help="Christmas/New Year: sleigh bells + bell melody")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list or not a.out:
        print("styles:", ", ".join(list(STYLES) + list(ACOUSTIC))); print("main rotation: deep_house -> mozart -> accordion"); return
    if a.style != "auto" and a.style not in STYLES and a.style not in ACOUSTIC:
        sys.exit("unknown style; use --list")
    cuts = [float(x) for x in a.cuts.split(",") if x.strip()]
    reveal = a.reveal if a.reveal is not None else max(0.5, a.dur - 2)
    mix, desc = build(a.dur, a.bpm, cuts, reveal, a.seed, a.festive, a.style)
    with wave.open(a.out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print(desc)


if __name__ == "__main__":
    main()
