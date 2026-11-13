# Execution Plan: Legacy IC Recovery-as-a-Service

## 5a. Product Definition

**Core value proposition**: Deploy robotic systems at e-waste recycling facilities that extract intact, reusable integrated circuits from circuit boards before shredding — recovering $10-100+ chips that would otherwise be destroyed, and supplying them to the $15B legacy semiconductor aftermarket.

**Key features for MVP (max 3)**:
1. Robotic desoldering cell: computer vision identifies valuable ICs, thermal + suction extracts them intact at 200+ chips/hour
2. Automated testing & grading: electrical functionality verification and quality grading of recovered chips
3. Digital catalog: every recovered chip logged with provenance (board source, extraction conditions, test results) for traceability

**What it does NOT do**:
- Not a full e-waste recycler (we extract chips BEFORE the board goes to standard shredding/smelting)
- Not a semiconductor fab or remanufacturer (we recover existing chips, not make new ones)
- Not a general-purpose pick-and-place robot (specialized for DESOLDERING from populated boards)
- Not testing all chip types (MVP focuses on high-value: DRAM, FPGA, microcontrollers, legacy ASICs)

**Success metrics for prototype validation**:
- Extract 200+ intact ICs per hour from mixed PCB stream
- 80%+ of extracted ICs pass functional testing
- Average recovered chip value > $5 (proving economics work)
- At least 1 e-waste recycler signs deployment contract

---

## 5b. Technical Architecture

**System diagram**:
```
[Mixed PCB Boards] → [Vision System: ID Valuable ICs] → [Thermal Profile Lookup] → [Robotic Desoldering Cell]
                                                                                              ↓
[Graded IC Inventory Database] ← [Functional Tester] ← [Cleaning/Inspection] ← [Extracted ICs]
          ↓
[Marketplace / Customer Orders]
```

**Technology stack**:
- **Computer vision**: YOLO-based IC detection + OCR for part number reading, trained on PCB imagery
- **Thermal database**: Lookup table mapping IC package types to optimal desoldering profiles (temperature, dwell time, ramp rate)
- **Robotic cell**: 6-axis robot arm + infrared preheater + focused hot air/laser for localized desoldering + vacuum pickup
- **Testing**: Custom bed-of-nails test jigs for common IC families + universal IC programmer for functional verification
- **Software**: Inventory management system with provenance tracking, marketplace integration

**Build vs. Buy**:
| Component | Decision | Rationale |
|-----------|----------|-----------|
| Vision system (IC detection) | BUILD | Core IP — training data on PCB images is our moat |
| Thermal profiles database | BUILD | Core IP — knowing exactly how to remove each IC type |
| Robot arm | BUY (Universal Robots UR5e) | Commodity hardware, well-documented API |
| Heating system | BUILD (integrate) | Custom IR preheater + hot air nozzle assembly |
| IC tester | BUY + CUSTOMIZE | Universal programmers exist; need custom test scripts |
| Inventory/marketplace | BUILD | Software is straightforward but provenance tracking is differentiator |

**Key technical risks and mitigation**:
1. **IC damage during extraction**: Mitigate with precise thermal profiling per package type; IR preheater warms board evenly to reduce thermal shock; success metric is 80%+ yield
2. **Vision system accuracy on diverse boards**: Mitigate with large training dataset; start with common board types (servers, networking equipment) before expanding to consumer electronics
3. **Testing throughput bottleneck**: Mitigate by prioritizing high-value ICs for full testing; visual-only inspection for lower-value parts

---

## 5c. Bill of Materials / Resources

### Hardware (per robotic cell)

| Item | Supplier | Cost | Notes |
|------|----------|------|-------|
| Universal Robots UR5e (6-axis) | UR | $35,000 | Collaborative, programmable, precise |
| Machine vision cameras (×2) | Basler/FLIR | $5,000 | High-res for OCR + thermal imaging |
| IR preheater station | Custom/Hakko | $3,000 | Board-level preheating |
| Focused hot air desoldering unit | Custom/Ersa | $5,000 | Component-level heat |
| Vacuum pickup system | Custom pneumatic | $2,000 | Suction extraction |
| Component tray handling | Custom 3D-printed | $1,000 | Sorted storage |
| Workstation PC (GPU for vision) | Dell/HP | $5,000 | RTX 4090 for inference |
| Universal IC programmer | Xeltek SuperPro | $3,000 | Functional testing |
| Bed-of-nails test fixtures | Custom PCB | $5,000 | For common IC families |
| Safety enclosure | Custom | $5,000 | For deployment at recycler sites |
| **Total per cell** | | **~$69,000** | |

### Software Development

| Item | Cost | Notes |
|------|------|-------|
| Training data collection (PCB images) | $10,000 | Crowdsourced labeling + synthetic generation |
| Cloud compute (model training) | $15,000 | GPU instances for YOLO training |
| Inventory system development | $20,000 | Or use open-source ERP + customize |

### Personnel (first 12 months)

| Role | Count | Annual Cost | Notes |
|------|-------|-------------|-------|
| Robotics engineer (lead) | 1 | $170,000 | UR programming, cell design, integration |
| Computer vision / ML engineer | 1 | $175,000 | IC detection, OCR, defect detection |
| Electronics/test engineer | 1 | $150,000 | Desoldering profiles, IC testing protocols |
| Business dev / operations | 1 | $130,000 | Recycler partnerships, customer acquisition |
| Technician | 1 | $70,000 | Prototype assembly, testing, data collection |
| **Total personnel** | 5 | **$695,000** | |

---

## 5d. Build Instructions

### Phase 1: Proof of Concept (Weeks 1-12)

