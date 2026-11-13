# Execution Plan: Genome-Scale Engineering Service Bureau

## 5a. Product Definition

**Core value proposition**: Build complete synthetic genomes (50 kb – 1 Mb+) in weeks instead of months/years — enabling pharmaceutical companies, synthetic biology firms, and government labs to design custom organisms for therapeutics, agriculture, and industrial biotech.

**Key features for MVP (max 3)**:
1. End-to-end genome synthesis service: customer provides sequence, we deliver verified synthetic DNA (50-200 kb)
2. AI-assisted genome design consultation (codon optimization, regulatory element placement, modular architecture)
3. Guaranteed accuracy: <1 error per 100 kb, verified by long-read sequencing

**What it does NOT do**:
- Not organism assembly/transformation (we deliver DNA, not living cells — customer handles host integration)
- Not small-scale gene synthesis (minimum project size: 50 kb)
- Not gene editing/CRISPR services (we build FROM SCRATCH, not modify existing)
- Not regulatory filing support (we're the build team, not the regulatory team)

**Success metrics for prototype validation**:
- Successfully assemble and verify a 100 kb+ synthetic construct
- Deliver within 8 weeks (vs. 6-12 months industry standard for genome-scale)
- Complete 3+ customer projects with verified sequence accuracy
- Generate $500K+ in contracted revenue within first 18 months

---

## 5b. Technical Architecture

**System diagram**:
```
[Customer Genome Design] → [Design Review & Optimization] → [Hierarchical Assembly Plan]
                                                                       ↓
[Verified Genome DNA] ← [Long-Read QC] ← [Genome Assembly] ← [Chunk Assembly (parallel)] ← [Gene Synthesis (parallel)]
                                                                       ↑
                                              [Error Correction Loop (if needed)]
```

**Hierarchical assembly strategy**:
```
Level 1: Oligos (200 nt) → Fragments (1-3 kb)     [Buy from Twist/IDT + assemble in parallel]
Level 2: Fragments → Chunks (10-30 kb)             [Gibson/Golden Gate assembly, parallel]
Level 3: Chunks → Segments (50-100 kb)             [In-yeast TAR cloning or in-vitro]
Level 4: Segments → Complete Genome (100 kb-1 Mb)  [Yeast assembly or specialized methods]
```

**Technology stack**:
- **Level 1-2**: Same as Idea 002 (parallel gene assembly platform) — our own technology or licensed
- **Level 3**: TAR (Transformation-Associated Recombination) cloning in yeast — proven at scale (Venter Institute used for first synthetic cell)
- **Level 4**: Serial yeast assembly or PEG-mediated fusion — established protocols
- **QC**: Oxford Nanopore PromethION for ultra-long reads (verify entire genome contiguity)
- **Design**: Custom genome design software (partition, modularity checking, synthesis feasibility scoring)
- **Automation**: Hamilton STAR liquid handler for high-throughput assembly

**Build vs. Buy decisions**:
| Component | Decision | Rationale |
|-----------|----------|-----------|
| Parallel gene assembly (Level 1-2) | BUILD (or build Idea 002 first) | Core capability — speed advantage comes from parallel lower levels |
| Yeast assembly (Level 3-4) | BUILD protocols | Published methods exist but need optimization for speed |
| Long-read sequencing QC | BUY (Nanopore) | Commodity; PromethION for throughput |
| Genome design software | BUILD | Differentiator — AI-assisted design reduces iteration cycles |
| Liquid handling | BUY (Hamilton STAR) | Industry standard, programmable |
| Lab infrastructure | LEASE | BSL-1/2 biotech incubator space |

**Key technical risks and mitigation**:
1. **Assembly accuracy drops at scale**: Mitigate with hierarchical approach (each level independently verified before proceeding) + error correction at each level
2. **Toxic sequences kill yeast hosts**: Mitigate with multiple host options (different yeast strains, E. coli BAC, cell-free) + sequence-toxicity prediction in design software
3. **Timeline unpredictability**: Mitigate with parallel paths for difficult segments + modular design that allows partial delivery + redesign of problematic regions

---

## 5c. Bill of Materials / Resources

### Lab Equipment (one-time)

| Item | Supplier | Cost | Notes |
|------|----------|------|-------|
| Hamilton STAR liquid handler | Hamilton | $250,000 | High-throughput automation |
| Oxford Nanopore PromethION | ONT | $200,000 | Long-read genome verification |
| Thermocyclers (×4) | Bio-Rad | $32,000 | Parallel PCR assembly |
| Gel documentation system | Bio-Rad | $15,000 | Size verification |
| Plate reader (absorbance + fluorescence) | Tecan | $40,000 | Colony screening, QC |
| Electroporator | Bio-Rad | $8,000 | Yeast/bacteria transformation |
| Shaker incubators (×4) | Infors | $60,000 | Yeast culture |
| -80°C freezers (×2) | Thermo Fisher | $20,000 | Sample/strain storage |
| Biosafety cabinets (×2) | Thermo Fisher | $16,000 | Sterile work |
| Pulsed-field gel electrophoresis | Bio-Rad CHEF | $25,000 | Large DNA verification |
| PCR workstations (×2) | Various | $6,000 | Contamination prevention |
| General lab supplies setup | Various | $30,000 | Benches, racks, small equipment |
| **Total equipment** | | **~$702,000** | |

### Recurring Costs (per 100 kb genome project)

| Item | Cost | Notes |
|------|------|-------|
| Oligo synthesis (Level 1, ~5000 oligos) | $15,000 | From Twist at $3/oligo |
| PCR/assembly reagents | $3,000 | Polymerases, ligases, buffers |
| Yeast media & consumables | $1,000 | Plates, liquid culture |
| Nanopore sequencing (5 flow cells) | $2,500 | Long-read QC at each level |
| Plasticware, tips, plates | $500 | Standard consumables |
| **Total per 100 kb project** | **~$22,000** | |

### Personnel (first 18 months)

| Role | Count | Annual Cost | Notes |
|------|-------|-------------|-------|
| Chief Scientific Officer (PhD, genome synthesis experience) | 1 | $200,000 | Must have experience at Venter Institute, Ginkgo, or similar |
| Senior molecular biologist | 2 | $320,000 | Yeast genetics, large-construct assembly |
| Computational biologist / bioinformatician | 1 | $170,000 | Genome design software, QC pipelines |
| Automation engineer | 1 | $140,000 | Hamilton programming, protocol automation |
| Lab technicians | 2 | $140,000 | Execute protocols, maintain cultures |
| CEO / business development | 1 | $150,000 | Pharma/biotech relationships, fundraising |
| **Total personnel** | 8 | **$1,120,000** | |

---

## 5d. Build Instructions

### Phase 1: Capability Building (Months 1-6)

**Step 1**: Establish Level 1-2 parallel assembly (Months 1-3)
- Either build Idea 002 (parallel gene assembly) in-house
- OR license existing technology (Genyro if available, or develop alternative)
- Validate: assemble 50+ genes (1-5 kb) in parallel reliably
- **Dependency**: This is the foundation — must work before proceeding
- **Output**: Reliable parallel gene-length assembly capability

**Step 2**: Establish Level 3 chunk assembly (Months 2-4)
- Set up yeast TAR cloning capability
- Validate: assemble 3-5 chunks (20-30 kb each) from gene-length fragments
- Optimize transformation efficiency and screening throughput
- **Skills**: Yeast genetics, molecular biology
- **Output**: Reliable 20-30 kb assembly from verified sub-fragments

**Step 3**: Establish Level 4 genome assembly (Months 3-6)
- Validate: assemble 2-3 chunks into a 50-100 kb construct in yeast
- Develop screening strategy (colony PCR + Nanopore sequencing)
- Characterize error rates and failure modes at each level
- **Go/no-go**: Can we reliably produce a 100 kb verified construct in <6 weeks?
- **Output**: Complete hierarchical assembly pipeline validated end-to-end

**Step 4**: Build genome design software (Months 1-6, parallel)
- Sequence partitioning algorithm (optimal fragment boundaries)
- Synthesis feasibility scoring (GC content, repeats, secondary structure)
- Toxicity prediction (sequences likely to kill host)
- Assembly plan visualization
- **Output**: Internal tool that generates assembly plan from sequence input

### Phase 2: First Projects (Months 6-12)

**Step 5**: Secure first 3 customer projects (Months 4-7)
- Target: pharma gene therapy vectors (50-100 kb), synbio pathway clusters (30-80 kb)
- Offer pilot pricing: $100/kb (vs. eventual $200-500/kb) for first projects
- Require design partnership (customer provides sequence + we collaborate on assembly strategy)
- **Output**: 3 signed contracts, $150-300K total value

**Step 6**: Execute customer projects (Months 7-12)
- Run hierarchical assembly pipeline on real customer sequences
- Track metrics: turnaround time, accuracy, failure rate per level
- Iterate and optimize based on real-world challenges
- Deliver verified synthetic DNA with full QC report
- **Output**: 3 delivered projects, customer testimonials

### Phase 3: Scale & Commercialize (Months 12-18)

**Step 7**: Optimize for speed and cost (Months 12-15)
- Automate screening with Hamilton
- Develop library of pre-assembled "standard parts" for common elements (promoters, terminators, selectable markers)
- Reduce turnaround from 8 weeks to 4-6 weeks for standard projects
- **Output**: Faster, cheaper pipeline

**Step 8**: Commercial launch and growth (Months 15-18)
- Publish capabilities and case studies
- Launch full commercial pricing ($200-500/kb depending on complexity)
- Target 2-3 new projects per month
- Hire additional scientists for throughput
- **Output**: $500K+ contracted revenue, growing pipeline

---

## 5e. Validation Plan

**How to test with real users**:
1. Design partner model: work with 3 pharma/synbio companies on actual projects during capability building
2. Publish benchmark: build a well-known reference genome (e.g., bacteriophage T7 at 40 kb) and share data
3. Present at synthetic biology conferences (SynBioBeta, SEED) to build credibility

**Minimum sample size**:
- 5+ successful genome-scale deliveries (>50 kb each)
- 3+ different customer types (pharma, synbio, academic)
- 1+ project >100 kb delivered with verified accuracy

**Key hypotheses to test**:
1. **Speed**: 4-8 week turnaround for 100 kb is achievable (vs. 6-12 months current)
2. **Accuracy**: <1 error per 100 kb is achievable with hierarchical verification
3. **Demand**: Multiple customers need genome-scale synthesis (not just one-off projects)
4. **Pricing**: $200-500/kb is acceptable for genome-scale (vs. $0.10-0.30/bp for gene-scale at Twist)
5. **Repeat business**: Customers have multiple genome projects (not a one-shot need)

**Go/no-go criteria**:
- PROCEED: 100 kb assembly in <8 weeks demonstrated, 3+ paying customers, $200K+ pipeline
- PIVOT: If speed doesn't differentiate enough, pivot to complexity (assemble "impossible" sequences others reject)
- KILL: If hierarchical assembly can't reliably exceed 50 kb, or zero customer demand at >$100/kb pricing

---

## 5f. Timeline & Milestones

| Month | Milestone | Decision Point |
|-------|-----------|---------------|
| 1-3 | Parallel gene assembly working (Level 1-2) | 50+ genes assembled correctly? |
| 2-4 | Chunk assembly working (Level 3, 20-30 kb) | Reliable yeast TAR? |
| 4-6 | Full pipeline validated (100 kb construct) | **KEY GATE**: End-to-end in <6 weeks? |
| 4-7 | 3 customer projects contracted | Demand validated at pilot pricing? |
| 7-12 | Customer projects delivered | Accuracy + speed confirmed on real projects? |
| 12-15 | Pipeline optimized, automation online | <4 weeks for standard projects? |
| 15-18 | Commercial launch, revenue growing | $500K+ in pipeline? |

---

## 5g. Cost Estimate

| Category | Cost (18 months) |
|----------|-----------------|
| Personnel (8 people, 18 months) | $1,680,000 |
| Lab equipment (one-time) | $702,000 |
| Lab space lease (2000 sq ft biotech incubator) | $180,000 |
| Consumables (R&D + 5 customer projects) | $200,000 |
| Oligo orders (for all projects) | $100,000 |
| Sequencing costs (PromethION flow cells) | $50,000 |
| Software development | $30,000 |
| IP/legal/FTO | $60,000 |
| Conferences, travel, business development | $50,000 |
| Contingency (15%) | $458,000 |
| **Total to commercial operation (18 months)** | **~$3.5M** |

**Monthly burn rate**: ~$165,000 (growing from $120K to $200K as team scales)

**Funding strategy**:
- Seed ($3-5M) from biotech-focused VCs (Andreessen Bio, Playground Global, DCVC)
- Customer revenue starting Month 8-10 (pilot projects at $100/kb)
- Revenue at Month 18: ~$50-100K/month from ongoing projects
- Series A ($15-25M) at Month 18-24 for scale, instrument development, larger team
- Break-even possible at ~$3M ARR with 15-person team

**Unit economics**:
- Cost per 100 kb project (consumables + labor): ~$30,000
- Revenue per 100 kb project: $50,000-100,000 (at $200-500/kb, complexity-dependent)
- Gross margin: 50-70%
- Projects per month (Year 2): 3-5
- Revenue run rate (Year 2): $2-5M ARR

**Revenue model at scale**:
- Project-based genome construction: $200-500/kb (core revenue)
- Design consultation: $10-50K per project (value-add)
- Maintenance/iteration contracts: ongoing strain improvement retainers
- Long-term: platform licensing for internal genome foundries (pharma)
