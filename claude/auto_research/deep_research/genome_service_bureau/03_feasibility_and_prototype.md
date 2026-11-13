# 03_feasibility_and_prototype.md — Genome-Scale Engineering Service Bureau

## Architecture

### System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                    CUSTOMER INTERFACE LAYER                       │
│  Secure Portal → Sequence Upload → Design Review → Project Track │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                    DESIGN & PLANNING ENGINE                       │
│  Feasibility Scoring → Partitioning → Assembly Strategy → Quote  │
│  (Python/ML pipeline, sequence analysis, toxicity prediction)    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                HIERARCHICAL ASSEMBLY PIPELINE                     │
│                                                                   │
│  Level 1: Oligos (200nt) → Fragments (1-3kb)  [Outsource+PCR]  │
│  Level 2: Fragments → Chunks (10-30kb)         [Gibson/GG]       │
│  Level 3: Chunks → Segments (50-100kb)         [Yeast TAR]       │
│  Level 4: Segments → Genome (100kb-1Mb)        [Yeast Assembly]  │
│                                                                   │
│  Each level: Build → Verify (Nanopore) → Error-correct if needed │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                    QC & DELIVERY LAYER                            │
│  Long-read sequencing → Alignment → Error report → Ship DNA      │
└─────────────────────────────────────────────────────────────────┘
```

### Software Architecture
```
┌─────────────────────────────────────────────────┐
│  Customer Portal (React + Next.js)               │
│  - Sequence upload, project dashboard, QC viewer │
└────────────────────────┬────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────┐
│  Backend Services (Python/FastAPI)               │
│  - Project management & workflow orchestration    │
│  - LIMS integration (sample tracking)            │
│  - Billing & invoicing                           │
└────────────────────────┬────────────────────────┘
                         │
┌────────────────────────▼────────────────────────┐
│  Bioinformatics Pipeline (Python/Snakemake)      │
│  - Sequence analysis & feasibility scoring       │
│  - Partitioning algorithm (optimal cut sites)    │
│  - Assembly strategy optimizer                   │
│  - QC: read alignment, variant calling, coverage │
└────────────────────────┬────────────────────────┘
                         │
