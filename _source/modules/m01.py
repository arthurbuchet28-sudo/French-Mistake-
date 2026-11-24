from svgkit import plot, table, svg, t, line, arrow, path_from, candles

NUM = 1
TITRE = "Les marchés financiers"
RESUME = "Actions, indices, obligations, Forex, matières premières, cryptos, ETF ; les acteurs, les horaires, la liquidité et la volatilité."
DUREE = "2 h 30"
INTRO = r"""<p>Un trader doit connaître son terrain de jeu. Ce module présente les grandes familles d'actifs, qui les échange, où et quand, ainsi que deux notions qui reviendront partout : la <strong>liquidité</strong> et la <strong>volatilité</strong>.</p>"""


def _courbe_obligation():
    xs = [i / 2 for i in range(1, 15)]  # 0,5 % à 7 %
    ys = [sum(30 / (1 + r / 100) ** k for k in range(1, 11)) + 1000 / (1 + r / 100) ** 10 for r in xs]
    return plot([{"x": xs, "y": ys, "cls": "g-l1", "label": "Prix d'une obligation 10 ans, coupon 3 %"}],
                label="Relation inverse entre taux du marché et prix d'une obligation",
                xlabel="Taux d'intérêt du marché (%)", yr=(600, 1300),
                xfmt=lambda v: f"{v:g} %".replace(".", ","),
                marks=[{"x": 3, "y": 1000, "t": "3 % → 1 000 €"}, {"x": 4, "y": 918.89, "t": "4 % → 918,89 €"},
                       {"x": 2, "y": 1089.83, "t": "2 % → 1 089,83 €"}],
                hlines=[{"y": 1000, "cls": "g-l3 g-fin"}])


SCHEMA_OBLIG = _courbe_obligation()


def _courbe_futures():
    m = [1, 2, 3, 4, 5, 6]
    return plot([{"x": m, "y": [80, 81.5, 82.8, 83.9, 84.8, 85.5], "cls": "g-l2", "label": "Contango : échéances lointaines plus chères"},
                 {"x": m, "y": [80, 79.1, 78.4, 77.9, 77.5, 77.2], "cls": "g-l4", "label": "Déport (backwardation) : échéances lointaines moins chères"}],
                label="Courbe des prix à terme en contango et en déport", xlabel="Échéance (mois)",
                yr=(74, 88), xticks=m, xfmt=lambda v: f"M{int(v)}")


SCHEMA_FUTURES = _courbe_futures()


def _etf_levier():
    idx, lev = [100], [100]
    moves = [10, -10, 10, -10, 10, -10, 10, -10]
    for mv in moves:
        idx.append(idx[-1] * (1 + mv / 100))
        lev.append(lev[-1] * (1 + 2 * mv / 100))
    x = list(range(len(idx)))
    return plot([{"x": x, "y": idx, "cls": "g-l1", "label": "Indice (+10 % / −10 % en alternance)"},
                 {"x": x, "y": lev, "cls": "g-lb", "label": "ETF à levier 2× quotidien"}],
                label="Érosion d'un ETF à levier quotidien dans un marché qui oscille", xlabel="Jours",
                yr=(60, 125), xticks=x, xfmt=lambda v: f"{int(v)}", hlines=[{"y": 100, "cls": "g-l3 g-fin"}],
                marks=[{"x": 8, "y": idx[-1], "t": f"{idx[-1]:.1f}".replace(".", ","), "dx": -40, "dy": -8},
                       {"x": 8, "y": lev[-1], "t": f"{lev[-1]:.1f}".replace(".", ","), "dx": -40, "dy": 16}])


SCHEMA_ETF = _etf_levier()


def _sessions():
    W, X0 = 680, 175
    sc = (W - X0 - 14) / 24
    rows = [("Tokyo (actions)", [(1, 7.5)], "g-rect-a"), ("Paris (Euronext)", [(9, 17.5)], "g-rect-h"),
            ("New York (actions)", [(15.5, 22)], "g-rect-b"), ("Session Forex Asie", [(0, 9)], "g-rect"),
            ("Session Forex Londres", [(9, 18)], "g-rect"), ("Session Forex New York", [(14, 23)], "g-rect")]
    p = []
    for h in range(0, 25, 3):
        x = X0 + h * sc
        p.append(line(x, 10, x, 214, "g-grille"))
        p.append(t(x, 230, f"{h}h", "g-txt g-petit", "middle"))
    for k, (nom, spans, cls) in enumerate(rows):
        y = 14 + k * 33
        p.append(t(X0 - 8, y + 16, nom, "g-txt", "end"))
        for a, b in spans:
            p.append(f'<rect x="{X0+a*sc:.1f}" y="{y}" width="{(b-a)*sc:.1f}" height="22" rx="4" class="{cls}"/>')
    p.append(f'<rect x="{X0+15.5*sc:.1f}" y="8" width="{2*sc:.1f}" height="206" class="g-zone"/>')
    p.append(t(X0 + 16.5 * sc, 250, "Chevauchement Paris / New York", "g-txt g-petit", "middle"))
    return svg(W, 258, "".join(p), "Horaires des principales places et sessions Forex, en heure de Paris (hiver)")


SCHEMA_SESSIONS = _sessions()

SCHEMA_VOL = candles(path_from([(0, 100), (40, 110)], seed=4, noise=0.3, wick=0.3), w=640, h=200,
                     label="Actif peu volatil", ymin=88, ymax=122)
SCHEMA_VOL2 = candles(path_from([(0, 100), (8, 115), (14, 95), (22, 118), (30, 98), (40, 110)], seed=7, noise=3.0, wick=2.2),
                      w=640, h=200, label="Actif très volatil", ymin=88, ymax=122)


def _acteurs():
    W = 660
    p = ['<rect x="250" y="95" width="160" height="60" rx="10" class="g-rect-a"/>',
         t(330, 120, "Marché", "g-txt g-fort", "middle"), t(330, 138, "(bourse, plateforme, gré à gré)", "g-txt g-petit", "middle")]
    acteurs = [(20, 10, "Banques centrales", "politique monétaire"), (240, 10, "Banques commerciales", "liquidité, change, clients"),
               (460, 10, "Institutionnels", "fonds, assureurs, retraites"), (20, 200, "Market makers / HFT", "cotent en continu"),
               (240, 200, "Entreprises", "couverture (change, matières)"), (460, 200, "Particuliers", "petite part des volumes")]
    for x, y, a, b in acteurs:
        p.append(f'<rect x="{x}" y="{y}" width="180" height="48" rx="8" class="g-rect"/>')
        p.append(t(x + 90, y + 21, a, "g-txt g-fort", "middle"))
        p.append(t(x + 90, y + 38, b, "g-txt g-petit", "middle"))
        cx, cy = x + 90, (y + 48 if y < 100 else y)
        tx, ty = 330 + (cx - 330) * 0.25, (95 if y < 100 else 155)
        p.append(arrow(cx, cy, tx, ty))
    return svg(W, 255, "".join(p), "Les principaux acteurs des marchés financiers")


