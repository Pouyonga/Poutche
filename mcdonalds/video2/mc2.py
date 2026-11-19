# McDonald's en style 2. Temps = voix off (words.json de mcdonalds/). Mascotte : Sou.
import os, sys, math, random
MCDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(MCDIR, "../../style2"))
from gfx2 import *
from PIL import Image, ImageDraw

TOTAL = 445.0
SRC = "McDonald's, rapport annuel 2025"

def put(img, L, x, y, a=1.0, s=1.0, r=0.0): rotate_paste(img, L, x, y, r, a, max(.02, s))
def pin(t, t0, d=.4, k=2.2): return back(prog(t, t0, d), k)
def bob(t, i=0, a=8, f=2.2): return math.sin(t * f + i) * a
def src(img, t, t0, s):
    a = eo(prog(t, t0, .6))
    if a > 0: chip(img, 30, 1035, "Source : " + s, a, fill=PAPER, color=INK, size=22, kind="semi", anchor="lm")
def label(img, x, y, s, t, t0, size=60, fg=INK, bg=PAPER, rot=-2): pop_word(img, x, y, s, t, t0, size, fg, bg, rot)
def bar(img, x, base, w, h, col, a=1.0):
    if h > 4: rrect(img, (x - w / 2, base - h, x + w / 2, base), 22, col, a, outline=INK + (255,), width=7)
def person(w, col=GRAPE):
    def f(d, W_, H_):
        s = W_ / 200
        d.ellipse((60 * s, 5 * s, 140 * s, 85 * s), fill=(255, 205, 170), outline=INK, width=int(6 * s))
        d.pieslice((10 * s, 90 * s, 190 * s, 330 * s), 180, 360, fill=col, outline=INK, width=int(6 * s))
        d.rectangle((13 * s, 208 * s, 187 * s, 250 * s), fill=col); d.line((13 * s, 210 * s, 13 * s, 250 * s), fill=INK, width=int(6 * s)); d.line((187 * s, 210 * s, 187 * s, 250 * s), fill=INK, width=int(6 * s))
        d.line((13 * s, 250 * s, 187 * s, 250 * s), fill=INK, width=int(6 * s))
        d.ellipse((80 * s, 38 * s, 92 * s, 50 * s), fill=INK); d.ellipse((108 * s, 38 * s, 120 * s, 50 * s), fill=INK)
    return sticker(f, w, int(w * 1.28))

# ---------------- 1. accroche (identique à la démo) ----------------
def s_world(img, t):
    for i, (x, y, t0) in enumerate([(380, 330, .9), (620, 250, 1.2), (1300, 260, 1.5), (1540, 360, 1.8), (500, 600, 2.1), (1420, 620, 2.4)]):
        p = pin(t, t0)
        if p > 0: put(img, icon_building(110), x, y + bob(t, i), 1, p * .9, math.sin(t + i) * 3)
    put(img, icon_burger(420), 960, 520 + bob(t, 0, 10), 1, pin(t, 0, .5), math.sin(t * 1.4) * 4)
    if t >= 3.6: label(img, 960, 860, fmt(139.4 * eo(prog(t, 3.6, 1.6)), 1) + " MILLIARDS $", t, 3.6, 120)
    mascot(img, 1680, 860, t, 230, "surpris" if t > 4.9 else "content", look=(-1, 0) if t > 4 else (0, 0), wave=1 if t < 2.5 else 0, alpha=eo(prog(t, .5, .4)))
    sx, sy = shake(t, 4.9); return 1.0 + .05 * eo(prog(t, 0, 6.4)), sx, sy, 0

def s_food(img, t):
    for i, (fn, x, t0, lab) in enumerate([(icon_burger, 520, 6.6, "BURGERS"), (icon_fries, 960, 7.36, "FRITES"), (icon_shake, 1400, 8.04, "MILKSHAKES")]):
        p = pin(t, t0, .4, 2.6)
        if p <= 0: continue
        put(img, fn(300 if fn is icon_burger else 200), x, 470 + bob(t, i, 12, 3), 1, p, (-6, 4, -3)[i])
        label(img, x, 790, lab, t, t0 + .05, 70, PAPER, INK, (-4, 3, -2)[i])
    return 1.0 + .03 * prog(t, 6.4, 2.6), 0, 0, 0

def s_share(img, t):
    x0, x1, y = 260, 1660, 430
    a = eo(prog(t, 9.1, .4))
    rrect(img, (x0, y, x1, y + 150), 40, PAPER, a, outline=INK + (255,), width=8)
    fp = 1 - eo(prog(t, 10.9, 1.2)) * (1 - 26.9 / 139.4)
    if a > 0: rrect(img, (x0 + 10, y + 10, x0 + 10 + (x1 - x0 - 20) * fp, y + 140), 32, SUN if fp > .5 else CORAL, 1)
    label(img, 560, 340, "139,4 Md$ vendus", t, 9.3, 64, INK, None)
    if t >= 11.0: label(img, x0 + (x1 - x0) * .1 + 230, 690, "26,9 Md$ pour McDonald's", t, 11.4, 64, INK, PAPER, 2)
    if t >= 12.88: label(img, 1350, 820, "MOINS D'1/5 !", t, 12.88, 110, PAPER, RED2, -5)
    mascot(img, 1680, 300, t, 210, "triste" if t > 12.0 else "neutre", look=(-1, 1))
    sx, sy = shake(t, 12.88); return 1.04 - .04 * eo(prog(t, 9.0, 5.0)), sx, sy, 0

def s_rich(img, t):
    put(img, icon_trophy(340), 960, 430 + bob(t, 0, 10, 3), 1, pin(t, 14.4, .5, 2), math.sin(t * 2) * 4)
    confetti(img, t, 15.3, 70, (100, 0, W - 100, 0), 3)
    label(img, 960, 730, "UNE DES PLUS RENTABLES", t, 15.4, 92)
    label(img, 960, 885, "DE LA PLANÈTE", t, 16.4, 92, PAPER, INK, 2)
    mascot(img, 300, 820, t, 220, "content", wave=1)
    return 1.0 + .06 * eo(prog(t, 14.3, 3.8)), 0, 0, 0

