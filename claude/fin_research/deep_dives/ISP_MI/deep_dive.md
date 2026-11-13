# Deep Dive — Intesa Sanpaolo (ISP.MI) — Bank, Italy

**Stage 4 finalist deep dive.** Author: Claude (Opus 4.8) for Hooman Shariati. **Not financial advice.**
Run date: 2026-07-02. Verdict at bottom.

> **Anti-hallucination.** Every number carries a source + as-of date and a confidence mark
> (VERIFIED / ASSUMED / UNVERIFIED). Not a US SEC filer — **no EDGAR**; ground truth is
> Intesa's own Investor Relations documents (management-produced primary source) plus the ECB,
> rating agencies, and financial press. Two data vintages: **yfinance snapshot 2026-07-02**
> (prices/multiples, real fetch, VERIFIED-but-single-source) and **Intesa IR / press 2026-02-02
> FY2025 release + 2026-02-02 "2026-2029 Business Plan" + 2026-05-08 1Q26** (company results).
> Web research done 2026-07-02; article *bodies* of some paywalled outlets (Reuters/FT/Bloomberg)
> were not readable — those claims are marked accordingly.

---

## 0. Snapshot (as-of 2026-07-02, yfinance — VERIFIED real fetch, single-source)

| Metric | ISP.MI | Source |
|---|--:|---|
| Price | €6.14 | yfinance 2026-07-02 |
| Market cap | €107bn | yfinance 2026-07-02 |
| P/B | **1.56** | yfinance 2026-07-02 |
| P/E (trailing) | **11.4** | yfinance 2026-07-02 |
| P/E (forward) | 9.7 | yfinance 2026-07-02 |
| Dividend yield | **6.34%** | yfinance 2026-07-02 |
| Payout ratio | 66% | yfinance 2026-07-02 |
| ROE | **14.0%** | yfinance 2026-07-02 |
| Book value / sh | €3.95 | yfinance 2026-07-02 |
| Trailing EPS | €0.54 | yfinance 2026-07-02 |

> Note: yfinance ROE (14.0%) is a trailing-average figure; Intesa's **reported FY2025 ROE was
> ~18% / ROTE ~22%** (IR, see §3). The gap is definitional (yfinance uses a different equity base).
> Screen trap-gate: **PASS**. yfinance P/E 11.4 vs the screen's 11.1 snapshot — consistent.

---

## 1. Business & Thesis

**What it is.** Intesa Sanpaolo is **Italy's largest bank** by market cap (€107bn, yfinance
2026-07-02) — a domestically-dominant retail/commercial bank that has deliberately reshaped
itself into a **"Wealth Management & Protection" company**: a large fee engine (asset management,
private banking, insurance) bolted onto the deposit-and-lending core. This matters for the whole
thesis.

**The fee engine is real, and it is the differentiator.** FY2025 operating income €27,270m split
as (Intesa FY2025 press release, 2026-02-02 — VERIFIED):
- Net interest income (NII): **€14,796m** (~54% of revenue), down −5.9% YoY as the ECB cut rates.
- Net fees & commissions: **€9,980m** (+6% YoY).
- Insurance income: **€1,815m** (+5% YoY).
- **Fees + insurance ≈ 43% of operating income** (management's benchmarked metric: 41%→43%→42%
  across FY24/FY25/1Q26) **vs a large-European-peer average of ~27%** (Intesa IR, VERIFIED per
  company; peer-avg is management's own figure — ASSUMED). This is the crux: Intesa is
  **~2x more fee-weighted than the average big European bank.**

**Value thesis type — mixed, primarily cheap-structural + cheap-cyclical:**
- **Cheap-structural:** the "Italian bank discount" — Italian macro/political risk and
  sovereign/BTP doom-loop fear have historically capped Italian bank multiples below French/UK/
  Spanish peers regardless of profitability.
- **Cheap-cyclical (rate-driven):** ~54% of revenue is NII, so a chunk of the record 2023-25
  earnings rode the ECB hiking cycle; the market discounts a mean-reversion as rates fell.
- **Cheap-quality overlay:** the fee/insurance franchise, best-in-class 42% cost/income, and
  ~18% ROE mean this is a genuinely *high-quality* bank on a *relative* sale — not a distressed
  cheapie. It sits closer to "quality-at-a-price" than deep value, which fits the project's
  quality-first mandate.

---

## 2. Valuation — is the "Italian bank discount" warranted?

**Own history.** The stock has ~5x'd off its 2021 lows (5y range €1.17–€6.23, yfinance
2026-07-02); it is **no longer a deep-value optically**. At P/B 1.56 it trades **above book** —
richer than the depressed sub-1.0x P/B Italian banks carried through the 2010s sovereign crises.
The re-rating has largely happened.

