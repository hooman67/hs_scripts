#!/usr/bin/env python3
"""Build the self-contained Astra V4.5 redesign task from frozen V4.4 evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
V44 = HERE.parents[1] / "v4_4"
V431 = HERE.parents[1] / "v4_3_1"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def make_transport_image(source: Path, destination: Path, max_side: int) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = image.convert("RGB")
        source_size = image.size
        if max(image.size) > max_side:
            scale = max_side / max(image.size)
            image = image.resize(
                (round(image.width * scale), round(image.height * scale)),
                Image.Resampling.LANCZOS,
            )
        image.save(destination, format="JPEG", quality=90, subsampling=0, optimize=True)
        transport_size = image.size
    return {
        "source_dimensions": list(source_size),
        "transport_dimensions": list(transport_size),
        "transport_sha256": sha256_bytes(destination.read_bytes()),
        "transport_bytes": destination.stat().st_size,
    }


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    expectations = json.loads(read(V431 / "data/gate_6_expectations_withheld.json"))
    manifest = json.loads(read(V44 / "data/dev_6_manifest.json"))
    diagnostic = json.loads(read(V44 / "data/gate_a_diagnostic_v1.json"))
    by_expectation = {row["record_id"]: row for row in expectations["records"]}

    evidence_records = []
    full_evidence_records = []
    for record in manifest["records"]:
        record_id = record["record_id"]
        rows = [row for row in diagnostic["rows"] if row["record_id"] == record_id]
        if len(rows) != 3:
            raise RuntimeError(f"expected three repeats for {record_id}, found {len(rows)}")
        repeats = []
        full_repeats = []
        for row in sorted(rows, key=lambda item: item["repeat"]):
            result_path = Path(row["result_path"])
            result = json.loads(read(result_path))
            full_repeats.append(
                {
                    "repeat": row["repeat"],
                    "status": result["status"],
                    "derived": result["derived"],
                    "defect_proposals": result["defect_proposals"],
                    "scout_test_outcomes": [
                        {
                            "test_id": item["test_id"],
                            "defect": item["defect"],
                            "severity": item["severity"],
                            "direct_evidence": item["direct_evidence"],
                            "counterevidence": item["counterevidence"],
                            "visibility_limit": item["visibility_limit"],
                            "region": item["region"],
                        }
                        for item in (result.get("scout") or {}).get("tests", [])
                    ],
                    "verifier": result.get("verifier"),
                    "raw_calls": result.get("raw_calls"),
                    "result_sha256": sha256_bytes(result_path.read_bytes()),
                }
            )
            derived = result["derived"]
            repeats.append(
                {
                    "repeat": row["repeat"],
                    "status": result["status"],
                    "derived_output": {
                        "score": derived["score"],
                        "score_valid": derived["score_valid"],
                        "verdict": derived["verdict"],
                        "reason": derived["reason"],
                        "confirmed_issues": derived["confirmed_issues"],
                        "uncertain_proposals": derived["uncertain_proposals"],
                        "warnings": derived["warnings"],
                        "owned_issue_codes": derived["owned_issue_codes"],
                        "explanation": derived["explanation"],
                    },
                    "scout_test_outcomes": [
                        {
                            "test_id": item["test_id"],
                            "defect": item["defect"],
                            "severity": item["severity"],
                            "direct_evidence": item["direct_evidence"],
                            "counterevidence": item["counterevidence"],
                            "visibility_limit": item["visibility_limit"],
                        }
                        for item in (result.get("scout") or {}).get("tests", [])
                    ],
                    "verifier_results": (result.get("verifier") or {}).get("results", []),
                    "result_sha256": sha256_bytes(result_path.read_bytes()),
                }
            )
        evidence_records.append(
            {
                "record_id": record_id,
                "runtime_input": record["runtime_input"],
                "frozen_hashes": record["frozen_hashes"],
                "human_label": by_expectation[record_id],
                "v4_4_repeats": repeats,
            }
        )
        full_evidence_records.append(
            {
                "record_id": record_id,
                "runtime_input": record["runtime_input"],
                "frozen_hashes": record["frozen_hashes"],
                "human_label": by_expectation[record_id],
                "v4_4_repeats": full_repeats,
            }
        )

    evidence = {
        "schema_version": "hp-placement-v4.5-astra-design-evidence-v1",
        "claim_boundary": "six reused labeled development cases; design diagnostics, not an accuracy estimate",
        "v4_4_protocol_freeze_sha256": diagnostic["protocol_freeze_sha256"],
        "v4_4_gate_metrics": {
            key: diagnostic[key]
            for key in (
                "repeat_count",
                "case_count",
                "model_calls",
                "repair_calls",
                "labeled_verdict_correct",
                "labeled_verdict_total",
                "required_issue_detected",
                "required_issue_total",
                "correct_predicted_issue_instances",
                "predicted_issue_instances",
                "material_fail_repeat_correct",
                "material_fail_repeat_total",
                "majority_labeled_verdict_correct",
                "majority_labeled_verdict_total",
                "majority_required_issue_detected",
                "majority_required_issue_total",
            )
        },
        "records": evidence_records,
    }
    evidence_path = HERE / "frozen_six_evidence.json"
    evidence_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n")
    full_evidence = dict(evidence)
    full_evidence["records"] = full_evidence_records
    (HERE / "frozen_six_evidence_full.json").write_text(
        json.dumps(full_evidence, indent=2, ensure_ascii=False) + "\n"
    )

    task = f"""# Task: diagnose V4.4 misses and design a minimal HP Natural Placement Judge V4.5

