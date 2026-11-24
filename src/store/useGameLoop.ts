import { useEffect } from 'react';
import { useGame } from './gameStore';

/**
 * Horloge de la simulation : x1 = 1 tick par seconde.
 * Aux vitesses rapides, on regroupe plusieurs ticks par rafraîchissement pour rester fluide.
 */
export function useGameLoop() {
  const speed = useGame((s) => s.settings.speed);
  const advance = useGame((s) => s.advance);
  useEffect(() => {
    if (speed === 0) return;
    const interval = speed === 1 ? 1000 : speed === 5 ? 200 : 250;
    const ticksPerInterval = Math.max(1, Math.round((speed * interval) / 1000));
    const id = setInterval(() => advance(ticksPerInterval), interval);
    return () => clearInterval(id);
  }, [speed, advance]);
}
