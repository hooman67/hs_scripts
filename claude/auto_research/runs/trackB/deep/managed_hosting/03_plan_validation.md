# Adversarial Red-Team — Managed Technical Hosting (HostiFi model) Execution Plan

**Date**: 2026-07-01. **Reviewer**: Claude (Opus 4.8), adversarial red-team pass.
**Docs reviewed**: `01_research_validation.md`, `02_execution_plan.md`.
**Founder constraints assumed**: Adobe eng manager, $25–150K capital, ~10–20 hrs/wk, CutLog is the
primary 0→1 and must not slip.

**Verdict up front: HOLDS-WITH-CHANGES.** The plan is genuinely good — it already inverted the
pitch, killed the from-scratch build, and gated every dollar. That intellectual honesty is why it
survives. But the *acquisition track it now leans on* imports a new set of optimistic assumptions
that the plan under-prices: the deals it wants mostly don't exist at the stated multiple, the
post-transfer churn/founder-dependence risk is worse than "±5%", and the "$1.5–3K/mo contractor
makes it part-time" claim quietly assumes cheap support labor can carry infra on-call, which it
can't. Corrected, realistic net is **$1.5–4.5K/mo in 18–30 months, with a materially higher
probability of a $0/mo outcome (walk-away or a dud acquisition) than the plan implies.**

---

## 1. Assumptions most likely WRONG (and the blast radius if they are)

### A. "A $3–12K/mo MRR, >60% margin, <15 hrs/wk, <5% churn, clean-license, no-vendor-cloud, sub-4x-profit deal is findable." — **MOST LIKELY WRONG / OVER-CONSTRAINED**
This is a seven-way AND. Each filter is individually reasonable; the conjunction is rare. The
research doc itself established that the *whole category* is either (a) vendor-cloud'd, (b)
license-gated, or (c) racing to a $1.80–$11/mo price floor. A seller who has a clean-license,
no-vendor-cloud, low-churn, part-time-runnable managed-hosting business at $3–12K/mo has a
**cash cow they have little reason to sell at 2.5–4x** — and if they do sell, the buyer pool on
Acquire.com/Flippa is deep, so it clears at the *top* of the range or above, not 2.5x.
- **What breaks if wrong:** Gate 1 forces Track B (the build) — the exact second-distribution-front
  the whole plan was designed to avoid. The plan treats Track B as a rare fallback; in reality the
  over-constrained Track-A filter makes Track B the *likely* outcome, not the exception. The plan's
  "recommended default" may be the branch that almost never fires.

### B. "MRR holds within ±5% through the transition." — **OPTIMISTIC**
Verified against broker guidance (FE International / Acquire diligence norms): the dominant
micro-SaaS acquisition failure mode is **churn acceleration when the founder leaves**, precisely
because in a solo micro-SaaS the founder *is* the support desk, the community presence, and the
trust. Managed hosting is worse than average here — the product is a *relationship of trust to keep
my server up*, and that trust is personal. A 10–25% MRR decline over the first 6 months
post-transfer is a more honest planning number for a founder-run hosting business than ±5%.
- **What breaks if wrong:** You buy at ~4x on claimed MRR, then lose 15% of it, so your effective
  multiple jumps to ~4.7x on *real* retained MRR, and your payback stretches from "18–30 months"
  to 30–48 months. Gate 2 (±5%) would correctly fail — but you've already spent $45–109K to learn it.

### C. "$1.5–3K/mo buys a contractor who owns tier-1 support AND on-call, keeping Hooman <5 hrs/wk." — **CONFLATES TWO DIFFERENT LABOR MARKETS**
Web-checked rates: offshore *support/VA* labor is genuinely ~$15–30/hr ($1.5–3K/mo part-time).
But offshore *DevOps engineers who can safely own infra on-call* are $40–100/hr (Upwork median
~$60), and on-call commands a premium on top. The plan wants the cheap person to do the expensive
job. In practice you get one of:
  - a $1.5–3K/mo support VA who escalates every real incident to Hooman (so Hooman keeps the pager
    → not <5 hrs/wk, and worse, unpredictable 2am hours), **or**
  - a real fractional DevOps on-call at $4–8K/mo (kills the margin — a $5K MRR biz at 65% margin
    = ~$3.25K gross; a real on-call contractor eats most of it).
- **What breaks if wrong:** The "part-time via delegation" mechanism — the single load-bearing
  assumption for coexistence with CutLog — is weaker than stated. Either Hooman is on the pager
  (CutLog slips, violating the hard rule) or margin collapses (the business can't fund its own
  contractor, which the plan itself says is the kill signal).

### D. "Infra skills become a margin/reliability edge post-acquisition." — **PARTIALLY WRONG (direction right, magnitude oversold)**
The plan projects "lift margin 5–10 pts" from Hooman re-architecting provisioning. Real cloud COGS
on a $5K MRR hosting biz is maybe $750–1,500/mo; shaving even 30% off it is +5–9 pts of margin =
~$225–450/mo. Nice, not transformative, and it costs Hooman engineering hours (the scarce
resource) to capture. The edge is real but small and time-expensive — it does not change the
venture's outcome the way the framing implies.

