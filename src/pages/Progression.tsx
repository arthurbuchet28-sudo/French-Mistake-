import { useState } from 'react';
import { LessonModal } from '../components/progression/LessonModal';
import { MissionList } from '../components/progression/MissionList';
import { Card } from '../components/ui/Card';
import { Modal } from '../components/ui/Modal';
import { Pct } from '../components/ui/Num';
import { BADGES } from '../data/badges';
import { CHALLENGES, type ChallengeId } from '../data/challenges';
import { FEATURE_LABEL, LEVELS } from '../data/levels';
import { LESSON_BY_LEVEL, type Lesson } from '../data/lessons';
import { useGame } from '../store/gameStore';
import { fmtDate } from '../utils/format';

export default function Progression() {
  const level = useGame((s) => s.level);
  const passed = useGame((s) => s.passedLessons);
  const badges = useGame((s) => s.badges);
  const challenge = useGame((s) => s.challenge);
  const results = useGame((s) => s.challengeResults);
  const day = useGame((s) => s.market.day);
  const startChallenge = useGame((s) => s.startChallenge);
  const abandonChallenge = useGame((s) => s.abandonChallenge);
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [confirmCh, setConfirmCh] = useState<ChallengeId | null>(null);

  return (
    <div className="space-y-4">
      <Card title="🎯 Niveaux et missions">
        <p className="mb-4 text-sm text-slate-400">
          Pour passer au niveau suivant : accomplis toutes les missions du niveau <strong>et</strong> réussis le quiz de sa leçon (2 bonnes réponses sur 3).
        </p>
        <ol className="space-y-4">
          {LEVELS.map((l) => {
            const ls = LESSON_BY_LEVEL[l.level];
            const unlocked = level >= l.level;
            const lessonDone = passed.includes(ls.id);
            return (
              <li key={l.level} className={`rounded-xl border p-4 ${l.level === level ? 'border-accent/60 bg-accent/5' : 'border-line'} ${unlocked ? '' : 'opacity-60'}`}>
                <div className="flex flex-wrap items-center gap-2">
                  <span className={`rounded-md px-2 py-0.5 text-xs font-bold ${unlocked ? 'bg-accent/20 text-accent' : 'bg-panel2 text-slate-500'}`}>Niv. {l.level}</span>
                  <h3 className="font-semibold text-white">{l.title}</h3>
                  <span className="text-xs text-slate-400">{l.subtitle}</span>
                  {!unlocked && <span className="ml-auto text-xs text-slate-500">🔒 Verrouillé</span>}
                  {l.level < level && <span className="ml-auto text-xs text-up">✔ Terminé</span>}
                </div>
                {l.unlocks.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    {l.unlocks.map((f) => (
                      <span key={f} className="rounded bg-panel2 px-2 py-0.5 text-[11px] text-slate-400">🔓 {FEATURE_LABEL[f]}</span>
                    ))}
                  </div>
                )}
                <div className="mt-3 grid gap-3 md:grid-cols-[1fr_260px]">
                  <MissionList level={l.level} />
                  <button
                    disabled={!unlocked}
                    onClick={() => setLesson(ls)}
                    className={`flex flex-col items-start rounded-lg border p-3 text-left transition disabled:cursor-not-allowed ${lessonDone ? 'border-up/40 bg-up/5' : 'border-line hover:border-accent'}`}
                  >
                    <span className="text-xs text-slate-400">📚 Leçon {l.level} · {ls.screens.length} écrans + quiz</span>
                    <span className="mt-1 text-sm font-medium text-white">{ls.title}</span>
                    <span className={`mt-2 text-xs ${lessonDone ? 'text-up' : 'text-accent'}`}>{lessonDone ? '✅ Quiz réussi — relire' : unlocked ? 'Commencer →' : '🔒'}</span>
                  </button>
                </div>
              </li>
            );
          })}
        </ol>
      </Card>

      <Card title="⚔️ Défis (optionnels, relançables)">
        {challenge && (
          <div className="mb-4 rounded-lg border border-gold/40 bg-gold/10 p-3 text-sm">
            Défi en cours : <strong>{CHALLENGES.find((c) => c.id === challenge.id)?.title}</strong> — jour {day - challenge.startDay + 1} / {challenge.endDay - challenge.startDay}. Ta partie principale est mise de côté et sera restaurée à la fin.
            <button className="btn-ghost ml-2 mt-2 px-2 py-1 text-xs sm:mt-0" onClick={abandonChallenge}>
              Abandonner le défi
            </button>
          </div>
        )}
        <div className="grid gap-3 md:grid-cols-3">
          {CHALLENGES.map((c) => {
            const mine = results.filter((r) => r.id === c.id);
            const best = mine.length ? Math.max(...mine.map((r) => r.portfolioReturn)) : null;
            return (
              <div key={c.id} className="flex flex-col rounded-xl border border-line p-4">
                <div className="text-3xl">{c.emoji}</div>
                <h3 className="mt-1 font-semibold text-white">{c.title}</h3>
                <p className="text-sm text-slate-300">{c.pitch}</p>
                <ul className="mt-2 list-disc space-y-0.5 pl-4 text-xs text-slate-400">
                  {c.rules.map((r) => <li key={r}>{r}</li>)}
                </ul>
                <p className="mt-2 text-xs text-gold">{c.goal}</p>
                {best !== null && (
                  <p className="mt-2 text-xs text-slate-400">
                    {mine.filter((r) => r.success).length}/{mine.length} réussi(s) · meilleur : <Pct value={best} />
                  </p>
                )}
                <button className="btn-primary mt-auto pt-2" style={{ marginTop: 12 }} disabled={!!challenge} onClick={() => setConfirmCh(c.id)}>
                  {mine.length ? 'Rejouer' : 'Lancer le défi'}
                </button>
              </div>
            );
          })}
        </div>
      </Card>

      <Card title={`🏅 Badges (${badges.length}/${BADGES.length})`}>
        <ul className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-5">
          {BADGES.map((b) => {
            const got = badges.includes(b.id);
            return (
              <li key={b.id} className={`rounded-lg border p-3 text-center ${got ? 'border-gold/50 bg-gold/5' : 'border-line opacity-50 grayscale'}`} title={b.description}>
                <div className="text-3xl">{b.emoji}</div>
                <div className="mt-1 text-xs font-medium text-white">{b.title}</div>
                <div className="mt-0.5 text-[11px] text-slate-400">{b.description}</div>
              </li>
            );
          })}
        </ul>
      </Card>

      {results.length > 0 && (
        <Card title="Historique des défis">
          <ul className="divide-y divide-line text-sm">
            {[...results].reverse().map((r, i) => (
              <li key={i} className="flex justify-between py-1.5">
                <span>{r.success ? '🏆' : '❌'} {CHALLENGES.find((c) => c.id === r.id)?.title} <span className="text-xs text-slate-500">· {fmtDate(r.day)}</span></span>
                <span><Pct value={r.portfolioReturn} /> <span className="text-xs text-slate-500">(indice <Pct value={r.indexReturn} />)</span></span>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {lesson && <LessonModal lesson={lesson} onClose={() => setLesson(null)} />}
      <Modal open={!!confirmCh} onClose={() => setConfirmCh(null)} title="Lancer le défi ?">
        <p className="text-sm text-slate-300">
          Ta partie actuelle (portefeuille, ordres, marché) est mise de côté et sera restaurée intacte à la fin du défi ou si tu l’abandonnes.
        </p>
        <div className="mt-4 flex gap-2">
          <button className="btn-ghost flex-1" onClick={() => setConfirmCh(null)}>Annuler</button>
          <button
            className="btn-primary flex-1"
            onClick={() => {
              if (confirmCh) startChallenge(confirmCh);
              setConfirmCh(null);
            }}
          >
            C’est parti
          </button>
        </div>
      </Modal>
    </div>
  );
}
