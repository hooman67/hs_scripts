"""Exercise the four staged reports, real pixels and preserved browser-only review state."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from threading import Lock
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

import generate
import report
import study

HELPER = study.PRIOR / "check_browser.py"
spec = importlib.util.spec_from_file_location("hp_exact_file_browser_transport", HELPER)
if spec is None or spec.loader is None:
    raise RuntimeError("The completed study's exact-file browser transport is unavailable")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def main():
    root, _ = generate.verify()
    publication = study.load(study.HERE / "publication_manifest.json")
    media = study.load(study.HERE / "media_inventory.json")
    if media["baseline_bindings_sha256"] != study.sha(study.HERE / "baseline_bindings.json"):
        raise ValueError("Existing-media audit does not bind this verified baseline")
    known = publication["entries"]
    for item in known.values():
        if study.sha(item["path"]) != item["sha256"]:
            raise ValueError("Staged report asset changed before the browser gate")
    source = study.load(study.HERE / "source_manifest.json")
    source_paths = {
        item["key"]: {**item, "path": str(study.HERE / "source" / relative)}
        for relative, item in source["objects"].items()
    }
    c, lock, cached, failures = study.client(), Lock(), {}, []
    old_mode = [False]

    def local_asset(url):
        parsed = urlsplit(url)
        canonical = "https://foundry-aws-corp.adobe.io" + parsed.path
        key = study.key_for(canonical)
        if old_mode[0] and key in (study.FE_PREFIX + "/viewer.html", study.FE_PREFIX + "/data.json"):
            item = source_paths[key]
        elif key in known:
            item = known[key]
        elif key in source_paths:
            item = source_paths[key]
        elif canonical in media["objects"]:
            expected = media["objects"][canonical]
            with lock:
                if canonical not in cached:
                    if "cached_path" in expected:
                        path = Path(expected["cached_path"])
                        if study.sha(path) != expected["sha256"]:
                            raise ValueError("Previously decoded source image changed")
                    else:
                        response = c.get_object(Bucket=study.BUCKET, Key=key)
                        body = response["Body"].read()
                        if (response["ETag"] != expected["etag"]
                                or response.get("VersionId") != expected["version_id"]
                                or len(body) != expected["bytes"]
                                or response["ContentType"] != expected["content_type"]):
                            raise ValueError("Actual browser source differs from its checked object")
                        path = root / "browser_cache" / (study.digest(key.encode()) + Path(key).suffix)
                        study.emit(path, body)
                    cached[canonical] = path
                return cached[canonical]
        else:
            failures.append("Unapproved browser dependency: " + canonical)
            raise ValueError(failures[-1])
        path = Path(item["path"])
        if not (path.resolve().is_relative_to(root.resolve())
                or path.resolve().is_relative_to(study.HERE.resolve())):
            raise ValueError("Browser fixture escaped the two approved durable study roots")
        if study.sha(path) != item["sha256"]:
            raise ValueError("Browser fixture differs from frozen bytes")
        return path

    errors, writes = [], []
    captures = root / "browser_screenshots"
    captures.mkdir(exist_ok=True)
    with helper.serve_assets(local_asset) as origin, sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=str(helper.CHROME), args=["--no-sandbox", "--no-process-singleton"],
        )

        def page_for(width=2400):
            page = browser.new_page(viewport={"width": width, "height": 1250})
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("dialog", lambda dialog: dialog.accept())

            def handle(route):
                url = route.request.url
                if route.request.method not in ("GET", "HEAD"):
                    writes.append(url)
                    route.abort()
                elif url.startswith("https://auth-stg1.services.adobe.com/"):
                    route.fulfill(content_type="application/javascript", body=helper.IMS)
                elif "/annotations/" in urlsplit(url).path:
                    route.fulfill(status=404, body="Annotation reads mocked; synthetic writes blocked.")
                elif url.startswith(origin + "/"):
                    route.continue_()
                elif url.startswith(study.GATEWAY):
                    route.fulfill(status=302, headers={"Location": origin + urlsplit(url).path})
                else:
                    failures.append("Blocked external browser request: " + url)
                    route.abort()
            page.route("**/*", handle)
            return page

        def browse(url):
            return url.replace("https://foundry-aws-corp.adobe.io", origin, 1)

        def pixels(page, selector, dimensions=False):
            page.locator(selector).evaluate_all("imgs=>imgs.forEach(i=>i.loading='eager')")
            page.wait_for_function(
                """({selector,dimensions})=>[...document.querySelectorAll(selector)].every(
                i=>i.complete&&i.naturalWidth>0&&(!dimensions||
                (i.naturalWidth===2368&&i.naturalHeight===1776)))""",
                arg={"selector": selector, "dimensions": dimensions}, timeout=120000,
            )

        try:
            fe_url = publication["links"][1]
            page = page_for()
            old_mode[0] = True
            page.goto(browse(fe_url), wait_until="domcontentloaded")
            page.wait_for_selector(".row", timeout=60000)
            assert page.evaluate("QUESTIONS.length") == 5
            old_ids = page.evaluate("QUESTIONS.map(q=>q.id)")
            old_scope = page.evaluate("ANNO_KEY")
            old_keys = page.evaluate("MERGED.map(m=>m.key)")
            first = page.locator(".row").first
            first.locator(".q").nth(0).locator(".qopt").filter(has_text="Good").click()
            first.locator(".q").nth(4).locator(".qopt").filter(has_text="Bad").click()
            first.locator(".annos textarea").fill("Synthetic browser-only note: retain across sixth-column update")
            page.evaluate("setQNote(MERGED[0].key,QUESTIONS[1].id,'Synthetic question note')")
            old_anno = page.evaluate("JSON.parse(localStorage.getItem(ANNO_KEY))")
            old_mode[0] = False
            page.reload(wait_until="domcontentloaded")
            page.wait_for_selector(".row")
            assert page.evaluate("ANNO_KEY") == old_scope
            assert page.evaluate("QUESTIONS.map(q=>q.id).slice(0,5)") == old_ids
            assert page.evaluate("MERGED.map(m=>m.key)") == old_keys
            assert page.evaluate("JSON.parse(localStorage.getItem(ANNO_KEY))") == old_anno

            for url, path, count, name in (
                (fe_url, report.STAGING / "fe/data.json", 6, "six_columns"),
                (publication["links"][2], report.PUBLIC / "fe/data.json", 2, "paired_columns"),
            ):
                data = study.load(path)
                if count == 2:
                    page.goto(browse(url), wait_until="domcontentloaded")
                    page.wait_for_selector(".row")
                    assert page.evaluate("ANNO_KEY") != old_scope
                    assert page.evaluate("Object.keys(ANNO).length") == 0
                assert page.evaluate("MERGED.length") == 160
                assert page.evaluate("QUESTIONS.length") == count
                assert page.evaluate("SOURCES[0].rows") == data["rows"]
                first = page.locator(".row").first
                assert first.locator(".asset").count() == count
                assert first.locator(".cap .body").all_text_contents() == [
                    a["text_content"] for a in data["rows"][0]["images"] if a["asset_type"] == "text"
                ]
                pixels(page, ".row .asset img")
                tops = first.locator(".asset").evaluate_all(
                    "tiles=>tiles.map(i=>Math.round(i.getBoundingClientRect().top))")
                assert len(set(tops)) == 1, tops
                first.locator(".q").nth(count - 1).locator(".qopt").filter(has_text="Good").click()
                page.reload(wait_until="domcontentloaded")
                page.wait_for_selector(".row")
                assert page.evaluate("ANNO[MERGED[0].key].answers[QUESTIONS[QUESTIONS.length-1].id]") == "good"
                if count == 6:
                    assert page.evaluate("ANNO[MERGED[0].key].note") == next(iter(old_anno.values()))["note"]
                    assert page.evaluate("ANNO[MERGED[0].key].answers[QUESTIONS[4].id]") == "bad"
                    assert page.evaluate("ANNO[MERGED[0].key].qnotes[QUESTIONS[1].id]") == "Synthetic question note"
                page.locator("#allMethodsGood").click()
                assert page.evaluate("MERGED.every(m=>QUESTIONS.every(q=>ANNO[m.key].answers[q.id]==='good'))")
                with page.expect_download() as downloaded:
                    page.locator("#exportRatings").click()
                export = json.loads(Path(downloaded.value.path()).read_text())
                assert len(export["rows"]) == 160 and len(export["questions"]) == count
                assert sum(len(row["answers"]) for row in export["rows"]) == 160 * count
                page.screenshot(path=str(captures / (name + "_desktop.png")))
                page.goto(browse(url) + "&rows=160", wait_until="domcontentloaded")
                page.wait_for_selector(".row")
                assert page.evaluate("MERGED.length") == 1
                assert page.locator(".asset img").evaluate_all("imgs=>imgs.map(i=>i.getAttribute('src'))") == [
                    a["image_src"] for a in data["rows"][-1]["images"] if a["asset_type"] == "image"
                ]
                pixels(page, ".row .asset img")
                page.set_viewport_size({"width": 390, "height": 844})
                assert page.locator(".asset").count() == count
                page.screenshot(path=str(captures / (name + "_mobile.png")))
                page.set_viewport_size({"width": 2400, "height": 1250})
            page.close()

            for url, path, name in (
                (publication["links"][0], report.STAGING / "grouped/data_v6_5_pr4619_20261112.json", "three_experiments"),
                (publication["links"][3], report.PUBLIC / "gallery/data.json", "paired_groups"),
            ):
                data = study.load(path)
                page = page_for(1800)
                page.goto(browse(url), wait_until="domcontentloaded")
                page.wait_for_function("n=>document.querySelectorAll('.card').length===n",
                                       arg=data["image_count"], timeout=120000)
                assert page.evaluate("DATA") == data
                assert page.locator(".input-group").count() == 16
                assert page.locator(".experiment").count() == 16 * data["experiment_count"]
                assert page.locator(".source-prompt[open],.input-context[open]").count() == 0
                actual = page.locator(".card").evaluate_all("""cards=>cards.map(c=>({
                    key:c.dataset.promptKey,rank:Number(c.dataset.rank),
                    image:c.querySelector('.card-image').getAttribute('src'),
                    prompt:c.querySelector('.source-prompt p').textContent}))""")
                assert actual == [{
                    "key": card["prompt_key"], "rank": card["rank"],
                    "image": card["image"], "prompt": card["prompt"],
                } for group in data["groups"] for experiment in group["experiments"] for card in experiment["cards"]]
                for group in (data["groups"][0], data["groups"][-1]):
                    page.locator("#bank").select_option(group["id"])
                    for experiment in group["experiments"]:
                        page.locator("#experiment").select_option(experiment["id"])
                        assert page.locator(".card").count() == 10
                        pixels(page, ".card-image", True)
                        tops = page.locator(".card-image").evaluate_all(
                            "imgs=>imgs.map(i=>Math.round(i.getBoundingClientRect().top))")
                        assert len(set(tops[:5])) == len(set(tops[5:])) == 1 and tops[5] > tops[0]
                        if experiment["id"] in (report.CELL, report.BASELINE_CELL):
                            assert page.locator(".statistics-status").all_text_contents() == [
                                card["statistics_status"] for card in experiment["cards"]
                            ]
                page.locator("#bank").select_option(data["groups"][0]["id"])
                page.locator("#experiment").select_option(report.CELL)
                page.locator("#showPrompts").check()
                assert page.locator(".source-prompt[open]").count() == 10
                page.locator("#showPrompts").uncheck()
                page.locator(".card").first.locator(".model-inputs>summary").click()
                pixels(page, ".card:first-child .model-inputs img")
                page.locator(".card").first.locator(".model-inputs>summary").click()
                page.locator(".card-image").first.click()
                assert page.locator("#lightbox").is_visible()
                page.keyboard.press("Escape")
                page.locator("#columns").evaluate(
                    "e=>{e.value='3';e.dispatchEvent(new Event('input',{bubbles:true}))}")
                assert page.locator(".cards").first.evaluate(
                    "e=>getComputedStyle(e).gridTemplateColumns.split(' ').length") == 3
                page.locator("#columns").evaluate(
                    "e=>{e.value='5';e.dispatchEvent(new Event('input',{bubbles:true}))}")
                page.locator("#experiment").select_option("")
                page.screenshot(path=str(captures / (name + "_desktop.png")))
                page.set_viewport_size({"width": 390, "height": 844})
                page.screenshot(path=str(captures / (name + "_mobile.png")))
                overflow = page.locator("body *").evaluate_all("""nodes=>nodes.filter(n=>
                    n.getBoundingClientRect().right>innerWidth+1&&n.getBoundingClientRect().width>0
                    ).slice(0,12).map(n=>({tag:n.tagName,id:n.id,cls:n.className,
                    right:n.getBoundingClientRect().right,text:n.textContent.slice(0,100)}))""")
                assert page.evaluate("document.documentElement.scrollWidth<=innerWidth"), overflow
                assert not page.locator("#error").inner_text()
                page.close()
            assert not errors, errors
            assert not failures, failures
            assert not writes, writes
        finally:
            browser.close()
    study.emit(study.HERE / "browser_validation.json", {
        "at_utc": study.now(), "passed": True, "reports": 4,
        "report_image_bindings": [480, 960, 320, 320],
        "old_five_method_ids_row_ids_ratings_comments_and_storage_scope_preserved": True,
        "new_sixth_rating_and_reload_persistence": True, "pair_has_independent_review_storage": True,
        "rating_exports_answers": [960, 320], "six_and_two_column_desktop_no_wrap": True,
        "grouped_all_bindings_and_first_last_ten_actual_pixels_checked": True,
        "source_prompts_actual_inputs_statistics_filters_and_lightbox_checked": True,
        "ims_and_annotation_reads": "mocked; live SSO/server annotation writes not certified",
        "external_writes": writes, "javascript_errors": errors,
        "publication_manifest_sha256": study.sha(study.HERE / "publication_manifest.json"),
        "media_inventory_sha256": study.sha(study.HERE / "media_inventory.json"),
        "checker_sha256": study.sha(Path(__file__)), "transport_helper_sha256": study.sha(HELPER),
    })
    print({"browser_passed": True, "reports": 4, "rating_answers": [960, 320]})


if __name__ == "__main__":
    main()
