#!/usr/bin/env python3
"""Générateur du site « Formation Trading ».

Usage : python3 _source/build.py
Les pages produites vont dans formation-trading/ (site statique autonome).
Les fichiers CSS/JS écrits à la main sont dans formation-trading/assets/
et ne sont pas touchés par ce script (sauf les fichiers de données générés).
"""
import html
import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "formation-trading"
sys.path.insert(0, str(SRC))

SITE = "Formation Trading"

CATS = {
    "marches": "Marchés",
    "ordres": "Ordres",
    "produits": "Produits",
    "technique": "Analyse technique",
    "fondamentale": "Analyse fondamentale",
    "risque": "Gestion du risque",
    "psychologie": "Psychologie",
    "reglementation": "Réglementation & fiscalité",
    "jargon": "Jargon & abréviations",
}

WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def esc(s):
    return html.escape(s, quote=True)


# --------------------------------------------------------------------------
# Glossaire
# --------------------------------------------------------------------------
def load_glossary():
    path = SRC / "glossaire.txt"
    if not path.exists():
        return []
    entries, cur = [], None
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.rstrip()
        if not line or line.startswith("%"):
            continue
        if line.startswith("## "):
            parts = [p.strip() for p in line[3:].split("|")]
            if len(parts) < 3:
                sys.exit(f"glossaire.txt:{n} en-tête invalide")
            cur = dict(slug=parts[0], terme=parts[1], cat=parts[2],
                       en=parts[3] if len(parts) > 3 else "",
                       alias=None, d="", e="", v=[])
            if cur["cat"] not in CATS:
                sys.exit(f"glossaire.txt:{n} catégorie inconnue {cur['cat']}")
            entries.append(cur)
        elif cur is None:
            sys.exit(f"glossaire.txt:{n} ligne hors entrée")
        elif line.startswith("= "):
            v = line[2:].strip()
            cur["alias"] = [] if v == "-" else [a.strip() for a in v.split(";") if a.strip()]
        elif line.startswith("D: "):
            cur["d"] = line[3:].strip()
        elif line.startswith("E: "):
            cur["e"] = line[3:].strip()
        elif line.startswith("V: "):
            cur["v"] = [a.strip() for a in line[3:].split(",") if a.strip()]
        else:
            sys.exit(f"glossaire.txt:{n} ligne non reconnue : {line[:40]}")
    slugs = {}
    for e in entries:
        if e["slug"] in slugs:
            sys.exit(f"slug en double : {e['slug']}")
        slugs[e["slug"]] = e
        if e["alias"] is None:
            e["alias"] = [re.sub(r"\s*\(.*?\)", "", e["terme"]).strip()]
        if not e["d"] or not e["e"]:
            warn(f"glossaire : définition ou exemple manquant pour {e['slug']}")
    for e in entries:
        for v in e["v"]:
            if v not in slugs:
                warn(f"glossaire : {e['slug']} renvoie vers {v} inexistant")
    return entries


GLOSS = load_glossary()
GSLUG = {e["slug"]: e for e in GLOSS}
USAGE = {}  # slug -> set(module num)

# Expression régulière d'auto-lien : alias triés du plus long au plus court
_alias = []
for e in GLOSS:
    for a in e["alias"]:
        _alias.append((a, e["slug"]))
_alias.sort(key=lambda x: -len(x[0]))
ALIAS_CI = {}   # alias normalisé -> slug (insensible à la casse)
ALIAS_CS = {}   # alias exact -> slug (sigles en majuscules)
_pat_ci, _pat_cs = [], []
for a, s in _alias:
    is_acr = len(a) > 1 and a.upper() == a and any(c.isalpha() for c in a)
    if is_acr:
        ALIAS_CS[a] = s
        _pat_cs.append(re.escape(a))
    else:
        ALIAS_CI[a.lower()] = s
        _pat_ci.append(re.escape(a))
B_L, B_R = r"(?<![\w\-])", r"(?:s|x)?(?![\w\-])"
RE_CI = re.compile(B_L + "(" + "|".join(_pat_ci) + ")" + B_R, re.I) if _pat_ci else None
RE_CS = re.compile(B_L + "(" + "|".join(_pat_cs) + ")" + B_R) if _pat_cs else None

