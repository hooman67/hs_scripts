# Cycle 060 Report

**Date**: 2026-07-09
**Round**: 4 (Domain #2 — Septic / Onsite-Wastewater), cycle 5 of 5 — **domain wrap-up**
**Agent**: Claude (Opus 4.8, 1M) — discovery Agent B
**This cycle's angle**: Last-chance search for a founder-owned wedge the first four cycles missed — the **inspection-form/permit-e-filing "middleware"** angle and the **county-portal integration** angle — then synthesize a domain verdict for cycles 056–060.

---

## Step 1: Technology Discovery (angle: e-filing middleware / portal integration / niche wedges)

### 1. Universal septic-report e-filing middleware (one app that files into any county's portal/OnlineRME + generates every state form)
- **Breakthrough**: LLM form-templating across 50 states + API/scrape bridges to county portals.
- **TRL**: 7. **Status**: PROMOTED to Step 2.
### 2. Inspector marketplace / lead-gen for time-of-sale septic inspections
- **TRL**: 8. **Status**: PROMOTED to Step 2.
### 3. Installer bid/estimate + as-built handoff tool (design→install→county submittal)
- **TRL**: 8. **Status**: PROMOTED to Step 2.
### 4–10 (rejected at Step 1): septic warranty/insurance product (insurer buyer + capital), drainfield-locator AR app (feature), homeowner subscription-maintenance club (consumer, low WTP + churn), septage-disposal-site capacity exchange (thin two-sided), soil-percolation-test scheduler (feature), pumper route-optimization (commodity/FSM feature), septic-loan marketplace (Round-3 fintech reject).

---

## Step 2: Competitive Analysis + ⭐ Incumbent Check + ⭐ Moat Gate

### Idea 1 — e-filing middleware
- **Kill**: This is the definition of relocating the moat to the portal. The value terminates in the **county's mandated portal (OnlineRME et al.)**; the founder is a thin pass-through with no compounding asset. And the incumbents already file into these portals (OnlineRME ingests pumper reports directly [VERIFIED]; National Onsite/Summit/ServiceCore integrate reporting). **Moat: FAIL. Density 5/5.**
### Idea 2 — inspector marketplace
- **Kill**: Two-sided cold-start with a tiny supply side (subset of ~7,700 operators), no data flywheel, and time-of-sale inspection demand is intermediated by real-estate agents/home-inspection platforms already. Absorbable feature. **Density 4/5, Moat FAIL.**
### Idea 3 — installer design→submittal tool
- **Kill**: Already served by **ServGround** ("design intake through permit closeout... stamped designs, as-built drawings, inspection reports") [VERIFIED] and installer-side FSM. **Density 4/5, Moat FAIL.**

**All three REJECT at Step 2.**

---

## Step 3–5: N/A — no graduate.

## Summary (cycle 060)

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 3 | 7 |
| Step 2 | 3 | 0 | 3 |
| Step 3–5 | 0 | 0 | 0 |

**Graduates this cycle: 0.**

---

# ⭐ DOMAIN VERDICT — Septic / Onsite-Wastewater (cycles 056–060)

**Result: HONEST ZERO. 0 graduates across 5 cycles. This domain does NOT hold a defensible #2 candidate for a pure-software solo founder.**

### Why the domain fails, tied to the four mandatory gates

1. **Incumbent/OEM gate — FAILED domain-wide.** The trade is already densely served by septic-specific SoRs (**Summit/Ritam, ServiceCore, National Onsite, Pro-Septic, InspectorData, ServGround, SepticMind**) and an AI-native report entrant (**SepticSnap, $99/mo**). "Digitize the paper inspection + as-built + service history" is not a gap — **National Onsite already ships the exact per-property permanent-history-with-component-locations moat the thesis proposed**, and SepticSnap already ships the AI-report wedge cheaply.

2. **Moat gate — FAILED domain-wide, two independent leaks:**
   - **Downstream to the mandated county portal.** Where the regulatory mandate is strongest (the thesis's own demand driver), the compounding as-built + service record is filed into and owned by the **county's portal** — **OnlineRME** is the mandated system of record (Snohomish/Island/Pierce WA), storing as-builts + service history and exposing them to homeowners [VERIFIED]. Same for advanced-system O&M reports and FOG manifests (Truwave/Nexinite).
   - **The base data is PUBLIC.** Septic as-builts/permits are public records held by county/state health departments, increasingly online (OnlineRME, Oregon DEQ, Clackamas, Pierce, "Septic Search") [VERIFIED]. A "proprietary per-property as-built graph" cannot be proprietary when the government already publishes it. This is why the **"septic plant" (cycle 057) is the anti-TitlePlant** — the one moat-class that survived Round 3 inverts here.
   - **Upstream to the equipment OEM** for the recurring ATU slice: telemetry lands in **Orenco VeriComm / RMSYS** clouds (cycle 058). The operator sits in the middle, uniquely accumulating nothing.

3. **SAM gate — FAILED.** ~**7,717 US septic/drain/sewer establishments** (IBISWorld 2026) [VERIFIED]; ~$7B service industry at ~4.5% CAGR [VERIFIED]. At an achievable pure-SaaS ACV of $1–3K/yr, even optimistic penetration yields a **~$10–15M ARR ceiling** — the same countable-buyer-universe red flag that killed HVAC-TAB in Round 2. SAM > $100M is not reachable against 7+ incumbents.

4. **Buyer gate — partially FAILED.** The fragmented private pumper/inspector exists (good), but the *valuable aggregate* record accrues to the **county/city (instant-reject government buyer)**, and the ATU channel is partly **captive to equipment OEMs/franchises**.

### The one honest bright spot (not enough to graduate)
Growth is fine (~4.5%, +3.3% establishment count YoY) and demand is genuinely non-deferrable (property-transfer + permit mandates). The domain is *real business*, just not a *defensible software moat for this founder*: it's already a competitive vertical-SaaS market with thin ACV and a data asset that structurally belongs to the government and the OEMs.

### Confidence
- **VERIFIED**: incumbent product existence + capabilities (vendor sites + search excerpts), OnlineRME mandated-portal status, public-record nature of septic data, IBISWorld establishment count + market size/CAGR, SepticSnap pricing, Orenco VeriComm/RMSYS telemetry ownership, FOG incumbent list.
- **ASSUMED**: exact achievable ACV ($1–3K/yr) and penetration → SAM ceiling (bottom-up estimate; direction is robust even if magnitudes shift).
- **UNVERIFIED**: precise count of certified septic *inspectors* (search engines rate-limited); does not change the verdict, since the buyer universe is already bounded by the ~7,700 establishments and every angle failed the moat gate upstream of SAM.

**Recommendation to the funnel**: Close Domain #2 as a zero. It reproduces Round 3's dominant failure (moat accrues to SoR/portal/OEM) and adds a distinctive septic-specific twist (the government publishes the data). Do not deep-research. Reallocate the deep-research budget to any Round-4 domain whose operator genuinely accumulates data the government does NOT already publish and no OEM control-panel captures.
