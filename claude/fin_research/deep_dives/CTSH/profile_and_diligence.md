# Cognizant (CTSH) — Company Primer & Deeper Diligence

**For:** Hooman (value investor, new to the name). **Prepared:** 2026-07-03 by Claude (Opus 4.8).
**Companion to** `deep_dive.md` (the valuation thesis) and `data/verified_financials.md` (the EDGAR tie-out).
This file is the **business/team/competitor/diligence** layer — it does not repeat the valuation verdict.

> **Not financial advice.** Research to inform Hooman's own decision (CLAUDE.md §1).
> **Confidence tags:** **[V]** verified from a primary filing / reliable source · **[A]** assumed/derived by me ·
> **[U]** unverified / single-source. Every number carries a source + as-of date.
>
> **Scope note:** the cross-cutting **AI-deflation** theme (does GenAI hollow out IT services?) is owned by a
> **separate theme agent** covering INTU/CTSH/TCS. It is referenced here only where it bears on the business;
> the full bull/bear is in `deep_dive.md §4(a)`. Do not treat §7 below as the AI deep-dive.

---

## Jargon glossary (read once)

- **Labor arbitrage** — the core IT-services business model: hire skilled engineers cheaply (mostly in India),
  bill their time to Western enterprises at a markup. Profit = the spread between offshore cost and Western
  billing rate. More headcount historically = more revenue.
- **TCV / bookings** — **Total Contract Value** of new deals signed. Cognizant reports **TTM bookings**
  (trailing-twelve-month), a leading indicator of future revenue. A "mega-deal" here = ≥$500M TCV; a "large
  deal" = ≥$100M.
- **Book-to-bill** — bookings ÷ revenue over a period. **>1.0 means the pipeline is growing faster than
  revenue is being recognized** (backlog building). CTSH runs ~1.3–1.4x.
- **Organic constant-currency (cc) growth** — revenue growth stripping out (a) acquisitions and (b) FX moves,
  so you see the underlying demand. This is the number that matters for a services firm; reported USD growth
  can be flattered or dented by the rupee/euro and by M&A.
- **BPO / BPS** — Business Process Outsourcing / Services: running a client's back-office processes (claims,
  finance ops, contact centers), not just software.
- **ADM** — Application Development & Maintenance: building and running the client's software estate. The
  bread-and-butter, most-arbitraged, most-AI-exposed line.

---

# PART A — Business Primer (for a newcomer)

## A1. What Cognizant does — in plain language

Cognizant is a **global IT-services and consulting firm**: enterprises pay it to build, run, and modernize
their technology and business processes. Concretely, it sells:
- **Digital engineering & application development/maintenance (ADM)** — writing and maintaining client software.
- **Cloud & infrastructure** — moving clients to AWS/Azure/GCP and running their IT.
- **Consulting & industry solutions** — domain-specific advice (e.g., helping a health insurer process claims).
- **Business process services (BPO)** — operating clients' back-office functions.

**The economic engine — labor arbitrage.** Cognizant employs **~351,600 people, of whom ~256,900 (73%) are in
India** [V, FY2025 10-K]. It bills those engineers mostly to **North American and European enterprises** at a
markup over its offshore delivery cost. Historically the growth formula was simple: **win more work → hire more
engineers → bill more hours.** (This is exactly the link GenAI now threatens — see §7 / `deep_dive.md §4a`.)

**Scale [V, FY2025 10-K / data/verified_financials.md]:**
- **FY2025 revenue: $21.108B** (+7.0% reported / **+6.4% organic cc**).
- **~351,600 employees** — a genuine large-cap of the services world.
- Delivery footprint: 256.9k India · 41.6k North America · 14.6k Continental Europe · 7.8k UK · 30.7k other.

**Four reporting segments (FY2025 cc growth) [V, Q4/FY2025 release 2026-02-04]:**
| Segment | ~% of revenue [A] | FY2025 cc growth | What it is |
|---|---|---|---|
| **Health Sciences** | **~30% (biggest)** | +6.4% | Payers, providers, life-sciences/pharma. CTSH's crown jewel; anchored by the 2014 **TriZetto** healthcare-IT acquisition ($2.7B) [V]. |
| **Financial Services** | ~20% | +6.8% | Banks, insurers, capital markets. |
| **Products & Resources** | ~23% | +9.7% | Manufacturing, retail, logistics, energy. Fastest-growing; now includes **Belcan** (aerospace/defense engineering). |
| **Comms, Media & Tech (CMT)** | ~19% | +0.7% | Telecom, media, tech clients. The laggard. |

