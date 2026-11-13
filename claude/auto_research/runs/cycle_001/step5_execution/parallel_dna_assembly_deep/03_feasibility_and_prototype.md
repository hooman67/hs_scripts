# Feasibility & Prototype Plan: Massively Parallel Gene Assembly Platform

## Architecture Overview

```
+-------------------------------------------------------------------+
|                         CUSTOMER LAYER                              |
|  [Web App] -> Sequence Upload -> Design Review -> Order Tracking   |
+-------------------------------------------------------------------+
        |                                              ^
        v                                              |
+-------------------------------------------------------------------+
|                      SOFTWARE PLATFORM                              |
|  [Design Engine]    [Assembly Planner]    [QC Pipeline]            |
|  - Sequence decomp  - Barcode assignment  - Alignment              |
|  - Overlap design   - Pool optimization   - Error calling          |
|  - Codon optim.     - Cross-reactivity    - Coverage stats         |
|                       checking                                      |
+-------------------------------------------------------------------+
        |                                              ^
        v                                              |
+-------------------------------------------------------------------+
|                        WET LAB LAYER                                |
|  [Oligo Ordering] -> [Parallel Assembly] -> [Separation] -> [QC]  |
|  (Twist/IDT)         (Proprietary)          (Barcode-dir.) (NGS)  |
+-------------------------------------------------------------------+
        |                                              ^
        v                                              |
+-------------------------------------------------------------------+
|                      INFRASTRUCTURE                                 |
|  [AWS Cloud]  [Lab Space]  [Liquid Handler]  [Sequencer]           |
+-------------------------------------------------------------------+
```

### Core Technical Workflow

1. **Input**: Customer provides N sequences (1-10 kb each, N = 50-200)
2. **Design**: Software decomposes each sequence into overlapping fragments (~200-500 bp), assigns orthogonal barcodes, generates oligo pool specification
3. **Order**: Oligo pool ordered from Twist (pooled synthesis, 1000-5000 oligos)
4. **Assembly**: Barcode-directed parallel overlap-extension PCR in a single reaction vessel
5. **Separation**: Constructs separated via barcode-directed capture (magnetic beads, affinity pull-down, or size selection)
6. **Error Correction**: Enzymatic error correction (T7 endonuclease I) + computational deconvolution
7. **Verification**: Oxford Nanopore long-read sequencing of all constructs
8. **Output**: Verified DNA constructs shipped to customer with QC report

---

## Bill of Materials

### Lab Equipment (One-Time Capital)

| Item | Supplier | Cost | Confidence | Notes |
|------|----------|------|------------|-------|
| Opentrons OT-2 liquid handler | Opentrons | $15,000 | VERIFIED | Open-source, Python-programmable. Adequate for 50-plex. |
| Opentrons Flex (upgrade path) | Opentrons | $25,000 | VERIFIED | For 200+ plex scale-up |
| Oxford Nanopore MinION | ONT | $1,000 | VERIFIED | Long-read sequencing for full-length construct verification |
| ONT Flow Cells (initial stock, 20x) | ONT | $10,000 | VERIFIED | $500 each, ~50 constructs per flow cell |
| Thermocycler (96-well, gradient) | Bio-Rad C1000 | $8,000 | VERIFIED | For overlap-extension PCR |
| Thermocycler (384-well) | Bio-Rad | $12,000 | ASSUMED | Needed for 200+ plex scale |
| Gel electrophoresis + imaging | Bio-Rad | $3,500 | VERIFIED | Size verification |
| Magnetic bead separator (96-well) | Invitrogen | $2,000 | VERIFIED | For barcode-directed separation |
| Microcentrifuge | Eppendorf | $3,000 | VERIFIED | Standard lab |
| NanoDrop spectrophotometer | Thermo | $5,000 | VERIFIED | DNA quantification |
| PCR workstation (UV sterile) | Various | $3,000 | VERIFIED | Contamination prevention |
| Biosafety cabinet (BSL-1) | Thermo Fisher | $8,000 | VERIFIED | Required for DNA handling |
| -20C freezer (upright) | Various | $3,000 | VERIFIED | Reagent storage |
| -80C freezer | Thermo | $8,000 | VERIFIED | Long-term sample storage |
| Pipettes (multichannel set) | Rainin | $5,000 | VERIFIED | Manual backup |
| Vortexer, heat blocks, misc. | Various | $3,000 | ASSUMED | Standard lab equipment |
| **TOTAL EQUIPMENT** | | **$115,500** | | |

