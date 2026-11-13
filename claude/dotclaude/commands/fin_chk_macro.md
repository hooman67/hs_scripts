---
name: fin-chk-macro
description: Macro-thesis, portfolio-allocation and full-history transaction-behavior validation for Hooman; monthly delta or requested full audit. Creates a dated evidence report, proposes thesis changes, and never trades or changes allocations during the review.
---

# Fin Macro Check

Usage: `/fin_chk_macro`

Run a rigorous monthly review of Hooman's macro beliefs, the evidence supporting them, and his complete
recorded trading behavior. The default run re-researches only theses whose evidence, triggers, or market
conditions changed or weakened. It still displays every thesis and its original factual basis. A full
fresh revalidation runs when Hooman requests `full` or asks in natural language to validate the entire
allocation, its assumptions, and its logic. That request is sufficient authorization; do not ask again.

This workflow is research and portfolio-process review. It never places trades and does not change
live allocation targets or calculate final order sizes during the initial report. When allocation validation
is requested, include report-only allocation alternatives, target dollars, and risk comparisons now;
these are proposals, not accepted policy or trade instructions.

## 1. Load the durable project and live state

Read `/home/colligo/hs_scripts/claude/dotclaude/RESEARCH_RULES.md` completely and follow it.

Read these current project records before analysis:

1. `/home/colligo/hs_scripts/claude/fin_research/portfolio/CLAUDE.md`
2. `/home/colligo/hs_scripts/claude/fin_research/portfolio/PROJECT_STATE.md`
3. `/home/colligo/hs_scripts/claude/fin_research/portfolio/DECISIONS.md`
4. `/home/colligo/hs_scripts/claude/fin_research/portfolio/LEARNINGS.md`
5. `/home/colligo/hs_scripts/claude/fin_research/portfolio/PHASE1_AUDIT.md`
6. `/home/colligo/hs_scripts/claude/fin_research/portfolio/ideal_allocation.md`
7. The prior macro-monitor report and summary, if they exist under
   `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/`.

Pull the live portfolio before drawing conclusions:

```bash
/opt/venv/bin/python3 /home/colligo/hs_scripts/claude/dotclaude/scripts/fin_check.py --json
```

The live sheet is authoritative when available. Never edit or overwrite the user-maintained
`FR_Portfolio!E1:K23` notes area. Reconcile the complete live target grid to 100%, independently of
script hardcoded sleeve names. Label live targets, accepted decisions, historical models and proposals
separately; surface conflicts instead of picking whichever supports the conclusion.

Verify holdings quantities, quote dates/currencies, cash by account, and total-value arithmetic. A CAD
record of a USD-quoted asset requires conversion only once. Distinguish bullion from futures quotes,
and stale stored prices from live prices. A missing quote or silent JSON fallback must remain visible;
never use a stale or incomplete source to produce precise allocation orders. Audit corrections may be
computed in a separate dated working artifact without altering the live sheet.

## 2. Build the complete thesis register

Inventory every recorded macro or cross-portfolio belief, including active, rejected, superseded,
conditional, and monitoring-only theses. Do not silently omit a belief because it appears stale.

At minimum, inspect the relevant sections of:

- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_usd_decay.md`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_energy.md`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_supercycle_metals.md`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_metals_uranium.md`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_ai_thesis.md`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_china.md`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/STAGFLATION_THESIS_AND_KIE_2026-08-26.md`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/FERTILIZER_SHORTAGE_THESIS_2026-08-27.md`
- Other accepted sector or thematic research referenced by `DECISIONS.md` or `PROJECT_STATE.md`.

For each thesis, report these fields separately:

| Field | Meaning |
|---|---|
| Thesis | Precise, falsifiable claim rather than a slogan |
| User conviction | Hooman's recorded High / Medium / Low conviction |
| Evidence confidence | High / Medium / Low confidence based on source quality and freshness |
| Status | Strengthening / Stable / Weakening / Refuted / Unresolved |
| Original facts | The facts and assumptions actually used when the decision was made |
| Evidence date | As-of date for the decision-driving evidence |
| Portfolio expression | Current holdings and allocation rules implementing the thesis |
| Confirming signals | Observable facts that would strengthen it |
| Invalidation signals | Observable facts that would weaken or reverse it |
| Last material change | What changed since the previous macro check |

Do not merge user conviction with evidence confidence. A strongly held belief can have weak evidence,
and strong evidence can support a thesis the user holds with low conviction.

## 3. Decide what requires fresh research

The default monthly run researches only changed or weakening theses. Treat a thesis as requiring fresh
validation when any of these apply:

- a recorded confirming or invalidation trigger was crossed;
- a new official dataset, filing, policy decision, forecast, supply/demand report, or market regime is
  material to the thesis;
- a key price, spread, valuation, rate, inventory, production, demand, or positioning variable changed
  enough to challenge the prior conclusion;
