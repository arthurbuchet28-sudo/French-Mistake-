import { COMPANY_BY_TICKER, SECTORS } from '../data/companies';
import type { SectorId, NewsItem } from './types';
import { marketValue, portfolioValue, type Position, type Transaction } from './trading';
import { tradeStats } from './stats';

export interface Decision {
  label: string;
  pnl: number;
}

export interface WeeklyReport {
  id: string;
  week: number;
  startDay: number;
  endDay: number;
  startValue: number;
  endValue: number;
  ret: number;
  indexRet: number;
  trades: number;
  best?: Decision;
  worst?: Decision;
  tips: string[];
}

/** Répartition par secteur des positions longues (valeur en €) */
export function sectorExposure(positions: Record<string, Position>, prices: Record<string, number>): Record<SectorId, number> {
  const out = {} as Record<SectorId, number>;
  for (const t in positions) {
    const p = positions[t];
    if (p.qty <= 0) continue;
    const sec = COMPANY_BY_TICKER[t].sector;
    out[sec] = (out[sec] ?? 0) + marketValue(p, prices[t] ?? 0);
  }
  return out;
}

export interface CoachInput {
  weekTx: Transaction[];
  allTx: Transaction[];
  positions: Record<string, Position>;
  cash: number;
  prices: Record<string, number>;
  news: NewsItem[];
  stopLossTickers: string[];
  stopLossUnlocked: boolean;
}

const pct = (x: number) => `${Math.round(x * 100)} %`;

/** Conseils personnalisés à partir du comportement observé */
export function coachTips(i: CoachInput): string[] {
  const tips: string[] = [];
  const total = portfolioValue({ cash: i.cash, positions: i.positions }, i.prices);
  const invested = total - i.cash;

  // Concentration sectorielle
  const exp = sectorExposure(i.positions, i.prices);
  for (const [sec, v] of Object.entries(exp) as [SectorId, number][]) {
    if (total > 0 && v / total >= 0.5) {
      tips.push(`${pct(v / total)} de ton portefeuille est dans le secteur ${SECTORS[sec].label.toLowerCase()}. Une seule mauvaise nouvelle sectorielle peut te coûter cher : pense à diversifier.`);
    }
  }
  // Position trop lourde
  for (const t in i.positions) {
    const w = Math.abs(marketValue(i.positions[t], i.prices[t])) / total;
    if (w > 0.25) tips.push(`${t} pèse ${pct(w)} de ton portefeuille. Au-delà de 25 % sur une seule ligne, le risque devient élevé.`);
  }
  // Vendre ses gagnants trop tôt
  const s = tradeStats(i.allTx);
  if (s.wins >= 2 && s.losses >= 2 && s.avgGainPct < Math.abs(s.avgLossPct) * 0.6) {
    tips.push(`Tu vends souvent tes gagnants trop tôt : gain moyen +${(s.avgGainPct * 100).toFixed(1)} % contre une perte moyenne de ${(s.avgLossPct * 100).toFixed(1)} %. Essaie de laisser courir tes gains et de couper plus vite tes pertes.`);
  }
  // Sur-trading
  if (i.weekTx.length >= 15) {
    const fees = i.weekTx.reduce((a, t) => a + t.fees, 0);
    tips.push(`${i.weekTx.length} ordres cette semaine, pour ${fees.toFixed(2).replace('.', ',')} € de frais. Trader trop souvent grignote ta performance.`);
  }
  // Argent qui dort
  if (total > 0 && invested / total < 0.2 && i.allTx.length > 0) {
    tips.push('Plus de 80 % de ton capital est en liquidités. C’est prudent, mais cet argent ne travaille pas.');
  }
  // Journal
  if (i.weekTx.length >= 3 && i.weekTx.filter((t) => t.note).length < i.weekTx.length / 2) {
    tips.push('Moins de la moitié de tes ordres ont une note dans le journal. Écrire ta raison t’aide à progresser.');
  }
  // Positions sans stop-loss
  if (i.stopLossUnlocked) {
    const naked = Object.values(i.positions).filter((p) => p.qty > 0 && !i.stopLossTickers.includes(p.ticker));
    if (naked.length > 0) tips.push(`${naked.length} position(s) sans stop-loss (${naked.map((p) => p.ticker).join(', ')}). Sais-tu à quel prix tu sortirais ?`);
  }
  // Réaction aux rumeurs
  const fakeReactions = i.weekTx.filter((t) =>
    i.news.some((n) => n.isFake && n.ticker === t.ticker && (t.day === n.day || t.day === n.day + 1) && (t.day > n.day || t.tick >= n.tick)),
  );
  if (fakeReactions.length > 0) {
    tips.push(`Tu as passé ${fakeReactions.length} ordre(s) juste après une rumeur (${[...new Set(fakeReactions.map((t) => t.ticker))].join(', ')}). Les fausses pistes bougent rarement les cours : ne surréagis pas.`);
  }
  if (tips.length === 0) {
    tips.push(i.allTx.length === 0 ? 'Tu n’as encore passé aucun ordre. Lance-toi avec une petite somme sur une entreprise dont tu comprends l’activité.' : 'Belle discipline cette semaine ! Continue à diversifier et à tenir ton journal.');
  }
  return tips.slice(0, 4);
}

/** Meilleure et pire décision de la semaine */
export function bestAndWorst(weekTx: Transaction[], positions: Record<string, Position>, prices: Record<string, number>): { best?: Decision; worst?: Decision } {
  const cands: Decision[] = [];
  for (const t of weekTx) {
    if (t.realizedPnl !== undefined) {
      cands.push({ label: `${t.side === 'sell' ? 'Vente' : 'Rachat'} de ${t.qty} ${t.ticker} à ${t.price.toFixed(2).replace('.', ',')} €`, pnl: t.realizedPnl });
    } else if (positions[t.ticker]) {
      const dir = t.side === 'buy' ? 1 : -1;
      cands.push({ label: `${t.side === 'buy' ? 'Achat' : 'Vente à découvert'} de ${t.qty} ${t.ticker} à ${t.price.toFixed(2).replace('.', ',')} € (encore en portefeuille)`, pnl: dir * t.qty * ((prices[t.ticker] ?? t.price) - t.price) - t.fees });
    }
  }
  if (cands.length === 0) return {};
  cands.sort((a, b) => b.pnl - a.pnl);
  return { best: cands[0].pnl > 0 ? cands[0] : undefined, worst: cands[cands.length - 1].pnl < 0 ? cands[cands.length - 1] : undefined };
}