SKIP_TAGS = {"a", "h1", "h2", "h3", "h4", "button", "script", "style", "svg",
             "summary", "code", "pre", "label", "th", "title", "figcaption"}
VOID = {"br", "hr", "img", "input", "meta", "link", "col", "wbr", "source"}


def term_link(text, slug, prefix, module):
    if slug not in GSLUG:
        warn(f"module {module}: terme de glossaire inconnu « {slug} »")
        return text
    USAGE.setdefault(slug, set()).add(module)
    d = esc(GSLUG[slug]["d"])
    return (f'<a class="terme" href="{prefix}glossaire.html#{slug}" '
            f'data-terme="{slug}" title="{d}">{text}</a>')


def autolink(fragment, prefix, module, linked):
    """Lie la première occurrence de chaque terme du glossaire (par leçon)."""
    # liens manuels [[texte|slug]] ou [[texte]]
    def manual(m):
        text, slug = m.group(1), m.group(2)
        if not slug:
            slug = ALIAS_CI.get(text.lower()) or ALIAS_CS.get(text) or slugify(text)
        linked.add(slug)
        return term_link(text, slug, prefix, module)
    fragment = re.sub(r"\[\[([^\]|]+?)(?:\|([a-z0-9\-]+))?\]\]", manual, fragment)
    if not GLOSS:
        return fragment
    parts = re.split(r"(<[^>]+>)", fragment)
    depth = 0
    stack = []
    out = []
    for p in parts:
        if p.startswith("<"):
            m = re.match(r"<\s*(/?)\s*([a-zA-Z0-9\-]+)", p)
            if m and not p.startswith("<!"):
                closing, tag = m.group(1) == "/", m.group(2).lower()
                selfclose = p.endswith("/>") or tag in VOID
                if tag in SKIP_TAGS and not selfclose:
                    if closing:
                        if stack and stack[-1] == tag:
                            stack.pop()
                            depth -= 1
                    else:
                        stack.append(tag)
                        depth += 1
            out.append(p)
            continue
        if depth or not p.strip():
            out.append(p)
            continue
        out.append(_link_text(p, prefix, module, linked))
    return "".join(out)


def _link_text(text, prefix, module, linked):
    matches = []
    for rx, table, ci in ((RE_CI, ALIAS_CI, True), (RE_CS, ALIAS_CS, False)):
        if not rx:
            continue
        for m in rx.finditer(text):
            key = m.group(1).lower() if ci else m.group(1)
            slug = table.get(key)
            if slug:
                matches.append((m.start(), m.end(), slug))
    matches.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    res, pos = [], 0
    for s, e, slug in matches:
        if s < pos or slug in linked:
            continue
        linked.add(slug)
        res.append(text[pos:s])
        res.append(term_link(text[s:e], slug, prefix, module))
        pos = e
    res.append(text[pos:])
    return "".join(res)


