"""Validate the multi-cup tab and preservation of the locked pre-merge gallery."""
from __future__ import annotations

import functools
import hashlib
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

RUN = Path("/home/colligo/mixology_data/refraction_research_2026-10-19")
TOPIC = Path("/home/colligo/hs_scripts/claude/mixology/research/multi-cup-refractions")
BASELINE = RUN / "_review/recipe_publication_2026-10-20/publication.json"
REVIEW = RUN / "_review/multi_cup_refractions_publication_2026-10-20"


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    REVIEW.mkdir(parents=True, exist_ok=True)
    baseline = json.loads(BASELINE.read_text())
    allowed_changes = {
        "gallery/data.js", "gallery/index.html", "gallery/style.css",
        "prompt_package/scripts/build_gallery.py",
    }
    changed = []
    baseline_outputs = []
    for item in baseline["files"]:
        path = RUN / item["path"]
        assert path.is_file(), item["path"]
        if sha(path) != item["sha256"]:
            changed.append(item["path"])
        if item["path"].endswith("/output.png"):
            baseline_outputs.append(item["path"])
    assert set(changed) == allowed_changes, changed
    assert len(baseline_outputs) == 55

    journal = json.loads((TOPIC / "iteration_journal.json").read_text())
    assert journal["generation_calls_started"] == journal["generation_outputs_completed"] == 20
    assert journal["final_stop_reason"].startswith("Generation ceiling reached")
    returned_ids = set()
    request_ids = set()
    reasoning_tokens = 0
    overall_passes = []
    for number, entry in enumerate(journal["entries"], 1):
        assert entry["generation_number"] == number
        folder = RUN / "multi-cup-refractions/runs" / entry["candidate_id"]
        record = json.loads((folder / "record.json").read_text())
        assert record["status"] == "complete"
        assert record["image_model"] == "gpt-image-2.5-sunburst"
        assert sha(folder / "output.png") == record["output_sha256"] == entry["output_sha256"]
        for item in record["input_images"]:
            assert sha(Path(item["path"])) == item["sha256"]
        request = json.loads((folder / "judge_request.json").read_text())
        judge = json.loads((folder / "judge.json").read_text())
        meta = judge["response_meta"]
        assert request["fresh_context"] is True
        assert request["model"] == "gpt-6-astra"
        assert request["reasoning"] == {"effort": "high"}
        assert meta["model"] == "gpt-6-astra" and meta["status"] == "completed"
        assert meta["error"] is None and meta["incomplete_details"] is None
        returned_ids.add(meta["id"])
        request_ids.add(meta["request_id"])
        reasoning_tokens += meta["usage"]["output_tokens_details"]["reasoning_tokens"]
        for image in request["images"]:
            assert sha(Path(image["path"])) == image["sha256"]
        if judge["output"]["overall_pass"]:
            overall_passes.append(entry["candidate_id"])
    assert len(returned_ids) == len(request_ids) == 20
    assert reasoning_tokens == 27277
    assert overall_passes == ["i09_trio_floor_correction"]

    html = (RUN / "gallery/index.html").read_text()
    assert 'id="composition-corrected-inputs"' in html
    assert 'id="recipe-to-image"' in html
    assert 'id="multi-cup-refractions"' in html
    assert html.count('class="sku mcr-run') == 20
    assert html.index('id="mcr-i09_trio_floor_correction"') < html.index('id="mcr-i12_five_global_focus_nostyle"')
    links = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(RUN)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    browser_result = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1600, "height": 1100}, device_scale_factor=1)
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.route("https://auth-stg1.services.adobe.com/imslib/imslib.js", lambda route: route.fulfill(
            content_type="application/javascript", body='''window.adobeImsFactory={createIMSLib:(c,k)=>{
            window[k]={initialize(){c.onReady({});},isSignedInUser(){return false;},signIn(){},signOut(){}};}};'''))
        page.goto(f"http://127.0.0.1:{server.server_port}/gallery/index.html#multi-cup-refractions", wait_until="networkidle")
        page.wait_for_selector("#content:not(.hidden)")
        assert page.locator("#multi-cup-refractions").is_visible()
        assert page.locator("#multi-cup-refractions-tab").get_attribute("aria-selected") == "true"
        assert page.locator(".mcr-run").count() == 20
        assert page.locator(".mcr-run .generated img").count() == 20
        for entry in journal["entries"]:
            cid = entry["candidate_id"]
            record = json.loads((RUN / "multi-cup-refractions/runs" / cid / "record.json").read_text())
            article = page.locator("#mcr-" + cid)
            assert article.locator(".composition-inputs img").count() == len(record["input_images"])
            assert article.locator("details").count() == 7
        page.evaluate("location.hash='mcr-i09_trio_floor_correction'")
        page.wait_for_selector("#multi-cup-refractions:not([hidden])")
        page.locator("#mcr-i09_trio_floor_correction .generated a.zoom").click()
        assert page.locator("#lightbox").is_visible()
        page.keyboard.press("Escape")
        assert page.locator("#lightbox").is_hidden()
        page.locator("#multi-cup-refractions-tab").focus()
        page.keyboard.press("ArrowLeft")
        assert page.locator("#recipe-to-image").is_visible()
        page.click("#multi-cup-refractions-tab")
        page.locator("#mcr-i09_trio_floor_correction").scroll_into_view_if_needed()
        page.screenshot(path=str(REVIEW / "desktop.png"))
        links = page.locator("[href],[src]").evaluate_all(
            "es=>es.flatMap(e=>[e.getAttribute('href'),e.getAttribute('src')]).filter(x=>x&&x.startsWith('.'))")
        for link in links:
            assert (RUN / "gallery" / link).resolve().is_file(), link
        page.set_viewport_size({"width": 390, "height": 844})
        page.evaluate("location.hash='multi-cup-refractions'")
        page.wait_for_selector("#multi-cup-refractions:not([hidden])")
        page.evaluate("window.scrollTo(0,0)")
        assert not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
        article = page.locator("#mcr-i12_five_global_focus_nostyle")
        article.scroll_into_view_if_needed()
        assert article.locator(".composition-inputs").evaluate("e=>getComputedStyle(e).gridTemplateColumns.split(' ').length") == 1
        assert not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
        page.screenshot(path=str(REVIEW / "mobile.png"))
        assert not errors, errors
        browser_result = {
            "local_browser_ims": "mocked only; no live signed-in browser claim",
            "javascript_errors": errors,
            "relative_links_checked": len(links),
            "desktop_screenshot": str(REVIEW / "desktop.png"),
            "mobile_screenshot": str(REVIEW / "mobile.png"),
            "mobile_overflow": False,
            "deep_links_lightbox_tabs": "pass",
        }
        browser.close()
    server.shutdown()
    result = {
        "validated": True,
        "baseline_objects_checked": len(baseline["files"]),
        "baseline_outputs_preserved": len(baseline_outputs),
        "expected_changed_baseline_files": sorted(changed),
        "iterations": 20,
        "actual_astra_high_judges": 20,
        "unique_response_ids": len(returned_ids),
        "unique_request_ids": len(request_ids),
        "returned_judge_reasoning_tokens": reasoning_tokens,
        "overall_passes": overall_passes,
        **browser_result,
    }
    (REVIEW / "local_validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
