# Customer Validation Plan: IoT Bolt Tension Monitor for Wind Turbines

## First 5 Target Customers

### Customer 1: Invenergy (Chicago, IL)
| Attribute | Detail |
|-----------|--------|
| **Fleet size** | 12,000+ MW wind, ~3,000+ turbines across US |
| **Turbine age** | Mix of 5-15 year old turbines, multiple OEMs (GE, Siemens, Vestas) |
| **O&M model** | In-house O&M team (not dependent on OEM service contracts) |
| **Why them** | Largest independent wind operator in US. Multi-OEM fleet means they need vendor-neutral solutions. In-house O&M team has authority to approve technology pilots without OEM permission. |
| **Contact path** | VP of Asset Management or Director of O&M Technology. LinkedIn outreach + industry conference (AWEA/Cleanpower). |
| **Pilot scope** | 10 turbines at aging Iowa or Texas site, 80 bolts each = 800 sensor nodes |
| **Revenue potential** | 3,000 turbines x $200/mo = $7.2M ARR at full deployment |
| **Confidence of engagement** | MEDIUM -- large company, innovation-friendly but bureaucratic |

### Customer 2: Avangrid Renewables (Portland, OR)
| Attribute | Detail |
|-----------|--------|
| **Fleet size** | 8,000+ MW, ~2,500 turbines (US) |
| **Turbine age** | Significant legacy Gamesa fleet (known bolt issues on certain models) |
| **O&M model** | Mix of in-house and third-party service |
| **Why them** | Gamesa turbines have documented bolt torque maintenance requirements. Their fleet is aging into the high-risk period. Parent company (Iberdrola) is tech-forward. |
| **Contact path** | Head of Technical Services or Reliability Engineering Manager. Approach via Iberdrola innovation program. |
| **Pilot scope** | 5 turbines, focus on Gamesa 2.0MW platforms with known bolt maintenance history |
| **Revenue potential** | 2,500 turbines x $200/mo = $6M ARR |
| **Confidence of engagement** | MEDIUM-HIGH -- Gamesa bolt issues are a known pain point |

### Customer 3: Leeward Renewable Energy (Dallas, TX)
| Attribute | Detail |
|-----------|--------|
| **Fleet size** | 2,500+ MW, ~1,000 turbines |
| **Turbine age** | Acquired older fleet from OEHI (formerly Infigen). Many 10-15 year old turbines. |
| **O&M model** | Third-party O&M (open to new technology to reduce costs) |
| **Why them** | Private equity-owned (OMERS), focused on cost optimization. Older fleet = higher bolt failure risk. PE ownership means shorter decision cycles if ROI is clear. |
| **Contact path** | VP of Operations or Chief Technical Officer. PE-backed companies respond to clear ROI math. |
| **Pilot scope** | 5-10 turbines at a single site in Texas |
| **Revenue potential** | 1,000 turbines x $200/mo = $2.4M ARR |
| **Confidence of engagement** | HIGH -- PE pressure for cost reduction, aging fleet |

### Customer 4: Natural Power (wind consultancy/O&M advisor)
| Attribute | Detail |
|-----------|--------|
| **Fleet size** | Advises on 50GW+ of wind projects globally |
| **Role** | Independent technical advisor, not operator. Recommends technology to clients. |
| **Why them** | Force multiplier. If Natural Power recommends our solution, their clients (asset owners, lenders) will adopt. They provide technical due diligence for wind farm acquisitions -- bolt monitoring data increases asset value. |
| **Contact path** | Head of Asset Management Services. They actively seek new monitoring technologies to recommend. |
| **Pilot scope** | Joint study / technical validation. They test, we get credibility. |
| **Revenue potential** | Indirect -- channel influence over $50M+ in potential ARR across their client base |
| **Confidence of engagement** | HIGH -- consultancies actively seek differentiating technology |

