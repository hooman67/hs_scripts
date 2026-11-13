# NTES — NetEase, Inc. — Stage 4 Deep Dive

**Prepared:** 2026-07-02 by Claude (Opus 4.8) for Hooman Shariati. **Not financial advice.**
**Listing:** Nasdaq **NTES** (ADS, 1 ADS = 5 ordinary shares) and HKEX **9999.HK**. HQ Hangzhou, China.
**Screen bucket:** B-only (best-quality cheap Chinese internet name; Comm-Svcs / Gaming). Screen score 82.8, Piotroski 7/7.

> **Anti-hallucination.** Every figure carries a source + as-of date and a confidence mark
> (VERIFIED / ASSUMED / UNVERIFIED). Financials are reported in **RMB** with a USD convenience
> translation; I use USD/CNY **6.7721** (yfinance `CNY=X`, 2026-07-02) where I convert.
> **NB the screen's own EV/EBITDA 6.4 and P/B 17.1 are DATA ARTIFACTS — corrected below (§2).**

---

## 0. TL;DR verdict

**WATCH, leaning BUY-worth-more-work.** Weighted scorecard **6.9 / 10** (§5). NetEase is a
genuinely high-quality, cash-gushing, founder-aligned games compounder trading at a **China
discount** (~16.5x trailing / ~12x forward P/E; ~11.5x P/E ex-net-cash) — cheaper than its own
history and roughly in line with lower-quality Western games peers despite far better margins and
returns. But it is **not** the "6.4x EV/EBITDA / 41% FCF-yield" bargain the raw screen implied
(both were currency-mix artifacts). The real EV/EBITDA is ~10.5x and FCF yield ~8-9%. The cheapness
is **mostly a China-risk discount, partly genuine value.** Top risks are structural and
non-diversifiable: (1) the **VIE structure** — US/HK investors own a Cayman shell with *contracts*
to (not equity in) the Chinese OpCos that generate ~85% of revenue; (2) China games regulation
(overhang has *cleared* but can re-appear overnight, as Dec-2023 showed). Both are "known, priced,
but binary" risks.

---

## 1. Business & thesis

**What it is.** NetEase is China's **#2 games company** (behind Tencent) plus two smaller listed/
consolidated arms:

| Segment | FY2025 revenue | % of total | Notes |
|---|---|---|---|
| **Games & related value-added services** | ¥92.1bn (~US$13.2bn) | **~82%** | The engine. ~97.3% of segment rev is online games (20-F, VERIFIED). |
| **Youdao** (education/dictionary) | ~¥5.6bn est. | ~5% | Separately Nasdaq-listed (DAO); EdTech, small. |
| **Cloud Music** (streaming) | ~¥8bn est. | ~7% | Separately HK-listed (9899.HK); Spotify-of-China #2. |
| **Innovative businesses / other** | remainder | ~6% | Yanxuan e-commerce, misc. |

Sources: segment split cross-checked from NetEase IR FY2025 (games ¥92.1bn, total ¥112.6bn →
81.8%; subagent web research, VERIFIED against IR release) and FY2025 20-F (games = 97.3% of the
games-segment; games-segment ≈82% of company). Youdao/Cloud Music sub-splits ASSUMED from prior
disclosure proportions — treat as approximate.

**The games franchise.** NetEase's moat is a stable of **long-running, self-developed PC/mobile
franchises with 15-25 year lifespans** — the "evergreen" anchor:
- *Fantasy Westward Journey* / *Westward Journey Online* (since 2001-02) — the cash cow, still
  cited every quarter (VERIFIED, IR).
- *Identity V* (2018), *Onmyoji*, *Eggy Party*, *Naraka: Bladepoint* (2021), *Justice / Ni Shui Han*.
- **New global hits (2024-26):** *Marvel Rivals* (F2P hero shooter, launched Dec 6 2024 — 40M+
  players by Feb 2025; VERIFIED) and *Where Winds Meet* (open-world RPG, 80M cumulative players by
  Feb 2026; global console/PC rollout through mid-2026; VERIFIED). These drove the FY24→FY25 +10%
  games growth.
