# Scorecard: IoT Bolt Tension Monitor for Wind Turbines

## Scoring Criteria (1-10 scale, 10 = best)

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Capital Required | 15% | 5 | 0.75 | $450K is moderate. Hardware development + certification + pilot is capital-intensive compared to pure software. Not excessive for hardware startup, but leaves thin margin for error. No second chance if first hardware revision fails. |
| Time to Revenue | 15% | 4 | 0.60 | Realistically 12-16 months to first paid customer. Hardware development (6-8 months), certification (4-6 months parallel), pilot (3-6 months), then conversion. Wind industry sales cycles add 3-6 months on top. This is SLOW by startup standards. |
| Moat Strength | 15% | 7 | 1.05 | Strong moat potential: (1) proprietary failure-prediction dataset grows with deployments, (2) hardware certification creates barrier for new entrants, (3) switching costs once installed (physical hardware on bolts), (4) wind-specific expertise compounds. Weakness: no deep-tech patents, commodity components. |
| Technical Risk | 10% | 5 | 0.50 | Individual components are proven (strain gauges, LoRa, cloud). Integration and ruggedization for wind environment is the challenge. Key unknowns: LoRa propagation through tower steel, strain gauge washer longevity under vibration. Solvable but non-trivial engineering. |
| Market Size | 10% | 8 | 0.80 | 70K+ US turbines, 400K+ globally. At $200/turbine/month = $168M US TAM, $960M global TAM. SHM market growing 10%+ CAGR. Offshore wind growth adds premium segment. Adjacent markets (bridges, transmission towers) expand TAM further. |
| Founder-Market Fit | 15% | 3 | 0.45 | Honest assessment: WEAK. Founder has no hardware design experience, no wind industry relationships, no manufacturing background. Core strengths (Python, ML, cloud) are necessary for the software layer but insufficient for the hardware-intensive critical path. Must hire hardware co-founder or senior EE contractor immediately. |
| Customer Accessibility | 10% | 4 | 0.40 | Wind operators are concentrated (top 20 own 80% of US fleet) which is good for targeting. But they are conservative, have long procurement cycles (12-24 months), and new vendors face qualification barriers. No existing relationships to leverage. Industry conferences and consultancy introductions are the primary access paths. |
| Scalability | 10% | 7 | 0.70 | Once hardware is certified and manufacturing is set up, deployment is highly repeatable. Software platform scales naturally. Per-turbine economics improve with fleet density. Natural expansion path: tower bolts --> blade root --> yaw --> foundation. International expansion follows same product. |

---

## Weighted Total Score

| Dimension | Weighted Score |
|-----------|---------------|
| Capital Required (15%) | 0.75 |
| Time to Revenue (15%) | 0.60 |
| Moat Strength (15%) | 1.05 |
| Technical Risk (10%) | 0.50 |
| Market Size (10%) | 0.80 |
| Founder-Market Fit (15%) | 0.45 |
| Customer Accessibility (10%) | 0.40 |
| Scalability (10%) | 0.70 |
| **TOTAL** | **5.25 / 10** |

---

## Interpretation

**5.25/10 = BORDERLINE -- Proceed with caution, address critical weaknesses before committing capital.**

This score reflects a genuine market opportunity (large TAM, clear whitespace, strong moat potential) significantly dragged down by founder-market fit challenges and slow time-to-revenue in a conservative industry.

---

## Key Strengths

1. **Genuine whitespace**: No direct competitor sells continuous wireless bolt monitoring for wind turbines today. This is rare -- most "startup ideas" have 5+ competitors. Here, the competitive landscape is effectively empty.

2. **Compelling unit economics**: $200/month/turbine vs. $3-10M catastrophic failure or $50K+/year in manual inspection costs. The ROI math is unambiguous -- this is not a "nice to have."

3. **Natural exit path**: Wind turbine OEMs (Siemens Gamesa, GE Vernova, Vestas) historically acquire niche monitoring companies rather than building internally. Likely exit at $20-50M revenue.

4. **Data moat deepens over time**: First to deploy at scale accumulates bolt failure signature data that competitors cannot replicate without equivalent field time. ML models trained on this data become the true product.

