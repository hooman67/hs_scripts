# 03 Feasibility & Prototype Plan: Livestock GPS+Health Tags with Satellite Backhaul

## Architecture Overview

```
[Ear Tag Hardware] --> BLE --> [Hubble Network Satellite] --> [Ground Station] --> [Cloud Backend] --> [Mobile/Web App]

Ear Tag:
  nRF52840 (BLE SoC + application processor)
  u-blox MAX-M10S (GPS receiver)
  LIS2DH12 (accelerometer)
  Coin cell battery (CR2477 or custom LiMnO2)
  PCB antenna (BLE + GPS)

Cloud:
  AWS IoT Core (device management, MQTT)
  AWS Lambda / ECS (data processing)
  PostgreSQL + TimescaleDB (time-series location/activity)
  React Native mobile app
  React web dashboard
```

**Data flow:**
1. GPS fix acquired every 4 hours (configurable). Accelerometer samples continuously at 10Hz, processed on-device to activity classification.
2. nRF52840 transmits compressed payload (~50 bytes: lat/lon/alt/activity_summary/battery/alert_flags) via BLE to Hubble satellite overhead.
3. Hubble ground station relays to cloud endpoint.
4. Cloud processes, stores, runs anomaly detection, triggers alerts.
5. User receives push notification and views dashboard.

## Bill of Materials (Single Unit)

| Component | Part Number | Function | Unit Cost | Confidence |
|-----------|-------------|----------|-----------|------------|
| MCU/BLE SoC | Nordic nRF52840 | Application processor + BLE 5.0 radio | $3.50 | VERIFIED (DigiKey, qty 1000) |
| GPS Module | u-blox MAX-M10S | GNSS receiver (GPS+GLONASS), low power | $8.50 | VERIFIED (DigiKey, qty 1000) |
| Accelerometer | ST LIS2DH12 | 3-axis MEMS, ultra-low power (2uA) | $0.85 | VERIFIED (DigiKey, qty 1000) |
| Battery | Renata CR2477N (950mAh) | Primary coin cell, -40 to +85C | $1.20 | VERIFIED |
| GPS Antenna | Ceramic patch 18x18mm | Passive GPS antenna | $0.80 | ASSUMED (Alibaba, qty 5000) |
| BLE Antenna | PCB trace antenna | Integrated on PCB, tuned for 2.4GHz | $0.00 | VERIFIED (design cost only) |
| PCB | 4-layer FR4, 30x40mm | Custom board | $1.50 | ASSUMED (JLCPCB, qty 1000) |
| Enclosure | Custom injection-molded polyurethane | IP68, UV-resistant, ear-tag form factor | $3.50 | ASSUMED (quotes needed) |
| Ear tag hardware | Titanium pin + retainer | Standard livestock tag attachment | $1.20 | ASSUMED (supplier quotes needed) |
| Passive components | Resistors, capacitors, crystals | Supporting circuitry | $1.50 | ASSUMED |
| Assembly (SMT) | Pick-and-place + reflow | Contract manufacturing | $2.50 | ASSUMED (PCBWay/similar, qty 1000) |
| Testing/QC | Functional test + waterproofing | Per-unit testing | $1.00 | ASSUMED |
| **TOTAL BOM** | | | **$26.05** | |

**Critical note on satellite modem:** The proposed architecture uses nRF52840's native BLE radio to communicate with Hubble Network satellites. There is NO separate satellite modem — Hubble's innovation is receiving standard BLE signals from orbit. This is what makes the BOM $26 instead of $80+. However, this is UNVERIFIED at commercial scale. Hubble has demonstrated the concept but has not shipped a commercial satellite service.

**Battery life calculation (ASSUMED — needs validation):**
- CR2477: 950mAh capacity
- GPS fix (MAX-M10S): ~25mA for 30 seconds = 0.21mAh per fix
- 6 fixes/day = 1.26mAh/day for GPS
- BLE transmission: ~15mA for 2 seconds per uplink = 0.008mAh per transmission
- 6 transmissions/day = 0.05mAh/day
- Accelerometer (LIS2DH12): 2uA continuous = 0.048mAh/day
- MCU sleep: 1.5uA = 0.036mAh/day
- MCU active (processing): ~5mA for 10 seconds per wake = 0.014mAh per wake, 6 wakes/day = 0.08mAh/day
- **Total daily consumption: ~1.47mAh/day**
- **Theoretical battery life: 950/1.47 = 646 days (~1.8 years)**
- **With 70% battery efficiency in temperature extremes: ~450 days (~1.2 years)**

