import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { CandleChart, type Timeframe } from '../components/charts/CandleChart';
import { NewsFeed } from '../components/news/NewsFeed';
import { OrderPanel } from '../components/trading/OrderPanel';
import { Card } from '../components/ui/Card';
import { Help, Label } from '../components/ui/Help';
import { Money, Pct } from '../components/ui/Num';
import { Locked, Tabs } from '../components/ui/Tabs';
import { COMPANY_BY_TICKER, SECTORS } from '../data/companies';
import { FEATURE_LEVEL } from '../data/levels';
import { dayChange } from '../engine/market';
import { unrealizedPnl, unrealizedPct } from '../engine/trading';
import { useGame } from '../store/gameStore';
import { useUnlocked } from '../store/selectors';
import { fmtInt, fmtNum, fmtPctPlain } from '../utils/format';

export default function StockDetail() {
  const { ticker = '' } = useParams();
  const c = COMPANY_BY_TICKER[ticker.toUpperCase()];
  const stock = useGame((s) => (c ? s.market.stocks[c.ticker] : undefined));
  const day = useGame((s) => s.market.day);
  const pos = useGame((s) => (c ? s.positions[c.ticker] : undefined));
  const allOrders = useGame((s) => s.orders);
  const orders = allOrders.filter((o) => o.ticker === c?.ticker);
  const cancelOrder = useGame((s) => s.cancelOrder);
  const indicatorsOk = useUnlocked('indicators');
  const [tf, setTf] = useState<Timeframe>('1M');
  const [ma, setMa] = useState(false);
  const [vol, setVol] = useState(false);

  if (!c || !stock) {
    return (
      <div className="card p-8 text-center">
        Action introuvable. <Link to="/marche" className="text-accent">Retour au marché</Link>
      </div>
    );
  }
  const ch = dayChange(stock);
  const last20 = stock.candles.slice(-20);
  const high = Math.max(...stock.candles.slice(-126).map((k) => k.h));
  const low = Math.min(...stock.candles.slice(-126).map((k) => k.l));

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end gap-x-4 gap-y-1">
        <Link to="/marche" className="w-full text-xs text-slate-400 hover:text-white">
          ← Marché
        </Link>
        <div>
          <h1 className="text-2xl font-semibold text-white">
            <span className="font-mono">{c.ticker}</span> <span className="text-base font-normal text-slate-400">{c.name}</span>
          </h1>
          <div className="text-xs text-slate-500">
            {SECTORS[c.sector].emoji} {SECTORS[c.sector].label}
          </div>
        </div>
        <div className="ml-auto text-right">
          <div className="num text-3xl font-semibold text-white">{fmtNum(stock.price)} €</div>
          <div className="text-sm">
            <Money value={stock.price - stock.prevClose} signed color /> (<Pct value={ch} />) <span className="text-slate-500">aujourd’hui</span>
          </div>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <div className="space-y-4 lg:col-span-2">
          <Card
            title={<Label term="chandelier">Graphique en chandeliers</Label>}
            right={<Tabs size="xs" value={tf} onChange={setTf} options={(['1J', '1S', '1M', '6M'] as Timeframe[]).map((v) => ({ value: v, label: v }))} />}
          >
            <div className="mb-2 flex flex-wrap items-center gap-3 text-xs">
              <label className={`flex items-center gap-1.5 ${indicatorsOk ? 'text-slate-300' : 'text-slate-500'}`}>
                <input type="checkbox" disabled={!indicatorsOk} checked={ma && indicatorsOk} onChange={(e) => setMa(e.target.checked)} />
                <Label term="moyenne-mobile">Moyennes mobiles 20/50</Label>
              </label>
              <label className={`flex items-center gap-1.5 ${indicatorsOk ? 'text-slate-300' : 'text-slate-500'}`}>
                <input type="checkbox" disabled={!indicatorsOk} checked={vol && indicatorsOk} onChange={(e) => setVol(e.target.checked)} />
                <Label term="volume">Volume</Label>
              </label>
              {!indicatorsOk && <Locked level={FEATURE_LEVEL.indicators} />}
            </div>
            <CandleChart stock={stock} day={day} timeframe={tf} showMA={ma && indicatorsOk} showVolume={vol && indicatorsOk} />
            <p className="mt-2 text-[11px] text-slate-500">
              {tf === '1J' ? 'Séance du jour, une bougie toutes les 3 minutes simulées.' : 'Une bougie = une journée de bourse. La dernière bougie est la séance en cours.'}
            </p>
          </Card>

          <Card title="À propos">
            <p className="text-sm leading-relaxed text-slate-300">{c.description}</p>
            <dl className="mt-4 grid grid-cols-2 gap-3 text-sm sm:grid-cols-4">
              <div>
                <dt className="text-xs text-slate-500">
                  <Label term="volatilite">Volatilité / jour</Label>
                </dt>
                <dd className="num">{fmtPctPlain(c.volatility)}</dd>
              </div>
              <div>
                <dt className="text-xs text-slate-500">
                  <Label term="dividende">Dividende annuel</Label>
                </dt>
                <dd className="num">{c.dividendYield > 0 ? `≈ ${fmtPctPlain(c.dividendYield)}` : 'Aucun'}</dd>
              </div>
              <div>
                <dt className="text-xs text-slate-500">Plus haut / bas 6 mois</dt>
                <dd className="num">
                  {fmtNum(high)} / {fmtNum(low)}
                </dd>
              </div>
              <div>
                <dt className="text-xs text-slate-500">
                  <Label term="volume">Volume moyen 20 j</Label>
                </dt>
                <dd className="num">{fmtInt(last20.reduce((a, k) => a + k.v, 0) / Math.max(1, last20.length))}</dd>
              </div>
            </dl>
          </Card>

          <Card title="📰 Actualités liées">
            <NewsFeed ticker={c.ticker} sector={c.sector} limit={10} />
          </Card>
        </div>

        <div className="space-y-4">
          <OrderPanel ticker={c.ticker} />

          {pos && (
            <Card title={<Label term="position">Ma position</Label>}>
              <dl className="space-y-1.5 text-sm">
                <div className="flex justify-between">
                  <dt className="text-slate-400">Quantité</dt>
                  <dd className="num">{pos.qty < 0 ? `${pos.qty} (à découvert)` : pos.qty}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-slate-400">
                    <Label term="prix-moyen">Prix moyen</Label>
                  </dt>
                  <dd className="num">{fmtNum(pos.avgPrice)} €</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-slate-400">
                    <Label term="pru">PRU</Label>
                  </dt>
                  <dd className="num">{fmtNum(pos.pru)} €</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-slate-400">
                    <Label term="latent">P&L latent</Label>
                  </dt>
                  <dd>
                    <Money value={unrealizedPnl(pos, stock.price)} signed color /> <Pct value={unrealizedPct(pos, stock.price)} className="text-xs" />
                  </dd>
                </div>
              </dl>
            </Card>
          )}

          {orders.length > 0 && (
            <Card title="Ordres en attente">
              <ul className="space-y-2">
                {orders.map((o) => (
                  <li key={o.id} className="flex items-center justify-between gap-2 text-sm">
                    <span>
                      {o.type === 'stop' ? '🛑 Stop-loss' : o.type === 'takeprofit' ? '🎯 Take-profit' : '🎚️ Limite'} {o.side === 'buy' ? 'achat' : 'vente'} {o.qty} @{' '}
                      <span className="num">{fmtNum(o.triggerPrice)} €</span>
                    </span>
                    <button className="text-xs text-down hover:underline" onClick={() => cancelOrder(o.id)}>
                      Annuler
                    </button>
                  </li>
                ))}
              </ul>
            </Card>
          )}
          <p className="px-1 text-[11px] text-slate-500">
            Tous les chiffres sont simulés. <Help term="action" />
          </p>
        </div>
      </div>
    </div>
  );
}
