# Démo « style 2 » : l'accroche de la vidéo McDonald's (voix s1, 0 à 28 s). Usage : python3 demo.py sortie [--preview t...]
import sys, os, math, subprocess
from gfx2 import *

FPS, LEAD, DUR = 30, 0.3, 29.0

def sc_world(img, t):
    # 0 → 6,4 s : « Chaque année… 139 milliards de dollars »
    put = lambda L, x, y, a=1, s=1, r=0: rotate_paste(img, L, x, y, r, a, s)
    for i, (x, y, t0) in enumerate([(380, 330, .9), (620, 250, 1.2), (1300, 260, 1.5), (1540, 360, 1.8), (500, 600, 2.1), (1420, 620, 2.4)]):
        p = back(prog(t, t0, .4))
        if p > 0: put(icon_building(110), x, y + math.sin(t * 2 + i) * 8, 1, max(.02, p * .9), math.sin(t + i) * 3)
    p = back(prog(t, 0.0, .5), 2.2)
    put(icon_burger(420), 960, 520 + math.sin(t * 2.2) * 10, 1, max(.02, p), math.sin(t * 1.4) * 4)
    if t >= 3.6:
        v = 139.4 * eo(prog(t, 3.6, 1.6))
        pop_word(img, 960, 860, fmt(v, 1) + " MILLIARDS $", t, 3.6, 120, INK, PAPER, -2)
    mascot(img, 1680, 860, t, 230, "surpris" if t > 4.9 else "content", look=(-1, 0) if t > 4 else (0, 0), wave=1 if t < 2.5 else 0, alpha=eo(prog(t, .5, .4)))
    sx, sy = shake(t, 4.9)
    return 1.0 + .05 * eo(prog(t, 0, 6.4)), sx, sy, 0

def sc_food(img, t):
    # 6,4 → 9 s : « Des burgers, des frites, des milkshakes »
    for i, (fn, x, t0, lab) in enumerate([(icon_burger, 520, 6.6, "BURGERS"), (icon_fries, 960, 7.36, "FRITES"), (icon_shake, 1400, 8.04, "MILKSHAKES")]):
        p = back(prog(t, t0, .4), 2.6)
        if p <= 0: continue
        L = fn(300 if fn is icon_burger else 200)
        rotate_paste(img, L, x, 470 + math.sin(t * 3 + i) * 12, (-6, 4, -3)[i], 1, max(.02, p))
        pop_word(img, x, 790, lab, t, t0 + .05, 70, PAPER, INK, (-4, 3, -2)[i])
    return 1.0 + .03 * prog(t, 6.4, 2.6), 0, 0, 0

def sc_share(img, t):
    # 9 → 14,3 s : « Mais McDonald's n'en encaisse qu'une petite partie. Moins d'un cinquième. »
    x0, x1, y = 260, 1660, 430
    a = eo(prog(t, 9.1, .4))
    rrect(img, (x0, y, x1, y + 150), 40, PAPER, a, outline=INK + (255,), width=8)
    fill_p = 1 - eo(prog(t, 10.9, 1.2)) * (1 - 26.9 / 139.4)
    if a > 0:
        rrect(img, (x0 + 10, y + 10, x0 + 10 + (x1 - x0 - 20) * fill_p, y + 140), 32, SUN if fill_p > .5 else CORAL, 1)
    pop_word(img, 560, 340, "139,4 Md$ vendus", t, 9.3, 64, INK, None, -2)
    if t >= 11.0: pop_word(img, x0 + (x1 - x0) * 26.9 / 139.4 / 2 + 40, 690, "26,9 Md$ pour McDonald's", t, 11.4, 64, INK, PAPER, 2)
    if t >= 12.88: pop_word(img, 1350, 820, "MOINS D'1/5 !", t, 12.88, 110, PAPER, RED2, -5)
    mascot(img, 1680, 300, t, 210, "triste" if t > 12.0 else "neutre", look=(-1, 1), alpha=1)
    sx, sy = shake(t, 12.88)
    return 1.04 - .04 * eo(prog(t, 9.0, 5.0)), sx, sy, 0

def sc_rich(img, t):
    # 14,3 → 18,1 s : « une des entreprises les plus rentables de la planète »
    p = back(prog(t, 14.4, .5), 2.0)
    rotate_paste(img, icon_trophy(340), 960, 430 + math.sin(t * 3) * 10, math.sin(t * 2) * 4, 1, max(.02, p))
    confetti(img, t, 15.3, 70, (100, 0, W - 100, 0), 3)
    pop_word(img, 960, 730, "UNE DES PLUS RENTABLES", t, 15.4, 92, INK, PAPER, -2)
    pop_word(img, 960, 885, "DE LA PLANÈTE", t, 16.4, 92, PAPER, INK, 2)
    mascot(img, 300, 820, t, 220, "content", wave=1, alpha=1)
    return 1.0 + .06 * eo(prog(t, 14.3, 3.8)), 0, 0, 0