### Recurring Consumables (Per 50-Construct Run)

| Item | Cost | Confidence | Notes |
|------|------|------------|-------|
| Oligo pool (Twist, ~1500 oligos x 200nt avg) | $3,000-4,500 | ASSUMED | Based on Twist pooled pricing ~$0.01/nt for pools |
| High-fidelity polymerase (Q5/KAPA) | $150 | VERIFIED | ~10 reactions worth |
| dNTPs, buffers, water | $50 | VERIFIED | Standard molecular biology |
| Magnetic beads (streptavidin-coated) | $200 | VERIFIED | For barcode capture |
| Biotinylated capture probes (50x) | $500 | ASSUMED | Custom oligos for barcode pull-down |
| Error correction enzymes (T7 endo I) | $100 | VERIFIED | NEB catalog |
| Column purification kits (50x) | $250 | VERIFIED | Qiagen/Zymo |
| Nanopore flow cell (1x) | $500 | VERIFIED | One per run for QC |
| Nanopore library prep kit | $150 | VERIFIED | ONT catalog |
| Tubes, tips, plates | $150 | VERIFIED | Standard consumables |
| Shipping supplies (to customers) | $100 | ASSUMED | Cold-pack shipping |
| **TOTAL PER RUN** | **~$5,150-5,650** | | |

**Cost per construct at 50-plex**: ~$103-113 (consumables only)
**Cost per construct at 200-plex**: ~$40-50 (consumables only, economies of scale on oligo pools)

### Software & Cloud Infrastructure (Monthly)

| Item | Monthly Cost | Confidence | Notes |
|------|-------------|------------|-------|
| AWS (EC2 + S3 + RDS) | $500 | ASSUMED | Design compute + customer data |
| Domain + SSL | $20 | VERIFIED | Standard |
| Benchling (lab LIMS) | $300 | VERIFIED | Sample tracking |
| GitHub Enterprise | $50 | VERIFIED | Code management |
| Monitoring (Datadog/similar) | $100 | ASSUMED | Ops monitoring |
| **TOTAL MONTHLY** | **~$970** | | |

### Personnel (First 12 Months)

| Role | Count | Annual Cost | Confidence | Notes |
|------|-------|-------------|------------|-------|
| Molecular Biologist (co-founder, PhD) | 1 | $150,000 | ASSUMED | Below market; equity-compensated |
| Computational Biologist (PhD) | 1 | $160,000 | VERIFIED | Assembly algorithm development |
| Lab Technician | 1 | $75,000 | VERIFIED | Protocol execution, QC |
| Full-Stack Engineer | 1 | $170,000 | VERIFIED | Customer portal + pipeline |
| CEO / BD (founder) | 1 | $120,000 | ASSUMED | Below market; equity-compensated |
| **TOTAL PERSONNEL** | 5 | **$675,000** | | |

### Facility (Monthly)

| Item | Monthly Cost | Confidence | Notes |
|------|-------------|------------|-------|
| Shared wet lab space (biotech incubator) | $5,000-8,000 | ASSUMED | LabCentral, QB3, BioLabs pricing |
| Utilities included | (included) | ASSUMED | Most incubators bundle |
| BSL-1 certification | (included) | ASSUMED | Standard for DNA work |
| **TOTAL MONTHLY** | **~$6,500** | | |

### Total First-Year Budget