> Segment % are approximate [A] — CTSH discloses segment revenue but the exact FY2025 split wasn't pulled to
> the dollar here. Health Sciences being the largest (~30%) is [V] and consistent across years.

**Geography:** majority North America (~70%+), with Europe and rest-of-world the balance. This matters because
the **demand cycle is a Western-enterprise-discretionary-spend cycle**, while the **cost base is Indian** — so
the model is long the rupee-vs-dollar spread and exposed to US visa policy (§7).

## A2. Management & the turnaround ("Project Leap" / "NextGen")

**Why there's a turnaround at all.** Through ~2019–2023 Cognizant **underperformed its peers**: FY2023 revenue
was **−0.4%** while TCS grew +13.7% cc, Infosys +15.4% cc, and Accenture +8% [V, respective FY2023 filings].
It also had a **culture/attrition problem** — trailing-12-month voluntary attrition **peaked at 32% in Q2 2022**
[V, SEC earnings exhibit] and multiple senior executives departed under prior CEO Brian Humphries [U, media].

**The CEO change.** **Brian Humphries** (CEO Apr-2019→Jan-2023) was **replaced by the board** — the 8-K uses
"replace"/without-cause language; "fired for underperformance" is media framing [V for the board action; U for
the reason]. **Ravi Kumar S** was appointed CEO **effective Jan-12-2023** [V, IR release]. Kumar is a **former
President of Infosys** (2016–2022, ran the Global Services Organization) — hired explicitly to **"reaccelerate
growth and drive shareholder value"** [V, appointment release]. **CFO Jatin Dalal** (ex-President & CFO of
**Wipro**) joined **Dec-2023** [V, IR release]. **Board chair: Stephen Rohleder**, ex-Accenture North America
Group CEO [V, company governance page]. So the top of the house is now staffed with **operators poached from
the two rivals CTSH was losing to** (Infosys, Wipro) plus an Accenture veteran as chair.

**What has actually improved [V]:**
- **Attrition collapsed:** 32% peak (Q2'22) → **~14.5% (Q3 2025)** [V, releases]. (Caveat: the 2021–22 figure
  is company-wide "voluntary"; 2023–25 is "Tech Services TTM" — closely related, not identically defined.)
- **Growth re-inflected:** FY2024 +2.0% → **five straight quarters of ~+6–8% cc growth** into FY2025 (+6.4% cc
  full-year) [V]. This is the single most important turnaround fact — the top line turned back up.
- **Margins expanded:** FY2025 GAAP operating margin **16.1% (+140 bps YoY)** [V].

