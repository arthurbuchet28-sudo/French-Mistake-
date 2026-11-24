import { Link } from 'react-router-dom';
import { SectorPie } from '../components/charts/SectorPie';
import { Card, Stat } from '../components/ui/Card';
import { Label } from '../components/ui/Help';
import { Money, Pct } from '../components/ui/Num';
import { COMPANY_BY_TICKER, SECTORS } from '../data/companies';
import { sectorExposure } from '../engine/coach';
import { marketValue, unrealizedPnl, unrealizedPct } from '../engine/trading';
import type { SectorId } from '../engine/types';
import { useGame } from '../store/gameStore';
import { labelOrderType } from '../store/logic';
import { usePortfolioSummary, usePrices } from '../store/selectors';
import { fmtDate, fmtNum, fmtPctPlain } from '../utils/format';

export default function Portfolio() {
  const positions = useGame((s) => s.positions);
  const orders = useGame((s) => s.orders);
  const cancelOrder = useGame((s) => s.cancelOrder);
  const prices = usePrices();
  const sum = usePortfolioSummary();
  const list = Object.values(positions).sort((a, b) => Math.abs(marketValue(b, prices[b.ticker])) - Math.abs(marketValue(a, prices[a.ticker])));
  const totalLatent = list.reduce((a, p) => a + unrealizedPnl(p, prices[p.ticker]), 0);
  const exp = sectorExposure(positions, prices);
  const pie = [
    ...(Object.entries(exp) as [SectorId, number][]).map(([k, v]) => ({ name: SECTORS[k].label, value: v, color: SECTORS[k].color })),
    ...(sum.cash > 0 ? [{ name: 'Liquidités', value: sum.cash, color: '#334155' }] : []),
  ];

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4" data-tour="portfolio-summary">
        <Stat label={<Label term="portefeuille">Valeur totale</Label>} value={<Money value={sum.total} />} />
        <Stat label={<Label term="liquidites">Liquidités</Label>} value={<Money value={sum.cash} />} />
        <Stat label="Investi" value={<Money value={sum.invested} />} sub={<span className="text-slate-500">{fmtPctPlain(sum.total ? sum.invested / sum.total : 0)} du total</span>} />
        <Stat label={<Label term="latent">Plus/moins-value latente</Label>} value={<Money value={totalLatent} signed color />} sub={<span className="text-slate-500">depuis le début : <Pct value={sum.totalPct} /></span>} />
      </div>

      <Card title="Mes positions" className="[&>div]:p-0">
        {list.length === 0 ? (
          <p className="p-8 text-center text-sm text-slate-500">
            Aucune position. <Link to="/marche" className="text-accent hover:underline">Va sur le marché</Link> pour acheter tes premières actions.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px]">
              <thead className="border-b border-line">
                <tr>
                  <th className="th">Action</th>
                  <th className="th text-right">Qté</th>
                  <th className="th text-right"><Label term="prix-moyen">Prix moyen</Label></th>
                  <th className="th text-right"><Label term="pru">PRU</Label></th>
                  <th className="th text-right"><Label term="cours">Cours</Label></th>
                  <th className="th text-right">Valeur</th>
                  <th className="th text-right"><Label term="latent">P&L latent</Label></th>
                  <th className="th text-right"><Label term="diversification">Poids</Label></th>
                </tr>
              </thead>
              <tbody>
                {list.map((p) => {
                  const price = prices[p.ticker];
                  const w = sum.total ? Math.abs(marketValue(p, price)) / sum.total : 0;
                  return (
                    <tr key={p.ticker} className="border-b border-line/50 last:border-0 hover:bg-panel2">
                      <td className="td">
                        <Link to={`/action/${p.ticker}`} className="font-mono font-semibold text-white hover:text-accent">{p.ticker}</Link>
                        <div className="text-xs text-slate-500">{COMPANY_BY_TICKER[p.ticker].name}{p.qty < 0 && ' · à découvert'}</div>
                      </td>
                      <td className="td num text-right">{p.qty}</td>
                      <td className="td num text-right">{fmtNum(p.avgPrice)} €</td>
                      <td className="td num text-right">{fmtNum(p.pru)} €</td>
                      <td className="td num text-right">{fmtNum(price)} €</td>
                      <td className="td text-right"><Money value={marketValue(p, price)} /></td>
                      <td className="td text-right">
                        <Money value={unrealizedPnl(p, price)} signed color />
                        <div><Pct value={unrealizedPct(p, price)} className="text-xs" /></div>
                      </td>
                      <td className={`td num text-right ${w > 0.25 ? 'text-down' : ''}`} title={w > 0.25 ? 'Plus de 25 % du portefeuille : risque de concentration' : ''}>
                        {fmtPctPlain(w)} {w > 0.25 && '⚠️'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card title={<Label term="diversification">Répartition par secteur</Label>}>
          <SectorPie data={pie} />
        </Card>
        <Card title="Ordres en attente">
          {orders.length === 0 ? (
            <p className="py-6 text-center text-sm text-slate-500">Aucun ordre en attente.</p>
          ) : (
            <ul className="divide-y divide-line">
              {orders.map((o) => (
                <li key={o.id} className="flex items-center justify-between gap-2 py-2 text-sm">
                  <span>
                    <span className="font-mono font-semibold">{o.ticker}</span> · {labelOrderType(o.type)} {o.side === 'buy' ? 'achat' : 'vente'} {o.qty} à{' '}
                    <span className="num">{fmtNum(o.triggerPrice)} €</span>
                    <span className="block text-xs text-slate-500">créé le {fmtDate(o.createdDay)} · cours actuel {fmtNum(prices[o.ticker])} €</span>
                  </span>
                  <button className="btn-ghost px-2 py-1 text-xs" onClick={() => cancelOrder(o.id)}>Annuler</button>
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>
    </div>
  );
}
