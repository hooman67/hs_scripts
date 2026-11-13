"""Check actual grouped bindings/pixels, with an explicit offline Adobe IMS stub."""

from __future__ import annotations

import mimetypes
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from playwright.sync_api import sync_playwright

import report
import text_study

ROOT = text_study.ROOT


def main() -> None:
    data = text_study.load(report.PUBLIC / "gallery/data.json")
    manifest = text_study.load(ROOT / "build_manifest.json")
    roots = {report.PREFIX: report.PUBLIC}
    inventories = {report.PREFIX: manifest["assets"]}
    for name in ("hp_lifestyle_v6_4_full160_pr4523_20261110", "hp_lifestyle_v6_4_pr4523_30_20261110"):
        folder = ROOT.parent / name / "public"
        roots["eval_sets/" + name] = folder
        inventories["eval_sets/" + name] = text_study.load(folder / "asset_manifest.json")["assets"]

    def local_asset(url: str) -> Path:
        parsed = urlsplit(url)
        if parsed.netloc != "foundry-aws-corp.adobe.io":
            raise ValueError("Unexpected browser asset origin")
        key = parsed.path.removeprefix("/asset/" + report.BUCKET + "/")
        for prefix, folder in roots.items():
            if key.startswith(prefix + "/"):
                name = key.removeprefix(prefix + "/")
                path = folder / name
                if not path.resolve().is_relative_to(folder.resolve()) or name not in inventories[prefix]:
                    raise ValueError("Browser asset escapes the frozen inventory")
                if text_study.sha(path) != inventories[prefix][name]["sha256"]:
                    raise ValueError("Browser asset bytes differ from the captured output")
                return path
        raise ValueError("Browser asset prefix is unknown")

    for group in data["groups"]:
        for experiment in group["experiments"]:
            if [card["rank"] for card in experiment["cards"]] != list(range(1, 11)):
                raise ValueError("Every writer grid must contain ten exact ranked slots")
            for card in experiment["cards"]:
                if card["image"]:
                    path = local_asset(urljoin(report.VIEWER_URL, card["image"]))
                    if text_study.sha(path) != card["image_sha256"]:
                        raise ValueError("Displayed image is not its recorded raw PNG")
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
            page.goto(report.VIEWER_URL)
            page.wait_for_function("document.querySelectorAll('.card').length===320", timeout=120000)
            assert page.locator(".input-group").count() == 16
            assert page.locator(".experiment").count() == 32
            assert page.evaluate("DATA.groups") == data["groups"]
            expected = [
                {"key": card["prompt_key"], "text": card["prompt"] or None, "image": card["image"]}
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
            for group in (data["groups"][0], data["groups"][-1]):
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
            page.locator("#bank").select_option("")
            page.locator("#experiment").select_option("")
            page.locator("#showPrompts").check()
            assert page.locator(".source-prompt[open]").count() == 160 + data["astra_text"]["accepted_prompts"]
            page.locator("#showPrompts").uncheck()
            page.screenshot(path=str(ROOT / "comparison_desktop.png"))
            page.set_viewport_size({"width": 390, "height": 844})
            assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
            page.screenshot(path=str(ROOT / "comparison_mobile.png"))
            assert not errors, errors
            assert not page.locator("#error").inner_text()
        finally:
            browser.close()
    text_study.write(
        ROOT / "browser_validation.json",
        {
            "status": "passed",
            "groups": 16,
            "slots": 320,
            "actual_images": data["image_count"],
            "build_manifest_sha256": text_study.sha(ROOT / "build_manifest.json"),
            "live_ims_not_certified": True,
        },
    )


if __name__ == "__main__":
    main()
