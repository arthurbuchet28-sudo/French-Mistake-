import { describe, expect, it } from 'vitest';
import {
  addToLong,
  computeFees,
  executeTrade,
  findTriggeredOrders,
  portfolioValue,
  quote,
  reduceLong,
  unrealizedPnl,
  unrealizedPct,
  type PendingOrder,
} from '../trading';
import { maxDrawdown, tradeStats } from '../stats';

describe('frais de courtage', () => {
  it('applique 0,5 % du montant', () => {
    expect(computeFees(1000)).toBe(5);
    expect(computeFees(2345.67)).toBe(11.73);
  });
  it('applique un minimum de 1 €', () => {
    expect(computeFees(50)).toBe(1);
    expect(computeFees(199.99)).toBe(1);
    expect(computeFees(200)).toBe(1);
    expect(computeFees(201)).toBe(1.01);
  });
  it('ne facture rien pour un montant nul', () => {
    expect(computeFees(0)).toBe(0);
  });
  it('calcule le total à payer ou à recevoir', () => {
    expect(quote('buy', 10, 100)).toEqual({ amount: 1000, fees: 5, total: 1005 });
    expect(quote('sell', 10, 100)).toEqual({ amount: 1000, fees: 5, total: 995 });
  });
});

describe('PRU (prix de revient unitaire)', () => {
  it('inclut les frais d’achat', () => {
    const p = addToLong(undefined, 'NOVA', 10, 100, 5, 0);
    expect(p.avgPrice).toBe(100);
    expect(p.pru).toBeCloseTo(100.5, 10);
  });
  it('fait la moyenne pondérée lors d’un renforcement', () => {
    let p = addToLong(undefined, 'NOVA', 10, 100, 5, 0); // coût 1005
    p = addToLong(p, 'NOVA', 30, 80, 12, 1); // coût 2412
    expect(p.qty).toBe(40);
    expect(p.avgPrice).toBeCloseTo((1000 + 2400) / 40, 10);
    expect(p.pru).toBeCloseTo((1005 + 2412) / 40, 10);
    expect(p.openedDay).toBe(0);
  });
  it('ne change pas lors d’une vente partielle', () => {
    const p = addToLong(undefined, 'NOVA', 10, 100, 5, 0);
    const r = reduceLong(p, 4, 110, 2.2);
    expect(r.position?.qty).toBe(6);
    expect(r.position?.pru).toBe(p.pru);
  });
});

describe('P&L', () => {
  it('calcule la plus-value réalisée nette de tous les frais', () => {
    const p = addToLong(undefined, 'NOVA', 10, 100, 5, 0);
    const r = reduceLong(p, 10, 110, 5.5);
    // 1100 − 5,5 − 1005 = 89,5
    expect(r.realizedPnl).toBe(89.5);
    expect(r.position).toBeUndefined();
  });
  it('calcule une moins-value réalisée', () => {
    const p = addToLong(undefined, 'NOVA', 10, 100, 5, 0);
    expect(reduceLong(p, 10, 90, 4.5).realizedPnl).toBe(-109.5); // 900 − 4,5 − 1005
  });
  it('calcule la plus-value latente', () => {
    const p = addToLong(undefined, 'NOVA', 10, 100, 5, 0);
    expect(unrealizedPnl(p, 120)).toBeCloseTo(195, 10);
    expect(unrealizedPct(p, 120)).toBeCloseTo(120 / 100.5 - 1, 10);
  });
  it('calcule le P&L d’une vente à découvert', () => {
    const base = { cash: 10_000, positions: {} };
    const prices = { NOVA: 100 };
    const open = executeTrade(base, { id: 't1', ticker: 'NOVA', side: 'sell', qty: 10, price: 100, day: 0, tick: 0, orderType: 'market', allowShort: true, prices });
    expect(open.ok).toBe(true);
    expect(open.positions.NOVA.qty).toBe(-10);
    expect(open.cash).toBe(10_995);
    expect(unrealizedPnl(open.positions.NOVA, 90)).toBeCloseTo(10 * (99.5 - 90), 10);
    const close = executeTrade(open, { id: 't2', ticker: 'NOVA', side: 'buy', qty: 10, price: 90, day: 1, tick: 0, orderType: 'market', allowShort: true, prices: { NOVA: 90 } });
    // 10 × 99,5 − 900 − 4,5 = 90,5
    expect(close.transaction?.realizedPnl).toBe(90.5);
    expect(close.positions.NOVA).toBeUndefined();
    expect(close.cash).toBe(10_090.5);
  });
});

