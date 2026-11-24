"""Examen final : 40 questions couvrant toute la formation (thème = module)."""

def M(n):
    return f"Module {n}"

QUESTIONS = [
# Module 0
("Un trader réalise 250 allers-retours par an à 12 € l'unité sur un compte de 15 000 €. Quelle part de son capital part en frais ?", ["2 %", "12 %", "20 %", "25 %"], 2, "250 × 12 = 3 000 € ; 3 000 ÷ 15 000 = 20 % par an, à gagner avant d'être à l'équilibre.", M(0)),
("Quelle affirmation est conforme aux données des régulateurs européens sur les CFD ?", ["Une majorité de particuliers gagne", "Environ la moitié gagne", "Une large majorité de comptes de particuliers perd de l'argent", "Aucune donnée n'existe"], 2, "L'ESMA citait 74 à 89 % de comptes perdants ; les courtiers doivent afficher leur propre pourcentage.", M(0)),
# Module 1
("Une obligation à 10 ans de coupon 3 % : que devient son prix si les taux du marché passent de 3 % à 4 % ?", ["Il monte", "Il baisse", "Il ne change pas", "Il double"], 1, "Taux du marché en hausse ⇒ prix des obligations existantes en baisse (environ 918,89 € pour 1 000 € de nominal dans l'exemple du module).", M(1)),
("Vous vendez 10 000 € sur EUR/USD à 1,1000 et rachetez à 1,0960. Résultat ?", ["+40 $", "−40 $", "+400 $", "−400 $"], 0, "Vous avez vendu la paire : (1,1000 − 1,0960) × 10 000 = +40 $ (gain en devise de cotation).", M(1)),
("Un ETF à levier 2× quotidien est surtout adapté :", ["À une détention de plusieurs années", "À un usage de court terme, car il s'érode dans les marchés qui oscillent", "Au PEA uniquement", "Aux obligations"], 1, "Il réplique 2× la performance quotidienne ; sur plusieurs jours de marché agité, sa performance diverge fortement.", M(1)),
# Module 2
("Une action cote 15,20 / 15,26. Vous achetez puis revendez immédiatement 500 titres. Perte due au spread ?", ["3 €", "30 €", "60 €", "300 €"], 1, "Spread = 0,06 € ; 500 × 0,06 = 30 €.", M(2)),
("Quel ordre utiliser pour acheter uniquement si le prix casse une résistance à 52 € (prix actuel 50 €) ?", ["Achat à cours limité à 52 €", "Stop d'achat à 52 €", "Vente limitée à 52 €", "Stop de vente à 52 €"], 1, "Un achat au-dessus du prix actuel, déclenché par la hausse, est un stop d'achat. Un achat limité à 52 € serait exécuté immédiatement à 50 €.", M(2)),
("Vous êtes vendeur à découvert de 200 actions à 25 €. L'action ouvre en gap à 29 € et votre stop à 26,50 € est exécuté à l'ouverture. Perte ?", ["300 €", "500 €", "800 €", "1 000 €"], 2, "Exécution à 29 € : (29 − 25) × 200 = 800 €, au lieu des 300 € prévus.", M(2)),
# Module 3
("CFD d'actions individuelles pour un particulier européen : marge minimale sur une position de 8 000 € ?", ["266,67 €", "400 €", "800 €", "1 600 €"], 3, "Levier maximal 5:1, soit 20 % : 8 000 × 20 % = 1 600 €.", M(3)),
("Capital 4 000 €, exposition 80 000 €. Quel mouvement contraire efface tout le capital ?", ["2 %", "5 %", "10 %", "20 %"], 1, "Levier effectif = 20 ; 100 % ÷ 20 = 5 %.", M(3)),
("Put de strike 60 acheté 2,50 € (contrat de 100 actions). À l'échéance, l'action vaut 56 €. Résultat ?", ["+150 €", "+400 €", "−250 €", "+650 €"], 0, "Valeur = (60 − 56) × 100 = 400 € ; résultat = 400 − 250 = +150 €.", M(3)),
("0,5 lot d'USD/JPY : combien vaut un pip, en yens ?", ["50 ¥", "500 ¥", "1 000 ¥", "5 000 ¥"], 1, "1 lot = 100 000 × 0,01 = 1 000 ¥ par pip ; 0,5 lot = 500 ¥.", M(3)),
# Module 4
("Agrégation de trois bougies horaires (O, H, B, C) : (10 ; 11 ; 9,5 ; 10,8), (10,8 ; 11,4 ; 10,6 ; 11,2), (11,2 ; 11,3 ; 10,2 ; 10,4). Bougie résultante ?", ["O 10 ; H 11,4 ; B 9,5 ; C 10,4", "O 10 ; H 11,3 ; B 10,2 ; C 10,4", "O 10,4 ; H 11,4 ; B 9,5 ; C 10", "O 10 ; H 11,4 ; B 10,2 ; C 11,2"], 0, "Première ouverture, plus haut des hauts, plus bas des bas, dernière clôture.", M(4)),
("Une résistance cassée à la hausse, puis retestée par le dessus, est souvent interprétée comme :", ["Un nouveau support (inversion des rôles)", "Une fausse cassure certaine", "Un signal de vente", "Sans importance"], 0, "C'est le principe d'inversion des rôles ; ce n'est jamais une certitude.", M(4)),
# Module 5
("Configuration réussie 72 % du temps, gain moyen 0,6R, perte moyenne 1,7R. Espérance ?", ["+0,43 R", "−0,04 R", "+0,12 R", "−0,20 R"], 1, "0,72 × 0,6 − 0,28 × 1,7 = 0,432 − 0,476 = −0,044 R : perdante malgré 72 % de réussite.", M(5)),
("Double sommet à 84, creux intermédiaire à 78. Objectif théorique après cassure ?", ["72", "75", "78", "90"], 0, "Hauteur = 6 ; objectif = 78 − 6 = 72 (ordre de grandeur, pas une certitude).", M(5)),
# Module 6
("Hausse de 50 à 70. Retracement de 38,2 % ?", ["57,64", "62,36", "60,00", "65,28"], 1, "70 − 20 × 0,382 = 70 − 7,64 = 62,36.", M(6)),
("Clôture précédente 30 ; bougie : haut 30,8, bas 28,1. True Range ?", ["0,8", "1,9", "2,7", "2,9"], 2, "max(2,7 ; 0,8 ; 1,9) = 2,7.", M(6)),
("Pourquoi utiliser le RSI, le stochastique et le Williams %R ensemble n'apporte presque rien ?", ["Ils sont interdits ensemble", "Ce sont des oscillateurs d'élan calculés sur les mêmes prix, très corrélés", "Ils mesurent le volume", "Ils ne fonctionnent que sur le Forex"], 1, "Leur accord est un écho, pas une confirmation indépendante.", M(6)),
# Module 7
("Croissance trimestrielle du PIB de 0,6 %. Croissance annualisée approximative ?", ["0,6 %", "2,4 %", "2,42 %", "7,2 %"], 2, "1,006^4 − 1 ≈ 2,42 %.", M(7)),
("Action à 72 €, BPA 4,80 €, dividende 2,16 €. PER et rendement ?", ["PER 15 ; rendement 3 %", "PER 12 ; rendement 2,16 %", "PER 15 ; rendement 45 %", "PER 33 ; rendement 3 %"], 0, "72 ÷ 4,80 = 15 ; 2,16 ÷ 72 = 3 %.", M(7)),
("Consensus d'inflation 2,4 %, chiffre publié 2,4 %. Réaction la plus probable des marchés ?", ["Forte, car l'inflation est élevée", "Limitée, car le chiffre était attendu", "Toujours une hausse des actions", "Fermeture des marchés"], 1, "Les marchés réagissent surtout à la surprise par rapport aux attentes.", M(7)),
# Module 8
("Objectif 6 pips, stop 6 pips, coût 2 pips. Taux de réussite minimal ?", ["50 %", "60 %", "66,7 %", "75 %"], 2, "Gain net 4, perte nette 8 : p = 8 ÷ 12 ≈ 66,7 %.", M(8)),
("Pour une personne qui travaille de 9 h à 18 h et dispose d'une heure le soir, le style le plus compatible est en général :", ["Le scalping", "Le day trading européen", "Le swing trading", "Le trading haute fréquence"], 2, "Analyse le soir, ordres placés à l'avance, positions de quelques jours.", M(8)),
# Module 9
("Après une perte de 25 %, quel gain faut-il pour revenir au capital initial ?", ["25 %", "30 %", "33,3 %", "50 %"], 2, "0,25 ÷ 0,75 ≈ 33,3 %.", M(9)),
("Capital 18 000 €, risque 1 %, entrée 64,00 €, stop 61,60 €. Taille de position ?", ["28 actions", "75 actions", "180 actions", "281 actions"], 1, "Risque 180 € ; distance 2,40 € ; 180 ÷ 2,40 = 75 actions.", M(9)),
("Capital 10 000 €, risque 0,8 %, stop à 25 pips, valeur du pip 9,20 € par lot. Taille (arrondie vers le bas à 0,01 lot) ?", ["0,32 lot", "0,34 lot", "0,35 lot", "3,4 lots"], 1, "80 ÷ (25 × 9,20) = 80 ÷ 230 = 0,3478 → 0,34 lot.", M(9)),
("Ratio 1:2,5. Taux de réussite minimal (sans frais) ?", ["25 %", "28,6 %", "40 %", "71,4 %"], 1, "1 ÷ (1 + 2,5) = 1 ÷ 3,5 ≈ 28,6 %.", M(9)),
("38 % de réussite, gain moyen 2,2R, perte moyenne 1R, coûts 0,05R par trade. Espérance nette ?", ["+0,166 R", "+0,216 R", "−0,05 R", "+0,836 R"], 0, "0,38 × 2,2 − 0,62 × 1 = 0,836 − 0,62 = 0,216 ; − 0,05 = +0,166 R.", M(9)),
("Capital : 8 000 → 9 500 → 8 100 → 10 200 → 8 670. Drawdown maximal ?", ["14,7 %", "15 %", "17,6 %", "8,4 %"], 1, "Pic 10 200 → 8 670 : (10 200 − 8 670) ÷ 10 200 = 15 % ; pic 9 500 → 8 100 : 14,7 %. Le maximum est 15 %.", M(9)),
("Deux positions à 1 % de risque, corrélation 0,5. Risque combiné (écart-type) ?", ["1 %", "1,41 %", "1,73 %", "2 %"], 2, "√(1 + 1 + 2 × 0,5) = √3 ≈ 1,73 %.", M(9)),
("À espérance identique, passer de 1 % à 3 % de risque par trade :", ["Divise le risque de ruine par trois", "Augmente bien plus que proportionnellement la probabilité de drawdown sévère", "Ne change rien", "Triple l'espérance en R"], 1, "Moins de pertes suffisent à creuser un drawdown profond ; l'espérance en R ne change pas.", M(9)),
# Module 10
("Une stratégie affiche un profit factor de 3,5 avec une EMA 23, et de 1,0 avec 21 ou 25. Conclusion ?", ["Stratégie robuste", "Surapprentissage probable", "Biais du survivant", "Il faut tripler le risque"], 1, "Une performance qui s'effondre avec des paramètres voisins est le signe d'un ajustement au bruit du passé.", M(10)),
("Écart-type des résultats 1,6R, 64 trades, espérance mesurée +0,3R. Intervalle de confiance à 95 % approximatif ?", ["+0,1 à +0,5 R", "−0,09 à +0,69 R", "+0,3 à +0,6 R", "−1,3 à +1,9 R"], 1, "Erreur type = 1,6 ÷ 8 = 0,2 ; 0,3 ± 1,96 × 0,2 = 0,3 ± 0,392.", M(10)),
("Gains bruts 42R, pertes brutes 35R sur 100 trades. Profit factor et espérance ?", ["1,2 et +0,07 R", "0,83 et −0,07 R", "1,2 et +0,7 R", "7 et +0,07 R"], 0, "42 ÷ 35 = 1,2 ; (42 − 35) ÷ 100 = +0,07 R par trade.", M(10)),
# Module 11
("Plan : 40 %, +2R / −1R. Réalisé : 48 %, +1,2R / −1,3R. Espérance réalisée ?", ["+0,20 R", "−0,10 R", "+0,58 R", "0"], 1, "0,48 × 1,2 − 0,52 × 1,3 = 0,576 − 0,676 = −0,10 R : l'exécution a détruit l'avantage.", M(11)),
("« Je garde cette action perdante jusqu'à ce qu'elle revienne à mon prix d'achat » illustre surtout :", ["L'ancrage et l'aversion à la perte", "Le FOMO", "La diversification", "Le surapprentissage"], 0, "Le prix d'achat n'a aucune importance pour le marché ; la décision doit porter sur la situation actuelle.", M(11)),
# Module 12
("Un site propose 4 % de rendement mensuel « garanti », exige un paiement en cryptoactifs et n'apparaît dans aucun registre. Que faire ?", ["Tester avec une petite somme", "Ne rien verser et consulter les listes noires de l'AMF", "Demander un bonus", "Payer des frais pour vérifier"], 1, "Rendement garanti élevé, paiement en crypto, absence d'autorisation : signaux d'escroquerie.", M(12)),
("Votre compte démo affiche 100 000 € fictifs alors que vous prévoyez un compte réel de 4 000 €. Que faire ?", ["Rien", "Régler le capital démo à 4 000 € et appliquer le même risque qu'en réel", "Augmenter le risque en démo", "Passer directement en réel"], 1, "Sinon les tailles de position et l'apprentissage sont faussés.", M(12)),
# Module 13
("Lequel de ces comptes doit être déclaré comme compte à l'étranger par un résident fiscal français ?", ["Un PEA dans une banque française", "Un compte chez un courtier en CFD établi à Chypre, même fermé dans l'année", "Un livret A", "Aucun"], 1, "Tout compte ouvert, détenu, utilisé ou clos à l'étranger dans l'année doit être déclaré, y compris les comptes de cryptoactifs.", M(13)),
]
