# 03 - Feasibility & Prototype: Autonomous UV-C Pest Control Robot Fleet

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FIELD DEPLOYMENT                              │
│                                                                     │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐       │
│  │   Robot 1    │     │   Robot 2    │     │   Robot N    │       │
│  │ ┌──────────┐ │     │              │     │              │       │
│  │ │GPS-RTK   │ │     │   (same)     │     │   (same)     │       │
│  │ │Receiver  │ │     │              │     │              │       │
│  │ ├──────────┤ │     └──────────────┘     └──────────────┘       │
│  │ │LiDAR +   │ │                                                   │
│  │ │Cameras   │ │     ┌──────────────┐                             │
│  │ ├──────────┤ │     │ RTK Base     │                             │
│  │ │Jetson    │ │     │ Station      │                             │
│  │ │Orin Nano │ │     │ (shared)     │                             │
│  │ ├──────────┤ │     └──────────────┘                             │
│  │ │UV-C LED  │ │                                                   │
│  │ │Arrays    │ │     ┌──────────────┐                             │
│  │ ├──────────┤ │     │ Charging     │                             │
│  │ │Bug Vacuum│ │     │ Dock         │                             │
│  │ │+ Zapper  │ │     └──────────────┘                             │
│  │ ├──────────┤ │                                                   │
│  │ │48V LiFe  │ │                                                   │
│  │ │PO4 Batt  │ │                                                   │
│  │ └──────────┘ │                                                   │
│  └──────────────┘                                                   │
└─────────────────────────────────────────────────────────────────────┘
                              │ 4G/LTE
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         CLOUD LAYER                                  │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │Fleet Manager │  │Pest Intel    │  │Grower        │            │
│  │(scheduling,  │  │(ML models,   │  │Dashboard     │            │
│  │ coordination)│  │ prediction)  │  │(maps, alerts)│            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| UV-C source | LED arrays (not mercury lamps) | Instant on/off, directional, durable, no warm-up |
| Navigation | GPS-RTK primary + LiDAR backup | ±2cm accuracy needed for row following; LiDAR for obstacles |
| Compute | Jetson Orin Nano | Sufficient for navigation + camera ML; low power |
| Power | 48V LiFePO4 100Ah | 8-10 hour runtime; safe chemistry for outdoor; 3000+ cycles |
| Connectivity | 4G LTE + local WiFi fallback | Rural areas have cellular; WiFi for base station area |
| Insect capture | UV-attraction + centrifugal fan + electrocution grid | Proven in pest traps; scale up for robot |
| Chassis | Custom aluminum frame, 4WD hub motors | Adjustable width for row spacing; IP65 weatherproofing |

---

## Bill of Materials (Single Robot Unit)

### Hardware BOM

| Component | Specification | Est. Cost | Confidence | Source |
|-----------|--------------|-----------|------------|--------|
| Chassis frame (aluminum, custom) | 1.2m × 0.8m, adjustable 0.6-1.2m width | $3,500 | ASSUMED | Custom fab quote needed |
| Hub motors (4x) + controllers | 4x 500W BLDC, IP65 | $2,800 | VERIFIED | ODrive + T-Motor |
| Wheels + suspension | 4x pneumatic ag tires, independent suspension | $1,200 | VERIFIED | Ag supply catalog |
| GPS-RTK receiver | u-blox ZED-F9P + antenna | $350 | VERIFIED | SparkFun/Digi-Key |
| RTK base station (amortized per 10 robots) | u-blox F9P base + radio link | $150 | VERIFIED | Per-robot share |
| LiDAR | Ouster OS0-32 (short range, wide FOV) | $2,500 | VERIFIED | Ouster pricing |
| Stereo cameras (2x) | Intel RealSense D435i | $700 | VERIFIED | Intel store |
| Compute | NVIDIA Jetson Orin Nano 8GB | $500 | VERIFIED | NVIDIA |
| UV-C LED arrays | 4x 100W UV-C modules (265nm, Nichia LEDs) | $4,000 | ASSUMED | Specialty supplier; price varies wildly |
| UV-C reflectors + housing | Custom aluminum parabolic | $800 | UNVERIFIED | Needs optical design |
| Bug vacuum system | Centrifugal fan + collection chamber + UV lure | $600 | ASSUMED | Modified commercial trap |
| Electrocution grid | High-voltage grid behind UV lure | $200 | VERIFIED | Bug zapper components |
| Battery pack | 48V 100Ah LiFePO4 (5.12 kWh) | $2,800 | VERIFIED | EG4/BattleBorn pricing |
| BMS + charger | 48V 30A BMS + 48V charger | $400 | VERIFIED | |
| Cellular modem | Sierra Wireless or Quectel 4G | $200 | VERIFIED | |
| Safety sensors | PIR (4x) + e-stop + beacon light | $300 | VERIFIED | |
| Weatherproof enclosure | IP65 aluminum housing for electronics | $1,200 | ASSUMED | Custom fab |
| Wiring, connectors, misc | Marine-grade connectors, cable management | $800 | ASSUMED | |
| **TOTAL PER ROBOT** | | **$23,000** | | |

