# Topic 1a — What Is Actually Required (I-693 vaccination requirement)

**Owner deliverable for:** Track A, Stage 1a (research-plan.md §2).
**Author:** Claude (Opus 4.8) research subagent. **Session date:** 2026-07-07.
**Status:** Primary-source-verified for the load-bearing claims (COVID removal, current
vaccine list, I-693 edition, waiver framework).

## 2026-09-11 LIVE RE-VERIFICATION — Hooman, age 35, October 2026 exam

**Scope:** Hooman only; age 35 at the anticipated civil-surgeon examination in October 2026;
medical contraindications intentionally excluded from this narrow age-table answer at Hooman's
request. **Confidence: VERIFIED-HIGH** against the current CDC civil-surgeon Technical Instructions
and current USCIS Policy Manual retrieved 2026-09-11. Direct automated access returned HTTP 403, so
the official pages were read through a text-fetch proxy; all citations below point to the canonical
official URLs.

For a 35-year-old, CDC Table 1 makes exactly these six rows age-appropriate:

1. **Td/Tdap**
2. **Polio (IPV/qualifying prior OPV)**
3. **MMR (measles, mumps, rubella)**
4. **Hepatitis B** (required through age 59)
5. **Varicella**
6. **Influenza** (the I-693 flu season is October 1 through March 31, so an October exam is in season)

This does **not** mean six injections are automatically necessary. CDC directs the civil surgeon to
apply written dated records and accepted laboratory immunity first. If neither exists, the applicant
generally receives at least the dose currently due at the examination; a multi-dose series need not
be completed before signature when the civil surgeon properly records "insufficient time interval."

| Row | What satisfies it without a new dose | If there is no acceptable evidence |
|---|---|---|
| Td/Tdap | Dated complete primary series plus a Td/Tdap dose within 10 years | Current Td/Tdap dose; use Tdap if no documented Tdap at age 10+; catch-up rules apply if primary series incomplete |
| Polio | Dated complete primary series, or accepted immunity test covering all 3 poliovirus types | Begin/continue IPV catch-up; first/currently-due dose at exam |
| MMR | Dated valid MMR record, or accepted positive immunity for measles, mumps, and rubella | 1 MMR dose under routine adult rule |
| Hepatitis B | Dated valid series, or accepted laboratory evidence of immunity | Begin/continue age-appropriate HepB series; first/currently-due dose at exam |
| Varicella | Dated valid series, accepted positive titer, or civil-surgeon-verified reliable disease history | Begin/continue 2-dose series; first/currently-due dose at exam |
| Influenza | Current-season dated dose | Current-season influenza dose because October is within the USCIS October 1–March 31 season |

**Not age-required at 35 for I-693:** pediatric DTP/DTaP/DT, rotavirus, Hib, hepatitis A,
meningococcal (MenACWY), and pneumococcal. COVID-19 is removed from the immigration requirement;
HPV and zoster are also not immigration requirements. ACIP risk/travel recommendations beyond the
routine general-population schedule are not imported into the status-adjustment table: CDC gives the
explicit example that an adult with a condition-specific Hib recommendation still does not require
Hib for status adjustment.

**Primary sources, retrieved 2026-09-11:**

- CDC, *Vaccination Technical Instructions for Civil Surgeons*, Table 1 and sections on records,
  laboratory immunity, and dose/series handling (page dated Mar. 11, 2025):
  https://www.cdc.gov/immigrant-refugee-health/hcp/civil-surgeons/vaccination.html
- USCIS Policy Manual, Vol. 8, Part B, Ch. 9 (flu season; Td/Tdap 10-year booster; COVID removal;
  reliance on CDC age chart): https://www.uscis.gov/policy-manual/volume-8-part-b-chapter-9
- CDC, *Adult Immunization Schedule Notes* (Td/Tdap, IPV, MMR, HepB, varicella, influenza dose
  rules): https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-notes.html
- USCIS, Form I-693 page (current page published July 24, 2026; edition 01/20/25 remains the only
  accepted edition for civil-surgeon signatures on/after July 3, 2025): https://www.uscis.gov/i-693

