import { COMPANY_BY_TICKER } from './companies';
import type { Position, Transaction } from '../engine/trading';

export type Feature = 'stopTakeProfit' | 'limit' | 'indicators' | 'advancedStats' | 'short' | 'volatile';

export const FEATURE_LEVEL: Record<Feature, number> = {
  stopTakeProfit: 2,
  limit: 3,
  indicators: 3,
  advancedStats: 4,
  short: 5,
  volatile: 5,
};

export const FEATURE_LABEL: Record<Feature, string> = {
  stopTakeProfit: 'Stop-loss et take-profit',
  limit: 'Ordres limites',
  indicators: 'Moyennes mobiles et volume',
  advancedStats: 'Statistiques avancées',
  short: 'Vente à découvert',
  volatile: 'Mode « marché volatil »',
};

export interface Counters {
  stopLossPlaced: number;
  takeProfitPlaced: number;
  limitUsed: number;
  newsReactions: number;
  shortsOpened: number;
  challengesWon: number;
  dividendsReceived: number;
  weeksWithoutBigLoss: number;
  monthsBeatingIndex: number;
  monthsLowDrawdown: number;
  volatileWeeks: number;
  fakeNewsReactions: number;
}

export const EMPTY_COUNTERS: Counters = {
  stopLossPlaced: 0,
  takeProfitPlaced: 0,
  limitUsed: 0,
  newsReactions: 0,
  shortsOpened: 0,
  challengesWon: 0,
  dividendsReceived: 0,
  weeksWithoutBigLoss: 0,
  monthsBeatingIndex: 0,
  monthsLowDrawdown: 0,
  volatileWeeks: 0,
  fakeNewsReactions: 0,
};

export interface ProgressContext {
  level: number;
  transactions: Transaction[];
  positions: Record<string, Position>;
  counters: Counters;
  passedLessons: string[];
  completedMissions: string[];
}

export interface Mission {
  id: string;
  level: number;
  title: string;
  hint: string;
  target: number;
  progress: (c: ProgressContext) => number;
}

const longSectors = (c: ProgressContext) =>
  new Set(Object.values(c.positions).filter((p) => p.qty > 0).map((p) => COMPANY_BY_TICKER[p.ticker]?.sector)).size;

export const MISSIONS: Mission[] = [
  // Niveau 1
  {
    id: 'm1_buy',
    level: 1,
    title: 'Faire un premier achat',
    hint: 'Ouvre une fiche action et passe un ordre d’achat au marché.',
    target: 1,
    progress: (c) => c.transactions.filter((t) => t.side === 'buy').length,
  },
  {
    id: 'm1_gain',
    level: 1,
    title: 'Revendre avec un gain',
    hint: 'Vends une action au-dessus de ton PRU (frais compris).',
    target: 1,
    progress: (c) => c.transactions.filter((t) => (t.realizedPnl ?? 0) > 0).length,
  },
  {
    id: 'm1_three',
    level: 1,
    title: 'Posséder 3 actions différentes',
    hint: 'Avoir en même temps 3 entreprises différentes en portefeuille.',
    target: 3,
    progress: (c) => Object.values(c.positions).filter((p) => p.qty > 0).length,
  },
  // Niveau 2
  {
    id: 'm2_stop',
    level: 2,
    title: 'Placer un stop-loss',
    hint: 'Sur une fiche action, choisis l’ordre « Stop-loss » sous le cours actuel.',
    target: 1,
    progress: (c) => c.counters.stopLossPlaced,
  },
  {
    id: 'm2_sectors',
    level: 2,
    title: 'Avoir 3 secteurs différents en portefeuille',
    hint: 'Diversifie : tech, énergie, santé, banque…',
    target: 3,
    progress: longSectors,
  },
  {
    id: 'm2_week',
    level: 2,
    title: 'Finir une semaine sans perdre plus de 5 %',
    hint: 'Une semaine simulée = 5 journées de bourse. Le bilan hebdo le vérifie.',
    target: 1,
    progress: (c) => c.counters.weeksWithoutBigLoss,
  },
  // Niveau 3
  {
    id: 'm3_limit',
    level: 3,
    title: 'Utiliser un ordre limite',
    hint: 'Fixe le prix maximum d’achat (ou minimum de vente) et attends qu’il soit atteint.',
    target: 1,
    progress: (c) => c.counters.limitUsed,
  },
  {
    id: 'm3_news',
    level: 3,
    title: 'Réagir à une actualité',
    hint: 'Passe un ordre sur une action (ou son secteur) le jour d’une vraie actualité la concernant.',
    target: 1,
    progress: (c) => c.counters.newsReactions,
  },
  {
    id: 'm3_journal',
    level: 3,
    title: 'Remplir le journal sur 5 trades',
    hint: 'Indique « Pourquoi je prends cette décision ? » au moment de l’ordre (ou plus tard dans le Journal).',
    target: 5,
    progress: (c) => c.transactions.filter((t) => t.note).length,
  },
  // Niveau 4
  {
    id: 'm4_beat',
    level: 4,
    title: 'Battre l’indice sur un mois simulé',
    hint: 'Sur 21 jours de bourse, fais mieux que l’INDEX 15.',
    target: 1,
    progress: (c) => c.counters.monthsBeatingIndex,
  },
  {
    id: 'm4_dd',
    level: 4,
    title: 'Garder un drawdown sous 10 % pendant un mois',
    hint: 'Sur 21 jours, ne jamais reculer de plus de 10 % depuis ton plus haut.',
    target: 1,
    progress: (c) => c.counters.monthsLowDrawdown,
  },
  // Niveau 5
  {
    id: 'm5_short',
    level: 5,
    title: 'Réaliser une vente à découvert',
    hint: 'Vends une action que tu ne possèdes pas, pour parier sur sa baisse.',
    target: 1,
    progress: (c) => c.counters.shortsOpened,
  },
  {
    id: 'm5_volatile',
    level: 5,
    title: 'Tenir une semaine en marché volatil sans perdre plus de 5 %',
    hint: 'Active le mode « marché volatil » dans les Réglages.',
    target: 1,
    progress: (c) => c.counters.volatileWeeks,
  },
  {
    id: 'm5_challenge',
    level: 5,
    title: 'Réussir un défi',
    hint: 'Krach, Bulle ou Budget 1 000 € : à toi de choisir.',
    target: 1,
    progress: (c) => c.counters.challengesWon,
  },
];

export interface Level {
  level: number;
  title: string;
  subtitle: string;
  unlocks: Feature[];
}

export const LEVELS: Level[] = [
  { level: 1, title: 'Premiers pas', subtitle: 'Acheter et vendre au marché', unlocks: [] },
  { level: 2, title: 'Gérer le risque', subtitle: 'Stop-loss, take-profit, diversification', unlocks: ['stopTakeProfit'] },
  { level: 3, title: 'Lire le marché', subtitle: 'Ordres limites, moyennes mobiles, volume, actualités', unlocks: ['limit', 'indicators'] },
  { level: 4, title: 'Stratégie', subtitle: 'Mesurer sa performance', unlocks: ['advancedStats'] },
  { level: 5, title: 'Avancé', subtitle: 'Vente à découvert et marché volatil', unlocks: ['short', 'volatile'] },
];

export const MAX_LEVEL = LEVELS.length;

export function missionsForLevel(level: number): Mission[] {
  return MISSIONS.filter((m) => m.level === level);
}