- decision-driving evidence is stale for its natural publication cadence;
- current holdings or transactions materially increased exposure to the thesis;
- reputable new evidence contradicts the prior record; or
- the prior thesis had unresolved or low-confidence evidence gaps that can now be tested.

List stable theses and why no fresh work was necessary. Do not manufacture activity merely to make the
monthly report look comprehensive.

If this is the first run and no prior macro-monitor baseline exists, reconstruct the complete register,
identify stale or vulnerable evidence, research those items, and explicitly ask whether Hooman wants a
full fresh baseline audit of every thesis.

If Hooman invokes `/fin_chk_macro full` or requests full allocation/assumption validation in ordinary
language, freshly test every decision-driving thesis, including evidence gaps in previously accepted
research. Do not interpret a prior VERIFIED label as fresh source verification.

## 4. Research the changed and weakening theses

Use the source and evidence rules in `RESEARCH_RULES.md`:

- Prefer primary sources: official statistics, central banks, government agencies, company filings,
  regulators, index providers, industry bodies, and direct datasets.
- Use reputable secondary sources for context, not as a substitute for available primary evidence.
- Open every decision-driving source; search snippets are discovery only.
- Record full working URLs, publication dates, retrieval date, scope, and limitations.
- Cross-check important single-source claims and recompute material arithmetic.
- Search specifically for contrary evidence and at least one credible alternative explanation.
- Clearly label `VERIFIED`, `DERIVED`, `REPORTED`, `UNVERIFIED`, and `USER-CONFIRMED` claims.
- Preserve unresolved contradictions instead of averaging them into false certainty.

Independent thesis updates and transaction analysis may run in parallel when their inputs are already
fixed. Only the main integrator may edit the dated report or canonical portfolio records.

## 4a. Full allocation validation when requested

Use the user's latest answers for priorities, residence/tax status, liability currencies, time horizon,
reserve access, income dependence and loss tolerance. Do not repeat answered diagnostic questions. If
risk tolerance is unknown, help derive it from dollars lost, spending reserves and acceptable delay of
the house purchase; run labeled sensitivities while asking for missing spending information.

- Separate immediately available cash, retirement accounts, saleable employer stock, unvested
  compensation and contingent family reserves. Unvested grants are employment-linked future income,
  not spendable net worth. A cumulative vested counter is not a current share balance.
- Separate domestic purchasing-power inflation, FX depreciation, gold appreciation and house-price
  changes. Match safe reserves to the currency/date of the liability; a listing currency is not an
  economic currency hedge. Prioritize the user's stated objectives rather than maximizing equity return.
- Look through overlapping issuers/funds and distinguish bullion, miners/streamers, futures, utilities,
  nominal duration and inflation-linked bonds. Revenue shares are illustrative business exposure, not
  exact asset betas. Do not call utilities, gold or commodity equities principal-stable reserves.
- Compare current holdings, complete live targets, and simpler alternatives with explicit budgets. Show
  matched-risk comparisons where possible; do not attribute all improvement to simplicity if the
  alternative also holds more safe assets. Explain each hedge's adverse regime and opportunity cost.
- Test demand-driven recession, inflation/supply shock, disinflation/recovery and simultaneous job loss
  with asset declines. Include rate/FX shocks and a conditional house purchase. Disclose all assumed
  shocks; they are scenarios, not forecasts or maximum losses. Historical tests must use available
  histories/proxies honestly, include total returns and avoid deriving safety from one quiet window.
- Use after-tax yield and maturity matching when comparing cash/TIPS/nominal bonds. Inflation-linked
  funds still have duration; nominal bonds can fall when inflation/term premia rise. Explain futures
  roll/collateral returns and daily-reset leveraged/inverse risks where held.
- Give defensible ranges and budget arithmetic; a precise weight requires a stated judgment or model.
  Unsupported conviction scores multiplied by evidence scores are not portfolio optimization.

## 5. Reconstruct all recorded transactions

Analyze all recorded history on every run, not only the latest month. Start with:

- `/home/colligo/hs_scripts/claude/fin_research/portfolio/positions/ledger.csv`
- Transaction and fill entries in
  `/home/colligo/hs_scripts/claude/fin_research/AUDIT_CHECKPOINT.md`
- Accepted decisions and dated implementation notes in
  `/home/colligo/hs_scripts/claude/fin_research/portfolio/DECISIONS.md`
- The current live holdings returned by `fin_check.py --json`.
- Relevant Git history when needed to reconstruct what the portfolio rules or records said at the time.

Use `.bak` files only to reconcile a discrepancy; never treat them as an additional transaction source
or double-count their rows.

Normalize each identifiable transaction into:

- trade date and time when available;
- ticker and security name;
- buy, sell, trim, add, close, or adjustment;
- quantity and fill price;
- currency and account;
- sleeve and thesis served;
- stated rationale and applicable decision rule at the time;
- intended funding source or redeployment, when recorded;
- whether the action matched the then-current target, cap, entry rule, and exit rule; and
- data gaps or reconciliation conflicts.

