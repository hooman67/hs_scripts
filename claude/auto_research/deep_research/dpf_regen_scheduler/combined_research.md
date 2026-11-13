# Deep Research: DPF Regen Scheduling Optimizer

**Idea slug:** `dpf_regen_scheduler`
**Type:** Pure SaaS — analytics layer on existing fleet telematics APIs (Samsara / Geotab / Motive). Zero hardware.
**Origin:** Cycle 029 graduate (feasibility 8/10). This is candidate #2 (Hooman is already building CutLog as #1).
**Research date:** 2026-06-28
**One-line:** A SaaS analytics layer that ingests J1939 engine data from a fleet's existing telematics provider and predicts/schedules diesel-particulate-filter regenerations so trucks regen during planned downtime instead of stranding mid-route.

**VERDICT: NO-GO (CONDITIONAL at best).** A directly-on-point competitor — **Intangles** — already sells "predictive alerts for scheduled DPF regeneration," raised **$30M (Oct 2025, Avataar Venture Partners)**, and several other named players (FleetRabbit, OxMaint, TEXA, Ceramex, TensorPlanet) occupy the niche. The "no one does this" premise from Cycle 029 is **falsified by web research.** Combined with a thin verified-signal feasibility gap (the soot/backpressure PIDs needed for true prediction are not cleanly exposed by the very APIs the idea is parasitic on), this fails the wide-open-market test that the funnel requires.

---

## 1. Product Definition

### Exact problem statement
Diesel particulate filters (DPFs) on 2007+ emissions trucks accumulate soot and must regenerate (burn it off). There are three modes (VERIFIED — Wikipedia "Diesel particulate filter"):
- **Passive regen** — happens naturally at highway load/temperature.
- **Active regen** — ECU injects fuel to raise exhaust temperature when passive is insufficient.
- **Forced / parked regen** — soot reaches a critical threshold; truck must stop, idle at ~1400 RPM 30-45 min, or a tech runs a scan-tool regen. This is the costly disruptive event.

Trucks doing urban/short-haul/low-load duty cycles can't sustain passive regen and slide toward forced regens. A forced regen mid-route = lost driving hours, missed loads, sometimes a tow and a shop visit. (Cost figures of $800-2000/event and a DPF cleaning of ~$300-500 are **ASSUMED** — industry trade-press sources that quantify this, e.g. truckinginfo.com / fleetowner.com / ccjdigital.com, were all blocked by network policy during this research and could not be independently verified.)

**Who has it:** maintenance managers / dispatchers at mid-market diesel fleets (10-200 trucks), especially short-haul / vocational / regional duty cycles where forced regens cluster.

### Product scope for v1 (3 features max)
1. **Regen risk score per truck**, updated daily from telematics data, flagging trucks trending toward a forced regen in the next 2-3 days.
2. **Scheduling recommendation** — "run a parked regen tonight at the yard for trucks 14, 22, 31" so it happens on planned downtime.
3. **Driver/dispatcher notification workflow** (email/SMS/Slack) and a simple fleet dashboard.

**Explicitly NOT in v1:** hardware/dongles, ELD/HOS, GPS tracking, full CMMS work-order management, engine OEM scan-tool control (cannot remotely trigger a regen — liability/OEM-gated), EV/battery monitoring.

### User workflow (day 1)
1. Fleet manager connects their existing Samsara/Geotab/Motive account via OAuth API key.
2. App backfills 30-90 days of engine stats, builds a per-truck duty-cycle/soot baseline.
3. Dashboard shows each truck's regen-risk score; high-risk trucks get a recommended scheduled-regen window.
4. Manager assigns the parked regen to a yard/overnight slot; gets a confirmation the truck cleared.

### Pricing
$25-35/truck/month SaaS (per Cycle 029). A 50-truck fleet = ~$18K/yr. ROI story depends on the **ASSUMED** $800-2000/forced-regen figure — unverified, which weakens the pitch.

### Ideal first customer
Regional/vocational diesel fleet, 30-150 trucks, already on Samsara or Geotab, maintenance manager with budget authority, duty cycle heavy on stop-and-go (refuse, regional LTL, utility, construction support) where forced regens are a known recurring pain.

---

## 2. Competitive Analysis

The Cycle 029 premise — "No dedicated DPF regen prediction/scheduling product exists" — is **FALSE.** Direct, named, in-market competitors found via web research:

### Direct competitors (DPF prediction/monitoring as a product)
- **Intangles** (intangles.ai) — **THE killer.** Sells an explicit **"DPF Monitoring"** product offering *"predictive alerts for scheduled DPF regeneration,"* tracks exhaust back pressure and regen-cycle quality, claims **95% accuracy forecasting component-level failures ~1 month in advance** (InRoute). Raised **$30M led by Avataar Venture Partners, Oct 2025.** Multi-controller edge+cloud ingest. This is precisely the proposed product, funded and shipping. (VERIFIED — intangles.ai/dpf-monitoring + company site.)
- **FleetRabbit** — DPF regen monitoring via OBD2: tracks soot levels, regen cycles, exhaust health in real time. (VERIFIED via search snippet; site itself blocked.)
- **OxMaint (oxmaint.ai)** — AI predictive maintenance explicitly marketing "detect DPF regeneration issues early." (Search snippet; domain blocked.)
- **TensorPlanet** — AI for predictive DPF cleaning intervals / avoiding excessive regen attempts. (Search snippet.)
- **TEXA eTRUCK** — remote DPF regeneration + live truck diagnostics. (Search snippet.)
- **Ceramex North America** — predictive analytics for emissions-system / DPF management. (Search snippet.)

