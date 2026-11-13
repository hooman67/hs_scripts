# DECISIONS — choices Hooman & I made, with rationale

Last updated: 2026-11-08 by Codex.

## 2026-11-08 — [RESEARCHER RECOMMENDATION, NOT YET USER-CONFIRMED] Adobe layoff contingency

- Do not ask BAL to pause AOS solely to preserve a possible visitor entry. Ask BAL today for an
  immediate filing decision while Adobe's offer may still be bona fide, conditional on the I-140,
  visa availability, Supplement J, and current employer intent.
- Open the official Lincoln parental-leave case now and coordinate/recode the December 1 PTO entry.
  Parental leave cannot begin before birth. Do not treat parental or medical leave as RIF immunity.
- Use medical leave only if the provider genuinely certifies current inability to work. Before doing
  so, obtain Lincoln's written calculation of how it affects the rolling FMLA/CFRA balance and the
  subsequent 16-week parental benefit.
- Do not depart the United States after I-485 filing without approved Advance Parole and BAL advice.
  Do not rely on visitor reentry as the primary delivery-continuity plan.
- Prepare COBRA continuity before a possible November employment end because active Adobe coverage
  could terminate November 30, immediately before the December 1 due date.

## 2026-10-02 — Wife's no-record/no-titer calculation
- For the stated case, report three expected I-693 injections: Tdap, first HepB dose, and injected
  current-season influenza. Do not advise MMR, varicella, or nasal-spray LAIV during pregnancy.
  Treat IPV as a pregnancy precaution normally handled by the civil surgeon's contraindication
  blanket waiver unless a separate immediate polio-exposure risk changes the clinical judgment.
- Explicitly correct the earlier “pregnancy exempts only live vaccines” framing because it omitted
  the IPV precaution. Keep Hashimoto's/levothyroxine out of the exemption analysis because neither
  creates a vaccine contraindication on the current facts.

## 2026-09-23 — Chest X-ray facility recommendation
- Recommend Valley Radiology East San Jose as the first non-Sutter option because it is the
  closest verified weekday walk-in X-ray site found near 95121 and its official live feed showed
  remaining same-day capacity at the check time. If same-day capacity expires, use its 8 a.m.
  weekday opening or the Samaritan/Ciro walk-in backups.
- Do not treat the presence of Aetna on the provider's payer list as proof that Hooman's exact PPO
  product is in network; confirm by phone before service. No appointment was booked and no medical
  information was uploaded during the search.

## 2026-09-23 — Positive QuantiFERON
- Recommend proceeding with the required low-dose digital PA chest X-ray rather than attempting
  repeat testing as an immigration workaround. A repeat IGRA/T-SPOT can still be discussed with
  a TB/ID clinician for medical confidence.
- Because Hooman has LGL leukemia, route any latent-TB treatment decision through hematology and
  infectious disease after active disease is excluded; exact immune-affecting medications remain
  a required input. No claim is made that the positive is active TB or that it is a likely false
  positive.

## 2026-09-17 — Proceed with I-693; price-check the laboratory package
- Do not delay the I-693 merely because Form I-485 changes on September 18; the medical form is
  unchanged and can be completed in parallel with BAL's I-485 redraft.
- Do not attempt to substitute family-doctor-ordered TB/syphilis tests. Ask Ask For Cure to
  itemize the $120 package and whether its civil-surgeon orders can be billed to insurance. If
  necessary, compare the all-in price with Dr. Deborah Salom, whose site says outside labs may use
  insurance. Do not compare only the lab component.
- Correct BAL's record that no September 22 appointment was actually made, then ask when it wants
  the sealed I-693 and photographs.

## 2026-09-15 — Civil-surgeon selection gate
- Recommend Dr. Vinit Kumar Agrawal first because both designation and the office's titer/record
  workflow are publicly documented. Do not equate the general policy with acceptance of Hooman's
  specific Labcorp report: upload it and obtain an individualized confirmation before payment or
  attendance. Keep Dr. Deborah Salom and Dr. Gina Bui as backups.
- Treat Form I-693 as the only routine doctor-signed form in Hooman's described employment-based
  I-485 packet; route the sealed result through BAL and let BAL identify any case-specific exception.

## 2026-09-14 — Flu-availability research scope
- Hooman clarified that "earliest available" means the 2026–27 vaccine at any provider, including a
  medical office, in San Jose city and Los Angeles city; he wants the earliest likely date, not
  filing-grade proof or proof tied to a particular exam date.
- Report July 30, 2026 for both cities as the earliest documented/defensible nationwide-availability
  date, while explicitly avoiding the stronger unsupported claim that every branch stocked it that
  day or that no private office could have offered it earlier.

## 2026-09-11 — Narrowed current vaccine-list scope
- Hooman asked for the exact list for **him only**, age **35**, for an anticipated **October 2026**
  civil-surgeon exam, and explicitly deferred LGL/treatment/contraindication analysis. The answer is
  therefore an age-table + records/titer analysis, not a medical-contraindication opinion.
