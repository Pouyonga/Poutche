# Rendu de la vidéo : python3 render.py video.mp4 [--preview t1 t2 ...]
import sys, os, subprocess, math, multiprocessing as mp
import numpy as np
from PIL import Image
from scenes_mc import *

FPS, LEAD, TOTAL = 30, 0.3, 445.0
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

TL = [(0.0, s_hook, "n"), (14.2, s_secret, "n"), (28.8, s_world, "n"), (48.4, s_two_cols, "n"), (67.5, s_question, "y"),
      (75.1, s_stand, "s"), (88.4, s_kroc, "s"), (104.5, s_problem, "s"), (118.8, s_sonneborn, "s"), (133.7, s_quote, "y"),
      (140.3, s_cheque, "s"), (159.7, s_flows, "n"), (187.8, s_gauges, "n"), (201.4, s_rent_roy, "n"), (215.2, s_margins, "g"),
      (256.2, s_risks, "n"), (270.4, s_value, "g"), (280.1, s_control, "n"), (295.6, s_opinc, "g"), (315.2, s_nuance, "n"),
      (328.6, s_cycle, "y"), (347.1, s_france, "n"), (355.9, s_receipt, "r"), (379.6, s_bait, "n"), (392.6, s_lesson, "y"),
      (399.4, s_cards, "n"), (424.5, lambda img, t: s_outro_mc(img, t, logo()), "n"), (433.4, lambda img, t: s_endcard(img, t, logo(), 433.4), "n")]
CHAPTERS = [(28.8, "LE PARADOXE"), (75.1, "L'HISTOIRE"), (159.7, "LE SYSTÈME"), (215.2, "LE CHIFFRE CLÉ"), (256.2, "POURQUOI ÇA MARCHE"),
            (347.1, "EN FRANCE"), (379.6, "CONCLUSION"), (424.5, None)]
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
