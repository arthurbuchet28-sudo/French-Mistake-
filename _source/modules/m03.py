from svgkit import plot, table, svg, t, line, arrow

NUM = 3
TITRE = "Produits et effet de levier"
RESUME = "Comptant ou dérivés ; CFD, futures, options, warrants, turbos ; levier, marge, liquidation ; pip, tick, lot ; tous les frais."
DUREE = "3 h"
INTRO = r"""<p>Le même pari sur la hausse du CAC 40 peut se prendre avec un ETF, un CFD, un contrat à terme, une option ou un turbo. Le risque, les coûts et ce qui peut arriver au pire ne sont pas du tout les mêmes. Ce module est dense : prenez le temps de refaire chaque calcul. L'<strong>effet de levier</strong>, en particulier, est la cause numéro un des comptes détruits chez les débutants.</p>"""


def _arbre():
    W = 680
    p = []
    def boite(x, y, w, txt, cls="g-rect", sous=""):
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{44 if sous else 32}" rx="7" class="{cls}"/>')
        p.append(t(x + w / 2, y + 20, txt, "g-txt g-fort", "middle"))
        if sous:
            p.append(t(x + w / 2, y + 36, sous, "g-txt g-petit", "middle"))
    boite(260, 6, 160, "Produits financiers", "g-rect-a")
    boite(40, 76, 220, "Comptant (au comptant)", "g-rect-h", "on détient l'actif")
    boite(420, 76, 220, "Dérivés", "g-rect-b", "valeur tirée d'un sous-jacent")
    p.append(arrow(320, 38, 150, 76)); p.append(arrow(360, 38, 530, 76))
    boite(40, 160, 220, "Actions, ETF, obligations,", sous="devises au comptant, cryptos détenues")
    boite(290, 160, 120, "Fermes", sous="futures, CFD")
    boite(430, 160, 120, "Optionnels", sous="options, warrants")
    boite(570, 160, 104, "À barrière", sous="turbos")
    p.append(arrow(150, 120, 150, 160)); p.append(arrow(500, 120, 350, 160)); p.append(arrow(530, 120, 490, 160)); p.append(arrow(560, 120, 620, 160))
    p.append(t(340, 232, "Perte limitée à la mise : comptant sans levier, achat d'options, warrants, turbos.", "g-txt g-petit", "middle"))
    p.append(t(340, 248, "Perte pouvant dépasser la mise : futures, vente d'options (et CFD, hors protection contre le solde négatif du compte).", "g-txt g-petit", "middle"))
    return svg(W, 258, "".join(p), "Classification des produits financiers")


SCHEMA_ARBRE = _arbre()

_S = list(range(80, 121, 1))
SCHEMA_CALL_PUT = '<div class="duo">' + plot(
    [{"x": _S, "y": [max(s - 100, 0) - 4 for s in _S], "cls": "g-lh", "label": "Achat de call (K = 100, prime 4)"},
     {"x": _S, "y": [-(max(s - 100, 0) - 4) for s in _S], "cls": "g-lb", "label": "Vente de call"}],
    w=420, h=260, label="Profil de gain à l'échéance d'un call acheté et vendu", xlabel="Prix du sous-jacent à l'échéance",
    yr=(-22, 22), vlines=[{"x": 104, "label": "Seuil 104", "cls": "g-l3 g-fin", "ly": 150}],
    yfmt=lambda v: f"{v:+.0f}".replace("+0", "0")) + plot(
    [{"x": _S, "y": [max(100 - s, 0) - 3 for s in _S], "cls": "g-lh", "label": "Achat de put (K = 100, prime 3)"},
     {"x": _S, "y": [-(max(100 - s, 0) - 3) for s in _S], "cls": "g-lb", "label": "Vente de put"}],
    w=420, h=260, label="Profil de gain à l'échéance d'un put acheté et vendu", xlabel="Prix du sous-jacent à l'échéance",
    yr=(-22, 22), vlines=[{"x": 97, "label": "Seuil 97", "cls": "g-l3 g-fin", "ly": 150}],
    yfmt=lambda v: f"{v:+.0f}".replace("+0", "0")) + '</div>'

_j = list(range(90, -1, -2))
SCHEMA_THETA = plot([{"x": [-d for d in _j], "y": [2.5 * (d / 90) ** 0.5 for d in _j], "cls": "g-l2", "label": "Valeur temps d'une option à la monnaie (illustratif)"}],
                    label="Érosion de la valeur temps à l'approche de l'échéance", xlabel="Jours avant l'échéance",
                    xr=(-90, 0), yr=(0, 2.8), xticks=[-90, -60, -30, 0], xfmt=lambda v: f"{-v:.0f}",
                    yfmt=lambda v: f"{v:.1f}".replace(".", ","))

_I = list(range(6900, 8001, 25))
SCHEMA_TURBO = plot([{"x": _I, "y": [max((i - 7000) / 100, 0) for i in _I], "cls": "g-lh", "label": "Valeur théorique du turbo call (strike = barrière = 7 000, parité 100)"}],
                    label="Valeur d'un turbo call selon le niveau de l'indice", xlabel="Niveau de l'indice", yr=(-0.5, 12), yticks=[0, 2, 4, 6, 8, 10],
                    legend_xy=(300, 196), vlines=[{"x": 7000, "label": "Barrière : désactivation", "cls": "g-lb", "ly": 40}, {"x": 7500, "label": "Achat : 5 €", "cls": "g-l3 g-fin", "ly": 70}],
                    yfmt=lambda v: f"{v:.0f} €")

_lev = [2, 3, 4, 5, 6, 8, 10, 15, 20, 25, 30, 40, 50]
SCHEMA_LEVIER = plot([{"x": _lev, "y": [100 / l for l in _lev], "cls": "g-lb", "label": "Mouvement contraire qui efface 100 % du capital"},
                      {"x": _lev, "y": [50 / l for l in _lev], "cls": "g-l2", "label": "Mouvement contraire qui fait perdre 50 %"}],
                     label="Plus le levier est élevé, plus un petit mouvement suffit à perdre le capital",
                     xlabel="Levier effectif (exposition ÷ capital)", yr=(0, 55), xr=(0, 50), legend_xy=(200, 20),
                     marks=[{"x": 10, "y": 10, "t": "Levier 10 : −10 % suffit"}, {"x": 30, "y": 100 / 30, "t": "Levier 30 : −3,3 %", "dy": -10}],
                     yfmt=lambda v: f"{v:.0f} %")

