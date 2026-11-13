# Topic 1e — Refusal, Inadmissibility & the Misrepresentation Guardrail (the "what NOT to do" file)

Research subagent output. Last updated 2026-07-08 by Claude (Opus 4.8).
Owner: Hooman Shariati. **NOT legal or medical advice** — decision-support for BAL + a physician.

> Purpose of this file (per research-plan §2, Stage 1e): document (A) what happens if an
> applicant simply **refuses** a required vaccine with no granted waiver, and (B) the
> **INA 212(a)(6)(C)(i) permanent-bar** risk from any misrepresentation on the medical or
> benefit application — so that every *other* door (titers, contraindication, religious
> waiver) can be steered away from this line. This is the risk register, not a recommended path.

---

## 0. Bottom line (read first)

1. **Bare refusal is not a strategy — it is an admission of inadmissibility.** If a required,
   medically-appropriate vaccine is refused and no waiver is granted, the civil surgeon must
   record that the applicant **does not meet** the requirement, and the applicant becomes
   **inadmissible under INA 212(a)(1)(A)(ii)**. This blocks the green card unless a waiver
   (medical certification under 212(g)(2)(B), or religious/moral under 212(g)(2)(C)) is
   granted. [VERIFIED]

2. **The vaccination ground is fixable; the misrepresentation ground is not.** Being found
   inadmissible for a missing vaccine is *curable* — get the shot, prove immunity, get a
   contraindication certified, or win a waiver. By contrast, a finding of **fraud or willful
   misrepresentation under INA 212(a)(6)(C)(i) is a LIFETIME bar**, waivable only by a narrow
   212(i) hardship waiver limited to spouses/parents of USCs/LPRs. **The cure for a vaccine
   problem must never create a misrepresentation problem.** [VERIFIED]

3. **Guardrail restated:** every door we pursue must be truthful — a real contraindication
   certified by a physician, genuine documented immunity, a sincere religious/moral objection,
   or a correctly-recorded refusal. We never help fabricate an exemption or misstate a record.
   The downside of misrepresentation (permanent inadmissibility) is categorically worse than
   any vaccine. [Project guardrail — CLAUDE.md §5]

---

## 1. What refusal actually triggers (INA 212(a)(1)(A)(ii))

### 1.1 The statute
8 USC 1182(a)(1)(A)(ii) makes inadmissible any applicant for immigrant status or adjustment of
status "who has failed to present documentation of having received vaccination against
vaccine-preventable diseases" — the statute names *mumps, measles, rubella, polio, tetanus and
diphtheria toxoids, pertussis, influenza type B, and hepatitis B, and any other vaccinations
against vaccine-preventable diseases recommended by the Advisory Committee for Immunization
Practices [ACIP]*.
- Source: 8 USC 1182(a)(1)(A)(ii), Cornell LII, read 2026-07-07. [VERIFIED]
- Note: the *current* operational required list (and COVID-19 status) is Topic 1a's job; the
  ACIP catch-all is why the list changes without the statute changing.

### 1.2 What the civil surgeon does on refusal
USCIS Policy Manual, **Volume 8, Part B, Chapter 9 — Vaccination Requirement** (published
2025-05-13): if an applicant's vaccine history is incomplete and the applicant **refuses
administration of a single dose of any required vaccine that is medically appropriate**, the
civil surgeon records that the **applicant does not meet the immunization requirements**, and
**the applicant may be inadmissible** under INA 212(a)(1)(A)(ii).
- Source: USCIS PM Vol 8 Pt B Ch 9, via r.jina.ai proxy of uscis.gov, read 2026-07-07. [VERIFIED]
- Mechanism: the civil surgeon does NOT adjudicate the waiver. The surgeon documents the factual
  state (met / not met / medically not appropriate / applicant will seek religious-moral waiver);
  **USCIS adjudicates admissibility.** (Full surgeon-discretion mechanics = Topic 3a.)

