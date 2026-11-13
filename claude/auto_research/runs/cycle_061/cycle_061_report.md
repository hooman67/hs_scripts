# Cycle 061 Report — ROUND 4 (Domain #3: Water-Well Drilling & the private "Well Plant")

**Date:** 2026-07-09
**Domain assigned:** Water-well drilling — core "well plant" thesis + driller field-ops.
**Agent:** Claude (Opus 4.8, 1M ctx). Method: full funnel Steps 1–5 with the 4 MANDATORY
Round-4 gates (Incumbent/OEM check, Moat gate, Growth+SAM, Buyer check).

> **Research-tooling note.** WebSearch unavailable; Google/DuckDuckGo/Bing were CAPTCHA/403-
> blocked. I fell back to direct fetches of authoritative pages (NGWA, USGS, TX-TWDB, CA-DWR
> open-data portal, vendor sites) plus Jan-2026 domain knowledge. Live-fetched claims are
> marked VERIFIED; others ASSUMED/UNVERIFIED.

---

## TL;DR (honest outcome)

**GRADUATES: 1 (conditional, low ~4.5/10).** The **core thesis of the domain fails the moat
gate — decisively, on the exact kill-risk the domain map named.** Water-well drillers are
*mandated by the state to FILE* their completion/lithology logs, and **the states then PUBLISH
those logs — including lithology and construction detail — as free open public data** (Texas
SDR: full driller's reports 2003–present, downloadable shapefiles + full DB exports, VERIFIED;
California DWR: geologic logs + casing + per-well PDFs, public-domain license, CSV/ArcGIS,
VERIFIED; USGS NWIS nationally, VERIFIED). So the "proprietary subsurface plant" **is not
proprietary — it is a government-published commodity.** This is the polar opposite of
TitlePlant, which survived precisely because title agents *assemble* a plant nobody re-publishes
wholesale. Here the regulator does the aggregation and gives it away.

Worse, an incumbent SoR — **DrillerDB** ($99–299/mo, all 50 states, VERIFIED) — already
(a) owns the driller workflow (field logs, lithology, **state e-filing**, scheduling,
invoicing), AND (b) has **aggregated 18M+ well records from state archives into a free "Well
Map,"** AND (c) already ships **"AI quotes from local well data"** — i.e. the exact
local-data prediction product this thesis proposed. The moat accrues to DrillerDB (and to the
states), never to a new founder.

The **only structurally-valid own-data angle** is rig *operational* telemetry (rate-of-
penetration / bit / air-mud parameters — a CutLog-analog "drilling-parameter flywheel") because
that data is **not** state-filed. It graduates conditionally but grades low: tiny trade
(~8,085 firms), marginal WTP on cheap shallow holes, and it collides with the heavily-served
oil&gas drilling-optimization space.

---

## Step 1 — Ten ideas scanned

| # | Idea | One-line | Verdict |
|---|------|----------|---------|
| 1 | **Water-Well "Well Plant"** | Proprietary subsurface DB from digitized completion logs; sell yield/formation prediction | REJECT (Step 2 — moat) |
| 2 | Driller field-logging + auto state e-filing app | Mobile capture of well log → auto-file state completion report | REJECT (Step 2 — incumbent) |
| 3 | Completion-report OCR/normalizer | Turn scanned state PDF logs into structured data | REJECT (Step 2 — commodity) |
| 4 | AI well-cost/bid estimator from local logs | Price a job from nearby historical wells | REJECT (Step 2 — incumbent ships it) |
| 5 | County depth-to-water / yield prediction map | Predict water depth & yield for a parcel | REJECT (Step 2 — public data) |
| 6 | Well-driller CRM / dispatch / invoicing | Vertical field-service mgmt for drillers | REJECT (Step 2 — incumbent + horizontal) |
| 7 | Well-permit application automation | Auto-fill & submit drilling permits to the state | REJECT (Step 2 — thin, per-state) |
| 8 | **Rig operational-telemetry flywheel** | Log ROP/bit/air-mud params vs formation; cross-shop drilling-parameter optimizer (CutLog-analog) | **PROMOTE** |
| 9 | Pump-service / well-rehab recommender | Recommend rehab from well history | REJECT (Step 2 — low value, siloed) |
| 10 | Well-owner lead-gen marketplace | Connect well owners to drillers | REJECT (Step 1 — not a data plant; Angi/Thumbtack) |