SCHEMA_ACTEURS = _acteurs()

LECONS = [
("1-1", "Les actions et les indices", r"""
<x-obj><ul><li>Comprendre ce qu'est une action et pourquoi son prix varie.</li>
<li>Savoir comment est construit un indice boursier.</li>
<li>Distinguer indice de prix et indice de rendement.</li></ul></x-obj>

<x-simple>
<p>Une <strong>action</strong> est une part du capital d'une entreprise. L'actionnaire est copropriétaire : il peut recevoir une part des bénéfices (le <strong>dividende</strong>, si l'entreprise en verse) et voter en assemblée générale. Le prix d'une action varie selon l'offre et la demande, qui reflètent les anticipations des investisseurs sur les bénéfices futurs, les taux d'intérêt et le climat général.</p>
<p>Un <strong>indice</strong> est un « panier » d'actions qui résume l'évolution d'un marché : CAC 40 (40 grandes valeurs françaises), Euro Stoxx 50 (zone euro), DAX (Allemagne), [[S&amp;P 500|sp-500]] (500 grandes entreprises américaines), Nasdaq 100 (grandes valeurs non financières du Nasdaq, très technologique), Nikkei 225 (Japon)… Un indice ne s'achète pas directement : on le trade via des ETF, des futures ou des CFD.</p>
</x-simple>

<x-approfondi>
<p><strong>Pondération.</strong> La plupart des grands indices sont pondérés par la <strong>capitalisation boursière flottante</strong> : plus une entreprise vaut cher en bourse (en ne comptant que les actions réellement échangeables), plus elle pèse. Le CAC 40 plafonne en plus le poids de chaque valeur à 15 %. Exception notable : le Dow Jones et le Nikkei 225 sont pondérés par le <strong>prix</strong> de l'action, une méthode historique moins représentative.</p>
<p><strong>Indice de prix ou de rendement.</strong> Le CAC 40 « classique » est un indice de <em>prix</em> : quand une entreprise verse un dividende, son cours baisse d'autant et l'indice baisse aussi. Les versions « dividendes réinvestis » (CAC 40 GR, ou NR net de retenues fiscales) reflètent le rendement total. L'écart se cumule sur des décennies : comparer un fonds à un indice de prix flatte le fonds.</p>
<p><strong>Ce qui fait bouger une action</strong> : les résultats et perspectives de l'entreprise (module 7), les taux d'intérêt (plus ils montent, plus les bénéfices futurs valent moins aujourd'hui), le sentiment général du marché, les flux (achats et ventes massifs des fonds), les événements (rachat, scandale, régulation).</p>
</x-approfondi>

<x-exemple>
<p>Un indice simplifié contient trois entreprises pondérées par leur capitalisation :</p>
""" + table(["Entreprise", "Capitalisation", "Poids", "Variation du jour", "Contribution"],
            [["A", "600 Md€", "600 ÷ 1 000 = 60 %", "+2 %", "60 % × 2 % = +1,2 %"],
             ["B", "300 Md€", "30 %", "−1 %", "30 % × (−1 %) = −0,3 %"],
             ["C", "100 Md€", "10 %", "+5 %", "10 % × 5 % = +0,5 %"],
             ["<strong>Total</strong>", "1 000 Md€", "100 %", "", "<strong>+1,4 %</strong>"]]) + r"""
<p>L'entreprise C a le plus progressé (+5 %), mais c'est A, la plus grosse, qui contribue le plus à la hausse de l'indice. Si l'indice valait 7 500 points la veille, il termine à 7 500 × 1,014 = <strong>7 605 points</strong>.</p>
</x-exemple>

<x-erreurs><ul>
<li>Croire qu'un indice représente « l'économie » : il ne représente que les grandes entreprises cotées qui le composent, et souvent quelques poids lourds dominent.</li>
<li>Comparer un placement à un indice de prix sans tenir compte des dividendes.</li>
<li>Penser qu'une action « pas chère » en euros (5 €) monte plus facilement qu'une action à 500 € : le prix unitaire n'a aucun sens seul, seule compte la valorisation totale (module 7).</li>
</ul></x-erreurs>
<x-cles><ul><li>Une action est une part d'entreprise ; un indice est un panier d'actions.</li>
<li>Dans un indice pondéré par la capitalisation, les plus grosses valeurs dominent les mouvements.</li>
<li>Indice de prix ≠ indice dividendes réinvestis.</li></ul></x-cles>
<x-exo><p>Reprenez l'indice de l'exemple. Le lendemain, A fait −1 %, B +4 %, C −3 %. Quelle est la variation de l'indice (en gardant les poids 60/30/10) ?</p>
<x-corr><div class="calcul">60 % × (−1 %) = −0,6 %
30 % × (+4 %) = +1,2 %
10 % × (−3 %) = −0,3 %
Total = −0,6 + 1,2 − 0,3 = +0,3 %</div>
<p>L'indice gagne 0,3 %. (En toute rigueur, les poids changent légèrement chaque jour avec les cours ; l'approximation est très bonne sur une journée.)</p></x-corr></x-exo>
"""),

("1-2", "Les obligations", r"""
<x-obj><ul><li>Comprendre le fonctionnement d'une obligation (nominal, coupon, échéance).</li>
<li>Savoir pourquoi le prix d'une obligation baisse quand les taux montent.</li></ul></x-obj>
<x-simple>
<p>Une <strong>obligation</strong> est un prêt découpé en titres. L'émetteur (un État, une entreprise) emprunte une somme, verse des intérêts réguliers appelés <strong>coupons</strong>, puis rembourse le <strong>nominal</strong> à l'échéance. Exemple : une obligation de nominal 1 000 € à 10 ans avec un coupon de 3 % verse 30 € par an pendant 10 ans, puis 1 000 €.</p>
<p>Une obligation se revend sur le marché avant son échéance. Son prix varie, principalement en fonction des <strong>taux d'intérêt</strong> et de la <strong>qualité de l'émetteur</strong> (risque qu'il ne rembourse pas).</p>
</x-simple>
<x-approfondi>
<p><strong>Pourquoi le prix baisse quand les taux montent ?</strong> Si de nouvelles obligations équivalentes rapportent désormais 4 %, plus personne ne voudra payer 1 000 € pour une ancienne obligation qui ne rapporte que 3 %. Son prix baisse jusqu'à ce que son rendement redevienne comparable. Le prix d'une obligation est la somme de ses flux futurs actualisés au taux du marché :</p>
<div class="formule">Prix = Σ Coupon ÷ (1 + taux)<sup>t</sup> + Nominal ÷ (1 + taux)<sup>n</sup></div>
<p>Plus l'échéance est lointaine, plus le prix est sensible aux variations de taux. Cette sensibilité se mesure par la <strong>duration</strong>. Les traders suivent surtout les <strong>rendements</strong> des emprunts d'État (le « 10 ans » américain, le Bund allemand, l'OAT française), car ils influencent tous les autres marchés. L'écart de rendement entre l'OAT et le Bund (le « spread OAT-Bund ») est par exemple surveillé comme indicateur du risque perçu sur la France.</p>
</x-approfondi>
<x-exemple>
<p><strong>Cas simple (1 an).</strong> Une obligation rembourse 1 000 € + 30 € de coupon dans un an. Les taux du marché passent à 4 %. Quel prix un acheteur est-il prêt à payer ?</p>
<div class="calcul">Prix = 1 030 ÷ 1,04 = 990,38 €
Vérification : 990,38 × 1,04 = 1 030 €, soit bien un rendement de 4 %</div>
<p><strong>Cas 10 ans.</strong> Même obligation (coupon 3 %) mais 10 ans avant l'échéance. En actualisant les 10 coupons et le nominal :</p>
<div class="calcul">Taux du marché à 4 % → prix ≈ 918,89 € (−8,1 %)
Taux du marché à 2 % → prix ≈ 1 089,83 € (+9,0 %)</div>
<p>Une hausse d'un point des taux fait perdre environ 0,96 % à l'obligation à 1 an, mais 8,1 % à l'obligation à 10 ans : l'échéance longue amplifie le risque de taux.</p>
</x-exemple>
<x-fig c="Prix d'une obligation à 10 ans de coupon 3 % selon le taux du marché : la relation est inverse et légèrement courbe (convexité).">""" + SCHEMA_OBLIG + r"""</x-fig>
<x-erreurs><ul><li>Croire qu'une obligation est « sans risque » : son prix peut fortement baisser si les taux montent (2022 en a été un exemple marquant), et l'émetteur peut faire défaut.</li>
<li>Confondre le taux du coupon (fixe) et le rendement (qui dépend du prix payé).</li></ul></x-erreurs>
<x-cles><ul><li>Obligation = prêt ; coupons + remboursement du nominal.</li>
<li>Taux en hausse ⇒ prix des obligations existantes en baisse, et inversement.</li>
<li>Plus l'échéance est longue, plus la sensibilité aux taux est forte.</li></ul></x-cles>
<x-exo><p>Une obligation rembourse 1 000 € + 50 € de coupon dans un an. Les taux du marché sont à 3 %. Quel est son prix ? Et si les taux tombent à 2 % ?</p>
<x-corr><div class="calcul">À 3 % : 1 050 ÷ 1,03 = 1 019,42 €
À 2 % : 1 050 ÷ 1,02 = 1 029,41 €</div><p>La baisse des taux fait monter le prix de l'obligation, d'environ 1 %.</p></x-corr></x-exo>
"""),

("1-3", "Le marché des changes (Forex)", r"""
<x-obj><ul><li>Lire une paire de devises et une cotation.</li><li>Comprendre ce que signifie acheter ou vendre une paire.</li><li>Calculer un gain en devise de cotation puis en euros.</li></ul></x-obj>
<x-simple>
<p>Le <strong>Forex</strong> (FX, foreign exchange) est le marché où s'échangent les devises. C'est le plus grand marché du monde : de l'ordre de 7 500 milliards de dollars échangés <em>par jour</em> selon l'enquête triennale 2022 de la Banque des règlements internationaux (BRI), et davantage encore dans l'enquête 2025. Il fonctionne 24 h/24, du dimanche soir au vendredi soir, de gré à gré (sans bourse centrale).</p>
<p>On y traite toujours une <strong>paire</strong> : EUR/USD = 1,0850 signifie que <strong>1 euro vaut 1,0850 dollar</strong>. La première devise est la <strong>devise de base</strong>, la seconde la <strong>devise de cotation</strong>. Acheter EUR/USD, c'est acheter des euros en vendant des dollars : on gagne si l'euro s'apprécie face au dollar.</p>
</x-simple>
<x-approfondi>
<p><strong>Les catégories de paires</strong> :</p>
<ul><li><strong>Majeures</strong> : paires avec le dollar américain parmi les devises les plus échangées : EUR/USD, USD/JPY, GBP/USD, USD/CHF, AUD/USD, USD/CAD, NZD/USD. Spreads les plus faibles.</li>
<li><strong>Croisées (crosses)</strong> : sans le dollar, par exemple EUR/GBP, EUR/JPY.</li>
<li><strong>Exotiques</strong> : une devise majeure contre une devise émergente (USD/TRY, EUR/ZAR…). Spreads larges, mouvements brutaux.</li></ul>
<p>Le dollar figure dans environ 9 transactions de change sur 10. Les cours des devises dépendent surtout des <strong>écarts de taux d'intérêt</strong> entre pays, de l'inflation, de la croissance, des flux commerciaux et de l'aversion au risque (module 7). L'unité de mouvement s'appelle le <strong>pip</strong> (0,0001 pour la plupart des paires, 0,01 pour les paires en yen) : nous la détaillerons au module 3.</p>
</x-approfondi>
<x-exemple>
<p>Vous achetez 10 000 € contre des dollars à 1,0850, puis revendez à 1,0920.</p>
<div class="calcul">Achat  : 10 000 € coûtent 10 000 × 1,0850 = 10 850 $
Vente  : 10 000 € rapportent 10 000 × 1,0920 = 10 920 $
Gain   : 10 920 − 10 850 = 70 $ (le gain est en devise de cotation)
En euros, au cours de sortie : 70 ÷ 1,0920 ≈ 64,10 €
Mouvement : 1,0920 − 1,0850 = 0,0070 = 70 pips</div>
<p>Sur 10 000 €, le gain est modeste (≈ 0,64 %) : les devises majeures bougent peu en pourcentage. C'est pourquoi le Forex est très souvent tradé avec effet de levier… ce qui augmente d'autant le risque (module 3).</p>
</x-exemple>
<x-erreurs><ul><li>Inverser le sens : « EUR/USD monte » veut dire que l'euro se renforce face au dollar, pas l'inverse.</li>
<li>Oublier que le gain ou la perte est exprimé dans la devise de cotation, et qu'il faut le convertir.</li>
<li>Croire que le Forex est « plus simple » parce qu'il n'y a que quelques paires : c'est l'un des marchés les plus efficients, dominé par les professionnels.</li></ul></x-erreurs>
<x-cles><ul><li>Une paire = devise de base / devise de cotation ; le cours indique combien d'unités de cotation vaut 1 unité de base.</li>
<li>Acheter la paire = parier sur la hausse de la devise de base.</li><li>Résultat en devise de cotation, à convertir dans la devise du compte.</li></ul></x-cles>
<x-exo><p>Vous vendez 20 000 £ contre des dollars sur GBP/USD à 1,2700 et rachetez à 1,2640. Calculez le résultat en dollars, puis en livres au cours de sortie.</p>
<x-corr><div class="calcul">Vente : 20 000 × 1,2700 = 25 400 $ reçus
Rachat : 20 000 × 1,2640 = 25 280 $ payés
Gain : 25 400 − 25 280 = 120 $ (la livre a baissé, la vente était gagnante)
En livres : 120 ÷ 1,2640 ≈ 94,94 £</div></x-corr></x-exo>
"""),

("1-4", "Les matières premières", r"""
<x-obj><ul><li>Connaître les grandes familles de matières premières.</li><li>Comprendre pourquoi on les trade surtout via des contrats à terme.</li><li>Découvrir le contango, le déport et le coût du « roll ».</li></ul></x-obj>
<x-simple>
<p>Les <strong>matières premières</strong> (commodities) se répartissent en grandes familles : l'<strong>énergie</strong> (pétrole Brent et WTI, gaz naturel), les <strong>métaux précieux</strong> (or, argent, platine), les <strong>métaux industriels</strong> (cuivre, aluminium, nickel) et les <strong>produits agricoles</strong> (blé, maïs, soja, café, cacao, sucre).</p>
<p>Un particulier ne stocke pas de barils de pétrole. Les matières premières se traitent donc surtout via des <strong>contrats à terme</strong> (futures : achat ou vente à une date future, module 3), des ETC/ETF, ou des CFD qui répliquent ces contrats.</p>
</x-simple>
<x-approfondi>
<p>Pour une même matière, il existe plusieurs contrats à terme d'échéances différentes. Leurs prix forment une <strong>courbe</strong> :</p>
<ul><li><strong>Contango</strong> : les échéances lointaines sont plus chères que les proches (coût du stockage, de l'assurance, du financement). Situation fréquente.</li>
<li><strong>Déport</strong> (backwardation) : les échéances proches sont plus chères, souvent quand il y a une pénurie immédiate.</li></ul>
<p>Quand un fonds ou un CFD doit passer d'une échéance qui expire à la suivante (le <strong>roll</strong>), il revend le contrat proche et achète le suivant. En contango, il achète plus cher à chaque roll : cela crée un coût régulier, même si le prix « au comptant » ne bouge pas. C'est pourquoi certains produits sur le pétrole ou le gaz ont durablement sous-performé le cours affiché dans les médias.</p>
<p>Cas extrême : le 20 avril 2020, le contrat WTI échéance mai a clôturé à <strong>−37,63 $</strong> le baril. À l'approche de la livraison, les détenteurs ne pouvaient pas stocker physiquement le pétrole et ont payé pour s'en débarrasser. Un prix négatif était jugé impossible par beaucoup de plateformes.</p>
</x-approfondi>
<x-fig c="Deux formes possibles de la courbe des prix à terme (chiffres illustratifs).">""" + SCHEMA_FUTURES + r"""</x-fig>
<x-exemple>
<p>Le pétrole cote 80 $ sur l'échéance du mois prochain (M1) et 81,50 $ sur la suivante (M2). Un fonds roule ses contrats chaque mois. Si la courbe reste identique et le prix « spot » ne bouge pas :</p>
<div class="calcul">Chaque mois, le fonds vend à 80 et rachète à 81,50 : il obtient 80 ÷ 81,50 = 0,9816 contrat pour chaque contrat
Coût par roll ≈ 1 − 0,9816 = 1,84 %
Sur 12 mois : 0,9816^12 ≈ 0,80, soit environ −20 % alors que le prix affiché n'a pas bougé</div>
<p>Ce chiffre est volontairement simplifié (la forme de la courbe change sans cesse), mais il montre que l'actif « sous-jacent » et le produit tradé peuvent diverger fortement.</p>
</x-exemple>
<x-erreurs><ul><li>Penser qu'un ETF ou un CFD sur le pétrole suit exactement le prix du pétrole cité dans les médias.</li>
<li>Ignorer les dates d'échéance et de roll des contrats.</li><li>Sous-estimer la volatilité des matières agricoles et énergétiques (météo, géopolitique, stocks).</li></ul></x-erreurs>
<x-cles><ul><li>Familles : énergie, métaux précieux, métaux industriels, agricoles.</li><li>Elles se traitent surtout via des contrats à terme et des produits qui les répliquent.</li><li>Le contango crée un coût de roll qui peut éroder un produit à long terme.</li></ul></x-cles>
<x-exo><p>Le gaz cote 30 € sur M1 et 33 € sur M2. Estimez le coût d'un roll mensuel si la courbe reste identique. Puis sur 6 mois.</p>
<x-corr><div class="calcul">Ratio = 30 ÷ 33 = 0,9091 → coût ≈ 9,1 % par roll
Sur 6 mois : 0,9091^6 ≈ 0,564 → environ −43,6 %</div><p>Un contango aussi marqué (fréquent sur le gaz à certaines saisons) rend la détention prolongée via des futures très coûteuse.</p></x-corr></x-exo>
"""),

("1-5", "Les cryptomonnaies", r"""
<x-obj><ul><li>Comprendre les spécificités des cryptoactifs en tant que marché.</li><li>Identifier les risques propres : volatilité, conservation, plateformes.</li><li>Connaître le cadre réglementaire européen dans ses grandes lignes.</li></ul></x-obj>
<x-simple>
<p>Les <strong>cryptoactifs</strong> (ou cryptomonnaies) sont des actifs numériques enregistrés sur une <strong>blockchain</strong>, un registre partagé et sécurisé par cryptographie. Ils s'échangent 24 h/24 et 7 j/7 sur des plateformes d'échange. Leur prix dépend presque entièrement de l'offre et de la demande : la plupart ne produisent ni bénéfices ni dividendes, ce qui rend leur valeur « fondamentale » très discutée.</p>
<p>Cette formation ne recommande <strong>aucune</strong> cryptomonnaie. Les notions de trading (ordres, risque, analyse technique) s'y appliquent comme ailleurs, avec des risques supplémentaires.</p>
</x-simple>
<x-approfondi>
<p><strong>Spécificités et risques :</strong></p>
<ul><li><strong>Volatilité très élevée</strong> : des baisses de 70 à 80 % depuis un sommet ont eu lieu à plusieurs reprises sur les cryptoactifs les plus connus, et bien plus sur les petits projets, dont beaucoup disparaissent.</li>
<li><strong>Risque de conservation</strong> : si vous détenez vous-même vos clés privées et les perdez, les fonds sont perdus. Si une plateforme les détient pour vous, vous dépendez de sa solidité. La faillite de FTX en 2022 a bloqué les fonds de nombreux clients.</li>
<li><strong>Stablecoins</strong> : cryptoactifs censés valoir une devise (souvent 1 $). Leur stabilité dépend des réserves de l'émetteur : certains ont perdu leur ancrage (TerraUSD en 2022).</li>
<li><strong>Manipulation</strong> : sur les petites capitalisations, les opérations de « pump and dump » sont fréquentes.</li>
<li><strong>Produits dérivés</strong> : de nombreuses plateformes hors UE proposent des « perpétuels » avec des leviers extrêmes (parfois ×100), interdits aux particuliers européens sous forme de CFD au-delà de ×2.</li></ul>
<p><strong>Réglementation.</strong> Dans l'Union européenne, le règlement <strong>MiCA</strong> (Markets in Crypto-Assets) s'applique depuis fin 2024, avec des périodes transitoires selon les pays : les prestataires doivent être agréés. En France, l'AMF publie la liste des prestataires autorisés et des listes noires de sites non autorisés. Vérifiez sur le site de l'AMF avant toute ouverture de compte (module 12). La fiscalité est spécifique (module 13).</p>
</x-approfondi>
<x-exemple>
<p>Comparons la volatilité « journalière typique » d'un cryptoactif dont la volatilité annuelle est de 80 % avec celle d'un indice actions à 15 %. On convertit une volatilité annuelle en volatilité journalière en divisant par la racine carrée du nombre de jours de cotation (365 pour une crypto, environ 252 pour un indice) :</p>
<div class="calcul">Crypto : 80 % ÷ √365 = 80 ÷ 19,10 ≈ 4,19 % par jour
Indice : 15 % ÷ √252 = 15 ÷ 15,87 ≈ 0,94 % par jour</div>
<p>Un mouvement journalier « normal » est donc environ 4 à 5 fois plus grand sur ce cryptoactif. À risque égal en euros, la position doit être environ 4 à 5 fois plus petite (module 9).</p>
</x-exemple>
<x-note><p>La règle de la racine carrée du temps suppose des rendements indépendants d'un jour à l'autre. C'est une approximation commode, pas une loi exacte : les marchés connaissent des périodes de volatilité groupée et des mouvements extrêmes plus fréquents que ce modèle ne prévoit.</p></x-note>
<x-erreurs><ul><li>Laisser des fonds sur une plateforme non autorisée, attiré par un levier élevé ou un « rendement » promis.</li>
<li>Utiliser la même taille de position que sur un indice, sans tenir compte de la volatilité bien plus forte.</li>
<li>Croire qu'un actif « qui a fait ×10 » va recommencer.</li></ul></x-erreurs>
<x-cles><ul><li>Marché ouvert en continu, très volatil, à la valeur fondamentale débattue.</li><li>Risques propres : conservation, plateforme, stablecoins, manipulation.</li><li>En Europe : MiCA ; en France, vérifier les autorisations sur le site de l'AMF.</li></ul></x-cles>
<x-exo><p>Un cryptoactif a une volatilité annuelle de 60 %. Quelle est sa volatilité journalière approximative ? Si vous acceptez un mouvement « typique » contre vous de 100 € par jour, quelle taille de position cela suggère-t-il ?</p>
<x-corr><div class="calcul">60 % ÷ √365 = 60 ÷ 19,10 ≈ 3,14 % par jour
Taille ≈ 100 € ÷ 3,14 % = 100 ÷ 0,0314 ≈ 3 185 €</div><p>Une position d'environ 3 200 € bouge typiquement de 100 € par jour. Des journées 2 à 3 fois plus fortes restent fréquentes.</p></x-corr></x-exo>
"""),

("1-6", "Les ETF (fonds indiciels cotés)", r"""
<x-obj><ul><li>Comprendre le fonctionnement d'un ETF.</li><li>Connaître les différences physique/synthétique, capitalisant/distribuant.</li><li>Comprendre l'érosion des ETF à levier quotidien.</li></ul></x-obj>
<x-simple>
<p>Un <strong>ETF</strong> (Exchange Traded Fund, ou « tracker ») est un fonds qui réplique un indice (CAC 40, S&amp;P 500, MSCI World, or…) et qui s'achète en bourse comme une action. Ses frais annuels (<strong>TER</strong>) sont en général faibles. C'est l'outil de base de l'investisseur passif, mais il se trade aussi.</p>
</x-simple>
<x-approfondi>
<ul><li><strong>Réplication physique</strong> : l'ETF détient réellement les titres de l'indice (tous, ou un échantillon). <strong>Réplication synthétique</strong> : il détient un autre panier et échange sa performance contre celle de l'indice via un contrat d'échange (swap) avec une banque. Cela permet par exemple à certains ETF d'indices mondiaux d'être éligibles au PEA (module 13). Le risque de contrepartie est encadré par la réglementation européenne (UCITS).</li>
<li><strong>Capitalisant</strong> : les dividendes sont réinvestis. <strong>Distribuant</strong> : ils sont versés aux porteurs.</li>
<li><strong>Écart de suivi</strong> (tracking difference) : différence de performance avec l'indice, due aux frais, à la fiscalité des dividendes, etc.</li>
<li><strong>ETF à levier et inverses</strong> : ils visent par exemple 2× ou −1× la performance <em>quotidienne</em> d'un indice. Sur plusieurs jours, leur performance n'est <strong>pas</strong> 2× celle de l'indice : dans un marché qui oscille, ils s'érodent. Ce sont des outils de court terme.</li></ul>
</x-approfondi>
<x-exemple>
<p>Un indice part de 100, monte de 10 % puis baisse de 10 %. Un ETF à levier 2× quotidien part aussi de 100.</p>
<div class="calcul">Indice : 100 × 1,10 = 110 ; puis 110 × 0,90 = 99      → −1 %
ETF 2× : 100 × 1,20 = 120 ; puis 120 × 0,80 = 96      → −4 %
« Le double de l'indice » aurait donné −2 % ; l'ETF fait −4 %.</div>
<p>Si l'alternance se répète 4 fois (8 jours), l'indice finit à 100 × 0,99<sup>4</sup> ≈ 96,1 mais l'ETF à 100 × 0,96<sup>4</sup> ≈ 84,9. L'indice a perdu 3,9 %, l'ETF 15,1 %.</p>
</x-exemple>
<x-fig c="Dans un marché qui oscille sans tendance, l'ETF à levier quotidien perd beaucoup plus que deux fois la baisse de l'indice.">""" + SCHEMA_ETF + r"""</x-fig>
<x-erreurs><ul><li>Garder un ETF à levier pendant des mois en pensant obtenir « deux fois l'indice ».</li><li>Choisir un ETF uniquement sur son nom, sans lire le document d'informations clés (DIC) : indice exact, réplication, frais.</li></ul></x-erreurs>
<x-cles><ul><li>ETF = fonds coté qui réplique un indice, frais généralement faibles.</li><li>Physique vs synthétique ; capitalisant vs distribuant.</li><li>Les ETF à levier suivent un multiple de la performance <em>quotidienne</em> et s'érodent dans les marchés agités.</li></ul></x-cles>
<x-exo><p>Un indice fait −5 % puis +5 %. Calculez la performance de l'indice et celle d'un ETF inverse (−1×) quotidien sur ces deux jours.</p>
<x-corr><div class="calcul">Indice : 100 × 0,95 × 1,05 = 99,75 → −0,25 %
ETF inverse : 100 × 1,05 × 0,95 = 99,75 → −0,25 %</div><p>Les deux perdent ! Intuitivement, on attendrait +0,25 % pour l'inverse. L'effet de capitalisation quotidienne pénalise les produits à levier ou inverses quand le marché oscille.</p></x-corr></x-exo>
"""),

("1-7", "Les acteurs du marché", r"""
<x-obj><ul><li>Identifier les grands participants et leurs motivations.</li><li>Comprendre le rôle des teneurs de marché.</li><li>Situer le particulier dans cet écosystème.</li></ul></x-obj>
<x-simple><p>Sur les marchés, vous n'êtes pas seul : en face de chacun de vos ordres se trouve quelqu'un, avec ses propres raisons. Connaître ces acteurs aide à comprendre pourquoi les prix bougent.</p></x-simple>
<x-fig c="Les principaux acteurs. Leurs objectifs sont très différents : tous ne cherchent pas à « gagner » sur chaque transaction.">""" + SCHEMA_ACTEURS + r"""</x-fig>
<x-approfondi>
<ul><li><strong>Banques centrales</strong> (BCE, Fed…) : fixent les taux directeurs et peuvent intervenir sur les marchés. Elles ne cherchent pas le profit mais la stabilité des prix (module 7).</li>
<li><strong>Banques commerciales et d'investissement</strong> : exécutent les ordres de leurs clients, fournissent de la liquidité, notamment sur le change et les obligations.</li>
<li><strong>Investisseurs institutionnels</strong> : fonds de pension, assureurs, gestionnaires d'actifs, fonds souverains. Ils gèrent des montants énormes et achètent ou vendent souvent progressivement, sur des jours ou des semaines.</li>
<li><strong>Hedge funds</strong> : fonds aux stratégies variées (macro, arbitrage, quantitatif…), souvent à effet de levier.</li>
<li><strong>Teneurs de marché</strong> (market makers) : ils affichent en permanence un prix d'achat et un prix de vente, et se rémunèrent principalement sur l'écart entre les deux (le spread), en gérant le risque de leur stock.</li>
<li><strong>Traders à haute fréquence</strong> (HFT) : algorithmes qui opèrent en millisecondes, souvent comme teneurs de marché ou arbitragistes.</li>
<li><strong>Entreprises</strong> : se couvrent contre les variations de change ou de matières premières (une compagnie aérienne achète du kérosène à terme). Elles acceptent de « perdre » sur la couverture pour stabiliser leur activité.</li>
<li><strong>Particuliers</strong> : une part minoritaire des volumes sur la plupart des marchés, même si elle a progressé. Ils ont moins d'informations, de technologie et de capital que les professionnels.</li></ul>
</x-approfondi>
<x-exemple>
<p>Un teneur de marché cote une action 99,98 € à l'achat (bid) et 100,02 € à la vente (ask). Dans la journée, il achète 500 000 titres à des vendeurs et en vend 500 000 à des acheteurs, aux prix affichés.</p>
<div class="calcul">Gain par titre acheté puis revendu = 100,02 − 99,98 = 0,04 €
Gain brut = 500 000 × 0,04 = 20 000 €</div>
<p>Ce gain est brut : le teneur de marché supporte le risque que le prix bouge pendant qu'il détient des titres. Il ajuste en permanence ses prix pour équilibrer son stock. Pour vous, ce spread est un <strong>coût</strong> payé à chaque aller-retour (module 2).</p>
</x-exemple>
<x-erreurs><ul><li>Imaginer que « les institutionnels chassent les stops des particuliers » à chaque mouvement : c'est une explication facile, rarement vérifiable. Les gros acteurs cherchent surtout de la <em>liquidité</em> pour exécuter de gros ordres, et elle se trouve souvent là où beaucoup d'ordres sont accumulés.</li>
<li>Penser que le marché « doit » réagir comme vous l'anticipez : des acteurs aux horizons différents peuvent avoir raison en faisant l'inverse de vous.</li></ul></x-erreurs>
<x-cles><ul><li>Les acteurs ont des objectifs différents : profit, couverture, politique monétaire, gestion à long terme.</li><li>Les teneurs de marché fournissent la liquidité et se rémunèrent sur le spread.</li><li>Le particulier est un petit acteur face à des professionnels mieux équipés.</li></ul></x-cles>
<x-exo><p>Une entreprise européenne qui sera payée 10 millions de dollars dans 6 mois vend aujourd'hui ces dollars à terme. Six mois plus tard, le dollar s'est apprécié : elle aurait gagné plus sans couverture. A-t-elle fait une erreur ?</p>
<x-corr><p>Non. Son objectif n'était pas de spéculer mais de <strong>supprimer l'incertitude</strong> sur son chiffre d'affaires en euros. La couverture a rempli son rôle. Cet exemple montre que certains acteurs acceptent volontairement un « manque à gagner » : ils ne jouent pas le même jeu que les traders.</p></x-corr></x-exo>
"""),

("1-8", "Bourses, horaires et sessions", r"""
<x-obj><ul><li>Connaître les horaires des grandes places en heure de Paris.</li><li>Comprendre les phases d'enchères et les sessions du Forex.</li><li>Gérer les décalages d'heure d'été.</li></ul></x-obj>
<x-simple>
<p>Les actions se négocient sur des <strong>bourses</strong> (Euronext, NYSE, Nasdaq, Deutsche Börse, Tokyo…), chacune avec ses horaires. Le Forex et beaucoup de contrats à terme se négocient presque 24 h/24 en semaine. Les cryptoactifs, eux, ne s'arrêtent jamais.</p>
<p>Les moments de forte activité (ouvertures, chevauchements de sessions, publications économiques) apportent volume et volatilité. Les heures creuses apportent des spreads plus larges.</p>
</x-simple>
<x-approfondi>
<p><strong>Euronext Paris</strong> (heure de Paris) : pré-ouverture avec accumulation d'ordres à partir de 7 h 15, <strong>fixing d'ouverture à 9 h 00</strong>, cotation en continu jusqu'à 17 h 30, puis <strong>fixing de clôture</strong> (enchère) jusqu'à 17 h 35 et une courte phase de négociation au dernier cours. Les enchères d'ouverture et de clôture concentrent des volumes importants.</p>
<p><strong>New York</strong> (NYSE, Nasdaq) : 9 h 30 – 16 h 00 heure de New York, soit en général <strong>15 h 30 – 22 h 00 à Paris</strong>. Il existe aussi des séances étendues (pré-marché et après-bourse), moins liquides.</p>
<p><strong>Tokyo</strong> : 9 h 00 – 15 h 30 heure locale (avec une pause déjeuner), soit environ 1 h 00 – 7 h 30 à Paris en hiver.</p>
<p><strong>Forex</strong> : du dimanche vers 23 h à Paris jusqu'au vendredi vers 23 h, en sessions successives (Asie, Londres, New York). Le chevauchement Londres / New York (environ 14 h – 18 h à Paris) est souvent le plus actif. Les heures exactes et les jours fériés peuvent changer : vérifiez le site de la bourse ou de votre courtier.</p>
<p><strong>Règlement-livraison</strong> : après un achat d'actions, l'échange effectif titres contre argent intervient à J+1 (États-Unis depuis mai 2024) ou à J+2 (Europe, avec un passage à J+1 prévu en 2027). Cela compte notamment pour les dates de détachement des dividendes.</p>
</x-approfondi>
<x-fig c="Horaires approximatifs en heure de Paris, en hiver (l'ensemble se décale lors des changements d'heure non simultanés). La zone bleutée marque le chevauchement Paris / New York.">""" + SCHEMA_SESSIONS + r"""</x-fig>
<x-exemple>
<p>Les États-Unis passent à l'heure d'été le deuxième dimanche de mars, l'Europe le dernier dimanche de mars. Pendant ces 2 à 3 semaines, l'écart entre Paris et New York n'est plus de 6 heures mais de 5 heures.</p>
<div class="calcul">En temps normal : 9 h 30 (New York) + 6 h = 15 h 30 à Paris
Pendant le décalage de mars : 9 h 30 + 5 h = 14 h 30 à Paris
Même phénomène fin octobre / début novembre (dates de retour à l'heure d'hiver différentes)</div>
<p>Un trader qui place une alarme à 15 h 30 « pour l'ouverture américaine » arrive alors une heure après l'ouverture.</p>
</x-exemple>
<x-erreurs><ul><li>Trader une action pendant une phase d'enchères en croyant être exécuté immédiatement.</li><li>Trader en pré-marché ou après-bourse sans réaliser que la liquidité y est faible et les spreads larges.</li><li>Oublier les jours fériés (bourses fermées, Forex moins liquide).</li></ul></x-erreurs>
<x-cles><ul><li>Paris : 9 h 00 – 17 h 30 en continu, avec enchères d'ouverture et de clôture.</li><li>New York : généralement 15 h 30 – 22 h 00 à Paris ; attention aux changements d'heure.</li><li>Forex : 24 h/24 en semaine, avec des sessions plus ou moins actives.</li></ul></x-cles>
<x-exo><p>Une statistique américaine importante est publiée à 8 h 30, heure de New York, un vendredi de juin. À quelle heure est-elle publiée à Paris ? La bourse de New York est-elle déjà ouverte ?</p>
<x-corr><p>En juin, les deux pays sont à l'heure d'été : l'écart est de 6 heures. 8 h 30 + 6 h = <strong>14 h 30 à Paris</strong>. La bourse de New York n'ouvre qu'à 15 h 30 (heure de Paris) : la publication tombe donc avant l'ouverture des actions américaines, mais pendant la séance européenne, le Forex et les contrats à terme, qui réagissent immédiatement.</p></x-corr></x-exo>
"""),

("1-9", "Liquidité et volatilité", r"""
<x-obj><ul><li>Définir et mesurer la liquidité et la volatilité.</li><li>Calculer une volatilité historique simple.</li><li>Comprendre les conséquences pratiques pour le trader.</li></ul></x-obj>
<x-simple>
<p>La <strong>liquidité</strong>, c'est la facilité à acheter ou vendre rapidement une quantité importante sans faire bouger le prix. Un marché liquide a un spread étroit, beaucoup de volume et beaucoup d'ordres en attente.</p>
<p>La <strong>volatilité</strong> mesure l'ampleur des variations de prix. Un actif volatil fait de grands mouvements dans les deux sens. Elle n'est ni bonne ni mauvaise : elle crée des opportunités et du risque à parts égales.</p>
</x-simple>
<div class="duo"><x-fig c="Faible volatilité : petites bougies, progression régulière.">""" + SCHEMA_VOL + r"""</x-fig><x-fig c="Forte volatilité : grandes bougies, mouvements amples. Même point de départ et même point d'arrivée.">""" + SCHEMA_VOL2 + r"""</x-fig></div>
<x-approfondi>
<p><strong>Mesurer la liquidité</strong> : volume échangé, spread, profondeur du carnet d'ordres (module 2). Une petite capitalisation peut afficher un spread de 1 % et seulement quelques milliers d'euros échangés par jour : en sortir rapidement peut coûter cher.</p>
<p><strong>Mesurer la volatilité</strong> : la mesure classique est l'<strong>écart-type des rendements</strong>, souvent annualisé. On utilise aussi l'<strong>ATR</strong> (amplitude moyenne des bougies, module 6) et la <strong>volatilité implicite</strong> tirée du prix des options (le VIX pour le S&amp;P 500, module 7).</p>
<p><strong>Conséquences pratiques</strong> : plus la volatilité est forte, plus les stops doivent être éloignés pour ne pas être touchés par le « bruit », et donc plus la position doit être petite pour garder le même risque en euros. Une faible liquidité augmente le coût réel des ordres (spread, slippage).</p>
</x-approfondi>
<x-exemple>
<p>Cinq rendements journaliers successifs : +1 %, −0,5 %, +1,5 %, −1 %, 0 %. Calculons la volatilité.</p>
<ol class="etapes"><li>Moyenne : (1 − 0,5 + 1,5 − 1 + 0) ÷ 5 = 1 ÷ 5 = 0,2 %</li>
<li>Écarts à la moyenne : 0,8 ; −0,7 ; 1,3 ; −1,2 ; −0,2</li>
<li>Carrés : 0,64 ; 0,49 ; 1,69 ; 1,44 ; 0,04 → somme = 4,30</li>
<li>Variance d'échantillon : 4,30 ÷ (5 − 1) = 1,075</li>
<li>Écart-type journalier : √1,075 ≈ 1,04 %</li>
<li>Annualisé : 1,04 % × √252 ≈ 1,04 × 15,87 ≈ 16,5 %</li></ol>
<p>Avec seulement 5 observations, ce chiffre est très imprécis : en pratique, on utilise 20 jours, 60 jours ou plus.</p>
</x-exemple>
<x-erreurs><ul><li>Confondre volatilité et tendance : un actif peut être très volatil sans aller nulle part.</li><li>Appliquer la même distance de stop sur tous les actifs, quelle que soit leur volatilité.</li><li>Trader des titres peu liquides sans regarder le spread ni le volume.</li></ul></x-erreurs>
<x-cles><ul><li>Liquidité = facilité d'exécution sans impact sur le prix (spread, volume, profondeur).</li><li>Volatilité = ampleur des variations ; mesurée par l'écart-type des rendements, l'ATR ou la volatilité implicite.</li><li>Volatilité plus forte ⇒ stop plus large ⇒ position plus petite.</li></ul></x-cles>
<x-exo><p>Un actif a une volatilité journalière de 2 %. Quelle est sa volatilité annualisée approximative (252 jours) ? Un autre affiche 12 % annualisés : quelle est sa volatilité journalière ?</p>
<x-corr><div class="calcul">2 % × √252 ≈ 2 × 15,87 ≈ 31,7 % par an
12 % ÷ √252 ≈ 12 ÷ 15,87 ≈ 0,76 % par jour</div></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Actions &amp; indices</h2><ul><li>Action = part d'entreprise (dividendes, droit de vote).</li><li>Indice pondéré par la capitalisation : les poids lourds dominent.</li><li>Variation de l'indice = Σ (poids × variation).</li><li>Indice de prix ≠ dividendes réinvestis.</li></ul></div>
<div class="encadre"><h2>Obligations</h2><ul><li>Prêt : coupons + nominal à l'échéance.</li><li>Taux ↑ ⇒ prix ↓ (et inversement).</li><li>Prix = Σ flux ÷ (1 + taux)<sup>t</sup>.</li><li>Échéance longue = plus sensible aux taux.</li></ul></div>
<div class="encadre"><h2>Forex</h2><ul><li>EUR/USD = 1,0850 : 1 € = 1,0850 $.</li><li>Acheter la paire = parier sur la devise de base.</li><li>Résultat en devise de cotation, à convertir.</li><li>Majeures, croisées, exotiques.</li></ul></div>
<div class="encadre"><h2>Matières premières</h2><ul><li>Énergie, métaux, agricoles ; surtout via des futures.</li><li>Contango : roll coûteux. Déport : l'inverse.</li><li>Le produit tradé peut diverger du prix affiché.</li></ul></div>
<div class="encadre"><h2>Cryptos</h2><ul><li>24/7, très volatiles, valeur fondamentale débattue.</li><li>Risques : conservation, plateforme, stablecoins, manipulation.</li><li>MiCA ; vérifier les autorisations sur le site de l'AMF.</li></ul></div>
<div class="encadre"><h2>ETF</h2><ul><li>Fonds coté répliquant un indice, faibles frais.</li><li>Physique / synthétique ; capitalisant / distribuant.</li><li>ETF à levier quotidien : érosion dans les marchés agités.</li></ul></div>
<div class="encadre"><h2>Acteurs</h2><ul><li>Banques centrales, banques, institutionnels, hedge funds, market makers, HFT, entreprises, particuliers.</li><li>Market maker : se rémunère sur le spread.</li></ul></div>
<div class="encadre"><h2>Horaires (heure de Paris)</h2><ul><li>Euronext : 9 h – 17 h 30 (+ enchères).</li><li>New York : 15 h 30 – 22 h (sauf décalages d'heure d'été).</li><li>Forex : dimanche ~23 h → vendredi ~23 h.</li></ul></div>
<div class="encadre"><h2>Liquidité &amp; volatilité</h2><ul><li>Liquidité : spread, volume, profondeur.</li><li>Volatilité annuelle ≈ volatilité journalière × √252 (approximation).</li><li>Plus volatil ⇒ stop plus large ⇒ position plus petite.</li></ul></div>
"""

QUIZ = [
("Un indice pondéré par la capitalisation : A (poids 50 %) fait +2 %, B (30 %) fait −2 %, C (20 %) fait +1 %. Variation de l'indice ?",
 ["+0,2 %", "+0,6 %", "+1 %", "−0,4 %"], 1, "50 % × 2 − 30 % × 2 + 20 % × 1 = 1 − 0,6 + 0,2 = +0,6 %."),
("Quand les taux d'intérêt du marché montent, le prix des obligations existantes :",
 ["Monte", "Baisse", "Ne change pas", "Double"], 1, "Les nouvelles obligations rapportent plus : les anciennes doivent baisser de prix pour rester attractives."),
("Quelle obligation est la plus sensible à une hausse des taux ?",
 ["Échéance 1 an", "Échéance 3 ans", "Échéance 10 ans", "Elles sont toutes aussi sensibles"], 2, "Plus l'échéance est longue, plus la duration et donc la sensibilité aux taux sont élevées."),
("EUR/USD passe de 1,1000 à 1,1050. Cela signifie que :",
 ["Le dollar s'est apprécié face à l'euro", "L'euro s'est apprécié face au dollar", "Les deux devises ont baissé", "Rien, c'est le spread"], 1, "Il faut plus de dollars pour 1 euro : l'euro s'est renforcé."),
("Vous achetez 10 000 € sur EUR/USD à 1,1000 et revendez à 1,1050. Votre gain est de :",
 ["5 $", "50 $", "500 $", "50 €"], 1, "10 000 × (1,1050 − 1,1000) = 10 000 × 0,0050 = 50 $ (en devise de cotation)."),
("Le contango désigne une situation où :",
 ["Les échéances lointaines sont plus chères que les proches", "Les échéances proches sont plus chères", "Le prix est négatif", "Il n'y a pas de contrat à terme"], 0, "En contango, la courbe monte avec l'échéance ; rouler ses positions coûte alors de l'argent."),
("Un ETF à levier 2× quotidien, quand l'indice fait +10 % puis −10 % :",
 ["Fait −2 %", "Fait −4 %", "Fait 0 %", "Fait +2 %"], 1, "100 × 1,20 × 0,80 = 96, soit −4 %, alors que l'indice fait −1 % : c'est l'érosion due à la capitalisation quotidienne."),
("Un teneur de marché se rémunère principalement :",
 ["Grâce aux dividendes", "Grâce à l'écart entre prix d'achat et de vente (spread)", "Grâce aux impôts", "En prédisant les tendances à long terme"], 1, "Il cote en permanence un bid et un ask et gagne l'écart, en gérant le risque de son stock."),
("En temps normal, l'ouverture de la bourse de New York (9 h 30 locale) correspond à quelle heure à Paris ?",
 ["14 h 30", "15 h 30", "16 h 30", "9 h 30"], 1, "Le décalage habituel est de 6 h, soit 15 h 30, sauf pendant les semaines où les changements d'heure ne sont pas simultanés (14 h 30)."),
("Un marché liquide se caractérise par :",
 ["Un spread large et peu de volume", "Un spread étroit, du volume et de la profondeur", "Des prix qui ne bougent jamais", "Une forte volatilité"], 1, "La liquidité, c'est pouvoir échanger rapidement de grandes quantités sans faire bouger le prix."),
("Un actif a une volatilité journalière de 1 %. Sa volatilité annualisée (252 jours) est d'environ :",
 ["2,5 %", "15,9 %", "25,2 %", "252 %"], 1, "1 % × √252 ≈ 1 × 15,87 ≈ 15,9 %."),
("Pour garder le même risque en euros sur un actif deux fois plus volatil, il faut en général :",
 ["Une position deux fois plus grande", "La même position", "Une position plus petite, avec un stop plus large", "Supprimer le stop"], 2, "Le stop doit être plus éloigné pour ne pas être touché par le bruit, donc la taille diminue pour un même risque."),
]