### 1.3 Consequence of an uncured refusal
An I-485 cannot be approved while the applicant is inadmissible. In practice an unresolved
vaccination gap yields a **Request for Evidence (RFE)** or, if unresolved, **denial** of the
I-485. It is **not** by itself a misrepresentation and **not** a permanent bar — it is a curable
deficiency. The applicant can still, at that point, choose a shot, titers, a certified
contraindication, or file the religious/moral waiver. [ASSUMED — consistent with the statute and
PM Ch 9; the specific RFE-then-deny sequence is standard adjudication practice, not a single
quoted line. Confirm exact procedure with BAL.]

### 1.4 Why refusal is the weakest door (H5)
- It doesn't *clear* the requirement — it *fails* it and defers the fight to USCIS.
- It converts a documentation question into a discretionary waiver question (212(g)(2)(C)) with
  a hard sincerity test, or leaves the case deniable.
- Every superior door (titers H2, contraindication H3) *avoids* the refusal box entirely by
  making the requirement genuinely met or genuinely medically-not-appropriate.
- **Use only as the last resort behind a real religious/moral waiver, never as a bare "no."**

---

## 2. The blanket/"not medically appropriate" outcomes that are NOT refusal

These matter here because the goal is to reach one of these truthful states instead of the
refusal box. Per PM Vol 8 Pt B Ch 9 (2025-05-13), a civil surgeon may mark a vaccine **"not
medically appropriate"** — which is *not* a refusal and needs *no* I-601 waiver — when:
1. **Not age-appropriate** for the applicant at exam time;
2. **Medically contraindicated** — "a condition in a recipient which is likely to result in a
   life-threatening problem if the vaccine is given";
3. **Insufficient time interval** to complete a multi-dose series; or
4. **Influenza** outside flu season / strain unavailable.
- Source: USCIS PM Vol 8 Pt B Ch 9, read 2026-07-07. [VERIFIED]
- These are the H2/H3 doors and are the *point* of this whole project. Detail lives in
  `titers_and_immunity.md` (1b) and `medical_contraindication.md` (1c). Flagged here only to
  contrast with §1: **a certified contraindication is a lawful "not appropriate," not a refusal.**

> ⚠️ Guardrail seam (route to Topic 1c + Stage 5 red-team): the contraindication door is
> truthful ONLY if the condition genuinely meets the CDC/ACIP contraindication standard as
> judged by a physician. Note the PM's *narrow* framing ("likely to result in a life-threatening
> problem"). A civil surgeon certifying a contraindication that a physician would not actually
> support would be a false certification — i.e., it converts an H3 door into a §3
> misrepresentation risk. The contraindication must come from genuine medical judgment
> (his hematologist / the CDC live-vaccine-in-immunosuppression and pregnancy rules), not be
> reverse-engineered to dodge a shot.

---

## 3. The misrepresentation permanent bar — INA 212(a)(6)(C)(i)

This is the line every other door must stay clear of.

### 3.1 The statute
8 USC 1182(a)(6)(C)(i): "Any alien who, **by fraud or willfully misrepresenting a material
fact**, seeks to procure (or has sought to procure or has procured) a visa, other documentation,
or admission into the United States or **other benefit provided under this chapter is
inadmissible**."
- Source: 8 USC 1182(a)(6)(C)(i), Cornell LII, read 2026-07-07. [VERIFIED]
- An I-485 adjustment application, and the I-693 medical that supports it, are squarely a
  "benefit provided under this chapter." [ASSUMED-HIGH — direct reading of the statute.]

### 3.2 It is a LIFETIME bar
USCIS Policy Manual **Vol 8, Part J, Chapter 2** (published 2025-02-26): "The alien will be
**barred from admission for the rest of his or her life** unless the alien qualifies for and is
granted a waiver."
- Source: USCIS PM Vol 8 Pt J Ch 2, read 2026-07-07. [VERIFIED]
- Contrast: the vaccination ground (§1) is curable at any time; this one is not.

### 3.3 The elements USCIS must find (willful misrepresentation)
Per PM Vol 8 Pt J Ch 2 & Ch 3 (2025-02-26): the alien
1. **procured, or sought to procure, a benefit** under U.S. immigration law;
2. made a **false representation**;
3. that was **willfully** made — "knowingly," as opposed to "accidentally, inadvertently, or in
   a good faith belief that the factual claims are true";