### Customer 5: GCube Insurance (specialist wind insurer)
| Attribute | Detail |
|-----------|--------|
| **Fleet size** | Insures 100GW+ of renewable energy assets globally |
| **Role** | Not an operator -- insurer. Pays out $3-10M claims when towers collapse. |
| **Why them** | If GCube offers premium discounts for continuously monitored turbines, we get pull-through demand from EVERY operator they insure. Insurance mandate = market creation. They have financial incentive to reduce bolt failure claims. |
| **Contact path** | Head of Underwriting or Chief Risk Officer. Present loss data + monitoring value proposition. |
| **Pilot scope** | Joint loss-prevention study. They fund pilot data collection in exchange for actuarial evidence. |
| **Revenue potential** | Market creation -- could drive 10,000+ turbine adoptions via insurance requirements |
| **Confidence of engagement** | MEDIUM -- insurers are conservative but data-driven. Need actuarial proof. |

---

## Discovery Questions (for operator conversations)

### Pain & Current Process
1. "How frequently do you perform bolt torque checks on your fleet today? What drives that schedule?"
2. "What does a single bolt inspection event cost you, including crane/access, technician time, and downtime?"
3. "Have you experienced a bolt-related failure or near-miss in the past 3 years? What was the cost and root cause?"
4. "Which bolt locations concern you most? (tower flange, blade root, yaw, foundation)"
5. "How do you currently decide which bolts to check vs. skip during a maintenance window?"

### Decision Process & Budget
6. "Who in your organization would own the decision to pilot a continuous bolt monitoring system?"
7. "What is your annual O&M budget per turbine? What portion goes to structural inspections?"
8. "Do you have a technology innovation budget or process for evaluating new monitoring solutions?"
9. "What would the business case need to look like for you to deploy monitoring on your full fleet?"
10. "What is your typical timeline from pilot approval to fleet-wide rollout?"

### Technical Requirements
11. "What SCADA or CMMS systems do you use? How important is integration vs. standalone dashboard?"
12. "Do you have cellular connectivity at all your sites, or are some in areas with poor coverage?"
13. "Would you be comfortable with us modifying bolt assemblies (adding a washer), or does that require OEM approval?"
14. "What certifications or standards would a bolt monitoring system need to meet for you to install it?"
15. "How do you handle data from existing CMS (vibration/temperature)? Same team or different?"

### Value & Willingness to Pay
16. "If a system could predict bolt loosening 30-60 days before failure, how would that change your maintenance planning?"
17. "Would you pay $150-$250 per turbine per month for continuous bolt monitoring with alerts? Why or why not?"
18. "Would insurance premium reduction (if achievable) change your ROI calculation significantly?"
19. "Would you prefer to buy the hardware outright or pay a higher monthly fee with hardware included?"
20. "If we could prove the system works on 5 of your turbines over 6 months, would that be sufficient evidence for fleet rollout?"

---

## Demand Signals to Watch

### Strong Positive Signals
- Operator has experienced a bolt failure ($1M+ cost) in past 2 years
- Operator is already doing quarterly or more frequent bolt inspections (high current cost)
- Operator mentions insurance pressure or increasing premiums related to structural risk
- Operator has in-house technical team evaluating monitoring technologies
- Operator's turbines are 10+ years old with original bolts
- Operator volunteers to host a pilot without requiring payment from us
- Operator asks "when can we start?" rather than "what is it?"

### Moderate Positive Signals
- Operator acknowledges bolt maintenance is a concern but hasn't had a failure yet
- Operator is interested but defers to OEM or third-party O&M provider for technology decisions
- Operator requests a detailed technical presentation for their engineering team
- Operator mentions they budget for structural monitoring generally

### Negative / Pause Signals
- "We already have a long-term service agreement with [OEM] that covers this"
- "Our bolts are all less than 5 years old, we don't have this problem yet"
- "We would need the turbine manufacturer to approve any modifications"
- "Our insurance doesn't differentiate between monitored and unmonitored turbines"
- "We're not willing to modify bolt assemblies for any reason"

---

## Outreach Plan (First 90 Days)

