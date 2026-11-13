# Feasibility & Prototype Plan: Remote Dryland Farm Soil Monitoring (Satellite)

## System Architecture

```
[Soil Probe]                    [Satellite Layer]           [Cloud]              [User]
                                                                                  
 Capacitive Sensor ─┐                                                            
 Temperature Sensor ─┼─► nRF52840 ──BLE──► Hubble ──► Hubble ──► AWS IoT ──► Web App
                     │    (MCU +         Satellite    Cloud       Core       Mobile App
                     │     BLE radio)    Constellation  API                   SMS Alerts
 Battery ────────────┘                                    │
 (Li-SOCl2, 5yr)                                         ▼
                                                    DynamoDB / TimeSeries
                                                         │
                                                         ▼
                                                    Alert Engine
                                                    (Lambda)
```

**Key architectural decision**: No gateway. Each probe communicates directly to satellite via BLE (Hubble Network protocol). This eliminates all ground infrastructure requirements and is the core differentiator.

**Data flow**:
1. Probe wakes from sleep every 6 hours
2. Takes capacitive moisture reading at 2 depths + temperature
3. Encodes into compact BLE advertising packet (≤20 bytes)
4. Transmits BLE advertisement for satellite window (~10 minutes)
5. Returns to deep sleep
6. Hubble satellite receives, forwards to ground station → Hubble API
7. Our backend ingests via webhook, stores, evaluates alert rules
8. User sees data on next app open or receives alert if threshold crossed

**Message format** (20 bytes):
- Device ID: 4 bytes
- Timestamp (offset): 2 bytes
- Moisture depth 1 (raw ADC): 2 bytes
- Moisture depth 2 (raw ADC): 2 bytes
- Temperature: 2 bytes
- Battery voltage: 1 byte
- Status flags: 1 byte
- CRC: 2 bytes
- Reserved: 2 bytes

---

## Bill of Materials (Per Probe, at 1,000 unit volume)

| Component | Specific Part | Unit Cost | Confidence | Notes |
|-----------|--------------|-----------|------------|-------|
| MCU + BLE SoC | Nordic nRF52840 | $4.50 | VERIFIED (DigiKey) | Runs application + BLE radio. Same as livestock tags. |
| Capacitive soil moisture sensor (depth 1) | Custom PCB capacitive | $2.00 | VERIFIED | Proven design (similar to Chirp!, $2-3 at volume) |
| Capacitive soil moisture sensor (depth 2) | Custom PCB capacitive | $2.00 | VERIFIED | Second electrode pair on same flex PCB |
| Temperature sensor | TMP117 (TI) | $1.50 | VERIFIED (DigiKey) | 0.1C accuracy, I2C, ultra-low power |
| Satellite modem/firmware | Hubble Network BLE protocol | $0.00-1.00 | ASSUMED | Uses standard nRF52840 BLE radio with Hubble firmware. No additional hardware. Hubble's model is "software on standard BLE chip." Cost is per-message, not hardware. |
| Battery | Saft LS14500 (Li-SOCl2, AA, 3.6V, 2600mAh) | $4.00 | VERIFIED | -60C to +85C. 10-year shelf life. Single cell sufficient for 4-5 year operation at 4 tx/day. |
| Antenna | PCB trace antenna (BLE 2.4GHz) | $0.10 | VERIFIED | Integrated on PCB. No discrete component needed for BLE. |
| Custom PCB (rigid-flex) | 4-layer rigid section + flex tail for sensors | $3.00 | ASSUMED | Rigid head (electronics) + flex tail (capacitive sensors at 2 depths). JLCPCB/PCBWay. |
| Passive components | Caps, resistors, ESD protection | $1.00 | VERIFIED | Standard BOM |
| Enclosure | Injection-molded HDPE tube (IP68) | $2.50 | ASSUMED | Simple tube with sealed cap. Cheaper than ear-tag (no animal-safe requirements). |
| O-rings + sealing | Silicone O-ring + epoxy potting | $0.50 | VERIFIED | Standard IP68 technique |
| Assembly + test | Contract manufacturing (Shenzhen) | $3.00 | ASSUMED | Per unit at 1K volume. Includes functional test. |
| Conformal coating | Parylene or acrylic spray | $0.50 | VERIFIED | Moisture protection for electronics |
| **TOTAL BOM** | | **$24.60-25.60** | | |

**Landed cost** (shipping, packaging, QC, yield loss): ~$32-35/unit
**Target retail price**: $99
**Hardware gross margin**: ~65%

### Confidence Summary
- VERIFIED (from distributor pricing/datasheets): $16.10 (65% of BOM)
- ASSUMED (reasonable estimates, need quotes): $8.50 (35% of BOM)
- UNVERIFIED: $0 — no exotic/unknown components

