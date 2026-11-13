# Feasibility & Prototype Plan: CNC Tool Wear Acoustic Detection

## Architecture

```
+------------------------+     +-------------------+     +-------------------+
|  Sensor Unit (On-CNC)  |     |   Cloud Backend   |     |   User Interfaces |
|                        |     |                   |     |                   |
| +------------------+   |     | +---------------+ |     | Mobile App        |
| | 3x ICS-43434    |   |     | | API Gateway   | |     | - Traffic light   |
| | MEMS Mics       |   |     | | (FastAPI)     | |     | - Alerts/push     |
| +------------------+   |     | +---------------+ |     |                   |
|   |                    |     |   |               |     | Web Dashboard     |
|   v                    |     |   v               |     | - Fleet view      |
| +------------------+   |     | +---------------+ |     | - Tool life stats |
| | STM32H7 MCU     |   |     | | ML Inference  | |     | - Analytics       |
| | (DSP + FFT)     |   |     | | (ONNX/Python) | |     +-------------------+
| +------------------+   | WiFi| +---------------+ |
|   |                    |---->|   |               |
|   v                    | TLS |   v               |
| +------------------+   |     | +---------------+ |
| | ESP32-S3        |   |     | | TimescaleDB   | |
| | (WiFi + BLE)    |   |     | | (Features DB) | |
| +------------------+   |     | +---------------+ |
|   |                    |     | +---------------+ |
| +------------------+   |     | | ML Training   | |
| | Local LED/Buzzer |   |     | | (PyTorch)     | |
| | (Green/Yellow/   |   |     | +---------------+ |
| |  Orange/Red)     |   |     +-------------------+
| +------------------+   |
| +------------------+   |
| | 5V USB-C Power   |   |
| +------------------+   |
+------------------------+
```

### Component Breakdown

**Sensor Unit (Hardware on each CNC machine)**
- 3x MEMS microphones (ICS-43434) in triangular array for spatial filtering and noise cancellation
- STM32H7 microcontroller: 480MHz Cortex-M7 with hardware DSP/FPU for real-time FFT computation
- Computes 4096-point FFT at 48kHz sample rate (frequency resolution: 11.7Hz, covers tool wear bands 1-24kHz)
- Extracts acoustic features on-device: spectral centroid, spectral flux, MFCC coefficients, RMS energy, crest factor
- ESP32-S3 handles WiFi connectivity, TLS encryption, data transmission to cloud
- Local status LEDs (RGB) + piezo buzzer for immediate on-machine feedback
- Enclosure: IP54 rated (dust-resistant, splash-resistant) ABS plastic, magnetic mounting
- Power: 5V USB-C (standard phone charger) or 24V DC barrel jack (from machine aux power)

**Edge Processing Pipeline (On-Device)**
- Raw audio -> anti-aliasing filter -> 48kHz ADC -> 4096-point FFT (every 85ms)
- FFT -> feature extraction (12 features per frame): spectral centroid, bandwidth, rolloff, flux, 8 MFCC coefficients
- Feature frames batched (10 frames = ~850ms window) -> compressed -> sent to cloud
- Local inference: lightweight anomaly threshold on spectral energy in tool-wear frequency bands (6-18kHz) for instant RED alert even without cloud connectivity
- Data rate: ~2KB/second to cloud during active cutting

**Cloud Backend (Multi-Tenant SaaS)**
- FastAPI application server (Python 3.11+)
- TimescaleDB for time-series feature storage
- ML inference pipeline: receives feature vectors, runs classification model, returns tool state
- Model training pipeline: nightly retraining per tool-type/material combination as labeled data grows
- Multi-tenant: per-customer data isolation, shared base models with customer-specific fine-tuning
- Deployment: AWS (ECS Fargate + RDS + S3)