- **Blizzard partnership resumed:** the 14-yr NetEase-Blizzard China deal ended Nov 2022 (WoW/
  Hearthstone/Overwatch went dark Jan 2023); a **new agreement was reached ~April 2024** and Blizzard
  titles are back live in China with NetEase (VERIFIED, Wikipedia/IR). Removes a prior overhang.

**The value thesis.** A dominant, high-margin (69% gross, ~40% op), high-ROE (~21%) franchise
business with a **US$24bn+ net-cash fortress** (30% of market cap), paying a growing dividend +
buying back stock, run by a founder who owns ~45.5% *without* super-voting shares — trading at
~12x forward earnings. That is a Nintendo-quality asset at a value-stock multiple.

**Why is it cheap?** Three candidate explanations, in order of weight:
1. **China discount (primary).** All China ADRs carry a geopolitical/VIE/capital-controls discount
   regardless of fundamentals. This is the bulk of it.
2. **Games-regulation overhang (secondary, now largely cleared).** The 2021-22 approval freeze and
   the Dec-2023 draft-spending-cap scare left a scar; approvals have since normalized/expanded and
   the draft rules died (§4), so this is *fading* — arguably the re-rating catalyst.
3. **Genuine value (partial).** Ex-cash the multiple is ~11.5x P/E for a 20%-ROE compounder — that
   is cheap on its own merits, not just relative to China peers.

Net read: **~2/3 China-risk discount, ~1/3 genuine value.** The question for Hooman is whether the
China/VIE risk is worth the ~11.5x ex-cash price. Bulls say yes; the discount overpays you for a
risk that has been stable-to-improving. Bears say the risk is un-hedgeable and the shell you own
is not the company.

---

## 2. Valuation — and correcting the screen's artifacts

### 2.1 The screen's EV/EBITDA 6.4 and P/B 17.1 are BOTH data artifacts (investigated)

The screen (yfinance `info`, 2026-07-02) reported EV/EBITDA **6.4** and P/B **17.1**. Both are wrong,
caused by yfinance **mixing USD market cap with RMB balance-sheet items**:
- **P/B 17.1 (artifact).** yfinance divided the **USD ADS price ($128.27)** by a `bookValue` of
  **$7.58** that is actually **RMB book value per *ordinary* share** (equity ¥160.3bn ÷ ~3.19bn
  ordinary shares ≈ ¥50/ord-share ≈ ¥250/ADS; the $7.58 is ~¥50 mislabeled as USD). **Corrected
  P/B ≈ 3.5** (equity ¥160.3bn vs market cap ¥556bn; equivalently $128.27 ÷ ~$37 book/ADS = 3.47).
  (VERIFIED by reconstruction; balance sheet from yfinance `balance_sheet` 2026-07-02.)
- **EV/EBITDA 6.4 (artifact).** yfinance's `enterpriseValue` was **$259bn — larger than the $82bn
  market cap**, which is impossible for a net-cash company; it added RMB debt/subtracted a mis-scaled
  cash figure against a USD cap, then divided by RMB EBITDA. **6.4 = $259bn ÷ ¥40.2bn** — a
  nonsensical USD-over-RMB ratio. **Corrected, all-in-RMB: net-cash-adjusted EV/EBITDA ≈ 10.5x;
  unadjusted (mktcap/EBITDA) ≈ 14.6x.** (VERIFIED by reconstruction.)

**Lesson (add to LEARNINGS):** for ADRs of foreign filers that report in local currency, yfinance
`info` fields (`enterpriseValue`, `priceToBook`, `enterpriseToEbitda`, `freeCashflow`) can silently
mix currencies. Rebuild EV, P/B, EV/EBITDA and FCF-yield from the raw statements + market cap in one
currency. The screen's headline "6.4x / 41% FCF-yield / P/B 17.1" for NTES should be **disregarded**.

