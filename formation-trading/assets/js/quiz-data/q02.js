window.QUIZ = {
"id": "q02",
"titre": "Quiz du module 2 — Fonctionnement d'un ordre",
"retour": "../modules/module-02.html",
"questions": [
{
"q": "Une action cote bid 20,00 / ask 20,04. À quel prix pouvez-vous l'acheter immédiatement ?",
"c": [
"20,00 €",
"20,02 €",
"20,04 €",
"Au prix de clôture de la veille"
],
"a": 2,
"e": "On achète à l'ask (le meilleur prix proposé par les vendeurs) : 20,04 €."
},
{
"q": "Le spread est :",
"c": [
"Une commission fixe du courtier",
"L'écart entre le prix de vente (ask) et le prix d'achat (bid)",
"La variation journalière du prix",
"Le montant de la marge"
],
"a": 1,
"e": "Spread = ask − bid. C'est un coût implicite payé à chaque aller-retour."
},
{
"q": "Un ordre à cours limité d'achat à 30 € sur une action qui cote 32 € :",
"c": [
"Est exécuté immédiatement à 32 €",
"Ne sera exécuté que si le prix descend à 30 € ou moins",
"Devient un ordre au marché",
"Est refusé"
],
"a": 1,
"e": "Un ordre limité garantit le prix (30 € maximum) mais pas l'exécution."
},
{
"q": "Quel ordre garantit le prix mais PAS l'exécution ?",
"c": [
"Ordre au marché",
"Ordre stop",
"Ordre à cours limité",
"Trailing stop"
],
"a": 2,
"e": "L'ordre limité ne sera jamais exécuté à un prix pire que la limite, mais il peut ne pas être exécuté du tout."
},
{
"q": "Vous êtes acheteur. Où placez-vous votre stop loss ?",
"c": [
"Au-dessus du prix actuel (stop d'achat)",
"En dessous du prix actuel (stop de vente)",
"Au prix actuel",
"On ne peut pas en placer"
],
"a": 1,
"e": "Pour protéger un achat, on place un stop de vente sous le prix actuel."
},
{
"q": "Quel est le principal danger d'un stop-limite utilisé comme stop loss ?",
"c": [
"Il coûte plus cher",
"Il peut ne pas être exécuté si le prix chute au-delà de la limite",
"Il est exécuté trop tôt",
"Il ne se déclenche jamais"
],
"a": 1,
"e": "Une fois déclenché, il devient un ordre limité : si le prix saute sous la limite, la position reste ouverte pendant la chute."
},
{
"q": "Un trailing stop de 3 € sur un achat à 50 € : le prix monte à 58 puis redescend. Où est le stop ?",
"c": [
"47 €",
"50 €",
"55 €",
"58 €"
],
"a": 2,
"e": "Il suit le plus haut (58) à 3 € de distance, soit 55 €, et ne redescend pas."
},
{
"q": "Un ordre OCO :",
"c": [
"Ouvre deux positions à la fois",
"Associe deux ordres ; l'exécution de l'un annule l'autre",
"Est un ordre exécuté uniquement à la clôture",
"Garantit le prix de sortie"
],
"a": 1,
"e": "One Cancels the Other : typiquement un objectif et un stop sur la même position."
},
{
"q": "Vous achetez 1 000 actions au marché. Le carnet affiche 600 à 10,00 € et 800 à 10,02 €. Prix moyen ?",
"c": [
"10,000 €",
"10,008 €",
"10,010 €",
"10,020 €"
],
"a": 1,
"e": "600 × 10,00 + 400 × 10,02 = 6 000 + 4 008 = 10 008 € ; 10 008 ÷ 1 000 = 10,008 €."
},
{
"q": "Stop à 47 €, l'action ouvre à 43 € après une mauvaise nouvelle. Le stop (au marché) est exécuté :",
"c": [
"À 47 € exactement",
"Vers 43 € (premier prix disponible)",
"Il est annulé",
"À 50 €"
],
"a": 1,
"e": "Le stop devient un ordre au marché au déclenchement : il est exécuté au premier prix disponible, ici dans le gap."
},
{
"q": "Vente à découvert de 100 actions à 30 €, rachat à 36 €. Résultat brut ?",
"c": [
"+600 €",
"−600 €",
"+360 €",
"−3 600 €"
],
"a": 1,
"e": "(30 − 36) × 100 = −600 € : le prix a monté contre une position courte."
},
{
"q": "Pourquoi la perte d'une vente à découvert est-elle théoriquement illimitée ?",
"c": [
"Parce que les frais sont illimités",
"Parce qu'un prix peut monter sans limite",
"Parce que le courtier peut tout saisir",
"Elle ne l'est pas"
],
"a": 1,
"e": "Le prix d'un actif ne peut pas descendre sous zéro, mais il n'a pas de plafond à la hausse."
}
]
};
