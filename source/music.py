# Music bed + sound design + final mix for the Laszlo TikTok.
# usage: python3 music.py <voice.wav> <out_dir>
import sys, os, subprocess, json
import numpy as np, soundfile as sf, pretty_midi
from scipy import signal

SR = 44100
DUR = 40.0
N = int(SR * DUR)
VOICE, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
SF2 = "/usr/share/sounds/sf2/MuseScore_General_Full.sf2"
rng = np.random.default_rng(7)

def buf(): return np.zeros((N, 2), np.float32)
def place(dst, x, t, gain=1.0, pan=0.0):
    if x.ndim == 1: x = np.stack([x * (1 - max(0, pan)), x * (1 + min(0, pan))], 1)
    i = int(t * SR)
    if i >= N: return
    j = min(N, i + len(x)); dst[i:j] += x[:j - i] * gain
def db(x): return 10 ** (x / 20)
def env_exp(n, tau): return np.exp(-np.arange(n) / (tau * SR)).astype(np.float32)
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'low', fs=SR, output='sos'), x, axis=0).astype(np.float32)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'high', fs=SR, output='sos'), x, axis=0).astype(np.float32)
def bp(x, lo, hi, o=2): return signal.sosfilt(signal.butter(o, [lo, hi], 'band', fs=SR, output='sos'), x, axis=0).astype(np.float32)
def noise(n): return rng.standard_normal(n).astype(np.float32)
def norm(x, peak=1.0): return x * (peak / (np.abs(x).max() + 1e-9))

# simple stereo reverb (decorrelated decaying noise IRs)
def reverb(x, secs=1.8, wet=.25, damp=6000):
    n = int(secs * SR)
    irs = []
    for s in range(2):
        ir = noise(n) * env_exp(n, secs / 6.5); ir = lp(ir, damp); ir[:int(.012 * SR)] = 0
        irs.append(ir / np.sqrt((ir ** 2).sum()))
    mono = x.mean(1) if x.ndim == 2 else x
    w = np.stack([signal.fftconvolve(mono, irs[0])[:len(mono)], signal.fftconvolve(mono, irs[1])[:len(mono)]], 1)
    dry = x if x.ndim == 2 else np.stack([x, x], 1)
    return (dry * (1 - wet) + w * wet * 2.2).astype(np.float32)

# ---------------- MUSIC: harmony / MIDI ----------------
A, F_, C, G, E, Dm = "A", "F", "C", "G", "E", "Dm"
CH = {"A": [45, 52, 57, 60, 64], "F": [41, 48, 53, 57, 60], "C": [36, 43, 48, 52, 55],
      "G": [43, 50, 55, 59, 62], "E": [40, 47, 52, 56, 59], "Dm": [38, 45, 50, 53, 57]}
ROOT = {"A": 33, "F": 29, "C": 36, "G": 31, "E": 28, "Dm": 26}
MEL = {"A": [76, 72], "F": [77, 72], "C": [79, 76], "G": [74, 71], "E": [76, 71], "Dm": [74, 69]}
BAR, T0 = 2.0, 3.0           # 120 bpm, bars start at 3.0 s
# bar index -> chord (b0 = 3.0 s)
PROG = [A, F_, C, G,  A, F_, C, G,  A, F_, C, G,  A, E,  A, F_, G, A]
def bt(b, beat=0.0): return T0 + b * BAR + beat * BAR / 4

pm = pretty_midi.PrettyMIDI(initial_tempo=120)
piano = pretty_midi.Instrument(program=0, name="piano")
strings = pretty_midi.Instrument(program=49, name="strings")
choir = pretty_midi.Instrument(program=52, name="choir")
celesta = pretty_midi.Instrument(program=8, name="celesta")
low = pretty_midi.Instrument(program=48, name="lowstr")
def note(inst, p, s, e, v): inst.notes.append(pretty_midi.Note(velocity=int(np.clip(v, 1, 127)), pitch=int(p), start=s, end=e))