### 2.2 Corrected valuation (all reconstructed in RMB; market cap converted at 6.7721)

| Metric | Value | Basis |
|---|--:|---|
| Market cap | **US$82.1bn** (¥556bn) | yfinance 2026-07-02, VERIFIED |
| Net cash (cash+time deposits+ST inv − total debt) | **¥156bn FY25 / ¥167.5bn Q1-26 (~US$24.3-24.7bn)** | 20-F FY25 & IR Q1-26, VERIFIED |
| Net cash as % of market cap | **~28-30%** | computed |
| Enterprise value (net-cash adj.) | **¥400bn (~US$59bn)** | mktcap − net cash |
| **P/E (trailing)** | **~16.5x** | ¥556bn ÷ ¥33.8bn NI |
| **P/E (forward)** | **~12.1x** | yfinance forwardPE, VERIFIED |
| **P/E ex-net-cash** | **~11.5x** | (mktcap − net cash) ÷ NI |
| **EV/EBITDA (net-cash adj.)** | **~10.5x** | ¥400bn ÷ ¥38.1bn |
| **EV/EBIT (net-cash adj.)** | **~11.2x** | ¥400bn ÷ ¥35.8bn |
| **P/B** | **~3.5x** | ¥556bn ÷ ¥160.3bn equity |
| **FCF yield (FCF/mktcap)** | **~8.8%** | ¥48.7bn FCF ÷ ¥556bn |
| **FCF yield on EV** | **~12.2%** | ¥48.7bn ÷ ¥400bn |
| Dividend yield (fwd, Q1-26 rate ×4) | **~2.2-2.5%** | $0.72/ADS/qtr × 4 ÷ $128.27, VERIFIED |

FY2025 income/BS/CF from yfinance statements (2026-07-02, VERIFIED as a real fetch; UNVERIFIED vs a
second source except where the 20-F/IR corroborate). Note: the **~41% FCF-yield** in the screen was
also an artifact (RMB FCF ÷ USD market cap). Real FCF yield ~8.8% — still healthy, but not 41%.

### 2.3 Vs its own history and vs peers

- **Vs own history:** ~12x forward P/E is near the **low end of NTES's 10-yr range** (historically
  ~15-25x; UNVERIFIED — macrotrends P/E page was paywalled, so this range is ASSUMED from general
  knowledge, flag to re-verify). The de-rate reflects the post-2021 China-tech compression.
- **Vs peers (yfinance `info`, 2026-07-02, VERIFIED fetches — note peer EV/EBITDA can carry the same
  ADR/currency artifacts; use P/E as the cleaner cross-market comp):**

| Company | Ticker | P/E | Fwd P/E | P/B | ROE | Gross mgn | Op mgn | Div yld |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| **NetEase** | NTES | ~16.5 | ~12.1 | **~3.5*** | 22.1% | 65.7% | 41.4% | 2.3% |
| Tencent | 0700.HK | 15.4 | 11.3 | 3.0 | 20.5% | 56.4% | 34.3% | 1.2% |
| Nintendo | 7974.T / NTDOY | ~19.7 | ~21 | 2.8 | 14.9% | 39.3% | 14.7% | ~3.2% |
| Electronic Arts | EA | 58.6 | 21.3 | 7.6 | 13.5% | 79.0% | 24.0% | 0.4% |
| Take-Two | TTWO | n/a (loss) | 25.0 | 13.2 | −10.6% | 57.7% | 2.3% | — |
| PDD Holdings | PDD | 8.7 | 6.7 | 1.9 | 25.4% | 56.0% | 18.4% | — |

*NTES P/B shown corrected (yfinance raw 16.9 is the artifact).

