# 04 - Customer Validation: High-Bandwidth CubeSat Communication Modules

## First 5 Target Customers

### 1. Planet Labs (San Francisco, CA)
**Why**: Operates 200+ Earth observation CubeSats (SuperDove constellation). Generates massive imagery data. Currently limited by downlink - uses multiple ground stations to compensate. Next-gen satellites in development.
**Contact path**: VP Engineering or VP Satellite Design. Attend SmallSat conference, Planet Labs is always there. Could reach through mutual connections in Bay Area aerospace.
**Budget signal**: $200M+ annual revenue, well-funded. $120K per satellite is feasible for next-gen fleet.
**Risk**: Planet has deep internal engineering and may develop in-house solution. Also may be moving toward optical.
**Confidence: MEDIUM** - Real company with real problem, but may not be accessible to unknown startup.

### 2. Spire Global (San Francisco, CA)
**Why**: Operates 100+ CubeSats for weather, maritime, aviation data. High data volumes from GNSS-RO payloads. Public company (NYSE: SPIR), accessible investor materials confirm downlink is a constraint.
**Contact path**: CTO or VP Satellite Engineering. Public company means investor relations can provide introductions. SmallSat conference presence.
**Budget signal**: Public company with $80M+ revenue. Module cost is material but justifiable for next-gen constellation.
**Risk**: Cost-conscious (public market pressure), may prefer cheaper solutions. May be evaluating optical.
**Confidence: MEDIUM-HIGH** - Publicly documented downlink limitations in their filings.

### 3. Capella Space (San Francisco, CA)
**Why**: SAR constellation generating enormous data volumes (radar imagery is data-heavy). Already customer of Tendeg for larger reflector antennas. Proven willingness to pay for deployable antenna technology.
**Contact path**: Already uses Tendeg - demonstrates comfort with deployable antennas. VP Engineering or Principal Systems Engineer. SmallSat presence.
**Budget signal**: $100M+ raised, defense contracts. High per-satellite spend.
**Risk**: Already served by Tendeg. May not need a smaller/lighter option given their 100+ kg satellites. SAR sats are larger than 3U.
**Confidence: MEDIUM** - Good fit for technology but their sats may be too large to need a 3U module specifically.

### 4. Satellogic (Buenos Aires / US)
**Why**: Sub-meter Earth observation from small satellites. 30+ satellites in constellation. Growing rapidly. Generating high-resolution imagery with significant downlink needs.
**Contact path**: CTO or Chief Systems Architect. Active at industry conferences. Recently became public company.
**Budget signal**: Raised $150M+, contract backlog growing. Per-satellite comm investment justified.
**Risk**: International company (Argentina-origin) may have different procurement preferences. Building own vertical integration.
**Confidence: MEDIUM** - Documented downlink challenge but may prioritize own engineering.

### 5. University/Government Early Adopter (e.g., MIT Lincoln Labs, NASA Ames, AFRL)
**Why**: Need to validate technology cheaply with a customer who values innovation over heritage. University CubeSat programs (Cal Poly, MIT, Colorado) have flight opportunities and budget for novel subsystems. NASA SBIR alignment provides both funding and credibility.
**Contact path**: NASA SBIR solicitations, AFRL Small Business office, university CubeSat lab directors. Most accessible of all targets.
**Budget signal**: SBIR Phase I = $150K, Phase II = $750K. University grants $50-200K per mission.
**Risk**: Slow procurement, no production volume, may not convert to commercial relationship.
**Confidence: HIGH** - NASA actively solicits CubeSat comm proposals, well-documented path.

## Discovery Questions (for customer interviews)

### Understanding the Problem
1. "How much data does your satellite generate per orbit vs. how much can you actually downlink per day?"
2. "What is the cost to you (in $/GB or $/day of latency) of data you cannot downlink?"
3. "Have you evaluated higher-bandwidth communication options? What did you find?"
4. "What is your current antenna configuration and achieved data rate?"
5. "If you could downlink 10-100x more data per pass, what would you do differently with your mission design?"