All ideas are TRL ≥ 6 (mobile capture + LLM/OCR + tabular ML are shipping today); ≤ 12 mo to
product. Technical readiness is not the constraint — moat is.

---

## Step 2 — Competitive density + MANDATORY Incumbent/OEM check + Moat gate

### The domain-wide incumbent/OEM finding (applies to 1–7, 9)
- **DrillerDB** (VERIFIED via drillerdb.com): $99 Starter / $299 Pro per month, all 50 states.
  Captures quotes, scheduling, **well logs + lithology**, **state e-filing of completion
  reports**, job maps, invoicing, mobile app. Maintains a free **"Well Map" aggregating 18M+
  well records** from state archives, and the Pro tier ships **"AI quotes from local well
  data."** This single product occupies ideas #1, #2, #4, #6 and touches #3, #5, #9.
- **Other driller apps** (VERIFIED via search snippets): WellSites, MyWaterWell, Fulcrum "Well
  Drilling Report," WinLoG (GAEA Technologies borehole logs). Fragmented but present.
- **The states themselves are the "OEM"** for the data: TX-TWDB SDR and CA-DWR both publish
  full driller logs with lithology as open/public-domain downloads (VERIFIED); USGS NWIS
  nationally (VERIFIED). The raw "plant" is free to everyone.

### Moat-gate verdicts
- **#1 Well Plant — REJECT.** The defensible asset (subsurface log database) is **published
  free by the state and already aggregated by DrillerDB's Well Map.** No exclusivity is
  possible; the value-add (interpretation/prediction) runs on the *same free dataset* any
  competitor can pull. Fails the Round-4 moat gate by construction. This is the exact kill-risk
  named in the domain map, now CONFIRMED REALIZED.
- **#2, #6 field-logging/CRM — REJECT.** DrillerDB owns the SoR at $99–299/mo; horizontal FSM
  (Jobber, ServiceTitan) also present. Density 4. No founder-accruing data moat.
- **#3 OCR normalizer — REJECT.** States already publish structured CSV/shapefile exports;
  DrillerDB structures logs. Absorbable feature, not a company. Density 4.
- **#4 bid/cost estimator — REJECT.** DrillerDB's "AI quotes from local well data" *is* this
  product, built on free public data. Incumbent-marketing-copy = the pitch. Density 4.
- **#5 depth-to-water/yield map — REJECT.** Runs entirely on free USGS/state data; multiple
  free public viewers exist; low WTP. Density 4.
- **#7 permit automation — REJECT.** Per-state, thin, and DrillerDB e-files. Buyer friction.
- **#9 pump-rehab recommender — REJECT.** Low decision value; DrillerDB has a pump-service
  module; data siloed to one shop = no flywheel.
- **#8 rig operational-telemetry flywheel — PROMOTE (density 2–3).** ROP/bit/air-mud parameters
  are **NOT filed with the state**, so a driller *does* uniquely accumulate this operational
  data — the one genuine CutLog-analog own-data angle in the domain. Incumbent check: oil&gas
  drilling-optimization is heavily served (Corva, Nabors SmartROS, Halliburton, Pason), but
  **water-well** rig telemetry is not. Promote with the parameter-sharing flywheel as the
  required differentiation.

---

## Step 3 — Market sizing + MANDATORY growth-rate check (idea 8 only)

