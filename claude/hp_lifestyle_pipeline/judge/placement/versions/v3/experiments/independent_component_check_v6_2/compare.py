#!/usr/bin/env python3
"""Mechanically compare names-only assessments with the earlier proposal-aware verifiers."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def classify(component: dict) -> str:
    if component["visibility"] == "unobservable" or component["confidence"] == "low" or component["severity"] is None:
        return "unknown"
    if component["severity"] >= 2:
        return "material"
    return "clear_nonmaterial"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--independent-run", type=Path, required=True)
    parser.add_argument("--development-verifier-run", type=Path, required=True)
    parser.add_argument("--new160-verifier-run", type=Path, required=True)
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    manifest = load(manifest_path)
    generated = datetime.now(timezone.utc).isoformat()
    rows = []
    result_hashes = {"independent": {}, "earlier": {}}
    independent_artifacts = {}
    latencies = []
    attempts = []
    for record in manifest["records"]:
        record_id = record["id"]
        independent_path = args.independent_run.resolve() / record_id / "result.json"
        earlier_root = args.new160_verifier_run.resolve() if record["cohort"].startswith("root_inspected") else args.development_verifier_run.resolve()
        earlier_path = earlier_root / record_id / "result.json"
        independent = load(independent_path)
        earlier = load(earlier_path)
        if independent.get("ok") is not True or earlier.get("ok") is not True:
            raise ValueError(f"{record_id}: comparison requires successful results")
        if independent["proposal_text_codes_severities_prior_verdicts_comments_passed"] is not False:
            raise ValueError(f"{record_id}: independent request contamination flag changed")
        request_path = independent_path.parent / "request.json"
        request = load(request_path)
        if set(request["sent_metadata"]) != {"product_type", "image_stage", "scene_prompt", "requested_component_names"}:
            raise ValueError(f"{record_id}: sent metadata whitelist changed")
        if request["sent_metadata"]["requested_component_names"] != record["requested_component_names"]:
            raise ValueError(f"{record_id}: sent component names changed")
        if set(independent["assessment"]["components"]) != set(record["requested_component_names"]):
            raise ValueError(f"{record_id}: independent component coverage mismatch")
        if set(earlier["assessment"]["components"]) != set(record["requested_component_names"]):
            raise ValueError(f"{record_id}: earlier component coverage mismatch")
        result_hashes["independent"][record_id] = {"path": str(independent_path), "sha256": sha256(independent_path)}
        result_hashes["earlier"][record_id] = {"path": str(earlier_path), "sha256": sha256(earlier_path)}
        independent_artifacts[record_id] = {
            filename: {"path": str(independent_path.parent / filename), "sha256": sha256(independent_path.parent / filename)}
            for filename in ("request.json", "response_schema.json", "system_prompt.md", "response.json", "result.json")
        }
        latencies.append(float(independent["elapsed_seconds"]))
        attempts.extend(independent["attempts"])
        for name in record["requested_component_names"]:
            before = earlier["assessment"]["components"][name]
            after = independent["assessment"]["components"][name]
            before_class, after_class = classify(before), classify(after)
            rows.append({
                "id": record_id,
                "cohort": record["cohort"],
                "evaluation_status": record["evaluation_status"],
                "component": name,
                "earlier": {"class": before_class, **before},
                "independent_names_only": {"class": after_class, **after},
                "direction": f"{before_class}->{after_class}",
                "exact_assessment_match": before == after,
            })
    expected_components = manifest["expected_component_count"]
    if len(rows) != expected_components:
        raise ValueError(f"Expected {expected_components} component comparisons, got {len(rows)}")
    result = {
        "schema_version": "placement-independent-component-comparison-v1",
        "generated_at_utc": generated,
        "comparison_script": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__).resolve())},
        "manifest": {"path": str(manifest_path), "sha256": sha256(manifest_path)},
        "research_status": "development_probe_not_heldout_no_merge_or_promotion_decision",
        "classification_rule": {
            "material": "observed or partial, medium/high confidence, integer severity >=2",
            "clear_nonmaterial": "observed or partial, medium/high confidence, integer severity 0 or 1",
            "unknown": "unobservable, low confidence, or null severity",
        },
        "coverage": {"cases": len(manifest["records"]), "components": len(rows), "missing": 0},
        "earlier_class_counts": dict(Counter(row["earlier"]["class"] for row in rows)),
        "independent_class_counts": dict(Counter(row["independent_names_only"]["class"] for row in rows)),
        "direction_counts": dict(Counter(row["direction"] for row in rows)),
        "exact_assessment_matches": sum(row["exact_assessment_match"] for row in rows),
        "independent_api": {
            "successful_cases": len(manifest["records"]),
            "failed_cases": 0,
            "successful_attempts": sum(attempt.get("status") == "ok" for attempt in attempts),
            "failed_attempts": sum(attempt.get("status") != "ok" for attempt in attempts),
            "retried_cases": sum(len(load(args.independent_run.resolve()/record["id"]/"result.json")["attempts"]) > 1 for record in manifest["records"]),
            "latency_seconds": {"min": min(latencies), "median": statistics.median(latencies), "mean": statistics.fmean(latencies), "max": max(latencies)},
        },
        "source_results": result_hashes,
        "independent_artifacts": independent_artifacts,
        "comparisons": rows,
    }
    output_json = args.independent_run.resolve() / "comparison.json"
    output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Independent names-only component check",
        "",
        f"Generated: `{generated}`",
        "",
        f"Coverage: {len(manifest['records'])} cases and {len(rows)} component assessments; no missing records.",
        "",
        "This is an explicitly inspected development probe. It is not held-out validation and makes no merge or promotion decision.",
        "",
        "## Direction counts",
        "",
    ]
    for direction, count in sorted(result["direction_counts"].items()):
        lines.append(f"- `{direction}`: {count}")
    lines += ["", "## Component comparisons", "", "| Case | Component | Earlier | Names-only | Direction |", "|---|---|---:|---:|---|"]
    for row in rows:
        lines.append(f"| {row['id']} | {row['component']} | {row['earlier']['class']} (s={row['earlier']['severity']}, {row['earlier']['confidence']}) | {row['independent_names_only']['class']} (s={row['independent_names_only']['severity']}, {row['independent_names_only']['confidence']}) | {row['direction']} |")
    output_md = args.independent_run.resolve() / "comparison.md"
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    audit = {
        "schema_version": "placement-independent-component-check-audit-v1",
        "generated_at_utc": generated,
        "comparison_script": result["comparison_script"],
        "manifest": result["manifest"],
        "freeze": {"path": str((Path(__file__).resolve().parent / "freeze.json")), "sha256": sha256(Path(__file__).resolve().parent / "freeze.json")},
        "system_prompt": {"path": str((Path(__file__).resolve().parent / "system_prompt.md")), "sha256": sha256(Path(__file__).resolve().parent / "system_prompt.md")},
        "coverage": result["coverage"],
        "independent_artifacts": independent_artifacts,
        "earlier_result_sources": result_hashes["earlier"],
    }
    output_audit = args.independent_run.resolve() / "audit.json"
    output_audit.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"comparison": str(output_json), "report": str(output_md), "audit": str(output_audit), "summary": {key: result[key] for key in ("coverage", "earlier_class_counts", "independent_class_counts", "direction_counts", "exact_assessment_matches", "independent_api")}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
