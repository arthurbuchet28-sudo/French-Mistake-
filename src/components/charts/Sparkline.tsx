import { memo } from 'react';
import { Line, LineChart, ResponsiveContainer, YAxis } from 'recharts';

export const Sparkline = memo(function Sparkline({ values, width = 96, height = 32 }: { values: number[]; width?: number; height?: number }) {
  const up = values[values.length - 1] >= values[0];
  const data = values.map((v, i) => ({ i, v }));
  return (
    <div style={{ width, height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 2, right: 2, bottom: 2, left: 2 }}>
          <YAxis hide domain={['dataMin', 'dataMax']} />
          <Line type="monotone" dataKey="v" stroke={up ? '#22c55e' : '#ef4444'} strokeWidth={1.5} dot={false} isAnimationActive={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
});
