window.QUIZ = {
"id": "examen",
"titre": "Examen final",
"retour": "index.html",
"questions": [
{
"q": "Un trader réalise 250 allers-retours par an à 12 € l'unité sur un compte de 15 000 €. Quelle part de son capital part en frais ?",
"c": [
"2 %",
"12 %",
"20 %",
"25 %"
],
"a": 2,
"e": "250 × 12 = 3 000 € ; 3 000 ÷ 15 000 = 20 % par an, à gagner avant d'être à l'équilibre.",
"t": "Module 0"
},
{
"q": "Quelle affirmation est conforme aux données des régulateurs européens sur les CFD ?",
"c": [
"Une majorité de particuliers gagne",
"Environ la moitié gagne",
"Une large majorité de comptes de particuliers perd de l'argent",
"Aucune donnée n'existe"
],
"a": 2,
"e": "L'ESMA citait 74 à 89 % de comptes perdants ; les courtiers doivent afficher leur propre pourcentage.",
"t": "Module 0"
},
{
"q": "Une obligation à 10 ans de coupon 3 % : que devient son prix si les taux du marché passent de 3 % à 4 % ?",
"c": [
"Il monte",
"Il baisse",
"Il ne change pas",
"Il double"
],
"a": 1,
"e": "Taux du marché en hausse ⇒ prix des obligations existantes en baisse (environ 918,89 € pour 1 000 € de nominal dans l'exemple du module).",
"t": "Module 1"
},
{
"q": "Vous vendez 10 000 € sur EUR/USD à 1,1000 et rachetez à 1,0960. Résultat ?",
"c": [
"+40 $",
"−40 $",
"+400 $",
"−400 $"
],
"a": 0,
"e": "Vous avez vendu la paire : (1,1000 − 1,0960) × 10 000 = +40 $ (gain en devise de cotation).",
"t": "Module 1"
},
{
"q": "Un ETF à levier 2× quotidien est surtout adapté :",
"c": [
"À une détention de plusieurs années",
"À un usage de court terme, car il s'érode dans les marchés qui oscillent",
"Au PEA uniquement",
"Aux obligations"
],
"a": 1,
"e": "Il réplique 2× la performance quotidienne ; sur plusieurs jours de marché agité, sa performance diverge fortement.",
"t": "Module 1"
},
{
"q": "Une action cote 15,20 / 15,26. Vous achetez puis revendez immédiatement 500 titres. Perte due au spread ?",
"c": [
"3 €",
"30 €",
"60 €",
"300 €"
],
"a": 1,
"e": "Spread = 0,06 € ; 500 × 0,06 = 30 €.",
"t": "Module 2"
},
{
"q": "Quel ordre utiliser pour acheter uniquement si le prix casse une résistance à 52 € (prix actuel 50 €) ?",
"c": [
"Achat à cours limité à 52 €",
"Stop d'achat à 52 €",
"Vente limitée à 52 €",
"Stop de vente à 52 €"
],
"a": 1,
"e": "Un achat au-dessus du prix actuel, déclenché par la hausse, est un stop d'achat. Un achat limité à 52 € serait exécuté immédiatement à 50 €.",
"t": "Module 2"
},
{
"q": "Vous êtes vendeur à découvert de 200 actions à 25 €. L'action ouvre en gap à 29 € et votre stop à 26,50 € est exécuté à l'ouverture. Perte ?",
"c": [
"300 €",
"500 €",
"800 €",
"1 000 €"
],
"a": 2,
"e": "Exécution à 29 € : (29 − 25) × 200 = 800 €, au lieu des 300 € prévus.",
"t": "Module 2"
},
{
"q": "CFD d'actions individuelles pour un particulier européen : marge minimale sur une position de 8 000 € ?",
"c": [
"266,67 €",
"400 €",
"800 €",
"1 600 €"
],
"a": 3,
"e": "Levier maximal 5:1, soit 20 % : 8 000 × 20 % = 1 600 €.",
"t": "Module 3"
},
{
"q": "Capital 4 000 €, exposition 80 000 €. Quel mouvement contraire efface tout le capital ?",
"c": [
"2 %",
"5 %",
"10 %",
"20 %"
],
"a": 1,
"e": "Levier effectif = 20 ; 100 % ÷ 20 = 5 %.",
"t": "Module 3"
},
{
"q": "Put de strike 60 acheté 2,50 € (contrat de 100 actions). À l'échéance, l'action vaut 56 €. Résultat ?",
"c": [
"+150 €",
"+400 €",
"−250 €",
"+650 €"
],
"a": 0,
"e": "Valeur = (60 − 56) × 100 = 400 € ; résultat = 400 − 250 = +150 €.",
"t": "Module 3"
},
{
"q": "0,5 lot d'USD/JPY : combien vaut un pip, en yens ?",
"c": [
"50 ¥",
"500 ¥",
"1 000 ¥",
"5 000 ¥"
],
"a": 1,
"e": "1 lot = 100 000 × 0,01 = 1 000 ¥ par pip ; 0,5 lot = 500 ¥.",
"t": "Module 3"
},
{
"q": "Agrégation de trois bougies horaires (O, H, B, C) : (10 ; 11 ; 9,5 ; 10,8), (10,8 ; 11,4 ; 10,6 ; 11,2), (11,2 ; 11,3 ; 10,2 ; 10,4). Bougie résultante ?",
"c": [
"O 10 ; H 11,4 ; B 9,5 ; C 10,4",
"O 10 ; H 11,3 ; B 10,2 ; C 10,4",
"O 10,4 ; H 11,4 ; B 9,5 ; C 10",
"O 10 ; H 11,4 ; B 10,2 ; C 11,2"
],
"a": 0,
"e": "Première ouverture, plus haut des hauts, plus bas des bas, dernière clôture.",
"t": "Module 4"
},
{
"q": "Une résistance cassée à la hausse, puis retestée par le dessus, est souvent interprétée comme :",
"c": [
"Un nouveau support (inversion des rôles)",
"Une fausse cassure certaine",
"Un signal de vente",
"Sans importance"
],
"a": 0,
"e": "C'est le principe d'inversion des rôles ; ce n'est jamais une certitude.",
"t": "Module 4"
},
{
"q": "Configuration réussie 72 % du temps, gain moyen 0,6R, perte moyenne 1,7R. Espérance ?",
"c": [
"+0,43 R",
"−0,04 R",
"+0,12 R",
"−0,20 R"
],
"a": 1,
"e": "0,72 × 0,6 − 0,28 × 1,7 = 0,432 − 0,476 = −0,044 R : perdante malgré 72 % de réussite.",
"t": "Module 5"
},
{
"q": "Double sommet à 84, creux intermédiaire à 78. Objectif théorique après cassure ?",
"c": [
"72",
"75",
"78",
"90"
],
"a": 0,
"e": "Hauteur = 6 ; objectif = 78 − 6 = 72 (ordre de grandeur, pas une certitude).",
"t": "Module 5"
},
{
"q": "Hausse de 50 à 70. Retracement de 38,2 % ?",
"c": [
"57,64",
"62,36",
"60,00",
"65,28"
],
"a": 1,
"e": "70 − 20 × 0,382 = 70 − 7,64 = 62,36.",
"t": "Module 6"
},
{
"q": "Clôture précédente 30 ; bougie : haut 30,8, bas 28,1. True Range ?",
"c": [
"0,8",
"1,9",
"2,7",
"2,9"
],
"a": 2,
"e": "max(2,7 ; 0,8 ; 1,9) = 2,7.",
"t": "Module 6"
},
{
"q": "Pourquoi utiliser le RSI, le stochastique et le Williams %R ensemble n'apporte presque rien ?",
"c": [
"Ils sont interdits ensemble",
"Ce sont des oscillateurs d'élan calculés sur les mêmes prix, très corrélés",
"Ils mesurent le volume",
"Ils ne fonctionnent que sur le Forex"
],
"a": 1,
"e": "Leur accord est un écho, pas une confirmation indépendante.",
"t": "Module 6"
},
{
"q": "Croissance trimestrielle du PIB de 0,6 %. Croissance annualisée approximative ?",
"c": [
"0,6 %",
"2,4 %",
"2,42 %",
"7,2 %"
],
"a": 2,
"e": "1,006^4 − 1 ≈ 2,42 %.",
"t": "Module 7"
},
{
"q": "Action à 72 €, BPA 4,80 €, dividende 2,16 €. PER et rendement ?",
"c": [
"PER 15 ; rendement 3 %",
"PER 12 ; rendement 2,16 %",
"PER 15 ; rendement 45 %",
"PER 33 ; rendement 3 %"
],
"a": 0,
"e": "72 ÷ 4,80 = 15 ; 2,16 ÷ 72 = 3 %.",
"t": "Module 7"
},
{
"q": "Consensus d'inflation 2,4 %, chiffre publié 2,4 %. Réaction la plus probable des marchés ?",
"c": [
"Forte, car l'inflation est élevée",
"Limitée, car le chiffre était attendu",
"Toujours une hausse des actions",
"Fermeture des marchés"
],
"a": 1,
"e": "Les marchés réagissent surtout à la surprise par rapport aux attentes.",
"t": "Module 7"
},
{
"q": "Objectif 6 pips, stop 6 pips, coût 2 pips. Taux de réussite minimal ?",
"c": [
"50 %",
"60 %",
"66,7 %",
"75 %"
],
"a": 2,
"e": "Gain net 4, perte nette 8 : p = 8 ÷ 12 ≈ 66,7 %.",
"t": "Module 8"
},
{
"q": "Pour une personne qui travaille de 9 h à 18 h et dispose d'une heure le soir, le style le plus compatible est en général :",
"c": [
"Le scalping",
"Le day trading européen",
"Le swing trading",
"Le trading haute fréquence"
],
"a": 2,
"e": "Analyse le soir, ordres placés à l'avance, positions de quelques jours.",
"t": "Module 8"
},
{
"q": "Après une perte de 25 %, quel gain faut-il pour revenir au capital initial ?",
"c": [
"25 %",
"30 %",
"33,3 %",
"50 %"
],
"a": 2,
"e": "0,25 ÷ 0,75 ≈ 33,3 %.",
"t": "Module 9"
},
{
"q": "Capital 18 000 €, risque 1 %, entrée 64,00 €, stop 61,60 €. Taille de position ?",
"c": [
"28 actions",
"75 actions",
"180 actions",
"281 actions"
],
"a": 1,
"e": "Risque 180 € ; distance 2,40 € ; 180 ÷ 2,40 = 75 actions.",
"t": "Module 9"
},
{
"q": "Capital 10 000 €, risque 0,8 %, stop à 25 pips, valeur du pip 9,20 € par lot. Taille (arrondie vers le bas à 0,01 lot) ?",
"c": [
"0,32 lot",
"0,34 lot",
"0,35 lot",
"3,4 lots"
],
"a": 1,
"e": "80 ÷ (25 × 9,20) = 80 ÷ 230 = 0,3478 → 0,34 lot.",
"t": "Module 9"
},
{
"q": "Ratio 1:2,5. Taux de réussite minimal (sans frais) ?",
"c": [
"25 %",
"28,6 %",
"40 %",
"71,4 %"
],
"a": 1,
"e": "1 ÷ (1 + 2,5) = 1 ÷ 3,5 ≈ 28,6 %.",
"t": "Module 9"
},
{
"q": "38 % de réussite, gain moyen 2,2R, perte moyenne 1R, coûts 0,05R par trade. Espérance nette ?",
"c": [
"+0,166 R",
"+0,216 R",
"−0,05 R",
"+0,836 R"
],
"a": 0,
"e": "0,38 × 2,2 − 0,62 × 1 = 0,836 − 0,62 = 0,216 ; − 0,05 = +0,166 R.",
"t": "Module 9"
},
{
"q": "Capital : 8 000 → 9 500 → 8 100 → 10 200 → 8 670. Drawdown maximal ?",
"c": [
"14,7 %",
"15 %",
"17,6 %",
"8,4 %"
],
"a": 1,
"e": "Pic 10 200 → 8 670 : (10 200 − 8 670) ÷ 10 200 = 15 % ; pic 9 500 → 8 100 : 14,7 %. Le maximum est 15 %.",
"t": "Module 9"
},
{
"q": "Deux positions à 1 % de risque, corrélation 0,5. Risque combiné (écart-type) ?",
"c": [
"1 %",
"1,41 %",
"1,73 %",
"2 %"
],
"a": 2,
"e": "√(1 + 1 + 2 × 0,5) = √3 ≈ 1,73 %.",
"t": "Module 9"
},
{
"q": "À espérance identique, passer de 1 % à 3 % de risque par trade :",
"c": [
"Divise le risque de ruine par trois",
"Augmente bien plus que proportionnellement la probabilité de drawdown sévère",
"Ne change rien",
"Triple l'espérance en R"
],
"a": 1,
"e": "Moins de pertes suffisent à creuser un drawdown profond ; l'espérance en R ne change pas.",
"t": "Module 9"
},
{
"q": "Une stratégie affiche un profit factor de 3,5 avec une EMA 23, et de 1,0 avec 21 ou 25. Conclusion ?",
"c": [
"Stratégie robuste",
"Surapprentissage probable",
"Biais du survivant",
"Il faut tripler le risque"
],
"a": 1,
"e": "Une performance qui s'effondre avec des paramètres voisins est le signe d'un ajustement au bruit du passé.",
"t": "Module 10"
},
{
"q": "Écart-type des résultats 1,6R, 64 trades, espérance mesurée +0,3R. Intervalle de confiance à 95 % approximatif ?",
"c": [
"+0,1 à +0,5 R",
"−0,09 à +0,69 R",
"+0,3 à +0,6 R",
"−1,3 à +1,9 R"
],
"a": 1,
"e": "Erreur type = 1,6 ÷ 8 = 0,2 ; 0,3 ± 1,96 × 0,2 = 0,3 ± 0,392.",
"t": "Module 10"
},
{
"q": "Gains bruts 42R, pertes brutes 35R sur 100 trades. Profit factor et espérance ?",
"c": [
"1,2 et +0,07 R",
"0,83 et −0,07 R",
"1,2 et +0,7 R",
"7 et +0,07 R"
],
"a": 0,
"e": "42 ÷ 35 = 1,2 ; (42 − 35) ÷ 100 = +0,07 R par trade.",
"t": "Module 10"
},
{
"q": "Plan : 40 %, +2R / −1R. Réalisé : 48 %, +1,2R / −1,3R. Espérance réalisée ?",
"c": [
"+0,20 R",
"−0,10 R",
"+0,58 R",
"0"
],
"a": 1,
"e": "0,48 × 1,2 − 0,52 × 1,3 = 0,576 − 0,676 = −0,10 R : l'exécution a détruit l'avantage.",
"t": "Module 11"
},
{
"q": "« Je garde cette action perdante jusqu'à ce qu'elle revienne à mon prix d'achat » illustre surtout :",
"c": [
"L'ancrage et l'aversion à la perte",
"Le FOMO",
"La diversification",
"Le surapprentissage"
],
"a": 0,
"e": "Le prix d'achat n'a aucune importance pour le marché ; la décision doit porter sur la situation actuelle.",
"t": "Module 11"
},
{
"q": "Un site propose 4 % de rendement mensuel « garanti », exige un paiement en cryptoactifs et n'apparaît dans aucun registre. Que faire ?",
"c": [
"Tester avec une petite somme",
"Ne rien verser et consulter les listes noires de l'AMF",
"Demander un bonus",
"Payer des frais pour vérifier"
],
"a": 1,
"e": "Rendement garanti élevé, paiement en crypto, absence d'autorisation : signaux d'escroquerie.",
"t": "Module 12"
},
{
"q": "Votre compte démo affiche 100 000 € fictifs alors que vous prévoyez un compte réel de 4 000 €. Que faire ?",
"c": [
"Rien",
"Régler le capital démo à 4 000 € et appliquer le même risque qu'en réel",
"Augmenter le risque en démo",
"Passer directement en réel"
],
"a": 1,
"e": "Sinon les tailles de position et l'apprentissage sont faussés.",
"t": "Module 12"
},
{
"q": "Lequel de ces comptes doit être déclaré comme compte à l'étranger par un résident fiscal français ?",
"c": [
"Un PEA dans une banque française",
"Un compte chez un courtier en CFD établi à Chypre, même fermé dans l'année",
"Un livret A",
"Aucun"
],
"a": 1,
"e": "Tout compte ouvert, détenu, utilisé ou clos à l'étranger dans l'année doit être déclaré, y compris les comptes de cryptoactifs.",
"t": "Module 13"
}
]
};