4. that was **material**; and
5. that was **made to a U.S. government official** (generally an immigration or consular officer).
- Source: USCIS PM Vol 8 Pt J Ch 2 & Ch 3, read 2026-07-07 / 08. [VERIFIED]
- **"Willful" ≠ intent to deceive.** The PM states evidence of intent to deceive is NOT required
  for *willful misrepresentation* (that extra element is only for *fraud*). So a knowing false
  statement is enough even without a scheme to defraud. [VERIFIED]
- **Fraud** = all of the above **plus** intent to deceive **plus** the official believed and
  acted on it. Anyone inadmissible for fraud is also inadmissible for willful misrepresentation.
  [VERIFIED]

### 3.4 What "material" means (the test that catches medical-exam lies)
PM Vol 8 Pt J Ch 3, Section E, applies the Supreme Court's **Kungys v. United States** standard:
a misrepresentation is material if it "**has a natural tendency to influence or was capable of
influencing the decisions of the decision-making body.**" Concretely, material if:
1. the alien **would be inadmissible on the true facts**; OR
2. the misrepresentation **"tends to cut off a line of inquiry which is relevant to the
   applicant's eligibility and which might have resulted in a proper determination that he or she
   is inadmissible."**
- Source: USCIS PM Vol 8 Pt J Ch 3 §E, read 2026-07-08. [VERIFIED]
- **Why this bites here:** falsely stating vaccination history, a fake immunity claim, or a
  contraindication the physician wouldn't actually certify all "cut off a line of inquiry"
  relevant to the (a)(1)(A)(ii) admissibility determination — squarely material.

### 3.5 The "made to a U.S. government official" element — and the civil-surgeon nuance
PM Vol 8 Pt J Ch 3: "The fraud or willful misrepresentation must have been made to an **official
of the U.S. government, generally an immigration or consular officer**." And: "Fraud or willful
misrepresentation made to a **private person or entity would not make one inadmissible** under
this ground."
- Source: USCIS PM Vol 8 Pt J Ch 3, read 2026-07-08. [VERIFIED]
- **Nuance to hand to BAL, do NOT rely on:** a civil surgeon is a USCIS-**designated** physician,
  arguably a private party, and the PM does not directly say a lie told only to the civil surgeon
  (never repeated to USCIS) satisfies this element. **This is NOT a loophole and must not be
  treated as one.** The I-693 the surgeon seals is submitted to and relied on by USCIS; a false
  statement that flows onto the I-693 and into the adjustment file reaches the adjudicating
  officer. And the I-485 itself is signed under penalty of perjury directly to USCIS. Treat any
  false statement anywhere in the medical/benefit chain as capable of triggering (a)(6)(C)(i).
  [ASSUMED — legal analysis for BAL; flagged as a seam, not a plan.]

### 3.6 Timely retraction (a narrow safety valve — not a plan)
PM Vol 8 Pt J Ch 3 recognizes **timely retraction**: a voluntary correction can prevent a
misstatement from becoming a basis of inadmissibility, but only if "the applicant must correct
his or her representation **before being exposed by the officer or U.S. government official or
before the conclusion of the proceeding**," and "**admitting to the false representation after
USCIS has challenged the veracity of the claim is not a timely retraction.**"
- Source: USCIS PM Vol 8 Pt J Ch 3, read 2026-07-08. [VERIFIED]
- **Do not design around this.** It is a mitigant for accidental error caught early, not a
  license to try a false statement and walk it back if questioned. The safe posture is: never
  submit anything untrue in the first place.

### 3.7 The only escape hatch (INA 212(i)) is narrow and discretionary
Once (a)(6)(C)(i) attaches, the only relief is a **212(i) waiver** (8 USC 1182(i)):
- Eligible only if the applicant is the **spouse, son, or daughter of a U.S. citizen or LPR** —
  and the extreme hardship must be to that **USC/LPR spouse or parent**. Per PM Vol 9 Pt F Ch 2
  (2025-02-26): qualifying relatives are a "U.S. citizen or LPR parent or spouse" (and a USC
  fiancé(e) petitioner for K visas); "**U.S. citizen or LPR children are not qualifying
  relatives.**" [VERIFIED]
