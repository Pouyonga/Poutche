# Miniature YouTube 1280x720 : vidéo 1 « Black Friday : qui gagne VRAIMENT de l'argent ? »
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from style import *

W, H = 1280, 720
OUT = sys.argv[1] if len(sys.argv) > 1 else "miniature_black_friday.png"

# fond : noir avec halo rouge derrière l'étiquette et halo chaud à droite
yy, xx = np.mgrid[0:H, 0:W]
base = np.array(BG, float)[None, None, :].repeat(H, 0).repeat(W, 1)
def glow(cx, cy, r, col, k):
    g = np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1) ** 2 * k
    return g[..., None] * (np.array(col, float) - base)
arr = base + glow(330, 400, 620, (150, 18, 14), 0.85) + glow(980, 330, 560, (70, 56, 0), 0.55)
img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
d = ImageDraw.Draw(img)

# courbe de prix rouge qui monte (derrière l'étiquette)
pts = [(-20, 640), (120, 560), (210, 600), (330, 430), (420, 470), (560, 250), (640, 140)]
glow_l = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow_l).line(pts, fill=(255, 40, 30, 200), width=30, joint="curve")
img.alpha_composite(glow_l.filter(ImageFilter.GaussianBlur(18)))
d = ImageDraw.Draw(img)
d.line(pts, fill=RED, width=12, joint="curve")
# pointe de flèche
ax, ay = pts[-1]; bx, by = pts[-2]
ang = math.atan2(ay - by, ax - bx)
tip = (ax + 34 * math.cos(ang), ay + 34 * math.sin(ang))
l = (ax + 30 * math.cos(ang + 2.4), ay + 30 * math.sin(ang + 2.4))
r = (ax + 30 * math.cos(ang - 2.4), ay + 30 * math.sin(ang - 2.4))
d.polygon([tip, l, r], fill=RED)

# étiquette de prix (dessinée à plat puis tournée)
TW, TH = 520, 300
tag = Image.new("RGBA", (TW + 80, TH + 80), (0, 0, 0, 0))
td = ImageDraw.Draw(tag)
ox, oy = 40, 40
notch = 95
poly = [(ox + notch, oy), (ox + TW, oy), (ox + TW, oy + TH), (ox + notch, oy + TH), (ox, oy + TH // 2)]
td.polygon(poly, fill=(250, 250, 250))
td.rounded_rectangle((ox + notch, oy, ox + TW, oy + TH), 26, fill=(250, 250, 250))
td.ellipse((ox + 52, oy + TH // 2 - 20, ox + 92, oy + TH // 2 + 20), fill=(30, 30, 36))
f = font("anton", 172)
tw, th, b = text_size(td, "-35%", f)
cx = ox + notch + (TW - notch) / 2 + 10
td.text((cx, oy + TH / 2 + 4), "-35%", font=f, fill=RED, anchor="mm")
# barre « prix barré » : un seul trait épais, en travers, qui laisse lire le chiffre
td.line((ox + notch + 100, oy + TH * 0.66, ox + TW - 16, oy + TH * 0.40), fill=(18, 18, 22), width=14)
tag = tag.rotate(9, resample=Image.BICUBIC, expand=True)
# ombre de l'étiquette
sh = Image.new("RGBA", tag.size, (0, 0, 0, 0))
sh.putalpha(tag.getchannel("A").point(lambda v: int(v * 0.75)))
TX, TY = 18, 170
img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)), (TX + 14, TY + 26))
img.alpha_composite(tag, (TX, TY))
d = ImageDraw.Draw(img)
# ficelle de l'étiquette
hx, hy = TX + 152, TY + 268
d.line([(hx, hy), (hx - 40, hy - 90), (hx - 62, hy - 190)], fill=(205, 205, 210), width=5, joint="curve")

# texte principal
fy = font("anton", 250)
draw_text(img, (1240, 92), "C’EST", fy, YELLOW, anchor="ra", stroke=10, stroke_fill=(0, 0, 0),
          shadow=(8, 12, 14, 0.9))
draw_text(img, (1240, 330), "FAUX ?", fy, YELLOW, anchor="ra", stroke=10, stroke_fill=(0, 0, 0),
          shadow=(8, 12, 14, 0.9))

# pastille « BLACK FRIDAY » en haut à gauche (loin du coin du minutage YouTube)
fp = font("anton", 54)
pw, ph, _ = text_size(d, "BLACK FRIDAY", fp)
d.rounded_rectangle((36, 34, 36 + pw + 44, 34 + 78), 14, fill=(250, 250, 250))
d.text((36 + 22 + pw / 2, 34 + 39), "BLACK FRIDAY", font=fp, fill=(12, 12, 16), anchor="mm")

img.convert("RGB").save(OUT, quality=95)
img.convert("RGB").resize((320, 180), Image.LANCZOS).save(OUT.replace(".png", "_mobile.png"))
print("ok", OUT)
