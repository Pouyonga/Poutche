# Sous-titres .srt depuis le minutage mot par mot, nombres écrits en chiffres
import json, re, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
W = json.load(open(f"{D}/words.json")); LEAD = 0.3
REP = [("moins trente-cinq pour cent", "-35 %"), ("d'environ trois pour cent", "d'environ 3 %"), ("six pour cent", "6 %"),
       ("onze virgule huit milliards", "11,8 milliards"), ("quatorze milliards", "14 milliards"),
       ("quarante-quatre milliards", "44 milliards"), ("deux cents milliards", "200 milliards"),
       ("deux cent cinquante-neuf euros", "259 euros"), ("quatre cents euros", "400 euros"), ("trente jours", "30 jours"),
       ("quatre fois cent euros", "4 × 100 euros"), ("dix minutes", "10 minutes"), ("années soixante", "années 1960"),
       ("Quarante personnes", "40 personnes"), ("trois en stock", "3 en stock"), ("paiement en trois ou quatre fois", "paiement en 3 ou 4 fois")]
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