# hook: low drone + stabs
note(low, 33, 0.0, 3.05, 70); note(low, 45, 0.0, 3.05, 60)
for p in (33, 45, 57): note(piano, p, 0.02, 2.0, 100)
for p in (57, 60, 64, 69): note(piano, p, 1.85, 3.0, 92)

for b, ch in enumerate(PROG):
    s = bt(b); c = CH[ch]
    last = b == len(PROG) - 1
    e = 40.0 if last else s + BAR
    drop = 14 <= b <= 16
    brk = b == 8
    # piano 8th-note arpeggio (soft in context, steadier in story)
    if not last:
        pat = [c[0], c[2], c[3], c[4], c[3], c[2], c[3], c[1]]
        for k, p in enumerate(pat):
            v = 52 + (10 if k == 0 else 0) + (8 if b >= 5 else 0) + (10 if drop else 0) - (14 if brk else 0)
            note(piano, p + (12 if drop and k % 2 else 0), s + k * .25, s + k * .25 + .45, v)
    else:
        for p in c[:4]: note(piano, p, s, 40.0, 70)
        note(piano, 81, s, 40.0, 55)
    # melody (from story on), celesta doubles in drop
    if b >= 5 and not brk and not last and b != 13:
        m = MEL[ch]
        note(piano, m[0], s, s + 1.0, 74 + (10 if drop else 0)); note(piano, m[1], s + 1.0, s + 2.0, 66 + (10 if drop else 0))
        if drop or b >= 9:
            note(celesta, m[0] + 12, s, s + 1.0, 60 if not drop else 80); note(celesta, m[1] + 12, s + 1.0, s + 2.0, 55 if not drop else 75)
    # strings pad
    if b >= 2:
        v = 45 + (20 if b >= 9 else 0) + (25 if drop else 0) - (10 if brk else 0)
        for p in c[1:4]: note(strings, p + 12, s, e, v)
        note(strings, c[0], s, e, v - 5)
    if b == 13:  # tension: tremolo-ish swell on E
        for p in (52, 56, 59, 64): note(strings, p, s, s + BAR, 85)
    if drop or last:
        for p in (c[2] + 12, c[3] + 12, c[4] + 12): note(choir, p, s, e, 70 if drop else 50)
for inst in (piano, strings, choir, celesta, low): pm.instruments.append(inst)
pm.write(f"{OUT}/music.mid")
subprocess.run(["fluidsynth", "-ni", "-q", "-g", "0.6", "-r", str(SR), "-F", f"{OUT}/music_inst.wav", SF2, f"{OUT}/music.mid"], check=True)
inst, sr = sf.read(f"{OUT}/music_inst.wav", dtype="float32"); assert sr == SR
mus = buf(); mus[:min(N, len(inst))] = inst[:N]
# lowpass the breakdown (Quatre jours passent) for a muffled feel
a, b_ = int(bt(8) * SR), int(bt(9) * SR)
mus[a:b_] = lp(mus[a:b_], 900, 2) * 1.3

# ---------------- DRUMS (synth) ----------------
def kick808(pitch=55, decay=.55, punch=1.0):
    n = int(decay * 3 * SR); t = np.arange(n) / SR
    f = pitch + 160 * np.exp(-t * 38)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * env_exp(n, decay)
    click = hp(noise(int(.004 * SR)), 2000) * .4 * punch
    x[:len(click)] += click
    return np.tanh(x * 1.6).astype(np.float32)
def bass808(midi, dur):
    f = 440 * 2 ** ((midi - 69) / 12); n = int((dur + .1) * SR); t = np.arange(n) / SR
    fr = f * (1 + .9 * np.exp(-t * 45))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR)
    e = np.minimum(1, t / .005) * np.where(t < dur, 1, np.exp(-(t - dur) * 40)) * (0.75 + .25 * np.exp(-t * 3))
    return np.tanh(x * e * 1.8).astype(np.float32) * .8
def clap():
    n = int(.35 * SR); x = np.zeros(n, np.float32)
    for o in (0, .011, .022):
        k = int(o * SR); m = int(.03 * SR); x[k:k + m] += noise(m) * env_exp(m, .006)
    tail = noise(n) * env_exp(n, .09) * .5; x += tail
    return bp(x, 900, 5000).astype(np.float32)
