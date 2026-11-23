import sys, json, subprocess, soundfile as sf, math
S, V, M, OUTDIR = sys.argv[1:5]
P = json.load(open(S+"/scripts/protos.json"))
STARTS=[0.15,2.1,4.85,6.4,8.0,9.0,12.3]
CUTS=[2,5,6,6.5,7,8,8.5,10,12.25]
STY={
 "A_hype":dict(pitch=1.10,mstart=0.4,mvol=1.2,flash="white@0.55",punch=0.07,shake=True,col="&H00FFFFFF",out="&H00000000",bord=8,size=88,font="Inter Black",fx=""),
 "B_playful":dict(pitch=1.04,mstart=3.4,mvol=1.1,flash="0xFFE14D@0.45",punch=0.05,shake=False,col="&H004DE1FF",out="&H00202020",bord=7,size=80,font="Inter Black",fx=""),
 "C_trailer":dict(pitch=0.94,mstart=0.4,mvol=1.0,flash="black@0.7",punch=0.0,shake=False,col="&H00F0F0F0",out="&H00000000",bord=0,size=64,font="Inter ExtraBold",fx="vignette=PI/4,eq=contrast=1.08:saturation=0.9,"),
}
def ts(t): return "%d:%02d:%05.2f"%(0,int(t//60),t%60)
for p in P:
    n=p["name"]; st=STY[n]; d=f"{S}/proto"
    # --- voiceover
    ins=[]; fl=[]
    for i in range(7):
        ins+=["-i",f"{d}/{n}_{i}.wav"]
        fl.append(f"[{i}]rubberband=pitch={st['pitch']},adelay={int(STARTS[i]*1000)}:all=1[a{i}]")
    fc=";".join(fl)+";"+"".join(f"[a{i}]" for i in range(7))+"amix=inputs=7:normalize=0,apad,atrim=0:16,aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=90,equalizer=f=3500:t=q:w=1:g=4,acompressor=threshold=-20dB:ratio=5:attack=3:release=60:makeup=3,loudnorm=I=-14:TP=-1.5[vo]"
    vo=f"{d}/{n}_vo.wav"
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",fc,"-map","[vo]",vo],check=True)
    # --- captions
    ass=f"{d}/{n}.ass"
    with open(ass,"w") as f:
        f.write(f"[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        bs = 3 if st["bord"]==0 else 1
        f.write(f"Style: C,{st['font']},{st['size']},{st['col']},&H000000FF,{st['out']},&H90000000,-1,0,0,0,100,100,{2 if n=='C_trailer' else 0},0,{bs},{st['bord'] or 14},{0 if bs==3 else 4},2,90,90,300,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        for i,t in enumerate(p["lines"]):
            dur=sf.info(f"{d}/{n}_{i}.wav").duration
            a=STARTS[i]; b=min(a+dur+0.3, STARTS[i+1]-0.05 if i<6 else 15.9)
            tag="{\\fad(250,250)}" if n=="C_trailer" else "{\\fscx135\\fscy135\\t(0,130,\\fscx100\\fscy100)\\fad(0,120)}"
            txt=t.upper() if n!="C_trailer" else t
            f.write(f"Dialogue: 0,{ts(a)},{ts(b)},C,,0,0,0,,{tag}{txt}\n")
    # --- video fx
    if st["punch"]>0:
        z="1+"+"+".join(f"{st['punch']}*gte(in/30,{c})*exp(-(in/30-{c})*9)" for c in CUTS)
    else:
        z="1+0.06*(in/30)/16"
    sx="+if(gte(in/30,9.95),sin(in*2.1)*28*exp(-(in/30-9.95)*7),0)" if st["shake"] else ""
    sy="+if(gte(in/30,9.95),cos(in*2.7)*22*exp(-(in/30-9.95)*7),0)" if st["shake"] else ""
    flash=",".join(f"drawbox=x=0:y=0:w=iw:h=ih:t=fill:color={st['flash']}:enable='between(t,{c},{c+0.07})'" for c in CUTS)
    vf=(f"scale=1188:2112,zoompan=z='{z}':d=1:x='iw/2-(iw/zoom/2){sx}':y='ih/2-(ih/zoom/2){sy}':s=1080x1920:fps=30,"
        f"{st['fx']}{flash},ass={ass}:fontsdir=/usr/share/fonts/opentype/inter")
    out=f"{OUTDIR}/DuoPad_prototype_{n}.mp4"
    fc=(f"[0:v]{vf}[v];[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:16,asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st=14.2:d=1.8,volume={st['mvol']}[mus];"
        f"[1:a]asplit[v1][v2];[mus][v2]sidechaincompress=threshold=0.03:ratio=4:attack=15:release=250[duck];[duck][v1]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1:LRA=9[a]")
    subprocess.run(["ffmpeg","-v","error","-y","-i",V,"-i",vo,"-ss",str(st["mstart"]),"-t","16.5","-i",M,"-filter_complex",fc,
        "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-t","16","-movflags","+faststart",out],check=True)
    print("built",out)
