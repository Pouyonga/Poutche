# Outils de dessin rapides pour le montage (canevas RGB 1920x1080, calques réduits à la taille utile)
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../marque"))
from style import BG, CARD, LINE, WHITE, GREY, DIM, YELLOW, RED, GREEN, BLUE, font

W, H = 1920, 1080

# ---------- courbes d'animation ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, d=0.45): return clamp((t - a) / d) if d > 0 else float(t >= a)
def eo(x): return 1 - (1 - x) ** 3
def eio(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def back(x, s=1.9):
    x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, p): return a + (b - a) * p
def mix(c1, c2, p): return tuple(int(lerp(a, b, p)) for a, b in zip(c1, c2))

# ---------- collage de calques ----------
def paste(img, layer, x, y, alpha=1.0):
    if alpha <= 0.003: return
    if alpha < 0.999:
        a = layer.getchannel("A").point(lambda v, k=alpha: int(v * k))
        layer = layer.copy(); layer.putalpha(a)
    img.paste(layer, (int(round(x)), int(round(y))), layer)

def _anchor_xy(x, y, w, h, anchor):
    ax, ay = anchor[0], anchor[1]
    if ax == "m": x -= w / 2
    elif ax == "r": x -= w
    if ay == "m": y -= h / 2
    elif ay == "b": y -= h
    return x, y

