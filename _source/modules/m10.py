import random
from svgkit import plot, table, svg, t, line, arrow

NUM = 10
TITRE = "Construire une stratégie"
RESUME = "Règles d'entrée, de sortie et de gestion ; backtest et forward test ; biais (surapprentissage, survivant) ; statistiques de performance."
DUREE = "2 h 45"
INTRO = r"""<p>Une <strong>stratégie</strong> n'est pas une intuition ni une collection d'indicateurs : c'est un ensemble de <strong>règles écrites, précises et testables</strong> qui disent quand entrer, où sortir, combien risquer. Ce module montre comment en construire une, comment la tester honnêtement, et comment éviter de se mentir avec des statistiques.</p>"""

R = [1.8, -1, -1, 2.4, -1, 0.6, -1, 2.1, -1, -0.5, 3.0, -1, -1, 1.5, -1, 2.2, -1, -1, 0.9, -1]
_eq = [0]
for r in R:
    _eq.append(round(_eq[-1] + r, 2))
SCHEMA_ECHANTILLON = plot([{"x": list(range(1, 21)), "y": R, "kind": "bar", "cls": "g-barre-h", "cls_neg": "g-barre-b", "bw": 18, "label": "Résultat de chaque trade (R)"},
                           {"x": list(range(0, 21)), "y": _eq, "cls": "g-l1", "label": "Résultat cumulé (R)"}],
                          label="Échantillon de 20 trades : résultat de chaque trade et courbe cumulée", xlabel="Numéro du trade",
                          yr=(-1.5, 5.6), xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f} R".replace("+0", "0"))


def _is_oos():
    rnd = random.Random(8)
    ins, oos = [0], []
    for i in range(120):
        ins.append(ins[-1] + rnd.gauss(0.35, 1.0))
    oos = [ins[-1]]
    for i in range(60):
        oos.append(oos[-1] + rnd.gauss(0.0, 1.0))
    return plot([{"x": list(range(121)), "y": ins, "cls": "g-l1", "label": "Période d'optimisation (dans l'échantillon)"},
                 {"x": list(range(120, 181)), "y": oos, "cls": "g-lb", "label": "Période de test (hors échantillon)"}],
                label="Une stratégie suroptimisée brille sur la période d'optimisation puis stagne sur des données nouvelles",
                xlabel="Trades", vlines=[{"x": 120, "label": "Données jamais vues", "cls": "g-l3", "ly": 60}],
                xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f} R".replace("+0", "0"))


SCHEMA_IS_OOS = _is_oos()


def _cycle():
    W = 680
    etapes = [("1. Idée", "observation, hypothèse"), ("2. Règles écrites", "entrée, sortie, taille"), ("3. Backtest", "données passées, frais inclus"),
              ("4. Test hors échantillon", "données jamais utilisées"), ("5. Forward test", "démo ou temps réel"), ("6. Réel, petite taille", "journal, suivi des écarts")]
    p = []
    pos = []
    for k, (a, b) in enumerate(etapes):
        x = 20 + (k % 3) * 225
        y = 16 if k < 3 else 112
        pos.append((x, y))
        p.append(f'<rect x="{x}" y="{y}" width="190" height="56" rx="8" class="{"g-rect-a" if k < 5 else "g-rect-h"}"/>')
        p.append(t(x + 95, y + 24, a, "g-txt g-fort", "middle"))
        p.append(t(x + 95, y + 42, b, "g-txt g-petit", "middle"))
    for k in range(5):
        (x1, y1), (x2, y2) = pos[k], pos[k + 1]
        if y1 == y2:
            p.append(arrow(x1 + 190, y1 + 28, x2, y2 + 28))
        else:
            p.append(arrow(x1 + 95, y1 + 56, x2 + 95, y2))
    p.append(t(340, 196, "Échec à n'importe quelle étape → retour à l'idée, sans « ajuster » jusqu'à ce que ça marche.", "g-txt g-petit", "middle"))
    return svg(W, 206, "".join(p), "Le cycle de développement d'une stratégie")


SCHEMA_CYCLE = _cycle()

