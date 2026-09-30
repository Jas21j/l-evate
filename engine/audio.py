"""L-evate sound: synthesise a soundtrack, in code, from a scene's cue list.

usage: python3 audio.py cues.json out.wav --T 40 [--loop] [--key E] [--gain 1.0]

The scene registers every sound with L.cue(t, sound, {...}); stills.js dumps
them to <name>.cues.json. Nothing is sampled: every voice below is built from
sines and filtered noise, so the whole mix is reproducible and license-free.

Cue sounds
  key, click, tick, pop, thud, whoosh_in, whoosh_out, sub, ding, blip_down,
  jingle {notes, step}, chord {chord, until}, drone {until}, swell {dur}
Common options: v (volume 0..1+), pan (-1..1)
"""
import json, sys, wave, argparse
import numpy as np

SR = 48000
RNG = np.random.default_rng(11)
NOTE_INDEX = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6,
              'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
CHORDS = {  # voiced low → high, wide and warm
    'E': ['E2', 'B2', 'E3', 'G#3', 'B3', 'E4'], 'C#m': ['C#2', 'G#2', 'C#3', 'E3', 'G#3', 'C#4'],
    'A': ['A1', 'E2', 'A2', 'C#3', 'E3', 'A3'], 'B': ['B1', 'F#2', 'B2', 'D#3', 'F#3', 'B3'],
    'Esus': ['E2', 'B2', 'E3', 'A3', 'B3', 'E4'], 'F#m': ['F#2', 'C#3', 'F#3', 'A3', 'C#4'],
}


def hz(name: str) -> float:
    name = name.strip()
    pitch, octave = (name[:2], name[2:]) if len(name) > 2 and name[1] in '#b' else (name[:1], name[1:])
    return 440.0 * 2 ** ((NOTE_INDEX[pitch] + 12 * (int(octave) + 1) - 69) / 12)


def tt(dur): return np.arange(int(dur * SR)) / SR


def lowpass(x, cutoff):
    """One-pole low-pass; cutoff may be a scalar or a per-sample array."""
    c = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = np.exp(-2 * np.pi * c / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):  # short signals only; beds use lowpass_fixed
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def lowpass_fixed(x, cutoff):
    """Fast one-pole low-pass for long signals, via an IIR computed with cumsum tricks."""
    from numpy.fft import rfft, irfft
    a = np.exp(-2 * np.pi * cutoff / SR)
    n = len(x)
    ir_len = min(n, int(SR * 0.2))
    ir = (1 - a) * a ** np.arange(ir_len)
    size = 1 << int(np.ceil(np.log2(n + ir_len)))
    return irfft(rfft(x, size) * rfft(ir, size), size)[:n]


def highpass(x, cutoff): return x - lowpass_fixed(x, cutoff)


def layer(*parts):
    """Sum signals of different lengths, padding the shorter ones with silence."""
    out = np.zeros(max(len(p) for p in parts))
    for p in parts:
        out[: len(p)] += p
    return out


# -------------------------------------------------------------------- voices
def v_key(v=1.0):
    t = tt(0.045)
    n = RNG.standard_normal(len(t)) * np.exp(-t / 0.004)
    n = highpass(n, 1800) * 0.5
    body = np.sin(2 * np.pi * (170 + RNG.uniform(-20, 20)) * t) * np.exp(-t / 0.008) * 0.35
    return (n + body) * 0.55 * v


def v_click(v=1.0):
    t = tt(0.05)
    n = highpass(RNG.standard_normal(len(t)), 2500) * np.exp(-t / 0.0025) * 0.7
    tone = np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.006) * 0.25
    low = np.sin(2 * np.pi * 220 * t) * np.exp(-t / 0.012) * 0.3
    return (n + tone + low) * v


def v_tick(v=1.0, f=1800):
    t = tt(0.06)
    return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.012) * 0.35 * v


def v_pop(v=1.0):
    t = tt(0.12)
    f = 520 + 420 * (1 - np.exp(-t / 0.02))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035) * 0.45 * v


