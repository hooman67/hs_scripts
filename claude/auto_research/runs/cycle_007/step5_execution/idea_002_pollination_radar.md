# Execution Plan: Precision Pollination Monitoring for Almond/Berry Growers

## 5a. Product Definition

**Core value proposition**: See exactly where pollinators are working your fields — verify hive rental ROI, find dead zones, optimize placement — all without disturbing a single bee.

**Key features for MVP (max 3)**:
1. Radar-based pollinator activity map updated every 15 minutes across monitored acreage
2. Hive placement optimizer: recommends moves based on activity patterns
3. Daily pollination report with per-block scoring (0-100% pollination adequacy)

**What it does NOT do**:
- Does not identify individual bee health or disease (hive-level monitoring is BeeHero's domain)
- Does not replace hive inspections
- Does not manage hive logistics or beekeeper relationships

**Success metrics for prototype validation**:
- Detects pollinator activity with >90% correlation to manual observation counts
- Correctly identifies under-pollinated zones (validated by fruit set data at harvest)
- 5 almond growers deploy during 2027 bloom season (Feb-March)

---

## 5b. Technical Architecture

**System components**:
1. mmWave radar unit (TI IWR6843 or AWR2944) on 3m pole mount
2. Edge compute (Jetson Nano or RPi 5) for on-device ML inference
3. Solar + battery power system (remote field deployment)
4. Cellular/satellite uplink (LTE CAT-M1, satellite fallback)
5. Cloud backend: data aggregation, map generation, analytics
6. Web/mobile app: activity maps, reports, hive optimizer

**Technology stack**:
- Radar: TI IWR6843AOP evaluation module ($100-200) with custom firmware
- Edge ML: TensorFlow Lite micro-Doppler classification model
- Comms: Quectel BG96 (LTE-M + GPS) or satellite for remote fields
- Backend: AWS IoT Core → Lambda → TimescaleDB → S3
- Frontend: React web app + React Native mobile
- ML training: Collect insect radar signatures → train species classifier

**Build vs buy**:
- Radar module: BUY (TI IWR6843, $100-200)
- Edge compute: BUY (Raspberry Pi 5 or Jetson Nano, $50-100)
- Solar power: BUY (standard 50W panel + 50Ah battery kit, $200)
- Cellular modem: BUY (Quectel, $30)
- Pole mount + enclosure: BUILD (custom weatherproof, $50)
- ML classifier: BUILD (proprietary, core IP)
- Cloud + app: BUILD

**Key technical risks**:
- Radar range limitation: TI IWR6843 effective range for insect-sized targets may be 20-50m → covers ~1 acre per unit (need 1 per 1-3 acres)
- Species confusion: honeybees vs other pollinators at 85% accuracy may be sufficient but growers want confidence
- Environmental noise: wind, dust, birds may create false positives → need robust filtering
- Seasonal deployability: units must survive outdoor exposure (rain, 100°F+ heat, dust)

---

## 5c. Bill of Materials (Per Monitoring Unit)

| Component | Supplier | Unit Cost | Notes |
|-----------|----------|-----------|-------|
| TI IWR6843AOP radar module | TI / Mouser | $150 | 60 GHz, antenna-on-package |
| Raspberry Pi 5 (4GB) | Various | $60 | Edge inference |
| Quectel BG96 LTE-M module | Quectel / DigiKey | $30 | Cellular + GPS |
| 50W solar panel | Renogy | $60 | Weatherproof |
| 50Ah LiFePO4 battery | various | $80 | 3+ days autonomy |
| Solar charge controller | Victron | $30 | MPPT |
| Custom PCB (carrier board) | JLCPCB | $10 | Integrates all modules |
| Weatherproof enclosure (IP67) | Polycase | $40 | UV-resistant |
| 3m pole + ground spike | Custom fabrication | $30 | Field deployment |
| Cabling + connectors | Various | $20 | Weatherproof |
| **Total BOM per unit** | | **~$510** | |

**Target price to grower**: $3,000-5,000 per unit (installed)
**Gross margin**: 85%+ (at $4K selling price)

---

## 5d. Build Instructions

1. **Weeks 1-4: Radar Signal Processing R&D** (radar/DSP engineer)
   - Configure TI IWR6843 for micro-Doppler insect detection
   - Replicate Denmark team's wingbeat extraction pipeline
   - Characterize detection range for honeybee-sized targets
   - Collect baseline radar data near commercial hives

2. **Weeks 3-6: ML Model Development** (ML engineer)
   - Collect labeled radar signatures: honeybees, bumblebees, wasps, flies, moths
   - Train micro-Doppler classifier (target: 85%+ species accuracy)
   - Optimize for edge deployment (TFLite, <100ms inference)
   - Validate against manual observation ground truth

3. **Weeks 5-8: Hardware Integration** (EE + mechanical)
   - Design carrier PCB (radar + compute + comms + power)
   - Build solar power system with battery backup
   - Design weatherproof enclosure (IP67, 0-50°C)
   - Assemble 5 prototype units

4. **Weeks 6-10: Cloud + App Development** (full-stack developer)
   - AWS IoT device management + data pipeline
   - Activity heatmap visualization (per-field, per-block)
   - Daily pollination report generation
   - Hive placement optimization algorithm
   - Mobile app for field teams

5. **Weeks 8-12: Controlled Field Test** (team)
   - Deploy 5 units at 2-3 California almond orchards (pre-bloom prep)
   - Run alongside manual pollinator counts for ground truth
   - Validate range, accuracy, durability, connectivity
   - Iterate on filtering (wind, birds, large insects)

6. **Weeks 12-20: Bloom Season Pilot (Feb-March 2027)** (team)
   - Deploy 20 units across 5 grower partners
   - Provide daily pollination reports during 3-week bloom
   - Correlate radar activity data with fruit set results (measured at harvest)
   - Build case study: "Radar-guided hive moves → X% yield improvement"

---

## 5e. Validation Plan

**Target**: 5 almond growers, 20 radar units, during Feb-March 2027 bloom

**Key hypotheses**:
1. Radar detects pollinator activity with >90% correlation to manual counts
2. Under-pollinated zones identified by radar correlate with lower fruit set
3. Hive placement changes based on radar data improve pollination by ≥5%
4. Growers would pay $4K/unit + $500/month for pollination intelligence

**Go/no-go criteria**:
- GO: >85% correlation with manual counts AND at least one documented case of radar-guided hive move improving fruit set AND 4/5 growers want to continue
- NO-GO: <70% correlation OR no measurable improvement from recommendations OR growers see no value

---

## 5f. Timeline & Milestones

| Week | Milestone | Decision Point |
|------|-----------|----------------|
| 4 | Radar detects insects at required range | Range sufficient? |
| 8 | ML classifier >80% on US pollinator species | Accuracy sufficient? |
| 12 | 5 prototype units field-tested (pre-bloom) | Hardware durable? |
| 20 | Bloom season pilot complete (20 units) | Correlation validated? |
| 32 | Harvest data correlates with radar predictions | Product works? |
| 36 | 50 commercial units manufactured for 2028 season | Scale prep |

---

## 5g. Cost Estimate

| Category | Amount |
|----------|--------|
| Radar/DSP engineer (8 months) | $120,000 |
| ML engineer (6 months) | $90,000 |
| Full-stack developer (6 months) | $90,000 |
| Hardware prototyping (20 units) | $15,000 |
| PCB + enclosure engineering | $20,000 |
| Field deployment (travel, installation) | $15,000 |
| Cloud infrastructure (12 months) | $5,000 |
| Grower partner incentives | $10,000 |
| TI evaluation kits + test equipment | $5,000 |
| Legal + misc | $10,000 |
| **Total to bloom pilot validation** | **~$380,000** |
| Commercial batch (50 units manufacturing) | $30,000 |
| Sales + marketing for 2028 season | $20,000 |
| **Total to first revenue** | **~$430,000** |

**Monthly burn rate**: ~$50K (3 FTE)

**Funding strategy**: Pre-seed ($500K) targeting ag-tech investors. Strong fit for: Thrive (ag-tech VC), AgFunder, USDA SBIR Phase I ($275K for pollinator technology). BeeHero's $40M raise validates market for pollination data.

**Revenue projection (Year 1 post-bloom validation)**:
- 50 units × $4K = $200K hardware
- 50 units × $500/month × 3 months (bloom season) = $75K SaaS
- Consulting/optimization services: $50K
- **Year 1: ~$325K** (seasonal — 80% in Q1)

**Scale potential**: California has 1.3M almond acres needing 1 unit per 3 acres = 433K addressable units. Even 1% penetration = 4,330 units × $4K = $17M hardware + recurring SaaS.
