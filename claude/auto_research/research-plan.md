# Auto Research: Startup & Product Idea Discovery

## Goal

Find startup or product ideas at the intersection of:
1. **New technology** that's just becoming practical (breakthrough in last 6–18 months)
2. **No existing products** using this tech currently on the market (or only early-stage, pre-product companies)
3. **Large enough market** to support a venture-scale business (TAM > $1B or SAM > $100M)

---

## Execution Model

- **Iterative**: Each cycle discovers 10 candidate technologies in Step 1, then runs them through the full funnel.
- **Persistent**: All results are recorded so subsequent cycles avoid duplicate work and build on prior learnings.
- **Long-running**: Runs inside tmux on the remote machine; survives SSH disconnects.
- **Output**: Each cycle produces a report summarizing promoted ideas and a detailed execution plan for finalists.

---

## Step 1: Technology / Science Advancement Research

**Objective**: Identify 10 recent technologies or scientific findings that are ready (or within 6–12 months of ready) for real-world product implementation.

### Search Strategy
- Academic preprint servers (arXiv, bioRxiv, Nature, Science) for papers with "practical", "real-time", "low-cost", "scalable" in abstracts from the last 12 months
- Patent filings (Google Patents, USPTO) showing implementation-ready claims
- Tech press (TechCrunch, Ars Technica, IEEE Spectrum, MIT Tech Review) for "breakthrough" announcements
- Conference proceedings (NeurIPS, ICML, CES, IEDM, ACM) from last 2 cycles
- Government grants/SBIR awards signaling commercialization readiness
- GitHub trending repos with rapid star growth in novel domains

### Domains to Scan (rotate across cycles)

> **⚠️ WIDER-NET DIRECTIVE (round 3, 2026-07-01).** Rounds 1–2 (40 cycles) converged hard on
> ONE archetype — "AI/software on industrial equipment for underserved mid-market trades"
> (laser, plasma, CNC, welding, HVAC, food processing…). That vein is largely mined (see
> `LEARNINGS.md`: domain exhaustion + moat collapse). This round deliberately explores
> **domains and archetypes we have NOT touched**, to surface genuinely new ideas. Bias Step 1
> AWAY from industrial-QC / shop-floor-sensor ideas unless they carry a real moat. Prefer
> domains with software-native network effects, data moats, or proprietary-data flywheels.

**Under-explored domains to prioritize this round (we barely touched these):**
- **Software-native / digital-only** (no physical world): vertical AI agents, developer tools,
  data/API products, fintech infrastructure, LLM-workflow automation for white-collar niches,
  compliance/audit automation, insurance tech, legal/accounting/HR back-office
- **Consumer & prosumer software** (subscriptions, creator tools, marketplaces) — was almost
  entirely excluded in rounds 1–2; re-examine with a moat lens
- **Healthcare software / digital health** (non-FDA-gated: workflow, billing, scheduling,
  clinical documentation, care coordination) — distinct from device/diagnostics
- **Education & training** (AI tutoring, professional certification, simulation)
- **Climate/energy software** (grid analytics, carbon accounting, VPP orchestration — software,
  not hardware)
