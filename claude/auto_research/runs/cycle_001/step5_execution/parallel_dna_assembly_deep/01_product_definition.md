# Product Definition: Massively Parallel Gene Assembly Platform

## Problem Statement

Synthetic biology companies building metabolic pathways, combinatorial strain libraries, or multi-gene circuits face a critical bottleneck: **DNA construct assembly is sequential, slow, and expensive**.

**Current pain:**
- Ordering 50+ genes from Twist/IDT means 50 individual orders, 10-21 day turnaround each
- In-house assembly of multi-gene pathways requires weeks of PhD-level labor per pathway
- Combinatorial library construction (testing 50-200 gene variants) is prohibitively slow — months of elapsed time
- Error rates compound with manual assembly steps, requiring multiple rounds of sequencing and re-work
- No single vendor offers "give us 50 sequences, get back 50 verified constructs" as a turnkey service

**Quantified pain:**
- A metabolic engineering team building a 20-gene pathway currently spends 8-16 weeks and $50K-$150K on gene synthesis + manual assembly + verification
- A pharma team screening 100 antibody gene variants spends $200K+ and 3-4 months
- Every week of delay in strain construction = $50K-$500K in lost project value for Series B+ synbio companies

**Confidence: HIGH** — validated through published literature on synbio workflow bottlenecks (Endy 2024, Cameron 2023) and pricing data from Twist/GenScript catalogs.

---

## Product Scope v1 (MVP)

### What It Does

A cloud-to-bench service that accepts 50+ DNA sequences (1-10 kb each) and delivers verified, assembled DNA constructs in under 2 weeks.

**Three integrated components:**

1. **Cloud Design Platform** — Web application where customers upload sequences (FASTA/GenBank), receive optimized assembly plans, track orders, and download QC reports
2. **Parallel Assembly Engine** — Proprietary wet-lab process that assembles 50+ gene-length constructs simultaneously in a single reaction workflow
3. **NGS Verification Pipeline** — Every construct is sequence-verified before delivery; customers receive full QC reports with accuracy metrics

### What It Does NOT Do (v1)

- Does not synthesize oligos (buys from Twist/IDT as commodity input)
- Does not assemble genomes (max 10 kb per construct in v1; no chromosome-scale)
- Does not do protein expression or downstream characterization
- Does not offer an on-premise instrument (service model only in v1)
- Does not compete on single-gene synthesis (minimum order: 10 constructs)

### Key Specifications (MVP)

| Parameter | Target | Stretch |
|-----------|--------|---------|
| Constructs per run | 50 | 200 |
| Construct length | 1-10 kb | 1-15 kb |
| First-pass success rate | >85% | >95% |
| Error rate (verified) | <1:10,000 bp | <1:50,000 bp |
| Turnaround time | 10-14 days | 5-7 days |
| Minimum order | 10 constructs | 5 constructs |

---

## User Workflow

### Step 1: Design (Customer, 15 minutes)
```
Customer logs into web platform
  -> Uploads FASTA file with 50-200 sequences
  -> Platform validates sequences (checks for toxicity genes, biosecurity screening)
  -> Platform generates optimized assembly plan
  -> Customer reviews plan, selects options (high-fidelity mode, rush delivery)
  -> Customer approves and pays
```

### Step 2: Assembly (Internal, 7-10 days)
```
Order enters production queue
  -> Design software generates oligo pool specifications
  -> Oligo pool ordered from Twist/IDT (2-4 day delivery)
  -> Parallel assembly reaction executed (1-2 days)
  -> Error correction applied (enzymatic + computational)
  -> Constructs separated and individually purified
  -> NGS verification of all constructs (1-2 days)
```

### Step 3: Delivery (Customer, same day)
```
Customer notified of completion
  -> Downloads QC report (per-construct accuracy, coverage plots)
  -> Receives shipped DNA (dried or in solution)
  -> Failed constructs flagged with diagnostic information
  -> Re-synthesis offered for failed constructs at no charge
```

### Step 4: Iterate (Customer, ongoing)
```
Customer reviews results in platform
  -> Can order variants of successful constructs
  -> Historical orders inform future design optimization
  -> Platform learns from assembly outcomes (ML feedback loop)
```

---

## Pricing Model

### Service Pricing (v1)

