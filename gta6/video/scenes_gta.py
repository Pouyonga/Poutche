# Scènes de la vidéo « GTA 6 : comment un jeu vidéo rapporte des MILLIARDS en quelques jours ».
# Aucune image du jeu ni logo : uniquement des formes et textes maison. Temps = voix off.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../mcdonalds/video"))
sys.path.insert(0, os.path.join(HERE, "../../black_friday/video"))
from PIL import Image, ImageDraw
from gfx import *
from scenes import background, header, source, a_in, dy_in, s_endcard
from scenes_mc import burger_layer, building_layer, person_layer, put, bar_v

PINK = (255, 80, 170); PURPLE = (150, 90, 255); ORANGE = (255, 150, 40)

_ic = {}
def pad_layer(w, col=(40, 40, 54)):
    """Manette de jeu stylisée (générique)."""
    key = ("pad", int(w), col)
    if key in _ic: return _ic[key]
    s = w / 600; L = Image.new("RGBA", (int(600 * s) + 4, int(360 * s) + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    S = lambda *v: tuple(int(x * s) for x in v)
    d.rounded_rectangle(S(40, 40, 560, 250), int(110 * s), fill=col)
    d.ellipse(S(0, 120, 230, 360), fill=col); d.ellipse(S(370, 120, 600, 360), fill=col)
    d.rectangle(S(115, 115, 145, 225), fill=WHITE); d.rectangle(S(75, 155, 185, 185), fill=WHITE)
    for (x, y, c) in [(450, 110, GREEN), (500, 160, RED), (400, 160, BLUE), (450, 210, YELLOW)]:
        d.ellipse(S(x - 24, y - 24, x + 24, y + 24), fill=c)
    d.ellipse(S(215, 210, 285, 280), fill=(20, 20, 28)); d.ellipse(S(315, 210, 385, 280), fill=(20, 20, 28))
    _ic[key] = L; return L

def bills(img, cx, base, n, a=1.0):
    for k in range(n):
        y = base - k * 26
        rrect(img, (cx - 170 + (k % 2) * 8, y - 30, cx + 170 + (k % 2) * 8, y), 6, (40, 150, 85), a, outline=(20, 90, 50, 255), width=3)

def tag_layer(text, w=520, h=220):
    return price_tag(w, h, text, size=int(h * .45))

def counter_big(img, t, t0, t1, v, fmt_fn, y, size=200, color=WHITE):
    p = eio(prog(t, t0, t1 - t0))
    T(img, 960, y, fmt_fn(v * p), "anton", size, color, "mm", a_in(t, t0 - .2, .2), shadow=True)

def money(v):
    s = f"{int(round(v)):,}".replace(",", " ")
    return s + " $"

# ---------- 1. accroche ----------
def s_hook(img, t):
    put(img, pad_layer(520), 960, 640, a_in(t, 0, .3), scale=lerp(.75, 1, eo(prog(t, 0, .5))))
    if t < 3.9:
        counter_big(img, t, 1.0, 3.0, 1e9, money, 230, 150)
        T(img, 960, 340, "coût de fabrication (estimation)", "semi", 42, GREY, "mm", a_in(t, 1.5))
    elif t < 9.2:
        counter_big(img, t, 6.2, 8.0, 1e9, money, 230, 150, GREEN)
        T(img, 960, 340, "de précommandes… avant même la sortie", "semi", 42, GREEN, "mm", a_in(t, 6.2))
    else:
        chip(img, 960, 230, "GTA 6 · sorti le 19 novembre 2026", a_in(t, 9.2, .3), fill=CARD, color=WHITE, size=50, kind="xbold", outline=(80, 80, 100))
        T(img, 960, 350, "une machine à argent", "anton", 80, YELLOW, "mm", a_in(t, 15.6))
    if t >= 18.8:
        a = a_in(t, 18.8, .4)
        rrect(img, (0, 0, W, H), 0, BG, a * .985)
        T(img, 960, 400, "COMMENT UN JEU VIDÉO RAPPORTE", "anton", 100, WHITE, "mm", a)
        T(img, 960, 540, "DES MILLIARDS", "anton", 170, GREEN, "mm", a_in(t, 22.4, .3), shadow=True)
        T(img, 960, 690, "… en quelques jours ?", "semi", 60, GREY, "mm", a_in(t, 24.0))

# ---------- 2. le pari ----------
def s_cost(img, t):
    header(img, t, 25.98, "LE COÛT DE FABRICATION")
    n = int(16 * eo(prog(t, 33.4, 3.0)))
    bills(img, 620, 880, n, a_in(t, 33.4))
    T(img, 1330, 430, "Chiffre officiel : aucun", "semi", 44, GREY, "mm", a_in(t, 30.3))
    T(img, 1330, 560, "1 à 1,5 Md$", "anton", 150, GREEN, "mm", a_in(t, 36.14), shadow=True)
    T(img, 1330, 670, "estimation des analystes", "semi", 38, GREY, "mm", a_in(t, 36.14))
    if t >= 39.82: chip(img, 1330, 790, "+ la publicité, en plus", a_in(t, 39.82, .3), fill=RED, color=WHITE, size=42, kind="xbold")
    source(img, t, 36.0, "estimations d'analystes, via NME")

def s_compare(img, t):
    header(img, t, 42.0, "POUR COMPARER")
    base, k = 860, 380
    a1 = a_in(t, 43.34)
    bar_v(img, 620, base, 300, k * .35 * eo(prog(t, 43.34, .8)), GREY, a1)
    T(img, 620, base + 50, "Les films les plus chers", "bold", 38, GREY, "mm", a1)
    T(img, 620, base - k * .35 - 60, "quelques centaines de M$", "anton", 52, WHITE, "mm", a_in(t, 45.26))
    a2 = a_in(t, 47.82)
    bar_v(img, 1300, base, 300, k * 1.25 * eo(prog(t, 47.82, .9)), GREEN, a2)
    T(img, 1300, base + 50, "GTA 6", "anton", 54, GREEN, "mm", a2)
    T(img, 1300, base - k * 1.25 - 60, "plus d'1 milliard $", "anton", 60, WHITE, "mm", a_in(t, 48.2))

def s_staff(img, t):
    header(img, t, 53.44, "UNE ARMÉE POUR UN SEUL JEU")
    for col_i, (x0, n, ti, lab, c) in enumerate([(220, 24, 60.66, "2 441", GREY), (1000, 47, 64.58, "4 711", YELLOW)]):
        a = a_in(t, ti - .3)
        shown = int(n * eo(prog(t, ti - .3, 1.2)))
        for i in range(shown):
            r, cc = divmod(i, 10)
            put(img, person_layer(48, c), x0 + cc * 66, 330 + r * 92, 1)
        T(img, x0 + 300, 840, lab, "anton", 120, c, "mm", a, shadow=True)
        T(img, x0 + 300, 935, "employés en " + ("2018" if col_i == 0 else "2026"), "semi", 38, GREY, "mm", a)
    T(img, 960, 1000, "1 silhouette = 100 personnes", "med", 28, DIM, "mm", a_in(t, 60.0))
    if t >= 69.22: chip(img, 960, 200, "Presque × 2", a_in(t, 69.22, .3), fill=RED, color=WHITE, size=46, kind="xbold")
    source(img, t, 59.0, "Bloomberg")

def s_time(img, t):
    header(img, t, 72.94, "ET IL Y A LE TEMPS")
    a = a_in(t, 74.78)
    strike_line(img, 300, 500, lerp(300, 1620, eio(prog(t, 75.3, 2.5))), 500, 1, GREY, 10, a)
    for x, lab, ti in [(300, "2013", 77.82), (1620, "2026", 78.6)]:
        shape(img, (x - 22, 478, x + 22, 522), lambda d, ox, oy, w, h: d.ellipse((ox, oy, ox + w, oy + h), fill=YELLOW + (255,)), a_in(t, ti))
        T(img, x, 580, lab, "anton", 70, WHITE, "mm", a_in(t, ti))
        T(img, x, 650, "GTA 5" if lab == "2013" else "GTA 6", "semi", 40, GREY, "mm", a_in(t, ti))
    T(img, 960, 400, "13 ANS", "anton", 160, YELLOW, "mm", a_in(t, 79.26, .3), shadow=True)
    for i, (s, ti) in enumerate([("salaires", 81.5), ("technologie", 82.42), ("tests", 83.5)]):
        chip(img, 640 + i * 320, 790, s, a_in(t, ti, .25), fill=CARD, color=WHITE, size=42, outline=(80, 80, 100))
    T(img, 960, 920, "… et un jeu repoussé plusieurs fois", "semi", 44, RED, "mm", a_in(t, 85.02))

# ---------- 3. GTA 5 ----------
def s_gta5(img, t):
    header(img, t, 89.31, "LE PRÉCÉDENT : GTA 5, EN 2013")
    if t < 103.4:
        T(img, 960, 470, f"{int(800 * eo(prog(t, 99.47, 1.2)))} M$", "anton", 240, GREEN, "mm", a_in(t, 99.2), shadow=True)
        T(img, 960, 640, "en une seule journée", "anton", 70, WHITE, "mm", a_in(t, 101.71))
    else:
        T(img, 960, 380, "1 MILLIARD $", "anton", 200, GREEN, "mm", a_in(t, 103.58, .3), shadow=True)
        T(img, 960, 520, "en 3 jours", "anton", 80, WHITE, "mm", a_in(t, 104.0))
        a = a_in(t, 106.3)
        cx, cy = 960, 760
        shape(img, (cx - 90, cy - 110, cx + 90, cy + 40), lambda d, ox, oy, w, h: d.pieslice((ox, oy - h, ox + w, oy + h), 0, 180, fill=YELLOW + (255,)), a)
        rrect(img, (cx - 22, cy + 30, cx + 22, cy + 90), 4, YELLOW, a); rrect(img, (cx - 70, cy + 88, cx + 70, cy + 110), 6, YELLOW, a)
        T(img, cx, cy + 160, "Record du monde homologué par le Guinness", "bold", 40, WHITE, "mm", a_in(t, 107.34))
        T(img, cx, cy + 220, "plus rapide que n'importe quel film", "semi", 36, YELLOW, "mm", a_in(t, 114.06))
    source(img, t, 99.0, "Guinness World Records, 2013")

def s_copies(img, t):
    header(img, t, 116.4, "13 ANS PLUS TARD")
    T(img, 960, 450, f"{int(230 * eo(prog(t, 120.83, 1.4)))} MILLIONS", "anton", 200, WHITE, "mm", a_in(t, 120.5), shadow=True)
    T(img, 960, 590, "d'exemplaires de GTA 5 vendus", "semi", 52, GREY, "mm", a_in(t, 121.95))
    T(img, 960, 680, "… et il se vend encore chaque année", "semi", 42, GREY, "mm", a_in(t, 122.99))
    if t >= 129.23: stamp(img, 960, 860, "UN PARI CALCULÉ", GREEN, 80, -4, a_in(t, 129.23, .2), scale=lerp(1.5, 1, eo(prog(t, 129.23, .3))))
    source(img, t, 121.0, "Take-Two, via TweakTown")

# ---------- 4. précommandes ----------
def s_preorders(img, t):
    header(img, t, 131.69, "AVANT MÊME LE PREMIER JOUR")
    a = a_in(t, 133.0)
    cx, cy = 520, 560
    shape(img, (cx - 200, cy - 150, cx + 200, cy + 190), lambda d, ox, oy, w, h: (d.line([(ox, oy), (ox + 60, oy), (ox + 110, oy + 230), (ox + w - 30, oy + 230), (ox + w, oy + 60), (ox + 80, oy + 60)], fill=WHITE + (255,), width=14),
          d.ellipse((ox + 110, oy + h - 70, ox + 170, oy + h - 10), fill=WHITE + (255,)), d.ellipse((ox + w - 110, oy + h - 70, ox + w - 50, oy + h - 10), fill=WHITE + (255,))), a)
    n = int(10 * eo(prog(t, 137.9, 3)))
    for k in range(n):
        T(img, cx - 90 + (k % 5) * 50, cy - 30 - (k // 5) * 50, "$", "anton", 60, GREEN, "mm", 1)
    T(img, 1350, 420, "Précommandes", "semi", 46, GREY, "mm", a_in(t, 137.93))
    T(img, 1350, 540, "+ d'1 Md$", "anton", 140, GREEN, "mm", a_in(t, 139.29), shadow=True)
    T(img, 1350, 660, "jusqu'à 1,6 Md$ selon certaines", "semi", 40, WHITE, "mm", a_in(t, 141.85))
    T(img, 1350, 740, "estimations, pas de chiffre officiel", "semi", 34, DIM, "mm", a_in(t, 136.49))
    source(img, t, 138.0, "estimations Sensor Tower et autres, via Forbes et Yahoo Finance")

def s_price(img, t):
    header(img, t, 145.27, "LE PRIX")
    lay = tag_layer("79,99 €", 640, 260)
    rotate_paste(img, lay, 960, 480, 4, a_in(t, 146.6, .3), scale=lerp(1.4, 1, back(prog(t, 146.6, .45))))
    T(img, 960, 720, "édition standard · France", "semi", 46, GREY, "mm", a_in(t, 148.71))
    T(img, 960, 820, "plus cher que la plupart des jeux", "bold", 48, RED, "mm", a_in(t, 150.33))
    source(img, t, 147.0, "Dexerto")

def s_forecast(img, t):
    header(img, t, 152.53, "CE QUE PRÉVOIT TAKE-TWO")
    T(img, 960, 400, "3,35 à 3,5 Md$", "anton", 170, YELLOW, "mm", a_in(t, 154.81, .3), shadow=True)
    T(img, 960, 530, "de ventes sur octobre-décembre 2026", "semi", 48, GREY, "mm", a_in(t, 158.17))
    chip(img, 960, 680, "Chiffres officiels de la sortie : pas encore publiés", a_in(t, 161.75, .3), fill=CARD, color=WHITE, size=38, outline=(80, 80, 100))
    T(img, 960, 830, "Le budget record, remboursé en quelques jours ?", "anton", 64, GREEN, "mm", a_in(t, 166.65))
    source(img, t, 155.0, "prévisions de Take-Two, via Shattered")

# ---------- 5. le vrai jackpot ----------
def s_jackpot(img, t):
    T(img, 960, 180, "LE VRAI JACKPOT", "anton", 110, YELLOW, "mm", a_in(t, 172.3, .3), shadow=True)
    put(img, pad_layer(420), 960, 560, a_in(t, 174.3))
    if t >= 178.19:
        for k in range(10):
            ph = ((t - 178.19) * .8 + k / 10) % 1
            x = 960 + math.sin(k * 2.1) * 260
            T(img, x, lerp(560, 960, ph), "$", "anton", 64, GREEN, "mm", (1 - ph) * a_in(t, 178.19))
    T(img, 960, 860, "ce que tu dépenses APRÈS l'avoir acheté", "anton", 64, WHITE, "mm", a_in(t, 178.19))

def s_online(img, t):
    header(img, t, 181.58, "GTA ONLINE : LE MODE EN LIGNE")
    a = a_in(t, 182.0)
    rrect(img, (220, 260, 900, 860), 30, (24, 24, 36), a, outline=(90, 90, 120, 255), width=4)
    T(img, 560, 330, "MODE EN LIGNE", "anton", 54, WHITE, "mm", a)
    T(img, 560, 400, "gratuit avec le jeu", "semi", 34, GREEN, "mm", a_in(t, 186.38))
    T(img, 560, 520, "argent virtuel", "bold", 40, GREY, "mm", a_in(t, 189.9))
    T(img, 560, 600, "= argent réel", "anton", 70, YELLOW, "mm", a_in(t, 191.74))
    for i, (s, ti) in enumerate([("une voiture", 193.38), ("un appartement", 194.3), ("une arme", 195.26)]):
        chip(img, 330 + i * 230, 760, s, a_in(t, ti, .25), fill=PURPLE, color=WHITE, size=30, kind="xbold")
    T(img, 1400, 470, "≈ 5 Md$", "anton", 170, GREEN, "mm", a_in(t, 201.34, .3), shadow=True)
    T(img, 1400, 600, "en 10 ans", "anton", 64, WHITE, "mm", a_in(t, 202.98))
    T(img, 1400, 690, "selon des fuites, jamais confirmées", "semi", 36, RED, "mm", a_in(t, 196.62))
    source(img, t, 200.0, "fuites relayées par la presse spécialisée (RespawnFirst)")

def s_pie(img, t):
    header(img, t, 204.14, "LE CŒUR DE TAKE-TWO")
    cx, cy, R = 560, 500, 230
    p = eo(prog(t, 209.5, 1.2)) * .78
    a = a_in(t, 205.0)
    shape(img, (cx - R, cy - R, cx + R, cy + R), lambda d, ox, oy, w, h: (d.ellipse((ox, oy, ox + w, oy + h), fill=CARD + (255,)),
          d.pieslice((ox, oy, ox + w, oy + h), -90, -90 + 360 * p, fill=YELLOW + (255,)) if p > 0 else None), a)
    T(img, cx, cy + R + 80, f"{round(p * 100)} % des revenus", "anton", 80, YELLOW, "mm", a_in(t, 209.5))
    T(img, 1330, 360, "« dépenses récurrentes »", "anton", 64, YELLOW, "mm", a_in(t, 213.28))
    for i, (s, ti) in enumerate([("achats dans les jeux", 214.94), ("abonnements", 216.22), ("contenus supplémentaires", 217.22)]):
        chip(img, 1330, 470 + i * 80, s, a_in(t, ti, .25), fill=CARD, color=WHITE, size=36, outline=(80, 80, 100))
    T(img, 1330, 780, "Le jeu à 80 € = la porte d'entrée", "bold", 44, WHITE, "mm", a_in(t, 219.1))
    T(img, 1330, 860, "Le vrai business = tout ce qui vient après", "bold", 44, GREEN, "mm", a_in(t, 222.09))
    source(img, t, 209.0, "résultats de Take-Two, exercice 2026, via Tiger Brokers")

def s_callback(img, t):
    T(img, 960, 200, "Ça te rappelle quelque chose ?", "anton", 80, WHITE, "mm", a_in(t, 226.46))
    put(img, burger_layer(300), 620, 560, a_in(t, 228.14))
    lay = price_tag(300, 110, "L'APPÂT", color=RED, text_color=WHITE, size=54)
    rotate_paste(img, lay, 650, 390, 10, a_in(t, 228.38))
    put(img, building_layer(220), 1300, 560, a_in(t, 229.26))
    T(img, 960, 880, "Ce qui rapporte le plus n'est pas ce que tu crois acheter", "bold", 46, YELLOW, "mm", a_in(t, 230.0))

# ---------- 6. risques ----------
def s_risks(img, t):
    header(img, t, 234.77, "LES RISQUES DU PARI")
    if t < 250.0:
        T(img, 960, 380, "Tout miser sur un seul jeu", "anton", 90, WHITE, "mm", a_in(t, 237.05))
        chip(img, 960, 540, "le moindre retard coûte des millions", a_in(t, 239.89, .3), fill=RED, color=WHITE, size=44, kind="xbold")
        chip(img, 960, 660, "une entreprise qui dépend d'une seule franchise", a_in(t, 242.4, .3), fill=CARD, color=WHITE, size=40, outline=(80, 80, 100))
        T(img, 960, 820, "Si GTA 6 avait déçu…", "semi", 50, GREY, "mm", a_in(t, 245.81))
        return
    X0, X1, Y1 = 300, 1300, 860
    a = a_in(t, 250.08)
    strike_line(img, X0, Y1, X1, Y1, 1, LINE, 4, a)
    p = eio(prog(t, 250.5, 3.0))
    r = random.Random(3)
    pts = []; y = 700
    for i in range(int(36 * p) + 1):
        y += r.uniform(-14, 16) - (40 if i > 30 else 0)
        pts.append((lerp(X0, X1, i / 36), y))
    if len(pts) > 1: shape(img, (X0, 300, X1 + 20, Y1), lambda d, ox, oy, w, h: d.line([(x - X0 + ox, yy - 300 + oy) for x, yy in pts], fill=GREEN + (255,), width=10, joint="curve"))
    T(img, X0, 330, "action Take-Two", "bold", 40, GREY, "lm", a)
    T(img, 1560, 520, "≈ + 6 %", "anton", 150, GREEN, "mm", a_in(t, 255.97, .3), shadow=True)
    T(img, 1560, 640, "au lancement", "semi", 44, WHITE, "mm", a_in(t, 256.69))
    T(img, 960, 220, "Premiers retours : excellents", "anton", 70, WHITE, "mm", a_in(t, 250.88))
    source(img, t, 253.0, "Forbes, 18 novembre 2026")

# ---------- 7. conclusion ----------
def s_three(img, t):
    put(img, pad_layer(380), 960, 560, a_in(t, 259.15))
    for i, (lab, ti, col, ang) in enumerate([("le jeu", 260.95, WHITE, -90), ("l'en ligne", 271.13, PURPLE, 30), ("des années de revenus", 273.39, GREEN, 150)]):
        x = 960 + 440 * math.cos(math.radians(ang)); y = 560 + 300 * math.sin(math.radians(ang))
        chip(img, x, y, lab, a_in(t, ti, .3), fill=col if i else CARD, color=(12, 12, 16) if i else WHITE, size=46, kind="xbold", outline=(80, 80, 100) if not i else None)
    T(img, 960, 140, "Un pari à plus d'1 milliard", "anton", 80, YELLOW, "mm", a_in(t, 261.93))

def s_final_quote(img, t):
    T(img, 960, 440, "Le jeu se vend une fois.", "anton", 120, WHITE, "mm", a_in(t, 276.14, .4), shadow=True)
    T(img, 960, 600, "L'en ligne se vend tous les jours.", "anton", 120, GREEN, "mm", a_in(t, 277.98, .4), shadow=True)

_mc_thumb = None
def s_outro(img, t, logo):
    global _mc_thumb
    a = a_in(t, 281.63)
    paste(img, logo, 960 - logo.width / 2, 120, a)
    T(img, 960, 420, "L'ENVERS DU BUSINESS", "anton", 96, WHITE, "mm", a)
    if t >= 285.55:
        s = back(prog(t, 285.55, .35))
        rrect(img, (960 - 230 * s, 520 - 50 * s, 960 + 230 * s, 520 + 50 * s), 50 * s, RED, 1)
        T(img, 960, 522, "S'ABONNER", "anton", 56, WHITE, "mm", 1, scale=max(.01, s))
    if t >= 286.59:
        if _mc_thumb is None:
            _mc_thumb = Image.open(os.path.join(HERE, "../../mcdonalds/miniature.png")).convert("RGBA").resize((512, 288), Image.LANCZOS)
        a2 = a_in(t, 286.59, .4)
        T(img, 960, 640, "Mardi : comment McDonald's gagne son argent", "semi", 40, GREY, "mm", a2)
        rrect(img, (700, 690, 1220, 986), 14, YELLOW, a2)
        paste(img, _mc_thumb, 704, 694, a2)
