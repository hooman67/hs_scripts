# Property Research Project State

**Canonical session handoff**

**As of:** 2026-09-28  
**Workspace:** `/home/colligo/hs_scripts/claude/prop_research`  
**Git repository root:** `/home/colligo/hs_scripts`  
**HEAD before this handoff:** `17526724c607e30d18069b0bb9a5cc50afce945d` (`main`, synchronized with `origin/main` when inspected)

This file lets a new agent continue without relying on conversation history. It records state and routing; underlying evidence remains in the linked project files. If this file conflicts with a current primary source, current user input, or a more specific active project artifact, investigate and update it rather than silently choosing.

## Start here in a new session

1. Read `/home/colligo/hs_scripts/claude/prop_research/AGENTS.md` completely.
2. Read `/home/colligo/hs_scripts/claude/prop_research/RESEARCH_METHODOLOGY.md` completely.
3. Read this file and `/home/colligo/hs_scripts/claude/prop_research/README.md`.
4. Read the summary file for the project being resumed.
5. Run `git -C /home/colligo/hs_scripts status --short` and preserve unrelated changes.
6. Refresh every time-sensitive claim before using it. Most current research was collected on 2026-09-10 through 2026-09-12 and is stale for a “current market” statement on 2026-09-28.
7. Do not use `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/legacy/` as evidence.

If the user says only “continue,” resume the principal-residence Gate B work described below because that was the latest active research thread. Do not activate the tracker or fan out cities yet.

## Non-negotiable research protocol

- Label every material claim with one evidence status: `PRIMARY`, `SECONDARY`, `QUOTED`, `INFERRED`, `ESTIMATE`, `SPECULATIVE`, `CONFLICTED`, or `UNKNOWN`.
- Separately label confidence `HIGH`, `MEDIUM`, `LOW`, or `UNKNOWN`.
- Direct user statements are `PRIMARY` evidence for the user's own preferences and circumstances.
- Open every cited source. Search snippets and prior-agent prose are not verification.
- Store atomic claims in a 20-column evidence ledger as specified by `/home/colligo/hs_scripts/claude/prop_research/RESEARCH_METHODOLOGY.md`.
- Preserve raw facts separately from calculations, scores, and recommendations.
- Never convert missing evidence into a neutral or favorable score.
- Do not rank until completeness gates pass; do not infer address-level schools, hazards, insurance, or commute from citywide data.
- Parallelize independent collection after a representative pilot teaches the schema. Do not fan out across a shared unresolved learning dependency.
- Automated scraping of restricted consumer portals is out of scope. Use authorized exports/APIs, official public data, or approved manual browser observations.

## User decisions currently in force

### Principal residence

These are direct user inputs unless explicitly marked as analytical policy:

