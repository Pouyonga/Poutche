# Rendu de la vidéo : python3 render.py video.mp4 [--preview t1 t2 ...]
import sys, os, subprocess, math, multiprocessing as mp
import numpy as np
from PIL import Image
from scenes_gta import *

FPS, LEAD, TOTAL = 30, 0.3, 305.5
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = None
def logo():
    global LOGO
    if LOGO is None:
        sys.path.insert(0, os.path.join(HERE, "../../marque"))
        import importlib.util
        spec = importlib.util.spec_from_file_location("ident", os.path.join(HERE, "../../marque/identite_chaine.py"))
        src = open(spec.origin).read().split("def tag_icon")[0]
        ns = {}; exec(src, ns)
        LOGO = ns["monogram"](260)
    return LOGO

TL = [(0.0, s_hook, "n"), (25.9, s_cost, "g"), (41.9, s_compare, "n"), (53.3, s_staff, "n"), (72.8, s_time, "y"),
      (89.2, s_gta5, "g"), (116.3, s_copies, "n"), (131.6, s_preorders, "g"), (145.2, s_price, "r"), (152.4, s_forecast, "y"),
      (172.2, s_jackpot, "y"), (181.5, s_online, "n"), (204.0, s_pie, "n"), (226.3, s_callback, "n"), (234.7, s_risks, "r"),
      (259.1, s_three, "n"), (276.0, s_final_quote, "g"), (281.5, lambda img, t: s_outro(img, t, logo()), "n"),
      (293.3, lambda img, t: s_endcard(img, t, logo(), 293.3), "n")]
CHAPTERS = [(25.9, "LE PARI À 1 MILLIARD"), (89.2, "LE PRÉCÉDENT"), (131.6, "LE LANCEMENT"), (172.2, "LE VRAI JACKPOT"),
            (234.7, "LES RISQUES"), (259.1, "CONCLUSION"), (281.5, None)]
XF = 0.3

def scene_frame(i, tv):
    t0, fn, bgk = TL[i]
    img = background(tv, bgk).copy()
    fn(img, tv)
    return img

def frame(t):
    tv = t - LEAD
    i = max(k for k, (s, _, _) in enumerate(TL) if s <= max(tv, 0))
    img = scene_frame(i, tv)
    if i > 0 and tv - TL[i][0] < XF:
        prev = scene_frame(i - 1, TL[i][0] - 0.01)
        img = Image.blend(prev, img, eio((tv - TL[i][0]) / XF))
    ch = None
    for s, name in CHAPTERS:
        if tv >= s: ch = name
    if ch:
        T(img, W - 110, 100, ch, "bold", 28, GREY, "rm", .85)
    return img

def worker(args):
    k, f0, f1, out = args
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for n in range(f0, f1):
        p.stdin.write(frame(n / FPS).tobytes())
        if (n - f0) % 600 == 0: print(f"[{k}] {n - f0}/{f1 - f0}", flush=True)
    p.stdin.close(); p.wait()
    return out

if __name__ == "__main__":
    out = sys.argv[1]
    if "--preview" in sys.argv:
        for ts in sys.argv[sys.argv.index("--preview") + 1:]:
            frame(float(ts)).save(f"{out}_{ts}.png")
        sys.exit()
    N = int(TOTAL * FPS); P = 4
    chunks = [(k, k * N // P, (k + 1) * N // P, f"{out}.part{k}.mp4") for k in range(P)]
    with mp.Pool(P) as pool:
        parts = pool.map(worker, chunks)
    with open(out + ".list", "w") as f:
        for pth in parts: f.write(f"file '{os.path.abspath(pth)}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", out + ".list", "-c", "copy", out], check=True)
    for pth in parts: os.remove(pth)
    os.remove(out + ".list")
    print("ok", out)