describe('exécution des ordres', () => {
  const empty = { cash: 1000, positions: {} };
  const base = { id: 'x', ticker: 'NOVA', day: 0, tick: 0, orderType: 'market' as const, allowShort: false, prices: { NOVA: 50 } };

  it('débite prix + frais à l’achat et met à jour la valeur', () => {
    const r = executeTrade(empty, { ...base, side: 'buy', qty: 10, price: 50 });
    expect(r.ok).toBe(true);
    expect(r.cash).toBe(1000 - 500 - 2.5);
    expect(portfolioValue(r, { NOVA: 50 })).toBe(997.5);
  });
  it('refuse un achat sans liquidités suffisantes', () => {
    const r = executeTrade(empty, { ...base, side: 'buy', qty: 20, price: 50 });
    expect(r.ok).toBe(false);
    expect(r.cash).toBe(1000);
  });
  it('refuse une vente sans position si la vente à découvert est verrouillée', () => {
    expect(executeTrade(empty, { ...base, side: 'sell', qty: 1, price: 50 }).ok).toBe(false);
  });
  it('refuse de vendre plus que la position', () => {
    const r = executeTrade(empty, { ...base, side: 'buy', qty: 5, price: 50 });
    expect(executeTrade(r, { ...base, side: 'sell', qty: 6, price: 50 }).ok).toBe(false);
  });
  it('refuse les quantités non entières', () => {
    expect(executeTrade(empty, { ...base, side: 'buy', qty: 1.5, price: 50 }).ok).toBe(false);
  });
  it('déclenche stop-loss, take-profit et ordres limites au bon moment', () => {
    const o = (type: PendingOrder['type'], side: PendingOrder['side'], triggerPrice: number): PendingOrder => ({
      id: `${type}-${side}`,
      ticker: 'NOVA',
      type,
      side,
      qty: 1,
      triggerPrice,
      createdDay: 0,
    });
    const orders = [o('stop', 'sell', 45), o('takeprofit', 'sell', 60), o('limit', 'buy', 48), o('limit', 'sell', 55)];
    expect(findTriggeredOrders(orders, { NOVA: 50 }).map((x) => x.id)).toEqual([]);
    expect(findTriggeredOrders(orders, { NOVA: 44 }).map((x) => x.id)).toEqual(['stop-sell', 'limit-buy']);
    expect(findTriggeredOrders(orders, { NOVA: 61 }).map((x) => x.id)).toEqual(['takeprofit-sell', 'limit-sell']);
  });
});

describe('statistiques', () => {
  it('calcule le drawdown maximum', () => {
    expect(maxDrawdown([100, 120, 90, 110, 130, 104])).toBeCloseTo(0.25, 10);
    expect(maxDrawdown([100, 101, 102])).toBe(0);
  });
  it('calcule taux de réussite, gain moyen et plus grosse perte', () => {
    const t = (pnl?: number) => ({ id: '', day: 0, tick: 0, ticker: 'A', side: 'sell' as const, effect: 'close' as const, qty: 1, price: 1, fees: 1, total: 1, orderType: 'market' as const, realizedPnl: pnl });
    const s = tradeStats([t(100), t(-50), t(20), t(-10), t(undefined)]);
    expect(s.closedTrades).toBe(4);
    expect(s.winRate).toBe(0.5);
    expect(s.avgGain).toBe(60);
    expect(s.avgLoss).toBe(-30);
    expect(s.biggestLoss).toBe(-50);
    expect(s.totalFees).toBe(5);
  });
});

import { coachTips } from '../coach';
import { addToLong as add } from '../trading';

describe('coach', () => {
  it('signale une concentration sectorielle', () => {
    const positions = { NOVA: add(undefined, 'NOVA', 100, 50, 25, 0), QBIT: add(undefined, 'QBIT', 100, 20, 10, 0) };
    const tips = coachTips({ weekTx: [], allTx: [], positions, cash: 1000, prices: { NOVA: 50, QBIT: 20 }, news: [], stopLossTickers: [], stopLossUnlocked: false });
    expect(tips.some((t) => t.includes('tech'))).toBe(true);
  });
});
