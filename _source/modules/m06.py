import random
from svgkit import (plot, table, svg, t, line, path_from, candles, panneau, sma, ema, rsi,
                    stochastique, bollinger, atr, macd, correlation)

NUM = 6
TITRE = "Indicateurs techniques"
RESUME = "Moyennes mobiles, MACD, RSI, stochastique, Bollinger, ATR, VWAP, Ichimoku, Fibonacci, divergences… et le piège de la surcharge."
DUREE = "3 h 30"
INTRO = r"""<p>Un <strong>indicateur technique</strong> est un calcul appliqué aux prix (et parfois aux volumes) pour en extraire une information : tendance, élan, volatilité. Tous sont <strong>dérivés du prix</strong> : ils n'ajoutent aucune information nouvelle, ils la présentent autrement. Ce module explique comment chacun est calculé (vous saurez le refaire à la main), comment on l'interprète, et pourquoi en empiler dix ne sert à rien.</p>"""

# Série principale utilisée par la plupart des schémas
D = path_from([(0, 100), (25, 112), (40, 105), (65, 121), (80, 113), (95, 116), (110, 104), (120, 108)], seed=5, noise=1.0, wick=0.8)
C = [x[3] for x in D]
N = len(D)

SCHEMA_MM = candles(D, label="Moyennes mobiles simple et exponentielle sur 20 périodes, et simple sur 50",
                    overlays=[{"values": sma(C, 20), "cls": "g-l1"}, {"values": ema(C, 20), "cls": "g-l2"}, {"values": sma(C, 50), "cls": "g-l3 g-plein"}],
                    legend=[("g-l1", "SMA 20"), ("g-l2", "EMA 20"), ("g-l3 g-plein", "SMA 50")])

_m, _s, _h = macd(C)
SCHEMA_MACD = candles(D, h=220, label="Prix") + panneau(
    [{"values": _h, "kind": "bar"}, {"values": _m, "cls": "g-l1"}, {"values": _s, "cls": "g-l2"}], N, h=150,
    yr=(min(v for v in _h + _m + _s if v is not None) * 1.15, max(v for v in _h + _m + _s if v is not None) * 1.15),
    titre="MACD (12, 26, 9) : ligne MACD (bleu), signal (orange), histogramme", label="MACD", dec=1)

_r = rsi(C, 14)
SCHEMA_RSI = candles(D, h=220, label="Prix") + panneau(
    [{"values": _r, "cls": "g-l4"}], N, h=140, yr=(0, 100), yticks=[30, 50, 70],
    zones=[{"y1": 70, "y2": 100, "cls": "g-zone-res"}, {"y1": 0, "y2": 30, "cls": "g-zone-sup"}],
    titre="RSI 14 (zones 70 / 30)", label="RSI")

_k, _d = stochastique(D, 14, 3)
SCHEMA_STOCH = panneau([{"values": _k, "cls": "g-l1"}, {"values": _d, "cls": "g-l2"}], N, h=140, yr=(0, 100), yticks=[20, 50, 80],
                       zones=[{"y1": 80, "y2": 100, "cls": "g-zone-res"}, {"y1": 0, "y2": 20, "cls": "g-zone-sup"}],
                       titre="Stochastique 14, 3 : %K (bleu), %D (orange)", label="Stochastique")
CORR = correlation(_r, _k)
SCHEMA_REDONDANCE = panneau([{"values": _r, "cls": "g-l4"}, {"values": _k, "cls": "g-l1"}], N, h=150, yr=(0, 100), yticks=[20, 50, 80],
                            titre=f"RSI 14 (vert) et stochastique %K 14 (bleu) : corrélation ≈ {CORR:.2f}".replace(".", ","), label="Redondance RSI et stochastique")

_bm, _bu, _bl = bollinger(C, 20, 2)
SCHEMA_BOLL = candles(D, label="Bandes de Bollinger (20, 2)",
                      overlays=[{"values": _bu, "values2": _bl, "cls_fill": "g-zone"}, {"values": _bm, "cls": "g-l1"},
                                {"values": _bu, "cls": "g-l3 g-plein"}, {"values": _bl, "cls": "g-l3 g-plein"}],
                      legend=[("g-l1", "Moyenne mobile 20"), ("g-l3 g-plein", "Bandes à ± 2 écarts-types")])

DA = (path_from([(0, 100), (30, 104), (45, 102)], seed=7, noise=0.4, wick=0.3)
      + path_from([(0, 102), (12, 110), (25, 99), (40, 106)], seed=8, noise=2.2, wick=1.6)[1:]
      + path_from([(0, 106), (35, 108)], seed=9, noise=0.6, wick=0.4)[1:])
_a = atr(DA, 14)
SCHEMA_ATR = candles(DA, h=220, label="Prix") + panneau([{"values": _a, "cls": "g-l5"}], len(DA), h=130,
                                                        yr=(0, max(v for v in _a if v) * 1.3), titre="ATR 14 (en points de prix)", label="ATR", dec=1)

# Intraday pour le VWAP
_rnd = random.Random(3)
ID = path_from([(0, 100), (8, 101.6), (20, 100.4), (30, 101.2), (39, 102.4)], seed=13, noise=0.25, wick=0.2)
VOLI = [int(2000 + 3000 * (1 if k < 4 or k > 34 else 0.4) * _rnd.uniform(0.6, 1.4)) for k in range(len(ID))]
_cum_pv, _cum_v, VW = 0, 0, []
for (o, h, l, c), v in zip(ID, VOLI):
    _cum_pv += (h + l + c) / 3 * v
    _cum_v += v
    VW.append(_cum_pv / _cum_v)
SCHEMA_VWAP = candles(ID, h=280, vol=VOLI, label="VWAP intraday", overlays=[{"values": VW, "cls": "g-l2"}],
                      legend=[("g-l2", "VWAP (repart de zéro chaque séance)")])


def _ichimoku(d):
    def milieu(i, n):
        if i < n - 1:
            return None
        w = d[i - n + 1:i + 1]
        return (max(x[1] for x in w) + min(x[2] for x in w)) / 2
    tenkan = [milieu(i, 9) for i in range(len(d))]
    kijun = [milieu(i, 26) for i in range(len(d))]
    ssa_raw = [None if a is None or b is None else (a + b) / 2 for a, b in zip(tenkan, kijun)]
    ssb_raw = [milieu(i, 52) for i in range(len(d))]
    ssa = [None] * 26 + ssa_raw[:-26]
    ssb = [None] * 26 + ssb_raw[:-26]
    chikou = [x[3] for x in d[26:]] + [None] * 26
    return tenkan, kijun, ssa, ssb, chikou


