# Customer Validation: CNC Tool Wear Acoustic Detection

## 1. First 5 Customers to Approach

### Customer 1: Small Aerospace Job Shop (3-8 machines)

**Profile:**
- 5-8 Haas VMCs (VF-2, VF-4) running aluminum 6061/7075 and titanium Ti-6Al-4V
- 8-15 employees, $2-5M revenue
- AS9100 certified (aerospace quality standard)
- Located in Southern California, Pacific Northwest, or Texas aerospace corridors
- Running 2 shifts, exploring lights-out on aluminum jobs
- Owner is 45-60 years old, built the business from one machine

**Why they are ideal:**
- Highest pain: titanium parts cost $500-$5000 each in material. One broken tool = one scrapped part = $5K+ loss
- Already quality-conscious (AS9100 requires process monitoring - this helps compliance)
- Can afford $199 + $99/month without blinking (they spend $3-5K/month on tooling already)
- Technical enough to appreciate the product but not so large they need enterprise solutions
- Likely has stories of expensive breakage events (emotional hook for conversation)

**How to find them:**
- Google Maps search: "CNC machine shop" + "aerospace" in San Jose/LA/Seattle/Dallas
- Thomasnet.com: search for AS9100 certified shops with 5-20 employees
- Local aerospace manufacturing associations (SAMPE chapters, NTMA local chapters)

---

### Customer 2: Medical Device Contract Manufacturer (3-6 machines)

