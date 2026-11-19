# Scènes de la vidéo « Black Friday : qui gagne VRAIMENT de l'argent ? »
# Tous les temps sont ceux de la voix off (secondes), relevés mot par mot (words.json).
import math, random
import numpy as np
from PIL import Image, ImageDraw
from gfx import *

# ---------- fond animé ----------
_yy, _xx = np.mgrid[0:H + 120, 0:W + 120]
def _bg(col, k):
    base = np.array(BG, float)
    g = np.clip(1 - np.hypot(_xx - (W + 120) / 2, _yy - (H + 120) * .45) / 1250, 0, 1) ** 2 * k
    a = base + g[..., None] * (np.array(col, float) - base)
    v = np.hypot((_xx - (W + 120) / 2) / W, (_yy - (H + 120) / 2) / H)
    a *= np.clip(1.12 - v * .75, .55, 1)[..., None]
    grid = ((_xx % 80) == 0) | ((_yy % 80) == 0)
    a[grid] += 7
    return np.clip(a, 0, 255).astype(np.uint8)
BGS = {k: _bg(c, s) for k, c, s in [("n", (40, 40, 58), .9), ("r", (110, 18, 14), .9), ("y", (95, 76, 0), .8),
                                      ("g", (10, 80, 45), .8), ("s", (70, 52, 28), .9)]}
def background(t, kind="n"):
    o = int(60 + 40 * math.sin(t * .05)), int(60 + 40 * math.cos(t * .043))
    return Image.fromarray(BGS[kind][o[1]:o[1] + H, o[0]:o[0] + W])

def a_in(t, t0, d=.4): return eo(prog(t, t0, d))
def dy_in(t, t0, d=.45, dist=40): return (1 - eo(prog(t, t0, d))) * dist

def header(img, t, t0, s, color=GREY):
    a = a_in(t, t0)
    T(img, 120, 110, s, "bold", 38, color, "lm", a, dy=dy_in(t, t0, dist=20))
    shape(img, (120, 140, 120 + 70 * a, 146), lambda d, ox, oy, w, h: d.rectangle((ox, oy, ox + w, oy + h), fill=YELLOW + (255,)), a)

def source(img, t, t0, s):
    T(img, 120, 1010, "Source : " + s, "med", 26, DIM, "lm", a_in(t, t0 + .3, .6))

# ---------- scènes ----------
def s_tag_intro(img, t):
    p = back(prog(t, 0.0, .55))
    cy = lerp(-250, 470, p)
    lay = price_tag(780, 380, "399,95 €", size=170, strike=eo(prog(t, 1.15, .35)), strike_color=RED)
    rotate_paste(img, lay, 960, cy, angle=4 * (1 - p) + 3)
    if t >= 1.2:
        s = back(prog(t, 1.2, .4), 2.6)
        shape(img, (1235 - 130 * s, 250 - 130 * s, 1235 + 130 * s, 250 + 130 * s),
              lambda d, ox, oy, w, h: d.ellipse((ox, oy, ox + w, oy + h), fill=RED + (255,)))
        T(img, 1235, 252, "-35 %", "anton", 92, WHITE, "mm", 1, scale=max(.01, s))
    a = a_in(t, 2.45)
    rrect(img, (960 - 230, 760 + dy_in(t, 2.45), 960 + 230, 840 + dy_in(t, 2.45)), 12, (250, 250, 250), a)
    T(img, 960, 800, "BLACK FRIDAY", "anton", 58, (12, 12, 16), "mm", a, dy=dy_in(t, 2.45))
    T(img, 960, 945, "UNE AFFAIRE ?", "anton", 96, YELLOW, "mm", a_in(t, 3.36, .3), shadow=True, scale=lerp(1.25, 1, eo(prog(t, 3.36, .3))))

def price_chart(img, t, pts, t_axes, title, labels_extra=None, src=None, src_t=None, illustrative=True):
    """Courbe de prix : pts = [(mois, prix, t_apparition, couleur, étiquette)]."""
    X0, X1, Y0, Y1 = 260, 1660, 300, 860
    lo, hi = 180, 460
    def py(v): return Y1 - (v - lo) / (hi - lo) * (Y1 - Y0)
    a = a_in(t, t_axes)
    header(img, t, t_axes, title)
    for v in (200, 300, 400):
        shape(img, (X0, py(v) - 1, X1, py(v) + 1), lambda d, ox, oy, w, h: d.rectangle((ox, oy, ox + w, oy + h), fill=LINE + (255,)), a)
        T(img, X0 - 20, py(v), f"{v} €", "med", 26, DIM, "rm", a)
    n = len(pts)
    xs = [lerp(X0 + 120, X1 - 120, i / (n - 1)) for i in range(n)]
    for i, (m, v, ti, col, lab) in enumerate(pts):
        T(img, xs[i], Y1 + 45, m, "semi", 32, GREY, "mt", a)
    # segments
    for i in range(1, n):
        ti = pts[i][2]
        p = eio(prog(t, ti - .5, .5))
        if p <= 0: continue
        x0, y0 = xs[i - 1], py(pts[i - 1][1]); x1, y1 = xs[i], py(pts[i][1])
        col = pts[i][3]
        strike_line(img, x0, y0, x0 + (x1 - x0), y0 + (y1 - y0), p, col, 10)
    for i, (m, v, ti, col, lab) in enumerate(pts):
        s = back(prog(t, ti, .35))
        if s <= 0: continue
        x, y = xs[i], py(v)
        glow(img, (x - 40, y - 40, x + 40, y + 40), 40, col, .5 * min(1, s), 18)
        shape(img, (x - 16 * s, y - 16 * s, x + 16 * s, y + 16 * s), lambda d, ox, oy, w, h, c=col: d.ellipse((ox, oy, ox + w, oy + h), fill=c + (255,)))
        chip(img, x, y - 70, lab, a_in(t, ti, .3), fill=col, color=(12, 12, 16) if col != RED else WHITE, size=40, kind="xbold", dy=dy_in(t, ti, dist=20))
    if labels_extra: labels_extra(img, t, xs, py)
    if src: source(img, t, src_t if src_t is not None else t_axes, src)

def s_chart_intro(img, t):
    def extra(img, t, xs, py):
        a = a_in(t, 11.0, .5)
        y = py(259)
        x = xs[0]
        while x < xs[-1]:
            shape(img, (x, y - 2, x + 22, y + 2), lambda d, ox, oy, w, h: d.rectangle((ox, oy, ox + w, oy + h), fill=GREEN + (255,)), a * .9)
            x += 40
        T(img, xs[-1] + 40, y + 50, "= prix de juillet", "bold", 34, GREEN, "rm", a)
    price_chart(img, t, [("Juillet", 259, 4.92, GREEN, "259 €"),
                         ("Septembre", 399.95, 9.5, RED, "399,95 €"), ("Black Friday", 259.97, 10.75, YELLOW, "« -35 % » = 260 €")],
                4.5, "LE PRIX DE CE CASQUE AU FIL DES MOIS", extra, "relevé UFC-Que Choisir (2025) · remise de 35 % à titre d'illustration", 4.6)

