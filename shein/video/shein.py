# V04 Shein, style 2 premium. Temps « Z(section, t) » = temps de la voix d'origine décalé du générique et des cartes de chapitre.
import os, sys, math, random
SHDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SHDIR, "../../style2"))
from gfx2 import *
from gfx import stamp
import gfx2
from PIL import Image, ImageDraw

PINK = (255, 110, 170)
gfx2.BGS["pink"] = (PINK, (255, 175, 210))
TOTAL = 312.0
D = {1: 0.0, 2: 2.5, 3: 3.9, 4: 5.3, 5: 6.7, 6: 8.1, 7: 9.5, 8: 9.5}
def Z(n, x): return x + D[n]

def put(img, L, x, y, a=1.0, s=1.0, r=0.0): rotate_paste(img, L, x, y, r, a, max(.02, s))
def pin(t, t0, d=.4, k=2.2): return back(prog(t, t0, d), k)
def bob(t, i=0, a=8, f=2.2): return math.sin(t * f + i) * a
def lab(img, x, y, s, t, t0, size=60, fg=INK, bg=PAPER, rot=-2): pop_word(img, x, y, s, t, t0, size, fg, bg, rot)
def src(img, t, t0, s):
    a = eo(prog(t, t0, .6))
    if a > 0: chip(img, 30, 1035, "Source : " + s, a, fill=PAPER, color=INK, size=22, kind="semi", anchor="lm")
def bar(img, x, base, w, h, col):
    if h > 4: rrect(img, (x - w / 2, base - h, x + w / 2, base), 22, col, 1, outline=INK + (255,), width=7)

# ---------- icônes ----------
_c = {}
def cache(key, fn):
    if key not in _c: _c[key] = fn()
    return _c[key]

def tshirt(w, col=PINK):
    def mk():
        def f(d, W_, H_):
            s = W_ / 420
            pts = [(120, 20), (170, 40), (250, 40), (300, 20), (410, 90), (360, 170), (320, 140), (320, 390), (100, 390), (100, 140), (60, 170), (10, 90)]
            d.polygon([(x * s, y * s) for x, y in pts], fill=col, outline=INK, width=int(9 * s))
            d.arc((165 * s, 5 * s, 255 * s, 75 * s), 0, 180, fill=INK, width=int(9 * s))
        return sticker(f, w, int(w * .95))
    return cache(("ts", w, col), mk)

def phone(w):
    def mk():
        def f(d, W_, H_):
            s = W_ / 240
            d.rounded_rectangle((4, 4, 236 * s, 460 * s), int(34 * s), fill=INK)
            d.rounded_rectangle((18 * s, 40 * s, 222 * s, 420 * s), int(16 * s), fill=PAPER)
            for r in range(3):
                for c in range(2):
                    x0, y0 = 32 + c * 96, 60 + r * 118
                    d.rounded_rectangle((x0 * s, y0 * s, (x0 + 80) * s, (y0 + 100) * s), int(10 * s), fill=[PINK, SKY, SUN, MINT, CORAL, GRAPE][r * 2 + c])
        return sticker(f, w, int(w * 1.95))
    return cache(("ph", w), mk)

def parcel(w):
    def mk():
        def f(d, W_, H_):
            s = W_ / 300
            d.polygon([(20 * s, 70 * s), (150 * s, 20 * s), (280 * s, 70 * s), (150 * s, 120 * s)], fill=(235, 190, 130), outline=INK, width=int(7 * s))
            d.polygon([(20 * s, 70 * s), (150 * s, 120 * s), (150 * s, 280 * s), (20 * s, 230 * s)], fill=(210, 160, 100), outline=INK, width=int(7 * s))
            d.polygon([(280 * s, 70 * s), (150 * s, 120 * s), (150 * s, 280 * s), (280 * s, 230 * s)], fill=(190, 140, 85), outline=INK, width=int(7 * s))
            d.line((85 * s, 45 * s, 215 * s, 95 * s), fill=INK, width=int(10 * s))
        return sticker(f, w, int(w * .95))
    return cache(("pc", w), mk)

def factory(w):
    def mk():
        def f(d, W_, H_):
            s = W_ / 360
            d.rectangle((20 * s, 150 * s, 340 * s, 300 * s), fill=PAPER, outline=INK, width=int(7 * s))
            d.polygon([(20 * s, 150 * s), (100 * s, 90 * s), (100 * s, 150 * s), (180 * s, 90 * s), (180 * s, 150 * s), (260 * s, 90 * s), (260 * s, 150 * s)], fill=CORAL, outline=INK, width=int(6 * s))
            d.rectangle((280 * s, 30 * s, 320 * s, 150 * s), fill=GRAPE, outline=INK, width=int(6 * s))
            for i in range(4): d.rectangle(((45 + i * 72) * s, 190 * s, (85 + i * 72) * s, 240 * s), fill=SKY, outline=INK, width=int(4 * s))
        return sticker(f, w, int(w * .85))
    return cache(("fa", w), mk)