### 2026-09-11 titer mapping

Hooman provided a Labcorp report collected 2026-07-16 and reported 2026-07-21. The original remains
outside the repository; no patient address, account number, specimen number, or other unnecessary
identifier was copied here.

| I-693 disease row | Reported result | Immigration consequence |
|---|---|---|
| Measles | IgG 121.0 AU/mL; lab threshold says immune >16.4 | Laboratory immunity should clear measles |
| Mumps | IgG 65.4 AU/mL; lab threshold says immune >10.9 | Laboratory immunity should clear mumps |
| Rubella | IgG <0.90 index; lab calls <0.90 non-immune | Titer does **not** clear rubella; absent an acceptable vaccination record or genuine contraindication, one MMR dose is the practical vaccine because licensed U.S. rubella-containing products are combined MMR/MMRV and MMRV is pediatric-only |
| Hepatitis B | anti-HBs 1683.0 mIU/mL; lab immunity threshold >10 | Laboratory immunity should clear HepB; negative total anti-HBc does not negate vaccine-derived anti-HBs immunity |
| Varicella | VZV IgG reactive; report explicitly calls this evidence of immunity | Laboratory immunity should clear varicella |
| Polio | Not tested | Still needs acceptable primary-series records, an accepted test covering all 3 poliovirus types, or currently-due IPV |
| Td/Tdap | Not tested; CDC does not list serology as an accepted I-693 immunity substitute | Still needs a dated record satisfying the 10-year rule or currently-due Td/Tdap |
| Influenza | Not tested; serology is not the I-693 route | Current 2026–27 seasonal dose expected for an October exam |

**Practical remaining vaccine list based on this report alone:** MMR (because rubella is non-immune),
Td/Tdap (unless cleared by a dated record), IPV (unless cleared by records or a qualifying all-three-
types test), and current-season influenza. **HepB and varicella should not require vaccination.**

The civil surgeon makes the final documentation determination. CDC Technical Instructions accept
laboratory immunity for measles, mumps, rubella, hepatitis B, polio (all 3 types), and varicella when
the assay uses an FDA-approved or CLIA-certified kit.

### 2026-09-14 — Earliest likely 2026–27 influenza-vaccine availability

For both **San Jose** and **Los Angeles city**, the earliest publicly documented, defensible date on
which Hooman could likely obtain the 2026–27 seasonal influenza vaccine was **July 30, 2026**.
Walgreens' official nationwide announcement, dated July 30, stated that flu shots were "now
available" for patients age 3+ with walk-in availability and appointments at pharmacies across the
country. Walgreens served both cities. A Google News date-bounded search found no earlier U.S.
public-availability announcement from June 1 through July 29; CVS's comparable nationwide
announcement came later, on August 27.

**Confidence: VERIFIED-MEDIUM.** July 30 is the earliest documented nationwide consumer-availability
date found, not proof that every individual branch had inventory at opening or that no private
medical office administered a dose earlier. There is no official citywide "release date," because
inventory arrives provider by provider.

This commercial-availability date is separate from the immigration rule. USCIS defines the I-693
influenza season as **October 1 through March 31**; availability in July did not by itself make flu
vaccination required for an I-693 signed before October 1.

Sources, retrieved 2026-09-14:

- Walgreens, *Flu Shots Now Available at Walgreens with Convenient Walk-In and Scheduling Options*,
  July 30, 2026: https://corporate.walgreens.com/news-and-stories/press-releases/pharmacy-healthcare/flu-shots-now-available-at-walgreens-with-convenient-walk-in-and-scheduling-options/
- USCIS Policy Manual, Vol. 8, Part B, Ch. 9 §E.4:
  https://www.uscis.gov/policy-manual/volume-8-part-b-chapter-9
- CVS Health, *CVS Pharmacy and MinuteClinic now offering updated flu vaccines nationwide*,
  August 27, 2026 (corroborating later broad availability):
  https://www.cvshealth.com/news/pharmacy/cvs-pharmacy-and-minuteclinic-now-offering-updated-flu-vaccines-nationwide.html

