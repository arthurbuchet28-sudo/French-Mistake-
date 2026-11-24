import { COMPANIES, SECTORS, SECTOR_IDS } from '../data/companies';
import { NEWS_TEMPLATES, type NewsTemplate } from '../data/newsTemplates';
import { TICKS_PER_DAY } from './gbm';
import type { Rng } from './random';
import type { ActiveEffect, MarketState, NewsItem } from './types';

/** Nombre moyen d'actualités par journée de bourse */
export const NEWS_PER_DAY = 1.6;

function pickTemplate(rng: Rng): NewsTemplate {
  const total = NEWS_TEMPLATES.reduce((s, t) => s + t.weight, 0);
  let r = rng.next() * total;
  for (const t of NEWS_TEMPLATES) {
    r -= t.weight;
    if (r <= 0) return t;
  }
  return NEWS_TEMPLATES[0];
}

const between = (rng: Rng, [a, b]: [number, number]) => a + (b - a) * rng.next();

/**
 * Crée une actualité aléatoire. Le choc et la tendance qui suit sont chiffrés.
 */
export function generateNews(
  rng: Rng,
  m: MarketState,
  forced?: Partial<Pick<NewsTemplate, 'kind'>> & { ticker?: string },
): { news: NewsItem; effect?: ActiveEffect } {
  let template = pickTemplate(rng);
  if (forced?.kind) template = NEWS_TEMPLATES.find((t) => t.kind === forced.kind) ?? template;
  const company = forced?.ticker
    ? COMPANIES.find((c) => c.ticker === forced.ticker)!
    : rng.pick(COMPANIES);
  const sector = template.scope === 'sector' ? rng.pick(SECTOR_IDS) : company.sector;
  const title = rng
    .pick(template.titles)
    .replace('{name}', company.name)
    .replace('{ticker}', company.ticker)
    .replace('{sector}', SECTORS[sector].label.toLowerCase());
  const id = `n${m.nextId++}`;
  const news: NewsItem = {
    id,
    day: m.day,
    tick: m.tick,
    kind: template.kind,
    title,
    body: template.body,
    ticker: template.scope === 'stock' ? company.ticker : undefined,
    sector: template.scope === 'sector' ? sector : template.scope === 'stock' ? company.sector : undefined,
    impact: between(rng, template.impact),
    isFake: !!template.fake,
  };
  let effect: ActiveEffect | undefined;
  if (template.driftDays > 0) {
    const total = between(rng, template.drift);
    const ticks = template.driftDays * TICKS_PER_DAY;
    effect = {
      id: `e${id}`,
      ticker: news.ticker,
      sector: template.scope === 'sector' ? sector : undefined,
      all: template.scope === 'market',
      driftPerTick: Math.log(1 + total) / ticks,
      delay: 0,
      ticksLeft: ticks,
    };
  }
  return { news, effect };
}

/** Applique le choc immédiat d'une actualité sur les cours concernés. */
export function applyNewsShock(m: MarketState, news: NewsItem, rng: Rng): void {
  for (const c of COMPANIES) {
    let impact = 0;
    if (news.ticker) {
      if (c.ticker === news.ticker) impact = news.impact;
    } else if (news.sector) {
      if (c.sector === news.sector) impact = news.impact * (0.7 + 0.6 * rng.next());
    } else {
      impact = news.impact * (0.4 + c.beta);
    }
    if (impact !== 0) {
      const s = m.stocks[c.ticker];
      s.price = Math.max(0.5, s.price * (1 + impact));
      s.dayHigh = Math.max(s.dayHigh, s.price);
      s.dayLow = Math.min(s.dayLow, s.price);
      s.intraday[s.intraday.length - 1] = s.price;
    }
  }
}

/** L'effet d'une tendance s'applique-t-il à cette action ? */
export function effectMatches(e: ActiveEffect, ticker: string, sector: string): boolean {
  if (e.all) return true;
  if (e.ticker) return e.ticker === ticker;
  if (e.sector) return e.sector === sector;
  return false;
}
