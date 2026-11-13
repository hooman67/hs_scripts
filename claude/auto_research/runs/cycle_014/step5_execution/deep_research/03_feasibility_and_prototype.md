# Feasibility & Prototype Plan: AI Weld Quality Monitoring from Electrical Signatures

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLOUD LAYER (AWS)                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ API Gateway  │  │ ML Training  │  │ Dashboard (React)│   │
│  │ (FastAPI)    │  │ Pipeline     │  │ + Report Gen     │   │
│  └──────┬──────┘  └──────────────┘  └──────────────────┘   │
│         │              ▲                                     │
│  ┌──────┴──────┐      │                                     │
│  │ TimescaleDB  │      │ Model updates (OTA)                │
│  │ (weld logs)  │      │                                     │
│  └─────────────┘      │                                     │
└────────────────────────┼────────────────────────────────────┘
                         │ WiFi (MQTT/HTTPS)
                         │
┌────────────────────────┼────────────────────────────────────┐
│                    EDGE DEVICE                               │
│  ┌─────────────┐  ┌───┴──────────┐  ┌──────────────────┐   │
│  │ Sensor       │  │ MCU          │  │ User Interface   │   │
│  │ Frontend     │──│ (ESP32-S3 or │──│ (3x LED, buzzer, │   │
│  │ (ADC+amp)    │  │  STM32H7)    │  │  WiFi status)    │   │
│  └──────┬──────┘  │              │  └──────────────────┘   │
│         │         │ - Signal proc │                          │
│         │         │ - ML inference│                          │
│         │         │ - Data buffer │                          │
│         │         │ - OTA updates │                          │
│  ┌──────┴──────┐  └──────────────┘                          │
│  │ Hall-effect  │                                            │
│  │ + Voltage    │                                            │
│  │ divider      │                                            │
│  └─────────────┘                                            │
└─────────────────────────────────────────────────────────────┘
         │
    ┌────┴────┐
    │ Welding  │  (Any brand: Lincoln, Miller, ESAB, etc.)
    │ Machine  │
    └─────────┘
