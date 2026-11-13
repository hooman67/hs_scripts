# Deep Research: Wireless TAB Documentation Platform

**Idea slug:** `tab_documentation`
**Type:** Pure SaaS (mobile-first)
**Date:** 2026-06-28
**Researcher:** Step-6 deep-research pass
**Verdict (preview):** NO-GO (downgraded from the cycle-026 "near-zero competition / 8.0 feasibility" thesis — see Section 2).

> **Headline finding:** The cycle-026 premise that this space has "near-zero competition" is **no longer true as of 2026.** A purpose-built competitor (**Air Balancing Pro**, HTIC PTY LTD) shipped on **2026-01-14** and was last updated **2026-06-28 (the day of this research)** — it already implements the exact proposed core (TAB projects, per-outlet measurements, automatic tolerance pass/fail, professional PDF reports, built-in duct sizer). Separately, **measureQuick** ($49/user/mo, free tier, Bluetooth to 80+ tools across 17 brands) is one pivot away, and instrument makers (**Testo**, **Evergreen Telemetry**) give away the Bluetooth data-capture + reporting layer *for free* to sell hardware. Combined with a structurally tiny buyer universe (NEBB: ~750 certified firms / ~3,205 individuals — **VERIFIED**), the SAM and moat no longer justify building. Detail below.

---

## 1. Product Definition

### 1.1 Exact problem statement
- **Who:** NEBB/AABC-certified Testing-Adjusting-Balancing (TAB) technicians and the mechanical contractors / commissioning agents who perform air (and hydronic) balancing on commercial HVAC projects.
- **The pain:** A TAB technician walks a building taking hundreds of airflow / static-pressure / temperature readings at diffusers, grilles, VAV boxes, and AHUs, comparing each to the engineer's design CFM, then iteratively adjusting dampers. Historically this is recorded on **paper field sheets or Excel**, re-keyed back at the office into NEBB/AABC-format report templates — a documentation step estimated at **15–25% of project labor** (ASSUMED, from cycle-026). Transcription errors, lost sheets, and slow turnaround are the daily complaints.
- **Bluetooth angle:** Modern airflow instruments (Testo 405i/410i/420, Evergreen Wireless Wrist Reporter, CPS, AccuTools) now stream readings over Bluetooth LE, removing manual jot-down. **VERIFIED** (Testo Smart Probes are BLE; Evergreen markets "Seamless Bluetooth Connectivity"; measureQuick lists 80+ BLE tools across 17 brands).

### 1.2 Proposed v1 scope (3 features max)
1. **Bluetooth instrument pairing + auto-log by location** — pair to common BLE airflow probes; tap a diffuser on an uploaded floor plan, capture the reading hands-free.
2. **NEBB/AABC-compliant auto-report** — design CFM vs. measured, % deviation, automatic pass/fail per the relevant standard, one-tap PDF in the association's accepted format.
3. **Cloud sync + team/office collaboration** — field tech captures, office reviews/edits/submits; multi-device, multi-user.

**Explicitly NOT in v1:** AI auto-balancing / damper-position optimization (that is a *separate, higher-risk* idea — the "TAB Optimization Engine" from cycle-026); hydronic/water balancing math; CFD; integration with design BIM models.

### 1.3 User workflow (day 1)
Create project → upload floor plan PDF → define systems (AHU/supply/return/exhaust) → walk space, pair probe, tap location, capture reading (auto tolerance check) → review system summary → export NEBB/AABC PDF → office reviews in cloud → submit to GC/owner.

### 1.4 Pricing model
- Proposed: **$99/seat/mo standard, $199/seat/mo with AI correction suggestions.**
- **Reality check:** the incumbent **measureQuick charges $49/user/mo** with a permanently-free real-time tier, and **Air Balancing Pro is free** (with a subscription after a 30-day trial; price not disclosed but the *free-to-start* anchor is set). The $99–199 anchor is now **above market** and must be defended on NEBB/AABC compliance + team workflow alone. (See risks.)

### 1.5 Ideal first customer
Mid-size (5–25 tech) NEBB-certified independent TAB firm in the US that does mostly new-construction commercial commissioning, where formal NEBB report deliverables are contractually required (so compliance has hard value). Buyer = owner/principal or QA manager; small budget authority; trades-conservative.

---

## 2. Competitive Analysis

### 2.1 Direct competitors (same thing, same buyer)

