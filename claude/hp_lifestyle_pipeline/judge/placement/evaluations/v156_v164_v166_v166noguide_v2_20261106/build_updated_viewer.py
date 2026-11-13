#!/usr/bin/env python3
"""Add validated natural-placement V3 results to the existing static viewer."""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]
MANIFEST = HERE / "manifest.json"
ORIGINAL = HERE / "source/viewer.original.html"
BUILT = HERE / "built"
CONSENSUS = (
    PROJECT
    / "judge/placement/versions/v3/experiments/consensus_policy/runs/"
    "v156-v164-v166-v166noguide-v2-consensus-v1"
)
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = (
    "hp-data-artifacts/hp-3p-gpt25/"
    "hp16-v6prompt-v156-vs-v164-vs-v166-vs-v166noguide-v2-e2e32-"
    "20261106T181903Z"
)
GATEWAY = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}"
LABEL_SLUGS = {
    "V15.6": "v15_6",
    "V16.4": "v16_4",
    "V16.6": "v16_6",
    "V16.6 no geometry": "v16_6_no_geometry",
}
COMPONENT_LABELS = {
    "support_scenario": "Support and scenario",
    "access_usability": "Access and usability",
    "orientation_alignment": "Orientation and alignment",
    "scale_perspective": "Scale and perspective",
    "contact_integration": "Contact and integration",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path):
    require(path.is_file(), f"missing JSON: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def result_map(expected_ids: set[str]) -> dict[str, dict]:
    require(CONSENSUS.is_dir(), f"consensus run missing: {CONSENSUS}")
    paths = sorted(CONSENSUS.glob("*/result.json"))
    results = {path.parent.name: load_json(path) for path in paths}
    require(set(results) == expected_ids, "consensus IDs do not exactly match manifest")
    for record_id, result in results.items():
        require(result.get("record_id") == record_id, f"{record_id}: result ID differs")
        require(
            result.get("schema_version") == "placement-consensus-additions-envelope-v2",
            f"{record_id}: wrong result schema",
        )
        decision = result.get("final_decision")
        judgment = result.get("application_merged_judgment")
        require(isinstance(decision, dict) and isinstance(judgment, dict), f"{record_id}: result incomplete")
        require(decision.get("verdict") == judgment.get("verdict"), f"{record_id}: verdict differs")
        score = judgment.get("natural_placement_score")
        require(
            isinstance(score, (int, float))
            and not isinstance(score, bool)
            and math.isfinite(score)
            and 0 <= score <= 100,
            f"{record_id}: invalid score",
        )
        observation = judgment.get("observation")
        require(isinstance(observation, dict), f"{record_id}: observation missing")
        require(isinstance(observation.get("summary"), str), f"{record_id}: explanation missing")
    return results


def tag(soup: BeautifulSoup, name: str, text: str | None = None, **attrs):
    node = soup.new_tag(name, **attrs)
    if text is not None:
        node.string = text
    return node


def add_component_table(soup: BeautifulSoup, details, judgment: dict) -> None:
    table = tag(soup, "table", attrs={"class": "judge-components"})
    head = tag(soup, "thead")
    row = tag(soup, "tr")
    for label in ("Component", "Score", "Assessment and evidence"):
        row.append(tag(soup, "th", label))
    head.append(row)
    table.append(head)
    body = tag(soup, "tbody")
    components = judgment["observation"]["components"]
    scores = judgment["component_scores"]
    for name, label in COMPONENT_LABELS.items():
        component = components[name]
        row = tag(soup, "tr")
        row.append(tag(soup, "td", label))
        score = scores.get(name)
        row.append(tag(soup, "td", "Unscored" if score is None else str(score)))
        cell = tag(soup, "td")
        visibility = component["visibility"]
        severity = component["severity"]
        confidence = component["confidence"]
        status = f"{visibility}; severity {severity if severity is not None else 'n/a'}; {confidence} confidence"
        cell.append(tag(soup, "div", status, attrs={"class": "judge-component-status"}))
        cell.append(tag(soup, "div", component["evidence"]))
        consequence = component.get("consequence")
        if consequence:
            cell.append(tag(soup, "div", f"Consequence: {consequence}", attrs={"class": "judge-muted"}))
        codes = component.get("issue_codes") or []
        if codes:
            cell.append(tag(soup, "div", "Issues: " + ", ".join(codes), attrs={"class": "judge-issues"}))
        row.append(cell)
        body.append(row)
    table.append(body)
    details.append(table)


def main() -> int:
    manifest = load_json(MANIFEST)
    records = manifest["records"]
    require(len(records) == manifest["expected_count"] == 128, "manifest count differs")
    by_id = {record["id"]: record for record in records}
    require(len(by_id) == 128, "manifest IDs are not unique")
    results = result_map(set(by_id))
    require(sha256(ORIGINAL) == manifest["source"]["viewer_sha256"], "original viewer changed")

    soup = BeautifulSoup(ORIGINAL.read_text(encoding="utf-8"), "html.parser")
    style = soup.find("style")
    require(style is not None, "viewer style missing")
    style.append(
        "\n.judge-note{background:#fff8db;border:1px solid #e3c858;border-radius:8px;padding:10px 12px;margin:12px 0 18px}"
        ".placement-judge{margin-top:8px;border:1px solid #ccd5e0;border-radius:6px;background:#f8fafc}"
        ".placement-judge>summary{cursor:pointer;padding:8px;font-weight:700}"
        ".placement-judge.pass>summary{color:#176b32}.placement-judge.review>summary{color:#8a5c00}.placement-judge.fail>summary{color:#a12622}"
        ".judge-body{padding:0 9px 10px}.judge-body p{margin:7px 0}.judge-muted{color:#5f6670;margin-top:4px}"
        ".judge-issues{color:#8b1e1e;margin-top:4px}.judge-components{width:100%;border-collapse:collapse;margin-top:9px;font-size:12px}"
        ".judge-components th,.judge-components td{border:1px solid #d8dee8;padding:6px;text-align:left;vertical-align:top}"
        ".judge-components th{background:#eef2f7}.judge-component-status{font-weight:600;margin-bottom:4px}"
    )
    h1 = soup.find("h1")
    require(h1 is not None, "viewer heading missing")
    note = tag(soup, "div", attrs={"class": "judge-note"})
    note.append(tag(soup, "b", "Natural-placement judge V3 consensus-v2 diagnostic. "))
    note.append(
        "Scores and explanations appear beneath each compared output. This judge is a research candidate for human review, not an automatic acceptance gate. "
        "It was calibrated on scene-generation images and is applied here to E2E comparison outputs at the user's request; treat scores as out-of-domain diagnostics."
    )
    h1.insert_after(note)

    inserted = 0
    verdicts = Counter()
    variants = Counter()
    for section in soup.find_all("section"):
        heading = section.find("h2")
        row = section.find("div", class_="row")
        require(heading is not None and row is not None, "viewer section structure differs")
        source_row_id = heading.get_text(" ", strip=True)
        figures = row.find_all("figure", recursive=False)
        require(len(figures) == 4, f"{source_row_id}: output count differs")
        for figure in figures:
            caption = figure.find("figcaption")
            require(caption is not None, f"{source_row_id}: caption missing")
            label = caption.get_text(" ", strip=True)
            require(label in LABEL_SLUGS, f"{source_row_id}: unknown variant {label}")
            record_id = f"{source_row_id}__{LABEL_SLUGS[label]}"
            result = results[record_id]
            decision = result["final_decision"]
            judgment = result["application_merged_judgment"]
            verdict = decision["verdict"]
            score = judgment["natural_placement_score"]
            confidence = decision["reported_overall_confidence"]
            verdicts[verdict] += 1
            variants[label] += 1

            details = tag(soup, "details", attrs={"class": f"placement-judge {verdict}"})
            details.append(
                tag(
                    soup,
                    "summary",
                    f"Judge: {verdict.title()} · {score:g}/100 · {confidence} confidence",
                )
            )
            body = tag(soup, "div", attrs={"class": "judge-body"})
            body.append(tag(soup, "p", judgment["observation"]["summary"]))
            body.append(
                tag(
                    soup,
                    "p",
                    f"Coverage {judgment['coverage']:.2f}; threshold status: {judgment['threshold_status']}",
                    attrs={"class": "judge-muted"},
                )
            )
            reasons = decision.get("verdict_reasons") or []
            if reasons:
                body.append(tag(soup, "p", "Decision reasons: " + ", ".join(reasons), attrs={"class": "judge-muted"}))
            for uncertainty in decision.get("uncertainty_notes") or []:
                body.append(tag(soup, "p", "Uncertainty: " + uncertainty, attrs={"class": "judge-muted"}))
            add_component_table(soup, body, judgment)
            details.append(body)
            figure.append(details)
            inserted += 1

    require(inserted == 128, f"expected 128 judge panels, inserted {inserted}")
    for node in soup.find_all(["a", "img"]):
        attribute = "href" if node.name == "a" else "src"
        value = node.get(attribute)
        if isinstance(value, str) and value.startswith("img/"):
            node[attribute] = f"{GATEWAY}/{quote(value)}"

    BUILT.mkdir(parents=True, exist_ok=True)
    viewer = BUILT / "viewer.html"
    viewer.write_text(str(soup), encoding="utf-8")
    result_export = {
        "schema_version": "placement-v3-consensus-v2-e2e-report-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_manifest": {"path": str(MANIFEST), "sha256": sha256(MANIFEST)},
        "source_viewer": {"path": str(ORIGINAL), "sha256": sha256(ORIGINAL)},
        "consensus_run": str(CONSENSUS),
        "claim_boundary": manifest["judge_application"],
        "counts": {
            "records": 128,
            "verdicts": dict(sorted(verdicts.items())),
            "variants": dict(sorted(variants.items())),
        },
        "records": [
            {
                "id": record_id,
                "source": by_id[record_id],
                "result_sha256": sha256(CONSENSUS / record_id / "result.json"),
                "result": results[record_id],
            }
            for record_id in sorted(results)
        ],
    }
    results_path = BUILT / "placement_judge_v3_results.json"
    results_path.write_text(json.dumps(result_export, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    reparsed = BeautifulSoup(viewer.read_text(encoding="utf-8"), "html.parser")
    require(len(reparsed.select("details.placement-judge")) == 128, "serialized panel count differs")
    require(all((img.get("src") or "").startswith("https://") for img in reparsed.find_all("img")), "relative image URL remains")
    build = {
        "status": "validated_local_build_not_published",
        "viewer": {"path": str(viewer), "bytes": viewer.stat().st_size, "sha256": sha256(viewer)},
        "results": {"path": str(results_path), "bytes": results_path.stat().st_size, "sha256": sha256(results_path)},
        "original_viewer_sha256": sha256(ORIGINAL),
        "records": 128,
        "judge_panels": 128,
        "verdicts": dict(sorted(verdicts.items())),
        "claim_boundary_shown": True,
        "all_media_urls_absolute": True,
    }
    build_path = BUILT / "build_manifest.json"
    build_path.write_text(json.dumps(build, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(build, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
