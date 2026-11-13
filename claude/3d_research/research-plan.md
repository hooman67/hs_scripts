# Research plan

## Research question

What controllable-video workflow can improve on the current THD motion-bank baseline while reducing
the work and expertise demanded of a non-technical customer?

## Competing hypotheses

- H1: A validated Blender blockout is a strong, general-purpose control signal and Astra can make
  authoring practical.
- H2: Blockouts improve control but merely move expensive curation from a motion bank into 3D scene
  construction and QA.
- H3: Simpler 2D controls or generated keyframes can reach comparable accuracy with lower user
  effort.
- H4: A hybrid workflow—automatic intent extraction plus selective 2D/3D constraints—dominates any
  single control representation.

## Staged method

1. Audit the proposal and its quantitative evidence.
2. Normalize incumbent and candidate workflows into the same task/effort/cost model.
3. Test Astra blockout authoring without paid Seedance generation.
4. Design the smallest discriminating paid A/B; run only after explicit approval.
5. Explore alternatives informed by observed failure modes.
6. Recommend adoption, integration, further validation, or rejection.

## Evidence schema

For every experiment retain:

- task and success criteria;
- source intent and all inputs;
- complete prompts and model/version/effort;
- code commit and environment;
- human interventions and elapsed active/wall time;
- validator outputs and visible failures;
- generated outputs and cost;
- blinded or clearly disclosed grading method;
- contradictions, failed runs, and exclusions.

## Quality gates

- Geometry validators passing is not sufficient; render inspection is mandatory.
- Headline scores must reconcile to raw per-example records.
- Same-task comparisons must control for prompt, duration, seed policy, and reference modality where
  feasible.
- Customer ease must count setup, corrections, specialized software, and hidden expert review—not
  only model runtime.
- No paid generation without a user-approved run and quoted maximum cost.

## Stopping rules

Stop or change direction when additional runs no longer change the conclusion, a failure is clearly
upstream of Seedance, the next uncertainty requires user evaluation, or the cost exceeds expected
information gain.

## Outputs

- A teach-back of each workflow and its real tradeoffs.
- Canonical evidence summaries with confidence labels.
- Jointly agreed experiment designs and review artifacts.
- A final workflow/architecture recommendation only after sufficient evidence.