| Competitor | Status / evidence | What it does | Price | Gaps |
|---|---|---|---|---|
| **Air Balancing Pro** (HTIC PTY LTD) | **VERIFIED** via Apple App Store API. Released **2026-01-14**, version 1.0.5, **last updated 2026-06-28** (actively maintained). 0 ratings (new). | "Professional HVAC air balancing and commissioning tool for mechanical contractors, **TAB technicians**, commissioning engineers." Multiple projects; systems (AHU/supply/return/exhaust); outlet airflow capture; **automatic tolerance pass/fail**; system + outlet summaries; **professional PDF reports**; CSV import/export; built-in duct sizer; velocity/pressure-loss/Reynolds calcs. | **Free**, 30-day trial then auto-renewing subscription (price not shown). | **No Bluetooth**, no NEBB/AABC named compliance, **local-only** (data on device, no cloud sync / team collaboration), no AI. iOS only (no Android seen). |
| **measureQuick HVAC** (Manifold Cloud Services) | **VERIFIED** (website + App Store). | HVAC commissioning/diagnostics; **Bluetooth to 80+ tools across 17+ brands** (Fieldpiece, Testo, NAVAC, AccuTools); airflow + static-pressure; cloud dashboard + reporting on paid tier. | Free tier; **Premier $49/user/mo**. | Oriented to residential / light-commercial *system* commissioning and refrigerant verification — **not formal per-outlet TAB-to-design balancing or NEBB/AABC report deliverables**. One pivot away (adjacent mover, below). |
| **BuildingStart / AiRNAB** (est. 2006) | **VERIFIED** (buildingstart.com). | Multi-trade field-data platform; **AiRNAB** module "capture and share air and water balancing data"; offline iOS/Android/Windows; photos, deficiencies, central storage. | Free trial; price by quote. | Dated, multi-trade (not TAB-purpose-built); ~$580K revenue / 9 staff per cycle-026 (ASSUMED) = weak execution but it exists and covers air/water balancing. |

### 2.2 Indirect / manual alternatives
- **Excel + paper field sheets** — the dominant incumbent; free; deeply entrenched ("we've always done it this way" inertia). NEBB/AABC publish blank report **forms** (VERIFIED NEBB offers "TAB Report Forms") that firms fill in by hand or in Excel.
- **Generic field-service / forms apps** (e.g. ServiceTitan, Jobber, GoCanvas, Fulcrum) — not TAB-aware but capture some firms.

### 2.3 Adjacent movers (one pivot away — HIGH risk)
- **measureQuick** already has the hardest pieces (BLE to 17 brands, cloud, reporting, free distribution, installed base). Adding a TAB/per-outlet-to-design report mode is a feature, not a rebuild. This is the single biggest competitive threat.
- **Instrument makers giving the layer away for free to sell hardware:** **Testo Smart Probes app** (BLE probes + free app that logs and exports PDF/Excel reports — probe BLE **VERIFIED**, report export **ASSUMED/known product behavior**); **Evergreen Telemetry** markets BLE TAB instruments with "Data Logging… No paperwork. No re-entry" (**VERIFIED**). A hardware vendor's software does not need to be profitable, which structurally caps software pricing power.

### 2.4 Open-source / DIY
- Trivially DIY-able with Excel + free NEBB/AABC form templates; a competent firm can build an internal spreadsheet in a weekend. Low technical barrier = low willingness to pay.

