# Legacy THD research-folder context

As of: 2026-09-22

Source root: `/home/colligo/hs_scripts/claude/thd`

## Scope loaded

The folder contains 221 substantive non-cache files totaling about 665 KB: 12 Markdown documents,
37 Python programs, 118 JSON records/configurations, 50 extracted text files, three small gallery
JavaScript files, and one `.gitignore`. Generated mypy/pytest caches and bytecode were excluded. The
git-ignored `creds.txt` was deliberately not read or copied.

There are no nested `AGENTS.md`, `CLAUDE.md`, or research-rule files in this source root.

## Workstream 1 — Door-lock article-to-video rewriter

The original experiment recreated THD door-lock how-to footage, especially shot 0003's three tape
measurements. Its main gallery manifest records 17 iterative rounds followed by pipeline results for
shots 0007–0027. The pipeline configs cover 23 JSON files; shot 0027 was deliberately skipped as a
full-body establishing/outro rather than a hands-on step.

Durable findings:

- A photoreal person in a Seedance image reference triggered the observed R3 rejection; bare hands
  and forearms passed. Person-free plates, cover-body edits, or line sketches were used instead.
- Reference composition dominated textual camera instructions. The first ordered keyframe was
  especially influential.
- A correct short tape span could not reliably be created from prose. Pre-building the correct state
  in a reference and using an ordered middle keyframe constrained interpolation.
- Ordered `@ImageN` keyframes transferred action better than first/last frames alone.
- Mixing wide and tight keyframes created a scale conflict. Consistently wide beat keyframes, made by
  removing the body while preserving real hands/tool, held framing and natural hands.
- Three subtle actions needed more temporal budget. Sixteen seconds separated the measurement beats
  better than eight seconds.
- Small, local prompt corrections worked better than heavy emphatic instruction. The approved
  sketch-driven result used thin sketches plus one concise between-beat clause.
- Sketches work best as the ordered geometry keyframes, with a trailing photoreal image used only for
  appearance. Putting the appearance plate first weakened geometry adherence.
- Fine numerals and text were not trustworthy and should be added in post.

Executable pipeline:

1. Extract beat frames from a source clip.
2. Use `cover_body`, `sketch`, or raw/hands-only preparation.
3. Compose ordered-keyframe prompts with per-beat constraints.
4. Generate Seedance reference-to-video and integrate results into the gallery.

Important code/document discrepancy: the documentation describes roughly five seconds per beat,
but the current `rewriter_pipeline.py` actually rounds and clamps the original source clip duration
to 4–22 seconds. The experimental manifests are qualitative records, not a formal blinded eval.

## Workstream 2 — Glacier Bay laundry-sink storyboard

FFDY-7304 converts an eight-slide customer storyboard into a roughly one-minute product/how-to spot.
It contains a 12-series storyboard index, 31 generation configurations/iterations, an invented couple
bible, assembly scripts, a target-shot comparison, and a 38-section review manifest.

The strongest methods were:

- face-free product macros through single-image i2v;
- person-free room/product plates plus a verbatim couple description for recurring generated talent;
- ordered keyframes for flat → lifted → standing assembly progressions;
- line-sketch geometry keyframes plus a prior photoreal generated frame for appearance;
- literal `LAST frame` language to pin an end state;
- locked-off camera wording for beauty shots;
- nano-based finish recoloring followed by a locked-off hold;
- trimming generated shots in post to reproduce fast commercial pacing.

Known failures include annotated marks being rendered, vague panel-motion language causing exaggerated
box deformation, image editors accidentally completing partially assembled products, and dirty/busy
cover-body source frames producing incorrect edited keyframes. Retiming to visually unambiguous source
moments was more effective than prompt escalation.

The folder records a time-sensitive policy reversal: Seedance 2.5 video-edit briefly accepted clips
containing generated people and later rejected them; Seedance 2.0 still accepted those tests as of the
recorded 2026-08-28 experiment. This must be reverified before relying on it.

## Workstream 3 — Makita storyboard and model comparison

FFDY-7309 indexes a 39-page Makita deck containing nine spots and shots 101–905 across saws, drills,
nailers, grinders, planers, blowers, and MakTrak. Only two shots have generation records:

- 901: rear-handle circular saw cutting wood, sketch → photoreal image → i2v;
- 806: angle grinder cutting metal with sparks, person-free photoreal image → i2v.

The associated model comparison contains 55 configs across Seedance 2.5, Seedance 2.0, and MiniMax
Hailuo 3. Recorded conclusions: H3 was often clean/sharp and accepted simple natural-language motion,
while Seedance retained the advantage for precise multi-keyframe progressions and hard end-state
control. Model/API behavior and pricing are historical and require current verification.

## Reference-preparation playbook

The folder includes a complete agent prompt for preparing Seedance-safe input images. It requires
visual inspection, explicit KEEP/REMOVE edit prompts, preservation of partially assembled states,
removal of people/reflections/baked-in graphics, and review after every edit. Its R3 rules are
empirical and time-sensitive rather than permanent provider guarantees.

## Context-use cautions

- Treat gallery notes such as “winner,” “matched,” and “final” as recorded human judgments, not
  standardized accuracy scores.
- Reverify live vendor safety behavior, endpoints, limits, and model availability.
- Do not reuse credentials from this folder; use the current approved credential workflows.
- Several FFDY-7309 scripts are copied from FFDY-7304 and retain stale laundry-sink docstrings, so
  code behavior and configuration paths are more reliable than those headers.
