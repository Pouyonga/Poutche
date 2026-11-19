# Mixage : voix + musique (baissée automatiquement sous la voix) + bruitages. Usage : python3 mix.py sortie.wav
import sys, subprocess, numpy as np, os
SR, LEAD, TOTAL = 48000, 0.3, 305.5
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
scene_starts = [25.9, 41.9, 53.3, 72.8, 89.2, 116.3, 131.6, 145.2, 152.4, 172.2, 181.5, 204.0, 226.3, 234.7, 259.1, 276.0, 281.5, 293.3]
ev = [("whoosh", s - .25) for s in scene_starts]
ev += [("impact", x) for x in [18.8, 22.4, 36.14, 79.26, 103.58, 129.23, 139.29, 146.6, 154.81, 172.3, 201.34, 255.97]]
ev += [("pop", x) for x in [9.2, 39.82, 69.22, 81.5, 82.42, 83.5, 193.38, 194.3, 195.26, 214.94, 216.22, 217.22, 239.89, 242.4, 260.95, 271.13, 273.39, 285.55, 161.75]]
ev += [("ching", x) for x in [3.0, 8.0, 100.7, 105.35, 122.2, 178.5]]
ev += [("riser", 20.5), ("riser", 97.4), ("crowd", 56.5), ("typewriter", 30.3)]
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
