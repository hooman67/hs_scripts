# Research Plan — AOS Without Vaccines (two tracks, one funnel)

Status: PROPOSED (2026-07-07). Awaiting Hooman's scoping answers before launch.
See `CLAUDE.md` for goal + operating rules; this file is the methodology.

---

## §0. Reframing (read this first)

Hooman framed two strategies: (1) a vaccine-conscious doctor, (2) legal exemption. Research
suggests the exemption space has **four distinct doors**, two of which need **no waiver
application at all**, and that one specific fear may already be moot. Confidence marks below
are pre-research (from training, cutoff Jan 2026) and MUST be re-verified against primary
sources in Stage 1 — they are the *hypotheses the funnel tests*, not conclusions.

**H1 — COVID-19 shot is likely NOT required anymore.** [ASSUMED-HIGH — VERIFY FIRST]
USCIS appears to have removed the COVID-19 vaccination from the I-693 requirement in early
2025. If confirmed, Hooman's central fear (the COVID shot he links to his LGL leukemia) is
resolved before any waiver. *This is the single highest-value thing to verify and we verify
it in the first hour.*

**H2 — Titers / proof of immunity avoid shots with no waiver.** [ASSUMED-HIGH]
For several required vaccines (MMR, varicella, Hep A/B), a blood test showing existing
immunity, or documented prior vaccination, satisfies the requirement. Zero new shots, zero
waiver form. Cheapest, cleanest door for anything Hooman is already immune to.

**H3 — Medical contraindication is a strong door for BOTH of them.** [ASSUMED-MED→HIGH]
- Hooman: LGL leukemia is autoimmune and frequently treated with immunosuppressive therapy
  (methotrexate, cyclophosphamide, etc.). Immunosuppression is a **standard contraindication
  to LIVE vaccines** (MMR, varicella, LAIV) under CDC/ACIP. A civil surgeon can mark these as
  medically contraindicated — a "blanket waiver," **no I-601 required.**
- Wife: **pregnancy is a standard contraindication to live vaccines** (MMR, varicella) under
  CDC/ACIP. Same mechanism — documented by the civil surgeon, no I-601.
- Limit: contraindication is vaccine-specific and often *temporary* (pregnancy ends; immuno-
  suppression may pause). It may defer rather than permanently exempt inactivated vaccines
  (e.g. Tdap, flu, Hep B). Scope carefully.

**H4 — Religious/moral waiver (Form I-601, INA 212(g)(1)(C)) is real but high-friction.**
[ASSUMED-MED] The door Hooman was thinking of. Requires showing the objection is (i)
religious or moral, (ii) **sincere**, and (iii) **opposition to vaccination in ANY form** —
not one specific vaccine. **Adversarial flag:** if Hooman has had prior vaccines, or the
objection reads as COVID-specific, USCIS can challenge sincerity. Slower, discretionary,
adjudicator-dependent.

**H5 — Refusal box exists but is the weakest door.** [ASSUMED-HIGH] I-693 has a box for
refusal; bare refusal without a granted waiver → inadmissibility. Last resort only.

**Resulting priority order to research/pursue:** H1 → H2 → H3 → H4 → H5. Hooman's "find a
doctor" idea is **not a separate path** — it is the *execution layer* that makes H2/H3/H5
happen correctly and, if needed, supports H4. Restructured as Track B below.

**GUARDRAIL restated:** every door must be truthful. We never seek a physician to fabricate
an exemption. See CLAUDE.md §5.

---

## §1. The two tracks

### Track A — "What is actually required, and how do I legally not take shots?"
Establishes ground truth (the requirement) then maps each exemption door with primary-source
citations, tailored to Hooman's LGL + wife's pregnancy. This is the **decision map**.

