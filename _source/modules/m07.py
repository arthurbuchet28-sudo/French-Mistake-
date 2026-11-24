from svgkit import plot, table, svg, t, line, arrow, path_from, candles

NUM = 7
TITRE = "Analyse fondamentale"
RESUME = "PIB, inflation, emploi, banques centrales (BCE, Fed), calendrier économique, résultats d'entreprises, ratios (PER, BPA, dividende) et sentiment de marché."
DUREE = "2 h 30"
INTRO = r"""<p>L'<strong>analyse fondamentale</strong> cherche à comprendre ce qui détermine la valeur d'un actif : l'état de l'économie, la politique des banques centrales, les résultats des entreprises. Même un trader purement « technique » doit la connaître, ne serait-ce que pour savoir <em>quand</em> le marché risque de bouger violemment (publications économiques, résultats) et pourquoi.</p>"""


def _transmission():
    W = 720
    p = []
    def b(x, y, w, a, c="", cls="g-rect"):
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="46" rx="8" class="{cls}"/>')
        p.append(t(x + w / 2, y + 20, a, "g-txt g-fort", "middle"))
        if c:
            p.append(t(x + w / 2, y + 37, c, "g-txt g-petit", "middle"))
    b(270, 8, 180, "Banque centrale", "relève ses taux directeurs", "g-rect-a")
    items = [(6, "Crédit plus cher", "conso. et investissement ↓"), (184, "Rendements obligataires ↑", "prix des obligations ↓"),
             (362, "Devise souvent ↑", "placements mieux rémunérés"), (540, "Actions sous pression", "bénéfices actualisés ↓")]
    for x, a, c in items:
        b(x, 104, 172, a, c)
        p.append(arrow(360, 54, x + 86, 104))
    b(210, 196, 300, "Objectif : ralentir l'inflation", "effets avec retard, souvent de plusieurs trimestres", "g-rect-h")
    for x, _, _ in items:
        p.append(arrow(x + 86, 150, 360, 196))
    return svg(W, 252, "".join(p), "Canaux de transmission d'une hausse des taux directeurs (effets habituels, non garantis)")


SCHEMA_TRANSMISSION = _transmission()

_A = path_from([(0, 1.0850), (20, 1.0856), (21, 1.0856)], seed=3, noise=0.00015, wick=0.0001)
_B = [(1.0856, 1.0861, 1.0792, 1.0801), (1.0801, 1.0830, 1.0788, 1.0822), (1.0822, 1.0840, 1.0805, 1.0811)]
_C = path_from([(0, 1.0811), (15, 1.0800)], seed=4, noise=0.0002, wick=0.00015)[1:]
SCHEMA_ANNONCE = candles(_A + _B + _C, label="Réaction d'EUR/USD (bougies d'une minute) à une statistique américaine meilleure que prévu", dec=4,
                         marks=[{"i": 21, "p": 1.0792, "t": "Publication : −55 pips en 1 minute", "pos": "bas", "anchor": "start"}])

SCHEMA_PMI = plot([{"x": list(range(1, 13)), "y": [52.1, 51.4, 50.8, 50.2, 49.6, 48.9, 48.7, 49.3, 49.9, 50.4, 51.0, 51.6], "kind": "bar",
                    "cls": "g-barre-a", "bw": 22}],
                  label="Indice PMI manufacturier fictif sur 12 mois", yr=(46, 54), legend=False,
                  hlines=[{"y": 50, "cls": "g-lb", "label": "50 : seuil expansion / contraction"}],
                  xticks=list(range(1, 13)), xfmt=lambda v: f"M{int(v)}", xlabel="Mois (données fictives)")

