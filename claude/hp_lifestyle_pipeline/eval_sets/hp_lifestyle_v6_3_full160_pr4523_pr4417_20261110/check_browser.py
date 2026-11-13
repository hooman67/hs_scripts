"""Verify the real gallery locally; mock only IMS, never report data or image bytes."""
import json
import mimetypes
import os
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
work = HERE / ".browser-work"
work.mkdir(exist_ok=True)
# A procfs descriptor aliases this same owned directory without creating an
# outside symlink; Chromium's UNIX socket cannot fit the full study pathname.
work_fd = os.open(work, os.O_RDONLY | os.O_DIRECTORY)
os.environ["TMPDIR"] = f"/proc/{os.getpid()}/fd/{work_fd}"
from playwright.sync_api import sync_playwright

errors = []
data_bytes = (HERE / "public/data/comparison.json").read_bytes()
data = json.loads(data_bytes)
with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="/mnt/localssd/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome",
        args=["--no-sandbox", "--no-process-singleton"],
    )
    page = browser.new_page(viewport={"width": 1600, "height": 1100})
    page.on("pageerror", lambda error: errors.append(str(error)))

    def local(route):
        relative = urlparse(route.request.url).path.lstrip("/")
        path = (HERE / "public" / relative).resolve()
        if not path.is_relative_to(HERE / "public") or not path.is_file():
            route.fulfill(status=404, body="Unknown asset")
            return
        route.fulfill(body=data_bytes if relative == "data/comparison.json" else path.read_bytes(),
                      content_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream")

    page.route("http://gallery.test/**", local)
    page.route("https://auth-stg1.services.adobe.com/**", lambda route: route.fulfill(
        content_type="application/javascript",
        body="""window.adobeImsFactory={createIMSLib(config,key){window[key]={
          initialize(){config.onAccessToken({token:"LOCAL-IMS-MOCK"});setTimeout(()=>config.onReady({}),0)},
          isSignedInUser(){return true},getProfile(){return Promise.resolve({displayName:"Local UI test",account_type:"test"})},
          getAccessToken(){return {token:"LOCAL-IMS-MOCK"}},signIn(){},signOut(){}}}};"""))
    page.goto("http://gallery.test/gallery/index.html", wait_until="load")
    page.wait_for_function("document.querySelectorAll('.pair').length === 160", timeout=120000)
    assert page.locator(".output").count() == 320
    done = sum(o["status"] == "done" for row in data["rows"] for o in row["outputs"].values())
    assert page.locator(".badge.reused").count() == 60
    assert page.locator(".badge.new").count() == 260
    assert page.get_by_text("Exact image-model prompt", exact=True).count() == done
    first = page.locator(".pair").first
    expected = data["rows"][0]
    assert expected["prompt"]["text"] in first.inner_text()
    first.get_by_text("Actual model inputs: product PNG, geometry guide, Astra style reference", exact=True).first.click()
    imgs = first.locator("details[open] img")
    assert imgs.count() == 3
    for image in imgs.all():
        image.scroll_into_view_if_needed()
        image.evaluate("(image) => image.loading = 'eager'")
        page.wait_for_function("(url) => [...document.images].some(i => i.src === url && i.complete && i.naturalWidth > 0)",
                               arg=image.get_attribute("src") if image.get_attribute("src").startswith("http") else
                               "http://gallery.test/" + image.get_attribute("src").replace("../", ""))
    columns = first.locator(".output").evaluate_all("els => els.map(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width}})")
    assert columns[0]["y"] == columns[1]["y"] and columns[1]["x"] > columns[0]["x"]
    page.locator("#search").fill(data["rows"][0]["prompt"]["prompt_key"])
    assert page.locator(".pair").count() == 1
    page.locator("#search").fill("")
    page.locator("#state").select_option("reused")
    reused_rows = sum(any(o["reuse_status"] == "reused" for o in row["outputs"].values()) for row in data["rows"])
    assert page.locator(".pair").count() == reused_rows
    page.locator("#state").select_option("")
    page.locator("#refresh").click()
    page.wait_for_function("document.querySelectorAll('.pair').length === 160")
    assert not errors, errors
    receipt = {"verified_at_utc": data["built_at_utc"], "real_report_rows": 160, "output_columns": 320,
               "reused_badges": 60, "new_badges": 260, "completed_outputs": done,
               "source_prompt_present": True, "actual_input_images_loaded": 3,
               "column_alignment": columns, "search_and_status_filter": True, "javascript_errors": errors,
               "ims": "mocked locally; live gateway login not certified"}
    (HERE / "browser_validation.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt))
    browser.close()
os.close(work_fd)
