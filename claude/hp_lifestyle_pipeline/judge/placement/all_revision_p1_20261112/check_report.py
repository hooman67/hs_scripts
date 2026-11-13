"""Verify exact actual judgments and four-column layout in the completed gallery."""

import json
import mimetypes
from pathlib import Path
from urllib.parse import urlsplit

import complete
import report
from playwright.sync_api import sync_playwright


def main():
    root = Path(__file__).resolve().parent
    audit = report.verify_build()
    source = complete.load(root / "source/object.json")
    document = complete.load(root / "gallery" / audit["results_filename"])
    records = {row["image_url"]: row for row in document["records"]}
    plan = complete.verify_plan()
    assets = {
        row[role]["url"]: row[role]
        for row in plan["cases"]
        for role in ("generated_image", "twin_image")
    }
    url = report.OLD.BASE + source["key"]
    prefix = url.rsplit("/", 1)[0] + "/"
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path="/mnt/localssd/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome",
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        page = browser.new_page(viewport={"width": 1700, "height": 1100})
        page.on("pageerror", lambda error: errors.append(str(error)))

        def route(request):
            target = request.request.url
            assert request.request.method == "GET"
            if target in assets:
                asset = assets[target]
                assert complete.sha(asset["local_path"]) == asset["sha256"]
                request.fulfill(
                    body=Path(asset["local_path"]).read_bytes(),
                    content_type=mimetypes.guess_type(asset["local_path"])[0],
                )
            elif target.startswith(prefix):
                name = urlsplit(target).path.rsplit("/", 1)[1]
                directory = (
                    "gallery"
                    if name in ("viewer.html", audit["results_filename"])
                    else "source"
                )
                path = root / directory / name
                assert path.is_file(), str(path)
                request.fulfill(
                    body=path.read_bytes(),
                    content_type="text/html; charset=utf-8"
                    if name.endswith(".html")
                    else "application/json; charset=utf-8",
                )
            elif target.endswith("/favicon.ico"):
                request.fulfill(status=404, body="")
            else:
                raise AssertionError("Unexpected browser resource: " + target)

        page.route("**/*", route)
        page.goto(url, wait_until="load")
        for selector, expected in (
            ("section", 32),
            (".row", 32),
            (".row>figure", 128),
            (".placement-judge", 128),
            (".v31-result", 256),
            (".astra-result", 1024),
            (".astra-previous", 128),
            (".astra-result.not-evaluated", 366),
            (".astra-result.error", 2),
            ('.astra-result[data-astra-candidate="p1"]', 512),
            (".astra-previous[open]", 0),
        ):
            assert page.locator(selector).count() == expected, selector
        columns = page.locator(".row>figure").evaluate_all(
            """figures=>figures.map(figure=>({
                url:figure.querySelector('img').src,
                results:[...figure.querySelectorAll('.astra-result')].map(node=>({
                    version:node.dataset.astraVersion,candidate:node.dataset.astraCandidate,
                    sha:node.dataset.imageSha256,title:node.querySelector('strong').textContent,
                    reason:node.querySelector('p')?.textContent,
                    components:node.querySelector('pre')?.textContent,
                    failed:node.querySelector('.failed-check')?.textContent
                }))
            }))"""
        )
        for column in columns:
            expected = records[column["url"]]
            assert len(column["results"]) == 8
            assert [value["candidate"] for value in column["results"]] == ["p1"] * 4 + [
                "p2"
            ] * 4
            for value in column["results"]:
                actual = expected["results"][value["version"]][value["candidate"]]
                assert value["sha"] == expected["image_sha256"]
                assert value["title"].startswith(
                    report.OLD.label(value["version"], value["candidate"]) + ": "
                )
                if actual is None:
                    assert value["candidate"] == "p2"
                    assert value["title"].endswith("NOT EVALUATED | no score")
                elif actual["status"] == "error":
                    assert value["candidate"] == "p2"
                    assert value["title"].endswith("ERROR | no score")
                    assert (
                        value["reason"] == actual["error_type"] + ": " + actual["error"]
                    )
                else:
                    assert value["title"].endswith(
                        f"{actual['verdict'].upper()} | {actual['score']:g}/100"
                    )
                    assert value["reason"] == actual["observation"]["summary"]
                    assert (
                        json.loads(value["components"])
                        == actual["observation"]["components"]
                    )
                    missed = [
                        key
                        for key, matched in (actual.get("checks") or {}).items()
                        if not matched
                    ]
                    assert all(key in value["failed"] for key in missed)

        def alignment():
            rows = page.locator(".row").evaluate_all(
                """rows=>rows.map(row=>[...row.children].map(figure=>({
                    priorBottom:figure.querySelector('[data-v31-version="r2"]').getBoundingClientRect().bottom,
                    primary:[...figure.children].filter(node=>node.classList.contains('astra-result'))
                      .map(node=>({top:node.getBoundingClientRect().top,bottom:node.getBoundingClientRect().bottom})),
                    other:figure.querySelector('.astra-previous').getBoundingClientRect().top
                })))"""
            )
            for row in rows:
                assert all(len(cell["primary"]) == 4 for cell in row)
                for index in range(4):
                    tops = [cell["primary"][index]["top"] for cell in row]
                    previous = [
                        cell["priorBottom"]
                        if index == 0
                        else cell["primary"][index - 1]["bottom"]
                        for cell in row
                    ]
                    assert max(tops) - min(tops) <= 1
                    assert min(tops) >= max(previous) - 1
                assert (
                    max(cell["other"] for cell in row)
                    - min(cell["other"] for cell in row)
                    <= 1
                )
                assert (
                    min(cell["other"] for cell in row)
                    >= max(cell["primary"][-1]["bottom"] for cell in row) - 1
                )

        alignment()
        page.locator(".placement-judge").first.evaluate("node=>node.open=true")
        page.locator('.astra-result[data-astra-candidate="p1"] details').first.evaluate(
            "node=>node.open=true"
        )
        alignment()
        page.locator(".astra-previous").first.evaluate("node=>node.open=true")
        alignment()
        for index in (0, 127):
            image = page.locator(".row>figure>a>img").nth(index)
            image.scroll_into_view_if_needed()
            image.evaluate("node=>node.loading='eager'")
            page.wait_for_function(
                """i=>{const img=document.querySelectorAll('.row>figure>a>img')[i];
                       return img.complete&&img.naturalWidth>0}""",
                arg=index,
            )
        downloads = sorted(
            set(
                page.locator("a").evaluate_all(
                    "nodes=>nodes.map(node=>node.href).filter(href=>href.endsWith('.json'))"
                )
            )
        )
        assert len(downloads) == 3
        for target in downloads:
            value = page.evaluate(
                """async url=>{const response=await fetch(url);
                  return {ok:response.ok,count:(await response.json()).records.length}}""",
                target,
            )
            assert value["ok"] and value["count"] == 128
        assert not errors, errors
        page.locator(".placement-judge").first.evaluate("node=>node.open=false")
        page.locator('.astra-result[data-astra-candidate="p1"] details').first.evaluate(
            "node=>node.open=false"
        )
        page.locator(".astra-previous").first.evaluate("node=>node.open=false")
        page.locator(".row").first.scroll_into_view_if_needed()
        page.screenshot(path=str(root / "gallery/first_row.png"))
        browser.close()
    receipt = {
        "passed": True,
        "html_sha256": audit["html_sha256"],
        "all512_selected_p1_bindings_scores_and_evidence_verified": True,
        "all_existing_p2_and_old_judges_preserved": True,
        "four_primary_revision_rows_align_across_four_image_columns": True,
        "alignment_after_opening_old_new_and_p2_evidence": True,
        "first_last_actual_cached_images_loaded": True,
        "all_three_current_and_historical_downloads_work": True,
        "javascript_errors": errors,
        "live_gateway_sso": "Not tested; actual cached images at intercepted gateway origin",
        "browser_helper_sha256": complete.sha(__file__),
    }
    complete.immutable(root / "browser_validation.json", receipt)
    print(json.dumps(receipt), flush=True)


if __name__ == "__main__":
    main()
