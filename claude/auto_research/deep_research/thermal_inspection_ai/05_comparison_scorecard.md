# 05_comparison_scorecard.md

## AI-Powered Thermal Inspection Tool — Comparison Scorecard

### Scoring Methodology

Each dimension scored 1-10 where:
- 1-3: Significant disadvantage / high risk / poor fit
- 4-6: Neutral / manageable / moderate
- 7-8: Advantage / low risk / good fit
- 9-10: Exceptional / near-zero risk / perfect fit

### Scores

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| **Capital Required** | 15% | 6 | 0.90 | $300K is tight for hardware+AI but feasible with phone-attachment V1 strategy. Founder-as-ML-engineer reduces cost. No margin for error. Custom handheld (V2) would require $500K+. |
| **Time to Revenue** | 15% | 6 | 0.90 | Phone attachment V1 = ~6 months to first unit sold. Realistic but requires parallel hardware + software development. Hardware certification adds unpredictable delay. Not as fast as pure SaaS. |
| **Moat Strength** | 15% | 7 | 1.05 | Proprietary training data (labeled thermal faults) is a genuine compounding moat. Network effects: more users = better model = more users. Report templates + code compliance knowledge add switching costs. BUT: if FLIR decides to compete, their distribution + brand = existential threat. |
| **Technical Risk** | 10% | 5 | 0.50 | AI accuracy for thermal fault classification is unproven at production quality. Edge inference on low-power hardware is challenging. Camera fusion (thermal+visible alignment) is a known-hard problem. Training data acquisition is the #1 technical unknown. |
| **Market Size** | 10% | 8 | 0.80 | Thermal camera market $5B+. Target segment (trades professionals): 1.3M+ in US alone. Serviceable addressable market: $500M+ (1M users × $500/year). Clear, large, growing (energy efficiency regulations drive thermal inspection demand). |
| **Founder-Market Fit** | 15% | 5 | 0.75 | Strong AI/ML and software skills perfectly match the core differentiator (the AI interpretation layer). However, hardware design (must hire), trades domain expertise (must partner), and distribution (must learn) are critical gaps. Overall: can build the brain, but needs help building the body and selling it. |
| **Customer Accessibility** | 10% | 7 | 0.70 | Target customers are concentrated in well-organized communities (InterNACHI 100K+ members, NECA chapters, trade shows). They actively discuss tools online. Not hidden behind enterprise procurement. Budget decision is usually individual or small-team. |
| **Scalability** | 10% | 7 | 0.70 | SaaS component scales beautifully (marginal cost ~$0). Hardware scales linearly (contract manufacturing). Model improves with scale (data flywheel). International expansion straightforward (thermal physics is universal, codes differ but report templates are configurable). Geographic expansion is natural. |

### Weighted Total

**TOTAL: 6.30 / 10.00**

### Interpretation

| Score Range | Verdict |
|-------------|---------|
| 8.0-10.0 | Exceptional opportunity — pursue aggressively |
| 6.5-7.9 | Strong opportunity — pursue with awareness of risks |
| 5.0-6.4 | **Viable but conditional** — pursue only if specific conditions are met |
| 3.5-4.9 | Weak opportunity — significant concerns, likely pass |
| 1.0-3.4 | Do not pursue |

**Verdict: VIABLE BUT CONDITIONAL (6.30)**

This score places the idea at the upper end of "conditional" — close to "strong" but held back by hardware complexity and founder-market fit gaps in hardware/trades domain.

### Key Strengths

1. **AI/data moat is real and compounding**: Unlike many "AI wrapper" startups, the proprietary labeled thermal fault dataset is genuinely hard to replicate. Every customer inspection improves the model. First mover with 10K users has a 2+ year data advantage.

2. **Clear, quantifiable ROI**: Saving 30 minutes per inspection at $100/hour billing = $50/use. Device pays for itself in 6-8 uses. This is not a "nice to have" — it is a calculable business tool.

3. **Market gap is verified**: No product currently ships AI interpretation + automated reporting for trades thermal. FLIR's Ace platform validates the need but confirms no one has built it yet.

4. **Software margins on hardware base**: The real business is $49/month SaaS (90% margin), not hardware. This creates a defensible recurring revenue stream that hardware incumbents cannot easily replicate without cannibalizing their ASP.

5. **Customer concentration enables efficient go-to-market**: 100K+ home inspectors in tight-knit communities. One successful forum post or trade show demo can reach thousands.

### Key Weaknesses

1. **Hardware adds significant risk and capital requirements**: Every layer of hardware (PCB, enclosure, certification, supply chain, manufacturing) adds time, cost, and failure modes. A pure SaaS play would score 7.5+.

2. **Founder lacks hardware and domain expertise**: Must hire hardware EE (expensive), must partner with domain experts (time-consuming), must learn trades distribution (unfamiliar). These are not insurmountable but add execution risk.

3. **FLIR is the existential threat**: If FLIR decides to add native AI interpretation to their sub-$1K cameras, their brand + distribution + installed base = near-impossible to overcome. The window is 18-24 months.

4. **Training data acquisition is the critical unknown**: Need 30K+ labeled thermal fault images to train production-quality model. This dataset does not exist. Building it requires inspector partnerships and significant investment (time + money). If labeling quality is poor, model will be poor.

5. **$300K capital is tight**: Budget leaves minimal margin for hardware iteration, certification delays, or pivots. One significant setback (model accuracy, supply chain, certification) could exhaust funding before revenue.

### Comparison to Strongest Alternative (Pure Software Play)

If this idea were pursued as pure software (AI layer for existing thermal cameras via phone app + cloud), scores would shift:

| Dimension | Hardware | Software-Only | Delta |
|-----------|----------|---------------|-------|
| Capital Required | 6 | 9 | +3 |
| Time to Revenue | 6 | 8 | +2 |
| Technical Risk | 5 | 7 | +2 |
| Founder-Market Fit | 5 | 7 | +2 |
| Moat Strength | 7 | 5 | -2 |
| **Weighted Total** | **6.30** | **7.35** | **+1.05** |

**Insight**: The software-only approach scores significantly higher due to lower risk and better founder fit, but sacrifices moat strength (anyone can build an app for existing cameras; owning the hardware creates lock-in).

### Recommended Path

**Phase 1 (Months 1-6, $100K)**: Software-only approach — build AI interpretation app that works with existing FLIR ONE / Seek Thermal phone attachments. Validate AI accuracy and report generation value with real users. This de-risks the business before committing to hardware.

**Phase 2 (Months 6-12, $200K)**: If Phase 1 validates (>500 paying users, >85% AI accuracy), build phone-attached thermal module with tighter integration. This gives hardware differentiation with proven software.

**Phase 3 (Months 12-24, raise Series A)**: If Phase 2 succeeds, develop custom handheld device for best-in-class experience. Fund with revenue + VC.

This staged approach reduces the weighted score's weaknesses (capital, time, technical risk, founder fit) while preserving the strengths (moat, market, scalability).
