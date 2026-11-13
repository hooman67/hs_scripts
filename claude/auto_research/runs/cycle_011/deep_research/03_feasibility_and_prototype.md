# Feasibility & Prototype Plan: IoT Bolt Tension Monitor for Wind Turbines

## System Architecture

```
[Strain Gauge Washer] --> [Wireless Sensor Node] --LoRa 915MHz--> [Tower Gateway]
     (per bolt)              (per bolt)                              (per turbine)
                                                                         |
                                                                    Cellular/WiFi
                                                                         |
                                                                    [Cloud Platform]
                                                                         |
                                                        +----------------+----------------+
                                                        |                |                |
                                                   [Ingestion]     [Analytics]      [Dashboard]
                                                   (Time-series)   (Alerting/ML)    (Web/Mobile)
```

### Hardware Architecture Detail

**Strain Gauge Washer:**
- Full Wheatstone bridge (4 gauges, 350 ohm) bonded to stainless steel washer
- Washer sized to match standard M30-M42 wind turbine flange bolts
- Temperature compensation via bridge configuration
- Output: 0-20mV proportional to applied load (0-500kN typical)
- Sealed: epoxy encapsulation, IP67 minimum
- Connector: spring-loaded pogo pins to sensor node (no cables)

**Wireless Sensor Node:**
- MCU: Nordic nRF52840 (BLE + capable of driving LoRa module via SPI)
- Radio: Semtech SX1276 LoRa transceiver (915MHz ISM band, US)
- ADC: 24-bit external ADC (ADS1220 or similar) for strain gauge signal
- Power: CR123A lithium primary battery (3V, 1500mAh) -- 5+ year life at 15-min intervals
- Enclosure: IP67 injection-molded polycarbonate, bolt-on/magnetic mount
- Size target: 40mm x 40mm x 20mm
- Operating temp: -40C to +85C

**Tower Gateway:**
- SBC: Raspberry Pi CM4 or similar Linux SBC
- LoRa: Concentrator module (SX1302) -- receives from up to 200 nodes simultaneously
- Uplink: 4G LTE modem (Cat-M1/NB-IoT for low bandwidth) + Ethernet backup
- Power: 24VDC from tower power rail (standard in most turbines)
- Storage: 32GB local buffer (survives connectivity outages)
- Enclosure: DIN-rail mount, IP54

---

## Bill of Materials (BOM) -- Per Bolt Sensor Point

| Component | Part / Source | Unit Cost | Confidence |
|-----------|--------------|-----------|------------|
| Strain gauge washer (blank) | Custom machined 17-4PH stainless, M36 | $8.00 | ASSUMED (based on machining quotes at 1000+ qty) |
| Strain gauges (4x) | Micro-Measurements CEA-06-125UW-350 or equiv | $3.50 | VERIFIED (Vishay catalog pricing) |
| Gauge bonding/encapsulation | M-Bond 610 + epoxy seal, labor | $2.50 | ASSUMED |
| Nordic nRF52840 module | u-blox BMD-340, Mouser | $4.50 | VERIFIED (distributor pricing at 1K qty) |
| LoRa transceiver SX1276 | HopeRF RFM95W module | $3.80 | VERIFIED (LCSC/Mouser pricing) |
| 24-bit ADC (ADS1220) | Texas Instruments, TSSOP-16 | $2.10 | VERIFIED (TI direct pricing) |
| PCB (4-layer, 30x30mm) | JLCPCB/PCBWay at 1000 qty | $1.20 | VERIFIED (online quote) |
| Battery CR123A (Panasonic) | Industrial pack | $1.50 | VERIFIED |
| Enclosure (injection molded) | Custom tooling amortized over 5000 units | $2.80 | ASSUMED (tooling $15K / 5000 units + material) |
| Antenna (PCB trace or chip) | Johanson 0915AT43A0026 | $0.45 | VERIFIED |
| Connectors, passives, misc | Various | $1.50 | ASSUMED |
| Assembly (pick-and-place + final) | Contract manufacturer | $3.00 | ASSUMED (estimate) |
| Calibration/test | Per-unit factory calibration | $2.00 | ASSUMED |
| **TOTAL PER BOLT** | | **$36.85** | |

### Per-Gateway BOM

