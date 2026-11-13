# Feasibility & Prototype Plan: Legacy IC Recovery-as-a-Service

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        IC RECOVERY CELL                                  │
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐             │
│  │  BOARD FEED  │───>│  VISION      │───>│  EXTRACTION  │             │
│  │  SYSTEM      │    │  STATION     │    │  STATION     │             │
│  │              │    │              │    │              │             │
│  │ Conveyor +   │    │ 4K camera +  │    │ 6-axis arm + │             │
│  │ PCB clamp    │    │ ring light + │    │ hot-air tool +│             │
│  │              │    │ barcode scan │    │ vacuum pickup │             │
│  └──────────────┘    └──────────────┘    └──────────────┘             │
│                                                  │                      │
│                                                  ▼                      │
│                                          ┌──────────────┐             │
│                                          │  TEST        │             │
│                                          │  STATION     │             │
│                                          │              │             │
│                                          │ ATE + X-ray  │             │
│                                          │ (Phase 2)    │             │
│                                          └──────────────┘             │
│                                                  │                      │
│                                                  ▼                      │
│                                          ┌──────────────┐             │
│                                          │  PACKAGING   │             │
│                                          │  & CATALOG   │             │
│                                          │              │             │
│                                          │ ESD tray +   │             │
│                                          │ label + DB   │             │
│                                          └──────────────┘             │
└─────────────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     SOFTWARE LAYER                                       │
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐             │
│  │  IC VISION   │    │  DEMAND DB   │    │  CELL        │             │
│  │  MODEL       │    │  & PRICING   │    │  CONTROLLER  │             │
│  │              │    │              │    │              │             │
│  │ YOLOv8/RT-  │    │ Aftermarket  │    │ Robot path   │             │
│  │ DETR + OCR  │    │ price feeds  │    │ planning +   │             │
│  │ + classif.  │    │ + demand     │    │ thermal ctrl │             │
│  └──────────────┘    └──────────────┘    └──────────────┘             │
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐                                  │
│  │  INVENTORY   │    │  PROVENANCE  │                                  │
│  │  CATALOG     │    │  & COMPLIANCE│                                  │
│  │              │    │              │                                  │
│  │ E-commerce + │    │ Source photo +│                                  │
│  │ API + search │    │ test data +  │                                  │
│  │              │    │ certificates │                                  │
│  └──────────────┘    └──────────────┘                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Bill of Materials (Prototype Cell)

### Hardware BOM

| Component | Specific Model | Unit Cost | Lead Time | Confidence |
|-----------|---------------|-----------|-----------|------------|
| Robot Arm (6-axis, 5kg payload) | Universal Robots UR3e | $25,000 | 4-6 weeks | VERIFIED |
| Hot-Air Rework Station | Metcal HCT-910 or JBC JTSE-2QA | $3,500 | 2 weeks | VERIFIED |
| Vacuum Pickup End-Effector | Custom (Schmalz vacuum + 3D-printed mount) | $2,000 | 3 weeks | ASSUMED |
| Industrial Camera (4K, global shutter) | FLIR Blackfly S BFS-U3-51S5C | $1,800 | 2 weeks | VERIFIED |
| Ring Light + Diffuser | SmartVisionLights DFLW-300 | $500 | 1 week | VERIFIED |
| PCB Clamping Fixture | Custom aluminum + pneumatic clamps | $3,000 | 4 weeks | ASSUMED |
| Thermal Camera (process monitoring) | FLIR A50 | $5,500 | 3 weeks | VERIFIED |
| Conveyor System (1m, variable speed) | Dorner 2200 Series | $4,000 | 4 weeks | VERIFIED |
| ESD-Safe Tray System | Custom IC carrier trays (100x) | $1,500 | 2 weeks | VERIFIED |
| Industrial PC (Vision + Control) | NVIDIA Jetson AGX Orin + x86 host | $3,500 | 2 weeks | VERIFIED |
| Safety Enclosure + E-Stop | Custom welded aluminum + polycarbonate | $5,000 | 4 weeks | ASSUMED |
| Fume Extraction System | BOFA V Oracle | $3,000 | 2 weeks | VERIFIED |
| Force/Torque Sensor (end-effector) | ATI Gamma IP65 | $4,500 | 4 weeks | VERIFIED |
| Soldering Iron (touch-up/through-hole) | JBC Tools CD-2BQF | $800 | 1 week | VERIFIED |
| Power Supply + Distribution | Custom 48V/24V/12V rail | $1,200 | 2 weeks | ASSUMED |
| **HARDWARE SUBTOTAL** | | **~$65,300** | | |

