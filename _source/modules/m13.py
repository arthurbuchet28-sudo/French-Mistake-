from svgkit import table

NUM = 13
TITRE = "Cadre légal et fiscal en France"
RESUME = "CTO, PEA et ce qu'on peut y trader ; principes d'imposition des plus-values (titres, dérivés, cryptoactifs) ; déclaration des comptes à l'étranger ; où vérifier."
DUREE = "1 h 30"
INTRO = r"""<div class="bloc bloc-attention"><h3 class="bloc-titre">🚨 Avertissement important</h3>
<p>Ce module explique des <strong>mécanismes généraux</strong> de la fiscalité française des particuliers, à la date de rédaction. Il ne donne volontairement <strong>aucun taux ni plafond chiffré</strong> : ils changent régulièrement (lois de finances annuelles, lois de financement de la sécurité sociale). Avant toute décision et toute déclaration, vérifiez les règles en vigueur sur <strong>impots.gouv.fr</strong> (et la doctrine officielle, le BOFiP), <strong>service-public.fr</strong> et le site de l'<strong>AMF</strong>, et consultez un professionnel (expert-comptable, avocat fiscaliste, conseiller en gestion de patrimoine) pour votre situation personnelle. Les exemples chiffrés utilisent des <strong>taux fictifs</strong>, clairement signalés, uniquement pour illustrer les calculs.</p></div>"""

