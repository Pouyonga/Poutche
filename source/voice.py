# Kokoro voice-over, each line fitted near its animation slot; also exports word timings
import numpy as np, soundfile as sf, json, sys, re
from kokoro_onnx import Kokoro
T=sys.argv[1]
k=Kokoro(T+'/kokoro-v1.0.onnx',T+'/voices-v1.0.bin')
VOICE=k.get_voice_style('ff_siwis')
SR=24000
# (slot_start, slot_end, spoken text, caption text)
LINES=[
 (0.10, 2.95, "Cet homme a payé deux pizzas... des centaines de millions d'euros.", "Cet homme a payé deux pizzas… des centaines de millions d'euros."),
 (3.10, 4.55, "Mai, deux mille dix.", "Mai 2010."),
 (4.60, 6.55, "Le bitcoin vient à peine de naître.", "Le bitcoin vient à peine de naître."),
 (6.60, 9.05, "Il ne vaut presque rien. Même pas un centime.", "Il ne vaut presque rien. Même pas un centime."),
 (9.10, 11.90, "Et personne ne s'en sert, pour acheter quoi que ce soit.", "Et personne ne s'en sert pour acheter quoi que ce soit."),
 (12.10, 14.55, "Lasslo Hanièts, un programmeur de Floride,", "Laszlo Hanyecz, un programmeur de Floride,"),
 (14.60, 16.15, "poste un message sur un forum :", "poste un message sur un forum :"),
 (16.20, 19.20, "dix mille bitcoins... pour deux pizzas.", "10 000 bitcoins… pour deux pizzas."),
 (19.30, 20.85, "Quatre jours passent...", "Quatre jours passent…"),
 (20.90, 22.85, "Puis un étudiant de dix-neuf ans accepte.", "Puis un étudiant de 19 ans accepte."),
 (22.90, 24.95, "Lasslo envoie ses dix mille bitcoins.", "Laszlo envoie ses 10 000 bitcoins."),
 (25.00, 26.35, "Et les pizzas arrivent.", "Et les pizzas arrivent."),
 (26.40, 28.00, "Le tout premier achat en bitcoin.", "Le tout premier achat en bitcoin."),
 (28.10, 30.35, "À l'époque, ça valait quarante et un dollars.", "À l'époque, ça valait 41 dollars."),
 (30.40, 31.75, "Aujourd'hui ?", "Aujourd'hui ?"),
 (31.80, 35.90, "Ces bitcoins vaudraient plus d'un demi-milliard d'euros.", "Ces bitcoins vaudraient plus d'un demi-milliard d'euros."),
 (36.10, 38.05, "Et toi... tu les aurais gardés ?", "Et toi, tu les aurais gardés ?"),
 (38.10, 39.95, "Abonne-toi, pour plus d'histoires d'argent.", "Abonne-toi pour plus d'histoires d'argent."),
]
def gen(txt,sp):
    a,sr=k.create(txt,voice=VOICE,speed=sp,lang='fr-fr'); assert sr==SR; return a.astype(np.float32)
def trim(x):
    idx=np.where(np.abs(x)>0.012)[0]; return x[max(0,idx[0]-240):idx[-1]+1200]
out=np.zeros(int(40*SR),np.float32); res=[]; prev=0.0
for i,(a,b,txt,cap) in enumerate(LINES):
    st=max(a, prev+0.1)
    lim=(LINES[i+1][0]+0.15) if i+1<len(LINES) else 39.85
    sp=1.05
    for _ in range(6):
        x=trim(gen(txt,sp)); d=len(x)/SR
        if st+d<=lim or sp>=1.28: break
        sp=min(1.28, sp*d/(lim-st))
    j=int(st*SR); out[j:j+len(x)]+=x[:len(out)-j]
    # word timing estimate: split caption words, weight by letters + punctuation pauses, inside voiced span
    env=np.convolve(np.abs(x),np.ones(240)/240,'same'); voiced=np.where(env>0.02)[0]
    v0,v1=voiced[0]/SR, voiced[-1]/SR
    words=cap.replace('10 000','10\xa0000').split(' '); wts=[]
    for w in words:
        n=len(re.sub(r"[^\wÀ-ÿ0-9]","",w)) or 1
        if w.startswith("10\xa0"): n=8
        wts.append(n+2.2)
    pauses=[1.8 if re.search(r"[,:….?»]$",w) else 0 for w in words]
    tot=sum(wts)+sum(pauses[:-1]); tcur=v0; wt=[]
    for w,ww,p in zip(words,wts,pauses):
        dd=(v1-v0)*ww/tot; wt.append((round(st+tcur,3),round(st+tcur+dd,3),w)); tcur+=dd+(v1-v0)*p/tot
    res.append(dict(start=st,end=st+d,speed=sp,cap=cap,words=wt))
    prev=st+d
    print(f"{st:6.2f}-{st+d:6.2f} slot {a:5.2f}-{b:5.2f} x{sp:.2f} {txt}")
json.dump(res,open(sys.argv[2]+'.json','w'),ensure_ascii=False,indent=0)
sf.write(sys.argv[2]+'.wav',out,SR)
