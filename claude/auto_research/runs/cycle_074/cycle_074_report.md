# Cycle 074 Report — Marine / Boat Surveying (core)

**Date**: 2026-07-09
**Domain (Round 4 map #6)**: Insurance/lender-mandated marine survey; thesis = surveyor
digitizes the condition report and accumulates a proprietary per-hull condition + comparable-
vessel valuation dataset that becomes a defensible depreciation model.
**Agent**: Round-4 discovery Agent F (cycles 074–077).

**Mandatory gates applied**: (1) incumbent/OEM check, (2) moat-accrues-to-founder, (3) growth+SAM,
(4) fragmented private buyer. This cycle attacks the CORE domain (recreational-vessel condition &
valuation surveys). Cycles 075–077 test adjacent asset-inspection trades and the "valuation plant"
reframe.

---

## Step 1: Technology / Product Discovery (10 candidates)

1. **AI-assisted marine survey report generator** (field notes → ABYC-structured PDF). TRL 8.
2. **Photo-driven defect detection** (corrosion/blister/delamination CV on hull photos). TRL 6.
3. **Per-hull condition-history "vessel Carfax"** (serial/HIN-keyed longitudinal record). TRL 8.
4. **Comparable-vessel valuation model** built from the surveyor's own accumulated survey data. TRL 7.
5. **Moisture-meter / IR-thermography reading logger** (structured capture on existing gear). TRL 8.
6. **Insurer-format compliance auto-formatter** (renders to each carrier's required survey template). TRL 8.
7. **Survey scheduling / renewal reminder on insurance re-survey cadence** (15–20 yr vessels). TRL 9.
8. **Voice-note → finding transcription in the field**. TRL 8.
9. **HIN decode + build-sheet enrichment**. TRL 8.
10. **Standardized deficiency severity classifier (ABYC/NFPA-302)**. TRL 7.

All are software-native, TRL ≥6, <12 mo to product — they PASS Step 1 on readiness. The problem is
downstream (Steps 2–3), so I promote the two that best embody the domain thesis for scrutiny:
**#3 vessel condition-history plant** and **#4 self-built comparable-valuation model** (these are the
only two that could carry the claimed founder-owned data moat). #1/#2/#6 are commodity report-writing
features already shipped by incumbents (see Step 2).

---

## Step 2: Competitive Analysis + MANDATORY Incumbent/OEM Check

**Marine-survey report software is a CROWDED, already-served field** (VERIFIED via vendor pages /
search). At least 8 active products, several launched 2023–2025, one already Claude-powered:

| Product | What it does | Pricing | Note |
|---|---|---|---|
| **FCG Surveyor** (fcgmarine.com) | "AI-powered" field-notes→report, ABYC findings, photo-to-finding, deficiency tracking. Built ON CLAUDE. | **$29.99/mo/surveyor** | Built by a credentialed surveyor; explicitly targets "10,000+ US marine surveyors." |
| **Boat Assessor** (Germany) | Clients, surveys, observations, PDF, cost calc, multi-language | €199/mo | ~15 active users, 235 reports — tiny. |
| **Force 5** | "Leading marine surveying software," report writer | **$50/mo** or lifetime one-time | Long-standing incumbent. |
| **InspectX** (inspectxpro.com) | Report builder, free post-purchase edits | subscription | — |
| **MarineSnap** | Survey app w/ trial | — | — |
| **Yacht Inspector Pro** | Photos, voice notes, "AI-powered documentation" | — | — |
| **RiskCovry / TideWater-class** | narrative report tools | — | — |

**Incumbent verdict**: the "digitize the paper survey + AI report" wedge is **already occupied by
multiple products, including an AI/Claude one at $30/mo** — i.e., exactly the founder's own build,
already shipped by a credentialed insider. Competitive density = **4/5 (REJECT)** for the report-app layer.

**Valuation-data incumbent check (the actual moat)**: the comparable-vessel value data is **already
owned by three entrenched price-guide incumbents** (VERIFIED):
- **BUC (BUCValu / BUC Used Boat Price Guide)** — the surveyor/broker/insurer/bank standard.
- **ABOS Marine Blue Book** — Price Digests; sells via **API integration, subscription, custom data**.
- **J.D. Power (ex-NADA Guides, acquired 2015)** — dealer-transaction-based boat values.

These are the "generally accepted price guides in the U.S." Insurers and surveyors already cite them.
A solo founder cannot out-accumulate a valuation dataset against firms that already aggregate dealer
transactions, auction results, and decades of guide history and **sell it by API**.

---

## Step 2 MOAT GATE (the decisive failure)

The domain thesis claims the surveyor accumulates a **proprietary per-hull condition + comparable-
valuation dataset** no insurer SoR holds. Under scrutiny this moat **does not accrue to the founder**:

1. **Valuation data is pre-owned** by BUC/ABOS/J.D. Power (above). The founder's per-survey data is
   sparse (one surveyor sees a few hundred hulls/yr) vs. guides fed by the whole dealer/auction market.
   The "self-built comparable model" is strictly dominated by an existing API subscription.
2. **Condition data is fragmented and non-cumulative in a useful way.** A given vessel is surveyed
   once every 5–10 yr, usually by a *different* surveyor at each transaction, and the report is owned
   by the *client who paid* (buyer/insurer), not the platform. There is no natural mechanism for one
   surveyor's platform to accumulate a HIN-keyed longitudinal history — the next survey happens on a
   competitor's tool. Unlike CutLog (same operator logs the same machines daily) or a title plant
   (every transaction in a county funnels through the recorder), marine condition data **does not
   funnel to any single accumulator**. Not uniquely accumulable → **moat FAILS.**
3. Even the report-writing SoR layer, if won, holds only that surveyor's own reports — an absorbable
   feature an incumbent ($30/mo Claude app) already ships.

**Moat gate: FAIL.** No founder-accruing data flywheel exists in this domain.

---

## Step 3: Market Analysis + MANDATORY SAM Check (the second decisive failure)

The Round-4 map flagged "market may be too small" as the kill-risk. **Confirmed.**

- **Accredited surveyor population**: SAMS ≈ **"close to 1,000 surveyors" in the US + ~20 countries**;
  NAMS smaller; USSA/SAMS/NAMS combined "well over 1,000 members" in the US (VERIFIED, AIMU/Wikipedia).
  FCG's own marketing claims a **"10,000+ US marine surveyors"** TAM including non-accredited (ASSUMED
  generous — includes cargo/commercial/part-time).