| Category | Cost |
|----------|------|
| Personnel | $675,000 |
| Equipment (one-time) | $115,500 |
| Lab space (12 months) | $78,000 |
| Consumables (R&D: ~25 runs) | $140,000 |
| Consumables (Beta customer runs: ~15 runs) | $85,000 |
| Software/cloud (12 months) | $11,640 |
| IP/Legal (patent filing, biosecurity compliance) | $50,000 |
| Travel/conferences/customer visits | $30,000 |
| Insurance (lab liability) | $15,000 |
| Contingency (15%) | $180,000 |
| **TOTAL YEAR 1** | **~$1,380,000** |

**Monthly burn rate**: ~$100,000 (after equipment purchased)
**Runway needed**: 18 months minimum = $1.8M (includes buffer for delays)
**Recommended raise**: $2.5-3.5M seed (18 months runway + equipment + contingency)

**Confidence: MODERATE** — Equipment costs are well-researched. Personnel costs are Bay Area market rates. Biggest uncertainty is consumables cost per run (oligo pool pricing varies significantly by volume and vendor relationship).

---

## Software Stack

### Design Engine (Core IP)

| Component | Technology | Notes |
|-----------|-----------|-------|
| Sequence decomposition | Python + Biopython | Fragment sequences into overlapping pieces |
| Barcode design | Custom algorithm (Python) | Generate orthogonal barcodes with >5nt Hamming distance |
| Thermodynamic modeling | NUPACK (Python bindings) | Verify no cross-hybridization in pools |
| Codon optimization | Custom + CodonW | Host-organism-aware optimization |
| Assembly path planning | Graph algorithms (NetworkX) | Optimal fragment ordering |
| Cross-reactivity checking | BLAST + custom | Ensure no off-target assembly |

### Customer Platform

| Component | Technology | Notes |
|-----------|-----------|-------|
| Frontend | React + TypeScript | Customer portal |
| Backend API | Python + FastAPI | Order management, design pipeline |
| Database | PostgreSQL | Orders, customers, results |
| File storage | AWS S3 | Sequence files, QC reports |
| Authentication | Auth0 | SSO for enterprise customers |
| Payment | Stripe | Invoicing and payment |
| Hosting | AWS ECS/Fargate | Container-based deployment |

### Lab Operations

| Component | Technology | Notes |
|-----------|-----------|-------|
| LIMS integration | Benchling API | Sample tracking |
| Liquid handler control | Opentrons API (Python) | Automated pipetting protocols |
| Sequencing pipeline | Minimap2 + custom | Alignment and QC |
| Reporting | Python + Jinja2 | Auto-generated QC reports |

---

## Build Instructions (Detailed Phases)

### Phase 0: Team Assembly (Weeks 0-4)

**Critical**: Recruit PhD molecular biologist co-founder.

- Target: Postdoc or early-career scientist with DNA assembly expertise (Gibson, Golden Gate, overlap-extension)
- Sources: MIT Voigt Lab alumni, Stanford Endy Lab alumni, Edinburgh BioFoundry alumni, Caltech alumni
- Compensation: 15-25% equity + $120-150K salary
- **Go/no-go**: If no PhD co-founder recruited by Week 4, pause all other activities

### Phase 1: Chemistry Development (Weeks 4-16)

**Step 1: Barcode System Design (Weeks 4-8)**
- Computationally generate library of 500+ orthogonal DNA barcodes (20-25 nt)
- Constraints: >5 nt Hamming distance, balanced GC content (40-60%), no homopolymers >4, no self-complementarity
- Model thermodynamics with NUPACK to verify no cross-hybridization at assembly temperatures
- Design removable barcode chemistry:
  - Option A: Type IIS restriction enzyme sites (BsaI/BsmBI) flanking barcode
  - Option B: Photocleavable linker (UV-removable)
  - Option C: USER enzyme (uracil-containing barcodes)
- **Output**: Validated barcode library (500+ sequences) + removal chemistry
- **Confidence: HIGH** — Barcode design is computational; well-understood thermodynamics