**Conclusion:** 2-year battery life claim is OPTIMISTIC. Realistic estimate is 1.2-1.5 years with 6 GPS fixes/day. Reducing to 4 fixes/day could extend to ~1.6 years. A larger custom LiMnO2 cell (1500mAh) would achieve 2 years but adds $2-3 to BOM and increases form factor.

## Software Stack

| Layer | Technology | License | Cost |
|-------|-----------|---------|------|
| Firmware | Zephyr RTOS + nRF Connect SDK | Apache 2.0 | Free |
| Firmware build | nRF Connect for VS Code | Nordic proprietary (free) | Free |
| Cloud IoT | AWS IoT Core | Commercial | ~$0.001/message |
| Backend | Python (FastAPI) on AWS Lambda/ECS | MIT | AWS compute costs |
| Database | PostgreSQL + TimescaleDB | Apache 2.0 / Timescale License | AWS RDS costs |
| Mobile App | React Native | MIT | Free |
| Web Dashboard | React + Mapbox GL JS | MIT / Mapbox ToS | Mapbox: $0.60/1000 map loads |
| Analytics | Python (scikit-learn, NumPy) | BSD | Free |
| CI/CD | GitHub Actions | Commercial | Free tier sufficient initially |
| Device OTA | MCUboot + Zephyr DFU | Apache 2.0 | Free |

## Step-by-Step Prototype Build Plan

### Phase 1: Proof of Concept — BLE + GPS (Weeks 1-4, $2,500)

1. **Week 1:** Order development hardware
   - Nordic nRF52840-DK ($40)
   - u-blox MAX-M10S EVK ($50)
   - ST LIS2DH12 breakout board ($15)
   - Breadboard, jumper wires, logic analyzer
   
2. **Week 2:** Firmware development (dev kit)
   - Set up Zephyr RTOS development environment
   - Implement GPS acquisition and power management
   - Implement accelerometer sampling and on-device activity classification
   - Implement BLE advertising with custom payload format

3. **Week 3:** Integration and power profiling
   - Integrate all sensors on breadboard
   - Measure actual power consumption per operational mode
   - Validate battery life projections with real measurements
   - Optimize GPS cold/warm start times

4. **Week 4:** Field test (BLE range and GPS accuracy)
   - Test GPS accuracy in open rangeland conditions
   - Test BLE transmission range (terrestrial receiver as satellite proxy)
   - Validate accelerometer-based activity classification against known cattle behaviors (use YouTube cattle behavior videos as proxy initially)

### Phase 2: Hubble Network Integration (Weeks 5-8, $5,000)

5. **Week 5-6:** Hubble Network developer engagement
   - Apply for Hubble Network developer program
   - Obtain SDK/API documentation
   - Understand BLE advertising format requirements for satellite reception
   - **CRITICAL GATE:** If Hubble satellite is not yet commercially available, this phase BLOCKS. Fallback: test with Hubble terrestrial network in urban area to validate data flow.

6. **Week 7-8:** End-to-end data path validation
   - Transmit from nRF52840 DK → Hubble Network → Cloud
   - Validate message delivery reliability, latency, and cost per message
   - Implement cloud backend (AWS IoT Core → Lambda → PostgreSQL)
   - Build minimal web dashboard showing device location on map

### Phase 3: Custom PCB & Enclosure (Weeks 9-16, $15,000)

7. **Week 9-11:** PCB design
   - Schematic capture in KiCad (4-layer board)
   - Layout optimization for antenna performance
   - Design for manufacturability (DFM) review
   - Order prototype PCBs (JLCPCB, 5-10 units, $500)

