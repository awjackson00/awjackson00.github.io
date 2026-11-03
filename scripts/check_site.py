"""Validate built Quarto HTML, avoiding a regression where HTML appears as literal code."""
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlparse, unquote

ROOT = Path("_site")
PAGES = {
    "index.html": ("landing-hero", "feature-grid", "home-closer"),
    "projects.html": ("portfolio-grid", "filter-row", "portfolio-card"),
    "projects/pairname.html": ("case-shell", "case-content"),
    "projects/risky-business.html": ("case-shell", "case-content"),
    "projects/prague-metro.html": ("case-shell", "case-content"),
    "projects/marion-berries.html": ("case-shell", "case-content"),
    "projects/infrastructure.html": ("case-shell", "case-content"),
}

class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.classes = set()
        self.assets = []
        self.links = []
        self.raw_markup_in_text = []
        self.headings = 0
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.classes.update(d.get("class", "").split())
        if tag in ("h1", "h2", "h3"):
            self.headings += 1
        if tag == "img" and d.get("src"):
            self.assets.append(d["src"])
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])
    def handle_data(self, data):
        if re.search(r"<(?:div|section|article|header|figure)\b", data, re.I):
            self.raw_markup_in_text.append(data[:90])

errors = []
for relative, expected in PAGES.items():
    page = ROOT / relative
    if not page.exists():
        errors.append(f"Missing page: {relative}")
        continue
    raw = page.read_text(encoding="utf-8")
    checker = Checker()
    checker.feed(raw)
    for required in expected:
        if required not in checker.classes:
            errors.append(f"{relative}: missing expected class {required}")
    if relative == "index.html" and "impact-strip" in checker.classes:
        errors.append("Homepage still contains the removed impact strip")
    if checker.raw_markup_in_text or re.search(r"&lt;(?:div|section|article)\b", raw):
        errors.append(f"{relative}: visible literal HTML instead of rendered markup")
    if checker.headings < 2:
        errors.append(f"{relative}: suspiciously few rendered headings")
    for target in checker.assets + checker.links:
        parsed = urlparse(target)
        if parsed.scheme or parsed.netloc or target.startswith(("#", "mailto:", "tel:", "//")):
            continue
        asset = unquote(parsed.path)
        resolved = ROOT / asset.lstrip("/") if asset.startswith("/") else page.parent / asset
        if not resolved.is_file() and not resolved.is_dir():
            errors.append(f"{relative}: missing local resource {target}")
    print(f"Checked {relative}: {len(checker.classes)} classes, {len(checker.assets)} images, {len(checker.links)} links")
if errors:
    raise SystemExit("\n".join(errors))
print("PASS: rendered HTML blocks and local project links/assets verified.")
