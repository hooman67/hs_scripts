# Feasibility & Prototype Plan: CNC Tool Wear Acoustic Detection

## 1. Architecture Overview

```
[MEMS Mic Array] --> [STM32 MCU] --> [WiFi Module] --> [Cloud Backend] --> [Dashboard/Alerts]
     (3x ICS-43434)    (I2S input,       (ESP32 or        (AWS IoT +        (React web app
      + 1x ref mic)     DSP, FFT,        MQTT over        SageMaker         + SMS/email
                         feature          TLS)             inference)         alerting)
                         extraction)

Local fallback: STM32 runs lightweight model --> LED bar (green/yellow/red) + buzzer
```

### Data Flow:
1. MEMS microphones capture audio at 48 kHz sample rate (16-bit I2S)
2. STM32 performs windowed FFT (1024-point, 50% overlap) every 21ms
3. Feature extraction on-device: mel-spectrogram bands, spectral centroid, spectral rolloff, zero-crossing rate
4. Features streamed to cloud every 2 seconds (compressed, ~500 bytes/packet)
5. Cloud ML model (1D-CNN or lightweight transformer) classifies: {healthy, wearing, critical, breakage_imminent}
6. Classification result sent back to device (LED update) and dashboard
7. If classification = critical/breakage_imminent: trigger alert pipeline

### Local-Only Mode (WiFi down):
- STM32 runs quantized TFLite model (~100KB) for basic green/yellow/red classification
- Reduced accuracy (~70% vs ~90% cloud) but functional
- Stores raw features locally (4MB flash buffer = ~2 hours) for later upload

---

## 2. Bill of Materials (Per Prototype Unit)

| Component | Part Number | Qty | Unit Cost | Total | Confidence |
|-----------|-------------|-----|-----------|-------|------------|
| MEMS Microphone (digital, I2S) | TDK/InvenSense ICS-43434 | 3 | $1.05 | $3.15 | VERIFIED (Digi-Key pricing at qty 100) |
| Reference Microphone (noise cancellation) | TDK ICS-43434 | 1 | $1.05 | $1.05 | VERIFIED |
| MCU with DSP | STM32H743VIT6 (480 MHz, FPU, 1MB SRAM) | 1 | $8.50 | $8.50 | VERIFIED (Digi-Key, qty 10) |
| WiFi/BT Module | ESP32-WROOM-32E | 1 | $2.80 | $2.80 | VERIFIED (LCSC pricing) |
| PCB (4-layer, 50x80mm) | Custom via JLCPCB | 1 | $3.00 | $3.00 | ASSUMED ($150 for 50 boards) |
| Enclosure (IP54 rated, ABS) | Hammond 1554C2GY or custom 3D print | 1 | $8.00 | $8.00 | ASSUMED (injection mold at scale: $2) |
| Magnetic Mount (N52 neodymium) | Custom bracket + 2x 20mm disc magnets | 1 | $4.00 | $4.00 | ASSUMED |
| Power: USB-C connector + 5V regulator | Various (LM1117-3.3 + USB-C receptacle) | 1 | $2.00 | $2.00 | VERIFIED |
| LED Bar (WS2812B, 8 LEDs) | WS2812B strip, cut to 8 | 1 | $1.50 | $1.50 | VERIFIED |
| Buzzer (piezo, 85dB) | CUI Devices CPT-2038-80 | 1 | $0.80 | $0.80 | VERIFIED |
| Passive components (caps, resistors, crystals) | Various | lot | $2.00 | $2.00 | ASSUMED |
| SPI Flash (feature buffer) | W25Q32JV (4MB) | 1 | $0.50 | $0.50 | VERIFIED |
| Antenna (2.4 GHz ceramic) | Johanson 2450AT18B100E | 1 | $0.30 | $0.30 | VERIFIED |
| USB-C Cable (2m, industrial grade) | Off-shelf | 1 | $3.00 | $3.00 | VERIFIED |
| Conformal coating (moisture protection) | MG Chemicals 419D | per unit | $0.50 | $0.50 | ASSUMED |
| **TOTAL BOM (prototype)** | | | | **$41.10** | |
| **TOTAL BOM (production, qty 1000)** | | | | **~$28-32** | UNVERIFIED (estimated 25% volume discount) |

