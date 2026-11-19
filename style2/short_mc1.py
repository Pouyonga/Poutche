# Short vertical 1080x1920 : « McDonald's ne gagne pas son argent avec les burgers » (voix réutilisée : mcdonalds s1 + extrait s5).
import os, sys, math, subprocess
import gfx2
from gfx2 import *

SW, SH = 1080, 1920
FPS = 30

def bgv(kind, t):
    return background(kind, t, SW, SH)

def put(img, L, x, y, a=1.0, s=1.0, r=0.0): rotate_paste(img, L, x, y, r, a, max(.02, s))

# Montage audio : accroche (0-28 s de s1) puis le « × 10 » (s5 de 9,8 s à 38,7 s, soit 225,1→253,9 sur la timeline)
A1 = (0.0, 27.95)          # s1 complet
A2 = (9.84, 38.7)          # dans s5 : « Les restaurants que McDonald's gère… énormément. »
GAP = 0.4
DUR = (A1[1] - A1[0]) + GAP + (A2[1] - A2[0]) + 2.2

def scene(img, t):
    # t = temps du Short
    if t < 9.0:
        put(img, icon_burger(560), 540, 760 + math.sin(t * 2) * 12, 1, back(prog(t, 0, .5), 2.2), math.sin(t * 1.4) * 4)
        if t >= 3.6: pop_word(img, 540, 1160, fmt(139.4 * eo(prog(t, 3.6, 1.6)), 1) + " Md$", t, 3.6, 150, INK, PAPER, -3)
        if t >= 4.0: pop_word(img, 540, 1330, "vendus chaque année", t, 4.0, 70, PAPER, INK, 2)
        mascot(img, 820, 1620, t, 300, "surpris" if t > 4.9 else "content", wave=1 if t < 2.5 else 0)
        return "sun"
    if t < 14.3:
        pop_word(img, 540, 520, "CE QUE McDONALD'S ENCAISSE", t, 9.1, 84, PAPER, INK, -2)
        pop_word(img, 540, 760, "MOINS D'1/5", t, 12.88, 170, PAPER, RED2, -5)
        pop_word(img, 540, 980, "(26,9 Md$)", t, 11.4, 90, INK, PAPER, 2)
        mascot(img, 540, 1450, t, 340, "triste" if t > 12 else "neutre")
        return "sky"
    if t < 21.6:
        if t < 18.1:
            put(img, icon_trophy(420), 540, 700 + math.sin(t * 3) * 10, 1, back(prog(t, 14.4, .5), 2))
            confetti(gfx2_img[0], t, 15.3, 60, (60, 0, SW - 60, 0), 3)
            pop_word(img, 540, 1100, "ULTRA RENTABLE", t, 15.4, 120, INK, PAPER, -2)
        else:
            put(img, icon_burger(460), 540, 760, 1, 1)
            if t >= 19.2:
                strike_line(img, 260, 560, 260 + 560 * eo(prog(t, 19.2, .25)), 560 + 400 * eo(prog(t, 19.2, .25)), 1, RED2, 46)
                strike_line(img, 820, 560, 820 - 560 * eo(prog(t, 19.4, .25)), 560 + 400 * eo(prog(t, 19.4, .25)), 1, RED2, 46)
            pop_word(img, 540, 1160, "PAS LES BURGERS", t, 18.6, 120, PAPER, INK, -2)
            if t >= 20.2: pop_word(img, 540, 1360, "SOUS TES PIEDS…", t, 20.4, 100, INK, SUN, 3)
        mascot(img, 820, 1650, t, 260, "fache" if t > 18.1 else "content")
        return "mint" if t < 18.1 else "grape"
    if t < 28.4:
        pop_word(img, 540, 600, "SON VRAI", t, 21.7, 140, PAPER, None, 0)
        pop_word(img, 540, 780, "BUSINESS ?", t, 22.3, 160, SUN, None, 0)
        put(img, icon_building(420), 540, 1250 + math.sin(t * 2) * 8, 1, back(prog(t, 23.0, .5), 2))
        return "night"
    # partie 2 : les marges (t2 = temps dans l'extrait)
    t2 = t - 28.35
    pop_word(img, 540, 300, "LE CHIFFRE QUI DIT TOUT", t2, 0.0, 80, NIGHT, SUN, -2)
    base, k = 1500, 40
    for x, lab, v, tv, m, tm, c1, c2 in [(300, "SES RESTOS", 9.7, .0, 1.4, 9.1, SKY, CORAL), (780, "FRANCHISÉS", 16.5, 14.1, 13.9, 18.0, SUN, MINT)]:
        if t2 < tv - .4: continue
        pop_word(img, x, 440, lab, t2, tv - .3, 56, PAPER, INK, 0)
        p = eio(prog(t2, tv, .8))
        if p > 0: rrect(img, (x - 150, base - v * k * p, x - 20, base), 18, c1, 1, outline=INK + (255,), width=6)
        q = eio(prog(t2, tm, .8))
        if q > 0: rrect(img, (x + 20, base - max(14, m * k * q), x + 150, base), 18, c2, 1, outline=INK + (255,), width=6)
        if q > 0: pop_word(img, x + 85, base - m * k * q - 60, fmt(m, 1), t2, tm, 60, INK, PAPER, 0)
        if p > 0: pop_word(img, x - 85, base - v * k * p - 60, fmt(v, 1), t2, tv, 60, INK, PAPER, 0)
    if t2 >= 20.8: pop_word(img, 540, 1690, "× 10 DE MARGE", t2, 20.8, 110, NIGHT, MINT, -4)
    T(img, 540, base + 50, "en milliards de $ · encaissé / marge", "bold", 34, INK, "mm", 1)
    if t2 >= 29.0:
        rrect(img, (0, 0, SW, SH), 0, NIGHT, eo(prog(t2, 29.0, .4)))
        pop_word(img, 540, 760, "LA VIDÉO COMPLÈTE", t2, 29.2, 90, PAPER, None, 0)
        pop_word(img, 540, 900, "SUR LA CHAÎNE ↓", t2, 29.5, 110, SUN, None, 0)
        mascot(img, 540, 1300, t2, 320, "clin")
    return "paper"

gfx2_img = [None]
def frame(t):
    kind = "sun"
    tmp = Image.new("RGB", (SW, SH))
    gfx2_img[0] = tmp
    kind = scene(tmp, t)  # premier passage : récupère le fond
    img = bgv(kind, t); gfx2_img[0] = img
    scene(img, t)
    # sous-titre de marque en bas
    T(img, 540, 1860, "L'ENVERS DU BUSINESS", "anton", 40, INK if kind != "night" else PAPER, "mm", .6)
    return img

if __name__ == "__main__":
    out = sys.argv[1]
    gfx2.W, gfx2.H = SW, SH
    import gfx as _g; _g.W, _g.H = SW, SH
    if "--preview" in sys.argv:
        for ts in sys.argv[sys.argv.index("--preview") + 1:]: frame(float(ts)).save(f"{out}_{ts}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SW}x{SH}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for n in range(int(DUR * FPS)): p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close(); p.wait(); print("ok", out, DUR)
