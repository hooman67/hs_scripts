#!/usr/bin/env python3
"""Evaluate frozen V4.3.1 canary + remaining five against withheld requirements."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scoring import validate_result

ROOT = Path(__file__).resolve().parent
CANARY_ID = "elitebook__laptop_FrontLeftMedium__p1"
CANARY_RESULT = ROOT / "runs/quality-canary-v1-gpt55/result/result.json"
BASELINE = ROOT.parent / "v4_1/data/development_15_v4_1_anchored_partial_gate_v1.json"


def result_path(run: Path, record_id: str) -> Path:
    return CANARY_RESULT if record_id == CANARY_ID else run / record_id / "result.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--remaining-run-dir", required=True)
    parser.add_argument("--output-stem", default="combined_six_evaluation_v1")
    args = parser.parse_args()
    run = Path(args.remaining_run_dir)
    expectations = json.loads((ROOT / "data/gate_6_expectations_withheld.json").read_text())["records"]
    baseline_rows = {row["record_id"]: row for row in json.loads(BASELINE.read_text())["rows"]}
    rows = []

    for expected in expectations:
        record_id = expected["record_id"]
        path = result_path(run, record_id)
        requirement = expected["v4_3_1_gate_requirement"]
        row = {
            "record_id": record_id,
            "result_source": "frozen_quality_canary" if record_id == CANARY_ID else "remaining_five_run",
            "result_path": str(path.resolve()),
            "result_exists": path.is_file(),
            "valid": False,
            "expected_verdict": requirement["verdict"],
            "required_issues": requirement["issues"],
            "forbidden_issues": requirement["forbidden"],
        }
        if path.is_file():
            result = json.loads(path.read_text())
            try:
                validate_result(result)
                row["valid"] = True
            except Exception as exc:
                row["validation_error"] = str(exc)
            derived = result.get("derived") or {}
            actual = set(derived.get("owned_issue_codes", []))
            row.update(
                status=result.get("status"),
                attempts=result.get("raw_attempts"),
                score=derived.get("score"),
                actual_verdict=derived.get("verdict"),
                verdict_match=requirement["verdict"] is None or derived.get("verdict") == requirement["verdict"],
                detected_required=sorted(actual.intersection(requirement["issues"])),
                all_required_detected=set(requirement["issues"]).issubset(actual),
                detected_forbidden=sorted(actual.intersection(requirement["forbidden"])),
                actual_issues=sorted(actual),
                general_artifact_warnings=(result.get("assessment") or {}).get("general_artifact_warnings", []),
            )
        baseline = baseline_rows.get(record_id)
        row["v4_1_baseline"] = None if not baseline or baseline.get("status") != "ok" else {
            "verdict": baseline.get("predicted_verdict"),
            "issues": baseline.get("observed_issue_codes", []),
            "verdict_match": baseline.get("verdict_match"),
            "issue_any_match": baseline.get("issue_any_match"),
        }
        rows.append(row)

    valid = sum(row["valid"] and row.get("status") == "ok" for row in rows)
    required_total = sum(len(row["required_issues"]) for row in rows)
    required_detected = sum(len(row.get("detected_required", [])) for row in rows)
    labeled = [row for row in rows if row["expected_verdict"] is not None]
    verdict_correct = sum(bool(row.get("verdict_match")) for row in labeled)
    forbidden_cases = sum(bool(row.get("detected_forbidden")) for row in rows)
    baseline_completed = [row for row in rows if row["v4_1_baseline"] is not None]
    baseline_labeled = [row for row in baseline_completed if row["expected_verdict"] is not None]
    baseline_issue_cases = [row for row in baseline_completed if row["required_issues"]]
    summary = {
        "schema_version": "hp-placement-v4.3.1-combined-six-evaluation-v1",
        "valid_ok": valid,
        "case_count": len(rows),
        "required_issue_codes_detected": required_detected,
        "required_issue_codes_total": required_total,
        "labeled_verdict_correct": verdict_correct,
        "labeled_verdict_total": len(labeled),
        "forbidden_issue_case_count": forbidden_cases,
        "strict_gate_pass": valid == 6 and required_detected == required_total and verdict_correct == len(labeled) and forbidden_cases == 0,
        "v4_1_same_case_completed_count": len(baseline_completed),
        "v4_1_labeled_verdict_correct": sum(bool(row["v4_1_baseline"]["verdict_match"]) for row in baseline_labeled),
        "v4_1_labeled_verdict_total": len(baseline_labeled),
        "v4_1_issue_any_matches": sum(bool(row["v4_1_baseline"]["issue_any_match"]) for row in baseline_issue_cases),
        "v4_1_issue_cases_total": len(baseline_issue_cases),
        "rows": rows,
    }
    output = ROOT / "data" / f"{args.output_stem}.json"
    output.write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# V4.3.1 combined six-case gate",
        "",
        f"- Valid: {valid}/6",
        f"- Required issue codes: {required_detected}/{required_total}",
        f"- Labeled verdicts: {verdict_correct}/{len(labeled)}",
        f"- Forbidden issue cases: {forbidden_cases}",
        f"- Strict gate: {'PASS' if summary['strict_gate_pass'] else 'FAIL'}",
        f"- V4.1 completed same cases: {len(baseline_completed)}/6",
        f"- V4.1 labeled verdicts on completed same cases: {summary['v4_1_labeled_verdict_correct']}/{summary['v4_1_labeled_verdict_total']}",
        f"- V4.1 expected-issue matches on completed same issue cases: {summary['v4_1_issue_any_matches']}/{summary['v4_1_issue_cases_total']}",
        "",
        "| Record | Source | Verdict | Issues | Required | Forbidden detected | V4.1 |",
        "|---|---|---:|---|---|---|---|",
    ]
    for row in rows:
        baseline = row["v4_1_baseline"]
        baseline_text = "missing" if baseline is None else f"{baseline['verdict']} / {', '.join(baseline['issues']) or 'none'}"
        lines.append(
            f"| `{row['record_id']}` | {row['result_source']} | {row.get('actual_verdict')} | "
            f"{', '.join(row.get('actual_issues', [])) or 'none'} | {', '.join(row['required_issues']) or 'none'} | "
            f"{', '.join(row.get('detected_forbidden', [])) or 'none'} | {baseline_text} |"
        )
    output.with_suffix(".md").write_text("\n".join(lines) + "\n")
    print(json.dumps({key: value for key, value in summary.items() if key != "rows"}, indent=2))


if __name__ == "__main__":
    main()
