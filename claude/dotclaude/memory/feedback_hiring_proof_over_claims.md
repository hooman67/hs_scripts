---
name: feedback_hiring_proof_over_claims
description: "In hiring (resume review + interview scoring), score demonstrated proof, not claims; reject is a valid default"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 18bf80bb-e6ec-44ae-9427-b1d024d3ddc7
---

In all hiring work ([[reference_hiring_skill]], resume ranking, and interview feedback via
`/hiring_generate_interview_feedback`), **score proof, not claims** — but ONLY as an accuracy
standard for grading answers, never as a promote/reject verdict. Anyone can claim anything; credit
only what's demonstrated.

**Why:** Hooman rejected a smooth candidate (Liu He, 2026-07-20) I'd over-scored — on proof he was
4/10 (CFG backwards, cross-attn Q/KV backwards, off-modality flagship). Then (2026-08-04) he
corrected me hard on interview feedback: **my job is to parse answers and score correctness, NOT to
decide whether to promote**, and I was injecting my own biases.

**Interview-feedback rules (the `/hiring_generate_interview_feedback` skill — supersedes the old
`/interview-score`):**
- **NEVER put a hire/advance/reject/tier verdict in interview feedback.** Whether to promote is
  Hooman's decision alone. Give questions, answers, and scores — nothing else.
- **Record the candidate's actual answer to EVERY question asked**, quoting the transcript, with a
  per-question score (0–10). Then part scores **Technical /4 · Experience /3 · Culture /3 → /10**.
- **Keep my biases out of culture.** Hooman PREFERS candidates who care more about **impact on the
  company** than about how interesting the work is — a company-impact/results lean is a POSITIVE.
  Do not penalize it (I wrongly docked Yizhi Wang for a 70/30 company-vs-interest split).
- **Prompting is not a scoring axis.** Score the answer the candidate gave; note "reached after a
  hint" factually, but don't deduct for the interviewer having to prod.

**Resume review** still uses tiers (Interview/Second/Pass) and "reject is a valid default" — that's
fine there. Same proof discipline as the Sriharsha correction: discount unbacked gen claims.