### Software & Compute

| Item | Cost | Confidence |
|------|------|------------|
| NVIDIA GPU for training (A100 80GB rental) | $3/hr, ~$5,000 for initial training | VERIFIED |
| Roboflow or Labelbox (annotation platform) | $500/month | VERIFIED |
| IC identification dataset (initial 10K images) | $15,000 (contract annotation) | ASSUMED |
| OCR engine (part number reading) | Open source (PaddleOCR/EasyOCR) | VERIFIED |
| Robot control software (UR ROS2 driver) | Open source | VERIFIED |
| Cloud hosting (catalog, API) | $500/month (AWS) | VERIFIED |
| Aftermarket price data feeds (Octopart, ERAI) | $2,000/month | ASSUMED |
| **SOFTWARE SUBTOTAL (Year 1)** | **~$55,000** | |

### Test Equipment (Phase 2)

| Item | Cost | Confidence |
|------|------|------------|
| ATE (Automated Test Equipment) - used | $50,000-150,000 | ASSUMED |
| X-Ray Inspection (used Nordson Dage) | $80,000-120,000 | ASSUMED |
| Curve Tracer (Keithley 2600B) | $15,000 | VERIFIED |
| LCR Meter (Keysight E4980A) | $12,000 | VERIFIED |
| **TEST EQUIPMENT SUBTOTAL** | **$157,000-$297,000** | |

### Total Prototype Budget

| Phase | Cost | Timeline |
|-------|------|----------|
| Phase 1: Extraction cell (no test station) | $120,000 | 4-6 months |
| Phase 2: Add test & authentication | $250,000-$400,000 | +3-4 months |
| Operating costs (Year 1) | $150,000 | Ongoing |
| **TOTAL TO FIRST REVENUE** | **$520,000-$670,000** | 8-10 months |

---

## Software Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Computer Vision (detection) | YOLOv8 or RT-DETR | Real-time IC detection on PCB; well-supported, fast inference |
| Computer Vision (OCR) | PaddleOCR + custom fine-tuning | Read chip markings (part number, date code, lot code) |
| IC Classification | Custom CNN (EfficientNet-B4 backbone) | Map visual appearance to part number when markings are damaged |
| Robot Control | ROS2 + Universal Robots ROS2 Driver | Industry standard, UR has excellent ROS2 support |
| Path Planning | MoveIt2 | Collision-aware motion planning |
| Thermal Control | Custom PID controller (Python + Modbus) | Control hot-air temperature/flow per chip package type |
| Database | PostgreSQL + pgvector | IC catalog, pricing, provenance records, image embeddings |
| API / Backend | FastAPI (Python) | Catalog search, order management, provenance API |
| Frontend | React + Next.js | E-commerce catalog for buyers |
| ML Training Pipeline | PyTorch + W&B | Model training and experiment tracking |
| Edge Inference | TensorRT on Jetson Orin | Real-time inference at cell |
| Monitoring | Grafana + Prometheus | Cell uptime, throughput, yield metrics |

---

## Build Instructions (Phase 1 Prototype)

### Week 1-4: Mechanical Setup
1. Procure UR3e arm, mount on 80/20 aluminum frame workbench
2. Design and manufacture PCB clamping fixture (CNC aluminum)
3. Mount camera system on arm (eye-in-hand) AND fixed overhead (eye-to-hand)
4. Integrate hot-air rework station with custom end-effector adapter
5. Add vacuum pickup (Schmalz suction cup + solenoid valve)
6. Install fume extraction and safety enclosure