def slugify(s):
    s = norm(s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


# --------------------------------------------------------------------------
# Blocs pédagogiques personnalisés
# --------------------------------------------------------------------------
BLOCKS = {
    "x-obj": ("bloc bloc-obj", "🎯 Objectifs de la leçon"),
    "x-simple": ("bloc bloc-simple", "💡 L'explication simple"),
    "x-approfondi": ("bloc bloc-approfondi", "🔬 Explication approfondie"),
    "x-exemple": ("bloc bloc-exemple", "🧮 Exemple chiffré pas à pas"),
    "x-erreurs": ("bloc bloc-erreurs", "⚠️ Erreurs fréquentes des débutants"),
    "x-cles": ("bloc bloc-cles", "📌 Points clés à retenir"),
    "x-exo": ("bloc bloc-exo", "✍️ Exercice pratique"),
    "x-note": ("bloc bloc-note", "🔍 Nuance : ce qui est débattu ou approximatif"),
    "x-attention": ("bloc bloc-attention", "🚨 Attention"),
    "x-info": ("bloc bloc-info", "ℹ️ Bon à savoir"),
}


def check_blocks(s, where):
    for tag in list(BLOCKS) + ["x-corr", "x-fig"]:
        o = len(re.findall(rf"<{tag}[\s>]", s))
        c = s.count(f"</{tag}>")
        if o != c:
            warn(f"{where} : balise {tag} ouverte {o} fois, fermée {c} fois")


def expand_blocks(s):
    def open_block(m):
        tag, attrs = m.group(1), m.group(2) or ""
        cls, title = BLOCKS[tag]
        t = re.search(r'\bt="([^"]*)"', attrs)
        if t:
            title = t.group(1)
        return f'<div class="{cls}"><h3 class="bloc-titre">{title}</h3>'
    names = "|".join(BLOCKS)
    s = re.sub(rf"<({names})(\s[^>]*)?>", open_block, s)
    s = re.sub(rf"</({names})>", "</div>", s)
    s = re.sub(r"<x-corr>",
               '<button type="button" class="btn btn-corr" aria-expanded="false">'
               'Voir la correction</button><div class="correction" hidden>', s)
    s = s.replace("</x-corr>", "</div>")

    def fig(m):
        cap = m.group(1)
        return f'<figure class="schema">'
    s = re.sub(r'<x-fig c="([^"]*)">',
               lambda m: f'<figure class="schema" data-cap="{m.group(1)}">', s)

    def close_fig(s):
        # remplace </x-fig> par figcaption + </figure> en retrouvant la légende
        out, stack = [], []
        for part in re.split(r'(<figure class="schema" data-cap="[^"]*">|</x-fig>)', s):
            m = re.match(r'<figure class="schema" data-cap="([^"]*)">', part)
            if m:
                stack.append(m.group(1))
                out.append('<figure class="schema">')
            elif part == "</x-fig>":
                cap = stack.pop()
                out.append(f"<figcaption>{cap}</figcaption></figure>")
            else:
                out.append(part)
        return "".join(out)
    return close_fig(s)


# --------------------------------------------------------------------------
# Gabarit de page
# --------------------------------------------------------------------------
MODULES = []


def load_modules():
    for f in sorted((SRC / "modules").glob("m[0-9][0-9].py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        MODULES.append(mod)


FOOTER = """<footer class="pied">
<p><strong>Avertissement sur les risques.</strong> Le trading d'instruments financiers comporte un risque élevé de perte en capital. Les produits à effet de levier (CFD, Forex, futures, options, turbos, warrants…) peuvent faire perdre très rapidement tout le capital engagé, et certains produits (futures, vente d'options, vente à découvert) peuvent entraîner des pertes supérieures à la mise initiale. Une majorité de particuliers perd de l'argent en tradant des CFD. Ce site est un support pédagogique général : il ne constitue ni un conseil en investissement, ni une recommandation personnalisée, ni une incitation à acheter ou vendre un instrument financier. Les performances passées ne préjugent pas des performances futures. N'investissez que de l'argent dont la perte n'affecterait pas votre niveau de vie.</p>
<p class="pied-liens"><a href="{p}a-propos.html">À propos &amp; sources</a> · <a href="{p}glossaire.html">Glossaire</a> · Contenu à jour à la date de rédaction : vérifiez toujours les règles en vigueur (AMF, impots.gouv.fr).</p>
</footer>"""


def sidebar(p, active):
    def item(href, label, key, extra=""):
        cur = ' aria-current="page"' if key == active else ""
        return f'<li{extra}><a href="{p}{href}"{cur}>{label}</a></li>'
    mods = "".join(
        item(f"modules/module-{m.NUM:02d}.html",
             f'<span class="num">{m.NUM}</span><span class="lib">{esc(m.TITRE)}</span><span class="etat" aria-hidden="true"></span>',
             f"m{m.NUM:02d}", f' data-module="{m.NUM:02d}"')
        for m in MODULES)
    return f"""<nav class="sidebar" id="sidebar" aria-label="Menu principal">
<p class="nav-titre">Démarrer</p><ul>
{item("index.html", "🏠 Accueil &amp; progression", "index")}
{item("a-propos.html", "ℹ️ À propos &amp; méthode", "apropos")}
</ul>
<p class="nav-titre">Modules</p><ul class="nav-modules">{mods}</ul>
<p class="nav-titre">S'entraîner</p><ul>
{item("outils.html", "🧮 Calculateurs &amp; simulateur", "outils")}
{item("journal-de-trading.html", "📓 Journal de trading", "journal")}
{item("examen-final.html", "🎓 Examen final (40 questions)", "examen")}
</ul>
<p class="nav-titre">Référence</p><ul>
{item("glossaire.html", "📖 Glossaire", "glossaire")}
</ul>
</nav>"""


def layout(title, body, depth=0, active="", scripts=(), body_class="", desc=""):
    p = "../" * depth
    scr = "\n".join(f'<script src="{p}{s}"></script>' for s in scripts)
    desc = desc or "Formation complète et gratuite pour apprendre le trading, du niveau débutant au niveau intermédiaire."
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · {SITE}</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="{p}assets/css/style.css">
<link rel="stylesheet" href="{p}assets/css/print.css" media="print">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3' fill='%231f5f8b'/%3E%3Cpath d='M3 11l3-3 2 2 5-5' stroke='white' stroke-width='1.8' fill='none'/%3E%3C/svg%3E">
<script>try{{var t=localStorage.getItem("ft-theme");if(t)document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}</script>
</head>
<body class="{body_class}" data-root="{p}">
<a class="evitement" href="#contenu">Aller au contenu</a>
<header class="barre">
<button type="button" class="btn-menu" aria-controls="sidebar" aria-expanded="false" aria-label="Ouvrir le menu">☰</button>
<a class="logo" href="{p}index.html"><span class="logo-icone" aria-hidden="true">📈</span> {SITE}</a>
<div class="barre-actions">
<a class="barre-lien" href="{p}glossaire.html" title="Glossaire">📖<span class="sr"> Glossaire</span></a>
<button type="button" class="btn-theme" aria-label="Basculer le mode sombre" title="Mode clair / sombre">◐</button>
</div>
</header>
<div class="cadre">
{sidebar(p, active)}
<div class="voile" hidden></div>
<div class="colonne">
<main id="contenu" class="contenu" tabindex="-1">
{body}
</main>
{FOOTER.format(p=p)}
</div>
</div>
<script src="{p}assets/js/nav-data.js"></script>
<script src="{p}assets/js/app.js"></script>
{scr}
</body>
</html>
"""


def write(rel, content):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# --------------------------------------------------------------------------
# Pages de modules, quiz et fiches
# --------------------------------------------------------------------------
def prevnext(i, kind):
    def href(m):
        return {"module": f"module-{m.NUM:02d}.html", "quiz": f"quiz-{m.NUM:02d}.html",
                "fiche": f"fiche-{m.NUM:02d}.html"}[kind]
    prev = MODULES[i - 1] if i > 0 else None
    nxt = MODULES[i + 1] if i + 1 < len(MODULES) else None
    a = (f'<a class="pn pn-prec" href="{href(prev)}"><small>← Précédent</small>'
         f'<span>Module {prev.NUM} · {esc(prev.TITRE)}</span></a>') if prev else "<span></span>"
    b = (f'<a class="pn pn-suiv" href="{href(nxt)}"><small>Suivant →</small>'
         f'<span>Module {nxt.NUM} · {esc(nxt.TITRE)}</span></a>') if nxt else "<span></span>"
    return f'<nav class="precsuiv" aria-label="Navigation entre modules">{a}{b}</nav>'


def build_module(i, m):
    num = f"{m.NUM:02d}"
    toc, secs = [], []
    for j, (lid, titre, body) in enumerate(m.LECONS, 1):
        sid = f"lecon-{m.NUM}-{j}"
        toc.append(f'<li><a href="#{sid}">{m.NUM}.{j} {esc(titre)}</a></li>')
        check_blocks(body, f"leçon {m.NUM}.{j}")
        body = expand_blocks(body)
        body = autolink(body, "../", m.NUM, set())
        secs.append(f'<section class="lecon" id="{sid}">\n<h2><span class="lecon-num">{m.NUM}.{j}</span> {esc(titre)}</h2>\n{body}\n</section>')
    intro = autolink(expand_blocks(m.INTRO), "../", m.NUM, set())
    body = f"""<article class="module" data-module="{num}">
<p class="fil"><a href="../index.html">Accueil</a> › Module {m.NUM}</p>
<header class="module-entete">
<p class="surtitre">Module {m.NUM} · {len(m.LECONS)} leçons · ≈ {m.DUREE}</p>
<h1>{esc(m.TITRE)}</h1>
<div class="chapeau">{intro}</div>
</header>
<nav class="sommaire" aria-label="Sommaire du module"><h2>Sommaire</h2><ol>{''.join(toc)}</ol></nav>
{''.join(secs)}
<section class="fin-module">
<h2>Fin du module {m.NUM}</h2>
<p>Vous avez terminé la lecture ? Marquez le module comme lu, puis vérifiez vos acquis avec le quiz.</p>
<div class="actions">
<button type="button" class="btn btn-principal btn-lu" data-module="{num}">✓ Marquer ce module comme lu</button>
<a class="btn" href="../quiz/quiz-{num}.html">📝 Faire le quiz ({len(m.QUIZ)} questions)</a>
<a class="btn" href="../fiches/fiche-{num}.html">🗂️ Fiche récapitulative</a>
</div>
</section>
{prevnext(i, "module")}
</article>"""
    write(f"modules/module-{num}.html",
          layout(f"Module {m.NUM} — {m.TITRE}", body, 1, f"m{num}",
                 ["assets/js/glossaire-data.js", "assets/js/glossaire-infobulle.js"],
                 "page-module", m.INTRO_TXT if hasattr(m, "INTRO_TXT") else ""))


def quiz_js(qid, titre, questions, retour):
    data = {"id": qid, "titre": titre, "retour": retour,
            "questions": [{"q": q[0], "c": q[1], "a": q[2], "e": q[3],
                           **({"t": q[4]} if len(q) > 4 else {})} for q in questions]}
    for k, q in enumerate(data["questions"]):
        if not (0 <= q["a"] < len(q["c"])):
            sys.exit(f"{qid} question {k+1}: index de réponse invalide")
    return "window.QUIZ = " + json.dumps(data, ensure_ascii=False, indent=0) + ";\n"


def build_quiz(i, m):
    num = f"{m.NUM:02d}"
    write(f"assets/js/quiz-data/q{num}.js",
          quiz_js(f"q{num}", f"Quiz du module {m.NUM} — {m.TITRE}", m.QUIZ,
                  f"../modules/module-{num}.html"))
    body = f"""<article class="page-quiz">
<p class="fil"><a href="../index.html">Accueil</a> › <a href="../modules/module-{num}.html">Module {m.NUM}</a> › Quiz</p>
<h1>Quiz · Module {m.NUM} — {esc(m.TITRE)}</h1>
<p class="chapeau">{len(m.QUIZ)} questions à choix multiple. Une seule bonne réponse par question. Validez à la fin pour voir la correction détaillée. Votre meilleur score est enregistré sur cet appareil.</p>
<div id="quiz" class="quiz"><noscript><p>Le quiz nécessite JavaScript.</p></noscript></div>
{prevnext(i, "quiz")}
</article>"""
    write(f"quiz/quiz-{num}.html",
          layout(f"Quiz module {m.NUM}", body, 1, f"m{num}",
                 [f"assets/js/quiz-data/q{num}.js", "assets/js/quiz-engine.js"], "page-quiz"))


def build_fiche(i, m):
    num = f"{m.NUM:02d}"
    body = f"""<article class="fiche">
<p class="fil ecran"><a href="../index.html">Accueil</a> › <a href="../modules/module-{num}.html">Module {m.NUM}</a> › Fiche</p>
<div class="fiche-outils ecran"><button type="button" class="btn btn-principal" onclick="window.print()">🖨️ Imprimer / PDF</button>
<a class="btn" href="../modules/module-{num}.html">← Revenir au module</a></div>
<header class="fiche-entete"><p class="surtitre">Fiche récapitulative · Module {m.NUM}</p><h1>{esc(m.TITRE)}</h1></header>
<div class="fiche-corps">{expand_blocks(m.FICHE)}</div>
<p class="fiche-pied">{SITE} — support pédagogique, pas un conseil en investissement. Le trading comporte un risque élevé de perte en capital.</p>
{prevnext(i, "fiche")}
</article>"""
    write(f"fiches/fiche-{num}.html",
          layout(f"Fiche module {m.NUM}", body, 1, f"m{num}", [], "page-fiche"))


# --------------------------------------------------------------------------
# Glossaire
# --------------------------------------------------------------------------
def build_glossary():
    data = {e["slug"]: {"t": e["terme"], "d": e["d"], "c": e["cat"], "en": e["en"]} for e in GLOSS}
    write("assets/js/glossaire-data.js",
          "window.GLOSSAIRE = " + json.dumps(data, ensure_ascii=False) + ";\n")
    entries = sorted(GLOSS, key=lambda e: norm(e["terme"]))
    groups = {}
    for e in entries:
        L = norm(e["terme"])[0].upper()
        if not L.isalpha():
            L = "#"
        groups.setdefault(L, []).append(e)
    chips = "".join(f'<button type="button" class="puce" data-cat="{k}" aria-pressed="false">{v} <span class="compte">{sum(1 for e in GLOSS if e["cat"]==k)}</span></button>'
                    for k, v in CATS.items())
    letters = "".join(f'<a href="#lettre-{L}">{L}</a>' for L in groups)
    html_groups = []
    for L, es in groups.items():
        arts = []
        for e in es:
            voir = ", ".join(f'<a href="#{v}">{esc(GSLUG[v]["terme"])}</a>' for v in e["v"] if v in GSLUG)
            used = sorted(USAGE.get(e["slug"], []))
            usage = ", ".join(f'<a href="modules/module-{u:02d}.html">Module {u}</a>' for u in used)
            search = esc(norm(" ".join([e["terme"], e["en"], e["d"], " ".join(e["alias"])])))
            arts.append(f"""<article class="entree" id="{e['slug']}" data-cat="{e['cat']}" data-recherche="{search}">
<h3>{esc(e['terme'])}{f' <span class="en" lang="en">{esc(e["en"])}</span>' if e['en'] else ''}</h3>
<p class="cat-badge cat-{e['cat']}">{CATS[e['cat']]}</p>
<p class="def">{e['d']}</p>
<p class="ex"><strong>Exemple :</strong> {e['e']}</p>
{f'<p class="voir"><strong>Voir aussi :</strong> {voir}</p>' if voir else ''}
{f'<p class="usage"><strong>Vu dans :</strong> {usage}</p>' if usage else ''}
</article>""")
        html_groups.append(f'<section class="lettre" id="lettre-{L}"><h2>{L}</h2>{"".join(arts)}</section>')
    body = f"""<article class="glossaire">
<p class="fil"><a href="index.html">Accueil</a> › Glossaire</p>
<h1>Glossaire du trading</h1>
<p class="chapeau">{len(GLOSS)} termes expliqués simplement, avec un exemple, l'équivalent anglais (le jargon des marchés est très largement anglophone) et les termes associés. La recherche ignore les accents et cherche aussi dans les définitions.</p>
<div class="glo-outils">
<label class="sr" for="glo-recherche">Rechercher un terme</label>
<input type="search" id="glo-recherche" placeholder="Rechercher : levier, spread, RSI, drawdown…" autocomplete="off">
<div class="puces" role="group" aria-label="Filtrer par catégorie"><button type="button" class="puce actif" data-cat="" aria-pressed="true">Toutes <span class="compte">{len(GLOSS)}</span></button>{chips}</div>
<p class="glo-compte" id="glo-compte" aria-live="polite"></p>
<nav class="lettres" aria-label="Accès par lettre">{letters}</nav>
</div>
<div id="glo-liste">{''.join(html_groups)}</div>
<p id="glo-vide" class="vide" hidden>Aucun terme ne correspond. Essayez un mot plus court ou une autre catégorie.</p>
</article>"""
    write("glossaire.html", layout("Glossaire", body, 0, "glossaire",
                                   ["assets/js/glossaire.js"], "page-glossaire"))


# --------------------------------------------------------------------------
# Pages simples
# --------------------------------------------------------------------------
def build_index():
    cards = []
    for m in MODULES:
        num = f"{m.NUM:02d}"
        cards.append(f"""<li class="carte-module{' central' if m.NUM == 9 else ''}" data-module="{num}">
<a class="carte-lien" href="modules/module-{num}.html">
<span class="carte-num">Module {m.NUM}</span>
<span class="carte-titre">{esc(m.TITRE)}</span>
<span class="carte-desc">{esc(m.RESUME)}</span>
</a>
<div class="carte-pied"><span class="carte-meta">{len(m.LECONS)} leçons · ≈ {m.DUREE}</span>
<span class="carte-etat" aria-live="polite"></span></div>
<div class="carte-liens"><a href="quiz/quiz-{num}.html">Quiz</a><a href="fiches/fiche-{num}.html">Fiche</a></div>
</li>""")
    intro = (SRC / "pages" / "index.html").read_text(encoding="utf-8")
    body = intro.replace("{{MODULES}}", "".join(cards)).replace("{{NB_TERMES}}", str(len(GLOSS)))
    body = body.replace("{{NB_QUESTIONS}}", str(sum(len(m.QUIZ) for m in MODULES)))
    write("index.html", layout("Accueil", body, 0, "index", [], "page-accueil"))
    nav = [{"n": m.NUM, "id": f"{m.NUM:02d}", "titre": m.TITRE,
            "href": f"modules/module-{m.NUM:02d}.html",
            "quiz": f"quiz/quiz-{m.NUM:02d}.html", "nbq": len(m.QUIZ)} for m in MODULES]
    write("assets/js/nav-data.js", "window.FT_MODULES = " + json.dumps(nav, ensure_ascii=False) + ";\n")


def build_page(name, out, title, active, scripts=(), cls="", link_terms=False):
    body = (SRC / "pages" / name).read_text(encoding="utf-8")
    body = expand_blocks(body)
    if link_terms:
        body = autolink(body, "", -1, set())
    write(out, layout(title, body, 0, active, scripts, cls))


def build_exam():
    spec = importlib.util.spec_from_file_location("exam", SRC / "exam.py")
    ex = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ex)
    if len(ex.QUESTIONS) != 40:
        warn(f"examen : {len(ex.QUESTIONS)} questions au lieu de 40")
    write("assets/js/quiz-data/examen.js",
          quiz_js("examen", "Examen final", ex.QUESTIONS, "index.html"))
    body = (SRC / "pages" / "examen.html").read_text(encoding="utf-8")
    write("examen-final.html", layout("Examen final", body, 0, "examen",
          ["assets/js/quiz-data/examen.js", "assets/js/quiz-engine.js"], "page-quiz"))


def main():
    load_modules()
    for i, m in enumerate(MODULES):
        build_module(i, m)
        build_quiz(i, m)
        build_fiche(i, m)
    build_index()
    build_page("a-propos.html", "a-propos.html", "À propos & méthode", "apropos")
    build_page("outils.html", "outils.html", "Calculateurs & simulateur", "outils",
               ["assets/js/calculateurs.js", "assets/js/simulateur.js"], "page-outils")
    build_page("journal.html", "journal-de-trading.html", "Journal de trading", "journal",
               ["assets/js/journal.js"], "page-journal")
    if (SRC / "exam.py").exists():
        build_exam()
    build_glossary()  # en dernier : utilise USAGE
    print(f"{len(MODULES)} modules, {len(GLOSS)} termes, "
          f"{sum(len(m.QUIZ) for m in MODULES)} questions de quiz.")
    unused = [e["slug"] for e in GLOSS if e["slug"] not in USAGE]
    print(f"Termes du glossaire jamais liés depuis un module : {len(unused)}")
    for w in WARNINGS:
        print("ATTENTION :", w)


if __name__ == "__main__":
    main()
