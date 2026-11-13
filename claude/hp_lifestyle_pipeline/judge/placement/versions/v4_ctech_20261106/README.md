# Natural-placement judge V4 C-Tech calibration candidate

This is the clean V3-to-V4 lineage requested on 2026-11-06. Older experimental directories named `v4*` remain untouched and are not part of this candidate.

V4 preserves V3's five scored components and adds targeted detection/calibration for the latest C-Tech feedback:

- modestly displaced chairs are warnings or review-level findings; an unseen chair in a close crop is unobservable;
- missing support structure, malformed furniture, impossible room perspective, major room-anchor problems, and material product/support misalignment can fail;
- prop/device interference and liquid crowding are explicit;
- bare walls, clipped artwork, sparse staging, and unattractive prop selection are unscored creative advisories;
- normal vanishing-point convergence is distinguished from bends, contradictory thickness, impossible corners, and incoherent comparable-edge convergence.

Severity semantics changed from V3:

| Severity | Meaning | Verdict effect |
| --- | --- | --- |
| 0 | no visible placement defect | none |
| 1 | warning / optional adjustment | may pass |
| 2 | clear review-level defect | review, score capped at 79 |
| 3 | clear fail-level defect | fail, score capped at 59 |
| 4 | impossible/effectively nonfunctional | fail, score capped at 19 |

The system prompt and scoring logic were informed by a high-effort GPT-6 Astra review, then checked against the original annotations and edited locally. Astra's advice is evidence, not an authority:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_2/astra_v6_2_and_judge_v4_response.md`

## Calibration evidence

The frozen joined annotations are:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_2/evidence/ctech_joined_evidence.json`

The explicit expected-verdict interpretation is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_ctech_20261106/evidence/calibration_cases.json`

These 35 cases are development calibration cases. They are not an accuracy estimate. V4 must also improve on held-out annotated cases before it can replace V3.

## Measured calibration result and promotion decision

This candidate did not establish an improvement over V3 and must not replace it.

- The 35-case development calibration matched 16 expected verdicts; V3 matched 15 on the same cases.
- The evidence-first 10-case gate matched 2/10; V3 matched 4/10. All five known failures were incorrectly passed, both expected review cases were passed, and only two clean passes were classified correctly.
- Adding C-Tech-specific visual anchors did not recover the defect detector. The first three known failures were still returned as pass/100, making the predeclared requirement of at least four detected failures impossible; the run was stopped rather than spending the remainder of the calls.
- A high-effort Astra vision probe also failed to identify a known missing-support defect and returned review because of limited visibility.

The failure is perceptual rather than a missing score cap: current multimodal prompting did not reliably see subtle furniture support, room-geometry, or load-path defects. More rubric wording, schema fields, or reference examples would overfit development comments without demonstrating detection. V4 is therefore retained as negative research evidence. The next judge iteration should add measurable geometric perception, such as product/support segmentation and line/plane consistency features, then test those features on a held-out annotated set.

Evidence is preserved at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_ctech_20261106/evidence/calibration_v2_report.md`

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_ctech_20261106/evidence/evidence_gate_v1_report.md`

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_ctech_20261106/evidence/anchors_gate_v2_stop.json`

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_ctech_20261106/runs/astra_probe_v1/magic__printer_FrontLeftMedium__p1.json`

## Validation

Run deterministic tests:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
PYTHONDONTWRITEBYTECODE=1 python -m pytest \
  judge/placement/versions/v4_ctech_20261106/test_v4_scoring.py -q
```

Build and validate the image manifest after obtaining AWS credentials through the standard broker:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
source ~/.claude/hshariati/aws_creds.env
python judge/placement/versions/v4_ctech_20261106/build_calibration_manifest.py
python judge/placement/versions/v4_ctech_20261106/run_batch.py \
  --manifest judge/placement/versions/v4_ctech_20261106/evidence/calibration_manifest.json \
  --run-name calibration_v1 \
  --workers 1 \
  --model gpt-5.5 \
  --validate-only
```

The candidate is frozen only as a failed calibration experiment. It is not eligible for promotion. A future successor requires a new version and held-out validation rather than edits to these recorded results.
