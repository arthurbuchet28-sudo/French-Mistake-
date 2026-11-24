"""Petits outils pour produire des graphiques SVG faits main, compatibles thème clair/sombre.

Les couleurs sont portées par des classes CSS (voir style.css, section « SVG ») :
  g-axe, g-grille, g-txt, g-txt-fort, g-haus, g-bais, g-l1..g-l5 (lignes), g-zone-sup,
  g-zone-res, g-zone, g-pt, g-fleche, g-vol
"""
import math
import random
from html import escape


def svg(w, h, inner, label):
    return (f'<svg class="graph" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}" '
            f'xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">'
            f'<defs><marker id="fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" class="g-fleche-tete"/></marker></defs>'
            f'{inner}</svg>')


def nice_ticks(lo, hi, n=5):
    span = hi - lo
    if span <= 0:
        return [lo]
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if step >= raw:
            break
    start = math.ceil(lo / step) * step
    ticks, v = [], start
    while v <= hi + 1e-9:
        ticks.append(round(v, 10))
        v += step
    return ticks


def fmt(v, dec=None):
    if dec is None:
        dec = 0 if abs(v) >= 100 or float(v).is_integer() else (2 if abs(v) < 10 else 1)
    s = f"{v:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s


def t(x, y, text, cls="g-txt", anchor="start", size=None, extra=""):
    sz = f' font-size="{size}"' if size else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{sz}{extra}>{escape(str(text))}</text>'


def line(x1, y1, x2, y2, cls, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}"{extra}/>'


def arrow(x1, y1, x2, y2, cls="g-fleche"):
    return line(x1, y1, x2, y2, cls, ' marker-end="url(#fl)"')


# ---------------------------------------------------------------------------
# Données synthétiques
# ---------------------------------------------------------------------------
def path_from(points, seed=1, noise=0.6, wick=0.6, vol_base=None):
    """points : liste de (indice, prix) ; renvoie une liste OHLC interpolée et bruitée."""
    rnd = random.Random(seed)
    closes = []
    for (i0, p0), (i1, p1) in zip(points, points[1:]):
        for i in range(i0, i1):
            f = (i - i0) / (i1 - i0)
            closes.append(p0 + (p1 - p0) * f)
    closes.append(points[-1][1])
    out = []
    prev = closes[0] - (closes[1] - closes[0]) if len(closes) > 1 else closes[0]
    for k, c in enumerate(closes):
        c = c + (rnd.uniform(-noise, noise) if 0 < k < len(closes) - 1 else 0)
        o = prev + rnd.uniform(-noise * 0.3, noise * 0.3)
        hi = max(o, c) + rnd.uniform(0.1, 1) * wick
        lo = min(o, c) - rnd.uniform(0.1, 1) * wick
        out.append((round(o, 6), round(hi, 6), round(lo, 6), round(c, 6)))
        prev = c
    return out


def sma(vals, n):
    res = []
    for i in range(len(vals)):
        res.append(None if i < n - 1 else sum(vals[i - n + 1:i + 1]) / n)
    return res


def ema(vals, n):
    k = 2 / (n + 1)
    res, prev = [], None
    for i, v in enumerate(vals):
        if i < n - 1:
            res.append(None)
        elif i == n - 1:
            prev = sum(vals[:n]) / n
            res.append(prev)
        else:
            prev = v * k + prev * (1 - k)
            res.append(prev)
    return res


