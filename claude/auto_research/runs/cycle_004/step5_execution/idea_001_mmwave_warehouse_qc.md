# Execution Plan: Smart Warehouse QC Module (mmWave Through-Package Inspection)

## 5a. Product Definition

**Core value proposition**: Non-destructive inspection of sealed packages on warehouse conveyor belts using mmWave radar — detect damaged, missing, or wrong items inside boxes without opening them, reducing costly returns and shipping errors.

**Key features for MVP (max 3)**:
1. mmWave radar scanner module that mounts on existing conveyor belts (plug-and-play hardware)
2. AI-powered 3D reconstruction that detects anomalies inside sealed packages (broken items, missing components, wrong product)
3. Real-time reject/pass decision with WMS integration (alert operators or auto-divert damaged packages)

**What it does NOT do**:
- Not a full warehouse management system (we integrate with existing WMS)
- Not visual inspection of external package condition (that's camera-based, well-served)
- Not X-ray (no ionizing radiation, no regulatory barriers)
- Not content identification for security (no reading labels or detecting contraband — that's a different regulatory regime)

**Success metrics for prototype validation**:
- Detect 80%+ of significant product damage (broken glass, crushed items, large missing components) inside sealed cardboard boxes
- False positive rate < 5% (to avoid unnecessary diverts)
- Process 30+ packages per minute (match conveyor speed)
- At least 2 pilot deployments at fulfillment centers

---

## 5b. Technical Architecture

**System diagram**:
```
[Conveyor Belt] → [mmWave Radar Array (multiple angles)] → [3D Point Cloud] → [AI Anomaly Detection] → [Pass/Reject Signal]
                                                                                                              ↓
                                                                                                    [WMS Integration API]
                                                                                                              ↓
                                                                                                    [Diverter Gate / Alert]
```

**Technology stack**:
- **Radar hardware**: Texas Instruments AWR2944 (77GHz mmWave radar, 4 TX / 4 RX antennas) × 4 units arrayed around conveyor for multi-angle view
- **Signal processing**: FMCW radar → range-Doppler → 3D point cloud (TI's DCA1000EVM for raw data capture)
- **3D reconstruction AI**: Trained neural network (inspired by MIT mmNorm) that converts multi-angle radar reflections into volumetric representation
- **Anomaly detection**: Comparison of reconstructed object against "golden reference" model (what the package SHOULD contain) — flagging deviations beyond threshold
- **Integration**: REST API for WMS integration + industrial I/O (24V signal to conveyor diverter gate)
- **Compute**: Edge GPU (Nvidia Jetson Orin) mounted locally for real-time inference

**Build vs. Buy**:
| Component | Decision | Rationale |
|-----------|----------|-----------|
| Radar modules | BUY (TI AWR2944) | Commodity, $40-100 per module |
| 3D reconstruction AI | BUILD | Core IP — the algorithm that makes radar data useful |
| Anomaly detection model | BUILD | Core IP — trained on package-specific data |
| Edge compute | BUY (Jetson Orin) | Standard embedded GPU |
| Conveyor mounting hardware | BUILD (sheet metal + 3D print) | Simple mechanical integration |
| WMS integration | BUILD | API layer, straightforward software |

---

## 5c. Bill of Materials / Resources

### Hardware per Scanner Unit

| Item | Cost | Notes |
|------|------|-------|
| TI AWR2944 radar modules × 4 | $400 | 77GHz mmWave, production pricing |
| TI DCA1000EVM data capture boards × 4 | $800 | Raw radar data acquisition |
| Nvidia Jetson Orin NX | $500 | Edge AI inference |
| Custom mounting frame (sheet metal) | $300 | Conveyor-mount enclosure |
| Industrial I/O board (24V relay) | $100 | Diverter gate control |
| Power supply + cabling | $200 | Industrial 24V + 12V |
| Ethernet switch + enclosure | $200 | Networking |
| **Total per unit (BOM)** | **~$2,500** | |

### Development Costs

| Item | Cost |
|------|------|
| TI radar dev kits (for R&D) × 8 | $4,000 |
| Jetson dev kits × 3 | $1,500 |
| Test packages (various products, damage types) | $5,000 |
| Cloud compute for model training (AWS) | $20,000 |
| Conveyor section for lab testing | $8,000 |
| Misc electronics & tools | $5,000 |

### Personnel (12 months)

| Role | Count | Annual Cost |
|------|-------|-------------|
| Radar/signal processing engineer (lead) | 1 | $180,000 |
| ML/computer vision engineer | 1 | $175,000 |
| Embedded systems engineer | 1 | $160,000 |
| Business dev / operations | 1 | $140,000 |
| **Total** | 4 | **$655,000** |

---

## 5d. Build Instructions (abbreviated)

**Phase 1 (Weeks 1-12)**: Radar data collection + AI model training
- Collect radar scans of 500+ package types (intact + various damage modes)
- Train 3D reconstruction model
- Train anomaly detection model
- **Gate**: Can we detect major damage (crushed box, broken glass) at >80%?

**Phase 2 (Weeks 10-20)**: Hardware integration + conveyor testing
- Build scanner array mounting hardware
- Integrate with Jetson for real-time inference
- Test at conveyor speed (30+ packages/minute)
- **Gate**: Real-time processing at line speed?

**Phase 3 (Weeks 18-30)**: Pilot deployment
- Deploy at 2 fulfillment centers for 90-day pilot
- Measure damage detection rate, false positive rate, throughput
- Build WMS integration for pilot customer's system
- **Gate**: Proven ROI (cost of scanner < cost of prevented returns)?

---

## 5g. Cost Estimate

| Category | Cost |
|----------|------|
| Personnel (12 months) | $655,000 |
| R&D hardware | $44,000 |
| Cloud compute (training) | $20,000 |
| Pilot deployment hardware (5 units) | $12,500 |
| Travel/customer visits | $25,000 |
| Legal/IP | $20,000 |
| Contingency (15%) | $117,000 |
| **Total to pilot validation** | **~$894K** |

**Revenue model**: Hardware module ($15-30K per unit installed) + SaaS ($2-5K/month for AI + updates)
**Target**: 100 units deployed Year 2 = $1.5-3M hardware + $2.4-6M ARR SaaS = $4-9M total
