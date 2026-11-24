from svgkit import plot, table

NUM = 11
TITRE = "Psychologie du trader"
RESUME = "Peur, avidité, FOMO, revenge trading, surtrading, biais cognitifs ; discipline, routine et journal de trading (modèle fourni)."
DUREE = "2 h"
INTRO = r"""<p>Beaucoup de traders connaissent la théorie et perdent quand même, parce qu'ils n'appliquent pas leurs propres règles au moment où cela compte. Le cerveau humain n'est pas fait pour prendre des décisions probabilistes sous pression financière. Ce module ne vous rendra pas insensible aux émotions (personne ne l'est), mais il vous aidera à les <strong>reconnaître</strong> et à mettre en place des <strong>garde-fous</strong>.</p>"""

SCHEMA_PEUR = plot([{"x": [1, 2], "y": [0.125, -0.19], "kind": "bar", "cls": "g-barre-h", "cls_neg": "g-barre-b", "bw": 120}],
                   label="Espérance du plan initial et espérance réalisée après interventions émotionnelles", xr=(0.4, 2.6), yr=(-0.3, 0.2),
                   xticks=[1, 2], legend=False, xfmt=lambda v: {1: "Plan : 45 %, +1,5R / −1R", 2: "Réalisé : 55 %, +0,8R / −1,4R"}.get(int(v), ""),
                   yfmt=lambda v: f"{v:+.1f} R".replace(".", ",").replace("+0,0", "0"),
                   texts=[{"x": 1, "y": 0.14, "t": "+0,125 R", "anchor": "middle"}, {"x": 2, "y": -0.215, "t": "−0,19 R", "anchor": "middle"}])

SCHEMA_JOURNAL = plot([{"x": [1, 2, 3, 4, 5], "y": [9.2, 4.1, -6.3, -8.7, 0.5], "kind": "bar", "cls": "g-barre-h", "cls_neg": "g-barre-b", "bw": 70}],
                      label="Résultat cumulé par catégorie de trades dans un journal fictif de 120 trades", xr=(0.4, 5.6), yr=(-11, 11),
                      xticks=[1, 2, 3, 4, 5], legend=False,
                      xfmt=lambda v: {1: "Setup A (plan)", 2: "Setup B (plan)", 3: "Hors plan", 4: "Après 2 pertes", 5: "Vendredi soir"}.get(int(v), ""),
                      yfmt=lambda v: f"{v:+.0f} R".replace("+0", "0"))