**ML Pipeline**
- Classification model: 1D-CNN + LSTM hybrid for temporal pattern recognition in spectral features
- Classes: FRESH (0-25% life), NORMAL (25-75%), APPROACHING_EOL (75-90%), DANGER (>90% / anomalous)
- Training data: public datasets (NIST, academic) + customer data as it accumulates
- Transfer learning: base model trained on aluminum end milling, fine-tuned per customer/material/tool
- Inference latency: <200ms from feature arrival to classification result

---

## Bill of Materials (BOM) -- Per Sensor Unit

### Hardware BOM (Per Unit, Production Volume 100)

| Component | Part Number | Qty | Unit Cost | Extended | Confidence |
|-----------|-------------|-----|-----------|----------|------------|
| MEMS Microphone | ICS-43434 (TDK InvenSense) | 3 | $1.10 | $3.30 | VERIFIED (Digi-Key qty 100) |
| MCU (DSP) | STM32H743VIT6 | 1 | $12.50 | $12.50 | VERIFIED (Digi-Key qty 100) |
| WiFi/BLE Module | ESP32-S3-WROOM-1 | 1 | $3.20 | $3.20 | VERIFIED (Digi-Key qty 100) |
| PCB (4-layer, 50x70mm) | Custom | 1 | $4.00 | $4.00 | ASSUMED (JLCPCB qty 100) |
| USB-C connector + power regulation | Various | 1 | $2.50 | $2.50 | VERIFIED |
| RGB LED (WS2812B) | WS2812B-V5 | 3 | $0.10 | $0.30 | VERIFIED |
| Piezo buzzer | CEM-1203(42) | 1 | $0.80 | $0.80 | VERIFIED |
| Passive components (caps, resistors, crystals) | Various | ~30 | $0.05 | $1.50 | ASSUMED |
| Enclosure (ABS, IP54) | Custom injection mold / 3D printed | 1 | $5.00 | $5.00 | ASSUMED ($5 at 100 qty from China; $15 if 3D printed for prototype) |
| Magnetic mount (neodymium) | N52 20mm disc | 2 | $1.50 | $3.00 | VERIFIED (Amazon) |
| Cable (USB-C, 2m) | Standard | 1 | $2.00 | $2.00 | VERIFIED |
| Conformal coating (humidity protection) | Spray | 1 | $0.50 | $0.50 | ASSUMED |
| Assembly labor (pick-and-place + hand solder) | -- | 1 | $5.00 | $5.00 | ASSUMED (Seeed Studio turnkey) |
| **TOTAL PER UNIT** | | | | **$43.60** | |

**Note**: At volume 1,000, unit cost drops to ~$28-32 (PCB, enclosure, and component volume discounts).

### Prototype Hardware Costs (First 10 Units)

| Item | Cost | Confidence | Notes |
|------|------|------------|-------|
| Development board: STM32H7 Nucleo (NUCLEO-H743ZI2) | $45 | VERIFIED | For firmware development |
| Development board: ESP32-S3-DevKitC | $10 | VERIFIED | For WiFi/cloud connectivity dev |
| ICS-43434 breakout boards (Adafruit/SparkFun) | $30 (3x $10) | VERIFIED | For acoustic prototyping before custom PCB |
| Logic analyzer (Saleae Logic 8) | $200 | VERIFIED | For debugging I2S/SPI protocols |
| Custom PCB prototype (5 boards) | $150 | VERIFIED | JLCPCB, including stencil |
| Components for 10 prototype units | $200 | ASSUMED | Digi-Key small quantities |
| 3D printed enclosures (10 units) | $150 | ASSUMED | Resin print, $15 each |
| Test CNC machine time (local makerspace/shop) | $500 | ASSUMED | 20 hours x $25/hr |
| Oscilloscope (if not owned) | $400 | VERIFIED | Rigol DS1054Z |
| **PROTOTYPE HARDWARE TOTAL** | **~$1,685** | | |

### Development Costs (Months 1-8)

