# 03 - Feasibility & Prototype Plan: Precision Pollination Monitoring Radar

## Architecture Overview

```
[Field Unit]                    [Cloud Backend]              [User Interface]
                                
TI IWR6843 radar module         AWS IoT Core                 React web dashboard
    |                               |                            |
RPi5 (edge ML inference)        Lambda (data ingest)         Heat map visualization
    |                               |                            |
Solar panel + battery           S3 (raw data lake)           Alert notifications (SMS/email)
    |                               |                            |
LTE modem (cellular)            SageMaker (model training)   PDF report generation
    |                               |
Weatherproof enclosure          RDS (metadata, config)
    |
Pole mount (3m height)
```

**Data flow:**
1. IWR6843 captures radar frames at 10-20 fps (range-Doppler maps)
2. RPi5 runs micro-Doppler feature extraction + lightweight classifier (TFLite)
3. Insect detection events (timestamp, estimated count, classification confidence, zone) sent via MQTT over LTE
4. Cloud aggregates events into spatial density maps, generates alerts
5. Dashboard polls API every 60 seconds during active monitoring

## Bill of Materials (Single Prototype Unit)

| Component | Part Number | Quantity | Unit Cost | Confidence | Notes |
|-----------|-------------|----------|-----------|------------|-------|
| Radar module | TI IWR6843ISK-ODS | 1 | $149 | VERIFIED (TI store) | 60-64 GHz, 4 RX / 3 TX antennas, 120-degree FOV |
| Radar carrier board | TI DCA1000EVM | 1 | $549 | VERIFIED (TI store) | Raw ADC data capture for development. Production would use custom PCB. |
| Single board computer | Raspberry Pi 5 (8GB) | 1 | $80 | VERIFIED (RPi authorized dealers) | May need CM5 for thermal management |
| LTE modem | Quectel RM500Q-GL | 1 | $89 | ASSUMED (distributor pricing) | 5G/LTE Cat 20, mPCIe form factor |
| SIM card + data plan | Hologram IoT | 1 | $5/month + $0.40/MB | VERIFIED (Hologram pricing page) | ~100MB/day during bloom = $40/month |
| Solar panel | Renogy 50W monocrystalline | 1 | $65 | VERIFIED (Amazon) | Overkill for power budget, ensures cloudy-day operation |
| Charge controller | Genasun GV-5 | 1 | $89 | VERIFIED | MPPT, 5A |
| Battery | 12V 20Ah LiFePO4 | 1 | $109 | VERIFIED (Amazon, multiple brands) | ~3 days autonomy without sun |
| Weatherproof enclosure | Polycase WH-12 | 1 | $45 | VERIFIED | NEMA 4X rated, 12x10x6" |
| Pole mount hardware | Custom bracket + U-bolts | 1 | $30 | ASSUMED | Fits standard 2" pipe or T-post |
| Antenna (if external needed) | Custom horn or lens antenna | 1 | $200 | UNVERIFIED | May be needed to extend range beyond IWR6843's built-in antenna. This is a major unknown. |
| Cables, connectors, misc | Various | 1 | $50 | ASSUMED | SMA cables, power cables, GPS antenna |
| GPS module | u-blox NEO-M9N | 1 | $35 | VERIFIED | For precise unit geolocation |

**Prototype BOM total: $1,495** (using dev boards)
**Production BOM estimate: $510** (custom PCB replacing DCA1000EVM, volume pricing)

**CRITICAL NOTE:** The $510 production BOM assumes the IWR6843's built-in antenna provides adequate range. If external high-gain antenna or amplification is needed to reach 50m, add $200-500 per unit.

## Software Stack

| Layer | Technology | License | Notes |
|-------|-----------|---------|-------|
| Radar signal processing | TI mmWave SDK + custom DSP | TI proprietary (free for TI chips) | Range-Doppler FFT, CFAR detection, micro-Doppler extraction |
| Edge ML inference | TensorFlow Lite | Apache 2.0 | Insect classification model, runs on RPi5 ARM |
| Edge OS | Raspberry Pi OS Lite (64-bit) | Debian/GPL | Headless, minimal |
| Communication | Paho MQTT + AWS IoT SDK | Eclipse/Apache 2.0 | Encrypted telemetry |
| Cloud ingest | AWS IoT Core + Lambda | AWS commercial | Pay-per-message |
| Data storage | S3 (raw) + TimescaleDB (time-series) | S3 commercial / TimescaleDB Apache 2.0 | Could use AWS Timestream instead |
| ML training | PyTorch + custom training pipeline | BSD | Micro-Doppler signature classification |
| Dashboard | React + Mapbox GL | MIT + Mapbox commercial | Spatial visualization |
| Alerting | AWS SNS | Commercial | SMS/email notifications |

