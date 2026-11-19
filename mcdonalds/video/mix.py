# Mixage : voix + musique (baissée automatiquement sous la voix) + bruitages. Usage : python3 mix.py sortie.wav
import sys, subprocess, numpy as np, os
SR, LEAD, TOTAL = 48000, 0.3, 445.0
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
def db(x): return 10 ** (x / 20)
N = int(TOTAL * SR)
out = np.zeros((N, 2), np.float32)
def add(sig, t, gain=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if i < N: out[i:j] += sig[:j - i] * gain

voice = load(f"{D}/voix_off_complete_nicolas.mp3")
vbuf = np.zeros((N, 2), np.float32); i = int(LEAD * SR); vbuf[i:i + len(voice)] = voice[:N - i]

# musique : A puis B puis A, fondus enchaînés de 4 s
A, B = load(f"{D}/../black_friday/audio/musique_b.mp3"), load(f"{D}/../black_friday/audio/musique_a.mp3")
xf = 4 * SR
def cross(x, y):
    r = np.linspace(0, 1, xf)[:, None]
    return np.concatenate([x[:-xf], x[-xf:] * (1 - r) + y[:xf] * r, y[xf:]])
mus = cross(cross(A, B), A)[:N]
mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
# enveloppe de la voix -> atténuation de la musique (« ducking »)
env = np.abs(vbuf).max(1)
k = int(.25 * SR); c = np.concatenate([[0], np.cumsum(env, dtype=np.float64)]); idx = np.arange(N); lo = np.clip(idx - k // 2, 0, N); hi = np.clip(idx + k // 2, 0, N); env = (c[hi] - c[lo]) / np.maximum(hi - lo, 1)
speak = np.clip(env / 0.02, 0, 1)
duck = db(-13) * speak + db(-4) * (1 - speak)
# lissage de l'atténuation (attaque / relâchement)
sm = np.empty_like(duck); a_att, a_rel = 1 - np.exp(-1 / (.05 * SR)), 1 - np.exp(-1 / (.6 * SR)); v = duck[0]
for n in range(0, N, 64):  # par blocs pour la vitesse
    tgt = duck[n]; v += (tgt - v) * (1 - (1 - (a_att if tgt < v else a_rel)) ** 64); sm[n:n + 64] = v
mus *= (sm * db(-7))[:, None]
fade = np.ones(N); fl = int(3 * SR); fade[-fl:] = np.linspace(1, 0, fl); fi = int(.5 * SR); fade[:fi] = np.linspace(0, 1, fi)
mus *= fade[:, None]
out += mus + vbuf

S = {n: load(f"{D}/../black_friday/audio/sfx_{n}.mp3") for n in ["whoosh", "impact", "ching", "pop", "tick", "scratch", "riser", "typewriter", "crowd", "notif"]}
G = {"whoosh": db(-15), "impact": db(-12), "ching": db(-14), "pop": db(-16), "tick": db(-18), "scratch": db(-16),
     "riser": db(-16), "typewriter": db(-18), "crowd": db(-24), "notif": db(-15)}
scene_starts = [14.2, 28.8, 48.4, 67.5, 75.1, 88.4, 104.5, 118.8, 133.7, 140.3, 159.7, 187.8, 201.4, 215.2, 256.2, 270.4, 280.1,
                295.6, 315.2, 328.6, 347.1, 355.9, 379.6, 392.6, 399.4, 424.5, 433.4]
ev = [("whoosh", s - .25) for s in scene_starts]
ev += [("impact", x) for x in [19.15, 20.24, 24.04, 39.0, 67.57, 71.6, 99.71, 116.4, 132.67, 138.38, 145.47, 212.8, 245.87, 305.46 - 0, 353.11 - 0]]
ev = [e for e in ev if not (e[0] == "impact" and e[1] in (305.46, 353.11))]
ev += [("pop", x) for x in [12.88, 43.65, 60.29, 63.37, 167.61, 175.13, 192.49, 194.49, 206.85, 208.97, 261.81, 262.69, 263.93, 267.28,
                            291.97, 294.05, 329.96, 335.8, 337.48, 338.4, 363.73, 365.15, 366.91, 383.88, 428.4, 272.17]]
ev += [("ching", x) for x in [5.0, 91.0 - 0, 151.0, 244.5, 371.55, 301.6]]
ev = [e for e in ev if not (e[0] == "ching" and e[1] == 91.0)]
ev += [("scratch", x) for x in [19.15, 19.35]]
ev += [("typewriter", 75.4), ("typewriter", 90.75), ("riser", 243.8), ("riser", 21.0), ("tick", 401.28), ("tick", 404.72), ("tick", 409.36)]
for n, t in ev:
    add(S[n], t + LEAD, G[n])

# limiteur doux + normalisation
peak = np.abs(out).max()
out = np.tanh(out / max(peak, 1e-6) * 1.2) / np.tanh(1.2) * 0.95
tmp = sys.argv[1] + ".raw.wav"
import wave
with wave.open(tmp, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), sys.argv[1]], check=True)
os.remove(tmp)
print("ok", sys.argv[1])
