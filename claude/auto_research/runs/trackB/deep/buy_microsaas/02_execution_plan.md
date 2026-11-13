# Execution Plan — Buy a Cash-Flowing Boring B2B / Vertical Micro-SaaS

**Owner**: Hooman Shariati. **Written**: 2026-07-01 by Claude (Opus 4.8).
**Companion docs**: `01_research_validation.md` (the skeptic pass this plan is built on).
**Verdict this plan implements**: CONDITIONAL / MEDIUM confidence. This is a
**~20-35% cash-on-cash yield capital deployment with a capped downside**, NOT a
"double it in 24 months" growth play. Everything below underwrites on **trailing,
source-verified cash flow with ZERO value assigned to the growth story.**

---

## 0. TL;DR — what this actually is

Deploy **$80-150K all-cash** to buy ONE vertical-B2B system-of-record micro-SaaS doing
**$2-4K/mo source-verified net**, priced at **~3.0-3.5x annual SDE (30-42x monthly)**,
with **escrow + a 10-30% earnout/seller note + non-compete + 60-90d transition**. Operate
it part-time (10-20 hrs/wk, front-loaded to months 1-6), stop the churn, cut hosting cost,
ship 1-2 AI/feature wins, then **delegate to a VA + contractor dev** so it settles into a
low-touch cash stream. Realistic 24-mo target: **hold-flat-to-$3-5K/mo base case; $6-10K/mo
upside only if he actively rerates a messy deal.** The whole thesis rests on Hooman's rare
edge: he can read the code others can't, so he buys the **technically-messy-but-fixable**
deal the non-technical buyer pool discounts.

**This coexists with CutLog because it spends CAPITAL + DELEGATION, not CutLog's building
hours — EXCEPT months 1-6, which are genuinely hands-on. See §8. Do not close a deal in a
month where CutLog needs his full attention.**

---

## 1. The Specific Target (locked)

**Acquisition profile — all criteria are filters, not preferences:**

| Dimension | Hard filter |
|---|---|
| **Type** | Vertical B2B **system-of-record / workflow tool** in an unglamorous trade: field-service ops, specialty-trade POS/quoting, niche compliance & recordkeeping, dental/med-lab ops, property/HOA admin, trade-specific scheduling. |
| **Revenue** | ≥18-24 mo history; B2B; **annual or sticky monthly** billing; **source-verified via read-only Stripe + bank**, never screenshots. |
| **Net (SDE)** | **$2-4K/mo trailing** (do NOT stretch to $6K; that costs $105-210K and breaks the budget). |
| **Price / multiple** | **$80-150K all-cash; 3.0-3.5x annual SDE (30-42x monthly).** Pay the low end for anything with declining or flat-fragile revenue. |
| **Churn** | Logo churn ≤ ~3%/mo, **cohort retention curve flattens** (not masked by new-logo adds). |
| **Concentration** | **<20% revenue from any single customer.** |
| **Owner load** | Current owner works **<10 hrs/wk** (proves part-time operability). |
| **Moat** | Switching cost from being a system-of-record. **REJECT**: consumer apps, SEO/content sites, Chrome extensions, thin AI wrappers, and any single-platform app (Shopify/WP/Stripe add-on) whose host can kill it. |
| **The edge lane** | Prefer a deal that is **technically messy but fixable** — ugly code, high hosting bill, burned-out solo founder — that non-technical buyers discount and Hooman can rerate. That is the ONE place his engineering edge converts to alpha. |
| **Deal structure** | Escrow + **10-30% held as 6-12mo earnout/seller note** + non-compete + **60-90d seller transition + SOP handover**. |

**Where to source**: Empire Flippers (most vetted, priced highest), Acquire.com (most
volume in this band), Flippa (most volume, most junk, heaviest diligence), + **direct
outreach to founders of stalled niche tools** (best price, no auction — the highest-alpha
channel once he knows his niche).