### Week 4-8: Software Integration
1. Calibrate camera intrinsics/extrinsics (hand-eye calibration)
2. Collect initial dataset: photograph 500+ PCBs with labeled IC locations
3. Train YOLOv8 detection model (IC bounding boxes on PCBs)
4. Train OCR pipeline for chip marking reading
5. Implement ROS2 control stack: camera trigger -> detection -> path plan -> extract
6. Build thermal profile database (start with 20 common package types: DIP, SOIC, QFP, PLCC)
7. Implement extraction sequence: approach -> heat -> dwell -> vacuum -> retract -> place

### Week 8-12: Integration & Tuning
1. End-to-end extraction runs on scrap PCBs
2. Optimize thermal profiles (minimize damage, maximize throughput)
3. Build aftermarket demand database (scrape Octopart, ERAI, broker listings)
4. Implement prioritization logic (skip $0.50 chips, extract $50+ chips)
5. Measure KPIs: throughput (chips/hour), yield (% passing visual inspection post-extract)
6. Iterate on gripper/vacuum design for different package sizes

### Week 12-16: Validation
1. Process 100 real-world mixed PCBs (sourced from local recycler)
2. Measure: extraction rate, damage rate, identification accuracy
3. Send recovered ICs to third-party test lab for electrical verification
4. Document results for investor pitch and customer demos
5. Begin LOI conversations with recyclers and distributors

---

## Risk Register

| # | Risk | Probability | Impact | Mitigation |
|---|------|-------------|--------|------------|
| 1 | Thermal damage rate too high (>10%) | HIGH | HIGH | Build extensive thermal profile library; use IR pre-heating; implement real-time thermal camera feedback loop |
| 2 | IC identification accuracy insufficient | MEDIUM | HIGH | Combine OCR + visual classification + board context; accept graceful degradation (manual review for uncertain IDs) |
| 3 | Throughput below 200 chips/hour | HIGH | MEDIUM | Optimize path planning; dual-arm setup; pre-scan and batch extraction; accept 100-150/hr initially |
| 4 | E-waste recycler refuses to host pilot | MEDIUM | HIGH | Offer zero-cost pilot with generous rev share; target 3+ recyclers simultaneously; have fallback of buying scrap boards |
| 5 | Recovered ICs have no aftermarket demand | LOW | HIGH | Pre-validate demand using ERAI/Octopart data BEFORE extraction; only extract chips with confirmed demand signals |
| 6 | BGA/fine-pitch packages too difficult for v1 | HIGH | LOW | Explicitly scope out BGAs from v1; focus on through-hole, SOIC, QFP, PLCC which are easier and often higher aftermarket value (older = more obsolete) |
| 7 | Counterfeit liability if mis-identified IC sold | LOW | CRITICAL | Implement multi-factor authentication (marking read + X-ray die analysis + electrical test); carry liability insurance; AS6171 compliance |
| 8 | UR3e payload insufficient for heavy tooling | MEDIUM | MEDIUM | Hot-air station mounted stationary; arm only carries vacuum pickup (lightweight); or upgrade to UR5e ($35K) |
| 9 | Competitor (Tuurny/Molg) raises large round and accelerates | MEDIUM | HIGH | Move fast; focus on defense/aerospace premium segment they are not targeting; build thermal profile moat quickly |
| 10 | Regulatory issues with e-waste handling | LOW | MEDIUM | Partner with licensed recyclers (they hold permits); we only handle extracted ICs, not waste |

---

## Validation Plan

### Technical Validation (Months 1-4)

| Milestone | Success Criteria | Validation Method |
|-----------|-----------------|-------------------|
| IC Detection | 95%+ mAP on test PCBs | Hold-out test set of 200 boards |
| OCR Accuracy | 90%+ correct part number reads | Manual verification of 500 reads |
| Extraction Rate | 100+ ICs/hour sustained | Timed runs on 50+ boards |
| Damage Rate | <10% post-extraction visual defects | Visual inspection of 500+ extracted ICs |
| Electrical Pass Rate | >85% of undamaged ICs pass basic test | Curve tracer + functional test on sample |

