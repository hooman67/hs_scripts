# Cycle 071 Report — Grease-Trap / FOG Compliance (NFPA-96-adjacent)

**Date**: 2026-07-09
**Domain**: Adjacent to NFPA-96 — restaurant **grease-trap / grease-interceptor pumping + FOG
(Fats, Oils & Grease) compliance manifests.** Same fragmented private contractor (grease hauler)
servicing the same restaurant buyer; same "mandated recurring job + documentation register"
shape as hood cleaning. Thesis: the hauler accumulates a proprietary per-site interceptor +
pump-out + manifest history, powering recompliance scheduling.

**Bottom line up front**: **Honest zero.** FOG has an even worse moat problem than hood cleaning:
the municipality mandates the record and increasingly **owns the system-of-record** (SwiftComply,
Truwave, SAMS run the city FOG programs), so the compounding compliance data accrues to the
**municipal portal**, not the hauler — the exact "moat accrues to the mandated portal" failure
the Round-4 map warns against. And the hauler side is already served by 5+ purpose-built apps.

---

## Step 1: Technology / Product-Angle Discovery (10)

1. **AI pump-cycle predictor** (predict when a trap fills from grease-load history) — TRL 8 — PROMOTED.
2. **Digital FOG manifest generator** (GPS-verified stop → waste manifest PDF) — TRL 9 — REJECTED
   (FAT FINGER, PumpDocket already do exactly this).
3. **Recompliance auto-scheduler on hauler's owned site history** (the thesis core) — TRL 9 — PROMOTED.
4. **Interceptor site-history register** (size, location, pump-outs, FOG readings per site) — TRL 9 — PROMOTED.
5. **Municipal-portal auto-submission** (push manifest to the city FOG portal) — TRL 8 — PROMOTED
   (moat-relevant — but the city owns the record).
6. **Route/density optimizer for pump trucks** — TRL 9 — REJECTED (generic FSM/ServiceCore already).
7. **Grease-recycling / rendering yield tracker** (byproduct value) — TRL 8 — REJECTED (off-thesis, commodity market).
8. **FOG deficiency / enforcement-notice avoidance alerts** — TRL 9 — PROMOTED.
9. **Restaurant-facing compliance dashboard** (owner sees pump history) — TRL 9 — PROMOTED.
10. **Cross-hauler / cross-restaurant FOG registry** (neutral compliance plant) — TRL 8 — PROMOTED
    (network angle — but natural owner = municipality; see gates).

**Step 1 out: 7 promoted, 3 rejected.**

---

## Step 2: Competitive Analysis + ⭐ Incumbent/OEM Check

### Purpose-built hauler / FOG apps already shipping (VERIFIED via search)
| Product | What it does |
|---|---|
| **PumpDocket** | Grease-trap cleaning software + FOG compliance for haulers. |
| **Grease Trap Dispatch** | **AI-predicted pump cycles** + digital manifests. |
| **FAT FINGER** | GPS-verified stops + digital waste manifests (FOG workflow). |
| **ServiceCore** | Scheduling, routing, manifests, invoicing, recurring services (portable-sanitation/hauler FSM). |
| **FieldTracer** | Routes, compliance manifests, dispatch for FOG operators. |

### Municipal-side system-of-record incumbents (the moat-killer, VERIFIED)
| Product | Role |
|---|---|
| **SwiftComply** | Municipal utility software for FOG program oversight + field ops (the same vendor named in the Round-4 backflow-domain kill-risk). |
| **Truwave** | Municipal FOG program management: inspection + manifest tracking. |
| **SAMS (NJB Software)** | Centralizes inspections, pump-outs, manifests, hauler workflows for the authority. |

### Competitive density
- Hauler-facing angles (1,3,4,6,8,9): **density 4** — 5 purpose-built apps + generic FSM.
- Municipal-submission / registry angles (5,10): **density 4** — SwiftComply/Truwave/SAMS own it.

### ⭐ Moat Gate
- **FAIL, harder than hood cleaning.** Where a FOG program exists, the city **mandates a specific
  portal (SwiftComply/Truwave/SAMS)** and the compounding compliance dataset accrues to that
  municipal SoR — the textbook "moat → the mandated portal's vendor," not the founder. The hauler
  app becomes a thin data-entry front-end that must integrate INTO the city portal.
- Where no city program exists, there is no mandate driving non-deferrable demand, so the ROI/
  regulatory tailwind evaporates and it's just another FSM.
- The hauler's own site history is per-tenant (no flywheel), already captured by PumpDocket et al.

**Step 2 out: 1 promoted (Angle 10 for SAM check, bias-to-action) — rest REJECTED.**

---

## Step 3: Market + ⭐ SAM / Growth Check

- The grease/liquid-waste hauling niche is fragmented small operators; hauler-app ACV is low
  ($50–200/mo class, per ServiceCore/PumpDocket positioning — ASSUMED). Even 5–8K US operators ×
  $150/mo × 12 ≈ **$9–14M/yr SAM**, far below $100M.
- The size-viable framing is the municipal program (thousands of US municipalities), but that
  buyer is the **government** → instant-reject, and SwiftComply/Truwave already own it.
- Growth: FOG-hauling grows with foodservice + tightening sewer ordinances but is a low-single to
  mid-single-digit % services market (ASSUMED); does not clear 15% CAGR.

**Step 3 out: REJECTED — SAM < $100M on the private-contractor side; size-viable side is a gov buyer.**

---

## Step 4: ⭐ Buyer Check + Feasibility

- Buyer check: private hauler PASSES; but municipal registry variant = government buyer = FAIL.
- Feasibility: trivial to build (anti-signal). Irrelevant given Step-2/3 failures.

**Step 4 out: REJECTED.**

## Step 5: None. **Zero graduates.**

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 7 | 3 |
| Step 2 | 7 | 1 | 6 |
| Step 3 | 1 | 0 | 1 |
| Step 4 | 0 | 0 | 0 |
| Step 5 | 0 | 0 | — |

**Graduates: 0.**

**Honest read**: FOG is a cleaner illustration of why this whole domain family fails the moat
gate: the municipality mandates a portal and thereby OWNS the compounding compliance record, so
the data flywheel accrues to SwiftComply/Truwave/SAMS, never to the hauler-app founder — while the
hauler workflow itself is already served by PumpDocket, Grease Trap Dispatch, FAT FINGER, and
generic FSM. No founder-unique data asset, SAM < $100M on the private side, government buyer on the
size-viable side. **No #2 candidate.**

Confidence: incumbent existence VERIFIED; market-size + ACV ASSUMED.
