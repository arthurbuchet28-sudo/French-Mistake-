import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import type { ChallengeId } from '../data/challenges';
import { TUTORIAL_STEPS } from '../data/tutorial';
import * as L from './logic';
import { throttledStorage } from './storage';
import type { OrderRequest, OrderResult, PersistedState, Speed, Toast } from './types';

export interface GameStore extends PersistedState {
  toasts: Toast[];
  /** Avance de n ticks */
  advance: (ticks: number) => void;
  /** Avance jusqu'à la fin de la journée */
  advanceDay: () => void;
  setSpeed: (s: Speed) => void;
  placeOrder: (req: OrderRequest) => OrderResult;
  cancelOrder: (id: string) => void;
  setNote: (txId: string, note: string) => void;
  passLesson: (lessonId: string) => void;
  startChallenge: (id: ChallengeId) => void;
  abandonChallenge: () => void;
  dismissChallengeResult: () => void;
  setSandbox: (v: boolean) => void;
  setVolatile: (v: boolean) => void;
  startTutorial: () => void;
  tutorialGo: (step: number) => void;
  endTutorial: () => void;
  dismissToast: (id: number) => void;
  markReportRead: () => void;
  dismissLevelUp: () => void;
  resetGame: () => void;
}

type Set = (fn: (s: GameStore) => Partial<GameStore>) => void;

/** Applique une fonction de logique sur un brouillon et pousse le résultat dans le store */
function mutate<R>(set: Set, get: () => GameStore, fn: (d: L.Draft) => R): R {
  const d: L.Draft = { ...get() };
  const r = fn(d);
  set(() => d);
  return r;
}

export const useGame = create<GameStore>()(
  persist(
    (set, get) => ({
      ...L.newPersistedState(),
      toasts: [],

      advance: (ticks) => mutate(set, get, (d) => L.advance(d, ticks)),
      advanceDay: () => mutate(set, get, (d) => L.advance(d, L.ticksToDayEnd(d))),
      setSpeed: (speed) => set((s) => ({ settings: { ...s.settings, speed } })),
      placeOrder: (req) =>
        mutate(set, get, (d) => {
          const r = L.placeOrder(d, req);
          if (r.ok && !d.challenge) L.evaluateProgress(d);
          return r;
        }),
      cancelOrder: (id) => mutate(set, get, (d) => L.cancelOrder(d, id)),
      setNote: (txId, note) =>
        mutate(set, get, (d) => {
          d.transactions = d.transactions.map((t) => (t.id === txId ? { ...t, note: note.trim() || undefined } : t));
          if (!d.challenge) L.evaluateProgress(d);
        }),
      passLesson: (id) => mutate(set, get, (d) => L.passLesson(d, id)),
      startChallenge: (id) => mutate(set, get, (d) => L.startChallenge(d, id)),
      abandonChallenge: () => mutate(set, get, (d) => L.abandonChallenge(d)),
      dismissChallengeResult: () => set(() => ({ lastChallengeResult: null })),
      setSandbox: (v) => set((s) => ({ settings: { ...s.settings, sandbox: v } })),
      setVolatile: (v) =>
        set((s) => ({ settings: { ...s.settings, volatileMode: v, volatileSince: v ? s.market.day : null } })),
      startTutorial: () => set(() => ({ tutorial: { done: false, active: true, step: 0 } })),
      tutorialGo: (step) =>
        set((s) =>
          step >= TUTORIAL_STEPS.length
            ? { tutorial: { done: true, active: false, step: 0 } }
            : { tutorial: { ...s.tutorial, step: Math.max(0, step) } },
        ),
      endTutorial: () => set(() => ({ tutorial: { done: true, active: false, step: 0 } })),
      dismissToast: (id) => set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),
      markReportRead: () => set(() => ({ unreadReportId: null })),
      dismissLevelUp: () => set(() => ({ pendingLevelUp: null })),
      resetGame: () =>
        set((s) => ({
          ...L.newPersistedState(),
          tutorial: { done: s.tutorial.done, active: false, step: 0 },
          toasts: [],
        })),
    }),
    {
      name: 'bourse-ecole-save',
      version: L.SAVE_VERSION,
      storage: createJSONStorage(() => throttledStorage),
      partialize: (s) => {
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const { toasts, ...rest } = s;
        const out: Record<string, unknown> = {};
        for (const [k, v] of Object.entries(rest)) if (typeof v !== 'function') out[k] = v;
        return out as unknown as GameStore;
      },
      migrate: (persisted, version) => {
        // Sauvegarde incompatible : on repart d'une partie neuve
        if (version !== L.SAVE_VERSION) return L.newPersistedState() as unknown as GameStore;
        return persisted as GameStore;
      },
    },
  ),
);

export const gameActions = () => useGame.getState();