### BOM comparison to livestock tags
Soil probe is SIMPLER than livestock tag because:
- No GPS module needed (probe is stationary; location set at install) — saves $9
- No accelerometer needed — saves $0.80
- No complex enclosure (stationary tube vs. animal-worn tag) — saves $1-2
- Same MCU, same satellite connectivity, same battery chemistry

---

## Software Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Firmware | Zephyr RTOS on nRF52840 | Same as livestock tags. Ultra-low-power framework. Nordic's reference platform. |
| Firmware - BLE | Hubble Network SDK | Handles satellite-optimized BLE advertising protocol |
| Firmware - Sensor | Custom ADC driver | Read capacitive sensor frequency/voltage, apply calibration curve |
| Cloud ingestion | AWS IoT Core | Managed MQTT/HTTP device ingestion. Scales to millions. |
| Data store | AWS Timestream (or DynamoDB) | Time-series optimized. Cheap at low write volumes. |
| Alert engine | AWS Lambda + EventBridge | Threshold evaluation on each new reading. Stateless, pay-per-use. |
| Notifications | AWS SNS (SMS) + SendGrid (email) + Firebase (push) | Multi-channel alerts |
| API | FastAPI on AWS Lambda (or ECS) | Python. REST API for app consumption. |
| Web dashboard | React + Leaflet (map) + Recharts | Lightweight. Map view with probe locations. Time-series charts. |
| Mobile app | React Native | Cross-platform iOS/Android from single codebase |
| Calibration service | Python + scikit-learn | Per-soil-type calibration curves (capacitive ADC → volumetric moisture %) |

**Firmware power budget**:
- Deep sleep: 1.5 uA (nRF52840 system OFF mode)
- Sensor reading: 5 mA for 100ms = 0.14 uAh per reading
- BLE transmission (satellite window): 8 mA for 10 minutes = 1.33 mAh per transmission
- Daily consumption: 4 readings x (0.14 uAh + 1.33 mAh) = ~5.3 mAh/day + 0.036 mAh sleep = ~5.34 mAh/day
- Battery capacity: 2600 mAh (LS14500)
- **Projected life: 2600 / 5.34 = ~487 days = 1.3 years**

**ISSUE**: 10-minute BLE window is too power-hungry. Must reduce to 2-3 minutes or use Hubble's optimized scheduling.
- With 3-minute window: 8mA x 3min = 0.4 mAh per tx → 1.6 mAh/day → **4.4 years** battery life
- **Confidence: MEDIUM** — depends on Hubble's actual required transmission window

---

## Build Instructions (Prototype to Pilot)

### Phase 1: Proof of Concept (Weeks 1-4) — $15K

**Goal**: Validate BLE-to-satellite soil data delivery

1. **Week 1**: Order nRF52840-DK dev board + Hubble Network dev kit + capacitive soil sensor breakout boards (off-shelf: DFRobot SEN0193 or similar)
2. **Week 2**: Write basic firmware:
   - Read capacitive sensor ADC value
   - Read temperature (TMP117 on I2C)
   - Format 20-byte payload
   - Transmit via BLE advertising (Hubble protocol)
3. **Week 3**: Deploy outdoors in soil. Verify:
   - Satellite message delivery (does Hubble receive it?)
   - Sensor readings correlate with known moisture (pour water, verify reading increases)
   - Power consumption measurement (Nordic Power Profiler Kit)
4. **Week 4**: Build minimal cloud endpoint (webhook receiver → DynamoDB → simple web page showing values)

**Decision gate**: Does Hubble actually deliver messages reliably? If NO → project stops.

### Phase 2: Custom Hardware (Weeks 5-10) — $25K

**Goal**: Design PCB optimized for soil deployment

5. **Week 5-6**: Schematic + PCB layout
   - Rigid-flex design: 30mm diameter rigid head (electronics) + 500mm flex tail (capacitive sensor electrodes at 150mm and 450mm)
   - Capacitive sensor design: interdigitated copper traces on flex PCB with polyimide substrate
   - Power: single LS14500 Li-SOCl2 cell with LDO (TPS7A02 — 25nA quiescent)
6. **Week 7**: Order PCB prototypes (JLCPCB, 5-day turn) + components (DigiKey/Mouser)
7. **Week 8**: Assemble 10 prototype boards (hand solder or local PCBA)
8. **Week 9**: Bench testing:
   - Power consumption vs. budget
   - Sensor calibration in known moisture samples (sand, loam, clay at 0%, 10%, 25%, 40% VWC)
   - BLE range test (in-soil attenuation)