# ---------------------------------------------------------------------------
# Graphique en chandeliers
# ---------------------------------------------------------------------------
def candles(ohlc, w=640, h=280, label="Graphique en chandeliers", lines=(), zones=(), marks=(),
            overlays=(), vol=None, ymin=None, ymax=None, style="bougies", legend=(), dec=None,
            xlabels=None):
    L, R, T, B = 8, 52, 14, 22
    vh = (h - T - B) * 0.22 if vol else 0
    ph = h - T - B - vh - (6 if vol else 0)
    lo = min(c[2] for c in ohlc) if ymin is None else ymin
    hi = max(c[1] for c in ohlc) if ymax is None else ymax
    for z in zones:
        lo, hi = min(lo, z["y1"], z["y2"]), max(hi, z["y1"], z["y2"])
    for ln in lines:
        if "y" in ln:
            lo, hi = min(lo, ln["y"]), max(hi, ln["y"])
    pad = (hi - lo) * 0.06
    lo, hi = lo - pad, hi + pad
    n = len(ohlc)
    step = (w - L - R) / n
    cw = max(1.5, step * 0.62)

    def X(i):
        return L + step * (i + 0.5)

    def Y(p):
        return T + (hi - p) / (hi - lo) * ph
    parts = []
    for tk in nice_ticks(lo, hi, 5):
        parts.append(line(L, Y(tk), w - R, Y(tk), "g-grille"))
        parts.append(t(w - R + 4, Y(tk) + 4, fmt(tk, dec), "g-txt g-petit"))
    for z in zones:
        y1, y2 = Y(max(z["y1"], z["y2"])), Y(min(z["y1"], z["y2"]))
        parts.append(f'<rect x="{L}" y="{y1:.1f}" width="{w-L-R}" height="{max(1,y2-y1):.1f}" class="{z.get("cls","g-zone")}"/>')
        if z.get("label"):
            parts.append(t(L + 4, y1 + 12, z["label"], "g-txt g-petit"))
    if style == "ligne":
        pts = " ".join(f"{X(i):.1f},{Y(c[3]):.1f}" for i, c in enumerate(ohlc))
        parts.append(f'<polyline points="{pts}" class="g-l1"/>')
    else:
        for i, (o, hgh, lw, c) in enumerate(ohlc):
            cls = "g-haus" if c >= o else "g-bais"
            x = X(i)
            if style == "barres":
                parts.append(line(x, Y(hgh), x, Y(lw), cls + " g-barre"))
                parts.append(line(x - cw / 2, Y(o), x, Y(o), cls + " g-barre"))
                parts.append(line(x, Y(c), x + cw / 2, Y(c), cls + " g-barre"))
            else:
                parts.append(line(x, Y(hgh), x, Y(lw), cls + " g-meche"))
                top, bot = Y(max(o, c)), Y(min(o, c))
                parts.append(f'<rect x="{x-cw/2:.1f}" y="{top:.1f}" width="{cw:.1f}" height="{max(1.2,bot-top):.1f}" class="{cls}"/>')
    for ov in overlays:
        if "values2" in ov:
            pts_a, pts_b = [], []
            for i, (a, b) in enumerate(zip(ov["values"], ov["values2"])):
                if a is not None and b is not None:
                    pts_a.append(f"{X(i):.1f},{Y(a):.1f}")
                    pts_b.append(f"{X(i):.1f},{Y(b):.1f}")
            if pts_a:
                parts.append(f'<polygon points="{" ".join(pts_a + pts_b[::-1])}" class="{ov.get("cls_fill", "g-zone")}"/>')
            continue
        segs, cur = [], []
        for i, v in enumerate(ov["values"]):
            if v is None:
                if cur:
                    segs.append(cur)
                cur = []
            else:
                cur.append(f"{X(i):.1f},{Y(v):.1f}")
        if cur:
            segs.append(cur)
        for s in segs:
            parts.append(f'<polyline points="{" ".join(s)}" class="{ov.get("cls","g-l2")}"/>')
    for ln in lines:
        cls = ln.get("cls", "g-l3")
        if "y" in ln:
            x1 = X(ln.get("i1", 0)) if "i1" in ln else L
            x2 = X(ln["i2"]) if "i2" in ln else w - R
            parts.append(line(x1, Y(ln["y"]), x2, Y(ln["y"]), cls))
            if ln.get("label"):
                parts.append(t(x2 - 4, Y(ln["y"]) - 5, ln["label"], "g-txt g-petit", "end"))
        else:
            (i1, p1), (i2, p2) = ln["p1"], ln["p2"]
            if ln.get("ext"):
                i3 = ln["ext"]
                p3 = p1 + (p2 - p1) * (i3 - i1) / (i2 - i1)
                i2, p2 = i3, p3
            parts.append(line(X(i1), Y(p1), X(i2), Y(p2), cls))
            if ln.get("label"):
                parts.append(t(X(i2) - 4, Y(p2) - 6, ln["label"], "g-txt g-petit", "end"))
    for mk in marks:
        x, y = X(mk["i"]), Y(mk["p"])
        pos = mk.get("pos", "haut")
        dy = -1 if pos == "haut" else 1
        y0 = y + dy * 34
        if mk.get("fleche", True):
            parts.append(arrow(x, y0 - dy * (-2), x, y + dy * 4))
        parts.append(t(x, y0 + (dy * 4 if pos == "bas" else -4) + (8 if pos == "bas" else 0),
                       mk["t"], "g-txt g-fort", mk.get("anchor", "middle")))
    if vol:
        vmax = max(vol)
        base = h - B
        for i, v in enumerate(vol):
            hh = v / vmax * vh
            cls = "g-vol-h" if ohlc[i][3] >= ohlc[i][0] else "g-vol-b"
            parts.append(f'<rect x="{X(i)-cw/2:.1f}" y="{base-hh:.1f}" width="{cw:.1f}" height="{hh:.1f}" class="{cls}"/>')
        parts.append(t(L + 2, base - vh - 2, "Volume", "g-txt g-petit"))
    parts.append(line(L, h - B, w - R, h - B, "g-axe"))
    if xlabels:
        for i, lab in xlabels:
            parts.append(t(X(i), h - B + 14, lab, "g-txt g-petit", "middle"))
    else:
        parts.append(t((w - R) / 2, h - 6, "Temps →", "g-txt g-petit", "middle"))
    for k, (cls, lab) in enumerate(legend):
        y = T + 4 + k * 15
        parts.append(line(L + 6, y, L + 26, y, cls))
        parts.append(t(L + 30, y + 4, lab, "g-txt g-petit"))
    return svg(w, h, "".join(parts), label)