**Read:** NTES has the **highest operating margin (41%) and near-highest ROE (22%)** in the group,
yet trades at ~12x forward — cheaper than Nintendo (~21x fwd, half the margin) and EA/Take-Two (loss
or ~21-25x fwd), and roughly in line with Tencent (a more diversified, arguably higher-quality
platform). The EA take-private (~US$55bn LBO, announced Sept 2025, PIF/Silver Lake — VERIFIED)
signals strategic appetite for premium games IP at a far richer multiple than NTES's public price.
**Bottom line:** NTES is inexpensive on P/E vs both its history and Western games peers of *lower*
quality; the EV/EBITDA (~10.5x) is merely reasonable, not screaming-cheap. The cheapness lives in
the **ex-cash P/E (~11.5x)** and the **China discount**, not in a distressed EV/EBITDA.

---

## 3. Quality — high, with a fortress balance sheet

FY2025 (RMB, yfinance statements 2026-07-02; corroborated by 20-F/IR where noted; VERIFIED fetch):

| Metric | FY2025 | Trend | Note |
|---|--:|---|---|
| Revenue | ¥112.6bn | +7% YoY | 4-yr CAGR positive; Q1-26 +6.1% YoY (IR, VERIFIED). |
| Gross margin | **64-69%** | rising | FY25 64% (full-yr statement) / 69% (Q1-26 IR) — mix toward high-margin games. |
| Operating margin | **~32%** | rising | ¥35.8bn op income. |
| Net margin | ~30% | stable-high | ¥33.8bn NI. |
| **ROE** | **~21%** | stable | ¥33.8bn NI ÷ ¥160.3bn equity. |
| ROA | ~15% | — | asset-light. |
| **FCF** | **¥48.7bn** | rising | FCF/NI conversion **~144%** (low capex, ¥2bn). Exceptional. |
| **Net cash** | **~US$24bn+** | growing | ~28-30% of market cap; near-zero net debt (debt ¥6.7bn, falling). |

**Returns on capital.** Reported ROE ~21% (VERIFIED). ROIC is even higher (asset-light, low debt) —
the screen's ROIC proxy was flagged unreliable/inflated for cash-heavy names, so **rank on ROE ~21%**.
Ex the huge cash drag, returns on *operating* capital are very high (op income ¥35.8bn on modest
tangible capital).

**Shareholder returns (quantified):**
- **Dividend:** NTES pays a **quarterly** dividend (unusual for a Chinese internet name). Q1-26
  declared **$0.144/ordinary share = $0.720/ADS** (IR, VERIFIED). FY2025 cash dividends paid ¥13.8bn
  (~US$2.0bn) → **~2.5% dividend yield**, payout ~40%.
- **Buyback:** **US$5.0bn** program, extended to Jan 9 2029; **US$2.1bn (23.2M ADS) repurchased to
  date** (IR Q1-26, VERIFIED). FY2025 buyback was light (¥0.6bn) after heavier 2022-24 years (¥8.3bn/
  ¥5.2bn/¥8.8bn) — repurchase pace is lumpy.
