#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""Validate the V4 gallery contract without generation or publication calls."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


EVAL_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = EVAL_ROOT.parents[1]
TEMPLATE_DIR = EVAL_ROOT / "gallery"
BUILD_SCRIPT = EVAL_ROOT / "build_gallery.py"
DEFAULT_RUN_DIR = PROJECT_ROOT / "local_data/generation_runs/hp_lifestyle_lived_in_v4_eval_20261026"
DEFAULT_REPORT = EVAL_ROOT / "publication/ui_validation.json"
EXPECTED_ENVIRONMENTS = ("Home", "Office", "Education", "Gaming", "Café", "Creative Studio")
EXPECTED_CANDIDATE_HEADERS = (
    "Ranked candidate", "Source and camera", "Score and relationship",
    "Evidence and explanation", "Visible scene and camera", "Selection and complete audit",
)
EXPECTED_GENERATION_HEADERS = (
    "Selected candidate", "Reference", "Source messaging", "Score and evidence",
    "Generated output", "usedPrompt", "Generation debug",
)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


class GalleryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: dict[str, dict[str, Any]] = {}
        self.elements: dict[str, dict[str, str]] = {}
        self.select_options: dict[str, list[str]] = {}
        self._table: str | None = None
        self._section: str | None = None
        self._th_parts: list[str] | None = None
        self._select: str | None = None
        self._option_parts: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        element_id = values.get("id")
        if element_id:
            self.elements[element_id] = values
        if tag == "table":
            classes = values.get("class", "").split()
            self._table = "candidate" if "candidate-table" in classes else "generation" if "generation-table" in classes else None
            if self._table:
                self.tables[self._table] = {"headers": [], "order": [], "tbody_rows": 0}
        elif tag in {"thead", "tbody"} and self._table:
            self._section = tag
            self.tables[self._table]["order"].append(tag)
        elif tag == "th" and self._table and self._section == "thead":
            self._th_parts = []
        elif tag == "tr" and self._table and self._section == "tbody":
            self.tables[self._table]["tbody_rows"] += 1
        elif tag == "select" and element_id:
            self._select = element_id
            self.select_options.setdefault(element_id, [])
        elif tag == "option" and self._select:
            self._option_parts = []

    def handle_data(self, data: str) -> None:
        if self._th_parts is not None:
            self._th_parts.append(data)
        if self._option_parts is not None:
            self._option_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "th" and self._th_parts is not None and self._table:
            self.tables[self._table]["headers"].append(" ".join("".join(self._th_parts).split()))
            self._th_parts = None
        elif tag == "option" and self._option_parts is not None and self._select:
            self.select_options[self._select].append(" ".join("".join(self._option_parts).split()))
            self._option_parts = None
        elif tag == "select":
            self._select = None
        elif tag in {"thead", "tbody"}:
            self._section = None
        elif tag == "table":
            self._table = None


def require(condition: bool, message: str, checks: list[str]) -> None:
    if not condition:
        raise ValueError(message)
    checks.append(message)


def parse_html(raw: str) -> GalleryParser:
    parser = GalleryParser()
    parser.feed(raw)
    parser.close()
    return parser


