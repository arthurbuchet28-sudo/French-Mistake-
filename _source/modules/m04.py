import random
from svgkit import plot, table, svg, t, line, arrow, path_from, candles

NUM = 4
TITRE = "Analyse technique : les bases"
RESUME = "Lire un graphique : chandeliers, unités de temps, tendances, supports et résistances, lignes de tendance, canaux et volumes."
DUREE = "2 h 30"
INTRO = r"""<p>L'<strong>analyse technique</strong> étudie l'historique des prix et des volumes pour repérer des situations où une hypothèse de trading a un intérêt. Ce module pose les bases indispensables : savoir lire un graphique, reconnaître une tendance, tracer des niveaux. Il commence par une question honnête : est-ce que ça marche ?</p>"""


def _marche_aleatoire():
    rnd = random.Random(11)
    x, p = [0], [100]
    for i in range(1, 250):
        p.append(p[-1] * (1 + rnd.gauss(0, 0.012)))
        x.append(i)
    return plot([{"x": x, "y": p, "cls": "g-l1", "label": "Prix simulé par tirage au sort (marche aléatoire)"}],
                label="Une marche aléatoire produit des « tendances » et des « niveaux » trompeurs",
                xlabel="Jours", yfmt=lambda v: f"{v:.0f}")


SCHEMA_ALEA = _marche_aleatoire()


def _anatomie():
    W = 640
    p = []
    # bougie haussière
    p += [line(150, 30, 150, 220, "g-haus g-meche"), f'<rect x="120" y="70" width="60" height="110" class="g-haus"/>']
    p += [t(150, 18, "Bougie haussière", "g-txt g-fort", "middle")]
    for y, lab in [(30, "Plus haut (High)"), (70, "Clôture (Close)"), (180, "Ouverture (Open)"), (220, "Plus bas (Low)")]:
        p.append(line(185, y, 215, y, "g-axe"))
        p.append(t(220, y + 4, lab, "g-txt"))
    p.append(t(95, 50, "Mèche haute", "g-txt g-petit", "end"))
    p.append(t(95, 128, "Corps", "g-txt g-petit", "end"))
    p.append(t(95, 203, "Mèche basse", "g-txt g-petit", "end"))
    # bougie baissière
    p += [line(470, 30, 470, 220, "g-bais g-meche"), f'<rect x="440" y="70" width="60" height="110" class="g-bais"/>']
    p += [t(470, 18, "Bougie baissière", "g-txt g-fort", "middle")]
    for y, lab in [(30, "Plus haut"), (70, "Ouverture"), (180, "Clôture"), (220, "Plus bas")]:
        p.append(line(505, y, 525, y, "g-axe"))
        p.append(t(530, y + 4, lab, "g-txt"))
    return svg(W, 236, "".join(p), "Anatomie d'un chandelier japonais")


SCHEMA_ANATOMIE = _anatomie()

_D = path_from([(0, 50), (8, 54), (14, 52), (22, 57)], seed=21, noise=0.7, wick=0.6)
SCHEMA_TYPES = ('<div class="duo">' +
                candles(_D, w=420, h=200, style="ligne", label="Graphique en ligne") +
                candles(_D, w=420, h=200, style="barres", label="Graphique en barres OHLC") + '</div>' +
                candles(_D, w=640, h=220, label="Graphique en chandeliers"))


def _agreger(d, n):
    out = []
    for k in range(0, len(d) - n + 1, n):
        g = d[k:k + n]
        out.append((g[0][0], max(c[1] for c in g), min(c[2] for c in g), g[-1][3]))
    return out


_UT = path_from([(0, 100), (15, 108), (25, 104), (40, 114), (50, 110), (60, 118)], seed=31, noise=0.8, wick=0.5)
SCHEMA_UT = ('<div class="duo">' + candles(_UT, w=420, h=220, label="Unité de temps courte : 60 bougies") +
             candles(_agreger(_UT, 5), w=420, h=220, label="Même période en unité de temps 5 fois plus longue : 12 bougies") + '</div>')

_T = path_from([(0, 100), (6, 106), (10, 103), (16, 110), (20, 107), (27, 115), (31, 111.5), (38, 119)], seed=41, noise=0.5, wick=0.5)
SCHEMA_TENDANCE = candles(_T, label="Tendance haussière : sommets et creux de plus en plus hauts",
                          marks=[{"i": 6, "p": _T[6][1], "t": "SH"}, {"i": 10, "p": _T[10][2], "t": "CH", "pos": "bas"},
                                 {"i": 16, "p": _T[16][1], "t": "SH"}, {"i": 20, "p": _T[20][2], "t": "CH", "pos": "bas"},
                                 {"i": 27, "p": _T[27][1], "t": "SH"}, {"i": 31, "p": _T[31][2], "t": "CH", "pos": "bas"}])

