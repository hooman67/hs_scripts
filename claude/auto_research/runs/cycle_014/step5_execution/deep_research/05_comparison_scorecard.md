# Comparison Scorecard: AI Weld Quality Monitoring from Electrical Signatures

## Scoring Criteria

Each dimension scored 1-10 where:
- 1-3: Poor / High risk / Significant concern
- 4-6: Moderate / Manageable with effort
- 7-8: Good / Favorable conditions
- 9-10: Excellent / Strong advantage

## Scores

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Capital Required | 15% | 8 | 1.20 | $250K is achievable with savings/angel. $80 BOM is genuinely cheap. No fab needed, no inventory risk at pilot stage. Deduct 2 for hardware unknowns (EMI shielding, enclosure iterations may cost more). |
| Time to Revenue | 15% | 6 | 0.90 | 8-9 months to first paid customer is realistic but not fast. Hardware product requires physical pilot deployments, iteration cycles. ML model training requires real-world data that takes time to collect. Not a "ship code and iterate" SaaS timeline. |
| Moat Strength | 15% | 7 | 1.05 | Training data moat compounds over time (more stations = more labeled data = better models = more stations). Brand-agnostic positioning is structural advantage OEMs cannot easily replicate without cannibalizing lock-in strategy. Deduct 3 for: (a) early stage has NO moat, (b) the hardware approach is trivially replicable, (c) a well-funded competitor could out-collect data. |
| Technical Risk | 10% | 5 | 0.50 | MEDIUM-HIGH. The fundamental science is published and validated in labs. But production accuracy on cheap sensors is UNPROVEN. Key unknowns: (a) 12-bit ADC sufficient or need 16-24 bit? (b) EMI in welding environment manageable? (c) Model generalizes across brands/materials/positions? Any of these failing requires significant pivots. |
| Market Size | 10% | 7 | 0.70 | 500K+ welding stations in US. At $2,300/year/station (hardware amortized + SaaS), TAM is $1.15B. SAM (addressable with v1 MIG-only, structural/pressure): ~100K stations = $230M. SOM (realistic 3-year): 2,000-5,000 stations = $4.6-11.5M ARR. Solid for VC-scale but not massive. Deduct for: niche industrial market, long sales cycles. |
| Founder-Market Fit | 15% | 5 | 0.75 | MIXED. ML/AI expertise is the core differentiator and founder has this in spades. Cloud/backend is covered. BUT: no hardware experience (critical for this product), no welding domain knowledge, no industrial sales experience. Three significant gaps that all require mitigation (contract hires, partnerships, learning). Compensating: strong technical learning ability, gaps are addressable with money. |
| Customer Accessibility | 10% | 7 | 0.70 | Industrial buyers are findable (AISC directory, AWS sections, FABTECH). Quality Managers are a well-defined persona. The ROI story is compelling and quantifiable. Deduct 3 for: (a) industrial sales cycles are 3-6 months, (b) trust-building required (they do not buy from unknown startups easily), (c) physical demos/installs required (cannot sell remotely). |
| Scalability | 10% | 7 | 0.70 | Hardware margins are excellent (84%). SaaS margins are excellent (90%). Model improves with more data (network effect). Once product-market fit proven, can scale through distributors (Airgas, Praxair), OEM partnerships, or international expansion. Deduct 3 for: (a) hardware manufacturing scaling is harder than SaaS, (b) installation/support does not scale linearly, (c) each new welding process (TIG, stick) requires new model development. |

## Summary

| Metric | Value |
|--------|-------|
| **Weighted Total** | **6.50 / 10** |
| **Letter Grade** | **B-** |
| **Verdict** | **CONDITIONAL-GO** |

## Score Breakdown Visualization

```
Capital Required   (15%): ████████░░ 8/10  [1.20]
Time to Revenue    (15%): ██████░░░░ 6/10  [0.90]
Moat Strength      (15%): ███████░░░ 7/10  [1.05]
Technical Risk     (10%): █████░░░░░ 5/10  [0.50]
Market Size        (10%): ███████░░░ 7/10  [0.70]
Founder-Market Fit (15%): █████░░░░░ 5/10  [0.75]
Customer Access    (10%): ███████░░░ 7/10  [0.70]
Scalability        (10%): ███████░░░ 7/10  [0.70]
─────────────────────────────────────────────────
WEIGHTED TOTAL:                         6.50/10
```

