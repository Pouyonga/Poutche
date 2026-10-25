import sherpa_onnx, soundfile as sf, numpy as np, sys
D="/tmp/claude-0/-home-user-Poutche/27b044ee-2896-5329-a14a-3541a7fa511f/scratchpad/tts/sherpa-onnx-whisper-small/"
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=D+"small-encoder.int8.onnx",decoder=D+"small-decoder.int8.onnx",tokens=D+"small-tokens.txt",language="fr",task="transcribe",num_threads=4)
def asr(x,sr):
    if sr!=16000:
        import math
        t=np.arange(0,len(x)/sr,1/16000); x=np.interp(t,np.arange(len(x))/sr,x)
    s=rec.create_stream(); s.accept_waveform(16000,x.astype(np.float32)); rec.decode_stream(s); return s.result.text
def f0(x,sr):
    fr=int(.04*sr); out=[]
    for i in range(0,len(x)-fr,fr):
        w=x[i:i+fr]
        if np.sqrt((w**2).mean())<0.03: continue
        c=np.correlate(w,w,'full')[fr-1:]; lo,hi=int(sr/400),int(sr/70)
        k=lo+np.argmax(c[lo:hi]); 
        if c[k]>0.3*c[0]: out.append(sr/k)
    return np.median(out) if out else 0
if __name__=="__main__":
    for f in sys.argv[1:]:
        x,sr=sf.read(f); print(f, f"F0={f0(x,sr):.0f}Hz", "|", asr(x,sr))
