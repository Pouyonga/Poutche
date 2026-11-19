# Mixage premium Shein : voix aux décalages du montage, musique qui coupe avant les chiffres chocs, montées sur générique et chapitres.
import sys, os, json, subprocess, wave
import numpy as np
SR, LEAD, TOTAL = 48000, 0.3, 312.0
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BF = os.path.join(D, "../black_friday/audio")
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
db = lambda x: 10 ** (x / 20)
N = int(TOTAL * SR)
voice = np.zeros((N, 2), np.float32)
offs = json.load(open(f"{D}/offsets.json"))
for n, o in offs.items():
    x = load(f"{D}/voix/s{n}.mp3"); i = int((o + LEAD) * SR); voice[i:i + len(x)] += x[:N - i]

A, B = load(f"{BF}/musique_a.mp3"), load(f"{BF}/musique_b.mp3")
xf = 4 * SR
def cross(x, y):
    r = np.linspace(0, 1, xf)[:, None]; return np.concatenate([x[:-xf], x[-xf:] * (1 - r) + y[:xf] * r, y[xf:]])
mus = cross(B, A)[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))

env = np.abs(voice).max(1); k = int(.25 * SR)
c = np.concatenate([[0], np.cumsum(env, dtype=np.float64)]); idx = np.arange(N)
env = (c[np.clip(idx + k // 2, 0, N)] - c[np.clip(idx - k // 2, 0, N)]) / k
g = np.where(env > 0.012, db(-19), db(-8)).astype(np.float64)
# coupures avant les chiffres chocs (0,5 s de silence musical puis reprise)
CHOCS = [1.28, 14.04, 57.97, 91.18, 114.62, 155.69, 191.49, 227.43, 257.23, 290.1]
for t in CHOCS:
    a, b = int((t + LEAD - .55) * SR), int((t + LEAD) * SR); g[a:b] = 0.0
# montées : générique et cartes de chapitre (musique plus forte)
for a_, b_ in [(28.15, 30.6), (68.54, 69.9), (121.5, 122.9), (164.3, 165.7), (194.2, 195.6), (261.98, 263.4), (302, 312)]:
    g[int((a_ + LEAD) * SR):int((b_ + LEAD) * SR)] = db(-4)
sm = np.convolve(g, np.ones(int(.06 * SR)) / int(.06 * SR), "same") if False else g
# lissage rapide par moyenne glissante (somme cumulée)
w = int(.08 * SR); cg = np.concatenate([[0], np.cumsum(g)]); sm = (cg[np.clip(idx + w // 2, 0, N)] - cg[np.clip(idx - w // 2, 0, N)]) / w
fade = np.ones(N); fade[:int(.4 * SR)] = np.linspace(0, 1, int(.4 * SR)); fade[-int(3 * SR):] = np.linspace(1, 0, int(3 * SR))
out = voice + mus * (sm * fade * db(-6))[:, None]

S = {n: load(f"{BF}/sfx_{n}.mp3") for n in ["whoosh", "impact", "ching", "pop", "tick", "scratch", "riser", "typewriter", "notif"]}
G = {"whoosh": db(-14), "impact": db(-10), "ching": db(-14), "pop": db(-17), "tick": db(-18), "scratch": db(-15), "riser": db(-13), "typewriter": db(-18), "notif": db(-15)}
def add(name, t):
    x = S[name]; i = int((t + LEAD) * SR); j = min(N, i + len(x)); out[i:j] += x[:j - i] * G[name]
TL = [28.15, 30.65, 47.6, 68.54, 69.94, 84.4, 100.1, 109.4, 121.5, 122.9, 149.9, 164.3, 165.73, 194.2, 195.59, 214.1, 233.2, 261.98, 263.38, 292.1, 302.0]
for t in TL: add("whoosh", t - .25)
for t in CHOCS: add("impact", t)
for t in [26.0, 67.2, 120.2, 163.0, 192.9, 260.7]: add("riser", t)
for t in [5.36, 5.48, 5.6, 5.72, 5.84, 5.96, 12.16, 13.0, 36.21, 39.77, 42.73, 96.7, 98.22, 99.26, 125.47, 130.87, 137.39, 144.47, 175.76, 183.73, 202.23, 210.23, 244.95, 253.27]: add("pop", t)
for t in [101.94, 156.43, 229.0]: add("scratch", t)
for t in [7.04, 96.9]: add("notif", t)
for t in [1.9, 44.0, 114.9]: add("ching", t)
add("typewriter", 236.3)
peak = np.abs(out).max(); out = np.tanh(out / peak * 1.2) / np.tanh(1.2) * .95
tmp = sys.argv[1] + ".raw.wav"
with wave.open(tmp, "wb") as wv:
    wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), sys.argv[1]], check=True)
os.remove(tmp); print("ok")