## Key Strengths

1. **Capital efficiency:** $80 BOM selling at $500 gives 84% hardware margins. $250K is enough to reach revenue. No need for massive fundraising before validation.

2. **Clear competitive gap:** Nobody offers brand-agnostic + AI-based + affordable weld quality monitoring. The market positioning is clean and defensible against OEM incumbents (who are structurally incentivized to remain brand-locked).

3. **Compounding data moat:** Every deployed sensor generates labeled training data (when correlated with inspection results). The model gets better, which attracts more customers, which generates more data. Classic data network effect.

4. **Quantifiable ROI:** A single caught defect saves $5K-50K. At $150/month, the system pays for itself if it catches one defect per quarter. This makes the sales conversation mathematical, not emotional.

5. **Large but fragmented market:** 500K+ stations, mostly un-monitored. No single buyer controls the market. Can grow without needing whale accounts.

## Key Weaknesses

1. **Technical uncertainty is the #1 risk:** The entire business rests on ML accuracy in production conditions. If accuracy is <80% in real environments, the product fails. This is UNPROVEN and cannot be resolved without physical hardware + real welding environment testing. No amount of desk research de-risks this.

2. **Founder hardware gap:** Building a reliable sensor product that survives a welding environment (EMI, heat, vibration, spatter, metal dust) requires embedded systems expertise the founder does not have. The contract engineer is a critical dependency.

3. **Training data chicken-and-egg:** Need labeled production data to train a good model. Need a good model to convince customers to deploy. Welding school partnership and deliberate-defect data collection partially addresses this, but it is a real bootstrapping problem.

4. **Industrial sales cycle:** Selling to fab shops is not like selling SaaS to tech companies. Relationships matter, trust takes time, physical presence is required. 3-6 month sales cycles are common. This slows everything down.

5. **Liability exposure:** If the system says "pass" and a weld later fails structurally, there could be significant liability. Must be very careful with positioning ("screening aid" not "inspection replacement") and carry appropriate insurance.

## Comparison to Pure-Software Alternatives

If this founder had $250K and no hardware constraints, a pure-software B2B SaaS would likely score 7.5-8.0/10 (faster time to revenue, no hardware risk, better founder fit). The hardware component adds risk and complexity but also creates a much stronger moat and higher barriers to entry.

## Go/No-Go Decision Framework

**GO if:**
- [ ] Gate G1 passes (clean signal capture from cheap sensors in welding environment)
- [ ] Gate G2 passes (>80% accuracy on lab data with 200+ labeled samples)
- [ ] 3+ prospective customers verbally commit to paid pilot
- [ ] Contract embedded engineer secured at reasonable cost (<$50K for 3 months)

**NO-GO if:**
- [ ] Signal quality from $10 sensors is insufficient (need $200+ instrumentation-grade sensors)
- [ ] ML accuracy plateaus below 70% even with good data
- [ ] 15+ customer conversations yield zero pilot commitments
- [ ] Liability/insurance costs are prohibitive (>$50K/year)
- [ ] OEM announces free cross-brand monitoring within 6 months

**Decision timeline:** Invest $5K in Gate G1 (signal capture). If it passes, invest $15K in Gate G2 (model accuracy). If both pass, commit remaining $230K to full build. Total risk at each gate is capped.

## Final Assessment

This is a **solid B-tier opportunity** with the potential to become A-tier if the technical risk resolves favorably. The market gap is real, the unit economics work, and the competitive positioning is defensible. The primary concern is that the business is bet on an unproven technical hypothesis (cheap sensors + edge ML = accurate defect classification in production) and the founder has a meaningful skill gap in the hardware domain.

**Recommended next step:** Spend $500 and 2 weeks building the breadboard prototype and capturing weld signals. This single experiment de-risks the highest-uncertainty factor at minimal cost. If the signals look clean and differentiated between good/bad welds, the technical thesis gains significant credibility and the project moves to STRONG-GO.
