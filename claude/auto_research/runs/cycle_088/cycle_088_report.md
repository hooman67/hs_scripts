# Cycle 088 Report — Adjacent angle: MC-331 cargo-tank / bobtail DOT inspection + fuel-oil-tank inspection

**Date**: 2026-07-09
**Domain (Round-4 map #9, adjacent probe)**: Two "mandated-inspection with per-asset history"
angles that sit beside the propane gas check but touch a *different asset class* than cycle
086/087:
1. **The delivery vehicle itself** — a propane **bobtail is an MC-331 cargo tank** requiring an
   **annual external-visual + periodic K/V/I/P/T/L (thickness/pressure/leakage) inspections**,
   plus delivery-hose testing; the dealer accumulates a per-truck cargo-tank inspection history.
2. **Heating-oil / fuel-oil tank inspection** — fuel-oil dealers (often the same companies that
   sell propane) run **NORA-certified tank inspections / sweeps** on residential and commercial
   oil tanks, accumulating a per-tank condition history.

Thesis-under-test: does either asset class have an *unowned* per-asset inspection flywheel a
solo software founder could capture?

**Gates**: incumbent/OEM (fleet-maintenance SoRs, P3/Tank Spotter, fuel-oil ERPs), moat, SAM, buyer.

---

## Step 1: Technology Discovery (10 candidates)

### 1. MC-331 cargo-tank annual DOT inspection recordkeeping app (bobtail)
- **Domain**: Hazmat cargo-tank compliance
- **Breakthrough**: Structured mobile capture of the annual external visual + delivery-hose test +
  thickness readings, per truck, with due-date alerts and DOT-report generation.
- **TRL**: 9 (shipping category)
- **Status**: PROMOTED (to test) — the *cargo-tank-specific* record may be less owned than the
  gas check; carry it.

### 2. Bobtail DVIR / DOT vehicle-inspection app (driver daily inspection)
- **Breakthrough**: Electronic DVIR for the delivery fleet.
- **TRL**: 9
- **Status**: **REJECTED (Step 1)** — **Fleetio, Whip Around, Samsara, Motive** own electronic
  DVIR / DOT fleet inspection; a saturated horizontal category. Instant incumbent.

### 3. Delivery-hose / meter (Neptune/LC) recertification tracker
- **Breakthrough**: Track meter calibration + hose test dates.
- **TRL**: 8
- **Status**: **REJECTED (Step 1)** — meter calibration overlaps Round-4 domain #8 (legal
  metrology, separate agent) and sits inside fleet-maintenance PM; absorbable.

### 4. Heating-oil residential tank inspection / condemn app (NORA-cert workflow)
- **Breakthrough**: Structured oil-tank inspection (age, corrosion, legs, fill/vent) + photo + PDF,
  building a per-tank condition history for the oil dealer.
- **TRL**: 8
- **Status**: PROMOTED (to test) — carry; check incumbents + market trajectory.

### 5. Underground oil-tank (UST/AST) closure & soil-testing documentation
- **Breakthrough**: Manage tank-removal/closure environmental docs.
- **TRL**: 8
- **Status**: **REJECTED (Step 1)** — buyer skews to environmental contractors + state DEP
  e-permit portals (regulator-adjacent); moat → state portal / enviro-SoR; fails buyer/moat.

### 6. Oil-tank insurance-inspection & replacement-lead scoring
- **Breakthrough**: Score tanks likely to fail insurance inspection → sell replacements.
- **TRL**: 7
- **Status**: PROMOTED (to test) — a lead-gen/valuation flavor; test whether ERP/data owner beats it.

### 7. AI ultrasonic-thickness reading logger for cargo tanks
- **Breakthrough**: BLE UT gauge streams wall-thickness readings into the cargo-tank record.
- **TRL**: 7
- **Status**: **REJECTED (Step 1)** — the mandated thickness test is performed by a **registered
  CT (cargo-tank) inspection facility / RStamp shop**, not the dealer; the record accrues to the
  inspection shop's system; hardware-integration niche, tiny buyer.
### 8. Combined truck+tank+cylinder "everything compliance" register
- **Status**: **REJECTED (Step 1)** — this is P3 / Tank Spotter's whole pitch. Direct incumbent.

### 9. Fuel-oil delivery ERP add-on for tank compliance
- **Status**: **REJECTED (Step 1)** — ADD Systems / Cargas / Blue Cow / iRely serve fuel-oil
  dealers too; the add-on accrues to the ERP, not the founder. Moat gate fail.

