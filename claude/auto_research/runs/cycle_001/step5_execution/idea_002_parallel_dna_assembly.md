# Execution Plan: Massively Parallel Gene Assembly Platform

## 5a. Product Definition

**Core value proposition**: Reduce DNA construct assembly from weeks to hours by building hundreds of gene-length sequences simultaneously in a single reaction — enabling synthetic biology projects that are currently too slow and expensive.

**Key features for MVP (max 3)**:
1. Parallel assembly of 50+ gene-length DNA constructs (1-10 kb each) in a single run
2. Cloud-based design software that takes sequences in, outputs optimized assembly plans
3. Error rate < 1 in 10,000 bases (verified by NGS sequencing included in service)

**What it does NOT do**:
- Not oligo synthesis (we buy oligos from Twist/IDT as input)
- Not genome assembly (MVP is gene-scale: 1-10 kb, not 100kb+ chromosomes)
- Not cloning/transformation (we deliver verified linear DNA constructs)
- Not protein expression (downstream of our product)

**Success metrics for prototype validation**:
- Successfully assemble 50+ correct constructs simultaneously from pooled oligos
- Error rate verified at < 1:10,000 by NGS
- Turnaround time from oligo input to verified DNA: < 72 hours
- At least 3 paying beta customers generating $50K+ in service revenue

---

## 5b. Technical Architecture

**System diagram**:
```
[Customer Sequences] → [Design Software (PyWinder-like)] → [Oligo Pool Order (Twist/IDT)]
                                                                      ↓
[Verified DNA Constructs] ← [NGS QC] ← [Error Correction] ← [Parallel Assembly Reaction] ← [Oligos Arrive]
        ↓
[Ship to Customer]
```

**Technology stack**:
- **Assembly chemistry**: Overlap-extension PCR with addressable barcode-directed ordering — proprietary approach distinct from Genyro's 3-Way Junction method
- **Design software**: Python-based computational pipeline for:
  - Sequence decomposition into overlapping fragments
  - Barcode design (orthogonal, removable via restriction enzymes or photocleavage)
  - Assembly plan optimization (minimize cross-reactivity, maximize parallelism)
- **Liquid handling**: Microfluidic droplet system OR acoustic liquid handler for picoliter-scale reactions
- **Sequencing QC**: Oxford Nanopore MinION for rapid long-read verification
- **Cloud platform**: AWS-hosted web app for customer order submission and tracking

**Build vs. Buy decisions**:
| Component | Decision | Rationale |
|-----------|----------|-----------|
| Assembly chemistry & protocol | BUILD | Core IP — the parallel assembly method is the differentiator |
| Design/optimization software | BUILD | Core IP — computational design of orthogonal barcodes is key |
| Oligo synthesis | BUY | Commodity input; Twist/IDT at ~$0.05-0.10/base |
| Liquid handling hardware | BUY (customize) | Use Opentrons OT-2 ($15K) or Beckman Echo ($200K) depending on scale |
| Sequencing QC | BUY | Oxford Nanopore MinION ($1K device, $500/flow cell) |
| Cloud infrastructure | BUY | AWS standard |
| Lab space | LEASE | Wet lab space (incubator or shared lab) |

**Key technical risks and mitigation**:
1. **Cross-reactivity in pooled assembly**: Mitigate with computational barcode design ensuring >5 nt Hamming distance between all barcode pairs; validate with small pools (10 constructs) first
2. **Error accumulation at gene scale**: Mitigate with enzymatic error correction (T7 endonuclease I) + design redundancy (multiple assembly paths per construct)
3. **Scaling from 10 → 50 → 320 parallel constructs**: Mitigate with systematic increase in pool complexity, tracking failure modes at each scale

---

## 5c. Bill of Materials / Resources

### Lab Equipment (one-time)

| Item | Supplier | Cost | Notes |
|------|----------|------|-------|
| Opentrons OT-2 liquid handler | Opentrons | $15,000 | Open-source, programmable |
| Oxford Nanopore MinION | ONT | $1,000 | Long-read sequencing for QC |
| Thermocycler (96-well) | Bio-Rad | $8,000 | For overlap-extension PCR |
| Gel electrophoresis system | Bio-Rad | $2,000 | Size verification |
| Microcentrifuge | Eppendorf | $3,000 | Standard |
| Pipettes & consumables starter kit | Various | $5,000 | |
| Biosafety cabinet (BSL-1) | Thermo Fisher | $8,000 | Required for DNA handling |
| -20°C / -80°C freezers | Various | $10,000 | Reagent and sample storage |
| PCR workstation (UV sterilization) | Various | $3,000 | Contamination prevention |
| **Total equipment** | | **~$55,000** | |

