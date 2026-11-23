# usage: build_cb.py S NAME PROTO_KEY HL TXT OUTLABEL
import sys, json, subprocess, soundfile as sf
S,name,key,hl,txt,label=sys.argv[1:7]
R="/home/user/lab-ovelse-24.08.26-abc"; d=S+"/cb"
V="/root/.claude/uploads/fe2361ff-9f1d-5aad-99ba-8b235721b24b/fcac6aee-B78E4F46-8C1E-4960-9BE7-51D544B002DD.mp4"
M="/root/.claude/uploads/fe2361ff-9f1d-5aad-99ba-8b235721b24b/390817d2-v24044gl0000dblqijvog65jrmgpoa90.mp4"
STARTS=[0.15,2.1,4.85,6.4,8.0,9.0,12.3]; ENDS=STARTS[1:]+[15.85]
lines={p["name"]:p for p in json.load(open(S+"/scripts/protos.json"))}[key]["lines"]
durs=[]
for i in range(7):
    src=f"{d}/{name}_{i}.wav"; tr=f"{d}/{name}_{i}_trim.wav"
    trim="silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-af",trim,tr],check=True)
    dur=sf.info(tr).duration; slot=ENDS[i]-STARTS[i]-0.05
    if dur>slot:
        f=min(dur/slot,1.4); subprocess.run(["ffmpeg","-v","error","-y","-i",tr,"-af",f"atempo={f:.3f}",tr+".f.wav"],check=True)
        subprocess.run(["mv",tr+".f.wav",tr]); dur=sf.info(tr).duration
    durs.append(round(dur,2)); print(i,round(dur,2),"slot",round(slot,2))
ins=[]; fl=[]
for i in range(7):
    ins+=["-i",f"{d}/{name}_{i}_trim.wav"]; fl.append(f"[{i}]adelay={int(STARTS[i]*1000)}:all=1[a{i}]")
fc=";".join(fl)+";"+"".join(f"[a{i}]" for i in range(7))+"amix=inputs=7:normalize=0,apad,atrim=0:16,aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=90,equalizer=f=3500:t=q:w=1:g=3,acompressor=threshold=-20dB:ratio=4:attack=3:release=60:makeup=2,loudnorm=I=-14:TP=-1.5[vo]"
vo=f"{d}/{name}_vo.wav"; subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",fc,"-map","[vo]",vo],check=True)
beats=json.load(open(S+"/rem/props_D.json"))["beats"]
props=f"{S}/rem/props_{name}.json"
json.dump(dict(lines=lines,starts=STARTS,durs=durs,accent="#1f5b2e",text=txt,hl=hl,beats=beats),open(props,"w"))
B="/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell"
vid=f"{S}/rem/out_{name}.mp4"
subprocess.run(["npx","remotion","render","src/index.ts","Ad",vid,f"--props={props}",f"--browser-executable={B}","--muted","--crf=18","--log=error"],cwd=S+"/rem",check=True)
out=f"{R}/DuoPad_prototype_{label}.mp4"
fc=("[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:16,asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st=14.2:d=1.8,volume=1.2[mus];"
    "[1:a]asplit[v1][v2];[mus][v2]sidechaincompress=threshold=0.03:ratio=4:attack=15:release=250[duck];[duck][v1]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1:LRA=9[a]")
subprocess.run(["ffmpeg","-v","error","-y","-i",vid,"-i",vo,"-ss","0.44","-t","16.5","-i",M,"-filter_complex",fc,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-t","16","-movflags","+faststart",out],check=True)
print("built",out)