9. **Week 10**: Environmental testing:
   - Waterproof enclosure validation (24hr submersion)
   - Temperature cycling (-20C to +60C)
   - UV exposure (enclosure material only)

**Decision gate**: Does custom hardware meet power/accuracy/durability targets?

### Phase 3: Firmware + Cloud (Weeks 8-14) — $30K

10. **Weeks 8-10**: Production firmware
    - Zephyr RTOS port with full power management
    - OTA update capability (via BLE during maintenance window)
    - Calibration curve storage (per-device factory calibration)
    - Watchdog + fault recovery
11. **Weeks 10-12**: Cloud backend
    - Device provisioning + management
    - Time-series storage with retention policies
    - Alert rule engine (per-device thresholds)
    - REST API for app
12. **Weeks 12-14**: Mobile app MVP
    - Map view with probe locations
    - Moisture time-series charts
    - Alert configuration
    - Device setup (QR scan → register)

### Phase 4: Enclosure + Manufacturing (Weeks 12-16) — $30K

13. **Weeks 12-14**: Enclosure design
    - HDPE tube, 35mm diameter x 550mm length
    - Sealed with marine-grade epoxy potting at electronics end
    - Pointed tip for soil insertion
    - Solar shield cap (prevents surface heating artifact)
14. **Week 14**: 3D print 20 prototypes for field testing
15. **Week 15-16**: Source injection mold tooling ($8-12K for simple tube mold)

### Phase 5: Field Pilot (Weeks 16-28) — $40K

16. **Week 16**: Deploy 50 probes across 5 Australian farms
17. **Weeks 16-28**: Monitor for 3 months:
    - Message delivery rate (target: >93%)
    - Battery consumption tracking
    - Sensor accuracy vs. manual soil samples (gravimetric validation)
    - Farmer engagement (app usage, alert response)
18. **Week 28**: Analyze results, iterate firmware/calibration

---

## Risk Register

| # | Risk | Likelihood | Impact | Mitigation | Residual Risk |
|---|------|-----------|--------|------------|---------------|
| 1 | Hubble Network fails to achieve coverage over Australia/US | MEDIUM | FATAL | Monitor Hubble's constellation deployment progress. Have contingency to switch to Kineis/Myriota (requires hardware redesign with separate radio module). | HIGH — no cheap mitigation exists |
| 2 | BLE signal does not propagate from 15-45cm underground through soil | MEDIUM | HIGH | Antenna design: keep BLE antenna at top of probe (surface level). Only sensor electrodes go deep. Test in wet vs. dry soil. | MEDIUM — solvable with antenna placement |
| 3 | Capacitive sensor accuracy degrades in saline/clay soils | MEDIUM | MEDIUM | Implement soil-type calibration curves. Factory calibration + field correction using farmer-reported soil type. Well-known limitation of capacitive sensors. | LOW — known problem with known solutions |
| 4 | Farmers do not value moisture data enough at $5/month (dryland demand risk) | MEDIUM | HIGH | Validate during pilot with willingness-to-pay interviews. Add value via planting recommendations, not just raw data. Bundle with carbon credit documentation. | MEDIUM — may need to adjust value proposition |
| 5 | Battery life shorter than projected (Hubble requires longer TX windows) | LOW-MEDIUM | MEDIUM | Use larger battery (D-cell Li-SOCl2, 19Ah) if needed. Or reduce to 2x daily readings. Cost increase ~$5/probe. | LOW — solvable with larger battery |
| 6 | Myriota/Lacuna achieve market dominance before we scale | MEDIUM | HIGH | Move fast. Target markets Myriota is not focused on (Africa, Central Asia). Build agronomic intelligence layer as differentiation beyond connectivity. | MEDIUM — speed is only defense |
| 7 | Animal/machinery damage to probes in field | LOW | LOW | Probe sits flush with ground (only cap visible). Low profile. Offer replacement warranty. Known farming risk. | LOW |
| 8 | Regulatory (radio emissions, satellite spectrum) | LOW | MEDIUM | Hubble handles spectrum licensing. BLE 2.4GHz is ISM band (license-free globally). No probe-side regulatory risk. | LOW |

---

## Validation Plan

### Hypotheses to test (in priority order)

1. **Connectivity works**: Hubble satellite receives BLE messages from probe at ground level in open-sky agricultural setting
   - Test: Deploy 10 probes, measure message delivery rate over 30 days
   - Pass: >90% delivery rate
   - Fail: <70% delivery rate

2. **Accuracy is actionable**: Capacitive readings correlate with actual volumetric water content within +/- 5% VWC
   - Test: Co-locate probes with gravimetric soil samples (gold standard)
   - Pass: R-squared > 0.85 across soil types
   - Fail: R-squared < 0.70

