# Topic 1c — Medical Contraindication Door (the "blanket waiver")

**Task:** Map CDC/ACIP contraindications for (i) immunosuppression / autoimmune disease
(Hooman's LGL leukemia + any immunosuppressive treatment) and (ii) pregnancy (his wife),
against each required vaccine. Establish which live vaccines are contraindicated, how the
civil surgeon records a contraindication on I-693, and whether it is permanent or temporary.

**Author:** Claude (Opus 4.8) · **Date:** 2026-07-07 · **Status:** Stage-1 research complete
for this door. Fed to `exemptions/decision_map.md` (Stage 2) and the Stage-5 red-team pass.

> NOT legal or medical advice. Whether a specific condition/medication is a contraindication
> for a specific person is a clinical judgment for Hooman's hematologist and the signing civil
> surgeon, grounded in CDC/ACIP. This file maps the rules; it does not diagnose.

---

## 0. Bottom line (the door in one paragraph)

The **medical-contraindication path is a real, no-waiver-application door**, and it is the
strongest single door for **live vaccines**. Under the USCIS Policy Manual, if a civil surgeon
marks a vaccine "not medically appropriate" because of a **contraindication**, USCIS **waives
that vaccine with no separate application (no I-601)** — this is a "blanket waiver." The Policy
Manual **explicitly names pregnancy and immuno-compromised conditions** as contraindication
grounds, and — critically — states that **once the civil surgeon properly marks the box at the
time of the exam, USCIS will never later require those vaccines even if the pregnancy has ended
or the applicant is no longer immunocompromised at adjudication.** [VERIFIED]

**The hard limit:** immunosuppression and pregnancy are contraindications to **LIVE**
vaccines only (MMR, varicella, LAIV; rotavirus is live but not age-relevant for adults). They
are **NOT** contraindications to the **inactivated/recombinant** vaccines on the list (Td/Tdap,
Hep A, Hep B, polio [IPV], pneumococcal, meningococcal, Hib, inactivated influenza). Those must
be cleared by a different door (titers / documented prior doses / age-not-appropriate), not by
this one. [VERIFIED]

---

## 1. The required vaccine list (for mapping) — and which are live vs. inactivated

Source: USCIS Policy Manual Vol. 8, Part B, Ch. 9(A) + CDC civil-surgeon vaccination page. [VERIFIED]

Statute (INA) requires: MMR, polio, Td (tetanus/diphtheria), pertussis, Hib, Hep B.
CDC adds: varicella, influenza, pneumococcal, rotavirus, Hep A, meningococcal.
**COVID-19 is removed** (see §5). HPV was removed in 2009.

| Required vaccine | Live-attenuated? | Contraindicated by immunosuppression? | Contraindicated by pregnancy? |
|---|---|---|---|
| **MMR** (measles/mumps/rubella) | **LIVE** | **YES** (severe immunosuppression) | **YES** |
| **Varicella** | **LIVE** | **YES** (severe immunosuppression) | **YES** |
| **Influenza — LAIV** (nasal, FluMist) | **LIVE** | **YES** | **YES** |
| **Influenza — IIV/RIV** (inactivated/recombinant shot) | inactivated | No (use this instead of LAIV) | No — recommended in pregnancy |
| **Rotavirus** | LIVE | YES — but **infant-only** vaccine; not age-appropriate for adults → cleared as "not age appropriate," not needed here | n/a (infant) |
| **Td / Tdap** (tetanus/diphtheria/pertussis) | inactivated (toxoid) | No | No — Tdap recommended each pregnancy |
| **Polio (IPV)** | inactivated | No | No |
| **Hib** | inactivated | No | No (adult rarely age-appropriate anyway) |
| **Hepatitis A** | inactivated | No | No |
| **Hepatitis B** | inactivated (recombinant) | No | No — recommended for adults 19–59 |
| **Pneumococcal** | inactivated | No | No |
| **Meningococcal** | inactivated | No | No |

[VERIFIED — live/inactivated classification per CDC Pinkbook Ch. 2 & CDC pregnancy-vaccination
guidance; required-list per USCIS PM Vol.8 Pt.B Ch.9(A). See §7 sources.]

**Takeaway:** the contraindication door only closes the **3 live rows relevant to adults**:
**MMR, varicella, and LAIV.** For LAIV specifically, the applicant can simply take the
inactivated flu shot instead — so pregnancy/immunosuppression does not by itself excuse the
flu requirement; it only excuses the *live* form. (Flu is separately deferrable when it is
"not flu season" — a different blanket-waiver category; see the titers/requirement files.)

---

## 2. Immunosuppression / autoimmune disease (Hooman's LGL leukemia)

### 2a. The CDC/ACIP rule
- CDC Pinkbook, Ch. 2 (General Best Practice Guidance): **"Severe immunosuppression is a
  contraindication to live, attenuated vaccines."** Live vaccines "should usually not be
  administered to severely immunosuppressed persons with congenital immunodeficiency,
  **leukemia, lymphoma, or generalized malignancy**." [VERIFIED — CDC Pinkbook Ch.2, read
  2026-07-07]
