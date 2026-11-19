# Shorts verticaux Shein. Usage : python3 short_shein.py 1|2 sortie.mp4 [--preview t...]
import os, sys, math, subprocess, wave
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../black_friday/video"))
import gfx, gfx2
SW, SH = 1080, 1920
gfx.W, gfx.H, gfx2.W, gfx2.H = SW, SH, SW, SH
from gfx2 import *
from gfx import stamp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../shein/video"))
import shein as S
gfx2.BGS["pink"] = (S.PINK, (255, 175, 210))
FPS = 30
VO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../shein/voix")
BF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../black_friday/audio")
def put(img, L, x, y, a=1.0, s=1.0, r=0.0): rotate_paste(img, L, x, y, r, a, max(.02, s))
def pin(t, t0, d=.4): return back(prog(t, t0, d), 2.2)
def lab(img, x, y, s, t, t0, size=80, fg=INK, bg=PAPER, rot=-2): pop_word(img, x, y, s, t, t0, size, fg, bg, rot)

# ------- Short 1 : le secret des 100 pièces -------
# audio : s1 [0 ; 15,0] puis s3 [14,64 ; 50,68] (s3 commence à 66,04 dans la timeline d'origine)
A1 = [("s1", 0.0, 15.0, 0.0), ("s3", 14.64, 50.68, 15.4)]
def M1(orig): return 15.4 + (orig - 80.68)
DUR1 = 15.4 + (50.68 - 14.64) + 2.4
def sc1(img, t):
    if t < 5.3:
        pop_word(img, 540, 640, fmt(41.8 * eo(prog(t, 0, 1.6)), 1), t, 0, 300, INK, PAPER, -3)
        lab(img, 540, 880, "MILLIARDS $", t, 1.28, 120, PAPER, INK, 2); lab(img, 540, 1060, "pour Shein en 2025", t, 2.64, 64, INK, SUN, -1)
        mascot(img, 780, 1500, t, 320, "surpris"); return "sun"
    if t < 12.0:
        for i in range(4): put(img, S.tshirt(260, [S.PINK, SKY, MINT, GRAPE][i]), 300 + (i % 2) * 480, 520 + (i // 2) * 360 + math.sin(t * 3 + i) * 12, 1, pin(t, 5.36 + i * .12), (-6, 5, 7, -4)[i])
        lab(img, 540, 1260, "QUELQUES EUROS…", t, 6.0, 110, PAPER, INK, -2)
        if t >= 9.3: lab(img, 540, 1460, "et la France veut l'arrêter", t, 9.32, 70, PAPER, RED2, 2)
        return "pink"
    if t < 15.4:
        for i, (w_, t0, col) in enumerate([("AMENDES", 12.16, RED2), ("LOI SPÉCIALE", 13.0, GRAPE), ("TRIBUNAL", 14.04, INK)]):
            lab(img, 540, 600 + i * 260, w_, t, t0, 140, PAPER, col, (-4, 3, -2)[i])
        return "sun"
    if t < M1(92.7):
        lab(img, 540, 380, "LE SECRET ?", t, M1(80.68), 110, PAPER, INK, -2)
        pop_word(img, 540, 760, "100", t, M1(87.28), 380, INK, PAPER, -4)
        lab(img, 540, 1060, "exemplaires seulement", t, M1(87.72), 76, PAPER, INK, 2)
        mascot(img, 540, 1450, t, 300, "surpris" if t > M1(87.3) else "neutre"); return "pink"
    if t < M1(100.76):
        put(img, S.phone(300), 540, 760, 1, pin(t, M1(92.0)), 5)
        for i, (w_, t0, col) in enumerate([("CLICS", M1(92.8), SKY), ("PANIERS", M1(94.32), SUN), ("VENTES", M1(95.36), MINT)]):
            lab(img, 540, 1240 + i * 150, w_, t, t0, 90, INK, col, (-4, 3, -2)[i])
        if t >= M1(97.93):
            rrect(img, (0, 0, SW, SH), 0, RED2, 1)
            lab(img, 540, 900, "ÇA NE SE VEND PAS ?", t, M1(96.36), 90, PAPER, INK, 0); lab(img, 540, 1080, "STOP.", t, M1(97.93), 200, RED2, PAPER, -4)
        return "mint"
    if t < M1(112.48):
        n = 1 + int(8 * eo(prog(t, M1(102.2), 2.4)))
        for i in range(n): put(img, S.tshirt(190), 260 + (i % 3) * 280, 560 + (i // 3) * 300, 1, pin(t, M1(100.9) + i * .2, .3), (i * 23) % 14 - 7)
        lab(img, 540, 1500, "ÇA SE VEND ? ON RELANCE", t, M1(101.32), 70, INK, MINT, 2)
        if t >= M1(110.72): pop_word(img, 540, 1700, "× 8 RÉASSORTS", t, M1(110.72), 100, PAPER, INK, -3)
        return "sun"
    if t < M1(115.88) + 1.0:
        lab(img, 540, 760, "IL NE DEVINE", t, M1(112.48), 120, PAPER, None, 0); lab(img, 540, 900, "PAS LA MODE.", t, M1(113.2), 120, PAPER, None, 0)
        lab(img, 540, 1120, "IL LA TESTE.", t, M1(114.46), 150, NIGHT, SUN, -3); return "night"
    lab(img, 540, 760, "LA VIDÉO COMPLÈTE", t, DUR1 - 2.2, 90, PAPER, None, 0); lab(img, 540, 900, "SUR LA CHAÎNE ↓", t, DUR1 - 1.9, 110, SUN, None, 0)
    mascot(img, 540, 1300, t, 320, "clin"); return "night"

# ------- Short 2 : la France contre Shein -------
A2 = [("s6", 24.32, 65.49, 1.6)]
def M2(orig): return 1.6 + (orig - 211.81)
DUR2 = 1.6 + (65.49 - 24.32) + 2.4
def sc2(img, t):
    if t < M2(215.86):
        lab(img, 540, 420, "LA FRANCE", t, 0.0, 150, PAPER, INK, -3); lab(img, 540, 600, "CONTRE SHEIN", t, .3, 130, PAPER, RED2, 3)
        if t >= M2(212.13): lab(img, 540, 1000, "l'État demande", t, M2(212.13), 70, INK, None, 0)
        if t >= M2(213.69): lab(img, 540, 1160, "SUSPENSION 3 MOIS", t, M2(213.69), 100, PAPER, INK, -2)
        mascot(img, 540, 1550, t, 280, "fache"); return "sky"
    if t < M2(225.25):
        put(img, S.gavel(420), 540, 640, 1, pin(t, M2(215.9), .35), -15 + 25 * math.sin(max(0, t - M2(218.3)) * 9) * (1 - prog(t, M2(218.3), .8)))
        lab(img, 540, 1000, "19 DÉC. 2025", t, M2(216.17), 100, INK, SUN, 3); lab(img, 540, 1230, "REFUSÉ", t, M2(219.33), 170, PAPER, RED2, -4)
        if t >= M2(221.0): lab(img, 540, 1440, "« disproportionnée »", t, M2(221.53), 70, PAPER, INK, 2)
        if t >= M2(222.93): lab(img, 540, 1590, "confirmé en appel", t, M2(223.77), 64, INK, MINT, -2)
        return "paper"
    if t < M2(241.62):
        lab(img, 540, 380, "ALORS : LA LOI", t, M2(225.25), 110, PAPER, INK, -2)
        lab(img, 540, 560, "promulguée en juillet 2026", t, M2(228.29), 64, INK, PAPER, 2)
        if t >= M2(233.7): lab(img, 540, 820, "PÉNALITÉ PAR VÊTEMENT", t, M2(233.7), 80, PAPER, INK, -2)
        if t >= M2(236.85): pop_word(img, 540, 1060, "jusqu'à 20 €", t, M2(236.85), 160, INK, SUN, 3)
        if t >= M2(238.29): lab(img, 540, 1280, "d'ici 2030 · max 50 % du prix", t, M2(238.29), 60, PAPER, INK, -1)
        return "mint"
    if t < M2(248.37):
        lab(img, 540, 720, "PUB INTERDITE", t, M2(243.53), 150, PAPER, RED2, -3); lab(img, 540, 920, "DÈS 2027", t, M2(242.25), 150, INK, PAPER, 3)
        if t >= M2(246.21): lab(img, 540, 1160, "même les influenceurs", t, M2(247.01), 80, PAPER, INK, -2)
        mascot(img, 540, 1550, t, 280, "surpris"); return "coral"
    if t < DUR2 - 2.3:
        lab(img, 540, 760, "« PAS CHER, VITE,", t, M2(249.13), 110, PAPER, None, 0); lab(img, 540, 900, "PARTOUT »", t, M2(250.29), 130, PAPER, None, 0)
        lab(img, 540, 1120, "C'EST FINI ?", t, M2(250.97), 140, NIGHT, CORAL, -3); return "night"
    lab(img, 540, 760, "LA VIDÉO COMPLÈTE", t, DUR2 - 2.2, 90, PAPER, None, 0); lab(img, 540, 900, "SUR LA CHAÎNE ↓", t, DUR2 - 1.9, 110, SUN, None, 0)
    mascot(img, 540, 1300, t, 320, "clin"); return "night"

def frame(sc, t):
    tmp = Image.new("RGB", (SW, SH)); kind = sc(tmp, t)
    img = background(kind, t, SW, SH); sc(img, t)
    T(img, 540, 1860, "L'ENVERS DU BUSINESS", "anton", 40, PAPER if kind == "night" else INK, "mm", .6)
    return img

def audio(parts, dur, out, chocs, pops):
    SR = 48000
    def load(p):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    N = int(dur * SR); v = np.zeros((N, 2), np.float32)
    for name, a, b, at in parts:
        x = load(f"{VO}/{name}.mp3")[int(a * SR):int(b * SR)]; i = int(at * SR); v[i:i + len(x)] += x[:N - i]
    m = load(f"{BF}/musique_a.mp3")[:N]; m = np.pad(m, ((0, N - len(m)), (0, 0)))
    env = np.abs(v).max(1); k = int(.3 * SR); c = np.concatenate([[0], np.cumsum(env)]); i = np.arange(N)
    env = (c[np.clip(i + k // 2, 0, N)] - c[np.clip(i - k // 2, 0, N)]) / k
    g = np.where(env > .012, 10 ** (-19 / 20), 10 ** (-9 / 20))
    for t in chocs: g[int((t - .5) * SR):int(t * SR)] = 0
    f = np.ones(N); f[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR))
    o = v + m * (g * f * 10 ** (-5 / 20))[:, None]
    sfx = {n: load(f"{BF}/sfx_{n}.mp3") for n in ["pop", "impact", "whoosh"]}
    def add(n, t, gdb):
        x = sfx[n]; j = int(t * SR); e = min(N, j + len(x)); o[j:e] += x[:e - j] * 10 ** (gdb / 20)
    for t in chocs: add("impact", t, -11)
    for t in pops: add("pop", t, -15)
    o = np.tanh(o / np.abs(o).max() * 1.2) / np.tanh(1.2) * .95
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((o * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    which, out = sys.argv[1], sys.argv[2]
    sc, dur, parts = (sc1, DUR1, A1) if which == "1" else (sc2, DUR2, A2)
    if "--preview" in sys.argv:
        for ts in sys.argv[sys.argv.index("--preview") + 1:]: frame(sc, float(ts)).save(f"{out}_{ts}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SW}x{SH}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p", out + ".v.mp4"], stdin=subprocess.PIPE)
    for n in range(int(dur * FPS)): p.stdin.write(frame(sc, n / FPS).tobytes())
    p.stdin.close(); p.wait()
    if which == "1": chocs, pops = [1.28, 14.04, M1(87.28), M1(97.93), M1(110.72), M1(114.46)], [6.0, 12.16, 13.0, M1(92.8), M1(94.32), M1(95.36), M1(101.32)]
    else: chocs, pops = [M2(219.33), M2(236.85), M2(243.53), M2(250.97)], [0.0, .3, M2(213.69), M2(216.17), M2(233.7), M2(238.29), M2(247.01)]
    audio(parts, dur, out + ".a.wav", chocs, pops)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", out + ".v.mp4", "-i", out + ".a.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(out + ".v.mp4"); os.remove(out + ".a.wav"); print("ok", out, round(dur, 1))