**Step 2: Single-Construct Assembly Protocol (Weeks 5-9)**
- Establish overlap-extension PCR protocol for 1-5 kb constructs from pooled oligos
- Test polymerases: Q5 (NEB), KAPA HiFi, Phusion
- Optimize: annealing temps, extension times, fragment overlap length (20-40 bp)
- Benchmark: assemble 10 known sequences individually, sequence-verify
- Target: >90% success rate for individual constructs
- **Output**: Optimized single-construct protocol
- **Confidence: HIGH** — Standard molecular biology; well-published protocols exist

**Step 3: 10-Plex Parallel Assembly (Weeks 8-12)**
- Pool 10 barcoded construct inputs into single reaction
- Perform pooled overlap-extension PCR
- Separate constructs via barcode-directed magnetic bead capture
- Sequence all 10 constructs on MinION
- Track: cross-contamination rate, per-construct yield, error rate
- **Go/no-go**: 8/10 correct constructs with <1:10,000 error rate?
- **Output**: Working 10-plex protocol
- **Confidence: MODERATE** — This is where novel chemistry begins; success not guaranteed

**Step 4: 50-Plex Parallel Assembly (Weeks 12-16)**
- Scale pool complexity from 10 to 50
- Optimize PCR conditions for larger pools (may need touchdown PCR, longer extension)
- Address crosstalk issues (likely to emerge at this scale)
- Potential solutions: compartmentalized reactions (droplets), staged assembly, improved barcode separation
- Full NGS verification of all 50 constructs
- **Go/no-go**: 40/50 correct constructs (>80% success rate)?
- **Output**: Working 50-plex protocol = MVP chemistry
- **Confidence: LOW-MODERATE** — Significant technical uncertainty. Cross-reactivity in large pools is the #1 risk.

### Phase 2: Software Platform (Weeks 8-20)

**Step 5: Design Algorithm (Weeks 8-14)**
- Input: FASTA file with N sequences (1-10 kb each)
- Processing:
  1. Decompose each sequence into ~200-500bp overlapping fragments
  2. Assign barcodes from validated library
  3. Check all fragment pairs for cross-reactivity (BLAST)
  4. Optimize fragment boundaries to avoid problematic sequences
  5. Generate oligo pool specification (Twist-compatible format)
- Output: Assembly plan + oligo order file
- Testing: Validate designs computationally against known successful assemblies
- **Confidence: HIGH** — Computational; can be built by the software engineer

**Step 6: Customer Web Portal (Weeks 14-20)**
- Core features:
  - User registration + authentication
  - Sequence upload (FASTA, GenBank, CSV)
  - Automated design pipeline (calls Step 5 algorithm)
  - Assembly plan review + approval
  - Order placement + payment
  - Status tracking dashboard
  - Results download (sequences, QC reports, coverage plots)
- Tech stack: React frontend, FastAPI backend, PostgreSQL, AWS
- **Confidence: HIGH** — Standard web application development

### Phase 3: Beta Launch (Weeks 16-28)

**Step 7: Beta Customer Recruitment (Weeks 16-20)**
- Identify and contact 20+ potential beta customers
- Offer: 50% discount, priority support, influence on product roadmap
- Target: 5 signed beta agreements with funded synbio companies
- Channels: SynBioBeta conference, LinkedIn outreach to strain engineering VPs, academic collaborators
- **Confidence: MODERATE** — Depends on network and timing

**Step 8: Beta Execution (Weeks 20-26)**
- Run 10-15 customer projects through platform
- Track: success rate, turnaround time, customer satisfaction, failure modes
- Iterate on protocol and software based on real-world feedback
- Document all failure modes and develop mitigations
- **Confidence: MODERATE** — Depends on chemistry working reliably

**Step 9: Commercial Optimization (Weeks 24-28)**
- Reduce cost per construct (optimize oligo utilization, pool sizes)
- Improve turnaround time (parallelize steps, streamline QC)
- Automate liquid handling (reduce manual steps)
- Finalize pricing and SLA terms
- Launch commercial service
- **Confidence: HIGH** — Optimization of working system

---

## Risk Register