def v_thud(v=1.0):
    t = tt(0.32)
    f = 55 + 95 * np.exp(-t / 0.05)
    s = np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / 0.09)
    n = lowpass_fixed(RNG.standard_normal(len(t)), 900) * np.exp(-t / 0.015) * 0.6
    return (s * 0.7 + n) * 0.6 * v


def v_whoosh(dur=0.7, rising=True, v=1.0):
    t = tt(dur)
    u = t / dur
    shape = np.sin(np.pi * u) ** 2 if rising is None else (u ** 2.2 if rising else (1 - u) ** 1.6)
    cutoff = 300 + 5200 * (u if rising else 1 - u)
    n = lowpass(RNG.standard_normal(len(t)), cutoff)
    return n * shape * 0.5 * v


def v_sub(v=1.0):
    t = tt(1.4)
    f = 46 + 18 * np.exp(-t / 0.08)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / 0.45) * 0.8 * v


def v_pluck(f, dur=1.2, v=1.0, bright=1.0):
    t = tt(dur)
    out = np.zeros_like(t)
    for k in range(1, 9):
        if f * k > 12000:
            break
        out += np.sin(2 * np.pi * f * k * t + k) / k ** (1.3 / bright) * np.exp(-t * (2.5 + 1.8 * k))
    attack = np.minimum(1, t / 0.003)
    return out * attack * 0.35 * v


def v_bell(f, dur=2.4, v=1.0):
    t = tt(dur)
    index = 2.2 * np.exp(-t / 0.35)
    s = np.sin(2 * np.pi * f * t + index * np.sin(2 * np.pi * f * 3.5 * t))
    s += 0.35 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t / 0.4)
    return s * np.exp(-t / 0.9) * np.minimum(1, t / 0.002) * 0.22 * v


def v_ding(v=1.0):
    a = layer(v_pluck(hz('B5'), 0.9, 0.9), v_bell(hz('B5'), 1.6, 0.8))
    b = layer(v_pluck(hz('E6'), 1.2, 1.0), v_bell(hz('E6'), 2.0, 1.0))
    out = np.zeros(int(SR * 2.2))
    out[:len(a)] += a
    off = int(SR * 0.09)
    out[off:off + len(b)] += b[:len(out) - off]
    return out * 0.8 * v


def v_blip_down(i=0, v=1.0):
    t = tt(0.16)
    f0 = hz('E5') * 2 ** (-i * 2 / 12)
    f = f0 * (1 - 0.35 * (t / 0.16))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05) * 0.3 * v


def v_jingle(notes=('E5', 'B5', 'E6'), step=0.12, v=1.0, big=False):
    """The launch motif: a rising figure, plucked and belled, on a sub thump."""
    length = int(SR * (len(notes) * step + 3.0))
    out = np.zeros(length)
    for i, n in enumerate(notes):
        f = hz(n)
        last = i == len(notes) - 1
        voice = layer(v_pluck(f, 1.6 if last else 0.8, 1.0, 1.2), v_bell(f, 2.8 if last else 1.2, 1.0 if last else 0.6))
        if last:
            voice = layer(voice, v_pluck(f / 2, 1.8, 0.5))  # the octave below makes the landing feel wide
        off = int(SR * i * step)
        out[off:off + len(voice)] += voice[:length - off]
    s = v_sub(0.9 if big else 0.7)
    out[:len(s)] += s
    return out * 0.9 * v


def pad_note(f, dur, v=1.0, seed=0):
    t = tt(dur)
    r = np.random.default_rng(seed)
    out = np.zeros_like(t)
    for d in (-0.004, 0.0, 0.0045):  # three detuned voices ≈ ±7 cents
        ph = r.uniform(0, 2 * np.pi)
        for k, a in ((1, 1.0), (2, 0.32), (3, 0.14), (4, 0.06)):
            out += a * np.sin(2 * np.pi * f * (1 + d) * k * t + ph * k)
    trem = 1 + 0.06 * np.sin(2 * np.pi * 0.23 * t + seed)
    return out * trem * 0.05 * v


