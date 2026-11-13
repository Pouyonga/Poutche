# Mixage : voix + musique (baissée automatiquement sous la voix) + bruitages. Usage : python3 mix.py sortie.wav
import sys, subprocess, numpy as np, os
SR, LEAD, TOTAL = 48000, 0.3, 404.0
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
A, B = load(f"{D}/audio/musique_a.mp3"), load(f"{D}/audio/musique_b.mp3")
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

S = {n: load(f"{D}/audio/sfx_{n}.mp3") for n in ["whoosh", "impact", "ching", "pop", "tick", "scratch", "riser", "typewriter", "crowd", "notif"]}
G = {"whoosh": db(-15), "impact": db(-12), "ching": db(-14), "pop": db(-16), "tick": db(-18), "scratch": db(-16),
     "riser": db(-16), "typewriter": db(-18), "crowd": db(-24), "notif": db(-15)}
scene_starts = [4.45, 12.25, 17.95, 26.6, 31.4, 42.4, 52.7, 59.6, 72.6, 83.0, 96.85, 106.95, 116.2, 129.8, 139.5, 146.85, 173.6,
                186.5, 202.95, 214.5, 233.7, 241.55, 249.4, 259.95, 269.1, 276.15, 289.25, 302.0, 312.9, 340.7, 355.7, 365.55,
                374.45, 380.0, 392.3]
ev = [("whoosh", s - .25) for s in scene_starts]
ev += [("impact", x) for x in [139.81, 234.01, 269.42, 49.67, 58.07, 70.07, 305.46, 353.11, 13.88, 116.29, 245.32]]
ev += [("pop", x) for x in [1.2, 38.23, 39.67, 41.03, 199.64, 200.94, 166.76, 167.56, 168.33, 272.17, 273.53, 274.85, 298.05,
                            299.05, 299.69, 362.05, 363.29, 364.09, 383.85, 316.88, 324.88, 335.44, 14.2, 14.45, 14.7, 191.56, 194.56,
                            4.92, 9.5, 10.75, 145.64]]
ev += [("scratch", x) for x in [1.15, 15.15, 204.54, 206.1, 226.0]]
ev += [("ching", x) for x in [91.9, 110.9, 245.6, 171.52]]
ev += [("tick", 217.0 + k) for k in range(5)]
ev += [("notif", x) for x in [218.16, 219.54]]
ev += [("riser", 20.3), ("typewriter", 28.4), ("crowd", 31.6), ("crowd", 35.5), ("crowd", 39.0)]
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
