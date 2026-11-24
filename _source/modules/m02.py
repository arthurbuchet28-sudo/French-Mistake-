from svgkit import plot, table, svg, t, line, arrow, path_from, candles

NUM = 2
TITRE = "Fonctionnement d'un ordre"
RESUME = "Bid, ask, spread, carnet d'ordres ; ordres au marché, à cours limité, stop, trailing, OCO ; slippage, gaps, positions longues et courtes."
DUREE = "2 h 15"
INTRO = r"""<p>Savoir <em>quoi</em> trader ne suffit pas : il faut savoir <em>comment</em> passer un ordre, à quel prix il sera exécuté, et ce qui peut mal tourner entre le moment où vous cliquez et celui où l'ordre est réellement exécuté. Ce module est très concret : la plupart des « mauvaises surprises » des débutants viennent d'une mauvaise compréhension des ordres.</p>"""


def _bidask():
    W = 640
    p = [line(60, 40, 60, 210, "g-axe")]
    niveaux = [(60, "Ask (vendeur) : 50,05 €", "g-lb", "← vous ACHETEZ à ce prix"), (125, "Prix « milieu » : 50,00 €", "g-l3", ""),
               (190, "Bid (acheteur) : 49,95 €", "g-lh", "← vous VENDEZ à ce prix")]
    for y, lab, cls, note in niveaux:
        p.append(line(60, y, 330, y, cls))
        p.append(t(70, y - 7, lab, "g-txt g-fort"))
        if note:
            p.append(t(345, y + 4, note, "g-txt"))
    p.append(arrow(300, 125, 300, 64))
    p.append(arrow(300, 125, 300, 186))
    p.append(t(470, 125, "Spread = 50,05 − 49,95 = 0,10 €", "g-txt g-fort", "middle"))
    p.append(t(470, 145, "(0,2 % du prix milieu)", "g-txt", "middle"))
    p.append(t(30, 125, "Prix", "g-txt", "middle", extra=' transform="rotate(-90 30 125)"'))
    return svg(W, 230, "".join(p), "Bid, ask et spread")


SCHEMA_BIDASK = _bidask()

SCHEMA_PROFONDEUR = plot(
    [{"x": [49.97, 49.98, 49.99, 50.00, 50.01], "y": [900, 600, 350, 500, 250], "kind": "bar", "cls": "g-barre-h", "bw": 24, "label": "Ordres d'achat en attente (bid)"},
     {"x": [50.05, 50.06, 50.08, 50.10], "y": [400, 300, 500, 800], "kind": "bar", "cls": "g-barre-b", "bw": 24, "label": "Ordres de vente en attente (ask)"}],
    label="Profondeur du carnet d'ordres", xr=(49.95, 50.12), yr=(0, 1000), xlabel="Prix (€)",
    xticks=[49.97, 49.99, 50.01, 50.03, 50.05, 50.07, 50.09, 50.11], xfmt=lambda v: f"{v:.2f}".replace(".", ","),
    yfmt=lambda v: f"{v:.0f}")


def _quadrants():
    W = 660
    p = [line(20, 130, W - 20, 130, "g-l1"), t(W / 2, 124, "Prix actuel du marché", "g-txt g-fort", "middle")]
    cases = [(30, 20, "g-rect-h", "STOP D'ACHAT (buy stop)", "Acheter si le prix MONTE jusqu'ici :", "entrer sur une cassure, ou couper une vente"),
             (345, 20, "g-rect-b", "LIMITE DE VENTE (sell limit)", "Vendre si le prix MONTE jusqu'ici :", "prendre son bénéfice, ou vendre plus cher"),
             (30, 145, "g-rect-h", "LIMITE D'ACHAT (buy limit)", "Acheter si le prix BAISSE jusqu'ici :", "acheter moins cher (sur un repli)"),
             (345, 145, "g-rect-b", "STOP DE VENTE (sell stop)", "Vendre si le prix BAISSE jusqu'ici :", "stop loss d'un achat, ou vente sur cassure")]
    for x, y, cls, a, b, c in cases:
        p.append(f'<rect x="{x}" y="{y}" width="285" height="88" rx="8" class="{cls}"/>')
        p.append(t(x + 142, y + 26, a, "g-txt g-fort", "middle"))
        p.append(t(x + 142, y + 50, b, "g-txt", "middle"))
        p.append(t(x + 142, y + 70, c, "g-txt g-petit", "middle"))
    p.append(t(W / 2, 252, "Au-dessus du prix : stop d'achat ou limite de vente.  En dessous : limite d'achat ou stop de vente.", "g-txt g-petit", "middle"))
    return svg(W, 262, "".join(p), "Où placer chaque type d'ordre par rapport au prix actuel")


SCHEMA_QUADRANTS = _quadrants()

_tr = path_from([(0, 100), (6, 104), (12, 110), (16, 107), (20, 112), (25, 104), (30, 100)], seed=3, noise=0.6, wick=0.8)[:24]
_stops, _st, _hh = [], None, 0
for _i, (_o, _h, _l, _c) in enumerate(_tr):
    _stops.append(_st)
    _hh = max(_hh, _h)
    _s = round(_hh - 5, 2)
    _st = _s if _st is None else max(_st, _s)
