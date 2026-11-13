# Deep Research: DryerIQ — AI Grain Dryer Optimization

**Idea slug:** `dryeriq_grain`
**Type:** HW+SW (retrofit sensor/gateway + cloud/edge ML SaaS)
**Researched:** 2026-06-28
**Researcher note:** Founder = Hooman (Adobe EM; AI/ML + cloud infra + software; BS EE; mech-eng friends). Seeking a SECONDARY, largely self-built business; pure software preferred, hardware penalized. Already building CutLog (laser-cutting parameter SaaS) as idea #1.

**VERDICT: NO-GO.** The defining premise from cycle_025 ("no brand-agnostic competitor") is factually false. The exact product proposed — a brand-agnostic retrofit controller that automatically modulates discharge rate on continuous-flow dryers from real-time inlet/outlet moisture sensing — has been sold for ~30 years by **Dryer Master** (DM510), which explicitly works across GSI, Sukup, Brock, Cimbria, Mathews, AGI/NECO, Chief and "more." Multiple other retrofit-controller vendors exist. This is a mature, hardware-heavy, dealer-distributed, seasonal market with an entrenched incumbent — the opposite of the blue ocean the cycle described, and a poor fit for a solo software founder.

---

## 1. Product Definition

### 1.1 Problem statement
Grain (corn, wheat, barley, canola, etc.) is harvested wet (18–25%+ moisture) and must be dried to a safe storage moisture (~13–15%) to prevent spoilage. Drying is the single largest post-harvest energy cost. Two failure modes cost money:
- **Over-drying** — drying below the target moisture. Grain is sold by weight, so every point of moisture removed below target is "shrink" (lost saleable weight) PLUS wasted fuel. Operators over-dry as a safety margin because manual control is coarse and lagging.
- **Energy waste** — running burners hotter/longer than necessary, or at the wrong discharge rate as incoming moisture and weather vary through the day.

The pain is real and well understood by operators (it is a line-item fuel + shrink cost), but it is **NOT invisible** — which the LEARNINGS file flags as the best ROI story ("invisible waste"). Grain operators already see their propane bills and their moisture discounts at the elevator. This weakens the demand wedge.

### 1.2 Proposed v1 scope (as the cycle imagined it)
- Brand-agnostic retrofit kit: sensor bridge + gateway reading inlet/outlet moisture + drying-air temp.
- Cloud/edge ML controller that modulates dryer discharge rate (or burner setpoint) to hit target moisture with minimum energy.
- Dashboard + mobile alerts + remote control. SaaS subscription.

### 1.3 Why this scope is already a commodity
Every element above is shipping today (see Section 2). "AI/ML" is a thin veneer: the underlying control problem (build a per-dryer performance model, predict outlet moisture from inlet moisture + temp + discharge rate, modulate discharge to hold setpoint) is exactly what Dryer Master's DM510 has done with a self-building dryer model for two decades. **VERIFIED** via dryermaster.com product pages.

### 1.4 Pricing reality
No public list pricing; sold through dealers ("call 1-800-265-2757"). Industry-typical DM510-class controller + moisture sensors run on the order of low-five-figures installed (ASSUMED, not verified — pricing is dealer-quoted). A new entrant would have to undercut a depreciated, trusted incumbent on a once-every-15-20-years capital purchase (one customer reported owning a DM510 "almost 20 years" — VERIFIED via dryermaster.com), i.e., an extremely slow replacement cycle.

---

## 2. Competitive Analysis

### 2.1 Direct competitors (brand-agnostic retrofit moisture control) — THE KILLER FINDING

