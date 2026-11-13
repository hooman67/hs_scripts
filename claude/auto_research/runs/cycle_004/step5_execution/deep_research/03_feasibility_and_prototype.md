# Feasibility & Prototype Plan: Smart Warehouse QC Module (mmWave Through-Package)

## System Architecture

```
                    ┌──────────────────────────────────────────────────────┐
                    │                  SCANNER UNIT                         │
                    │                                                       │
                    │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐│
                    │  │Radar #1 │  │Radar #2 │  │Radar #3 │  │Radar #4 ││
                    │  │(Top)    │  │(Left)   │  │(Right)  │  │(Angled) ││
                    │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘│
                    │       │            │            │            │      │
                    │       └──────────┐ │ ┌──────────┘            │      │
                    │                  ▼ ▼ ▼                       │      │
                    │         ┌─────────────────┐                  │      │
                    │         │  Data Capture   │◄─────────────────┘      │
                    │         │  (DCA1000EVM    │                          │
                    │         │   or custom ADC)│                          │
                    │         └────────┬────────┘                          │
                    │                  │ Raw ADC data (Ethernet)           │
                    │                  ▼                                    │
                    │         ┌─────────────────┐                          │
                    │         │  Edge Compute   │                          │
                    │         │  (Jetson Orin)  │                          │
                    │         │                 │                          │
                    │         │  - Signal proc  │                          │
                    │         │  - 3D reconstr  │                          │
                    │         │  - ML inference │                          │
                    │         └────────┬────────┘                          │
                    │                  │                                    │
                    └──────────────────┼────────────────────────────────────┘
                                       │
                    ┌──────────────────┼────────────────────────────────────┐
                    │                  ▼                                    │
                    │  ┌─────────────────────────────┐                     │
                    │  │      Decision Engine        │                     │
                    │  │  PASS / REVIEW / REJECT     │                     │
                    │  └──────────┬──────────────────┘                     │
                    │             │                                         │
                    │    ┌────────┼────────┐                               │
                    │    ▼        ▼        ▼                               │
                    │ ┌──────┐ ┌──────┐ ┌──────────┐                      │
                    │ │GPIO  │ │REST  │ │Dashboard │                      │
                    │ │(24V) │ │API   │ │(Web UI)  │                      │
                    │ │Divert│ │→ WMS │ │          │                      │
                    │ └──────┘ └──────┘ └──────────┘                      │
                    │           SOFTWARE LAYER                              │
                    └──────────────────────────────────────────────────────┘
```

### Data Flow:
1. Trigger sensor (photoelectric) detects package entering scan zone
2. Barcode scanner (existing) reads package ID, system looks up expected contents from WMS
3. All 4 radar modules perform synchronized FMCW chirp sequence (~50ms)
4. Raw IF (intermediate frequency) data streamed to edge compute via Ethernet
5. Signal processing pipeline: Range FFT -> Doppler FFT -> Angle estimation -> 3D point cloud
6. ML model compares 3D radar signature to reference signature for expected SKU
7. Classification: PASS (>95% match) / REVIEW (70-95%) / REJECT (<70%)
8. Output: GPIO signal to diverter gate + API call to WMS + dashboard update

---

## Bill of Materials (Prototype Unit)

### Hardware BOM

