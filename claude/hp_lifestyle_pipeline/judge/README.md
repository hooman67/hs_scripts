# HP lifestyle generation judges

Judge research is a temporary detour from the frozen V6.1 writer. Everything intended for Git lives in this directory. Image bytes live in ignored local_runs/ and are recoverable from source S3 manifests.

## Current project

The first judge evaluates **natural laptop/printer placement in scene-generation images**. It produces a 0–100 index, component evidence, coverage, confidence and a provisional pass/review/fail decision. It is a research prototype, not an approved automatic acceptance gate.

- [Current placement v2 findings and rubric](placement/versions/v2/SUMMARY.md)
- [Placement v3 feedback-driven research candidate](placement/versions/v3/SUMMARY.md)
- [Independent V3.1 C-Tech amendment and fresh V3 comparison — calibration gate not met; no promotion](placement/versions/v3_1/SUMMARY.md)
- [Frozen placement v1 experiment](placement/SUMMARY.md)
- [Exact live checkpoint](PROJECT_STATE.md)
- [Decisions and confirmed user contract](DECISIONS.md)
- [Durable lessons](LEARNINGS.md)
- [Roadmap](LONG_TERM_PLANS.md)
- [Research method](research-plan.md)
- [Pipeline access and successful generation smoke test](pipeline_access/README.md)

## Placement implementation

The current research candidate is V3's consensus revision, documented in `placement/versions/v3/SUMMARY.md`. It combines frozen V2 and compact V3 assessments, then corroborates newly raised material concerns with two differently instructed checks. It shows a small development gain with an additional uncertainty review; it is not an approved replacement for human acceptance. The completed160-image V6.1 evaluation has118 pass,38 fail,4 review. All predictions, unsuccessful experiments, source hashes and model responses remain preserved.

V2 stays frozen under `placement/versions/v2/` as the reproducible baseline, including the96 earlier V6 judgments and their published annotations. V3's new review reports separate image quality from agreement with the judge. `placement/versions/v3/data/release_status.json` records the exact selected candidate and limitations.

The following files describe the preserved v1 baseline:

- `placement/system_prompt.md`: judge instructions.
- `placement/data/visual_anchors.json`: fixed development examples and reference illustrations.
- `placement/observation_schema.json`, `placement/scoring.py`: contract and deterministic aggregation.
- `placement/run_judge.py`, `placement/run_pilot.py`: real model invocation and bounded evaluation.
- `placement/evaluate_pilot.py`: exact-target versus ambiguous-comment detection audit.
- `placement/build_report.py`: evidence gallery.
- `placement/data/`: frozen sources, manifests, labels and split.
- `placement/runs/`: preserved trials and raw model responses.

Inputs: generated image, original twin render, laptop/printer type and original scene prompt; scene_generation stage only. Geometry guides and downstream rewritten prompts are diagnostic context only and are not passed to the judge. No new generation run is part of this task.

Use the current research candidate with its explicit limitations in placement/versions/v3/SUMMARY.md. Do not treat a score of 100 or model-reported high confidence as a verified human approval.
