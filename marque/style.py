# Charte graphique « L'Envers du Business » : couleurs, polices et outils de dessin partagés
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
INTER = "/usr/share/fonts/opentype/inter/"

BG = (11, 11, 16)
CARD = (24, 24, 32)
LINE = (44, 44, 56)
WHITE = (246, 246, 248)
GREY = (150, 150, 162)
DIM = (82, 82, 96)
YELLOW = (255, 212, 0)
RED = (255, 59, 48)
GREEN = (52, 211, 120)
BLUE = (64, 156, 255)

_cache = {}
def font(kind, size):
    key = (kind, int(size))
    if key not in _cache:
        path = {
            "anton": os.path.join(HERE, "polices/Anton-Regular.ttf"),
            "bebas": os.path.join(HERE, "polices/BebasNeue-Regular.ttf"),
            "black": INTER + "InterDisplay-Black.otf",
            "xbold": INTER + "InterDisplay-ExtraBold.otf",
            "bold": INTER + "InterDisplay-Bold.otf",
            "semi": INTER + "InterDisplay-SemiBold.otf",
            "med": INTER + "Inter-Medium.otf",
            "reg": INTER + "Inter-Regular.otf",
        }[kind]
        _cache[key] = ImageFont.truetype(path, int(size))
    return _cache[key]

def text_size(d, txt, f):
    b = d.textbbox((0, 0), txt, font=f)
    return b[2] - b[0], b[3] - b[1], b

def draw_text(img, xy, txt, f, fill, anchor="la", stroke=0, stroke_fill=(0, 0, 0),
              shadow=None, alpha=1.0):
    """Texte avec contour, ombre portée floue et transparence."""
    if alpha <= 0:
        return
    W, H = img.size
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if shadow:
        dx, dy, blur, sa = shadow
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0] + dx, xy[1] + dy), txt, font=f, fill=(0, 0, 0, int(255 * sa)),
                                anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * sa)))
        layer = Image.alpha_composite(layer, sh.filter(ImageFilter.GaussianBlur(blur)))
        d = ImageDraw.Draw(layer)
    d.text(xy, txt, font=f, fill=fill + (255,) if len(fill) == 3 else fill, anchor=anchor,
           stroke_width=stroke, stroke_fill=stroke_fill)
    if alpha < 1:
        a = layer.getchannel("A").point(lambda v: int(v * alpha))
        layer.putalpha(a)
    img.alpha_composite(layer)
