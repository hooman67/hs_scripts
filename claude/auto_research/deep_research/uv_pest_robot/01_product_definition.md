# 01 - Product Definition: Autonomous UV-C Pest Control Robot Fleet

## Problem Statement

High-value crop growers (berries, vineyards, greenhouses) spend $500-2,000/acre/season on chemical pesticides that:
1. Prevent organic certification (organic premium: 30-100% higher retail prices)
2. Face increasing regulatory restrictions (EU Farm to Fork: 50% pesticide reduction by 2030)
3. Create resistance in pest populations requiring stronger/costlier chemicals each year
4. Harm beneficial insects (pollinators), creating secondary pest outbreaks
5. Generate food safety concerns that constrain market access (export MRLs)

**The core pain**: Growers want organic certification revenue but cannot achieve pest control without chemicals. Existing organic methods (beneficial insects, neem oil, manual scouting) are labor-intensive, inconsistent, and often insufficient for commercial-scale operations.

**Confidence: HIGH** — validated by SAGA Robotics' commercial traction (150+ robots deployed, 40% ROI claims), TRIC Robotics' oversubscribed $5.5M seed round, and Carbon Robotics' $100M+ revenue proving ag-robot willingness-to-pay.

---

## Product Scope v1 (MVP)

### What It Does
An autonomous ground robot fleet that patrols crop rows at night, applying calibrated UV-C light to kill insects and fungal spores without chemicals.

### Core Features (MVP — 3 maximum)
1. **Autonomous night patrol**: GPS-RTK guided (±2cm) robot navigates between crop rows at 0.5-1 mph, applying UV-C to foliage from multiple angles. Operates dusk-to-dawn (8-10 hours) without human intervention.
2. **Dual-mode pest kill**: UV-C radiation for fungal spore destruction (proven) + UV-attraction phototaxis combined with mechanical capture (vacuum/electrocution) for flying insects (the differentiation from SAGA).
3. **Fleet management dashboard**: Coverage maps, pest pressure heatmaps, treatment logs for organic certification documentation, multi-robot coordination.

### What It Does NOT Do (explicit scope boundaries)
- No daytime operation (UV-C degrades in sunlight; night operation exploits insect phototaxis)
- No weed control (that is Carbon Robotics' domain)
- No harvesting or crop manipulation
- No chemical application of any kind
- No indoor/greenhouse in v1 (outdoor field deployment only — greenhouses are v2)

### Success Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Pest reduction vs. untreated | >70% | Trap counts + visual assessment |
| Acres covered per robot per night | >10 acres | GPS logs |
| Autonomous uptime (no intervention) | >95% | Fleet telemetry |
| Cost per acre vs. chemical program | <60% | Direct cost comparison |
| Organic certification enablement | Yes | USDA NOP compliance audit |

---

## User Workflow

### Farmer Experience (Day-to-Day)

1. **Setup (once per season)**: Technician installs GPS-RTK base station, maps field boundaries and row paths via tablet app. Robots are delivered pre-configured.
2. **Daily operation**: At dusk, robots autonomously undock from charging stations, begin patrol routes. Farmer receives morning summary: "12.4 acres treated, 3 pest hotspots detected in Block C rows 14-18."
3. **Monitoring**: Dashboard shows real-time robot positions, historical coverage heatmaps, pest trend data. Alerts only for anomalies (stuck robot, low battery, obstacle).
4. **Seasonal review**: End-of-season report documenting all treatments for organic certification auditors. Comparative yield/quality data vs. previous chemical seasons.

### Operational Model
- **RaaS (Robotics-as-a-Service)**: No equipment purchase. Seasonal contract. We own, maintain, deploy robots.
- **Service window**: Seasonal (March-October in Northern Hemisphere berry/vine regions)
- **Support**: Remote fleet monitoring 24/7 + on-site technician visit 1x/week

---

## Pricing Model

### Primary: Robotics-as-a-Service (per-acre/season)

| Tier | Acreage | Price/Acre/Season | Annual Contract Value |
|------|---------|-------------------|----------------------|
| Starter | 10-25 acres | $1,200/acre | $12K-30K |
| Growth | 25-75 acres | $1,000/acre | $25K-75K |
| Enterprise | 75-200+ acres | $800/acre | $60K-160K |

**Justification**: Growers currently spend $500-2,000/acre on chemical programs. Our pricing at $800-1,200/acre replaces chemicals AND enables organic premium (30-100% price increase on harvest). Net ROI for grower: 2-4x in first season.

**Confidence: MEDIUM** — Pricing validated by SAGA's reported $800-1,500/acre pricing and willingness-to-pay surveys in ag-tech literature. Actual willingness depends on demonstrated efficacy.

### Revenue Build-Up
- Year 1: 5-8 growers, 80-120 acres, $80K-$144K actual (below $1M unless aggressive)
- **Realistic Year 1 revenue: $500K-800K** (not $1M as initially projected unless 10+ grower deals close)
- Year 2: 20+ growers, 400+ acres, $320K-480K
- Year 3: 50+ growers, 1000+ acres, $800K-1.2M

**Honest assessment**: The $1M Year 1 revenue target is aggressive. Seasonal deployment means you have ONE growing season to prove it works. More realistic: $300-500K Year 1 revenue from 3-5 early adopter growers paying premium for the novelty + organic enablement.

---

## Ideal First Customer Profile

### Demographics
- **Crop**: Organic or transitioning-to-organic strawberry grower
- **Location**: Salinas Valley / Watsonville, CA (highest density of premium strawberry operations)
- **Size**: 50-150 acres (large enough to justify fleet, small enough to be agile)
- **Current pain**: Spending $1,500+/acre on organic-compliant pest management (beneficial insects + manual scouting + organic sprays) with inconsistent results
- **Mindset**: Technology-forward, already uses GPS guidance on tractors, has tried at least one ag-tech product

### Why Strawberries First
1. Highest pest pressure crop (spider mites, thrips, botrytis — all UV-C susceptible)
2. Highest chemical spend per acre ($1,500-2,500)
3. Highest organic premium (organic strawberries: 80-120% retail premium over conventional)
4. Concentrated geography (easy to service multiple growers from one base in Central California)
5. SAGA and TRIC both started here — validates the beachhead

### Specific Target Companies (public info)
1. Driscoll's contract growers (largest berry company globally, aggressive on sustainability)
2. California Giant Berry Farms growers
3. Naturipe Farms organic division
4. Independent growers in Watsonville/Salinas with 50-200 acre operations
5. Mañana berries (organic-focused, technology-forward)

### First Customer Deal Structure
- **Pilot**: 10 acres free for 4 weeks (prove efficacy)
- **Convert**: Remaining acreage at $1,000/acre/season if pilot shows >50% pest reduction
- **Reference**: Permission to publish results + use as case study
- **Timeline**: Secure pilot commitment by December for spring deployment