- Approximately USD 600,000 in deployable savings: about USD 300,000 cash and USD 300,000 invested. The invested portion is freely deployable; tax basis/liquidation cost remains unknown.
- Housing ceiling is USD 5,000–7,000/month. It includes mortgage, property tax, required insurance, HOA, maintenance, and utilities. Private/Montessori tuition is outside this ceiling.
- Use USD 6,000/month as the working target and USD 7,000 as the hard economic-carry ceiling. `INFERRED | HIGH`.
- Primary office: Adobe, 345 Park Ave, San Jose, CA 95110, Tuesday through Thursday. Arrival time is flexible.
- Recurring one-way commute target is at most 60 minutes; 90 minutes is the hard bad-day boundary. `INFERRED | MEDIUM` from the user's wording.
- The San Francisco Adobe office is a real secondary option, but San Jose is preferred because it is headquarters.
- Seattle-area homes are authorized for a later relocation phase. Keep Seattle separate from the Bay Area ranking.
- Principal home must be a detached house with at least three bedrooms and a backyard.
- Yard must work for two young children and a dog. Current analytical bands: under about 800 usable square feet requires review; 800–1,200 may be acceptable; over 1,200 is preferred. These are `ESTIMATE | MEDIUM`, not user-stated cutoffs.
- Prefer no HOA. Current analytical bands: USD 1–200 acceptable after document review; USD 201–350 review; over USD 350 presumptive screen-out unless it replaces material costs. `INFERRED | MEDIUM`.
- Home should be habitable, financeable, and insurable at closing. Renovation policy: up to USD 50,000 acceptable; USD 50,001–75,000 requires contractor-supported scope and at least 20% contingency; larger or structural/full-gut projects are outside the standard search. `INFERRED | MEDIUM`.
- Schools matter strongly because there are two young children, but school quality must trade off against other factors. Montessori and homeschooling are acceptable possibilities.
- Do not use one school-rating cutoff. Verify the assigned public path and compare multi-year academics, growth where available, chronic absenteeism, climate/suspension, program fit, and logistics. Keep alternatives and tuition separate. `INFERRED | MEDIUM`.
- Former health-policy constraint is removed from principal-residence research.
- Purchase horizon is within about three years; sooner only for an unusually good deal that passes full diligence.
- Holding policy: plan for at least seven years and prefer ten. `INFERRED | MEDIUM`.
- Preserve at least USD 150,000 post-close liquidity; prefer USD 175,000–200,000 when renovation/hazard uncertainty is high. `INFERRED | MEDIUM`.
- Hazard policy and insurance stress tests are in `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/gate_a/02_affordability_holding_hazard_policy.md`.
- Manual Google Maps commute observations are approved.
- Exact candidate addresses and map screenshots may be stored in this private repository, subject to any MLS/export license.
- The user thinks a buyer-agent MLS export is probably obtainable but has not yet obtained one.

### Income and enjoyment property

- Separate project from the principal residence.
- Approximately USD 300,000 capital; prefer cash or a large down payment because rates are high.
- United States and Canada are in scope.
- Legal, remotely manageable LTR, STR, seasonal, mixed-use, or land-first models may be considered.
- The property should generate income and provide enjoyment: beach/lake/mountain/forest, projects/gardening/homestead potential, or compelling amenities.
- Wife especially values beach access.
- No market or property is currently recommended.

## Principal-residence project state

**Summary:** `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/principal_around_silicon_valley.md`

### What is complete

- The old model's 156 files were reorganized under `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/legacy/` and treated as untrusted historical input.
- The legacy defect audit documented incompatible scoring systems, missing claimed source-of-truth files, stale/geographically mismatched inputs, unsupported professional claims, and incorrect calculations. See `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/foundation/04_legacy_defect_audit.md`.
- Gate A criteria and provisional policies are recorded:
  - `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/gate_a/01_decision_inputs_v1.md` (file path retained; document title is v2)
  - `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/gate_a/02_affordability_holding_hazard_policy.md`
  - `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/gate_a/03_property_and_school_tradeoff_policy.md`
- A reproducible affordability calculator exists at `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/calculations/affordability_scenarios.py` with generated CSV beside it.
- At the 2026-09-10 Freddie Mac 6.76% benchmark and explicit estimates (1.20% tax, USD 300/month insurance, USD 500/month utilities, 1% annual maintenance, no HOA), the modeled price envelope was roughly USD 738,000–979,000 with USD 300,000 down or USD 816,000–1,057,000 with USD 400,000 down across the USD 5,000–7,000 ceiling. This is `ESTIMATE | MEDIUM` and is stale; refresh the mortgage rate and all property-specific inputs before reuse.
- Candidate universe includes Fremont, San Mateo, Pleasanton, Dublin, Berkeley-area alternatives, Willow Glen/San Jose alternatives, San Carlos, Belmont, fresh comparators, and a later Seattle phase. See `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/foundation/02_candidate_universe.md`.
- One Fremont pilot was run sequentially and independently audited. It defined six official City of Fremont neighborhood polygons: Ardenwood, Centerville, Irvington, Mission San Jose, Niles, and Warm Springs.
- Fremont pilot validated official boundary, CDE school identity/outcome, parcel/tax lookup, FEMA flood schema, and transit source components. It did not rank or recommend a submarket.
- Fremont evidence contains 30 validated claims plus a 17-claim source-unblock ledger:
  - `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/pilots/fremont/evidence/claims.csv`
  - `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/pilots/fremont/evidence/unblock_source_claims_2026-09-12.csv`
