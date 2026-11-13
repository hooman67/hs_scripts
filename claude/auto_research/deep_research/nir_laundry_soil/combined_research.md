# Deep Research: NIR Laundry Soil Classifier

**Idea slug:** `nir_laundry_soil`
**Type:** HW + SW (NIR optical sensor module + edge ML + cloud SaaS)
**Researched:** 2026-06-28
**Source:** Cycle 024 report, idea #1 (PROMOTED through Step 5, feasibility 8/10)

> One-line: An inline near-infrared (NIR) sensor + edge-ML module that classifies the *type* of soil
> (protein/blood, fat/oil, mineral, starch) on incoming commercial-laundry loads and auto-tunes the
> wash formula and chemical dose per load — turning the "chemicals are 17-48% of opex and 15-30% is
> wasted on over-dosing" problem into a measurable line-item saving on the first chemical invoice.

**Verdict: CONDITIONAL GO — leaning NO-GO for this founder.** The market pain is real and quantified,
and the white space (no commercial NIR *soil-type* classifier exists) is genuine. But the idea fails the
founder's two hardest filters: it is hardware-first (custom NIR optical module, harsh wet/hot environment,
per-machine integration), and the closest validated prior art was done by **Henkel + BSH** — exactly the
detergent + appliance incumbents who own the buyer relationship and the chemistry IP. It scores well below
the pure-software bar Hooman should hold out for as a #2 idea.

---

## 1. Product Definition

### 1.1 Exact problem statement
Commercial / industrial laundries (hotels, hospitals, uniform & linen rental, healthcare) wash by
**fixed wash formulas selected from manual soil classification**. Operators sort linen into broad
soil-level buckets (light / medium / heavy) by linen *category* and visual judgment, then run a
pre-programmed formula. Chemical dosing is **formula-based, not soil-based** — Ecolab's commercial
laundry dispensers (Ultrax for washer-extractors, Elados Smart for tunnels) dose "the right amount every
time" per the *programmed formula*, not per the actual soil on the load. (VERIFIED — Ecolab commercial
laundry dispensing page, https://www.ecolab.com/solutions/tcd/commercial-laundry-dispensing-solutions ;
TRSA runs a formal manual "Soil Sort" course, https://www.trsa.org/course/soil-sort/ .)