| # | Risk | Probability | Impact | Mitigation | Residual Risk |
|---|------|------------|--------|------------|---------------|
| 1 | Cross-reactivity in 50+ plex pools makes assembly unreliable | 35% | CRITICAL | Compartmentalized reactions (droplets); staged assembly in groups of 10; improved barcode design | Could reduce to 20-plex service (smaller market) |
| 2 | Twist launches competing parallel assembly product | 30% | HIGH | Speed to market; build data/software moat; target underserved segments | Become niche player or acquisition target |
| 3 | Cannot recruit PhD molecular biologist co-founder | 25% | CRITICAL | Offer generous equity; target frustrated postdocs; consider CTO-for-hire initially | Cannot proceed without; would kill project |
| 4 | Unit economics require pricing above market willingness | 20% | HIGH | Reduce COGS through volume oligo contracts; optimize yield; target premium customers first | Margin compression; may need instrument model earlier |
| 5 | Regulatory/biosecurity screening delays exceed 5 days | 15% | MODERATE | Automate screening; pre-screen common sequences; build relationship with IGSC | Adds 2-3 days to turnaround; price into SLA |
| 6 | Oligo pool quality from suppliers is insufficient | 15% | MODERATE | Dual-source (Twist + IDT); QC incoming oligos; build error-correction redundancy | Adds cost and time per run |
| 7 | Customer demand insufficient (market too early) | 15% | HIGH | Extensive customer discovery pre-build; pivot to lower-plex if needed | Reduce burn; focus on 10-20 plex market first |
| 8 | IP conflict with existing patents (Genyro/Caltech) | 20% | HIGH | FTO analysis early (Week 1-4); design around known patents; file own patents | May need to license or develop alternative chemistry |
| 9 | Lab contamination / reproducibility issues | 20% | MODERATE | Strict SOPs; dedicated PCR workstation; positive/negative controls every run | Standard biotech mitigation; adds cost |
| 10 | Key person risk (small team) | 30% | MODERATE | Document all protocols; cross-train team; use Benchling for lab documentation | Inherent to early-stage; accept risk |

---

## Validation Plan

### Technical Validation Milestones

| Milestone | Success Criteria | Timeline | Confidence |
|-----------|-----------------|----------|------------|
| Barcode library validated | 500+ orthogonal barcodes, <1% cross-hybridization in silico | Week 8 | HIGH |
| Single-construct assembly | 9/10 correct, <1:10K error rate | Week 9 | HIGH |
| 10-plex demonstrated | 8/10 correct, <1:10K error rate | Week 12 | MODERATE |
| 50-plex demonstrated | 40/50 correct, <1:10K error rate | Week 16 | LOW-MODERATE |
| Customer construct success | >80% first-pass success rate across 5+ customers | Week 26 | LOW |

### Customer Validation Milestones

| Milestone | Success Criteria | Timeline |
|-----------|-----------------|----------|
| 5 LOIs from beta customers | Signed letters of intent with budget commitment | Week 18 |
| 3 beta orders completed | Constructs delivered, customers satisfied (NPS >40) | Week 24 |
| First repeat order | A beta customer places a second paid order | Week 26 |
| 10 commercial customers | Paying full price, generating >$50K/mo revenue | Week 40 |

### Kill Criteria (When to Stop)

1. **Week 12**: If 10-plex assembly achieves <50% success rate after 3 optimization attempts -> KILL
2. **Week 16**: If 50-plex assembly achieves <60% success rate -> PIVOT to 20-plex service
3. **Week 20**: If <3 beta customers sign up despite outreach to 30+ prospects -> KILL (no market demand)
4. **Week 26**: If COGS per construct >$200 at 50-plex -> PIVOT to premium pricing or instrument model
5. **Any time**: If Twist announces a directly competing product -> Evaluate acquisition vs. differentiation

---

## Cost & Time Estimate Summary