def v_chord(chord, dur, v=1.0, attack=1.4, release=1.8):
    notes = CHORDS[chord]
    total = dur + release
    t = tt(total)
    env = np.minimum(1, t / attack) * np.clip((total - t) / release, 0, 1) ** 1.5
    out = np.zeros_like(t)
    for i, n in enumerate(notes):
        out += pad_note(hz(n), total, 1.0 / (1 + 0.15 * i), seed=i)
    return lowpass_fixed(out * env, 2400) * v


def v_drone(dur, v=1.0):
    """Unresolved tension: a low cluster and rumble for the 'before' section."""
    total = dur + 0.6
    t = tt(total)
    env = np.minimum(1, t / 1.2) * np.clip((total - t) / 0.6, 0, 1)
    out = layer(pad_note(hz('E2'), total, 1.0, 3), pad_note(hz('F2'), total, 0.7, 4), pad_note(hz('A#2'), total, 0.5, 5))
    rumble = lowpass_fixed(RNG.standard_normal(len(t)), 120) * 0.12
    return (lowpass_fixed(out, 900) + rumble) * env * v


def v_swell(dur=1.0, v=1.0):
    """A rising reversed-cymbal-like swell that lands on its end time."""
    t = tt(dur)
    u = t / dur
    n = highpass(RNG.standard_normal(len(t)), 3000) * u ** 3 * 0.35
    return n * v


VOICES = {
    'key': lambda c: v_key(c.get('v', 1)),
    'click': lambda c: v_click(c.get('v', 1)),
    'tick': lambda c: v_tick(c.get('v', 1), c.get('f', 1800)),
    'pop': lambda c: v_pop(c.get('v', 1)),
    'thud': lambda c: v_thud(c.get('v', 1)),
    'whoosh_in': lambda c: v_whoosh(c.get('dur', 0.6), False, c.get('v', 1)),
    'whoosh_out': lambda c: v_whoosh(c.get('dur', 0.6), True, c.get('v', 1)),
    'whoosh': lambda c: v_whoosh(c.get('dur', 0.8), None, c.get('v', 1)),
    'sub': lambda c: v_sub(c.get('v', 1)),
    'ding': lambda c: v_ding(c.get('v', 1)),
    'blip_down': lambda c: v_blip_down(c.get('i', 0), c.get('v', 1)),
    'jingle': lambda c: v_jingle(tuple(c.get('notes', ('E5', 'B5', 'E6'))), c.get('step', 0.12), c.get('v', 1), c.get('big', False)),
    'chord': lambda c: v_chord(c['chord'], c['until'] - c['t'], c.get('v', 1)),
    'drone': lambda c: v_drone(c['until'] - c['t'], c.get('v', 1)),
    'swell': lambda c: v_swell(c.get('dur', 1.0), c.get('v', 1)),
}
WET = {'jingle': 0.32, 'ding': 0.3, 'chord': 0.22, 'drone': 0.15, 'pop': 0.12, 'blip_down': 0.18, 'swell': 0.2, 'sub': 0.05}
LEADS_IN = {'swell'}
# The mix, stated explicitly. Every voice is normalised to its own peak, then
# placed at this level (linear peak), so a jingle cannot bury a click and a
# sustained pad cannot bury everything. Beds are levelled by RMS instead.
PEAK = {'jingle': 0.85, 'ding': 0.5, 'thud': 0.5, 'click': 0.42, 'key': 0.24, 'tick': 0.2, 'pop': 0.3,
        'blip_down': 0.3, 'sub': 0.7, 'whoosh': 0.22, 'whoosh_in': 0.32, 'whoosh_out': 0.24, 'swell': 0.3}
RMS = {'chord': 0.05, 'drone': 0.065}  # these end on their cue time rather than start on it


def reverb_ir(seconds=1.8, seed=5):
    r = np.random.default_rng(seed)
    t = tt(seconds)
    ir = r.standard_normal((2, len(t))) * np.exp(-t / (seconds / 5.5))
    ir[:, : int(SR * 0.012)] *= np.linspace(0, 1, int(SR * 0.012))
    ir = np.stack([lowpass_fixed(ch, 5200) for ch in ir])
    # Unit energy per channel, so the reverb adds space rather than gain.
    return ir / np.sqrt(np.sum(ir ** 2, axis=1, keepdims=True))


