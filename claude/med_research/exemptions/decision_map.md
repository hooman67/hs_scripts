# Stage 2 — The Decision Map (door-by-door matrix + recommended paths)

**What this is:** the single consolidated deliverable that merges Stage-1 topics 1a–1e into one
door-by-door matrix. For every currently-required vaccine (rows) against every exemption door
(columns) it states whether that door **clears** the requirement, the **evidence needed**, and the
**confidence**. It then gives a **recommended path for Hooman** and a **separate one for his wife**,
with fallbacks, and honestly flags any requirement that **no legitimate door clears** (a shot may be
unavoidable).

**Author:** Claude (Opus 4.8) · **Date:** 2026-07-08 · **Status:** Stage-2 synthesis. Built from the
five Stage-1 files (all primary-source-verified this cycle):
`requirement/vaccine_requirement.md` (1a), `exemptions/titers_and_immunity.md` (1b),
`exemptions/medical_contraindication.md` (1c), `exemptions/religious_waiver_i601.md` (1d),
`exemptions/refusal_and_risks.md` (1e).

> ⚠️ **NOT legal or medical advice.** Decision-support for BAL (Berry Appleman & Leiden) and a
> licensed physician / civil surgeon. Confidence tags: **VERIFIED** = traced live this cycle to a
> primary official source (USCIS Policy Manual / Form I-693 PDF / CDC civil-surgeon Technical
> Instructions / US Code); **ASSUMED** = strong inference from verified material; **UNVERIFIED** =
> lead only, do not rely on.
>
> ⚠️ **GUARDRAIL (non-negotiable).** Every door below is legitimate ONLY on literally true facts —
> a real positive titer, a genuine physician-judged contraindication, a sincere categorical belief,
> or a correctly-recorded refusal. A material misrepresentation on the I-693/I-485 is an
> **INA 212(a)(6)(C)(i) lifetime bar** that Hooman almost certainly **cannot** waive (no USC/LPR
> spouse/parent; wife is a co-applicant; unborn child does not count — 1e §3.7). That downside is
> categorically worse than any vaccine. No cell in this map may be reached by overstating a fact.

---

## 0. Headline (read this first)

1. **COVID-19 is gone — no shot, no titer, no waiver.** USCIS stopped enforcing it for any I-485
   pending on/after Jan 20, 2025; CDC struck it from the civil-surgeon list Mar 11, 2025. Hooman's
   central fear is resolved at the *requirement* level before any door is opened. The leftover
   COVID row on the 01/20/25 I-693 PDF is a harmless form-lag artifact. **[VERIFIED — 1a]**

