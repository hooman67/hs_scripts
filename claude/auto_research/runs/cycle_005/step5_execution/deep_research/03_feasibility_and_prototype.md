# Feasibility & Prototype Plan: Portable Brewery EPR Freshness Monitor

## Architecture Overview

### System Block Diagram

```
[DISPOSABLE CARTRIDGE]     [HANDHELD PROBE UNIT]           [MOBILE APP]        [CLOUD]
+------------------+      +---------------------+         +------------+      +-------+
| Beer sample      |      | Permanent Magnet    |         | BLE conn   |      | AWS   |
| + PBN spin trap  |----->| (NdFeB, 0.34T)      |         | Spectrum   |      | Lambda|
| (200 uL well)   |      |                     |         | display    |      | Dynamo|
+------------------+      | Microwave Resonator |         | Freshness  |      | S3    |
                          | (planar, 9.7 GHz)   |         | Score      |      | ML    |
                          |                     |         | History    |      | model |
                          | RF Source + Detector |<--BLE-->| Alerts     |<---->| API   |
                          | (VCO + mixer + LNA) |         | Export     |      |       |
                          |                     |         +------------+      +-------+
                          | MCU (nRF52840)      |
                          | Lock-in Amplifier   |
                          | (digital, on-chip)  |
                          |                     |
                          | Li-Po Battery       |
                          | (2000 mAh)          |
                          +---------------------+
```

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| EPR frequency | X-band (~9.7 GHz) | Best sensitivity for aqueous samples; most published beer EPR data is X-band |
| Magnet type | Permanent (NdFeB) | No power consumption, no cooling needed; field swept via small correction coils |
| Resonator | Planar microstrip | Compatible with miniaturization; SpinMagIC approach uses planar resonators |
| Detection | Homodyne with digital lock-in | Reduces analog complexity; MCU handles phase-sensitive detection |
| Spin trap | PBN (alpha-phenyl-N-tert-butylnitrone) | Standard for beer radical studies; stable adducts, well-characterized spectra |
| Sample interface | Disposable cartridge with capillary fill | Eliminates cross-contamination; pre-loaded with spin trap |
| Connectivity | BLE 5.0 | Low power, sufficient bandwidth for spectral data (~2 KB per measurement) |

---

## Bill of Materials (MVP Prototype — 1 Unit)

| # | Component | Specification | Supplier | Unit Cost | Lead Time | Confidence |
|---|-----------|---------------|----------|-----------|-----------|------------|
| 1 | NdFeB permanent magnet | N52 grade, 25x25x25mm cube, 0.34T | K&J Magnetics | $35 | 1 week | VERIFIED |
| 2 | Magnet shimming poles | Custom soft iron, CNC machined | Protolabs / local shop | $200 | 2 weeks | ASSUMED |
| 3 | Field sweep coils | Helmholtz pair, 50 turns, copper wire | Hand-wound / custom | $25 | 1 week | VERIFIED |
| 4 | Microwave VCO | 9.5-10.0 GHz, Analog Devices HMC431 or similar | DigiKey / Mouser | $45 | In stock | VERIFIED |
| 5 | Planar microstrip resonator | Custom PCB, Rogers RO4003C substrate | JLCPCB (RF service) | $50 | 3 weeks | ASSUMED |
| 6 | LNA (Low Noise Amplifier) | Gain 20dB, NF <1.5dB at 10GHz (e.g., Qorvo QPL9057) | DigiKey | $12 | In stock | VERIFIED |
| 7 | Mixer / IQ demodulator | ADL5380 or HMC1048 | Analog Devices / DigiKey | $18 | In stock | VERIFIED |
| 8 | MCU + BLE | nRF52840 dev kit | Nordic Semi / DigiKey | $40 | In stock | VERIFIED |
| 9 | ADC (high-resolution) | ADS1256 (24-bit, for lock-in output) | TI / DigiKey | $12 | In stock | VERIFIED |
| 10 | DAC (field sweep drive) | DAC8562 (16-bit, dual) | TI / DigiKey | $8 | In stock | VERIFIED |
| 11 | Modulation coil driver | Op-amp + current buffer, 100 kHz | Standard parts | $5 | In stock | VERIFIED |
| 12 | PCB (main board) | 4-layer, RF-optimized, 80x60mm | JLCPCB | $20 | 2 weeks | VERIFIED |
| 13 | PCB (resonator board) | 2-layer, Rogers substrate, 30x20mm | JLCPCB RF | $30 | 3 weeks | ASSUMED |
| 14 | Li-Po battery | 3.7V, 2000 mAh, JST connector | Adafruit / Amazon | $12 | In stock | VERIFIED |
| 15 | Battery management | TP4056 module + boost converter | Various | $5 | In stock | VERIFIED |
| 16 | Enclosure | 3D printed (SLA), ~120x80x60mm | In-house / Shapeways | $30 | 1 week | VERIFIED |
| 17 | Sample cartridge (prototype) | 3D printed PDMS mold + glass capillary | In-house | $5 each | 1 week | ASSUMED |
| 18 | PBN spin trap reagent | 1g bottle (Sigma-Aldrich, P7263) | Sigma-Aldrich | $85 (makes ~500 cartridges) | In stock | VERIFIED |
| 19 | Miscellaneous (connectors, wires, SMA, shielding) | — | Various | $50 | In stock | VERIFIED |
| | **PROTOTYPE UNIT TOTAL** | | | **~$700** | | |

