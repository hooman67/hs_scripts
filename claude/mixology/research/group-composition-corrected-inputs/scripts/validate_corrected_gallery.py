"""Validate the corrected-input tab and preservation of the live 643-file baseline."""
from __future__ import annotations

import functools
import hashlib
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright


RUN = Path("/home/colligo/mixology_data/refraction_research_2026-10-19")
TOPIC = Path("/home/colligo/hs_scripts/claude/mixology/research/group-composition-corrected-inputs")
SNAPSHOT = RUN / "_review/corrected_composition_prepublication_2026-10-20"
TEMPLATE = Path("/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/gallery")


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert (RUN / "gallery/imsauth.js").read_bytes() == (TEMPLATE / "imsauth.js").read_bytes()
    live = json.loads((SNAPSHOT / "live_s3_manifest.json").read_text())
    live_by_path = {item["path"]: item for item in live["files"]}
    baseline_outputs = [item for item in live["files"] if item["path"].endswith("/output.png")]
    assert len(baseline_outputs) == 35
    for item in baseline_outputs:
        assert digest(RUN / item["path"]) == item["sha256"], item["path"]

    plan = json.loads((TOPIC / "cases.json").read_text())
    records = [
        json.loads(path.read_text())
        for path in sorted((RUN / "composition-corrected-inputs/runs").glob("*/record.json"))
    ]
    assert len(records) == len(plan) == 9
    for record in records:
        assert record["status"] == "complete"
        assert record["visual_review"]
        assert digest(Path(record["output"])) == record["output_sha256"]
        assert record["output_dimensions"] == [1536, 1024]
        assert digest(Path(record["original_counterpart"]["output"])) == record["original_counterpart"]["output_sha256"]
        assert "wire-level image POST count is unknown" in record["transport_retry_limitation"]
        folder = Path(record["output"]).parent
        for name in [
            "system_prompt.md", "user_prompt.txt", "image_prompt.txt", "rewriter_request.json",
            "rewriter_response.json", "image_request.json", "image_submission.json",
            "image_response.json", "judge_request.json", "judge.json",
        ]:
            assert (folder / name).is_file(), (record["id"], name)
        for item in record["input_images"]:
            assert digest(Path(item["path"])) == item["sha256"]

    html = (RUN / "gallery/index.html").read_text()
    data = (RUN / "gallery/data.js").read_text()
    assert html.count('id="composition-corrected-inputs-tab"') == 1
    assert html.count('id="composition-corrected-inputs"') == 1
    assert "Group composition corrected inputs" in html
    assert "direct OpenAI" in html and "FAL condition" in html
    for run_id in plan:
        assert f'id="corrected-composition-{run_id}"' in html
        assert "composition_corrected_" + run_id in data

    links = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(RUN)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    result = {
        "validated_at": "2026-10-20",
        "live_baseline_files": len(live_by_path),
        "live_baseline_outputs_preserved": len(baseline_outputs),
        "corrected_outputs": len(records),
        "ims_template": "byte-identical",
        "authentication_test": "IMS mocked in local browser only; live signed-in gateway not exercised",
    }
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1600, "height": 1100})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.route(
            "https://auth-stg1.services.adobe.com/imslib/imslib.js",
            lambda route: route.fulfill(
                content_type="application/javascript",
                body="""window.adobeImsFactory={createIMSLib:(c,k)=>{window[k]={initialize(){c.onReady({});},isSignedInUser(){return false;},signIn(){},signOut(){}};}};""",
            ),
        )
        url = f"http://127.0.0.1:{server.server_port}/gallery/index.html#composition-corrected-inputs"
        page.goto(url, wait_until="networkidle")
        page.wait_for_selector("#content:not(.hidden)")
        page.wait_for_selector("#composition-corrected-inputs:not([hidden])")
        assert page.locator("#composition-corrected-inputs-tab").get_attribute("aria-selected") == "true"
        assert page.locator(".corrected-composition-run").count() == 9
        page.locator("img[loading]").evaluate_all("items=>items.forEach(item=>item.loading='eager')")
        page.wait_for_function("Array.from(document.querySelectorAll('img[src]')).every(i=>i.complete && i.naturalWidth>0)")
        links = page.locator("[href],[src]").evaluate_all(
            "items=>items.flatMap(i=>[i.getAttribute('href'),i.getAttribute('src')]).filter(x=>x&&x.startsWith('.'))"
        )
        for link in links:
            assert (RUN / "gallery" / link).resolve().is_file(), link
        for record in records:
            section = page.locator("#corrected-composition-" + record["id"])
            assert section.locator(".composition-inputs img").count() == len(record["input_images"])
            assert section.locator(".composition-comparison img").count() == 2
            text = section.inner_text()
            assert record["user_prompt"] in text
            assert "Original-input output · FAL condition" in text
            assert "Corrected-input output · direct OpenAI" in text
        first = page.locator("#corrected-composition-corrected_v1small_pair_lineup")
        first.locator("details").first.locator("summary").click()
        assert first.locator("details").first.get_attribute("open") is not None
        first.locator(".composition-comparison a.zoom").last.click()
        assert page.locator("#lightbox").is_visible()
        page.keyboard.press("Escape")
        assert page.locator("#lightbox").is_hidden()
        page.evaluate("location.hash='corrected-composition-corrected_v1fal_staggered'")
        page.wait_for_selector("#composition-corrected-inputs:not([hidden])")
        page.locator("#corrected-composition-corrected_v1fal_staggered").scroll_into_view_if_needed()
        review = RUN / "_review"
        page.screenshot(path=str(review / "gallery_corrected_composition_desktop.png"), full_page=False)
        page.set_viewport_size({"width": 390, "height": 844})
        page.evaluate("window.scrollTo(0,0)")
        assert not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
        for record in records:
            section = page.locator("#corrected-composition-" + record["id"])
            section.scroll_into_view_if_needed()
            assert not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
            assert section.locator(".composition-inputs").evaluate(
                "element=>getComputedStyle(element).gridTemplateColumns.split(' ').length"
            ) == 1
        page.locator("#corrected-composition-corrected_v1small_pair_lineup .composition-comparison").screenshot(
            path=str(review / "gallery_corrected_composition_mobile.png")
        )
        assert not errors, errors
        result.update(
            relative_links_checked=len(links),
            loaded_images=page.locator("img[src]").count(),
            deep_link="pass",
            prompts_and_critiques="pass",
            lightbox="pass",
            mobile_overflow=False,
            javascript_errors=errors,
        )
        browser.close()
    server.shutdown()
    (RUN / "_review/corrected_composition_gallery_validation.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result))


if __name__ == "__main__":
    main()
