/* Moteur de quiz (QCM à réponse unique) : affichage, correction détaillée, score sauvegardé.
   Données attendues : window.QUIZ = { id, titre, retour, questions: [{ q, c: [...], a: index, e: "explication", t?: thème }] } */
(function () {
  "use strict";
  var Q = window.QUIZ;
  var zone = document.getElementById("quiz");
  if (!Q || !zone) return;
  var P = window.FTProgression;
  var ordre = [];

  function melanger(t) {
    for (var i = t.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var x = t[i]; t[i] = t[j]; t[j] = x; }
    return t;
  }

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function rendre(melange) {
    zone.innerHTML = "";
    ordre = Q.questions.map(function (q, i) {
      var choix = q.c.map(function (_, k) { return k; });
      return { i: i, choix: melanger(choix) }; // choix toujours mélangés ; ordre des questions mélangé seulement au « Recommencer »
    });
    if (melange) melanger(ordre);

    var best = P && P.score(Q.id);
    if (best) zone.appendChild(el("p", "chapeau", "Votre meilleur score jusqu'ici : <strong>" + best.meilleur + " %</strong> (" + best.essais + " essai" + (best.essais > 1 ? "s" : "") + ")."));

    var resultat = el("div", "quiz-resultat");
    resultat.hidden = true;
    resultat.id = "quiz-resultat";
    resultat.setAttribute("tabindex", "-1");
    zone.appendChild(resultat);

    var form = el("form", "quiz-form");
    form.setAttribute("novalidate", "");
    ordre.forEach(function (o, n) {
      var q = Q.questions[o.i];
      var bloc = el("div", "quiz-q");
      bloc.id = "q-" + n;
      var fs = el("fieldset");
      var lg = el("legend", null, '<span class="quiz-num">' + (n + 1) + ".</span> " + q.q);
      fs.appendChild(lg);
      o.choix.forEach(function (k) {
        var lab = el("label", "quiz-choix");
        var inp = document.createElement("input");
        inp.type = "radio"; inp.name = "q" + n; inp.value = k;
        lab.appendChild(inp);
        lab.appendChild(el("span", null, q.c[k]));
        fs.appendChild(lab);
      });
      bloc.appendChild(fs);
      form.appendChild(bloc);
    });
    var barre = el("div", "quiz-barre");
    var btn = el("button", "btn btn-principal", "Valider mes réponses");
    btn.type = "submit";
    var info = el("span", "quiz-info");
    barre.appendChild(btn); barre.appendChild(info);
    form.appendChild(barre);
    zone.appendChild(form);

    form.addEventListener("change", function () {
      var n = form.querySelectorAll("input:checked").length;
      info.textContent = n + " / " + ordre.length + " réponses";
    });
    info.textContent = "0 / " + ordre.length + " réponses";

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var manquantes = ordre.length - form.querySelectorAll("input:checked").length;
      if (manquantes > 0 && !window.confirm(manquantes + " question(s) sans réponse : elles seront comptées fausses. Valider quand même ?")) return;
      corriger(form, resultat, btn);
    });
  }

  function corriger(form, resultat, btn) {
    var bonnes = 0, themes = {};
    ordre.forEach(function (o, n) {
      var q = Q.questions[o.i];
      var bloc = document.getElementById("q-" + n);
      var coche = form.querySelector('input[name="q' + n + '"]:checked');
      var rep = coche ? parseInt(coche.value, 10) : -1;
      var ok = rep === q.a;
      if (ok) bonnes++;
      if (q.t) { themes[q.t] = themes[q.t] || [0, 0]; themes[q.t][1]++; if (ok) themes[q.t][0]++; }
      bloc.classList.add(ok ? "ok" : "ko");
      Array.prototype.forEach.call(bloc.querySelectorAll(".quiz-choix"), function (lab) {
        var inp = lab.querySelector("input");
        var k = parseInt(inp.value, 10);
        inp.disabled = true;
        if (k === q.a) lab.classList.add("bonne");
        else if (k === rep) lab.classList.add("fausse");
      });
      var ex = el("div", "quiz-expl",
        '<span class="quiz-verdict ' + (ok ? "pos" : "neg") + '">' + (ok ? "✓ Bonne réponse." : (rep < 0 ? "✗ Pas de réponse." : "✗ Mauvaise réponse.")) + "</span> " + q.e);
      bloc.appendChild(ex);
    });
    var total = ordre.length;
    var pct = Math.round(bonnes / total * 100);
    var s = P ? P.enregistrerScore(Q.id, bonnes, total) : null;
    var msg = pct >= 80 ? "Très bien : les notions sont acquises." :
      pct >= 60 ? "Correct, mais relisez les explications des erreurs avant de passer à la suite." :
        "Il est conseillé de relire le module avant de continuer : ce n'est pas un échec, c'est le but d'un quiz.";
    var h = '<p class="quiz-score">' + bonnes + " / " + total + " (" + pct + " %)</p><p>" + msg + "</p>";
    if (s) h += "<p><small>Meilleur score enregistré : " + s.meilleur + " % · essai n° " + s.essais + "</small></p>";
    var tk = Object.keys(themes);
    if (tk.length) {
      h += "<p><strong>Détail par module :</strong></p><ul class=\"quiz-themes\">";
      tk.sort(function (a, b) { return parseInt(a.replace(/\D/g, ""), 10) - parseInt(b.replace(/\D/g, ""), 10); });
      tk.forEach(function (t) { var v = themes[t]; h += "<li>" + t + " : " + v[0] + "/" + v[1] + (v[0] < v[1] ? " — à revoir" : "") + "</li>"; });
      h += "</ul>";
    }
    h += '<div class="actions"><button type="button" class="btn btn-principal" id="quiz-refaire">↻ Recommencer (ordre mélangé)</button>';
    if (Q.retour) h += '<a class="btn" href="' + Q.retour + '">Revenir au module</a>';
    h += "</div>";
    resultat.innerHTML = h;
    resultat.hidden = false;
    btn.disabled = true;
    resultat.focus();
    resultat.scrollIntoView({ block: "start" });
    document.getElementById("quiz-refaire").addEventListener("click", function () { rendre(true); window.scrollTo(0, 0); });
    var r = resultat;
    // le bloc résultat n'est plus collant une fois lu, pour ne pas masquer la correction
    window.setTimeout(function () { r.style.position = "static"; }, 50);
  }

  rendre(false);
})();
