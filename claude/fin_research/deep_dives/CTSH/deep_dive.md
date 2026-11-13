# Deep Dive: CTSH — Cognizant Technology Solutions

**Stage 4 value-investing deep dive.** Prepared 2026-07-02 by Claude (Opus 4.8) for Hooman Shariati.
Price basis: **$41.66** (Yahoo Finance chart API, 2026-07-02). All financials cross-checked to SEC EDGAR
XBRL (CIK 0001058290): latest **10-K FY2025** (filed 2026-02-12) and **10-Q Q1 2026** (ended 2026-03-31,
filed 2026-04-29). Raw pull + tables in `data/verified_financials.md` and `data/companyfacts.json`.

Confidence tags: **[V]** verified from primary filing / reliable source · **[A]** assumed/derived by me ·
**[U]** unverified / single-source.

---

## ⚠️ Framing correction vs. the screen
The screen tagged CTSH as a cheap name in an AI-sentiment-overhung sector. **That is right, but understates
the drama.** CTSH ended 2025 at **$83** and trades at **~$41.66 today — down ~50% in ~6 months** [V, Yahoo
year-end $83.00; current $41.66]. This is not a quietly-cheap screen artifact; it is a **violent, recent,
sector-wide de-rating**. The stock is now cheaper than its own 2020 COVID trough and its 2022 rate-shock
trough. Whether that is opportunity or a market correctly pricing a broken model is the entire question here.

---

## 1. Business & thesis

Cognizant is a global IT-services / digital-consulting firm — application development & maintenance, cloud &
digital engineering, BPO, and industry consulting — with **FY2025 revenue $21.1B** [V, 10-K] across four
segments (Health Sciences, Financial Services, Products & Resources, Communications/Media/Tech). Its economic
engine is the classic **labor-arbitrage model**: ~**352k employees, 257k (73%) in India** [V, 10-K], billing
mostly Western clients (majority North America) at a spread over offshore cost.

