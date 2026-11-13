"""Offline evidence/known-error audit and parent-ready export; never resamples."""
from __future__ import annotations

import ast
import importlib.metadata
import json
import shutil
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

import external_driver as driver

HERE = Path(__file__).resolve().parent


def known_errors(row):
    folder = HERE / "runs/r2" / row["id"]
    runner = driver.runners()["r2"]
    details = []
    for request_path in sorted(folder.glob("*/request.json")):
        request = driver.read(request_path)
        role = request_path.parent
        saved_path, raw_path = role / "result.json", role / "response.json"
        detail = {"stage": role.name, "request_path": str(request_path),
                  "request_sha256": driver.sha(request_path)}
        if saved_path.exists():
            saved = driver.read(saved_path)
            detail.update({key: saved.get(key) for key in ("ok", "error_type", "status_code")})
        else:
            detail["ok"] = False
            detail["error_type"] = "ambiguous_started_role"
        if raw_path.exists():
            raw = driver.read(raw_path)
            choice = raw["choices"][0]
            detail.update(response_path=str(raw_path), response_sha256=driver.sha(raw_path),
                          model_returned=raw.get("model"), finish_reason=choice["finish_reason"])
            names = request["requested_components"]
            payload_schema = runner.component_schema(names) if names else runner.SCORING.OBSERVATION_SCHEMA
            try:
                envelope = json.loads(choice["message"]["content"])
                observation = runner.TRACE.validate(envelope, payload_schema)
                if names:
                    runner.validate_components(observation, payload_schema)
                else:
                    runner.validate_new_observation(observation)
            except Exception as exc:
                detail["validation_error_type"] = type(exc).__name__
                detail["validation_detail"] = (
                    f"Schema keyword {exc.validator} at {list(exc.absolute_path)}"
                    if hasattr(exc, "validator") else str(exc).splitlines()[0])
        details.append(detail)
    return details


def main():
    # This recomputes only saved results; it never invokes judge()/the provider.
    driver.export()
    path = HERE / "gallery_results.json"
    output = driver.read(path)
    output["source_object"] = driver.read(HERE / "source_verification.json")["source_object"]
    output["evaluation_scope"] = {
        "source_image_stage": "e2e_comparison_output",
        "runtime_stage_adapter": "scene_generation literal for unchanged V3 validator; out-of-domain diagnostic.",
        "prior_calibration_gate_override": "This original128 evaluation only; no promotion or rubric change.",
        "source_verification_path": str(HERE / "source_verification.json"),
        "source_verification_sha256": driver.sha(HERE / "source_verification.json"),
    }
    errors = []
    for row in output["records"]:
        if row["r2"]["status"] == "error":
            detail = known_errors(row)
            row["r2"]["error"]["known_stage_errors"] = detail
            errors.append({"source_row_id": row["source_row_id"], "variant": row["variant"],
                           "generated_image_url": row["generated_image"]["url"],
                           **row["r2"]["error"]})
    output["errors"] = errors
    records = output["records"]
    assert len(records) == 128 and len({r["generated_image"]["url"] for r in records}) == 128
    assert len({r["source_row_id"] for r in records}) == 32
    assert all(r["r1"]["status"] == "complete" and r["r1"]["reused"] for r in records)
    assert sum(r["r2"]["reused"] for r in records) == 6
    assert sum(not r["r2"]["reused"] for r in records) == 122
    assert all(r[v]["status"] in {"complete", "error"} for r in records for v in ("r1", "r2"))
    assert all(r[v]["verdict"] is r[v]["score"] is r[v]["short_reason"] is None
               for r in records for v in ("r1", "r2") if r[v]["status"] == "error")
    for row in records:
        for version in ("r1", "r2"):
            result = row[version]
            if result["status"] == "complete":
                normalized = " ".join(result["short_reason_source"]["original_text"].split())
                brief = result["short_reason"]
                assert brief == normalized or (brief.endswith("…") and normalized.startswith(brief[:-1]))
    Draft202012Validator(driver.read(HERE / "gallery_results.schema.json")).validate(output)
    driver.write(path, output)
    driver.write(HERE / "errors.json", {"count": len(errors), "items": errors})
    new_requests = list((HERE / "runs/r2").glob("*/*/request.json"))
    new_raw = list((HERE / "runs/r2").glob("*/*/response.json"))
    new_role_results = [driver.read(p) for p in (HERE / "runs/r2").glob("*/*/result.json")]
    reused = driver.read(HERE / "reused_results.json")
    models = sorted({driver.read(p).get("model") for p in new_raw})
    validation = {
        "validated_utc": driver.now(), "schema_valid": True, "records": 128,
        "source_row_count": 32, "unique_generated_image_urls": 128,
        "join_by_exact_original_generated_image_url": True,
        "all_display_reasons_are_saved_output_excerpts": True,
        "error_values_null_without_fallback": True,
        "counts": output["counts"], "known_errors": len(errors),
        "r1_reused_raw_responses": sum(len(r["r1"]["raw_calls"]) for r in reused),
        "r2_reused_raw_responses": sum(len(r["r2"]["raw_calls"]) for r in reused if r["r2"]),
        "new_r2_scheduled_roles": len(new_requests), "new_r2_raw_responses": len(new_raw),
        "new_r2_validated_role_responses": sum(r["ok"] for r in new_role_results),
        "new_r2_failed_roles": sum(not r["ok"] for r in new_role_results),
        "new_r2_models_returned": models, "semantic_resamples": 0,
        "original_stored_judge_row_replaced": False,
        "r1_or_fresh_v3_rerun": False, "both_candidates_remain_unpromoted": True,
        "gallery_results_sha256": driver.sha(path),
        "original_artifacts_preservation_check": "Every protected hash checked by offline export.",
    }
    driver.write(HERE / "export_validation.json", validation)
    driver.write(HERE / "runtime_packages.json", {
        "python": sys.version, "packages": {name: importlib.metadata.version(name) for name in
                                          ("foundry-aws-gateway", "openai", "jsonschema", "beautifulsoup4")},
    })
    integration = driver.read(HERE / "INTEGRATION.json")
    integration.update(ready=True, completed_utc=driver.now(), counts=output["counts"],
                       gallery_results_sha256=driver.sha(path),
                       errors_path=str(HERE / "errors.json"),
                       validation_path=str(HERE / "export_validation.json"),
                       finalization_command=(
                           "Run finalize_evaluation.py with the same requirements environment; "
                           "offline only, no model calls."))
    driver.write(HERE / "INTEGRATION.json", integration)
    for source in HERE.glob("*.py"):
        ast.parse(source.read_text(), filename=str(source))
    work = HERE / ".work"
    if work.exists():
        shutil.rmtree(work)
    files = [p for p in sorted(HERE.rglob("*")) if p.is_file() and p.name != "ARTIFACT_MANIFEST.json"]
    driver.write(HERE / "ARTIFACT_MANIFEST.json", {
        "created_utc": driver.now(), "scope": str(HERE), "self_excluded": True,
        "file_count": len(files), "total_bytes": sum(p.stat().st_size for p in files),
        "files": [{"path": str(p), "sha256": driver.sha(p), "bytes": p.stat().st_size} for p in files],
    })
    print(json.dumps({"ready": True, "export": str(path), "sha256": driver.sha(path), **validation}))


if __name__ == "__main__":
    main()
