/* Simulateurs : effet du levier, séries de pertes, trajectoires Monte-Carlo (canvas fait main). */
(function () {
  "use strict";
  function $(id) { return document.getElementById(id); }
  function v(id) { var x = parseFloat(String($(id).value).replace(",", ".")); return isFinite(x) ? x : NaN; }
  function f(x, d) {
    if (!isFinite(x)) return "—";
    if (d == null) d = Math.abs(x) >= 100 ? 0 : 2;
    return x.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d });
  }
  function couleurs() {
    var cs = getComputedStyle(document.documentElement);
    function c(n) { return cs.getPropertyValue(n).trim(); }
    return { texte: c("--texte-2"), bord: c("--bord"), discret: c("--discret"), accent: c("--accent"), haus: c("--haus"),
      bais: c("--bais"), l2: c("--l2"), l3: c("--l3"), l4: c("--l4"), l5: c("--l5"), surface: c("--surface") };
  }

  /* Petit moteur de tracé : repère, grilles, courbes */
  function Repere(canvas, x0, x1, y0, y1, opts) {
    opts = opts || {};
    var dpr = window.devicePixelRatio || 1;
    var w = canvas.clientWidth, h = canvas.clientHeight;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    var ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    var L = 58, R = 14, T = 14, B = 34;
    var C = couleurs();
    var rp = {
      ctx: ctx, C: C, w: w, h: h,
      X: function (x) { return L + (x - x0) / (x1 - x0) * (w - L - R); },
      Y: function (y) { return T + (y1 - y) / (y1 - y0) * (h - T - B); }
    };
    ctx.font = "12px system-ui, sans-serif";
    ctx.lineWidth = 1;
    function ticks(a, b, n) {
      var span = b - a, raw = span / n, mag = Math.pow(10, Math.floor(Math.log10(raw))), st = mag;
      [1, 2, 2.5, 5, 10].some(function (m) { st = m * mag; return st >= raw; });
      var t = [], s = Math.ceil(a / st) * st;
      for (var k = s; k <= b + 1e-9; k += st) t.push(+k.toFixed(10));
      return t;
    }
    ctx.fillStyle = C.texte; ctx.strokeStyle = C.bord;
    ticks(y0, y1, 5).forEach(function (t) {
      ctx.beginPath(); ctx.moveTo(L, rp.Y(t)); ctx.lineTo(w - R, rp.Y(t)); ctx.stroke();
      ctx.textAlign = "right"; ctx.fillText((opts.yfmt || f)(t), L - 6, rp.Y(t) + 4);
    });
    ticks(x0, x1, 6).forEach(function (t) {
      ctx.textAlign = "center"; ctx.fillText((opts.xfmt || f)(t), rp.X(t), h - B + 16);
    });
    ctx.strokeStyle = C.discret;
    ctx.beginPath(); ctx.moveTo(L, T); ctx.lineTo(L, h - B); ctx.lineTo(w - R, h - B); ctx.stroke();
    if (y0 < 0 && y1 > 0) { ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(L, rp.Y(0)); ctx.lineTo(w - R, rp.Y(0)); ctx.stroke(); ctx.setLineDash([]); }
    if (opts.xlabel) { ctx.textAlign = "center"; ctx.fillText(opts.xlabel, (L + w - R) / 2, h - 4); }
    rp.courbe = function (pts, couleur, ep, alpha) {
      ctx.save(); ctx.strokeStyle = couleur; ctx.lineWidth = ep || 2; ctx.globalAlpha = alpha == null ? 1 : alpha;
      ctx.beginPath();
      pts.forEach(function (p, i) { var X = rp.X(p[0]), Y = rp.Y(p[1]); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); });
      ctx.stroke(); ctx.restore();
    };
    rp.zone = function (ya, yb, couleur, alpha) {
      ctx.save(); ctx.fillStyle = couleur; ctx.globalAlpha = alpha || 0.12;
      ctx.fillRect(L, rp.Y(yb), w - L - R, rp.Y(ya) - rp.Y(yb)); ctx.restore();
    };
    rp.legende = function (items) {
      items.forEach(function (it, i) {
        var y = T + 10 + i * 16;
        ctx.save(); ctx.strokeStyle = it[1]; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(L + 10, y); ctx.lineTo(L + 30, y); ctx.stroke();
        ctx.fillStyle = C.texte; ctx.textAlign = "left"; ctx.fillText(it[0], L + 36, y + 4); ctx.restore();
      });
    };
    return rp;
  }

  /* ---------------- 1. Levier ---------------- */
  function calcLevier() {
    var cap = v("lv-capital"), lev = v("lv-levier"), dv = v("lv-var");
    $("lv-levier-v").textContent = lev;
    $("lv-var-v").textContent = (dv > 0 ? "+" : "") + f(dv, 1).replace("-", "−");
    var expo = cap * lev, pl = expo * dv / 100, pct = pl / cap * 100;
    var seuil = 100 / lev;
    var h = '<div class="kpis">' +
      '<div class="kpi"><small>Exposition</small><b>' + f(expo) + " €</b></div>" +
      '<div class="kpi"><small>Résultat</small><b class="' + (pl >= 0 ? "pos" : "neg") + '">' + (pl >= 0 ? "+" : "") + f(Math.max(pl, -cap)) + " €</b></div>" +
      '<div class="kpi"><small>En % du capital</small><b class="' + (pl >= 0 ? "pos" : "neg") + '">' + (pct >= 0 ? "+" : "") + f(Math.max(pct, -100), 1) + " %</b></div>" +
      '<div class="kpi"><small>Baisse qui efface tout le capital</small><b>−' + f(seuil, 2) + " %</b></div>" +
      "</div>";
    h += '<div class="calcul">Exposition = ' + f(cap) + " × " + lev + " = " + f(expo) + " €\n" +
      "Résultat = " + f(expo) + " × " + f(dv, 1) + " % = " + f(pl) + " €  →  " + f(pct, 1) + " % du capital (= " + f(dv, 1) + " % × " + lev + ")\n" +
      "Capital effacé si le marché bouge de 100 % ÷ " + lev + " = " + f(seuil, 2) + " % contre vous</div>";
    if (pct <= -100) h += '<p class="alerte">Le capital engagé est entièrement perdu. Dans la réalité, la position aurait été liquidée avant, et un gap peut aggraver la perte.</p>';
    $("r-levier").innerHTML = h;
    var c = $("c-levier");
    var rp = Repere(c, -15, 15, -150, 150, { xlabel: "Variation du marché (%)", yfmt: function (t) { return f(t, 0) + " %"; }, xfmt: function (t) { return f(t, 0); } });
    rp.zone(-150, -100, rp.C.bais, 0.15);
    var cols = [rp.C.discret, rp.C.accent, rp.C.l2, rp.C.bais];
    var levs = [1, 5, 10, 30];
    levs.forEach(function (L, i) {
      rp.courbe([[-15, Math.max(-150, -15 * L)], [Math.max(-15, -150 / L), Math.max(-150, -15 * L)], [Math.min(15, 150 / L), Math.min(150, 15 * L)], [15, Math.min(150, 15 * L)]].sort(function (a, b) { return a[0] - b[0]; }), cols[i], 1.6, 0.6);
    });
    rp.courbe([[-15, Math.max(-150, -15 * lev)], [Math.max(-15, -150 / lev), Math.max(-150, -15 * lev)], [Math.min(15, 150 / lev), Math.min(150, 15 * lev)], [15, Math.min(150, 15 * lev)]], rp.C.l4, 3.5, 1);
    var ctx = rp.ctx;
    ctx.fillStyle = rp.C.l4; ctx.beginPath(); ctx.arc(rp.X(dv), rp.Y(Math.max(-150, Math.min(150, pct))), 5, 0, 6.3); ctx.fill();
    rp.legende([["Levier 1×", cols[0]], ["Levier 5×", cols[1]], ["Levier 10×", cols[2]], ["Levier 30×", cols[3]], ["Votre levier (" + lev + "×)", rp.C.l4]]);
  }
  ["lv-capital", "lv-levier", "lv-var"].forEach(function (id) { $(id).addEventListener("input", calcLevier); });

  /* ---------------- 2. Séries de pertes ---------------- */
  // Probabilité d'au moins une série de k pertes consécutives sur n trades (programmation dynamique)
  function probSerie(n, k, q) {
    // etat[j] = probabilité d'être sur une série en cours de j pertes sans avoir encore atteint k
    var etat = new Array(k).fill(0); etat[0] = 1; var atteint = 0;
    for (var i = 0; i < n; i++) {
      var nouv = new Array(k).fill(0);
      for (var j = 0; j < k; j++) {
        if (!etat[j]) continue;
        nouv[0] += etat[j] * (1 - q);
        if (j + 1 >= k) atteint += etat[j] * q; else nouv[j + 1] += etat[j] * q;
      }
      etat = nouv;
    }
    return atteint;
  }
  function calcSeries() {
    var cap = v("se-capital"), r = v("se-risque") / 100, n = Math.round(v("se-n")), w = v("se-win") / 100;
    if (!(cap > 0) || !(r >= 0) || !(n >= 1)) return;
    var fin = cap * Math.pow(1 - r, n), dd = 1 - fin / cap, rattrapage = fin > 0 ? cap / fin - 1 : Infinity;
    var q = 1 - w;
    var p100 = probSerie(100, n, q), p500 = probSerie(500, n, q);
    var h = '<div class="kpis">' +
      '<div class="kpi"><small>Capital après ' + n + " pertes</small><b>" + f(fin) + " €</b></div>" +
      '<div class="kpi"><small>Drawdown</small><b class="neg">−' + f(dd * 100, 1) + " %</b></div>" +
      '<div class="kpi"><small>Gain nécessaire pour revenir</small><b>+' + (isFinite(rattrapage) ? f(rattrapage * 100, 1) : "∞") + " %</b></div>" +
      '<div class="kpi"><small>Proba. d\'au moins une série de ' + n + " pertes en 100 trades</small><b>" + f(p100 * 100, 1) + " %</b></div>" +
      '<div class="kpi"><small>… en 500 trades</small><b>' + f(p500 * 100, 1) + " %</b></div>" +
      "</div>";
    h += '<div class="calcul">Capital restant = ' + f(cap) + " × (1 − " + f(r * 100, 1) + " %)^" + n + " = " + f(fin) + " €\n" +
      "Gain pour revenir = capital initial ÷ capital restant − 1 = " + f(cap) + " ÷ " + f(fin) + " − 1 = " + (isFinite(rattrapage) ? f(rattrapage * 100, 1) : "∞") + " %\n" +
      "Probabilité de " + n + " pertes d'affilée sur une séquence donnée = " + f(q, 2) + "^" + n + " = " + f(Math.pow(q, n) * 100, 3) + " % ; mais sur de nombreux trades, une telle série finit souvent par arriver.</div>" +
      "<p><small>Hypothèse : trades indépendants avec un taux de réussite constant. En réalité, les pertes ont tendance à se regrouper quand le marché change de régime : ces probabilités sont plutôt optimistes.</small></p>";
    $("r-series").innerHTML = h;
    var c = $("c-series");
    var rp = Repere(c, 0, n, 0, cap * 1.05, { xlabel: "Nombre de pertes consécutives", xfmt: function (t) { return f(t, 0); }, yfmt: function (t) { return f(t, 0); } });
    var niveaux = [[0.01, rp.C.haus], [0.02, rp.C.accent], [0.05, rp.C.l2], [0.10, rp.C.bais]];
    niveaux.forEach(function (nv) {
      var pts = []; for (var i = 0; i <= n; i++) pts.push([i, cap * Math.pow(1 - nv[0], i)]);
      rp.courbe(pts, nv[1], 1.6, 0.7);
    });
    var pts = []; for (var i = 0; i <= n; i++) pts.push([i, cap * Math.pow(1 - r, i)]);
    rp.courbe(pts, rp.C.l4, 3.5);
    rp.legende([["1 % par trade", rp.C.haus], ["2 %", rp.C.accent], ["5 %", rp.C.l2], ["10 %", rp.C.bais], ["Votre réglage (" + f(r * 100, 1) + " %)", rp.C.l4]]);
  }
  ["se-capital", "se-risque", "se-n", "se-win"].forEach(function (id) { $(id).addEventListener("input", calcSeries); });

  /* ---------------- 3. Monte-Carlo ---------------- */
  var dernier = null;
  function simuler() {
    var cap = v("mc-capital"), w = v("mc-win") / 100, R = v("mc-rr"), r = v("mc-risque") / 100;
    var n = Math.min(2000, Math.round(v("mc-n"))), S = Math.min(500, Math.round(v("mc-sims")));
    if (!(cap > 0 && w > 0 && w < 1 && R > 0 && r > 0 && n > 0 && S > 0)) { $("r-mc").innerHTML = "<p>Vérifiez les paramètres.</p>"; return; }
    var trajs = [], finaux = [], ddmax = [], series = [], ruine50 = 0, perte = 0;
    for (var s = 0; s < S; s++) {
      var c = cap, pic = cap, dd = 0, serie = 0, serieMax = 0, t = [c];
      for (var i = 0; i < n; i++) {
        if (Math.random() < w) { c += c * r * R; serie = 0; } else { c -= c * r; serie++; if (serie > serieMax) serieMax = serie; }
        if (c > pic) pic = c;
        dd = Math.max(dd, 1 - c / pic);
        t.push(c);
      }
      trajs.push(t); finaux.push(c); ddmax.push(dd); series.push(serieMax);
      if (Math.min.apply(null, t) <= cap * 0.5) ruine50++;
      if (c < cap) perte++;
    }
    function med(a) { var b = a.slice().sort(function (x, y) { return x - y; }); var m = Math.floor(b.length / 2); return b.length % 2 ? b[m] : (b[m - 1] + b[m]) / 2; }
    var espR = w * R - (1 - w);
    dernier = { trajs: trajs, cap: cap, n: n };
    var h = '<div class="kpis">' +
      '<div class="kpi"><small>Espérance par trade</small><b class="' + (espR >= 0 ? "pos" : "neg") + '">' + (espR >= 0 ? "+" : "") + f(espR, 3) + " R</b></div>" +
      '<div class="kpi"><small>Capital final médian</small><b>' + f(med(finaux)) + " €</b></div>" +
      '<div class="kpi"><small>Meilleur / pire final</small><b>' + f(Math.max.apply(null, finaux)) + " / " + f(Math.min.apply(null, finaux)) + " €</b></div>" +
      '<div class="kpi"><small>Simulations finissant en perte</small><b>' + f(perte / S * 100, 0) + " %</b></div>" +
      '<div class="kpi"><small>Drawdown max médian</small><b class="neg">−' + f(med(ddmax) * 100, 1) + " %</b></div>" +
      '<div class="kpi"><small>Pire drawdown observé</small><b class="neg">−' + f(Math.max.apply(null, ddmax) * 100, 1) + " %</b></div>" +
      '<div class="kpi"><small>Passées sous 50 % du capital</small><b>' + f(ruine50 / S * 100, 0) + " %</b></div>" +
      '<div class="kpi"><small>Plus longue série de pertes (médiane)</small><b>' + f(med(series), 0) + "</b></div>" +
      "</div>";
    h += '<div class="calcul">Espérance = ' + f(w, 2) + " × " + f(R, 2) + " − " + f(1 - w, 2) + " × 1 = " + f(espR, 3) + " R par trade\n" +
      "Chaque trade risque " + f(r * 100, 1) + " % du capital du moment (risque composé).</div>";
    if (espR <= 0) h += '<p class="alerte">Espérance négative ou nulle : aucune gestion de la taille ne rend une telle stratégie gagnante à long terme.</p>';
    $("r-mc").innerHTML = h;
    dessinerMC();
  }
  function dessinerMC() {
    if (!dernier) return;
    var max = 0, min = Infinity;
    dernier.trajs.forEach(function (t) { t.forEach(function (x) { if (x > max) max = x; if (x < min) min = x; }); });
    max = Math.min(max, dernier.cap * 20);
    var rp = Repere($("c-mc"), 0, dernier.n, Math.max(0, min * 0.9), max * 1.05, { xlabel: "Nombre de trades", xfmt: function (t) { return f(t, 0); }, yfmt: function (t) { return f(t, 0); } });
    var cols = [rp.C.accent, rp.C.l2, rp.C.l3, rp.C.l4, rp.C.l5];
    dernier.trajs.forEach(function (t, k) {
      var pas = Math.max(1, Math.floor(t.length / 400));
      var pts = [];
      for (var i = 0; i < t.length; i += pas) pts.push([i, Math.min(t[i], max * 1.05)]);
      rp.courbe(pts, cols[k % cols.length], 1.2, 0.45);
    });
    var ctx = rp.ctx; ctx.save(); ctx.strokeStyle = rp.C.texte; ctx.setLineDash([6, 4]); ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(rp.X(0), rp.Y(dernier.cap)); ctx.lineTo(rp.X(dernier.n), rp.Y(dernier.cap)); ctx.stroke(); ctx.restore();
  }
  $("mc-go").addEventListener("click", simuler);

  function toutRedessiner() { calcLevier(); calcSeries(); dessinerMC(); }
  var minuteur;
  window.addEventListener("resize", function () { clearTimeout(minuteur); minuteur = setTimeout(toutRedessiner, 150); });
  document.addEventListener("ft-theme", toutRedessiner);
  calcLevier(); calcSeries(); simuler();
})();
