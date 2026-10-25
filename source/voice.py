# Kokoro voice-over, each line fitted near its animation slot; also exports word timings
import numpy as np, soundfile as sf, json, sys, re
from kokoro_onnx import Kokoro
T=sys.argv[1]
k=Kokoro(T+'/kokoro-v1.0.onnx',T+'/voices-v1.0.bin')
sys.path.insert(0,T); from asr import asr
_sw,_on,_om=k.get_voice_style('ff_siwis'),k.get_voice_style('am_onyx'),k.get_voice_style('hm_omega')
def blend(w): return w*_sw+(1-w)/2*(_on+_om)
WEIGHTS=[.3,.35,.4,.45]
ALT={  # alternative spellings tried when a line is not understood clearly
 "Cet homme a payé deux pizzas... des centaines de millions d'euros.":["Cet homme a payé... deux pizzas. Des centaines de millions d'euros.","Cet homme, a payé deux pizzas... des centaines de millions d'euros."],
 "Lasslo envoie ses dix mille bitcoins.":["Lasslo, envoie ses dix mille bitcoins.","Lasslo envoie alors ses dix mille bitcoins."],
 "Mai, deux mille dix.":["Mai deux mille dix.","Mai... deux-mille-dix."],
 "Puis un étudiant de dix-neuf ans accepte.":["Puis, un étudiant de dix neuf ans, accepte.","Puis un étudiant, de dix-neuf ans, accepte."],
 "Et les pizzas arrivent.":["Et les pizzas... arrivent.","Et, les pizzas arrivent."],
 "Et toi... tu les aurais gardés ?":["Et toi, tu les aurais gardés ?","Et toi ? Tu les aurais gardés ?"],
 "Lasslo Hanièts, un programmeur de Floride,":["Lasslo Hanièts... un programmeur de Floride,"],
}
def nrm(s):
    s=s.lower().replace("-"," ").replace("'"," ").replace("10 000","10000").replace("\xa0","")
    return _re.sub(r"[^\w\s]"," ",s).split()
def wer(r,h):
    r,h=nrm(r),nrm(h)
    if 'programmeur' in r: r=r[r.index('programmeur'):]; h=h[h.index('programmeur'):] if 'programmeur' in h else h
    if r and r[0]=='laszlo': r=r[1:]; h=h[2:] if len(h)>2 else h
    d=np.zeros((len(r)+1,len(h)+1),int); d[:,0]=range(len(r)+1); d[0,:]=range(len(h)+1)
    for i in range(1,len(r)+1):
        for j in range(1,len(h)+1): d[i,j]=min(d[i-1,j]+1,d[i,j-1]+1,d[i-1,j-1]+(r[i-1]!=h[j-1]))
    return d[-1,-1]/max(1,len(r))
import re as _re
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
def gen(txt,sp,w=.3):
    a,sr=k.create(txt,voice=blend(w),speed=sp,lang='fr-fr'); assert sr==SR; return a.astype(np.float32)
def trim(x):
    idx=np.where(np.abs(x)>0.012)[0]; return x[max(0,idx[0]-240):idx[-1]+1200]
out=np.zeros(int(40*SR),np.float32); res=[]; prev=0.0
for i,(a,b,txt,cap) in enumerate(LINES):
    st=max(a-0.2, prev+0.08)
    lim=(LINES[i+1][0]+0.1) if i+1<len(LINES) else 39.85
    best=None
    for tv in [txt]+ALT.get(txt,[]):
        for w in WEIGHTS:
            xx=trim(gen(tv,1.05,w))
            hyp=asr(np.concatenate([np.zeros(SR//4),xx,np.zeros(SR//2)]),SR); e=wer(cap,hyp)
            if best is None or e<best[0]-1e-9: best=(e,tv,w,hyp)
            if e==0: break
        if best[0]==0: break
    e,txt,W_,hyp=best
    print(f"   choose w={W_} wer={e:.2f} '{txt}' -> {hyp}")
    sp=1.05
    for _ in range(6):
        x=trim(gen(txt,sp,W_)); d=len(x)/SR
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