5. **Market tailwinds**: Aging fleet (average US turbine age increasing), offshore wind growth (higher monitoring value per turbine), insurance pressure, and potential regulatory requirements all push toward adoption.

---

## Key Weaknesses

1. **Founder-market fit gap**: The critical path runs through hardware design, environmental qualification, and industrial sales -- none of which are in the founder's skillset. This is the single biggest risk. Without a hardware-experienced co-founder or senior hire, failure probability is high.

2. **Time to revenue is long**: 12-16 months minimum, realistically 18-24 months with industry sales cycle realities. This means $450K must last almost 2 years with no revenue, leaving very thin margin for hardware redesigns or customer acquisition delays.

3. **Hardware risk compounds**: Unlike software where you can iterate daily, hardware iterations take 6-12 weeks each. A failed environmental qualification test at month 5 could add 3-4 months and $30-50K to the timeline. The budget has limited contingency for multiple hardware failures.

4. **Conservative buyer**: Wind farm operators are not early adopters. They require certification, proven track record, reference customers, and often 12-24 month evaluation periods. First-time startup with no track record faces significant trust barrier.

5. **No existing customer relationships**: Cold outreach into a concentrated industry with long sales cycles is hard. Without an industry insider (advisor, co-founder, or early employee with rolodex), customer acquisition could stall despite genuine demand.

---

## Comparison to Ideal Venture Opportunity

| Attribute | This Idea | Ideal for Solo Technical Founder |
|-----------|-----------|----------------------------------|
| Time to first $1 of revenue | 12-18 months | 1-3 months |
| Capital efficiency | $450K for MVP + pilot | <$50K for MVP |
| Iteration speed | 6-12 week hardware cycles | Daily software deploys |
| Founder skill match | 40% (software layer only) | 90%+ (core product in founder's domain) |
| Sales cycle | 12-24 months | Self-serve or 1-4 week trial |
| Risk of total loss | MEDIUM-HIGH | LOW-MEDIUM |

---

## Recommendations

### If proceeding (CONDITIONAL-GO):
1. **Find a hardware co-founder** before spending any capital. This person needs: PCB design, embedded firmware, industrial sensor experience, and ideally wind/energy industry background. Offer 30-40% equity.
2. **Validate customer demand before building hardware**: Spend 4-8 weeks on customer discovery first ($0 cost beyond time). If you cannot get 3+ operators interested in a pilot conversation, the market timing may not be right.
3. **Seek strategic investment**: Apply to wind-energy-specific accelerators (e.g., Greentown Labs, New Energy Nexus) or approach Nord-Lock Group / SKF for strategic partnership/investment. They bring industry credibility + customer access.
4. **De-risk LoRa propagation first**: Before committing to full hardware design, do a $500 experiment: bring a LoRa transmitter inside a wind turbine tower and measure signal at various points. If LoRa fails, the entire architecture needs redesign.
5. **Consider the "monitoring-as-a-service" model**: Instead of selling hardware, lease it. This aligns incentives (you maintain hardware quality) and reduces customer upfront commitment. Higher blended margin over time.

### If NOT proceeding:
- The core insight (continuous bolt monitoring is valuable) is correct. The challenge is founder-market fit and capital intensity. Consider:
  - Pivoting to the **software/analytics layer only** and partnering with a hardware company
  - Targeting a **faster-adopting adjacent market** first (data center structural monitoring, bridge sensors) where sales cycles are shorter
  - Building the **cloud analytics platform** that could serve multiple hardware sensor providers, rather than vertically integrating hardware + software

---

## Final Assessment

**This is a real opportunity in a real market with a real gap.** The idea itself scores 7-8/10. The challenge is execution fit for THIS specific founder profile. A founder team with: (1) hardware/sensor background + (2) wind industry connections + (3) software/ML capability would score 7.5-8/10 overall. The missing pieces are addressable through hiring/partnerships, but they must be addressed BEFORE committing capital, not after.

**Bottom line: Do not write the first check until you have a hardware-capable co-founder and at least 3 operators who have agreed to pilot conversations. Both are achievable within 60-90 days at zero cost.**