def s_one_in_three(img, t):
    T(img, 960, 300, "1 PROMO SUR 3", "anton", 230, WHITE, "mm", a_in(t, 13.88, .3), shadow=True, scale=lerp(1.3, 1, eo(prog(t, 13.88, .35))))
    for i in range(3):
        ti = 14.2 + i * .25
        s = back(prog(t, ti, .35))
        bad = i == 2 and t >= 15.15
        lay = price_tag(300, 150, "PROMO", color=(RED if bad else (250, 250, 250)), text_color=(WHITE if bad else (18, 18, 22)), size=64)
        rotate_paste(img, lay, 560 + i * 400, 620, angle=-6 + i * 3, alpha=min(1, s * 1.5), scale=max(.01, s))
        if bad:
            p = eo(prog(t, 15.15, .3))
            strike_line(img, 560 + 800 - 150, 545, 560 + 800 + 150, 700, p, (255, 255, 255), 14)
    T(img, 960, 820, "ne respecte pas les règles d'affichage des prix", "semi", 50, GREY, "mm", a_in(t, 15.6), dy=dy_in(t, 15.6))
    source(img, t, 13.9, "Commission européenne et autorités nationales (2026), via UFC-Que Choisir")

def s_question(img, t):
    T(img, 960, 200, "UNE SEULE QUESTION", "bold", 40, YELLOW, "mm", a_in(t, 19.76) * (1 - a_in(t, 20.9)), dy=dy_in(t, 19.76))
    T(img, 960, 330, "PENDANT LE BLACK FRIDAY…", "bold", 54, GREY, "mm", a_in(t, 20.99), dy=dy_in(t, 20.99))
    T(img, 960, 480, "QUI GAGNE VRAIMENT", "anton", 170, WHITE, "mm", a_in(t, 22.32, .3), shadow=True, dy=dy_in(t, 22.32, dist=60))
    T(img, 960, 660, "DE L'ARGENT ?", "anton", 170, YELLOW, "mm", a_in(t, 23.28, .3), shadow=True, dy=dy_in(t, 23.28, dist=60))
    T(img, 960, 850, "… et est-ce que c'est toi ?", "semi", 56, RED, "mm", a_in(t, 24.93), dy=dy_in(t, 24.93))

def s_philly(img, t):
    t0 = 26.71
    a = a_in(t, t0, .6)
    rrect(img, (360, 200, 1560, 860), 18, (58, 44, 28), a)
    rrect(img, (380, 220, 1540, 840), 12, (40, 30, 20), a)
    random.seed(3)
    for _ in range(14):  # rues stylisées
        x = random.randint(420, 1500)
        shape(img, (x, 240, x + 3, 820), lambda d, ox, oy, w, h: d.rectangle((ox, oy, ox + w, oy + h), fill=(70, 55, 36, 255)), a)
    for _ in range(8):
        y = random.randint(260, 800)
        shape(img, (400, y, 1520, y + 3), lambda d, ox, oy, w, h: d.rectangle((ox, oy, ox + w, oy + h), fill=(70, 55, 36, 255)), a)
    n = int(clamp((t - 28.4) / .9) * 12)
    T(img, 960, 480, "PHILADELPHIE"[:n], "anton", 170, (240, 222, 190), "mm", 1 if n else 0, shadow=True)
    T(img, 960, 640, "ÉTATS-UNIS · DÉBUT DES ANNÉES 1960", "bold", 46, (200, 170, 120), "mm", a_in(t, 29.5), dy=dy_in(t, 29.5))
    p = eo(prog(t, 28.47, .5))
    if p > 0:
        py_ = lerp(120, 330, p)
        shape(img, (1400, py_ - 60, 1460, py_ + 20), lambda d, ox, oy, w, h: (d.ellipse((ox, oy, ox + w, oy + w), fill=RED + (255,)),
              d.polygon([(ox + 6, oy + w * .7), (ox + w - 6, oy + w * .7), (ox + w / 2, oy + h)], fill=RED + (255,)),
              d.ellipse((ox + 20, oy + 20, ox + w - 20, oy + w - 20), fill=(40, 30, 20, 255))))

_crowd = [(random.Random(i).uniform(-1, 1), random.Random(i * 7 + 1).uniform(0, 1), random.Random(i * 13 + 5).uniform(.6, 1.4)) for i in range(220)]
def s_crowd(img, t):
    t0 = 31.48
    header(img, t, t0, "LE LENDEMAIN DE THANKSGIVING")
    rrect(img, (200, 330, 1200, 900), 20, (22, 22, 30), a_in(t, t0))
    T(img, 700, 370, "CENTRE-VILLE", "bold", 30, DIM, "mm", a_in(t, t0))
    dens = clamp((t - 33.9) / 6)
    for i, (sx, sy, sp) in enumerate(_crowd):
        if i / len(_crowd) > dens: break
        ph = (t * .15 * sp + sy) % 1
        x = 700 + sx * 470 + math.sin(t * sp + i) * 8
        y = 410 + ((sy + t * .04 * sp) % 1) * 390
        c = [WHITE, YELLOW, GREY, (200, 120, 80)][i % 4]
        img.paste(c, (int(x) - 5, int(y) - 5, int(x) + 5, int(y) + 5))
    n_cars = int(clamp((t - 38.2) / 3) * 9)
    for k in range(n_cars):
        x = 250 + k * 105
        rrect(img, (x, 830, x + 90, 870), 10, [RED, BLUE, YELLOW][k % 3], 1)
    for i, (s, ti) in enumerate([("Embouteillages monstres", 38.23), ("Trottoirs bondés", 39.67), ("Vols à l'étalage", 41.03)]):
        chip(img, 1290, 440 + i * 140, s, a_in(t, ti, .3), fill=CARD, color=WHITE, size=44, kind="bold", anchor="lm", outline=(70, 70, 85), dy=dy_in(t, ti, dist=25))

