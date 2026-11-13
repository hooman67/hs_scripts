# Execution Plan: Portable Brewery EPR Freshness Monitor

## 5a. Product Definition

**Core value proposition**: Instant, in-line oxidation measurement for craft breweries — catch staling before it ruins a batch.

**Key features for MVP (max 3)**:
1. Handheld EPR probe that measures dissolved oxygen radicals in beer samples in <30 seconds
2. Mobile app with trend tracking, batch correlation, and alert thresholds
3. Cloud dashboard with historical data and batch comparison

**What it does NOT do**:
- Does not replace full lab analysis (microbiology, off-flavors beyond oxidation)
- Does not integrate with existing brewery management systems in V1
- Does not handle in-line continuous monitoring (V1 is sample-based)

**Success metrics for prototype validation**:
- Detects 5-50 ppb dissolved oxygen equivalent (standard brewery concern range)
- Correlates with reference lab EPR measurements (R² > 0.9)
- 10 beta brewery users achieve <2 min sample-to-result workflow

---

## 5b. Technical Architecture

**System components**:
1. EPR sensor module (either SpinMagIC chip or custom miniaturized EPR circuit)
2. Microcontroller + BLE communication (nRF52840 or similar)
3. Sample chamber with microfluidic cartridge
4. Mobile app (React Native) → cloud API (AWS)
5. Web dashboard for QC managers

**Technology stack**:
- Hardware: Custom PCB, EPR resonator, permanent magnet assembly, nRF52840 MCU
- Firmware: Zephyr RTOS for BLE + sensor acquisition
- App: React Native (iOS/Android)
- Backend: AWS Lambda + DynamoDB + S3
- ML: TensorFlow Lite model for spectral interpretation

**Build vs buy**:
- EPR sensor chip: BUY (from SpinMagIC if available) or BUILD (custom resonator + frequency synthesizer)
- Microfluidics: BUY (standard lab-on-chip cartridge supplier)
- BLE module: BUY (Nordic nRF52840)
- Cloud: BUY (AWS)
- Spectral ML model: BUILD (proprietary training on beer samples)

**Key technical risks**:
- SpinMagIC may not sell standalone chips → mitigation: develop in-house miniaturized EPR using published CEA-Leti architecture
- Sensitivity may be insufficient for dissolved oxygen at ppb levels in complex beer matrix → mitigation: use spin-trap reagent in sample cartridge to amplify signal
- Permanent magnet size/weight trade-off → mitigation: use rare-earth NdFeB magnets; target 200g total device weight

---

## 5c. Bill of Materials (MVP Prototype)

| Component | Supplier | Unit Cost | Lead Time |
|-----------|----------|-----------|-----------|
| EPR resonator + frequency synthesizer IC | Custom PCB / SpinMagIC | $50-200 | 8-12 weeks |
| NdFeB permanent magnet (0.3T, 25mm cube) | K&J Magnetics / Magnet-Shop | $30 | 1 week |
| nRF52840 BLE SoC + antenna | Nordic Semi / DigiKey | $8 | In stock |
| Custom PCB (4-layer, RF-optimized) | JLCPCB / PCBWay | $15 | 2 weeks |
| Microfluidic sample cartridge (PDMS) | Dolomite / custom) | $5 (at volume) | 4-6 weeks |
| Enclosure (3D printed → injection molded) | Protolabs | $10-30 | 1-2 weeks |
| Battery (Li-Po 2000mAh) | Generic | $5 | In stock |
| Spin-trap reagent (DMPO/PBN) | Sigma-Aldrich | $2/test | In stock |
| **Prototype unit total** | | **~$350-500** | |

**Software costs (monthly)**:
- AWS hosting: $200/month (MVP scale)
- Apple/Google developer accounts: $125/year
- Design tools (Figma): $15/month

---

## 5d. Build Instructions

1. **Weeks 1-4: EPR Sensor Design** (EE + RF engineer)
   - Design miniaturized EPR resonator (X-band, ~9.5 GHz)
   - Select/design frequency sweep circuit
   - Simulate magnetic field uniformity with NdFeB permanent magnet
   - Order PCBs and components

2. **Weeks 3-6: Sample Interface Design** (Mechanical engineer)
   - Design microfluidic cartridge for beer sample + spin-trap mixing
   - 3D print prototypes of sample chamber
   - Validate fluid handling (50-100µL sample volume)

3. **Weeks 5-8: Electronics Integration** (EE)
   - Assemble first prototype boards
   - Integrate EPR sensor + BLE MCU + battery
   - Write firmware for frequency sweep and data acquisition
   - Validate signal acquisition with known spin-trap standards

4. **Weeks 6-10: Software Development** (Full-stack developer)
   - Build React Native app with BLE connection
   - Develop spectral analysis ML pipeline
   - Deploy cloud backend (API + database + auth)
   - Build web dashboard

5. **Weeks 8-12: Beer Sample Validation** (Food scientist + EE)
   - Collect samples from 3-5 partner breweries at various oxidation levels
   - Run parallel measurements: prototype vs reference lab EPR
   - Train ML model on beer-specific spectral signatures
   - Iterate on sensitivity/specificity

**Critical path**: EPR sensor design → electronics integration → beer validation

---

## 5e. Validation Plan

**Target**: 10 craft breweries in beta program (6-week pilot)

**Key hypotheses to test**:
1. Brewers will measure oxidation at least 3x/week if tool is available (usage hypothesis)
2. Device detects oxidation problems at least 48 hours before sensory panel (value hypothesis)
3. Brewers would pay $200/month for the service (willingness-to-pay hypothesis)

**Go/no-go criteria**:
- GO: ≥7/10 breweries use device 3x+/week AND correlation with lab results R² > 0.85
- NO-GO: <5/10 breweries use regularly OR correlation R² < 0.7

---

## 5f. Timeline & Milestones

| Week | Milestone | Decision Point |
|------|-----------|----------------|
| 4 | EPR sensor PCB designed and ordered | Feasible at target size? |
| 8 | First working prototype (lab bench) | Signal quality sufficient? |
| 10 | App + cloud backend functional | — |
| 12 | Beer sample validation complete | Correlation with lab EPR acceptable? |
| 14 | 3 beta brewery units shipped | — |
| 18 | Beta pilot complete | Go/no-go on commercial launch |
| 20 | Manufacturing design (DFM) begins | — |
| 24 | First commercial units available | — |

---

## 5g. Cost Estimate

| Category | Amount |
|----------|--------|
| Hardware prototyping (10 units) | $15,000 |
| PCB/component engineering | $25,000 |
| Software development (6 months, 1 dev) | $90,000 |
| RF/EPR specialist (6 months, contract) | $120,000 |
| Food science consultant | $20,000 |
| Brewery beta program (equipment + travel) | $15,000 |
| Cloud/tools/misc | $10,000 |
| **Total to validation** | **~$295,000** |
| Manufacturing tooling + first batch (50 units) | $150,000 |
| **Total to first revenue** | **~$445,000** |

**Monthly burn rate**: ~$50K (2 FTE + contractor + materials)

**Funding strategy**: Angel round ($500K) targeting hardware/biotech angels. Alternatively, SBIR Phase I ($275K) from NSF/USDA for food safety innovation.
