"""User-authorized historical r2 expansion; no changes to either frozen candidate."""
from __future__ import annotations

import argparse
import concurrent.futures
import fcntl
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
R1 = HERE.parent.parent
R2 = R1 / "r2"
SOURCE = HERE.parent / "source/viewer.html"
EXPECTED_SOURCE_SHA = "ba33d6f719b1169eadab5ee5f036611a4edf5a67e961f8d0709b741ca0aa187b"
SCHEMA_VERSION = "hp-original-gallery-v3.1-r1-r2-v1"
LOCK = threading.Lock()
LOCAL = threading.local()
_RUNNERS = None


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    staging = path.with_name(path.name + ".writing")
    staging.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    os.replace(staging, path)


def runners():
    global _RUNNERS
    if _RUNNERS is None:
        sys.path.insert(0, str(R2))
        loaded = {}
        for version, root in (("r2", R2), ("r1", R1)):
            spec = importlib.util.spec_from_file_location(f"gallery_frozen_{version}", root / "run_judge.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            loaded[version] = module
        _RUNNERS = loaded
    return _RUNNERS


def runtime(record):
    return {
        "generated_image": record["generated_image"]["local_path"],
        "twin_image": record["twin_image"]["local_path"],
        "product_type": record["product_type"], "scene_prompt": record["scene_prompt"],
        "image_stage": "scene_generation",
    }


def source_mapping(viewer, base):
    from bs4 import BeautifulSoup
    rows = []
    for section in BeautifulSoup(viewer.read_text(), "html.parser").find_all("section"):
        heading, container = section.find("h2"), section.find("div", class_="row")
        if not heading or not container:
            continue
        request = section.find("p", class_="req").get_text(" ", strip=True)
        if not request.startswith("User request:"):
            raise ValueError("Missing original scene prompt")
        twin = urljoin(base, section.find("details", class_="in").find("a", href=True)["href"])
        product = section.find("p", class_="meta").get_text(" ", strip=True).split(" · ", 1)[0].strip()
        figures = container.find_all("figure", recursive=False)
        if len(figures) != 4:
            raise ValueError("Source row is not exactly four original variants")
        for index, figure in enumerate(figures):
            rows.append({
                "source_row_id": heading.get_text(" ", strip=True),
                "variant": figure.find("figcaption").get_text(" ", strip=True),
                "column_index_0based": index,
                "generated_image_url": urljoin(base, figure.find("a", href=True)["href"]),
                "twin_image_url": twin,
                "scene_prompt": request.removeprefix("User request:").strip(),
                "product_type": product,
            })
    return rows


def verify_mapping(inventory):
    if sha(SOURCE) != EXPECTED_SOURCE_SHA or SOURCE.read_bytes() != (R1 / "sources/viewer.html").read_bytes():
        raise ValueError("Refreshed source differs from the frozen source HTML")
    parsed = source_mapping(SOURCE, inventory["source_viewer"]["url"])
    expected = []
    for record in inventory["records"]:
        expected.append({
            **{key: record[key] for key in ("source_row_id", "variant", "column_index_0based",
                                          "scene_prompt", "product_type")},
            "generated_image_url": record["generated_image"]["url"],
            "twin_image_url": record["twin_image"]["url"],
        })
    if parsed != expected or len(parsed) != 128 or len({r["generated_image_url"] for r in parsed}) != 128:
        raise ValueError("Exact source row/variant/URL/prompt mapping mismatch")
    assets = {record[key]["local_path"]: record[key]["sha256"]
              for record in inventory["records"] for key in ("generated_image", "twin_image")}
    if len(assets) != 160 or any(sha(path) != digest for path, digest in assets.items()):
        raise ValueError("Frozen source-image hash mismatch")
    return {"source_rows": 32, "generated_outputs": 128, "image_objects_hash_verified": 160,
            "refreshed_html_matches_original_snapshot": True,
            "mapping_verified": ["source_row_id", "variant", "column_index", "generated_image_url",
                                 "twin_image_url", "scene_prompt", "product_type"],
            "live_s3_image_bytes_refetched": False,
            "source_object": read(SOURCE.parent / "object.json")}


def protected_files():
    paths = {}
    for root in (R1, R2):
        manifest_path = root / "ARTIFACT_MANIFEST.json"
        manifest = read(manifest_path)
        for row in manifest["files"]:
            if sha(row["path"]) != row["sha256"]:
                raise ValueError("Pre-existing artifact changed")
            paths[row["path"]] = row["sha256"]
        paths[str(manifest_path)] = sha(manifest_path)
        freeze_path = root / "protocol_freeze.json"
        for row in read(freeze_path)["files"]:
            if sha(row["path"]) != row["sha256"]:
                raise ValueError("Frozen dependency changed")
            paths[row["path"]] = row["sha256"]
        paths[str(freeze_path)] = sha(freeze_path)
    paths[str(SOURCE)] = sha(SOURCE)
    return [{"path": path, "sha256": digest} for path, digest in sorted(paths.items())]


def audit_result(version, record, result_path):
    runner = runners()[version]
    result_path = Path(result_path)
    result = read(result_path)
    expected = runtime(record)
    freeze = sha((R1 if version == "r1" else R2) / "protocol_freeze.json")
    if (not result["ok"] or result["runtime_input"] != expected
            or result["protocol_freeze_sha256"] != freeze
            or result["protocol_version"] != runner.PROTOCOL_VERSION):
        raise ValueError("Preserved result input/protocol identity mismatch")
    observations, models, calls = {}, set(), []
    for stage, artifact in result["stages"].items():
        stage_path = Path(artifact["path"])
        if sha(stage_path) != artifact["sha256"]:
            raise ValueError("Stage hash binding mismatch")
        saved = read(stage_path)
        request = read(stage_path.parent / "request.json")
        raw_path = stage_path.parent / "response.json"
        raw = read(raw_path)
        choice = raw["choices"][0]
        if (not saved["ok"] or not runner.identity_matches(raw.get("model"))
                or choice["finish_reason"] != "stop" or choice["message"].get("refusal")):
            raise ValueError("Invalid/incomplete preserved model response")
        if (request["runtime_input"] != expected or request["protocol_version"] != runner.PROTOCOL_VERSION
                or request["protocol_freeze_sha256"] != freeze
                or request["model_requested"] != "gpt-5.5" or request["reasoning_effort"] != "high"
                or request["transport_max_retries"] != 2 or request["timeout_seconds"] != 180
                or request["semantic_retries"] != 0
                or request["target_comments_or_expectations_passed"] is not False):
            raise ValueError("Stage input/settings/label-isolation mismatch")
        if request["fingerprint"] != runner.json_sha({k: v for k, v in request.items() if k != "fingerprint"}):
            raise ValueError("Request fingerprint mismatch")
        if saved["fingerprint"] != request["fingerprint"]:
            raise ValueError("Saved response fingerprint mismatch")
        for key in ("generated_image", "twin_image"):
            if request["images"][key]["sha256"] != record[key]["sha256"]:
                raise ValueError("Model image differs from frozen inventory")
        names = request["requested_components"]
        schema = runner.component_schema(names) if names else runner.SCORING.OBSERVATION_SCHEMA
        if request["max_completion_tokens"] != (6000 if names else 12000):
            raise ValueError("Frozen token budget changed")
        value = json.loads(choice["message"]["content"])
        if version == "r2":
            wire = runner.TRACE.envelope_schema(schema)
            observation = runner.TRACE.validate(value, schema)
            if saved["evidence_envelope"] != value:
                raise ValueError("Raw evidence envelope was edited")
        else:
            wire, observation = schema, value
        if names:
            runner.validate_components(observation, schema)
        else:
            runner.validate_new_observation(observation)
        if (saved["observation"] != observation or read(stage_path.parent / "schema.json") != wire
                or request["schema_sha256"] != runner.json_sha(wire)):
            raise ValueError("Raw observation/schema differs from saved evidence")
        root = R1 if version == "r1" else R2
        prompt = root / "prompts" / f"{stage}.md"
        if (request["system_prompt_sha256"] != sha(prompt)
                or (stage_path.parent / "system_prompt.md").read_bytes() != prompt.read_bytes()):
            raise ValueError("Frozen prompt changed")
        if stage == "independent" and request["proposals"] is not None:
            raise ValueError("Names-only verifier received proposal text")
        observations[stage] = observation
        models.add(raw["model"])
        calls.append({"stage": stage, "response_path": str(raw_path), "response_sha256": sha(raw_path),
                      "request_path": str(stage_path.parent / "request.json"),
                      "request_sha256": sha(stage_path.parent / "request.json")})
    recomputed = runner.aggregate_stages(observations["baseline"], observations["compact"],
                                         observations.get("proposal"), observations.get("independent"))
    if any(result[key] != value for key, value in recomputed.items()):
        raise ValueError("Ensemble differs from deterministic raw-response recomputation")
    return result, sorted(models), calls


def reason_for(result):
    judgment = result["application_merged_judgment"]
    observation = judgment["observation"]
    decision = result["final_decision"]
    pointer = "application_merged_judgment.observation.summary"
    text = observation["summary"]
    if observation["product_match"] != "match":
        pointer, text = "application_merged_judgment.observation.product_match_note", observation["product_match_note"]
    elif decision["verdict"] == "fail":
        material = [(name, c) for name, c in observation["components"].items()
                    if c["visibility"] in {"observed", "partial"} and c["confidence"] in {"medium", "high"}
                    and isinstance(c["severity"], int) and c["severity"] >= 2]
        if material:
            name, component = max(material, key=lambda row: row[1]["severity"])
            pointer, text = f"application_merged_judgment.observation.components.{name}.evidence", component["evidence"]
    elif decision["verdict"] == "review":
        uncertain = [(name, c) for name, c in observation["components"].items()
                     if c["visibility"] == "unobservable" or c["confidence"] == "low"]
        if decision["uncertainty_notes"]:
            pointer, text = "final_decision.uncertainty_notes[0]", decision["uncertainty_notes"][0]
        elif uncertain:
            name, component = uncertain[0]
            pointer, text = f"application_merged_judgment.observation.components.{name}.evidence", component["evidence"]
    normalized = " ".join(text.split())
    brief = normalized if len(normalized) <= 260 else normalized[:259].rsplit(" ", 1)[0] + "…"
    return brief, {"field": pointer, "original_text": text,
                   "method": "Extractive; whitespace normalization and optional 260-character clipping only."}


def complete_object(version, record, path, reused):
    result, models, calls = audit_result(version, record, path)
    reason, source = reason_for(result)
    return {
        "status": "complete", "reused": reused, "version_id": f"v3_1_{version}",
        "protocol_version": result["protocol_version"],
        "protocol_freeze_sha256": result["protocol_freeze_sha256"],
        "verdict": result["final_decision"]["verdict"],
        "score": result["application_merged_judgment"]["natural_placement_score"],
        "short_reason": reason, "short_reason_source": source,
        "result_path": str(path), "result_sha256": sha(path),
        "model_returned": models, "raw_calls": calls, "error": None,
    }


def prepare():
    if (HERE / "execution_manifest.json").exists():
        raise RuntimeError("External execution already prepared; preserve it and use run/export")
    inventory = read(R1 / "evaluation/inventory.json")
    mapping = verify_mapping(inventory)
    protected = protected_files()
    runners()["r1"].verify_freeze()
    runners()["r2"].verify_freeze()
    reused_ids = {row["id"] for row in read(R2 / "calibration/results.json")["items"] if row["ok"]}
    if len(reused_ids) != 6:
        raise ValueError("Expected the six exact preserved r2 judgments")
    reused = []
    for record in inventory["records"]:
        r1_path = R1 / "evaluation/runs/v3_1" / record["id"] / "result.json"
        r1 = complete_object("r1", record, r1_path, True)
        r2 = None
        if record["id"] in reused_ids:
            r2_path = R2 / "calibration/runs" / record["id"] / "result.json"
            r2 = complete_object("r2", record, r2_path, True)
        reused.append({"id": record["id"], "r1": r1, "r2": r2})
    write(HERE / "reused_results.json", reused)
    write(HERE / "protected_snapshot.json", {"created_utc": now(), "files": protected})
    write(HERE / "source_verification.json", {"verified_utc": now(), **mapping})
    files = [HERE / name for name in (
        "external_driver.py", "test_external_driver.py", "requirements.txt",
        "gallery_results.schema.json", "source_verification.json",
        "reused_results.json", "protected_snapshot.json")]
    manifest = {
        "created_utc": now(), "authorization": (
            "Explicit user authorization 2026-11-10: run remaining122 historical r2 once despite prior gate; "
            "no promotion, tuning, r1/V3 reruns, or new-generation judging."),
        "source_viewer_url": inventory["source_viewer"]["url"], "source_html_sha256": sha(SOURCE),
        "record_count": 128, "reused_r1": 128, "reused_r2": 6, "fresh_r2": 122,
        "workers": 4, "source_stage": "e2e_comparison_output",
        "runtime_stage_adapter": "scene_generation literal, unchanged out-of-domain diagnostic.",
        "provider": "foundry_aws_gateway.llm.get_azure_openai",
        "model": "gpt-5.5", "reasoning_effort": "high", "timeout_seconds": 180,
        "transport_max_retries": 2, "semantic_retries": 0,
        "primary_max_completion_tokens": 12000, "verifier_max_completion_tokens": 6000,
        "r1_protocol_freeze_sha256": sha(R1 / "protocol_freeze.json"),
        "r2_protocol_freeze_sha256": sha(R2 / "protocol_freeze.json"),
        "fresh_ids": [row["id"] for row in reused if row["r2"] is None],
        "files": [{"path": str(path), "sha256": sha(path)} for path in files],
    }
    write(HERE / "execution_manifest.json", manifest)
    print(json.dumps({key: manifest[key] for key in ("record_count", "reused_r1", "reused_r2", "fresh_r2")}))


def verify_execution():
    manifest = read(HERE / "execution_manifest.json")
    if any(sha(row["path"]) != row["sha256"] for row in manifest["files"]):
        raise RuntimeError("External frozen execution dependency changed")
    return manifest


def resume_state(folder):
    """A started role without a durable successful response is terminal, never resampled."""
    folder = Path(folder)
    if (folder / "terminal.json").exists():
        return "terminal"
    if (folder / "result.json").exists():
        return "saved_ensemble"
    for stage in ("baseline", "compact", "proposal", "independent"):
        role = folder / stage
        if (role / "request.json").exists():
            saved = role / "result.json"
            if not saved.exists():
                return "ambiguous_started_role"
            try:
                if not read(saved).get("ok") or not (role / "response.json").exists():
                    return "failed_started_role"
            except (ValueError, KeyError):
                return "corrupt_started_role"
    return "new_or_successful_partial"


def terminal_error(record, folder, error_type):
    stages = []
    for path in sorted(folder.glob("*/result.json")):
        saved = read(path)
        detail = {"stage": path.parent.name, "ok": saved["ok"],
                  "result_path": str(path), "result_sha256": sha(path)}
        if not saved["ok"]:
            detail.update({key: saved.get(key) for key in ("error_type", "status_code")})
        stages.append(detail)
    return {
        "status": "error", "reused": False, "version_id": "v3_1_r2",
        "protocol_version": runners()["r2"].PROTOCOL_VERSION,
        "protocol_freeze_sha256": sha(R2 / "protocol_freeze.json"),
        "verdict": None, "score": None, "short_reason": None,
        "result_path": None, "result_sha256": None, "model_returned": [],
        "error": {"error_type": error_type, "case_directory": str(folder), "stages": stages},
    }


def run_one(record, judge=None):
    folder = HERE / "runs/r2" / record["id"]
    folder.mkdir(parents=True, exist_ok=True)
    terminal = folder / "terminal.json"
    state = resume_state(folder)
    if state == "terminal":
        return read(terminal)
    if state in {"ambiguous_started_role", "failed_started_role", "corrupt_started_role"}:
        item = terminal_error(record, folder, state)
    else:
        expected = runtime(record)
        input_path = folder / "input.json"
        if input_path.exists() and read(input_path) != expected:
            raise RuntimeError("Preserved case input mismatch")
        if not input_path.exists():
            write(input_path, expected)
        try:
            for key in ("generated_image", "twin_image"):
                if sha(expected[key]) != record[key]["sha256"]:
                    raise ValueError("Frozen case image bytes changed")
            if state != "saved_ensemble":
                if judge is None:
                    import foundry_aws_gateway.llm
                    if not hasattr(LOCAL, "client"):
                        LOCAL.client = foundry_aws_gateway.llm.get_azure_openai().with_options(
                            max_retries=2, timeout=180)
                    runners()["r2"].judge(expected, folder, client=LOCAL.client)
                else:
                    judge(expected, folder)
            item = complete_object("r2", record, folder / "result.json", False)
        except Exception as exc:
            item = terminal_error(record, folder, type(exc).__name__)
    item["terminal_utc"] = now()
    write(terminal, item)
    return item


def progress():
    manifest = read(HERE / "execution_manifest.json")
    items = {}
    for case_id in manifest["fresh_ids"]:
        path = HERE / "runs/r2" / case_id / "terminal.json"
        if path.exists():
            items[case_id] = read(path)
    summary = {
        "updated_utc": now(), "expected_fresh_terminal": 122, "fresh_terminal": len(items),
        "fresh_complete": sum(v["status"] == "complete" for v in items.values()),
        "fresh_error": sum(v["status"] == "error" for v in items.values()),
        "reused_r1": 128, "reused_r2": 6, "remaining": 122 - len(items),
        "execution_manifest_sha256": sha(HERE / "execution_manifest.json"),
    }
    write(HERE / "progress.json", summary)
    return summary


def run():
    manifest = verify_execution()
    tests = read(HERE / "test_gate.json")
    if not tests["passed"] or tests["driver_sha256"] != sha(HERE / "external_driver.py"):
        raise RuntimeError("Targeted tests have not passed for this exact external driver")
    runners()["r2"].verify_freeze()
    import foundry_aws_gateway.llm
    # Authentication preflight is not a model call and prevents burning122 cases on missing access.
    foundry_aws_gateway.llm.get_azure_openai().with_options(max_retries=2, timeout=180)
    records = read(R1 / "evaluation/inventory.json")["records"]
    selected = [record for record in records if record["id"] in set(manifest["fresh_ids"])]
    with (HERE / "run.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            futures = {pool.submit(run_one, record): record["id"] for record in selected}
            for future in concurrent.futures.as_completed(futures):
                item = future.result()
                with LOCK:
                    summary = progress()
                    print(json.dumps({"id": futures[future], "status": item["status"],
                                      "verdict": item["verdict"], "score": item["score"],
                                      **summary}), flush=True)
        final = progress()
        if final["fresh_terminal"] != 122:
            raise RuntimeError("Incomplete external run")
    export()


def export():
    manifest = verify_execution()
    preserved = read(HERE / "protected_snapshot.json")["files"]
    if any(sha(row["path"]) != row["sha256"] for row in preserved):
        raise RuntimeError("An original artifact or source changed")
    reused = {row["id"]: row for row in read(HERE / "reused_results.json")}
    records, errors = [], []
    for record in read(R1 / "evaluation/inventory.json")["records"]:
        prior = reused[record["id"]]
        r2 = prior["r2"]
        if r2 is None:
            path = HERE / "runs/r2" / record["id"] / "terminal.json"
            if not path.exists():
                raise RuntimeError("Final export waits for every fresh case to become terminal")
            r2 = read(path)
            if r2["status"] == "complete":
                fresh = complete_object("r2", record, r2["result_path"], False)
                if any(r2[key] != value for key, value in fresh.items()):
                    raise ValueError("Fresh terminal differs from independently audited result")
        for candidate in (prior["r1"], r2):
            if candidate["status"] == "complete" and sha(candidate["result_path"]) != candidate["result_sha256"]:
                raise ValueError("Reused or fresh result checksum changed")
        if r2["status"] == "error":
            errors.append({"source_row_id": record["source_row_id"], "variant": record["variant"],
                           "generated_image_url": record["generated_image"]["url"], **r2["error"]})
        records.append({
            "id": record["id"], "source_row_id": record["source_row_id"], "variant": record["variant"],
            "generated_image": {key: record["generated_image"][key] for key in ("url", "sha256")},
            "r1": prior["r1"], "r2": r2,
        })
    versions = {
        version: {
            "candidate": f"V3.1 {version}", "promoted": False, "calibration_gate_met": False,
            "protocol_version": runners()[version].PROTOCOL_VERSION,
            "protocol_freeze_path": str(root / "protocol_freeze.json"),
            "protocol_freeze_sha256": sha(root / "protocol_freeze.json"),
            "model_requested": "gpt-5.5",
            "model_returned": sorted({model for row in records for model in row[version]["model_returned"]}),
        } for version, root in (("r1", R1), ("r2", R2))
    }
    lookup = {}
    for index, record in enumerate(records):
        lookup.setdefault(record["source_row_id"], {})[record["variant"]] = index
    output = {
        "schema_version": SCHEMA_VERSION, "generated_utc": now(),
        "source_viewer_url": manifest["source_viewer_url"],
        "source_html_sha256": manifest["source_html_sha256"],
        "source_object": read(SOURCE.parent / "object.json"),
        "versions": versions, "execution_manifest_sha256": sha(HERE / "execution_manifest.json"),
        "records": records, "by_source_row_variant": lookup,
        "counts": {"r1_complete": 128, "r1_reused": 128,
                   "r2_complete": sum(r["r2"]["status"] == "complete" for r in records),
                   "r2_error": len(errors), "r2_reused": 6, "r2_fresh_terminal": 122},
        "errors": errors,
        "claim_boundary": (
            "Explicit evaluation-only gate override; both candidates remain unpromoted. "
            "Original stored judge rows must stay untouched. No fresh V3/r1 rerun or new-generation judging."),
    }
    from jsonschema import Draft202012Validator
    Draft202012Validator(read(HERE / "gallery_results.schema.json")).validate(output)
    write(HERE / "gallery_results.json", output)
    write(HERE / "export_validation.json", {
        "validated_utc": now(), "source_and_original_artifacts_preserved": len(preserved),
        "records": len(records), "unique_generated_image_urls": len({r["generated_image"]["url"] for r in records}),
        "r1_reused": 128, "r2_reused": 6, "r2_fresh_terminal": 122,
        "r2_successful_ensembles_independently_recomputed": output["counts"]["r2_complete"],
        "gallery_results_sha256": sha(HERE / "gallery_results.json"), "counts": output["counts"],
    })
    print(json.dumps({"export": str(HERE / "gallery_results.json"),
                      "sha256": sha(HERE / "gallery_results.json"), **output["counts"]}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "run", "export"])
    args = parser.parse_args()
    {"prepare": prepare, "run": run, "export": export}[args.command]()


if __name__ == "__main__":
    main()
