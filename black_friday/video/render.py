# Rendu de la vidéo : python3 render.py video.mp4 [--preview t1 t2 ...]
import sys, os, subprocess, math, multiprocessing as mp
import numpy as np
from PIL import Image
from scenes import *

FPS, LEAD, TOTAL = 30, 0.3, 404.0
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

TL = [(0.0, s_tag_intro, "r"), (4.45, s_chart_intro, "n"), (12.25, s_one_in_three, "r"), (17.95, s_question, "y"),
      (26.6, s_philly, "s"), (31.4, s_crowd, "n"), (42.4, s_police, "n"), (52.7, s_big_friday, "y"), (59.6, s_ledger, "n"),
      (72.6, s_atlantic, "n"), (83.0, s_usa_counter, "n"), (96.85, s_bars, "n"), (106.95, s_france, "n"), (116.2, s_but, "y"),
      (129.8, s_basket, "n"), (139.5, s_ch1, "y"), (146.85, s_loss_leader, "n"), (173.6, s_rule, "n"), (186.5, s_chart_ufc, "n"),
      (202.95, s_fake_ref, "n"), (214.5, s_urgency, "r"), (233.7, s_ch2, "y"), (241.55, s_bnpl, "n"), (249.4, s_balance, "n"),
      (259.95, s_who_paid, "n"), (269.1, s_ch3, "y"), (276.15, s_ads, "n"), (289.25, s_data, "n"), (302.0, s_and_you, "g"),
      (312.9, s_rules, "n"), (340.7, s_joko, "g"), (355.7, s_conclusion, "y"), (365.55, s_recap, "n"), (374.45, s_quote, "y"),
      (380.0, lambda img, t: s_outro(img, t, logo()), "n"), (392.3, lambda img, t: s_endcard(img, t, logo(), 392.3), "n")]
CHAPTERS = [(26.6, "ORIGINES"), (83.0, "LES CHIFFRES"), (139.5, None), (146.85, "GAGNANT N°1 · LE MAGASIN"), (233.7, None),
            (241.55, "GAGNANT N°2 · LE CRÉDIT"), (269.1, None), (276.15, "GAGNANT N°3 · LES PLATEFORMES"), (302.0, "ET TOI ?"),
            (355.7, "CONCLUSION"), (380.0, None)]
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
