"""Capture the actual published Shiny traffic dashboard for portfolio visual review."""
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PTimeout
from PIL import Image
from collections import Counter
import json, time, os, re

URL = "https://ajackson25.shinyapps.io/USA_Accidents/"
OUT = Path("images/projects/traffic-accidents-highres-preview.png")
OUT.parent.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(
        viewport={"width": 1600, "height": 900},
        device_scale_factor=2,
        color_scheme="light",
        reduced_motion="reduce",
        locale="en-US",
    )
    page = context.new_page()
    failures=[]
    page.on("requestfailed",lambda request: failures.append({"url":request.url[:130],"error":request.failure}))
    response=page.goto(URL,wait_until="domcontentloaded",timeout=120000)
    if response is None or response.status>=400: raise RuntimeError(f"Site returned {response.status if response else 'no response'}")
    # Wait for R Shiny's dynamically populated map, not just the document shell.
    try:
        page.locator("#usa_map.leaflet-container").wait_for(state="visible",timeout=110000)
    except PTimeout:
        print(json.dumps({"error":"Could not see Leaflet container","title":page.title(),"body":page.locator("body").inner_text()[:2000],"url":page.url}))
        page.screenshot(path=str(OUT),full_page=False,animations="disabled")
        raise
    try:
        page.wait_for_function("""() => {
          const el=document.querySelector('#usa_map.leaflet-container');
          return !!el && el.querySelectorAll('.leaflet-interactive').length > 20;
        }""", timeout=65000)
    except PTimeout:
        print("WARNING: Leaflet shapes had not fully appeared before screenshot.")
    page.wait_for_timeout(8500)
    diagnostics=page.evaluate("""() => ({
      title:document.title,
      nav:document.querySelector('.navbar-brand')?.textContent?.trim(),
      height:window.innerHeight,
      scrollY:window.scrollY,
      map:document.querySelector('#usa_map')?.getBoundingClientRect().toJSON(),
      loadedTiles:document.querySelectorAll('.leaflet-tile-loaded').length,
      tiles:[...document.querySelectorAll('.leaflet-tile')].slice(0,25).map(x=>x.getAttribute('src')),
      interactiveShapes:document.querySelectorAll('#usa_map .leaflet-interactive').length,
      pageText:document.body.innerText.slice(0,700),
    })""")
    print("SHINY_CAPTURE_DIAGNOSTICS "+json.dumps(diagnostics))
    print("SHINY_CAPTURE_FAILED_REQUESTS "+json.dumps(failures[:15]))
    if diagnostics["interactiveShapes"]<10: raise RuntimeError("Shiny crash data map did not render enough geographic polygons")
    if diagnostics["loadedTiles"]<4: raise RuntimeError("Base map tiles did not load; capture would be low quality")
    page.screenshot(path=str(OUT),full_page=False,animations="disabled")
    with Image.open(OUT) as im:
        im.verify()
    with Image.open(OUT) as im:
        if im.size!=(3200,1800):raise RuntimeError(f"Unexpected screenshot resolution {im.size}")
        # High-quality web copy for portfolio; the source PNG stays unmodified.
        im.convert("RGB").save("images/projects/traffic-accidents-highres.webp",format="WEBP",quality=88,method=6)
    print("SHINY_CAPTURE_SUCCESS "+json.dumps({"image":str(OUT),"png_bytes":OUT.stat().st_size,"webp_bytes":Path("images/projects/traffic-accidents-highres.webp").stat().st_size,"resolution":[3200,1800]}))
    browser.close()