Reconcile the reconstructed history against current holdings. Surface missing fills, inconsistent share
counts, ambiguous currencies, duplicate records, and transactions known only through narrative notes.
Do not invent missing transaction details. If the ledger is absent or overwritten, report coverage as
all available identifiable events, not all actual trades. Mark prior-report-only entries as unverified
until supported. Cash/basis changes are not automatically trades; fund conversions and duplicates
require reconciliation. A cluster of trades can implement one planned rebalance and is not by itself
evidence of harmful overtrading.

## 6. Analyze decision behavior without hindsight bias

Separate decision quality from subsequent return. A profitable trade can have violated the process, and
a losing trade can have followed a sound process.

Evaluate patterns including:

- compliance with allocation targets, position caps, funding rules, and accepted theses;
- chasing recent strength versus buying planned weakness;
- trimming strength versus waiting for break-even;
- loss aversion, anchoring to cost, and delays in clearing the exit queue;
- premature selling of high-quality compounders or winners;
- averaging down without fresh thesis validation;
- repeated tactical trades that gradually create an unintended permanent sleeve;
- starter-position and speculation-cap discipline;
- overreaction to one-day price moves or headlines;
- concentration, overlap, and repeated exposure to the same macro bet;
- account-location, tax, currency-conversion, and withholding efficiency;
- uninvested sale proceeds and deviations from the stated funding source;
- time from recorded decision to execution, when observable; and
- whether recent trades reduced or increased the portfolio's largest known risks.

Where price history is available, calculate pre-trade and post-trade returns over useful windows such as
5, 20, and 60 trading days. Use them only as contextual evidence, not as proof that a decision was good
or bad.

Do not diagnose emotions or personality. Label a behavioral pattern `SUPPORTED` only when multiple
independent transactions demonstrate it. Label fewer observations `POSSIBLE` and show the examples.
Also identify positive habits worth preserving.

## 7. Create the dated report

Create one Markdown report per run at:

`/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/reports/YYYY-MM-DD_macro_check.md`

If more than one run occurs on the same date, append `_HHMM` using local Pacific time. Never overwrite a
prior completed report. Resume the same unfinished run in its existing working report; update the
project audit checkpoint after substantive batches so interruptions do not restart research.

Mark the report `PENDING USER REVIEW`. Include:

1. Executive conclusions and the most decision-relevant changes.
2. Complete thesis dashboard covering every belief.
3. Fresh evidence for changed or weakening theses.
4. Stable theses not re-researched and the reason each remained stable.
5. Contradictions, false assumptions, stale facts, and unresolved evidence gaps.
6. Current portfolio exposures tied to each thesis.
7. Complete transaction reconstruction and reconciliation summary.
8. Supported and possible behavioral patterns with concrete examples.
9. Positive process habits worth preserving.
10. Recommendations ranked by evidence, impact, reversibility, and urgency.
11. Proposed thesis-record changes shown explicitly as old state → proposed state.
12. Full source log with working URLs and absolute local paths.
13. The cheapest next validation step for every material uncertainty.
14. When allocation validation is requested: current-versus-target economic exposures, stress assumptions
    and results, emergency/house funding capacity, and report-only alternatives tied to user priorities.

Use compact tables and a visible confidence legend. Report facts, interpretations, and recommendations
separately. Do not hide adverse or contradictory evidence.

The canonical ongoing thesis register belongs at:

`/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/SUMMARY.md`

Do not change that summary, `DECISIONS.md`, `PROJECT_STATE.md`, `LEARNINGS.md`, allocation targets, or
buy/sell records until Hooman has reviewed the dated report.

## 8. Present findings for review

Complete the authorized audit and clearly distinguish proposed thesis/policy changes from accepted
records. Keep the dated report by default; delete it only on explicit request. Do not ask whether to
expand to a full review when full review was already requested.

Ask only for unresolved user choices or approval of concrete proposed changes to canonical investment
records. Explain the relevant boundary: this skill requires review before changing those records.
Report-only allocation validation does not require an extra approval phase. Execution planning can
follow an explicit request using refreshed holdings, account restrictions and tax lots; never trade.

After the user accepts specified changes, merge those changes into the latest canonical records and
show what changed. Do not require repetitive confirmation of work already authorized.

## 9. Monthly scheduled-task contract

The intended scheduled run is a standalone monthly task in the local project, so the dated report is
written to the main finance-research checkout.

Suggested task prompt:

```text
Run $fin-chk-macro in /home/colligo/hs_scripts/claude/fin_research. Perform the default monthly delta review of changed or weakening macro theses and the full-history transaction-behavior audit. Create the dated PENDING USER REVIEW report. Do not update canonical thesis records, allocation targets, or trades until I review the report.
```

Suggested Pacific-time cadence: first weekday of every month at 9:00 AM.

```text
RRULE:FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=1;BYHOUR=9;BYMINUTE=0
```

Scheduled runs require network access for fresh research and local-project access to create the report.

