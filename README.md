# Bourse École — simulateur de trading pédagogique

Application web pour apprendre à trader **sans aucun risque**. Tout est fictif : les 15 entreprises, les cours, les actualités et l'argent (10 000 € au départ). Aucune donnée réelle, aucun courtier, aucun appel réseau. La partie est sauvegardée automatiquement dans le navigateur (localStorage).

## Lancer l'application

```bash
npm install
npm run dev
```

Puis ouvrir l'adresse affichée (par défaut http://localhost:5173).

Autres commandes :

```bash
npm test          # tests unitaires (Vitest)
npm run build     # build de production dans dist/
npm run preview   # servir le build
```

## Comment jouer

1. **Tutoriel** : il démarre au premier lancement (10 étapes, dont un premier achat guidé sur NOVA). Il peut être relancé à tout moment avec le bouton **Aide**.
2. **Le temps** : 1 journée de bourse = 60 secondes à x1. Boutons pause / x1 / x5 / x20 et ⏭ « avancer d'une journée » en haut à droite.
3. **Trader** : Marché → clic sur une action → panneau d'ordre. Les frais (0,5 %, minimum 1 €) sont affichés avant validation, puis un écran de confirmation récapitule quantité, prix, frais, total et part du portefeuille, avec des garde-fous (position > 25 %, achat sans stop-loss…) et le champ « Pourquoi je prends cette décision ? ».
4. **Progresser** : onglet Progression. Chaque niveau = des missions + une leçon (3 à 5 écrans) avec un quiz de 3 questions. Les deux sont nécessaires pour passer au niveau suivant :
   - Niv. 1 Premiers pas : ordres au marché
   - Niv. 2 Gérer le risque : stop-loss, take-profit
   - Niv. 3 Lire le marché : ordres limites, moyennes mobiles 20/50, volume
   - Niv. 4 Stratégie : statistiques avancées
   - Niv. 5 Avancé : vente à découvert, mode « marché volatil »
5. **Défis** (Krach, Bulle, Budget 1 000 €) : ta partie est mise de côté puis restaurée à la fin.
6. **Bilan hebdomadaire** : chaque semaine simulée (5 jours), avec ta performance face à l'indice, ta meilleure et ta pire décision, et des conseils personnalisés.
7. **Réglages** : mode bac à sable (tout débloquer), marché volatil, relancer le tutoriel, réinitialiser la partie.

## Architecture

```
src/
├── engine/      Simulation pure TypeScript (testée) : GBM corrélé, historique, actualités,
│                dividendes, frais/PRU/P&L, ordres, statistiques, coach
├── store/       État global Zustand + persistance localStorage (écriture différée),
│                logique de partie (temps, ordres, missions, défis), boucle de jeu
├── data/        Entreprises, modèles d'actualités, leçons/quiz, niveaux/missions,
│                badges, défis, glossaire, étapes du tutoriel
├── components/  UI, graphiques (lightweight-charts, Recharts), ordres, tutoriel, progression
├── pages/       Tableau de bord, Marché, Fiche action, Portefeuille, Historique,
│                Journal, Statistiques, Progression, Glossaire, Réglages
└── utils/       Formats français (1 234,56 €, JJ/MM/AAAA)
```

### Modèle de prix

À chaque tick : `S ← S · exp((μ − σ²/2)·dt + σ·√dt·Z)` avec `dt = 1/60` de journée. Le tirage `Z` combine un facteur marché (pondéré par le bêta de l'action), un facteur secteur et un facteur propre à l'action, ce qui fait bouger ensemble les actions d'un même secteur. Les actualités appliquent un choc immédiat puis une tendance sur quelques jours. Les « fausses pistes » ont un impact quasi nul.

### Règles de calcul

- Frais : `max(1 €, 0,5 % × montant)`, arrondis au centime.
- PRU : moyenne pondérée des achats, **frais inclus**. Le « prix moyen » affiché à côté est hors frais.
- P&L réalisé : `qté × prix de vente − frais de vente − qté × PRU`.
- Vente à découvert : 150 % du montant bloqué en garantie, dividendes à la charge du vendeur.
