# Cycle 067 Report

**Date**: 2026-07-09
**Round**: 4, Agent D — Domain #4 Cathodic-Protection / Corrosion Survey (AMPP-mandated)
**Cycle focus**: CP-adjacent **tank inspection & corrosion survey** trades where the mandate hits *tanks* rather than *pipelines* — aboveground storage tanks (API 653), potable water storage tanks (AWWA), and tank-bottom CP. Hypothesis: tank inspection is performed by fragmented private certified inspectors (API 653 / AWWA), which might clear the buyer gate that pipelines fail. Test whether they accumulate their own compounding corrosion time-series and whether the market clears SAM.

**Mandatory gates**: (1) Incumbent/OEM — American Innovations PCS/Bullhorn, MOBILTEX CorView, iFactory + tank-inspection SoRs; (2) Moat accrues to FOUNDER; (3) SAM > $100M; (4) fragmented PRIVATE contractor buyer, not operator/utility.

**Carry-forward from cycle 066**: In the pipeline/utility CP core, American Innovations' PCS Field Data Collector already ships the mandated survey app and the operator owns the data flywheel via PCS. UST-contractor segment passes the buyer gate but fails SAM (~$2–12M) with a thin 3-yr flywheel. This cycle tests the tank-inspection adjacency.

---

## Step 1: Technology Discovery

### 1. API 653 aboveground-storage-tank (AST) inspection app + tank-bottom corrosion history
- **Domain**: AST inspection for API-653 certified inspectors
- **Breakthrough**: API 653 mandates periodic external, internal (bottom), and UT-thickness inspections of ASTs; work is done by fragmented independent API-653 inspectors and tank-service firms. Digitize the inspection report + own the **per-tank bottom-corrosion / shell-thickness time-series**. Corrosion is time-series-rich (UT readings over years) — a better flywheel than UST 3-yr CP. [VERIFIED that API 653 governs in-service AST inspection; corrosion protection of soil-contacting tank bottoms via CP is standard — Wikipedia storage-tank]
- **TRL**: 9
- **Time to product**: 4–6 mo
- **Status**: PROMOTED

### 2. Potable water storage tank CP + coating inspection app (AWWA)
- **Domain**: Municipal/rural water storage tank inspection & CP
- **Breakthrough**: Steel water tanks (elevated, standpipe, ground) get periodic AWWA-guided coating + CP inspections, often by fragmented tank-service/dive-inspection firms. Digitize + own per-tank condition history.
- **TRL**: 9
- **Time to product**: 4–6 mo
- **Status**: PROMOTED (carry to buyer gate — water buyer risk)

