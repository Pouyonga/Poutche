import json,urllib.request,os,sys
H={'xi-api-key':'proxy-injected','Content-Type':'application/json'}
def post(url,body,out):
    if os.path.exists(out) and os.path.getsize(out)>1000: print('skip',out); return
    try:
        r=urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(body).encode(),headers=H),timeout=600)
        open(out,'wb').write(r.read()); print('ok',out,os.path.getsize(out))
    except urllib.error.HTTPError as e: print('ERR',out,e.code,e.read()[:300])
M='https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192'
post(M,{'prompt':'Instrumental only, no vocals. Modern investigative documentary underscore for a YouTube business explainer. Minimal, tense but elegant: soft pulsing synth bass, muted plucks, light ticking hi-hats, warm pads, subtle piano motif. Steady 95 BPM, consistent energy, no big drops, leaves room for a narrator voice. Loopable.','music_length_ms':200000,'force_instrumental':True},'audio/musique_a.mp3')
post(M,{'prompt':'Instrumental only, no vocals. Curious, slightly playful documentary background for an economics explainer: pizzicato strings, marimba, soft electronic beat, light bass, optimistic but restrained, 100 BPM, steady, leaves space for narration. Loopable.','music_length_ms':200000,'force_instrumental':True},'audio/musique_b.mp3')
S='https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_192'
for name,txt,d in [
 ('whoosh','fast clean cinematic whoosh transition, airy, short',1.0),
 ('impact','deep cinematic boom impact hit with short tail, clean',1.5),
 ('ching','cash register ka-ching with coin bell, crisp',1.2),
 ('pop','soft UI pop click, satisfying, short',0.5),
 ('tick','single clock tick, crisp mechanical',0.5),
 ('scratch','marker pen strike-through scribble on paper, quick',0.8),
 ('riser','short tension riser swelling up, 2 seconds, cinematic',2.0),
 ('typewriter','short burst of typewriter keys typing',1.5),
 ('crowd','busy city street crowd and car horns ambience, 1960s',4.0),
 ('notif','smartphone notification ding, modern, short',0.6),
]:
    post(S,{'text':txt,'duration_seconds':d,'prompt_influence':0.6},f'audio/sfx_{name}.mp3')
