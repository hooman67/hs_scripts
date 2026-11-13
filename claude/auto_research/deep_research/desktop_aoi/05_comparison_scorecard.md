# 05 Comparison Scorecard: Desktop AI-Powered AOI

## Scoring (1-10 scale, 10 = best)

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Capital Required (lower=better) | 15% | 7 | 1.05 | $245K is moderate. Hardware business requires inventory ($2K BOM x 50 units = $100K in parts before selling). Higher capital than pure software but manageable with pre-orders. |
| Time to First Revenue | 15% | 6 | 0.90 | 3-month prototype + 3-month beta = 6 months to first paid customer. Hardware lead times and beta testing add friction vs. software products. |
| Competitive Moat Strength | 15% | 4 | 0.60 | Weak moat. AI model is commoditized (open source YOLOv8). Hardware is sourceable by anyone. Moat must come from data flywheel + UX -- both take time to build. Cognex/Keyence could crush this with one product launch. |
| Technical Risk (lower=better) | 10% | 5 | 0.50 | Medium technical risk. Core ML is solved but optical system design, real-world accuracy (vs. academic datasets), and production hardware reliability are non-trivial. The telecentric lens FOV miscalculation discovered during analysis illustrates hidden hardware pitfalls. |
| Market Size (SAM) | 10% | 6 | 0.60 | SAM estimate: 5,000-15,000 small PCB assemblers in US/EU that could justify $5K AOI. At $5K hardware + $2.4K/year software = $7.4K Year 1. SAM = $37M-$111M. Decent but not massive. Constrained by how many shops actually have enough volume to justify automation. |
| Founder-Market Fit | 15% | 3 | 0.45 | Weak fit. Strong ML skills (the easy part) but no hardware, optics, or PCB manufacturing domain expertise. No industry connections. Would need to overcome significant learning curve and network-building. |
| Customer Accessibility | 10% | 5 | 0.50 | Mixed. Customers are findable (Google Maps, LinkedIn, trade shows) but dispersed, offline, and relationship-driven buyers. Not a "post on ProductHunt and get customers" market. Requires boots-on-ground sales. |
| Scalability Beyond Prototype | 10% | 5 | 0.50 | Hardware scaling is harder than software. Need contract manufacturer for production units, supply chain management, warranty/support infrastructure. Subscription software component scales well but hardware operations add complexity. |

## Weighted Total: 5.10 / 10.00

## Key Strengths

1. **Clear value proposition with quantifiable ROI:** A $5K tool that prevents $20-50K/year in defect escapes sells itself -- IF the accuracy claims hold up.
2. **Large price gap in market:** 10x cheaper than established AOI is a genuine market gap. Incumbents structurally cannot address it with their sales model.
3. **AI/ML core competency is strong:** The founder can build state-of-the-art detection models. Training pipeline, deployment, MLOps -- all in the wheelhouse.
4. **Recurring revenue via subscription:** Software updates + cloud model improvements create defensible recurring revenue that hardware-only competitors cannot easily replicate.
5. **Reshoring tailwind:** As electronics manufacturing returns to US/EU, more small shops will open, expanding the TAM.

## Key Weaknesses

1. **Extremely weak competitive moat:** The AI is commoditized, the hardware is available to anyone, and Cognex/Keyence could launch a competing product with 10,000x the resources and brand trust. The only moat is speed-to-market and data flywheel -- both are fragile.
2. **Poor founder-market fit:** No hardware expertise, no domain knowledge, no industry connections. The founder would be learning optics, PCB manufacturing workflows, and B2B hardware sales simultaneously while competing against people who've done this for decades.
3. **Hardware business complexity:** Inventory risk, supply chain, warranty/repair, physical shipping, installation support. Every unit sold creates ongoing obligations. Far more operationally complex than software.
4. **Real-world accuracy gap:** Academic datasets (HRIPCB, DeepPCB) show 98% mAP. Real-world performance with varying board designs, lighting conditions, component types, and solder paste formulations will be significantly worse. Getting from "demo that works" to "production tool customers trust" is a 6-12 month journey.
5. **Customer acquisition is expensive:** Each $5K sale requires on-site demo, installation support, training, and hand-holding. Customer acquisition cost could be $1,000-$2,000/customer, eating into the already thin hardware margin.

## Comparison to Investment Threshold

- **Revenue projection ($1.3M Year 1) requires:** ~175 hardware units sold ($5K each) + subscription revenue. Selling 175 units in Year 1 with no brand, no sales team, and no track record in a relationship-driven market is AGGRESSIVE. More realistic: 30-50 units Year 1 = $150K-$375K + subscriptions.
- **Break-even:** At $3K gross margin per hardware unit + $200/month subscription, need ~40 active customers to cover one founder's salary + operating costs.
- **Capital efficiency:** $245K buys ~100 hardware units of inventory + 12 months of founder salary. Tight but feasible IF sales materialize.

## Final Assessment

**Score: 5.10/10 -- BELOW AVERAGE for venture pursuit.**

This idea sits in a challenging middle ground: technically feasible, market exists, but weak moat and poor founder-market fit create high execution risk. The biggest concern is not "can this be built?" (it can) but "can THIS founder build a defensible business in THIS market before Cognex/Keyence notices?" The answer is: probably not without a co-founder who brings hardware expertise and industry connections.

**Would improve to 6.5+/10 with:**
- A co-founder with 5+ years in machine vision or PCB manufacturing
- Pre-validated demand (3+ LOIs from target customers before building)
- A software-only pivot (sell AI software to run on customers' existing cameras, eliminating hardware risk entirely)
