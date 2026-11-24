from svgkit import plot, table, svg, t, line, arrow

NUM = 0
TITRE = "Avant de commencer"
RESUME = "Trading, investissement ou spéculation ? Les vraies statistiques, le bon état d'esprit et ce que cette formation ne promet pas."
DUREE = "1 h 15"
INTRO = r"""<p>Avant d'apprendre <em>comment</em> trader, il faut savoir <em>ce qu'est</em> le trading, ce qu'il n'est pas, et à quoi s'attendre réellement. Ce module est le plus court techniquement, mais c'est peut-être le plus important : il pose des attentes réalistes, ce qui vous évitera la plupart des erreurs coûteuses des débutants.</p>"""

# --- Schéma 0.1 : coût des frais selon le nombre d'allers-retours
_n = [0, 50, 100, 200, 300, 400, 500]
SCHEMA_FRAIS = plot(
    [{"x": _n, "y": [n * 10 / 10000 * 100 for n in _n], "cls": "g-l2", "label": "Frais annuels en % du capital (10 € par aller-retour, compte de 10 000 €)"}],
    label="Les frais annuels augmentent proportionnellement au nombre de trades",
    xlabel="Nombre d'allers-retours par an", yfmt=lambda v: f"{v:.0f} %", yr=(0, 55),
    marks=[{"x": 200, "y": 20, "t": "200 trades → 20 % du capital", "dx": 8, "dy": 16}])

SCHEMA_STATS = plot(
    [{"x": [1, 2, 3, 4], "y": [74, 89, 89, 97], "kind": "bar", "cls": "g-barre-b", "bw": 70}],
    label="Proportion de particuliers perdants selon plusieurs études",
    xr=(0.4, 4.6), yr=(0, 100), xticks=[1, 2, 3, 4],
    xfmt=lambda v: {1: "ESMA (bas)", 2: "ESMA (haut)", 3: "AMF 2014", 4: "Brésil*"}.get(int(v), ""),
    yfmt=lambda v: f"{v:.0f} %", legend=False,
    texts=[{"x": 1, "y": 77, "t": "74 %", "anchor": "middle"}, {"x": 2, "y": 92, "t": "89 %", "anchor": "middle"},
           {"x": 3, "y": 92, "t": "89 %", "anchor": "middle"}, {"x": 4, "y": 99, "t": "97 %", "anchor": "middle"}])


def _bar_horizons():
    rows = [("Scalping", 0, 0.6, "secondes → minutes"), ("Day trading", 0.6, 1.6, "minutes → heures (clôture le jour même)"),
            ("Swing trading", 1.6, 2.8, "jours → semaines"), ("Position trading", 2.8, 3.9, "semaines → mois"),
            ("Investissement", 3.9, 5.4, "années → décennies")]
    p = []
    W, X0 = 640, 150
    sc = (W - X0 - 20) / 5.4
    for k, (nom, a, b, lib) in enumerate(rows):
        y = 18 + k * 38
        cls = "g-rect-a" if nom != "Investissement" else "g-rect-h"
        p.append(t(X0 - 10, y + 17, nom, "g-txt g-fort", "end"))
        p.append(f'<rect x="{X0 + a*sc:.1f}" y="{y}" width="{(b-a)*sc:.1f}" height="26" rx="5" class="{cls}"/>')
        p.append(t(X0 + a * sc + 6, y + 17, lib, "g-txt g-petit"))
    p.append(arrow(X0, 214, W - 16, 214))
    p.append(t(X0, 232, "Durée de détention plus courte", "g-txt g-petit"))
    p.append(t(W - 16, 232, "plus longue", "g-txt g-petit", "end"))
    return svg(W, 240, "".join(p), "Horizons de détention : du scalping à l'investissement")


SCHEMA_HORIZONS = _bar_horizons()