def hat(open_=False):
    n = int((.25 if open_ else .05) * SR)
    return hp(noise(n) * env_exp(n, .08 if open_ else .012), 7000, 4) * .7
def snare():
    n = int(.25 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 190 * t) * env_exp(n, .05)
    return (hp(noise(n), 1500) * env_exp(n, .07) * .8 + body * .6).astype(np.float32)
def crash():
    n = int(2.5 * SR); return hp(noise(n) * env_exp(n, .7), 5000, 2) * .6

drums = buf(); bass = buf()
K, CL, HC, HO, SN, CR = kick808(), clap(), hat(), hat(True), snare(), crash()
DRUM_BARS = [5, 6, 7, 9, 10, 11, 12, 14, 15, 16]
for b in DRUM_BARS:
    s = bt(b); drop = b >= 14; ch = PROG[b]
    for st16 in (0, 6, 10) if not drop else (0, 3, 6, 10, 14):
        place(drums, K, s + st16 * BAR / 16, .9)
    place(drums, CL, s + BAR / 2, .75 if not drop else .9, .0)
    for k in range(8):
        place(drums, HC, s + k * BAR / 8, .35 if k % 2 else .5, .25)
    if b % 2 == 1 or drop:  # hat rolls at end of bar
        for k in range(6): place(drums, HC, s + BAR * 12 / 16 + k * BAR / 24, .3, -.2)
    # 808 bass on roots
    for st16, l16 in ((0, 6), (6, 4), (10, 6)):
        place(bass, bass808(ROOT[ch] + 12 if drop and st16 == 10 else ROOT[ch], l16 * BAR / 16 * .95), s + st16 * BAR / 16, .55 if not drop else .7)
# build: snare roll during bar 13 (29-31) until 30.3, accelerating
t = bt(13)
for k in range(30):
    tt = t + 1.3 * (1 - (1 - k / 30) ** 1.6)
    if tt > 30.3: break
    place(drums, SN, tt, .15 + .5 * k / 30)
place(drums, CR, bt(14), .8); place(drums, CR, bt(9), .4); place(drums, CR, bt(5), .45)
place(drums, K, bt(14), 1.1); place(drums, K, bt(17), .8)
drums = reverb(drums, 1.0, .12)

# ---------------- SFX ----------------
sfx = buf()
def impact(size=1.0):
    n = int(2.5 * SR); t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(30 + 60 * np.exp(-t * 6)) / SR) * env_exp(n, .6)
    hit = lp(noise(n) * env_exp(n, .12), 1800) * .8
    return reverb(np.tanh((sub + hit) * 1.4) * size, 2.5, .3)
def whoosh(dur=.6, up=True):
    n = int(dur * SR); x = noise(n); t = np.linspace(0, 1, n)
    out = np.zeros(n, np.float32); hop = 512
    for i in range(0, n, hop):
        f = (400 + 5000 * (t[i] if up else 1 - t[i]))
        seg = x[max(0, i - 2048):i + hop]
        y = bp(seg, f * .6, min(f * 1.6, 18000))[-min(hop, n - i):]
        out[i:i + len(y)] = y
    e = np.sin(np.pi * t) ** 2
    st = np.stack([out * e, np.roll(out, 300) * e], 1)
    return reverb(st, 1.2, .25) * 1.2
def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * np.cumsum(200 * 2 ** (3 * t / dur)) / SR) * .25
    nz = hp(noise(n), 2000) * .5
    e = (t / dur) ** 2.2
    return reverb(((tone + nz) * e).astype(np.float32), 1.5, .3)
def pop(f=900):
    n = int(.09 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * np.cumsum(f * np.exp(-t * 25) + 180) / SR) * env_exp(n, .025)).astype(np.float32)
def tick(f=2600):
    n = int(.03 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) * env_exp(n, .004) + hp(noise(n), 3000) * env_exp(n, .002) * .5).astype(np.float32)
