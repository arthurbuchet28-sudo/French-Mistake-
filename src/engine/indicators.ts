import type { Candle } from './types';

/** Moyenne mobile simple. Renvoie null tant qu'il n'y a pas assez de points. */
export function sma(values: number[], period: number): (number | null)[] {
  const out: (number | null)[] = [];
  let sum = 0;
  for (let i = 0; i < values.length; i++) {
    sum += values[i];
    if (i >= period) sum -= values[i - period];
    out.push(i >= period - 1 ? sum / period : null);
  }
  return out;
}

/** Regroupe une série de prix tick par tick en bougies de `size` ticks. */
export function aggregateTicks(prices: number[], size: number, volumes?: number[]): Candle[] {
  const out: Candle[] = [];
  for (let i = 1; i < prices.length; i += size) {
    const slice = prices.slice(i, i + size);
    if (slice.length === 0) break;
    const o = prices[i - 1];
    const c = slice[slice.length - 1];
    const v = volumes ? volumes.slice(i, i + size).reduce((a, b) => a + b, 0) : 0;
    out.push({ t: i, o, h: Math.max(o, ...slice), l: Math.min(o, ...slice), c, v });
  }
  return out;
}

export function pctChange(from: number, to: number): number {
  return from === 0 ? 0 : (to - from) / from;
}
