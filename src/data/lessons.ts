export interface LessonScreen {
  title: string;
  emoji: string;
  paragraphs: string[];
}

export interface QuizQuestion {
  question: string;
  options: string[];
  answer: number;
  explanation: string;
}

export interface Lesson {
  id: string;
  level: number;
  title: string;
  screens: LessonScreen[];
  quiz: QuizQuestion[];
}

export const LESSONS: Lesson[] = [
  {
    id: 'l1',
    level: 1,
    title: 'Acheter, vendre, et comprendre son résultat',
    screens: [
      {
        title: 'Une action, c’est un petit morceau d’entreprise',
        emoji: '🧩',
        paragraphs: [
          'Quand tu achètes une action Novalink (NOVA), tu deviens propriétaire d’une toute petite part de l’entreprise.',
          'Si l’entreprise gagne en valeur, ta part aussi. Si elle en perd, ta part baisse.',
        ],
      },
      {
        title: 'Pourquoi le prix bouge',
        emoji: '⚖️',
        paragraphs: [
          'Le cours est fixé par la rencontre entre acheteurs et vendeurs. Plus il y a d’acheteurs que de vendeurs, plus le prix monte.',
          'Les actualités (résultats, scandales, rumeurs) changent l’avis des investisseurs, donc l’offre et la demande.',
        ],
      },
      {
        title: 'L’ordre au marché',
        emoji: '⚡',
        paragraphs: [
          'Un ordre « au marché » s’exécute tout de suite, au prix actuel.',
          'À chaque ordre, tu paies des frais de courtage : ici 0,5 % du montant, avec un minimum de 1 €. Acheter 10 € d’action te coûte donc 10 % de frais !',
        ],
      },
      {
        title: 'Plus-value et moins-value',
        emoji: '📊',
        paragraphs: [
          'Ton PRU (prix de revient unitaire) est ce que t’a vraiment coûté chaque action, frais compris.',
          'Si le cours est au-dessus de ton PRU, tu as une plus-value latente (« sur le papier »). Elle devient réalisée seulement quand tu vends.',
        ],
      },
    ],
    quiz: [
      {
        question: 'Tu achètes 10 actions à 20 €. Combien de frais paies-tu ?',
        options: ['0 €', '1 €', '2 €', '10 €'],
        answer: 1,
        explanation: '0,5 % de 200 € = 1 €, et le minimum est de 1 € : tu paies 1 €.',
      },
      {
        question: 'Qu’est-ce qu’une plus-value latente ?',
        options: ['Un gain déjà encaissé', 'Un gain sur le papier, tant que tu n’as pas vendu', 'Un dividende', 'Des frais cachés'],
        answer: 1,
        explanation: 'Latente = pas encore réalisée. Elle peut encore disparaître si le cours baisse.',
      },
      {
        question: 'Pourquoi le cours d’une action bouge-t-il ?',
        options: ['Le courtier le décide', 'Il suit l’offre et la demande', 'Il monte toujours avec le temps', 'Il change seulement une fois par an'],
        answer: 1,
        explanation: 'Le prix résulte des achats et ventes des investisseurs, influencés par les nouvelles.',
      },
    ],
  },
  {
    id: 'l2',
    level: 2,
    title: 'Gérer le risque',
    screens: [
      {
        title: 'Savoir à quel prix on sort',
        emoji: '🚪',
        paragraphs: [
          'Avant d’acheter, un trader décide où il sortira : en cas de perte (stop-loss) et en cas de gain (take-profit).',
          'Cela évite de prendre des décisions sous le coup de l’émotion.',
        ],
      },
      {
        title: 'Le stop-loss',
        emoji: '🛑',
        paragraphs: [
          'Un stop-loss vend automatiquement si le cours descend jusqu’à un prix fixé.',
          'Exemple : tu achètes à 50 € et places un stop à 46 €. Si l’action chute, tu limites ta perte à environ 8 %.',
        ],
      },
      {
        title: 'Le take-profit',
        emoji: '🎯',
        paragraphs: [
          'Un take-profit vend automatiquement quand le cours atteint ton objectif de gain.',
          'Exemple : achat à 50 €, take-profit à 58 € : tu encaisses +16 % sans avoir à surveiller l’écran.',
        ],
      },
      {
        title: 'La diversification',
        emoji: '🧺',
        paragraphs: [
          'Ne mets pas tous tes œufs dans le même panier : répartis ton argent entre plusieurs actions et plusieurs secteurs.',
          'Les actions d’un même secteur bougent souvent ensemble. Avoir 3 actions tech, c’est moins diversifié qu’une tech, une banque et une santé.',
        ],
      },
    ],
    quiz: [
      {
        question: 'Tu achètes à 100 € et places un stop-loss à 92 €. Que se passe-t-il si le cours tombe à 91 € ?',
        options: ['Rien', 'L’action est vendue automatiquement', 'Tu achètes plus d’actions', 'Le courtier te rembourse'],
        answer: 1,
        explanation: 'Le stop-loss se déclenche dès que le cours passe sous 92 € et vend ta position.',
      },
      {
        question: 'Quel portefeuille est le plus diversifié ?',
        options: ['3 actions tech', '1 action tech, 1 banque, 1 santé', '1 seule action très solide', '2 actions énergie'],
        answer: 1,
        explanation: 'Plusieurs secteurs = moins de risque qu’une même crise touche tout ton portefeuille.',
      },
      {
        question: 'À quoi sert un take-profit ?',
        options: ['À limiter une perte', 'À encaisser automatiquement un gain', 'À payer moins de frais', 'À recevoir un dividende'],
        answer: 1,
        explanation: 'Il vend quand ton objectif de prix est atteint.',
      },
    ],
  },
  {
    id: 'l3',
    level: 3,
    title: 'Lire le marché',
    screens: [
      {
        title: 'Lire une bougie',
        emoji: '🕯️',
        paragraphs: [
          'Chaque bougie résume une période : le corps va du prix d’ouverture au prix de clôture, les mèches montrent le plus haut et le plus bas.',
          'Bougie verte : le prix a monté sur la période. Rouge : il a baissé.',
        ],
      },
      {
        title: 'Les moyennes mobiles',
        emoji: '〰️',
        paragraphs: [
          'La moyenne mobile 20 jours (MM20) fait la moyenne des 20 dernières clôtures. Elle lisse le bruit et montre la tendance.',
          'Quand le cours est au-dessus de sa MM50, la tendance de fond est plutôt haussière. Ce n’est pas une garantie !',
        ],
      },
      {
        title: 'Le volume',
        emoji: '📶',
        paragraphs: [
          'Le volume, c’est le nombre d’actions échangées. Un mouvement de prix avec un gros volume est plus « sérieux » qu’avec un petit volume.',
        ],
      },
      {
        title: 'L’ordre limite',
        emoji: '🎚️',
        paragraphs: [
          'Un ordre limite fixe ton prix : « je veux acheter NOVA, mais pas plus cher que 45 € ».',
          'Il ne s’exécute que si ce prix est atteint. Tu maîtrises le prix, mais tu n’es pas sûr d’être servi.',
        ],
      },
      {
        title: 'Actualités et fausses pistes',
        emoji: '📰',
        paragraphs: [
          'Une vraie actualité (résultats, rachat, réglementation) peut faire bouger un cours durablement.',
          'Une rumeur sans source fait souvent beaucoup de bruit et peu d’effet. Ne surréagis pas !',
        ],
      },
    ],
    quiz: [
      {
        question: 'Une bougie rouge signifie…',
        options: ['Que le volume a baissé', 'Que le prix de clôture est inférieur au prix d’ouverture', 'Qu’il y a eu un scandale', 'Que l’action est vendue'],
        answer: 1,
        explanation: 'Rouge = baisse sur la période : clôture < ouverture.',
      },
      {
        question: 'Tu places un ordre d’achat limite à 45 € alors que le cours est à 48 €. Que se passe-t-il ?',
        options: ['Tu achètes tout de suite à 48 €', 'L’ordre attend que le cours descende à 45 € ou moins', 'L’ordre est refusé', 'Tu achètes à 45 € tout de suite'],
        answer: 1,
        explanation: 'L’ordre limite n’est exécuté que si le cours atteint ton prix.',
      },
      {
        question: 'Comment réagir à une rumeur publiée sur un forum anonyme ?',
        options: ['Acheter tout de suite', 'Vendre tout de suite', 'Rester prudent et attendre une confirmation', 'Emprunter pour investir'],
        answer: 2,
        explanation: 'Les rumeurs ont souvent un impact négligeable. Mieux vaut attendre une source fiable.',
      },
    ],
  },
  {
    id: 'l4',
    level: 4,
    title: 'Construire une stratégie',
    screens: [
      {
        title: 'Se comparer à l’indice',
        emoji: '🏁',
        paragraphs: [
          'L’INDEX 15 représente la moyenne du marché. Si tu fais +3 % quand l’indice fait +6 %, acheter tout le marché aurait été mieux.',
          'Battre l’indice dans la durée est difficile, même pour les professionnels.',
        ],
      },
      {
        title: 'Le drawdown',
        emoji: '🕳️',
        paragraphs: [
          'Le drawdown mesure ta plus forte chute depuis un sommet. Passer de 12 000 € à 9 000 €, c’est un drawdown de 25 %.',
          'Attention : après −50 %, il faut +100 % pour revenir au point de départ.',
        ],
      },
      {
        title: 'Taux de réussite et ratio gain/perte',
        emoji: '⚖️',
        paragraphs: [
          'On peut gagner de l’argent en ayant raison seulement 40 % du temps… si les gains moyens sont plus gros que les pertes moyennes.',
          'Couper vite ses pertes et laisser courir ses gains : c’est la règle la plus citée.',
        ],
      },
    ],
    quiz: [
      {
        question: 'Ton portefeuille fait +4 %, l’indice +7 %. As-tu battu l’indice ?',
        options: ['Oui', 'Non', 'Impossible à dire'],
        answer: 1,
        explanation: '+4 % < +7 % : tu as fait moins bien que le marché.',
      },
      {
        question: 'Tu as perdu 50 %. Quel gain faut-il pour revenir au départ ?',
        options: ['+50 %', '+75 %', '+100 %', '+25 %'],
        answer: 2,
        explanation: '1 000 € → 500 € : il faut doubler (+100 %) pour revenir à 1 000 €.',
      },
      {
        question: 'Taux de réussite de 40 %, gain moyen 300 €, perte moyenne 100 €. Sur 10 trades…',
        options: ['Tu perds de l’argent', 'Tu gagnes environ 600 €', 'Tu es à l’équilibre'],
        answer: 1,
        explanation: '4 × 300 − 6 × 100 = 1 200 − 600 = +600 €.',
      },
    ],
  },
  {
    id: 'l5',
    level: 5,
    title: 'Techniques avancées',
    screens: [
      {
        title: 'La vente à découvert',
        emoji: '🔻',
        paragraphs: [
          'Vendre à découvert, c’est vendre une action que tu ne possèdes pas (empruntée) pour la racheter plus tard, idéalement moins cher.',
          'Tu gagnes si le cours baisse. Mais si le cours monte, la perte n’a théoriquement pas de limite !',
        ],
      },
      {
        title: 'La garantie',
        emoji: '🔐',
        paragraphs: [
          'Ici, chaque vente à découvert bloque 150 % du montant vendu en garantie. Le produit de la vente ne peut pas servir à acheter autre chose.',
          'Les dividendes versés pendant un short sont à ta charge.',
        ],
      },
      {
        title: 'Marché volatil',
        emoji: '🌪️',
        paragraphs: [
          'En période agitée, les cours bougent beaucoup plus fort. Les stop-loss se déclenchent plus souvent, les gains et les pertes vont plus vite.',
          'Réduire la taille de ses positions est une bonne façon de garder le même niveau de risque.',
        ],
      },
    ],
    quiz: [
      {
        question: 'Tu vends à découvert à 50 € et tu rachètes à 40 €. Avant frais, tu…',
        options: ['Perds 10 € par action', 'Gagnes 10 € par action', 'Es à l’équilibre'],
        answer: 1,
        explanation: 'Vendre 50, racheter 40 : +10 € par action.',
      },
      {
        question: 'Quel est le principal danger de la vente à découvert ?',
        options: ['Les dividendes reçus', 'Une perte potentiellement illimitée si le cours monte', 'Les frais nuls', 'Rien'],
        answer: 1,
        explanation: 'Un cours peut monter sans limite : la perte aussi.',
      },
      {
        question: 'En marché volatil, que faire pour garder le même risque ?',
        options: ['Doubler ses positions', 'Réduire la taille de ses positions', 'Supprimer tous les stop-loss'],
        answer: 1,
        explanation: 'Des positions plus petites compensent des mouvements plus forts.',
      },
    ],
  },
];

export const LESSON_BY_LEVEL: Record<number, Lesson> = Object.fromEntries(LESSONS.map((l) => [l.level, l]));
