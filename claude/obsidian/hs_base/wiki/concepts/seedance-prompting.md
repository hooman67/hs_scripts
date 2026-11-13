---
type: concept
title: Seedance prompting & the structured rewriter
tags: [seedance, prompting, rewriter, foundry, thd, video-generation]
created: 2026-09-14
updated: 2026-09-14
sources: ["[[raw/thd-seedance-video-pipeline-learnings-2026-09]]"]
---

# Seedance prompting & the structured rewriter

How the [[wiki/entities/thd-video|THD Video]] app turns a raw brief into a high-adherence
[[wiki/entities/seedance|Seedance]] prompt: a GPT **structured rewriter** produces a typed shot, then a
deterministic compiler renders the exact string sent to fal (byte-for-byte "parity"). Lives in
`seedance_rewriter/` (`orchestrator.py`, `compiler.py`, `schema.py`, `rewriter_system_prompt.md`).

## The structured shot
- **Event Script** — a beat timeline tiled across `seconds` (e.g. `0-4 seconds: …`), the one hard
  timing contract Seedance honours.
- **beats** — ordered *physical* actions; each becomes one Event-Script segment. Expression/mood go in
  **`demeanor`**, a separate **uncapped** 【Performance】 box that does NOT consume a beat.
- **【Fidelity】** — a standing anti-blur directive (references are anonymized upstream, so tell the
  model to regenerate clear people/text rather than reproduce blur).
- **Reference Asset Roles** — a shipped section labelling each `@ImageN` with a role
  (`scene | identity | keyframe | motion | storyboard`).

## Key insight: the rewriter LLM is multimodal
`rewriter.py` hardcodes `role:"scene"` in the manifest it *shows* the LLM — but that's only an **input
hint**. The LLM **receives the image bytes** and re-roles each `@ImageN` in its output from what it
sees; the compiler ships those inferred roles. So the shipped prompt is **not** uniformly "scene" —
always verify against a real `used_prompt` before claiming it is. (Reviewers flagged the hardcoded
"scene" as a bug; the real gap is that we don't feed the *known* roles in — see Image roles below.)

## Image roles (reference vs storyboard)
- The request contract (`ImageAssetInput`) carries per image **only** `role: reference | storyboard` —
  there is no product/character/scene field. Storyboard-role assets get a fixed **storyboard directive**
  appended to the prompt (editable config text + a per-request debug override).
- The eval sets' `ordered_assets.entity/kind` (drill/couch/living-room/storyboard) is an **offline
  digestion artifact**, not a production input. At inference the only per-image signals are: the request
  role, the server's product-bank match, and the multimodal LLM's inference. Feeding the known signals
  into the rewriter instead of the hardcoded "scene" is a deferred follow-up.

## Response signals
- `notesToUser` — human-facing clamp/drop/"couldn't-honour" notes; returned in the envelope.
- `must_be_true` — checkable facts the rewriter captures, clamps, and validates, but **no consumer
  reads them** (not shipped to Seedance, not in the response): effectively write-only.

## Duration control (the 10s cap was ours)
fal `duration:"auto"` **sizes the clip to the prompt** (4–30s), so any short-clip ceiling is imposed by
*us*, in the rewriter:
- **`schema.py MAX_SECONDS`** clamps the Event-Script timeline, and **the system-prompt rule
  "seconds: an integer 4–N"** — these must move together (raising the code cap alone won't help; the LLM
  keeps proposing ≤ what the prompt states). `MAX_BEATS` caps beats (each is a segment; scale with
  duration but watch adherence — Seedance handles fewer beats better).
- To get longer clips, **keep sending `auto`** — it follows the now-longer prompt. Explicit
  `durationSeconds` (4–30) also works. Proven: `MAX_SECONDS 10→30`, `MAX_BEATS 2→5` yielded a 12s clip
  on a brief whose beats ran to 0:12, still with `auto`.

## Related
- [[wiki/entities/seedance]] · [[wiki/entities/thd-video]]
- [[wiki/concepts/foundry-standalone-app-pipeline]] — where the rewriter sits in the pipeline
- [[wiki/concepts/foundry-eval-workflow]] — how we measure rewriter/prompt changes
