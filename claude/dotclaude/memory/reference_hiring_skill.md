---
name: reference_hiring_skill
description: "/hiring skill — ranks resumes for Foundry gen-models roles against a living profile, keeps a persistent candidate ledger"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1f0828ea-f143-4856-b138-474723471050
---

`/hiring` skill (created 2026-06-25) reviews candidates for Hooman's Foundry generative-models
roles. Command file: `dotclaude/commands/hiring.md` (symlinked to ~/.claude/commands). Data store is the
project folder `/Users/hshariati/hs_scripts/claude/hiring/` (git-backed — note: contains candidate PII):
- `profile.md` — living target-candidate profile + scoring rubric (the source of truth; develops over time).
- `candidates.md` — ledger of every candidate reviewed by batch, with tier + one-liner + observed patterns.

Rubric = Hooman's three hard bars: (1) lead a project E2E, (2) strong eng AND ML in image/video
**generation**, (3) go-getter (top weight). Hard modality filter: generation only — demote
understanding/perception/3D/detection/recommendation even at Principal/Staff level.

Args: `/hiring <dir>` ranks a resume batch and appends to the ledger; `profile` shows/edits the
profile; `candidates` summarizes the ledger; `add <name>` records a single candidate/outcome.

Resumes come from adoberesearch Slack channel C09H6QJKSKY — the default bot token (adobe.enterprise)
CANNOT read that workspace, so resumes are downloaded manually into a ~/Downloads dir. See
[[feedback_make_blockers_obvious]].
