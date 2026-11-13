# Feasibility & Prototype Plan: AI Textile Defect Detection for Small Mills

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FABRICEYE SYSTEM v1                           │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │  Line-Scan   │    │  LED Line    │    │  Mounting Frame  │  │
│  │  Camera      │───>│  Light       │    │  (adjustable     │  │
│  │  (2K-4K px)  │    │  (diffuse)   │    │   width)         │  │
│  └──────┬───────┘    └──────────────┘    └──────────────────┘  │
│         │ GigE / USB3                                           │
│         v                                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  EDGE PC (NVIDIA Jetson Orin Nano / Intel N100)          │   │
│  │  ┌──────────┐  ┌────────────┐  ┌───────────────────┐    │   │
│  │  │ Frame    │  │ AI Model   │  │ Defect Mapper     │    │   │
│  │  │ Grabber  │->│ (TensorRT) │->│ + Roll Grader     │    │   │
│  │  │          │  │ YOLOv8/    │  │ + Report Gen      │    │   │
│  │  │          │  │ EfficientDet│  │                   │    │   │
│  │  └──────────┘  └────────────┘  └─────────┬─────────┘    │   │
│  │                                           │              │   │
│  │  ┌──────────────────┐  ┌─────────────────v──────────┐   │   │
│  │  │ Local Storage    │  │ UI (touchscreen / web)     │   │   │
│  │  │ (NVMe 256GB)     │  │ Operator view + dashboard  │   │   │
│  │  └──────────────────┘  └────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│         │ WiFi / Ethernet (when available)                      │
│         v                                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  CLOUD (optional, async sync)                            │   │
│  │  - Defect data aggregation    - Model retraining         │   │
│  │  - Multi-mill dashboard       - OTA model updates        │   │
│  │  - Analytics / trends         - Billing / licensing      │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Bill of Materials (BOM)

### Option A: Budget Build ($1,500 BOM)

| Component | Specific Part | Unit Cost | Confidence | Notes |
|-----------|--------------|-----------|------------|-------|
| Line-scan camera | IRAYPLE LB Series 2048px GigE | $487 | VERIFIED (Alibaba) | 2K resolution, 58kHz line rate, sufficient for 40m/min at 0.7mm/pixel |
| LED line light | Generic 500mm diffuse bar | $69 | VERIFIED (Alibaba) | May need 2x for full width |
| Edge PC | NVIDIA Jetson Orin Nano 8GB Dev Kit | $249 | VERIFIED (NVIDIA) | 67 TOPS AI performance; sufficient for YOLO inference |
| Mounting frame | Custom aluminum extrusion | $200 | ASSUMED | 80/20 extrusion + brackets; local fabrication |
| Touchscreen | 15.6" industrial capacitive | $180 | ASSUMED | AliExpress industrial panels |
| Lens | C-mount 25mm f/1.4 | $80 | ASSUMED | Standard machine vision lens |
| Cables + connectors | GigE cable, power, DIN rail | $60 | ASSUMED | |
| Enclosure / covers | Sheet metal + powder coat | $100 | ASSUMED | Protects from lint/dust |
| Power supply | 12V 10A industrial | $35 | VERIFIED | Mean Well or equivalent |
| Encoder (speed sync) | Rotary encoder + wheel | $40 | ASSUMED | Syncs camera to fabric speed |
| **TOTAL Option A** | | **$1,500** | | |

### Option B: Performance Build ($2,800 BOM)

| Component | Specific Part | Unit Cost | Confidence | Notes |
|-----------|--------------|-----------|------------|-------|
| Line-scan camera | Teledyne DALSA Linea 4K GigE | $1,200 | ASSUMED | 4096px, 80kHz, higher quality sensor |
| LED line light | Custom 2200mm diffuse (full width) | $300 | ASSUMED | Covers widest fabric |
| Edge PC | NVIDIA Jetson Orin NX 16GB | $500 | ASSUMED | 157 TOPS; headroom for larger models |
| Mounting frame | Custom precision aluminum | $300 | ASSUMED | Better adjustment mechanism |
| Touchscreen | 15.6" industrial IP65 | $250 | ASSUMED | Dust/water resistant |
| Lens | Schneider 35mm f/2.0 | $150 | ASSUMED | Premium optics |
| Cables + connectors | Industrial GigE + power | $80 | ASSUMED | |
| Enclosure | IP54 rated aluminum | $200 | ASSUMED | Full dust protection |
| Power supply | Industrial redundant | $50 | VERIFIED | |
| Encoder | Industrial rotary + wheel | $60 | ASSUMED | |
| NVMe storage | 512GB industrial grade | $80 | VERIFIED | |
| UPS | Small 30-min backup | $130 | ASSUMED | Prevents data loss on power cut |
| **TOTAL Option B** | | **$2,800** | | |