| Component | Unit Cost | Confidence |
|-----------|-----------|------------|
| Raspberry Pi CM4 (4GB/32GB) | $55 | VERIFIED |
| CM4 IO board or custom carrier | $40 | ASSUMED |
| SX1302 LoRa concentrator HAT | $120 | VERIFIED (RAK2287) |
| 4G LTE modem (Quectel EG25-G) | $35 | VERIFIED |
| Power supply (24V to 5V, DIN) | $15 | VERIFIED |
| Enclosure (DIN-rail, IP54) | $25 | ASSUMED |
| Antenna (LoRa + LTE), cables | $30 | ASSUMED |
| Assembly + test | $40 | ASSUMED |
| **TOTAL PER GATEWAY** | **$360** | |

### Total Per-Turbine Hardware Cost (80 bolts monitored)
- 80 bolt sensors: 80 x $37 = **$2,960**
- 1 gateway: **$360**
- Installation materials: **$200**
- **Total: ~$3,520 per turbine** (at 1000-unit scale)
- At pilot scale (10 turbines, 50 units): ~$5,500/turbine (lower volume pricing)

---

## Software Stack

### Cloud Platform
| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Ingestion | AWS IoT Core + Kinesis | Managed MQTT broker, handles device auth |
| Time-series DB | TimescaleDB on RDS (or InfluxDB) | Optimized for sensor data queries |
| Application | Python (FastAPI) on ECS/Fargate | Founder's strength, rapid iteration |
| Analytics | Python (NumPy, SciPy, scikit-learn) | Signal processing, anomaly detection |
| Dashboard | React + Grafana (embedded) | Fast to build, extensible |
| Alerts | AWS SNS + PagerDuty integration | Reliable delivery |
| Storage | S3 (raw data archive) | Cheap long-term storage |

### Firmware
| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Node firmware | Zephyr RTOS (C) | Best-in-class for nRF52840, low-power |
| Gateway OS | Yocto Linux or Raspberry Pi OS | Reliable, OTA-updatable |
| Gateway application | Python + MQTT | Rapid iteration, founder-friendly |
| OTA updates | Golioth or custom (MQTT-based) | Critical for field updates |

### Data Pipeline
```
Sensor Node (LoRa packet every 15 min)
    --> Gateway (MQTT publish to AWS IoT Core)
        --> Kinesis Data Stream
            --> Lambda (validation, enrichment)
                --> TimescaleDB (operational queries)
                --> S3 (raw archive, ML training data)
                    --> SageMaker (future: failure prediction models)
```

---

## Prototype Build Plan

### Phase 1: Lab Bench Prototype (Weeks 1-8, $25K)

**Goal**: Prove strain gauge washer + wireless node concept works on a bench.

**Steps:**
1. **Week 1-2**: Procure off-the-shelf load washer (Futek LTH500 or equivalent) to validate measurement concept before custom design
2. **Week 2-4**: Design custom strain gauge washer (engage mechanical engineer contractor, $5-8K)
3. **Week 3-5**: Design sensor node PCB (use nRF52840-DK + SX1276 breakout for initial testing, then custom PCB)
4. **Week 4-6**: Develop Zephyr firmware (sampling, LoRa transmission, power management)
5. **Week 6-7**: Integrate washer + node, validate measurement accuracy on hydraulic test rig
6. **Week 7-8**: Gateway prototype (RPi4 + RAK2245 HAT), cloud connectivity proof

**Success criteria:**
- Measurement accuracy within +/-2% of reference load cell
- LoRa link budget verified at 50m through steel (simulated tower)
- Battery current draw <50uA average (projecting 5+ year life)
- End-to-end data path: washer --> node --> gateway --> cloud --> dashboard

**Hardware needed (not in BOM -- development costs):**
- Hydraulic bolt tensioner + test fixture: $3K (rent or university lab access)
- Development boards, components: $2K
- Mechanical engineering contractor: $8K
- PCB prototyping (5 revisions): $3K
- Test equipment (oscilloscope, DMM, spectrum analyzer): $5K (or borrow)
- Misc/contingency: $4K

### Phase 2: Environmental Qualification (Weeks 9-16, $40K)

**Goal**: Prove hardware survives wind turbine environment.

**Steps:**
1. Thermal cycling test (-40C to +85C, 500 cycles) -- use environmental chamber at test lab
2. Vibration testing (IEC 61400-2 profile) -- 20Hz-2000Hz random vibration
3. Humidity testing (95% RH, condensation cycles)
4. EMC testing (immunity to variable-frequency drive interference)
5. Lightning surge testing (basic level -- indirect effects)
6. LoRa range testing in real steel structure (bridge, building frame, or actual turbine tower)

