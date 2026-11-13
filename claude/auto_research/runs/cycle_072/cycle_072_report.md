# Cycle 072 Report — Kitchen Fire-Suppression (NFPA-17A) & Fire-Door (NFPA-80) Inspection

**Date**: 2026-07-09
**Domain**: Two NFPA-mandated documentation trades directly adjacent to hood cleaning — the
**NFPA-17A restaurant fire-suppression (Ansul/wet-chemical) semi-annual inspection**, and the
**NFPA-80 annual fire-door inspection.** Both are recurring, mandated, photo/checklist-documented
jobs performed by fragmented private contractors — same shape as hood cleaning, and NFPA-17A is
frequently done by the SAME contractor who cleans the hood. Thesis: the inspector accumulates a
proprietary per-device / per-door inspection + deficiency register enabling recompliance scheduling.

**Bottom line up front**: **Honest zero — and the most crowded of the four cycles.** NFPA-25/72/17A
is the single most-saturated fire-inspection software category in this whole project (Inspect Point
15K users, ServiceTrade, BuildingReports — already documented at ~4.5 in the Fire-Sprinkler
red-team, LEARNINGS.md). NFPA-80 fire doors is served by 9+ purpose-built apps. Both fail the
incumbent gate outright; moat is per-tenant, not a flywheel.

---

## Step 1: Product-Angle Discovery (10)

**Fire suppression (NFPA-17A):**
1. AI photo-verification of nozzle/fusible-link condition — TRL 8 — PROMOTED.
2. Semi-annual recompliance auto-scheduler on inspector's device history — TRL 9 — PROMOTED.
3. Per-system suppression-device register (cylinders, links, nozzles, hydro-test dates) — TRL 9 — PROMOTED.
4. Deficiency → AHJ/insurer report generator — TRL 9 — REJECTED (every fire-inspection app does this).
5. Combined hood-clean + suppression-inspection single record — TRL 9 — REJECTED (HoodClean Pro/Guspora already bundle NFPA-96 + 17A).

**Fire doors (NFPA-80):**
6. AI gap-measurement / drop-test from phone photos/video — TRL 7 — PROMOTED.
7. Per-door annual inspection register + deficiency tracking — TRL 9 — PROMOTED.
8. Annual recompliance auto-scheduler across a facility's door assemblies — TRL 9 — PROMOTED.
9. JCAHO/K-tag mapping for healthcare facilities — TRL 8 — REJECTED (Stark, Fire Inspect Hub already).
10. Cross-facility fire-life-safety compliance registry (network) — TRL 8 — PROMOTED (network angle; watch gates).

**Step 1 out: 7 promoted, 3 rejected.**

---

## Step 2: Competitive Analysis + ⭐ Incumbent Check

### NFPA-17A / fire-inspection incumbents (VERIFIED)
- **Inspect Point** — purpose-built fire-protection inspection, built-in codes, auto-scheduling
  (~15K users per prior project research).
- **ServiceTrade** — fire alarms, fire suppression, fire equipment inspection SoR.
- **HoodClean Pro, Guspora, Essential, Inspectly360, Fire Inspect Hub** — all explicitly cover
  kitchen NFPA-17A suppression (several bundle it WITH NFPA-96 hood cleaning — see cycle 070).

### NFPA-80 fire-door incumbents (VERIFIED, 9 named)
- **Fire Inspect Hub, FireInspected, Krinkle Fire Door, Guspora, Essential, OxMaint, KomplyOS,
  Ember Software, Stark** — all purpose-built NFPA-80 fire-door inspection apps with checklists,
  gap/drop-test capture, deficiency tracking, AI reports.

### Density
- All suppression angles (1,2,3): **density 4–5** (this is the most-saturated fire category in the project).
- All fire-door angles (6,7,8): **density 4** (9 purpose-built apps).
- Registry angle (10): **density 3** — but see moat/buyer gates.

### ⭐ Moat Gate
- **FAIL.** The inspector's device/door history is per-tenant data already accumulated by the
  15K-user incumbent (Inspect Point) and 9 fire-door apps. No founder-unique flywheel.
- The registry angle relocates data to a neutral layer whose natural owner is the AHJ/insurer/
  facility (buyer-gate fail) and duplicates BuildingReports' existing verified-report model.

**Step 2 out: 1 promoted (Angle 10, bias-to-action) — rest REJECTED.**

---

## Step 3: Market + ⭐ SAM / Growth Check

- Fire-inspection software is a real >$100M category IN AGGREGATE — but that size is precisely why
  it is fully owned (Inspect Point/ServiceTrade/BuildingReports). The *un-owned residual* for a new
  entrant is near zero.
- NFPA-17A-only sub-slice (kitchen suppression) overlaps the same few-thousand hood contractors as
  cycle 070 → same sub-$15M SAM ceiling at niche ACV.
- Growth: fire-inspection SaaS grows with construction + code enforcement, mid-single-digit %
  services base (ASSUMED); the *contestable* slice does not clear 15% CAGR OR $100M SAM.

**Step 3 out: REJECTED — aggregate market is owned; contestable residual < $100M SAM.**

---

## Step 4: ⭐ Buyer Check + Feasibility

- Buyer: private fire contractor PASSES; registry variant → AHJ/insurer = FAIL.
- Feasibility: trivial build (anti-signal); the real barrier is distribution against a 15K-user
  incumbent, i.e. Hooman's documented weakness (B2B trust/sales), not his strength.

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

**Honest read**: This is the domain's strongest incumbent wall. Fire suppression/alarm/door
inspection is the most-saturated fire-safety software arena in the entire project — Inspect Point
(~15K users), ServiceTrade, and BuildingReports own NFPA-25/72/17A (already red-teamed to ~4.5 as
"Fire Sprinkler"), and 9 purpose-built apps own NFPA-80 fire doors. Moat is per-tenant, not a
flywheel; the aggregate market is large *because* it's owned. **No #2 candidate.**

Confidence: incumbent existence VERIFIED; ACV/market-size ASSUMED; Inspect Point user count from
prior project research (LEARNINGS.md Fire-Sprinkler red-team).