| Item | Cost | Confidence | Notes |
|------|------|------------|-------|
| Founder salary (ML/software, no salary) | $0 | VERIFIED | Founder contribution |
| Contract embedded engineer (4 months) | $48,000 | ASSUMED | $12K/month for STM32 firmware + PCB design |
| Contract frontend/mobile dev (3 months) | $36,000 | ASSUMED | $12K/month for React dashboard + React Native app |
| Cloud infrastructure (development) | $1,200 | VERIFIED | AWS, 8 months x $150/month |
| Domain + branding | $1,500 | VERIFIED | Domain, logo, landing page |
| Legal (incorporation, IP) | $5,000 | ASSUMED | Delaware C-corp + provisional patent |
| CNC shop partnerships (testing access) | $2,000 | ASSUMED | Buy shop owners lunch + pay for test time |
| ML training compute (GPU instances) | $800 | VERIFIED | AWS spot instances for model training |
| **DEVELOPMENT TOTAL** | **~$96,185** | | |

### Manufacturing (First 100 Units)

| Item | Cost | Confidence | Notes |
|------|------|------------|-------|
| PCB assembly (100 units, Seeed/JLCPCB) | $4,360 | VERIFIED | $43.60 x 100 units |
| FCC/CE certification testing | $8,000 | ASSUMED | Required for intentional radiator (WiFi) |
| Injection mold tooling (enclosure) | $3,000 | ASSUMED | Simple 2-part mold from China |
| Packaging + shipping materials | $500 | ASSUMED | Simple box + instruction card |
| Quality testing (10% sample) | $1,000 | ASSUMED | Functional test of sample units |
| **MANUFACTURING TOTAL** | **~$16,860** | | |

### Go-to-Market Costs

| Item | Cost | Confidence | Notes |
|------|------|------------|-------|
| Trade show (IMTS / Eastec -- attend, no booth) | $3,000 | ASSUMED | Travel + registration |
| YouTube/Instagram content creation | $2,000 | ASSUMED | Demo videos, shop visits |
| Practical Machinist / CNCzone forum engagement | $0 | VERIFIED | Time only |
| Google Ads (CNC tool breakage keywords) | $6,000 | ASSUMED | $1K/month x 6 months |
| Local machine shop visits (first customers) | $2,000 | ASSUMED | Drive time + coffee/lunch |
| **GTM TOTAL** | **~$13,000** | | |

### Total Capital Required

| Phase | Cost | Cumulative |
|-------|------|-----------|
| Prototype development (months 1-4) | $96,185 | $96,185 |
| Manufacturing first batch (month 5-6) | $16,860 | $113,045 |
| Go-to-market (months 4-8) | $13,000 | $126,045 |
| Working capital buffer (3 months) | $36,000 | $162,045 |
| Contingency (30%) | $48,600 | $210,645 |
| **TOTAL** | **~$215,000** | |

**Confidence: MEDIUM** -- hardware development has higher uncertainty than pure software. The 30% contingency accounts for PCB respins, firmware delays, and unexpected environmental challenges.

---

## Software Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Firmware (DSP) | C/C++ on STM32H7 (STM32CubeIDE) | Real-time DSP, hardware FFT acceleration, deterministic timing |
| Firmware (WiFi) | ESP-IDF (C) on ESP32-S3 | Mature WiFi stack, TLS support, OTA updates |
| Communication | MQTT over TLS | Lightweight IoT protocol, handles intermittent connectivity |
| API Server | FastAPI (Python 3.11) | Rapid development, async, good ML ecosystem |
| ML Training | PyTorch + torchaudio | Best audio ML ecosystem, pretrained models |
| ML Inference | ONNX Runtime | Fast inference, deployable everywhere |
| Time-Series DB | TimescaleDB | SQL + time-series optimization |
| Cache/Queue | Redis | MQTT message buffering, real-time state |
| Frontend | React + TypeScript + Tailwind | Standard, fast iteration |
| Mobile App | React Native | Cross-platform from single codebase |
| Real-time | WebSocket | Live traffic light updates |
| Hosting | AWS (ECS + RDS + IoT Core) | IoT Core handles MQTT at scale |
| CI/CD | GitHub Actions | Simple, integrated |
| OTA Updates | AWS IoT + custom bootloader | Essential for field firmware updates |
| Monitoring | Grafana Cloud | Device fleet + backend observability |

