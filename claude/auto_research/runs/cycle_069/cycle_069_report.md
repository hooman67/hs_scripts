# Cycle 069 Report

**Date**: 2026-07-09
**Round**: 4, Agent D — Domain #4 Cathodic-Protection / Corrosion Survey (AMPP-mandated)
**Cycle focus**: Final sweep of the last untested corners where a CP-service contractor might DURABLY own its accounts (defeating cycle 068's "transient surveyor" moat leak): **marina/dock & marine-facility CP**, **CP-system design/install firms who then service what they built** (recurring O&M on their own installed base), **small-diameter distribution & farm-tap / propane-yard CP**, and a hard look at whether any "own-the-installed-base" recurring model clears all four gates. Then: the **domain-level verdict** for Agent D.

**Mandatory gates**: (1) Incumbent/OEM — American Innovations PCS/Bullhorn/Survey Manager, MOBILTEX CorView, iFactory; (2) Moat to FOUNDER; (3) SAM > $100M; (4) fragmented PRIVATE contractor buyer.

**Carry-forward (the three prior kills)**:
- **066**: pipeline CP core → AI PCS owns the mandated app + operator owns the flywheel; utility buyer. UST-testing path → passes buyer gate but SAM ~$2–12M + thin 3-yr flywheel.
- **067**: AST/API-653 + water-tank inspection → best flywheel in domain (UT/corrosion-rate) but buyer/SAM scissors (enterprise+occupied vs. too-few independents); water tank = municipal buyer.
- **068**: CIS/DCVG survey contractor → structural moat leak (asset owner permanent, surveyor transient) + AI/OEM density 4/5.

---

## Step 1: Technology Discovery

### 1. Marina / dock / marine-facility CP survey + anode-replacement app
- **Domain**: Small marine-facility CP (steel pilings, sheet-pile bulkheads, floating docks)
- **Breakthrough**: Marinas & waterfront facilities have galvanic/ICCP systems on steel pilings needing periodic potential surveys + anode replacement, often serviced by regional marine-service/dive firms with durable client relationships. Digitize the survey + own per-piling history.
- **TRL**: 8
- **Time to product**: 6 mo
- **Status**: PROMOTED (carry to buyer/SAM gate)

### 2. "Service-your-own-installed-base" CP O&M platform for CP design/install firms
- **Domain**: CP contractors who DESIGN+INSTALL systems and then hold the recurring O&M/survey contract on that same installed base
- **Breakthrough**: This is the one model that defeats 068's moat leak — if the contractor OWNS the customer relationship because they built the system, the survey time-series accrues to THEM durably. Digitize their installed-base register + recurring survey + rectifier monitoring.
- **TRL**: 9
- **Time to product**: 5 mo
- **Status**: PROMOTED (this is the cycle's key test)

### 3. Rectifier remote-monitoring SaaS for small CP-service firms (BYO-cell-modem)
- **Domain**: Low-cost rectifier RMU + dashboard for small contractors' installed base
- **Breakthrough**: Commodity cellular IoT + dashboard to undercut AI Bullhorn / MOBILTEX for small firms.
- **TRL**: 7
- **Time to product**: 9 mo
- **Status**: PROMOTED (carry — but hardware-fit flag)

### 4. Propane/bulk-plant & farm-tap CP inspection app
- **Domain**: LPG bulk-plant buried-tank CP + farm-tap distribution CP
- **Breakthrough**: Propane dealers' buried tanks/lines need CP checks; overlaps Domain #9 (propane). Digitize.
- **TRL**: 9
- **Time to product**: 4 mo
- **Status**: REJECTED
- **Reasoning**: Overlaps Agent I (propane, Domain #9) — leave to that agent to avoid double-counting; and buyer/data accrue to the propane ERP (ADD Systems/Cargas) per that domain's kill-risk.

### 5. Galvanic anode remaining-life estimator for small installed bases
- **Domain**: Anode-life analytics
- **Breakthrough**: Predict sacrificial-anode depletion from potential trend on the contractor's own installed base.
- **TRL**: 6
- **Time to product**: 8 mo
- **Status**: PROMOTED (folds into #2)

### 6. CP system design / sizing calculator SaaS
- **Domain**: Engineering design tool for CP designers
- **Breakthrough**: Automate anode-bed sizing, current-demand calc, attenuation modeling.
- **TRL**: 8
- **Time to product**: 5 mo
- **Status**: REJECTED
- **Reasoning**: One-time-per-project tool, no recurring data flywheel; Elsyca / BEASY / SAcP and spreadsheets serve it; tiny buyer universe. Absorbable.

### 7. AMPP CP-tester compliance / cert-tracking + procedure library
- **Domain**: Contractor QA/compliance ops
- **Breakthrough**: Track tester certs, procedures, calibration records.
- **TRL**: 9
- **Time to product**: 4 mo
- **Status**: REJECTED (generic compliance/HR feature; no data moat; tiny WTP)

### 8. Owned installed-base "CP plant" data network (TitlePlant analog)
- **Domain**: Cross-contractor benchmark of installed-base performance
- **Breakthrough**: If enough small CP firms log their installed bases, anonymized anode-performance-by-soil-type becomes a data asset.
- **TRL**: 7
- **Status**: PROMOTED (moat-deepener; evaluate with #2)

### 9. Mobile potential-survey app with offline sync for spotty-signal field
- **Domain**: Core field UX
- **Breakthrough**: Offline-first CP data capture.
- **TRL**: 9
- **Status**: REJECTED (feature of #2, and AI Field Data Collector already offline-capable)

### 10. Insurance/warranty-backed CP performance certificates
- **Domain**: New revenue layer for CP firms
- **Breakthrough**: Issue a "CP-verified" certificate per structure.
- **TRL**: 8
- **Status**: REJECTED (no demand signal; buyers don't ask CP contractors for warranty certs)

---

## Step 2: Competitive Analysis

### "Service-your-own-installed-base" CP O&M platform (idea #2 bundle: +5,8)
- **Competitors found**:
  - **American Innovations PCS Field Data Collector + Survey Manager + Bullhorn** — again, the mature mandated tool; also sold into CP-service firms that work for operators. [VERIFIED]
  - **MOBILTEX CorView** (rectifier/RMU monitoring), **iFactory** (analytics). [VERIFIED]
  - Small firms currently use Excel + the datalogger OEM software + paper. [ASSUMED]
- **Competitive density score**: 3/5 (the enterprise tools exist but are heavy/expensive for a 3–15-person design-install firm; genuine gap at the small-firm price point).
- **Differentiation angle**: A lightweight, installed-base-centric O&M+survey app priced for small CP design-install firms, where the firm's OWN durable installed base is the data asset (defeating 068's transience problem).
- **Status**: BORDERLINE-PROMOTE → the decisive test is SAM (Step 3), because here the moat and buyer gates finally PASS.

### Marina/marine-facility CP (idea #1)
- **Competitors**: Marine-service firms bundle it into dive/maintenance contracts; no dedicated software; AI overkill. Density 2/5.
- **Status**: → Step 3 (SAM risk — very small niche).

### Small-firm rectifier RMU SaaS (idea #3)
- **Competitors**: AI Bullhorn, MOBILTEX CorView own remote monitoring. Density 4/5, AND it requires a hardware/cellular build that inverts founder-fit. **REJECTED** (incumbent + founder-fit).

---

## Step 3: Market Analysis

### "Service-your-own-installed-base" CP O&M platform (the domain's best-surviving candidate)
- **Buyer (gate 4)**: The **small private CP design-install-service firm** — fragmented, pays directly. **PASSES.** (These firms sell to end-owners but the SOFTWARE buyer is the firm itself.)
- **Moat (gate 2)**: Because the firm holds a durable O&M relationship on systems IT installed, the survey/rectifier time-series accrues to the firm's platform and compounds. **PASSES** (the first candidate in four cycles to pass the moat gate cleanly), with idea #8's cross-firm benchmark as a network-effect deepener.
- **Market sizing (bottom-up, honest — this is where it dies)**:
  - The universe of independent CP-service/design-install firms in the US is **small — plausibly ~500–2,000 firms** [ASSUMED; could not verify a firm count or the AMPP CP-tester population via live search — searches were CAPTCHA-blocked. Mark UNVERIFIED]. The industry is regionally concentrated and many CP techs work for the big service majors (Corrpro/Aegion, MATCOR, Mears) or in-house at operators.
  - At a realistic **$3,000–8,000/yr** per-firm SaaS ACV (small firms, price-sensitive), SAM ≈ **$1.5M–$16M**.
- **Growth rate**: Corrosion-control demand stable-to-modest; not a >15% CAGR software category on its own. [ASSUMED]
- **Status**: **REJECTED**
- **Reasoning**: Clears buyer AND moat (finally), but **fails SAM > $100M by roughly 10×**. The buyer universe is a countable few-thousand-firm trade — the exact "countable buyer universe is a red flag" pattern (TAB, cycle 066/067). There is no realistic ACV × seat count that reaches $100M SAM in the independent-CP-firm segment.

### Marina/marine-facility CP
- **SAM**: Sub-$50M niche (a few thousand marinas with steel structures, low software ACV). **REJECTED** on SAM.

---

## Step 4: Feasibility Analysis

No idea reached Step 4. The best candidate (installed-base O&M platform) passed buyer + moat but failed SAM at Step 3.

---

## Step 5: Execution Summary

**No graduates this cycle. No graduates for Agent D across cycles 066–069.**

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 5 (bundled) | 5 |
| Step 2 | 3 | 1 borderline | 2 |
| Step 3 | 2 | 0 | 2 (SAM) |
| Step 4 | 0 | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates this cycle: 0.**

---

## DOMAIN-LEVEL VERDICT — Cathodic-Protection / Corrosion Survey (Agent D, cycles 066–069)

**This domain returns an honest ZERO. It does NOT hold a defensible #2 candidate for a solo software founder.** The four cycles map cleanly onto four independent kill mechanisms, and every viable segment trips at least one:

1. **Pipeline/utility CP core** — the mandated survey app already ships (**American Innovations PCS Field Data Collector + Survey Manager**, used by 90%+ of major operators; VERIFIED), the flywheel accrues to the **operator's PCS/Bullhorn/CorView system-of-record**, and the buyer is a utility/pipeline operator on 12–24mo procurement = **instant-reject buyer + occupied incumbent + moat-to-incumbent** (066, 068).

2. **The structural moat leak** — in surveying, the *structure is owned by a permanent operator* while the *survey contractor is a rotating, bid-selected vendor*. The compounding time-series therefore cannot durably accrue to the contractor's platform. This defeats every "CP survey contractor app" (068).

3. **Where a contractor DOES durably own accounts** (UST testing, own-installed-base O&M firms, marinas), the **buyer universe is a countable few-thousand-firm trade → SAM ~$2–16M, ~10× short of the $100M gate**, and the flywheel is thin (UST = 3-yr cadence). Passing the buyer and moat gates still can't rescue a sub-$100M SAM (066, 069).

4. **The one segment with a genuinely dense/compounding flywheel** (AST/API-653 UT-corrosion time-series) has its money on the **large owner-operator** side (occupied by AVEVA/Meridium/Antea APM) or the **municipal water utility** — wrong buyer, occupied incumbent (067).

**No segment simultaneously satisfies: fragmented private buyer + founder-owned compounding data + SAM > $100M + unoccupied by AI/OEM.** The domain's central thesis ("own the multi-year potential time-series per structure") is real as a data idea but is structurally mis-aligned: the party that owns the time-series is the asset operator (an instant-reject buyer with an incumbent SoR), not the fragmented contractor.

**Confidence note**: Incumbent findings (American Innovations PCS/Bullhorn/Survey Manager targeting 90% of major operators; MOBILTEX CorView; iFactory; Titan Cloud UST-owner focus) are **VERIFIED** via vendor sites/search. The buyer-universe / firm-count figures used in the SAM kills are **UNVERIFIED** (live search was CAPTCHA-blocked mid-cycle) — but the SAM gap is ~10×, so even a 2–3× undercount of firms would not change the verdict. Recommend NOT advancing any CP/corrosion-survey idea to deep research (Step 6).