- Must show **"extreme hardship"** to that qualifying relative, AND a favorable exercise of
  **discretion** ("the applicant's positive factors outweigh the negative factors"). [VERIFIED]
- **Application to Hooman:** this waiver would likely be **unavailable** — he is here on
  employment sponsorship; unless he has a USC/LPR spouse or parent, there is no qualifying
  relative. His wife is a **co-applicant** (also a foreign national adjusting), so she would not
  supply a qualifying relationship, and a pregnancy/future USC child does **not** count.
  **Meaning: for Hooman, a 212(a)(6)(C)(i) finding is realistically permanent with no waiver.**
  This is exactly why the misrepresentation line is the one bright red line in this project.
  [ASSUMED-HIGH — turns on his family facts; confirm qualifying-relative status with BAL.]

---

## 4. Concrete "what NOT to do" list (steer every door away from these)

Each of these would risk converting a curable vaccine question into a permanent (a)(6)(C)(i) bar.
None are proposed; they are enumerated so BAL, the physician, and future agents can spot and
avoid them.

- **Do NOT** claim vaccines were received that were not received, or submit an altered/forged
  vaccination record. (False material fact → §3.)
- **Do NOT** claim a titer/immunity result that isn't backed by a genuine lab report. (Same.)
- **Do NOT** obtain (or ask any physician or civil surgeon to sign) a **contraindication
  certification the treating physician's own medical judgment would not genuinely support** under
  CDC/ACIP standards. A contraindication note must reflect real clinical judgment about Hooman's
  LGL/immunosuppression or his wife's pregnancy — not a favor to dodge a shot. (False
  certification → §3, and it also exposes the signing physician.)
- **Do NOT** assert a religious/moral objection that is not sincere, or frame a COVID-specific /
  single-vaccine objection as blanket opposition just to fit the 212(g)(2)(C) test. Sincerity is
  itself adjudicated; an insincere claim is a misrepresentation. (See `religious_waiver_i601.md`.)
- **Do NOT** omit or conceal a material fact on the I-485 or I-693 hoping it won't surface —
  concealment that cuts off a relevant line of inquiry is itself material misrepresentation (§3.4).
- **Do NOT** treat "I only told the civil surgeon, not USCIS" as a shield (§3.5). It is not a plan.
- **Do NOT** submit a false statement intending to retract it if challenged — that is not a
  timely retraction (§3.6).

**The safe universal rule:** if a door requires stating something that is not literally, factually
true as judged by the physician/lab/applicant's genuine belief, it is off the table — regardless
of how much easier it would make the case.

---

## 5. How this steers the other doors (hand-off notes)

- **1a (requirement):** if the current required list is smaller than feared (e.g., COVID-19
  removed), the whole refusal/misrepresentation risk shrinks — fewer vaccines to reconcile. Verify
  the *current* list; do not carry stale assumptions that could tempt a shortcut.
- **1b (titers):** cleanest door precisely because it produces *genuine* documentary proof (lab
  report) — zero §3 exposure as long as results are real and unaltered.
- **1c (contraindication):** strong door but the one with the sharpest guardrail seam (§2 ⚠, §4).
  Must rest on the physician's real CDC/ACIP judgment. Feed the "life-threatening problem"
  framing and the pregnancy/immunosuppression live-vaccine rules into 1c and Stage-5 red-team.
- **1d (religious/moral waiver):** the "any form / all vaccines" sincerity test (212(g)(2)(C)) is
  itself a misrepresentation trap if the objection is really COVID-specific. Sincerity is
  adjudicated → an insincere or overstated claim = §3 risk. See 1d.
- **Decision map (Stage 2):** every cell should carry a "misrepresentation-clean? Y/N" check.

---

## 6. Statutory-citation correction to propagate (housekeeping)

The plan (research-plan.md H3/H4 and Stage 1d) cites the vaccination waiver as **INA
212(g)(1)(C)**. Primary sources confirm it is **INA 212(g)(2)** (8 USC 1182(g)(2)):
- (g)(1) = waiver of the **communicable-disease** ground (a)(1)(A)(i);
- **(g)(2) = waiver of the VACCINATION ground (a)(1)(A)(ii)**, with subclauses (A) receives the
  vaccine, (B) civil surgeon/medical officer certifies vaccination **not medically appropriate**,
  (C) contrary to **religious beliefs or moral convictions** (by AG regulation);