- **Total shareholder yield:** dividend ~2.5% + buyback ~0.1% in FY25 (~2.6%), but in a heavy-buyback
  year (e.g. FY2024's ¥8.8bn ≈ ~1.6% buyback) the total ran ~4%+. Call the **through-cycle shareholder
  yield ~3-5%.** (VERIFIED from cash-flow statement.)

**Franchise durability.** The Westward Journey franchise (24+ years) is the most durable asset —
proof of long-tail live-service economics. Newer hits (*Marvel Rivals*, *Where Winds Meet*) add
growth but are hit-driven and can fade fast (see §4). **Quality is high and above the peer set** —
this is the "quality-first" name the framing wants; the debate is entirely about *risk*, not quality.

---

## 4. Bear case / risks — argue both sides

### 4.1 VIE structure — the real governance risk (must-read)

**What you actually own.** NTES/9999 is a **Cayman Islands holding company**. Foreign ownership of
Chinese internet/gaming/content businesses is restricted, so the Cayman parent does **not own equity**
in the mainland operating companies. Instead it consolidates them as **Variable Interest Entities
(VIEs)** via a web of contracts (exclusive service agreements, equity pledges, powers of attorney).
Per the FY2025 20-F (VERIFIED): *"All of the VIEs are domestic companies incorporated in China
mainland in which we do not have any equity ownership, but their financial results have been
consolidated…"* and **VIE-generated revenue was 87.7% / 87.2% / 85.2% of total in 2023/2024/2025.**

- **Bear:** You own a shell with *contractual claims* over the assets that produce ~85% of revenue —
  not the assets themselves. Enforceability of VIE contracts under PRC law has never been fully tested;
  Beijing could restrict/void the structure; dividends must clear PRC capital controls to reach you.
  If the contracts fail, the equity could be near-worthless despite the operating business thriving.
- **Bull:** VIEs are the *universal* structure for every Chinese ADR (Alibaba, Tencent-HK-equivalents,
  PDD, Baidu). China's 2021-2023 overseas-listing rules (CSRC filing regime) effectively *blessed and
  regularized* rather than banned VIEs. A wholesale voiding would nuke China's access to global capital
  — self-defeating. It has held for 20+ years. This is a tail risk, not a base case.
- **Verdict:** genuine, non-diversifiable governance risk that *is* the reason for a chunk of the
  discount. Size the position accordingly; do not treat NTES equity as equivalent to owning NetEase.

### 4.2 China games regulation

- **Bear:** The state controls supply via **banhao (版号) approval licenses** (NPPA) and can freeze
  them (it did, Aug-2021→Apr-2022, ~8 months). The **Dec-2023 draft rules** (spending caps, reward
  bans) wiped ~US$80bn off Tencent+NetEase in a day (NTES −24-25%). Minors are capped at ~3 hrs/week
  since Aug 2021. Any hostile policy is a step-change, un-hedgeable, overnight.
- **Bull (and current state — VERIFIED from nppa.gov.cn counts):** approvals have **normalized and
  expanded** — 1,075 (2023) → **1,416 (2024, +32%, most since 2019)** → **1,771 (2025, +25%)**, steady
  monthly batches into 2026. The **Dec-2023 draft rules were softened, the responsible official was
  removed, and the draft was deleted from the NPPA site on Jan 23 2024 — never promulgated; spending
  caps never took legal effect.** NetEase's key titles got approvals (*Where Winds Meet* Jun-2023;
  *Marvel Rivals* import ~Aug-2024). The minors' rule is long absorbed (minors are a small revenue
  share). **The overhang has cleared — this is the re-rating catalyst, not just a risk.**
- **Verdict:** currently the *most improved* of the risks; but the Dec-2023 episode proves it can flare
  without warning. Priced, improving, but binary.

### 4.3 ADR delisting / HFCAA — largely resolved (note)

- The **Dec 15 2022 PCAOB determination** confirmed it can now inspect mainland-China + HK auditors,
  vacating the 2021 adverse finding. NetEase's FY2025 20-F states it *"does not expect to be identified
  as a Commission-Identified Issuer."* **NetEase is not currently at HFCAA delisting risk** (VERIFIED,
  20-F + SEC Federal Register 91 FR 29183, 2026-05-19).
- 2025-26 friction (Feb-2025 "America First Investment Policy" memo; Nasdaq's new China-*listing* rule,
  SEC-approved ~May-2026) targets **new listings only** — NetEase (listed since 2000) is **grandfathered**
  (VERIFIED). Backstop: **HK secondary listing 9999.HK** since Jun-2020 — Hooman can hold the HK line to
  sidestep ADR-specific risk.
- **Verdict:** dormant, not active. A residual US-China-relations tail risk, but not a live threat.

### 4.4 Other risks
- **China macro / consumer:** discretionary gaming spend is macro-sensitive; a weak Chinese consumer
  caps growth. Offsetting: games are cheap entertainment, historically resilient.
- **Hit-driven concentration:** ~82% of revenue is games; per-title revenue is never disclosed
  (UNVERIFIED concentration). *Marvel Rivals* concurrent players fell **~77% from the Jan-2025 peak**
  by mid-2026, and NetEase laid off its Seattle design team Feb-2025 — a reminder that live-service
  hits fade fast and overseas studio bets are being pulled back. The evergreen franchises (Westward
  Journey) are the dependable anchor; new hits are optionality, not the base.
