"""Exercise the five-column page using real frozen data/images and mocked IMS."""
import json
import mimetypes
import os
from pathlib import Path
from urllib.parse import unquote, urlsplit

import update

HERE = update.HERE
STAGING = HERE / "staging"
manifest = update.load(STAGING / update.MANIFEST_PATH)
data = update.load(STAGING / update.DATA_PATH)
work = HERE / ".browser-work"
work.mkdir(exist_ok=True)
fd = os.open(work, os.O_RDONLY | os.O_DIRECTORY)
os.environ["TMPDIR"] = f"/proc/{os.getpid()}/fd/{fd}"

from playwright.sync_api import sync_playwright  # noqa: E402

errors = []
missing = []
excluded_judge_images = set()
verified = set()
roots = {update.TARGET: update.OLD / "public", update.SOURCE: update.NEW / "public"}
inventories = {update.TARGET: update.load(HERE / "snapshot/target/asset_manifest.json")["assets"],
               update.SOURCE: update.load(HERE / "snapshot/source/asset_manifest.json")["assets"]}


def local_asset(url):
    key = unquote(urlsplit(url).path).removeprefix(f"/asset/{update.BUCKET}/")
    for prefix, root in roots.items():
        if not key.startswith(prefix + "/"):
            continue
        name = key.removeprefix(prefix + "/")
        if prefix == update.TARGET and (STAGING / name).is_file():
            path = STAGING / name
            expected = manifest["assets"].get(name)
        else:
            path = root / name
            expected = inventories[prefix].get(name)
        if not path.resolve().is_relative_to((STAGING if path.is_relative_to(STAGING) else root).resolve()):
            raise ValueError("browser fixture path escaped its frozen report")
        if not path.is_file():
            raise FileNotFoundError(path)
        if path not in verified:
            if expected is not None and update.digest(path.read_bytes()) != expected["sha256"]:
                raise ValueError("local fixture differs from its live published asset manifest")
            verified.add(path)
        return path
    raise ValueError("unexpected report origin or asset prefix")


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
                if ("/hp-data-artifacts/hp-3p-gpt25/" in route.request.url
                        and route.request.resource_type == "image"
                        and route.request.frame.parent_frame is not None):
                    excluded_judge_images.add(urlsplit(route.request.url).path)
                    route.abort()
                    return
                try:
                    path = local_asset(route.request.url)
                except (ValueError, FileNotFoundError) as error:
                    missing.append(str(error))
                    route.fulfill(status=404, body="Missing frozen browser fixture")
                    return
                route.fulfill(path=str(path),
                              content_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream")

            page.route("**/*", handle)
            page.goto(update.BASE + "index.html")
            page.wait_for_function("document.querySelectorAll('#comparison > .pair').length===30",
                                   timeout=120000)
            assert page.locator("#comparison .image-grid > .output").count() == 150
            assert page.locator("#comparison .historical > .output").count() == 30
            assert page.locator("#comparison .prompt-pair > article").count() == 90
            columns = ("v6_2_pr4417", "v6_2_pr4523", "v6_3_pr4417", "v6_3_pr4523", update.CELL)
            assert page.locator("#comparison .pair").evaluate_all(
                "rows=>rows.map(r=>[...r.querySelectorAll('.image-grid > .output > img')].map(i=>i.getAttribute('src')))") == [
                    [row["outputs"][column]["image"] for column in columns] for row in data["rows"]]
            assert page.locator("#comparison .pair").evaluate_all(
                "rows=>rows.map(r=>[...r.querySelectorAll('.image-grid > .output > h4')].map(h=>h.textContent))") == [
                    ["V6.2 / PR 4417 - V15.6", "V6.2 / PR 4523 - V15.7 shapes",
                     "V6.3 / PR 4417 - V15.6", "V6.3 / PR 4523 - V15.7 shapes", update.TITLE]] * 30
            for row in data["rows"]:
                for column in columns:
                    local_asset(update.urljoin(update.BASE, row["outputs"][column]["image"]))
                new = row["outputs"][update.CELL]
                for value in [new["record_url"], *new["inputs"].values()]:
                    local_asset(update.urljoin(update.BASE, value))
            for index in (0, 29):
                page.locator("#search").fill(data["rows"][index]["prompts"]["v6_3"]["prompt_key"])
                assert page.locator("#comparison > .pair").count() == 1
                images = page.locator("#comparison .image-grid > .output > img")
                images.evaluate_all("images=>images.forEach(i=>i.loading='eager')")
                images.first.scroll_into_view_if_needed()
                page.wait_for_function("""() => [...document.querySelectorAll(
                    '#comparison .image-grid > .output > img')].every(i=>i.complete&&i.naturalWidth===2368)""")
                assert images.evaluate_all(
                    "images=>Math.max(...images.map(i=>i.getBoundingClientRect().top))-Math.min(...images.map(i=>i.getBoundingClientRect().top))") < 1
            page.locator("#search").fill(data["rows"][0]["prompts"]["v6_3"]["prompt_key"])
            added = page.locator("#comparison .image-grid > .output").nth(4)
            assert data["rows"][0]["prompts"]["v6_4"]["text"] in page.locator("#comparison .prompt-pair").inner_text()
            source = page.locator("#comparison > .pair").get_by_text(
                "Full V6.4 Smart Brief + source messaging + camera input", exact=True)
            source.click()
            assert json.loads(source.locator("..").locator("pre").inner_text()) == data["rows"][0]["v6_4_source_input"]
            added.get_by_text("Geometry-guide image input", exact=True).click()
            added.get_by_text("Actual prepared product and Astra style reference", exact=True).click()
            added.locator("details[open] img").evaluate_all("images=>images.forEach(i=>i.loading='eager')")
            page.wait_for_function("""() => [...document.querySelectorAll(
                '#comparison .image-grid > .output:last-child details[open] img')].every(i=>i.complete&&i.naturalWidth>0)""")
            assert added.locator("details[open] img").count() == 3
            added.locator(":scope > img").click()
            assert page.locator("#lightbox").is_visible()
            page.locator("#closeImage").click()
            page.locator("#search").fill("")
            page.locator("#refresh").click()
            page.wait_for_function("document.querySelectorAll('#comparison > .pair').length===30")
            page.locator('[data-tab="prompts"]').click()
            assert page.locator("#prompts").is_visible()
            assert page.locator("#prompts .prompt").count() == 160
            page.locator('[data-tab="judges"]').click()
            assert page.locator("#judges").is_visible()
            page.locator('[data-tab="comparison"]').click()
            page.screenshot(path=str(HERE / "five_columns.png"))
            assert not errors, errors
            assert not missing, missing
        finally:
            browser.close()
finally:
    os.close(fd)

update.write(HERE / "browser_validation.json", {
    "status": "passed", "rows": 30, "generation_columns": 5, "output_bindings": 150,
    "historical_images_preserved": 30, "writer_records": 90, "all_v63_prompts_preserved": 160,
    "first_last_all_five_images_rendered": True, "new_column_inputs_rendered": 3,
    "lightbox_search_refresh_tabs_passed": True, "javascript_errors": errors,
    "manifest_sha256": update.digest((STAGING / update.MANIFEST_PATH).read_bytes()),
    "unrelated_historical_judge_images_not_exercised": len(excluded_judge_images),
    "network_boundary": "Exact comparison data/images with live-manifest hashes; IMS mocked. Unrelated historical judge iframe image requests aborted. Live gateway/IMS not certified."})
print("Passed:30 rows,150 exact output bindings,five aligned generation columns,inputs and preserved tabs.")
