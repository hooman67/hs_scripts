#!/usr/bin/env python3
"""Build the generated-output gallery while preserving the input eval layout."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
EVAL_ROOT = PROJECT_ROOT / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1"
INPUT_DATA_JS = EVAL_ROOT / "gallery/data.js"
INPUT_IMS_AUTH = EVAL_ROOT / "gallery/imsauth.js"
INPUT_STYLE = EVAL_ROOT / "gallery/style.css"
TEMPLATE_ROOT = Path(__file__).resolve().parent


def load_input_data() -> dict[str, Any]:
    text = INPUT_DATA_JS.read_text(encoding="utf-8")
    match = re.fullmatch(r"const EVAL_DATA = (.*);\n?", text, re.S)
    if not match:
        raise ValueError(f"Could not parse {INPUT_DATA_JS}")
    return json.loads(match.group(1))


def load_records(run_dir: Path) -> dict[str, dict[str, Any]]:
    records = {}
    for path in sorted((run_dir / "records").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        records[record["row_id"]] = record
    return records


def gallery_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": record.get("status", "failed"),
        "job_id": record.get("job_id", ""),
        "attempt": record.get("attempt"),
        "request_payload": record.get("request_payload") or {},
        "total_latency_ms": record.get("total_latency_ms"),
        "output_image_id": record.get("output_image_id", ""),
        "output_image_filename": record.get("output_image_filename", ""),
        "output_seed": record.get("output_seed"),
        "debugData": record.get("debugData") or {},
        "error": record.get("error", ""),
        "completed_at_utc": record.get("completed_at_utc", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    data = load_input_data()
    records = load_records(args.run_dir)
    missing = [row["row_id"] for row in data["rows"] if row["row_id"] not in records]
    failed = [row_id for row_id, record in records.items() if record.get("status") != "done"]
    if (missing or failed) and not args.allow_partial:
        raise SystemExit(
            f"Generation is incomplete: {len(missing)} missing, {len(failed)} failed. "
            "Use --allow-partial only for an intentional preview."
        )

    for record in records.values():
        if record.get("status") == "done":
            image = args.run_dir / "images" / record["output_image_filename"]
            if not image.is_file():
                raise FileNotFoundError(image)

    summary_path = args.run_dir / "summary.json"
    summary = json.loads(summary_path.read_text()) if summary_path.exists() else {}
    data["generation"] = {
        "metadata": {
            **summary,
            "title": "HP Lifestyle Prompt × Digital Twin Generation Eval v1",
            "s3_prefix": "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/generated_v1",
        },
        "results": {
            row_id: gallery_record(record)
            for row_id, record in sorted(records.items())
        },
    }

    gallery_dir = args.run_dir / "gallery"
    gallery_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(INPUT_IMS_AUTH, gallery_dir / "imsauth.js")
    shutil.copy2(TEMPLATE_ROOT / "output_index.html", gallery_dir / "index.html")
    shutil.copy2(TEMPLATE_ROOT / "output_main.js", gallery_dir / "main.js")
    style = INPUT_STYLE.read_text(encoding="utf-8")
    style = style.replace("min-width: 1250px;", "min-width: 2400px;")
    style = re.sub(
        r"\.prompt-column \{ width: 31%; \}\n"
        r"\.twin-column \{ width: 25%; \}\n"
        r"\.source-column \{ width: 22%; \}\n"
        r"\.explanation-column \{ width: 22%; \}",
        ".prompt-column { width: 23%; }\n"
        ".twin-column { width: 18%; }\n"
        ".source-column { width: 12%; }\n"
        ".explanation-column { width: 12%; }\n"
        ".output-column { width: 18%; }\n"
        ".rewrite-column { width: 8.5%; }\n"
        ".debug-column { width: 8.5%; }",
        style,
    )
    style += """

/* Generated-output columns */
.output-cell .image-button { background: #111; }
.output-cell .image-button img { background: #111; }
.output-meta {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    margin-top: 8px;
    color: #858585;
    font-size: 0.7rem;
}
.status-pill {
    display: inline-flex;
    padding: 3px 8px;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 650;
}
.status-pill.done { background: #173a27; color: #96e7b4; }
.status-pill.failed { background: #4a1d1d; color: #ffaaa3; }
.status-pill.missing { background: #3b3318; color: #efd478; }
.generation-pre { max-height: 650px; }
.failure-message {
    padding: 12px;
    border: 1px solid #5a2a2a;
    border-radius: 6px;
    background: #231111;
    color: #ffaaa3;
    font-size: 0.78rem;
    overflow-wrap: anywhere;
}
"""
    (gallery_dir / "style.css").write_text(style, encoding="utf-8")
    (gallery_dir / "data.js").write_text(
        "const EVAL_DATA = "
        + json.dumps(data, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    (args.run_dir / "results.json").write_text(
        json.dumps(
            {
                "summary": summary,
                "records": [records[row["row_id"]] for row in data["rows"]],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "rows": len(data["rows"]),
                "records": len(records),
                "done": sum(r.get("status") == "done" for r in records.values()),
                "failed": len(failed),
                "missing": len(missing),
                "gallery": str(gallery_dir / "index.html"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
