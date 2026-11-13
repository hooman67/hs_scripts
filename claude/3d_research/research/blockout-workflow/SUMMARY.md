# Blockout → Seedance workflow

As of: 2026-09-22

## Contents

- [Question](#question)
- [Executive synthesis](#executive-synthesis)
- [Conceptual glossary](#conceptual-glossary)
- [What the workflow actually is](#what-the-workflow-actually-is)
- [What is supported](#what-is-supported)
- [What is not supported](#what-is-not-supported)
- [Astra evidence audit](#astra-evidence-audit)
- [Customer-effort implications](#customer-effort-implications)
- [Relationship to the incumbent](#relationship-to-the-incumbent)
- [Open questions](#open-questions)
- [Sources](#sources)

## Question

What is the proposed Blender blockout → Seedance workflow, what does each stage contribute, how
strong is its evidence, and is its authoring burden compatible with a non-technical THD customer?

## Executive synthesis

`VERIFIED` — The mechanism is real: a synthetic five-second Blender animation supplied as a
Seedance 2.5 video reference can strongly control coarse camera, staging, action path, and timing.
Direct inspection of the deployed clips confirms conspicuous transfer on the sampled lawn-aerator,
dryer-vent, and drill-bench examples.

`VERIFIED` — This is not currently a simple customer workflow. It replaces a curated motion clip
with a per-shot 3D program, geometric validation, render review, a detailed semantic mapping of
every grey primitive, and a 1.9K–4.0K-character Seedance prompt. The underlying rig is 2,276 lines
and 133 KB.

`ASSUMED`, strongly supported — The most promising product interpretation is not “customers use
Blender.” The blockout is an intermediate representation: a model compiles a natural-language
brief into a validated motion/camera trace, and the customer approves a cheap preview before any
paid video generation.

`UNVERIFIED` — The current evidence does not show that this workflow beats the THD incumbent on
instructional accuracy, appearance, product identity, tool-use correctness, or customer effort.
The published score only measures visible transfer from blockout to output.

## Conceptual glossary

**Blender** is a general-purpose 3D creation application. It can build geometry, connect parts into
an articulated hierarchy, position cameras, animate values with keyframes, and render those 3D
scenes into images or video. It is deterministic 3D software, not the generative video model in
this workflow.

In this project Blender is not operated primarily through its graphical interface. Python code
uses Blender's `bpy` API to construct a scene from boxes, cylinders, spheres, joints, camera poses,
and animation keyframes. Blender's Workbench renderer then turns 120 frames into a five-second grey
preview. Seedance performs the later photoreal generation.

**Temperature** is a model sampling control. Higher values flatten the token-probability
distribution and permit more varied choices; lower values concentrate choices on the most likely
continuation. Temperature 0 requests the least-random decoding available, but does not guarantee
bit-for-bit determinism across API calls. Two temperature-0 calls to the same model with the same
prompt and media are repeated measurements from one judge configuration, not independent judges.

### Inputs used to author the blockouts

- Scenes 1–11: according to the repository, a Claude Opus 5 coding session wrote and iteratively
  edited the Python rig/scene code, ran Blender probes and validators, and inspected renders. The
  exact original chat transcript and complete initial briefs are not tracked, so their full inputs
  cannot be audited.
- Astra lawn-aerator scene: the model received the complete 133-KB `whitemodel.py`, including all
  comments and prior lessons; a detailed textual lawn-aerator brief with six hard requirements;
  three tools for replacing scene code, running allowlisted Blender probes, and viewing renders;
  and each tool result/render during the loop.
- Astra via Codex dryer-vent scene: the documented inputs were a scratch copy of
  `whitemodel.py`, `footslide.py`, and `contact.py`, plus a `TASK.md`. The `TASK.md`, transcript,
  verification logs, and auxiliary assertion script are not tracked; only a summary and one still
  are preserved.

The later Seedance input is different: one blockout MP4 plus a detailed text prompt. The controlled
blockout study supplied no real photograph, source footage, or appearance plate to Seedance.

## What the workflow actually is

1. A Python program builds a faceless grey figure, props, set, camera, and 120-frame animation in
   Blender.
2. Three classes of checks inspect geometry: per-frame anatomy/invariants, temporal foot sliding,
   and selected contact with the work surface. A rendered still must also be reviewed by eye.
3. Blender renders a five-second, 1280×720 MP4.
4. That MP4 is sent as Seedance 2.5 `video_urls` / `@Video1` input.
5. A separate prompt explains what every grey solid represents, describes the real scene and
   talent, restates the beats and camera, and asks Seedance not to retain the clay appearance.
6. Seedance produces the photoreal output. The paid generation is downstream of all cheap geometry
   checks.

The proposal has “coarse” and “fine” arms. They differ primarily in whether `@Video1` is described
as supplying motion/camera only or as supplying the full structure to be re-rendered. The published
judge saturated and could not distinguish these arms.

## What is supported

### Structural control

`VERIFIED` for the sampled deployed examples and author-reported judged set — The output often
retains the blockout's framing, subject path, broad pose, camera motion, and beat timing. The
lawn-aerator and dryer-vent samples show striking spatial correspondence across five sampled
seconds.

### Cheap preview before paid generation

`VERIFIED` in the documented environment — Once authored, a blockout renders in roughly 18 seconds
and can be inspected before a Seedance call. This is an attractive failure-localization boundary:
fix obvious staging errors before paying for photoreal generation.

### A synthetic route around real-person reference restrictions

`VERIFIED` for the project's observed Seedance 2.5 behavior — The synthetic faceless video
reference passes where references carrying real-person likeness have been rejected. This does not
establish a universal provider policy.

### Astra can operate the bespoke rig

`VERIFIED` as an existence proof — In one purpose-built-harness run, Astra wrote a lawn-aerator
scene, invoked probes and renders, and produced a scene that passed the available validators. A
second Codex-CLI-authored dryer-vent scene is present in the branch and its deployed output shows
the intended broad setup and action.

## What is not supported

### The 2.97–3.00 scores are not an accuracy score

The paired Gemini rubric asks whether the generated clip resembles the blockout. It explicitly
does not judge appearance quality, brand compliance, product identity, or correct tool use. A
physically wrong blockout copied faithfully can score 3/3. The page itself documents wrong geometry
being copied into paid outputs.

The headline set contains 19 outputs but only seven scene types. Sixteen outputs are repetitions of
four original scenes (two prompt arms × two generations); three more scenes contribute one output
each. The effective task diversity is therefore seven, not nineteen.

The judge uses the same `gemini-3.7-flash` prompt twice at temperature 0. These are separate calls,
not independent judges. Five genuinely unrelated mismatch controls scored zero, which supports
gross discriminative validity. Two visually similar controls scored high or disagreed, showing
that the rubric cannot reliably identify the precise action/tool when scene and body layout are
similar.

The matched distribution is ceiling-saturated, so it cannot rank coarse versus fine or detect
meaningful improvements. The raw `conformance.json` is neither tracked in the branch nor published
beside the deployed page, so the aggregate cannot be independently recomputed from the durable
artifacts currently available.

### Appearance and product fidelity remain open

Three of 19 judged outputs retained visible grey-blockout residue. Direct inspection confirms a
drill-bench output with a grey ovoid head. The sampled lawn-aerator output preserves the composition
but renders a generic/bare machine. No product-identity reference image was used in the proposal's
controlled test.

### Generality is not established

The published work uses a single hand-built procedural rig, one model family, small scene diversity,
and no comparison against storyboard/keyframe controls on the same tasks. The documented Blender
binary is absent from the current research host, so the geometry commands cannot yet be rerun here.

## Astra evidence audit

The headline Astra run reports 9m08s, 11 turns, three code writes, eight probe runs, five viewed
renders, 507,586 input tokens, 16,899 output tokens, and 5,198 reasoning tokens. This establishes
that Astra can use a well-commented specialist rig and its tools.

It does not establish “natural language to finished Seedance input in nine minutes”:

- Astra received the complete 133-KB rig source and years-of-experience-style comments every turn.
- The harness only asked Astra to write the Blender scene block.
- A usable generation also required manual additions to `SCENE_LOOK`, `MAPPING`, `EVENT`, `CAMERA`,
  subject/preposition overrides, page titles, and publishing metadata.
- The Astra commit added 46 lines to the prompt system outside the harness; the model-authored
  Blender block added roughly 196 source lines.
- The 33m52s human comparison was a different scene and its commit included the scene, 30 prompt
  lines, review-page changes, and budget/documentation changes. The raw timed transcript is not
  tracked, so exact scope equality cannot be verified.
- There is one timed run, no repeats, and no task-matched human/Astra crossover.

Therefore the “3.7× faster” figure is `UNVERIFIED` as an end-to-end comparison. It is directional
evidence that Astra may reduce marginal 3D authoring time.

The second Astra/Codex result is weaker evidence: the branch preserves a short result summary and
one still, but not the claimed raw task, transcript, verification log, or auxiliary assertion
script. It is useful as another existence proof, not a reproducible benchmark.

## Customer-effort implications

Today, the blockout method trades one curation problem for another:

| Incumbent burden | Blockout burden |
|---|---|
| Curate reusable product-motion clips and metadata | Author per-shot 3D geometry and animation |
| Select/retrieve a motion asset | Compile a new scene into a bespoke rig |
| Preprocess customer images | Run geometry/temporal/contact checks and visual review |
| Rewrite prompt around references | Map every grey primitive to semantic identity in a long prompt |

The blockout route becomes customer-friendly only if all Blender/code/mapping work is hidden behind
an agent and a cheap visual approval loop. Customer-facing controls should be intent, corrections,
and acceptance—not coordinates, joint angles, Python, or Blender.

### Alternative under investigation: reusable articulated SKU rigs

The user proposed a materially different approach from the per-shot blockouts audited above:

1. Import authoritative CAD for a finite product catalog.
2. Separate the CAD into rigid moving components.
3. Define physical pivots, translation axes, limits, dependencies, and grasp points once per SKU.
4. Let a product-knowledgeable user visually pose those controls and insert timeline keyframes.
5. Attach simplified hands to explicit grasp targets.
6. Render the animation as the video condition supplied to Seedance.

`ASSUMED` — This is closer to a reusable digital puppet than a conventional blockout. It could
replace a library of fixed motion clips with a compact kinematic model capable of producing many
valid motions. It is especially promising for machines with coupled moving parts, where text alone
is an inadequate specification.

The editable source remains the Blender scene—meshes, component hierarchy, constraints, and
keyframes. The rendered MP4 is a flattened delivery format for Seedance and cannot preserve those
editable mechanisms.

Important boundary: CAD supplies geometry but normally does not supply production-ready animation.
A rigging step must still identify component boundaries, place pivot origins, encode degrees of
freedom and limits, define coupled motion, and create hand-grasp targets.

## Relationship to the incumbent

The incumbent HTML contains 54 shots: 52 succeeded and two failed. It shows 147 ordinary reference
images, 74 storyboard images, 211 processed images, and 14 attached motion clips. Despite its legacy
filename, the report states that this run uses person-gated sketch-Nano preprocessing rather than
SAM3 anonymization.

The blockout proposal does not replace everything the incumbent does:

- It could replace or augment the motion-bank clip for shot-specific motion and camera control.
- It does not by itself solve product identity, visual style, scene identity, or character
  consistency; those likely still need customer references.
- The most plausible winner is a hybrid: ordinary references for appearance/identity plus an
  automatically generated blockout for motion/camera only.

## Open questions

- Can Astra repeatedly produce valid scenes across distinct action families without human code
  repair?
- How much total human time is required including brief clarification, prompt mapping, preview
  review, and correction?
- Can the semantic mapping and event/camera prompt be compiled automatically from the same scene
  representation?
- Do the validators predict human judgments of tool-use and instructional correctness?
- Does a blockout outperform storyboard frames or ordered keyframes on the same difficult shots?
- Does a hybrid blockout + appearance-reference workflow preserve control without clay or generic
  product leakage?

## Sources

- Adobe-Firefly/THD_Proj, immutable commit
  `b4b684f268e49bf38a6a7c0fa70b4a7a6244d878`, retrieved 2026-09-22.
- https://github.com/Adobe-Firefly/THD_Proj/blob/b4b684f268e49bf38a6a7c0fa70b4a7a6244d878/docs/blockout/REPRODUCE.md
- https://github.com/Adobe-Firefly/THD_Proj/blob/b4b684f268e49bf38a6a7c0fa70b4a7a6244d878/docs/blockout/AUTHORING-TIME.md
- https://github.com/Adobe-Firefly/THD_Proj/blob/b4b684f268e49bf38a6a7c0fa70b4a7a6244d878/scripts/blockout/judge_conform.py
- https://github.com/Adobe-Firefly/THD_Proj/blob/b4b684f268e49bf38a6a7c0fa70b4a7a6244d878/scripts/blockout/astra_scene.py
- https://github.com/Adobe-Firefly/THD_Proj/blob/b4b684f268e49bf38a6a7c0fa70b4a7a6244d878/scripts/blockout/whitemodel.py
- https://pluto-prod-zouyang-snap-restore-h2-7-0-41004.or2.colligo.dev/thd_blockout/
- User-selected incumbent baseline linked in `/home/colligo/hs_scripts/claude/3d_research/README.md`.