- A source audit found:
  - manual public MLSListings workflow can support current active/contingent/pending discovery but not the required recent closed cohort;
  - Alameda County transfer data was stale and lacked beds/lot/yard/condition/arms-length fields;
  - a licensed agent/MLS export is the preferred source for current closed comps;
  - manual Google Maps observations are the approved route-data method;
  - no unattended portal scraper should be built.

### Gate B status

**NOT PASSED. This is not a rejection of Fremont. Do not fan out city research yet.**

Outstanding shared blockers:

1. Current closed-sale and current inventory observations for detached 3+ bedroom homes with usable yards, joined to official neighborhood polygons.
2. Repeated manual commute observations to 345 Park Ave across the approved flexible time grid.
3. Address-level elementary/middle/high-school assignments plus broader multi-year evidence.
4. Current adopted wildfire layer, parcel flood/geologic overlays, and property-specific insurance deferral/quotes.
5. Remaining completeness-plan categories or an explicit coordinator-approved narrowing of Gate B.

### Prepared manual inputs

- Copyable buyer-agent request: `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/data/manual_inputs/mls_export_request.md`
- Commute CSV schema: `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/data/manual_inputs/commute_observations_template.csv`
- Exact addresses/screenshots may be stored. Before ingesting an MLS file, preserve its license/retention restrictions and exclude confidential agent remarks or occupant information.

### Next principal-residence actions, in order

1. Check `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/data/manual_inputs/` for a newly supplied MLS CSV/XLSX.
2. If no export exists, help the user obtain one using `mls_export_request.md`; do not manufacture closed comps from portal snippets.
3. Collect the approved manual commute sample only after freezing two representative residential origins per Fremont polygon. Keep planned and live observations separate.
4. Join any supplied listing/export addresses to Alameda APNs and the frozen Fremont polygons; preserve raw statuses and missingness.
5. Verify property/representative-address school assignment, current hazards, taxes, HOA, yard, condition, and insurance handling.
6. Rerun and independently audit Fremont Gate B. Apply schema lessons from `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/pilots/fremont/schema_lessons.md`.
7. Only after Gate B passes, parallelize comparable candidate collection into separate files; centralize schema changes, synthesis, scoring, and disconfirmation review.
8. Produce an audited shortlist before activating market tracking.
9. Evaluate Seattle as a later, separate relocation phase, not inside the Bay Area commute score.

## Housing-tracking project state

**Summary:** `/home/colligo/hs_scripts/claude/prop_research/tracking_housing_process/tracking_housing_process.md`

- Methodology research is complete at `/home/colligo/hs_scripts/claude/prop_research/tracking_housing_process/analysis/tracking_methodology_research.md`.
- Evidence ledger has 21 validated claims at `/home/colligo/hs_scripts/claude/prop_research/tracking_housing_process/evidence/source_claims_2026-09-10.csv`.
- Supported design is vintage-preserving: authorized MLS/API/agent exports for listing data, official government sources for validation/context, permitted manual inputs, and address-specific diligence.
- Repository-local skill exists at `/home/colligo/hs_scripts/claude/prop_research/.agents/skills/track-housing-market/SKILL.md`.
- Config is `/home/colligo/hs_scripts/claude/prop_research/tracking_housing_process/config/tracker_config.json` with status `AWAITING_AUDITED_SHORTLIST`, zero markets/cohorts/sources, and no alert rules.
- Skill validator was independently forward-tested and passed. It correctly refuses an active run without the shortlist, completed pilot, authorized sources, and reviewed rules.
- Do not improvise tracker markets. Do not run monitoring until the principal-residence shortlist and first source-qualified market pass their gates.

## Income-and-enjoyment project state

**Summary:** `/home/colligo/hs_scripts/claude/prop_research/income_and_enjoyment_property/income_and_enjoyment_property.md`

