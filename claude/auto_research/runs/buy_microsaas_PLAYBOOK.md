# 90-DAY ACQUISITION PLAYBOOK — Buy a Cash-Flowing Micro-SaaS

**Owner**: Hooman Shariati (hshariati@adobe.com). **Written**: 2026-07-02 by Claude (Opus 4.8).

**What this is**: The concrete, week-by-week execution plan for Hooman to buy ONE vertical-B2B
micro-SaaS. It operationalizes the research in `runs/buy_microsaas_research.md` and the prior
plan/validation (`runs/trackB/deep/buy_microsaas/02_execution_plan.md`, `03_plan_validation.md`).
Read those for the "why"; this is the "do."

**The honest one-line verdict it implements (do not relitigate)**: This is a **capped-downside,
~13-22% gross cash-yield** capital deployment that nets **~$0-2.5K/mo of TRUE profit after his own
time** on the asset his budget can actually buy. It is NOT a $5-30K/mo passive-income machine. It
is worth doing only if (a) he has idle capital he can't deploy better, (b) he accepts owning a small
part-time job with real resale optionality, and (c) he clears **Gate 0** (below). If the true goal
is passive $5-30K/mo, one sub-$150K acquisition does not get there — do the ~$0 dry-run first and be
willing to walk with the capital intact.

---

## GATE 0 — DO THIS BEFORE SPENDING A DOLLAR OR AN HOUR (Day 0, free)

**The single go/no-go question**: *Can Hooman honestly commit **15-20 hrs/wk (realistically 20-25 in
months 1-6, spiking on incidents) AND 8-12 hrs/wk indefinitely thereafter**, for at least 6 months,
without hurting CutLog?*

- If CutLog is mid-crunch (a launch push, a 0→1 grind) → **DEFER the entire thing.** Do not split the
  building hours CutLog needs. This is a scheduling decision, not a deal decision, and deferring is
  the most defensible call per the validation.
- If YES, and he has a genuine calendar window → proceed to Day 1. Keep deal-flow (Days 1-50) running
  passively in the background; only pull the trigger (LOI/close) in a month CutLog has slack.

**Also lock before Day 1**:
- **Pick 1-2 target verticals** he can underwrite credibly (see Ideal Target below). Being a focused,
  fast, confident buyer in a niche beats being a tourist across all of them — it wins the messy deals.
- **Accept the multiple reality**: he will pay **4-4.5x annual SDE** for anything not declining.
  3-3.5x = buying decline. Do not chase the 3x fantasy asset; it doesn't reach a slow solo buyer's inbox.

---

## THE IDEAL TARGET (the Buy Box — every line is a hard filter, not a preference)

