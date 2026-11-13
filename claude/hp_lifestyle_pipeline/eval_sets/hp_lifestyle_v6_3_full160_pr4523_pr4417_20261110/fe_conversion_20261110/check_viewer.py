#!/usr/bin/env python3
"""Check the exact minimal report with its actual cached published images."""

import json
import mimetypes
import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import convert


def main():
    work = convert.HERE / ".browser-work"
    work.mkdir(exist_ok=True)
    fd = os.open(work, os.O_RDONLY | os.O_DIRECTORY)
    os.environ["TMPDIR"] = f"/proc/{os.getpid()}/fd/{fd}"
    from playwright.sync_api import sync_playwright

    audit = json.loads((convert.HERE / "build_audit.json").read_text())
    data = json.loads((convert.REPORT / "data.json").read_text())
    routes = {convert.BASE + "fe/" + name: convert.REPORT / name for name in ("viewer.html", "data.json")}
    for row in data["rows"]:
        for asset in row["images"]:
            path = convert.PUBLIC / asset["image_src"].removeprefix(convert.BASE)
            if not path.is_file():
                raise FileNotFoundError(path)
            routes[asset["image_src"]] = path
    if (convert.REPORT / "viewer.html").read_bytes() != (convert.prior.VENDOR / "annotation_viewer.html").read_bytes():
        raise ValueError("official viewer changed")
    errors = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path="/mnt/localssd/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome",
                headless=True, args=["--no-sandbox", "--no-process-singleton"],
            )
            try:
                page = browser.new_page(viewport={"width": 1920, "height": 1200})
                page.on("pageerror", lambda error: errors.append(str(error)))

                def handle(route):
                    path = routes.get(route.request.url.split("?", 1)[0])
                    if path is None:
                        route.fulfill(status=404, body="Not present in the cached browser fixture.")
                    else:
                        route.fulfill(path=str(path), content_type=mimetypes.guess_type(path.name)[0])

                page.route("**/*", handle)
                page.goto(convert.VIEWER_URL)
                page.locator("#setupSkip").click()
                page.wait_for_selector(".row")
                assert page.evaluate("MERGED.length") == 160
                assert page.evaluate("SOURCES[0].links.length") == 0
                assert page.evaluate("SOURCES[0].meta_texts.length") == 0
                assert page.locator(".caps, .mfold, .asset.input").count() == 0
                assert page.get_by_text(convert.TITLE, exact=True).count() > 0
                assert page.evaluate("SOURCES[0].rows.map(r => r.images.map(a => a.image_src))") == [
                    [asset["image_src"] for asset in row["images"]] for row in data["rows"]
                ]
                first = page.locator(".row").first
                assert first.locator(".asset").count() == 2
                assert first.locator(".asset .lbl b").all_text_contents() == ["V15.6", "V15.7"]
                page.wait_for_function("""() =>
                    [...document.querySelector('.row').querySelectorAll('.asset img')]
                    .every(image => image.complete && image.naturalWidth > 0)""")
                columns = first.locator(".asset").evaluate_all(
                    "els => els.map(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width}})")
                assert columns[0]["y"] == columns[1]["y"] and columns[1]["x"] > columns[0]["x"]
                page.screenshot(path=str(convert.HERE / "comparison.png"))
                parts = urlsplit(page.url)
                params = dict(parse_qsl(parts.query))
                params["rows"] = "160"
                page.goto(urlunsplit(parts._replace(query=urlencode(params))))
                page.wait_for_selector(".row")
                assert page.evaluate("MERGED.length") == 1
                assert page.locator(".rowhead .rowidx").first.inner_text() == data["rows"][-1]["meta_data"]["evalset_item_id"]
                page.wait_for_function("""() =>
                    [...document.querySelector('.row').querySelectorAll('.asset img')]
                    .every(image => image.complete && image.naturalWidth > 0)""")
                assert not errors, errors
            finally:
                browser.close()
    finally:
        os.close(fd)
    convert.prior.write_json(convert.HERE / "browser_validation.json", {
        "status": "passed", "rows": 160, "images_per_row": 2, "all_image_bindings_verified": 320,
        "column_order": ["V15.6", "V15.7"], "column_alignment": columns,
        "first_and_last_row_images_rendered": True, "extra_assets_text_metadata_links": 0,
        "vendor_viewer_unchanged": True, "javascript_errors": errors, "files": audit["files"],
        "network_boundary": "Cached actual published images; live IMS and annotation writes not exercised.",
    })
    print({"status": "passed", "rows": 160, "images": 320, "columns": 2})


if __name__ == "__main__":
    main()
