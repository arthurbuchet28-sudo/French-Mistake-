window.QUIZ = {
"id": "q10",
"titre": "Quiz du module 10 — Construire une stratégie",
"retour": "../modules/module-10.html",
"questions": [
{
"q": "« Acheter quand le RSI passe sous 30 » est :",
"c": [
"Une stratégie complète",
"Un signal d'entrée, auquel il manque le stop, la sortie, la taille et le contexte",
"Un biais du survivant",
"Un backtest"
],
"a": 1,
"e": "Une stratégie précise aussi le contexte, le stop, la sortie, la taille et la gestion."
},
{
"q": "Une règle est testable si :",
"c": [
"Elle a fonctionné une fois",
"Deux personnes ou un programme prennent toujours les mêmes décisions avec les mêmes données",
"Elle utilise au moins trois indicateurs",
"Elle vient d'un livre"
],
"a": 1,
"e": "Une règle testable ne laisse aucune place à l'interprétation."
},
{
"q": "Espérance brute +0,18R, coûts 0,07R par trade. Espérance nette ?",
"c": [
"+0,25 R",
"+0,11 R",
"+0,07 R",
"−0,11 R"
],
"a": 1,
"e": "0,18 − 0,07 = 0,11 R."
},
{
"q": "Le surapprentissage consiste à :",
"c": [
"Tester sur trop de marchés",
"Ajuster les règles au bruit du passé, au point qu'elles ne fonctionnent plus sur des données nouvelles",
"Utiliser un stop trop large",
"Faire du forward test"
],
"a": 1,
"e": "La stratégie a « appris » le hasard du passé."
},
{
"q": "Tester une stratégie uniquement sur les actions qui composent l'indice aujourd'hui crée :",
"c": [
"Un biais du survivant",
"Un biais de confirmation",
"Un effet de levier",
"Un gap"
],
"a": 0,
"e": "On oublie les sociétés sorties de l'indice ou disparues, souvent après de mauvaises performances."
},
{
"q": "Utiliser la clôture du jour pour décider d'acheter à l'ouverture de ce même jour est :",
"c": [
"Correct",
"Un biais d'anticipation (look-ahead)",
"Un biais du survivant",
"Un ratio de Sharpe"
],
"a": 1,
"e": "La clôture n'était pas connue au moment de l'ouverture."
},
{
"q": "Gains bruts 30R, pertes brutes 20R. Profit factor ?",
"c": [
"0,67",
"1,5",
"10",
"50"
],
"a": 1,
"e": "30 ÷ 20 = 1,5."
},
{
"q": "Une stratégie n'est rentable qu'avec une SMA de 37, pas avec 35 ou 40. C'est un signe de :",
"c": [
"Robustesse",
"Surapprentissage",
"Faible volatilité",
"Bonne diversification"
],
"a": 1,
"e": "Une stratégie robuste résiste à de petites variations de ses paramètres."
},
{
"q": "Écart-type 2R, 100 trades. Erreur type de l'espérance ?",
"c": [
"0,02 R",
"0,2 R",
"2 R",
"20 R"
],
"a": 1,
"e": "2 ÷ √100 = 0,2 R."
},
{
"q": "Pourquoi le forward test est-il nécessaire après un bon backtest ?",
"c": [
"Il n'est pas nécessaire",
"Il révèle l'exécution réelle, la discipline et un éventuel surapprentissage",
"Il remplace la gestion du risque",
"Il garantit les gains"
],
"a": 1,
"e": "Le temps réel montre ce que le backtest ne peut pas montrer."
},
{
"q": "Rendement mensuel moyen 1 %, taux sans risque mensuel 0,25 %, écart-type mensuel 1,5 %. Sharpe annualisé ?",
"c": [
"0,5",
"≈ 1,73",
"6",
"12"
],
"a": 1,
"e": "(1 − 0,25) ÷ 1,5 = 0,5 par mois ; × √12 ≈ 1,73."
},
{
"q": "20 trades, espérance +0,3R, intervalle de confiance de −0,4R à +1,0R. Conclusion ?",
"c": [
"La stratégie est gagnante",
"On ne peut pas encore conclure : il faut plus de trades",
"La stratégie est perdante",
"Il faut doubler le risque"
],
"a": 1,
"e": "L'intervalle contient zéro : le résultat est compatible avec une stratégie sans avantage."
}
]
};