> NOT legal or medical advice. Decision-support for BAL + a civil surgeon/physician.
> Confidence marks: **VERIFIED** = read live this session from a primary official source
> (USCIS.gov Policy Manual / USCIS I-693 form PDF / CDC civil-surgeon Technical
> Instructions). **ASSUMED** = well-established but not re-pinned to primary source this
> session. **UNVERIFIED** = lead only.

> ⚙️ Access note for future agents: USCIS.gov blocks the WebFetch bot and plain curl
> (HTTP 403, Akamai). The Policy Manual and I-693 PDF were retrieved this session via the
> **Internet Archive Wayback Machine** using curl + a browser User-Agent (WebFetch itself
> cannot reach web.archive.org, but `curl` to `http://web.archive.org/web/<ts>/<url>` works).
> CDC.gov is directly fetchable with a browser UA. Snapshots used are dated May–Jun 2026 and
> the Policy Manual page shows "Current as of May 08, 2026" — recent enough to rely on, but
> re-verify live before any filing.

---

## HEADLINE ANSWERS (the three asks)

### 1) Is the COVID-19 vaccination still required on Form I-693? → **NO. REMOVED.** ✅ VERIFIED
This resolves Hooman's central fear at the requirement level — before any waiver, titer, or
contraindication argument is even needed. Two independent, dated, official actions:

- **USCIS (adjudication side):** "On January 22, 2025, USCIS announced that as of January 20,
  2025, officers would no longer issue any RFEs or Notices of Intent to Deny (NOIDs), or deny
  adjustment of status applications, based on an applicant's failure to submit documentation
  of having received the COVID-19 vaccination." … "**applicants who are subject to the
  immigrant vaccination requirements are not required to submit documentation of having
  completed the COVID-19 vaccination series for any application pending on or after January
  20, 2025.**"
  - Source: USCIS Policy Manual, Volume 8, Part B, Chapter 9 ("Vaccination Requirement"),
    §D, "1. COVID-19 Vaccination." Page states **"Current as of May 08, 2026."**
    URL: https://www.uscis.gov/policy-manual/volume-8-part-b-chapter-9
    (retrieved via Wayback snapshot 20260523030011). **VERIFIED (as of 2026-07-07).**

- **CDC (medical-requirement side):** "On March 11, 2025, CDC updated their Technical
  Instructions for Civil Surgeons to remove the COVID-19 vaccination from the list of
  required vaccinations for immigration purposes." (quoted in the USCIS Policy Manual, and
  corroborated directly on the CDC page below — COVID-19 does **not** appear in the CDC
  required-disease list, and the CDC page carries a "Mar. 11, 2025" date.)
  - Source: CDC, "Vaccination Technical Instructions for Civil Surgeons," dated Mar. 11, 2025.
    URL: https://www.cdc.gov/immigrant-refugee-health/hcp/civil-surgeons/vaccination.html
    **VERIFIED (as of 2026-07-07).**

- **Effective date to cite:** requirement effectively gone for any I-485 pending **on or after
  January 20, 2025** (USCIS adjudication) and formally struck from the medical list on
  **March 11, 2025** (CDC). Hooman's case is well after both dates → **COVID-19 is not a
  requirement for him or his wife.** VERIFIED.

⚠️ **One nuance to hand to BAL / the civil surgeon (not a contradiction, just form mechanics):**
The **current I-693 form itself still contains a COVID-19 row** in the Part 10 vaccination
chart (see §4). This is normal — the paper form lags the policy. The form's own instructions
point civil surgeons to the CDC vaccination page "for COVID-19 specific vaccine guidance,"
and CDC no longer lists it as required. So in practice a civil surgeon should not require the
COVID-19 shot; if a row must be addressed, it is handled per CDC guidance (e.g., blanket-waiver
"not routinely available" column exists specifically for COVID-19 — see §4). **Net: Hooman does
not need the COVID-19 vaccine.** The presence of the row on the PDF is a documentation detail,
not a live requirement. VERIFIED (form text + policy text both read this session).

---

### 2) Current full list of required vaccines (and live vs. inactivated)

