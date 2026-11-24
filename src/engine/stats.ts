import type { Transaction } from './trading';

export interface Snapshot {
  day: number;
  value: number;
  cash: number;
  index: number;
}

/** Drawdown maximum : plus forte baisse depuis un sommet (fraction positive, ex. 0.12 = −12 %). */
export function maxDrawdown(values: number[]): number {
  let peak = -Infinity;
  let mdd = 0;
  for (const v of values) {
    if (v > peak) peak = v;
    if (peak > 0) mdd = Math.max(mdd, (peak - v) / peak);
  }
  return mdd;
}

/** Série de drawdown (0 ou négative) pour un graphique */
export function drawdownSeries(values: number[]): number[] {
  let peak = -Infinity;
  return values.map((v) => {
    peak = Math.max(peak, v);
    return peak > 0 ? v / peak - 1 : 0;
  });
}

export interface TradeStats {
  closedTrades: number;
  wins: number;
  losses: number;
  winRate: number;
  avgGain: number;
  avgLoss: number;
  avgGainPct: number;
  avgLossPct: number;
  biggestGain: number;
  biggestLoss: number;
  totalRealized: number;
  totalFees: number;
  /** Gain moyen / perte moyenne (en valeur absolue) */
  payoffRatio: number;
}

export function tradeStats(transactions: Transaction[]): TradeStats {
  const closed = transactions.filter((t) => t.realizedPnl !== undefined);
  const wins = closed.filter((t) => (t.realizedPnl ?? 0) > 0);
  const losses = closed.filter((t) => (t.realizedPnl ?? 0) <= 0);
  const sum = (xs: number[]) => xs.reduce((a, b) => a + b, 0);
  const avg = (xs: number[]) => (xs.length ? sum(xs) / xs.length : 0);
  const avgGain = avg(wins.map((t) => t.realizedPnl!));
  const avgLoss = avg(losses.map((t) => t.realizedPnl!));
  return {
    closedTrades: closed.length,
    wins: wins.length,
    losses: losses.length,
    winRate: closed.length ? wins.length / closed.length : 0,
    avgGain,
    avgLoss,
    avgGainPct: avg(wins.map((t) => t.realizedPct ?? 0)),
    avgLossPct: avg(losses.map((t) => t.realizedPct ?? 0)),
    biggestGain: wins.length ? Math.max(...wins.map((t) => t.realizedPnl!)) : 0,
    biggestLoss: losses.length ? Math.min(...losses.map((t) => t.realizedPnl!)) : 0,
    totalRealized: sum(closed.map((t) => t.realizedPnl!)),
    totalFees: sum(transactions.map((t) => t.fees)),
    payoffRatio: avgLoss !== 0 ? Math.abs(avgGain / avgLoss) : 0,
  };
}

/** Performance relative : rendement du portefeuille − rendement de l'indice */
export function relativePerformance(startValue: number, endValue: number, startIndex: number, endIndex: number) {
  const portfolio = startValue > 0 ? endValue / startValue - 1 : 0;
  const index = startIndex > 0 ? endIndex / startIndex - 1 : 0;
  return { portfolio, index, excess: portfolio - index };
}