| Dimension | Hard filter |
|---|---|
| **Type** | Vertical B2B **system-of-record / compliance-recordkeeping / workflow tool** in an unglamorous trade. Moat = switching cost (customer's data/history lives in it) + domain trust. |
| **Revenue** | ≥18-24mo history; B2B; annual or sticky-monthly billing; **source-verified via read-only Stripe + bank** (never screenshots). |
| **Net (SDE)** | **$2-4K/mo trailing** — but underwrite knowing a fair multiple puts realistic buys at the **$1.5-2.5K/mo** end within budget. |
| **Price** | **$80-120K all-cash** (leaves room for costs + a $10-15K reserve inside the $150K ceiling). Expect **4-4.5x annual** for non-declining. |
| **Churn** | Cohort retention curve **actually flattens in the raw Stripe export** (not masked by new-logo adds). Re-baseline the model to **~4.5%/mo**, not ≤3%. |
| **Concentration** | **<20%** of revenue from any single customer AND no single acquisition channel carrying the business. |
| **Owner load** | Current owner **<10 hrs/wk** (proves part-time operability). |
| **AI-safe / moat** | **REJECT** consumer apps, SEO/content sites, Chrome extensions, thin AI wrappers, single-platform add-ons (Shopify/WP/Stripe app the host can kill). The Microns "AI Resume Checker / AI Writing Assistant / AI Book Summaries" listings are the archetype to reject. |

**Concrete niches (boring, sticky, AI-safe, underwritable by an infra engineer)**: field-service ops
for a narrow trade (fire-alarm/backflow inspection, pool-service routing, septic/grease-trap logs);
niche compliance & recordkeeping (OSHA/EPA logs, HACCP food-safety, calibration/maintenance logs,
permit tracking); specialty-trade quoting/POS/scheduling (sign shops, upholstery, monument shops,
gunsmith FFL logs, vet/med-lab specimen tracking); property/HOA/self-storage admin; trade-association
membership/CE tracking.

**Reframe his edge (per validation WRONG-4)**: Hooman's engineering skill is **diligence alpha
(spotting traps others can't), NOT value-creation alpha.** Small B2B SaaS churns on relationships/
support/domain trust, not ugly code. Do not pay a premium expecting to rerate via a rewrite.

---

## DAYS 1-20 — SETUP + DEAL-FLOW ENGINE (≈$0 spent)

**Goal**: a running, filtered pipeline and a reusable diligence toolkit, so Hooman is a fast buyer.

### Week 1 (Days 1-7) — Accounts + saved searches
- Open **buyer accounts**: **Acquire.com** (highest volume in the $2-8K MRR SaaS band — shop here
  most), **Empire Flippers** (most vetted, priced higher), **Flippa** (most volume + most junk),
  **Microns.io** (curated micro-SaaS, on-band). Verify buyer status where required (EF/Acquire gate
  contact info behind verification).
- **Exact saved-search filters** (apply on every marketplace that supports them):
  - Category/type: **SaaS** (exclude content, ecommerce, agency, app, newsletter).
  - Price band: **$75K-$160K** (buy in the $80-120K sweet spot; upper edge catches negotiable deals).
  - Monthly net profit: **$2,000-$5,000** (Flippa/EF expose "net profit"; on Acquire filter by TTM
    profit / revenue and read the P&L).
  - Age/history: **≥18 months** ("established"/"18+ mo" filters where available).
  - Business model: **B2B**, subscription/recurring; on Flippa set **churn, LTV, AOV** filter columns
    visible so they can be read at a glance.
  - Exclude: AI-wrapper, Chrome extension, single-platform add-on, marketplace/two-sided.
- Set **email alerts** on each saved search so new inventory pushes to him (deal-flow runs passively).

### Week 2 (Days 8-14) — Build the reusable diligence toolkit (his repeat-buyer moat)
- **Financial model spreadsheet**: trailing SDE, MRR trend, self-built cohort retention curve,
  gross logo churn, revenue vs one-time/services split, customer concentration, true hosting/ops cost,
  underwriting at 4.0-4.5x with **zero growth credit**.
- **Code/infra red-flag checklist**: single points of failure; secrets committed in repo; backup story
  (exists? tested?); dependency rot; scaling-cost cliff; the one undocumented cron/hack holding it
  together; clean IP chain (every contributor's IP assigned — FE calls missing IP-assignment a top
  red flag).
- **Standard read-only-access request template**: read-only **Stripe** login, **bank/PayPal** statements,
  **Google Analytics / Search Console**, **hosting console**, **repo**. (No live access = walk.)
- **Killer-questions call script**: why selling; owner hrs/wk; top-5 customers' % of revenue;
  acquisition channel mix; tech stack; who does support today; what breaks at 2x scale.

### Week 3 (Days 15-20) — Start the review routine
- **Deal-flow routine (make it a habit, ~3-5 hrs/wk)**: review **20-30 listings/week** against the
  Buy Box. Reject fast and hard — **90%+ should die on the paper screen.** Log every rejection reason
  in the model (builds pattern memory + speeds future screens).
- By Day 20: a **shortlist of 5-8** that pass the paper screen (GATE 1 — paper screen, free).

**Reality check on supply**: cheap SaaS is abundant; clean, sticky, fairly-priced sub-$150K B2B SaaS
is the true constraint, and the buy-side is crowded ($2B+ verified buyer funds on Acquire + cash-ready
micro-PE holdcos). Expect to review **50-90 listings** across these 20 days to net 5-8 real candidates.

---

## DAYS 20-50 — DILIGENCE FUNNEL: SCREEN → LOI → DEEP DILIGENCE (still ~$0)

**Goal**: take the 5-8 shortlist down to 1-2 finalists via source-verification and the code/infra
audit — Hooman's edge — then submit an LOI on the one that clears.

### Days 20-28 — Seller calls, narrow 5-8 → 3-5 (GATE 1 confirm)
- Sign NDAs; run the killer-questions call on each shortlisted deal. Reject on any Buy-Box miss.
- Shortlist to **3-5** worth requesting live access.

### Days 28-42 — Source-verification on top 2-3 (GATE 2 — the #1 gate, free)
**Revenue source-verify (no live access = instant walk):**
- Get **read-only Stripe + bank/PayPal statements** and **three-way reconcile**:
  **bank deposits ↔ Stripe MRR ↔ the P&L they showed.** Screenshots are worthless.
- **Build the cohort retention curve yourself** from the raw Stripe export. Confirm MRR is flat/growing
  on a **revenue-retention** basis, not propped up by new-logo adds masking churn.
- Separate **recurring MRR from one-time/services**; flag lifetime/heavily-discounted annual plans and
  **unscheduled discount spikes** (classic dress-up tactics).
- **Concentration**: <20% from any one customer; check acquisition-channel concentration (single-channel,
  esp. price-competitive PPC vs funded rivals = red flag).
- **Traffic** (if any SEO/organic dependence): pull GA/Search Console read-only; check no single
  keyword/referrer carries the business.

### Days 42-50 — Technical diligence (HIS EDGE) on the finalist (GATE 3 setup)
- Read the repo + map the infra. FE calls **poor code documentation "deal-killing"** — confirm the
  **clean IP chain** (every contributor assigned IP; no missing contractor assignments).
- Hunt for: single points of failure, secrets in repo, no/stale backups, dependency rot, a scaling-cost
  cliff, one undocumented hack holding it together. **Price the true hosting/ops cost** (sellers
  understate it).
- Decide **"messy-but-fixable" vs "messy-and-a-trap."** Identify the 1-2 self-serve net-lift levers
  (hosting rightsizing, dunning) — NOT a rewrite.
- **Underwrite on trailing SDE only, zero growth credit.** If it pencils at **4.0-4.5x** with a genuinely
  capped downside → proceed to offer (GATE 3 pass).

**The eight deal-killer red flags (walk on any):**
1. Seller **refuses live read-only Stripe/bank** → instant walk.
2. **Declining** revenue/profit dressed as "stable" (cf. EF #94153: −37% rev / −50% profit YoY).
3. **Churn masked** by new-logo adds; cohort curve never flattens.
4. **>20% single-customer** (or single-channel) concentration.
5. **Thin/undocumented code, unclear IP ownership**, secrets in repo, no backups.
6. **Platform-dependent** (host can kill it) or **AI-wrapper commodity** (an LLM can clone it).
7. **Lifetime/one-time revenue** dressed as recurring; unscheduled discount spikes.
8. **Owner-as-the-product** with no SOPs and no willingness to do a real 60-90d transition.

**If nothing clears by Day 50 → that is SUCCESS, not failure.** Keep alerts running, keep reviewing,
never force a deal to a deadline. Patience is the entire risk-management strategy.

---

## DAYS 50-75 — OFFER, DEAL STRUCTURE, AND CLOSE

**Goal**: submit a structured LOI that caps the downside, pass confirmatory diligence in escrow, close.

### Days 50-58 — LOI + negotiate structure
**Recommended structure (this is what makes "downside capped" actually TRUE):**
- **All-cash on the bulk + 10-30% held as a 6-12mo earnout / seller note** tied to **revenue
  retention** (protects against the melting-ice-cube), **through escrow**, plus **non-compete** and a
  **60-90d paid seller transition + SOP handover** written into the APA.
- **Multiple**: **4.0-4.5x annual SDE (≈48-54x monthly)** for a non-declining asset. Pay the low end,
  or push toward 3.5x, ONLY if the numbers genuinely show flat-fragile/turnaround — and then price the
  base case as decline, not flat.
- **Use the earnout as a RISK-SHIFTER you request, not a discount you celebrate.** A seller who
  *eagerly* offers financing/earnout may be signaling low confidence in their own trailing numbers
  (adverse selection). Budget mostly cash regardless.
- **AVOID SBA / personal-guarantee financing.** SBA 7(a) acquisition loans require a personal guarantee
  (often a lien on personal assets/home) — that **destroys the capped, cash-only downside that is this
  idea's entire point.** All-cash caps max loss at the price minus resale; an SBA-leveraged deal can
  lose *more than the cash in* via the PG.

### Days 58-68 — Confirmatory diligence in escrow (GATE 4)
- Legal review of the asset-purchase agreement (budget a lawyer, see P&L). Lock the transition plan +
  SOP handover + non-compete + earnout terms in the contract.
- Re-verify metrics have not moved; any material discrepancy → **walk** (escrow protects the money).

### Days 68-75 — Close
- Fund via **escrow**; document the earnout/note. **Migrate everything**: domains, Stripe, bank/payout,
  hosting/DNS, repo, email, support inbox, customer records. Keep a **$10-15K working-capital reserve**
  untouched (EF: "never spend money unless you're okay losing 100% of it" — hold reserves for a slump).

---

## DAYS 75-90 — TRANSITION, FIRST IMPROVEMENTS, DELEGATION SETUP

**Goal**: do-no-harm absorption, then the self-serve net-lift moves (his edge), and set the honest
delegation posture.

### Days 75-85 — Absorb (do no harm)
- **Shadow the seller** on support; read every open ticket and the last 90 days of resolved ones.
- **Change NOTHING** on pricing or product yet. The months 1-2 goal is **stop the churn / do no harm**,
  not grow. (At ~4.5%/mo churn, two do-nothing months can bleed ~9% of MRR — minimize, don't add to it.)
- Start writing **SOPs** for support and routine ops as he learns them (prerequisite for any later VA).

### Days 85-90 — First operating improvements (the moves that resolve the delegation trap)
Instead of delegating a too-small asset, **engineer net up himself** — cheaper than a VA+dev and
exactly where his skills apply:
1. **Cut hosting/ops cost** (pure margin; his infra edge) — the safest first win.
2. **Recover involuntary churn via dunning / failed-card recovery** — a one-time **~3-8% MRR lift**
   (this touches only the ~0.8%/mo involuntary slice; it does NOT fix voluntary churn).
3. **Ship one AI/feature win himself** if the codebase is clean enough.

### The delegation setup — WHO does WHAT at WHAT COST (spelled out with numbers)
| Task | Delegable? | Cost |
|---|---|---|
| Tier-1 support / onboarding / mundane ops | Yes, **after SOPs exist** (month 6+) | Offshore VA **$300-1,500/mo** (~$5-12/hr, 20-40 hr/mo → $300-800; heavier front-line → $800-1,500) |
| Routine bug fixes / small features / dep upgrades | Yes, to a contractor dev | **$800-3,000/mo** variable (~$40-100+/hr) |
| Infra/hosting rightsizing | Hooman once (his edge), then rare | ~$0 ongoing |
| **Technical/escalated support, churn saves, key-account fires** | **NO — stays with Hooman** | his 8-12 hrs/wk |
| **Roadmap, pricing, dev direction, code review** | **NO — stays with Hooman** | included above |

**THE DELEGATION-AFFORDABILITY CHECK (the core math — memorize the numbers):**
- The asset he can **afford** ($80-120K → **~$1.5-2.5K/mo net** at a fair 4-4.5x) **cannot afford to be
  delegated**: a $1,000-2,500/mo VA+dev spend consumes most-to-all of the profit → he'd be paying to
  own a part-time job.
- The asset **worth** delegating (**$4K+/mo net**, leaving $1.5-2.5K after a ~$1.5-2.5K delegation spend)
  costs **~$190-215K at a fair multiple — over the $150K ceiling.**
- **Rule**: **Delegation (VA+dev) only pencils above ~$4K/mo net.** Below that, Hooman IS the operator
  at **8-12 hrs/wk indefinitely** (steady state; 20-25 in months 1-6). Delegate later by **growing into
  $4K/mo**, not by delegating a small asset into the red.

---

## THE HONEST BUDGET (within $25-150K)

| Item | Cost |
|---|---|
| Purchase price (mostly cash; 10-30% as earnout/note through escrow) | **$80-120K** |
| Escrow fee (~0.5-1% of price) | $500-1,500 |
| Legal review of APA | $2-5K |
| Diligence tooling / paid data | ~$500 |
| **Working-capital reserve** (transition dip + surprises) | **$10-15K** |
| **Total capital committed** | **~$95-140K** (stays inside $150K) |

**Expected cash yield**: at **~$1.5-2.5K/mo net** on ~$100-140K all-in = **~13-22% gross annual cash
yield**. Payback of purchase price **~5-7 years** at a fair multiple (faster only if he genuinely lifts
net), plus the **resale value** of the asset (can return most of the capital at exit). **True economic
profit after valuing his own ~40 hrs/mo at even $50/hr (~$2K/mo, below his real rate) ≈ $0-2.5K/mo** —
i.e. it barely clears, or fails to clear, hobby income once his time is priced. Upside ($5-7K/mo)
requires re-igniting customer acquisition (NOT his stated edge) — do not plan or pay for it.

### Realistic 12-month P&L (base case, fair 4-4.5x entry, ~4.5%/mo churn)
| Period | Gross net/mo | Delegation spend | Owner hrs/wk | Notes |
|---|---|---|---|---|
| Month 0 (close) | $1.5-2.5K | $0 | 20-25 | Entry, source-verified |
| Months 1-3 | $1.2-2.0K | $0 | 20-25 | Do-no-harm transition churn dip (~70-80% of entry) |
| Months 4-6 | $1.5-2.5K | $0 | 15-20 | Recover via hosting cut + dunning (~3-8% one-time lift) |
| Months 7-9 | $1.5-2.8K | ~$0 (NOT affordable to delegate at this size) | 8-12 | Steady state; Hooman stays operator |
| Months 10-12 | $1.5-3.0K | ~$0 | 8-12 | Optional small price test on new/renewing (low elasticity) |

**12-mo cash flow (before valuing his time)**: roughly **$18-32K gross**, minus ~$5-10K one-time close
costs already counted in capital, minus modest hosting/tools (~$300-1,000/mo, partly offset by the
hosting cut) → **~$12-25K net cash in year 1** on ~$100-140K deployed. **Do NOT model a VA+dev line in
year 1** — it is unaffordable and would push the P&L negative; that is the whole point of the delegation
check above.

---

## GO / NO-GO SUMMARY

- **Gate 0 (pass/fail)**: 15-20 hrs/wk (20-25 in months 1-6) + 8-12 hrs/wk indefinitely for ≥6 months,
  without hurting CutLog. If CutLog is mid-crunch → **DEFER.**
- **Gate 1** (Day 20): 5-8 listings pass the paper Buy Box.
- **Gate 2** (Day 42): live read-only Stripe+bank three-way reconcile; cohort curve flattens;
  concentration <20%. Refuse access → instant walk.
- **Gate 3** (Day 50): underwrites at 4-4.5x on trailing SDE with zero growth credit; tech is
  "messy-but-fixable," not a trap.
- **Gate 4** (Day 68): confirmatory diligence clean; contract has escrow + earnout + non-compete +
  transition. Any material discrepancy → walk.

**Do the ~$0 dry-run first (Days 1-50).** If nothing clears the gates in ~2-3 months, that is signal
the clean-deal price doesn't work for him — **keep the capital.** Verdict stands **CONDITIONAL**:
pursue only with idle capital, acceptance of a small part-time job with resale optionality, and a
genuine calendar window that does not steal CutLog's 0→1 hours.

---

## Sources
Built on `runs/buy_microsaas_research.md` (marketplace survey + multiples/churn, fetched 2026-07-01/02:
Acquire.com $500M+/2,000+ sold/$2B+ buyer funds/81-day close/median 3.9x profit; Empire Flippers
$589.6M/2,640 sold + live listing #94153; Microns.io in-budget ~3x-rev SaaS + AI-wrapper junk;
FE International 5-7x SDE under $2M, churn avg 4.7%/mo), and `runs/trackB/deep/buy_microsaas/`
02_execution_plan.md + 03_plan_validation.md (gates, delegation trap, honest revised economics).