- **FX / capital controls:** earnings are RMB; cash largely onshore; getting it to shareholders needs
  to clear PRC capital controls.

---

## 5. Catalysts & scorecard verdict

**Catalysts (positive):** (1) continued normal banhao flow → confidence the overhang stays cleared;
(2) global expansion of *Where Winds Meet* / *Marvel Rivals* / *Destiny: Rising* (Bungie IP) as
non-China revenue; (3) a step-up in buyback pace toward the US$5bn authorization; (4) any thaw in
US-China relations compressing the China discount; (5) Blizzard-title ramp in China. **Catalyst
weight is low** — the thesis is "cheap quality + discount unwinds," not an event.

### Scorecard (CLAUDE.md §3 weights)

| Factor | Weight | Score /10 | Rationale |
|---|--:|--:|---|
| **Cheapness** | 30% | **7** | ~12x fwd / ~11.5x ex-cash P/E, ~10.5x adj. EV/EBITDA, ~8.8% FCF-yield, ~28-30% net cash. Cheap vs own history & vs lower-quality Western peers — but *not* the 6.4x/41% the screen implied (artifacts). Solidly cheap, not distressed-cheap. |
| **Quality** | 30% | **8** | ~21% ROE, 65%+ gross / ~40% op margin, ~144% FCF conversion, US$24bn+ net cash, dividend + buyback, 20+ yr franchises. Top-tier — best in the games peer set. |
| **Trap-risk (inverse)** | 20% | **6** | Not a classic value trap (real earnings, real cash, growing). But the *structural* risks (VIE, regulation) are un-hedgeable and binary — caps this. Piotroski 7/7 (VERIFIED screen). |
| **Moat & leadership** | 15% | **7** | #2 in China games with durable self-developed IP; founder owns ~45.5% one-share-one-vote (aligned, no super-voting — shareholder-friendly). Below Tencent's platform moat; hit-driven at the margin. |
| **Catalyst** | 5% | **6** | Overhang-clearing + buyback + global launches; no single hard catalyst. |

**Weighted total = 0.30·7 + 0.30·8 + 0.20·6 + 0.15·7 + 0.05·6 = 2.10 + 2.40 + 1.20 + 1.05 + 0.30 = 6.90 / 10.**

### Verdict: **WATCH → BUY-worth-more-work**

At ~6.9 NTES clears the bar for further work but not an unconditional buy. It is a **high-quality,
cash-rich, founder-aligned games compounder at a value multiple**, where the cheapness is ~2/3 a
China/VIE discount and ~1/3 genuine value. **The decision hinges on risk appetite, not quality:** if
Hooman is willing to own the China-tech/VIE risk (ideally sized modestly and possibly via 9999.HK to
sidestep ADR-specific tail risk), NTES is one of the better risk-adjusted ways to do it — better
quality than PDD/Baidu, more games-pure and cheaper-vs-quality than Tencent. If the VIE "you-own-a-
shell" structure or binary regulation risk is a hard no, **PASS** — no valuation compensates for a
structure you don't trust.

**Re-verify before acting:** (a) NTES 10-yr P/E range (macrotrends paywalled — the "low end of range"
claim is ASSUMED); (b) peer EV/EBITDA (may carry ADR artifacts); (c) exact Youdao/Cloud Music segment
splits (ASSUMED); (d) *Marvel Rivals* banhao platform/date. Cross-checked primary sources: FY2025 20-F
(sec.gov/Archives/edgar/data/1110646/000110465926043468/ntes-20251231x20f.htm, filed 2026-04-15, UA
"Hooman Shariati hshariati@adobe.com"); Q1-2026 IR 6-K (…/000110465926064764/tm2615053d1_ex99-1.htm);
NPPA approval counts (nppa.gov.cn); SEC Federal Register 91 FR 29183.