_SR = path_from([(0, 104), (5, 99), (10, 105.5), (15, 99.2), (20, 105.8), (25, 99), (31, 106), (35, 110), (39, 106.6), (45, 113)], seed=51, noise=0.5, wick=0.5)
SCHEMA_SR = candles(_SR, label="Support, résistance et inversion des rôles",
                    zones=[{"y1": 98.4, "y2": 99.4, "cls": "g-zone-sup", "label": "Zone de support"},
                           {"y1": 105.6, "y2": 106.6, "cls": "g-zone-res", "label": "Résistance… puis support"}],
                    marks=[{"i": 39, "p": _SR[39][2], "t": "Retour sur l'ancienne résistance", "pos": "bas", "anchor": "start"}])

_CH = path_from([(0, 100), (5, 105), (9, 102), (14, 108), (18, 105), (23, 111), (27, 108), (32, 114), (36, 111), (40, 115)], seed=61, noise=0.4, wick=0.4)
SCHEMA_CANAL = candles(_CH, label="Canal haussier : ligne de tendance et ligne parallèle",
                       lines=[{"p1": (9, 101.2), "p2": (18, 104.2), "ext": 40, "cls": "g-sup"},
                              {"p1": (5, 106.0), "p2": (14, 109.0), "ext": 40, "cls": "g-res"}],
                       legend=[("g-sup", "Ligne de tendance (relie les creux)"), ("g-res", "Parallèle (haut du canal)")])

_V = path_from([(0, 50), (6, 52), (12, 50.4), (18, 52.2), (24, 50.6), (28, 51.8), (30, 54.5), (36, 56)], seed=71, noise=0.35, wick=0.3)
_vol = [1.2 + random.Random(i).uniform(-0.3, 0.3) for i in range(len(_V))]
_vol[29], _vol[30], _vol[31] = 2.1, 3.1, 2.4
SCHEMA_VOLUME = candles(_V, h=300, vol=_vol, label="Cassure de résistance accompagnée d'un fort volume",
                        lines=[{"y": 52.6, "cls": "g-res", "label": "Résistance 52,60", "i2": 29}],
                        marks=[{"i": 30, "p": _V[30][1], "t": "Cassure : volume ≈ 2,6 × la moyenne", "anchor": "end"}])

