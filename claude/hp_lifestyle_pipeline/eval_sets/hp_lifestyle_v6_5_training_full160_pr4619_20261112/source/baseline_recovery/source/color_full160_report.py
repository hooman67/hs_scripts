import csv
import gzip
import io
import itertools
import json
import shutil
import subprocess

import blue_poc as blue
import color_full160 as batch
from PIL import Image
from pilot import CODE, digest, load, save


def build():
    root = batch.ROOT
    cases, manifest = load(root / "pilot-cases.json"), load(root / "pilot-manifest.json")
    summary = load(root / "pilot-generation-summary.json")
    assert summary["completed"] == len(cases) == manifest["cases"] and summary["status"] != "running"
    for name, checksum in manifest["source_files"].items():
        assert digest((CODE / name).read_bytes()) == checksum
    for name, checksum in manifest["helper_files"].items():
        assert digest((blue.SCRIPTS / name).read_bytes()) == checksum
    swatches, proof = load(root / "blue-lookup-swatches.json"), load(root / "swatch-source-proof.json")
    assert digest((root / "full_element_histogram.csv.gz").read_bytes()) == manifest["lookup_sha256"]
    output = root / "comparison"
    output.mkdir(exist_ok=True)

    def asset(source, relative):
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        return relative

    def image(source, label, kind="model_output"):
        return {"asset_type": "image", "is_model_input_or_output": kind,
                "image_src": source, "meta_text": {"label": label}}

    def text(label, value):
        return {"asset_type": "text", "text_content": value, "meta_text": {"label": label}}

    rows, records, members = [], [], set()
    native_success = fallback_count = 0
    for case in cases:
        native_folder, folder = root / "native/rows" / case["id"], root / "color/rows" / case["id"]
        native, color = load(native_folder / "result.json"), load(folder / "result.json")
        context = native.get("scap_context", {})
        fallback = context.get("statistics_disabled", False)
        fallback_count += fallback
        assert native["input_fingerprint"] == case["user_prompt_sha256"]
        expected_identity = manifest["prior_native_identity"] if case["native_reused"] else manifest["fallback_identity"]
        assert native["scap_inputs"] == expected_identity
        assert color["original_prompt"] == (native["prompt"] or "No image prompt produced.")
        media = []
        number = case["row_idx"]
        if fallback:
            assert context["matched_environment"] is None and context["fields"] == {}
            assert context["cohort_n"] is None
            assert context["environment_selection"]["prompt_quote"] in case["user_prompt"]
            if native["status"] == "ok":
                assert native["scap_usage"] == [] and native["background_density"]["additions"] == []
                assert native["background_density"]["level"] == "not_assessed"
        if native["status"] == "ok":
            native_success += 1
            calls = load(native_folder / "native_calls.json")
            expected_text = 4 if fallback else 5
            assert [c["kind"] for c in calls] == ["text"] * expected_text + ["image"]
            assert all(c["status"] == "ok" for c in calls)
            raw = (native_folder / "gpt_1.png").read_bytes()
            assert digest(raw) == calls[-1]["sha256"]
            assert Image.open(io.BytesIO(raw)).size == (2368, 1776)
            request = load(native_folder / f"native_{expected_text + 1:02}_request.json")
            assert request["prompt"] == native["prompt"] and request["mask"] is None
            assert len(request["images"]) == request["n"] == 1
            assert request["images"][0]["sha256"] == digest((native_folder / "geometry_guide.png").read_bytes())
            base = load(native_folder / "scap_base_writing_response.json")
            assert (native["camera"], native["layout"]) == (base["camera"], base["layout"])
            media.append(image(asset(native_folder / "gpt_1.png", f"images/{number}-native.png"), batch.LEFT))
        else:
            media.append(text("Native control failed", native["error"]))
        calls = load(folder / "native_calls.json")
        assert sum(c["kind"] == "image" for c in calls) <= 1
        if color["prompt"]:
            colored, revised, plan = batch.combined_plan(
                native["prompt"], load(folder / "blue_response.json"),
                load(folder / "wall_response.json"), swatches, proof,
            )
            assert (colored, revised, plan) == (color["blue_prompt"], color["prompt"], color["plan"])
            assert len(set(blue.HEX.findall(revised))) == 2 and revised.endswith(blue.LIGHTING)
            members.update((b["element"], b["hex"]) for b in plan["blue"]["bindings"])
        if color["status"] == "ok":
            raw = (folder / "gpt_1.png").read_bytes()
            assert digest(raw) == color["sha256"]
            assert Image.open(io.BytesIO(raw)).size == (2368, 1776)
            if not case["color_reused"]:
                assert [c["kind"] for c in calls] == ["text", "text", "image"]
                assert all(c["status"] == "ok" for c in calls)
                assert digest(raw) == calls[-1]["sha256"]
                request = load(folder / "native_03_request.json")
                assert request["prompt"] == color["prompt"] and request["mask"] is None
                assert len(request["images"]) == request["n"] == 1
                assert request["images"][0]["sha256"] == digest((native_folder / "geometry_guide.png").read_bytes())
            else:
                assert not calls and color["reused_from"]
            media.append(image(asset(folder / "gpt_1.png", f"images/{number}-color.png"), batch.RIGHT))
        else:
            assert color["error"]
            media.append(text("Color variant failed or blocked", color["error"]))
        if (native_folder / "geometry_guide.png").exists():
            media.append(image(asset(native_folder / "geometry_guide.png", f"inputs/{number}-guide.png"),
                               "Shared native geometry guide", "model_input"))
        else:
            media.append(image(asset(root / case["product_path"], f"inputs/{case['product_sha256']}.png"),
                               "Original product; native guide unavailable", "model_input"))
        media.extend([
            text("Original V6.4 user prompt", case["user_prompt"]),
            text("Exact control image prompt", color["original_prompt"]),
            text("Exact POC image prompt", color["prompt"] or "No image prompt produced."),
            text("Blue choices and wall-only edit audit", json.dumps(color["plan"], indent=2)),
            text("Statistics/fallback audit", json.dumps(context, indent=2)),
        ])
        details = {
            "Generation": color["status"], "Input group": case["group"], "Prompt rank": case["rank"],
            "Device": case["device"], "Camera": case["camera"], "Environment": case["environment"],
            "Statistics": "NO STATISTICS - approved fallback" if fallback else
            f"{context.get('family', 'Unavailable')} / {context.get('matched_environment', 'Unavailable')}",
            "Native control": "Prior success reused" if case["native_reused"] else "New authorized retry",
            "Color result": "Ten-case POC output reused unchanged" if case["color_reused"] else "New color/wall output",
            "Previous failure": case["previous_failure"] or "None",
        }
        if color["plan"]:
            details["Blue bindings"] = "; ".join(
                f"{b['element']} {b['hex']}" for b in color["plan"]["blue"]["bindings"]
            )
            details["Wall treatment"] = color["plan"]["wall"]["treatment_type"]
        rows.append({"meta_data": {"row_idx": number, "evalset_item_id": case["id"],
                                  "key_val_informations": details}, "images": media})
        records.append({"case": case, "native": native, "result": color})
        for label, source in (("native", native_folder), ("color", folder)):
            for path in source.glob("*.json"):
                asset(path, f"records/{case['id']}/{label}/{path.name}")
    found = set()
    with gzip.open(root / "full_element_histogram.csv.gz", "rt", newline="") as stream:
        for record in itertools.islice(csv.reader(stream), 1, None):
            pair = (record[0], record[1].upper())
            if pair in members:
                assert int(record[2]) == proof[f"{pair[0]}/{pair[1]}"]["pixel_count"]
                found.add(pair)
    assert found == members
    save(root / "pilot-validation.json", {
        "passed": True, "cases": len(cases), "native_success": native_success,
        "color_success": summary["success"], "color_failed": summary["failed"],
        "no_statistics_fallback_cases": fallback_count,
        "full_source_hex_membership_checked": True, "single_image_contracts_checked": True,
        "minimal_color_and_wall_insertions_checked": True, "raw_native_bytes_preserved": True,
        "fallback_does_not_borrow_statistics": True,
    })
    save(output / "data.json", {
        "is_secure": True, "meta_texts": [
            "PR #4619 - full 160: contrasting lookup blues + vibrant lighting + artistic walls",
            ["Experiment", {
                "Scope": manifest["scope"],
                "Native controls": f"{native_success}/{len(cases)} successful, including reused prior successes.",
                "Color results": f"{summary['success']}/{len(cases)} successful; {summary['failed']} failed.",
                "Fallback": manifest["fallback"], "Fallback cases": fallback_count,
                "Reused latest POC outputs": summary["color_reused"],
                "Concurrency": manifest["workers"], "Limits": manifest["limits"],
                "Lookup": swatches["selection"],
                "Conditioning": "GPT Image receives only the final text and native guide, never the lookup table.",
                "Review": "Good/Bad per method; bulk ratings, browser persistence and JSON export.",
            }],
        ], "links": {
            "Prior native 160 comparison": manifest["prior_native_report"],
            "Ten-case color/wall POC": manifest["prior_color_report"],
            "Run manifest": "manifest.json", "Audited results": "results.json",
        }, "rows": rows,
    })
    save(output / "results.json", records)
    viewer = (blue.SCRIPTS.parent / "v64-full30/viewer-template.html").read_text()
    old = "['Baseline #4523', 'Adaptive backgrounds + realism']"
    assert viewer.count(old) == 1
    viewer = viewer.replace(old, repr([batch.LEFT, batch.RIGHT]))
    for name in ("viewer.html", "index.html"):
        (output / name).write_text(viewer)
    for source, target in (
        ("pilot-manifest.json", "manifest.json"), ("pilot-generation-summary.json", "generation_summary.json"),
        ("pilot-validation.json", "validation.json"), ("blue-lookup-swatches.json", "blue-lookup-swatches.json"),
        ("swatch-source-proof.json", "swatch-source-proof.json"), ("profiles.json", "profiles.json"),
    ):
        asset(root / source, target)
    for name in manifest["helper_files"]:
        asset(blue.SCRIPTS / name, "source/" + name)
    for name in manifest["source_files"]:
        asset(CODE / name, "source/" + name)
    save(root / "pilot-build-receipt.json", {"files": {
        path.relative_to(output).as_posix(): digest(path.read_bytes())
        for path in sorted(output.rglob("*")) if path.is_file()
    }})
    print(json.dumps({"built": len(cases), "native_success": native_success,
                      "color_success": summary["success"], "fallbacks": fallback_count}), flush=True)


def finish():
    build()
    batch.progress("browser_check", expected=160)
    subprocess.run([
        "/mnt/localssd/pw/venv/bin/python", str(blue.SCRIPTS / "check_blue_poc.py"),
        "--root", str(batch.ROOT),
    ], check=True)
    import report_pilot

    report_pilot.ROOT = batch.ROOT
    batch.progress("publishing", expected=160)
    report_pilot.publish()
    receipt = load(batch.ROOT / "pilot-publication-receipt.json")
    summary = load(batch.ROOT / "pilot-generation-summary.json")
    batch.progress("published", url=receipt["url"], color_success=summary["success"],
                   color_failed=summary["failed"], native_retry_success=summary["native_retry_success"])
