# Cycle 084 Report

**Date**: 2026-07-09
**Round**: 4 (fresh-domain discovery, cycles 051–100)
**Domain (assigned #8)**: Legal-Metrology / Calibration-Service Records — sub-angle C: **adjacent mandated-certification service trades where the tested item is a DUMB (non-connected) instrument**, so the service provider might genuinely be the sole accumulator of the drift series. Trades tested: torque-tool cal (ISO 6789), portable gas-detector cal/bump, pipette cal (ISO 8655), pressure-relief-valve (PRV/PSV) testing & recert, weight/mass cal, medical-imaging QA physics, backflow-of-metrology (analytical instrument IQ/OQ/PQ).
**Thesis under test**: if the instrument is *not* internet-connected and there is *no* dominant vertical SoR, the independent service company is the only holder of the multi-customer drift series → founder-accruing moat could survive here even though it died in 082/083.
**Kill-risk to clear first**: (a) horizontal cal-lab SaaS (082 incumbents) covers these instrument classes too; (b) device-OEM free cloud (gas detectors are the obvious one); (c) niche verticalized SoR already exists (PRV, pipette).

---

## Step 1: Technology Discovery (10 candidates)

### 1. Torque-tool calibration service platform (ISO 6789 cert + tool drift history)
- **Domain**: Torque metrology service. **TRL**: 8. **Time**: 4–6mo.
- Field/bench capture of torque-tester runs, auto ISO-6789 cert, per-wrench drift across customers.
- **Status**: PROMOTED.

### 2. Portable gas-detector cal/bump-test fleet + service-company platform
- **Domain**: Gas-detection safety compliance. **TRL**: 8.
- **Status**: PROMOTED (must face the OEM-cloud gate — this is the canonical "OEM gives it free" risk).

### 3. Pipette calibration service platform (ISO 8655 cert, per-pipette drift)
- **Domain**: Lab liquid-handling metrology. **TRL**: 8. **Time**: 6mo.
- **Status**: PROMOTED.

### 4. Pressure/safety relief valve (PRV/PSV) testing & recertification records (API 510/576, VR stamp)
- **Domain**: Pressure-equipment mandated recert. **TRL**: 8.
- Digitize pop-test/set-pressure capture + per-valve recert history; renewal scheduling.
- **Status**: PROMOTED.

### 5. Weight/mass calibration lab (OIML/ASTM class weights) service records
- **Domain**: Mass metrology. **Status**: REJECTED at Step 1 — pure bench cal-lab work; horizontal cal SoRs (Beamex/IndySoft/Qualer, cycle 082) own it directly. Not separable.

### 6. Medical-imaging QA / diagnostic-physics survey records (CT/MR/mammo annual physics)
- **Domain**: Medical physics compliance. **Status**: REJECTED at Step 1 — buyer overlaps hospital QMS; incumbents (Radimetrics, DoseWatch, Qaelum, Radar/Landauer) + ACR portals own it; regulated/near-FDA adjacency. Poor founder fit.

### 7. Fire-extinguisher / suppression hydrostatic-test & tag records (NFPA 10)
- **Domain**: Fire equipment recert. **Status**: REJECTED at Step 1 — this is fire-protection service, already covered by cycle-70s hood/fire work and by Inspect Point / ServiceTrade / BuildingReports (LEARNINGS: NFPA space owned). Out of legal-metrology scope; density high.

### 8. Analytical-instrument IQ/OQ/PQ field-service records (HPLC/GC/spectrometer qualification)
- **Domain**: GxP lab-instrument qualification service. **Status**: REJECTED at Step 1 — buyer is GxP/pharma (validated-systems, 21 CFR Part 11); instrument OEM service arms (Agilent CrossLab, Waters, Thermo) own the qualification record. Enterprise sales, poor solo fit.

### 9. Thermometer / thermal-mapping / autoclave & cold-chain validation service records
- **Domain**: Thermal validation service. **TRL**: 8. **Time**: 6mo.
- **Status**: PROMOTED (bundled with #3 — same lab/pharma-adjacent service buyer, similar dynamics).

### 10. Anesthesia/biomed equipment (BMET) calibration & PM records for clinics
- **Domain**: Biomedical equipment service. **Status**: REJECTED at Step 1 — CMMS/CE incumbents (Nuvolo, EQ2 HEMS, Accruent/Connectiv, Phoenix) own the biomed asset record; hospital buyer, long sales. Poor fit.

---

## Step 2: Competitive Analysis + ⭐MANDATORY Incumbent/OEM check

### #2 Gas-detector cal/bump platform — OEM FREE-CLOUD GATE FAILED (hardest fail)
- **OEM check (VERIFIED):** the detector OEMs give the calibration/fleet cloud away to lock in sensor/instrument sales — textbook "OEM ships it free":
  - **Industrial Scientific iNet** (iNet Control / Exchange / Insights): dock to "bump test, calibrate, upload data logs," schedule automated cal/bump events, fleet reporting. (fetched 2026-07-09.)
  - **MSA Grid / MSA+**, **Blackline Safety** cloud, **Honeywell (BW) Safety Suite / Fleet Manager** — all provide the same free-with-hardware cal/bump record.
- Service companies (Total Safety, Levitt-Safety) operate *on top of* iNet, not a rival record. **Density 5/5.** The drift/bump record accrues to the OEM cloud. **Moat gate fails.** **Status**: REJECTED.

### #1 Torque-tool calibration service platform — INCUMBENT GATE FAILED
- **Incumbent/OEM check:** torque-tester OEMs bundle cert software: **Norbar (Torque Data Management / TDMS)**, **Crane Electronics (TorqueStar / TWC)**, **Sturtevant Richmont**, **Mountz** all ship ISO-6789 certificate + history software with their torque analyzers. Horizontal cal SoRs (Beamex/IndySoft) also model torque as an instrument class.
- **Density 4/5.** The tester OEM owns the capture→cert flow (same pattern as documenting calibrators in cycle 082). **Moat gate:** drift series is captured by the OEM tester's software. **Status**: REJECTED.

### #3 Pipette calibration service platform — INCUMBENT GATE FAILED
- **Incumbent/OEM check:** balance/pipette OEMs own it: **Sartorius (SartoCollect / cyberEYE)**, **METTLER TOLEDO Calibry** (dedicated pipette-cal software), **Artel (PCS/MVS)** are the standard; plus **Andrew Alliance/Waters**. Horizontal cal SoRs also cover ISO-8655.
- **Density 5/5.** Calibry/Artel are purpose-built for exactly this service. **Moat gate fails.** **Status**: REJECTED.

### #4 PRV/PSV testing & recert records — INCUMBENT/VERTICAL-SoR GATE FAILED
- **Incumbent check:** valve-test-bench OEMs and mechanical-integrity SoRs own it: **Seatell / Accudyne**, **Hydrotechnik**, and test-bench makers ship data-capture + cert; **valve-shop ERP** (VMS / Valve Management Systems, **STI/Emerson valve MI**) and plant mechanical-integrity SoRs (**Meridium/GE APM, Cority, Intelex**) hold the recert record on the owner side. Density 4/5. Buyer often the refinery/plant (large, slow procurement). **Status**: REJECTED.

### #9 Thermal/cold-chain validation records — INCUMBENT GATE FAILED
- **Incumbent check:** validation-logger OEMs own it: **Kaye (Amphenol) ValProbe/AVS**, **Ellab ValSuite**, **Vaisala viewLinc** are the GxP-standard thermal-validation software bundled with the loggers; plus GxP QMS. Density 5/5, GxP buyer. **Status**: REJECTED.

---

## Step 3–5
Nothing cleared Step 2. No sizing/feasibility/execution.

Buyer-type note: #1/#3/#4/#9 buyers are legitimately fragmented private service companies (buyer gate PASS), but every instrument class has a **measuring-device OEM that bundles the certificate + history software to sell instruments/sensors** — so the drift series is captured by the OEM tool the tech already uses, not by a new founder's platform. Same structural death as cycles 082–083.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 5 | 5 |
| Step 2 | 5 | 0 | 5 |
| Step 3 | 0 | 0 | — |
| Step 4 | 0 | — | — |
| Step 5 | 0 | — | — |

**Graduates this cycle: 0.**

**Honest read (cycle 084):** The "dumb instrument = founder owns the data" hypothesis fails on contact. Every mandated-cert instrument class has its own **measuring-instrument OEM** whose analyzer/tester/dock ships with certificate-and-history software (Norbar/Crane for torque, METTLER Calibry & Artel for pipettes, Kaye/Ellab for thermal, Industrial Scientific iNet for gas detectors), given away to sell the hardware and its consumables/sensors. The tested item may be dumb, but the *reference standard the tech reads it against is not*, and its OEM owns the capture-to-certificate flow. Layer in the horizontal cal SoRs (082) modeling every one of these classes and there is no unserved drift series to own. Zero graduates. One structural exit remains untested — a benchmark that spans MANY labs/service companies, which no single OEM's or SoR's siloed data can build — cycle 085.
