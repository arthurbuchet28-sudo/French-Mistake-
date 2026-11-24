import type { ChallengeId, ChallengeResult } from '../data/challenges';
import type { Counters } from '../data/levels';
import type { WeeklyReport } from '../engine/coach';
import type { Snapshot } from '../engine/stats';
import type { OrderType, PendingOrder, Position, Side, Transaction } from '../engine/trading';
import type { MarketState } from '../engine/types';

export type Speed = 0 | 1 | 5 | 20;

export interface DividendRecord {
  day: number;
  ticker: string;
  qty: number;
  perShare: number;
  amount: number;
}

/** Tout ce qui constitue une partie (sauvegardé/restauré lors d'un défi) */
export interface GameData {
  market: MarketState;
  cash: number;
  positions: Record<string, Position>;
  orders: PendingOrder[];
  transactions: Transaction[];
  dividends: DividendRecord[];
  snapshots: Snapshot[];
  startDay: number;
  startValue: number;
  startIndex: number;
  level: number;
  levelReachedDay: Record<number, number>;
  completedMissions: string[];
  passedLessons: string[];
  badges: string[];
  counters: Counters;
  reports: WeeklyReport[];
  challengeResults: ChallengeResult[];
  monthWindowStart: number | null;
  nextTxId: number;
}

export interface ActiveChallenge {
  id: ChallengeId;
  startDay: number;
  endDay: number;
  startValue: number;
  startIndex: number;
  bubbleTicker?: string;
  saved: GameData;
}

export interface Settings {
  sandbox: boolean;
  volatileMode: boolean;
  volatileSince: number | null;
  speed: Speed;
}

export interface TutorialState {
  done: boolean;
  active: boolean;
  step: number;
}

export interface PersistedState extends GameData {
  version: number;
  settings: Settings;
  tutorial: TutorialState;
  challenge: ActiveChallenge | null;
  unreadReportId: string | null;
  pendingLevelUp: number | null;
  lastChallengeResult: ChallengeResult | null;
}

export interface Toast {
  id: number;
  kind: 'success' | 'error' | 'info' | 'mission' | 'badge' | 'news';
  title: string;
  body?: string;
}

export interface OrderRequest {
  ticker: string;
  side: Side;
  qty: number;
  type: OrderType;
  triggerPrice?: number;
  note?: string;
  /** Stop-loss à rattacher après un achat au marché */
  stopLoss?: number;
  /** Take-profit à rattacher après un achat au marché */
  takeProfit?: number;
}

export interface OrderResult {
  ok: boolean;
  error?: string;
}
