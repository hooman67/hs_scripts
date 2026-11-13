# 04 Customer Validation: Custom Alloy Software Plugin for Metal 3D Printers

## First 5 Customers to Approach

### Customer 1: Sintavia (Hollywood, FL)
- **Why:** Defense/aerospace AM specialist. Known for developing novel material qualifications. ~15 metal printers including EOS M290 and M400. Funded by Sumitomo. Actively pursues AS9100/NADCAP certification for new alloys.
- **Contact approach:** VP of Materials Engineering or Chief Metallurgist.
- **Hypothesis to test:** Would Sintavia pay for software that lets them offer custom alloy printing to DoD customers?
- **Signal of interest:** They agree to a 30-minute call. They describe specific customer requests they have declined due to alloy limitations.

### Customer 2: Beehive Industries (Knoxville, TN)
- **Why:** Defense/propulsion focused service bureau. Aggressive growth (opened large facility 2024-2025). Printing rocket engine components where novel high-temperature alloys are valuable.
- **Contact approach:** CTO or Head of Process Development.
- **Hypothesis to test:** Is novel alloy capability a competitive differentiator for winning DoD contracts?
- **Signal of interest:** They describe active programs requiring alloys not available as pre-alloyed powder.

### Customer 3: Rosswag Engineering (Pfinztal, Germany)
- **Why:** Explicitly markets "custom alloy development for AM" as a service. Already does powder atomization + AM process development. One of very few bureaus that actively develops new AM alloys.
- **Contact approach:** Head of Additive Manufacturing or R&D Director.
- **Hypothesis to test:** Would Rosswag adopt software to accelerate their alloy development process? Or do they view their manual process as their competitive moat?
- **Signal of interest:** They describe specific pain points in current alloy development workflow (too slow, too expensive, too many iterations).

### Customer 4: Morf3D (El Segundo, CA)
- **Why:** Boeing HorizonX backed. Aerospace AM specialist. Known for pushing AM material boundaries. Strong engineering team.
- **Contact approach:** VP of Engineering or Principal Materials Engineer.
- **Hypothesis to test:** Would Morf3D use this as a differentiated offering to Boeing and other aerospace customers?
- **Signal of interest:** They confirm Boeing has asked for non-standard alloy parts that they could not produce.

### Customer 5: Carpenter Additive (Philadelphia, PA)
- **Why:** Both a powder supplier AND an AM service bureau. They produce metal powders AND print parts. Unique perspective on whether in-situ mixing threatens or complements their powder business.
- **Contact approach:** Director of Additive Solutions or VP of Technology.
- **Hypothesis to test:** Would a powder company view in-situ mixing as a threat (cannibalize pre-alloyed sales) or opportunity (sell more elemental powders)?
- **Signal of interest:** They express interest in partnering rather than competing. Or they reveal that elemental powder blending is something customers already request.

## Discovery Questions

### Problem Validation (ask first)
1. "How often do you receive RFQs or customer inquiries for alloys you cannot currently print? What percentage of total inquiries?"
2. "When a customer needs a non-standard alloy, what do you do today? Walk me through the process."
3. "What does it cost you (time, money) to develop a new alloy for AM printing? How many attempts does it typically take?"
4. "Have you ever lost a contract because you could not offer a specific material? What was the value of that contract?"
5. "Are there specific alloy families (high-entropy, gradient, refractory) that your customers are asking about?"

### Solution Validation (ask second, only if problem confirmed)
6. "If software existed that could generate laser parameters for mixing elemental powders into novel alloys during printing, how would that fit into your workflow?"
7. "What would you need to see (data, certifications, demonstrations) before you would trust such software for production parts? For R&D parts?"
8. "What printer models do you run? Which would you be willing to experiment with?"
9. "Would you be willing to dedicate machine time (say, 50 hours over 3 months) to validate a new alloy mixing capability if the software were provided free during the pilot?"
10. "What price point would make sense for this capability? How do you think about software spend per machine?"

### Competitive/Alternative Validation
11. "Have you evaluated or used Elementum 3D powders? What was your experience?"
12. "Do you use any computational tools for materials development today (Citrine, Thermo-Calc, ICME tools)?"
13. "Has your printer OEM (EOS, SLM, etc.) discussed any plans for multi-material or alloy mixing capabilities?"

