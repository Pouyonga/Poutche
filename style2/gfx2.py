# Style 2 de la chaîne : fonds colorés, caméra vivante, mascotte « Pièce », mots qui sautent, transitions balayées.
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../black_friday/video"))
from PIL import Image, ImageDraw, ImageFilter
from gfx import W, H, clamp, prog, eo, eio, back, lerp, mix, paste, T, tw, shape, rrect, chip, rotate_paste, strike_line, fmt, font

# ---------- palette style 2 ----------
INK = (24, 22, 38)          # texte principal (presque noir violacé)
PAPER = (255, 251, 240)     # blanc chaud
SUN = (255, 214, 10)        # jaune de la chaîne
SKY = (96, 190, 255)
CORAL = (255, 112, 96)
MINT = (80, 220, 160)
GRAPE = (130, 100, 255)
NIGHT = (22, 20, 40)        # réservé aux moments forts
RED2 = (235, 50, 60)
GREEN2 = (30, 170, 100)

BGS = {"sun": (SUN, (255, 232, 120)), "sky": (SKY, (170, 225, 255)), "coral": (CORAL, (255, 170, 150)),
       "mint": (MINT, (170, 245, 210)), "grape": (GRAPE, (185, 165, 255)), "night": (NIGHT, (60, 50, 110)), "paper": (PAPER, (255, 236, 200))}

def background(kind, t, w=W, h=H):
    """Fond uni + grosses formes douces qui dérivent lentement (jamais d'aplat immobile)."""
    base, soft = BGS[kind]
    img = Image.new("RGB", (w, h), base)
    d = ImageDraw.Draw(img)
    for i, (cx, cy, r, sp) in enumerate([(.15, .2, .28, .07), (.85, .75, .35, -.05), (.7, .1, .18, .09), (.3, .9, .22, -.08)]):
        x = (cx + .03 * math.sin(t * sp * 6 + i)) * w; y = (cy + .03 * math.cos(t * sp * 5 + i)) * h; rr = r * h
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=mix(base, soft, .55))
    # petits points en grille qui défilent
    off = (t * 18) % 60
    dot = mix(base, soft, .9)
    for yy in range(-60, h + 60, 60):
        for xx in range(-60, w + 60, 60):
            d.ellipse((xx + off - 3, yy + off * .5 - 3, xx + off + 3, yy + off * .5 + 3), fill=dot)
    return img

# ---------- caméra ----------
def camera(img, zoom=1.0, dx=0.0, dy=0.0, rot=0.0):
    """Zoom / déplacement / légère rotation autour du centre."""
    if abs(zoom - 1) < 1e-3 and abs(dx) < .5 and abs(dy) < .5 and abs(rot) < 1e-3: return img
    a = math.radians(rot); c, s = math.cos(a) / zoom, math.sin(a) / zoom
    cx, cy = W / 2, H / 2
    # transformation inverse : sortie -> source
    coeffs = (c, s, cx - c * cx - s * cy - dx * c - dy * s, -s, c, cy + s * cx - c * cy + dx * s - dy * c)
    return img.transform((W, H), Image.AFFINE, coeffs, resample=Image.BILINEAR)

def shake(t, t0, amp=14, dur=.35):
    p = prog(t, t0, dur)
    if p <= 0 or p >= 1: return 0, 0
    k = (1 - p) * amp
    return k * math.sin(t * 90), k * math.cos(t * 77)

# ---------- transitions balayées ----------
def swipe(img, t, t0, color, dur=.5, direction=1):
    """Une bande colorée inclinée traverse l'écran (à superposer au changement de scène)."""
    p = prog(t, t0 - dur / 2, dur)
    if p <= 0 or p >= 1: return
    x = lerp(-W * .8, W * 1.8, eio(p)) if direction > 0 else lerp(W * 1.8, -W * .8, eio(p))
    shape(img, (0, 0, W, H), lambda d, ox, oy, w, h: d.polygon([(x - 700 + ox, oy), (x + 200 + ox, oy), (x - 100 + ox, oy + h), (x - 1000 + ox, oy + h)], fill=color + (255,)))

