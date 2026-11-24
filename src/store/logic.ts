/**
 * Logique de partie, indépendante de React : avance du temps, exécution des ordres,
 * dividendes, bilans, missions, défis. Opère sur un « brouillon » (copie de l'état).
 */
import { BADGES } from '../data/badges';
import { CHALLENGE_BY_ID, isChallengeSuccess, type ChallengeId } from '../data/challenges';
import { COMPANIES, COMPANY_BY_TICKER, SECTOR_IDS } from '../data/companies';
import { EMPTY_COUNTERS, FEATURE_LEVEL, MAX_LEVEL, MISSIONS, missionsForLevel, type Feature, type ProgressContext } from '../data/levels';
import { LESSON_BY_LEVEL } from '../data/lessons';
import { DAYS_PER_MONTH, DAYS_PER_WEEK } from '../engine/calendar';
import { bestAndWorst, coachTips } from '../engine/coach';
import { TICKS_PER_DAY } from '../engine/gbm';
import { addNews, cloneMarket, createMarket, currentPrices, stepTick } from '../engine/market';
import { createRng, randomSeed } from '../engine/random';
import { maxDrawdown, relativePerformance } from '../engine/stats';
import {
  executeTrade,
  findTriggeredOrders,
  portfolioValue,
  round2,
  STARTING_CASH,
  type PendingOrder,
  type Transaction,
} from '../engine/trading';
import type { MarketState, NewsItem } from '../engine/types';
import type { GameData, OrderRequest, OrderResult, PersistedState, Toast } from './types';

export const SAVE_VERSION = 1;
export const VOLATILE_MULT = 1.8;

export type Draft = PersistedState & { toasts: Toast[] };

let toastId = 1;
export function pushToast(d: Draft, t: Omit<Toast, 'id'>) {
  d.toasts = [...d.toasts, { ...t, id: toastId++ }].slice(-4);
}

export function newGameData(seed = randomSeed()): GameData {
  const market = createMarket(seed);
  return {
    market,
    cash: STARTING_CASH,
    positions: {},
    orders: [],
    transactions: [],
    dividends: [],
    snapshots: [{ day: market.day - 1, value: STARTING_CASH, cash: STARTING_CASH, index: market.index.value }],
    startDay: market.day,
    startValue: STARTING_CASH,
    startIndex: market.index.value,
    level: 1,
    levelReachedDay: { 1: market.day },
    completedMissions: [],
    passedLessons: [],
    badges: [],
    counters: { ...EMPTY_COUNTERS },
    reports: [],
    challengeResults: [],
    monthWindowStart: null,
    nextTxId: 1,
  };
}

export function newPersistedState(): PersistedState {
  return {
    ...newGameData(),
    version: SAVE_VERSION,
    settings: { sandbox: false, volatileMode: false, volatileSince: null, speed: 1 },
    tutorial: { done: false, active: true, step: 0 },
    challenge: null,
    unreadReportId: null,
    pendingLevelUp: null,
    lastChallengeResult: null,
  };
}

export function extractGameData(s: PersistedState): GameData {
  return {
    market: s.market,
    cash: s.cash,
    positions: s.positions,
    orders: s.orders,
    transactions: s.transactions,
    dividends: s.dividends,
    snapshots: s.snapshots,
    startDay: s.startDay,
    startValue: s.startValue,
    startIndex: s.startIndex,
    level: s.level,
    levelReachedDay: s.levelReachedDay,
    completedMissions: s.completedMissions,
    passedLessons: s.passedLessons,
    badges: s.badges,
    counters: s.counters,
    reports: s.reports,
    challengeResults: s.challengeResults,
    monthWindowStart: s.monthWindowStart,
    nextTxId: s.nextTxId,
  };
}

export function isUnlocked(s: Pick<PersistedState, 'level' | 'settings'>, f: Feature): boolean {
  return s.settings.sandbox || s.level >= FEATURE_LEVEL[f];
}

export const fmtEur = (x: number) =>
  new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(x);

