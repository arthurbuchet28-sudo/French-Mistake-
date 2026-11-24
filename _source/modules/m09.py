import math
from svgkit import plot, table, svg, t, line, arrow, path_from, candles

NUM = 9
TITRE = "Gestion du risque"
RESUME = "Le module central : risque par trade, taille de position, stops, ratio risque/rendement, espérance, drawdown, séries de pertes, risque de ruine, corrélation."
DUREE = "4 h"
INTRO = r"""<p>Si vous ne deviez retenir qu'un module, ce serait celui-ci. On ne contrôle pas le marché ; on contrôle <strong>combien on risque</strong>, <strong>où l'on sort</strong> et <strong>combien de positions on ouvre</strong>. Une stratégie médiocre avec une excellente gestion du risque survit et peut s'améliorer. Une excellente stratégie avec une mauvaise gestion du risque finit, tôt ou tard, par une perte dont on ne se relève pas.</p>
<p>Tous les calculs de ce module peuvent être refaits avec les <a href="../outils.html">calculateurs et simulateurs</a>.</p>"""

_L = [10, 20, 30, 40, 50, 60, 75]
SCHEMA_ASYM = plot([{"x": _L, "y": _L, "kind": "bar", "cls": "g-barre-b", "bw": 22, "label": "Perte subie (%)"},
                    {"x": [l + 3.2 for l in _L], "y": [min(l / (100 - l) * 100, 300) for l in _L], "kind": "bar", "cls": "g-barre-h", "bw": 22, "label": "Gain nécessaire pour revenir (%)"}],
                   label="Asymétrie entre pertes et gains nécessaires pour les compenser", xr=(4, 82), yr=(0, 320), xticks=_L,
                   xfmt=lambda v: f"−{v:.0f} %", yfmt=lambda v: f"{v:.0f} %", xlabel="Perte subie",
                   texts=[{"x": l + 3.2, "y": l / (100 - l) * 100 + 8, "t": f"+{l / (100 - l) * 100:.0f} %", "anchor": "middle", "cls": "g-txt g-petit"} for l in _L])

_n = list(range(0, 21))
SCHEMA_SERIE = plot([{"x": _n, "y": [10000 * (1 - r / 100) ** k for k in _n], "cls": c, "label": f"Risque de {r} % par trade"}
                     for r, c in [(1, "g-lh"), (2, "g-l1"), (5, "g-l2"), (10, "g-lb")]],
                    label="Capital restant après une série de pertes consécutives selon le risque par trade",
                    xlabel="Nombre de pertes consécutives", yr=(0, 10500), legend_xy=(60, 140),
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:,.0f} €".replace(",", " "))

_E = path_from([(0, 44.0), (8, 42.2), (14, 43.6), (18, 42.6)], seed=91, noise=0.25, wick=0.3)
SCHEMA_TAILLE = candles(_E, h=260, label="Taille de position : la distance au stop détermine la quantité",
                        lines=[{"y": 42.50, "cls": "g-l1", "label": "Entrée 42,50"}, {"y": 40.80, "cls": "g-lb", "label": "Stop 40,80"}],
                        zones=[{"y1": 40.80, "y2": 42.50, "cls": "g-zone-res", "label": "Distance : 1,70 € par action"}], ymin=40.2)

_S = path_from([(0, 100), (10, 106), (16, 102.2), (24, 108)], seed=93, noise=0.5, wick=0.6)
_low = min(c[2] for c in _S[12:20])
SCHEMA_STOPS = candles(_S, h=280, label="Trois façons de placer un stop pour un achat sur repli",
                       lines=[{"y": 103.6, "cls": "g-l1", "label": "Entrée 103,60"},
                              {"y": 102.9, "cls": "g-l3", "label": "Stop arbitraire (−0,70) : dans le bruit"},
                              {"y": round(_low - 0.6, 2), "cls": "g-lb", "label": f"Stop sous la structure ({_low - 0.6:.2f})".replace(".", ",")},
                              {"y": 103.6 - 2 * 1.3, "cls": "g-l2", "label": "Stop à 2 ATR (101,00)"}])

_R = [0.5 + i * 0.1 for i in range(46)]
SCHEMA_SEUIL = plot([{"x": _R, "y": [100 / (1 + r) for r in _R], "cls": "g-l1", "label": "Taux de réussite minimal = 1 ÷ (1 + R)"}],
                    label="Taux de réussite minimal pour ne pas perdre selon le ratio risque/rendement",
                    xlabel="Ratio gain visé / risque (R)", yr=(0, 70), xr=(0.5, 5),
                    legend_xy=(250, 20),
                    xfmt=lambda v: f"{v:g}".replace(".", ","), yfmt=lambda v: f"{v:.0f} %",
                    marks=[{"x": 1, "y": 50, "t": "1:1 → 50 %"}, {"x": 2, "y": 100 / 3, "t": "1:2 → 33,3 %"}, {"x": 3, "y": 25, "t": "1:3 → 25 %"}])

_w = [i for i in range(10, 81)]
SCHEMA_ESP = plot([{"x": _w, "y": [w / 100 * R - (1 - w / 100) for w in _w], "cls": c, "label": f"R = {R}".replace(".", ",")}
                   for R, c in [(1, "g-lb"), (1.5, "g-l2"), (2, "g-l1"), (3, "g-lh")]],
                  label="Espérance par trade (en R) selon le taux de réussite, pour plusieurs ratios", xlabel="Taux de réussite (%)",
                  yr=(-1, 2.2), xfmt=lambda v: f"{v:.0f} %", yfmt=lambda v: f"{v:+.1f} R".replace(".", ",").replace("+0,0", "0"))

_eq = [10000, 10400, 10900, 11200, 10600, 9800, 10200, 10500, 9600, 9100, 9900, 10800, 11500, 12000]
_pk, _dd = 0, []
for v in _eq:
    _pk = max(_pk, v)
    _dd.append((v / _pk - 1) * 100)
