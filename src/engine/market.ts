import { COMPANIES, COMPANY_BY_TICKER } from '../data/companies';
import { DAYS_PER_QUARTER } from './calendar';
import { correlatedShock, gbmStep, TICK_DT, TICKS_PER_DAY } from './gbm';
import { generateHistory, HISTORY_DAYS } from './history';
import { applyNewsShock, effectMatches, generateNews, NEWS_PER_DAY } from './news';
import { createRng, type Rng } from './random';
import type { ActiveEffect, Candle, MarketEvent, MarketState, NewsItem, StockState } from './types';
import { SECTOR_IDS } from '../data/companies';

/** Nombre maximal de bougies journalières conservées par action */
export const MAX_CANDLES = 400;
export const MAX_NEWS = 150;
export const INDEX_BASE = 1000;

export function indexValue(prices: Record<string, number>, base: Record<string, number>): number {
  let sum = 0;
  let n = 0;
  for (const t in base) {
    sum += prices[t] / base[t];
    n++;
  }
  return n === 0 ? INDEX_BASE : (INDEX_BASE * sum) / n;
}

/** Crée un marché neuf, avec 6 mois d'historique. */
export function createMarket(seed: number): MarketState {
  const rng = createRng(seed);
  const history = generateHistory(rng, HISTORY_DAYS);
  const base: Record<string, number> = {};
  for (const c of COMPANIES) base[c.ticker] = history[c.ticker][0].o;

  const indexCandles: Candle[] = [];
  for (let d = 0; d < HISTORY_DAYS; d++) {
    const pick = (k: 'o' | 'h' | 'l' | 'c') =>
      indexValue(Object.fromEntries(COMPANIES.map((c) => [c.ticker, history[c.ticker][d][k]])), base);
    const o = pick('o');
    const c = pick('c');
    indexCandles.push({ t: d, o, c, h: Math.max(o, c, pick('h')), l: Math.min(o, c, pick('l')), v: 0 });
  }

  const stocks: Record<string, StockState> = {};
  for (const c of COMPANIES) {
    const p = c.startPrice;
    stocks[c.ticker] = {
      ticker: c.ticker,
      price: p,
      prevClose: p,
      candles: history[c.ticker],
      intraday: [p],
      dayOpen: p,
      dayHigh: p,
      dayLow: p,
      dayVolume: 0,
    };
  }
  const prices = Object.fromEntries(COMPANIES.map((c) => [c.ticker, c.startPrice]));
  const iv = indexValue(prices, base);
  return {
    rngState: rng.state,
    day: HISTORY_DAYS,
    tick: 0,
    stocks,
    index: {
      value: iv,
      prevClose: iv,
      candles: indexCandles,
      intraday: [iv],
      dayOpen: iv,
      dayHigh: iv,
      dayLow: iv,
      base,
    },
    news: [],
    effects: [],
    volMult: 1,
    nextId: 1,
  };
}

/**
 * Copie « assez profonde » pour l'immutabilité côté React :
 * les objets qui changent à chaque tick sont copiés, les bougies passées sont partagées.
 */
export function cloneMarket(m: MarketState): MarketState {
  const stocks: Record<string, StockState> = {};
  for (const t in m.stocks) {
    const s = m.stocks[t];
    stocks[t] = { ...s, intraday: s.intraday.slice() };
  }
  return {
    ...m,
    stocks,
    index: { ...m.index, intraday: m.index.intraday.slice() },
    news: m.news.slice(),
    effects: m.effects.map((e) => ({ ...e })),
  };
}

export function currentPrices(m: MarketState): Record<string, number> {
  const out: Record<string, number> = {};
  for (const t in m.stocks) out[t] = m.stocks[t].price;
  return out;
}

export function addNews(m: MarketState, news: NewsItem, effect: ActiveEffect | undefined, rng: Rng): void {
  applyNewsShock(m, news, rng);
  m.news = [news, ...m.news].slice(0, MAX_NEWS);
  if (effect) m.effects.push(effect);
}

/**
 * Avance le marché d'un tick (MUTE l'objet passé : utiliser cloneMarket avant).
 * Renvoie les événements survenus (actualités, dividendes, fin de journée).
 */