# ---------- mots qui sautent ----------
def pop_word(img, x, y, word, t, t0, size=120, color=INK, bg=None, rot=-3, kind="anton"):
    """Mot qui apparaît en rebondissant, puis respire légèrement."""
    p = prog(t, t0, .35)
    if p <= 0: return
    s = back(p, 2.4) * (1 + .02 * math.sin((t - t0) * 4))
    f = font(kind, size)
    b = f.getbbox(word); w, h = b[2] - b[0], b[3] - b[1]
    pad = int(size * .35)
    lay = Image.new("RGBA", (w + 2 * pad, h + 2 * pad + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    if bg: d.rounded_rectangle((0, 0, lay.width - 1, lay.height - 11), int(size * .25), fill=bg)
    d.text((pad - b[0], pad - b[1]), word, font=f, fill=color)
    rotate_paste(img, lay, x, y, rot, min(1, p * 2), max(.02, s))

# ---------- mascotte « Pièce » ----------
def mascot(img, x, y, t, size=260, mood="neutre", look=(0, 0), wave=0.0, alpha=1.0, squash=0.0):
    """Pièce dorée avec visage. mood : neutre, surpris, content, clin, fache, triste."""
    S = size / 260
    L = Image.new("RGBA", (int(340 * S), int(340 * S)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    k = lambda *v: tuple(int(a * S) for a in v)
    cx, cy = 170, 170
    # bras
    if wave:
        ang = math.radians(-60 + 25 * math.sin(t * 10) * wave)
        hx, hy = cx + 140 * math.cos(ang), cy + 140 * math.sin(ang) - 10
        d.line([k(cx + 95, cy), k(hx, hy)], fill=INK, width=int(14 * S)); d.ellipse(k(hx - 18, hy - 18, hx + 18, hy + 18), fill=PAPER, outline=INK, width=int(6 * S))
    # corps
    d.ellipse(k(cx - 120, cy - 120, cx + 120, cy + 120), fill=(230, 160, 0), outline=INK, width=int(8 * S))
    d.ellipse(k(cx - 100, cy - 100, cx + 100, cy + 100), fill=SUN)
    d.arc(k(cx - 100, cy - 100, cx + 100, cy + 100), 200, 290, fill=(255, 240, 150), width=int(12 * S))
    # yeux (clignement toutes les ~3,2 s)
    blink = (t % 3.2) < .12
    lx, ly = look
    for ex in (-42, 42):
        wink = mood == "clin" and ex > 0
        if blink or wink:
            d.arc(k(cx + ex - 24, cy - 40, cx + ex + 24, cy), 200, 340, fill=INK, width=int(8 * S))
            continue
        ry = 34 if mood == "surpris" else 28
        d.ellipse(k(cx + ex - 24, cy - 30 - ry / 2, cx + ex + 24, cy - 30 + ry), fill=PAPER, outline=INK, width=int(6 * S))
        d.ellipse(k(cx + ex - 10 + lx * 8, cy - 20 + ly * 8, cx + ex + 10 + lx * 8, cy + ly * 8), fill=INK)
    # sourcils
    if mood in ("fache", "surpris", "triste"):
        for ex in (-42, 42):
            if mood == "fache": a, b = (cx + ex - 26, cy - 78 + (8 if ex < 0 else -8) * -1), (cx + ex + 26, cy - 78 + (8 if ex < 0 else -8))
            elif mood == "triste": a, b = (cx + ex - 26, cy - 70 + (-8 if ex < 0 else 8) * -1), (cx + ex + 26, cy - 70 + (-8 if ex < 0 else 8))
            else: a, b = (cx + ex - 22, cy - 88), (cx + ex + 22, cy - 92)
            d.line([k(*a), k(*b)], fill=INK, width=int(8 * S))
    # bouche
    if mood == "surpris": d.ellipse(k(cx - 20, cy + 30, cx + 20, cy + 75), fill=INK)
    elif mood in ("content", "clin"): d.chord(k(cx - 48, cy + 10, cx + 48, cy + 80), 0, 180, fill=INK)
    elif mood == "fache": d.arc(k(cx - 40, cy + 40, cx + 40, cy + 90), 200, 340, fill=INK, width=int(8 * S))
    elif mood == "triste": d.arc(k(cx - 36, cy + 45, cx + 36, cy + 95), 200, 340, fill=INK, width=int(8 * S))
    else: d.arc(k(cx - 36, cy + 20, cx + 36, cy + 66), 20, 160, fill=INK, width=int(8 * S))
    # joues
    for ex in (-70, 70): d.ellipse(k(cx + ex - 14, cy + 20, cx + ex + 14, cy + 36), fill=(255, 150, 120))
    bob = math.sin(t * 3) * 8 * S
    if squash:
        L = L.resize((int(L.width * (1 + squash)), int(L.height * (1 - squash))), Image.BICUBIC)
    paste(img, L, x - L.width / 2, y - L.height / 2 + bob, alpha)

# ---------- icônes plates (contour épais, style autocollant) ----------
def sticker(lay_fn, w, h, outline=6):
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); lay_fn(ImageDraw.Draw(L), w, h); return L

def icon_burger(w):
    def f(d, W_, H_):
        s = W_ / 300
        d.chord((10 * s, 10 * s, 290 * s, 170 * s), 180, 360, fill=(240, 160, 60), outline=INK, width=int(6 * s))
        d.rectangle((10 * s, 88 * s, 290 * s, 92 * s), fill=INK)
        d.rounded_rectangle((5 * s, 95 * s, 295 * s, 120 * s), int(10 * s), fill=(90, 200, 90), outline=INK, width=int(5 * s))
        d.rounded_rectangle((15 * s, 118 * s, 285 * s, 160 * s), int(18 * s), fill=(120, 62, 30), outline=INK, width=int(6 * s))
        d.rounded_rectangle((20 * s, 158 * s, 280 * s, 200 * s), int(18 * s), fill=(230, 150, 60), outline=INK, width=int(6 * s))
        for sx, sy in [(90, 45), (150, 35), (210, 50), (120, 70), (185, 72)]: d.ellipse(((sx - 7) * s, (sy - 4) * s, (sx + 7) * s, (sy + 4) * s), fill=PAPER)
    return sticker(f, w, int(w * 0.7))

def icon_fries(w):
    def f(d, W_, H_):
        s = W_ / 200
        for i in range(6):
            x = 40 + i * 22; d.rounded_rectangle((x * s, (10 + (i % 3) * 12) * s, (x + 16) * s, 150 * s), int(5 * s), fill=(255, 210, 60), outline=INK, width=int(4 * s))
        d.polygon([(25 * s, 90 * s), (175 * s, 90 * s), (155 * s, 250 * s), (45 * s, 250 * s)], fill=RED2, outline=INK, width=int(6 * s))
    return sticker(f, w, int(w * 1.3))

def icon_shake(w):
    def f(d, W_, H_):
        s = W_ / 200
        d.line((120 * s, 0, 100 * s, 70 * s), fill=CORAL, width=int(12 * s))
        d.chord((30 * s, 40 * s, 170 * s, 120 * s), 180, 360, fill=PAPER, outline=INK, width=int(5 * s))
        d.polygon([(30 * s, 80 * s), (170 * s, 80 * s), (150 * s, 260 * s), (50 * s, 260 * s)], fill=(255, 180, 200), outline=INK, width=int(6 * s))
        d.rectangle((48 * s, 140 * s, 152 * s, 170 * s), fill=PAPER)
    return sticker(f, w, int(w * 1.3))

def icon_building(w, lit=1.0):
    def f(d, W_, H_):
        s = W_ / 300
        d.rectangle((40 * s, 60 * s, 260 * s, 400 * s), fill=PAPER, outline=INK, width=int(7 * s))
        d.polygon([(25 * s, 66 * s), (150 * s, 5 * s), (275 * s, 66 * s)], fill=CORAL, outline=INK, width=int(6 * s))
        for r in range(4):
            for c in range(3):
                x0, y0 = 65 + c * 65, 95 + r * 65
                d.rectangle((x0 * s, y0 * s, (x0 + 42) * s, (y0 + 38) * s), fill=SUN if (r * 3 + c) % 2 == 0 or lit > .5 else SKY, outline=INK, width=int(4 * s))
        d.rectangle((125 * s, 340 * s, 175 * s, 400 * s), fill=GRAPE, outline=INK, width=int(5 * s))
    return sticker(f, w, int(w * 1.36))

def icon_trophy(w):
    def f(d, W_, H_):
        s = W_ / 240
        d.chord((30 * s, -60 * s, 210 * s, 170 * s), 0, 180, fill=SUN, outline=INK, width=int(7 * s))
        d.arc((0, 10 * s, 70 * s, 100 * s), 90, 270, fill=INK, width=int(10 * s)); d.arc((170 * s, 10 * s, 240 * s, 100 * s), 270, 90, fill=INK, width=int(10 * s))
        d.rectangle((105 * s, 165 * s, 135 * s, 215 * s), fill=SUN, outline=INK, width=int(5 * s))
        d.rounded_rectangle((55 * s, 210 * s, 185 * s, 250 * s), int(8 * s), fill=GRAPE, outline=INK, width=int(6 * s))
        d.text((120 * s, 70 * s), "1", font=font("anton", int(80 * s)), fill=INK, anchor="mm")
    return sticker(f, w, int(w * 1.08))

def icon_plate(w):
    def f(d, W_, H_):
        s = W_ / 400
        d.ellipse((0, 0, 400 * s, 160 * s), fill=PAPER, outline=INK, width=int(7 * s))
        d.ellipse((60 * s, 25 * s, 340 * s, 135 * s), outline=(220, 215, 200), width=int(6 * s))
    return sticker(f, w, int(w * .4))

def confetti(img, t, t0, n=40, area=(0, 0, W, H), seed=1):
    if t < t0: return
    import random
    r = random.Random(seed)
    for i in range(n):
        x0 = r.uniform(area[0], area[2]); vy = r.uniform(250, 520); vx = r.uniform(-120, 120)
        dt = t - t0 - r.uniform(0, .4)
        if dt < 0 or dt > 3: continue
        x = x0 + vx * dt; y = area[1] - 40 + vy * dt
        c = [SUN, CORAL, MINT, SKY, GRAPE, PAPER][i % 6]
        a = math.radians((t * 300 + i * 40) % 360)
        sx = 14 * abs(math.cos(a)) + 2
        img.paste(c, (int(x - sx), int(y - 8), int(x + sx), int(y + 8)))
