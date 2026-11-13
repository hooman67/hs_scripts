#!/usr/bin/env python3
"""Build a self-contained text-only Astra audit of the root-owned V4.5 judge."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
V45 = HERE.parent
OUT = HERE / "attempt_4_text_only_review"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    evidence = read(HERE / "frozen_six_evidence.json")
    task = f"""# Text-only Astra audit: HP Natural Placement Judge V4.5

You are auditing a proposed multimodal image-judge architecture. **This request contains no images.** You must not claim to have visually inspected any case or validated any pixel-level label. Treat the six exact human annotations and recorded model outputs as development evidence supplied by the engineering team.

Your role is to audit the root-owned V4.5 design before its six-case development gate. Do not edit files or produce implementation code. Return concrete, bounded prompt/codebook/scoring recommendations that the implementing engineer can accept or reject.

## Runtime goal

The deployed judge receives a generated scene image, original product digital twin, product type, and scene prompt, but the V4.5 visual observers intentionally do not receive the scene prompt. It scores only natural product placement in the scene-generation image. Hidden/cropped relations are unobservable, not wrong. Tight crops must be able to pass. Output includes 0–100 score, pass/review/fail, issue evidence, warnings, and audit metadata.

## Why V4.5 exists

V4.4 used one broad defect scout and a verifier that could inspect only scout-positive proposals. Across six reused labeled development cases × three repeats:

- 18/18 scoreable;
- required-issue recall 4/21 at repeat level and 1/7 at majority-case level;
- labeled verdicts 6/15 repeat level and 2/5 majority-case level;
- 4/4 predicted issues were correct;
- 0/9 material-fail repeats returned fail.

The failure was stable false negatives. A later text-independent visual probe removed the scene prompt and scanned seven relations in one call. It improved required issue recall to 3/7 but verdicts fell to 1/5 because it over-severed chair displacement and under-severed central-table and prop issues. It still missed support anatomy, missing load path, device/support axis conflict, and shared perspective. The clean control remained clean.

## Proposed V4.5 architecture

V4.5 uses two independent visual observers:

1. functional/room observer owns support role, support room placement, device surface position, prop/activity relation, operating access, and user position;
2. geometry/topology observer owns device/support axes, furniture/room axes, product scale, load path, support anatomy, shared perspective, support contact, and shadows/reflections.

Neither sees the scene prompt or the other observer's result. The application validates both structured outputs and deterministically owns issue-code mapping, severity, penalty grouping, score, and verdict. A single global repair may fix only invalid JSON/schema/transport output. There is no scout-positive-only verifier in this first experiment because omission recall is the established failure and V4.4 precision was 4/4.

## Exact six-case annotations and V4.4 repeat evidence

The JSON below includes all six exact human comments, expected verdict/issue descriptions, scene-prompt text supplied to V4.4, three compact repeat outputs per case, every scout test outcome, and verifier results. It contains labels because this is a design audit; labels must never be passed to the deployed judge.

```json
{evidence}
```

## V4.5 focused-probe diagnostic

```text
{read(V45 / 'root_probe/focused_probe_diagnostic.md')}
```

## Exact root-owned functional observer prompt

```text
{read(V45 / 'functional_observer_system.md')}
```

## Exact root-owned geometry/topology observer prompt

```text
{read(V45 / 'geometry_observer_system.md')}
```

## Exact current codebook

```python
{read(V45 / 'codebook.py')}
```

## Current deterministic validation/synthesis/scoring

```python
{read(V45 / 'scoring.py')}
```

## Current implementation/claim boundary

```text
{read(V45 / 'DESIGN_AND_CLAIM_BOUNDARY.md')}
```

## Local evidence-based design synthesis

This is the implementing team's proposal, not an Astra answer. Audit it critically.

```text
{read(HERE / 'SYNTHESIS.md')}
```

## Requested audit

Return these sections:

1. **Evidence-grounded diagnosis:** For each of the six cases, identify which observer owns the expected issue and which prompt/schema/scoring behavior is most likely to recover or miss it. Use only the textual evidence; explicitly avoid visual claims.
2. **Prompt audit:** Identify concrete ambiguity, confirmation-bias, false-positive, and false-negative risks in each exact observer prompt. Quote the exact risky text. Propose only minimal replacement/addition/deletion blocks, with exact wording. Do not rewrite the prompts wholesale.
3. **Codebook and deterministic-policy audit:** Check issue ownership, subtype coverage, severity ownership, observability handling, duplicate penalties, and error sentinels. Give concrete recommended changes and explain which six-case failure each addresses.
4. **False-positive controls:** Protect tight crops, ordinary perspective convergence, valid partial supports/pedestals/panels/cantilevers, intentional but usable product rotation, movable chairs, and unrelated malformed props. State schema invariants or deterministic rules rather than relying on prose alone.
5. **Gate A acceptance criteria:** Audit the current proposed six-case × three-repeat gate. Give exact numeric go/stop conditions for issue recall, fail recall, chair severity, clean control precision, structural validity, and stability. Separate development gating from any accuracy claim.
6. **Smallest fallback if Gate A fails:** Choose one next information-flow change. Options include splitting the geometry observer into topology versus axes/perspective, adding a generic non-target anchor set, or adding an independent bounded confirmer. Pick one, with normal/worst-case call budgets.

Constraints:

- Do not recommend target-label injection, case-specific anchors, human post-editing, or scaling to 160 before gates pass.
- Do not claim image inspection or empirical validation from this text-only request.
- Keep normal calls low and retries bounded.
- Preserve application-owned issue mapping, severity, scoring, and verdict unless you identify a specific deterministic defect.
- Prioritize recall improvement without turning unobservable relations into defects or causing the clean control to fail.
"""
    task_path = OUT / "astra_task.md"
    task_path.write_text(task, encoding="utf-8")
    source_paths = [
        HERE / "frozen_six_evidence.json",
        HERE / "SYNTHESIS.md",
        V45 / "root_probe/focused_probe_diagnostic.md",
        V45 / "functional_observer_system.md",
        V45 / "geometry_observer_system.md",
        V45 / "codebook.py",
        V45 / "scoring.py",
        V45 / "DESIGN_AND_CLAIM_BOUNDARY.md",
    ]
    manifest = {
        "schema_version": "hp-placement-v4.5-astra-text-audit-request-v1",
        "task_path": str(task_path),
        "task_sha256": sha(task_path),
        "task_bytes": task_path.stat().st_size,
        "images_attached": 0,
        "claim_boundary": "text-only design audit; no visual evaluation claims",
        "model_requested": "gpt-6-astra",
        "reasoning_effort": "high",
        "max_completion_tokens": 12000,
        "sdk_max_retries": 2,
        "request_timeout_seconds": 600,
        "wall_timeout_seconds": 900,
        "sources": [
            {"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size}
            for path in source_paths
        ],
    }
    (OUT / "request_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"task_bytes": task_path.stat().st_size, "task_sha256": manifest["task_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