### BOM Notes:
- ICS-43434 chosen over SPH0641LU4H (ultrasonic, 80 kHz bandwidth) for prototype. If testing shows need for >20 kHz, switch to SPH0641LU4H at ~$2.50 each (adds $4.50 to BOM).
- STM32H743 is overkill for prototype (chosen for DSP horsepower and development flexibility). Production could use STM32H723 (~$5) or STM32U585 (~$4) for lower cost.
- ESP32-WROOM is separate from STM32 in prototype for debugging. Production revision could use STM32 with WiFi (STM32WB series) or single ESP32-S3 (has I2S + WiFi + ML accelerator, $3.50 total, replaces both chips).

### Alternative Architecture (Lower BOM, Higher Risk):
Replace STM32 + ESP32 with single ESP32-S3:
- ESP32-S3-WROOM-1 ($3.50) has I2S, WiFi, BT, 240MHz dual-core, PSRAM
- BOM drops to ~$25 per unit
- Risk: ESP32-S3 DSP performance may be insufficient for real-time FFT at 48 kHz x 4 channels
- Decision: Prototype with STM32+ESP32 (safe), optimize to ESP32-S3 for production if feasible

---

## 3. Software Stack

| Layer | Technology | License | Cost |
|-------|-----------|---------|------|
| **Firmware** | STM32 HAL + CMSIS-DSP + TensorFlow Lite Micro | Apache 2.0 / BSD | Free |
| **Firmware RTOS** | FreeRTOS | MIT | Free |
| **WiFi Firmware** | ESP-IDF (Espressif IoT Development Framework) | Apache 2.0 | Free |
| **Cloud IoT** | AWS IoT Core (MQTT) | Proprietary (usage-based) | ~$1/month per 1000 devices |
| **ML Training** | Python + PyTorch + torchaudio | BSD | Free |
| **ML Inference (cloud)** | AWS SageMaker Serverless or Lambda + ONNX Runtime | Proprietary | ~$0.10/device/month |
| **ML Inference (edge)** | TensorFlow Lite Micro (quantized INT8) | Apache 2.0 | Free |
| **Backend API** | Python FastAPI on AWS Lambda | MIT | ~$5/month at 500 devices |
| **Database** | AWS DynamoDB (time-series features) + S3 (raw audio samples) | Proprietary | ~$20/month at 500 devices |
| **Dashboard Frontend** | React + Vite + Tailwind CSS | MIT | Free |
| **Alerting** | AWS SNS (SMS) + SES (email) | Proprietary | ~$0.01/alert |
| **Monitoring** | AWS CloudWatch | Proprietary | ~$5/month |
| **PCB Design** | KiCad 8 | GPL | Free |
| **Firmware IDE** | STM32CubeIDE | Proprietary (free) | Free |
| **Version Control** | Git + GitHub | Free tier | Free |

**Total cloud cost at 500 devices:** ~$50-100/month (well within $99/device/month subscription revenue)

**Total software licensing cost:** $0 (all open-source or free-tier)

---

## 4. Step-by-Step Build Instructions (First Prototype)

### Phase 0: Validation Rig (Week 1-2) - Cost: ~$150

**Goal:** Confirm MEMS mics can capture useful acoustic signatures from CNC cutting.

1. **Order:**
   - 1x Adafruit I2S MEMS Microphone Breakout (SPH0645LM4H) - $7
   - 1x ESP32-S3-DevKitC-1 - $10
   - 1x USB sound card (for reference recording) - $15
   - 1x Knowles SPH0641LU4H breakout (ultrasonic MEMS, if available) - $25
   - Jumper wires, breadboard - $10
   - 3D printed mount (or hot glue + magnets) - $5

2. **Assemble:** Wire I2S mic to ESP32-S3 dev board. Power via USB.