### 10. Cargo-tank inspection-facility (RStamp shop) scheduling marketplace
- **Status**: **REJECTED (Step 1)** — thin two-sided marketplace; tiny supply side; no data moat.

**Step 1 result: 3 promoted (#1, #4, #6), 7 rejected.**

---

## Step 2: Competitive Analysis + MANDATORY Incumbent/OEM Check

| Candidate | Incumbent / OEM reality | Density | Verdict |
|---|---|---|---|
| #1 MC-331 cargo-tank annual inspection | **Fleetio / Whip Around / Samsara / Motive** already do custom inspection templates + PM scheduling + document storage for commercial fleets, incl. cargo tanks; and **P3 markets cargo-tank/DOT compliance**. No search surfaced an *unserved* gap — the round-3 "result dies today, is that the whole product?" test: the annual cargo-tank record is a document-storage + reminder feature of fleet-maintenance software. | **4** | REJECT |
| #4 Heating-oil tank inspection app | **BaseCamp (Global Fueling Systems), Fulcrum (oil-tank inspection checklist app), Field Eagle, SafetyCulture** all offer oil-tank inspection templates today [Brave — VERIFIED]; NORA-cert workflow is a form, not a moat; fuel-oil ERPs (ADD/Cargas) serve the same dealers | **4** | REJECT |
| #6 Oil-tank replacement-lead scoring | homeowner-lead economy owned by insurers + the dealer's own CRM/ERP; data (which tanks are old) sits with the dealer/insurer, not accretable uniquely by founder | **3–4** | REJECT on moat/SAM |

**Findings:**
- **Cargo-tank (#1)**: the horizontal fleet-maintenance category (Fleetio, Whip Around, Samsara,
  Motive) already covers custom DOT inspection templates + PM reminders + document storage. A
  propane bobtail's annual cargo-tank inspection is a *template inside an existing SoR*, not an
  empty category. Density 4.
- **Fuel-oil (#4)**: multiple dedicated inspection apps already exist (BaseCamp, Fulcrum, Field
  Eagle) plus horizontal SafetyCulture; the NORA-cert workflow is a checklist. Density 4. Compounded
  by market trajectory (below).

**Step 2 result: 0 promoted; all die at the incumbent gate.**

---

## Step 3: Market Analysis (recorded for the two that got closest)

- **Cargo-tank (#1)** — buyer = the ~2,000 independent propane/fuel dealers (same universe as
  cycle 086) counting *trucks*, not accounts; even at $200–500/truck/yr across ~30–60K bobtails,
  SAM ≈ **$10–25M**, and it's a document/reminder feature Fleetio/Whip Around bundle for a flat
  per-vehicle fee. **FAILS SAM + incumbent.**
- **Fuel-oil (#4)** — **the fuel-oil / heating-oil market is in secular DECLINE in the US**
  (Northeast heating-oil households falling as gas + heat pumps displace oil; well-documented
  multi-decade downtrend). Per the round-3 MANDATORY growth-rate check, a **declining market is a
  reject even if absolute size passes.** Combined with existing inspection apps ⇒ **REJECT.**
  [Trajectory VERIFIED directionally; exact CAGR ASSUMED negative]

**Step 3 result: 0 promoted.**

---

## Step 4 / Step 5

No candidate reached Step 4. **Zero execution plans.**

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 3 | 7 |
| Step 2 | 3 | 0 | 3 |
| Step 3 | 0 | 0 | — |
| Step 4 | 0 | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates this cycle: 0.**

**Honest read**: Widening to the *asset classes beside* the gas check does not rescue the domain.
- **Cargo-tank / bobtail DOT inspection** is owned by the **horizontal fleet-maintenance SoRs
  (Fleetio, Whip Around, Samsara, Motive)** as a template + reminder feature, and by P3 on the
  compliance side. No unserved gap; SAM (~$10–25M on a per-truck basis) is far below $100M.
- **Fuel-oil tank inspection** faces multiple dedicated inspection apps (BaseCamp, Fulcrum, Field
  Eagle) *and* a **secularly declining market** (heating oil → gas/heat pumps), which the mandatory
  growth-rate check rejects outright.
- Both share the propane domain's ~2,400-company countable buyer universe.

Third consecutive honest zero. Cycle 089 does the final synthesis probe: is there ANY defensible
#2 hiding in the propane/LPG mandated-inspection domain — e.g. a data-aggregation "plant" play
distinct from selling software to the dealer — or is the domain a confirmed zero?
