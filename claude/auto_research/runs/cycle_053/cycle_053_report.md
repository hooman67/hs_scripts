# Cycle 053 Report — Adjacent mandated water trades: FOG/grease-trap, meter testing, medical gas

**Date**: 2026-07-09
**Agent**: Round-4 discovery Agent A (Opus 4.8, 1M)
**Domain**: Mandated water/plumbing-adjacent testing trades closely related to backflow, where the *private licensed operator* might accumulate their OWN compounding device/site data (the moat requirement). This cycle scans three: (1) FOG / grease-trap pumping & manifests, (2) large commercial water-meter accuracy testing, (3) medical-gas system verification (NFPA 99 / ASSE 6030).

---

## Step 1: Idea Discovery

### 1. Grease-trap / FOG hauler compliance + manifest app
- **Concept**: FOG haulers pump grease traps on a mandated schedule and must file manifests; digitize the pump job, GPS-verified manifest, per-establishment service history.
- **TRL**: 9. **Status**: PROMOTED to Step 2.

### 2. Large water-meter accuracy-testing service app (AWWA M6)
- **Concept**: Large commercial/industrial meters are periodically tested for accuracy; private meter-testing service companies do this. Capture the test + build a per-meter drift/accuracy history.
- **TRL**: 9. **Status**: PROMOTED to Step 2.

### 3. Medical-gas verification documentation (NFPA 99 / ASSE 6030)
- **Concept**: Medical gas systems in hospitals must be verified/certified by an ASSE 6030 verifier; digitize the verification report + per-facility system history.
- **TRL**: 9. **Status**: PROMOTED to Step 2.

### 4. Cross-connection-control *survey* app (distinct from backflow test)
- **Concept**: Before backflow testing, a hazard survey identifies cross-connections at a site; digitize the survey.
- **TRL**: 9. **Status**: REJECTED at Step 1 — the survey is a utility-program function; wsOne, iWorQ, Hydrocorp, Mango Apps template already own it, buyer is the municipality (instant-reject buyer).

---

## Step 2: Competitive Analysis + ⭐ Incumbent Check + Moat Gate

### Idea 1 — FOG / grease-trap hauler app
- **Incumbent check**: Crowded on BOTH sides. Hauler-side: **PumpDocket, GreaseIQ, ServiceCore, FAT FINGER** (GPS manifests). Municipal-side: **SwiftComply FOG, TrackMyFOG (Aqua Backflow), Truwave, SAMS/NJB, BMPcomp**. Same architecture as backflow: the municipality mandates a FOG-compliance portal that owns the aggregated establishment/manifest data. [VERIFIED]
- **Moat gate**: Identical failure to backflow — the compounding per-establishment FOG history is owned by the municipal portal (SwiftComply FOG / TrackMyFOG), and the hauler-side operating data is already held by GreaseIQ/ServiceCore/PumpDocket. Founder cannot uniquely accumulate. FAIL. Density 5/5.
- **Status**: REJECTED.

### Idea 2 — Large water-meter accuracy-testing service app
- **Incumbent check**: The dominant player is **MARS Company** — they make the field test equipment (VEROflow-4 Touch) AND offer "Meter Testing Solutions (MTS)" as a service + software. Classic **OEM-owns-the-data-feed** pattern: the test-instrument maker bundles the recording software. AllDrive Services also in the space. [VERIFIED]
- **Moat gate**: The hidden hard part is the metrology instrument (VEROflow); MARS owns it and bundles the software free-ish to sell hardware — the exact round-3 "OEM ships it free, caps price at ~$0" pattern. The buyer, moreover, is largely **the water utility itself** (meters are utility revenue-assurance assets) — an instant-reject 12–24mo-procurement buyer, not a fragmented private operator. FAIL on both the OEM moat AND the buyer check.
- **Status**: REJECTED.

### Idea 3 — Medical-gas verification documentation
- **Incumbent check**: The buyer/operator is the ASSE-6030 verifier and the hospital facilities team. Documentation is currently handled by verification firms (e.g., Medical Testing Solutions) plus generic inspection apps (Joyfill, SafetyCulture/iAuditor, Fulcrum) and hospital CMMS. NFPA-99-specific documentation is thin, BUT —
- **Moat gate + buyer + SAM**: (a) The verifier count is tiny — ASSE 6030 verifiers number in the low thousands nationally, and each hospital is verified infrequently → **SAM likely << $100M** at any realistic SaaS ACV. (b) The compounding data (per-facility medical-gas system as-built) is more naturally owned by the hospital's CMMS/facility record than by an itinerant verifier who visits once. (c) The buyer is partly the hospital (long healthcare procurement) rather than a fragmented private operator. Weak on all three gates.
- **Status**: REJECTED — primarily on SAM (too few verifiers / infrequent events) and split buyer; secondarily on data-ownership.

### Competitive Density: FOG 5/5, meter 4/5 (OEM+utility), medical gas 3/5 but fails SAM/buyer.

---

## Steps 3–5
Not reached.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 4 | 3 | 1 |
| Step 2 | 3 | 0 | 3 |
| Step 3–5 | 0 | — | — |

**Graduates this cycle: 0.**

**Honest verdict**: The two trades structurally closest to backflow (FOG haulers, cross-connection surveys) reproduce the exact same failure — a municipal-mandated portal owns the compounding data, and the operator side is already served by 4–6 apps. Large-meter testing fails because the instrument OEM (MARS) owns the data feed and the buyer is the utility. Medical-gas verification is the only one with thin documentation competition, but the operator universe is too small to clear SAM and the data naturally lands in the hospital's record. No graduates. One more cycle to test Legionella/water-management and irrigation-audit adjacencies before closing the domain.