---

## Build Instructions (Sprint Plan)

### Phase 1: Proof of Concept (Months 1-2)

**Sprint 1 (Weeks 1-2): Acoustic Capture Validation**
- Buy STM32H7 Nucleo board + ICS-43434 breakout board
- Write firmware to capture audio at 48kHz via I2S interface
- Implement 4096-point FFT using CMSIS-DSP library (hardware-accelerated)
- Visualize spectrum in real-time on laptop (serial -> Python -> matplotlib)
- **CRITICAL TEST**: Record audio from an actual CNC machine cutting (visit local shop). Verify that tool wear frequency bands (6-18kHz) are detectable above noise floor. If NOT detectable, entire project thesis fails -- STOP HERE.

**Sprint 2 (Weeks 3-4): Feature Extraction + Initial ML**
- Implement feature extraction on STM32: spectral centroid, flux, MFCC (8 coefficients)
- Collect labeled data: record 20+ tool wear progressions (fresh -> worn -> broken) from:
  - YouTube machining videos (audio channel)
  - Public datasets (PHM 2010 challenge, NIST)
  - Local shop visits (bring recorder)
- Train initial classifier (PyTorch, on laptop) using spectral features
- Measure classification accuracy on held-out test set
- **GO/NO-GO gate**: If classifier achieves <60% accuracy on lab data, fundamental approach needs rethinking.

### Phase 2: Working Prototype (Months 3-4)

**Sprint 3 (Weeks 5-6): Custom PCB + Enclosure**
- Design PCB in KiCad: STM32H7 + 3x ICS-43434 + ESP32-S3 + power regulation + LEDs
- Order from JLCPCB (5 boards, 10 day lead time)
- Design enclosure in FreeCAD/Fusion 360, 3D print in PETG
- Assemble first 3 prototype units
- Write ESP32 firmware: WiFi provisioning, MQTT client, TLS

**Sprint 4 (Weeks 7-8): Cloud Backend + Dashboard**
- Deploy FastAPI backend on AWS (ECS Fargate)
- MQTT broker (AWS IoT Core) receives feature vectors from devices
- Inference pipeline: feature arrival -> ONNX model -> classification -> store + push
- Basic React dashboard: list of machines, traffic light status, alert history
- Mobile push notifications via Firebase Cloud Messaging

### Phase 3: Real-World Validation (Months 5-6)

**Sprint 5 (Weeks 9-10): Field Testing**
- Install 3 prototype units in 2-3 different CNC shops
- Run for 2-4 weeks continuous
- Collect LABELED data: ask operators to note tool changes and any tool failures
- Measure: detection rate, false alarm rate, signal quality in various environments
- Iterate firmware: adjust gain, add digital filtering, tune frequency bands

**Sprint 6 (Weeks 11-12): Model Improvement + Product Polish**
- Retrain model with real-world labeled data (50-100 tool life cycles)
- Implement adaptive threshold per machine (account for different noise floors)
- Add "learning mode" (first 24 hours on a new machine = baseline collection)
- Polish dashboard: tool life charts, alert configuration, machine settings
- Write user documentation / setup guide

### Phase 4: Production Prep (Months 7-8)

**Sprint 7 (Weeks 13-14): Manufacturing Readiness**
- PCB design-for-manufacturing review (DFM check with Seeed/JLCPCB)
- FCC pre-compliance testing (rent time at local EMC lab, ~$2K)
- Order first production batch (100 units)
- Set up OTA firmware update mechanism
- Implement device provisioning flow (zero-touch onboarding)

**Sprint 8 (Weeks 15-16): Launch Prep**
- Finalize pricing and subscription billing (Stripe)
- Build landing page with demo video
- Write case study from field test results
- Prepare for first 10 paying customers
- Submit for FCC/CE certification

---

## Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| 1 | MEMS mics cannot detect tool wear above shop ambient noise | MEDIUM | CRITICAL | Array beamforming for spatial filtering. Validate in Sprint 1 before spending more capital. High-pass filter to eliminate low-freq shop noise. Focus on 6-18kHz band. Mount close to spindle. |
| 2 | Coolant splash degrades microphone performance over time | MEDIUM | HIGH | IP54 enclosure with acoustic membrane (Gore-Tex style). Mount OUTSIDE machine enclosure. Replaceable membrane. |
| 3 | ML model doesn't generalize across tool types/materials | HIGH | MEDIUM | Start with ONE material (aluminum) and ONE operation (end milling). Transfer learning from base model. Require 5-10 tool life cycles for calibration. |
| 4 | PCB design requires multiple respins | MEDIUM | MEDIUM | Hire experienced embedded contractor for PCB design. Use development boards first. Budget 2 respins ($300 each). |
| 5 | WiFi unreliable in metal-heavy shop environments | MEDIUM | MEDIUM | ESP32-S3 external antenna option. Local-only mode with LED indication as fallback. BLE option for phone connectivity. |
| 6 | CNC machinists don't trust/adopt the product | MEDIUM | HIGH | Get influential machinists as beta testers. Video testimonials. Partner with machinist for marketing credibility. |
| 7 | FCC certification fails or is delayed | LOW | MEDIUM | Use pre-certified ESP32 module. Keep PCB layout within reference design. Budget for pre-compliance testing. |
| 8 | Supply chain issues (chip shortage) | LOW | MEDIUM | STM32H7 and ESP32-S3 widely available. ICS-43434 has multiple distributors. Keep 6-month component buffer. |
| 9 | Patent infringement | LOW | HIGH | Our MEMS airborne approach is differentiated from piezoelectric AE sensor patents. File provisional patent early. Freedom-to-operate search ($3-5K). |
| 10 | Machine enclosure attenuates acoustic signal | MEDIUM | MEDIUM | Sound leaks at joints/doors. Offer internal mounting option with waterproof membrane for fully sealed machines. Test both configurations in Sprint 5. |

---

## Validation Plan

### Technical Validation (Months 1-3) -- MUST PASS BEFORE SPENDING MORE

1. **Signal-to-noise test** (Week 2): Record cutting audio from 3 different CNC machines in operating shop. Compute SNR in 6-18kHz band during cutting vs. idle. Require SNR > 10dB for GO.
2. **Classification accuracy on real data** (Week 4): Train model on collected real-world data. Achieve >70% accuracy distinguishing fresh vs. worn tools.
3. **False alarm rate** (Week 10): During 2-week field test, target <5% false alarm rate (fewer than 1 false alarm per day per machine).
4. **Environmental robustness** (Week 10): Test in 3 different shops. Model accuracy should not degrade more than 15% across environments.

### Market Validation (Months 3-5)

1. **Discovery interviews**: 20+ conversations with CNC shop owners/operators
2. **Beta test commitment**: 5 shops willing to install prototype for free and provide feedback
3. **Willingness to pay**: 3+ shops verbally commit to $49-89/month if product works
4. **Channel validation**: Identify which outreach channel generates most interest

### Business Validation (Months 6-8)

1. **Breakage prevention**: Demonstrate at least 1 avoided tool breakage event during beta
2. **Tool life extension**: Show 10%+ tool life improvement
3. **Subscription conversion**: 3+ beta users convert to paid subscription
4. **Unit economics**: Hardware COGS + cloud costs < 40% of monthly subscription revenue

---

## Cost & Time Estimate Summary