- Same source: **"Inactivated vaccines cannot replicate, so they are safe to use in
  immunosuppressed persons"** (immune response may be diminished, but there is no
  contraindication). [VERIFIED]
- The operative clinical threshold is **"severe" / "altered immunocompetence."** Two triggers
  are relevant to Hooman: (a) **the disease itself** — LGL leukemia is a leukemia, one of the
  named conditions; and (b) **immunosuppressive treatment** — LGL leukemia is frequently
  managed with immunosuppressive agents (e.g., methotrexate, cyclophosphamide, ciclosporin).
  Whether Hooman meets the "severe immunosuppression" bar is a **clinical determination** for
  his hematologist / the civil surgeon, not something this file can assert. [ASSUMED — the
  disease category and typical treatments are documented; the individual determination is
  medical. Flag for the physician question list.]

### 2b. What USCIS says about immuno-compromised applicants
USCIS Policy Manual Vol. 8, Part B, Ch. 9, §B.2 states verbatim:
> "Some vaccines are not medically appropriate for applicants who have an immuno-compromised
> condition (such as HIV/AIDS or a weakened immune system because of taking certain
> medications) and may be marked by the civil surgeon as contraindicated." [VERIFIED — read
> 2026-07-07, archived Jan 2026 copy of the live chapter]

And, decisively for durability:
> "In the case of an immuno-compromised person, **the officer should never issue an RFE for
> additional vaccines even if, at the time of the adjudication of adjustment of status, the
> applicant is no longer immuno-compromised.** As long as the vaccination assessment was
> properly completed at the time of the examination by the civil surgeon, the vaccination
> assessment can be accepted. The applicant should not be required to get the missing vaccines
> later." [VERIFIED]

### 2c. Live rows this closes for Hooman
If a civil surgeon determines his LGL leukemia and/or its treatment constitutes a
contraindication to live vaccines: **MMR, varicella, and LAIV** can be marked contraindicated
→ blanket-waived, no I-601. **It does NOT excuse** Td/Tdap, Hep A, Hep B, IPV, pneumococcal,
meningococcal, or the inactivated flu shot — those are safe in immunosuppression and must be
cleared by titers/prior-dose documentation or age-not-appropriate. [VERIFIED for the rule;
the per-person determination is clinical.]

---

## 3. Pregnancy (Hooman's wife, co-applicant with her own I-693)

### 3a. The CDC/ACIP rule
- CDC Pinkbook Ch. 2: **"Live, attenuated viral vaccines (e.g., MMR-II, Varivax, FluMist) are
  contraindicated during pregnancy because of the theoretical risk of virus transmission to
  the fetus."** [VERIFIED]
