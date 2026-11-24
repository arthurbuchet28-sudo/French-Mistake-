import { describe, expect, it } from 'vitest';
import { COMPANIES } from '../../data/companies';
import { TICKS_PER_DAY } from '../gbm';
import { HISTORY_DAYS } from '../history';
import { cloneMarket, createMarket, stepTick } from '../market';
import { createRng } from '../random';
import { sma, aggregateTicks } from '../indicators';

describe('marché simulé', () => {
  it('génère 6 mois d’historique qui se terminent au prix de départ', () => {
    const m = createMarket(123);
    for (const c of COMPANIES) {
      const s = m.stocks[c.ticker];
      expect(s.candles).toHaveLength(HISTORY_DAYS);
      expect(s.candles[s.candles.length - 1].c).toBeCloseTo(c.startPrice, 6);
      for (const k of s.candles) {
        expect(k.h).toBeGreaterThanOrEqual(Math.max(k.o, k.c) - 1e-9);
        expect(k.l).toBeLessThanOrEqual(Math.min(k.o, k.c) + 1e-9);
        expect(k.v).toBeGreaterThan(0);
      }
    }
    expect(m.index.candles).toHaveLength(HISTORY_DAYS);
  });

  it('est déterministe pour une même graine', () => {
    const run = () => {
      let m = createMarket(77);
      const rng = createRng(m.rngState);
      for (let i = 0; i < 200; i++) {
        m = cloneMarket(m);
        stepTick(m, rng);
      }
      return m.stocks.NOVA.price;
    };
    expect(run()).toBe(run());
  });

  it('clôture une journée tous les 60 ticks avec une bougie cohérente', () => {
    const m = createMarket(5);
    const rng = createRng(m.rngState);
    const day = m.day;
    let ended = false;
    for (let i = 0; i < TICKS_PER_DAY; i++) {
      const ev = stepTick(m, rng);
      if (ev.some((e) => e.type === 'dayEnd')) ended = true;
    }
    expect(ended).toBe(true);
    expect(m.day).toBe(day + 1);
    expect(m.tick).toBe(0);
    const last = m.stocks.NOVA.candles[m.stocks.NOVA.candles.length - 1];
    expect(last.t).toBe(day);
    expect(m.stocks.NOVA.intraday).toHaveLength(1);
  });

  it('ne modifie pas le marché d’origine quand on travaille sur une copie', () => {
    const m = createMarket(8);
    const before = m.stocks.NOVA.price;
    const copy = cloneMarket(m);
    stepTick(copy, createRng(copy.rngState));
    expect(m.stocks.NOVA.price).toBe(before);
    expect(m.stocks.NOVA.intraday).toHaveLength(1);
  });

  it('verse un dividende chaque trimestre', () => {
    const m = createMarket(9);
    const rng = createRng(m.rngState);
    const dividends: string[] = [];
    for (let i = 0; i < TICKS_PER_DAY * 70; i++) {
      for (const e of stepTick(m, rng)) if (e.type === 'dividend') dividends.push(e.ticker);
    }
    expect(dividends).toContain('PTRX');
    expect(dividends).not.toContain('NOVA');
  });
});

describe('indicateurs', () => {
  it('calcule une moyenne mobile simple', () => {
    expect(sma([1, 2, 3, 4, 5], 3)).toEqual([null, null, 2, 3, 4]);
  });
  it('regroupe des ticks en bougies', () => {
    const c = aggregateTicks([10, 11, 9, 12, 13], 2);
    expect(c).toHaveLength(2);
    expect(c[0]).toMatchObject({ o: 10, h: 11, l: 9, c: 9 });
    expect(c[1]).toMatchObject({ o: 9, h: 13, l: 9, c: 13 });
  });
});