```

## Bill of Materials (BOM) - Production Unit

| Component | Specific Part | Unit Cost | Qty | Subtotal | Confidence |
|-----------|--------------|-----------|-----|----------|------------|
| Hall-effect current sensor | ACS770xCB-200B (200A) or TMCS1108A4U (±75A) | $8-12 | 1 | $10 | VERIFIED (Mouser/DigiKey) |
| Voltage divider + protection | Resistor network + TVS diode + diff amp (INA219 or AD8479) | $3-5 | 1 | $4 | VERIFIED |
| ADC | ADS131M04 (24-bit, 64kSPS) or built-in ESP32-S3 12-bit SAR | $5-15 | 1 | $10 | ASSUMED - need to validate 12-bit is sufficient |
| MCU + WiFi | ESP32-S3-WROOM-1 (dual-core 240MHz, WiFi, 8MB PSRAM) | $4-6 | 1 | $5 | VERIFIED (LCSC/DigiKey) |
| Alternatively: STM32H7 + separate WiFi | STM32H743 + ESP32-C3 for WiFi | $12-18 | 1 | $15 | VERIFIED but increases BOM |
| Power supply | 24V industrial input -> 3.3V/5V buck (LM2596 or MP1584) | $2-4 | 1 | $3 | VERIFIED |
| Enclosure | IP65 ABS enclosure (120x80x55mm) + DIN rail mount | $5-10 | 1 | $8 | ASSUMED |
| LED indicators | 3x 5mm LED (R/Y/G) + current limiting resistors | $0.50 | 1 | $1 | VERIFIED |
| Buzzer | Piezo buzzer (optional, for defect alert) | $1 | 1 | $1 | VERIFIED |
| PCB (custom) | 4-layer, 100x60mm, manufactured by JLCPCB | $3-5 | 1 | $4 | VERIFIED (at qty 500+) |
| Connectors | Current clamp connector + voltage banana jacks + USB-C (debug) | $5-8 | 1 | $6 | ASSUMED |
| EMI shielding | Ferrite beads + shielding can (welding env is noisy) | $3-5 | 1 | $4 | ASSUMED - critical for welding EMI |
| Antenna | External WiFi antenna (SMA, for metal enclosure) | $2-3 | 1 | $2 | VERIFIED |
| Assembly + testing | SMT assembly (JLCPCB) + QC testing | $8-12 | 1 | $10 | ASSUMED (at qty 500+) |
| **TOTAL BOM** | | | | **$68-83** | |
| **Target BOM** | | | | **$80** | |

**BOM Confidence Notes:**
- VERIFIED: Price confirmed on DigiKey/Mouser/LCSC within last data (qty 100+)
- ASSUMED: Reasonable estimate based on similar products, needs supplier quotes
- UNVERIFIED: Critical uncertainty that could significantly change cost

**Key BOM Decision: ESP32-S3 vs STM32H7**

| Factor | ESP32-S3 | STM32H7 |
|--------|----------|---------|
| Cost | $5 | $15 (+ WiFi module) |
| ML inference | TFLite Micro, limited | Powerful DSP, better for signal processing |
| ADC quality | 12-bit SAR, noisy | 16-bit internal ADC, better |
| WiFi | Built-in | Needs separate module |
| Development | Arduino/ESP-IDF, large community | STM32CubeIDE, steeper learning curve |
| Power | Lower | Higher |
| **Recommendation** | **Prototype (cheaper, faster)** | **Production (if 12-bit ADC insufficient)** |

**Prototype BOM (v0.1 - lab validation):**

| Component | Part | Cost | Source |
|-----------|------|------|--------|
| ESP32-S3 DevKit | ESP32-S3-DevKitC-1 | $10 | Amazon/DigiKey |
| Current sensor | ACS712 30A module (breadboard-friendly) | $5 | Amazon |
| ADC (external) | ADS1115 16-bit I2C module | $8 | Adafruit |
| Voltage divider | Resistors + breadboard | $2 | Any |
| Breadboard + wires | Standard | $10 | Amazon |
| Power bank | USB-C power bank | $15 | Amazon |
| **Prototype total** | | **~$50** | |

## Software Stack

### Edge (MCU firmware)
```
Language: C/C++ (ESP-IDF or Arduino framework)
ML Runtime: TensorFlow Lite Micro (quantized INT8 models)
Signal Processing: Custom DSP (FFT, wavelet decomposition, RMS calculations)
Communication: MQTT over WiFi (AWS IoT Core)
OTA Updates: ESP-IDF OTA partition scheme
Storage: Local flash buffer (2MB) for offline operation
```

### Cloud Backend
```
API: Python FastAPI (async, high performance)
Database: TimescaleDB (time-series weld data) + PostgreSQL (metadata)
ML Training: PyTorch (model development) -> ONNX -> TFLite (edge deployment)
Infrastructure: AWS (IoT Core, Lambda, S3, ECS)
Dashboard: React + Recharts (weld visualizations)
Auth: AWS Cognito (multi-tenant)
CI/CD: GitHub Actions -> ECR -> ECS
```

### ML Pipeline
```
Training Data: Labeled weld signals (current + voltage waveforms + defect labels)
Features: 
  - Time-domain: RMS, peak, crest factor, kurtosis
  - Frequency-domain: FFT magnitude spectrum, spectral centroid
  - Time-frequency: Short-time FFT, wavelet coefficients
  - Statistical: rolling mean/std deviation, rate of change
Model: 1D-CNN or LSTM (small enough for edge deployment)
  - Input: 1000-sample windows (~10ms at 100kHz)
  - Output: [Good, Porosity, Undercut, ColdLap, BurnThrough] probabilities
  - Size target: <500KB quantized (fits ESP32-S3 flash)