### Week 1-2: Research & Preparation
- [ ] Build target list of 30 wind farm operators (US) with fleet age >8 years
- [ ] Identify key personnel at each (VP Operations, Director O&M, Reliability Engineering Manager)
- [ ] Create 1-page sell sheet (problem, solution, economics, pilot offer)
- [ ] Create 5-slide technical deck for engineering audiences
- [ ] Register for AWEA Cleanpower conference (if timing works) or regional wind O&M event

### Week 3-4: Warm Outreach
- [ ] LinkedIn connect + message to 20 targets with personalized note referencing their fleet
- [ ] Email outreach to 10 targets with 1-page sell sheet
- [ ] Contact Natural Power and 2 other wind consultancies for introductions
- [ ] Reach out to GCube and 1-2 other wind insurers (present loss reduction thesis)
- [ ] Post on LinkedIn about bolt monitoring (thought leadership, attract inbound)

### Week 5-8: Conversations & Discovery
- [ ] Target: 8-12 discovery calls from outreach efforts
- [ ] Run discovery questions, document responses in CRM
- [ ] Identify 3-5 operators willing to discuss pilot terms
- [ ] Present at any available industry webinar or local wind energy meetup
- [ ] Ask every conversation for 2-3 referrals to other operators

### Week 9-12: Pilot Negotiation
- [ ] Draft pilot agreement template (terms: free monitoring for 6 months, they provide access + installation support, data shared)
- [ ] Negotiate pilot terms with top 2-3 prospects
- [ ] Secure at least 1 signed LOI or pilot agreement
- [ ] If no LOI by week 12: reassess approach, consider pivoting outreach to O&M service providers as channel

### Channels to Leverage
| Channel | Expected Yield | Cost |
|---------|---------------|------|
| LinkedIn direct outreach | 10-15% response rate | $0 (time only) |
| Industry conferences (AWEA, Wind O&M) | 3-5 qualified conversations per event | $2-5K per event |
| Wind consultancy introductions | Warm leads, 30-50% meeting rate | Advisory equity/retainer |
| Insurance partnership (GCube) | Pull-through demand creation | Time + data sharing |
| Published case study / white paper | Inbound leads over time | $0 (after pilot data) |
| Wind energy trade publications | Awareness, credibility | $1-3K for sponsored content |

---

## Validation Milestones & Go/No-Go Gates

### Gate 1 (Week 4): Market Interest
- **Pass**: 5+ operators agree to a discovery call
- **Fail action**: Revise messaging, try O&M service provider channel, or pivot to adjacent vertical (bridges, offshore platforms)

### Gate 2 (Week 8): Willingness to Pilot
- **Pass**: 2+ operators express willingness to host pilot (verbal)
- **Fail action**: Offer more aggressive terms (pay operators for access), or reassess product-market fit

### Gate 3 (Week 12): Signed Agreement
- **Pass**: 1+ signed LOI or pilot agreement
- **Fail action**: If operators want pilot but cannot commit (procurement delays), accept verbal commitment and begin hardware development in parallel. If no interest at all: KILL the idea.

### Gate 4 (Month 6): Pilot Data
- **Pass**: System deployed, collecting data, no major hardware failures
- **Fail action**: If hardware fails -- redesign and re-pilot. If data is not actionable -- pivot to simpler use case (installation verification only).

### Gate 5 (Month 9): Conversion Signal
- **Pass**: Pilot customer expresses intent to pay for continued monitoring and/or expand to more turbines
- **Fail action**: If pilot customer does not convert -- diagnose why. If value not proven, may need longer data history. If price is barrier, adjust.

---

## Competitive Intelligence Gathering (During Validation)

During every customer conversation, ask:
1. "Are you aware of any other companies offering continuous bolt monitoring? Who else have you talked to?"
2. "Has your turbine OEM mentioned adding bolt monitoring to their service offering?"
3. "Are you evaluating any other structural health monitoring technologies currently?"
4. "What made you take this call -- is bolt monitoring something you've been actively seeking?"

This surfaces competitors we may have missed and gauges urgency of market demand.
