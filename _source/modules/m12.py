from svgkit import plot, table, svg, t, line, arrow

NUM = 12
TITRE = "Passer à la pratique en sécurité"
RESUME = "Choisir un courtier régulé, vérifier les listes noires de l'AMF, utiliser un compte démo, connaître les plateformes, déjouer les arnaques, suivre un plan sur plusieurs mois."
DUREE = "2 h"
INTRO = r"""<p>Ce module fait le lien entre la théorie et la pratique. Il ne recommande <strong>aucun courtier ni aucune plateforme</strong> : il vous donne des critères objectifs et des réflexes de vérification. Il insiste sur un danger bien réel : les escroqueries financières, qui visent précisément les personnes qui s'intéressent au trading.</p>"""


def _plan():
    W = 680
    ph = [("Formation", "mois 0 à 2", "modules, exercices, quiz"), ("Démo", "mois 2 à 5", "≥ 60 trades, journal"),
          ("Réel micro", "mois 5 à 8", "risque 0,25 à 0,5 %"), ("Montée progressive", "mois 8 à 12+", "si critères atteints")]
    p = []
    for k, (a, b, c) in enumerate(ph):
        x = 8 + k * 168
        p.append(f'<rect x="{x}" y="20" width="156" height="78" rx="10" class="{["g-rect-a", "g-rect", "g-rect-h", "g-rect-h"][k]}"/>')
        p.append(t(x + 78, 44, a, "g-txt g-fort", "middle"))
        p.append(t(x + 78, 64, b, "g-txt", "middle"))
        p.append(t(x + 78, 84, c, "g-txt g-petit", "middle"))
        if k < 3:
            p.append(arrow(x + 156, 59, x + 168, 59))
    p.append(t(W / 2, 122, "Chaque passage exige des critères écrits. Si un critère n'est pas atteint : on reste (ou on revient) à l'étape précédente.", "g-txt g-petit", "middle"))
    return svg(W, 132, "".join(p), "Plan de progression sur environ 12 mois")


SCHEMA_PLAN = _plan()

_m = list(range(0, 13))
SCHEMA_PONZI = plot([{"x": _m, "y": [50 * m for m in _m], "cls": "g-lb", "label": "Rendements promis versés (cumul, k€)"},
                     {"x": _m, "y": [0] * 13, "cls": "g-lh", "label": "Gains réels de trading (aucun)"}],
                    label="Pyramide de Ponzi : les « rendements » ne peuvent venir que des nouveaux dépôts", xlabel="Mois",
                    yr=(-30, 650), xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f} k€",
                    marks=[{"x": 12, "y": 600, "t": "600 k€ à trouver auprès de nouveaux clients", "anchor": "end", "dx": -6}])

