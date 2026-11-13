# Topic 3a — Civil Surgeon Discretion & Mechanics (who decides what, and how the form moves)

**Task (research-plan §2, Stage 3a):** Map how much latitude a civil surgeon has to (a) accept
titers / prior records, (b) document a medical contraindication (blanket waiver), and (c) record a
refusal — versus what **only USCIS** can adjudicate (chiefly the I-601 religious/moral waiver). Cover
the **sealed-envelope** process, the **I-693 validity window**, and current **edition** mechanics.
Grounded in the CDC Vaccination Technical Instructions for Civil Surgeons and the USCIS Policy Manual.

**Author:** Claude (Opus 4.8) · **Date:** 2026-07-08 · **Status:** Stage-3 research complete for this
topic. Builds on Stage-1 files (1a `requirement/vaccine_requirement.md`, 1c
`exemptions/medical_contraindication.md`) and Stage-2 `exemptions/decision_map.md`.

> ⚠️ **NOT legal or medical advice.** Decision-support for BAL (Berry Appleman & Leiden) and a licensed
> physician / civil surgeon. The *clinical* judgment (is this a genuine contraindication?) belongs to
> the physician; the *legal* adjudication belongs to USCIS. This file maps the division of labor.
>
> ⚠️ **GUARDRAIL.** Everything below is legitimate only on literally true facts. A civil surgeon's
> latitude is real but bounded: they may record a genuine titer, a genuine contraindication, or a
> genuine refusal — they may **not** manufacture any of them, and USCIS can and does police fabricated
> or tampered forms (see §5, §7). A false notation → INA 212(a)(6)(C)(i) lifetime bar. See CLAUDE.md §5.

> ⚙️ **Sources verified LIVE this session (2026-07-08):**
> - **CDC "Vaccination Technical Instructions for Civil Surgeons"** — fetched **directly** (HTTP 200),
>   https://www.cdc.gov/immigrant-refugee-health/hcp/civil-surgeons/vaccination.html
> - **USCIS Policy Manual Vol. 8, Part B, Ch. 9 "Vaccination Requirement"** — via Wayback (uscis.gov
>   blocks the bot), snapshot of the live page marked **"Current as of May 08, 2026."**
>   https://www.uscis.gov/policy-manual/volume-8-part-b-chapter-9
> - **USCIS Policy Manual Vol. 8, Part B, Ch. 4 "Review of Medical Examination Documentation"** — via
>   Wayback, same "Current as of May 08, 2026." https://www.uscis.gov/policy-manual/volume-8-part-b-chapter-4
> All quotations below were read from these live/near-live copies this session. **[VERIFIED]** unless
> marked otherwise. Re-verify on the live site near the exam date.

---

## 0. Bottom line (the division of labor in one paragraph)

The civil surgeon is the **gatekeeper of the facts**, not the adjudicator of the law. Within the exam,
the surgeon has broad, USCIS-respected latitude to **(a) credit existing immunity** — accepting dated
prior-vaccination records and recording serologic (titer) proof of immunity in the "Complete Series"
column; **(b) document a medical contraindication**, which USCIS treats as a **self-executing blanket
waiver requiring NO separate application (no I-601)** and to which the adjudicating officer "should
usually defer … because such a finding involves medical judgment"; and **(c) record a refusal**, which
the surgeon documents but which is a **failure state**, not a clearance. What the surgeon **cannot** do
is grant the **religious/moral waiver** — that is an *individual* waiver the surgeon merely *flags* by
checking a box; the applicant must then file **Form I-601** and **USCIS alone adjudicates it**. The
completed form travels to USCIS in a **sealed envelope** the applicant may not open, and (for forms
signed on/after Nov 1, 2023) is valid for the **entire pendency of the associated application** with no
fixed expiry. **[VERIFIED — CDC TI; PM Ch. 9 §B; PM Ch. 4]**

---

## 1. What the civil surgeon CAN do inside the exam (the three self-executing doors)