┌────────────────────────▼────────────────────────┐
│  Lab Automation (Hamilton Venus/Python)           │
│  - Liquid handler protocols                      │
│  - Plate tracking & barcode management           │
│  - Protocol scheduling                           │
└─────────────────────────────────────────────────┘
```

## Bill of Materials

### Lab Equipment (One-Time Capital)

| Item | Supplier | Est. Cost | Confidence | Notes |
|---|---|---|---|---|
| Hamilton STAR liquid handler | Hamilton | $250,000 | VERIFIED (vendor quote range $200-300K) | High-throughput automation, 96/384-well |
| Oxford Nanopore PromethION | ONT | $200,000 | VERIFIED (public pricing) | Long-read verification at each level |
| Thermocyclers x4 | Bio-Rad | $32,000 | VERIFIED ($7-9K each) | Parallel PCR assembly |
| CHEF-DR III PFGE system | Bio-Rad | $25,000 | VERIFIED (list price) | Large DNA size verification |
| Plate reader (Tecan Spark) | Tecan | $40,000 | ASSUMED (range $30-60K) | Colony screening, OD measurement |
| Electroporator (Gene Pulser) | Bio-Rad | $8,000 | VERIFIED | Yeast/bacteria transformation |
| Shaker incubators x4 | Infors/Eppendorf | $60,000 | ASSUMED ($12-18K each) | Yeast culture growth |
| -80C freezers x2 | Thermo Fisher | $20,000 | VERIFIED ($8-12K each) | Sample/strain storage |
| Biosafety cabinets x2 | Thermo Fisher | $16,000 | VERIFIED ($6-10K each) | Sterile work |
| Gel documentation system | Bio-Rad | $15,000 | VERIFIED | Size confirmation |
| PCR workstations x2 | AirClean | $6,000 | VERIFIED | Contamination prevention |
| General lab setup | Various | $30,000 | ASSUMED | Benches, centrifuges, pipettes, small equipment |
| **TOTAL EQUIPMENT** | | **~$702,000** | | |

### Facility

| Item | Est. Cost/yr | Confidence | Notes |
|---|---|---|---|
| Lab space (2000 sq ft, biotech incubator) | $120,000 | ASSUMED (varies wildly by market: $60/sqft Bay Area, $40/sqft Boston/RTP) | BSL-1/2 rated, HVAC, waste handling |
| Utilities, maintenance | $24,000 | ASSUMED | Included in some incubators |
| IT infrastructure | $18,000 | ASSUMED | Servers, network, security |
| **TOTAL FACILITY (Year 1)** | **~$162,000** | | |

### Personnel (First 18 Months)

| Role | Count | Annual Salary | Total 18mo | Confidence |
|---|---|---|---|---|
| CSO (PhD, genome synthesis exp.) | 1 | $200,000 | $300,000 | VERIFIED (Glassdoor range $180-250K) |
| Sr. Molecular Biologists | 2 | $160,000 each | $480,000 | VERIFIED |
| Computational Biologist | 1 | $170,000 | $255,000 | VERIFIED |
| Automation Engineer | 1 | $140,000 | $210,000 | ASSUMED |
| Lab Technicians | 2 | $70,000 each | $210,000 | VERIFIED |
| CEO / BD | 1 | $150,000 | $225,000 | ASSUMED (founder salary) |
| **TOTAL PERSONNEL (18mo)** | **8** | | **$1,680,000** | |

### Recurring Costs (Per 100kb Genome Project)

| Item | Cost | Confidence |
|---|---|---|
| Oligo/fragment orders (Twist/IDT) | $15,000 | VERIFIED (at current Twist pricing) |
| PCR/assembly reagents | $3,000 | ASSUMED |
| Yeast media & consumables | $1,000 | ASSUMED |
| Nanopore flow cells (5x) | $2,500 | VERIFIED ($450-500/flow cell) |
| Plasticware, tips | $500 | ASSUMED |
| **TOTAL per 100kb project** | **~$22,000** | |

### Total 18-Month Budget

| Category | Cost |
|---|---|
| Personnel | $1,680,000 |
| Equipment | $702,000 |
| Facility (18mo) | $243,000 |
| Consumables (R&D + 5 projects) | $200,000 |
| Oligo orders | $100,000 |
| Sequencing | $50,000 |
| Legal/IP/compliance | $60,000 |
| Software development | $30,000 |
| BD/conferences/travel | $50,000 |
| Contingency (15%) | $467,000 |
| **TOTAL** | **~$3.6M** |

## Software Stack

| Layer | Technology | Rationale |
|---|---|---|
| Customer portal | React + Next.js, deployed on Vercel/AWS | Standard web stack, fast iteration |
| Backend API | Python + FastAPI | Bioinformatics ecosystem is Python-native |
| Workflow engine | Snakemake or Nextflow | Standard bioinformatics pipeline orchestration |
| LIMS | Benchling (or custom lightweight) | Sample tracking, protocol management |
| Bioinformatics | BioPython, minimap2, medaka, custom | Sequence analysis, QC alignment |
| ML/Design | PyTorch (toxicity prediction, feasibility scoring) | Standard ML framework |
| Lab automation | Hamilton Venus + Python SDK | Liquid handler programming |
| Database | PostgreSQL + S3 (sequence storage) | Relational + blob storage |
| Deployment | AWS (HIPAA-eligible region) | SOC 2 compliance path |

## Build Instructions (Condensed)

### Phase 1: Capability Building (Months 1-6)
1. **Months 1-3**: Establish Level 1-2 parallel assembly. Order fragments from Twist/IDT, develop in-house Gibson/Golden Gate protocols for 10-30kb chunks. Validate 50+ successful assemblies.
2. **Months 2-4**: Establish Level 3 yeast TAR cloning. Validate assembly of 3-5 chunks into 50-100kb segments. Optimize transformation efficiency.
3. **Months 3-6**: End-to-end pipeline validation. Assemble a known reference (bacteriophage T4 at 169kb or partial synthetic yeast chromosome). Demonstrate <8 week timeline.
4. **Months 1-6 (parallel)**: Build design software — partitioning algorithm, feasibility scoring, assembly plan generation.

### Phase 2: First Customers (Months 6-12)
5. **Months 4-7**: Secure 3 pilot customers at 50% discount. Target gene therapy companies.
6. **Months 7-12**: Execute customer projects. Track metrics obsessively. Iterate on failure modes.

### Phase 3: Scale (Months 12-18)
7. **Months 12-15**: Automate with Hamilton. Develop standard parts library. Reduce timeline to 4-6 weeks.
8. **Months 15-18**: Commercial launch at full pricing. Target 2-3 new projects/month.

## Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Assembly fails above 100kb consistently | MEDIUM | CRITICAL | Multiple host options (yeast, BAC, cell-free); modular delivery option |
| No customers at $200+/kb pricing | MEDIUM | HIGH | Pilot at $100/kb to prove value; target time-constrained programs |
| Key hire (CSO) leaves | LOW | HIGH | Equity incentives; document all protocols; cross-train |
| Twist enters genome-scale market | MEDIUM | HIGH | Move fast; secure government contracts (biosecurity moat); build customer lock-in |
| Regulatory/biosecurity incident | LOW | CRITICAL | Screening software (IGSC standards); secure facility; compliance officer |
| Capital runs out before revenue | MEDIUM | CRITICAL | Tight milestones; bridge funding at Month 12; customer revenue starting Month 8 |
| Sequence toxicity kills all hosts | LOW | MEDIUM | Cell-free assembly fallback; multiple host strains; redesign service |

## Validation Plan

**Hypothesis 1 — Speed**: 100kb construct deliverable in <8 weeks
- Test: Build known reference genome (T4 phage, 169kb) end-to-end
- Success: Verified correct sequence in <8 weeks from order placement
- Go/No-go gate: Month 6

**Hypothesis 2 — Accuracy**: <1 error per 100kb achievable
- Test: Sequence 5+ independent assemblies at >50kb, measure error rate
- Success: Median error rate <10 per Mb (i.e., <1 per 100kb)
- Go/No-go gate: Month 6

**Hypothesis 3 — Demand**: 3+ customers willing to pay >$100/kb
- Test: Outreach to 20+ gene therapy/synbio companies
- Success: 3+ signed LOIs or contracts
- Go/No-go gate: Month 7

**Hypothesis 4 — Repeat business**: Customers have multiple projects
- Test: First 3 customers each have 2+ additional projects in pipeline
- Success: >50% of revenue from repeat customers by Month 18
- Validation: Month 12-18

## Cost & Time Estimate

- **Total capital required**: $3.6M (seed) + $15-25M (Series A at Month 18-24)
- **Time to first revenue**: 8-10 months
- **Time to $1M ARR**: 18-24 months
- **Time to breakeven**: 30-36 months (at ~$3M ARR with 15-person team)
- **Monthly burn rate**: $165K average (growing from $120K to $200K)

## Founder-Market Fit Assessment

**Founder profile**: AI/ML infrastructure engineer, deep Python/systems/cloud, no hardware or wet-lab background.

**Fit: POOR (2/10)**

**Critical gaps**:
1. **No wet-lab experience**: Genome synthesis is fundamentally a molecular biology operation. The founder cannot personally debug failed assemblies, optimize yeast transformation, or troubleshoot toxic sequence issues.
2. **No biotech network**: Customer relationships in pharma/biotech take years to build. No existing relationships with potential customers or key hires.
3. **No regulatory knowledge**: Biosecurity screening, ITAR compliance, and FDA-adjacent work require domain expertise.
4. **No hardware/physical operations experience**: Running a lab with expensive equipment, reagent supply chains, and biological waste is fundamentally different from software infrastructure.

**What the founder CAN contribute**:
- Software/automation layer (design tools, customer portal, bioinformatics pipelines)
- Systems thinking and operational efficiency mindset
- Fundraising capability (technical founder with AI background is attractive to VCs)

**What's required to compensate**:
- **Must hire a world-class CSO as co-founder** (someone from Venter Institute, GP-write, or Ginkgo with hands-on genome assembly experience)
- Must hire experienced BD person with pharma/biotech relationships
- Founder's role would effectively be CTO/COO focused on software, automation, and operations

**Honest assessment**: This is not a founder-market fit play. The founder would be contributing maybe 20% of the critical expertise needed. A better approach would be to find a molecular biologist co-founder who has this as their life's work, with the software/AI founder providing the automation and operational scaling layer.