LECONS = [
("11-1", "Peur et avidité", r"""
<x-obj><ul><li>Reconnaître les effets de la peur et de l'avidité sur ses décisions.</li><li>Mesurer leur coût sur l'espérance d'une stratégie.</li></ul></x-obj>
<x-simple>
<p>Deux émotions dominent le trading :</p>
<ul><li>la <strong>peur</strong> : peur de perdre (on n'ose pas entrer, on sort trop tôt d'un trade gagnant) et peur d'avoir tort (on refuse de couper une perte) ;</li>
<li>l'<strong>avidité</strong> : on augmente la taille, on vise des objectifs irréalistes, on reste trop longtemps dans un gain qui se retourne.</li></ul>
<p>Le comportement typique qui en résulte : <strong>couper ses gains trop tôt et laisser courir ses pertes</strong>, exactement l'inverse de ce qu'il faudrait.</p>
</x-simple>
<x-approfondi>
<p>Ces réactions ne sont pas des défauts de caractère : ce sont des réponses normales du cerveau au risque et à l'incertitude. On ne les supprime pas ; on les <strong>encadre</strong> par des règles décidées à froid et, autant que possible, automatisées : ordres stop et objectif placés dès l'entrée, taille calculée à l'avance, risque assez petit pour ne pas être angoissant. Un bon indicateur : si une position vous empêche de dormir ou de vous concentrer, elle est trop grosse.</p>
</x-approfondi>
<x-exemple>
<p>Plan : 45 % de réussite, objectif 1,5R, stop 1R. En pratique, le trader sort ses gains trop tôt (moyenne 0,8R) et décale ses stops (perte moyenne 1,4R). Les sorties précoces augmentent un peu le taux de réussite, à 55 %.</p>
<div class="calcul">Espérance prévue = 0,45 × 1,5 − 0,55 × 1 = 0,675 − 0,550 = +0,125 R
Espérance réalisée = 0,55 × 0,8 − 0,45 × 1,4 = 0,440 − 0,630 = −0,19 R
Sur 200 trades à 100 € de risque : prévu +2 500 € ; réalisé −3 800 €</div>
<p>Même stratégie, même marché, même trader : seule l'exécution a changé, et le résultat s'est inversé, alors que le trader gagne plus souvent qu'avant.</p>
</x-exemple>
<x-fig c="Les interventions émotionnelles (gains coupés, pertes élargies) transforment une espérance positive en espérance négative, tout en augmentant le taux de réussite.">""" + SCHEMA_PEUR + r"""</x-fig>
<x-erreurs><ul><li>Juger sa discipline à son taux de réussite (il peut monter quand on coupe ses gains).</li><li>Prendre une position si grosse que chaque tick provoque une émotion forte.</li><li>Retirer le stop « pour laisser une chance au trade ».</li></ul></x-erreurs>
<x-cles><ul><li>La peur coupe les gains, l'espoir et l'orgueil laissent courir les pertes.</li><li>Placez stop et objectif dès l'entrée ; réduisez la taille si l'émotion domine.</li><li>Mesurez le gain moyen et la perte moyenne réels, pas seulement le taux de réussite.</li></ul></x-cles>
<x-exo><p>Votre plan vise 2R pour 1R de risque avec 40 % de réussite. Votre journal montre en réalité un gain moyen de 1,3R, une perte moyenne de 1,2R et 46 % de réussite. Calculez les deux espérances.</p>
<x-corr><div class="calcul">Prévue = 0,40 × 2 − 0,60 × 1 = 0,80 − 0,60 = +0,20 R
Réalisée = 0,46 × 1,3 − 0,54 × 1,2 = 0,598 − 0,648 = −0,05 R</div><p>L'exécution a détruit l'avantage. Priorité : respecter les objectifs et ne plus déplacer les stops.</p></x-corr></x-exo>
"""),

("11-2", "FOMO, revenge trading et surtrading", r"""
<x-obj><ul><li>Identifier trois comportements destructeurs.</li><li>Chiffrer leur impact et mettre en place des parades.</li></ul></x-obj>
<x-simple>
<ul><li><strong>FOMO</strong> (Fear Of Missing Out, peur de rater) : entrer en retard dans un mouvement déjà très avancé, parce que « tout le monde gagne ».</li>
<li><strong>Revenge trading</strong> (trading de revanche) : après une perte, reprendre immédiatement une position, souvent plus grosse, pour « se refaire ».</li>
<li><strong>Surtrading</strong> : trader trop souvent, hors de son plan, par ennui, par excitation ou pour atteindre un objectif de gain.</li></ul>
</x-simple>
<x-approfondi>
<p>Parades concrètes :</p>
<ul><li><strong>FOMO</strong> : ne trader que les setups définis à l'avance ; se rappeler qu'il y aura toujours une autre occasion ; si l'entrée est trop éloignée du stop logique, le ratio n'est plus bon : on s'abstient.</li>
<li><strong>Revenge</strong> : limite de perte journalière (module 9) ; pause obligatoire (par exemple 30 minutes) après deux pertes ; jamais d'augmentation de taille après une perte.</li>
<li><strong>Surtrading</strong> : nombre maximal de trades par jour ou par semaine ; noter dans le journal la raison de chaque trade ; supprimer les notifications et applications de trading du téléphone pendant le travail.</li></ul>
</x-approfondi>
<x-exemple>
<p><strong>Revenge trading.</strong> Capital 10 000 €, risque prévu 1 % par trade, limite journalière 2 %.</p>
<div class="calcul">Trade 1 : −100 € ; trade 2 : −100 € (limite de 2 % atteinte : il faudrait s'arrêter)
Trade 3 « de revanche » avec 3 % de risque : −300 €
Perte du jour = 500 € (5 %) au lieu de 200 € (2 %)
Gain nécessaire pour revenir : 500 ÷ 9 500 ≈ 5,3 % au lieu de 200 ÷ 9 800 ≈ 2,0 %</div>
<p><strong>FOMO.</strong> Un actif a déjà monté de 4 ATR. Le stop logique est sous le dernier creux, à 4,5 ATR sous le prix actuel ; l'objectif réaliste est à 2 ATR au-dessus.</p>
<div class="calcul">R/R = 2 ÷ 4,5 ≈ 0,44 → taux de réussite minimal = 1 ÷ 1,44 ≈ 69 %
La même configuration prise au début du mouvement offrait peut-être 1:3 (seuil de 25 %).</div>
</x-exemple>
<x-erreurs><ul><li>Se dire « juste un dernier trade pour finir la journée en positif ».</li><li>Entrer sur un actif parce qu'il fait la une des réseaux sociaux.</li><li>Fixer un objectif de gain quotidien (« 100 € par jour »).</li></ul></x-erreurs>
<x-cles><ul><li>FOMO : entrées tardives, mauvais ratio. Revenge : tailles qui grossissent après les pertes. Surtrading : frais et erreurs.</li><li>Parades : setups écrits, limite de perte journalière, pause obligatoire, nombre maximal de trades.</li></ul></x-cles>
<x-exo><p>Un trader fait en moyenne 4 trades planifiés et 6 trades impulsifs par semaine. Son journal montre +0,2R par trade planifié et −0,3R par trade impulsif. Coût moyen : 0,05R par trade (déjà inclus). Quel est son résultat hebdomadaire ? Que gagnerait-il en supprimant les trades impulsifs ?</p>
<x-corr><div class="calcul">Planifiés : 4 × 0,2 = +0,8 R
Impulsifs : 6 × (−0,3) = −1,8 R
Total = −1,0 R par semaine
Sans les impulsifs : +0,8 R par semaine, soit 1,8 R de mieux</div></x-corr></x-exo>
"""),

("11-3", "Les biais cognitifs", r"""
<x-obj><ul><li>Connaître les principaux biais qui faussent les décisions de trading.</li><li>Associer à chaque biais une parade concrète.</li></ul></x-obj>
<x-simple>
<p>Les <strong>biais cognitifs</strong> sont des raccourcis de pensée systématiques, étudiés notamment par Daniel Kahneman et Amos Tversky. Ils nous trompent de façon prévisible :</p>
""" + table(["Biais", "En trading", "Parade"],
            [["Confirmation", "Ne chercher que les arguments qui confirment sa position", "Écrire le scénario qui invaliderait le trade avant d'entrer"],
             ["Ancrage", "Rester accroché à un prix (son prix d'achat, un ancien sommet)", "Raisonner sur la situation actuelle, pas sur son prix d'entrée"],
             ["Aversion à la perte", "Une perte fait plus mal qu'un gain équivalent ne fait plaisir", "Stops placés à l'avance, risque petit"],
             ["Effet de disposition", "Vendre trop vite les gagnants, garder les perdants", "Règles de sortie écrites et automatisées"],
             ["Excès de confiance", "Surestimer ses compétences après quelques gains", "Statistiques sur un grand échantillon"],
             ["Biais de récence", "Surpondérer les derniers trades", "Juger sur 100 trades, pas sur 5"],
             ["Erreur du joueur", "« Après 5 pertes, la prochaine sera gagnante »", "Les trades sont (presque) indépendants"],
             ["Illusion de contrôle", "Croire qu'on maîtrise le résultat d'un trade", "Penser en probabilités, juger le processus"]]) + r"""
</x-simple>
<x-approfondi>
<p>Selon la théorie des perspectives (Kahneman et Tversky, 1979), une perte pèse psychologiquement environ <strong>deux fois</strong> plus qu'un gain de même montant (les estimations varient selon les études, souvent entre 1,5 et 2,5). C'est ce qui pousse à refuser de « matérialiser » une perte.</p>
<p>L'<strong>effet de disposition</strong> a été documenté sur des comptes réels de particuliers : Terrance Odean (1998) a montré que des investisseurs vendaient plus volontiers leurs titres gagnants que leurs perdants, alors que les gagnants vendus ont ensuite fait mieux, sur l'année suivante, que les perdants conservés (d'environ 3,4 points de pourcentage dans son échantillon).</p>
</x-approfondi>
<x-exemple>
<p><strong>Aversion à la perte.</strong> On propose un pari : 50 % de chances de gagner 150 €, 50 % de perdre 100 €.</p>
<div class="calcul">Espérance = 0,5 × 150 − 0,5 × 100 = 75 − 50 = +25 €
Avec une perte ressentie comme deux fois plus forte : « valeur ressentie » = 0,5 × 150 − 0,5 × 2 × 100 = 75 − 100 = −25
→ La plupart des gens refusent ce pari favorable.</div>
<p><strong>Ancrage.</strong> Vous avez acheté à 50 €, le titre vaut 40 € et votre analyse est devenue négative. « J'attends de revenir à 50 € » : le marché ignore votre prix d'achat. La seule question est : achèteriez-vous ce titre aujourd'hui à 40 € ? Sinon, pourquoi le garder ?</p>
</x-exemple>
<x-erreurs><ul><li>Croire qu'on n'est pas concerné par les biais (c'est lui-même un biais).</li><li>Lire uniquement les analyses qui vont dans le sens de sa position.</li><li>Dire « ce n'est pas une perte tant que je n'ai pas vendu ».</li></ul></x-erreurs>
<x-cles><ul><li>Biais majeurs : confirmation, ancrage, aversion à la perte, disposition, excès de confiance, récence, erreur du joueur.</li><li>Une perte pèse environ deux fois plus qu'un gain équivalent.</li><li>Parade générale : règles écrites à l'avance, décisions automatisées, statistiques.</li></ul></x-cles>
<x-exo><p>Après 6 trades gagnants, un trader double sa taille de position « parce qu'il a trouvé la bonne méthode ». Quels biais sont à l'œuvre ? Que devrait-il faire ?</p>
<x-corr><p><strong>Excès de confiance</strong> et <strong>biais de récence</strong> : 6 trades ne prouvent rien (module 10 : sur un petit échantillon, le hasard domine). Il devrait garder sa taille de risque inchangée et n'envisager de l'ajuster que selon des règles écrites à l'avance, sur un échantillon de plusieurs dizaines ou centaines de trades.</p></x-corr></x-exo>
"""),

("11-4", "Discipline et routine", r"""
<x-obj><ul><li>Construire une routine avant, pendant et après la séance.</li><li>Utiliser une checklist avant chaque trade.</li></ul></x-obj>
<x-simple>
<p>La <strong>discipline</strong>, c'est faire ce que l'on a prévu, surtout quand on n'en a pas envie. Elle s'appuie sur une <strong>routine</strong> : des actions répétées chaque jour, qui réduisent le nombre de décisions prises dans l'émotion.</p>
</x-simple>
<x-approfondi>
<p><strong>Avant la séance</strong> : consulter le calendrier économique, mettre à jour les niveaux clés, vérifier les positions ouvertes et le risque total, noter son état (fatigue, stress : un mauvais jour peut justifier de ne pas trader).</p>
<p><strong>Pendant</strong> : n'agir que sur les setups du plan, appliquer la checklist, respecter les limites.</p>
<p><strong>Après</strong> : remplir le journal, capturer les graphiques des trades, noter une leçon.</p>
<p><strong>Checklist avant un trade</strong> (exemple) :</p>
<ol><li>Le setup est-il dans mon plan ? Lequel ?</li><li>Le contexte (tendance de l'unité supérieure) est-il favorable ?</li><li>Le stop est-il à un niveau logique ?</li><li>La taille est-elle calculée pour le risque prévu ?</li><li>Le ratio est-il au moins égal à mon minimum ?</li><li>Y a-t-il une annonce importante dans la durée prévue du trade ?</li><li>Mon risque total ouvert reste-t-il sous la limite ?</li><li>Suis-je dans un état émotionnel neutre (pas de revanche, pas d'euphorie) ?</li></ol>
<p>Un seul « non » = pas de trade.</p>
</x-approfondi>
<x-exemple>
<p>Un trader suit 40 setups en un mois. Il applique la checklist et en écarte 15. Son journal montre ensuite, pour les 15 trades écartés, l'issue qu'ils auraient eue :</p>
<div class="calcul">Trades pris (25) : espérance mesurée +0,22 R → total ≈ +5,5 R
Trades écartés (15), simulés après coup : espérance −0,35 R → total évité ≈ −5,25 R
Sans checklist : 5,5 − 5,25 ≈ +0,25 R pour 40 trades, soit environ 0,006 R par trade</div>
<p>La checklist n'a rien ajouté au talent de ce trader : elle a supprimé les trades qui détruisaient son résultat (chiffres illustratifs, sur un petit échantillon).</p>
</x-exemple>
<x-erreurs><ul><li>Avoir une routine « dans sa tête » plutôt qu'écrite.</li><li>Trader fatigué, malade ou contrarié.</li><li>Appliquer la checklist… après être entré en position.</li></ul></x-erreurs>
<x-cles><ul><li>Routine avant, pendant, après la séance.</li><li>Checklist avant chaque trade : un « non » = pas de trade.</li><li>Ne pas trader est aussi une décision, souvent la meilleure.</li></ul></x-cles>
<x-exo><p>Rédigez votre checklist personnelle en 6 points au maximum, adaptée à votre style (module 8).</p>
<x-corr><p>Exemple pour un swing trader : (1) setup A ou B de mon plan ; (2) prix au-dessus de la SMA 50 journalière pour un achat ; (3) stop sous le dernier creux + 0,5 ATR ; (4) taille = 1 % du capital ; (5) objectif d'au moins 2R sans résistance majeure avant ; (6) pas de résultats d'entreprise avant la fin prévue du trade. Une bonne checklist est courte, précise et vérifiable.</p></x-corr></x-exo>
"""),

("11-5", "Le journal de trading", r"""
<x-obj><ul><li>Tenir un journal de trading complet.</li><li>L'analyser pour trouver ce qui coûte de l'argent.</li></ul></x-obj>
<x-simple>
<p>Le <strong>journal de trading</strong> est le registre de chacun de vos trades : ce que vous avez prévu, ce que vous avez fait, ce qui s'est passé, et ce que vous ressentiez. C'est la base de toute amélioration : sans données, on ne fait que des suppositions.</p>
<p>Un modèle complet est disponible sur la page <a href="../journal-de-trading.html">Journal de trading</a> : version interactive dans le navigateur, export CSV pour un tableur, et version papier imprimable.</p>
</x-simple>
<x-approfondi>
<p><strong>Ce qu'il faut noter</strong> : date et heure, instrument, sens, setup (nom de la règle du plan), entrée, stop, objectif, taille, risque initial en euros, sortie, résultat en euros et en R, respect du plan (oui/non), émotion dominante, capture du graphique avant et après, leçon.</p>
<p><strong>Comment l'analyser</strong> (chaque semaine et chaque mois) : résultats par setup, par instrument, par jour et par heure ; trades dans le plan et hors plan ; résultats selon l'émotion notée ; comparaison avec les statistiques du backtest. On cherche <strong>les fuites</strong> : les catégories de trades qui coûtent de l'argent.</p>
</x-approfondi>
<x-fig c="Journal fictif de 120 trades : les setups du plan gagnent ; les trades hors plan et ceux pris juste après deux pertes détruisent la performance.">""" + SCHEMA_JOURNAL + r"""</x-fig>
<x-exemple>
<div class="calcul">Résultat total = 9,2 + 4,1 − 6,3 − 8,7 + 0,5 = −1,2 R
Sans les trades hors plan et ceux pris après 2 pertes : 9,2 + 4,1 + 0,5 = +13,8 R
Avec 100 € de risque par R : −120 € réalisés au lieu de +1 380 € possibles</div>
<p>Deux règles simples (pas de trade hors plan, pause après deux pertes) auraient suffi. Seul le journal permet de le voir.</p>
</x-exemple>
<x-erreurs><ul><li>Ne noter que les trades gagnants, ou remplir le journal « de mémoire » des jours plus tard.</li><li>Noter les trades sans jamais les analyser.</li><li>Oublier les champs « respect du plan » et « émotion », souvent les plus instructifs.</li></ul></x-erreurs>
<x-cles><ul><li>Noter chaque trade, immédiatement, y compris l'émotion et le respect du plan.</li><li>Analyser par catégorie pour trouver les fuites.</li><li>Une amélioration à la fois.</li></ul></x-cles>
<x-exo><p>Extrait d'un journal : 30 trades le matin (résultat +6R), 25 trades l'après-midi (résultat −4R), dont 15 après 16 h (résultat −7R). Quelle décision prendriez-vous ? Avec quelle précaution ?</p>
<x-corr><div class="calcul">Après-midi avant 16 h : 25 − 15 = 10 trades, résultat −4 − (−7) = +3 R
Après 16 h : 15 trades, −7 R, soit ≈ −0,47 R par trade</div><p>Décision possible : <strong>ne plus trader après 16 h</strong> (fatigue ? volatilité de l'ouverture américaine ?). Précaution : 15 trades est un petit échantillon ; on teste la règle sur les semaines suivantes et on continue à mesurer.</p></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Émotions</h2><ul><li>Peur : sorties précoces, entrées manquées.</li><li>Avidité : tailles trop grosses, objectifs irréalistes.</li><li>Gains coupés + pertes élargies = espérance détruite.</li></ul></div>
<div class="encadre"><h2>Comportements à risque</h2><ul><li>FOMO : entrée tardive, mauvais ratio.</li><li>Revenge : taille ↑ après une perte.</li><li>Surtrading : frais, erreurs.</li><li>Parades : setups écrits, limite journalière, pause, nombre max de trades.</li></ul></div>
<div class="encadre"><h2>Biais</h2><ul><li>Confirmation, ancrage, aversion à la perte (≈ ×2), disposition, excès de confiance, récence, erreur du joueur, illusion de contrôle.</li></ul></div>
<div class="encadre"><h2>Routine &amp; checklist</h2><ul><li>Avant : calendrier, niveaux, risque ouvert, état personnel.</li><li>Pendant : plan + checklist (un « non » = pas de trade).</li><li>Après : journal, captures, leçon.</li></ul></div>
<div class="encadre"><h2>Journal</h2><ul><li>Setup, entrée, stop, objectif, taille, risque, sortie, R, plan oui/non, émotion.</li><li>Analyse par setup, horaire, émotion, plan / hors plan.</li><li>Chercher les fuites, une amélioration à la fois.</li></ul></div>
"""

QUIZ = [
("Couper ses gains trop tôt et laisser courir ses pertes :", ["Améliore l'espérance", "Peut transformer une espérance positive en négative, même avec un taux de réussite plus élevé", "N'a aucun effet", "Est recommandé"], 1, "Le gain moyen baisse et la perte moyenne augmente : l'espérance s'effondre."),
("Le FOMO désigne :", ["Une figure chartiste", "La peur de rater un mouvement, qui pousse à entrer en retard", "Un ordre OCO", "Une stratégie de couverture"], 1, "Fear Of Missing Out : entrer dans un mouvement déjà avancé, souvent avec un mauvais ratio."),
("Après deux pertes, le trader double sa taille pour se refaire. C'est :", ["Une gestion du risque adaptée", "Du revenge trading", "Du position trading", "Un biais du survivant"], 1, "Le trading de revanche augmente le risque au pire moment."),
("Selon la théorie des perspectives, une perte pèse psychologiquement environ :", ["Autant qu'un gain équivalent", "Deux fois plus qu'un gain équivalent", "Dix fois moins", "Rien"], 1, "Les estimations courantes se situent autour de 2 (souvent entre 1,5 et 2,5)."),
("« J'attendrai de revenir à mon prix d'achat pour vendre » illustre :", ["Le biais d'ancrage", "Le biais de récence", "Le FOMO", "La diversification"], 0, "Le marché ignore votre prix d'entrée ; seule compte l'analyse actuelle."),
("L'effet de disposition consiste à :", ["Vendre trop vite ses gagnants et garder ses perdants", "Diversifier son portefeuille", "Utiliser des stops", "Tenir un journal"], 0, "Il a été documenté sur des comptes réels de particuliers (Odean, 1998)."),
("« Après 5 pertes, la suivante sera forcément gagnante » est :", ["Vrai", "L'erreur du joueur", "Une loi statistique", "Le biais de confirmation"], 1, "Les trades sont (approximativement) indépendants : le passé ne rend pas un gain « dû »."),
("Plan : 40 %, +2R / −1R. Réalisé : 50 %, +1R / −1,3R. Espérance réalisée ?", ["+0,20 R", "−0,15 R", "+0,35 R", "0"], 1, "0,5 × 1 − 0,5 × 1,3 = 0,5 − 0,65 = −0,15 R (contre +0,20 R prévu)."),
("Dans une checklist avant trade, un seul « non » signifie :", ["Prendre le trade en réduisant un peu la taille", "Ne pas prendre le trade", "Prendre le trade si l'intuition est bonne", "Doubler le stop"], 1, "La checklist ne fonctionne que si elle est appliquée strictement."),
("Le principal intérêt du journal de trading est :", ["De se souvenir de ses gains", "D'identifier, données à l'appui, les catégories de trades qui coûtent de l'argent", "De remplacer le stop loss", "D'obtenir un meilleur spread"], 1, "Sans données, on ne fait que des suppositions sur ses erreurs."),
("Quelle information du journal est souvent la plus révélatrice ?", ["La couleur du graphique", "Le respect du plan et l'émotion dominante", "Le nom du courtier", "L'heure de lever"], 1, "Elles permettent de séparer la qualité de la stratégie de la qualité de l'exécution."),
]