The CDC Technical Instructions define the surgeon's job precisely (verbatim, read this session):

> "Determine the vaccines the applicant needs based on his or her age, records, documented immunity,
> and information provided in Table 1. **Assess for contraindications and precautions** that might apply
> to the applicant. Administer vaccines, if indicated. **Complete the applicant's Form I-693 and give it
> to the applicant in a sealed envelope** for USCIS, in addition to a copy for the applicant to keep."
> — CDC TI, "Determining the Vaccines the Applicant Needs." **[VERIFIED]**

### 1a. (a) Accept titers / prior records — the immunity door (H2)

The surgeon has full authority to credit existing immunity two ways, **without** giving any shot:

- **Documented prior vaccination.** CDC TI, "Review of Vaccination Records" (verbatim): "The civil
  surgeon should instruct the applicant to submit **all available written records** of vaccination
  history for review. Acceptable vaccination documentation must come from a vaccination record … Only
  those records of vaccine doses that include the **dates of receipt (month, day, and year)** are
  acceptable. **The document must not appear to have been altered**, and dates of vaccinations should
  seem reasonable. **Self-reported vaccine doses without written documentation are not acceptable.**"
  Foreign records are acceptable if consistent with ACIP schedules; the **applicant** bears the burden
  of supplying reliable **English translations.** **[VERIFIED]**
  - *Latitude/limit:* the surgeon decides whether a record is acceptable (dated, unaltered, reasonable).
    Broad discretion to **accept**, but records that are undated, altered, or self-reported **must** be
    rejected — this is a hard rule, not discretion. This is a guardrail seam: an unaltered dated record
    is the safest door of all; an "adjusted" record is exactly the misrepresentation trap.

- **Serologic proof of immunity (titers).** CDC TI, "Laboratory Confirmation of Immunity" (verbatim):
  "Laboratory evidence of immunity is acceptable for **measles, mumps, rubella, hepatitis A, hepatitis
  B, polio, and varicella** if the applicant lacks acceptable documented history of vaccination for
  these diseases. **Titers must include all three poliovirus types to be acceptable.**" Tests must use
  "**FDA-approved kits or CLIA-certified kits.**" **[VERIFIED]**
  - **Varicella special case (cheapest door):** "An applicant who provides a **reliable written or oral
    history of varicella disease does not require laboratory confirmation or further vaccination.**" To
    accept it the surgeon inquires about (1) an epidemiologic link to another typical/lab-confirmed case
    or (2) lab confirmation at the time of acute disease. This is recorded as **"VH"** in the chart.
    Note: this is the **one place CDC lets the surgeon accept an *oral* history** — everything else needs
    a dated written record or a lab test. **[VERIFIED]**
  - *Where it lands on the form:* the immunity/titer result is written in the **"Complete Series"**
    column of the Part 10 chart (mark "X" if complete; **write the date of the lab test if immune**; or
    "VH" for varicella history). Recording it there **satisfies the requirement with no shot and no
    waiver.** **[VERIFIED — I-693 01/20/25 Part 10, Stage-1 1a.]**

### 1b. (b) Document a medical contraindication — the blanket-waiver door (H3)

This is the surgeon's strongest lever and the one USCIS most defers to.

- **It is self-executing — no I-601, no separate application.** CDC TI, "Waivers and Documenting"
  (verbatim): "the applicant can still be considered to have completed the … vaccination requirements
  by means of a **Blanket Waiver.** The civil surgeon needs to document the appropriate Blanket Waiver
  reason for each vaccine not given on the Form I-693, and **the waiver will be granted to the applicant
  if documented correctly. The applicant does not need to apply for a Blanket Waiver.**" **[VERIFIED]**

- **The four "Not Medically Appropriate" reasons** (CDC TI, verbatim list): **(1) Not age-appropriate**
  — "For all applicants, this reason will need to be documented for at least one vaccine" (e.g. adults
  and Hib/rotavirus); **(2) Contraindication** — "If an applicant has contraindications or precautions
  to specific vaccines"; **(3) Insufficient time interval between doses** (incl. spacing two live
  vaccines); **(4) Influenza vaccine not available** ("Not flu season"). **[VERIFIED]**

