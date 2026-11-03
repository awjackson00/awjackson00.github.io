"""Capture real, anonymous browser screenshots of the two public project sites."""
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from PIL import Image
import json

TARGETS = [
    ("PairName", "https://pairname.awjackson00.workers.dev/", "images/projects/pairname-website.png", "pairname.awjackson00.workers.dev"),
    ("Risky Business", "https://awjackson00.github.io/Risky-Business/", "images/projects/risky-business-website.png", "awjackson00.github.io"),
]
Path("images/projects").mkdir(parents=True, exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(
        viewport={"width": 1440, "height": 810},
        device_scale_factor=1,
        color_scheme="light",
        reduced_motion="reduce",
        locale="en-US"
    )
    context.set_default_timeout(30000)
    for name, url, path, host in TARGETS:
        page = context.new_page()
        response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
        if response is None or response.status >= 400:
            raise RuntimeError(f"{name} returned status {response.status if response else 'none'}")
        try:
            page.wait_for_load_state("networkidle", timeout=18000)
        except PlaywrightTimeout:
            pass  # Some live applications keep connections open for realtime updates.
        page.wait_for_timeout(1600)
        title = page.title()
        body = page.locator("body").inner_text(timeout=20000)
        if len(body.strip()) < 24:
            raise RuntimeError(f"{name}: page body unexpectedly empty")
        if any(term in body.lower() for term in ("this site can’t be reached", "this site can't be reached", "404 file not found", "502 bad gateway", "access denied")):
            raise RuntimeError(f"{name}: site seems to show an error page")
        if host not in page.url:
            raise RuntimeError(f"{name}: unexpectedly redirected to {page.url}")
        page.screenshot(path=path, type="png", full_page=False, animations="disabled")
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            if image.size != (1440, 810):
                raise RuntimeError(f"{name}: unexpected viewport {image.size}")
        print(json.dumps({"name":name,"title":title,"url":page.url,"http":response.status,"screenshot":path,"bytes":Path(path).stat().st_size,"body_preview":body[:180]}))
        page.close()
    browser.close()

# Download the authentic, unmodified 2026 Prague Metro station map with attribution.
# Source: Tomáš Vojtíšek, based on Bilykralik16's map; Wikimedia Commons, CC BY-SA 4.0.
import hashlib
from urllib.request import Request, urlopen

map_url = "https://upload.wikimedia.org/wikipedia/commons/c/cb/Prague_metro_plan_2026.svg"
request = Request(map_url, headers={"User-Agent": "AlexanderJacksonPortfolio/1.0 (personal educational portfolio; Wikimedia Commons attribution)"})
with urlopen(request, timeout=45) as response:
    raw_map = response.read()
expected_hash = "8940d9197bf2aff482a803e3381759c8663a3da1"
actual_hash = hashlib.sha1(raw_map).hexdigest()
if actual_hash != expected_hash or b"<svg" not in raw_map[:1000] or b"<script" in raw_map.lower():
    raise RuntimeError(f"Downloaded Prague map differs from the licensed 2026 Commons original ({actual_hash})")
map_path = Path("images/projects/prague-metro-map-2026.svg")
map_path.write_bytes(raw_map)
print(json.dumps({"name": "Prague Metro", "source": map_url, "file": str(map_path), "sha1":actual_hash, "bytes":len(raw_map)}))