# ---------------------------------------------------------------------------
# Graphique générique (courbes, barres)
# ---------------------------------------------------------------------------
def plot(series, w=640, h=260, label="Graphique", xr=None, yr=None, xticks=None, yticks=None,
         hlines=(), vlines=(), xlabel="", ylabel="", zones=(), marks=(), legend=True,
         xfmt=None, yfmt=None, texts=(), legend_xy=None):
    L, R, T, B = 52, 16, 16, 34
    xs = [x for s in series for x in s["x"]]
    ys = [y for s in series for y in s["y"] if y is not None]
    x0, x1 = xr or (min(xs), max(xs))
    if yr:
        y0, y1 = yr
    else:
        y0, y1 = min(ys), max(ys)
        pad = (y1 - y0) * 0.08 or 1
        y0, y1 = y0 - pad, y1 + pad

    def X(v):
        return L + (v - x0) / (x1 - x0) * (w - L - R)

    def Y(v):
        return T + (y1 - v) / (y1 - y0) * (h - T - B)
    xf = xfmt or (lambda v: fmt(v))
    yf = yfmt or (lambda v: fmt(v))
    p = []
    for z in zones:
        if "x1" in z:
            p.append(f'<rect x="{X(z["x1"]):.1f}" y="{T}" width="{X(z["x2"])-X(z["x1"]):.1f}" height="{h-T-B}" class="{z.get("cls","g-zone")}"/>')
        else:
            ya, yb = Y(max(z["y1"], z["y2"])), Y(min(z["y1"], z["y2"]))
            p.append(f'<rect x="{L}" y="{ya:.1f}" width="{w-L-R}" height="{yb-ya:.1f}" class="{z.get("cls","g-zone")}"/>')
        if z.get("label"):
            zx = X(z["x1"]) + 4 if "x1" in z else L + 4
            zy = T + 12 if "x1" in z else Y(max(z["y1"], z["y2"])) + 12
            p.append(t(zx, zy, z["label"], "g-txt g-petit"))
    for tk in (yticks if yticks is not None else nice_ticks(y0, y1, 5)):
        p.append(line(L, Y(tk), w - R, Y(tk), "g-grille"))
        p.append(t(L - 6, Y(tk) + 4, yf(tk), "g-txt g-petit", "end"))
    for tk in (xticks if xticks is not None else nice_ticks(x0, x1, 6)):
        p.append(line(X(tk), h - B, X(tk), h - B + 4, "g-axe"))
        p.append(t(X(tk), h - B + 16, xf(tk), "g-txt g-petit", "middle"))
    p.append(line(L, T, L, h - B, "g-axe"))
    p.append(line(L, h - B, w - R, h - B, "g-axe"))
    if y0 < 0 < y1:
        p.append(line(L, Y(0), w - R, Y(0), "g-axe g-zero"))
    for hl in hlines:
        p.append(line(L, Y(hl["y"]), w - R, Y(hl["y"]), hl.get("cls", "g-l3")))
        if hl.get("label"):
            p.append(t(w - R - 4, Y(hl["y"]) - 5, hl["label"], "g-txt g-petit", "end"))
    for vl in vlines:
        p.append(line(X(vl["x"]), T, X(vl["x"]), h - B, vl.get("cls", "g-l3")))
        if vl.get("label"):
            p.append(t(X(vl["x"]) + 4, T + vl.get("ly", 12), vl["label"], "g-txt g-petit"))
    for s in series:
        kind = s.get("kind", "line")
        cls = s.get("cls", "g-l1")
        if kind == "bar":
            bw = s.get("bw", (w - L - R) / max(1, len(s["x"])) * 0.6)
            base = 0 if y0 <= 0 <= y1 else y0
            for x, y in zip(s["x"], s["y"]):
                ya, yb = Y(max(base, y)), Y(min(base, y))
                c = cls if y >= 0 else s.get("cls_neg", cls)
                p.append(f'<rect x="{X(x)-bw/2:.1f}" y="{ya:.1f}" width="{bw:.1f}" height="{max(0.8,yb-ya):.1f}" class="{c}"/>')
        elif kind == "points":
            for x, y in zip(s["x"], s["y"]):
                p.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="3.2" class="{cls}"/>')
        else:
            seg, segs = [], []
            for x, y in zip(s["x"], s["y"]):
                if y is None:
                    if seg:
                        segs.append(seg)
                    seg = []
                else:
                    seg.append(f"{X(x):.1f},{Y(y):.1f}")
            if seg:
                segs.append(seg)
            for sg in segs:
                p.append(f'<polyline points="{" ".join(sg)}" class="{cls}"/>')
    for mk in marks:
        x, y = X(mk["x"]), Y(mk["y"])
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" class="g-pt"/>')
        if mk.get("t"):
            dx = mk.get("dx", 6)
            dy = mk.get("dy", -8)
            p.append(t(x + dx, y + dy, mk["t"], "g-txt g-fort", mk.get("anchor", "start")))
    for tx in texts:
        p.append(t(X(tx["x"]), Y(tx["y"]), tx["t"], tx.get("cls", "g-txt"), tx.get("anchor", "start")))
    if xlabel:
        p.append(t((L + w - R) / 2, h - 4, xlabel, "g-txt g-petit", "middle"))
    if ylabel:
        p.append(f'<text x="12" y="{(T+h-B)/2:.1f}" class="g-txt g-petit" text-anchor="middle" transform="rotate(-90 12 {(T+h-B)/2:.1f})">{escape(ylabel)}</text>')
    if legend:
        k = 0
        lx, ly = legend_xy or (L, T)
        for s in series:
            if s.get("label"):
                y = ly + 6 + k * 15
                if s.get("kind") == "bar":
                    p.append(f'<rect x="{lx+10}" y="{y-5}" width="14" height="9" class="{s.get("cls","g-l1")}"/>')
                else:
                    p.append(line(lx + 8, y, lx + 28, y, s.get("cls", "g-l1")))
                p.append(t(lx + 32, y + 4, s["label"], "g-txt g-petit"))
                k += 1
    return svg(w, h, "".join(p), label)


