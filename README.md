# Formation Trading

Formation complète et gratuite pour apprendre le trading, en français, du niveau débutant au niveau intermédiaire.

**Pour l'utiliser :** ouvrez `formation-trading/index.html` dans un navigateur (double-clic). Aucun serveur, aucune connexion internet, aucune dépendance.

## Contenu

- **14 modules** (0 à 13), soit 96 leçons. Chacune contient : objectifs, explication simple puis approfondie, exemple chiffré pas à pas, schéma (SVG), erreurs fréquentes, points clés, exercice avec correction masquée.
- **14 quiz** (164 questions), avec correction et explications, et un **examen final** de 40 questions avec un bilan par module.
- **14 fiches récapitulatives** imprimables (A4).
- **Glossaire de 341 termes** : recherche instantanée sans accents, filtre par catégorie, équivalent anglais, termes associés, et les modules où chaque terme apparaît. Les termes techniques des leçons renvoient automatiquement au glossaire, avec une infobulle au survol.
- **Outils** : calculateur de taille de position, calculateur de ratio risque/rendement et d'espérance, simulateurs de levier, de séries de pertes et de trajectoires (Monte-Carlo).
- **Journal de trading** : version interactive, export CSV et modèle papier imprimable.
- **Fonctionnalités** : mode sombre, affichage adapté au mobile, progression enregistrée dans `localStorage` (protégée par try/catch), avertissement sur les risques en pied de chaque page.

## Structure

```
formation-trading/     site livré (fichiers générés + assets écrits à la main)
  index.html, glossaire.html, outils.html, examen-final.html, journal-de-trading.html, a-propos.html
  modules/  quiz/  fiches/
  assets/css/  assets/js/
_source/               sources du contenu et générateur
  build.py             génère les pages HTML à partir des sources
  check.py             vérifie liens, ancres et sigles absents du glossaire
  svgkit.py            graphiques SVG et calcul des indicateurs (RSI, ATR, MACD…)
  modules/mXX.py       contenu de chaque module (leçons, fiche, quiz)
  glossaire.txt        glossaire
  exam.py              examen final
  pages/               contenu des pages annexes
```

## Modifier le contenu

```bash
python3 _source/build.py
```

```bash
python3 _source/check.py
```

## Avertissement

Support pédagogique général. Ce n'est ni un conseil en investissement, ni une recommandation personnalisée. Le trading comporte un risque élevé de perte en capital. Aucun courtier, aucune plateforme et aucun actif ne sont recommandés. Les règles fiscales et réglementaires évoluent : vérifiez-les sur impots.gouv.fr et sur le site de l'AMF.
