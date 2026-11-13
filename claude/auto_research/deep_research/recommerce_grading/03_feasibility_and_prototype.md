# Feasibility & Prototype Plan: AI Recommerce Grading Station

## Architecture

```
+-----------------------------------+     +------------------------+     +-------------------+
|  Grading Station (Physical)       |     |   Cloud Backend        |     |   Web Dashboard   |
|                                   |     |                        |     |                   |
| +-------------+  +-----------+    |     | +------------------+   |     | Analytics Portal  |
| | 3x Cameras  |  | Turntable |    |     | | API Server       |   |     | - Grade distrib.  |
| | (USB3 12MP) |  | (stepper) |    |     | | (FastAPI)        |   |<----| - Model accuracy  |
| +------+------+  +-----+-----+    |     | +------------------+   |     | - Throughput KPIs |
|        |              |            |     |   |                    |     | - Override trends |
|        v              v            |     |   v                    |     +-------------------+
| +-----------------------------+   |     | +------------------+   |
| | Edge PC (Nvidia Jetson      |   |---->| | Model Registry   |   |
| | Orin NX / Mini PC + RTX)    |   | TLS | | + Training       |   |
| | - Inference engine          |   |     | | Pipeline         |   |
| | - Camera control            |   |     | +------------------+   |
| | - Turntable control         |   |     |   |                    |
| | - Local UI (touchscreen)    |   |     |   v                    |
| +-----------------------------+   |     | +------------------+   |
|        |                          |     | | PostgreSQL       |   |
|        v                          |     | | + S3 (images)    |   |
| +-----------------------------+   |     | +------------------+   |
| | Barcode Scanner + RFID      |   |     +------------------------+
| +-----------------------------+   |
| +-----------------------------+   |
| | LED Lights + Enclosure      |   |
| +-----------------------------+   |
+-----------------------------------+
```

### Component Breakdown

**Grading Station Hardware**
- Enclosed aluminum-frame booth with white diffusion panels
- 3x industrial USB3 cameras (FLIR Blackfly S or Basler ace 2) at fixed positions
- LED strip lighting (CRI 95+) on all 4 sides + top
- Motorized turntable (NEMA 17 stepper + timing belt, 360-degree in configurable increments)
- 15.6" touchscreen display (operator interface)
- Barcode scanner (Zebra DS2208 or similar)
- Edge compute unit (see options below)

**Edge Compute (Option A - Preferred): Nvidia Jetson Orin NX 16GB**
- 100 TOPS AI inference performance
- Runs ONNX/TensorRT models at 30+ FPS
- Low power (15-25W)
- $500-700 at volume
- Fanless operation possible with heatsink

**Edge Compute (Option B - Higher Performance): Mini PC + Nvidia RTX 4060**
- Standard x86 mini PC (Intel NUC or similar) + discrete GPU
- RTX 4060: 15.1 TFLOPS, 8GB VRAM
- $800-1200 total
- More power, more heat, needs active cooling
- Easier development (standard CUDA/PyTorch workflow)

**Cloud Backend**
- FastAPI application server (Python 3.11+)
- PostgreSQL for grading records, customer configs, model metadata
- S3-compatible storage for grading images (raw + annotated)
- Model training pipeline (GPU instances on-demand for retraining)
- Multi-tenant SaaS with per-customer model versioning

**ML Pipeline**
- Object detection: YOLOv8/v9 for defect localization (stains, tears, scuffs)
- Classification: EfficientNet-V2 or ConvNeXt for overall grade assignment
- Segmentation: SAM-based for precise defect boundary delineation
- Ensemble: Multiple model heads combined for final grade prediction
- Training: Transfer learning from ImageNet + custom defect datasets
- Serving: TensorRT-optimized models on edge, <500ms total inference per item

---

## Bill of Materials (Per Station)

### Hardware BOM