### Track B — "Who signs the form, and how?"
The execution layer: how civil surgeons work, how much discretion they have over
contraindication/titer/refusal documentation, how to find and pre-screen one who will
*properly* document a legitimate exemption, and the mechanics (sealed envelope, editions,
timing vs. wife's pregnancy and vs. RFE risk).

The tracks are mostly parallel, but Track B's *targeting* depends on Track A's output (you
pre-screen doctors for the specific door you'll use). So: **Track A Stage 1 runs first
(parallel internally); Track B launches once we know which doors are live.**

---

## §2. The funnel (stages, subagent layout, dependencies)

### Stage 0 — Sources & scoping [main session, blocking]
- Build `sources.md` (primary sources: USCIS Policy Manual Vol. 8 Part B/C, Form I-693 +
  instructions, CDC civil-surgeon Technical Instructions & ACIP contraindication guides,
  relevant Federal Register notices, INA 212(g), 8 CFR 245).
- Resolve Hooman's open scoping questions (in PROJECT_STATE.md).

### Stage 1 — Ground truth + door mapping [PARALLEL subagents, Track A]
Independent, fan out concurrently. Each returns a topic file with confidence-marked, cited
findings + open questions:
- **1a — Current requirement.** Verify H1 (COVID status), pull the *current* required-vaccine
  list, the current I-693 edition date, and how the vaccination assessment page works.
  → `requirement/vaccine_requirement.md`
- **1b — Titers / immunity door (H2).** Which vaccines accept titers or documented history;
  what evidence a civil surgeon accepts. → `exemptions/titers_and_immunity.md`
- **1c — Medical contraindication door (H3).** CDC/ACIP contraindications for LGL/immuno-
  suppression AND for pregnancy, mapped to each required vaccine; how the civil surgeon
  records a blanket waiver. → `exemptions/medical_contraindication.md`
- **1d — Religious/moral waiver door (H4).** I-601 process, the "any form" sincerity test,
  evidence, timelines, discretion, documented denial patterns. → `exemptions/religious_waiver_i601.md`
- **1e — Refusal + inadmissibility (H5) and the misrepresentation guardrail.** What refusal
  triggers; the 212(a)(6)(C) permanent-bar risk. → `exemptions/refusal_and_risks.md`

### Stage 2 — Merge into a decision map [main session, serialized]
Combine 1a–1e into a single **door-by-door matrix**: for each required vaccine × each of
{titer, contraindication-his, contraindication-wife, waiver, refusal} → does it clear the
requirement? Confidence? Evidence needed? This is the core deliverable.
→ `exemptions/decision_map.md`

### Stage 3 — Track B: civil surgeon execution [PARALLEL, launches after Stage 2 picks doors]
- **3a — Civil surgeon discretion & mechanics.** How much latitude a civil surgeon has to
  document titers/contraindication/refusal; sealed-envelope process; what the surgeon can vs.
  cannot decide (surgeon does the exam; USCIS adjudicates waivers). → `civil_surgeon/mechanics.md`
- **3b — Finding & pre-screening.** How to use the USCIS "Find a Civil Surgeon" locator;
  a phone script to pre-screen a doctor for willingness to *properly* document the specific
  door(s) we chose; questions to confirm they provide I-693 in the current edition.
  → `civil_surgeon/finding_and_prescreen.md`

### Stage 4 — Synthesis & the BAL/doctor packet [main session]
Two short deliverables for Hooman:
- **Recommended path** (ranked, with the fallback chain) + exactly what evidence to gather.
- **A question list for BAL and for the physician/hematologist** — the items only they can
  answer (co-applicant status, whether they'll support a contraindication letter, whether BAL
  will file an I-601 if needed). Framed so Hooman can forward it.
→ `LONG_TERM_PLANS.md` holds the roadmap; the packet lives in `exemptions/recommended_path.md`.

### Stage 5 — Adversarial review [subagent, before anything is called "done"]
A red-team pass: try to break the recommended path. "Where does this get challenged in an
RFE? Where is sincerity attackable? Where does a contraindication expire before adjudication?
Where could a well-meaning doctor's note constitute misrepresentation?" Findings feed back
into the decision map. Nothing is VERIFIED-final until it survives this.

---

## §3. Scorecard (how we rank the doors for Hooman)

Each door scored, so the recommendation is a ranking not a hunch:
- **Certainty of clearing the requirement** 30% (does it actually satisfy USCIS?)
- **No new shots for Hooman or wife** 25% (the actual goal)
- **Low legal risk** 20% (distance from the misrepresentation/inadmissibility line)
- **Speed / low friction** 15% (waiver adds months + RFE risk)
- **Durability** 10% (permanent vs. temporary/deferral; survives to adjudication)

Tune weights with Hooman after Stage 1.

---

## §4. What I will NOT do
- Not file forms, not contact BAL or any doctor on Hooman's behalf without his say-so.
- Not assert any law/date/vaccine-list from memory as VERIFIED — primary source or it's UNVERIFIED.
- Not propose, hint at, or design around any misrepresentation. (CLAUDE.md §5 guardrail.)
- Not litigate the LGL↔COVID causation question (CLAUDE.md §6).