| Component | Part Number | Qty | Unit Cost | Total | Confidence |
|-----------|-------------|-----|-----------|-------|------------|
| mmWave Radar SoC Eval Module | TI IWR6843ISK-ODS | 4 | $149 | $596 | VERIFIED (ti.com) |
| Data Capture Card | TI DCA1000EVM | 2 | $249 | $498 | VERIFIED (ti.com) |
| Edge GPU Computer | Nvidia Jetson Orin NX 16GB Dev Kit | 1 | $599 | $599 | VERIFIED (nvidia.com) |
| Industrial SSD | Samsung 970 EVO Plus 500GB NVMe | 1 | $60 | $60 | VERIFIED |
| Ethernet Switch | Netgear GS108 (8-port gigabit) | 1 | $40 | $40 | VERIFIED |
| Trigger Sensor | Omron E3Z-T61 photoelectric | 1 | $85 | $85 | ASSUMED (may need different model) |
| Industrial Power Supply | Mean Well RSP-320-12 (12V/26.7A) | 1 | $55 | $55 | VERIFIED |
| Industrial Power Supply | Mean Well RSP-150-5 (5V/30A) | 1 | $35 | $35 | VERIFIED |
| Mounting Frame (80/20 aluminum extrusion) | Various | 1 | $200 | $200 | ASSUMED |
| 3D Printed Radar Enclosures | Custom (PETG) | 4 | $15 | $60 | ASSUMED |
| GPIO Relay Board (for diverter) | Waveshare Industrial 8-ch Relay | 1 | $30 | $30 | VERIFIED |
| Cables (Ethernet, power, GPIO) | Various | 1 | $100 | $100 | ASSUMED |
| Industrial Enclosure (NEMA 4) | Hammond 1418 series | 1 | $150 | $150 | ASSUMED |
| **PROTOTYPE BOM TOTAL** | | | | **$2,508** | |

### Development Equipment (one-time)

| Item | Cost | Confidence |
|------|------|------------|
| Additional TI radar dev kits (for experiments) x4 | $600 | VERIFIED |
| TI mmWave Studio license | Free | VERIFIED |
| Conveyor belt section (used, 6ft, variable speed) | $2,000-$5,000 | ASSUMED |
| Test packages (various sizes, contents, damage types) | $3,000 | ASSUMED |
| Oscilloscope (for signal debugging) | $1,500 | ASSUMED |
| Network analyzer (antenna tuning) | $2,000 | ASSUMED |
| Workstation for ML training (RTX 4090) | $3,000 | VERIFIED |
| AWS/GCP compute credits (model training) | $15,000 | ASSUMED |
| Misc tools, connectors, supplies | $2,000 | ASSUMED |
| **DEVELOPMENT TOTAL** | **$30,000-$33,000** | |

### Production BOM Estimate (at 100-unit scale)

| Component | Production Cost | Confidence |
|-----------|----------------|------------|
| Custom mmWave radar PCB (replaces eval modules) x4 | $120 total | UNVERIFIED (needs RF PCB design) |
| Custom data capture FPGA board | $150 | UNVERIFIED |
| Jetson Orin NX (production module, no dev kit) | $399 | VERIFIED (Nvidia pricing) |
| Custom enclosure (injection mold amortized) | $50 | ASSUMED |
| All other components | $200 | ASSUMED |
| Assembly labor | $100 | ASSUMED |
| **PRODUCTION BOM (per unit)** | **~$1,020** | |
| **Target sell price** | **$18,000-$28,000** | |
| **Gross margin** | **93-96%** | ASSUMED (software margins dominate) |

---

## Software Stack

### Signal Processing Layer
- **Language**: C++ (real-time performance critical)
- **Libraries**: TI mmWave SDK (radar configuration), FFTW (FFT processing), Eigen (linear algebra)
- **Function**: Raw radar data -> range-Doppler maps -> 3D point clouds
- **Latency budget**: <100ms for 4 radars simultaneously

### ML/AI Layer
- **Language**: Python (training), C++ with TensorRT (inference)
- **Framework**: PyTorch (training), TensorRT (edge deployment on Jetson)
- **Models**:
  1. **3D Reconstruction Network**: Converts multi-angle radar point clouds into volumetric representation. Architecture: Modified PointNet++ or 3D sparse convolution network.
  2. **Content Classifier**: Compares reconstructed volume to reference signatures. Architecture: Siamese network with contrastive learning (learns "same vs. different" rather than classifying individual items).
  3. **Anomaly Detector**: Identifies damage patterns (unusual density distributions, voids, fragments). Architecture: Autoencoder-based anomaly detection.
- **Training data strategy**: Synthetic data generation (simulated radar returns) + real captured data from pilot installations
- **Inference latency target**: <200ms total pipeline on Jetson Orin NX