**Value thesis:** CTSH is a high-return, cash-generative, net-cash market leader now trading at **EV/EBITDA
4.8 / P/E 8.9 / FCF yield ~13%** [A, computed from V inputs] — roughly **half its own 8-year median EV/EBITDA
(~10)** [A] — because a June-2026 industry-wide "AI will hollow out IT services" panic (triggered by
Accenture's guidance cut) crushed the whole sector. Meanwhile CTSH's *own* fundamentals are still growing:
**Q1 2026 revenue +5.8% YoY, bookings +21% YoY, guidance maintained** [V, Q1 press release]. So the setup is
"the sentiment collapsed faster than the fundamentals."

**Cheap-cyclical or cheap-broken?** **Cheap-with-a-real-structural-question.** It is not a broken balance sheet
or a company in decline (revenue and bookings are up). But the bear case is not mere sentiment either — the
labor-arbitrage model faces a genuine, unresolved GenAI-deflation threat. So: **cheap-cyclical/sentiment on the
surface, with a live secular-disruption tail risk underneath.** That tension drives the verdict below.

---

## 2. Valuation

### Current multiples (price $41.66, 2026-07-02) [A, from V inputs]
| Metric | Value | Basis |
|---|---|---|
| Market cap | ~$19.7B | 474M sh (Q1'26) × $41.66 [V sh count] |
| Net cash | +$0.98B | cash 1,504 + STI 13 − LT debt 535 (Q1'26) [V] |
| Enterprise value | ~$18.8B | mktcap − net cash |
| EV/EBITDA | **4.8x** | EBITDA $3,939M FY25 (op 3,389 + D&A 550) [V] |
| P/E (trailing) | **8.9x** | NI $2,230M FY25 [V] |
| FCF yield | **13.1%** | FCF $2,595M FY25 (OCF 2,883 − capex 288) [V] |
| P/B | **1.31x** | equity $15,068M Q1'26 [V] |
| Dividend yield | ~3.1% | dividends $610M FY25 [V] |

**Screen check:** the snapshot (EV/EBITDA 4.9, P/E 8.9, P/B 1.29) is **CONFIRMED** at today's price [V]. One
nuance: the screen's "earnings yield 17.5%" is richer than trailing NI/mktcap (11.3%) or FCF yield (13.1%) —
it looks like an operating-earnings/EV-based or forward figure. **Corrected read: trailing earnings yield
~11%, FCF yield ~13%** [A]. Still cheap, just not 17.5% on a clean trailing-NI basis.

### Vs. its own history [A, computed from V price+financials]
| Year-end | Price | EV/EBITDA | P/E |
|---|---|---|---|
| 2018 | $63 | 9.7 | 17.5 |
| 2020 | $82 | 15.4 | 31.8 |
| 2021 | $89 | 13.1 | 21.8 |
| 2022 (rate trough) | $57 | 7.7 | 12.7 |
| 2024 | $77 | 10.7 | 17.0 |
| 2025 | $83 | 9.8 | 17.8 |
| **Now** | **$42** | **4.8** | **8.9** |

CTSH now trades **below its 2022 trough and roughly half its 8-year median.** The de-rating is real and
extreme by its own standards.

### Vs. peers (as of 2026-07-02, stockanalysis.com) [V, secondary]
| Company | Price | P/E | EV/EBITDA | P/B | Div yld | TTM rev growth | 12-mo price |
|---|---|---|---|---|---|---|---|
| **CTSH** | $41.61 | **9.05** | **4.89** | **1.29** | 3.2% | +6.5% | **−47.6%** |
| Accenture (ACN) | $134.85 | 10.5 | 6.25 | 2.52 | 4.8% | +6.7% | −55.3% |
| Infosys (INFY) | ₹1,043 | 13.1 | 8.58 | 4.32 | 5.0% | ~+4.6% | −35.1% |
| TCS | ₹2,071 | 14.6 | 9.53 | 6.60 | 5.6% | ~+4.6% | −39.6% |
| Wipro | ₹174 | 13.8 | 8.34 | 2.05 | 6.3% | ~+4.0% | −34.2% |
| *IBM (ref)* | $289 | 25.4 | 19.9 | 8.16 | 2.3% | +9.7% | −1.2% |

**Read:** the *entire* sector is down 34–55% over 12 months — this is **sector-wide, not CTSH-specific**. But
within the group **CTSH is the cheapest on every metric** (lowest P/E, EV/EBITDA, P/B), while still posting
the *fastest* revenue growth alongside ACN (+6.5%). The Indian majors carry higher multiples (asset-light,
higher ROE/payout). IBM is the outlier that did NOT de-rate — the market treats it as an AI/software winner,
not a labor-arbitrage name. So CTSH sits at the value end of an already-cheap cohort.

### Rough fair-value / expected-return sketch [A — illustrative, not a target]
- **FCF/owner-earnings basis:** ~$2.6B FCF on $19.7B mktcap = **13% FCF yield**. Even with *zero* growth,
  buying a market-leader FCF stream at 13% and returning it via buybacks+dividends (FY25 returned
  $1.99B = ~10% of cap) is a high-single-digit/low-double-digit base return before any re-rate [A].
- **Re-rate scenario:** if fears prove overdone and it re-rates to just its 2022 *trough* of EV/EBITDA 7.7
  (still well below median), that's ~$18.8B→$30B EV, roughly **+55–60% equity upside** on flat EBITDA [A].
  A return to the ~10x median implies a near-double.
- **Bear scenario:** if AI deflation is real, EBITDA erodes and the multiple stays ~5x → the stock is roughly
  fairly-to-cheaply valued and you clip the ~13% FCF yield while it shrinks. Downside is more "dead money +
  modest income" than "−50%," given the net-cash balance sheet and buyback support [A].
- **Asymmetry:** skewed favorably — but only if the model isn't structurally broken. That is the whole bet.

**Genuinely cheap, not an optical trap on the numbers.** The trap risk is *fundamental* (AI), not *accounting*.

---

## 3. Quality

- **Returns:** FY2025 **ROE ~15.2%** (NI/avg equity) [A]; **ROIC ~18%** (NOPAT@25% tax / (equity+debt−cash))
  [A] — confirms the screen's ~18% ROIC. Consistently high-teens returns; asset-light. Piotroski 7/7 per
  screen [U, screen].
- **Margins:** FY2025 **operating margin 16.1%, net margin 10.6%** [V]. Operating margin *expanded* in 2025
  (from ~14.7% in 2024) and Q1'26 adjusted OM guidance was *raised* to 16.0–16.2% [V, Q1 release] — margins
  going the right way, aided by "Project Leap" restructuring.
- **FCF conversion:** **116% of net income in FY2025** [V]; consistently >90% historically. Clean earnings.
- **Balance sheet:** **net cash +$0.98B** (Q1'26) [V], minimal debt ($535M). Fortress balance sheet — removes
  bankruptcy/solvency risk from the value-trap checklist.
- **Capital returns:** steady. Share count **578M (2018) → 474M (Q1'26)**, ~18% reduction [V]. FY2025 returned
  **$1.38B buybacks + $0.61B dividends = ~$2.0B (~10% of current cap)** [V]. Dividend growing (~$610M FY25).
- **Growth quality:** revenue CAGR is modest (~4%/yr 2018–2025: $16.1B→$21.1B) [A] — this is a low-growth
  compounder, not a grower. Net income has been *flat* (~$2.1–2.3B) since 2018 despite revenue growth — margin
  and buyback have driven EPS more than profit growth [V]. That flatness is a fair knock on quality.

**Moat assessment — narrow.** Switching costs (embedded in client systems/workflows), scale, domain
expertise, and long-term contracts give real stickiness — but IT services is competitive and largely
commoditized at the low end, with no pricing power (evidenced by flat net income on rising revenue). Call it a
**narrow moat**: durable client relationships and scale, but not a wide, pricing-power moat like a software
platform. The AI thesis directly attacks the labor-arbitrage core of that moat (§4).

---

## 4. The bear case / key risks

This is the crux. CTSH is cheap *because* of a credible bear thesis, not in spite of one.

### (a) AI disruption of IT services — the central risk [balanced, both sides evidenced]
**Bear (AI compresses the model) [V/U]:**
- Productivity uplift flows to clients: GitHub Copilot study showed devs **55% faster** [U, github.blog];
  McKinsey found GenAI cut common dev tasks ~33–50% [U, 2023-06]; Infosys migrated 3M lines of Hertz COBOL at
  **60% lower cost / 60% faster** [U, Forbes 2026-06-10]. In a per-FTE/T&M model, client productivity =
  **fewer billable hours = revenue deflation** unless volume grows.
- **CEOs now say "deflation" out loud.** HCLTech CEO expects **AI deflation to cut revenue 3–5%**; TCS CEO
  called it "degrowth"; Infosys expects "deflation to become a factor" [U, The Register 2026-04-28]. Analyst
  estimates of revenue-at-risk span **~2–16%** (HCLTech 2–3%, Motilal Oswal 9–12%, HSBC 14–16%) [U,
  Moneycontrol/Business Today 2026]. JPMorgan frames a multi-year "AI deflation" cycle [U, Business Today
  2026-07-01].
- **Cognizant is itself pivoting to token/outcome-based pricing** — CEO Ravi Kumar: *"Token metering is now a
  reality for projects, both fixed-price and T&M"* [V, CRN Apr 2026]. Per Nearshore Americas, **40–50% of new
  2025 outsourcing deals include AI-efficiency pass-through clauses** [U]. The deflation mechanism is showing
  up in CTSH's own contract structure.
- **Headcount decoupled from revenue** — the clearest hard signal. Indian big-four had net FY24 headcount
  *declines* (Wipro −24.5k, Infosys −26k, TCS −13k) with rising margins; TCS announced **10,000+ layoffs**
  (Aug 2025) citing AI-driven workforce realignment [V, The Register]. CTSH's **"Project Leap"** targets **up
  to 12,000–15,000 job cuts in 2026 (mostly India)**, ~$270M severance, **$200–300M savings** by 2027, ~⅓
  reinvested in upskilling [V, CRN Apr 2026]. Great for near-term EPS; consistent with the bear view that the
  *growth engine* (headcount-led arbitrage) is structurally impaired.
- Client insourcing + hyperscaler automation attack the core: India **GCCs (captives) added ~2x the net staff
  of IT-services firms in FY26**; AWS Transform processed >1.1B lines of code / saved >810k hours; autonomous
  coding agents (Cognition's Devin at Fiserv) emerging [U, Forbes/TechRepublic/TechCrunch 2026].

**Bull (AI is a net services opportunity) [V/U]:**
- **GenAI bookings are large and growing — the cleanest hard numbers:** Accenture FY25 GenAI **new bookings
  ~doubled to $5.9B, revenue tripled to $2.7B** on 6,000 projects [U, CRN 2025-09]. IBM's GenAI "book of
  business" grew **>$2B → >$12.5B over six quarters, ~80% consulting/services** [U, The Register 2026-01]. For
  CTSH: **5,000+ active AI engagements, ~40% of code AI-assisted, ~30% AI-generated revenue in key accounts**
  [V, CRN Apr 2026]. Clients pay integrators to *deploy* GenAI.
- **"AI needs services":** only **~14% of enterprises have a clear AI strategy** [U, HFS/Genpact 2025-04]; ROI
  depends on messy data estates, integration, governance — exactly what integrators sell. Gartner forecasts
  worldwide **IT-services spend $1.87T (+9.0%) in 2026** [U, Business Wire 2026-04].
- Cognizant CEO frames AI as a **"net-new tailwind... an increase in our total addressable spend"** [U/V, CRN].
- **Historical base rate:** Y2K, cloud (2010s), RPA (late 2010s) were each feared to gut headcount-led
  services; the leaders adapted, moved up-stack, and grew [U, Forbes/diginomica 2026]. Wedbush upgraded CTSH to
  Outperform in June 2026 calling the selloff overdone [U].
- **CTSH's own numbers so far contradict the collapse:** Q1'26 revenue **+5.8%**, bookings **+21%** (best in 3
  years), TTM bookings **$29.6B, 1.4x book-to-bill**, one >$500M mega-deal, **guidance maintained**, margin
  guidance *raised* [V, Q1'26 release]. If AI were already gutting demand, this is not what it would look like.

**Net:** genuinely unresolved. The market has priced a fairly severe deflation outcome (EV/EBITDA 4.8, below
COVID and 2022 troughs). The reported fundamentals do not (yet) confirm that outcome. This is the debate you'd
be taking a side on.

### (b) Growth stagnation [V] — real. Net income has been ~flat ($2.1–2.3B) since 2018 despite revenue rising
$16→$21B. EPS growth has leaned on buybacks and margin, not profit growth. Even absent AI, this is a slow
compounder — the bull return relies on the *multiple*, not the earnings engine.

### (c) Visa / immigration exposure [V] — material and a live 2025-26 risk. 73% of staff in India; US on-site
delivery leans on H-1B/L-1. Cognizant is named among the **largest H-1B sponsors** (with TCS, Infosys) that
"bear the brunt" of new fees [U]. The Trump administration imposed a **$100,000 H-1B fee effective 2025-09-21,
applying only to NEW petitions** (not renewals/existing holders, per USCIS) [U, Business Insider/colorado.edu].
A proposed ~30% prevailing-wage hike could further accelerate India GCC growth [U]. This raises the cost of the
visa-dependent delivery model and pressures margin or forces more local hiring. CTSH has been localizing US
hiring for years, but exposure is among the highest in the group. **Note:** a reported June-2026 federal court
strike-down of the fee surfaced only via aggregator and is **UNVERIFIED** — confirm on the primary docket
before relying on it.

### (d) Client concentration [U] — the FY2025 10-K excerpt I pulled did not disclose a hard top-client %
(states revenue is "distributed among a number of clients"). Historically CTSH's top-10 clients are a
meaningful but not dangerous share; **not independently verified here** — flag for follow-up if this advances.

### (e) Discretionary-spend / macro [U] — soft enterprise discretionary spending + higher-for-longer US rates
are delaying client projects sector-wide (a key driver of ACN's June guidance cut). Cyclical, not structural,
but weighs near-term.

---

## 5. Catalysts & verdict

### What re-rates it
1. **Fundamentals keep holding** — 2–3 more quarters of the Q1'26 pattern (mid-single-digit growth, strong
   bookings, held/raised guidance) would directly refute the "AI is gutting demand *now*" thesis and force a
   re-rate off trough multiples. **This is the primary catalyst** [A].
2. **AI reframed as a tailwind** — visible acceleration in GenAI bookings converting to revenue; management
   quantifying AI as net-positive to growth.
3. **Sentiment mean-reversion** — the sector fell on one guidance cut (ACN, June 18); a single sector-wide
   "beat + AI-is-a-tailwind" print could reverse the herd. Analyst sentiment is already split (Wedbush upgrade,
   Citi raise vs. Morgan Stanley/Daiwa cuts).
4. **Capital returns** — buying back ~10% of the cap/yr at a 13% FCF yield is a self-help re-rate lever.

### Scorecard (0–10; weights from CLAUDE.md §3: Cheapness 30 / Quality 30 / Trap-risk-inverse 20 / Moat 15 / Catalyst 5)
| Dimension | Weight | Score | Weighted | Rationale |
|---|---|---|---|---|
| **Cheapness** | 30% | **9** | 2.70 | EV/EBITDA 4.8 / P/E 8.9 / FCF yld 13% — half its own median, below 2022 trough, cheapest of peers. Genuinely cheap. [V/A] |
| **Quality** | 30% | **7** | 2.10 | ROIC ~18%, ROE ~15%, 116% FCF conversion, net cash, disciplined buybacks — high. Docked for flat net income since 2018 / low growth. [V] |
| **Trap-risk (inverse)** | 20% | **5** | 1.00 | Balance sheet & accounting clean (low trap), BUT genuine unresolved AI-deflation secular risk keeps this only mid. [A] |
| **Moat & leadership** | 15% | **6** | 0.90 | Narrow moat: switching costs, scale, sticky contracts; no pricing power (flat profit); AI attacks the arbitrage core. Competent mgmt (Ravi Kumar, margin discipline). [A] |
| **Catalyst** | 5% | **6** | 0.30 | Clear near-term catalysts (earnings prints, bookings, buyback) but timing/sentiment-dependent. [A] |
| **TOTAL** | 100% | | **7.00 / 10** | |

*(Screen scored 76.7/100 ≈ 7.7; my 7.0 is a touch lower, docking growth stagnation and the live secular AI risk after diligence.)*

### Verdict: **WATCH → tilt toward BUY-worth-more-work**

CTSH is **genuinely, verifiably cheap** — not an accounting/balance-sheet trap. It's a net-cash, ~18%-ROIC,
13%-FCF-yield market leader trading below its COVID and rate-shock troughs, cheapest of an already-cheap peer
group, while its *own reported fundamentals are still growing* (Q1'26 revenue +5.8%, bookings +21%, guidance
held). The bear case is real but, so far, **not confirmed by the company's own numbers** — the market has
priced a severe AI-deflation outcome that hasn't yet shown up in results. The asymmetry favors the buyer: a
re-rate to even the 2022 trough is ~+55%, while the net-cash sheet and buyback cap the downside to "modest
income on a shrinking base" rather than a wipeout.

I stop short of a clean BUY because the **single most important risk — structural GenAI deflation of the
labor-arbitrage model — is genuinely unresolved**, and the growth engine has been flat for years even before
AI. This is a "high-conviction cheap, medium-conviction thesis" name: **worth advancing to a position-sizing /
final-conviction stage**, ideally after (a) one more earnings print to confirm the fundamentals are holding,
and (b) verifying client concentration and the current H-1B fee status. Size it as a value bet on a real but
bounded secular risk, not as a safe compounder.

---

## Appendix — source list
- SEC EDGAR XBRL companyfacts, CIK 0001058290 (FY2025 10-K, Q1 2026 10-Q): https://data.sec.gov/api/xbrl/companyfacts/CIK0001058290.json [V primary]
- FY2025 10-K document: https://www.sec.gov/Archives/edgar/data/1058290/000105829026000008/ctsh-20251231.htm [V primary]
- Yahoo Finance chart API (prices, 2026-07-02) [V]
- stockanalysis.com — CTSH/ACN/INFY/TCS/WIPRO/IBM statistics & financials, as-of 2026-07-02 [V secondary]
- Cognizant Q1 2026 results (2026-04-29): https://news.cognizant.com/2026-04-29-Cognizant-Reports-First-Quarter-2026-Results [V]
- Motley Fool, IT-services selloff (2026-06-21): https://www.fool.com/investing/2026/06/21/wall-street-just-sold-off-these-it-services-stocks/ [U secondary]
- Morgan Stanley PT cut $63→$44 (2026-06-23): https://www.insidermonkey.com/blog/morgan-stanley-cuts-price-target-on-cognizant-technology-solutions-ctsh-here-is-why-1790102/ [U]
- Daiwa cut / $40.56 52-wk low (2026-06-25): https://www.marketbeat.com/instant-alerts/cognizant-technology-solutions-nasdaqctsh-reaches-new-52-week-low-after-analyst-downgrade-2026-06-25/ [U]
- Business Today, "AI deflation" / IT worst year since 2008 (2026-07-01): https://www.businesstoday.in/markets/stocks/story/it-stocks-set-for-worst-performance-in-18-years-brokerages-and-analysts-share-outlook-540233-2026-07-01 [U]
- McKinsey, economic potential of generative AI: https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier [U]
- The Register, "AI deflation" — IT-services CEOs (2026-04-28): https://www.theregister.com/software/2026/04/28/ [U]
- The Register, TCS 10,000+ layoffs (2025-08-11): https://www.theregister.com/on-prem/2025/08/11/ [V secondary]
- CRN, Cognizant Project Leap $270M / token pricing (Apr 2026): https://www.crn.com/news/ai/2026/cognizant-s-project-leap-270m-plan [V secondary]
- CRN, Accenture FY25 GenAI bookings $5.9B (2025-09): https://www.crn.com/news/ai/2025/ [U]
- The Register, IBM GenAI book of business >$12.5B (2026-01-29): https://www.theregister.com/2026/01/29/ibm_q4_2025/ [U]
- Forbes, AWS Transform / Infosys COBOL (2026-06-10): https://www.forbes.com/sites/janakirammsv/ [U]
- Everest Group / HFS Research (AI services demand, 2025): https://www.everestgrp.com/ , https://www.hfsresearch.com/ [U]
- H-1B $100k fee (new petitions only, eff. 2025-09-21): White House proclamation + Business Insider / colorado.edu/isss coverage [U — June-2026 court strike-down UNVERIFIED, reconfirm]

**Verification caveats:** analyst PT cuts and AI-thesis commentary are largely single-source/secondary [U];
GenAI-bookings figures come from company disclosure/coverage, not always the primary transcript; a claimed
Nasdaq-100 removal was NOT verifiable and is excluded. Client concentration % not verified. All core financials
(revenue, income, cash flow, balance sheet, share count) are [V] from SEC XBRL.
