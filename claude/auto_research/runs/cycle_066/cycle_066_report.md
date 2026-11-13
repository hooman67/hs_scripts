# Cycle 066 Report

**Date**: 2026-07-09
**Round**: 4 (fresh domains), Agent D — Domain #4 Cathodic-Protection / Corrosion Survey (AMPP-mandated)
**Cycle focus**: The core thesis, head-on — digitizing the mandated CP survey (annual test-point structure-to-soil potentials, 60-day/annual rectifier readings) and owning the multi-year potential time-series per structure. This cycle tests whether the founder can OWN that time-series, or whether the incumbent system-of-record and the utility buyer already foreclose it.

**Mandatory gates applied every idea**: (1) Incumbent/OEM check — American Innovations Bullhorn + PCS Field Data Collector/Survey Manager, MOBILTEX CorView, iFactory, HSC Cloud; (2) Moat gate — data must accrue to the FOUNDER's platform; (3) SAM > $100M; (4) Buyer must be a fragmented PRIVATE CP-service contractor who pays directly (pipeline/utility operator = instant-reject, 12–24mo procurement).

---

## Standing competitive picture (established this cycle, carried forward to 067–069)

| Incumbent | What it is | Target buyer | Owns the data? |
|---|---|---|---|
| **American Innovations — PCS Field Data Collector + Survey Manager** | Mobile CP field-data-collection app (Mesa/Archer tablets, iOS, Windows) that captures test-point surveys, structure-to-soil potentials, rectifier readings; feeds the **PCS Pipeline Compliance System** (system-of-record) with a **CP Data Manager** module. [VERIFIED — aiworldwide.com/products] | "Trusted by **90%+ of major operators**" — oil & gas, gas distribution/transmission, PHMSA/FERC transmission. [VERIFIED] | **The operator, via PCS.** The contractor is a data-entry vendor INTO the operator's SoR. |
| **American Innovations — Bullhorn** | Remote monitoring: rectifier RMUs, test-point RMUs, bond monitors, Triton test stations + Bullhorn Web. [VERIFIED] | Same 90%-of-major-operators base. | Operator. |
| **MOBILTEX CorView Cloud** | Remote-monitoring device data storage + reporting. [VERIFIED — search result] | Utilities and pipeline operators. | Operator/utility. |
| **iFactory / iFactoryApp** | Unified analytics layer for rectifier + survey data; also UST CP monitoring content. [VERIFIED — search result] | Pipeline corrosion-control teams. | Operator. |
| **HSC Cloud** | GPS-guided mobile CP forms, failure alerts, one-click reporting; "solves paper CP logs." [VERIFIED — search result] **NOTE: primary domain now parked/for-sale — possibly defunct or acquired.** [VERIFIED — hsccloud.com → GoDaddy park] | Gas utilities. | Utility. |
| **FAT FINGER / FieldProxy / Corpad** | Horizontal field-data / digital-form apps with CP templates (pipe-to-soil, GPS, rectifier records, NFC/QR). [VERIFIED — search result] | Field-service teams generally; adaptable to CP. | Whoever configures it (usually operator). |

