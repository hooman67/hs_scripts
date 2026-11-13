# Cycle 068 Report

**Date**: 2026-07-09
**Round**: 4, Agent D — Domain #4 Cathodic-Protection / Corrosion Survey (AMPP-mandated)
**Cycle focus**: The specialized **CP-survey-contractor services** where a private survey firm is hired for discrete, high-value survey campaigns — **close-interval survey (CIS), DCVG/ACVG coating-defect survey, and soil/interference surveys** — plus **facility/plant-yard CP** at private industrial sites (refineries, tank farms, chemical plants) that own many buried structures. Hypothesis: these are performed by fragmented private survey contractors and generate dense spatial time-series. Test the four gates.

**Mandatory gates**: (1) Incumbent/OEM — American Innovations PCS/Bullhorn/Survey Manager, MOBILTEX CorView, iFactory; (2) Moat to FOUNDER; (3) SAM > $100M; (4) fragmented PRIVATE contractor buyer.

**Carry-forward**: 066 killed the pipeline CP core (AI PCS owns app+data; utility buyer) and UST-contractor path (SAM). 067 killed AST/water-tank inspection (buyer/SAM scissors; enterprise APM incumbents). This cycle probes CIS/DCVG survey contractors and facility CP.

---

## Step 1: Technology Discovery

### 1. Close-Interval Survey (CIS) data-collection + analytics app for survey contractors
- **Domain**: Pipeline CIS coating/CP surveys performed by specialist survey crews
- **Breakthrough**: CIS collects on-the-order-of one structure-to-soil reading every ~2.5–5 ft over miles of pipe = huge spatial datasets. Specialist survey contractors (often distinct from the operator) run these campaigns. Digitize collection + auto-analyze + own the geospatial reading history.
- **TRL**: 8
- **Time to product**: 6 mo
- **Status**: PROMOTED (carry to incumbent gate)