SCHEMA_TRAILING = candles(_tr, label="Trailing stop qui suit les plus hauts à 5 € de distance",
                          overlays=[{"values": _stops, "cls": "g-lb"}],
                          marks=[{"i": 0, "p": 99.2, "t": "Achat à 100", "pos": "bas", "anchor": "start"},
                                 {"i": 23, "p": 107.58, "t": "Stop touché ≈ 107,58", "pos": "bas", "anchor": "end"}],
                          legend=[("g-lb", "Trailing stop (plus haut atteint − 5 €)")])

_gap = path_from([(0, 52), (10, 50.5), (15, 51)], seed=5, noise=0.4, wick=0.4)
_gap2 = path_from([(0, 44.2), (6, 43.5), (10, 44.5)], seed=6, noise=0.4, wick=0.4)
_gap2[0] = (44.0, 44.8, 43.6, 44.3)
SCHEMA_GAP = candles(_gap + _gap2, label="Gap baissier qui saute par-dessus un stop",
                     lines=[{"y": 47, "cls": "g-lb", "label": "Stop de vente à 47 €"}],
                     marks=[{"i": 16, "p": 44.0, "t": "Ouverture à 44 € : exécution ≈ 44 €", "pos": "bas", "anchor": "start"}])

SCHEMA_LONGSHORT = plot(
    [{"x": [0, 100], "y": [-50, 50], "cls": "g-lh", "label": "Position longue (achat à 50)"},
     {"x": [0, 100], "y": [50, -50], "cls": "g-lb", "label": "Position courte (vente à 50)"}],
    label="Gain ou perte par action selon le prix final, pour un achat et une vente à découvert à 50",
    xlabel="Prix de l'action au moment de clôturer (€)", xr=(0, 100), yr=(-55, 55),
    vlines=[{"x": 50, "label": "Entrée 50 €", "cls": "g-l3 g-fin"}],
    marks=[{"x": 0, "y": -50, "t": "Perte max de l'acheteur : −50 €", "dx": 10, "dy": -6}],
    texts=[{"x": 52, "y": -40, "t": "Perte du vendeur à découvert : sans limite →"}],
    yfmt=lambda v: f"{v:+.0f} €".replace("+0", "0"))