def validate_static(checks: list[str]) -> None:
    index = (TEMPLATE_DIR / "index.html").read_text(encoding="utf-8")
    javascript = (TEMPLATE_DIR / "main.js").read_text(encoding="utf-8")
    parsed = parse_html(index)
    require(tuple(parsed.tables["candidate"]["headers"]) == EXPECTED_CANDIDATE_HEADERS, "candidate headers match the six rendered cells", checks)
    require(tuple(parsed.tables["generation"]["headers"]) == EXPECTED_GENERATION_HEADERS, "generation headers match the seven rendered cells", checks)
    require(parsed.tables["candidate"]["order"] == ["thead", "tbody"], "candidate headers precede candidate rows", checks)
    require(parsed.tables["generation"]["order"] == ["thead", "tbody"], "generation headers precede generation rows", checks)
    require("active" in parsed.elements["generationTab"].get("class", "").split(), "Generated images (108 selected rows) is the active default tab", checks)
    require("active" not in parsed.elements["candidateTab"].get("class", "").split(), "540-candidate tab is inactive by default", checks)
    require("hidden" not in parsed.elements["generationView"].get("class", "").split(), "generated-image table is visible by default", checks)
    require("hidden" in parsed.elements["candidateView"].get("class", "").split(), "candidate table is hidden by default", checks)
    environment_match = re.search(r'const EXPECTED_ENVIRONMENTS = (\[[^;]+\]);', javascript)
    require(environment_match is not None, "JavaScript declares a fixed native environment taxonomy", checks)
    environments = tuple(json.loads(environment_match.group(1))) if environment_match else ()
    require(environments == EXPECTED_ENVIRONMENTS, "environment filter contains Home, Office, Education, Gaming, Café, and Creative Studio", checks)
    require('addOptions("environmentFilter", EXPECTED_ENVIRONMENTS, false)' in javascript, "environment menu is populated from the fixed six-value taxonomy", checks)
    require('scoreHtml(candidate, true)' in javascript, "generated-row explanation is rendered collapsed", checks)
    candidate_function = javascript.split("function candidateRowHtml", 1)[1].split("function referenceHtml", 1)[0]
    generation_function = javascript.split("function generationRowHtml", 1)[1].split("function render()", 1)[0]
    require(candidate_function.count("<td>") == len(EXPECTED_CANDIDATE_HEADERS), "candidate row renders one cell under each header", checks)
    require(generation_function.count("<td>") == len(EXPECTED_GENERATION_HEADERS), "generation row renders one cell under each header", checks)
    require("<details open" not in generation_function, "generated-row source, explanation, usedPrompt, and debug details have no open attribute", checks)
    require('jsonDetails("Complete generation record", result)' in generation_function, "generation debug is behind a collapsed detail", checks)
    require("<summary>View usedPrompt</summary>" in generation_function, "usedPrompt is behind a collapsed detail", checks)
    require('jsonDetails("Full source messaging"' in javascript and 'jsonDetails("Exact runtime input"' in javascript, "source messaging and runtime input are behind collapsed details", checks)
    require('class="output-column">Generated output' in index, "generated output has a dedicated image column header", checks)
    output_function = javascript.split("function outputHtml", 1)[1].split("function generationRowHtml", 1)[0]
    require('result.generated_image' in output_function and '<img loading="lazy"' in output_function, "done rows render the actual generated image in the output column", checks)
    node = shutil.which("node")
    if node:
        result = subprocess.run([node, "--check", str(TEMPLATE_DIR / "main.js")], text=True, capture_output=True, check=False)
        require(result.returncode == 0, f"main.js passes node --check{': ' + result.stderr.strip() if result.returncode else ''}", checks)
    else:
        checks.append("node --check skipped because node is unavailable")


