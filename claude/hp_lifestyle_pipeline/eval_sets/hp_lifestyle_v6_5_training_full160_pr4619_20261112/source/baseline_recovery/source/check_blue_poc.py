import argparse
import functools
import hashlib
import http.server
import json
import threading

from playwright.sync_api import sync_playwright


def check(root):
    output = root / "comparison"
    load = lambda path: json.loads(path.read_text())
    cases, results = load(root / "pilot-cases.json"), load(output / "results.json")
    data = load(output / "data.json")
    expected_count = len(cases)
    assert len(results) == len(data["rows"]) == expected_count
    manifest = load(root / "pilot-manifest.json")
    left_method = manifest.get("rating_left", "Native PR #4619 control")
    receipt = load(root / "pilot-build-receipt.json")
    for name, checksum in receipt["files"].items():
        assert hashlib.sha256((output / name).read_bytes()).hexdigest() == checksum

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(Handler, directory=str(output)),
    )
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    errors = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page(viewport={"width": 1800, "height": 1100})
                page.on("pageerror", lambda exc: errors.append(str(exc)))
                base = f"http://127.0.0.1:{server.server_port}"
                response = page.goto(base + "/viewer.html?q=W10%3D", wait_until="domcontentloaded")
                assert response.status == 200
                page.wait_for_function(
                    "count => VIEW.length === count && document.querySelectorAll('.row').length > 0",
                    arg=expected_count,
                )
                assert "contrasting lookup blues" in page.locator("#title").inner_text()
                assert page.evaluate("QUESTIONS.length") == 2
                for case, record, row in zip(cases, results, data["rows"]):
                    page.evaluate("""({group, rank}) => {
                        ACTIVE_FILTERS = {'Input group': new Set([group]),
                                          'Prompt rank': new Set([String(rank)])};
                        applyView();
                    }""", {"group": case["group"], "rank": case["rank"]})
                    page.locator("#search").fill(case["user_prompt"])
                    page.wait_for_function(
                        "key => VIEW.length === 1 && MERGED[VIEW[0]].key === key", arg=case["id"],
                    )
                    card = page.locator(".row").first
                    assert card.get_by_role("checkbox").count() == 4
                    count = sum(item["asset_type"] == "image" for item in row["images"])
                    page.wait_for_function(
                        "count => { const imgs = [...document.querySelectorAll('.row .assets img')]; "
                        "return imgs.length === count && imgs.every(img => img.complete && img.naturalWidth > 0); }",
                        arg=count,
                    )
                    for label, expected in (
                        ("Original V6.4 user prompt", case["user_prompt"]),
                        ("Exact control image prompt", record["result"]["original_prompt"]),
                        ("Exact POC image prompt", record["result"]["prompt"] or "No image prompt produced."),
                    ):
                        caption = card.locator(".cap").filter(has=page.locator(".cap-h", has_text=label))
                        assert caption.locator(".body").inner_text() == expected
                good = page.get_by_role("checkbox", name=left_method + ": Good", exact=True)
                bad = page.get_by_role("checkbox", name=left_method + ": Bad", exact=True)
                good.check()
                bad.check()
                assert bad.is_checked() and not good.is_checked()
                page.once("dialog", lambda dialog: dialog.accept())
                page.locator("#allMethodsGood").click()
                assert page.evaluate(
                    "MERGED.every(m => QUESTIONS.every(q => ANNO[m.key].answers[q.id] === 'good'))"
                )
                page.goto(base + "/index.html?q=W10%3D", wait_until="domcontentloaded")
                page.wait_for_function("count => VIEW.length === count", arg=expected_count)
                assert page.evaluate("pendingRows().length") == 0
                with page.expect_download() as downloaded:
                    page.locator("#exportRatings").click()
                temporary = root / "browser-ratings.json"
                downloaded.value.save_as(temporary)
                exported = load(temporary)
                assert exported["report"]["complete"] and len(exported["rows"]) == expected_count
                temporary.unlink()
                page.evaluate("""group => {
                    ACTIVE_FILTERS = {'Input group': new Set([group]), 'Prompt rank': new Set(['1'])};
                    applyView();
                }""", cases[0]["group"])
                page.locator("#expandInputs").click()
                page.screenshot(path=str(root / "poc-desktop.png"))
                page.set_viewport_size({"width": 390, "height": 1000})
                assert page.locator(".row").first.get_by_role("checkbox").count() == 4
                page.screenshot(path=str(root / "poc-mobile.png"))
                assert not errors, errors
                (root / "pilot-browser-check.json").write_text(json.dumps({
                    "passed": True, "cases": expected_count, "exact_prompts_checked": True,
                    "ratings_persistence_bulk_export_checked": True,
                    "javascript_errors": errors, "build_receipt": receipt,
                }, indent=2) + "\n")
                print(json.dumps({"browser_check": "passed", "cases": expected_count}), flush=True)
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join()


if __name__ == "__main__":
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    check(parser.parse_args().root)
