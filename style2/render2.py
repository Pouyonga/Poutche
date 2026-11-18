# Moteur de rendu style 2 (commun à toutes les vidéos). Une vidéo fournit : TL (début, scène, fond), TOTAL, et éventuellement des balayages.
import sys, os, subprocess, multiprocessing as mp
from gfx2 import *

FPS, LEAD = 30, 0.3
SWIPE_COLORS = [INK, SUN, CORAL, SKY, MINT, GRAPE]

def make_frame(TL):
    starts = [s for s, _, _ in TL]
    def frame(t):
        tv = t - LEAD
        i = max(k for k, s in enumerate(starts) if s <= max(tv, 0))
        s0, fn, bg = TL[i]
        img = background(bg, tv)
        cam = fn(img, tv) or (1.0, 0, 0, 0)
        img = camera(img, *cam)
        for k, s in enumerate(starts[1:], 1):
            if abs(tv - s) < .4: swipe(img, tv, s, SWIPE_COLORS[k % len(SWIPE_COLORS)], .55)
        return img
    return frame

def _work(args):
    mod, k, f0, f1, out = args
    m = __import__(mod); frame = make_frame(m.TL)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for n in range(f0, f1):
        p.stdin.write(frame(n / FPS).tobytes())
        if (n - f0) % 900 == 0: print(f"[{k}] {n - f0}/{f1 - f0}", flush=True)
    p.stdin.close(); p.wait(); return out

def run(mod, out, argv):
    m = __import__(mod)
    if "--preview" in argv:
        fr = make_frame(m.TL)
        for ts in argv[argv.index("--preview") + 1:]: fr(float(ts)).save(f"{out}_{ts}.png")
        return
    N = int(m.TOTAL * FPS); P = 4
    chunks = [(mod, k, k * N // P, (k + 1) * N // P, f"{out}.part{k}.mp4") for k in range(P)]
    with mp.Pool(P) as pool: parts = pool.map(_work, chunks)
    with open(out + ".list", "w") as f:
        for pth in parts: f.write(f"file '{os.path.abspath(pth)}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", out + ".list", "-c", "copy", out], check=True)
    for pth in parts: os.remove(pth)
    os.remove(out + ".list"); print("ok", out)

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[1])))
    run(os.path.splitext(os.path.basename(sys.argv[1]))[0], sys.argv[2], sys.argv)
