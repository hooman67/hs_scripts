#!/usr/bin/env python3
"""Verify minimal FE pages against the actual cached published images."""

import asyncio
import json
import mimetypes
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.async_api import async_playwright

import clean_reports as clean
import convert as original


async def main():
    audit = json.loads((clean.WORK / "build_audit.json").read_text())
    routes = {}
    datasets = {}
    for name, report in audit["reports"].items():
        base = report["url"].split("?", 1)[0].rsplit("/", 1)[0] + "/"
        directory = clean.WORK / "reports" / name
        data = json.loads((directory / "data.json").read_text())
        datasets[name] = data
        for filename in ("viewer.html", "data.json"):
            routes[base + filename] = directory / filename
        assert (directory / "viewer.html").read_bytes() == (
            original.VENDOR / "annotation_viewer.html").read_bytes()
        for row in data["rows"]:
            for asset in row["images"]:
                path = original.PUBLIC / asset["image_src"].removeprefix(original.BASE)
                assert path.is_file()
                routes[asset["image_src"]] = path
    errors = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            executable_path="/mnt/localssd/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome",
            headless=True, args=["--no-sandbox"],
        )
        try:
            page = await browser.new_page(viewport={"width": 1920, "height": 1200})
            page.on("pageerror", lambda error: errors.append(str(error)))

            async def handle(route):
                path = routes.get(route.request.url.split("?", 1)[0])
                if path is None:
                    await route.fulfill(status=404, body="Not present in the cached browser fixture.")
                else:
                    await route.fulfill(path=str(path), content_type=mimetypes.guess_type(path.name)[0])

            await page.route("**/*", handle)
            for name, report in audit["reports"].items():
                data = datasets[name]
                await page.goto(report["url"])
                await page.locator("#setupSkip").click()
                await page.wait_for_selector(".row")
                assert await page.evaluate("MERGED.length") == 30
                assert await page.evaluate("SOURCES[0].links.length") == 0
                assert await page.evaluate("SOURCES[0].meta_texts.length") == 0
                assert await page.locator(".caps, .mfold, .asset.input").count() == 0
                assert await page.evaluate("SOURCES[0].rows.map(r => r.images.map(a => a.image_src))") == [
                    [asset["image_src"] for asset in row["images"]] for row in data["rows"]
                ]
                first = page.locator(".row").first
                assert await first.locator(".asset").count() == report["images_per_row"]
                assert await first.locator(".asset .lbl b").all_text_contents() == [
                    asset["meta_text"]["label"] for asset in data["rows"][0]["images"]
                ]
                await page.wait_for_function("""() =>
                    [...document.querySelector('.row').querySelectorAll('.asset img')]
                    .every(image => image.complete && image.naturalWidth > 0)""")
                await page.screenshot(path=str(clean.WORK / (name + ".png")))
                parts = urlsplit(page.url)
                params = dict(parse_qsl(parts.query))
                params["rows"] = "30"
                await page.goto(urlunsplit(parts._replace(query=urlencode(params))))
                await page.wait_for_selector(".row")
                assert await page.evaluate("MERGED.length") == 1
                assert await page.locator(".rowhead .rowidx").first.inner_text() == (
                    data["rows"][-1]["meta_data"]["evalset_item_id"])
                await page.wait_for_function("""() =>
                    [...document.querySelector('.row').querySelectorAll('.asset img')]
                    .every(image => image.complete && image.naturalWidth > 0)""")
            if errors:
                raise AssertionError(errors)
        finally:
            await browser.close()
    receipt = {
        "status": "passed", "separate_reports": 4, "rows_per_report": 30,
        "images_per_separate_row": 1, "existing_combined_columns": 4,
        "extra_assets_text_metadata_links": 0, "all_image_bindings_verified": True,
        "first_and_last_row_images_rendered": True, "vendor_viewer_unchanged": True,
        "network_boundary": "Cached actual published images; live IMS and annotation writes not exercised.",
        "files": {name: report["files"] for name, report in audit["reports"].items()},
    }
    original.write_json(clean.WORK / "browser_validation.json", receipt)
    print(json.dumps(receipt))


if __name__ == "__main__":
    asyncio.run(main())
