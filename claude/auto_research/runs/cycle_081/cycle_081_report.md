# Cycle 081 Report — ROUND 4

**Date:** 2026-07-09
**Domain:** Final arborist-domain cycle — deliberately hunting the ONE shape that could still yield a founder-owned flywheel here: a **cross-firm aggregated data "plant"** (the CutLog / TitlePlant class) rather than a single-operator system-of-record. If any defensible #2 candidate exists in tree-risk / PHC, it must be a network/data-aggregation play the SoRs structurally can't be, because they silo each customer's data.
**Founder:** Hooman — AI/ML + software + cloud infra; EE bachelor's; solo/software-preferred; already building CutLog.
**Graduates:** 0 (one CONDITIONAL near-miss documented honestly)
**Verdict:** The aggregation-plant shape is the only intellectually live idea in the domain, but each concrete instance dies on a real blocker: the data is either (a) confidential/liability-loaded and not shareable across firms, (b) already public (municipal inventories, USDA/urban-forest datasets), or (c) too slow-accumulating against a tiny paying universe. No clean graduate. Honest zero for the domain overall.

---

## Method note

Same environment (search CAPTCHAs); direct fetches. This cycle is analysis-heavy (testing a data-strategy hypothesis) rather than incumbent-enumeration, since cycles 078–080 already VERIFIED the SoR incumbents (SingleOps, PlanIT Geo TreePlotter, Arborgold, PestPac/WorkWave, Civica ArborSafe). Confidence marks inline.

---

## Step 1 — 10 ideas scanned (all framed as founder-owned-data-flywheel plays)

| # | Idea | The would-be flywheel | TRL | Step-1 call |
|---|------|----------------------|-----|-------------|
| 1 | Tree-appraisal **comps plant** (species×size×condition×region → $ value) | Cross-firm appraisal comps | 7 | PROMOTE |
| 2 | Species-level **defect→failure outcome** dataset (predict likelihood of failure) | Labeled failure outcomes across firms | 6 | PROMOTE |
| 3 | Regional **pest/disease outbreak** early-warning from aggregated PHC treatment logs | Network treatment data → alerts | 6 | PROMOTE |
| 4 | Anonymized **PHC benchmarking** (what products/rates peers use, at what cost/outcome) | Cross-firm treatment benchmarks | 6 | PROMOTE |
| 5 | Urban-forest **canopy/valuation** dataset resold to insurers/appraisers | Aggregated inventory | 6 | REJECT (S1) — overlaps public i-Tree/USDA + PlanIT Geo NatureScore |
| 6 | **Storm-damage claims** tree dataset for insurers | Claims outcomes | 6 | REJECT (S1) — insurer buyer + data owned by carriers/CoreLogic |
| 7 | Consumer **"CarFax for the tree on your lot"** history at property sale | Per-tree provenance | 5 | REJECT (S1) — consumer, no accumulation mechanism, no buyer |
| 8 | Contractor **price/bid benchmarking** for tree work | Cross-firm pricing | 6 | REJECT (S1) — SoRs (SingleOps/Aspire) sit on this already |
| 9 | TRAQ **inter-rater calibration** dataset (standardize risk ratings) | Assessment consistency data | 5 | REJECT (S1) — ISA-owned methodology; tiny; academic |
| 10 | **Invasive/quarantine spread** model from treatment logs | Aggregated geo-treatment | 6 | REJECT (S1) — gov/APHIS buyer; instant-reject |

4 promoted to Step 2.

---

## Step 2 — Competitive density + Incumbent/OEM + Moat gates

### 1. Tree-appraisal comps plant — **Density 2, CARRY (best-in-domain, but see Step 3)**
- Genuinely under-served (no dominant comps SoR); a real TitlePlant-flavored asset in principle.
- **Moat gate — PARTIAL:** the killer is **data shareability**. Appraisals are confidential litigation/insurance deliverables; arborists have little incentive (and often contractual bars) to pool them. Without contribution, no plant. And the CTLA Trunk Formula is a published method, so the "value" is judgment + comps, and the comps are the exact thing that won't flow. Carry to Step 3 for the size test it will also fail (see cycle 078: RCA universe ~low thousands → ~$3–10M SAM).

### 2. Species defect→failure outcome dataset — **Density 3, REJECT**
- **Moat gate FAIL + founder-fit inversion:** the valuable asset is labeled (defect state → subsequent failure) longitudinal outcomes — **slow to accumulate** (failures are rare, multi-year), **liability-loaded** (a "low risk" prediction that fails = lawsuit), and **better accrued by the big-inventory incumbents** (TreePlotter/ArborNote already hold millions of tree records to label against). A solo entrant cannot out-accumulate them, and the science (biomechanics) is a research problem, not a plumbing one. Reject.

### 3. Regional outbreak early-warning from aggregated PHC logs — **Density 3, REJECT**
- **Moat gate FAIL:** requires a large installed base of contributing PHC firms FIRST (chicken-and-egg), and that base is exactly what the SoRs (Arborgold, SingleOps, RealGreen) already own — they could light up aggregate outbreak alerts from their existing customer telemetry the moment it mattered. Any standalone entrant must win the SoR race first. Also overlaps public/extension pest-alert networks (free). Reject.

### 4. Anonymized PHC/pricing benchmarking — **Density 3-4, REJECT**
- **Incumbent check:** benchmarking is the classic value-add a vertical SoR ships once it has scale (Aspire/ServiceTitan explicitly market industry benchmarks; SingleOps holds the data). The party with the transactions owns the benchmark. A benchmarking-only entrant has no data until it has customers, and the SoRs have both. Reject.

Only #1 carried.

---

## Step 3 — Market (survivor: #1 appraisal comps plant)

- Same result as cycle 078's #8: paying universe = ISA **consulting/registered consulting arborists** doing appraisals — **low thousands** (ASCA membership ~1,500–2,000; RCAs low thousands, ASSUMED). At $1,000–1,500/yr, **SAM ≈ $3–10M**, 10–30× under the $100M gate. Even granting the comps-plant moat, the market is a rounding error, and the contribution-incentive problem (confidential appraisals) means the plant may never reach critical mass.
- **Status: REJECT** — SAM far below gate; countable buyer universe (Round-2 TAB red-flag); flywheel-ignition risk.

No idea reaches Step 4.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 4 | 6 |
| Step 2 | 4 | 1 | 3 |
| Step 3 | 1 | 0 | 1 |
| Step 4 | 0 | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates this cycle: 0.**

**Honest read (domain-level, cycles 078–081):** I hunted the aggregation-plant shape specifically because it's the only one the incumbent SoRs structurally can't own (they silo per-customer data). It's the right instinct, but every concrete instance in this domain dies: appraisal comps = too small + won't-share data; defect-failure dataset = slow, liability-loaded, incumbent-advantaged; outbreak/benchmarking = requires the installed base the SoRs already have. There is no defensible #2 candidate in arborist tree-risk / pesticide compliance for a solo software founder.
</content>