_tcache = {}
def text_layer(s, f, fill, stroke=0, stroke_fill=(0, 0, 0)):
    key = (s, id(f), fill, stroke, stroke_fill)
    if key in _tcache: return _tcache[key]
    dd = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    b = dd.textbbox((0, 0), s, font=f, stroke_width=stroke)
    pad = 4 + stroke
    lay = Image.new("RGBA", (b[2] - b[0] + 2 * pad, b[3] - b[1] + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((-b[0] + pad, -b[1] + pad), s, font=f, fill=fill,
                             stroke_width=stroke, stroke_fill=stroke_fill)
    if len(_tcache) > 3000: _tcache.clear()
    _tcache[key] = (lay, pad)
    return lay, pad

def T(img, x, y, s, kind, size, fill=WHITE, anchor="mm", alpha=1.0, stroke=0, stroke_fill=(0, 0, 0),
      shadow=False, dy=0.0, scale=1.0):
    """Texte ancré (l/m/r + t/m/b) avec fondu, glissement vertical (dy) et échelle."""
    if alpha <= 0.003 or not s: return 0
    f = font(kind, max(6, size * scale))
    lay, pad = text_layer(s, f, fill, stroke, stroke_fill)
    w, h = lay.size[0] - 2 * pad, lay.size[1] - 2 * pad
    px, py = _anchor_xy(x, y + dy, w, h, anchor)
    if shadow:
        sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.getchannel("A").point(lambda v: int(v * .7)))
        paste(img, sh.filter(ImageFilter.GaussianBlur(8)), px - pad + 4, py - pad + 7, alpha)
    paste(img, lay, px - pad, py - pad, alpha)
    return w

def tw(s, kind, size):
    f = font(kind, size); b = f.getbbox(s); return b[2] - b[0]

def shape(img, box, draw_fn, alpha=1.0, blur=0):
    """Dessine une forme sur un calque à la taille de la boîte, puis la colle avec transparence."""
    x0, y0, x1, y1 = [int(v) for v in box]
    pad = 2 + blur * 3
    lay = Image.new("RGBA", (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(lay), pad, pad, x1 - x0, y1 - y0)
    if blur: lay = lay.filter(ImageFilter.GaussianBlur(blur))
    paste(img, lay, x0 - pad, y0 - pad, alpha)

def rrect(img, box, r, fill, alpha=1.0, outline=None, width=0):
    shape(img, box, lambda d, ox, oy, w, h: d.rounded_rectangle((ox, oy, ox + w, oy + h), r, fill=fill + (255,) if fill and len(fill) == 3 else fill,
                                                               outline=outline, width=width), alpha)

def glow(img, box, r, color, alpha=0.6, blur=30):
    shape(img, box, lambda d, ox, oy, w, h: d.rounded_rectangle((ox, oy, ox + w, oy + h), r, fill=color + (255,)), alpha, blur=blur)

def chip(img, x, y, s, alpha=1.0, fill=CARD, color=WHITE, size=40, kind="bold", anchor="mm", outline=None, dy=0, scale=1.0):
    """Pastille arrondie avec texte."""
    if alpha <= 0.003: return
    size = size * scale
    w = tw(s, kind, size) + size * 1.2; h = size * 1.7
    px, py = _anchor_xy(x, y + dy, w, h, anchor)
    rrect(img, (px, py, px + w, py + h), h / 2, fill, alpha, outline=outline, width=3 if outline else 0)
    T(img, px + w / 2, py + h / 2 + size * 0.02, s, kind, size, color, "mm", alpha)
    return w, h

def price_tag(w, h, text, color=(250, 250, 250), text_color=(18, 18, 22), kind="anton", size=None, strike=0.0,
              strike_color=(18, 18, 22)):
    """Étiquette de prix (calque RGBA)."""
    pad = 30
    lay = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    notch = int(h * 0.32)
    d.polygon([(pad + notch, pad), (pad + w, pad), (pad + w, pad + h), (pad + notch, pad + h), (pad, pad + h // 2)], fill=color)
    d.rounded_rectangle((pad + notch, pad, pad + w, pad + h), int(h * 0.09), fill=color)
    hr = max(6, int(h * 0.06))
    d.ellipse((pad + notch * .55 - hr, pad + h / 2 - hr, pad + notch * .55 + hr, pad + h / 2 + hr), fill=BG)
    size = size or int(h * 0.5)
    f = font(kind, size)
    cx = pad + notch + (w - notch) / 2
    d.text((cx, pad + h / 2), text, font=f, fill=text_color, anchor="mm")
    if strike > 0:
        b = d.textbbox((cx, pad + h / 2), text, font=f, anchor="mm")
        x0, x1 = b[0] - 10, b[2] + 10
        d.line((x0, pad + h / 2 + 4, lerp(x0, x1, strike), pad + h / 2 + 4), fill=strike_color, width=max(6, h // 18))
    return lay

def rotate_paste(img, lay, cx, cy, angle=0, alpha=1.0, scale=1.0):
    if scale != 1.0:
        lay = lay.resize((max(1, int(lay.width * scale)), max(1, int(lay.height * scale))), Image.BICUBIC)
    if angle:
        lay = lay.rotate(angle, resample=Image.BICUBIC, expand=True)
    paste(img, lay, cx - lay.width / 2, cy - lay.height / 2, alpha)

def stamp(img, cx, cy, s, color=RED, size=150, angle=-6, alpha=1.0, scale=1.0):
    """Tampon encadré, légèrement tourné."""
    f = font("anton", size)
    b = f.getbbox(s)
    w, h = b[2] - b[0] + size * .6, b[3] - b[1] + size * .5
    lay = Image.new("RGBA", (int(w) + 20, int(h) + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    lw = max(6, size // 14)
    d.rounded_rectangle((10, 10, 10 + w, 10 + h), size // 8, outline=color, width=lw)
    d.text((10 + w / 2, 10 + h / 2), s, font=f, fill=color, anchor="mm")
    rotate_paste(img, lay, cx, cy, angle, alpha, scale)

def strike_line(img, x0, y0, x1, y1, p, color=RED, width=12, alpha=1.0):
    if p <= 0: return
    xe, ye = lerp(x0, x1, p), lerp(y0, y1, p)
    bx = (min(x0, xe) - width, min(y0, ye) - width, max(x0, xe) + width, max(y0, ye) + width)
    shape(img, bx, lambda d, ox, oy, w, h: d.line((x0 - bx[0] + ox, y0 - bx[1] + oy, xe - bx[0] + ox, ye - bx[1] + oy),
                                                   fill=color + (255,), width=width), alpha)

def fmt(v, dec=1):
    s = f"{v:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s