3. **Farmers engage**: Pilot farmers check dashboard at least weekly and find data useful
   - Test: App analytics + post-pilot survey
   - Pass: 4/5 farmers rate "useful" or "very useful" AND check weekly
   - Fail: <3/5 engaged

4. **Willingness to pay**: Farmers would pay $5/month per probe
   - Test: Van Westendorp price sensitivity survey + actual pilot conversion
   - Pass: >60% say "acceptable" at $5/month
   - Fail: <40% say "acceptable"

5. **Battery life**: Actual consumption matches projected 3+ year life
   - Test: Measure current draw over 90 days, extrapolate
   - Pass: Projected life >30 months
   - Fail: Projected life <18 months

---

## Cost & Time Estimate

| Phase | Duration | Cost | Cumulative |
|-------|----------|------|-----------|
| Phase 1: Proof of Concept | 4 weeks | $15,000 | $15,000 |
| Phase 2: Custom Hardware | 6 weeks | $25,000 | $40,000 |
| Phase 3: Firmware + Cloud | 7 weeks | $30,000 | $70,000 |
| Phase 4: Enclosure + Mfg | 5 weeks | $30,000 | $100,000 |
| Phase 5: Field Pilot | 12 weeks | $40,000 | $140,000 |
| Personnel (1 EE + 1 SW, 7 months) | — | $140,000 | $280,000 |
| Contingency (10%) | — | $20,000 | $300,000 |
| **Total to validated pilot** | **~7 months** | **$300,000** | |

**Post-pilot to first revenue** (additional):
- First production run (500 units): $20,000
- Marketing/sales: $15,000
- Regulatory/certification: $5,000
- **Additional: $40,000**

**Total to first revenue: ~$340,000** (within $300K budget if personnel costs are founder sweat equity)

**Time to first revenue**: ~10 months from start (7 months to validated pilot + 3 months to manufacture and sell)

---

## Founder-Market Fit Assessment

**Founder profile**: AI/ML infrastructure engineer. Deep Python/systems/cloud. No hardware background.

### Strengths (for this venture)
| Area | Relevance | Fit Score |
|------|-----------|-----------|
| Cloud/backend architecture | Critical for data pipeline, API, alerting | 9/10 |
| Python/ML | Important for calibration algorithms, data analysis | 8/10 |
| Systems engineering | Good for firmware logic (not hardware design) | 7/10 |
| Infrastructure scaling | Important for 10K+ device fleet management | 9/10 |
| Data platform design | Future moat (agronomic intelligence) | 9/10 |

### Weaknesses (gaps to fill)
| Area | Criticality | Gap Size | Mitigation |
|------|-------------|----------|------------|
| Hardware/EE design | HIGH (PCB, antenna, sensor) | LARGE | Hire contract EE ($50-80/hr) or find EE co-founder. Cannot self-serve. |
| Embedded firmware (Zephyr/RTOS) | HIGH | MEDIUM | Can learn (Python → C is bridgeable), but Zephyr ecosystem has learning curve. Hire embedded developer for first 6 months. |
| Agricultural domain knowledge | MEDIUM | LARGE | Partner with agronomist. Join farming communities (GrainGrowers, GRDC in Australia). Spend time on farms. |
| Hardware manufacturing | MEDIUM | LARGE | Use contract manufacturer. PCBA houses (MacroFab, JLCPCB) handle production. |
| Sales to farmers | HIGH | LARGE | Need channel partner (ag supply stores, ag advisors) or hire someone with farmer relationships. |

### Net Founder-Market Fit: 5/10

**Honest assessment**: The founder's strengths (cloud, ML, systems) map well to the SOFTWARE layer of this product, which is ~40% of the total work. The hardware (40%) and market access (20%) are significant gaps. This is not a fatal mismatch — many successful hardware startups have software-background founders — but it requires:

1. An EE co-founder or senior contractor (non-negotiable for first 6 months)
2. Ag industry advisor or channel partner (for market access)
3. Willingness to spend significant time in unfamiliar territory (farms, hardware labs)

**Comparison to pure-software ideas**: A pure SaaS play (like laser cutting optimization or alloy parameter software) would score 8-9/10 on founder-market fit. This scores 5/10 because hardware + agriculture domain are both gaps. It is buildable but not natural.

### Synergy with Livestock Tags
If the livestock tag product is built first (same architecture), the soil probe becomes a derivative product:
- Shared firmware base (same MCU, same BLE protocol, same Hubble integration)
- Shared cloud backend (device management, alerting)
- Shared Hubble Network relationship
- Shared manufacturing pipeline

**In that case, founder-market fit for the INCREMENTAL effort of soil probes rises to 7/10** because the hard hardware/connectivity problems are already solved.