### Recurring Consumables (per 50-construct run)

| Item | Cost | Notes |
|------|------|-------|
| Oligo pool (Twist, 1000 oligos × 200 nt) | $3,000 | Input material |
| PCR reagents (polymerase, dNTPs, buffer) | $200 | High-fidelity polymerase |
| Nanopore flow cell | $500 | For QC sequencing |
| Gel/purification kits | $150 | Column purification |
| Tubes, tips, plates | $100 | Standard consumables |
| **Total per run** | **~$4,000** | |

### Software & Cloud

| Item | Monthly Cost | Notes |
|------|-------------|-------|
| AWS hosting (compute + storage) | $500 | For design software + customer portal |
| Benchling (lab LIMS) | $300 | Sample tracking |
| GitHub/CI (private repos) | $50 | Code management |
| **Total monthly** | **~$850** | |

### Personnel (first 12 months)

| Role | Count | Annual Cost | Notes |
|------|-------|-------------|-------|
| Molecular biologist (lead, PhD) | 1 | $150,000 | DNA assembly expertise, protocol development |
| Computational biologist | 1 | $160,000 | Barcode design, assembly optimization algorithms |
| Lab technician | 1 | $70,000 | Run protocols, handle samples, QC |
| Software engineer (full-stack) | 1 | $170,000 | Customer portal, order management, cloud pipeline |
| CEO/business development | 1 | $130,000 | Customers, fundraising, operations |
| **Total personnel** | 5 | **$680,000** | |

---

## 5d. Build Instructions

### Phase 1: Chemistry Development (Weeks 1-12)

**Step 1**: Design barcode system (Weeks 1-4)
- Computationally generate library of 500+ orthogonal barcodes (20-25 nt)
- Verify no cross-hybridization via thermodynamic modeling (NUPACK)
- Design cleavable linker chemistry (restriction site or photocleavable)
- **Skills**: Computational biology, nucleic acid thermodynamics
- **Output**: Validated barcode library + removal chemistry design

**Step 2**: Develop single-construct assembly protocol (Weeks 2-6)
- Validate overlap-extension PCR assembly for 1-5 kb constructs
- Optimize polymerase selection (Q5, Phusion, KAPA HiFi)
- Establish error correction step (T7 endo I + Hi-Fi assembly)
- Benchmark: assemble 10 known sequences individually
- **Skills**: Molecular biology, PCR optimization
- **Output**: Optimized single-construct assembly protocol with known error rate

**Step 3**: Scale to 10-parallel assembly (Weeks 5-8)
- Pool 10 barcode-addressed construct inputs
- Perform pooled overlap-extension PCR
- Separate constructs via barcode-directed capture
- Verify all 10 by Nanopore sequencing
- **Go/no-go**: 8/10 correct at < 1:10,000 error rate?
- **Output**: Working 10-plex parallel assembly

**Step 4**: Scale to 50-parallel assembly (Weeks 8-12)
- Expand pool complexity
- Optimize PCR conditions for larger pools
- Address crosstalk issues (if any)
- Full sequencing verification
- **Go/no-go**: 40/50 correct at < 1:10,000 error rate?
- **Output**: Working 50-plex parallel assembly = MVP chemistry

### Phase 2: Software Platform (Weeks 4-16)

**Step 5**: Build design algorithm (Weeks 4-10)
- Input: FASTA file of N sequences
- Output: Optimized oligo pool design + assembly instructions
- Key features: fragment decomposition, overlap optimization, barcode assignment, cross-reactivity checking
- **Skills**: Algorithms, bioinformatics, Python
- **Output**: Command-line tool that converts sequences → oligo order

**Step 6**: Build customer web portal (Weeks 10-16)
- Sequence upload (FASTA, GenBank)
- Automated design pipeline (calls Step 5 tool)
- Order tracking dashboard
- Results delivery (download verified sequences)
- Payment processing
- **Skills**: Full-stack web development (React + Python/FastAPI + AWS)
- **Output**: Web app at beta.company.com

### Phase 3: Service Launch (Weeks 12-24)

**Step 7**: Beta customer recruitment (Weeks 12-16)
- Reach out to 20+ synbio labs (academic and commercial)
- Offer 50% discount for beta access + feedback
- Target: 5 beta customers with real projects
- **Skills**: Business development, synbio network
- **Output**: 5 signed beta agreements

