import math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR = 1080, 1920, 30, 40.0
N = int(FPS * DUR)
OUT = sys.argv[1]
PREVIEW = sys.argv[2:]  # optional list of times to dump as png

FD = "/usr/share/fonts/opentype/inter/"
def F(name, size): return ImageFont.truetype(FD + name, size)
BLACK = lambda s: F("InterDisplay-Black.otf", s)
XB = lambda s: F("InterDisplay-ExtraBold.otf", s)
BOLD = lambda s: F("InterDisplay-Bold.otf", s)
SEMI = lambda s: F("InterDisplay-SemiBold.otf", s)
MED = lambda s: F("Inter-Medium.otf", s)
MONO = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", s)

BG = (10, 10, 14)
WHITE = (245, 245, 247)
GREY = (140, 140, 152)
DIM = (70, 70, 82)
ORANGE = (247, 147, 26)
GREEN = (52, 211, 120)
CARD = (24, 24, 32)

BTC_PRICE_EUR = 55000            # cours approx. octobre 2026 (à ajuster)
TODAY_VALUE = 10000 * BTC_PRICE_EUR

# ---------- easing helpers ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def eo(x): return 1 - (1 - x) ** 3                      # ease out cubic
def eio(x): return 4*x**3 if x < .5 else 1 - (-2*x+2)**3/2
def back(x, s=1.7):
    x -= 1; return x*x*((s+1)*x + s) + 1
def fade(t, a, b, fi=.3, fo=.3):
    """alpha for an element visible in [a,b]"""
    return clamp(min(prog(t, a, a+fi), 1 - prog(t, b-fo, b)))

# ---------- background ----------
yy, xx = np.mgrid[0:H, 0:W]
def make_bg(cx, cy, col, strength):
    d = np.sqrt((xx-cx)**2 + (yy-cy)**2) / 1100
    g = np.clip(1 - d, 0, 1) ** 2 * strength
    base = np.array(BG, float)
    img = base + g[..., None] * (np.array(col, float) - base)
    # vignette
    v = np.sqrt(((xx-W/2)/W)**2 + ((yy-H/2)/H)**2)
    img *= np.clip(1.15 - v*0.9, 0.6, 1)[..., None]
    return img
BG_NEUTRAL = make_bg(540, 820, (40, 40, 60), 0.9)
BG_ORANGE = make_bg(540, 860, (120, 64, 10), 0.9)
GRID = np.zeros((H, W), float)
GRID[::90, :] = 1; GRID[:, ::90] = 1

def background(t):
    # orange warmth rises during the climax
    w = max(fade(t, 0, 3.0, .01, .5) * .5, fade(t, 28, 40, 1.5, .01))
    img = BG_NEUTRAL * (1 - w) + BG_ORANGE * w
    off = int(t * 12) % 90
    grid = np.roll(GRID, off, axis=0)
    img = img + grid[..., None] * 7
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")

