/* Journal de trading interactif : saisie, statistiques, export CSV. Stockage local protégé par try/catch. */
(function () {
  "use strict";
  var CLE = "ft-journal-v1";
  var memoire = [];
  function $(id) { return document.getElementById(id); }
  function lire() {
    try { var b = localStorage.getItem(CLE); if (b) return JSON.parse(b); } catch (e) {}
    return memoire;
  }
  function ecrire(t) {
    memoire = t;
    try { localStorage.setItem(CLE, JSON.stringify(t)); } catch (e) { $("j-avert").hidden = false; }
  }
  try { localStorage.setItem("__t", "1"); localStorage.removeItem("__t"); } catch (e) { $("j-avert").hidden = false; }

  function f(x, d) { return isFinite(x) ? x.toLocaleString("fr-FR", { minimumFractionDigits: d == null ? 2 : d, maximumFractionDigits: d == null ? 2 : d }) : "—"; }
  function txt(s) { var d = document.createElement("div"); d.textContent = s == null ? "" : String(s); return d.innerHTML; }
  function num(id) { var x = parseFloat($(id).value); return isFinite(x) ? x : null; }

  var CHAMPS = ["date", "inst", "sens", "setup", "entree", "stop", "obj", "sortie", "risque", "res", "plan", "emo", "notes"];
  var ENTETES = ["Date", "Instrument", "Sens", "Setup", "Entrée", "Stop", "Objectif", "Sortie", "Risque (€)", "Résultat (€)", "Plan respecté", "Émotion", "Notes", "R"];

  function afficher() {
    var t = lire();
    var tb = $("j-table").querySelector("tbody");
    tb.innerHTML = "";
    t.forEach(function (tr, i) {
      var R = tr.risque > 0 ? tr.res / tr.risque : NaN;
      var row = document.createElement("tr");
      row.innerHTML = "<td>" + txt(tr.date) + "</td><td>" + txt(tr.inst) + "</td><td>" + txt(tr.sens) + "</td><td>" + txt(tr.setup) + "</td>" +
        '<td class="n">' + txt(tr.entree) + '</td><td class="n">' + txt(tr.stop) + '</td><td class="n">' + txt(tr.sortie) + "</td>" +
        '<td class="n">' + f(tr.risque) + '</td><td class="n ' + (tr.res >= 0 ? "pos" : "neg") + '">' + f(tr.res) + '</td><td class="n">' + f(R) + "</td>" +
        "<td>" + txt(tr.plan) + "</td><td>" + txt(tr.emo) + "</td><td>" + txt(tr.notes) + "</td>" +
        '<td><button type="button" class="btn" data-suppr="' + i + '" aria-label="Supprimer ce trade">✕</button></td>';
      tb.appendChild(row);
    });
    stats(t);
  }

  function stats(t) {
    var out = $("j-stats");
    if (!t.length) { out.innerHTML = "<p>Aucun trade pour l'instant. Ajoutez-en ou chargez les exemples fictifs pour voir les statistiques.</p>"; return; }
    var n = t.length, g = 0, sg = 0, sp = 0, sR = 0, nR = 0, horsPlan = 0, resHP = 0, resP = 0, emo = {};
    t.forEach(function (x) {
      if (x.res > 0) { g++; sg += x.res; } else sp += -x.res;
      if (x.risque > 0) { sR += x.res / x.risque; nR++; }
      if (x.plan === "Non") { horsPlan++; resHP += x.res; } else resP += x.res;
      if (x.res < 0) emo[x.emo] = (emo[x.emo] || 0) + 1;
    });
    var emoMax = Object.keys(emo).sort(function (a, b) { return emo[b] - emo[a]; })[0];
    out.innerHTML = '<div class="kpis">' +
      '<div class="kpi"><small>Trades</small><b>' + n + "</b></div>" +
      '<div class="kpi"><small>Taux de réussite</small><b>' + f(g / n * 100, 1) + " %</b></div>" +
      '<div class="kpi"><small>Résultat total</small><b class="' + (sg - sp >= 0 ? "pos" : "neg") + '">' + f(sg - sp) + " €</b></div>" +
      '<div class="kpi"><small>Espérance moyenne</small><b>' + (nR ? f(sR / nR) + " R" : "—") + "</b></div>" +
      '<div class="kpi"><small>Profit factor</small><b>' + (sp > 0 ? f(sg / sp) : "∞") + "</b></div>" +
      '<div class="kpi"><small>Trades hors plan</small><b>' + horsPlan + " (" + f(resHP) + " €)</b></div>" +
      '<div class="kpi"><small>Résultat des trades dans le plan</small><b>' + f(resP) + " €</b></div>" +
      (emoMax ? '<div class="kpi"><small>Émotion la plus fréquente sur les pertes</small><b>' + txt(emoMax) + "</b></div>" : "") +
      "</div>" + (n < 30 ? "<p><small>Moins de 30 trades : ces statistiques sont encore très dépendantes du hasard.</small></p>" : "");
  }

  $("j-date").valueAsDate = new Date();
  $("j-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var tr = {
      date: $("j-date").value, inst: $("j-inst").value.trim(), sens: $("j-sens").value, setup: $("j-setup").value.trim(),
      entree: num("j-entree"), stop: num("j-stop"), obj: num("j-obj"), sortie: num("j-sortie"),
      risque: num("j-risque"), res: num("j-res"), plan: $("j-plan").value, emo: $("j-emo").value, notes: $("j-notes").value.trim()
    };
    if (tr.risque == null || tr.res == null) { alert("Le risque initial et le résultat sont obligatoires."); return; }
    var t = lire(); t.push(tr); ecrire(t); afficher();
    ["j-inst", "j-setup", "j-entree", "j-stop", "j-obj", "j-sortie", "j-risque", "j-res", "j-notes"].forEach(function (id) { $(id).value = ""; });
  });
  $("j-table").addEventListener("click", function (e) {
    var b = e.target.closest("[data-suppr]");
    if (!b) return;
    var t = lire(); t.splice(parseInt(b.getAttribute("data-suppr"), 10), 1); ecrire(t); afficher();
  });
  $("j-vider").addEventListener("click", function () {
    if (confirm("Supprimer tous les trades du journal ? Pensez à exporter avant.")) { ecrire([]); afficher(); }
  });

  function csvCell(v) { var s = v == null ? "" : (typeof v === "number" ? String(v).replace(".", ",") : String(v)); return /[";\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
  function telecharger(nom, contenu) {
    var blob = new Blob(["﻿" + contenu], { type: "text/csv;charset=utf-8" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = nom;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }
  $("j-export").addEventListener("click", function () {
    var lignes = [ENTETES.join(";")];
    lire().forEach(function (tr) {
      var R = tr.risque > 0 ? (tr.res / tr.risque).toFixed(2).replace(".", ",") : "";
      lignes.push(CHAMPS.map(function (c) { return csvCell(tr[c]); }).concat([R]).join(";"));
    });
    telecharger("journal-de-trading.csv", lignes.join("\n"));
  });
  $("j-modele").addEventListener("click", function () {
    telecharger("modele-journal-de-trading.csv", ENTETES.join(";") + "\n");
  });
  $("j-exemple").addEventListener("click", function () {
    var ex = [
      { date: "2026-01-05", inst: "Action fictive A", sens: "Achat", setup: "Cassure de résistance", entree: 50, stop: 48, obj: 54, sortie: 54, risque: 100, res: 195, plan: "Oui", emo: "Calme", notes: "Plan suivi, sortie à l'objectif" },
      { date: "2026-01-06", inst: "EUR/USD", sens: "Vente", setup: "Pullback sous EMA 20", entree: 1.085, stop: 1.088, obj: 1.079, sortie: 1.088, risque: 100, res: -104, plan: "Oui", emo: "Calme", notes: "Perte normale" },
      { date: "2026-01-06", inst: "EUR/USD", sens: "Achat", setup: "", entree: 1.088, stop: 1.084, obj: 1.095, sortie: 1.0835, risque: 100, res: -118, plan: "Non", emo: "Frustration / revanche", notes: "Trade de revanche juste après la perte : à éviter" },
      { date: "2026-01-08", inst: "Indice fictif", sens: "Achat", setup: "Pullback sur EMA 20", entree: 7500, stop: 7460, obj: 7580, sortie: 7540, risque: 100, res: 96, plan: "Oui", emo: "Peur", notes: "Sortie anticipée par peur, objectif atteint ensuite" }
    ];
    ecrire(lire().concat(ex)); afficher();
  });
  afficher();
})();
