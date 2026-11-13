# Cycle 079 Report — ROUND 4

**Date:** 2026-07-09
**Domain:** Pesticide-application compliance / spray-log record-keeping for the green industry (lawn / ornamental / tree / structural PHC applicators) — the second half of Round-4 domain #7.
**Founder:** Hooman — AI/ML + software + cloud infra; EE bachelor's; solo/software-preferred; already building CutLog.
**Graduates:** 0
**Verdict:** The pesticide-compliance flank fails the SAME way the pest-control cycle (036, PestDoc) already failed, and for the same reason. State pesticide record-keeping IS a hard mandate (good demand driver), but the record is a **thin structured log** (date, product, EPA reg #, rate, site, applicator license) that (a) every green-industry field-service SoR already captures as "product usage logging," and (b) is not a compounding, uniquely-founder-owned asset — it's a compliance checkbox the SoR absorbs. Moat accrues to the incumbent workflow, not the founder. Honest zero.

---

## Method note

Same environment constraints as cycle 078 (search-engine CAPTCHAs). Competitive checks run against vendor pages directly. The federal recordkeeping rule (7 CFR Part 110 / AMS) and EPA WPS pages redirected/403'd to the fetcher; the mandate summary below is ASSUMED from well-established regulatory knowledge (federal 2-year retention for restricted-use pesticides; most states extend to all commercial applications; California DPR requires monthly Pesticide Use Reporting). The decisive competitive fact (SoRs already log product usage) is VERIFIED from vendor pages (Briostack, RealGreen, Arborgold, SingleOps).

---

## Step 1 — 10 ideas scanned

| # | Idea | Enabling shift | TRL | Step-1 call |
|---|------|----------------|-----|-------------|
| 1 | Mobile spray-log capture + auto state-compliant report (per-application record) | Mobile forms + PDF gen | 8 | PROMOTE |
| 2 | California DPR monthly Pesticide Use Report (PUR) auto-filing for landscape/structural PCOs | API/e-file + LLM mapping | 7 | PROMOTE |
| 3 | Restricted-use-pesticide (RUP) inventory + purchase-to-application reconciliation | Barcode + ledger | 7 | PROMOTE |
| 4 | Applicator-license + CEU-renewal tracking across a crew | Calendar + reminders | 8 | REJECT (S1) — trivial feature, no moat |
| 5 | Drift/buffer-zone + sensitive-site (school, water) geofence compliance checker | GIS + label rules DB | 6 | PROMOTE |
| 6 | Pesticide-label rules engine (rate/site legality) as an API ("is this application legal here?") | Structured label DB + LLM | 6 | PROMOTE |
| 7 | Neighbor pre-notification / posting compliance (state notification registries) | Registry integration | 6 | REJECT (S1) — buyer skew to registries/state; thin |
| 8 | Chemical mix/tank-load calculator + safety-data-sheet (SDS) manager | Calc + doc store | 8 | REJECT (S1) — commodity free tools; no moat |
| 9 | Worker Protection Standard (WPS) training/records for ag handlers | Records | 6 | REJECT (S1) — agricultural buyer; heavily served (Agrian, etc.) |
| 10 | "Green" reduced-risk product recommendation + IPM decision log | LLM advisor | 6 | REJECT (S1) — advisory, no mandate, no moat |

5 promoted to Step 2.

---

## Step 2 — Competitive density + MANDATORY Incumbent/OEM + Moat gates

### 1. Mobile spray-log capture + auto state report — **Density 4-5, REJECT**
- **Incumbent check (VERIFIED):** every green-industry field-service SoR already captures the application at the point of service. **Briostack** field app does "product usage logging, photo capture, digital signatures" for pest/lawn care. **RealGreen** (AI green-industry software), **Service Autopilot**, **FieldRoutes**, **Arborgold** (PHC), and **SingleOps** all run the technician workflow where the chemical record is entered. The state-report PDF is a formatting layer on data the SoR already holds.
- **Moat gate FAIL:** identical to **PestDoc (cycle 036, NO-GO)** — "the incumbent who owns the workflow can add the AI/compliance button." The record accrues to the SoR. No founder-owned flywheel.

### 2. California DPR monthly PUR auto-filing — **Density 3, REJECT on moat**
- **Mandate (ASSUMED):** CA DPR requires monthly Pesticide Use Reporting; a real, non-deferrable mandate. **Agrian, SureHarvest/Trace, and county-integrated tools** serve the agricultural PUR flow; for structural/landscape the pest-control ERPs (PestPac/WorkWave, FieldRoutes) handle CA reporting.
- **Moat gate FAIL + geo-concentration:** value is a single-state e-filing integration = an **absorbable feature** of the SoR, and demand is concentrated in one state (CA). No compounding founder asset; whoever owns the technician workflow files the report. Reject.

### 3. RUP inventory ↔ application reconciliation — **Density 3, REJECT**
- Restricted-use tracking is a module inside pest-control ERPs (PestPac, WorkWave) and ag platforms (Agrian). The reconciliation ledger is an accounting feature of the SoR that already records both the purchase and the application. No founder-owned data flywheel; absorbable. Reject.

### 5. Drift/buffer-zone / sensitive-site geofence checker — **Density 3, REJECT on founder-fit + moat**
- The defensible asset is a **maintained, authoritative database of sensitive-site geometries + per-label buffer rules + state-specific setbacks** — a regulatory-data-maintenance business (slow, legally exposed, needs domain-expert curation), not a software-plumbing play. Overlaps Agrian/label-data vendors. The data isn't uniquely accumulable by *this* founder as a by-product of operations — it must be sourced/curated. Inverts to a data-ops hard part; no operator flywheel. Reject.

### 6. Pesticide-label rules engine API ("is this legal here?") — **Density 3-4, REJECT**
- **Incumbent check:** structured pesticide-label data is already a product — **Agrian Label database, CDMS, Kelly Registration/state registration data, Greenbook.** Selling a rules API means licensing/re-deriving their data. The moat (the label dataset) accrues to the entrenched label-data vendors, not a new entrant. Reject.

All 5 rejected.

---

## Step 3 / 4 / 5

No survivors reached Step 3. No market sizing, feasibility, or execution plan produced.

(For the record on the size question this cycle would have tested: the *serviceable* buyer is the subset of ~175,000 US tree/lawn firms that apply pesticides and would pay for a **standalone** compliance tool rather than getting it inside their SoR. Because the SoRs bundle it, standalone WTP collapses toward ~$0 — the same "OEM/SoR ships it free" price cap seen repeatedly in Rounds 2–3.)

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 5 | 5 |
| Step 2 | 5 | 0 | 5 |
| Step 3 | 0 | 0 | — |
| Step 4 | 0 | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates this cycle: 0.**

**Honest read:** Pesticide-application compliance is a genuine mandate but a **solved, bundled, absorbable feature** — this is a re-run of the PestDoc (036) NO-GO with a different trade attached. The compliance record is a thin structured log every green-industry SoR already captures ("product usage logging"), and the only would-be data moats (label databases, sensitive-site geometries) are owned by entrenched regulatory-data vendors (Agrian/CDMS/Kelly), not accumulable by a solo operator. No path to a founder-owned flywheel here.
</content>
