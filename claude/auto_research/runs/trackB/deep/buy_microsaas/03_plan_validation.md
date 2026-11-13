# Plan Validation — Adversarial Red-Team of "Buy a Cash-Flowing Boring B2B / Vertical Micro-SaaS"

**Idea slug**: `buy_microsaas`
**Date**: 2026-07-01. **Reviewer**: Claude (Opus 4.8), adversarial red-team pass.
**Docs reviewed**: `01_research_validation.md`, `02_execution_plan.md`.
**Founder**: Hooman — Adobe eng manager; $25-150K capital; ~10-20 hrs/wk; already building CutLog.

**One-line verdict**: The plan is unusually honest and well-structured — it already
pre-corrected most of the pitch's optimism. But it still carries THREE embedded errors
that make the returns look better and the time look lighter than reality: (1) the entry
**multiple is too low** for the target quality (you don't buy sticky-low-churn assets at
3.0-3.5x — those trade at 4-6x; at 3-3.5x you're buying decline), (2) the **churn
assumption (≤3%/mo) is below the empirically-observed SMB average (4.7%/mo, 44%/yr)**,
which quietly turns "hold flat" into "slow bleed," and (3) the **time estimate understates
the perpetual founder-glue floor** of a support-heavy B2B SaaS. Net: this HOLDS-WITH-CHANGES
as a ~15-25% cash-yield play, not the ~20-35% the plan claims.

---

## 1. Assumptions most likely WRONG (and the blast radius)

### WRONG-1 — "Buy sticky, low-churn, flat-and-fixable at 3.0-3.5x annual SDE." (The core pricing lie.)
This is the plan's central contradiction and its biggest error. The plan wants BOTH:
- a **high-quality asset** (≤3%/mo churn, system-of-record switching cost, <20% concentration,
  ≥18-24mo flat/growing revenue), AND
- a **low-quality price** (3.0-3.5x annual SDE = 30-42x monthly).

**Fact-check (2026-07-01):** FE International states SaaS **under $2M sells at 5.0x-7.0x SDE**.
Acquire.com's Jan-2026 report: **median 3.9x profit, low-to-mid-4x average**, "stable YoY."
So the *market clearing price* for even a mediocre small SaaS is ~4x, and a genuinely
sticky/low-churn one is 4.5-6x. **3.0-3.5x is the price of a DECLINING or fragile asset**,
exactly the "melting ice cube" the plan says to avoid. You cannot simultaneously demand
top-quartile stickiness and pay a bottom-quartile multiple in a marketplace with $2B+ of
buyer capital chasing supply (Acquire.com) and 81-day average time-to-close. **The good
assets don't reach your inbox at 3-3.5x; cash-ready micro-PE takes them at 4-5x first.**

**What happens if wrong (it is):** One of two things, both bad for the stated plan:
- (a) He holds the 3.0-3.5x discipline → he only ever gets to buy **declining** businesses
  (the ones nobody else wants at that price), and the "hold flat" base case is actually
  "-10 to -30%/yr," or
- (b) He relaxes to 4.5-5.5x to win a genuinely good asset → the **cash yield drops from
  ~25-33% to ~18-22%** and the payback stretches from 3-4yr to **5-6yr**. Either way the
  headline economics degrade. Realistic path: he pays ~4-4.5x for something merely okay.

### WRONG-2 — "Logo churn ≤3%/mo; base case = hold flat." (Churn floor too low.)
The plan's revenue table assumes a dip in months 1-3 then recovery to flat/modest-lift.
**FE International's own sample of 25 SaaS acquisitions: churn ranged 1-11%/mo, average
4.7%/mo ≈ 44% annualized.** SMB/micro B2B is the *high* end because small-business
customers themselves fail and switch cheaply. At 4.7%/mo gross logo churn, a business
needs to add ~4.7%/mo in new revenue *just to stand still* — and these businesses are for
sale precisely because the founder **stopped doing the sales/marketing that fed that top
of funnel.** A new owner who "does no harm" for months 1-2 (as the plan correctly
prescribes) is, in a 4.7%/mo-churn business, watching **~9% of revenue walk out** in those
two do-nothing months before he's even allowed to touch anything.

**What happens if wrong:** "Hold flat" is not the base case — **gentle decline is.** The
month-24 "$3-5K base / $6-10K upside" band should shift down to **"$1.5-3.5K base, $5-7K
upside."** The dunning/involuntary-churn recovery the plan leans on (the "free 10-20% MRR
recovery") only addresses **involuntary** churn (~0.8%/mo of the 4.7%); it does nothing for
the ~3.9%/mo **voluntary** churn that dominates. The plan overweights the one lever that's
cheap and underweights the expensive one (re-igniting acquisition).

### WRONG-3 — "Seller financing negotiable but budget mostly cash." (Actually more ambiguous — but doesn't help him.)
The research doc says EF states "cash upfront remains the most popular option." The EF
financing page I fetched today says the opposite: seller financing/earnouts are "**by far
the most common method for buyers to finance their deals.**" This contradiction means the
underlying evidence is softer than either doc claims. **Net effect is neutral-to-negative
for the plan either way:** if seller financing IS common, it's because sellers of *weak*
businesses offer it to de-risk the buyer (adverse selection — the seller who'll finance
knows something). Cheap leverage on a declining asset is a trap, not a gift. Assuming cash
is the safe planning posture, so the plan's conclusion ("budget mostly cash") survives — but
it should stop implying the earnout is a reliable downside cap; a seller eager to earnout
may be signaling low confidence in the trailing numbers.

### WRONG-4 — "The technically-messy-but-fixable deal is his lane / his edge converts to alpha."
This is the plan's *thesis*, and it's the least tested. The problem: **messy code is rarely
the reason a $2-4K/mo B2B SaaS is cheap or churning.** Small B2B SaaS lives and dies on
**customer relationships, support responsiveness, and domain trust** — none of which an
Adobe infra engineer's code-reading skill fixes. If the business is cheap because of ugly
code, rewriting it produces **zero new revenue** (customers don't pay more for a clean
backend). If it's cheap because the founder stopped selling / support degraded / the niche
is shrinking, **Hooman's edge is irrelevant to the actual problem.** His engineering edge is
real for *diligence* (spotting traps) but weak for *value creation* here. The "rerate a messy
deal to $6-10K" upside leans on an edge aimed at the wrong bottleneck.

**What happens if wrong:** the upside case largely evaporates; he's left with the base-case
yield only, and the whole thing is "a bond that can default," not a growth option.

### WRONG-5 — "Coexists with CutLog because it spends capital + delegation, not building hours."
The plan itself hedges this (Gate 0, "months 1-6 are hands-on"), which is good. But it still
undersells the **perpetual floor**. B2B SaaS support is not fully delegable to a $800-1.5K/mo
VA: technical support tickets, key-account fires, churn saves, and dev-direction all need the
owner. Realistic steady state is **8-12 hrs/wk indefinitely, spiking to 20+ on any incident**,
not the "5-10 hrs/wk" end state. That's the same attention pool CutLog's 0→1 grind needs.

---

## 2. Independent financial sanity-check — rebuild conservatively

| Lever | Plan's number | Red-team conservative | Why |
|---|---|---|---|
| Entry multiple (annual SDE) | 3.0-3.5x | **4.0-4.5x** for anything not declining | FE 5-7x under $2M; Acquire median 3.9x. 3-3.5x = decline. |
| Entry net (SDE) at $80-120K price | $2-4K/mo | **$1.5-2.5K/mo** at a realistic 4-4.5x | Same $80-120K buys less profit at a fair multiple. |
| Gross logo churn | ≤3%/mo | **~4.5%/mo (≈44%/yr)** | FE sample avg 4.7%; SMB is the high end. |
| Months 1-6 revenue path | dip to $1.8-3.6K, recover to entry | **dip to ~70% of entry, partial recovery only** | Do-no-harm period + no re-acquisition = net erosion. |
| Involuntary-churn recovery | "free 10-20% MRR recovery" | **3-8% one-time MRR** | Recovery only touches the ~0.8%/mo involuntary slice. |
| Month-24 base case | $3-5K/mo | **$1.5-3.5K/mo** | Churn floor + edge-mismatch cut the lift. |
| Month-24 upside | $6-10K/mo | **$5-7K/mo**, low-probability | Requires re-igniting acquisition, not just code fixes. |
| Ongoing burn (mo 7+) | $2-4.5K/mo (VA+dev) | **$2-4.5K/mo — but this eats a $2-2.5K/mo asset alive** | On a $1.5-2.5K/mo business, a $2K+ VA+dev spend is negative. Delegation is unaffordable below ~$4K/mo net. |
| Owner time, steady state | 5-10 hrs/wk | **8-12 hrs/wk + incident spikes** | Support/relationship floor isn't delegable. |
| Cash yield at entry | 20-35%/yr | **12-22%/yr** | Lower net (WRONG-1) ÷ same capital, before decline. |
| Payback | 3-4 yr | **5-7 yr** (or resale-dependent) | Follows from lower yield + decline drag. |

**The delegation-affordability trap (biggest hidden math error):** The plan targets a
$2-4K/mo net asset but plans $2-4.5K/mo of delegation spend at month 7+. **If the asset is
at the low/realistic end ($1.5-2.5K/mo net), the delegation budget consumes ALL the profit
and then some** — Hooman would be paying to own a job. Delegation only pencils on an asset
netting **$4K+/mo**, which at a fair 4-4.5x multiple costs **$190-215K — well over the $150K
ceiling.** So there's a structural squeeze: *the assets he can afford ($80-120K) can't afford
to be delegated; the assets worth delegating cost more than his budget.* This is the plan's
core financial contradiction and it isn't acknowledged.

**Honest yield range:** ~$1.5-3K/mo net on ~$100-140K all-in ≈ **13-22% gross cash yield,
before the owner values his own 8-12 hrs/wk.** Charge his time at even $50/hr (well below his
real rate) and ~40 hrs/mo = $2K/mo of labor — which **wipes out most or all of the cash
yield** on a low-end asset. The "passive-ish capital deployment" framing only survives at the
top of the net range, which the budget can't reach at a fair price.

---

## 3. Does it REALLY stay within 10-20 hrs/wk?

**Months 1-6: NO — plan on 20-25 hrs/wk, spiking higher.** Transition, learning an
undocumented codebase, reconciling every customer relationship, and stopping churn on a
business you didn't build is genuinely heavy. The plan admits "front-loaded"; the honest
number is higher than the "15-20" it states, and it directly collides with CutLog's grind.

**Steady state (month 7+): 8-12 hrs/wk, NOT 5-10 — and only IF he can afford delegation,
which (see §2) he can't on a sub-$4K/mo asset.** Without an affordable VA+dev, he stays the
support desk and the dev, i.e. **it stays a part-time job, not a yield.** The plan's "5-10
hrs/wk delegated end state" is achievable only on an asset too expensive for his budget.

**Verdict on time:** it does NOT reliably stay in 10-20 hrs/wk. It's 20+ up front and settles
to a **8-12 hr/wk owner-operator job** that competes with CutLog for the same scarce attention,
because the delegation that would make it passive is unaffordable at his price point.

---

## 4. Honest revised realistic monthly profit

Netting out (a) a fair 4-4.5x entry multiple → lower entry net, (b) ~4.5%/mo churn drag,
(c) edge-mismatch on the upside, and (d) delegation being unaffordable on a small asset:

- **Entry (month 0):** $1.5-2.5K/mo net (source-verified), for ~$100-140K all-in.
- **Months 1-6:** dips to ~$1.2-2K/mo (transition churn), Hooman spending 20-25 hrs/wk.
- **Month 24 base case: $1.5-3K/mo net**, at 8-12 hrs/wk, **before** valuing his time and
  **before** any delegation spend (which he can't afford at this size without going negative).
- **Realistic all-in owner economics:** roughly **$1.5-3K/mo gross cash yield, minus the
  opportunity cost of ~40 owner-hours/mo → effectively $0-2K/mo of true economic profit** on
  a low-end asset, up to ~$3-4K if he lands the rare fair-priced sticky one and it holds.
- **Upside (low probability):** $5-7K/mo if he buys well AND re-ignites acquisition (a skill
  not in his stated edge). Not the base case; don't plan or pay for it.

**Honest revised realistic monthly profit: ~$1.5-3K/mo gross cash flow (≈13-22% cash yield),
which nets to roughly $0-2.5K/mo of true economic profit after his own time — with real
option value in the asset's resale and a genuinely capped $80-140K downside.**

---

## 5. Does the plan hold?

### Verdict: HOLDS-WITH-CHANGES.

The *structure* is sound and the plan's process discipline (zero-cost gates, source-verified
Stripe/bank, escrow + earnout, walk-away default, CutLog sequencing) is genuinely good — better
than most acquisition playbooks. The **downside cap is real and is the best feature.** What
does NOT hold is the *return and effort framing*: it's a **~13-22% cash yield that nets close
to zero after the owner's own time on affordable-sized assets**, not a ~20-35% near-passive
yield, and it needs 8-12 hrs/wk indefinitely, not 5-10.

**Mandatory changes to make it PURSUE-grade:**

1. **Fix the multiple/quality contradiction.** Either (a) accept you'll pay **4-4.5x** for a
   genuinely sticky asset and re-underwrite at **~15-20% yield / 5-7yr payback**, or (b) keep
   the 3-3.5x discipline and explicitly accept you're buying **turnaround/decline** assets
   where Hooman's edge must actually reverse the business — a much harder, higher-variance bet.
   Pick one honestly; you can't have both.

2. **Re-baseline churn to 4-5%/mo** in the underwriting model. Require the cohort curve to
   *actually* flatten in the Stripe data (not just be claimed), and treat any asset needing
   ongoing acquisition to stand still as a growth bet, not a yield bet — and price it as such.

3. **Resolve the delegation-affordability trap.** State the rule explicitly: **delegation
   (VA+dev) only pencils above ~$4K/mo net.** Below that, the plan must own that Hooman remains
   the operator (a job, not a yield). If he won't accept a part-time job, raise the budget/quality
   bar to a $4K+/mo asset — which means going above $150K and defeating the current constraint.

4. **Downgrade the "messy code = my alpha" thesis.** Reposition his engineering edge as a
   **diligence/trap-detection** advantage (real) rather than a **value-creation** advantage
   (weak, because code isn't why small B2B SaaS churns). Do not pay a premium expecting to
   rerate via a rewrite.

5. **Harden Gate 0.** Given months 1-6 are 20-25 hrs/wk (not 15-20), and steady state is 8-12
   (not 5-10), the honest question is: can he spare **20-25 hrs/wk for 6 months AND 8-12
   hrs/wk indefinitely** without hurting CutLog? If not — and during a CutLog 0→1 grind the
   answer is likely no — **defer** is the correct call, as the plan's own hard-stop says.

**Bottom line:** Keep the disciplined *process*; discard the optimistic *arithmetic*. This is
a fair-but-modest capped-downside cash-flow purchase that, at Hooman's budget and time, most
likely returns **a mid-teens cash yield that barely clears his own labor cost** — worth doing
only if he genuinely has idle capital he can't deploy better and is content owning a small
part-time job with resale optionality. Given CutLog needs the same scarce hours, **defer until
CutLog is past its 0→1 crunch** is the most defensible call.

---

## Sources (fetched/confirmed 2026-07-01)
- Acquire.com biannual multiples report (Jan 2026): median 3.9x profit, low-to-mid-4x avg,
  81-day avg time-to-close. blog.acquire.com/acquire-com-biannual-acquisition-multiples-report-jan-2026/
- FE International SaaS valuation: under-$2M SaaS = **5.0-7.0x SDE**; 25-acquisition sample
  churn **1-11%/mo, avg 4.7%/mo (~44%/yr)**. feinternational.com/blog/saas-metrics-value-saas-business/
- Empire Flippers financing page: states seller financing/earnouts are "by far the most common
  method" — **contradicts** the research doc's "cash is most popular" citation; leverage evidence
  is softer than either doc claims. empireflippers.com/oba/online-business-financing/
- Carried forward from `01_research_validation.md`: SaaSRanger ~18% micro-SaaS "make it";
  wearefounders.uk / shno.co ~3.5%/mo blended churn benchmark.