// ————————————————————————————————————————————— Ordres

/** Une actualité récente (aujourd'hui ou la veille) concerne-t-elle cette action ? */
function recentNews(news: NewsItem[], ticker: string, day: number): NewsItem[] {
  const sector = COMPANY_BY_TICKER[ticker].sector;
  return news.filter((n) => (n.day === day || n.day === day - 1) && (n.ticker === ticker || (!n.ticker && (n.sector === sector || !n.sector))));
}

function recordTransaction(d: Draft, tx: Transaction) {
  d.transactions = [...d.transactions, tx];
  if (tx.side === 'sell' && tx.effect === 'open') d.counters = { ...d.counters, shortsOpened: d.counters.shortsOpened + 1 };
  const related = recentNews(d.market.news, tx.ticker, tx.day);
  if (related.some((n) => !n.isFake)) d.counters = { ...d.counters, newsReactions: d.counters.newsReactions + 1 };
  if (related.some((n) => n.isFake)) d.counters = { ...d.counters, fakeNewsReactions: d.counters.fakeNewsReactions + 1 };
}

/** Supprime les stop-loss / take-profit devenus sans objet et ajuste leurs quantités */
function pruneProtectiveOrders(d: Draft) {
  d.orders = d.orders
    .map((o) => {
      if (o.type === 'limit') return o;
      const pos = d.positions[o.ticker];
      const held = pos ? (o.side === 'sell' ? Math.max(0, pos.qty) : Math.max(0, -pos.qty)) : 0;
      return held === 0 ? null : { ...o, qty: Math.min(o.qty, held) };
    })
    .filter((o): o is PendingOrder => o !== null);
}

export function placeOrder(d: Draft, req: OrderRequest): OrderResult {
  const m = d.market;
  const price = m.stocks[req.ticker]?.price;
  if (price === undefined) return { ok: false, error: 'Action inconnue.' };
  if (!Number.isInteger(req.qty) || req.qty <= 0) return { ok: false, error: 'La quantité doit être un nombre entier positif.' };
  const prices = currentPrices(m);

  if (req.type === 'market') {
    const r = executeTrade(d, {
      id: `t${d.nextTxId}`,
      ticker: req.ticker,
      side: req.side,
      qty: req.qty,
      price,
      day: m.day,
      tick: m.tick,
      orderType: 'market',
      allowShort: isUnlocked(d, 'short'),
      prices,
      note: req.note,
    });
    if (!r.ok || !r.transaction) return { ok: false, error: r.error };
    d.nextTxId += 1;
    d.cash = r.cash;
    d.positions = r.positions;
    recordTransaction(d, r.transaction);
    pruneProtectiveOrders(d);
    // Protections rattachées
    const closeSide = req.side === 'buy' ? 'sell' : 'buy';
    if (req.stopLoss && req.stopLoss > 0) addPending(d, { ticker: req.ticker, side: closeSide, qty: req.qty, type: 'stop', triggerPrice: req.stopLoss });
    if (req.takeProfit && req.takeProfit > 0) addPending(d, { ticker: req.ticker, side: closeSide, qty: req.qty, type: 'takeprofit', triggerPrice: req.takeProfit });
    const t = r.transaction;
    pushToast(d, {
      kind: 'success',
      title: `${t.side === 'buy' ? 'Achat' : 'Vente'} exécuté : ${t.qty} ${t.ticker}`,
      body: `à ${fmtEur(t.price)} — frais ${fmtEur(t.fees)}${t.realizedPnl !== undefined ? ` — résultat ${fmtEur(t.realizedPnl)}` : ''}`,
    });
    return { ok: true };
  }

  // Ordres en attente
  const feature: Feature = req.type === 'limit' ? 'limit' : 'stopTakeProfit';
  if (!isUnlocked(d, feature)) return { ok: false, error: `Ce type d’ordre se débloque au niveau ${FEATURE_LEVEL[feature]}.` };
  const trig = req.triggerPrice ?? 0;
  if (!(trig > 0)) return { ok: false, error: 'Indique un prix de déclenchement valide.' };
  const pos = d.positions[req.ticker];
  if (req.type !== 'limit') {
    const held = pos ? (req.side === 'sell' ? Math.max(0, pos.qty) : Math.max(0, -pos.qty)) : 0;
    if (held < req.qty) return { ok: false, error: 'Un stop-loss ou un take-profit protège une position existante : quantité insuffisante.' };
    const isLong = req.side === 'sell';
    if (req.type === 'stop' && (isLong ? trig >= price : trig <= price))
      return { ok: false, error: isLong ? 'Le stop-loss doit être sous le cours actuel.' : 'Le stop d’un short doit être au-dessus du cours actuel.' };
    if (req.type === 'takeprofit' && (isLong ? trig <= price : trig >= price))
      return { ok: false, error: isLong ? 'Le take-profit doit être au-dessus du cours actuel.' : 'Le take-profit d’un short doit être sous le cours actuel.' };
  }
  addPending(d, { ticker: req.ticker, side: req.side, qty: req.qty, type: req.type, triggerPrice: trig, note: req.note });
  pushToast(d, { kind: 'info', title: 'Ordre enregistré', body: `${labelOrderType(req.type)} ${req.side === 'buy' ? 'achat' : 'vente'} ${req.qty} ${req.ticker} à ${fmtEur(trig)}` });
  return { ok: true };
}