def s_police(img, t):
    t0 = 42.47
    a = a_in(t, t0)
    cx, cy, R = 430, 520, 200
    pts = []
    for k in range(16):
        r = R if k % 2 == 0 else R * .62
        ang = -math.pi / 2 + k * math.pi / 8
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    shape(img, (cx - R, cy - R, cx + R, cy + R), lambda d, ox, oy, w, h: (d.polygon([(x - cx + R + ox, y - cy + R + oy) for x, y in pts], fill=(200, 170, 60, 255)),
          d.ellipse((ox + R * .55, oy + R * .55, ox + R * 1.45, oy + R * 1.45), fill=(30, 40, 70, 255))), a)
    T(img, cx, cy, "POLICE", "anton", 52, (230, 210, 140), "mm", a)
    T(img, 1250, 380, "LE PIRE JOUR DE L'ANNÉE", "anton", 84, WHITE, "mm", a_in(t, 44.39), dy=dy_in(t, 44.39))
    T(img, 1250, 480, "Aucun congé possible", "semi", 50, RED, "mm", a_in(t, 45.83), dy=dy_in(t, 45.83))
    s = prog(t, 49.67, .28)
    if s > 0:
        stamp(img, 1250, 690, "BLACK FRIDAY", RED, 130, -6, min(1, s * 2), scale=lerp(1.8, 1, eo(s)))
    T(img, 1250, 860, "« le vendredi noir »", "semi", 46, GREY, "mm", a_in(t, 51.03), dy=dy_in(t, 51.03))