### 2. DCVG / ACVG coating-defect survey app with defect severity ranking
- **Domain**: Above-ground coating-defect surveys
- **Breakthrough**: DCVG %IR severity classification from field readings; digitize + rank defects for dig-list prioritization.
- **TRL**: 7
- **Time to product**: 6 mo
- **Status**: PROMOTED (folds into #1)

### 3. Facility/plant-yard CP survey app for industrial site CP techs
- **Domain**: Refinery/terminal/chem-plant buried-structure CP surveys
- **Breakthrough**: Private industrial sites have hundreds of buried structures needing annual CP surveys; often serviced by regional CP-service contractors. Digitize the site survey + own per-structure history.
- **TRL**: 9
- **Time to product**: 5 mo
- **Status**: PROMOTED (carry to buyer/incumbent gate)

### 4. Survey-crew productivity / QA app (flag bad readings in field)
- **Domain**: CIS/DCVG data quality
- **Breakthrough**: Real-time outlier detection so a crew doesn't re-walk miles.
- **TRL**: 8
- **Time to product**: 5 mo
- **Status**: PROMOTED (folds into #1 as QA feature)

### 5. GIS-aligned CP survey overlay (align readings to pipe centerline/GIS)
- **Domain**: Geospatial CP data
- **Breakthrough**: Auto-align CIS reading strings to the operator's GIS/alignment sheets.
- **TRL**: 7
- **Time to product**: 7 mo
- **Status**: REJECTED
- **Reasoning**: This deliverable is consumed by the operator's GIS/integrity SoR (PCS, ESRI-based integrity platforms); value accrues to the operator's system. Absorbable into #1 at best.

### 6. Interference/HVAC-AC survey analytics near powerlines
- **Domain**: AC interference surveys
- **Breakthrough**: ML on AC-density survey data.
- **TRL**: 6
- **Time to product**: 9 mo
- **Status**: REJECTED
- **Reasoning**: Deliverable goes to transmission operator; buyer instant-reject.

### 7. Survey-report auto-generation for the survey contractor's client deliverable
- **Domain**: CIS/DCVG report automation
- **Breakthrough**: Auto-build the branded survey report the contractor hands the operator.
- **TRL**: 8
- **Time to product**: 4 mo
- **Status**: PROMOTED (this is the actual wedge for #1)

### 8. Cross-campaign corrosion-trend network for survey contractors
- **Domain**: Data-network effect
- **Breakthrough**: A survey contractor who re-surveys the same pipe every few years accumulates change-over-time — but the OPERATOR owns that pipe and switches contractors on bid.
- **TRL**: 7
- **Status**: REJECTED (moat leak — see Step 2)

### 9. Handheld survey datalogger integration (Tinker&Rasor / MC Miller / Gas Electronics)
- **Domain**: Instrument data ingestion
- **Breakthrough**: Import from existing survey dataloggers instead of re-keying.
- **TRL**: 8
- **Time to product**: 5 mo
- **Status**: REJECTED (absorbable integration feature; OEM dataloggers already export)

### 10. AI dig-list prioritization from combined CIS+DCVG+ILI
- **Domain**: Integrity dig prioritization
- **Breakthrough**: Fuse survey + inline-inspection data to rank dig sites.
- **TRL**: 6
- **Time to product**: 9 mo
- **Status**: REJECTED
- **Reasoning**: Buyer = pipeline integrity engineer at the operator; competes with operator integrity SoRs; instant-reject buyer.

---

## Step 2: Competitive Analysis

### CIS/DCVG survey contractor platform (idea #1 bundle: +2,4,7)
- **Competitors found**:
  - **American Innovations PCS Field Data Collector + Survey Manager** — explicitly built to collect and manage CP survey data including CIS-type surveys, and feeds PCS. Mature. [VERIFIED]
  - **MOBILTEX CorView, iFactory** — survey/monitoring data platforms. [VERIFIED]
  - Survey-datalogger OEMs (**Tinker & Rasor, M.C. Miller, Gas Electronics, Allegro/Juniper rugged PCs**) ship their own CIS data-collection software with the instrument. [ASSUMED — standard in the trade]
  - Large survey contractors (**Corrpro/Aegion, MATCOR, Mears/Quanta, Corrosion Control Engineering**) have in-house survey software. [ASSUMED]
- **Competitive density score**: 4/5. The mandated CIS/DCVG collection app already ships from AI and from the datalogger OEMs.
- **Differentiation angle**: Thin — a nicer contractor-side analytics/report layer. Not defensible.
- **Status**: REJECTED (density 4/5).

### Facility/plant-yard CP survey app (idea #3)
- **Competitors found**: AI PCS Field Data Collector serves this too (same product covers plant CP as well as pipeline). Large industrial sites also route CP data into their mechanical-integrity/APM SoR (AVEVA/Meridium, per cycle 067). [VERIFIED for AI; ASSUMED for APM tie-in]
- **Competitive density**: 4/5.
- **Status**: REJECTED.

---

## Step 3: Market Analysis

Neither survivor passed Step 2's density gate, so formal sizing is moot. Recording the decisive gate failures:

- **Moat gate (idea #1, CIS/DCVG contractor)**: **FAILS.** The pipe belongs to the OPERATOR. When the operator re-bids the survey to a different contractor next cycle, the "compounding change-over-time" data resets — the survey contractor cannot uniquely accumulate a compounding per-structure history because it doesn't durably control the structures or win them repeatedly. The longitudinal asset accrues to whoever holds the pipe's SoR = the operator (PCS). This is the fatal structural flaw of the whole "CP survey contractor" thesis: **the contractor is transient on any given asset; the operator is permanent.**
- **Buyer gate (idea #3, facility CP)**: The paying client for facility CP surveys is the **plant owner-operator** (refinery/terminal/chemical), an enterprise buyer, and the data accrues to their APM SoR. Fails buyer + moat.

---

## Step 4: Feasibility Analysis

No idea reached Step 4.

---

## Step 5: Execution Summary

**No graduates this cycle.** This cycle isolated the domain's **core structural defect** for the founder's moat thesis:

> In CP surveying, the *structure* (pipe, tank, plant) is owned by a permanent operator, while the *survey contractor* is a rotating vendor selected by bid. Therefore the compounding time-series the founder wants to own inevitably accrues to the operator's system-of-record, not to the contractor's app. The one segment where a contractor DOES durably own its accounts (UST testing, cycle 066) has too few tanks-per-contractor and too slow a cadence to build a real flywheel — and too small a SAM.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 5 (bundled) | 5 |
| Step 2 | 2 bundles | 0 | 2 (density 4/5) |
| Step 3 | 0 | 0 | — |
| Step 4 | 0 | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates this cycle: 0.**

**Honest read**: The survey-contractor segment fails on the deepest possible level — not on incumbents or SAM alone, but on a **structural moat leak**: the asset's owner is permanent and the surveyor is transient, so the flywheel can never accrue to the founder's platform. This is the cleanest kill in the domain and applies to every "CP survey contractor app" variant. Cycle 069 does a final sweep of the last untested corner (small-structure / marina & marine-facility / owner-operated CP with durable contractor relationships) and delivers the domain-level verdict.
