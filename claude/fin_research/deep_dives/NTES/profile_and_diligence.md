# NetEase, Inc. (NTES) — Company Primer + Deeper Diligence

**Prepared:** 2026-07-03 by Claude (Opus 4.8) for Hooman Shariati (Canadian citizen). **Research, not financial advice.**
**Listings:** Nasdaq **NTES** (ADR/ADS — an American Depositary Share; **1 ADS = 5 ordinary shares**) and HKEX **9999.HK** (secondary listing, June 2020). HQ Hangzhou, China.
**Companion doc:** `deep_dive.md` (Stage-4 valuation deep dive, score **6.9/10**). This file is the newcomer-friendly **primer + tie-out to primary filings**. It builds on the deep dive; it does not repeat the full bear-case argument (see deep_dive §4).

> **Anti-hallucination.** Every figure carries a source + as-of date and a confidence mark (VERIFIED / ASSUMED / UNVERIFIED). NetEase reports in **RMB (Chinese yuan)** with a USD "convenience translation." **All multiples below are rebuilt in ONE currency** — because yfinance's raw `info` fields (EV/EBITDA 6.4, P/B 17, FCF-yield 41%) for this ADR are **known artifacts** from mixing a USD market cap with RMB financials (proven in deep_dive §2). When I convert, USD/CNY = **6.7721** (yfinance spot, 2026-07-02). NetEase's own filings use **6.9942** (20-F FY2025 convenience rate).

---

## Quick orientation (read this first if you're new to the name)

NetEase is **China's #2 video-games company behind Tencent** — a founder-controlled, cash-gushing games publisher that also owns a small education arm (Youdao), a music-streaming service (Cloud Music), and an e-commerce brand (Yanxuan). It is genuinely high-quality (64% gross margin, 21% ROE, ~US$24bn net cash = ~30% of its market cap, growing dividend + buyback) trading at a **value multiple** (~12x forward earnings, ~11x ex-cash) — the low end of its own 10-year history. **The catch is not quality; it's structure and geography:** you buy a Cayman-Islands shell that holds *contracts* over — not equity in — the mainland Chinese companies that make ~85% of the revenue (the "**VIE**" structure), plus the usual China-ADR/regulatory discount. The debate is entirely about whether that risk is worth the discount.

**Jargon, defined once (used throughout):**
- **ADR / ADS** — a US-listed proxy for a foreign share. Here 1 ADS (what trades as "NTES") = 5 ordinary shares.
- **VIE (Variable Interest Entity)** — a contractual structure Chinese tech firms use so foreigners can get the *economics* of a restricted Chinese business without legally *owning* it. Detailed in Part A §2.
- **Live-ops (live-service)** — running a game as an ongoing service (updates, events, in-game purchases) for years, not a one-time boxed sale. This is the source of games' recurring, high-margin revenue.
- **banhao (版号)** — the Chinese government approval license every game needs before it can monetize in China. The state controls games *supply* by controlling banhao issuance.
- **HFCAA** — the US Holding Foreign Companies Accountable Act, which can delist ADRs whose auditors the US regulator (PCAOB) cannot inspect. Explained in §2.
- **Ex-cash multiple** — a P/E or EV/EBITDA computed after subtracting the company's net cash from its price. It answers "what am I paying for the *operating business* alone, ignoring the cash pile?" For a company with ~30% of its value in cash, this is the honest multiple.

---

# PART A — Business primer

## A1. What NetEase does

NetEase is a **games company first, everything else second.** Games and related value-added services were **82% of FY2025 revenue**, and within that segment **97.3% is online games** (i.e. games are ~80% of the whole company). (FY2025 20-F, filed 2026-04-15, **VERIFIED**.)