### 2.5 Big-tech / incumbent risk
- FAANG: negligible (too niche).
- **Industrial-QC incumbents** (SIKORA, Pixargus, Dr. Schenk, Precitec, Marposs, Cognex, Keyence per LEARNINGS #9): **not relevant** — these are inline web/optical inspection firms, not HVAC commissioning. Confirmed out of scope.
- **Real incumbent risk = the instrument OEMs (Testo, Fluke, Evergreen) + measureQuick**, all of whom either already have, or can trivially add, the data-capture+report layer and bundle it with hardware for free.

### 2.6 Competitive density verdict
- Cycle-026 scored this **1/5 (wide open)**. **Updated 2026 assessment: 3–4/5.** A purpose-built, actively-developed direct app now exists (Air Balancing Pro), a well-funded adjacent platform is one feature away (measureQuick), and free OEM apps commoditize the capture layer. The "near-zero competition" thesis is **falsified**.

**Section verdict: NO-GO / at best CONDITIONAL-GO** — only viable if narrowly wedged into *NEBB/AABC-compliant report deliverables + multi-user office workflow*, the one slice none of the above does well. That wedge is real but small and easily copied.

---

## 3. Feasibility & Prototype Plan

Feasibility is **not** the problem here — buildability is high; the problem is competition + market size. Still, the build path:

### 3.1 Technical feasibility — **VERIFIED, low risk**
- Mobile app (React Native / Expo or Flutter) + cloud (Supabase/Firebase). All commodity. **VERIFIED.**
- **Hardest real problem = Bluetooth instrument fragmentation.** There is **no universal BLE GATT standard for airflow probes**; each maker (Testo, Evergreen, AccuTools, CPS, Fieldpiece) uses a proprietary characteristic/protocol, and SDKs are often gated behind partnership agreements. measureQuick's "80+ tools / 17 brands" is itself years of reverse-engineering + partnerships — that integration is the actual moat, and it's already someone else's. **This is the one UNVERIFIED feasibility item**: whether a solo founder can get BLE SDK access from ≥2 instrument makers without a business-development relationship. Likely answer: not easily.
  - **Fallback:** manual keypad entry + CSV import (what Air Balancing Pro does). But that removes the headline "wireless/Bluetooth" differentiator — collapsing the idea into "another air-balancing form app," now occupied.
- NEBB/AABC report templates: documented standards, straightforward to template. **VERIFIED** (forms publicly published by associations).

### 3.2 Phase-0 PoC path (<$100, <1 week)
1. **Day 1–2:** Build an Expo app that connects to **one** cheap BLE device you already have (or a Testo 405i, ~$60, if buyable) and reads a characteristic. If you can't get *any* airflow-probe BLE stream without an SDK NDA, that is the **go/no-go signal** — stop here.
2. **Day 3–4:** Hard-code one NEBB air-distribution report template; render measured-vs-design pass/fail to PDF (react-native-pdf / a serverless Puppeteer render).
3. **Day 5:** Mock floor-plan tap-to-tag. Capture 20 fake readings, export a clean NEBB-style PDF.
- **Cost:** $0 (software) + ~$60 optional probe. **Validates the only uncertain item (BLE access) before committing.**

### 3.3 Software stack (build)
- Front end: Expo/React Native; BLE: `react-native-ble-plx`.
- Backend: Supabase (Postgres + auth + storage); PDF: serverless Chromium/Puppeteer.
- Floor-plan: PDF.js render + tap overlay (no CV needed for v1; "auto room detection" from cycle-026 is over-scoped — drop it).
- Hosting: ~$25–50/mo at PoC scale. **VERIFIED** (standard SaaS economics, >90% gross margin).

### 3.4 Capital & time to working prototype
- **Capital: $30–80K** if mostly self-built nights/weekends (well under the cycle-026 $150–250K, because no AI and no CV). Pure software, no hardware to source. **VERIFIED** as low-capital.
- **Time:** PoC 1 week; sellable MVP ~3–4 months part-time.

### 3.5 Risk register
| Risk | Likelihood | Impact | Mitigation | Fallback |
|---|---|---|---|---|
| BLE SDK access blocked by OEMs | **High** | Kills the "wireless" wedge | Apply to Testo/AccuTools dev programs early | Manual entry + CSV (but then = Air Balancing Pro) |
| measureQuick adds NEBB/AABC TAB mode | Med-High | Erases differentiation | Move fast on compliance + team workflow | None — they have distribution + BLE moat |
| Buyer inertia (Excel/paper) | High | Slow adoption | Land NEBB firms with contractual report needs | — |
| Market too small (see §5) | **High (structural)** | Caps revenue | Expand to all commissioning/hydronic | — |

---

## 4. Customer Validation Strategy

### 4.1 First 5 customers to approach
1. Mid-size NEBB-certified TAB firms (find via the **NEBB "Find a Professional" directory** — ~750 firms listed; **VERIFIED** NEBB has ~750 firms / ~3,205 individuals).
2. AABC member balancing agencies (independent third-party TAB).
3. Mechanical contractors with in-house TAB divisions.
4. Independent commissioning (Cx) agents who sub TAB.
5. The handful of firms already grumbling on **HVAC-Talk forums** and TAB LinkedIn groups about paperwork.

### 4.2 Discovery questions (don't reveal the hand)
- "Walk me through how a balancing report gets from the field to the GC today — what's the slowest part?"
- "How many hours per project go into writing up the NEBB/AABC report after the readings are taken?"
- "What instruments do your techs carry — any Bluetooth ones? Do you use their apps?"
- "Have you tried any apps for this (measureQuick, Air Balancing Pro, BuildingStart)? What happened?"

### 4.3 Demand signal = confirmed
- Verbal "yes I'd pay $X/seat/mo" is weak (trades say yes, don't switch). **Strong signal = a pre-paid pilot or signed LOI from a firm that has *already tried* measureQuick/Air Balancing Pro and found them lacking on NEBB compliance/team workflow.** If firms are happy with the free incumbents, that is the kill signal.

### 4.4 Where buyers congregate
- NEBB & AABC annual conferences/trade shows (highest-signal, per LEARNINGS #14 trade channels), HVAC-Talk forum, "Test and Balance" / TAB LinkedIn groups, ACCA, AHR Expo. (Facebook-group channel less active for this niche than for laser/CNC.)

---

## 5. Scorecard & Verdict

### Market sizing (honest)
- HVAC **services** market: **$72.5B in 2026, 6.38% CAGR** (Mordor Intelligence — **VERIFIED via fetch**). Commissioning ≈ 10% of retrofit project value; ICC rules mandate continuous monitoring for facilities >50,000 sq ft (**regulatory tailwind, VERIFIED via Mordor**).
- TAB **services** sub-segment: ~$6B global / ~$1.5B US (cycle-026 — **ASSUMED**, report pages gated).
- **Software SAM is the killer:** buyer universe is structurally tiny. NEBB ~750 firms + ~3,205 individuals (**VERIFIED**); AABC similar order. Even generously, ~3,000 US TAB firms × ~5 paying seats × ~$50–99/mo (market-clearing price set by free/$49 incumbents) ≈ **$9–18M SAM** — *below* the $100M SAM bar, and that assumes near-total penetration against free competitors. This is a lifestyle-software ceiling, not a venture one. As a **secondary income stream** it could net low-to-mid six figures ARR if executed well, but the moat is thin.

### Scorecard (weighted)
| Dimension | Weight | Score (1-10) | Note |
|---|---|---|---|
| Capital required (lower=better) | 15% | 9 | $30–80K, pure software, no hardware |
| Time to first revenue | 15% | 7 | MVP 3–4 mo, but conversion slow (free incumbents) |
| Competitive moat | 15% | 3 | BLE-integration moat already owned by measureQuick; report-template wedge easily copied |
| Tech risk (lower=better) | 10% | 7 | Build is easy; BLE SDK *access* is the one real uncertainty |
| Market size (SAM) | 10% | 3 | ~$9–18M SAM, below threshold |
| Founder fit | 15% | 8 | Pure SaaS = ideal for Hooman; no hardware, no PhD; but no AI/infra edge leveraged |
| Customer accessibility | 10% | 6 | Reachable via NEBB/AABC directories + shows, but conservative + small |
| Scalability | 10% | 4 | Caps out at a few-thousand-firm niche; expansion needs hydronic/Cx |

**Weighted total ≈ 5.7/10.**

### Verdict: **NO-GO** (as a standalone bet)
The original "near-zero competition" thesis is falsified by a same-quarter direct competitor (Air Balancing Pro, updated the day of this research), a one-pivot-away funded adjacent (measureQuick at $49/mo with the BLE moat already built), and free OEM apps that commoditize the capture layer. The realistic software SAM (~$9–18M, below the $100M bar) and a thin, easily-copied moat make this a marginal lifestyle product rather than a defensible secondary income stream. Capital efficiency and founder-fit are genuinely excellent — but per LEARNINGS #4 (tech-risk fine but moat+market weak) and #2 (capital efficiency can't rescue a weak moat/market), this does not clear the bar. **Hooman's #1 idea (CutLog) has a stronger data-flywheel moat; this should not displace it.**

### Confidence summary
- **VERIFIED:** Air Balancing Pro exists/feature set/dates (App Store API); measureQuick price/BLE breadth; Evergreen BLE + logging; BuildingStart/AiRNAB exists; NEBB ~750/3,205; HVAC services $72.5B/6.38% CAGR + ICC >50k sqft mandate; build stack & margins; low capital.
- **ASSUMED:** TAB sub-segment $6B global/$1.5B US; documentation = 15–25% of labor; Testo app PDF/Excel export; AABC member count order-of-magnitude.
- **UNVERIFIED (critical, resolve in Phase-0):** Whether a solo founder can obtain Bluetooth SDK access to ≥2 airflow-instrument makers without a BD relationship. If not, the "wireless" differentiator collapses and the idea becomes a clone of an existing free app.
