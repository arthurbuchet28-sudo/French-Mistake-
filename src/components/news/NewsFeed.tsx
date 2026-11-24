import { Link } from 'react-router-dom';
import { COMPANY_BY_TICKER, SECTORS } from '../../data/companies';
import { NEWS_KIND_LABEL } from '../../data/newsTemplates';
import type { NewsItem } from '../../engine/types';
import { useGame } from '../../store/gameStore';
import { fmtDate, fmtPct, fmtTime } from '../../utils/format';
import { Help } from '../ui/Help';

function NewsRow({ n, today }: { n: NewsItem; today: number }) {
  const revealed = n.day < today;
  const scope = n.ticker ? COMPANY_BY_TICKER[n.ticker]?.name : n.sector ? `Secteur ${SECTORS[n.sector].label}` : 'Tout le marché';
  return (
    <li className="border-b border-line/60 py-2.5 last:border-0">
      <div className="flex items-center gap-2 text-[11px] text-slate-500">
        <span className="num">
          {n.day === today ? 'Aujourd’hui' : fmtDate(n.day)} {fmtTime(n.tick)}
        </span>
        <span className={`rounded px-1.5 py-0.5 ${n.kind === 'rumeur' ? 'bg-slate-700/60 text-slate-300' : 'bg-panel2 text-slate-300'}`}>{NEWS_KIND_LABEL[n.kind]}</span>
        {n.ticker ? (
          <Link to={`/action/${n.ticker}`} className="font-mono text-accent hover:underline">
            {n.ticker}
          </Link>
        ) : (
          <span>{scope}</span>
        )}
        <span className={`num ml-auto ${Math.abs(n.impact) < 0.01 ? 'text-slate-400' : n.impact > 0 ? 'text-up' : 'text-down'}`} title="Impact immédiat sur le cours">
          {fmtPct(n.impact, 1)}
        </span>
      </div>
      <div className="mt-1 text-sm text-slate-200">{n.title}</div>
      {n.isFake && revealed && (
        <div className="mt-1 inline-flex items-center gap-1 text-[11px] text-gold">
          🕵️ Fausse piste : impact négligeable <Help term="fausse-piste" />
        </div>
      )}
    </li>
  );
}

export function NewsFeed({ ticker, limit = 12, sector }: { ticker?: string; limit?: number; sector?: string }) {
  const news = useGame((s) => s.market.news);
  const today = useGame((s) => s.market.day);
  const items = news
    .filter((n) => !ticker || n.ticker === ticker || (!n.ticker && (n.sector === sector || !n.sector)))
    .slice(0, limit);
  if (items.length === 0) return <p className="py-6 text-center text-sm text-slate-500">Pas encore d’actualité. Elles tombent au fil des journées de bourse.</p>;
  return (
    <ul>
      {items.map((n) => (
        <NewsRow key={n.id} n={n} today={today} />
      ))}
    </ul>
  );
}