### Market Validation (Months 2-6)

| Milestone | Success Criteria | Validation Method |
|-----------|-----------------|-------------------|
| Demand Confirmation | 500+ part numbers with >$25 aftermarket value per board | Cross-reference Octopart/ERAI with typical telecom/server board BOMs |
| Recycler Interest | 2+ LOIs from recyclers willing to host | Direct outreach to 10+ recyclers |
| Buyer Interest | 3+ LOIs from distributors/OEMs willing to purchase recovered ICs | Direct outreach to aftermarket distributors |
| Unit Economics | Average recovered IC value >$25 with extraction cost <$5 | Run economics model on actual recovery data |

---

## Cost & Time Estimate

| Phase | Duration | Cash Required | Headcount |
|-------|----------|--------------|-----------|
| Phase 1: Lab Prototype | 4 months | $150,000 | 2 (founder + robotics engineer) |
| Phase 2: Pilot at Recycler | 4 months | $200,000 | 3 (+ ML engineer) |
| Phase 3: Add Test Station | 3 months | $300,000 | 4 (+ test engineer) |
| Phase 4: Second Cell + Sales | 6 months | $500,000 | 6 (+ sales + ops) |
| **TOTAL TO 2 CELLS DEPLOYED** | **17 months** | **$1.15M** | |

**Funding strategy**: 
- $500K pre-seed for Phase 1-2 (lab prototype + pilot validation)
- $1.5M seed for Phase 3-4 (test station + scale to multiple cells)
- Revenue-positive at 2-3 cells (Month 14-17)

---

## Founder-Market Fit Assessment

**Founder profile**: AI/ML infrastructure engineer, deep Python/systems/cloud expertise, no hardware/robotics background.

| Dimension | Score (1-10) | Assessment |
|-----------|-------------|------------|
| Technical (software/ML) | 9/10 | Computer vision, ML training pipelines, backend systems -- all in wheelhouse |
| Technical (hardware/robotics) | 2/10 | No robotics, mechatronics, or manufacturing experience. Critical gap. |
| Technical (electronics) | 3/10 | Likely understands ICs conceptually but no hands-on desoldering/test experience |
| Domain (e-waste industry) | 2/10 | No existing relationships with recyclers |
| Domain (semiconductor aftermarket) | 2/10 | No existing relationships with brokers/distributors |
| Business model execution | 6/10 | Equipment-as-a-service is cloud-native thinking applied to physical world; reasonable |
| Fundraising ability | 6/10 | Adobe/AI pedigree helps, but hardware startups are harder to fund |

### Critical Gaps to Fill:

1. **MUST HAVE co-founder**: Robotics/mechatronics engineer with experience in:
   - Robot arm integration (UR, Fanuc, ABB)
   - End-effector design
   - Industrial automation
   - Ideally: electronics manufacturing or rework experience

2. **MUST HAVE early hire or advisor**: Someone from the legacy semiconductor aftermarket who:
   - Knows the buyer ecosystem (distributors, defense procurement)
   - Understands AS6171/AS6081 compliance requirements
   - Has relationships with e-waste recyclers

3. **SHOULD HAVE**: Electronics test engineer familiar with IC characterization

### Honest Assessment:

**Founder-market fit is POOR for solo execution but VIABLE with right co-founder.**

The software/ML portion (50% of the challenge) is well-matched to founder's skills. The robotics/hardware portion (40%) and industry relationships (10%) are critical gaps. This is a team-dependent opportunity -- the right robotics co-founder transforms this from "founder out of their depth" to "complementary founding team."

**Comparable successful precedent**: Many robotics startups have been founded by software engineers who recruited robotics co-founders (e.g., Locus Robotics, Covariant). The ML/software layer is increasingly where differentiation lives in robotics ventures.

**Red flag**: If founder cannot recruit a robotics co-founder within 3 months, this is likely not the right opportunity. Hardware iteration cycles are brutal without hands-on expertise.