def gavel(w):
    def mk():
        def f(d, W_, H_):
            s = W_ / 320
            d.line((90 * s, 230 * s, 230 * s, 90 * s), fill=(150, 95, 55), width=int(26 * s))
            d.rounded_rectangle((140 * s, 20 * s, 300 * s, 110 * s), int(18 * s), fill=(170, 110, 60), outline=INK, width=int(7 * s))
            d.rounded_rectangle((20 * s, 250 * s, 220 * s, 300 * s), int(10 * s), fill=GRAPE, outline=INK, width=int(7 * s))
        return sticker(f, w, int(w * .95))
    return cache(("gv", w), mk)

def store(w):
    def mk():
        def f(d, W_, H_):
            s = W_ / 340
            d.rectangle((20 * s, 90 * s, 320 * s, 300 * s), fill=PAPER, outline=INK, width=int(7 * s))
            for i in range(5): d.rectangle(((20 + i * 60) * s, 50 * s, (80 + i * 60) * s, 100 * s), fill=CORAL if i % 2 else PAPER, outline=INK, width=int(5 * s))
            d.rectangle((60 * s, 150 * s, 160 * s, 300 * s), fill=SKY, outline=INK, width=int(5 * s))
            d.rectangle((190 * s, 150 * s, 290 * s, 240 * s), fill=SKY, outline=INK, width=int(5 * s))
        return sticker(f, w, int(w * .9))
    return cache(("st", w), mk)

def ui_card(txt, sub, col, w=360, h=150):
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((3, 3, w - 3, h - 3), 26, fill=col, outline=INK, width=7)
    d.text((w / 2, h * .42), txt, font=font("anton", int(h * .36)), fill=INK, anchor="mm")
    if sub: d.text((w / 2, h * .76), sub, font=font("semi", int(h * .16)), fill=INK, anchor="mm")
    return L

# ---------- habillage premium ----------
def sting(img, t, t0=28.15):
    """Générique 2,5 s : Sou entre, le logo se dessine, balayage."""
    p = prog(t, t0, 2.5)
    mascot(img, 960, lerp(-200, 430, back(prog(t, t0, .6), 1.8)), t, 300, "content" if p < .6 else "clin", wave=1 if p < .5 else 0)
    if t >= t0 + .5: pop_word(img, 960, 720, "L'ENVERS DU BUSINESS", t, t0 + .5, 110, PAPER, INK, -2)
    if t >= t0 + 1.0: pop_word(img, 960, 850, "comment ils gagnent VRAIMENT leur argent", t, t0 + 1.0, 44, INK, SUN, 2)
    return 1.0 + .05 * eo(p), 0, 0, 0

def chapter_card(img, t, t0, num, title, col_bg=SUN):
    pop_word(img, 960, 380, f"CHAPITRE {num}", t, t0, 70, PAPER, INK, -3)
    pop_word(img, 960, 560, title, t, t0 + .15, 130, INK, col_bg, 2)
    mascot(img, 1600, 840, t, 200, "content", look=(-1, -1), alpha=eo(prog(t, t0 + .2, .3)))
    return 1.0 + .06 * eo(prog(t, t0, 1.4)), 0, 0, 0

def number_card(img, t, t0):
    """Rubrique récurrente « Le chiffre qui dit tout »."""
    pop_word(img, 960, 420, "LE CHIFFRE", t, t0, 160, SUN, None, -3)
    pop_word(img, 960, 600, "QUI DIT TOUT", t, t0 + .25, 160, PAPER, None, 2)
    confetti(img, t, t0 + .3, 60, (100, 0, W - 100, 0), 9)
    sx, sy = shake(t, t0 + .25, 16)
    return 1.0 + .06 * eo(prog(t, t0, 1.4)), sx, sy, 0

# ================= 1. ouverture à froid =================
def s_open(img, t):
    if t < 5.3:
        pop_word(img, 960, 420, fmt(41.8 * eo(prog(t, 0, 1.6)), 1), t, 0.0, 300, INK, PAPER, -3)
        lab(img, 960, 640, "MILLIARDS DE DOLLARS", t, 1.28, 90, PAPER, INK, 2)
        lab(img, 960, 800, "encaissés par Shein en 2025", t, 2.64, 50, INK, SUN, -1)
        mascot(img, 1680, 860, t, 230, "surpris", look=(-1, -1))
        sx, sy = shake(t, 1.28, 14); return 1.0 + .04 * eo(prog(t, 0, 5)), sx, sy, 0
    if t < 12.0:
        for i in range(6):
            p = pin(t, 5.36 + i * .12, .4, 2.6)
            if p > 0: put(img, tshirt(210, [PINK, SKY, SUN, MINT, CORAL, GRAPE][i]), 330 + i * 250, 380 + bob(t, i, 14, 3), 1, p, (-8, 6, -4, 7, -6, 5)[i])
        lab(img, 960, 650, "QUELQUES EUROS", t, 6.0, 90, PAPER, INK, -2)
        if t >= 7.0: put(img, phone(170), 960, 880 + bob(t, 2, 6), 1, pin(t, 7.04), -8)
        if t >= 9.3: lab(img, 960, 160, "… et la France veut l'arrêter", t, 9.32, 64, PAPER, RED2, 2)
        return 1.0 + .04 * eo(prog(t, 5.3, 6.7)), 0, 0, 0
    if t < 15.0:
        for i, (w_, t0, ic) in enumerate([("AMENDES", 12.16, None), ("LOI SPÉCIALE", 13.0, None), ("TRIBUNAL", 14.04, gavel)]):
            lab(img, 960, 330 + i * 200, w_, t, t0, 130, PAPER, (RED2, GRAPE, INK)[i], (-4, 3, -2)[i])
        put(img, gavel(280), 1600, 760, 1, pin(t, 14.04, .35, 3), -15 + 25 * math.sin(max(0, t - 14.04) * 9) * (1 - prog(t, 14.04, .8)))
        sx, sy = shake(t, 14.3, 18); return 1.04, sx, sy, 0
    if t < 20.05:
        put(img, tshirt(300), 520, 540 + bob(t, 1, 10, 3), 1, pin(t, 15.2), -5)
        put(img, factory(420), 1380, 520 + bob(t, 2, 6), 1, pin(t, 18.6), 0)
        lab(img, 960, 860, "un simple site… devenu un GÉANT MONDIAL ?", t, 16.2, 58, INK, PAPER)
        mascot(img, 960, 230, t, 180, "surpris" if t > 18.7 else "neutre")
        return 1.0 + .04 * eo(prog(t, 15.0, 5)), 0, 0, 0
    lab(img, 960, 300, "À LA FIN DE CETTE VIDÉO, TU SAURAS :", t, 20.05, 60, PAPER, INK)
    lab(img, 960, 480, "1. comment Shein vend aussi peu cher", t, 22.4, 64, INK, SUN, -2)
    lab(img, 960, 640, "2. pourquoi son modèle vacille", t, 25.2, 64, INK, CORAL, 2)
    mascot(img, 1660, 860, t, 210, "clin" if t > 26 else "content")
    return 1.0 + .03 * eo(prog(t, 20.0, 7)), 0, 0, 0