**Profile:**
- 3-6 CNC mills + 2-4 Swiss lathes running stainless 316L, titanium, cobalt chrome
- ISO 13485 certified (medical device quality)
- 5-12 employees, $1-3M revenue
- Located near medical device hubs: Minneapolis, Boston, San Jose, Orange County
- Produces surgical instruments, orthopedic implants, dental components
- Extremely tight tolerances (0.0005" typical), surface finish critical

**Why they are ideal:**
- Part values are very high ($200-$2000 per part in material + machining time)
- Tool wear directly impacts surface finish - they already care about tool condition obsessively
- Regulatory environment rewards process monitoring (FDA likes documented process controls)
- Small enough to be accessible, large enough to afford the product
- Quality-driven culture means they will actually USE monitoring data

**How to find them:**
- Medical device manufacturing directories (MDMA member list)
- ISO 13485 certified shop directories
- LinkedIn search: "CNC" + "medical device" + "owner" or "president"

---

### Customer 3: YouTube/Instagram CNC Creator with Job Shop

**Profile:**
- 2-5 machines (likely Tormach, Haas Mini Mill, or Datron)
- Runs a job shop AND creates CNC content (5K-100K followers)
- 30-45 years old, technically sophisticated, early adopter mentality
- Revenue from both machining jobs and content/sponsorships
- Examples of archetype: Titans of CNC (too big), NYC CNC (now Datron, too big), but smaller creators like "Edge Precision", "Abom79", "Stefan Gotteswinter" tier

**Why they are ideal:**
- Will create content about the product (free marketing worth $10K-$50K in equivalent ad spend)
- Early adopter mentality - willing to try new tech, tolerant of beta bugs
- Audience of exactly our target customers (small shop owners who watch CNC YouTube)
- Provides authentic third-party validation
- Fast feedback cycle (they will tweet/post about problems immediately)

**How to find them:**
- YouTube search: CNC machining channels with 5K-50K subscribers who also run a job shop
- Instagram: #cncmachining #cncmill #machineshop with business accounts
- Direct DM with offer of free unit in exchange for honest review content

---

### Customer 4: Owner-Operator Solo/Duo Shop (1-3 machines)

**Profile:**
- 1-3 machines (Haas Mini Mill, Tormach 1100M/770M, or used Haas VF-2)
- 1-2 employees (owner + maybe one helper)
- Revenue $200K-$800K/year
- Garage shop or small industrial unit
- Running general job work (automotive, hobby, prototyping)
- Owner does everything: quoting, programming, machining, shipping

**Why they are ideal:**
- MOST price-sensitive (validates that $199 + $99/month works for smallest shops)
- Cannot afford to be at the machine 100% of the time (doing admin, quoting, shipping)
- Highest anxiety about unattended machining (one breakage event can be month's profit)
- If product works for them, it works for everyone above them in size
- Fastest decision maker (owner says yes, done - no procurement process)

**How to find them:**
- Reddit: r/Machinists, r/CNC, r/hobbycnc (filter for people running commercial work)
- Practical Machinist forums (most active CNC forum, many owner-operators)
- Local makerspace networks (some members graduate to commercial shops)
- Facebook groups: "Haas CNC Owners", "Tormach Owners Group"

---

### Customer 5: Multi-Machine Production Shop Starting Lights-Out (8-15 machines)

**Profile:**
- 8-15 CNC machines (mix of mills and lathes, likely Haas-heavy)
- 15-30 employees, $3-10M revenue
- Running 2 shifts staffed, exploring 3rd shift unattended
- Aluminum and steel production work (automotive, consumer products)
- Shop foreman or production manager is key decision maker (not owner)
- Located in Midwest manufacturing belt (Ohio, Michigan, Indiana, Wisconsin)

**Why they are ideal:**
- Transitioning to lights-out is the #1 trigger for buying tool monitoring
- Can deploy across 8-15 machines (validates volume pricing and multi-machine dashboard)
- Has budget for tooling/equipment improvements ($5K-$20K discretionary per quarter)
- Production environment provides consistent data for ML training (same parts, same tools)
- If successful, becomes case study for "lights-out machining made safe" messaging

**How to find them:**
- NTMA (National Tooling and Machining Association) member directory
- Modern Machine Shop magazine readership / website forums
- LinkedIn: "production manager" + "CNC" + "lights out" or "unattended"
- Trade shows: IMTS (too big/rare), but regional shows like EASTEC, WESTEC, HOUSTEX

---

## 2. Discovery Questions

### Opening (Establish Pain):
1. "When was the last time a tool broke unexpectedly on one of your machines? What happened? What did it cost you?"
2. "How do you currently decide when to change a tool? Fixed schedule, operator judgment, or something else?"
3. "Do you run any machines unattended? If not, what is stopping you?"
4. "How much do you estimate you spend per year on scrapped parts from tool failures?"
5. "Have you ever looked at tool monitoring systems like Montronix or Caron Engineering? What stopped you from buying one?"

### Problem Validation (Confirm Assumptions):
6. "If you could know 60 seconds before a tool was about to break, what would you do differently?"
7. "How many unexpected tool breakage events do you have in a typical month?"
8. "Which operations worry you most? (roughing aluminum, finishing titanium, drilling deep holes, etc.)"
9. "Do your experienced machinists listen for problems? What do they listen for?"
10. "When a machinist is at lunch or in the bathroom, what happens if a tool starts to fail?"

### Solution Validation (Test Our Approach):
11. "If there was a device you could stick to your machine with a magnet, plug in, and it would text you when a tool is about to break - would you use it?"
12. "What would it need to do for you to trust it enough to walk away from the machine?"
13. "How much would you pay per machine per month for something that prevented even one breakage event per year?"
14. "Would you want it to automatically stop the machine, or just alert you?"
15. "How important is it that it works without internet? (e.g., if your shop WiFi goes down)"

### Pricing Validation:
16. "If the hardware was $199 and the monitoring service was $99/month, would that be a no-brainer, reasonable, or too expensive?"
17. "Would you prefer to pay more upfront ($500) with a lower monthly ($49/month), or lower upfront with higher monthly?"
18. "At what price point would you put one on every machine? At what price would you put one on your most critical machine only?"

### Competitive/Alternative Validation:
19. "Have you tried using spindle load monitoring on your control? How well does it work?"
20. "Do you know anyone who has Montronix or similar? What do they think of it?"

---

## 3. Demand Signals (What Confirms Interest)

### STRONG Signals (Proceed with Confidence):

| Signal | What It Looks Like | Why It Matters |
|--------|-------------------|----------------|
| Unprompted story telling | Customer launches into a 5-minute story about a specific breakage event without being prompted | Emotional pain is real and top-of-mind |
| Asks "when can I get one?" | Before you have finished explaining the product, they ask about availability | Active demand, not just polite interest |
| Offers to be beta tester | Volunteers their shop, their machines, their time | Willing to invest time = real pain |
| Asks about pricing unprompted | "How much would something like this cost?" before you mention price | Already mentally purchasing |
| Pulls out wallet / asks for invoice | Literally tries to buy it during the conversation | Obviously |
| Tells other shop owners about it | Forwards your info to friend who also runs a shop | Organic referral = genuine excitement |
| Describes specific scenario | "Last month I had a $8K titanium part scrapped because I was on the phone when the tool went" | Specific, recent, quantifiable pain |

### MODERATE Signals (Encouraging but Needs More Validation):

| Signal | What It Looks Like |
|--------|-------------------|
| Nods along, says "that would be nice" | Polite interest, not burning pain. May buy at $49/month but not $99. |
| Asks many technical questions | Curious but may be tire-kicker or engineer who never buys. |
| "Send me info when it is ready" | Delaying tactic. May convert later but not a beta candidate. |
| Compares to spindle load monitoring | Thinking about alternatives - need to differentiate clearly. |

### WEAK/NEGATIVE Signals (Re-evaluate Assumptions):

| Signal | What It Looks Like | What It Means |
|--------|-------------------|---------------|
| "I can hear when something is wrong" | Trusts their ears more than technology | May not be early adopter; revisit when they retire or hire less experienced operators |
| "My tools last a predictable amount" | Running production, not job shop | Wrong customer segment (they already know tool life from repetition) |
| "$99/month is too much for me" | Price sensitivity | May need cheaper tier, or wrong customer segment (too small) |
| "I would need to see data proving it works" | Skepticism about ML/acoustic approach | Need case study / pilot results before these customers convert |
| "I had one of those monitoring systems, it gave too many false alarms" | Bad experience with Montronix or similar | Huge insight - false positives kill trust. Must solve this. |

---

## 4. Cold Outreach Plan

### Where CNC Shop Owners/Operators Hang Out:

**Online Communities (Highest Density, Lowest Cost):**
1. **Practical Machinist Forum** (practicalmachinist.com) - THE forum for professional machinists. 500K+ members. Active daily. Post in "CNC Milling" subforum.
2. **Reddit: r/Machinists** (~80K members) - younger demographic, more open to new tech
3. **Reddit: r/CNC** (~50K members) - mix of hobby and professional
4. **Facebook Groups:** "Haas CNC Owners" (15K+), "CNC Machinist Network" (50K+), "Tormach Owners" (5K+)
5. **Instagram: #cncmachining** - visual platform, good for demo videos
6. **YouTube CNC community** - comments on popular CNC channels, sponsor smaller creators
7. **CNCZone.com** - older forum, still active for specific technical questions

**In-Person (Highest Conversion, Highest Cost):**
1. **Local NTMA chapter meetings** - monthly meetups of shop owners in most metro areas
2. **Regional trade shows:** EASTEC (New England), WESTEC (California), HOUSTEX (Texas), SOUTHTEC (Southeastern US) - smaller than IMTS, more accessible
3. **IMTS 2026** (September, Chicago) - 100K+ attendees, every CNC shop owner goes. Expensive but massive reach.
4. **Haas Demo Days** - Haas HFOs (Haas Factory Outlets) host events; their customers are our customers
5. **Local makerspace CNC classes** - find graduates who started commercial shops
6. **Community college machining programs** - instructors know every local shop

**Industry Media:**
1. **Modern Machine Shop** (magazine + website) - THE trade publication. Guest article or product announcement.
2. **Production Machining** - focused on production shops
3. **Machining Cloud** - digital tool library; partner for tool wear data
4. **Titans of CNC Academy** - education platform, potential partnership for reach

### Outreach Strategy (First 30 Days):

**Week 1-2: Online Community Immersion (Cost: $0, Time: 10 hrs)**
- Create accounts on Practical Machinist and Reddit (if not existing)
- Post genuine question: "Curious how shops here handle tool wear monitoring. Running a few VMCs and tired of replacing tools on schedule. Anyone tried acoustic monitoring or load-based systems? What worked/failed?"
- Goal: Learn the language, identify pain points, find potential beta candidates from responses
- DO NOT pitch product. Listen only.

**Week 2-3: Direct Outreach to 20 Shops (Cost: $0, Time: 15 hrs)**
- Identify 20 shops within 2-hour drive using Google Maps + Thomasnet
- Cold email template:

```
Subject: Quick question about tool breakage in your shop

Hi [Name],

I am an engineer building a low-cost tool wear detection system for CNC shops. 
Think of it as a $200 device that listens to your cutting and texts you before 
a tool breaks - kind of like what Montronix does but 100x cheaper.

I am looking for 3-5 shops to test early prototypes in exchange for free hardware 
and 12 months free service. No obligation, no risk - I just need real machines 
to validate the technology.

Would you be open to a 15-minute chat about whether this would be useful in your shop?

Best,
[Name]
[Phone]
```

- Send via email (find on shop websites) or LinkedIn InMail to owners
- Expected response rate: 10-15% (2-3 responses from 20 outreach)

**Week 3-4: YouTube/Instagram Creator Outreach (Cost: $0-500, Time: 8 hrs)**
- Identify 10 CNC YouTube creators with 5K-50K subscribers who run job shops
- DM on Instagram or email:

```
Subject: Free tool monitoring device for your shop (content opportunity?)

Hey [Creator Name],

Love your channel, especially [specific video reference]. 

I am building a device that uses MEMS microphones + ML to detect tool wear 
acoustically - think predictive maintenance for $200 instead of $50K.

Would you be interested in trying a prototype in your shop? I would send you 
the hardware for free, no strings attached. If you find it useful and want to 
make a video about it, that would be amazing - but no obligation.

I am looking for honest feedback from experienced machinists, not paid endorsements.

[Name]
```

- Expected response rate: 20-30% (creators love free products to review)

**Week 4: Follow-Up and Schedule Visits (Cost: $200 gas/food, Time: 20 hrs)**
- Schedule shop visits with all interested parties
- Bring validation rig (even if not pretty - machinists respect function over form)
- Run discovery questions during visit
- Goal: 3-5 committed beta partners by end of Week 4

### Outreach Metrics to Track:

| Metric | Target (30 days) |
|--------|------------------|
| Cold emails/DMs sent | 30 |
| Response rate | >10% |
| Discovery calls completed | 5-8 |
| Shop visits completed | 3-5 |
| Committed beta partners | 3 |
| "Send me one when it is ready" list | 10+ |
| Unprompted referrals received | 1-2 |

### Channels to AVOID (Low ROI for Early Stage):
- Paid Google/Facebook ads (too early, no product to sell yet)
- Trade show booths (too expensive, $5K-$20K for booth)
- Print magazine ads (expensive, unmeasurable)
- Cold calling (shop owners hate phone calls during working hours)
- Distributor partnerships (too early, they want proven products with margin)
