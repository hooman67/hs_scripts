---
name: feedback_lighter_touch_prompts
description: "Prompt tuning: prefer the smallest delta; heavy all-caps multi-clause additions degrade generative-model output"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d24f6783-62e3-43e4-9386-81e8e1cd0c68
  modified: 2026-08-24T17:16:05.244Z
---

When tuning a generation prompt to fix a residual artifact, make the **smallest possible change** — keep the
known-good prompt verbatim and append ONE short clause. Do not escalate to heavy, all-caps, multi-clause
"instructions."

**Why:** On the THD video rewriter ([[project_thd_video_rewriter]]), to remove a minor between-beat tape
retract I first added a heavy all-caps anti-retract paragraph (and separately tried thicker sketch lines).
Hooman's verdict: **both made the result visibly WORSE** than the plain baseline. The fix that worked was
the light one — baseline prompt unchanged + a single plain sentence. He said it directly: "you probably
need a lighter touch on the prompt." Over-constraining a diffusion/video model distorts the whole output,
not just the targeted behavior.

**How to apply:** Iterate prompts as minimal diffs. Change one thing, keep everything else byte-identical,
and A/B against the incumbent (put both in the gallery side by side). Resist the urge to pile on emphasis,
caps, or negations. If a small nudge doesn't fix it, the lever is probably elsewhere (keyframes, timestamps,
reference plate) — not a louder prompt.
