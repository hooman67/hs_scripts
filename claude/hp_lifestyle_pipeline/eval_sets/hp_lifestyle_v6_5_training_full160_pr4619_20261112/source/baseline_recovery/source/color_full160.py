import argparse
import concurrent.futures
import io
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

import blue_poc as blue
import wall_poc as wall
from fallback_profiles import POLICY, FallbackProfiles
from PIL import Image
from pilot import CODE, COMMIT, AuditClient, digest, load, save

ROOT = Path("/mnt/localssd/hp-pr4619-full160-color-walls-20w-6cd5fab9-20261111")
NATIVE = blue.CONTROL
BLUE = Path("/mnt/localssd/hp-pr4619-blue-lookup-poc-6cd5fab9-20261111")
WALL = Path("/mnt/localssd/hp-pr4619-artistic-wall-poc-6cd5fab9-20261111")
VERSION = "full160-lookup-blue-lighting-artistic-walls-v3"
LEFT, RIGHT = "Native background + realism control", "Lookup blues + lighting + artistic walls"


def progress(phase, **fields):
    value = {"phase": phase, "updated_at": datetime.now(timezone.utc).isoformat(), **fields}
    save(ROOT / "background-status.json", value)
    print(json.dumps(value), flush=True)


def combined_plan(prompt, blue_response, wall_response, swatches, proof):
    colored, blue_plan = blue.apply_bindings(prompt, blue_response, swatches, proof)
    revised, wall_plan = wall.apply_wall(colored, wall_response, base_plan=blue_plan)
    return colored, revised, {"blue": blue_plan, "wall": wall_plan["wall_refinement"]}