- (g)(3) = physical/mental-disorder ground.
- Source: 8 USC 1182(g), govinfo USCODE-2022 + Cornell LII, read 2026-07-07. [VERIFIED]
- **Action:** update research-plan.md and any other topic files that wrote "212(g)(1)(C)" to
  "212(g)(2)(C)". (Left for main-session to apply so this subagent doesn't edit the plan silently.)

---

## 7. Open questions (route to BAL / physician; do not let these drive a recommendation)

1. **Qualifying relative for a hypothetical 212(i) waiver** — does Hooman have any USC/LPR spouse
   or parent? (Almost certainly not; determines whether an (a)(6)(C)(i) finding is truly
   unwaivable for him.) → BAL. [UNVERIFIED — family facts]
2. **Exact RFE-vs-denial procedure** when a vaccination gap is unresolved at I-485 adjudication,
   and whether the applicant can cure via waiver after the RFE. → BAL. [UNVERIFIED]
3. **Does a false statement made only to the civil surgeon (never repeated to USCIS) satisfy the
   "to a U.S. government official" element?** Legal question for BAL — flagged as a seam, NOT to
   be relied on regardless of the answer. [UNVERIFIED — §3.5]
4. **Current I-693 edition & the exact vaccination-section checkboxes** (met / not
   age-appropriate / contraindicated / insufficient interval / "applicant will request
   religious-moral waiver") — the I-693 page shows editions 01/20/25 and 03/09/23; the checkbox
   text should be read off the actual form. → Topic 1a / data capture. [UNVERIFIED — form text]

---

## 8. Sources used (all read live this session; primary unless noted)

- **8 USC 1182(a)(1)(A)(ii), (a)(6)(C)(i), (g), (i)** — Cornell Legal Information Institute,
  https://www.law.cornell.edu/uscode/text/8/1182 — read 2026-07-07. [VERIFIED primary statute]
- **8 USC 1182(g) full subsection** — govinfo USCODE-2022-title8-sec1182,
  https://www.govinfo.gov/content/pkg/USCODE-2022-title8/html/USCODE-2022-title8-chap12-subchapII-partII-sec1182.htm
  — read 2026-07-07. [VERIFIED primary statute]
- **USCIS Policy Manual, Vol 8, Part B, Chapter 9 — Vaccination Requirement** (published
  2025-05-13), https://www.uscis.gov/policy-manual/volume-8-part-b-chapter-9 — read 2026-07-07
  via r.jina.ai text proxy (uscis.gov blocks direct automated fetch/Akamai 403). [VERIFIED
  primary policy — proxy note below]
- **USCIS Policy Manual, Vol 8, Part J, Chapters 1–3 — Fraud & Willful Misrepresentation**
  (published 2025-02-26), https://www.uscis.gov/policy-manual/volume-8-part-j-chapter-{1,2,3} —
  read 2026-07-07/08 via r.jina.ai. [VERIFIED primary policy]
- **USCIS Policy Manual, Vol 9, Part F, Chapter 2 — Adjudication of Fraud/Misrep Waivers**
  (published 2025-02-26), https://www.uscis.gov/policy-manual/volume-9-part-f-chapter-2 — read
  2026-07-07 via r.jina.ai. [VERIFIED primary policy]
- **Form I-693 page** (editions 01/20/25 & 03/09/23 referenced), https://www.uscis.gov/i-693 —
  read 2026-07-07 via r.jina.ai; checkbox text not fully captured (→ open Q 4). [PARTIAL]

> **Source-access caveat:** uscis.gov returns Akamai HTTP 403 to WebFetch and to curl with a
> browser UA; web.archive.org is blocked in this environment. USCIS Policy Manual content was
> read through the r.jina.ai text proxy, which renders the live uscis.gov page. Quoted language
> and the published dates (2025-05-13, 2025-02-26) should be **spot-confirmed against the live
> USCIS site in a normal browser** before anything here is treated as citation-of-record for BAL.
> Statutory text was read directly from Cornell LII and govinfo (not proxied). [Method note]