def convolve(x, ir):
    from numpy.fft import rfft, irfft
    n = len(x) + ir.shape[1]
    size = 1 << int(np.ceil(np.log2(n)))
    X = rfft(x, size)
    return np.stack([irfft(X * rfft(ch, size), size)[: len(x)] for ch in ir])


def mix(cues, T, loop=False, gain=1.0):
    n = int(SR * (T + 4))
    dry = np.zeros((2, n))
    send = np.zeros(n)
    for c in cues:
        name = c['sound']
        if name not in VOICES:
            print('unknown sound', name, file=sys.stderr)
            continue
        s = VOICES[name](c)
        v = c.get('v', 1.0)
        if name in RMS:
            level = np.sqrt(np.mean(s ** 2)) or 1
            s = s / level * RMS[name] * v
        else:
            s = s / (np.max(np.abs(s)) or 1) * PEAK.get(name, 0.3) * v
        start = int(SR * c['t']) - (len(s) if name in LEADS_IN else 0)
        if start < 0:
            s, start = s[-start:], 0
        end = min(n, start + len(s))
        s = s[: end - start]
        pan = c.get('pan', 0.0)
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        dry[0, start:end] += s * l
        dry[1, start:end] += s * r
        send[start:end] += s * WET.get(name, 0.06)
    wet = convolve(send, reverb_ir())
    out = dry + wet * 0.9
    out = np.stack([highpass(ch, 28) for ch in out])
    if loop:  # fold the tail past T back onto the start so the loop is seamless
        tail = out[:, int(SR * T):]
        out = out[:, : int(SR * T)].copy()
        out[:, : tail.shape[1]] += tail[:, : out.shape[1]]
    else:
        out = out[:, : int(SR * T)]
        fade = int(SR * 0.4)
        out[:, -fade:] *= np.linspace(1, 0, fade)
    out = out * gain
    over = np.abs(out) > 0.8                     # soft-knee limiter above -2 dBFS
    out[over] = np.sign(out[over]) * (0.8 + 0.2 * np.tanh((np.abs(out[over]) - 0.8) / 0.2))
    return out


def measure_lufs(stereo):
    """Integrated loudness (EBU R128), measured by ffmpeg on a temporary file."""
    import subprocess, tempfile, os, re
    tmp = tempfile.mktemp(suffix='.wav')
    write_wav(tmp, stereo)
    out = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp, '-af', 'ebur128=framelog=quiet', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    os.remove(tmp)
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1])


def limit(x, ceiling=0.84, release=0.08, block=64):
    """Stereo-linked look-ahead peak limiter: instant attack one block early,
    exponential release. Only the loudest transients are touched."""
    env = np.max(np.abs(x), axis=0)
    n = len(env)
    e = np.pad(env, (0, (-n) % block)).reshape(-1, block).max(1)
    g = np.minimum(1.0, ceiling / np.maximum(e, 1e-9))
    g = np.minimum(g, np.roll(g, -1))
    rel = np.exp(-block / (SR * release))
    for i in range(1, len(g)):
        g[i] = min(g[i], g[i - 1] * rel + (1 - rel))
    return x * np.repeat(g, block)[:n]


def master(stereo, lufs=-16.0):
    """Bring the mix to a loudness target, then limit. Two passes, because
    limiting lowers loudness slightly."""
    for _ in range(2):
        stereo = limit(stereo * 10 ** ((lufs - measure_lufs(stereo)) / 20))
    return stereo


def write_wav(path, stereo):
    pcm = (np.clip(stereo.T, -1, 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cues')
    ap.add_argument('out')
    ap.add_argument('--T', type=float, required=True)
    ap.add_argument('--loop', action='store_true')
    ap.add_argument('--gain', type=float, default=1.0)
    ap.add_argument('--lufs', type=float, default=-16.0, help='integrated loudness target; 0 skips')
    a = ap.parse_args()
    cues = json.load(open(a.cues))
    stereo = mix(cues, a.T, a.loop, a.gain)
    if a.lufs:
        stereo = master(stereo, a.lufs)
    write_wav(a.out, stereo)
    print('wrote', a.out, len(cues), 'cues')