The cost of this:
- **Chemicals are 17-48% of annual operating cost**; many facilities spend >$125K/yr on chemicals.
  (VERIFIED — Softrol, "Chemical Dosing Accuracy," https://softrol.com/feeds/blog/chemical-dosing-accuracy-laundry )
- **Dosing errors raise opex 15-30%** via over-dosing, rewash, and accelerated linen wear; 30% over-dose
  is "common with manual systems." A $50K chemical budget over-dosed 20% wastes $10K/yr; total savings from
  better accuracy typically $15K-25K/yr, payback <2 yr. (VERIFIED — same Softrol source.)
- Different soils need different chemistry: protein/blood → cool wash + protease/alkali (heat sets blood);
  fat/oil → high alkalinity + surfactant + heat; mineral/clay → builders/acid sour. Mis-classifying soil
  wastes chemistry *and* damages linen. (ASSUMED from standard laundry chemistry; the US Chemical "Laundry
  Formulas" PDF and American Laundry News "wash formula" articles confirm formulas are soil-driven, but the
  PDF text was not machine-readable — https://www.uschemical.com/wp-content/uploads/2016/04/L000241_Laundry_Formulas.pdf )

**What they do today:** humans eyeball/sort, pick a canned formula, and dose to formula. No machine senses
the actual soil chemistry on the load.

### 1.2 Product scope for v1 (3 features max)
1. **Soil-type classification** — NIR reflectance/transmittance of the incoming load (or wash liquor)
   → ML classifier outputs soil-type mix (protein / fat-oil / mineral / starch) + soil load level.
2. **Formula/dose recommendation** — maps the classification to a recommended wash formula + chemical
   dose adjustment, displayed on a dashboard (advisory mode in v1; closed-loop control is v2).
3. **Savings dashboard** — quantified chemical spend vs. baseline, "savings visible on first invoice."

**Explicitly NOT in v1:** closed-loop automatic dispenser control (regulatory/liability + integration with
each OEM dispenser); fabric/fiber identification; water-reuse optimization; consumer machines.

### 1.3 User workflow (day 1)
Sensor module mounted at the soil-side conveyor / load chute of a washer-extractor or tunnel washer →
reads each sling/load → edge ML classifies → dashboard shows recommended formula + dose → operator (or,
v2, the dispenser PLC) applies it → monthly report shows chemical $ saved.

### 1.4 Pricing model
Hardware module $2-5K one-time per wash line + SaaS $500-1,200/mo per facility. Justified by $15-25K/yr
documented chemical savings (payback 2-6 months). (Pricing ASSUMED, anchored to the verified savings range.)

### 1.5 Ideal first customer
Mid-to-large industrial linen/healthcare laundry (the ~1,817 US industrial laundry & linen-supply
businesses; VERIFIED IBISWorld 2026, https://www.ibisworld.com/united-states/number-of-businesses/industrial-laundry-linen-supply/1731/ )
or a multi-property hotel/hospital on-premise laundry. Buyer = plant/operations manager with chemical-budget
authority. Healthcare laundries (blood/protein soils, infection-control formulas) feel the pain most.

---

## 2. Competitive Analysis

### 2.1 Direct competitors (commercial NIR soil-type classifier)
**None found.** Repeated multi-angle searches (DuckDuckGo lite, Bing, Ecosia, Marginalia, vendor sites)
returned **zero** commercial products that spectroscopically classify soil *type* on commercial laundry.
This matches the Cycle 024 "white space" call. (VERIFIED-as-absence, with the caveat below.)

### 2.2 The decisive prior art / incumbent risk — Henkel + BSH
The closest validated work is **NIR real-time soil detection during automatic *dishwashing*** —
authored jointly by **Henkel AG, BSH Hausgeräte (Bosch/Siemens appliances), and University of Bonn**,
detecting oatmeal/egg-yolk/butterfat with **R² > 0.92** using FT-NIR. (VERIFIED — *J. Near Infrared
Spectroscopy* 27(3):183-190, 2019; https://opg.optica.org/jnirs/abstract.cfm?uri=jnirs-27-3-183 ; follow-up
2021 quantitative online tracking system, https://journals.sagepub.com/doi/10.1177/09670335211006614 .)

Implication: the two incumbents who own (a) the detergent chemistry + buyer relationship (Henkel) and
(b) the machine (BSH) **have already prototyped NIR soil sensing** in the adjacent dishwashing domain.
At CES 2025 Henkel launched **SmartWash** — an AI-driven, cartridge-based *adaptive dosing* system for
laundry and dish, consumer-first but explicitly courting appliance-maker partnerships. (VERIFIED —
https://www.prnewswire.com/news-releases/henkels-smartwash-defines-a-new-era-of-clean-at-ces-2025-302346886.html ;
https://www.henkel.com/spotlight/innovation/2025-04-30-the-revolution-in-the-laundry-room-henkel-smartwash-2049578 )
SmartWash today appears to be algorithmic dosing, not optical soil typing (no soil-sensor disclosed), so the
*commercial NIR soil-type* niche is still technically open — but the incumbent is clearly moving down this
road and could fold soil sensing in. **This is a competitive-density 4-5 risk hiding behind a density-2
present-day landscape.**

### 2.3 Indirect competitors / manual alternative
- **Manual soil sorting + fixed formulas** (TRSA Soil Sort course) = the incumbent process. Cheap, "good
  enough," deeply habituated — high customer inertia. (VERIFIED.)
- **Soil-weight tracking** (Softrol Soil Weight Tracking System; https://softrol.com/feeds/service/soil-weight-tracking-system-laundry )
  measures *weight*, not soil type — partial overlap with the "right-size the load/dose" value prop.
- **Turbidity / conductivity wash-liquor sensors** in some OPL washers measure soil *level*, not *type*.

### 2.4 Chemical-supplier dosing incumbents (channel control)
**Ecolab, Diversey (Solenis), Christeyns** sell/lend dosing hardware as a hook for chemical-supply
contracts; their revenue is chemicals, so a product that *cuts* chemical use is structurally opposed to
their model (LEARNINGS #12 invisible-waste is good, but here the channel owner profits from the waste).
Ecolab already markets a "commercial laundry data intelligence platform" with real-time visibility
(VERIFIED — https://www.ecolab.com/about/industries-we-serve/commercial-laundries ), so they own the data
relationship and could add soil sensing as a feature/defensive move.

### 2.5 Big-tech / industrial-QC incumbent scan
Per LEARNINGS #9, checked entrenched optical-QC firms — none are in laundry soil, but several make exactly
the NIR/hyperspectral inspection hardware that would commoditize this: **Cognex, Keyence** (machine vision),
and NIR-sorting players. The real risk is not them entering laundry but the **detergent/appliance duopoly
(Henkel/BSH, P&G, Electrolux Professional, Alliance/UniMac, Girbau, Kannegiesser, Jensen)** bundling it.

### 2.6 Verdict
**CONDITIONAL GO.** Present-day white space is real (density 2). But the moat is weak: the core method is
already published by the incumbents (Henkel/BSH), the chemistry IP and buyer relationship sit with chemical
suppliers who are *adverse* to chemical savings, and a small HW+SW startup would be racing Henkel SmartWash's
roadmap. For a solo software founder this is a NO-GO; for a hardware-comfortable team it's a CONDITIONAL GO.

---

## 3. Feasibility & Prototype Plan

### 3.1 Core feasibility claims (confidence-marked)
- **NIR can classify common soils in a wash context** — VERIFIED (Henkel/BSH dishwashing study, R²>0.92,
  oatmeal/egg/fat; 2019/2021). Laundry textiles add fabric-background variance not in that study → the
  *textile* generalization is ASSUMED, not verified.
- **Commodity chip-scale NIR sensors exist** — VERIFIED. **Si-Ware NeoSpectra Micro / NeoSpectra Scanner**,
  MEMS FT-NIR, 1350-2500 nm, "benchtop accuracy at 10x lower cost," OEM module form factor
  (https://welcome.si-ware.com/neospectra-performance-profitability/nir-spectrometer ). Volume module price
  ~$300-500 and dev kit low-thousands is ASSUMED (vendor does not publish list price; TI DLP NIRscan Nano,
  the cheaper alt cited in Cycle 024, is **discontinued** — UNVERIFIED that a sub-$50 NIR sensor with the
  needed range still ships). Hamamatsu mini-spectrometers are the backup (https://shop.hamamatsu.com/collections/mini-spectrometers ).
- **Soil-type → chemistry mapping is well understood** — ASSUMED (standard laundry chemistry; sources
  confirm formulas are soil-driven but text not machine-extracted).
- **Edge ML (random forest / 1D-CNN on NIR spectra) is trivial** — VERIFIED (Hooman's core skill; many
  published NIR-classification pipelines).
- **Hardest unsolved problem** — UNVERIFIED and the crux: getting a clean, repeatable NIR read of *soiled
  textile in a hot/wet/moving industrial line* (steam, water film, varying fabric/color background, motion)
  vs. the controlled lab transmittance cell in the Henkel study. Calibration across fabric × color × soil
  combinations needs a large labeled dataset that **does not exist publicly** and must be built inside a
  partner laundry. This is the make-or-break and is currently unsolved.

### 3.2 Bill of materials (prototype, Phase 1)
| Item | Part / source | Unit cost | Notes |
|---|---|---|---|
| NIR sensor | Si-Ware NeoSpectra Micro dev kit | ~$3-4K (ASSUMED) | MEMS FT-NIR 1350-2500nm; backup: Hamamatsu C12880MA mini (~$300, 340-850nm — too narrow, VIS only) |
| Edge compute | Raspberry Pi 5 / Jetson Orin Nano | $80-500 | runs classifier |
| Illumination | broadband NIR LED/halogen + optics | $50-150 | |
| Enclosure | IP65 wet/steam-hardened housing | $100-300 | custom — mech-eng friend task |
| **Phase-1 total** | | **~$4-5K** | one bench rig |

### 3.3 Software stack
- Spectral preprocessing: SNV/MSC, Savitzky-Golay (scipy / `pybaselines`).
- Classifier: scikit-learn RandomForest baseline → 1D-CNN (PyTorch) once data grows.
- Cloud: simple FastAPI + Postgres + a dashboard; AWS (Hooman's home turf). All low-risk.

### 3.4 Cheap Phase-0 PoC (<$100, <1 week) — answer the one fatal question first
**Question: can NIR even separate soil types on *textile* (not in a clean cuvette)?**
1. Borrow/rent a benchtop NIR or use a smartphone-NIR / cheap VIS-NIR module (~$60) — Phase-0 accepts
   reduced range for speed (LEARNINGS #15 "alternate faster path").
2. Prepare swatches: clean towel + towel soiled with blood (protein), cooking oil (fat), clay (mineral),
   starch — 10 each, wet and dry.
3. Scan, run a RandomForest in a notebook, report cross-val accuracy.
4. **Go/no-go:** if you cannot separate protein vs oil vs mineral on *wet textile* at >85% with a low-cost
   sensor, the whole idea is dead before spending on the NeoSpectra. This is the single highest-leverage
   experiment and costs a weekend.

### 3.5 Risk register
| Risk | Likelihood | Impact | Mitigation | Fallback |
|---|---|---|---|---|
| NIR can't classify on wet/moving textile | **High** | Fatal | Phase-0 swatch test first; control geometry/illumination | Pivot to wash-liquor sensing (closer to Henkel's proven cuvette case) |
| No cheap sensor with right NIR range (TI discontinued) | Med | High | NeoSpectra Micro / Hamamatsu | Higher BOM, hurts unit economics |
| Calibration dataset must be built in a partner plant | **High** | High | Pilot deal trading free hardware for data | Slow, capital-heavy |
| Henkel/BSH or Ecolab bundle soil sensing | Med | High | Move fast, target chemical-agnostic value | Acqui-hire/exit, or niche to healthcare |
| Chemical suppliers block (channel control) | Med | High | Sell direct to laundry operator on $ savings | Partner with a challenger chemical brand |
| Harsh-environment hardware reliability | Med | Med | IP65, mech-eng friend | Service contracts |

### 3.6 Validation criteria & timeline
- "Working" = >85% soil-type accuracy on wet textile in Phase-0; in Phase-1, demonstrate a recommended
  dose change that yields measurable chemical reduction on one real line.
- Phase-0: 1 weekend, <$100. Phase-1 bench: 4-6 weeks, ~$5K. Plant pilot + dataset: 3-6 months, requires a
  partner laundry (the real gate). To first revenue: 12+ months (matches Cycle 024 estimate), capital
  $250-400K (VERIFIED-consistent with Cycle 024).

---

## 4. Customer Validation Strategy

### 4.1 First 5 customers to approach
1. Independent regional **healthcare laundry** (blood/protein, infection-control formulas — highest pain).
2. **Hotel/resort OPL** group operations manager (multi-property, visible chemical spend).
3. **Uniform/linen rental** plant (UniFirst, Cintas franchisee, or regional independent).
4. A **TRSA member** plant (they run the Soil Sort course → already think about soil classification).
5. A challenger **chemical supplier** open to a chemical-agnostic analytics layer (not Ecolab/Diversey).

### 4.2 Discovery questions (don't reveal the hand)
- "How do you decide which wash formula a load gets today? Who sorts, how?"
- "What's your monthly chemical spend, and how do you know if you're over-dosing?"
- "What % of loads get rewashed? What drives it?"
- "If you could see soil *type* per load automatically, would you change your formulas?"

### 4.3 Demand signal = confirmed
LOI or a paid pilot where the laundry gives floor access + chemical-invoice baseline data in exchange for a
free sensor — and agrees to pay SaaS if first-invoice savings beat a threshold. Verbal "nice idea" ≠ demand.

### 4.4 Where buyers congregate
**TRSA** (Textile Rental Services Association — courses, Clean Show), **American Laundry News** (trade
press), **Clean Show / The Laundry Show**, ARTA (healthcare laundries), LinkedIn plant-manager groups.
Per LEARNINGS #14, Facebook/industry groups are high-signal — but commercial laundry is more
association/trade-show driven than the hobbyist laser/CNC crowd.

---

## 5. Scorecard

| Dimension | Weight | Score (1-10) | Rationale |
|---|---|---|---|
| Capital required (lower=better) | 15% | 5 | $250-400K to revenue; bench Phase-1 ~$5K but plant pilot + dataset is capital/time heavy |
| Time to first revenue | 15% | 4 | 12+ mo; gated on building a labeled dataset inside a partner plant |
| Competitive moat | 15% | 3 | Method already published by Henkel/BSH; chemical suppliers own channel; SmartWash adjacent |
| Technical risk (lower=better) | 10% | 4 | Core wet-textile NIR classification UNVERIFIED; calibration across fabric×color×soil is hard |
| Market size (SAM) | 10% | 6 | Real ($100M+ if SaaS across thousands of OPL+industrial sites), but only ~1,817 large US industrial plants |
| Founder-market fit | 15% | 4 | ML/cloud = strong; but HW-first, harsh-environment optics, plant integration = exactly the penalty zone for a solo software founder (LEARNINGS #1, #3) |
| Customer accessibility | 10% | 5 | Reachable via TRSA/trade shows, but conservative buyers, association-gated, long-ish B2B cycle |
| Scalability | 10% | 5 | SaaS scales; per-line hardware install + per-plant recalibration limits it |

**Weighted total:** 0.15(5)+0.15(4)+0.15(3)+0.10(4)+0.10(6)+0.15(4)+0.10(5)+0.10(5)
= 0.75+0.60+0.45+0.40+0.60+0.60+0.50+0.50 = **4.4 / 10**

### Verdict: CONDITIONAL GO (effectively NO-GO for this founder)
The pain is real and beautifully quantified (chemicals 17-48% of opex, 15-30% wasted, savings on first
invoice), and there is genuine present-day white space. But it fails Hooman's structural filters:
hardware-first in a wet/hot industrial environment, an UNVERIFIED core feasibility claim (wet-textile NIR
classification), a dataset that must be built inside a partner plant, and a weak moat against incumbents
(Henkel/BSH already published the method; chemical suppliers control the channel and profit from the waste).
**Recommendation:** keep CutLog as #1; do NOT pick this as #2 unless (a) the weekend Phase-0 swatch test
clears >85% on wet textile AND (b) a hardware-comfortable co-founder joins. A pure-software idea should
out-rank this for the secondary income stream.

---

### Interesting facts uncovered
- Henkel + BSH (Bosch/Siemens) jointly prototyped NIR soil sensing — for *dishwashers* — back in 2019, hitting R²>0.92.
- Henkel shipped **SmartWash** AI adaptive dosing at CES 2025, signaling incumbent intent to own adaptive dosing.
- Chemicals are **17-48% of commercial laundry operating cost**; 30% over-dosing is "common with manual systems."
- Only **~1,817** US industrial laundry & linen-supply *businesses* (IBISWorld 2026) — far fewer than the "10,000+ facilities" in the Cycle 024 SAM; OPL sites (hotels/hospitals) expand the count but are smaller buyers.
- The cheap sensor Cycle 024 assumed (TI DLP NIRscan Nano, sub-$50) is **discontinued**; the realistic part is Si-Ware NeoSpectra Micro (chip-scale MEMS FT-NIR, low-hundreds-$ in volume, not sub-$50).
- The chemical-supplier channel (Ecolab/Diversey/Christeyns) profits from chemical volume — structurally adverse to a product that cuts chemical use.