### Understanding Constraints
6. "What is your mass/volume/power budget for the communication subsystem?"
7. "What is your tolerance for mechanical complexity (deployable vs. fixed)?"
8. "What qualification level do you require (proto-flight, full qual, heritage)?"
9. "What is your next satellite design freeze date?"
10. "What ground station infrastructure do you use and would you change it?"

### Understanding Buying Behavior
11. "What would a communication module need to demonstrate for you to include it in your next satellite?"
12. "Would you fly an unproven but tested module if the manufacturer provided insurance/replacement guarantee?"
13. "What is your budget range for a communication subsystem?"
14. "Who makes the buy decision for subsystem components - engineering or program management?"
15. "Would you consider a joint development / early-adopter discount arrangement?"

## Demand Signals to Monitor

| Signal | Source | Interpretation |
|--------|--------|---------------|
| CubeSat downlink complaints at conferences | SmallSat, IAC proceedings | Confirms ongoing pain |
| NASA SBIR topics on CubeSat comm | SBIR.gov solicitations | Government funding available |
| Competitor fundraising/hiring | LinkedIn, Crunchbase | Market heating up |
| Ground station capacity expansion | AWS, KSAT, RBC press releases | Complementary approach gaining traction (validates the problem but different solution) |
| Optical terminal miniaturization announcements | TBIRD follow-on, Mynaric press | Threat timeline accelerating |
| CubeSat constellation announcements | Launch manifests, FCC filings | Growing TAM |
| Large-sat antenna companies entering CubeSat market | Tendeg, L3Harris product announcements | Window closing |

## Outreach Plan (12-week cadence)

### Weeks 1-4: Research & Warm Outreach
- Attend virtual/physical NewSpace events (SmallSat Symposium February, SmallSat Conference August)
- Join CubeSat mailing lists and forums (CubeSat.org, small-sat Slack communities)
- LinkedIn outreach to 20 satellite systems engineers at target companies
- Request informational interviews (not selling, learning)
- Submit NASA SBIR Phase I proposal if solicitation is open

### Weeks 5-8: Structured Discovery
- Conduct 8-10 customer discovery interviews using questions above
- Present preliminary design concept (paper study level) for feedback
- Ask: "Would you co-develop with us? What would you need to see?"
- Identify 2-3 customers willing to provide letter of intent contingent on demonstration

### Weeks 9-12: Commitment Seeking
- Present simulation results and prototype plan to interested customers
- Request LOIs or MOUs for early-adopter pricing ($50-80K vs. $120K list)
- Explore joint development arrangements (customer provides bus, we provide module)
- Apply for SBIR Phase I (if not already submitted)
- Present at CubeSat developers workshop for visibility

### Success Criteria
- **Minimum**: 10 discovery conversations completed, problem confirmed by 8/10
- **Good**: 2+ LOIs or MOUs signed
- **Excellent**: 1 paying early-adopter contract ($50K+ for engineering model)
- **Kill signal**: Fewer than 3/10 interviewees confirm downlink as top-3 problem, OR all say "we are going optical"

## Key Risks in Customer Validation

1. **Credibility gap**: Without space credentials on the team, potential customers may not take meetings seriously. Mitigation: Lead with technical content (simulation results, published concept), mention advisory board with space heritage.

2. **Long sales cycles**: Space procurement takes 12-24 months from first contact to PO. Mitigation: Target missions already in design phase with near-term design freeze dates.

3. **NDA barriers**: Customers may not discuss their downlink constraints openly. Mitigation: Focus on published specifications, use public filings (FCC, ITU) to estimate capabilities.

4. **Moving target**: Customer may be evaluating optical simultaneously. Mitigation: Position RF as complementary to optical (works through clouds, simpler ground infrastructure, available sooner).
