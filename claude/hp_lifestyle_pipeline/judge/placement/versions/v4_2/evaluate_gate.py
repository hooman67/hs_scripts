#!/usr/bin/env python3
"""Evaluate the frozen six-case gate without exposing expectations at runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scoring import validate_result

ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output-stem", default="gate_6_evaluation_v1")
    args = parser.parse_args()
    run = Path(args.run_dir)
    expectations = json.loads((ROOT / "data" / "gate_6_expectations_withheld.json").read_text())["records"]
    rows = []
    for expected in expectations:
        record_id = expected["record_id"]
        path = run / record_id / "result.json"
        row = {"record_id": record_id, "result_exists": path.is_file(), "valid": False}
        if path.is_file():
            result = json.loads(path.read_text())
            try:
                validate_result(result); row["valid"] = True
            except Exception as exc:
                row["validation_error"] = str(exc)
            derived = result.get("derived") or {}
            required = expected["v4_2_gate_requirement"]
            actual_issues = set(derived.get("owned_issue_codes", []))
            row.update({
                "status": result.get("status"), "attempts": result.get("raw_attempts"),
                "expected_verdict": required["verdict"], "actual_verdict": derived.get("verdict"),
                "verdict_match": required["verdict"] is None or derived.get("verdict") == required["verdict"],
                "required_issues": required["issues"], "detected_required": sorted(actual_issues.intersection(required["issues"])),
                "all_required_detected": set(required["issues"]).issubset(actual_issues),
                "forbidden_issues": required["forbidden"], "detected_forbidden": sorted(actual_issues.intersection(required["forbidden"])),
                "actual_issues": sorted(actual_issues),
            })
        rows.append(row)
    valid = sum(r["valid"] and r.get("status") == "ok" for r in rows)
    required_total = sum(len(r.get("required_issues", [])) for r in rows)
    required_detected = sum(len(r.get("detected_required", [])) for r in rows)
    labeled = [r for r in rows if r.get("expected_verdict") is not None]
    verdict_correct = sum(bool(r.get("verdict_match")) for r in labeled)
    false_positive_blocks = sum(bool(r.get("detected_forbidden")) for r in rows)
    summary = {
        "valid_ok": valid, "case_count": len(rows),
        "required_issue_codes_detected": required_detected, "required_issue_codes_total": required_total,
        "labeled_verdict_correct": verdict_correct, "labeled_verdict_total": len(labeled),
        "forbidden_issue_case_count": false_positive_blocks,
        "strict_astra_gate_pass": valid == 6 and required_detected == required_total and verdict_correct == len(labeled) and false_positive_blocks == 0,
        "rows": rows,
    }
    out = ROOT / "data" / f"{args.output_stem}.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    lines = ["# V4.2 six-case gate", "", f"- Valid: {valid}/6", f"- Required issue codes: {required_detected}/{required_total}", f"- Labeled verdicts: {verdict_correct}/{len(labeled)}", f"- Forbidden issue cases: {false_positive_blocks}", f"- Strict gate: {'PASS' if summary['strict_astra_gate_pass'] else 'FAIL'}", "", "| Record | Verdict | Issues | Required | Forbidden |", "|---|---:|---|---|---|"]
    for r in rows:
        lines.append(f"| `{r['record_id']}` | {r.get('actual_verdict')} | {', '.join(r.get('actual_issues', []))} | {', '.join(r.get('required_issues', []))} | {', '.join(r.get('detected_forbidden', []))} |")
    out.with_suffix(".md").write_text("\n".join(lines) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
