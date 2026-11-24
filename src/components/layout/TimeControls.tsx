import { useGame } from '../../store/gameStore';
import type { Speed } from '../../store/types';

const SPEEDS: { v: Speed; label: string; title: string }[] = [
  { v: 0, label: '⏸', title: 'Pause' },
  { v: 1, label: 'x1', title: 'Vitesse normale : 1 journée = 60 s' },
  { v: 5, label: 'x5', title: '5 fois plus vite' },
  { v: 20, label: 'x20', title: '20 fois plus vite' },
];

export function TimeControls() {
  const speed = useGame((s) => s.settings.speed);
  const setSpeed = useGame((s) => s.setSpeed);
  const advanceDay = useGame((s) => s.advanceDay);
  return (
    <div className="flex items-center gap-1" data-tour="time-controls">
      <div className="inline-flex rounded-lg border border-line bg-bg p-0.5">
        {SPEEDS.map((s) => (
          <button
            key={s.v}
            title={s.title}
            aria-label={s.title}
            onClick={() => setSpeed(s.v)}
            className={`num rounded-md px-2 py-1 text-xs font-semibold transition ${speed === s.v ? (s.v === 0 ? 'bg-gold text-black' : 'bg-accent text-white') : 'text-slate-400 hover:text-white'}`}
          >
            {s.label}
          </button>
        ))}
      </div>
      <button className="btn-ghost px-2 py-1 text-xs" title="Avancer jusqu’à la clôture de la journée" onClick={advanceDay}>
        ⏭ <span className="hidden sm:inline">Journée</span>
      </button>
    </div>
  );
}
