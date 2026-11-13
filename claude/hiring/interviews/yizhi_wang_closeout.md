# Close-out — Yizhi Wang (R161074, Staff Applied Scientist, Firefly Foundry)

**From:** Hooman Shariati (pre-screen) → Eric Caldwell / Mollie Schenck (recruiting), cc Ajinkya Kale
**Decision:** **Not advancing** after pre-screen. Please close the loop with the candidate.
**Candidate:** Yizhi Wang (C7083578) — ByteDance, Seedance 1.0/2.0.
**Pre-screen:** 5/10 (Technical 2/4 · Experience 2/3 · Culture 1/3). Full report:
`interviews/wang_yizhi_2026-07-27.md`

---

## Message to paste for recruiting (candidate-safe framing)

> Thanks for setting up the conversation with Yizhi — I enjoyed talking with him. After the
> pre-screen we've decided **not to move forward to the full panel for the Staff Applied Scientist
> role.** He has relevant, on-modality video-generation experience (Seedance I2V), but for this
> **Staff-level** bar the technical depth on core post-training material and the evidence of
> independent, whole-project ownership weren't quite where we need them. It's a level/depth fit
> issue, not a lack of talent — he's early in his career and clearly capable. Happy to share more
> detail if useful. Please close him out gracefully.

## Internal rationale (for the record — do not send to candidate)

Scored on demonstrated proof, not claims. Genuine positives — but not enough to clear bar on all
three axes, and clearly below **Staff** scope:

- **Technical (2/4):** correct on entry-level material (SFT/DPO, CFG mechanism + high-CFG failure),
  but below bar on the gating material — the **GRPO answer was near-content-free** (the hard gate),
  **cross-attention K/V was backwards**, and he needed the VAE-decoder debugging answer supplied to
  him. Almost every answer required prompting or correction.
- **Experience (2/3):** genuinely on-modality with one credibly-owned contribution (a retrieval-based
  training-pair pipeline to avoid a "copy-paste" shortcut) — actually a positive — but no scale/eval/
  post-training/outcome detail; reads as a strong mid-level contributor on a large team, not Staff.
- **Culture (1/3):** asked to own a mistake, the bug in his story belonged to another team's
  deployment, not to him; and he self-rated motivation as 70% company-impact/recognition vs. 30%
  interest in the work. Strong initiative story and good live listening, but the two heavily-weighted
  axes both fell short.

**Net:** reject; the on-modality experience is real but the hard-gate technical gaps + ownership/
motivation signals put him below bar, especially for Staff. Not a re-approach for this req.
