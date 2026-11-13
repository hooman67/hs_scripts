# Comparison Scorecard: Portable Brewery EPR Freshness Monitor

## Scoring Criteria

Each dimension scored 1-10 where:
- 10 = Exceptional / best possible scenario
- 7-9 = Strong / favorable
- 4-6 = Moderate / manageable concerns
- 1-3 = Weak / significant concerns

---

## Scores

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Capital Required | 15% | 5 | 0.75 | $400K-$450K needed to first revenue. Hardware prototyping is capital-intensive. Cannot bootstrap — requires angel round or SBIR grant. Not extreme (not $2M+), but not lean either. |
| Time to Revenue | 15% | 4 | 0.60 | 10-12 months to first revenue is realistic but NOT fast. Multiple physics gates must pass before any revenue is possible. If EPR proof-of-concept fails at week 6, entire investment is lost. No revenue path during development (unlike SaaS where you can sell early). |
| Moat Strength | 15% | 9 | 1.35 | Exceptional moat. Physics-based barrier (EPR miniaturization), patent-eligible hardware IP, brewing-specific calibration data, and consumable lock-in. No competitor can replicate without deep RF engineering talent and 12+ months of development. DO meter companies cannot pivot to EPR without fundamentally different hardware. |
| Technical Risk | 10% | 3 | 0.30 | HIGH technical risk. EPR miniaturization to handheld form factor with adequate sensitivity for beer-matrix measurements is unproven at this scale. SpinMagIC chip is not commercially available. Multiple physics gates (resonator Q, magnet homogeneity, sensitivity floor) must all pass. Any single failure is project-ending. |
| Market Size | 10% | 3 | 0.30 | Small TAM. ~9,500 US craft breweries, realistic penetration $7-9M over 5 years for brewing alone. This is a solid niche business ($2-3M/year at maturity) but NOT venture-scale without significant adjacency expansion (wine, spirits, pharma, food). Even with adjacencies, total addressable is probably $30-50M — not a billion-dollar market. |
| Founder-Market Fit | 15% | 3 | 0.45 | POOR fit for solo AI/ML engineer. Core value creation is in RF/microwave hardware engineering and analytical chemistry — neither is in the founder's wheelhouse. Would need to find and manage an RF engineering co-founder/contractor AND a food science advisor from day 1. Software/cloud/ML skills are necessary but insufficient. |
| Customer Accessibility | 10% | 6 | 0.60 | Craft brewers are accessible via guilds, conferences (CBC, MBAA), LinkedIn, and local communities. They are generally friendly and willing to talk. However, founder has NO existing relationships in the brewing industry. Cold outreach is feasible but requires 2-3 months of relationship building. Brewing is a tight-knit community where peer endorsement matters enormously. |
| Scalability | 10% | 4 | 0.40 | Hardware businesses scale harder than software. Each unit requires manufacturing, QC, inventory management, and physical distribution. Consumable cartridges add recurring revenue but also supply chain complexity. International expansion requires regulatory certification (CE, etc.). Adjacent markets (wine, spirits, food) require separate validation and potentially different hardware calibration. Not a "deploy code and scale" business. |

---

## Weighted Total

| | |
|---|---|
| **Weighted Score** | **4.75 / 10.0** |
| **Percentile Interpretation** | Below average for a startup opportunity |

---

## Score Breakdown by Category

```
Capital Required (15%)    [=====     ] 5/10  (0.75)
Time to Revenue (15%)     [====      ] 4/10  (0.60)
Moat Strength (15%)       [========='] 9/10  (1.35)
Technical Risk (10%)      [===       ] 3/10  (0.30)
Market Size (10%)         [===       ] 3/10  (0.30)
Founder-Market Fit (15%)  [===       ] 3/10  (0.45)
Customer Access (10%)     [======    ] 6/10  (0.60)
Scalability (10%)         [====      ] 4/10  (0.40)
                                      ------
WEIGHTED TOTAL                         4.75/10
```

---

## Key Strengths

1. **Exceptional moat (9/10)**: This is the single strongest attribute. The physics-based barrier is real and durable. No one can clone this without years of RF engineering and domain calibration data. Patent potential is strong. Consumable lock-in adds recurring revenue defensibility.