- CDC Vaccination-During-Pregnancy guidance (for clinicians): **"MMR vaccine is
  contraindicated for use during pregnancy and should not be administered to women known to be
  pregnant"**; **"varicella vaccine is contraindicated for use during pregnancy"**; **"Live
  attenuated influenza vaccine (LAIV) is contraindicated for use during pregnancy."** [VERIFIED]
- Recommended (NOT contraindicated) in pregnancy: **Tdap** (one dose each pregnancy),
  **inactivated/recombinant influenza** (any trimester), **Hep B** if indicated. So pregnancy
  does not excuse those. [VERIFIED]
- After a live vaccine, CDC counsels avoiding pregnancy for **28 days (MMR)** / **1 month
  (varicella)** — relevant only if she were considering catching up post-partum. [VERIFIED]

### 3b. What USCIS says about pregnant applicants
USCIS PM Vol. 8, Pt. B, Ch. 9, §B.2 states verbatim:
> "Some vaccines are, in general, not medically appropriate during pregnancy. These vaccines
> will likely be marked as contraindicated on Form I-693 if the applicant was pregnant at the
> time of the medical examination." [VERIFIED]

And for durability:
> "An officer should also **never issue an RFE for additional vaccines if the applicant is no
> longer pregnant at the time of the adjudication** of the adjustment of status. As long as the
> vaccination assessment was properly completed by the civil surgeon at the time of the
> examination, the vaccination assessment can be accepted. In other words, if a woman did not
> receive certain required vaccines because she was pregnant at the time of the medical
> examination, and the contraindication box is marked by the civil surgeon, the applicant is
> **not required to get those vaccines later** at the time of the adjudication." [VERIFIED]

### 3c. Live rows this closes for the wife
**MMR, varicella, LAIV** → contraindicated during pregnancy → blanket-waived, no I-601.
Does NOT excuse Tdap, inactivated flu, Hep B, or the other inactivated vaccines — those are
recommended/allowed in pregnancy and must be cleared by titers/prior-dose documentation.
[VERIFIED for the rule.]

> ⚠️ **Timing subtlety (feed to red-team + BAL):** the wife's contraindication is anchored to
> "pregnant **at the time of the medical examination.**" To rely on the pregnancy door for her
> live vaccines, her I-693 exam should be done **while she is pregnant** and the box marked
> then. The Policy Manual protects her from being asked to catch up after delivery — but only
> if the exam captured the pregnancy. If her exam happens post-partum, pregnancy no longer
> supplies the contraindication and she'd need titers/prior doses for MMR & varicella instead.

---

## 4. How the civil surgeon records it, and permanent vs. temporary

### 4a. Mechanics (the "blanket waiver")
- The civil surgeon marks the finding directly on **Form I-693** (current edition **01/20/25**;
  USCIS accepts only the 01/20/25 edition for exams signed on/after **July 2, 2025**) in the
  vaccination-assessment chart. There is a **"not medically appropriate"** box per vaccine row;
  "not medically appropriate" is defined by USCIS to include four sub-reasons: **not age
  appropriate; contraindication; insufficient time interval; not flu season.** Contraindication
  is the one that applies here. [VERIFIED — I-693 edition date from USCIS forms page (archived
  Jan 2026); box definitions from PM Vol.8 Pt.B Ch.9 §B.1]
- USCIS PM §B.1 verbatim: **"If receiving the vaccine is not medically appropriate, the civil
  surgeon should indicate this medical finding on the … Form I-693 in the appropriate boxes.
  USCIS will then waive that vaccine(s). A separate waiver application is not required for an
  officer to grant a waiver of the vaccination requirement as 'not medically appropriate.'"**
  [VERIFIED] → **This is why the contraindication door needs NO I-601.**
- Deference: **"An officer … should usually defer to a civil surgeon's finding that a vaccine
  is not medically appropriate because of a contraindication. This is because such a finding
  involves medical judgment."** (Contrast: the officer *can* second-guess "not age appropriate"
  or "not flu season," which are objectively checkable.) [VERIFIED]