LECONS = [
("12-1", "Choisir un courtier", r"""
<x-obj><ul><li>Vérifier qu'un intermédiaire est autorisé à exercer en France.</li><li>Comparer des courtiers sur des critères objectifs, frais compris.</li></ul></x-obj>
<x-simple>
<p>Avant de comparer les frais ou les plateformes, une seule question compte d'abord : <strong>cet intermédiaire est-il autorisé à me proposer ces services en France ?</strong></p>
<ol><li>Chercher son nom (et son numéro d'agrément) sur le registre <strong>REGAFI</strong> (établissements autorisés par l'ACPR, y compris les entreprises européennes intervenant en France via le « passeport européen »).</li>
<li>Vérifier les <strong>listes noires</strong> et les mises en garde publiées par l'<strong>AMF</strong> (sites non autorisés pour le Forex, les CFD, les cryptoactifs, le « divers biens »).</li>
<li>Pour les cryptoactifs : vérifier l'agrément du prestataire sur le site de l'AMF.</li>
<li>Pour un conseiller : vérifier son immatriculation sur le registre de l'<strong>ORIAS</strong>.</li></ol>
</x-simple>
<x-approfondi>
<p><strong>Attention aux « sociétés clones »</strong> : des escrocs utilisent le nom, le logo, voire le numéro d'agrément d'une société réellement autorisée. Vérifiez l'adresse du site web et les coordonnées sur le registre officiel, et contactez la société par les coordonnées du registre, pas par celles fournies par votre interlocuteur.</p>
<p><strong>Critères de comparaison</strong> (après la vérification réglementaire) :</p>
<ul><li><strong>Protection des avoirs</strong> : ségrégation des fonds des clients, mécanisme de garantie des titres et des espèces du pays d'agrément (en France, le FGDR ; les plafonds sont fixés par la réglementation : à vérifier sur son site).</li>
<li><strong>Frais complets</strong> : commissions, spreads, financement, change, garde, inactivité, retrait (module 3).</li>
<li><strong>Produits et marchés</strong> disponibles, tailles minimales (micro-lots, fractions).</li>
<li><strong>Qualité d'exécution</strong>, plateforme, stabilité, service client en français.</li>
<li><strong>Fiscalité</strong> : un courtier établi en France fournit en principe un imprimé fiscal unique (IFU) récapitulatif ; avec un courtier étranger, c'est à vous de calculer et de déclarer (module 13), y compris le compte lui-même.</li></ul>
<p>Le choix final vous appartient : cette formation ne recommande aucun courtier.</p>
</x-approfondi>
<x-exemple>
<p>Vous prévoyez 15 allers-retours par mois sur des actions européennes, 3 000 € par ordre. Deux courtiers fictifs :</p>
""" + table(["", "Courtier A", "Courtier B"],
            [["Commission", "0,10 % (minimum 2 €)", "6 € fixes par ordre"], ["Frais de garde", "0", "2 € par mois"], ["Frais d'inactivité", "10 € par trimestre sans ordre", "0"]]) + r"""
<div class="calcul">Ordres par an = 15 × 2 × 12 = 360
A : commission = max(0,10 % × 3 000 ; 2) = 3 € → 360 × 3 = 1 080 € par an
B : 360 × 6 = 2 160 € + 12 × 2 = 24 € → 2 184 € par an
Avec des ordres de 10 000 € : A = 360 × 10 = 3 600 € ; B = 2 184 € → B devient moins cher
Seuil : 0,10 % × montant = 6 € → montant = 6 000 € par ordre (hors frais de garde)</div>
<p>Le « moins cher » dépend de votre façon de trader. Faites le calcul avec vos propres chiffres.</p>
</x-exemple>
<x-erreurs><ul><li>Ouvrir un compte après un appel ou une publicité, sans vérifier le registre.</li><li>Choisir sur la seule base du bonus d'ouverture ou du levier maximal.</li><li>Se fier à un site qui « ressemble » à celui d'une société connue.</li></ul></x-erreurs>
<x-cles><ul><li>Vérifier d'abord : REGAFI, listes noires de l'AMF, agrément crypto, ORIAS.</li><li>Méfiance envers les sociétés clones.</li><li>Comparer ensuite protection, frais complets, produits, exécution, fiscalité.</li></ul></x-cles>
<x-exo><p>Un « conseiller » vous appelle de la part d'une société au nom connu et vous envoie un lien d'ouverture de compte. Listez les vérifications à faire avant toute action.</p>
<x-corr><ol><li>Raccrocher et ne rien communiquer (pièces d'identité, coordonnées bancaires).</li><li>Chercher la société sur REGAFI et vérifier le nom exact, l'adresse et le site officiel.</li><li>Consulter les listes noires et mises en garde de l'AMF.</li><li>Contacter la société par les coordonnées <em>officielles</em> pour savoir si ce conseiller existe.</li><li>En cas de doute, contacter l'AMF (service AMF Épargne Info Service).</li></ol><p>Un démarchage téléphonique non sollicité pour des produits à risque est en soi un signal d'alerte.</p></x-corr></x-exo>
"""),

("12-2", "Le compte démo", r"""
<x-obj><ul><li>Utiliser un compte démo de façon réaliste.</li><li>Connaître ses limites.</li></ul></x-obj>
<x-simple>
<p>Un <strong>compte démo</strong> (de démonstration) permet de trader avec de l'argent fictif, dans des conditions proches du réel. Il sert à apprendre la plateforme, tester les types d'ordres, appliquer sa stratégie (forward test, module 10) et tenir son journal, sans risque financier.</p>
</x-simple>
<x-approfondi>
<p><strong>Pour qu'il soit utile</strong> : régler le capital fictif au niveau du capital réel prévu (pas 100 000 € si vous comptez démarrer avec 3 000 €), appliquer exactement les mêmes règles de risque, tenir le journal comme en réel, et fixer une durée et un nombre minimal de trades.</p>
<p><strong>Limites</strong> : l'exécution est souvent meilleure qu'en réel (peu ou pas de slippage), certains coûts peuvent être absents, et surtout <strong>l'absence d'argent réel supprime une grande partie de la pression émotionnelle</strong>. Des résultats en démo sont une condition nécessaire, pas suffisante. Méfiez-vous des « concours de trading en démo » qui servent à attirer vers des comptes réels.</p>
</x-approfondi>
<x-exemple>
<p>En démo, un débutant laisse le capital par défaut de 100 000 € et risque 1 000 € par trade « pour voir ». Il prévoit ensuite d'ouvrir un compte réel de 5 000 €.</p>
<div class="calcul">Risque en démo = 1 000 € = 1 % de 100 000 €… mais 20 % de 5 000 €
Pour un apprentissage réaliste : capital démo = 5 000 €, risque 1 % = 50 €
Les tailles de position seront 20 fois plus petites : il faut vérifier que l'instrument
le permet (micro-lots, CFD de petite taille, actions à l'unité).</div>
</x-exemple>
<x-erreurs><ul><li>Garder un capital fictif sans rapport avec le capital réel.</li><li>Traiter la démo comme un jeu (tailles énormes, pas de journal).</li><li>Passer en réel après une semaine de bons résultats en démo.</li></ul></x-erreurs>
<x-cles><ul><li>Démo = apprentissage de la plateforme, des ordres et de la stratégie.</li><li>Capital et règles identiques au réel prévu.</li><li>Exécution idéalisée et émotions absentes : résultats nécessaires, pas suffisants.</li></ul></x-cles>
<x-exo><p>Votre démo affiche 70 trades, 41 % de réussite, gain moyen 2,0R, perte moyenne 1,0R, et 94 % de trades conformes au plan. Calculez l'espérance. Ces résultats suffisent-ils pour passer en réel ?</p>
<x-corr><div class="calcul">Espérance = 0,41 × 2,0 − 0,59 × 1,0 = 0,82 − 0,59 = +0,23 R</div><p>C'est encourageant (espérance positive, bonne discipline), mais 70 trades restent un petit échantillon (module 10). Un passage en <strong>réel à très petite taille</strong> (0,25 à 0,5 % de risque) est raisonnable, en continuant à comparer les statistiques.</p></x-corr></x-exo>
"""),

("12-3", "Plateformes et outils", r"""
<x-obj><ul><li>Connaître les grandes familles de plateformes et d'outils.</li><li>Évaluer le coût des abonnements par rapport au capital.</li></ul></x-obj>
<x-simple>
<p>Présentation neutre des principaux types d'outils (sans recommandation) :</p>
<ul><li><strong>Plateformes de graphiques</strong> comme TradingView : graphiques web, indicateurs, alertes, partage d'analyses ; versions gratuites et payantes. Certaines sont connectables à des courtiers.</li>
<li><strong>Plateformes de trading multi-courtiers</strong> comme MetaTrader 4/5 (très répandue sur le Forex et les CFD, permet l'automatisation via des robots), cTrader, NinjaTrader (orientée futures), et d'autres.</li>
<li><strong>Plateformes propres aux courtiers</strong> (web et mobile).</li>
<li><strong>Outils complémentaires</strong> : calendrier économique, filtres d'actions (screeners), tableur pour le journal et les backtests, langages de programmation pour les tests automatisés.</li></ul>
</x-simple>
<x-approfondi>
<p>Critères de choix : marchés couverts, qualité des données, fiabilité, ordres disponibles (OCO, trailing stop géré côté serveur ou non), possibilités de backtest, coût. Attention aux <strong>robots de trading</strong> (« expert advisors ») vendus en ligne avec des performances spectaculaires : ils sont très souvent suroptimisés (module 10), et certains sont des arnaques.</p>
</x-approfondi>
<x-exemple>
<p>Abonnements envisagés : données en temps réel 15 €/mois, plateforme de graphiques premium 25 €/mois, robot « de signaux » 49 €/mois. Capital : 4 000 €.</p>
<div class="calcul">Total mensuel = 15 + 25 + 49 = 89 €
Total annuel = 89 × 12 = 1 068 €
En % du capital = 1 068 ÷ 4 000 ≈ 26,7 % : à gagner avant même d'être à l'équilibre
Sans le robot : (15 + 25) × 12 = 480 € → 12 % du capital, encore très lourd</div>
<p>Pour un petit compte, les versions gratuites suffisent largement à apprendre.</p>
</x-exemple>
<x-erreurs><ul><li>Accumuler les abonnements « pour être sérieux ».</li><li>Acheter un robot sur la foi de résultats affichés.</li><li>Changer de plateforme sans cesse au lieu de maîtriser un outil.</li></ul></x-erreurs>
<x-cles><ul><li>Graphiques, plateformes multi-courtiers, plateformes des courtiers, outils complémentaires.</li><li>Les frais fixes pèsent lourd sur un petit compte.</li><li>Méfiance envers les robots et « systèmes » vendus en ligne.</li></ul></x-cles>
<x-exo><p>Votre budget d'outils est de 20 € par mois. À partir de quel capital ce coût représente-t-il moins de 2 % par an ?</p>
<x-corr><div class="calcul">Coût annuel = 20 × 12 = 240 €
240 ÷ capital ≤ 2 % → capital ≥ 240 ÷ 0,02 = 12 000 €</div></x-corr></x-exo>
"""),

("12-4", "Les arnaques courantes", r"""
<x-obj><ul><li>Reconnaître les principales escroqueries liées au trading.</li><li>Connaître les signaux d'alerte et les bons réflexes.</li></ul></x-obj>
<x-simple>
<p>Les escroqueries financières en ligne sont nombreuses et sophistiquées. L'AMF publie régulièrement des mises en garde et des listes noires de sites non autorisés. Principales formes :</p>
<ul><li><strong>Faux courtiers</strong> (Forex, CFD, cryptos) : la plateforme affiche des gains fictifs ; impossible de retirer son argent ; on vous demande de payer des « frais » ou des « taxes » pour débloquer les fonds.</li>
<li><strong>Sociétés clones</strong> : usurpation de l'identité d'un établissement réellement autorisé.</li>
<li><strong>Signaux payants et « gourous »</strong> : abonnements à des signaux, groupes privés, formations promettant un revenu ; captures d'écran de gains invérifiables, train de vie mis en scène. Beaucoup gagnent surtout grâce aux abonnements et aux commissions d'affiliation des courtiers.</li>
<li><strong>Pyramides de Ponzi</strong> : rendements réguliers promis, payés avec l'argent des nouveaux entrants.</li>
<li><strong>Arnaques sentimentales ou « amicales »</strong> : une personne rencontrée en ligne vous initie à une plateforme « miracle ».</li>
<li><strong>Arnaques au recouvrement</strong> : après une première escroquerie, de faux avocats ou de faux régulateurs promettent de récupérer vos fonds… contre paiement.</li></ul>
</x-simple>
<x-approfondi>
<p><strong>Signaux d'alerte</strong> : rendement élevé « garanti » ou « sans risque » ; pression pour décider vite ; démarchage non sollicité (téléphone, réseaux sociaux, messagerie) ; demande d'installer un logiciel de prise de contrôle à distance ; paiement en cryptoactifs ou vers un compte à l'étranger ; société absente des registres officiels ; impossibilité de retirer ; demande de payer pour retirer.</p>
<p><strong>Réflexes</strong> : vérifier les registres (REGAFI, ORIAS, liste des prestataires crypto autorisés) et les listes noires de l'AMF ; ne jamais transmettre ses codes ni installer de logiciel de contrôle à distance ; ne jamais payer pour « débloquer » des fonds. En cas de problème : cesser tout versement, conserver toutes les preuves, contacter sa banque, porter plainte, signaler sur les plateformes officielles (par exemple PHAROS pour les contenus illicites en ligne), et contacter AMF Épargne Info Service.</p>
</x-approfondi>
<x-exemple>
<p><strong>Pourquoi une pyramide finit toujours par s'effondrer.</strong> Une plateforme collecte 1 000 000 € et promet 5 % par mois, sans aucun gain réel.</p>
<div class="calcul">« Rendement » à verser chaque mois = 1 000 000 × 5 % = 50 000 €
Sur 12 mois = 600 000 €, qui ne peuvent venir que de nouveaux dépôts
Pour verser 5 % par mois sur un capital qui grandit, la collecte doit croître sans fin ;
dès que les dépôts ralentissent ou que des retraits massifs arrivent, tout s'effondre.</div>
<p>Rappel du module 0 : 5 % par mois composé = 1,05<sup>12</sup> − 1 ≈ 79,6 % par an. Aucun placement légitime ne promet cela.</p>
</x-exemple>
<x-fig c="Sans gains réels, les rendements promis ne peuvent être payés que par l'argent des nouveaux clients.">""" + SCHEMA_PONZI + r"""</x-fig>
<x-erreurs><ul><li>Penser « ça n'arrive qu'aux autres » : les victimes ont tous les profils, y compris diplômés et prudents.</li><li>Verser plus d'argent pour « débloquer » un retrait.</li><li>Faire confiance à un site qui affiche des gains en temps réel (les chiffres peuvent être entièrement fictifs).</li><li>Payer un « service de récupération » après une arnaque.</li></ul></x-erreurs>
<x-cles><ul><li>Rendement élevé garanti, urgence, démarchage, paiement en crypto = alertes rouges.</li><li>Toujours vérifier REGAFI, ORIAS, agréments crypto et listes noires de l'AMF.</li><li>Ne jamais payer pour retirer ou « récupérer » des fonds.</li></ul></x-cles>
<x-exo><p>Sur un réseau social, un compte affiche des captures de gains de « +3 400 € cette semaine » et propose un groupe privé à 79 € par mois pour copier ses trades. Quels sont les signaux d'alerte ? Comment pourriez-vous vérifier ses affirmations ?</p>
<x-corr><p>Signaux d'alerte : captures invérifiables (faciles à truquer, compte démo, sélection des bons jours), modèle économique fondé sur l'abonnement (il gagne même si vous perdez), probable affiliation à un courtier, absence de statistiques complètes et auditées, pression sociale. Vérification : demander un historique complet et vérifiable sur plusieurs années (rarement fourni), vérifier son statut réglementaire (un conseil en investissement personnalisé exige un statut, consultable sur l'ORIAS), consulter les mises en garde de l'AMF. Les autorités ont par ailleurs encadré la promotion de produits financiers par les influenceurs.</p></x-corr></x-exo>
"""),

("12-5", "Un plan de progression sur plusieurs mois", r"""
<x-obj><ul><li>Construire un plan de progression par étapes avec des critères de passage.</li><li>Fixer des critères objectifs pour avancer ou revenir en arrière.</li></ul></x-obj>
<x-simple>
<p>Progresser en trading, ce n'est pas « gagner plus vite » : c'est franchir des étapes, chacune validée par des <strong>critères mesurables</strong> plutôt que par des dates ou des montants de gains.</p>
</x-simple>
<x-fig c="Un exemple de plan sur environ un an. Les durées sont indicatives : seuls les critères comptent.">""" + SCHEMA_PLAN + r"""</x-fig>
<x-approfondi>
""" + table(["Étape", "Objectifs", "Critères pour passer à l'étape suivante (exemples)"],
            [["1. Formation", "Modules 0 à 13, exercices, quiz", "Tous les quiz ≥ 80 %, examen final ≥ 80 %, plan de trading écrit"],
             ["2. Démo", "Appliquer le plan, tenir le journal", "≥ 60 trades ; ≥ 90 % conformes au plan ; espérance > 0 après frais ; drawdown max dans les limites prévues"],
             ["3. Réel micro", "Vivre les émotions avec un risque minime (0,25 à 0,5 %)", "≥ 50 trades ; statistiques proches de la démo ; limites jamais enfreintes"],
             ["4. Montée progressive", "Augmenter le risque par paliers (ex. +0,25 point par trimestre, jusqu'à 1 %)", "Maintien des critères ; retour au palier inférieur si drawdown > seuil"]]) + r"""
<p>À chaque étape, il est normal de rester plus longtemps que prévu, ou de revenir en arrière. Il est aussi parfaitement légitime de conclure, au vu de ses résultats, que le trading actif n'est pas pour soi, et de se tourner vers un investissement passif à long terme.</p>
</x-approfondi>
<x-exemple>
<p>Bilan de fin de démo : 72 trades, dont 66 conformes au plan ; résultat net +9,4R ; drawdown maximal 6,2R ; limite prévue de drawdown : 8R.</p>
<div class="calcul">Conformité = 66 ÷ 72 ≈ 91,7 % (critère ≥ 90 % : ✔)
Espérance = 9,4 ÷ 72 ≈ +0,13 R par trade (critère > 0 : ✔)
Drawdown max 6,2R &lt; 8R (✔)
Nombre de trades ≥ 60 (✔)
→ Passage en réel micro avec 0,25 % de risque : sur 6 000 €, 15 € par trade</div>
</x-exemple>
<x-erreurs><ul><li>Fixer les étapes par dates (« dans 3 mois je trade en réel ») plutôt que par critères.</li><li>Augmenter fortement la taille après un bon mois.</li><li>Ne pas prévoir de critère de retour en arrière.</li></ul></x-erreurs>
<x-cles><ul><li>Étapes : formation → démo → réel micro → montée progressive.</li><li>Des critères mesurables pour avancer, et pour reculer.</li><li>Conclure que le trading actif ne vous convient pas est un résultat légitime.</li></ul></x-cles>
<x-exo><p>Rédigez votre plan de progression personnel : capital prévu, critères de passage à chaque étape, risque par trade à chaque palier, critère de retour en arrière.</p>
<x-corr><p>Exemple : « Capital réel prévu : 5 000 €. Démo avec 5 000 € fictifs, risque 1 % : passage en réel après 60 trades, ≥ 90 % conformes, espérance > 0. Réel : 0,25 % (12,50 €) pendant 50 trades, puis 0,5 % si les statistiques restent proches de la démo, puis 0,75 %, puis 1 % au maximum. Retour au palier précédent si le drawdown dépasse 6 % ; retour en démo s'il dépasse 10 %. » Ce qui compte : des chiffres, écrits avant de commencer.</p></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Vérifier avant tout</h2><ul><li>REGAFI (établissements autorisés).</li><li>Listes noires et mises en garde de l'AMF.</li><li>Agrément des prestataires crypto (site de l'AMF).</li><li>ORIAS (conseillers).</li><li>Méfiance : sociétés clones.</li></ul></div>
<div class="encadre"><h2>Comparer un courtier</h2><ul><li>Protection : ségrégation, garantie des avoirs.</li><li>Frais complets selon VOTRE activité.</li><li>Produits, tailles minimales, exécution.</li><li>IFU (France) / déclaration à faire (étranger).</li></ul></div>
<div class="encadre"><h2>Démo</h2><ul><li>Capital et règles identiques au réel prévu.</li><li>Journal obligatoire.</li><li>Exécution idéalisée, pas d'émotions : nécessaire, pas suffisant.</li></ul></div>
<div class="encadre"><h2>Outils</h2><ul><li>Graphiques, plateformes multi-courtiers, plateformes des courtiers.</li><li>Abonnements : coût en % du capital.</li><li>Robots vendus en ligne : méfiance.</li></ul></div>
<div class="encadre"><h2>Arnaques : alertes</h2><ul><li>Rendement garanti, urgence, démarchage.</li><li>Paiement en crypto ou vers l'étranger.</li><li>Impossible de retirer ; frais pour débloquer.</li><li>Faux « récupérateurs » de fonds.</li></ul></div>
<div class="encadre"><h2>Plan de progression</h2><ul><li>Formation → démo → réel micro → montée progressive.</li><li>Critères mesurables (conformité, espérance, drawdown, nombre de trades).</li><li>Critères de retour en arrière.</li></ul></div>
"""

QUIZ = [
("Quelle est la première vérification avant d'ouvrir un compte chez un intermédiaire ?", ["Le montant du bonus d'ouverture", "Son autorisation (REGAFI) et l'absence sur les listes noires de l'AMF", "Le design de son site", "Le levier maximal proposé"], 1, "La vérification réglementaire passe avant toute autre considération."),
("Une « société clone » est :", ["Une filiale d'un courtier", "Une escroquerie qui usurpe l'identité d'un établissement autorisé", "Un courtier à bas coût", "Un compte démo"], 1, "Les escrocs copient nom, logo et parfois numéro d'agrément : il faut contacter la société par ses coordonnées officielles."),
("Courtier A : 0,1 % par ordre. Courtier B : 5 € fixes. À partir de quel montant par ordre B est-il moins cher ?", ["500 €", "5 000 €", "50 000 €", "Jamais"], 1, "0,1 % × montant = 5 € → montant = 5 000 €."),
("Comment régler son compte démo ?", ["Avec le capital maximal proposé", "Avec le capital et les règles de risque prévus pour le compte réel", "Sans stop pour apprendre plus vite", "Peu importe"], 1, "Sinon, l'apprentissage des tailles de position et des émotions est faussé."),
("Principale limite d'un compte démo :", ["Les graphiques sont faux", "L'exécution est souvent idéalisée et la pression émotionnelle absente", "On ne peut pas passer d'ordres stop", "Il est payant"], 1, "Les résultats en démo sont nécessaires mais pas suffisants."),
("Abonnements de 50 € par mois sur un capital de 3 000 €. Coût annuel en % du capital ?", ["2 %", "10 %", "20 %", "50 %"], 2, "50 × 12 = 600 € ; 600 ÷ 3 000 = 20 %."),
("La plateforme affiche des gains, mais on vous demande de payer des « taxes » pour retirer. C'est :", ["Une procédure normale", "Un signal caractéristique d'escroquerie", "Une exigence de l'AMF", "Un appel de marge"], 1, "Un intermédiaire légitime ne demande jamais de payer pour débloquer des fonds."),
("Pourquoi une pyramide de Ponzi s'effondre-t-elle toujours ?", ["Parce que l'AMF la ferme immédiatement", "Parce que les rendements promis ne peuvent être payés qu'avec des dépôts nouveaux toujours croissants", "Parce que les cryptos baissent", "Elle ne s'effondre pas"], 1, "Sans gains réels, la collecte doit croître sans fin : c'est mathématiquement impossible."),
("Après une escroquerie, une société propose de récupérer vos fonds contre une avance de frais. C'est probablement :", ["Un avocat légitime", "Une seconde arnaque (arnaque au recouvrement)", "L'AMF", "Votre banque"], 1, "Les victimes sont souvent ciblées une seconde fois par de faux récupérateurs."),
("Un plan de progression devrait reposer sur :", ["Des dates fixes", "Des critères mesurables (conformité au plan, espérance, drawdown, nombre de trades)", "L'intuition", "Le montant des gains du mois"], 1, "Ce sont les critères qui doivent décider du passage d'une étape à l'autre."),
("Démo : 80 trades, 70 conformes au plan. Taux de conformité ?", ["70 %", "80 %", "87,5 %", "93 %"], 2, "70 ÷ 80 = 87,5 % : sous un critère de 90 %, il faut prolonger la démo."),
]