### Recommended: Start with Option A for prototype, ship Option B for production

**Sale price target**: $6,000 (Option A) to $8,000 (Option B)
**Gross margin**: 75% (Option A) to 65% (Option B)

---

## Software Stack

### Edge Software (runs on Jetson / edge PC)

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| OS | Ubuntu 22.04 + JetPack 6.x | NVIDIA's supported platform for Jetson |
| Camera SDK | Aravis (GigE Vision) or vendor SDK | Open-source GigE Vision library; works with any GigE camera |
| Frame pipeline | GStreamer + custom plugins | Low-latency video pipeline; handles line-scan reconstruction |
| AI inference | TensorRT (NVIDIA) | 10-50x faster than PyTorch; INT8 quantization for speed |
| Model | YOLOv8-nano or EfficientDet-Lite | Best accuracy/speed tradeoff for edge; <10ms per frame |
| Application | Python 3.11 + FastAPI | Rapid development; REST API for UI communication |
| UI | React (Electron or browser-based) | Touchscreen-friendly; local web server on edge PC |
| Database | SQLite (local) + sync to PostgreSQL (cloud) | Offline-first; eventual consistency |
| OTA updates | Mender.io or custom | Reliable A/B partition updates for edge devices |

### Cloud Software (optional, customer-facing)

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Backend | FastAPI on AWS (or GCP) | Same framework as edge; shared code |
| Database | PostgreSQL + TimescaleDB | Time-series defect data; efficient queries |
| Dashboard | Next.js or Grafana | Mill manager view; multi-language |
| Model training | PyTorch + W&B | Retraining pipeline from aggregated defect data |
| Storage | S3 | Defect images, reports, model artifacts |
| Auth | Firebase Auth or Cognito | Simple, multi-tenant |

### AI Model Architecture

```
Input: Line-scan image strips (2048px wide x 256px tall segments)
       ↓
Preprocessing: Normalize, augment (rotation, flip, brightness)
       ↓
Backbone: YOLOv8-nano (modified for 1D-like aspect ratios)
  - OR: EfficientDet-D0 with custom anchors
  - OR: Custom encoder-decoder (U-Net style for pixel-level segmentation)
       ↓
Head: Detection (bounding boxes) + Classification (defect type)
       ↓
Post-processing: NMS, confidence threshold, defect tracking across strips
       ↓
Output: Defect list with (x, y, width, height, class, confidence)
```

**Training data requirements:**
- Minimum viable: 5,000 labeled defect images across 10+ fabric types
- Production quality: 50,000+ images with 15+ defect categories
- Sources: Partner mills (install camera, collect data), public datasets (TILDA, AITEX), synthetic augmentation

---

## Build Instructions (Prototype in 12 Weeks)

### Phase 1: Camera + Lighting Validation (Weeks 1-3)

**Goal**: Prove we can capture fabric defects with sufficient resolution

1. **Week 1**: Order components
   - IRAYPLE 2K line-scan camera ($487)
   - LED line light ($69)
   - Jetson Orin Nano Dev Kit ($249)
   - Mounting hardware, lens, cables (~$200)
   - **Total initial spend: ~$1,100**

2. **Week 2**: Camera integration
   - Install JetPack 6.x on Jetson
   - Get camera streaming via Aravis/GigE
   - Test line rates at different fabric speeds (manual pull-through)
   - Validate image quality: can we see 0.5mm defects at 30m/min?

3. **Week 3**: Lighting optimization
   - Test direct vs. diffuse vs. dark-field illumination
   - Determine optimal camera-to-fabric distance (typically 200-400mm)
   - Document settings for different fabric types (white cotton vs. dark denim)

**Milestone**: Can capture clear images showing real defects at target speed

### Phase 2: AI Model Development (Weeks 3-8)

**Goal**: Train a model that detects 80%+ of defects with <10% false positives

4. **Weeks 3-4**: Data collection
   - Partner with 1-2 local mills (offer free inspection audit in exchange for data access)
   - Collect 2,000+ images of good fabric + known defects
   - Label using CVAT or Labelbox (outsource to labeling service if needed)
   - Supplement with public datasets (AITEX: 245 images, 7 defect types; TILDA: 800 images)

