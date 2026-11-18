# Scènes de la vidéo 2 « Comment McDonald's gagne VRAIMENT son argent ». Temps = voix off (words.json).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../black_friday/video"))
from PIL import Image, ImageDraw
from gfx import *
from scenes import background, header, source, a_in, dy_in, chapter, s_endcard

SRC_10K = "McDonald's, rapport annuel 2025 (10-K)"

# ---------- icônes ----------
_icache = {}
def burger_layer(w):
    key = ("burger", int(w))
    if key in _icache: return _icache[key]
    s = w / 460
    B = Image.new("RGBA", (int(460 * s) + 4, int(350 * s) + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(B)
    S = lambda *v: tuple(int(x * s) for x in v)
    d.chord(S(20, 10, 440, 250), 180, 360, fill=(222, 150, 60)); d.rectangle(S(20, 128, 440, 150), fill=(222, 150, 60))
    for sx, sy in [(120, 60), (190, 40), (260, 45), (330, 70), (160, 95), (230, 85), (300, 100), (380, 110), (90, 105)]:
        d.ellipse(S(sx - 9, sy - 5, sx + 9, sy + 5), fill=(255, 240, 200))
    pts = [(10, 160)] + [(10 + i * 22, 150 + (12 if i % 2 else 0)) for i in range(21)] + [(450, 160), (450, 185), (10, 185)]
    d.polygon([S(*p) for p in pts], fill=(70, 190, 80))
    d.polygon([S(30, 182), S(430, 182), S(400, 220), S(230, 250), S(60, 220)], fill=(255, 200, 40))
    d.rounded_rectangle(S(25, 195, 435, 265), int(30 * s), fill=(110, 58, 30))
    d.rounded_rectangle(S(30, 270, 430, 340), int(26 * s), fill=(205, 135, 55))
    _icache[key] = B; return B

def building_layer(w, lit=0.0):
    key = ("bld", int(w), round(lit, 2))
    if key in _icache: return _icache[key]
    s = w / 420
    L = Image.new("RGBA", (int(420 * s) + 4, int(520 * s) + 4), (0, 0, 0, 0))
    q = ImageDraw.Draw(L); S = lambda *v: tuple(int(x * s) for x in v)
    q.rectangle(S(60, 60, 360, 500), fill=(235, 238, 245)); q.polygon([S(40, 70), S(210, 0), S(380, 70)], fill=(200, 205, 215))
    for r in range(5):
        for c in range(3):
            x0, y0 = 95 + c * 85, 105 + r * 70
            on = (r + c) % 3 == 0 or (lit > 0 and ((r * 3 + c) % 7) / 7 < lit)
            q.rectangle(S(x0, y0, x0 + 55, y0 + 45), fill=YELLOW if on else (60, 70, 95))
    q.rectangle(S(170, 440, 250, 500), fill=(60, 70, 95))
    if len(_icache) > 400: _icache.clear()
    _icache[key] = L; return L

def person_layer(w, col=(200, 200, 215)):
    key = ("p", int(w), col)
    if key in _icache: return _icache[key]
    L = Image.new("RGBA", (int(w), int(w * 1.6)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse((w * .3, 0, w * .7, w * .4), fill=col); d.pieslice((0, w * .45, w, w * 1.9), 180, 360, fill=col)
    d.rectangle((0, w * 1.15, w, w * 1.6), fill=col)
    _icache[key] = L; return L

def put(img, lay, cx, cy, alpha=1.0, scale=1.0, angle=0):
    rotate_paste(img, lay, cx, cy, angle, alpha, scale)

def bar_v(img, x, base, w, h, col, a=1.0):
    if h > 1: rrect(img, (x - w / 2, base - h, x + w / 2, base), 14, col, a)

def gauge(img, x, y, w, p, col, label, val, t, t0):
    a = a_in(t, t0 - .4)
    T(img, x, y - 50, label, "bold", 40, GREY, "lm", a)
    rrect(img, (x, y, x + w, y + 44), 22, CARD, a)
    pp = eo(prog(t, t0, 1.0)) * p
    if pp > 0: rrect(img, (x, y, x + max(44, w * pp), y + 44), 22, col, a)
    T(img, x + w + 30, y + 22, f"{round(pp * 100)} %", "anton", 70, col, "lm", a)

# ---------- 1. accroche ----------
def s_hook(img, t):
    put(img, burger_layer(420), 960, 640, a_in(t, 0.0, .3), scale=lerp(.7, 1, eo(prog(t, 0, .5))))
    v = 139.4 * eio(prog(t, 0.6, 4.3))
    if t >= 9.04: v = lerp(139.4, 26.9, eio(prog(t, 9.04, 1.2)))
    col = WHITE if t < 9.04 else mix(WHITE, YELLOW, prog(t, 9.04, 1.2))
    T(img, 960, 250, fmt(v, 1), "anton", 210, col, "mm", a_in(t, 0.3, .3), shadow=True)
    T(img, 960, 390, "MILLIARDS DE DOLLARS", "anton", 64, YELLOW if t < 9.04 else GREY, "mm", a_in(t, .5, .3))
    lab = "vendus par tous les restaurants McDonald's" if t < 9.04 else "ce que McDonald's, l'entreprise, encaisse"
    T(img, 960, 460, lab, "semi", 40, GREY, "mm", a_in(t, 3.0 if t < 9.04 else 10.0))
    if t >= 12.88: chip(img, 960, 945, "MOINS D'UN CINQUIÈME", a_in(t, 12.88, .3), fill=RED, color=WHITE, size=46, kind="xbold")
    source(img, t, 3.0, SRC_10K)

def s_secret(img, t):
    T(img, 960, 150, "UNE DES ENTREPRISES LES PLUS RENTABLES DE LA PLANÈTE", "anton", 62, WHITE, "mm", a_in(t, 14.36), dy=dy_in(t, 14.36))
    bx = lerp(960, 560, eio(prog(t, 20.24, .6)))
    put(img, burger_layer(380), bx, 560, a_in(t, 18.16))
    if t >= 19.15:
        p = eo(prog(t, 19.15, .35))
        strike_line(img, bx - 200, 400, bx + 200, 720, p, RED, 30); strike_line(img, bx + 200, 400, bx - 200, 720, eo(prog(t, 19.35, .35)), RED, 30)
        T(img, bx, 830, "PAS DANS TON ASSIETTE", "anton", 60, RED, "mm", a_in(t, 19.3))
    if t >= 20.24:
        rise = eo(prog(t, 20.24, .7))
        put(img, building_layer(330), 1360, lerp(1100, 560, rise))
        T(img, 1360, 870, "SOUS TES PIEDS", "anton", 60, GREEN, "mm", a_in(t, 20.92))
    if t >= 21.6:
        a = a_in(t, 21.65, .4)
        rrect(img, (0, 0, W, H), 0, BG, a * .985)
        T(img, 960, 420, "COMMENT McDONALD'S GAGNE", "anton", 110, WHITE, "mm", a)
        T(img, 960, 560, "VRAIMENT SON ARGENT", "anton", 130, YELLOW, "mm", a_in(t, 24.04, .3), shadow=True)
        T(img, 960, 700, "(et ce n'est pas avec les burgers)", "semi", 50, GREY, "mm", a_in(t, 26.52))

# ---------- 2. le paradoxe ----------
_dots = None
def _world_dots():
    global _dots
    if _dots is None:
        r = random.Random(11); pts = []
        while len(pts) < 420:
            x, y = r.uniform(-1, 1), r.uniform(-1, 1)
            if (x / 1) ** 2 + (y / .55) ** 2 < 1 and not (-.15 < x < .05 and y > .2): pts.append((960 + x * 760, 560 + y * 640))
        _dots = pts
    return _dots

def s_world(img, t):
    header(img, t, 28.85, "FIN 2025, DANS LE MONDE")
    n = int(len(_world_dots()) * eo(prog(t, 30.77, 2.4)))
    franch = t >= 35.21
    pw = eo(prog(t, 35.4, 2.5))
    for i, (x, y) in enumerate(_world_dots()[:n]):
        white = franch and (i % 20 != 0) and (i / 420) < pw * 1.05
        img.paste(WHITE if white else YELLOW, (int(x) - 6, int(y) - 6, int(x) + 6, int(y) + 6))
    v = 45356 * eo(prog(t, 30.77, 2.4))
    if t < 39.0:
        rrect(img, (660, 470, 1260, 650), 30, BG, a_in(t, 30.77) * .9)
        T(img, 960, 540, fmt(v, 0), "anton", 140, WHITE, "mm", a_in(t, 30.77), shadow=True)
        T(img, 960, 625, "RESTAURANTS McDONALD'S", "anton", 44, YELLOW, "mm", a_in(t, 31.4))
    else:
        a = a_in(t, 39.0, .3)
        rrect(img, (610, 430, 1310, 700), 30, BG, a * .92)
        T(img, 960, 540, "≈ 95 %", "anton", 170, WHITE, "mm", a, shadow=True)
        T(img, 960, 650, "TENUS PAR DES FRANCHISÉS", "anton", 50, YELLOW, "mm", a)
    if t >= 43.65: chip(img, 960, 950, "Des entrepreneurs indépendants qui paient pour utiliser la marque", a_in(t, 43.65, .3), fill=CARD, color=WHITE, size=34, outline=(70, 70, 85))
    source(img, t, 31.0, SRC_10K)

def s_two_cols(img, t):
    header(img, t, 48.49, "CE QUE McDONALD'S ENCAISSE : 26,9 MILLIARDS $ EN 2025")
    base, k = 840, 26
    items = [(620, "Ventes de ses propres restaurants", 9.7, 63.37, GREY), (1300, "Ce que lui versent les franchisés", 16.5, 60.29, YELLOW)]
    for x, lab, v, ti, col in items:
        p = eio(prog(t, ti, .9))
        bar_v(img, x, base, 300, v * k * p, col)
        if p > 0: T(img, x, base - v * k * p - 60, fmt(v * p, 1) + " Md$", "anton", 86, WHITE, "mm", a_in(t, ti, .2))
        T(img, x, base + 50, lab, "bold", 36, GREY, "mm", a_in(t, ti - .3))
    T(img, 960, 260, "La plus grosse partie ne vient pas des burgers vendus", "semi", 46, WHITE, "mm", a_in(t, 53.61) * (1 - a_in(t, 57.0)))
    T(img, 960, 260, "… mais de ce que paient les franchisés, chaque mois", "semi", 46, YELLOW, "mm", a_in(t, 57.05))
    source(img, t, 60.0, SRC_10K)

def s_question(img, t):
    T(img, 960, 420, "?", "anton", 400, YELLOW, "mm", a_in(t, 67.57, .3), shadow=True, scale=lerp(1.4, 1, back(prog(t, 67.57, .45))))
    T(img, 960, 720, "Que paient les franchisés, exactement ?", "anton", 80, WHITE, "mm", a_in(t, 68.0))
    if t >= 71.6: stamp(img, 960, 900, "RETOUR EN 1955", YELLOW, 70, -4, a_in(t, 71.6, .2), scale=lerp(1.5, 1, eo(prog(t, 71.6, .3))))

# ---------- 3. l'histoire ----------
SEP = (240, 222, 190); SEP2 = (200, 170, 120); SEPD = (58, 44, 28)
def sepia_card(img, t, t0):
    a = a_in(t, t0, .5)
    rrect(img, (260, 170, 1660, 910), 20, SEPD, a); rrect(img, (280, 190, 1640, 890), 14, (40, 30, 20), a)
    return a

def s_stand(img, t):
    a = sepia_card(img, t, 75.23)
    T(img, 960, 260, "CALIFORNIE · ANNÉES 1940-1950", "bold", 38, SEP2, "mm", a)
    # petit restaurant stylisé
    rrect(img, (700, 380, 1220, 660), 10, (90, 70, 45), a)
    rrect(img, (680, 330, 1240, 400), 10, (150, 40, 30), a)
    T(img, 960, 366, "McDONALD'S", "anton", 50, SEP, "mm", a)
    for i in range(4): rrect(img, (740 + i * 120, 450, 820 + i * 120, 560), 6, (60, 48, 32), a)
    T(img, 960, 740, "Richard et Maurice McDonald", "anton", 66, SEP, "mm", a_in(t, 80.59))
    if t >= 83.7:
        T(img, 960, 830, "Des burgers très vite, toujours de la même façon… comme à l'usine", "semi", 36, SEP2, "mm", a_in(t, 83.71))

def s_kroc(img, t):
    a = sepia_card(img, t, 88.4)
    put(img, person_layer(200, SEP2), 560, 520, a)
    T(img, 560, 740, "RAY KROC", "anton", 80, SEP, "mm", a_in(t, 90.75))
    T(img, 560, 815, "vendeur de machines à milkshake", "semi", 34, SEP2, "mm", a_in(t, 89.2))
    T(img, 1200, 400, "Son idée :", "semi", 44, SEP2, "mm", a_in(t, 94.7))
    T(img, 1200, 480, "vendre le concept partout", "anton", 64, SEP, "mm", a_in(t, 95.9))
    T(img, 1200, 560, "en franchise", "anton", 64, YELLOW, "mm", a_in(t, 98.47))
    if t >= 99.71: stamp(img, 1200, 720, "1955 · 1er FRANCHISÉ", (230, 120, 60), 56, -5, a_in(t, 99.71, .2), scale=lerp(1.5, 1, eo(prog(t, 99.71, .3))))

def s_problem(img, t):
    a = sepia_card(img, t, 104.5)
    T(img, 960, 270, "UN PROBLÈME", "anton", 90, (230, 120, 60), "mm", a)
    T(img, 960, 380, "Kroc touche seulement", "semi", 46, SEP2, "mm", a_in(t, 105.92))
    v = 1.9 * eo(prog(t, 110.27, .8))
    T(img, 960, 520, fmt(v, 1) + " %", "anton", 200, SEP, "mm", a_in(t, 109.9), shadow=True)
    T(img, 960, 640, "des ventes de chaque restaurant", "semi", 42, SEP2, "mm", a_in(t, 109.9))
    T(img, 960, 720, "… dont une partie pour les frères McDonald", "semi", 38, SEP2, "mm", a_in(t, 111.95))
    if t >= 116.4: stamp(img, 960, 820, "PRESQUE PAS D'ARGENT", RED, 60, 3, a_in(t, 116.4, .2), scale=lerp(1.5, 1, eo(prog(t, 116.4, .3))))

def s_sonneborn(img, t):
    a = sepia_card(img, t, 118.8)
    put(img, person_layer(170, SEP), 470, 470, a)
    T(img, 470, 650, "HARRY SONNEBORN", "anton", 56, SEP, "mm", a_in(t, 119.95))
    T(img, 470, 715, "ancien financier", "semi", 34, SEP2, "mm", a_in(t, 121.18))
    # schéma terrain -> franchisé
    a2 = a_in(t, 126.9)
    rrect(img, (850, 330, 1190, 470), 16, (90, 70, 45), a2)
    T(img, 1020, 400, "McDONALD'S", "anton", 50, SEP, "mm", a2)
    if t >= 127.7:
        a3 = a_in(t, 127.71)
        rrect(img, (850, 560, 1190, 700), 16, (70, 110, 60), a3)
        T(img, 1020, 630, "TERRAIN", "anton", 56, SEP, "mm", a3)
        T(img, 1020, 520, "achète ou loue ↓", "semi", 30, SEP2, "mm", a3)
    if t >= 130.88:
        p = eo(prog(t, 130.88, .5))
        strike_line(img, 1200, 630, lerp(1200, 1380, p), 630, 1, SEP, 10)
        a4 = a_in(t, 131.3)
        rrect(img, (1390, 560, 1600, 700), 16, (110, 80, 50), a4)
        T(img, 1495, 610, "loue au", "semi", 28, SEP2, "mm", a4); T(img, 1495, 655, "FRANCHISÉ", "anton", 40, SEP, "mm", a4)
    if t >= 132.67: stamp(img, 1300, 800, "PLUS CHER", YELLOW, 70, -6, a_in(t, 132.67, .2), scale=lerp(1.6, 1, eo(prog(t, 132.67, .3))))

def s_quote(img, t):
    a = a_in(t, 133.79, .4)
    T(img, 300, 300, "«", "anton", 300, YELLOW, "mm", a)
    T(img, 960, 450, "Nous ne sommes pas vraiment", "anton", 92, WHITE, "mm", a_in(t, 136.07))
    T(img, 960, 560, "dans la restauration.", "anton", 92, WHITE, "mm", a_in(t, 136.9))
    T(img, 960, 700, "Nous sommes dans l'immobilier.", "anton", 104, YELLOW, "mm", a_in(t, 138.38), shadow=True)
    T(img, 960, 850, "Phrase attribuée à Harry Sonneborn", "semi", 34, GREY, "mm", a_in(t, 134.11))

def s_cheque(img, t):
    header(img, t, 140.35, "GRÂCE À L'ARGENT DES LOYERS…")
    if t >= 145.47: stamp(img, 1550, 260, "1961", YELLOW, 90, 8, a_in(t, 145.47, .2), scale=lerp(1.5, 1, eo(prog(t, 145.47, .3))))
    a = a_in(t, 146.83)
    rrect(img, (360, 340, 1460, 700), 18, (236, 230, 210), a)
    T(img, 420, 400, "PAYEZ À L'ORDRE DE : Richard et Maurice McDonald", "semi", 34, (60, 50, 40), "lm", a)
    T(img, 420, 470, "Pour : la marque et le concept McDonald's", "semi", 30, (90, 80, 70), "lm", a_in(t, 148.3))
    T(img, 1400, 590, fmt(2.7 * eo(prog(t, 150.07, .8)), 1) + " MILLIONS $", "anton", 96, (20, 90, 50), "rm", a_in(t, 149.95))
    T(img, 960, 790, "Les frères : un chèque", "anton", 56, GREY, "mm", a_in(t, 152.38))
    T(img, 960, 880, "Kroc : un empire… construit sur des terrains", "anton", 64, YELLOW, "mm", a_in(t, 154.59))

# ---------- 4. aujourd'hui ----------
def s_flows(img, t):
    header(img, t, 159.77, "CE QUE PAIE UN FRANCHISÉ")
    a = a_in(t, 162.41)
    put(img, person_layer(130), 380, 560, a)
    T(img, 380, 720, "LE FRANCHISÉ", "anton", 50, WHITE, "mm", a)
    put(img, building_layer(220), 1540, 540, a_in(t, 163.57))
    T(img, 1540, 720, "McDONALD'S", "anton", 50, YELLOW, "mm", a_in(t, 163.57))
    if t >= 166.81:
        p = eo(prog(t, 167.6, .6))
        strike_line(img, 520, 420, lerp(520, 1380, p), 420, 1, BLUE, 18)
        chip(img, 950, 360, "REDEVANCE", a_in(t, 167.61, .3), fill=BLUE, color=(6, 21, 39), size=40, kind="xbold")
        T(img, 950, 470, "% des ventes · marque, recettes, méthodes", "semi", 34, GREY, "mm", a_in(t, 168.69))
    if t >= 173.37:
        p = eo(prog(t, 175.13, .6))
        strike_line(img, 520, 640, lerp(520, 1380, p), 640, 1, YELLOW, 40)
        chip(img, 950, 580, "LOYER", a_in(t, 175.13, .3), fill=YELLOW, color=(12, 12, 16), size=54, kind="xbold")
        T(img, 950, 710, "le terrain ou le bâtiment appartient à McDonald's", "semi", 34, GREY, "mm", a_in(t, 177.69))
    if t >= 180.71:
        T(img, 950, 880, "Loyer = % des ventes + un minimum à payer quoi qu'il arrive", "bold", 40, WHITE, "mm", a_in(t, 182.17), dy=dy_in(t, 182.17))

def s_gauges(img, t):
    header(img, t, 187.85, "McDONALD'S EST PROPRIÉTAIRE DE…")
    gauge(img, 360, 400, 1000, .56, YELLOW, "des terrains", "", t, 192.49)
    gauge(img, 360, 620, 1000, .80, GREEN, "des bâtiments", "", t, 194.49)
    T(img, 960, 840, "Le reste : loué par McDonald's… puis sous-loué aux franchisés", "semi", 42, GREY, "mm", a_in(t, 197.13))
    source(img, t, 192.0, SRC_10K + " · pays gérés directement")

def s_rent_roy(img, t):
    header(img, t, 201.51, "CE QUE RAPPORTENT LES FRANCHISÉS (2025)")
    base, k = 800, 48
    for x, lab, v, ti, col in [(700, "Loyers", 10.4, 206.85, YELLOW), (1220, "Redevances", 6.0, 208.97, BLUE)]:
        p = eio(prog(t, ti, .8))
        bar_v(img, x, base, 300, v * k * p, col)
        if p > 0: T(img, x, base - v * k * p - 55, "≈ " + fmt(v * p, 0 if v == 6.0 else 1) + " Md$", "anton", 80, WHITE, "mm", a_in(t, ti, .2))
        T(img, x, base + 50, lab, "anton", 54, col, "mm", a_in(t, ti - .3))
    if t >= 212.8: stamp(img, 960, 945, "AVANT TOUT UN PROPRIÉTAIRE", RED, 56, -3, a_in(t, 212.8, .2), scale=lerp(1.5, 1, eo(prog(t, 212.8, .3))))
    if t < 212.6: source(img, t, 207.0, "FourWeekMBA, d'après le rapport annuel 2025 de McDonald's")

# ---------- 5. le chiffre qui dit tout ----------
def s_margins(img, t):
    T(img, 960, 120, "LE CHIFFRE QUI DIT TOUT", "anton", 80, YELLOW, "mm", a_in(t, 215.27))
    cols = [(520, "SES PROPRES RESTAURANTS", 9.7, 225.11, 1.4, 234.23, GREY, RED), (1400, "SES FRANCHISÉS", 16.5, 239.19, 13.9, 243.07, YELLOW, GREEN)]
    base, k = 880, 30
    for x, lab, v, tv, m, tm, c1, c2 in cols:
        T(img, x, 230, lab, "anton", 50, WHITE, "mm", a_in(t, tv - 3.5 if x < 960 else tv - 1.8))
        p = eio(prog(t, tv, .8))
        bar_v(img, x - 110, base, 170, v * k * p, c1)
        if p > 0: T(img, x - 110, base - v * k * p - 40, fmt(v, 1), "anton", 56, WHITE, "mm", a_in(t, tv, .2))
        T(img, x - 110, base + 36, "encaissé", "semi", 30, GREY, "mm", a_in(t, tv))
        q = eio(prog(t, tm, .8))
        bar_v(img, x + 110, base, 170, max(6, m * k * q) if q > 0 else 0, c2)
        if q > 0: T(img, x + 110, base - m * k * q - 40, fmt(m, 1), "anton", 56, c2, "mm", a_in(t, tm, .2))
        T(img, x + 110, base + 36, "marge", "semi", 30, GREY, "mm", a_in(t, tm))
    if 229.3 < t < 236.5:
        for i, (s, ti) in enumerate([("employés", 229.99), ("nourriture", 230.95), ("électricité…", 231.96)]):
            chip(img, 520, 330 + i * 70, "− " + s, a_in(t, ti, .25), fill=CARD, color=GREY, size=30)
    if t >= 245.87:
        T(img, 960, 520, "× 10", "anton", 260, GREEN, "mm", a_in(t, 245.87, .2), shadow=True, scale=lerp(1.6, 1, back(prog(t, 245.87, .4))))
    T(img, 960, 990, "Vendre des burgers : un peu.   Louer des restaurants : énormément.", "bold", 38, WHITE, "mm", a_in(t, 250.47))
    if t < 250.3: source(img, t, 225.0, SRC_10K + " · milliards de dollars")

# ---------- 6. pourquoi c'est génial ----------
def s_risks(img, t):
    header(img, t, 256.29, "1 · LE FRANCHISÉ PREND LES RISQUES")
    put(img, person_layer(150), 520, 520, a_in(t, 258.7))
    T(img, 520, 700, "LE FRANCHISÉ", "anton", 48, WHITE, "mm", a_in(t, 258.7))
    for i, (s, ti) in enumerate([("Embaucher", 261.81), ("Acheter les stocks", 262.69), ("Gérer au quotidien", 263.93)]):
        chip(img, 520, 790 + i * 70, s, a_in(t, ti, .25), fill=RED, color=WHITE, size=32, kind="xbold")
    a = a_in(t, 265.97)
    put(img, building_layer(220), 1400, 500, a)
    T(img, 1400, 680, "McDONALD'S", "anton", 48, YELLOW, "mm", a)
    chip(img, 1400, 780, "encaisse loyer + redevance", a_in(t, 267.28, .3), fill=GREEN, color=(10, 30, 20), size=34, kind="xbold")

def s_value(img, t):
    header(img, t, 270.43, "2 · LES TERRAINS PRENNENT DE LA VALEUR")
    X0, X1, Y1 = 260, 1100, 820
    p = eio(prog(t, 272.0, 2.5))
    pts = [(lerp(X0, X1, u / 40), Y1 - (u / 40) ** 1.6 * 420 - math.sin(u * .9) * 8) for u in range(int(40 * p) + 1)]
    strike_line(img, X0, Y1, X1, Y1, 1, LINE, 4, a_in(t, 270.5))
    if len(pts) > 1: shape(img, (X0, 300, X1 + 10, Y1 + 10), lambda d, ox, oy, w, h: d.line([(x - X0 + ox, y - 300 + oy) for x, y in pts], fill=GREEN + (255,), width=10, joint="curve"))
    T(img, X0, 330, "valeur de l'immobilier", "bold", 34, GREY, "lm", a_in(t, 272.0))
    T(img, X1, Y1 + 40, "les années passent →", "semi", 30, DIM, "rm", a_in(t, 272.0))
    sh = 1 - eo(prog(t, 276.17, 1.2)) * .75
    put(img, burger_layer(260), 1450, 420, a_in(t, 275.65), scale=max(.05, sh))
    T(img, 1450, 560, "mangé en quelques minutes", "semi", 32, GREY, "mm", a_in(t, 276.17))
    put(img, building_layer(170), 1450, 760, a_in(t, 277.65))
    T(img, 1450, 900, "l'immobilier, lui, reste", "bold", 34, GREEN, "mm", a_in(t, 278.43))

def s_control(img, t):
    header(img, t, 280.13, "3 · LE CONTRÔLE")
    a = a_in(t, 281.89)
    cx, cy = 600, 560
    shape(img, (cx - 120, cy - 220, cx + 120, cy - 20), lambda d, ox, oy, w, h: d.arc((ox, oy, ox + w, oy + h * 1.6), 180, 360, fill=WHITE + (255,), width=34), a)
    rrect(img, (cx - 170, cy - 60, cx + 170, cy + 200), 30, YELLOW, a)
    shape(img, (cx - 28, cy + 40, cx + 28, cy + 110), lambda d, ox, oy, w, h: d.ellipse((ox, oy, ox + w, oy + w), fill=(12, 12, 16, 255)), a)
    T(img, 1300, 400, "Propriétaire des murs", "anton", 70, WHITE, "mm", a_in(t, 282.93))
    T(img, 1300, 490, "= énorme moyen de pression", "semi", 44, YELLOW, "mm", a_in(t, 285.05))
    T(img, 1300, 640, "Ne pas respecter les règles, c'est risquer :", "semi", 40, GREY, "mm", a_in(t, 288.29))
    chip(img, 1300, 730, "de perdre l'enseigne", a_in(t, 291.97, .3), fill=CARD, color=WHITE, size=40, outline=(70, 70, 85))
    chip(img, 1300, 830, "… et l'emplacement", a_in(t, 294.05, .3), fill=RED, color=WHITE, size=40, kind="xbold")

def s_opinc(img, t):
    header(img, t, 295.65, "LE RÉSULTAT EN 2025")
    T(img, 520, 420, fmt(12.4 * eo(prog(t, 300.65, 1.0)), 1) + " Md$", "anton", 150, GREEN, "mm", a_in(t, 300.29), shadow=True)
    T(img, 520, 530, "résultat d'exploitation", "semi", 40, GREY, "mm", a_in(t, 302.09))
    T(img, 1400, 420, "26,9 Md$", "anton", 150, WHITE, "mm", a_in(t, 303.89), shadow=True)
    T(img, 1400, 530, "de revenus", "semi", 40, GREY, "mm", a_in(t, 305.57))
    p = eo(prog(t, 306.65, 1.0)) * 12.4 / 26.9
    a = a_in(t, 306.6)
    rrect(img, (260, 660, 1660, 720), 30, CARD, a)
    if p > 0: rrect(img, (260, 660, 260 + max(60, 1400 * p), 720), 30, GREEN, a)
    T(img, 960, 800, "Presque la moitié devient du bénéfice d'exploitation", "anton", 60, WHITE, "mm", a_in(t, 306.65))
    T(img, 960, 890, "Pour une entreprise de restauration, c'est énorme", "semi", 42, YELLOW, "mm", a_in(t, 311.23))
    source(img, t, 300.0, SRC_10K)

# ---------- 6 bis. nuance ----------
def s_nuance(img, t):
    header(img, t, 315.24, "ATTENTION : LES BURGERS COMPTENT QUAND MÊME")
    a = a_in(t, 315.3)
    cx, cy = 960, 470
    rrect(img, (cx - 10, cy, cx + 10, 760), 6, GREY, a); rrect(img, (cx - 120, 750, cx + 120, 780), 10, GREY, a)
    strike_line(img, cx - 460, cy, cx + 460, cy, 1, GREY, 12, a)
    put(img, burger_layer(260), cx - 460, cy - 100, a)
    put(img, building_layer(150), cx + 460, cy - 120, a)
    T(img, 960, 860, "Loyer et redevance = un pourcentage des ventes", "bold", 44, WHITE, "mm", a_in(t, 320.12))
    T(img, 960, 940, "Moins de ventes → moins d'argent pour McDonald's", "semi", 40, RED, "mm", a_in(t, 324.28))

def s_cycle(img, t):
    header(img, t, 328.63, "LE CERCLE DU SYSTÈME")
    cx, cy, R = 960, 560, 290
    labs = [("Publicité, menus, applis", 329.96), ("Plus de ventes", 335.8), ("Plus de loyers", 337.48), ("Plus de moyens", 338.4)]
    for i, (s, ti) in enumerate(labs):
        ang = -math.pi / 2 + i * math.pi / 2
        x, y = cx + 470 * math.cos(ang), cy + R * math.sin(ang)
        chip(img, x, y, s, a_in(t, ti, .3), fill=[BLUE, YELLOW, GREEN, CARD][i], color=(12, 12, 16) if i < 3 else WHITE, size=38, kind="xbold")
    p = eo(prog(t, 330.0, 8.0))
    if p > 0:
        shape(img, (cx - 470, cy - R, cx + 470, cy + R), lambda d, ox, oy, w, h: d.arc((ox + 40, oy + 40, ox + w - 40, oy + h - 40), -80, -80 + 340 * p, fill=(90, 90, 110, 255), width=8))
    if t >= 339.51:
        rrect(img, (cx - 190, cy - 90, cx + 190, cy + 90), 24, BG, a_in(t, 339.51))
        T(img, cx, cy - 30, "LE BURGER", "anton", 60, YELLOW, "mm", a_in(t, 339.51))
        T(img, cx, cy + 35, "= le moteur", "semi", 40, WHITE, "mm", a_in(t, 342.6))

# ---------- 7. France ----------
FRANCE = [(0.46, 0.02), (0.58, 0.08), (0.74, 0.12), (0.86, 0.22), (0.82, 0.38), (0.86, 0.55), (0.80, 0.68), (0.84, 0.82), (0.70, 0.90),
          (0.56, 0.86), (0.44, 0.98), (0.30, 0.92), (0.20, 0.80), (0.24, 0.62), (0.16, 0.48), (0.02, 0.38), (0.10, 0.30), (0.26, 0.30), (0.34, 0.16)]
_fdots = None
def _france_dots(x0, y0, s):
    global _fdots
    if _fdots is None:
        poly = [(x0 + u * s, y0 + v * s) for u, v in FRANCE]
        mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).polygon(poly, fill=255)
        r = random.Random(4); pts = []
        while len(pts) < 260:
            x, y = r.uniform(x0, x0 + s), r.uniform(y0, y0 + s)
            if mask.getpixel((int(x), int(y))): pts.append((x, y))
        _fdots = (poly, pts)
    return _fdots

def s_france(img, t):
    header(img, t, 347.15, "ET EN FRANCE ?")
    poly, pts = _france_dots(260, 190, 760)
    a = a_in(t, 347.3)
    shape(img, (250, 180, 1030, 960), lambda d, ox, oy, w, h: d.polygon([(x - 250 + ox, y - 180 + oy) for x, y in poly], fill=(30, 30, 42, 255), outline=(80, 80, 100, 255)), a)
    n = int(len(pts) * eo(prog(t, 349.4, 2.2)))
    for i, (x, y) in enumerate(pts[:n]):
        col = WHITE if (t >= 352.7 and i % 7 != 0) else YELLOW
        img.paste(col, (int(x) - 5, int(y) - 5, int(x) + 5, int(y) + 5))
    T(img, 1450, 430, "1 600+", "anton", 200, WHITE, "mm", a_in(t, 350.11), shadow=True)
    T(img, 1450, 560, "RESTAURANTS McDONALD'S", "anton", 48, YELLOW, "mm", a_in(t, 351.35))
    T(img, 1450, 680, "l'immense majorité", "semi", 44, GREY, "mm", a_in(t, 352.71))
    T(img, 1450, 740, "tenue par des franchisés", "bold", 44, WHITE, "mm", a_in(t, 354.19))
    source(img, t, 350.0, "classement France Snacking 2026 (1 629 restaurants)")

def s_receipt(img, t):
    header(img, t, 355.99, "SUR 100 € DE BURGERS VENDUS EN FRANCE")
    a = a_in(t, 356.2)
    x0, y0, w = 560, 220, 800
    rrect(img, (x0, y0, x0 + w, 900), 10, (246, 244, 236), a)
    for i in range(16):
        xx = x0 + i * w / 16
        shape(img, (xx, 892, xx + w / 16, 920), lambda d, ox, oy, ww, hh: d.polygon([(ox, oy), (ox + ww / 2, oy + hh), (ox + ww, oy)], fill=(246, 244, 236, 255)), a)
    T(img, x0 + w / 2, y0 + 70, "TICKET · 100,00 €", "anton", 56, (30, 30, 36), "mm", a)
    rows = [("Loyer", "≈ 10 €", 363.73), ("Redevance de marque", "≈ 5 €", 365.15), ("Publicité", "4 à 5 €", 366.91)]
    for i, (lab, v, ti) in enumerate(rows):
        y = y0 + 190 + i * 100
        T(img, x0 + 50, y, lab, "semi", 44, (60, 60, 70), "lm", a_in(t, ti))
        T(img, x0 + w - 50, y, v, "anton", 60, (200, 40, 30), "rm", a_in(t, ti))
    aa = a_in(t, 369.59)
    shape(img, (x0 + 40, y0 + 480, x0 + w - 40, y0 + 484), lambda d, ox, oy, ww, hh: d.rectangle((ox, oy, ox + ww, oy + hh), fill=(120, 120, 130, 255)), aa)
    T(img, x0 + 50, y0 + 560, "Vers McDonald's", "bold", 44, (30, 30, 36), "lm", aa)
    T(img, x0 + w - 50, y0 + 560, "≈ 20 €", "anton", 80, (200, 40, 30), "rm", a_in(t, 371.55))
    T(img, 960, 980, "Ces pourcentages varient selon les contrats et les emplacements", "semi", 32, GREY, "mm", a_in(t, 375.39))
    source(img, t, 358.0, "Toute-la-franchise.com (estimations)")

# ---------- 8. conclusion ----------
def s_bait(img, t):
    T(img, 960, 150, "ALORS, McDONALD'S VEND DES BURGERS ?", "anton", 72, WHITE, "mm", a_in(t, 379.68))
    T(img, 960, 250, "Oui.", "anton", 72, YELLOW, "mm", a_in(t, 382.88))
    put(img, burger_layer(380), 560, 600, a_in(t, 383.56))
    if t >= 383.88:
        lay = price_tag(330, 120, "L'APPÂT", color=RED, text_color=WHITE, size=60)
        rotate_paste(img, lay, 600, 380, 10, a_in(t, 383.88, .3), scale=lerp(1.4, 1, eo(prog(t, 383.88, .3))))
    lit = eo(prog(t, 389.36, 1.5))
    put(img, building_layer(300, lit), 1380, 580, a_in(t, 386.69))
    if t >= 389.36: T(img, 1380, 900, "LE VRAI BUSINESS : LE TERRAIN", "anton", 56, GREEN, "mm", a_in(t, 389.36))

def s_lesson(img, t):
    a = a_in(t, 392.69, .4)
    T(img, 960, 400, "Ce qu'une entreprise vend", "anton", 110, WHITE, "mm", a, shadow=True)
    T(img, 960, 540, "n'est pas toujours", "anton", 110, WHITE, "mm", a_in(t, 396.84), shadow=True)
    T(img, 960, 680, "ce qui la fait gagner de l'argent.", "anton", 110, YELLOW, "mm", a_in(t, 397.72), shadow=True)

def s_cards(img, t):
    header(img, t, 399.5, "LE MÊME PRINCIPE, PARTOUT")
    items = [("L'imprimante", "pas chère", "Les cartouches", "hors de prix", 399.52, 401.28),
             ("Le rasoir", "offert", "Les lames", "à vie", 403.08, 404.72),
             ("La console", "presque sans marge", "Jeux, abonnements", "derrière", 406.8, 409.36)]
    for i, (a1, b1, a2, b2, t1, t2) in enumerate(items):
        x = 360 + i * 600
        flip = prog(t, t2, .5)
        sx = abs(math.cos(flip * math.pi))
        front = flip < .5
        al = a_in(t, t1, .3)
        if al <= 0: continue
        w = 480 * max(.04, sx)
        col = CARD if front else (20, 70, 45)
        rrect(img, (x - w / 2, 300, x + w / 2, 760), 26, col, al, outline=(80, 80, 100, 255) if front else GREEN + (255,), width=4)
        if sx > .3:
            T(img, x, 470, a1 if front else a2, "anton", 56, WHITE, "mm", al)
            T(img, x, 560, b1 if front else b2, "semi", 38, GREY if front else GREEN, "mm", al)
    T(img, 960, 870, "Le produit que tu vois n'est que la porte d'entrée", "bold", 46, YELLOW, "mm", a_in(t, 411.44))
    if t >= 417.3:
        rrect(img, (0, 0, W, H), 0, BG, a_in(t, 417.44, .4) * .96)
        T(img, 960, 420, "La prochaine fois que tu achètes quelque chose :", "semi", 52, GREY, "mm", a_in(t, 417.44))
        T(img, 960, 560, "SUR QUOI CETTE ENTREPRISE", "anton", 100, WHITE, "mm", a_in(t, 420.8))
        T(img, 960, 680, "GAGNE-T-ELLE VRAIMENT SON ARGENT ?", "anton", 100, YELLOW, "mm", a_in(t, 421.44))

_bf_thumb = None
def s_outro_mc(img, t, logo):
    global _bf_thumb
    a = a_in(t, 424.56)
    paste(img, logo, 960 - logo.width / 2, 120, a)
    T(img, 960, 420, "L'ENVERS DU BUSINESS", "anton", 96, WHITE, "mm", a)
    if t >= 428.4:
        s = back(prog(t, 428.4, .35))
        rrect(img, (960 - 230 * s, 520 - 50 * s, 960 + 230 * s, 520 + 50 * s), 50 * s, RED, 1)
        T(img, 960, 522, "S'ABONNER", "anton", 56, WHITE, "mm", 1, scale=max(.01, s))
    if t >= 429.36:
        if _bf_thumb is None:
            _bf_thumb = Image.open(os.path.join(HERE, "../../black_friday/miniature_c_le_piege.png")).convert("RGBA").resize((512, 288), Image.LANCZOS)
        a2 = a_in(t, 429.36, .4)
        T(img, 960, 640, "Tu as raté la vidéo sur le Black Friday ?", "semi", 40, GREY, "mm", a2)
        rrect(img, (700, 690, 1220, 986), 14, YELLOW, a2)
        paste(img, _bf_thumb, 704, 694, a2)
