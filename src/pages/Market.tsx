import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkline } from '../components/charts/Sparkline';
import { Card } from '../components/ui/Card';
import { Label } from '../components/ui/Help';
import { Pct } from '../components/ui/Num';
import { COMPANIES, INDEX_NAME, SECTORS, SECTOR_IDS } from '../data/companies';
import { dayChange } from '../engine/market';
import type { SectorId } from '../engine/types';
import { useGame } from '../store/gameStore';
import { fmtInt, fmtNum } from '../utils/format';

export default function Market() {
  const stocks = useGame((s) => s.market.stocks);
  const index = useGame((s) => s.market.index);
  const positions = useGame((s) => s.positions);
  const [sector, setSector] = useState<SectorId | 'all'>('all');
  const [sort, setSort] = useState<'name' | 'change'>('name');
  const navigate = useNavigate();
  const list = COMPANIES.filter((c) => sector === 'all' || c.sector === sector)
    .map((c) => ({ c, s: stocks[c.ticker] }))
    .sort((a, b) => (sort === 'change' ? dayChange(b.s) - dayChange(a.s) : a.c.ticker.localeCompare(b.c.ticker)));
  const idxSpark = [...index.candles.slice(-30).map((k) => k.c), index.value];

  return (
    <div className="space-y-4">
      <div className="card flex flex-wrap items-center gap-4 p-4">
        <div>
          <div className="text-xs text-slate-400">
            <Label term="indice">{INDEX_NAME}</Label>
          </div>
          <div className="num text-2xl font-semibold text-white">{fmtNum(index.value)}</div>
        </div>
        <Pct value={index.value / index.prevClose - 1} className="text-lg" />
        <div className="ml-auto">
          <Sparkline values={idxSpark} width={180} height={44} />
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <button onClick={() => setSector('all')} className={`chip ${sector === 'all' ? 'border-accent bg-accent/15 text-white' : 'text-slate-400'}`}>
          Tous
        </button>
        {SECTOR_IDS.map((id) => (
          <button key={id} onClick={() => setSector(id)} className={`chip ${sector === id ? 'border-accent bg-accent/15 text-white' : 'text-slate-400'}`}>
            {SECTORS[id].emoji} {SECTORS[id].label}
          </button>
        ))}
        <select className="input ml-auto w-auto py-1 font-sans text-xs" value={sort} onChange={(e) => setSort(e.target.value as 'name' | 'change')}>
          <option value="name">Trier par nom</option>
          <option value="change">Trier par variation</option>
        </select>
      </div>

      <Card className="overflow-hidden [&>div]:p-0" tour="market-list">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[560px]">
            <thead className="border-b border-line">
              <tr>
                <th className="th">Action</th>
                <th className="th hidden sm:table-cell">Secteur</th>
                <th className="th text-right">
                  <Label term="cours">Cours</Label>
                </th>
                <th className="th text-right">Var. jour</th>
                <th className="th hidden text-right md:table-cell">
                  <Label term="volume">Volume</Label>
                </th>
                <th className="th">30 jours</th>
              </tr>
            </thead>
            <tbody>
              {list.map(({ c, s }) => (
                <tr key={c.ticker} className="cursor-pointer border-b border-line/50 transition last:border-0 hover:bg-panel2" onClick={() => navigate(`/action/${c.ticker}`)}>
                  <td className="td">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-semibold text-white">{c.ticker}</span>
                      {positions[c.ticker] && <span className="rounded bg-accent/20 px-1 text-[10px] text-accent">détenue</span>}
                    </div>
                    <div className="text-xs text-slate-500">{c.name}</div>
                  </td>
                  <td className="td hidden text-xs text-slate-400 sm:table-cell">
                    {SECTORS[c.sector].emoji} {SECTORS[c.sector].label}
                  </td>
                  <td className="td num text-right text-slate-100">{fmtNum(s.price)} €</td>
                  <td className="td text-right">
                    <Pct value={dayChange(s)} />
                  </td>
                  <td className="td num hidden text-right text-xs text-slate-400 md:table-cell">{fmtInt(s.dayVolume)}</td>
                  <td className="td">
                    <Sparkline values={[...s.candles.slice(-30).map((k) => k.c), s.price]} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