def key_click():
    n = int(.045 * SR)
    return bp(noise(n) * env_exp(n, .006), 1500, 7000) * (.6 + .4 * rng.random())
def bell(freqs, decay=.5, amp=(1, .6, .4)):
    n = int(decay * 4 * SR); t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * t) * env_exp(n, decay / (1 + i)) for i, (f, a) in enumerate(zip(freqs, amp)))
    return x.astype(np.float32)
def coin_clink():
    f = 2400 * (0.9 + .25 * rng.random())
    return bell([f, f * 1.47, f * 2.31], .12) * .5
def kaching():
    x = np.zeros(int(1.6 * SR), np.float32)
    thunk = lp(noise(int(.08 * SR)) * env_exp(int(.08 * SR), .02), 600) * 1.2
    x[:len(thunk)] += thunk
    b = bell([1568, 2093, 3136, 4186], .45, (1, .8, .5, .3)) * .6
    k = int(.06 * SR); x[k:k + len(b)] += b[:len(x) - k]
    for i in range(6):
        c = coin_clink(); k = int((.08 + .05 * i) * SR); x[k:k + len(c)] += c[:len(x) - k] * .6
    return reverb(x, 1.4, .25)
def ding():
    return reverb(bell([1318.5, 2637], .35) * .5 + np.pad(bell([1975.5, 3951], .4) * .5, (int(.09 * SR), 0))[:int(.35 * 4 * SR)], 1.2, .25)
def thud():
    n = int(.4 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 70 * t) * env_exp(n, .08) + lp(noise(n), 400) * env_exp(n, .03)).astype(np.float32)

# --- timeline (matches render2.py animations)
place(sfx, impact(1.0), 0.0, .9)
place(sfx, pop(700), .25, .35, -.4); place(sfx, pop(800), .45, .35, .4)
place(sfx, whoosh(.45), .3, .5)
place(sfx, impact(.7), 1.85, .7); place(sfx, kaching(), 1.9, .35)
place(sfx, riser(.9), 2.15, .35); place(sfx, whoosh(.5, False), 2.85, .55)
for k in range(16):                     # year counter 2026 -> 2010
    tt = 3.1 + 1.1 * (1 - (1 - k / 16) ** .5) ; place(sfx, tick(2200 + 40 * k), tt, .25)
place(sfx, pop(500), 4.6, .45); place(sfx, bell([987.8, 1975.5], .4) * .4, 4.75, .5)
for k in range(10):                     # price sliding down
    place(sfx, tick(3000 - 180 * k), 6.6 + 2.0 * (1 - (1 - k / 10) ** 2) , .2)
place(sfx, thud(), 9.1, .6)
place(sfx, whoosh(.55), 11.85, .6)
place(sfx, pop(650), 12.1, .3)
tt = 13.0
while tt < 16.4:                        # typing
    place(sfx, key_click(), tt, .45, float(rng.uniform(-.3, .3))); tt += float(rng.uniform(.045, .11))
place(sfx, ding(), 16.2, .45)
place(sfx, whoosh(.5, False), 19.05, .5)
for k in range(5): place(sfx, tick(1800), 19.4 + k * .27, .55)   # clock ticks
for k in range(4): place(sfx, tick(1200), 19.535 + k * .27, .35)
place(sfx, whoosh(.5), 20.65, .55)
for i in range(10):                     # coins fly + land
    place(sfx, coin_clink(), 22.9 + i * .13 + .85, .55, .5)
place(sfx, whoosh(.35), 22.9, .35)
place(sfx, whoosh(.4, False), 24.95, .45); place(sfx, pop(600), 25.3, .4); place(sfx, pop(700), 25.45, .4)
place(sfx, ding(), 26.4, .4)
place(sfx, whoosh(.5), 27.85, .55); place(sfx, pop(500), 28.25, .4)
place(sfx, riser(1.6), 29.3, .5)
place(sfx, impact(1.1), 31.0, .9)
tt = 31.0                               # counter ticks, accelerating
while tt < 34.6:
    place(sfx, tick(2400 + 900 * (tt - 31) / 3.6), tt, .2, float(rng.uniform(-.2, .2)))
    tt += max(.035, .16 * (1 - (tt - 31) / 3.6))
