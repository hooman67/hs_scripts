# Deep Research: DoseRight — AI Chemical Dosing Optimization for Small Municipal Wastewater

**Idea slug:** `doseright_wwtp`
**Type:** Pure SaaS (software on existing SCADA; no hardware)
**Date:** 2026-06-28
**Researcher:** Step-6 deep-research pass (Claude)
**One-line:** Self-serve SaaS that reads a small wastewater plant's existing SCADA data and recommends optimal coagulant/polymer/disinfectant dosing to cut chemical spend 10-20%.

> **Headline verdict: NO-GO (borderline CONDITIONAL).** The product is technically buildable and the ROI story is real, but the buyer is a municipal/government utility — the single worst buyer profile in our LEARNINGS (12-24 month procurement, risk-averse, no budget authority at the plant level). On top of that, the exact value proposition (no-hardware AI chemical-dosing optimization for utilities) is **already sold by a funded incumbent (Aquasight, 120+ utilities) and surrounded by giants** (Veolia Hubgrade, SUEZ AquaDvanced/Xylem-Idrica). This violates two hard rules at once: instant-reject buyer + competitive density ≥4. See Scorecard.

---

## 1. Product Definition

### Exact problem statement
Small municipal wastewater treatment plants (WWTPs) dose chemicals — coagulants (alum, ferric chloride), polymers (flocculant aids), and disinfectants (chlorine/sodium hypochlorite) — to remove solids, precipitate phosphorus, and disinfect effluent ([Wikipedia: Sewage treatment](https://en.wikipedia.org/wiki/Sewage_treatment), VERIFIED). Today, dosing at small plants is set largely by **operator intuition + periodic jar tests**, with conservative over-dosing as the default to stay safely inside permit limits. Chemicals are a top-2 operating cost (after energy). Over-dosing wastes money and can itself cause permit excursions (e.g., excess residual chlorine).

The pain is **real but low-urgency**: a small plant's annual chemical bill is $50K-$400K, so a 15% saving is $8K-$60K/yr. That is meaningful to a utility but not a "hair-on-fire" emergency — it competes with every other capital and staffing priority.

### Product scope for v1 (3 features max)
1. **SCADA read-only connector** — pull historical + live flow, turbidity, pH, TSS, ORP, chemical pump rates from the plant's existing SCADA/historian via Modbus/DNP3/OPC-UA or CSV export.
2. **Dosing recommendation engine** — per-plant ML model (transfer-learned from a base physico-chemical model) that outputs a recommended dose setpoint and a confidence band, with a human-in-the-loop "advisory only" mode (operator still sets the pump).
3. **Savings + compliance dashboard** — show $ saved vs. baseline dosing, and a clean log for the monthly Discharge Monitoring Report (DMR).

### What it explicitly does NOT do (v1)
- Does NOT close the loop / auto-actuate pumps (liability + approval nightmare — advisory only).
- Does NOT sell or install any hardware/sensors.
- Does NOT do drinking-water (regulatory tier above wastewater; different permit regime).
- Does NOT do membrane fouling, energy/aeration optimization, or asset management (those are separate platforms — and where incumbents already are).

### User workflow (day 1)
1. Operator/superintendent connects the connector to the plant historian (or uploads 6-12 months of CSV logs).
2. Tool ingests history, fits a baseline dosing model, shows "you currently average X mg/L alum; model suggests Y; estimated saving $Z/mo."
3. Operator runs in shadow/advisory mode for 30-60 days, manually applying suggestions during a day shift, watching effluent quality.
4. Dashboard accrues realized savings; superintendent uses it to justify the subscription to the city.

### Pricing model
$500-$1,500/mo per plant ($6K-$18K/yr), self-serve, no CapEx. Justification: 15% of a $50K-$400K chemical bill = $7.5K-$60K/yr saved, so even the top tier is <30% of savings. (ASSUMED pricing — no comparable self-serve small-plant SaaS exists publicly to benchmark against; incumbents quote custom enterprise pricing.)

### Ideal first customer profile
A 0.3-1.0 MGD activated-sludge plant serving 3,000-10,000 people, with: (a) a modern-enough SCADA/historian (not a paper logbook), (b) a tech-curious superintendent with informal authority to trial a sub-$2K/mo tool without a council vote, (c) chemical spend high enough that 15% is visible. This is a **narrow** intersection.

---

## 2. Competitive Analysis

### (a) Direct competitors — the killer
- **Aquasight** ([aquasight.io](https://www.aquasight.io/), VERIFIED) — AI SaaS for water/wastewater utilities. Its **APOLLO** product explicitly does *treatment optimization "driving energy and chemical savings, recommending optimal settings."* Claims **120+ utilities** (Seattle Public Utilities, Charlotte Water, Boston Water & Sewer), **no hardware required**, results "in weeks," and **10-20% cost savings** — i.e., the *exact* pitch and *exact* savings number this idea claims. This is a direct, funded, named competitor that has already shipped DoseRight's value prop. (VERIFIED from their site.)
- **The Turing Company / Transcend-adjacent water-AI** — prior cycle notes ~$14M raised targeting larger utilities (UNVERIFIED this pass — their `.com` no longer resolves, suggesting a rename/pivot/acquisition; either way the IP and team exist in the space).
- **EMAGIN** (emagin.ai) — AI autonomous control for water/wastewater (HARMONY platform); site unreachable from this environment (network-blocked), but widely documented as a treatment-optimization AI vendor (ASSUMED from prior knowledge; could not re-verify this pass).

### (b) Indirect / manual alternatives
- **Jar testing + operator experience** — the dominant incumbent "technology." Free, trusted, and the regulatory record of choice. Hard to displace culturally.
- **Chemical suppliers' own service** — companies like USALCO, Kemira, Solenis already send reps who help dial in dosing as part of selling the chemical. The supplier has *negative* incentive to cut chemical usage but *every* incentive to control the dosing relationship.
- **Engineering consultants** (Brown & Caldwell, Jacobs, HDR) do dosing studies as paid engagements.

### (c) Big-tech / incumbent risk — high
- **Veolia (Hubgrade)** — Veolia is the world's largest private water operator (110M drinking-water users, 97M sanitation, 215K employees; [Wikipedia: Veolia](https://en.wikipedia.org/wiki/Veolia), VERIFIED). Hubgrade is their digital monitoring/optimization layer and they *operate municipal plants directly*, including in the US.
- **SUEZ — AquaDvanced** suite does treatment/network optimization (ASSUMED, widely documented).
- **Xylem** — $8.6B revenue, 23K employees ([Wikipedia: Xylem](https://en.wikipedia.org/wiki/Xylem_Inc.), VERIFIED); owns **Idrica/GoAigua** and **Innovyze** (now sold to Autodesk) digital-water assets and **Evoqua** ($7.5B acq., 2023) treatment chemicals/services. Xylem can bundle dosing analytics into existing utility relationships at effectively zero marginal CAC.
- **The European industrial-QC firms** from LEARNINGS (SIKORA, Precitec, Cognex, Keyence, etc.) are **NOT** relevant here — this is process chemistry, not optical inspection. (One genuine positive: this niche is outside their wheelhouse.)

### (d) Open source / DIY
SCADA historians already trend dosing vs. effluent; a competent operator + a spreadsheet (or a $0 PID-loop on the dosing pump tied to a turbidity probe) captures much of the easy savings. The marginal lift of ML over a well-tuned feed-forward/PID control is real but modest and hard to prove to a skeptical operator.

### Competitive density score: **4-5 / 5 (REJECT range)**
At least one funded direct competitor (Aquasight) with the identical "no-hardware, 10-20% chemical savings" pitch and 120+ live utilities, plus 2-3 more startups and 3 global incumbents who operate the plants themselves. The supposed "small-plant gap" is real *only* because small plants are the **least profitable, slowest-to-close** segment — which is a reason incumbents ignore it, but also the reason it may be a bad business, not a hidden gold mine (LEARNINGS #10: empty micro-niches are often empty for a reason).

---

## 3. Feasibility & Prototype

### Technical feasibility — genuinely high (this is the idea's one real strength)
- **SCADA access is standardized.** Modbus (open, Schneider), DNP3, IEC 60870, and OPC-UA are recognized by all major SCADA vendors ([Wikipedia: SCADA](https://en.wikipedia.org/wiki/SCADA), VERIFIED). Mature Python libraries exist (`pymodbus`, `opcua-asyncio`, `dnp3`/`pydnp3`). **BUT** small/rural plants frequently run **RTUs with radio/GSM/satellite links and old or no historian** (VERIFIED that small sites use RTU+radio; ASSUMED that data quality/access is poor in practice). Real-world integration friction per plant is the hidden cost.
- **Dosing models are well-established** — coagulation/flocculation dose-response is decades of published water-chemistry; ML on plant history is straightforward regression/time-series. Tech risk of the *core algorithm* is low.
- **No hardware, no firmware, no manufacturing** — pure software. This is the best possible fit for a software/ML founder (LEARNINGS #1, #6).

### Hardest unsolved problem
Not the ML — it's **(1) getting clean, labeled data out of heterogeneous small-plant SCADA, and (2) earning operator trust to act on advisory output** in a permit-liability environment where over/under-dosing can trigger a violation. Neither is a research problem; both are grinding integration + sales/trust problems that don't scale cheaply.

### Cheap Phase-0 PoC (<$100, <1 week) — VERIFIED feasible
1. Pull a **public WWTP operating dataset** (many state DMR datasets and EPA ECHO/CWNS data are public; academic coagulation-dosing datasets exist on Kaggle/UCI). Cost: $0.
2. Train a baseline gradient-boosted/regression dosing model in Python (`scikit-learn`/`xgboost`); back-test: does "model dose" hold effluent quality while reducing chemical mass vs. recorded dosing? Cost: laptop.
3. Build a one-screen Streamlit dashboard showing $ saved. Host free.
4. **Validation bar:** model reproduces ≥10% chemical reduction on held-out historical periods without effluent-quality degradation. If it can't beat the operator's historical baseline on paper, stop.
Total: <$100, ~1 weekend.

### Phase-1 (real plant): the cost is access, not code
A single friendly plant + 6-12 months of their SCADA export is worth more than any further coding. Expect 1-3 months of relationship-building per plant.

### Risk register
| Risk | Likelihood | Impact | Mitigation | Fallback |
|---|---|---|---|---|
| Municipal sales cycle 12-24 mo (LEARNINGS instant-reject) | **High** | Fatal to a *secondary/nights-weekends* business | Sell to private contract operators (Veolia/Woodard&Curran-operated plants) instead of cities | None viable for solo part-timer |
| Aquasight/incumbent already owns the pitch | **High** | Severe (no differentiation) | Go ultra-low-end self-serve <$1K/mo | Incumbents can drop price for any deal they care about |
| Permit-liability fear blocks "act on advice" | Med | High | Advisory-only, shadow mode | Becomes a reporting tool, not optimization |
| Small-plant SCADA data too poor/old | Med-High | High | Pre-qualify plants with historians | Manual CSV upload (kills self-serve) |
| Chemical suppliers defend the relationship | Med | Med | Partner with a supplier (channel) | — |

### Confidence summary
- SCADA protocols standardized: **VERIFIED**
- Dosing ML is low-research-risk: **VERIFIED** (established literature)
- Aquasight sells the identical value prop to 120+ utilities: **VERIFIED**
- Small plants are underserved/manual: **ASSUMED** (EPA confirms small/rural systems get technical-assistance funding and 4,500+ lagoon systems exist — [EPA small/rural wastewater](https://www.epa.gov/small-and-rural-wastewater-systems), VERIFIED — but EPA funds *consultants/operators*, not software, which signals the buyer expects help to be *grant-funded*, not a SaaS line item).
- $500-1,500/mo self-serve will close: **UNVERIFIED** (no public small-plant SaaS comp; municipal self-serve purchasing is itself doubtful).

---

## 4. Customer Validation Strategy

### Where buyers congregate
- **State Rural Water Associations** + **National Rural Water Association (NRWA)** conferences/training — the real watering hole for small-plant operators.
- **Water Environment Federation (WEF)** and state WEF member associations (WEFTEC trade show).
- **Operator certification courses** and state-run "circuit rider" technical-assistance programs.
- Operator forums / Facebook groups for water operators (LEARNINGS #14: FB groups are high-signal for trade operators — worth checking if an equivalent exists here; likely smaller/quieter than CNC/laser communities).

### First 5 to approach (profiles, not committing to names)
1. A privately-operated municipal plant cluster (Veolia/Woodard & Curran/Inframark contract ops) — private operator = faster decision than a city.
2. A tech-forward small-city public works director who already bought SCADA upgrades.
3. A state Rural Water Association technical-assistance lead (channel, not buyer).
4. A regional chemical supplier rep (channel/partner).
5. An academic/extension water program running operator training.

### Discovery questions (don't reveal the build)
- "Walk me through how you decide your alum/polymer dose each shift — what changes it?"
- "What's your monthly chemical spend, and has anyone ever asked you to cut it?"
- "When the city wants to fund something here, how does that purchase actually happen — your call or a council vote?"  ← *the real qualifier*
- "Do you have a historian, and could you pull last year's flow + dosing + effluent to a CSV today?"

### Signal = confirmed demand
- A superintendent who can name their chemical bill, expresses cost pressure, AND says "I could trial a sub-$X tool myself without a council vote." (If the answer is "that needs to go to procurement/council," that is a **demand red flag**, not a sale.)
- A private contract operator signing a paid 60-day pilot across multiple plants.

### Honest demand read
The economic ROI exists; the **purchasing path does not** for a part-time solo founder. Government/utility buyers are a named instant-reject in our own LEARNINGS for exactly this reason.

---

## 5. Scorecard

| Dimension | Weight | Score (1-10) | Rationale |
|---|---|---|---|
| Capital required (lower=better) | 15% | **9** | Pure software, ~$50-250K to MVP; Phase-0 PoC <$100. Best-in-class. |
| Time to first revenue | 15% | **3** | Municipal/utility sales 12-24 mo; pilots-before-pay; no impulse buy. |
| Competitive moat | 15% | **3** | Dosing ML is commoditized; incumbents (Aquasight + Veolia/SUEZ/Xylem) own relationships; weak data flywheel for a solo. |
| Technical risk (lower=better) | 10% | **7** | Core ML/SCADA low-risk; real risk is messy small-plant data, not algorithms. |
| Market size (SAM) | 10% | **5** | ~16K POTWs but small-plant SAM realistically ~$100-140M and slow-converting; biggest spenders already served by incumbents. |
| Founder-market fit | 15% | **6** | Excellent on tech (pure SaaS/ML = Hooman's sweet spot) but poor on the **GTM**: municipal sales is the antithesis of a nights/weekends solo motion. Net middling. |
| Customer accessibility | 10% | **2** | Government/utility buyers, council/procurement gates, conservative permit-liability culture. Worst buyer profile in our playbook. |
| Scalability beyond prototype | 10% | **4** | Each plant needs bespoke SCADA integration + trust-building; self-serve thesis likely breaks; scaling = headcount, not code. |

**Weighted total:** (9×.15)+(3×.15)+(3×.15)+(7×.10)+(5×.10)+(6×.15)+(2×.10)+(4×.10)
= 1.35+0.45+0.45+0.70+0.50+0.90+0.20+0.40 = **4.95 / 10**

### Verdict: **NO-GO**
Two independent hard-rule violations: (1) **government/utility buyer** = LEARNINGS instant-reject (12-24 mo procurement, no plant-level budget authority); (2) **competitive density ≥4** with a funded incumbent (Aquasight, 120+ utilities) already shipping the *identical* "no-hardware, 10-20% chemical savings" pitch, plus three global incumbents (Veolia/SUEZ/Xylem) who operate the plants. The only genuinely strong attribute — pure-software founder fit and tiny capital — cannot overcome a buyer Hooman structurally cannot reach part-time and a market the giants already cover at the top and ignore at the bottom *for good reason*.

### Interesting facts uncovered
- Aquasight's APOLLO advertises the **exact** "10-20% chemical/energy savings, no hardware, weeks not months" claim this idea was built on — the differentiation thesis is already someone else's marketing copy.
- EPA funds small/rural wastewater via **technical-assistance grants to consultants and operators** ($25.5M + $41M tranches), not software licenses — signaling the segment expects help to arrive as grant-funded service, not a SaaS subscription.
- Veolia alone serves 97M sanitation users and *operates* municipal plants directly — an incumbent that is simultaneously the buyer, the operator, and a potential competitor.
- SCADA is genuinely standardized (Modbus/DNP3/OPC-UA), but small/rural plants lean on RTU+radio/GSM with weak historians — the data, not the protocol, is the bottleneck.