**Vs peers (P/B and P/E, ~2026-07-02; ISP + immediate peers yfinance VERIFIED, others
cross-checked press UNVERIFIED-single-source):**

| Bank | P/B | P/E (ttm) | ROE | Div yield | Read |
|---|--:|--:|--:|--:|---|
| BNP Paribas | 0.87 | 9.7 | 9.6% | 9.8% | Cheapest (below book) but lowest ROE — French universal bank |
| **Intesa (ISP.MI)** | **1.56** | **11.4** | **14.0%** (rep. ~18%) | **6.34%** | Mid-pack P/B, top-tier ROE/efficiency |
| UniCredit (UCG.MI) | 1.80 | 11.3 | 17.0% | 4.0% | Higher ROE, richer P/B, lower yield |
| Santander (SAN.MC) | 1.70 | 14.1 | 12.9% | 2.1% | Richer, EM-exposed, lower yield |
| BBVA (BBVA.MC) | 2.36 | 12.4 | 19.0% | 4.2% | Richest P/B; highest ROE (Mexico/Turkey) |

*(ISP/UCG/BNP/SAN/BBVA all yfinance 2026-07-02, VERIFIED. STOXX Europe 600 Banks index P/B & P/E:
**could not verify a citable figure** — UNVERIFIED, do not quote a number.)*

**Read on the discount:** Against ROE, Intesa is **not** the cheapest — BNP (0.87x P/B) is far
cheaper on book but earns a ~9.6% ROE; Intesa at 1.56x P/B earns ~14-18% ROE. On a **P/B-to-ROE**
basis Intesa is reasonably-to-fully valued, not screamingly cheap. The residual "Italian discount"
today is **modest and narrowing**: Italian-bank aggregate P/E rose from ~9x (Jul 2025) to ~11.7x
(Jul 2026), roughly +30%, part of a broad European bank re-rating (Simply Wall St aggregates,
UNVERIFIED-single-source). Given Italy's sovereign upgrades (§4) the historic discount looks
**decreasingly warranted** — but that also means **most of the easy re-rating upside is behind us.**

**Total shareholder yield — the key attraction (quantified).** This is where Intesa stands out.
FY2025 total capital return ≈ **€8.8bn** = €6.5bn dividend (DPS €0.376) + €2.3bn buyback
(ECB-approved, launched Jul 2026) (Intesa IR, 2026-02-02, VERIFIED):
- Dividend yield ≈ **6.1%** + buyback yield ≈ **2.1%** = **total shareholder yield ≈ 8.2%** on
  the €107bn cap (my calc from sourced components — the *components* VERIFIED, the *sum* ASSUMED).
- Dividend growth is steep: DPS rose from ~€0.07 (2021) to €0.376 (2025) (yfinance dividend
  history, VERIFIED).
- The new **2026-2029 plan** promises **~€50bn total capital return over 2025-2029 at a 95%
  payout (75% cash + 20% buyback)** (Intesa 2026-2029 Business Plan deck, 2026-02-02, VERIFIED) —
  roughly **half the current €107bn market cap returned over four years** if delivered.