def s_plate(img, t):
    put(img, icon_plate(620), 960, 640); put(img, icon_burger(300), 960, 560 + bob(t, 0, 6, 3))
    if t >= 19.2:
        strike_line(img, 700, 360, 700 + 520 * eo(prog(t, 19.2, .25)), 360 + 400 * eo(prog(t, 19.2, .25)), 1, RED2, 40)
        strike_line(img, 1220, 360, 1220 - 520 * eo(prog(t, 19.4, .25)), 360 + 400 * eo(prog(t, 19.4, .25)), 1, RED2, 40)
    label(img, 960, 210, "PAS DANS TON ASSIETTE", t, 18.6, 100, PAPER, INK)
    mascot(img, 1660, 800, t, 210, "fache", look=(-1, 0))
    sx, sy = shake(t, 19.2, 18); return 1.02, sx, sy, 0

def s_ground(img, t):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 640, W, H), fill=(120, 80, 50)); d.rectangle((0, 620, W, 660), fill=(80, 190, 90))
    for i in range(14): d.ellipse((i * 150 + 30, 760 + (i % 3) * 60, i * 150 + 70, 790 + (i % 3) * 60), fill=(150, 105, 70))
    p = pin(t, 20.4, .5)
    put(img, icon_building(300), 960, 640 - 200 * max(.02, p), 1, p)
    label(img, 960, 880, "LE TERRAIN", t, 20.9, 110, INK, SUN, -3)
    mascot(img, 420, 500, t, 200, "surpris", look=(1, 1))
    return 1.0 + .08 * eo(prog(t, 20.2, 1.4)), 0, -60 * eo(prog(t, 20.2, 1.4)), 0

def s_title(img, t):
    lines = [[("COMMENT", 22.76), ("McDONALD'S", 23.0), ("GAGNE", 23.68)], [("VRAIMENT", 24.04), ("SON ARGENT", 24.48)]]
    for li, (ln, y) in enumerate(zip(lines, (380, 560))):
        ws = [tw(w_, "anton", 130) + 60 for w_, _ in ln]; x = 960 - sum(ws) / 2
        for (wd, t0), wpx in zip(ln, ws):
            pop_word(img, x + wpx / 2, y, wd, t, t0, 130, SUN if li == 1 else PAPER, None, 0); x += wpx
    if t >= 26.5: label(img, 960, 780, "(et pas avec les burgers)", t, 26.52, 70, NIGHT, CORAL, -3)
    mascot(img, 1650, 880, t, 200, "clin" if t > 26.8 else "content", alpha=eo(prog(t, 22.0, .4)))
    sx, sy = shake(t, 24.04, 10); return 1.0 + .03 * math.sin(t * .8), sx, sy, 0

# ---------------- 2. le paradoxe ----------------
_dots = None
def s_world_count(img, t):
    global _dots
    if _dots is None:
        r = random.Random(11); _dots = []
        while len(_dots) < 300:
            x, y = r.uniform(-1, 1), r.uniform(-1, 1)
            if x * x + (y / .55) ** 2 < 1: _dots.append((960 + x * 820, 560 + y * 700, r.uniform(0, 6)))
    n = int(len(_dots) * eo(prog(t, 30.77, 2.4)))
    for i, (x, y, ph) in enumerate(_dots[:n]):
        white = t >= 35.5 and i % 20 != 0 and (i / 300) < eo(prog(t, 35.5, 2.5)) * 1.05
        r = 9 + 2 * math.sin(t * 3 + ph)
        shape(img, (x - r, y - r, x + r, y + r), lambda d, ox, oy, w, h, c=(PAPER if white else SUN): d.ellipse((ox, oy, ox + w, oy + h), fill=c + (255,), outline=INK + (255,), width=3))
    if t < 39.0:
        label(img, 960, 500, fmt(45356 * eo(prog(t, 30.77, 2.4)), 0), t, 30.77, 150, INK, PAPER, -2)
        label(img, 960, 650, "RESTAURANTS DANS LE MONDE", t, 31.4, 54, PAPER, INK, 2)
    else:
        label(img, 960, 500, "≈ 95 %", t, 39.0, 170, INK, PAPER, -2)
        label(img, 960, 660, "TENUS PAR DES FRANCHISÉS", t, 39.4, 60, PAPER, INK, 2)
    if t >= 43.65: label(img, 960, 960, "des entrepreneurs qui paient pour la marque", t, 43.65, 46, INK, SUN, -1)
    mascot(img, 1720, 180, t, 170, "surpris" if t > 39 else "neutre", look=(-1, 1))
    src(img, t, 31.0, SRC)
    return 1.0 + .04 * eo(prog(t, 28.8, 19)), 0, 0, 0

def s_two(img, t):
    label(img, 960, 140, "CE QUE McDONALD'S ENCAISSE : 26,9 Md$", t, 48.6, 64, PAPER, INK)
    base, k = 880, 26
    for x, lab, v, ti, col in [(620, "ventes de SES restaurants", 9.7, 63.37, SKY), (1300, "ce que paient les FRANCHISÉS", 16.5, 60.29, SUN)]:
        p = eio(prog(t, ti, .9))
        bar(img, x, base, 300, v * k * p, col)
        if p > 0: label(img, x, base - v * k * p - 70, fmt(v * p, 1) + " Md$", t, ti, 80, INK, PAPER, 0)
        label(img, x, base + 70 - 30, lab, t, ti - .4, 38, PAPER, INK, 0)
    if t < 57.0: label(img, 960, 290, "la plus grosse partie ne vient PAS des burgers", t, 53.6, 48, INK, None, -1)
    else: label(img, 960, 290, "… mais des franchisés, chaque mois", t, 57.05, 52, RED2, PAPER, -1)
    mascot(img, 180, 860, t, 180, "surpris" if t > 60.3 else "neutre", look=(1, -1))
    src(img, t, 60.0, SRC)
    sx, sy = shake(t, 60.29, 10); return 1.0 + .03 * eo(prog(t, 48.4, 19)), sx, sy, 0