**Pick a lane before shopping.** Hooman should choose **1-2 verticals he can underwrite
credibly** (e.g. field-service + one compliance/recordkeeping niche) so he becomes a fast,
confident buyer instead of a tourist. Domain familiarity = faster diligence = wins the
messy deals others can't judge.

---

## 2. First 90 Days (week-by-week)

**Phase A (Weeks 1-4): Setup + deal-flow, ~zero money spent.**

- **Wk 1** — Hooman: open buyer accounts on Empire Flippers, Acquire.com, Flippa. Set
  saved-search alerts for the profile in §1 ($75-160K, SaaS, B2B). Pick the 1-2 target
  verticals. Write a one-page personal Buy Box (this §1 as a checklist).
- **Wk 2** — Build the **diligence toolkit** (reusable, this is his moat as a repeat buyer):
  a spreadsheet model (trailing SDE, cohort retention, concentration, churn, hosting cost);
  a code/infra red-flag checklist (single points of failure, secrets in repo, backup story,
  dependency rot, scaling cost); a standard **read-only-access request** template (Stripe,
  bank/PayPal, Google Analytics, hosting console, repo).
- **Wk 3** — Review **20-30 listings** against the Buy Box. Reject fast. Goal: a shortlist
  of **5-8** that pass the paper screen. Log every rejection reason (builds pattern memory).
- **Wk 4** — Request seller intros / LOI-precursor calls on the top **3-5**. Ask the killer
  questions: why selling, owner hrs/wk, top-5 customer % of revenue, tech stack, who does
  support, what breaks at 2x scale.

**Phase B (Weeks 5-8): Deep diligence on 1-2 finalists (cheap validation — see §6).**