export function stepTick(m: MarketState, rng: Rng): MarketEvent[] {
  const events: MarketEvent[] = [];

  // 1. Actualité aléatoire ?
  if (rng.next() < NEWS_PER_DAY / TICKS_PER_DAY) {
    const { news, effect } = generateNews(rng, m);
    addNews(m, news, effect, rng);
    events.push({ type: 'news', news });
  }

  // 2. Effets de tendance actifs
  const active = m.effects.filter((e) => e.delay <= 0);

  // 3. Nouveaux prix (GBM corrélé)
  const zm = rng.normal();
  const zs: Record<string, number> = {};
  for (const sec of SECTOR_IDS) zs[sec] = rng.normal();
  for (const c of COMPANIES) {
    const s = m.stocks[c.ticker];
    const mu = c.drift;
    let vol = c.volatility * m.volMult;
    let extra = 0;
    for (const e of active) {
      if (effectMatches(e, c.ticker, c.sector)) {
        extra += e.driftPerTick;
        if (e.volMult) vol *= e.volMult;
      }
    }
    const z = correlatedShock(c.beta, zm, zs[c.sector], rng.normal());
    const prev = s.price;
    const p = Math.max(0.5, gbmStep(prev, mu, vol, TICK_DT, z) * Math.exp(extra));
    s.price = p;
    s.intraday.push(p);
    s.dayHigh = Math.max(s.dayHigh, p);
    s.dayLow = Math.min(s.dayLow, p);
    const ret = Math.abs(p / prev - 1);
    s.dayVolume += Math.round((c.avgVolume / TICKS_PER_DAY) * Math.exp(rng.normal() * 0.5) * (1 + ret * 40));
  }

  // 4. Décompte des effets
  m.effects = m.effects
    .map((e) => (e.delay > 0 ? { ...e, delay: e.delay - 1 } : { ...e, ticksLeft: e.ticksLeft - 1 }))
    .filter((e) => e.ticksLeft > 0);

  // 5. Indice
  const iv = indexValue(currentPrices(m), m.index.base);
  m.index.value = iv;
  m.index.intraday.push(iv);
  m.index.dayHigh = Math.max(m.index.dayHigh, iv);
  m.index.dayLow = Math.min(m.index.dayLow, iv);

  m.tick += 1;
  if (m.tick >= TICKS_PER_DAY) events.push(...closeDay(m));
  m.rngState = rng.state;
  return events;
}

/** Clôture la journée : bougie journalière, dividendes, nouvelle séance. */
function closeDay(m: MarketState): MarketEvent[] {
  const events: MarketEvent[] = [];
  const closedDay = m.day;
  for (const t in m.stocks) {
    const s = m.stocks[t];
    const candle: Candle = { t: closedDay, o: s.dayOpen, h: s.dayHigh, l: s.dayLow, c: s.price, v: s.dayVolume };
    s.candles = [...s.candles, candle].slice(-MAX_CANDLES);
  }
  const ix = m.index;
  ix.candles = [...ix.candles, { t: closedDay, o: ix.dayOpen, h: ix.dayHigh, l: ix.dayLow, c: ix.value, v: 0 }].slice(
    -MAX_CANDLES,
  );
  events.push({ type: 'dayEnd', day: closedDay });

  // Dividende trimestriel : détaché à la clôture, le cours baisse du montant versé
  if ((closedDay + 1) % DAYS_PER_QUARTER === 0) {
    for (const t in m.stocks) {
      const c = COMPANY_BY_TICKER[t];
      if (c.dividendYield > 0) {
        const s = m.stocks[t];
        const perShare = Math.round(s.price * (c.dividendYield / 4) * 100) / 100;
        s.price -= perShare;
        events.push({ type: 'dividend', ticker: t, perShare, day: closedDay });
      }
    }
  }

  m.day += 1;
  m.tick = 0;
  for (const t in m.stocks) {
    const s = m.stocks[t];
    s.prevClose = s.candles[s.candles.length - 1].c;
    s.dayOpen = s.price;
    s.dayHigh = s.price;
    s.dayLow = s.price;
    s.dayVolume = 0;
    s.intraday = [s.price];
  }
  ix.prevClose = ix.value;
  ix.value = indexValue(currentPrices(m), ix.base);
  ix.dayOpen = ix.value;
  ix.dayHigh = ix.value;
  ix.dayLow = ix.value;
  ix.intraday = [ix.value];
  return events;
}

/** Ticks restants avant la fin de la journée */
export function ticksToDayEnd(m: MarketState): number {
  return TICKS_PER_DAY - m.tick;
}

export function dayChange(s: StockState): number {
  return s.prevClose === 0 ? 0 : s.price / s.prevClose - 1;
}
