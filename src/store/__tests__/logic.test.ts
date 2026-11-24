import { describe, expect, it } from 'vitest';
import * as L from '../logic';

const draft = (): L.Draft => ({ ...L.newPersistedState(), toasts: [] });

describe('logique de partie', () => {
  it('démarre avec 10 000 € et un historique', () => {
    const d = draft();
    expect(d.cash).toBe(10_000);
    expect(d.market.stocks.NOVA.candles.length).toBeGreaterThan(100);
  });

  it('achète au marché et accomplit la mission « premier achat »', () => {
    const d = draft();
    const r = L.placeOrder(d, { ticker: 'NOVA', side: 'buy', qty: 5, type: 'market', note: 'Test' });
    expect(r.ok).toBe(true);
    expect(d.positions.NOVA.qty).toBe(5);
    L.evaluateProgress(d);
    expect(d.completedMissions).toContain('m1_buy');
  });

  it('refuse le stop-loss au niveau 1, l’accepte en mode bac à sable', () => {
    const d = draft();
    L.placeOrder(d, { ticker: 'NOVA', side: 'buy', qty: 5, type: 'market' });
    const p = d.market.stocks.NOVA.price;
    expect(L.placeOrder(d, { ticker: 'NOVA', side: 'sell', qty: 5, type: 'stop', triggerPrice: p * 0.9 }).ok).toBe(false);
    d.settings = { ...d.settings, sandbox: true };
    expect(L.placeOrder(d, { ticker: 'NOVA', side: 'sell', qty: 5, type: 'stop', triggerPrice: p * 0.9 }).ok).toBe(true);
    expect(L.placeOrder(d, { ticker: 'NOVA', side: 'sell', qty: 5, type: 'stop', triggerPrice: p * 1.1 }).ok).toBe(false);
  });

  it('exécute un stop-loss quand le cours chute et supprime le take-profit orphelin', () => {
    const d = draft();
    d.settings = { ...d.settings, sandbox: true };
    const p = d.market.stocks.NOVA.price;
    L.placeOrder(d, { ticker: 'NOVA', side: 'buy', qty: 10, type: 'market', stopLoss: p * 0.999, takeProfit: p * 5 });
    expect(d.orders).toHaveLength(2);
    // On force une forte baisse
    d.market = { ...d.market, effects: [{ id: 'x', ticker: 'NOVA', driftPerTick: -0.05, delay: 0, ticksLeft: 100 }] };
    L.advance(d, 5);
    expect(d.positions.NOVA).toBeUndefined();
    expect(d.orders).toHaveLength(0);
    expect(d.transactions.at(-1)?.orderType).toBe('stop');
  });

  it('passe au niveau 2 après les missions et le quiz', () => {
    const d = draft();
    d.completedMissions = ['m1_buy', 'm1_gain', 'm1_three'];
    L.evaluateProgress(d);
    expect(d.level).toBe(1);
    L.passLesson(d, 'l1');
    expect(d.level).toBe(2);
    expect(d.pendingLevelUp).toBe(2);
  });

  it('produit un bilan hebdomadaire au bout de 5 jours', () => {
    const d = draft();
    for (let i = 0; i < 5; i++) L.advance(d, L.ticksToDayEnd(d));
    expect(d.reports).toHaveLength(1);
    expect(d.reports[0].tips.length).toBeGreaterThan(0);
    expect(d.snapshots).toHaveLength(6);
  });

  it('lance un défi puis restaure la partie principale', () => {
    const d = draft();
    L.placeOrder(d, { ticker: 'NOVA', side: 'buy', qty: 3, type: 'market' });
    L.startChallenge(d, 'krach');
    expect(d.challenge).not.toBeNull();
    expect(Object.keys(d.positions)).toHaveLength(4);
    for (let i = 0; i < 10; i++) L.advance(d, L.ticksToDayEnd(d));
    expect(d.challenge).toBeNull();
    expect(d.positions.NOVA.qty).toBe(3);
    expect(d.challengeResults).toHaveLength(1);
    expect(d.lastChallengeResult?.portfolioReturn).toBeLessThan(0);
  });
});