Inference: ~50ms per window on ESP32-S3 (estimated)
```

## Build Instructions (Prototype Phase)

### Phase 1: Signal Capture Validation (Weeks 1-3)

**Goal:** Confirm we can capture clean, useful weld current/voltage signals with cheap hardware.

**Steps:**
1. Assemble breadboard prototype (ESP32-S3 + ACS712 + ADS1115)
2. Write firmware to capture ADC samples at max rate (860 SPS on ADS1115, or 100kSPS on ESP32 internal ADC)
3. Stream raw data to laptop via serial/WiFi
4. Record 10+ welds on a MIG welder (borrow time at local welding school or makerspace)
5. Visualize waveforms in Python, confirm we can see:
   - Arc start/stop events
   - Short-circuit transfer mode oscillations (for GMAW)
   - Deliberate defects (move too fast for cold lap, too slow for burn-through)
6. Compare to published waveform literature -- do our signals match expected patterns?

**Success criteria:** Clean waveform capture showing visible differences between good and intentionally bad welds.

**Hardware needed:** ~$50 in components + access to a MIG welder for testing.

### Phase 2: ML Model Development (Weeks 3-8)

**Goal:** Train a defect classification model that works on captured data.

**Steps:**
1. Collect training data:
   - Partner with welding school (AWS CWI instructor) to create labeled samples
   - Run 200+ welds: 50 good + 50 each of 3 deliberate defect types
   - Record waveforms + photograph/section each coupon for ground truth labels
   - Augment with published datasets (if available) and synthetic perturbations
2. Feature engineering:
   - Extract time-domain features per 10ms window
   - Compute frequency-domain features (FFT)
   - Generate spectrograms for CNN input
3. Model training:
   - Start with Random Forest on engineered features (baseline)
   - Train 1D-CNN on raw waveform windows
   - Train lightweight LSTM for sequential detection
   - Compare accuracy, latency, model size
4. Quantize best model to INT8 for edge deployment
5. Validate on held-out test set (different welder, different operator)

**Success criteria:** >80% accuracy on 4-class classification (good + 3 defect types) on held-out data from a DIFFERENT welder than training.

**Critical risk:** If accuracy is <70% on cross-welder validation, the fundamental approach may not work with cheap sensors. Need higher-resolution ADC or additional sensor modalities.

### Phase 3: Edge Deployment (Weeks 8-11)

**Goal:** Run ML inference on ESP32-S3 in real-time.

**Steps:**
1. Convert trained model to TensorFlow Lite format
2. Quantize to INT8 (post-training quantization or quantization-aware training)
3. Deploy to ESP32-S3 using TFLite Micro runtime
4. Measure inference latency (target: <100ms per classification)
5. Implement LED output logic (green/yellow/red based on classification confidence)
6. Add WiFi data upload (MQTT to AWS IoT Core)
7. Test in real welding environment (EMI robustness, heat, vibration)
8. Iterate on EMI shielding if needed

**Success criteria:** Real-time classification on ESP32-S3 with <200ms latency, surviving 8 hours of continuous operation next to a running welder.

### Phase 4: Pilot Deployment (Weeks 11-16)

**Goal:** Deploy 5-10 units in a real fabrication shop for 4-6 weeks.

**Steps:**
1. Build 10 semi-production units (custom PCB from JLCPCB, 3D-printed enclosure)
2. Install at partner fab shop (structural steel or pressure vessel)
3. Run alongside their normal quality process (NDT continues as usual)
4. Compare our classifications to their NDT results (confusion matrix)
5. Iterate model based on production data (retrain with new labeled samples)
6. Measure: false positive rate, false negative rate, operator feedback

**Success criteria:** 
- >85% agreement with NDT results on defect detection
- <15% false positive rate (too many false alarms = operators ignore the system)
- Positive operator feedback (not annoying, actually useful)
- System reliability >99% uptime over 4 weeks

## Risk Register

| # | Risk | Probability | Impact | Mitigation | Status |
|---|------|-------------|--------|------------|--------|
| R1 | ML accuracy insufficient in production (<80%) | MEDIUM | CRITICAL | Start with easier problem (binary good/bad only). Add sensor channels. Use higher-res ADC. | Open |
| R2 | EMI from welding arc corrupts sensor readings | MEDIUM | HIGH | Shielded cables, differential sensing, ferrite beads, galvanic isolation (ISO7741). Budget $10 extra for shielding. | Open |
| R3 | Model does not generalize across welder brands | MEDIUM | HIGH | Collect training data from 3+ brands. Use domain adaptation techniques. Include "machine state" features. | Open |
| R4 | Cannot acquire sufficient labeled training data | MEDIUM | HIGH | Partner with welding school (AWS Sense). Offer free hardware in exchange for data. Hire CWI part-time. | Open |
| R5 | Welders/operators resist "monitoring" device | MEDIUM | MEDIUM | Frame as quality aid for the welder, not management surveillance. Provide direct feedback to welder only. | Open |
| R6 | IP65 enclosure insufficient for welding env | LOW | MEDIUM | Test in actual environment. May need IP67 or conformal coating. Add $3-5 to BOM. | Open |
| R7 | Product liability if system misses a critical defect | LOW | CRITICAL | Position as "screening aid" not "certified inspection." Strong disclaimers. Product liability insurance ($5K/year). Legal review. | Open |
| R8 | WiFi unreliable in metal shop environment | MEDIUM | LOW | Edge inference works offline. WiFi only for upload. Add local SD card logging as backup. Consider LoRa for bad WiFi. | Open |
| R9 | ESP32-S3 insufficient for complex ML models | MEDIUM | MEDIUM | Fall back to STM32H7 (+$10 BOM). Or use simpler model (RF instead of CNN). Or edge-compute on Raspberry Pi CM4 (+$35). | Open |
| R10 | Competitor OEM adds cross-brand monitoring | LOW | HIGH | Move fast, lock in customers with annual contracts, build data moat before they react. 18-36 month window. | Open |

## Validation Plan

### Technical Validation Gates

| Gate | Criteria | Timeline | Investment to reach | Go/No-Go |
|------|----------|----------|--------------------|---------:|
| G1 | Clean signal capture from 3 different welders | Week 3 | $500 (hardware + welder access) | Must pass to continue |
| G2 | >80% classification accuracy on lab data | Week 8 | $5K (welding school time + CWI) | Must pass to continue |
| G3 | Real-time inference on ESP32-S3, <200ms | Week 11 | $2K (PCB prototyping) | Must pass (or pivot to STM32) |
| G4 | >85% accuracy in production pilot, <15% FP rate | Week 16 | $15K (10 units + pilot support) | Must pass for commercial launch |
| G5 | 3+ pilot customers willing to pay $500 + $150/mo | Week 18 | $5K (sales/travel) | Must pass for Series A |

### Market Validation Gates

| Gate | Criteria | Timeline | Method |
|------|----------|----------|--------|
| M1 | 10+ fab shops express interest in pilot | Month 2 | Cold outreach + LinkedIn + trade shows |
| M2 | 3+ shops sign LOI for pilot (free hardware, feedback commitment) | Month 3 | Direct sales conversations |
| M3 | 1+ pilot shop confirms willing to pay post-pilot | Month 5 | Pilot results + pricing conversation |
| M4 | First 10 paid customers | Month 8 | Direct sales + referrals |

## Cost & Time Estimate

### Bootstrap Budget ($250K allocation)

| Category | Amount | Timeline | Detail |
|----------|--------|----------|--------|
| Hardware prototyping | $5K | Month 1-3 | Components, PCBs, test equipment |
| Welding school partnership | $10K | Month 1-4 | Facility time, CWI consultant, consumables |
| PCB design + manufacturing (10 pilot units) | $8K | Month 3-4 | JLCPCB + assembly + enclosures |
| Cloud infrastructure | $5K | Month 2-12 | AWS (IoT Core, ECS, RDS, S3) |
| Founder salary (12 months, reduced) | $120K | Month 1-12 | Below-market to conserve runway |
| Embedded engineer (contract, 3 months) | $45K | Month 2-5 | PCB design + firmware (critical skill gap) |
| Legal (IP, liability, terms) | $15K | Month 4-6 | Patent provisional + product liability |
| Travel + sales | $12K | Month 4-12 | Customer visits, trade shows (FABTECH) |
| Product liability insurance | $5K | Month 6-12 | Required before commercial deployment |
| Contingency (10%) | $25K | - | Unknown unknowns |
| **TOTAL** | **$250K** | **12 months** | |

### Timeline

```
Month 1-2:   Signal capture validation (Gate G1)
Month 2-4:   ML model development + training data collection (Gate G2)
Month 3-5:   PCB design + embedded engineering (contract)
Month 4-5:   Edge deployment + EMI testing (Gate G3)
Month 5-7:   Pilot deployment at 2-3 fab shops (Gate G4)
Month 7-8:   Iterate model, fix issues from pilot
Month 8-9:   First paid customers, production manufacturing
Month 9-12:  Scale to 30+ customers, build repeatable sales motion
Month 12:    $510K revenue target, raise seed round if scaling
```

## Founder-Market Fit Assessment

**Founder profile:** AI/ML infrastructure engineer, deep Python/systems/cloud, no hardware background.

| Dimension | Fit | Gap | Mitigation |
|-----------|-----|-----|------------|
| ML/AI expertise | STRONG | None -- core competency | N/A |
| Cloud/backend engineering | STRONG | None | N/A |
| Python data science | STRONG | None | N/A |
| Edge ML deployment | MODERATE | Has done cloud ML, not embedded ML | TFLite Micro tutorials, ESP32 community is excellent |
| Hardware/embedded systems | WEAK | No PCB design, no firmware, no sensor experience | Contract embedded engineer ($45K for 3 months). This is the critical hire. |
| Welding domain knowledge | WEAK | No welding background | Partner with AWS CWI. Attend welding school intro course ($500, 1 week). Read IIW/AWS papers. |
| Manufacturing/operations | WEAK | No experience shipping hardware at scale | Use contract manufacturer (JLCPCB for PCB, local for assembly). Hire ops person at scale. |
| Sales to industrial buyers | MODERATE | B2B SaaS sales experience transfers. But industrial buyers are different (trade shows, distributors, relationships). | Start with direct sales to pilot customers. Hire industrial sales rep at 20+ customers. |
| Regulatory/compliance | WEAK | No experience with industrial product liability | Engage product liability attorney early ($5K). Join AWS (American Welding Society) as corporate member. |

**Overall founder-market fit: 5/10**

**Critical gap:** Hardware/embedded engineering. The ML and cloud side is well-covered, but this product lives and dies on the sensor hardware working reliably in a harsh environment. The contract embedded engineer hire in months 2-5 is non-negotiable.

**Compensating strengths:**
- ML expertise is the CORE differentiator -- no competitor has this depth
- Cloud/systems background means the SaaS platform will be well-built
- Data pipeline expertise is critical for the training data moat strategy
- Fast iteration speed on the ML side while hardware is contracted out

**Founder development plan:**
1. Week 1-4: Complete ESP32 crash course (tons of free content, large maker community)
2. Week 1-2: Take intro welding class at local community college or makerspace
3. Month 2: Hire contract embedded engineer, work closely to learn PCB/firmware basics
4. Month 3-4: Attend FABTECH or local AWS Section meeting to build welding industry network
5. Ongoing: Read 2-3 welding metallurgy papers per week to build domain intuition