### Confidence Legend
- **VERIFIED**: Price confirmed from current supplier catalogs (DigiKey, Mouser, McMaster)
- **ASSUMED**: Estimated based on similar components; actual may vary 30-50%
- **UNVERIFIED**: Speculative; requires supplier engagement to confirm availability and pricing

### Critical Component Risks

| Component | Risk | Mitigation |
|-----------|------|------------|
| Planar resonator | Q-factor may be too low for adequate sensitivity | Design multiple resonator geometries; test 3 variants |
| VCO phase noise | May limit spectral resolution | Add PLL loop; alternatively use DDS + multiplier chain |
| Permanent magnet homogeneity | Field non-uniformity broadens lines, reduces sensitivity | Active shimming with correction coils; magnet selection/sorting |
| Sample cartridge seal | Beer carbonation may create bubbles that interfere | De-gas sample in cartridge design; include bubble trap |

---

## Software Stack

### Firmware (Probe Unit)

| Layer | Technology | Notes |
|-------|------------|-------|
| RTOS | Zephyr OS | Nordic-supported, BLE native, real-time capable |
| Sensor acquisition | Custom Zephyr driver | Drives DAC for field sweep, reads ADC for lock-in output |
| Digital lock-in | DSP on nRF52840 (Cortex-M4F) | 100 kHz modulation, phase-sensitive detection in firmware |
| BLE stack | Zephyr BLE (NUS - Nordic UART Service) | Streams spectral data to phone |
| Power management | Zephyr power framework | Sleep between measurements; wake on button press |

### Mobile App

| Layer | Technology | Notes |
|-------|------------|-------|
| Framework | React Native | Cross-platform iOS/Android |
| BLE library | react-native-ble-plx | Mature BLE communication library |
| State management | Zustand | Lightweight, performant |
| Charts | Victory Native | EPR spectrum display, trend lines |
| ML inference | TensorFlow Lite (on-device) | Spectral classification for Freshness Score |
| Offline storage | SQLite (via expo-sqlite) | Measurement history stored locally |
| Auth | AWS Cognito | Federated auth, multi-user support |

### Cloud Backend

| Layer | Technology | Notes |
|-------|------------|-------|
| API | AWS API Gateway + Lambda (Python) | Serverless, pay-per-use |
| Database | DynamoDB | Measurement records, user profiles |
| Storage | S3 | Raw spectral data, firmware updates |
| ML training | SageMaker | Retrain interpretation model as data grows |
| Analytics | QuickSight or Metabase | Internal dashboards for product usage |
| Notifications | SNS + push (via Amplify) | Alert thresholds |

### ML Model (Spectral Interpretation)

- **Input**: 1D EPR spectrum (512 points, first-derivative absorption)
- **Output**: Freshness Score (0-100, continuous) + confidence interval
- **Architecture**: 1D CNN (3 conv layers + 2 FC layers), ~50K parameters
- **Training data**: Simulated spectra (EPR spectral simulation libraries) + real spectra from beta breweries
- **Edge deployment**: TFLite model on phone (<1 MB)
- **Cold start problem**: Initially use peak-height ratio of PBN-OOH adduct as simple heuristic. Train ML model after collecting 500+ real spectra.

