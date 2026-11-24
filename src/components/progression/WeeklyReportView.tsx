import type { WeeklyReport } from '../../engine/coach';
import { fmtDate, fmtEurSigned } from '../../utils/format';
import { Money, Pct } from '../ui/Num';

export function WeeklyReportView({ r }: { r: WeeklyReport }) {
  const beat = r.ret > r.indexRet;
  return (
    <div className="space-y-4">
      <p className="text-xs text-slate-400">
        Du {fmtDate(r.startDay)} au {fmtDate(r.endDay)} · {r.trades} ordre(s)
      </p>
      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="rounded-lg bg-panel2 p-2">
          <div className="text-[11px] text-slate-400">Ma performance</div>
          <Pct value={r.ret} className="text-lg font-semibold" />
          <div>
            <Money value={r.endValue - r.startValue} signed color className="text-xs" />
          </div>
        </div>
        <div className="rounded-lg bg-panel2 p-2">
          <div className="text-[11px] text-slate-400">INDEX 15</div>
          <Pct value={r.indexRet} className="text-lg font-semibold" />
        </div>
        <div className="rounded-lg bg-panel2 p-2">
          <div className="text-[11px] text-slate-400">Écart</div>
          <Pct value={r.ret - r.indexRet} className="text-lg font-semibold" />
          <div className="text-[11px] text-slate-400">{beat ? 'Indice battu 💪' : 'Sous l’indice'}</div>
        </div>
      </div>
      {(r.best || r.worst) && (
        <div className="space-y-2 text-sm">
          {r.best && (
            <div className="rounded-lg border border-up/30 p-2">
              <span className="text-up">👍 Meilleure décision :</span> {r.best.label} <span className="num text-up">({fmtEurSigned(r.best.pnl)})</span>
            </div>
          )}
          {r.worst && (
            <div className="rounded-lg border border-down/30 p-2">
              <span className="text-down">👎 Pire décision :</span> {r.worst.label} <span className="num text-down">({fmtEurSigned(r.worst.pnl)})</span>
            </div>
          )}
        </div>
      )}
      <div>
        <h4 className="mb-2 text-sm font-semibold text-slate-200">🧑‍🏫 Conseils du coach</h4>
        <ul className="space-y-2">
          {r.tips.map((t, i) => (
            <li key={i} className="rounded-lg bg-panel2 p-2.5 text-sm text-slate-300">
              {t}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