### 3. Tank-bottom CP anode-bed life prediction from UT + rectifier trend
- **Domain**: AST CP consumable-life analytics
- **Breakthrough**: Predict tank-bottom corrosion-rate / anode depletion from stacked UT + CP-reading history.
- **TRL**: 6
- **Time to product**: 9 mo
- **Status**: PROMOTED (folds into #1)

### 4. UT thickness reading logger with corrosion-rate trend (tank shell/floor)
- **Domain**: NDT thickness monitoring
- **Breakthrough**: Log UT grid readings across inspections, auto-compute corrosion rate + remaining-life per API 653.
- **TRL**: 8
- **Time to product**: 5 mo
- **Status**: PROMOTED (folds into #1)

### 5. Marine/offshore CP survey app (impressed-current + sacrificial anode hull surveys)
- **Domain**: Ship-hull / offshore-platform CP diver surveys
- **Breakthrough**: Digitize diver/ROV CP potential surveys.
- **TRL**: 7
- **Time to product**: 9 mo
- **Status**: REJECTED
- **Reasoning**: Buyers are large operators (shipowners, offshore majors, classification societies) = enterprise/12–24mo procurement; specialist diver/ROV hard part inverts founder-fit. Fails buyer + founder-fit.

### 6. Rebar/concrete CP monitoring (bridges, parking structures)
- **Domain**: Reinforced-concrete CP
- **Breakthrough**: Half-cell potential mapping + embedded-sensor CP for bridge decks.
- **TRL**: 6
- **Time to product**: 12 mo
- **Status**: REJECTED
- **Reasoning**: Buyer = DOT/municipal/utility (government instant-reject). Sensor/embedded-probe hard part. Fails buyer + founder-fit.

### 7. API 653 report auto-generation + regulatory-package builder
- **Domain**: AST compliance reporting
- **Breakthrough**: Auto-assemble the API 653 inspection report + SPCC package.
- **TRL**: 8
- **Time to product**: 4 mo
- **Status**: PROMOTED (folds into #1 — the report IS the wedge)

### 8. Tank inspection photo/defect-tagging with vision assist
- **Domain**: Visual inspection documentation
- **Breakthrough**: Vision model flags pitting/coating failure from inspection photos.
- **TRL**: 7
- **Time to product**: 6 mo
- **Status**: PROMOTED (folds into #1 as a feature)

### 9. AST corrosion-rate benchmarking network across inspectors
- **Domain**: Cross-account corrosion data network
- **Breakthrough**: Anonymized corrosion-rate benchmarks by product/region/coating — a data-network effect on top of #1's owned data.
- **TRL**: 7
- **Time to product**: 12 mo (needs installed base first)
- **Status**: PROMOTED (this is the moat-deepener; evaluate with #1)

### 10. Dedicated tank-inspection FSM/scheduling
- **Domain**: Field-service management for tank inspectors
- **Breakthrough**: Route + next-due scheduling for API-653 recert cycles.
- **TRL**: 9
- **Time to product**: 4 mo
- **Status**: REJECTED
- **Reasoning**: Horizontal FSM covers it; no unique data flywheel. Absorbable.

---

## Step 2: Competitive Analysis

### API 653 AST inspection platform (idea #1 bundle: +3,4,7,8,9)
- **Competitors found**:
  - **Incumbent tank-integrity software**: There is an established enterprise tier for tank inspection data management — e.g. **Antea, Visions Enterprise (by IDGeniX), TEAM/Inspectioneering-adjacent tools, PCMS, Meridium/GE APM, AVEVA APM** serve refinery/terminal owner-operators' mechanical-integrity programs. These are **owner-operator (refinery/terminal) enterprise SoRs**, priced and sold to large asset owners. [ASSUMED — named from domain knowledge; not re-verified via live search this cycle]
  - **API 653 inspection is also done by large service firms** (TEAM Inc., Acuren, MISTRAS, Tank Industry Consultants) that have their own internal tooling. [ASSUMED]
  - For the SMALL independent API-653 inspector: paper/Word templates + Excel UT grids remain common. [ASSUMED]
- **Competitive density score**: 4/5 for the refinery/terminal owner-operator segment (Meridium/AVEVA/Antea entrenched); 3/5 for the small-independent-inspector segment.
- **Differentiation angle**: Inspector-side (not owner-side APM) app that owns the inspector's **cross-client tank corrosion time-series** and auto-builds the API 653 report. But see moat gate below.
- **Status**: BORDERLINE → moat/buyer test.

### Water storage tank CP + coating inspection (idea #2)
- **Competitors found**: Tank-service firms (Suez/Utility Service Co./SUEZ Water Technologies, Dixon Engineering, KLM/Pittsburg Tank & Tower) bundle inspection with maintenance contracts; municipal asset-management SoRs (Cityworks, Cartegraph) hold the water utility's asset record. [ASSUMED]
- **Competitive density**: 3/5.
- **Status**: → buyer gate (water-utility risk).

---

## Step 3: Market Analysis

### API 653 AST inspection platform
- **Buyer question (gate 4)**: This is the crux. Two possible payers:
  - (a) The **owner-operator** (refinery, terminal, chemical plant, large fuel-storage) — this is who buys mechanical-integrity/APM software today. That buyer is a **large enterprise with 12–24mo procurement** = effectively the instant-reject profile, and the segment is owned by Meridium/AVEVA/Antea. **REJECT on this buyer.**
  - (b) The **independent API-653 inspection contractor** — fragmented, private, pays directly = passes the buyer gate. BUT: many ASTs are inspected by large service firms (TEAM/Acuren/MISTRAS) with in-house tools, so the "small independent inspector" reachable universe is limited.
- **Market sizing (independent-inspector segment, bottom-up, honest)**:
  - Reachable universe of small/independent API-653 inspection firms plausibly **~1,000–3,000 firms** [ASSUMED — no verified count]. At **$2,000–5,000/yr** ACV = **~$2M–$15M SAM**.
  - Owner-operator segment is larger ($100M+) but is the wrong (enterprise) buyer and is occupied.
- **Growth rate**: AST inspection demand stable (aging tank fleet, SPCC enforcement) but not high-growth. [ASSUMED]
- **Status**: **REJECTED**
- **Reasoning**: The buyer splits into "large enterprise, occupied, wrong-profile" (fails buyer + incumbent) OR "small independent inspector, right buyer but ~$2–15M SAM" (fails SAM by ~10×). No slice clears both gates.

### Water storage tank CP + coating inspection
- **Buyer**: The ultimate payer for water-tank inspection is the **water utility / municipality** (they own the tank and contract the inspection). The tank-service contractor is paid by the water utility on utility procurement cycles, and the asset record accrues to the utility's Cityworks/Cartegraph SoR. [ASSUMED]
- **Status**: **REJECTED** — buyer is a municipal water utility (government instant-reject); moat accrues to the utility's municipal asset SoR.

---

## Step 4: Feasibility Analysis

No idea reached Step 4.

**Moat gate verdict (recorded for completeness)**: The API-653 inspector app has the domain's *best* flywheel so far — UT-thickness + corrosion-rate time-series is genuinely dense and compounding (idea #9's cross-inspector benchmarking network is a real network-effect). This is the one place the "own the corrosion time-series" thesis has teeth. **But it dies on the buyer/SAM scissors**: the buyer with money (owner-operator) is enterprise + occupied; the buyer with the right profile (independent inspector) is too few to clear SAM.

---

## Step 5: Execution Summary

**No graduates this cycle.**

- AST/API-653 inspection: best data moat in the domain, killed by the buyer/SAM scissors.
- Water-tank CP: municipal-utility buyer instant-reject + utility-owned SoR.
- Marine/rebar CP: enterprise/government buyers + specialist/sensor founder-fit inversion.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 6 (mostly bundled into #1) | 4 |
| Step 2 | 2 bundles | 2 borderline | — |
| Step 3 | 2 | 0 | 2 (buyer/SAM) |
| Step 4 | 0 | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates this cycle: 0.**

**Honest read**: The tank-inspection adjacency has a *stronger data flywheel* than the pipeline CP core (UT/corrosion-rate time-series compounds far better than a 3-year CP potential), which is encouraging for the archetype in principle. But the corrosion/tank world is structured so the money is with large asset owners (occupied by AVEVA/Meridium/Antea) or government water utilities, and the fragmented private inspector who WOULD be the right buyer is both too few (sub-$15M SAM) and partly displaced by large service firms with in-house tooling. Cycles 068–069 test the smaller-structure, higher-frequency CP-service trades (well-casing / facility / marina & dock CP) to see if any combination clears all four gates.
