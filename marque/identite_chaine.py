# Photo de profil (800x800) et bannière (2560x1440) de la chaîne « L'Envers du Business »
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from style import *

OUTDIR = sys.argv[1] if len(sys.argv) > 1 else "."

def monogram(size):
    """Emblème : « E » retourné (l'envers) en blanc + « B » jaune, dans un anneau jaune."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lw = max(3, size // 34)
    d.ellipse((lw, lw, size - lw, size - lw), outline=YELLOW, width=lw)
    f = font("anton", int(size * 0.58))
    e = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(e).text((size * 0.5, size * 0.5), "E", font=f, fill=WHITE, anchor="mm")
    e = e.transpose(Image.FLIP_LEFT_RIGHT)
    bb = e.getbbox(); e = e.crop(bb)
    b = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(b).text((size * 0.5, size * 0.5), "B", font=f, fill=YELLOW, anchor="mm")
    bb2 = b.getbbox(); b = b.crop(bb2)
    gap = int(size * 0.035)
    tw = e.width + gap + b.width
    x = (size - tw) // 2; y = (size - e.height) // 2
    im.alpha_composite(e, (x, y)); im.alpha_composite(b, (x + e.width + gap, y))
    return im

def tag_icon(size, fill, text_fill, label="EB", angle=-12):
    """Étiquette de prix stylisée avec le monogramme : l'emblème de la chaîne."""
    TW, TH = int(size * 1.0), int(size * 0.62)
    pad = int(size * 0.2)
    im = Image.new("RGBA", (TW + 2 * pad, TH + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ox, oy = pad, pad
    notch = int(TH * 0.42)
    d.polygon([(ox + notch, oy), (ox + TW, oy), (ox + TW, oy + TH), (ox + notch, oy + TH), (ox, oy + TH // 2)], fill=fill)
    d.rounded_rectangle((ox + notch, oy, ox + TW, oy + TH), int(TH * 0.12), fill=fill)
    hr = int(TH * 0.075)
    hx, hy = ox + int(notch * 0.62), oy + TH // 2
    d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=BG)
    f = font("anton", int(TH * 0.78))
    d.text((ox + notch + (TW - notch) * 0.48, oy + TH / 2 + TH * 0.02), label, font=f, fill=text_fill, anchor="mm")
    return im.rotate(angle, resample=Image.BICUBIC, expand=True)

def radial_bg(W, H, spots):
    yy, xx = np.mgrid[0:H, 0:W]
    base = np.array(BG, float)[None, None, :].repeat(H, 0).repeat(W, 1)
    arr = base.copy()
    for cx, cy, r, col, k in spots:
        g = np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1) ** 2 * k
        arr += g[..., None] * (np.array(col, float) - base)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

# ---------- photo de profil ----------
S = 800
pp = radial_bg(S, S, [(400, 400, 520, (60, 50, 0), 0.9)])
icon = monogram(640)
pp.alpha_composite(icon, ((S - icon.width) // 2, (S - icon.height) // 2))
pp.convert("RGB").save(f"{OUTDIR}/photo_profil.png")
# aperçu rond en petit, comme sur YouTube
m = Image.new("L", (S, S), 0); ImageDraw.Draw(m).ellipse((0, 0, S, S), fill=255)
prev = Image.new("RGBA", (S, S), (255, 255, 255, 255)); prev.paste(pp, (0, 0), m)
prev.resize((88, 88), Image.LANCZOS).save(f"{OUTDIR}/photo_profil_apercu.png")

# ---------- bannière ----------
W, H = 2560, 1440
bn = radial_bg(W, H, [(1280, 720, 1100, (55, 46, 0), 0.7), (2000, 900, 700, (120, 20, 14), 0.5)])
d = ImageDraw.Draw(bn)
for x in range(0, W, 80):
    d.line([(x, 0), (x, H)], fill=(20, 20, 27))
for y in range(0, H, 80):
    d.line([(0, y), (W, y)], fill=(20, 20, 27))
# courbes de prix décoratives en fond
rng = np.random.default_rng(7)
for col, base_y, amp in [((90, 24, 20), 1000, 160), ((70, 60, 10), 880, 120)]:
    pts = []; y = base_y
    for x in range(-40, W + 80, 120):
        y += rng.normal(-6, 38); pts.append((x, y))
    d.line(pts, fill=col, width=6, joint="curve")
# zone sûre (visible sur tous les écrans) : 1546 x 423 centrée
cx, cy = W // 2, H // 2
icon = monogram(186)
f1 = font("anton", 138)
tw, th, _ = text_size(d, "L’ENVERS DU BUSINESS", f1)
total = icon.width + 30 + tw
x0 = cx - total // 2
bn.alpha_composite(icon, (x0, cy - icon.height // 2 - 40))
draw_text(bn, (x0 + icon.width + 30, cy - 40), "L’ENVERS DU BUSINESS", f1, WHITE, anchor="lm",
          shadow=(6, 8, 12, 0.8))
d = ImageDraw.Draw(bn)
f2 = font("semi", 50)
draw_text(bn, (cx, cy + 95), "Comment les entreprises gagnent VRAIMENT leur argent", f2, YELLOW, anchor="mm")
f3 = font("med", 40)
draw_text(bn, (cx, cy + 160), "Nouvelle vidéo chaque mardi et vendredi", f3, GREY, anchor="mm")
bn.convert("RGB").save(f"{OUTDIR}/banniere.png")
# aperçu de la zone sûre (ce qu'on voit sur téléphone)
bn.crop((cx - 773, cy - 211, cx + 773, cy + 212)).convert("RGB").save(f"{OUTDIR}/banniere_zone_mobile.png")
print("ok")
