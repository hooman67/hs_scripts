"""Exercise the actual five-column review, images, prompts and browser-only ratings."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import mimetypes
from pathlib import Path
import sys
from threading import Lock
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

import build_report as build

sys.path.append(str(build.V65))
spec = importlib.util.spec_from_file_location("completed_v65_browser", build.V65 / "check_browser.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Exact-file HTTP browser helper is unavailable")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def main():
    build.verify()
    publication = build.study.load(build.HERE / "publication_manifest.json")
    data = build.study.load(build.PUBLIC / "data.json")
    heads = build.study.load(build.HERE / "image_head_audit.json")
    if heads["image_bindings"] != 800 or heads["v65_hash_metadata_matches"] != 160:
        raise ValueError("All image objects must be checked before the browser gate")
    known = {
        build.PREFIX + "/" + name: Path(item["path"])
        for name, item in publication["files"].items()
    }
    v65 = {item["v65_image"]: item["v65_image_sha256"]
           for item in build.study.load(build.PUBLIC / "provenance.json")["row_mapping"]}
    client = build.study.s3_client()
    lock = Lock()
    cache = build.HERE / "browser_images"
    cache.mkdir(exist_ok=True)
    cached = {}

    def local_asset(url):
        parsed = urlsplit(url)
        canonical = "https://foundry-aws-corp.adobe.io" + parsed.path
        key = build.study.key_for(canonical)
        if key in known:
            path = known[key]
            if build.study.sha(path) != publication["files"][path.name]["sha256"]:
                raise ValueError("Built report changed during browser execution")
            return path
        if canonical not in heads["images"]:
            raise ValueError(f"Browser requested an unapproved asset: {canonical}")
        with lock:
            if canonical in cached:
                return cached[canonical]
            response = client.get_object(Bucket=build.study.BUCKET, Key=key)
            body = response["Body"].read()
            expected = heads["images"][canonical]
            if (
                response["ETag"] != expected["etag"]
                or response.get("VersionId") != expected["version_id"]
                or len(body) != expected["bytes"]
                or (canonical in v65 and hashlib.sha256(body).hexdigest() != v65[canonical])
            ):
                raise ValueError("Actual browser image differs from the checked source object")
            path = cache / (hashlib.sha256(key.encode()).hexdigest() + ".png")
            build.emit(path, body)
            cached[canonical] = path
            return path

    labels = [a["meta_text"]["label"] for a in data["rows"][0]["images"][:5]]
    errors = []
    writes = []
    with helper.serve_assets(local_asset) as origin, sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=str(helper.CHROME), args=["--no-sandbox", "--no-process-singleton"],
        )
        try:
            page = browser.new_page(viewport={"width": 2100, "height": 1250})
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
                    route.fulfill(status=404, body="Annotation reads mocked; no writes permitted.")
                elif url.startswith(origin + "/"):
                    route.continue_()
                else:
                    path = local_asset(url)
                    route.fulfill(path=str(path), content_type=mimetypes.guess_type(path.name)[0]
                                  or "application/octet-stream")

            page.route("**/*", handle)
            url = publication["url"].replace("https://foundry-aws-corp.adobe.io", origin, 1)
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_selector(".row", timeout=60000)
            assert page.evaluate("MERGED.length") == 160
            assert page.evaluate("QUESTIONS.map(q=>q.text)") == labels
            assert page.evaluate("SOURCES[0].rows") == data["rows"]
            assert page.locator("#columnChangeSummary section").count() == 5
            first = page.locator(".row").first
            assert first.locator(".asset").count() == 5
            assert first.locator(".cap").count() == 2
            assert first.locator(".cap .body").all_text_contents() == [
                data["rows"][0]["images"][index]["text_content"] for index in (5, 6)
            ]
            assert first.locator(".asset img").evaluate_all(
                "images=>images.map(i=>i.getAttribute('src'))"
            ) == [a["image_src"] for a in data["rows"][0]["images"][:5]]
            first.locator(".asset img").evaluate_all("images=>images.forEach(i=>i.loading='eager')")
            page.wait_for_function("""()=>[...document.querySelector('.row').querySelectorAll('.asset img')]
                .every(i=>i.complete&&i.naturalWidth>0)""", timeout=120000)
            tops = first.locator(".asset").evaluate_all(
                "tiles=>tiles.map(i=>Math.round(i.getBoundingClientRect().top))")
            assert len(set(tops)) == 1, tops
            assert first.locator(".q").count() == 5
            first.locator(".q").nth(4).locator(".qopt").filter(has_text="Good").click()
            assert page.evaluate(
                "Object.values(ANNO).some(a=>a.answers&&a.answers[QUESTIONS[4].id]==='good')"
            )
            page.reload(wait_until="domcontentloaded")
            page.wait_for_selector(".row")
            assert page.evaluate(
                "Object.values(ANNO).some(a=>a.answers&&a.answers[QUESTIONS[4].id]==='good')"
            )
            assert build.PREFIX in page.evaluate("ANNO_KEY")
            page.locator("#allMethodsGood").click()
            assert page.evaluate(
                "MERGED.every(m=>QUESTIONS.every(q=>ANNO[m.key].answers[q.id]==='good'))"
            )
            with page.expect_download() as download:
                page.locator("#exportRatings").click()
            downloaded = download.value.path()
            if downloaded is None:
                raise RuntimeError("Ratings JSON download did not complete")
            payload = json.loads(Path(downloaded).read_text())
            assert len(payload["questions"]) == 5
            assert len(payload["rows"]) == 160
            assert all(len(row["answers"]) == 5 for row in payload["rows"])
            page.screenshot(path=str(build.HERE / "five_columns_desktop.png"))
            page.goto(url + "&rows=160", wait_until="domcontentloaded")
            page.wait_for_selector(".row")
            assert page.evaluate("MERGED.length") == 1
            last = page.locator(".row").first
            assert last.locator(".asset img").evaluate_all(
                "images=>images.map(i=>i.getAttribute('src'))"
            ) == [a["image_src"] for a in data["rows"][-1]["images"][:5]]
            assert last.locator(".cap .body").all_text_contents() == [
                data["rows"][-1]["images"][index]["text_content"] for index in (5, 6)
            ]
            last.locator(".asset img").evaluate_all("images=>images.forEach(i=>i.loading='eager')")
            page.wait_for_function("""()=>[...document.querySelector('.row').querySelectorAll('.asset img')]
                .every(i=>i.complete&&i.naturalWidth>0)""", timeout=120000)
            page.set_viewport_size({"width": 390, "height": 844})
            assert last.locator(".asset").count() == 5
            page.screenshot(path=str(build.HERE / "five_columns_mobile.png"))
            assert not errors, errors
            assert not writes, writes
        finally:
            browser.close()
    build.emit(build.HERE / "browser_validation.json", {
        "passed": True, "at_utc": build.study.now(), "rows": 160, "image_bindings": 800,
        "image_columns": 5, "source_prompts": 320, "all_loaded_rows_match_exact_data": True,
        "first_last_actual_images_and_both_prompts_rendered": True,
        "five_side_by_side_desktop_columns": True, "five_ratings_and_reload_persistence": True,
        "bulk_rating_and_160_row_800_answer_json_export": True,
        "browser_only_synthetic_ratings": True, "external_writes": writes,
        "ims_and_annotation_reads": "mocked; live SSO/publishing not certified",
        "javascript_errors": errors, "original_report_not_modified": True,
        "publication_manifest_sha256": build.study.sha(build.HERE / "publication_manifest.json"),
        "checker_sha256": build.study.sha(Path(__file__)),
        "transport_helper_sha256": build.study.sha(build.V65 / "check_browser.py"),
    })
    print(json.dumps({"browser_passed": True, "rows": 160, "columns": 5, "ratings_export_answers": 800}))


if __name__ == "__main__":
    main()
