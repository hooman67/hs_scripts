# 05 Comparison Scorecard: Custom Alloy Software Plugin for Metal 3D Printers

## Scoring (1-10, where 10 is best)

| Dimension | Weight | Score | Reasoning |
|-----------|--------|-------|-----------|
| Capital required (lower=better) | 15% | 3/10 | $990K is high for pre-revenue software. Requires 4 PhDs. Physical validation adds $100K+ before knowing if concept works on commercial machines. Compare to typical SaaS ($50-200K to MVP). |
| Time to first revenue | 15% | 4/10 | 9-10 months optimistic, 14-16 realistic. Physical validation bottleneck cannot be parallelized. Each alloy takes weeks to print + characterize. Compare to pure software (3-6 months). |
| Competitive moat strength | 15% | 3/10 | Core algorithm is based on PUBLIC NIST research. PySLM provides open-source scaffolding. Moat is only in validated recipe library (which takes years to build). OEMs can replicate with firmware access. No patent protection on public-domain research. |
| Technical risk (lower=better) | 10% | 3/10 | HIGH technical risk. Three critical unknowns: (1) Can commercial scanners execute elliptical paths? (2) Does physical mixing match simulation? (3) Will OEMs allow build file modification? Any one of these could kill the project. |
| Market size (SAM) | 10% | 4/10 | SAM is 300 metal AM service bureaus x $60K = $18M. BUT realistic addressable (R&D-focused bureaus with EOS machines who would adopt) is maybe 30 x $60K = $1.8M. Even with OEM expansion, SAM ceiling is $30-50M -- below typical venture targets. |
| Founder-market fit | 15% | 2/10 | Severe mismatch. Founder has zero metallurgy expertise, zero AM industry connections, zero physical science background, zero relationships with target customers. Would be entirely dependent on hired PhDs for all technical decisions. Cannot evaluate core technology. |
| Customer accessibility | 10% | 5/10 | Service bureaus are identifiable (known industry), attend conferences, are on LinkedIn. Not hiding. But they are risk-averse industrial buyers with long sales cycles (6+ months). Not accessible in the way that developers or SMBs are. |
| Scalability beyond prototype | 10% | 4/10 | Each new printer platform requires $50K+ in validation. Each new alloy requires physical testing. Scaling is linear, not exponential. Software itself scales, but the validated recipe library grows slowly. |

## Weighted Total

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Capital required | 0.15 | 3 | 0.45 |
| Time to first revenue | 0.15 | 4 | 0.60 |
| Competitive moat strength | 0.15 | 3 | 0.45 |
| Technical risk | 0.10 | 3 | 0.30 |
| Market size (SAM) | 0.10 | 4 | 0.40 |
| Founder-market fit | 0.15 | 2 | 0.30 |
| Customer accessibility | 0.10 | 5 | 0.50 |
| Scalability beyond prototype | 0.10 | 4 | 0.40 |
| **TOTAL** | **1.00** | -- | **3.40 / 10.00** |

## Key Strengths

1. **Genuine white space.** No direct competitor exists today. The product concept is novel and technically sound.
2. **Public-domain foundation.** No licensing fees or IP negotiations needed to access the underlying NIST research. Low legal risk.
3. **Software-only model.** No hardware manufacturing, no inventory, no supply chain. High gross margins once validated.
4. **Growing market.** Metal AM market growing 25%+/year. More printers deployed = more potential licenses.
5. **High switching costs once adopted.** If a bureau validates specific alloy recipes on their machines using this software, switching to a competitor requires re-validating all recipes (months of work).

## Key Weaknesses

1. **Fatal platform dependency.** Entirely dependent on printer OEM cooperation (or at minimum, tolerance). EOS/Trumpf can block access at firmware level or build competing feature. No contractual protection.
2. **Catastrophic founder-market mismatch.** Founder has none of the required domain expertise (metallurgy, AM process engineering, materials characterization). Building a materials science company without materials science background is extremely high risk.
3. **Physical validation bottleneck.** Cannot know if core concept works without expensive ($100K+), time-consuming (4-6 months) physical experiments. This is not a "build fast, test fast" software product.
4. **Tiny realistic market.** 300 service bureaus sounds good, but only 15-30 are realistic buyers (R&D-oriented, right machines, right customers, right risk tolerance). At $60K/year, that is $1-2M -- not venture-scale.
5. **Weak moat.** Based on public research, implementable with open-source tools, no patent protection. University groups and OEMs can replicate once concept is validated.
6. **Capital inefficiency.** $990K for 4 PhDs to serve <30 potential customers with high physical validation costs per machine platform. Risk/reward ratio is poor.
7. **OEM kill switch.** If the concept succeeds and in-situ alloying becomes valuable, printer OEMs will build it themselves. Startup is doing R&D validation that OEMs will harvest.

## Final Assessment

**Score: 3.40 / 10.00 -- NO-GO**

This idea scores poorly across nearly all dimensions. The combination of (a) severe founder-market mismatch, (b) fatal platform dependency on OEMs, (c) high capital with long physical validation timeline, (d) weak competitive moat on public-domain research, and (e) small realistic addressable market makes this unsuitable for pursuit.

The idea would score significantly better (perhaps 5.5-6.5/10) for a different founder -- specifically a computational metallurgy PhD with AM industry experience, existing OEM relationships, and access to printer time at a national lab. For Hooman's profile (AI/ML infrastructure, software/cloud, no materials science), there are far better opportunities that leverage existing strengths.