**P/tangible-book:** Intesa does not headline a clean P/TBV; implied tangible equity from
net income / ROTE (€9.32bn / 22% ≈ €42bn) gives **P/TBV ≈ 2.5x** (my derivation, ASSUMED —
treat as rough; the €42bn is a back-out, not a reported tangible-equity line). This is high for a
bank and reflects the fee-franchise premium the market now assigns.

---

## 3. Quality — genuinely high

| Metric | Value | As-of / source | Confidence |
|---|--:|---|---|
| Net income FY2025 | **€9,321m** (+7.6%) | Intesa FY25 release 2026-02-02 | VERIFIED (IR) |
| Net income FY2024 | €8,666m | Intesa FY24 deck 2025-02-04 | VERIFIED (IR) |
| ROE FY2025 (reported) | **~18%** | Intesa FY25 deck 2026-02-02 | VERIFIED (IR) |
| ROTE FY2025 (reported) | **~22%** | Intesa FY25 deck 2026-02-02 | VERIFIED (IR); minor def. wrinkle (25% on 1Q26 basis) |
| Cost/income FY2025 | **42.2%** ("lowest ever") | Intesa FY25 release 2026-02-02 | VERIFIED (IR) |
| CET1 fully-loaded (pre-buyback) | **13.9%** (31 Dec 2025) | Intesa FY25 release 2026-02-02 | VERIFIED (IR) |
| CET1 (post dividend+buyback) | 13.2% | Intesa FY25 release 2026-02-02 | VERIFIED (IR) |
| Gross NPL ratio | **1.8%** (net 0.9%), Dec 2025 | Intesa FY25 release 2026-02-02 | VERIFIED (IR) |
| NPL coverage | 48.6% | Intesa FY25 release 2026-02-02 | VERIFIED (IR) |
| 2026-2029 targets | Net income >€11.5bn; ROTE 27%; C/I 36.8% by 2029 | Intesa plan deck 2026-02-02 | VERIFIED (IR) |

**Capital — well-capitalized: VERIFIED YES.** CET1 fully-loaded **13.9%** (pre-buyback,
Dec 2025), comfortably above the plan's >12.5% floor and the >13% "well-capitalized" bar. The
buyback is funded from a genuine capital surplus.

**Asset quality — dramatically de-risked.** Gross NPL **1.8% / net 0.9%** — Intesa now brands
itself a "Zero-NPL Bank." The long-run improvement is real: net NPL ratio fell from **4.8%
(end-2017) → 0.8% (end-2025)** (Intesa IR, VERIFIED). *Caveat:* the specific **2015 peak (~€88bn
gross NPLs) could NOT be verified** in current Intesa docs — they benchmark to 2017, not 2015; use
the 2017→2025 trajectory as the verifiable proxy (UNVERIFIED on the 2015 baseline).

**Fee/wealth-management income stability.** Fees +6% and insurance +5% in FY2025 (VERIFIED, IR) —
they *grew* while NII fell, which is exactly the resilience the wealth-management franchise is
supposed to deliver. ~€1.7tn of customer financial assets underpins the fee base.

**NIM / rate trend.** yfinance lacks NIM. From results: FY2025 NII −5.9% as ECB cut ~200bps, but
1Q26 NII was **flat YoY** despite falling Euribor, cushioned by ~€160-170bn of structural
deposit hedges (~4yr duration). Management guides **NII "growth expected in 2026"** (qualitative;
no numeric guidance found — UNVERIFIED on the exact figure).

**Verdict: high-quality bank** — 42% cost/income and ~18% ROE / ~22% ROTE are among the best in
Europe, capital is strong, and asset quality is excellent.

---

## 4. Bear Case / Risks

**Risk 1 — Rate-cut / NII sensitivity (the dominant earnings driver). Argue both sides.**
- *Bear:* ~54% of revenue is NII (VERIFIED). Record 2023-25 earnings partly rode the ECB hiking
  cycle. Morningstar explicitly flags that recent profitability improvement was "almost exclusively
  due to higher interest rates," a sustainability risk as rates ease (press, UNVERIFIED body). If
  the ECB stays low/cuts further, the biggest single revenue block compresses.