SCHEMA_DD = ('<div class="duo">' +
             plot([{"x": list(range(len(_eq))), "y": _eq, "cls": "g-l1", "label": "Capital"}], w=420, h=240, label="Courbe de capital",
                  xlabel="Semaines", yfmt=lambda v: f"{v:,.0f}".replace(",", " "), xfmt=lambda v: f"{v:.0f}",
                  marks=[{"x": 3, "y": 11200, "t": "Pic 11 200", "dy": -8}, {"x": 9, "y": 9100, "t": "Creux 9 100", "dy": 16, "dx": -30}]) +
             plot([{"x": list(range(len(_eq))), "y": _dd, "cls": "g-lb", "label": "Drawdown (%)"}], w=420, h=240, label="Courbe de drawdown",
                  xlabel="Semaines", yr=(-22, 2), yfmt=lambda v: f"{v:.0f} %", xfmt=lambda v: f"{v:.0f}",
                  marks=[{"x": 9, "y": -18.75, "t": "−18,75 %", "dy": 4}]) + '</div>')


def _prob_serie(n, k, q):
    e = [0] * k
    e[0] = 1
    a = 0
    for _ in range(n):
        nv = [0] * k
        for j in range(k):
            if not e[j]:
                continue
            nv[0] += e[j] * (1 - q)
            if j + 1 >= k:
                a += e[j] * q
            else:
                nv[j + 1] += e[j] * q
        e = nv
    return a


_k = list(range(3, 16))
SCHEMA_SERIES_PROBA = plot([{"x": _k, "y": [_prob_serie(n, k, 0.55) * 100 for k in _k], "cls": c, "label": f"Sur {n} trades"}
                            for n, c in [(50, "g-l2"), (100, "g-l1"), (500, "g-lb")]],
                           label="Probabilité de subir au moins une série de k pertes consécutives (taux de réussite 45 %)",
                           xlabel="Longueur de la série de pertes (k)", yr=(0, 105), legend_xy=(300, 20),
                           xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f} %")

_rho = [i / 20 for i in range(-20, 21)]
SCHEMA_CORR = plot([{"x": _rho, "y": [math.sqrt(2 + 2 * r) for r in _rho], "cls": "g-l1", "label": "Risque combiné de deux positions à 1 % chacune"}],
                   label="Risque combiné de deux positions selon leur corrélation", xlabel="Corrélation entre les deux positions",
                   yr=(0, 2.2), xfmt=lambda v: f"{v:g}".replace(".", ","), yfmt=lambda v: f"{v:.1f} %".replace(".", ","),
                   marks=[{"x": 0, "y": math.sqrt(2), "t": "0 → 1,41 %", "dy": 16}, {"x": 0.8, "y": math.sqrt(3.6), "t": "0,8 → 1,90 %", "dx": -70, "dy": -8},
                          {"x": -1, "y": 0, "t": "−1 → 0 % (couverture parfaite)", "dy": -8}])