5. **Weeks 5-6**: Model training v1
   - Train YOLOv8-nano on collected data
   - Evaluate on held-out test set
   - Target: mAP50 > 0.75 on test set

6. **Weeks 7-8**: Edge optimization
   - Convert to TensorRT (INT8 quantization)
   - Benchmark: must achieve <20ms per frame on Jetson Orin Nano
   - Stress test: continuous operation for 8 hours (one shift)

**Milestone**: Model running on Jetson, detecting defects in real-time

### Phase 3: Application Layer (Weeks 7-10)

**Goal**: Operator-usable interface with reporting

7. **Weeks 7-8**: Core application
   - Frame pipeline: camera -> inference -> defect map
   - Speed encoder integration (sync line position to physical position)
   - Local database for roll records

8. **Weeks 9-10**: UI + reporting
   - Touchscreen UI: live view, defect markers, roll start/stop
   - Report generation: PDF per roll with defect map + grade
   - Basic dashboard: rolls inspected today, defect rate trend

**Milestone**: Complete system demo-able to mill owners

### Phase 4: Field Validation (Weeks 10-12)

**Goal**: Prove it works in a real mill environment

9. **Weeks 10-11**: Install at partner mill
   - Mount on their inspection table
   - Run alongside human inspector for 100+ rolls
   - Measure: detection rate vs. human, false positive rate, uptime

10. **Week 12**: Iterate and document
    - Fix issues found in field (dust, vibration, speed variation, fabric curl)
    - Create installation guide
    - Collect testimonial / case study data

**Milestone**: System running in production at one mill for 1+ week

---

## Risk Register

| # | Risk | Probability | Impact | Mitigation |
|---|------|-------------|--------|------------|
| 1 | Camera resolution insufficient for fine defects (needle holes, thin yarn breaks) | MEDIUM | HIGH | Test multiple cameras early; upgrade to 4K if 2K fails; can always increase magnification with narrower FOV |
| 2 | AI model struggles to generalize across fabric types | HIGH | HIGH | Collect diverse training data from day 1; use few-shot learning / fabric-specific fine-tuning; plan for per-customer calibration step |
| 3 | Jetson thermal throttling in hot mill environment (40-50C ambient in India) | MEDIUM | MEDIUM | Add heat sink + fan; test at elevated temps; fall back to Intel N100 (lower power) if needed |
| 4 | Lighting variation (daylight from windows, machine shadows) | MEDIUM | MEDIUM | Enclosed light tunnel design; high-frequency LED eliminates ambient; test with worst-case conditions |
| 5 | Fabric speed variation causes blur or missed sections | MEDIUM | MEDIUM | Encoder-based triggering (not free-running); test at 2x max expected speed |
| 6 | Mill environment (dust, lint, vibration) damages equipment | MEDIUM | LOW | IP54 enclosure; regular cleaning schedule; vibration dampening mounts |
| 7 | No partner mill willing to let us install prototype | LOW | HIGH | Offer free audit + free system; leverage textile association connections; target progressive mill owners |
| 8 | Jetson Orin Nano supply constraints | LOW | MEDIUM | Alternative: Intel N100 mini-PC + Hailo-8 AI accelerator; or Rockchip RK3588 |
| 9 | Customer expects 99% detection (Uster-level) but we deliver 90% | HIGH | MEDIUM | Set expectations clearly: "better than human" (65%) not "perfect"; position as complement to human inspector, not replacement |
| 10 | Payment collection from small mills in developing markets | HIGH | HIGH | Prepaid annual plans with discount; hardware lease with remote disable; work with textile machinery finance companies |

---

## Validation Plan

### Technical Validation (before spending >$5K)

| Test | Pass Criteria | Method | Cost |
|------|--------------|--------|------|
| Image quality | Resolve 0.5mm defects at 30m/min | Lab test with calibration targets | $1,100 (components) |
| Inference speed | <20ms per 2K frame on Jetson | Benchmark with TensorRT | $0 (same hardware) |
| Detection accuracy | mAP50 > 0.75 on 200+ test images | Held-out dataset evaluation | $500 (labeling) |
| Thermal stability | 8-hour run at 45C ambient | Thermal chamber or summer test | $0-$200 |
| End-to-end latency | Defect alert within 50ms of defect passing camera | Stopwatch + high-speed video | $0 |

### Market Validation (before spending >$20K)

| Test | Pass Criteria | Method |
|------|--------------|--------|
| Price sensitivity | 3+ mills say "yes" at $6K-$8K + $200-$400/mo | In-person interviews (20 mills) |
| Willingness to install | 2+ mills agree to free pilot installation | Direct outreach |
| Budget authority | Identified decision-maker can approve $6K-$8K without board approval | Discovery calls |
| Alternative comparison | System beats their current human inspection by measurable margin | Side-by-side test |