LECONS = [
("4-1", "Les principes de l'analyse technique et leurs limites", r"""
<x-obj><ul><li>Connaître les hypothèses sur lesquelles repose l'analyse technique.</li><li>Comprendre le débat sur son efficacité.</li><li>Se méfier des motifs qui apparaissent par hasard.</li></ul></x-obj>
<x-simple>
<p>L'analyse technique repose sur trois idées héritées notamment de Charles Dow (fin du XIX<sup>e</sup> siècle) :</p>
<ol><li><strong>Le prix intègre l'information disponible</strong> : inutile de tout analyser, le graphique reflète déjà les anticipations.</li>
<li><strong>Les prix évoluent en tendances</strong>, qui ont tendance à se prolonger plutôt qu'à s'inverser.</li>
<li><strong>Les comportements se répètent</strong> : peur et avidité produisent des configurations récurrentes.</li></ol>
<p>En pratique, l'analyse technique sert surtout à <strong>structurer des décisions</strong> : où entrer, où placer un stop, où prendre un bénéfice. Elle ne prédit pas l'avenir.</p>
</x-simple>
<x-note>
<p><strong>Son efficacité est débattue.</strong></p>
<ul><li>L'<strong>hypothèse d'efficience des marchés</strong> (Eugene Fama) soutient que les prix passés ne permettent pas de battre durablement le marché une fois les frais déduits. De nombreuses règles techniques simples, testées rigoureusement, ne survivent pas aux coûts de transaction.</li>
<li>À l'inverse, certains phénomènes sont bien documentés dans la recherche académique, comme l'effet <strong>momentum</strong> (les actifs qui ont le plus monté sur 3 à 12 mois ont eu tendance à continuer à surperformer, Jegadeesh et Titman, 1993) et le suivi de tendance sur longue période dans les contrats à terme. Leur intensité varie beaucoup selon les périodes.</li>
<li>Une partie de l'effet de certains niveaux viendrait du fait que beaucoup d'intervenants les regardent (effet <strong>autoréalisateur</strong>), ce qui est fragile.</li></ul>
<p>Position de cette formation : l'analyse technique est un <strong>cadre utile pour gérer le risque et formuler des hypothèses testables</strong>. Ce n'est pas une boule de cristal. Toute règle doit être testée (module 10).</p>
</x-note>
<x-approfondi>
<p>Le cerveau humain voit des motifs partout, même dans le hasard (c'est l'<strong>apophénie</strong>). Un prix tiré au sort produit des « tendances », des « supports » et des « figures » parfaitement convaincants. C'est un excellent exercice d'humilité : avant de croire qu'une configuration « marche », demandez-vous si elle apparaîtrait aussi dans une série aléatoire.</p>
</x-approfondi>
<x-fig c="Cette courbe est entièrement générée par tirage au sort (variations journalières aléatoires d'environ 1,2 %). On croit pourtant y voir des tendances et des niveaux.">""" + SCHEMA_ALEA + r"""</x-fig>
<x-exemple>
<p>Vous testez <strong>100 règles de trading différentes</strong> sur un historique, et vous retenez celles dont le résultat est « statistiquement significatif » au seuil de 5 %. Supposons qu'aucune règle n'ait en réalité le moindre pouvoir prédictif.</p>
<div class="calcul">Nombre de « fausses découvertes » attendues = 100 × 5 % = 5 règles
Probabilité qu'au moins une règle paraisse significative par hasard = 1 − 0,95^100 ≈ 99,4 %</div>
<p>En testant suffisamment d'idées, on trouve presque toujours une règle « gagnante » sur le passé, sans qu'elle ait la moindre valeur. C'est le <strong>surapprentissage</strong>, étudié au module 10.</p>
</x-exemple>
<x-erreurs><ul><li>Croire qu'une figure « doit » produire le mouvement annoncé.</li><li>Chercher des confirmations sur un graphique après avoir décidé d'acheter (biais de confirmation).</li><li>Rejeter en bloc l'analyse technique, ou au contraire lui attribuer des pouvoirs prédictifs.</li></ul></x-erreurs>
<x-cles><ul><li>Hypothèses : le prix intègre l'information, les tendances persistent, les comportements se répètent.</li><li>Efficacité débattue : certaines règles résistent aux tests, beaucoup non.</li><li>Le hasard produit des motifs convaincants : tester avant de croire.</li></ul></x-cles>
<x-exo><p>Un forum annonce : « J'ai testé 40 configurations, et 3 battent le marché sur 5 ans ». Au seuil de 5 %, combien de configurations auraient paru gagnantes par pur hasard, en moyenne ? Que faudrait-il faire pour valider ces 3 configurations ?</p>
<x-corr><div class="calcul">40 × 5 % = 2 configurations attendues par hasard</div><p>Trouver 3 « gagnantes » sur 40 est donc proche de ce que donnerait le hasard. Pour les valider, il faut les tester sur des <strong>données qu'on n'a pas utilisées</strong> pour les choisir (autre période, autres marchés : test hors échantillon), frais compris, puis en conditions réelles de démonstration (forward test, module 10).</p></x-corr></x-exo>
"""),

("4-2", "Les types de graphiques et le chandelier japonais", r"""
<x-obj><ul><li>Lire un graphique en ligne, en barres et en chandeliers.</li><li>Construire un chandelier à partir des prix OHLC.</li></ul></x-obj>
<x-simple>
<p>Chaque période (une minute, une heure, un jour…) est résumée par quatre prix : <strong>ouverture</strong> (Open), <strong>plus haut</strong> (High), <strong>plus bas</strong> (Low), <strong>clôture</strong> (Close), d'où le sigle <strong>OHLC</strong>.</p>
<ul><li>Le <strong>graphique en ligne</strong> relie les seuls cours de clôture : simple et lisible, mais il perd l'information sur l'amplitude.</li>
<li>Le <strong>graphique en barres</strong> montre les quatre prix : un trait vertical du plus bas au plus haut, un petit tiret à gauche pour l'ouverture, à droite pour la clôture.</li>
<li>Le <strong>chandelier japonais</strong> montre les mêmes informations de façon plus visuelle : un <strong>corps</strong> entre ouverture et clôture (vert ou blanc si la clôture est plus haute, rouge ou noir sinon) et des <strong>mèches</strong> jusqu'aux extrêmes.</li></ul>
</x-simple>
<x-fig c="Anatomie d'un chandelier. Les couleurs varient selon les plateformes (souvent vert/rouge, ou blanc/noir).">""" + SCHEMA_ANATOMIE + r"""</x-fig>
<x-fig c="Les mêmes données en ligne, en barres et en chandeliers.">""" + SCHEMA_TYPES + r"""</x-fig>
<x-approfondi>
<p>Un chandelier se lit comme le résumé d'un combat : un grand corps vert indique que les acheteurs ont dominé de l'ouverture à la clôture ; une longue mèche basse indique que les vendeurs ont fait baisser le prix, mais que les acheteurs l'ont ramené vers le haut avant la clôture. Ce n'est qu'un résumé : deux séances très différentes peuvent produire la même bougie.</p>
<p>Il existe d'autres représentations (Heikin-Ashi, Renko, Point &amp; Figure) qui lissent ou filtrent les prix. Attention : certaines, comme le Heikin-Ashi, n'affichent <em>pas</em> les vrais prix d'ouverture et de clôture.</p>
</x-approfondi>
<x-exemple>
<p>Construisons la bougie <strong>journalière</strong> à partir de quatre bougies de deux heures :</p>
""" + table(["Bougie", "Ouverture", "Plus haut", "Plus bas", "Clôture"],
            [["9 h – 11 h", "50,00", "51,50", "49,80", "51,00"], ["11 h – 13 h", "51,00", "51,20", "50,10", "50,40"],
             ["13 h – 15 h", "50,40", "52,30", "50,30", "52,10"], ["15 h – 17 h", "52,10", "52,60", "51,40", "51,70"]]) + r"""
<div class="calcul">Ouverture = ouverture de la première bougie = 50,00
Plus haut = maximum des plus hauts = max(51,50 ; 51,20 ; 52,30 ; 52,60) = 52,60
Plus bas = minimum des plus bas = min(49,80 ; 50,10 ; 50,30 ; 51,40) = 49,80
Clôture = clôture de la dernière bougie = 51,70
Corps = 51,70 − 50,00 = 1,70 (haussier) ; mèche haute = 52,60 − 51,70 = 0,90 ; mèche basse = 50,00 − 49,80 = 0,20</div>
</x-exemple>
<x-erreurs><ul><li>Confondre la couleur d'une bougie (ouverture vs clôture de la période) avec la variation par rapport à la veille : une bougie peut être verte alors que le prix a baissé depuis la veille (ouverture en gap baissier, puis légère remontée).</li><li>Analyser une bougie qui n'est pas encore clôturée.</li></ul></x-erreurs>
<x-cles><ul><li>OHLC : ouverture, plus haut, plus bas, clôture.</li><li>Corps = de l'ouverture à la clôture ; mèches = extrêmes.</li><li>Agréger des bougies : 1<sup>re</sup> ouverture, max des hauts, min des bas, dernière clôture.</li></ul></x-cles>
<x-exo><p>Une bougie a ouvert à 120, est montée à 124, descendue à 113 et a clôturé à 115. Est-elle haussière ou baissière ? Calculez le corps et les deux mèches.</p>
<x-corr><div class="calcul">Clôture (115) &lt; ouverture (120) → bougie baissière
Corps = 120 − 115 = 5
Mèche haute = 124 − 120 = 4
Mèche basse = 115 − 113 = 2</div></x-corr></x-exo>
"""),

("4-3", "Les unités de temps et l'analyse multi-unités", r"""
<x-obj><ul><li>Choisir une unité de temps cohérente avec son style.</li><li>Combiner plusieurs unités de temps sans se contredire.</li><li>Comprendre l'effet de l'unité de temps sur la taille du stop et de la position.</li></ul></x-obj>
<x-simple>
<p>L'<strong>unité de temps</strong> (timeframe) est la durée représentée par chaque bougie : 1 minute (M1), 5 minutes (M5), 1 heure (H1), 4 heures (H4), 1 jour (D1), 1 semaine (W1)… Le même marché peut être haussier en hebdomadaire et baissier en horaire : les deux sont vrais à leur échelle.</p>
</x-simple>
<x-fig c="Mêmes prix, deux unités de temps : l'unité plus longue gomme les petits mouvements et fait mieux apparaître la tendance de fond.">""" + SCHEMA_UT + r"""</x-fig>
<x-approfondi>
<p>L'<strong>analyse multi-unités de temps</strong> consiste à :</p>
<ol><li>définir le <strong>contexte</strong> sur une unité longue (tendance, grands niveaux) ;</li>
<li>chercher un <strong>signal</strong> sur l'unité de travail ;</li>
<li>éventuellement affiner l'<strong>entrée</strong> sur une unité plus courte.</li></ol>
<p>Une convention répandue (popularisée par Alexander Elder) est un rapport de 4 à 6 entre les unités : hebdomadaire / journalier / 4 heures, ou journalier / 4 heures / 1 heure. C'est un repère pratique, pas une règle démontrée.</p>
<p>Plus l'unité de temps est courte, plus il y a de « bruit » (mouvements aléatoires), plus les trades sont nombreux, et plus les frais pèsent par rapport aux gains visés.</p>
</x-approfondi>
<x-exemple>
<p>Vous risquez 100 € par trade sur une action. L'amplitude moyenne d'une bougie (ATR, module 6) est de 2,00 € en journalier et de 0,50 € en horaire. Vous placez votre stop à 1 ATR.</p>
<div class="calcul">En journalier : stop à 2,00 € → taille = 100 ÷ 2,00 = 50 actions
En horaire   : stop à 0,50 € → taille = 100 ÷ 0,50 = 200 actions
Le risque en euros est le même (100 €), mais en horaire la position est 4 fois plus grosse.
Avec un spread de 0,04 € : coût = 50 × 0,04 = 2 € (2 % du risque) en journalier,
200 × 0,04 = 8 € (8 % du risque) en horaire.</div>
<p>Les frais pèsent bien plus lourd sur les petites unités de temps : c'est une raison majeure de la difficulté du trading très court terme.</p>
</x-exemple>
<x-erreurs><ul><li>Changer d'unité de temps en cours de trade pour justifier de garder une position perdante (« en hebdomadaire, c'est toujours haussier »).</li><li>Regarder trop d'unités de temps et ne plus jamais trouver de signal cohérent.</li><li>Commencer par les unités très courtes (M1, M5) : c'est là que le bruit et les frais sont les plus forts.</li></ul></x-erreurs>
<x-cles><ul><li>Chaque unité de temps a sa propre tendance.</li><li>Contexte sur l'unité longue, signal sur l'unité de travail.</li><li>Unité courte = plus de bruit, plus de trades, plus de frais relatifs.</li></ul></x-cles>
<x-exo><p>Vous tradez en H4. Quelles unités de temps choisiriez-vous pour le contexte et pour affiner l'entrée, avec un rapport d'environ 4 à 6 ? Combien de bougies H4 compte une semaine de Forex (5 jours de 24 h) ?</p>
<x-corr><p>Contexte : <strong>journalier</strong> (rapport 6). Affinage : <strong>H1</strong> (rapport 4).</p><div class="calcul">Bougies H4 par semaine = 5 × 24 ÷ 4 = 30</div></x-corr></x-exo>
"""),

("4-4", "La tendance et la structure de marché", r"""
<x-obj><ul><li>Identifier une tendance haussière, baissière ou un marché sans tendance.</li><li>Repérer une rupture de structure.</li></ul></x-obj>
<x-simple>
<ul><li><strong>Tendance haussière</strong> : une succession de <strong>sommets plus hauts</strong> (SH) et de <strong>creux plus hauts</strong> (CH).</li>
<li><strong>Tendance baissière</strong> : des sommets plus bas et des creux plus bas.</li>
<li><strong>Range</strong> (marché sans tendance, ou latéral) : les prix oscillent entre deux niveaux sans direction claire.</li></ul>
<p>Le dicton « la tendance est votre amie » résume l'idée : il est souvent plus simple de trader dans le sens de la tendance dominante.</p>
</x-simple>
<x-fig c="Tendance haussière : chaque creux (CH) est plus haut que le précédent, chaque sommet (SH) aussi.">""" + SCHEMA_TENDANCE + r"""</x-fig>
<x-approfondi>
<p>Une tendance alterne des <strong>impulsions</strong> (mouvements dans le sens de la tendance) et des <strong>corrections</strong> ou <strong>pullbacks</strong> (replis temporaires). Les entrées « sur pullback » cherchent à acheter un repli dans une tendance haussière, avec un stop sous le dernier creux.</p>
<p>Une tendance haussière est remise en cause quand le prix casse le dernier creux significatif : on parle de <strong>rupture de structure</strong>. Ce n'est pas forcément un retournement : le marché peut passer en range.</p>
<p>Le choix des points « significatifs » reste subjectif : selon l'unité de temps et la sensibilité de l'œil, deux analystes ne marqueront pas les mêmes sommets. Pour être objectif, on peut définir un sommet de façon mécanique (par exemple : un plus haut supérieur aux 2 bougies avant et aux 2 bougies après).</p>
</x-approfondi>
<x-exemple>
<p>Succession de points hauts et bas d'un marché (dans l'ordre) : creux 100 → sommet 106 → creux 103 → sommet 110 → creux 107 → sommet 115 → creux 111,5 → sommet 119.</p>
<div class="calcul">Sommets : 106 &lt; 110 &lt; 115 &lt; 119 → sommets de plus en plus hauts ✔
Creux  : 100 &lt; 103 &lt; 107 &lt; 111,5 → creux de plus en plus hauts ✔
Conclusion : tendance haussière.
Taille des impulsions : 6 ; 7 ; 8 ; 7,5 points. Des corrections : 3 ; 3 ; 3,5 points.
Rupture de structure si le prix repasse sous le dernier creux : 111,5.</div>
</x-exemple>
<x-erreurs><ul><li>Voir une tendance après deux bougies.</li><li>Acheter un « creux » dans une tendance baissière en pensant qu'elle va se retourner (« attraper un couteau qui tombe »).</li><li>Confondre un pullback normal avec un retournement et sortir trop tôt, ou l'inverse.</li></ul></x-erreurs>
<x-cles><ul><li>Hausse : sommets et creux plus hauts. Baisse : sommets et creux plus bas. Sinon : range.</li><li>Une tendance alterne impulsions et corrections.</li><li>Cassure du dernier creux (ou sommet) significatif = rupture de structure.</li></ul></x-cles>
<x-exo><p>Points successifs : sommet 80 → creux 74 → sommet 77 → creux 70 → sommet 75 → creux 71 → sommet 78. Quelle est la structure ? Que s'est-il passé au dernier point ?</p>
<x-corr><p>Sommets : 80 → 77 → 75 (de plus en plus bas), creux : 74 → 70 (plus bas) : <strong>tendance baissière</strong>. Puis le creux à 71 est plus haut que 70, et le sommet à 78 dépasse le dernier sommet (75) : c'est une <strong>rupture de structure baissière</strong>. La tendance baissière est remise en cause, sans qu'une tendance haussière soit encore établie (il faudrait un nouveau creux plus haut que 71).</p></x-corr></x-exo>
"""),

("4-5", "Supports et résistances", r"""
<x-obj><ul><li>Tracer des zones de support et de résistance.</li><li>Comprendre l'inversion des rôles.</li><li>Placer un stop en tenant compte d'une zone.</li></ul></x-obj>
<x-simple>
<p>Un <strong>support</strong> est une zone de prix où la baisse s'est arrêtée plusieurs fois, parce que des acheteurs y sont apparus. Une <strong>résistance</strong> est une zone où la hausse s'est arrêtée, parce que des vendeurs y sont apparus. Plus une zone a été testée, plus elle est visible… et plus elle attire l'attention.</p>
</x-simple>
<x-fig c="Le prix rebondit plusieurs fois sur le support, finit par casser la résistance, puis revient la tester par le dessus : elle sert alors de support.">""" + SCHEMA_SR + r"""</x-fig>
<x-approfondi>
<p>Où trouver des supports et des résistances : anciens plus hauts et plus bas, zones de consolidation, chiffres ronds (100 €, 1,1000 sur EUR/USD), plus hauts et plus bas de la veille ou de la semaine, gaps.</p>
<p><strong>Ce sont des zones, pas des lignes</strong> : les prix dépassent souvent un niveau de quelques centimes avant de repartir. Tracez une bande qui englobe les mèches.</p>
<p><strong>Inversion des rôles</strong> : une résistance cassée devient souvent un support (et inversement). Ce sont les mêmes intervenants qui se souviennent de ce prix : ceux qui ont acheté au niveau de la cassure le défendent.</p>
<p>Une cassure peut être <strong>fausse</strong> : le prix dépasse le niveau, déclenche des ordres, puis revient brutalement. Beaucoup de traders attendent une clôture au-delà du niveau, ou un retour sur le niveau, avant d'agir.</p>
</x-approfondi>
<x-exemple>
<p>Trois creux récents sur une action : 98,60 €, 99,10 € et 98,80 €. L'ATR est de 1,20 €. Vous achetez à 101,00 € sur un rebond, en plaçant votre stop sous la zone avec une marge d'une demi-ATR.</p>
<div class="calcul">Zone de support = du plus bas (98,60) au plus haut des creux (99,10)
Marge = 0,5 × 1,20 = 0,60 €
Stop = 98,60 − 0,60 = 98,00 €
Distance au stop = 101,00 − 98,00 = 3,00 €
Pour un risque de 150 € : taille = 150 ÷ 3,00 = 50 actions</div>
<p>Un stop placé juste à 98,59 € aurait été plus serré, mais exposé au moindre dépassement de la zone.</p>
</x-exemple>
<x-erreurs><ul><li>Tracer des niveaux partout : si tout est un support, rien ne l'est.</li><li>Placer son stop exactement sur le niveau, là où beaucoup d'autres stops sont regroupés.</li><li>Acheter dès le premier contact avec une résistance cassée, sans confirmation.</li></ul></x-erreurs>
<x-cles><ul><li>Support = zone où la baisse s'arrête ; résistance = zone où la hausse s'arrête.</li><li>Ce sont des zones, pas des lignes précises.</li><li>Une résistance cassée devient souvent un support (et inversement).</li></ul></x-cles>
<x-exo><p>Vous voulez vendre à découvert sous une résistance. Sommets récents : 54,20 €, 54,60 €, 54,35 €. ATR = 0,80 €. Vous vendez à 53,00 €. Où placez-vous le stop (marge d'une demi-ATR) ? Combien d'actions pour risquer 120 € ?</p>
<x-corr><div class="calcul">Zone de résistance : 54,20 à 54,60 €
Stop = 54,60 + 0,5 × 0,80 = 55,00 €
Distance = 55,00 − 53,00 = 2,00 €
Taille = 120 ÷ 2,00 = 60 actions</div></x-corr></x-exo>
"""),

("4-6", "Lignes de tendance et canaux", r"""
<x-obj><ul><li>Tracer une ligne de tendance et un canal.</li><li>Calculer la pente d'une ligne et projeter sa valeur future.</li></ul></x-obj>
<x-simple>
<p>Une <strong>ligne de tendance haussière</strong> relie au moins deux creux successifs ; elle est considérée comme validée au troisième contact. Une ligne baissière relie des sommets. Un <strong>canal</strong> est formé par une ligne de tendance et une parallèle passant par les extrêmes opposés : le prix évolue alors dans un « couloir ».</p>
</x-simple>
<x-fig c="Canal haussier : la ligne de tendance relie les creux, la parallèle passe par les sommets.">""" + SCHEMA_CANAL + r"""</x-fig>
<x-approfondi>
<p>Règles de tracé courantes : relier les creux (ou les sommets) en touchant les mèches ou les corps, mais rester cohérent ; ne pas « forcer » la ligne en coupant des bougies. Plus la ligne est pentue, moins elle est durable. Une cassure de ligne de tendance n'est pas un retournement en soi : elle signale un ralentissement de la tendance.</p>
<p><strong>Échelle linéaire ou logarithmique</strong> : sur de longues périodes ou de fortes hausses, une échelle logarithmique (où un même écart vertical représente un même pourcentage) donne des lignes plus pertinentes. Une ligne tracée en échelle linéaire et la même en logarithmique ne coupent pas le prix aux mêmes endroits.</p>
</x-approfondi>
<x-exemple>
<p>Deux creux : jour 5 à 100 € et jour 20 à 106 €. La ligne de tendance passe par ces deux points.</p>
<div class="calcul">Pente = (106 − 100) ÷ (20 − 5) = 6 ÷ 15 = 0,40 € par jour
Valeur de la ligne au jour 30 = 106 + 0,40 × (30 − 20) = 106 + 4 = 110 €
Le haut du canal passe par un sommet au jour 12 à 111 € :
valeur au jour 30 = 111 + 0,40 × (30 − 12) = 111 + 7,20 = 118,20 €
Largeur du canal = 118,20 − 110 = 8,20 €</div>
</x-exemple>
<x-erreurs><ul><li>Ajuster la ligne après coup pour qu'elle « tienne » malgré une cassure.</li><li>Tracer une ligne sur deux points très proches dans le temps.</li><li>Trader le haut et le bas d'un canal sans tenir compte de la tendance de l'unité supérieure.</li></ul></x-erreurs>
<x-cles><ul><li>Ligne haussière : relie des creux ; baissière : relie des sommets ; validée au 3<sup>e</sup> contact.</li><li>Canal = ligne de tendance + parallèle.</li><li>Pente = écart de prix ÷ écart de temps ; projection = dernier point + pente × durée.</li></ul></x-cles>
<x-exo><p>Ligne baissière passant par deux sommets : jour 3 à 75 € et jour 13 à 70 €. Quelle est sa valeur au jour 21 ? Le prix est à 69 € au jour 21 : est-il au-dessus ou en dessous de la ligne ?</p>
<x-corr><div class="calcul">Pente = (70 − 75) ÷ (13 − 3) = −5 ÷ 10 = −0,50 € par jour
Valeur au jour 21 = 70 − 0,50 × 8 = 66 €</div><p>Le prix (69 €) est <strong>au-dessus</strong> de la ligne baissière : elle a été cassée à la hausse. C'est un signe d'essoufflement de la baisse, à confirmer.</p></x-corr></x-exo>
"""),

("4-7", "Les volumes", r"""
<x-obj><ul><li>Utiliser le volume pour confirmer ou relativiser un mouvement.</li><li>Comprendre les limites du volume selon les marchés.</li></ul></x-obj>
<x-simple>
<p>Le <strong>volume</strong> est la quantité échangée pendant une période (nombre d'actions ou de contrats). Il mesure l'<strong>intensité</strong> de la participation. Idée générale : un mouvement accompagné d'un volume élevé implique davantage d'intervenants, et a plus de chances d'être significatif.</p>
</x-simple>
<x-fig c="La cassure de la résistance s'accompagne d'un volume nettement supérieur à la moyenne : un signe de participation, pas une garantie.">""" + SCHEMA_VOLUME + r"""</x-fig>
<x-approfondi>
<ul><li><strong>Confirmation</strong> : cassure avec fort volume ; tendance haussière avec volumes plus forts sur les hausses que sur les baisses.</li>
<li><strong>Divergence</strong> : prix qui monte avec des volumes de plus en plus faibles = essoufflement possible.</li>
<li><strong>Climax</strong> : volume extrême après un long mouvement, parfois proche d'un point de retournement (capitulation).</li></ul>
<p><strong>Limites</strong> : sur le <strong>Forex</strong>, il n'y a pas de volume centralisé ; les plateformes affichent un « volume de ticks » (nombre de variations de prix), qui est un indicateur indirect d'activité. Sur les actions, une partie des échanges a lieu hors de la bourse principale. Le volume est aussi naturellement plus fort à l'ouverture et à la clôture : comparez toujours avec la moyenne de la même heure ou du même type de journée. Des indicateurs comme l'OBV ou le VWAP (module 6) intègrent le volume.</p>
</x-approfondi>
<x-exemple>
<p>Les volumes des 20 dernières séances totalisent 24 millions d'actions. Le jour de la cassure, 3,1 millions d'actions sont échangées.</p>
<div class="calcul">Volume moyen = 24 000 000 ÷ 20 = 1 200 000
Ratio = 3 100 000 ÷ 1 200 000 ≈ 2,6 fois la moyenne</div>
<p>Beaucoup de traders considèrent un volume supérieur à 1,5 ou 2 fois la moyenne comme « élevé ». Ce seuil est une convention, à tester sur votre marché.</p>
</x-exemple>
<x-erreurs><ul><li>Interpréter le volume du Forex affiché par une plateforme comme un volume réel.</li><li>Comparer le volume d'une demi-séance (jour férié) à une séance complète.</li><li>Croire qu'un fort volume indique forcément des achats : chaque transaction a un acheteur et un vendeur.</li></ul></x-erreurs>
<x-cles><ul><li>Le volume mesure l'intensité de la participation.</li><li>Fort volume sur une cassure = confirmation ; volumes déclinants = essoufflement possible.</li><li>Forex : seulement un volume de ticks ; comparer les volumes à des périodes comparables.</li></ul></x-cles>
<x-exo><p>Volume moyen sur 50 jours : 800 000. Trois cassures : jour A 950 000, jour B 2 000 000, jour C 600 000. Calculez les ratios. Laquelle est la mieux confirmée par le volume ?</p>
<x-corr><div class="calcul">A : 950 000 ÷ 800 000 ≈ 1,19
B : 2 000 000 ÷ 800 000 = 2,5
C : 600 000 ÷ 800 000 = 0,75</div><p>La cassure B est la mieux confirmée. La C se fait avec un volume inférieur à la moyenne, ce qui invite à la prudence (risque de fausse cassure).</p></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Principes et limites</h2><ul><li>Prix intègre l'info ; tendances ; répétition des comportements.</li><li>Efficacité débattue ; momentum documenté ; tester avant de croire.</li><li>Le hasard produit des motifs convaincants.</li></ul></div>
<div class="encadre"><h2>Chandeliers</h2><ul><li>OHLC : ouverture, plus haut, plus bas, clôture.</li><li>Corps = ouverture ↔ clôture ; mèches = extrêmes.</li><li>Agrégation : 1<sup>re</sup> ouverture, max des hauts, min des bas, dernière clôture.</li></ul></div>
<div class="encadre"><h2>Unités de temps</h2><ul><li>Contexte (unité longue) → signal → entrée (unité courte).</li><li>Rapport 4 à 6 entre unités (convention).</li><li>Unité courte = plus de bruit et de frais relatifs.</li></ul></div>
<div class="encadre"><h2>Tendance</h2><ul><li>Hausse : sommets et creux plus hauts.</li><li>Baisse : sommets et creux plus bas.</li><li>Rupture de structure : cassure du dernier creux/sommet.</li></ul></div>
<div class="encadre"><h2>Supports / résistances</h2><ul><li>Zones, pas lignes.</li><li>Inversion des rôles après cassure.</li><li>Stop au-delà de la zone, avec une marge (ex. 0,5 ATR).</li></ul></div>
<div class="encadre"><h2>Lignes &amp; canaux</h2><ul><li>2 points pour tracer, 3<sup>e</sup> contact pour valider.</li><li>Pente = Δprix ÷ Δtemps.</li><li>Échelle log sur longues périodes.</li></ul></div>
<div class="encadre"><h2>Volume</h2><ul><li>Ratio = volume du jour ÷ volume moyen.</li><li>Fort volume confirme ; faible volume = prudence.</li><li>Forex : volume de ticks seulement.</li></ul></div>
"""

QUIZ = [
("Quelle est l'une des hypothèses de base de l'analyse technique ?", ["Les prix sont totalement aléatoires", "Les prix évoluent en tendances qui tendent à se prolonger", "Seuls les résultats d'entreprise comptent", "Le volume n'a aucune importance"], 1, "La persistance des tendances est l'un des principes hérités de la théorie de Dow."),
("Si l'on teste 60 règles sans pouvoir prédictif au seuil de 5 %, combien paraîtront significatives par hasard en moyenne ?", ["0", "3", "6", "12"], 1, "60 × 5 % = 3 fausses découvertes en moyenne."),
("Une bougie ouvre à 40, monte à 43, descend à 39 et clôture à 42. Son corps mesure :", ["1", "2", "3", "4"], 1, "Corps = |clôture − ouverture| = 42 − 40 = 2 (bougie haussière)."),
("Dans l'exemple précédent, la mèche basse mesure :", ["1", "2", "3", "0"], 0, "Mèche basse = ouverture − plus bas = 40 − 39 = 1 (pour une bougie haussière)."),
("Pour agréger des bougies horaires en bougie journalière, le plus haut du jour est :", ["Le plus haut de la première bougie", "Le maximum des plus hauts", "La moyenne des plus hauts", "La clôture la plus haute"], 1, "Ouverture = première ouverture ; plus haut = max des hauts ; plus bas = min des bas ; clôture = dernière clôture."),
("Une tendance haussière se définit par :", ["Des sommets plus hauts et des creux plus hauts", "Des sommets plus bas et des creux plus hauts", "Un volume en hausse", "Un prix au-dessus de 100"], 0, "C'est la définition par la structure de marché."),
("Pourquoi tracer des supports sous forme de zones plutôt que de lignes ?", ["Pour faire joli", "Parce que les prix dépassent souvent un niveau de quelques centimes", "Parce que les lignes sont interdites", "Pour placer le stop exactement sur le niveau"], 1, "Les réactions de prix ne sont pas précises au centime : une zone englobe les mèches."),
("Une résistance cassée à la hausse devient souvent :", ["Une ligne de tendance", "Un support", "Un gap", "Sans importance"], 1, "C'est l'inversion des rôles."),
("Ligne de tendance : jour 2 à 50 €, jour 12 à 55 €. Sa valeur au jour 22 ?", ["57,50 €", "60 €", "62,50 €", "65 €"], 1, "Pente = 5 ÷ 10 = 0,50 €/jour ; 55 + 0,50 × 10 = 60 €."),
("Volume moyen 500 000, volume du jour 1 250 000. Ratio ?", ["0,4", "1,25", "2,5", "7,5"], 2, "1 250 000 ÷ 500 000 = 2,5 fois la moyenne."),
("Sur le Forex au comptant, le volume affiché par une plateforme est généralement :", ["Le volume mondial exact", "Un volume de ticks (nombre de variations de prix)", "Le volume de la BCE", "Toujours nul"], 1, "Le Forex n'a pas de marché centralisé : le volume affiché est un indicateur indirect d'activité."),
("Avec un risque fixe de 90 €, passer d'un stop de 1,80 € (journalier) à 0,45 € (horaire) multiplie la taille de position par :", ["2", "4", "0,25", "1"], 1, "1,80 ÷ 0,45 = 4 : 50 actions deviennent 200. Les frais par trade sont multipliés d'autant."),
]
