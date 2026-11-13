# fe-html suitability for the KDP blind real-vs-generated evaluation

Date: 2026-10-07

## Conclusion

`fe-html` supports the core KDP evaluation without building a new viewer: one image per row, a custom
`Real / Generated / Unsure` question, additional confidence/usability questions, reviewer-attributed publishing,
CSV export, and aggregate summaries.

The stock folder/S3 conversion is not safely blind by itself. It exposes filename/path-derived row IDs and tile
labels, retains asset URLs in `data.json`, and does not randomize presentation order. The correct POC approach is
to build a blinded `data.json`/staging prefix with opaque asset names, opaque shuffled row IDs, a neutral tile label,
no provenance metadata, and an admin-only truth map stored outside the report directory.

A custom viewer is needed only if the study requires a locked questionnaire or different randomized order for each
reviewer from one shared URL. For a first C-Tech pilot, preprocessing the manifest is sufficient.

## Verified capability matrix

| Requirement | Stock fe-html | Evidence / limitation |
|---|---|---|
| One stimulus per row | Yes | Default `--group-by none` creates one asset per row. |
| Ask “real or generated?” | Yes | Custom rubrics accept arbitrary options; use `Real, Generated, Unsure`. |
| Add confidence/usability | Yes | Multiple questions and 1–5 or custom rubrics are supported. |
| Preconfigure questions in shared URL | Yes, editable | `?q=<base64 JSON>` overrides local storage, but reviewers can reopen Questions and change them. |
| Reviewer identity | Yes | IMS/LDAP identity is included in published annotation documents. |
| Persist results | Yes | One-click publish writes `annotations/reviewer_<n>.json`. |
| Export results | Yes | CSV export and a multi-reviewer Summary tab are built in. |
| Hide provenance automatically | No | Default wrapper uses relative paths/basenames as row IDs and labels. URLs remain in DOM/`data.json`. |
| Randomize order automatically | No | Inputs are lexicographically sorted; viewer preserves data order unless a user explicitly sorts. |
| Lock the protocol | No | Questions/columns remain editable in the stock viewer. |
| Pairwise A/B comparison | Available but not recommended here | Compare mode exists, but the desired task is single-stimulus source classification, not paired preference. |

## Source evidence

Default wrapper sorting and provenance-bearing IDs/labels:

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html_report.py:108`

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html_report.py:157`

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html_report.py:173`

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html_report.py:178`

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html_report.py:180`

Custom rubric parsing and shareable question configuration:

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html:4197`

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html:4266`

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html:4417`

Always-visible row ID / asset label behavior:

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html:5620`

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html:5712`

Annotation publishing, reviewer identity, CSV, and Summary behavior:

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html:6231`

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html:6362`

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html:6968`

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html:7023`

## Recommended no-fork pilot design

1. Select balanced real/generated stimuli within each SKU and comparable scene archetype.
2. Export every stimulus to the same dimensions, format, color profile, and approximate compression; strip EXIF.
3. Copy stimuli under opaque random names such as `candidate_00417.png` in one neutral S3 prefix. Do not use
   `real/`, `generated/`, SKU-source, or model-name subfolders.
4. Create opaque row IDs and a neutral asset label such as `Image`. Do not include truth/source/model fields in the
   report's `data.json`.
5. Shuffle the manifest before publishing. For stronger control, publish reviewer-specific shuffled manifests.
6. Store the ID→truth mapping outside the report directory and do not expose it through the viewer.
7. Preconfigure questions through the shareable `?q=` URL and show one row per page:
   - `Do you think this image is real or AI-generated?` — `Real / Generated / Unsure`
   - `How confident are you?` — `1 / 2 / 3 / 4 / 5`
   - `Is this usable for marketing after normal production review?` — `Yes / No / Unsure`
8. Publish annotations through the gateway URL and analyze classification accuracy against the hidden truth map.

## Escalation trigger for a custom viewer

Fork or minimally customize the viewer only if the pilot requires:

- deterministic per-reviewer random order from one shared report;
- disabling sort/search/compare controls during the blind pass;
- locking questions and column visibility;
- preventing reviewers from inspecting provenance-bearing URLs in the browser DOM/network panel.