# ================= 2. le paradoxe =================
def s_rev(img, t):
    lab(img, 960, 110, "LES CHIFFRES OFFICIELS DE SHEIN", t, Z(2, 28.15), 60, PAPER, INK)
    base, k = 900, 14
    for i, (yr, v, t0) in enumerate([("2023", 32.1, Z(2, 34.99)), ("2024", 38.7, Z(2, 38.36)), ("2025", 41.8, Z(2, 41.43))]):
        x = 520 + i * 440
        p = eio(prog(t, t0, .8)); bar(img, x, base, 260, v * k * p, (SKY, SUN, MINT)[i])
        if p > 0: lab(img, x, base - v * k * p - 60, fmt(v * p, 1) + " Md$", t, t0, 66, INK, PAPER, 0)
        lab(img, x, base + 60, yr, t, t0 - .5, 54, PAPER, INK, 0)
    if t >= Z(2, 43.27): lab(img, 1650, 260, "ÇA MONTE ↗", t, Z(2, 43.27), 70, INK, MINT, 6)
    mascot(img, 200, 300, t, 170, "content", look=(1, 1))
    src(img, t, Z(2, 33.6), "prospectus de Shein (Bourse de Hong Kong, 2026)")
    return 1.0 + .03 * eo(prog(t, Z(2, 28), 17)), 0, 0, 0

def s_profit(img, t):
    lab(img, 960, 110, "MAIS REGARDE LE BÉNÉFICE…", t, Z(2, 45.35), 66, PAPER, INK)
    base, k = 880, 150
    for i, (yr, v, t0, col) in enumerate([("2024", 3.4, Z(2, 48.41), SUN), ("2025", 2.06, Z(2, 52.39), CORAL)]):
        x = 680 + i * 560
        p = eio(prog(t, t0, .8)); bar(img, x, base, 300, v * k * p, col)
        if p > 0: lab(img, x, base - v * k * p - 60, ("≈ 3,4" if i == 0 else "2,06") + " Md$", t, t0, 70, INK, PAPER, 0)
        lab(img, x, base + 60, yr, t, t0 - .5, 54, PAPER, INK, 0)
    if t >= Z(2, 54.23): pop_word(img, 1600, 330, "− 39 %", t, Z(2, 55.47), 160, PAPER, RED2, -6)
    if t >= Z(2, 57.03):
        rrect(img, (0, 0, W, H), 0, NIGHT, eo(prog(t, Z(2, 57.03), .3)) * .97)
        lab(img, 960, 440, "SHEIN VEND DE PLUS EN PLUS…", t, Z(2, 57.03), 96, PAPER, None, 0)
        lab(img, 960, 600, "… MAIS GAGNE DE MOINS EN MOINS", t, Z(2, 58.92), 96, NIGHT, SUN, -2)
        mascot(img, 960, 860, t, 200, "surpris")
    else:
        mascot(img, 200, 300, t, 170, "triste" if t > Z(2, 53.0) else "neutre", look=(1, 1))
    sx, sy = shake(t, Z(2, 55.47), 16); return 1.0 + .03 * eo(prog(t, Z(2, 45), 20)), sx, sy, 0