3. **Record:** Mount on CNC machine (borrow time at local makerspace or Techshop). Record:
   - Air cutting (spindle on, no material)
   - Healthy cutting (new tool, aluminum 6061)
   - Worn tool cutting (use a visibly worn endmill)
   - Chatter (intentionally cause with wrong speeds/feeds)
   - Background shop noise (no cutting)

4. **Analyze:** Use Python (librosa + matplotlib) to visualize spectrograms. Determine:
   - Are wear signatures visible in 0-20 kHz range?
   - Is signal-to-noise ratio sufficient with shop noise?
   - What frequency bands carry the most information?

5. **Decision gate:** If clear spectral differences exist between healthy/worn/chatter in 0-20 kHz, proceed. If not, test ultrasonic MEMS (0-80 kHz). If still insufficient, STOP (fundamental approach may not work with MEMS).

### Phase 1: ML Model Development (Week 2-6) - Cost: ~$500

1. **Data collection:** Partner with 1-2 local CNC shops. Mount validation rig on 3-5 machines. Record 100+ hours of cutting across:
   - 3+ materials (aluminum, mild steel, stainless)
   - 5+ tool types (2-flute, 4-flute, ball end, face mill, drill)
   - Full tool life cycles (new tool to failure)
   - Label data: tool change records from shop + operator annotations

2. **Feature engineering:**
   - Mel-spectrogram (128 bands, 0-20 kHz)
   - Spectral centroid, bandwidth, rolloff
   - MFCCs (13 coefficients)
   - RMS energy in bands (0-2 kHz, 2-8 kHz, 8-20 kHz)
   - Zero-crossing rate
   - Temporal features (rate of change over 10-second windows)

3. **Model training:**
   - Architecture: 1D-CNN (4 conv layers + 2 dense) or small LSTM
   - Input: 2-second windows of mel-spectrogram
   - Output: {healthy, wearing, critical, breakage_imminent} classification
   - Training: 80/10/10 split (train/val/test), per-machine and cross-machine evaluation
   - Target: >85% accuracy on held-out test set, >90% recall on "critical" class

4. **Edge model:**
   - Quantize to INT8 using TFLite converter
   - Target: <100KB model size, <50ms inference on STM32H7
   - Accept 5-10% accuracy drop from quantization

### Phase 2: Custom Hardware Prototype (Week 4-8) - Cost: ~$800

1. **PCB Design (KiCad):**
   - 4-layer PCB, 50x80mm
   - STM32H743 + 3x ICS-43434 (I2S bus) + ESP32-WROOM + LED bar + buzzer
   - USB-C power input with ESD protection
   - SPI flash for local data buffer
   - Debug header (SWD + UART)

2. **Order PCB:** JLCPCB, 5 boards ($30 total with assembly of passives)

3. **Order components:** Digi-Key/Mouser, ~$200 for 5 units worth

4. **Assembly:** Hand-solder QFP and connectors (or use JLCPCB SMT assembly for $50 extra)

5. **Enclosure:** 3D print IP54-rated enclosure with magnetic mount integrated. Material: ASA or PETG for heat resistance.

6. **Firmware:**
   - I2S DMA capture at 48 kHz x 4 channels
   - Real-time FFT using CMSIS-DSP (arm_cfft_f32)
   - Feature extraction pipeline (mel-spectrogram computation)
   - TFLite Micro inference loop
   - MQTT publish over WiFi (ESP32 handles TCP/TLS stack)
   - LED bar + buzzer control based on classification output
   - OTA firmware update capability

### Phase 3: Cloud Backend + Dashboard (Week 6-10) - Cost: ~$200

1. **AWS IoT Core:** Device provisioning, MQTT broker, message routing
2. **Lambda functions:** Receive features, run cloud model inference, store results
3. **DynamoDB:** Time-series storage of classifications and features per device
4. **SageMaker:** Model training pipeline (retrain weekly with new data)
5. **React Dashboard:**
   - Real-time machine status (green/yellow/red per device)
   - Historical tool wear curves
   - Alert configuration (thresholds, notification preferences)
   - Tool life analytics (actual vs. expected)