def s_question(img, t):
    p = pin(t, 67.57, .5, 3)
    pop_word(img, 960, 420, "?", t, 67.57, 420, PAPER, None, math.sin(t * 3) * 6)
    label(img, 960, 760, "Que paient les franchisés, exactement ?", t, 68.0, 70, INK, PAPER)
    if t >= 71.6: label(img, 960, 900, "RETOUR EN 1955", t, 71.6, 80, PAPER, INK, -4)
    mascot(img, 1600, 450, t, 220, "surpris" if t < 71 else "content", look=(-1, 0))
    return 1.0 + .05 * eo(prog(t, 67.5, 7)), 0, 0, 0

# ---------------- 3. l'histoire (fond papier, style album) ----------------
def polaroid(img, x, y, w, h, t, t0, draw_fn, rot=-3, cap=None):
    p = pin(t, t0, .45)
    if p <= 0: return
    L = Image.new("RGBA", (w + 40, h + 110), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((0, 0, w + 39, h + 109), fill=PAPER, outline=INK, width=6)
    draw_fn(d, 20, 20, w, h)
    if cap: d.text(((w + 40) / 2, h + 65), cap, font=font("anton", 44), fill=INK, anchor="mm")
    put(img, L, x, y + bob(t, x, 5, 1.5), 1, p, rot + math.sin(t * .8) * 1.5)

def s_stand(img, t):
    label(img, 960, 120, "CALIFORNIE · ANNÉES 1940-1950", t, 75.4, 56, PAPER, INK)
    def resto(d, ox, oy, w, h):
        d.rectangle((ox, oy, ox + w, oy + h), fill=(170, 220, 255)); d.rectangle((ox, oy + h * .7, ox + w, oy + h), fill=(120, 190, 100))
        d.rectangle((ox + w * .2, oy + h * .3, ox + w * .8, oy + h * .75), fill=PAPER, outline=INK, width=5)
        d.rectangle((ox + w * .15, oy + h * .2, ox + w * .85, oy + h * .32), fill=RED2, outline=INK, width=5)
        d.text((ox + w / 2, oy + h * .26), "BURGERS", font=font("anton", 34), fill=PAPER, anchor="mm")
    polaroid(img, 720, 520, 520, 380, t, 75.6, resto, -4, "LE 1ER McDONALD'S")
    def bros(d, ox, oy, w, h):
        d.rectangle((ox, oy, ox + w, oy + h), fill=(255, 230, 190))
        for k, c in enumerate((SKY, MINT)):
            cx = ox + w * (.32 + k * .36)
            d.ellipse((cx - 40, oy + 60, cx + 40, oy + 140), fill=(255, 205, 170), outline=INK, width=4)
            d.pieslice((cx - 80, oy + 150, cx + 80, oy + h + 120), 180, 360, fill=c, outline=INK, width=4)
    polaroid(img, 1310, 560, 420, 320, t, 80.59, bros, 5, "RICHARD & MAURICE")
    if t >= 83.7: label(img, 960, 960, "des burgers très vite… comme à l'usine", t, 83.71, 50, INK, SUN)
    return 1.0 + .04 * eo(prog(t, 75.1, 13)), 0, 0, 0

def s_kroc(img, t):
    put(img, person(260, CORAL), 520, 560 + bob(t, 1, 6), 1, pin(t, 88.6, .5))
    label(img, 520, 870, "RAY KROC", t, 90.75, 90, PAPER, INK)
    label(img, 520, 970, "vendeur de machines à milkshake", t, 89.2, 38, INK, PAPER, 2)
    put(img, icon_shake(130), 760, 470 + bob(t, 2, 10, 3), 1, pin(t, 89.95, .4), 12)
    label(img, 1320, 380, "SON IDÉE :", t, 94.7, 60, INK, None)
    label(img, 1320, 500, "VENDRE LE CONCEPT PARTOUT", t, 95.9, 60, PAPER, INK)
    label(img, 1320, 620, "EN FRANCHISE", t, 98.47, 90, INK, SUN, -4)
    if t >= 99.71: label(img, 1320, 790, "1955 · 1er franchisé", t, 99.71, 64, PAPER, RED2, 4)
    mascot(img, 1760, 930, t, 150, "content")
    return 1.0 + .04 * eo(prog(t, 88.4, 16)), 0, 0, 0

def s_problem(img, t):
    label(img, 960, 150, "UN PROBLÈME", t, 104.6, 110, PAPER, RED2, -3)
    label(img, 960, 330, "Kroc ne touche que", t, 105.92, 56, INK, None)
    v = 1.9 * eo(prog(t, 110.27, .8))
    pop_word(img, 960, 520, fmt(v, 1) + " %", t, 109.9, 260, INK, PAPER, -2)
    label(img, 960, 720, "des ventes de chaque restaurant", t, 109.9, 50, PAPER, INK)
    label(img, 960, 830, "(et une partie va aux frères McDonald)", t, 111.95, 40, INK, None)
    if t >= 116.4: label(img, 960, 950, "PRESQUE PAS D'ARGENT", t, 116.4, 70, PAPER, RED2, 3)
    mascot(img, 1650, 600, t, 220, "triste" if t > 114 else "surpris", look=(-1, 0))
    sx, sy = shake(t, 110.4, 10); return 1.0 + .04 * eo(prog(t, 104.5, 14)), sx, sy, 0

def s_sonneborn(img, t):
    put(img, person(220, SKY), 330, 520 + bob(t, 3, 6), 1, pin(t, 119.0, .5))
    label(img, 330, 790, "HARRY SONNEBORN", t, 119.95, 54, PAPER, INK)
    label(img, 330, 880, "ancien financier", t, 121.18, 38, INK, PAPER)
    def box(x, y, txt, col, t0, w=360):
        if t < t0: return
        p = pin(t, t0, .4)
        L = Image.new("RGBA", (w, 150), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
        dd.rounded_rectangle((3, 3, w - 3, 147), 26, fill=col, outline=INK, width=7)
        dd.text((w / 2, 75), txt, font=font("anton", 56), fill=INK, anchor="mm")
        put(img, L, x, y, 1, p)
    box(1000, 330, "McDONALD'S", SUN, 126.9)
    if t >= 127.7:
        box(1000, 650, "LE TERRAIN", MINT, 127.71)
        label(img, 1000, 490, "achète ou loue ↓", t, 127.9, 40, INK, None)
    if t >= 130.88:
        strike_line(img, 1190, 650, lerp(1190, 1390, eo(prog(t, 130.88, .5))), 650, 1, INK, 14)
        box(1600, 650, "FRANCHISÉ", CORAL, 131.4, 330)
    if t >= 132.67: label(img, 1450, 870, "LOUÉ PLUS CHER !", t, 132.67, 80, PAPER, RED2, -5)
    sx, sy = shake(t, 132.67, 12); return 1.0 + .04 * eo(prog(t, 118.8, 15)), sx, sy, 0

def s_quote(img, t):
    pop_word(img, 260, 280, "«", t, 133.9, 300, SUN, None, 0)
    label(img, 960, 420, "Nous ne sommes pas vraiment", t, 136.07, 90, PAPER, None, 0)
    label(img, 960, 540, "dans la restauration.", t, 136.9, 90, PAPER, None, 0)
    label(img, 960, 700, "Nous sommes dans l'IMMOBILIER.", t, 138.38, 100, NIGHT, SUN, -2)
    label(img, 960, 880, "phrase attribuée à Harry Sonneborn", t, 134.11, 36, PAPER, None, 0)
    mascot(img, 1720, 860, t, 180, "surpris" if t > 138.4 else "neutre", look=(-1, -1))
    sx, sy = shake(t, 138.38, 10); return 1.0 + .03 * eo(prog(t, 133.7, 6.6)), sx, sy, 0

def s_cheque(img, t):
    label(img, 960, 130, "GRÂCE À L'ARGENT DES LOYERS…", t, 140.4, 60, PAPER, INK)
    if t >= 145.47: label(img, 1600, 280, "1961", t, 145.47, 100, INK, SUN, 8)
    p = pin(t, 146.83, .5)
    if p > 0:
        L = Image.new("RGBA", (1120, 380), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((4, 4, 1116, 376), 24, fill=PAPER, outline=INK, width=8)
        d.rectangle((4, 60, 1116, 100), fill=MINT)
        d.text((50, 160), "À l'ordre de : Richard et Maurice McDonald", font=font("semi", 40), fill=INK)
        d.text((50, 225), "Pour : la marque et le concept", font=font("semi", 34), fill=(90, 90, 110))
        d.text((1070, 320), fmt(2.7 * eo(prog(t, 150.07, .8)), 1) + " MILLIONS $", font=font("anton", 90), fill=GREEN2, anchor="rm")
        put(img, L, 960, 520, 1, p, -2 + math.sin(t) * 1.2)
    label(img, 700, 860, "Les frères : un chèque", t, 152.38, 54, INK, PAPER, -2)
    label(img, 1260, 960, "Kroc : un EMPIRE sur des terrains", t, 154.59, 60, PAPER, INK, 2)
    mascot(img, 200, 880, t, 170, "content" if t > 154.6 else "neutre")
    sx, sy = shake(t, 150.9, 8); return 1.0 + .04 * eo(prog(t, 140.3, 19)), sx, sy, 0

# ---------------- 4. aujourd'hui ----------------
def s_flows(img, t):
    label(img, 960, 120, "CE QUE PAIE UN FRANCHISÉ", t, 159.9, 64, PAPER, INK)
    put(img, person(170, CORAL), 330, 560 + bob(t, 1, 6), 1, pin(t, 162.4, .4))
    label(img, 330, 790, "LE FRANCHISÉ", t, 162.5, 46, PAPER, INK)
    put(img, icon_building(220), 1600, 540 + bob(t, 2, 6), 1, pin(t, 163.6, .4))
    label(img, 1600, 790, "McDONALD'S", t, 163.6, 46, INK, SUN)
    if t >= 167.0:
        strike_line(img, 480, 420, lerp(480, 1450, eo(prog(t, 167.6, .6))), 420, 1, INK, 26)
        strike_line(img, 480, 420, lerp(480, 1450, eo(prog(t, 167.6, .6))), 420, 1, SKY, 16)
        label(img, 960, 360, "REDEVANCE", t, 167.61, 56, INK, SKY, -2)
        label(img, 960, 480, "% des ventes · marque, recettes, méthodes", t, 168.69, 34, INK, PAPER, 0)
        for k in range(4):
            ph = ((t - 167.6) * .5 + k / 4) % 1
            T(img, lerp(500, 1440, ph), 420, "€", "anton", 50, INK, "mm", 1)
    if t >= 173.4:
        w_ = 26 + 14 * eo(prog(t, 175.13, .6))
        strike_line(img, 480, 640, lerp(480, 1450, eo(prog(t, 175.13, .6))), 640, 1, INK, int(w_ + 12))
        strike_line(img, 480, 640, lerp(480, 1450, eo(prog(t, 175.13, .6))), 640, 1, SUN, int(w_))
        label(img, 960, 570, "LOYER", t, 175.13, 80, INK, SUN, -3)
        label(img, 960, 720, "le terrain ou le bâtiment est à McDonald's", t, 177.69, 34, INK, PAPER, 0)
        for k in range(7 if t >= 175.6 else 0):
            ph = ((t - 175.1) * .6 + k / 7) % 1
            T(img, lerp(500, 1440, ph), 640, "€", "anton", 64, INK, "mm", 1)
    if t >= 180.71: label(img, 960, 900, "% des ventes + un MINIMUM garanti", t, 182.17, 56, PAPER, INK, 0)
    mascot(img, 1760, 230, t, 140, "surpris" if t > 175 else "neutre", look=(-1, 1))
    sx, sy = shake(t, 175.13, 8); return 1.0 + .03 * eo(prog(t, 159.7, 28)), sx, sy, 0

def s_gauges(img, t):
    label(img, 960, 140, "McDONALD'S EST PROPRIÉTAIRE DE…", t, 187.9, 64, PAPER, INK)
    for i, (lab, v, ti, col, icon) in enumerate([("des TERRAINS", .56, 192.49, MINT, None), ("des BÂTIMENTS", .80, 194.49, SUN, None)]):
        y = 380 + i * 250
        a = eo(prog(t, ti - .4, .3))
        rrect(img, (300, y, 1400, y + 110), 55, PAPER, a, outline=INK + (255,), width=8)
        p = eo(prog(t, ti, 1.0)) * v
        if p > 0: rrect(img, (310, y + 10, 310 + max(90, 1080 * p), y + 100), 45, col, 1)
        label(img, 420, y - 40, lab, t, ti - .4, 44, INK, None, 0)
        if p > 0: pop_word(img, 1580, y + 55, f"{round(p * 100)} %", t, ti, 110, INK, PAPER, -3)
    label(img, 960, 900, "le reste : loué… puis SOUS-LOUÉ aux franchisés", t, 197.13, 48, PAPER, INK)
    mascot(img, 1750, 150, t, 150, "content", look=(-1, 1))
    src(img, t, 192.0, SRC + " (pays gérés en direct)")
    return 1.0 + .03 * eo(prog(t, 187.8, 13)), 0, 0, 0

def s_rent(img, t):
    label(img, 960, 120, "CE QUE RAPPORTENT LES FRANCHISÉS", t, 201.6, 62, PAPER, INK)
    base, k = 800, 46
    for x, lab, v, ti, col in [(700, "LOYERS", 10.4, 206.85, SUN), (1220, "REDEVANCES", 6.0, 208.97, SKY)]:
        p = eio(prog(t, ti, .8))
        bar(img, x, base, 300, v * k * p, col)
        if p > 0: label(img, x, base - v * k * p - 70, "≈ " + fmt(v * p, 0 if v == 6.0 else 1) + " Md$", t, ti, 72, INK, PAPER, 0)
        label(img, x, base + 60, lab, t, ti - .3, 54, PAPER, INK, 0)
    if t >= 212.8: label(img, 960, 960, "AVANT TOUT UN PROPRIÉTAIRE", t, 212.8, 70, PAPER, RED2, -3)
    mascot(img, 1650, 500, t, 200, "surpris" if t > 207 else "neutre", look=(-1, 0))
    if t < 212.6: src(img, t, 207.0, "FourWeekMBA, d'après le rapport annuel")
    sx, sy = shake(t, 212.8, 10); return 1.0 + .03 * eo(prog(t, 201.4, 14)), sx, sy, 0

# ---------------- 5. le chiffre qui dit tout ----------------
def s_margins(img, t):
    label(img, 960, 110, "LE CHIFFRE QUI DIT TOUT", t, 215.3, 90, NIGHT, SUN, -2)
    base, k = 900, 30
    for x, lab, v, tv, m, tm, c1, c2 in [(500, "SES PROPRES RESTAURANTS", 9.7, 225.11, 1.4, 234.23, SKY, CORAL), (1420, "SES FRANCHISÉS", 16.5, 239.19, 13.9, 243.07, SUN, MINT)]:
        label(img, x, 240, lab, t, tv - 3.5 if x < 960 else tv - 1.8, 48, PAPER, INK, 0)
        p = eio(prog(t, tv, .8)); bar(img, x - 115, base, 180, v * k * p, c1)
        if p > 0: label(img, x - 115, base - v * k * p - 50, fmt(v, 1), t, tv, 54, INK, PAPER, 0)
        if p > 0: T(img, x - 115, base + 40, "encaissé", "bold", 30, INK, "mm", 1)
        q = eio(prog(t, tm, .8)); bar(img, x + 115, base, 180, max(10, m * k * q) if q > 0 else 0, c2)
        if q > 0: label(img, x + 115, base - m * k * q - 50, fmt(m, 1), t, tm, 54, INK, PAPER, 0)
        if q > 0: T(img, x + 115, base + 40, "marge", "bold", 30, INK, "mm", 1)
    if 229.3 < t < 236.5:
        for i, (s, ti) in enumerate([("− salaires", 229.99), ("− nourriture", 230.95), ("− électricité", 231.96)]):
            label(img, 820, 420 + i * 80, s, t, ti, 40, INK, PAPER, (-2, 2, -1)[i])
    if t >= 245.87: pop_word(img, 960, 560, "× 10", t, 245.87, 220, NIGHT, MINT, -6)
    if t >= 247.6: label(img, 960, 1010, "vendre des burgers : un peu · louer des restaurants : ÉNORMÉMENT", t, 247.63, 40, PAPER, INK, 0)
    mascot(img, 1800, 110, t, 130, "surpris" if t > 245.8 else ("triste" if t > 234.2 else "neutre"))
    sx, sy = shake(t, 245.87, 16); return 1.0 + .03 * eo(prog(t, 215.2, 41)), sx, sy, 0

# ---------------- 6. pourquoi c'est génial ----------------
def s_risks(img, t):
    label(img, 960, 120, "1 · LE FRANCHISÉ PREND LES RISQUES", t, 256.4, 62, PAPER, INK)
    put(img, person(190, CORAL), 520, 520 + bob(t, 0, 6), 1, pin(t, 258.7, .4))
    for i, (s, ti) in enumerate([("embaucher", 261.81), ("acheter les stocks", 262.69), ("gérer au quotidien", 263.93)]):
        label(img, 520, 790 + i * 85, s, t, ti, 44, PAPER, RED2, (-3, 2, -2)[i])
    put(img, icon_building(220), 1400, 500 + bob(t, 1, 6), 1, pin(t, 265.97, .4))
    label(img, 1400, 780, "encaisse loyer + redevance", t, 267.28, 46, INK, MINT, 2)
    mascot(img, 960, 560, t, 170, "clin" if t > 267 else "neutre")
    if t < 265.9: label(img, 1400, 500, "et McDonald's ?", t, 260.5, 60, INK, PAPER, 3)
    return 1.0 + .03 * eo(prog(t, 256.2, 14)), 0, 0, 0

def s_value(img, t):
    label(img, 960, 120, "2 · LES TERRAINS PRENNENT DE LA VALEUR", t, 270.5, 60, PAPER, INK)
    X0, X1, Y1 = 220, 1080, 860
    rrect(img, (X0 - 40, 260, X1 + 40, Y1 + 40), 30, PAPER, eo(prog(t, 270.6, .3)), outline=INK + (255,), width=7)
    p = eio(prog(t, 272.0, 2.5))
    pts = [(lerp(X0, X1, u / 40), Y1 - 40 - (u / 40) ** 1.6 * 460 - math.sin(u * .9) * 8) for u in range(int(40 * p) + 1)]
    if len(pts) > 1: shape(img, (X0, 280, X1 + 10, Y1 + 10), lambda d, ox, oy, w, h: d.line([(x - X0 + ox, y - 280 + oy) for x, y in pts], fill=GREEN2 + (255,), width=14, joint="curve"))
    T(img, X0 + 20, 310, "valeur de l'immobilier", "bold", 34, INK, "lm", eo(prog(t, 272, .3)))
    sh = 1 - eo(prog(t, 276.17, 1.2)) * .8
    put(img, icon_burger(300), 1450, 400 + bob(t, 1, 8, 3), 1, max(.25, sh))
    label(img, 1450, 560, "mangé en 5 minutes", t, 276.17, 40, INK, PAPER, -2)
    put(img, icon_building(200), 1450, 770, 1, pin(t, 277.65, .4))
    label(img, 1450, 980, "l'immobilier, lui, RESTE", t, 278.43, 46, PAPER, INK, 2)
    return 1.0 + .03 * eo(prog(t, 270.4, 10)), 0, 0, 0

def s_control(img, t):
    label(img, 960, 120, "3 · LE CONTRÔLE", t, 280.2, 70, PAPER, INK)
    a = pin(t, 281.89, .45)
    if a > 0:
        L = Image.new("RGBA", (360, 440), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.arc((60, 0, 300, 260), 180, 360, fill=INK, width=44); d.arc((70, 10, 290, 250), 180, 360, fill=(200, 200, 215), width=26)
        d.rounded_rectangle((10, 160, 350, 430), 40, fill=SUN, outline=INK, width=9)
        d.ellipse((150, 250, 210, 310), fill=INK); d.rectangle((168, 290, 192, 360), fill=INK)
        put(img, L, 520, 560 + bob(t, 0, 6), 1, a, math.sin(t * 2) * 4)
    label(img, 1300, 380, "Propriétaire des murs", t, 282.93, 70, INK, PAPER)
    label(img, 1300, 490, "= énorme moyen de pression", t, 285.05, 50, PAPER, INK, 2)
    label(img, 1300, 650, "ne pas respecter les règles = risquer :", t, 288.29, 40, INK, None, 0)
    label(img, 1300, 750, "de perdre l'enseigne", t, 291.97, 50, INK, PAPER, -2)
    label(img, 1300, 860, "… ET L'EMPLACEMENT", t, 294.05, 64, PAPER, RED2, 3)
    mascot(img, 200, 900, t, 160, "fache", look=(1, 0))
    sx, sy = shake(t, 294.05, 10); return 1.0 + .03 * eo(prog(t, 280.1, 15)), sx, sy, 0

def s_opinc(img, t):
    label(img, 960, 120, "LE RÉSULTAT EN 2025", t, 295.7, 70, PAPER, INK)
    if t < 300.2:
        pop_word(img, 960, 520, "IMPRESSIONNANT", t, 296.69, 150, INK, PAPER, -4)
        confetti(img, t, 296.8, 50, (100, 0, W - 100, 0), 7)
    pop_word(img, 560, 380, fmt(12.4 * eo(prog(t, 300.65, 1.0)), 1) + " Md$", t, 300.29, 140, INK, MINT, -3)
    label(img, 560, 520, "de résultat d'exploitation", t, 302.09, 42, PAPER, INK)
    pop_word(img, 1360, 380, "26,9 Md$", t, 303.89, 140, INK, PAPER, 3)
    label(img, 1360, 520, "de revenus", t, 305.57, 42, PAPER, INK)
    a = eo(prog(t, 306.6, .3))
    rrect(img, (260, 640, 1660, 740), 50, PAPER, a, outline=INK + (255,), width=8)
    p = eo(prog(t, 306.65, 1.0)) * 12.4 / 26.9
    if p > 0: rrect(img, (270, 650, 270 + max(80, 1380 * p), 730), 40, MINT, 1)
    label(img, 960, 850, "PRESQUE LA MOITIÉ DEVIENT DU BÉNÉFICE", t, 306.65, 64, INK, SUN, -2)
    label(img, 960, 965, "énorme pour de la restauration", t, 311.23, 42, PAPER, INK, 2)
    mascot(img, 1760, 870, t, 160, "content" if t > 306 else "surpris")
    src(img, t, 300.0, SRC)
    sx, sy = shake(t, 306.65, 8); return 1.0 + .03 * eo(prog(t, 295.6, 19)), sx, sy, 0

# ---------------- 6 bis. nuance ----------------
def s_nuance(img, t):
    label(img, 960, 120, "ATTENTION : LES BURGERS COMPTENT QUAND MÊME", t, 315.3, 56, PAPER, INK)
    tilt = math.sin(t * 1.5) * 4
    cx, cy = 960, 480
    a = eo(prog(t, 315.4, .4))
    strike_line(img, cx, cy, cx, 760, 1, INK, 20, a)
    strike_line(img, cx - 470, cy + 470 * math.sin(math.radians(tilt)), cx + 470, cy - 470 * math.sin(math.radians(tilt)), 1, INK, 18, a)
    put(img, icon_burger(260), cx - 470, cy - 110 + 470 * math.sin(math.radians(tilt)), a)
    put(img, icon_building(130), cx + 470, cy - 130 - 470 * math.sin(math.radians(tilt)), a)
    label(img, 960, 860, "loyer et redevance = un % des VENTES", t, 320.12, 56, INK, PAPER)
    label(img, 960, 970, "moins de ventes → moins d'argent pour McDonald's", t, 324.28, 44, PAPER, RED2, 1)
    return 1.0 + .03 * eo(prog(t, 315.2, 13)), 0, 0, 0

def s_cycle(img, t):
    label(img, 960, 110, "LE CERCLE DU SYSTÈME", t, 328.7, 66, PAPER, INK)
    cx, cy, RX, RY = 960, 560, 520, 300
    p = eo(prog(t, 330.0, 8.0))
    shape(img, (cx - RX, cy - RY, cx + RX, cy + RY), lambda d, ox, oy, w, h: d.arc((ox + 20, oy + 20, ox + w - 20, oy + h - 20), -80, -80 + 340 * p, fill=INK + (255,), width=12))
    for i, (s, ti, col) in enumerate([("pub, menus, applis", 329.96, SKY), ("plus de ventes", 335.8, SUN), ("plus de loyers", 337.48, MINT), ("plus de moyens", 338.4, CORAL)]):
        ang = -math.pi / 2 + i * math.pi / 2
        label(img, cx + RX * math.cos(ang), cy + RY * math.sin(ang), s, t, ti, 46, INK, col, (-3, 2, -2, 3)[i])
    if t >= 339.51:
        label(img, cx, cy - 30, "LE BURGER", t, 339.51, 80, PAPER, INK)
        label(img, cx, cy + 70, "= le moteur", t, 342.6, 46, INK, PAPER)
    mascot(img, cx, cy + 10, t, 150, "content", alpha=1 - eo(prog(t, 339.3, .3)))
    return 1.0 + .03 * math.sin(t * .6), 0, 0, 0

# ---------------- 7. France ----------------
FRANCE = [(0.46, 0.02), (0.58, 0.08), (0.74, 0.12), (0.86, 0.22), (0.82, 0.38), (0.86, 0.55), (0.80, 0.68), (0.84, 0.82), (0.70, 0.90),
          (0.56, 0.86), (0.44, 0.98), (0.30, 0.92), (0.20, 0.80), (0.24, 0.62), (0.16, 0.48), (0.02, 0.38), (0.10, 0.30), (0.26, 0.30), (0.34, 0.16)]
_fd = None
def s_france(img, t):
    global _fd
    x0, y0, s = 230, 170, 780
    poly = [(x0 + u * s, y0 + v * s) for u, v in FRANCE]
    if _fd is None:
        m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon(poly, fill=255); r = random.Random(4); _fd = []
        while len(_fd) < 180:
            x, y = r.uniform(x0, x0 + s), r.uniform(y0, y0 + s)
            if m.getpixel((int(x), int(y))): _fd.append((x, y))
    a = eo(prog(t, 347.3, .4))
    shape(img, (x0 - 10, y0 - 10, x0 + s + 10, y0 + s + 10), lambda d, ox, oy, w, h: d.polygon([(x - x0 + 10 + ox, y - y0 + 10 + oy) for x, y in poly], fill=PAPER + (255,), outline=INK + (255,), width=10), a)
    n = int(len(_fd) * eo(prog(t, 349.4, 2.2)))
    for i, (x, y) in enumerate(_fd[:n]):
        c = SUN if (t < 352.7 or i % 7 == 0) else GRAPE
        r_ = 9 + 2 * math.sin(t * 4 + i)
        shape(img, (x - r_, y - r_, x + r_, y + r_), lambda d, ox, oy, w, h, c=c: d.ellipse((ox, oy, ox + w, oy + h), fill=c + (255,), outline=INK + (255,), width=3))
    label(img, 1450, 330, "ET EN FRANCE ?", t, 347.2, 70, PAPER, INK)
    pop_word(img, 1450, 520, "1 600+", t, 350.11, 200, INK, PAPER, -3)
    label(img, 1450, 680, "RESTAURANTS McDONALD'S", t, 351.35, 52, PAPER, INK)
    label(img, 1450, 800, "l'immense majorité : des franchisés", t, 352.71, 42, INK, SUN, 2)
    src(img, t, 350.0, "France Snacking 2026 (1 629 restaurants)")
    return 1.0 + .04 * eo(prog(t, 347.1, 9)), 0, 0, 0

def s_receipt(img, t):
    label(img, 960, 110, "SUR 100 € DE BURGERS VENDUS", t, 356.0, 64, PAPER, INK)
    p = pin(t, 356.2, .5)
    if p > 0:
        L = Image.new("RGBA", (820, 760), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rectangle((10, 10, 810, 720), fill=PAPER, outline=INK, width=7)
        for i in range(20): d.polygon([(10 + i * 40, 718), (30 + i * 40, 750), (50 + i * 40, 718)], fill=PAPER, outline=INK)
        d.text((410, 80), "TICKET · 100,00 €", font=font("anton", 60), fill=INK, anchor="mm")
        for i, (lab, v, ti) in enumerate([("Loyer", "≈ 10 €", 363.73), ("Redevance de marque", "≈ 5 €", 365.15), ("Publicité", "4 à 5 €", 366.91)]):
            if t >= ti:
                d.text((60, 220 + i * 110), lab, font=font("semi", 44), fill=INK, anchor="lm")
                d.text((760, 220 + i * 110), v, font=font("anton", 64), fill=RED2, anchor="rm")
        if t >= 369.59:
            d.line((50, 540, 770, 540), fill=INK, width=5)
            d.text((60, 620), "Vers McDonald's", font=font("bold", 46), fill=INK, anchor="lm")
            if t >= 371.55: d.text((760, 620), "≈ 20 €", font=font("anton", 86), fill=RED2, anchor="rm")
        put(img, L, 900, 590, 1, p, -2 + math.sin(t * .9) * 1.2)
    label(img, 960, 1010, "varie selon les contrats et les emplacements", t, 375.39, 36, PAPER, INK, 0)
    mascot(img, 1650, 600, t, 200, "surpris" if t > 371.5 else "neutre", look=(-1, 0))
    sx, sy = shake(t, 371.55, 10); return 1.0 + .03 * eo(prog(t, 355.9, 23)), sx, sy, 0

# ---------------- 8. conclusion ----------------
def s_bait(img, t):
    label(img, 960, 120, "ALORS, McDONALD'S VEND DES BURGERS ?", t, 379.7, 70, PAPER, INK)
    label(img, 960, 250, "OUI.", t, 382.88, 90, INK, SUN, -4)
    put(img, icon_burger(380), 560, 600 + bob(t, 0, 10, 3), 1, pin(t, 383.56, .4))
    if t >= 383.88: label(img, 600, 400, "L'APPÂT", t, 383.88, 80, PAPER, RED2, 10)
    put(img, icon_building(300, eo(prog(t, 389.36, 1.5))), 1380, 560 + bob(t, 2, 6), 1, pin(t, 386.69, .4))
    if t >= 389.36: label(img, 1380, 960, "LE VRAI BUSINESS : LE TERRAIN", t, 389.36, 60, INK, MINT, 2)
    mascot(img, 960, 860, t, 150, "clin" if t > 389.5 else "content")
    return 1.0 + .04 * eo(prog(t, 379.6, 13)), 0, 0, 0

def s_lesson(img, t):
    label(img, 960, 380, "Ce qu'une entreprise vend", t, 392.69, 110, PAPER, None, 0)
    label(img, 960, 530, "n'est pas toujours", t, 396.84, 110, PAPER, None, 0)
    label(img, 960, 690, "ce qui la fait gagner de l'argent.", t, 397.72, 104, NIGHT, SUN, -2)
    return 1.0 + .04 * eo(prog(t, 392.6, 7)), 0, 0, 0

def s_cards(img, t):
    label(img, 960, 110, "LE MÊME PRINCIPE, PARTOUT", t, 399.5, 66, PAPER, INK)
    items = [("L'imprimante", "pas chère", "Les cartouches", "hors de prix", 399.52, 401.28, SKY),
             ("Le rasoir", "offert", "Les lames", "à vie", 403.08, 404.72, CORAL),
             ("La console", "presque sans marge", "Jeux, abonnements", "derrière", 406.8, 409.36, MINT)]
    for i, (a1, b1, a2, b2, t1, t2, col) in enumerate(items):
        x = 360 + i * 600
        p = pin(t, t1, .4)
        if p <= 0: continue
        flip = prog(t, t2, .5); sx = abs(math.cos(flip * math.pi)); front = flip < .5
        w = int(480 * max(.04, sx))
        L = Image.new("RGBA", (max(8, w), 460), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((2, 2, max(6, w - 2), 458), 30, fill=PAPER if front else col, outline=INK, width=8)
        if sx > .35:
            d.text((w / 2, 190), a1 if front else a2, font=font("anton", 54), fill=INK, anchor="mm")
            d.text((w / 2, 280), b1 if front else b2, font=font("semi", 38), fill=(90, 90, 110) if front else INK, anchor="mm")
        put(img, L, x, 530 + bob(t, i, 8, 2), 1, p, (-3, 2, -2)[i])
    label(img, 960, 880, "le produit que tu vois = la PORTE D'ENTRÉE", t, 411.44, 54, PAPER, INK)
    if t >= 417.3:
        rrect(img, (0, 0, W, H), 0, NIGHT, eo(prog(t, 417.44, .4)))
        label(img, 960, 380, "La prochaine fois que tu achètes quelque chose :", t, 417.44, 50, PAPER, None, 0)
        label(img, 960, 540, "SUR QUOI CETTE ENTREPRISE", t, 420.8, 100, PAPER, None, 0)
        label(img, 960, 680, "GAGNE-T-ELLE VRAIMENT SON ARGENT ?", t, 421.44, 96, NIGHT, SUN, -2)
        mascot(img, 1700, 900, t, 170, "clin")
    return 1.0 + .03 * eo(prog(t, 399.4, 25)), 0, 0, 0

_bf = None
def s_outro(img, t):
    global _bf
    mascot(img, 960, 230, t, 240, "content", wave=1)
    label(img, 960, 470, "L'ENVERS DU BUSINESS", t, 424.6, 96, PAPER, INK)
    if t >= 428.4: label(img, 960, 600, "ABONNE-TOI", t, 428.4, 70, PAPER, RED2, -3)
    if t >= 429.36:
        if _bf is None: _bf = Image.open(os.path.join(MCDIR, "../../black_friday/miniature_c_le_piege.png")).convert("RGBA").resize((480, 270), Image.LANCZOS)
        L = Image.new("RGBA", (500, 290), INK + (255,)); L.paste(_bf, (10, 10))
        put(img, L, 960, 870, 1, pin(t, 429.36, .4), -2)
        label(img, 960, 680, "tu as raté la vidéo Black Friday ?", t, 429.36, 40, INK, PAPER, 0)
    return 1.0, 0, 0, 0

def s_end(img, t):
    label(img, 960, 140, "MERCI D'AVOIR REGARDÉ !", t, 433.5, 80, PAPER, INK)
    a = eo(prog(t, 433.5, .5))
    for i, lab in enumerate(["vidéo suivante", "vidéo conseillée"]):
        x = 150 + i * 620
        rrect(img, (x, 360, x + 560, 675), 26, PAPER, a, outline=INK + (255,), width=6)
        T(img, x + 280, 520, lab, "bold", 34, (120, 120, 140), "mm", a)
    mascot(img, 1590, 520, t, 280, "content", alpha=a)
    label(img, 1590, 760, "ABONNE-TOI", t, 433.8, 50, PAPER, RED2, 0)
    return 1.0, 0, 0, 0

TL = [(0.0, s_world, "sun"), (6.4, s_food, "coral"), (9.0, s_share, "sky"), (14.25, s_rich, "mint"), (18.1, s_plate, "grape"),
      (20.2, s_ground, "sky"), (21.6, s_title, "night"), (28.8, s_world_count, "sun"), (48.4, s_two, "sky"), (67.5, s_question, "coral"),
      (75.1, s_stand, "paper"), (88.4, s_kroc, "sun"), (104.5, s_problem, "paper"), (118.8, s_sonneborn, "sky"), (133.7, s_quote, "night"),
      (140.3, s_cheque, "mint"), (159.7, s_flows, "sky"), (187.8, s_gauges, "sun"), (201.4, s_rent, "coral"), (215.2, s_margins, "paper"),
      (256.2, s_risks, "sky"), (270.4, s_value, "mint"), (280.1, s_control, "grape"), (295.6, s_opinc, "sun"), (315.2, s_nuance, "coral"),
      (328.6, s_cycle, "paper"), (347.1, s_france, "sky"), (355.9, s_receipt, "coral"), (379.6, s_bait, "sun"), (392.6, s_lesson, "night"),
      (399.4, s_cards, "grape"), (424.5, s_outro, "sun"), (433.4, s_end, "sky")]