**Dryer Master (DM510 / Moisture Monitor Pro / DM100)** — **VERIFIED, dryermaster.com**
- ~30 years in business ("30 years experience"; customer owning a unit "almost 20 years").
- Self-describes the DM510 as "the industry leading drying control system for continuous flow grain dryers."
- Measures inlet + outlet moisture and drying-air temperature; **automatically** adjusts discharge rate; "builds a performance model" of each specific dryer (this IS the ML/adaptive-control claim).
- **Explicitly brand-agnostic:** "The DM510 can be used on almost all continuous flow grain dryers" — screen, mixed-flow, farm, tower, profile. Formal OEM embeds with Mathews Company, AGI/NECO, Chief Agri (Caldwell), Grain Handler, Kentra, Superior, Millennium. Customers have retrofitted it onto **GSI, Zimmerman, Sukup, Brock, Cimbria, Shanzer, Delux, Vertec, Mega, Keppler Weber, Meyer, Perry "and more."**
- Remote access/mobile via DM Mobile.
- **This is verbatim the product the cycle claimed did not exist, targeting verbatim the same dryer brands the cycle proposed targeting (GSI, Sukup, Brock).**

The cycle_025 report's central differentiation — "No pure-software, brand-agnostic AI dryer optimization product exists for the massive retrofit market" — is **FALSE (VERIFIED)**.

### 2.2 Other retrofit / aftermarket dryer-control vendors (fragmented but present) — **VERIFIED via search**
- **CZAR Controls** — automated retrofit systems upgrading existing dryers with new moisture controls, smartphone/tablet access, text alerts.
- **Dry Max Solutions** — moisture control that analyzes content and auto-adjusts energy/airflow for efficiency or throughput.
- **Horner Automation (XL7 grain dryer control)** — control system addressing inefficiencies of traditional control.
- **Custom Agri Systems (Platinum+ Controller)** — drying-process management upgrades.
- **Red Board Systems** — retrofit kits for remote internet viewing/control.
- **AI Grain Solutions** — retrofittable systems automating fan control and optimizing moisture (storage/aeration-leaning).

Competitive density here is realistically **4 ("established startups/vendors with products in market")**, not the "2" the cycle assigned.

### 2.3 Hardware-bundled OEM controls (the dryers themselves are getting smart)
- **Tornum IDC (Intelligent Dryer Control)** — software control for continuous-flow dryers; monitors in/out moisture, controls speed to hold moisture; PC/tablet. (AI-enhanced positioning claimed at LAMMA 2025 in the cycle note; I could NOT independently verify the "AI" launch claim via web search — **UNVERIFIED**. The base IDC moisture-control product is **VERIFIED** via tornum.com / AgriExpo listing.)
- **GSI (AGCO), Sukup, Brock (CTB/Berkshire Hathaway), Mathews, AGI** — every major OEM ships PLC/touchscreen moisture-control automation on new dryers, increasingly with cloud/remote (GSI WatchDog, etc.). New-dryer buyers get this built in, shrinking the retrofit TAM over time.