def table(headers, rows, cls="tableau"):
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tableau-defile"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


# ---------------------------------------------------------------------------
# Indicateurs techniques (calculs réels, utilisés pour les schémas)
# ---------------------------------------------------------------------------
def rsi(closes, n=14):
    """RSI avec lissage de Wilder."""
    res = [None] * len(closes)
    if len(closes) <= n:
        return res
    gains = [max(closes[i] - closes[i - 1], 0) for i in range(1, len(closes))]
    pertes = [max(closes[i - 1] - closes[i], 0) for i in range(1, len(closes))]
    ag, ap = sum(gains[:n]) / n, sum(pertes[:n]) / n
    for i in range(n, len(closes)):
        if i > n:
            ag = (ag * (n - 1) + gains[i - 1]) / n
            ap = (ap * (n - 1) + pertes[i - 1]) / n
        res[i] = 100.0 if ap == 0 else 100 - 100 / (1 + ag / ap)
    return res


def stochastique(ohlc, n=14, d=3):
    k = [None] * len(ohlc)
    for i in range(n - 1, len(ohlc)):
        hh = max(c[1] for c in ohlc[i - n + 1:i + 1])
        ll = min(c[2] for c in ohlc[i - n + 1:i + 1])
        k[i] = 50.0 if hh == ll else (ohlc[i][3] - ll) / (hh - ll) * 100
    dd = [None] * len(ohlc)
    for i in range(len(ohlc)):
        w = k[max(0, i - d + 1):i + 1]
        if len(w) == d and None not in w:
            dd[i] = sum(w) / d
    return k, dd