### Application Layer
- **Language**: Python (FastAPI)
- **Components**:
  - REST API for WMS integration (receive order manifests, report results)
  - WebSocket for real-time dashboard updates
  - PostgreSQL for scan history, model performance metrics
  - Redis for real-time state (current packages in scan zone)
- **Dashboard**: React frontend (or Streamlit for prototype)

### DevOps / Deployment
- **Edge**: Docker containers on Jetson (JetPack OS)
- **Cloud**: AWS (model training, dashboard hosting, fleet management)
- **OTA updates**: Balena or custom update mechanism for edge devices
- **Monitoring**: Prometheus + Grafana for system health; custom ML model drift detection

---

## Build Instructions (Phase-Gated)

### Phase 0: Feasibility Validation (Weeks 1-6) -- CRITICAL GO/NO-GO
**Objective**: Prove mmWave can distinguish different items inside sealed cardboard boxes

**Steps**:
1. Set up single TI IWR6843ISK radar module on optical bench (static, no conveyor)
2. Collect radar signatures of 10 different common products (book, phone case, coffee mug, shirt, headphones, water bottle, toy, candle, shoe, electronics box) each inside standard corrugated cardboard box
3. Collect 50 scans per item (varied orientation)
4. Train simple classifier (SVM or shallow neural network) on raw radar features
5. Test: Can classifier distinguish between items with >80% accuracy?

**Go/No-Go Gate**:
- GO: >80% classification accuracy on 10-item set with single radar
- CONDITIONAL: 60-80% accuracy -- may improve with multi-angle radar array
- KILL: <60% accuracy -- fundamental physics limitation confirmed

**Cost**: ~$500 (1 radar dev kit + boxes + items)
**Time**: 6 weeks part-time (founder can do this alone)

### Phase 1: Multi-Angle Prototype (Weeks 7-18)
**Objective**: Build 4-radar array, prove multi-angle improves accuracy, test on conveyor

**Steps**:
1. Build mounting frame for 4 radar modules (top, left, right, angled)
2. Synchronize radar captures across all 4 modules
3. Implement 3D point cloud fusion from multiple viewpoints
4. Expand SKU set to 50 items
5. Train 3D reconstruction + classification pipeline
6. Mount on conveyor belt section, test at various speeds
7. Characterize: accuracy vs. speed, accuracy vs. package size, accuracy vs. item similarity

**Gate**: >85% accuracy on 50-item set at 500 packages/hour equivalent speed

### Phase 2: Production Prototype (Weeks 19-30)
**Objective**: Build deployment-ready unit, integrate with WMS, prepare for pilot

**Steps**:
1. Design custom PCB (replace eval modules with production-ready boards)
2. Design industrial enclosure (IP54 rated for warehouse dust)
3. Implement full software stack (signal processing + ML + API + dashboard)
4. Stress testing: 8-hour continuous operation, thermal management validation
5. WMS integration development (Manhattan Associates API, Blue Yonder API)
6. Build SKU enrollment workflow (how customers add new items to system)

**Gate**: 8-hour continuous operation at 500+ packages/hour with <5% false positive rate

### Phase 3: Pilot Deployment (Weeks 31-52)
**Objective**: Deploy at 2 customer sites, prove ROI, collect production training data

**Steps**:
1. Install at Pilot Customer #1 (targeting mid-size 3PL)
2. 30-day burn-in period (system runs in monitoring mode, does not divert)
3. Calibrate thresholds based on real-world performance
4. Enable active divert mode
5. Measure: detection rate, false positive rate, system uptime, packages processed
6. Deploy at Pilot Customer #2
7. Collect data for model improvement (continuous learning pipeline)

