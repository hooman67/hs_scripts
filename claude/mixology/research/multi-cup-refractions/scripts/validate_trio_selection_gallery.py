#!/usr/bin/env python3
"""Validate the standalone three-cup, two-stage selection gallery."""

from __future__ import annotations

import functools
import hashlib
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path("/home/colligo/mixology_data/refraction_research_2026-10-19/trio-two-stage-selection")
GALLERY = ROOT / "gallery"
RUNS = Path("/home/colligo/mixology_data/refraction_research_2026-10-19/multi-cup-refractions/runs")
REVIEW = ROOT / "_review"
STRICT = [
    "i02_trio_two_stage_origstyle",
    "i05_trio_two_stage_benchmark",
    "i07_trio_two_stage_focusclause",
]
SUPPLEMENTARY = ["i09_trio_floor_correction", "i01_trio_one_stage_origstyle"]


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_: object) -> None:
        pass


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["strict_candidates"] == STRICT
    assert manifest["followup"] == SUPPLEMENTARY[0]
    assert manifest["context"] == SUPPLEMENTARY[1]

    for candidate_id in [*STRICT, *SUPPLEMENTARY]:
        source_record = json.loads((RUNS / candidate_id / "record.json").read_text(encoding="utf-8"))
        gallery_record = json.loads((ROOT / f"candidates/{candidate_id}/record.json").read_text(encoding="utf-8"))
        assert source_record == gallery_record
        copied_output = ROOT / manifest["candidate_records"][candidate_id]["output"]
        assert copied_output.is_file()
        assert digest(copied_output) == source_record["output_sha256"]

    template = Path(
        "/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/"
        "research/generation/smoke_2026-10-07/gallery/imsauth.js"
    )
    assert (GALLERY / "imsauth.js").read_bytes() == template.read_bytes()

    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    result: dict[str, object] = {}
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(args=["--no-sandbox"])
            page = browser.new_page(viewport={"width": 1600, "height": 1100})
            errors: list[str] = []
            failed_requests: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on(
                "requestfailed",
                lambda request: failed_requests.append(f"{request.url}: {request.failure}"),
            )
            page.route(
                "https://auth-stg1.services.adobe.com/imslib/imslib.js",
                lambda route: route.fulfill(
                    content_type="application/javascript",
                    body="""window.adobeImsFactory={createIMSLib:(c,k)=>{
                    window[k]={initialize(){c.onReady({});},isSignedInUser(){return false;},
                    signIn(){},signOut(){}};}};""",
                ),
            )
            page.goto(
                f"http://127.0.0.1:{server.server_port}/gallery/index.html",
                wait_until="networkidle",
            )
            page.wait_for_selector("#content:not(.hidden)")
            assert page.locator(".strict-candidate").count() == 3
            assert page.locator("[data-pick]").count() == 3
            assert page.locator(".candidate").count() == 5
            review_images = page.locator(".image-card img")
            assert review_images.count() == 20
            page.locator(".context-details").evaluate("details=>details.open=true")
            for index in range(review_images.count()):
                review_images.nth(index).scroll_into_view_if_needed()
            assert review_images.evaluate_all("imgs=>imgs.every(i=>i.complete&&i.naturalWidth>0)")

            page.locator('[data-pick="i07_trio_two_stage_focusclause"]').click()
            assert "i07_trio_two_stage_focusclause" in page.locator("#selection-banner").inner_text()
            assert page.locator("#i07_trio_two_stage_focusclause").get_attribute("class").find("is-selected") >= 0
            page.locator("#i02_trio_two_stage_origstyle .image-button").first.click()
            assert page.locator("#lightbox").evaluate("dialog=>dialog.open")
            page.locator("#lightbox-close").click()
            assert not page.locator("#lightbox").evaluate("dialog=>dialog.open")

            page.screenshot(path=str(REVIEW / "desktop.png"), full_page=True)
            assert not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")

            page.set_viewport_size({"width": 390, "height": 844})
            page.evaluate("window.scrollTo(0,0)")
            assert not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
            page.locator("#i07_trio_two_stage_focusclause").scroll_into_view_if_needed()
            assert not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
            page.screenshot(path=str(REVIEW / "mobile.png"), full_page=True)
            assert not errors, errors
            assert not failed_requests, failed_requests
            result = {
                "validated": True,
                "strict_two_stage_candidates": len(STRICT),
                "third_stage_followups": 1,
                "one_stage_context": 1,
                "rendered_images": review_images.count(),
                "javascript_errors": errors,
                "failed_requests": failed_requests,
                "desktop_screenshot": str(REVIEW / "desktop.png"),
                "mobile_screenshot": str(REVIEW / "mobile.png"),
                "desktop_mobile_overflow": False,
                "picker_and_lightbox": "pass",
                "local_browser_ims": "mocked only; no live signed-in browser claim",
            }
            browser.close()
    finally:
        server.shutdown()

    (REVIEW / "local_validation.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
