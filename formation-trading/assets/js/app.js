/* Formation Trading — script commun à toutes les pages.
   - thème clair / sombre
   - menu latéral mobile
   - progression (modules lus, scores aux quiz) dans localStorage, protégée par try/catch
   - boutons « Voir la correction »
*/
(function () {
  "use strict";

  /* ---------- Stockage sécurisé ---------- */
  var CLE = "ft-progression-v1";
  var memoire = null; // repli si localStorage indisponible (navigation privée, file:// sous Firefox…)

  function lire() {
    try {
      var brut = window.localStorage.getItem(CLE);
      if (brut) return JSON.parse(brut);
    } catch (e) { /* stockage indisponible ou JSON corrompu */ }
    return memoire || { lus: {}, quiz: {} };
  }
  function ecrire(etat) {
    memoire = etat;
    try {
      window.localStorage.setItem(CLE, JSON.stringify(etat));
      return true;
    } catch (e) { return false; }
  }
  function stockageDisponible() {
    try {
      var k = "__ft_test__";
      window.localStorage.setItem(k, "1");
      window.localStorage.removeItem(k);
      return true;
    } catch (e) { return false; }
  }

  var Progression = {
    etat: lire,
    estLu: function (id) { return !!lire().lus[id]; },
    marquerLu: function (id, valeur) {
      var e = lire(); e.lus = e.lus || {};
      if (valeur) e.lus[id] = new Date().toISOString(); else delete e.lus[id];
      ecrire(e);
    },
    score: function (qid) { var e = lire(); return (e.quiz || {})[qid] || null; },
    enregistrerScore: function (qid, bonnes, total) {
      var e = lire(); e.quiz = e.quiz || {};
      var ancien = e.quiz[qid];
      var pct = Math.round(bonnes / total * 100);
      e.quiz[qid] = {
        dernier: pct, meilleur: ancien ? Math.max(ancien.meilleur, pct) : pct,
        essais: ancien ? ancien.essais + 1 : 1, date: new Date().toISOString()
      };
      ecrire(e);
      return e.quiz[qid];
    },
    reinitialiser: function () {
      memoire = { lus: {}, quiz: {} };
      try { window.localStorage.removeItem(CLE); } catch (e) {}
    },
    disponible: stockageDisponible
  };
  window.FTProgression = Progression;

  /* ---------- Thème ---------- */
  function themeCourant() {
    var attr = document.documentElement.getAttribute("data-theme");
    if (attr) return attr;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  var btnTheme = document.querySelector(".btn-theme");
  if (btnTheme) {
    btnTheme.addEventListener("click", function () {
      var nouveau = themeCourant() === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", nouveau);
      try { window.localStorage.setItem("ft-theme", nouveau); } catch (e) {}
      document.dispatchEvent(new CustomEvent("ft-theme"));
    });
  }

  /* ---------- Menu mobile ---------- */
  var btnMenu = document.querySelector(".btn-menu");
  var voile = document.querySelector(".voile");
  function menu(ouvrir) {
    document.body.classList.toggle("menu-ouvert", ouvrir);
    if (btnMenu) btnMenu.setAttribute("aria-expanded", ouvrir ? "true" : "false");
    if (voile) voile.hidden = !ouvrir;
  }
  if (btnMenu) btnMenu.addEventListener("click", function () { menu(!document.body.classList.contains("menu-ouvert")); });
  if (voile) voile.addEventListener("click", function () { menu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") menu(false); });

  /* ---------- Marques « lu » dans le menu ---------- */
  function rafraichirMenu() {
    var items = document.querySelectorAll(".nav-modules li[data-module]");
    for (var i = 0; i < items.length; i++) {
      var id = items[i].getAttribute("data-module");
      items[i].classList.toggle("lu", Progression.estLu("m" + id));
    }
  }
  rafraichirMenu();
  var courant = document.querySelector('.sidebar a[aria-current="page"]');
  if (courant && courant.scrollIntoView) {
    try { courant.scrollIntoView({ block: "center" }); window.scrollTo(0, 0); } catch (e) {}
  }

  /* ---------- Bouton « Marquer comme lu » ---------- */
  var btnLu = document.querySelector(".btn-lu");
  if (btnLu) {
    var mid = "m" + btnLu.getAttribute("data-module");
    var majLu = function () {
      var lu = Progression.estLu(mid);
      btnLu.classList.toggle("est-lu", lu);
      btnLu.textContent = lu ? "✓ Module lu (cliquer pour annuler)" : "✓ Marquer ce module comme lu";
    };
    majLu();
    btnLu.addEventListener("click", function () {
      Progression.marquerLu(mid, !Progression.estLu(mid));
      majLu(); rafraichirMenu();
    });
  }

  /* ---------- Corrections d'exercices ---------- */
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".btn-corr");
    if (!b) return;
    var c = b.nextElementSibling;
    if (!c) return;
    var ouvert = b.getAttribute("aria-expanded") === "true";
    b.setAttribute("aria-expanded", ouvert ? "false" : "true");
    b.textContent = ouvert ? "Voir la correction" : "Masquer la correction";
    c.hidden = ouvert;
  });

  /* ---------- Accueil : tableau de progression ---------- */
  var zone = document.getElementById("progression");
  if (zone && window.FT_MODULES) {
    var mods = window.FT_MODULES;
    var nbLus = 0, nbQuiz = 0, somme = 0;
    mods.forEach(function (m) {
      var carte = document.querySelector('.carte-module[data-module="' + m.id + '"]');
      var lu = Progression.estLu("m" + m.id);
      var sc = Progression.score("q" + m.id);
      if (lu) nbLus++;
      if (sc) { nbQuiz++; somme += sc.meilleur; }
      if (carte) {
        carte.classList.toggle("lu", lu);
        var et = carte.querySelector(".carte-etat");
        var txt = [];
        if (lu) txt.push("✓ Lu");
        if (sc) txt.push("Quiz : " + sc.meilleur + " %");
        if (et) et.textContent = txt.join(" · ");
      }
    });
    var ex = Progression.score("examen");
    var pct = Math.round(nbLus / mods.length * 100);
    zone.querySelector(".jauge > span").style.width = pct + "%";
    zone.querySelector(".stats").innerHTML =
      "<span><b>" + nbLus + "/" + mods.length + "</b> modules lus (" + pct + " %)</span>" +
      "<span><b>" + nbQuiz + "/" + mods.length + "</b> quiz faits" + (nbQuiz ? " · moyenne des meilleurs scores <b>" + Math.round(somme / nbQuiz) + " %</b>" : "") + "</span>" +
      "<span>Examen final : <b>" + (ex ? ex.meilleur + " %" : "pas encore passé") + "</b></span>";
    var suite = null;
    for (var i = 0; i < mods.length; i++) { if (!Progression.estLu("m" + mods[i].id)) { suite = mods[i]; break; } }
    var lien = zone.querySelector(".reprendre");
    if (lien) {
      if (suite) { lien.href = suite.href; lien.textContent = (nbLus ? "▶ Reprendre : " : "▶ Commencer : ") + "Module " + suite.n + " — " + suite.titre; }
      else { lien.href = "examen-final.html"; lien.textContent = "🎓 Tous les modules sont lus : passer l'examen final"; }
    }
    if (!Progression.disponible()) {
      var avert = zone.querySelector(".stockage-avert");
      if (avert) avert.hidden = false;
    }
    var raz = zone.querySelector(".btn-raz");
    if (raz) raz.addEventListener("click", function () {
      if (window.confirm("Effacer toute votre progression (modules lus et scores) ?")) { Progression.reinitialiser(); window.location.reload(); }
    });
  }
})();
