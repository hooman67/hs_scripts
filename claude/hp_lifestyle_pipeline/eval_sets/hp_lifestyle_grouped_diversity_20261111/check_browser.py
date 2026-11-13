"""Exercise the actual grouped gallery and images; mock only Adobe IMS."""
import mimetypes
import os
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import report

HERE = report.HERE
data = report.load(report.PUBLIC / "gallery/data.json")
manifest = report.load(HERE / "build_manifest.json")
roots = {report.PREFIX: report.PUBLIC}
inventories = {report.PREFIX: manifest["assets"]}
for name in (
    "hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110",
    "hp_lifestyle_v6_4_full160_pr4523_20261110",
    "hp_lifestyle_v6_4_pr4523_30_20261110",
):
    root = HERE.parent / name / "public"
    prefix = "eval_sets/" + name
    roots[prefix] = root
    inventories[prefix] = report.load(root / "asset_manifest.json")["assets"]
verified = {}
errors = []
work = HERE / ".browser-work"
work.mkdir(exist_ok=True)
fd = os.open(work, os.O_RDONLY | os.O_DIRECTORY)
os.environ["TMPDIR"] = f"/proc/{os.getpid()}/fd/{fd}"

from playwright.sync_api import sync_playwright  # noqa: E402


def local_asset(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "foundry-aws-corp.adobe.io":
        raise ValueError("unexpected external browser request")
    key = unquote(parsed.path).removeprefix("/asset/" + report.BUCKET + "/")
    for prefix, root in roots.items():
        if not key.startswith(prefix + "/"):
            continue
        name = key.removeprefix(prefix + "/")
        path = root / name
        if not path.resolve().is_relative_to(root.resolve()) or name not in inventories[prefix]:
            raise ValueError("browser asset escapes the frozen inventory")
        if path not in verified:
            verified[path] = report.sha(path)
            if verified[path] != inventories[prefix][name]["sha256"]:
                raise ValueError("actual browser image/file differs from frozen inventory")
        return path
    raise ValueError("unknown browser asset prefix")


expected = []
for group in data["groups"]:
    experiments = []
    for experiment in group["experiments"]:
        cards = []
        for card in experiment["cards"]:
            path = local_asset(urljoin(report.VIEWER_URL, card["image"]))
            if verified[path] != card["image_sha256"]:
                raise ValueError("grouped image is not the original recorded raw PNG")
            cards.append({"rank": card["rank"], "key": card["prompt_key"],
                          "image": card["image"], "prompt": card["prompt"]})
        experiments.append({"id": experiment["id"], "cards": cards})
    expected.append({"id": group["id"], "experiments": experiments})

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path="/mnt/localssd/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome",
            args=["--no-sandbox", "--no-process-singleton"])
        try:
            page = browser.new_page(viewport={"width": 1800, "height": 1200})
            page.on("pageerror", lambda error: errors.append(str(error)))

            def route_request(route):
                if route.request.url.startswith("https://auth-stg1.services.adobe.com/"):
                    route.fulfill(content_type="application/javascript", body="""
window.adobeImsFactory={createIMSLib(config,key){window[key]={
 initialize(){config.onAccessToken({token:"LOCAL-IMS-MOCK"});setTimeout(()=>config.onReady({}),0)},
 isSignedInUser(){return true},getProfile(){return Promise.resolve({displayName:"Local UI test",account_type:"test"})},
 getAccessToken(){return {token:"LOCAL-IMS-MOCK"}},signIn(){},signOut(){}}}};
""")
                    return
                path = local_asset(route.request.url)
                route.fulfill(path=str(path),
                              content_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream")

            page.route("**/*", route_request)
            page.goto(report.VIEWER_URL)
            page.wait_for_function("document.querySelectorAll('.card').length===480", timeout=120000)
            assert page.locator(".input-group").count() == 16
            assert page.locator(".experiment").count() == 48
            assert page.locator(".source-prompt[open],.input-context[open]").count() == 0
            assert page.locator(".input-group").evaluate_all("""groups=>groups.map(group=>({
              id:group.id,experiments:[...group.querySelectorAll('.experiment')].map(experiment=>({
                id:experiment.dataset.experiment,cards:[...experiment.querySelectorAll('.card')].map(card=>({
                  rank:Number(card.dataset.rank),key:card.dataset.promptKey,
                  image:card.querySelector('img').getAttribute('src'),
                  prompt:card.querySelector('.source-prompt p').textContent
                }))
              }))
            }))""") == expected
            assert page.evaluate("DATA.groups.map(g=>g.contexts)") == [g["contexts"] for g in data["groups"]]
            for group in (data["groups"][0], data["groups"][-1]):
                page.locator("#bank").select_option(group["id"])
                for experiment in group["experiments"]:
                    page.locator("#experiment").select_option(experiment["id"])
                    assert page.locator(".input-group").count() == 1
                    assert page.locator(".card").count() == 10
                    images = page.locator(".card-image")
                    images.evaluate_all("images=>images.forEach(i=>i.loading='eager')")
                    images.first.scroll_into_view_if_needed()
                    page.wait_for_function("""() => [...document.querySelectorAll('.card-image')]
                        .every(i=>i.complete&&i.naturalWidth===2368&&i.naturalHeight===1776)""",
                        timeout=120000)
                    tops = images.evaluate_all("images=>images.map(i=>Math.round(i.getBoundingClientRect().top))")
                    assert len(set(tops[:5])) == len(set(tops[5:])) == 1 and tops[5] > tops[0]
            page.locator("#bank").select_option(data["groups"][0]["id"])
            page.locator("#experiment").select_option("v6_4_pr4523")
            page.locator(".source-prompt summary").first.click()
            assert page.locator(".source-prompt p").first.inner_text() == data["groups"][0]["experiments"][2]["cards"][0]["prompt"]
            page.locator("#showPrompts").check()
            assert page.locator(".source-prompt[open]").count() == 10
            page.locator("#showPrompts").uncheck()
            assert page.locator(".source-prompt[open]").count() == 0
            page.locator(".input-context > summary").click()
            page.locator(".source-context > summary").nth(1).click()
            assert "Smart Brief" in page.locator(".source-context[open]").inner_text()
            assert page.locator(".source-context[open] pre").count() == 2
            images = page.locator(".card-image")
            images.first.scroll_into_view_if_needed()
            images.first.click()
            assert page.locator("#lightbox").is_visible()
            assert page.locator("#largeImage").get_attribute("src") == urljoin(
                report.VIEWER_URL, data["groups"][0]["experiments"][2]["cards"][0]["image"])
            page.keyboard.press("Escape")
            assert not page.locator("#lightbox").is_visible()
            page.locator(".input-context > summary").click()
            page.locator("#columns").evaluate("e=>{e.value='3';e.dispatchEvent(new Event('input',{bubbles:true}))}")
            assert page.locator(".cards").evaluate("e=>getComputedStyle(e).gridTemplateColumns.split(' ').length") == 3
            page.locator("#columns").evaluate("e=>{e.value='5';e.dispatchEvent(new Event('input',{bubbles:true}))}")
            page.locator("#experiment").select_option("")
            page.evaluate("window.scrollTo(0,0)")
            page.screenshot(path=str(HERE / "grouped_desktop.png"))
            page.set_viewport_size({"width": 390, "height": 844})
            assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
            assert page.locator(".cards").first.evaluate(
                "e=>getComputedStyle(e).gridTemplateColumns.split(' ').length") == 2
            page.screenshot(path=str(HERE / "grouped_mobile.png"))
            assert not errors, errors
            assert not page.locator("#error").inner_text()
        finally:
            browser.close()
finally:
    os.close(fd)
    work.rmdir()

report.emit(HERE / "browser_validation.json", {
    "status": "passed", "groups": 16, "ten_image_grids": 48,
    "exact_original_image_prompt_rank_bindings": 480,
    "original_raw_image_hashes_verified": 480, "first_and_last_banks_all_ten_images_rendered_per_experiment": True,
    "collapsed_prompt_and_context_expansion": True, "bank_experiment_filters_size_control_and_lightbox": True,
    "desktop_five_columns_mobile_two_columns_no_overflow": True, "javascript_errors": errors,
    "build_manifest_sha256": report.sha(HERE / "build_manifest.json"),
    "network_boundary": "Actual frozen source/data and original images; IMS mocked. Live gateway/login not certified.",
})
print("Passed: 16 banks, 48 ten-image grids, 480 exact original image/prompt bindings.")