export function labelOrderType(t: string): string {
  return t === 'limit' ? 'Limite' : t === 'stop' ? 'Stop-loss' : t === 'takeprofit' ? 'Take-profit' : 'Au marché';
}

function addPending(d: Draft, o: Omit<PendingOrder, 'id' | 'createdDay'>) {
  const order: PendingOrder = { ...o, triggerPrice: round2(o.triggerPrice), id: `o${d.nextTxId++}`, createdDay: d.market.day };
  d.orders = [...d.orders, order];
  const c = { ...d.counters };
  if (o.type === 'stop') c.stopLossPlaced++;
  if (o.type === 'takeprofit') c.takeProfitPlaced++;
  if (o.type === 'limit') c.limitUsed++;
  d.counters = c;
}

function processOrders(d: Draft) {
  if (d.orders.length === 0) return;
  const prices = currentPrices(d.market);
  const triggered = findTriggeredOrders(d.orders, prices);
  for (const o of triggered) {
    if (!d.orders.some((x) => x.id === o.id)) continue; // supprimé entre-temps
    d.orders = d.orders.filter((x) => x.id !== o.id);
    const r = executeTrade(d, {
      id: `t${d.nextTxId}`,
      ticker: o.ticker,
      side: o.side,
      qty: o.qty,
      price: prices[o.ticker],
      day: d.market.day,
      tick: d.market.tick,
      orderType: o.type,
      allowShort: isUnlocked(d, 'short'),
      prices,
      note: o.note,
    });
    if (r.ok && r.transaction) {
      d.nextTxId++;
      d.cash = r.cash;
      d.positions = r.positions;
      recordTransaction(d, r.transaction);
      pruneProtectiveOrders(d);
      const t = r.transaction;
      pushToast(d, {
        kind: o.type === 'stop' ? 'error' : 'success',
        title: `${labelOrderType(o.type)} déclenché : ${t.side === 'buy' ? 'achat' : 'vente'} de ${t.qty} ${t.ticker}`,
        body: `à ${fmtEur(t.price)}${t.realizedPnl !== undefined ? ` — résultat ${fmtEur(t.realizedPnl)}` : ''}`,
      });
    } else {
      pushToast(d, { kind: 'error', title: `Ordre ${labelOrderType(o.type).toLowerCase()} annulé (${o.ticker})`, body: r.error });
    }
  }
}

export function cancelOrder(d: Draft, id: string) {
  d.orders = d.orders.filter((o) => o.id !== id);
}

// ————————————————————————————————————————————— Temps

