#!/usr/bin/env python3
"""Browser-check the locally built generation gallery with an IMS mock."""

from __future__ import annotations

import argparse
import json
import threading
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError as exc:
    raise SystemExit("Run with: uv run --with playwright python browser_validate_generation_gallery.py") from exc


PROJECT_ROOT = Path(__file__).resolve().parents[3]
RUN_DIR = PROJECT_ROOT / "local_data/generation_runs/hp_lifestyle_ctech_v4_1_pilot_20261026_corrected_twins_20261027"
OUTPUT_DIR = Path(__file__).resolve().with_name("browser_validation")
IMS_MOCK = """
window.adobeImsFactory={createIMSLib(config,key){window[key]={
initialize(){config.onAccessToken({token:"local-mock"});queueMicrotask(()=>config.onReady({}));},
isSignedInUser(){return true;},async getProfile(){return {displayName:"Local IMS Mock"};},
signIn(){},signOut(){}};}};
"""


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *_args) -> None:
        pass


def require(value: bool, message: str, checks: list[str]) -> None:
    if not value:
        raise AssertionError(message)
    checks.append(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=RUN_DIR)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--headed", action="store_true")
    args = parser.parse_args()
    run_dir, output_dir = args.run_dir.resolve(), args.output_dir.resolve()
    gallery = run_dir / "gallery"
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / "browser_validation.json"
    screenshot = output_dir / "generation_gallery.png"
    checks: list[str] = []
    console_errors: list[str] = []
    page_errors: list[str] = []
    request_failures: list[str] = []
    result = {"version": "hp-ctech-v4.1-generation-browser-validation-v1", "validated_at_utc": datetime.now(timezone.utc).isoformat(), "run_dir": str(run_dir), "status": "failed", "ims": "local_mock_no_credentials", "checks": checks, "console_errors": console_errors, "page_errors": page_errors, "request_failures": request_failures, "screenshot": str(screenshot)}
    missing = [str(gallery / name) for name in ("index.html", "data.js", "main.js", "style.css", "imsauth.js") if not (gallery / name).is_file()]
    if missing:
        raise SystemExit("Built gallery is not ready: " + ", ".join(missing))
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(run_dir)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=not args.headed)
            page = browser.new_page(viewport={"width": 1800, "height": 1100})
            page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            page.on("requestfailed", lambda request: request_failures.append(f"{request.method} {request.url}: {request.failure}"))
            page.route("**/imslib.js", lambda route: route.fulfill(status=200, content_type="application/javascript", body=IMS_MOCK))
            response = page.goto(f"http://127.0.0.1:{server.server_port}/gallery/index.html", wait_until="domcontentloaded")
            require(response is not None and response.ok, "gallery loads over local HTTP", checks)
            page.wait_for_selector("#content:not(.hidden)")
            require("Local IMS Mock" in page.locator("#ims").inner_text(), "IMS mock completes authentication bootstrap", checks)
            require(page.evaluate("GENERATION_DATA.rows.length") == 120, "data contains all 120 prompt rows", checks)
            require(page.locator("#environmentFilter option").count() == 7, "environment filter exposes all six environments", checks)
            require(page.locator("#galleryRows tr").count() == 20, "default page renders twenty rows", checks)
            require(page.locator("thead th").count() == 7, "gallery renders the seven required columns", checks)
            first = page.locator("#galleryRows tr").first
            require(bool(first.locator(".prompt-text").inner_text().strip()), "prompt text is visible", checks)
            require(first.locator("td").nth(1).locator("img").count() == 1, "corrected input image is visible", checks)
            first.locator("td").nth(2).locator("summary").click()
            source_text = first.locator("td").nth(2).inner_text()
            require("source messaging" in source_text.lower() and "camera" in source_text.lower(), "source messaging and camera expand", checks)
            require(page.locator(".downloads a").count() == 4, "all prompt/system/source downloads are linked", checks)
            for link in page.locator(".downloads a").all():
                href = link.get_attribute("href")
                response = page.request.get(page.url.rsplit("/", 1)[0] + "/" + href.removeprefix("./"))
                require(response.ok and len(response.body()) > 0, f"download resolves: {href}", checks)
            first.locator(".image-button").first.click()
            require(page.locator("#assetModal").get_attribute("class").endswith("active"), "corrected input opens full-size", checks)
            page.keyboard.press("Escape")
            require(not console_errors, "no browser console errors", checks)
            require(not page_errors, "no uncaught JavaScript errors", checks)
            require(not request_failures, "no failed browser requests", checks)
            page.screenshot(path=str(screenshot), full_page=True)
            require(screenshot.is_file() and screenshot.stat().st_size > 0, "screenshot is captured", checks)
            result["browser_version"] = browser.version
            browser.close()
        result["status"] = "passed"
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