LECONS = [
("0-1", "Trading, investissement et spéculation", r"""
<x-obj><ul>
<li>Distinguer trading, investissement et spéculation.</li>
<li>Comprendre d'où vient (ou non) le rendement dans chaque approche.</li>
<li>Mesurer le poids des frais quand on multiplie les opérations.</li>
</ul></x-obj>

<x-simple>
<p><strong>Investir</strong>, c'est acheter un actif (une part d'entreprise, un fonds, une obligation…) pour profiter de ce qu'il produit sur la durée : bénéfices de l'entreprise, dividendes, intérêts. On garde le plus souvent l'actif des années.</p>
<p><strong>Trader</strong>, c'est acheter et vendre (ou vendre puis racheter) des actifs sur une durée courte, de quelques secondes à quelques semaines, pour profiter des <em>variations de prix</em>. Le trader ne cherche pas à « posséder » une entreprise : il cherche un écart de prix.</p>
<p><strong>Spéculer</strong>, c'est prendre une position en pariant sur un mouvement de prix futur. Le mot n'est pas une insulte : tout trader spécule. Mais on parle aussi de spéculation pour un investissement sans base solide (acheter « parce que ça monte »).</p>
</x-simple>

<x-fig c="Les approches se distinguent d'abord par l'horizon de détention. La frontière entre elles est floue.">""" + SCHEMA_HORIZONS + r"""</x-fig>

<x-approfondi>
<p><strong>D'où vient le rendement ?</strong> C'est la question clé.</p>
<ul>
<li>L'<strong>investisseur en actions</strong> à long terme profite de la création de richesse des entreprises : bénéfices réinvestis, dividendes. Collectivement, les détenteurs d'actions se partagent cette richesse. C'est un jeu à <em>somme positive</em> (sur le long terme et en moyenne, sans aucune garantie sur une période donnée).</li>
<li>Le <strong>trader à court terme</strong>, lui, ne capte presque rien de cette croissance : sur une journée, elle est négligeable. Son gain vient surtout de la capacité à acheter moins cher ou vendre plus cher que les autres participants. Avant frais, c'est un jeu à <em>somme nulle</em> par rapport au marché : ce que l'un gagne en plus, un autre le perd. Après frais (commissions, spread, financement), cela devient un jeu à <em>somme négative</em>.</li>
<li>Pour les <strong>produits dérivés</strong> (CFD, futures, options), c'est encore plus net : chaque contrat a un acheteur et un vendeur, et les gains de l'un sont exactement les pertes de l'autre, avant frais.</li>
</ul>
<p>Conséquence : pour gagner en trading, il ne suffit pas d'être « bon ». Il faut être <strong>meilleur que la moyenne des autres participants, frais compris</strong>. Parmi eux, il y a des institutions avec des moyens considérables.</p>
</x-approfondi>

<x-exemple>
<p>Deux personnes disposent chacune de 10 000 €.</p>
<ul>
<li><strong>Camille (investisseuse)</strong> achète un fonds indiciel et le garde. Elle paie, disons, 0,2 % de frais par an, soit 10 000 × 0,002 = <strong>20 € par an</strong>.</li>
<li><strong>Hugo (trader)</strong> fait 200 allers-retours par an (environ 4 par semaine). Chaque aller-retour lui coûte 10 € en commissions et en spread. Ses frais annuels sont de 200 × 10 = <strong>2 000 €</strong>.</li>
</ul>
<div class="calcul">Frais d'Hugo en % du capital = 2 000 ÷ 10 000 = 0,20 = 20 % par an
Pour finir l'année à zéro, Hugo doit donc d'abord gagner 20 % brut,
uniquement pour payer ses frais.</div>
<p>Une performance brute de +20 % par an est déjà exceptionnelle. Sur le long terme, les grands indices actions ont historiquement rapporté de l'ordre de 5 à 10 % par an en moyenne, avec de fortes variations. Hugo doit donc être nettement meilleur que la moyenne… uniquement pour ne pas perdre.</p>
</x-exemple>

<x-fig c="Coût annuel des frais selon le nombre d'allers-retours (hypothèse : 10 € par aller-retour, compte de 10 000 €).">""" + SCHEMA_FRAIS + r"""</x-fig>

<x-erreurs><ul>
<li>Croire que le trading est « de l'investissement en plus rapide ». Ce sont deux métiers différents, avec des sources de rendement différentes.</li>
<li>Ignorer les frais, parce qu'ils paraissent petits sur un trade isolé (quelques euros). Multipliés par des centaines de trades, ils deviennent énormes.</li>
<li>Penser que, parce que les marchés montent en moyenne sur le long terme, le trading à court terme est aussi « en moyenne gagnant ».</li>
</ul></x-erreurs>

<x-cles><ul>
<li>Investir, c'est capter la création de richesse dans la durée. Trader, c'est chercher à profiter d'écarts de prix à court terme.</li>
<li>Avant frais, le trading à court terme est un jeu à somme nulle face au marché. Après frais, il est à somme négative.</li>
<li>Les frais sont proportionnels au nombre de trades : plus on trade, plus la barre est haute.</li>
</ul></x-cles>

<x-exo>
<p>Léa dispose de 5 000 €. Elle prévoit 3 allers-retours par jour de bourse, environ 250 jours par an, avec un coût moyen de 4 € par aller-retour. Quel pourcentage de son capital part en frais chaque année ?</p>
<x-corr>
<div class="calcul">Nombre d'allers-retours = 3 × 250 = 750
Frais annuels = 750 × 4 € = 3 000 €
En % du capital = 3 000 ÷ 5 000 = 0,60 = 60 %</div>
<p>Léa doit gagner <strong>60 % brut par an</strong> rien que pour couvrir ses frais. C'est pourquoi les styles très actifs (scalping, day trading) exigent des coûts très bas et un capital suffisant. Le module 8 y revient.</p>
</x-corr>
</x-exo>
"""),

("0-2", "La réalité des statistiques", r"""
<x-obj><ul>
<li>Connaître les principales données publiques sur les résultats des traders particuliers.</li>
<li>Savoir lire correctement ces chiffres, sans les exagérer ni les minimiser.</li>
<li>Comprendre pourquoi les produits à effet de levier sont particulièrement risqués.</li>
</ul></x-obj>

<x-simple>
<p>Les régulateurs ont étudié les comptes de particuliers chez les courtiers. Le constat est constant : <strong>une large majorité de particuliers perd de l'argent</strong>, surtout sur les produits à effet de levier comme les CFD et le Forex. C'est pour cela qu'en Europe, les courtiers en CFD doivent afficher le pourcentage de leurs clients particuliers qui perdent de l'argent.</p>
</x-simple>

<x-approfondi>
<p>Voici quelques données de référence. Elles proviennent de régulateurs ou de recherches universitaires publiées.</p>
<ul>
<li><strong>ESMA (2018)</strong> : en préparant ses mesures d'intervention sur les CFD, l'autorité européenne indiquait qu'entre <strong>74 % et 89 %</strong> des comptes de particuliers perdaient de l'argent sur ces produits, selon les études nationales.</li>
<li><strong>AMF (étude de 2014 sur le Forex)</strong> : sur quatre années étudiées (2009-2012), environ <strong>89 %</strong> des clients particuliers ont perdu de l'argent. La perte moyenne par client était d'environ 11 000 €.</li>
<li><strong>Mentions obligatoires des courtiers en CFD</strong> : chaque courtier européen affiche un pourcentage calculé sur ses propres clients et mis à jour régulièrement. Ces pourcentages se situent le plus souvent <strong>entre 60 % et 85 %</strong> environ, selon les courtiers et les périodes.</li>
<li><strong>Day traders au Brésil</strong> (Chague, De-Losso et Giovannetti, étude publiée à partir de 2019, sur les contrats à terme sur indice) : parmi les particuliers ayant pratiqué le day trading pendant plus de 300 jours, environ <strong>97 %</strong> ont perdu de l'argent. Environ 1 % seulement gagnaient plus que le salaire minimum local.</li>
<li><strong>Day traders à Taïwan</strong> (Barber, Lee, Liu et Odean) : moins de 1 % des day traders étaient capables de gagner de façon régulière et prévisible, une fois les frais déduits.</li>
</ul>
</x-approfondi>

<x-fig c="Part de particuliers perdants dans plusieurs études. *Brésil : uniquement les personnes ayant fait du day trading plus de 300 jours. Les populations, périodes et produits diffèrent : ces barres ne sont pas directement comparables entre elles.">""" + SCHEMA_STATS + r"""</x-fig>

<x-note>
<p>Ces chiffres doivent être lus avec précision :</p>
<ul>
<li>Ils portent sur des <strong>comptes</strong> et sur des <strong>périodes données</strong>. Un compte « gagnant » sur un trimestre peut être perdant sur trois ans.</li>
<li>« X % des comptes gagnent » ne veut pas dire « X % vivent du trading ». Beaucoup de comptes gagnants gagnent de petites sommes, parfois grâce à la chance.</li>
<li>Les chiffres varient selon les produits, les pays et les périodes (un marché haussier calme aide les acheteurs). Mais aucune étude sérieuse ne montre une majorité de particuliers gagnants en trading actif avec effet de levier.</li>
</ul>
</x-note>

<x-exemple>
<p>Un courtier affiche : « 76 % des comptes d'investisseurs particuliers perdent de l'argent lors de la négociation de CFD avec ce fournisseur ». Que signifie ce chiffre pour 1 000 clients ?</p>
<div class="calcul">Comptes perdants = 1 000 × 76 % = 760
Comptes gagnants = 1 000 − 760 = 240</div>
<p>Parmi ces 240 gagnants, supposons (hypothèse purement illustrative) que les trois quarts aient gagné moins de 500 € sur la période :</p>
<div class="calcul">Petits gagnants = 240 × 75 % = 180
Gagnants significatifs = 240 − 180 = 60, soit 60 ÷ 1 000 = 6 % des clients</div>
<p>Et même parmi ces 60, une partie a simplement eu de la chance sur une courte période. Être dans la « bonne » minorité de façon <em>durable</em> est donc bien plus rare que ce que suggère le chiffre de 24 %.</p>
</x-exemple>

<x-erreurs><ul>
<li>Penser « ces statistiques concernent les autres, moi je vais me former ». La quasi-totalité des perdants pensait la même chose, et beaucoup s'étaient formés.</li>
<li>Confondre « compte gagnant sur une période » et « trader rentable dans la durée ».</li>
<li>Croire que ces chiffres sont gonflés par quelques personnes imprudentes. Les pertes sont largement réparties.</li>
</ul></x-erreurs>

<x-cles><ul>
<li>Selon les régulateurs européens, environ 3 particuliers sur 4 au moins perdent de l'argent sur les CFD.</li>
<li>Les études sur les day traders montrent des taux d'échec encore plus élevés chez ceux qui persistent.</li>
<li>Un pourcentage de comptes gagnants sur une période surestime la proportion de traders rentables dans la durée.</li>
</ul></x-cles>

<x-exo>
<p>Un courtier affiche « 68 % des comptes perdent de l'argent ». Un autre affiche « 81 % ». Peut-on en conclure que le premier courtier est « meilleur » et qu'on y gagnera plus facilement ?</p>
<x-corr>
<p><strong>Non.</strong> Le pourcentage dépend surtout de la <strong>clientèle</strong> (expérience, produits tradés, montants), de la <strong>période</strong> (marché calme ou agité) et de la <strong>méthode de calcul</strong>. Un courtier qui attire des clients plus expérimentés, ou qui propose surtout des indices dans un marché haussier, affichera un meilleur chiffre sans que ses conditions soient meilleures pour vous. Votre résultat dépend avant tout de ce que <em>vous</em> faites. Ce chiffre est un avertissement, pas un critère de choix.</p>
</x-corr>
</x-exo>
"""),

("0-3", "Le bon état d'esprit", r"""
<x-obj><ul>
<li>Juger une décision sur sa qualité, pas sur son résultat.</li>
<li>Comprendre la place du hasard à court terme.</li>
<li>Définir un capital que l'on peut se permettre de perdre.</li>
</ul></x-obj>

<x-simple>
<p>En trading, une <strong>bonne décision peut perdre</strong> et une <strong>mauvaise décision peut gagner</strong>. Sur un seul trade, le hasard domine. Ce n'est que sur un grand nombre de trades que la qualité d'une méthode apparaît. Le bon état d'esprit consiste donc à suivre un <strong>processus</strong> (des règles écrites, une gestion du risque stricte) et à évaluer ce processus sur des dizaines ou des centaines de trades, pas sur le dernier.</p>
</x-simple>

<x-approfondi>
<p>Trois idées structurent l'état d'esprit d'un trader sérieux :</p>
<ol>
<li><strong>Penser en probabilités.</strong> Un trade n'est qu'un tirage parmi d'autres. Ce qui compte, c'est l'espérance de gain de la méthode (module 9), pas l'issue d'un trade isolé.</li>
<li><strong>Préserver le capital d'abord.</strong> Tant que vous avez du capital, vous pouvez apprendre. Un trader qui « explose » son compte n'apprend plus rien. Cela passe par des pertes petites et contrôlées.</li>
<li><strong>Accepter une progression lente.</strong> Apprendre prend des mois, souvent des années. Les premières phases devraient se faire sans argent, ou avec très peu (compte démo, puis petites tailles : module 12).</li>
</ol>
<p>Le capital consacré au trading doit être de l'<strong>argent dont la perte n'aurait aucune conséquence</strong> sur votre vie : pas l'épargne de précaution, pas l'argent d'un projet, jamais de l'argent emprunté.</p>
</x-approfondi>

<x-exemple>
<p>Imaginons un jeu à pile ou face truqué en votre faveur : vous gagnez 1 € avec une probabilité de 60 %, vous perdez 1 € avec une probabilité de 40 %. C'est une excellente « stratégie » : en moyenne, chaque partie rapporte 0,60 × 1 − 0,40 × 1 = <strong>+0,20 €</strong>.</p>
<p>Quelle est pourtant la probabilité d'être <strong>en perte</strong> après seulement 10 parties ? Il faut avoir gagné 4 parties ou moins sur 10. La loi binomiale donne :</p>
<div class="calcul">P(4 gains ou moins sur 10) ≈ 16,6 %
P(exactement 5 gains, donc résultat nul) ≈ 20,1 %
Après 100 parties, P(moins de 50 gains, donc en perte) ≈ 1,7 %</div>
<p>Avec une méthode gagnante, on a donc environ <strong>une chance sur six d'être en perte après 10 essais</strong>. Juger sa méthode sur 10 trades n'a pas de sens. Sur 100 trades, le hasard pèse beaucoup moins. Dans la réalité, on ne connaît pas sa vraie probabilité de gain : c'est encore plus difficile.</p>
</x-exemple>

<x-erreurs><ul>
<li>Changer de méthode après 3 pertes consécutives (on abandonne peut-être une méthode valable).</li>
<li>Augmenter la taille après 3 gains consécutifs en se croyant infaillible.</li>
<li>Trader avec de l'argent nécessaire (loyer, épargne de précaution) ou emprunté : la pression émotionnelle fausse toutes les décisions.</li>
<li>Se fixer un objectif de gain mensuel : cela pousse à forcer des trades quand le marché n'offre rien.</li>
</ul></x-erreurs>

<x-cles><ul>
<li>Jugez vos décisions sur le respect de votre processus, pas sur le résultat d'un trade.</li>
<li>Le hasard domine à court terme : il faut un grand nombre de trades pour évaluer une méthode.</li>
<li>Ne tradez qu'un capital dont la perte totale serait sans conséquence pour vous.</li>
</ul></x-cles>

<x-exo>
<p>Un débutant a suivi scrupuleusement son plan sur 8 trades. Il en a perdu 5 et conclut que sa méthode « ne marche pas ». Un autre a ignoré son plan, a doublé sa taille sur un coup de tête et a gagné 600 €. Lequel a pris les meilleures décisions ? Que devrait faire chacun ?</p>
<x-corr>
<p>Le <strong>premier</strong> a pris de meilleures décisions : il a respecté son processus. 8 trades ne suffisent pas pour juger une méthode (l'exemple du pile ou face montre qu'une bonne méthode perd souvent sur 10 essais). Il doit continuer à appliquer et à noter ses trades (journal, module 11), puis évaluer sur un échantillon plus grand.</p>
<p>Le <strong>second</strong> a pris une mauvaise décision qui a payé par chance. C'est dangereux, car le gain renforce le mauvais comportement. Il doit noter ce trade comme une <strong>faute</strong> dans son journal, quel que soit son résultat.</p>
</x-corr>
</x-exo>
"""),

("0-4", "Ce que cette formation n'est pas", r"""
<x-obj><ul>
<li>Savoir ce que vous pouvez (et ne pouvez pas) attendre de cette formation.</li>
<li>Repérer les promesses de rendement irréalistes par le calcul.</li>
</ul></x-obj>

<x-simple>
<p>Cette formation vous apprend à <strong>comprendre</strong> les marchés et à <strong>gérer le risque</strong>. Elle ne vous donne :</p>
<ul>
<li>ni stratégie « clé en main » garantie,</li>
<li>ni promesse de gains,</li>
<li>ni conseil personnalisé (quoi acheter, quand, chez quel courtier),</li>
<li>ni recommandation d'actif ou de cryptomonnaie particulière.</li>
</ul>
<p>Personne ne peut honnêtement vous promettre un rendement en trading. Ceux qui le font sont soit dans l'erreur, soit en train de vous vendre quelque chose (formation, signaux, robot, compte géré…).</p>
</x-simple>

<x-approfondi>
<p>Un bon moyen de repérer une promesse irréaliste est de la <strong>composer dans le temps</strong>. Les intérêts composés rendent les petits pourcentages réguliers vertigineux. Si une méthode rapportait vraiment « 1 % par jour », son auteur deviendrait en quelques années l'une des personnes les plus riches du monde. Il n'aurait aucun intérêt à vendre une formation à 497 €.</p>
<p>À titre de comparaison, très peu de fonds professionnels font durablement mieux que leur indice de référence une fois leurs frais déduits. Les études de suivi (comme les rapports SPIVA de S&amp;P) le montrent année après année sur de longues périodes.</p>
</x-approfondi>

<x-exemple>
<p>Promesse : « +1 % par jour avec ma méthode ». Il y a environ 250 jours de bourse par an. Calculons ce que deviendraient 10 000 € :</p>
<div class="calcul">Après 1 an  : 10 000 × 1,01^250 ≈ 10 000 × 12,03   ≈ 120 300 €
Après 2 ans : 10 000 × 1,01^500 ≈ 10 000 × 144,8   ≈ 1 447 700 €
Après 3 ans : 10 000 × 1,01^750 ≈ 10 000 × 1 741,9 ≈ 17 419 000 €</div>
<p>En trois ans, 10 000 € deviendraient plus de 17 millions. Ce rendement est irréaliste : aucun investisseur au monde ne l'obtient durablement. La promesse est donc mensongère, quelles que soient les « preuves » montrées (captures d'écran faciles à truquer, comptes démo, sélection des bonnes périodes).</p>
</x-exemple>

<x-erreurs><ul>
<li>Croire qu'une capture d'écran de gains prouve quelque chose. Elle peut être truquée, venir d'un compte démo, ou montrer un seul bon mois parmi de nombreux mauvais.</li>
<li>Chercher « la » stratégie gagnante avant d'avoir appris à gérer le risque.</li>
<li>Payer pour des « signaux » ou des formations promettant un revenu (module 12 sur les arnaques).</li>
</ul></x-erreurs>

<x-cles><ul>
<li>Aucune méthode honnête ne promet un rendement en trading.</li>
<li>Composez toute promesse de rendement sur plusieurs années pour tester sa vraisemblance.</li>
<li>Cette formation donne des compétences et de la lucidité, pas une garantie de résultat.</li>
</ul></x-cles>

<x-exo>
<p>Un « mentor » sur les réseaux sociaux promet « 10 % par mois, régulier ». Que deviendraient 2 000 € en 5 ans si c'était vrai ? Conclusion ?</p>
<x-corr>
<div class="calcul">5 ans = 60 mois
2 000 × 1,10^60 ≈ 2 000 × 304,5 ≈ 609 000 €</div>
<p>2 000 € deviendraient environ 609 000 € en 5 ans, soit un rendement annuel composé de 1,10^12 − 1 ≈ <strong>+214 % par an</strong>. C'est sans commune mesure avec ce qu'obtiennent les meilleurs gérants professionnels sur longue période. La promesse n'est pas crédible. Un « mentor » qui obtiendrait vraiment cela n'aurait pas besoin de vendre quoi que ce soit.</p>
</x-corr>
</x-exo>
"""),

("0-5", "Comment suivre cette formation", r"""
<x-obj><ul>
<li>Organiser son apprentissage dans le temps.</li>
<li>Utiliser efficacement les leçons, quiz, fiches, outils et le glossaire.</li>
</ul></x-obj>

<x-simple>
<p>La formation suit une progression logique : comprendre le terrain (modules 1 à 3), apprendre à lire les marchés (4 à 7), choisir un style (8), maîtriser le risque (9), construire et tester une stratégie (10), se maîtriser soi-même (11), puis passer à la pratique en sécurité (12) en respectant le cadre légal et fiscal (13).</p>
<p>Pour chaque leçon : lisez, refaites les calculs des exemples vous-même, faites l'exercice <strong>avant</strong> d'ouvrir la correction, puis passez le quiz du module.</p>
</x-simple>

<x-approfondi>
<p>Quelques principes d'apprentissage efficaces :</p>
<ul>
<li><strong>Espacer</strong> : 3 séances d'une heure valent mieux qu'une séance de 3 heures.</li>
<li><strong>Se tester</strong> : les quiz et les exercices fixent la mémoire bien mieux que la relecture (c'est l'« effet de test » bien documenté en psychologie cognitive).</li>
<li><strong>Appliquer</strong> : dès le module 4, ouvrez des graphiques (plateforme de démonstration ou site de graphiques gratuit) et cherchez les notions vues.</li>
<li><strong>Revenir aux fiches</strong> : imprimez-les et relisez-les avant chaque module suivant.</li>
</ul>
</x-approfondi>

<x-exemple>
<p>La formation demande environ 30 heures, exercices compris. Vous disposez de 4 heures par semaine.</p>
<div class="calcul">Durée = 30 h ÷ 4 h par semaine = 7,5 semaines, soit environ 2 mois</div>
<p>À cela s'ajoute la pratique en compte démo, recommandée sur <strong>au moins 2 à 3 mois</strong> (module 12). Comptez donc <strong>4 à 6 mois minimum</strong> avant d'envisager de petites positions réelles. C'est normal, et c'est même une protection.</p>
</x-exemple>

<x-erreurs><ul>
<li>Sauter directement aux indicateurs techniques (module 6) en négligeant le risque (module 9).</li>
<li>Lire sans refaire les calculs : on croit comprendre, puis on se trompe sur la taille de position en situation réelle.</li>
<li>Ouvrir un compte réel « pour apprendre plus vite » avant la fin de la formation.</li>
</ul></x-erreurs>

<x-cles><ul>
<li>Suivez l'ordre des modules, faites les exercices avant de lire les corrections.</li>
<li>Prévoyez plusieurs mois entre le début de la formation et le premier euro réellement engagé.</li>
</ul></x-cles>

<x-exo>
<p>Établissez votre propre calendrier : combien d'heures par semaine pouvez-vous consacrer à la formation ? À quelle date prévoyez-vous de finir le module 9 (environ 60 % de la formation) ?</p>
<x-corr>
<p>Exemple de réponse : « 3 h par semaine. 60 % de 30 h = 18 h, soit 18 ÷ 3 = 6 semaines. Si je commence le 1<sup>er</sup> du mois, je termine le module 9 vers la mi-mois suivant. » Il n'y a pas de bonne réponse unique. L'important est d'avoir un rythme régulier et réaliste, et de l'écrire.</p>
</x-corr>
</x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Trading ≠ investissement</h2><ul>
<li><strong>Investir</strong> : détenir longtemps, capter la création de richesse (bénéfices, dividendes, intérêts).</li>
<li><strong>Trader</strong> : profiter de variations de prix à court terme.</li>
<li><strong>Spéculer</strong> : parier sur un mouvement futur de prix.</li>
<li>Trading court terme : somme nulle avant frais, <strong>somme négative après frais</strong>.</li></ul></div>
<div class="encadre"><h2>Les frais</h2><ul>
<li>Frais annuels = nombre d'allers-retours × coût moyen.</li>
<li>200 trades × 10 € sur 10 000 € = 20 % du capital par an.</li></ul></div>
<div class="encadre"><h2>Les chiffres</h2><ul>
<li>ESMA : 74 à 89 % des comptes de particuliers perdants sur les CFD.</li>
<li>AMF (Forex, 2009-2012) : environ 89 % de perdants.</li>
<li>Day traders persistants (Brésil) : environ 97 % de perdants.</li>
<li>« Compte gagnant sur une période » ≠ « trader rentable durablement ».</li></ul></div>
<div class="encadre"><h2>L'état d'esprit</h2><ul>
<li>Juger le <strong>processus</strong>, pas le résultat d'un trade.</li>
<li>Le hasard domine à court terme : une bonne méthode peut perdre sur 10 trades.</li>
<li>Capital de trading = argent dont la perte n'a aucune conséquence. Jamais d'argent emprunté.</li></ul></div>
<div class="encadre"><h2>Repérer une promesse irréaliste</h2><ul>
<li>Composer : 1 % par jour ≈ ×12 par an, ×1 700 en 3 ans.</li>
<li>Captures de gains = aucune preuve.</li>
<li>Personne ne peut promettre un rendement en trading.</li></ul></div>
<div class="encadre"><h2>Méthode d'apprentissage</h2><ul>
<li>Modules dans l'ordre, exercices avant corrections, quiz.</li>
<li>4 à 6 mois minimum avant tout argent réel (formation + démo).</li></ul></div>
"""

QUIZ = [
("Quelle est la principale source de rendement d'un investisseur en actions à long terme ?",
 ["Les écarts de prix intraday", "La création de richesse des entreprises (bénéfices, dividendes)", "Le levier offert par le courtier", "Les erreurs des autres investisseurs"], 1,
 "Sur le long terme, l'investisseur capte la croissance des bénéfices et les dividendes. Le trader à court terme, lui, cherche des écarts de prix."),
("Avant frais, le trading à court terme est, par rapport au marché :",
 ["Un jeu à somme positive", "Un jeu à somme nulle", "Un jeu à somme négative", "Toujours gagnant pour les particuliers"], 1,
 "Avant frais, ce qu'un participant gagne de plus que le marché, un autre le perd : c'est un jeu à somme nulle. Les frais le rendent ensuite à somme négative."),
("Un trader fait 300 allers-retours par an à 8 € l'unité sur un compte de 6 000 €. Ses frais représentent :",
 ["4 % du capital", "24 % du capital", "40 % du capital", "48 % du capital"], 2,
 "300 × 8 = 2 400 € ; 2 400 ÷ 6 000 = 0,40 = 40 % du capital par an."),
("Selon l'ESMA (2018), quelle proportion de comptes de particuliers perdait de l'argent sur les CFD ?",
 ["Entre 10 et 25 %", "Environ 50 %", "Entre 74 et 89 %", "Moins de 5 %"], 2,
 "L'ESMA citait une fourchette de 74 à 89 % de comptes perdants, selon les études nationales."),
("« 70 % des comptes perdent de l'argent » signifie que :",
 ["30 % des clients vivent du trading", "30 % des comptes étaient gagnants sur la période mesurée, souvent de peu", "Le courtier est fiable", "Il suffit de se former pour faire partie des 30 %"], 1,
 "Le chiffre porte sur des comptes et sur une période. Un compte gagnant peut l'être de quelques euros, ou par chance. Cela ne dit rien d'une rentabilité durable."),
("Avec un jeu gagnant à 60 % (+1/−1), la probabilité d'être en perte après 10 parties est d'environ :",
 ["0 %", "1,7 %", "16,6 %", "40 %"], 2,
 "Il faut 4 gains ou moins sur 10 : selon la loi binomiale, environ 16,6 %. Sur 100 parties, cette probabilité tombe à environ 1,7 %. Le hasard domine à court terme."),
("Quelle attitude est la plus saine après une perte sur un trade qui respectait parfaitement le plan ?",
 ["Changer de méthode immédiatement", "Doubler la taille pour se refaire", "Noter le trade et continuer à appliquer le plan", "Arrêter définitivement le trading"], 2,
 "Une perte fait partie du jeu. Si le plan a été respecté, c'est une bonne décision. On l'évalue sur un grand échantillon de trades."),
("Quel argent est acceptable pour trader ?",
 ["L'épargne de précaution", "Un crédit à la consommation", "Un capital dont la perte n'aurait aucune conséquence sur sa vie", "L'argent prévu pour un apport immobilier"], 2,
 "Seul un capital que l'on peut perdre intégralement sans conséquence est acceptable. L'argent emprunté ou nécessaire crée une pression qui fausse les décisions."),
("Une promesse de « +1 % par jour » transformerait 10 000 € en environ combien après un an (250 jours) ?",
 ["12 500 €", "35 000 €", "120 000 €", "2,5 millions €"], 2,
 "10 000 × 1,01^250 ≈ 10 000 × 12,03 ≈ 120 300 €. Ce rendement est irréaliste : la promesse n'est pas crédible."),
("Qu'est-ce que cette formation NE fournit PAS ?",
 ["Des explications sur la gestion du risque", "Des exercices corrigés", "Des recommandations personnalisées d'achat ou de vente", "Un glossaire"], 2,
 "La formation est pédagogique. Elle ne donne aucun conseil d'investissement personnalisé et ne recommande aucun actif ni aucun courtier."),
("Pourquoi les produits dérivés (CFD, futures) sont-ils qualifiés de jeu à somme nulle avant frais ?",
 ["Parce qu'ils ne bougent jamais", "Parce que le gain de l'acheteur est exactement la perte du vendeur", "Parce qu'ils sont garantis par l'État", "Parce qu'ils versent des dividendes"], 1,
 "Chaque contrat oppose un acheteur et un vendeur : ce que l'un gagne, l'autre le perd, avant frais."),
]