- The reason for the contraindication *may* be annotated in the remarks section; per PM, if the
  reason annotation is omitted, **USCIS "does not need to issue a Request for Evidence (RFE)
  solely for that omission as long as the contraindication is marked in the vaccine chart."**
  [VERIFIED]

### 4b. Permanent or temporary?
This is the crucial nuance. The *biological* contraindication is temporary (pregnancy ends;
immunosuppression may pause) — but the *immigration effect* is effectively **permanent for
this application**:
- The contraindication is assessed **as of the exam date.** [VERIFIED]
- USCIS **will not** later require the waived vaccines even if the condition has resolved by
  adjudication — this is stated explicitly for **both** pregnancy and immuno-compromised cases
  (quoted in §2b and §3b). [VERIFIED]
- So for the purpose of *this* I-485, a properly-marked contraindication box **closes the row
  permanently** — it is not a deferral that comes back as an RFE later. (It is not a lifetime
  medical exemption in the abstract; a *future, separate* immigration filing with a *new* I-693
  would be assessed fresh. Not relevant to the current AOS.) [VERIFIED for current application;
  ASSUMED re: future filings — no separate filing is contemplated.]

Contrast with the other "not medically appropriate" reasons:
- **"Insufficient time interval"** (a multi-dose series that can't be finished before the exam
  is signed) — this IS a true deferral; USCIS can require completion. Not our mechanism.
- **"Not flu season"** — deferral of the flu shot; objectively checkable by the officer.
[VERIFIED — PM §B.1]

---

## 5. COVID-19 status (context; owned by task 1a, restated for completeness)
COVID-19 vaccination has been **removed** from the immigration requirement: USCIS announced
(Jan 22, 2025) that as of **Jan 20, 2025** it stopped issuing RFEs/NOIDs/denials for missing
COVID documentation, and **CDC removed COVID-19 from the civil-surgeon Technical Instructions
on March 11, 2025.** Applicants pending on/after Jan 20, 2025 need not document COVID vaccination.
[VERIFIED — USCIS PM Vol.8 Pt.B Ch.9, footnote/section on COVID-19; Technical Update dated
2025-05-13]. → Hooman's central fear (the COVID shot) is moot *without* needing this door at all.

---

## 6. What this door does and does NOT do (precise per-vaccine summary)

**CLOSES (live vaccines) — via contraindication, no I-601:**
- **MMR** — Hooman (if immunosuppression is severe per his physician) AND wife (pregnant at exam). ✅
- **Varicella** — same. ✅
- **LAIV (nasal flu)** — same; but note the *inactivated* flu shot is still available/allowed,
  so the flu *requirement* is not excused by this door alone (clear flu via "not flu season"
  deferral or by taking the inactivated shot / documenting it). ⚠️

**DOES NOT CLOSE (inactivated/recombinant — safe in both conditions):**
- **Td/Tdap, IPV (polio), Hib, Hep A, Hep B, pneumococcal, meningococcal, inactivated flu.**
  These are not contraindicated by pregnancy or immunosuppression and must be cleared another
  way — **titers / documented prior doses** (see `exemptions/titers_and_immunity.md`), or
  "not age appropriate" where applicable. [VERIFIED]

**Net:** the contraindication door reliably removes the *live-vaccine* exposure for both of
them — which is likely the subset they most object to — but it is **not** a complete pass on
the whole list. The inactivated vaccines still need the titer/prior-dose door. This is the key
handoff into the Stage-2 decision map.

---

## 7. Sources (primary, read live 2026-07-07)

