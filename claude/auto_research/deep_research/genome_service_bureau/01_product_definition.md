# 01_product_definition.md — Genome-Scale Engineering Service Bureau

## Problem Statement

No commercial entity today offers a reliable, turnkey service to synthesize verified synthetic DNA constructs at the 50kb-1Mb scale. The current landscape fragments at a hard ceiling:

- **Sub-5kb**: Commoditized (Twist, IDT, GenScript at $0.07-0.09/bp, 2-4 week delivery)
- **5-50kb**: Emerging but unreliable (Ansa just reaching 50kb, GenScript can do limited assembly)
- **50kb-1Mb**: No commercial service bureau exists

Customers who need genome-scale DNA (pharma developing gene therapy vectors, synthetic biology companies building metabolic pathways, government labs engineering organisms for biodefense) are forced to build internal capabilities — hiring 3-5 PhDs, spending 6-18 months troubleshooting hierarchical assembly, with unpredictable timelines and failure rates. This is analogous to every company running its own data center before AWS existed.

**Confidence: HIGH** — validated by the absence of any commercial offering at this scale and the existence of academic consortia (GP-write, Sc2.0) that took years to accomplish what a dedicated service should do in weeks.

## Product Scope v1

**Core offering**: End-to-end genome synthesis service. Customer provides a DNA sequence (50kb-1Mb), receives verified synthetic DNA delivered as purified material (in yeast artificial chromosome, BAC, or linearized format per customer specification).

**Key features (MVP, max 3)**:
1. **Guaranteed delivery**: 50-200kb constructs delivered in 4-8 weeks with sequence verification (long-read sequencing confirmation)
2. **AI-assisted design review**: Automated synthesis feasibility scoring — flag toxic sequences, difficult regions, GC extremes, repetitive elements — with redesign suggestions before construction begins
3. **Hierarchical QC with full data package**: Customer receives Nanopore sequencing data, assembly map, and error correction report at every assembly level

**What v1 does NOT include**:
- No organism engineering or transformation (deliver DNA only)
- No constructs below 50kb (refer to Twist/GenScript)
- No regulatory filing support
- No cell-free systems or protein expression
- No classified/ITAR work in Year 1 (requires facility certification timeline)

**Success metrics for v1**:
- 3+ paying customers with delivered projects
- >95% first-pass assembly success rate at each hierarchical level
- Median delivery time <8 weeks for 100kb construct
- <1 error per 100kb in final delivered sequence
- $500K+ in contracted revenue within 18 months

## User Workflow

```
1. SUBMIT:    Customer uploads sequence (FASTA/GenBank) via secure portal
2. REVIEW:    Design team runs feasibility analysis (24-48h turnaround)
              → Report: complexity score, estimated timeline, price quote, flagged regions
3. APPROVE:   Customer approves quote and assembly strategy (or requests redesign)
4. BUILD:     Hierarchical assembly executes in parallel:
              Level 1: Oligos → 1-3kb fragments (outsourced to Twist/IDT)
              Level 2: Fragments → 10-30kb chunks (Gibson/Golden Gate in-house)
              Level 3: Chunks → 50-100kb segments (yeast TAR cloning)
              Level 4: Segments → complete construct (yeast assembly)
5. VERIFY:    Long-read sequencing (Nanopore) at each level + final verification
6. DELIVER:   Purified DNA shipped (dry ice) + full QC data package
7. SUPPORT:   30-day post-delivery support for downstream use questions
```

**Customer portal features**: Real-time project tracking (which assembly level is active), automated notifications at each QC checkpoint, secure sequence handling (SOC 2 compliant).

## Pricing Model

| Construct Size | Price/kb | Typical Project | Timeline |
|---|---|---|---|
| 50-100kb | $300-500/kb | $15K-50K | 4-6 weeks |
| 100-300kb | $200-400/kb | $20K-120K | 6-10 weeks |
| 300kb-1Mb | $150-300/kb | $45K-300K | 10-16 weeks |

**Pricing adjustments**:
- +50% for high-complexity sequences (extreme GC, long repeats >1kb, toxic in standard hosts)
- -20% for repeat customers or multi-project contracts
- Pilot pricing (first 6 months): 50% discount to attract design partners

**Comparison**: At $200-500/kb for genome-scale, this is 20-50x the per-bp cost of gene-scale synthesis ($0.07-0.09/bp at Twist). The premium is justified by:
- Assembly complexity (hierarchical multi-level process)
- Verification burden (entire construct must be contiguous and error-free)
- Speed premium (weeks vs. 6-18 months internally)
- Risk transfer (customer pays only on successful delivery)

**Confidence: MEDIUM** — Pricing is based on academic project cost estimates and analogies to other high-value CRO services. No commercial precedent at this exact scale to validate willingness-to-pay.

## Ideal First Customer

**Profile: Mid-size gene therapy company (100-500 employees, Series C+)**

**Why they are ideal**:
1. **Acute need**: Developing large gene therapy vectors (AAV payloads with complex regulatory elements, 50-150kb constructs for integration) — too large for Twist/IDT, too specialized to build in-house efficiently
2. **Budget**: Gene therapy programs have $10-50M budgets; a $50-100K synthesis project is a rounding error vs. 6 months of internal scientist time
3. **Repeat business**: Multiple vector variants needed for clinical programs (5-20 constructs per program)
4. **Time pressure**: Clinical development timelines create urgency — every month of delay costs millions in lost patent life
5. **Referenceable**: Success story in gene therapy validates the service for entire pharma sector

**Specific target companies** (Confidence: MEDIUM-HIGH):
- Bluebird Bio (gene therapy, needs large constructs)
- Intellia Therapeutics (CRISPR-based, complex donor templates)
- Generation Bio (non-viral gene therapy, large payloads)
- Sarepta Therapeutics (gene therapy for muscular dystrophy)
- Beam Therapeutics (base editing, complex multi-component constructs)

**Secondary customer segments**:
- Synthetic biology companies (Ginkgo customers who need pre-built genomes before using Ginkgo's foundry)
- DARPA/BARDA-funded academic labs (biodefense programs)
- Agricultural biotech (pathway engineering for crop improvement)
