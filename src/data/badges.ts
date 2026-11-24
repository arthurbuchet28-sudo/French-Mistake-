import type { ProgressContext } from './levels';
import type { ChallengeResult } from './challenges';

export interface BadgeContext extends ProgressContext {
  challengeResults: ChallengeResult[];
  reportsCount: number;
}

export interface Badge {
  id: string;
  emoji: string;
  title: string;
  description: string;
  check: (c: BadgeContext) => boolean;
}

export const BADGES: Badge[] = [
  { id: 'first_trade', emoji: '🐣', title: 'Premier ordre', description: 'Passer ton tout premier ordre.', check: (c) => c.transactions.length > 0 },
  { id: 'first_gain', emoji: '💶', title: 'Premier gain', description: 'Réaliser une première plus-value.', check: (c) => c.transactions.some((t) => (t.realizedPnl ?? 0) > 0) },
  { id: 'diversified', emoji: '🧺', title: 'Panier garni', description: 'Détenir 5 actions différentes en même temps.', check: (c) => Object.values(c.positions).filter((p) => p.qty > 0).length >= 5 },
  { id: 'dividend', emoji: '🎁', title: 'Rentier en herbe', description: 'Recevoir un dividende.', check: (c) => c.counters.dividendsReceived > 0 },
  { id: 'journal10', emoji: '📓', title: 'Plume de trader', description: 'Écrire 10 notes dans ton journal.', check: (c) => c.transactions.filter((t) => t.note).length >= 10 },
  { id: 'protected', emoji: '🛡️', title: 'Bien protégé', description: 'Placer 5 stop-loss.', check: (c) => c.counters.stopLossPlaced >= 5 },
  { id: 'scholar', emoji: '🎓', title: 'Studieux', description: 'Réussir 3 quiz.', check: (c) => c.passedLessons.length >= 3 },
  { id: 'cool_head', emoji: '🧊', title: 'Sang-froid', description: 'Finir 4 semaines sans perdre plus de 5 %.', check: (c) => c.counters.weeksWithoutBigLoss >= 4 },
  { id: 'krach', emoji: '🪂', title: 'Parachute', description: 'Réussir le défi Krach.', check: (c) => c.challengeResults.some((r) => r.id === 'krach' && r.success) },
  { id: 'bulle', emoji: '📌', title: 'Éclateur de bulles', description: 'Réussir le défi Bulle.', check: (c) => c.challengeResults.some((r) => r.id === 'bulle' && r.success) },
  { id: 'budget', emoji: '🪙', title: 'Petit budget, grand esprit', description: 'Réussir le défi Budget 1 000 €.', check: (c) => c.challengeResults.some((r) => r.id === 'budget' && r.success) },
  { id: 'trader50', emoji: '⚙️', title: 'Habitué', description: 'Passer 50 ordres.', check: (c) => c.transactions.length >= 50 },
  { id: 'level3', emoji: '🔭', title: 'Analyste', description: 'Atteindre le niveau 3.', check: (c) => c.level >= 3 },
  { id: 'graduate', emoji: '🏆', title: 'Diplômé', description: 'Terminer toutes les missions du niveau 5.', check: (c) => ['m5_short', 'm5_volatile', 'm5_challenge'].every((m) => c.completedMissions.includes(m)) },
];