LECONS = [
("9-1", "Pourquoi le risque passe avant l'entrée", r"""
<x-obj><ul><li>Comprendre l'asymétrie entre pertes et gains.</li><li>Savoir pourquoi la préservation du capital est la priorité.</li></ul></x-obj>
<x-simple>
<p>Les débutants passent l'essentiel de leur temps à chercher le « bon » point d'entrée. Les traders expérimentés passent l'essentiel du leur à décider <strong>combien risquer</strong> et <strong>où sortir</strong>. La raison est mathématique : une perte se rattrape beaucoup plus difficilement qu'elle ne se subit.</p>
<div class="formule">Gain nécessaire pour revenir = Perte ÷ (1 − Perte)</div>
</x-simple>
<x-fig c="Plus la perte est grande, plus le gain nécessaire pour revenir au point de départ explose.">""" + SCHEMA_ASYM + r"""</x-fig>
<x-approfondi>
<p>Cette asymétrie a une conséquence directe : <strong>éviter les grosses pertes compte plus que réussir les gros gains</strong>. Un trader qui perd 50 % doit doubler son capital pour revenir à zéro, ce qui peut prendre des années, voire ne jamais arriver.</p>
<p>La gestion du risque répond à trois questions, avant chaque trade : <strong>Combien</strong> suis-je prêt à perdre si j'ai tort (risque par trade) ? <strong>Où</strong> saurai-je que j'ai tort (stop) ? <strong>Quelle quantité</strong> en découle (taille de position) ? Et, au niveau du compte : combien de risque total ai-je en même temps (exposition, corrélation), et quand dois-je m'arrêter (limites de perte) ?</p>
</x-approfondi>
<x-exemple>
""" + table(["Perte", "Capital restant (sur 10 000 €)", "Gain nécessaire pour revenir"],
            [["−10 %", "9 000 €", "1 000 ÷ 9 000 = +11,1 %"], ["−20 %", "8 000 €", "+25 %"], ["−30 %", "7 000 €", "+42,9 %"],
             ["−50 %", "5 000 €", "+100 %"], ["−75 %", "2 500 €", "+300 %"], ["−90 %", "1 000 €", "+900 %"]]) + r"""
<div class="calcul">Exemple : −30 % → gain nécessaire = 0,30 ÷ (1 − 0,30) = 0,30 ÷ 0,70 ≈ 42,9 %</div>
</x-exemple>
<x-erreurs><ul><li>Penser « je perds 30 %, il me suffit de regagner 30 % ».</li><li>Prendre plus de risque après une perte pour « revenir plus vite ».</li><li>Consacrer des heures à l'entrée et quelques secondes à la taille de position.</li></ul></x-erreurs>
<x-cles><ul><li>Gain nécessaire = perte ÷ (1 − perte) : l'asymétrie est brutale.</li><li>Éviter les grosses pertes est la priorité absolue.</li><li>Avant chaque trade : combien je risque, où je sors, quelle taille.</li></ul></x-cles>
<x-exo><p>Un compte passe de 25 000 € à 16 000 €. Quelle est la perte en % ? Quel gain faut-il pour revenir à 25 000 € ?</p>
<x-corr><div class="calcul">Perte = (25 000 − 16 000) ÷ 25 000 = 36 %
Gain nécessaire = 25 000 ÷ 16 000 − 1 = 56,25 % (ou 0,36 ÷ 0,64 = 56,25 %)</div></x-corr></x-exo>
"""),

("9-2", "Le risque par trade : la règle des 1 à 2 %", r"""
<x-obj><ul><li>Fixer un risque par trade en pourcentage du capital.</li><li>Comprendre l'origine et les limites de la « règle des 1 à 2 % ».</li></ul></x-obj>
<x-simple>
<p>Le <strong>risque par trade</strong> est la perte maximale acceptée si le stop est touché, exprimée en pourcentage du capital. Une convention très répandue recommande de ne pas dépasser <strong>1 à 2 %</strong> par trade (et souvent 0,5 à 1 % pour un débutant). Avec 10 000 €, 1 % = 100 € de perte maximale prévue par trade.</p>
<p>Le risque n'est <strong>pas</strong> le montant investi : on peut investir 5 000 € et ne risquer que 100 € si le stop est proche.</p>
</x-simple>
<x-fig c="Après 10 pertes consécutives (ce qui arrive), il reste 9 044 € avec 1 % de risque par trade… et 3 487 € avec 10 %.">""" + SCHEMA_SERIE + r"""</x-fig>
<x-note><p>La règle des 1 à 2 % est une <strong>convention prudente</strong> issue de la pratique, pas une loi démontrée. Le niveau « optimal » dépend de l'espérance réelle de la stratégie, de sa variabilité et de la tolérance du trader au drawdown. La théorie (critère de Kelly : f = p − (1 − p) ÷ R) donne une fraction qui maximise la croissance à long terme… mais seulement si l'on connaît parfaitement les vraies probabilités, ce qui n'est jamais le cas, et au prix de drawdowns très violents. Par exemple, avec 45 % de réussite et R = 1,5, Kelly donne 0,45 − 0,55 ÷ 1,5 ≈ 8,3 % par trade, un niveau que presque aucun professionnel n'utiliserait. En pratique, une petite fraction fixe protège contre l'erreur d'estimation, qui est la règle plutôt que l'exception.</p></x-note>
<x-approfondi>
<p>Deux variantes : risque en % du capital <strong>courant</strong> (le montant baisse après des pertes et monte après des gains : c'est automatiquement protecteur) ou en % du capital <strong>initial</strong> (montant fixe, plus simple, mais moins protecteur en cas de drawdown). Le risque se calcule sur le stop prévu : n'oubliez pas qu'un gap ou un slippage peuvent le dépasser (module 2), d'où l'intérêt de garder une marge.</p>
</x-approfondi>
<x-exemple>
<p>Capital de 10 000 €, 10 pertes consécutives, risque en % du capital courant :</p>
<div class="calcul">1 %  : 10 000 × 0,99^10 ≈ 9 044 € (−9,6 %)
2 %  : 10 000 × 0,98^10 ≈ 8 171 € (−18,3 %)
5 %  : 10 000 × 0,95^10 ≈ 5 987 € (−40,1 %)
10 % : 10 000 × 0,90^10 ≈ 3 487 € (−65,1 %), il faut ensuite +187 % pour revenir</div>
</x-exemple>
<x-erreurs><ul><li>Confondre montant investi et montant risqué.</li><li>Augmenter le risque « quand on est sûr de soi ».</li><li>Fixer le risque après avoir choisi la taille de position, au lieu de l'inverse.</li></ul></x-erreurs>
<x-cles><ul><li>Risque par trade = perte si le stop est touché, en % du capital.</li><li>Convention : 0,5 à 2 %, plutôt bas pour débuter.</li><li>C'est une convention de prudence ; l'optimum théorique dépend de paramètres qu'on ne connaît pas avec certitude.</li></ul></x-cles>
<x-exo><p>Capital de 7 500 €, risque de 1,5 % par trade. Quel est le risque en euros ? Après une perte, en % du capital courant, quel est le nouveau risque ?</p>
<x-corr><div class="calcul">Risque = 7 500 × 1,5 % = 112,50 €
Capital après perte = 7 500 − 112,50 = 7 387,50 €
Nouveau risque = 7 387,50 × 1,5 % ≈ 110,81 €</div></x-corr></x-exo>
"""),

("9-3", "Calculer la taille de position", r"""
<x-obj><ul><li>Calculer la taille de position pour des actions, du Forex, des CFD et des futures.</li><li>Identifier les cas où la taille minimale rend le trade impossible.</li></ul></x-obj>
<x-simple>
<div class="formule">Taille = Montant risqué ÷ (Distance au stop × Valeur d'une unité de mouvement)</div>
<p>On part du montant qu'on accepte de perdre, on mesure la distance entre l'entrée et le stop, et on en déduit la quantité. On arrondit toujours <strong>vers le bas</strong>.</p>
</x-simple>
<x-fig c="Le stop est placé à un endroit logique ; la taille s'adapte à la distance, et non l'inverse.">""" + SCHEMA_TAILLE + r"""</x-fig>
<x-exemple t="🧮 Exemple 1 : actions">
<div class="calcul">Capital 20 000 € ; risque 1 % = 200 €
Entrée 42,50 € ; stop 40,80 € → distance 1,70 € par action
Taille = 200 ÷ 1,70 = 117,6 → 117 actions
Risque réel = 117 × 1,70 = 198,90 € ; valeur de la position = 117 × 42,50 = 4 972,50 €</div>
</x-exemple>
<x-exemple t="🧮 Exemple 2 : Forex">
<div class="calcul">Capital 10 000 € ; risque 1 % = 100 €
EUR/USD : entrée 1,0850 ; stop 1,0815 → 35 pips
Valeur du pip pour 1 lot ≈ 9,20 € (10 $ avec 1 € = 1,087 $)
Taille = 100 ÷ (35 × 9,20) = 100 ÷ 322 = 0,31 lot
Risque réel = 0,31 × 35 × 9,20 ≈ 99,82 €</div>
</x-exemple>
<x-exemple t="🧮 Exemple 3 : CFD sur indice">
<div class="calcul">Capital 15 000 € ; risque 0,5 % = 75 €
Entrée 7 500 ; stop 7 462 → 38 points ; 1 contrat = 1 € par point ; pas minimal 0,1
Taille = 75 ÷ 38 = 1,97 → 1,9 contrat ; risque réel = 1,9 × 38 = 72,20 €</div>
</x-exemple>
<x-exemple t="🧮 Exemple 4 : future (quand la taille minimale pose problème)">
<div class="calcul">Capital 30 000 € ; risque 1 % = 300 € ; stop à 25 points
Micro-future à 5 $ par point ≈ 4,60 € par point → 25 × 4,60 = 115 € par contrat
Taille = 300 ÷ 115 = 2,6 → 2 contrats ; risque réel = 230 €
Future standard à 50 $ par point : 25 × 50 = 1 250 $ ≈ 1 150 € pour UN contrat = 3,8 % du capital
→ trop gros : il faut renoncer, ou prendre le micro-contrat</div>
</x-exemple>
<x-approfondi>
<p>Vérifications à faire ensuite : la marge requise est-elle disponible ? Le levier effectif total du compte reste-t-il raisonnable ? Les frais ont-ils été pris en compte (on peut les retrancher du budget de risque) ? La position n'est-elle pas trop grosse par rapport à la liquidité de l'actif ?</p>
</x-approfondi>
<x-erreurs><ul><li>Prendre « 1 lot » ou « 100 actions » par habitude, quel que soit le stop.</li><li>Arrondir vers le haut.</li><li>Oublier la conversion de devise sur le Forex et les futures étrangers.</li><li>Rapprocher le stop d'un niveau illogique juste pour pouvoir prendre une taille plus grosse.</li></ul></x-erreurs>
<x-cles><ul><li>Taille = risque ÷ (distance au stop × valeur unitaire), arrondie vers le bas.</li><li>Le stop est choisi pour des raisons de marché ; la taille en découle.</li><li>Si la taille minimale dépasse le risque autorisé : on ne prend pas le trade.</li></ul></x-cles>
<x-exo><p>Capital 12 000 €, risque 1 %. Vente à découvert d'une action à 64 €, stop à 66,40 €. Combien d'actions ? Avec un CFD (levier 5), quelle marge est immobilisée ?</p>
<x-corr><div class="calcul">Risque = 120 € ; distance = 66,40 − 64 = 2,40 €
Taille = 120 ÷ 2,40 = 50 actions
Valeur = 50 × 64 = 3 200 € ; marge (20 %) = 640 €</div></x-corr></x-exo>
"""),

("9-4", "Placer le stop loss et le take profit", r"""
<x-obj><ul><li>Placer un stop là où l'hypothèse de trade est invalidée.</li><li>Choisir une méthode de sortie en gain.</li></ul></x-obj>
<x-simple>
<p>Le <strong>stop loss</strong> se place à l'endroit où, si le prix y arrive, votre idée de trade est <strong>fausse</strong>. Ce n'est pas un montant « que vous voulez bien perdre » : c'est un niveau de marché. Le <strong>take profit</strong> (objectif) est l'endroit où vous prévoyez d'encaisser le gain.</p>
</x-simple>
<x-fig c="Un stop arbitraire très proche est dans le bruit normal ; un stop sous la structure ou à 2 ATR laisse respirer le trade. La taille de position s'adapte.">""" + SCHEMA_STOPS + r"""</x-fig>
<x-approfondi>
<p><strong>Méthodes de stop</strong> :</p>
<ul><li><strong>Structurel</strong> : au-delà du dernier creux (achat) ou sommet (vente), d'un support ou d'une résistance, avec une petite marge.</li>
<li><strong>Volatilité</strong> : à un multiple de l'ATR (1,5 à 3 ATR selon le style), pour rester hors du bruit.</li>
<li><strong>Temps</strong> : sortir si le trade n'a pas évolué après une durée donnée.</li></ul>
<p><strong>Méthodes de sortie en gain</strong> : objectif fixe sur un niveau (résistance, objectif de figure), multiple du risque (2R, 3R), sortie partielle (la moitié à 1R, le reste suivi par un trailing stop), sortie sur signal contraire. Aucune n'est supérieure dans l'absolu : il faut la tester avec la stratégie.</p>
<p><strong>Règle d'or</strong> : un stop peut être déplacé dans le sens du trade (pour protéger un gain), jamais dans le sens de la perte.</p>
</x-approfondi>
<x-exemple>
<p>Achat sur repli à 103,60. Dernier creux à 102,43. ATR = 1,30. Risque = 130 €.</p>
<div class="calcul">Stop arbitraire à 102,90 : distance 0,70 → 130 ÷ 0,70 = 185 unités, mais stop dans le bruit (moins d'une ATR)
Stop structurel = 102,43 − 0,60 = 101,83 : distance 1,77 → 130 ÷ 1,77 = 73 unités
Stop à 2 ATR = 103,60 − 2,60 = 101,00 : distance 2,60 → 130 ÷ 2,60 = 50 unités
Objectif à 2R avec le stop structurel : 103,60 + 2 × 1,77 = 107,14</div>
<p>La perte en euros est la même dans les trois cas ; seule la probabilité d'être sorti par le bruit change.</p>
</x-exemple>
<x-erreurs><ul><li>Placer le stop en fonction de l'argent qu'on veut perdre, sans regarder le graphique.</li><li>Déplacer le stop plus loin quand le prix s'en approche.</li><li>Ne pas avoir de stop « parce qu'on surveille ».</li><li>Placer un objectif juste derrière une résistance majeure.</li></ul></x-erreurs>
<x-cles><ul><li>Stop = niveau d'invalidation (structure, volatilité, temps).</li><li>Sortie en gain : niveau, multiple de R, partielle, trailing.</li><li>On déplace un stop uniquement pour réduire le risque.</li></ul></x-cles>
<x-exo><p>Vente à découvert à 58,00 ; dernier sommet à 59,60 ; ATR = 0,80 ; risque 100 €. Placez un stop structurel (marge de 0,5 ATR), calculez la taille et un objectif à 2R.</p>
<x-corr><div class="calcul">Stop = 59,60 + 0,40 = 60,00 → distance 2,00
Taille = 100 ÷ 2,00 = 50 actions
Objectif à 2R = 58,00 − 2 × 2,00 = 54,00</div></x-corr></x-exo>
"""),

("9-5", "Le ratio risque/rendement", r"""
<x-obj><ul><li>Calculer le ratio risque/rendement d'un trade.</li><li>Relier ce ratio au taux de réussite minimal.</li><li>Comprendre pourquoi un bon ratio seul ne suffit pas.</li></ul></x-obj>
<x-simple>
<p>Le <strong>ratio risque/rendement</strong> (R/R) compare ce que vous risquez à ce que vous visez. Si vous risquez 2 € pour en gagner 6, le ratio est de 1:3 (on dit aussi que l'objectif est à 3R, R désignant le risque initial).</p>
<div class="formule">Taux de réussite minimal (sans frais) = 1 ÷ (1 + R)</div>
</x-simple>
<x-fig c="Plus le ratio est élevé, plus le taux de réussite nécessaire est faible.">""" + SCHEMA_SEUIL + r"""</x-fig>
<x-approfondi>
<p>Piège fréquent : « je ne prends que des trades à 1:3, donc je suis gagnant ». Faux : plus l'objectif est lointain, plus la probabilité de l'atteindre baisse. Un ratio de 1:5 avec 10 % de réussite perd de l'argent. Le ratio et le taux de réussite sont <strong>liés</strong> et doivent être mesurés ensemble, sur un historique (module 10). Le ratio prévu n'est pas non plus le ratio réalisé : sorties anticipées, slippage et frais le dégradent.</p>
</x-approfondi>
<x-exemple>
<div class="calcul">Entrée 50 ; stop 48 ; objectif 56
Risque = 2 ; gain visé = 6 → R = 3 (ratio 1:3)
Taux de réussite minimal = 1 ÷ (1 + 3) = 25 %
Avec R = 1 : 50 % ; R = 2 : 33,3 % ; R = 0,5 : 66,7 %</div>
<p>Avec des frais de 0,1R par trade, le gain net devient 2,9R et la perte nette 1,1R : seuil = 1,1 ÷ (2,9 + 1,1) = 27,5 %.</p>
</x-exemple>
<x-erreurs><ul><li>Fixer des objectifs irréalistes pour afficher un « beau » ratio.</li><li>Oublier que le ratio réalisé est souvent inférieur au ratio prévu.</li><li>Juger une stratégie sur son ratio sans connaître son taux de réussite.</li></ul></x-erreurs>
<x-cles><ul><li>R/R = gain visé ÷ risque.</li><li>Seuil de réussite = 1 ÷ (1 + R), plus élevé avec les frais.</li><li>Ratio et taux de réussite vont ensemble.</li></ul></x-cles>
<x-exo><p>Entrée 1,2700 ; stop 1,2660 ; objectif 1,2760. Calculez R et le taux de réussite minimal. Si vous gagnez 38 % du temps, êtes-vous rentable (sans frais) ?</p>
<x-corr><div class="calcul">Risque = 40 pips ; gain visé = 60 pips → R = 1,5
Seuil = 1 ÷ 2,5 = 40 %
Avec 38 % : espérance = 0,38 × 1,5 − 0,62 = −0,05R → légèrement perdant</div></x-corr></x-exo>
"""),

("9-6", "Taux de réussite et espérance mathématique", r"""
<x-obj><ul><li>Calculer l'espérance d'une stratégie en R et en euros.</li><li>Interpréter une espérance positive ou négative.</li></ul></x-obj>
<x-simple>
<p>L'<strong>espérance mathématique</strong> est le gain moyen attendu par trade sur un grand nombre de trades :</p>
<div class="formule">Espérance = (taux de réussite × gain moyen) − (taux d'échec × perte moyenne)</div>
<p>Exprimée en R (multiples du risque), elle permet de comparer des stratégies indépendamment de la taille des positions. Une espérance positive est une condition <strong>nécessaire</strong> pour gagner à long terme ; la gestion du risque ne peut pas rendre gagnante une espérance négative.</p>
</x-simple>
<x-fig c="L'espérance dépend à la fois du taux de réussite et du ratio : un taux de 40 % peut suffire avec R = 2, pas avec R = 1.">""" + SCHEMA_ESP + r"""</x-fig>
<x-approfondi>
<p>L'espérance se mesure sur un <strong>échantillon</strong> de trades réels ou simulés. Avec peu de trades, l'estimation est très incertaine (module 10). Elle doit être calculée <strong>après frais</strong>. Enfin, une espérance positive ne garantit pas une progression régulière : la variance peut produire de longues périodes de pertes (leçons 9.7 et 9.8).</p>
</x-approfondi>
<x-exemple>
<p>Votre journal montre 50 trades : 22 gagnants avec un gain moyen de +2,1R, 28 perdants avec une perte moyenne de −1R.</p>
<div class="calcul">Taux de réussite = 22 ÷ 50 = 44 %
Espérance = 0,44 × 2,1 − 0,56 × 1 = 0,924 − 0,560 = +0,364 R par trade
Avec un risque de 100 € par trade : +36,40 € par trade en moyenne
Sur 100 trades : ≈ +36,4 R, soit +3 640 € en moyenne… avec une forte incertitude sur 50 trades seulement</div>
</x-exemple>
<x-erreurs><ul><li>Juger une stratégie sur son taux de réussite seul.</li><li>Calculer l'espérance avant frais.</li><li>Croire qu'une gestion de position « astucieuse » (doubler après une perte…) peut rendre une espérance négative positive.</li></ul></x-erreurs>
<x-cles><ul><li>Espérance = p × gain moyen − (1 − p) × perte moyenne.</li><li>En R pour comparer ; en euros pour la réalité ; toujours après frais.</li><li>Espérance positive = condition nécessaire, pas suffisante.</li></ul></x-cles>
<x-exo><p>Stratégie A : 60 % de réussite, gain moyen 0,9R, perte moyenne 1R. Stratégie B : 35 % de réussite, gain moyen 2,4R, perte moyenne 1R. Laquelle a la meilleure espérance ?</p>
<x-corr><div class="calcul">A : 0,60 × 0,9 − 0,40 × 1 = 0,54 − 0,40 = +0,14 R
B : 0,35 × 2,4 − 0,65 × 1 = 0,84 − 0,65 = +0,19 R</div><p>B a une meilleure espérance, mais elle perd 65 % du temps : psychologiquement plus difficile, avec des séries de pertes plus longues.</p></x-corr></x-exo>
"""),

("9-7", "Le drawdown", r"""
<x-obj><ul><li>Calculer un drawdown et un drawdown maximal.</li><li>Anticiper le temps et l'effort de récupération.</li></ul></x-obj>
<x-simple>
<p>Le <strong>drawdown</strong> est la baisse du capital depuis son plus haut précédent. Le <strong>drawdown maximal</strong> est la pire baisse observée, du pic au creux, sur une période. C'est la mesure la plus concrète de la « douleur » d'une stratégie.</p>
<div class="formule">Drawdown = (Pic − Valeur actuelle) ÷ Pic</div>
</x-simple>
<x-fig c="La courbe de drawdown (en rouge) montre en permanence la distance au dernier plus haut.">""" + SCHEMA_DD + r"""</x-fig>
<x-approfondi>
<p>Toutes les stratégies connaissent des drawdowns. La question est de savoir si celui que vous vivez est « normal » (comparable à ce que montrent vos tests) ou anormal (signe que la stratégie ne fonctionne plus). D'où l'intérêt de connaître à l'avance le drawdown maximal historique et la plus longue période sans nouveau plus haut. Une règle prudente : s'attendre à vivre en réel un drawdown <strong>plus important</strong> que celui du backtest.</p>
</x-approfondi>
<x-exemple>
<p>Capital hebdomadaire : 10 000 → 10 400 → 10 900 → <strong>11 200</strong> → 10 600 → 9 800 → 10 200 → 10 500 → 9 600 → <strong>9 100</strong> → 9 900 → 10 800 → 11 500 → 12 000.</p>
<div class="calcul">Pic = 11 200 ; creux suivant le plus bas = 9 100
Drawdown maximal = (11 200 − 9 100) ÷ 11 200 = 2 100 ÷ 11 200 = 18,75 %
Gain nécessaire depuis le creux pour retrouver le pic = 11 200 ÷ 9 100 − 1 ≈ 23,1 %
Durée du drawdown : de la semaine 3 à la semaine 12 (nouveau plus haut à 11 500), soit 9 semaines</div>
</x-exemple>
<x-erreurs><ul><li>Mesurer le drawdown depuis le capital de départ plutôt que depuis le plus haut.</li><li>Augmenter le risque pendant un drawdown pour en sortir plus vite.</li><li>Ne pas avoir défini à l'avance le drawdown qui déclenche une pause et une révision.</li></ul></x-erreurs>
<x-cles><ul><li>Drawdown = baisse depuis le dernier plus haut ; drawdown max = pire pic-creux.</li><li>Récupération = pic ÷ creux − 1.</li><li>S'attendre à pire en réel qu'en backtest.</li></ul></x-cles>
<x-exo><p>Capital : 5 000 → 5 600 → 5 300 → 6 100 → 5 200 → 5 500 → 6 300. Calculez le drawdown maximal.</p>
<x-corr><div class="calcul">Premier pic 5 600 → creux 5 300 : 5,4 %
Pic 6 100 → creux 5 200 : (6 100 − 5 200) ÷ 6 100 ≈ 14,8 %
Drawdown maximal ≈ 14,8 %</div></x-corr></x-exo>
"""),

("9-8", "Séries de pertes et risque de ruine", r"""
<x-obj><ul><li>Estimer la probabilité des séries de pertes.</li><li>Comprendre la notion de risque de ruine et les limites de ses formules.</li></ul></x-obj>
<x-simple>
<p>Même avec une stratégie gagnante, les <strong>séries de pertes</strong> sont inévitables. Avec 45 % de réussite, une série de 8 pertes d'affilée paraît improbable… mais sur 200 trades, elle a plus d'une chance sur deux de se produire. Le <strong>risque de ruine</strong> est la probabilité de perdre une part du capital telle qu'on ne peut plus (ou ne veut plus) continuer.</p>
</x-simple>
<x-fig c="Probabilité de vivre au moins une série de k pertes d'affilée, avec 45 % de réussite (trades supposés indépendants).">""" + SCHEMA_SERIES_PROBA + r"""</x-fig>
<x-approfondi>
<p>Une formule classique, valable pour un pari à gain égal à la perte (R = 1) avec une mise fixe en euros, donne : risque de ruine ≈ (q ÷ p)<sup>N</sup>, où p est la probabilité de gain, q celle de perte, et N le nombre de pertes qui épuisent le capital. Elle montre l'idée essentielle : <strong>plus on risque par trade, plus N est petit, et plus la ruine devient probable</strong>.</p>
</x-approfondi>
<x-note><p>Ces formules reposent sur des hypothèses irréalistes : probabilité de gain connue et constante, trades indépendants, gains et pertes de taille fixe. En réalité, les pertes ont tendance à se regrouper (changement de régime de marché, erreurs psychologiques en série) et l'on surestime souvent son taux de réussite. Prenez ces chiffres comme des <strong>ordres de grandeur optimistes</strong>. La simulation (outil Monte-Carlo du site) est plus parlante que la formule.</p></x-note>
<x-exemple>
<div class="calcul">Taux de réussite 45 % (q = 0,55). Au moins une série de 8 pertes :
  sur 100 trades ≈ 30,7 % ; sur 200 trades ≈ 53,0 %
Formule simplifiée (p = 0,55 ; q = 0,45 ; R = 1 ; mise fixe) :
  risque 2 % du capital initial → N = 50 → (0,45 ÷ 0,55)^50 ≈ 0,004 %
  risque 10 %                   → N = 10 → (0,818)^10 ≈ 13,4 %
Simulation (45 % de réussite, R = 1,5, 500 trades, risque composé) :
  probabilité de subir un drawdown d'au moins 30 % ≈ 2 % avec 1 % de risque,
  ≈ 48 % avec 2 %, et quasi certaine avec 5 %</div>
<p>À espérance identique (+0,125R par trade), le simple passage de 1 % à 2 % de risque multiplie par plus de vingt la probabilité d'un drawdown de 30 %.</p>
</x-exemple>
<x-erreurs><ul><li>Croire qu'après 5 pertes, « la prochaine sera forcément gagnante » (erreur du joueur).</li><li>Prendre les formules de risque de ruine pour des garanties.</li><li>Ne pas prévoir de plan pour une série de pertes.</li></ul></x-erreurs>
<x-cles><ul><li>Les longues séries de pertes sont probables sur un grand nombre de trades.</li><li>Le risque de ruine augmente très vite avec le risque par trade.</li><li>Formules = ordres de grandeur optimistes ; préférez la simulation et la prudence.</li></ul></x-cles>
<x-exo><p>Avec 50 % de réussite, quelle est la probabilité que les 6 prochains trades soient tous perdants ? Utilisez le <a href="../outils.html#series">simulateur de séries de pertes</a> pour estimer la probabilité d'au moins une série de 6 pertes sur 100 trades.</p>
<x-corr><div class="calcul">0,5^6 = 1 ÷ 64 ≈ 1,6 % pour 6 trades donnés</div><p>Le simulateur (taux de réussite 50 %, 6 pertes) indique environ 55 % de probabilité d'au moins une telle série sur 100 trades (et environ 98 % sur 500 trades, selon le même calcul). Une série « rare » sur 6 trades donnés devient probable sur une centaine de trades.</p></x-corr></x-exo>
"""),

("9-9", "La corrélation entre positions", r"""
<x-obj><ul><li>Comprendre comment la corrélation augmente le risque réel du compte.</li><li>Calculer le risque combiné de deux positions corrélées.</li></ul></x-obj>
<x-simple>
<p>Deux positions sont <strong>corrélées</strong> si elles ont tendance à évoluer ensemble. Acheter EUR/USD et GBP/USD, ou deux grandes valeurs technologiques, revient souvent à prendre presque deux fois le même pari. Risquer 1 % sur chacune ne fait pas « 1 % de risque » : c'est souvent proche de 2 % sur une seule idée.</p>
</x-simple>
<x-fig c="Risque combiné (en écart-type) de deux positions risquant chacune 1 %, selon leur corrélation : une forte corrélation positive revient presque à doubler la mise.">""" + SCHEMA_CORR + r"""</x-fig>
<x-approfondi>
<div class="formule">Risque combiné ≈ √(r₁² + r₂² + 2 × ρ × r₁ × r₂)</div>
<p>ρ (rhô) est le coefficient de corrélation, entre −1 et +1. Cette formule s'applique à la variabilité (écart-type) des résultats ; si les deux stops sont touchés ensemble, la perte réelle sera bien la somme des deux.</p>
<p>Les corrélations <strong>changent</strong> : en période de crise, de nombreux actifs habituellement peu corrélés se mettent à baisser ensemble (« en crise, toutes les corrélations tendent vers 1 »). Règle pratique : regrouper les positions par « idée » (dollar faible, actions technologiques, pétrole…) et plafonner le risque total par idée, par exemple à 2 %.</p>
</x-approfondi>
<x-exemple>
<p>Deux positions, chacune avec 1 % de risque :</p>
<div class="calcul">Corrélation 0 (indépendantes) : √(1 + 1 + 0) = √2 ≈ 1,41 %
Corrélation 0,8 : √(1 + 1 + 2 × 0,8) = √3,6 ≈ 1,90 %
Corrélation 1 : √4 = 2 %
Corrélation −1 : 0 % (les positions se compensent… ainsi que leurs gains)
Pire cas réel (les deux stops touchés) : 2 % de perte</div>
</x-exemple>
<x-erreurs><ul><li>Ouvrir 5 positions à 1 % sur des actifs très liés et croire risquer « 1 % par trade ».</li><li>Se croire diversifié avec plusieurs paires contenant toutes le dollar dans le même sens.</li><li>Supposer que les corrélations passées resteront stables en crise.</li></ul></x-erreurs>
<x-cles><ul><li>Positions corrélées = risque concentré.</li><li>Risque combiné ≈ √(r₁² + r₂² + 2ρr₁r₂).</li><li>Plafonner le risque total par idée ; les corrélations montent en crise.</li></ul></x-cles>
<x-exo><p>Vous êtes acheteur d'EUR/USD (risque 1 %) et vendeur d'USD/CHF (risque 1 %). Ces deux positions sont-elles indépendantes ? Expliquez.</p>
<x-corr><p>Non. Les deux paris reviennent à <strong>vendre le dollar</strong> : acheter EUR/USD gagne si le dollar baisse face à l'euro ; vendre USD/CHF gagne si le dollar baisse face au franc. Historiquement, ces deux positions sont fortement corrélées positivement. Le risque réel est proche de 2 % sur une seule idée (« dollar faible »).</p></x-corr></x-exo>
"""),

("9-10", "Les règles de protection du compte", r"""
<x-obj><ul><li>Définir des limites de perte journalière, hebdomadaire et mensuelle.</li><li>Mettre en place un plan de réduction du risque en drawdown.</li></ul></x-obj>
<x-simple>
<p>Les règles de protection sont des « disjoncteurs » décidés <strong>à froid</strong>, qui s'appliquent automatiquement quand la situation se dégrade : on arrête de trader pour la journée, la semaine ou le mois, ou on réduit la taille. Elles protègent surtout contre soi-même (revanche, surtrading : module 11).</p>
</x-simple>
<x-approfondi>
""" + table(["Règle", "Exemple de seuil (à adapter)", "Action"],
            [["Perte journalière maximale", "2 % ou 3R", "Arrêt jusqu'au lendemain"], ["Perte hebdomadaire maximale", "5 %", "Arrêt jusqu'à la semaine suivante, revue du journal"],
             ["Drawdown depuis le plus haut", "10 %", "Risque par trade divisé par 2"], ["Drawdown depuis le plus haut", "15 à 20 %", "Arrêt du trading réel, retour en démo, révision complète"],
             ["Exposition totale", "Ex. 5 % de risque cumulé ouvert", "Pas de nouvelle position"], ["Risque par idée corrélée", "Ex. 2 %", "Pas de position supplémentaire sur la même idée"]]) + r"""
<p>Ces seuils sont des exemples, pas des normes. L'essentiel est de les <strong>écrire</strong> avant de commencer, de les respecter sans exception, et de les vérifier dans le journal.</p>
</x-approfondi>
<x-exemple>
<p>Capital 10 000 €, risque 1 % par trade, limite journalière 2 %, réduction de moitié du risque à −10 % de drawdown.</p>
<div class="calcul">Limite journalière = 200 € → au plus 2 pertes pleines par jour, puis arrêt
Après un drawdown de 10 % (capital 9 000 €) : risque = 0,5 % × 9 000 = 45 € par trade
  (au lieu de 1 % × 9 000 = 90 €)
Pour revenir à 10 000 € (+11,1 %), il faut alors environ 1 000 ÷ 45 ≈ 22 R de gains nets :
c'est plus lent, mais une nouvelle série de pertes coûtera deux fois moins cher.</div>
</x-exemple>
<x-erreurs><ul><li>Fixer des limites… et les ignorer « juste cette fois ».</li><li>Fixer des limites après une perte, sous le coup de l'émotion.</li><li>Ne prévoir que des limites de perte et aucune règle sur l'exposition totale.</li></ul></x-erreurs>
<x-cles><ul><li>Limites journalières, hebdomadaires, de drawdown : des disjoncteurs écrits à l'avance.</li><li>Réduire la taille en drawdown, plafonner l'exposition totale.</li><li>Une règle non respectée n'est pas une règle.</li></ul></x-cles>
<x-exo><p>Rédigez vos propres règles de protection pour un compte de 5 000 € avec 1 % de risque par trade : limite journalière, limite hebdomadaire, seuil de réduction du risque, seuil d'arrêt.</p>
<x-corr><p>Exemple : « Risque 1 % = 50 €. Limite journalière : 100 € (2 pertes). Limite hebdomadaire : 250 € (5 %). À −10 % depuis le plus haut (4 500 € si le pic est 5 000 €), risque à 0,5 %. À −20 %, arrêt du réel, deux semaines de revue et de démo. Jamais plus de 3 % de risque ouvert en même temps. » Ce qui compte, c'est que ce soit écrit, chiffré et appliqué.</p></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Asymétrie</h2><ul><li>Gain pour revenir = perte ÷ (1 − perte).</li><li>−20 % → +25 % ; −50 % → +100 %.</li></ul></div>
<div class="encadre"><h2>Risque par trade</h2><ul><li>0,5 à 2 % du capital (convention prudente).</li><li>Risque ≠ montant investi.</li><li>Kelly : f = p − q ÷ R (théorique, trop agressif en pratique).</li></ul></div>
<div class="encadre"><h2>Taille de position</h2><ul><li>Taille = risque € ÷ (distance au stop × valeur unitaire).</li><li>Arrondir vers le bas.</li><li>Taille minimale trop grosse → pas de trade.</li></ul></div>
<div class="encadre"><h2>Stops &amp; objectifs</h2><ul><li>Stop = invalidation : structure, ATR, temps.</li><li>Objectif : niveau, multiple de R, partiel, trailing.</li><li>Jamais éloigner un stop.</li></ul></div>
<div class="encadre"><h2>R/R &amp; espérance</h2><ul><li>R = gain visé ÷ risque.</li><li>Seuil de réussite = 1 ÷ (1 + R).</li><li>E = p × G − (1 − p) × P, après frais.</li></ul></div>
<div class="encadre"><h2>Drawdown</h2><ul><li>DD = (pic − valeur) ÷ pic.</li><li>Récupération = pic ÷ creux − 1.</li><li>S'attendre à pire qu'en backtest.</li></ul></div>
<div class="encadre"><h2>Séries &amp; ruine</h2><ul><li>45 % de réussite : ≈ 53 % de chances d'au moins 8 pertes d'affilée en 200 trades.</li><li>Ruine ≈ (q ÷ p)<sup>N</sup> (hypothèses irréalistes).</li><li>Risque par trade ↑ ⇒ ruine ↑ très vite.</li></ul></div>
<div class="encadre"><h2>Corrélation &amp; protection</h2><ul><li>Risque combiné ≈ √(r₁² + r₂² + 2ρr₁r₂).</li><li>Plafond par idée ; corrélations ↑ en crise.</li><li>Limites jour / semaine / drawdown, écrites à l'avance.</li></ul></div>
"""

QUIZ = [
("Après une perte de 40 %, quel gain faut-il pour revenir au capital initial ?", ["40 %", "50 %", "66,7 %", "80 %"], 2, "0,40 ÷ 0,60 ≈ 66,7 %."),
("Capital 8 000 €, risque 1,5 %. Montant risqué par trade ?", ["15 €", "80 €", "120 €", "1 200 €"], 2, "8 000 × 1,5 % = 120 €."),
("Risque 150 €, entrée 30 €, stop 28,50 €. Combien d'actions ?", ["50", "100", "150", "200"], 1, "Distance = 1,50 € ; 150 ÷ 1,50 = 100 actions."),
("Risque 100 €, stop à 40 pips, pip à 9 € par lot. Taille en lots (arrondie vers le bas à 0,01) ?", ["0,25", "0,27", "0,28", "2,7"], 1, "100 ÷ (40 × 9) = 100 ÷ 360 = 0,277 → 0,27 lot."),
("Où doit se trouver le stop loss ?", ["À un montant rond que l'on accepte de perdre", "Au niveau où l'hypothèse du trade est invalidée", "Toujours à 1 % sous l'entrée", "Il n'en faut pas si l'on surveille"], 1, "Le stop est un niveau de marché ; la taille de position s'adapte ensuite."),
("Ratio 1:4. Taux de réussite minimal sans frais ?", ["20 %", "25 %", "40 %", "80 %"], 0, "1 ÷ (1 + 4) = 20 %."),
("45 % de réussite, gain moyen 1,8R, perte moyenne 1R. Espérance ?", ["−0,04 R", "+0,26 R", "+0,81 R", "+0,45 R"], 1, "0,45 × 1,8 − 0,55 × 1 = 0,81 − 0,55 = +0,26 R."),
("Pic 20 000 €, creux 15 000 €. Drawdown ?", ["15 %", "20 %", "25 %", "33 %"], 2, "(20 000 − 15 000) ÷ 20 000 = 25 %."),
("Dans l'exemple précédent, quel gain faut-il depuis le creux pour revenir au pic ?", ["25 %", "30 %", "33,3 %", "50 %"], 2, "20 000 ÷ 15 000 − 1 ≈ 33,3 %."),
("Avec 50 % de réussite, probabilité que les 5 prochains trades soient perdants ?", ["50 %", "10 %", "3,125 %", "0,5 %"], 2, "0,5^5 = 1 ÷ 32 ≈ 3,125 % ; mais sur 100 trades, une telle série est très probable."),
("Que se passe-t-il quand on double le risque par trade, à espérance égale ?", ["Le risque de grosse perte augmente beaucoup plus que proportionnellement", "Le risque de ruine est divisé par deux", "L'espérance en R double", "Rien"], 0, "Moins de pertes suffisent à épuiser le capital : la probabilité de drawdown sévère augmente très vite."),
("Deux positions à 1 % de risque, corrélation 0,8. Risque combiné (écart-type) ?", ["1 %", "1,41 %", "1,90 %", "2,8 %"], 2, "√(1 + 1 + 2 × 0,8) = √3,6 ≈ 1,90 %."),
("Acheter EUR/USD et vendre USD/CHF revient surtout à :", ["Se couvrir", "Parier deux fois contre le dollar", "Être neutre", "Parier sur le franc suisse uniquement"], 1, "Les deux positions gagnent si le dollar baisse : risque concentré."),
("Après 10 % de drawdown, une règle de protection prudente consiste à :", ["Doubler le risque pour se refaire", "Réduire le risque par trade", "Supprimer les stops", "Ouvrir plus de positions"], 1, "Réduire la taille limite les dégâts si la série de pertes continue."),
("Kelly avec p = 0,5 et R = 2 donne :", ["10 %", "25 %", "50 %", "0 %"], 1, "f = 0,5 − 0,5 ÷ 2 = 0,25, soit 25 % : bien trop agressif en pratique, d'où l'usage de petites fractions."),
]
