import { useState } from 'react';
import type { Lesson } from '../../data/lessons';
import { useGame } from '../../store/gameStore';
import { Modal } from '../ui/Modal';

export function LessonModal({ lesson, onClose }: { lesson: Lesson; onClose: () => void }) {
  const passLesson = useGame((s) => s.passLesson);
  const passed = useGame((s) => s.passedLessons.includes(lesson.id));
  const [page, setPage] = useState(0);
  const [answers, setAnswers] = useState<(number | null)[]>(lesson.quiz.map(() => null));
  const [submitted, setSubmitted] = useState(false);
  const inQuiz = page >= lesson.screens.length;
  const score = answers.filter((a, i) => a === lesson.quiz[i].answer).length;
  const success = score >= 2;

  return (
    <Modal open onClose={onClose} title={`Leçon ${lesson.level} — ${lesson.title}`} wide>
      <div className="mb-4 flex gap-1">
        {[...lesson.screens, null].map((_, i) => (
          <span key={i} className={`h-1 flex-1 rounded-full ${i <= page ? 'bg-accent' : 'bg-line'}`} />
        ))}
      </div>

      {!inQuiz ? (
        <div className="min-h-[200px]">
          <div className="text-4xl">{lesson.screens[page].emoji}</div>
          <h3 className="mt-2 text-lg font-semibold text-white">{lesson.screens[page].title}</h3>
          {lesson.screens[page].paragraphs.map((p, i) => (
            <p key={i} className="mt-3 leading-relaxed text-slate-300">
              {p}
            </p>
          ))}
        </div>
      ) : (
        <div>
          <h3 className="text-lg font-semibold text-white">🧠 Mini-quiz</h3>
          <p className="text-sm text-slate-400">2 bonnes réponses sur 3 pour valider la leçon.</p>
          <ol className="mt-4 space-y-5">
            {lesson.quiz.map((q, qi) => (
              <li key={qi}>
                <p className="font-medium text-slate-100">
                  {qi + 1}. {q.question}
                </p>
                <div className="mt-2 grid gap-1.5">
                  {q.options.map((o, oi) => {
                    const chosen = answers[qi] === oi;
                    const correct = submitted && oi === q.answer;
                    const wrong = submitted && chosen && oi !== q.answer;
                    return (
                      <button
                        key={oi}
                        disabled={submitted}
                        onClick={() => setAnswers((a) => a.map((x, i) => (i === qi ? oi : x)))}
                        className={`rounded-lg border px-3 py-2 text-left text-sm transition ${
                          correct ? 'border-up bg-up/15 text-green-200' : wrong ? 'border-down bg-down/15 text-red-200' : chosen ? 'border-accent bg-accent/15 text-white' : 'border-line text-slate-300 hover:border-slate-500'
                        }`}
                      >
                        {o}
                      </button>
                    );
                  })}
                </div>
                {submitted && <p className="mt-1.5 text-xs text-slate-400">💡 {q.explanation}</p>}
              </li>
            ))}
          </ol>
          {submitted && (
            <div className={`mt-4 rounded-lg p-3 text-sm ${success ? 'bg-up/15 text-green-200' : 'bg-gold/15 text-amber-200'}`}>
              Score : {score}/3. {success ? 'Leçon validée 🎉' : 'Pas tout à fait… relis la leçon et retente ta chance !'}
            </div>
          )}
        </div>
      )}

      <div className="mt-6 flex justify-between gap-2">
        <button className="btn-ghost" disabled={page === 0} onClick={() => { setPage((p) => p - 1); setSubmitted(false); }}>
          ← Précédent
        </button>
        {!inQuiz && (
          <button className="btn-primary" onClick={() => setPage((p) => p + 1)}>
            {page === lesson.screens.length - 1 ? 'Passer au quiz' : 'Suivant →'}
          </button>
        )}
        {inQuiz && !submitted && (
          <button
            className="btn-primary"
            disabled={answers.some((a) => a === null)}
            onClick={() => {
              setSubmitted(true);
              if (answers.filter((a, i) => a === lesson.quiz[i].answer).length >= 2) passLesson(lesson.id);
            }}
          >
            Valider mes réponses
          </button>
        )}
        {inQuiz && submitted && (
          success || passed ? (
            <button className="btn-primary" onClick={onClose}>
              Terminer
            </button>
          ) : (
            <button className="btn-primary" onClick={() => { setAnswers(lesson.quiz.map(() => null)); setSubmitted(false); }}>
              Réessayer
            </button>
          )
        )}
      </div>
    </Modal>
  );
}