You are the senior multimodal-evaluation architect for an HP lifestyle-image placement judge. You are receiving the exact six labeled development cases as images after this text, plus their exact human comments and all V4.4 repeat outputs below. Diagnose why V4.4 has high precision but unusably low recall, then specify the smallest V4.5 architecture change that can materially improve recall without over-rejecting the clean control.

You cannot access the filesystem. Everything needed is embedded here or supplied as images in the same request. Treat this as a design task. Do not implement or run a larger judge. Do not recommend scaling to 160 until a development gate and a frozen held-out gate pass.

## Runtime and product contract

- Production inputs: generated scene image, original digital-twin render, product type (`laptop` or `printer`), and scene prompt.
- The judge scores only the scene-generation image. The twin identifies the product and functional front.
- Hidden/cropped relations are unobservable, not wrong. Tight crops must be able to pass.
- Output: 0–100 placement score, pass/review/fail, component checks, concise visible evidence, and full audit data.
- Current production candidate model is GPT-5.5 through Direct OpenAI.
- Application-owned deterministic validation, synthesis, scoring, caching, and bounded retries are allowed.
- A repair call may fix only transport or invalid structured output, never a valid visual conclusion.
- Human labels, expected verdicts, and case-specific anchors must never be passed to the deployed judge.

## Human natural-placement requirements

1. Printers should sit on dedicated equipment tables, credenzas, cabinets, or supports, not personal desks visibly occupied by someone.
2. Products need usable, believable orientation relative to furniture and the scenario.
3. Avoid laptops stranded centrally without a plausible user position, products aimed toward corners, and awkwardly foregrounded printers.
4. Maintain plausible scale, shared perspective, orientation, support contact/load path, cast shadows, and reflections.
5. Relevant product/support and furniture/room edge families should follow coherent perspective and deliberate alignment. Corresponding real-world parallel edges may converge in perspective; unequal 2D slopes alone are not proof.
6. A printer's functional front must be approachable; props must not block loading, output, or controls.
7. A laptop should relate to the only plausible visible associated chair. A modest chair offset can be severity-1 review; never invent an off-frame chair to rescue the layout.
8. A rectangular/square home printer support normally belongs at a wall or room edge. Central placement needs a visibly established shared-equipment/work narrative.
9. Correct product position does not rescue malformed/misplaced support furniture.
10. Missing furniture support and malformed support geometry are placement defects, but a cropped underside is not evidence of missing support.
11. A diagonal product/support relation is not automatically intentional. Visible functional evidence must support an intentional diagonal use.
12. Unrelated rendering defects belong in warnings unless they block use or contradict the activity zone.

## V4.4 diagnostic result

V4.4 used a defect-oriented scout followed by a verifier that received only scout-positive proposals. The six cases were run three times each. All 18 repeats were scoreable. It made 37 calls, including one objective repair. Repeat-level verdict accuracy on labeled cases was 6/15; required-issue recall was 4/21. Its four predicted issue instances were all correct, but it returned `fail` on 0/9 material-fail repeats. Majority results got 2/5 labeled verdicts and 1/7 required issues. Five of six cases were stable, primarily because false negatives were stable. V4.4 is rejected and must not scale.

The key information-flow problem is that the verifier cannot discover a defect the scout omitted. Yet merely making the verifier another broad all-issue scan may reproduce the same perceptual failure. Your proposal must account for both independence and task specialization.

## Constraints on the V4.5 answer