- **USCIS's definition of "contraindication" (this is the bar the physician must genuinely meet).** PM
  Vol. 8 Pt. B Ch. 9 §B.1 (verbatim): "A contraindication is a condition in a recipient which is likely
  to result in a **life-threatening problem if the vaccine is given.** Examples of contraindications
  include **a severe allergic reaction to a vaccination that was previously given, or pregnancy.**"
  **[VERIFIED]** — Note the framing is stringent ("life-threatening"); for the live-vaccine rows the
  operative clinical concept is CDC's "severe immunosuppression is a contraindication to live vaccines"
  (Hooman/LGL) and "live vaccines are contraindicated during pregnancy" (wife) — see 1c. The surgeon
  transcribes the physician's judgment; the surgeon does not invent it.

- **The officer must usually defer to it.** PM Ch. 9 §B (verbatim): "An officer … **should usually defer
  to a civil surgeon's finding that a vaccine is not medically appropriate because of a
  contraindication. This is because such a finding involves medical judgment.**" **[VERIFIED]** — This
  is the sharp contrast with the objectively-checkable reasons (see §2): the officer *can* overrule
  "not age appropriate" / "not flu season" on the face of the dates, but a contraindication gets
  deference.

- **The reason annotation is optional for RFE purposes.** PM Ch. 9 (verbatim): "the specific reason for
  the contraindication may be annotated by the civil surgeon on the Form I-693; however, **if it is
  omitted, the officer does not need to issue a Request for Evidence (RFE) solely for that omission as
  long as the contraindication is marked in the vaccine chart.**" **[VERIFIED]** (Best practice is still
  to annotate, and to attach the hematologist's letter — see §6.)

