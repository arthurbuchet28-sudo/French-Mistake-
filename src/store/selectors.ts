import { useMemo } from 'react';
import { currentPrices } from '../engine/market';
import { buyingPower, portfolioValue, shortCollateral } from '../engine/trading';
import { useGame } from './gameStore';
import { isUnlocked } from './logic';
import type { Feature } from '../data/levels';

/** Prix courants (recalculés à chaque tick) */
export function usePrices(): Record<string, number> {
  const market = useGame((s) => s.market);
  return useMemo(() => currentPrices(market), [market]);
}

export interface PortfolioSummary {
  total: number;
  cash: number;
  invested: number;
  buyingPower: number;
  collateral: number;
  dayPnl: number;
  dayPct: number;
  totalPnl: number;
  totalPct: number;
  prevValue: number;
}

export function usePortfolioSummary(): PortfolioSummary {
  const prices = usePrices();
  const cash = useGame((s) => s.cash);
  const positions = useGame((s) => s.positions);
  const snapshots = useGame((s) => s.snapshots);
  const startValue = useGame((s) => s.startValue);
  return useMemo(() => {
    const p = { cash, positions };
    const total = portfolioValue(p, prices);
    const prevValue = snapshots[snapshots.length - 1]?.value ?? startValue;
    return {
      total,
      cash,
      invested: total - cash,
      buyingPower: buyingPower(p, prices),
      collateral: shortCollateral(p, prices),
      dayPnl: total - prevValue,
      dayPct: prevValue ? total / prevValue - 1 : 0,
      totalPnl: total - startValue,
      totalPct: startValue ? total / startValue - 1 : 0,
      prevValue,
    };
  }, [prices, cash, positions, snapshots, startValue]);
}

export function useUnlocked(f: Feature): boolean {
  const level = useGame((s) => s.level);
  const sandbox = useGame((s) => s.settings.sandbox);
  return isUnlocked({ level, settings: { sandbox } as never }, f);
}