6. **Alerting:** SNS for SMS, SES for email, webhook for Slack/Teams integration

### Phase 4: Beta Deployment (Week 8-14) - Cost: ~$2000

1. Install 10-20 units across 3-5 partner shops
2. Collect labeled data (operator confirms/denies alerts)
3. Iterate on ML model with real-world data
4. Measure: false positive rate, detection rate, time-to-detection
5. User feedback on dashboard, alert frequency, installation difficulty

### Phase 5: Commercial Launch Preparation (Week 14-20)

1. FCC/CE certification for production hardware (if selling, required for intentional radiator)
2. Production PCB revision (cost-optimized, DFM review)
3. Injection mold enclosure tooling
4. Marketing site + Shopify store
5. First 50-unit production run via contract manufacturer

---

## 5. Risk Register

| # | Risk | Likelihood | Impact | Mitigation | Fallback |
|---|------|-----------|--------|------------|----------|
| 1 | MEMS frequency range (0-20 kHz) insufficient for key wear signatures | 30% | FATAL | Test ultrasonic MEMS (SPH0641LU4H, 80 kHz) in Phase 0 validation | Add one industrial AE sensor (~$50) as hybrid approach; BOM goes to $90 but still 100x cheaper than Montronix |
| 2 | Shop noise (coolant, adjacent machines, compressors) overwhelms signal | 40% | HIGH | Beamforming array (3 mics directional), reference mic for noise cancellation, train on noisy data | Require mounting inside machine enclosure (less convenient but much lower noise) |
| 3 | ML model does not generalize across machine types | 25% | HIGH | Transfer learning architecture; per-machine fine-tuning with 30-min baseline; start with single machine model (Haas VF-2 only) | Offer "machine-specific" product initially; each new machine type requires data collection partnership |
| 4 | False positive rate too high (operator ignores alerts) | 35% | MEDIUM | Conservative thresholds; "learning mode" for first week; operator feedback loop to retrain | Two-tier alerting: "watch" (yellow, dashboard only) vs. "act" (red, SMS) with different thresholds |
| 5 | WiFi unreliable in metal shop environment | 20% | MEDIUM | Test WiFi signal strength in real shops during Phase 0; use ESP32 long-range mode; metal enclosure antenna placement | Offer Ethernet version (add W5500 chip, $2); or LoRa for shops with no WiFi |
| 6 | Founder has no hardware experience | 50% | MEDIUM | Use dev boards for prototype; hire freelance embedded engineer for PCB design ($3-5K); use JLCPCB assembly service | Partner with hardware design firm for production (e.g., Tempo Automation, $10-20K for production design) |
| 7 | CNC shop owners unwilling to share acoustic data | 20% | MEDIUM | Offer free hardware + 6 months free service for beta partners; data sharing agreement with clear IP ownership | Collect data from own purchased machine (Tormach 1100M: ~$12K) in controlled environment |
| 8 | Regulatory (FCC Part 15 for intentional radiator) | 10% | MEDIUM | Use pre-certified WiFi module (ESP32-WROOM has FCC cert); only need unintentional radiator testing for PCB | Use USB connection to existing shop PC instead of WiFi (no FCC needed for passive device) |
| 9 | Latency too high for real-time alerting via cloud | 15% | LOW | Edge inference for critical alerts (local buzzer + LED); cloud only for dashboard and analytics | Full edge-only mode with periodic sync |
| 10 | Competitor launches similar product during development | 10% | MEDIUM | Ship fast (20-week target); build data moat; focus on ease of install as differentiator | Pivot to OEM partnership (license technology to Haas/DMG Mori) |

---

## 6. Validation Plan

### Success Criteria (Phase 0 - Must Pass to Continue):