LECONS = [
("2-1", "Bid, ask et spread", r"""
<x-obj><ul><li>Comprendre qu'il existe toujours deux prix : un prix d'achat et un prix de vente.</li><li>Calculer le coût du spread sur un trade.</li></ul></x-obj>
<x-simple>
<p>À chaque instant, un actif a <strong>deux prix</strong> :</p>
<ul><li>le <strong>bid</strong> (« offre d'achat ») : le meilleur prix auquel quelqu'un accepte d'<em>acheter</em>. C'est le prix auquel <strong>vous pouvez vendre</strong> immédiatement ;</li>
<li>l'<strong>ask</strong> (ou « offer », demande) : le meilleur prix auquel quelqu'un accepte de <em>vendre</em>. C'est le prix auquel <strong>vous pouvez acheter</strong> immédiatement.</li></ul>
<p>L'ask est toujours supérieur au bid. L'écart entre les deux est le <strong>spread</strong>. C'est un coût : si vous achetez puis revendez immédiatement, vous perdez le spread.</p>
</x-simple>
<x-fig c="Vous achetez au prix le plus haut (ask) et vendez au prix le plus bas (bid) : le spread est un coût à chaque aller-retour.">""" + SCHEMA_BIDASK + r"""</x-fig>
<x-approfondi>
<p>Le spread dépend de la <strong>liquidité</strong> (actif très échangé = spread étroit), de la <strong>volatilité</strong> (marché agité = spread plus large), de l'<strong>heure</strong> (plus large hors des heures principales, à l'ouverture, ou autour d'annonces économiques) et du <strong>courtier</strong> (certains se rémunèrent en élargissant le spread plutôt que par une commission).</p>
<p>Les graphiques affichent généralement le prix <em>bid</em>. Conséquence pratique : un ordre d'achat peut être exécuté (au prix ask) alors que le graphique n'a pas « touché » votre niveau. De même, un stop de vente sur une position courte se déclenche sur l'ask. Le spread s'exprime en devise, en pourcentage du prix, ou en pips sur le Forex.</p>
</x-approfondi>
<x-exemple>
<p><strong>Action</strong> : bid 49,95 €, ask 50,05 €. Vous achetez 200 actions puis les revendez aussitôt.</p>
<div class="calcul">Achat : 200 × 50,05 = 10 010 €
Revente : 200 × 49,95 = 9 990 €
Perte = 20 € = 200 × 0,10 € de spread
Spread en % du prix milieu = 0,10 ÷ 50,00 = 0,2 %</div>
<p><strong>Forex</strong> : EUR/USD bid 1,08480, ask 1,08490. Spread = 0,0001 = 1 pip. Sur 1 lot standard (100 000 €), 1 pip vaut 10 $ : chaque aller-retour coûte donc 10 $ de spread.</p>
</x-exemple>
<x-erreurs><ul><li>Croire qu'on achète au prix affiché sur le graphique (souvent le bid).</li><li>Trader des actifs à spread large sur de petits mouvements : le spread mange tout le gain.</li><li>Ouvrir une position juste avant une annonce économique, quand le spread s'élargit brutalement.</li></ul></x-erreurs>
<x-cles><ul><li>Bid = prix auquel vous vendez ; ask = prix auquel vous achetez.</li><li>Spread = ask − bid : un coût payé à chaque aller-retour.</li><li>Il s'élargit quand la liquidité baisse ou que la volatilité augmente.</li></ul></x-cles>
<x-exo><p>Une petite capitalisation affiche bid 7,80 € et ask 7,95 €. Quel est le spread en % du prix milieu ? De combien le cours doit-il monter (en %) pour qu'un achat suivi d'une revente soit à l'équilibre, hors commissions ?</p>
<x-corr><div class="calcul">Spread = 7,95 − 7,80 = 0,15 €
Prix milieu = (7,80 + 7,95) ÷ 2 = 7,875 €
Spread en % = 0,15 ÷ 7,875 ≈ 1,9 %
Équilibre : le bid doit passer de 7,80 à 7,95 (votre prix d'achat), soit +0,15 €, ≈ +1,9 %</div><p>Il faut un mouvement de près de 2 % juste pour revenir à zéro. Sur ce type de titre, le trading à court terme est très coûteux.</p></x-corr></x-exo>
"""),

("2-2", "Le carnet d'ordres et la profondeur de marché", r"""
<x-obj><ul><li>Lire un carnet d'ordres.</li><li>Comprendre comment un gros ordre au marché « remonte » le carnet.</li></ul></x-obj>
<x-simple>
<p>Le <strong>carnet d'ordres</strong> liste tous les ordres à cours limité en attente : à gauche les acheteurs (bid) avec leur prix et leur quantité, à droite les vendeurs (ask). Le meilleur bid et le meilleur ask forment la « fourchette ». La <strong>profondeur de marché</strong> (market depth, ou niveau 2) est la quantité disponible à chaque niveau de prix.</p>
</x-simple>
""" + table(["Quantité (achat)", "Prix bid", "Prix ask", "Quantité (vente)"],
            [["250", "50,01", "50,05", "400"], ["500", "50,00", "50,06", "300"], ["350", "49,99", "50,08", "500"], ["600", "49,98", "50,10", "800"], ["900", "49,97", "", ""]]) + r"""
<x-fig c="La même information sous forme graphique : quantités en attente à chaque prix.">""" + SCHEMA_PROFONDEUR + r"""</x-fig>
<x-approfondi>
<p>Quand un ordre au marché arrive, il « consomme » les ordres en attente en commençant par le meilleur prix, puis passe au niveau suivant si la quantité ne suffit pas. Le prix moyen d'exécution peut donc être moins bon que le prix affiché. Ce phénomène s'appelle l'<strong>impact de marché</strong>.</p>
<p>Limites : sur les actions, le carnet d'une bourse n'est qu'une partie de la liquidité (il existe d'autres plateformes et des « dark pools »). Les gros acteurs ne montrent souvent qu'une fraction de leur ordre (ordres « iceberg »). Sur le Forex et les CFD, il n'existe pas de carnet central : la profondeur affichée est celle d'un fournisseur de liquidité particulier. Le carnet est donc utile, mais il ne montre jamais tout.</p>
</x-approfondi>
<x-exemple>
<p>Avec le carnet ci-dessus, vous passez un ordre d'achat au marché de <strong>1 500 actions</strong>.</p>
<div class="calcul">400 × 50,05 = 20 020,00 €
300 × 50,06 = 15 018,00 €
500 × 50,08 = 25 040,00 €
300 × 50,10 = 15 030,00 €   (il en reste 500 à ce prix dans le carnet)
Total = 1 500 actions pour 75 108,00 €
Prix moyen = 75 108 ÷ 1 500 = 50,072 €
Écart avec le meilleur ask : 50,072 − 50,05 = 0,022 € par action, soit 33 € au total</div>
<p>Après votre ordre, le meilleur ask est remonté à 50,10 € : vous avez fait bouger le prix.</p>
</x-exemple>
<x-erreurs><ul><li>Passer un gros ordre au marché sur un titre peu liquide sans regarder le carnet.</li><li>Croire qu'un gros ordre affiché est une « intention ferme » : il peut être annulé à tout moment.</li></ul></x-erreurs>
<x-cles><ul><li>Le carnet liste les ordres limités en attente, côté achat et côté vente.</li><li>Un ordre au marché consomme le carnet niveau par niveau ; le prix moyen peut se dégrader.</li><li>Le carnet visible n'est qu'une partie de la liquidité réelle.</li></ul></x-cles>
<x-exo><p>Avec le même carnet, vous vendez <strong>1 200 actions</strong> au marché. Quel est votre prix moyen d'exécution ?</p>
<x-corr><div class="calcul">250 × 50,01 = 12 502,50 €
500 × 50,00 = 25 000,00 €
350 × 49,99 = 17 496,50 €
100 × 49,98 =  4 998,00 €
Total = 1 200 actions pour 59 997,00 €
Prix moyen = 59 997 ÷ 1 200 = 49,9975 €</div><p>Soit 0,0125 € de moins par action que le meilleur bid (50,01 €).</p></x-corr></x-exo>
"""),

("2-3", "Ordres au marché et ordres à cours limité", r"""
<x-obj><ul><li>Savoir choisir entre un ordre au marché et un ordre à cours limité.</li><li>Comprendre le compromis entre garantie de prix et garantie d'exécution.</li></ul></x-obj>
<x-simple>
<ul><li><strong>Ordre au marché</strong> : « achetez (ou vendez) tout de suite, au meilleur prix disponible ». Exécution quasi certaine sur un marché liquide, mais <strong>pas de garantie de prix</strong>.</li>
<li><strong>Ordre à cours limité</strong> (limit order) : « achetez au maximum à X » ou « vendez au minimum à Y ». <strong>Garantie de prix</strong> (vous n'aurez pas pire que votre limite), mais <strong>pas de garantie d'exécution</strong> : si le prix n'atteint pas votre limite, rien ne se passe.</li></ul>
</x-simple>
<x-approfondi>
<p>Un ordre limité d'achat se place en général <strong>sous</strong> le prix actuel (on espère acheter moins cher), un ordre limité de vente <strong>au-dessus</strong>. Un ordre limité placé « du mauvais côté » (achat limité au-dessus de l'ask) est exécuté immédiatement, au meilleur prix disponible jusqu'à votre limite : c'est un « ordre au marché protégé », pratique pour éviter un prix aberrant.</p>
<p>Un ordre limité s'exécute à votre prix <strong>ou mieux</strong> : si le marché ouvre en baisse sous votre limite d'achat, vous achetez au prix d'ouverture, plus bas. Il peut aussi n'être exécuté que <strong>partiellement</strong> s'il n'y a pas assez de contrepartie. En bourse, les ordres limités sont servis par ordre de prix puis d'arrivée (priorité prix-temps).</p>
<p>Il existe d'autres types, plus rares : l'ordre « à la meilleure limite » (exécuté au meilleur prix du côté opposé, le reste devenant un ordre limité à ce prix), ou les ordres réservés aux enchères d'ouverture et de clôture.</p>
</x-approfondi>
<x-exemple>
<p>Une action cote 50,00 / 50,05. Vous voulez l'acheter, mais trouvez le prix élevé. Vous placez un <strong>achat limité à 49,50 €</strong> pour 100 actions.</p>
<ul><li><strong>Scénario 1</strong> : le prix descend à 49,40 puis remonte. Votre ordre est exécuté à 49,50 € (ou mieux). Coût : 100 × 49,50 = 4 950 €, soit 55 € d'économie par rapport à un achat au marché à 50,05.</li>
<li><strong>Scénario 2</strong> : le prix monte directement à 53 €. Votre ordre n'est jamais exécuté. Vous avez « raté » un gain de 100 × (53 − 50,05) = 295 €.</li>
<li><strong>Scénario 3</strong> : après une mauvaise nouvelle, l'action ouvre à 47 €. Votre ordre est exécuté à 47 € (mieux que votre limite)… mais vous achetez un titre qui vient de chuter pour une raison que vous ignorez peut-être.</li></ul>
</x-exemple>
<x-erreurs><ul><li>Passer un ordre au marché sur un titre peu liquide ou en dehors des heures principales.</li><li>Oublier un ordre limité en attente, qui s'exécute des jours plus tard dans un contexte différent.</li><li>Placer une limite trop ambitieuse et ne jamais être exécuté, puis courir après le prix au marché (FOMO).</li></ul></x-erreurs>
<x-cles><ul><li>Au marché : exécution garantie (en pratique), prix non garanti.</li><li>Limité : prix garanti (ou mieux), exécution non garantie.</li><li>Sur les titres peu liquides, privilégiez les ordres limités.</li></ul></x-cles>
<x-exo><p>Vous détenez 300 actions achetées à 40 €. Elles cotent 44,80 / 44,85. Vous voulez vendre si elles atteignent 46 €. Quel ordre placez-vous, à quel prix ? Que gagnez-vous s'il est exécuté (hors frais) ?</p>
<x-corr><p>Un <strong>ordre de vente à cours limité à 46 €</strong>, placé au-dessus du prix actuel. S'il est exécuté :</p><div class="calcul">Gain = 300 × (46 − 40) = 300 × 6 = 1 800 €</div></x-corr></x-exo>
"""),

("2-4", "Ordres stop, stop-limite et trailing stop", r"""
<x-obj><ul><li>Comprendre le fonctionnement d'un ordre stop et ses différences avec un ordre limité.</li><li>Utiliser un stop-limite et un trailing stop en connaissant leurs limites.</li></ul></x-obj>
<x-simple>
<p>Un <strong>ordre stop</strong> (stop au marché) reste « dormant » jusqu'à ce que le prix atteigne un niveau de déclenchement. Il devient alors un <strong>ordre au marché</strong>. Son usage principal est le <strong>stop loss</strong> : « si le prix descend à 47, vendez pour limiter ma perte ». On l'utilise aussi pour <strong>entrer</strong> sur une cassure : « si le prix dépasse 52, achetez ».</p>
</x-simple>
<x-fig c="Les quatre ordres « en attente » selon leur position par rapport au prix actuel.">""" + SCHEMA_QUADRANTS + r"""</x-fig>
<x-approfondi>
<ul><li><strong>Stop (au marché)</strong> : une fois déclenché, il est exécuté au prix disponible, qui peut être moins bon que le niveau du stop (slippage, leçon 2.6). Il garantit la <em>sortie</em>, pas le <em>prix</em>.</li>
<li><strong>Stop-limite</strong> : une fois déclenché, il devient un ordre <em>limité</em>. Exemple : déclenchement à 47, limite à 46,80. Vous ne vendrez pas sous 46,80… mais si le prix chute directement à 45, vous ne vendrez pas du tout et resterez en position pendant la chute. Pour un stop loss, c'est dangereux.</li>
<li><strong>Trailing stop</strong> (stop suiveur) : un stop qui se déplace automatiquement dans le sens favorable, à une distance fixe (en prix ou en %) du meilleur cours atteint. Il ne recule jamais. Il permet de « laisser courir » un gain tout en le protégeant. Attention : selon les plateformes, il peut être géré par le serveur du courtier ou seulement par votre logiciel, qui doit alors rester ouvert.</li>
<li><strong>Stop garanti</strong> : proposé par certains courtiers en CFD, contre une prime. Il est exécuté exactement au niveau choisi, même en cas de gap.</li></ul>
</x-approfondi>
<x-exemple>
<p>Vous achetez à 100 € avec un <strong>trailing stop de 5 €</strong>.</p>
<div class="calcul">Le prix monte à 104 → le stop monte à 104 − 5 = 99
Le prix monte à 110,83 → le stop monte à 105,83
Le prix monte à 111,02 → le stop monte à 106,02
Le prix redescend à 107,36 → le stop reste à 106,02 (il ne recule jamais)
Nouveau plus haut à 112,58 → le stop monte à 107,58
Le prix chute sous 107,58 → vente déclenchée vers 107,58
Gain ≈ 107,58 − 100 = +7,58 € par action</div>
</x-exemple>
<x-fig c="Le trailing stop suit les plus hauts et ne recule jamais. Il finit par être touché lors d'un repli plus fort que 5 €.">""" + SCHEMA_TRAILING + r"""</x-fig>
<x-erreurs><ul><li>Utiliser un stop-limite comme stop loss et rester bloqué en position pendant une chute.</li><li>Placer un trailing stop trop serré : il est touché par le moindre « bruit » et coupe des trades qui auraient bien tourné.</li><li>Croire qu'un stop garantit le prix de sortie (seul un stop garanti le fait).</li><li>Déplacer son stop loss plus loin quand le prix s'en approche, « pour lui laisser de l'air ».</li></ul></x-erreurs>
<x-cles><ul><li>Stop = ordre au marché déclenché à un niveau : sortie garantie, prix non garanti.</li><li>Stop-limite = prix plafonné, mais risque de non-exécution.</li><li>Trailing stop = stop qui suit le prix dans le sens favorable et ne recule jamais.</li></ul></x-cles>
<x-exo><p>Vous êtes vendeur à découvert à 80 €, avec un trailing stop de 4 €. Le prix baisse à 76, puis 71, remonte à 73, baisse à 69, puis remonte à 75. Où se trouve le stop à chaque étape, et à quel prix sortez-vous (sans slippage) ?</p>
<x-corr><div class="calcul">Départ : stop à 80 + 4 = 84
Plus bas à 76 → stop à 80
Plus bas à 71 → stop à 75
Remontée à 73 → stop reste à 75 (pas touché)
Plus bas à 69 → stop à 73
Remontée à 75 → touché à 73 → rachat à 73
Gain = 80 − 73 = +7 € par action</div><p>Pour une vente, le trailing stop se place <em>au-dessus</em> du prix et descend avec les plus bas.</p></x-corr></x-exo>
"""),

("2-5", "Ordres OCO, ordres liés et durée de validité", r"""
<x-obj><ul><li>Encadrer une position avec un stop et un objectif liés (OCO).</li><li>Choisir la durée de validité d'un ordre.</li></ul></x-obj>
<x-simple>
<p>Un ordre <strong>OCO</strong> (One Cancels the Other, « l'un annule l'autre ») associe deux ordres : quand l'un est exécuté, l'autre est automatiquement annulé. Usage typique : un <strong>take profit</strong> (limite de vente au-dessus) et un <strong>stop loss</strong> (stop de vente en dessous) sur une position achetée. Les plateformes proposent souvent des <strong>ordres liés</strong> (« bracket ») : l'entrée, le stop et l'objectif sont saisis ensemble.</p>
</x-simple>
<x-approfondi>
<p><strong>Durées de validité courantes</strong> :</p>
<ul><li><strong>Jour</strong> : l'ordre expire en fin de séance s'il n'est pas exécuté.</li>
<li><strong>À révocation</strong> (GTC, good till cancelled) : il reste actif jusqu'à exécution ou annulation. Les courtiers imposent souvent une durée maximale.</li>
<li><strong>À date</strong> (GTD) : jusqu'à une date choisie.</li>
<li><strong>Exécuter ou annuler</strong> (IOC) : exécuté immédiatement pour la quantité disponible, le reste est annulé.</li>
<li><strong>Tout ou rien</strong> (FOK, fill or kill) : exécuté immédiatement et en totalité, ou annulé.</li></ul>
<p>Points d'attention : un ordre peut être annulé ou ajusté lors d'opérations sur titres (division d'action, détachement de dividende selon les marchés et les courtiers). Vérifiez régulièrement vos ordres en attente.</p>
</x-approfondi>
<x-exemple>
<p>Vous achetez 100 actions à 50 €. Vous placez un OCO : vente limitée à 56 € (objectif) et stop de vente à 47 €.</p>
<div class="calcul">Si l'objectif est atteint : gain = 100 × (56 − 50) = +600 € ; le stop est annulé
Si le stop est touché     : perte ≈ 100 × (47 − 50) = −300 € ; l'objectif est annulé
Rapport gain potentiel / perte potentielle = 600 ÷ 300 = 2</div>
<p>Sans le lien OCO, si l'objectif est atteint et que le stop reste actif par oubli, il pourrait plus tard <em>ouvrir une position courte</em> non voulue si le prix redescend à 47 €.</p>
</x-exemple>
<x-erreurs><ul><li>Laisser un stop orphelin actif après la clôture d'une position.</li><li>Oublier qu'un ordre « jour » a expiré et croire que la position est protégée le lendemain.</li><li>Ne pas vérifier ses ordres après une division d'action ou un dividende.</li></ul></x-erreurs>
<x-cles><ul><li>OCO : deux ordres liés, l'exécution de l'un annule l'autre.</li><li>Bracket = entrée + stop + objectif saisis ensemble.</li><li>Choisissez et vérifiez la durée de validité de chaque ordre.</li></ul></x-cles>
<x-exo><p>Vous vendez à découvert 50 actions à 120 €. Vous voulez un objectif à 108 € et un stop à 126 €. Quels ordres placez-vous dans l'OCO ? Quels sont le gain et la perte potentiels ?</p>
<x-corr><p>Pour une position courte, on sort en <strong>achetant</strong> : un <strong>achat limité à 108 €</strong> (objectif, sous le prix) et un <strong>stop d'achat à 126 €</strong> (stop loss, au-dessus du prix).</p><div class="calcul">Gain = 50 × (120 − 108) = +600 €
Perte ≈ 50 × (126 − 120) = −300 € (hors slippage)</div></x-corr></x-exo>
"""),

("2-6", "Slippage et gaps : pourquoi un stop n'est pas garanti", r"""
<x-obj><ul><li>Comprendre le slippage et ses causes.</li><li>Mesurer le risque de gap sur une position conservée la nuit ou le week-end.</li></ul></x-obj>
<x-simple>
<p>Le <strong>slippage</strong> (glissement) est la différence entre le prix attendu et le prix réellement obtenu. Il survient quand le marché bouge vite ou manque de liquidité.</p>
<p>Un <strong>gap</strong> est un « trou » sur le graphique : le prix d'ouverture est très différent de la clôture précédente, sans échanges entre les deux. Cela arrive après une nouvelle importante survenue marché fermé (résultats, événement politique, week-end). Un stop placé dans le gap sera exécuté au premier prix disponible, parfois très loin du niveau prévu.</p>
</x-simple>
<x-fig c="Le stop à 47 € ne peut pas être exécuté à 47 € : aucun échange n'a eu lieu entre 51 € et 44 €.">""" + SCHEMA_GAP + r"""</x-fig>
<x-approfondi>
<p>Le slippage peut être <strong>négatif</strong> (le plus fréquent sur les stops, qui sont des ordres au marché déclenchés quand le prix va contre vous) ou <strong>positif</strong>. Il augmente autour des annonces économiques, à l'ouverture, sur les titres peu liquides et avec les gros ordres.</p>
<p>Les gaps sont fréquents sur les actions (résultats publiés hors séance) et existent aussi sur le Forex le lundi matin. Pour s'en protéger : réduire la taille des positions gardées la nuit ou le week-end, éviter de détenir une position au moment des résultats d'une entreprise, utiliser un stop garanti quand il est proposé, ou choisir des produits à risque limité par construction (achat d'options, turbos : module 3).</p>
<p>Protection réglementaire : pour les particuliers en Europe, les CFD doivent bénéficier d'une <strong>protection contre le solde négatif</strong> : la perte ne peut pas dépasser le capital du compte CFD. Elle ne protège pas d'une perte bien supérieure à celle que vous aviez prévue.</p>
</x-approfondi>
<x-exemple>
<p>Vous détenez 200 actions achetées à 50 €, avec un stop à 47 € : risque prévu = 200 × 3 = 600 €. Après des résultats décevants publiés le soir, l'action ouvre à 44 €.</p>
<div class="calcul">Exécution du stop ≈ 44 €
Perte réelle = 200 × (50 − 44) = 1 200 €
Perte prévue : 600 € → la perte réelle est 2 fois plus élevée
Si votre capital est de 30 000 € : risque prévu 2 %, perte réelle 4 %</div>
</x-exemple>
<x-erreurs><ul><li>Considérer que la perte maximale est toujours « entrée − stop ».</li><li>Garder une grosse position pendant la publication des résultats d'une entreprise.</li><li>Placer des stops pile sur des chiffres ronds très visibles, où le slippage peut être plus fort.</li></ul></x-erreurs>
<x-cles><ul><li>Slippage = écart entre prix attendu et prix obtenu.</li><li>Un gap peut faire exécuter un stop bien au-delà de son niveau.</li><li>Gérez le risque de nuit et de week-end : taille réduite, évitement des annonces, stop garanti.</li></ul></x-cles>
<x-exo><p>Vous êtes acheteur d'un CFD sur un indice : 2 contrats à 10 € le point, entrée 7 500, stop 7 460. Le lundi, l'indice ouvre à 7 380. Quelle était la perte prévue, et quelle est la perte réelle ?</p>
<x-corr><div class="calcul">Perte prévue = (7 500 − 7 460) × 10 × 2 = 40 × 20 = 800 €
Perte réelle = (7 500 − 7 380) × 10 × 2 = 120 × 20 = 2 400 €</div><p>La perte réelle est trois fois plus élevée que prévu.</p></x-corr></x-exo>
"""),

("2-7", "Positions longues et courtes (vente à découvert)", r"""
<x-obj><ul><li>Comprendre comment gagner à la baisse.</li><li>Connaître les coûts et risques spécifiques de la vente à découvert.</li></ul></x-obj>
<x-simple>
<p>Être <strong>long</strong> (ou acheteur), c'est acheter en espérant revendre plus cher. Être <strong>court</strong> (short, ou vendeur à découvert), c'est <strong>vendre d'abord</strong> un actif qu'on ne possède pas, en espérant le <strong>racheter moins cher</strong> plus tard. On gagne alors à la baisse.</p>
</x-simple>
<x-approfondi>
<p><strong>Mécanisme sur les actions</strong> : le courtier emprunte les titres pour vous, vous les vendez, puis vous les rachetez pour les rendre. Vous payez des <strong>frais d'emprunt</strong>, vous devez reverser les <strong>dividendes</strong> versés pendant la période, et le prêteur peut rappeler les titres. En France, la vente à découvert se pratique notamment via le SRD (service de règlement différé, sur les valeurs éligibles), les CFD, les futures, ou l'achat d'options de vente et de turbos baissiers.</p>
<p><strong>Asymétrie du risque</strong> : un acheteur perd au maximum 100 % de sa mise (le prix tombe à zéro) et peut gagner sans limite. Un vendeur à découvert gagne au maximum 100 % (si le prix tombe à zéro) et peut perdre <strong>sans limite théorique</strong>, car un prix peut monter indéfiniment.</p>
<p><strong>Short squeeze</strong> : quand beaucoup de vendeurs à découvert doivent racheter en même temps (stops, appels de marge), leurs achats font monter le prix encore plus vite. L'épisode GameStop de janvier 2021 en est un exemple célèbre.</p>
<p>Les autorités peuvent temporairement interdire ou restreindre la vente à découvert en période de crise, et les positions courtes importantes sur actions doivent être déclarées au régulateur au-delà de certains seuils.</p>
</x-approfondi>
<x-fig c="Résultat par action selon le prix final, pour un achat et une vente à découvert à 50 €. La perte du vendeur n'a pas de limite théorique.">""" + SCHEMA_LONGSHORT + r"""</x-fig>
<x-exemple>
<p>Vous vendez à découvert 100 actions à 50 €.</p>
<div class="calcul">Rachat à 44 €  : (50 − 44) × 100 = +600 €
Rachat à 60 €  : (50 − 60) × 100 = −1 000 €
Rachat à 80 €  : (50 − 80) × 100 = −3 000 €
Rachat à 150 € : (50 − 150) × 100 = −10 000 € (soit 2 fois la valeur vendue au départ)
Gain maximal possible (prix à 0) : 50 × 100 = +5 000 €</div>
<p>À cela s'ajoutent les frais d'emprunt et, si un dividende de 1 € est versé pendant la période, 100 × 1 = 100 € à reverser.</p>
</x-exemple>
<x-erreurs><ul><li>Vendre à découvert sans stop « parce que c'est surévalué » : un actif surévalué peut le rester très longtemps, et monter encore.</li><li>Oublier les coûts : emprunt, dividendes, financement.</li><li>Shorter un titre très vendu à découvert, exposé à un short squeeze.</li></ul></x-erreurs>
<x-cles><ul><li>Long : acheter puis vendre. Court : vendre puis racheter.</li><li>Achat : perte maximale = mise. Vente à découvert : perte théoriquement illimitée.</li><li>Coûts propres au short : emprunt de titres, dividendes reversés, financement.</li></ul></x-cles>
<x-exo><p>Vous vendez à découvert 40 actions à 125 €. Un dividende de 2 € par action est versé pendant la détention. Vous rachetez à 110 €. Les frais d'emprunt totaux sont de 15 €. Quel est votre résultat net ?</p>
<x-corr><div class="calcul">Gain brut = (125 − 110) × 40 = 600 €
Dividende reversé = 2 × 40 = 80 €
Frais d'emprunt = 15 €
Résultat net = 600 − 80 − 15 = +505 € (hors commissions)</div></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Bid / ask / spread</h2><ul><li><strong>Bid</strong> : prix auquel vous VENDEZ.</li><li><strong>Ask</strong> : prix auquel vous ACHETEZ.</li><li>Spread = ask − bid : coût à chaque aller-retour.</li><li>Plus large si faible liquidité, forte volatilité, annonces, heures creuses.</li></ul></div>
<div class="encadre"><h2>Carnet d'ordres</h2><ul><li>Ordres limités en attente, à l'achat et à la vente.</li><li>Un ordre au marché consomme le carnet niveau par niveau → prix moyen dégradé.</li><li>Il ne montre jamais toute la liquidité (icebergs, autres plateformes).</li></ul></div>
<div class="encadre"><h2>Types d'ordres</h2>""" + table(["Ordre", "Prix garanti ?", "Exécution garantie ?"],
    [["Au marché", "Non", "Oui (en pratique)"], ["Limité", "Oui (ou mieux)", "Non"], ["Stop", "Non", "Oui une fois déclenché"],
     ["Stop-limite", "Oui (plafond)", "Non"], ["Stop garanti", "Oui", "Oui (prime payée)"]]) + r"""</div>
<div class="encadre"><h2>Où placer les ordres ?</h2><ul><li>Au-dessus du prix : <strong>stop d'achat</strong> ou <strong>limite de vente</strong>.</li><li>En dessous : <strong>limite d'achat</strong> ou <strong>stop de vente</strong>.</li><li>Trailing stop : suit le prix, ne recule jamais.</li><li>OCO : objectif + stop ; l'un annule l'autre.</li></ul></div>
<div class="encadre"><h2>Validité</h2><ul><li>Jour, à révocation (GTC), à date (GTD), IOC, FOK.</li><li>Vérifier les ordres orphelins et les opérations sur titres.</li></ul></div>
<div class="encadre"><h2>Slippage &amp; gaps</h2><ul><li>Un stop n'est PAS un prix garanti.</li><li>Gap : exécution au premier prix disponible.</li><li>Risque de nuit et de week-end, résultats d'entreprise.</li></ul></div>
<div class="encadre"><h2>Long / court</h2><ul><li>Long : gain = (sortie − entrée) × quantité.</li><li>Court : gain = (entrée − sortie) × quantité.</li><li>Court : perte théoriquement illimitée, frais d'emprunt, dividendes reversés, short squeeze.</li></ul></div>
"""

QUIZ = [
("Une action cote bid 20,00 / ask 20,04. À quel prix pouvez-vous l'acheter immédiatement ?",
 ["20,00 €", "20,02 €", "20,04 €", "Au prix de clôture de la veille"], 2, "On achète à l'ask (le meilleur prix proposé par les vendeurs) : 20,04 €."),
("Le spread est :",
 ["Une commission fixe du courtier", "L'écart entre le prix de vente (ask) et le prix d'achat (bid)", "La variation journalière du prix", "Le montant de la marge"], 1, "Spread = ask − bid. C'est un coût implicite payé à chaque aller-retour."),
("Un ordre à cours limité d'achat à 30 € sur une action qui cote 32 € :",
 ["Est exécuté immédiatement à 32 €", "Ne sera exécuté que si le prix descend à 30 € ou moins", "Devient un ordre au marché", "Est refusé"], 1, "Un ordre limité garantit le prix (30 € maximum) mais pas l'exécution."),
("Quel ordre garantit le prix mais PAS l'exécution ?",
 ["Ordre au marché", "Ordre stop", "Ordre à cours limité", "Trailing stop"], 2, "L'ordre limité ne sera jamais exécuté à un prix pire que la limite, mais il peut ne pas être exécuté du tout."),
("Vous êtes acheteur. Où placez-vous votre stop loss ?",
 ["Au-dessus du prix actuel (stop d'achat)", "En dessous du prix actuel (stop de vente)", "Au prix actuel", "On ne peut pas en placer"], 1, "Pour protéger un achat, on place un stop de vente sous le prix actuel."),
("Quel est le principal danger d'un stop-limite utilisé comme stop loss ?",
 ["Il coûte plus cher", "Il peut ne pas être exécuté si le prix chute au-delà de la limite", "Il est exécuté trop tôt", "Il ne se déclenche jamais"], 1, "Une fois déclenché, il devient un ordre limité : si le prix saute sous la limite, la position reste ouverte pendant la chute."),
("Un trailing stop de 3 € sur un achat à 50 € : le prix monte à 58 puis redescend. Où est le stop ?",
 ["47 €", "50 €", "55 €", "58 €"], 2, "Il suit le plus haut (58) à 3 € de distance, soit 55 €, et ne redescend pas."),
("Un ordre OCO :",
 ["Ouvre deux positions à la fois", "Associe deux ordres ; l'exécution de l'un annule l'autre", "Est un ordre exécuté uniquement à la clôture", "Garantit le prix de sortie"], 1, "One Cancels the Other : typiquement un objectif et un stop sur la même position."),
("Vous achetez 1 000 actions au marché. Le carnet affiche 600 à 10,00 € et 800 à 10,02 €. Prix moyen ?",
 ["10,000 €", "10,008 €", "10,010 €", "10,020 €"], 1, "600 × 10,00 + 400 × 10,02 = 6 000 + 4 008 = 10 008 € ; 10 008 ÷ 1 000 = 10,008 €."),
("Stop à 47 €, l'action ouvre à 43 € après une mauvaise nouvelle. Le stop (au marché) est exécuté :",
 ["À 47 € exactement", "Vers 43 € (premier prix disponible)", "Il est annulé", "À 50 €"], 1, "Le stop devient un ordre au marché au déclenchement : il est exécuté au premier prix disponible, ici dans le gap."),
("Vente à découvert de 100 actions à 30 €, rachat à 36 €. Résultat brut ?",
 ["+600 €", "−600 €", "+360 €", "−3 600 €"], 1, "(30 − 36) × 100 = −600 € : le prix a monté contre une position courte."),
("Pourquoi la perte d'une vente à découvert est-elle théoriquement illimitée ?",
 ["Parce que les frais sont illimités", "Parce qu'un prix peut monter sans limite", "Parce que le courtier peut tout saisir", "Elle ne l'est pas"], 1, "Le prix d'un actif ne peut pas descendre sous zéro, mais il n'a pas de plafond à la hausse."),
]