export function advance(d: Draft, ticks: number) {
  const m: MarketState = cloneMarket(d.market);
  const rng = createRng(m.rngState);
  m.volMult = d.settings.volatileMode ? VOLATILE_MULT : 1;
  d.market = m;
  for (let i = 0; i < ticks; i++) {
    const events = stepTick(m, rng);
    for (const e of events) {
      if (e.type === 'news') {
        const owned = e.news.ticker && d.positions[e.news.ticker];
        if (owned || Math.abs(e.news.impact) >= 0.06) {
          pushToast(d, { kind: 'news', title: e.news.title, body: owned ? 'Tu détiens cette action.' : undefined });
        }
      } else if (e.type === 'dividend') {
        const pos = d.positions[e.ticker];
        if (pos) {
          const amount = round2(pos.qty * e.perShare);
          d.cash = round2(d.cash + amount);
          d.dividends = [...d.dividends, { day: e.day, ticker: e.ticker, qty: pos.qty, perShare: e.perShare, amount }];
          if (amount > 0) d.counters = { ...d.counters, dividendsReceived: d.counters.dividendsReceived + 1 };
          pushToast(d, {
            kind: amount >= 0 ? 'success' : 'error',
            title: amount >= 0 ? `Dividende reçu : ${e.ticker}` : `Dividende payé (vente à découvert) : ${e.ticker}`,
            body: `${fmtEur(e.perShare)} × ${Math.abs(pos.qty)} = ${fmtEur(amount)}`,
          });
        }
      } else if (e.type === 'dayEnd') {
        processOrders(d);
        onDayEnd(d, e.day);
        if (d.challenge && d.market.day >= d.challenge.endDay) {
          finishChallenge(d);
          return;
        }
      }
    }
    processOrders(d);
  }
  if (!d.challenge) evaluateProgress(d);
}

export function ticksToDayEnd(d: Draft): number {
  return TICKS_PER_DAY - d.market.tick;
}

function onDayEnd(d: Draft, day: number) {
  const prices = currentPrices(d.market);
  const value = portfolioValue(d, prices);
  d.snapshots = [...d.snapshots, { day, value, cash: d.cash, index: d.market.index.value }];
  if (d.challenge) return;

  const eligible = (f: Feature) => isUnlocked(d, f);
  const elapsed = day + 1 - d.startDay;

  // Bilan hebdomadaire
  if (elapsed > 0 && elapsed % DAYS_PER_WEEK === 0) {
    const weekStart = day - DAYS_PER_WEEK + 1;
    const startSnap = [...d.snapshots].reverse().find((s) => s.day < weekStart) ?? d.snapshots[0];
    const weekTx = d.transactions.filter((t) => t.day >= weekStart && t.day <= day);
    const perf = relativePerformance(startSnap.value, value, startSnap.index, d.market.index.value);
    const invested = Object.keys(d.positions).length > 0 || weekTx.length > 0;
    const c = { ...d.counters };
    if (invested && perf.portfolio > -0.05 && eligible('stopTakeProfit')) c.weeksWithoutBigLoss++;
    if (invested && perf.portfolio > -0.05 && d.settings.volatileMode && d.settings.volatileSince !== null && d.settings.volatileSince <= weekStart)
      c.volatileWeeks++;
    d.counters = c;
    const report = {
      id: `w${elapsed / DAYS_PER_WEEK}-${day}`,
      week: elapsed / DAYS_PER_WEEK,
      startDay: weekStart,
      endDay: day,
      startValue: startSnap.value,
      endValue: value,
      ret: perf.portfolio,
      indexRet: perf.index,
      trades: weekTx.length,
      ...bestAndWorst(weekTx, d.positions, prices),
      tips: coachTips({
        weekTx,
        allTx: d.transactions,
        positions: d.positions,
        cash: d.cash,
        prices,
        news: d.market.news,
        stopLossTickers: d.orders.filter((o) => o.type === 'stop').map((o) => o.ticker),
        stopLossUnlocked: eligible('stopTakeProfit'),
      }),
    };
    d.reports = [...d.reports, report].slice(-52);
    d.unreadReportId = report.id;
  }

  // Fenêtre mensuelle (niveau 4)
  if (eligible('advancedStats')) {
    if (d.monthWindowStart === null) d.monthWindowStart = day;
    else if (day - d.monthWindowStart >= DAYS_PER_MONTH) {
      const start = d.monthWindowStart;
      const win = d.snapshots.filter((s) => s.day >= start && s.day <= day);
      if (win.length >= 2) {
        const perf = relativePerformance(win[0].value, win[win.length - 1].value, win[0].index, win[win.length - 1].index);
        const invested = d.transactions.some((t) => t.day > start);
        const c = { ...d.counters };
        if (invested && perf.excess > 0) c.monthsBeatingIndex++;
        if (invested && maxDrawdown(win.map((s) => s.value)) < 0.1) c.monthsLowDrawdown++;
        d.counters = c;
      }
      d.monthWindowStart = day;
    }
  }
}