| Component | Specific Part | Qty | Unit Cost | Total | Status |
|-----------|--------------|-----|-----------|-------|--------|
| Camera | FLIR Blackfly S BFS-U3-122S6C-C (12.3MP, USB3) | 3 | $420 | $1,260 | VERIFIED (FLIR website pricing) |
| Camera Lens | Computar M1214-MP2 12mm f/1.4 C-mount | 3 | $85 | $255 | VERIFIED (B&H Photo) |
| Edge Computer | Nvidia Jetson Orin NX 16GB Dev Kit | 1 | $599 | $599 | VERIFIED (Nvidia store) |
| Turntable Motor | NEMA 17 Stepper + DM542T Driver | 1 | $45 | $45 | VERIFIED (Amazon/StepperOnline) |
| Turntable Platform | Custom 18" diameter aluminum plate + bearing | 1 | $120 | $120 | ASSUMED (custom fab) |
| LED Lighting | Waveform 5600K LED strips (CRI 98), 4x 2ft | 4 | $35 | $140 | VERIFIED (Waveform Lighting) |
| LED Power Supply | Mean Well LPV-60-24 (24V 60W) | 1 | $22 | $22 | VERIFIED |
| Touchscreen | 15.6" HDMI capacitive touch (Waveshare/EleDuino) | 1 | $180 | $180 | VERIFIED (Amazon) |
| Barcode Scanner | Zebra DS2208-SR handheld 2D | 1 | $130 | $130 | VERIFIED (Zebra direct) |
| Enclosure Frame | 80/20 aluminum extrusion kit (1" profile, custom cut) | 1 | $280 | $280 | ASSUMED (80/20 configurator estimate) |
| Enclosure Panels | White acrylic diffusion panels (4 sides + top) | 5 | $40 | $200 | ASSUMED |
| USB Hub | Industrial 7-port USB 3.0 hub (powered) | 1 | $60 | $60 | VERIFIED |
| Cables & Connectors | USB3 cables, power cables, stepper cable | 1 | $80 | $80 | ASSUMED |
| Stepper Controller | Arduino/ESP32 + motor shield (turntable control) | 1 | $35 | $35 | VERIFIED |
| Misc Hardware | Brackets, screws, cable management, feet | 1 | $75 | $75 | ASSUMED |

**Total BOM: $3,481**

| Category | Amount | % of Total |
|----------|--------|-----------|
| VERIFIED components | $2,711 | 78% |
| ASSUMED components | $770 | 22% |
| UNVERIFIED | $0 | 0% |

**Target sell price: $10,000** (65% gross margin on hardware)
**Volume pricing note**: At 50+ units, camera costs drop 15-20% (distributor pricing), total BOM likely ~$3,000.

### Alternative BOM (Budget Version for Pilot)

| Component | Substitution | Savings |
|-----------|-------------|---------|
| Camera | Arducam 12MP USB (IMX477) instead of FLIR | -$900 (3x $300 less) |
| Edge PC | Jetson Orin Nano 8GB instead of NX 16GB | -$200 |
| Turntable | Manual rotation (operator turns item) | -$165 |
| Enclosure | Plywood + foam board (prototype only) | -$280 |

**Pilot BOM: ~$1,900** (for internal testing and first customer demo)

---

## Software Stack

### Edge Software
- **OS**: JetPack 6.x (Ubuntu 22.04 base) on Jetson, or Ubuntu 22.04 on x86
- **Inference**: TensorRT (Nvidia) or ONNX Runtime with CUDA EP
- **Camera SDK**: Spinnaker SDK (FLIR) or libusb/v4l2 (Arducam)
- **Motor Control**: Serial/USB to Arduino/ESP32 running AccelStepper
- **UI**: PyQt6 or Electron app on local touchscreen
- **Networking**: MQTT for cloud telemetry, HTTPS for model pulls and image upload

### Cloud Software
- **API**: FastAPI (Python 3.11) + Pydantic v2
- **Database**: PostgreSQL 15 (grading records, customer config)
- **Image Storage**: AWS S3 (or MinIO for on-prem option)
- **ML Training**: PyTorch + Lightning, Weights & Biases for experiment tracking
- **Model Registry**: MLflow or custom (versioned models per customer per category)
- **Frontend**: React + TypeScript + Recharts (analytics dashboard)
- **Deployment**: AWS ECS Fargate (API) + S3 + RDS + SageMaker (training)
- **CI/CD**: GitHub Actions, Docker containers

### ML Model Architecture
```
Input: 12-18 images (3 cameras x 4-6 positions)
    |
    v
[Image Preprocessing] -- resize, normalize, white balance correction
    |
    v
[Defect Detection Head] -- YOLOv8-m (medium) 
    |                        Outputs: bounding boxes + class (stain/tear/scuff/pilling/missing_part)
    v
[Defect Severity Head] -- EfficientNet-V2-S per detected defect region
    |                      Outputs: severity 1-5 per defect
    v
[Grade Aggregation] -- Rule engine + learned weights
    |                   Inputs: all defects + severities + category-specific rules
    v
Output: Grade (A/B/C/D/Reject) + confidence + defect annotations
```

---

## Build Instructions (Prototype to Production)

### Phase 1: ML Validation (Weeks 1-8, $40K)

**Objective**: Prove the AI can grade at 85%+ accuracy on footwear.

1. **Data Collection (Weeks 1-3)**
   - Partner with local thrift store or ThredUp outlet to access 500+ used shoes
   - Photograph each pair using temporary rig (tripod + good lighting + manual rotation)
   - Have 3 human graders independently grade each item (establish ground truth by majority vote)
   - Target: 500 items x 12 images each = 6,000 images, labeled with defects and grades

2. **Model Training (Weeks 3-6)**
   - Fine-tune YOLOv8 on defect detection (stains, scuffs, sole wear, lace damage)
   - Train grade classifier on the full image set
   - Evaluate: per-class accuracy, confusion matrix, inter-rater agreement vs. model agreement

3. **Accuracy Target**
   - Model must achieve 85%+ exact-grade agreement (matches human majority vote)
   - For comparison: human inter-rater agreement is ~65-70% (so exceeding humans is feasible)
   - Adjacent-grade tolerance: 95%+ (off by one grade is acceptable for V1)

4. **Go/No-Go Decision at Week 8**
   - If 85%+ accuracy: proceed to hardware build
   - If 75-84%: identify failure modes, collect more data for those categories, extend 4 weeks
   - If <75%: fundamental rethink (likely need better hardware or constrained categories)

**Cost**: $30K compute (GPU cloud for training) + $10K data collection (thrift purchases, grader time)

### Phase 2: Hardware Prototype (Weeks 6-14, $25K)

**Objective**: Build 2 working stations (1 for testing, 1 for customer demo).

1. **Mechanical Design (Weeks 6-8)**
   - CAD design of enclosure (Fusion 360 or SolidWorks)
   - 80/20 aluminum frame with modular camera mounts
   - Turntable mechanism (bearing + timing belt + stepper)
   - LED lighting layout for uniform illumination

2. **Electronics Integration (Weeks 8-10)**
   - Camera mounting and alignment (fixed positions, repeatable geometry)
   - Jetson Orin NX setup + power delivery
   - Motor controller board (Arduino + stepper driver)
   - Cable routing, EMI shielding for cameras

3. **Software Integration (Weeks 10-14)**
   - Camera capture sequencing (trigger rotation, capture at each position)
   - Model deployment on Jetson (TensorRT optimization)
   - Touchscreen UI (PyQt6: scan item -> capture -> display grade -> confirm/override)
   - Basic cloud connectivity (upload images + grades for analytics)

**Cost**: $15K (2x prototype BOM at ~$4K each + tools/equipment + iteration materials) + $10K (mechanical design contractor if needed)

### Phase 3: Pilot Deployment (Weeks 14-22, $30K)

**Objective**: Deploy at first customer site, validate real-world performance.

1. Install 1-2 stations at pilot customer
2. Run in "shadow mode" first 2 weeks (AI grades alongside human, compare without replacing)
3. Measure: accuracy, throughput, operator satisfaction, edge cases
4. Iterate model based on real-world data (expect 100-500 new labeled examples per week)
5. Transition to "AI-primary" mode (human reviews only low-confidence grades)

**Cost**: $20K (travel, installation, on-site support) + $10K (ongoing cloud/compute)

### Phase 4: Production & Scale (Weeks 22-40, $200K)

1. Design for manufacturing (DFM review of enclosure)
2. Find contract manufacturer for mechanical assembly (likely 2-3 vendors for different parts)
3. Production run of 10-20 stations
4. Sales and deployment

**Cost**: $200K (first production run, tooling, inventory)

---

## Risk Register

| # | Risk | Probability | Impact | Mitigation |
|---|------|-------------|--------|------------|
| 1 | ML accuracy insufficient for customer trust (<85% agreement) | MEDIUM | HIGH | Phase 1 go/no-go gate. Start with constrained category (footwear only). Use human-in-the-loop for low-confidence grades. |
| 2 | Customer grading criteria too subjective to encode | MEDIUM | MEDIUM | Work with customer to formalize criteria before deployment. Offer calibration service. Use their own historical grades as training data. |
| 3 | Camera/lighting inconsistency in warehouse environment | LOW | MEDIUM | Enclosed booth eliminates ambient light. Fixed camera positions ensure repeatability. Temperature extremes unlikely in indoor facilities. |
| 4 | Hardware reliability in 24/7 operation | MEDIUM | MEDIUM | Use industrial-grade components. MTBF testing during Phase 2. Spare parts kit included. Remote monitoring for hardware health. |
| 5 | StyleShoots or Optoro launches competing product | MEDIUM | HIGH | Speed to market is the mitigation. First-mover with working product + customer data creates 12-18 month window. Focus on GRADING intelligence as differentiator. |
| 6 | Customer WMS integration complexity exceeds estimates | HIGH | LOW | Start with CSV export (works with any system). Build top-5 WMS integrations (Manhattan, SAP, Blue Yonder, Oracle, HighJump) over time. |
| 7 | Edge compute insufficient for required model complexity | LOW | MEDIUM | Jetson Orin NX handles YOLOv8-m + EfficientNet in <500ms. If needed, upgrade to Orin AGX ($1,999) or x86+RTX. BOM increase manageable. |
| 8 | Sales cycle longer than expected (>6 months) | HIGH | HIGH | Offer free 2-week pilot with real items. ROI is undeniable if accuracy meets threshold. Target innovation teams at brands (faster decision-making than operations). |
| 9 | Liability if AI misgrade causes customer complaint downstream | LOW | HIGH | Clear SLA that AI assists but human operator confirms. Confidence threshold below which human review is mandatory. Insurance. |
| 10 | Founder lacks retail/logistics domain relationships | HIGH | MEDIUM | Hire BD with returns industry background within first 6 months. Attend NRF, RLA conferences. Advisory board with operations leaders. |

---

## Validation Plan

### Technical Validation (Phase 1)
- [ ] 500+ items photographed and human-graded (establish ground truth)
- [ ] Model achieves 85%+ exact-grade accuracy on holdout set
- [ ] Inference time <3 seconds per item on Jetson Orin NX
- [ ] Camera + lighting produces consistent image quality (SSIM >0.95 between repeated captures of same item)

### Market Validation (Phase 1-2)
- [ ] 10+ discovery interviews with returns operations managers
- [ ] 3+ expressed interest in pilot (verbal or email)
- [ ] 1 signed LOI or pilot agreement before committing to production hardware
- [ ] Pricing validated ($10K + $750/month does not cause sticker shock)

### Operational Validation (Phase 3)
- [ ] Pilot station operates 8+ hours/day without intervention for 2 weeks
- [ ] Throughput: 150+ items/hour achieved in real operation
- [ ] Operator NPS >7/10 (they prefer the station to manual grading)
- [ ] Grade agreement with customer's QA spot-checks: 90%+

---

## Cost & Time Summary

| Phase | Duration | Cost | Cumulative |
|-------|----------|------|-----------|
| Phase 1: ML Validation | 8 weeks | $40K | $40K |
| Phase 2: Hardware Prototype | 8 weeks (2 overlap) | $25K | $65K |
| Phase 3: Pilot Deployment | 8 weeks | $30K | $95K |
| Phase 4: Production & Scale | 18 weeks | $200K | $295K |
| Buffer / Contingency | -- | $55K | $350K |

**Total: $350K over 10 months to first revenue**

**Team required:**
- Founder/CTO: ML engineering, system architecture, edge deployment (full-time)
- Mechanical engineer: Booth design, DFM (contract, 3-4 months)
- Frontend/cloud engineer: Dashboard, API, cloud infrastructure (full-time from month 3)
- Data labeler(s): Part-time during Phase 1, ongoing for model improvement

---

## Founder-Market Fit Assessment

### Strengths (ML/Infrastructure Engineer Background)
- **Computer vision / ML**: Core technical competency aligns perfectly. Training defect detection models, optimizing inference on edge hardware, building ML pipelines -- this IS the product.
- **Systems / Infrastructure**: Edge-cloud architecture, deployment automation, monitoring -- critical for a hardware+software product.
- **Engineering management**: Can hire and lead the small team needed. Understands build-vs-buy tradeoffs.

### Gaps (No Retail/Logistics Background)
- **No existing relationships** in returns/recommerce industry. Cold outreach required. Sales cycle will be longer without warm intros.
- **No domain intuition** for what "Grade B" means to a Nike operations manager vs. a ThredUp quality analyst. Must learn through immersion.
- **No hardware manufacturing experience**. Building 2 prototypes is different from manufacturing 100 stations reliably. Will need contract manufacturing partner.
- **No enterprise sales experience** in retail/logistics vertical. Procurement processes, RFPs, pilot-to-contract conversion are learned skills.

### Mitigation Strategy
1. **Advisory board**: Recruit 1-2 advisors from returns/recommerce operations (LinkedIn: "VP Operations" at Optoro, Trove, or brand return centers)
2. **Domain immersion**: Spend 2 weeks working in a returns processing center (volunteer or paid observation) before building anything
3. **Hardware partner**: Contract the mechanical/electrical engineering to a firm that does industrial equipment design
4. **Sales hire**: Plan to bring on a BD/sales person with retail logistics relationships by month 6-8

### Honest Assessment
**Founder-market fit: 5.5/10**

The technical core (CV, ML, edge deployment) is a near-perfect match -- this is what makes the product work and what creates the moat. But the go-to-market side (relationships, domain credibility, enterprise sales) is genuinely weak. The ideal founder for this business would be an ML engineer who previously worked at ThredUp, The RealReal, or a brand's returns division. Lacking that background means 6-12 months of slower traction while building credibility. Not fatal, but it IS a handicap that costs time and capital.
