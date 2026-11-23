import React from 'react';
import {Composition} from 'remotion';
import {Ad, AdProps} from './Ad';
const def: AdProps = {lines: [], starts: [], durs: [], accent: '#1f5b2e', text: '#ffffff', hl: '#e07a2e', beats: []};
export const Root: React.FC = () => (
  <Composition id="Ad" component={Ad as any} durationInFrames={480} fps={30} width={1080} height={1920} defaultProps={def} />
);