### Indirect / incumbent risk (telematics platforms — the APIs this idea rides on)
- **Samsara** — exposes `faultCodes`, `engineStates`, `defLevelMilliPercent`, `ambientAirTemperatureMilliC`, engine load/oil/coolant via API (VERIFIED — developers.samsara.com getVehicleStatsFeed). Already does fault-code monitoring + alerts. DPF soot-load / exhaust-backpressure PIDs are **NOT** in the published stat list (UNVERIFIED whether obtainable) — a real feasibility hole. Whoever owns the telematics relationship can add a DPF view as a feature at zero CAC.
- **Geotab** — `StatusData` + `FaultData` entities expose engine/J1939 data via SDK (VERIFIED — geotab.github.io). Large add-on Marketplace; no DPF-specific add-on found today (snapshot), but the surface area for one to appear is trivial.
- **Motive** — fault-code alerts + preventative maintenance + OEM telematics integration; no dedicated DPF predictive product surfaced (VERIFIED via gomotive.com equipment-monitoring page).

### OEM connected platforms (entrenched, free-with-truck)
- **Detroit Connect Virtual Technician, Cummins Connected Diagnostics/Guidanz, PACCAR Connect** — OEM aftertreatment/DPF telematics bundled with the truck. Pages blocked by network policy (UNVERIFIED specifics), but these are well-known to deliver aftertreatment fault and regen guidance directly to fleets at no extra cost, covering ~85% of Class 8 powertrains. Strong incumbent moat against an independent layer.

### Open-source / DIY
J1939 PIDs are an open SAE standard; a fleet's data engineer could pull soot-load/backpressure off the bus and threshold it. Low technical barrier for a determined in-house team.

**Competitive density score: 4-5** (established + funded startups in market AND incumbents positioned to add it). Per the funnel's own rubric this is REJECT territory; the Cycle 029 score of "2" was wrong.

**Why a customer picks you over them:** hard to articulate. Cheaper than Intangles? Maybe. OEM-agnostic? So is Intangles. There is no defensible wedge once a $30M-funded incumbent owns the exact phrase "predictive scheduled DPF regeneration."

---

## 3. Feasibility & Prototype

### Core feasibility claims
- **Telematics APIs expose engine diagnostic data** — VERIFIED. Samsara (faultCodes, DEF level, ambient temp, engine states) and Geotab (StatusData/FaultData) both serve J1939-derived engine data via documented APIs.
- **The *specific* DPF predictors (soot mass / DPF differential backpressure / time-since-regen / regen counts) are cleanly available via those APIs** — **UNVERIFIED, and this is the load-bearing gap.** Samsara's published stat list does NOT enumerate soot load or DPF backpressure. Without those PIDs, a "prediction" degrades to inferring soot from duty cycle + DEF + ambient temp — far weaker than Intangles, which ingests multi-controller data directly. The whole differentiation premise ("pure parasitic SaaS on Samsara/Geotab") may not have the inputs it needs.
- **ML time-series prediction of maintenance events is tractable** — ASSUMED/VERIFIED in general; well within Hooman's wheelhouse. The constraint is **labeled training data** (actual forced-regen timestamps per truck), which requires fleet partnerships — a cold-start chicken-and-egg problem.

### Cheap Phase-0 PoC (<$100, <1 week)
1. Get **one** friendly fleet's read-only Samsara or Geotab API key (or use Geotab's free demo `MyGeotab` database / sample data).
2. Python: pull 60-90 days of StatusData/FaultData + DEF + ambient for ~20 trucks. Cost: API free tier + a few dollars of cloud.
3. Check empirically: **are DPF soot-load / backpressure / regen-event PIDs actually present in the returned data?** This single test decides go/no-go on the parasitic-SaaS thesis. (Currently UNVERIFIED — must be resolved before any build.)
4. If present: build a trivial threshold + duty-cycle model, backtest against known forced-regen events, measure lead-time accuracy.

### Risk register
| Risk | Likelihood | Impact | Mitigation | Fallback |
|---|---|---|---|---|
| Intangles (funded) owns the exact product | High | Fatal | None credible | Abandon / pick different idea |
| Needed soot/backpressure PIDs not in API | Med-High | Fatal to thesis | Phase-0 PID audit first | Require own dongle = becomes hardware play, kills the edge |
| Telematics vendor ships it as a feature | Med | Fatal | Move fast, niche duty cycles | None |
| OEM platforms already give fleets this free | High | High | Position as cross-OEM fleet view | Weak |
| Training-data cold start | High | High | Paid pilots for labeled data | Slow, capital-burning |

