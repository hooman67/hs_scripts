# Candidate Profile — Foundry Generative Models (Image/Video)

> **Status: v0.2 (2026-07-06).** This is the living spec the `/hiring` skill scores
> candidates against. Edit freely — the rubric below is what the skill actually applies, so
> changes here change every future ranking. Pairs with `interview_process.md` (the 5-round
> panel + screening rubric + culture-fit-over-skills principle).

## Role context

- **Team:** Adobe Firefly / Foundry — consumer generative models.
- **Actual project:** image/video **generation** (the live bar has historically been **I2V /
  image-to-video**, plus T2I / I2I / image editing). This is generation, *not* understanding.
- **Shape of hire:** someone who can **lead a project end-to-end** — own it from data →
  training → post-training → deployment — combining real engineering with real ML.

## The three hard bars (Hooman's spec, used verbatim across prior batches)

> "I'm looking for someone that can lead a project E2E. Strong eng and ML skills (relevant to
> image / video gen) and most importantly a go getter attitude."

1. **E2E project leadership** — can own and drive a project end to end, not just contribute a slice.
2. **Strong eng AND ML — in image/video *generation*.** Both, not either alone. The rare combo
   of shipping-grade engineering + genuine ML/research depth.
3. **Go-getter attitude** — *explicitly the top weight* ("most importantly").

## Modality filter (hard)

Generation is a **hard filter, not a nice-to-have.** On-target = diffusion / DiT / flow-matching /
T2I / I2I / I2V / T2V / image editing / video gen, including post-training (SFT/DPO/GRPO/RLHF),
distillation, and serving of generative models.

Off-target (demote regardless of seniority) = understanding / VQA / captioning / detection /
segmentation / ReID / retrieval / recommendation / autonomous-driving perception / 3D
reconstruction / pure infra. Strong candidates in these areas have repeatedly been dropped to
second tier even at Principal / Staff level.

**Not auto-pass anymore (2026-07-06).** The modality filter is a **strong demote, not an
auto-reject.** An adjacent-modality candidate who shows strong go-getter/collaboration signal
should surface to **second tier** (worth a screen) rather than be dropped — the culture-fit
screen is where a slightly-off-but-excellent candidate gets rescued. Top tier
(interview-first) stays reserved for on-modality candidates.

## What counts as "go-getter" signal

- Competition/challenge wins (ICPC, CVPR challenges, Olympiads).
- Self-initiated projects pitched to leadership / 0→1 founding.
- Projects whose success expanded team or org investment.
- Internship → lead / intern → full-time conversions.
- Measurable scale wins (e.g. 1B→30B params, 4→120 words, beat a named SOTA model).

## What counts as "E2E + eng+ML" signal

- Owned full lifecycle: data curation → pretrain → post-train → deploy, with **adoption/impact
  metrics** ("X% adoption lift", "shipped to millions", "N× GPU/latency reduction").
- Top-tier publications (CVPR/ICCV/ECCV/NeurIPS/ICLR) **on generation** AND production shipping.
- "Lowest-risk give-them-a-project-and-it-ships" is the top compliment.

## Culture-fit axis (new, 2026-07-06)

Culture fit can **outweigh** a slightly-irrelevant skillset — and a strong-skills candidate
with **bad culture fit is a no** (unless we believe we can coach the behaviour). This axis is
mostly decided in the **screen/interview** (see `interview_process.md`: collaborator · listens ·
responsible · takes initiative), but score the **resume-visible proxies** when ranking:

- **Collaborator / responsible:** cross-team ownership, mentoring, open-source maintainership,
  "led a working group", incident/on-call ownership.
- **Initiative:** overlaps with the go-getter signals below (0→1 founding, self-pitched projects).
- Use these to **promote a borderline-adjacent candidate into second tier**, and to add a
  caveat when a skills-strong candidate reads as a lone-wolf / hand-off-heavy contributor.

## Red flags / auto-pass

- Thin/generic resumes or recruiter-profile exports.
- Generation claims unbacked by publications or shipped products (vague "contributed to /
  collaborated on" language around the gen work, while first-author depth is in another domain).
- Off-domain core (ETL, autonomous driving, recommendation, pure perception).

## Tie-breakers / preferences

- **Eng+ML combo over pure research prestige** without shipping, and over pure infra/inference
  without model R&D.
- Direct generation modality (image OR video) **beats** adjacent (3D/agentic-3D/motion synthesis)
  even when the adjacent candidate is the stronger leader/go-getter.

## Resolved decisions (Hooman, 2026-06-25)

1. **Role shape: strong senior IC (= the bar for "project lead").** (Clarified 2026-07-10.)
   To Hooman, a **strong senior IC and a project lead are the same bar** — the technical ownership
   depth is what matters, not a management title.
   - **A "project lead" who is NOT a strong senior IC is a NO.** Org/people-leadership does not
     substitute for hands-on gen depth.
   - **A strong senior IC who can't lead a whole project *immediately* is still a YES** — the
     leadership can grow; the IC strength cannot be faked. So don't reject a strong IC solely for
     lacking a formal "led the whole project" story.
   - The Yuanhao Zhai screen-out was **not** "no lead title" — it was that his ownership read as
     slice-level contribution, i.e. not yet a *strong senior IC* in the E2E sense. Probe for
     genuine ownership/delivery capability (see `prescreen_guide.md` Part 2), not for a title.
2. **Modality: image AND video weighted equally.** T2I/I2I/editing counts as much as I2V/T2V.
   (Broader than the prior "I2V is the bullseye" — pure image-gen is no longer "adjacent".)
3. **Tenure: prefer 2+ yrs shipping.** Demote brand-new grads / <1yr full-time, even with elite
   research+internship signal. (Flag the tenure gap explicitly rather than auto-passing.)
4. **Training + post-training experience IS a gate — but method-agnostic (2026-07-06).**
   Hands-on **training and post-training of generative models** is a genuine requirement:
   candidates must have actually trained/improved gen models, not just consumed or served
   them. **Do NOT over-index on the specific technique.** SFT, distillation, and RL
   (GRPO/DPO/RLHF) all satisfy the gate equally — significant SFT and/or distillation is fully
   sufficient, and RL is not specially required. The gate is *"real training/post-training
   depth on gen models,"* not *"which method."* Note the methods as context, don't rank on them.

## Resolved decisions (Hooman, 2026-07-06)

5. **Culture fit is decisive and can flip the call.** Slightly-irrelevant skillset + strong
   culture fit **beats** strong skills + bad culture fit, unless we believe we can coach the
   behaviour. Resume ranking softened accordingly: the hard modality filter is now a **strong
   demote/flag, not an auto-reject** — adjacent candidates with strong initiative/collaboration
   signal surface to second tier so the culture-fit screen can rescue them. Training +
   post-training on gen models remains a **gate**, but is **method-agnostic** (SFT /
   distillation / RL all count equally — don't over-index on which). See `interview_process.md`.
