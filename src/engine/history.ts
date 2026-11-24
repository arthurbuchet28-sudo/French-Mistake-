import { COMPANIES, SECTOR_IDS } from '../data/companies';
import { correlatedShock, gbmStep } from './gbm';
import type { Rng } from './random';
import type { Candle, SectorId } from './types';

/** Environ 6 mois de bourse */
export const HISTORY_DAYS = 126;
const SUBSTEPS = 12;

/**
 * Génère un historique journalier (bougies OHLC + volume) pour chaque action,
 * avec le même modèle GBM corrélé que la simulation temps réel.
 * Les séries sont ensuite remises à l'échelle pour finir exactement au prix de départ.
 */
export function generateHistory(rng: Rng, days = HISTORY_DAYS): Record<string, Candle[]> {
  const prices: Record<string, number> = {};
  const out: Record<string, Candle[]> = {};
  for (const c of COMPANIES) {
    prices[c.ticker] = c.startPrice;
    out[c.ticker] = [];
  }
  const dt = 1 / SUBSTEPS;
  for (let d = 0; d < days; d++) {
    const open: Record<string, number> = {};
    const high: Record<string, number> = {};
    const low: Record<string, number> = {};
    // Petit écart à l'ouverture
    for (const c of COMPANIES) {
      const p = prices[c.ticker] * (1 + rng.normal() * c.volatility * 0.15);
      prices[c.ticker] = p;
      open[c.ticker] = p;
      high[c.ticker] = p;
      low[c.ticker] = p;
    }
    // Saut ponctuel façon « actualité »
    let jumpTicker: string | null = null;
    let jumpSize = 0;
    if (rng.next() < 0.12) {
      jumpTicker = rng.pick(COMPANIES).ticker;
      jumpSize = (rng.next() < 0.5 ? -1 : 1) * (0.03 + rng.next() * 0.06);
    }
    for (let s = 0; s < SUBSTEPS; s++) {
      const zm = rng.normal();
      const zs: Record<string, number> = {};
      for (const sec of SECTOR_IDS) zs[sec] = rng.normal();
      for (const c of COMPANIES) {
        const z = correlatedShock(c.beta, zm, zs[c.sector as SectorId], rng.normal());
        let p = gbmStep(prices[c.ticker], c.drift, c.volatility, dt, z);
        if (jumpTicker === c.ticker && s === Math.floor(SUBSTEPS / 3)) p *= 1 + jumpSize;
        prices[c.ticker] = p;
        high[c.ticker] = Math.max(high[c.ticker], p);
        low[c.ticker] = Math.min(low[c.ticker], p);
      }
    }
    for (const c of COMPANIES) {
      const close = prices[c.ticker];
      const ret = Math.abs(close / open[c.ticker] - 1);
      const v = Math.round(c.avgVolume * Math.exp(rng.normal() * 0.35) * (1 + ret * 15));
      out[c.ticker].push({ t: d, o: open[c.ticker], h: high[c.ticker], l: low[c.ticker], c: close, v });
    }
  }
  // Remise à l'échelle : la dernière clôture = prix de départ
  for (const c of COMPANIES) {
    const series = out[c.ticker];
    const k = c.startPrice / series[series.length - 1].c;
    out[c.ticker] = series.map((x) => ({ ...x, o: x.o * k, h: x.h * k, l: x.l * k, c: x.c * k }));
  }
  return out;
}