def sc_plate(img, t):
    # 18,1 → 20,2 s : « Son secret n'est pas dans ton assiette »
    rotate_paste(img, icon_plate(620), 960, 640, 0, 1, 1)
    rotate_paste(img, icon_burger(300), 960, 560 + math.sin(t * 3) * 6, 0, 1, 1)
    if t >= 19.2:
        p = eo(prog(t, 19.2, .25))
        strike_line(img, 700, 360, 700 + 520 * p, 360 + 400 * p, 1, RED2, 40)
        p2 = eo(prog(t, 19.4, .25))
        strike_line(img, 1220, 360, 1220 - 520 * p2, 360 + 400 * p2, 1, RED2, 40)
    pop_word(img, 960, 210, "PAS DANS TON ASSIETTE", t, 18.6, 100, PAPER, INK, -2)
    mascot(img, 1660, 800, t, 210, "fache", look=(-1, 0), alpha=1)
    sx, sy = shake(t, 19.2, 18)
    return 1.02, sx, sy, 0

def sc_ground(img, t):
    # 20,2 → 21,6 s : « Il est sous tes pieds » — la caméra plonge vers le sol
    d = ImageDraw.Draw(img)
    d.rectangle((0, 640, W, H), fill=(120, 80, 50)); d.rectangle((0, 620, W, 660), fill=(80, 190, 90))
    for i in range(14): d.ellipse((i * 150 + 30, 760 + (i % 3) * 60, i * 150 + 70, 790 + (i % 3) * 60), fill=(150, 105, 70))
    p = back(prog(t, 20.4, .5))
    rotate_paste(img, icon_building(300), 960, 640 - 200 * max(.02, p), 0, 1, max(.02, p))
    pop_word(img, 960, 880, "LE TERRAIN", t, 20.9, 110, INK, SUN, -3)
    mascot(img, 420, 500, t, 200, "surpris", look=(1, 1), alpha=1)
    return 1.0 + .08 * eo(prog(t, 20.2, 1.4)), 0, -60 * eo(prog(t, 20.2, 1.4)), 0

def sc_title(img, t):
    # 21,6 → fin : titre (moment fort, fond nuit)
    lines = [[("COMMENT", 22.76), ("McDONALD'S", 23.0), ("GAGNE", 23.68)], [("VRAIMENT", 24.04), ("SON ARGENT", 24.48)]]
    for li, (ln, y) in enumerate(zip(lines, (380, 560))):
        ws = [tw(w_, "anton", 130) + 60 for w_, _ in ln]
        x = 960 - sum(ws) / 2
        for (wd, t0), wpx in zip(ln, ws):
            pop_word(img, x + wpx / 2, y, wd, t, t0, 130, SUN if li == 1 else PAPER, None, 0)
            x += wpx
    if t >= 26.5: pop_word(img, 960, 780, "(et pas avec les burgers)", t, 26.52, 70, NIGHT, CORAL, -3, "bold")
    mascot(img, 1650, 880, t, 200, "clin" if t > 26.8 else "content", alpha=eo(prog(t, 22.0, .4)))
    sx, sy = shake(t, 24.04, 10)
    return 1.0 + .03 * math.sin(t * .8), sx, sy, 0

SCENES = [(0.0, sc_world, "sun"), (6.4, sc_food, "coral"), (9.0, sc_share, "sky"), (14.25, sc_rich, "mint"),
          (18.1, sc_plate, "grape"), (20.2, sc_ground, "sky"), (21.6, sc_title, "night")]
SWIPE = {6.4: INK, 9.0: SUN, 14.25: CORAL, 18.1: SKY, 20.2: MINT, 21.6: SUN}

def frame(t):
    tv = t - LEAD
    i = max(k for k, (s, _, _) in enumerate(SCENES) if s <= max(tv, 0))
    s0, fn, bg = SCENES[i]
    img = background(bg, tv)
    z, dx, dy, r = fn(img, tv)
    img = camera(img, z, dx, dy, r)
    for ts, col in SWIPE.items():
        swipe(img, tv, ts, col, .55)
    return img

if __name__ == "__main__":
    out = sys.argv[1]
    if "--preview" in sys.argv:
        for ts in sys.argv[sys.argv.index("--preview") + 1:]: frame(float(ts)).save(f"{out}_{ts}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for n in range(int(DUR * FPS)): p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close(); p.wait(); print("ok", out)
