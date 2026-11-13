# Feasibility & Prototype Plan: AI Pallet Damage Detection Station

## Architecture Overview

```
[Dock Door Opening]
        |
   [Steel Frame] -- mounted above/around door opening
        |
   +----+----+----+
   |    |    |    |
 Cam1  Cam2  Cam3  LED Bars (x4)
 (top) (left) (right)
        |
   [PoE Switch]
        |
   [Edge PC] -- running inference + local dashboard
        |
   [Alert System] -- LED light bar (red/green) + optional buzzer
        |
   [Wi-Fi/Ethernet] -- to facility network
        |
   [Cloud] -- dashboard, model updates, fleet management (optional)
```

**Data flow:**
1. Motion/presence sensor triggers capture sequence
2. 3 cameras fire simultaneously (or in rapid sequence <100ms)
3. Images preprocessed on edge PC (resize, normalize, align)
4. YOLO/Detectron2 model runs inference (~50-200ms on Jetson Orin)
5. Defect classification output (type, location, confidence score)
6. Pass/fail decision applied against threshold
7. Alert system activated if fail
8. Images + metadata stored locally (7-day rolling buffer) and synced to cloud

## Bill of Materials

### Hardware BOM (per station)

| Component | Specific Part | Qty | Unit Cost | Total | Confidence |
|-----------|--------------|-----|-----------|-------|------------|
| Industrial camera | FLIR Blackfly S BFS-U3-51S5C-C (5MP, USB3, global shutter) | 3 | $595 | $1,785 | VERIFIED (FLIR distributor pricing) |
| Camera lens | Tamron M118FM16 (16mm, 1/1.8" C-mount) | 3 | $180 | $540 | VERIFIED (standard industrial lens) |
| LED bar light | Smart Vision Lights LXE300 (300mm, 24V, IP67) | 4 | $125 | $500 | ASSUMED (could use cheaper bars at $60-80 each) |
| Edge compute | NVIDIA Jetson Orin Nano Developer Kit (8GB) | 1 | $499 | $499 | VERIFIED (NVIDIA direct pricing) |
| PoE switch | Netgear GS305EP (5-port managed PoE+) | 1 | $80 | $80 | VERIFIED |
| USB3 hub | Industrial USB3 hub (powered, 4-port) | 1 | $65 | $65 | ASSUMED |
| Steel frame | Custom welded steel frame, powder-coated | 1 | $400 | $400 | ASSUMED (local fabrication shop quote) |
| Alert light | Banner TL50 tower light (red/green/amber) | 1 | $120 | $120 | VERIFIED |
| Buzzer | Industrial piezo buzzer, 24V, IP65 | 1 | $35 | $35 | VERIFIED |
| Power supply | Mean Well 24V 150W DIN-rail | 1 | $55 | $55 | VERIFIED |
| Enclosure | NEMA 4X fiberglass enclosure (for PC + switch) | 1 | $150 | $150 | ASSUMED |
| Cabling | Cat6 + USB3 + power cables, connectors | 1 | $120 | $120 | ASSUMED |
| Motion sensor | Banner QS30 photoelectric sensor (trigger) | 1 | $85 | $85 | VERIFIED |
| Mounting hardware | Brackets, bolts, cable management | 1 | $75 | $75 | ASSUMED |

**Total Hardware BOM: $4,509**

Note: Original estimate was $3,500. Revised upward after specifying actual parts. The $2K camera budget was optimistic -- quality industrial cameras with appropriate lenses cost ~$775/each. Could reduce to $3,500 by using cheaper cameras (Basler ace 2 at $400 each) or consumer-grade alternatives, but reliability suffers.

### Alternative BOM (Budget Version)

| Component | Part | Cost | Trade-off |
|-----------|------|------|-----------|
| Camera (x3) | Basler ace 2 a2A1920-51gcBAS (2MP GigE) | $350 x 3 = $1,050 | Lower resolution, adequate for pallet damage |
| Edge compute | Intel NUC 13 Pro (i5-1340P) | $450 | No GPU -- must use ONNX/OpenVINO optimization |
| LED bars | Generic Amazon industrial LED bars | $40 x 4 = $160 | Less uniform illumination, shorter lifespan |

**Budget BOM total: ~$3,200** (closer to original $3,500 estimate)

## Software Stack

| Component | Technology | License | Cost |
|-----------|-----------|---------|------|
| OS | Ubuntu 22.04 LTS (Jetson: JetPack 6.0) | Free (open source) | $0 |
| ML framework | PyTorch 2.x | BSD | $0 |
| Detection model | YOLOv8/v9 (Ultralytics) | AGPL-3.0 (requires commercial license for closed-source deployment) | $1,500/year OR use Apache-licensed alternative |
| Alternative model | Detectron2 (Meta) | Apache 2.0 | $0 |
| Model optimization | TensorRT (NVIDIA) | Proprietary (free with Jetson) | $0 |
| Camera SDK | Spinnaker SDK (FLIR) | Proprietary (free with FLIR cameras) | $0 |
| Web dashboard | FastAPI + React (or Streamlit for prototype) | MIT | $0 |
| Database | SQLite (local) + PostgreSQL (cloud) | Free | $0 |
| Cloud sync | MQTT + S3 | AWS costs ~$20/month/station | $240/year |
| Labeling tool | Label Studio | Apache 2.0 | $0 |
| Monitoring | Prometheus + Grafana (or simple health check endpoint) | Apache 2.0 | $0 |

**IMPORTANT LICENSE NOTE**: Ultralytics YOLO is AGPL-3.0. Using it in a commercial product without open-sourcing your code requires an Enterprise License (~$1,500/year). Alternative: use Detectron2 (Apache 2.0) or train a custom model architecture.

## Step-by-Step Build Instructions (First Prototype)

### Phase 1: Data Collection & Model Training (Weeks 1-4)

**Week 1-2: Dataset assembly**
1. Source pallet damage images from:
   - Roboflow Universe public datasets (1,349+ images available)
   - Partner with local pallet recycler for access to damaged pallets (photograph 200+ pallets with various defect types)
   - Synthetic augmentation (rotate, crop, lighting changes)
2. Target: 2,000+ labeled images across 6 defect classes:
   - Broken top deck board
   - Broken stringer/block
   - Protruding nail
   - Crack/split
   - Missing board
   - Excessive wear/rot
3. Use Label Studio for annotation (bounding boxes + class labels)

**Week 3-4: Model training**
1. Start with YOLOv8m pre-trained on COCO
2. Fine-tune on pallet dataset (transfer learning)
3. Training hardware: Any GPU instance (AWS g4dn.xlarge at $0.52/hr, ~10 hours = $5.20)
4. Target metrics: mAP@50 > 0.85, inference time < 100ms on Jetson
5. Export to TensorRT for Jetson deployment
6. Validate on held-out test set (20% of data)

### Phase 2: Hardware Assembly (Weeks 3-5, overlapping with Phase 1)

**Week 3: Procurement**
1. Order all BOM components (lead time: cameras 1-2 weeks, Jetson 3-5 days, frame 1-2 weeks custom fab)
2. Set up Jetson Orin Nano with JetPack 6.0

**Week 4: Bench assembly**
1. Mount cameras on test fixture (simulate dock door geometry)
2. Wire LED bars to power supply
3. Configure camera exposure/gain settings for warehouse lighting + LED supplementation
4. Test trigger sequence (motion sensor -> capture -> inference pipeline)
5. Validate image quality at various forklift speeds (3-8 mph typical)

**Week 5: Integration testing**
1. Assemble full frame with all components
2. End-to-end pipeline test: motion trigger -> 3-camera capture -> inference -> alert
3. Measure total latency (target: <2 seconds from trigger to verdict)
4. Stress test: 100 consecutive passes, measure reliability
5. Test failure modes (camera failure, network loss, power glitch)

### Phase 3: Lab Validation (Weeks 5-6)

1. Collect 50 damaged pallets (various defect types and severities)
2. Run each through prototype system
3. Measure:
   - True positive rate (defects correctly caught)
   - False positive rate (good pallets incorrectly flagged)
   - False negative rate (defects missed -- most critical)
   - Latency distribution
4. Target: >90% true positive, <5% false positive, <3% false negative on obvious defects
5. Document failure cases for model improvement

### Phase 4: Field Pilot (Weeks 7-10)

1. Identify pilot site (see Customer Validation doc)
2. Install prototype at one dock door
3. Run in "shadow mode" for 2 weeks (alerts visible but non-binding)
4. Collect ground truth by having dock supervisor verify predictions
5. Tune sensitivity threshold based on facility preferences
6. Switch to "active mode" with alerts for remaining 2 weeks
7. Collect pilot metrics for case study

## Risk Register

| # | Risk | Likelihood | Impact | Mitigation | Fallback |
|---|------|-----------|--------|------------|----------|
| 1 | Cameras cannot capture clear images at forklift speed (3-8 mph) | MEDIUM | HIGH | Use global shutter cameras, short exposure time (1-2ms), high-power LED strobes. Test at maximum expected speed. | Reduce speed requirement to walking pace; add speed bump/slow zone at dock door. |
| 2 | Insufficient training data for rare defect types (protruding nails, internal cracks) | HIGH | MEDIUM | Use synthetic data augmentation. Partner with pallet recycler for access to diverse damage. Transfer learning from general defect detection. | Ship with fewer defect classes in v1. Add classes over time with field data. |
| 3 | High false positive rate in production (dust, dirt, surface marks confused with cracks) | HIGH | HIGH | Aggressive data augmentation with dirty/marked pallets. Multi-frame averaging. Confidence threshold tuning per site. | Allow per-site threshold tuning. Accept 5-10% false positive rate with easy override. |
| 4 | Warehouse lighting variability defeats vision system | MEDIUM | MEDIUM | Dedicated LED light bars create controlled illumination zone. Cameras set to fixed exposure. | Add more LED bars. Use IR illumination. Train model with diverse lighting augmentation. |
| 5 | Jetson Orin insufficient for 3-camera simultaneous inference | LOW | MEDIUM | Benchmark early. TensorRT optimization. Sequential capture (not simultaneous) is acceptable. | Upgrade to Jetson AGX Orin ($999) or process images sequentially. |
| 6 | Frame vibration from forklift traffic causes image blur | MEDIUM | LOW | Vibration-isolated mounting. Use machine vision cameras with vibration resistance. Strobe illumination freezes motion. | Add anti-vibration pads. Reduce capture to moments between forklift passes. |
| 7 | Facility IT refuses to allow device on network | MEDIUM | MEDIUM | Offer standalone mode (local dashboard only, USB export). Cellular modem option. | Operate fully offline with local storage. Cloud sync via USB drive weekly. |
| 8 | Pallets partially obscured by product/wrap on fork tines | HIGH | MEDIUM | Train model on partially visible pallets. Focus on visible surfaces only. Accept reduced detection for obscured areas. | Market as "inbound empty pallet inspection" only (pallets without product). |
| 9 | Customer expects 100% detection rate, real-world performance is 85-92% | HIGH | HIGH | Set expectations upfront: "catches defects humans miss, not perfect." Emphasize it as a supplement to (not replacement for) human awareness. | Position as "evidence capture for liability" rather than "automated rejection." |

## Validation Plan

### Success Criteria (Prototype)
- Detection accuracy: >85% mAP@50 on test set
- False positive rate: <10% in controlled environment
- Latency: <2 seconds trigger-to-verdict
- Reliability: >99% uptime over 7-day continuous test
- Forklift speed tolerance: works at up to 5 mph

### Success Criteria (Pilot)
- Catches at least 1 genuinely damaged pallet per day at a busy facility
- False positive rate <15% in production environment (acceptable for v1)
- Dock workers do not ignore alerts (behavioral adoption)
- Customer agrees to provide testimonial or continue paid engagement

### Validation Timeline
| Week | Milestone | Go/No-Go Decision |
|------|-----------|-------------------|
| 4 | Model achieves >80% mAP on lab data | If <70%, need more data or different approach |
| 6 | Full prototype passes 50-pallet lab test at >85% detection | If <75%, hardware or model redesign needed |
| 8 | Pilot site installed and running in shadow mode | If no pilot site secured, pivot to different market |
| 10 | Pilot results show >1 catch/day, customer satisfied | If customer disengages, fundamental product-market issue |

## Total Cost and Time Estimate

### Prototype Cost
| Category | Cost | Notes |
|----------|------|-------|
| Hardware (1 station) | $4,509 | Full BOM above |
| Cloud compute (training) | $200 | GPU instances for model training |
| Software licenses | $0-$1,500 | Depends on YOLO license vs Detectron2 |
| Data collection (pallet recycler access) | $500 | Gas, time, possible payment for access |
| Miscellaneous (tools, spare parts) | $500 | |
| **Total prototype** | **$5,709 - $7,209** | |

### Full $220K Budget Allocation
| Category | Amount | Notes |
|----------|--------|-------|
| Vision engineer (5 months, contractor) | $75,000 | $15K/month, senior ML engineer |
| Founder salary (5 months) | $50,000 | Minimal living expenses |
| Hardware (5 pilot stations + 2 dev units) | $31,563 | 7 x $4,509 |
| Installation & travel (5 pilot sites) | $15,000 | $3K/site (travel, hotel, misc) |
| Cloud infrastructure | $5,000 | Training, dashboard hosting, S3 storage |
| Legal (incorporation, contracts, liability) | $10,000 | LLC + customer contracts + liability insurance |
| Sales & marketing | $15,000 | Website, trade show (ProMat), materials |
| Insurance (product liability) | $8,000 | Critical for hardware in warehouses |
| Contingency (20%) | $10,437 | Unexpected costs |
| **Total** | **$220,000** | |

### Timeline
| Month | Milestone |
|-------|-----------|
| Month 1 | Data collection, model training, hardware procurement |
| Month 2 | Prototype assembly, lab testing, iterate |
| Month 3 | First pilot site installation (shadow mode) |
| Month 4 | Pilot validation, second + third sites |
| Month 5 | First revenue (convert pilots to paid), begin manufacturing pipeline |
| Month 6-8 | Scale to 10 paid stations |
| Month 9-12 | Scale to 100 stations (requires additional capital or revenue-funded) |

## Founder-Market Fit Assessment

**Founder profile**: Hooman Shariati -- AI/ML infrastructure engineer at Adobe, deep Python/systems/cloud expertise, no hardware background, no warehouse/logistics industry connections.

### Fit Analysis

| Dimension | Score | Notes |
|-----------|-------|-------|
| ML/AI capability | 9/10 | Core strength. Can build and optimize detection models. |
| Systems/cloud engineering | 9/10 | Can build the full software stack, dashboard, cloud sync. |
| Hardware design | 3/10 | No embedded systems or industrial hardware experience. Frame design, camera selection, thermal management, IP ratings are new. |
| Logistics domain knowledge | 2/10 | No warehouse industry experience. Doesn't know the buyer, the procurement process, or the operational reality. |
| Sales to industrial buyers | 2/10 | Enterprise sales to VP-Operations at 3PLs is very different from tech/SaaS sales. Long cycles, relationship-driven. |
| Capital efficiency | 7/10 | Lean engineering background. Can build the software without a team. Hardware requires a contractor. |

### Gaps to Fill
1. **Hardware integration partner**: Need someone who has built industrial machine vision products. Either hire contractor ($15K/month) or find co-founder with this background.
2. **Industry advisor**: Need someone who has sold to warehouse/logistics buyers. A former VP-Ops at a 3PL would be ideal. Could find via LinkedIn or industry events (ProMat, MODEX).
3. **Pilot site access**: No existing relationships. Will need cold outreach or industry introductions.

### Overall Fit: 4/10
The founder brings strong ML/software capability but lacks the two most critical ingredients for this specific business: (1) hardware product experience and (2) logistics industry access. These are fillable gaps but add time, cost, and execution risk compared to a founder who has both. A founder who was previously VP-Engineering at a logistics tech company (e.g., Locus Robotics, 6 River Systems, Fetch Robotics) would be ideal for this opportunity.
