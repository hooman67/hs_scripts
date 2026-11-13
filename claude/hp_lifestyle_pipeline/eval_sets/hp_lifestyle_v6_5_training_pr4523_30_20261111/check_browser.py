"""Verify exact local report bytes/pixels in Chromium; IMS alone is mocked."""
import functools
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
from urllib.parse import unquote, urljoin, urlsplit

from playwright.sync_api import sync_playwright

import study

HERE = study.HERE
PUBLIC = HERE / "public"
CHROME = Path("/mnt/localssd/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome")


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def original_path(url):
    url = urljoin(
        f"https://foundry-aws-corp.adobe.io/asset/{study.BUCKET}/{study.PREFIX}/gallery/index.html", url,
    )
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "foundry-aws-corp.adobe.io":
        raise ValueError(f"unexpected asset origin: {url}")
    base = f"/asset/{study.BUCKET}/"
    if not parsed.path.startswith(base) or parsed.query or parsed.fragment:
        raise ValueError(f"unexpected asset path: {url}")
    relative = unquote(parsed.path[len(base):])
    for prefix, root in (
        (study.PREFIX + "/", PUBLIC),
        ("eval_sets/" + study.BASELINE.name + "/", study.BASELINE / "public"),
    ):
        if relative.startswith(prefix):
            path = root / relative[len(prefix):]
            if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
                raise ValueError(f"missing or out-of-scope exact browser fixture: {url}")
            return path
    raise ValueError(f"unapproved browser fixture prefix: {url}")


