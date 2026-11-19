# Miniature vidéo GTA 6 (1280x720). Aucun logo ni visuel du jeu : manette générique + billets + texte.
import sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from style import *

W, H = 1280, 720
OUT = sys.argv[1] if len(sys.argv) > 1 else "miniature_gta6.png"
yy, xx = np.mgrid[0:H, 0:W]
base = np.array(BG, float)[None, None, :].repeat(H, 0).repeat(W, 1)
def glow(cx, cy, r, col, k):
    g = np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1) ** 2 * k
    return g[..., None] * (np.array(col, float) - base)
arr = base + glow(360, 420, 560, (20, 140, 70), .9) + glow(960, 300, 520, (60, 60, 90), .6)
img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

def shadowed(layer, x, y, a=.55, blur=16):
    m = blur * 3
    big = Image.new("RGBA", (layer.width + 2 * m, layer.height + 2 * m), (0, 0, 0, 0)); big.paste(layer, (m, m))
    layer = big; x -= m; y -= m
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0)); sh.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (x + 10, y + 16)); img.alpha_composite(layer, (x, y))

def bill(w, h, ang):
    b = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0)); q = ImageDraw.Draw(b)
    q.rounded_rectangle((10, 10, 10 + w, 10 + h), 10, fill=(40, 160, 90), outline=(20, 90, 50), width=5)
    q.ellipse((10 + w / 2 - h * .3, 10 + h * .2, 10 + w / 2 + h * .3, 10 + h * .8), outline=(210, 245, 220), width=5)
    q.text((10 + w / 2, 10 + h / 2 + 2), "$", font=font("anton", int(h * .55)), fill=(230, 255, 235), anchor="mm")
    return b.rotate(ang, resample=Image.BICUBIC, expand=True)

# billets qui jaillissent (derrière la manette)
rnd = random.Random(8)
for i in range(9):
    ang = rnd.uniform(-40, 40); s = rnd.uniform(.7, 1.05)
    x = int(330 + math.cos(math.radians(-90 + (i - 4) * 19)) * rnd.uniform(150, 250) - 100)
    y = int(400 + math.sin(math.radians(-90 + (i - 4) * 19)) * rnd.uniform(150, 260) - 50)
    shadowed(bill(int(170 * s), int(85 * s), ang), x, y, .35, 8)

# manette générique
s = 1.0
P = Image.new("RGBA", (620, 380), (0, 0, 0, 0)); d = ImageDraw.Draw(P)
col = (34, 34, 46)
d.rounded_rectangle((40, 40, 580, 260), 110, fill=col); d.ellipse((0, 130, 240, 375), fill=col); d.ellipse((380, 130, 620, 375), fill=col)
d.rectangle((118, 115, 150, 230), fill=WHITE); d.rectangle((78, 157, 190, 189), fill=WHITE)
for (x, y, c) in [(465, 110, GREEN), (515, 160, RED), (415, 160, BLUE), (465, 210, YELLOW)]:
    d.ellipse((x - 25, y - 25, x + 25, y + 25), fill=c)
d.ellipse((222, 215, 292, 285), fill=(15, 15, 22)); d.ellipse((328, 215, 398, 285), fill=(15, 15, 22))
P = P.resize((496, 304), Image.LANCZOS)
shadowed(P, 70, 400)

# textes
draw_text(img, (1240, 40), "GTA 6", font("anton", 170), WHITE, anchor="ra", stroke=8, stroke_fill=(0, 0, 0), shadow=(6, 10, 12, .9))
draw_text(img, (1245, 245), "+1 MILLIARD $", font("anton", 118), GREEN, anchor="ra", stroke=8, stroke_fill=(0, 0, 0), shadow=(6, 10, 12, .9))
d = ImageDraw.Draw(img)
fp = font("anton", 58)
txt = "AVANT SA SORTIE"
b = d.textbbox((0, 0), txt, font=fp); tw = b[2] - b[0]
d.rounded_rectangle((1240 - tw - 50, 445, 1240, 535), 16, fill=RED)
d.text((1240 - 25 - tw / 2, 490), txt, font=fp, fill=WHITE, anchor="mm")

img.convert("RGB").save(OUT, quality=95)
img.convert("RGB").resize((320, 180), Image.LANCZOS).save(OUT.replace(".png", "_mobile.png"))
print("ok")
