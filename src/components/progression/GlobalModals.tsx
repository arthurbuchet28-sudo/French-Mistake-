import { useNavigate } from 'react-router-dom';
import { CHALLENGE_BY_ID } from '../../data/challenges';
import { FEATURE_LABEL, LEVELS } from '../../data/levels';
import { useGame } from '../../store/gameStore';
import { Modal } from '../ui/Modal';
import { Pct } from '../ui/Num';
import { WeeklyReportView } from './WeeklyReportView';

/** Bilan hebdo, passage de niveau, résultat de défi */
export function GlobalModals() {
  const navigate = useNavigate();
  const tutorialActive = useGame((s) => s.tutorial.active);
  const unread = useGame((s) => s.unreadReportId);
  const reports = useGame((s) => s.reports);
  const markRead = useGame((s) => s.markReportRead);
  const levelUp = useGame((s) => s.pendingLevelUp);
  const dismissLevelUp = useGame((s) => s.dismissLevelUp);
  const result = useGame((s) => s.lastChallengeResult);
  const dismissResult = useGame((s) => s.dismissChallengeResult);
  const setSpeed = useGame((s) => s.setSpeed);

  if (tutorialActive) return null;

  if (result) {
    const c = CHALLENGE_BY_ID[result.id];
    return (
      <Modal open onClose={dismissResult} title={`${c.emoji} Défi ${c.title} terminé`}>
        <div className="text-center">
          <div className="text-5xl">{result.success ? '🏆' : '💪'}</div>
          <p className="mt-2 text-lg font-semibold text-white">{result.success ? 'Défi réussi !' : 'Défi échoué… mais c’est en s’entraînant qu’on apprend.'}</p>
          <p className="mt-1 text-sm text-slate-400">{c.goal}</p>
          <div className="mt-4 grid grid-cols-2 gap-2">
            <div className="rounded-lg bg-panel2 p-2">
              <div className="text-xs text-slate-400">Ton portefeuille</div>
              <Pct value={result.portfolioReturn} className="text-lg font-semibold" />
            </div>
            <div className="rounded-lg bg-panel2 p-2">
              <div className="text-xs text-slate-400">INDEX 15</div>
              <Pct value={result.indexReturn} className="text-lg font-semibold" />
            </div>
          </div>
          <p className="mt-4 text-xs text-slate-500">Ta partie principale a été restaurée telle que tu l’avais laissée.</p>
          <button className="btn-primary mt-4 w-full" onClick={dismissResult}>
            Continuer
          </button>
        </div>
      </Modal>
    );
  }

  if (levelUp) {
    const l = LEVELS[levelUp - 1];
    return (
      <Modal open onClose={dismissLevelUp} title="🎉 Niveau supérieur !">
        <div className="text-center">
          <div className="text-5xl">🚀</div>
          <p className="mt-2 text-xl font-semibold text-white">
            Niveau {l.level} — {l.title}
          </p>
          <p className="mt-1 text-sm text-slate-400">{l.subtitle}</p>
          {l.unlocks.length > 0 && (
            <ul className="mt-4 space-y-1 text-left text-sm">
              {l.unlocks.map((f) => (
                <li key={f} className="rounded-lg bg-panel2 px-3 py-2">
                  🔓 {FEATURE_LABEL[f]}
                </li>
              ))}
            </ul>
          )}
          <p className="mt-4 text-sm text-slate-300">Une nouvelle leçon t’attend, ainsi que de nouvelles missions.</p>
          <div className="mt-4 flex gap-2">
            <button className="btn-ghost flex-1" onClick={dismissLevelUp}>
              Plus tard
            </button>
            <button
              className="btn-primary flex-1"
              onClick={() => {
                dismissLevelUp();
                navigate('/progression');
              }}
            >
              Voir la leçon
            </button>
          </div>
        </div>
      </Modal>
    );
  }

  const report = unread ? reports.find((r) => r.id === unread) : undefined;
  if (report) {
    return (
      <Modal
        open
        onClose={markRead}
        title={`📅 Bilan de la semaine ${report.week}`}
        wide
      >
        <WeeklyReportView r={report} />
        <div className="mt-5 flex gap-2">
          <button
            className="btn-ghost flex-1"
            onClick={() => {
              setSpeed(0);
              markRead();
            }}
          >
            Fermer et mettre en pause
          </button>
          <button className="btn-primary flex-1" onClick={markRead}>
            Continuer
          </button>
        </div>
      </Modal>
    );
  }
  return null;
}
