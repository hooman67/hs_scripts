#!/usr/bin/env python3
"""Compare a completed V4 judge run with frozen development expectations."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-stem", required=True)
    args = parser.parse_args()

    labels = {
        case["id"]: case
        for case in json.loads((ROOT / "evidence/calibration_cases.json").read_text())["cases"]
    }
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    records = manifest["records"]
    rows = []
    for record in records:
        case_id = record["id"]
        expected = labels[case_id]
        result_path = ROOT / "runs" / args.run_name / case_id / "result.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        judgment = result["judgment"]
        observation = judgment["observation"]
        findings = observation.get("defect_inventory", [])
        rows.append(
            {
                "id": case_id,
                "expected": expected["expected_v4_verdict"],
                "v3": expected["v3_verdict"],
                "actual": judgment["verdict"],
                "score": judgment["natural_placement_score"],
                "matched": expected["expected_v4_verdict"] == judgment["verdict"],
                "finding_types": [finding["defect_type"] for finding in findings],
                "finding_evidence": [finding["evidence"] for finding in findings],
                "ctech_comment": expected["ctech_comment"],
            }
        )

    matrix = Counter((row["expected"], row["actual"]) for row in rows)
    report = {
        "run_name": args.run_name,
        "case_count": len(rows),
        "agreement": sum(row["matched"] for row in rows),
        "agreement_rate": round(sum(row["matched"] for row in rows) / len(rows), 4),
        "v3_agreement_on_same_cases": sum(row["expected"] == row["v3"] for row in rows),
        "confusion": [
            {"expected": expected, "actual": actual, "count": count}
            for (expected, actual), count in sorted(matrix.items())
        ],
        "rows": rows,
    }
    json_path = ROOT / "evidence" / f"{args.output_stem}.json"
    md_path = ROOT / "evidence" / f"{args.output_stem}.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# {args.run_name} calibration report",
        "",
        f"- Agreement: {report['agreement']}/{report['case_count']} ({report['agreement_rate']:.1%})",
        f"- V3 agreement on the same cases: {report['v3_agreement_on_same_cases']}/{report['case_count']}",
        "- These are development checks, not an accuracy estimate.",
        "",
        "| ID | Expected | Actual | Score | Findings |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in rows:
        findings = "; ".join(row["finding_types"]) or "none"
        lines.append(
            f"| {row['id']} | {row['expected']} | {row['actual']} | {row['score']} | {findings} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_path), "markdown": str(md_path), **{k: report[k] for k in ("agreement", "case_count", "agreement_rate")}}, indent=2))


if __name__ == "__main__":
    main()
