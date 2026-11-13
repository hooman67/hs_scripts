Daily portfolio price-action, allocation-gap and news review for Hooman. Inspects every holding and watchlist name, but reports a concise prose decision brief instead of repeating the full per-stock return tables. Read-only.

Usage: /fin_check

## Philosophy (READ THIS — updated 2026-11-05)

Hooman wants a concise decision brief rather than the same large table of every stock's 1d / 3d / 5d /
20d move on every invocation. The workflow must still inspect every holding and watchlist name so a
material move or underweight opportunity cannot be silently missed. Summarize the material evidence,
allocation decisions, catalysts and entry gates in prose.

**Do not print the full per-stock return tables.** Action/accounting tables such as the profit-exit
queue, legacy-exit cost check, or compact sleeve-gap table remain useful. The omitted quote tables do
not permit cherry-picking: inspect the complete script output internally and mention every material
mover, data error, actionable position and underweight sleeve.

## Steps

1. **Pull and inspect the full data set:**
   ```bash
   /opt/venv/bin/python3 ~/.claude/scripts/fin_check.py
   ```
   Prints EVERY holding + watchlist name grouped by role, each with **1d / 3d / 5d / 20d** moves + a
   flag on big movers, then the SIZING block (sleeve over/underweight + $), then AUTO-FLAGS. Inspect
   all of it as working evidence.
   (`--movers` filters to notable moves only; `--json` for machine-readable. Default = show everything.)

2. **Return a prose decision brief.** Do not relay the full macro, held-core, exit-queue, speculation,
   or buy-watchlist return tables. Lead with the phase read, what changed, decisions, and the most
   relevant current prices/moves. Include exact figures where they support a decision. Mention quiet
   names only when their allocation, entry gate, thesis or data quality matters.

3. **Check news on the movers** (names up or down >~3% on the day or >~5-6% on the week, plus any big
   holding). Use WebFetch on `https://html.duckduckgo.com/html/?q=<query>` (follow the 302 to
   html.duckduckgo.com). Oil/Iran/Hormuz, Fed/rates, single-stock earnings. **CRITICAL: verify magnitude
   against the live price — past hyped "oil to $120" headlines clashed with the actual ~$73 spot. Anchor
   to the price.** Add a one-line news note next to the movers it explains.