- **It is effectively permanent for THIS application.** PM Ch. 9 (verbatim): "An officer should **never
  issue an RFE for additional vaccines even if, at the time of the adjudication … the applicant is no
  longer immuno-compromised.** As long as the vaccination assessment was properly completed at the time
  of the examination by the civil surgeon, the … assessment can be accepted." And for pregnancy: "An
  officer should also **never issue an RFE for additional vaccines if the applicant is no longer
  pregnant at the time of the adjudication.**" **[VERIFIED]** — This is the durability guarantee: the
  contraindication is assessed **as of the exam date** and does not "reopen" if the condition later
  resolves. (Directly load-bearing for the wife's timing rule — see §3 and 1c §3c.)

### 1c. (c) Record a refusal — the failure-state "door" (H5)

The surgeon documents refusal but it does not clear anything. CDC TI (verbatim): "**Applicant refuses a
vaccine.** If an applicant's vaccine history is incomplete and the applicant **refuses a single dose of
any required vaccine that is medically appropriate** for the applicant, it should be documented that
the **vaccine requirements are not complete and that the applicant refuses vaccination.**" **[VERIFIED]**

On the I-693 this drives the third Results box — **"Applicant does not meet immunization requirements"**
— which leads to inadmissibility under INA 212(a)(1)(A)(ii) unless a waiver is granted (see 1e). The
surgeon has **no latitude to convert a refusal into a clearance**; refusal of a *medically appropriate*
required vaccine is, by definition, the thing that fails the requirement. **[VERIFIED — CDC TI; 1e.]**

---

## 2. What the civil surgeon CANNOT decide — reserved to USCIS

| Question | Who decides | Basis |
|---|---|---|
| Is a claimed **contraindication** medically valid? | **Civil surgeon** (with treating physician's input); officer **defers** | CDC TI; PM Ch. 9 §B "defer … medical judgment" **[VERIFIED]** |
| Is a **titer / prior record** acceptable proof of immunity? | **Civil surgeon** (must be dated/unaltered/CLIA-FDA lab) | CDC TI "Review of Records" + "Lab Confirmation" **[VERIFIED]** |
| Is the applicant excused on **"not age-appropriate"** / **"not flu season"**? | Surgeon documents, but **officer can overrule on the face of the dates** | PM Ch. 9 §B: officer "should be able to clearly see whether the finding is correct" **[VERIFIED]** |
| Is a **religious/moral objection** sufficient to waive vaccines? | **USCIS ONLY** (Form I-601, discretionary). Surgeon merely **checks a box**. | CDC TI + PM Ch. 9 **[VERIFIED]** — see §2a |
| Is the overall applicant **admissible** on health grounds? | **USCIS officer** (the surgeon's I-693 is *evidence*, not the decision) | PM Ch. 4 "Burden of Proof" **[VERIFIED]** |
| Should a **valid** I-693 nonetheless be re-examined (changed condition / inaccuracy)? | **USCIS officer** (discretion to demand a new/updated form) | PM Ch. 4 "USCIS Discretion on Form I-693 Validity" **[VERIFIED]** |

### 2a. The religious/moral waiver is NOT the surgeon's to grant (critical boundary)

CDC TI (verbatim): "**Applicant may request a waiver based on religious or moral convictions.** If an
applicant objects to vaccination based on religious or moral convictions, it must be documented that
applicant is requesting an individual waiver based on religious or moral convictions. **This is not a
Blanket Waiver, and the applicant will have to submit a waiver request to USCIS.**" **[VERIFIED]**

USCIS PM Ch. 9 confirms the mechanics and adds a trap to know about (verbatim): the surgeon must check
the "**Applicant will request an individual waiver based on religious or moral convictions**" box; "This
is not a blanket waiver, and **the applicant will have to submit a waiver request on Form I-601.**"
Critically: "**Even if the applicant otherwise requires a blanket waiver(s), the civil surgeon must
check this box, and not the box titled 'Applicants may be eligible for blanket waivers.'** It may be,
however, that the civil surgeon checks **both** boxes, in which case the officer should just request the
waiver documentation that establishes the religious or moral" objection. **[VERIFIED]**

**Implication for Hooman's strategy:** checking the religious/moral box **pulls the case OUT of the
self-executing lane and INTO discretionary USCIS adjudication of an I-601.** This is exactly why the
decision map demotes H4 to a reserve: invoking it can *forfeit* the clean blanket-waiver posture unless
both boxes are checked, and even then it opens a sincerity/​"any form" fight (see `religious_waiver_i601.md`).
The surgeon cannot shield the applicant here — only USCIS can grant it, and only on the I-601. Keep the
case in the **blanket-waiver + titer** lane (boxes for contraindication/age/season + Complete-Series
immunity) and avoid checking the religious/moral box unless a genuine, deliberate I-601 is intended.

---

## 3. The two "Results" boxes vs. the third (how the surgeon's marks resolve)

Part 10 of Form I-693 (edition 01/20/25) ends with the civil surgeon checking one overall result
(Stage-1 1a read this from the PDF; the box semantics are confirmed by PM Ch. 9):

1. ☐ **"Applicant completed vaccination requirements or may be eligible for blanket waivers as indicated
   above."** ← the target. Covers **titers/records (Complete-Series column)** + **blanket waivers**
   (contraindication / not-age-appropriate / insufficient-interval / not-flu-season). **Self-executing.**
2. ☐ **"Applicant will request an individual waiver based on religious or moral convictions."** ← pulls
   into **I-601 / USCIS-only** adjudication (§2a). **Not self-executing.**
3. ☐ **"Applicant does not meet immunization requirements."** ← the **refusal / failure** box →
   inadmissibility until cured. **[VERIFIED — 1a from the PDF; PM Ch. 9 box language this session.]**

**Wife's timing rule restated in mechanics terms:** because a contraindication is assessed **as of the
exam date** and USCIS "should never issue an RFE … if the applicant is no longer pregnant at the time of
adjudication," her exam must be done **while she is pregnant** so the surgeon can mark the live-vaccine
(MMR, varicella, LAIV) contraindication into Result box #1. Post-partum, pregnancy no longer supplies
the contraindication and she'd fall back to titers. **[VERIFIED — PM Ch. 9; 1c §3c.]**

---

## 4. The sealed-envelope process (chain of custody)

- **Who seals it:** the **civil surgeon.** CDC TI (verbatim): "After administering any needed vaccines,
  the civil surgeon **must complete Form I-693 and give it to the applicant in a sealed envelope**, which
  the applicant will present to USCIS. **A copy of the completed vaccination record in Part 10 must also
  be provided to the applicant** for his or her personal records." **[VERIFIED]** — so the applicant
  keeps a **copy of Part 10** but the **original travels sealed.**
- **The applicant must NOT open it.** PM Ch. 4 lists, among the acceptance criteria, that "**The form
  must be in a sealed envelope as detailed in the form's instructions.**" **[VERIFIED]** If the envelope
  is opened, or the form/envelope shows signs of tampering, USCIS treats the form as deficient.
- **Tampering → RFE, not silent acceptance.** PM Ch. 4 (verbatim): "if there is evidence that the form or
  the envelope the form was placed in has been **tampered with**, the officer should issue an RFE to
  correct any Form I-693 deficiencies." **[VERIFIED]** — This is the enforcement backstop behind the
  guardrail: the sealed envelope + tamper rule is precisely how USCIS detects altered records.
- **How to fix a deficient form (RFE response) — two routes, both re-sealed by the surgeon.** PM Ch. 4
  (verbatim): the surgeon either "**annotates the original** … and both the applicant and the civil
  surgeon **re-sign and re-date**" and "**must place the corrected Form I-693 in a sealed envelope**,"
  **or** "**completes an entirely new Form I-693** … [and] must place the new Form I-693 in a sealed
  envelope," which the applicant then delivers. **[VERIFIED]** — Correctable, but always back through the
  surgeon and always re-sealed; the applicant can't self-edit.
- **Filing tip (mechanics, not our call):** because the applicant holds the sealed envelope, BAL/Hooman
  should confirm whether the I-693 is being **filed concurrently with the I-485** or **carried to the
  interview** — either is allowed; the point is the seal is intact when USCIS opens it.

---

## 5. Officer review — the boundary between "defer" and "second-guess"

PM Ch. 9 §B draws the line explicitly (verbatim): for **not-age-appropriate** and **not-flu-season**, "if
a vaccine was age appropriate at the time of the medical exam … but the civil surgeon marked that the
vaccine is not medically appropriate because it is not age appropriate, then **it is clear that the civil
surgeon's mark is incorrect. The same is true for … not flu season; the officer should be able to
clearly see whether the finding is correct based on the date of the medical examination.**" **[VERIFIED]**

By contrast (verbatim, again): "An officer, however, **should usually defer to a civil surgeon's finding
that a vaccine is not medically appropriate because of a contraindication. This is because such a
finding involves medical judgment.**" **[VERIFIED]**

**Flu-season nuance (an RFE that can arise even in the clean lane):** PM Ch. 9 (verbatim) — if flu vaccine
was required at the exam ("the date of the civil surgeon's certification governs") but the flu annotation
is missing, "the officer should **only** issue an RFE if it is **still the same flu season** and it is
reasonable to expect the applicant can obtain it within the RFE window." **[VERIFIED]** — Reinforces the
Stage-2 recommendation to **schedule the exam off-season** so flu is a "not flu season" blanket waiver.

**Net:** the surgeon's *medical* calls (contraindication, immunity) sit inside a zone of deference; the
surgeon's *objective/administrative* calls (age, season, dates, completeness, seal) are checkable and can
draw an RFE. This is why the decision map's lead doors (titer + contraindication) are strong: they land in
the deferred-to zone, provided they are genuine and correctly documented.

---

## 6. I-693 validity window + current-edition mechanics

### 6a. Validity window (how long a signed I-693 "lasts")

The rule turns on the **civil surgeon's signature date** and split at **November 1, 2023** (PM Ch. 4, all
verbatim, read this session):

- **Signed ON/AFTER Nov 1, 2023 (Hooman's case):** "a properly completed Form I-693 that is signed by a
  civil surgeon on or after November 1, 2023 **can only be used as evidence … for the entire period the
  immigration benefit application with which the Form I-693 is submitted is pending.**" **[VERIFIED]** →
  **No fixed expiry / no 2-year clock.** It stays valid for the whole pendency of the associated I-485.
  (This removed the old worry that a titer/contraindication finding could "age out" before adjudication.)
- **Signed BEFORE Nov 1, 2023:** "retains evidentiary value for **2 years from the date of the civil
  surgeon's signature.**" **[VERIFIED]** (Not applicable to Hooman's future exam — informational.)
- **The 60-day-before-filing signature rule was REMOVED.** PM Ch. 4 references that USCIS "permanently
  removed" the requirement that the surgeon's signature be dated no more than 60 days before filing.
  **[VERIFIED — historical policy-alert language on the page.]** So there is no longer a 60-day pre-filing
  signature window to satisfy.
- **USCIS retains discretion to demand a fresh form even when valid.** PM Ch. 4 (verbatim): "**Even in
  cases in which an applicant's Form I-693 is valid … if a USCIS officer has reason to believe that the
  applicant's medical condition has changed since the civil surgeon signed the Form I-693 or that the
  Form I-693 does not accurately reflect the applicant's medical condition** … then the officer **has the
  discretion to request further evidence or a new or updated Form I-693.**" **[VERIFIED]** — A latent risk
  worth flagging to BAL for a case involving an active hematologic condition, though it cuts toward *more*
  medical scrutiny, not toward forcing vaccines.

### 6b. Current-edition mechanics

- **Edition: `01/20/25`.** Confirmed in Stage-1 1a from the I-693 form page and PDF footer. **This is the
  only edition USCIS accepts for exams signed on/after July 3, 2025.** Hooman's exam will be well after →
  **must be the 01/20/25 edition.** **[VERIFIED — 1a.]**
- **The edition-lock rule (why a stale edition is generally fatal, and why it usually won't hurt Hooman).**
  PM Ch. 4 (verbatim): "As long as the civil surgeon complied with all procedures … and **used the edition
  of the form that was current on the date that they signed** Form I-693, the applicant's Form I-693 can
  be accepted as valid." And: an applicant "is not subject to any additional requirements that do not
  apply to them on the day the civil surgeon signed Form I-693 unless otherwise specified by the CDC.
  Therefore, officers should **not** issue an RFE … to meet requirements that did not apply … on the date
  the civil surgeon signed." **[VERIFIED]** — Two consequences: (1) using the current edition on exam day
  is mandatory; (2) the requirements are **frozen as of the signature date** (so, e.g., the COVID removal
  in force now applies; a *later* rule change won't retroactively demand more of a form already properly
  signed). "Prior editions … are generally not acceptable because they may lack required information."
- **The stale COVID-19 row on the 01/20/25 PDF is a harmless form-lag artifact** — CDC removed COVID from
  the required list (Mar 11, 2025) and USCIS stopped enforcing it (Jan 20, 2025); the paper form simply
  lags. Handled per CDC guidance, not by a shot. **[VERIFIED — 1a; decision_map §0.]**

---

## 7. Guardrail seams specific to the mechanics (where truthful ≠ convenient)

1. **Records must be dated + unaltered; oral history only counts for varicella.** CDC bars self-reported
   or altered records; the sealed envelope + tamper rule (§4) is USCIS's detector. An "improved" record is
   the classic 212(a)(6)(C) trap. **[VERIFIED]**
2. **Contraindication must be a genuine medical judgment.** The officer defers *because* it is medical
   judgment — which means the physician/surgeon must actually hold that judgment in good faith (Hooman's
   "severe immunosuppression" determination is the hematologist's to make — 1c §8). Deference is not a
   license to fabricate; a false contraindication is a false statement on the form. **[VERIFIED rule;
   clinical call reserved to physician.]**
3. **Checking the religious/moral box changes the legal posture** (§2a) — it forfeits the clean lane and
   invites I-601 sincerity scrutiny. Don't check it unless a genuine, deliberate I-601 is intended.
4. **Refusal is a documented failure, not a workaround** (§1c). The surgeon can't relabel a refusal of a
   medically-appropriate required vaccine as anything else. **[VERIFIED]**

---

## 8. Open items to route (from this topic)

- **[Civil surgeon — pre-screen, feeds 3b]** Confirm the office (a) uses the **01/20/25** edition; (b) will
  **accept a treating hematologist's contraindication letter** as the basis for the contraindication mark
  and annotate/attach it; (c) accepts standard **anti-HBs** titers and **all-three-type polio** titers from
  a CLIA/FDA lab; (d) will record a reliable **varicella disease history ("VH")** without a titer. **[1b/1c]**
- **[BAL]** Given PM Ch. 4 "USCIS Discretion" — does an active hematologic diagnosis raise any risk the
  officer demands an updated I-693, and does that change filing/timing? Confirm the I-693 filing vehicle
  (concurrent with I-485 vs. at interview) so the **sealed envelope** stays intact. Confirm the wife's exam
  is booked **while pregnant** (contraindication captured as of exam date). **[PM Ch. 4; §3]**
- **[Live re-verify before filing]** Re-open PM Ch. 9, PM Ch. 4, and the CDC civil-surgeon page on the live
  site near the exam date; confirm edition still 01/20/25 and the "Current as of" date has not moved with a
  substantive change. **[1a]**

---

## 9. Sources (primary, read live this session 2026-07-08)

- **CDC "Vaccination Technical Instructions for Civil Surgeons"** (dated Mar. 11, 2025 per 1a; fetched
  directly, HTTP 200). Sections used: "Determining the Vaccines the Applicant Needs," "Review of
  Vaccination Records," "Laboratory Confirmation of Immunity," "Waivers and Documenting Reasons for Not
  Giving a Vaccine" (four blanket-waiver reasons; religious/moral individual waiver; refusal), sealed
  envelope. https://www.cdc.gov/immigrant-refugee-health/hcp/civil-surgeons/vaccination.html **[VERIFIED]**
- **USCIS Policy Manual, Vol. 8, Part B, Ch. 9 "Vaccination Requirement"** — "Current as of May 08, 2026."
  Sections used: §B.1 (definition of "not medically appropriate" + contraindication definition), §B
  (officer deference vs. clear-error review; RFE rules for missing annotations, flu, pregnancy/immuno
  never-RFE-later), the individual religious/moral waiver box + I-601 routing.
  https://www.uscis.gov/policy-manual/volume-8-part-b-chapter-9 (via Wayback; uscis.gov blocks the bot).
  **[VERIFIED]**
- **USCIS Policy Manual, Vol. 8, Part B, Ch. 4 "Review of Medical Examination Documentation"** — "Current
  as of May 08, 2026." Sections used: acceptance criteria (signature, validity, sealed envelope),
  tampering → RFE, RFE-correction routes (annotate-and-reseal vs. new form), validity window (on/after Nov
  1 2023 = entire pendency; before = 2 years), removal of 60-day signature rule, edition-lock rule,
  requirements-frozen-at-signature, USCIS discretion to demand a new form.
  https://www.uscis.gov/policy-manual/volume-8-part-b-chapter-4 (via Wayback). **[VERIFIED]**
- **Form I-693, Edition 01/20/25** — Part 10 chart columns + three Results boxes (read in Stage-1 1a).
  https://www.uscis.gov/i-693 **[VERIFIED — 1a]**
