# Sous-titres .srt depuis le minutage mot par mot, nombres écrits en chiffres
import json, re, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
W = json.load(open(f"{D}/words.json")); LEAD = 0.3
REP = [("Quarante et un virgule huit milliards", "41,8 milliards"), ("quarante et un virgule huit", "41,8"), ("trente-deux milliards", "32 milliards"),
       ("trente-huit virgule sept", "38,7"), ("trois virgule quatre milliards", "3,4 milliards"), ("deux virgule zéro six", "2,06"),
       ("quarante pour cent", "40 %"), ("cent ou deux cents", "100 ou 200"), ("huit fois", "8 fois"),
       ("quatre-vingt-dix-huit milliards", "98 milliards"), ("soixante-quatre milliards", "64 milliards"), ("vingt-six milliards", "26 milliards"),
       ("neuf pour cent", "9 %"), ("quarante millions", "40 millions"), ("vingt-deux millions", "22 millions"), ("trois mois", "3 mois"),
       ("dix-neuf décembre", "19 décembre"), ("vingt euros", "20 euros")]
def norm(w): return re.sub(r"[^\w'-]", "", w.lower())
toks = [list(x) for x in W]  # [section, mot, début, fin]
for src, dst in REP:
    pat = [norm(x) for x in src.split()]
    i = 0
    while i <= len(toks) - len(pat):
        if [norm(t[1]) for t in toks[i:i + len(pat)]] == pat:
            last = toks[i + len(pat) - 1][1]
            tail = re.sub(r"^[\w'-]+", "", last.split()[-1]) if re.search(r"[^\w'-]$", last) else ""
            pre = re.match(r"^[^\w'-]*", toks[i][1]).group(0)
            dst_c = dst[0].upper() + dst[1:] if toks[i][1][len(pre):][:1].isupper() else dst
            toks[i:i + len(pat)] = [[toks[i][0], pre + dst_c + tail, toks[i][2], toks[i + len(pat) - 1][3]]]
        i += 1
def ts(x):
    ms = int(round(x * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
cues, cur = [], []
for i, (sec, w, a, b) in enumerate(toks):
    cur.append((w, a, b)); txt = " ".join(x[0] for x in cur)
    nxt = toks[i + 1] if i + 1 < len(toks) else None
    if (nxt is None or nxt[0] != sec or w[-1] in ".?!…:" or (len(txt) >= 34 and w[-1] in ",;»")
            or len(txt) >= 50 or (nxt and nxt[2] - b > .6)):
        cues.append([cur[0][1] + LEAD, cur[-1][2] + LEAD, txt]); cur = []
# fusionne les morceaux trop courts avec le suivant
m = []
for c in cues:
    if m and len(m[-1][2]) < 14 and len(m[-1][2] + c[2]) < 56 and c[0] - m[-1][1] < .4: m[-1] = [m[-1][0], c[1], m[-1][2] + " " + c[2]]
    else: m.append(c)
out = []
for k, (a, b, t) in enumerate(m):
    t = re.sub(r" ([?!:;»])", " \\1", t).replace("« ", "« ")
    nb = m[k + 1][0] if k + 1 < len(m) else b + 1
    out.append(f"{k + 1}\n{ts(a)} --> {ts(min(b + .25, nb - .02))}\n{t}\n")
open(f"{D}/sous_titres.srt", "w").write("\n".join(out))
print(len(m), "sous-titres")
