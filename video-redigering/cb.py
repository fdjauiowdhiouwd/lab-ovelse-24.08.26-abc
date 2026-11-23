import sys, json, time, torch, torchaudio
from chatterbox.tts import ChatterboxTTS
S=sys.argv[1]; out=S+"/cb"
torch.set_num_threads(4)
m = ChatterboxTTS.from_pretrained(device="cpu")
P={p["name"]:p for p in json.load(open(S+"/scripts/protos.json"))}
jobs=[("CB_hype",P["A_hype"]["lines"],None,0.95,0.3),
      ("CB_playful",P["B_playful"]["lines"],S+"/proto/B_playful_1.wav",0.85,0.35)]
for name,lines,ref,ex,cfg in jobs:
    for i,t in enumerate(lines):
        t0=time.time(); torch.manual_seed(7)
        w = m.generate(t, audio_prompt_path=ref, exaggeration=ex, cfg_weight=cfg) if ref else m.generate(t, exaggeration=ex, cfg_weight=cfg)
        torchaudio.save(f"{out}/{name}_{i}.wav", w, m.sr)
        print(name,i,round(w.shape[-1]/m.sr,2),"s, took",round(time.time()-t0),"s",flush=True)