## Step-by-Step Prototype Build Instructions

### Phase 1: Lab Validation (Weeks 1-4) -- MOST CRITICAL

**Goal:** Determine if the IWR6843 can detect and classify bee-sized targets at any commercially useful range.

1. **Week 1:** Acquire IWR6843ISK-ODS evaluation kit + DCA1000EVM data capture card. Set up TI mmWave Studio on Windows laptop. Capture raw radar data from known targets (ball bearings of various sizes simulating insect RCS).

2. **Week 2:** Characterize detection range vs. target size:
   - 3mm steel ball (RCS ~ honeybee): measure max detection range
   - 6mm steel ball (RCS ~ bumblebee): measure max detection range
   - Record at 1m, 2m, 5m, 10m, 20m, 50m distances
   - Document SNR at each range

3. **Week 3:** Acquire live insects (purchase from insectary: honeybees, hoverflies, wasps). Conduct controlled flight detection tests in enclosed space (garage or greenhouse). Record micro-Doppler signatures.

4. **Week 4:** Analyze data. Make GO/NO-GO decision on range viability.

**GO criteria:** Detect bee-sized targets at >= 20m with SNR > 10 dB
**STRETCH criteria:** >= 50m detection
**NO-GO criteria:** Cannot reliably detect bees beyond 5m

### Phase 2: ML Model Development (Weeks 5-8)

5. **Week 5-6:** Build micro-Doppler signature dataset. Capture 1000+ flight events from honeybees, bumblebees, hoverflies, wasps, flies. Label by species.

6. **Week 7-8:** Train CNN classifier on micro-Doppler spectrograms. Target: >85% accuracy distinguishing honeybees from non-pollinators. Port to TFLite for RPi5.

### Phase 3: Field Prototype Integration (Weeks 9-12)

7. **Week 9:** Assemble complete hardware unit. Integrate radar + RPi5 + solar + cellular in weatherproof enclosure. 3D-print or fabricate pole mount.

8. **Week 10:** Deploy in controlled field environment (community garden or small orchard with known bee activity). Run for 1 week continuous.

9. **Week 11-12:** Build minimal web dashboard. Validate end-to-end: radar detects -> edge classifies -> cloud ingests -> dashboard displays.

### Phase 4: Field Trial (Weeks 13-16)

10. **Week 13-16:** Deploy 2-3 units in a cooperating grower's field during a bloom period (requires timing with crop bloom calendar). Collect ground-truth data via manual bee counts for validation.

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Fallback |
|------|-----------|--------|------------|----------|
| Radar cannot detect bees at >5m | HIGH (60%) | FATAL | Use TI IWR6843AOP (antenna-on-package) for baseline, then explore external high-gain antennas or IWR1843 (77GHz, higher freq = better small-target sensitivity) | Pivot to acoustic hybrid (radar for large insects + microphone array for bees). Or abandon. |
| Micro-Doppler classification accuracy <70% | MEDIUM (40%) | HIGH | Collect larger training dataset. Use data augmentation. Try multiple model architectures (CNN, LSTM, transformer). | Fall back to simple "insect present/absent" binary without species classification. Less valuable but still useful. |
| Seasonal revenue makes business unviable | HIGH (70%) | HIGH | Develop multi-season use cases: pest moth monitoring (spring-fall), spray drift detection, frost event monitoring | Position as research tool for universities/USDA at higher per-unit price with year-round data collection mandate |
| BeeHero launches competing field sensor | MEDIUM (50%) | HIGH | Move faster. Secure IP on radar-specific micro-Doppler processing. Target niches BeeHero ignores (organic, small farms). | Pivot to licensing radar IP to BeeHero. Become their "radar module supplier." |
| Solar/battery insufficient for continuous operation | LOW (20%) | MEDIUM | Power budget: IWR6843 (~2W) + RPi5 (~5W) + LTE modem (~2W) = ~9W continuous. 50W panel + 20Ah battery should cover. But California fog can reduce solar significantly in Feb (almond bloom). | Larger battery (40Ah) or reduce to daylight-only operation (bees are inactive at night anyway) |
| Cellular coverage gaps in rural Central Valley | LOW (25%) | MEDIUM | Hologram multi-carrier SIM roams across AT&T/T-Mobile/Verizon. Most almond-growing areas have coverage. | Edge-store data locally, batch-upload when connection available. Dashboard shows slight delay. |
| Regulatory issues with 60GHz radar emissions | LOW (10%) | MEDIUM | IWR6843 operates in ISM band (60-64GHz), no FCC license required for Part 15 devices at this power level. | Confirm with FCC Part 15.255 compliance. TI's module is pre-certified. |