### 2.4 Indirect / manual alternatives
- Manual operation by an experienced operator watching a discharge moisture meter — the default, and "good enough" for many.
- Standalone moisture meters (DICKEY-john, Perten) + manual discharge tweaks.
- Over-drying as a deliberate safety margin (the behavior we'd be trying to displace) is cheap insurance against spoilage/discount and is psychologically sticky.

### 2.5 Big-tech / incumbent risk
- Low FAANG risk (too niche), BUT high **agricultural-incumbent** risk: AGCO/GSI, CTB/Brock, AGI, Sukup, Bühler, Cimbria all own the dryer hardware, the dealer channel, the firmware, and the customer relationship. They can (and do) bundle "smart" control for free with new equipment. A third-party SaaS layer is structurally squeezed between them and Dryer Master.
- Per LEARNINGS #9 (entrenched industrial firms) and #13 (avoid markets with entrenched OEM lock-in), this is a red-flag configuration.

### 2.6 Competitive verdict
**Crowded and entrenched.** One ~30-year brand-agnostic incumbent doing the exact proposed product, a half-dozen retrofit-controller vendors, plus every dryer OEM building it in. Density ≈ 4–5. The cycle's "blue ocean" was a research error.

---

## 3. Feasibility & Prototype

### 3.1 Technical feasibility
- The control algorithm is **VERIFIED feasible and not novel** — it's classic adaptive/model-predictive control of a thermal process; Dryer Master has shipped it for ~20 years. ML adds marginal lift at best. No defensible technical moat for a software founder.
- **Hardest unsolved problem is NOT software — it's hardware + integration + field deployment:**
  - Real-time in-line grain moisture sensing is the crux. Reliable capacitance/NIR moisture sensors that survive grain flow, dust, and temperature swings are non-trivial; this is a core part of incumbents' IP and calibration libraries (per-grain, per-variety, temperature-compensated). **UNVERIFIED that a commodity sensor matches incumbent accuracy** — this is the make-or-break gap and it is a hardware/instrumentation problem, the founder's weakest area.
  - Actuation: physically interfacing to dozens of different dryer control architectures (relay logic, 4–20 mA, Modbus, proprietary OEM PLCs) to modulate discharge/burner — bespoke integration per brand, in the field, by traveling technicians.
- This is a **HW+SW + field-services** business, not a software business. It violates LEARNINGS #1/#6 (pure software / "software on hardware the customer already controls via an open API"). There is no clean public API; you must add sensors and tap into control wiring.

### 3.2 Cheap Phase-0 PoC path (<$100? — NO)
A meaningful PoC cannot be done for <$100/<1 week like a pure-software idea:
- **Software-only sandbox (cheap, ~$0–50, 1 week):** Build a dryer simulation / fit an ML controller against a public continuous-flow drying dataset or a physics model (thin-layer drying equations are published). Demonstrates the algorithm — but proves nothing the incumbent hasn't, and proves nothing about the real bottleneck (sensing + actuation).
- **Real PoC (realistic, $3–10K, requires a cooperating farm + harvest season):** Commodity moisture sensor(s) (e.g., capacitance grain-moisture probe, a few hundred USD each), an edge gateway (Raspberry Pi / industrial PLC), wiring into one real dryer, validated over a harvest window. **Seasonally gated: you can only test during fall harvest** — a multi-month calendar lock that makes iteration glacial. **UNVERIFIED / ASSUMED costs.**

### 3.3 Capital & time
- To reach paying pilots: the cycle's own estimate was **$250–400K**, well above CutLog-class capital and above the "low-capital wins" bar (LEARNINGS #2). Realistically higher once you account for per-brand integration engineering, sensor calibration, field installs, and harvest-season-gated validation.
- Time-to-revenue is throttled by the **annual harvest cycle** (one real selling/validation window per year) and by dealer-channel sales — slow.

### 3.4 Risk register (top items)
| Risk | Likelihood | Impact | Mitigation | Verdict |
|---|---|---|---|---|
| Entrenched incumbent (Dryer Master) already owns the exact niche | **Certain (VERIFIED)** | Fatal | None credible for a solo founder | Kills the thesis |
| Moisture-sensing accuracy ≠ incumbent calibration | High | Fatal (bad data → bad control → spoilage liability) | License/buy sensors; deep calibration work (hardware-heavy) | Founder-mismatch |
| Per-brand control integration sprawl | High | High cost/time | Limit to 1–2 brands first | Slow, services-heavy |
| Seasonal validation (1 window/yr) | Certain | High | Multi-region/hemisphere testing | Slows everything |
| OEMs bundle smart control for free | High | Erodes TAM | None | Structural |
| Liability if mis-control spoils a bin/over-dries | Med | High | Insurance, conservative defaults | Adds cost/caution |

---

## 4. Customer Validation Strategy (if one ignored the above and proceeded)

- **Where buyers congregate:** AgTalk / NewAgTalk forums, r/farming and grain-specific subreddits, Facebook grain-farming and grain-handling groups (LEARNINGS #14: FB groups = highest-signal B2B channel), commodity-elevator and feed-mill associations (GEAPS — Grain Elevator and Processing Society), farm shows (Farm Progress Show, National Farm Machinery Show, LAMMA in UK).
- **First-5 customer profile:** independent grain elevators and 2,000–10,000-acre row-crop operations running an older continuous-flow dryer WITHOUT an existing automatic moisture controller (the shrinking set that Dryer Master/OEMs haven't already captured).
- **Discovery questions (don't reveal hand):** "How do you decide discharge rate during harvest — by feel or by meter?" / "How much do you over-dry as a safety margin, and what does a point of shrink cost you?" / "Have you looked at Dryer Master or your OEM's auto-control? Why / why not?"
- **Demand signal = confirmed:** the answer to the Dryer Master question is the whole ballgame. If prospects say "we already run Dryer Master / our GSI does it," demand for a new entrant is dead. A real signal would be a pre-paid pilot deposit before next harvest — but the seasonal gate means you learn this only once a year.

---

## 5. Scorecard

| Dimension | Weight | Score (1-10) | Notes |
|---|---|---|---|
| Capital required (lower=better) | 15% | 3 | $250–400K+; hardware, sensors, field installs, per-brand integration |
| Time to first revenue | 15% | 3 | Annual harvest gate + dealer-channel sales |
| Competitive moat | 15% | 2 | Algorithm not novel; incumbents own sensing IP, channel, hardware |
| Technical risk (higher=lower risk) | 10% | 4 | Software is easy; moisture sensing + control integration is the hard, hardware-heavy part |
| Market size (SAM) | 10% | 6 | Real >$100M, but shrinking as OEMs bundle and Dryer Master holds the retrofit niche |
| Founder fit | 15% | 2 | HW + instrumentation + field services + seasonal ag sales = wrong shape for a solo AI/SW founder |
| Customer accessibility | 10% | 5 | Farmers reachable via forums/FB/shows, but conservative, dealer-mediated, seasonal |
| Scalability beyond prototype | 10% | 3 | Per-brand integration + per-site install caps scaling; not pure-software leverage |

**Weighted total:** (3×.15)+(3×.15)+(2×.15)+(4×.10)+(6×.10)+(2×.15)+(5×.10)+(3×.10)
= 0.45+0.45+0.30+0.40+0.60+0.30+0.50+0.30 = **3.3 / 10**

**VERDICT: NO-GO.**

### Why NO-GO (summary)
1. **The founding premise is false (VERIFIED).** Dryer Master has sold brand-agnostic retrofit moisture-control automation across all the target dryer brands for ~30 years; CZAR, Dry Max, Horner, Custom Agri, Red Board, plus Tornum and every OEM, fill the rest.
2. **Wrong business shape for this founder.** It's hardware + instrumentation + field integration + seasonal ag sales — the opposite of the pure-software, low-capital, fast-iteration profile that suits Hooman (LEARNINGS #1, #2, #6).
3. **No moat.** The "AI" is cosmetic over a 20-year-old solved control problem; the real IP (moisture sensing/calibration) sits with incumbents.
4. **Slow everything.** One validation window per year; once-in-15-20-years replacement cycle; dealer channel.

### Known false assumptions from cycle_025 (corrected here)
- "No brand-agnostic AI dryer optimization product exists" → **FALSE.** Dryer Master DM510 (VERIFIED).
- "Competitive density = 2" → realistically **4–5** (VERIFIED multiple vendors + OEMs).
- "Tornum is the only player and only on its own hardware" → **FALSE.** Brand-agnostic retrofit is exactly Dryer Master's category.

## Sources
- Dryer Master product/company pages (VERIFIED): https://www.dryermaster.com , .../Dryer-Master-510-Controller.htm , .../Dryer-Manufacturers.htm , .../Dryer-Master-Application-Examples.htm
- Tornum IDC (VERIFIED base product; AI claim UNVERIFIED): https://www.tornum.com/en/
- Competitor list via web search (VERIFIED existence): CZAR Controls, Dry Max Solutions, Horner Automation XL7, Custom Agri Systems Platinum+, Red Board Systems, AI Grain Solutions.
- Grain-drying energy economics (over-drying shrink + propane cost) — directional/ASSUMED; specific per-bushel figures not retrieved (extension sources were network-blocked during research).
