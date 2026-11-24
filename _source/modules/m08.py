from svgkit import plot, table

NUM = 8
TITRE = "Styles de trading"
RESUME = "Scalping, day trading, swing trading, position trading : temps requis, coûts, stress, profil adapté, et un test pour vous situer."
DUREE = "1 h 30"
INTRO = r"""<p>Il n'y a pas de « meilleur » style de trading, seulement des styles plus ou moins adaptés à votre emploi du temps, votre capital, votre tempérament et vos coûts. Ce module compare les quatre grands styles, chiffres à l'appui. Un fil rouge : <strong>plus l'horizon est court, plus les frais pèsent lourd</strong>.</p>"""

_c = [i / 10 for i in range(0, 31)]
SCHEMA_SCALP = plot([{"x": _c, "y": [(5 + c) / 10 * 100 for c in _c], "cls": "g-lb", "label": "Taux de réussite minimal (objectif 5 pips, stop 5 pips)"}],
                    label="Taux de réussite minimal d'un scalping selon le coût par trade", xlabel="Coût total par aller-retour (pips)",
                    yr=(45, 85), yfmt=lambda v: f"{v:.0f} %", xfmt=lambda v: f"{v:g}".replace(".", ","),
                    marks=[{"x": 1.5, "y": 65, "t": "1,5 pip de coût → 65 % requis", "dx": 8, "dy": 16}])

SCHEMA_COUTS = plot([{"x": [1, 2, 3, 4], "y": [30, 10, 3.3, 2], "kind": "bar", "cls": "g-barre-b", "bw": 80}],
                    label="Part de l'objectif de gain absorbée par les coûts selon le style (ordres de grandeur illustratifs)",
                    xr=(0.4, 4.6), yr=(0, 35), xticks=[1, 2, 3, 4], legend=False,
                    xfmt=lambda v: {1: "Scalping", 2: "Day trading", 3: "Swing", 4: "Position"}.get(int(v), ""),
                    yfmt=lambda v: f"{v:.0f} %",
                    texts=[{"x": 1, "y": 31.5, "t": "≈ 30 %", "anchor": "middle"}, {"x": 2, "y": 11.5, "t": "≈ 10 %", "anchor": "middle"},
                           {"x": 3, "y": 4.8, "t": "≈ 3 %", "anchor": "middle"}, {"x": 4, "y": 3.5, "t": "≈ 2 %", "anchor": "middle"}])

