# Red-Team / Plan Validation — Royalty Licensing (inventRight model)

**Date**: 2026-07-01. **Reviewer**: Claude (Opus 4.8), adversarial red-team mode.
**Docs reviewed**: `01_research_validation.md`, `02_execution_plan.md`.
**Founder**: Hooman (Adobe EM; capital $25–150K; ~10–20 hrs/wk; already building CutLog).

---

## 0. Headline

This is the most honest plan in the study. It has already done 80% of the red-team's job to
itself: it strikes the survivorship-biased income claim, disproves both cited "proofs," caps the
budget hard, and repeatedly says out loud that this is *not* the secondary income Hooman wants.
There is very little optimism left to puncture on the **downside** (the money-at-risk math is
sound and conservative).

**But the plan is still optimistic in three places that matter**, and all three point the same
direction — toward "this produces $0 and quietly eats CutLog focus for a year":

1. It systematically **under-states the TIME**, especially Hooman's *personal, non-delegable* time.
2. It treats **delegation (VA/Fiverr) as a clean time-for-money swap** — it is not; delegation of
   creative/judgment tasks adds management overhead and produces low-quality shots.
3. It **quietly reintroduces an income narrative** (Section 5's "$5–15K/mo requires a hit,"
   "windfall") that keeps a dead lottery ticket emotionally alive — the exact sunk-cost trap the
   rest of the doc warns against.

Fact-checks (below) came back almost entirely in the plan's favor — the numbers it cites are real
and, if anything, conservative. So the plan **HOLDS-WITH-CHANGES**, and the changes are about
protecting CutLog and Hooman's time, not about the money.

---

## 1. Fact-check of load-bearing claims (independent web verification)

| Claim in plan | Verdict | Evidence |
|---|---|---|
| USPTO provisional fee ~$65–130 micro-entity | **CONFIRMED** | USPTO fee schedule eff. 2025-01-19: micro $65 / small $130 / large $325. Plan's $65–130 micro is exact. |
| inventRight coaching $3,495 / $6,999 / $17,999 | **CONFIRMED (exact)** | inventright.com current pricing: Coaching $3,495, Gateway $6,999 (or 3×$2,450), APEX $17,999. |
| MarketBlast "~1,500 companies," submission fees $0–100 | **CONFIRMED (plan is conservative)** | marketblast.com: "no sign-up cost, monthly fees or commissions." So MarketBlast itself is $0; the $0–100/$300 lines are over-budgeting, which is fine. |
| No public licensing conversion rate exists | **CONFIRMED** | Neither inventRight nor MarketBlast publishes success rate, % of members who license, or average royalties. Absence of data by parties with every incentive to publish a good number = the number is not good. |
| "<10% per idea, ~3–5% commercialize" base rate | **PLAUSIBLE / consistent** | The widely-cited "~3–5% of patents are ever commercialized" rough figure is directionally consistent with the plan's <10%-per-idea assumption. No cleaner primary stat exists; treat as triangulated, not proven. |

**Net**: the plan's cost and mechanics numbers are correct and conservative. Nothing in the
budget or downside needs to get *worse*. The optimism is entirely on the **time** and **behavioral**
axes.

---

## 2. Assumptions most likely WRONG — and what happens if they are

### A. "Hooman keeps only idea selection / go-no-go / negotiation → ~2 hrs/wk" — **MOST LIKELY WRONG**
This is the plan's central time claim and it is the shakiest. The tasks the plan hands to a VA are
exactly the tasks that (a) require domain taste and (b) determine whether a shot is any good:
- **Idea generation** ("15–20 candidate improvements"): cannot be delegated — it *is* the product.
- **Prior-art scanning**: the plan calls this "the real kill filter," then delegates it to an
  $8–20/hr VA. A VA with no patent-reading skill will produce false clears (missing a design patent
  or a foreign filing) and false kills (flagging non-blocking art). Hooman will have to re-do or at
  least re-check every one, or he files provisionals on already-covered ideas and wastes the $65–325
  + weeks of pitching. Prior-art judgment is *not* a $15/hr task.