8. **Week 12-13:** PCB assembly and bring-up
   - SMT assembly (hand-soldering prototype or use PCB assembly service)
   - Functional validation of each subsystem
   - Power consumption verification vs. dev kit measurements
   - RF testing (BLE output power, GPS sensitivity)

9. **Week 14-16:** Enclosure design and prototyping
   - 3D-printed enclosure for cattle-ear-tag form factor
   - IP68 waterproofing validation (submersion test)
   - Mechanical attachment design (compatible with standard tag applicators)
   - Environmental testing: -30C to +60C operation (freezer + heat gun)
   - **Note:** Production injection molding tooling is $10-30K; use 3D printing for prototype only

### Phase 4: Field Trial (Weeks 17-24, $10,000)

10. **Week 17-18:** Obtain cattle field trial partnership
    - Partner with local rancher or university agricultural extension (e.g., Montana State, Texas A&M)
    - Apply for any necessary animal research permits
    - Install 10-20 tags on cattle

11. **Week 19-24:** 6-week monitored field trial
    - Daily data validation: GPS accuracy, message delivery rate, battery drain
    - Weekly: physical tag inspection (attachment integrity, damage)
    - Collect ground-truth behavioral data for activity classification validation
    - Iterate firmware based on real-world performance

## Risk Register

| # | Risk | Likelihood | Impact | Mitigation | Fallback |
|---|------|-----------|--------|------------|----------|
| 1 | Hubble satellite not commercially available | HIGH | CRITICAL | Early engagement with Hubble; parallel evaluation of Kineis/Lacuna Space | Pivot to LoRa mesh + gateway (abandons "no infrastructure" value prop) |
| 2 | Hubble pricing higher than $1/device/month | MEDIUM | HIGH | Negotiate volume commitment; pre-pay for locked rates | Absorb cost, raise subscription to $5/month (still cheaper than cellular) |
| 3 | BLE signal too weak for satellite reception from ear-tag PCB antenna | MEDIUM | CRITICAL | Optimize antenna design; consult RF engineer; test multiple antenna configurations | External antenna stub (degrades form factor) |
| 4 | Battery life <1 year in field conditions | MEDIUM | HIGH | Reduce GPS frequency; use larger cell; implement adaptive scheduling | Solar supplementation (adds cost, mimics Ceres Tag approach) |
| 5 | Ear tag retention failure (cattle pull them out) | LOW-MEDIUM | MEDIUM | Use proven tag attachment mechanisms from Allflex/Y-Tex; field trial validates | Redesign attachment; explore secondary retention clip |
| 6 | Ceres Tag or Allflex launches identical product at lower price during development | MEDIUM | HIGH | Accelerate timeline; focus on niche differentiation (AI health analytics) | Pivot to software-only platform that integrates with multiple tag vendors |
| 7 | GPS accuracy insufficient under tree cover / terrain | LOW | MEDIUM | u-blox MAX-M10S supports multi-constellation; test in varied terrain | Add dead-reckoning from accelerometer data |
| 8 | Manufacturing scale-up quality issues | MEDIUM | MEDIUM | Partner with experienced IoT contract manufacturer (e.g., Flex, Jabil for volume; PCBWay for early runs) | Over-engineer early batches; accept higher BOM cost initially |
| 9 | Regulatory (FCC Part 15 certification) delays | LOW-MEDIUM | MEDIUM | Begin FCC testing at Phase 3; use pre-certified modules where possible | Budget $15-20K and 3-4 months for certification |
| 10 | Rancher adoption resistance (technology skepticism) | MEDIUM | MEDIUM | Partner with cattlemen's associations; use trusted rancher influencers; offer money-back guarantee | Focus on progressive early-adopter ranchers only |

## Validation Plan

### Success Criteria

| Metric | Target | How to Measure |
|--------|--------|----------------|
| GPS accuracy | <10m CEP in open terrain | Compare tag position vs. known ground-truth locations |
| Message delivery rate | >95% of scheduled transmissions received | Cloud message count vs. expected count |
| Battery life | >365 days in field conditions | Continuous voltage monitoring; extrapolate from 6-week trial |
| Activity classification accuracy | >80% agreement with visual observation | Video-annotated ground truth vs. tag classification |
| Tag retention | >98% over 6-week trial | Physical inspection count |
| Rancher satisfaction | >4/5 on "would recommend" | Post-trial survey |
| Data latency | <30 minutes from transmission to dashboard | Timestamp comparison |