## Validation Plan

**Success Criteria:**

| Metric | Minimum Viable | Target | Method |
|--------|---------------|--------|--------|
| Detection range (honeybee) | 20m | 50m | Controlled test with tethered/free-flying bees at measured distances |
| Classification accuracy | 70% bee vs. non-bee | 85% species-level | Confusion matrix against manual expert labeling |
| False positive rate | <30% | <10% | Compare radar counts vs. manual 5-min observation counts |
| Uptime in field | 90% over 2-week deployment | 99% | System logs, connectivity monitoring |
| Grower perceived value | "Interesting" | "I would pay for this" | Customer interviews post-demo |

**Timeline:**
- Month 1: Lab validation (GO/NO-GO gate)
- Month 2: ML model development
- Month 3: Hardware integration + bench testing
- Month 4: Field trial (must align with a bloom window -- almond bloom is Feb-March, berry bloom is April-June)

## Total Cost and Time Estimate

| Category | Cost | Notes |
|----------|------|-------|
| Prototype hardware (3 units) | $4,500 | Using dev boards, not production BOM |
| Cloud infrastructure (4 months) | $500 | AWS IoT + compute for dev/testing |
| Development tools/software | $0 | All open source / free tiers |
| Travel to field sites (Central Valley) | $2,000 | 4-6 trips from Bay Area |
| Insect specimens for lab testing | $500 | From insectary suppliers |
| Contingency | $2,500 | Unknown unknowns |
| **TOTAL** | **$10,000** | Prototype phase only |
| **Time to prototype** | **4 months** | Assumes full-time effort |
| **Time to first revenue** | **12-18 months** | Must hit a bloom season with working product |

## Founder-Market Fit Assessment

**Founder profile:** Hooman Shariati -- AI/ML infrastructure engineer at Adobe. Deep Python/systems/cloud expertise. No hardware background. No agriculture industry connections.

| Dimension | Score (1-5) | Rationale |
|-----------|-------------|-----------|
| Technical (software/ML) | 5/5 | ML pipeline, cloud infrastructure, data processing are core strengths |
| Technical (hardware/radar) | 1/5 | No RF engineering, no PCB design, no radar signal processing experience. This is the core technical challenge. |
| Domain expertise (agriculture) | 1/5 | No farming background, no grower relationships, no understanding of ag sales cycles |
| Domain expertise (entomology) | 1/5 | No background in insect behavior, pollination biology, or radar entomology |
| Go-to-market ability | 2/5 | Enterprise SaaS sales experience is somewhat transferable, but ag sales are relationship-driven and seasonal |
| Capital access | 3/5 | Adobe salary provides personal runway. But ag-tech VCs want domain founders. |

**Overall founder-market fit: POOR (2/5)**

The critical gap is RF engineering / radar signal processing. This is not a software problem that can be solved with better code -- it is a physics problem requiring specialized hardware expertise. The founder would need to either:
1. Recruit a co-founder with radar/RF background (ex-TI, Infineon, or defense radar engineer)
2. Engage a radar consultancy for the first 6 months ($50K-100K additional cost)
3. Spend 6-12 months self-learning radar signal processing before even starting the prototype

The secondary gap (agriculture domain) can be partially bridged through customer discovery, but selling to conservative Central Valley almond growers without existing relationships is extremely difficult.
