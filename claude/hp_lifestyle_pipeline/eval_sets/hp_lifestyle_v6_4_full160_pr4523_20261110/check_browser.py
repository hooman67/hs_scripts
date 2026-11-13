"""Verify both three-column reports with real frozen assets and mocked IMS."""
import json
import mimetypes
import os
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import extend_comparisons as extension
import report
import study

HERE = study.HERE
STAGING = extension.STAGING
manifest = study.load(STAGING / extension.MANIFEST_PATH)
data = study.load(STAGING / extension.DATA_PATH)
fe = study.load(STAGING / "fe/data.json")
old_fe_viewer = HERE / "baseline_live/full160/fe/viewer.html"
assert old_fe_viewer.read_bytes() == (Path.home() / ".claude/scripts/fe_html/annotation_viewer.html").read_bytes()
roots = {extension.TARGET: study.COMPARISON / "public",
         study.PREFIX: report.PUBLIC, report.PRIOR_PREFIX: study.PRIOR / "public"}
inventories = {extension.TARGET: study.load(HERE / "baseline_live/full160/asset_manifest.json")["assets"],
               study.PREFIX: study.load(report.PUBLIC / "asset_manifest.json")["assets"],
               report.PRIOR_PREFIX: study.load(study.PRIOR / "public/asset_manifest.json")["assets"]}
verified = set()
errors = []
work = HERE / ".browser-work"
work.mkdir(exist_ok=True)
fd = os.open(work, os.O_RDONLY | os.O_DIRECTORY)
os.environ["TMPDIR"] = f"/proc/{os.getpid()}/fd/{fd}"

from playwright.sync_api import sync_playwright  # noqa: E402


def local_asset(url):
    parsed = urlsplit(url)
    if parsed.netloc != "foundry-aws-corp.adobe.io":
        raise ValueError("unexpected external browser request")
    key = unquote(parsed.path).removeprefix("/asset/" + study.BUCKET + "/")
    for prefix, root in roots.items():
        if not key.startswith(prefix + "/"):
            continue
        name = key.removeprefix(prefix + "/")
        if prefix == extension.TARGET and (STAGING / name).is_file():
            path = STAGING / name
            expected = manifest["assets"].get(name)
        elif prefix == extension.TARGET and name in ("fe/viewer.html", "gallery/imsauth.js"):
            path = HERE / "baseline_live/full160" / name
            expected = None
        else:
            path = root / name
            expected = inventories[prefix].get(name)
        if not any(path.resolve().is_relative_to(allowed.resolve()) for allowed in
                   (root, STAGING, HERE / "baseline_live/full160")) or not path.is_file():
            raise ValueError("missing or escaped frozen browser asset")
        if path not in verified:
            if expected is not None and study.sha(path) != expected["sha256"]:
                raise ValueError("browser fixture differs from its published asset identity")
            verified.add(path)
        return path
    raise ValueError("unexpected browser asset prefix")