_tk, _kj, _sa, _sb, _ck = _ichimoku(D)
SCHEMA_ICHI = candles(D, label="Ichimoku : Tenkan, Kijun, nuage (Kumo) et Chikou",
                      overlays=[{"values": _sa, "values2": _sb, "cls_fill": "g-zone"}, {"values": _sa, "cls": "g-lh g-fin"}, {"values": _sb, "cls": "g-lb g-fin"},
                                {"values": _tk, "cls": "g-l1"}, {"values": _kj, "cls": "g-l2"}, {"values": _ck, "cls": "g-l3 g-plein g-fin"}],
                      legend=[("g-l1", "Tenkan (9)"), ("g-l2", "Kijun (26)"), ("g-lh", "Senkou A"), ("g-lb", "Senkou B"), ("g-l3 g-plein", "Chikou")])

F = path_from([(0, 82), (5, 80), (22, 120), (32, 104.5), (38, 112)], seed=17, noise=0.6, wick=0.6)
SCHEMA_FIBO = candles(F, h=300, label="Retracements de Fibonacci d'une hausse de 80 à 120",
                      lines=[{"y": 120 - 40 * r / 100, "cls": "g-l3", "label": f"{str(r).replace('.', ',')} % → {120 - 40 * r / 100:.2f}".replace(".", ",")}
                             for r in (23.6, 38.2, 50, 61.8, 78.6)] + [{"y": 120, "cls": "g-axe", "label": "0 % → 120"}, {"y": 80, "cls": "g-axe", "label": "100 % → 80"}])

DV = path_from([(0, 100), (14, 112), (22, 106), (34, 113.5), (44, 104)], seed=23, noise=0.9, wick=0.6)
_rdv = rsi([x[3] for x in DV], 14)
_i1 = max(range(10, 18), key=lambda i: DV[i][1])
_i2 = max(range(28, 38), key=lambda i: DV[i][1])
SCHEMA_DIV = candles(DV, h=230, label="Divergence baissière : nouveau sommet du prix",
                     lines=[{"p1": (_i1, DV[_i1][1]), "p2": (_i2, DV[_i2][1]), "cls": "g-res"}]) + panneau(
    [{"values": _rdv, "cls": "g-l4"}], len(DV), h=140, yr=(0, 100), yticks=[30, 50, 70],
    titre=f"RSI 14 : {_rdv[_i1]:.0f} au 1er sommet, {_rdv[_i2]:.0f} au 2e (plus bas)", label="RSI en divergence")

_p1, _p2 = DV[_i1][1], DV[_i2][1]
_creux = min(x[2] for x in DV[_i1:_i2 + 1])
def _f(v, d=2):
    return f"{v:.{d}f}".replace(".", ",")
DIV_TXT = (f"Sommet 1 : prix {_f(_p1)} ; RSI {_rdv[_i1]:.0f}\n"
           f"Sommet 2 : prix {_f(_p2)} (plus haut) ; RSI {_rdv[_i2]:.0f} (plus bas)\n"
           f"→ Divergence baissière : {_f((_p2 / _p1 - 1) * 100, 1)} % de plus sur le prix, {_rdv[_i2] - _rdv[_i1]:.0f} points de RSI\n"
           f"Confirmation possible : cassure du creux intermédiaire ({_f(_creux)}) → vente, stop au-dessus de {_f(_p2)}\n"
           f"Risque = {_f(_p2)} − {_f(_creux)} = {_f(_p2 - _creux)} points : stop éloigné, la taille de position doit être réduite")

