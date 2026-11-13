#!/usr/bin/env python3
"""Render the built V4.1 report with a local IMS mock and validate its browser UI."""

from __future__ import annotations

import argparse
import hashlib
import json
import threading
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urljoin

try:
    from playwright.sync_api import sync_playwright
except ImportError as exc:  # pragma: no cover - exercised only when invoked without uv dependency
    raise SystemExit(
        "Playwright is required. Run: uv run --with playwright python browser_validate.py"
    ) from exc


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
HERE = PROJECT / "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1"
DEFAULT_REPORT = PROJECT / "local_data/reports/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1"
DEFAULT_OUTPUT = HERE / "browser_validation"
IMS_MOCK = r"""
window.adobeImsFactory = {
  createIMSLib(config, key) {
    window[key] = {
      initialize() {
        config.onAccessToken({token: "local-browser-validation-token"});
        queueMicrotask(() => config.onReady({}));
      },
      isSignedInUser() { return true; },
      async getProfile() { return {displayName: "Local IMS Mock", account_type: "local"}; },
      signIn() {},
      signOut() {}
    };
  }
};
"""
EXPECTED_DOWNLOADS = {
    "../downloads/analysis.json",
    "../downloads/pilot_prompts.txt",
    "../downloads/pilot_prompts.json",
    "../downloads/system_prompt.md",
    "../downloads/candidate_metrics.csv",
    "../downloads/lexical_audit.json",
    "../downloads/reference_prompts.json",
}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *_args) -> None:
        pass