LECONS = [
("10-1", "Anatomie d'une stratégie", r"""
<x-obj><ul><li>Connaître les composantes d'une stratégie complète.</li><li>Distinguer une stratégie d'un simple signal.</li></ul></x-obj>
<x-simple>
<p>Une stratégie complète répond à toutes ces questions, <strong>par écrit</strong> :</p>
<ol><li><strong>Marché et unité de temps</strong> : quoi, et sur quel graphique ?</li>
<li><strong>Contexte</strong> : dans quelles conditions la stratégie est-elle active (tendance, volatilité, horaires) ?</li>
<li><strong>Entrée</strong> : quel événement précis déclenche l'ordre, et quel type d'ordre ?</li>
<li><strong>Stop</strong> : où, et comment est-il calculé ?</li>
<li><strong>Sortie en gain</strong> : objectif, trailing, sortie partielle, sortie au temps ?</li>
<li><strong>Taille</strong> : quel risque par trade ?</li>
<li><strong>Gestion</strong> : déplace-t-on le stop ? Que fait-on avant une annonce ou le week-end ?</li>
<li><strong>Filtres et limites</strong> : nombre maximal de positions, limites de perte (module 9).</li></ol>
</x-simple>
<x-fig c="Le cycle de développement : chaque étape peut invalider l'idée. C'est normal, et c'est même le but.">""" + SCHEMA_CYCLE + r"""</x-fig>
<x-approfondi>
<p>« Acheter quand le RSI passe sous 30 » est un <strong>signal</strong>, pas une stratégie : il manque le contexte, le stop, la sortie, la taille. Deux traders appliquant le même signal avec des sorties différentes auront des résultats complètement différents. Souvent, la sortie et la gestion du risque comptent davantage que l'entrée.</p>
</x-approfondi>
<x-exemple>
<p>Calcul de cohérence d'une stratégie avant même de la tester : stop moyen de 1,5 ATR, objectif à 2R, coûts estimés à 0,1R par trade.</p>
<div class="calcul">Gain net d'un gagnant = 2 − 0,1 = 1,9 R ; perte nette = 1 + 0,1 = 1,1 R
Taux de réussite minimal = 1,1 ÷ (1,9 + 1,1) ≈ 36,7 %
Question à se poser : est-il plausible d'atteindre un objectif de 3 ATR (2 × 1,5 ATR) avant un stop de 1,5 ATR plus d'une fois sur trois ? Le backtest répondra.</div>
</x-exemple>
<x-erreurs><ul><li>Confondre signal et stratégie.</li><li>Garder des règles floues (« si le marché a l'air fort ») impossibles à tester.</li><li>Ne pas prévoir les cas particuliers (gap au-delà du stop, annonce, jour férié).</li></ul></x-erreurs>
<x-cles><ul><li>Stratégie = marché, contexte, entrée, stop, sortie, taille, gestion, limites.</li><li>Un signal seul ne fait pas une stratégie.</li><li>Calculez le taux de réussite minimal avant de tester.</li></ul></x-cles>
<x-exo><p>Complétez ce signal pour en faire une stratégie : « Acheter quand le prix clôture au-dessus du plus haut des 20 derniers jours ».</p>
<x-corr><p>Exemple : <em>Marché</em> : un indice actions, graphique journalier. <em>Contexte</em> : prix au-dessus de la moyenne mobile 200 jours. <em>Entrée</em> : achat à l'ouverture suivante si la clôture dépasse le plus haut des 20 jours. <em>Stop</em> : 2 ATR sous l'entrée. <em>Sortie</em> : clôture sous le plus bas des 10 derniers jours (trailing). <em>Taille</em> : 1 % de risque. <em>Gestion</em> : pas de nouvelle position si 3 positions sont déjà ouvertes ; stop non déplacé avant 1R de gain. Toutes ces règles sont testables.</p></x-corr></x-exo>
"""),

("10-2", "Écrire des règles testables", r"""
<x-obj><ul><li>Transformer une idée en règles sans ambiguïté.</li><li>Vérifier qu'une règle est testable.</li></ul></x-obj>
<x-simple>
<p>Une règle est <strong>testable</strong> si deux personnes différentes, ou un ordinateur, l'appliquant aux mêmes données, prennent exactement les mêmes décisions. Test simple : pourriez-vous la programmer ?</p>
</x-simple>
<x-approfondi>
""" + table(["Règle floue", "Règle testable"],
            [["Acheter en tendance haussière", "Clôture au-dessus de la SMA 50, et SMA 50 plus haute qu'il y a 10 jours"],
             ["Acheter sur un repli", "Le prix touche l'EMA 20 (plus bas ≤ EMA 20) après au moins 3 clôtures au-dessus"],
             ["Stop sous le support", "Stop = plus bas des 5 dernières bougies − 0,5 ATR 14"],
             ["Sortir quand ça ralentit", "Sortie à la clôture si le RSI 14 repasse sous 50, ou objectif à 2R"],
             ["Éviter les annonces", "Pas d'entrée entre 30 min avant et 30 min après une publication classée 3 étoiles"]]) + r"""
<p>Précisez aussi : à quel moment la condition est-elle vérifiée (clôture de la bougie ou en cours de bougie) ? À quel prix l'ordre est-il exécuté (ouverture suivante, ordre stop, ordre limité) ? Ces détails changent fortement les résultats d'un test.</p>
</x-approfondi>
<x-exemple>
<p>Une même règle « acheter quand le prix casse le plus haut de la veille » testée de deux façons :</p>
<div class="calcul">Version A : achat à la clôture du jour de cassure → prix moyen d'entrée = clôture
Version B : ordre stop d'achat 0,05 € au-dessus du plus haut de la veille → entrée pendant la séance
Sur une cassure : plus haut de la veille 50,00 ; la séance monte à 51,20 et clôture à 50,40
A : entrée 50,40 ; B : entrée 50,05 (+ slippage éventuel)
Écart = 0,35 € ; avec un stop à 1,00 €, c'est 0,35R de différence sur ce seul trade</div>
</x-exemple>
<x-erreurs><ul><li>Laisser une part d'appréciation dans les règles (« si le contexte est bon »).</li><li>Ne pas préciser le moment de vérification et le prix d'exécution.</li></ul></x-erreurs>
<x-cles><ul><li>Une règle testable donne toujours la même décision avec les mêmes données.</li><li>Préciser : condition, moment de vérification, type d'ordre, prix d'exécution.</li></ul></x-cles>
<x-exo><p>Rendez testable : « Je vends quand le marché est suracheté sur une résistance. »</p>
<x-corr><p>Exemple : « Vente à découvert à l'ouverture suivante si : (1) le RSI 14 clôture au-dessus de 70 ; (2) le plus haut du jour est à moins de 0,5 ATR d'un sommet des 60 derniers jours ; (3) le prix est sous sa SMA 200. Stop : plus haut du jour + 0,5 ATR. Sortie : objectif 1,5R ou clôture après 10 jours. » Ce n'est pas forcément une bonne stratégie, mais elle est testable.</p></x-corr></x-exo>
"""),

("10-3", "Le backtesting", r"""
<x-obj><ul><li>Réaliser un backtest manuel ou automatisé.</li><li>Intégrer frais et slippage, et éviter les erreurs classiques.</li></ul></x-obj>
<x-simple>
<p>Le <strong>backtest</strong> consiste à appliquer ses règles sur des données passées, comme si l'on avait tradé à l'époque, et à enregistrer chaque trade. On peut le faire à la main (faire défiler un graphique bougie par bougie, sans regarder la suite) ou par programme (tableur, langage de script des plateformes, Python…).</p>
</x-simple>
<x-approfondi>
<p>Points d'attention :</p>
<ul><li><strong>Données de qualité</strong> : ajustées des divisions d'actions et dividendes, sans trous, couvrant plusieurs régimes de marché (hausse, baisse, range, crise).</li>
<li><strong>Frais et slippage réalistes</strong>, voire pessimistes.</li>
<li><strong>Exécution réaliste</strong> : on ne peut pas acheter au plus bas d'une bougie qu'on vient de voir se former.</li>
<li><strong>Nombre suffisant de trades</strong> (leçon 10.7).</li>
<li><strong>Biais</strong> (leçon 10.5) : look-ahead, survivant, surapprentissage.</li></ul>
<p>En backtest manuel, notez chaque trade dans un tableau (date, entrée, stop, sortie, résultat en R). C'est long, mais extrêmement formateur : vous apprenez à reconnaître vos setups.</p>
</x-approfondi>
<x-exemple>
<p>Un backtest de 150 trades donne une espérance brute de +0,25R. Coûts estimés : spread et commission = 0,06R, slippage = 0,02R par trade.</p>
<div class="calcul">Espérance nette = 0,25 − 0,06 − 0,02 = +0,17 R
Sur 150 trades : 150 × 0,17 = 25,5 R au lieu de 37,5 R brut, soit 32 % de moins
Si les coûts réels sont deux fois plus élevés (0,16R) : 0,25 − 0,16 = +0,09 R</div>
<p>Une stratégie dont l'avantage brut est faible devient vite neutre ou perdante en conditions réelles.</p>
</x-exemple>
<x-erreurs><ul><li>Tester sans frais.</li><li>Faire un backtest manuel en voyant la suite du graphique.</li><li>Tester sur une seule période favorable (par exemple uniquement un marché haussier).</li></ul></x-erreurs>
<x-cles><ul><li>Backtest = application honnête des règles sur le passé.</li><li>Données propres, frais et slippage inclus, plusieurs régimes de marché.</li><li>Un avantage brut faible disparaît souvent après coûts.</li></ul></x-cles>
<x-exo><p>Backtest de 80 trades : 30 gagnants à +2,2R, 50 perdants à −1R. Coûts de 0,1R par trade. Calculez l'espérance brute et nette.</p>
<x-corr><div class="calcul">Brute = (30 × 2,2 − 50 × 1) ÷ 80 = (66 − 50) ÷ 80 = +0,20 R
Nette = 0,20 − 0,10 = +0,10 R</div></x-corr></x-exo>
"""),

("10-4", "Le forward testing", r"""
<x-obj><ul><li>Comprendre l'intérêt du test en temps réel.</li><li>Comparer résultats de backtest et de forward test.</li></ul></x-obj>
<x-simple>
<p>Le <strong>forward test</strong> (ou paper trading) consiste à appliquer la stratégie <strong>en temps réel</strong>, sur un compte de démonstration ou avec de très petites positions, sans connaître la suite. Il révèle ce que le backtest ne montre pas : exécution réelle, disponibilité, discipline, émotions.</p>
</x-simple>
<x-approfondi>
<p>Comparez les statistiques du forward test à celles du backtest : taux de réussite, gain et perte moyens, espérance, drawdown. Un écart modéré est normal ; un écart important signale un problème : surapprentissage, coûts sous-estimés, règles mal appliquées. Notez aussi les trades « manqués » (signal présent, mais vous n'étiez pas là) et les trades « hors plan » : ils font partie de la performance réelle.</p>
<p>Limite du compte démo : l'exécution y est souvent meilleure que la réalité, et l'absence d'argent réel supprime une grande partie de la pression émotionnelle (module 12).</p>
</x-approfondi>
<x-exemple>
""" + table(["Statistique", "Backtest (150 trades)", "Forward test (40 trades)"],
            [["Taux de réussite", "42 %", "38 %"], ["Gain moyen", "+2,0 R", "+1,8 R"], ["Perte moyenne", "−1,0 R", "−1,1 R"], ["Espérance", "+0,26 R", "?"]]) + r"""
<div class="calcul">Espérance du forward test = 0,38 × 1,8 − 0,62 × 1,1 = 0,684 − 0,682 ≈ 0 R
Les gains moyens plus faibles et les pertes plus fortes (slippage, sorties anticipées ?) effacent l'avantage.
Avec seulement 40 trades, l'écart peut être dû au hasard, mais il faut enquêter : comparer trade par trade.</div>
</x-exemple>
<x-erreurs><ul><li>Sauter le forward test parce que le backtest est « excellent ».</li><li>Ne pas noter les trades manqués ou hors plan.</li><li>Conclure trop vite sur 10 ou 20 trades.</li></ul></x-erreurs>
<x-cles><ul><li>Forward test = application en temps réel, en démo ou en très petite taille.</li><li>Comparer ses statistiques au backtest et enquêter sur les écarts.</li><li>La démo surestime souvent l'exécution et sous-estime les émotions.</li></ul></x-cles>
<x-exo><p>Forward test : 50 trades, 21 gagnants à +1,9R en moyenne, 29 perdants à −1,05R. Calculez l'espérance.</p>
<x-corr><div class="calcul">p = 21 ÷ 50 = 42 %
E = 0,42 × 1,9 − 0,58 × 1,05 = 0,798 − 0,609 ≈ +0,19 R</div></x-corr></x-exo>
"""),

("10-5", "Les biais du backtest", r"""
<x-obj><ul><li>Reconnaître le surapprentissage, le biais du survivant, le biais d'anticipation et le biais de sélection.</li><li>Appliquer des parades simples.</li></ul></x-obj>
<x-simple>
<ul><li><strong>Surapprentissage</strong> (overfitting) : ajuster les paramètres jusqu'à ce que la stratégie colle parfaitement au passé. Elle a alors appris le bruit, pas un phénomène reproductible.</li>
<li><strong>Biais du survivant</strong> : tester uniquement sur les actifs qui existent aujourd'hui (les « survivants »), en oubliant ceux qui ont disparu (faillites, sorties d'indice).</li>
<li><strong>Biais d'anticipation</strong> (look-ahead) : utiliser une information qui n'était pas disponible au moment de la décision.</li>
<li><strong>Biais de sélection</strong> : ne retenir que la période, le marché ou la version qui donne de bons résultats.</li></ul>
</x-simple>
<x-fig c="Simulation : sur la période d'optimisation, la stratégie semble excellente ; sur des données nouvelles, son avantage disparaît. C'est la signature typique du surapprentissage.">""" + SCHEMA_IS_OOS + r"""</x-fig>
<x-approfondi>
<p><strong>Parades</strong> :</p>
<ul><li>Peu de règles et peu de paramètres ; des paramètres « ronds » et logiques plutôt qu'optimisés au dixième.</li>
<li>Réserver des données <strong>hors échantillon</strong>, jamais utilisées pendant la conception, pour un test final unique.</li>
<li>Vérifier la <strong>robustesse</strong> : la stratégie doit rester correcte si l'on change un peu les paramètres (SMA 45 ou 55 au lieu de 50). Si seul « 50 » fonctionne, c'est suspect.</li>
<li>Tester sur d'autres marchés et d'autres périodes.</li>
<li>Utiliser des listes historiques de composants d'indice (qui incluent les sociétés disparues).</li>
<li>Compter <strong>combien de variantes</strong> ont été essayées (module 4 : avec assez d'essais, on trouve toujours une « pépite » par hasard).</li></ul>
</x-approfondi>
<x-exemple>
<p>Vous testez une stratégie avec 3 paramètres, chacun avec 10 valeurs possibles.</p>
<div class="calcul">Nombre de combinaisons = 10 × 10 × 10 = 1 000
Au seuil de 5 %, combinaisons « significatives » attendues par hasard ≈ 1 000 × 5 % = 50
La meilleure des 1 000 sera presque toujours excellente sur le passé, même sans aucun avantage réel.</div>
<p>Biais du survivant (illustration chiffrée hypothétique) : un backtest sur les 40 valeurs actuelles d'un indice donne +11 % par an ; refait avec la composition historique réelle, incluant les sociétés sorties de l'indice après de fortes baisses, il ne donne plus que +7 %. Les 4 points d'écart viennent uniquement du choix des données.</p>
</x-exemple>
<x-erreurs><ul><li>Optimiser chaque paramètre au maximum.</li><li>Regarder les données « hors échantillon » plusieurs fois et réajuster à chaque fois (elles deviennent alors « dans l'échantillon »).</li><li>Utiliser la clôture du jour pour décider d'une entrée à l'ouverture du même jour.</li></ul></x-erreurs>
<x-cles><ul><li>Surapprentissage, survivant, anticipation, sélection : quatre façons de se tromper avec un backtest.</li><li>Peu de paramètres, test hors échantillon unique, robustesse, autres marchés.</li><li>Compter les essais effectués.</li></ul></x-cles>
<x-exo><p>Une stratégie donne un profit factor de 2,4 avec une SMA de 37 jours, mais de 1,0 avec 35 et de 0,9 avec 40. Qu'en concluez-vous ?</p>
<x-corr><p>La performance dépend d'une valeur très précise et s'effondre avec des valeurs voisines : c'est un signe fort de <strong>surapprentissage</strong>. Le « 37 » a capturé un hasard du passé. Une stratégie robuste donne des résultats proches sur une plage de paramètres voisins.</p></x-corr></x-exo>
"""),

("10-6", "Les statistiques de performance", r"""
<x-obj><ul><li>Calculer taux de réussite, gain et perte moyens, espérance, profit factor et drawdown maximal.</li><li>Découvrir le ratio de Sharpe.</li></ul></x-obj>
<x-simple>
<p>Voici un échantillon de 20 trades (en R) : +1,8 ; −1 ; −1 ; +2,4 ; −1 ; +0,6 ; −1 ; +2,1 ; −1 ; −0,5 ; +3,0 ; −1 ; −1 ; +1,5 ; −1 ; +2,2 ; −1 ; −1 ; +0,9 ; −1.</p>
</x-simple>
<x-fig c="Les barres montrent chaque trade, la courbe le résultat cumulé : malgré 60 % de trades perdants, le total est positif.">""" + SCHEMA_ECHANTILLON + r"""</x-fig>
<x-exemple>
<div class="calcul">Gagnants : 8 (1,8 + 2,4 + 0,6 + 2,1 + 3,0 + 1,5 + 2,2 + 0,9 = 14,5 R)
Perdants : 12 (11 × −1 et 1 × −0,5 = −11,5 R)
Taux de réussite = 8 ÷ 20 = 40 %
Gain moyen = 14,5 ÷ 8 ≈ 1,81 R ; perte moyenne = 11,5 ÷ 12 ≈ 0,96 R
Espérance = 3,0 ÷ 20 = +0,15 R par trade (ou 0,40 × 1,81 − 0,60 × 0,96 ≈ 0,15)
Profit factor = gains bruts ÷ pertes brutes = 14,5 ÷ 11,5 ≈ 1,26
Courbe cumulée : 0 ; 1,8 ; 0,8 ; −0,2 ; 2,2 ; … plus haut 5,1 au trade 16, puis 3,0 au trade 18
Drawdown maximal = 5,1 − 3,0 = 2,1 R
Plus longue série de pertes : 2</div>
</x-exemple>
<x-approfondi>
<p><strong>Profit factor</strong> : au-dessus de 1, la stratégie gagne ; les valeurs supérieures à 2 sont rares sur de longues périodes et doivent rendre méfiant (surapprentissage ?).</p>
<p><strong>Ratio de Sharpe</strong> (introduction) : rendement moyen au-dessus du taux sans risque, divisé par la volatilité des rendements. Il mesure le rendement par unité de risque.</p>
<div class="formule">Sharpe = (Rendement moyen − Taux sans risque) ÷ Écart-type des rendements</div>
<p>Il se calcule sur des rendements périodiques (mensuels, par exemple) et s'annualise en multipliant par √12 pour des données mensuelles. Limites : il pénalise autant la volatilité à la hausse qu'à la baisse, suppose des rendements « normaux » et peut être flatté par des stratégies qui vendent des risques extrêmes rares. Des variantes existent (Sortino, ratio de Calmar = rendement annuel ÷ drawdown maximal).</p>
<div class="calcul">12 rendements mensuels (%) : 1,2 ; −0,8 ; 2,1 ; 0,5 ; −1,5 ; 1,8 ; 0,9 ; −0,4 ; 1,1 ; 2,4 ; −0,6 ; 1,3
Moyenne = 8,0 ÷ 12 ≈ 0,667 % ; écart-type ≈ 1,239 %
Taux sans risque mensuel supposé = 0,25 % (≈ 3 % par an)
Sharpe mensuel = (0,667 − 0,25) ÷ 1,239 ≈ 0,336 → annualisé ≈ 0,336 × √12 ≈ 1,16</div>
</x-approfondi>
<x-erreurs><ul><li>Ne regarder que le taux de réussite ou que le résultat total.</li><li>Ignorer le drawdown maximal, qui dit si vous supporterez la stratégie.</li><li>Calculer un Sharpe sur 3 mois et l'annualiser.</li></ul></x-erreurs>
<x-cles><ul><li>Taux de réussite, gain et perte moyens, espérance, profit factor, drawdown maximal, plus longue série de pertes.</li><li>Profit factor = gains bruts ÷ pertes brutes.</li><li>Sharpe = (rendement − taux sans risque) ÷ volatilité ; à manier avec précaution.</li></ul></x-cles>
<x-exo><p>10 trades : +2 ; −1 ; −1 ; +1,5 ; −1 ; −1 ; +3 ; −1 ; −1 ; +0,5. Calculez le taux de réussite, l'espérance, le profit factor et le drawdown maximal en R.</p>
<x-corr><div class="calcul">Gagnants : 4 → 2 + 1,5 + 3 + 0,5 = 7 R ; perdants : 6 → −6 R
Taux de réussite = 40 % ; espérance = 1 ÷ 10 = +0,1 R ; profit factor = 7 ÷ 6 ≈ 1,17
Cumul : 2 ; 1 ; 0 ; 1,5 ; 0,5 ; −0,5 ; 2,5 ; 1,5 ; 0,5 ; 1
Drawdown max : du pic 2,0 au creux −0,5 = 2,5 R</div></x-corr></x-exo>
"""),

("10-7", "Taille d'échantillon : pourquoi 30 trades ne prouvent rien", r"""
<x-obj><ul><li>Estimer l'incertitude sur une espérance mesurée.</li><li>Évaluer le nombre de trades nécessaire pour conclure.</li></ul></x-obj>
<x-simple>
<p>Une espérance mesurée sur un petit nombre de trades est <strong>très incertaine</strong>. La chance peut facilement faire paraître gagnante une stratégie neutre, ou perdante une stratégie gagnante. Plus l'échantillon est grand, plus la mesure est fiable.</p>
</x-simple>
<x-approfondi>
<div class="formule">Erreur type de l'espérance ≈ écart-type des résultats ÷ √(nombre de trades)</div>
<div class="formule">Intervalle de confiance à 95 % ≈ espérance ± 1,96 × erreur type</div>
<p>Cette approximation suppose des trades indépendants et un nombre de trades suffisant ; elle donne un ordre de grandeur utile. Conséquence : pour distinguer une petite espérance (+0,1 à +0,2R) de zéro, il faut souvent <strong>plusieurs centaines de trades</strong>.</p>
</x-approfondi>
<x-exemple>
<p>Reprenons les 20 trades de la leçon précédente : espérance +0,15R, écart-type des résultats ≈ 1,48R.</p>
<div class="calcul">Erreur type = 1,48 ÷ √20 = 1,48 ÷ 4,47 ≈ 0,33 R
Intervalle à 95 % ≈ 0,15 ± 1,96 × 0,33 = 0,15 ± 0,65 → de −0,50 R à +0,80 R
→ Impossible de dire si la stratégie est gagnante, neutre ou perdante.
Nombre de trades pour que l'intervalle exclue zéro si l'espérance vraie est 0,2 R (écart-type 1,48 R) :
n > (1,96 × 1,48 ÷ 0,2)² ≈ 210 trades</div>
</x-exemple>
<x-erreurs><ul><li>Déclarer une stratégie gagnante après 20 ou 30 trades.</li><li>Abandonner une stratégie après 10 pertes alors qu'elles sont compatibles avec ses statistiques.</li><li>Ignorer que le marché change : un très long historique peut aussi mélanger des régimes différents.</li></ul></x-erreurs>
<x-cles><ul><li>Erreur type ≈ écart-type ÷ √n ; intervalle ≈ ± 1,96 erreur type.</li><li>Une petite espérance exige des centaines de trades pour être démontrée.</li><li>Jugez une stratégie sur un échantillon suffisant, pas sur une impression.</li></ul></x-cles>
<x-exo><p>100 trades, espérance mesurée +0,25R, écart-type 1,5R. Calculez l'intervalle de confiance à 95 %. Peut-on conclure que l'espérance est positive ?</p>
<x-corr><div class="calcul">Erreur type = 1,5 ÷ √100 = 0,15 R
Intervalle = 0,25 ± 1,96 × 0,15 = 0,25 ± 0,294 → de −0,044 R à +0,544 R</div><p>L'intervalle contient zéro (de justesse) : on ne peut pas encore conclure avec ce niveau de confiance, même si les résultats sont encourageants. Il faut plus de trades.</p></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Une stratégie, c'est…</h2><ul><li>Marché, unité de temps, contexte.</li><li>Entrée précise (moment, type d'ordre).</li><li>Stop, sortie, taille, gestion, limites.</li><li>Règles testables : programmables sans ambiguïté.</li></ul></div>
<div class="encadre"><h2>Tester</h2><ul><li>Backtest : données propres, frais + slippage, plusieurs régimes.</li><li>Hors échantillon : un seul test final.</li><li>Forward test en démo ou très petite taille.</li></ul></div>
<div class="encadre"><h2>Biais</h2><ul><li>Surapprentissage : peu de paramètres, robustesse.</li><li>Survivant : composition historique.</li><li>Anticipation : info non disponible à l'époque.</li><li>Sélection : compter les essais.</li></ul></div>
<div class="encadre"><h2>Statistiques</h2><ul><li>Réussite, gain/perte moyens, espérance.</li><li>Profit factor = gains bruts ÷ pertes brutes.</li><li>Drawdown max, plus longue série de pertes.</li><li>Sharpe = (r − r<sub>f</sub>) ÷ σ ; × √12 si mensuel.</li></ul></div>
<div class="encadre"><h2>Échantillon</h2><ul><li>Erreur type ≈ σ ÷ √n.</li><li>IC 95 % ≈ E ± 1,96 × σ ÷ √n.</li><li>Petite espérance ⇒ centaines de trades nécessaires.</li></ul></div>
"""

QUIZ = [
("« Acheter quand le RSI passe sous 30 » est :", ["Une stratégie complète", "Un signal d'entrée, auquel il manque le stop, la sortie, la taille et le contexte", "Un biais du survivant", "Un backtest"], 1, "Une stratégie précise aussi le contexte, le stop, la sortie, la taille et la gestion."),
("Une règle est testable si :", ["Elle a fonctionné une fois", "Deux personnes ou un programme prennent toujours les mêmes décisions avec les mêmes données", "Elle utilise au moins trois indicateurs", "Elle vient d'un livre"], 1, "Une règle testable ne laisse aucune place à l'interprétation."),
("Espérance brute +0,18R, coûts 0,07R par trade. Espérance nette ?", ["+0,25 R", "+0,11 R", "+0,07 R", "−0,11 R"], 1, "0,18 − 0,07 = 0,11 R."),
("Le surapprentissage consiste à :", ["Tester sur trop de marchés", "Ajuster les règles au bruit du passé, au point qu'elles ne fonctionnent plus sur des données nouvelles", "Utiliser un stop trop large", "Faire du forward test"], 1, "La stratégie a « appris » le hasard du passé."),
("Tester une stratégie uniquement sur les actions qui composent l'indice aujourd'hui crée :", ["Un biais du survivant", "Un biais de confirmation", "Un effet de levier", "Un gap"], 0, "On oublie les sociétés sorties de l'indice ou disparues, souvent après de mauvaises performances."),
("Utiliser la clôture du jour pour décider d'acheter à l'ouverture de ce même jour est :", ["Correct", "Un biais d'anticipation (look-ahead)", "Un biais du survivant", "Un ratio de Sharpe"], 1, "La clôture n'était pas connue au moment de l'ouverture."),
("Gains bruts 30R, pertes brutes 20R. Profit factor ?", ["0,67", "1,5", "10", "50"], 1, "30 ÷ 20 = 1,5."),
("Une stratégie n'est rentable qu'avec une SMA de 37, pas avec 35 ou 40. C'est un signe de :", ["Robustesse", "Surapprentissage", "Faible volatilité", "Bonne diversification"], 1, "Une stratégie robuste résiste à de petites variations de ses paramètres."),
("Écart-type 2R, 100 trades. Erreur type de l'espérance ?", ["0,02 R", "0,2 R", "2 R", "20 R"], 1, "2 ÷ √100 = 0,2 R."),
("Pourquoi le forward test est-il nécessaire après un bon backtest ?", ["Il n'est pas nécessaire", "Il révèle l'exécution réelle, la discipline et un éventuel surapprentissage", "Il remplace la gestion du risque", "Il garantit les gains"], 1, "Le temps réel montre ce que le backtest ne peut pas montrer."),
("Rendement mensuel moyen 1 %, taux sans risque mensuel 0,25 %, écart-type mensuel 1,5 %. Sharpe annualisé ?", ["0,5", "≈ 1,73", "6", "12"], 1, "(1 − 0,25) ÷ 1,5 = 0,5 par mois ; × √12 ≈ 1,73."),
("20 trades, espérance +0,3R, intervalle de confiance de −0,4R à +1,0R. Conclusion ?", ["La stratégie est gagnante", "On ne peut pas encore conclure : il faut plus de trades", "La stratégie est perdante", "Il faut doubler le risque"], 1, "L'intervalle contient zéro : le résultat est compatible avec une stratégie sans avantage."),
]
