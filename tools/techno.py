"""Original techno music bed for VA Corporation reels (royalty-free, generated in code).

Usage:
  python3 tools/techno.py OUT.wav --dur 12 --bpm 128 --cuts 2.0,4.1,6.3 --reveal 9.5 --seed 7
  --cuts    scene-change times in seconds (riser before, impact on each)
  --reveal  time of the brand/logo reveal (big impact + drop)
"""
import argparse, wave
import numpy as np

SR = 44100


def env_exp(n, k):
    return np.exp(-np.arange(n) / SR * k)


def kick(n=int(0.5 * SR)):
    t = np.arange(n) / SR
    f = 45 + 140 * np.exp(-t * 38)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    click = np.random.RandomState(1).randn(n) * np.exp(-t * 400) * 0.15
    return np.tanh((s + click) * 1.6) * 0.95


def hat(open_=False, seed=2):
    n = int((0.22 if open_ else 0.05) * SR)
    noise = np.random.RandomState(seed).randn(n)
    noise = np.diff(np.concatenate([[0], noise]))  # crude high-pass
    return noise * env_exp(n, 14 if open_ else 90) * (0.20 if open_ else 0.11)


def clap():
    n = int(0.25 * SR)
    noise = np.random.RandomState(3).randn(n)
    e = np.zeros(n)
    for d in (0, 0.012, 0.024):
        i = int(d * SR)
        e[i:] += np.exp(-np.arange(n - i) / SR * 28)
    return noise * e * 0.18


def saw(freq, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((t * freq + phase) % 1.0) - 1


def lowpass(x, cutoff, res=0.0):
    """One-pole-ish resonant lowpass with per-sample cutoff (array or float)."""
    y = np.zeros_like(x)
    cut = np.broadcast_to(cutoff, x.shape)
    a_prev = b_prev = 0.0
    for i in range(len(x)):
        g = min(0.99, 2 * np.pi * cut[i] / SR)
        fb = res * (a_prev - b_prev)
        a_prev = a_prev + g * (x[i] - a_prev + fb)
        b_prev = b_prev + g * (a_prev - b_prev)
        y[i] = b_prev
    return y


def build(dur, bpm, cuts, reveal, seed):
    rng = np.random.RandomState(seed)
    n_total = int(dur * SR)
    L = np.zeros(n_total)
    R = np.zeros(n_total)
    beat = 60.0 / bpm
    step = beat / 4

    def add(sig, t0, pan=0.0, gain=1.0):
        i = int(t0 * SR)
        if i >= n_total:
            return
        m = min(len(sig), n_total - i)
        L[i:i + m] += sig[:m] * gain * (1 - max(0, pan))
        R[i:i + m] += sig[:m] * gain * (1 + min(0, pan))

    K, HC, HO, CL = kick(), hat(False), hat(True), clap()
    root = [55.0, 55.0, 65.41, 49.0][rng.randint(0, 4)]
    pattern = [0, 0, 12, 0, 7, 0, 12, 10, 0, 0, 12, 0, 3, 0, 15, 12]
    acid_notes = [0, 12, 7, 10, 0, 15, 12, 3]

    steps = int(dur / step) + 1
    for s in range(steps):
        t0 = s * step
        if t0 > dur - 0.4:
            break
        in_intro = t0 < 0.9  # short filtered intro before the first drop
        if s % 4 == 0:
            add(K, t0, gain=0.6 if in_intro else 1.0)
        if s % 4 == 2:
            add(HO, t0, pan=0.25)
        add(HC, t0, pan=-0.3, gain=0.8 if s % 2 else 0.5)
        if s % 8 == 4 and not in_intro:
            add(CL, t0, pan=0.1)
        # rolling bass (offbeat 16ths)
        if s % 4 != 0 and not in_intro:
            f = root * 2 ** (pattern[s % 16] / 12)
            n = int(step * SR * 0.9)
            b = lowpass(saw(f, n), 380, 0.2) * env_exp(n, 9) * 0.55
            add(b, t0)
    # acid lead with filter sweep, every 8th note
    n_lead = int(step * 2 * SR * 0.85)
    for s in range(0, steps, 2):
        t0 = s * step
        if t0 < 1.0 or t0 > dur - 0.6:
            continue
        f = root * 4 * 2 ** (acid_notes[(s // 2) % 8] / 12)
        sweep = 500 + 2600 * (0.5 + 0.5 * np.sin(2 * np.pi * t0 / (beat * 8)))
        sig = lowpass(saw(f, n_lead), sweep, 0.85) * env_exp(n_lead, 7) * 0.22
        add(sig, t0, pan=0.35 if (s // 2) % 2 else -0.35)
    # risers + impacts on scene cuts and reveal
    for c in list(cuts) + [reveal]:
        n = int(0.6 * SR)
        t = np.arange(n) / SR
        rise = rng.randn(n) * (t / 0.6) ** 2.2 * 0.22
        add(rise, max(0, c - 0.6), pan=-0.2)
        add(rise[::-1] * 0, c)  # placeholder keep alignment
        boom_n = int(0.9 * SR)
        bt = np.arange(boom_n) / SR
        boom = np.sin(2 * np.pi * (40 + 60 * np.exp(-bt * 10)) * bt) * np.exp(-bt * 3.5)
        add(boom, c, gain=0.9 if c == reveal else 0.45)
        add(CL, c, gain=0.8)
    # mix bus: soft clip, fade, normalize
    mix = np.stack([L, R], axis=1)
    mix = np.tanh(mix * 1.15)
    fl = int(0.6 * SR)
    mix[-fl:] *= np.linspace(1, 0, fl)[:, None]
    fi = int(0.05 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)[:, None]
    mix /= max(1e-9, np.max(np.abs(mix)))
    return mix * 0.89


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--dur", type=float, default=12)
    ap.add_argument("--bpm", type=float, default=128)
    ap.add_argument("--cuts", default="")
    ap.add_argument("--reveal", type=float, default=None)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    cuts = [float(x) for x in a.cuts.split(",") if x.strip()]
    reveal = a.reveal if a.reveal is not None else a.dur - 3
    mix = build(a.dur, a.bpm, cuts, reveal, a.seed)
    with wave.open(a.out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    main()