def main():
    if not CHROME.is_file():
        raise FileNotFoundError("previously installed Chromium executable is unavailable")
    data = study.load(PUBLIC / "gallery/data.json")
    completion = study.load(study.TEXT_SNAPSHOT / "exports/completion_audit.json")
    assert data["text_recovery_provenance"] == {
        key: completion[key] for key in (
            "original_native_successful_banks", "original_native_failed_banks",
            "accepted_unchanged_banks", "additional_semantic_calls", "actual_semantic_calls",
            "bounded_recovery_successful_banks", "bounded_recovery_failed_banks",
            "extra_replies_offline_revalidated",
        )
    }
    manifest_path = PUBLIC / "asset_manifest.json"
    assets = study.load(manifest_path)["assets"]
    for name, metadata in assets.items():
        path = PUBLIC / name
        if study.sha(path) != metadata["sha256"] or path.stat().st_size != metadata["bytes"]:
            raise ValueError("browser fixture differs from explicit public manifest")
    for row in data["rows"]:
        for version in ("v6_4", "v6_5"):
            cell = row[version]
            if study.sha(original_path(cell["image"])) != cell["image_sha256"]:
                raise ValueError("browser image differs from actual audited raw output")
            for url in cell["inputs"].values():
                original_path(url)
    if len(data["training_examples"]) != 48:
        raise ValueError("actual training sample missing")
    for example in data["training_examples"]:
        if study.sha(original_path(example["image"])) != example["image_sha256"]:
            raise ValueError("training thumbnail differs from the actual consultation input")
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(Handler, directory=str(PUBLIC)),
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    errors = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=str(CHROME), args=["--no-sandbox"])
            page = browser.new_page(viewport={"width": 1500, "height": 1000})
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.route("https://auth-stg1.services.adobe.com/**",
                       lambda route: route.fulfill(body="", content_type="application/javascript"))
            page.route(
                "**/gallery/imsauth.js",
                lambda route: route.fulfill(
                    body='function initializeIMS(){document.getElementById("loading").hidden=true;'
                         'document.getElementById("content").classList.remove("hidden");onAuthReady();}',
                    content_type="application/javascript",
                ),
            )

            def asset_route(route):
                path = original_path(route.request.url)
                route.fulfill(path=str(path))

            page.route("https://foundry-aws-corp.adobe.io/**", asset_route)
            origin = "http://127.0.0.1:" + str(server.server_port)
            page.route(
                origin + "/" + study.BASELINE.name + "/**",
                lambda route: route.fulfill(path=str(original_path(
                    "../../" + route.request.url.split(origin + "/", 1)[1]
                ))),
            )
            page.goto(origin + "/gallery/index.html", wait_until="domcontentloaded")
            page.locator("#comparison>.pair").nth(29).wait_for(timeout=60000)
            assert page.locator("#comparison>.pair").count() == 30
            assert "0 successful / 16 failed" in page.locator("#textRecovery").inner_text()
            assert "15 banks received one explicitly authorized extra repair each" in page.locator("#textRecovery").inner_text()
            assert "2 extra replies also needed recognition-only revalidation" in page.locator("#textRecovery").inner_text()
            assert page.locator(".columns>.card").count() == 60
            assert page.locator(".columns>.card>.output").count() == 60
            assert page.locator(".source-prompt[open]").count() == 0
            assert page.locator("#trainingExamples figure").count() == 48
            page.locator("#trainingReferences>summary").click()
            first_reference = page.locator("#trainingExamples img").first
            first_reference.scroll_into_view_if_needed()
            page.wait_for_function(
                "(image) => image.complete && image.naturalWidth > 0",
                arg=first_reference.element_handle(), timeout=30000,
            )
            for index, example in enumerate(data["training_examples"]):
                figure = page.locator("#trainingExamples figure").nth(index)
                assert figure.get_attribute("data-training-id") == example["sample_id"]
                assert figure.locator("img").get_attribute("src") == example["image"]
                assert json.loads(figure.locator("pre").text_content()) == example["astra_observation"]
            page.locator("#trainingReferences>summary").click()
            for index, row in enumerate(data["rows"]):
                pair = page.locator(".pair").nth(index)
                assert pair.get_attribute("data-key") == " / ".join(map(str, row["key"]))
                assert pair.locator(".feedback>p").first.text_content() == row["feedback"]
                for column, version in enumerate(("v6_4", "v6_5")):
                    card = pair.locator(".card").nth(column)
                    assert card.locator(".output").get_attribute("src") == row[version]["image"]
                    assert card.locator(".source-prompt>p").text_content() == row[version]["prompt"]
            for index in (0, 29):
                pair = page.locator(".pair").nth(index)
                for column in (0, 1):
                    image = pair.locator(".output").nth(column)
                    image.scroll_into_view_if_needed()
                    image.evaluate("(image) => image.loading = 'eager'")
                    page.wait_for_function(
                        "(image) => image.complete && image.naturalWidth === 2368 && image.naturalHeight === 1776",
                        arg=image.element_handle(), timeout=60000,
                    )
            page.locator("#showPrompts").check()
            assert page.locator(".source-prompt[open]").count() == 60
            page.locator("#showPrompts").uncheck()
            first = page.locator(".pair").first
            first.locator(".source-context>summary").click()
            contexts = first.locator(".source-context pre").all_text_contents()
            assert contexts == [
                value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
                for value in (data["rows"][0]["source_input"]["smart_brief"],
                              data["rows"][0]["source_input"]["source_messaging"])
            ]
            first.locator(".source-context>summary").click()
            image = first.locator(".output").first
            image.click()
            assert page.locator("#lightbox").is_visible()
            assert page.locator("#originalImage").get_attribute("href") == urljoin(
                origin + "/gallery/index.html", data["rows"][0]["v6_4"]["image"],
            )
            page.locator("#closeImage").click()
            assert not page.locator("#lightbox").is_visible()
            for link in page.locator(".downloads a").all():
                response = page.request.get(origin + "/gallery/" + link.get_attribute("href"))
                assert response.ok
            for device in {row["key"][0] for row in data["rows"]}:
                page.locator("#device").select_option(device)
                expected = sum(row["key"][0] == device for row in data["rows"])
                assert page.locator(".pair").count() == expected
            page.locator("#device").select_option("")
            assert page.locator(".pair").count() == 30
            assert page.locator(".columns").first.evaluate(
                "(element) => getComputedStyle(element).gridTemplateColumns.split(' ').length"
            ) == 2
            page.set_viewport_size({"width": 390, "height": 844})
            assert page.locator(".columns").first.evaluate(
                "(element) => getComputedStyle(element).gridTemplateColumns.split(' ').length"
            ) == 1
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            assert not page.locator("#error").inner_text()
            assert not errors, errors
            browser.close()
        study.write(HERE / "browser_validation.json", {
            "passed": True, "at_utc": study.now(), "rows": 30, "image_bindings": 60,
            "all_raw_image_hashes_verified": True,
            "actual_training_thumbnail_and_astra_observation_bindings": 48,
            "first_and_last_actual_image_pixels": "2368x1776",
            "original_prompts_feedback_sources_and_downloads": "passed",
            "original_native_and_explicit_recovery_outcomes": "truthful and visible",
            "device_filter_prompt_expansion_lightbox_desktop_mobile": "passed",
            "javascript_executed_without_page_errors": True,
            "ims": "mocked; live gateway/SSO/annotation behavior not certified",
            "asset_manifest_sha256": study.sha(manifest_path),
            "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "temporary_http_service": "stopped in finally",
        })
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    print(json.dumps({"browser_passed": True, "rows": 30, "image_bindings": 60}))


if __name__ == "__main__":
    main()
