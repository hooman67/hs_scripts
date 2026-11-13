# Cycle 070 Report — Commercial Kitchen Exhaust / Hood Cleaning (NFPA 96), CORE

**Date**: 2026-07-09
**Domain (Round-4 map #5)**: Commercial Kitchen Exhaust / Hood Cleaning (NFPA 96).
**Thesis under test**: A hood-cleaning contractor digitizes the mandated job (before/after
photo-evidence report + certification sticker/QR + next-due scheduling) and accumulates a
proprietary **site-history + photo-evidence register** across all restaurants they service,
powering automated recompliance scheduling (recurring revenue). Moat = that register. Named
kill-risk = horizontal FSM (ServiceTitan/Jobber/Housecall Pro) adding a hood template, or a
hood-cleaning-specific app locking the niche.

**Bottom line up front**: The named kill-risk is not hypothetical — it is already reality.
This cycle found **7+ purpose-built hood-cleaning / NFPA-96 apps already shipping the exact
thesis** (photo-evidence register + compliance certificate + recurring recompliance
scheduling), including one (HoodOps) that ADDS AI photo-analysis and insurer-accepted proof.
Core thesis = **honest zero**. All Step-1 angles collapse at the incumbent gate or moat gate.

---

## Step 1: Technology / Product-Angle Discovery (10)

Angles are product framings of the "AI/software on the mandated NFPA-96 job" thesis.

### 1. AI photo-analysis grease-depth + NFPA-96 violation detector (from job photos)
- **Angle**: Vision model reads crew before/after photos, auto-measures grease depth (mils),
  flags NFPA-96 deficiencies, auto-issues the compliance certificate.
- **TRL**: 8 (commodity vision + LLM captioning). **Status**: PROMOTED to Step 2 (novel-ish).

### 2. NFPA-96 photo-report generator (CompanyCam → branded PDF)
- **Angle**: Turn field photos into the purveyor/insurer-format NFPA-96 report PDF.
- **TRL**: 9. **Status**: REJECTED at Step 1 — trivially built; `hoodcleaningreport.com` already
  does exactly "CompanyCam photos → branded NFPA-96 report PDF." Absorbable feature.

### 3. Recompliance auto-scheduler on the contractor's owned site history
- **Angle**: Schedule next clean by NFPA-96 frequency class (monthly/quarterly/semi/annual)
  per site, auto-remind. This is the claimed moat (recurring-revenue flywheel).
- **TRL**: 9. **Status**: PROMOTED to Step 2 (this IS the thesis core).

### 4. Certification sticker / QR register (scan sticker → last-clean history)
- **Angle**: QR sticker on the hood; AHJ/owner scans to see clean history.
- **TRL**: 9. **Status**: PROMOTED to Step 2.

### 5. Insurer-accepted compliance proof feed
- **Angle**: Push sealed NFPA-96 records to the restaurant's insurance carrier as accepted proof.
- **TRL**: 8. **Status**: PROMOTED to Step 2 (moat-relevant — but who holds the record?).

### 6. Route/density optimizer for multi-restaurant nightly cleaning routes
- **Angle**: Optimize crew routes across the book of restaurants.
- **TRL**: 9. **Status**: REJECTED at Step 1 — generic FSM (Jobber/ServiceTrade) already
  route-optimizes; not NFPA-specific.

### 7. NFPA-96 frequency-class recommender (cooking-type → schedule)
- **Angle**: Classify cooking volume/type (solid fuel, high-volume, moderate, low) to set the
  code-mandated inspection frequency automatically.
- **TRL**: 9. **Status**: PROMOTED to Step 2 (small differentiator).

### 8. Access/rooftop-fan condition tracker with photo timeline per component
- **Angle**: Per-component (hood, duct, fan, filters) longitudinal photo timeline.
- **TRL**: 9. **Status**: PROMOTED to Step 2 (part of site-history register).

### 9. Grease-fire liability / deficiency documentation shield
- **Angle**: Immutable timestamped photo record to defend the contractor against liability.
- **TRL**: 9. **Status**: PROMOTED to Step 2.

### 10. Cross-contractor restaurant compliance registry (network play)
- **Angle**: A neutral registry where ANY contractor's clean history for a site is visible to
  the owner/AHJ/insurer — a "compliance plant" for the food-service built environment.
- **TRL**: 8. **Status**: PROMOTED to Step 2 (the only true network-effect angle — but it
  relocates data OFF the founder's contractor app; watch the moat + buyer gates).

**Step 1 out: 8 promoted, 2 rejected.**

---

## Step 2: Competitive Analysis + ⭐ MANDATORY Incumbent/OEM Check

**This is where the domain dies.** The incumbent check returns a crowded, recently-funded field
of purpose-built apps — the opposite of the "incumbents aren't watching" premise.

### Purpose-built hood-cleaning / NFPA-96 apps already shipping (VERIFIED via product pages / search)
| Product | What it already does | Source |
|---|---|---|
| **HoodOps** (gethoodops.com) | **AI analyzes job photos for NFPA-96 violations + grease depth, auto-generates compliance certificates, recurring scheduling (7/5/3/1-day reminders by NFPA-96 frequency), offline field workflow, EvidLY insurer-accepted proof.** $99/mo. Launch Aug 2026, founder is IKECA-certified NFPA-96 expert witness. | gethoodops.com |
| **HoodClean Pro** (hoodcleanpro.com) | NFPA-96 hood reports + NFPA-17A suppression inspections, CRM, scheduling, invoices, payments, QuickBooks sync. "The #1 App for Commercial Kitchen Exhaust & Fire." | search + product copy |
| **Hood Cleaning Report** (hoodcleaningreport.com) | CompanyCam photos → branded NFPA-96 report PDFs. | search |
| **MyHoodClean** (myhoodclean.com) | Before/after photos, grease depth in mils, component checklist, deficiency log, fire-suppression check. | search |
| **Claver** (goclaver.com/industries/hood-cleaning) | NFPA-96 recurring billing, route optimization, fire-marshal-acceptable compliance photos. | search |
| **Guspora** (guspora.com/industries/kitchen-hood) | NFPA-17A/96 checklists, before/after photo docs, scheduling. | search |
| **FAT FINGER** (fatfinger.io) | Digitizes NFPA-96 workflow: before/after photos + compliance certificates. | search |

### Horizontal FSM already in the vertical (the named kill-risk, VERIFIED)
- **ServiceTrade**: ships "mobile kitchen exhaust cleaning software to schedule and manage
  service jobs and take photos"; used by real hood contractors (e.g. SoCal Hoods documents its
  14-step process + full compliance docs through ServiceTrade). Also owns fire-suppression
  inspection (NFPA-17A/25/72) — see cycle 072.
- **Jobber / Housecall Pro**: multi-trade FSM explicitly positioned for contractors who run
  hood cleaning as one of several trades (HVAC, fire suppression, pressure washing, dryer vent,
  grease trap). Templates + recurring scheduling + photos are core FSM features.

### Per-angle competitive density
| Angle | Density (1–5) | Why |
|---|---|---|
| 1. AI photo grease/violation | **4** | HoodOps already ships exactly this. |
| 3. Recompliance auto-scheduler | **5** | Every niche app + all horizontal FSM do recurring scheduling. |
| 4. Cert sticker/QR register | **4** | Standard in the niche apps; also a generic QR feature. |
| 5. Insurer-accepted proof feed | **4** | EvidLY (via HoodOps) already does this — and it MOVES the moat to the insurer layer. |
| 7. Frequency-class recommender | **4** | Absorbable one-page rule; niche apps encode NFPA-96 frequency. |
| 8. Component photo timeline | **4** | Part of MyHoodClean / HoodClean Pro today. |
| 9. Liability documentation shield | **4** | Timestamped photo record is inherent to every one of these apps. |
| 10. Cross-contractor registry | **3** | No dominant registry yet — BUT see moat + buyer gates below. |

### ⭐ MANDATORY Moat Gate
- The claimed moat is the contractor's **own site + photo history**. It is real switching-cost
  lock-in, but it is **NOT a flywheel/network-effect moat**: my contractor's site history does
  not make your jobs better. It is per-tenant data every one of the 7 incumbent apps already
  accumulates for its own users. Cloning the UI clones the moat (the exact failure mode
  LEARNINGS.md flags as "absorbable feature, not a company").
- Angle 10 (cross-contractor registry) is the only true network effect — but it **relocates the
  compounding data OFF the founder's contractor app into a neutral registry**, and its natural
  owner/buyer is the insurer or AHJ (see buyer gate). Fails "moat accrues to the FOUNDER."
- **The insurer angle actively INVERTS the moat**: EvidLY already positions the record as
  "insurance-ready proof their carrier accepts" — the verification value is migrating to the
  insurer's accepted-proof layer, not a new contractor app.

**Moat gate: FAIL for all 8 angles.** No angle gives the founder a uniquely accumulable,
compounding data asset that the 7 incumbents (or the horizontal FSMs) don't already hold.

**Step 2 out: 1 promoted (Angle 10, on bias-to-action, to test SAM/buyer) — all others REJECTED
at the incumbent + moat gate.**

---

## Step 3: Market Analysis + ⭐ SAM / Growth Check (Angle 10 only)

- **Market size**: Kitchen-exhaust-cleaning services reported at ~$0.34–1.2B global (varies by
  source) growing ~6.5–8.8% CAGR (ASSUMED — multiple low-confidence market-research blurbs;
  no IBISWorld access). Growth passes >15%? **No — ~6.5–8.8% CAGR, below the 15% bar.**
- **Reachable seat count (the binding constraint)**: IKECA membership ~250–400 companies
  (VERIFIED range from search). Total US hood-cleaning firms is a fragmented long tail of small
  operators — plausibly low-single-digit thousands, mostly 1–3 crews (ASSUMED).
- **SAM math (niche-app play, for reference)**: even a generous 5,000 US firms × $200/mo × 12 =
  **$12M/yr** — an order of magnitude below the $100M SAM bar. Niche ACV ($99–300/mo, per HoodOps
  $99) × a few-thousand-firm universe cannot clear SAM > $100M.
- **Angle 10 (registry)**: a registry monetized per-restaurant-site could in theory address the
  ~ hundreds of thousands of US commercial kitchens — but the payer would be the insurer/AHJ,
  which fails the buyer gate below, and the value migrates to that payer, not the founder.

**Step 3 out: REJECTED.** Growth <15% CAGR AND the fragmented private-contractor buyer universe
is too small for SAM > $100M at niche ACV. The only size-viable framing (registry across all
kitchens) violates the buyer gate.

---

## Step 4: ⭐ Buyer Check + Feasibility

- **Buyer check**: The intended buyer (fragmented private hood-cleaning contractor) is correct
  and non-AHJ — this single gate PASSES. But the size-viable registry variant flips the buyer to
  the **insurer / AHJ / fire-marshal** = instant-reject 12–24-mo procurement buyer.
- **Feasibility**: Technically trivial for this founder (vision + LLM + CRUD scheduling; ~$100–200K
  MVP). But trivially buildable + no flywheel = exactly the anti-signal LEARNINGS.md warns is a
  *failure* signal, not a green light. Feasibility score irrelevant given Step-2/3 failures.

**Step 4 out: REJECTED.**

---

## Step 5: Execution Plan

None. **Zero graduates this cycle.**

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 8 | 2 |
| Step 2 (incumbent + moat) | 8 | 1 | 7 |
| Step 3 (SAM + growth) | 1 | 0 | 1 |
| Step 4 (buyer + feasibility) | 0 | 0 | 0 |
| Step 5 | 0 | 0 | — |

**Graduates: 0.**

**Honest read on the core domain**: The Round-4 map rated this "medium-high conviction." The
evidence says otherwise. The named kill-risk (horizontal FSM template) is fully realized, AND a
dense field of 7+ purpose-built NFPA-96 apps — several launched in 2026, one with AI photo
analysis + insurer-accepted proof (HoodOps, Aug 2026) — already ships the entire thesis. The
site-history register is real switching-cost lock-in but not a founder-unique flywheel; it is a
per-tenant feature every incumbent already has. Growth (~6.5–8.8% CAGR) is below bar and the
private-contractor buyer universe (~IKECA 250–400 members; low-thousands total) cannot clear
SAM > $100M at $99–300/mo. This is a textbook "cheap + trivial + no flywheel = absorbable
feature" domain (the PestDoc / Fire-Sprinkler failure mode). **No defensible #2 candidate here.**

Confidence: incumbent existence VERIFIED (live product pages/search); market-size figures
ASSUMED (low-quality secondary sources, IBISWorld blocked); seat-count ASSUMED.