| Scenario | Timeline | Capital Required | Key Assumption |
|----------|----------|------------------|----------------|
| Optimistic | 6 months to beta revenue | $1.2M | Chemistry works at 50-plex on first approach |
| Base case | 9 months to beta revenue | $1.8M | One major pivot in chemistry (e.g., reduce to 30-plex, then scale) |
| Pessimistic | 14 months to beta revenue | $3.0M | Multiple chemistry iterations needed; team expansion required |
| Failure | 6 months (kill) | $600K | Chemistry cannot scale past 10-plex |

**Recommended funding**: $2.5-3.5M seed round to cover base case + 6 months buffer.

---

## Founder-Market Fit Assessment

**Founder profile**: AI/ML infrastructure engineer with deep Python/systems/cloud expertise. No wet-lab/hardware background.

### Fit Analysis

| Dimension | Score (1-10) | Assessment |
|-----------|-------------|------------|
| Technical domain expertise | 2/10 | No molecular biology, wet-lab, or biotech experience. Cannot develop core chemistry independently. |
| Software/platform capability | 9/10 | Excellent. Can build the design engine, customer portal, and data pipeline single-handedly. |
| Industry network | 2/10 | No existing connections to synbio companies, biotech investors, or molecular biology academics. |
| Fundraising capability | 4/10 | Strong technical background helps, but biotech investors want domain expertise on the team. |
| Operational readiness | 5/10 | Can run a company, but lab operations require domain-specific knowledge. |
| Speed of learning | 7/10 | Strong technical foundation suggests ability to learn, but molecular biology has a steep experiential curve. |

### Critical Gaps

1. **Cannot build core product alone**: The assembly chemistry IS the product. A software founder cannot develop, optimize, or troubleshoot wet-lab protocols. This is not something that can be learned from YouTube.

2. **No industry credibility**: Biotech buyers (VP Strain Engineering at Ginkgo) will not trust a DNA assembly platform built by someone with no molecular biology credentials. The domain requires PhDs.

3. **No network for hiring**: Finding and evaluating molecular biology talent requires knowing the field. Who are the top 50 DNA assembly experts? Which labs produce the best talent? A software founder cannot assess this.

4. **Investor skepticism**: Biotech VCs (a16z Bio, Arch Venture, DCVC Bio) want founding teams with domain expertise. A software-only founder will struggle to raise $2.5M+ for a wet-lab startup.

### What This Founder CAN Contribute

- **Software platform**: Build the entire design engine, customer portal, and data pipeline
- **Cloud infrastructure**: Deploy and scale the computational components
- **Automation mindset**: Apply software engineering discipline to lab operations
- **AI/ML integration**: Build the ML feedback loop that improves assembly design over time

### Required Co-Founder Profile

**Must have**: PhD in molecular biology, biochemistry, or bioengineering with hands-on DNA assembly experience (Gibson, Golden Gate, or overlap-extension PCR). 3+ years post-PhD in a synbio company or academic foundry. Publications in ACS Synthetic Biology or similar.

**Ideal**: Led a team doing high-throughput construct building at a foundry (Ginkgo, Zymergen, Amyris) or academic equivalent (MIT BioFoundry, Edinburgh). Has hit the assembly bottleneck personally and is frustrated enough to solve it.

**Where to find them**:
- MIT Voigt Lab / Synthetic Biology Center alumni
- Stanford Bioengineering (Endy Lab, Smolke Lab)
- Caltech (Murray Lab, where Genyro IP originated)
- Ginkgo Bioworks (many frustrated scientists after layoffs)
- Edinburgh BioFoundry alumni
- Joint BioEnergy Institute (JBEI) alumni

### Overall Founder-Market Fit: 3/10

**Honest assessment**: This is a poor founder-market fit for a solo founder. The idea requires deep wet-lab expertise that cannot be acquired quickly. However, it becomes a 6-7/10 fit WITH the right PhD co-founder — the software/AI/platform capabilities become genuinely valuable as one half of a complementary founding team.

**Recommendation**: Do not pursue this idea unless a PhD co-founder is recruited first. The co-founder search should be treated as the first and most important milestone, with a 4-week deadline. If no co-founder is found, this idea should be shelved in favor of software-native opportunities.