def s_big_friday(img, t):
    t0 = 52.79
    T(img, 960, 260, "Les commerçants détestent ce nom", "semi", 54, GREY, "mm", a_in(t, t0), dy=dy_in(t, t0))
    p_in = back(prog(t, 56.89, .4))
    fall = eio(prog(t, 58.07, .9))
    if p_in > 0:
        lay = Image.new("RGBA", (1100, 300), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((550, 150), "BIG FRIDAY", font=font("anton", 220), fill=YELLOW, anchor="mm")
        shake = math.sin(t * 60) * 10 * (1 - fall) if t > 58.0 else 0
        rotate_paste(img, lay, 960 + shake, 540 + fall * 650, angle=-fall * 25, alpha=1 - fall * .9, scale=max(.01, p_in))
    if t >= 58.07:
        stamp(img, 960, 560, "ÉCHEC TOTAL", RED, 150, -8, a_in(t, 58.07, .2), scale=lerp(1.6, 1, eo(prog(t, 58.07, .25))))

def s_ledger(img, t):
    t0 = 59.7
    header(img, t, t0, "UNE AUTRE EXPLICATION, PLUS FLATTEUSE")
    a = a_in(t, t0)
    rrect(img, (560, 230, 1360, 780), 16, (238, 232, 218), a)
    for i in range(7):
        y = 300 + i * 66
        shape(img, (600, y + 40, 1320, y + 42), lambda d, ox, oy, w, h: d.rectangle((ox, oy, ox + w, oy + h), fill=(200, 190, 170, 255)), a)
    turn = eo(prog(t, 66.1, .6))
    rows = [("Janvier → octobre", "- 18 000 €", RED, 0), ("Novembre", "- 4 000 €", RED, 0), ("Black Friday", "+ 9 500 €", (20, 20, 24), 1),
            ("Décembre", "+ 21 000 €", (20, 20, 24), 1)]
    for i, (lab, v, col, late) in enumerate(rows):
        y = 300 + i * 90
        aa = a_in(t, 61.0 + i * .2) if not late else a_in(t, 66.1 + (i - 2) * .3)
        T(img, 620, y + 20, lab, "semi", 38, (110, 100, 90), "lm", aa)
        T(img, 1300, y + 20, v, "xbold", 42, col, "rm", aa)
        shape(img, (600, y + 55, 1320, y + 57), lambda d, ox, oy, w, h: d.rectangle((ox, oy, ox + w, oy + h), fill=(200, 190, 170, 255)), a)
    T(img, 620, 690, "SOLDE", "anton", 50, (60, 50, 40), "lm", a)
    T(img, 1300, 690, "+ 8 500 €" if turn > .5 else "- 22 000 €", "anton", 64, mix(RED, (20, 20, 24), turn), "rm", a)
    T(img, 960, 760, "chiffres fictifs, pour illustrer", "med", 24, (120, 110, 100), "mm", a)
    T(img, 960, 860, "« passer dans le noir » = faire du bénéfice", "bold", 50, WHITE, "mm", a_in(t, 67.19), dy=dy_in(t, 67.19))
    T(img, 1540, 330, "Joli…", "semi", 54, GREY, "mm", a_in(t, 69.23))
    if t >= 70.07:
        stamp(img, 960, 520, "INVENTÉ BIEN APRÈS", RED, 110, -7, a_in(t, 70.07, .2), scale=lerp(1.6, 1, eo(prog(t, 70.07, .25))))

def s_atlantic(img, t):
    t0 = 72.74
    a = a_in(t, t0)
    L, R_ = (420, 560), (1500, 560)
    for (x, y), lab, ti in [(L, "ÉTATS-UNIS", t0), (R_, "FRANCE", 77.03)]:
        s = back(prog(t, ti, .4))
        pul = 1 + .15 * math.sin(t * 4) if t > ti + .4 else 1
        glow(img, (x - 70, y - 70, x + 70, y + 70), 70, YELLOW if lab == "FRANCE" else RED, .45 * min(1, s), 25)
        shape(img, (x - 26 * s * pul, y - 26 * s * pul, x + 26 * s * pul, y + 26 * s * pul),
              lambda d, ox, oy, w, h, c=(YELLOW if lab == "FRANCE" else RED): d.ellipse((ox, oy, ox + w, oy + h), fill=c + (255,)))
        T(img, x, y + 80, lab, "anton", 64, WHITE, "mt", a_in(t, ti))
    for k in range(5):  # vagues
        y = 640 + k * 40
        shape(img, (760, y, 1160, y + 20), lambda d, ox, oy, w, h: d.arc((ox, oy, ox + w, oy + h * 2), 200, 340, fill=(50, 80, 120, 255), width=4), a * .8)
    T(img, 960, 860, "OCÉAN ATLANTIQUE", "bold", 30, (70, 100, 140), "mm", a)
    p = eio(prog(t, 75.43, 1.4))
    if p > 0:
        pts = []
        for i in range(int(60 * p) + 1):
            u = i / 60
            x = lerp(L[0], R_[0], u); y = L[1] - math.sin(u * math.pi) * 300
            pts.append((x, y))
        if len(pts) > 1:
            shape(img, (380, 200, 1540, 600), lambda d, ox, oy, w, h: d.line([(x - 380 + ox, y - 200 + oy) for x, y in pts], fill=YELLOW + (255,), width=8, joint="curve"))
    T(img, 960, 160, "Avec Internet, le Black Friday traverse l'Atlantique", "semi", 48, GREY, "mm", a_in(t, 73.27), dy=dy_in(t, 73.27))
    T(img, 1500, 760, "la grande majorité des consommateurs", "semi", 38, YELLOW, "mm", a_in(t, 78.5))
    T(img, 1500, 810, "déclarent y participer", "semi", 38, YELLOW, "mm", a_in(t, 79.6))

def counter(img, t, t0, t1, v, unit, y=520, dec=1, size=260, color=WHITE):
    p = eio(prog(t, t0, t1 - t0))
    T(img, 960, y, fmt(v * p, dec), "anton", size, color, "mm", a_in(t, t0, .2), shadow=True)
    T(img, 960, y + size * .8, unit, "anton", 80, YELLOW, "mm", a_in(t, t0 + .2, .3))

def s_usa_counter(img, t):
    header(img, t, 83.09, "COMBIEN D'ARGENT CIRCULE ?")
    chip(img, 960, 250, "ÉTATS-UNIS · BLACK FRIDAY 2025 · EN LIGNE", a_in(t, 86.29), fill=CARD, color=GREY, size=36, outline=(70, 70, 85))
    counter(img, t, 90.13, 91.9, 11.8, "MILLIARDS DE DOLLARS", 500)
    T(img, 960, 800, "en une seule journée", "semi", 50, GREY, "mm", a_in(t, 92.81), dy=dy_in(t, 92.81))
    if t >= 94.77:
        stamp(img, 1500, 380, "RECORD", GREEN, 90, 8, a_in(t, 94.77, .2), scale=lerp(1.6, 1, eo(prog(t, 94.77, .25))))
    source(img, t, 90.1, "Adobe Analytics, 2025")

def s_bars(img, t):
    header(img, t, 96.91, "ÉTATS-UNIS · ACHATS EN LIGNE 2025 (MILLIARDS $)")
    items = [("Black Friday", 11.8, 96.95, GREY), ("Cyber Monday", 14.25, 98.39, YELLOW), ("Cyber Week (5 jours)", 44.2, 102.81, RED)]
    base_y, maxh = 870, 560
    for i, (lab, v, ti, col) in enumerate(items):
        x = 480 + i * 480
        p = eio(prog(t, ti, .9))
        h = maxh * v / 44.2 * p
        if p > 0:
            rrect(img, (x - 130, base_y - h, x + 130, base_y), 14, col, 1)
            T(img, x, base_y - h - 50, fmt(v * p, 2 if v == 14.25 else 1), "anton", 84, WHITE, "mm", a_in(t, ti, .2))
        T(img, x, base_y + 50, lab, "bold", 38, GREY, "mm", a_in(t, ti, .3))
    source(img, t, 96.95, "Adobe Analytics, 2025")

def s_france(img, t):
    header(img, t, 107.01, "EN FRANCE")
    counter(img, t, 109.37, 110.9, 196.4, "MILLIARDS D'EUROS", 400, dec=1, size=230)
    T(img, 960, 690, "vendus en ligne sur l'année 2025", "semi", 48, GREY, "mm", a_in(t, 110.5), dy=dy_in(t, 110.5))
    months = ["JAN", "FÉV", "MAR", "AVR", "MAI", "JUIN", "JUIL", "AOÛT", "SEPT", "OCT", "NOV", "DÉC"]
    a = a_in(t, 112.21)
    for i, m in enumerate(months):
        x = 300 + i * 120
        hot = i == 10 and t >= 112.6
        rrect(img, (x - 52, 790, x + 52, 870), 12, RED if hot else CARD, a, outline=None)
        T(img, x, 830, m, "bold", 30, WHITE if hot else GREY, "mm", a)
    T(img, 300 + 10 * 120, 925, "un des pics de l'année", "bold", 36, RED, "mm", a_in(t, 114.45))
    source(img, t, 109.4, "Fevad, bilan du e-commerce 2025")

def s_but(img, t):
    if t < 118.4:
        T(img, 960, 540, "MAIS…", "anton", 260, YELLOW, "mm", a_in(t, 116.29, .25), shadow=True, scale=lerp(1.3, 1, eo(prog(t, 116.29, .3))))
        return
    header(img, t, 118.45, "BLACK FRIDAY 2025 EN FRANCE")
    for i, (lab, v, ti, col) in enumerate([("COMMANDES EN LIGNE", 3, 122.45, GREY), ("CHIFFRE D'AFFAIRES", 6, 126.61, GREEN)]):
        x = 560 + i * 800
        a = a_in(t, ti - .6)
        rrect(img, (x - 330, 330, x + 330, 780), 26, CARD, a)
        T(img, x, 410, lab, "bold", 40, GREY, "mm", a)
        p = eio(prog(t, ti, .7))
        T(img, x, 620, f"+{v * p:.0f} %" if p > 0 else "…", "anton", 220, col, "mm", a)
        if i == 0: T(img, x, 475, "environ", "semi", 36, GREY, "mm", a_in(t, ti))
        if i == 1: T(img, x, 475, "près de", "semi", 36, GREY, "mm", a_in(t, ti))
    source(img, t, 121.0, "Criteo, via l'AFP (2025)")

def s_basket(img, t):
    t0 = 129.89
    T(img, 960, 230, "ON N'ACHÈTE PAS BEAUCOUP PLUS…", "anton", 90, WHITE, "mm", a_in(t, 131.09), dy=dy_in(t, 131.09))
    T(img, 960, 350, "… ON DÉPENSE PLUS PAR COMMANDE", "anton", 90, YELLOW, "mm", a_in(t, 132.77), dy=dy_in(t, 132.77))
    s = lerp(.8, 1.25, eo(prog(t, 133.0, 1.6)))
    cx, cy = 960, 690
    w, h = 300 * s, 190 * s
    shape(img, (cx - w / 2 - 20, cy - h / 2 - 120 * s, cx + w / 2 + 20, cy + h / 2), lambda d, ox, oy, ww, hh: (
        d.arc((ox + ww * .25, oy, ox + ww * .75, oy + 230 * s), 180, 360, fill=WHITE + (255,), width=int(14 * s)),
        d.polygon([(ox, oy + 120 * s), (ox + ww, oy + 120 * s), (ox + ww - 40 * s, oy + hh), (ox + 40 * s, oy + hh)], fill=WHITE + (255,))), a_in(t, t0))
    n = int(clamp((t - 133.0) / 1.6) * 6)
    for k in range(n):
        T(img, cx - (n - 1) * 30 * s + k * 60 * s, cy + 10 * s, "€", "anton", 70 * s, RED, "mm", 1)
    T(img, 960, 960, "et c'est exactement ce que les marques cherchent", "semi", 44, GREY, "mm", a_in(t, 135.2))

def chapter(img, t, t0, small, big, sub=None, t_sub=None):
    T(img, 960, 400, small, "bold", 54, YELLOW, "mm", a_in(t, t0), dy=dy_in(t, t0))
    T(img, 960, 540, big, "anton", 200, WHITE, "mm", a_in(t, t0 + .25, .3), shadow=True, scale=lerp(1.25, 1, eo(prog(t, t0 + .25, .35))))
    w = tw(big, "anton", 200)
    shape(img, (960 - w / 2, 650, 960 - w / 2 + w * eo(prog(t, t0 + .45, .5)), 660), lambda d, ox, oy, ww, hh: d.rectangle((ox, oy, ox + ww, oy + hh), fill=YELLOW + (255,)))
    if sub: T(img, 960, 760, sub, "semi", 50, GREY, "mm", a_in(t, t_sub), dy=dy_in(t, t_sub))

def s_ch1(img, t):
    chapter(img, t, 139.56, "GAGNANT N°1", "LE MAGASIN", "3 techniques", 145.64)

def icon_device(img, cx, cy, kind, a, s=1.0):
    if kind == "Télé":
        rrect(img, (cx - 230 * s, cy - 140 * s, cx + 230 * s, cy + 130 * s), 16, (30, 30, 40), a, outline=WHITE + (255,), width=6)
        rrect(img, (cx - 60 * s, cy + 140 * s, cx + 60 * s, cy + 160 * s), 6, WHITE, a)
    elif kind == "Console":
        rrect(img, (cx - 210 * s, cy - 90 * s, cx + 210 * s, cy + 90 * s), 70, (30, 30, 40), a, outline=WHITE + (255,), width=6)
        T(img, cx - 110 * s, cy, "+", "anton", 120 * s, WHITE, "mm", a)
        for dx, dy in [(110, -30), (150, 10), (110, 50), (70, 10)]:
            shape(img, (cx + dx * s - 14, cy + dy * s - 14, cx + dx * s + 14, cy + dy * s + 14), lambda d, ox, oy, w, h: d.ellipse((ox, oy, ox + w, oy + h), fill=WHITE + (255,)), a)
    else:
        rrect(img, (cx - 95 * s, cy - 170 * s, cx + 95 * s, cy + 170 * s), 30, (30, 30, 40), a, outline=WHITE + (255,), width=6)

def s_loss_leader(img, t):
    header(img, t, 146.92, "TECHNIQUE 1 · LE PRODUIT D'APPEL", YELLOW)
    dev = "Télé"
    if t >= 156.04: dev = "Console"
    if t >= 156.92: dev = "Smartphone"
    left = t >= 163.42
    cx = lerp(960, 500, eio(prog(t, 163.42, .6)))
    icon_device(img, cx, 470, dev, a_in(t, 149.4))
    T(img, cx, 700, dev.upper(), "anton", 64, WHITE, "mm", a_in(t, 155.24))
    lay = price_tag(330, 140, "PROMO", color=RED, text_color=WHITE, size=66)
    rotate_paste(img, lay, cx + 230, 300, 8, a_in(t, 150.12))
    a = a_in(t, 151.92)
    rrect(img, (cx - 260, 790, cx + 260, 880), 45, CARD, a, outline=RED + (255,), width=4)
    T(img, cx, 835, "MARGE : MINUSCULE", "anton", 50, RED, "mm", a)
    if t >= 154.1 and t < 163.42:
        T(img, cx, 950, "parfois même à perte", "semi", 40, GREY, "mm", a_in(t, 154.1))
    if 160.0 <= t < 163.42:
        T(img, 1500, 470, "BUT :", "bold", 44, GREY, "mm", a_in(t, 161.0))
        T(img, 1500, 550, "TE FAIRE VENIR", "anton", 84, YELLOW, "mm", a_in(t, 161.72))
    for i, (s, ti) in enumerate([("Câble", 166.76), ("Support mural", 167.56), ("Extension de garantie", 168.33)]):
        y = 330 + i * 180
        a = a_in(t, ti, .35)
        x = 960 + dy_in(t, ti, dist=80)
        rrect(img, (x, y, x + 860, y + 130), 22, CARD, a)
        T(img, x + 40, y + 65, s, "bold", 44, WHITE, "lm", a)
        if t >= 171.52:
            chip(img, x + 830, y + 65, "MARGE ÉNORME", a_in(t, 171.52 + i * .15, .3), fill=GREEN, color=(10, 30, 20), size=30, kind="xbold", anchor="rm")

def s_rule(img, t):
    header(img, t, 173.66, "TECHNIQUE 2 · LE PRIX BARRÉ", YELLOW)
    a = a_in(t, 176.25)
    rrect(img, (260, 260, 1660, 720), 28, CARD, a)
    T(img, 960, 330, "LA RÈGLE EN EUROPE", "bold", 40, GREY, "mm", a)
    T(img, 960, 420, "Prix de référence d'une promo =", "semi", 52, WHITE, "mm", a_in(t, 178.16))
    T(img, 960, 500, "le prix le plus bas des 30 jours précédents", "xbold", 54, YELLOW, "mm", a_in(t, 180.44))
    rnd = random.Random(5)
    vals = [rnd.uniform(.35, 1) for _ in range(30)]; vals[18] = .22
    for i, v in enumerate(vals):
        x = 330 + i * 42
        p = prog(t, 181.68 + i * .02, .3)
        hgt = 110 * v * eo(p)
        col = GREEN if i == 18 else (70, 70, 88)
        if p > 0: img.paste(col, (int(x), int(690 - hgt), int(x + 30), 690))
    T(img, 960, 860, "… mais certains vendeurs jouent avec les règles", "semi", 50, RED, "mm", a_in(t, 183.72), dy=dy_in(t, 183.72))

def s_chart_ufc(img, t):
    def extra(img, t, xs, py):
        if t >= 199.64: chip(img, 1440, 215, "TECHNIQUEMENT LÉGAL", a_in(t, 199.64, .3), fill=GREEN, color=(10, 30, 20), size=40, kind="xbold")
        if t >= 200.94: chip(img, 1440, 305, "FRANCHEMENT TROMPEUR", a_in(t, 200.94, .3), fill=RED, color=WHITE, size=40, kind="xbold")
    price_chart(img, t, [("Juillet", 259, 191.56, GREEN, "259 €"), ("Septembre", 399.95, 194.56, RED, "≈ 400 €"),
                         ("Black Friday", 280, 197.96, YELLOW, "« ÉNORME RÉDUCTION »")],
                186.57, "UN CASQUE AUDIO RELEVÉ PAR L'UFC-QUE CHOISIR", extra, "UFC-Que Choisir, « Black Friday 2025 : encore des prix douteux »", 187.0)

def s_fake_ref(img, t):
    header(img, t, 203.04, "LES PRIX « DE RÉFÉRENCE »", YELLOW)
    for i, (lab, ti, y) in enumerate([("PRIX CONSEILLÉ", 204.04, 330), ("PRIX DE COMPARAISON", 205.6, 500)]):
        s = back(prog(t, ti, .4))
        lay = price_tag(560, 140, lab, color=(250, 250, 250), size=56, strike=eo(prog(t, ti + .5, .4)), strike_color=RED)
        rotate_paste(img, lay, 700 + i * 520, y + math.sin(t * 1.5 + i) * 10, -4 + i * 6, min(1, s * 1.5), max(.01, s))
    T(img, 960, 650, "jamais pratiqué nulle part ?", "semi", 50, GREY, "mm", a_in(t, 207.6), dy=dy_in(t, 207.6))
    a = a_in(t, 209.72)
    rrect(img, (360, 730, 1560, 960), 24, CARD, a)
    T(img, 420, 800, "Réduction affichée", "semi", 46, GREY, "lm", a)
    T(img, 1500, 800, "ÉNORME", "anton", 64, YELLOW, "rm", a)
    T(img, 420, 890, "Économie réelle", "semi", 46, GREY, "lm", a_in(t, 211.84))
    T(img, 1500, 890, "PRESQUE RIEN", "anton", 64, RED, "rm", a_in(t, 211.84))

def s_urgency(img, t):
    header(img, t, 214.57, "TECHNIQUE 3 · L'URGENCE", YELLOW)
    if t >= 217.0:
        rem = max(0, 3 * 3600 - 1 - (t - 217.0))
        hh, mm, ss = int(rem // 3600), int(rem % 3600 // 60), int(rem % 60)
        a = a_in(t, 217.0, .3)
        rrect(img, (220, 330, 1000, 560), 26, (60, 12, 10), a)
        T(img, 610, 445, f"{hh:02d}:{mm:02d}:{ss:02d}", "anton", 170, RED, "mm", a)
        T(img, 610, 610, "L'OFFRE SE TERMINE DANS…", "bold", 36, GREY, "mm", a)
    for i, (s, ti) in enumerate([("Plus que 3 en stock !", 218.16), ("40 personnes regardent ce produit", 219.54)]):
        a = a_in(t, ti, .3)
        x = 1060 + (1 - eo(prog(t, ti, .4))) * 400
        y = 360 + i * 170
        rrect(img, (x, y, x + 780, y + 130), 22, (250, 250, 250), a)
        shape(img, (x + 30, y + 40, x + 80, y + 90), lambda d, ox, oy, w, h: d.ellipse((ox, oy, ox + w, oy + h), fill=RED + (255,)), a)
        T(img, x + 105, y + 65, s, "bold", 34, (20, 20, 24), "lm", a)
    if t >= 221.7:
        T(img, 960, 780, "Tout est fait pour t'empêcher de…", "semi", 46, GREY, "mm", a_in(t, 221.7))
        s = a_in(t, 225.4, .3)
        T(img, 960, 900, "COMPARER", "anton", 120, YELLOW, "mm", s)
        w = tw("COMPARER", "anton", 120)
        strike_line(img, 960 - w / 2 - 20, 905, 960 + w / 2 + 20, 895, eo(prog(t, 226.0, .3)), RED, 16)
    if t >= 226.6:
        # fondu vers le message sur le cerveau
        a = a_in(t, 226.6, .4)
        rrect(img, (0, 0, W, H), 0, BG, a * .97)
        T(img, 960, 450, "Notre cerveau déteste", "anton", 110, WHITE, "mm", a)
        T(img, 960, 580, "RATER UNE OCCASION", "anton", 130, YELLOW, "mm", a_in(t, 228.24))
        T(img, 960, 760, "Les marques le savent… et l'exploitent à fond.", "semi", 48, GREY, "mm", a_in(t, 229.56))

def card_icon(img, cx, cy, w, h, a, angle=0, col=(40, 70, 160)):
    lay = Image.new("RGBA", (int(w) + 10, int(h) + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((5, 5, 5 + w, 5 + h), int(h * .1), fill=col)
    d.rounded_rectangle((5 + w * .08, 5 + h * .3, 5 + w * .25, 5 + h * .52), 6, fill=(220, 190, 90))
    d.text((5 + w * .08, 5 + h * .75), "•••• •••• •••• 2026", font=font("semi", int(h * .1)), fill=(230, 230, 240))
    rotate_paste(img, lay, cx, cy, angle, a)

def s_ch2(img, t):
    if t < 239.3:
        chapter(img, t, 233.76, "GAGNANT N°2", "PAYER PLUS TARD")
        return
    T(img, 960, 220, "« Paiement en 3 ou 4 fois »", "anton", 90, WHITE, "mm", a_in(t, 239.3))
    p = eio(prog(t, 239.9, .7))
    for k in range(4):
        cx = 960 + (k - 1.5) * lerp(0, 330, p)
        T(img, cx, 800, f"{k + 1}/4", "anton", 70, YELLOW, "mm", p)
        lay_w = 640 / 4
        # chaque morceau = une part de la carte
        x0 = 960 - 320 + k * lay_w
        part = Image.new("RGBA", (int(lay_w), 400), (0, 0, 0, 0))
        d = ImageDraw.Draw(part)
        d.rounded_rectangle((-k * lay_w, 0, -k * lay_w + 640, 400), 40, fill=(40, 70, 160))
        d.rounded_rectangle((-k * lay_w + 50, 120, -k * lay_w + 160, 210), 10, fill=(220, 190, 90))
        paste(img, part, x0 + (cx - (x0 + lay_w / 2)), 340 + math.sin(k) * 20 * p)

def s_bnpl(img, t):
    header(img, t, 241.63, "ÉTATS-UNIS · CYBER MONDAY 2025")
    T(img, 960, 470, "+ 1 MILLIARD $", "anton", 230, YELLOW, "mm", a_in(t, 245.32, .3), shadow=True, scale=lerp(1.3, 1, eo(prog(t, 245.32, .35))))
    T(img, 960, 660, "d'achats payés en plusieurs fois", "semi", 54, WHITE, "mm", a_in(t, 246.59), dy=dy_in(t, 246.59))
    T(img, 960, 740, "en une seule journée", "semi", 44, GREY, "mm", a_in(t, 247.68))
    source(img, t, 245.3, "Adobe Analytics, Cyber Monday 2025")

def s_balance(img, t):
    header(img, t, 249.47, "POURQUOI ÇA MARCHE ?")
    tilt = eio(prog(t, 254.46, .9)) * 7
    cx, cy = 960, 420
    a = a_in(t, 249.6)
    rrect(img, (cx - 12, cy, cx + 12, 820), 6, GREY, a)
    rrect(img, (cx - 140, 810, cx + 140, 840), 10, GREY, a)
    ang = math.radians(tilt)
    lx, ly = cx - 480 * math.cos(ang), cy + 480 * math.sin(ang)
    rx, ry = cx + 480 * math.cos(ang), cy - 480 * math.sin(ang)
    strike_line(img, lx, ly, rx, ry, 1 if a > 0 else 0, GREY, 14, a)
    for (px, py_), lab, ti, col in [((lx, ly), "400 €", 251.74, RED), ((rx, ry), "4 × 100 €", 254.46, GREEN)]:
        strike_line(img, px, py_, px, py_ + 160, 1, (110, 110, 120), 4, a)
        rrect(img, (px - 190, py_ + 160, px + 190, py_ + 190), 12, (110, 110, 120), a)
        aa = a_in(t, ti, .3)
        if lab == "400 €":
            rrect(img, (px - 150, py_ + 40, px + 150, py_ + 160), 16, col, aa)
        else:
            for k in range(4):
                rrect(img, (px - 160 + k * 82, py_ + 100, px - 160 + k * 82 + 70, py_ + 160), 10, col, aa)
        T(img, px, py_ + 250, lab, "anton", 90, col, "mm", aa)
    T(img, 960, 960, "Même produit · la « douleur » de payer est découpée", "semi", 46, YELLOW, "mm", a_in(t, 255.96))

def s_who_paid(img, t):
    header(img, t, 260.0, "LES SOCIÉTÉS DE PAIEMENT SONT PAYÉES…")
    rows = [("PAR LE COMMERÇANT", "qui sait que tu achèteras plus", 262.84, YELLOW),
            ("PARFOIS PAR TOI", "si tu paies en retard", 265.84, RED)]
    for i, (a_, b_, ti, col) in enumerate(rows):
        y = 380 + i * 260
        a = a_in(t, ti, .35)
        x = 260 + dy_in(t, ti, dist=80)
        rrect(img, (x, y, x + 1400, y + 200), 26, CARD, a)
        shape(img, (x + 40, y + 60, x + 120, y + 140), lambda d, ox, oy, w, h, c=col: d.ellipse((ox, oy, ox + w, oy + h), fill=c + (255,)), a)
        T(img, x + 80, y + 100, "€", "anton", 60, (12, 12, 16), "mm", a)
        T(img, x + 170, y + 75, a_, "anton", 70, WHITE, "lm", a)
        T(img, x + 170, y + 145, b_, "semi", 42, GREY, "lm", a)

def s_ch3(img, t):
    chapter(img, t, 269.17, "GAGNANT N°3", "LES PLATEFORMES")
    for i, (lab, ti) in enumerate([("Places de marché", 272.17), ("Moteurs de recherche", 273.53), ("Réseaux sociaux", 274.85)]):
        chip(img, 520 + i * 440, 820, lab, a_in(t, ti, .3), fill=CARD, color=WHITE, size=40, outline=(70, 70, 85), dy=dy_in(t, ti, dist=25))

def s_ads(img, t):
    header(img, t, 276.21, "TOUT LE MONDE VEUT ÊTRE VISIBLE")
    X0, X1, Y0, Y1 = 260, 1180, 300, 820
    a = a_in(t, 276.3)
    strike_line(img, X0, Y1, X1, Y1, 1, LINE, 4, a)
    strike_line(img, X0, Y0, X0, Y1, 1, LINE, 4, a)
    T(img, X0, Y0 - 40, "Prix de la pub en ligne", "bold", 36, GREY, "lm", a)
    T(img, X1, Y1 + 40, "fin novembre →", "semi", 32, DIM, "rm", a)
    p = eio(prog(t, 280.29, 2.4))
    pts = []
    for i in range(int(40 * p) + 1):
        u = i / 40
        pts.append((lerp(X0, X1, u), Y1 - 60 - (u ** 2.6) * 420 - math.sin(u * 17) * 12))
    if len(pts) > 1:
        shape(img, (X0, Y0 - 20, X1 + 20, Y1), lambda d, ox, oy, w, h: d.line([(x - X0 + ox, y - Y0 + 20 + oy) for x, y in pts], fill=RED + (255,), width=10, joint="curve"))
    # pièces qui tombent dans la poche des plateformes
    a2 = a_in(t, 283.63)
    rrect(img, (1340, 560, 1700, 840), 30, CARD, a2, outline=YELLOW + (255,), width=5)
    T(img, 1520, 700, "PLATEFORMES", "anton", 56, YELLOW, "mm", a2)
    if t >= 284.0:
        for k in range(8):
            ph = ((t - 284.0) * .9 + k / 8) % 1
            x = 1520 + math.sin(k * 2.3) * 120
            y = lerp(220, 600, ph)
            T(img, x, y, "€", "anton", 60, YELLOW, "mm", (1 - ph) * a2)
    T(img, 1520, 920, "que tu achètes… ou non", "semi", 40, GREY, "mm", a_in(t, 286.91))

def s_data(img, t):
    header(img, t, 289.33, "LE DEUXIÈME TRÉSOR : TES DONNÉES", YELLOW)
    a = a_in(t, 289.6)
    rrect(img, (230, 260, 830, 900), 30, CARD, a)
    shape(img, (450, 310, 610, 470), lambda d, ox, oy, w, h: d.ellipse((ox, oy, ox + w, oy + h), fill=GREY + (255,)), a)
    shape(img, (370, 480, 690, 640), lambda d, ox, oy, w, h: d.pieslice((ox, oy, ox + w, oy + h * 2), 180, 360, fill=GREY + (255,)), a)
    T(img, 530, 700, "TOI", "anton", 64, WHITE, "mm", a)
    for i, (lab, ti) in enumerate([("Chaque clic", 293.17), ("Chaque recherche", 293.97), ("Chaque panier abandonné", 295.09)]):
        y = 330 + i * 120
        aa = a_in(t, ti, .3)
        x = 950 + dy_in(t, ti, dist=60)
        rrect(img, (x, y, x + 760, y + 90), 20, CARD, aa)
        T(img, x + 30, y + 45, "●", "bold", 30, GREEN, "lm", aa)
        T(img, x + 80, y + 45, lab, "bold", 42, WHITE, "lm", aa)
    T(img, 1330, 720, "→ pour mieux te cibler", "xbold", 50, YELLOW, "mm", a_in(t, 296.21))
    for i, (lab, ti) in enumerate([("Noël", 298.05), ("Soldes", 299.05), ("L'année suivante", 299.69)]):
        chip(img, 1030 + i * 250 + (i == 2) * 60, 840, lab, a_in(t, ti, .3), fill=RED, color=WHITE, size=38, kind="xbold")

def s_and_you(img, t):
    T(img, 960, 330, "ET TOI ?", "anton", 220, WHITE, "mm", a_in(t, 302.1, .3), shadow=True)
    T(img, 960, 500, "forcément perdant ?", "semi", 60, GREY, "mm", a_in(t, 303.18), dy=dy_in(t, 303.18))
    if t >= 305.46:
        stamp(img, 960, 650, "PAS FORCÉMENT", GREEN, 110, -4, a_in(t, 305.46, .2), scale=lerp(1.5, 1, eo(prog(t, 305.46, .25))))
    T(img, 960, 840, "Les vraies bonnes affaires profitent à ceux qui suivent", "semi", 46, GREY, "mm", a_in(t, 309.86))
    T(img, 960, 930, "3 RÈGLES", "anton", 90, YELLOW, "mm", a_in(t, 311.62))

def s_rules(img, t):
    header(img, t, 312.98, "LES 3 RÈGLES DU BLACK FRIDAY", YELLOW)
    rows = [("1", "Décide avant", "Fais ta liste, n'achète rien d'autre", 312.98, 315.38),
            ("2", "Vérifie l'historique des prix", "Prix monté juste avant la promo ? Passe ton chemin", 320.54, 323.38),
            ("3", "Ignore le compte à rebours", "Une vraie bonne offre attend 10 minutes", 331.14, 333.94)]
    for i, (n, a_, b_, ti, tb) in enumerate(rows):
        y = 260 + i * 230
        a = a_in(t, ti, .35)
        x = 220 + dy_in(t, ti, dist=80)
        rrect(img, (x, y, x + 1480, y + 190), 28, CARD, a)
        shape(img, (x + 40, y + 45, x + 140, y + 145), lambda d, ox, oy, w, h: d.ellipse((ox, oy, ox + w, oy + h), fill=YELLOW + (255,)), a)
        T(img, x + 90, y + 95, n, "anton", 66, (12, 12, 16), "mm", a)
        T(img, x + 190, y + 70, a_, "anton", 68, WHITE, "lm", a)
        T(img, x + 190, y + 140, b_, "semi", 40, GREY, "lm", a_in(t, tb, .35))
        if t >= tb + 1.5:
            s = back(prog(t, tb + 1.5, .3))
            T(img, x + 1400, y + 95, "✓", "black", 90, GREEN, "mm", min(1, s), scale=max(.01, s))

def s_joko(img, t):
    header(img, t, 340.79, "BLACK FRIDAY 2025 EN FRANCE · ÉTUDE JOKO")
    a = a_in(t, 341.0)
    rrect(img, (260, 260, 1660, 640), 30, CARD, a)
    T(img, 960, 380, "Beaucoup n'achètent pas plus…", "anton", 84, WHITE, "mm", a_in(t, 344.66))
    T(img, 960, 520, "… ils avancent leurs achats de Noël", "anton", 84, YELLOW, "mm", a_in(t, 346.9))
    T(img, 960, 760, "Achats prévus + vrais bons prix", "semi", 56, WHITE, "mm", a_in(t, 349.57), dy=dy_in(t, 349.57))
    if t >= 353.11:
        stamp(img, 960, 900, "TU FAIS PARTIE DES GAGNANTS", GREEN, 70, -3, a_in(t, 353.11, .2), scale=lerp(1.4, 1, eo(prog(t, 353.11, .25))))
    source(img, t, 341.0, "Étude Joko, Black Friday 2025")

def s_conclusion(img, t):
    T(img, 960, 300, "PAS UNE FÊTE DU CONSOMMATEUR", "anton", 100, GREY, "mm", a_in(t, 355.77), dy=dy_in(t, 355.77))
    T(img, 960, 470, "UNE OPÉRATION COMMERCIALE", "anton", 130, YELLOW, "mm", a_in(t, 358.97, .3), shadow=True, scale=lerp(1.25, 1, eo(prog(t, 358.97, .35))))
    for i, (lab, ti) in enumerate([("Dépenser plus", 362.05), ("plus vite", 363.29), ("en réfléchissant moins", 364.09)]):
        chip(img, 520 + i * 430 + (i == 2) * 40, 700, lab, a_in(t, ti, .3), fill=CARD, color=WHITE, size=44, outline=(70, 70, 85), dy=dy_in(t, ti, dist=25))

def s_recap(img, t):
    header(img, t, 365.61, "QUI GAGNE VRAIMENT ?")
    rows = [("LE MAGASIN", "grâce au panier complet", 365.61), ("LE CRÉDIT", "grâce au paiement découpé", 368.41), ("LES PLATEFORMES", "grâce à la pub et à tes données", 371.21)]
    for i, (a_, b_, ti) in enumerate(rows):
        y = 280 + i * 210
        a = a_in(t, ti, .35)
        x = 260 + dy_in(t, ti, dist=80)
        rrect(img, (x, y, x + 1400, y + 170), 26, CARD, a)
        T(img, x + 50, y + 85, a_, "anton", 76, WHITE, "lm", a)
        T(img, x + 1350, y + 85, b_, "semi", 46, YELLOW, "rm", a_in(t, ti + .8, .35))
    T(img, 960, 960, "Et toi ? Seulement si tu connais leurs règles du jeu.", "semi", 46, GREY, "mm", a_in(t, 374.54))

def s_quote(img, t):
    T(img, 960, 420, "Le meilleur prix,", "anton", 130, WHITE, "mm", a_in(t, 374.6, .4), shadow=True)
    T(img, 960, 580, "c'est celui que tu as vérifié.", "anton", 130, YELLOW, "mm", a_in(t, 375.5, .4), shadow=True)
    T(img, 960, 780, "Maintenant, tu connais leurs règles.", "semi", 50, GREY, "mm", a_in(t, 378.25))

def s_outro(img, t, logo):
    a = a_in(t, 380.09)
    paste(img, logo, 960 - logo.width / 2, 170, a)
    T(img, 960, 470, "L'ENVERS DU BUSINESS", "anton", 100, WHITE, "mm", a)
    T(img, 960, 560, "Comment les entreprises gagnent VRAIMENT leur argent", "semi", 40, GREY, "mm", a)
    if t >= 383.85:
        s = back(prog(t, 383.85, .35))
        rrect(img, (960 - 230 * s, 640 - 50 * s, 960 + 230 * s, 640 + 50 * s), 50 * s, RED, 1)
        T(img, 960, 642, "S'ABONNER", "anton", 56, WHITE, "mm", 1, scale=max(.01, s))
    a2 = a_in(t, 384.81, .4)
    rrect(img, (360, 760, 1560, 1000), 26, CARD, a2, outline=YELLOW + (255,), width=4)
    T(img, 420, 810, "PROCHAINE VIDÉO", "bold", 34, YELLOW, "lm", a2)
    T(img, 420, 880, "Comment McDonald's gagne VRAIMENT son argent", "anton", 54, WHITE, "lm", a_in(t, 387.0))
    T(img, 420, 950, "(indice : pas avec les burgers)", "semi", 36, GREY, "lm", a_in(t, 389.97))

def s_endcard(img, t, logo, t0):
    a = a_in(t, t0, .5)
    T(img, 960, 140, "MERCI D'AVOIR REGARDÉ !", "anton", 90, WHITE, "mm", a)
    # emplacements des éléments de fin YouTube (2 vidéos + abonnement)
    for i, lab in enumerate(["Vidéo suivante", "Vidéo conseillée"]):
        x = 150 + i * 620
        rrect(img, (x, 360, x + 560, 675), 18, CARD, a, outline=(70, 70, 85, 255), width=3)
        T(img, x + 280, 520, lab, "bold", 36, DIM, "mm", a)
    small = logo.resize((200, 200), Image.LANCZOS)
    paste(img, small, 1490, 420, a)
    T(img, 1590, 740, "Abonne-toi", "bold", 40, WHITE, "mm", a)
    T(img, 960, 940, "Sources dans la description", "med", 30, DIM, "mm", a)
