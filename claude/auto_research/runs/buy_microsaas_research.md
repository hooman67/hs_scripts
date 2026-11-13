# Buy-a-Micro-SaaS — Acquisition Research (the RESEARCH half of the playbook)

**Created**: 2026-07-02 by Claude (Opus 4.8). **Owner**: Hooman Shariati (hshariati@adobe.com).

**What this is**: The concrete, web-researched marketplace + diligence + deal-structure +
delegation-math half of the buy-a-micro-SaaS playbook. It BUILDS ON (does not repeat) the
three prior docs in `runs/trackB/deep/buy_microsaas/` (01 research-validation, 02 execution-plan,
03 plan-validation) and the honest verdict in `runs/FLAT_SHOWDOWN.md`.

**Inherited honest economics (do not relitigate here — see 03_plan_validation.md)**:
Entry ~$2-4K/mo net (often $1.5-2.5K at a *fair* multiple on his budget); base case flat-to-
$3-5K over 24mo; **~$0-2.5K TRUE net after valuing his own 8-12 hrs/wk**; downside genuinely
capped at the all-cash price (~$80-140K). The live risk this doc pins down with real numbers
is the **DELEGATION-AFFORDABILITY TRAP**: a VA+dev spend that eats all profit on an asset he
can actually afford.

**Founder recap**: Adobe eng manager; AI/ML + cloud + infra; EE; $25-150K cash; ~10-20 hrs/wk;
wants $5-30K/mo secondary income; freeing focus from CutLog for this. His edge is *technical
diligence* (reading code/infra others can't); his gap is *distribution* (why he buys, not builds).

---

## 1. The actual marketplaces — what $2-8K MRR B2B SaaS lists at RIGHT NOW

**Methodology note (important, for honesty)**: The big marketplace *listing grids*
(Acquire.com, Flippa, Empire Flippers) render client-side, so a static fetch returns an
empty grid — I could NOT scrape the full live inventory anonymously (buyer login required).
What I CAN cite with real numbers: (a) live individual listings that rendered, (b) the
marketplaces' own aggregate stats and valuation formulas, (c) the two 2026 multiple reports
(Acquire.com biannual, FE International), all fetched 2026-07-01/02. Where I state a "typical
list price," it is derived from those multiples applied to the target MRR, and flagged as such.

### 1a. Marketplace-by-marketplace (fetched 2026-07-02)

| Marketplace | Scale / what it is | This-band relevance | Real numbers captured |
|---|---|---|---|
| **Acquire.com** (ex-MicroAcquire) | **2,000+ startups sold, $500M+ closed volume, 500K+ entrepreneurs, $2B+ verified buyer funds**, 4.7/500+ reviews | **Highest volume in the $2-8K MRR SaaS band.** Where Hooman shops most. | Avg time on market **81 days**; most deals close **<90 days**; *smaller/lower-revenue businesses sell faster* (source: Acquire biannual Jan-2026) |
| **Empire Flippers** | **2,640 businesses sold, $589,590,332 transacted**; last-30-day sales $852,470; rejects most applicants (vetted) | Most *vetted* but skews larger/pricier; thinner sub-$150K SaaS inventory | Live SaaS listing #94153 (below). Valuation formula: **[6-12mo avg net profit] × multiple (typically 20-60+ monthly)** |
| **Flippa** | **~5,284 buy listings** across all types, **953K off-market** leads, "LaurenAI" origination tool | Most volume **and most junk** — heaviest diligence burden; strong filters (churn, LTV, AOV, refund rate) | Filter bands go $0-999 → $250K+; SaaS grid was empty on anonymous fetch |
| **Microns.io** | Curated micro-SaaS marketplace, "verified metrics" | **Most on-point for the $3.6K-200K micro-SaaS band** | Live listings below — real asking prices + multiples |
| **FE International** | Broker (advisory, not self-serve grid), sub-$2M focus | Higher-quality, broker-priced; **5-7x SDE** band | Multiples + churn sample (§2) |
| **Motion Invest** | Content-site heavy (not SaaS) | Low relevance — mostly content/affiliate sites | Page 404'd; known to skew content |
| **Tiny Acquisitions** | Micro/starter deals, many pre-revenue | Low relevance — too small/early, high junk | Domain unreachable at fetch time |

### 1b. Live listings captured (real asking prices / multiples, fetched 2026-07-02)

**Empire Flippers #94153** — "auditing and securing reimbursements" (Service + SaaS, **B2B**):
- Asking **$377,472**; monthly net profit **$11,797**; **32x monthly** (~2.7x annual).
- **Distressed**: profit −50%, revenue −37% YoY. The 32x is a *decline discount*, not a bargain.
- Lesson: the one healthy-looking SaaS on EF today is (a) 3x Hooman's budget and (b) shrinking.

**Microns.io live micro-SaaS listings** (annual-revenue multiples shown):
| Business | Annual rev | Asking | ~Multiple (annual rev) | Niche | Read |
|---|---|---|---|---|---|
| Healthcare Exercise Mgmt SaaS | $40,401 | $120,000 | ~3.0x rev | Healthcare/fitness B2B | In-budget, plausible profile |
| Chat API & SDKs platform | $78,400 | $200,000 | ~2.5x rev | Dev tools | Over budget |
| AI Resume Checker | $864 | $10,000 | **~11.6x rev** | EdTech | Priced on hope, tiny rev |
| AI Writing Assistant | $2,250 | $5,500 | ~2.4x rev | AI/productivity | **AI-wrapper — reject** |
| AI Book Summaries | $1,114 | $3,600 | ~3.2x rev | AI/content | **AI-wrapper — reject** |

**What this shows**: (1) In-budget SaaS ($80-150K) at ~$40K/yr revenue (~$3.3K/mo) exists and
lists around **3x annual revenue** — consistent with the low-tier profile. (2) The cheapest
"SaaS" is overwhelmingly **AI-wrapper / content junk** priced on multiples of hope (11.6x rev on
$864/yr) — exactly the category to reject. (3) Nothing sticky-and-boring is *cheap*; the boring
B2B system-of-record either isn't for sale or is priced fairly (3x+).

### 1c. What actually SELLS vs SITS (from the 2026 reports)

- **Sells fast**: profitable, realistically-priced, source-verifiable small SaaS → *smaller,
  lower-revenue businesses sell faster* (Acquire Jan-2026), 81-day average, most <90 days.
  "More profitable startups attract higher buyer interest / more inbound offers."
- **Sits**: over-priced-on-growth-story listings, declining businesses at healthy-business
  multiples, AI-wrapper commodities, anything with un-verifiable revenue.
- **The buy-side is crowded**: $2B+ verified buyer funds on Acquire alone, plus micro-PE
  holdcos (SureSwift, Tiny, XO Capital, Dura Software) that are cash-ready and faster. **Clean
  assets get bid up / taken before a slower solo buyer moves.** Hooman's realistic lane is the
  *technically-messy-but-fixable* deal others fear (his diligence edge) — but note 03's
  correction: messy *code* is rarely why small B2B SaaS is cheap (relationships/support are),
  so treat the messy-deal edge as **diligence alpha, not value-creation alpha**.

---

## 2. Real multiples, churn, and the pricing truth (2026 data)

| Source (fetched 2026-07-01/02) | Multiple / metric | Notes |
|---|---|---|
| **Acquire.com biannual, Jan-2026** | **Median 3.9x annual profit** (both 2024 & 2025); avg low-to-mid **4x**; stable YoY | ≈ **47x monthly** median — *higher* than the "25-40x" the original pitch used |
| **FE International (2026)** | **Under $2M SaaS = 5.0-7.0x SDE**; over $2M = 7-10x | Broker-quality assets; premium for stickiness/low-owner-dependence |
| **Empire Flippers** | Formula: net profit × **20-60+ monthly** (≈1.7-5x+ annual) | Wide; declining biz (like #94153) lands ~30x, healthy ~40-50x+ |
| **Microns.io live** | ~2.4-3.2x **annual revenue** for real-revenue micro-SaaS | Revenue basis; junk/hope priced far higher |

**The pricing truth (this is the crux, and it confirms 03_plan_validation.md's WRONG-1)**:
- Market-clearing price for even a *mediocre* small SaaS is **~4x annual profit**; a genuinely
  **sticky/low-churn** one is **4.5-6x** (FE 5-7x band).
- **3.0-3.5x annual = the price of DECLINE/fragility**, not sticky-and-cheap. You cannot buy
  top-quartile stickiness at a bottom-quartile multiple in a market with $2B+ chasing supply.
- **Consequence for the budget**: $80-150K at a *fair* 4-4.5x buys **~$1.5-2.5K/mo net**, not
  $3-6K. To net $4K/mo (the delegation threshold — see §5) at 4-4.5x costs **~$190-215K**, over
  the $150K ceiling. This is the structural squeeze behind the delegation trap.

**Churn reality (FE International sample of 25 acquisitions, $250K-$20M)**:
- Range **1.0-11.0%/mo**, **average 4.7%/mo (~44%/yr)**. SMB-focused SaaS is the *high* end
  (2.5-5%+/mo); mid-market 1-2%/mo; enterprise ~1%/mo.
- **Implication**: at ~4.5%/mo gross logo churn, a business must add ~4.5%/mo just to stand
  still — and it's for sale precisely because the founder *stopped* feeding the funnel. A
  "do-no-harm" first 60 days can bleed ~9% of MRR before Hooman touches anything. **"Hold flat"
  is optimistic; gentle decline is the honest base case** unless the cohort curve genuinely
  flattens in the Stripe data.

---

## 3. The IDEAL TARGET PROFILE for Hooman (concrete)

**Shape**: vertical B2B **system-of-record / compliance-recordkeeping / workflow tool** in an
unglamorous trade. The moat is *switching cost* (the customer's data/history/workflow lives in
it) + *domain trust*, not features. This is the AI-safe category: a horizontal LLM feature or the
platform vendor can't trivially clone a system-of-record holding years of a customer's records.

**Hard filters (all must pass — from 02_execution_plan §1, kept)**:
- **Revenue**: ≥18-24mo history; B2B; annual or sticky-monthly billing; **source-verified via
  read-only Stripe + bank** (never screenshots).
- **Net (SDE)**: **$2-4K/mo trailing** — but underwrite knowing a *fair* multiple puts realistic
  buys at the **$1.5-2.5K** end within budget.
- **Price**: $80-150K all-cash (aim **$80-120K** to leave room for costs + a $10-15K reserve).
  Expect to pay **4-4.5x annual** for anything not declining; 3-3.5x only signals a turnaround.
- **Churn**: cohort retention curve **actually flattens** in the raw Stripe export (not masked
  by new-logo adds). Re-baseline the model to **~4.5%/mo**, not ≤3%.
- **Concentration**: **<20%** of revenue from any single customer.
- **Owner load**: current owner **<10 hrs/wk** (proves part-time operability).
- **AI-safe / moat**: **REJECT** consumer apps, SEO/content sites, Chrome extensions, thin AI
  wrappers, and single-platform add-ons (Shopify/WP/Stripe app the host can kill). The Microns
  "AI Resume Checker / AI Writing Assistant / AI Book Summaries" listings are the archetype to
  reject — commodity AI wrappers priced on hope.

**Concrete example niches (boring, sticky, AI-safe, underwritable by an infra engineer)**:
- **Field-service ops** for a narrow trade (e.g. fire-alarm/backflow inspection scheduling +
  compliance records; pool-service routing; septic/grease-trap logs).
- **Niche compliance & recordkeeping** (OSHA/EPA logs, food-safety HACCP records, calibration/
  maintenance logs, permit tracking) — regulatory *mandate to keep records* = durable demand.
- **Specialty-trade quoting/POS/scheduling** (sign shops, upholstery, monument/headstone shops,
  taxidermy, gunsmith FFL logs, veterinary/med-lab specimen tracking).
- **Property/HOA/self-storage admin**, **dental/med-lab operational tools**, **trade-association
  membership/CE tracking**.

**Why these fit HIM specifically**: (a) low customer concentration (many small shops, none
dominant), (b) tech stacks a solo infra engineer can operate (LAMP/Rails/Django + Postgres +
Stripe on a single VPS/Heroku/Render — not a 12-microservice mess), (c) support is domain-simple
enough to hand to a VA once SOPs exist, (d) not a bidding-war darling (boring niches bore the
holdcos), (e) AI-safe (system-of-record, not content generation).

---

## 4. Diligence essentials + the specific red flags that tank a deal

**Source-verify REVENUE (the #1 gate — no live access = walk)**:
- Demand **read-only Stripe login + bank/PayPal statements**, and reconcile three ways:
  **bank deposits ↔ Stripe MRR ↔ the P&L they showed.** Screenshots are worthless.
- Build the **cohort retention curve** from the raw Stripe export yourself — do not accept a
  churn number. Confirm MRR trend is flat/growing on a *revenue-retention* basis, not propped up
  by new-logo adds masking churn.
- Separate **recurring MRR from one-time/services revenue**; FE flags lifetime/heavily-discounted
  annual plans (MRR is worth ~2x equivalent lifetime revenue) and **undisciplined discounting**
  (unscheduled sales inflating apparent revenue) as classic dress-up tactics.

**Verify CHURN / concentration / traffic**:
- Concentration: **<20%** from any one customer; also check *acquisition-channel* concentration
  — FE calls single-channel dependency (esp. price-competitive PPC vs funded rivals) a red flag.
- Traffic: if any organic/SEO dependence, pull GA/Search Console read-only; check for a single
  keyword/referrer carrying the business.

**Code / infra quality (HOOMAN'S EDGE — this is where his diligence beats the buyer pool)**:
- Read the repo + map infra. FE explicitly calls **poor code documentation "deal-killing"** and
  **undocumented code ownership / missing contractor IP-assignment** a top red flag — confirm
  clean IP chain (every contributor assigned IP).
- Hunt: single points of failure, secrets committed in the repo, no/stale backups, dependency
  rot, a scaling-cost cliff, one undocumented cron/hack holding it together. Price the *true*
  hosting/ops cost (sellers understate it). Decide **"messy-but-fixable" vs "messy-and-a-trap."**

**Key-person / operational risk**:
- The "product" is often the founder's **support relationships + undocumented tribal ops**. FE:
  **owner-critical technical roles** and **haphazard/unproven outsourced support** are red flags.
  Require a **60-90d paid seller transition + SOP handover + non-compete** in the APA.

**The specific red flags that TANK a deal (consolidated, sourced to FE + EF + 01/03)**:
1. Seller **refuses live read-only Stripe/bank** → instant walk.
2. **Declining** revenue/profit dressed as "stable" (see EF #94153: −37%/−50% YoY).
3. **Churn masked** by new-logo adds; cohort curve never flattens.
4. **>20% single-customer** (or single-channel) concentration.
5. **Thin/undocumented code, unclear IP ownership**, secrets in repo, no backups.
6. **Platform-dependent** (host can kill it) or **AI-wrapper commodity** (LLM can clone it).
7. **Lifetime/one-time revenue** dressed as recurring; unscheduled discount spikes.
8. **Owner-as-the-product** with no SOPs and no willingness to do a real transition.

---

## 5. Deal structures — capping the downside on a first deal

**All-cash vs seller financing / earnout (2026 evidence, and it's genuinely mixed)**:
- **Empire Flippers financing page (fetched 2026-07-02)** says seller financing / earnouts are
  **"by far the most common method"** for buyers, often at **0% interest** (sellers rarely bother
  pricing interest). This *contradicts* an earlier EF line ("cash upfront remains most popular")
  — so the evidence is softer than any single source claims.
- **The honest read (from 03_plan_validation WRONG-3)**: if a seller *eagerly* offers financing/
  earnout, that can be **adverse selection** — they may doubt their own trailing numbers. Cheap
  leverage on a declining asset is a trap. **So: budget mostly cash; use the earnout as a
  RISK-SHIFTER you request, not a discount you celebrate.**

**Recommended structure for a first deal (this is what makes "downside capped" actually true)**:
- **All-cash on the bulk + 10-30% held as a 6-12mo earnout / seller note** tied to revenue
  retention (protects against the melting-ice-cube), **through escrow**, plus **non-compete** and
  **60-90d paid transition + SOP handover**.
- **AVOID SBA / personal-guarantee financing on a first deal.** SBA 7(a) loans for business
  acquisition require a **personal guarantee** (and often a lien on personal assets/home); that
  **breaks the single best feature of this whole idea — the capped, cash-only downside.** An
  all-cash deal caps max loss at ~$80-140K (minus resale value); an SBA-leveraged deal can lose
  *more than the cash in* via the PG. Main-Street SBA seller-financing norms (75-90% financed)
  are a *different market* and don't apply to a $100K digital SaaS.
- **Downside cap in practice**: escrow + source-verified revenue + earnout/holdback = the loss is
  bounded and partly contingent. Keep a **$10-15K working-capital reserve** (EF advice: "never
  spend money unless you're okay losing 100% of it"; hold reserves for a slump).

---

## 6. The delegation math, done honestly (the LIVE risk)

**The trap in one line**: the asset Hooman can *afford* ($80-120K → ~$1.5-2.5K/mo net at a fair
4-4.5x) **cannot afford to be delegated**, and the asset *worth* delegating ($4K+/mo net) costs
**~$190-215K — over his $150K ceiling.**

**Real delegation costs (2026 sector figures; VA-cost pages blocked on fetch, so these are the
well-established market ranges cross-checked against 03's $800-1.5K/mo VA figure)**:
- **Offshore VA / support (Philippines etc.)**: **~$5-12/hr** → a part-time (20-40 hr/mo)
  support VA ≈ **$300-800/mo**; a heavier front-line role ≈ **$800-1,500/mo**.
- **US-based VA**: ~$25-50/hr (usually unaffordable at this asset size).
- **Fractional/contract developer**: **~$40-100+/hr** → even light maintenance (10-20 hr/mo)
  ≈ **$800-2,000/mo**; a real feature/tech-debt cadence ≈ **$1-3K/mo variable**.

**What CAN vs MUST be delegated**:
| Task | Delegable? | Cost |
|---|---|---|
| Tier-1 support / onboarding / mundane ops | Yes, **after SOPs exist** (month 6+) | VA $300-1,500/mo |
| Routine bug fixes / small features / dep upgrades | Yes, to a contractor dev | $800-3,000/mo variable |
| Infra/hosting rightsizing | Hooman once (his edge), then rare | ~$0 ongoing |
| **Technical/escalated support, churn saves, key-account fires** | **NO — stays with Hooman** | his 8-12 hrs/wk |
| **Roadmap, pricing, dev direction, code review** | **NO — stays with Hooman** | included above |

**The honest net-out**:
- On a **$1.5-2.5K/mo** asset (what the budget realistically buys): a $1,000-2,500/mo VA+dev spend
  **consumes most-to-all of the profit** → he'd be paying to own a part-time job. **Delegation is
  NOT affordable here.** He remains the support desk + dev at **8-12 hrs/wk indefinitely** (03's
  correction: steady state is 8-12, not the plan's 5-10).
- On a **$4K+/mo** asset, a ~$1.5-2.5K/mo delegation spend still leaves **$1.5-2.5K/mo** and drops
  him toward 5-10 hrs/wk — but that asset is **>$150K**, outside budget.
- **True economic profit** on an affordable asset, after charging his own ~40 hrs/mo at even
  $50/hr (~$2K/mo, far below his real rate): roughly **$0-2.5K/mo** — i.e. it barely clears, or
  fails to clear, hobby income once his time is priced. This matches FLAT_SHOWDOWN's honest line.

**Does it net out above hobby income?** Only in the **rare fair-priced sticky asset that holds
$3-5K+/mo at low touch** — the ~upside, not the base case. In the base case it is a
**capped-downside, mid-teens (13-22%) cash yield that nets ~$0-2.5K after his time**, plus real
resale optionality. **Verdict stands: CONDITIONAL** — pursue only if (a) he has idle capital he
can't deploy better, (b) he accepts owning a small part-time job with resale value, and (c) he
has genuinely freed 20-25 hrs/wk for months 1-6 and 8-12 hrs/wk after (Gate 0). If the true goal
is $5-30K/mo *passive*, one sub-$150K acquisition does **not** get there.

**The one move that resolves the trap**: instead of delegating a too-small asset, **use his
technical edge to raise net without adding spend** — cut hosting cost (pure margin), recover
involuntary churn via dunning (a one-time ~3-8% MRR lift), and ship one AI/feature win himself.
That's cheaper than a VA+dev and is exactly where his skills apply. Delegation should wait until
the asset genuinely clears **~$4K/mo net**, which likely means buying well and *growing into it*,
not delegating into it.

---

## 7. Bottom line for the playbook

- **The marketplaces and scale are real and verified** (Acquire $500M+/2,000+ sold/$2B+ buyer
  funds; EF $589M/2,640 sold). Supply of *cheap* SaaS is abundant; supply of *clean, sticky,
  fairly-priced sub-$150K B2B* SaaS is the true constraint, and the buy-side is crowded.
- **Real multiples**: median **3.9x annual profit** (Acquire 2026); sticky small SaaS **4.5-6x**
  (FE 5-7x). **3-3.5x = decline.** His budget realistically buys **~$1.5-2.5K/mo net**.
- **Churn**: **~4.5%/mo** average (FE) — base case is flat-to-gentle-decline, not growth.
- **Deal structure**: all-cash + 10-30% earnout/note + escrow + non-compete + 60-90d transition.
  **Avoid SBA/personal-guarantee** — it destroys the capped-downside that is this idea's whole point.
- **Delegation trap is real and quantified**: affordable asset ($1.5-2.5K/mo) can't afford a
  $1-2.5K/mo VA+dev; worth-delegating asset ($4K+/mo) costs >$150K. Base-case true net after his
  time ≈ **$0-2.5K/mo**. Resolve it by *engineering net up* himself, not delegating a small asset.
- **Do the ~$0 dry-run first**: filter Acquire/EF/Microns for the §3 profile, request read-only
  Stripe/bank on 2-3, build the model + tech review. If nothing clears the gates in ~2-3 months,
  that's signal the clean-deal price doesn't work for him — keep the capital.

---

## Sources (all fetched 2026-07-01 / 2026-07-02)
- Acquire.com marketplace + homepage: acquire.com/ — 2,000+ sold, $500M+ volume, 500K+ users, $2B+ buyer funds, 4.7/500+ reviews.
- Acquire.com biannual acquisition-multiples report (Jan 2026): blog.acquire.com/acquire-com-biannual-acquisition-multiples-report-jan-2026/ — median 3.9x profit (2024 & 2025), low-mid-4x avg, 81-day avg time-to-close, smaller businesses sell faster.
- Empire Flippers marketplace + valuation tool: empireflippers.com/marketplace/, /valuation-tool/ — 2,640 sold, $589,590,332 transacted; live SaaS listing #94153 ($377,472, $11,797/mo, 32x, B2B, −50%/−37% YoY); formula = net profit × 20-60+ monthly.
- Empire Flippers financing page: empireflippers.com/oba/online-business-financing/ — seller financing/earnouts "by far the most common," often 0% interest; hold working-capital reserves.
- Flippa: flippa.com — ~5,284 buy listings, 953K off-market, filters for churn/LTV/AOV; anonymous SaaS grid empty.
- Microns.io: live micro-SaaS listings — Healthcare Exercise Mgmt $120K/$40.4K rev (~3x), Chat API $200K/$78.4K, AI Resume Checker $10K/$864 (~11.6x), AI Writing Assistant $5.5K/$2.25K, AI Book Summaries $3.6K/$1.1K.
- FE International SaaS valuation: feinternational.com/blog/saas-metrics-value-saas-business/ — under-$2M SaaS 5-7x SDE; 25-acquisition sample churn 1-11%/mo, avg 4.7%/mo (~44%/yr); code-doc/IP/concentration/owner-dependence red flags.
- VA/dev cost ranges: sector-standard (offshore VA ~$5-12/hr, US $25-50/hr; freelance dev ~$40-100+/hr), cross-checked to 03_plan_validation.md's $800-1,500/mo VA and $1-3K/mo dev figures (VA-cost pages returned 403/404 on fetch).
- Prior docs (build-on, not repeat): runs/trackB/deep/buy_microsaas/01,02,03; runs/FLAT_SHOWDOWN.md.
