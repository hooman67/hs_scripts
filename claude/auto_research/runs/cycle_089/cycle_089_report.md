# Cycle 089 Report — Final synthesis probe: is there ANY defensible #2 in propane/LPG mandated inspection?

**Date**: 2026-07-09
**Domain (Round-4 map #9, final cycle)**: Cycles 086–088 killed the three obvious framings
(on-delivery gas check, DOT cylinder, cargo-tank/fuel-oil). This last cycle deliberately hunts the
**non-obvious** shapes — data-aggregation "plants," parasitic layers, and buyer-substitution plays —
to make sure the domain isn't hiding a CutLog/TitlePlant-class winner behind the incumbent wall.
Then it renders the domain verdict.

**Gates** (all four applied): incumbent/OEM, moat-accrues-to-founder, SAM>$100M, fragmented-private buyer.

---

## Step 1: Technology Discovery (10 non-obvious candidates)

### 1. Cross-dealer propane "system-history plant" (aggregate the per-tank data across dealers)
- **Thesis**: A TitlePlant analog — aggregate anonymized per-tank/per-appliance histories across
  many dealers into a data asset (e.g. failure rates by regulator model, tank corrosion by region).
- **TRL**: 8
- **Status**: **REJECTED (Step 1)** — the source data **already sits in P3 and Tank Spotter's
  clouds** (they hold 700+ and 100+ dealers' inspection histories). Whoever aggregates the plant
  is *them*, not a new founder who has zero dealers. The plant requires owning the SoR first — and
  the SoR is taken. Moat gate fail at the root.

### 2. Insurance-facing propane risk-scoring API (sell compliance signal to LPG insurers)
- **Thesis**: Score a dealer's/site's compliance posture; sell to insurers underwriting propane risk.
- **TRL**: 7
- **Status**: **REJECTED (Step 1)** — the compliance signal originates in P3 (whose entire pitch is
  "reduce documentation error 30%→5%" *for the insurer/liability audience*); P3 is one product step
  from selling this. Also insurer buyer = long enterprise sales. Data + relationship both accrue to
  incumbent.

### 3. LPG appliance-service marketplace (connect homeowners to certified service techs)
- **TRL**: 8
- **Status**: **REJECTED (Step 1)** — two-sided local-services marketplace; brutal cold-start,
  no proprietary data, dealers own the customer relationship; classic no-moat marketplace.

### 4. Parasitic analytics on tank-telemetry APIs (Otodata/Tank Utility/Anova)
- **Thesis**: Layer route/consumption/compliance analytics on the tank-monitor OEM feeds.
- **TRL**: 8
- **Status**: **REJECTED (Step 1)** — the round-3 parasitic-SaaS pattern, and it dies the round-3
  way: **the telemetry OEMs (Otodata Nee-Vo, Tank Utility, Anova/Wesroc) ship their own FREE apps +
  portals + routing software** [Brave — VERIFIED], own the data feed, and cap the layer at ~$0.
  Moat accrues to the device OEM.

### 5. Compliance-as-training: NFPA-58 CETP micro-credential + tracking
- **TRL**: 9
- **Status**: **REJECTED (Step 1)** — NPGA/PERC own **CETP** (the industry certification), and Tank
  Spotter already bundles ~500 training videos. Credential network pre-owned (round-3 edtech lesson).
### 6. State-portal e-filing middleware for propane compliance
- **TRL**: 8
- **Status**: **REJECTED (Step 1)** — moat → the state portal / AHJ; regulator-adjacent; the
  round-4 "mandated portal relocates the moat" trap. Buyer/moat fail.
### 7. LLM "NFPA-58 code assistant" subscription
- **Status**: **REJECTED (Step 1)** — advisory, no flywheel, cloneable, liability. (Same as
  cycle 086 #10.)
### 8. Propane leak-detection consumer IoT (home methane/propane sensor + app)
- **Status**: **REJECTED (Step 1)** — consumer hardware; OEMs (First Alert, telemetry cos.) + a
  crowded smart-home category; instant-reject class (consumer hardware).
### 9. Bulk-plant (dealer storage facility) NFPA-58 self-inspection SoR
- **Status**: **REJECTED (Step 1)** — Tank Spotter explicitly does "plant inspections"; P3 covers
  it. Direct incumbent.
### 10. M&A due-diligence data room for propane dealer roll-ups (compliance-history valuation)
- **Thesis**: The consolidating MLPs buying independents need to value the acquired book's
  compliance liability; sell a diligence/valuation tool.
- **TRL**: 7
- **Status**: PROMOTED (to test) — the ONE genuinely novel buyer (acquirer, not operator); carry it.

**Step 1 result: 1 promoted (#10), 9 rejected.**

---

## Step 2: Competitive Analysis (candidate #10 — propane roll-up diligence tool)

- **Incumbent check**: the compliance-history data the diligence tool would read **lives in P3 /
  Tank Spotter / the target's ERP** — the acquirer just gets a P3 export. No independent data
  source to own.
- **Buyer**: the acquirers are the **big MLPs + PE roll-ups** (AmeriGas, Ferrellgas, Suburban,
  Superior Plus, and a handful of PE platforms) — a **concentrated, ~dozen-buyer** market doing
  episodic deals. Fails Gate 4 (fragmented private operator) — this is nearly the opposite: a tiny
  set of large episodic buyers.
- **Density**: general M&A VDR tools (Datasite, Intralinks) + accounting diligence firms already
  serve energy roll-ups; a propane-specific compliance overlay is a thin feature.
- **Status**: **REJECTED (Step 2)** — concentrated episodic buyer + no ownable data + horizontal
  VDR incumbents. Density 4.

**Step 2 result: 0 promoted.**

---

## Step 3 / 4 / 5

No candidate survived Step 2. **Zero market sizings, zero feasibility, zero execution plans.**

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 1 | 9 |
| Step 2 | 1 | 0 | 1 |
| Step 3 | 0 | 0 | — |
| Step 4 | 0 | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates this cycle: 0.**

---

## DOMAIN VERDICT (cycles 086–089): Propane / LPG NFPA-58 inspection is a CONFIRMED ZERO

Four cycles, 40 candidates, **zero graduates**. This is an honest, valuable "no" — the domain does
**not** hold a defensible #2 for this founder. The reasons are structural, not framing-dependent:

1. **The moat this domain was chosen for is already OWNED by dedicated incumbents.** The Round-4
   map picked propane because "the dealer's field techs accumulate a proprietary per-account system
   + appliance history." That exact flywheel is already the product of **P3 Propane Safety** (~700
   clients, **NPGA-endorsed "gold standard,"** wired into ADD Systems / Blue Cow / AgVantage so it
   pulls the account roster daily) and **Tank Spotter** (100+ companies, 65+ modules, NFPA-54/58
   auto-verified inspections). A new founder starts with **zero** dealers and cannot uniquely
   accumulate data two incumbents already hold. [VERIFIED]

2. **The map feared the wrong incumbent.** It flagged the delivery ERPs (ADD/Cargas/Blue Cow). The
   real killer is the **dedicated compliance-SaaS layer that sits between the tech and the ERP** —
   invisible on Crunchbase, exactly the "entrenched private niche player" the round-3 check warns
   about. Lesson: for mandated-inspection trades, check for a **niche compliance-SoR vendor with a
   trade-association (NPGA/affinity) endorsement**, not just the ERP.

3. **OEMs weaponize free at both ends.** **RegO** (equipment OEM) ships a **free** leak-check/
   gas-check/appliance app; **Otodata / Tank Utility / Anova** (tank-telemetry OEMs) ship free
   monitoring apps + portals and own the tank data feed. Any parasitic or consumer angle is capped
   at ~$0 — the round-3 "OEM ships it free" pattern, twice.

4. **SAM is structurally too small.** The entire buyer universe is **~2,400 NPGA companies**;
   reachable independents ~2,000; realistic safety-compliance ACV $3–15K ⇒ SAM **$6–30M**, 3–15×
   below the $100M gate — and **~35% already penetrated** by P3+Tank Spotter. A countable
   ~2,400-company universe is a red flag (the TAB lesson), not a green field.

5. **Adjacent asset classes don't help.** Cylinders (Blue Rhino/AmeriGas duopoly + P3's requal
   tracker), cargo-tanks (Fleetio/Whip Around/Samsara own fleet inspection), and fuel-oil tanks
   (dedicated inspection apps + a **declining market**) each fail on incumbent, buyer, or growth.

6. **Buyer gate is the only one it passes** (fragmented private dealer, not a regulator) — but one
   passing gate cannot save a domain that fails incumbent + moat + SAM.

**Net for the Round-4 hunt**: Domain #9 joins the honest-zero column. The prize — a defensible #2 in
the CutLog/TitlePlant class — is not here. The single transferable lesson for the remaining Round-4
domains (backflow, septic, well-drilling, cathodic, hood-cleaning, marine, arborist, metrology,
radon): **before promoting any "digitize the mandated inspection" thesis, search for a trade-
association-endorsed niche compliance-SaaS vendor (the P3 pattern) — its existence, more than any
ERP, is what collapses the moat.** If backflow's SwiftComply, septic's e-permit portals, or
metrology's GAGEtrak look like P3, expect the same zero.