TEST = r"""
<form class="autoeval" id="autoeval" onsubmit="return false">
<p><strong>1. Combien de temps pouvez-vous consacrer au trading en semaine, pendant les heures de marché ?</strong></p>
<label><input type="radio" name="a1" value="p"> Quelques minutes par jour, le soir</label><br>
<label><input type="radio" name="a1" value="s"> 30 minutes à 1 heure par jour, hors séance</label><br>
<label><input type="radio" name="a1" value="d"> Plusieurs heures d'affilée, en séance</label>
<p><strong>2. Comment réagissez-vous à une position qui reste ouverte la nuit ?</strong></p>
<label><input type="radio" name="a2" value="d"> Je dors mal : je préfère tout clôturer le soir</label><br>
<label><input type="radio" name="a2" value="s"> Ça me va si le risque est maîtrisé</label><br>
<label><input type="radio" name="a2" value="p"> Aucun problème, même plusieurs semaines</label>
<p><strong>3. Quel nombre de décisions par jour vous paraît supportable ?</strong></p>
<label><input type="radio" name="a3" value="d"> Beaucoup : j'aime l'action</label><br>
<label><input type="radio" name="a3" value="s"> Quelques-unes par semaine</label><br>
<label><input type="radio" name="a3" value="p"> Très peu : je préfère réfléchir longtemps</label>
<p><strong>4. Vos frais de trading sont-ils très bas (spreads serrés, commissions faibles) ?</strong></p>
<label><input type="radio" name="a4" value="d"> Oui, très bas</label><br>
<label><input type="radio" name="a4" value="s"> Corrects</label><br>
<label><input type="radio" name="a4" value="p"> Je ne sais pas / plutôt élevés</label>
<p><strong>5. Votre capital de trading est :</strong></p>
<label><input type="radio" name="a5" value="s"> Inférieur à 5 000 €</label><br>
<label><input type="radio" name="a5" value="s"> Entre 5 000 et 25 000 €</label><br>
<label><input type="radio" name="a5" value="d"> Supérieur à 25 000 €</label>
<div class="actions"><button type="button" class="btn btn-principal" id="autoeval-go">Voir mon profil</button></div>
<div class="resultat" id="autoeval-res" hidden></div>
</form>
<script>
(function () {
  var b = document.getElementById("autoeval-go");
  if (!b) return;
  b.addEventListener("click", function () {
    var sc = { d: 0, s: 0, p: 0 }, n = 0;
    for (var i = 1; i <= 5; i++) {
      var c = document.querySelector('input[name="a' + i + '"]:checked');
      if (c) { sc[c.value]++; n++; }
    }
    var r = document.getElementById("autoeval-res");
    r.hidden = false;
    if (n < 5) { r.innerHTML = "<p>Répondez aux 5 questions.</p>"; return; }
    var best = Object.keys(sc).sort(function (a, b) { return sc[b] - sc[a]; })[0];
    var txt = {
      d: "<p><strong>Profil plutôt « intraday » (day trading).</strong> Attention : c'est le style le plus exigeant en temps, en frais et en discipline, et celui où les statistiques sont les plus défavorables. Si vous débutez, commencez quand même par du swing en démo pour apprendre sans la pression du temps réel.</p>",
      s: "<p><strong>Profil plutôt « swing trading ».</strong> C'est souvent le style le plus compatible avec une activité professionnelle : analyse le soir, ordres placés à l'avance, positions de quelques jours. Restez attentif au risque de gap et aux frais de financement des produits à levier.</p>",
      p: "<p><strong>Profil plutôt « position trading ».</strong> Peu de décisions, horizon de plusieurs semaines ou mois. Privilégiez des produits sans coût de financement élevé (actions, ETF au comptant) et des tailles de position adaptées à des stops plus larges. Vous êtes proche de l'investisseur : comparez honnêtement avec une simple stratégie d'investissement passif.</p>"
    }[best];
    if (document.querySelector('input[name="a4"][value="p"]:checked')) txt += "<p>⚠️ Vos frais semblent élevés ou inconnus : cela pénalise d'abord les styles à horizon court. Calculez-les avant tout (module 3).</p>";
    r.innerHTML = txt + "<p><small>Ce test est indicatif et ne remplace pas votre propre réflexion.</small></p>";
  });
})();
</script>
"""