- **Sell-sheet iteration, pitch targeting, follow-up judgment**: template outreach can be VA'd; the
  *reply handling* ("is this OEM actually interested or being polite?") cannot.

**If wrong**: personal time is not 2 hrs/wk — it is realistically **4–8 hrs/wk in any active week**
(idea generation weeks, provisional-filing weeks, and any week an OEM replies), spiking higher
during negotiation. That is squarely into the range that competes with CutLog for the same evening
hours — the plan's own #1 kill-risk. The "≤2 hrs/wk" figure should be read as an aspiration, not a
forecast.

### B. "Delegation is a clean time-for-money swap" — **WRONG in the usual way**
Delegating creative/judgment work to a VA you've never worked with has a well-known failure mode:
the first 2–3 deliverables are wrong, you spend more time writing the brief + correcting than doing
it yourself, and the quality ceiling is low. For a *portfolio of 2–3 lifetime shots*, there is not
enough volume to amortize the cost of training a VA. **If wrong**: the "$900 VA" line buys worse
shots AND costs Hooman management hours — the opposite of the intended effect. For a 2–3 shot
pilot, DIY is likely both cheaper and higher-quality; the VA lever only makes sense at 10+ ideas/yr,
which the plan explicitly does not do.

### C. "Gate 0 stomach check will actually fire" — **OPTIMISTIC about human behavior**
Gate 0 asks Hooman, before spending a dollar, "am I willing to cold-pitch 30+ strangers/yr?" The
honest answer for most engineers who *dislike* cold outreach (which the research says is Hooman's
documented weakness) is "no" — but a $0, no-consequence, self-administered gate answered while
optimistic ("I'll try, how hard can it be") is trivially easy to pass in the moment and fail in
practice at pitch #4. **If wrong**: the cheapest off-ramp doesn't fire; instead the project dies
slowly at Gate 2/3 after $600–1,500 and a year of low-grade guilt/context-switching. The gate needs
a *behavioral* trigger, not a self-assessment (see §5 changes).

### D. "Provisional → real IP leverage in a pitch" — **OVER-CREDITS the provisional**
A provisional is a 12-month placeholder that is never examined and confers no enforceable rights
unless converted (~$1–3K+ and real prosecution cost/time). Sophisticated OEM open-submission
programs know this; many require you to sign away or acknowledge that submission creates no
obligation, and some will happily take a "patent-pending" idea and design around it. The plan's
provisional is real for *cost* purposes (cheap) but weak for *leverage* purposes. **If wrong** (i.e.
if Hooman assumes "patent pending" protects him): he over-shares in sell sheets and an OEM ships a
close variant with no deal. Mitigation is already partially in the plan (audit clause, don't convert
speculatively) but the *pre-deal* exposure is under-flagged.

### E. "Category = workshop/tools because he tinkers" — **THIN edge, possibly wrong category**
The research is blunt that Hooman's EE/AI depth is *not* the moat and persistence/volume is. "He
tinkers" is a weak basis for picking a category with hundreds of entrenched OEMs and sophisticated
in-house R&D (tool companies invent their own improvements constantly). **If wrong**: he picks a
saturated category where the "obvious improvements" are already patented or already shipped — which
is exactly what Weeks 5–6 prior-art will show (plan predicts 3–4 of 5 die; realistically it's 5 of 5
for obvious ideas in a mature tool category). Not fatal, but it means the pilot likely produces zero
prior-art-clear ideas without much deeper category-specific insight than "I tinker."