| Metric | Estimate | Confidence |
|--------|----------|-----------|
| Total capital to first revenue | $215K | MEDIUM |
| Time to working prototype | 4 months | MEDIUM-HIGH |
| Time to first field deployment | 5-6 months | MEDIUM |
| Time to first paid customer | 7-8 months | MEDIUM |
| Time to 100 machines deployed | 12-14 months | MEDIUM-LOW |
| Hardware COGS per unit (at 100 qty) | $43.60 | HIGH |
| Hardware COGS per unit (at 1,000 qty) | ~$30 | MEDIUM |
| Monthly cloud cost per machine | ~$3-5 | HIGH |
| Break-even units (monthly) | ~80 machines at $79 avg | MEDIUM |

---

## Founder-Market Fit Assessment

**Founder profile**: ML/infrastructure engineer, deep Python/systems/cloud, NO hardware background, NO CNC/machining background.

### Strengths (What the founder brings)

| Capability | Relevance | Score |
|-----------|-----------|-------|
| ML/AI engineering (model training, inference) | Core to product (acoustic classification model) | 10/10 |
| Python systems programming | Cloud backend, data pipeline, training infrastructure | 9/10 |
| Cloud infrastructure (AWS) | Multi-tenant SaaS backend, IoT Core, deployment | 9/10 |
| Data engineering | Feature pipeline, time-series storage, model retraining | 8/10 |
| Signal processing fundamentals | FFT, filtering, spectral analysis (learnable from ML background) | 6/10 |

### Gaps (What the founder lacks)

| Gap | Severity | Mitigation | Cost |
|-----|----------|-----------|------|
| Embedded systems / firmware development | HIGH | Hire contract embedded engineer (4 months). STM32 + ESP32 well-documented but requires specific expertise. | $48K |
| PCB design and hardware manufacturing | HIGH | Hire contractor for PCB layout. Use JLCPCB/Seeed for manufacturing. | Included in embedded contract |
| CNC machining domain knowledge | HIGH | Partner with a machinist (co-founder or advisor). Spend 40+ hours in CNC shops observing. Join Practical Machinist. Watch 100 hours of CNC YouTube. | Time + $2K for shop access |
| Signal processing / acoustics depth | MEDIUM | Learnable given ML background. Academic literature is extensive. Key algorithms (FFT, MFCC) well-documented. | 4-6 weeks self-study |
| Hardware supply chain / manufacturing | MEDIUM | Use turnkey services (Seeed Studio Fusion). Simple BOM (8 components). | Small premium for turnkey |
| Sales to blue-collar / trades persona | MEDIUM | Partner with machinist for marketing credibility. Simple value prop. Let product demo itself. | Time + partner |

### Overall Founder-Market Fit: 5/10

**Reasoning**: This idea has a genuine founder-market fit gap. The core product requires THREE domains the founder lacks: embedded hardware, CNC machining, and acoustics/signal processing. The ML/cloud expertise is necessary but not sufficient -- it's maybe 30% of the challenge. The remaining 70% (building reliable hardware that works in a harsh industrial environment, understanding tool wear acoustics, and earning trust from machinists) requires expertise the founder must hire or partner for.

**Comparison to ideal founder**: The ideal founder for this product is a CNC machinist who learned to code, or an embedded engineer who ran a machine shop.

**Saving graces**:
- The embedded engineering challenge is well-scoped (can be fully contracted)
- The ML/cloud backend IS the long-term IP and moat (founder's strength)
- Hardware is "dumb sensor" -- complexity is in cloud ML, not in device firmware
- CNC domain knowledge is acquirable (40 hours of shop observation + community immersion)

**Critical requirement**: Founder MUST find either (a) a CNC machinist co-founder/advisor or (b) an embedded engineer with manufacturing sensor experience. Without one of these, the product will not be credible or technically sound.

**Comparable founder profiles that succeeded:**
- Samsara founders: software engineers from Meraki who built IoT hardware for fleets. Key: hired hardware leads early.
- Augury founders: software + acoustics PhD built vibration monitoring for HVAC. Raised $100M+.
- Tulip Interfaces: software engineers built manufacturing platform for shop floors. No manufacturing background. Key: extensive factory floor observation.

The pattern shows: software founders CAN win in hardware-adjacent industrial markets, but only with deep domain immersion and hired hardware expertise.