LECONS = [
("8-1", "Le scalping", r"""
<x-obj><ul><li>Comprendre ce qu'est le scalping et ses contraintes.</li><li>Calculer l'impact des coûts sur le taux de réussite nécessaire.</li></ul></x-obj>
<x-simple>
<p>Le <strong>scalping</strong> consiste à prendre de très nombreux trades de quelques secondes à quelques minutes, pour des gains minuscules (quelques ticks ou pips). L'idée est de cumuler beaucoup de petits gains.</p>
</x-simple>
<x-approfondi>
<p>Contraintes : une exécution très rapide, des coûts extrêmement bas, une concentration totale pendant les séances, et une forte résistance au stress. Le scalping est aussi le terrain de jeu des algorithmes à haute fréquence, contre lesquels un humain a un désavantage de vitesse structurel. Certains courtiers restreignent ou interdisent certaines formes de scalping.</p>
<p>Le problème principal est mathématique : quand l'objectif est de 5 pips et que l'aller-retour coûte 1,5 pip, les coûts représentent 30 % du gain visé.</p>
</x-approfondi>
<x-exemple>
<p>Objectif de 5 pips, stop de 5 pips, coût total (spread + commission) de 1,5 pip par aller-retour.</p>
<div class="calcul">Gain net d'un trade gagnant = 5 − 1,5 = 3,5 pips
Perte nette d'un trade perdant = 5 + 1,5 = 6,5 pips
Taux de réussite minimal p : p × 3,5 = (1 − p) × 6,5 → p = 6,5 ÷ (3,5 + 6,5) = 65 %
Sans coûts, il suffirait de 50 %.</div>
</x-exemple>
<x-fig c="Plus le coût par trade est élevé par rapport à l'objectif, plus le taux de réussite nécessaire grimpe.">""" + SCHEMA_SCALP + r"""</x-fig>
<x-erreurs><ul><li>Commencer par le scalping parce qu'il donne « beaucoup d'action ».</li><li>Sous-estimer le slippage, qui se cumule sur des centaines de trades.</li><li>Scalper pendant les publications économiques.</li></ul></x-erreurs>
<x-cles><ul><li>Très nombreux trades très courts, petits objectifs.</li><li>Les coûts représentent une part énorme de l'objectif.</li><li>Style le plus difficile pour un particulier ; déconseillé aux débutants.</li></ul></x-cles>
<x-exo><p>Objectif 8 pips, stop 6 pips, coût 1 pip. Calculez le taux de réussite minimal.</p>
<x-corr><div class="calcul">Gain net = 8 − 1 = 7 ; perte nette = 6 + 1 = 7
p = 7 ÷ (7 + 7) = 50 %</div><p>Sans coût, il aurait suffi de 6 ÷ (8 + 6) ≈ 42,9 %.</p></x-corr></x-exo>
"""),

("8-2", "Le day trading", r"""
<x-obj><ul><li>Comprendre les caractéristiques du day trading.</li><li>Mesurer l'effort et les coûts sur une année.</li></ul></x-obj>
<x-simple>
<p>Le <strong>day trading</strong> (trading intraday) consiste à ouvrir et fermer ses positions dans la même journée. Aucune position n'est conservée la nuit : pas de risque de gap ni de frais de financement overnight. En contrepartie, il faut être disponible pendant les heures de marché.</p>
</x-simple>
<x-approfondi>
<p>Les day traders travaillent souvent sur des unités de temps de 1 à 15 minutes, autour des moments actifs : ouverture, chevauchement des sessions, publications. Ils utilisent volontiers le VWAP, les niveaux de la veille, les plus hauts et plus bas de la première heure. C'est un style qui demande une routine stricte et des limites de perte journalières (module 9).</p>
<p>Rappel des statistiques (module 0) : les études sur les day traders particuliers montrent des taux d'échec très élevés chez ceux qui persistent.</p>
</x-approfondi>
<x-exemple>
<p>3 trades par jour, 250 jours par an, risque de 0,5 % par trade, coûts moyens de 0,05R par trade (un vingtième du risque).</p>
<div class="calcul">Nombre de trades par an = 3 × 250 = 750
Coût annuel en R = 750 × 0,05 = 37,5 R
Avec 0,5 % de risque par R : 37,5 × 0,5 % ≈ 18,75 % du capital par an en frais
(approximation qui ignore la capitalisation)
Il faut donc une espérance brute d'au moins 0,05R par trade, juste pour être à l'équilibre.</div>
<p>Et le temps : 4 heures par jour × 250 jours = 1 000 heures par an, l'équivalent d'un mi-temps.</p>
</x-exemple>
<x-erreurs><ul><li>Faire du day trading pendant ses heures de travail, par à-coups, sur son téléphone.</li><li>Se sentir obligé de trader chaque jour.</li><li>Ne pas fixer de perte maximale journalière.</li></ul></x-erreurs>
<x-cles><ul><li>Positions ouvertes et fermées dans la journée : pas de gap de nuit.</li><li>Exige du temps, une routine et des coûts bas.</li><li>Les frais cumulés sont considérables.</li></ul></x-cles>
<x-exo><p>2 trades par jour, 200 jours par an, coût moyen de 6 € par trade, sur un compte de 8 000 €. Quel pourcentage du capital part en frais ?</p>
<x-corr><div class="calcul">Trades = 2 × 200 = 400
Coûts = 400 × 6 = 2 400 €
En % = 2 400 ÷ 8 000 = 30 %</div></x-corr></x-exo>
"""),

("8-3", "Le swing trading", r"""
<x-obj><ul><li>Comprendre le swing trading et sa compatibilité avec une activité professionnelle.</li><li>Intégrer le coût de financement et le risque de gap.</li></ul></x-obj>
<x-simple>
<p>Le <strong>swing trading</strong> vise à capter des mouvements de quelques jours à quelques semaines, souvent un « swing » (une oscillation) à l'intérieur d'une tendance. L'analyse se fait sur graphiques journaliers ou 4 heures, souvent le soir, et les ordres (entrée, stop, objectif) sont placés à l'avance.</p>
</x-simple>
<x-approfondi>
<p>Avantages : moins de temps d'écran, moins de trades donc moins de frais, des décisions prises « à froid ». Inconvénients : risque de gap de nuit et de week-end, coûts de financement sur les produits à levier, et des stops plus larges, donc des positions plus petites pour un même risque. C'est souvent le style recommandé pour apprendre, car il laisse le temps de réfléchir.</p>
</x-approfondi>
<x-exemple>
<p>CFD d'une valeur de 10 000 €, conservé 5 nuits, avec un financement de 6 % par an (illustratif).</p>
<div class="calcul">Financement = 10 000 × 6 % × 5 ÷ 365 ≈ 8,22 €
Objectif du trade : +3 % = 300 € ; coût d'entrée et de sortie (spread) : 10 €
Coûts totaux ≈ 18,22 €, soit environ 6 % de l'objectif</div>
<p>C'est raisonnable, à condition de ne pas transformer le trade en position de plusieurs mois.</p>
</x-exemple>
<x-erreurs><ul><li>Regarder les positions toutes les cinq minutes « au cas où » : cela annule l'intérêt du style.</li><li>Oublier les publications de résultats pendant la détention.</li><li>Laisser un swing perdant devenir un « investissement à long terme ».</li></ul></x-erreurs>
<x-cles><ul><li>Positions de quelques jours à quelques semaines, analyse en fin de journée.</li><li>Compatible avec un emploi ; bon style pour apprendre.</li><li>Risques : gaps, financement ; positions plus petites car stops plus larges.</li></ul></x-cles>
<x-exo><p>Vous gardez un CFD de 15 000 € pendant 12 nuits à 5,5 % par an. Quel est le coût du financement ? Si votre objectif est de 2,5 %, quelle part de l'objectif représente-t-il ?</p>
<x-corr><div class="calcul">Financement = 15 000 × 5,5 % × 12 ÷ 365 ≈ 27,12 €
Objectif = 15 000 × 2,5 % = 375 €
Part = 27,12 ÷ 375 ≈ 7,2 %</div></x-corr></x-exo>
"""),

("8-4", "Le position trading", r"""
<x-obj><ul><li>Comprendre le position trading et sa frontière avec l'investissement.</li><li>Choisir des produits adaptés à une détention longue.</li></ul></x-obj>
<x-simple>
<p>Le <strong>position trading</strong> vise des mouvements de plusieurs semaines à plusieurs mois, en suivant les grandes tendances (souvent sur graphiques journaliers et hebdomadaires), parfois en combinant analyse technique et fondamentale. Il demande très peu de temps, mais beaucoup de patience et des stops larges.</p>
</x-simple>
<x-approfondi>
<p>Les produits à financement quotidien (CFD) deviennent coûteux sur ces durées : on privilégie le comptant (actions, ETF), éventuellement les futures. Ce style est le plus proche de l'investissement : il est utile de comparer honnêtement ses résultats avec une stratégie passive (acheter et conserver un ETF), qui demande encore moins d'effort.</p>
<p>Le suivi de tendance sur longue période fait partie des approches les mieux documentées dans la recherche (sur les contrats à terme diversifiés), avec de longues périodes sans gains et des drawdowns importants.</p>
</x-approfondi>
<x-exemple>
<p>Position de 10 000 € gardée 90 jours.</p>
<div class="calcul">En CFD à 6 % par an : 10 000 × 6 % × 90 ÷ 365 ≈ 147,95 €
Au comptant (action) : pas de financement ; frais d'achat et de vente, par exemple 2 × 0,1 % = 20 €
Écart ≈ 128 € en faveur du comptant, soit 1,3 % de la position</div>
</x-exemple>
<x-erreurs><ul><li>Utiliser des CFD pour des positions de plusieurs mois.</li><li>Placer des stops trop serrés pour l'horizon choisi.</li><li>Abandonner après quelques mois sans tendance, alors que c'est le fonctionnement normal du style.</li></ul></x-erreurs>
<x-cles><ul><li>Horizon de semaines à mois ; peu de temps, beaucoup de patience.</li><li>Privilégier le comptant ; éviter le financement quotidien.</li><li>Comparer avec une stratégie passive.</li></ul></x-cles>
<x-exo><p>Vous visez une tendance de 4 mois (120 jours) sur un indice, exposition 20 000 €. Comparez un CFD à 5 % de financement annuel et un ETF au comptant avec 0,15 % de frais à l'achat et à la vente.</p>
<x-corr><div class="calcul">CFD : 20 000 × 5 % × 120 ÷ 365 ≈ 328,77 €
ETF : 20 000 × 0,15 % × 2 = 60 € (+ frais de gestion de l'ETF, faibles sur 4 mois)
Écart ≈ 269 € en faveur de l'ETF</div></x-corr></x-exo>
"""),

("8-5", "Comparer les styles et choisir le sien", r"""
<x-obj><ul><li>Comparer les styles sur des critères objectifs.</li><li>Identifier le style compatible avec votre situation.</li></ul></x-obj>
<x-simple>
<p>Le bon style est celui que vous pouvez appliquer <strong>avec régularité et discipline</strong>, compte tenu de votre emploi du temps, de votre capital, de vos coûts et de votre tempérament. Un style mal adapté conduit presque toujours à enfreindre ses règles.</p>
</x-simple>
<x-approfondi>
""" + table(["", "Scalping", "Day trading", "Swing", "Position"],
            [["Durée d'un trade", "Secondes à minutes", "Minutes à heures", "Jours à semaines", "Semaines à mois"],
             ["Trades par an (ordre de grandeur)", "Milliers", "Centaines", "Dizaines à ~100", "Quelques dizaines"],
             ["Temps d'écran", "Très élevé, en séance", "Élevé, en séance", "Faible, hors séance", "Très faible"],
             ["Poids des frais", "Très élevé", "Élevé", "Modéré", "Faible"],
             ["Risque de gap", "Nul", "Nul", "Présent", "Présent"],
             ["Stress", "Très élevé", "Élevé", "Modéré", "Faible (mais patience)"],
             ["Pour débuter", "Déconseillé", "Difficile", "Adapté", "Adapté"]]) + r"""
</x-approfondi>
<x-fig c="Ordres de grandeur, tirés des exemples de ce module : part de l'objectif de gain absorbée par les coûts. Ils varient beaucoup selon le marché et le courtier.">""" + SCHEMA_COUTS + r"""</x-fig>
<x-exemple>
<p>Sophie travaille de 9 h à 18 h et dispose d'environ 45 minutes chaque soir. Son capital de trading est de 6 000 €.</p>
<div class="calcul">Disponibilité en séance (Europe 9 h – 17 h 30) : nulle → scalping et day trading européen exclus
Day trading sur la séance américaine (15 h 30 – 22 h) : seulement en soirée, fatigue, partiel → déconseillé
Swing : analyse le soir (45 min), ordres placés à l'avance → compatible
Risque de 1 % par trade = 60 € ; avec des stops journaliers plus larges, les positions seront petites
→ instruments avec des tailles minimales faibles (actions au comptant, micro-contrats, CFD de petite taille)</div>
</x-exemple>
<x-erreurs><ul><li>Choisir un style pour son image (« le scalper qui vit devant six écrans »).</li><li>Changer de style après chaque série de pertes.</li><li>Mélanger les styles sur une même position (entrer en day trading, rester en swing parce que ça perd).</li></ul></x-erreurs>
<x-cles><ul><li>Plus l'horizon est court, plus les frais et le stress sont élevés.</li><li>Le swing et le position trading sont les plus compatibles avec un emploi.</li><li>Un style = des règles cohérentes ; ne pas changer de style en cours de trade.</li></ul></x-cles>
<x-exo><p>Faites le test d'auto-évaluation ci-dessous, puis écrivez en trois lignes : votre style, vos horaires d'analyse, et ce que vous n'êtes pas prêt à faire (par exemple : « pas de position pendant les résultats d'entreprise »).</p>
""" + TEST + r"""
<x-corr><p>Il n'y a pas de correction unique. Exemple : « Swing trading sur actions européennes et indices. Analyse du lundi au jeudi de 20 h 30 à 21 h 15, ordres placés pour le lendemain. Pas de position pendant une publication de résultats, pas de trade décidé en séance. »</p></x-corr></x-exo>
"""),
]

