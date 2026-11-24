/* Glossaire : recherche instantanée (insensible aux accents) + filtre par catégorie. */
(function () {
  "use strict";
  var champ = document.getElementById("glo-recherche");
  var puces = document.querySelectorAll(".puce");
  var entrees = Array.prototype.slice.call(document.querySelectorAll(".entree"));
  var lettres = document.querySelectorAll(".lettre");
  var compte = document.getElementById("glo-compte");
  var vide = document.getElementById("glo-vide");
  var cat = "";

  function norm(s) {
    return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  }
  function titreNorm(e) {
    if (!e._t) e._t = norm(e.querySelector("h3").textContent);
    return e._t;
  }

  function filtrer() {
    var q = norm(champ.value.trim());
    var mots = q ? q.split(/\s+/) : [];
    var n = 0;
    entrees.forEach(function (e) {
      var okCat = !cat || e.getAttribute("data-cat") === cat;
      var txt = e.getAttribute("data-recherche");
      var okTxt = mots.every(function (m) { return txt.indexOf(m) !== -1; });
      var vis = okCat && okTxt;
      e.hidden = !vis;
      if (vis) n++;
    });
    // les termes dont le titre correspond passent en premier dans chaque lettre
    lettres.forEach(function (l) {
      var visibles = l.querySelectorAll(".entree:not([hidden])");
      l.hidden = visibles.length === 0;
    });
    compte.textContent = n + " terme" + (n > 1 ? "s" : "") + (q || cat ? " trouvé" + (n > 1 ? "s" : "") : " au total");
    vide.hidden = n !== 0;
  }

  champ.addEventListener("input", filtrer);
  champ.addEventListener("keydown", function (ev) {
    if (ev.key === "Enter") {
      var q = norm(champ.value.trim());
      var cible = entrees.filter(function (e) { return !e.hidden; })
        .sort(function (a, b) { return (titreNorm(a).indexOf(q) === 0 ? 0 : 1) - (titreNorm(b).indexOf(q) === 0 ? 0 : 1); })[0];
      if (cible) { cible.scrollIntoView({ block: "start" }); surligner(cible); }
    }
  });
  Array.prototype.forEach.call(puces, function (p) {
    p.addEventListener("click", function () {
      cat = p.getAttribute("data-cat");
      Array.prototype.forEach.call(puces, function (x) {
        var actif = x === p;
        x.classList.toggle("actif", actif);
        x.setAttribute("aria-pressed", actif ? "true" : "false");
      });
      filtrer();
    });
  });

  function surligner(el) {
    entrees.forEach(function (e) { e.classList.remove("cible"); });
    el.classList.add("cible");
  }
  function depuisAncre() {
    var id = decodeURIComponent(window.location.hash.slice(1));
    if (!id) return;
    var el = document.getElementById(id);
    if (el && el.classList.contains("entree")) {
      if (el.hidden) { champ.value = ""; cat = ""; filtrer(); }
      surligner(el);
      setTimeout(function () { el.scrollIntoView({ block: "start" }); }, 30);
    }
  }
  window.addEventListener("hashchange", depuisAncre);
  filtrer();
  depuisAncre();
})();
