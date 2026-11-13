# 03_feasibility_and_prototype.md

## AI-Powered Thermal Inspection Tool — Feasibility & Prototype Plan

### System Architecture

```
+------------------------------------------+
|           HANDHELD DEVICE                 |
|                                          |
|  +----------------+  +---------------+   |
|  | FLIR Lepton 3.5|  | OV5640 Visible|   |
|  | 160x120 thermal|  | 5MP camera    |   |
|  +-------+--------+  +-------+-------+   |
|          |                    |           |
|          v                    v           |
|  +--------------------------------------+|
|  | Application Processor (RK3566/CM4)   ||
|  | - Linux (Buildroot/Yocto)            ||
|  | - TFLite/ONNX Runtime inference      ||
|  | - Camera fusion pipeline             ||
|  | - UI framework (LVGL or Qt Lite)     ||
|  +--------------------------------------+|
|          |            |          |        |
|  +-------+--+ +------+---+ +----+-----+ |
|  | 4" LCD   | | WiFi/BLE | | Battery  | |
|  | Touch    | | Module   | | 3000mAh  | |
|  +----------+ +----------+ +----------+ |
+------------------------------------------+
          |                    |
          | WiFi/BLE           | USB-C
          v                    v
+------------------+  +------------------+
| Companion App    |  | Cloud Backend    |
| (React Native)  |  | (AWS)            |
| - Report mgmt   |  | - Model training |
| - Client sharing |  | - OTA updates   |
| - Historical     |  | - Fleet metrics |
+------------------+  +------------------+
```

### Alternative Architecture: Phone-First (Lower Risk)

Instead of a custom handheld device, an alternative approach attaches a thermal module to a smartphone:

```
+-------------------+       +--------------------+
| Thermal Module    | USB-C | Smartphone (User's)|
| - FLIR Lepton 3.5|------>| - AI inference     |
| - Visible camera  |       | - Report gen       |
| - Battery (small) |       | - Cloud sync       |
+-------------------+       +--------------------+
```

**Trade-offs**:
| Factor | Custom Handheld | Phone Attachment |
|--------|----------------|-----------------|
| Capital required | $525K | $200K |
| Time to market | 18 months | 8 months |
| User experience | Best (purpose-built) | Good (phone dependency) |
| Hardware risk | HIGH | LOW |
| Differentiation | Strong | Moderate (FLIR ONE exists) |
| Unit economics | $260 COGS, $399 retail | $180 COGS, $299 retail |

**Recommendation**: Start with phone attachment (V1) to validate AI/report value proposition with minimal capital. Move to custom handheld (V2) once product-market fit is proven and revenue funds hardware development.

### Bill of Materials (Phone Attachment V1)

| Component | Cost (1K vol) | Confidence |
|-----------|---------------|------------|
| FLIR Lepton 3.5 module (160x120, 8.7Hz) | $180 | VERIFIED — GroupGets/Digikey pricing |
| Visible camera module (OV5640) | $3.50 | VERIFIED — standard commodity part |
| USB-C interface board (FTDI/custom) | $8 | ASSUMED — based on similar USB camera designs |
| Microcontroller (ESP32-S3 for camera control) | $4 | VERIFIED — Espressif pricing |
| Custom PCB (4-layer, assembly) | $12 | ASSUMED — based on PCBWay quotes for similar boards |
| Enclosure (injection molded, small) | $5 | ASSUMED — simple geometry, single mold |
| Battery (optional, 800mAh LiPo) | $3 | VERIFIED — standard cell pricing |
| Misc (cables, buttons, packaging) | $8 | ASSUMED |
| **Total BOM** | **~$224** | |

**Target retail**: $299 (attachment) / $349 (with extra battery + protective case)
**Gross margin**: 25-33%

### Bill of Materials (Custom Handheld V2)

| Component | Cost (1K vol) | Confidence |
|-----------|---------------|------------|
| FLIR Lepton 3.5 module | $180 | VERIFIED |
| RK3566 SoC + LPDDR4 (2GB) + eMMC (16GB) | $18 | VERIFIED — Rockchip reference designs |
| OV5640 visible camera | $3.50 | VERIFIED |
| 4" IPS LCD + capacitive touch | $15 | VERIFIED — Alibaba/Waveshare pricing |
| WiFi 5 + BLE 5.0 module (AP6256) | $4 | VERIFIED — standard combo module |
| 3000mAh LiPo battery + BMS | $8 | VERIFIED |
| Custom PCB (6-layer, assembly) | $22 | ASSUMED — based on complexity |
| Injection molded enclosure (IP54) | $8 | UNVERIFIED — depends on mold complexity, could be $12-15 |
| Buttons, USB-C port, speaker, gaskets | $10 | ASSUMED |
| Packaging + accessories | $5 | ASSUMED |
| **Total BOM** | **~$274** | |

