---
name: project_thd_rewriter
description: "THD production shot-rewriter we're building: design + implementation + FFDY-7583 reproduction"
metadata: 
  node_type: memory
  type: project
  originSessionId: d24f6783-62e3-43e4-9386-81e8e1cd0c68
  modified: 2026-08-29T08:31:13.307Z
---

Building a production **shot rewriter**: user's per-shot brief (SCENE/CHARACTER/PRODUCTS/SHOT
DESCRIPTION/MISC + reference images) → **Seedance prompt**, returned as a **structured, editable**
object with **carry-overs marked** for cross-shot consistency. Code in `hs_scripts/claude/thd/rewriter/`.
Grounded in our two experiments ([[project_ffdy7304_laundry_sink]], [[project_thd_video_rewriter]]) and
cross-checked against the report's `videogen` package (Adobe-Firefly/THD_Proj PR 145 — access via
[[reference_github_thd_proj]]), its eval, and the product bank.

**Design (DESIGN.md).** KEEP from the report: one LLM call → structured fields → one deterministic
compiler → string (parity-tested); the measured Seedance rules (camera whitelist w/ hit-rates, never
orbit_360/mounted_on_tool/probe_lens; **≤2 beats**; **onset-yes/cessation-no** — never ask an action to
stop; describe motion not the rig; 4–10s; @ImageN↔image_urls[N-1]; send full-res originals; report
clamps, never silent). DROP (their own eval couldn't separate arms on score — value was discipline):
family matching, corpus prior, fixed hands-only talent, template matching. CORRECTION we made (Hooman's
objection, correct): **style/framing come from the USER's reference images**, not tool footage/corpus;
the product bank only grounds tool **appearance + motion**. Talent = the user's CHARACTER + face-removal
prep. `must_be_true`/`camera_why` kept as metadata, NOT shipped in the string.

**Structured schema:** `carry_overs` parent (characters / scene / style / products / continuity) +
per-shot `shot`. Carry-overs are replayed verbatim into later shots so a stateless rewriter still yields
a consistent stitched film (generalises our "couple bible").

**Files:** `DESIGN.md`, `rewriter_system_prompt.md`, `schema.py`, `compiler.py` (parity boundary),
`orchestrator.py`, `llm_adapter.py` (→ /gpt_call, [[reference_gpt_call_skill]]), `test_parity.py` (all
pass), `repro_ffdy7583.py`, `build_repro_html.py`.

**⚠️ Open question to verify:** the bank's PROMPTS.md claims `@Video` motion-transfer works on Seedance
2.5 ref-to-video — CONTRADICTS our Makita finding (no video→video motion transfer). Design does NOT
hard-depend on it (motion note drives beats + keyframe fallback). Run a 2-clip A/B before trusting it.

**FFDY-7583 reproduction (done 2026-08-29):** drove the 8 final-cut laundry-sink shots (1,2,3,4,5,8,9,
hero) through the rewriter with SIMPLE briefs + GPT-5.6-terra; generated with Seedance 2.5 (original
plates/modes, rewriter's prompt). Couple stayed consistent across all person shots via carry-overs;
shots closely match the originals. Ours keeps faces off-screen (brief said so; original showed faces).
Gallery: `s3://…/video_rewriter/rewriter_repro_ffdy7583/gallery/index.html`.