- Do not solve this by adding more rubric prose to the same broad scout.
- Explicitly consider removing the scene prompt from perception calls, because intent language may bias the model toward a coherent story. The scene prompt can be used later only if you justify a narrowly bounded role.
- Consider issue-specific visual passes or deterministic crops/overlays where they change what the model must perceive.
- Consider small visual anchors only if they are generic, frozen, non-target examples and cannot leak labels from evaluated cases. State whether they are needed.
- Keep deterministic application synthesis and issue-code ownership.
- Give an explicit worst-case and normal-case model-call budget. Prefer the minimum architecture that can recover the four missed material families.
- The clean control must remain a placement pass; unrelated disfigured glasses may be a warning.
- Separate observed visual facts from policy classification. Avoid model-written narratives that can rationalize geometry.
- Any third call must be narrowly triggered and bounded. No open-ended deliberation.
- The answer must be concrete enough to implement strict schemas and tests.

## Required answer

1. **Failure diagnosis by case and by pipeline stage.** Explain why the exact V4.4 scout/verifier outputs missed or found each required issue, using the supplied images and repeats.
2. **Minimal V4.5 architecture.** Specify stages, what images/crops each stage sees, whether it sees the twin and/or scene prompt, and how stages remain independent.
3. **Per-stage strict JSON shapes.** Give compact field definitions/enums and semantic invariants. You may use pseudocode JSON Schema rather than full boilerplate.
4. **Deterministic synthesis.** Give exact mapping from observed facts to current issue codes, conflict handling, observability behavior, score/verdict derivation, and duplicate-penalty control.
5. **Prompts.** Give exact concise system-prompt language for each visual stage. Prompts must focus on direct measurements/facts and must not contain target-case labels.
6. **Visual processing.** State which full images, product/support crops, furniture/room crops, edge/line aids, or generic visual anchors are used, and how raw pixels remain authoritative.
7. **Call budget and failure behavior.** State normal/worst-case calls, one objective repair budget, timeouts/retries, and explicit error sentinels.
8. **Test protocol.** First reuse these six labeled development cases with three repeats. Give a numeric stop/go criterion that requires material-fail recall improvement and protects precision/clean control. Then define a frozen held-out 8–12 case gate with labels withheld from prompts. Only after both gates may a 160-case diagnostic run occur.
9. **Risks and falsification.** Name the most likely failure modes, what evidence would show this architecture is still inadequate, and the next smallest information-flow change if it fails.

Prefer a minimal architecture over a maximal ensemble. If two designs are plausible, select one and explain why the alternative is not the first experiment.

## Exact frozen six-case evidence

```json
{json.dumps(evidence, indent=2, ensure_ascii=False)}
```

## Exact V4.4 scout system prompt

```text
{read(V44 / 'scout_system_prompt.md')}
```

## Exact V4.4 verifier system prompt

```text
{read(V44 / 'verifier_system_prompt.md')}
```

## Exact V4.4 codebook

```python
{read(V44 / 'codebook.py')}
```

## Exact V4.4 deterministic validation/reconciliation/scoring

```python
{read(V44 / 'scoring.py')}
```
"""
    task_path = HERE / "astra_task.md"
    task_path.write_text(task, encoding="utf-8")

    image_assets = []
    run_root = V44 / "runs/dev_6_gate_a_v1_gpt55"
    for record in manifest["records"]:
        rid = record["record_id"]
        repeat_dir = run_root / rid / "repeat_1"
        paths = {
            "raw_scene": Path(record["runtime_input"]["generated_image"]),
            "original_twin": Path(record["runtime_input"]["twin_image"]),
            "product_support_crop": repeat_dir / "product_support_crop.png",
            "geometry_overlay": repeat_dir / "geometry_overlay.png",
        }
        for role, path in paths.items():
            if not path.is_file():
                raise FileNotFoundError(path)
            transport_path = HERE / "request_images" / rid / f"{role}.jpg"
            transport = make_transport_image(
                path,
                transport_path,
                1800 if role in {"raw_scene", "product_support_crop", "geometry_overlay"} else 1400,
            )
            image_assets.append(
                {
                    "record_id": rid,
                    "role": role,
                    "source_path": str(path),
                    "source_sha256": sha256_bytes(path.read_bytes()),
                    "source_bytes": path.stat().st_size,
                    "transport_path": str(transport_path),
                    **transport,
                }
            )
    request_manifest = {
        "schema_version": "hp-placement-v4.5-astra-design-request-v1",
        "task_path": str(task_path),
        "task_sha256": sha256_bytes(task_path.read_bytes()),
        "task_bytes": task_path.stat().st_size,
        "model_requested": "gpt-6-astra",
        "reasoning_effort": "high",
        "max_completion_tokens": 24000,
        "image_assets": image_assets,
        "transport_total_bytes": sum(item["transport_bytes"] for item in image_assets),
    }
    (HERE / "request_manifest.json").write_text(
        json.dumps(request_manifest, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps({"task_bytes": task_path.stat().st_size, "image_count": len(image_assets)}, indent=2))


if __name__ == "__main__":
    main()
