from svgkit import plot, table, svg, t, line, arrow, path_from, candles

NUM = 5
TITRE = "Chandeliers et figures chartistes"
RESUME = "Doji, marteau, avalement, étoiles ; tête-épaules, doubles sommets, triangles, drapeaux, biseaux ; et surtout leur fiabilité réelle."
DUREE = "2 h"
INTRO = r"""<p>Les configurations de chandeliers et les figures chartistes sont parmi les outils les plus populaires… et les plus surestimés. Ce module vous apprend à les reconnaître et à les mesurer, mais aussi à les remettre à leur juste place : ce sont des <strong>indices de contexte</strong>, jamais des signaux automatiques.</p>"""


def galerie(items, w=660, h=190, label="Configurations de chandeliers"):
    """items : liste de (nom, [ (o,h,l,c), ... ]) ; chaque groupe est normalisé dans sa case."""
    n = len(items)
    cw = w / n
    p = []
    for k, (nom, bougies) in enumerate(items):
        lo = min(b[2] for b in bougies)
        hi = max(b[1] for b in bougies)
        x0 = k * cw
        p.append(f'<rect x="{x0+4:.1f}" y="4" width="{cw-8:.1f}" height="{h-8}" rx="8" class="g-rect"/>')

        def Y(v):
            return 20 + (hi - v) / (hi - lo) * (h - 84)
        m = len(bougies)
        step = min(26, (cw - 30) / m)
        bw = step * 0.6
        start = x0 + cw / 2 - step * (m - 1) / 2
        for j, (o, hh, ll, c) in enumerate(bougies):
            x = start + j * step
            cls = "g-haus" if c >= o else "g-bais"
            p.append(line(x, Y(hh), x, Y(ll), cls + " g-meche"))
            top, bot = Y(max(o, c)), Y(min(o, c))
            p.append(f'<rect x="{x-bw/2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{max(1.6, bot-top):.1f}" class="{cls}"/>')
        mots = nom.split("\n")
        for i, mot in enumerate(mots):
            p.append(t(x0 + cw / 2, h - 34 + i * 14, mot, "g-txt g-fort" if i == 0 else "g-txt g-petit", "middle"))
    return svg(w, h, "".join(p), label)


SCHEMA_SIMPLES = galerie([
    ("Doji\nindécision", [(50, 52, 48, 50.05)]),
    ("Marteau\naprès une baisse", [(49.6, 50.4, 47.8, 50.2)]),
    ("Pendu\naprès une hausse", [(50.2, 50.4, 47.8, 49.6)]),
    ("Étoile filante\naprès une hausse", [(50.2, 52.6, 49.9, 49.7)]),
], label="Configurations à une bougie (1/2)") + galerie([
    ("Marteau inversé\naprès une baisse", [(49.7, 52.4, 49.5, 50.2)]),
    ("Toupie\npetit corps", [(49.8, 51.3, 48.6, 50.3)]),
    ("Marubozu\nsans mèches", [(48, 52, 48, 52)]),
], label="Configurations à une bougie (2/2)")

SCHEMA_MULTI = galerie([
    ("Avalement haussier", [(53, 53.3, 51.6, 52), (52.4, 52.6, 50.3, 50.5), (50.2, 52.6, 50.0, 52.4)]),
    ("Avalement baissier", [(48, 50.2, 47.8, 50), (50.1, 51.6, 49.9, 51.4), (51.7, 51.9, 49.6, 49.8)]),
    ("Harami haussier", [(54, 54.2, 50.8, 51), (51, 51.2, 49.2, 49.4), (49.9, 50.6, 49.7, 50.5)]),
], label="Configurations à plusieurs bougies (1/2)") + galerie([
    ("Étoile du matin", [(54, 54.3, 50.8, 51), (50.6, 50.9, 49.7, 50.4), (50.9, 53.6, 50.7, 53.4)]),
    ("Étoile du soir", [(46, 49.2, 45.8, 49), (49.4, 50.3, 49.1, 49.6), (49.1, 49.3, 46.4, 46.6)]),
    ("Trois soldats", [(48, 49.6, 47.8, 49.4), (49.2, 51, 49, 50.8), (50.6, 52.4, 50.4, 52.2)]),
], label="Configurations à plusieurs bougies (2/2)")

