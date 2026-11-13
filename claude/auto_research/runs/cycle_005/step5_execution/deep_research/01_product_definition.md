# Product Definition: Portable Brewery EPR Freshness Monitor

## Problem Statement

Craft breweries lose 3-8% of production annually to oxidative staling — flavor degradation caused by free radical chain reactions that convert desirable hop and malt compounds into cardboard-like aldehydes (primarily trans-2-nonenal). The problem:

1. **Current detection is indirect.** Dissolved oxygen (DO) meters measure O2 levels — an *input* to staling, not staling itself. A batch with 20 ppb DO might be fine; another with 15 ppb might already be damaged. DO is a necessary but insufficient indicator.

2. **Direct detection requires sending samples to labs.** Reference EPR spectroscopy (the gold standard for measuring free radicals) costs $200-500/sample, takes 3-7 days for results, and requires spin-trapping reagent preparation by trained chemists. By the time results arrive, the batch is packaged and shipped.

3. **Sensory panels catch staling too late.** Trained tasters detect oxidation only after significant damage has occurred — typically when trans-2-nonenal exceeds 50 ng/L (threshold varies by beer style). At that point, the batch is already ruined.

**The gap:** No tool exists that gives a brewer a real-time, direct measurement of oxidative radical activity in beer at the production floor.

**Confidence: HIGH** — This problem is well-documented in brewing science literature (Bamforth 2004, Vanderhaegen et al. 2006, Lund et al. 2012). The EPR method is validated academically but has never been miniaturized for field use.

---

## Product Scope v1 (MVP)

### What It Is

A handheld probe (~500g, battery-powered) with a disposable sample cartridge that measures free radical concentration in a beer sample via miniaturized Electron Paramagnetic Resonance spectroscopy. Results display on a paired mobile app in <30 seconds.

### Core Features (MVP — maximum 3)

1. **Single-measurement radical assay**: Insert sample cartridge (pre-loaded with PBN spin trap), pipette 200 uL of beer, insert into probe, get a "Freshness Score" (0-100 scale) in 30 seconds.

2. **Mobile companion app**: Bluetooth-connected iOS/Android app displays results, stores batch history, shows trend lines per beer style, alerts when a batch crosses user-defined thresholds.

3. **Calibration kit**: Monthly calibration standard (known radical concentration) shipped with cartridge refills to maintain measurement accuracy.

### What It Does NOT Do (v1)

- No inline/continuous monitoring (sample-based only)
- No integration with brewery ERP/management software
- No prediction of remaining shelf life (just current radical state)
- No identification of specific radical species (total radical load only)
- No multi-analyte panel (only oxidative radicals, not diacetyl/DMS/other off-flavors)

### Success Criteria for MVP

| Metric | Target | Rationale |
|--------|--------|-----------|
| Measurement time | <30 seconds | Must fit into brewer's workflow without waiting |
| Sensitivity | Detect 0.1-50 uM spin-trapped radical (PBN-OOH adduct) | Covers the biologically relevant range for beer oxidation |
| Correlation with lab EPR | R-squared > 0.90 | Must produce trustworthy results |
| Device weight | <600g | One-hand operation |
| Battery life | >50 measurements per charge | Full shift without recharging |
| Cartridge cost | <$3/test at production volume | Keeps per-test cost manageable for craft budgets |

---

## User Workflow

**Persona:** Head brewer / QC manager at a 5,000-15,000 barrel/year craft brewery. Age 28-45, technically curious, quality-obsessed, budget-conscious. Uses refractometers, pH meters, and DO meters daily. Comfortable with digital tools but not a scientist.

### Daily Workflow (3-5 minutes total)

1. **Sample collection** (30 sec): Pull 5 mL sample from bright tank, fermenter, or packaged can using standard sampling port or can piercer.

2. **Cartridge preparation** (15 sec): Snap open a single-use cartridge (pre-loaded with spin-trap reagent). Pipette 200 uL of beer sample into cartridge well using included micropipette.

3. **Insert and measure** (30 sec): Slide cartridge into probe slot. Press "Measure" button. Device emits a brief chirp when complete.

4. **Read result** (5 sec): Freshness Score appears on phone app — green (0-30: fresh), yellow (31-60: monitor closely), red (61-100: staling in progress). Historical trend line updates automatically.

5. **Act on result**: If yellow/red, brewer investigates — check DO pickup points, CO2 blanket integrity, transfer hose connections, yeast health. Optionally re-test after corrective action.

### Weekly Workflow

- Compare scores across batches, fermenters, and beer styles
- Review trend dashboards to identify systemic oxidation sources
- Export reports for quality documentation

---

## Pricing Model

### Hardware