LECONS = [
("13-1", "Les comptes : CTO et PEA", r"""
<x-obj><ul><li>Distinguer compte-titres ordinaire et plan d'épargne en actions.</li><li>Savoir quels produits peuvent être détenus dans chacun.</li></ul></x-obj>
<x-simple>
<ul><li>Le <strong>compte-titres ordinaire</strong> (CTO) peut accueillir presque tous les titres cotés : actions françaises et étrangères, obligations, ETF, warrants, turbos, et selon les courtiers, des options et des futures. Il n'y a ni plafond de versement ni contrainte de durée. Les gains sont imposés selon le régime de droit commun (leçon 13.2).</li>
<li>Le <strong>plan d'épargne en actions</strong> (PEA) est une enveloppe fiscale destinée à financer les entreprises européennes. Il accueille principalement des actions de sociétés ayant leur siège dans l'Union européenne ou l'Espace économique européen, et des fonds ou ETF éligibles (investis majoritairement en actions européennes, y compris certains ETF synthétiques répliquant des indices mondiaux). Il a un <strong>plafond de versements</strong> et un régime fiscal favorable après une certaine durée de détention.</li></ul>
</x-simple>
<x-approfondi>
<p><strong>Ce qu'on ne peut pas mettre dans un PEA</strong> : les CFD et le Forex (qui ne sont d'ailleurs pas des titres), les contrats à terme, les options, les warrants et turbos, les cryptoactifs, les obligations, les actions de sociétés hors UE/EEE détenues en direct. Le PEA est donc peu adapté au trading à effet de levier, mais convient à un trading ou un investissement en actions européennes au comptant.</p>
<p><strong>Mécanisme fiscal du PEA</strong> (sans les chiffres) : tant que les gains restent dans le plan, ils ne sont pas imposés. Au-delà d'une durée minimale de détention, les gains retirés sont exonérés d'impôt sur le revenu mais restent soumis aux prélèvements sociaux. Avant cette durée, un retrait entraîne en principe la clôture du plan et une imposition, sauf exceptions prévues par la loi (les règles ont été assouplies ces dernières années). Il existe aussi le PEA-PME, dédié aux petites et moyennes entreprises.</p>
<p>Les comptes chez un courtier en CFD ou en Forex ne sont pas des CTO au sens strict, mais leurs gains relèvent en général du même régime d'imposition des gains sur instruments financiers (leçon 13.2). Les cryptoactifs ont leur propre régime.</p>
<p>Durées, plafonds et exceptions : à vérifier sur service-public.fr et impots.gouv.fr.</p>
</x-approfondi>
<x-exemple>
""" + table(["Produit", "CTO", "PEA"],
            [["Actions françaises et européennes", "✔", "✔"], ["Actions américaines en direct", "✔", "✗"], ["ETF éligible PEA (y compris certains ETF « monde » synthétiques)", "✔", "✔"],
             ["Obligations", "✔", "✗"], ["Warrants, turbos", "✔", "✗"], ["Options, futures (selon le courtier)", "✔", "✗"],
             ["CFD, Forex", "Compte spécifique chez un courtier en CFD", "✗"], ["Cryptoactifs", "Plateforme ou portefeuille dédié (régime fiscal propre)", "✗"]]) + r"""
<p><strong>Illustration du mécanisme</strong> avec des <strong>taux fictifs</strong> (ne pas utiliser pour vos calculs) : gain de 2 000 € retiré.</p>
<div class="calcul">Taux global fictif sur un CTO : 30 % → impôt = 2 000 × 30 % = 600 € → net = 1 400 €
PEA après la durée minimale, prélèvements sociaux fictifs de 17 % → 2 000 × 17 % = 340 € → net = 1 660 €
Écart = 260 € sur cet exemple. Avec les taux réels, l'écart sera différent : vérifiez-les.</div>
</x-exemple>
<x-erreurs><ul><li>Croire qu'on peut trader des turbos ou des CFD dans un PEA.</li><li>Retirer d'un PEA avant la durée minimale sans connaître les conséquences.</li><li>Choisir une enveloppe uniquement pour la fiscalité, sans vérifier qu'elle accepte les produits voulus.</li></ul></x-erreurs>
<x-cles><ul><li>CTO : presque tous les titres, sans plafond, fiscalité de droit commun.</li><li>PEA : actions européennes et fonds éligibles, plafond, fiscalité favorable après une durée minimale.</li><li>CFD, Forex, dérivés et cryptoactifs : hors PEA.</li></ul></x-cles>
<x-exo><p>Pour chaque produit, indiquez s'il peut être placé dans un PEA : (a) une action allemande ; (b) un turbo sur le CAC 40 ; (c) un ETF éligible PEA répliquant un indice mondial ; (d) une action américaine ; (e) un CFD sur indice.</p>
<x-corr><p>(a) Oui ; (b) Non ; (c) Oui, s'il est bien éligible (le document d'informations clés et le courtier l'indiquent) ; (d) Non en direct ; (e) Non.</p></x-corr></x-exo>
"""),

("13-2", "Les principes de l'imposition des plus-values", r"""
<x-obj><ul><li>Comprendre comment se calcule le gain imposable sur l'année.</li><li>Connaître les grands mécanismes : imposition forfaitaire ou option pour le barème, prélèvements sociaux, imputation des moins-values.</li><li>Découvrir la logique propre aux cryptoactifs.</li></ul></x-obj>
<x-simple>
<p>Pour un particulier, les gains de cession de titres et les profits sur instruments financiers (dont, en général, les CFD, le Forex et les contrats à terme tradés à titre non professionnel) sont imposés <strong>une fois par an</strong>, sur le <strong>solde net</strong> de l'année : plus-values moins moins-values. Ce solde est soumis :</p>
<ul><li>à l'<strong>impôt sur le revenu</strong> : par défaut via un <strong>prélèvement forfaitaire unique</strong> (« flat tax »), ou, sur option globale (valable pour l'ensemble des revenus du capital de l'année), au <strong>barème progressif</strong> ;</li>
<li>aux <strong>prélèvements sociaux</strong>.</li></ul>
<p>Les taux de ces composantes sont fixés par la loi et évoluent : consultez impots.gouv.fr.</p>
</x-simple>
<x-approfondi>
<p><strong>Calcul du gain</strong> : prix de cession − prix d'acquisition, frais d'achat et de vente compris. Pour des titres identiques achetés en plusieurs fois, la règle française utilise le <strong>prix moyen pondéré d'acquisition</strong>.</p>
<p><strong>Moins-values</strong> : elles s'imputent sur les plus-values de même nature de la même année ; l'excédent est reportable sur les années suivantes, dans une limite de temps fixée par la loi.</p>
<p><strong>Dividendes et intérêts</strong> : également des revenus du capital ; les dividendes étrangers peuvent subir une retenue à la source dans le pays d'origine, avec des mécanismes de crédit d'impôt selon les conventions fiscales.</p>
<p><strong>Cryptoactifs</strong> (particuliers, activité non professionnelle) : régime spécifique. L'imposition intervient lors des cessions contre une monnaie ayant cours légal (euros…) ou contre un bien ou un service ; les échanges d'un cryptoactif contre un autre ne sont en principe pas imposables au moment de l'échange. Le gain se calcule selon une formule propre, fondée sur la <strong>valeur globale du portefeuille</strong> de cryptoactifs. Un petit montant annuel de cessions peut être exonéré. Des formulaires spécifiques existent.</p>
<p><strong>Trading habituel et professionnel</strong> : si l'activité présente un caractère professionnel (fréquence, moyens, part des revenus…), le régime peut être différent (bénéfices non commerciaux par exemple). La frontière dépend des circonstances : situation à examiner avec un professionnel.</p>
</x-approfondi>
<x-exemple>
<p><strong>1. Prix moyen pondéré.</strong> Vous achetez 50 actions à 40 € puis 30 actions à 46 € (frais inclus dans les prix pour simplifier), et vendez 60 actions à 50 €.</p>
<div class="calcul">Prix moyen = (50 × 40 + 30 × 46) ÷ 80 = (2 000 + 1 380) ÷ 80 = 42,25 €
Plus-value = 60 × (50 − 42,25) = 60 × 7,75 = 465 €
Il reste 20 actions au prix moyen de 42,25 €</div>
<p><strong>2. Solde annuel.</strong> Plus-values de l'année : 3 500 € ; moins-values de l'année : 1 200 € ; moins-values reportées des années précédentes (encore utilisables) : 800 €.</p>
<div class="calcul">Solde imposable = 3 500 − 1 200 − 800 = 1 500 €
Illustration avec un taux global FICTIF de 30 % : 1 500 × 30 % = 450 € (vérifiez les taux réels)</div>
<p><strong>3. Cryptoactifs (formule de principe).</strong> Valeur globale du portefeuille au moment de la cession : 10 000 € ; prix total d'acquisition du portefeuille : 6 000 € ; vous vendez pour 2 000 € contre des euros.</p>
<div class="calcul">Gain = prix de cession − prix total d'acquisition × (prix de cession ÷ valeur globale)
     = 2 000 − 6 000 × (2 000 ÷ 10 000) = 2 000 − 1 200 = 800 €
Le prix total d'acquisition restant est ensuite diminué de la part utilisée (1 200 €).</div>
</x-exemple>
<x-erreurs><ul><li>Penser que seuls les retraits vers son compte bancaire sont imposables (pour les titres et dérivés, c'est la réalisation du gain dans l'année qui compte).</li><li>Oublier d'imputer les moins-values reportables.</li><li>Croire que les échanges crypto-crypto et les cessions en euros suivent les mêmes règles.</li><li>Se fier à un taux lu sur un forum ou dans un ancien article.</li></ul></x-erreurs>
<x-cles><ul><li>Imposition annuelle du solde net (plus-values − moins-values).</li><li>Impôt sur le revenu (forfaitaire par défaut, barème sur option globale) + prélèvements sociaux.</li><li>Prix moyen pondéré ; moins-values reportables pendant une durée limitée.</li><li>Cryptoactifs : régime propre, formule fondée sur la valeur globale du portefeuille.</li></ul></x-cles>
<x-exo><p>Vous achetez 100 actions à 20 €, puis 100 à 24 €. Vous en vendez 150 à 25 €. Frais : 10 € à chaque achat et 12 € à la vente. Calculez la plus-value.</p>
<x-corr><div class="calcul">Coût total d'acquisition = 100 × 20 + 10 + 100 × 24 + 10 = 4 420 €
Prix moyen pondéré = 4 420 ÷ 200 = 22,10 €
Prix de cession net = 150 × 25 − 12 = 3 738 €
Coût des 150 actions vendues = 150 × 22,10 = 3 315 €
Plus-value = 3 738 − 3 315 = 423 €</div></x-corr></x-exo>
"""),

("13-3", "La déclaration des comptes à l'étranger", r"""
<x-obj><ul><li>Savoir quels comptes doivent être déclarés.</li><li>Connaître les conséquences d'un oubli.</li></ul></x-obj>
<x-simple>
<p>Un résident fiscal français doit déclarer chaque année, avec sa déclaration de revenus, les <strong>comptes ouverts, détenus, utilisés ou clos à l'étranger</strong> au cours de l'année. Cela concerne notamment :</p>
<ul><li>les comptes bancaires et les comptes de paiement (y compris certaines néobanques étrangères) ;</li>
<li>les comptes chez des <strong>courtiers étrangers</strong> (CFD, Forex, actions) ;</li>
<li>les comptes d'<strong>actifs numériques</strong> (cryptoactifs) ouverts auprès de plateformes établies à l'étranger.</li></ul>
<p>Cette déclaration se fait sur un formulaire dédié (n° 3916, ou 3916-bis pour les actifs numériques ; vérifiez les numéros et les modalités en vigueur).</p>
</x-simple>
<x-approfondi>
<p>La déclaration est due <strong>même si le compte est vide, inactif ou a été clos dans l'année</strong>, et indépendamment de tout gain. L'absence de déclaration expose à des <strong>amendes par compte non déclaré</strong> (plus élevées pour certains pays) et peut allonger le délai pendant lequel l'administration peut contrôler. Les montants sont fixés par la loi : vérifiez-les.</p>
<p>Par ailleurs, avec un courtier étranger, vous ne recevez généralement pas l'imprimé fiscal unique (IFU) français : c'est à vous de calculer vos gains et pertes et de les reporter sur les formulaires adéquats. Conservez tous vos relevés.</p>
<p>Sur le plan réglementaire (et non fiscal), un courtier européen peut légalement proposer ses services en France grâce au passeport européen : il apparaît alors dans REGAFI. Un courtier hors UE non autorisé en France est à éviter (module 12).</p>
</x-approfondi>
<x-exemple>
<p>Au cours de l'année, Karim a : un compte chez un courtier en CFD établi à Chypre, un compte sur une plateforme de cryptoactifs établie à Malte (qu'il a fermé en juin), un compte de paiement d'une néobanque lituanienne dont il n'utilise que la carte, et un PEA chez une banque française.</p>
<div class="calcul">Comptes à déclarer comme comptes à l'étranger :
  1. Courtier CFD (Chypre)                    → oui
  2. Plateforme crypto (Malte), même fermée     → oui (compte d'actifs numériques)
  3. Néobanque (Lituanie)                       → oui (compte de paiement à l'étranger)
  4. PEA (France)                               → non (compte en France)
Total : 3 comptes, indépendamment des gains ou pertes réalisés.</div>
</x-exemple>
<x-erreurs><ul><li>Ne pas déclarer un compte « parce qu'il n'y a pas de gain ».</li><li>Oublier un compte clos dans l'année.</li><li>Oublier que les comptes de plateformes de cryptoactifs à l'étranger sont concernés.</li></ul></x-erreurs>
<x-cles><ul><li>Déclarer chaque année tout compte détenu, utilisé, ouvert ou clos à l'étranger (bancaire, courtier, crypto).</li><li>Même vide, même fermé dans l'année.</li><li>Courtier étranger : pas d'IFU, calculs à faire soi-même.</li></ul></x-cles>
<x-exo><p>Vous avez utilisé en démo uniquement (sans argent réel) un compte chez un courtier étranger, et vous avez un compte réel chez un courtier établi en France. Que devez-vous vérifier ?</p>
<x-corr><p>Le compte réel en France n'est pas un compte à l'étranger. Pour le compte de démonstration, la question est de savoir s'il s'agit d'un véritable compte ouvert auprès de l'établissement étranger (avec identification, contrat) ou d'un simple accès à un environnement fictif. En cas de doute, renseignez-vous sur impots.gouv.fr ou auprès de votre service des impôts : déclarer est sans risque, ne pas déclarer peut coûter cher.</p></x-corr></x-exo>
"""),

("13-4", "Où vérifier et quand consulter un professionnel", r"""
<x-obj><ul><li>Connaître les sources officielles fiables.</li><li>Organiser ses justificatifs.</li><li>Savoir quand se faire accompagner.</li></ul></x-obj>
<x-simple>
<p>Sources de référence :</p>
<ul><li><strong>impots.gouv.fr</strong> : règles, formulaires, notices, simulateurs, messagerie sécurisée de l'espace particulier ;</li>
<li><strong>BOFiP</strong> (Bulletin officiel des finances publiques) : la doctrine officielle de l'administration fiscale ;</li>
<li><strong>service-public.fr</strong> : fiches pratiques (PEA, CTO, déclaration des revenus) ;</li>
<li><strong>AMF</strong> : produits, risques, listes noires, protection des épargnants ;</li>
<li>votre <strong>service des impôts</strong>.</li></ul>
<p>Ce que disent un forum, un réseau social ou un influenceur n'a aucune valeur juridique.</p>
</x-simple>
<x-approfondi>
<p><strong>Organiser ses justificatifs</strong> : relevés de compte annuels, avis d'opéré (confirmations de chaque transaction), IFU, historique complet des transactions sur les plateformes de cryptoactifs (à exporter régulièrement : une plateforme peut fermer), tableau de calcul de vos plus-values. Conservez-les plusieurs années.</p>
<p><strong>Quand consulter un professionnel</strong> : activité très fréquente (question du caractère professionnel), courtiers ou plateformes étrangers multiples, cryptoactifs avec de nombreuses opérations (staking, prêts, échanges multiples), produits complexes, montants importants, changement de résidence fiscale, ou simplement au moindre doute. Le coût d'un conseil est souvent bien inférieur à celui d'une erreur.</p>
</x-approfondi>
<x-exemple>
<p>Préparation de la déclaration d'un trader actif (chiffres fictifs) :</p>
<div class="calcul">Courtier français : IFU reçu → plus-values nettes reportées : 1 850 €
Courtier CFD étranger : pas d'IFU → calcul personnel : gains 4 200 €, pertes 3 100 € → solde +1 100 €
Moins-values reportables des années précédentes : 600 €
Solde global sur instruments financiers ≈ 1 850 + 1 100 − 600 = 2 350 € (sous réserve que ces gains relèvent bien du même régime : à vérifier)
Cryptoactifs : calcul séparé selon le régime spécifique
Comptes à l'étranger : 1 (courtier CFD) + plateformes crypto étrangères éventuelles</div>
<p>Ce trader cumule plusieurs régimes et plusieurs plateformes : c'est typiquement un cas où un accompagnement professionnel est utile.</p>
</x-exemple>
<x-erreurs><ul><li>Se fier à un taux ou à une règle trouvés sur un site non officiel ou dans un article ancien.</li><li>Ne pas exporter l'historique d'une plateforme de cryptoactifs avant sa fermeture.</li><li>Attendre la dernière semaine pour reconstituer une année de transactions.</li></ul></x-erreurs>
<x-cles><ul><li>Sources : impots.gouv.fr, BOFiP, service-public.fr, AMF, service des impôts.</li><li>Conserver et organiser tous les justificatifs.</li><li>Situation complexe ou doute : consulter un professionnel.</li></ul></x-cles>
<x-exo><p>Préparez votre « dossier fiscal de trading » : listez les documents à conserver pour chaque compte que vous ouvrez ou envisagez d'ouvrir.</p>
<x-corr><p>Pour chaque compte : contrat d'ouverture et pays de l'établissement ; relevés annuels ; avis d'opéré ou historique complet des transactions ; IFU s'il existe ; justificatifs de frais ; pour les cryptoactifs, export complet des transactions avec dates, montants en euros et valeur du portefeuille ; copie des déclarations déposées (y compris celles des comptes à l'étranger) ; votre tableau de calcul des gains. Le tout classé par année.</p></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>⚠️ Règle d'or</h2><ul><li>Aucun taux ni plafond ici : ils changent.</li><li>Vérifier sur impots.gouv.fr, BOFiP, service-public.fr, AMF.</li><li>Consulter un professionnel en cas de doute.</li></ul></div>
<div class="encadre"><h2>Enveloppes</h2><ul><li>CTO : presque tous les titres, sans plafond.</li><li>PEA : actions UE/EEE et fonds éligibles ; plafond ; avantage après une durée minimale.</li><li>Hors PEA : CFD, Forex, dérivés, turbos, cryptos, obligations.</li></ul></div>
<div class="encadre"><h2>Imposition des gains</h2><ul><li>Solde annuel net (plus-values − moins-values).</li><li>IR (forfaitaire par défaut, ou barème sur option globale) + prélèvements sociaux.</li><li>Prix moyen pondéré ; moins-values reportables (durée limitée).</li><li>Activité habituelle : régime possiblement différent.</li></ul></div>
<div class="encadre"><h2>Cryptoactifs</h2><ul><li>Imposition à la cession contre euros ou biens/services.</li><li>Échanges crypto-crypto : en principe non imposables à l'échange.</li><li>Gain = cession − acquisition totale × (cession ÷ valeur globale).</li></ul></div>
<div class="encadre"><h2>Comptes à l'étranger</h2><ul><li>Déclarer chaque compte (banque, courtier, crypto) détenu, utilisé, ouvert ou clos.</li><li>Même vide ou fermé ; amendes par compte non déclaré.</li><li>Courtier étranger : pas d'IFU.</li></ul></div>
<div class="encadre"><h2>Justificatifs</h2><ul><li>Relevés, avis d'opéré, IFU, exports crypto, tableau de calcul.</li><li>Conserver plusieurs années.</li></ul></div>
"""

QUIZ = [
("Peut-on détenir des turbos dans un PEA ?", ["Oui", "Non", "Seulement sur le CAC 40", "Seulement après 5 ans"], 1, "Les warrants et turbos ne sont pas éligibles au PEA."),
("Quel compte accepte des actions américaines en direct ?", ["Le PEA", "Le compte-titres ordinaire (CTO)", "Aucun", "Le livret A"], 1, "Le CTO accepte la plupart des titres cotés, sans contrainte géographique."),
("Comment est imposé, en principe, un particulier sur ses gains de cession de titres ?", ["Trade par trade, au moment de chaque vente", "Sur le solde net annuel (plus-values − moins-values)", "Uniquement lors du retrait vers sa banque", "Jamais"], 1, "C'est le solde net de l'année qui est imposé."),
("Achat de 40 actions à 10 € puis 60 à 15 €. Prix moyen pondéré ?", ["12,50 €", "13,00 €", "12,00 €", "15,00 €"], 1, "(400 + 900) ÷ 100 = 13 €."),
("Plus-values 5 000 €, moins-values de l'année 2 000 €, moins-values reportables 1 000 €. Solde imposable ?", ["5 000 €", "3 000 €", "2 000 €", "8 000 €"], 2, "5 000 − 2 000 − 1 000 = 2 000 €."),
("Cryptoactifs : un échange d'un cryptoactif contre un autre est en principe :", ["Imposable immédiatement", "Non imposable au moment de l'échange (régime des particuliers)", "Interdit", "Soumis à la TVA"], 1, "L'imposition intervient lors des cessions contre une monnaie ayant cours légal ou contre un bien ou un service."),
("Portefeuille crypto : valeur globale 20 000 €, acquisition totale 8 000 €, cession de 5 000 €. Gain selon la formule ?", ["5 000 €", "3 000 €", "2 000 €", "12 000 €"], 1, "5 000 − 8 000 × (5 000 ÷ 20 000) = 5 000 − 2 000 = 3 000 €."),
("Faut-il déclarer un compte chez un courtier étranger fermé en cours d'année et sans gain ?", ["Non", "Oui", "Seulement s'il y a eu des gains", "Seulement au-delà d'un certain montant"], 1, "Tout compte ouvert, détenu, utilisé ou clos à l'étranger dans l'année doit être déclaré."),
("Où trouver la doctrine officielle de l'administration fiscale ?", ["Sur un forum de traders", "Dans le BOFiP", "Sur les réseaux sociaux", "Dans le document d'un courtier"], 1, "Le Bulletin officiel des finances publiques (BOFiP) publie la doctrine de l'administration."),
("Pourquoi ce module ne donne-t-il pas les taux d'imposition ?", ["Parce qu'il n'y en a pas", "Parce qu'ils changent régulièrement et doivent être vérifiés à la source", "Parce qu'ils sont secrets", "Parce qu'ils sont identiques pour tous les produits"], 1, "Les taux et plafonds évoluent avec les lois de finances : seule la source officielle à jour fait foi."),
]