**Target retail**: $499
**Gross margin**: 45%

### Software Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| On-device OS | Buildroot Linux (V2) / Android (V1 phone) | Minimal footprint, fast boot, full hardware control |
| ML Inference | TensorFlow Lite (quantized INT8) / ONNX Runtime | Optimized for ARM, <100ms inference on RK3566 |
| Model Architecture | MobileNetV3 backbone + custom detection head | Best accuracy/latency trade-off for edge |
| Camera Fusion | Custom pipeline: thermal + visible alignment, registration | Critical for accurate overlay and report images |
| Report Engine | Jinja2 templates + WeasyPrint (PDF) | Fast generation, customizable templates |
| Mobile App | React Native (iOS + Android) | Cross-platform, good camera/BLE support |
| Cloud Backend | AWS (Lambda + S3 + DynamoDB + SageMaker) | Model training, OTA updates, telemetry |
| OTA Updates | Mender.io (V2 device) / App Store (V1 phone) | Secure, differential updates |

### AI Model Details

**Classification targets (V1)**:
1. Electrical hot spots (loose connections, overloaded circuits, failing breakers)
2. Moisture intrusion (wall moisture, roof leaks, pipe condensation)
3. Insulation gaps (missing insulation, thermal bridging, air infiltration)

**Training data requirements**:
- Minimum 10,000 labeled thermal images per fault category (30K total)
- Sources: Partner inspectors (paid per labeled image), public thermal image datasets, synthetic augmentation
- Labeling: Bounding box + fault class + severity (1-5) + ground truth confirmation

**Model metrics targets**:
- Precision: >90% (false positives destroy trust with tradespeople)
- Recall: >80% (acceptable to miss some edge cases initially)
- Inference time: <200ms per frame on target hardware
- Model size: <20MB (for OTA and device storage)

### Build Instructions (Phone Attachment V1 — Recommended Start)

| Phase | Duration | Activities | Deliverable |
|-------|----------|-----------|-------------|
| **0. Data Collection** | Weeks 1-8 | Partner with 5-10 inspectors; pay $5/labeled image; collect 5K images minimum | Labeled dataset v0.1 |
| **1. AI Prototype** | Weeks 1-6 | Train MobileNetV3 on laptop; validate accuracy; iterate | Model achieving >85% precision |
| **2. Phone App MVP** | Weeks 4-10 | React Native app with camera integration (phone camera only, no thermal yet); report generation | App generating reports from manual annotations |
| **3. Hardware Prototype** | Weeks 6-12 | FLIR Lepton breakout board + ESP32-S3 + USB-C phone connection; basic thermal streaming to app | 5 prototype units streaming thermal to phone |
| **4. Integration** | Weeks 10-14 | AI inference on-phone from thermal stream; fused thermal+visible overlay; one-tap report | Working end-to-end prototype |
| **5. Beta Testing** | Weeks 14-18 | 10-20 beta users (inspectors) using daily; collect feedback + more training data | Beta validation data |
| **6. Production Prep** | Weeks 16-20 | DFM, FCC certification (unintentional radiator = simpler), production tooling | Manufacturing-ready design |
| **7. Launch** | Week 20-24 | First 200 units; online sales + 2 distributor partnerships | Revenue |

**Total timeline**: 6 months (phone attachment V1)
**Total timeline**: 12-18 months (custom handheld V2, after V1 validates)

### Risk Register

| # | Risk | Probability | Impact | Mitigation |
|---|------|------------|--------|-----------|
| 1 | AI accuracy insufficient (<80%) for trades use | MEDIUM | CRITICAL | Start with narrow scope (electrical hot spots only — most unambiguous thermal signature). Expand after proven. |
| 2 | FLIR Lepton supply constraint or price increase | LOW | HIGH | Dual-source with InfiRay micro thermal module ($150, 256x192). Design hardware abstraction layer. |
| 3 | FLIR adds AI to sub-$1K cameras | MEDIUM | HIGH | Ship faster. Build data moat. Differentiate on report generation + multi-brand compatibility. |
| 4 | Trades workers reject "AI" (trust issue) | MEDIUM | MEDIUM | Position as "smart highlighter" not "robot inspector." Show confidence %. Allow override. Reference code sections. |
| 5 | FCC certification delays (>3 months) | LOW | MEDIUM | Phone attachment V1 may qualify as unintentional radiator (simpler process). Budget 8 weeks + $15K. |
| 6 | Training data insufficient quality/quantity | MEDIUM | HIGH | Pay inspectors well ($5-10/image). Partner with trade schools (students annotate as coursework). Augment synthetically. |
| 7 | Phone thermal streaming latency too high | LOW | MEDIUM | USB-C direct connection (not wireless). Target 5fps minimum (thermal is 8.7Hz max on Lepton 3.5). |
| 8 | Competitor raises $10M+ for same thesis | LOW | CRITICAL | Speed is the only defense. Be first with 10K users + data moat. Consider strategic partnership/acquisition. |

