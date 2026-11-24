import { missionsForLevel } from '../../data/levels';
import { useGame } from '../../store/gameStore';
import { progressContext } from '../../store/logic';

export function MissionList({ level, compact = false }: { level: number; compact?: boolean }) {
  const state = useGame();
  const ctx = progressContext(state);
  const missions = missionsForLevel(level);
  return (
    <ul className="space-y-2">
      {missions.map((m) => {
        const done = state.completedMissions.includes(m.id);
        const locked = level > state.level;
        const prog = Math.min(m.target, m.progress(ctx));
        return (
          <li key={m.id} className={`flex items-start gap-3 rounded-lg border p-3 ${done ? 'border-up/40 bg-up/5' : 'border-line'}`}>
            <span className="mt-0.5 text-lg">{done ? '✅' : locked ? '🔒' : '⬜'}</span>
            <div className="min-w-0 flex-1">
              <div className={`text-sm font-medium ${done ? 'text-green-200' : 'text-slate-100'}`}>{m.title}</div>
              {!compact && <div className="mt-0.5 text-xs text-slate-400">{m.hint}</div>}
              {!done && !locked && m.target > 1 && (
                <div className="mt-1.5 flex items-center gap-2">
                  <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-line">
                    <div className="h-full bg-accent" style={{ width: `${(prog / m.target) * 100}%` }} />
                  </div>
                  <span className="num text-[11px] text-slate-400">
                    {prog}/{m.target}
                  </span>
                </div>
              )}
            </div>
          </li>
        );
      })}
    </ul>
  );
}
