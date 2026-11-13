# Comparison Scorecard: AI Fire Sprinkler Inspection App

## Scoring Criteria

Each dimension scored 1-10 where:
- 1-3: Poor / High risk / Major concerns
- 4-6: Moderate / Manageable / Average
- 7-8: Good / Low risk / Above average
- 9-10: Excellent / Minimal risk / Outstanding

## Scorecard

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| **Capital Required** | 15% | 8 | 1.20 | $200-225K is achievable with savings/angel. Pure software = no hardware/manufacturing/inventory costs. No need for Series A to launch MVP. Tight but doable. |
| **Time to Revenue** | 15% | 6 | 0.90 | 6-7 months to beta, 8-9 months to first paying customer. Acceptable but not fast -- training data collection and model iteration create unavoidable lag. Cannot shortcut ML accuracy. |
| **Moat Strength** | 15% | 8 | 1.20 | Proprietary training data is a genuine compounding moat. Every inspection makes the model better. NFPA compliance engine adds regulatory moat. Network effects are real. However, Inspect Point could acquire/build in 18 months if motivated. |
| **Technical Risk** | 10% | 7 | 0.70 | Core tech (CNN image classification, object detection) is proven and mature. CoreML on-device inference is well-documented. Risk is in domain-specific accuracy (paint vs. corrosion vs. normal aging) -- solvable with data but unknown until tried. |
| **Market Size** | 10% | 5 | 0.50 | 15K fire protection companies, 50K inspectors. At $300/seat, max TAM is ~$180M (if every inspector subscribes). Realistically addressable market is $30-50M initially. Can expand to adjacent inspection types (alarms, extinguishers) for $500M+. Niche but real. |
| **Founder-Market Fit** | 15% | 6 | 0.90 | ML/AI expertise is the key technical differentiator and founder has it. However, zero fire protection domain knowledge and no iOS development experience. Must hire for both. The ML-specific fit is 9/10; overall fit is pulled down by domain and mobile gaps. |
| **Customer Accessibility** | 10% | 6 | 0.60 | Fire protection is a defined, findable industry (NFSA directories, trade shows, LinkedIn). However, it's a conservative industry where relationships matter. No existing industry connections. Need to attend NFSA events and build trust from scratch. Not impossible but takes time. |
| **Scalability** | 10% | 7 | 0.70 | Pure software scales well -- add users without proportional cost increase. Model improves with scale (more data). BUT: expansion requires adding new inspection types (each needs new training data). Geographic expansion is easy (same NFPA code nationwide). International expansion harder (different codes). |

## Weighted Total: 6.70 / 10

## Score Interpretation

| Range | Meaning | Action |
|-------|---------|--------|
| 8.0-10.0 | Exceptional opportunity | Go immediately, full commitment |
| 6.5-7.9 | Strong opportunity with conditions | Go with specific risk mitigations |
| 5.0-6.4 | Moderate opportunity, significant concerns | Proceed with caution, validate hard |
| Below 5.0 | Weak opportunity | Likely pass unless conditions change |

**This idea scores 6.70 -- a STRONG OPPORTUNITY WITH CONDITIONS.** It sits solidly in the "go with mitigations" zone.

## Key Strengths

1. **Clear market gap with no competition in AI vision** -- Verified that zero players (including $28M-funded Inspect Point and $1B-valued BuildOps) offer computer vision for sprinkler deficiency detection. The gap is confirmed, not assumed.

2. **Regulatory tailwind creates inelastic demand** -- NFPA 25 mandates annual inspections for every commercial building. Demand does not depend on economic cycles. Insurance companies are tightening documentation requirements post-Surfside.

3. **Pure software with compounding data moat** -- No hardware risk. Every inspection generates training data that makes the model more accurate, which attracts more users, which generates more data. This flywheel is genuinely defensible once spinning.

4. **Founder's ML expertise matches the hardest problem** -- The differentiating technology (computer vision for sprinkler deficiency detection) is exactly what the founder builds professionally. The hard part is not building forms or workflows -- it's training accurate domain-specific models.

5. **Capital efficiency** -- $200K to MVP is remarkably low for an AI product with genuine defensibility. No hardware prototyping, no manufacturing, no inventory. Risk-reward ratio is favorable.

## Key Weaknesses

1. **Training data cold-start problem** -- The product cannot exist without 1,000+ labeled sprinkler deficiency images, and these images do not exist publicly anywhere. Must convince fire protection companies to share proprietary inspection photos before the product is built. This is a chicken-and-egg problem that could stall development.

2. **Niche market ceiling** -- At $180M theoretical max TAM (and $30-50M realistically addressable), this may be "too small" for venture scale. Could be a great lifestyle/bootstrapped business ($5-15M ARR) but may not attract VC if scaling ambitions require it. Expansion to adjacent inspection types (fire alarms, extinguishers, suppression systems) is necessary for large outcomes.

3. **Domain expertise gap** -- Founder has zero fire protection knowledge. NFPA 25 is complex regulatory territory where errors have liability implications. Must hire domain expertise early and thoroughly. Cannot "learn it along the way" -- inspectors will immediately detect if the tool doesn't understand their world.

4. **Conservative customer base** -- Fire protection companies skew traditional. Technology adoption is slower than in tech-forward industries. Selling cycles may be 3-6 months. Trust must be earned through relationships, trade shows, and proven accuracy -- not through SaaS marketing playbooks.

5. **Inspect Point acquisition/build risk** -- If this product shows traction, Inspect Point (15K users, $28M funding, fire-specific platform) could add vision AI within 12-18 months. They have the distribution, domain expertise, and existing customer relationships. First-mover window is real but finite.

## Comparison to Alternatives

| vs. Alternative | Advantage | Disadvantage |
|-----------------|-----------|--------------|
| vs. Starting a SaaS in crowded market | Clear gap, no direct competition in AI vision | Niche market, need domain expertise |
| vs. Horizontal AI inspection tool | Deeper moat, regulatory lock-in, specific value prop | Smaller TAM, less flexibility |
| vs. Competing with Inspect Point directly | Different value (vision AI vs. workflow) | They have 15K users and could add vision |
| vs. Hardware/IoT approach | Zero COGS, faster iteration, lower capital | Less "moaty" than proprietary hardware |

## Final Assessment

**CONDITIONAL-GO at 6.70/10.**

This is a genuinely good opportunity for a technical founder with ML expertise. The market gap is verified, the technology is feasible, and the economics work at modest scale. The conditions that must be met:

1. Secure training data within 60 days (Gate 1 -- kill the project if this fails)
2. Hire fire protection domain expert within 30 days
3. Achieve >85% model accuracy by month 3 (Gate 2)
4. Plan for adjacent inspection types by month 6 (addresses market size concern)

If all conditions are met, this has a realistic path to $5-15M ARR as a bootstrapped/lightly-funded company, or $30-50M+ ARR as a multi-inspection-type platform with venture backing.
