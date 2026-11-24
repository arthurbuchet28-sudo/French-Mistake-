#!/usr/bin/env python3
"""Vérifications : liens et ancres internes, sigles non définis dans le glossaire."""
import re, sys, html
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "formation-trading"
pages = list(OUT.rglob("*.html"))
ids = {}
for p in pages:
    ids[p.resolve()] = set(re.findall(r'\bid="([^"]+)"', p.read_text(encoding="utf-8")))
errs = 0
nliens = 0
for p in pages:
    t = p.read_text(encoding="utf-8")
    for attr, url in re.findall(r'\b(href|src)="([^"]+)"', t):
        if url.startswith(("http", "mailto:", "data:", "javascript:")):
            continue
        nliens += 1
        path, _, anchor = url.partition("#")
        target = (p.parent / path).resolve() if path else p.resolve()
        if not target.exists():
            print(f"LIEN CASSÉ {p.relative_to(OUT)} → {url}"); errs += 1; continue
        if anchor and target.suffix == ".html" and anchor not in ids.get(target, set()):
            print(f"ANCRE ABSENTE {p.relative_to(OUT)} → {url}"); errs += 1
print(f"{len(pages)} pages, {nliens} liens internes vérifiés, {errs} erreur(s)")

# Sigles présents dans le texte des leçons mais inconnus du glossaire
gl = (OUT.parent / "_source" / "glossaire.txt").read_text(encoding="utf-8")
connus = set(re.findall(r"\b[A-Z][A-Za-z&]*[A-Z]\b", gl))
ignores = {"UE", "EEE", "OK", "II", "XIX", "USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "NZD", "TRY", "ZAR",
           "SH", "CH", "SPIVA", "BRI", "CFTC", "IFRS", "GAAP", "PACTE", "PHAROS", "CBOE", "GR", "NR", "DE", "LA"}
manquants = {}
for p in sorted((OUT / "modules").glob("*.html")):
    t = re.sub(r"<(svg|script|style)[\s\S]*?</\1>", " ", p.read_text(encoding="utf-8"))
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    for s in set(re.findall(r"\b[A-Z][A-Z0-9&]{1,}\b", t)):
        if s not in connus and s not in ignores and not s.isdigit() and not re.fullmatch(r"[A-Z]\d+", s):
            manquants.setdefault(s, []).append(p.stem)
for s, m in sorted(manquants.items()):
    print("SIGLE HORS GLOSSAIRE :", s, m[:4])
sys.exit(1 if errs else 0)
