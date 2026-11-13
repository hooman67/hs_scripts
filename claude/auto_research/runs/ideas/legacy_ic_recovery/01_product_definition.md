# Product Definition: Legacy IC Recovery-as-a-Service

## Problem Statement

Every year, millions of PCBs containing functional legacy ICs are shredded at e-waste recyclers for raw material recovery (gold, copper, palladium). Meanwhile, the $15B+ legacy semiconductor aftermarket suffers from chronic shortages, long lead times (6-18 months for Rochester Electronics re-manufacture), and a 10-15% counterfeit rate on gray market parts. Defense programs, aerospace systems, and industrial automation running 20-40 year lifecycles cannot redesign around a $3 obsolete chip without spending $500K-$5M in requalification.

**The gap**: No one systematically extracts, tests, and authenticates individual ICs from e-waste PCBs before shredding. The technology now exists (computer vision, precision robotics, thermal profiling) to do this at scale.

**Confidence: HIGH** -- The aftermarket shortage is well-documented (ERAI counterfeit reports, GIDEP alerts, DLA obsolescence data).

---

## Product Scope v1

**Core offering**: Robotic desoldering cells deployed at e-waste recycler facilities that identify, extract, test, and catalog legacy ICs from PCBs destined for shredding.

**Key features for MVP (max 3)**:
1. Computer vision IC identification system -- recognizes chip packages, reads markings, cross-references against aftermarket demand database to prioritize high-value extractions
2. Robotic thermal desoldering cell -- 6-axis arm with hot-air/IR rework station end-effector, achieving 200+ chips/hour extraction with <5% thermal damage rate
3. Automated electrical test & authentication station -- functional test, X-ray inspection, provenance documentation meeting AS6171/AS6081 traceability standards

**What it does NOT do (v1)**:
- Does not perform full mil-spec qualification testing (partner with accredited test labs)
- Does not handle BGA/flip-chip packages in v1 (through-hole and SOIC/QFP only initially)
- Does not sell direct to end-users initially (supply to authorized distributors and brokers)
- Does not process boards with hazardous materials beyond standard e-waste (no radioactive/military-classified)

**Success metrics for prototype validation**:
- Extract 200+ ICs/hour sustained throughput from mixed PCB boards
- <5% thermal damage rate (measured by post-extraction electrical test pass rate)
- 95%+ correct IC identification (part number, manufacturer, date code)
- At least 3 LOIs from legacy semiconductor distributors or defense procurement offices
- Unit economics: recovered IC average value >$25, extraction cost <$5/chip

---

## User Workflow

### Workflow 1: E-Waste Recycler (Host Site)

```
1. Recycler diverts PCBs to IC recovery cell instead of shredder
2. Boards loaded onto conveyor/tray system
3. Computer vision scans board, identifies all ICs, checks against demand DB
4. System prioritizes high-value targets (>$20 aftermarket value)
5. Robot arm positions over target IC
6. Thermal profile applied (chip-specific temperature ramp)
7. Vacuum suction extracts chip once solder reflows
8. Chip placed in carrier tray, board continues to shredder
9. Extracted ICs move to test station
10. Tested ICs packaged in ESD trays with full provenance documentation
```

### Workflow 2: Legacy IC Buyer (Procurement Engineer)

```
1. Search online catalog for needed obsolete part number
2. See available quantity, condition grade, provenance data
3. Request authentication package (X-ray, electrical test, board source)
4. Purchase at 30-50% discount vs. Rochester/Lansdale pricing
5. Receive parts with full AS6171-compliant documentation
```

---

## Pricing Model

### Revenue Streams:

1. **Equipment-as-a-Service** (primary): Monthly fee per robotic cell deployed at recycler
   - $15,000-25,000/month per cell (includes maintenance, software updates, demand DB)
   - Recycler pays nothing upfront; revenue share on recovered IC sales
   - **Confidence: ASSUMED** -- modeled on industrial robotics-as-a-service precedents

2. **IC Sales Revenue Share**: 60/40 split (us/recycler) on recovered IC sales
   - Average recovered IC value: $25-$500 (high-mix)
   - Top 5% of recovered ICs: $500-$5,000+ (mil-spec, aerospace)
   - **Confidence: ASSUMED** -- aftermarket pricing from Rochester/ERAI databases

3. **Authentication & Certification Fees**: $15-50 per IC for full AS6171 documentation
   - Required for defense/aerospace buyers
   - **Confidence: HIGH** -- standard industry pricing for authentication services

### Unit Economics Target:
- Cost per IC extracted: <$5 (amortized equipment + labor + consumables)
- Average selling price: $50-100 (blended across demand tiers)
- Gross margin target: 60-70% on IC sales
- Cell payback period: 8-12 months

---

## Ideal First Customer

### Primary: Mid-Size E-Waste Recycler (Host Site)

**Profile**:
- Processing 500-2,000 tons of e-waste/month
- Already sorting PCBs by grade (server boards, telecom boards vs. consumer)
- Has space for a robotic cell (200 sq ft)
- Interested in revenue diversification beyond commodity metal recovery
- Examples: Sims Lifecycle Services, ERI (Electronic Recyclers International), Kuusakoski

**Why they buy**:
- Zero capex (equipment-as-a-service model)
- New revenue stream from boards they currently shred for $2-5/kg
- A single military-grade IC worth $2,000 exceeds the gold value of 100 boards
- ESG/sustainability narrative enhancement

### Secondary: Legacy IC Distributor (Buyer)

**Profile**:
- Authorized aftermarket semiconductor distributor
- Serving defense/aerospace with AS6171-compliant supply chain
- Currently sourcing from gray market with extensive (expensive) incoming inspection
- Examples: Smith & Associates (now Smith+Nephew acquired), Converge (Arrow subsidiary), SourcEngus

**Why they buy**:
- Guaranteed provenance eliminates counterfeit risk
- Lower cost than Rochester re-manufacture ($50 vs. $200+ for same part)
- Faster availability (recovered ICs ship in days vs. 6-18 month re-manufacture lead time)
- Full documentation package reduces their internal inspection costs

---

## Go-to-Market Sequence

1. **Months 1-6**: Deploy first robotic cell at one e-waste recycler (likely Sims or ERI). Focus on telecom and server boards (highest IC density and value).
2. **Months 6-12**: Build catalog of 1,000+ unique recovered/tested part numbers. Sign distribution agreements with 2-3 aftermarket distributors.
3. **Months 12-18**: Deploy cells 2-4 at additional recyclers. Expand to automotive and aerospace board streams.
4. **Months 18-24**: 10+ cells deployed. Launch direct e-commerce for standard industrial buyers. Begin defense/aerospace certification process (QTSL listing).
