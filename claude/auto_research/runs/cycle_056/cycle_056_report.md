# Cycle 056 Report

**Date**: 2026-07-09
**Round**: 4 (domain map cycle 056–060, Domain #2 — Septic / Onsite-Wastewater Inspection & Service)
**Agent**: Claude (Opus 4.8, 1M) — discovery Agent B
**This cycle's angle**: The headline thesis — digitize the septic **inspection + as-built system diagram + service history** so the private operator accumulates a proprietary per-property record.

---

## Domain thesis under test (from round4_domain_map.md #2)

> 60M+ US homes on septic; most states mandate inspection at property transfer and periodic
> operating-permit inspections. Pumpers/inspectors work off paper. Digitize the inspection +
> as-built diagram + service log. **Moat should accrue to the FOUNDER** as a compounding
> per-property as-built graph nobody else holds. Kill-risk: a septic-specific field-service
> SoR (Ritam/Summit, ServiceCore) or a state/county e-permit portal already owns the as-built.

---

## Step 1: Technology Discovery (angle: paper→digital inspection + as-built capture)

### 1. AI photo→report septic inspection generator
- **Domain**: Onsite-wastewater inspection documentation
- **Breakthrough**: Multimodal LLMs turn field photos + tapped measurements into a compliant multi-page inspection PDF in minutes; 50-state form templating is now a prompt/template problem, not custom software.
- **TRL**: 8 (already shipping). **Time to product**: 0–3 months.
- **Status**: PROMOTED (to competitive check) — but see Step 2, it is already a live product.

### 2. Per-property as-built "system graph" capture (tank size, drainfield geometry, component ages, failure history)
- **Domain**: Septic system-of-record
- **Breakthrough**: Mobile mapping + photo-anchored component tagging lets a field tech build a durable per-property diagram in the field.
- **TRL**: 8. **Time to product**: 3–6 months.
- **Status**: PROMOTED to Step 2 (this is the moat-bearing core of the thesis).

### 3. Renewal/recompliance scheduling engine on the owned property history
- **Domain**: Recurring-revenue flywheel
- **Breakthrough**: Due-date prediction from accumulated service intervals + advanced-system permit cadence.
- **TRL**: 8. **Status**: PROMOTED (this is the flywheel that would monetize #2).

### 4–10 (batch-rejected at Step 1 — enumerated for the record)
- Drainfield-failure prediction from soil/hydraulic-loading history (TRL 5, needs proprietary outcome data nobody has), effluent-quality trend ML (data lives in ATU telemetry OEM cloud — cycle 058), homeowner-facing septic "smart tank" IoT (consumer HW, wrong buyer), permit-auto-filing bot (relocates value to the county portal — cycle 060), LiDAR drainfield locating (hardware), inspection-photo defect classifier (feature, not company), voice-to-report transcription (commodity LLM feature).

---

## Step 2: Competitive Analysis + ⭐ MANDATORY Incumbent/OEM Check

**This is where the domain thesis meets reality. The check was run BEFORE any promotion.**

### Septic-specific field-service Systems-of-Record (the named kill-risk)
| Product | What it does | Owns per-property as-built + history? |
|---|---|---|
| **Summit / Array (Ritam)** [VERIFIED — ritam.com] | Full septic-business software: scheduling, service reminders, billing, customer + job-site records, mobile, customer portal. 5 editions (Lite→Premium). | Yes — organizes by customer/job-site with service reminders. Long-established incumbent. |
| **ServiceCore** [VERIFIED — servicecore.com] | "Software for Portable Toilet, Septic, and Dumpster Businesses" — scheduling, routing, billing. Funded, growing. | Yes for service history; bundles septic with porta-john/dumpster (fragmented-operator SoR). |
| **National Onsite** [VERIFIED — search excerpt] | "Organizes service data **by property** rather than customer... attaches all service records, photos, and **component locations** to the physical property address, creating a **permanent, accessible history**." Site maps, mobile-first. | **YES — this is verbatim the founder's moat thesis, already built and shipping.** |
| **Pro-Septic / PRO Software** | Automated pumpout scheduling, custom inspection forms, CCTV job tracking for haulers. | Yes for service records. |
| **SepticMind** | "AI-powered operations platform built specifically for septic service workflows." | Yes; AI-native incumbent. |
| **InspectorData** | Septic inspection software: tank/drainfield/effluent documentation, state-form templates, 90-day trial. | Yes for inspection records. |
| **ServGround** | Design→permit→as-built drawings→inspection for designers/installers. | Yes — explicitly stores **as-built drawings**. |

### AI-native cheap entrant (caps the price of the "digitize with AI" wedge)
- **SepticSnap** [VERIFIED — septicsnap.com]: AI photo→report, 8-page PDF in ~5 min, 50-state + BC compliant, ASHI-verified/InterNACHI-endorsed. **Pricing: $29.99/single report, $99/mo unlimited, $349/mo for 5 seats.** First report free.

### ⭐ Incumbent-check verdict
- **OEM already does it?** N/A (no single hardware OEM), but the **field-service SoR incumbents already ship the exact product**, including the property-anchored as-built history (National Onsite) and AI report generation (SepticSnap, SepticMind).
- **Funded horizontal platform lists this vertical?** Yes — ServiceCore explicitly bundles septic with porta-john/dumpster; generic FSM (Jobber, Housecall Pro, ServiceTitan) also serve pumpers.
- **Incumbent marketing copy = your pitch?** **Yes, near-verbatim.** National Onsite's "permanent per-property history with component locations" IS the pitch. SepticSnap's "AI writes your report" IS the pitch.

**Competitive Density Score: 5/5.** Established incumbents with products in market + an AI-native entrant at $99/mo. **REJECT at Step 2.**

### ⭐ MANDATORY Moat Gate — the decisive failure
Two independent moat leaks:
1. **The as-built + service-history record leaks to the mandated county portal.** **OnlineRME** [VERIFIED] is the mandated system of record in Snohomish, Island, and Pierce Counties (WA) — "required under Snohomish County Board of Health Code." A pumper files the report on-site; it appears instantly in the **health department's** database, which stores **as-built drawings + service history** and exposes them to homeowners. In the jurisdictions with the strongest mandate (the thesis's own demand driver), the compounding record accrues to the **county's portal vendor**, not the founder.
2. **Septic as-builts/permits are largely PUBLIC records** held by county health departments, many online (Snohomish OnlineRME, Pierce, Oregon DEQ for Curry/Jackson/Josephine, Clackamas "As-Built record for the entire septic system") [VERIFIED]. A "proprietary per-property as-built graph" is not proprietary when the county already publishes it — this commoditizes the data asset the thesis depends on.

**Moat gate: FAIL.** The defensible asset accrues to the mandated portal / is public, and where it isn't, a shipping incumbent (National Onsite) already owns the property-anchored history. The operator cannot *uniquely* accumulate compounding data.

---

## Step 3: Market Analysis (run for completeness despite Step-2 kill)

- **Buyer universe**: **~7,717 US septic/drain/sewer cleaning establishments** (IBISWorld 2026, +3.3% YoY) [VERIFIED]. Industry revenue ~$7B (2025) [VERIFIED]; septic-tank equipment market ~4.5% CAGR [VERIFIED].
- **SAM**: Pure-SaaS ACV realistically $1–3K/yr. Even at a generous 6,000 reachable seats × $2K = **$12M ARR ceiling**. To clear SAM>$100M you'd need to own essentially the whole trade at a high ACV — implausible against 7+ incumbents.
- **Countable-buyer-universe red flag**: ~7,700 total buyers is the same structural problem that killed HVAC-TAB in Round 2 (~750 firms / ~$9–18M SAM). Fragmented + countable + low ACV.
- **Status**: REJECT (SAM fails; buyer universe too small at achievable ACV).

## Step 4: Feasibility (abbreviated — idea already dead on moat + SAM)
- Tech risk: Low (it's a CRUD+LLM app — which is exactly why it's already built cheaply by 7+ players).
- Market risk: High (must displace entrenched SoRs; AI wedge already at $99/mo).
- Moat: None that accrues to founder.
- **Feasibility score: 3.0/10.**

## Step 5: Execution Plan
- **N/A — no graduate.** No idea cleared Step 2 (competitive) or the moat gate.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 3 | 7 |
| Step 2 | 3 | 0 | 3 |
| Step 3 | — | 0 | — |
| Step 4 | — | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates this cycle: 0.**

**Honest read**: The core thesis is already a shipped product category. National Onsite implements the exact "per-property permanent history with component locations" moat; SepticSnap/SepticMind implement the AI-report wedge at $99/mo; Summit/ServiceCore/Pro-Septic/InspectorData/ServGround fill the rest. Worse, the compounding data leaks to the mandated county portal (OnlineRME) and septic records are largely public. Moat gate FAIL + SAM fail. This is a decisive death for the headline angle.