**FY2025 revenue by segment** (20-F, RMB, **VERIFIED**; USD at the filing's 6.9942 rate):

| Segment | FY2025 (RMB) | FY2025 (US$) | % of total | What it is |
|---|--:|--:|--:|---|
| **Games & related value-added services** | ¥92.15bn | $13.18bn | **81.8%** | The engine. Self-developed PC/mobile franchises + licensed titles (incl. Blizzard). |
| **Youdao** (9899… no — Nasdaq: **DAO**) | ¥5.91bn | $0.85bn | 5.2% | EdTech / online learning / dictionary; separately US-listed. |
| **NetEase Cloud Music** (HKEX: **9899.HK**) | ¥7.76bn | $1.11bn | 6.9% | Music streaming — the "Spotify of China" #2 behind Tencent Music; separately HK-listed. |
| **Innovative businesses & others** | ¥6.81bn | $0.97bn | 6.0% | **Yanxuan** (private-label e-commerce), advertising, misc. |
| **Total net revenues** | **¥112.63bn** | **$16.11bn** | 100% | +7.0% YoY vs ¥105.30bn FY2024. |

(Segment splits are now **VERIFIED exact** from the 20-F, upgrading the deep dive's "estimated" Youdao/Cloud-Music figures.)

**The games franchise — why it's durable.** NetEase's moat is a stable of **long-running, self-developed franchises with 15-25 year lifespans**, run as live-ops:
- ***Fantasy Westward Journey* / *Westward Journey Online*** (since 2001-02) — the 24-year-old cash cow, still cited every quarter (**VERIFIED**, IR).
- ***Justice / Ni Shui Han***, ***Naraka: Bladepoint***, ***Identity V***, ***Onmyoji***, ***Eggy Party*** — the mid-life catalog.
- **New global hits (2024-26):** ***Marvel Rivals*** (free-to-play hero shooter, launched Dec 2024, 40M+ players by Feb 2025) and ***Where Winds Meet*** (open-world RPG, 80M+ cumulative players by early 2026) — these drove the FY24→FY25 games growth. *Caveat:* Marvel Rivals concurrent players fell **~77% off the Jan-2025 peak** by mid-2026 and NetEase cut its Seattle team — a live-service hit can fade fast (deep_dive §4.4, **VERIFIED**).
- **Blizzard partnership RESUMED.** NetEase distributed Blizzard's games in China for 14 years until the deal lapsed Nov 2022 (WoW/Hearthstone/Overwatch went dark in China Jan 2023). A **new agreement was struck ~April 2024** and the titles are back live with NetEase — this removed a real overhang (**VERIFIED**, deep_dive §1).

## A2. Ownership, management & the VIE structure

**Founder control — and why it's a governance *positive* here.**
- Founder **William Ding (Ding Lei)** owns **~44-45%** of NetEase (**ASSUMED** ~44.6% from prior 20-F beneficial-ownership disclosure; the FY2025 20-F confirms he remains the controlling shareholder — treat the exact % as approximate).
- Crucially, NetEase has **one class of ordinary shares, one-share-one-vote — no dual-class super-voting structure.** This is a **governance positive versus many Chinese/US tech peers** (Alibaba, Baidu, JD, and Google/Meta all use super-voting founder shares). Ding's control comes from a genuine ~45% economic stake, not from 10x-vote shares that let a founder control the company while owning a sliver. Interests are aligned with outside shareholders. (Share structure **VERIFIED** from 20-F; ownership % **ASSUMED**.)
- Founder-led since 1997; long-term, disciplined, cash-generative culture. Ding is famously frugal with capital and returns cash via dividends + buybacks.

**The VIE structure — the real, un-hedgeable risk (the single most important thing to understand).**

When you buy NTES on Nasdaq (or 9999.HK), **you do NOT own the Chinese operating companies.** Here is the chain, in plain terms:
1. China **prohibits/restricts foreign ownership** of internet, gaming, and content businesses.
2. So the entity you buy is a **Cayman Islands holding company** ("NetEase, Inc.").
3. That Cayman company **does not hold equity** in the mainland Chinese operating companies. Instead it consolidates them as **Variable Interest Entities (VIEs)** through a web of **contracts** — exclusive-service agreements, equity pledges, powers of attorney, loan agreements — that route the *economics and control* (but not legal ownership) up to the Cayman parent.
4. The 20-F states it plainly (**VERIFIED**): *"All of the VIEs are domestic companies incorporated in China mainland in which we do not have any equity ownership, but their financial results have been consolidated…"*
5. **The VIEs generated 87.7% / 87.2% / 85.2% of total net revenues in 2023 / 2024 / 2025** (20-F, **VERIFIED**). So ~85% of the revenue you're "buying" flows through entities you legally do not own.

**Why this is a genuine risk (bear):** VIE contracts have **never been fully tested/enforced** in PRC courts. Beijing could restrict, reinterpret, or void the structure; getting cash out to foreign holders must clear **PRC capital controls**. In a worst case the contracts fail and the equity is impaired *even if the underlying business thrives.* This is **not diversifiable and not hedgeable** — it is a chunk of why the stock is cheap.

**Why it's a tail risk, not a base case (bull):** VIEs are the **universal** structure for *every* Chinese ADR (Alibaba, PDD, Baidu, Tencent's HK-listed equivalents). China's 2021-2023 overseas-listing rules (the CSRC filing regime) effectively **regularized and blessed** VIEs rather than banning them — a wholesale voiding would cut China off from global capital and is self-defeating. The structure has held for 20+ years. (deep_dive §4.1, **VERIFIED**.)

**HFCAA / ADR-delisting history — largely resolved.**
- NetEase *was* named a "Commission-Identified Issuer" under the HFCAA after its FY2021 20-F (because the US audit regulator, PCAOB, couldn't then inspect China-based auditors).
- On **Dec 15, 2022 the PCAOB vacated that determination** — it regained the ability to inspect auditors in mainland China and Hong Kong. NetEase's FY2025 20-F states it **does not expect to be identified as a Commission-Identified Issuer** (**VERIFIED**). PCAOB reassesses annually, so it's dormant, not permanently closed.
- 2025-26 US-China friction (the "America First Investment Policy" memo; a new Nasdaq China-*listing* rule) targets **new listings only** — NetEase (listed since 2000) is grandfathered (deep_dive §4.3, **VERIFIED**).
- **Backstop:** the **9999.HK Hong Kong secondary listing** (since June 2020) lets a holder sidestep ADR-specific delisting risk entirely by holding the HK line. As a **Canadian citizen**, Hooman can hold 9999.HK directly.

## A3. Business model & moat

**Games economics = the good business.** Online games are **high-margin, recurring, and long-lived**: once a game is built, each additional player is nearly pure margin, and live-ops (events, seasons, in-game items) keep a 20-year-old franchise generating cash. That is why NetEase runs **64% gross margin and ~32% operating margin** on ~80%-games revenue (FY2025 20-F, **VERIFIED**), and converts profit to cash at ~144% (very low capex — it's a code-and-servers business, not factories).

**The fortress balance sheet.** At Q1-2026 NetEase held **RMB 167.5bn (~US$24.3bn) net cash** (cash + time deposits + short-term investments minus borrowings), = **~28-30% of the ~US$82bn market cap** (Q1-2026 6-K, **VERIFIED**; FY2025 20-F components tie out: cash ¥47.2bn + time deposits ¥95.6bn + ST investments ¥22.8bn − borrowings ¥6.4bn ≈ ¥159bn at year-end, **VERIFIED**). Near-zero net debt.

**Shareholder returns.** Unusually for a Chinese internet name, NetEase pays a **quarterly dividend** and buys back stock:
- **Dividend:** four quarterly dividends declared for FY2025 totaling **US$0.68 + $0.57 + $0.57 + $1.16 = ~US$2.98/ADS** (the Q4 figure is a larger year-end dividend). Cash dividends *paid* in FY2025 = **RMB 13.8bn (~US$2.0bn)**, payout ~40% (20-F, **VERIFIED**). Forward yield ~2.3-2.5%.
- **Buyback:** **US$5.0bn** authorization extended to **Jan 9, 2029**; **~23.2M ADS / ~US$2.1bn** repurchased to date (Q1-2026 6-K, **VERIFIED**). Pace is lumpy and was near-dormant in H2-2025.
- **Through-cycle total shareholder yield ~3-5%** (deep_dive §3, **VERIFIED**).

**Why it's "cheap" (net read from deep_dive §1, reaffirmed):** ~**2/3 China/VIE discount, ~1/3 genuine value.** Every China ADR carries a geopolitical/VIE/capital-controls discount regardless of fundamentals (the primary driver); a fading games-regulation overhang is secondary; and ex-cash ~11x P/E for a 21%-ROE compounder is genuinely cheap on its own merits (partial).

---

# PART B — Deeper diligence

## B1. Recent earnings prints (FY2025 quarters + Q1-2026) — tied out to SEC filings

All figures below were read directly from **SEC 6-K earnings exhibits and the FY2025 20-F** (CIK 0001110646), UA header "Hooman Shariati hshariati@adobe.com". **VERIFIED** unless flagged. RMB with USD convenience as reported. Margins marked "derived" are computed from reported RMB profit ÷ revenue (releases quote rounded RMB billions, not the %).

| Metric | Q1 2025 | Q2 2025 | Q3 2025 | Q4 2025 | Q1 2026 |
|---|--:|--:|--:|--:|--:|
| **Total net revenues** | ¥28.8bn | ¥27.9bn | ¥28.4bn | ¥27.5bn | **¥30.6bn** |
| YoY growth | +7.4% | +9.4% | +8.2% | +3.0% | **+6.1%** |
| **Games & VAS** | ¥24.0bn (+12.1%) | ¥22.8bn (+13.7%) | ¥23.3bn (+11.8%) | ¥22.0bn (+3.4%) | **¥25.7bn (+6.9%)** |
| **Youdao** | ¥1.3bn (−6.7%) | ¥1.4bn (+7.2%) | ¥1.6bn (+3.6%) | ¥1.6bn (+16.8%) | ¥1.35bn (+3.8%) |
| **Cloud Music** | ¥1.9bn (−8.4%) | ¥2.0bn (−3.5%) | ¥2.0bn (−1.8%) | ¥2.0bn (+4.7%) | ¥1.98bn (+6.6%) |
| **Innovative & others** | ¥1.6bn (−17.6%) | ¥1.7bn (−17.8%) | ¥1.4bn (−18.9%) | ¥2.0bn (−10.4%) | ¥1.55bn (−4.6%) |
| **Gross margin** | ~64.1% (der.) | ~64.9% (der.) | ~64.1% (der.) | ~64.3% | **~69.3% (der.)** |
| **Operating profit** | ¥10.4bn | ¥9.06bn | ¥8.01bn | ¥8.3bn | **¥12.66bn** |
| Operating margin | ~36.2% (der.) | ~32.5% (der.) | ~28.3% (der.) | ~30.2% (der.) | **41.4% (der.)** |
| **Net income (to shareholders)** | ¥10.3bn | ¥8.6bn | ¥8.6bn | ¥6.2bn | **¥10.67bn** |
| **Dividend declared / ADS** | US$0.675 | US$0.570 | US$0.570 | US$1.16 | US$0.720 |

Source URLs (all **VERIFIED** SEC 6-K exhibits): Q1-25 `…000110465925048779/tm2514907d1_ex99-1.htm`; Q2-25 `…000110465925077838/tm2522950d2_ex99-1.htm`; Q3-25 `…000110465925114338/tm2531333d1_ex99-1.htm`; Q4-25/FY25 `…000110465926012943/tm265608d1_ex99-1.htm`; Q1-26 `…000110465926064764/tm2615053d1_ex99-1.htm`.

**FY2025 full year (20-F tie-out, VERIFIED):** revenue **¥112.63bn (+7.0%)**; gross profit **¥72.40bn (64.3% margin)**; operating profit **¥35.83bn (31.8% margin)**; net income to shareholders **¥33.76bn (30.0% margin)**; diluted EPS ¥10.48 / diluted per ADS ¥52.42 (US$7.50); shareholders' equity **¥160.30bn**; shares outstanding **3.192bn ordinary** (÷5 = ~638M ADS-equivalent).

**Two things worth flagging in the trend:**
1. **Quarterly net income *fell* through FY2025** (¥10.3bn Q1 → ¥6.2bn Q4) even as revenue held, then **rebounded to ¥10.67bn in Q1-2026** with operating margin snapping back to 41.4% and gross margin to ~69%. The FY2025 back-half softness appears to be higher opex / lower-margin quarters; Q1-2026 shows the margin engine intact. Watch whether the Q1-26 margin recovery holds.
2. **The non-games segments are flat-to-shrinking.** Cloud Music was roughly flat/declining most of 2025; "Innovative & others" (Yanxuan) shrank double-digits all year. The thesis rests almost entirely on **games**.

## B2. Valuation — corrected, single-currency (rebuilt from the 20-F)

**All-in-RMB reconstruction** (FY2025 20-F statements; net cash from Q1-2026 6-K; market cap US$81.5bn = ~¥552bn at 6.7721, yfinance 2026-07-03). This **supersedes the yfinance raw `info` fields**, which are currency-mix artifacts (deep_dive §2).

| Metric | Corrected value | Basis | Confidence |
|---|--:|---|:--|
| Market cap | **US$81.5bn (¥552bn)** | yfinance 2026-07-03 | VERIFIED |
| Net cash (Q1-2026) | **¥167.5bn (~US$24.3bn)** | Q1-26 6-K | VERIFIED |
| Net cash % of market cap | **~28-30%** | computed | VERIFIED |
| Enterprise value (net-cash adj.) | **~¥385bn (~US$57bn)** | mktcap − net cash | VERIFIED |
| **P/E (trailing)** | **~16.4x** | ¥552bn ÷ ¥33.76bn NI | VERIFIED |
| **P/E (forward)** | **~12.0x** | yfinance forwardPE 2026-07-03 | VERIFIED |
| **P/E ex-net-cash** | **~11.4x** | (mktcap − net cash) ÷ NI | VERIFIED |
| **EV/EBITDA (net-cash adj.)** | **~10.1-10.5x** | EV ÷ ~¥38bn EBITDA | VERIFIED (EBITDA est.) |
| **EV/EBIT (net-cash adj.)** | **~10.7-11.2x** | EV ÷ ¥35.8bn op profit | VERIFIED |
| **P/B** | **~3.4x** | ¥552bn ÷ ¥160.3bn equity | VERIFIED |
| **FCF yield (FCF/mktcap)** | **~8.8%** | ¥48.7bn FCF ÷ ¥552bn | VERIFIED |
| **FCF yield on EV** | **~12.7%** | ¥48.7bn ÷ EV | VERIFIED |
| Dividend yield (fwd) | **~2.3-2.5%** | run-rate ÷ ADS price | VERIFIED |

> **Reminder of the artifact:** yfinance raw shows EV/EBITDA **6.4**, P/B **16.8**, FCF-yield **~41%** for NTES — **all wrong**, from dividing/comparing a USD market cap against RMB balance-sheet and cash-flow items (deep_dive §2 proves each). Use the corrected column. The real story is "reasonably cheap," not "distressed-cheap."

**Vs its own history (now VERIFIED, upgraded from the deep dive's ASSUMED).** Macrotrends year-end trailing P/E, 2016-2025 (**VERIFIED**, fetched 2026-07-03): 14.3 / 23.6 / 29.3 / 11.6 / 31.1 / 23.4 / 14.9 / 13.7 / 13.6 / 18.1. **Min ~11.6, median ~16.5, max ~31.** Current **~16x trailing / ~12x forward sits at the LOW end** — NTES de-rated from the ~25-31x of 2017-2021 to the low-teens post-2022 China-tech compression. So it's cheap vs its own 10-year range, though not at an absolute historic trough (2019 and 2023-24 year-ends printed a touch lower).

## B3. Competitor & sector comparison

Peer data from yfinance `info` (2026-07-03, **VERIFIED** fetches) plus stockanalysis.com FY figures (**VERIFIED**, 2026-07-03). **Use P/E and operating margin as the cleaner cross-market comps** — EV/EBITDA for ADRs/foreign filers can carry the same currency artifact, and EA/TTWO/RBLX multiples are distorted (EA by its take-private price, TTWO/RBLX by losses).

| Company | Ticker | Trailing P/E | Fwd P/E | P/B | ROE | Gross mgn | Op mgn | Rev growth | Net cash | Div yld |
|---|---|--:|--:|--:|--:|--:|--:|--:|:--|--:|
| **NetEase** | NTES | ~16.4 | **~12.0** | **~3.4*** | **22.1%** | 64% | **~32-41%** | +6-7% | **+US$24bn (~30% of cap)** | 2.4% |
| Tencent | 0700.HK | 15.0-15.5 | ~11.3 | 3.0 | 20.5% | 56% | ~33-35% | **+14%** | +¥16bn (thin) | 1.2% |
| Nintendo | 7974.T | 19.6 | ~21 | 2.8 | 14.9% | 39% | 15.6% | +99%† | **+¥2.2tn (all net cash)** | 3.1% |
| Electronic Arts | EA | 58.5‡ | 21.2 | 7.6 | 13.5% | 79% | 15-24% | +1% | +US$1.5bn | 0.4% |
| Take-Two | TTWO | n/a (loss) | 25.6 | 13.5 | −10.6% | 58% | ~neg | +18% | −US$1.0bn (net debt) | — |
| Roblox | RBLX | n/a (loss) | neg | 91.7 | −312% | 24% | −16 to −25% | +36-40% | +US$3.9bn incl LT inv | — |

\* NTES P/B shown **corrected** (yfinance raw 16.8 is the artifact). † Nintendo +99% is the Switch 2 launch year (FY ended Mar-2026) — not a steady-state rate. ‡ EA trailing P/E 58x reflects its stock trading near the **US$210/share take-private price** (PIF/Silver Lake/Affinity, ~US$55bn EV, announced Sept 29 2025, shareholder-approved Dec 2025, expected close ~mid-2026, **VERIFIED**) — a deal artifact, not fundamentals.

**Read — is NetEase cheap purely on the China/VIE discount?**
- **Vs Western peers:** NetEase has the **highest operating margin and near-highest ROE** in the group, a **fortress net-cash balance sheet (~30% of cap — only Nintendo rivals it)**, yet trades at **~12x forward** — cheaper than Nintendo (~21x fwd, ~half the margin), and far cheaper than EA (~21x fwd) or loss-making Take-Two (~26x fwd) / Roblox. The EA take-private at ~US$55bn / rich multiple shows strategic buyers pay up for premium games IP — NetEase is *higher-quality on margins/ROE* than EA but trades at ~40% of EA's forward multiple. **Yes — the gap vs Western peers is essentially the China/VIE discount, not a quality gap.** If NetEase were a US company with the same financials it would plausibly trade double the multiple.
- **Vs Tencent:** the two are close on P/E (~12x fwd each), ROE (~20-22%), and margins. Tencent is **more diversified** (WeChat/payments/cloud/ads + a games portfolio) and growing faster (+14% vs +6-7%), arguably a higher-quality *platform*; NetEase is a **purer, higher-margin games play** with a bigger relative cash cushion. They share the same China/VIE discount, so the choice is diversification (Tencent) vs games-purity + margin + net cash (NetEase). NetEase is **not** obviously cheaper than Tencent — the China discount is common to both.

**Bottom line:** NetEase is inexpensive on **forward P/E and ex-cash P/E (~11x)** vs both its own 10-year history and *lower-quality* Western peers. The corrected **EV/EBITDA ~10.5x is reasonable, not screaming-cheap** — the real value lives in the ex-cash P/E and the net-cash cushion, and the discount vs the West is a China/VIE-risk discount, not a quality discount.

## B4. What to watch (the diligence checklist)

1. **China games regulation / banhao flow — the swing factor.** The state controls games supply via banhao approval licenses (NPPA). **Current state is favorable and improving (VERIFIED):** approvals normalized and expanded — **1,075 (2023) → 1,416 (2024, +32%) → 1,771 (2025, +25%)**, steady monthly batches. The feared **Dec-2023 draft "spending-cap" rules were dropped** — walked back within weeks, the responsible official removed, never enacted (**VERIFIED**). *Risk:* the Dec-2023 scare (which cut ~US$80bn off Tencent+NetEase in a day) proves policy can flip overnight. **Watch:** continued normal monthly banhao batches (bullish) vs any new restrictive draft (step-change bearish).
2. **The VIE structure — the key *structural* risk.** ~85% of revenue flows through entities you don't legally own. Not hedgeable. **Watch:** any PRC move to reinterpret/restrict VIEs, or CSRC/capital-control changes affecting dividend repatriation. Mitigant: hold **9999.HK** to avoid ADR-specific delisting risk.
3. **Game-pipeline / new-title success (hit-driven).** ~80% of revenue is games and per-title revenue is never disclosed. Evergreen franchises (Fantasy Westward Journey, 24 yrs) are the dependable anchor; new hits are optionality that can fade fast (**Marvel Rivals −77% off peak**, Seattle studio cut, **VERIFIED**). **Watch:** *Where Winds Meet* global rollout, *Destiny: Rising* (Bungie IP), and whether new launches replace fading ones — and whether the Q1-26 margin rebound (op margin back to 41%) sustains after the soft FY2025 back-half.
4. **Blizzard-partnership contribution.** Resumed ~April 2024; WoW/Diablo/Hearthstone back in China with NetEase. **Watch:** whether it becomes a measurable revenue contributor (currently not separately disclosed).
5. **China consumer macro.** Discretionary gaming spend is macro-sensitive; a weak Chinese consumer caps growth (offset: games are cheap, resilient entertainment). The flat/shrinking Cloud Music + Yanxuan segments already show some consumer softness.

---

## Sources (primary, with as-of dates)
- **FY2025 Form 20-F** (FY ended 2025-12-31), filed **2026-04-15**: `sec.gov/Archives/edgar/data/1110646/000110465926043468/ntes-20251231x20f.htm` (CIK 0001110646). Revenue, segments, margins, net income, equity, cash components, VIE % (85.2%), dividends, HFCAA. **VERIFIED**, UA "Hooman Shariati hshariati@adobe.com".
- **Q1-2026 earnings 6-K**, filed **2026-05-21**: `…000110465926064764/tm2615053d1_ex99-1.htm`. Net cash US$24.3bn, Q1-26 P&L, dividend, buyback. **VERIFIED**.
- **FY2025 quarterly 6-K earnings exhibits** (Q1-Q4 2025), URLs in §B1. **VERIFIED**.
- **NTES 10-yr P/E history:** Macrotrends `macrotrends.net/stocks/charts/NTES/netease/pe-ratio`, fetched 2026-07-03. **VERIFIED**.
- **Peer fundamentals:** yfinance `info` (2026-07-03) + stockanalysis.com FY figures. **VERIFIED** fetches; EV/EBITDA for ADRs flagged as potentially artifact-prone.
- **EA take-private:** PIF/Silver Lake/Affinity, ~US$210/share, ~US$55bn, announced 2025-09-29 (multi-source). **VERIFIED**.
- **banhao counts / Dec-2023 draft withdrawal:** NPPA via Niko Partners / TechNode / Game World Observer. **VERIFIED**.
- **Companion:** `deep_dives/NTES/deep_dive.md` (score 6.9/10; artifact correction §2; bear case §4).

**Confidence notes:** Ding Lei ownership % is **ASSUMED** ~44-45% (exact figure not re-pulled from the FY2025 20-F beneficial-ownership table — verify before relying). Quarterly gross/operating margins marked "derived" are computed from rounded RMB inputs (±0.3pp). EBITDA (~¥38bn) is an estimate (op profit ¥35.8bn + modest D&A) since NetEase does not report EBITDA. All headline revenue/segment/net-income/dividend/net-cash figures are **VERIFIED** from primary filings.