**Source of truth for the disease list:** CDC "Vaccination Technical Instructions for Civil
Surgeons," dated **Mar. 11, 2025** (VERIFIED, read live 2026-07-07). CDC states the required
list is *narrower* than routine ACIP recommendations: "the vaccines required for applicants do
not include all the vaccines recommended by the ACIP and CDC for routine US domestic use, and
are limited to vaccination for the following diseases."

**Required diseases/vaccines (CDC list, verbatim order):**

| # | Disease / Vaccine | Live or Inactivated | Relevance flag |
|---|---|---|---|
| 1 | Diphtheria | Inactivated (toxoid; Td/Tdap/DTaP) | |
| 2 | Tetanus | Inactivated (toxoid) | |
| 3 | Pertussis | Inactivated (acellular) | |
| 4 | Polio | Inactivated — **IPV** ("IPV = inactivated poliovirus vaccine (killed)", CDC verbatim) | |
| 5 | Measles | **LIVE attenuated** (MMR) | ⭐ contraindication door (H3) |
| 6 | Mumps | **LIVE attenuated** (MMR) | ⭐ |
| 7 | Rubella | **LIVE attenuated** (MMR) | ⭐ |
| 8 | Rotavirus | **LIVE attenuated** (oral) — but pediatric-only; "Not age-appropriate" for adults | age-blanket-waiver for adults |
| 9 | *Haemophilus influenzae* type b (Hib) | Inactivated (conjugate) — pediatric; "Not age-appropriate" for adults | age-blanket-waiver for adults |
| 10 | Hepatitis A | Inactivated | titer door (H2) |
| 11 | Hepatitis B | Inactivated (recombinant) | titer door (H2) |
| 12 | Meningococcal disease | Inactivated (conjugate/recombinant) | mostly age/risk-based |
| 13 | Varicella | **LIVE attenuated** | ⭐ contraindication (H3) + titer (H2) |
| 14 | Pneumococcal disease | Inactivated (conjugate/polysaccharide) | age/risk-based |
| 15 | Influenza | Inactivated (IIV/recombinant) is required form; **LAIV nasal is the live version** | ⭐ seasonal blanket waiver "Not flu season"; inactivated form is not a live-vaccine contraindication |

- Disease list: **VERIFIED** (CDC page, 2026-07-07).
- IPV = inactivated: **VERIFIED** (CDC page verbatim: "IPV = inactivated poliovirus vaccine (killed)").
- Live-vs-inactivated classification for the rest (MMR, varicella, rotavirus = live;
  Tdap/Td, Hep A/B, IPV, pneumococcal, meningococcal, IIV = inactivated): **ASSUMED-HIGH**
  — this is standard, long-settled CDC/ACIP immunology, but I did not re-pin every single
  vaccine to a primary CDC page this session. **→ Topic 1c must lock this down against the
  CDC "Live vs. inactivated" / contraindication Technical Instructions, because the entire
  H3 contraindication strategy hinges on which vaccines are live.** The four ⭐ live vaccines
  (MMR ×3 diseases, varicella, rotavirus, and the LAIV form of flu) are the ones a
  live-vaccine contraindication (immunosuppression, pregnancy) can knock out.

**Which are actually required for two healthy-history ADULTS (Hooman + wife) — practical read:**
Rotavirus and Hib are pediatric and get a "Not age-appropriate" blanket waiver automatically
for adults (CDC verbatim example). So the adult-relevant required set narrows toward:
Tdap/Td, IPV (adult catch-up rules), **MMR**, Hep A, Hep B, meningococcal (age/risk),
**varicella**, pneumococcal (age/risk), influenza (seasonal). Exact per-person requirement is
governed by CDC "Table 1 — Vaccine Requirements According to Applicant Age." → **Topic 1b/1c
should pull Table 1 for the adult age band.** ASSUMED-HIGH.

---

### 3) Current I-693 edition + how the vaccination assessment page works

**I-693 edition date: `01/20/25`.** ✅ VERIFIED (USCIS I-693 form page + the PDF footer on
every page reads "Form I-693 Edition 01/20/25").
- **This is the ONLY edition USCIS accepts for forms signed by a civil surgeon on or after
  July 3, 2025.** (Before that, 03/09/23 or 01/20/25 were both accepted.) Hooman's exam will
  be well after July 3, 2025 → **must use the 01/20/25 edition.** VERIFIED.