def bollinger(closes, n=20, m=2):
    mid, up, lo = [None] * len(closes), [None] * len(closes), [None] * len(closes)
    for i in range(n - 1, len(closes)):
        w = closes[i - n + 1:i + 1]
        mu = sum(w) / n
        sd = (sum((x - mu) ** 2 for x in w) / n) ** 0.5  # écart-type de population (convention usuelle)
        mid[i], up[i], lo[i] = mu, mu + m * sd, mu - m * sd
    return mid, up, lo


def atr(ohlc, n=14):
    tr = [ohlc[0][1] - ohlc[0][2]]
    for i in range(1, len(ohlc)):
        h, l, pc = ohlc[i][1], ohlc[i][2], ohlc[i - 1][3]
        tr.append(max(h - l, abs(h - pc), abs(l - pc)))
    res = [None] * len(ohlc)
    if len(ohlc) < n:
        return res
    a = sum(tr[:n]) / n
    res[n - 1] = a
    for i in range(n, len(ohlc)):
        a = (a * (n - 1) + tr[i]) / n
        res[i] = a
    return res


def macd(closes, f=12, s=26, sig=9):
    ef, es = ema(closes, f), ema(closes, s)
    m = [None if a is None or b is None else a - b for a, b in zip(ef, es)]
    first = next(i for i, v in enumerate(m) if v is not None)
    sg = [None] * first + ema(m[first:], sig)
    hist = [None if a is None or b is None else a - b for a, b in zip(m, sg)]
    return m, sg, hist


def correlation(a, b):
    pts = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    cov = sum((x - mx) * (y - my) for x, y in pts)
    vx = sum((x - mx) ** 2 for x, _ in pts)
    vy = sum((y - my) ** 2 for _, y in pts)
    return cov / (vx * vy) ** 0.5


def panneau(series, n, w=640, h=130, yr=(0, 100), hlines=(), label="Indicateur", titre="", yticks=None, dec=None, zones=()):
    """Panneau d'indicateur aligné horizontalement sur candles() (mêmes marges)."""
    L, R, T, B = 8, 52, 16, 8
    step = (w - L - R) / n
    y0, y1 = yr

    def X(i):
        return L + step * (i + 0.5)

    def Y(v):
        return T + (y1 - v) / (y1 - y0) * (h - T - B)
    p = []
    for z in zones:
        ya, yb = Y(max(z["y1"], z["y2"])), Y(min(z["y1"], z["y2"]))
        p.append(f'<rect x="{L}" y="{ya:.1f}" width="{w-L-R}" height="{yb-ya:.1f}" class="{z.get("cls","g-zone")}"/>')
    for tk in (yticks if yticks is not None else nice_ticks(y0, y1, 3)):
        p.append(line(L, Y(tk), w - R, Y(tk), "g-grille"))
        p.append(t(w - R + 4, Y(tk) + 4, fmt(tk, dec), "g-txt g-petit"))
    for hl in hlines:
        p.append(line(L, Y(hl["y"]), w - R, Y(hl["y"]), hl.get("cls", "g-l3")))
    for s in series:
        if s.get("kind") == "bar":
            bw = step * 0.6
            for i, v in enumerate(s["values"]):
                if v is None:
                    continue
                ya, yb = Y(max(0, v)), Y(min(0, v))
                c = s.get("cls", "g-barre-h") if v >= 0 else s.get("cls_neg", "g-barre-b")
                p.append(f'<rect x="{X(i)-bw/2:.1f}" y="{ya:.1f}" width="{bw:.1f}" height="{max(0.6, yb-ya):.1f}" class="{c}"/>')
        else:
            segs, cur = [], []
            for i, v in enumerate(s["values"]):
                if v is None:
                    if cur:
                        segs.append(cur)
                    cur = []
                else:
                    cur.append(f"{X(i):.1f},{Y(v):.1f}")
            if cur:
                segs.append(cur)
            for sg in segs:
                p.append(f'<polyline points="{" ".join(sg)}" class="{s.get("cls","g-l1")}"/>')
    p.append(line(L, h - B, w - R, h - B, "g-axe"))
    x = L + 4
    if titre:
        p.append(t(x, T - 4, titre, "g-txt g-fort"))
    return svg(w, h, "".join(p), label)