LECONS = [
("6-1", "Indicateurs de tendance et oscillateurs", r"""
<x-obj><ul><li>Classer les indicateurs par famille.</li><li>Comprendre le compromis entre réactivité et faux signaux.</li></ul></x-obj>
<x-simple>
<p>On distingue surtout :</p>
<ul><li>les <strong>indicateurs de tendance</strong> (moyennes mobiles, MACD, Ichimoku…) : ils aident à savoir dans quel sens va le marché. Ils fonctionnent bien en tendance et donnent beaucoup de faux signaux en range ;</li>
<li>les <strong>oscillateurs</strong> (RSI, stochastique…) : ils évoluent entre des bornes et mesurent l'élan (momentum), ou la position du prix dans son amplitude récente. Ils sont plus utiles en range et peuvent rester « extrêmes » très longtemps en tendance ;</li>
<li>les <strong>indicateurs de volatilité</strong> (ATR, bandes de Bollinger) et de <strong>volume</strong> (VWAP, OBV).</li></ul>
</x-simple>
<x-approfondi>
<p>Tous les indicateurs calculés sur des prix passés sont <strong>retardés</strong> (lagging) : ils confirment ce qui s'est passé. Plus un indicateur est réactif (période courte), plus il donne de signaux précoces… et de faux signaux. Plus il est lent, plus il est fiable sur la direction… mais tardif. Il n'existe pas de réglage « optimal » universel : c'est un compromis à tester.</p>
<p>Certains présentent les oscillateurs comme « avancés » (leading) parce qu'ils peuvent montrer un essoufflement avant le prix. C'est un abus de langage : ils sont calculés sur le passé comme les autres.</p>
</x-approfondi>
<x-exemple>
<p>Un prix monte de 1 € par jour pendant 30 jours (100 → 130). Quel est le retard d'une moyenne mobile simple sur 10 jours ?</p>
<div class="calcul">Au jour 30, la moyenne des 10 dernières clôtures = moyenne de 121 à 130 = (121 + 130) ÷ 2 = 125,5
Prix actuel = 130 → écart = 4,5 €, soit le prix d'il y a 4,5 jours
Avec une moyenne sur 20 jours : moyenne de 111 à 130 = 120,5 → retard de 9,5 jours</div>
<p>Dans une tendance régulière, une moyenne simple sur N périodes est en retard d'environ (N − 1) ÷ 2 périodes.</p>
</x-exemple>
<x-erreurs><ul><li>Utiliser un oscillateur pour vendre « parce qu'il est en surachat » dans une forte tendance haussière.</li><li>Chercher le réglage parfait qui aurait tout prédit sur le passé (surapprentissage).</li></ul></x-erreurs>
<x-cles><ul><li>Familles : tendance, oscillateurs, volatilité, volume.</li><li>Tous les indicateurs sont dérivés du prix et retardés.</li><li>Réactivité ↔ faux signaux : un compromis, pas une solution.</li></ul></x-cles>
<x-exo><p>Une moyenne mobile simple sur 50 jours, dans une tendance régulière : de combien de jours est-elle en retard ? Si le prix monte de 0,40 € par jour, quel est l'écart attendu entre le prix et la moyenne ?</p>
<x-corr><div class="calcul">Retard ≈ (50 − 1) ÷ 2 = 24,5 jours
Écart ≈ 24,5 × 0,40 = 9,80 €</div></x-corr></x-exo>
"""),

("6-2", "Les moyennes mobiles (SMA et EMA)", r"""
<x-obj><ul><li>Calculer une moyenne mobile simple et exponentielle.</li><li>Connaître leurs usages : filtre de tendance, supports dynamiques, croisements.</li></ul></x-obj>
<x-simple>
<p>Une <strong>moyenne mobile simple</strong> (SMA) sur N périodes est la moyenne des N dernières clôtures. Elle « glisse » à chaque nouvelle bougie. Une <strong>moyenne mobile exponentielle</strong> (EMA) donne plus de poids aux prix récents : elle réagit plus vite.</p>
<p>Usages classiques : savoir si le prix est au-dessus (contexte haussier) ou en dessous (contexte baissier) d'une moyenne de référence (50 ou 200 jours sur les actions) ; repérer des replis vers une moyenne dans une tendance ; suivre les croisements de deux moyennes.</p>
</x-simple>
<x-fig c="La moyenne exponentielle (orange) suit le prix de plus près que la moyenne simple de même période (bleu). La moyenne 50 (pointillés) est beaucoup plus lente.">""" + SCHEMA_MM + r"""</x-fig>
<x-approfondi>
<div class="formule">SMA<sub>N</sub> = (C<sub>1</sub> + C<sub>2</sub> + … + C<sub>N</sub>) ÷ N</div>
<div class="formule">EMA<sub>aujourd'hui</sub> = C<sub>aujourd'hui</sub> × k + EMA<sub>hier</sub> × (1 − k), avec k = 2 ÷ (N + 1)</div>
<p>On initialise souvent l'EMA avec la SMA des N premières valeurs : selon l'initialisation, deux plateformes peuvent afficher des valeurs légèrement différentes au début de l'historique.</p>
<p><strong>Croisements</strong> : quand une moyenne courte passe au-dessus d'une moyenne longue, on parle de croisement haussier (le « golden cross » désigne souvent le passage de la 50 jours au-dessus de la 200 jours ; le « death cross », l'inverse). Ces signaux sont très tardifs et produisent de nombreux allers-retours perdants en range.</p>
</x-approfondi>
<x-exemple>
<p>Clôtures des 5 derniers jours : 10, 11, 12, 11, 13.</p>
<div class="calcul">SMA 5 = (10 + 11 + 12 + 11 + 13) ÷ 5 = 57 ÷ 5 = 11,40
Le lendemain, clôture à 14 :
  Nouvelle SMA 5 = (11 + 12 + 11 + 13 + 14) ÷ 5 = 61 ÷ 5 = 12,20
  EMA 5 : k = 2 ÷ (5 + 1) = 0,333 ; en partant de 11,40
  EMA = 14 × 0,333 + 11,40 × 0,667 = 4,667 + 7,600 = 12,27</div>
<p>L'EMA (12,27) a davantage réagi au dernier prix (14) que la SMA (12,20).</p>
</x-exemple>
<x-erreurs><ul><li>Acheter chaque croisement en range : une succession de petites pertes.</li><li>Croire qu'une moyenne précise (200 jours) a un pouvoir particulier : elle est surveillée par beaucoup, ce qui peut créer des réactions, rien de plus.</li><li>Changer de période à chaque fois que la moyenne « ne marche pas ».</li></ul></x-erreurs>
<x-cles><ul><li>SMA : moyenne des N dernières clôtures ; EMA : poids plus fort aux prix récents, k = 2 ÷ (N + 1).</li><li>Usage principal : filtrer le contexte (au-dessus / en dessous).</li><li>Croisements tardifs, nombreux faux signaux en range.</li></ul></x-cles>
<x-exo><p>EMA 10 d'hier : 50,00. Clôture du jour : 52,20. Calculez l'EMA 10 du jour.</p>
<x-corr><div class="calcul">k = 2 ÷ 11 ≈ 0,1818
EMA = 52,20 × 0,1818 + 50,00 × 0,8182 ≈ 9,49 + 40,91 = 50,40</div></x-corr></x-exo>
"""),

("6-3", "Le MACD", r"""
<x-obj><ul><li>Comprendre la construction du MACD.</li><li>Lire ses trois composantes et leurs signaux.</li></ul></x-obj>
<x-simple>
<p>Le <strong>MACD</strong> (Moving Average Convergence Divergence, Gerald Appel) mesure l'écart entre deux moyennes exponentielles :</p>
<ul><li><strong>ligne MACD</strong> = EMA 12 − EMA 26 ;</li><li><strong>ligne de signal</strong> = EMA 9 de la ligne MACD ;</li><li><strong>histogramme</strong> = MACD − signal.</li></ul>
<p>MACD positif : la moyenne courte est au-dessus de la longue (élan haussier). Histogramme qui diminue : l'élan ralentit.</p>
</x-simple>
<x-fig c="Le MACD est un indicateur de tendance et d'élan, retardé comme les moyennes dont il est issu.">""" + SCHEMA_MACD + r"""</x-fig>
<x-approfondi>
<p>Signaux courants : croisement de la ligne MACD et de sa ligne de signal, passage de la ligne MACD au-dessus ou en dessous de zéro, divergences avec le prix (leçon 6.11). Le MACD n'est pas borné : ses valeurs dépendent du prix de l'actif, on ne peut donc pas comparer le MACD de deux actifs différents. Les paramètres 12/26/9 sont historiques (issus de la semaine de 6 jours de bourse d'autrefois) et n'ont rien d'optimal.</p>
</x-approfondi>
<x-exemple>
<div class="calcul">EMA 12 = 105,20 ; EMA 26 = 103,80
Ligne MACD = 105,20 − 103,80 = +1,40
Ligne de signal (EMA 9 du MACD) = 1,10
Histogramme = 1,40 − 1,10 = +0,30
Le lendemain : MACD = 1,25 ; signal = 1,13 → histogramme = +0,12 (l'élan haussier ralentit)</div>
</x-exemple>
<x-erreurs><ul><li>Prendre chaque croisement MACD / signal comme un signal d'achat ou de vente.</li><li>Comparer la valeur du MACD d'une action à 20 € et d'une action à 500 €.</li></ul></x-erreurs>
<x-cles><ul><li>MACD = EMA 12 − EMA 26 ; signal = EMA 9 du MACD ; histogramme = différence.</li><li>Mesure la tendance et l'élan, avec retard.</li><li>Non borné : valeurs propres à chaque actif.</li></ul></x-cles>
<x-exo><p>EMA 12 = 47,30 ; EMA 26 = 48,10 ; signal = −0,50. Calculez la ligne MACD et l'histogramme. Que disent-ils ?</p>
<x-corr><div class="calcul">MACD = 47,30 − 48,10 = −0,80
Histogramme = −0,80 − (−0,50) = −0,30</div><p>La moyenne courte est sous la longue (contexte baissier), et le MACD est sous sa ligne de signal : l'élan baissier s'accentue.</p></x-corr></x-exo>
"""),

("6-4", "Le RSI", r"""
<x-obj><ul><li>Calculer un RSI pas à pas.</li><li>Interpréter les zones de 70 et 30 avec prudence.</li></ul></x-obj>
<x-simple>
<p>Le <strong>RSI</strong> (Relative Strength Index, J. Welles Wilder, 1978) compare l'ampleur des hausses et des baisses récentes. Il évolue entre 0 et 100. Au-dessus de 70, on parle de <strong>surachat</strong> ; sous 30, de <strong>survente</strong>. Ces mots sont trompeurs : un marché « suracheté » peut continuer à monter longtemps.</p>
</x-simple>
<x-fig c="RSI 14 : en tendance haussière, il peut rester longtemps au-dessus de 50 et toucher 70 à plusieurs reprises sans que la hausse s'arrête.">""" + SCHEMA_RSI + r"""</x-fig>
<x-approfondi>
<div class="formule">RSI = 100 − 100 ÷ (1 + RS), avec RS = moyenne des hausses ÷ moyenne des baisses (sur N périodes, N = 14 par défaut)</div>
<p>Wilder utilise un lissage particulier : après la première moyenne simple, chaque nouvelle moyenne = (moyenne précédente × (N − 1) + valeur du jour) ÷ N. Certaines plateformes utilisent d'autres lissages : les valeurs peuvent différer légèrement.</p>
<p>Usages : en tendance haussière, un RSI qui redescend vers 40-50 peut signaler un repli « normal » ; les zones 70/30 sont plus pertinentes en range ; les divergences (leçon 6.11) signalent un essoufflement.</p>
</x-approfondi>
<x-exemple>
<p>RSI simplifié sur 5 périodes (pour faciliter le calcul), clôtures : 44,0 ; 44,5 ; 44,2 ; 45,0 ; 45,6 ; 45,3.</p>
<div class="calcul">Variations : +0,5 ; −0,3 ; +0,8 ; +0,6 ; −0,3
Moyenne des hausses = (0,5 + 0,8 + 0,6) ÷ 5 = 1,9 ÷ 5 = 0,38
Moyenne des baisses = (0,3 + 0,3) ÷ 5 = 0,6 ÷ 5 = 0,12
RS = 0,38 ÷ 0,12 ≈ 3,167
RSI = 100 − 100 ÷ (1 + 3,167) = 100 − 24,0 = 76,0
Le jour suivant, +0,4 (lissage de Wilder) :
  hausses = (0,38 × 4 + 0,4) ÷ 5 = 0,384 ; baisses = (0,12 × 4 + 0) ÷ 5 = 0,096
  RS = 4,0 → RSI = 100 − 100 ÷ 5 = 80,0</div>
</x-exemple>
<x-erreurs><ul><li>Vendre systématiquement à 70 dans une tendance haussière forte.</li><li>Acheter systématiquement à 30 dans une tendance baissière (« ça ne peut pas baisser plus »).</li><li>Comparer des RSI de périodes différentes.</li></ul></x-erreurs>
<x-cles><ul><li>RSI = 100 − 100 ÷ (1 + RS), RS = hausses moyennes ÷ baisses moyennes.</li><li>Surachat / survente ≠ signal de retournement.</li><li>Plus utile en range, ou pour repérer les divergences.</li></ul></x-cles>
<x-exo><p>Sur 14 périodes, la moyenne des hausses est de 0,90 et celle des baisses de 0,60. Calculez le RSI.</p>
<x-corr><div class="calcul">RS = 0,90 ÷ 0,60 = 1,5
RSI = 100 − 100 ÷ 2,5 = 100 − 40 = 60</div></x-corr></x-exo>
"""),

("6-5", "Le stochastique", r"""
<x-obj><ul><li>Calculer le %K et le %D.</li><li>Comprendre ce que mesure le stochastique.</li></ul></x-obj>
<x-simple>
<p>Le <strong>stochastique</strong> (George Lane) situe la dernière clôture dans l'amplitude des N dernières périodes : 100 = clôture au plus haut de la période, 0 = clôture au plus bas. Zones usuelles : au-dessus de 80 (haut de l'amplitude), sous 20 (bas de l'amplitude).</p>
</x-simple>
<x-approfondi>
<div class="formule">%K = (Clôture − Plus bas sur N) ÷ (Plus haut sur N − Plus bas sur N) × 100</div>
<div class="formule">%D = moyenne mobile (souvent sur 3) du %K</div>
<p>La version « lente » lisse le %K une fois de plus. Signaux courants : croisements de %K et %D dans les zones extrêmes. Mêmes limites que le RSI : en tendance, il reste collé aux extrêmes.</p>
</x-approfondi>
<x-fig c="Stochastique (14, 3) calculé sur les mêmes prix que les schémas précédents.">""" + SCHEMA_STOCH + r"""</x-fig>
<x-exemple>
<div class="calcul">Sur 14 jours : plus haut = 58,00 ; plus bas = 50,00 ; clôture = 56,00
%K = (56 − 50) ÷ (58 − 50) × 100 = 6 ÷ 8 × 100 = 75
Les deux %K précédents valaient 68 et 80 → %D = (68 + 80 + 75) ÷ 3 = 74,3</div>
</x-exemple>
<x-erreurs><ul><li>Utiliser le stochastique et le RSI en même temps en croyant avoir deux confirmations indépendantes (leçon 6.12).</li><li>Agir sur chaque croisement %K/%D, très fréquents.</li></ul></x-erreurs>
<x-cles><ul><li>Stochastique = position de la clôture dans l'amplitude des N dernières périodes.</li><li>%K brut, %D = moyenne de %K.</li><li>Zones 80 / 20 ; mêmes limites que le RSI en tendance.</li></ul></x-cles>
<x-exo><p>Plus haut sur 14 jours : 1,1050 ; plus bas : 1,0950 ; clôture : 1,0970. Calculez le %K. Où se situe la clôture ?</p>
<x-corr><div class="calcul">%K = (1,0970 − 1,0950) ÷ (1,1050 − 1,0950) × 100 = 0,0020 ÷ 0,0100 × 100 = 20</div><p>La clôture est dans le bas de son amplitude récente (zone de 20).</p></x-corr></x-exo>
"""),

("6-6", "Les bandes de Bollinger", r"""
<x-obj><ul><li>Calculer des bandes de Bollinger.</li><li>Comprendre la notion de compression (squeeze) et ses limites.</li></ul></x-obj>
<x-simple>
<p>Les <strong>bandes de Bollinger</strong> (John Bollinger) entourent une moyenne mobile (20 périodes) de deux bandes placées à ± 2 <strong>écarts-types</strong>. Elles s'écartent quand la volatilité augmente et se resserrent quand elle baisse.</p>
</x-simple>
<x-fig c="Les bandes enveloppent la plupart des prix ; leur écartement suit la volatilité.">""" + SCHEMA_BOLL + r"""</x-fig>
<x-approfondi>
<div class="formule">Bande haute = SMA 20 + 2 × écart-type ; bande basse = SMA 20 − 2 × écart-type</div>
<div class="formule">Largeur (bandwidth) = (bande haute − bande basse) ÷ SMA ; %B = (prix − bande basse) ÷ (bande haute − bande basse)</div>
<p>Si les rendements suivaient une loi normale, environ 95 % des prix seraient entre les bandes. Ce n'est qu'une approximation : les prix ne sont pas normalement distribués et les sorties de bandes sont plus fréquentes et plus violentes. Un prix qui « touche la bande haute » n'est pas automatiquement trop cher : en forte tendance, il peut « marcher sur la bande ».</p>
<p>Le <strong>squeeze</strong> (bandes très resserrées) signale une volatilité anormalement faible, souvent suivie d'un mouvement plus ample… dont il ne dit pas le sens.</p>
</x-approfondi>
<x-exemple>
<div class="calcul">SMA 20 = 100,00 ; écart-type des 20 dernières clôtures = 2,00
Bande haute = 100 + 2 × 2 = 104,00 ; bande basse = 100 − 4 = 96,00
Largeur = (104 − 96) ÷ 100 = 8 %
Prix à 103,00 : %B = (103 − 96) ÷ (104 − 96) = 7 ÷ 8 = 0,875 (dans le haut des bandes)</div>
</x-exemple>
<x-erreurs><ul><li>Vendre chaque contact avec la bande haute en tendance haussière.</li><li>Croire qu'un squeeze indique le sens de la cassure à venir.</li></ul></x-erreurs>
<x-cles><ul><li>Moyenne 20 ± 2 écarts-types.</li><li>L'écartement mesure la volatilité ; le squeeze annonce un mouvement, pas sa direction.</li><li>Les « 95 % » supposent une loi normale : approximation grossière.</li></ul></x-cles>
<x-exo><p>SMA 20 = 50 ; écart-type = 1,5. Calculez les bandes. Le prix est à 46,5 : calculez le %B.</p>
<x-corr><div class="calcul">Bande haute = 50 + 3 = 53 ; bande basse = 50 − 3 = 47
%B = (46,5 − 47) ÷ (53 − 47) = −0,5 ÷ 6 ≈ −0,08</div><p>%B négatif : le prix est sous la bande basse.</p></x-corr></x-exo>
"""),

("6-7", "L'ATR (Average True Range)", r"""
<x-obj><ul><li>Calculer le « true range » et l'ATR.</li><li>Utiliser l'ATR pour placer un stop et dimensionner une position.</li></ul></x-obj>
<x-simple>
<p>L'<strong>ATR</strong> (Wilder) mesure l'amplitude moyenne des bougies, en tenant compte des gaps. Il ne dit rien du sens du marché : c'est une <strong>mesure de volatilité</strong>, exprimée en unités de prix. C'est l'un des indicateurs les plus utiles pour la <strong>gestion du risque</strong>.</p>
</x-simple>
<x-fig c="L'ATR augmente quand les bougies s'agrandissent (marché agité) et diminue quand le marché se calme.">""" + SCHEMA_ATR + r"""</x-fig>
<x-approfondi>
<div class="formule">True Range = max(Haut − Bas ; |Haut − Clôture précédente| ; |Bas − Clôture précédente|)</div>
<p>L'ATR est la moyenne (lissée à la manière de Wilder) du true range sur 14 périodes. Usages : placer un stop à un multiple de l'ATR (par exemple 1,5 à 3 ATR) pour qu'il soit hors du « bruit » habituel ; comparer la volatilité actuelle à la volatilité passée ; adapter la taille de position à la volatilité (module 9).</p>
</x-approfondi>
<x-exemple>
<p>Clôture de la veille : 50,00. Bougie du jour : plus haut 53,00, plus bas 51,50 (ouverture en gap haussier).</p>
<div class="calcul">Haut − Bas = 53,00 − 51,50 = 1,50
|Haut − clôture précédente| = |53,00 − 50,00| = 3,00
|Bas − clôture précédente| = |51,50 − 50,00| = 1,50
True Range = 3,00 (le gap est pris en compte)
Stop à 2 ATR avec ATR = 1,20 : distance = 2,40 €. Achat à 52,00 → stop à 49,60 €
Pour risquer 120 € : taille = 120 ÷ 2,40 = 50 actions</div>
</x-exemple>
<x-erreurs><ul><li>Lire l'ATR comme un indicateur de direction.</li><li>Garder le même stop en euros quand l'ATR double : il sera touché par le simple bruit.</li></ul></x-erreurs>
<x-cles><ul><li>True Range intègre les gaps ; ATR = moyenne du True Range.</li><li>Mesure de volatilité, pas de direction.</li><li>Outil clé pour placer les stops et dimensionner les positions.</li></ul></x-cles>
<x-exo><p>Clôture précédente 80,00 ; bougie : haut 79,20, bas 76,50. Calculez le True Range. Avec un ATR de 2,00 et un stop à 1,5 ATR pour une vente à découvert à 77,00, où placer le stop ?</p>
<x-corr><div class="calcul">Haut − Bas = 2,70 ; |79,20 − 80| = 0,80 ; |76,50 − 80| = 3,50 → TR = 3,50
Stop = 77,00 + 1,5 × 2,00 = 80,00 €</div></x-corr></x-exo>
"""),

("6-8", "Le VWAP", r"""
<x-obj><ul><li>Calculer un prix moyen pondéré par les volumes.</li><li>Comprendre l'usage du VWAP en intraday.</li></ul></x-obj>
<x-simple>
<p>Le <strong>VWAP</strong> (Volume Weighted Average Price) est le prix moyen auquel l'actif s'est échangé depuis le début de la séance, en donnant plus de poids aux prix où beaucoup de volume a été échangé. Il repart de zéro chaque séance.</p>
</x-simple>
<x-fig c="Le VWAP (orange) intègre toute la séance : il bouge de moins en moins à mesure que le volume cumulé augmente.">""" + SCHEMA_VWAP + r"""</x-fig>
<x-approfondi>
<div class="formule">VWAP = Σ (prix typique × volume) ÷ Σ volume, avec prix typique = (Haut + Bas + Clôture) ÷ 3</div>
<p>Les institutionnels l'utilisent comme <strong>référence d'exécution</strong> : un gros ordre acheté sous le VWAP de la séance est considéré comme bien exécuté. Les day traders s'en servent comme repère : prix au-dessus du VWAP = acheteurs dominants sur la séance. Il existe des VWAP « ancrés » sur un événement (début de semaine, publication de résultats).</p>
<p>Le VWAP a peu de sens sans volume fiable (Forex au comptant) ni sur des unités de temps supérieures à la journée.</p>
</x-approfondi>
<x-exemple>
<div class="calcul">Tranche 1 : prix typique 100,00 ; volume 2 000 → 200 000
Tranche 2 : prix typique 101,00 ; volume 3 000 → 303 000
Tranche 3 : prix typique  99,50 ; volume 1 000 →  99 500
VWAP = (200 000 + 303 000 + 99 500) ÷ (2 000 + 3 000 + 1 000) = 602 500 ÷ 6 000 ≈ 100,42
(La moyenne simple des trois prix serait 100,17 : le VWAP penche vers 101, où le volume était le plus fort.)</div>
</x-exemple>
<x-erreurs><ul><li>Utiliser le VWAP sur le Forex au comptant avec un volume de ticks.</li><li>Comparer le VWAP d'aujourd'hui à un prix de la veille.</li></ul></x-erreurs>
<x-cles><ul><li>VWAP = prix moyen pondéré par les volumes depuis l'ouverture.</li><li>Référence d'exécution des institutionnels, repère intraday.</li><li>Repart de zéro chaque séance (sauf VWAP ancré).</li></ul></x-cles>
<x-exo><p>Deux tranches : 4 000 titres à 20,00 € et 1 000 titres à 21,00 €. Calculez le VWAP et la moyenne simple.</p>
<x-corr><div class="calcul">VWAP = (4 000 × 20 + 1 000 × 21) ÷ 5 000 = (80 000 + 21 000) ÷ 5 000 = 20,20 €
Moyenne simple = (20 + 21) ÷ 2 = 20,50 €</div></x-corr></x-exo>
"""),

("6-9", "Ichimoku (introduction)", r"""
<x-obj><ul><li>Connaître les cinq composantes d'Ichimoku.</li><li>Calculer Tenkan, Kijun et les bords du nuage.</li></ul></x-obj>
<x-simple>
<p><strong>Ichimoku Kinko Hyo</strong> (« équilibre en un coup d'œil »), développé par Goichi Hosoda, superpose plusieurs lignes au graphique pour résumer la tendance, l'élan et des zones de support et de résistance. Il paraît complexe, mais chaque ligne est un simple calcul de <strong>milieu d'amplitude</strong>.</p>
</x-simple>
<x-approfondi>
<ul><li><strong>Tenkan-sen</strong> = (plus haut 9 + plus bas 9) ÷ 2 : ligne rapide.</li>
<li><strong>Kijun-sen</strong> = (plus haut 26 + plus bas 26) ÷ 2 : ligne de référence.</li>
<li><strong>Senkou Span A</strong> = (Tenkan + Kijun) ÷ 2, <strong>décalée de 26 périodes vers l'avant</strong>.</li>
<li><strong>Senkou Span B</strong> = (plus haut 52 + plus bas 52) ÷ 2, décalée de 26 périodes vers l'avant.</li>
<li>Entre A et B se forme le <strong>nuage</strong> (Kumo).</li>
<li><strong>Chikou Span</strong> = clôture actuelle, tracée 26 périodes en arrière.</li></ul>
<p>Lecture de base : prix au-dessus du nuage = contexte haussier ; sous le nuage = baissier ; dans le nuage = indécision. Un nuage épais est considéré comme une zone de support ou de résistance plus forte. Les paramètres 9/26/52 viennent de l'époque des semaines de 6 jours ; certains traders les adaptent, d'autres non.</p>
</x-approfondi>
<x-fig c="Ichimoku sur la série de référence (le nuage est ici affiché sur la partie calculable de l'historique).">""" + SCHEMA_ICHI + r"""</x-fig>
<x-exemple>
<div class="calcul">9 dernières périodes : plus haut 110, plus bas 100 → Tenkan = (110 + 100) ÷ 2 = 105
26 dernières : plus haut 112, plus bas 96 → Kijun = (112 + 96) ÷ 2 = 104
Senkou A = (105 + 104) ÷ 2 = 104,5 (tracée 26 périodes plus loin)
52 dernières : plus haut 115, plus bas 90 → Senkou B = 102,5 (tracée 26 périodes plus loin)
Prix actuel 107 &gt; 104,5 et &gt; 102,5 → prix au-dessus du nuage projeté</div>
</x-exemple>
<x-erreurs><ul><li>Utiliser Ichimoku sans comprendre les décalages (le nuage « d'aujourd'hui » a été calculé il y a 26 périodes).</li><li>Ajouter Ichimoku à cinq autres indicateurs de tendance : redondance garantie.</li></ul></x-erreurs>
<x-cles><ul><li>Tenkan (9), Kijun (26) : milieux d'amplitude.</li><li>Nuage : Senkou A et B projetées 26 périodes en avant.</li><li>Prix au-dessus / dans / sous le nuage = contexte haussier / neutre / baissier.</li></ul></x-cles>
<x-exo><p>Sur 9 périodes : haut 48, bas 44. Sur 26 : haut 50, bas 40. Calculez Tenkan, Kijun et Senkou A. La Tenkan est-elle au-dessus de la Kijun ?</p>
<x-corr><div class="calcul">Tenkan = (48 + 44) ÷ 2 = 46
Kijun = (50 + 40) ÷ 2 = 45
Senkou A = (46 + 45) ÷ 2 = 45,5</div><p>Oui, la Tenkan (46) est au-dessus de la Kijun (45) : l'élan récent est plutôt haussier.</p></x-corr></x-exo>
"""),

("6-10", "Les retracements de Fibonacci", r"""
<x-obj><ul><li>Tracer et calculer les niveaux de retracement de Fibonacci.</li><li>Connaître les limites théoriques de cet outil.</li></ul></x-obj>
<x-simple>
<p>Après un mouvement, le prix revient souvent en partie en arrière avant de repartir. Les <strong>retracements de Fibonacci</strong> proposent des niveaux où ce repli pourrait s'arrêter : <strong>23,6 %, 38,2 %, 50 %, 61,8 % et 78,6 %</strong> du mouvement précédent. Les ratios viennent de la suite de Fibonacci (1, 1, 2, 3, 5, 8, 13…), où le rapport entre deux termes successifs tend vers 0,618.</p>
</x-simple>
<x-fig c="Niveaux de retracement d'une hausse de 80 à 120. Le niveau de 50 % ne provient pas de la suite de Fibonacci, mais il est traditionnellement ajouté.">""" + SCHEMA_FIBO + r"""</x-fig>
<x-note><p>Il n'existe <strong>pas de fondement théorique solide</strong> expliquant pourquoi les marchés respecteraient ces ratios plutôt que d'autres, et les études qui les ont testés ne montrent pas de supériorité claire sur des niveaux choisis au hasard. Leur éventuelle utilité tient surtout à leur popularité (beaucoup de traders regardent les mêmes niveaux) et au fait qu'avec 5 niveaux, il y en a presque toujours un près de l'endroit où le prix s'arrête. Utilisez-les, si vous le souhaitez, comme des repères de zone combinés avec d'autres éléments (supports, moyennes), pas comme des niveaux magiques.</p></x-note>
<x-approfondi>
<div class="formule">Niveau (hausse) = Sommet − (Sommet − Creux) × ratio ; Niveau (baisse) = Creux + (Sommet − Creux) × ratio</div>
<p>Le choix des points de départ (quel creux, quel sommet ?) est subjectif et change tous les niveaux. Il existe aussi des « extensions » (127,2 %, 161,8 %) utilisées comme objectifs.</p>
</x-approfondi>
<x-exemple>
<p>Hausse de 80 à 120 (amplitude 40).</p>
<div class="calcul">23,6 % : 120 − 40 × 0,236 = 120 − 9,44 = 110,56
38,2 % : 120 − 40 × 0,382 = 120 − 15,28 = 104,72
50 %   : 120 − 40 × 0,500 = 100,00
61,8 % : 120 − 40 × 0,618 = 120 − 24,72 = 95,28
78,6 % : 120 − 40 × 0,786 = 120 − 31,44 = 88,56</div>
</x-exemple>
<x-erreurs><ul><li>Attribuer un pouvoir « naturel » ou « mathématique » à ces niveaux.</li><li>Retracer les niveaux à partir d'autres points jusqu'à ce qu'ils « collent » au graphique.</li></ul></x-erreurs>
<x-cles><ul><li>Niveaux : 23,6 ; 38,2 ; 50 ; 61,8 ; 78,6 %.</li><li>Calcul : sommet − amplitude × ratio (pour une hausse).</li><li>Fondement théorique faible ; à utiliser comme zones parmi d'autres repères.</li></ul></x-cles>
<x-exo><p>Baisse de 250 à 190. Calculez les retracements de 38,2 % et 61,8 % (niveaux où une remontée pourrait s'arrêter).</p>
<x-corr><div class="calcul">Amplitude = 60
38,2 % : 190 + 60 × 0,382 = 190 + 22,92 = 212,92
61,8 % : 190 + 60 × 0,618 = 190 + 37,08 = 227,08</div></x-corr></x-exo>
"""),

("6-11", "Les divergences", r"""
<x-obj><ul><li>Reconnaître une divergence haussière ou baissière.</li><li>Comprendre pourquoi une divergence n'est pas un signal d'entrée en soi.</li></ul></x-obj>
<x-simple>
<p>Il y a <strong>divergence</strong> quand le prix et un oscillateur (RSI, MACD, stochastique) ne racontent pas la même histoire :</p>
<ul><li><strong>Divergence baissière</strong> : le prix fait un sommet plus haut, mais l'oscillateur fait un sommet plus bas. L'élan de la hausse faiblit.</li>
<li><strong>Divergence haussière</strong> : le prix fait un creux plus bas, mais l'oscillateur fait un creux plus haut. La baisse s'essouffle.</li></ul>
</x-simple>
<x-fig c="Le prix monte plus haut au second sommet, mais le RSI ne confirme pas : divergence baissière, suivie ici d'une baisse.">""" + SCHEMA_DIV + r"""</x-fig>
<x-approfondi>
<p>Une divergence signale un <strong>ralentissement</strong>, pas un retournement. En tendance forte, on peut observer plusieurs divergences successives sans que la tendance s'arrête. Beaucoup de traders attendent une confirmation par le prix (cassure d'une ligne de tendance, rupture de structure) avant d'agir. Il existe aussi des divergences « cachées », interprétées comme des signaux de continuation.</p>
<p>L'exemple ci-dessus a été choisi parce qu'il illustre bien la notion : c'est exactement le biais rétrospectif décrit au module 5. Sur un historique complet, de nombreuses divergences n'aboutissent à rien.</p>
</x-approfondi>
<x-exemple>
<div class="calcul">""" + DIV_TXT + r"""</div>
</x-exemple>
<x-erreurs><ul><li>Vendre dès la première divergence dans une tendance forte.</li><li>Ne retenir que les divergences qui ont « fonctionné » quand on les étudie après coup.</li></ul></x-erreurs>
<x-cles><ul><li>Divergence = désaccord entre le prix et l'oscillateur.</li><li>Elle signale un essoufflement, pas un retournement.</li><li>Attendre une confirmation par le prix.</li></ul></x-cles>
<x-exo><p>Le prix fait un creux à 45, puis un creux plus bas à 43. Le MACD fait un creux à −1,2 puis à −0,7. De quelle divergence s'agit-il ? Que faut-il attendre avant d'acheter ?</p>
<x-corr><p>Prix : creux plus bas ; MACD : creux plus haut → <strong>divergence haussière</strong>. Il faut attendre une confirmation par le prix : par exemple, la cassure du dernier sommet intermédiaire ou d'une ligne de tendance baissière, avec un stop sous 43.</p></x-corr></x-exo>
"""),

("6-12", "Le piège de la surcharge d'indicateurs", r"""
<x-obj><ul><li>Comprendre pourquoi multiplier les indicateurs n'augmente pas l'information.</li><li>Construire un ensemble d'outils simple et complémentaire.</li></ul></x-obj>
<x-simple>
<p>Les débutants empilent souvent cinq, dix indicateurs sur leur graphique en pensant que « quand tous sont d'accord, le signal est fiable ». Mais la plupart des indicateurs sont calculés sur les <strong>mêmes prix</strong> avec des formules proches : ils disent la même chose. Leur accord n'est pas une confirmation indépendante, c'est un écho.</p>
</x-simple>
<x-fig c="Sur notre série de référence, le RSI et le stochastique évoluent presque ensemble : leur accord n'apporte presque aucune information supplémentaire.">""" + SCHEMA_REDONDANCE + r"""</x-fig>
<x-approfondi>
<p>Principe d'un ensemble cohérent : <strong>un outil par question</strong>.</p>
""" + table(["Question", "Exemples d'outils (en choisir un)"],
            [["Quel est le contexte, la tendance ?", "Structure de marché, une moyenne mobile, Ichimoku"],
             ["Où sont les zones de décision ?", "Supports / résistances, VWAP, éventuellement Fibonacci"],
             ["Quel est l'élan ?", "RSI ou stochastique ou MACD (un seul)"],
             ["Quelle est la volatilité, où placer le stop ?", "ATR ou Bollinger"]]) + r"""
<p>Plus on ajoute de conditions, plus on risque aussi le <strong>surapprentissage</strong> : une combinaison parfaitement ajustée au passé, qui ne fonctionne plus ensuite (module 10). Et un graphique surchargé favorise le biais de confirmation : on trouve toujours un indicateur qui valide ce qu'on voulait faire.</p>
</x-approfondi>
<x-exemple>
<p>Sur la série de référence de ce module, on mesure la corrélation entre le RSI 14 et le stochastique %K 14 :</p>
<div class="calcul">Corrélation ≈ """ + f"{CORR:.2f}".replace(".", ",") + r""" (1 = évolution identique, 0 = aucun lien)</div>
<p>Avec une corrélation aussi élevée, attendre que « le RSI <em>et</em> le stochastique » confirment revient presque à regarder deux fois le même indicateur. Imaginons maintenant 4 indicateurs indépendants qui donneraient chacun un bon signal 55 % du temps : leur accord unanime serait rare, mais informatif. Avec 4 indicateurs presque identiques, l'accord est fréquent et n'apporte presque rien de plus qu'un seul.</p>
</x-exemple>
<x-erreurs><ul><li>Ajouter un indicateur après chaque perte « pour filtrer ».</li><li>Utiliser RSI, stochastique, CCI et Williams %R ensemble.</li><li>Ne plus voir le prix lui-même derrière les indicateurs.</li></ul></x-erreurs>
<x-cles><ul><li>Les indicateurs sont dérivés du prix et souvent très corrélés entre eux.</li><li>Un outil par question : contexte, zones, élan, volatilité.</li><li>Moins de règles = moins de surapprentissage et plus de clarté.</li></ul></x-cles>
<x-exo><p>Un trader utilise : EMA 20, EMA 50, MACD, RSI, stochastique, Bollinger et ATR. Proposez une version simplifiée à 3 ou 4 outils, en justifiant.</p>
<x-corr><p>Exemple : <strong>EMA 50</strong> pour le contexte (le MACD est construit à partir de moyennes : redondant) ; <strong>supports / résistances</strong> tracés à la main pour les zones ; <strong>RSI</strong> pour l'élan (le stochastique est redondant) ; <strong>ATR</strong> pour placer le stop et dimensionner (Bollinger mesure aussi la volatilité : redondant). Il n'y a pas une seule bonne réponse : l'important est qu'aucun outil ne fasse double emploi.</p></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Familles</h2><ul><li>Tendance : MM, MACD, Ichimoku.</li><li>Oscillateurs : RSI, stochastique.</li><li>Volatilité : ATR, Bollinger. Volume : VWAP.</li><li>Tous retardés, tous dérivés du prix.</li></ul></div>
<div class="encadre"><h2>Moyennes mobiles</h2><ul><li>SMA = moyenne des N clôtures.</li><li>EMA : k = 2 ÷ (N + 1) ; EMA = C × k + EMA<sub>préc</sub> × (1 − k).</li><li>Retard SMA ≈ (N − 1) ÷ 2 périodes.</li></ul></div>
<div class="encadre"><h2>MACD</h2><ul><li>EMA 12 − EMA 26 ; signal = EMA 9 ; histogramme = MACD − signal.</li></ul></div>
<div class="encadre"><h2>RSI &amp; stochastique</h2><ul><li>RSI = 100 − 100 ÷ (1 + RS) ; zones 70/30.</li><li>%K = (C − Bas<sub>N</sub>) ÷ (Haut<sub>N</sub> − Bas<sub>N</sub>) × 100 ; zones 80/20.</li><li>Surachat ≠ signal de vente.</li></ul></div>
<div class="encadre"><h2>Volatilité</h2><ul><li>Bollinger : SMA 20 ± 2 écarts-types ; squeeze = mouvement à venir, sens inconnu.</li><li>TR = max(H − B ; |H − C<sub>préc</sub>| ; |B − C<sub>préc</sub>|) ; ATR = moyenne.</li><li>Stop à k × ATR ; taille = risque ÷ distance.</li></ul></div>
<div class="encadre"><h2>VWAP &amp; Ichimoku</h2><ul><li>VWAP = Σ(prix typique × volume) ÷ Σ volume, par séance.</li><li>Tenkan (9), Kijun (26), nuage décalé de 26, Chikou.</li></ul></div>
<div class="encadre"><h2>Fibonacci</h2><ul><li>23,6 / 38,2 / 50 / 61,8 / 78,6 %.</li><li>Niveau = sommet − amplitude × ratio.</li><li>Fondement théorique faible.</li></ul></div>
<div class="encadre"><h2>Divergences &amp; surcharge</h2><ul><li>Divergence = essoufflement, à confirmer par le prix.</li><li>Un outil par question ; RSI et stochastique très corrélés.</li></ul></div>
"""

QUIZ = [
("Clôtures : 20, 22, 21, 23, 24. Moyenne mobile simple sur 5 ?", ["21", "22", "23", "22,5"], 1, "(20 + 22 + 21 + 23 + 24) ÷ 5 = 110 ÷ 5 = 22."),
("Coefficient k d'une EMA 19 :", ["0,05", "0,10", "0,19", "0,5"], 1, "k = 2 ÷ (19 + 1) = 0,10."),
("La ligne MACD est égale à :", ["EMA 26 − EMA 12", "EMA 12 − EMA 26", "SMA 12 − SMA 26", "EMA 9 du prix"], 1, "MACD = EMA 12 − EMA 26 ; la ligne de signal est l'EMA 9 du MACD."),
("Moyenne des hausses 1,2, des baisses 0,4. RSI ?", ["25", "60", "75", "80"], 2, "RS = 3 ; RSI = 100 − 100 ÷ 4 = 75."),
("Un RSI à 78 en forte tendance haussière signifie :", ["Qu'il faut vendre immédiatement", "Que l'élan haussier est fort ; ce n'est pas en soi un signal de retournement", "Que le marché va s'effondrer", "Que l'indicateur est cassé"], 1, "Le surachat peut durer longtemps en tendance."),
("Haut 14 = 30, bas 14 = 20, clôture = 22. %K ?", ["20", "22", "45", "80"], 0, "(22 − 20) ÷ (30 − 20) × 100 = 20."),
("Bandes de Bollinger avec SMA 20 = 80 et écart-type = 2,5 :", ["77,5 / 82,5", "75 / 85", "70 / 90", "78 / 82"], 1, "80 ± 2 × 2,5 = 75 et 85."),
("Clôture précédente 40 ; bougie haut 44, bas 42,5. True Range ?", ["1,5", "2,5", "4", "4,5"], 2, "max(1,5 ; |44 − 40| = 4 ; |42,5 − 40| = 2,5) = 4."),
("Le VWAP est surtout utilisé :", ["Sur des graphiques mensuels", "Comme référence de prix moyen d'une séance, pondéré par les volumes", "Pour mesurer les taux d'intérêt", "Sur le Forex sans volume"], 1, "Il repart chaque séance et sert de référence d'exécution intraday."),
("Hausse de 60 à 100. Retracement de 61,8 % ?", ["75,28", "84,72", "61,80", "80,00"], 0, "100 − 40 × 0,618 = 100 − 24,72 = 75,28."),
("Le prix fait un sommet plus haut, le RSI un sommet plus bas : c'est", ["Une divergence haussière", "Une divergence baissière", "Un squeeze", "Un croisement doré"], 1, "Désaccord prix/oscillateur au sommet = divergence baissière (essoufflement)."),
("Pourquoi l'accord du RSI et du stochastique n'est-il pas une double confirmation ?", ["Parce qu'ils sont interdits ensemble", "Parce qu'ils sont calculés sur les mêmes prix et très corrélés", "Parce que le stochastique est toujours faux", "Parce que le RSI est un indicateur de volume"], 1, "Ils mesurent tous deux l'élan à partir des mêmes prix : leur accord est un écho, pas une information indépendante."),
("Ichimoku : la Kijun-sen est :", ["La clôture décalée de 26", "Le milieu de l'amplitude des 26 dernières périodes", "Une EMA 26", "Le milieu des 9 dernières"], 1, "Kijun = (plus haut 26 + plus bas 26) ÷ 2."),
]
