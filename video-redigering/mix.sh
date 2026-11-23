#!/bin/bash
# usage: mix.sh VIDEO VOICEOVER MUSIC START_SECONDS OUT
V=$1; VO=$2; M=$3; ST=$4; OUT=$5
ffmpeg -v error -y -i "$V" -i "$VO" -ss "$ST" -t 16.5 -i "$M" -filter_complex "
[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:16,asetpts=PTS-STARTPTS,
 afade=t=in:d=0.4,afade=t=out:st=14.2:d=1.8,volume=1.1[mus];
[1:a]asplit[vo1][vo2];
[mus][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=15:release=250:makeup=1[duck];
[duck][vo1]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1:LRA=9[out]" \
 -map 0:v -map "[out]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
