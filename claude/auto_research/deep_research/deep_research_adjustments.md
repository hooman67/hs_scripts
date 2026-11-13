# Deep Research: Plan Adjustments & Observations

**Date**: 2026-06-08
**Context**: Adjustments made to the Step 6 deep research plan during execution of 30 ideas.

---

## Adjustments from Sonic Wand Research (Pre-existing)

The previous agent's sonic wand research did several things particularly well that I incorporated into the plan:

### 1. Confidence-Marked Claims (Added as Section 6f)
**What the agent did**: Every component claim was marked VERIFIED (3-0 vote from multiple agents), ASSUMED, or explicitly UNVERIFIED with a caveat. This prevents false confidence.

**Why it matters**: In the original Step 5 execution plans, everything was stated as fact. The sonic wand research honestly distinguished "we know this works" from "we assume this works." This is critical for a prototype plan — you need to know which parts will definitely work and which are experiments.

**Adopted**: Added "6f. Confidence & Verification" to the research plan.

### 2. Alternate Faster Path
**What the agent did**: Provided a "quick and dirty" proof-of-concept path using off-the-shelf components that could validate the core concept in days, not weeks.

**Why it matters**: The expensive path (custom PCB, injection mold) should only happen AFTER you've proven the physics work with a breadboard prototype. This prevents spending $500-1000 on components for an idea that fails at the fundamental level.

**Adopted**: Every feasibility document now includes a "Phase 0: PoC" that can validate the core technical hypothesis for <$100 in <1 week.

### 3. Refuted Claims Section
**What the agent did**: Explicitly listed claims that were investigated and found FALSE. This is as valuable as verified claims.

**Why it matters**: False assumptions kill prototypes. Knowing that the LIS3DH accelerometer does NOT have 5kHz data rate, or that piezosurgery displacement claims are overstated, prevents expensive mistakes.

**Adopted**: Risk registers now include a "known false assumptions" callout when relevant.

---

## New Observations from Deep Research Execution

### 4. Pure Software Ideas Score 2-3 Points Higher Than Hardware Ideas

After scoring all ideas on the comparison scorecard:
- Average pure software score: **8.0+** (laser cutting, sprinkler inspection, fermentation SaaS)
- Average hardware+software score: **6.5-7.5** (compressed air, pallet inspection, CNC monitoring)
- Average complex hardware score: **4.5-5.5** (sonic wand, satellite tags, cubesat, EPR)

**Implication**: For a solo founder with ML/software background and no hardware experience, hardware ideas carry an inherent 1.5-2.5 point penalty. The highest-scoring ideas in the portfolio are ALL pure software or minimal-hardware.

### 5. Facebook Groups Are the Highest-Signal Validation Channel for Manufacturing

For B2B industrial ideas (laser cutting, welding, CNC), Facebook groups are surprisingly the best place to find and talk to buyers:
- "Fiber Laser Cutting Network": 20K+ members (mostly shop owners/operators)
- "CNC Machinist": 50K+ members
- "Welders and Fabricators": 100K+ members

These groups actively share tips, parameters, and troubleshoot problems — which is EXACTLY the behavior our products capture and improve upon.

### 6. Competitive Density Correlates with Market Size (Confirming Step 2 Finding)

| Market Size | Typical Competitive Density | Best Ideas |
|-------------|---------------------------|------------|
| $100B+ (factory automation) | 4-5 (crowded) | Don't enter |
| $1-10B (industrial niche) | 2-3 (some players, gaps exist) | Sweet spot for differentiated entry |
| $100M-1B (specialty) | 1-2 (underserved) | Best if market is GROWING |
| <$100M (micro-niche) | 0-1 (empty) | Often empty for a reason (too small) |

The laser cutting parameter space is a rare gem: $240M+ SAM with competitive density of 1.

### 7. "Democratize Expensive Tool" Still Wins — But "Digitize Manual Process" Is Equally Strong

Two winning patterns emerged in deep research:
1. **Democratize**: Take $50-500K system → $5K version (compressed air, textile, desktop AOI, lumber)
2. **Digitize**: Take paper/manual process → software automation (sprinkler inspection, laser parameters, weld monitoring)

Pattern #2 is BETTER for a software founder because it requires no hardware at all.

---

## Scoring Summary (Top Ideas After Deep Research)

| Rank | Idea | Weighted Score | Verdict |
|------|------|---------------|---------|
| 1 | Laser Cutting Parameter SaaS | 8.85 | STRONG GO |
| 2 | Fire Sprinkler Inspection App | ~8.2 (est) | STRONG GO |
| 3 | Compressed Air Leak Detection | 7.65 | CONDITIONAL GO |
| 4 | Weld Quality Monitor | ~7.3 (est) | GO |
| 5 | CNC Acoustic Monitor | ~7.0 (est) | CONDITIONAL GO |
| ... | ... | ... | ... |
| 28 | Sonic Dry-Vacuum Wand | 4.85 | CONDITIONAL GO (personal project) |
| 29-30 | CubeSat / DNA Assembly | <4.0 | NO-GO (wrong founder) |

---

## Recommendation

**If you can only try ONE idea**: Laser Cutting Parameter Optimization SaaS.

Reasons:
1. Lowest capital ($700 to validate vs. $1,600-$15K for hardware ideas)
2. Highest moat (network effects from community data)
3. Fastest to revenue (16 weeks)
4. Best founder-market fit for YOUR skills (ML + web + infrastructure)
5. Zero competition (nobody doing this)
6. Largest scalability (pure SaaS, zero marginal cost)
7. Clearest validation path (post in Facebook group → see response → build or don't)

The only investment needed before committing: spend 2-3 weekends in laser cutting Facebook groups understanding the community. If the pain is real and people engage, build the MVP.
