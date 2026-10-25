import soundfile as sf, numpy as np, sys
from piper import PiperVoice, SynthesisConfig
v=PiperVoice.load(sys.argv[1]+"/vits-piper-fr_FR-tom-medium/fr_FR-tom-medium.onnx")
SR=v.config.sample_rate
def gen(txt, sp):
    cfg=SynthesisConfig(length_scale=1/sp)
    return np.concatenate([c.audio_float_array for c in v.synthesize(txt, syn_config=cfg)]).astype(np.float32)
# (slot_start, slot_end, spoken text)
LINES=[
 (0.10, 2.95, "Cet homme a payé deux pizzas... des centaines de millions d'euros."),
 (3.10, 4.55, "Mai deux mille dix."),
 (4.60, 6.55, "Le bitcoin vient à peine de naître."),
 (6.60, 9.05, "Il ne vaut presque rien : moins d'un centime."),
 (9.10, 11.90, "Et personne ne s'en sert pour acheter quoi que ce soit."),
 (12.10, 14.55, "Lasslo Hanièts, un programmeur de Floride,"),
 (14.60, 16.15, "poste un message sur un forum :"),
 (16.20, 19.20, "dix mille bitcoins, pour deux pizzas."),
 (19.30, 20.85, "Quatre jours passent..."),
 (20.90, 22.85, "Puis un étudiant de dix-neuf ans accepte."),
 (22.90, 24.95, "Lasslo envoie ses dix mille bitcoins."),
 (25.00, 26.35, "Les pizzas arrivent."),
 (26.40, 28.00, "Le tout premier achat en bitcoin."),
 (28.10, 30.35, "À l'époque, ça valait quarante et un dollars."),
 (30.40, 31.75, "Aujourd'hui ?"),
 (31.80, 35.90, "Ces bitcoins vaudraient plus d'un demi-milliard d'euros."),
 (36.10, 38.05, "Et toi, tu les aurais gardés ?"),
 (38.10, 39.95, "Abonne-toi pour plus d'histoires d'argent."),
]
mode=sys.argv[2]
out=np.zeros(int(40*SR),np.float32); timings=[]
def trim(x):
    idx=np.where(np.abs(x)>0.01)[0]; return x[max(0,idx[0]-200):idx[-1]+600]
prev_end=0.0
for k,(a,b,txt) in enumerate(LINES):
    st=max(a-0.3, prev_end+0.12)
    lim=(LINES[k+1][0]+0.15) if k+1<len(LINES) else 39.9
    sp=1.1
    for _ in range(6):
        x=trim(gen(txt,sp)); dur=len(x)/SR
        if st+dur<=lim or sp>=1.3: break
        sp=min(1.3, sp*dur/(lim-st))
    timings.append((st, st+dur, sp, txt))
    i=int(st*SR); out[i:i+len(x)]+=x[:len(out)-i]
    prev_end=st+dur
    print(f"{st:6.2f} {st+dur:6.2f}  slot {a:5.2f}-{b:5.2f}  x{sp:.2f}  {txt}")
import json; json.dump(timings, open("timings.json","w"))
if mode=="write":
    out/=max(1e-6,np.abs(out).max()); out*=0.89
    sf.write(sys.argv[3],out,SR)