- **Industry base (VERIFIED, NGWA):** ~**500,000 new residential wells/yr**; **13.1M+**
  US households on private wells; **~8,085 groundwater contracting firms** operating **18,460
  drilling machines**. ~39M groundwater wells globally (Wikipedia, VERIFIED-ish).
- **TAM:** water-well drilling services revenue is a multi-$B industry (ASSUMED ~$3–5B US;
  IBISWorld page 404'd this cycle — UNVERIFIED). Passes TAM>$1B.
- **SAM (the binding constraint):** the buyer universe is only **~8,085 firms.** At a generous
  $150/mo per firm and an optimistic 25% reachable penetration → ~2,000 seats × $1,800/yr ≈
  **$3.6M ARR.** Even at $300/mo and 40% penetration → ~$11.6M. **SAM is an order of magnitude
  below the $100M bar.** This is a countable-thousands micro-trade — the same red flag that
  killed HVAC-TAB (~750 firms) in Round 2.
- **Growth:** water-well drilling grows roughly with housing/rural development, low-single-digit
  %/yr (ASSUMED); not a >15% CAGR story. A geothermal-loop tailwind exists but is a different
  cycle (063).
- **Verdict: promote to Step 4 only to record feasibility; it FAILS the SAM gate.**

---

## Step 4 — Feasibility (idea 8)

- **Technical risk: LOW-MED.** Logging ROP/air/mud is straightforward; the ML value (predict
  penetration/formation to optimize the run) is real but marginal on cheap shallow holes.
- **Market risk: HIGH.** Water-well margins are thin; a $150–300/mo optimizer competing with
  "the driller already knows their local formations" and a free DrillerDB is a hard sell.
- **Execution risk: HIGH.** Cold-start flywheel needs many shops sharing operational data they
  view as competitive edge; ~8,085-firm ceiling caps the network.
- **Timing risk: LOW.** Tech is ready now.
- **Capital:** ~$150–250K (pure SaaS). **Founder fit: 7/10** (pure software/ML). But two HIGH
  risks (market + execution) + a failed SAM gate.
- **Feasibility score: 4.5/10.** Two HIGH-risk dimensions breach the "no more than one High"
  bar. Graduates **CONDITIONALLY** only as the domain's least-bad candidate.

---

## Step 5 — Execution summary (conditional graduate)

### Rig Operational-Telemetry / Drilling-Parameter Flywheel (4.5/10)
- **Product:** mobile/tablet app that logs rate-of-penetration, air/mud, and bit data against
  formation depth on each water-well job; cross-shop anonymized parameter benchmarking predicts
  penetration and flags bit/air-program changes for the next comparable hole (CutLog for water
  drilling).
- **Moat (weak):** operational rig data is NOT state-filed, so it is the one thing the driller
  uniquely accumulates — but the network ceiling is ~8,085 firms and the per-shop edge is small.
- **Market:** ~8,085 US firms; SAM ~$3.6–11.6M — **below the $100M bar.**
- **Capital:** $150–250K pure SaaS.
- **Why it's still only conditional:** fails SAM; two HIGH-risk dimensions; DrillerDB owns the
  workflow the app must ride on. This is a feature DrillerDB could add, not a standalone company.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|----|----------|----------|
| Step 1 | 10 | 1 | 9 |
| Step 2 | 1 | 1 | (7 rejected here) |
| Step 3 | 1 | 1* | (fails SAM, recorded) |
| Step 4 | 1 | 1 (conditional) | — |
| Step 5 | 1 | 1 (conditional, 4.5) | — |

**Graduates this cycle: 1 conditional (4.5/10).** *promoted-to-record despite failing SAM.

**Domain read (this cycle):** the headline "well plant" thesis is **dead on the named kill-
risk** — states publish full lithology logs as free open data and DrillerDB already aggregated
them and shipped the AI-prediction product. The moat accrues to the government + the incumbent
SoR, never to a solo founder. Only non-state-filed operational telemetry offers a real own-data
flywheel, and that trade is too small (SAM ≪ $100M). Not a defensible #2.