_HS = path_from([(0, 100), (8, 112), (13, 109), (19, 120), (25, 110), (31, 113), (37, 109.5), (41, 104)], seed=81, noise=0.5, wick=0.6)
SCHEMA_HS = candles(_HS, h=300, label="Tête-épaules : épaule gauche, tête, épaule droite et ligne de cou",
                    lines=[{"p1": (13, 109), "p2": (25, 110), "ext": 41, "cls": "g-res"}],
                    marks=[{"i": 8, "p": _HS[8][1], "t": "Épaule gauche"}, {"i": 19, "p": _HS[19][1], "t": "Tête"},
                           {"i": 31, "p": _HS[31][1], "t": "Épaule droite"}, {"i": 38, "p": _HS[38][2], "t": "Cassure de la ligne de cou", "pos": "bas", "anchor": "end"}],
                    legend=[("g-res", "Ligne de cou")], ymax=126)

_DB = path_from([(0, 96), (8, 80.4), (15, 90), (22, 80.8), (30, 90.5), (33, 93), (36, 95)], seed=91, noise=0.5, wick=0.6)
SCHEMA_DB = candles(_DB, h=280, label="Double creux et projection de l'objectif",
                    lines=[{"y": 90, "cls": "g-res", "label": "Ligne de cou 90"}, {"y": 100, "cls": "g-l3", "label": "Objectif théorique 100"}],
                    marks=[{"i": 8, "p": _DB[8][2], "t": "Creux 1", "pos": "bas"}, {"i": 22, "p": _DB[22][2], "t": "Creux 2", "pos": "bas"}],
                    ymax=102, ymin=73)

_FL = path_from([(0, 50), (2, 50.5), (9, 60), (12, 58.4), (15, 57), (18, 56.6), (20, 58.2), (25, 64)], seed=101, noise=0.3, wick=0.35)
SCHEMA_DRAPEAU = candles(_FL, h=280, label="Drapeau haussier : mât, consolidation légèrement descendante, cassure",
                         lines=[{"p1": (9, 60.4), "p2": (19, 58.4), "cls": "g-res"}, {"p1": (10, 58.6), "p2": (18, 56.2), "cls": "g-sup"},
                                {"y": 68, "cls": "g-l3", "label": "Objectif : 58 + 10 = 68"}],
                         marks=[{"i": 5, "p": 54.5, "t": "Mât : +10", "pos": "haut", "anchor": "end", "fleche": False}], ymax=69)

_TR = path_from([(0, 92), (4, 99.8), (8, 94), (12, 99.9), (16, 96), (20, 99.8), (23, 97.6), (25, 100.3), (30, 104)], seed=111, noise=0.25, wick=0.3)
SCHEMA_TRIANGLE = candles(_TR, h=260, label="Triangle ascendant : résistance horizontale et creux de plus en plus hauts",
                          lines=[{"y": 100.2, "cls": "g-res", "label": "Résistance ≈ 100", "i2": 25}, {"p1": (8, 93.6), "p2": (16, 95.6), "ext": 24, "cls": "g-sup"}])

SCHEMA_REUSSITE = plot([{"x": [1, 2, 3], "y": [0.125, -0.04, -0.12], "kind": "bar", "cls": "g-barre-h", "cls_neg": "g-barre-b", "bw": 90}],
                       label="Espérance de trois configurations selon leur taux de réussite et leurs gains et pertes moyens",
                       xr=(0.4, 3.6), yr=(-0.2, 0.2), xticks=[1, 2, 3], legend=False,
                       xfmt=lambda v: {1: "A : 65 %, +1R / −1,5R", 2: "B : 70 %, +0,8R / −2R", 3: "C : 40 %, +1,5R / −1,2R"}.get(int(v), ""),
                       yfmt=lambda v: f"{v:+.2f} R".replace(".", ",").replace("+0,00", "0"))