## Demand Signals (What Confirms Interest)

### STRONG signals (proceed to prototype):
- Customer describes specific lost contracts due to alloy limitations (quantified revenue loss)
- Customer offers machine time for validation pilot without payment
- Customer asks "when can we start?" or "how do I get early access?"
- Customer names 3+ specific alloy compositions they would want immediately
- Customer introduces you to their end-customer (aerospace OEM) for joint validation

### MODERATE signals (continue exploration):
- Customer agrees to second meeting with their technical team
- Customer says "this is interesting but I need to see it work first"
- Customer identifies 1-2 alloys of interest but frames as "nice to have" not "must have"
- Customer refers you to another service bureau that might be more interested

### WEAK/NEGATIVE signals (reconsider viability):
- Customer says "our customers never ask for non-standard alloys"
- Customer says "we would just buy pre-alloyed powder if it existed"
- Customer is unwilling to risk machine time on unproven process
- Customer says "EOS would need to certify this before we could use it"
- Customer says "we tried powder blending and it didn't work"

## Cold Outreach Plan

### Where Buyers Hang Out

| Channel | Specifics | Quality |
|---------|-----------|---------|
| RAPID + TCT Conference (annual, June) | Largest AM industry event. 5,000+ attendees. Service bureau executives attend. | HIGH -- face-to-face |
| Formnext (Frankfurt, November) | Largest global AM trade show. 30,000+ attendees. | HIGH -- international reach |
| AMUG (Additive Manufacturing Users Group) | Practitioner-focused conference. Smaller (1,500), more technical. | VERY HIGH -- right audience |
| LinkedIn AM Groups | "Additive Manufacturing" (180K+ members), "Metal AM" (15K members) | MEDIUM -- noisy but targetable |
| Metal AM Magazine | Industry publication. Covers service bureaus specifically. | MEDIUM -- for thought leadership |
| SAE/ASTM AM standards committees | Small groups of industry leaders defining AM material standards. | HIGH -- direct access to decision makers |
| AM Research community (TMS, MS&T conferences) | Academic conferences with industry attendees. | MEDIUM -- academic-leaning |

### How to Reach Them

**Phase 1: Research & Positioning (Weeks 1-4)**
- Publish technical white paper: "Computational Design of In-Situ Alloying Strategies for LPBF" (establishes credibility)
- Post on LinkedIn with simulation videos showing melt pool mixing
- Join ASTM F42 (AM standards) committee as observer

**Phase 2: Direct Outreach (Weeks 4-8)**
- LinkedIn InMail to VP/Director of Materials Engineering at target bureaus
- Template:

> Subject: Novel alloy capability for your AM machines -- research partnership

> Hi [Name], I'm building software that generates laser scan strategies for in-situ mixing of elemental powders into custom alloys during LPBF printing -- based on published NIST research on melt pool stirring. We're looking for 2-3 forward-thinking service bureaus to partner with for validation. Would your team be interested in a 20-minute conversation about whether this could add value for your aerospace customers? No cost, no commitment -- just exploring demand.

- Target: 30 outreach messages, expect 10-15% response rate (3-5 conversations).

**Phase 3: Conference Engagement (Weeks 8-16)**
- Attend AMUG or RAPID with simulation demo (laptop + visualization)
- Book meetings with service bureau leaders in advance
- Present poster or give talk if accepted

**Phase 4: Pilot Recruitment (Weeks 12-20)**
- Convert 2-3 interested parties into pilot agreements
- Formal pilot terms: 3 months, software provided free, 50 hours machine time committed, results shared for case study

### Expected Conversion Funnel

| Stage | Count | Rate |
|-------|-------|------|
| Outreach messages sent | 50 | -- |
| Conversations secured | 5-8 | 10-15% |
| Problem confirmed (interested) | 3-4 | 50-60% of conversations |
| Pilot agreement signed | 1-2 | 30-50% of interested |
| Converted to paid (post-pilot) | 1 | 50-100% of pilots with positive results |

**Realistic assessment:** Getting to 1 paying customer within 12 months is achievable but requires successful physical validation AND a bureau willing to take the risk. The sales cycle for a $60K/year decision at a service bureau is 3-6 months minimum.
