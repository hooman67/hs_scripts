"""Verify both actual reports locally; only IMS is mocked, never images or data."""
from __future__ import annotations

import json
import mimetypes
import os
from pathlib import Path
import study

HERE = Path(__file__).resolve().parent
PUBLIC = HERE / "public"
BASE = "https://foundry-aws-corp.adobe.io/asset/" + study.BUCKET + "/" + study.PREFIX + "/"
work = HERE / ".browser-work"
work.mkdir(exist_ok=True)
work_fd = os.open(work, os.O_RDONLY | os.O_DIRECTORY)
os.environ["TMPDIR"] = f"/proc/{os.getpid()}/fd/{work_fd}"

from playwright.sync_api import sync_playwright  # noqa: E402

errors = []
data = study.load(PUBLIC / "data/generation.json")
fe = study.load(PUBLIC / "fe/data.json")
assert fe["meta_texts"] == [study.TITLE]
assert (PUBLIC / "fe/viewer.html").read_bytes() == (
    Path.home() / ".claude/scripts/fe_html/annotation_viewer.html").read_bytes()

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path="/mnt/localssd/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome",
            args=["--no-sandbox", "--no-process-singleton"],
        )
        try:
            page = browser.new_page(viewport={"width": 1600, "height": 1100})
            page.on("pageerror", lambda error: errors.append(str(error)))

            def handle(route):
                url = route.request.url.split("?", 1)[0]
                if url.startswith("https://auth-stg1.services.adobe.com/"):
                    route.fulfill(content_type="application/javascript", body="""
window.adobeImsFactory={createIMSLib(config,key){window[key]={
 initialize(){config.onAccessToken({token:"LOCAL-IMS-MOCK"});setTimeout(()=>config.onReady({}),0)},
 isSignedInUser(){return true},getProfile(){return Promise.resolve({displayName:"Local UI test",account_type:"test"})},
 getAccessToken(){return {token:"LOCAL-IMS-MOCK"}},signIn(){},signOut(){}}}};
""")
                    return
                relative = url.removeprefix(BASE) if url.startswith(BASE) else None
                path = (PUBLIC / relative).resolve() if relative is not None else None
                if path is None or not path.is_relative_to(PUBLIC) or not path.is_file():
                    route.fulfill(status=404, body="Not present in the owned local browser fixture.")
                    return
                route.fulfill(path=str(path),
                              content_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream")

            page.route("**/*", handle)
            page.goto(BASE + "gallery/index.html")
            page.wait_for_function("document.querySelectorAll('.pair').length === 30", timeout=120000)
            assert page.title() == study.TITLE
            assert page.locator(".output").count() == 30
            assert page.locator(".pair").evaluate_all(
                "rows => rows.map(row => row.dataset.key)") == [r["prompt"]["prompt_key"] for r in data["rows"]]
            assert page.locator(".output > img").evaluate_all(
                "images => images.map(i => i.getAttribute('src'))") == [r["output"]["image"] for r in data["rows"]]
            first = page.locator(".pair").first
            assert data["rows"][0]["prompt"]["text"] in first.inner_text()
            first.get_by_text("Actual model inputs: product PNG, geometry guide, Astra style reference",
                              exact=True).click()
            assert first.locator("details[open] img").count() == 3
            for image in first.locator("img").all():
                image.scroll_into_view_if_needed()
                image.evaluate("i => i.loading='eager'")
                page.wait_for_function(
                    "(url) => [...document.images].some(i=>i.src===url&&i.complete&&i.naturalWidth>0)",
                    arg=image.evaluate("i => i.src"),
                )
            page.screenshot(path=str(HERE / "gallery_browser.png"))
            page.locator("#search").fill(data["rows"][0]["prompt"]["prompt_key"])
            assert page.locator(".pair").count() == 1
            page.locator("#search").fill("")
            page.locator("#refresh").click()
            page.wait_for_function("document.querySelectorAll('.pair').length === 30")
            page.goto(BASE + "fe/viewer.html?ldap=hshariati")
            page.locator("#setupSkip").click()
            page.wait_for_selector(".row")
            assert page.evaluate("MERGED.length") == 30
            assert page.evaluate("SOURCES[0].rows.map(r=>r.images.map(i=>i.image_src))") == [
                [a["image_src"] for a in row["images"]] for row in fe["rows"]]
            assert page.locator(".caps, .mfold, .asset.input").count() == 0
            assert page.evaluate("SOURCES[0].links.length") == 0
            assert page.locator(".row").first.locator(".asset").count() == 1
            page.wait_for_function("""() => [...document.querySelector('.row').querySelectorAll('img')]
                                     .every(i=>i.complete&&i.naturalWidth>0)""")
            page.screenshot(path=str(HERE / "fe_browser.png"))
            page.goto(BASE + "fe/viewer.html?ldap=hshariati&rows=30")
            page.wait_for_selector(".row")
            assert page.evaluate("MERGED.length") == 1
            assert page.locator(".rowhead .rowidx").first.inner_text() == (
                fe["rows"][-1]["meta_data"]["evalset_item_id"])
            page.wait_for_function("""() => [...document.querySelector('.row').querySelectorAll('img')]
                                     .every(i=>i.complete&&i.naturalWidth>0)""")
            assert not errors, errors
        finally:
            browser.close()
finally:
    os.close(work_fd)

receipt = {
    "status": "passed", "rows_per_report": 30, "output_images_per_row": 1,
    "all_row_and_output_bindings_verified": True, "actual_input_images_loaded": 3,
    "first_and_last_fe_images_rendered": True, "no_extra_fe_columns": True,
    "official_viewer_unchanged": True, "detailed_search_and_refresh": True,
    "javascript_errors": errors,
    "asset_manifest_sha256": study.sha(PUBLIC / "asset_manifest.json"),
    "network_boundary": "Actual local data/images; IMS mocked. Live login and annotation writes not certified.",
}
study.write(HERE / "browser_validation.json", receipt)
print(json.dumps(receipt))