- Decision-support should state six applicable rows but must not equate them with six automatic
  injections; actual doses depend on Hooman's unidentified titer and dated records.
- After reviewing Hooman's July 2026 Labcorp titer, treat HepB and varicella as titer-cleared and
  measles/mumps as immune components, subject to civil-surgeon acceptance. Do not treat the MMR row
  as cleared because rubella is non-immune; MMR remains on the practical list unless records or a
  genuine contraindication resolve it. Do not store the source PDF or unnecessary PHI in git.

## 2026-07-07 — Project created
- **Adopted the sibling-project operating model** (fin_research / auto_research): single
  CLAUDE.md source of truth + four living records, organize-by-topic, parallel subagents with
  serialized dependent steps, cite/quantify/mark-confidence, ask on scope decisions.
- **Reframed the problem from 2 strategies to a 5-door priority stack** (H1→H5, see
  research-plan.md §0). Rationale: the exemption space is richer than "religious waiver," and
  the no-shot/no-waiver doors (verify-COVID-gone, titers, contraindication) are both lower
  risk and likely sufficient — worth exhausting before the high-friction waiver.
- **Added a hard truthfulness guardrail** (CLAUDE.md §5): no path may involve
  misrepresentation; "vaccine-conscious doctor" = one who *properly documents genuine*
  exemptions, never one who fabricates. Rationale: misrepresentation = permanent immigration
  bar, categorically worse than a vaccine.
- **Framed all output as decision-support for BAL + a physician**, not as advice or action.

## 2026-07-08 — Folded the 7 Stage-5 red-team corrections into recommended_path.md
Per Hooman's instruction. All 7 fixes applied: (1) H3-Hooman downgraded from "guarantee/4.8
co-lead" to contingent-possibly-unavailable, titers made his primary door; (2) pneumo/mening
boomerang added as §1.5 risk; (3) headline reframed "plausibly zero shots" → "~1 Td/Tdap each
unless dated dose <10yr"; (4) wife's ordering flipped to titers-primary, pregnancy-backstop;
(5) hematologist ask rewritten as strictly neutral ("is he severely immunosuppressed?");
(6) religious waiver stated as hard "do NOT attempt with his stated reasons" (§1.6); (7) live-
re-verify hard gate + date-discrepancy resolution added to appendix. red_team_review.md kept
as the companion critique. Rationale: the pre-fix draft's "guarantee/zero-shots" framing was
the exact pressure that could point a clinician at the misrepresentation line.

## 2026-07-08 — New medical fact: wife has Hashimoto's thyroiditis
Hooman asked whether pregnancy + Hashimoto's lets his wife avoid ALL vaccines. Launched a
focused primary-source research agent → `exemptions/wife_pregnancy_hashimotos.md`. CONFIRMED (VERIFIED-HIGH, file written): three primary CDC/ACIP sources fetched live 2026-07-08.
Decisive: CDC ACIP Contraindications Table 4-2 explicitly lists "Autoimmune disease" among
conditions *incorrectly perceived* as contraindications; Hashimoto's/levothyroxine appears
NOWHERE in Pinkbook Ch.2 contraindications or the Altered-Immunocompetence definition →
Hashimoto's opens ZERO doors (live or inactivated). Pregnancy shields only LIVE vaccines (MMR,
varicella, LAIV); Tdap + inactivated flu are RECOMMENDED in pregnancy. Honest answer: NO — she
cannot avoid all vaccines; her path = titers-first → records → pregnancy backstop (live rows
only) → shot last, same Td/Tdap pinch point as Hooman. Guardrail held (agent refused to
manufacture a door). One caveat: USCIS mechanics inherited VERIFIED via proxy — re-verify live
via BAL near exam. File: exemptions/wife_pregnancy_hashimotos.md.

## 2026-07-07 — Scoping answers from Hooman (reshapes the ranking)
- **Vaccine history: "Yes, various over my life."** CONSEQUENCE: the religious/moral waiver
  (H4) "opposed to vaccination in ANY form" test is now **weak/likely unavailable** — prior
  vaccines undercut sincerity of a categorical objection. Conversely, **titers (H2) are
  PROMOTED to a lead door** — he may already be immune to MMR/varicella/Hep B from those
  prior shots, clearing them with a blood test and zero new shots. Net: door priority shifts
  to **H1 (verify COVID gone) → H2 (titers) → H3 (contraindication) → [H4 demoted] → H5**.
- **Wife IS a co-applicant** (her own I-485 + I-693). Her pregnancy is a live-vaccine
  contraindication that matters for the case → research her path in PARALLEL with his.
- **Prepare TWO packets:** one for BAL (legal/filing), one for his hematologist/civil surgeon
  (medical contraindication + titer documentation).
- **No hard deadline** → optimize for lowest-risk, most durable path over speed. The slow
  I-601 waiver's main disadvantage (time) matters less, but it's demoted anyway on the
  sincerity problem above.