2. **Genuine white space**: Zero direct competitors exist anywhere in the world. The product would create a new category. First-mover advantage is meaningful in niche instrumentation markets.

3. **Validated science**: EPR measurement of beer oxidation radicals is well-established in academic literature. The method works — the question is whether it can be miniaturized and productized, not whether the underlying science is sound.

4. **Clear value proposition**: "Measure actual staling damage in 30 seconds" vs. "infer possible staling from oxygen levels" is a genuinely 10x improvement in information quality.

---

## Key Weaknesses

1. **Technical risk dominates (3/10)**: The entire venture depends on solving a cutting-edge physics/engineering challenge (miniaturized EPR with beer-matrix sensitivity). If the resonator Q-factor is too low, or the permanent magnet homogeneity is insufficient, or sensitivity floor is above the biologically relevant range — there is no pivot. The physics either works or it doesn't.

2. **Founder-market fit is poor (3/10)**: An AI/ML infrastructure engineer attempting to build a microwave spectroscopy hardware product is a significant mismatch. The founder can build the software/cloud/ML stack (perhaps 30-40% of the total product), but the core hardware that creates value is entirely outside their expertise. This requires finding, evaluating, and managing specialized talent (RF engineers) in a field the founder cannot deeply assess.

3. **Small market limits upside (3/10)**: Even with perfect execution, the US craft brewing market caps out at $7-9M total hardware revenue over 5 years. This makes it a strong lifestyle business or small acquisition target, but NOT a venture-scale opportunity. Adjacency expansion (wine, spirits, pharma, food oils) could multiply the market 3-5x, but each adjacency requires separate R&D, validation, and go-to-market.

4. **Hardware scaling is hard (4/10)**: Manufacturing, supply chain, inventory, physical distribution, calibration, warranty/repair — all the challenges of hardware that software founders underestimate. The consumable cartridge supply chain adds further complexity (spin-trap reagent shelf stability, packaging, cold chain).

---

## Comparison to Threshold

| Threshold | Score | Assessment |
|-----------|-------|------------|
| Venture-scale opportunity (>7.0) | 4.75 | NO — below threshold |
| Solid niche business (>5.5) | 4.75 | NO — slightly below threshold |
| Worth further exploration (>4.0) | 4.75 | YES — barely above threshold |

---

## Recommendation

**DO NOT PURSUE as a solo founder with this background.**

The idea has genuine technical and scientific merit. The moat is exceptional. But the combination of:
- High technical risk in a domain outside the founder's expertise
- Poor founder-market fit
- Small addressable market
- Capital-intensive hardware development

...makes this a poor fit for an AI/ML engineer working with limited capital.

### Scenarios Where This Becomes Attractive

1. **Co-founder scenario**: If paired with an RF/EPR engineer who has actually built EPR spectrometers (e.g., PhD from Bruker, CEA-Leti, or a university EPR lab), the founder-market fit score jumps to 6-7/10, and technical risk drops to 5/10. Weighted score would be ~5.8-6.2.

2. **SpinMagIC licensing scenario**: If SpinMagIC commercializes their chip and makes it available for OEM integration, the technical risk drops dramatically (4-5/10). The product becomes primarily a systems integration + software challenge — much better fit for the founder.

3. **Adjacent market expansion**: If the same hardware platform can address wine oxidation ($300B global market), pharmaceutical stability testing, and cooking oil rancidity detection, the market size score jumps to 6-7/10. This requires separate validation but is physically plausible.

4. **SBIR/grant-funded R&D**: If the physics risk can be de-risked with non-dilutive funding (NSF SBIR Phase I: $275K), the capital efficiency improves significantly. Pursue government grants for the hardware R&D; use private capital only for go-to-market.

---

## Final Verdict

| Attribute | Value |
|-----------|-------|
| Weighted Score | 4.75 / 10.0 |
| Recommendation | CONDITIONAL NO-GO (for this specific founder profile) |
| Revisit if | RF/EPR co-founder found, OR SpinMagIC chip becomes available, OR SBIR grant secured for hardware de-risking |
| Alternative | Consider licensing the concept/IP to Bruker or a brewing equipment company; or pursue as a side project with university collaboration |
