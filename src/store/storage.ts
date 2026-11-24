import type { StateStorage } from 'zustand/middleware';

/**
 * Stockage localStorage avec écriture différée : la simulation met à jour l'état
 * plusieurs fois par seconde, inutile de sérialiser à chaque tick.
 */
let pending: [string, string] | null = null;
let timer: ReturnType<typeof setTimeout> | null = null;

function flush() {
  if (timer) clearTimeout(timer);
  timer = null;
  if (!pending) return;
  const [k, v] = pending;
  pending = null;
  try {
    localStorage.setItem(k, v);
  } catch (e) {
    console.warn('Sauvegarde impossible', e);
  }
}

if (typeof window !== 'undefined') {
  window.addEventListener('beforeunload', flush);
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') flush();
  });
}

export const throttledStorage: StateStorage = {
  getItem: (name) => {
    try {
      return localStorage.getItem(name);
    } catch {
      return null;
    }
  },
  setItem: (name, value) => {
    pending = [name, value];
    if (!timer) timer = setTimeout(flush, 1500);
  },
  removeItem: (name) => {
    pending = null;
    try {
      localStorage.removeItem(name);
    } catch {
      /* ignore */
    }
  },
};

export const flushStorage = flush;