- *Bull:* the fee/insurance ~43% revenue mix (2x peers) is the structural cushion, and it *worked*
  — FY2025 operating income *rose* (+€163m) even as NII fell −5.9%, because fees/insurance offset
  it; 1Q26 NII was flat YoY. Deposit hedges (~4yr, ~1.7-1.8% yield) smooth the descent. **This is
  the single best argument for owning Intesa over a pure-NII bank** — it is demonstrably *less*
  rate-cyclical than peers, though not immune.
- *Rate path (VERIFIED, ECB):* deposit rate peaked 4.00% (Sep 2023) → cut to a **2.00% trough
  (Jun 2025)** → **+25bp back to 2.25% (effective 17 Jun 2026)**, the first hike since 2023
  (energy-led inflation ~3%). So rates are **off the bottom and rising slightly** — a *tailwind*
  vs the feared endless-cut scenario. (Per-decision ECB pages not individually opened; levels
  cross-checked across ECB rate page + Trading Economics.)

**Risk 2 — Italian sovereign / BTP doom-loop. Argue both sides.**
- *Bear:* Intesa holds **~€32bn Italian government debt (banking book, Dec 2025; ~€35bn Mar 2026)**
  plus ~€9bn government loans; including insurance, total Italian govt securities ≈ **€75bn**
  (Intesa IR, VERIFIED; Intesa doesn't label a "BTP" line — these are its Italian
  central+local-government sovereign rows, the closest measure). A blow-up in Italian public
  finances hits the bond book and funding costs simultaneously — the classic doom-loop.
- *Bull:* the sovereign risk premium is **shrinking, not widening.** **Italy was UPGRADED in
  2025-26:** Moody's Baa3→**Baa2** (21 Nov 2025, first upgrade in years); S&P **BBB+** outlook
  moved to **Positive** (30 Jan 2026); DBRS **A(low)** (Oct 2025) (VERIFIED via rating trackers;
  **no Fitch/Scope 2025-26 action confirmed** — UNVERIFIED there). BTP-Bund 10Y spread ~**75bps**
  (2026-07-02) vs several-hundred-bps in past crises (level VERIFIED; "tightest-ever" narrative
  UNVERIFIED). Sovereign duration ~0.5y after hedging. **The doom-loop fear is at a cyclical low.**

**Risk 3 — Italian macro / political.** Italy has chronic low growth, high public debt, and
frequent political turnover. Structural, not going away — but currently benign (upgrades, tight
spreads).

**Risk 4 — Payout sustainability if earnings fall.** The ~8% total shareholder yield and 95%
plan-payout leave little margin if earnings drop. *Bull counter:* CET1 13.9% is a genuine surplus,
the cash-dividend leg is ~66-75% payout (buybacks are the flexible top-up that can be cut first),
and the fee franchise defends earnings. The 95% payout is **CET1-conditional (>12.5% floor)** —
i.e. designed to flex down, not a fixed promise. Sustainable at current earnings; the buyback
portion is the shock absorber.

**Risk 5 — Most of the re-rating has happened.** From €1.17 to €6.14 and from sub-1x to 1.56x
P/B, the cheap-structural discount has largely closed. Forward return now leans on **capital
return (~8% yield) + modest earnings growth**, not multiple expansion. This is a *yield/quality*
hold, not a deep-value double.

---

## 5. Catalysts & Verdict

**Catalysts:**
- Delivery on the **2026-2029 plan** (>€11.5bn net income, ~€50bn capital return, ROTE 27%) —
  each beat/on-track print supports the multiple. (VERIFIED plan targets, execution ASSUMED.)
- Further **Italy sovereign upgrades** (S&P Positive outlook → potential upgrade) tightening the
  country risk premium and narrowing the Italian-bank discount further.
- **Continued fee/wealth-management growth** proving out the "less rate-sensitive" thesis as NII
  stabilizes.
- Buyback execution (€2.3bn 2025 tranche launched Jul 2026) supporting the share count/EPS.

**Scorecard (project weights: Cheapness 30 / Quality 30 / Trap 20 / Moat 15 / Catalyst 5):**

