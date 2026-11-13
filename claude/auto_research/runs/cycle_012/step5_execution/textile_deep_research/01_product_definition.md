# Product Definition: AI Textile Defect Detection for Small Mills

## Problem Statement

Small and medium textile mills (100-500 employees) in India, Bangladesh, Turkey, and Vietnam produce fabric with 2-8% defect rates. Manual human inspection catches only 60-70% of defects at speeds of 15-25 m/min. These mills lose $50K-$200K annually in customer returns, price downgrades, and waste.

Existing automated solutions (Uster FABRIQ VISION at $100K-$500K, Shelton WebSpector at $50K-$150K) are priced 10-50x beyond what these mills can afford. The result: 100,000+ mills worldwide rely on tired human inspectors squinting at moving fabric under fluorescent lights.

**The gap**: No productized, AI-powered fabric inspection system exists at the $5K-$10K price point with edge inference capability.

**Confidence**: HIGH -- price gap is verifiable from competitor pricing; manual inspection limitations are well-documented in textile quality literature.

---

## Product Scope v1: "FabricEye"

### Core System
A turnkey hardware + software unit that mounts above the fabric inspection table or take-up roller, inspecting fabric in real-time as it passes beneath.

### What It Does (v1)
1. **Detects defects** in woven and knitted fabrics at speeds up to 60 m/min
2. **Classifies defects** into standard taxonomy (hole, stain, broken yarn, missing pick, slub, oil spot, crease mark -- 15+ categories)
3. **Maps defects** with position coordinates (length + width) on a digital fabric map
4. **Grades rolls** using 4-point or 10-point grading systems (buyer-configurable)
5. **Generates reports** per roll, per lot, per shift -- exportable as PDF or integrated with local ERPs

### What It Does NOT Do (v1)
- Color measurement / shade variation (requires expensive spectrophotometer -- v2)
- Pattern matching for printed fabrics (requires separate training pipeline -- v2)
- Predictive maintenance on looms (requires loom integration -- v3)
- Automatic fabric cutting optimization (partner with existing cutting software)

---

## User Workflow

### Setup (one-time, 2 hours)
1. Mount camera bar above inspection table (adjustable bracket, 1.6-2.2m fabric width)
2. Connect LED line light (already integrated in bar)
3. Power on edge PC (pre-configured, auto-boots inspection software)
4. Run calibration: pass 2m of known-good fabric; system auto-adjusts exposure/threshold
5. Select fabric type from library OR create new fabric profile (5 min guided process)

### Daily Operation
1. Operator loads roll on inspection table
2. Scans roll barcode (or enters roll ID manually on touchscreen)
3. Presses START -- fabric moves at normal inspection speed
4. System displays live defect markers on 15" touchscreen (green = good, red = defect)
5. Operator can pause, mark false positives, add manual annotations
6. At roll end: system shows summary -- defect count, grade, pass/fail
7. Report auto-saves; syncs to cloud dashboard when internet available (offline-first)

### Mill Manager View (mobile app / web dashboard)
- Daily/weekly defect trends
- Operator performance comparison
- Supplier quality scorecards (which yarn lots produce more defects)
- Alerts for sudden defect rate spikes (e.g., loom malfunction)

---

## Pricing Model

### Hardware (one-time)
| Component | Cost to Us | Sale Price |
|-----------|-----------|------------|
| Line-scan camera (2K-4K resolution) | $500-$1,200 | Included |
| LED line light (500mm-2200mm) | $100-$300 | Included |
| Edge PC (NVIDIA Jetson Orin Nano or equivalent) | $249-$500 | Included |
| Frame/mounting bracket (custom aluminum) | $200-$400 | Included |
| Touchscreen display (15" industrial) | $150-$300 | Included |
| Cables, connectors, enclosure | $100-$200 | Included |
| **Total BOM** | **$1,300-$2,900** | -- |
| **System Sale Price** | -- | **$6,000-$8,000** |

**Gross margin on hardware**: 60-75% (at scale, BOM drops toward $1,500)

### Software/Service (recurring)
| Tier | Monthly | Includes |
|------|---------|----------|
| Basic | $200/mo | Model updates, cloud sync, email reports |
| Pro | $400/mo | + Mobile app, multi-machine dashboard, API, priority support |
| Enterprise | Custom | + On-prem deployment, custom integrations, SLA |

### Alternative: Pay-Per-Meter
- $0.002 per linear meter inspected (typical mill inspects 500K-2M meters/month)
- Revenue: $1,000-$4,000/month per installation
- Lower barrier to entry; higher LTV for high-volume mills

---

## Ideal First Customer Profile

### Demographics
- **Type**: Woven fabric manufacturer (grey fabric or finished)
- **Size**: 50-200 looms, 200-500 employees
- **Location**: Surat, Tiruppur, or Erode (India) -- dense textile clusters with progressive owners
- **Revenue**: $2M-$10M annually
- **Current QC**: 2-4 human inspectors per shift, catching ~65% of defects
- **Pain**: Recently lost a major export order due to quality issues OR facing buyer pressure to provide inspection certificates

### Psychographics
- Owner/GM is 30-50 years old, second-generation textile family
- Has WhatsApp, uses smartphone for business
- Understands ROI math (speaks in "cost per meter" or "seconds per point")
- Has seen Uster at trade fairs (ITMA, India ITME) but dismissed as too expensive
- Exports to Europe/USA where quality requirements are tightening

### Why They Buy
1. **Immediate ROI**: Reducing defect pass-through from 4% to 1% saves $80K-$200K/year in returns and downgrades
2. **Export qualification**: Many buyers now require automated inspection certificates
3. **Labor cost**: Replacing 2 inspectors ($3K-$6K/year each in India) with 1 operator + machine
4. **Status**: Being "the mill with AI inspection" differentiates them to buyers

### Discovery Signals (how to find them)
- Active on IndiaMart / TradeIndia looking for inspection equipment
- Attending ITMA, India ITME, Texprocess trade shows
- Members of textile associations (SIMA, TEA, PDEXCIL)
- Recently invested in new looms (Picanol, Toyota, Tsudakoma) -- indicates growth mindset
- Posting on LinkedIn about quality certifications or export wins

---

## Success Metrics for v1

| Metric | Target | Measurement |
|--------|--------|-------------|
| Defect detection rate | >90% (vs human ~65%) | Side-by-side test with trained grader |
| False positive rate | <5% | Operator override tracking |
| Fabric speed supported | 30-60 m/min | Mechanical test |
| Setup time | <3 hours | Installation timer |
| Time to value | <1 week | First report generated |
| System uptime | >98% | Edge PC telemetry |
| Payback period for customer | <6 months | Customer ROI worksheet |