- **USCIS Policy Manual, Vol. 8, Part B, Ch. 9 — "Vaccination Requirement."**
  https://www.uscis.gov/policy-manual/volume-8-part-b-chapter-9
  (uscis.gov blocks automated fetch → read via Internet Archive snapshot captured 2026-01-03,
  i.e. current live text; most recent Technical Update on the page dated 2025-05-13 "Removal of
  COVID-19 Vaccine Requirement"). Sections used: A (required list), B.1 (blanket waiver /
  not-medically-appropriate definition + officer deference), B.2 (pregnancy & immuno-compromised
  + the never-RFE-later rule), COVID-19 update section. [VERIFIED]
- **USCIS Form I-693 page — edition date 01/20/25**; only the 01/20/25 edition accepted for
  civil-surgeon signatures on/after July 2, 2025. https://www.uscis.gov/i-693 (via Archive
  snapshot, 2026). [VERIFIED]
- **CDC Pinkbook, Ch. 2 — General Best Practice Guidance for Immunization** (contraindications
  & precautions; "severe immunosuppression is a contraindication to live attenuated vaccines";
  leukemia/lymphoma named; inactivated vaccines safe in immunosuppression).
  https://www.cdc.gov/pinkbook/hcp/table-of-contents/chapter-2-general-best-practice-guidance.html
  [VERIFIED]
- **CDC — Vaccination During Pregnancy (clinician guidance)** (MMR/varicella/LAIV
  contraindicated; Tdap + inactivated flu recommended; 28-day / 1-month post-live avoidance).
  https://www.cdc.gov/vaccines-pregnancy/hcp/vaccination-guidelines/ [VERIFIED]
- **CDC — Vaccination Technical Instructions for Civil Surgeons** (required-vaccine list; defers
  when a contraindication/precaution is present; documents "contraindication" reason for a
  blanket waiver on I-693; COVID-19 absent).
  https://www.cdc.gov/immigrant-refugee-health/hcp/civil-surgeons/vaccination.html [VERIFIED]
- **CDC ACIP General Best Practices — Contraindications & Precautions** (index; detail lives in
  Pinkbook Ch.2 and vaccine-specific ACIP statements).
  https://www.cdc.gov/vaccines/hcp/acip-recs/general-recs/contraindications.html [VERIFIED as
  a pointer; substantive text taken from Pinkbook Ch.2]

---

## 8. Open questions → for the physician / hematologist and for BAL

1. **[Physician — hematologist]** Does Hooman's LGL leukemia and/or his current treatment meet
   the CDC/ACIP threshold of **"severe immunosuppression / altered immunocompetence"** such
   that a civil surgeon can, in good faith, mark MMR/varicella/LAIV as contraindicated? What
   documentation (diagnosis, medication list, immune-status labs) supports that determination?
   *(This is the entire hinge for Hooman's use of this door — and it must be genuinely true;
   see the guardrail.)*
2. **[Civil surgeon]** Will the civil surgeon accept a treating-hematologist's letter as the
   basis for the contraindication mark, and annotate the reason in the remarks box?
3. **[BAL / logistics]** Should the **wife's I-693 exam be scheduled while she is still
   pregnant** so the pregnancy contraindication is captured at exam time (per §3c timing note)?
   Confirm her co-applicant status and her own I-693 timeline.
4. **[Handoff]** For every **inactivated** vaccine the contraindication door does NOT excuse,
   which can be cleared by **titers / documented prior doses**? → routes to
   `exemptions/titers_and_immunity.md` and the Stage-2 decision map.

---

## 9. GUARDRAIL note (truthfulness)
This door is only legitimate if the contraindication is **medically real**: the wife is
genuinely pregnant at exam time, and Hooman genuinely meets the immunosuppression threshold in
his physician's judgment. If a physician would not, in good faith, mark a contraindication,
this door does not apply and must not be manufactured — a false medical notation would expose
the application to the permanent misrepresentation bar under INA 212(a)(6)(C), which is
categorically worse than any vaccine. We surface this door as a **question for the physician**,
not a conclusion. [Per CLAUDE.md §5 guardrail.]
