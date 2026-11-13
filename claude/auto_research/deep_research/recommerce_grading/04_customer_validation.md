# Customer Validation Plan: AI Recommerce Grading Station

## First 5 Target Customers

### Customer 1: Nike (Nike Refurbished Program)
- **What they do**: Nike Refurbished takes returned shoes, grades them (Like New / Gently Worn / Cosmetically Flawed), cleans them, and resells at discount in select stores and online.
- **Stage**: Launched 2021, now in 15+ locations. Processing estimated 5-10M returned pairs/year across their network.
- **Why ideal**: Footwear is our beachhead category. Nike has massive volume (they process more returned shoes than anyone else on Earth). They've already invested in the recommerce concept -- they need to SCALE it. Grading is their bottleneck.
- **Pain point (hypothesized)**: Grading throughput limits expansion of the Refurbished program. Current human graders handle 30-40 pairs/hour. Inconsistency between locations means a "Gently Worn" in Portland might be a "Like New" in Memphis. Nike's brand reputation depends on consistency.
- **Decision maker**: VP/Director of Nike Refurbished or Sustainability Operations
- **Budget authority**: Nike's sustainability budget is $hundreds of millions. A $100K pilot (10 stations) is a rounding error.
- **How to reach**: LinkedIn (Nike Refurbished team members are visible). NRF conference. Nike's sustainability team actively publishes thought leadership -- engage there.
- **Confidence**: HIGH (program exists, is scaling, and grading is publicly acknowledged as a challenge in Nike's sustainability reports)

### Customer 2: ThredUp
- **What they do**: Largest online resale platform (publicly traded, TDUP). Processes 100K+ items/day at 4 distribution centers. Items arrive in bags from sellers, get photographed, described, priced, and listed.
- **Stage**: Public company, $200M+ revenue, 4 DCs processing at scale.
- **Why ideal**: Extreme volume. ThredUp's entire business MODEL is processing returned/used items. Every second saved per item = millions in annual savings. They already use automation (robotic hanging systems, automated photography via StyleShoots). They are TECHNOLOGY BUYERS.
- **Pain point (hypothesized)**: Processing cost per item is ThredUp's key unit economic challenge (disclosed in 10-K as major cost driver). Currently ~$4-5 per item in processing labor. Grading (condition assessment for pricing) is part of this. Even 20% throughput improvement would save $10M+/year across their network.
- **Decision maker**: VP Engineering or VP Operations
- **Budget authority**: Cap-ex for technology investments approved at $10-50M annually per their filings.
- **How to reach**: ThredUp's engineering team publishes blog posts and speaks at conferences. Their investor relations materials identify processing throughput as a key priority. Direct outreach to engineering leadership on LinkedIn.
- **Confidence**: HIGH (publicly traded, unit economics are documented, technology investment priorities are stated)

### Customer 3: Lululemon (Like New Program, powered by Trove)
- **What they do**: Lululemon Like New resells returned/traded-in leggings, tops, and accessories. Operated in partnership with Trove.
- **Stage**: Launched 2022, available in all US stores for trade-in. Online resale active. Growing rapidly.
- **Why ideal**: Apparel (stretchy athletics wear) is an interesting category challenge -- pilling, fabric degradation, and color fading are subtle defects that require consistent assessment. High value per item ($60-130 retail). Lululemon's brand demands PREMIUM quality control.
- **Pain point (hypothesized)**: Grading athletic fabric for pilling, seam integrity, and color fading requires experienced eyes. Training new graders takes weeks. Seasonal volume spikes (January, post-holiday) strain the system.
- **Decision maker**: Director of Like New Program or VP Sustainability
- **Budget authority**: Lululemon committed publicly to sustainability goals tied to exec compensation. Budget available.
- **How to reach**: Trove is the actual operator -- they may be the better entry point. Trove's CTO/VP Engineering would evaluate grading technology. Lululemon sustainability team for brand-level relationship.
- **Confidence**: MEDIUM-HIGH (program exists, but actual grading operation is behind Trove's wall)

### Customer 4: The RealReal (Luxury Consignment)
- **What they do**: Authenticated luxury resale. Items graded on a detailed scale that determines pricing. A Chanel bag graded "Pristine" sells for $3,000; "Good" sells for $2,000 -- grading directly = revenue.
- **Stage**: Public company (REAL), ~$500M GMV, 5 authentication/processing centers, ~1,800 employees.
- **Why ideal**: Highest value-per-grade-decision in the industry. Getting the grade RIGHT is worth potentially $hundreds per item. They process watches, handbags, shoes, jewelry, clothing. High willingness to pay for accuracy.
- **Pain point (hypothesized)**: Authentication and grading is their core IP but also their biggest cost center. They employ hundreds of "luxury experts" at $25-40/hr. Scale is limited by ability to hire and train these experts. Each new category (watches vs. bags vs. shoes) needs specialized human expertise.
- **Decision maker**: VP Product or VP Operations (authentication team)
- **Budget authority**: Technology is a stated priority in investor presentations. $50-100K pilot budget likely available.
- **How to reach**: Public company, leadership visible on LinkedIn. Attend luxury resale conferences. Their engineering blog discusses technology investments.
- **Confidence**: MEDIUM (high value target but luxury grading is more complex than standard recommerce -- may need V2 capabilities)

### Customer 5: Patagonia (Worn Wear Program)
- **What they do**: Patagonia Worn Wear buys back used Patagonia gear, repairs what can be repaired, and resells the rest. Operated both online and via touring pop-up events.
- **Stage**: Running since 2013. One of the oldest brand resale programs. Reno, NV distribution center.
- **Why ideal**: Patagonia is an INNOVATION LEADER in sustainability. They experiment with new technology (e.g., they were early adopters of repair robots). Smaller scale = easier pilot. Brand values align perfectly with "extending product life through technology." They are willing to be a reference customer for good PR.
- **Pain point (hypothesized)**: Grading outdoor gear (jackets, fleeces) for wear patterns, DWR coating degradation, zipper function -- subjective and training-intensive. Limited by skilled grader availability.
- **Decision maker**: Director of Worn Wear or VP Supply Chain
- **Budget authority**: Smaller than Nike/Lululemon, but Patagonia allocates real budget to sustainability innovation. $50K pilot is feasible.
- **How to reach**: Patagonia Reno DC is a known location. Worn Wear team members are visible on LinkedIn and speak at sustainability conferences (Circularity, GreenBiz).
- **Confidence**: MEDIUM (progressive early adopter, but smaller volume may not justify hardware investment until price point drops)

---

## Discovery Questions (For First Conversations)

### Understanding Current Grading Operations
1. "Walk me through what happens when a returned item arrives at your facility. Who touches it, and what decisions get made at each step?"
2. "How many items per day/week does your team grade? What's your current throughput per grader per hour?"
3. "What does your grading rubric look like? How many grade levels? Is it documented or tribal knowledge?"
4. "What's the cost of a misgrade -- both overgrading (customer complaint) and undergrading (revenue left on table)?"
5. "How do you handle peak seasons (January)? Do you hire temp workers? How long does training take?"

### Understanding Pain Severity
6. "If you could grade 5x faster with the same accuracy, what would that unlock for your business?" (Tests whether throughput is truly the bottleneck)
7. "What's your inter-rater agreement? If you gave the same item to two different graders, how often do they assign the same grade?" (Establishes baseline for comparison)
8. "What's your biggest quality issue right now -- misgrading, slow processing, or something else?"
9. "Have you evaluated any technology solutions for grading? What happened?" (Shows buying intent or reveals past failures)
10. "What would need to be true for you to pilot a grading technology? What accuracy level? What integration requirements?"

### Technical Qualification
11. "What WMS do you use? Is there an API?" (Integration complexity)
12. "Do you have existing photography equipment for your items?" (Potential hardware synergy)
13. "Where does grading data live today -- spreadsheets, WMS, custom system?" (Data availability for model training)
14. "Would you be willing to share 500+ pre-graded items for us to benchmark our AI against?" (Training data access)

### Budget & Decision Process
15. "Who else would need to be involved in evaluating a solution like this?"
16. "What's your typical evaluation timeline for new technology in operations?"
17. "Is there budget allocated for processing technology this year, or would this need a new approval?"

---

## Validation Signals (What "Yes" Looks Like)

### Strong Positive Signals
- Customer shares their grading rubric document (trust, intent)
- Customer offers to provide graded items for benchmarking (active collaboration)
- Customer introduces you to their operations manager on-site (multi-stakeholder engagement)
- Customer asks about timeline/pricing unprompted (buying intent)
- Customer describes specific recent incident where misgrading cost money (acute pain)
- Customer says "we've been looking for something like this" (validated demand)

### Weak/Neutral Signals
- "Interesting, send me more info" (polite dismissal -- follow up but don't count it)
- "We're building something internally" (they recognize the problem but may not buy externally)
- "Come back in 6 months when we have budget" (real timing constraint OR polite no)

### Negative Signals (Disqualify)
- "Our current grading process works fine" (no pain, no sale)
- "We need 99%+ accuracy" (unrealistic bar, perfectionism will prevent adoption)
- "We can't share any items or data" (no way to train customer-specific model)
- "Our CTO wants to build this in-house" (will take 2 years but blocks budget for external)

---

## Outreach Strategy

### Phase 1: Warm Approaches (Weeks 1-4)
1. **LinkedIn connections**: Connect with 20-30 people at target companies (search: "operations" + "returns" OR "recommerce" OR "resale" + company name)
2. **Conference attendance**: Reverse Logistics Association (RLA) conference, NRF (National Retail Federation), Circularity conference by GreenBiz
3. **Content**: Publish 2-3 LinkedIn posts about "the grading problem in recommerce" -- attract inbound interest from people who recognize the pain
4. **Advisor recruitment**: Find 1-2 advisors with direct connections to target companies (ex-ThredUp, ex-Optoro, ex-brand returns leaders)

### Phase 2: Direct Outreach (Weeks 3-8)
1. **Personalized emails** to 10 decision makers, referencing their specific program (Nike Refurbished, Lululemon Like New, etc.)
2. **Demo video**: 60-second video showing the grading station concept (even with prototype/mockup imagery) -- concrete visualization sells better than slide decks
3. **ROI calculator**: One-page spreadsheet showing their specific savings (input: items/day, current graders, hourly cost -> output: annual savings with AI station)
4. **Offer**: "We'll grade 200 of your items for free and compare to your human grades. No commitment."

### Phase 3: Pilot Conversion (Weeks 6-16)
1. Free benchmarking test (receive items, grade them, present results vs. their human baseline)
2. If accuracy meets threshold: propose 30-day pilot with 1 station on-site
3. Pilot terms: $5,000 flat fee for 30 days (covers hardware + on-site support). Success criteria agreed upfront.
4. Pilot success -> 1-year SaaS contract + additional stations

---

## Expected Timeline to First Revenue

| Milestone | Target Week | Confidence |
|-----------|-------------|-----------|
| 10 discovery calls completed | Week 4 | HIGH (people will talk about their problems) |
| 3 companies express pilot interest | Week 8 | MEDIUM |
| 1 benchmarking test completed | Week 12 | MEDIUM |
| 1 pilot agreement signed | Week 16 | MEDIUM-LOW |
| First pilot deployed | Week 22 | MEDIUM-LOW |
| First recurring SaaS revenue | Week 26-30 | LOW-MEDIUM |

**Honest assessment**: Enterprise sales cycles in logistics/operations are typically 3-6 months from first conversation to signed agreement. The free benchmarking offer accelerates this because it removes risk for the buyer. But expect the first dollar of RECURRING revenue at month 7-8, not month 4-5.