| Dimension | Score /10 | Weight | Contribution | Rationale |
|---|--:|--:|--:|---|
| **Cheapness** | 6.0 | 30% | 1.80 | P/E ~11, ~8% total shareholder yield are attractive; but P/B 1.56 (above book) and ~2.5x P/TBV mean the deep discount is gone. Cheaper on yield than on assets. |
| **Quality** | 8.5 | 30% | 2.55 | ~18% ROE / 22% ROTE, 42% cost/income, 13.9% CET1, 1.8% NPL, resilient fee franchise — top-tier European bank. |
| **Trap-risk (inverse)** | 6.5 | 20% | 1.30 | Trap-gate PASS, payout covered, capital strong. Docked for NII rate-cyclicality (54% of rev) + €75bn Italian sovereign concentration. |
| **Moat & leadership** | 7.0 | 15% | 1.05 | Dominant Italian franchise + scaled wealth-mgmt/insurance fee engine (43% of rev, 2x peers) = a real, if geographically concentrated, moat. |
| **Catalyst** | 6.5 | 5% | 0.325 | New 4-yr plan, sovereign upgrades, huge capital-return runway — but much re-rating already realized. |
| **TOTAL** | | | **~7.0 / 10** | |

**VERDICT: WATCH (leaning BUY-worth-more-work for an income/quality sleeve).**

Intesa is a **genuinely high-quality bank on a modest, and narrowing, discount** — not a deep-value
bargain. The standout attraction is the **~8% total shareholder yield** (6.1% dividend + 2.1%
buyback) backed by a fortress 13.9% CET1 and a fee/insurance franchise that makes it demonstrably
**less rate-sensitive than pure-NII peers**. The bull case is quality + yield + Italy's improving
sovereign story; the bear case is that ~54% of revenue is still NII (rate-cyclical) and the
€1.17→€6.14 re-rating has already closed most of the "Italian discount." I would rank it **below
the deep-value BOTH/B-only industrial and energy finalists on cheapness, but as the best
dev-ex-US bank in the finalist set** and a legitimate quality-at-a-price income holding.

---

## Return summary (for parent)

**Verdict: WATCH, leaning BUY-worth-more-work for a quality/income sleeve — scorecard ~7.0/10**
(Cheapness 6.0, Quality 8.5, Trap 6.5, Moat 7.0, Catalyst 6.5). **Is the Italian-bank discount
warranted? Largely NO longer** — Italy was upgraded in 2025-26 (Moody's→Baa2 Nov-2025, S&P
BBB+/Positive Jan-2026), the BTP-Bund spread is ~75bps, and Intesa's ~18% ROE / 22% ROTE, 42%
cost/income, 13.9% CET1 and 1.8% NPL are top-tier — so the discount is modest and narrowing, but
that also means most of the easy re-rating (from €1.17 to €6.14, sub-1x to 1.56x P/B) is behind
us; it's now a yield/quality hold, not a deep-value double. **The single most attractive feature
is the ~8% total shareholder yield** (6.1% dividend + 2.1% buyback FY2025, VERIFIED components),
with a 2026-2029 plan promising ~€50bn of capital return (roughly half the market cap) at a
CET1-conditional 95% payout. **Top risk = rate-cut/NII sensitivity** (54% of revenue is NII), only
partly offset by the fee/insurance franchise (43% of revenue, ~2x peers) that let operating income
*rise* in FY2025 even as NII fell −5.9%; the ECB has actually turned (2.00% trough Jun-2025 →
+25bp to 2.25% Jun-2026), which is a tailwind, not the feared endless cut. Secondary risk is the
~€75bn Italian sovereign concentration (doom-loop), currently at a cyclical-low fear level.
Confidence: core financials VERIFIED from Intesa IR (no EDGAR — not a US filer); ranking/scorecard
ASSUMED; a few items (2015 NPL peak, STOXX banks index multiples, Fitch/Scope actions, exact NII
guidance) UNVERIFIED and flagged in the doc.