| Tier | Price | Includes |
|------|-------|----------|
| Starter Kit | $4,995 | Probe unit + 100 cartridges + calibration kit + 1 year app subscription |
| Pro Kit | $7,995 | 2 probe units + 500 cartridges + calibration kit + 2 year app subscription + priority support |

### Consumables (recurring revenue)

| Item | Price | Notes |
|------|-------|-------|
| Cartridge 50-pack | $125 ($2.50/test) | Refill packs shipped monthly/quarterly |
| Cartridge 200-pack | $400 ($2.00/test) | Volume discount |
| Annual calibration kit | $195 | Includes 4 calibration standards |

### Software Subscription (after included period)

| Plan | Price | Features |
|------|-------|----------|
| Basic | $49/month | App access, batch history, basic alerts |
| Pro | $99/month | Multi-user, API access, export, advanced analytics |

### Revenue Model Math (Year 1 target: $500K)

- Sell 60 Starter Kits @ $5K = $300K
- Consumable revenue (60 breweries x 100 tests/year x $2.50) = $15K
- Software subscriptions (60 x $49/mo x 6 months avg) = $18K
- Pro Kit upgrades (10 @ $8K) = $80K
- Total Year 1: ~$413K hardware + $33K recurring = $446K

**To hit $500K:** Need ~70 units sold in Year 1 or higher Pro Kit mix. Aggressive but achievable if beta program converts well.

**Confidence: MEDIUM** — Pricing is in the sweet spot based on comparable brewery instruments (Anton Paar CboxQC at $10K+, Hach portable DO at $3K+). Actual willingness-to-pay requires validation.

---

## Ideal First Customer Profile

### Primary Target: Quality-Obsessed Mid-Size Craft Breweries

**Firmographics:**
- Annual production: 5,000-30,000 barrels
- Revenue: $2M-$15M
- Employees: 10-50
- Has a dedicated QC person (or head brewer doubles as QC)
- Already owns: DO meter, pH meter, turbidity meter, possibly a spectrophotometer
- Location: US, with concentration in craft-dense regions (Pacific Northwest, Colorado, New England, Upper Midwest)

**Psychographics:**
- "Science-forward" breweries that market on quality and consistency
- Participates in competitions (GABF, World Beer Cup)
- Active in brewing science communities (MBAA, local guild technical committees)
- Has experienced a staling-related batch loss or customer complaint in the past 12 months
- Follows Bruker/academic EPR research on beer oxidation (small but real segment)

### Top 5 Ideal First Customer Archetypes

1. **The Hop-Forward IPA Specialist** — IPAs are extremely susceptible to oxidation (hop compounds are radical-scavenger targets). These breweries obsess over freshness dating and cold-chain. They would kill for a tool that proves their beer is fresh at packaging. Examples: Alchemist, Tree House, Trillium, Monkish.

2. **The Quality-Certified Brewery** — Breweries pursuing or maintaining SQF/ISO/HACCP certification need documented quality controls. An EPR monitor adds a quantitative data point to their QC program. Examples: Larger regionals like Deschutes, Firestone Walker, Bell's.

3. **The Distribution-Expanding Brewery** — Breweries moving from taproom-only to distribution face new staling challenges (time in market, temperature abuse). They need assurance their beer arrives fresh. Examples: Mid-size breweries entering new states.

4. **The Contract Brewer** — Breweries that contract-brew for others need to prove quality to their clients. Quantitative freshness data is a competitive differentiator. Examples: Two Roads, Brew Hub.

5. **The Brewing Science Geek** — Owner/brewer with a chemistry or biology background who is intrinsically interested in radical measurement. Will be an early adopter and evangelist. These exist in every craft brewing community.

### Disqualified Customers (Not v1 Targets)

- Nano-breweries (<1,000 bbl): Cannot afford $5K instrument
- Macro-breweries (AB InBev, Molson Coors): Have in-house EPR labs already; would not buy a $5K tool when they have $200K Bruker systems
- Non-beer producers (wine, spirits): Different oxidation chemistry; requires separate validation (v2+ opportunity)

---

## Key Assumptions Requiring Validation

| Assumption | Confidence | How to Validate |
|------------|------------|-----------------|
| Brewers will pay $5K for a staling detection tool | MEDIUM | Customer discovery interviews (Doc 4) |
| 30-second measurement is achievable with miniaturized EPR | LOW | Physics prototype (Doc 3) |
| PBN spin-trap in disposable cartridge is shelf-stable for 6+ months | MEDIUM | Accelerated aging study |
| Brewers will adopt a new QC step in their workflow | MEDIUM | Beta program usage data |
| $2.50/test consumable cost is acceptable | HIGH | Comparable to DO meter sensor caps ($1-5 each) |
| Freshness Score correlates with sensory staling perception | MEDIUM | Controlled forced-aging study with trained panel |