**Gate**: Demonstrated ROI (scanner cost < prevented return costs) at both pilot sites

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Residual Risk |
|------|-----------|--------|------------|---------------|
| mmWave cannot resolve items inside package (physics limitation) | MEDIUM | CRITICAL | Phase 0 feasibility test with kill criteria. Multi-angle + ML may overcome single-sensor limitations | If multi-angle still fails, pivot to damage detection only (less resolution needed) |
| Similar items indistinguishable (blue shirt vs. red shirt) | HIGH | HIGH | Position product for "category-level" verification (is it a shirt vs. a mug) not "SKU-level" (which exact shirt). Address highest-value errors first. | Narrow initial market to cases where wrong items are categorically different |
| Conveyor vibration degrades radar signal | MEDIUM | MEDIUM | Vibration-isolated mounting, motion compensation in signal processing, shorter chirp sequences | Can be engineered out with proper mechanical design |
| Edge compute insufficient for real-time inference | LOW | MEDIUM | Jetson Orin has 100 TOPS; profile early, optimize model architecture. Fallback: batch processing with small buffer delay | Solvable with model optimization (quantization, pruning) |
| Vayyar pivots into this market | LOW-MEDIUM | HIGH | Speed to market, patent protection, customer lock-in via training data. If they enter, pivot to being acquired by them. | File patents immediately, build customer relationships |
| Long sales cycle delays revenue | HIGH | MEDIUM | Offer free pilot (hardware cost only), success-based pricing, target innovation-ready 3PLs | Accept 12-18 month sales cycle, plan capital accordingly |
| Amazon builds internally | MEDIUM | MEDIUM | Target non-Amazon 3PLs. Position as acquisition target. Amazon's internal R&D takes 3-5 years to productize. | Diversify customer base beyond Amazon ecosystem |
| Metal or liquid items in package block radar | MEDIUM | LOW | Characterize material limitations clearly, exclude from scanning (fall back to checkweigher). Most e-commerce items are non-metallic. | Product limitation, not failure |
| Cardboard moisture (humid warehouses) attenuates signal | LOW | LOW | Characterize attenuation vs. humidity. Standard warehouses are climate-controlled. | Unlikely to be blocking |
| Training data insufficient for accuracy targets | MEDIUM | HIGH | Synthetic data generation (simulate radar returns from known geometries), data augmentation, federated learning across pilot sites | Start with narrow SKU set, expand as data accumulates |

---

## Validation Plan

### Technical Validation Milestones

| Milestone | Success Criteria | Timeline | Method |
|-----------|-----------------|----------|--------|
| T1: Single-radar discrimination | >80% accuracy, 10 SKUs, static | Week 6 | Lab bench test |
| T2: Multi-radar improvement | >85% accuracy, 50 SKUs, static | Week 14 | Lab with 4-radar array |
| T3: Moving conveyor | >80% accuracy at 500 pkg/hr | Week 20 | Lab conveyor test |
| T4: Damage detection | >75% accuracy for major damage | Week 22 | Intentionally damaged items |
| T5: Continuous operation | 8hr runtime, <1% system failures | Week 26 | Stress test |
| T6: Production environment | >85% accuracy in real warehouse | Week 40 | Pilot site |

### Business Validation Milestones

| Milestone | Success Criteria | Timeline | Method |
|-----------|-----------------|----------|--------|
| B1: Problem validation | 5+ 3PLs confirm pain point in interviews | Week 4 | Customer discovery |
| B2: Willingness to pay | 2+ LOIs for pilot at $18K+ hardware | Week 16 | Sales conversations |
| B3: Pilot commitment | 2 signed pilot agreements | Week 24 | Contracts |
| B4: ROI proven | Scanner cost < prevented returns (measured) | Week 48 | Pilot data |
| B5: Reorder intent | Pilot customers commit to multi-unit purchase | Week 52 | Purchase orders |

---

## Cost & Time Estimate

### Total Capital Required

| Phase | Duration | Cost | Cumulative |
|-------|----------|------|-----------|
| Phase 0: Feasibility | Weeks 1-6 | $5,000 | $5,000 |
| Phase 1: Multi-angle prototype | Weeks 7-18 | $45,000 | $50,000 |
| Phase 2: Production prototype | Weeks 19-30 | $120,000 | $170,000 |
| Phase 3: Pilot deployment | Weeks 31-52 | $180,000 | $350,000 |
| Personnel (1 FTE founder + 1 contractor, 12mo) | Ongoing | $200,000 | $550,000 |
| Contingency (20%) | -- | $110,000 | $660,000 |
| **Total to pilot validation** | **12 months** | **$660,000** | |

