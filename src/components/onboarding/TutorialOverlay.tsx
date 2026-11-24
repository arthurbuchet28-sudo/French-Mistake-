import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { TUTORIAL_STEPS } from '../../data/tutorial';
import { useGame } from '../../store/gameStore';

/**
 * Tutoriel en surimpression : met en surbrillance la zone concernée (attribut data-tour)
 * et affiche une carte explicative avec « Suivant ».
 */
export function TutorialOverlay() {
  const tutorial = useGame((s) => s.tutorial);
  const go = useGame((s) => s.tutorialGo);
  const end = useGame((s) => s.endTutorial);
  const txCount = useGame((s) => s.transactions.length);
  const navigate = useNavigate();
  const location = useLocation();
  const step = TUTORIAL_STEPS[tutorial.step];
  const startTx = useRef(txCount);
  const [cardOnTop, setCardOnTop] = useState(false);

  // Navigation vers la page de l'étape
  useEffect(() => {
    if (!tutorial.active || !step?.route) return;
    if (location.pathname !== step.route) navigate(step.route);
  }, [tutorial.active, tutorial.step]); // eslint-disable-line react-hooks/exhaustive-deps

  // Mémorise le nombre de transactions au début d'une étape interactive
  useEffect(() => {
    startTx.current = txCount;
  }, [tutorial.step]); // eslint-disable-line react-hooks/exhaustive-deps

  // Étape « passe ton premier ordre » : avance automatiquement
  useEffect(() => {
    if (tutorial.active && step?.waitFor === 'buy' && txCount > startTx.current) go(tutorial.step + 1);
  }, [txCount]); // eslint-disable-line react-hooks/exhaustive-deps

  // Surbrillance
  useLayoutEffect(() => {
    if (!tutorial.active || !step?.target) return;
    let el: Element | null = null;
    let tries = 0;
    let timer: ReturnType<typeof setTimeout>;
    const apply = () => {
      el = document.querySelector(`[data-tour="${step.target}"]`);
      if (!el) {
        if (tries++ < 20) timer = setTimeout(apply, 100);
        return;
      }
      el.classList.add('tour-highlight');
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      const r = el.getBoundingClientRect();
      setCardOnTop(r.top + r.height / 2 > window.innerHeight * 0.55);
    };
    apply();
    return () => {
      clearTimeout(timer);
      el?.classList.remove('tour-highlight');
    };
  }, [tutorial.active, tutorial.step, location.pathname]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!tutorial.active || !step) return null;
  const last = tutorial.step === TUTORIAL_STEPS.length - 1;
  const waiting = step.waitFor === 'buy' && txCount <= startTx.current;

  return (
    <>
      {!step.target && <div className="fixed inset-0 z-40 bg-black/75" />}
      <div
        className={`fixed z-[60] w-[calc(100vw-24px)] max-w-md ${
          step.target
            ? `left-3 sm:left-6 ${cardOnTop ? 'top-20' : 'bottom-10'}`
            : 'left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2'
        }`}
      >
        <div className="card border-accent/50 p-5 shadow-2xl">
          <div className="mb-2 flex items-center justify-between text-xs text-slate-400">
            <span>
              Tutoriel · étape {tutorial.step + 1}/{TUTORIAL_STEPS.length}
            </span>
            <button className="hover:text-white" onClick={end}>
              Passer le tutoriel ✕
            </button>
          </div>
          <h3 className="text-lg font-semibold text-white">{step.title}</h3>
          {step.body.map((p, i) => (
            <p key={i} className="mt-2 text-sm leading-relaxed text-slate-300">
              {p}
            </p>
          ))}
          <div className="mt-2 flex gap-1">
            {TUTORIAL_STEPS.map((_, i) => (
              <span key={i} className={`h-1 flex-1 rounded-full ${i <= tutorial.step ? 'bg-accent' : 'bg-line'}`} />
            ))}
          </div>
          <div className="mt-4 flex items-center justify-between gap-2">
            <button className="btn-ghost" disabled={tutorial.step === 0} onClick={() => go(tutorial.step - 1)}>
              ← Retour
            </button>
            {waiting ? (
              <div className="flex flex-col items-end gap-1">
                <span className="text-xs text-gold">⏳ Passe l’ordre pour continuer…</span>
                <button className="text-xs text-slate-400 underline hover:text-white" onClick={() => go(tutorial.step + 1)}>
                  Passer cette étape
                </button>
              </div>
            ) : (
              <button className="btn-primary" onClick={() => (last ? end() : go(tutorial.step + 1))}>
                {last ? 'C’est parti ! 🚀' : 'Suivant →'}
              </button>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