def prepare():
    ROOT.mkdir(exist_ok=True)
    assert not (ROOT / "pilot-manifest.json").exists(), "Batch already prepared"
    previous_manifest = load(NATIVE / "pilot-manifest.json")
    assert previous_manifest["commit"] == COMMIT
    for name, checksum in previous_manifest["source_files"].items():
        assert digest((CODE / name).read_bytes()) == checksum
    for name in ("full_element_histogram.csv.gz", "blue-lookup-swatches.json", "swatch-source-proof.json"):
        shutil.copyfile(WALL / name, ROOT / name)
    for name in ("profiles.json", "reference_catalog.json", "ref_captions.json"):
        shutil.copyfile(NATIVE / name, ROOT / name)
    cases = load(NATIVE / "pilot-cases.json")
    swatches, proof = load(ROOT / "blue-lookup-swatches.json"), load(ROOT / "swatch-source-proof.json")
    copied_products = set()
    for case in cases:
        old = NATIVE / "run/rows" / case["id"]
        native = load(old / "result.json")
        case["native_reused"] = native["status"] == "ok"
        case["previous_failure"] = native["error"]
        case["color_reused"] = False
        product = ROOT / case["product_path"]
        if case["product_path"] not in copied_products:
            product.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(NATIVE / case["product_path"], product)
            assert digest(product.read_bytes()) == case["product_sha256"]
            copied_products.add(case["product_path"])
        if not case["native_reused"]:
            continue
        target = ROOT / "native/rows" / case["id"]
        target.mkdir(parents=True, exist_ok=False)
        for path in old.iterdir():
            if path.suffix == ".json" or path.name in ("gpt_1.png", "geometry_guide.png"):
                shutil.copyfile(path, target / path.name)
        assert native["input_fingerprint"] == case["user_prompt_sha256"]
        assert native["scap_inputs"] == previous_manifest["scap_identity"]
        prior_wall = WALL / "run/rows" / case["id"]
        if not (prior_wall / "result.json").exists():
            continue
        old_wall = load(prior_wall / "result.json")
        assert old_wall["status"] == "ok"
        old_blue = load(BLUE / "run/rows" / case["id"] / "result.json")
        assert old_blue["original_prompt"] == native["prompt"]
        assert digest((target / "geometry_guide.png").read_bytes()) == digest(
            (WALL / "controls" / case["id"] / "geometry_guide.png").read_bytes()
        )
        blue_response = load(BLUE / "run/rows" / case["id"] / "native_01_response.json")
        wall_response = load(prior_wall / "native_01_response.json")
        colored, revised, plan = combined_plan(native["prompt"], blue_response, wall_response, swatches, proof)
        assert revised == old_wall["prompt"] and colored == old_blue["prompt"]
        color = ROOT / "color/rows" / case["id"]
        color.mkdir(parents=True, exist_ok=False)
        shutil.copyfile(prior_wall / "gpt_1.png", color / "gpt_1.png")
        assert digest((color / "gpt_1.png").read_bytes()) == old_wall["sha256"]
        save(color / "blue_response.json", blue_response)
        save(color / "wall_response.json", wall_response)
        save(color / "native_calls.json", [])
        save(color / "result.json", {
            "id": case["id"], "status": "ok", "error": None, "policy": VERSION,
            "original_prompt": native["prompt"], "blue_prompt": colored, "prompt": revised,
            "plan": plan, "sha256": old_wall["sha256"], "reused_from": load(WALL / "pilot-manifest.json")["run_id"],
        })
        case["color_reused"] = True
    assert len(cases) == 160 and sum(c["native_reused"] for c in cases) == 138
    assert sum(c["color_reused"] for c in cases) == 10
    run_id = "hp160-v64-bluehex-lighting-artistic-walls-20w-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    manifest = {
        "run_id": run_id, "s3_prefix": "hp-data-artifacts/hp-3p-gpt25/" + run_id,
        "cases": 160, "workers": 20, "policy": VERSION, "commit": COMMIT,
        "native_retry_policy": POLICY, "fallback_identity": FallbackProfiles(ROOT / "profiles.json").identity,
        "prior_native_identity": previous_manifest["scap_identity"],
        "native_retries_authorized": 22, "native_reused": 138, "color_reused": 10, "new_color_cases": 150,
        "rating_left": LEFT, "rating_right": RIGHT,
        "lookup_sha256": blue.LOOKUP_SHA, "lookup_s3_key": blue.LOOKUP_KEY,
        "source_files": previous_manifest["source_files"],
        "helper_files": {name: digest((blue.SCRIPTS / name).read_bytes()) for name in (
            "color_full160.py", "color_full160_report.py", "fallback_profiles.py",
            "blue_poc.py", "wall_poc.py", "pilot.py", "check_blue_poc.py", "report_pilot.py",
            "live_gallery.py", "live-gallery-index.html", "live-gallery-main.js", "live-gallery-style.css",
        )},
        "prior_native_report": load(NATIVE / "pilot-publication-receipt.json")["url"],
        "prior_color_report": load(WALL / "pilot-publication-receipt.json")["url"],
        "scope": "Retry exactly the 22 historical native failures in new directories, then cover all 160 "
                 "original prompts with the latest color, lighting and artistic-wall final-prompt treatment.",
        "fallback": "Only validated unsupported/missing same-family cohorts may skip statistics. "
                    "Stage B and text-only realism remain; no statistical additions or borrowed cohorts.",
        "limits": "Twenty total row workers, not twenty per variant. No automatic retries. Each new native "
                  "control and each new color variant has at most one image call. Frozen guides and "
                  "insertion-only color/wall edits do not guarantee identical non-target rendered pixels, "
                  "calibrated rendered HEX values, product fidelity or visual acceptance. No commits/pushes.",
    }
    save(ROOT / "pilot-cases.json", cases)
    save(ROOT / "pilot-manifest.json", manifest)
    progress("prepared", expected=160, workers=20, native_retries=22, new_color=150, reused_color=10,
             run_id=run_id)


def call_counts(folder):
    path = folder / "native_calls.json"
    calls = load(path) if path.exists() else []
    return {"text": sum(c["kind"] == "text" for c in calls),
            "image": sum(c["kind"] == "image" for c in calls)}