place(sfx, kaching(), 34.6, .8); place(sfx, impact(.6), 34.6, .5)
place(sfx, whoosh(.5, False), 35.75, .5)
place(sfx, pop(700), 36.1, .45); place(sfx, pop(600), 36.6, .3); place(sfx, pop(800), 36.75, .3)
place(sfx, ding(), 38.1, .45)

# ---------------- VOICE chain ----------------
vraw, vsr = sf.read(VOICE, dtype="float32")
if vraw.ndim == 2: vraw = vraw.mean(1)
v = signal.resample_poly(vraw, SR, vsr).astype(np.float32)
v = np.pad(v, (0, max(0, N - len(v))))[:N]
v = hp(v, 85, 2)
# EQ: warmth +2.5 dB @ 180 Hz, cut mud -2 dB @ 450 Hz, presence +3 dB @ 3.5k, air +2 dB shelf 10k
def peq(x, f0, gdb, q):
    A_ = 10 ** (gdb / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * A_, -2 * np.cos(w), 1 - al * A_]; a = [1 + al / A_, -2 * np.cos(w), 1 - al / A_]
    return signal.lfilter(b, a, x).astype(np.float32)
v = peq(v, 180, 2.5, .8); v = peq(v, 450, -2, 1.0); v = peq(v, 3500, 3, .9); v = peq(v, 10000, 2, .7)
# compressor (RMS, 4:1 above -20 dB)
def compress(x, thr=-20, ratio=4, att=.005, rel=.12):
    e = np.abs(x); out = np.zeros_like(e); ga = np.exp(-1 / (att * SR)); gr = np.exp(-1 / (rel * SR))
    lvl = 0.0
    for i in range(0, len(e), 64):
        m = e[i:i + 64].max(); lvl = ga * lvl + (1 - ga) * m if m > lvl else gr * lvl + (1 - gr) * m
        out[i:i + 64] = lvl
    ldb = 20 * np.log10(out + 1e-9); g = np.where(ldb > thr, (thr + (ldb - thr) / ratio) - ldb, 0)
    return (x * 10 ** (g / 20)).astype(np.float32)
v = norm(v, .9); v = compress(v, -22, 3.5); v = norm(v, .95)
vs = reverb(v, 0.7, .06, 7000)

# ---------------- MIX ----------------
# sidechain: duck music when voice talks
env = np.abs(v); win = int(.05 * SR)
env = np.convolve(env, np.ones(win) / win, 'same')
env = env / (env.max() + 1e-9)
sm = np.zeros_like(env); a_, r_ = np.exp(-1 / (.02 * SR / 64)), np.exp(-1 / (.35 * SR / 64))
lvl = 0.0
for i in range(0, N, 64):
    m = env[i:i + 64].max(); lvl = a_ * lvl + (1 - a_) * m if m > lvl else r_ * lvl + (1 - r_) * m
    sm[i:i + 64] = lvl
duck = 1 - .6 * np.clip(sm / .25, 0, 1)
music = mus * db(-1) + drums * db(-4) + bass * db(-5)
music = music * duck[:, None]
# fade out the end
fo = np.ones(N, np.float32); k = int(38.5 * SR); fo[k:] = np.linspace(1, 0, N - k) ** 1.5
mix = vs * db(0) + music * db(-13) + sfx * db(-13)
mix *= fo[:, None]
sf.write(f"{OUT}/stem_voice.wav", vs, SR); sf.write(f"{OUT}/stem_music.wav", music, SR); sf.write(f"{OUT}/stem_sfx.wav", sfx, SR)
sf.write(f"{OUT}/mix_raw.wav", mix / (np.abs(mix).max() + 1e-9) * .9, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/mix_raw.wav", "-af",
                "loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.89", "-ar", str(SR), f"{OUT}/mix.wav"], check=True)
print("ok")
