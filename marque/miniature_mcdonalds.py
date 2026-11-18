# Miniature vidéo 2 « Comment McDonald's gagne VRAIMENT son argent » (1280x720)
# Concept : burger barré « PAS ÇA » -> immeuble rentable « ÇA ! ». Aucun logo de marque.
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from style import *

W, H = 1280, 720
OUT = sys.argv[1] if len(sys.argv) > 1 else "miniature_mcdonalds.png"

yy, xx = np.mgrid[0:H, 0:W]
base = np.array(BG, float)[None, None, :].repeat(H, 0).repeat(W, 1)
def glow(cx, cy, r, col, k):
    g = np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1) ** 2 * k
    return g[..., None] * (np.array(col, float) - base)
arr = base + glow(300, 420, 520, (120, 20, 14), .8) + glow(960, 380, 620, (20, 110, 60), .75)
img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

def shadowed(layer, x, y, a=.55):
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (x + 10, y + 16))
    img.alpha_composite(layer, (x, y))

# ---- burger ----
B = Image.new("RGBA", (460, 380), (0, 0, 0, 0))
d = ImageDraw.Draw(B)
d.chord((20, 10, 440, 250), 180, 360, fill=(222, 150, 60))                # pain du dessus
d.rectangle((20, 128, 440, 150), fill=(222, 150, 60))
for sx, sy in [(120, 60), (190, 40), (260, 45), (330, 70), (160, 95), (230, 85), (300, 100), (380, 110), (90, 105)]:
    d.ellipse((sx - 9, sy - 5, sx + 9, sy + 5), fill=(255, 240, 200))       # sésame
pts = [(10, 160)] + [(10 + i * 22, 150 + (12 if i % 2 else 0)) for i in range(21)] + [(450, 160), (450, 185), (10, 185)]
d.polygon(pts, fill=(70, 190, 80))                                         # salade
d.polygon([(30, 182), (430, 182), (400, 220), (230, 250), (60, 220)], fill=(255, 200, 40))  # fromage
d.rounded_rectangle((25, 195, 435, 265), 30, fill=(110, 58, 30))           # steak
d.rounded_rectangle((30, 270, 430, 340), 26, fill=(205, 135, 55))          # pain du dessous
shadowed(B, 40, 210)
d = ImageDraw.Draw(img)
# grande croix rouge
for (a, b) in [((60, 230), (500, 610)), ((500, 230), (60, 610))]:
    d.line([a, b], fill=(0, 0, 0), width=48)
    d.line([a, b], fill=RED, width=34)
draw_text(img, (270, 112), "PAS ÇA", font("anton", 120), RED, anchor="mm", stroke=8, stroke_fill=(0, 0, 0),
          shadow=(6, 10, 12, .9))

# ---- flèche ----
d.polygon([(560, 395), (650, 395), (650, 360), (720, 430), (650, 500), (650, 465), (560, 465)], fill=WHITE)

# ---- immeuble ----
Bd = Image.new("RGBA", (420, 520), (0, 0, 0, 0))
q = ImageDraw.Draw(Bd)
q.rectangle((60, 60, 360, 500), fill=(235, 238, 245))
q.polygon([(40, 70), (210, 0), (380, 70)], fill=(200, 205, 215))
for r in range(5):
    for c in range(3):
        x0, y0 = 95 + c * 85, 105 + r * 70
        q.rectangle((x0, y0, x0 + 55, y0 + 45), fill=(255, 212, 0) if (r + c) % 3 == 0 else (60, 70, 95))
q.rectangle((170, 440, 250, 500), fill=(60, 70, 95))
shadowed(Bd, 770, 190)
# pastille « € » géante
d = ImageDraw.Draw(img)
d.ellipse((1075, 400, 1245, 570), fill=GREEN, outline=(0, 0, 0), width=8)
d.text((1160, 490), "€", font=font("anton", 130), fill=(8, 40, 22), anchor="mm")
draw_text(img, (980, 100), "ÇA !", font("anton", 120), GREEN, anchor="mm", stroke=8, stroke_fill=(0, 0, 0),
          shadow=(6, 10, 12, .9))

img.convert("RGB").save(OUT, quality=95)
img.convert("RGB").resize((320, 180), Image.LANCZOS).save(OUT.replace(".png", "_mobile.png"))
print("ok")