- **Wk 5** — Sign NDA; get **read-only Stripe + bank + analytics** on the #1 finalist.
  Reconcile bank deposits ↔ Stripe MRR ↔ the P&L they showed. **If they refuse live
  read-only access → walk.** (Kill-risk #2.)
- **Wk 6** — Build the real cohort-retention curve from Stripe data. Confirm churn, MRR
  trend (flat/growing, not decline dressed up by new logos), concentration <20%.
- **Wk 7** — **Technical diligence (Hooman's edge)**: read the codebase, map infra, price
  the true hosting/ops cost, list the tech debt and the 1-2 quick wins (hosting cut, an AI
  feature). This is where he decides "messy-but-fixable" vs "messy-and-a-trap."
- **Wk 8** — Underwrite on trailing SDE only (zero growth credit). If it pencils at
  3.0-3.5x with a capped downside → submit **LOI** with escrow + 10-30% earnout/note +
  non-compete + 60-90d transition. **GATE 3 (§6) here.**

**Phase C (Weeks 9-13): Close + start transition.**

- **Wk 9-10** — Confirmatory diligence during escrow; legal review of the asset-purchase
  agreement (budget a lawyer, §5). Lock the transition plan + SOP handover in the contract.
- **Wk 11** — **Close.** Funds via escrow; earnout/note documented. Migrate access,
  domains, Stripe, hosting, repo to Hooman.
- **Wk 12-13** — Absorb: shadow the seller on support, read every open ticket, do NOT
  change pricing or product yet. Goal for months 1-2 is **stop the churn / do no harm**,
  not grow. Ship only the safest cost win (e.g. hosting rightsizing) once stable.

**If no deal clears diligence by Week 13 → that's a SUCCESS, not a failure.** Keep the
alerts running and repeat Phase A/B on new listings. **Never force a deal to hit a
deadline** — patience is the whole risk-management strategy here.

---

## 3. Months 4-12 — Path to the revenue target (stays part-time)

**Operating cadence shifts from "learn it" to "stabilize + modest lift + delegate."**

- **Months 4-6 — Stabilize & instrument.** Kill involuntary churn (dunning/failed-card
  recovery — usually a free 10-20% MRR recovery). Fix the worst tech debt. Ship **one**
  customer-visible win (an AI feature or a top-requested feature). Write SOPs for support
  and ops as he goes. Time: still **~15 hrs/wk**.
- **Months 7-9 — Delegate.** Hire a **part-time VA / support contractor** (front-line
  support, onboarding, mundane ops) and put a **fractional contractor dev** on retainer for
  the tech debt / feature backlog. Hooman moves to **owner/operator: 5-10 hrs/wk** —
  strategy, roadmap, key-account touch, reviewing the dev's work.
- **Months 10-12 — Optional lift.** Test a 5-10% price increase on new/renewing customers
  (system-of-record = low elasticity). One low-effort acquisition channel already used by
  the business (e.g. its existing SEO/referral). Reassess: hold, reinvest, or add a 2nd
  asset.

**Realistic revenue path (base case, priced this way on purpose):**

| Month | Net/mo | Note |
|---|---|---|
| 0 (close) | $2-4K | Entry, source-verified |
| 1-3 | $1.8-3.6K | Expected transition churn dip |
| 4-6 | $2-4K | Recover to entry via dunning + retention |
| 7-12 | $2.5-5K | Modest lift; delegation frees Hooman |
| 24 (base) | $3-5K | Durable; **upside $6-10K** only if he actively rerates a messy deal |

**$8-15K/mo is a top-quartile, actively-operated outcome — do NOT plan on it or pay for
it.** The plan succeeds if the asset holds $3-5K/mo net at 5-10 hrs/wk — that is a durable
20-35% cash yield plus optionality.

---

## 4. Delegation / hiring plan (must stay part-time)

- **Months 1-6**: Hooman + the **seller (paid transition/consulting)**. No hires yet — he
  must understand the business before delegating it.
- **Month 7+**: **VA / support contractor** ($800-1,500/mo) for front-line support & ops.
- **Month 7+ (as needed)**: **fractional contractor dev** on retainer or per-task ($1-3K/mo
  variable) for the backlog. Hooman never becomes the full-time dev — he directs.
- **End state**: Hooman at **5-10 hrs/wk** (roadmap, key accounts, reviewing contractors).
  If it can't get to <10 hrs/wk, it's either the wrong asset or needs more delegation budget.

---

## 5. Budget (within $25-150K), burn, break-even

**One-time acquisition + close (from the capital allocation):**

| Item | Cost |
|---|---|
| Purchase price (mostly cash; 10-30% as earnout/note) | **$80-150K** |
| Escrow fee (~0.5-1% of price) | $500-1,500 |
| Legal review of APA | $2-5K |
| Diligence tooling / paid data | ~$500 |
| **Working-capital reserve** (transition dip + first hires + surprises) | **$10-15K** |
| **Total capital committed** | **~$95-170K** — *aim for the $80-120K purchase band to stay inside $150K all-in.* |

**To respect the $150K ceiling: target a purchase price of ~$80-120K**, leaving room for
close costs + the $10-15K reserve. A $150K purchase blows past the budget once costs and
reserve are added.

**Ongoing monthly burn (post-close):**

- Months 1-6: hosting + tools **$300-1,000/mo**; seller transition consulting (often
  bundled into price or a few $K one-time). Effectively **< $1K/mo** cash burn.
- Months 7+: + VA **$800-1,500/mo** + contractor dev **$1-3K/mo variable** = **$2-4.5K/mo**.

**Break-even / payback:**
- The business is **cash-flow positive from day one** (that's the point — you buy profit).
- **Payback of purchase price**: at $2-4K/mo net, **~3-4 years** to return capital (20-35%
  annual cash yield), FASTER if he rerates it, plus the resale value of the asset itself
  (which can return most of the capital at exit). This is a yield + optionality play, not a
  quick flip.

---

## 6. Go/No-Go gates + cheapest validation BEFORE real money

**All validation up to LOI costs ~$0 and only Hooman's hours. Do NOT wire money until
Gate 3.**

- **GATE 0 — Personal fit (Week 0, free).** Can Hooman honestly commit **15-20 hrs/wk for
  months 1-6** alongside CutLog? If CutLog is mid-crunch, **defer the whole thing** — do not
  split the hours the CutLog thesis needs. This is a scheduling decision, not a deal
  decision.
- **GATE 1 — Paper screen (Weeks 3-4, free).** Passes the §1 Buy Box on the listing's
  stated numbers + vertical fit. Reject 90%+ here.
- **GATE 2 — Source-verified metrics (Weeks 5-6, free).** **Live read-only Stripe + bank
  reconcile to the claimed P&L**; cohort retention flat/growing; concentration <20%. Seller
  refuses live access → **instant walk.** This single gate kills kill-risks #1 and #2.
- **GATE 3 — Underwrites on trailing cash + tech is fixable (Weeks 7-8, free).** Pencils at
  3.0-3.5x annual SDE with **zero growth credit**; Hooman's code/infra review says
  "messy-but-fixable" not "trap." Only now submit LOI with escrow + earnout/note +
  non-compete + transition.
- **GATE 4 — Confirmatory diligence in escrow (Weeks 9-10).** No surprises; contract has the
  risk-shifters. Any material discrepancy → walk (escrow protects the money).

**Cheapest validation of the whole STRATEGY before committing to any deal:** run Phases A-B
on **2-3 real listings as a dry run** — request read-only access, build the model, do the
tech review — and only proceed to LOI if a real one clears Gate 3. If nothing clears after
~2-3 months of looking, that's strong signal the clean-deal supply/price doesn't work for
him, and he keeps the capital.

---

## 7. Kill-risks → mitigations (carry-through from research)

1. **Melting ice cube** → underwrite trailing only; ≥18-24mo verified flat/growing; earnout; walk from declines.
2. **Fake metrics** → live read-only Stripe/bank; cohort retention; escrow. No live access = no deal.
3. **Key-person dependency** → 60-90d transition + non-compete + SOP handover in the contract.
4. **Platform / disintermediation** → buy system-of-record with switching cost; reject platform add-ons and thin AI wrappers.
5. **Bidding-war adverse selection** → deliberately fish the messy-but-fixable pond his eng edge wins; walk from messy-in-ways-he-can't-fix (legal/customer/market).
6. **Time is the real constraint** → Gate 0; front-load hours to months 1-6; delegate hard by month 7; never neglect it (neglect → churn).
7. **Concentration (one deal = all eggs)** → accept single-asset risk at this capital level; only add a 2nd asset after the 1st is delegated and stable.

---

## 8. Coexistence with CutLog (the binding real-world constraint)

**CutLog is the primary bet and needs Hooman's scarce BUILDING hours (0→1 grind). This
acquisition is deliberately chosen because it consumes CAPITAL + DELEGATION instead —
EXCEPT the months 1-6 absorption, which is genuinely hands-on.**

Rules to keep both alive:
1. **Sequence, don't stack the crunches.** Do NOT close a micro-SaaS deal in a month where
   CutLog needs a launch push. The deal-flow (Phase A) is passive/async and can run
   continuously in the background; only pull the trigger (Phase B/C) when CutLog has slack.
2. **Front-load then delegate.** Absorb in months 1-6, then hand support to a VA and dev to
   a contractor by month 7 so it drops to 5-10 hrs/wk and stops competing with CutLog.
3. **Capital is separate from attention.** The $80-120K is money Hooman can commit without
   spending building hours; that's the strategic reason BUY beats BUILD for a *second*
   stream (his only gap is distribution, and he's buying distribution).
4. **Hard stop**: if at Gate 0 he can't spare 15-20 hrs/wk for 6 months without hurting
   CutLog, **defer the acquisition entirely** rather than split focus. A neglected
   acquisition churns out and loses the allocation (kill-risk #6).

---

## 9. Immediate next actions

1. **Hooman**: answer Gate 0 — can he give this 15-20 hrs/wk for months 1-6 without hurting
   CutLog, and in which calendar window? (Scope confirmation before any spend.)
2. **Hooman**: pick the 1-2 target verticals he can underwrite credibly.
3. Then: open marketplace accounts + saved searches, build the diligence toolkit, start the
   Phase-A dry run on 2-3 real listings — all free, all reversible.