- Phase-one screening/underwriting foundation is complete; no investment recommendation exists.
- Foundation: `/home/colligo/hs_scripts/claude/prop_research/income_and_enjoyment_property/analysis/foundation/phase_1_foundation.md`
- Evidence ledger: `/home/colligo/hs_scripts/claude/prop_research/income_and_enjoyment_property/evidence/claim_ledger.csv` (22 claims when created)
- Official notes: `/home/colligo/hs_scripts/claude/prop_research/income_and_enjoyment_property/evidence/official_source_notes_2026-09-10.md`
- Sequential learning pilots selected, not recommended:
  1. Panama City Beach, Florida: professionally managed beach-condo STR archetype.
  2. Canmore, Alberta: existing, correctly designated Tourist Home archetype.
- Do Panama City Beach first, audit it, revise the schema, then do Canmore. Do not parallelize these pilots because the U.S. pilot's lessons are intended to shape the Canadian pilot.
- Before an investment ranking, resolve current tax residency/immigration/ownership, minimum return and negative-cash-flow tolerance, hold/personal-use pattern, management effort, and risk/illiquidity limits.
- All September 10 legal/tax/rule findings require a current-source refresh before decision use.

## Important lessons already learned

1. **The monthly ceiling, not the old USD 2 million number, is the binding principal-residence constraint.** Price must be derived from live rates, taxes, insurance, HOA, utilities, maintenance, down payment, and reserves.
2. **A city is too coarse.** Use explicit submarket polygons and parcel/address joins for property, schools, tax, hazards, and route origins.
3. **A citywide median cannot answer whether qualifying detached 3+ bedroom homes with usable yards are affordable.** Current licensed/property-level observations are required.
4. **Lot size is not usable-yard evidence.** Preserve lot square feet, then separately classify yard evidence from photos/aerials/visit.
5. **School identity, outcomes, and address assignment are three different evidence objects.** Do not substitute one for another or reduce school quality to one rating.
6. **One route estimate is not “the commute.”** Store each dated origin/destination/time/mode observation and report distributions/upper tails.
7. **Hazard layer title is insufficient.** Store map adoption/effective/version status; the accessible Fremont fire layer was too old for current policy.
8. **Public county transfer data is useful corroboration but not sufficient current comp data.** It lacked the necessary dwelling fields and was stale in the Fremont pilot.
9. **Evidence type and confidence are independent.** A primary source can still be low confidence for the decision if stale or geographically mismatched.
10. **Do not parallelize before learning stabilizes the schema.** Fremont must teach the Bay Area process; Panama City Beach must teach the investment-property process before equivalent fan-out.
11. **Tracker activation follows selection, not the reverse.** The local skill exists but must remain paused until markets, cohorts, authorized sources, and alert rules are audited.

## Validation commands

Run from `/home/colligo/hs_scripts/claude/prop_research`:

```bash
python principal_around_silicon_valley/analysis/calculations/affordability_scenarios.py
python principal_around_silicon_valley/analysis/pilots/fremont/calculations/validate_pilot.py
python .agents/skills/track-housing-market/scripts/validate_config.py
git -C /home/colligo/hs_scripts diff --check
```

Expected at handoff creation:

- Fremont ledger validator passes 30 unique claims.
- Tracker schema validates but reports `activation_ready: false` and `status: AWAITING_AUDITED_SHORTLIST`.
- Affordability CSV regenerates from explicit assumptions.
- No tracked `__pycache__` file should be added.

## Git and file-integrity note

- The worktree was clean at `17526724c607e30d18069b0bb9a5cc50afce945d` before creating this handoff.
- This task intentionally leaves this new `/home/colligo/hs_scripts/claude/prop_research/PROJECT_STATE.md`, the README link/status update, and the AGENTS startup pointer uncommitted.
- During final validation, an unrelated concurrent modification appeared at `/home/colligo/hs_scripts/claude/dev_research/PROJECT_STATE.md`. It is not part of property research and must be preserved, not edited or reverted by this project.
- Preserve any additional users' changes if the live worktree differs when the next session starts.
- No external messages, purchases, account registrations, agent contacts, offers, or transactions were made.
