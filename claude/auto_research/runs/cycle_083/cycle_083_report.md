# Cycle 083 Report

**Date**: 2026-07-09
**Round**: 4 (fresh-domain discovery, cycles 051–100)
**Domain (assigned #8)**: Legal-Metrology / Calibration-Service Records — sub-angle B: **narrower FIELD legal-metrology service trades** (commercial scale service agents, retail fuel-dispenser / petroleum-meter provers, ATG tank-gauge calibration, in-motion/weigh-in-motion, LMI-registered service companies)
**Thesis under test**: the horizontal cal-lab SaaS (cycle 082) is bench/lab-centric; maybe a *narrower field trade* under state Weights & Measures (NIST Handbook 44) is fragmented, paper-based, and unserved — the field tech accumulates a per-device drift/service history the customer's system never holds.
**Kill-risk to clear first**: (a) same enterprise cal-management incumbents leaking down; (b) **device-OEM / dispenser-OEM free cloud**; (c) buyer skewing to the state W&M program itself (instant-reject gov buyer).

---

## Step 1: Technology Discovery (10 candidates)

### 1. Commercial-scale service-agent field app (place-in-service reports, W&M seal/test records)
- **Domain**: Scale-company field service + legal metrology
- **Breakthrough**: Mobile capture of as-found/as-left across test weights + auto NIST-HB44-format placed-in-service report; per-scale drift history across all customers.
- **TRL**: 8. **Time to product**: 4–6mo. **Status**: PROMOTED.

### 2. Retail fuel-dispenser / meter-prover service platform (W&M compliance + meter drift)
- **Domain**: Petroleum retail metrology
- **Breakthrough**: Field-proving capture (5-gal prover / master meter), auto compliance doc, per-dispenser meter-drift trend.
- **TRL**: 8. **Time to product**: 6mo. **Status**: PROMOTED.

### 3. Automatic Tank Gauge (ATG) calibration & UST leak-detection compliance records
- **Domain**: Petroleum storage compliance
- **Breakthrough**: Digitize ATG calibration + monthly leak-test compliance state per tank; renewal scheduling.
- **TRL**: 8. **Time to product**: 6mo. **Status**: PROMOTED.

### 4. Weigh-in-motion / truck-scale (LTL, aggregate, waste) calibration service records
- **Domain**: Heavy-capacity scale metrology
- **Breakthrough**: Digitize the multi-point HB44 test of vehicle scales; per-scale drift trend to predict OOT.
- **TRL**: 7. **Time to product**: 6mo. **Status**: PROMOTED.

### 5. Test-weight (reference standard) recall/traceability manager for the scale company's own weights
- **Domain**: Field reference-standard management
- **Breakthrough**: Track the service company's own certified test weights + reverse-impact if a weight is found OOT.
- **TRL**: 8. **Status**: REJECTED at Step 1 — this is a sub-feature; horizontal cal SoRs (cycle 082) already own reference-standard/reverse-traceability. Absorbable.

### 6. Grocery/deli price-verification + scale label compliance (UPC/price-verification device data)
- **Domain**: Retail W&M
- **Breakthrough**: Digitize price-verification sweeps mandated by W&M.
- **TRL**: 7. **Status**: REJECTED at Step 1 — buyer is the state W&M inspector (gov, instant-reject) or the retailer's own loss-prevention; not a fragmented private service trade.

### 7. Highway/vehicle-scale WIM analytics for DOT enforcement
- **Domain**: Transport enforcement
- **Status**: REJECTED at Step 1 — buyer is state DOT/gov, 12–24mo procurement. Instant-reject.

### 8. Medical/pharmacy balance & lab-scale calibration service for clinics
- **Domain**: Healthcare metrology service
- **Breakthrough**: Field cal of analytical balances at pharmacies/labs + cert.
- **TRL**: 8. **Status**: REJECTED at Step 1 — this is exactly the horizontal cal-lab SaaS use case (Beamex/IndySoft/Qualer) plus GxP QMS; no field-trade separation, incumbent-owned.

### 9. Livestock/agricultural & waste-transfer scale route-scheduling + compliance
- **Domain**: Ag/waste scale service
- **Breakthrough**: Niche routing + HB44 cert for the ag-scale service niche.
- **TRL**: 8. **Status**: PROMOTED (bundled with #1 as a vertical of the same buyer).

### 10. Parking/taxi meter & EV-charger dispenser metrology (emerging W&M category)
- **Domain**: Emerging legal metrology (EVSE billing accuracy)
- **Breakthrough**: New NIST HB44 §3.40 EV-fueling code → EV chargers become legal-for-trade devices needing periodic accuracy verification.
- **TRL**: 6 (regulation maturing). **Time to product**: 12–18mo. **Status**: PROMOTED (novel timing angle).

---

## Step 2: Competitive Analysis + ⭐MANDATORY Incumbent/OEM check

### #1/#4/#9 Scale service-agent field platform (incl. truck/ag scale) — INCUMBENT + OEM GATE FAILED
- **OEM check (VERIFIED):** the scale-indicator OEMs already ship service/field software bundled to sell hardware — the round-2/round-3 "OEM gives it away free" pattern:
  - **Rice Lake Weighing Systems** ships **iRite/Rice Lake iQUBE² + inbuilt service tools** and calibration record features on its indicators; large dealer channel.
  - **METTLER TOLEDO** ships **"ServiceXRT" / Smart5** and connected-scale service documentation; its own service arm dominates commercial scale service.
  - **Cardinal Scale / Avery Weigh-Tronix** provide dealer service software + connected-scale calibration logging.
  - Generic field-service-management SoRs (**ServiceTitan, Jobber, Housecall Pro, FieldEdge**) cover the dispatch/invoice layer for any service trade; the scale dealer typically runs one of these + the OEM tool.
- **Competitive density: 4/5.** The HB44 report is a template inside the OEM/dealer tooling, and dispatch is covered by horizontal FSM. **Moat gate:** connected scales stream calibration data to the *OEM's* cloud (Mettler/Rice Lake), so the drift time-series accrues to the OEM, not a new founder. **Status**: REJECTED.

### #2 Fuel-dispenser / meter-prover service platform — INCUMBENT/ERP GATE FAILED
- **OEM/ERP check (VERIFIED direction; some ASSUMED):**
  - Dispenser OEMs **Gilbarco Veeder-Root** and **Dover Fuels (Wayne / OPW)** own the forecourt: **Veeder-Root** ATG + **Insite360 / FMS** already provide compliance, meter-accuracy and tank-monitoring cloud; **Gilbarco** dealer/ASC (Authorized Service Contractor) network runs OEM-mandated service tooling.
  - Petroleum-service field companies run petroleum-vertical FSM/ERP: **FDS Amtech, PDI Technologies, Titan Cloud, Canary (leak-detection compliance)** — Titan Cloud and Canary specifically own UST/ATG compliance records.
- **Competitive density: 5/5.** Compliance record + meter accuracy is owned by the ATG-OEM cloud (Veeder-Root) and by UST-compliance SaaS (Titan Cloud, Canary). **Moat gate fails** — data accrues to the OEM/compliance SoR. **Status**: REJECTED.

### #3 ATG calibration / UST leak-detection compliance — REJECTED
- Same as #2: **Veeder-Root Insite360, Titan Cloud, Canary, Fairbanks** own the UST leak-test compliance record; the reg driver (EPA/state) pushes operators to these. Density 5/5. REJECTED.

### #10 EV-charger legal-for-trade accuracy verification — MOAT/TIMING GATE FAILED
- **OEM check:** EVSE billing-accuracy data lives in the charger network's own cloud (**ChargePoint, EVgo, Tesla, Shell Recharge**) and CPO back-ends (**AMPECO, Driivz, ev.energy**); the network owns the transaction/metering record. NIST HB44 §3.40 verification, where required, is performed by state W&M (gov buyer) or the CPO's own contractor feeding the CPO cloud.
- **Moat gate:** any drift/accuracy series accrues to the charger network, not a third-party app. **Timing:** regulation still maturing (TRL 6). **Buyer:** trends toward the CPO (few, large, not fragmented) or the state (gov). **Status**: REJECTED.

---

## Step 3–5
Nothing cleared Step 2. No sizing, feasibility, or execution plans.

Domain market notes (VERIFIED where cited): the field legal-metrology trades sit inside the same low-growth (~5.3% CAGR) calibration-services envelope; the reachable software SAM after OEM/compliance-SoR capture is well under $100M for a solo founder. Buyer-type is correct (fragmented private service company) for #1/#2/#4/#9, but every one loses the data moat to an OEM or compliance SoR.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 6 | 4 |
| Step 2 | 6 | 0 | 6 |
| Step 3 | 0 | 0 | — |
| Step 4 | 0 | — | — |
| Step 5 | 0 | — | — |

**Graduates this cycle: 0.**

**Honest read (cycle 083):** Going narrower into field legal-metrology trades does NOT escape the trap — it makes the moat gate worse. In every field sub-trade the compounding data asset is captured by a **connected-device OEM cloud** (Mettler-Toledo / Rice Lake for scales; Gilbarco Veeder-Root / Dover for dispensers & ATGs) or a **vertical compliance SoR** (Titan Cloud, Canary for UST). The scale/dispenser/tank device is increasingly a connected instrument phoning home to its maker, so the "service tech accumulates a proprietary drift series" premise is false — the OEM already owns that stream and gives the service software away to sell hardware. Buyer-type passes; moat and growth gates fail. Zero graduates.
