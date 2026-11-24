/* Calculateurs : taille de position, ratio risque/rendement, espérance. */
(function () {
  "use strict";
  function $(id) { return document.getElementById(id); }
  function v(id) { var x = parseFloat(String($(id).value).replace(",", ".")); return isFinite(x) ? x : NaN; }
  function f(x, d) {
    if (!isFinite(x)) return "—";
    if (d == null) d = Math.abs(x) >= 100 ? 0 : 2;
    return x.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d });
  }
  function arrondiBas(x, pas) {
    if (!(pas > 0)) return x;
    var n = Math.floor(x / pas + 1e-9) * pas;
    var dec = (String(pas).split(".")[1] || "").length;
    return parseFloat(n.toFixed(dec));
  }

  /* ---------------- Taille de position ---------------- */
  var type = $("t-type");
  function majChamps() {
    var t = type.value;
    document.querySelectorAll(".t-forex").forEach(function (e) { e.hidden = t !== "forex"; });
    document.querySelectorAll(".t-points").forEach(function (e) { e.hidden = t !== "points"; });
  }
  type.addEventListener("change", function () {
    var t = type.value;
    if (t === "actions") { $("t-entree").value = 50; $("t-stop").value = 48; $("t-pas").value = 1; $("t-levier").value = 1; }
    if (t === "forex") { $("t-entree").value = 1.0850; $("t-stop").value = 1.0820; $("t-pas").value = 0.01; $("t-levier").value = 30; }
    if (t === "points") { $("t-entree").value = 7500; $("t-stop").value = 7460; $("t-pas").value = 1; $("t-vpoint").value = 1; $("t-levier").value = 20; }
    majChamps(); calcTaille();
  });

  function calcTaille() {
    var t = type.value, cap = v("t-capital"), r = v("t-risque"), e = v("t-entree"), s = v("t-stop");
    var frais = v("t-frais") || 0, pas = v("t-pas"), lev = v("t-levier") || 1;
    var out = $("r-taille");
    if (!(cap > 0) || !(r > 0) || !isFinite(e) || !isFinite(s)) { out.innerHTML = "<p>Renseignez le capital, le risque, l'entrée et le stop.</p>"; return; }
    if (e === s) { out.innerHTML = '<p class="alerte">Le stop doit être différent du prix d\'entrée.</p>'; return; }
    var sens = s < e ? "achat (position longue)" : "vente (position courte)";
    var budget = cap * r / 100;
    var budgetNet = budget - frais;
    var dist = Math.abs(e - s);
    var unite, uniteLib, risqueUnite, distLib, notionnelUnite;
    if (t === "actions") {
      risqueUnite = dist; unite = "titre(s)"; uniteLib = "par titre";
      distLib = f(dist, 2) + " € soit " + f(dist / e * 100, 2) + " %";
      notionnelUnite = e;
    } else if (t === "forex") {
      var pip = parseFloat($("t-pip").value), vpip = v("t-vpip");
      var pips = dist / pip;
      risqueUnite = pips * vpip; unite = "lot(s)"; uniteLib = "par lot standard";
      distLib = f(pips, 1) + " pips (" + f(dist, 5) + ")";
      notionnelUnite = 100000 * (vpip / 10); // approx. valeur d'un lot en € (devise de base ≈ EUR si cotation EUR/xxx)
    } else {
      var vpt = v("t-vpoint");
      risqueUnite = dist * vpt; unite = "contrat(s)"; uniteLib = "par contrat";
      distLib = f(dist, 2) + " points";
      notionnelUnite = e * vpt;
    }
    if (!(risqueUnite > 0)) { out.innerHTML = "<p>Vérifiez la valeur du pip ou du point.</p>"; return; }
    if (budgetNet <= 0) { out.innerHTML = '<p class="alerte">Les frais (' + f(frais) + " €) dépassent le budget de risque (" + f(budget) + " €) : le trade n'a pas de sens à cette taille de compte.</p>"; return; }
    var brute = budgetNet / risqueUnite;
    var taille = arrondiBas(brute, pas);
    var risqueReel = taille * risqueUnite + frais;
    var notionnel = taille * notionnelUnite;
    var marge = notionnel / lev;
    var h = "";
    if (taille <= 0) {
      h += '<p class="alerte">Taille arrondie = 0. Même la plus petite taille possible (' + f(pas, 2) + " " + unite + ") ferait risquer " +
        f(pas * risqueUnite + frais) + " € soit " + f((pas * risqueUnite + frais) / cap * 100, 2) + " % du capital. Rapprochez le stop (si c'est justifié techniquement), choisissez un instrument plus petit, ou renoncez au trade.</p>";
    } else {
      h += '<p>Taille de position : <span class="gros">' + f(taille, (String(pas).split(".")[1] || "").length) + " " + unite + "</span> (" + sens + ")</p>";
    }
    h += '<div class="kpis">' +
      '<div class="kpi"><small>Budget de risque</small><b>' + f(budget) + " €</b></div>" +
      '<div class="kpi"><small>Distance au stop</small><b>' + distLib + "</b></div>" +
      '<div class="kpi"><small>Perte si stop touché</small><b>' + f(risqueReel) + " € (" + f(risqueReel / cap * 100, 2) + " %)</b></div>" +
      '<div class="kpi"><small>Valeur exposée (notionnel)</small><b>≈ ' + f(notionnel) + " €</b></div>" +
      '<div class="kpi"><small>Levier effectif</small><b>' + f(notionnel / cap, 2) + "×</b></div>" +
      (lev > 1 ? '<div class="kpi"><small>Marge immobilisée (levier ' + f(lev, 0) + ")</small><b>≈ " + f(marge) + " €</b></div>" : "") +
      "</div>";
    h += '<div class="calcul">1. Budget de risque = ' + f(cap) + " × " + f(r, 2) + " % = " + f(budget) + " €\n" +
      "2. Budget net de frais = " + f(budget) + " − " + f(frais) + " = " + f(budgetNet) + " €\n" +
      "3. Risque " + uniteLib + " = " + (t === "actions" ? f(dist, 2) + " €" : t === "forex" ? f(dist / parseFloat($("t-pip").value), 1) + " pips × " + f(v("t-vpip"), 2) + " € = " + f(risqueUnite) + " €" : f(dist, 2) + " points × " + f(v("t-vpoint"), 2) + " € = " + f(risqueUnite) + " €") + "\n" +
      "4. Taille = " + f(budgetNet) + " ÷ " + f(risqueUnite) + " = " + f(brute, 3) + " → arrondi vers le bas : " + f(taille, 2) + "</div>";
    if (notionnel > cap * 5 && taille > 0) h += '<p class="alerte">Exposition supérieure à 5 fois le capital : un gap au-delà du stop pourrait coûter bien plus que prévu.</p>';
    if (r > 2) h += '<p class="alerte">Un risque supérieur à 2 % par trade rend les séries de pertes très douloureuses (voir le simulateur plus bas).</p>';
    if (t === "forex") h += "<p><small>Le notionnel affiché suppose que la devise de base est l'euro (ex. EUR/USD). Pour d'autres paires, la conversion diffère.</small></p>";
    out.innerHTML = h;
  }
  ["t-capital", "t-risque", "t-entree", "t-stop", "t-frais", "t-pip", "t-vpip", "t-vpoint", "t-pas", "t-levier"].forEach(function (id) {
    $(id).addEventListener("input", calcTaille);
    $(id).addEventListener("change", calcTaille);
  });
  majChamps(); calcTaille();

  /* ---------------- Ratio R/R et espérance ---------------- */
  function calcRR() {
    var e = v("rr-entree"), s = v("rr-stop"), o = v("rr-obj"), w = v("rr-win") / 100, m = v("rr-montant"), fr = v("rr-frais") || 0;
    var out = $("r-rr");
    if (![e, s, o].every(isFinite) || e === s) { out.innerHTML = "<p>Renseignez une entrée, un stop et un objectif différents.</p>"; return; }
    var long = s < e;
    if ((long && o <= e) || (!long && o >= e)) { out.innerHTML = '<p class="alerte">Incohérence : pour un achat, stop sous l\'entrée et objectif au-dessus ; pour une vente, l\'inverse.</p>'; return; }
    var risque = Math.abs(e - s), gain = Math.abs(o - e), R = gain / risque;
    var seuil = 1 / (1 + R);
    var espR = w * R - (1 - w);
    var espE = isFinite(m) ? w * (R * m) - (1 - w) * m - fr : NaN;
    var seuilFrais = isFinite(m) && m > 0 ? (m + fr) / (R * m + m) : NaN;
    var h = '<p>Ratio risque/rendement : <span class="gros">1 : ' + f(R, 2) + "</span> (" + (long ? "achat" : "vente") + ")</p>";
    h += '<div class="kpis">' +
      '<div class="kpi"><small>Risque par unité</small><b>' + f(risque, 2) + "</b></div>" +
      '<div class="kpi"><small>Gain visé par unité</small><b>' + f(gain, 2) + "</b></div>" +
      '<div class="kpi"><small>Taux de réussite minimal (sans frais)</small><b>' + f(seuil * 100, 1) + " %</b></div>" +
      (isFinite(seuilFrais) ? '<div class="kpi"><small>Taux minimal avec frais</small><b>' + f(seuilFrais * 100, 1) + " %</b></div>" : "") +
      '<div class="kpi"><small>Espérance par trade</small><b class="' + (espR >= 0 ? "pos" : "neg") + '">' + (espR >= 0 ? "+" : "") + f(espR, 2) + " R</b></div>" +
      (isFinite(espE) ? '<div class="kpi"><small>Espérance nette en €</small><b class="' + (espE >= 0 ? "pos" : "neg") + '">' + (espE >= 0 ? "+" : "") + f(espE, 2) + " €</b></div>" : "") +
      "</div>";
    h += '<div class="calcul">R = gain visé ÷ risque = ' + f(gain, 2) + " ÷ " + f(risque, 2) + " = " + f(R, 2) + "\n" +
      "Seuil de rentabilité = 1 ÷ (1 + R) = 1 ÷ " + f(1 + R, 2) + " = " + f(seuil * 100, 1) + " %\n" +
      "Espérance = p × R − (1 − p) × 1 = " + f(w, 2) + " × " + f(R, 2) + " − " + f(1 - w, 2) + " = " + f(espR, 3) + " R" +
      (isFinite(espE) ? "\nEn euros : " + f(w, 2) + " × " + f(R * m) + " − " + f(1 - w, 2) + " × " + f(m) + " − " + f(fr) + " (frais) = " + f(espE, 2) + " €" : "") + "</div>";
    h += espR > 0 ? '<p class="ok">Espérance positive… si le taux de réussite saisi est réaliste. C\'est presque toujours lui le point faible.</p>' :
      '<p class="alerte">Espérance négative ou nulle : sur un grand nombre de trades, cette configuration perd de l\'argent.</p>';
    out.innerHTML = h;
  }
  ["rr-entree", "rr-stop", "rr-obj", "rr-win", "rr-montant", "rr-frais"].forEach(function (id) { $(id).addEventListener("input", calcRR); });
  calcRR();

  function calcStats() {
    var n = v("st-n"), g = v("st-g"), mg = v("st-mg"), mp = v("st-mp");
    var out = $("r-stats");
    if (!(n > 0) || !(g >= 0) || g > n || !(mg >= 0) || !(mp > 0)) { out.innerHTML = "<p>Vérifiez les valeurs (le nombre de gagnants ne peut pas dépasser le nombre de trades).</p>"; return; }
    var p = g / n, perdants = n - g;
    var esp = p * mg - (1 - p) * mp;
    var bruts = g * mg, pertes = perdants * mp;
    var pf = pertes > 0 ? bruts / pertes : Infinity;
    var h = '<div class="kpis">' +
      '<div class="kpi"><small>Taux de réussite</small><b>' + f(p * 100, 1) + " %</b></div>" +
      '<div class="kpi"><small>Ratio gain moyen / perte moyenne</small><b>' + f(mg / mp, 2) + "</b></div>" +
      '<div class="kpi"><small>Espérance par trade</small><b class="' + (esp >= 0 ? "pos" : "neg") + '">' + (esp >= 0 ? "+" : "") + f(esp, 2) + " €</b></div>" +
      '<div class="kpi"><small>Profit factor</small><b>' + (isFinite(pf) ? f(pf, 2) : "∞") + "</b></div>" +
      '<div class="kpi"><small>Résultat total</small><b class="' + (bruts - pertes >= 0 ? "pos" : "neg") + '">' + f(bruts - pertes) + " €</b></div>" +
      "</div>";
    h += '<div class="calcul">Taux de réussite p = ' + g + " ÷ " + n + " = " + f(p * 100, 1) + " %\n" +
      "Espérance = p × gain moyen − (1 − p) × perte moyenne = " + f(p, 3) + " × " + f(mg) + " − " + f(1 - p, 3) + " × " + f(mp) + " = " + f(esp, 2) + " €\n" +
      "Profit factor = gains bruts ÷ pertes brutes = " + f(bruts) + " ÷ " + f(pertes) + " = " + (isFinite(pf) ? f(pf, 2) : "∞") + "</div>";
    if (n < 100) h += "<p><small>⚠️ Avec " + n + " trades, ces chiffres sont très incertains : la part de hasard reste importante (voir module 10, taille d'échantillon).</small></p>";
    out.innerHTML = h;
  }
  ["st-n", "st-g", "st-mg", "st-mp"].forEach(function (id) { $(id).addEventListener("input", calcStats); });
  calcStats();
})();