def load_gallery_data(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    prefix = "const V4_DATA = "
    if not raw.startswith(prefix) or not raw.rstrip().endswith(";"):
        raise ValueError(f"Unexpected data.js wrapper: {path}")
    return json.loads(raw[len(prefix):].rstrip()[:-1])


def validate_data(run_dir: Path, final: bool, checks: list[str]) -> dict[str, Any]:
    data = load_gallery_data(run_dir / "gallery/data.js")
    metadata = data["metadata"]
    candidates = data["candidates"]
    rows = data["generation_rows"]
    require(metadata["candidate_count"] == 540 == len(candidates), "gallery data contains exactly 540 candidates", checks)
    require(metadata["selected_count"] == 108 == len(rows), "gallery data contains exactly 108 selected generation rows", checks)
    require(set(metadata["environment_counts"]) == set(EXPECTED_ENVIRONMENTS), "gallery data natively covers all six environments", checks)
    require(set(item["environment"] for item in candidates) == set(EXPECTED_ENVIRONMENTS), "candidate environments use only the native six-value taxonomy", checks)
    require(len({item["candidate_key"] for item in candidates}) == 540, "candidate keys are unique", checks)
    require(len({row["row_id"] for row in rows}) == 108, "generation row IDs are unique", checks)
    require(all(row["candidate_key"] for row in rows), "every generation row resolves a selected candidate key", checks)
    done_rows = [row for row in rows if row["status"] == "done"]
    for row in done_rows:
        image = row["result"]["generated_image"]
        require(bool(image.get("filename") and image.get("native_width") and image.get("native_height")), f"done row {row['row_id']} carries an actual generated-image asset", checks)
    if final:
        require(len(done_rows) == 108, "final gallery has 108 actual generated-image assets", checks)
    return {"candidate_count": len(candidates), "generation_row_count": len(rows), "done_row_count": len(done_rows), "environment_counts": metadata["environment_counts"]}


def browser_binary() -> str | None:
    return next((path for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable") if (path := shutil.which(name))), None)


def validate_browser(run_dir: Path, checks: list[str]) -> dict[str, Any]:
    browser = browser_binary()
    if not browser:
        return {
            "status": "skipped",
            "reason": (
                "no supported Chromium binary is installed; static HTML and serialized data "
                "were validated, and JavaScript contract markers were inspected; the checks "
                "list records whether a standalone JavaScript syntax runtime was available"
            ),
        }
    gallery = run_dir / "gallery"
    index = (gallery / "index.html").read_text(encoding="utf-8")
    index = re.sub(r'\s*<script src="https://auth-stg1[^>]+></script>', "", index)
    index = index.replace('    <script src="./imsauth.js"></script>\n', "")
    index = re.sub(r'\s*<script>document\.addEventListener\("DOMContentLoaded"[^<]+</script>', "", index)
    harness_call = '<script>document.getElementById("loading").classList.add("hidden");document.getElementById("content").classList.remove("hidden");onAuthReady();</script>\n'
    index = index.replace("</body>", harness_call + "</body>")
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".html", prefix=".v4_ui_harness_", dir=gallery, delete=False) as handle:
        handle.write(index)
        harness = Path(handle.name)
    try:
        result = subprocess.run(
            [browser, "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage", "--allow-file-access-from-files", "--dump-dom", harness.as_uri()],
            text=True, capture_output=True, timeout=45, check=False,
        )
    finally:
        harness.unlink(missing_ok=True)
    require(result.returncode == 0, f"headless browser rendered the local gallery{': ' + result.stderr[-500:] if result.returncode else ''}", checks)
    parsed = parse_html(result.stdout)
    require(parsed.tables["generation"]["tbody_rows"] > 0, "headless browser rendered generated-view rows", checks)
    require(parsed.tables["candidate"]["tbody_rows"] == 0, "headless browser retained the generated view as default", checks)
    require(tuple(parsed.select_options["environmentFilter"][1:]) == EXPECTED_ENVIRONMENTS, "headless browser rendered the six native environment options in order", checks)
    return {"status": "passed", "binary": browser, "visible_generation_rows": parsed.tables["generation"]["tbody_rows"]}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--static-only", action="store_true", help="Validate templates before the 540/108 exports exist")
    parser.add_argument("--final", action="store_true", help="Require all 108 actual generated outputs")
    parser.add_argument("--skip-browser", action="store_true")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    if args.static_only and args.final:
        parser.error("--static-only and --final cannot be combined")
    checks: list[str] = []
    report: dict[str, Any] = {"version": "hp-lived-in-v4-ui-validation-v1", "checked_at_utc": utc_now(), "status": "failed", "mode": "static" if args.static_only else "final" if args.final else "progressive"}
    try:
        validate_static(checks)
        if not args.static_only:
            command = [sys.executable, str(BUILD_SCRIPT), "--run-dir", str(args.run_dir.resolve())]
            if args.final:
                command.append("--final")
            built = subprocess.run(command, cwd=PROJECT_ROOT, text=True, capture_output=True, check=False)
            if built.returncode:
                raise ValueError(f"gallery build failed ({built.returncode}): {built.stderr[-2000:]}")
            report["data"] = validate_data(args.run_dir.resolve(), args.final, checks)
            report["browser"] = {"status": "skipped", "reason": "--skip-browser"} if args.skip_browser else validate_browser(args.run_dir.resolve(), checks)
        else:
            report["browser"] = {"status": "skipped", "reason": "serialized data does not exist in static-only mode"}
        report.update({"status": "passed", "checks": checks})
    except Exception as exc:
        report.update({"checks": checks, "error": {"type": type(exc).__name__, "message": str(exc)}})
    if not args.static_only:
        write_json(args.report.resolve(), report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