- **Robotics & autonomy software layers** (fleet orchestration, teleop, simulation, RL infra)
- **Media/entertainment/generative AI applications** (Hooman's day-job domain — Firefly/genAI)
- **Bio/health data & informatics software** (not wet-lab: multi-omics analysis, trial ops)
- **Trust & safety / provenance / authenticity** (deepfake detection, content provenance, C2PA)

**Legacy domains (rounds 1–2 already covered heavily — deprioritize, don't re-mine):**
- Materials science & manufacturing (metamaterials, bio-fabrication, novel batteries)
- AI/ML on industrial physical systems (shop-floor sensors, machine monitoring) — SATURATED
- Energy & sustainability HARDWARE (carbon capture, grid storage, fusion-adjacent)
- Space tech (smallsat, in-space manufacturing, Earth observation)
- Food & agriculture tech (precision ag, post-harvest, processing) — heavily mined
- Biotech wet-lab / diagnostics / therapeutics (poor founder fit — needs PhDs/labs)

### Promotion Criteria (must meet ALL)
| Criterion | Threshold |
|-----------|-----------|
| Technology Readiness Level (TRL) | ≥ 5 (validated in relevant environment) |
| Time to first product | ≤ 18 months from today |
| Key enabling breakthrough | Clearly identified (cost reduction, miniaturization, accuracy jump, etc.) |
| Reproducibility | Demonstrated by ≥ 2 independent groups OR open-sourced |
| Not purely incremental | Represents a step-change, not a marginal improvement |

### Rejection Reasons (any one disqualifies)
- Still lab-only with no path to scale (TRL < 4)
- Requires regulatory approval > 3 years out (e.g., novel drug, nuclear)
- Fundamental physics/engineering barriers unresolved
- Already well-known and widely covered (e.g., LLMs themselves — too late)

### Output per Technology
- Name and one-line description
- Source (paper/article URL)
- Key breakthrough that makes it practical now
- TRL assessment (1–9)
- Estimated time to productization
- Domain category
- Promotion decision (PROMOTED / REJECTED) with reasoning

---

## Step 2: Competitive Analysis

**Objective**: For each promoted technology from Step 1, determine whether existing products/companies already occupy the space.

### Search Strategy
- Product Hunt, G2, Capterra for existing products using the technology
- Crunchbase, PitchBook for funded startups in the space (seed through Series B)
- Google search: "[technology] startup", "[technology] product", "[technology] company"
- Patent landscape analysis: who holds key IP?
- LinkedIn job postings mentioning the technology (signals company building around it)
- App stores (if consumer-facing)

### ⭐ MANDATORY Incumbent / OEM Check (added round 3 — the #1 lesson from round 2)

**Round 2's fatal recurring error: 14 of 19 "8–9/10, zero-competition" ideas actually had a
funded incumbent or OEM already shipping the core product.** The cycle stage was blind to
them. Before scoring competitive density, you MUST run ALL of these searches and record the
results — a "no competition" verdict is INVALID until every box is checked:

- [ ] **OEM already does it?** Search the equipment/platform maker's own product pages for the
      feature (e.g. Hypertherm SYNC, Atlas Copco SMARTLINK, Samsara API docs). OEMs that own
      the hardware/data are one firmware release away from your product and often give the
      software away free to sell hardware.
- [ ] **Entrenched European / private industrial firm?** Explicitly search German/Swiss/Dutch/
      Scandinavian players (SIKORA, Pixargus, Dr. Schenk, GlassQuality, Precitec, Marposs,
      Fraunhofer spinouts). Invisible on Crunchbase; dominant in niche. Search the trade-show
      exhibitor lists for the industry (e.g. drinktec, FABTECH, wire Düsseldorf).
- [ ] **Funded horizontal platform that lists your vertical?** Search "[problem] AI platform"
      and read their customers page (e.g. Uncountable lists rubber; Aquasight lists WWTP).
- [ ] **Incumbent's own marketing copy = your pitch?** If a competitor already advertises your
      exact value prop ("10–20% savings, no hardware, weeks not months"), the space is taken.
- [ ] **The result "dies" today — is that the whole product?** If the only gap is plumbing data
      that already exists (e.g. XRF grade never reaching inventory), it's an absorbable feature,
      not a company.

**If any box is checked, competitive density is ≥3 (usually 4–5). Do not promote on a
US-startup-search "empty" result.**

### Scoring: Competitive Density Score (1–5)

| Score | Meaning | Decision |
|-------|---------|----------|
| 1 | No companies/products found | **PROMOTE** — wide open |
| 2 | 1–2 very early startups (pre-revenue, < $2M raised) | **PROMOTE** — early enough to compete |
| 3 | 3–5 startups OR 1–2 with significant funding (> $10M) | **BORDERLINE** — promote only if clear differentiation angle exists |
| 4 | Established startups with products in market | **REJECT** — crowded |
| 5 | Big tech or incumbents actively building | **REJECT** — too late |

### ⭐ MANDATORY Moat Gate (added round 3 — round 2's kill dimension)

**Round 2 lesson: the funnel got great at cheap, buildable, well-fit ideas — but moat
collapsed to 2.8/10 avg because cheap+trivial-to-build means anyone (esp. the incumbent) can
copy it. Capital efficiency gets you to the start line; only a moat keeps you in the race.**

Before promoting past Step 2, answer: **"If this works, what stops the OEM / a funded
competitor / a weekend cloner from taking it in 6 months?"** A valid answer is one of:
- **Data / network-effect flywheel** (gets better as it grows, can't be cloned by copying UI —
  this is CutLog's moat, and the ONLY idea in 49 that had a true one)
- **Proprietary data asset** you can uniquely acquire
- **Genuine technical difficulty** you're positioned to solve (but beware: if the hard part is
  hardware/chemistry/sensing, that usually INVERTS this founder's strengths — reject)
- **Regulatory / integration lock-in** that accrues to you, not the incumbent

**"Cheap + trivial to build + no flywheel" = absorbable feature, NOT a company → REJECT even
if every other dimension is a 9.** (PestDoc had the lowest tech-risk of all 49 and is NO-GO
for exactly this reason.)

### Output per Technology
- List of discovered competitors (name, stage, funding, product status)
- Competitive Density Score (1–5)
- Differentiation angles (if any exist despite competition)
- Promotion decision with reasoning

---

## Step 3: Market Analysis

**Objective**: For technologies promoted from Step 2, identify target markets and potential products, then size the opportunity.

### Process
1. **Product ideation**: For each technology, brainstorm 3–5 specific products/solutions it enables
2. **Market identification**: For each product, identify the target customer segment and industry vertical
3. **Market sizing** (TAM/SAM/SOM):
   - **TAM** (Total Addressable Market): Total revenue opportunity if 100% market share
   - **SAM** (Serviceable Addressable Market): Segment you can realistically reach
   - **SOM** (Serviceable Obtainable Market): What you could capture in 3–5 years
4. **Revenue model**: How would the product make money? (SaaS, hardware, marketplace, licensing, etc.)

### Market Sizing Methods
- **Top-down**: Industry reports (Statista, Grand View Research, IBISWorld) → narrow to segment
- **Bottom-up**: Number of potential customers × willingness to pay × purchase frequency
- **Analogous**: Compare to similar products in adjacent markets

### Promotion Criteria
| Criterion | Threshold |
|-----------|-----------|
| TAM | > $1B |
| SAM | > $100M |
| Growth rate | > 15% CAGR |
| Clear buyer persona | Identifiable decision-maker with budget |
| Willingness to pay | Evidence of spending in adjacent solutions |

### Rejection Reasons
- Market too small/niche (SAM < $50M) — **and count the real buyer universe** (round 2: TAB
  had only ~750 firms / ~$9–18M SAM). A countable buyer universe is a red flag, not a green field.
- **Declining or flat market** — ⭐ MANDATORY growth-rate check (round 3). Round 2 promoted
  several shrinking markets that looked "large": dental labs (−1.6%/yr), craft breweries
  (−2.9% in 2025), cabinet shops (−0.6%/yr). Verify CAGR from a real source; reject if flat/
  declining even if absolute size passes. **Trajectory matters more than size** (size is the
  least-discriminating dimension across 49 ideas).
- No clear buyer (technology looking for a problem)
- Regulatory barriers to market entry in most geographies
- **Hidden hard-part check**: if the defensible/valuable part is a sensor, analog circuit, or
  chemistry the founder can't cheaply build (ppb sensing, trace-gas analyzers, wet-lab), the
  software is the commodity and someone else owns the moat → reject for founder-fit.

### Output per Product Idea
- Product name and description
- Target market and customer segment
- TAM / SAM / SOM estimates with methodology
- Revenue model
- Key assumptions and risks
- Promotion decision with reasoning

---

## Step 4: Feasibility Analysis

**Objective**: Validate that promoted product ideas can actually be built with available technology, talent, and capital within a reasonable timeframe.

### Assessment Dimensions

#### 4a. Technical Feasibility
- Can a working prototype be built in < 6 months?
- Are key components commercially available?
- What's the hardest unsolved engineering problem?
- Does it require specialized talent that's extremely scarce?

#### 4b. Economic Feasibility
- Estimated cost to build MVP (target: < $500K)
- Unit economics at scale (gross margin > 50% for software, > 30% for hardware)
- Capital intensity (how much funding needed to reach revenue?)
- Time to revenue (target: < 18 months)

#### 4c. Headwinds & Tailwinds

| Tailwinds (accelerators) | Headwinds (blockers) |
|--------------------------|---------------------|
| Regulatory push (mandates, incentives) | Regulatory barriers |
| Declining component costs | Supply chain risks |
| Cultural/behavioral shifts | Customer inertia / switching costs |
| Platform shifts enabling distribution | Incumbent lock-in |
| Adjacent ecosystem maturity | Missing infrastructure |
| Talent availability improving | Scarce specialized talent |

#### 4d. Risk Assessment
- **Technical risk**: Can we build it? (Low/Medium/High)
- **Market risk**: Will people buy it? (Low/Medium/High)
- **Execution risk**: Can a small team pull it off? (Low/Medium/High)
- **Timing risk**: Is it too early or too late? (Low/Medium/High)

### Promotion Criteria
- No more than ONE dimension rated "High" risk
- At least 2 strong tailwinds identified
- MVP buildable within budget and timeline constraints
- No single-point-of-failure dependencies (one supplier, one regulation, etc.)

### Output per Product Idea
- Technical feasibility assessment
- Economic model (costs, margins, funding needs)
- Headwinds and tailwinds table
- Risk matrix (4 dimensions)
- Overall feasibility score (1–10)
- Promotion decision with reasoning

---

## Step 5: Detailed Execution Plan

**Objective**: For ideas promoted from Step 4, produce a comprehensive blueprint for building the first prototype.

### Execution Plan Structure

#### 5a. Product Definition
- Core value proposition (one sentence)
- Key features for MVP (max 3)
- What it does NOT do (scope boundaries)
- Success metrics for prototype validation

#### 5b. Technical Architecture
- System diagram (components and data flow)
- Technology stack choices with rationale
- Build vs. buy decisions for each component
- Key technical risks and mitigation strategies

#### 5c. Bill of Materials / Resources
- **Hardware products**: Exact parts, suppliers, unit costs, lead times
- **Software products**: APIs, services, frameworks, hosting, estimated monthly costs
- **Mixed**: Both of the above

#### 5d. Build Instructions
- Step-by-step assembly/development instructions
- Estimated time per step
- Skills required per step
- Dependencies between steps (critical path)

#### 5e. Validation Plan
- How to test the prototype with real users
- Minimum sample size for validation
- Key hypotheses to test
- Go/no-go criteria for moving to full product

#### 5f. Timeline & Milestones
- Week-by-week plan for first 12 weeks
- Key decision points
- Resource requirements (people, capital, equipment)

#### 5g. Cost Estimate
- Total prototype cost (materials + labor + services)
- Monthly burn rate
- Funding strategy (bootstrap, angel, grant, etc.)

---

## Record Keeping

### File Structure

```
auto_research/
├── research-plan.md              # This file
├── runs/
│   ├── cycle_001/
│   │   ├── step1_technologies.csv
│   │   ├── step2_competitive.csv
│   │   ├── step3_markets.csv
│   │   ├── step4_feasibility.csv
│   │   ├── step5_execution/
│   │   │   ├── idea_001_plan.md
│   │   │   └── idea_002_plan.md
│   │   └── cycle_001_report.md   # Summary report for this cycle
│   ├── cycle_002/
│   │   └── ...
│   └── ...
├── global_registry.csv           # Master list of ALL ideas across all cycles
├── patterns.md                   # Observed patterns, lessons learned across cycles
└── sources.md                    # Curated list of high-quality sources discovered
```

### Global Registry Schema (global_registry.csv)

| Column | Description |
|--------|-------------|
| id | Unique ID (e.g., C001-T003 = cycle 1, tech 3) |
| cycle | Which cycle discovered it |
| technology | Technology name |
| domain | Domain category |
| source_url | Where it was found |
| trl | Technology Readiness Level |
| step1_status | PROMOTED / REJECTED |
| step1_reason | Brief reasoning |
| competitive_score | 1–5 density score |
| step2_status | PROMOTED / REJECTED / N/A |
| step2_reason | Brief reasoning |
| product_idea | Specific product concept |
| tam | TAM estimate |
| sam | SAM estimate |
| step3_status | PROMOTED / REJECTED / N/A |
| step3_reason | Brief reasoning |
| feasibility_score | 1–10 |
| step4_status | PROMOTED / REJECTED / N/A |
| step4_reason | Brief reasoning |
| step5_status | COMPLETE / IN_PROGRESS / N/A |
| date_discovered | Date first encountered |
| date_last_updated | Last update |

### Per-Step CSV Schemas

**step1_technologies.csv**: id, technology, domain, source_url, breakthrough, trl, time_to_product, status, reasoning

**step2_competitive.csv**: id, technology, competitors_found, competitive_score, differentiation_angles, status, reasoning

**step3_markets.csv**: id, technology, product_idea, target_market, tam, sam, som, revenue_model, growth_rate, status, reasoning

**step4_feasibility.csv**: id, product_idea, tech_risk, market_risk, execution_risk, timing_risk, tailwinds, headwinds, feasibility_score, status, reasoning

### Deduplication Strategy
- Before starting Step 1 in any new cycle, load `global_registry.csv` and extract all previously seen technologies
- Use semantic similarity (not just exact match) to avoid rediscovering the same idea phrased differently
- If a previously rejected idea appears with NEW evidence (new paper, cost reduction, etc.), it can be re-evaluated — mark as "RE-EVALUATED" with reference to original entry

### Pattern Tracking (patterns.md)
After each cycle, append observations:
- Which domains yielded the most promotions?
- What's the most common rejection reason at each stage?
- Are there technology clusters forming?
- What search strategies found the best candidates?

---

## Iteration Protocol

1. **Start cycle**: Create `runs/cycle_NNN/` directory
2. **Step 1**: Search for 10 new technologies (avoiding duplicates from global registry)
3. **Steps 2–4**: Run promoted ideas through the funnel, recording results at each stage
4. **Step 5**: Build execution plans for survivors
5. **Record**: Update global registry, write cycle report, append to patterns
6. **Repeat**: Begin next cycle

### Convergence & Stopping
- Continue cycles until we have **at least 3 ideas** with completed execution plans (Step 5)
- OR until 10 cycles have been completed (whichever comes first)
- After stopping, produce a final ranked report of all Step 5 graduates

---

## Quality Guidelines

- **Cite sources**: Every claim should link back to a paper, article, or data source
- **Be specific**: "Perovskite solar cells achieved 33.7% efficiency (Nature, Jan 2026)" not "solar tech is improving"
- **Quantify**: Numbers over adjectives. "$2.3B market growing at 24% CAGR" not "large and growing market"
- **Be honest about uncertainty**: Flag assumptions clearly, distinguish facts from estimates
- **Bias toward action**: When borderline, promote and let the next stage filter — information compounds through the funnel

---

## Step 6: Deep Research on Final Candidates

**Purpose**: Take select winning ideas from the 20-cycle funnel and validate them deeply enough to confidently pick ONE to build. Each deep research pass makes it crystal clear what the idea entails — the real competitive landscape, exact build steps, and honest risk picture.

**When to execute**: On demand — specify which idea to deep-research and this playbook runs.

### File Structure

```
auto_research/
├── deep_research/
│   ├── {idea_slug}/
│   │   ├── 01_product_definition.md
│   │   ├── 02_competitive_analysis.md
│   │   ├── 03_feasibility_and_prototype.md
│   │   ├── 04_customer_validation.md
│   │   ├── 05_comparison_scorecard.md
│   │   └── assets/           # diagrams, screenshots, supplier links
```

### 6a. Product Definition (Refined)

Go beyond the one-page execution plan. Nail down:
- **Exact problem statement**: Who has this problem, how painful is it, what do they do today?
- **Product scope for v1**: What the prototype does (3 features max) and what it explicitly does NOT do
- **User workflow**: Step-by-step how a customer uses this on day 1
- **Pricing model**: Exact price point with justification (what's their alternative cost?)
- **Ideal first customer profile**: Company size, industry, role of buyer, budget authority

### 6b. Deep Competitive Analysis

Not just "who exists" — validate from multiple angles:

1. **Direct competitors**: Companies selling the same thing to the same buyer
2. **Indirect competitors**: Different solution to the same problem (including manual/human processes)
3. **Adjacent movers**: Companies one pivot away from entering this space
4. **Open source / DIY**: Can customers cobble this together themselves?
5. **Big tech risk**: Is any FAANG/incumbent likely to add this as a feature?

For each competitor found:
- What they charge, how many customers, funding raised
- Their actual product capabilities (sign up for demos/trials if possible)
- Their weaknesses and gaps
- Why a customer would pick YOU over them

**Verdict**: Clear GO / NO-GO / CONDITIONAL-GO with reasoning

### 6c. Feasibility & Prototype Plan

The goal: hand this document to yourself on a Saturday morning and start building.

1. **Bill of Materials** — exact parts with:
   - Product name, model number
   - Supplier + link (verify in stock / lead time)
   - Unit cost
   - Alternatives if primary is unavailable

2. **Software stack** — exact libraries, APIs, models:
   - What to use for each function
   - Any licensing concerns
   - Performance expectations (latency, accuracy)

3. **Build instructions** — step by step:
   - Hardware assembly sequence (if applicable)
   - Software setup / environment
   - Integration steps
   - Expected time per step

4. **Risk register** — for each identified risk:
   - Likelihood (High/Med/Low)
   - Impact if it happens
   - Mitigation plan (not generic — specific actions)
   - Fallback if mitigation fails

5. **Prototype validation plan**:
   - What "working" looks like (measurable success criteria)
   - How to test with a real user/environment
   - Minimum data needed to call it validated
   - Timeline: days/weeks to each milestone

6. **Total cost & time to working prototype**:
   - Itemized budget
   - Calendar estimate (assuming nights/weekends vs. full-time)

### 6d. Customer Validation Strategy

Before building, confirm demand:
- **Who are the first 5 customers you'd approach?** (Named companies or specific profiles)
- **What's the discovery question?** (How to ask without revealing your hand)
- **What signal = confirmed demand?** (Letter of intent, verbal commitment, pre-order, etc.)
- **Cold outreach plan**: Where do these buyers hang out? LinkedIn, trade shows, forums?

### 6e. Comparison Scorecard

Standardized across all deep-researched ideas for apples-to-apples comparison:

| Dimension | Weight | Score (1-10) |
|-----------|--------|--------------|
| Capital required (lower = better) | 15% | |
| Time to first revenue | 15% | |
| Competitive moat strength | 15% | |
| Technical risk (lower = better) | 10% | |
| Market size (SAM) | 10% | |
| Founder-market fit (your skills) | 15% | |
| Customer accessibility | 10% | |
| Scalability beyond prototype | 10% | |
| **Weighted total** | | |

"Founder-market fit" accounts for AI/ML infrastructure and deep systems experience. Ideas that lean on software/ML and can start without a co-founder score higher.

### 6f. Confidence & Verification (Learned from Sonic Wand Research)

For each major claim in the feasibility section, mark confidence:
- **VERIFIED** (independently confirmed via multiple sources)
- **ASSUMED** (reasonable but unconfirmed — mark with caveat)
- **UNVERIFIED** (critical gap that must be resolved before building)

For component sourcing, include:
- **Primary source** with specific search terms and model numbers
- **Backup source** if primary is unavailable
- **Alternate faster path** — a quick proof-of-concept version using whatever's in stock (sacrifice quality for speed to first test)

### Execution Protocol

When triggered with "deep research on [idea]":
1. Create `deep_research/{idea_slug}/` folder
2. Run thorough web research on competitors (searching from multiple angles, verifying claims)
3. Find exact components/parts/services with real links and prices
4. Identify and attempt to resolve each risk
5. Produce all 5 documents (6a–6e)
6. Mark confidence levels on all major claims (6f)
7. Score the idea on the comparison scorecard
8. If other ideas have been deep-researched, produce a head-to-head comparison