### Confidence Assessment
- **VERIFIED** (actual supplier quotes or catalog prices): 60% of BOM
- **ASSUMED** (based on similar products, not directly quoted): 30% of BOM
- **UNVERIFIED** (engineering estimate, no source): 10% of BOM
- **Contingency recommended**: +25% ($5,750) → **$28,750 realistic per-unit cost**

### Infrastructure (One-Time / Shared)

| Item | Cost | Notes |
|------|------|-------|
| RTK base station (full) | $1,500 | Covers 10km radius |
| Charging dock (per 4 robots) | $3,000 | 4-bay, weatherproof |
| Field mapping equipment | $2,000 | Tablet + RTK rover for initial survey |
| Spare parts inventory | $5,000 | Motors, wheels, UV modules |

---

## Software Stack

| Layer | Technology | Build/Buy | Rationale |
|-------|-----------|-----------|-----------|
| Robot OS | ROS2 Humble (Ubuntu 22.04) | BUY | Industry standard; massive ecosystem |
| Navigation | Nav2 + GPS waypoint follower | BUY + CONFIGURE | Well-solved; RTK integration documented |
| Obstacle avoidance | LiDAR-based costmap + emergency stop | BUY (Nav2 built-in) | Standard ROS2 |
| UV-C dosing control | Custom ROS2 node | BUILD | Core IP — dose calculation based on speed + pest type |
| Pest detection | YOLOv8 on Jetson (camera-based) | BUILD | Identify pest presence, adjust treatment |
| Fleet coordination | Custom Python service (FastAPI) | BUILD | Multi-robot scheduling, path deconfliction |
| Cloud dashboard | React + PostgreSQL + Grafana | BUILD | Grower-facing; coverage maps, alerts |
| Data pipeline | MQTT → TimescaleDB → analytics | BUILD | Telemetry, pest data aggregation |
| ML pipeline | MLflow + PyTorch | BUILD | Pest prediction models, dosing optimization |

---

## Build Instructions (Detailed)

### Phase 0: Validation (Months 1-2) — $15,000

**Objective**: Prove UV-C kills target insects at achievable field doses before building anything.

1. Purchase benchtop UV-C LED setup (single 100W module + power supply): $1,500
2. Partner with UC Davis/Cal Poly entomology lab (consulting agreement): $10,000
3. Run controlled dose-response experiments:
   - Species: spider mites, thrips, whiteflies, aphids, spotted wing drosophila
   - Variables: UV-C intensity (mW/cm²), exposure time, distance
   - Measure: mortality at 24h, 48h, 72h (accounting for photoreactivation)
4. Determine minimum lethal dose for each species
5. Calculate: at robot speed of X mph, can we deliver lethal dose in single pass?

**GO/NO-GO GATE**: If minimum lethal dose requires >30 seconds exposure at 5cm distance, the concept is NOT viable for a moving robot. Must achieve kill at <5 second exposure to be practical at 0.5-1 mph.