# ---------- drawing primitives on RGBA layers ----------
def layer(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def text(base, s, font, cx, cy, fill, alpha=1.0, scale=1.0, anchor="mm", glow=None, dy=0):
    if alpha <= 0.01: return
    bbox = font.getbbox(s)
    tw, th = bbox[2] - bbox[0] + 40, bbox[3] - bbox[1] + 40
    tl = Image.new("RGBA", (tw + 60, th + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(tl)
    d.text((tl.width/2, tl.height/2), s, font=font, fill=fill + (255,), anchor="mm")
    if glow:
        g = tl.copy().filter(ImageFilter.GaussianBlur(glow))
        tl = Image.alpha_composite(g, tl)
    if scale != 1.0:
        tl = tl.resize((max(1, int(tl.width*scale)), max(1, int(tl.height*scale))), Image.LANCZOS)
    if alpha < 1:
        a = tl.getchannel("A").point(lambda v: int(v * alpha)); tl.putalpha(a)
    x = int(cx - tl.width/2); y = int(cy + dy - tl.height/2)
    base.alpha_composite(tl, (max(0, x), max(0, y)), (max(0, -x), max(0, -y)))

def rrect(base, box, r, fill, alpha=1.0, outline=None, width=0):
    L = layer(); d = ImageDraw.Draw(L)
    d.rounded_rectangle(box, r, fill=fill + (int(255*alpha),),
                        outline=(outline + (int(255*alpha),)) if outline else None, width=width)
    base.alpha_composite(L)

def coin(base, cx, cy, r, alpha=1.0, rot=0.0):
    if alpha <= .01: return
    s = int(4 * r + 20)
    L = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    c = s / 2
    sx = abs(math.cos(rot)) * 0.85 + 0.15   # fake 3D flip
    d.ellipse((c-r*sx, c-r, c+r*sx, c+r), fill=ORANGE + (255,))
    d.ellipse((c-r*.84*sx, c-r*.84, c+r*.84*sx, c+r*.84), outline=(255, 190, 90, 255), width=max(2, int(r*.06)))
    if sx > .45:
        f = BLACK(int(r * 1.15))
        sym = Image.new("RGBA", (s, s), (0, 0, 0, 0)); sd = ImageDraw.Draw(sym)
        sd.text((c, c), "B", font=f, fill=(255, 255, 255, 255), anchor="mm")
        bw = max(3, int(r*.09))
        for ox in (-r*.12, r*.12):
            sd.rectangle((c+ox-bw/2, c-r*.66, c+ox+bw/2, c+r*.66), fill=(255, 255, 255, 255))
        sd.text((c, c), "B", font=f, fill=(255, 255, 255, 255), anchor="mm")
        sym = sym.resize((max(1, int(s*sx)), s)); tmp = Image.new("RGBA", (s, s), (0,0,0,0))
        tmp.alpha_composite(sym, (int((s - sym.width)/2), 0)); L.alpha_composite(tmp)
    glow = L.filter(ImageFilter.GaussianBlur(r*.35))
    L = Image.alpha_composite(glow, L)
    if alpha < 1: L.putalpha(L.getchannel("A").point(lambda v: int(v*alpha)))
    base.alpha_composite(L, (int(cx - c), int(cy - c)))

def pizza(base, cx, cy, r, alpha=1.0, rot=0.0, bite=0):
    if alpha <= .01: return
    s = int(2*r + 40)
    L = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    c = s/2
    d.ellipse((c-r, c-r, c+r, c+r), fill=(214, 140, 60, 255))            # crust
    d.ellipse((c-r*.86, c-r*.86, c+r*.86, c+r*.86), fill=(252, 196, 70, 255))  # cheese
    for i in range(8):                                                    # slice lines
        a = rot + i * math.pi/4
        d.line((c, c, c + math.cos(a)*r*.86, c + math.sin(a)*r*.86), fill=(214, 150, 60, 255), width=max(2, int(r*.03)))
    rng = np.random.RandomState(3)
    for i in range(9):                                                    # pepperoni
        a = rot + rng.rand()*2*math.pi; rr = r*(.2 + .5*rng.rand())
        px, py = c + math.cos(a)*rr, c + math.sin(a)*rr; pr = r*.11
        d.ellipse((px-pr, py-pr, px+pr, py+pr), fill=(196, 52, 40, 255))
    if alpha < 1: L.putalpha(L.getchannel("A").point(lambda v: int(v*alpha)))
    base.alpha_composite(L, (int(cx-c), int(cy-c)))

def fmt(n):
    return f"{int(n):,}".replace(",", " ")

# ---------- subtitles (synced to the voice-over script) ----------
SUBS = [
    (0.15, 1.35, "Cet homme a payé"),
    (1.35, 2.95, "deux pizzas…"),
    (1.95, 2.95, "des centaines de millions d'euros."),
    (3.10, 4.60, "Mai 2010."),
    (4.60, 6.60, "Le bitcoin vient à peine de naître."),
    (6.60, 9.10, "Il ne vaut presque rien : moins d'un centime."),
    (9.10, 11.90, "Et personne ne s'en sert pour acheter quoi que ce soit."),
    (12.10, 14.60, "Laszlo Hanyecz, un programmeur de Floride,"),
    (14.60, 16.20, "poste un message sur un forum :"),
    (16.20, 19.20, "« 10 000 bitcoins pour deux pizzas. »"),
    (19.30, 20.90, "Quatre jours passent…"),
    (20.90, 22.90, "Puis un étudiant de 19 ans accepte."),
    (22.90, 25.00, "Laszlo envoie ses 10 000 bitcoins."),
    (25.00, 26.40, "Les pizzas arrivent."),
    (26.40, 28.00, "Le tout premier achat en bitcoin."),
    (28.10, 30.40, "À l'époque, ça valait 41 dollars."),
    (30.40, 31.80, "Aujourd'hui ?"),
    (31.80, 35.90, "Ces bitcoins vaudraient plus d'un demi-milliard d'euros."),
    (36.10, 38.10, "Et toi, tu les aurais gardés ?"),
    (38.10, 39.95, "Abonne-toi pour plus d'histoires d'argent."),
]
# hook: show one line at a time
SUBS[1] = (1.35, 1.95, "deux pizzas…")

SUB_Y = 1380
def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if font.getlength(t) > maxw and cur: lines.append(cur); cur = w_
        else: cur = t
    lines.append(cur); return lines

def draw_subs(base, t):
    f = XB(54)
    for a, b, s in SUBS:
        if a <= t < b:
            p = eo(prog(t, a, a + .15))
            lines = wrap(s, f, 860)
            lh = 72
            total = lh * len(lines)
            pad = 26
            maxw = max(f.getlength(l) for l in lines)
            box = (W/2 - maxw/2 - pad, SUB_Y - total/2 - pad*.6, W/2 + maxw/2 + pad, SUB_Y + total/2 + pad*.6)
            rrect(base, tuple(int(v) for v in box), 22, (0, 0, 0), alpha=.55*p)
            for i, l in enumerate(lines):
                y = SUB_Y - total/2 + lh*(i + .5) + (1-p)*14
                # highlight key words in orange
                col = ORANGE if any(k in l for k in ("bitcoin", "pizzas", "millions", "milliard", "10 000", "41")) else WHITE
                text(base, l, f, W/2, y, col if i == 0 and len(lines) == 1 else WHITE, alpha=p)
            return

# ---------- scenes ----------
def scene_hook(img, t):
    if t > 3.2: return
    out = 1 - prog(t, 2.85, 3.15)
    # "CET HOMME A PAYÉ"
    p = eo(prog(t, 0.05, .45))
    text(img, "CET HOMME A PAYÉ", BOLD(58), W/2, 330, GREY, alpha=p*out, dy=(1-p)*30)
    # two pizzas pop in
    for i, (x, d) in enumerate(((360, .25), (720, .45))):
        q = prog(t, d, d + .45)
        pizza(img, x, 640, 170 * back(q) if q > 0 else 0, alpha=min(1, q*3)*out, rot=t*.6 + i)
    text(img, "2 PIZZAS", BLACK(150), W/2, 920, WHITE, alpha=eo(prog(t, .5, .8))*out, scale=.85 + .15*back(prog(t, .5, .9)))
    # equals + big money
    q = prog(t, 1.6, 2.0)
    text(img, "=", BLACK(110), W/2, 1060, GREY, alpha=eo(q)*out)
    text(img, "+500 000 000 €", BLACK(118), W/2, 1190, ORANGE, alpha=eo(prog(t, 1.85, 2.1))*out,
         scale=.7 + .3*back(prog(t, 1.85, 2.25)), glow=18)

def scene_context(img, t):
    if not (2.9 < t < 12.3): return
    a_all = fade(t, 3.0, 12.1, .3, .35)
    # date
    p = eo(prog(t, 3.1, 3.6))
    text(img, "MAI", BOLD(70), W/2, 300, GREY, alpha=p*a_all, dy=(1-p)*-30)
    yr = int(2026 - (2026-2010)*eio(prog(t, 3.1, 4.2)))
    text(img, str(yr), BLACK(230), W/2, 470, WHITE, alpha=p*a_all)
    # coin + price
    q = prog(t, 4.6, 5.2)
    coin(img, W/2, 790, 150*back(q) if q > 0 else 1, alpha=min(1, q*3)*a_all, rot=4*math.pi*eo(prog(t, 4.6, 6.6)))
    r = prog(t, 6.6, 8.6)
    price = 0.30 - (0.30 - 0.004) * eo(r)
    if t > 6.6:
        text(img, "1 BITCOIN =", BOLD(54), W/2, 1010, GREY, alpha=a_all*eo(prog(t, 6.6, 6.9)))
        s = f"{price:.3f} $".replace(".", ",")
        text(img, s, BLACK(140), W/2, 1130, ORANGE, alpha=a_all*eo(prog(t, 6.6, 6.9)), glow=14)
    # "personne ne l'utilise" : crossed-out shop tags
    if t > 9.1:
        k = eo(prog(t, 9.1, 9.5))
        text(img, "Commerces qui l'acceptent : 0", BOLD(48), W/2, 1250, GREY, alpha=a_all*k)
        # move content up a touch? keep simple: strike line
        sl = 0
        if sl > 0:
            L = layer(); d = ImageDraw.Draw(L)
            d.line((W/2 - 300, 1252, W/2 - 300 + 600*sl, 1252), fill=(230, 70, 70, int(255*a_all)), width=6)
            img.alpha_composite(L)

POST_EN = "I'll pay 10,000 bitcoins for a couple of pizzas.. like maybe 2 large ones so I have some left over for the next day."
def scene_story(img, t):
    if not (11.9 < t < 28.3): return
    # --- part A: forum post (12 – 19.2)
    a = fade(t, 12.1, 19.3, .4, .35)
    if a > 0:
        p = eo(prog(t, 12.1, 12.6))
        text(img, "18 MAI 2010", BOLD(56), W/2, 250, ORANGE, alpha=a*p)
        top = 340 + (1-p)*60
        rrect(img, (90, int(top), 990, int(top + 780)), 34, CARD, alpha=a, outline=(50, 50, 64), width=2)
        # header
        L = layer(); d = ImageDraw.Draw(L)
        d.ellipse((140, top+50, 240, top+150), fill=ORANGE + (int(255*a),))
        img.alpha_composite(L)
        text(img, "L", BLACK(60), 190, top+100, (255, 255, 255), alpha=a)
        d = ImageDraw.Draw(img)
        f1 = BOLD(44); f2 = MED(32)
        col = lambda c: c + (int(255*a),)
        d.text((270, top+62), "laszlo", font=f1, fill=col(WHITE))
        d.text((270, top+115), "bitcointalk.org · forum", font=f2, fill=col(GREY))
        d.text((140, top+200), "Pizza for bitcoins?", font=BOLD(52), fill=col(WHITE))
        # typed text
        n = int(len(POST_EN) * prog(t, 13.0, 16.4))
        typed = POST_EN[:n] + ("|" if (t*2) % 1 < .5 and n < len(POST_EN) else "")
        ff = MED(40)
        for i, l in enumerate(wrap(typed, ff, 780)):
            d.text((140, top+290 + i*58), l, font=ff, fill=col((210, 210, 220)))
        # translation tag
        if t > 16.2:
            q = eo(prog(t, 16.2, 16.6))
            rrect(img, (140, int(top+600), 940, int(top+720)), 24, (60, 36, 6), alpha=a*q)
            text(img, "10 000 ₿  →  2 pizzas".replace("₿", "BTC"), BLACK(60), W/2, top+660, ORANGE, alpha=a*q)
    # --- part B: 4 days pass (19.3 – 20.9)
    b = fade(t, 19.3, 20.95, .25, .25)
    if b > 0:
        days = 18 + min(4, int(prog(t, 19.4, 20.5) * 5))
        text(img, f"{days} MAI", BLACK(190), W/2, 650, WHITE, alpha=b)
        text(img, "… toujours personne", BOLD(56), W/2, 860, GREY, alpha=b)
        # little progress dots
        L = layer(); d = ImageDraw.Draw(L)
        for i in range(5):
            on = i <= days - 18
            x = W/2 - 160 + i*80
            d.ellipse((x-14, 1000-14, x+14, 1000+14), fill=(ORANGE if on else DIM) + (int(255*b),))
        img.alpha_composite(L)
    # --- part C: the deal (20.9 – 28)
    c = fade(t, 20.9, 28.15, .3, .3)
    if c > 0:
        text(img, "22 MAI 2010", BOLD(56), W/2, 250, ORANGE, alpha=c)
        # left: Laszlo / right: student
        for x, lab, sub in ((250, "Laszlo", "Floride"), (830, "Jeremy", "19 ans")):
            L = layer(); d = ImageDraw.Draw(L)
            d.ellipse((x-90, 380, x+90, 560), fill=(40, 40, 54, int(255*c)), outline=(80, 80, 96, int(255*c)), width=3)
            d.ellipse((x-34, 410, x+34, 478), fill=(150, 150, 165, int(255*c)))
            d.pieslice((x-66, 486, x+66, 618), 180, 360, fill=(150, 150, 165, int(255*c)))
            img.alpha_composite(L)
            text(img, lab, BOLD(48), x, 610, WHITE, alpha=c)
            text(img, sub, MED(34), x, 660, GREY, alpha=c)
        # coins fly left -> right (22.9 – 25)
        for i in range(10):
            st = 22.9 + i*.13
            q = prog(t, st, st + .9)
            if 0 < q < 1:
                e = eio(q)
                x = 250 + (830-250)*e; y = 470 - math.sin(e*math.pi)*110
                coin(img, x, y, 40, alpha=c*min(1, (1-q)*6, q*6), rot=q*6)
        # counter of sent BTC
        sent = 10000 * eo(prog(t, 23.0, 24.6))
        if t > 22.9:
            text(img, f"{fmt(sent)} BTC", BLACK(110), W/2, 860, ORANGE, alpha=c*eo(prog(t, 22.9, 23.2)), glow=12)
            text(img, "envoyés", BOLD(46), W/2, 955, GREY, alpha=c*eo(prog(t, 22.9, 23.2)))
        # pizzas arrive from right -> left (25 – 26.4)
        for i, tx in enumerate((400, 680)):
            q = prog(t, 25.0 + i*.15, 25.8 + i*.15)
            if q > 0:
                e = back(q, 1.2)
                x = 830 + (tx - 830)*e if q < 1 else tx
                pizza(img, x, 1095, 115, alpha=c*min(1, q*4), rot=t*.5 + i)
        if t > 26.4:
            q = eo(prog(t, 26.4, 26.8))
            rrect(img, (170, 1232, 910, 1306), 38, (60, 36, 6), alpha=c*q)
            text(img, "BITCOIN PIZZA DAY", BLACK(46), W/2, 1269, ORANGE, alpha=c*q)

def scene_climax(img, t):
    if not (27.9 < t < 36.3): return
    a = fade(t, 28.1, 36.1, .3, .3)
    # then
    p = eo(prog(t, 28.2, 28.6))
    text(img, "EN 2010", BOLD(52), W/2, 300, GREY, alpha=a*p)
    text(img, "41 $", BLACK(140), W/2, 430, WHITE, alpha=a*p)
    # now
    if t > 30.4:
        q = eo(prog(t, 30.4, 30.8))
        text(img, "AUJOURD'HUI", BOLD(52), W/2, 640, ORANGE, alpha=a*q)
        r = prog(t, 30.7, 34.6)
        # exponential-feeling count up
        val = 41 * (TODAY_VALUE/41) ** eo(r) if r > 0 else 41
        done = r >= 1
        sc = 1.0 + (0.08*math.sin(prog(t, 34.6, 35.0)*math.pi) if done else 0)
        s = fmt(val) + " €"
        size = 128 if len(s) <= 13 else 112
        text(img, s, BLACK(size), W/2, 810, ORANGE if done else WHITE, alpha=a*q, scale=sc, glow=24 if done else 8)
        # growth bar
        L = layer(); d = ImageDraw.Draw(L)
        d.rounded_rectangle((140, 940, 940, 966), 13, fill=(40, 40, 52, int(255*a*q)))
        d.rounded_rectangle((140, 940, 140 + max(26, 800*eo(r)), 966), 13, fill=ORANGE + (int(255*a*q),))
        img.alpha_composite(L)
        text(img, f"x {fmt(TODAY_VALUE/41)}", BOLD(56), W/2, 1060, GREEN, alpha=a*eo(prog(t, 34.6, 35.0)))
        text(img, f"10 000 BTC × ~{fmt(BTC_PRICE_EUR)} €", MED(34), W/2, 1140, GREY, alpha=a*q*.9)
        # floating coins
        for i in range(7):
            ph = i*1.3
            x = 120 + (i*137) % 840; y = 1250 - ((t-30.4)*90 + i*60) % 1100
            coin(img, x, y, 26, alpha=a*q*.18, rot=t*2 + ph)

def scene_outro(img, t):
    if t < 35.9: return
    a = fade(t, 36.0, 40.5, .35, .01)
    p = eo(prog(t, 36.1, 36.6))
    text(img, "ET TOI ?", BLACK(170), W/2, 420, WHITE, alpha=a*p, scale=.8 + .2*back(prog(t, 36.1, 36.6)))
    text(img, "Tu aurais gardé", BOLD(66), W/2, 600, GREY, alpha=a*p)
    text(img, "tes bitcoins ?", BOLD(66), W/2, 680, ORANGE, alpha=a*p)
    # two choices
    q = eo(prog(t, 36.6, 37.0))
    rrect(img, (140, 800, 520, 920), 30, CARD, alpha=a*q, outline=(70, 70, 86), width=2)
    rrect(img, (560, 800, 940, 920), 30, CARD, alpha=a*q, outline=(70, 70, 86), width=2)
    text(img, "Gardé", BOLD(48), 330, 860, WHITE, alpha=a*q)
    text(img, "Pizzas", BOLD(48), 750, 860, WHITE, alpha=a*q)
    # subscribe pill
    if t > 38.1:
        r = prog(t, 38.1, 38.5); pulse = 1 + .04*math.sin((t-38.5)*8) * (t > 38.5)
        w = 380 * back(r) * pulse
        rrect(img, (int(W/2 - w), 1040, int(W/2 + w), 1170), 65, ORANGE, alpha=a*min(1, r*3))
        text(img, "ABONNE-TOI", BLACK(64), W/2, 1105, (15, 15, 18), alpha=a*eo(prog(t, 38.25, 38.5)))
        text(img, "pour plus d'histoires d'argent", BOLD(44), W/2, 1235, WHITE, alpha=a*eo(prog(t, 38.3, 38.6)))

# progress bar on top (story timeline)
def topbar(img, t):
    L = layer(); d = ImageDraw.Draw(L)
    d.rectangle((0, 0, int(W*t/DUR), 8), fill=ORANGE + (200,))
    img.alpha_composite(L)

def frame(t):
    img = background(t)
    scene_hook(img, t); scene_context(img, t); scene_story(img, t)
    scene_climax(img, t); scene_outro(img, t)
    draw_subs(img, t); topbar(img, t)
    return img.convert("RGB")

if PREVIEW:
    for s in PREVIEW:
        frame(float(s)).save(f"prev_{s}.png")
    sys.exit()

ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
for i in range(N):
    ff.stdin.write(frame(i / FPS).tobytes())
    if i % 150 == 0: print(i, flush=True)
ff.stdin.close(); ff.wait()
print("done")