# ================= 3. les cent pièces =================
def s_classic(img, t):
    lab(img, 960, 110, "LA MODE CLASSIQUE", t, Z(3, 66.04), 70, PAPER, INK)
    put(img, store(380), 420, 520 + bob(t, 0, 6), 1, pin(t, Z(3, 67.3)))
    n = int(24 * eo(prog(t, Z(3, 71.56), 1.6)))
    for i in range(n):
        put(img, tshirt(80, [PINK, SKY, SUN][i % 3]), 900 + (i % 8) * 110, 380 + (i // 8) * 110, 1, 1, (i * 37) % 20 - 10)
    if t >= Z(3, 70.5): lab(img, 1340, 260, "DES MILLIERS D'EXEMPLAIRES", t, Z(3, 71.56), 54, INK, SUN, -3)
    if t >= Z(3, 73.85): lab(img, 1340, 760, "… et on croise les doigts 🤞".replace(" 🤞", ""), t, Z(3, 73.96), 52, PAPER, INK, 2)
    for i, (w_, t0) in enumerate([("SOLDES", Z(3, 77.72)), ("INVENDUS", Z(3, 78.44)), ("PERTES", Z(3, 79.4))]):
        lab(img, 760 + i * 300, 920, w_, t, t0, 64, PAPER, RED2, (-4, 3, -2)[i])
    mascot(img, 1750, 140, t, 140, "triste" if t > Z(3, 78) else "neutre")
    return 1.0 + .03 * eo(prog(t, Z(3, 66), 14)), 0, 0, 0

def s_hundred(img, t):
    lab(img, 960, 100, "SHEIN, LUI, FAIT L'INVERSE", t, Z(3, 80.68), 66, PAPER, INK)
    pop_word(img, 560, 470, "100", t, Z(3, 87.28), 280, INK, PAPER, -4)
    lab(img, 560, 680, "à 200 exemplaires seulement", t, Z(3, 87.72), 52, PAPER, INK, 2)
    put(img, phone(230), 1380, 560 + bob(t, 1, 6), 1, pin(t, Z(3, 89.21)), 6)
    for i, (w_, t0, col) in enumerate([("CLICS", Z(3, 92.8), SKY), ("PANIERS", Z(3, 94.32), SUN), ("VENTES", Z(3, 95.36), MINT)]):
        lab(img, 1700, 330 + i * 160, w_, t, t0, 60, INK, col, (-4, 3, -2)[i])
    mascot(img, 960, 900, t, 160, "surpris" if t > Z(3, 87.3) else "neutre", look=(1, -1))
    src(img, t, Z(3, 87.0), "Shein Group (modèle « à la demande »)")
    sx, sy = shake(t, Z(3, 87.28), 12); return 1.0 + .03 * eo(prog(t, Z(3, 80.5), 15.5)), sx, sy, 0

def s_test(img, t):
    lab(img, 960, 110, "LE TEST EN TEMPS RÉEL", t, Z(3, 96.36), 66, PAPER, INK)
    # gauche : flop
    put(img, tshirt(220, (180, 180, 195)), 480, 470 + bob(t, 0, 6), 1, pin(t, Z(3, 96.4)), -4)
    if t >= Z(3, 97.93):
        strike_line(img, 360, 360, 360 + 240 * eo(prog(t, Z(3, 97.93), .25)), 360 + 220 * eo(prog(t, Z(3, 97.93), .25)), 1, RED2, 26)
        strike_line(img, 600, 360, 600 - 240 * eo(prog(t, Z(3, 98.1), .25)), 360 + 220 * eo(prog(t, Z(3, 98.1), .25)), 1, RED2, 26)
        lab(img, 480, 720, "ÇA NE SE VEND PAS → STOP", t, Z(3, 98.04), 50, PAPER, RED2, -2)
    # droite : succès qui se multiplie
    if t >= Z(3, 100.76):
        n = 1 + int(7 * eo(prog(t, Z(3, 102.2), 2.4)))
        for i in range(n):
            put(img, tshirt(110 if i else 200), 1440 + (0 if i == 0 else ((i - 1) % 4 - 1.5) * 120), 460 if i == 0 else 700 + ((i - 1) // 4) * 120, 1, pin(t, Z(3, 100.9) + i * .2, .3), (i * 23) % 14 - 7)
        lab(img, 1440, 300, "ÇA SE VEND → ON RELANCE", t, Z(3, 101.32), 50, INK, MINT, 2)
    mascot(img, 960, 860, t, 170, "fache" if Z(3, 97.9) < t < Z(3, 100.7) else ("content" if t > Z(3, 100.7) else "neutre"))
    return 1.0 + .03 * eo(prog(t, Z(3, 96.3), 9)), 0, 0, 0

def s_eight(img, t):
    if t < Z(3, 112.48):
        lab(img, 960, 140, "un exemple raconté par Shein", t, Z(3, 105.64), 54, PAPER, INK)
        pop_word(img, 960, 470, "× 8", t, Z(3, 110.72), 300, INK, SUN, -6)
        lab(img, 960, 720, "RÉASSORTS D'AFFILÉE", t, Z(3, 111.0), 80, PAPER, INK, 2)
        put(img, tshirt(260), 420, 520 + bob(t, 0, 8, 3), 1, pin(t, Z(3, 105.9)), -6)
        lab(img, 420, 760, "vendu en quelques heures", t, Z(3, 108.28), 46, PAPER, INK, 2)
        if t < Z(3, 110.6): mascot(img, 1400, 520, t, 240, "surpris", look=(-1, 0))
        confetti(img, t, Z(3, 110.8), 50, (100, 0, W - 100, 0), 4)
        src(img, t, Z(3, 106.0), "contenu Shein publié sur Bloomberg (partenariat)")
        sx, sy = shake(t, Z(3, 110.72), 14); return 1.0 + .03 * eo(prog(t, Z(3, 105.5), 7)), sx, sy, 0
    rrect(img, (0, 0, W, H), 0, NIGHT, 1)
    lab(img, 960, 440, "SHEIN NE DEVINE PAS LA MODE.", t, Z(3, 112.48), 96, PAPER, None, 0)
    lab(img, 960, 620, "IL LA TESTE. EN TEMPS RÉEL.", t, Z(3, 114.46), 110, NIGHT, SUN, -3)
    mascot(img, 1650, 880, t, 180, "clin")
    sx, sy = shake(t, Z(3, 114.6), 10); return 1.0 + .04 * eo(prog(t, Z(3, 112.4), 4)), sx, sy, 0

# ================= 4. pourquoi si peu cher =================
def s_why(img, t):
    lab(img, 960, 100, "POURQUOI C'EST AUSSI PEU CHER", t, Z(4, 117.61), 66, PAPER, INK)
    items = [("1", "TRÈS PEU D'INVENDUS", "moins de vêtements jetés", Z(4, 120.17), MINT),
             ("2", "PRESQUE PAS DE MAGASINS", "pas de loyers, tout sur l'appli", Z(4, 125.57), SKY),
             ("3", "DES MILLIERS D'ATELIERS", "en Chine, très rapides", Z(4, 132.09), SUN),
             ("4", "LE COLIS VA DIRECT CHEZ TOI", "depuis la Chine", Z(4, 139.08), CORAL)]
    cur = max([i for i, it in enumerate(items) if t >= it[3] - .2] or [0])
    for i, (n, a1, a2, t0, col) in enumerate(items):
        y = 250 + i * 190
        if t < t0 - .2: continue
        p = pin(t, t0 - .2, .4)
        L = Image.new("RGBA", (1240, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((3, 3, 1237, 157), 34, fill=PAPER if i != cur else col, outline=INK, width=7)
        d.ellipse((26, 26, 134, 134), fill=INK); d.text((80, 80), n, font=font("anton", 70), fill=PAPER, anchor="mm")
        d.text((170, 62), a1, font=font("anton", 60), fill=INK, anchor="lm"); d.text((172, 122), a2, font=font("semi", 34), fill=INK, anchor="lm")
        put(img, L, 860, y + 40, 1, p, (-1, 1, -1, 1)[i] * (1.5 if i == cur else .5))
    ic = [None, store, factory, parcel][cur]
    if cur == 0: put(img, tshirt(220), 1700, 560 + bob(t, 0, 8, 3), 1, 1, 6)
    else:
        put(img, ic(260), 1700, 560 + bob(t, cur, 8, 3), 1, 1, 4)
        if cur == 1:
            strike_line(img, 1580, 450, 1820, 670, 1, RED2, 22)
    mascot(img, 1700, 900, t, 150, "content")
    return 1.0 + .03 * eo(prog(t, Z(4, 117.5), 27)), 0, 0, 0

def s_customs(img, t):
    lab(img, 960, 110, "L'AVANTAGE DISCRET", t, Z(4, 144.76), 70, PAPER, INK)
    # carte stylisée Chine -> USA
    a = eo(prog(t, Z(4, 144.8), .4))
    rrect(img, (200, 260, 680, 660), 40, PAPER, a, outline=INK + (255,), width=7)
    rrect(img, (1240, 260, 1720, 660), 40, PAPER, a, outline=INK + (255,), width=7)
    T(img, 440, 460, "CHINE", "anton", 90, INK, "mm", a); T(img, 1480, 460, "ÉTATS-UNIS", "anton", 80, INK, "mm", a)
    p = (t - Z(4, 145.6)) * .45 % 1 if t > Z(4, 145.6) else 0
    if t > Z(4, 145.6): put(img, parcel(150), lerp(700, 1220, p), 460 - math.sin(p * math.pi) * 160, 1, 1, p * 30)
    if t >= Z(4, 147.69): lab(img, 960, 760, "0 DROIT DE DOUANE", t, Z(4, 147.69), 90, INK, MINT, -3)
    if t >= Z(4, 150.39):
        strike_line(img, 600, 760, 600 + 720 * eo(prog(t, Z(4, 150.4), .3)), 760, 1, RED2, 24)
        lab(img, 960, 900, "C'EST FINI.", t, Z(4, 151.0), 90, PAPER, RED2, 3)
    if t >= Z(4, 151.99): lab(img, 1540, 150, "« une des raisons de la baisse »", t, Z(4, 152.45), 40, PAPER, INK, 3)
    mascot(img, 200, 880, t, 160, "fache" if t > Z(4, 150.4) else "content")
    src(img, t, Z(4, 152.0), "prospectus de Shein, via Reuters")
    sx, sy = shake(t, Z(4, 150.4), 14); return 1.0 + .03 * eo(prog(t, Z(4, 144.7), 13)), sx, sy, 0

# ================= 5. le chiffre qui dit tout =================
def s_value(img, t):
    lab(img, 960, 100, "LA VALEUR DE SHEIN", t, Z(5, 159.03), 70, PAPER, INK)
    pts = [("2022", 98.2, Z(5, 166.63)), ("2024", 64, Z(5, 170.43)), ("IPO 2026", 26, Z(5, 177.03))]
    X = [460, 960, 1460]; Y = lambda v: 860 - v * 5.2
    a = eo(prog(t, Z(5, 163.1), .4))
    rrect(img, (220, 300, 1700, 900), 40, PAPER, a, outline=INK + (255,), width=7)
    for i in range(1, 3):
        p = eio(prog(t, pts[i][2] - .4, .6))
        if p > 0: strike_line(img, X[i - 1], Y(pts[i - 1][1]), lerp(X[i - 1], X[i], p), lerp(Y(pts[i - 1][1]), Y(pts[i][1]), p), 1, RED2, 16)
    for i, (yr, v, t0) in enumerate(pts):
        p = pin(t, t0, .35)
        if p <= 0: continue
        shape(img, (X[i] - 26, Y(v) - 26, X[i] + 26, Y(v) + 26), lambda d, ox, oy, w, h: d.ellipse((ox, oy, ox + w, oy + h), fill=SUN + (255,), outline=INK + (255,), width=6))
        lab(img, X[i], Y(v) - 90, f"{fmt(v, 0) if v != 98.2 else '≈ 98'} Md$", t, t0, 70, INK, (MINT, SUN, CORAL)[i], 0)
        T(img, X[i], 870 - 40, yr, "anton", 44, INK, "mm", 1)
    if t >= Z(5, 178.55): lab(img, 1560, 230, "− 9 % le 1er jour", t, Z(5, 181.31), 56, PAPER, RED2, 5)
    if t >= Z(5, 182.47):
        rrect(img, (0, 0, W, H), 0, NIGHT, eo(prog(t, Z(5, 182.47), .3)) * .975)
        lab(img, 960, 420, "EN 4 ANS, SA VALEUR A ÉTÉ", t, Z(5, 182.5), 84, PAPER, None, 0)
        pop_word(img, 960, 620, "÷ 4", t, Z(5, 184.79), 260, NIGHT, SUN, -5)
        mascot(img, 1650, 880, t, 190, "surpris")
    else:
        mascot(img, 1750, 940, t, 140, "triste" if t > Z(5, 176) else "neutre")
    src(img, t, Z(5, 166.0), "prospectus de Shein ; CNBC (Bourse de Hong Kong, sept. 2026)")
    sx, sy = shake(t, Z(5, 184.8), 18); return 1.0 + .03 * eo(prog(t, Z(5, 160), 26)), sx, sy, 0

# ================= 6. la France contre-attaque =================
def s_fines(img, t):
    lab(img, 960, 100, "LA FRANCE CONTRE-ATTAQUE", t, Z(6, 187.49), 70, PAPER, INK)
    if t < Z(6, 193.5):
        pop_word(img, 960, 520, "LA FRANCE", t, Z(6, 190.13), 220, INK, PAPER, -3)
        T(img, 960, 700, "lui mène la vie la plus dure", "anton", 60, INK, "mm", eo(prog(t, Z(6, 188.5), .4)))
    for i, (yr, amt, why, t0, col) in enumerate([("2025", "40 M€", "réductions trompeuses", Z(6, 194.13), SUN), ("JUIN 2026", "≈ 22 M€", "répression des fraudes · contestée", Z(6, 202.13), CORAL)]):
        x = 560 + i * 800
        p = pin(t, t0 - .4, .4)
        if p <= 0: continue
        L = Image.new("RGBA", (680, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((4, 4, 676, 416), 34, fill=PAPER, outline=INK, width=8)
        d.rectangle((4, 4, 676, 90), fill=col); d.line((4, 90, 676, 90), fill=INK, width=8)
        d.text((340, 50), "AMENDE · " + yr, font=font("anton", 50), fill=INK, anchor="mm")
        d.text((340, 230), amt, font=font("anton", 150), fill=RED2, anchor="mm")
        d.text((340, 360), why, font=font("semi", 34), fill=INK, anchor="mm")
        put(img, L, x, 520, 1, p, (-3, 3)[i])
        if t >= t0: stamp(img, x + 210, 790, "ACCEPTÉE" if i == 0 else "CONTESTÉE", INK if i == 0 else RED2, 46, 12, eo(prog(t, t0 + (.4 if i == 0 else 2.6), .2)))
    mascot(img, 960, 920, t, 150, "fache")
    src(img, t, Z(6, 194.0), "Al Jazeera ; DGCCRF via Siècle Digital")
    sx, sy = shake(t, Z(6, 194.13), 10); return 1.0 + .03 * eo(prog(t, Z(6, 187.4), 18)), sx, sy, 0

def s_court(img, t):
    lab(img, 960, 100, "FIN 2025 : LA JUSTICE S'EN MÊLE", t, Z(6, 206.21), 66, PAPER, INK)
    lab(img, 480, 330, "produits illégaux sur la place de marché", t, Z(6, 208.33), 42, PAPER, RED2, -2)
    lab(img, 480, 470, "L'ÉTAT DEMANDE :", t, Z(6, 211.81), 56, INK, None, 0)
    lab(img, 480, 590, "SUSPENSION 3 MOIS", t, Z(6, 213.69), 80, PAPER, INK, -2)
    put(img, gavel(320), 1360, 470, 1, pin(t, Z(6, 215.86), .35, 3), -15 + 25 * math.sin(max(0, t - Z(6, 218.3)) * 9) * (1 - prog(t, Z(6, 218.3), .8)))
    if t >= Z(6, 215.86): lab(img, 1360, 700, "19 DÉC. 2025 : REFUSÉ", t, Z(6, 219.33), 70, INK, SUN, 3)
    if t >= Z(6, 220.2): lab(img, 1360, 820, "« disproportionnée »", t, Z(6, 221.53), 50, PAPER, INK, -2)
    if t >= Z(6, 222.93): lab(img, 1360, 930, "confirmé en appel", t, Z(6, 223.77), 46, INK, MINT, 2)
    mascot(img, 200, 900, t, 150, "surpris" if t > Z(6, 219.3) else "neutre", look=(1, -1))
    src(img, t, Z(6, 216.0), "Euronews ; Le Monde du droit")
    sx, sy = shake(t, Z(6, 218.33), 14); return 1.0 + .03 * eo(prog(t, Z(6, 206), 19)), sx, sy, 0

def s_law(img, t):
    lab(img, 960, 100, "ALORS LA FRANCE CHANGE D'ARME : LA LOI", t, Z(6, 225.25), 60, PAPER, INK)
    a = pin(t, Z(6, 228.29), .45)
    if a > 0:
        L = Image.new("RGBA", (560, 720), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rectangle((6, 6, 554, 714), fill=PAPER, outline=INK, width=8)
        d.text((280, 80), "LOI ANTI", font=font("anton", 64), fill=INK, anchor="mm"); d.text((280, 150), "ULTRA FAST-FASHION", font=font("anton", 50), fill=RED2, anchor="mm")
        d.text((280, 215), "promulguée en juillet 2026", font=font("semi", 30), fill=INK, anchor="mm")
        for i in range(6): d.line((60, 290 + i * 60, 500 - (i % 2) * 80, 290 + i * 60), fill=(200, 195, 185), width=10)
        put(img, L, 480, 590, 1, a, -3 + math.sin(t) * 1)
    lab(img, 1350, 330, "PÉNALITÉ PAR VÊTEMENT", t, Z(6, 233.7), 64, PAPER, INK, -2)
    if t > Z(6, 236.85): pop_word(img, 1350, 510, "jusqu'à 20 €", t, Z(6, 236.85), 120, INK, SUN, 3)
    if t >= Z(6, 238.29): lab(img, 1350, 660, "d'ici 2030 · max. 50 % du prix", t, Z(6, 238.29), 44, PAPER, INK, -1)
    if t >= Z(6, 241.62): lab(img, 1350, 800, "PUB INTERDITE DÈS 2027", t, Z(6, 243.53), 70, PAPER, RED2, 2)
    if t >= Z(6, 246.21): lab(img, 1350, 930, "même par les influenceurs", t, Z(6, 247.01), 46, INK, PAPER, -2)
    if t >= Z(6, 248.37):
        rrect(img, (0, 0, W, H), 0, NIGHT, eo(prog(t, Z(6, 248.37), .3)) * .975)
        lab(img, 960, 460, "« PAS CHER, VITE, PARTOUT »", t, Z(6, 249.13), 110, PAPER, None, 0)
        lab(img, 960, 640, "DEVIENT BEAUCOUP PLUS DIFFICILE", t, Z(6, 250.97), 90, NIGHT, CORAL, -2)
        mascot(img, 1650, 880, t, 170, "fache")
    else:
        mascot(img, 1760, 160, t, 130, "surpris" if t > Z(6, 236) else "neutre")
    src(img, t, Z(6, 229.0), "franceinfo ; Ouest-France")
    return 1.0 + .03 * eo(prog(t, Z(6, 225.2), 27)), 0, 0, 0

# ================= 7. la leçon =================
def s_lesson(img, t):
    if t < Z(7, 266.97):
        lab(img, 960, 140, "ALORS, SHEIN, C'EST QUOI VRAIMENT ?", t, Z(7, 253.88), 70, PAPER, INK)
        put(img, tshirt(260, SKY), 520, 520 + bob(t, 0, 8, 3), 1, pin(t, Z(7, 257.8)), -5)
        if t >= Z(7, 258.2):
            strike_line(img, 380, 380, 380 + 280 * eo(prog(t, Z(7, 258.3), .25)), 380 + 280 * eo(prog(t, Z(7, 258.3), .25)), 1, RED2, 28)
            lab(img, 520, 760, "pas d'abord un fabricant", t, Z(7, 258.2), 46, PAPER, RED2, -2)
        if t >= Z(7, 259.08):
            put(img, phone(230), 1380, 520 + bob(t, 1, 8, 3), 1, pin(t, Z(7, 259.64)), 6)
            lab(img, 1380, 820, "UNE MACHINE À MESURER", t, Z(7, 259.64), 64, INK, SUN, 2)
            lab(img, 1380, 930, "ce que tu as envie d'acheter", t, Z(7, 261.69), 42, PAPER, INK, -1)
        mascot(img, 960, 860, t, 150, "surpris" if t > Z(7, 259.6) else "neutre")
        return 1.0 + .03 * eo(prog(t, Z(7, 253.8), 13)), 0, 0, 0
    if t < Z(7, 277.16):
        lab(img, 960, 260, "MAIS CE MODÈLE A UN PRIX", t, Z(7, 266.97), 90, PAPER, INK)
        lab(img, 960, 470, "accusé de pousser à la surconsommation", t, Z(7, 269.16), 56, INK, PAPER, -2)
        for i in range(4):
            p = pin(t, Z(7, 272.25) + i * .4, .35)
            if p > 0: put(img, parcel(150), 560 + i * 270, 760, 1, p, 0)
        if t >= Z(7, 273.9):
            for i in range(4):
                strike_line(img, 480 + i * 270, 700, 640 + i * 270, 840, eo(prog(t, Z(7, 274.36) + i * .2, .2)), RED2, 18)
            lab(img, 960, 960, "les pays ferment les portes une à une", t, Z(7, 274.36), 46, PAPER, INK, 2)
        mascot(img, 1750, 240, t, 140, "triste")
        return 1.0 + .03 * eo(prog(t, Z(7, 266.9), 10)), 0, 0, 0
    rrect(img, (0, 0, W, H), 0, NIGHT, 1)
    lab(img, 960, 430, "Le prix bas, c'est ce que tu vois.", t, Z(7, 277.16), 100, PAPER, None, 0)
    lab(img, 960, 610, "La machine derrière, c'est ce qui rapporte.", t, Z(7, 279.13), 96, NIGHT, SUN, -2)
    mascot(img, 1650, 880, t, 180, "clin")
    return 1.0 + .04 * eo(prog(t, Z(7, 277.1), 5)), 0, 0, 0

def s_outro(img, t):
    mascot(img, 960, 260, t, 260, "content", wave=1)
    lab(img, 960, 500, "L'ENVERS DU BUSINESS", t, Z(8, 282.73), 100, PAPER, INK)
    if t >= Z(8, 286.89): lab(img, 960, 640, "ABONNE-TOI", t, Z(8, 286.89), 80, PAPER, RED2, -3)
    if t >= Z(8, 287.89):
        lab(img, 960, 800, "MARDI :", t, Z(8, 287.89), 50, INK, None, 0)
        lab(img, 960, 910, "pourquoi Lidl est moins cher que tout le monde", t, Z(8, 289.33), 56, INK, SUN, 2)
    return 1.0, 0, 0, 0

def s_end(img, t):
    t0 = 302.0
    lab(img, 960, 140, "MERCI D'AVOIR REGARDÉ !", t, t0, 80, PAPER, INK)
    a = eo(prog(t, t0, .5))
    for i, txt in enumerate(["vidéo suivante", "vidéo conseillée"]):
        x = 150 + i * 620
        rrect(img, (x, 360, x + 560, 675), 26, PAPER, a, outline=INK + (255,), width=6)
        T(img, x + 280, 520, txt, "bold", 34, (120, 120, 140), "mm", a)
    mascot(img, 1590, 520, t, 280, "content", alpha=a)
    lab(img, 1590, 760, "ABONNE-TOI", t, t0 + .3, 50, PAPER, RED2, 0)
    return 1.0, 0, 0, 0

# chapitres : (début de carte, n°, titre, couleur)
CH = [(Z(3, 66.04) - 1.4, 1, "LE SECRET DES 100 PIÈCES", SUN), (Z(4, 117.61) - 1.4, 2, "POURQUOI SI PEU CHER", MINT),
      (Z(5, 159.03) - 1.4, 3, "LA VALEUR DE SHEIN", CORAL), (Z(6, 187.49) - 1.4, 4, "LA FRANCE CONTRE-ATTAQUE", SKY),
      (Z(7, 253.88) - 1.4, 5, "LA VRAIE LEÇON", SUN)]

def mk_card(c):
    t0, n, title, col = c
    if n == 3: return lambda img, t: number_card(img, t, t0)
    return lambda img, t: chapter_card(img, t, t0, n, title, col)

TL = [(0.0, s_open, "sun"), (28.15, sting, "pink"), (Z(2, 28.15), s_rev, "sky"), (Z(2, 45.1), s_profit, "coral"),
      (CH[0][0], mk_card(CH[0]), "night"), (Z(3, 66.04), s_classic, "paper"), (Z(3, 80.5), s_hundred, "pink"), (Z(3, 96.2), s_test, "mint"), (Z(3, 105.5), s_eight, "sun"),
      (CH[1][0], mk_card(CH[1]), "night"), (Z(4, 117.61), s_why, "grape"), (Z(4, 144.6), s_customs, "sky"),
      (CH[2][0], mk_card(CH[2]), "night"), (Z(5, 159.03), s_value, "sun"),
      (CH[3][0], mk_card(CH[3]), "night"), (Z(6, 187.49), s_fines, "sky"), (Z(6, 206.0), s_court, "paper"), (Z(6, 225.1), s_law, "mint"),
      (CH[4][0], mk_card(CH[4]), "night"), (Z(7, 253.88), s_lesson, "pink"), (Z(8, 282.6), s_outro, "sun"), (302.0, s_end, "sky")]