def require(condition: bool, message: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(message)
    checks.append(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-root", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--headed", action="store_true")
    args = parser.parse_args()
    report_root = args.report_root.resolve()
    output_dir = args.output_dir.resolve()
    gallery = report_root / "gallery"
    source_manifest = report_root / "source_manifest.json"
    required = [gallery / "index.html", gallery / "data.js", gallery / "report.js",
                gallery / "style.css", gallery / "imsauth.js", source_manifest]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Built report is not ready; missing: " + ", ".join(missing))

    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot = output_dir / "report_full_page.png"
    result_path = output_dir / "browser_validation.json"
    checks: list[str] = []
    console_errors: list[str] = []
    page_errors: list[str] = []
    request_failures: list[str] = []
    result = {
        "version": "hp-v4.1-distribution-browser-validation-v1",
        "validated_at_utc": datetime.now(timezone.utc).isoformat(),
        "report_root": str(report_root),
        "source_manifest_sha256": sha256(source_manifest),
        "ims": "local_mock_no_credentials",
        "status": "failed",
        "checks": checks,
        "console_errors": console_errors,
        "page_errors": page_errors,
        "request_failures": request_failures,
        "screenshot": str(screenshot),
    }

    handler = partial(QuietHandler, directory=str(report_root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}/gallery/index.html"

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=not args.headed)
            result["browser_version"] = browser.version
            page = browser.new_page(viewport={"width": 1600, "height": 1100}, device_scale_factor=1)
            page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            page.on("requestfailed", lambda request: request_failures.append(
                f"{request.method} {request.url}: {request.failure}"
            ))
            page.route("**/imslib.js", lambda route: route.fulfill(
                status=200, content_type="application/javascript", body=IMS_MOCK
            ))
            response = page.goto(base_url, wait_until="domcontentloaded")
            require(response is not None and response.ok, "report index loads over local HTTP", checks)
            page.wait_for_selector("#content:not(.hidden)")
            page.wait_for_function(
                "document.querySelectorAll('#candidateExplorer details.candidate').length === 120"
            )
            require("Local IMS Mock" in page.locator("#ims").inner_text(),
                    "local IMS mock completes authentication bootstrap", checks)
            require(page.locator("#loading").is_hidden(), "loading state is hidden", checks)
            narrative = page.locator("#interpretation").inner_text()
            require("one bounded GPT-5.5 correction pass" in narrative
                    and "8 of 120" in narrative
                    and "not evidence of single-call production reliability" in narrative,
                    "main narrative discloses correction, 8/120 edits, and reliability limit", checks)

            require(page.locator("#environmentChart .bar-row").count() == 6,
                    "environment chart renders six categories", checks)
            require(page.locator("#relationshipChart .bar-row").count() > 0,
                    "relationship chart renders", checks)
            require(page.locator("#scoreChart svg").count() == 1,
                    "score histogram renders", checks)
            require(page.locator("#similarityChart svg").count() == 1,
                    "similarity histogram renders", checks)
            require(page.locator("#scatter circle.point").count() == 120,
                    "semantic map renders 120 prompt points", checks)
            require(page.locator("#scatter polygon.ref-star").count() == 18,
                    "semantic map renders eighteen reference stars", checks)
            require(page.locator("#feedbackComparison tbody tr").count() == 2,
                    "feedback comparison renders both lexical indicators", checks)

            explorer = page.locator("#candidateExplorer details.candidate")
            require(explorer.count() == 120, "candidate explorer renders all 120 prompts", checks)
            first_candidate = explorer.first
            first_candidate.locator(":scope > summary").click()
            require(first_candidate.get_attribute("open") is not None,
                    "candidate detail toggle opens", checks)
            source_text = first_candidate.locator(".source-input pre").inner_text()
            require("KSP1" in source_text and "ValueProposition" in source_text,
                    "candidate detail shows full source messaging", checks)
            require(bool(first_candidate.locator("section").filter(has_text="Input camera").first.inner_text().strip()),
                    "candidate detail shows input camera", checks)
            first_candidate.locator(":scope > summary").click()
            require(first_candidate.get_attribute("open") is None,
                    "candidate detail toggle closes", checks)
            edited_candidates = page.locator("#candidateExplorer details.candidate:has(.editorial-badge)")
            require(edited_candidates.count() == 8,
                    "explorer marks exactly eight editorial scene edits", checks)
            edited_candidate = edited_candidates.first
            edited_candidate.locator(":scope > summary").click()
            provenance = edited_candidate.locator("details.provenance-detail")
            provenance.locator("summary").click()
            provenance_text = provenance.inner_text()
            require("raw_correction_text" in provenance_text
                    and "repair_normalized_text" in provenance_text
                    and "edit details" in provenance_text,
                    "edited candidate exposes correction and edit provenance", checks)

            references = page.locator("#referenceList details.reference")
            require(references.count() == 18, "reference list renders all eighteen references", checks)
            ct11 = references.nth(10)
            require(ct11.locator("summary").inner_text().startswith("CT11 ·"),
                    "reference list preserves CT01-CT18 order", checks)
            ct11.locator("summary").click()
            require(ct11.get_attribute("open") is not None,
                    "reference detail toggle opens", checks)
            reference_headings = ct11.locator("h3").all_text_contents()
            require("Raw source example" in reference_headings
                    and "Normalized core used for text embedding" in reference_headings,
                    "reference detail shows raw and normalized text", checks)
            require("raw source SHA-256" in (ct11.locator("p.note").text_content() or ""),
                    "reference detail shows raw-source hash", checks)

            page.select_option("#colorBy", "view_role")
            require("close_up" in page.locator("#legend").inner_text()
                    and "wide" in page.locator("#legend").inner_text(),
                    "color dropdown redraws legend by camera view", checks)
            expected_close = page.evaluate(
                "ANALYSIS.points.filter(point => point.view_role === 'close_up').length"
            )
            page.select_option("#pointFilter", "close_up")
            require(page.locator("#scatter circle.point").count() == expected_close,
                    "point dropdown filters close-up prompts", checks)
            expected_home = page.evaluate(
                "ANALYSIS.points.filter(point => point.display_environment === 'Home').length"
            )
            page.select_option("#pointFilter", "env:Home")
            require(page.locator("#scatter circle.point").count() == expected_home,
                    "point dropdown filters an environment", checks)
            page.select_option("#pointFilter", "all")
            page.select_option("#colorBy", "display_environment")

            download_links = page.locator(".downloads a")
            hrefs = set(download_links.evaluate_all("nodes => nodes.map(node => node.getAttribute('href'))"))
            require(hrefs == EXPECTED_DOWNLOADS, "download navigation exposes the exact report artifacts", checks)
            for href in sorted(hrefs):
                download_response = page.request.get(urljoin(page.url, href))
                require(download_response.ok and len(download_response.body()) > 0,
                        f"download resolves with content: {href}", checks)
            with page.expect_download() as download_info:
                page.get_by_role("link", name="Prompts text").click()
            download = download_info.value
            require(download.suggested_filename == "pilot_prompts.txt",
                    "plain-text prompt link downloads pilot_prompts.txt", checks)
            download.cancel()

            require(not console_errors, "no browser console errors", checks)
            require(not page_errors, "no uncaught JavaScript errors", checks)
            require(not request_failures, "no failed browser requests", checks)
            page.screenshot(path=str(screenshot), full_page=True)
            require(screenshot.is_file() and screenshot.stat().st_size > 0,
                    "full-page screenshot is captured", checks)
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
