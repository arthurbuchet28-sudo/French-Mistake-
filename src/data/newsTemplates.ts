import type { NewsKind } from '../engine/types';

export type NewsScope = 'stock' | 'sector' | 'market';

export interface NewsTemplate {
  kind: NewsKind;
  scope: NewsScope;
  /** Variables : {name}, {ticker}, {sector} */
  titles: string[];
  body: string;
  /** Choc immédiat, bornes min/max (ex. [0.03, 0.08]) */
  impact: [number, number];
  /** Tendance qui suit l'annonce : variation totale sur `driftDays` jours */
  drift: [number, number];
  driftDays: number;
  weight: number;
  fake?: boolean;
}

export const NEWS_TEMPLATES: NewsTemplate[] = [
  {
    kind: 'resultats_bons',
    scope: 'stock',
    titles: [
      '{name} publie des résultats trimestriels supérieurs aux attentes',
      '{name} relève ses prévisions annuelles',
      'Chiffre d’affaires record pour {name}',
    ],
    body: 'Les ventes et les marges dépassent ce qu’anticipaient les analystes. Les investisseurs revoient leurs estimations à la hausse.',
    impact: [0.03, 0.08],
    drift: [0.01, 0.04],
    driftDays: 3,
    weight: 10,
  },
  {
    kind: 'resultats_mauvais',
    scope: 'stock',
    titles: [
      '{name} déçoit avec des résultats en baisse',
      '{name} abaisse ses objectifs pour l’année',
      'Avertissement sur résultats chez {name}',
    ],
    body: 'Les bénéfices sont inférieurs aux attentes. La direction évoque une demande plus faible et des coûts en hausse.',
    impact: [-0.09, -0.03],
    drift: [-0.04, -0.01],
    driftDays: 3,
    weight: 10,
  },
  {
    kind: 'rachat',
    scope: 'stock',
    titles: ['Offre de rachat sur {name} : un concurrent propose une prime de 20 %', '{name} annonce un programme de rachat d’actions'],
    body: 'Un acheteur se manifeste ou l’entreprise rachète ses propres titres : la demande pour l’action augmente.',
    impact: [0.06, 0.15],
    drift: [0, 0.02],
    driftDays: 2,
    weight: 3,
  },
  {
    kind: 'scandale',
    scope: 'stock',
    titles: [
      'Enquête ouverte sur les comptes de {name}',
      'Rappel massif de produits chez {name}',
      'Démission surprise du PDG de {name}',
    ],
    body: 'La confiance des investisseurs est ébranlée. Des incertitudes pèsent sur l’activité dans les prochains mois.',
    impact: [-0.14, -0.05],
    drift: [-0.06, -0.01],
    driftDays: 4,
    weight: 4,
  },
  {
    kind: 'contrat',
    scope: 'stock',
    titles: ['{name} décroche un contrat important', 'Partenariat stratégique pour {name}'],
    body: 'Ce nouveau contrat devrait soutenir le chiffre d’affaires des prochaines années.',
    impact: [0.02, 0.06],
    drift: [0, 0.02],
    driftDays: 2,
    weight: 7,
  },
  {
    kind: 'produit',
    scope: 'stock',
    titles: ['{name} lance un nouveau produit très attendu', 'Feu vert des autorités pour un produit de {name}'],
    body: 'Le marché salue l’innovation, mais le succès commercial reste à confirmer.',
    impact: [0.01, 0.05],
    drift: [-0.01, 0.03],
    driftDays: 3,
    weight: 6,
  },
  {
    kind: 'reglementation',
    scope: 'sector',
    titles: [
      'Nouvelle réglementation contraignante pour le secteur {sector}',
      'Taxe exceptionnelle envisagée sur le secteur {sector}',
    ],
    body: 'Les entreprises du secteur devront supporter des coûts supplémentaires. Tout le secteur recule.',
    impact: [-0.06, -0.02],
    drift: [-0.03, 0],
    driftDays: 3,
    weight: 4,
  },
  {
    kind: 'crise_sectorielle',
    scope: 'sector',
    titles: ['Crise dans le secteur {sector} : les valeurs chutent', 'Pénurie de matières premières : le secteur {sector} sous pression'],
    body: 'Un choc frappe l’ensemble du secteur. Les actions concernées baissent ensemble : c’est la corrélation sectorielle.',
    impact: [-0.1, -0.04],
    drift: [-0.05, -0.01],
    driftDays: 4,
    weight: 3,
  },
  {
    kind: 'boom_sectoriel',
    scope: 'sector',
    titles: ['Engouement des investisseurs pour le secteur {sector}', 'Plan de soutien public au secteur {sector}'],
    body: 'Les perspectives du secteur s’améliorent. Les actions concernées montent ensemble.',
    impact: [0.02, 0.06],
    drift: [0.01, 0.04],
    driftDays: 3,
    weight: 4,
  },
  {
    kind: 'macro',
    scope: 'market',
    titles: ['La banque centrale fictive baisse ses taux', 'Croissance économique plus forte que prévu'],
    body: 'Bonne nouvelle pour l’économie : la plupart des actions profitent du mouvement.',
    impact: [0.005, 0.02],
    drift: [0, 0.015],
    driftDays: 3,
    weight: 3,
  },
  {
    kind: 'macro',
    scope: 'market',
    titles: ['Inflation plus forte que prévu : les marchés s’inquiètent', 'Tensions géopolitiques fictives : prudence sur les marchés'],
    body: 'Les investisseurs deviennent prudents. La plupart des actions reculent.',
    impact: [-0.02, -0.005],
    drift: [-0.012, 0],
    driftDays: 3,
    weight: 3,
  },
  // ——— Fausses pistes : beaucoup de bruit, presque aucun effet ———
  {
    kind: 'rumeur',
    scope: 'stock',
    titles: [
      'Rumeur : {name} serait en discussion pour un rachat',
      'Un influenceur affirme que {name} va « exploser »',
      'Selon un forum anonyme, {name} préparerait une annonce majeure',
    ],
    body: 'Information non confirmée, sans source officielle. Prudence : beaucoup de rumeurs ne se vérifient jamais.',
    impact: [-0.006, 0.006],
    drift: [0, 0],
    driftDays: 0,
    weight: 7,
    fake: true,
  },
  {
    kind: 'rumeur',
    scope: 'stock',
    titles: ['Un blog financier annonce la chute imminente de {name}', 'Le PDG de {name} aperçu dans un restaurant avec un concurrent'],
    body: 'Rien d’officiel ici : ces bruits font souvent réagir les débutants, rarement le cours sur la durée.',
    impact: [-0.006, 0.004],
    drift: [0, 0],
    driftDays: 0,
    weight: 5,
    fake: true,
  },
];

export const NEWS_KIND_LABEL: Record<NewsKind, string> = {
  resultats_bons: 'Résultats',
  resultats_mauvais: 'Résultats',
  rachat: 'Rachat',
  scandale: 'Scandale',
  reglementation: 'Réglementation',
  crise_sectorielle: 'Crise sectorielle',
  boom_sectoriel: 'Secteur',
  contrat: 'Contrat',
  produit: 'Produit',
  macro: 'Économie',
  rumeur: 'Rumeur',
};