---

## Build Instructions (Detailed)

### Phase 1: EPR Sensor Proof-of-Concept (Weeks 1-6)

**Goal**: Demonstrate EPR signal detection from a known standard (DPPH radical) using miniaturized components on a lab bench.

**Steps**:
1. Design planar microstrip resonator in HFSS or CST Studio (electromagnetic simulation)
2. Design Helmholtz coil pair for field sweep (5 mT range around 0.34T)
3. Order magnet, resonator PCB, VCO, LNA, mixer, ADC
4. Assemble RF chain on evaluation board: VCO --> resonator --> mixer --> ADC
5. Write firmware for field sweep (DAC drives correction coils) and lock-in detection
6. Test with DPPH standard (strong, stable radical — guaranteed signal)
7. **Decision gate**: Can we detect DPPH with SNR > 100? If yes, proceed. If no, investigate resonator redesign or frequency change.

**Required expertise**: RF/microwave engineer (contract, $150-200/hr)
**Estimated cost**: $5,000 (components + contract engineer time)

### Phase 2: Beer Sample Detection (Weeks 6-10)

**Goal**: Detect PBN spin-trap adducts from oxidized beer samples.

**Steps**:
1. Prepare PBN-spiked beer samples at known radical concentrations
2. Validate with benchtop EPR (if accessible — university collaboration)
3. Test our prototype sensor with same samples
4. Characterize sensitivity floor (minimum detectable radical concentration)
5. Measure linearity across 0.1-50 uM range
6. **Decision gate**: Can we detect PBN-OOH at 1 uM with SNR > 10? Is linearity R-squared > 0.85?

**Required expertise**: Food scientist or analytical chemist (part-time consultant)
**Estimated cost**: $8,000 (samples, reagents, consultant, university EPR time rental)

### Phase 3: Portable Integration (Weeks 8-14)

**Goal**: Package all electronics + magnet + resonator into a handheld form factor.

**Steps**:
1. Design integrated PCB (combine RF chain + MCU + power on one board)
2. Design magnet housing with shimming provision
3. Design sample cartridge interface (slide-in mechanism)
4. 3D print enclosure; iterate on ergonomics (3-4 iterations)
5. Assemble 3 prototype units
6. Validate portability: does it work held in hand? Vibration sensitivity? Temperature sensitivity?
7. **Decision gate**: Does portable prototype maintain >80% of bench-top SNR?

**Required expertise**: PCB layout engineer, mechanical designer (CAD)
**Estimated cost**: $15,000 (PCBs, assembly, 3D printing, iteration)

### Phase 4: Software Development (Weeks 6-16, parallel)

**Goal**: Complete mobile app and cloud backend.

**Steps**:
1. Implement BLE communication protocol (firmware + app)
2. Build measurement workflow UI (guided steps with illustrations)
3. Implement spectral display (real-time plot during measurement)
4. Build Freshness Score algorithm (initial heuristic, then ML)
5. Implement batch tracking, trend visualization, alerts
6. Build cloud API (measurement storage, multi-device sync, firmware OTA)
7. Beta test app with internal team

