# Med-Research — AOS Vaccination Exemption Research (Project State & Operating Manual)

**This is the single source of truth for this project.** If you are a new agent picking
this up, read this file top to bottom first. It tells you the goal, what's been done, where
execution stands, and how to behave.

Last updated: 2026-07-07 by Claude (Opus 4.8). Owner: Hooman Shariati (hshariati@adobe.com).

> ⚠️ This machine can die at any time. **Persist everything to disk as you go** and update
> the four living records (below) after every working session. Minimize work lost.

> ⚠️ **THIS IS NOT LEGAL OR MEDICAL ADVICE.** This project is *research to inform Hooman and
> his attorneys and physicians*. The green-card case is filed by Berry Appleman & Leiden LLP
> (BAL); medical judgments belong to a licensed physician / civil surgeon. Output = a
> cited, confidence-marked map of options + questions to take to BAL and to a doctor. We do
> not file forms, and we never propose anything that misstates facts (see §5, guardrail).

---

## 1. The Goal (what Hooman actually wants)

Complete his **Adjustment of Status (I-485)** green-card step **without Hooman or his wife
having to receive any vaccines** — by using only *legitimate, documented* pathways.

Context (facts from Hooman, 2026-07-07):
- Currently in the US on **TN visa**; employer-sponsored green card; **PERM approved**; now
  at the **AOS (I-485)** stage. Medical exam (**Form I-693**) by a USCIS civil surgeon is a
  required piece; I-693 includes a vaccination requirement.
- Hooman does **not** want vaccines — moral, religious, AND health concerns.
- Has an autoimmune disease: **Large Granular Lymphocytic (LGL) leukemia**, which he
  believes was caused by COVID-19 vaccination. *(Causation is his belief; see §6 — for the
  immigration goal we do not need to prove/disprove it, only to know whether the condition
  and its treatment create documented vaccine contraindications.)*
- **Wife is pregnant** and is a co-applicant (confirm co-applicant status — see open Qs).
- Immigration case is handled by **BAL** (paralegal contact: Emily Reyes). Anything we
  surface should be framed as input for BAL and a physician, not as a self-executed action.

Hooman's two starting strategies:
1. Find a **vaccine-conscious civil surgeon** who will legitimately sign the I-693.
2. Explore **legal ways to be exempt** from the vaccination requirement.

**Reframed strategy stack (see `research-plan.md`), best → last resort:**
verify current requirement (COVID likely removed) → **titers / proof of existing immunity**
→ **medical contraindication** (his LGL + wife's pregnancy) → **religious/moral waiver
(I-601)** → **refusal**.

---

## 2. Where We Are Right Now (PROJECT STATE)

**Status: PLANNING.** Project created 2026-07-07. Scaffolding written; no research run yet.
`research-plan.md` holds the two-track methodology; awaiting Hooman's scoping answers
(open questions in `PROJECT_STATE.md`) before launching subagents.

→ See `PROJECT_STATE.md` for the live action-item checklist. This CLAUDE.md holds stable
context; PROJECT_STATE.md holds moment-to-moment status.

---

## 3. Anti-Hallucination Backbone (this project is HIGH-stakes on accuracy)

A wrong fact here can cost a green card. Discipline is stricter than the sibling projects:

- **Primary, official sources only for anything load-bearing:** USCIS.gov (Policy Manual
  Vol. 8, Form I-693 + instructions), CDC (ACIP recommendations & the vaccination Technical
  Instructions for civil surgeons), the INA / 8 CFR, and Federal Register notices. Law-firm
  blogs and forums are *leads to verify*, never citations of record. Full list in `sources.md`.
- **Every load-bearing claim carries: source + as-of date + confidence
  (VERIFIED / ASSUMED / UNVERIFIED).** "VERIFIED" means traced to a primary official source
  read this cycle — not recalled from training.
- **Law and policy change.** Cite the *edition/date* of I-693 and the *effective date* of any
  policy. Re-verify the COVID-19 requirement status before relying on it.
- When a claim can't be pinned to a primary source, mark it UNVERIFIED and list it as an open
  question — do not let it drive a recommendation.

---

## 4. File / Folder Organization

Organize by topic, few files. Names navigable with zero context.

```
med_research/
├── CLAUDE.md              # THIS FILE — stable context + operating manual
├── PROJECT_STATE.md       # LIVE status: action items, open questions, what's next
├── LEARNINGS.md           # durable findings (consolidated, confidence-marked)
├── DECISIONS.md           # decisions Hooman & I made + rationale
├── LONG_TERM_PLANS.md     # roadmap / where this is heading
├── research-plan.md       # the two-track methodology + subagent plan
├── sources.md             # curated primary sources + reliability notes
├── requirement/           # what is ACTUALLY required (vaccine list, I-693 edition, COVID status)
├── exemptions/            # the exemption doors: titers, contraindication, I-601 waiver, refusal
├── civil_surgeon/         # finding/vetting a civil surgeon; discretion & form mechanics
└── data/                  # saved source PDFs, screenshots, form copies (dated)
```

One file per topic inside each folder; don't spawn a file per source.

---

## 5. How To Work Here (operating rules — from Hooman)

1. **Diligent, human-readable records.** Maintain the four living files (PROJECT_STATE,
   LEARNINGS, DECISIONS, LONG_TERM_PLANS). After every session, check each for updates.
   **If unsure whether Hooman acted on advice, how he did it, or whether he agreed to a plan
   change — ASK. Don't assume.**
2. **Organize by topic, minimize file count.** Fix fragmentation when reasonable.
3. **Fan out subagents for independent work; keep the main session free. Serialize dependent
   steps.** (Requirement scoping must finish before exemption deep-dives; see plan.) Don't
   over-parallelize.
4. **Cite primary sources, quantify, mark confidence. No hallucinated law, dates, or lists.**
5. **Bias toward action inside the funnel; bias toward asking on scope/direction decisions
   that are Hooman's** (which door to pursue, whether to loop in BAL, medical disclosures).

**GUARDRAIL (non-negotiable, added at project start):** Every path must be *truthful*.
Material misrepresentation on an immigration medical or benefit application is grounds for a
**permanent** inadmissibility bar (INA 212(a)(6)(C)) — categorically worse than any vaccine.
We only pursue exemptions grounded in genuine facts (real contraindications, real immunity,
sincere convictions, correctly-recorded refusal). We never help find a physician to fabricate
an exemption or misstate a record, and we flag the moment any idea drifts toward that line.

---

## 6. Scope Notes / Sensitive Points

- **LGL-leukemia ↔ COVID-vaccine causation is out of scope as a thing to prove.** For the
  immigration goal it matters only through two factual channels: (a) does the disease + its
  treatment create *documented* contraindications to specific vaccines (a medical question
  for his hematologist/civil surgeon, grounded in CDC/ACIP)? and (b) does it support the
  *sincerity* of a moral/religious conviction? We research those channels; we do not
  litigate causation.
- **Not legal/medical advice** (see header). Deliverables are decision-support for BAL + a
  physician.

---

## 7. Hard-Won Learnings (short version — full list in LEARNINGS.md)

_(none yet — project just started; see the reframing in research-plan.md §0)_
