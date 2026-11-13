"""Publish a clean image + original source-prompt variant without changing old FE data."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import mimetypes
import os
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
PREFIX = "eval_sets/" + STUDY.name
BUCKET = "foundry-hp-enterprise-adobe-assets"
BASE = "https://foundry-aws-corp.adobe.io/asset/" + BUCKET + "/" + PREFIX + "/"
NAME = "data_source_prompts_20261110.json"
URL = BASE + "fe/viewer.html?src=" + NAME + "&ldap=hshariati"
VENDOR = Path.home() / ".claude/scripts/fe_html"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def save(name, value):
    HERE.mkdir(exist_ok=True)
    body = value if isinstance(value, bytes) else (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()
    if (HERE / name).exists():
        if (HERE / name).read_bytes() != body:
            raise ValueError("saved source or report changed; preserve and inspect before continuing")
        return
    with (HERE / name).open("xb") as stream:
        stream.write(body)


client = module("v64_clean30_s3", STUDY.parent /
    "hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/s3_access.py").s3_client()
objects = {}
for name in ("data/generation.json", "fe/data.json", "fe/viewer.html"):
    response = client.get_object(Bucket=BUCKET, Key=PREFIX + "/" + name)
    body = response["Body"].read()
    objects[name] = {"sha256": hashlib.sha256(body).hexdigest(), "etag": response["ETag"],
                     "version_id": response.get("VersionId")}
    save("source_" + name.replace("/", "_"), body)
source = json.loads((HERE / "source_data_generation.json").read_text())
old_fe = json.loads((HERE / "source_fe_data.json").read_text())
assert len(source["rows"]) == len(old_fe["rows"]) == 30
assert (HERE / "source_fe_viewer.html").read_bytes() == (VENDOR / "annotation_viewer.html").read_bytes()
rows = []
for index, (row, old) in enumerate(zip(source["rows"], old_fe["rows"]), 1):
    assert old["meta_data"]["evalset_item_id"] == " / ".join(map(str, row["key"]))
    image = old["images"][0]
    assert image["asset_type"] == "image" and len(old["images"]) == 1
    assert image["image_src"] == BASE + row["output"]["image"].removeprefix("../")
    assert hashlib.sha256(row["prompt"]["text"].encode()).hexdigest() == row["prompt"]["text_sha256"]
    rows.append({"row_idx": index, "evalset_item_id": old["meta_data"]["evalset_item_id"],
                 "assets": [{"kind": "image", "src": image["image_src"], "label": image["meta_text"]["label"]},
                            {"kind": "text", "content": row["prompt"]["text"], "label": "Source prompt"}]})
data = module("v64_clean30_converter", VENDOR / "parquet_to_fe_html.py").manifest_to_data_json(
    {"rows": rows}, is_secure=True, title="V6.4 / PR 4523 - V15.7 shapes")
save(NAME, data)
work = HERE / ".browser-work"
work.mkdir(exist_ok=True)
fd = os.open(work, os.O_RDONLY | os.O_DIRECTORY)
os.environ["TMPDIR"] = f"/proc/{os.getpid()}/fd/{fd}"

from playwright.sync_api import sync_playwright  # noqa: E402

errors = []
try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path="/mnt/localssd/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome",
            args=["--no-sandbox", "--no-process-singleton"])
        try:
            page = browser.new_page(viewport={"width": 1500, "height": 1100})
            page.on("pageerror", lambda error: errors.append(str(error)))

            def handle(route):
                if route.request.url.startswith("https://auth-stg1.services.adobe.com/"):
                    route.fulfill(content_type="application/javascript", body="""
window.adobeImsFactory={createIMSLib(config,key){window[key]={
 initialize(){config.onAccessToken({token:"LOCAL-IMS-MOCK"});setTimeout(()=>config.onReady({}),0)},
 isSignedInUser(){return true},getProfile(){return Promise.resolve({displayName:"Local UI test",account_type:"test"})},
 getAccessToken(){return {token:"LOCAL-IMS-MOCK"}},signIn(){},signOut(){}}}};
""")
                    return
                name = urlsplit(route.request.url).path.removeprefix(urlsplit(BASE).path)
                if name.startswith("fe/annotations/"):
                    route.fulfill(status=404, body="No annotation fixture; annotation writes are not exercised.")
                    return
                path = (HERE / NAME if name == "fe/" + NAME else
                        HERE / "source_fe_viewer.html" if name == "fe/viewer.html" else STUDY / "public" / name)
                if not path.resolve().is_relative_to(STUDY) or not path.is_file():
                    raise ValueError("unexpected clean-FE fixture request: " + name)
                route.fulfill(path=str(path), content_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream")

            page.route("**/*", handle)
            page.goto(URL)
            page.locator("#setupSkip").click()
            page.wait_for_selector(".row")
            assert page.evaluate("MERGED.length") == 30
            assert page.locator(".row").first.locator(".asset").count() == 1
            assert data["rows"][0]["images"][1]["text_content"] in page.locator(".row").first.inner_text()
            assert page.evaluate("SOURCES[0].links.length") == 0
            page.wait_for_function("""() => [...document.querySelector('.row').querySelectorAll('img')]
                                     .every(i=>i.complete&&i.naturalWidth===2368)""")
            assert not errors, errors
        finally:
            browser.close()
finally:
    os.close(fd)
work.rmdir()
for name, expected in objects.items():
    response = client.get_object(Bucket=BUCKET, Key=PREFIX + "/" + name)
    assert response["ETag"] == expected["etag"] and hashlib.sha256(response["Body"].read()).hexdigest() == expected["sha256"]
body = (HERE / NAME).read_bytes()
client.put_object(Bucket=BUCKET, Key=PREFIX + "/fe/" + NAME, Body=body,
                  ContentType="application/json", CacheControl="no-cache", IfNoneMatch="*")
response = client.get_object(Bucket=BUCKET, Key=PREFIX + "/fe/" + NAME)
assert response["Body"].read() == body and response["ContentType"] == "application/json"
save("publication_receipt.json", {"verified_at_utc": datetime.now(timezone.utc).isoformat(),
    "url": URL, "rows": 30, "images_per_row": 1, "original_prompt_per_row": 1,
    "debug_or_rewritten_prompts": 0, "new_model_calls": 0, "image_uploads": 0,
    "sha256": hashlib.sha256(body).hexdigest(), "etag": response["ETag"],
    "version_id": response.get("VersionId"), "preserved_objects": objects,
    "browser": "Actual data/images; original prompt visible. Live IMS/annotation writes not certified."})
save("report_links.txt", (URL + "\n").encode())
print(URL)
