# NEM — Newmont Corporation — Stage 4 Deep Dive

**Ticker:** NEM (NYSE) · **Sector:** Materials / Gold mining · **Region:** US (Denver, CO) · **Bucket:** B-only (cheap-quality in a non-1a-cheap sector)
**Run:** 2026-07-02 by Claude (Opus 4.8). **Owner:** Hooman Shariati. **NOT financial advice.**

> **Anti-hallucination.** Every number carries a source + as-of date. Financials cross-checked against
> SEC EDGAR (CIK 0001164727) XBRL company-facts and the FY2025 (filed 2026-02-19) and Q1-2026
> (filed 2026-04-23) filings. Peer/market context from web sources (cited inline). Confidence marks:
> **VERIFIED** (primary filing / direct fetch) / **ASSUMED** (my judgment) / **UNVERIFIED** (single/secondary source).

---

## Screen snapshot being tested (yfinance, 2026-07-02)
EV/EBITDA ~5.9 · earnings yield 15.9% · ROE 25.8% · Piotroski 7/7 · P/B 2.87 · P/E ~12.1 · combined score **87.1** (#2 of the whole global run). Brief instruction: **rank quality on ROE, not the inflated ROIC-proxy.**

**Verification of the screen (EDGAR ground truth):**
- **Market cap ~$105B** at ~$96.5/share × 1.088B shares out (dei EntityCommonStockSharesOutstanding 1,087,874,212 as-of 2026-02-12; price ~$96.5 from stockanalysis.com/marketbeat 2026-07-02). Screen's "$100B" ✓ close. **VERIFIED.**
- **P/E ~12.1** — matches TTM. On **FY2025 GAAP EPS $6.51** (NI $7.085B ÷ 1.088B sh), trailing P/E = **14.8**; on adjusted EPS $6.89, **14.0**. On *annualized Q1-2026* earnings, forward P/E collapses to **~8** — this gap IS the thesis (see §2). **VERIFIED.**
- **P/B ~2.9–3.1** — FY2025 book equity **$33.867B** (EDGAR) → P/B **3.10** at $105B cap. Screen 2.87 was on a slightly lower price. **VERIFIED.**
- **ROE 25.8%** (screen, TTM). On FY2025 GAAP NI $7.085B ÷ avg equity ($33.87B/$29.93B) = **22.2%**; ÷ end equity = 20.9%. TTM (incl. the very strong Q1-2026) supports ~26%. **VERIFIED — quality ranked on ROE per brief.**
- **FCF FY2025 = $7.30B** (CFO $10.334B − capex $3.035B, EDGAR) → **FCF yield ~7.0%.** Newmont's own "record $7.3B FCF." **VERIFIED.**

---

## 1. Business & Thesis

**What it is.** Newmont is the **world's largest gold producer** — ~5.9M attributable gold oz in FY2025 (VERIFIED, Q4-2025 release, 2026-02-19), targeting ~6M oz/yr long-term. It became #1 via the **all-stock acquisition of Newcrest Mining, closed 2023-11-06** (0.400 exchange ratio; legacy Newcrest holders ended ~31% of the combined company → **~31% dilution**; share count jumped ~794M (2023-02-16) → ~1,153M (2024-02-15), EDGAR dei). Post-deal the portfolio spans Nevada (JV with Barrick), Australia (Boddington, Tanami, Cadia), PNG (Lihir; Wafi-Golpu JV), Canada (Brucejack, Red Chris), Latin America (Peru, Argentina, Mexico, Suriname, Dom. Rep.), and Ghana (Ahafo). Newmont calls **~94% of reserves "Tier-1"** (125.5M of 134.1M oz, operations.newmont.com, end-2024; the exact by-country split is **UNVERIFIED** behind a CDN block).

**Value thesis (bull).** A statistically cheap #1 franchise printing record cash: FY2025 revenue **$22.67B** (from $18.68B FY2024), GAAP NI **$7.085B** (2.1× FY2024's $3.348B), adj. EBITDA **$13.5B**, FCF **$7.3B**, now **net-cash ($8.78B cash vs $5.08B LT debt = ~$3.7B net cash, Q1-2026, EDGAR)** after de-levering from ~$8.55B LT debt at the post-Newcrest peak (Q3-2024). ~7/7 Piotroski, 15.9% earnings yield, EV/EBITDA ~5.9 — cheaper than premium peer Agnico and roughly in line with Barrick/Kinross. Consensus is **Buy/Moderate Buy, median target ~$139 (~44% upside)** (stockanalysis.com/marketbeat, 2026-06-30).

**The central question — is the cheapness real or a peak-earnings mirage?** This is the whole game for a commodity producer and is addressed head-on in §2. Short version (ASSUMED, argued both sides): the **low trailing/forward P/E is substantially a function of a high — and recently record — gold price**, not a durable re-rating. Realized gold went **$3,498/oz (FY2025) → $4,900/oz (Q1-2026)**, spot hit an all-time **~$5,608 in Jan-2026** and has since fallen to **~$4,136 (2026-07-02, up 24% YoY)** (tradingeconomics/Kitco). Earnings are near a cyclical high. But there is a genuine value component too: Newmont books reserves at **$2,000/oz** — less than half of spot — so if gold merely *holds* above ~$3,000, the cash-flow stream is far higher than the last decade's and the balance sheet is now fortress-grade. The name is **"cheap on peak-ish gold, with real de-risking underneath"** — not a clean bargain, not a pure trap.

---

## 2. Valuation — and the PEAK-CYCLE question (the key trap risk)

### Multiples vs peers (as-of 2026-07-02, stockanalysis.com)
| Company | Ticker | EV/EBITDA | P/E (TTM) | Fwd P/E | FY25 AISC (by-product) | Reserve price |
|---|---|--:|--:|--:|--:|--:|
| **Newmont** | NEM | **5.9** | 12.1 | ~9.2 | **$1,358/oz** | **$2,000/oz** |
| Barrick | B | 5.8 | 10.5 | 8.8 | $1,637/oz | $1,500/oz |
| Agnico Eagle | AEM | **7.8** | 14.3 | 10.7 | **$1,313/oz** (lowest) | $1,600/oz |
| Kinross | KGC | 5.4 | 10.4 | 7.1 | $1,571/oz | n/v |

Source: stockanalysis.com statistics pages + company 40-F/8-K filings (FY2025), 2026-07-02. **P/NAV** (directional, VERIFIED only for two points): **Newmont ~1.08×** (Stifel, investing.com 2025-07-08) vs **Agnico ~1.1×** (premium; Jefferies) vs senior-peer avg ~0.8×; Barrick ~0.95× / Kinross ~1.23× are **UNVERIFIED** snippets.

**Read:** Newmont is **cheaper than Agnico** (the quality/jurisdiction premium name) on EV/EBITDA, P/E and P/NAV, and **roughly in line with Barrick/Kinross**. Its ~1.08× P/NAV vs Agnico's premium reflects (a) the 2024 execution overhang, (b) higher mixed-jurisdiction exposure, and (c) **by-product AISC flattering the cost comparison** — Agnico ($1,313 co-product basis) is the genuine low-cost operator; Newmont's $1,358 nets out copper/silver/zinc credits. Newmont is *statistically* cheap but the discount to Agnico is the market pricing execution/jurisdiction, not free value.

### Own-history context
EV/EBITDA ~5.9× is **below** where senior gold majors trade in the middle of a cycle (typically ~7–9×); the compression is the market saying "these EBITDA dollars are peak dollars." Newmont's own multiple has ranged widely; a mid-single-digit EV/EBITDA on record EBITDA is the classic cyclical signature.

### THE PEAK-CYCLE CALL (explicit, per brief)
**A low P/E on peak gold is the definitional value trap for a miner.** The evidence that earnings are at/near a cyclical peak (VERIFIED figures):
- **Realized gold price trajectory:** $3,498/oz (FY2025 avg) → **$4,900/oz (Q1-2026 avg realized)** — a ~40% jump YoY that is almost entirely price, not volume (Q1-2026 output ~1.3M oz, *down* ~16% YoY partly on divestitures).
- **Margin explosion:** Q1-2026 by-product AISC $1,029/oz vs realized $4,900/oz = **~$3,870/oz cash margin.** Q1-2026 GAAP NI **$3.262B** in a single quarter (EDGAR) — annualized ~$13B, putting **forward P/E at ~8** on run-rate earnings.
- **Spot is *below* Q1's realized price and ~26% off the Jan-2026 peak** ($4,136 vs $5,608; tradingeconomics 2026-07-02). Q2-2026 was reportedly gold's worst quarter in ~13 years. So Q1's $4,900 realization is *itself* above current spot — the peak-earnings quarter may already be behind.

**But the trap is partial, not total** (the bull rebuttal):
- **Reserve price $2,000/oz** (raised from ~$1,400; VERIFIED, FY2025 10-K SK-1300 Boddington report). Spot is >2× the price at which the 118.2M-oz reserve base is booked. Even at $3,000 gold — a ~27% *fall* from here — margins stay historically fat.
- **The balance sheet has been permanently de-risked with cycle cash:** net-cash, $6B buyback authorization (fully spent once, re-loaded 2026-04), integration complete, ~20-yr reserve life (118.2M oz P&P ÷ 5.9M oz/yr). This is durable value that survives a gold pullback.
- Miners at cyclical peaks *should* show low P/Es; the question is whether gold's regime (central-bank buying ~244t Q1-2026, de-dollarization, geopolitics) has structurally shifted the floor higher. Bank 2026 targets span **~$4,300–$6,300** (JPMorgan $6,000; Goldman $4,900; TD sees a dip <$3,900 first) — dispersion = genuine uncertainty, not consensus peak.

**Verdict on the trap question (ASSUMED):** **~60% cyclical, ~40% real value.** Do NOT capitalize the ~$13B annualized Q1 earnings — that is a spike quarter on record gold. Value it on a **normalized gold deck ($3,000–3,500/oz)**, where NI is closer to FY2025's $7B and the P/E is ~14–15× (fair, not cheap). The *durable* value is the net-cash balance sheet, 20-yr Tier-1 reserve life, and huge optionality if the high-gold regime persists. Treat NEM as a **quality gold OPTION on a de-risked balance sheet**, not a mispriced compounder.

---

## 3. Quality

- **ROE (rank quality here per brief):** TTM **~26%** (screen); FY2025 GAAP **22.2%** on avg equity (20.9% on end equity) — inflated by the gold spike but genuinely strong. Multi-year ROE was far lower/negative in weak-gold years (macrotrends fetch failed, HTTP 402 — **UNVERIFIED long series**; but FY2024 NI $3.348B on ~$30B equity ≈ 11% shows the swing). **ROE is cycle-levered — do not extrapolate 26%.**
- **Margins vs gold price:** net margin FY2025 ~31% ($7.085B/$22.67B) vs a thin single-digit/negative in trough years — confirms earnings are a leveraged play on the gold price, not a stable spread. **VERIFIED.**
- **FCF:** record **$7.3B FY2025** (7% yield); **$3.1B "record" Q1-2026** (EDGAR CFO $3.785B − capex). Excellent — but again price-driven. **VERIFIED.**
- **Balance sheet post-Newcrest:** de-levered from ~$8.55B LT debt (Q3-2024) to **$5.08B**, cash **$8.78B → net cash ~$3.7B** (Q1-2026, EDGAR). Fortress. **VERIFIED — the standout durable-quality item.**
- **Capital return:** FY2025 returned **$3.4B** (dividends + buybacks); dividend rebased to a **"sustainable $1.1B/yr"** ($0.26/qtr, $1.04 annualized — *cut* from the pre-2024 level; div paid $1.42B FY2023 → $1.11B FY2025, EDGAR). **$6B buyback fully executed, then re-authorized $6B (2026-04).** Per-share growth is intended to come via buybacks, not dividend hikes. **VERIFIED.**
- **Cost discipline / execution — the blemish (VERIFIED):** **2024 was genuinely poor** — UBS downgraded to Neutral citing production ~9% below and costs ~16% above guidance; FY2024 AISC overran to ~$1,516/oz; $1,114M loss on assets held for sale + $78M impairments; Q3-2024 stock −5.6% on an EPS miss. **2025–2026 was a clean turnaround** — met 5.9M-oz guidance, AISC $1,358, every quarter beat, integration costs to $0, divestiture program raised **~$4.3B gross** (vs a ~$2B target; completed 2025-09). Synergy target ($500M/yr) scored at max/200% and was retired. **Execution track record = one bad year (2024) followed by strong delivery — improving but not yet Agnico-grade.**
- **Newcrest synergies:** hit/exceeded $500M target per proxy incentive metric (200% payout FY2024); a single audited realized-$ figure not separately disclosed (**UNVERIFIED** exact total).

**Quality read:** high-quality *for a gold miner* (net-cash, scale, Tier-1 reserves, 7/7 Piotroski), but ROE/margins/FCF are all cycle-inflated, execution has a 2024 scar, and the dividend was cut. Rank as good, not elite.

---

## 4. Bear Case / Risks

1. **Gold-price sensitivity (dominant risk).** Earnings, FCF, ROE and the whole thesis are levered to gold. Spot is already ~26% below the Jan-2026 peak and *below* Q1's $4,900 realization. A regime reversion toward $3,000 (−27%) roughly halves incremental margin; a slide to the $2,000s (still above reserve price) would compress the P/E dramatically and expose the low-multiple-on-peak-earnings trap. **This is the single risk that matters most.**
2. **Peak-cycle / earnings mean-reversion.** As above — the ~8× forward P/E is on spike earnings. Normalize and it's ~14–15×.
3. **Cost inflation.** 2026 AISC guidance **$1,680/oz** — *up* from $1,358 actual FY2025 (labor, energy, lower grades, divestiture mix). If gold falls while costs stay sticky, margins compress from both sides. The 2024 cost overrun shows this is a live risk.
4. **Jurisdiction / geopolitical risk.** Despite the "94% Tier-1" label, real exposure includes Peru (Yanacocha — Cajamarca conflict; Sulfides deferred, drove a 2025 impairment), Mexico (Peñasquito — 2023 strike + 2023 mining-law reform / resource nationalism), Argentina (Cerro Negro — 2024 fatalities & suspension), PNG (Lihir + Wafi-Golpu — permitting/state-equity risk), Ghana, Suriname. Higher-risk than Agnico's Canada/Finland/Australia base — a core reason for the P/NAV discount.
5. **Capital allocation / dilution history.** Newcrest was an **all-stock deal that diluted ~31%** at a full price; the dividend was subsequently **cut**. Buybacks are now unwinding some dilution (~1,153M → 1,088M shares), but the M&A-then-dilute-then-buyback pattern is a caution. Buying back stock at peak-gold valuations also risks poor timing.
6. **Reserve depletion / reinvestment.** ~20-yr life is fine, but major growth projects (Cadia, Tanami, Ahafo North, Wafi-Golpu) require capex and carry execution risk given the 2024 record.

---

## 5. Catalysts & Verdict

**Catalysts (near-term):** (a) continued record FCF → accelerated buybacks (fresh $6B authorization) if gold holds; (b) sustained execution beats rebuilding the Agnico-vs-Newmont valuation gap; (c) a durable high-gold regime (central-bank buying, Fed cuts) re-rating the whole group; (d) further balance-sheet optionality (net cash). **Counter-catalyst:** any gold pullback or a single production/cost miss re-opens the 2024 narrative fast.

### Scorecard (0–10; weights per CLAUDE.md §3)
| Dimension | Weight | Score | Rationale |
|---|--:|:--:|---|
| **Cheapness** | 30% | **6.0** | Statistically cheap (EV/EBITDA 5.9, EY 15.9%, FCFy 7%, cheaper than Agnico) — but heavily discounted because it's **cheap on peak-ish gold**; normalized P/E ~14–15× is only fair. Half the cheapness is a mirage. |
| **Quality** | 30% | **6.5** | Strong *for a miner*: net-cash, 7/7 Piotroski, record FCF, ~26% ROE (cycle-inflated), 20-yr Tier-1 reserves. Docked for cycle-levered margins, the 2024 execution scar, dividend cut. Rank on ROE per brief. |
| **Trap-risk (inverse)** | 20% | **4.5** | The commodity-peak trap is real and partly present — spot already off ~26% from peak, earnings near cyclical high, 2026 AISC rising. Partly mitigated by net-cash B/S + $2,000 reserve price. Below-average safety. |
| **Moat & leadership** | 15% | **5.5** | No true moat (price-taker on a fungible commodity); "moat" is scale, Tier-1 asset quality and low-cost position. Leadership improving post-2024 but not proven elite; some jurisdiction exposure. |
| **Catalyst** | 5% | **6.0** | Buybacks + execution-gap-closing + gold regime; symmetric with downside. |

**Weighted total = 6.0×0.30 + 6.5×0.30 + 4.5×0.20 + 5.5×0.15 + 6.0×0.05**
= 1.80 + 1.95 + 0.90 + 0.825 + 0.30 = **5.78 / 10.**

### VERDICT: **WATCH** (lean positive, but not a clean value buy at peak-ish gold)

Newmont is a genuinely improved, net-cash #1 gold franchise that screens cheap — but the cheapness is **substantially a peak-gold artifact** (forward P/E ~8 on annualized record-quarter earnings; realized gold $4,900 in Q1-2026 vs a reserve price of $2,000 and spot already ~26% below the Jan-2026 peak). On a normalized $3,000–3,500 gold deck it is only *fairly* valued (~14–15× P/E). The durable value — fortress net-cash balance sheet, ~20-yr Tier-1 reserves, restored execution — is real and provides downside protection, so this is best framed as a **high-quality gold OPTION**, not a mispriced compounder. **Prefer to size on a gold pullback** (buy the miner cheap when gold is soft, not after a 24% run), or **prefer Agnico for quality / Kinross for cheapness** within the same theme. Not enough conviction for BUY-worth-more-work given the cycle timing; not weak enough for PASS given the balance sheet and optionality.

---

## Confidence summary
- **VERIFIED (EDGAR primary):** FY2025 revenue/NI/equity/debt/cash/CFO/capex/shares; Q1-2026 NI/cash/FCF; FY2025 production/AISC/realized-price/reserves/guidance (company releases).
- **VERIFIED (direct fetch):** spot gold $4,136/oz + Jan-2026 peak (tradingeconomics 2026-07-02); Q1-2026 realized $4,900 & AISC $1,029 (EDGAR exhibit).
- **UNVERIFIED / single-source:** long-run ROE series (macrotrends 402); P/NAV magnitudes beyond two points; some bank gold-price targets (aggregated); exact reserve %-by-country; Kinross reserve price; CEO succession.
- **ASSUMED (my judgment):** the ~60% cyclical / ~40% real-value split; normalized-gold valuation; all scorecard scores; WATCH verdict.