def row_record(case):
    native = load(ROOT / "native/rows" / case["id"] / "result.json")
    color = load(ROOT / "color/rows" / case["id"] / "result.json")
    native_calls = {"text": 0, "image": 0} if case["native_reused"] else call_counts(
        ROOT / "native/rows" / case["id"]
    )
    color_calls = call_counts(ROOT / "color/rows" / case["id"])
    return {
        "id": case["id"], "native_status": native["status"], "native_error": native["error"],
        "status": color["status"], "error": color["error"],
        "native_reused": case["native_reused"], "color_reused": case["color_reused"],
        "no_statistics_fallback": native.get("scap_context", {}).get("statistics_disabled", False),
        "text_calls": native_calls["text"] + color_calls["text"],
        "image_calls": native_calls["image"] + color_calls["image"],
    }


def generate():
    import hp3p.pipeline as pipeline
    from hp3p.catalog import load_catalog
    from hp3p.evalset import Row
    from hp3p.openai_client import OpenAIClient

    manifest, cases = load(ROOT / "pilot-manifest.json"), load(ROOT / "pilot-cases.json")
    assert manifest["cases"] == len(cases) == 160 and manifest["workers"] == 20
    for name, checksum in manifest["helper_files"].items():
        assert digest((blue.SCRIPTS / name).read_bytes()) == checksum
    for name, checksum in manifest["source_files"].items():
        assert digest((CODE / name).read_bytes()) == checksum
    with (ROOT / "generation.lock").open("x") as lock:
        lock.write(VERSION + "\n")
    fields = Path(f"/proc/{os.getpid()}/stat").read_text().rpartition(")")[2].split()
    save(ROOT / "generation-owner.json", {"pid": os.getpid(), "identity": fields[19]})
    pipeline.SCAP_VERSION = POLICY
    profiles = FallbackProfiles(ROOT / "profiles.json")
    assert profiles.identity == manifest["fallback_identity"]
    base = OpenAIClient()
    catalog, captions = load_catalog(ROOT / "reference_catalog.json"), load(ROOT / "ref_captions.json")
    swatches, proof = load(ROOT / "blue-lookup-swatches.json"), load(ROOT / "swatch-source-proof.json")
    blue_schema = {
        "type": "object", "additionalProperties": False, "required": ["bindings"],
        "properties": {"bindings": {
            "type": "array", "minItems": 2, "maxItems": 2,
            "items": {"type": "object", "additionalProperties": False,
                      "required": ["anchor", "element", "hex", "reason"],
                      "properties": {
                          "anchor": {"type": "string"}, "hex": {"type": "string"},
                          "reason": {"type": "string"},
                          "element": {"type": "string", "enum": sorted(swatches["elements"])},
                      }},
        }},
    }
    wall_schema = {
        "type": "object", "additionalProperties": False,
        "required": ["anchor", "wall_treatment", "treatment_type", "reason"],
        "properties": {name: {"type": "string"} for name in
                       ("anchor", "wall_treatment", "treatment_type", "reason")},
    }

    def stage(case, name):
        save(ROOT / "stages" / (case["id"] + ".json"),
             {"stage": name, "at": datetime.now(timezone.utc).isoformat()})

    def one(case):
        native_folder = ROOT / "native/rows" / case["id"]
        if not case["native_reused"]:
            stage(case, "native_retry")
            native_folder.mkdir(parents=True, exist_ok=False)
            audit = AuditClient(base, native_folder)
            row = Row(case["id"], case["user_prompt"], case["product_path"], 2368, 1776, [])
            pipeline.run_row(
                row, audit, catalog, ROOT / "native", (ROOT / case["product_path"]).read_bytes(),
                captions, ref_count=1, size=(2368, 1776),
                camera=case["source_camera_metadata"], scap=profiles,
            )
        native = load(native_folder / "result.json")
        folder = ROOT / "color/rows" / case["id"]
        folder.mkdir(parents=True, exist_ok=False)
        audit = AuditClient(base, folder)
        result = {
            "id": case["id"], "status": "error", "error": None, "policy": VERSION,
            "original_prompt": native["prompt"] or "No image prompt produced.",
            "blue_prompt": None, "prompt": None, "plan": None, "reused_from": None,
        }
        try:
            assert native["status"] == "ok" or native.get("image_calls") == 1, (
                "Color variant blocked by native planning failure: " + str(native["error"])
            )
            guide = (native_folder / "geometry_guide.png").read_bytes()
            stage(case, "blue_selection")
            blue_response = audit.chat_json(blue.SYSTEM, json.dumps({
                "original_user_request": case["user_prompt"], "final_image_prompt": native["prompt"],
                "lookup": swatches, "fixed_lighting_adjustment": blue.LIGHTING,
            }, ensure_ascii=False), [], blue_schema)
            save(folder / "blue_response.json", blue_response)
            colored, blue_plan = blue.apply_bindings(native["prompt"], blue_response, swatches, proof)
            result["blue_prompt"] = colored
            stage(case, "wall_refinement")
            wall_response = audit.chat_json(wall.SYSTEM, json.dumps({
                "original_user_request": case["user_prompt"], "existing_final_image_prompt": colored,
                "unchanged_blue_bindings": blue_plan["bindings"],
            }, ensure_ascii=False), [], wall_schema)
            save(folder / "wall_response.json", wall_response)
            _, result["prompt"], result["plan"] = combined_plan(
                native["prompt"], blue_response, wall_response, swatches, proof,
            )
            stage(case, "color_image")
            raw = audit.edit_image(result["prompt"], [("image/png", guide)], "2368x1776")
            (folder / "gpt_1.png").write_bytes(raw)
            assert Image.open(io.BytesIO(raw)).size == (2368, 1776)
            result.update(status="ok", sha256=digest(raw))
        except Exception as exc:
            result["error"] = f"{type(exc).__name__}: {exc}"
        if not (folder / "native_calls.json").exists():
            save(folder / "native_calls.json", audit.calls)
        save(folder / "result.json", result)
        stage(case, "complete")
        return row_record(case)

    records = [row_record(case) for case in cases if case["color_reused"]]

    def snapshot():
        summary = {
            "status": "running", "expected": 160, "completed": len(records), "workers": 20,
            "success": sum(r["status"] == "ok" for r in records),
            "failed": sum(r["status"] != "ok" for r in records),
            "native_retries_completed": sum(not r["native_reused"] for r in records),
            "native_retry_success": sum(not r["native_reused"] and r["native_status"] == "ok" for r in records),
            "fallback_cases": sum(r["no_statistics_fallback"] for r in records),
            "native_reused": 138, "color_reused": 10,
            "text_calls": sum(r["text_calls"] for r in records),
            "image_calls": sum(r["image_calls"] for r in records), "rows": records,
        }
        save(ROOT / "pilot-generation-summary.json", summary)
        progress("generating", **{k: v for k, v in summary.items() if k != "rows"})
        return summary

    snapshot()
    pending = sorted((c for c in cases if not c["color_reused"]), key=lambda c: c["native_reused"])
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        futures = [pool.submit(one, case) for case in pending]
        for future in concurrent.futures.as_completed(futures):
            records.append(future.result())
            snapshot()
    summary = snapshot()
    summary["status"] = "completed_with_errors" if summary["failed"] else "complete"
    summary["ended_at"] = datetime.now(timezone.utc).isoformat()
    save(ROOT / "pilot-generation-summary.json", summary)


def finish():
    import color_full160_report

    color_full160_report.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("prepare", "generate", "finish", "all"))
    action = parser.parse_args().action
    if action == "all":
        with (ROOT / "background.lock").open("x") as lock:
            lock.write(VERSION + "\n")
        generate()
        finish()
    else:
        {"prepare": prepare, "generate": generate, "finish": finish}[action]()