**External costs:**
- Environmental test lab rental: $15K (2 weeks of chamber time)
- EMC pre-compliance testing: $8K
- Vibration test fixture + setup: $5K
- Travel for field testing: $3K
- Redesign iterations: $9K

### Phase 3: Pilot Deployment (Weeks 17-32, $80K)

**Goal**: Deploy on 5 real turbines, collect 3+ months of continuous data.

**Steps:**
1. Manufacture 50 sensor nodes + 5 washers (small batch, $20K)
2. Negotiate pilot agreement with wind farm operator (revenue-free, data-sharing)
3. Installation (2 days per turbine, with operator's maintenance crew)
4. 3 months monitoring, iterating on firmware and cloud platform
5. Collect validation data: compare our readings to manual ultrasonic checks

**Costs:**
- Small-batch manufacturing: $20K
- Travel/installation: $15K (5 site visits)
- Cloud infrastructure: $2K (3 months)
- Operator relationship / business development: $10K
- Software development (dashboard, alerts): covered by founder time
- Contingency/rework: $33K

---

## Risk Register

| # | Risk | Probability | Impact | Mitigation | Status |
|---|------|-------------|--------|------------|--------|
| R1 | LoRa signal cannot penetrate tower steel reliably | MEDIUM | HIGH | Test early (Phase 1). Fallback: slot antenna near flange gaps, or mesh topology with relay nodes | OPEN |
| R2 | Strain gauge bond fails under vibration/temperature cycling | MEDIUM | HIGH | Use proven aerospace-grade adhesives (M-Bond 610, cures at 150C). Accelerated life test in Phase 2 | OPEN |
| R3 | Battery life <3 years in field conditions | LOW | MEDIUM | Power budget analysis shows 5+ years at 15-min intervals. Duty cycle adjustable. Energy harvesting (vibration) as backup | OPEN |
| R4 | Wind operators refuse to modify bolt assemblies | MEDIUM | HIGH | Design washer to maintain bolt class rating. Get DNV statement of conformity. Insurance backing. | OPEN |
| R5 | Hardware certification (IEC/CE) takes >12 months | MEDIUM | MEDIUM | Start pre-compliance early. Engage notified body in Phase 2. Budget $50-80K for full cert. | OPEN |
| R6 | Pilot operator churns before meaningful data collected | LOW | MEDIUM | Multi-operator pilot (3+ sites). Offer free monitoring for 6 months. | OPEN |
| R7 | OEM announces competitive product during our development | LOW | HIGH | Speed is the mitigation. Also: OEM products serve OEM fleet only; independents still need us. | OPEN |
| R8 | Manufacturing quality issues at scale | MEDIUM | MEDIUM | Start with reputable CM (Jabil, Flex for larger runs; PCBWay/Seeed for prototype). 100% factory test. | OPEN |
| R9 | Customer acquisition cost too high (long sales cycles) | HIGH | MEDIUM | Partner with O&M service providers (they have existing relationships). Insurance-driven demand. | OPEN |
| R10 | Founder lacks hardware expertise | HIGH | MEDIUM | Hire EE/ME contractor for hardware design. Focus founder time on software platform + business development. | OPEN |

---

## Validation Plan

| Milestone | Timeline | Validation Method | Pass Criteria |
|-----------|----------|-------------------|---------------|
| Measurement accuracy | Week 8 | Compare to calibrated reference load cell | +/-2% full scale |
| LoRa range in steel | Week 10 | Field test in industrial structure | Reliable link at 80m through 2+ steel floors |
| Environmental survival | Week 16 | IEC-profile thermal/vibration test | Zero failures in 500 thermal cycles, 4hr vibe test |
| Battery life projection | Week 12 | Measured average current draw | <50uA average (projects to 5+ years) |
| Cloud latency | Week 8 | End-to-end measurement timestamp | <5 min from sample to dashboard |
| Pilot data quality | Week 28 | Cross-reference with manual UT check | Correlation R^2 > 0.95 with ultrasonic measurement |
| Customer willingness | Week 20 | Signed pilot agreement | At least 1 operator signs (even unpaid pilot) |

---

## Cost & Timeline Estimate

### Total Prototype-to-Pilot Budget

| Phase | Duration | Cost | Cumulative |
|-------|----------|------|-----------|
| Phase 1: Lab prototype | 8 weeks | $25K | $25K |
| Phase 2: Environmental qual | 8 weeks | $40K | $65K |
| Phase 3: Pilot deployment | 16 weeks | $80K | $145K |
| Certification (parallel) | 20 weeks | $60K | $205K |
| Manufacturing setup | 8 weeks | $80K | $285K |
| First production run (200 units) | 8 weeks | $40K | $325K |
| Operating costs (12 mo) | Ongoing | $75K | $400K |
| Contingency (12%) | -- | $50K | **$450K** |

### Timeline to Revenue
- **Month 0-2**: Lab prototype development
- **Month 2-4**: Environmental testing + certification start
- **Month 4-8**: Pilot deployment + data collection
- **Month 6-9**: Certification completion (parallel)
- **Month 8-10**: Manufacturing setup + first production run
- **Month 10-12**: First paying customers deployed
- **Month 12+**: Revenue ramp

**Realistic first revenue: Month 10-12** (optimistic), **Month 14-16** (realistic given wind industry timelines)

---

## Founder-Market Fit Assessment

### Founder Profile
- **Background**: AI/ML infrastructure engineer
- **Strengths**: Deep Python, systems architecture, cloud (AWS), data pipelines, analytics
- **Weaknesses**: No hardware design experience, no wind industry relationships, no manufacturing background

### Fit Analysis

| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Technical fit (software) | 5/5 | Cloud platform, analytics, ML pipeline are squarely in founder's wheelhouse |
| Technical fit (hardware) | 1/5 | Zero hardware design experience. Must hire/contract EE+ME immediately |
| Domain expertise | 1/5 | No wind industry background. Must learn or hire domain expert |
| Customer access | 2/5 | No existing relationships with wind operators. Cold outreach required |
| Operational fit | 3/5 | Systems thinking translates; manufacturing operations are learnable |
| Fundraising fit | 3/5 | Hardware + vertical SaaS is fundable; AI/ML background helps narrative |

### Founder-Market Fit Verdict: WEAK (but addressable)

**The honest assessment**: This is primarily a hardware + industrial sales business with a software component. The founder's strengths (Python, ML, cloud) are necessary but not sufficient. The critical-path skills (hardware design, wind industry relationships, certification navigation, hardware manufacturing) are all gaps.

**How to address:**
1. **Hire co-founder or senior contractor with EE/ME background** (ideally with sensor/IoT hardware experience). Budget: $80-120K/year or equity.
2. **Engage wind industry advisor** (retired O&M director or technical consultant). Budget: $5-10K retainer + advisory equity (0.5-1%).
3. **Leverage founder's data/ML skills** as the differentiator: the hardware is commodity; the intelligence layer (failure prediction, fleet optimization) is where the moat lives. Position yourself as CEO/CTO of the software+analytics side.
4. **Partner with hardware design house** for first 2 iterations (e.g., Anduril-style approach: outsource hardware design, own the integration and software).

**Key risk**: Founder may underestimate hardware development timelines and costs. Hardware always takes 2-3x longer than software engineers expect. Budget accordingly.

---

## Build vs. Buy Decision Matrix

| Component | Build | Buy/Partner | Recommendation |
|-----------|-------|-------------|----------------|
| Strain gauge washer | Must build (no off-the-shelf product for this form factor) | Buy blank washers, outsource gauge bonding to sensor house | **PARTNER** with strain gauge manufacturer (e.g., HBM, Vishay) |
| Sensor node PCB | Must build (custom integration) | Use reference designs from Nordic/Semtech | **BUILD** (using reference designs as starting point) |
| Node firmware | Must build (power optimization is critical) | Could use Zephyr + existing LoRa stacks | **BUILD** on open-source foundations |
| Gateway hardware | Can buy (RPi + HAT) | Off-the-shelf LoRa gateways exist | **BUY** for prototype, custom for production |
| Gateway software | Must build (domain-specific logic) | MQTT/bridge software exists | **BUILD** (lightweight, Python-based) |
| Cloud platform | Must build (core product) | Generic IoT platforms exist (AWS IoT, Losant) | **BUILD** on AWS IoT Core (managed infrastructure) |
| Manufacturing | Cannot do in-house (no factory) | Contract manufacturer | **BUY** (partner with CM like Jabil/PCBWay) |
| Certification | Cannot do in-house | Test labs + notified bodies | **BUY** (engage lab like TUV, Bureau Veritas) |