**Step 8**: Execute beta orders (Weeks 16-22)
- Run customer constructs through platform
- Measure turnaround time, success rate, customer satisfaction
- Iterate on protocol and software based on feedback
- Document failure modes and fixes
- **Output**: Track record of successful deliveries

**Step 9**: Production optimization (Weeks 20-24)
- Reduce cost per construct (optimize oligo utilization)
- Improve turnaround time (target 48-72 hours)
- Automate liquid handling steps
- Prepare for commercial launch
- **Output**: Production-ready protocol and pricing model

---

## 5e. Validation Plan

**How to test with real users**:
1. Partner with 3-5 synthetic biology companies as design partners during chemistry development
2. Run their actual research constructs through the platform (free → beta pricing → full pricing)
3. Compare our turnaround and success rate to their existing gene synthesis vendor (Twist, GenScript)

**Minimum sample size**: 
- 100+ constructs assembled across 5+ customers
- 3+ repeat customers placing second orders

**Key hypotheses to test**:
1. **Technical**: 50+ parallel assembly works reliably (>80% success rate per construct)
2. **Speed**: 48-72 hour turnaround vs. 2-4 weeks from gene synthesis vendors
3. **Demand**: Customers have enough constructs to benefit from parallelism (most synbio projects need 10-100+ variants)
4. **Price**: Customers will pay $50-200 per construct (vs. $200-500 at gene synthesis vendors for individual genes)

**Go/no-go criteria**:
- PROCEED: >80% construct success rate, 3+ repeat paying customers, <72hr turnaround achieved
- PIVOT: If success rate <80% at 50-plex, reduce to 20-plex and focus on speed advantage
- KILL: If chemistry fundamentally can't scale past 10-plex reliably, or no customer demand for parallel assembly

---

## 5f. Timeline & Milestones

| Week | Milestone | Decision Point |
|------|-----------|---------------|
| 1-4 | Barcode library designed + validated computationally | Orthogonality confirmed in silico? |
| 5-6 | Single-construct assembly working at <1:10K error | Chemistry validated? |
| 7-8 | 10-plex parallel assembly demonstrated | 8/10+ correct? |
| 9-12 | 50-plex parallel assembly demonstrated | 40/50+ correct? **KEY GATE** |
| 13-16 | Customer portal beta deployed, beta customers signed | Demand validated? |
| 17-22 | Beta orders executed, feedback collected | >80% success rate? Customers happy? |
| 23-24 | Commercial launch, pricing published | Revenue starting? |
| 25-36 | Scale to 100-plex, hire, grow revenue | $500K+ ARR achievable? |
| 37-52 | Series A fundraise, scale team and throughput | Path to $5M ARR clear? |

---

## 5g. Cost Estimate

| Category | Cost |
|----------|------|
| Personnel (12 months, 5 people) | $680,000 |
| Lab equipment (one-time) | $55,000 |
| Lab space lease (shared biotech incubator, 12 months) | $60,000 |
| Consumables (R&D phase, ~30 runs) | $120,000 |
| Software development (cloud, tools, licenses) | $25,000 |
| Sequencing costs (QC, ~100 flow cells) | $50,000 |
| IP/legal (patent filing, FTO analysis) | $40,000 |
| Travel, conferences, customer visits | $30,000 |
| Contingency (15%) | $160,000 |
| **Total to commercial launch (12 months)** | **~$1.22M** |

**Monthly burn rate**: ~$85,000

**Funding strategy**:
- Angel/pre-seed ($500K-1M) for Phase 1-2 (chemistry + software)
- Seed ($2-4M) after 50-plex demonstration + beta customers for hiring and scale
- Revenue begins Month 6-8 (beta pricing), meaningful revenue by Month 12
- Series A ($10-15M) at ~$1M ARR for instrument development and commercial scale

**Unit economics at scale**:
- Cost per 50-construct run: ~$4,000 (consumables) + $500 (labor) = $4,500
- Revenue per run: 50 constructs × $100/construct = $5,000
- Gross margin (service model): ~55-60%
- At $5M ARR: ~1,000 runs/year, ~$2.5-3M gross profit
- Instrument model (Year 3+): 70%+ gross margins on consumables subscription

**Revenue model at scale**:
- Service: $50-200 per construct depending on length and complexity
- Platform subscription (Year 2): $50K-200K/year for high-volume users running their own protocols
- Instrument + consumables (Year 3): $200K instrument + $50K/year consumables subscription