### Timeline

| Phase | Duration | Cost | Key Deliverable |
|-------|----------|------|-----------------|
| Phase 1: PoC | 4 weeks | $2,500 | Working BLE+GPS+accel on dev kit with validated power budget |
| Phase 2: Connectivity | 4 weeks | $5,000 | End-to-end data path through Hubble (or validated terrestrial proxy) |
| Phase 3: Hardware | 8 weeks | $15,000 | 20 custom PCB prototypes in waterproof enclosures |
| Phase 4: Field Trial | 8 weeks | $10,000 | 6-week cattle deployment with performance data |
| **Total** | **24 weeks** | **$32,500** | **Validated prototype ready for manufacturing scale-up pitch** |

### Post-Prototype to Revenue (additional)

| Phase | Duration | Cost | Key Deliverable |
|-------|----------|------|-----------------|
| FCC Certification | 12-16 weeks | $15,000-25,000 | Part 15 certification |
| Manufacturing tooling | 8-12 weeks | $30,000-50,000 | Injection molds, test jigs, assembly line setup |
| First production run (1,000 units) | 8-12 weeks | $50,000-80,000 | Shippable product |
| Go-to-market | 4-8 weeks | $20,000-30,000 | Website, sales materials, first customer onboarding |
| **Total to first revenue** | **~12 months** | **$150,000-$190,000** | |

## Total Cost and Time Estimate

| Milestone | Cumulative Cost | Cumulative Time |
|-----------|----------------|-----------------|
| Prototype validated | $32,500 | 6 months |
| Manufacturing-ready | $80,000-$110,000 | 9 months |
| First units shipping | $150,000-$190,000 | 12 months |
| 1,000 customers (break-even trajectory) | $300,000-$350,000 | 18 months |

**Total capital required to reach revenue: ~$190K-$345K** (consistent with stated $345K estimate, which likely includes working capital for first production run + 6 months operations).

## Founder-Market Fit Assessment

**Founder profile:** Hooman Shariati — AI/ML infrastructure engineer at Adobe, deep Python/systems/cloud expertise, no hardware background, no livestock industry connections.

| Dimension | Score (1-10) | Assessment |
|-----------|-------------|------------|
| Technical (software/cloud) | 9/10 | Strong: Backend, cloud infrastructure, ML/AI are directly applicable to cloud platform and future health analytics |
| Technical (hardware) | 2/10 | Weak: No PCB design, RF engineering, or embedded firmware experience. Would need to hire or contract. |
| Technical (embedded/firmware) | 3/10 | Weak: Systems programming helps, but Zephyr RTOS + BLE + GPS power management is specialized |
| Domain knowledge | 1/10 | None: No ranching, agriculture, or livestock industry experience |
| Customer access | 1/10 | None: No existing relationships with ranchers, cattlemen's associations, or ag distributors |
| Manufacturing | 1/10 | None: No hardware manufacturing, supply chain, or contract manufacturing experience |
| Regulatory | 2/10 | Low: No FCC certification or agricultural device regulatory experience |
| Fundraising/pitch | 6/10 | Moderate: Adobe/tech background is credible but agtech investors want domain expertise |

**Overall founder-market fit: 2.5/10 — POOR**

**Critical gaps:**
1. Hardware engineering (PCB, RF, mechanical) — must hire or find co-founder
2. Livestock industry domain expertise — must partner or hire
3. Manufacturing and supply chain — must outsource entirely
4. Customer access — no warm introductions possible

**Honest assessment:** This is a hardware + deep-domain product being pursued by a software engineer with zero relevant industry connections. The cloud backend and future AI analytics are strong fits, but they represent perhaps 20% of the total challenge. The other 80% (hardware engineering, manufacturing, livestock domain, regulatory, customer access) are all founder weaknesses. A strong technical co-founder with embedded/RF expertise AND an industry advisor/co-founder with ranching connections would be minimum requirements.
