"""Verify public-URL integration, provenance and preservation; make no model calls."""
from __future__ import annotations

import ast
import difflib
import hashlib
import json
import shutil
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R1 = ROOT.parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def main():
    comparison_path = ROOT / "evaluation/comparison.json"
    comparison = json.loads(comparison_path.read_text())
    calibration = comparison["calibration"]
    assert calibration["status"] == "calibration_gate_not_met"
    assert calibration["all_stated_checks_matched"] is False
    assert calibration["full128_started"] is False
    assert len(calibration["items"]) == 6 and all(item["ok"] for item in calibration["items"])
    records = comparison["records"]
    assert len(records) == 128
    assert sum(row["v3_1"]["status"] == "complete" for row in records) == 6
    unrun = [row for row in records if row["v3_1"]["status"] == "not_run_gate_blocked"]
    assert len(unrun) == 122
    assert all(row["v3_1"][key] is None for row in unrun
               for key in ("verdict", "score", "confidence", "components"))
    assert all(row["verdict_changed"] is None and row["changed_dimensions"] is None for row in unrun)
    for path in ROOT.glob("*.py"):
        ast.parse(path.read_text(), filename=str(path))
    for freeze_name in ("protocol_freeze.json", "calibration_execution_freeze.json"):
        freeze = json.loads((ROOT / freeze_name).read_text())
        assert all(sha(row["path"]) == row["sha256"] for row in freeze["files"])
    before = json.loads((ROOT / "r1_integrity_before.json").read_text())
    assert sha(R1 / "ARTIFACT_MANIFEST.json") == before["manifest_sha256"]
    original_manifest = json.loads((R1 / "ARTIFACT_MANIFEST.json").read_text())
    assert all(sha(row["path"]) == row["sha256"] for row in original_manifest["files"])

    class Parser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.sections, self.images, self.judges = [], [], 0

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "section":
                self.sections.append(attrs["id"])
            if tag == "img":
                self.images.append(attrs)
            if tag == "article" and attrs.get("class") == "judge":
                self.judges += 1

    document = (ROOT / "evaluation/comparison.html").read_text()
    parser = Parser()
    parser.feed(document)
    assert parser.sections == [row["id"] for row in records]
    assert parser.judges == 256 and len(parser.images) == 256
    expected_urls = [row[key]["url"] for row in records for key in ("generated_image", "twin_image")]
    assert [image["src"] for image in parser.images] == expected_urls
    assert all(image["src"] == image["data-source-url"] for image in parser.images)
    assert all(url.startswith("https://foundry-aws-corp.adobe.io/asset/") for url in expected_urls)
    assert "CALIBRATION GATE NOT MET" in document and "DO NOT PROMOTE" in document
    assert "Overall verdict / score / confidence" in document
    assert "Placement / product-table alignment" in document
    assert "Table/chair geometry + scale/perspective" in document
    sources = {row[key]["local_path"]: row[key]["sha256"]
               for row in records for key in ("generated_image", "twin_image")}
    assert len(sources) == 160 and all(sha(path) == digest for path, digest in sources.items())
    validation = {
        "validated_utc": datetime.now(timezone.utc).isoformat(),
        "sections": 128, "judge_panels": 256, "image_elements": 256,
        "all_image_src_are_exact_full_original_urls": True,
        "local_image_fixture_dependency_in_html": False,
        "overall_and_criterion_outcomes_separate": True,
        "unpromoted_banner_present": True, "local_source_objects_hash_verified": 160,
        "v3_baseline_reused_complete": 128, "r2_complete": 6,
        "r2_not_run_gate_blocked": 122, "unrun_scores_are_null": True,
        "original_r1_artifacts_unchanged": len(original_manifest["files"]),
        "new_python_syntax_valid": True, "protocol_and_execution_freezes_unchanged": True,
    }
    write(ROOT / "evaluation/report_validation.json", validation)

    (ROOT / "deltas").mkdir(exist_ok=True)
    pairs = [(R1 / "run_judge.py", ROOT / "run_judge.py")]
    pairs += [(R1 / "prompts" / f"{stage}.md", ROOT / "prompts" / f"{stage}.md")
              for stage in ("baseline", "compact", "proposal", "independent")]
    transforms = []
    for source, target in pairs:
        filename = "runtime.diff" if target.suffix == ".py" else f"{target.stem}.diff"
        diff_path = ROOT / "deltas" / filename
        diff_path.write_text("".join(difflib.unified_diff(
            source.read_text().splitlines(keepends=True),
            target.read_text().splitlines(keepends=True), fromfile=str(source), tofile=str(target))))
        transforms.append({"source_path": str(source), "source_sha256": sha(source),
                           "output_path": str(target), "output_sha256": sha(target),
                           "diff_path": str(diff_path), "diff_sha256": sha(diff_path)})
    source_text, output_text = (R1 / "run_judge.py").read_text(), (ROOT / "run_judge.py").read_text()
    functions = []
    for text in (source_text, output_text):
        functions.append({node.name: ast.get_source_segment(text, node)
                          for node in ast.parse(text).body if isinstance(node, ast.FunctionDef)})
    unchanged = [name for name in functions[0] if functions[0][name] == functions[1][name]]
    assert set(functions[0]) - set(unchanged) == {"call_stage"}
    for name in ("judge", "aggregate_stages", "trigger_names"):
        assert name in unchanged
    astra_metadata = json.loads((ROOT / "astra/metadata.json").read_text())
    provenance = {
        "lineage": "Selected frozen V3 consensus -> r1 C-Tech semantics -> sole r2 evidence-envelope amendment.",
        "v4_runtime_or_rules_imported": False, "semantic_revisions": 1,
        "astra_model_returned": astra_metadata["model_returned"], "astra_metadata": astra_metadata,
        "judging_models_returned": comparison["versions"]["v3_1"]["actual_models_returned"],
        "unchanged_runtime_function_bodies": unchanged,
        "scoring_path": str(R1 / "scoring.py"), "scoring_sha256": sha(R1 / "scoring.py"),
        "observation_schema_path": str(R1 / "observation_schema.json"),
        "observation_schema_sha256": sha(R1 / "observation_schema.json"),
        "outer_envelope_version": "placement-evidence-envelope-v3.1-r2",
        "protocol_freeze_sha256": sha(ROOT / "protocol_freeze.json"),
        "transforms": transforms,
        "calibration_labels_passed_to_model": False, "semantic_resamples": 0,
        "raw_output_repair": False,
    }
    write(ROOT / "implementation_provenance.json", provenance)
    release = {
        "as_of_utc": datetime.now(timezone.utc).isoformat(),
        "candidate": "V3.1 r2", "status": "calibration_gate_not_met", "promoted": False,
        "approved_final_v3_1_replacement": None, "revision_budget_exhausted": True,
        "full128_r2_started": False, "new_generation_study_judged": False,
        "anchors": [row for row in calibration["items"] if row["role"] == "ctech_anchor"],
        "unmet_criteria": [{"id": row["id"], "dimension": name}
                          for row in calibration["items"] for name, matched in row["checks"].items()
                          if not matched],
        "r1_preserved": before, "root_docs_edited": False, "independently_published": False,
        "next_step": "Stop; source-label adjudication and a distinct approach need fresh authorization.",
    }
    write(ROOT / "release_status.json", release)
    sample = next(row for row in records if row["v3_1"]["ok"])
    integration = {
        "schema_version": comparison["schema_version"],
        "top_level_keys": list(comparison), "record_keys": list(sample),
        "complete_r2_judge_keys": list(sample["v3_1"]),
        "component_dimensions": list(sample["v3_1"]["components"]),
        "component_keys": list(next(iter(sample["v3_1"]["components"].values()))),
        "r2_status_values": ["complete", "error", "not_run_gate_blocked"],
        "null_rule": "Unrun r2 verdict/score/confidence/components and change flags are null; never use r1 as fallback.",
        "candidate_promoted": False,
        "integration": "Copy HTML and JSON bytes unchanged. All img src values already use full original Foundry URLs.",
        "image_availability": "Six anonymous probes ConnectTimeout; no public/browser-access claim.",
        "files": [{"path": str(ROOT / name), "sha256": sha(ROOT / name)}
                  for name in ("evaluation/comparison.html", "evaluation/comparison.json",
                               "evaluation/evidence_audit.json", "evaluation/report_validation.json",
                               "astra/input.md", "astra/config.json", "astra/response.json",
                               "astra/output.md", "astra/metadata.json", "implementation_provenance.json",
                               "release_status.json", "SUMMARY.md")],
    }
    write(ROOT / "INTEGRATION.json", integration)
    work = ROOT / ".work"
    if work.exists():
        shutil.rmtree(work)
    files = [path for path in sorted(ROOT.rglob("*"))
             if path.is_file() and path.name != "ARTIFACT_MANIFEST.json"]
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(), "scope": str(ROOT),
        "self_excluded": True, "r1_artifacts_preserved": len(original_manifest["files"]),
        "file_count": len(files), "total_bytes_excluding_manifest": sum(p.stat().st_size for p in files),
        "files": [{"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size} for path in files],
    }
    write(ROOT / "ARTIFACT_MANIFEST.json", manifest)
    print(json.dumps({"release": release["status"], "unmet_criteria": release["unmet_criteria"],
                      "validation": validation, "new_file_count": len(files),
                      "new_bytes_excluding_manifest": manifest["total_bytes_excluding_manifest"],
                      "integration_files": integration["files"][:2]}))


if __name__ == "__main__":
    main()