**Required expertise**: Full-stack mobile developer (this is the founder's wheelhouse)
**Estimated cost**: $20,000 (if done by founder; mostly opportunity cost)

### Phase 5: Beta Validation (Weeks 16-24)

**Goal**: Deploy 5-10 units to beta breweries; validate product-market fit.

**Steps**:
1. Recruit 5-10 beta breweries (see Doc 4)
2. Ship units with onboarding documentation
3. Weekly check-ins: usage frequency, issues, feedback
4. Collect comparative data: our Freshness Score vs. their DO readings vs. sensory evaluation
5. Iterate on hardware/software based on feedback
6. **Final decision gate**: Do breweries use it 3x+/week? Would they pay $5K+?

**Required expertise**: Founder (customer success) + food scientist (data analysis)
**Estimated cost**: $25,000 (travel, cartridge production, support time)

---

## Risk Register

| # | Risk | Probability | Impact | Mitigation | Owner |
|---|------|-------------|--------|------------|-------|
| R1 | Planar resonator Q-factor insufficient for beer-matrix sensitivity | 40% | CRITICAL | Design 3 resonator variants; consider loop-gap resonator alternative; increase modulation amplitude | RF Engineer |
| R2 | Permanent magnet homogeneity too poor for resolved spectra | 25% | HIGH | Active shimming coils; magnet sorting/selection; accept broader lines if total radical quantitation (not species ID) is the goal | RF Engineer |
| R3 | SpinMagIC chip unavailable AND custom design fails | 20% | CRITICAL | Maintain two parallel paths: (a) chip purchase/license, (b) discrete RF chain. Accept larger form factor if needed for v1 | Founder |
| R4 | Beer carbonation/bubbles interfere with measurement | 30% | MEDIUM | Degassing step in cartridge (membrane vent); sample preparation protocol | Food Scientist |
| R5 | Spin-trap cartridge shelf life <3 months | 35% | MEDIUM | Nitrogen-sealed foil packaging; desiccant; accelerated aging study; cold-chain for inventory | Food Scientist |
| R6 | Craft brewers unwilling to pay $5K for radical measurement | 30% | HIGH | Customer discovery before build; consider lower-price model ($2,500) with higher consumable cost; lease/subscription model | Founder |
| R7 | Bruker launches sub-$20K EPR | 5% | HIGH | Move fast; build brewery-specific workflow moat; price below any Bruker offering | Founder |
| R8 | Regulatory requirements (FDA/ASBC method validation) block adoption | 15% | MEDIUM | Position as QC screening tool, not official method; pursue ASBC method adoption in parallel | Food Scientist |
| R9 | RF/microwave engineer unavailable or too expensive | 25% | HIGH | Identify 3+ potential contractors upfront; consider university collaboration (reduced cost, IP complexity); approach RF consulting firms (e.g., Modelithics, Rogers Corp application engineers) | Founder |
| R10 | Battery life insufficient (<20 measurements per charge) | 15% | LOW | Use larger battery (3000 mAh); optimize duty cycle (VCO off between measurements) | EE |

---

## Validation Plan

### Gate 1: Physics Validation (Week 6) — Budget: $5K

**Question**: Can we detect EPR signal from known radicals at miniaturized scale?

| Criterion | Pass | Fail |
|-----------|------|------|
| DPPH detection | SNR > 100 with 1 mM DPPH standard | SNR < 20 |
| Sensitivity | Detect 10 uM DPPH (10x dilution) | Cannot detect below 1 mM |
| Measurement time | Complete sweep in <60 seconds | Requires >5 minutes for adequate SNR |

**If FAIL**: Pivot to alternative resonator design, or pivot away from this idea entirely.

### Gate 2: Beer Matrix Validation (Week 10) — Budget: $8K

**Question**: Does it work with real beer samples (complex matrix, low radical concentrations)?

| Criterion | Pass | Fail |
|-----------|------|------|
| PBN-OOH detection in beer | Detect 1 uM spin-trap adduct in beer matrix | Cannot detect below 10 uM |
| Linearity | R-squared > 0.85 across 0.1-50 uM range | R-squared < 0.7 |
| Beer style robustness | Works across lager, IPA, stout (3+ styles) | Only works in one style |
| Temperature sensitivity | <10% variation from 4C to 25C | >30% variation |

**If FAIL**: Investigate pre-concentration step, alternative spin trap, or narrower application scope.

### Gate 3: Portability Validation (Week 14) — Budget: $15K

**Question**: Does miniaturization maintain adequate performance?

| Criterion | Pass | Fail |
|-----------|------|------|
| Portable vs. bench | Portable retains >80% of bench SNR | <50% SNR retention |
| Measurement time | <30 seconds | >2 minutes |
| Vibration robustness | Stable reading while handheld | Requires flat surface |
| Size/weight | <600g, fits in one hand | >1 kg or requires two hands |

### Gate 4: Market Validation (Week 24) — Budget: $25K

**Question**: Will breweries adopt and pay?

| Criterion | Pass | Fail |
|-----------|------|------|
| Usage frequency | 7/10 beta breweries use 3x+/week | <5/10 use regularly |
| Willingness to pay | 6/10 would pay $4K+ for production unit | <4/10 willing at $4K |
| Early detection value | Device flags staling 24+ hours before sensory panel | No time advantage |
| NPS | >50 | <20 |

---

## Cost & Time Estimate

### Total Budget to Market Validation

| Phase | Duration | Cost | Cumulative |
|-------|----------|------|------------|
| Phase 1: EPR Proof-of-Concept | 6 weeks | $50,000 | $50,000 |
| Phase 2: Beer Matrix Testing | 4 weeks | $30,000 | $80,000 |
| Phase 3: Portable Integration | 6 weeks | $60,000 | $140,000 |
| Phase 4: Software Development | 10 weeks (parallel) | $40,000 | $180,000 |
| Phase 5: Beta Validation | 8 weeks | $50,000 | $230,000 |
| **Total to validated prototype** | **~24 weeks (6 months)** | **$230,000** | |

### Total Budget to First Revenue

| Item | Cost |
|------|------|
| Prototype validation (above) | $230,000 |
| Manufacturing design (DFM) | $40,000 |
| Regulatory / safety testing (CE, FCC) | $25,000 |
| First production run (50 units) | $75,000 |
| Marketing / launch | $30,000 |
| Working capital / buffer | $50,000 |
| **Total to first revenue** | **~$450,000** |

### Timeline Summary

| Month | Milestone |
|-------|-----------|
| Month 1-2 | EPR proof-of-concept on bench |
| Month 3 | Beer sample validation |
| Month 4 | Portable prototype assembled |
| Month 5 | Software complete, beta units ready |
| Month 6-7 | Beta program with 5-10 breweries |
| Month 8 | Manufacturing design |
| Month 9-10 | First production units |
| Month 10-12 | Commercial launch, first revenue |

**Monthly burn rate**: ~$40K (RF contractor + food scientist consultant + components + cloud)

---

## Founder-Market Fit Assessment

### Founder Profile
- Background: AI/ML infrastructure engineer
- Strengths: Deep Python/systems/cloud expertise, software architecture, data pipelines, ML model development
- Weaknesses: No hardware background, no RF/microwave engineering, no food science domain expertise, no brewery industry connections

### Fit Analysis

| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Technical capability (software/ML) | 9/10 | Can build the entire software stack, ML model, cloud backend |
| Technical capability (hardware/RF) | 2/10 | Cannot design EPR resonator, RF chain, or magnet assembly without significant outside help |
| Domain expertise (brewing science) | 2/10 | No existing knowledge of brewing QC workflows, oxidation chemistry, or spin-trap methodology |
| Industry network (craft brewing) | 1/10 | No existing relationships with breweries, brewers guilds, or brewing suppliers |
| Go-to-market capability | 5/10 | General startup skills transferable, but lacks specific channel knowledge |
| Fundraising capability | 6/10 | Technical founder credibility, but hardware startups are harder to fund than software |

### Critical Gaps That Must Be Filled

1. **RF/Microwave Engineer (CRITICAL)**: Must find and hire/contract an experienced RF engineer with EPR or high-frequency analog design experience. This person designs the core sensing hardware. Without them, the project cannot start. Likely cost: $150-250/hr contract or $180K+/year full-time.

2. **Food Science / Brewing Advisor (IMPORTANT)**: Need someone who understands spin-trap EPR methodology in food systems AND has brewery industry connections. Target: recently graduated PhD from DTU (Technical University of Denmark — leading beer oxidation EPR research group) or UC Davis Food Science department.

3. **Hardware Engineering (IMPORTANT)**: PCB layout, mechanical design, DFM expertise. Contract role initially.

### Honest Assessment

**Founder-market fit: POOR (3/10)**

This is fundamentally a hardware-physics product being proposed by a software engineer. The core value creation happens in the EPR sensor — the RF engineering, magnet design, and spectral chemistry. The software (app, cloud, ML) is important but secondary; it is also the easier part that any competent developer could build.

**This does not mean the idea is bad — it means the founding team is incomplete.** A software/ML founder building this alone would almost certainly fail. However, a software/ML founder PAIRED WITH an RF engineer and a food scientist could succeed. The founder's contribution would be:
- Product vision and startup execution
- Software/cloud/ML stack (50% of the product)
- Fundraising and business operations

**Recommendation**: Do NOT attempt this alone. Find an RF/EPR hardware co-founder or commit to a $100K+ engineering contract for the sensor subsystem before committing the remaining capital.