LECONS = [
("5-1", "Les configurations à une bougie", r"""
<x-obj><ul><li>Reconnaître le doji, le marteau, le pendu, l'étoile filante, le marteau inversé, la toupie et le marubozu.</li><li>Vérifier les critères d'une configuration par le calcul.</li></ul></x-obj>
<x-simple>
<p>Une bougie isolée résume l'équilibre entre acheteurs et vendeurs sur la période. Certaines formes ont reçu un nom, issu de la tradition japonaise des marchés du riz, popularisée en Occident par Steve Nison dans les années 1990 :</p>
<ul><li><strong>Doji</strong> : ouverture ≈ clôture. Indécision.</li>
<li><strong>Marteau</strong> : petit corps en haut, longue mèche basse, <em>après une baisse</em>. Les vendeurs ont poussé le prix vers le bas, mais les acheteurs l'ont ramené.</li>
<li><strong>Pendu</strong> : même forme, mais <em>après une hausse</em>. Signal d'alerte.</li>
<li><strong>Étoile filante</strong> : petit corps en bas, longue mèche haute, après une hausse : rejet des prix élevés.</li>
<li><strong>Marteau inversé</strong> : même forme, après une baisse.</li>
<li><strong>Toupie</strong> : petit corps, mèches des deux côtés : indécision.</li>
<li><strong>Marubozu</strong> : grand corps sans (ou presque sans) mèches : domination nette d'un camp.</li></ul>
</x-simple>
<x-fig c="Les principales configurations à une bougie. Le même dessin change de nom selon le contexte (marteau ou pendu).">""" + SCHEMA_SIMPLES + r"""</x-fig>
<x-approfondi>
<p>Le <strong>contexte</strong> est essentiel : un marteau n'a de sens qu'après une baisse, idéalement sur un support. Le même dessin au milieu d'un range ne signifie à peu près rien.</p>
<p>Les critères chiffrés usuels (ils varient selon les auteurs) : pour un marteau, mèche basse ≥ 2 fois le corps, mèche haute petite (≤ environ un tiers du corps, ou ≤ 10 % de l'amplitude totale). Pour un doji, corps ≤ environ 5 à 10 % de l'amplitude. Définir des critères chiffrés permet de tester objectivement une configuration (module 10).</p>
<p>La plupart des auteurs recommandent d'attendre une <strong>confirmation</strong> : par exemple, une bougie suivante qui clôture au-dessus du plus haut du marteau.</p>
</x-approfondi>
<x-exemple>
<p>Après trois jours de baisse, une bougie affiche : ouverture 49,60 ; plus haut 50,40 ; plus bas 47,80 ; clôture 50,20. Est-ce un marteau selon les critères « mèche basse ≥ 2 × corps » et « mèche haute ≤ 10 % de l'amplitude » ?</p>
<div class="calcul">Corps = 50,20 − 49,60 = 0,60
Mèche basse = min(ouverture, clôture) − plus bas = 49,60 − 47,80 = 1,80 → 1,80 ÷ 0,60 = 3 fois le corps ✔
Amplitude = 50,40 − 47,80 = 2,60
Mèche haute = 50,40 − 50,20 = 0,20 → 0,20 ÷ 2,60 ≈ 7,7 % ✔
Contexte : après une baisse ✔ → marteau</div>
<p>Un trader pourrait alors attendre une clôture au-dessus de 50,40 pour acheter, avec un stop sous 47,80 : distance au stop d'au moins 2,60 €.</p>
</x-exemple>
<x-erreurs><ul><li>Ignorer le contexte (un « marteau » en plein range).</li><li>Agir avant la clôture de la bougie : une bougie en formation peut changer complètement de forme.</li><li>Oublier que la longue mèche du marteau impose un stop éloigné, donc une petite taille.</li></ul></x-erreurs>
<x-cles><ul><li>Une bougie isolée est un indice, pas un signal.</li><li>Le nom dépend du contexte : marteau (après baisse), pendu (après hausse).</li><li>Fixer des critères chiffrés et attendre une confirmation.</li></ul></x-cles>
<x-exo><p>Après une hausse, bougie : ouverture 72,00 ; plus haut 75,10 ; plus bas 71,70 ; clôture 71,80. Calculez le corps et les mèches. Quelle configuration est-ce ?</p>
<x-corr><div class="calcul">Corps = 72,00 − 71,80 = 0,20 (baissier)
Mèche haute = 75,10 − 72,00 = 3,10 (15,5 fois le corps)
Mèche basse = 71,80 − 71,70 = 0,10</div><p>Longue mèche haute, petit corps en bas, après une hausse : une <strong>étoile filante</strong>. Les acheteurs ont poussé jusqu'à 75,10 mais n'ont pas tenu ce niveau.</p></x-corr></x-exo>
"""),

("5-2", "Les configurations à plusieurs bougies", r"""
<x-obj><ul><li>Reconnaître l'avalement, le harami, les étoiles du matin et du soir, les trois soldats et les trois corbeaux.</li><li>Vérifier une configuration à partir des prix.</li></ul></x-obj>
<x-simple>
<ul><li><strong>Avalement haussier</strong> (bullish engulfing) : après une baisse, une bougie haussière dont le corps englobe entièrement le corps baissier précédent. <strong>Avalement baissier</strong> : l'inverse, après une hausse.</li>
<li><strong>Harami</strong> : une petite bougie dont le corps est contenu dans le corps de la grande bougie précédente (« femme enceinte » en japonais). Signal d'essoufflement.</li>
<li><strong>Étoile du matin</strong> : grande bougie baissière, petite bougie (souvent en gap), puis grande bougie haussière qui remonte dans le corps de la première. <strong>Étoile du soir</strong> : l'inverse, après une hausse.</li>
<li><strong>Trois soldats blancs</strong> : trois grandes bougies haussières successives, clôtures de plus en plus hautes. <strong>Trois corbeaux noirs</strong> : l'inverse.</li></ul>
</x-simple>
<x-fig c="Configurations à plusieurs bougies (la ou les premières bougies représentent le contexte).">""" + SCHEMA_MULTI + r"""</x-fig>
<x-approfondi>
<p>Sur les marchés qui cotent en continu (Forex, cryptos, futures presque 24 h/24), il y a rarement des gaps entre bougies : les définitions classiques qui exigent un gap (étoile du matin, par exemple) sont alors assouplies. Autres configurations connues : la pénétrante (piercing line) et la couverture en nuage noir (dark cloud cover), proches des avalements mais partielles.</p>
<p>Comme pour les bougies isolées, la configuration a plus de sens sur un niveau important (support, résistance), dans le sens d'une tendance de l'unité de temps supérieure, et avec un volume élevé.</p>
</x-approfondi>
<x-exemple>
<p>Jour 1 : ouverture 52,00, clôture 50,50 (baissière). Jour 2 : ouverture 50,20, clôture 52,40 (haussière). Est-ce un avalement haussier ?</p>
<div class="calcul">Corps du jour 1 : de 50,50 à 52,00
Corps du jour 2 : de 50,20 à 52,40
Le corps 2 englobe le corps 1 si 50,20 ≤ 50,50 et 52,40 ≥ 52,00 → ✔ les deux sont vrais
Taille relative : corps 2 = 2,20 ; corps 1 = 1,50 → 2,20 ÷ 1,50 ≈ 1,47 fois plus grand</div>
<p>C'est un avalement haussier… à condition qu'il survienne après une baisse.</p>
</x-exemple>
<x-erreurs><ul><li>Voir un avalement dès que la bougie est plus grande, sans vérifier que le <em>corps</em> englobe le corps précédent.</li><li>Trader les trois soldats blancs à leur sommet, alors que le prix est déjà très étendu (stop très lointain).</li><li>Collectionner les noms de configurations sans jamais mesurer leur résultat.</li></ul></x-erreurs>
<x-cles><ul><li>Avalement : le corps englobe le corps précédent.</li><li>Harami : le petit corps est contenu dans le grand.</li><li>Étoiles du matin et du soir : configurations de retournement à trois bougies.</li><li>Toujours : contexte + niveau + confirmation.</li></ul></x-cles>
<x-exo><p>Jour 1 : ouverture 30,00 ; clôture 33,00. Jour 2 : ouverture 32,40 ; clôture 31,20. La tendance précédente était haussière. Quelle configuration ?</p>
<x-corr><div class="calcul">Corps 1 : de 30,00 à 33,00 (haussier, 3,00)
Corps 2 : de 31,20 à 32,40 (baissier, 1,20), entièrement contenu dans le corps 1</div><p>C'est un <strong>harami baissier</strong> : un signe d'essoufflement de la hausse, plus faible qu'un avalement baissier.</p></x-corr></x-exo>
"""),

("5-3", "Les figures de retournement", r"""
<x-obj><ul><li>Identifier une tête-épaules et un double sommet ou double creux.</li><li>Calculer l'objectif théorique d'une figure.</li></ul></x-obj>
<x-simple>
<p>Les <strong>figures chartistes</strong> sont des formes dessinées par les prix sur de nombreuses bougies.</p>
<ul><li><strong>Tête-épaules</strong> (head and shoulders) : trois sommets, celui du milieu (la tête) plus haut que les deux autres (les épaules). Les creux entre eux forment la <strong>ligne de cou</strong>. Sa cassure à la baisse signale un possible retournement baissier. La version inversée (tête-épaules inversée) signale un retournement haussier.</li>
<li><strong>Double sommet</strong> (double top) : deux sommets à peu près au même niveau, séparés par un creux. Cassure de ce creux = signal baissier. <strong>Double creux</strong> (double bottom) : l'inverse. Il existe aussi des triples sommets et triples creux.</li></ul>
</x-simple>
<x-fig c="Tête-épaules : la figure n'est complète qu'à la cassure de la ligne de cou.">""" + SCHEMA_HS + r"""</x-fig>
<x-approfondi>
<p><strong>Objectif théorique</strong> : on mesure la hauteur de la figure (de la tête à la ligne de cou, ou des sommets au creux pour un double sommet) et on la reporte depuis le point de cassure. C'est un ordre de grandeur, pas une destination garantie : le prix peut s'arrêter avant ou aller bien au-delà.</p>
<p>Une figure n'existe qu'<strong>une fois terminée</strong>. Avant la cassure de la ligne de cou, ce ne sont que trois sommets ; beaucoup de « têtes-épaules » en formation ne se terminent jamais. Le prix revient souvent tester la ligne de cou après la cassure (le « pullback »), ce qui offre parfois une entrée avec un stop plus proche.</p>
</x-approfondi>
<x-fig c="Double creux : la hauteur (90 − 80 = 10) est projetée depuis la ligne de cou pour obtenir un objectif théorique de 100.">""" + SCHEMA_DB + r"""</x-fig>
<x-exemple>
<p><strong>Tête-épaules</strong> : tête à 120, ligne de cou à 110 (horizontale pour simplifier).</p>
<div class="calcul">Hauteur = 120 − 110 = 10
Objectif théorique = 110 − 10 = 100
Vente à la cassure vers 109,50, stop au-dessus de l'épaule droite (113) :
Risque = 113 − 109,50 = 3,50 ; gain potentiel = 109,50 − 100 = 9,50
Rapport = 9,50 ÷ 3,50 ≈ 2,7</div>
<p><strong>Double creux</strong> : creux à 80 et 80,80, ligne de cou à 90. Hauteur = 90 − 80 = 10 → objectif = 90 + 10 = 100.</p>
</x-exemple>
<x-erreurs><ul><li>Anticiper la figure avant la cassure de la ligne de cou.</li><li>Voir des têtes-épaules partout (n'importe quels trois sommets).</li><li>Prendre l'objectif théorique pour une certitude et ne pas gérer la position.</li></ul></x-erreurs>
<x-cles><ul><li>Tête-épaules : trois sommets, ligne de cou ; signal à la cassure.</li><li>Double sommet / double creux : deux extrêmes au même niveau.</li><li>Objectif = hauteur de la figure reportée depuis la cassure : un ordre de grandeur.</li></ul></x-cles>
<x-exo><p>Tête-épaules inversée : tête à 42 €, ligne de cou à 50 €. Cassure à 50,40 €. Stop sous l'épaule droite à 46,90 €. Calculez l'objectif théorique et le rapport gain potentiel / risque.</p>
<x-corr><div class="calcul">Hauteur = 50 − 42 = 8
Objectif = 50 + 8 = 58 €
Risque = 50,40 − 46,90 = 3,50 ; gain potentiel = 58 − 50,40 = 7,60
Rapport ≈ 7,60 ÷ 3,50 ≈ 2,2</div></x-corr></x-exo>
"""),

("5-4", "Les figures de continuation", r"""
<x-obj><ul><li>Reconnaître triangles, drapeaux, fanions, biseaux et rectangles.</li><li>Calculer l'objectif d'un drapeau et d'un triangle.</li></ul></x-obj>
<x-simple>
<p>Les figures de continuation sont des <strong>pauses</strong> dans une tendance, après lesquelles celle-ci reprend souvent (mais pas toujours).</p>
<ul><li><strong>Drapeau</strong> : après un mouvement rapide (le « mât »), une petite consolidation en canal légèrement opposé à la tendance, puis une cassure dans le sens du mât. <strong>Fanion</strong> : même chose, mais la consolidation forme un petit triangle.</li>
<li><strong>Triangles</strong> : symétrique (sommets plus bas et creux plus hauts), ascendant (résistance horizontale, creux montants : souvent haussier), descendant (support horizontal, sommets descendants : souvent baissier).</li>
<li><strong>Rectangle</strong> : range entre un support et une résistance horizontaux.</li>
<li><strong>Biseaux</strong> (wedges) : deux lignes convergentes inclinées dans le même sens. Le biseau ascendant est généralement considéré comme baissier, le biseau descendant comme haussier.</li></ul>
</x-simple>
<x-fig c="Drapeau haussier. L'objectif théorique reporte la hauteur du mât depuis le point de cassure.">""" + SCHEMA_DRAPEAU + r"""</x-fig>
<x-fig c="Triangle ascendant : les acheteurs reviennent de plus en plus haut sous une résistance qui finit par céder.">""" + SCHEMA_TRIANGLE + r"""</x-fig>
<x-approfondi>
<p>Les conventions d'objectif : pour un drapeau ou un fanion, on reporte la hauteur du mât depuis la cassure ; pour un triangle, la hauteur de la base (la partie la plus large) depuis la cassure ; pour un rectangle, sa hauteur.</p>
<p>Les volumes diminuent souvent pendant la consolidation et augmentent à la cassure. Une cassure sans volume est plus suspecte. La classification « continuation » ou « retournement » n'est qu'une tendance statistique : un triangle symétrique, par exemple, peut casser dans les deux sens.</p>
</x-approfondi>
<x-exemple>
<p><strong>Drapeau</strong> : le prix monte de 50 à 60 (mât de 10), consolide entre 58,4 et 56,6, puis casse le haut du drapeau à 58.</p>
<div class="calcul">Objectif = point de cassure + hauteur du mât = 58 + 10 = 68
Stop sous le bas du drapeau, 56,40 : risque = 58 − 56,40 = 1,60
Gain potentiel = 68 − 58 = 10 → rapport ≈ 6,25</div>
<p>Un rapport aussi élevé doit rendre prudent : l'objectif est théorique, et un rapport séduisant ne dit rien de la probabilité de l'atteindre.</p>
<p><strong>Triangle ascendant</strong> : résistance à 100, premier creux à 92 (base de 8). Cassure à 100,30 → objectif ≈ 100 + 8 = 108.</p>
</x-exemple>
<x-erreurs><ul><li>Entrer avant la cassure en devinant son sens.</li><li>Confondre un drapeau (consolidation courte et serrée) avec un retournement en cours.</li><li>Oublier qu'une cassure peut être fausse et revenir dans la figure.</li></ul></x-erreurs>
<x-cles><ul><li>Figures de continuation : drapeaux, fanions, triangles, rectangles, biseaux.</li><li>Objectif d'un drapeau = hauteur du mât ajoutée au point de cassure.</li><li>« Continuation » est une tendance statistique, pas une règle.</li></ul></x-cles>
<x-exo><p>Drapeau baissier : le prix chute de 120 à 104, consolide légèrement à la hausse jusqu'à 108, puis casse le bas du drapeau à 105. Calculez l'objectif. Avec un stop à 108,60, quel est le rapport gain potentiel / risque ?</p>
<x-corr><div class="calcul">Mât = 120 − 104 = 16
Objectif = 105 − 16 = 89
Risque = 108,60 − 105 = 3,60 ; gain potentiel = 105 − 89 = 16
Rapport = 16 ÷ 3,60 ≈ 4,4</div></x-corr></x-exo>
"""),

("5-5", "Fiabilité et limites des chandeliers et des figures", r"""
<x-obj><ul><li>Évaluer une configuration par son espérance, pas par son taux de réussite.</li><li>Connaître les limites des statistiques publiées sur les figures.</li></ul></x-obj>
<x-simple>
<p>Une configuration est utile seulement si, <strong>appliquée systématiquement avec des règles précises</strong>, elle rapporte plus qu'elle ne coûte, frais compris. Le « taux de réussite » souvent annoncé ne suffit pas : il faut aussi connaître la taille moyenne des gains et des pertes.</p>
</x-simple>
<x-note>
<ul><li><strong>Subjectivité</strong> : deux analystes ne tracent pas la même ligne de cou. Ce qui n'est pas défini précisément ne peut pas être testé.</li>
<li><strong>Biais rétrospectif</strong> : après coup, on voit les figures qui ont « marché » ; on oublie celles qui ont échoué ou ne se sont jamais terminées.</li>
<li><strong>Statistiques publiées</strong> : des ouvrages de référence (comme ceux de Thomas Bulkowski) compilent des taux de réussite pour de nombreuses figures. Ils sont utiles comme ordre de grandeur, mais dépendent des définitions choisies, des périodes et des marchés, et ne sont pas des études académiques évaluées par des pairs.</li>
<li><strong>Recherche académique</strong> : une étude connue (Lo, Mamaysky et Wang, 2000) a trouvé que certaines figures apportent un peu d'information sur les rendements futurs, sans démontrer qu'on peut en tirer un profit après frais. Plusieurs études sur les chandeliers japonais, sur les actions américaines et japonaises, n'ont pas trouvé de rentabilité après coûts.</li></ul>
<p>Conclusion raisonnable : ces outils servent à <strong>localiser</strong> des zones de décision et à placer des stops logiques. Leur valeur prédictive propre est faible et doit être testée sur votre marché.</p>
</x-note>
<x-exemple>
<p>Trois configurations mesurées sur 100 occurrences chacune (chiffres illustratifs, en R : multiples du risque initial) :</p>
<div class="calcul">A : réussite 65 %, gain moyen 1R, perte moyenne 1,5R
    Espérance = 0,65 × 1 − 0,35 × 1,5 = 0,65 − 0,525 = +0,125 R par trade
B : réussite 70 %, gain moyen 0,8R, perte moyenne 2R
    Espérance = 0,70 × 0,8 − 0,30 × 2 = 0,56 − 0,60 = −0,04 R par trade
C : réussite 40 %, gain moyen 1,5R, perte moyenne 1,2R
    Espérance = 0,40 × 1,5 − 0,60 × 1,2 = 0,60 − 0,72 = −0,12 R par trade</div>
<p>La configuration B, avec le meilleur taux de réussite (70 %), <strong>perd de l'argent</strong>. Et si les frais coûtent 0,05R par trade, l'espérance de A tombe à +0,075R : la marge est mince.</p>
</x-exemple>
<x-fig c="Espérance par trade des trois configurations (avant frais). Le taux de réussite seul ne dit rien de la rentabilité.">""" + SCHEMA_REUSSITE + r"""</x-fig>
<x-erreurs><ul><li>Choisir une configuration pour son taux de réussite affiché.</li><li>Croire aux statistiques d'une vidéo ou d'une formation payante sans pouvoir les vérifier.</li><li>Compter ses souvenirs de « figures qui ont marché » au lieu de tenir des statistiques complètes.</li></ul></x-erreurs>
<x-cles><ul><li>Ce qui compte : l'espérance (réussite × gain moyen − échec × perte moyenne), frais compris.</li><li>Les figures sont subjectives ; il faut des règles précises pour les tester.</li><li>Leur intérêt principal : localiser des zones de décision et placer des stops logiques.</li></ul></x-cles>
<x-exo><p>Une configuration réussit 55 % du temps, avec un gain moyen de 1,2R et une perte moyenne de 1R. Les frais coûtent 0,08R par trade. Quelle est l'espérance nette ? Sur 200 trades à 100 € de risque, quel résultat moyen attendre ?</p>
<x-corr><div class="calcul">Espérance brute = 0,55 × 1,2 − 0,45 × 1 = 0,66 − 0,45 = +0,21 R
Espérance nette = 0,21 − 0,08 = +0,13 R
Sur 200 trades : 200 × 0,13 × 100 € = +2 600 € en moyenne</div><p>« En moyenne » : la dispersion autour de ce résultat peut être grande (voir le simulateur de trajectoires), et ces chiffres doivent venir d'un échantillon suffisant.</p></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Une bougie</h2><ul><li>Doji : indécision.</li><li>Marteau (après baisse) / pendu (après hausse) : longue mèche basse.</li><li>Étoile filante / marteau inversé : longue mèche haute.</li><li>Toupie : petit corps ; marubozu : sans mèches.</li><li>Critère marteau : mèche basse ≥ 2 × corps.</li></ul></div>
<div class="encadre"><h2>Plusieurs bougies</h2><ul><li>Avalement : corps qui englobe le corps précédent.</li><li>Harami : corps contenu dans le précédent.</li><li>Étoiles du matin / du soir.</li><li>Trois soldats / trois corbeaux.</li></ul></div>
<div class="encadre"><h2>Retournement</h2><ul><li>Tête-épaules (et inversée) : signal à la cassure de la ligne de cou.</li><li>Double / triple sommet ou creux.</li><li>Objectif = hauteur reportée depuis la cassure.</li></ul></div>
<div class="encadre"><h2>Continuation</h2><ul><li>Drapeau, fanion : objectif = hauteur du mât.</li><li>Triangles symétrique, ascendant, descendant.</li><li>Rectangle ; biseaux (ascendant souvent baissier).</li></ul></div>
<div class="encadre"><h2>Fiabilité</h2><ul><li>Contexte + niveau + confirmation + volume.</li><li>Espérance = p × gain moyen − (1 − p) × perte moyenne.</li><li>Taux de réussite élevé ≠ rentable.</li><li>Subjectivité, biais rétrospectif, statistiques à vérifier.</li></ul></div>
"""

QUIZ = [
("Une bougie avec un petit corps en haut et une longue mèche basse, après une baisse, s'appelle :", ["Un pendu", "Un marteau", "Une étoile filante", "Un marubozu"], 1, "Même forme que le pendu, mais après une baisse : c'est un marteau."),
("Le même dessin qu'un marteau, mais après une hausse, s'appelle :", ["Un doji", "Un pendu", "Un harami", "Un avalement"], 1, "Le contexte change le nom et l'interprétation."),
("Bougie : ouverture 20,0 ; clôture 20,4 ; plus bas 19,0. La mèche basse mesure combien de fois le corps ?", ["1,5", "2,5", "3,5", "4"], 1, "Corps = 0,4 ; mèche basse = 20,0 − 19,0 = 1,0 ; 1,0 ÷ 0,4 = 2,5."),
("Un avalement haussier exige que :", ["La deuxième bougie ait un volume double", "Le corps haussier englobe entièrement le corps baissier précédent", "Les mèches soient égales", "Il y ait un gap"], 1, "C'est la définition : le corps englobe le corps précédent, après une baisse."),
("Une tête-épaules est considérée comme complète :", ["Dès que la tête est formée", "À la cassure de la ligne de cou", "Après trois jours", "Quand le volume baisse"], 1, "Avant la cassure de la ligne de cou, ce ne sont que trois sommets."),
("Double sommet : sommets à 150, creux intermédiaire à 138. Objectif théorique après cassure ?", ["126", "132", "138", "162"], 0, "Hauteur = 150 − 138 = 12 ; objectif = 138 − 12 = 126."),
("Drapeau haussier : mât de 40 à 52, cassure à 50. Objectif théorique ?", ["52", "56", "62", "64"], 2, "Mât = 12 ; objectif = 50 + 12 = 62."),
("Un triangle ascendant a :", ["Un support horizontal et des sommets descendants", "Une résistance horizontale et des creux montants", "Deux lignes parallèles", "Aucune ligne"], 1, "Les creux montent sous une résistance plate : la pression acheteuse augmente."),
("Le biseau ascendant est généralement considéré comme :", ["Une figure haussière", "Une figure baissière", "Neutre", "Une configuration de chandelier"], 1, "Deux lignes montantes convergentes : la hausse s'essouffle ; il est souvent classé comme baissier."),
("Réussite 70 %, gain moyen 0,5R, perte moyenne 1,5R. Espérance ?", ["+0,35 R", "−0,10 R", "+0,20 R", "0"], 1, "0,70 × 0,5 − 0,30 × 1,5 = 0,35 − 0,45 = −0,10 R : perdante malgré 70 % de réussite."),
("Quelle affirmation sur les figures chartistes est la plus juste ?", ["Elles prédisent l'avenir avec 80 % de fiabilité", "Leur valeur prédictive est débattue ; elles aident surtout à localiser des zones de décision", "Elles ne fonctionnent que sur les cryptos", "Elles sont validées par toutes les études académiques"], 1, "La recherche est partagée ; leur intérêt principal est de structurer les décisions et les stops."),
]
