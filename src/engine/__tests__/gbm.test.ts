import { describe, expect, it } from 'vitest';
import { correlatedShock, gbmStep, theoreticalCorrelation } from '../gbm';
import { createRng } from '../random';

describe('mouvement brownien géométrique', () => {
  it('sans aléa ni volatilité, applique exactement la tendance', () => {
    expect(gbmStep(100, 0.01, 0, 1, 0)).toBeCloseTo(100 * Math.exp(0.01), 10);
  });

  it('reste strictement positif', () => {
    const r = createRng(3);
    let p = 10;
    for (let i = 0; i < 10_000; i++) {
      p = gbmStep(p, 0, 0.08, 1 / 60, r.normal());
      expect(p).toBeGreaterThan(0);
    }
  });

  it('a une espérance égale à S0·exp(μ·T)', () => {
    const r = createRng(11);
    const n = 40_000;
    const mu = 0.002;
    const sigma = 0.02;
    let sum = 0;
    for (let i = 0; i < n; i++) sum += gbmStep(100, mu, sigma, 1, r.normal());
    expect(sum / n).toBeCloseTo(100 * Math.exp(mu), 1);
  });

  it('a une volatilité des rendements log égale à σ√dt', () => {
    const r = createRng(5);
    const sigma = 0.03;
    const dt = 1 / 60;
    const n = 40_000;
    const rets: number[] = [];
    for (let i = 0; i < n; i++) rets.push(Math.log(gbmStep(100, 0, sigma, dt, r.normal()) / 100));
    const m = rets.reduce((a, b) => a + b, 0) / n;
    const sd = Math.sqrt(rets.reduce((a, b) => a + (b - m) ** 2, 0) / n);
    expect(sd).toBeCloseTo(sigma * Math.sqrt(dt), 3);
  });

  it('corrèle davantage deux actions du même secteur', () => {
    const r = createRng(9);
    const n = 30_000;
    const pairs = { same: [] as [number, number][], diff: [] as [number, number][] };
    for (let i = 0; i < n; i++) {
      const zm = r.normal();
      const zs1 = r.normal();
      const zs2 = r.normal();
      const a = correlatedShock(0.6, zm, zs1, r.normal());
      const b = correlatedShock(0.6, zm, zs1, r.normal());
      const c = correlatedShock(0.6, zm, zs2, r.normal());
      pairs.same.push([a, b]);
      pairs.diff.push([a, c]);
    }
    const corr = (xs: [number, number][]) => {
      const mx = xs.reduce((s, [x]) => s + x, 0) / xs.length;
      const my = xs.reduce((s, [, y]) => s + y, 0) / xs.length;
      let cov = 0;
      let vx = 0;
      let vy = 0;
      for (const [x, y] of xs) {
        cov += (x - mx) * (y - my);
        vx += (x - mx) ** 2;
        vy += (y - my) ** 2;
      }
      return cov / Math.sqrt(vx * vy);
    };
    expect(corr(pairs.same)).toBeCloseTo(theoreticalCorrelation(0.6, 0.6, true), 1);
    expect(corr(pairs.diff)).toBeCloseTo(theoreticalCorrelation(0.6, 0.6, false), 1);
    expect(corr(pairs.same)).toBeGreaterThan(corr(pairs.diff));
  });
});
