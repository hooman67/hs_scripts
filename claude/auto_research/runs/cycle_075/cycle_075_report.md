# Cycle 075 Report — Adjacent asset-inspection trades (RV, aircraft pre-buy, heavy equipment)

**Date**: 2026-07-09
**Domain (Round 4 map #6, adjacency sweep)**: same structural thesis as marine survey —
a licensed/certified inspector digitizes a mandated condition/valuation report and (claimed) accrues
a proprietary condition + comparable-valuation dataset — applied to the three nearest asset classes
where a pre-purchase/insurance inspection is customary: **RV inspection, aircraft pre-buy, heavy-
equipment appraisal.** Purpose: test whether the SAM or moat that fails for boats survives in a larger
adjacent asset class.
**Agent**: Round-4 discovery Agent F.

**Mandatory gates**: incumbent/OEM, moat-to-founder, growth+SAM, fragmented-private-buyer.

---

## Step 1: Candidates (3 asset classes × structural analog)

1. **RV inspection platform** — NRVIA-standard inspection report + photo/VIN + per-unit history. TRL 8.
2. **RV comparable-valuation model** from accumulated inspections. TRL 7.
3. **Aircraft pre-buy inspection platform** — A&P/IA logbook + airframe findings + squawk list. TRL 7.
4. **Aircraft comparable-valuation model**. TRL 7.
5. **Heavy-equipment field appraisal/inspection app** (ASA/AMEA appraisers, auction/lender). TRL 8.
6. **Heavy-equipment comparable-valuation model** from accumulated inspections. TRL 7.
7. **Cross-asset "used-asset condition Carfax"** keyed to VIN/HIN/serial/N-number. TRL 7.
8. **AI defect/CV photo grading** across asset classes. TRL 6.
9. **Insurer/lender-format report auto-formatter** per asset. TRL 8.
10. **Renewal/re-inspection scheduling on lender cadence**. TRL 9.

Promote the three "comparable-valuation from own data" variants (#2/#4/#6) + the RV/aircraft/equipment
report platforms — these carry the domain's claimed moat and land in larger asset markets.

---

## Step 2: Incumbent/OEM check + valuation-data ownership (the recurring kill)

**In EVERY adjacent asset class, the valuation dataset is already owned by an entrenched incumbent
that sells it by API/subscription** (VERIFIED):

| Asset | Report-app incumbents (crowded) | Valuation-data owner (moat already taken) |
|---|---|---|
| **RV** | Scribeware / RV Scribeware, RV Inspector Pro (2017), Dib for RV, **WanderWise (AI image analysis + VIN scan)**, RV Pro Check, HomeGauge RV template | **J.D. Power / NADA RV values**, ABOS RV; dealer-transaction based |
| **Aircraft** | pre-buy is service-shop-driven; tech tools exist (logbook/records review) | **VREF** ("real-time aircraft valuation platform"), **Aircraft Bluebook**, **JetNet**; AOPA gives basic Vref free to members |
| **Heavy equipment** | field-appraisal apps thin, but... | **Ritchie Bros. ecosystem** — EquipmentWatch, Rouse Services, Ritchie Bros. Price Results — "used in almost **every equipment appraisal** in the industry" |

**Incumbent verdict**: RV report layer is **as crowded as marine** (6+ apps, one AI/VIN one). Aircraft
and equipment valuation are **monopoly-ish incumbents** (Ritchie Bros. explicitly "every appraisal";
Vref/Bluebook the aircraft standard, partly free via AOPA). Competitive density **4–5/5** on the moat
asset in all three. REJECT the valuation-model variants on incumbency.

---

## Step 2 MOAT GATE

Same structural failure as boats, and *worse* for valuation:
- **Valuation data pre-owned and API-distributed** by J.D. Power/ABOS (RV), Vref/Bluebook/JetNet
  (aircraft), Ritchie Bros./EquipmentWatch/Rouse (equipment). A solo inspector's few-hundred-units/yr
  cannot out-accumulate firms fed by whole-market dealer + auction transactions. **Moat FAILS.**
- **Condition data does not funnel to one accumulator.** RV units re-inspected at each sale by whichever
  inspector the buyer hires; aircraft pre-buys done by different shops; equipment appraised by different
  ASA appraisers per deal. No single platform owns the longitudinal record → not uniquely accumulable.
- Aircraft/equipment also **invert founder-fit**: the valuable judgment is A&P airframe/records
  expertise or ASA machinery appraisal — domain expertise the founder lacks; the software is commodity.

**Moat gate: FAIL** across all three adjacencies.

---

## Step 3: SAM check

- **RV inspectors (NRVIA)**: population undisclosed but small — NRVIA is a ~10-yr-old niche cert;
  realistic low-thousands of active certified RV inspectors (ASSUMED, count not published). × $360–600
  ACV = low **single-digit $M SAM.** Same order as marine — FAIL.
- **Aircraft appraisers (NAAA)**: a few hundred; pre-buy shops number in the low thousands but they buy
  MRO/shop software, not an appraisal SaaS. SAM well under $50M — FAIL.
- **Heavy-equipment appraisers (ASA M&TS / AMEA)**: a few thousand certified appraisers, but their
  valuation input is Ritchie Bros. data (bought, not self-built). A "report app" seat business is again
  low **single-digit-to-tens $M** — FAIL, and moat sits with Ritchie Bros.

None of the three clears **SAM > $100M** at software ACVs; the larger the asset value, the *fewer* the
inspectors and the more entrenched the single valuation-data monopoly. **SAM gate: FAIL.**

---

## Step 4: Feasibility

Report apps are trivially buildable (RV space already has 6, incl. an AI/VIN one) — cheap + no moat +
small SAM = absorbable feature. Aircraft/equipment add a founder-fit inversion (specialist domain
judgment). No promotion.

## Step 5: Execution Plan
**None.** Honest zero.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 6 | 4 |
| Step 2 (incumbent + moat) | 6 | 0 | 6 |
| Step 3–5 | 0 | 0 | — |

**Graduates: 0.** The marine-survey failure mode **generalizes to every adjacent transaction-inspection
trade**: (a) valuation data is a pre-owned, API-sold incumbent monopoly (J.D. Power/ABOS, Vref/Bluebook,
Ritchie Bros./EquipmentWatch), and (b) condition data never funnels to a single accumulator because each
transaction is inspected by a different operator on a different tool. Larger asset value → fewer
inspectors + stronger single valuation monopoly, so SAM *shrinks* as asset size grows.

**Confidence**: valuation-data owners VERIFIED (vendor/search); inspector-population counts ASSUMED
(NRVIA/NAAA/ASA counts not published, but all are small niche certs). Directionally certain: no
founder-owned flywheel and no >$100M SAM in any of the three adjacencies.