LECONS = [
("3-1", "Comptant ou dérivés", r"""
<x-obj><ul><li>Distinguer un actif détenu au comptant d'un produit dérivé.</li><li>Savoir quels produits peuvent faire perdre plus que la mise.</li></ul></x-obj>
<x-simple>
<p>Acheter <strong>au comptant</strong>, c'est acheter l'actif lui-même et le payer en totalité : 100 actions à 50 € coûtent 5 000 €, et vous en êtes propriétaire.</p>
<p>Un <strong>produit dérivé</strong> est un contrat dont la valeur dépend (« dérive ») du prix d'un autre actif, appelé <strong>sous-jacent</strong>. Vous ne possédez pas l'actif : vous êtes exposé à ses variations. La plupart des dérivés permettent de prendre une exposition importante avec une mise réduite : c'est l'<strong>effet de levier</strong>.</p>
</x-simple>
<x-fig c="Une classification simplifiée. Le risque maximal dépend autant de la façon dont on utilise le produit (acheteur ou vendeur) que du produit lui-même.">""" + SCHEMA_ARBRE + r"""</x-fig>
<x-approfondi>
<p>Les dérivés existent d'abord pour <strong>se couvrir</strong> (un producteur de blé vend sa récolte à terme pour fixer son prix) et pour <strong>transférer le risque</strong> vers ceux qui acceptent de le porter. Ils servent aussi à spéculer avec levier. On distingue :</p>
<ul><li>les <strong>dérivés fermes</strong> (futures, forwards, CFD) : les deux parties sont engagées, gains et pertes sont symétriques ;</li>
<li>les <strong>dérivés optionnels</strong> (options, warrants) : l'acheteur a un droit, pas une obligation ; sa perte est limitée à la prime payée ;</li>
<li>les <strong>produits à barrière</strong> (turbos) : la position est automatiquement désactivée si une barrière est touchée.</li></ul>
<p>Certains sont négociés en <strong>bourse</strong> (futures, options listées, turbos, warrants), d'autres <strong>de gré à gré</strong> (OTC), directement avec un intermédiaire (CFD, Forex au comptant chez un courtier). De gré à gré, la contrepartie est souvent le courtier lui-même.</p>
</x-approfondi>
<x-exemple>
<p>Vous voulez une exposition de 5 000 € à une action à 50 €.</p>
<div class="calcul">Au comptant : 100 actions × 50 € = 5 000 € déboursés
En CFD (marge de 20 %, soit un levier de 5) : 5 000 × 20 % = 1 000 € immobilisés
Si l'action baisse de 10 % : perte = 5 000 × 10 % = 500 € dans les deux cas
Au comptant : 500 ÷ 5 000 = −10 % de la somme engagée
En CFD : 500 ÷ 1 000 = −50 % de la marge immobilisée</div>
<p>Le levier ne change pas la perte en euros pour une même exposition. Il permet de prendre une exposition bien plus grande que son capital, et c'est là que se trouve le danger.</p>
</x-exemple>
<x-erreurs><ul><li>Croire qu'un produit dérivé est « plus risqué en soi » : c'est surtout la taille de l'exposition qui compte.</li><li>À l'inverse, croire qu'une mise de 1 000 € limite la perte à 1 000 € sur un produit à levier.</li><li>Trader un dérivé sans savoir qui est la contrepartie ni où il se négocie.</li></ul></x-erreurs>
<x-cles><ul><li>Comptant : on possède l'actif. Dérivé : on est exposé à son prix via un contrat.</li><li>Dérivés fermes, optionnels, à barrière ; en bourse ou de gré à gré.</li><li>Le levier permet une exposition supérieure au capital : c'est la source du risque.</li></ul></x-cles>
<x-exo><p>Vous voulez une exposition de 12 000 € à un indice. Combien immobilisez-vous avec un levier de 20 ? Si l'indice baisse de 3 %, quelle est la perte en euros et en % de la marge ?</p>
<x-corr><div class="calcul">Marge = 12 000 ÷ 20 = 600 €
Perte = 12 000 × 3 % = 360 €
En % de la marge = 360 ÷ 600 = 60 %</div></x-corr></x-exo>
"""),

("3-2", "Les CFD (contrats sur différence)", r"""
<x-obj><ul><li>Comprendre le fonctionnement d'un CFD et ses coûts.</li><li>Connaître les protections européennes pour les particuliers.</li></ul></x-obj>
<x-simple>
<p>Un <strong>CFD</strong> (Contract for Difference) est un contrat entre vous et un courtier : vous échangez la <strong>différence</strong> de prix d'un actif entre l'ouverture et la clôture de la position. Vous ne possédez jamais l'actif. On peut être acheteur ou vendeur aussi facilement, et on ne dépose qu'une <strong>marge</strong>, une fraction de la valeur de la position.</p>
</x-simple>
<x-approfondi>
<p><strong>Coûts</strong> : spread (parfois plus une commission sur les actions), <strong>financement overnight</strong> pour toute position gardée après la clôture du jour (voir leçon 3.9), éventuellement frais de conversion de devise. Les CFD sont conçus pour le court terme : le financement les rend coûteux à long terme.</p>
<p><strong>Mesures européennes (ESMA 2018, reprises par l'AMF) pour les clients particuliers</strong> :</p>
""" + table(["Sous-jacent", "Levier maximal", "Marge minimale"],
            [["Paires de devises majeures", "30:1", "3,33 %"], ["Autres devises, or, indices majeurs", "20:1", "5 %"],
             ["Matières premières (hors or), indices non majeurs", "10:1", "10 %"], ["Actions individuelles et autres", "5:1", "20 %"], ["Cryptoactifs", "2:1", "50 %"]]) + r"""
<ul><li><strong>Clôture automatique</strong> des positions quand les fonds du compte tombent à 50 % de la marge minimale requise.</li>
<li><strong>Protection contre le solde négatif</strong> : la perte totale est limitée aux fonds du compte CFD.</li>
<li><strong>Interdiction des incitations</strong> (bonus) et <strong>avertissement standardisé</strong> indiquant le pourcentage de clients perdants.</li></ul>
<p>Les clients classés « professionnels » peuvent obtenir davantage de levier, mais perdent ces protections. Certains sites poussent les particuliers à demander ce statut : méfiance.</p>
<p><strong>Risque de contrepartie</strong> : le courtier est souvent votre contrepartie (modèle « teneur de marché ») ou transmet vos ordres à des fournisseurs de liquidité. D'où l'importance d'un courtier régulé et des règles de ségrégation des fonds clients (module 12).</p>
</x-approfondi>
<x-exemple>
<p>Vous achetez un CFD sur 100 actions à 50 € (levier maximal 5:1, soit 20 % de marge) et gardez la position 30 jours. Le financement annuel est de 5,5 % (taux de référence + marge du courtier, chiffre illustratif).</p>
<div class="calcul">Valeur de la position (notionnel) = 100 × 50 = 5 000 €
Marge requise = 5 000 × 20 % = 1 000 €
Financement ≈ 5 000 × 5,5 % × 30 ÷ 365 ≈ 22,60 €
Si l'action passe à 53 € : gain brut = 100 × 3 = 300 € ; net ≈ 300 − 22,60 = 277,40 € (hors spread)
Si l'action passe à 47 € : perte = 300 + 22,60 = 322,60 €, soit 32 % de la marge</div>
</x-exemple>
<x-erreurs><ul><li>Garder des CFD des mois sans calculer le financement.</li><li>Utiliser tout le levier disponible « parce qu'il est offert ».</li><li>Accepter le statut de client professionnel pour obtenir plus de levier.</li><li>Ouvrir un compte chez un intermédiaire non autorisé en France (vérifier sur le site de l'AMF et REGAFI).</li></ul></x-erreurs>
<x-cles><ul><li>CFD = contrat sur la différence de prix, sans propriété de l'actif, avec marge.</li><li>Leviers plafonnés pour les particuliers (30:1 à 2:1), clôture à 50 % de marge, protection contre le solde négatif.</li><li>Coûts : spread, commission éventuelle, financement overnight.</li></ul></x-cles>
<x-exo><p>CFD sur indice majeur : 2 contrats à 5 € le point, indice à 8 000. Quelle est la marge minimale pour un particulier ? Combien perdez-vous si l'indice baisse de 120 points ?</p>
<x-corr><div class="calcul">Notionnel = 8 000 × 5 € × 2 = 80 000 €
Marge minimale (indice majeur, 20:1 → 5 %) = 80 000 × 5 % = 4 000 €
Perte = 120 points × 5 € × 2 = 1 200 € (soit 30 % de la marge, pour une baisse de 1,5 %)</div></x-corr></x-exo>
"""),

("3-3", "Les contrats à terme (futures)", r"""
<x-obj><ul><li>Comprendre ce qu'est un future standardisé et comment fonctionne la chambre de compensation.</li><li>Calculer le résultat et les appels de marge quotidiens.</li></ul></x-obj>
<x-simple>
<p>Un <strong>contrat à terme</strong> (future) est un engagement d'acheter ou de vendre un actif à un prix fixé aujourd'hui, à une date future (l'<strong>échéance</strong>). Il est <strong>standardisé</strong> (taille, échéance, pas de cotation) et négocié en bourse. Une <strong>chambre de compensation</strong> s'interpose entre acheteurs et vendeurs et garantit la bonne fin des contrats.</p>
</x-simple>
<x-approfondi>
<ul><li><strong>Multiplicateur</strong> (valeur du point) : par exemple 10 € par point pour le future Euro Stoxx 50, 25 € pour le future DAX standard (avec des versions mini et micro), 50 $ pour le E-mini S&amp;P 500 et 5 $ pour sa version micro. Vérifiez toujours la fiche officielle du contrat sur le site de la bourse.</li>
<li><strong>Tick</strong> : plus petite variation de prix (0,25 point sur le E-mini S&amp;P 500, soit 12,50 $).</li>
<li><strong>Dépôt de garantie</strong> (marge initiale) : fixé par la chambre de compensation selon la volatilité, et modifiable à tout moment.</li>
<li><strong>Appels de marge quotidiens</strong> : chaque jour, les gains et pertes sont crédités ou débités sur le compte (« mark-to-market »). Si le solde tombe sous la marge de maintenance, il faut remettre des fonds, sinon le courtier ferme la position.</li>
<li><strong>Échéance et roll</strong> : les contrats sur indices sont souvent trimestriels (mars, juin, septembre, décembre). Pour rester en position, on « roule » vers l'échéance suivante. Le règlement se fait en espèces (indices) ou par livraison physique (certaines matières premières, que le particulier doit absolument éviter).</li></ul>
<p>Avantages : marché centralisé et transparent, coûts souvent faibles, presque 24 h/24. Inconvénients : contrats souvent gros pour un petit compte, et <strong>pas de protection contre le solde négatif</strong> : la perte peut dépasser le capital du compte.</p>
</x-approfondi>
<x-exemple>
<p>Vous achetez 1 future sur un indice à 5 000 points, à 10 € le point. Dépôt de garantie supposé : 4 000 €.</p>
<div class="calcul">Exposition = 5 000 × 10 = 50 000 € (levier ≈ 50 000 ÷ 4 000 = 12,5 si le compte ne contient que la marge)
Jour 1 : clôture à 4 950 → 50 × 10 = −500 € débités
Jour 2 : clôture à 5 030 → 80 × 10 = +800 € crédités
Jour 3 : vous revendez à 5 010 → 20 × 10 = −200 €
Résultat total = −500 + 800 − 200 = +100 € = (5 010 − 5 000) × 10</div>
</x-exemple>
<x-erreurs><ul><li>Trader un contrat trop gros pour son compte (un seul contrat standard peut représenter plusieurs fois le capital).</li><li>Oublier l'échéance, ou laisser arriver à livraison un contrat à livraison physique.</li><li>Confondre dépôt de garantie et perte maximale.</li></ul></x-erreurs>
<x-cles><ul><li>Future = engagement standardisé, en bourse, garanti par une chambre de compensation.</li><li>Résultat = variation en points × valeur du point × nombre de contrats.</li><li>Appels de marge quotidiens ; pertes possibles supérieures au capital.</li></ul></x-cles>
<x-exo><p>Vous vendez 2 micro-futures sur un indice américain à 5 $ le point, à 5 200. Vous rachetez à 5 150. Résultat ? Et si vous aviez racheté à 5 290 ?</p>
<x-corr><div class="calcul">Rachat à 5 150 : (5 200 − 5 150) × 5 × 2 = 50 × 10 = +500 $
Rachat à 5 290 : (5 200 − 5 290) × 5 × 2 = −90 × 10 = −900 $</div></x-corr></x-exo>
"""),

("3-4", "Les options (1) : call, put, prime, strike, échéance", r"""
<x-obj><ul><li>Comprendre le droit acheté avec une option d'achat (call) ou de vente (put).</li><li>Tracer et lire un profil de gain à l'échéance.</li><li>Comprendre l'asymétrie entre acheteur et vendeur d'options.</li></ul></x-obj>
<x-simple>
<p>Une <strong>option</strong> donne à son acheteur le <strong>droit, mais pas l'obligation</strong>, d'acheter (option <strong>call</strong>) ou de vendre (option <strong>put</strong>) un actif à un prix fixé, le <strong>prix d'exercice</strong> (strike), jusqu'à une date donnée (l'<strong>échéance</strong>). Pour ce droit, l'acheteur paie une <strong>prime</strong> au vendeur.</p>
<ul><li>Acheteur de call : il parie sur la hausse ; perte limitée à la prime.</li>
<li>Acheteur de put : il parie sur la baisse ou se protège ; perte limitée à la prime.</li>
<li>Vendeur d'option : il encaisse la prime mais prend une <strong>obligation</strong> ; sa perte peut être très importante (illimitée pour un call vendu « à nu »).</li></ul>
</x-simple>
<x-approfondi>
<p>Une option <strong>européenne</strong> ne s'exerce qu'à l'échéance ; une option <strong>américaine</strong> à tout moment jusqu'à l'échéance (les noms ne désignent pas des lieux). Un contrat porte souvent sur 100 actions (selon le marché et le contrat). En pratique, la plupart des options sont revendues avant l'échéance plutôt qu'exercées.</p>
<p>À l'échéance, la valeur d'un call est max(S − K ; 0) et celle d'un put max(K − S ; 0), où S est le prix du sous-jacent et K le strike. Le <strong>point mort</strong> (seuil de rentabilité) d'un call acheté est K + prime ; celui d'un put acheté est K − prime.</p>
</x-approfondi>
<x-fig c="Profils de gain à l'échéance, par action. L'acheteur perd au plus la prime ; le vendeur gagne au plus la prime.">""" + SCHEMA_CALL_PUT + r"""</x-fig>
<x-exemple>
<p><strong>Call</strong> de strike 100, prime 4 € (par action), contrat de 100 actions : coût = 400 €.</p>
<div class="calcul">À l'échéance, action à 110 : valeur = 110 − 100 = 10 € ; gain = (10 − 4) × 100 = +600 €
Action à 104 : valeur = 4 € ; gain = 0 € (point mort = 100 + 4)
Action à 95 : valeur = 0 ; perte = la prime, −400 € (et pas plus, même si l'action tombe à 50)</div>
<p><strong>Put</strong> de strike 100, prime 3 € : point mort = 100 − 3 = 97.</p>
<div class="calcul">Action à 90 : valeur = 100 − 90 = 10 € ; gain = (10 − 3) × 100 = +700 €
Action à 105 : valeur = 0 ; perte = −300 €</div>
<p>Pour le <strong>vendeur</strong> du call : il encaisse 400 €. Si l'action finit à 130, il doit payer (130 − 100) × 100 = 3 000 €, soit une perte nette de 2 600 €.</p>
</x-exemple>
<x-erreurs><ul><li>Acheter des options très éloignées du prix (« pas chères ») qui expirent presque toujours sans valeur.</li><li>Vendre des options pour « encaisser des primes régulières » sans mesurer le risque extrême.</li><li>Oublier que le temps joue contre l'acheteur (leçon suivante).</li></ul></x-erreurs>
<x-cles><ul><li>Call = droit d'acheter ; put = droit de vendre ; au prix d'exercice, jusqu'à l'échéance.</li><li>Acheteur : perte limitée à la prime. Vendeur : gain limité à la prime, perte potentiellement très grande.</li><li>Point mort : K + prime (call), K − prime (put).</li></ul></x-cles>
<x-exo><p>Vous achetez 2 contrats put (100 actions chacun) de strike 50, prime 2,50 €. À l'échéance, l'action vaut 44 €. Quel est votre résultat ? Et si elle vaut 49 € ?</p>
<x-corr><div class="calcul">Coût = 2,50 × 100 × 2 = 500 €
À 44 € : valeur = (50 − 44) × 200 = 1 200 € → gain net = 1 200 − 500 = +700 €
À 49 € : valeur = (50 − 49) × 200 = 200 € → résultat = 200 − 500 = −300 €</div><p>À 49 €, l'option a une valeur, mais inférieure à la prime payée : le point mort est 50 − 2,50 = 47,50 €.</p></x-corr></x-exo>
"""),

("3-5", "Les options (2) : valeur temps et introduction aux grecques", r"""
<x-obj><ul><li>Décomposer une prime en valeur intrinsèque et valeur temps.</li><li>Comprendre l'intuition des grecques : delta, gamma, thêta, vega.</li></ul></x-obj>
<x-simple>
<p>Avant l'échéance, la prime d'une option se compose de deux parties :</p>
<ul><li>la <strong>valeur intrinsèque</strong> : ce que l'option rapporterait si on l'exerçait maintenant. Pour un call : max(S − K ; 0) ;</li>
<li>la <strong>valeur temps</strong> : le reste. C'est le prix de la « chance » que l'option prenne de la valeur d'ici l'échéance. Elle diminue avec le temps et vaut zéro à l'échéance.</li></ul>
<p>Une option est <strong>dans la monnaie</strong> si elle a une valeur intrinsèque, <strong>à la monnaie</strong> si le prix est proche du strike, <strong>hors de la monnaie</strong> sinon.</p>
</x-simple>
<x-approfondi>
<p>Les <strong>grecques</strong> mesurent la sensibilité de la prime à différents facteurs. Elles sont calculées par des modèles (le plus connu est Black-Scholes) et sont des approximations valables pour de petites variations :</p>
<ul><li><strong>Delta</strong> : variation de la prime pour 1 € de variation du sous-jacent. Entre 0 et 1 pour un call (environ 0,5 à la monnaie), entre −1 et 0 pour un put.</li>
<li><strong>Gamma</strong> : variation du delta quand le sous-jacent bouge. Élevé à la monnaie et près de l'échéance.</li>
<li><strong>Thêta</strong> : perte de valeur par jour qui passe, toutes choses égales par ailleurs. Négatif pour l'acheteur. L'érosion s'accélère à l'approche de l'échéance.</li>
<li><strong>Vega</strong> : variation de la prime pour un point de <strong>volatilité implicite</strong>. Une option devient plus chère quand le marché anticipe plus de mouvements (avant des résultats, par exemple) et peut perdre de la valeur après l'annonce, même si le prix va dans le bon sens.</li>
<li>(Rhô : sensibilité aux taux d'intérêt, en général secondaire.)</li></ul>
</x-approfondi>
<x-note><p>Cette leçon est une introduction. Les modèles de valorisation reposent sur des hypothèses (volatilité constante, distribution des rendements…) qui ne sont pas vérifiées dans la réalité ; les grecques changent en permanence. Le trading d'options demande une formation spécifique bien plus approfondie que ce module.</p></x-note>
<x-fig c="Illustration de la valeur temps d'une option à la monnaie (forme proportionnelle à la racine du temps restant, approximation courante) : elle fond de plus en plus vite près de l'échéance.">""" + SCHEMA_THETA + r"""</x-fig>
<x-exemple>
<p>Call de strike 100, action à 105, prime 7,50 €. Delta 0,60, thêta −0,05 € par jour (valeurs fournies par la plateforme).</p>
<div class="calcul">Valeur intrinsèque = 105 − 100 = 5,00 €
Valeur temps = 7,50 − 5,00 = 2,50 €
Si l'action monte de 1 € (à 106) : prime ≈ 7,50 + 0,60 × 1 = 8,10 €
Si rien ne bouge pendant 10 jours : prime ≈ 7,50 − 10 × 0,05 = 7,00 €
(approximations : delta et thêta changent eux-mêmes avec le prix et le temps)</div>
</x-exemple>
<x-erreurs><ul><li>Acheter une option juste avant une annonce, avoir raison sur le sens, et perdre quand même à cause de la chute de la volatilité implicite.</li><li>Ignorer le thêta : une position qui « ne bouge pas » perd de l'argent chaque jour.</li><li>Prendre les grecques pour des valeurs fixes.</li></ul></x-erreurs>
<x-cles><ul><li>Prime = valeur intrinsèque + valeur temps.</li><li>Delta (prix), gamma (variation du delta), thêta (temps), vega (volatilité implicite).</li><li>Le temps joue contre l'acheteur, et de plus en plus vite près de l'échéance.</li></ul></x-cles>
<x-exo><p>Un put de strike 80 vaut 6 € alors que l'action est à 77 €. Calculez sa valeur intrinsèque et sa valeur temps. Avec un delta de −0,55, que devient approximativement la prime si l'action baisse à 75 € ?</p>
<x-corr><div class="calcul">Valeur intrinsèque = 80 − 77 = 3 €
Valeur temps = 6 − 3 = 3 €
Baisse de 2 € : prime ≈ 6 + (−0,55) × (−2) = 6 + 1,10 = 7,10 €</div></x-corr></x-exo>
"""),

("3-6", "Les warrants et les turbos", r"""
<x-obj><ul><li>Comprendre les produits de bourse à levier vendus aux particuliers.</li><li>Calculer le levier et le risque de désactivation d'un turbo.</li></ul></x-obj>
<x-simple>
<p><strong>Warrants</strong> et <strong>turbos</strong> sont des produits émis par des banques et cotés en bourse (en France notamment sur Euronext). Ils s'achètent comme une action, avec une perte maximale égale à la somme investie.</p>
<ul><li>Un <strong>warrant</strong> fonctionne comme une option (call ou put) avec une échéance, une prime, et une sensibilité au temps et à la volatilité.</li>
<li>Un <strong>turbo</strong> est un produit à levier avec une <strong>barrière désactivante</strong> : si le sous-jacent touche la barrière, le turbo est désactivé (« knock-out »). Il ne vaut alors plus rien, ou seulement une petite valeur résiduelle selon le type de produit.</li></ul>
</x-simple>
<x-approfondi>
<p>La valeur d'un turbo call est à peu près : (prix du sous-jacent − prix d'exercice) ÷ <strong>parité</strong>. La parité indique combien de turbos il faut pour « représenter » une unité de sous-jacent. Il y a peu de valeur temps, ce qui le rend plus lisible qu'un warrant. Les turbos « infinis » (sans échéance) intègrent un coût de financement qui fait évoluer le strike et la barrière chaque jour.</p>
<p>L'émetteur est la contrepartie (risque de crédit de l'émetteur) et le teneur de marché du produit : il fixe les prix d'achat et de vente, et peut ne pas coter dans certaines conditions. Le levier change en permanence : il augmente à mesure qu'on s'approche de la barrière.</p>
<p>Les turbos sont faciles d'accès sur un compte-titres classique, ce qui les rend populaires et dangereux : une barrière peut être touchée en quelques minutes, y compris lors d'un mouvement bref qui se retourne ensuite.</p>
</x-approfondi>
<x-fig c="Un turbo call amplifie la hausse comme la baisse, puis vaut zéro si la barrière est touchée, même si l'indice remonte ensuite.">""" + SCHEMA_TURBO + r"""</x-fig>
<x-exemple>
<p>Indice à 7 500. Turbo call de strike = barrière = 7 000, parité 100.</p>
<div class="calcul">Prix ≈ (7 500 − 7 000) ÷ 100 = 5,00 €
Levier ≈ prix du sous-jacent ÷ (prix du turbo × parité) = 7 500 ÷ (5 × 100) = 15
L'indice monte de 2 % → 7 650 : turbo ≈ (7 650 − 7 000) ÷ 100 = 6,50 € → +30 %
L'indice baisse de 2 % → 7 350 : turbo ≈ 3,50 € → −30 %
L'indice touche 7 000 (−6,7 %) : turbo désactivé → perte de 100 %</div>
</x-exemple>
<x-erreurs><ul><li>Choisir le turbo avec la barrière la plus proche « pour plus de levier ».</li><li>Croire que la désactivation n'arrive qu'en clôture : la barrière s'applique en continu, y compris parfois hors des heures de la bourse sur laquelle le turbo cote.</li><li>Moyenner à la baisse un turbo qui se rapproche de sa barrière.</li></ul></x-erreurs>
<x-cles><ul><li>Warrant ≈ option cotée ; turbo = levier + barrière désactivante.</li><li>Perte maximale = somme investie, mais elle peut être atteinte très vite.</li><li>Levier d'un turbo ≈ prix du sous-jacent ÷ (prix du turbo × parité).</li></ul></x-cles>
<x-exo><p>Action à 60 €. Turbo put (pari sur la baisse) de strike = barrière = 66 €, parité 1. Quel est son prix approximatif et son levier ? Que vaut-il si l'action baisse à 57 € ? Et si elle monte à 66 € ?</p>
<x-corr><div class="calcul">Prix ≈ (66 − 60) ÷ 1 = 6 €
Levier ≈ 60 ÷ 6 = 10
Action à 57 € : (66 − 57) = 9 € → +50 %
Action à 66 € : barrière touchée → désactivé, perte de 100 %</div></x-corr></x-exo>
"""),

("3-7", "Levier, marge, appel de marge et liquidation", r"""
<x-obj><ul><li>Calculer le levier effectif d'un compte.</li><li>Comprendre le niveau de marge, l'appel de marge et la liquidation.</li><li>Calculer le mouvement contraire qui déclenche une liquidation.</li></ul></x-obj>
<x-simple>
<p>L'<strong>effet de levier</strong> est le rapport entre l'exposition (la valeur des positions) et le capital. Avec 1 000 € et un levier de 10, vous contrôlez 10 000 €. Un mouvement de 1 % du marché fait alors varier votre capital de 10 %.</p>
<p>La <strong>marge</strong> est la somme bloquée par le courtier en garantie. Si les pertes font trop baisser votre capital, le courtier lance un <strong>appel de marge</strong> (il faut ajouter des fonds ou réduire les positions), puis <strong>liquide</strong> automatiquement les positions si le seuil de clôture est atteint.</p>
</x-simple>
<x-approfondi>
<div class="formule">Levier effectif = Exposition totale ÷ Capital du compte</div>
<div class="formule">Marge requise = Exposition ÷ Levier maximal autorisé</div>
<div class="formule">Niveau de marge = Fonds propres (capital + gains/pertes latents) ÷ Marge utilisée</div>
<p>Distinguez le <strong>levier maximal</strong> (ce que le courtier autorise : 30:1, par exemple) du <strong>levier effectif</strong> (ce que vous utilisez réellement). Le risque dépend du levier effectif. Un trader peut avoir accès à un levier de 30 et n'utiliser qu'un levier effectif de 2.</p>
<p>Pour les CFD des particuliers européens, le courtier doit clôturer les positions quand le niveau de marge tombe à <strong>50 %</strong>. La liquidation se fait au prix du marché : en cas de mouvement rapide, la perte peut être supérieure à ce seuil.</p>
</x-approfondi>
<x-fig c="Mouvement contraire du marché qui fait perdre 50 % ou 100 % du capital, selon le levier effectif.">""" + SCHEMA_LEVIER + r"""</x-fig>
<x-exemple>
<p>Compte de <strong>2 000 €</strong>. Vous achetez 0,5 lot d'EUR/USD (50 000 €) avec un levier maximal de 30.</p>
<div class="calcul">Marge requise = 50 000 ÷ 30 = 1 666,67 €
Levier effectif = 50 000 ÷ 2 000 = 25
Niveau de marge au départ = 2 000 ÷ 1 666,67 = 120 %
Clôture forcée à 50 % : fonds propres = 50 % × 1 666,67 = 833,33 €
Perte qui déclenche la clôture = 2 000 − 833,33 = 1 166,67 €
Valeur d'un pip pour 0,5 lot = 5 $ ≈ 4,60 € (avec 1 € = 1,087 $)
Mouvement contraire = 1 166,67 ÷ 4,60 ≈ 254 pips, soit environ 2,3 % de baisse de l'euro</div>
<p>Une baisse de 2,3 % de l'EUR/USD n'a rien d'exceptionnel sur quelques semaines : ce trader peut perdre 58 % de son compte sur un mouvement banal. Avec un 1 lot complet, ce ne serait même pas possible (marge de 3 333 € > capital).</p>
</x-exemple>
<x-erreurs><ul><li>Confondre levier maximal autorisé et levier conseillé.</li><li>Ajouter des fonds pour « tenir » une position perdante lors d'un appel de marge.</li><li>Ouvrir plusieurs positions corrélées et découvrir que le levier effectif total est énorme.</li></ul></x-erreurs>
<x-cles><ul><li>Levier effectif = exposition ÷ capital ; c'est lui qui mesure le risque.</li><li>Avec un levier L, un mouvement contraire de 100 % ÷ L efface le capital.</li><li>Appel de marge puis liquidation automatique ; la liquidation peut se faire à un prix défavorable.</li></ul></x-cles>
<x-exo><p>Capital de 5 000 €, positions sur indices pour une exposition totale de 60 000 €. Quel est le levier effectif ? Quel mouvement contraire de l'indice fait perdre 20 % du capital ?</p>
<x-corr><div class="calcul">Levier effectif = 60 000 ÷ 5 000 = 12
Perte de 20 % du capital = 1 000 €
Mouvement = 1 000 ÷ 60 000 ≈ 1,67 % (ou 20 % ÷ 12)</div></x-corr></x-exo>
"""),

("3-8", "Pip, tick, lot et taille de contrat", r"""
<x-obj><ul><li>Maîtriser les unités de mesure des différents marchés.</li><li>Calculer la valeur d'un pip ou d'un tick dans la devise de son compte.</li></ul></x-obj>
<x-simple>
<ul><li><strong>Pip</strong> (Forex) : unité standard de variation, 0,0001 pour la plupart des paires (4<sup>e</sup> décimale), 0,01 pour les paires en yen. Beaucoup de plateformes affichent une décimale de plus : c'est le <strong>pipette</strong> (1/10 de pip).</li>
<li><strong>Lot</strong> (Forex) : taille d'une position. Lot standard = 100 000 unités de la devise de base ; mini-lot = 10 000 ; micro-lot = 1 000.</li>
<li><strong>Tick</strong> : plus petite variation de prix possible sur un contrat à terme ou une action ; chaque tick a une valeur monétaire.</li>
<li><strong>Taille de contrat / multiplicateur</strong> : valeur monétaire d'un point de variation (futures, CFD).</li></ul>
</x-simple>
<x-approfondi>
<div class="formule">Valeur d'un pip = Taille de la position × Taille du pip (exprimée en devise de cotation)</div>
<p>Il faut ensuite convertir dans la devise du compte. Pour EUR/USD, 1 lot = 100 000 × 0,0001 = <strong>10 $ par pip</strong>. Pour USD/JPY, 1 lot = 100 000 × 0,01 = 1 000 ¥ par pip. Pour une paire dont la devise de cotation est l'euro (comme GBP/EUR, rare), la valeur est directement en euros.</p>
<div class="formule">Valeur d'un tick = Taille du tick × Multiplicateur</div>
<p>Exemple : E-mini S&amp;P 500 : tick de 0,25 point × 50 $ = 12,50 $ par tick.</p>
</x-approfondi>
<x-exemple>
<p>Compte en euros, avec EUR/USD = 1,0870 et USD/JPY = 150.</p>
<div class="calcul">EUR/USD, 1 lot : 10 $ par pip → 10 ÷ 1,087 ≈ 9,20 € par pip
EUR/USD, 0,3 lot : 0,3 × 9,20 ≈ 2,76 € par pip
USD/JPY, 1 lot : 1 000 ¥ par pip → 1 000 ÷ 150 ≈ 6,67 $ → 6,67 ÷ 1,087 ≈ 6,13 € par pip
Mouvement de 45 pips sur 0,3 lot d'EUR/USD : 45 × 2,76 ≈ 124 €</div>
</x-exemple>
<x-erreurs><ul><li>Confondre pip et pipette (erreur d'un facteur 10 sur le risque).</li><li>Supposer qu'un pip vaut toujours 10 € par lot, quelle que soit la paire.</li><li>Ignorer la valeur du point d'un CFD : selon le courtier, 1 contrat peut valoir 1 €, 10 € ou 25 € par point.</li></ul></x-erreurs>
<x-cles><ul><li>Pip = 0,0001 (0,01 pour le yen) ; lot standard = 100 000 unités.</li><li>Valeur du pip = taille × 0,0001 en devise de cotation, puis conversion.</li><li>Valeur du tick = taille du tick × multiplicateur.</li></ul></x-cles>
<x-exo><p>Vous tradez 0,2 lot de GBP/USD (1 € = 1,087 $). Combien vaut un pip en euros ? Votre stop est à 35 pips : combien risquez-vous ?</p>
<x-corr><div class="calcul">1 lot = 10 $ par pip → 0,2 lot = 2 $ par pip
2 ÷ 1,087 ≈ 1,84 € par pip
Risque = 35 × 1,84 ≈ 64,40 €</div></x-corr></x-exo>
"""),

("3-9", "Tous les frais : commissions, spread, financement, change", r"""
<x-obj><ul><li>Recenser tous les coûts d'un trade.</li><li>Calculer le coût du financement overnight et du swap.</li></ul></x-obj>
<x-simple>
<p>Le coût d'un trade ne se limite pas à la commission affichée. Il faut additionner :</p>
<ul><li>la <strong>commission</strong> (fixe, en % du montant, ou par contrat) ;</li><li>le <strong>spread</strong> (coût implicite, leçon 2.1) ;</li><li>le <strong>slippage</strong> ;</li><li>le <strong>financement overnight</strong> ou <strong>swap</strong> pour les positions à levier conservées la nuit ;</li><li>les <strong>frais de change</strong> si l'actif est dans une autre devise ;</li><li>d'autres frais éventuels : droits de garde, frais d'inactivité, abonnements aux données, taxes (en France, une taxe sur les transactions financières s'applique à l'achat de certaines grandes valeurs françaises).</li></ul>
</x-simple>
<x-approfondi>
<p><strong>Financement des CFD</strong> : chaque nuit, une position acheteuse paie en général un intérêt calculé sur la valeur de la position, du type (taux de référence + marge du courtier) × notionnel ÷ 365 (ou 360 selon les courtiers). Une position vendeuse peut recevoir ou payer selon le niveau des taux.</p>
<p><strong>Swap sur le Forex</strong> : il dépend de l'écart de taux d'intérêt entre les deux devises, moins une marge du courtier. Il peut être positif ou négatif. Le mercredi, il est souvent <strong>triplé</strong> pour couvrir le week-end (lié aux délais de règlement des devises).</p>
<p>Les grilles tarifaires changent souvent : consultez toujours le document tarifaire et le document d'informations clés (DIC) du produit.</p>
</x-approfondi>
<x-exemple>
<p>Vous détenez un CFD sur un indice : 1 contrat à 1 € le point, indice à 7 500. Taux de financement annuel = 4,5 % (illustratif). Marge requise : 5 %.</p>
<div class="calcul">Notionnel = 7 500 × 1 = 7 500 €
Marge = 7 500 × 5 % = 375 €
Financement par nuit = 7 500 × 4,5 % ÷ 365 ≈ 0,92 €
Sur 30 nuits ≈ 27,74 €, soit 27,74 ÷ 375 ≈ 7,4 % de la marge immobilisée
Sur un an ≈ 337,50 €, soit 90 % de la marge</div>
<p>Le coût paraît dérisoire par nuit, mais il est énorme rapporté à la somme réellement engagée.</p>
</x-exemple>
<x-erreurs><ul><li>Choisir un courtier « sans commission » sans regarder ses spreads et son financement.</li><li>Garder des positions à levier pendant des mois.</li><li>Oublier les frais de change sur des actions étrangères (aller et retour).</li></ul></x-erreurs>
<x-cles><ul><li>Coût total = commission + spread + slippage + financement + change + autres frais.</li><li>Financement ≈ notionnel × taux × nombre de nuits ÷ 365 (ou 360).</li><li>Swap Forex : selon l'écart de taux, souvent triplé le mercredi.</li></ul></x-cles>
<x-exo><p>Vous achetez pour 4 000 $ d'actions américaines avec un compte en euros. Frais de change : 0,25 % à l'achat et à la vente. Commission : 2 $ par ordre. Spread : 0,05 %. Quel est le coût total approximatif d'un aller-retour, en dollars ?</p>
<x-corr><div class="calcul">Change : 4 000 × 0,25 % × 2 = 20 $
Commissions : 2 × 2 = 4 $
Spread : 4 000 × 0,05 % = 2 $
Total ≈ 26 $, soit 0,65 % du montant</div><p>Il faut donc que l'action monte d'environ 0,65 % pour couvrir les frais.</p></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Familles</h2><ul><li>Comptant : on possède l'actif.</li><li>Dérivés fermes (futures, CFD), optionnels (options, warrants), à barrière (turbos).</li><li>Perte &gt; mise possible : futures, vente d'options.</li></ul></div>
<div class="encadre"><h2>CFD (particuliers UE)</h2><ul><li>Levier max : 30 (FX majeures), 20 (indices majeurs, or), 10, 5 (actions), 2 (cryptos).</li><li>Clôture à 50 % de marge ; protection contre le solde négatif.</li><li>Coûts : spread, commission, financement.</li></ul></div>
<div class="encadre"><h2>Futures</h2><ul><li>Standardisés, en bourse, chambre de compensation.</li><li>Résultat = points × valeur du point × contrats.</li><li>Appels de marge quotidiens ; échéance et roll.</li></ul></div>
<div class="encadre"><h2>Options</h2><ul><li>Call = droit d'acheter ; put = droit de vendre.</li><li>Acheteur : perte max = prime. Vendeur : gain max = prime.</li><li>Point mort : K + prime (call) ; K − prime (put).</li><li>Prime = intrinsèque + valeur temps.</li><li>Delta, gamma, thêta, vega.</li></ul></div>
<div class="encadre"><h2>Turbos</h2><ul><li>Valeur ≈ (S − strike) ÷ parité.</li><li>Barrière touchée ⇒ désactivation.</li><li>Levier ≈ S ÷ (prix × parité).</li></ul></div>
<div class="encadre"><h2>Levier &amp; marge</h2><ul><li>Levier effectif = exposition ÷ capital.</li><li>Marge = exposition ÷ levier max.</li><li>Capital effacé par un mouvement de 100 % ÷ levier.</li></ul></div>
<div class="encadre"><h2>Unités</h2><ul><li>Pip = 0,0001 (yen : 0,01) ; lot = 100 000.</li><li>EUR/USD : 1 lot = 10 $/pip.</li><li>Tick : E-mini S&amp;P 0,25 × 50 $ = 12,50 $.</li></ul></div>
<div class="encadre"><h2>Frais</h2><ul><li>Commission + spread + slippage + financement + change + autres.</li><li>Financement ≈ notionnel × taux × nuits ÷ 365.</li></ul></div>
"""

QUIZ = [
("Quel produit donne à son acheteur un droit, mais pas une obligation ?", ["Un future", "Un CFD", "Une option", "Une action"], 2, "L'option donne un droit d'acheter (call) ou de vendre (put) ; l'acheteur n'est pas obligé de l'exercer."),
("Levier maximal sur les CFD d'actions individuelles pour un particulier en Europe :", ["30:1", "20:1", "5:1", "100:1"], 2, "Les actions individuelles sont limitées à 5:1, soit 20 % de marge minimale."),
("Que garantit la protection contre le solde négatif sur les CFD ?", ["Qu'on ne perd jamais d'argent", "Que la perte ne dépasse pas les fonds du compte CFD", "Que le stop est exécuté au prix exact", "Que le financement est gratuit"], 1, "La perte totale ne peut pas dépasser les fonds déposés sur le compte. Cela n'empêche pas de perdre tout le compte."),
("1 future à 10 € le point, acheté à 4 800, revendu à 4 765. Résultat ?", ["−35 €", "−350 €", "+350 €", "−3 500 €"], 1, "(4 765 − 4 800) × 10 = −35 × 10 = −350 €."),
("Call de strike 50 acheté 3 €. À l'échéance, l'action vaut 51 €. Résultat par action ?", ["+1 €", "−2 €", "+4 €", "−3 €"], 1, "Valeur à l'échéance = 51 − 50 = 1 € ; résultat = 1 − 3 = −2 €. Le point mort est 53 €."),
("La valeur temps d'une option :", ["Augmente à l'approche de l'échéance", "Vaut zéro à l'échéance", "Est toujours égale à la valeur intrinsèque", "Ne dépend pas de la volatilité"], 1, "À l'échéance, il ne reste que la valeur intrinsèque ; la valeur temps fond, de plus en plus vite près de l'échéance."),
("Le delta d'un call mesure :", ["La perte de valeur par jour", "La variation de la prime pour 1 € de variation du sous-jacent", "La sensibilité à la volatilité", "Le prix d'exercice"], 1, "Le thêta mesure le temps, le vega la volatilité ; le delta mesure la sensibilité au prix du sous-jacent."),
("Turbo call, strike = barrière = 4 000, parité 10, indice à 4 200. Prix approximatif ?", ["2 €", "20 €", "200 €", "420 €"], 1, "(4 200 − 4 000) ÷ 10 = 20 €."),
("Capital 3 000 €, exposition 45 000 €. Levier effectif ?", ["3", "10", "15", "30"], 2, "45 000 ÷ 3 000 = 15. Un mouvement contraire de 100 % ÷ 15 ≈ 6,7 % effacerait le capital."),
("Avec un levier effectif de 20, quel mouvement contraire efface tout le capital ?", ["2 %", "5 %", "10 %", "20 %"], 1, "100 % ÷ 20 = 5 %."),
("Valeur d'un pip pour 1 lot standard d'EUR/USD :", ["1 $", "10 $", "100 $", "10 €"], 1, "100 000 × 0,0001 = 10 $, à convertir dans la devise du compte."),
("Notionnel de 10 000 €, taux de financement 5 % par an, 73 nuits (base 365). Coût du financement ?", ["10 €", "50 €", "100 €", "500 €"], 2, "10 000 × 5 % × 73 ÷ 365 = 500 × 0,2 = 100 €."),
]