### Cost & time to prototype
~$5-15K and 6-8 weekend-weeks for a working PoC **if** a partner fleet's API key is available and the PIDs check out. Low capital — the one genuine strength.

---

## 4. Customer Validation Strategy

- **First 5 to approach:** regional/vocational fleet maintenance managers (refuse haulers, regional LTL, utility fleets) already running Samsara/Geotab, 30-150 trucks.
- **Where buyers congregate:** TMC (ATA Technology & Maintenance Council) meetings; r/Truckers and fleet-maintenance LinkedIn groups; Facebook fleet-maintenance/owner-operator groups (per LEARNINGS #14, FB groups are the highest-signal B2B channel); CCJ / FleetOwner / Truckinginfo comment communities.
- **Discovery question (no tell):** "How many forced/parked regens did your fleet eat last quarter, and what did the worst one cost you in downtime?" Then: "Do you find out before or after it strands a truck?" and "Does your Samsara/OEM tool warn you early enough to schedule it?"
- **Demand signal = confirmed:** a maintenance manager who can name the dollar cost AND says their current Samsara/Detroit Connect/Intangles tooling does NOT warn them early enough = a paid pilot LOI. **If they say "Intangles/Detroit Connect already does this," that's the kill signal** — and given the competitive findings, that answer is likely.
- **Note:** Several quantification trade-press sources (truckinginfo, fleetowner, ccjdigital) were network-blocked, so the cost-per-regen demand math remains ASSUMED and must be validated directly with fleets before any build.

---

## 5. Scorecard

| Dimension | Weight | Score (1-10) | Note |
|---|---|---|---|
| Capital required (lower=better) | 15% | 8 | Pure SaaS, ~$5-15K PoC. Genuine strength. |
| Time to first revenue | 15% | 5 | Cold-start training data + enterprise sales drag. |
| Competitive moat | 15% | 2 | Intangles ($30M) + 5 named players + incumbents. No wedge. |
| Technical risk (lower=better) | 10% | 5 | ML easy; but soot/backpressure PID availability UNVERIFIED. |
| Market size (SAM) | 10% | 7 | 500K+ trucks in target fleets; real $100M+ SAM. |
| Founder-market fit | 15% | 8 | Pure software/ML/cloud/API — exactly Hooman's strengths, no hardware. |
| Customer accessibility | 10% | 5 | Fleets reachable but slow, skeptical, OEM-loyal buyers. |
| Scalability | 10% | 8 | Software margins, API-driven, multi-tenant. |

**Weighted total:** 0.15(8)+0.15(5)+0.15(2)+0.10(5)+0.10(7)+0.15(8)+0.10(5)+0.10(8)
= 1.2+0.75+0.30+0.50+0.70+1.20+0.50+0.80 = **5.95 / 10.**

**Verdict: NO-GO.** Founder fit and capital efficiency are excellent and the market is real, but the defining funnel criterion — *no existing product occupying the space* — is violated. A funded, on-point incumbent (Intangles) plus a crowd of named players plus the telematics/OEM platforms that own the data and the customer relationship leave no defensible wedge. The parasitic-SaaS thesis additionally rests on an UNVERIFIED assumption (that Samsara/Geotab expose soot-load/backpressure PIDs) that, if false, removes the very advantage. Recommend not building this as candidate #2.

---

## Sources
- intangles.ai (home) and intangles.ai/dpf-monitoring — DPF product, predictive scheduled regen, $30M Avataar raise Oct 2025, 95% accuracy / ~1-month lead (InRoute). VERIFIED.
- developers.samsara.com getVehicleStatsFeed — faultCodes, defLevelMilliPercent, ambientAirTemperatureMilliC, engineStates exposed; no soot/DPF-backpressure PID listed. VERIFIED.
- geotab.github.io SDK concepts — StatusData / FaultData (J1939 engine data) via API. VERIFIED.
- gomotive.com equipment-monitoring — fault-code alerts + preventative maintenance, no dedicated DPF predictive product. VERIFIED.
- en.wikipedia.org/wiki/Diesel_particulate_filter — passive/active/forced regen mechanics, differential pressure sensing. VERIFIED.
- en.wikipedia.org/wiki/Trucking_industry_in_the_United_States — ~711K trucking businesses, 91.5% run ≤10 trucks, highly fragmented SMB market. VERIFIED.
- FleetRabbit, OxMaint, TensorPlanet, TEXA eTRUCK, Ceramex — DPF monitoring/prediction offerings (search-snippet level; direct sites blocked). PARTIALLY VERIFIED.
- DPF cost-per-event ($800-2000) and cleaning cost figures — trade-press sources (truckinginfo/fleetowner/ccjdigital) network-blocked. ASSUMED / UNVERIFIED.
- Detroit Connect / Cummins / PACCAR aftertreatment telematics — sites blocked; incumbent free-with-truck DPF coverage. UNVERIFIED specifics.