FICHE = r"""
<div class="encadre"><h2>Scalping</h2><ul><li>Secondes à minutes, milliers de trades.</li><li>Coûts énormes par rapport à l'objectif.</li><li>Seuil de réussite = (stop + coût) ÷ (objectif + stop).</li><li>Déconseillé aux débutants.</li></ul></div>
<div class="encadre"><h2>Day trading</h2><ul><li>Clôture le jour même : pas de gap de nuit.</li><li>Temps en séance, routine, limite de perte journalière.</li><li>Frais cumulés importants.</li></ul></div>
<div class="encadre"><h2>Swing trading</h2><ul><li>Jours à semaines ; analyse le soir.</li><li>Compatible avec un emploi ; bon pour apprendre.</li><li>Gaps, financement ≈ notionnel × taux × nuits ÷ 365.</li></ul></div>
<div class="encadre"><h2>Position trading</h2><ul><li>Semaines à mois ; stops larges.</li><li>Comptant plutôt que CFD.</li><li>Comparer avec une stratégie passive.</li></ul></div>
<div class="encadre"><h2>Choisir</h2><ul><li>Emploi du temps, capital, coûts, tempérament.</li><li>Ne jamais changer de style en cours de trade.</li></ul></div>
"""

QUIZ = [
("Quel style conserve des positions de quelques jours à quelques semaines ?", ["Scalping", "Day trading", "Swing trading", "Arbitrage haute fréquence"], 2, "C'est la définition du swing trading."),
("Objectif 4 pips, stop 4 pips, coût 1 pip. Taux de réussite minimal ?", ["50 %", "55,6 %", "62,5 %", "75 %"], 2, "Gain net 3, perte nette 5 : p = 5 ÷ (3 + 5) = 62,5 %."),
("Avantage principal du day trading par rapport au swing :", ["Moins de frais", "Pas de risque de gap de nuit ni de financement overnight", "Moins de temps d'écran", "Plus de levier"], 1, "Les positions sont fermées le soir."),
("Quel style est généralement le plus compatible avec un emploi à temps plein ?", ["Scalping", "Day trading", "Swing trading", "Aucun"], 2, "Analyse le soir et ordres placés à l'avance."),
("CFD de 8 000 € conservé 10 nuits à 7,3 % par an. Financement ?", ["1,60 €", "16 €", "58,40 €", "160 €"], 1, "8 000 × 7,3 % × 10 ÷ 365 = 16 €."),
("Pour une détention de plusieurs mois, on privilégie plutôt :", ["Des CFD", "Le comptant (actions, ETF) ou les futures", "Des options à très court terme", "Le scalping"], 1, "Le financement quotidien des CFD devient coûteux sur de longues durées."),
("Pourquoi le poids des frais augmente-t-il quand l'horizon raccourcit ?", ["Parce que les courtiers facturent plus cher le matin", "Parce que les objectifs de gain sont plus petits alors que les coûts par trade restent similaires", "Parce qu'il y a moins de liquidité", "Ce n'est pas le cas"], 1, "Le spread et la commission sont à peu près fixes par trade ; l'objectif, lui, est beaucoup plus petit."),
("Une position de day trading perd en fin de journée. Le trader la garde « en swing ». C'est :", ["Une bonne adaptation", "Une erreur classique : changer de style pour éviter d'encaisser une perte", "Obligatoire", "Sans conséquence"], 1, "Les règles du trade (stop, horizon) ont été conçues pour un style ; en changer en cours de route est une façon de fuir la perte."),
("200 trades par an à 5 € de frais sur un compte de 4 000 €. Frais en % du capital ?", ["5 %", "12,5 %", "25 %", "50 %"], 2, "200 × 5 = 1 000 € ; 1 000 ÷ 4 000 = 25 %."),
("Quel style est généralement déconseillé aux débutants ?", ["Le swing trading", "Le position trading", "Le scalping", "L'investissement passif"], 2, "Coûts, vitesse, stress et concurrence des algorithmes rendent le scalping particulièrement difficile."),
]
