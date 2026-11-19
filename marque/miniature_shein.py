# Miniature Shein (1280x720) : t-shirt minuscule prix vs montagne d'argent, + mascotte Sou (test de reconnaissance).
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../style2")); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../black_friday/video"))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import gfx, gfx2
from style import font, draw_text, YELLOW, RED, WHITE, GREEN

W, H = 1280, 720
gfx.W, gfx.H, gfx2.W, gfx2.H = W, H, W, H
OUT = sys.argv[1] if len(sys.argv) > 1 else "miniature_shein.png"

yy, xx = np.mgrid[0:H, 0:W]
base = np.array((14, 12, 24), float)[None, None, :].repeat(H, 0).repeat(W, 1)
def glow(cx, cy, r, col, k):
    g = np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1) ** 2 * k
    return g[..., None] * (np.array(col, float) - base)
arr = base + glow(330, 380, 520, (255, 90, 150), .55) + glow(1000, 420, 560, (30, 150, 80), .5)
img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

def shadowed(L, x, y, a=.55, blur=14):
    m = blur * 3; big = Image.new("RGBA", (L.width + 2 * m, L.height + 2 * m), (0, 0, 0, 0)); big.paste(L, (m, m))
    sh = Image.new("RGBA", big.size, (0, 0, 0, 0)); sh.putalpha(big.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (x - m + 10, y - m + 14)); img.alpha_composite(big, (x - m, y - m))

INK = (24, 22, 38)
# t-shirt
T_ = Image.new("RGBA", (420, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(T_)
pts = [(120, 20), (170, 40), (250, 40), (300, 20), (410, 90), (360, 170), (320, 140), (320, 390), (100, 390), (100, 140), (60, 170), (10, 90)]
d.polygon(pts, fill=(255, 120, 170), outline=INK, width=9)
d.arc((165, 5, 255, 75), 0, 180, fill=INK, width=9)
shadowed(T_.rotate(-6, resample=Image.BICUBIC, expand=True), 60, 170)
# étiquette « ? € »
tag = Image.new("RGBA", (260, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(tag)
d.polygon([(40, 0), (258, 0), (258, 128), (40, 128), (0, 64)], fill=(255, 251, 240), outline=INK, width=7)
d.ellipse((22, 55, 40, 73), fill=INK)
d.text((150, 66), "? €", font=font("anton", 84), fill=RED, anchor="mm")
shadowed(tag.rotate(12, resample=Image.BICUBIC, expand=True), 300, 140)
# textes
draw_text(img, (1250, 90), "SHEIN", font("anton", 190), WHITE, anchor="ra", stroke=8, stroke_fill=(0, 0, 0), shadow=(6, 10, 12, .9))
draw_text(img, (1250, 320), "41,8 MD$", font("anton", 150), GREEN, anchor="ra", stroke=8, stroke_fill=(0, 0, 0), shadow=(6, 10, 12, .9))
# mascotte Sou
L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gfx2.mascot(L, 620, 560, 0.5, 200, "surpris", look=(-1, -1))
img.alpha_composite(L)

img.convert("RGB").save(OUT, quality=95)
img.convert("RGB").resize((320, 180), Image.LANCZOS).save(OUT.replace(".png", "_mobile.png"))
print("ok")