**The structural finding this cycle produces:** In the pipeline/utility core of CP, the mandated survey app **already exists and is mature** (AI's PCS Field Data Collector is exactly the "digitize the paper survey" product), AND the resulting time-series accrues to the **operator's** PCS/Bullhorn/CorView system-of-record — not to the survey contractor, who is a captive data-entry vendor. The central Round-4 thesis for this domain therefore fails BOTH the buyer gate (utility) and the moat gate (SoR owns the flywheel) in its core segment. The only survival path is a segment where the PAYER is a fragmented private contractor AND that contractor can accumulate its OWN cross-account data — which pushes the domain out of pipelines and into UST/water-tank/facility CP (explored in 067–069).

---

## Step 1: Technology Discovery

### 1. Mobile CP test-point survey app with multi-year potential trend/anomaly detection (pipeline/distribution)
- **Domain**: CP survey digitization for pipeline/gas-distribution operators
- **Breakthrough**: Cheap tablets + LLM-assisted anomaly flagging on structure-to-soil potential time-series.
- **TRL**: 9 (this product already ships)
- **Time to product**: 3 mo
- **Status**: REJECTED
- **Reasoning**: This IS American Innovations PCS Field Data Collector + Survey Manager, in market with 90%+ of major operators. Competitive density 5/5. Instant-reject.

### 2. UST cathodic-protection testing app for independent CP testers (EPA 40 CFR 280.31)
- **Domain**: Underground storage tank CP compliance testing — the fragmented private-contractor segment
- **Breakthrough**: Every regulated steel UST needs a **CP survey every 3 years + rectifier check every 60 days** (40 CFR 280.31; NACE TM0101/TM0497). ~534,000 active petroleum USTs at ~190,000 facilities [VERIFIED — EPA UST Program Facts, May 2025]. These are tested by fragmented private CP/tank-testing contractors, NOT by the gas-station owner. A mobile app that captures the test, auto-generates the state-format compliance PDF, and owns the **per-tank CP history across all the contractor's accounts** could be the contractor's book of business.
- **TRL**: 9 (components exist; it's app+PDF+scheduling)
- **Time to product**: 4–6 mo
- **Status**: PROMOTED
- **Reasoning**: This is the one segment where the payer is a fragmented private contractor. Carry to Steps 2–4 for the incumbent + moat + SAM test.

### 3. Rectifier 60-day inspection logger + auto-compliance calendar for UST contractors
- **Domain**: UST impressed-current rectifier compliance
- **Breakthrough**: 60-day rectifier reading is the highest-frequency mandated CP touchpoint; a scheduling+logging app prevents the enforcement-triggering missed cycle.
- **TRL**: 9
- **Time to product**: 3 mo
- **Status**: PROMOTED (folds into #2 as a feature — evaluated together)
- **Reasoning**: Higher cadence than the 3-year survey = a thicker recurring touch; strengthens the #2 flywheel. Promote as part of the UST-contractor bundle.

### 4. Parasitic AI layer on the operator's existing CP data (PCS/Bullhorn API)
- **Domain**: AI analytics on pipeline operators' CP time-series
- **Breakthrough**: LLM/ML anomaly + rectifier-failure prediction on data already in PCS/Bullhorn.
- **TRL**: 7
- **Time to product**: 6 mo
- **Status**: REJECTED
- **Reasoning**: Moat accrues to AI (owns the data + one feature-flag away) and the buyer is the operator (12–24mo procurement). Fails both gates. This is the exact Round-3 "layer AI on the incumbent SoR" dead-end.

### 5. Automated PHMSA/state CP compliance-report generator
- **Domain**: Regulatory reporting for CP surveys
- **Breakthrough**: Auto-fill 49 CFR 192.451/195.551 annual survey reports.
- **TRL**: 8
- **Time to product**: 4 mo
- **Status**: REJECTED
- **Reasoning**: PCS Compliance already does this for operators; buyer is the operator/utility. Fails buyer + incumbent gates.

### 6. Handheld CP meter with built-in cloud logging (hardware)
- **Domain**: CP measurement instrument + data
- **Breakthrough**: GPS + cellular voltmeter that auto-uploads structure-to-soil potentials.
- **TRL**: 7
- **Time to product**: 12–18 mo
- **Status**: REJECTED
- **Reasoning**: Hardware build (analog front-end, ruggedization, FCC) inverts founder-fit; Tinker/Rasor, MC Miller, and RMU OEMs (AI, MOBILTEX) own the instrument+feed. Hidden hard part = the meter. Reject.

### 7. Test-station RFID/NFC identity + visit-history register
- **Domain**: CP test-station asset identity
- **Breakthrough**: NFC-tag each test station; app pulls prior readings on tap.
- **TRL**: 8
- **Time to product**: 4 mo
- **Status**: REJECTED (absorbable feature)
- **Reasoning**: Corpad already does NFC/QR test-point identity; AI's Field Data Collector geolocates test points. Feature, not a company.

### 8. Stray-current / AC-interference monitoring analytics (pipeline)
- **Domain**: AC-interference CP mitigation
- **Breakthrough**: ML on coupon/AC-density data to flag interference.
- **TRL**: 6
- **Time to product**: 9 mo
- **Status**: REJECTED
- **Reasoning**: Buyer is transmission operator (instant-reject); AI's AC Coupon Test Station monitors + Bullhorn own the feed. Fails buyer + incumbent.

### 9. Contractor field-crew dispatch/scheduling for CP survey routes
- **Domain**: CP-contractor field-service management
- **Breakthrough**: Route optimization for annual test-point survey circuits.
- **TRL**: 9
- **Time to product**: 4 mo
- **Status**: REJECTED
- **Reasoning**: Horizontal FSM (ServiceTitan/Jobber/FieldProxy) covers dispatch; no CP-specific data flywheel accrues here. Absorbable.

### 10. Anode/groundbed remaining-life prediction from rectifier trend
- **Domain**: CP consumable-life prediction (echoes Plasma 9/10 archetype)
- **Breakthrough**: Predict anode-bed depletion from rising rectifier voltage/output trend.
- **TRL**: 6
- **Time to product**: 9 mo
- **Status**: PROMOTED (conditionally — carry to Step 2)
- **Reasoning**: Genuine analytics value and a possible data moat IF the founder owns the reading history. But the reading history lives in PCS/Bullhorn for the operator segment. Only survives if attached to a segment where the CONTRACTOR owns the readings (i.e., bundled into the UST-contractor app #2). Evaluate under that constraint.

---

## Step 2: Competitive Analysis

### UST CP testing app for independent testers (idea #2, +#3 rectifier logger, +#10 anode-life)
- **Competitors found**:
  - **American Innovations PCS Field Data Collector** — built for pipeline operators; overkill and enterprise-priced for a 2–10-person UST-testing shop; not sold to that buyer. [VERIFIED]
  - **iFactoryApp** — has UST CP monitoring content but oriented to corrosion-control teams/monitoring, not the small testing contractor's compliance-report workflow. [VERIFIED]
  - **Titan Cloud / Canary Compliance** — UST compliance platforms, but the buyer is the **tank owner / fuel retailer / fleet** (7-Eleven, Circle K, UPS), and CP testing is one line inside "Site Inspections, Testing & Permitting." They own the compliance SoR on the OWNER side. [VERIFIED — titancloud.com]
  - **Generic**: FAT FINGER, FieldProxy, Corpad (configurable forms), plus paper/Excel (the real incumbent for small shops).
- **Competitive density score**: 3/5
- **Differentiation angle**: A CP-testing-contractor-native app (not an owner-side compliance SoR, not a pipeline enterprise tool): captures the 3-yr survey + 60-day rectifier check, auto-generates each state's UST CP report format, and — critically — accumulates the contractor's **own cross-account per-tank CP history** (serial, anode type, potentials trend, next-due) that no owner-side platform holds in one place.
- **Status**: BORDERLINE-PROMOTE
- **Reasoning**: Real gap for the small testing shop; but the moat question (below) is serious.

---

## Step 3: Market Analysis

### UST CP Testing Contractor App
- **Target market**: Independent UST CP-testing / tank-service contractors in the US.
- **Buyer**: The private testing contractor (2–20 techs) — PASSES the fragmented-private-buyer gate. NOT the tank owner and NOT a utility.
- **Market sizing (bottom-up, honest)**:
  - ~534,000 active petroleum USTs; a large share are steel-with-CP requiring the 3-yr test [VERIFIED tank count; CP-eligible fraction ASSUMED ~40–60% = ~200–320K tanks].
  - The buyer universe is the **contractors**, not the tanks. CP/tank-testing is a fragmented trade, but the reachable universe is plausibly only **~1,500–4,000 firms** nationally [ASSUMED — could not verify a firm count; AMPP tester population unverified]. At a realistic **$1,500–3,000/yr** SaaS ACV for a small shop, that is **~$2.3M–$12M SAM**.
- **Revenue model**: Per-seat/per-tech SaaS + optional per-report fee.
- **Growth rate**: UST population flat-to-declining (EV transition pressures fuel retail long-term); CP-testing mandate stable. [ASSUMED flat]
- **Status**: **REJECTED**
- **Reasoning**: **Fails the SAM > $100M gate by more than an order of magnitude.** The countable buyer universe (a few thousand small testing firms) at small-shop ACV cannot clear $100M — the exact "countable buyer universe is a red flag" pattern from the TAB learning. Even generous assumptions top out ~$12M SAM.

---

## Step 4: Feasibility Analysis

No idea reached Step 4. The one buyer-gate survivor (UST CP testing app) died at Step 3 on SAM, and its moat is also weak:

- **Moat gate verdict on the UST app**: PARTIAL. The contractor CAN accumulate a cross-account per-tank history the owner-side SoRs don't hold — a real, if modest, data asset. BUT the flywheel is thin: a **3-year** survey cadence means only ~1 potential reading per tank per 3 years, so the "compounding time-series per structure" that justifies the whole domain thesis is anemic. The 60-day rectifier check helps cadence but is a pass/fail log, not rich trend data. Anode-life prediction (idea #10) needs denser data than this cadence provides. Net: weak flywheel, and it's capped by a sub-$15M SAM regardless.

---

## Step 5: Execution Summary

**No graduates this cycle.** The core CP-survey thesis is foreclosed:

- **Pipeline/utility core** → instant-reject buyer AND incumbent (AI PCS/Bullhorn) owns both the mandated field app and the data flywheel. This is a mature, occupied space, not a green field.
- **UST-contractor segment** (the only fragmented-private-buyer path) → passes the buyer gate but **fails SAM by 10× and has a thin (3-year-cadence) flywheel.**

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 4 (2,3,10 bundled + borderline) | 6 |
| Step 2 | 1 (bundle) | 1 borderline | — |
| Step 3 | 1 | 0 | 1 (SAM) |
| Step 4 | 0 | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates this cycle: 0.**

**Honest read**: The central Round-4 thesis for this domain ("own the multi-year potential time-series per structure") is strongest exactly where the buyer is worst (pipeline/utility) and the incumbent already owns it (American Innovations PCS/Bullhorn). Where the buyer is right (UST testing contractors), the market is too small and the flywheel too thin. Cycles 067–069 push into CP-adjacent inspection trades to find a segment that passes all four gates simultaneously.
