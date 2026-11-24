import { describe, expect, it } from 'vitest';
import { createRng } from '../random';

describe('générateur aléatoire', () => {
  it('est reproductible avec la même graine', () => {
    const a = createRng(42);
    const b = createRng(42);
    for (let i = 0; i < 100; i++) expect(a.next()).toBe(b.next());
  });

  it('reprend à partir de son état sauvegardé', () => {
    const a = createRng(7);
    a.next();
    a.next();
    const b = createRng(a.state);
    expect(b.next()).toBe(a.next());
  });

  it('produit une loi normale de moyenne ~0 et variance ~1', () => {
    const r = createRng(1);
    const n = 50_000;
    let s = 0;
    let s2 = 0;
    for (let i = 0; i < n; i++) {
      const z = r.normal();
      s += z;
      s2 += z * z;
    }
    const mean = s / n;
    expect(Math.abs(mean)).toBeLessThan(0.02);
    expect(Math.abs(s2 / n - mean * mean - 1)).toBeLessThan(0.03);
  });
});
