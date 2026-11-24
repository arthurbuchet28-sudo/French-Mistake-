import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import type { Snapshot } from '../../engine/stats';
import { fmtDate, fmtNum } from '../../utils/format';

/** Courbe du portefeuille comparée à l'indice, base 100 au début de la partie */
export function PortfolioVsIndexChart({ snapshots, live, height = 260 }: { snapshots: Snapshot[]; live: Snapshot; height?: number }) {
  const all = [...snapshots, live];
  const v0 = all[0].value || 1;
  const i0 = all[0].index || 1;
  const data = all.map((s, k) => ({
    label: k === all.length - 1 ? 'Maintenant' : fmtDate(s.day),
    portefeuille: (s.value / v0) * 100,
    indice: (s.index / i0) * 100,
  }));
  if (all.length < 3) {
    return (
      <div className="flex items-center justify-center text-center text-sm text-slate-500" style={{ height }}>
        La courbe se dessine au fil des journées de bourse.
        <br />
        Astuce : accélère le temps (x5, x20) ou avance d’une journée.
      </div>
    );
  }
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -12 }}>
        <CartesianGrid stroke="#1a2336" vertical={false} />
        <XAxis dataKey="label" tick={{ fill: '#64748b', fontSize: 11 }} minTickGap={40} stroke="#243049" />
        <YAxis domain={['auto', 'auto']} tick={{ fill: '#64748b', fontSize: 11 }} stroke="#243049" tickFormatter={(v) => fmtNum(v)} width={56} />
        <Tooltip
          contentStyle={{ background: '#182033', border: '1px solid #243049', borderRadius: 8, fontSize: 12 }}
          formatter={(v: number, name) => [fmtNum(v), name === 'portefeuille' ? 'Portefeuille' : 'INDEX 15']}
        />
        <Legend formatter={(v) => (v === 'portefeuille' ? 'Mon portefeuille' : 'INDEX 15')} wrapperStyle={{ fontSize: 12 }} />
        <Line type="monotone" dataKey="portefeuille" stroke="#3b82f6" strokeWidth={2} dot={false} isAnimationActive={false} />
        <Line type="monotone" dataKey="indice" stroke="#94a3b8" strokeDasharray="4 3" strokeWidth={1.5} dot={false} isAnimationActive={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}
