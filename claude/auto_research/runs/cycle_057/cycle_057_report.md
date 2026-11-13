# Cycle 057 Report

**Date**: 2026-07-09
**Round**: 4 (Domain #2 — Septic / Onsite-Wastewater), cycle 2 of 5
**Agent**: Claude (Opus 4.8, 1M) — discovery Agent B
**This cycle's angle**: The **"septic plant"** data-aggregation play — a TitlePlant analog. Instead of selling software to operators, aggregate per-property septic records into a property-data product sold to buyers/agents/lenders/insurers. (Tests whether the moat can be relocated to an *aggregator* the founder owns.)

---

## Why this angle

Cycle 056 killed the operator-SoR angle: the compounding record leaks to the county portal or a shipping incumbent. Round-3's only survivor (TitlePlant) worked because the operator *accumulates* proprietary data. So the sharpest remaining question for this domain is: **can a solo founder build a proprietary "septic plant" — a regional/national aggregate of septic system records with predictive/valuation value — the way TitlePlant aggregated title data?**

---

## Step 1: Technology Discovery (angle: septic property-data aggregation)

### 1. Regional "septic plant" — aggregate as-built/permit/pumping records into a queryable property database
- **Breakthrough**: County health-dept septic records are increasingly digitized + online (OnlineRME, Oregon DEQ, county GIS); scraping/ingesting + normalizing them is now a data-engineering task.
- **TRL**: 8. **Status**: PROMOTED to Step 2.

### 2. Pre-purchase septic risk report for home buyers/agents (a "CLUE report for septic")
- **Breakthrough**: LLM synthesis of aggregated records + local failure priors into a buyer-facing risk score.
- **TRL**: 7. **Status**: PROMOTED to Step 2.

### 3. Septic-system valuation/depreciation model for insurers/lenders
- **Breakthrough**: Component-age + regional-failure data → remaining-life estimate.
- **TRL**: 6. **Status**: PROMOTED to Step 2.

### 4–10 (rejected at Step 1): drainfield-life prediction (needs private outcome data), homeowner maintenance-reminder app (consumer, no WTP), realtor-disclosure autofill (feature), septic-loan origination (fintech, Round-3 reject), soil-suitability GIS for installers (public NRCS data), septic-comp marketplace (two-sided cold-start), inspector-lead-gen marketplace (thin).

---

## Step 2: Competitive Analysis + ⭐ Incumbent Check + ⭐ Moat Gate

### The fatal structural problem: the source data is PUBLIC and government-held
- Septic as-builts and permits are **public records held by county/state health departments** [VERIFIED — EPA: "permitted and inspected by your local permitting authority"], and increasingly **published online**: Snohomish/Island/Pierce via **OnlineRME** (as-built drawings + service history, homeowner-accessible), **Oregon DEQ** (Curry, Jackson, Josephine + historical Baker/Union/Wallowa), **Clackamas County** ("As-Built record for the entire septic system"), **Tacoma-Pierce County Health** (drainfield info) [all VERIFIED].
- A generic "Septic Search"-style centralized lookup is already referenced as existing [VERIFIED — search excerpt: "a centralized database where you can find information about onsite wastewater systems"].

### ⭐ Moat Gate — the decisive failure (mirror-image of the TitlePlant lesson)
TitlePlant worked because title agents **build their own plant** from records the county does NOT synthesize into a usable product, and the plant compounds privately. **Septic inverts every one of those conditions:**
1. **The government already aggregates and publishes it.** Where the mandate is strongest (WA), the county portal (OnlineRME) *is* the aggregate, free to homeowners. You'd be reselling public data — anyone can replicate it, and the county gives it away.
2. **No unique accumulation.** A founder-aggregator has no privileged pipe; it scrapes the same public sources a competitor (or the county itself) can. This is the "layer on someone else's data" anti-pattern, not the "accumulate your own" pattern.
3. **Fragmentation without a national key.** 3,000+ counties, no standard schema, many still paper — so a *national* plant is a brutal, capital-heavy data-ops slog with no defensibility at the end (the moment it's valuable, the county's own portal or a funded property-data incumbent absorbs it).

### Incumbent/adjacent check (property-data buyers)
- Property-data + disclosure incumbents (title/property-data companies, home-inspection report platforms, real-estate disclosure vendors) are one data-partnership away; septic is a *field* on a property report, not a standalone product. Buyer-facing "septic risk report" = an **absorbable feature** of an existing property report, not a company (Round-3 pattern).
- **Competitive Density: 4/5** (public data + adjacent property-data incumbents). **Moat Gate: FAIL.**

**Status: REJECT at Step 2** for all three ideas — moat accrues to the government (who publishes it free) and to property-data incumbents (who can add the field).

---

## Step 3: Market Analysis (abbreviated)
- Buyer for a "septic plant" data product would be **agents/lenders/insurers** — but that reintroduces the disclosure/property-data incumbents AND drifts toward enterprise/insurer sales (long cycles). The fragmented private operator (the mandated buyer) is NOT the buyer here, violating the domain's Buyer-check gate.
- SAM: a septic add-on field to property reports is a low-single-digit-$M line item, not a $100M+ standalone SAM.
- **Status**: REJECT (SAM + wrong buyer).

## Step 4: Feasibility
- Tech risk: Medium (data-ops across 3,000 counties). Market/moat risk: High. Wrong-buyer risk: High.
- **Feasibility score: 2.5/10.**

## Step 5: Execution Plan — **N/A, no graduate.**

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 3 | 7 |
| Step 2 | 3 | 0 | 3 |
| Step 3–5 | 0 | 0 | 0 |

**Graduates this cycle: 0.**

**Honest read**: The "septic plant" is the anti-TitlePlant. TitlePlant survived precisely because title agents privately accumulate what the county does *not* synthesize; septic records are the opposite — **the government already aggregates and publishes them free** (OnlineRME, DEQ, county GIS), and a buyer-facing septic report is an absorbable field on existing property-data products. The one moat-class that saved Round 3 does not transfer to this domain. Decisive zero.