2. **Two self-executing "no new shot, no I-601" doors carry the whole strategy:**
   **(H2) titer / prior-immunity** and **(H3) medical contraindication** (Hooman's LGL/
   immunosuppression; wife's pregnancy). Both are recorded by the civil surgeon on Form I-693 and
   granted with no separate waiver application. **[VERIFIED — 1a, 1b, 1c]**

3. **The contraindication door (H3) only closes LIVE vaccines** — MMR, varicella, LAIV. It does
   **nothing** for the inactivated vaccines, which are safe in both pregnancy and immunosuppression.
   **[VERIFIED — 1c]**

4. **The honest pinch point for BOTH of them is Td/Tdap** (tetanus/diphtheria/pertussis): it has
   **no titer path**, it is **inactivated** (so neither LGL nor pregnancy contraindicates it), and a
   booster is due if the last dose was >10 years ago. If neither spouse has a dated Td/Tdap dose
   within 10 years, **this one shot may be genuinely unavoidable by any truthful door.** See §4.
   **[VERIFIED — 1b, 1c]**

5. **The religious/moral waiver (H4) is a demoted reserve, not a plan.** Hooman's vaccination
   history + COVID-specific objection is the "pick-and-choose" profile the "opposed to all vaccines
   in any form" test rejects; forcing it would risk the misrepresentation bar. **[VERIFIED test — 1d]**

---

## 1. The rows: what is actually required for two adults

Current required list = **15 diseases** (COVID-19 removed). Two of them auto-fall-away for adults as
**"not age-appropriate"** (a self-executing blanket waiver in its own right). "Live?" drives whether
the H3 contraindication door can touch the row. **[VERIFIED disease list & IPV=inactivated — CDC,
1a; full live/inactivated split — CDC Pinkbook Ch.2 + pregnancy guidance, 1c.]**

| # | Vaccine (disease) | Live? | Titer path? | Adult status |
|---|---|---|---|---|
| 1–3 | **Td/Tdap** (tetanus, diphtheria, pertussis) | Inactivated | **No** | Required; booster if >10 yr |
| 4 | **Polio (IPV)** | Inactivated | Yes (all 3 types) | Required (adult catch-up) |
| 5–7 | **MMR** (measles, mumps, rubella) | **LIVE** | Yes | Required |
| 8 | **Rotavirus** | Live | No | **Not age-appropriate** (infant only) → auto-cleared |
| 9 | **Hib** | Inactivated | No | **Not age-appropriate** (pediatric) → auto-cleared |
| 10 | **Hepatitis A** | Inactivated | Yes | Required |
| 11 | **Hepatitis B** | Inactivated | Yes | Required (adults 19–59) |
| 12 | **Meningococcal** | Inactivated | No | Age/risk-based → likely not-age-appropriate for adults* |
| 13 | **Varicella** | **LIVE** | Yes (+ disease history "VH") | Required |
| 14 | **Pneumococcal** | Inactivated | No | Age/risk-based → likely not-age-appropriate for adults* |
| 15 | **Influenza** | IIV inactivated (LAIV is live) | No | Required in season; "not flu season" defers |
| — | ~~COVID-19~~ | — | — | **REMOVED** — not required at all |

\* Exact adult age cut-offs for meningococcal/pneumococcal (CDC "Table 1 — Vaccine Requirements
According to Applicant Age") were **not fully extracted** in Stage 1 — **[UNVERIFIED, open item]**.
For a typical healthy adult outside the risk/age band these are expected to clear as
"not age-appropriate," but confirm each spouse's age band and risk factors with the civil surgeon.

---

## 2. THE MATRIX — does each door clear each vaccine?

**Doors (columns):**
- **H2 Titer/Immunity** — positive serologic titer OR a valid dated prior-vaccination record (or, for
  varicella, reliable disease history). Recorded in the I-693 "Complete Series" column (write lab-test
  date / "VH" / "X"). Self-executing, no waiver form. [1b]
- **H3-H Contraindication (Hooman / LGL-immunosuppression)** — civil-surgeon "not medically
  appropriate → contraindication" mark; live vaccines only; hinges on his hematologist judging his
  disease/treatment "severe immunosuppression." Self-executing blanket waiver, no I-601. [1c]
- **H3-W Contraindication (wife / pregnancy)** — same mechanism; live vaccines only; must be pregnant
  **at the time of the exam**. Self-executing, no I-601. [1c]
- **H4 Religious/Moral waiver** — INA 212(g)(2)(C), Form I-601, fee, discretionary. Requires categorical
  "opposed to all vaccines in any form" + sincerity. [1d]
- **H5 Refusal** — no waiver; civil surgeon records requirement not met → inadmissible under
  INA 212(a)(1)(A)(ii). Curable, but a failure state, not a clearance. [1e]

Legend: **YES** = clears the requirement with no shot · **NO** = does not clear ·
**MAYBE** = clears only if a stated condition is genuinely met.

| Vaccine | H2 Titer/Immunity | H3-H Hooman (LGL) | H3-W Wife (pregnancy) | H4 Religious/Moral (I-601) | H5 Refusal | Also |
|---|---|---|---|---|---|---|
| **Td/Tdap** (tet/diph/pert) | **MAYBE** — no titer; only a **dated dose ≤10 yr** clears (record). If >10 yr → due. `[VERIFIED]` | **NO** — inactivated, not contraindicated by immunosuppression `[VERIFIED]` | **NO** — inactivated; Tdap is *recommended* in pregnancy `[VERIFIED]` | MAYBE (only if genuine categorical objection) — weak `[VERIFIED test]` | Fails req → inadmissible `[VERIFIED]` | Individual contraindication only if a *real* clinical one (e.g. documented severe reaction to prior dose) — physician call |
| **Polio (IPV)** | **YES** — titer (all 3 types) OR dated record `[VERIFIED]` | **NO** — inactivated `[VERIFIED]` | **NO** — inactivated `[VERIFIED]` | MAYBE — weak `[VERIFIED]` | Fails req `[VERIFIED]` | — |
| **Measles (MMR)** | **YES** — titer OR dated record `[VERIFIED]` | **MAYBE** — YES if hematologist certifies severe immunosuppression `[VERIFIED rule]` | **MAYBE** — YES if pregnant at exam `[VERIFIED rule]` | MAYBE — weak `[VERIFIED]` | Fails req `[VERIFIED]` | — |
| **Mumps (MMR)** | **YES** `[VERIFIED]` | **MAYBE** (as measles) | **MAYBE** (as measles) | MAYBE — weak | Fails req | — |
| **Rubella (MMR)** | **YES** `[VERIFIED]` | **MAYBE** (as measles) | **MAYBE** (as measles) | MAYBE — weak | Fails req | — |
| **Varicella** | **YES** — titer OR dated record OR **reliable disease history ("VH")** `[VERIFIED]` | **MAYBE** — YES if severe immunosuppression certified `[VERIFIED rule]` | **MAYBE** — YES if pregnant at exam `[VERIFIED rule]` | MAYBE — weak | Fails req | Disease-history route is the cheapest of all if either had chickenpox |
| **Hepatitis A** | **YES** — titer OR dated record `[VERIFIED]` | **NO** — inactivated `[VERIFIED]` | **NO** — inactivated `[VERIFIED]` | MAYBE — weak | Fails req | — |
| **Hepatitis B** | **YES** — anti-HBs titer OR dated record `[VERIFIED; anti-HBs marker ASSUMED]` | **NO** — inactivated `[VERIFIED]` | **NO** — recommended in pregnancy `[VERIFIED]` | MAYBE — weak | Fails req | Confirm surgeon accepts standard anti-HBs titer `[open Q]` |
| **Influenza** | **MAYBE** — no titer; dated in-season record clears `[VERIFIED]` | **NO** for the requirement — LAIV(live) contraindicated but IIV(shot) still available `[VERIFIED]` | **NO** for the requirement — IIV recommended in pregnancy `[VERIFIED]` | MAYBE — weak | Fails req | **"Not flu season" blanket waiver defers it** — schedule exam off-season `[VERIFIED]` |
| **Meningococcal** | NO titer `[VERIFIED]` | **NO** — inactivated `[VERIFIED]` | **NO** — inactivated `[VERIFIED]` | MAYBE — weak | Fails req | **Not age-appropriate** for most adults → auto-clear `[VERIFIED mechanism; adult cut-off UNVERIFIED]` |
| **Pneumococcal** | NO titer `[VERIFIED]` | **NO** — inactivated `[VERIFIED]` | **NO** — inactivated `[VERIFIED]` | MAYBE — weak | Fails req | **Not age-appropriate** for most adults → auto-clear `[VERIFIED mechanism; adult cut-off UNVERIFIED]` |
| **Hib** | (n/a) | NO | NO | — | — | **Not age-appropriate** (pediatric) → auto-clear `[VERIFIED]` |
| **Rotavirus** | (n/a) | NO | NO | — | — | **Not age-appropriate** (infant only) → auto-clear `[VERIFIED]` |
| ~~COVID-19~~ | n/a | n/a | n/a | n/a | n/a | **Not required** — removed `[VERIFIED]` |

**How to read the matrix in one line:** the LIVE rows (MMR ×3, varicella) have **two** truthful doors
each (titer *and* contraindication); the inactivated titer-eligible rows (polio, Hep A, Hep B) have
**one** strong door (titer/record); Td/Tdap has **only** the record door (and it expires at 10 years);
influenza is cleared by **timing** (off-season) or an in-season record; meningococcal/pneumococcal/
Hib/rotavirus fall away on **age**. The contraindication door is powerful but never touches an
inactivated vaccine.

---

## 3. Scoring the doors (research-plan §3 scorecard)

Weights: Certainty of clearing 30% · No new shots 25% · Low legal risk 20% · Speed/friction 15% ·
Durability 10%. Scores 1–5, weighted total out of 5.

| Door | Certainty (30%) | No-shot (25%) | Low legal risk (20%) | Speed (15%) | Durability (10%) | Weighted | Verdict |
|---|---|---|---|---|---|---|---|
| **H2 Titer / prior record** | 5 | 5 (if immune) | 5 | 5 | 5 | **5.0** | **Lead door.** Genuine lab/record = zero misrep exposure; permanent; self-executing. |
| **H3 Contraindication** (LGL / pregnancy) | 5 | 5 (live only) | 4 | 5 | 5 | **4.8** | **Co-lead for live vaccines.** Only caveat: must be genuine physician judgment (guardrail seam). Partial — live only. |
| **Not-age-appropriate / not-flu-season** | 5 | 5 | 5 | 5 | 5 | **5.0** | Self-executing, objective; handles Hib/rotavirus (both) + likely mening./pneumo. + flu timing. |
| **H4 Religious/Moral (I-601)** | 2 | 4 (if granted) | 2 | 2 | 3 | **2.4** | **Reserve only.** Discretionary; Hooman fails the "any form" gate; sincerity fight is itself a misrep trap. |
| **H5 Refusal** | 1 | 5 | 3 | 1 | 1 | **2.1** | **Failure state,** not a clearance. Last resort; converts to inadmissibility until cured. |

**Ranking:** H2 ≈ age/season blanket ≈ H3 (all self-executing, truthful, free) ≫ H4 ≫ H5.

---

## 4. RECOMMENDED PATH — HOOMAN

**Objective:** clear all 15 rows with the fewest new shots and lowest legal risk. Chain doors in this
order; a shot is a last resort only where no truthful door reaches.

**Step 0 — COVID-19:** nothing to do. Not required. Expect to see a stale COVID row on the PDF; BAL/
surgeon disregard it per CDC. **[VERIFIED]**

**Step 1 — Age/pediatric auto-clears (no shot, no titer):** Hib and rotavirus → **not age-appropriate**.
Meningococcal and pneumococcal → **not age-appropriate** for a typical healthy adult (confirm his age
band/risk factors with the surgeon). **[VERIFIED mechanism; adult cut-offs UNVERIFIED — open item]**

**Step 2 — Pull every dated immunization record first (free, zero-risk).** Childhood/school, prior
physicals, travel/employer clinics, Canadian records — anything with month/day/year, unaltered. Any
disease with a valid dated complete series is cleared by record: **no shot, no titer.** This is the
cheapest door and it also fixes the Td/Tdap and influenza rows if a recent dated dose exists. **[VERIFIED]**

**Step 3 — Titers for the 7 titer-eligible diseases (one blood draw):** measles, mumps, rubella,
varicella, hepatitis A, hepatitis B, polio (all 3 types). Positive result clears each with **no shot**;
surgeon writes the lab-test date in "Complete Series." Given "various vaccines over his life," this is
very likely to clear MMR, varicella, and (if he was vaccinated/exposed) Hep A/B and polio. For
varicella, a reliable **disease history ("VH")** clears it with neither shot nor titer. **[VERIFIED]**

**Step 4 — Contraindication backstop for the LIVE rows only (MMR, varicella):** if any live-vaccine
titer comes back **non-immune**, the fallback is his **LGL/immunosuppression contraindication** —
*if and only if* his hematologist genuinely judges his disease/treatment to be "severe
immunosuppression / altered immunocompetence," and the civil surgeon marks it. Self-executing, no
I-601, durable for this application. This is what guarantees he never needs a live shot even if a
titer fails. **[VERIFIED rule; the clinical determination is the physician's — guardrail]**

**Step 5 — Influenza:** clear by **scheduling the exam outside flu season** ("not flu season" blanket
waiver) or by a dated in-season flu-shot record. LAIV(live) would be contraindicated by his condition,
but that alone does **not** excuse flu because the inactivated shot exists — so use timing/record, not
contraindication. **[VERIFIED]**

**Step 6 — The residual pinch points (honest flags):**
- **Td/Tdap — the hardest row.** No titer. Inactivated, so **neither LGL nor any contraindication door
  applies** in the ordinary case. If his last tetanus/Tdap dose is **within 10 years and documented**,
  Step 2 clears it. **If it is >10 years ago (or undocumented), no truthful self-executing door
  reaches it** — a single Td/Tdap booster may be **genuinely unavoidable**, absent (a) a real
  individual medical contraindication his physician would certify (e.g., documented history of a
  severe/anaphylactic reaction or Guillain-Barré after a prior dose — a real clinical fact, not
  manufacturable), or (b) a genuine categorical religious/moral objection (H4, which he likely does
  not truthfully hold). **This is the row most likely to require one shot. [VERIFIED analysis]**
- **Hep A / Hep B / Polio** — strong door (titer/record), but if a titer is **negative** *and* there is
  no dated record, there is **no contraindication fallback** (inactivated). Those would then require the
  shot(s). Likelihood depends on his actual immunity/records. **[VERIFIED]**

**Fallback chain if a door fails:** record → titer → (live only) contraindication → *(genuine only)*
individual medical contraindication or religious/moral I-601 → shot. Do **not** escalate to H4/refusal
for a single inactivated shot he has no truthful exemption for; taking that one shot is lower-risk than
a discretionary or insincere waiver.

**Net for Hooman:** realistically **0 shots** if (a) titers show immunity to the live + Hep/polio rows
and (b) he has a Td/Tdap dose within 10 years. **Most probable single unavoidable shot: Td/Tdap** if
his last booster is stale. Everything else is coverable by truthful self-executing doors.

---

## 5. RECOMMENDED PATH — WIFE (pregnant, co-applicant, own I-693)

**Same funnel, one timing rule that dominates:** her pregnancy contraindication is anchored to being
**pregnant at the time of her exam**. To use it, her I-693 exam should be done **while she is still
pregnant**, with the contraindication box marked then. USCIS will not require those live vaccines later
even after delivery, *if the exam captured the pregnancy.* **[VERIFIED — 1c]**

**Step 0 — COVID-19:** not required. **[VERIFIED]**

**Step 1 — Age/pediatric auto-clears:** Hib, rotavirus → not age-appropriate; meningococcal/
pneumococcal likely not age-appropriate (confirm her age band/risk). **[VERIFIED mechanism]**

**Step 2 — Records:** pull all dated prior doses (same as Hooman Step 2). Clears any documented row,
including Td/Tdap and flu if recent. **[VERIFIED]**

**Step 3 — Live rows (MMR, varicella): two truthful doors, both available.**
- **(a) Pregnancy contraindication (H3-W)** — clean, self-executing, works even if her immunity is
  unknown, *provided the exam is done while pregnant.* **[VERIFIED]**
- **(b) Titers** — more **durable** (immunity doesn't end with pregnancy) and avoids any timing
  dependency. Recommended to run titers anyway; use pregnancy contraindication as the backstop for any
  live row that titers show non-immune. **[VERIFIED]**

**Step 4 — Titer-eligible inactivated rows (polio, Hep A, Hep B):** titer or dated record. No pregnancy
fallback (inactivated/safe/recommended in pregnancy), so a negative titer + no record → shot. **[VERIFIED]**

**Step 5 — Influenza:** off-season exam ("not flu season") or dated in-season record. Note the
inactivated flu shot is *recommended* in pregnancy, so pregnancy does not excuse it — use timing/record.
**[VERIFIED]**

**Step 6 — Residual pinch point — Td/Tdap:** identical to Hooman, and **sharper for her**: Tdap is
*recommended every pregnancy*, so pregnancy is the opposite of a contraindication here; no titer path.
If she lacks a dated Td/Tdap within 10 years, a booster may be **genuinely unavoidable** unless a real
individual contraindication exists. **[VERIFIED]**

**Fallback chain:** record → titer → (live only) pregnancy contraindication → *(genuine only)*
individual medical contraindication → shot.

**Net for the wife:** live rows are the **easiest** part of her case (pregnancy door + titers both
work). Her exposure is the **same inactivated pinch points** as Hooman — chiefly Td/Tdap if stale, and
any inactivated row where she is non-immune with no record. **Key logistics ask for BAL: schedule her
I-693 while she is still pregnant** so the contraindication is captured.

---

## 6. Requirements NO legitimate door clears (honest flags — where a shot may be unavoidable)

These are the rows where, on certain fact patterns, **no truthful exemption reaches** and a single
shot is the lowest-risk truthful option. We flag them rather than pretend a door exists.

1. **Td/Tdap (both spouses)** — **[VERIFIED]** No titer; inactivated (no immunosuppression/pregnancy
   contraindication); booster due at 10 years. If the last dose is >10 years old or undocumented, the
   only doors left are a *genuine* individual medical contraindication (a real severe-reaction/GBS
   history — physician's call, not manufacturable) or a *genuine* categorical religious/moral objection
   (H4 — Hooman likely fails the "any form" test). **Absent those, one Td/Tdap shot each is the honest,
   lowest-risk outcome.** This is the single most likely unavoidable shot in the whole case.

2. **Hep A / Hep B / Polio (either spouse)** — **[VERIFIED]** Strong titer/record door, but purely
   fact-dependent: if a titer is negative AND no dated record exists, there is no contraindication
   fallback (inactivated). Then the shot(s) are required. Probability unknown until titers/records are in.

3. **Influenza (either spouse)** — **[VERIFIED, low severity]** Cleared by off-season timing or an
   in-season record; if the exam must occur in flu season and there is no record, the inactivated flu
   shot is required (contraindication does not excuse it — only LAIV is contraindicated). Usually
   avoidable by scheduling.

**Not flagged (confidently clearable, no shot):** COVID-19 (removed); Hib, rotavirus (not
age-appropriate); MMR ×3 and varicella (titer OR contraindication — two doors each); meningococcal,
pneumococcal (expected not-age-appropriate for adults — confirm age band).

---

## 7. Consolidated open items to route to BAL / physician (from all Stage-1 files)

**To the hematologist (Hooman):** Does his LGL leukemia and/or its treatment meet the CDC/ACIP
**"severe immunosuppression / altered immunocompetence"** threshold, so a civil surgeon can in good
faith mark MMR/varicella (and LAIV) as contraindicated? What documentation supports it? *(Hinge for
H3-H; must be genuinely true.)* **[1c]**

**To the civil surgeon:** (a) Will they accept a treating-hematologist's letter as the basis for the
contraindication mark and annotate it? (b) Do they accept a standard **anti-HBs** titer as evidence of
Hep B immunity? (c) Confirm they use the **01/20/25** I-693 edition. **[1b, 1c]**

**To BAL:** (a) **Schedule the wife's I-693 while she is still pregnant** (pregnancy-at-exam rule) —
confirm her co-applicant status and I-693 timeline. (b) Confirm Hooman has **no USC/LPR spouse/parent**
qualifying relative (determines that a 212(a)(6)(C)(i) finding would be unwaivable — reinforces the
guardrail). (c) Exact RFE-vs-denial procedure and whether a waiver can still cure after an RFE. (d) Does
BAL consider the religious/moral I-601 viable for a client with a prior-vaccination record (house view)?
**[1c, 1d, 1e]**

**To verify LIVE before filing (uscis.gov blocks this environment — Stage-1 read via Wayback/proxy):**
re-confirm USCIS Policy Manual Vol.8 Pt.B Ch.9 and the CDC civil-surgeon page on the live site near the
exam date; confirm the I-693 edition is still 01/20/25; pull the current I-601 fee/edition if H4 is ever
touched. **[1a, 1b, 1d]**

**Still UNVERIFIED (don't let drive a recommendation):** exact ACIP dose counts for a "complete series"
per disease; precise adult age cut-offs for meningococcal/pneumococcal (CDC Table 1). **[1b]**

**Citation correction to propagate:** the vaccination waiver is **INA 212(g)(2)(C)**, not "212(g)(1)(C)"
as written in `research-plan.md` (H3/H4) — 212(g)(1) is the communicable-disease waiver. **[VERIFIED — 1d, 1e]**

---

## 8. One-paragraph bottom line

COVID-19 is off the table entirely. For everything else, the strategy is: **records first, titers
second, contraindication third (live rows only), shot last** — and for the wife, **do her exam while
pregnant** to capture the live-vaccine contraindication. If titers show the immunity his history
suggests, and if each spouse has a Td/Tdap dose within the last 10 years, **both can plausibly reach
zero new shots** through truthful, self-executing doors that need no I-601. The one row that may
genuinely force a single shot each is **Td/Tdap** (no titer, inactivated, 10-year booster) if their
last dose is stale — and taking that one shot is a lower-risk truthful outcome than a discretionary
religious/moral waiver or a refusal. Nothing in this map may be reached by overstating a fact.