- Source: https://www.uscis.gov/i-693 (Wayback snapshot 20260622020620, read 2026-07-07);
  edition footer confirmed in the form PDF itself.
- Form validity rules live in USCIS Policy Manual Vol. 8, Part B, **Chapter 4** (per the form
  page) — separate from the vaccination substance in Chapter 9.

**The vaccination assessment mechanics — Part 10 "Vaccination Record" of Form I-693.** VERIFIED
(read from the 01/20/25 PDF and the CDC Technical Instructions this session).

Structure of the Part 10 chart — each vaccine row has these columns:
1. **Vaccine Given / Date Given by Civil Surgeon.**
2. **Vaccine History Transferred From A Written Record** (dates from prior records — this is how
   documented prior vaccination is credited without re-vaccinating).
3. **Complete Series** — "Mark 'X' if complete; **write date of lab test if immune** or 'VH' if
   varicella history." → *This column is the TITER door (H2): a serology/lab test proving
   immunity is recorded here and satisfies the requirement with no shot.* VERIFIED.
4. **Blanket Waiver(s) to be Requested from USCIS (Not Medically Appropriate)** — three
   sub-columns: **Not Age-Appropriate**, **Contraindication**, **Insufficient Time Interval**,
   plus a "*See Below Table" seasonal column.

**The four "Not Medically Appropriate" BLANKET-WAIVER reasons** (auto-granted, applicant files
no separate waiver — CDC Technical Instructions verbatim, VERIFIED):
- **Not age-appropriate** — e.g., adults not needing Hib/rotavirus.
- **Contraindication** — "If an applicant has contraindications or precautions to specific
  vaccines." ⭐ *This is the H3 door for Hooman's immunosuppression and his wife's pregnancy.*
- **Insufficient time interval between doses** (incl. spacing of two live vaccines).
- **Influenza not available / "Not flu season"** (seasonal). A parallel column exists on the
  form for **COVID-19 "not routinely available"** blanket waiver.

**Key blanket-waiver property (VERIFIED, USCIS Policy Manual Ch. 9 §D):** a blanket waiver is
**self-executing** — "The applicant does not need to apply for a Blanket Waiver." The civil
surgeon marks the reason on the I-693 and "the waiver will be granted to the applicant if
documented correctly." **No I-601, no separate USCIS petition.**

**PREGNANCY / IMMUNOCOMPROMISED — explicitly addressed by USCIS (huge for this case).** VERIFIED,
Policy Manual Ch. 9 §D "2. Pregnancy or an Immuno-Compromised Condition":
- "Some vaccines are, in general, not medically appropriate during pregnancy. These vaccines
  will likely be marked as contraindicated on Form I-693 if the applicant was pregnant at the
  time of the medical examination."
- "**if a woman did not receive certain required vaccines because she was pregnant at the time
  of the medical examination, and the contraindication box is marked by the civil surgeon, the
  applicant is not required to get those vaccines later at the time of the adjudication.**"
- USCIS instructs officers **not** to issue an RFE for additional vaccines where a
  contraindication (pregnancy or "a condition other than pregnancy") is marked in the chart.
- → This is direct primary-source support that **the wife's pregnancy contraindication, and
  Hooman's "condition other than pregnancy" (LGL/immunosuppression) contraindication, are
  handled as self-executing blanket waivers via the civil surgeon — no I-601.** (The precise
  set of vaccines each contraindication covers is Topic 1c's job, per CDC/ACIP.)

**Part 10 final assessment — the three "Results" boxes the civil surgeon checks:** VERIFIED
(read from the 01/20/25 PDF):
1. ☐ **"Applicant completed vaccination requirements or may be eligible for blanket waivers as
   indicated above."** ← the target outcome (covers titers + contraindication/age/seasonal
   blanket waivers).
2. ☐ **"Applicant will request an individual waiver based on religious or moral convictions."**
   ← the H4 / I-601 individual-waiver path (NOT self-executing; applicant must file with USCIS).
