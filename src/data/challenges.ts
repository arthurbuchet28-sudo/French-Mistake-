export type ChallengeId = 'krach' | 'bulle' | 'budget';

export interface Challenge {
  id: ChallengeId;
  title: string;
  emoji: string;
  pitch: string;
  rules: string[];
  durationDays: number;
  startCash: number;
  goal: string;
}

export const CHALLENGES: Challenge[] = [
  {
    id: 'krach',
    title: 'Krach',
    emoji: '📉',
    pitch: 'Le marché va chuter d’environ 30 %. Limite la casse !',
    rules: [
      'Tu démarres avec un portefeuille déjà investi à 80 % dans 4 actions.',
      'Dès le 2e jour, un krach fait chuter tout le marché pendant une semaine.',
      'Durée : 10 jours de bourse.',
    ],
    durationDays: 10,
    startCash: 10_000,
    goal: 'Réussi si ta perte reste inférieure à 12 %.',
  },
  {
    id: 'bulle',
    title: 'Bulle',
    emoji: '🫧',
    pitch: 'Une action s’envole… Sauras-tu sortir à temps ?',
    rules: [
      'Une action de la tech va monter de façon spectaculaire, puis s’effondrer brutalement.',
      'Personne ne sait exactement quand la bulle éclate.',
      'Durée : 15 jours de bourse.',
    ],
    durationDays: 15,
    startCash: 10_000,
    goal: 'Réussi si ton portefeuille termine à +10 % ou plus.',
  },
  {
    id: 'budget',
    title: 'Budget 1 000 €',
    emoji: '🪙',
    pitch: 'Petit capital, grosses contraintes : les frais minimum pèsent lourd.',
    rules: [
      'Tu démarres avec 1 000 € seulement.',
      'Le minimum de frais de 1 € par ordre pèse plus lourd sur les petits montants.',
      'Durée : 20 jours de bourse.',
    ],
    durationDays: 20,
    startCash: 1_000,
    goal: 'Réussi si tu fais mieux que l’indice sur la période.',
  },
];

export const CHALLENGE_BY_ID = Object.fromEntries(CHALLENGES.map((c) => [c.id, c])) as Record<ChallengeId, Challenge>;

export interface ChallengeResult {
  id: ChallengeId;
  day: number;
  success: boolean;
  portfolioReturn: number;
  indexReturn: number;
}

export function isChallengeSuccess(id: ChallengeId, portfolioReturn: number, indexReturn: number): boolean {
  switch (id) {
    case 'krach':
      return portfolioReturn > -0.12;
    case 'bulle':
      return portfolioReturn >= 0.1;
    case 'budget':
      return portfolioReturn > indexReturn;
  }
}