**Two restructuring programs (don't confuse them):**
- **"NextGen" (2023–2024)** — post-pandemic office consolidation + delayering. Total charge **$363M** ($229M in
  2023 + $134M in 2024) — *not* the ~$400M some media reported [V, FY2024 10-K Note 4]. Reduced lease assets
  ~$170M cumulatively; ~3,500 jobs cut [U, media — not in filings].
- **"Project Leap" (2026)** — the current, **AI-framed** restructuring. Company-disclosed [V, Q1'26 10-Q / 8-K
  2026-04-29]: total cost **$230M–$320M** (of which **$200M–$270M** severance), substantially all in 2026;
  **in-year 2026 savings ~$200M–$300M**; raised 2026 adjusted-operating-margin guidance +20–40 bps. **The
  reported "12,000–15,000 job cuts, mostly India" figure is media/analyst, NOT disclosed by Cognizant** — the
  company gives only dollar costs and "associated reductions in headcount" [U for the headcount number].

> **Correction to prior notes:** `deep_dive.md §4a` cited Project Leap savings "by 2027" and "$270M severance"
> as a point estimate. Primary filings say **in-year 2026** savings and severance as the **top of a $200–270M
> range**. Minor, but flag it.

**Capital allocation [V, FY2025 10-K unless noted]:**
- **Buybacks:** $13.5B cumulative authorization (amended Mar-2025); **$1.92B remaining at Dec-31-2025**. FY2025
  repurchased ~17.4M shares / **$1.3B**. **Correction:** the "~10%/yr share-count reduction" in `deep_dive.md`
  is **overstated** — actual annual reduction is **low-single-digit %** (~17–19M shares/yr on ~490M
  outstanding). Share count did fall 578M (2018) → 474M (Q1'26), ~18% over seven years, i.e. ~2.5%/yr [V]. The
  **buyback *yield*** (dollars returned ÷ market cap) is ~2.4% at today's depressed price, but that's a
  price-driven yield, not a 10%/yr float shrink.
- **Dividend:** initiated 2017; grown ~5%/yr to **$0.33/qtr ($1.32 annualized), raised Feb-2026** [V]. Payout ~28%.
- **Bolt-on M&A:** **Belcan** (aerospace/defense engineering R&D) closed **Aug-26-2024 for ~$1.363B**
  (mostly cash + 1.47M shares) — pushes CTSH up-market into higher-value engineering [V, FY2025 10-K].
  **Thirdera** (elite ServiceNow partner, ~940 staff) closed **Jan-2024** (price undisclosed) [V]. Historic
  anchor: **TriZetto** (healthcare IT, $2.7B, 2014) — the foundation of the Health Sciences segment [V].

**Turnaround takeaway:** a **credible, evidence-backed operational recovery** — attrition normalized, growth
re-inflected, margins up, disciplined returns, and a management bench pulled from the rivals that beat CTSH.
The open question is not "is the turnaround real?" (it is, on the numbers) but "does GenAI break the model the
turnaround is built on?" (§7).

## A3. Business model & competitive position — where CTSH sits

**The IT-services hierarchy (roughly):**
- **Accenture (ACN)** — the premium leader: strongest in high-value strategy/consulting, biggest (~$73B rev,
  ~779k staff), historically best growth+margin+brand. Commands the premium multiple within the group.
- **The Indian majors — TCS, Infosys, HCLTech, Wipro** — the offshore-arbitrage champions. **Structurally the
  most profitable and capital-efficient** (TCS ROIC ~69%, Infosys ~42%, HCLTech ~36% [V, stockanalysis.com
  2026-07-02]) thanks to a higher offshore mix and asset-light model. Trade at premium multiples for that
  quality.
- **Cognizant & Capgemini** — the **"value" tier**: Western-listed, Western-heavy client bases, mid-teens
  margins/returns (CTSH ROIC ~15%). Cheaper multiples reflect lower structural returns than the Indian pure-plays.

**So CTSH is a large-cap "value player":** bigger by revenue than Infosys, Wipro, HCLTech, and Capgemini;
smaller than Accenture and TCS. It has historically **lagged Accenture/TCS on growth and margin**, which is
exactly why it trades cheapest of the peer set (see §6).

**Moat = narrow [A]** (consistent with `deep_dive.md §3`):
- **Switching costs** — CTSH is embedded in clients' core systems (a health insurer's claims platform, a bank's
  apps); ripping it out is expensive and risky. Multi-year contracts and deep domain knowledge (esp. Health
  Sciences via TriZetto) reinforce stickiness.
- **Scale & delivery footprint** — 350k trained engineers and global delivery centers are hard to replicate.
- **But: no pricing power.** IT services is competitive and commoditized at the low end — evidenced by **flat
  net income** (~$2.1–2.3B) since 2018 despite revenue rising $16B→$21B [V]. Margin/buyback, not pricing, drove
  EPS. Call it a **narrow moat**: durable relationships and scale, not a wide software-platform moat.

**Why it trades cheapest of the peer set** (full table in §6): (1) lower structural returns than the Indian
pure-plays; (2) US-listed + Western-client-heavy, so it got hit hardest in the **June-2026 sector-wide
"AI-deflation" de-rating** (down ~48% over 12 months, second only to Accenture's −55%); (3) a longer memory of
the pre-2023 underperformance. The value case is that the market is pricing (1)+(2)+(3) as *permanent* just as
the turnaround is proving (1) and (3) are improving.

---

# PART B — Deeper Diligence

## B4. Recent earnings prints (last 5 quarters) — EDGAR-tied

Source: Cognizant IR press releases (news.cognizant.com), each dated below; headline dollar figures and cc
growth **cross-checked to SEC EDGAR XBRL** (CIK 0001058290) in `data/verified_financials.md` (FY2025 10-K
filed 2026-02-12; Q1'26 10-Q filed 2026-04-29). All **[V]** unless noted.

| Quarter (reported) | Revenue | Organic **cc** growth | TTM bookings (YoY) / book-to-bill | Adj. op margin | Adj. EPS | Mega-deals (≥$500M) |
|---|---|---|---|---|---|---|
| **Q1 2025** (2025-04-30) | $5.115B | **+8.2%** | $26.7B (+3%) / ~1.3x | 15.5% | $1.23 | 0 |
| **Q2 2025** (2025-07-30) | $5.245B | **+7.2%** | $27.8B (+6%) / ~1.4x | 15.6% | $1.31 | 2 (>$1B TCV) |
| **Q3 2025** (2025-10-29) | $5.415B | **+6.5%** | $27.5B (+5%) / 1.3x | 16.0% | $1.39 | 0 |
| **Q4 2025** (2026-02-04) | $5.333B | **+3.8%** | (FY $28.4B) / ~1.3x | 16.0% | $1.35 | 2 |
| **Q1 2026** (2026-04-29) | $5.413B | **+3.9%** | **$29.6B (+11%)** / **~1.4x** | 15.6% | $1.40 | 1 |

> Q3'25 **GAAP** EPS was only $0.56 due to a ~$0.80 **one-time tax charge** — not a business deterioration;
> adjusted $1.39 is the clean number [V]. Q1'26 bookings **+21% YoY** in the quarter (the "best in 3 years"
> claim) drove TTM bookings to a record $29.6B [V].

**Full-year FY2025 (10-K) [V]:** revenue **$21.108B (+7.0% reported / +6.4% cc)**; GAAP operating margin
**16.1% (+140 bps)**; **GAAP EPS $4.56**, **adjusted EPS $5.28 (+11%)**; TTM bookings $28.4B (~1.3x
book-to-bill); FY buybacks $1.3B (17.4M sh), dividend raised to $0.33/qtr.

> **EPS reconciliation note:** `data/verified_financials.md` used a trailing EPS of ~$4.66 to get P/E ~8.9.
> The **FY2025 GAAP EPS is $4.56** and **adjusted is $5.28** [V]. At **$41.99** (2026-07-02), that's **P/E ~9.2
> on GAAP** and **~8.0 on adjusted** [A]. Either way, single-digit P/E — the deep-dive conclusion is unchanged;
> just note the trailing figure is $4.56 GAAP, not $4.66.

**Guidance — FY2026 (set at Q4'25, raised at Q1'26) [V]:**
- Revenue growth **4.0%–6.5% cc** (unchanged).
- Adjusted operating margin **16.0%–16.2%** (*raised* +20–40 bps from the initial 15.9–16.1%).
- Adjusted EPS **$5.63–$5.77** (*raised* to +7–9% YoY, from initial $5.56–$5.70).

**Segment trajectory to watch [V, cc YoY]:** the headline growth is masking a **rotation** —
- **Health Sciences (biggest segment)** decelerated hard: **+11.4% (Q1'25) → −0.9% (Q1'26)**. This is the single
  most important negative in the recent prints (§7).
- **Financial Services** re-accelerated to **+10.2% (Q1'26)**.
- **CMT** swung from −1.9% (Q1'25) to **+6.5% (Q1'26)** — the laggard is recovering.
- **Products & Resources** +1.1% (Q1'26), decelerating off tough comps.

**Read:** the top line held (guidance maintained *and* margin/EPS guide raised at Q1'26), **bookings hit a
record (+11% TTM / +21% in-quarter)** — a strong forward signal — but cc growth **decelerated to ~3.9%** in the
last two quarters and **Health Sciences turned negative**. So the "fundamentals are still growing" thesis is
intact at the aggregate/bookings level, but softer and more uneven under the hood than the Q1'26 bookings
headline alone suggests.

## B5. Valuation now vs. history

(Full tables in `deep_dive.md §2` and `data/verified_financials.md`; summarized and updated here.)

| Metric | Now (~$41.99, 2026-07-02) | 8-yr context |
|---|---|---|
| **P/E** | **~9.2 GAAP / ~8.0 adj** [A] | vs own ~17–18 median; 2022 trough 12.7 [V] |
| **EV/EBITDA** | **~4.8–5.0** [A/V] | vs ~10 median; below 2022 trough of 7.7 [V] |
| **FCF yield** | **~12.4–13%** [A/V] | FCF $2,595M FY25 [V] |
| **P/B** | **~1.3** [V] | vs ~2.5–3 historically [A] |
| **Dividend yield** | **~3.1%** [V] | growing dividend |

**The drawdown context [V, deep_dive.md §framing]:** CTSH ended 2025 at **$83** and trades **~$42 today —
down ~50% in ~6 months**, below its 2020 COVID trough and its 2022 rate-shock trough. The de-rating is real and
extreme *by its own standards*, and it is **sector-wide** (§6), triggered by the June-2026 "AI-deflation" panic
(Accenture's guidance cut on 2026-06-18 lit the fuse). CTSH now trades at **~half its own 8-year median
multiple** while its reported fundamentals are still growing — that gap is the value thesis.

## B6. Competitor & sector comparison

**As-of ~2026-07-02/03. Source: stockanalysis.com (S&P Global data), cross-checked with screener.in for the
Indian names [V, secondary].** Fiscal years differ (ACN: Aug; Indian IT: Mar; Capgemini & CTSH: Dec) — treat
cross-company comparisons as directional.

| Metric | **CTSH** | Accenture (ACN) | TCS (NSE) | Infosys (INFY) | Wipro (WIT) | HCLTech | Capgemini (CAP) |
|---|---|---|---|---|---|---|---|
| Price | $41.99 | $137.35 | ₹2,093 | $11.16 | $1.89 | ₹1,139 | €91.90 |
| Market cap | ~$19.9B | ~$84B | ~$85B | ~$44.5B | ~$19.4B | ~$35B | ~€15.6B |
| **P/E (TTM)** | **9.1** | 11.0 | 15.2 | 13.4 | 13.8 | 17.6 | 10.1 |
| Forward P/E | 7.3 | 9.6 | 13.3 | 13.5 | 13.3 | 15.8 | 7.0 |
| **EV/EBITDA** | **5.0** | 6.4 | 10.0 | 9.5 | 8.7 | 10.0 | 7.0 |
| **P/B** | **1.32** | 2.64 | 6.89 | 4.52 | 2.05 | 4.14 | 1.34 |
| **FCF yield** | **12.4%** | 15.0% | 6.4% | 8.4% | 7.2% | 6.4% | 14.1% |
| TTM rev growth | +6.5% | +6.7% | +4.6% | +4.6% | +4.0% | +6.0% | +1.7% |
| Operating margin | 15.8% | 15.8% | **25.0%** | 20.3% | 16.2% | 17.2% | 11.2% |
| **ROIC** | **15.0%** | 27.1% | **68.6%** | 41.9% | 21.4% | 35.6% | 10.3% |
| ROE | 14.9% | 24.4% | 48.4% | 31.4% | 15.4% | 23.4% | 13.7% |
| Dividend yield | 3.1% | 4.8% | 5.3%⚠ | 4.0% | 5.8% | 5.0% | 3.7% |
| Buyback yield | **2.4%** | ~1.5% | n/a⚠ | 0.8% | ~0 | ~0 | ~0.6% |
| Total shareholder yld | 5.5% | 6.3% | n/a⚠ | ~4.8% | 5.7% | 5.3% | 4.3% |
| **12-mo price change** | **−48%** | **−55%** | −39% | −41% | −38% | −34% | −37% |

⚠ TCS dividend yield conflicts across sources (5.3% stockanalysis vs 3.06% screener.in — likely
special-dividend/timing); TCS buyback yield not surfaced [U]. CTSH operating margin: one source page showed an
anomalous ~4% TTM figure (likely a one-off-charge/parse artifact) — defer to our EDGAR-verified ~16% [V].

**Scale & mix [V, secondary]:** ACN ~$73B rev / ~779k staff (biggest); TCS ~$32B / ~584k; **CTSH ~$21B / ~352k**;
Infosys ~$20B / ~329k; HCLTech ~$14.7B / ~226k; Capgemini ~€22.5B / ~423k; Wipro ~$9.9B / ~240k. CTSH is a genuine
large-cap — **bigger by revenue than Infosys, Wipro, HCLTech, Capgemini; behind ACN and TCS.**

**What the table says:**
1. **CTSH is the cheapest on every valuation line** — lowest P/E, lowest EV/EBITDA, lowest P/B (tied with
   Capgemini), while posting **top-of-pack revenue growth (+6.5%, ~tied with ACN)**. That combination — cheapest
   multiple *and* fastest growth — is the crux of the value case.
2. **You pay for that cheapness with lower structural quality.** CTSH's **ROIC ~15% and margin ~16% are the
   lowest in the group alongside Capgemini.** The Indian pure-plays are in a different league on capital
   efficiency (TCS ROIC ~69%, Infosys ~42%, HCLTech ~36%) because of their higher offshore mix and asset-light
   models. **CTSH is cheap partly for a reason** — it's a mid-teens-return business, not a 40%+ ROIC one.
3. **It returns cash aggressively** — highest buyback yield in the group (2.4%) and a 5.5% total shareholder
   yield, vs the Indian names that lean almost entirely on dividends.
4. **The selloff is sector-wide** — everyone is down 34–55% over 12 months. ACN (−55%) and CTSH (−48%) fell
   hardest (US-listed integrators, most exposed to the "AI kills services" narrative); the Indian names and
   Capgemini fell less. **This confirms CTSH's drawdown is a sector re-rating, not a company-specific blowup.**

### Reconciling the deep-dives' **CTSH > TCS** conclusion
TCS is the "finalist sibling." Comparing them directly:
- **Valuation:** CTSH P/E **9.1 vs TCS 15.2** (~40% cheaper on P/E, ~½ if you use adjusted EPS); **P/B 1.32 vs
  6.89** (~**1/5** the price-to-book); **EV/EBITDA 5.0 vs 10.0** (half). CTSH is dramatically cheaper on every
  multiple [V]. This confirms the deep-dives' "half the P/E, ~1/5 the P/B" framing.
- **Quality:** TCS wins decisively — **ROIC ~69% vs ~15%, operating margin 25% vs 16%.** TCS is the higher-
  quality business, full stop.
- **Growth inflection:** **CTSH +6.5% vs TCS +4.6% TTM** — CTSH's turnaround has it growing *faster* than TCS
  right now, and CTSH's revenue re-inflected (five quarters of ~6–8% cc) while TCS decelerated and announced
  10,000+ AI-driven layoffs (Aug-2025) [V]. So the growth *trend* favors CTSH even though the *level* of
  quality favors TCS.
- **The trade:** CTSH > TCS is a **valuation call, not a quality call** — you're paying half-to-a-fifth the
  multiple for a business that is currently growing faster, accepting materially lower structural returns and a
  narrower moat. It only works if the multiple gap is *sentiment* (the AI de-rating hit US names harder) rather
  than a *permanent* quality discount. If AI deflation is real, TCS's higher offshore efficiency may weather it
  better; if it's overdone, CTSH's cheaper multiple + faster growth re-rates more. **The deep-dives' CTSH > TCS
  preference is defensible on price and growth-trend, but it is explicitly buying the cheaper, lower-quality
  name — size accordingly.**

**Where CTSH is cheap vs the group and why:** cheapest multiples in a cohort that is *already* cheap post-selloff,
because it combines (a) the lowest structural returns of the arbitrage majors, (b) the hardest US-listed hit in
the AI-deflation de-rating, and (c) a pre-2023 underperformance memory — against which the offset is a genuine,
verified turnaround (growth re-inflected, margins up, record bookings) that the multiple isn't yet crediting.

## B7. What to watch (diligence checklist)

Ranked by importance:

1. **The AI-on-IT-services question — DEFER to the theme agent** (`deep_dive.md §4a` for the full bull/bear).
   In one line: does GenAI productivity flow to clients as *fewer billable hours* (revenue deflation) or does
   "AI needs integrators" expand CTSH's addressable spend? CTSH is itself moving to **token/outcome-based
   pricing** and running **Project Leap** (AI-driven headcount realignment) — consistent with a model in
   transition. Unresolved; the whole thesis hinges on it. **Do not treat this section as the AI deep-dive.**
2. **Bookings / book-to-bill trend.** The cleanest forward signal. **TTM bookings $29.6B (+11%), book-to-bill
   ~1.4x at Q1'26** [V] — record and rising. If book-to-bill holds ≥1.3x and TTM bookings keep growing, demand
   is not being gutted *yet*. A drop below ~1.2x would be the first hard sign the AI-deflation bear is arriving.
3. **Health Sciences vertical health (~30% of revenue).** It **turned −0.9% cc in Q1'26** after +11% a year
   earlier [V]. This is CTSH's biggest and highest-value segment (TriZetto/claims/pharma). Whether that's a
   comp/timing dip or a real slowdown in its most important vertical is a top thing to track next print.
4. **Margin trajectory under Project Leap.** FY2026 adjusted-OM guide **raised to 16.0–16.2%** [V]; the
   restructuring is designed to fund margin. Watch that the ~$200–300M in-year savings show up without the
   revenue base eroding faster (the deflation risk is that cuts are cost-driven, not efficiency-reinvested).
5. **Discretionary-spend recovery among Western clients.** Soft enterprise discretionary spend + higher-for-
   longer US rates delayed projects sector-wide (a driver of ACN's June guidance cut). Cyclical, not structural,
   but it caps near-term growth. CMT's recovery (+6.5% Q1'26) is an early positive tell.
6. **H-1B / visa cost & legal status.** 73% of staff in India; US on-site delivery leans on H-1B/L-1. A
   **$100,000 H-1B fee (new petitions only, eff. 2025-09-21)** raises the cost of the visa-dependent model and
   accelerates India-GCC (captive) competition [U — and a reported June-2026 court strike-down of the fee is
   **UNVERIFIED**; confirm on the primary docket before relying on it]. CTSH is among the largest H-1B
   sponsors, so exposure is high; it has been localizing US hiring for years.
7. **Client concentration.** The FY2025 10-K excerpt pulled did not disclose a hard top-client %; **not
   independently verified** [U]. Flag for follow-up if this advances to sizing.

---

## Summary of corrections applied to prior CTSH notes (for the record)
- **FY2025 EPS:** GAAP **$4.56** / adjusted **$5.28** (prior note used ~$4.66 trailing) → P/E ~9.2 GAAP / ~8.0 adj.
- **Buybacks:** low-single-digit %/yr float shrink (~2.5%/yr over 7 yrs), **not ~10%/yr** as `deep_dive.md`
  stated; $13.5B authorization, $1.92B remaining at Dec-2025.
- **NextGen charge:** **$363M** (not ~$400M).
- **Project Leap:** savings are **in-year 2026** (~$200–300M), not "by 2027"; severance is top of a $200–270M
  range; the **12–15k India layoff count is media, not company-disclosed**.
- **Humphries departure:** board-driven / "without cause" per 8-K (media framing = "fired for underperformance").

## Sources (new to this file; §B4/B6 primary + secondary)
- Cognizant IR quarterly releases (primary): Q1'25 https://news.cognizant.com/2025-04-30-Cognizant-Reports-First-Quarter-2025-Results · Q2'25 …2025-07-30… · Q3'25 …2025-10-29… · Q4/FY'25 …2026-02-04… · Q1'26 https://news.cognizant.com/2026-04-29-Cognizant-Reports-First-Quarter-2026-Results [V]
- Ravi Kumar appointment (2023-01-12): https://news.cognizant.com/2023-01-12-Cognizant-Appoints-Ravi-Kumar-S-as-Chief-Executive-Officer [V]
- Jatin Dalal CFO (2023-09-28): https://news.cognizant.com/2023-09-28-Cognizant-Appoints-Jatin-Dalal-as-Chief-Financial-Officer [V]
- Humphries replacement 8-K (2023-01): https://www.sec.gov/Archives/edgar/data/1058290/000105829023000008/ctsh-20230109.htm [V]
- Board chair Rohleder: https://www.cognizant.com/us/en/about-cognizant/corporate-governance/board-of-directors/stephen-j-rohleder [V]
- FY2025 10-K (buybacks, dividend, Belcan, segments): https://www.sec.gov/Archives/edgar/data/1058290/000105829026000008/ctsh-20251231.htm [V]
- FY2024 10-K (NextGen $363M charge, Note 4): https://www.sec.gov/Archives/edgar/data/1058290/000105829025000017/ctsh-20241231.htm [V]
- Q1'26 10-Q / 8-K (Project Leap): https://www.sec.gov/Archives/edgar/data/1058290/000105829026000016/ctsh-20260331.htm [V]
- Thirdera close (2024-01): https://news.cognizant.com/cognizant-thirdera-acquisition-complete [V]
- Peer comparison metrics (as-of 2026-07-02/03): stockanalysis.com statistics pages for ACN/TCS/INFY/WIT/HCLTECH/CAP/CTSH; screener.in for Indian fundamentals [V, secondary]
- Attrition history: SEC earnings exhibits (2022) — e.g. https://www.sec.gov/Archives/edgar/data/1058290/000105829022000320/exhibit9939302022.htm [V]