### Validation Plan

**Hypothesis 1**: AI can correctly identify electrical hot spots with >85% precision
- Test: Collect 200 labeled electrical fault images. Run model. Measure precision/recall.
- Go/No-Go: If precision <80% after 3 iterations, pivot to assisted (human-in-loop) model.

**Hypothesis 2**: Report generation saves >20 minutes per inspection
- Test: Time 10 inspectors doing manual report vs AI-assisted report for same job.
- Go/No-Go: If time savings <15 minutes, report value prop is insufficient.

**Hypothesis 3**: Trade professionals will pay $49/month for AI features
- Test: Offer 30-day free trial to 50 beta users. Measure conversion to paid at day 31.
- Go/No-Go: If conversion <30%, price is wrong or value is insufficient.

**Hypothesis 4**: Hardware at $299 is acceptable price point for target customer
- Test: Pre-order page with pricing. Measure conversion rate and volume.
- Go/No-Go: If <100 pre-orders in 60 days with $5K ad spend, demand is insufficient.

### Cost & Time Estimate (Phone Attachment V1)

| Category | Amount |
|----------|--------|
| ML engineer (6 months, contract or cofounder) | $75,000 |
| Mobile app developer (6 months, contract) | $60,000 |
| Hardware engineering (EE, 3 months part-time) | $25,000 |
| Training data collection (5K+ labeled images) | $30,000 |
| Prototype parts + PCB runs (20 units) | $15,000 |
| FCC testing + certification | $12,000 |
| Injection mold tooling (simple enclosure) | $10,000 |
| First production run (500 units × $224) | $112,000 |
| Marketing + trade show presence | $20,000 |
| Contingency (15%) | $54,000 |
| **TOTAL** | **~$413,000** |

Within $300K budget? **NO — but close with adjustments:**
- $300K path: Founder does ML work (saves $75K), use 3D-printed enclosures for first 100 units (saves $10K mold), smaller first run (200 units = $45K savings). Total: ~$280K.
- Requires founder to be the ML engineer (see founder-market fit below).

### Founder-Market Fit Assessment

**Founder profile**: AI/ML infrastructure engineer, deep Python/systems/cloud, no hardware background.

| Dimension | Fit | Notes |
|-----------|-----|-------|
| AI/ML model development | STRONG (9/10) | Core skill. Can build, train, deploy the anomaly detection model without hiring. |
| Python/systems engineering | STRONG (9/10) | Full software stack is natural. Backend, inference pipeline, data processing. |
| Cloud infrastructure | STRONG (9/10) | AWS deployment, OTA updates, model serving are trivial. |
| Hardware design | WEAK (3/10) | No PCB design, thermal sensor, or embedded systems experience. Must hire or contract. |
| Embedded firmware | WEAK (3/10) | Buildroot/RTOS is specialized. Can learn but will be slow. |
| Trades domain expertise | WEAK (2/10) | Does not know NEC codes, inspection workflows, or trade professional culture. Must partner. |
| Product/UX for blue-collar users | MODERATE (5/10) | Software UX skills transfer, but designing for field conditions + non-tech users requires research. |
| Hardware manufacturing | WEAK (2/10) | DFM, supply chain, certification are foreign. Need advisor or cofounder. |
| Sales to trades | WEAK (3/10) | Enterprise SaaS sales don't transfer well to trade distributor relationships. |

**Overall founder-market fit: 5.5/10 — MODERATE**

**Critical gaps to fill**:
1. **Hardware cofounder or contractor** (EE with consumer electronics experience) — non-negotiable
2. **Domain advisor** (experienced home inspector or electrical contractor) — needed for AI labeling, UX testing, channel introductions
3. **Trades distribution partner** (relationship with Grainger, Home Depot Pro, or electrical supply distributor)

**Recommended approach**: Founder focuses on AI model + software platform (their superpower). Contract hardware engineering. Partner with inspectors for domain expertise and training data. This plays to strengths while acknowledging gaps.
