import torch, torch.nn as nn, torch.nn.functional as F, numpy as np
from scipy import signal
class W2V(nn.Module):
    def __init__(s):
        super().__init__()
        ks=[(10,5),(3,2),(3,2),(3,2),(3,2),(2,2),(2,2)]
        s.fe=nn.ModuleList()
        for i,(k,st) in enumerate(ks):
            s.fe.append(nn.Conv1d(1 if i==0 else 512,512,k,st,bias=False))
        s.gn=nn.GroupNorm(512,512)
        s.ln=nn.LayerNorm(512); s.proj=nn.Linear(512,768)
        s.pos=nn.utils.parametrizations.weight_norm(nn.Conv1d(768,768,128,padding=64,groups=16),dim=2) if False else None
        s.pos_w=None
        s.enc_ln=nn.LayerNorm(768)
        s.layers=nn.ModuleList([nn.ModuleDict(dict(q=nn.Linear(768,768),k=nn.Linear(768,768),v=nn.Linear(768,768),o=nn.Linear(768,768),
            ln1=nn.LayerNorm(768),fc1=nn.Linear(768,3072),fc2=nn.Linear(3072,768),ln2=nn.LayerNorm(768))) for _ in range(12)])
    def forward(s,x):
        x=x[:,None]
        for i,c in enumerate(s.fe):
            x=c(x)
            if i==0: x=s.gn(x)
            x=F.gelu(x)
        x=x.transpose(1,2); x=s.ln(x); x=s.proj(x)
        p=F.conv1d(x.transpose(1,2),s.pos_weight,s.pos_bias,padding=64,groups=16)[:,:,:-1]
        x=x+F.gelu(p).transpose(1,2)
        x=s.enc_ln(x)
        B,T,_=x.shape
        for L in s.layers:
            r=x
            q=L['q'](x).view(B,T,12,64).transpose(1,2)*(64**-.5); k=L['k'](x).view(B,T,12,64).transpose(1,2); v=L['v'](x).view(B,T,12,64).transpose(1,2)
            a=torch.softmax(q@k.transpose(-1,-2),-1)@v
            x=L['o'](a.transpose(1,2).reshape(B,T,768)); x=L['ln1'](r+x)
            r=x; x=L['fc2'](F.gelu(L['fc1'](x))); x=L['ln2'](r+x)
        return x
class UTMOS(nn.Module):
    def __init__(s,path):
        super().__init__()
        sd=torch.load(path,map_location='cpu')
        s.w=W2V()
        m={}
        for i in range(7):
            m[f'fe.{i}.weight']=sd[f'wav2vec2.feature_extractor.conv_layers.{i}.0.weight']
        m['gn.weight']=sd['wav2vec2.feature_extractor.conv_layers.0.2.weight']; m['gn.bias']=sd['wav2vec2.feature_extractor.conv_layers.0.2.bias']
        m['ln.weight']=sd['wav2vec2.layer_norm.weight']; m['ln.bias']=sd['wav2vec2.layer_norm.bias']
        m['proj.weight']=sd['wav2vec2.post_extract_proj.weight']; m['proj.bias']=sd['wav2vec2.post_extract_proj.bias']
        m['enc_ln.weight']=sd['wav2vec2.encoder.layer_norm.weight']; m['enc_ln.bias']=sd['wav2vec2.encoder.layer_norm.bias']
        mp=dict(q='self_attn.q_proj',k='self_attn.k_proj',v='self_attn.v_proj',o='self_attn.out_proj',ln1='self_attn_layer_norm',fc1='fc1',fc2='fc2',ln2='final_layer_norm')
        for i in range(12):
            for a,b in mp.items():
                for t in ('weight','bias'): m[f'layers.{i}.{a}.{t}']=sd[f'wav2vec2.encoder.layers.{i}.{b}.{t}']
        s.w.load_state_dict(m,strict=True)
        g=sd['wav2vec2.encoder.pos_conv.0.weight_g']; v=sd['wav2vec2.encoder.pos_conv.0.weight_v']
        s.w.pos_weight=g*v/v.norm(dim=(0,1),keepdim=True); s.w.pos_bias=sd['wav2vec2.encoder.pos_conv.0.bias']
        s.dom=sd['domain_emb']; s.jud=sd['judge_emb']
        s.blstm=nn.LSTM(1024,512,batch_first=True,bidirectional=True)
        s.blstm.load_state_dict({k[6:]:v for k,v in sd.items() if k.startswith('blstm.')})
        pk=sorted({int(k.split('.')[1]) for k in sd if k.startswith('projection.')})
        s.p1=nn.Linear(1024,2048); s.p2=nn.Linear(2048,1)
        s.p1.load_state_dict({'weight':sd[f'projection.{pk[0]}.weight'],'bias':sd[f'projection.{pk[0]}.bias']})
        s.p2.load_state_dict({'weight':sd[f'projection.{pk[1]}.weight'],'bias':sd[f'projection.{pk[1]}.bias']})
        s.eval()
    @torch.no_grad()
    def __call__(s,x,sr):
        if sr!=16000: x=signal.resample_poly(x,16000,sr)
        x=torch.tensor(x,dtype=torch.float32)[None]
        h=s.w(x); B,T,_=h.shape
        h=torch.cat([h,s.dom.expand(B,T,128),s.jud.expand(B,T,128)],-1)
        h,_=s.blstm(h); y=s.p2(F.relu(s.p1(h)))
        return float(y.mean()*2+3)