LECONS = [
("7-1", "Les grands indicateurs macroéconomiques", r"""
<x-obj><ul><li>Connaître les principaux indicateurs : PIB, inflation, emploi, PMI.</li><li>Savoir lire une variation trimestrielle, annuelle ou annualisée.</li></ul></x-obj>
<x-simple>
<ul><li><strong>PIB</strong> (produit intérieur brut) : la valeur de tout ce qui est produit dans un pays. Sa croissance mesure l'activité économique. Publié chaque trimestre, avec des révisions.</li>
<li><strong>Inflation</strong> : hausse générale des prix, mesurée par l'indice des prix à la consommation (IPC ; CPI aux États-Unis ; IPCH harmonisé en zone euro). L'inflation « sous-jacente » (core) exclut les éléments les plus volatils (énergie, alimentation).</li>
<li><strong>Emploi</strong> : taux de chômage, créations d'emplois. Aux États-Unis, le rapport mensuel sur l'emploi (dont les créations d'emplois hors secteur agricole, les « NFP ») est l'une des publications les plus suivies au monde.</li>
<li><strong>PMI</strong> (indices des directeurs d'achat) : enquêtes mensuelles auprès des entreprises. Au-dessus de 50, l'activité est jugée en expansion ; en dessous, en contraction. Ils sont publiés tôt et anticipent souvent les statistiques « dures ».</li></ul>
</x-simple>
<x-fig c="Exemple fictif : un PMI qui passe sous 50 signale une contraction de l'activité, puis repasse au-dessus.">""" + SCHEMA_PMI + r"""</x-fig>
<x-approfondi>
<p><strong>Attention aux conventions</strong> : la croissance du PIB américain est publiée en rythme <strong>annualisé</strong> (la variation trimestrielle « projetée » sur un an), alors que la zone euro publie d'abord la variation <strong>trimestrielle</strong> brute. Un « +2 % » américain et un « +0,5 % » européen peuvent décrire un rythme comparable.</p>
<p>Les marchés réagissent moins au chiffre qu'à l'<strong>écart avec les attentes</strong> (leçon 7.3), et aux conséquences pour la politique monétaire : une inflation plus forte que prévu fait craindre des taux plus élevés.</p>
<p>D'autres indicateurs comptent : ventes au détail, production industrielle, confiance des consommateurs, balance commerciale, demandes hebdomadaires d'allocations chômage aux États-Unis, indice ZEW et IFO en Allemagne…</p>
</x-approfondi>
<x-exemple>
<div class="calcul">PIB en hausse de 0,5 % sur un trimestre
Variation annualisée = (1 + 0,005)^4 − 1 ≈ 2,02 %
Inversement, un PIB américain annualisé à +1,2 %
correspond à une variation trimestrielle de (1,012)^(1/4) − 1 ≈ 0,30 %
Inflation : IPC à 104,2 contre 101,6 un an plus tôt → (104,2 ÷ 101,6) − 1 ≈ 2,56 % sur un an</div>
</x-exemple>
<x-erreurs><ul><li>Comparer un PIB annualisé à un PIB trimestriel.</li><li>Oublier les révisions : le chiffre du mois précédent peut être fortement corrigé.</li><li>Trader le chiffre « en soi » sans connaître les attentes.</li></ul></x-erreurs>
<x-cles><ul><li>PIB (activité), inflation (prix), emploi, PMI (seuil 50).</li><li>Trimestriel ≠ annualisé : annualisé ≈ (1 + trimestriel)^4 − 1.</li><li>Les marchés réagissent à la surprise et aux implications pour les taux.</li></ul></x-cles>
<x-exo><p>Un PIB progresse de 0,8 % sur un trimestre. Quelle est la croissance annualisée ? L'IPC passe de 118,0 à 121,5 en un an : quelle est l'inflation ?</p>
<x-corr><div class="calcul">Annualisé = 1,008^4 − 1 ≈ 3,24 %
Inflation = 121,5 ÷ 118,0 − 1 ≈ 2,97 %</div></x-corr></x-exo>
"""),

("7-2", "Les banques centrales et les taux directeurs", r"""
<x-obj><ul><li>Comprendre le rôle de la BCE et de la Fed.</li><li>Connaître les canaux de transmission des taux vers les marchés.</li><li>Calculer un taux réel et un écart de taux.</li></ul></x-obj>
<x-simple>
<p>Les <strong>banques centrales</strong> fixent les taux d'intérêt de court terme (les <strong>taux directeurs</strong>). En les relevant, elles rendent le crédit plus cher et freinent l'inflation ; en les baissant, elles soutiennent l'activité.</p>
<ul><li>La <strong>BCE</strong> (Banque centrale européenne, Francfort) a pour mandat principal la stabilité des prix, avec un objectif d'inflation de 2 % à moyen terme. Son Conseil des gouverneurs se réunit environ toutes les six semaines pour la politique monétaire.</li>
<li>La <strong>Fed</strong> (Réserve fédérale américaine) a un double mandat : stabilité des prix (objectif de 2 %) et plein emploi. Son comité, le FOMC, se réunit huit fois par an et fixe une fourchette cible pour le taux des fonds fédéraux.</li></ul>
<p>Les niveaux de taux changent : consultez les sites de la BCE et de la Fed pour les valeurs en vigueur.</p>
</x-simple>
<x-fig c="Une hausse de taux agit par plusieurs canaux. Ces effets sont habituels mais pas automatiques : tout dépend de ce que le marché avait déjà anticipé.">""" + SCHEMA_TRANSMISSION + r"""</x-fig>
<x-approfondi>
<p>Au-delà des taux, les banques centrales utilisent leur <strong>bilan</strong> (achats massifs d'obligations, dits « assouplissement quantitatif » ou QE, et leur réduction, QT) et leur <strong>communication</strong> (forward guidance). Les marchés réagissent souvent davantage aux conférences de presse et aux projections qu'à la décision elle-même, généralement anticipée.</p>
<p>Le <strong>taux réel</strong> (taux nominal − inflation) mesure le vrai coût de l'argent. L'<strong>écart de taux</strong> entre deux pays est un moteur important des devises : les capitaux ont tendance à aller vers les devises mieux rémunérées (c'est le principe du « carry trade », qui peut se retourner brutalement).</p>
<p>Vocabulaire : une banque centrale « <strong>hawkish</strong> » (faucon) privilégie la lutte contre l'inflation (taux plus hauts) ; « <strong>dovish</strong> » (colombe) privilégie le soutien à l'activité.</p>
</x-approfondi>
<x-exemple>
<div class="calcul">Taux directeur = 3,50 % ; inflation = 2,40 %
Taux réel ≈ 3,50 − 2,40 = +1,10 % (politique plutôt restrictive)
Si l'inflation était à 5 % : taux réel ≈ 3,50 − 5,00 = −1,50 % (encore accommodant)

Écart de taux : zone A à 4,25 %, zone B à 2,00 %
Écart = 2,25 points. Sur 100 000 € placés un an, la différence d'intérêts = 2 250 €
(avant coûts, et sans compter le risque de change, qui peut effacer ce gain)</div>
</x-exemple>
<x-erreurs><ul><li>Croire qu'une hausse de taux fait forcément monter la devise : si elle était anticipée, ou jugée insuffisante, la devise peut baisser.</li><li>Trader pendant la conférence de presse d'une banque centrale sans plan : les mouvements sont rapides et contradictoires.</li></ul></x-erreurs>
<x-cles><ul><li>BCE : stabilité des prix (2 %). Fed : prix (2 %) et emploi.</li><li>Taux ↑ : crédit plus cher, obligations ↓, devise souvent ↑, actions sous pression.</li><li>Taux réel = nominal − inflation ; l'écart de taux influence les devises.</li></ul></x-cles>
<x-exo><p>Une banque centrale relève ses taux de 0,25 point alors que le marché attendait 0,50 point. Comment la devise pourrait-elle réagir, et pourquoi ?</p>
<x-corr><p>La devise pourrait <strong>baisser</strong> malgré la hausse de taux : le marché avait déjà intégré une hausse de 0,50 point. La décision est moins « hawkish » que prévu. Ce qui compte, c'est l'écart avec les attentes.</p></x-corr></x-exo>
"""),

("7-3", "Le calendrier économique", r"""
<x-obj><ul><li>Lire un calendrier économique (précédent, consensus, réel).</li><li>Mesurer une surprise et anticiper la volatilité.</li></ul></x-obj>
<x-simple>
<p>Un <strong>calendrier économique</strong> (proposé gratuitement par de nombreux sites et courtiers) liste les publications à venir avec leur heure, leur importance (souvent 1 à 3 étoiles), le chiffre <strong>précédent</strong>, le <strong>consensus</strong> (prévision moyenne des économistes) et, après publication, le chiffre <strong>réel</strong>.</p>
</x-simple>
<x-fig c="Exemple illustratif : à la publication, le prix peut parcourir en une minute plus que pendant l'heure précédente. Spreads et slippage explosent.">""" + SCHEMA_ANNONCE + r"""</x-fig>
<x-approfondi>
<p>La <strong>surprise</strong> = réel − consensus. Elle s'apprécie par rapport à la dispersion habituelle des prévisions. Il faut aussi regarder les <strong>révisions</strong> du chiffre précédent et le <strong>détail</strong> (pour l'emploi : salaires, taux de chômage, heures travaillées) : un chiffre principal bon avec des détails mauvais peut provoquer des allers-retours violents.</p>
<p>Règle de prudence pour un débutant : <strong>ne pas avoir de position ouverte</strong> (ou une position réduite) sur un actif concerné au moment d'une publication majeure, et éviter d'ouvrir une position dans les minutes qui suivent.</p>
</x-approfondi>
<x-exemple>
""" + table(["Publication", "Précédent", "Consensus", "Réel"],
            [["Créations d'emplois (États-Unis)", "200 k (révisé à 150 k)", "180 k", "250 k"], ["Taux de chômage", "4,1 %", "4,1 %", "4,0 %"], ["Salaire horaire moyen (sur un mois)", "+0,3 %", "+0,3 %", "+0,5 %"]]) + r"""
<div class="calcul">Surprise sur les emplois = 250 − 180 = +70 000 (forte)
Mais révision du mois précédent = 150 − 200 = −50 000
Surprise nette sur deux mois ≈ +70 − 50 = +20 000 (beaucoup plus modeste)
Salaires plus forts que prévu (+0,5 % contre +0,3 %) → risque d'inflation → taux plus élevés anticipés</div>
<p>Interprétation probable : signal plutôt favorable au dollar (économie solide, salaires dynamiques), mais la révision tempère. La réaction peut être confuse pendant plusieurs minutes.</p>
</x-exemple>
<x-erreurs><ul><li>Ignorer le calendrier et se faire surprendre par une annonce.</li><li>Placer un stop serré juste avant une publication : il risque d'être touché par un pic, avec du slippage.</li><li>Lire seulement le chiffre principal.</li></ul></x-erreurs>
<x-cles><ul><li>Consultez le calendrier avant chaque séance.</li><li>Surprise = réel − consensus ; tenir compte des révisions et des détails.</li><li>Autour des publications : spreads larges, slippage, mouvements erratiques.</li></ul></x-cles>
<x-exo><p>Inflation sur un an : précédent 3,1 %, consensus 2,9 %, réel 3,2 %. Quelle est la surprise ? Quel effet probable sur les anticipations de taux et sur la devise ?</p>
<x-corr><div class="calcul">Surprise = 3,2 − 2,9 = +0,3 point (inflation plus forte que prévu)</div><p>Le marché peut anticiper des taux plus élevés plus longtemps : plutôt favorable à la devise, défavorable aux obligations (rendements en hausse). Ce n'est qu'une tendance : la réaction dépend du contexte et des autres données.</p></x-corr></x-exo>
"""),

("7-4", "Les résultats d'entreprise", r"""
<x-obj><ul><li>Lire les éléments clés d'une publication de résultats.</li><li>Comprendre pourquoi une action peut baisser malgré de « bons » résultats.</li></ul></x-obj>
<x-simple>
<p>Les entreprises cotées publient leurs résultats régulièrement (trimestriellement aux États-Unis ; souvent semestriellement, avec des informations trimestrielles, en Europe). On y regarde notamment :</p>
<ul><li>le <strong>chiffre d'affaires</strong> (ventes) ;</li><li>les <strong>marges</strong> (part des ventes qui reste en bénéfice) ;</li><li>le <strong>résultat net</strong> et le <strong>BPA</strong> (bénéfice par action) ;</li><li>les <strong>perspectives</strong> (guidance) annoncées par la direction.</li></ul>
<p>Comme pour la macroéconomie, c'est l'écart avec les attentes des analystes (le consensus) qui fait bouger le cours.</p>
</x-simple>
<x-approfondi>
<p>Les publications ont souvent lieu avant l'ouverture ou après la clôture : elles provoquent des <strong>gaps</strong> (module 2). La guidance compte souvent plus que les chiffres passés : une entreprise peut battre le consensus (« beat ») et chuter parce qu'elle prévoit un trimestre suivant décevant.</p>
<p>Attention aux indicateurs « ajustés » (hors éléments exceptionnels) choisis par l'entreprise : ils peuvent flatter la réalité. Comparez avec les chiffres selon les normes comptables (IFRS en Europe, US GAAP aux États-Unis).</p>
</x-approfondi>
<x-exemple>
""" + table(["", "Année N − 1", "Année N", "Variation"],
            [["Chiffre d'affaires", "2 000 M€", "2 200 M€", "+10 %"], ["Résultat opérationnel", "300 M€", "308 M€", "+2,7 %"],
             ["Résultat net", "200 M€", "210 M€", "+5 %"], ["Nombre d'actions", "100 M", "100 M", ""]]) + r"""
<div class="calcul">Marge opérationnelle N − 1 = 300 ÷ 2 000 = 15,0 %
Marge opérationnelle N = 308 ÷ 2 200 = 14,0 % → la marge baisse d'un point
BPA N − 1 = 200 ÷ 100 = 2,00 € ; BPA N = 210 ÷ 100 = 2,10 € (+5 %)
Consensus BPA = 2,15 € → résultat inférieur aux attentes de (2,10 − 2,15) ÷ 2,15 ≈ −2,3 %</div>
<p>Les ventes progressent bien, mais la rentabilité se dégrade et le BPA manque le consensus : une baisse du cours est possible malgré la croissance.</p>
</x-exemple>
<x-erreurs><ul><li>Garder une position importante pendant la publication de résultats (risque de gap).</li><li>Juger un résultat sans le comparer au consensus et à la guidance.</li><li>Se fier uniquement aux indicateurs « ajustés ».</li></ul></x-erreurs>
<x-cles><ul><li>Chiffre d'affaires, marges, résultat net, BPA, guidance.</li><li>Surprise par rapport au consensus et perspectives : les vrais moteurs du cours.</li><li>Publications hors séance : risque de gap.</li></ul></x-cles>
<x-exo><p>Une entreprise réalise 500 M€ de chiffre d'affaires et 60 M€ de résultat net, avec 40 millions d'actions. Calculez la marge nette et le BPA. Le consensus attendait un BPA de 1,40 € : est-ce un « beat » ?</p>
<x-corr><div class="calcul">Marge nette = 60 ÷ 500 = 12 %
BPA = 60 ÷ 40 = 1,50 €
Écart = (1,50 − 1,40) ÷ 1,40 ≈ +7,1 % → oui, BPA supérieur aux attentes</div><p>La réaction du cours dépendra aussi de la guidance et de la qualité du résultat.</p></x-corr></x-exo>
"""),

("7-5", "Les ratios de valorisation : capitalisation, PER, BPA, dividende", r"""
<x-obj><ul><li>Calculer la capitalisation, le BPA, le PER et le rendement du dividende.</li><li>Comprendre les limites des comparaisons de ratios.</li></ul></x-obj>
<x-simple>
<ul><li><strong>Capitalisation boursière</strong> = cours × nombre d'actions. C'est la valeur de l'entreprise en bourse (pour les actionnaires).</li>
<li><strong>BPA</strong> (bénéfice par action) = résultat net ÷ nombre d'actions.</li>
<li><strong>PER</strong> (Price Earnings Ratio) = cours ÷ BPA. Il indique combien d'années de bénéfices actuels le marché paie. Un PER élevé traduit des attentes de croissance (ou une surévaluation) ; un PER bas, des doutes (ou une opportunité).</li>
<li><strong>Rendement du dividende</strong> = dividende par action ÷ cours.</li>
<li><strong>Taux de distribution</strong> (payout) = dividende ÷ BPA.</li></ul>
</x-simple>
<x-approfondi>
<p>On distingue le PER sur les bénéfices passés (trailing) et sur les bénéfices estimés (forward). Un PER n'a de sens que comparé : à l'historique de l'entreprise, à son secteur, à sa croissance (le ratio PEG = PER ÷ taux de croissance annuel du BPA en %). Les PER des banques, des entreprises technologiques et des services publics ne sont pas comparables entre eux.</p>
<p>Limites : le BPA peut être gonflé ou déprimé par des éléments exceptionnels ; les entreprises en perte n'ont pas de PER significatif ; d'autres ratios existent (valeur d'entreprise / EBITDA, cours / valeur comptable, cours / chiffre d'affaires). Le rendement du dividende élevé peut être un piège si le cours a chuté parce que le dividende risque d'être réduit.</p>
<p>Le « rendement des bénéfices » (1 ÷ PER) est parfois comparé au rendement des obligations d'État pour juger de la cherté relative des actions. C'est une comparaison discutée, car elle compare un rendement réel incertain à un rendement nominal garanti.</p>
</x-approfondi>
<x-exemple>
<p>Action à 45 €, 200 millions d'actions, BPA 3,00 €, dividende 1,35 €.</p>
<div class="calcul">Capitalisation = 45 × 200 000 000 = 9 milliards €
PER = 45 ÷ 3,00 = 15
Rendement des bénéfices = 1 ÷ 15 ≈ 6,7 %
Rendement du dividende = 1,35 ÷ 45 = 3,0 %
Taux de distribution = 1,35 ÷ 3,00 = 45 %
Si le BPA croît de 10 % par an : PEG = 15 ÷ 10 = 1,5</div>
</x-exemple>
<x-erreurs><ul><li>Acheter une action « parce que le PER est bas » sans chercher pourquoi.</li><li>Comparer les PER de secteurs différents.</li><li>Confondre capitalisation et chiffre d'affaires.</li><li>Choisir une action uniquement pour un rendement du dividende très élevé.</li></ul></x-erreurs>
<x-cles><ul><li>Capitalisation = cours × actions ; BPA = résultat net ÷ actions.</li><li>PER = cours ÷ BPA ; rendement = dividende ÷ cours ; payout = dividende ÷ BPA.</li><li>Un ratio se juge par comparaison (historique, secteur, croissance).</li></ul></x-cles>
<x-exo><p>Entreprise : résultat net 1,2 Md€, 300 millions d'actions, cours 80 €, dividende 2 € par action. Calculez le BPA, le PER, la capitalisation, le rendement et le taux de distribution.</p>
<x-corr><div class="calcul">BPA = 1 200 ÷ 300 = 4,00 €
PER = 80 ÷ 4 = 20
Capitalisation = 80 × 300 M = 24 Md€
Rendement du dividende = 2 ÷ 80 = 2,5 %
Taux de distribution = 2 ÷ 4 = 50 %</div></x-corr></x-exo>
"""),

("7-6", "Le sentiment de marché et l'actualité", r"""
<x-obj><ul><li>Connaître les mesures de sentiment (VIX, enquêtes, positionnement).</li><li>Comprendre le « buy the rumor, sell the news ».</li><li>Convertir le VIX en mouvement attendu.</li></ul></x-obj>
<x-simple>
<p>Le <strong>sentiment de marché</strong> est l'humeur collective des investisseurs : optimisme (risk-on : actions, devises cycliques et cryptos recherchées) ou peur (risk-off : refuge vers les obligations d'État, le dollar, le yen, le franc suisse, l'or). Il peut pousser les prix bien au-delà de ce que justifient les fondamentaux, dans les deux sens.</p>
</x-simple>
<x-approfondi>
<ul><li>Le <strong>VIX</strong>, souvent appelé « indice de la peur », mesure la volatilité implicite à 30 jours du S&amp;P 500, tirée des prix des options. Il monte quand les investisseurs achètent de la protection. (Il existe un équivalent européen, le VSTOXX.)</li>
<li><strong>Enquêtes</strong> de sentiment auprès des investisseurs particuliers ou des gérants.</li>
<li><strong>Positionnement</strong> : le rapport hebdomadaire COT (Commitments of Traders) de la CFTC américaine montre les positions sur les contrats à terme par catégorie d'intervenants.</li>
<li><strong>Ratio put/call</strong> : volume d'options de vente rapporté aux options d'achat.</li></ul>
<p>Les extrêmes de sentiment sont parfois utilisés « à contre-courant » (quand tout le monde est euphorique, il reste peu d'acheteurs), mais le sentiment peut rester extrême longtemps.</p>
<p>« <strong>Acheter la rumeur, vendre la nouvelle</strong> » : un événement attendu est souvent déjà intégré dans les prix ; quand il se produit, les acheteurs prennent leurs bénéfices et le prix baisse. D'où l'importance de distinguer l'information <em>nouvelle</em> de l'information <em>déjà connue</em>.</p>
</x-approfondi>
<x-exemple>
<p>Le VIX est à 20. Il s'exprime en volatilité annualisée (en %). Le mouvement « d'un écart-type » attendu par le marché des options est donc d'environ :</p>
<div class="calcul">Sur 30 jours (≈ 1/12 d'année) : 20 % ÷ √12 ≈ 20 ÷ 3,46 ≈ 5,8 %
Sur 1 jour de bourse : 20 % ÷ √252 ≈ 20 ÷ 15,87 ≈ 1,26 %
Avec le VIX à 40 : ≈ 2,5 % par jour, soit des séances deux fois plus agitées</div>
<p>« Un écart-type » signifie qu'environ deux tiers des mouvements devraient être inférieurs à ce chiffre si la loi normale s'appliquait, ce qui n'est qu'une approximation.</p>
</x-exemple>
<x-erreurs><ul><li>Trader les titres de presse en temps réel : les professionnels reçoivent l'information plus vite et par des flux automatisés.</li><li>Croire qu'une « bonne nouvelle » fait forcément monter le prix.</li><li>Se laisser emporter par le sentiment des réseaux sociaux (module 11 : FOMO).</li></ul></x-erreurs>
<x-cles><ul><li>Risk-on / risk-off ; valeurs refuges.</li><li>VIX : volatilité implicite à 30 jours ; mouvement journalier ≈ VIX ÷ √252.</li><li>Ce qui est attendu est déjà dans les prix (« buy the rumor, sell the news »).</li></ul></x-cles>
<x-exo><p>Le VIX passe de 14 à 28. Quel est le mouvement journalier « typique » attendu avant et après ? Quelle conséquence pour la taille de vos positions si vous gardez le même risque en euros ?</p>
<x-corr><div class="calcul">Avant : 14 ÷ 15,87 ≈ 0,88 % par jour
Après : 28 ÷ 15,87 ≈ 1,76 % par jour (deux fois plus)</div><p>Pour garder le même risque, les stops doivent être plus éloignés et les positions environ <strong>deux fois plus petites</strong>.</p></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Macroéconomie</h2><ul><li>PIB, inflation (IPC, core), emploi (NFP, chômage), PMI (seuil 50).</li><li>Annualisé = (1 + trimestriel)<sup>4</sup> − 1.</li><li>On réagit à la surprise et aux implications pour les taux.</li></ul></div>
<div class="encadre"><h2>Banques centrales</h2><ul><li>BCE : prix (2 %). Fed : prix (2 %) + emploi ; FOMC 8 fois par an.</li><li>Taux ↑ : obligations ↓, devise souvent ↑, actions sous pression.</li><li>Taux réel = nominal − inflation. Hawkish / dovish.</li></ul></div>
<div class="encadre"><h2>Calendrier</h2><ul><li>Précédent / consensus / réel ; surprise = réel − consensus.</li><li>Révisions et détails.</li><li>Pas de position (ou réduite) pendant les publications majeures.</li></ul></div>
<div class="encadre"><h2>Résultats</h2><ul><li>CA, marges, résultat net, BPA, guidance.</li><li>Beat / miss vs consensus ; guidance souvent décisive.</li><li>Publications hors séance → gaps.</li></ul></div>
<div class="encadre"><h2>Ratios</h2><ul><li>Capitalisation = cours × actions.</li><li>BPA = RN ÷ actions ; PER = cours ÷ BPA.</li><li>Rendement = dividende ÷ cours ; payout = dividende ÷ BPA.</li><li>Comparer dans le même secteur.</li></ul></div>
<div class="encadre"><h2>Sentiment</h2><ul><li>Risk-on / risk-off ; valeurs refuges.</li><li>VIX : mouvement/jour ≈ VIX ÷ √252.</li><li>COT, put/call, enquêtes.</li><li>Buy the rumor, sell the news.</li></ul></div>
"""

QUIZ = [
("Un PMI à 48 signifie généralement :", ["Une expansion de l'activité", "Une contraction de l'activité", "Une inflation de 48 %", "Un chômage de 48 %"], 1, "Le seuil est 50 : en dessous, l'activité est jugée en contraction."),
("Croissance trimestrielle de 1 %. Croissance annualisée approximative ?", ["1 %", "4,06 %", "12 %", "0,25 %"], 1, "1,01^4 − 1 ≈ 4,06 %."),
("Le mandat de la Fed comprend :", ["La stabilité des prix uniquement", "La stabilité des prix et le plein emploi", "Le cours du dollar uniquement", "Le niveau des actions"], 1, "C'est le double mandat de la Fed ; la BCE a pour mandat principal la stabilité des prix."),
("Taux directeur 4 %, inflation 5 %. Taux réel approximatif ?", ["+9 %", "+1 %", "−1 %", "−9 %"], 2, "4 − 5 = −1 % : le taux réel est négatif."),
("Une banque centrale relève ses taux moins que prévu. La devise :", ["Monte forcément", "Peut baisser, car la décision est moins restrictive qu'anticipé", "Ne bouge jamais", "Double"], 1, "Le marché réagit à l'écart avec les attentes."),
("Consensus 180 k, réel 220 k. La surprise est de :", ["−40 k", "+40 k", "+220 k", "0"], 1, "Surprise = réel − consensus = +40 000."),
("Pourquoi éviter d'avoir une position au moment d'une publication majeure quand on débute ?", ["Parce que c'est interdit", "Spreads élargis, slippage et mouvements erratiques", "Parce que les marchés ferment", "Parce que les courtiers ne cotent plus jamais"], 1, "Les conditions d'exécution se dégradent fortement autour des publications."),
("Résultat net 50 M€, 25 millions d'actions, cours 30 €. PER ?", ["2", "10", "15", "25"], 2, "BPA = 50 ÷ 25 = 2 € ; PER = 30 ÷ 2 = 15."),
("Dividende 1,20 €, cours 40 €. Rendement ?", ["1,2 %", "3 %", "4 %", "33 %"], 1, "1,20 ÷ 40 = 3 %."),
("Une entreprise bat le consensus mais l'action chute. Explication la plus probable ?", ["Une erreur de la bourse", "Des perspectives (guidance) décevantes ou des attentes déjà très élevées", "Le PER est trop bas", "Le dividende a augmenté"], 1, "La guidance et les attentes déjà intégrées dans le cours pèsent souvent plus que le chiffre passé."),
("VIX à 25. Mouvement journalier « typique » attendu sur le S&P 500 ?", ["0,25 %", "1,6 %", "5 %", "25 %"], 1, "25 ÷ √252 ≈ 25 ÷ 15,87 ≈ 1,6 %."),
("« Buy the rumor, sell the news » signifie :", ["Qu'il faut acheter toutes les rumeurs", "Qu'un événement attendu est souvent déjà dans les prix et peut provoquer des prises de bénéfices quand il survient", "Qu'il faut vendre les actualités négatives", "Que les rumeurs sont illégales"], 1, "Ce qui est anticipé est intégré ; l'annonce elle-même peut déclencher des ventes."),
]
