# Miniatures B et C pour le test A/B YouTube de la vidéo Black Friday (1280x720)
#   B « QUI ENCAISSE ? »  : levier argent / curiosité, fond jaune pour trancher dans le fil
#   C « LE PIÈGE »        : levier preuve / chiffres, la courbe 259 € -> 399 € -> promo
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from style import *

W, H = 1280, 720
OUT = sys.argv[1] if len(sys.argv) > 1 else "."

def radial(spots, base_col):
    yy, xx = np.mgrid[0:H, 0:W]
    base = np.array(base_col, float)[None, None, :].repeat(H, 0).repeat(W, 1)
    arr = base.copy()
    for cx, cy, r, col, k in spots:
        g = np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1) ** 2 * k
        arr += g[..., None] * (np.array(col, float) - base)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

def shadowed(img, layer, x, y, blur=18, off=(10, 16), a=.6):
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (x + off[0], y + off[1]))
    img.alpha_composite(layer, (x, y))

def save(img, name):
    img.convert("RGB").save(f"{OUT}/{name}.png")
    img.convert("RGB").resize((320, 180), Image.LANCZOS).save(f"{OUT}/{name}_mobile.png")

# ---------------- B : QUI ENCAISSE ? ----------------
img = radial([(380, 380, 700, (255, 236, 120), .9)], (255, 205, 0))
d = ImageDraw.Draw(img)
# sac de courses noir « BLACK FRIDAY »
bag = Image.new("RGBA", (520, 560), (0, 0, 0, 0))
bd = ImageDraw.Draw(bag)
bd.arc((150, 10, 370, 230), 180, 360, fill=(14, 14, 18), width=26)
bd.polygon([(40, 130), (480, 130), (440, 540), (80, 540)], fill=(14, 14, 18))
bd.rectangle((40, 130, 480, 160), fill=(30, 30, 38))
bd.text((260, 290), "BLACK", font=font("anton", 96), fill=YELLOW, anchor="mm")
bd.text((260, 395), "FRIDAY", font=font("anton", 96), fill=WHITE, anchor="mm")
bag = bag.rotate(-6, resample=Image.BICUBIC, expand=True)
shadowed(img, bag, 70, 125, a=.45)
# billets qui s'envolent du sac
def bill(w, h, ang):
    b = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    q = ImageDraw.Draw(b)
    q.rounded_rectangle((10, 10, 10 + w, 10 + h), 10, fill=(40, 150, 85), outline=(20, 90, 50), width=5)
    q.ellipse((10 + w / 2 - h * .3, 10 + h * .2, 10 + w / 2 + h * .3, 10 + h * .8), outline=(210, 245, 220), width=5)
    q.text((10 + w / 2, 10 + h / 2 + 2), "€", font=font("anton", int(h * .5)), fill=(230, 255, 235), anchor="mm")
    return b.rotate(ang, resample=Image.BICUBIC, expand=True)
for (x, y, a, s) in [(380, 70, 18, 1.0), (520, 190, -14, .9), (250, 30, -22, .8), (600, 40, 30, .75)]:
    bl = bill(int(190 * s), int(100 * s), a)
    shadowed(img, bl, x, y, blur=10, off=(6, 10), a=.35)
# texte
draw_text(img, (1245, 150), "QUI", font("anton", 230), (14, 14, 18), anchor="ra")
draw_text(img, (1245, 390), "ENCAISSE ?", font("anton", 150), RED, anchor="ra", stroke=8, stroke_fill=(14, 14, 18))
save(img, "miniature_b_qui_encaisse")

# ---------------- C : LE PIÈGE ----------------
img = radial([(420, 470, 650, (120, 18, 14), .8), (1050, 260, 520, (60, 50, 0), .6)], BG)
d = ImageDraw.Draw(img)
for x in range(0, W, 64): d.line([(x, 0), (x, H)], fill=(22, 22, 30))
for y in range(0, H, 64): d.line([(0, y), (W, y)], fill=(22, 22, 30))
P = [(70, 560), (230, 548), (400, 190), (575, 440)]   # juillet, août, septembre, promo
glow_l = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow_l).line(P[1:3], fill=(255, 40, 30, 220), width=36)
img.alpha_composite(glow_l.filter(ImageFilter.GaussianBlur(20)))
d = ImageDraw.Draw(img)
d.line(P[0:2], fill=GREEN, width=14)
d.line(P[1:3], fill=RED, width=16)
d.line(P[2:4], fill=YELLOW, width=14)
for (x, y), c in zip(P, [GREEN, GREEN, RED, YELLOW]):
    d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=c, outline=BG, width=5)
def bubble(x, y, s, fill, col, size):
    f = font("anton", size); b = f.getbbox(s)
    w, h = b[2] - b[0] + size * .5, b[3] - b[1] + size * .45
    d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), h / 2.6, fill=fill)
    d.text((x, y), s, font=f, fill=col, anchor="mm")
bubble(150, 640, "259 €", GREEN, (8, 30, 18), 70)
bubble(400, 95, "400 €", RED, WHITE, 82)
bubble(590, 535, "PROMO !", YELLOW, (14, 14, 18), 62)
# flèche « hausse cachée »
draw_text(img, (1240, 170), "LE", font("anton", 150), WHITE, anchor="ra", shadow=(6, 10, 12, .9))
draw_text(img, (1245, 305), "PIÈGE", font("anton", 235), YELLOW, anchor="ra", stroke=10, stroke_fill=(0, 0, 0), shadow=(8, 12, 14, .9))
fp = font("anton", 46)
d = ImageDraw.Draw(img)
d.rounded_rectangle((900, 34, 1240, 112), 14, fill=(250, 250, 250))
d.text((1070, 73), "BLACK FRIDAY", font=fp, fill=(12, 12, 16), anchor="mm")
save(img, "miniature_c_le_piege")
print("ok")
