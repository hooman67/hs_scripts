"""Execute the four actual reports and raw images in Chromium; mock IMS/annotation reads only."""
from __future__ import annotations

import json
import mimetypes
from contextlib import contextmanager
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import unquote, urljoin, urlsplit

from playwright.sync_api import sync_playwright

import report
import study

CHROME = Path("/mnt/localssd/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome")
IMS = """
window.adobeImsFactory={createIMSLib(config,key){window[key]={
 initialize(){config.onAccessToken({token:"LOCAL-IMS-MOCK"});setTimeout(()=>config.onReady({}),0)},
 isSignedInUser(){return true},getProfile(){return Promise.resolve({displayName:"Local UI test",account_type:"test"})},
 getAccessToken(){return {token:"LOCAL-IMS-MOCK"}},signIn(){},signOut(){}}}};
"""


@contextmanager
def serve_assets(local_asset):
    class Handler(SimpleHTTPRequestHandler):
        def translate_path(self, path):
            return str(local_asset("https://foundry-aws-corp.adobe.io" + path))

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def main():
    frozen = study.verify()
    publication = study.load(study.HERE / "publication_manifest.json")
    known = dict(publication["entries"])
    for name, metadata in frozen["baseline_live_objects"].items():
        known.setdefault(metadata["key"], {**metadata, "path": str(study.HERE / "baseline_live" / name)})
    for directory in (
        study.COMPARISON.name, study.LEGACY.name, "hp_lifestyle_v6_4_pr4523_30_20261110", study.PRIOR.name,
    ):
        root = study.HERE.parent / directory / "public"
        for name, metadata in study.load(root / "asset_manifest.json")["assets"].items():
            known.setdefault("eval_sets/" + directory + "/" + name, {**metadata, "path": str(root / name)})
    verified = {}
    errors = []

    def local_asset(url):
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc != "foundry-aws-corp.adobe.io":
            raise ValueError(f"unapproved browser origin: {url}")
        prefix = f"/asset/{study.BUCKET}/"
        if not parsed.path.startswith(prefix):
            raise ValueError("unapproved browser bucket")
        key = unquote(parsed.path[len(prefix):])
        if key not in known:
            raise ValueError(f"browser asset absent from exact inventory: {key}")
        item = known[key]
        path = Path(item["path"])
        if not path.resolve().is_relative_to(study.PROJECT.resolve()):
            raise ValueError("browser fixture escaped project")
        if path not in verified:
            verified[path] = study.sha(path)
            if verified[path] != item["sha256"]:
                raise ValueError(f"browser fixture differs from frozen bytes: {key}")
        return path

    four = study.load(report.STAGING / "grouped" / report.GROUP_DATA)
    two = study.load(report.PUBLIC / "gallery/data.json")
    full = study.load(report.STAGING / "full" / report.FULL_DATA)
    fe = study.load(report.STAGING / "full/fe/data.json")
    columns = ("v6_3_pr4417", "v6_3_pr4523", "v6_4_pr4523", report.CELL)
    full_base = study.GATEWAY + report.FULL + "/gallery/index.html"
    grouped_reports = (
        (report.BASE + "gallery/index.html", two, "two_versions"),
        (study.GATEWAY + report.GROUPED + "/gallery/index.html", four, "four_experiments"),
    )
    for row in full["rows"]:
        for column in columns:
            output = row["outputs"][column]
            path = local_asset(urljoin(full_base, output["image"]))
            if verified[path] != output["image_sha256"]:
                raise ValueError("detailed output differs from actual raw PNG")
            for value in output["inputs"].values():
                local_asset(urljoin(full_base, value))
    for url, data, _name in grouped_reports:
        for group in data["groups"]:
            for experiment in group["experiments"]:
                for card in experiment["cards"]:
                    path = local_asset(urljoin(url, card["image"]))
                    if verified[path] != card["image_sha256"]:
                        raise ValueError("grouped output differs from actual raw PNG")
                    for value in card.get("inputs", {}).values():
                        local_asset(urljoin(url, value))
    if not CHROME.is_file():
        raise FileNotFoundError("actual installed Chromium executable is unavailable")
    with serve_assets(local_asset) as origin, sync_playwright() as playwright:
        def browse_url(url):
            return url.replace("https://foundry-aws-corp.adobe.io", origin, 1)

        browser = playwright.chromium.launch(
            executable_path=str(CHROME), args=["--no-sandbox", "--no-process-singleton"],
        )
        try:
            page = browser.new_page(viewport={"width": 1800, "height": 1100})
            page.on("pageerror", lambda error: errors.append(str(error)))

            def handle(route):
                if route.request.url.startswith("https://auth-stg1.services.adobe.com/"):
                    route.fulfill(content_type="application/javascript", body=IMS)
                elif "/fe/annotations/" in urlsplit(route.request.url).path:
                    route.fulfill(status=404, body="Annotation reads mocked; no writes are tested.")
                elif route.request.url.startswith(origin + "/"):
                    route.continue_()
                else:
                    path = local_asset(route.request.url)
                    route.fulfill(path=str(path), content_type=mimetypes.guess_type(path.name)[0]
                                  or "application/octet-stream")

            page.route("**/*", handle)
            for url, data, name in grouped_reports:
                page.goto(browse_url(url), wait_until="domcontentloaded")
                page.wait_for_function(
                    "(n)=>document.querySelectorAll('.card').length===n",
                    arg=data["image_count"], timeout=120000,
                )
                assert page.locator(".input-group").count() == 16
                assert page.locator(".experiment").count() == 16 * data["experiment_count"]
                assert page.locator(".source-prompt[open],.input-context[open]").count() == 0
                expected = [{
                    "id": group["id"], "experiments": [{
                        "id": experiment["id"], "cards": [{
                            "rank": card["rank"], "key": card["prompt_key"],
                            "image": card["image"], "prompt": card["prompt"],
                        } for card in experiment["cards"]],
                    } for experiment in group["experiments"]],
                } for group in data["groups"]]
                assert page.locator(".input-group").evaluate_all("""groups=>groups.map(group=>({
                    id:group.id,experiments:[...group.querySelectorAll('.experiment')].map(experiment=>({
                    id:experiment.dataset.experiment,cards:[...experiment.querySelectorAll('.card')].map(card=>({
                      rank:Number(card.dataset.rank),key:card.dataset.promptKey,
                      image:card.querySelector('.card-image').getAttribute('src'),
                      prompt:card.querySelector('.source-prompt p').textContent
                    }))}))
                }))""") == expected
                assert page.evaluate("DATA.groups.map(g=>g.contexts)") == [g["contexts"] for g in data["groups"]]
                assert f"/ {data['image_count']} images" in page.locator("#status").inner_text()
                for group in (data["groups"][0], data["groups"][-1]):
                    page.locator("#bank").select_option(group["id"])
                    for experiment in group["experiments"]:
                        page.locator("#experiment").select_option(experiment["id"])
                        assert page.locator(".card").count() == 10
                        images = page.locator(".card-image")
                        images.evaluate_all("images=>images.forEach(i=>i.loading='eager')")
                        images.first.scroll_into_view_if_needed()
                        page.wait_for_function("""()=>[...document.querySelectorAll('.card-image')]
                            .every(i=>i.complete&&i.naturalWidth===2368&&i.naturalHeight===1776)""",
                            timeout=120000)
                        tops = images.evaluate_all("images=>images.map(i=>Math.round(i.getBoundingClientRect().top))")
                        assert len(set(tops[:5])) == len(set(tops[5:])) == 1 and tops[5] > tops[0]
                page.locator("#bank").select_option(data["groups"][0]["id"])
                page.locator("#experiment").select_option(report.CELL)
                page.locator("#showPrompts").check()
                assert page.locator(".source-prompt[open]").count() == 10
                page.locator("#showPrompts").uncheck()
                page.locator(".input-context>summary").click()
                page.locator(".source-context>summary").last.click()
                contexts = page.locator(".source-context").last.locator("pre").all_text_contents()
                assert contexts == [
                    value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
                    for value in (
                        data["groups"][0]["contexts"][-1]["input"]["smart_brief"],
                        data["groups"][0]["contexts"][-1]["input"]["source_messaging"],
                    )
                ]
                page.locator(".input-context>summary").click()
                first = page.locator(".card").first
                first.locator(".model-inputs>summary").click()
                first.locator(".model-inputs img").evaluate_all("images=>images.forEach(i=>i.loading='eager')")
                first.locator(".model-inputs img").last.scroll_into_view_if_needed()
                page.wait_for_function("""()=>[...document.querySelector('.card .model-inputs')
                    .querySelectorAll('img')].every(i=>i.complete&&i.naturalWidth>0)""", timeout=60000)
                assert first.locator(".model-inputs img").count() == 3
                first.locator(".model-inputs>summary").click()
                first.locator(".card-image").click()
                assert page.locator("#lightbox").is_visible()
                assert page.locator("#originalImage").get_attribute("href") == urljoin(
                    browse_url(url), data["groups"][0]["experiments"][-1]["cards"][0]["image"])
                page.keyboard.press("Escape")
                page.locator("#columns").evaluate("e=>{e.value='3';e.dispatchEvent(new Event('input',{bubbles:true}))}")
                assert page.locator(".cards").first.evaluate(
                    "e=>getComputedStyle(e).gridTemplateColumns.split(' ').length") == 3
                page.locator("#columns").evaluate("e=>{e.value='5';e.dispatchEvent(new Event('input',{bubbles:true}))}")
                page.locator("#experiment").select_option("")
                page.evaluate("window.scrollTo(0,0)")
                page.screenshot(path=str(study.HERE / (name + "_desktop.png")))
                page.set_viewport_size({"width": 390, "height": 844})
                assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
                assert page.locator(".cards").first.evaluate(
                    "e=>getComputedStyle(e).gridTemplateColumns.split(' ').length") == 2
                page.screenshot(path=str(study.HERE / (name + "_mobile.png")))
                assert not page.locator("#error").inner_text()
                page.set_viewport_size({"width": 1800, "height": 1100})
            page.close()
            page = browser.new_page(viewport={"width": 1800, "height": 1100})
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("crash", lambda _page: errors.append("Chromium detailed-view renderer crashed"))
            page.route("**/*", handle)
            page.goto(browse_url(full_base), wait_until="domcontentloaded")
            page.wait_for_function("document.querySelectorAll('#comparison>.pair').length===160", timeout=120000)
            assert page.locator(".image-grid>.output").count() == 640
            assert page.locator(".pair").evaluate_all("""rows=>rows.map(r=>
                [...r.querySelectorAll('.image-grid>.output>img')].map(i=>i.getAttribute('src')))""") == [
                    [row["outputs"][column]["image"] for column in columns] for row in full["rows"]
                ]
            for index in (0, 159):
                page.locator("#search").fill(full["rows"][index]["prompt"]["prompt_key"])
                assert page.locator(".pair").count() == 1
                page.locator(".image-grid>.output>img").evaluate_all(
                    "images=>images.forEach(i=>i.loading='eager')")
                page.wait_for_function("""()=>[...document.querySelectorAll('.image-grid>.output>img')]
                    .every(i=>i.complete&&i.naturalWidth===2368&&i.naturalHeight===1776)""", timeout=120000)
                assert full["rows"][index]["prompt_v6_5"]["text"] in page.locator(".pair").inner_text()
            page.locator("#search").fill("")
            page.locator("#state").select_option("reused")
            assert page.locator(".pair").count() == 30
            page.locator("#state").select_option("")
            page.locator("#refresh").click()
            page.wait_for_function("document.querySelectorAll('#comparison>.pair').length===160")
            page.screenshot(path=str(study.HERE / "full160_four_columns.png"))
            fe_base = study.GATEWAY + report.FULL + "/fe/viewer.html?ldap=hshariati"
            page.close()
            page = browser.new_page(viewport={"width": 1800, "height": 1100})
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.route("**/*", handle)
            page.goto(browse_url(fe_base), wait_until="domcontentloaded")
            page.locator("#setupSkip").click()
            page.wait_for_selector(".row")
            assert page.evaluate("MERGED.length") == 160
            assert page.evaluate("SOURCES[0].rows.map(r=>r.images.map(i=>i.image_src))") == [
                [image["image_src"] for image in row["images"]] for row in fe["rows"]
            ]
            assert page.locator(".row").first.locator(".asset").count() == 4
            assert page.locator(".caps,.mfold,.asset.input").count() == 0
            assert page.evaluate("SOURCES[0].links.length") == 0
            page.wait_for_function("""()=>[...document.querySelector('.row').querySelectorAll('img')]
                .every(i=>i.complete&&i.naturalWidth===2368&&i.naturalHeight===1776)""", timeout=120000)
            page.screenshot(path=str(study.HERE / "fe_four_columns.png"))
            page.goto(browse_url(fe_base) + "&rows=160", wait_until="domcontentloaded")
            page.wait_for_selector(".row")
            assert page.evaluate("MERGED.length") == 1
            assert page.locator(".rowhead .rowidx").first.inner_text() == fe["rows"][-1]["meta_data"]["evalset_item_id"]
            page.wait_for_function("""()=>[...document.querySelector('.row').querySelectorAll('img')]
                .every(i=>i.complete&&i.naturalWidth===2368&&i.naturalHeight===1776)""", timeout=120000)
            assert not errors, errors
        except Exception as error:
            print(json.dumps({"browser_error": str(error), "javascript_errors": errors,
                              "last_page_url": page.url}), flush=True)
            raise
        finally:
            browser.close()
    report.emit(study.HERE / "browser_validation.json", {
        "passed": True, "at_utc": study.now(), "grouped_input_banks": 16,
        "new_two_version_image_bindings": 320, "existing_four_experiment_bindings": 640,
        "detailed_four_column_bindings": 640, "fe_four_column_bindings": 640,
        "all_actual_output_hashes_and_source_inputs_verified": True,
        "first_last_banks_all_ten_raw_images_per_experiment_rendered": True,
        "collapsed_prompts_inputs_filters_size_lightbox_desktop_mobile": True,
        "official_fe_viewer_and_old_row_annotation_ids_unchanged": True,
        "javascript_errors": errors, "ims_and_annotation_reads": "mocked; writes/live gateway not certified",
        "asset_transport": "exact hash-checked files over temporary loopback HTTP; original paths preserved",
        "publication_manifest_sha256": study.sha(study.HERE / "publication_manifest.json"),
        "checker_sha256": study.sha(Path(__file__)),
    })
    print(json.dumps({"browser_passed": True, "reports": 4, "grouped_images": [320, 640]}))


if __name__ == "__main__":
    main()