4. **Interpret the complete data:** explain which names are notably up (trim candidates if their sleeve
   is overweight), notably down (possible buys only if their sleeve and thesis permit it), and affected
   by fresh news. Sleeve over/underweight comes from the SIZING block. Every buy/trim note carries a
   dollar figure. Hooman decides; you inform.

   **Required allocation review — added at Hooman's request, 2026-10-16.** Give every current
   target sleeve an explicit **BUY SMALL / WAIT / HOLD / REDUCE / DATA UNVERIFIED** judgment,
   with current versus target weight, the dollar gap, a concise reason and what would change the
   judgment. Quiet price action must not exclude a sleeve. End with the preferred purchases, if any,
   proposed tranche dollars/shares and funding source; distinguish a recommendation from an order.

   Always assess these separately, even when they do not meet the mover threshold:
   - **Healthcare:** review VHT, IHI, CI and LLY against their latest accepted individual targets
     and entry rules. A sleeve shortfall is not permission to add to an already-full constituent.
   - **Emerging markets / China:** review broad VWO separately from KWEB/BABA concentration; assess
     country, currency, valuation and earnings risks rather than treating all EM as one China trade.
   - **Ex-U.S. core:** review VXUS separately from VTI. VXUS includes both developed and emerging
     markets; count its overlap with VWO and other foreign holdings before suggesting both.

   **Required underweight watch — user-confirmed 2026-10-28.** Include a clearly labeled special-watch
   section on every run. Start from every live target sleeve below target, rather than a hard-coded
   historical list, and state current/target weight, dollar shortfall, preferred implementation,
   present judgment, entry trigger and any wash-sale/data constraint. Give added attention to:
   - **Healthcare:** VHT, IHI, CI and LLY.
   - **Build Canada:** CGY.TO, EFX.TO, BDGI.TO, VNP.TO and FTG.TO, while retaining their existing
     economic-sleeve mappings and avoiding double-counting them as a separate allocation sleeve.
   - **China / broad EM:** MCHI, KWEB, BABA, IEMG and VWO; separate broad EM from China concentration.
   - **Uranium / nuclear:** NLR, CCO.TO, CEG, UROY and any blocked direct-name repurchase candidates.

   These are priority monitoring groups, not standing buy orders. A target gap alone is not a buy
   signal; specify what price, valuation, catalyst or macro change would justify the next tranche.

   Separate **sensible staged allocation at today's price** from **a special tactical bargain**.
   A large red day is not required for the former, and a drawdown or target gap does not prove the
   latter. Use dated issuer valuation/composition evidence and relevant current developments; expose
   stale or unavailable inputs. Compare like-for-like valuation measures and do not describe USD
   trading currency as USD-only economic exposure or describe foreign equities as principal protection.
   Keep any proposed tranche within both the individual/sleeve target and the household's deployable
   risk budget. If recommending an exception to the standing cash-deployment timing, state it explicitly
   as a proposal; do not silently change policy. A blanket "hold cash" answer requires a substantive
   explanation for each of these three spaces. A "no buy" judgment must identify the actual constraint
   or evidence and the next review condition, rather than relying only on the day's percentage move.

   **Required signal and recommendation scores — user-confirmed 2026-11-05.** Inspect the complete
   holdings and watchlist universe and report every non-neutral buy or sell signal, including signals
   that cannot be acted on because a sleeve or individual-name allocation is full. Keep two distinct
   layers so portfolio constraints never hide an attractive or dangerous security:

   - **Raw security signal:** `STRONG BUY`, `MEDIUM BUY`, `WEAK BUY`, `NEUTRAL`, `WEAK SELL`,
     `MEDIUM SELL`, `STRONG SELL`, or `DATA UNVERIFIED`. Judge the security, ETF or commodity on
     current valuation/price versus its recorded gate, thesis quality, fresh fundamentals, catalyst
     durability, macro fit and downside. Ignore current sleeve capacity, current position size and
     funding availability for this raw signal. Do not ignore stale evidence, a broken thesis,
     instrument defects, liquidity, wash-sale restrictions or tax/account facts that make the
     purported signal invalid or unexecutable.
   - **Portfolio action:** retain `BUY SMALL / WAIT / HOLD / REDUCE / DATA UNVERIFIED`, and score every
     explicit buy, reduce or sell recommendation `STRONG / MEDIUM / WEAK`. This layer incorporates
     sleeve and name targets, overlap, concentration, house/job reserve, tax location, wash-sale
     restrictions and the funding source. It may therefore say, for example, `STRONG BUY signal;
     WAIT — sleeve full`.

   Use `STRONG` only when the recorded valuation/price gate is met or exceeded and current evidence
   independently confirms the thesis, or when a sell has a clear thesis break, mandatory standing
   trigger or material risk excess. Use `MEDIUM` for an attractive staged allocation with sound but
   incomplete evidence or a meaningful rebalance. Use `WEAK` when the direction is favorable but the
   valuation gate, evidence, magnitude or timing is marginal. A large red or green day by itself is
   never a strong signal. Briefly state why the grade applies and what would upgrade, downgrade or
   reverse it.

   Lead the decision brief with a compact ranked signal list. Include blocked signals explicitly with
   the blocking constraint. End with executable recommendations separately, including strength,
   dollars/shares and funding source. Do not turn raw signals into orders, change targets, or conceal
   `DATA UNVERIFIED` behind a conviction grade.

5. **Check the full exit queue against recorded cost every run.** For every exit holding, show current
   value, aggregate recorded cost basis, nominal P/L dollars, and label it **ABOVE COST** or **BELOW
   COST**. Explicitly identify which positions can currently be sold without a nominal loss. Treat this
   as an aggregate accounting check before commissions and taxes, not tax-lot advice; account-specific
   tax lots can differ, and losses inside an RRSP are not deductible.