try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path="/mnt/localssd/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome",
            args=["--no-sandbox", "--no-process-singleton"])
        try:
            page = browser.new_page(viewport={"width": 1920, "height": 1100})
            page.on("pageerror", lambda error: errors.append(str(error)))

            def handle(route):
                if route.request.url.startswith("https://auth-stg1.services.adobe.com/"):
                    route.fulfill(content_type="application/javascript", body="""
window.adobeImsFactory={createIMSLib(config,key){window[key]={
 initialize(){config.onAccessToken({token:"LOCAL-IMS-MOCK"});setTimeout(()=>config.onReady({}),0)},
 isSignedInUser(){return true},getProfile(){return Promise.resolve({displayName:"Local UI test",account_type:"test"})},
 getAccessToken(){return {token:"LOCAL-IMS-MOCK"}},signIn(){},signOut(){}}}};
""")
                    return
                if "/fe/annotations/" in urlsplit(route.request.url).path:
                    route.fulfill(status=404, body="Annotation reads/writes are not exercised.")
                    return
                path = local_asset(route.request.url)
                route.fulfill(path=str(path),
                              content_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream")

            page.route("**/*", handle)
            page.goto(extension.TARGET_BASE + "gallery/index.html")
            page.wait_for_function("document.querySelectorAll('#comparison > .pair').length===160", timeout=120000)
            assert page.locator("#comparison .image-grid > .output").count() == 480
            columns = ("v6_3_pr4417", "v6_3_pr4523", extension.CELL)
            assert page.locator("#comparison > .pair").evaluate_all(
                "rows=>rows.map(r=>[...r.querySelectorAll('.image-grid > .output > img')].map(i=>i.getAttribute('src')))") == [
                    [row["outputs"][column]["image"] for column in columns] for row in data["rows"]]
            for row in data["rows"]:
                for column in columns:
                    local_asset(urljoin(extension.TARGET_BASE + "gallery/", row["outputs"][column]["image"]))
                for value in row["outputs"][extension.CELL]["inputs"].values():
                    local_asset(urljoin(extension.TARGET_BASE + "gallery/", value))
            for index in (0, 159):
                page.locator("#search").fill(data["rows"][index]["prompt"]["prompt_key"])
                assert page.locator("#comparison > .pair").count() == 1
                images = page.locator("#comparison .image-grid > .output > img")
                images.evaluate_all("images=>images.forEach(i=>i.loading='eager')")
                images.first.scroll_into_view_if_needed()
                page.wait_for_function("""() => [...document.querySelectorAll(
                    '#comparison .image-grid > .output > img')].every(i=>i.complete&&i.naturalWidth===2368)""")
                assert images.evaluate_all(
                    "images=>Math.max(...images.map(i=>i.getBoundingClientRect().top))-Math.min(...images.map(i=>i.getBoundingClientRect().top))") < 1
            page.locator("#search").fill(data["rows"][0]["prompt"]["prompt_key"])
            assert data["rows"][0]["prompt_v6_4"]["text"] in page.locator("#comparison").inner_text()
            added = page.locator("#comparison .image-grid > .output").nth(2)
            added.get_by_text("Actual model inputs: product PNG, geometry guide, Astra style reference", exact=True).click()
            added.locator("details[open] img").evaluate_all("images=>images.forEach(i=>i.loading='eager')")
            page.wait_for_function("""() => [...document.querySelectorAll(
                '#comparison .image-grid > .output:last-child details[open] img')].every(i=>i.complete&&i.naturalWidth>0)""")
            assert added.locator("details[open] img").count() == 3
            added.locator(":scope > img").click()
            assert page.locator("#lightbox").is_visible()
            page.locator("#closeImage").click()
            page.locator("#search").fill("")
            page.locator("#state").select_option("reused")
            assert page.locator("#comparison > .pair").count() == 30
            page.locator("#state").select_option("")
            page.locator("#refresh").click()
            page.wait_for_function("document.querySelectorAll('#comparison > .pair').length===160")
            page.screenshot(path=str(HERE / "gallery_three_columns.png"))
            page.goto(extension.TARGET_BASE + "fe/viewer.html?ldap=hshariati")
            page.locator("#setupSkip").click()
            page.wait_for_selector(".row")
            assert page.evaluate("MERGED.length") == 160
            assert page.evaluate("SOURCES[0].rows.map(r=>r.images.map(i=>i.image_src))") == [
                [image["image_src"] for image in row["images"]] for row in fe["rows"]]
            assert page.locator(".row").first.locator(".asset").count() == 3
            assert page.locator(".caps, .mfold, .asset.input").count() == 0
            assert page.evaluate("SOURCES[0].links.length") == 0
            page.wait_for_function("""() => [...document.querySelector('.row').querySelectorAll('img')]
                                     .every(i=>i.complete&&i.naturalWidth===2368)""")
            page.screenshot(path=str(HERE / "fe_three_columns.png"))
            page.goto(extension.TARGET_BASE + "fe/viewer.html?ldap=hshariati&rows=160")
            page.wait_for_selector(".row")
            assert page.evaluate("MERGED.length") == 1
            assert page.locator(".rowhead .rowidx").first.inner_text() == fe["rows"][-1]["meta_data"]["evalset_item_id"]
            page.wait_for_function("""() => [...document.querySelector('.row').querySelectorAll('img')]
                                     .every(i=>i.complete&&i.naturalWidth===2368)""")
            assert not errors, errors
        finally:
            browser.close()
finally:
    os.close(fd)

report.emit(HERE / "browser_validation.json", {"status": "passed", "rows_per_report": 160,
    "image_columns_per_report": 3, "all_output_bindings_verified": 480,
    "original_two_columns_preserved": True, "actual_v64_input_images_loaded": 3,
    "first_last_all_three_images_rendered": True, "search_state_refresh_lightbox": True,
    "fe_no_extra_columns": True, "official_fe_viewer_unchanged": True, "javascript_errors": errors,
    "extension_manifest_sha256": study.sha(STAGING / extension.MANIFEST_PATH),
    "network_boundary": "Actual frozen images/data; IMS mocked. Live gateway/login/annotation writes not certified."})
print("Passed: both160-row reports;480 exact image bindings; three clean FE columns.")
