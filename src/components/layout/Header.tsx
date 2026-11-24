import { Link } from 'react-router-dom';
import { INDEX_NAME } from '../../data/companies';
import { LEVELS, MAX_LEVEL, missionsForLevel } from '../../data/levels';
import { BADGES } from '../../data/badges';
import { useGame } from '../../store/gameStore';
import { usePortfolioSummary } from '../../store/selectors';
import { fmtDate, fmtTime, fmtWeekday } from '../../utils/format';
import { Money, Pct } from '../ui/Num';
import { TimeControls } from './TimeControls';
import { CHALLENGE_BY_ID } from '../../data/challenges';

export function Header() {
  const day = useGame((s) => s.market.day);
  const tick = useGame((s) => s.market.tick);
  const index = useGame((s) => s.market.index);
  const level = useGame((s) => s.level);
  const done = useGame((s) => s.completedMissions);
  const badges = useGame((s) => s.badges);
  const challenge = useGame((s) => s.challenge);
  const startTutorial = useGame((s) => s.startTutorial);
  const sum = usePortfolioSummary();
  const missions = missionsForLevel(level);
  const doneHere = missions.filter((m) => done.includes(m.id)).length;
  const lvl = LEVELS[level - 1];
  const progress = level >= MAX_LEVEL && doneHere === missions.length ? 1 : (doneHere + 0.0001) / (missions.length + 1);

  return (
    <header className="sticky top-0 z-30 border-b border-line bg-bg/95 backdrop-blur">
      {challenge && (
        <div className="bg-gold/15 px-4 py-1 text-center text-xs text-gold">
          {CHALLENGE_BY_ID[challenge.id].emoji} Défi « {CHALLENGE_BY_ID[challenge.id].title} » en cours — jour {day - challenge.startDay + 1}/{challenge.endDay - challenge.startDay}.{' '}
          <Link to="/progression" className="underline">
            Détails
          </Link>
        </div>
      )}
      <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-x-4 gap-y-2 px-3 py-2 sm:px-4">
        <Link to="/" className="flex items-center gap-2">
          <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230b0f17'/%3E%3Cpath d='M5 23l7-8 5 5 10-12' stroke='%2322c55e' stroke-width='3' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E" alt="" className="h-7 w-7" />
          <span className="hidden font-semibold tracking-tight text-white sm:inline">Bourse École</span>
        </Link>

        <div className="num hidden text-xs text-slate-400 md:block">
          {fmtWeekday(day)} {fmtDate(day)} · {fmtTime(tick)}
        </div>

        <Link to="/marche" className="hidden items-baseline gap-1.5 text-xs lg:flex">
          <span className="text-slate-400">{INDEX_NAME}</span>
          <span className="num text-slate-100">{index.value.toFixed(2).replace('.', ',')}</span>
          <Pct value={index.value / index.prevClose - 1} />
        </Link>

        <Link to="/portefeuille" className="flex items-baseline gap-1.5 text-xs">
          <span className="text-slate-400">Valeur</span>
          <Money value={sum.total} className="text-sm font-semibold text-white" />
          <Pct value={sum.dayPct} className="hidden sm:inline" />
        </Link>

        <div className="ml-auto flex items-center gap-2 sm:gap-3">
          <Link to="/progression" className="flex items-center gap-2" data-tour="header-progress" title={`Niveau ${level} — ${lvl.title}`}>
            <span className="rounded-md bg-accent/20 px-1.5 py-0.5 text-xs font-bold text-accent">Niv. {level}</span>
            <span className="hidden flex-col sm:flex">
              <span className="text-[11px] leading-tight text-slate-300">{lvl.title}</span>
              <span className="mt-0.5 h-1.5 w-24 overflow-hidden rounded-full bg-line">
                <span className="block h-full rounded-full bg-accent transition-all" style={{ width: `${Math.round(progress * 100)}%` }} />
              </span>
            </span>
            <span className="text-xs text-slate-400" title="Badges obtenus">
              🏅 {badges.length}/{BADGES.length}
            </span>
          </Link>
          <TimeControls />
          <button className="btn-ghost px-2 py-1 text-xs" onClick={startTutorial} title="Relancer le tutoriel">
            ❔ <span className="hidden sm:inline">Aide</span>
          </button>
        </div>
      </div>
    </header>
  );
}