| Criterion | Target | How to Test | Timeline |
|-----------|--------|-------------|----------|
| Acoustic signal detectability | SNR > 10dB for cutting vs. idle in 2-20 kHz band | Mount MEMS mic on running CNC, compare spectrograms | Week 1-2 |
| Wear signature visibility | Visible spectral difference between new and worn tool | Record full tool life cycle, plot spectrogram evolution | Week 2-4 |
| Noise resilience | Signal detectable with adjacent machine running | Record with 1-2 other machines active in same shop | Week 2-3 |

### Success Criteria (Phase 1 - ML Validation):

| Criterion | Target | How to Test | Timeline |
|-----------|--------|-------------|----------|
| Classification accuracy | >85% overall, >90% recall on "critical" class | Hold-out test set from real shop data | Week 6 |
| False positive rate | <5% (healthy classified as critical) | Count false alarms over 100+ hours of monitoring | Week 6-8 |
| Detection lead time | >30 seconds before breakage | Record through breakage events, measure when model first detects | Week 6-10 |
| Cross-machine generalization | >70% accuracy on unseen machine (same type) | Train on machines A,B,C; test on machine D | Week 8 |
| Edge model performance | <50ms inference, >80% accuracy after quantization | Benchmark on STM32H7 dev board | Week 6 |

### Success Criteria (Phase 4 - Beta):

| Criterion | Target | How to Test | Timeline |
|-----------|--------|-------------|----------|
| Installation time | <15 minutes by shop owner (no technician) | Time 5 installations by non-technical shop employees | Week 10 |
| Uptime | >99% over 30-day period | Monitor device connectivity and classification output | Week 10-14 |
| Operator trust | >80% of alerts acknowledged as valid | Track alert dismissal vs. confirmation in dashboard | Week 10-14 |
| Prevented incidents | At least 1 documented prevented breakage | Partner shop confirms tool change based on alert | Week 10-14 |
| NPS | >40 from beta users | Survey 10+ beta users | Week 14 |

---

## 7. Total Cost and Time Estimate

### Cost Breakdown:

| Category | Amount | Notes |
|----------|--------|-------|
| Phase 0: Validation rig | $150 | Dev boards, mics, misc |
| Phase 1: ML development | $500 | Compute (AWS), travel to shops |
| Phase 2: Hardware prototype (5 units) | $800 | PCBs, components, 3D printing |
| Phase 3: Cloud backend | $200 | AWS services for 3 months |
| Phase 4: Beta (20 units) | $2,000 | Production prototypes, shipping |
| Freelance embedded engineer | $5,000 | PCB design review + firmware help |
| CNC shop access/partnerships | $2,000 | Travel, lunches, free service |
| Tooling + misc | $1,000 | Tools, test equipment, contingency |
| **Total prototype through beta:** | **$11,650** | |

### If Hiring (Full $215K Budget):

| Role | Duration | Cost |
|------|----------|------|
| ML engineer (contract) | 6 months | $90,000 |
| Embedded engineer (contract) | 4 months | $50,000 |
| Cloud/full-stack dev (contract) | 4 months | $50,000 |
| Hardware prototyping (50 units) | - | $5,000 |
| Shop partnerships + travel | - | $10,000 |
| Cloud infrastructure | 6 months | $5,000 |
| Contingency | - | $5,000 |
| **Total to first revenue:** | | **$215,000** |

### Timeline:

| Milestone | Week | Date (starting today) |
|-----------|------|----------------------|
| Phase 0 complete (validation) | Week 2 | Late June 2026 |
| GO/NO-GO decision | Week 3 | Early July 2026 |
| ML model v1 trained | Week 6 | Mid July 2026 |
| Custom hardware prototype working | Week 8 | Early August 2026 |
| Cloud dashboard MVP | Week 10 | Mid August 2026 |
| Beta deployment begins | Week 12 | Early September 2026 |
| Beta complete, commercial launch | Week 20 | Late October 2026 |
| First paying customer | Week 22 | November 2026 |
| 100 machines deployed | Week 40 | March 2027 |
| 500 machines deployed | Week 70 | January 2028 |

