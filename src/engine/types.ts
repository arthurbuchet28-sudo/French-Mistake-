export type SectorId = 'tech' | 'energie' | 'sante' | 'luxe' | 'banque' | 'industrie' | 'agro';

export interface Company {
  ticker: string;
  name: string;
  sector: SectorId;
  description: string;
  /** Prix de départ (cours « actuel » au début de la partie) */
  startPrice: number;
  /** Volatilité journalière (écart-type des rendements sur une journée, ex. 0.02 = 2 %) */
  volatility: number;
  /** Tendance journalière moyenne (ex. 0.0004 = +0,04 %/jour) */
  drift: number;
  /** Sensibilité au marché global (0..1) */
  beta: number;
  /** Rendement du dividende annuel (0 = pas de dividende) */
  dividendYield: number;
  /** Volume moyen d'actions échangées par jour */
  avgVolume: number;
}

export interface Candle {
  /** Indice du jour de bourse (ou du tick pour l'intraday) */
  t: number;
  o: number;
  h: number;
  l: number;
  c: number;
  v: number;
}

export interface StockState {
  ticker: string;
  price: number;
  prevClose: number;
  /** Bougies journalières terminées */
  candles: Candle[];
  /** Prix tick par tick de la journée en cours */
  intraday: number[];
  dayOpen: number;
  dayHigh: number;
  dayLow: number;
  dayVolume: number;
}

export type NewsKind =
  | 'resultats_bons'
  | 'resultats_mauvais'
  | 'rachat'
  | 'scandale'
  | 'reglementation'
  | 'crise_sectorielle'
  | 'boom_sectoriel'
  | 'contrat'
  | 'produit'
  | 'macro'
  | 'rumeur';

export interface NewsItem {
  id: string;
  day: number;
  tick: number;
  kind: NewsKind;
  title: string;
  body: string;
  ticker?: string;
  sector?: SectorId;
  /** Choc immédiat sur le cours (ex. -0.06 = -6 %) */
  impact: number;
  /** Fausse piste : impact quasi nul */
  isFake: boolean;
}

/** Effet de tendance temporaire (suite d'une actualité, krach, bulle…) */
export interface ActiveEffect {
  id: string;
  ticker?: string;
  sector?: SectorId;
  /** S'applique à tout le marché */
  all?: boolean;
  /** Dérive logarithmique ajoutée à chaque tick */
  driftPerTick: number;
  /** Multiplicateur de volatilité */
  volMult?: number;
  /** Ticks avant activation */
  delay: number;
  /** Ticks restants une fois actif */
  ticksLeft: number;
}

export interface MarketState {
  rngState: number;
  /** Indice du jour de bourse courant */
  day: number;
  /** Tick dans la journée (0..TICKS_PER_DAY-1) */
  tick: number;
  stocks: Record<string, StockState>;
  index: {
    value: number;
    prevClose: number;
    candles: Candle[];
    intraday: number[];
    dayOpen: number;
    dayHigh: number;
    dayLow: number;
    /** Prix de référence de chaque action pour la base de l'indice */
    base: Record<string, number>;
  };
  news: NewsItem[];
  effects: ActiveEffect[];
  /** Multiplicateur global de volatilité (mode « marché volatil ») */
  volMult: number;
  nextId: number;
}

export type MarketEvent =
  | { type: 'news'; news: NewsItem }
  | { type: 'dividend'; ticker: string; perShare: number; day: number }
  | { type: 'dayEnd'; day: number };