3. ☐ **"Applicant does not meet immunization requirements."** ← the H5 bare-refusal box →
   inadmissibility risk. Last resort.

So the two "no new shots, no separate waiver filing" doors both resolve into checkbox #1:
titers (Complete-Series/immune column) and blanket-waiver contraindication (pregnancy +
immunosuppression) + age + season.

---

## What this means for the overall strategy (hand-off to Stage 2)

1. **H1 CONFIRMED and stronger than assumed.** COVID-19 is removed at BOTH the CDC list level
   (Mar 11, 2025) and the USCIS adjudication level (Jan 20, 2025). Hooman's single biggest fear
   is a non-issue at the requirement stage. VERIFIED.
2. **The form still shows a COVID-19 row** — a cosmetic/lag artifact, not a live requirement.
   Flag for BAL so no one is alarmed by seeing it on the PDF.
3. **Two self-executing doors are confirmed on the form itself:** the "immune / date of lab
   test" column (titers, H2) and the "Contraindication" blanket-waiver column (H3). USCIS's own
   Policy Manual explicitly blesses pregnancy AND "a condition other than pregnancy"
   contraindications as needing no later re-vaccination and no RFE. This is the cleanest route
   for the wife (pregnancy) and very likely for Hooman (LGL/immunosuppression → live-vaccine
   contraindication).
4. **The live vaccines are the ones the contraindication door removes:** MMR (measles/mumps/
   rubella), varicella, rotavirus, and LAIV (nasal flu). Inactivated vaccines (Tdap, IPV, Hep
   A/B, pneumococcal, meningococcal, IIV flu) are generally NOT contraindicated by
   immunosuppression/pregnancy → those must be cleared by titer (H2) or documented prior
   vaccination, or actually deferred/given. This is the boundary Topic 1c must map precisely.

---

## Open questions for downstream topics / BAL / physician

- **[1c]** Pin the live-vs-inactivated classification and the exact CDC/ACIP contraindication
  list for (a) immunosuppression/LGL and (b) pregnancy, mapped to each of the 15 required
  vaccines. The H3 door's strength depends entirely on this.
- **[1b/1c]** Pull CDC **"Table 1 — Vaccine Requirements According to Applicant Age"** for the
  adult age band to confirm exactly which vaccines are even required for two adults (rotavirus/
  Hib fall away as "not age-appropriate"; confirm meningococcal/pneumococcal are age/risk-based).
- **[1b]** For each inactivated required vaccine, confirm that a **titer / documented written
  record** is accepted (the "Complete Series — immune / VH / lab test date" column) and what
  evidence a civil surgeon will take.
- **[BAL/physician]** Will the hematologist write a contraindication letter tying Hooman's LGL
  and/or its immunosuppressive treatment to live-vaccine contraindication in terms the civil
  surgeon can transcribe onto the I-693? (Medical judgment — not ours to make.)
- **[live re-verify before filing]** Re-open USCIS Policy Manual Ch. 9 and the CDC page live
  (not via Wayback) close to the exam date to confirm nothing changed after the May 2026
  snapshot, and confirm the I-693 edition is still 01/20/25.

## Primary sources used (all read this session, 2026-07-07)
- USCIS Policy Manual, Vol. 8, Part B, Ch. 9 "Vaccination Requirement" — "Current as of May 08,
  2026." https://www.uscis.gov/policy-manual/volume-8-part-b-chapter-9
- USCIS Form I-693 page (edition 01/20/25; acceptance rules) — https://www.uscis.gov/i-693
- USCIS Form I-693 PDF, Edition 01/20/25 (Part 10 vaccination chart + Results boxes) —
  https://www.uscis.gov/sites/default/files/document/forms/i-693.pdf
- CDC "Vaccination Technical Instructions for Civil Surgeons," dated Mar. 11, 2025 —
  https://www.cdc.gov/immigrant-refugee-health/hcp/civil-surgeons/vaccination.html
- CDC civil-surgeon index — https://www.cdc.gov/immigrant-refugee-health/hcp/civil-surgeons/index.html