### E. "Escrow + a $1.5K lawyer-reviewed SaaS purchase agreement is adequate diligence." — **UNDER-BUDGETED**
Verifying Stripe payouts vs claimed MRR, cohort churn, refund rate, COGS invoices, customer
concentration, and hosted-tool license transferability on a $50–100K deal is real work. A $1.5K
template review does not cover a proper asset-purchase agreement with reps/warranties, an
IP/domain/infra transfer schedule, and a clawback/holdback for MRR that walks. Realistic legal +
diligence is **$3–7K**, and the *time* cost (Hooman doing the financial diligence himself because
he won't pay for a full QoE on a sub-$100K deal) is 20–40 hours concentrated in weeks 5–8 — which
will collide with CutLog.

### F. "Zero Track-A candidates AND zero Track-B tools ⇒ clean cheap NO-GO at Gate 0." — **TRUE and the plan's best feature.** No correction; this is the plan working as designed.

---

## 2. Independent financial sanity-check — rebuilt conservatively

### 2.1 The acquisition multiple (Track A)
- Plan says buy at **2.5–4x annual profit**, $40–100K, for a ~$5K/mo MRR business.
- Web-check: **3x SDE is the consensus micro-SaaS benchmark**; 2.5–4x is a fair *range*. So the
  multiple is **not** where the optimism lives. **This number holds.**
- BUT: for a $5K/mo MRR business, annual MRR is $60K. At 65% margin that's ~$39K gross, and SDE
  (add back owner's non-market labor, subtract real replacement support cost) is realistically
  **$25–40K/yr**, not $60K. So 3x SDE ⇒ **$75–120K purchase**, i.e. the top of the plan's band,
  not the middle. The plan's "$40–100K" quietly assumes you buy near 2.5x SDE — achievable only on
  a distressed/declining asset, which is exactly the asset most likely to keep declining. **Healthy
  asset ⇒ ~$90–120K; cheap asset ⇒ probably a churn trap.** The good-and-cheap quadrant is thin.

### 2.2 Payback, corrected
- Purchase $90K (healthy), net ~$3K/mo after a *real* contractor and COGS ⇒ **payback ~30 months**,
  not "18–30." Add 15% transition churn and it's **36–42 months**. That's a 3-year capital lockup
  of ~60–70% of the low end of Hooman's envelope, for a $3K/mo asset.

### 2.3 Contractor / margin, corrected
- Plan's monthly burn: "$2.5–5K/mo (contractor + COGS)" against $5K MRR. Note this is **50–100% of
  revenue.** If the true on-call contractor is $4–8K/mo, the business is **structurally
  loss-making at $5K MRR** until it grows — meaning it can't fund its own delegation, i.e. Hooman
  holds the pager. The plan's own kill-rule fires.
- Honest version: at $5K MRR you can afford a $1.5–2.5K/mo *support VA*, and Hooman *is* the
  on-call engineer for real incidents (a few hrs most weeks, occasional bad nights). That is
  tolerable for a while but is **not "<5 hrs/wk, delegated"** and it **does** compete with CutLog.

### 2.4 Track B economics (the likely-forced branch), corrected
- Plan: 80 instances @ ~$35/mo by month 12 ⇒ ~$2.5K/mo net. To hit 80 paid instances part-time,
  from a standing start, in a niche with no proof point, at ≤6–10 hrs/wk, against horizontal players
  at $1.80–$11 — CAC is almost entirely **founder time**, and the research already flagged sales as
  Hooman's weakness. Realistic month-12 is **20–40 instances (~$0.5–1.5K/mo net)**, not 80. Track B
  hitting the numbers is the least believable table in the plan.

### 2.5 Corrected ramp (blend of "healthy Track A" and "reality")
| Month | 6 | 12 | 18 | 24 | 30 |
|---|---|---|---|---|---|
| Plan Track A net | 2.5K | 4.5K | 6K | 7K | — |
| **Red-team Track A net** | 1.0K | 2.5K | 3.5K | 4.0K | 4.5K |
| **Red-team Track B net** | ~0 | 0.5–1.5K | 2K | 3K | 3.5K |

The plan's ramp assumes both no transition churn and cheap effective on-call. Removing those two
optimisms halves the first-year net and pushes the plan's "$8–10K/mo by 18–24mo" out to
**year 3+, if ever.**

---

## 3. Does it REALLY stay within 10–20 hrs/wk?

**During validation (weeks 1–8): yes** — ≤6 hrs/wk is realistic for saved searches, disqualifier
scans, and seller calls. The gating design genuinely protects Hooman here. Good.

**Weeks 5–12 (diligence + transition): NO — a spike.** Financial diligence on a sub-$100K deal that
Hooman won't pay a full QoE for means *he* verifies Stripe/cohorts/COGS (20–40 hrs), and the 30-day
seller-handover transition is front-loaded with incident learning. This is a **30–40 hr/wk-equivalent
month** compressed into calendar time, landing squarely on CutLog. The plan does not budget for this
collision; it just asserts ≤6 hrs/wk through week 12, which is not credible for the close-and-transfer
window.

**Steady-state (month 4+): CONDITIONAL.** Only stays <10 hrs/wk *if* the cheap contractor can
actually absorb on-call. Per §1C/§2.3 that's the weak assumption. Realistically Hooman remains the
infra escalation point — a few predictable hours most weeks plus **unpredictable off-hours pages**.
For an Adobe EM already running CutLog, it's the *unpredictability* (not the hour count) that's the
real cost: a 2am UniFi-controller-down page the night before a CutLog customer demo. The plan's
"delegated, <5 hrs/wk" steady state is achievable only above ~$10K MRR, which is a 18–24mo+ outcome.

**Bottom line on time:** it stays part-time *on average* but has two hidden full-attention spikes
(transition month; incident nights) that the plan doesn't price and that specifically threaten
CutLog, which is the one thing the plan swore to protect.

---

## 4. Honest revised realistic monthly profit

- **Track A, healthy acquisition, executed well:** **$1.5–4.5K/mo net** reached over **18–30 months**,
  after a real contractor and post-transfer churn, on ~$90–120K deployed. Best-case, patient outcome.
- **Track A, cheap acquisition:** high odds it's a declining/founder-dependent asset → net drifts to
  **$0–1.5K/mo** and you've locked up capital in a shrinking book.
- **Track B (the likely-forced branch):** **$0.5–2.5K/mo net** by 18–24 months, high effort, high
  chance of the Gate-3 kill at <30 instances.
- **Probability-weighted, honest expectation:** ~**$1.5–4K/mo net in 18–30 months**, with a
  **meaningful (~40–50%) chance the honest answer is $0** — either a clean walk-away at Gate 0/1
  (good, cheap) or a dud acquisition that never clears payback (bad, expensive). The plan's own
  "$2–8K/mo" band is defensible only if you both find the rare good-and-cheap deal *and* delegation
  actually works; strip either and you're at the bottom of that band or below.

---

## 5. Does the plan hold? — **HOLDS-WITH-CHANGES**

It holds because the *structure* is right: it already rejected the pitch, killed the build,
capped downside, and gates every dollar behind a real card charge or verified payout. That
skeleton is sound and low-risk. What must change is the acquisition-track optimism:

**Required changes:**
1. **Re-price the deal honestly.** Assume a *healthy* target costs **~3x SDE = $90–120K**, and that
   SDE ≠ MRR (owner labor + real support cost come out first). Budget **$3–7K** for legal/diligence,
   not $1.5K. If the deal is cheap, assume it's cheap *for a reason* and diligence the decline.
2. **Add an MRR holdback/earn-out to the purchase.** Structure 15–25% of price as a 6-month holdback
   contingent on retained MRR. This directly hedges the §1B churn risk and is standard in
   micro-SaaS deals. The plan currently pays 100% at close via escrow — don't.
3. **Fix the contractor assumption.** Separate the two roles: a $1.5–2.5K/mo support VA for tier-1,
   **plus** an explicit line item / decision for infra on-call. Either accept Hooman-as-on-call
   (and then honestly admit this is NOT <5 hrs/wk and CutLog is exposed to pages), or budget a real
   fractional DevOps ($3–5K/mo) and admit the business is margin-negative until ~$10K MRR. Do not
   let the plan pretend a $2K/mo hire covers 24/7 infra.
4. **Add an explicit on-call SLA / runbook + a $/incident cap in Gate 2.** Gate 2 should measure
   *unplanned off-hours pages*, not just "on-call <8 hrs/wk." One 2am page a month can violate the
   CutLog hard-rule even at low total hours.
5. **Move the transition-month time spike into the plan and pre-agree the CutLog trade.** Weeks
   5–12 are not ≤6 hrs/wk. Decide *now* what CutLog work gets paused during the close, or delay the
   close to a CutLog-quiet window. Otherwise the plan silently breaks its own #1 constraint.
6. **Demote the ±5% Gate-2 threshold to a realistic band and price churn in.** Expect and plan for
   10–15% transition churn; make the go/no-go about *stabilization trajectory*, not perfection.
7. **Acknowledge Track B is the *probable* branch, not the rare fallback**, given how
   over-constrained the Track-A filter is — and therefore either loosen a Track-A filter (accept a
   slightly-declining asset you can fix) or accept up front that this idea most likely resolves to
   "walk away at Gate 1," which is a fine outcome but should be stated as the base case, not the
   exception.

**The one thing that would make me say PASS instead of HOLDS-WITH-CHANGES:** if diligence on real
listings in weeks 1–2 shows the good-and-cheap-and-clean-license quadrant is empty (highly likely
per the research), then the honest move is to take the cheap NO-GO at Gate 0/1 and put the capital
toward CutLog or a proven cash-flowing asset in a *non-hosting* category — not to slide into the
Track-B build the plan itself calls a trap. The plan's own gates already enable this; the change is
to stop framing acquisition as a likely win and start treating "walk away cheaply" as the expected,
acceptable result.
