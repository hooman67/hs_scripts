"""Verify all320 real images, unchanged original cards and the failure snapshot."""

from __future__ import annotations

import mimetypes
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from playwright.sync_api import sync_playwright

import report as original
import text_study
from recovery.complete160 import completed_report as report


def main() -> None:
    data = text_study.load(report.PUBLIC / report.DATA_NAME)
    manifest = text_study.load(report.HERE / "build_manifest.json")
    old_manifest = text_study.load(report.ROOT / "build_manifest.json")
    baseline = {}
    for name in ("hp_lifestyle_v6_4_full160_pr4523_20261110", "hp_lifestyle_v6_4_pr4523_30_20261110"):
        folder = report.ROOT.parent / name / "public"
        baseline["eval_sets/" + name] = (folder, text_study.load(folder / "asset_manifest.json")["assets"])

    def local_asset(url: str) -> Path:
        parsed = urlsplit(url)
        if parsed.netloc != "foundry-aws-corp.adobe.io" or parsed.query:
            raise ValueError("Unexpected browser asset origin/query")
        key = parsed.path.removeprefix("/asset/" + report.BUCKET + "/")
        roots = [
            (report.PREFIX, report.PUBLIC, manifest["assets"]),
            (report.PREFIX, original.PUBLIC, old_manifest["assets"]),
            *((prefix, folder, inventory) for prefix, (folder, inventory) in baseline.items()),
        ]
        for prefix, folder, inventory in roots:
            if not key.startswith(prefix + "/"):
                continue
            name = key.removeprefix(prefix + "/")
            if name not in inventory:
                continue
            path = folder / name
            if not path.resolve().is_relative_to(folder.resolve()) or text_study.sha(path) != inventory[name]["sha256"]:
                raise ValueError("Browser asset differs from the frozen source inventory")
            return path
        raise ValueError("Browser requested an unrecognized asset: " + key)

    if data["image_count"] != 320:
        raise ValueError("Completed comparison must contain320 actual images")
    for group in data["groups"]:
        for experiment in group["experiments"]:
            if [card["rank"] for card in experiment["cards"]] != list(range(1, 11)):
                raise ValueError("Each comparison grid must retain all ten ranked slots")
            if experiment.get("bank_result_url"):
                local_asset(urljoin(original.VIEWER_URL, experiment["bank_result_url"]))
            for card in experiment["cards"]:
                path = local_asset(urljoin(original.VIEWER_URL, card["image"]))
                if card["status"] != "done" or text_study.sha(path) != card["image_sha256"]:
                    raise ValueError("A completed card is not its recorded raw image")
                for url in card["details"]["inputs"].values():
                    local_asset(urljoin(original.VIEWER_URL, url))
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=["--no-sandbox"])
        try:
            page = browser.new_page(viewport={"width": 1800, "height": 1200})
            page.on("pageerror", lambda error: errors.append(str(error)))

            def route_request(route):
                if route.request.url.startswith("https://auth-stg1.services.adobe.com/"):
                    route.fulfill(
                        content_type="application/javascript",
                        body="""
window.adobeImsFactory={createIMSLib(config,key){window[key]={
 initialize(){config.onAccessToken({token:"LOCAL-IMS-MOCK"});setTimeout(()=>config.onReady({}),0)},
 isSignedInUser(){return true},getProfile(){return Promise.resolve({displayName:"Offline test"})},
 getAccessToken(){return {token:"LOCAL-IMS-MOCK"}},signIn(){},signOut(){}}}};
""",
                    )
                else:
                    path = local_asset(route.request.url)
                    route.fulfill(
                        path=str(path), content_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream"
                    )

            page.route("**/*", route_request)
            page.goto(original.VIEWER_URL)
            page.wait_for_function("document.querySelectorAll('.card').length===320", timeout=120000)
            assert page.locator(".input-group").count() == 16
            assert page.locator(".experiment").count() == 32
            assert page.evaluate("DATA.groups") == data["groups"]
            expected = [
                {"key": card["prompt_key"], "text": card["prompt"], "image": card["image"]}
                for group in data["groups"]
                for experiment in group["experiments"]
                for card in experiment["cards"]
            ]
            assert (
                page.locator(".card").evaluate_all("""cards=>cards.map(c=>({
 key:c.dataset.promptKey,text:c.querySelector('.source-prompt p')?.textContent||null,
 image:c.querySelector('.card-image')?.getAttribute('src')||null}))""")
                == expected
            )
            checked_images = 0
            for group in data["groups"]:
                page.locator("#bank").select_option(group["id"])
                for experiment in group["experiments"]:
                    page.locator("#experiment").select_option(experiment["id"])
                    assert page.locator(".card").count() == 10
                    page.locator(".card-image").evaluate_all("images=>images.forEach(i=>i.loading='eager')")
                    page.wait_for_function(
                        """() => [...document.querySelectorAll('.card-image')]
                        .every(i=>i.complete&&i.naturalWidth===2368&&i.naturalHeight===1776)""",
                        timeout=120000,
                    )
                    checked_images += page.locator(".card-image").count()
            assert checked_images == 320
            page.locator(".card-image").first.click()
            assert page.locator("#lightbox").evaluate("dialog=>dialog.open")
            page.locator("#closeImage").click()
            page.locator("#bank").select_option("")
            page.locator("#experiment").select_option("")
            page.locator("#showPrompts").check()
            assert page.locator(".source-prompt[open]").count() == 320
            page.locator("#showPrompts").uncheck()
            page.screenshot(path=str(report.HERE / "completed_desktop.png"))
            page.set_viewport_size({"width": 390, "height": 844})
            assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
            page.screenshot(path=str(report.HERE / "completed_mobile.png"))
            page.goto(urljoin(original.VIEWER_URL, "./original_run_20261112.html"))
            page.wait_for_function("document.querySelectorAll('.card').length===320", timeout=120000)
            assert page.evaluate("DATA") == text_study.load(report.HERE / "source/gallery/data.json")
            assert not errors, errors
            assert not page.locator("#error").inner_text()
        finally:
            browser.close()
    text_study.write(
        report.HERE / "browser_validation.json",
        {
            "status": "passed",
            "groups": 16,
            "slots": 320,
            "actual_images": 320,
            "all320_images_decoded_at_native_resolution": True,
            "original_snapshot_verified": True,
            "build_manifest_sha256": text_study.sha(report.HERE / "build_manifest.json"),
            "live_ims_not_certified": True,
        },
    )


if __name__ == "__main__":
    main()
