import { TUTORIAL_TICKER } from './companies';

export interface TutorialStep {
  id: string;
  title: string;
  body: string[];
  /** Page à afficher pendant l'étape */
  route?: string;
  /** Valeur de l'attribut data-tour à mettre en surbrillance */
  target?: string;
  /** Étape interactive : attendre une action de l'utilisateur */
  waitFor?: 'buy';
}

export const TUTORIAL_STEPS: TutorialStep[] = [
  {
    id: 'welcome',
    title: 'Bienvenue sur Bourse École 👋',
    body: [
      'Ici, tu apprends à trader avec 10 000 € d’argent fictif, sur un marché d’entreprises imaginaires.',
      'Aucun risque : rien n’est réel, aucune donnée ne sort de ton navigateur. Tu peux te tromper autant que tu veux, c’est fait pour ça.',
    ],
    route: '/',
  },
  {
    id: 'stock',
    title: 'C’est quoi, une action ?',
    body: [
      'Une action est une petite part d’une entreprise. Son prix bouge selon l’offre et la demande : quand plus de gens veulent acheter que vendre, le prix monte.',
      'Les actualités (résultats, scandales, rumeurs…) changent l’avis des investisseurs, donc le prix. Elles apparaissent dans le fil d’infos.',
    ],
    route: '/',
    target: 'news-feed',
  },
  {
    id: 'market',
    title: 'L’écran Marché',
    body: [
      'Voici les 15 entreprises fictives. Pour chacune : son prix, sa variation du jour (vert = hausse, rouge = baisse) et une mini-courbe des dernières semaines.',
      'Tu peux filtrer par secteur. Clique sur une ligne pour ouvrir la fiche de l’action.',
    ],
    route: '/marche',
    target: 'market-list',
  },
  {
    id: 'chart',
    title: 'Lire un graphique en chandeliers',
    body: [
      'Chaque bougie résume une journée : le corps va du prix d’ouverture au prix de clôture, les fines mèches montrent le plus haut et le plus bas.',
      'Bougie verte = le prix a monté ce jour-là. Rouge = il a baissé. Change la période avec 1J, 1S, 1M, 6M.',
    ],
    route: `/action/${TUTORIAL_TICKER}`,
    target: 'candle-chart',
  },
  {
    id: 'order-qty',
    title: 'Ton premier ordre (1/2)',
    body: [
      `Achetons quelques actions ${TUTORIAL_TICKER}. Dans le panneau d’ordre, choisis une quantité, par exemple 5.`,
      'Regarde : les frais et le montant total s’affichent avant que tu valides.',
    ],
    route: `/action/${TUTORIAL_TICKER}`,
    target: 'order-panel',
  },
  {
    id: 'order-buy',
    title: 'Ton premier ordre (2/2)',
    body: [
      'Clique sur « Acheter », vérifie l’écran de confirmation (quantité, prix, frais, total, part du portefeuille), puis confirme.',
      'Tu peux aussi écrire pourquoi tu achètes : c’est ton journal de trading.',
    ],
    route: `/action/${TUTORIAL_TICKER}`,
    target: 'order-panel',
    waitFor: 'buy',
  },
  {
    id: 'portfolio',
    title: 'Suivre ton portefeuille',
    body: [
      'Ici, tu retrouves tes positions. Le PRU (prix de revient unitaire) est ce que t’a coûté chaque action, frais compris.',
      'Si le cours est au-dessus du PRU : plus-value (en vert). En dessous : moins-value (en rouge). Tant que tu n’as pas vendu, elle est « latente ».',
    ],
    route: '/portefeuille',
    target: 'portfolio-summary',
  },
  {
    id: 'rules',
    title: 'Les 3 règles d’or du débutant',
    body: [
      '1. Ne mise pas tout sur une seule action : diversifie.',
      '2. Sache toujours à quel prix tu sors, en cas de gain comme de perte.',
      '3. Tiens ton journal : note pourquoi tu prends chaque décision, et relis-le.',
    ],
  },
  {
    id: 'time',
    title: 'Maîtriser le temps',
    body: [
      'Une journée de bourse dure 60 secondes. Mets en pause, accélère (x5, x20) ou avance d’une journée d’un clic.',
    ],
    target: 'time-controls',
  },
  {
    id: 'progress',
    title: 'Ta progression',
    body: [
      'Tu commences au niveau 1. Chaque niveau propose des missions et une courte leçon avec un quiz de 3 questions.',
      'Termine-les pour débloquer de nouveaux outils : stop-loss, ordres limites, indicateurs, statistiques, vente à découvert…',
      'Ce tutoriel peut être relancé à tout moment avec le bouton « Aide ». Bon entraînement !',
    ],
    target: 'header-progress',
  },
];