// ————————————————————————————————————————————— Progression

export function progressContext(s: PersistedState): ProgressContext {
  return {
    level: s.level,
    transactions: s.transactions,
    positions: s.positions,
    counters: s.counters,
    passedLessons: s.passedLessons,
    completedMissions: s.completedMissions,
  };
}

export function canLevelUp(s: PersistedState): boolean {
  if (s.level >= MAX_LEVEL) return false;
  const lesson = LESSON_BY_LEVEL[s.level];
  return missionsForLevel(s.level).every((m) => s.completedMissions.includes(m.id)) && (!lesson || s.passedLessons.includes(lesson.id));
}

export function evaluateProgress(d: Draft) {
  const ctx = progressContext(d);
  const done = new Set(d.completedMissions);
  for (const m of MISSIONS) {
    if (m.level > d.level || done.has(m.id)) continue;
    if (m.progress(ctx) >= m.target) {
      done.add(m.id);
      pushToast(d, { kind: 'mission', title: `Mission accomplie : ${m.title}`, body: `Niveau ${m.level}` });
    }
  }
  if (done.size !== d.completedMissions.length) d.completedMissions = [...done];

  while (canLevelUp(d)) {
    d.level += 1;
    d.levelReachedDay = { ...d.levelReachedDay, [d.level]: d.market.day };
    d.pendingLevelUp = d.level;
    pushToast(d, { kind: 'mission', title: `Niveau ${d.level} débloqué !`, body: 'Nouvelle leçon et nouvelles fonctionnalités disponibles.' });
  }

  const badgeCtx = { ...progressContext(d), challengeResults: d.challengeResults, reportsCount: d.reports.length };
  const owned = new Set(d.badges);
  for (const b of BADGES) {
    if (!owned.has(b.id) && b.check(badgeCtx)) {
      owned.add(b.id);
      pushToast(d, { kind: 'badge', title: `Badge obtenu : ${b.emoji} ${b.title}`, body: b.description });
    }
  }
  if (owned.size !== d.badges.length) d.badges = [...owned];
}

export function passLesson(d: Draft, lessonId: string) {
  if (!d.passedLessons.includes(lessonId)) d.passedLessons = [...d.passedLessons, lessonId];
  evaluateProgress(d);
}

// ————————————————————————————————————————————— Défis

