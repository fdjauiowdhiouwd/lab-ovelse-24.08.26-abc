import sys, json, soundfile as sf
from kokoro_onnx import Kokoro
m, cfg, out = sys.argv[1], sys.argv[2], sys.argv[3]
c = json.load(open(cfg)); k = Kokoro(m+"/kokoro-v1.0.onnx", m+"/voices-v1.0.bin")
for p in c:
    for i,t in enumerate(p["lines"]):
        a, sr = k.create(t, voice=p["voice"], speed=p["speed"], lang=p.get("lang","en-us"))
        sf.write(f"{out}/{p['name']}_{i}.wav", a, sr); print(p["name"], i, round(len(a)/sr,2))
