#!/usr/bin/env python3
"""Exercise the unchanged viewer against cached published assets, without IMS."""

import asyncio
import json
import mimetypes
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.async_api import async_playwright

import convert as fe

CHROME = Path("/mnt/localssd/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome")


async def main():
    data = json.loads((fe.HERE / "report/data.json").read_text())
    source = json.loads((fe.PUBLIC / "data/comparison.json").read_text())
    images = [asset["image_src"] for row in data["rows"] for asset in row["images"]
              if asset["asset_type"] == "image"]
    for url in images:
        relative = url.removeprefix(fe.BASE)
        if relative == url or not (fe.PUBLIC / relative).is_file():
            raise AssertionError("an image does not bind to an existing published artifact")
    assert len(images) == 540
    assert (fe.HERE / "report/viewer.html").read_bytes() == (
        fe.VENDOR / "annotation_viewer.html").read_bytes()
    errors = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            executable_path=str(CHROME), headless=True, args=["--no-sandbox"],
        )
        try:
            page = await browser.new_page(viewport={"width": 1920, "height": 1200})
            page.on("pageerror", lambda error: errors.append(str(error)))

            async def route_request(route):
                url = route.request.url
                if url.startswith(fe.BASE):
                    relative = urlsplit(url).path.split("/" + fe.PREFIX + "/", 1)[1]
                    path = (fe.HERE / "report" / relative[3:]) if relative.startswith("fe/") else (
                        fe.PUBLIC / relative)
                    if path.is_file():
                        await route.fulfill(
                            path=str(path),
                            content_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                        )
                        return
                await route.fulfill(status=404, body="Not present in the cached browser fixture.")

            await page.route("**/*", route_request)
            await page.goto(fe.VIEWER_URL)
            await page.locator("#setupSkip").click()
            await page.wait_for_selector(".row")
            assert await page.evaluate("MERGED.length") == 30
            assert await page.get_by_text(fe.TITLE, exact=True).count() >= 1
            assert await page.evaluate("SOURCES[0].links") == data["links"]
            first = page.locator(".row").first
            assert await first.locator(".assets .asset.input").count() == 13
            await page.locator("#expandInputs").click()
            assert await first.locator(".assets .asset.input").count() == 0
            expected_labels = [asset["meta_text"]["label"] for asset in data["rows"][0]["images"][:5]]
            assert await first.locator(".assets .asset .lbl b").all_text_contents() == expected_labels
            assert await first.locator(".caps .cap .body").all_text_contents() == [
                asset["text_content"] for asset in data["rows"][0]["images"][18:]
            ]
            await page.wait_for_function("""() =>
                [...document.querySelector('.row').querySelectorAll('.asset img')]
                .every(image => image.complete && image.naturalWidth > 0)""")
            await page.screenshot(path=str(fe.HERE / "first_row.png"))
            parts = urlsplit(page.url)
            params = dict(parse_qsl(parts.query))
            params["rows"] = "30"
            await page.goto(urlunsplit(parts._replace(query=urlencode(params))))
            await page.wait_for_selector(".row")
            assert await page.evaluate("MERGED.length") == 1
            assert await page.locator(".rowhead .rowidx").first.inner_text() == (
                " / ".join(map(str, source["rows"][-1]["key"])))
            if await page.locator(".row").first.locator(".asset.input").count():
                await page.locator("#expandInputs").click()
            await page.wait_for_function("""() =>
                [...document.querySelector('.row').querySelectorAll('.asset img')]
                .every(image => image.complete && image.naturalWidth > 0)""")
            if errors:
                raise AssertionError(errors)
        finally:
            await browser.close()
    receipt = {
        "status": "passed", "rows": 30, "comparison_outputs": 120,
        "historical_references": 30, "input_image_references": 390,
        "exact_cached_image_bindings": 540, "download_links": 12,
        "first_and_last_row_images_rendered": True, "inputs_toggle": True,
        "prompt_and_rewrite_captions_preserved": True, "vendor_viewer_unchanged": True,
        "network_boundary": "Cached published bytes intercepted at exact gateway URLs; live IMS login "
                            "and annotation writes were not exercised.",
        "files": {name: fe.digest((fe.HERE / "report" / name).read_bytes())
                  for name in ("data.json", "viewer.html")},
    }
    fe.write_json(fe.HERE / "browser_validation.json", receipt)
    print(json.dumps(receipt))


if __name__ == "__main__":
    asyncio.run(main())
