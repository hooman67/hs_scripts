# Cycle 059 Report

**Date**: 2026-07-09
**Round**: 4 (Domain #2 — Septic / Onsite-Wastewater), cycle 4 of 5
**Agent**: Claude (Opus 4.8, 1M) — discovery Agent B
**This cycle's angle**: **Adjacent mandated liquid-waste haul trade — grease trap / FOG (fats-oils-grease) pumping compliance.** Same buyer *class* (fragmented private pumper/hauler with a vacuum truck), stronger recurring regulatory mandate (municipal FOG programs), and a chain-of-custody manifest that could be a founder-owned record. Tests whether an *adjacent* haul trade escapes the septic moat leak.

---

## Why this angle (domain-adjacency, per assignment scope)

Assignment permits "related mandated property-transfer / recurring inspection trades where the operator accumulates a proprietary per-property as-built + service history." FOG is the closest liquid-waste cousin to septic pumping: same trucks/operators, but the mandate is **municipal FOG ordinances** requiring restaurants to pump grease traps on a schedule with a filed **manifest** (chain-of-custody). The per-establishment pump history + manifest could, in principle, be a founder-owned recurring-revenue record.

---

## Step 1: Technology Discovery (angle: FOG haul compliance + manifest)

### 1. Hauler-side FOG manifest + compliance platform (per-restaurant pump history, audit-ready manifests, auto-schedule)
- **TRL**: 8. **Status**: PROMOTED to Step 2.
### 2. AI pump-interval optimizer per grease trap (predict fill from prior manifests)
- **TRL**: 7. **Status**: PROMOTED to Step 2.
### 3. Restaurant-facing FOG compliance dashboard (proof-of-service for the AHJ)
- **TRL**: 8. **Status**: PROMOTED to Step 2.
### 4–10 (rejected at Step 1): city-side FOG program portal (government buyer — instant reject), grease-to-biodiesel feedstock marketplace (commodity trading), IoT grease-level sensor (hardware), NASSCO-style sewer CCTV defect AI (different trade, PACP-owned), lift-station monitoring (utility buyer), used-cooking-oil theft tracking (niche), digester FOG-dosing analytics (utility buyer).

---

## Step 2: Competitive Analysis + ⭐ Incumbent Check + ⭐ Moat Gate

### Incumbent check — the space is already split and taken [all VERIFIED — search excerpts]
| Product | Side | Notes |
|---|---|---|
| **PumpDocket** | Hauler | Disposal records + "audit readiness" for haulers. |
| **DispatchNode / Grease Trap Dispatch** | Hauler | Multi-location compliance data. |
| **SAMS (NJB Software)** | Both | Inspections + pump-outs + manifests + hauler workflows. |
| **FAT FINGER** | Hauler | Mobile app to digitize FOG workflows + manifests. |
| **iFactory** | Hauler | **AI-based pumping-schedule optimization** (idea #2 already built). |
| **Copliancy** | Restaurant | Multi-location restaurant operator compliance. |
| **Truwave, Nexinite** | Municipal | City-side program management (the government-portal SoR). |
| **ServiceCore** (cycle 056) | Hauler | Already serves septic **+ FOG/liquid-waste** haulers — the septic FSM incumbent is already in FOG. |

Every one of the three promoted ideas is already a shipping product (hauler platform, AI schedule optimizer, restaurant dashboard). **Competitive Density: 5/5.**

### ⭐ Moat Gate — FAIL (same leak as septic, plus a mandated city portal)
- The **manifest / compliance record is legally a chain-of-custody document filed to the municipal FOG program** — and cities increasingly mandate their own portals (**Truwave, Nexinite**) to receive it. Where the mandate bites hardest, the compounding compliance record accrues to the **city portal vendor**, not the hauler's software (identical to OnlineRME in septic).
- On the hauler side, the record is already owned by PumpDocket/FAT FINGER/SAMS/ServiceCore. No unique accumulation left for a new entrant.
- Buyer split-risk: the *valuable* aggregate (all restaurants in a city) is the city's, whose buyer is the municipality (instant-reject 12–24mo procurement).

**Moat Gate: FAIL. REJECT at Step 2.**

---

## Step 3: Market Analysis (abbreviated)
- FOG hauling overlaps the same ~7,700 liquid-waste establishments (many pumpers do both septic + grease). Achievable pure-SaaS ACV $1–3K/yr × a few thousand reachable haulers = **sub-$50M SAM**, contested by 6+ incumbents and horizontal FSM. **Status: REJECT.**

## Step 4: Feasibility
- Tech: Low. Moat: none. Market: saturated + partly government-owned. **Feasibility: 2.5/10.**

## Step 5: Execution Plan — **N/A, no graduate.**

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 3 | 7 |
| Step 2 | 3 | 0 | 3 |
| Step 3–5 | 0 | 0 | 0 |

**Graduates this cycle: 0.**

**Honest read**: The adjacent FOG-haul trade reproduces the septic domain's exact failure at higher resolution: a crowded hauler-SoR field (PumpDocket, FAT FINGER, SAMS, iFactory's AI optimizer, ServiceCore) on one side, and a **mandated municipal portal** (Truwave, Nexinite) that captures the compliance flywheel on the other. Moving one trade sideways did not escape the double-sided moat leak. Decisive zero.
