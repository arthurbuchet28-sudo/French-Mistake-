import { useState } from 'react';
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { WeeklyReportView } from '../components/progression/WeeklyReportView';
import { Card, Stat } from '../components/ui/Card';
import { Label } from '../components/ui/Help';
import { Money, Pct } from '../components/ui/Num';
import { Locked } from '../components/ui/Tabs';
import { COMPANY_BY_TICKER, SECTORS } from '../data/companies';
import { FEATURE_LEVEL } from '../data/levels';
import { drawdownSeries, maxDrawdown, relativePerformance, tradeStats } from '../engine/stats';
import type { SectorId } from '../engine/types';
import { useGame } from '../store/gameStore';
import { usePortfolioSummary, useUnlocked } from '../store/selectors';
import { fmtDate, fmtEur, fmtNum, fmtPctPlain } from '../utils/format';

const tooltipStyle = { background: '#182033', border: '1px solid #243049', borderRadius: 8, fontSize: 12 };

export default function Stats() {
  const tx = useGame((s) => s.transactions);
  const snapshots = useGame((s) => s.snapshots);
  const index = useGame((s) => s.market.index.value);
  const day = useGame((s) => s.market.day);
  const reports = useGame((s) => s.reports);
  const sum = usePortfolioSummary();
  const advanced = useUnlocked('advancedStats');
  const [reportIdx, setReportIdx] = useState<number | null>(null);

  const s = tradeStats(tx);
  const values = [...snapshots.map((x) => x.value), sum.total];
  const mdd = maxDrawdown(values);
  const perf = relativePerformance(snapshots[0].value, sum.total, snapshots[0].index, index);
  const closed = tx.filter((t) => t.realizedPnl !== undefined);
  const bySector: Record<string, number> = {};
  for (const t of closed) {
    const sec = COMPANY_BY_TICKER[t.ticker].sector;
    bySector[sec] = (bySector[sec] ?? 0) + (t.realizedPnl ?? 0);
  }
  const dd = drawdownSeries(values).map((v, i) => ({ label: i < snapshots.length ? fmtDate(snapshots[i].day) : fmtDate(day), dd: v * 100 }));
  const report = reportIdx !== null ? reports[reportIdx] : reports[reports.length - 1];

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Stat label={<Label term="taux-reussite">Trades gagnants</Label>} value={s.closedTrades ? fmtPctPlain(s.winRate, 0) : '—'} sub={<span className="text-slate-500">{s.wins} gagnant(s) / {s.closedTrades} clôturé(s)</span>} />
        <Stat label="Gain moyen" value={<Money value={s.avgGain} signed color />} sub={<span className="text-slate-500">soit {fmtPctPlain(s.avgGainPct)}</span>} />
        <Stat label="Perte moyenne" value={<Money value={s.avgLoss} signed color />} sub={<span className="text-slate-500">soit {fmtPctPlain(s.avgLossPct)}</span>} />
        <Stat label="Plus grosse perte" value={<Money value={s.biggestLoss} signed color />} />
        <Stat label={<Label term="drawdown">Drawdown maximum</Label>} value={<span className={mdd > 0.1 ? 'text-down' : ''}>{fmtPctPlain(-mdd)}</span>} />
        <Stat label="Ma performance" value={<Pct value={perf.portfolio} />} />
        <Stat label={<Label term="indice">Performance de l’indice</Label>} value={<Pct value={perf.index} />} />
        <Stat label="Écart vs indice" value={<Pct value={perf.excess} />} sub={<span className="text-slate-500">{perf.excess > 0 ? 'Tu bats le marché 💪' : 'Le marché fait mieux'}</span>} />
      </div>

      <Card title="📈 Statistiques avancées" right={!advanced && <Locked level={FEATURE_LEVEL.advancedStats} />}>
        {!advanced ? (
          <p className="py-6 text-center text-sm text-slate-500">
            Graphiques de P&L par trade, courbe de drawdown, résultats par secteur et ratio gain/perte : disponibles au niveau {FEATURE_LEVEL.advancedStats} « Stratégie ».
          </p>
        ) : (
          <div className="grid gap-6 lg:grid-cols-2">
            <div>
              <h3 className="mb-2 text-sm text-slate-300">P&L réalisé par trade</h3>
              {closed.length === 0 ? (
                <p className="py-8 text-center text-sm text-slate-500">Aucune vente pour l’instant.</p>
              ) : (
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={closed.map((t, i) => ({ n: i + 1, pnl: t.realizedPnl, label: `${t.ticker} ${fmtDate(t.day)}` }))}>
                    <CartesianGrid stroke="#1a2336" vertical={false} />
                    <XAxis dataKey="n" tick={{ fill: '#64748b', fontSize: 11 }} stroke="#243049" />
                    <YAxis tick={{ fill: '#64748b', fontSize: 11 }} stroke="#243049" width={50} />
                    <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [fmtEur(v), 'P&L']} labelFormatter={(_, p) => p?.[0]?.payload?.label ?? ''} />
                    <Bar dataKey="pnl" isAnimationActive={false}>
                      {closed.map((t) => (
                        <Cell key={t.id} fill={(t.realizedPnl ?? 0) >= 0 ? '#22c55e' : '#ef4444'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
            <div>
              <h3 className="mb-2 text-sm text-slate-300">
                <Label term="drawdown">Courbe de drawdown</Label>
              </h3>
              <ResponsiveContainer width="100%" height={200}>
                <AreaChart data={dd}>
                  <CartesianGrid stroke="#1a2336" vertical={false} />
                  <XAxis dataKey="label" tick={{ fill: '#64748b', fontSize: 11 }} stroke="#243049" minTickGap={40} />
                  <YAxis tick={{ fill: '#64748b', fontSize: 11 }} stroke="#243049" width={40} tickFormatter={(v) => `${v.toFixed(0)} %`} />
                  <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [`${fmtNum(v)} %`, 'Drawdown']} />
                  <Area dataKey="dd" stroke="#ef4444" fill="#ef4444" fillOpacity={0.2} isAnimationActive={false} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div>
              <h3 className="mb-2 text-sm text-slate-300">P&L réalisé par secteur</h3>
              <ul className="space-y-1.5 text-sm">
                {Object.keys(bySector).length === 0 && <li className="text-slate-500">—</li>}
                {Object.entries(bySector).map(([k, v]) => (
                  <li key={k} className="flex justify-between">
                    <span>{SECTORS[k as SectorId].emoji} {SECTORS[k as SectorId].label}</span>
                    <Money value={v} signed color />
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="mb-2 text-sm text-slate-300">Ratios</h3>
              <dl className="space-y-1.5 text-sm">
                <div className="flex justify-between"><dt className="text-slate-400">Ratio gain moyen / perte moyenne</dt><dd className="num">{s.payoffRatio ? fmtNum(s.payoffRatio) : '—'}</dd></div>
                <div className="flex justify-between"><dt className="text-slate-400">Plus gros gain</dt><dd><Money value={s.biggestGain} signed color /></dd></div>
                <div className="flex justify-between"><dt className="text-slate-400">P&L réalisé total</dt><dd><Money value={s.totalRealized} signed color /></dd></div>
                <div className="flex justify-between"><dt className="text-slate-400"><Label term="frais">Frais totaux</Label></dt><dd><Money value={s.totalFees} /></dd></div>
                <div className="flex justify-between"><dt className="text-slate-400">Frais / P&L réalisé</dt><dd className="num">{s.totalRealized > 0 ? fmtPctPlain(s.totalFees / s.totalRealized) : '—'}</dd></div>
              </dl>
            </div>
          </div>
        )}
      </Card>

      <Card
        title="📅 Bilans hebdomadaires"
        right={
          reports.length > 0 && (
            <select className="input w-auto py-1 font-sans text-xs" value={reportIdx ?? reports.length - 1} onChange={(e) => setReportIdx(Number(e.target.value))}>
              {reports.map((r, i) => (
                <option key={r.id} value={i}>
                  Semaine {r.week} ({fmtDate(r.endDay)})
                </option>
              ))}
            </select>
          )
        }
      >
        {report ? <WeeklyReportView r={report} /> : <p className="py-6 text-center text-sm text-slate-500">Le premier bilan arrive à la fin de ta première semaine simulée (5 journées de bourse).</p>}
      </Card>
    </div>
  );
}
