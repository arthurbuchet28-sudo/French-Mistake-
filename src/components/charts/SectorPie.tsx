import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';
import { fmtEur, fmtPctPlain } from '../../utils/format';

export interface Slice {
  name: string;
  value: number;
  color: string;
}

export function SectorPie({ data, height = 240 }: { data: Slice[]; height?: number }) {
  const total = data.reduce((a, b) => a + b.value, 0);
  if (total <= 0) return <div className="py-10 text-center text-sm text-slate-500">Aucune position pour l’instant.</div>;
  return (
    <div className="flex flex-col items-center gap-4 sm:flex-row">
      <div className="h-[200px] w-full sm:w-1/2" style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" innerRadius="55%" outerRadius="90%" paddingAngle={2} isAnimationActive={false} stroke="none">
              {data.map((d) => (
                <Cell key={d.name} fill={d.color} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{ background: '#182033', border: '1px solid #243049', borderRadius: 8, fontSize: 12 }}
              itemStyle={{ color: '#e2e8f0' }}
              formatter={(v: number, n) => [`${fmtEur(v)} (${fmtPctPlain(v / total)})`, n]}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <ul className="w-full space-y-1.5 sm:w-1/2">
        {[...data]
          .sort((a, b) => b.value - a.value)
          .map((d) => (
            <li key={d.name} className="flex items-center gap-2 text-sm">
              <span className="h-2.5 w-2.5 rounded-full" style={{ background: d.color }} />
              <span className="flex-1 text-slate-300">{d.name}</span>
              <span className="num text-slate-400">{fmtPctPlain(d.value / total)}</span>
            </li>
          ))}
      </ul>
    </div>
  );
}