### Revenue Timeline

| Quarter | Activity | Revenue |
|---------|----------|---------|
| Q1-Q2 | R&D, prototype, customer discovery | $0 |
| Q3 | Pilot deployments (subsidized) | $36K (2 units at $18K) |
| Q4 | Pilot results, begin sales pipeline | $0 |
| Q5 (Year 2 Q1) | First commercial sales | $90K (5 units) |
| Q6-Q8 | Scale sales | $500K-$1.5M |
| **Year 1 total** | | **$36K** (pilots only) |
| **Year 2 total** | | **$1.0-$1.5M** (conservative) |

### Funding Strategy
- **Phase 0**: Self-funded ($5K) -- pure technical feasibility
- **Phase 0 success -> Pre-seed**: $150K from angels/SAFE based on technical proof point
- **Phase 2 success -> Seed**: $500K-$1M based on working prototype + LOIs
- **Phase 3 success -> Series A**: $3-5M based on pilot results + pipeline

---

## Founder-Market Fit Assessment

### Founder Profile: AI/ML infrastructure engineer, deep Python/systems/cloud, no hardware background

| Dimension | Fit Score | Notes |
|-----------|-----------|-------|
| ML/AI expertise | 9/10 | Core competency. 3D reconstruction, signal processing ML, model deployment -- all within skillset |
| Signal processing | 6/10 | Related to ML but radar-specific DSP (FMCW, range-Doppler) requires learning curve. 2-3 months of study needed. |
| Hardware engineering | 3/10 | Major gap. PCB design, RF engineering, antenna optimization, industrial enclosure design -- will need contractor or cofounder |
| Systems integration | 8/10 | Strong. Connecting radar -> compute -> API -> WMS is systems engineering, directly in wheelhouse |
| Cloud/deployment | 9/10 | Strong. Edge deployment, OTA updates, fleet management, monitoring -- all familiar territory |
| Warehouse/logistics domain | 2/10 | Weak. No prior experience in 3PL operations, warehouse workflows, or logistics sales. Customer discovery needed. |
| Enterprise sales | 3/10 | Weak. Hardware sales to operations teams require different motion than SaaS/developer tools |
| Fundraising | 5/10 | Neutral. Technical founders can fundraise, but deep-tech hardware requires different investor profile (not typical SaaS VCs) |

### Critical Gaps to Address:

1. **Hardware engineering (CRITICAL)**: Must hire RF/radar engineer contractor within Phase 1. Options:
   - Freelance RF engineer from Upwork/Toptal ($150-250/hr) for antenna and PCB work
   - University collaboration (many ECE departments have mmWave labs)
   - TI's design services (they help customers build products on their chips)

2. **Logistics domain expertise (HIGH)**: Must acquire through:
   - 20+ customer discovery interviews in first 8 weeks
   - Advisor with 3PL operations background (offer 0.5-1% equity)
   - Attend logistics trade shows (MODEX, ProMat) for immersion

3. **Enterprise hardware sales (MEDIUM)**: Can defer initially:
   - First 2-3 sales via personal network / warm intros
   - Hire VP Sales after pilot success (not before)
   - Consider channel partnerships (systems integrators like Bastian Solutions, Dematic)

### Honest Assessment:
The founder can personally build the ML pipeline, the inference system, the API layer, and the dashboard. They CANNOT personally design the custom RF hardware or sell into warehouse operations without help. The minimum viable team for Phase 1 is founder + RF/radar contractor. The minimum viable team for Phase 3 is founder + RF engineer + business development person.

**Overall founder-market fit: 5.5/10** -- Strong on the AI/software side which is where the core IP lives, but meaningful gaps in hardware and domain expertise that must be filled with hires or advisors. This is a harder fit than a pure software startup but workable if the right radar engineer is found early.