**Confidence this gate passes: MEDIUM** — UV-C kills fungal spores in 2-3 second exposure (SAGA data). Insect kill likely requires higher dose. Spider mites (small, thin cuticle) likely susceptible; larger insects may require mechanical assist (vacuum).

### Phase 1: Single Robot Prototype (Months 2-5) — $85,000

1. **Chassis build** (Month 2-3):
   - Commission aluminum frame fabrication (local machine shop)
   - Integrate hub motors + ODrive controllers
   - Install suspension + ag tires
   - Wire 48V battery system + BMS
   - Target: robot drives under manual RC control

2. **Navigation integration** (Month 3-4):
   - Install Jetson Orin Nano + ROS2
   - Mount GPS-RTK receiver + LiDAR
   - Configure Nav2 for row-following using GPS waypoints
   - Add stereo cameras for visual row detection (backup)
   - Target: robot follows a row autonomously in open field

3. **UV-C integration** (Month 4-5):
   - Mount 4x UV-C LED arrays with reflectors
   - Build dosing controller (ROS2 node): intensity varies with speed
   - Add safety interlocks (PIR detection → instant UV shutoff)
   - Add bug vacuum system with UV lure
   - Target: robot drives row delivering calibrated UV-C dose

4. **Safety certification prep** (Month 5):
   - Document UV-C exposure levels at various distances
   - Implement multi-layer safety (PIR + geofence + physical kill switch + beacon)
   - Engage safety consultant for pre-assessment

### Phase 2: Field Trial (Months 5-8) — $60,000

1. Secure partner grower (free trial in exchange for data rights + testimonial)
2. Deploy single robot on 5-acre strawberry block
3. Establish control plots (untreated rows)
4. Run nightly treatments for 8-12 weeks
5. Measure: pest counts (sticky traps + visual), fruit quality, yield
6. Document everything for organic certification review

**GO/NO-GO GATE**: >50% pest reduction in treated vs. control with no crop damage.

### Phase 3: Fleet Prototype (Months 8-12) — $120,000

1. Build 3 additional robots (incorporating lessons from prototype)
2. Develop fleet management software (scheduling, coordination, monitoring)
3. Deploy multi-robot fleet at 2-3 grower sites
4. Validate fleet economics (coverage rate, maintenance needs, uptime)
5. Begin organic certification documentation process with USDA NOP

---

## Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| 1 | UV-C insufficient to kill insects at practical speeds | MEDIUM | FATAL | Phase 0 lab validation before any robot build; pivot to fungal-only if insects fail |
| 2 | Photoreactivation negates UV-C kill (insects repair DNA) | MEDIUM | HIGH | Night-only operation (4+ hours darkness post-treatment); higher dose; mechanical assist (vacuum) |
| 3 | TRIC Robotics captures market before us | MEDIUM | HIGH | Move fast; differentiate on multi-crop + fleet intelligence; target different geography initially |
| 4 | Robot durability in outdoor conditions (dust, rain, mud) | HIGH | MEDIUM | IP65 minimum; design for field serviceability; extensive environmental testing |
| 5 | Regulatory barriers (UV-C safety, autonomous vehicle rules) | LOW | HIGH | Engage regulatory counsel early; night-only + geofenced operation reduces human exposure risk |
| 6 | Seasonal revenue creates cash flow crisis | HIGH | HIGH | Service southern hemisphere clients (counter-seasonal); greenhouse clients (year-round); pre-season contracts |
| 7 | Grower adoption slower than expected | MEDIUM | HIGH | Free pilots; performance guarantees; partner with crop consultants as sales channel |
| 8 | John Deere acquires SAGA, enters market with massive resources | MEDIUM | MEDIUM | Build differentiated data/insect moat; position as complementary acquisition target |
| 9 | Robot damages crops (UV-C burns, mechanical contact) | LOW | HIGH | Conservative speed limits; crop distance sensors; extensive testing; insurance |
| 10 | IP litigation from SAGA or others | LOW | MEDIUM | FTO analysis before launch; focus on novel insect-kill methods (not just UV-C fungal) |

---

## Validation Plan

