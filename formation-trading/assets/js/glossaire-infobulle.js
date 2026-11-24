/* Infobulle de définition au survol (ou au focus clavier) des termes techniques.
   Le clic sur un terme ouvre sa fiche complète dans le glossaire. */
(function () {
  "use strict";
  var G = window.GLOSSAIRE || {};
  var bulle = null;

  function cacher() { if (bulle) { bulle.remove(); bulle = null; } }

  function montrer(a) {
    var slug = a.getAttribute("data-terme");
    var e = G[slug];
    if (!e) return;
    // le title natif ferait doublon avec l'infobulle
    if (a.hasAttribute("title")) { a.setAttribute("data-title", a.getAttribute("title")); a.removeAttribute("title"); }
    cacher();
    bulle = document.createElement("div");
    bulle.className = "infobulle";
    bulle.setAttribute("role", "tooltip");
    var titre = document.createElement("strong");
    titre.textContent = e.t;
    if (e.en) {
      var en = document.createElement("span");
      en.className = "en";
      en.textContent = " — " + e.en;
      titre.appendChild(en);
    }
    var d = document.createElement("span");
    d.innerHTML = e.d; // définitions rédigées par l'auteur (contenu de confiance)
    bulle.appendChild(titre);
    bulle.appendChild(d);
    document.body.appendChild(bulle);
    var r = a.getBoundingClientRect();
    var bw = bulle.offsetWidth, bh = bulle.offsetHeight;
    var x = Math.min(Math.max(8, r.left + window.scrollX), window.scrollX + document.documentElement.clientWidth - bw - 8);
    var y = r.bottom + window.scrollY + 6;
    if (r.bottom + bh + 12 > window.innerHeight) y = r.top + window.scrollY - bh - 6;
    bulle.style.left = x + "px";
    bulle.style.top = y + "px";
  }

  var survol = window.matchMedia && window.matchMedia("(hover: hover)").matches;
  document.addEventListener("mouseover", function (ev) {
    if (!survol) return;
    var a = ev.target.closest && ev.target.closest("a.terme");
    if (a) montrer(a);
  });
  document.addEventListener("mouseout", function (ev) {
    var a = ev.target.closest && ev.target.closest("a.terme");
    if (a) cacher();
  });
  document.addEventListener("focusin", function (ev) {
    if (ev.target.matches && ev.target.matches("a.terme")) montrer(ev.target);
  });
  document.addEventListener("focusout", cacher);
  window.addEventListener("scroll", cacher, { passive: true });
})();
