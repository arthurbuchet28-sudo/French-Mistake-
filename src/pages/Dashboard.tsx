import { Link } from 'react-router-dom';
import { PortfolioVsIndexChart } from '../components/charts/PortfolioVsIndexChart';
import { NewsFeed } from '../components/news/NewsFeed';
import { MissionList } from '../components/progression/MissionList';
import { Card, Stat } from '../components/ui/Card';
import { Label } from '../components/ui/Help';
import { Money, Pct } from '../components/ui/Num';
import { COMPANY_BY_TICKER, INDEX_NAME } from '../data/companies';
import { LEVELS } from '../data/levels';
import { dayChange } from '../engine/market';
import { useGame } from '../store/gameStore';
import { usePortfolioSummary } from '../store/selectors';

export default function Dashboard() {
  const sum = usePortfolioSummary();
  const snapshots = useGame((s) => s.snapshots);
  const market = useGame((s) => s.market);
  const level = useGame((s) => s.level);
  const txCount = useGame((s) => s.transactions.length);
  const movers = Object.values(market.stocks)
    .map((s) => ({ t: s.ticker, ch: dayChange(s), price: s.price }))
    .sort((a, b) => b.ch - a.ch);
  const live = { day: market.day, value: sum.total, cash: sum.cash, index: market.index.value };
  const indexTotal = market.index.value / snapshots[0].index - 1;

  return (
    <div className="space-y-4">
      {txCount === 0 && (
        <div className="card flex flex-col gap-3 border-accent/40 bg-accent/5 p-4 sm:flex-row sm:items-center">
          <div className="flex-1">
            <p className="font-medium text-white">Prêt pour ton premier trade ?</p>
            <p className="text-sm text-slate-400">Tu as 10 000 € fictifs. Va sur le Marché, choisis une entreprise et achète quelques actions.</p>
          </div>
          <Link to="/marche" className="btn-primary">
            Voir le marché →
          </Link>
        </div>
      )}

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Stat label={<Label term="portefeuille">Valeur totale</Label>} value={<Money value={sum.total} />} sub={<span className="text-slate-500">dont investi {Math.round((sum.invested / sum.total) * 100)} %</span>} />
        <Stat label={<Label term="liquidites">Liquidités</Label>} value={<Money value={sum.cash} />} sub={sum.collateral > 0 ? <span className="text-slate-500">disponible <Money value={sum.buyingPower} /></span> : undefined} />
        <Stat
          label={<Label term="latent">Résultat du jour</Label>}
          value={<Money value={sum.dayPnl} signed color />}
          sub={<Pct value={sum.dayPct} />}
        />
        <Stat
          label={<Label term="plus-value">Résultat total</Label>}
          value={<Money value={sum.totalPnl} signed color />}
          sub={
            <span>
              <Pct value={sum.totalPct} /> <span className="text-slate-500">· indice</span> <Pct value={indexTotal} />
            </span>
          }
        />
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card title={<Label term="indice">Mon portefeuille vs {INDEX_NAME} (base 100)</Label>} className="lg:col-span-2">
          <PortfolioVsIndexChart snapshots={snapshots} live={live} />
        </Card>
        <Card
          title={`🎯 Missions — niveau ${level} « ${LEVELS[level - 1].title} »`}
          right={
            <Link to="/progression" className="text-xs text-accent hover:underline">
              Tout voir
            </Link>
          }
        >
          <MissionList level={level} compact />
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card title="📰 Fil d’actualités" className="lg:col-span-2" tour="news-feed">
          <NewsFeed limit={8} />
        </Card>
        <Card title="🔥 Plus fortes variations du jour">
          <ul className="space-y-1">
            {[...movers.slice(0, 3), ...movers.slice(-3)].map((m) => (
              <li key={m.t}>
                <Link to={`/action/${m.t}`} className="flex items-center justify-between rounded-lg px-2 py-1.5 hover:bg-panel2">
                  <span>
                    <span className="font-mono text-sm font-semibold text-white">{m.t}</span>{' '}
                    <span className="text-xs text-slate-500">{COMPANY_BY_TICKER[m.t].name}</span>
                  </span>
                  <Pct value={m.ch} className="text-sm" />
                </Link>
              </li>
            ))}
          </ul>
        </Card>
      </div>
    </div>
  );
}
