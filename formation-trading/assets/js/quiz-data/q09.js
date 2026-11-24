window.QUIZ = {
"id": "q09",
"titre": "Quiz du module 9 — Gestion du risque",
"retour": "../modules/module-09.html",
"questions": [
{
"q": "Après une perte de 40 %, quel gain faut-il pour revenir au capital initial ?",
"c": [
"40 %",
"50 %",
"66,7 %",
"80 %"
],
"a": 2,
"e": "0,40 ÷ 0,60 ≈ 66,7 %."
},
{
"q": "Capital 8 000 €, risque 1,5 %. Montant risqué par trade ?",
"c": [
"15 €",
"80 €",
"120 €",
"1 200 €"
],
"a": 2,
"e": "8 000 × 1,5 % = 120 €."
},
{
"q": "Risque 150 €, entrée 30 €, stop 28,50 €. Combien d'actions ?",
"c": [
"50",
"100",
"150",
"200"
],
"a": 1,
"e": "Distance = 1,50 € ; 150 ÷ 1,50 = 100 actions."
},
{
"q": "Risque 100 €, stop à 40 pips, pip à 9 € par lot. Taille en lots (arrondie vers le bas à 0,01) ?",
"c": [
"0,25",
"0,27",
"0,28",
"2,7"
],
"a": 1,
"e": "100 ÷ (40 × 9) = 100 ÷ 360 = 0,277 → 0,27 lot."
},
{
"q": "Où doit se trouver le stop loss ?",
"c": [
"À un montant rond que l'on accepte de perdre",
"Au niveau où l'hypothèse du trade est invalidée",
"Toujours à 1 % sous l'entrée",
"Il n'en faut pas si l'on surveille"
],
"a": 1,
"e": "Le stop est un niveau de marché ; la taille de position s'adapte ensuite."
},
{
"q": "Ratio 1:4. Taux de réussite minimal sans frais ?",
"c": [
"20 %",
"25 %",
"40 %",
"80 %"
],
"a": 0,
"e": "1 ÷ (1 + 4) = 20 %."
},
{
"q": "45 % de réussite, gain moyen 1,8R, perte moyenne 1R. Espérance ?",
"c": [
"−0,04 R",
"+0,26 R",
"+0,81 R",
"+0,45 R"
],
"a": 1,
"e": "0,45 × 1,8 − 0,55 × 1 = 0,81 − 0,55 = +0,26 R."
},
{
"q": "Pic 20 000 €, creux 15 000 €. Drawdown ?",
"c": [
"15 %",
"20 %",
"25 %",
"33 %"
],
"a": 2,
"e": "(20 000 − 15 000) ÷ 20 000 = 25 %."
},
{
"q": "Dans l'exemple précédent, quel gain faut-il depuis le creux pour revenir au pic ?",
"c": [
"25 %",
"30 %",
"33,3 %",
"50 %"
],
"a": 2,
"e": "20 000 ÷ 15 000 − 1 ≈ 33,3 %."
},
{
"q": "Avec 50 % de réussite, probabilité que les 5 prochains trades soient perdants ?",
"c": [
"50 %",
"10 %",
"3,125 %",
"0,5 %"
],
"a": 2,
"e": "0,5^5 = 1 ÷ 32 ≈ 3,125 % ; mais sur 100 trades, une telle série est très probable."
},
{
"q": "Que se passe-t-il quand on double le risque par trade, à espérance égale ?",
"c": [
"Le risque de grosse perte augmente beaucoup plus que proportionnellement",
"Le risque de ruine est divisé par deux",
"L'espérance en R double",
"Rien"
],
"a": 0,
"e": "Moins de pertes suffisent à épuiser le capital : la probabilité de drawdown sévère augmente très vite."
},
{
"q": "Deux positions à 1 % de risque, corrélation 0,8. Risque combiné (écart-type) ?",
"c": [
"1 %",
"1,41 %",
"1,90 %",
"2,8 %"
],
"a": 2,
"e": "√(1 + 1 + 2 × 0,8) = √3,6 ≈ 1,90 %."
},
{
"q": "Acheter EUR/USD et vendre USD/CHF revient surtout à :",
"c": [
"Se couvrir",
"Parier deux fois contre le dollar",
"Être neutre",
"Parier sur le franc suisse uniquement"
],
"a": 1,
"e": "Les deux positions gagnent si le dollar baisse : risque concentré."
},
{
"q": "Après 10 % de drawdown, une règle de protection prudente consiste à :",
"c": [
"Doubler le risque pour se refaire",
"Réduire le risque par trade",
"Supprimer les stops",
"Ouvrir plus de positions"
],
"a": 1,
"e": "Réduire la taille limite les dégâts si la série de pertes continue."
},
{
"q": "Kelly avec p = 0,5 et R = 2 donne :",
"c": [
"10 %",
"25 %",
"50 %",
"0 %"
],
"a": 1,
"e": "f = 0,5 − 0,5 ÷ 2 = 0,25, soit 25 % : bien trop agressif en pratique, d'où l'usage de petites fractions."
}
]
};