6. **Sell-on-profit queue — user-confirmed 2026-10-15.** Every holding currently classified as
   `Speculation` is a conditional full-exit candidate as soon as it is above its recorded average
   purchase cost. The initial queue is LULU.TO, TTD, NKE, CLX, SHOP.TO, UBER, ASTS and FIS. The script
   pins those names so a sleeve-label change cannot silently remove the exit instruction; newly held
   Speculation names are also included automatically. Sold/zero-share positions are not displayed.

   Show the script's complete `SELL WHEN PROFITABLE` table every run, with shares, quote and average
   cost in the same currency, nominal P/L, quote date, and either **PROFITABLE — SELL CANDIDATE**,
   **BELOW COST — WAIT**, **AT COST — WAIT FOR PROFIT**, or an explicit data-verification warning.
   This is strictly positive price profit before unrecorded selling costs/taxes/dividends. CAD gains
   translated at today's FX are not historical-FX tax gains. Check broker lots, executable bid and
   fees before declaring that a sale will net a profit. Missing/stale quotes, unknown costs/currencies
   and fallback holdings must never produce a current sell trigger.

   Lead with profitable candidates, including on quiet price days. Never issue generic dip-buy/add
   recommendations for this queue. Retain Speculation classification and existing allocation targets
   while positions await sale; the legacy exit queue keeps its own rules. This is monitoring on each
   invocation, not continuous monitoring or an automatic brokerage order. The user's new condition
   governs these queued positions; flag any competing thesis-break/cap concern separately rather than
   silently converting a below-cost position into an immediate sale.

7. **Show every RESEARCH WATCH block emitted by the script.** These names have accepted research but no
   allocation target and are not automatic buys. For SOXQ, retain the accepted semiconductor rules:
   wait above $85; at or below $85 reassess for an up-to-0.5% starter; near $79-$80 reassess for a second
   tranche; cap the tactical overweight at 1.0% and fund it by substituting for VTI/JQUA rather than
   creating a new permanent sleeve. A price trigger requires fresh fundamental confirmation.

   For LRCX and KLAC, retain the 2026-11-02 accepted Quality-sleeve rules: keep 5.5% JQUA by default;
   re-underwrite LRCX around $205 or approximately 22x confirmed forward GAAP earnings and KLAC around
   $140 or approximately 25x comparable GAAP earnings. These are review gates, not orders. Any future
   direct position replaces JQUA dollar-for-dollar; LRCX is capped at 1.0%, combined LRCX plus KLAC at
   1.5%, and the user's 2% single-company cap remains a hard maximum.

8. **Do NOT execute or edit records.** Hooman trades in his brokerage, then tells you the fills; only
   then do you log them (manual dashboard update, not this skill).

## ⚠️ STAGFLATION PLAYBOOK (2026-07-26 — Hooman's macro game-plan; apply this to every read)

Hooman's base-case macro path is an **oil-shock stagflation**, in two phases, and it dictates the
timing of buys/sells. **Every daily read must be interpreted through this lens — say which phase we
appear to be in and what it implies.**

| Asset | Phase 1 (oil spike, inflation ↑) | Phase 2 (demand destruction / recession) | Grade |
|---|---|---|---|
| **Gold** | ✅✅ strong | ✅ often strong | **A — best; now 14% target** |
| **Energy stocks** | ✅✅ (the cause — he's long) | ⚠️ demand destruction hits them | **B, front-loaded** |
| VTIP | ✅ good | ✅ good | A− (but Hooman REJECTED it → moved to gold) |
| IEF | ❌ bad (yields ↑) | ⚠️ maybe (only if Fed cuts) | C — coin-flip |
| Cash/SGOV | ⚠️ loses to inflation | ⚠️ loses to inflation, BUT = dry powder | C nominal / **strategic** |
| **Broad equities (VTI)** | ❌ bad | ❌❌ worst (earnings + multiple compress) | **D — worst** |

**The rules that follow from this table (enforce them):**
1. **SELL energy into Phase-1 strength, and SELL energy HARD when Phase-2 / demand-destruction starts**
   (oil rolling over from a spike, demand/recession signals). Energy is front-loaded — don't ride it into
   the demand-destruction leg. This is the single most important timing call.
2. **HOLD CASH as dry powder — do NOT deploy the cash pile into broad equities yet.** Equities are the
   worst stagflation asset; the plan is to wait for the recession and buy the crash. So on the BUY side,
   **do NOT push "deploy cash into VTI/VXUS" as urgent** — the DCA of the core is deprioritized until a
   real drawdown. Small opportunistic adds to gold / cheap-quality on big dips are fine; wholesale
   equity deployment is NOT.
3. **Gold is the anchor** (14% target) — add on gold weakness, it works in both phases.
4. **Phase read:** each run, note oil trend (spiking = Phase 1; rolling over + weak demand = Phase 2
   turning) and flag if it's time to sell energy / start deploying the dry powder.

### 🔔 MELT-UP / CASH-DRAG WATCH — REQUIRED every run (the counter-check to holding cash)

The wait-for-the-crash plan has ONE big failure mode: **the market melts up for months/years and the
~52% cash pile badly lags.** Hooman EXPLICITLY asked to be reminded of this so he doesn't sleepwalk into
a costly cash drag. **Every run, compute and show a one-line "Melt-up watch" verdict.** Method:

- Look at VTI's trend (the script prints 1d/3d/5d/20d; also eyeball the ~20-day and, if you want, pull a
  longer lookback). Rough triggers to WARN on:
  - **VTI up >~8% over ~20 trading days** (a sustained melt-up, not a bounce), OR
  - **VTI at/near a 52-week high AND up 3 of the last 4 weekly reads**, OR
  - **it's been ≳2-3 months of the cash sitting idle while VTI kept climbing** (no recession in sight).