export function startChallenge(d: Draft, id: ChallengeId) {
  if (d.challenge) return;
  const saved = extractGameData(d);
  const def = CHALLENGE_BY_ID[id];
  const fresh = newGameData();
  const m = fresh.market;
  const rng = createRng(m.rngState ^ 0x5bd1e995);
  let cash = def.startCash;
  const positions: GameData['positions'] = {};
  let bubbleTicker: string | undefined;
  const news = (title: string, body: string, extra: Partial<NewsItem> = {}) => {
    const n: NewsItem = { id: `n${m.nextId++}`, day: m.day, tick: 0, kind: 'macro', title, body, impact: 0, isFake: false, ...extra };
    addNews(m, n, undefined, rng);
  };

  if (id === 'krach') {
    const picks = ['CLDR', 'BKRM', 'AERO', 'LUMA'];
    for (const t of picks) {
      const price = m.stocks[t].price;
      const qty = Math.floor(2000 / price);
      cash -= qty * price;
      positions[t] = { ticker: t, qty, avgPrice: price, pru: price, openedDay: m.day };
    }
    cash = round2(cash);
    m.effects.push({ id: 'krach', all: true, driftPerTick: Math.log(0.7) / (5 * TICKS_PER_DAY), volMult: 1.6, delay: TICKS_PER_DAY, ticksLeft: 5 * TICKS_PER_DAY });
    news('Les marchés deviennent nerveux', 'Plusieurs indicateurs fictifs inquiètent les investisseurs. Le défi Krach commence !');
  } else if (id === 'bulle') {
    bubbleTicker = rng.pick(['NOVA', 'QBIT', 'CLDR']);
    const rise = 8 * TICKS_PER_DAY;
    const delay = 30;
    const burstDelay = delay + rise + rng.int(0, 2 * TICKS_PER_DAY);
    m.effects.push({ id: 'bulle-up', ticker: bubbleTicker, driftPerTick: Math.log(2.4) / rise, volMult: 1.3, delay, ticksLeft: rise });
    m.effects.push({ id: 'bulle-down', ticker: bubbleTicker, driftPerTick: Math.log(0.35) / (2 * TICKS_PER_DAY), volMult: 1.5, delay: burstDelay, ticksLeft: 2 * TICKS_PER_DAY });
    const c = COMPANY_BY_TICKER[bubbleTicker];
    news(`Engouement spectaculaire autour de ${c.name}`, 'Les forums s’enflamment, tout le monde veut en acheter. Jusqu’où ira la hausse ?', { ticker: bubbleTicker, sector: c.sector, kind: 'produit' });
  } else {
    news('Défi Budget 1 000 €', 'Avec un petit capital, chaque euro de frais compte. Bonne chance !');
  }

  const prices = currentPrices(m);
  const startValue = portfolioValue({ cash, positions }, prices);
  d.market = m;
  d.cash = cash;
  d.positions = positions;
  d.orders = [];
  d.transactions = [];
  d.dividends = [];
  d.snapshots = [{ day: m.day - 1, value: startValue, cash, index: m.index.value }];
  d.startDay = m.day;
  d.startValue = startValue;
  d.startIndex = m.index.value;
  d.nextTxId = 1;
  d.challenge = { id, startDay: m.day, endDay: m.day + def.durationDays, startValue, startIndex: m.index.value, bubbleTicker, saved };
  pushToast(d, { kind: 'info', title: `Défi ${def.title} lancé`, body: def.goal });
}

function restore(d: Draft, g: GameData) {
  Object.assign(d, g);
  d.challenge = null;
}

export function finishChallenge(d: Draft) {
  const ch = d.challenge;
  if (!ch) return;
  const value = portfolioValue(d, currentPrices(d.market));
  const portfolioReturn = value / ch.startValue - 1;
  const indexReturn = d.market.index.value / ch.startIndex - 1;
  const success = isChallengeSuccess(ch.id, portfolioReturn, indexReturn);
  const result = { id: ch.id, day: ch.saved.market.day, success, portfolioReturn, indexReturn };
  restore(d, ch.saved);
  d.challengeResults = [...d.challengeResults, result];
  if (success) d.counters = { ...d.counters, challengesWon: d.counters.challengesWon + 1 };
  d.lastChallengeResult = result;
  evaluateProgress(d);
}

export function abandonChallenge(d: Draft) {
  if (d.challenge) restore(d, d.challenge.saved);
}

// ————————————————————————————————————————————— Divers

/** Toutes les entreprises, pour vérifier que les données sont cohérentes */
export const ALL_TICKERS = COMPANIES.map((c) => c.ticker);
export const ALL_SECTORS = SECTOR_IDS;
