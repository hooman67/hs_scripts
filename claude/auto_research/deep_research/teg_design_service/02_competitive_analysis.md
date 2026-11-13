# 02 - Competitive Analysis: TEG Design-as-a-Service

## Direct Competitors

### 1. Applied Thermoelectric Solutions LLC (Novi, Michigan)
- **Founded:** Unknown (small consultancy)
- **Funding:** None (bootstrapped one-person shop)
- **Revenue:** ~$200K/year (estimated)
- **Headcount:** 1
- **Pricing:** Likely $150-$300/hr consulting rates
- **Services:** Feasibility analysis, prototype development, modeling, design optimization
- **Approach:** Traditional physics-based (no ML/AI)
- **Weaknesses:** No AI differentiation; one-person capacity constraints; no web platform; no brand recognition; slow turnaround (traditional consulting timelines)
- **Threat Level:** LOW-MEDIUM. Validates the market exists but also demonstrates its ceiling.

### 2. In-house COMSOL Teams (The Incumbent Approach)
- **What:** Companies licensing COMSOL Multiphysics ($25K-$50K/year) and hiring thermoelectric PhDs internally
- **Scale:** COMSOL AB has ~$200M+ revenue; the TE modeling module is a small fraction
- **Pricing:** $25K-$50K license + $120K-$180K/year for a qualified engineer
- **Weaknesses:** Requires rare expertise to operate; slow iteration (days per simulation run); expensive total cost of ownership ($200K+/year)
- **Threat Level:** MEDIUM. This is the primary incumbent. Most potential customers who can afford this already do it in-house.

### 3. TeGDS (MATLAB File Exchange)
- **What:** Free MATLAB-based TEG geometry optimization and simulation tool
- **Pricing:** Free (requires MATLAB license ~$2K/year)
- **Weaknesses:** Academic quality; no support; requires MATLAB expertise; no validation against real hardware; no CAD output
- **Threat Level:** LOW. DIY option for academics and technically sophisticated teams.

## Indirect Competitors

### 1. ORC System Vendors (Orcan Energy, Enertime, Heliex Power)
- Compete for the same "waste heat recovery" budget dollars
- ORC (Organic Rankine Cycle) turbines work better at higher temperatures (>300C) and larger scales (>100kW)
- TEGs win at lower temperatures (<300C), smaller scales (<10kW), and where no moving parts are essential
- **Threat Level:** MEDIUM for overlapping temperature/scale ranges

### 2. Global Power Technologies (Calgary)
- Manufactures complete TEG products for remote off-grid power (oil & gas pipelines)
- Sells finished systems, not design services
- Fixed product catalog, not custom optimization
- **Threat Level:** LOW. Product company, not a service competitor.

### 3. TEGnology (Denmark)
- Makes TEG modules for industrial IoT power harvesting (milliwatt scale)
- Different market segment entirely (sensor power vs. industrial recovery)
- **Threat Level:** LOW.

### 4. Gentherm (NASDAQ: THRM, $1.5B revenue)
- Abandoned TEG power generation years ago; focused on thermal comfort (heated seats)
- **Threat Level:** NEGLIGIBLE.

## Adjacent Movers (One Pivot Away)

### 1. Northwestern Thermoelectrics Group (Prof. Jeff Snyder)
- World-leading academic lab; ZT Calculator already online
- NASA-JPL partnerships; high credibility
- Could spin off commercial design service at any time
- **Threat Level:** MEDIUM. Academic reputation gives instant credibility.

### 2. NIMS Japan (TEGNet Creators)
- Developed the actual TEGNet model this startup would use
- Currently research-focused, not commercial
- Could offer competing service with "original creator" authority
- **Threat Level:** LOW-MEDIUM. Unlikely to commercialize but carries moral authority risk.

### 3. Materials Informatics Startups (Citrine Informatics, MaterialsZone)
- AI-powered materials design platforms
- Could add TEG optimization as a vertical module
- Citrine has raised $40M+ in funding
- **Threat Level:** LOW. TEG market too small to attract their attention, but technically trivial for them to enter.

### 4. Alphabet Energy (DEFUNCT - Critical Lesson)
- Raised $35M+ (Schlumberger, GM Ventures, TPG Capital)
- Built TEG hardware for oil & gas waste heat
- Failed in 2018: hardware CapEx too high, oil price crash, slow adoption
- **Lesson:** Even $35M couldn't make TEG economics work in hardware. Design-only avoids the hardware trap but underlying demand problem persists.

## Open Source / DIY Risk

**HIGH.**

The core technology stack is entirely open:
- **TEGNet** (Apache-2.0, GitHub) - the primary ML model
- **TeGDS** (MATLAB File Exchange) - geometry optimization
- **ThermoParser, AMSET, Phoebe** - thermoelectric property calculations
- **OpenFOAM** - free CFD alternative to COMSOL for thermal simulation
- **FreeCAD / CadQuery** - parametric CAD generation
- **GitHub: albertoferrarioPD/ThermoelectricGeneratorDesignAndSimulation** - open simulation code

Any engineering firm with a competent ML engineer could replicate the proposed service in 2-4 weeks. The "moat" is expertise and speed, not proprietary technology.

## Big Tech Risk

**VERY LOW.**

- No FAANG/MANGA company has interest in TEG design (market too small at ~$1B total)
- Industrial conglomerates (Siemens, ABB, Honeywell) have thermal management divisions but zero TEG design service interest
- The entire TEG consulting market is likely $5-20M globally - invisible to big tech
- Risk of an AI materials company pivoting in is theoretically possible but economically irrational

## Final Verdict: NO-GO

**Reasoning:**

1. **Market too small.** The addressable market for TEG design consulting is likely $5-20M globally. The sole known direct competitor does ~$200K/year. Even with 50% market share, this is a $2.5-10M business at best - below venture scale.

2. **Zero defensibility.** TEGNet is Apache-2.0 open source. COMSOL is commercially available. The workflow (ML inference + simulation + CAD) can be replicated by any engineering firm. Speed advantage erodes as competitors adopt the same tools.

3. **Consulting trap.** Revenue scales linearly with headcount. The "5 days per project" promise means maximum capacity of ~48 projects/year solo, or $720K-$2.4M revenue at $15K-$50K/project. This is a good lifestyle business, not a venture-scale opportunity.

4. **Weak demand signals.** The fact that only one tiny competitor exists (after decades of TEG technology being available) suggests insufficient demand, not an untapped opportunity.

5. **Alphabet Energy's $35M failure.** The fundamental problem is not design speed - it's that TEG economics (5-8% efficiency, high $/watt) make adoption marginal for most applications. Faster design doesn't fix the underlying ROI problem for customers.

6. **Long sales cycles.** Industrial buyers take 12-18 months to make $50K service decisions. CAC will be high relative to deal size for a bootstrapped founder without industry connections.