---

## Cost & Time Estimate

### Prototype Phase (Months 1-3): $15K-$25K

| Item | Cost |
|------|------|
| Hardware (2 prototype units) | $3,000 |
| Data labeling (5,000 images) | $2,000 |
| Travel to textile clusters (2 trips to India) | $5,000 |
| Cloud compute for training (AWS/GCP) | $1,000 |
| Miscellaneous (tools, shipping, contingency) | $2,000 |
| **Living expenses (3 months, if full-time)** | **$9,000** |
| **Total** | **$22,000** |

### MVP Phase (Months 4-7): $60K-$80K

| Item | Cost |
|------|------|
| Hardware (10 pilot units) | $15,000 |
| Software development (1 contractor, 4 months) | $30,000 |
| Additional data collection + labeling | $5,000 |
| Travel + installation at pilot sites | $8,000 |
| Cloud infrastructure | $2,000 |
| Legal (company formation, contracts) | $3,000 |
| **Total** | **$63,000** |

### Scale Phase (Months 7-12): $150K-$200K

| Item | Cost |
|------|------|
| Manufacturing first batch (50 units) | $75,000 |
| Sales + marketing (trade shows, demos) | $30,000 |
| Team (2 hires: field engineer + sales) | $50,000 |
| Working capital (inventory, receivables) | $30,000 |
| Cloud + support infrastructure | $10,000 |
| **Total** | **$195,000** |

### Grand Total to Year 1 Revenue: ~$280K
(Matches the stated capital requirement)

---

## Founder-Market Fit Assessment

**Founder profile**: AI/ML infrastructure engineer, deep Python/systems/cloud, NO hardware background

### Strengths for This Venture

| Factor | Rating | Explanation |
|--------|--------|-------------|
| AI/ML model development | 9/10 | Can build, train, optimize, and deploy the core AI model without external help |
| Edge deployment (TensorRT, Jetson) | 8/10 | NVIDIA ecosystem is well-documented; Python skills transfer directly |
| Cloud infrastructure | 9/10 | Can build the SaaS dashboard, OTA updates, model retraining pipeline solo |
| Systems engineering | 8/10 | Understanding of latency, throughput, reliability from infra background |
| Data pipeline design | 9/10 | Critical for the data flywheel (collection -> labeling -> retraining -> deployment) |

### Gaps for This Venture

| Factor | Rating | Explanation | Mitigation |
|--------|--------|-------------|------------|
| Hardware design | 3/10 | No experience with cameras, optics, lighting, industrial mounting | Use COTS components; hire mechanical engineer contractor for frame design; no custom PCBs in v1 |
| Optics / imaging science | 2/10 | Lighting geometry, lens selection, sensor calibration are specialized | Study fundamentals (2 weeks); consult with machine vision distributor; empirical testing |
| Textile domain knowledge | 1/10 | Does not know fabric types, defect taxonomy, mill workflows | Partner with retired textile QC manager as advisor; spend 2 weeks in mills observing |
| Emerging market sales | 2/10 | No experience selling to Indian/Bangladeshi manufacturers | Hire local sales agent (commission-only initially); leverage textile association introductions |
| Manufacturing at scale | 2/10 | No experience with BOM optimization, supplier management, assembly | Contract manufacturer for assembly; keep design simple (fewer than 10 components) |
| Hindi/Bengali/Turkish language | 1/10 | Essential for customer communication | Hire multilingual team members; localize UI early |

### Overall Founder-Market Fit: 5/10 (MARGINAL)

**Honest assessment**: The founder can build the AI and software (which IS the core IP), but cannot solo-execute on hardware, domain expertise, or go-to-market in emerging markets. This is a team venture, not a solo founder play.

**Recommended team composition:**
1. Founder (AI/ML + systems) -- builds the brain
2. Co-founder or early hire: Textile industry veteran from India -- provides domain + customer access
3. Contractor: Mechanical/optical engineer -- designs the hardware
4. Early hire: Field sales/support in target geography -- installs, trains, collects

**De-risking path for a solo AI founder:**
1. Build the AI model first (plays to strength)
2. Use commodity hardware (no custom design needed for v1)
3. Partner with an existing inspection table manufacturer (they provide hardware, you provide AI)
4. Find a textile cluster "champion" -- one progressive mill owner who becomes your first customer AND advisor