| Tier | Constructs | Length | Price/Construct | Total Example |
|------|-----------|--------|-----------------|---------------|
| Standard | 10-49 | 1-5 kb | $150 | $1,500 - $7,350 |
| Standard | 10-49 | 5-10 kb | $250 | $2,500 - $12,250 |
| Parallel 50 | 50-99 | 1-5 kb | $100 | $5,000 - $9,900 |
| Parallel 50 | 50-99 | 5-10 kb | $175 | $8,750 - $17,325 |
| Parallel 200 | 100-200 | 1-5 kb | $75 | $7,500 - $15,000 |
| Parallel 200 | 100-200 | 5-10 kb | $125 | $12,500 - $25,000 |

**Rush delivery**: +50% for 5-7 day turnaround (standard is 10-14 days)
**Guarantee**: Free re-synthesis for any construct that fails QC

### Comparison to Alternatives

| Provider | 50 genes x 3kb | Turnaround | Assembly included? |
|----------|----------------|------------|-------------------|
| **Us (Parallel 50)** | **$5,000** | **10-14 days** | **Yes, verified** |
| Twist (individual genes) | $13,500 ($0.09/bp x 3000bp x 50) | 10 days | No, just genes |
| GenScript (gene synthesis) | $18,000-$30,000 | 2-3 weeks | No, just genes |
| In-house (buy genes + assemble) | $13,500 + $15K labor | 6-8 weeks | Manual, unverified |

**Value proposition: 60-70% cheaper than manual approach, 4-6x faster, with guaranteed verification.**

**Confidence: MODERATE** — Pricing assumes cost-per-run of ~$4,000-$5,000 (consumables) at 50-plex. Actual costs unvalidated until chemistry is developed. Margins could be thin if success rate is <85%.

---

## Ideal First Customer Profile

### Primary Beachhead: Series A-C Synthetic Biology Companies

**Demographics:**
- 20-200 employees, $10M-$100M raised
- Located in Boston/Cambridge, SF Bay Area, San Diego, or Research Triangle
- Building metabolic pathways for industrial chemicals, fuels, food ingredients, or therapeutics
- Have a molecular biology team of 5-20 people
- Currently spending $200K-$2M/year on gene synthesis from Twist/IDT/GenScript

**Psychographics:**
- Speed-obsessed — their competitive advantage is design-build-test-learn cycle time
- Comfortable with new vendors if quality is guaranteed
- Frustrated that construct assembly is their #1 bottleneck
- Technical buyers are PhD molecular biologists who understand assembly chemistry

**Specific Company Archetypes:**

1. **Metabolic engineering companies** (Ginkgo partners, Zymergen successors)
   - Need: 50-200 pathway variants per design cycle
   - Example companies: DMC Biotechnologies, Lanzatech, Genomatica

2. **Protein engineering companies** (antibody, enzyme optimization)
   - Need: 100+ gene variants for combinatorial screening
   - Example companies: Absci, Evotec, Codexis

3. **Cell therapy / gene therapy companies**
   - Need: Multiple construct variants for optimization
   - Example companies: Genentech (constructs), Intellia (guide RNA libraries)

4. **Agricultural biotech**
   - Need: Multi-gene trait stacks for crop engineering
   - Example companies: Inari Agriculture, Pairwise, Pivot Bio

### Ideal First Customer (Single Company)

**Profile**: Series B metabolic engineering company, 50-100 employees, building engineered organisms for industrial fermentation. They have a 10-person strain engineering team running 20-50 design-build-test-learn cycles per year. Each cycle requires 30-100 new DNA constructs.

**Why they buy:**
- Currently spending $500K/year on gene synthesis + 2-3 FTE worth of time on manual assembly
- Our service replaces $300K of that spend + frees 1-2 FTE for higher-value work
- 3-4x faster cycle time means they can run 60-150 DBTL cycles/year instead of 20-50
- This acceleration is worth $2-5M in faster time-to-market for their products

**How to reach them:**
- CTO/VP Engineering is the budget holder
- Head of Strain Engineering is the technical champion
- They attend SynBioBeta, SEED, and ASM conferences
- They publish in ACS Synthetic Biology, Nature Biotechnology, Metabolic Engineering

**Confidence: HIGH** — This customer archetype is well-documented in synbio industry reports and clearly experiences the assembly bottleneck.

---

## Success Metrics (12-Month Targets)

| Metric | Month 6 | Month 9 | Month 12 |
|--------|---------|---------|----------|
| Beta customers (paying) | 3 | 5 | 5 |
| Commercial customers | 0 | 3 | 10 |
| Constructs delivered/month | 150 | 400 | 1,000 |
| Monthly revenue | $15K | $50K | $100K |
| First-pass success rate | >80% | >85% | >90% |
| Average turnaround | 14 days | 12 days | 10 days |
| NPS score | >40 | >50 | >60 |
| Repeat order rate | 60% | 70% | 80% |