- If ANY trigger fires, print: **"⚠️ MELT-UP WATCH: market up X% over ~N days with no recession — the
  cash-heavy stance is now costing you. Consider (a) starting a measured DCA of the core after all, or
  (b) consciously reaffirming the wait — but decide, don't drift."** Then it's Hooman's call.
- If no trigger: print a short **"Melt-up watch: OK — no sustained melt-up; holding cash still cheap."**
- The point is a FORCED periodic gut-check: cash-as-dry-powder is a market-timing bet, and this line
  stops it from silently becoming a permanent, unexamined drag. Never omit this line.

## Current-source precedence

Use live holdings and the full live target grid; verify target weights sum to 100%. Display quote
currencies and dates, calculate 20d from 20 trading observations, and expose stored-price fallbacks.
Current user-confirmed decisions override historical targets and biographical assertions below.
Research proposals are not accepted allocation changes. Preserve `FR_Portfolio!E1:K23` user notes.

## Reference — targets & context (updated 2026-07-26; update as the plan evolves)

- **Target sleeves** (% of total): Cash 20.5 / Global-equity-core 20 (VTI 11 + VXUS 9 + AVUV tilt) / EM 5
  / Quality 8 / **Energy 9** / **Gold 14** / Utilities 4 / Financials 3 / Uranium 3.5 / Copper 3 / Ag 3 /
  Healthcare 2 / Defense 2 / Crypto 2 / Silver-Plat 1. **(Dropped the 5% Short-TIPS/VTIP sleeve → moved to
  Gold, 9%→14%.)** SIZING block computes live over/underweight — trust it over this list. Full model:
  `fin_research/portfolio/ideal_allocation.md`.
- **State:** cash ~52% = DRY POWDER (held for the recession, NOT to deploy into equities now); energy near
  target (sell into strength / Phase-2); metals/uranium overweight (trim into strength); gold underweight
  vs the new 14% target (add on weakness).
- **Per-name targets** live in the dashboard "Name Tgt %" column (seeded from research/name_targets_*.md).
- **Buy the US-div core (VTI/GOOGL) into RRSP once it has USD** (withholding shelter); VXUS in taxable (FTC).
- **Standing biases:** trim into strength; the cash is dry powder (don't rush equities); Adobe (~57% of
  net worth) makes US-tech adds low-priority. Inspect everything regardless of bias and report the
  decision-relevant result without repeating the full quote tables.

## Notes

- Read-only. Shows data + context; Hooman decides & executes.
- Watchlist auto-loads the full holdings from the dashboard source + a MACRO and BUY_WATCHLIST list.
  To evolve the buy-watchlist or macro tickers, edit the lists at the top of `~/.claude/scripts/fin_check.py`.
- Research-watch names are informational and deliberately excluded from SIZING targets.
- Prices via GOOGLEFINANCE/yfinance; #N/A on a ticker is usually transient throttling, flagged inline.