| Stage | Question | Method | Timeline | Success Criteria |
|-------|----------|--------|----------|-----------------|
| Lab validation | Does UV-C kill target insects? | Controlled exposure experiments | Month 1-2 | >80% mortality at <10 sec exposure |
| Single robot | Can we deliver dose autonomously? | Field prototype test | Month 5-6 | 10 acres/night, ±5cm row tracking |
| Field trial | Does it reduce pests in real conditions? | Treated vs. control plots | Month 6-8 | >50% pest reduction |
| Fleet trial | Can multiple robots coordinate? | Multi-robot deployment | Month 9-12 | 3 robots, 30+ acres, >95% uptime |
| Commercial pilot | Will growers pay? | Paid seasonal contract | Month 12-15 | 3+ paying customers |

---

## Cost & Time Estimate

### Total to First Revenue

| Phase | Timeline | Cost |
|-------|----------|------|
| Lab validation | Months 1-2 | $15,000 |
| Single robot prototype | Months 2-5 | $85,000 |
| Field trial | Months 5-8 | $60,000 |
| Fleet prototype (3 more robots) | Months 8-12 | $120,000 |
| Personnel (12 months, 3 people min) | Months 1-12 | $450,000 |
| Ops, legal, insurance, travel | Months 1-12 | $70,000 |
| **Subtotal** | | **$800,000** |
| Contingency (20%) | | $160,000 |
| **Total** | **12-15 months** | **$960,000** |

### Minimum Viable Team

| Role | Type | Annual Cost | Critical Because |
|------|------|-------------|-----------------|
| Robotics/controls engineer | Full-time hire | $170,000 | Navigation, autonomy, hardware integration |
| Agricultural scientist | Part-time / advisor | $60,000 | UV-C dosing protocols, field trial design, pest biology |
| Founder (you) — fleet software + ops | Full-time | $130,000 | Dashboard, fleet management, business development |
| Electrical/mechanical contractor | Contract | $90,000 | Chassis fab, UV array design, weatherproofing |

---

## Founder-Market Fit Assessment

**Founder profile**: AI/ML infrastructure engineer, deep Python/systems/cloud expertise, no hardware/robotics/agriculture background.

| Dimension | Fit | Gap | Mitigation |
|-----------|-----|-----|------------|
| Fleet management software | STRONG | None | Cloud, distributed systems, monitoring — directly applicable |
| ML/AI pest intelligence | STRONG | None | ML pipeline, model deployment — core skill |
| Data platform (pest analytics) | STRONG | None | ETL, analytics, dashboards — routine |
| Robot navigation/autonomy | WEAK | ROS2, control theory, sensor fusion | Hire robotics engineer (critical first hire) |
| Electrical/hardware design | WEAK | PCB design, power systems, UV optics | Contract electrical engineer |
| Agriculture domain knowledge | WEAK | Agronomy, pest biology, grower relationships | Hire/advise with ag scientist; embed with growers |
| Mechanical engineering | WEAK | Chassis design, weatherproofing, durability | Contract mechanical engineer |
| Regulatory (UV safety, autonomous vehicles) | WEAK | FDA/EPA/OSHA UV regulations | Engage specialized counsel |
| Sales to farmers | WEAK | Trust-building, seasonal sales cycle, channel partnerships | Partner with crop consultants; attend ag trade shows |

### Honest Assessment

**Founder-market fit: 3/10**

The founder's strengths (cloud infrastructure, ML, Python) map to ~30% of the challenge. The hardest 70% — ruggedized outdoor robotics, agricultural science, farmer sales relationships, hardware manufacturing — are outside the founder's experience.

**This is a hardware + deep-domain company being started by a software person.** History shows this CAN work (Tesla, Carbon Robotics) but requires:
1. Exceptional hiring of hardware/domain leads in first 6 months
2. Willingness to be in fields, not behind a keyboard
3. 2-3x longer timeline than a pure-software startup
4. Significantly more capital due to hardware iteration cycles

**Honest recommendation**: This idea is better suited for a founder with robotics/ag background who needs a software co-founder. If proceeding solo, the MVP should maximize software differentiation (fleet intelligence, pest prediction) while outsourcing/contracting all hardware build.
