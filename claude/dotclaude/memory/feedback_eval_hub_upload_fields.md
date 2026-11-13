---
name: feedback-eval-hub-upload-fields
description: "When user invokes /eval_hub_upload, always ask for the five required fields up front before running anything."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d7506a15-d978-4278-8d36-88190cc25743
---

When the user invokes `/eval_hub_upload`, always ask them to confirm these five fields before running anything — do not assume defaults from prior runs:

1. `--eval-set` (eval set name, e.g. `humain_t2i_gpt_592`)
2. `--version` (eval set version, e.g. `1.0`)
3. `--model-id` (e.g. `h06_v13_iter_1026000_expanded_prompts`)
4. `--created-by` (e.g. `hshariati`)
5. `--num-variations` (e.g. `2`)

**Why:** Hooman explicitly asked this on the first real Humain run. These five fields determine the published run identity in Eval Hub; using a stale value silently re-uses someone else's eval set / model id and corrupts downstream analytics. Asking once up front catches typos before 1000+ assets get uploaded.

**How to apply:** Even if `$ARGUMENTS` to the skill includes some of them, present the full list back via `AskUserQuestion` or plain text and have the user confirm before running. After they confirm, echo all five values together so they can spot typos at a glance.

See [[reference-eval-hub-skill]] for the skill itself and supported input modes.