- **Marine surveying is largely UNREGULATED** — no national/international license requirement (VERIFIED,
  Wikipedia). So the "regulatory mandate" is only an *insurer* requirement on older hulls (15–20 yr+),
  not a licensing mandate that guarantees a captive, growing seat base.
- **Realistic SAM math** (bottom-up):
  - Optimistic seat count: 10,000 US surveyors × realistic SaaS ACV $360–600/yr (incumbents charge
    $30–50/mo) = **$3.6M–$6M SAM.**
  - Accredited-only (the buyers who'd actually pay): ~2,000 × $500 = **~$1M SAM.**
  - Add a per-report or valuation upsell and stretch globally to IIMS's ~1,000 intl members: still
    **well under $20M** — an order of magnitude short of the **$100M SAM gate.**
- **Buyer check**: PASS in isolation — the buyer *is* the fragmented private surveyor (not insurer/gov).
  But that's the only gate this domain passes.

**SAM gate: FAIL** (SAM ≈ $3–6M, needs >$100M). Market ~15× too small at software prices.

---

## Step 4: Feasibility Analysis

Feasibility is *high* (pure software, TRL 8, buildable in weeks — the founder could clone FCG in a
weekend). **That is precisely the problem, not a virtue**: cheap + trivial-to-build + no flywheel +
tiny SAM + a $30/mo AI incumbent already shipping = the textbook Round-2/3 "absorbable feature, not a
company" pattern (LEARNINGS.md ⭐ moat gate; PestDoc analog). No feasibility score can rescue a
$3–6M SAM with no moat. **Not promoted.**

- Tech risk: Low. Market risk: **High** (SAM fail). Execution risk: **High** (crowded, insider incumbents).
  Timing risk: Med (AI report tools already launched — arguably *late*).

---

## Step 5: Execution Plan

**None.** No candidate clears the moat gate or the SAM gate. Writing an execution plan would violate
the honest-zero directive.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 2 | 8 (commodity report features) |
| Step 2 (incumbent + moat) | 2 | 0 | 2 |
| Step 3 (SAM) | 0 | 0 | — |
| Step 4 | 0 | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates: 0.** Core marine-boat surveying is an **honest ZERO** on two independent, decisive gates:
1. **Moat FAIL** — valuation data pre-owned by BUC/ABOS/J.D. Power (sold by API); condition data does
   not funnel to any single accumulator (each transaction re-surveyed by a different tool), so no
   founder-owned flywheel. Report-app layer already has 8 incumbents including a **$30/mo Claude-powered
   app built by a credentialed surveyor.**
2. **SAM FAIL** — ~1,000–2,000 accredited (≤10,000 total) surveyors × $360–600 ACV = **$3.6–6M SAM**,
   ~15× below the $100M gate; profession is *unregulated* so no licensing tailwind.

**Confidence**: surveyor counts VERIFIED (SAMS ~1,000; unregulated). Incumbent apps + pricing VERIFIED
(vendor pages). Valuation-data ownership VERIFIED (BUC/ABOS/J.D. Power). SAM math ASSUMED from those
inputs. The kill-risk the Round-4 map named ("too small + already served") is **confirmed true**.