### Solo Founder Timeline (No Hires, Bootstrapped):
- Add 4-8 weeks to each phase (one person doing everything)
- Total: 30-36 weeks to first paying customer
- Cost: ~$12K out of pocket
- Realistic for founder with day job? Only if working 20+ hrs/week on this

---

## 8. Founder-Market Fit Assessment

**Founder Profile:** Hooman Shariati
- Engineering Manager at Adobe (AI platform infrastructure, Firefly generative models)
- Deep expertise: Python, ML/AI systems, cloud infrastructure (AWS), distributed systems
- Experience: Building and scaling ML pipelines, managing engineering teams
- Gap: No hardware/embedded background, no CNC/manufacturing industry connections

### Fit Scorecard:

| Dimension | Score (1-10) | Rationale |
|-----------|-------------|-----------|
| ML/AI expertise | 9/10 | Core of the product is ML on audio data. Hooman builds ML infrastructure daily at Adobe. Can architect training pipeline, model optimization, edge deployment. |
| Cloud/backend | 9/10 | AWS IoT, Lambda, SageMaker - this is his world. Can build cloud stack in sleep. |
| Hardware/embedded | 2/10 | No embedded systems experience. Has never designed a PCB or written firmware. STM32/ESP32 are new territory. Will need to learn or hire. |
| CNC/manufacturing domain | 1/10 | No connections to machine shops. Has likely never operated a CNC machine. Does not know the language, culture, or pain points first-hand. |
| Product management | 7/10 | EM experience at Adobe means customer empathy, prioritization, shipping products. But B2B hardware is different from enterprise software. |
| Sales/distribution | 3/10 | No experience selling to small business owners. Different buyer psychology than enterprise software. |
| Fundraising | 5/10 | Adobe brand + AI expertise is attractive to VCs. But no prior startup experience or track record. |

### Overall Founder-Market Fit: 4.5/10

### Critical Gaps and Mitigations:

**Gap 1: Hardware (Critical)**
- Impact: Cannot build prototype alone
- Mitigation options:
  - a) Learn ESP32/STM32 basics (2-4 weeks of evenings, many tutorials available)
  - b) Hire freelance embedded engineer ($50-100/hr, Upwork/Toptal)
  - c) Find technical co-founder with embedded background
  - d) Use dev boards only (no custom PCB) for first 20 units - uglier but functional
- Recommendation: Option (a) + (b). Learn enough to prototype with dev boards, hire for production PCB.

**Gap 2: Manufacturing Domain Knowledge (Critical)**
- Impact: Cannot validate problem, find customers, or build credibility without understanding the world
- Mitigation options:
  - a) Spend 40+ hours in CNC shops (volunteer, pay for access, find a friend with a shop)
  - b) Join Practical Machinist forum, CNCZone, Reddit r/Machinists - lurk and learn for 2 weeks
  - c) Find a CNC shop owner as advisor/angel investor (gives credibility + access)
  - d) Take a weekend CNC class at local makerspace or community college
- Recommendation: ALL of the above. Domain immersion is non-negotiable. Cannot sell to machinists without speaking their language.

**Gap 3: Sales to Small Business (Important)**
- Impact: Beautiful product that nobody buys
- Mitigation:
  - a) Study how Haas sells to small shops (simple messaging, YouTube presence, dealer network)
  - b) Build in public on YouTube/Instagram CNC community (demonstrate product, build trust)
  - c) Partner with tool distributors (MSC Industrial, McMaster-Carr) for distribution

### Honest Assessment:
The founder's AI/ML and cloud expertise is a massive asset for building the software/ML side of this product - arguably the hardest and most defensible part. The hardware gap is real but solvable (embedded engineering is hireable). The domain knowledge gap is the most concerning - this is a product that needs to be built WITH machinists, not FOR them from the outside. The single most important action is finding 2-3 machinist partners/advisors in the first two weeks.

**Verdict:** Founder can build this, but MUST find either a co-founder or close advisor with deep CNC shop experience within the first month. Going alone without domain expertise will result in building the wrong product.