### F. Section 5 reintroduces the income fantasy — **BEHAVIORALLY DANGEROUS**
Sections 0 and 7 correctly say "plan around zero." Then Section 5 says "$5–15K/mo requires a hit…
3–5 year (or never) horizon" and calls returns a "windfall." Restating the jackpot — even hedged —
keeps the lottery emotionally alive and is precisely how sunk-cost spirals start ("I'm only 2 ideas
in, the big one could be idea #7…"). The plan's own stop-loss is undermined by its own revenue
section. **If this framing wins**: Gate 2/3 get rationalized past, the $6K cap creeps, and the
"never steals hours from CutLog" rule erodes idea-by-idea.

---

## 3. Independent financial sanity-check — where it's optimistic, rebuilt conservatively

The **money downside is genuinely sound** — this is the plan's strongest part. The optimism is in
**time** and **expected value**, not dollars-at-risk.

### 3a. Cash — plan is CONSERVATIVE (good)
- Provisional fees confirmed cheaper than budgeted; MarketBlast confirmed free. The $600 DIY /
  $6,200 delegated caps are safe. No correction needed downward. If anything, a true DIY 2–3-idea
  pilot lands at **~$300–900 all-in** (fees + Fiverr sell sheets + prints), well under $600–6,200.

### 3b. Time — plan is OPTIMISTIC (correct this)
| Task | Plan implies | Conservative reality |
|---|---|---|
| Learn model (wks 1–2) | ~6 hrs (one-time) | 8–12 hrs (book + curated YouTube). One-time, fine. |
| Idea gen + filter (wks 3–4) | delegable-ish | **4–6 hrs, non-delegable** (it's the product). |
| Prior-art scan | VA'd | VA builds lists; **Hooman re-checks: 1–2 hrs/idea non-delegable.** |
| Provisional drafting | ~cheap/fast | A *good* provisional (claims + drawings) is **3–6 hrs each** if self-done; a $65 filing with a bad spec has near-zero value. |
| Sell sheet + outreach | Fiverr/VA | Brief-writing + correcting VA + reply-handling **2–4 hrs/active idea**. |
| **Personal load, active weeks** | **~2 hrs/wk** | **~4–8 hrs/wk**, spiking to 8–12 during filing/negotiation weeks. |

The "≤2 hrs/wk" is achievable *only* in the passive weeks between milestones — not in the weeks that
actually move the ball. Averaged over a year it might be ~2–3 hrs/wk, but it is **lumpy and lands in
exactly the evening slots CutLog needs**, which is what matters given the stated constraint.

### 3c. Expected value — plan's own numbers, made explicit
Using the plan's own base rates (≤10% per idea licenses; a licensed product base case $0–$6K/yr;
a meaningful hit is rare):
- **2–3 idea pilot**: P(≥1 license) ≈ 1 − 0.9³ ≈ **~27%**, but most of those are the $0–6K/yr kind.
- **Expected annual royalty from the pilot** ≈ 3 ideas × ~8% license × ~$3K/yr expected-given-license
  ≈ **~$700/yr**, dominated by a tiny probability of a large hit. Modal (most-likely) outcome = **$0**.
- **10–15 lifetime ideas** (well beyond this pilot): expected ~1–2 licenses, expected annual value
  still **low-thousands**, modal outcome still $0, with a long-shot tail into real money.

**Honest revised monthly profit**: **$0/mo in year 1** (near-certain). **$0–a few hundred $/mo**
expected across years 2–3 *if* the pilot is extended into a 10+ idea portfolio (heavily
right-skewed: most-likely $0, small chance of a genuine hit worth $5K+/mo). As a *reliable* monthly
income: **$0**. The plan already says this; the correction is only to strip the "$5–15K/mo … windfall"
language that makes $0 feel like a near-miss instead of the expected result.

---

## 4. Does it REALLY stay within 10–20 hrs/wk? — Yes for the ACTIVITY, but it targets the WRONG hours

Two separate questions:

- **Total hours**: Yes. Even at the conservative 4–8 hrs/wk active / ~2–3 hrs/wk averaged, this fits
  well inside Hooman's 10–20 hr/wk budget in raw magnitude. It does **not** secretly need full-time
  attention — it is genuinely a part-time-feasible activity.
- **WHICH hours**: This is the real problem, and the plan flags it but under-weights it. Both CutLog
  and this consume **the same scarce, high-focus evening/weekend engineering-brain hours** — not
  fungible "any 10 hours." A cold-outreach follow-up, a negotiation email, or a prior-art re-check
  lands in the exact slot Hooman would otherwise ship CutLog features. So while it *fits* the hour
  budget, it does **not** fit alongside CutLog without measurably taxing CutLog — which the plan's own
  stop-loss admits is the halt condition.

**Verdict on §3 of the prompt**: Stays ≤20 hrs/wk comfortably. Does **not** stay ≤2 hrs/wk personal
as claimed (realistically 4–8 in active weeks). Does **not** coexist with CutLog cost-free — it
spends CutLog's specific hours, not spare ones.

---

## 5. Does the plan hold? — **HOLDS-WITH-CHANGES**

The plan holds *as written for its stated purpose* (run this correctly if run at all, as a bounded
lottery ticket) because it already refuses to promise income. It needs these changes so its own
guardrails actually fire:

1. **Replace Gate 0 self-assessment with a behavioral trigger.** Before ANY spend, require Hooman to
   actually send **5 real cold pitches** (existing simple idea, free MarketBlast + email) in Week 2.
   Kill on *revealed* behavior — did he do it and not hate it — not a hypothetical yes. This is still
   $0 and is a far harder, more honest off-ramp.

2. **Drop the VA delegation for a 2–3 idea pilot; do it DIY or don't do it.** Delegation only pays
   off at 10+ ideas/yr. For a pilot, a VA buys worse shots plus management overhead. Reserve
   delegation strictly for pure-clerical Fiverr sell-sheet graphics. This also removes the fiction
   that personal time drops to 2 hrs/wk.

3. **Cut or quarantine Section 5's income language.** State the expected outcome as **"$0, full stop;
   any royalty is a statistical accident, not a plan."** Remove "$5–15K/mo," "windfall," and the
   3–5-year ramp from the operating plan (keep them only in the research doc as *disproven claims*).
   This closes the sunk-cost door the rest of the plan tries to lock.

4. **Add a hard CutLog-primacy metric to the stop-loss, measured not felt.** "CutLog momentum
   measurably slips" is unmeasurable as written. Define it: e.g., *if CutLog ships zero user-facing
   changes in any 2-week window while royalty work was active → halt royalty work immediately.* Tie
   the halt to a CutLog output metric, not a self-report of vibes.

5. **Reframe the provisional's role honestly in the pitch section:** it is a cheap 12-month timestamp
   with weak pre-deal protection; do not over-share proprietary detail in sell sheets, and never
   assume "patent pending" prevents an OEM from designing around it.

6. **Shrink the pilot to sharpen the test.** 2–3 ideas is fine, but front-load to **ONE** idea all
   the way through pitch #10 before starting idea #2. The fastest, cheapest information is "does a
   single clean shot get *any* reply?" — buy that signal for ~$300 and one quarter before spending
   more time or money.

**Bottom line**: The economics are honest and the downside is genuinely small — Hooman cannot lose
more than ~$1K and some evenings. It **HOLDS** as a $300–900 DIY curiosity bet with a real behavioral
kill-gate. It **does not hold** as anything Hooman should let touch CutLog's calendar, and it must be
stripped of the residual income fantasy that would otherwise keep a dead ticket alive. The single
biggest risk is not money — it's a year of low-grade context-switching that quietly slows the one
asset (CutLog) that actually fits his profile.

**Confidence: HIGH** on the money/mechanics (independently verified: USPTO fees, inventRight pricing,
MarketBlast-free, no published conversion rate). **MEDIUM** on the exact time estimates and base-rate
EV (triangulated, no clean primary conversion statistic exists — by design of an industry that would
publish a good number if it had one).
