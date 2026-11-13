# 05 - Comparison Scorecard: Precision Pollination Monitoring Radar

## Scoring (1-10 scale, higher is better)

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Capital required (lower=better) | 15% | 4 | 0.60 | $430K is moderate for hardware startup but high relative to revenue potential. Hardware development, inventory, and field deployment all require upfront capital. Not bootstrappable. |
| Time to first revenue | 15% | 2 | 0.30 | 12-18 months minimum. Must solve physics problem (4 months), build product (4 months), AND hit a bloom season (Feb-March). Miss the window = wait another year. Worst-case: 24 months to first dollar. |
| Competitive moat strength | 15% | 7 | 1.05 | IF the radar physics works, micro-Doppler IP for insect classification is genuinely defensible. No one else is doing radar-based pollinator monitoring. Patents on signal processing algorithms would be strong. But this moat only exists if the range problem is solved. |
| Technical risk (lower=better) | 10% | 2 | 0.20 | Fundamental physics uncertainty: can mmWave radar detect 100mg targets at useful range? Published literature suggests 2-5m, not 50m. This is not an engineering problem (solvable with effort) -- it may be a physics limitation (unsolvable with current tech). Score 2 = very high risk. |
| Market size (SAM) | 10% | 5 | 0.50 | SAM: ~7,600 CA almond operations + ~5,000 specialty berry operations = 12,600 potential customers. At $4K/unit x 4 units average = $16K/customer x 12,600 = $200M theoretical SAM. But realistic penetration in 5 years: 2-5% = $4M-$10M. Decent but not massive. |
| Founder-market fit | 15% | 2 | 0.30 | Critical mismatch. Founder has no RF/radar expertise (the core technical challenge), no agriculture domain knowledge, no grower relationships. Would need radar co-founder AND ag advisor. ML/cloud skills are necessary but not sufficient. |
| Customer accessibility | 10% | 4 | 0.40 | Almond growers are identifiable and concentrated geographically (Central Valley, CA). But they are conservative, relationship-driven buyers with seasonal decision windows. No warm introductions = cold start. University/USDA path is more accessible but lower revenue. |
| Scalability beyond prototype | 10% | 5 | 0.50 | Hardware scales linearly (each unit must be manufactured and deployed). Software/ML component scales well. Could potentially license technology rather than sell hardware. SaaS recurring revenue helps. But manufacturing + field deployment is inherently less scalable than pure software. |

## WEIGHTED TOTAL: 3.85 / 10.00

## Key Strengths

1. **Genuine whitespace.** Zero radar-based pollinator monitoring products exist. If the physics works, first-mover advantage is real and defensible with IP.

2. **Quantifiable ROI for buyer.** Growers can calculate exactly what 5-10% yield improvement is worth. The value proposition is not "nice to have" -- it is measurable in dollars per acre.

3. **All-weather advantage over alternatives.** Unlike cameras (fail in rain/dust/fog) and microphones (fail in wind), radar works in all conditions. California almond bloom coincides with rain season -- this matters.

4. **Hardware lock-in.** Once deployed, switching costs are high. Growers will not rip out installed sensors.

5. **Regulatory tailwind.** USDA and state ag departments are increasingly mandating pollinator-friendly practices. Data-driven pollinator monitoring aligns with policy direction.

## Key Weaknesses

1. **CRITICAL: Physics may not work.** The entire business depends on an unproven assumption about radar range for bee-sized targets. Published research is discouraging. If detection is limited to 5m, you need one unit per row -- making economics absurd ($100K+ per field).

2. **CRITICAL: Extreme seasonality.** Revenue concentrates in a 3-6 week bloom window. Hardware is idle 90% of the year. This makes unit economics, cash flow, and customer value all structurally worse than year-round products.

3. **$64M gorilla in the room.** BeeHero has the capital, the grower relationships, and a working product. They could copy any proven approach within 6-12 months, or simply acquire the startup.

4. **Founder gap.** No RF/radar expertise and no agriculture connections means both the core technical challenge and the go-to-market are uphill battles simultaneously.

5. **Bloom window dependency.** Cannot validate with customers, cannot generate revenue, cannot even test the product outside of a narrow seasonal window. Slows iteration cycle to once per year.

## Summary Verdict

**Score: 3.85/10 -- BELOW THRESHOLD for pursuit.**

This idea has a genuine insight (growers need objective pollination data) and a defensible technical approach (radar-based micro-Doppler classification). However, the combination of (a) unresolved physics risk, (b) a well-funded incumbent, (c) extreme seasonality, and (d) poor founder-market fit makes this a poor bet for a first-time hardware startup founder without radar expertise.

**If pursuing anyway:** The only rational path is to first spend $5K and 4 weeks in a lab to determine if the physics works at commercially viable range. If YES (>20m detection of bee-sized targets with <$500 hardware), revisit the entire scorecard -- moat strength jumps to 9, and the path forward becomes much clearer. If NO, walk away having spent only $5K and 1 month.
