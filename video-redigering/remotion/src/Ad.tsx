import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, interpolate, spring, useVideoConfig, continueRender, delayRender} from 'remotion';
export type AdProps = {lines: string[]; starts: number[]; durs: number[]; accent: string; text: string; hl: string; beats: number[]};
const CUTS = [2, 5, 6, 6.5, 7, 8, 8.5, 10, 12.25];

const decay = (t: number, events: number[], k: number) =>
  events.reduce((a, e) => (t >= e ? Math.max(a, Math.exp(-(t - e) * k)) : a), 0);

export const Ad: React.FC<AdProps> = ({lines, starts, durs, accent, text, hl, beats}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const punch = decay(t, CUTS, 9);
  const pulse = decay(t, beats, 12);
  const boom = t >= 9.95 ? Math.exp(-(t - 9.95) * 6) : 0;
  const scale = 1 + 0.08 * punch + 0.018 * pulse + 0.05 * boom;
  const rot = (CUTS.findIndex(c => c > t) % 2 ? 1 : -1) * 1.2 * punch;
  const shakeX = Math.sin(frame * 2.1) * 26 * boom, shakeY = Math.cos(frame * 2.7) * 20 * boom;
  const flash = decay(t, CUTS, 30);
  // active line
  const li = starts.findIndex((s, i) => t >= s && t < s + durs[i] + 0.35);
  let caption = null;
  if (li >= 0) {
    const words = lines[li].toUpperCase().split(' ');
    const total = words.reduce((a, w) => a + w.length + 1, 0);
    let acc = 0;
    caption = (
      <div style={{position: 'absolute', bottom: t >= 12.25 ? 60 : 330, width: '100%', display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '10px 18px', padding: '0 70px', boxSizing: 'border-box'}}>
        {words.map((w, i) => {
          const wStart = starts[li] + (acc / total) * durs[li] * 0.92;
          acc += w.length + 1;
          const wEnd = starts[li] + (acc / total) * durs[li] * 0.92;
          const f0 = Math.round(wStart * fps);
          const s = spring({frame: frame - f0, fps, config: {damping: 11, stiffness: 220, mass: 0.6}});
          const active = t >= wStart && t < wEnd + 0.08;
          if (frame < f0) return <span key={i} style={{opacity: 0, fontSize: 92, fontFamily: 'Inter', fontWeight: 900}}>{w}</span>;
          return (
            <span key={i} style={{
              fontFamily: 'Inter', fontWeight: 900, fontSize: 92, lineHeight: 1.05, color: active ? '#fff' : text,
              background: active ? hl : 'transparent', borderRadius: 18, padding: '2px 14px',
              transform: `scale(${interpolate(s, [0, 1], [0.4, active ? 1.1 : 1])}) translateY(${interpolate(s, [0, 1], [40, 0])}px) rotate(${active ? -2 : 0}deg)`,
              display: 'inline-block',
              textShadow: active ? 'none' : '0 0 2px #000, 0 6px 0 #000, 4px 4px 0 #000, -4px 4px 0 #000, 4px -2px 0 #000, -4px -2px 0 #000',
              WebkitTextStroke: active ? '0' : '3px #000',
            }}>{w}</span>
          );
        })}
      </div>
    );
  }
  // shockwave ring at boom
  const ringT = t - 9.95;
  const ring = ringT > 0 && ringT < 0.6 ? (
    <div style={{position: 'absolute', left: 540, top: 1150, width: 0, height: 0}}>
      <div style={{position: 'absolute', left: -ringT * 1400, top: -ringT * 1400, width: ringT * 2800, height: ringT * 2800,
        borderRadius: '50%', border: `${interpolate(ringT, [0, 0.6], [40, 2])}px solid ${hl}`, opacity: 1 - ringT / 0.6}} />
    </div>) : null;
  const progress = Math.min(1, t / 16);
  return (
    <AbsoluteFill style={{backgroundColor: '#000', overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translate(${shakeX}px, ${shakeY}px) scale(${scale}) rotate(${rot}deg)`}}>
        <OffthreadVideo src={staticFile('ad.mp4')} muted />
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.35) 100%)'}} />
      {ring}
      {caption}
      <AbsoluteFill style={{backgroundColor: '#fff', opacity: flash * 0.6}} />
      <div style={{position: 'absolute', left: 0, bottom: 0, height: 14, width: `${progress * 100}%`, background: hl}} />
    </AbsoluteFill>
  );
};