**Step 1**: Build vision system (Weeks 1-6)
- Collect 5000+ labeled PCB images (IC locations, part numbers)
- Train YOLO model for IC detection + OCR pipeline for part number reading
- Validate: 95%+ detection rate on server/networking boards
- **Output**: Working vision system that identifies and reads ICs on boards

**Step 2**: Develop desoldering profiles (Weeks 2-8)
- Catalog top 50 IC package types by volume/value (QFP, BGA, SOIC, etc.)
- Develop thermal profiles for each: preheat temp, peak temp, dwell time
- Test on sacrificial boards: extraction without damage
- **Output**: Thermal profile database covering 80% of high-value ICs encountered

**Step 3**: Integrate robotic cell (Weeks 6-12)
- Mount UR5e with vision camera and desoldering tools
- Program pick-and-place routine: vision → position → preheat → desolder → extract → place
- Run on mixed boards: measure throughput and yield
- **Go/no-go**: 200+ ICs/hour at 80%+ yield?
- **Output**: Working prototype cell

### Phase 2: Testing & Economics (Weeks 12-20)

**Step 4**: Build IC testing capability (Weeks 12-16)
- Develop functional test protocols for top 20 IC families
- Build bed-of-nails fixtures for common packages
- Measure pass rate of extracted ICs
- **Output**: Testing station that verifies IC functionality

**Step 5**: Economic validation (Weeks 16-20)
- Process 1000+ boards, catalog all recovered ICs
- Price each recovered IC against aftermarket pricing (Rochester, UtSource, etc.)
- Calculate: cost of extraction vs. market value of recovered chips
- **Go/no-go**: Average margin > $3/chip after extraction + testing costs?
- **Output**: Validated unit economics proving the business model works

### Phase 3: Deployment (Weeks 18-30)

**Step 6**: Partner with e-waste recycler (Weeks 18-22)
- Approach 5-10 UK/US recyclers with economic data
- Offer revenue-share model: we deploy cell at their site, split recovered chip revenue
- Target: 1 signed partner with 6-month pilot
- **Output**: Deployed cell at customer site

**Step 7**: Optimize and scale (Weeks 22-30)
- Run production at partner site, track metrics
- Expand IC type coverage (consumer electronics, automotive boards)
- Build inventory and list on aftermarket channels
- Design multi-cell configuration for higher throughput
- **Output**: Proven production system, growing inventory, first chip sales

---

## 5e. Validation Plan

**How to test with real users**:
1. Source boards from local e-waste collectors for R&D (easy to obtain)
2. Price-check every recovered IC on aftermarket platforms (Rochester, Utource, eBay)
3. Offer recovered ICs to vintage electronics repair community first (less risk-averse, validates demand)
4. Partner with one recycler for 6-month co-located pilot

**Key hypotheses to test**:
1. Vision system can identify and read ICs reliably on dirty, aged boards (not clean new boards)
2. 80%+ of ICs survive thermal extraction without damage
3. Recovered ICs pass functional testing at rates high enough for economics to work (>60%)
4. E-waste recyclers will host our equipment (we add value without disrupting their workflow)
5. Aftermarket buyers will purchase robotically-recovered (vs. hand-pulled) ICs

**Go/no-go**:
- PROCEED: 200+ ICs/hour, 80%+ extraction yield, >$3 margin/chip, 1 recycler deployment
- PIVOT: If yield is lower, focus only on highest-value ICs (FPGAs, specialty ASICs at $50-500 each)
- KILL: If boards arriving at recyclers have already had valuable ICs stripped manually

---

## 5f. Timeline & Milestones

| Week | Milestone |
|------|-----------|
| 1-6 | Vision system detects + reads ICs at 95%+ on test boards |
| 6-12 | Integrated robotic cell achieves 200+ ICs/hour |
| 12-16 | Testing station validates recovered IC functionality |
| 16-20 | Economics validated: >$3 margin per chip |
| 18-22 | First recycler partner signed and cell deployed |
| 22-30 | Production running, inventory growing, first sales |

---

## 5g. Cost Estimate

| Category | Cost |
|----------|------|
| Personnel (12 months, 5 people) | $695,000 |
| Prototype hardware (2 cells) | $138,000 |
| Training data and ML compute | $25,000 |
| PCB boards for R&D (sourced from recyclers) | $5,000 |
| IC testing equipment | $15,000 |
| Deployment at partner site (installation, logistics) | $20,000 |
| Software development (inventory, marketplace) | $30,000 |
| Legal / IP | $20,000 |
| Travel, conferences (e-waste industry events) | $25,000 |
| Contingency (15%) | $147,000 |
| **Total to first deployed production cell** | **~$1.12M** |

**Monthly burn rate**: ~$75,000

**Funding strategy**:
- Pre-seed ($500K-1M): Build and validate prototype
- Seed ($3-5M): Deploy 10-20 cells at recycler sites, build inventory
- Revenue begins Month 7-8 (chip sales from pilot), scales with cell deployments
- Series A ($10-20M): Scale to 100+ cells, build marketplace, establish brand

**Unit economics at scale**:
- Cost per cell: ~$69K hardware + $30K installation + $20K/year maintenance = ~$120K first year
- Revenue per cell: 200 ICs/hr × 8 hrs × 250 days × 60% sellable × $5 avg value = ~$1.2M/year
- Even at 30% yield and $3/chip: 200 × 8 × 250 × 30% × $3 = $360K/year per cell
- Gross margin per cell: 70%+ after year 1
- Payback period: 3-6 months per cell

**Revenue model**:
- Revenue-share with recyclers (split chip resale revenue 60/40 or 70/30)
- OR cell lease + buyback guarantee (guaranteed minimum recovery value)
- Marketplace commission on chip sales (15-20%)
- Data licensing (catalog of recoverable ICs from different board types)
