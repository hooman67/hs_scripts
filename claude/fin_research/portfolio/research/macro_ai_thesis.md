# AI Investment Thesis — Evidence Review & Verdict

**For:** Hooman Shariati (Canadian citizen; quality-first value investor; self-described poor stock-picker; large involuntary US-tech exposure via ~$732k Adobe RSUs).
**Author:** Claude (Opus 4.8), technology-sector analyst.
**Date:** 2026-07-07. **Prices:** market close 2026-07-06 unless noted.
**Method:** 6 parallel research agents, web-sourced. Every number tagged VERIFIED (source + date) / ASSUMED (single news snippet) / UNVERIFIED. This is research to inform your decisions — **not financial advice, no trades.**

> **⚠️ Sourcing honesty.** Live keyword web-search was largely unavailable this session; agents leaned on `stockanalysis.com` (prices/multiples), primary earnings releases where reachable (Alphabet Q1'26, Microsoft blog, Nvidia IR), and Wikipedia for the AI-bubble/deal chronology. Deal figures still under negotiation and macro claims (Morgan Stanley $3T, MIT 95%, Cisco peak P/E) are **single-sourced** — flagged inline. Re-pull from primary IR/10-Q before any of these drive a real trade.

---

## TL;DR — Scorecard on Your 5 Sub-Theses

| # | Your thesis | Correct? (1–10) | One-line verdict |
|---|---|:--:|---|
| 1 | AI bubble will burst, but AI is real like the internet; winners emerge | **7** | Right in spirit. But it's not one uniform bubble — the froth is concentrated (Tesla/AMD/Palantir + loss-making OpenAI + circular financing), while mega-cap compute owners earn real profits at ~18–29x forward. "Bubble" is half-true. |
| 2 | Amazon & Google are the winners; Google genuinely good; Amazon owns stakes in Anthropic AND OpenAI | **6** | Google thesis is strong and well-supported. Amazon–Anthropic (~$8B, minority) is **VERIFIED**. **Amazon owns NO OpenAI equity — that part is wrong.** The Amazon–OpenAI tie is a $38B AWS *compute contract*, not a stake. |
| 3 | Less bullish on MSFT/Meta; most bearish OpenAI; OpenAI could spike on a govt bailout | **5** | MSFT/Meta lower-conviction is *understandable* but arguably overshoots — both are cheaper than GOOGL/AMZN on forward P/E with intact fundamentals. OpenAI bearishness is well-founded (deeply loss-making). "Government bailout probable" is **UNVERIFIED speculation** — no evidence; don't bank on it. |
| 4 | Foundation models commoditize / flooded with cheap open-source; winners in app + infra layers | **8** | The best-supported of your five. Mid-tier models *are* commoditizing (cost −10x/yr; open weights ~6–12mo behind). Enterprise dollars crossed to majority app-layer in 2025. **Caveat:** the *frontier* premium has NOT collapsed (test-time compute keeps re-opening a lead). |
| 5 | Energy = indirect AI bet (avoids picking AI winners) | **4** | Half-right, half-confused. **Broad "energy" (oil & gas / XLE) does NOT capture AI upside** — it's crude-price risk, largely orthogonal to AI compute. The clean "AI-power" bet is **electricity/power-infrastructure** (nuclear IPPs, gas turbines, grid, datacenter cooling), not hydrocarbons. And most of it has already re-rated hard. |

**Bottom-line recommendation (detail in §9):** Given your Adobe concentration + genuine bubble risk + your own stated weak stock-picking record, **do not try to hand-pick AI single names as your primary AI exposure.** Lean on (a) breadth/indexing for the "AI is real" upside, (b) 1–2 high-conviction quality names you already understand (Alphabet is the cleanest), and (c) treat your involuntary Adobe stake as your app-layer bet — and decide whether to *reduce* it, not add to it.

---

## 1. Is there an AI bubble? — Half-true. Concentrated froth, not uniform mania.

### Valuations (VERIFIED, stockanalysis.com, 2026-07-06)

| Company | Price | Trailing P/E | Forward P/E | Mkt cap |
|---|--:|--:|--:|--:|
| Nvidia (NVDA) | $195.55 | 29.9 | **19.7** | $4.74T |
| Microsoft (MSFT) | $386.74 | 23.0 | **20.9** | $2.87T |
| Alphabet (GOOGL) | $366.46 | 28.0 | 29.2 | $4.47T |
| Amazon (AMZN) | $244.16 | 29.2 | 29.2 | $2.63T |
| Meta (META) | $600.29 | 21.8 | **18.3** | $1.52T |
| Apple (AAPL) | $312.66 | 37.9 | 34.3 | $4.59T |
| Tesla (TSLA) | $419.77 | 408 | **191** | $1.58T |
| Broadcom (AVGO) | $373.90 | 62.2 | 23.8 | $1.78T |
| Palantir (PLTR) | $132.54 | **149** | **83** | $318B |
| AMD | $552.05 | **184** | **63** | $900B |
| Oracle (ORCL) | $143.76 | 24.7 | 17.9 | $414B |

- **The key insight:** the mega-cap compute owners (NVDA fwd 19.7x, MSFT 20.9x, META 18.3x, ORCL 17.9x, AVGO 23.8x) trade at forward multiples **near or only modestly above the market** — remarkable given 20%+ growth. That is the strongest "NOT a bubble" fact. The genuine froth sits in **Tesla (191x fwd), AMD (63x fwd), Palantir (83x fwd)**.
- **Market-level warning signs (VERIFIED):** S&P 500 P/E **32.4** vs historical mean 16.2 (multpl.com, 2026-07-06) — ~2x its long-run average. Shiller CAPE **exceeded 40** for the first time since the dot-com crash (late 2025). Five largest companies ≈ **30% of the S&P 500** ("greatest concentration in 50 years"); Nvidia alone ~7.3%. AI-related firms drove **~80% of 2025 US market gains**.

### The capex boom (VERIFIED, cash-flow statements, stockanalysis.com)

| | FY2024 | FY2025 | TTM (~Mar 2026) |
|---|--:|--:|--:|
| Microsoft | $44.5B | $64.6B | $97.2B |
| Alphabet | $52.5B | $91.4B | $109.9B |
| Amazon | $83.0B | $131.8B | $151.0B |
| Meta | $37.3B | $69.7B | $75.7B |
| **Sum of 4** | **~$217B** | **~$357B** | **~$434B** |

Hyperscaler capex roughly **doubled in ~18 months** to a ~$430B+/yr run rate. Alphabet guiding ~$190B FY26 capex; Meta guided ~$145B for 2026 (ASSUMED — snippet) and the stock dropped ~8% on the announcement. Morgan Stanley (ASSUMED, single-source): ~$3T global datacenter spend 2025–2028, half funded by private credit; datacenter debt could exceed $1T by 2028.

### Circular-financing web (the core bear thesis — deal *structures* VERIFIED-as-reported, exact $ ASSUMED where still negotiating)

- **Nvidia → OpenAI:** ~$100B investment MOU (Sept 2025), up to 10+ GW of Nvidia systems. The concern: Nvidia funds OpenAI → OpenAI buys Nvidia GPUs → looks like organic demand.
- **OpenAI → Oracle:** ~$300B compute over ~5 yrs (Stargate).
- **Stargate (OpenAI+SoftBank+Oracle+MGX):** $100B initial → $500B target by 2029. Bloomberg (Aug 2025): "no funds raised" toward it yet; SoftBank funding heavily debt-based.
- **AMD → OpenAI (Oct 2025):** 6 GW MI450; OpenAI granted a warrant on up to **160M AMD shares (~10%)** — buyer becomes a large shareholder.
- **Microsoft ↔ OpenAI:** OpenAI committed **$250B of Azure**; MSFT holds ~27%.
- **OpenAI ↔ CoreWeave (Mar 2025):** OpenAI took $350M of CoreWeave stock; CoreWeave gets $11.9B over 5 yrs from OpenAI.

The same dollars circulate among Nvidia, OpenAI, Oracle, AMD, CoreWeave, Microsoft. The most fragile node is **cash-burning OpenAI**.

### Durable earnings vs top signals

- **Durable (bull):** Nvidia Data-Center revenue is real and accelerating — Q4 FY2026 (rep. Feb 25, 2026) Data Center **$62.3B**, +75% YoY → **~$249B annualized run-rate**; full FY2026 net income **$120.1B** (VERIFIED, Nvidia IR). This is nothing like 2000's revenue-less dot-coms.
- **Top signals (bear):** A **June 2026 selloff** — Oracle −19% (worst week since dot-com), Micron −13%, Nasdaq −5% cumulative (VERIFIED-as-reported, Wikipedia). **Michael Burry** disclosed puts on Nvidia and Palantir, deregistered Scion (Nov 25, 2025), started an AI-bubble Substack. **BoE, IMF (Georgieva), Ray Dalio** all drew dot-com comparisons; **Jamie Dimon:** "AI is real" but much invested money "will be wasted." **OpenAI economics:** ~$13.1B 2025 revenue but **~$9B net loss**, ~$1.4T of datacenter commitments; some estimates it "runs out of money by mid-2027" — yet valued at **$852B** (Apr 2026). MIT (2025): 95% of business AI projects unprofitable (ASSUMED).

### Dot-com comparison

- Nasdaq 2000 peak P/E **≈ 200**; fell 78% by Oct 2002, ~$5T erased. Cisco briefly >$500B, lost ~80%. **Cisco peak trailing P/E ~130–150x is UNVERIFIED** (couldn't confirm from a live source).
- **Verdict:** The *concentration* and CAPE >40 rhyme with 2000. The decisive difference is **earnings quality** — today's leaders are highly profitable at 18–29x forward, nowhere near 200x. The bubble risk is concentrated in (a) momentum names at 60–190x, and (b) the circular, debt-funded, loss-making OpenAI demand engine. **Your instinct — "bubble, but real, with winners" — is directionally correct; just don't treat the whole complex as one bubble.**

**Score: 7/10.** Right that risk is elevated and a shakeout is plausible; slightly wrong to model it as a uniform dot-com-style bubble across all AI names.

---

## 2. Alphabet (Google) — "genuinely good" is the best-supported claim you made. Score 8/10.

**Bull (mostly VERIFIED from Alphabet Q1 2026 release, 2026-04-29):**
- **Google Cloud inflecting:** Q1'26 revenue **$20.0B, +63% YoY**; operating income $6.6B → **~33% margin** (vs ~18% a year earlier); **backlog ~$460B, nearly doubled QoQ.** This is the standout. Growing faster than AWS/Azure.
- **Search resilient — the feared disruption isn't in the numbers yet:** Search revenue **$60.4B, +19% YoY**, "queries at an all-time high." AI Overviews >2.5B monthly users; AI Mode >1B (both VERIFIED-ish, snippets).
- **Gemini credible at/near frontier:** Gemini 3 (Nov 2025) → shipping fast into 2026 (3.5 Flash May 2026). Consumer AI "strongest quarter ever"; 350M paid subscriptions; Gemini Enterprise +40% QoQ paid MAU; >16B tokens/min via API (+60% QoQ).
- **TPUs are now a real moat:** Anthropic committed to **up to 1M Google TPUs / >1 GW** (Oct 2025); Meta reportedly in talks to deploy TPUs (Nov 2025). Full vertical stack (chips → models → cloud) that most rivals lack.
- **Antitrust de-risked:** Sept 2025 remedy — no exclusive default deals + data-sharing, but **NOT forced to divest Chrome/Android** (Barron's: "almost best-case"). Appeals ongoing.
- **Valuation:** ~28x trailing / 29x forward at $4.47T. Not statistically cheap, but reasonable vs 20%+ growth and 63% cloud growth.

**Bear (honest):**
- Gemini's benchmark lead is **contested, not decisive**; rivals still win specific benchmarks.
- **AI-search monetization rate vs legacy 10-blue-links is unquantified** (UNVERIFIED) — the central unknown. Publisher-traffic cannibalization is real.
- Q1'26 headline net income +81% was **inflated by a $37.7B one-time equity gain**; core operating income grew a cleaner **+30%**. Use +30%.
- ~$190B FY26 capex is enormous. Cloud still only ~#3 (~13% share, UNVERIFIED).

**Verdict:** Your "Google is genuinely good" is the strongest single call in your thesis. It's the cleanest quality-at-a-reasonable-price AI winner: real accelerating cloud profits, a defensible vertical stack, and search holding up. Forward P/E 29 is the one caveat — not a bargain.

---

## 3. Amazon — right on Anthropic, WRONG on OpenAI. Score on the stake claim: partially incorrect.

- **Anthropic stake — VERIFIED equity, ~$8B cumulative, minority:** $1.25B (Sept 2023) → +$2.75B (Mar 2024, "total investment... $4 billion") → +$4B (Nov 2024) = **~$8B**. Structure explicitly a **minority stake**; exact % **not disclosed**. (Amazon press releases; Wikipedia "Anthropic," 2026-07-07.) For comparison Google put in ~$3B — so Amazon is Anthropic's largest strategic investor. Anthropic uses AWS as primary cloud, Claude on Bedrock, trains on Trainium.
- **OpenAI stake — REFUTED.** Amazon holds **no OpenAI equity.** OpenAI's Oct 2025 cap table: **Microsoft ~27%, OpenAI Foundation ~26%, employees/other ~47%** — Amazon absent. The real Amazon–OpenAI link is a **$38B AWS compute contract over 7 years** (announced Nov 3, 2025) — a customer relationship, **not a stake**. **Microsoft, not Amazon, is OpenAI's equity backer.** (⚠️ A Wikipedia line claiming "Amazon led a $50B OpenAI round Feb 2026" is unsourced, contradicts the same article's cap table, and couldn't be corroborated — treat as erroneous.)
- **AWS AI position (VERIFIED):** Q1'26 revenue ~$37.6B, **+28% YoY** (fastest in ~15 quarters), ~37–38% margin, ~$150B run-rate. Trainium/Inferentia at a **~$20B run-rate**; **Project Rainier** = the huge Trainium cluster for Anthropic. AWS is ~21% of revenue but **~60% of operating profit** — the valuation anchor.
- **Valuation:** $244.16, $2.63T, trailing/forward P/E ~29x.

**Verdict:** Amazon is a legitimate AI winner via AWS + its Anthropic stake. But **correct your mental model: you do not get OpenAI exposure through Amazon.** If you want OpenAI-adjacent equity exposure, the public proxy is **Microsoft** (~27%), and the compute-demand proxies are Nvidia/Oracle/AMD/Broadcom — none of them Amazon.

---

## 4. Microsoft & Meta — your lower conviction is *understandable* but arguably overshoots. Score 5/10.

**Valuations (VERIFIED, 2026-07-06):** MSFT $386.74 / $2.87T / **fwd P/E 20.9**; META $600.29 / $1.52T / **fwd P/E 18.3**. Both are **cheaper on forward earnings than GOOGL (29) and AMZN (29)** — the two you prefer. Worth sitting with that.

**Microsoft:**
- OpenAI restructured to a PBC (Oct 28, 2025): MSFT stake **~27%, marked at ~$135B**; Azure API exclusivity + IP through AGI, but AGI now verified by an independent panel and **MSFT lost right-of-first-refusal on compute**. OpenAI went multi-cloud ($38B AWS, ~$300B Oracle) — a genuine narrative negative. Offsetting: OpenAI committed **$250B of Azure**.
- Azure ~40% growth (ASSUMED); AI run-rate ~$37B (ASSUMED). Capex FY23 $28B → FY25 $65B → **TTM $97B** (VERIFIED) — tripled, and accelerating.
- Fundamentals intact: TTM revenue +18%, EPS +30%. **The de-rating (mkt cap down ~19%) is narrative/multiple, not deteriorating fundamentals.**

**Meta:**
- **Llama 4 (Apr 2025) was a botched, controversial launch** (LMArena rebuke, test-set accusations). Pivot: **Meta Superintelligence Labs** (Jun 2025), **$14.3B for ~49% of Scale AI** + hired Alexandr Wang. **Retreating from full open-source** — Zuckerberg's Jul 30, 2025 letter: will be "careful about what we choose to open source." (This partly undercuts *your* "flood of cheap open-source" thesis — see §5.)
- Capex FY25 $69.7B → TTM $75.7B; **2026 guide ~$145B** (ASSUMED) triggered an ~8% drop. Ad revenue +26% TTM shows AI targeting is working. Concern is ROI/timing, not solvency. Cheapest of the group at 18.3x forward.

**Verdict:** Both are quality-at-a-price where multiple compression exceeds any visible fundamental damage — which actually *fits your value framework*. MSFT's moat narrative genuinely weakened (OpenAI diversifying away); Meta's concern is more real (Llama stumble + $145B spend with unproven ROI). But being *more* bearish on MSFT/Meta than on the pricier GOOGL/AMZN is not clearly supported by the numbers. If anything, they're the value names in the group.

---

## 5. "Models commoditize; value → app + infra layer" — your best-supported thesis. Score 8/10.

**Commoditization — YES for mid-tier, CONTESTED at the frontier:**
- **DeepSeek shock (Jan 2025):** V3 claimed ~$5.6M marginal training cost (the single most-disputed AI number — excludes R&D/infra); R1 claimed o1-parity. Triggered **Nvidia's ~17% / ~$600B single-day drop (Jan 27, 2025)** — largest US market-cap loss ever.
- **Cost-per-token collapse (VERIFIED):** a16z "LLMflation" ≈ **10x/yr decline** at fixed performance; Epoch AI median 50x/yr. Open weights now ~6–12 months behind frontier (Llama, Qwen3, DeepSeek).
- **VC consensus (VERIFIED):** Sequoia's "AI's $600B Question" / "Act o1" — model layer is "a knife-fight," value accrues to the app layer.
- **Counter (VERIFIED):** **test-time compute is a new scaling law** — o3 hit SWE-bench 71.7% vs o1's 48.9% within weeks of DeepSeek; Stargate's $500B capex keeps the frontier moving. **The frontier premium has NOT collapsed.** Also note: Meta *retreating* from open-sourcing frontier models (§4) slightly cuts against "market flooded with cheap open frontier models" — the cheap open models trail the frontier.

**The money proof (Menlo Ventures, Dec 2025, ASSUMED-as-reported):** total gen-AI spend **$37B in 2025 (3.2x YoY)**; **application layer $19B = 51%, first time above infrastructure.** Coding = $4B standout. Model-provider share: Anthropic 40%, OpenAI 27%.

**Infra-layer winners (data-dense; mix VERIFIED/ASSUMED):**
- **Chips:** Nvidia (DC ~$205B run-rate Q3 FY26, ~90% merchant AI-GPU share); AMD (OpenAI 6 GW deal); **Broadcom** (custom ASIC/XPU king, AI semi ~$10.8B/qtr +143%, tracking ~$56B AI FY — ASSUMED); Marvell; **TSMC** (CoWoS packaging is the binding constraint). Rising custom-silicon (Trainium/TPU/Maia) is the key risk to Nvidia's share.
- **Memory (HBM — 2nd chokepoint):** **SK Hynix** (leader, stock +250% H1'26 — ASSUMED), **Micron** ("biggest quarter ever" Jun 2026), Samsung catching up. HBM effectively sold out into 2026.
- **Networking:** Broadcom, **Arista** (1.6T Ethernet, ~55x earnings), Nvidia now #1 in DC Ethernet switching.
- **Power/electrical/thermal — the strongest *quantified* backlog signals:** **Vertiv (VRT)** orders +60%, backlog ~$15B, ~70x P/E; **GE Vernova (GEV)** Q1'26 orders $18.3B (+71%), backlog $163B, DC orders $2.4B in one quarter > all of 2025; **Eaton, Schneider, Quanta (PWR backlog $48.5B), Powell** (orders +97%).

**App-layer — winning on revenue, but margins are the tension:** Palantir Q1'26 revenue $1.63B (+85%) but **~61x sales / 149x P/E**; ServiceNow +22%, ~25x forward; coding tools hyper-growth but thin margins (Cursor only "slight" gross-margin profitability Apr 2026; GitHub Copilot moved to usage-based billing Jun 2026 because flat per-seat is "no longer sustainable"). **Threat:** model labs move up-stack (Claude Code $2.5B ARR) and eat app revenue directly. AI apps run ~50–65% gross margin vs classic SaaS 80%+ — **the inference-cost squeeze is real, and it matters directly for Adobe (§7).**

**Verdict:** Your framing is the emerging consensus and largely validated. Two refinements: (1) don't over-assume the *frontier* commoditizes — it hasn't; (2) the app layer wins on *revenue* but faces a *margin* squeeze from inference costs and from model labs moving up-stack. **Value-investor caveat: the infra winners are mostly expensive** (Palantir 61x sales, Vertiv 70x P/E, GEV fwd 62x). Cheapness — not quality — is the binding filter here.

---

## 6. "Energy as indirect AI bet" — the weakest link in your thesis. Score 4/10.

**The core error: "energy" ≠ "AI power."**
- **Broad energy / XLE is oil & gas, not electricity.** XLE top holdings: Exxon 20%, Chevron 15%, ConocoPhillips 6%, refiners, pipelines — the top 10 (72% of the fund) have **zero direct AI-datacenter-electricity exposure.** Buying XLE for the AI theme mostly buys **crude-oil price risk** (OPEC+, global GDP, transport) — largely orthogonal to AI compute. Its +26% 1-yr return was an oil move, not an AI move. **You already hold ~30% of your non-cash portfolio in oil & gas — that is a commodity/USD-hedge bet, not an AI bet. Don't conflate the two.**

**What actually captures the AI-power theme (electricity/power infrastructure):**
- **Datacenter power demand is real (VERIFIED, secondary):** global datacenter electricity ~415 TWh in 2024 (~1.5% of global) → IEA projects **~945 TWh by 2030** (~2.3x); datacenters ≈ **half of all new US electricity-demand growth through 2030**; US datacenter share heading to ~6.7–12% by 2028 (LBNL). US load is genuinely inflecting after ~15–20 flat years.
- **Cleanest plays:** nuclear/merchant IPPs — **Constellation (CEG)** (Microsoft/Three Mile Island restart; P/E ~21 — the relative-value name), **Vistra (VST)** (fwd P/E ~17), Talen (TLN); gas turbines — **GE Vernova (GEV)**; datacenter electrical/thermal — **Vertiv, Eaton**; transmission — **Quanta**.
- **The catch (VERIFIED prices):** these have **already re-rated hard** — GEV +131% 1-yr (fwd P/E 62), VRT P/E 80, PWR +90%. The theme is real but **largely priced in.** CEG (P/E 21) and VST (fwd P/E 17) are the survivors on a value lens.
- **ETFs:** **NUKZ** (nuclear renaissance — Cameco, GEV, Rolls-Royce; +49%/yr since Jan 2024) and **GRID** (First Trust Smart Grid — Schneider, Eaton, ABB, Quanta; +35% 1-yr) are the cleanest single-ticket "AI power" instruments.

**Verdict:** The *instinct* (get AI upside without picking model winners) is sound, and "AI power" is a legitimate indirect theme. But **the execution in your framing is off**: your oil-heavy energy book does not deliver it. If you want indirect AI-power exposure, own *electricity/grid/nuclear* — and even there, be a valuation discipline because it's crowded. **Note your portfolio already holds CEG, CCJ, BWXT (uranium/nuclear) and GEV (electrification)** — so you *already* have some of the clean AI-power exposure; the oil & gas block is not adding to it.

---

## 7. Adobe (your ~$732k single biggest asset) — the market says "victim," the fundamentals say "winner-in-progress." This is material.

**The setup (VERIFIED, 2026-07-06):** ADBE **$218.07**, mkt cap **$86.7B (down ~47%)**, **P/E 12.5, forward P/E 8.4** — a violent derating for a company that historically traded 30–45x. 1-yr −43%, 5-yr −64%. Yet fundamentals are fine: FY2025 revenue $23.8B (+10.5%), Q2 FY2026 record revenue $6.62B, **total ARR $27.1B (+12.5% YoY)**, earnings up.

**Why it's down:** the market is pricing a **terminal AI-disruption risk** (OpenAI images/Sora, Midjourney, Google, Canva, Figma commoditizing creative tools), amplified by skepticism about Adobe's new **freemium pivot** (read as an admission of pricing-power pressure). This is exactly the app-layer margin squeeze from §5, aimed at Adobe.

**Bull case ("winner not victim"):** "AI-influenced ARR topped $5B" (Q3 FY2025); Firefly trained on commercially-safe licensed data (a real enterprise/legal differentiator vs Midjourney/OpenAI); entrenched enterprise base (99% of Fortune 100); aggressive product cadence (Firefly Image Model 5, video, Topaz acquisition). At 8.4x forward with +12.5% ARR growth, the bar is very low; consensus "Hold," target ~$280 (~29% upside).

**What this means for your positioning — the most important practical point in this report:**
1. **You are already massively long the app layer via Adobe (~$732k RSUs vesting over 4 yrs).** Adobe *is* an AI-application-layer bet — precisely the layer you (correctly) think has winners but which also faces the clearest margin/commoditization pressure. You don't need to *add* app-layer AI exposure; you need to decide whether to *keep* this much.
2. **It is a concentrated, single-stock, single-employer bet** where your salary and your equity are the same risk. If the AI-victim thesis wins, you lose your RSU value and job security together.
3. **The fact that it's cheap (8.4x fwd) cuts both ways.** As an outside value investor you might *buy* Adobe here as a contrarian quality-at-a-price name. But you already own $732k of it involuntarily — so the rational move is almost certainly to **diversify away from it as it vests** (sell RSUs on vest, redeploy elsewhere), not to double down. Concentration risk dominates the cheap-multiple appeal when it's this large a share of your net worth and it's your employer.

**Verdict:** Adobe is a genuine coin-flip between "cheap quality survivor" and "structurally disrupted." For a *diversified* investor it's an interesting contrarian buy. For *you specifically* it's an oversized, undiversifiable concentration you should be trimming as it vests — and it already gives you all the app-layer AI exposure you need.

---

## 8. Cross-cutting: what your thesis is missing

1. **You have no direct infra-layer exposure** — the layer with the most verified earnings (Nvidia DC ~$249B run-rate; HBM sold out; power backlogs exploding). Your only proxies are indirect (uranium/nuclear, GEV). Yet infra is where you said the winners are.
2. **The "government bailout of OpenAI is probable" claim (thesis #3) is UNVERIFIED speculation.** No evidence found. Don't build a position around a low-visibility policy bet — that's exactly the kind of call your stated weak track record should avoid.
3. **You already own the pieces, uncoordinated:** AMZN + ARKK (tech), CEG + CCJ + BWXT (nuclear/AI-power), GEV (electrification), + $732k Adobe (app layer). Your portfolio *already expresses* much of this thesis — the problem is it's unintentional and unbalanced, not that you lack exposure.
4. **Concentration + your self-described weak stock-picking = index the theme, don't hand-pick it.** The single most reliable finding across all six research streams is that *which* AI name wins is genuinely uncertain (Gemini's lead contested, OpenAI loss-making, Meta stumbling, model layer commoditizing). Uncertainty that deep argues for breadth over conviction bets.

---

## 9. Recommendation — how to hold AI given Adobe + bubble fear + weak stock-picking

**Framework:** Treat Adobe as your (involuntary, oversized) app-layer AI bet. Everything else should be (a) diversified, (b) valuation-disciplined given bubble risk, and (c) minimally dependent on you picking the single winner.

**Concrete, in rough priority order:**

1. **Reduce Adobe concentration as RSUs vest.** Sell on vest and redeploy — don't accumulate $732k+ in a single disrupted-app-layer employer stock. This is the highest-impact AI-portfolio decision you have. (Not tax/legal advice — check the CAD tax treatment of RSU sales.)

2. **For the "AI is real, winners exist" upside — use breadth, not single-name bets.** A low-cost broad tech/Nasdaq index (e.g., QQQ or a total-market fund) captures the mega-cap compute owners at their *reasonable* forward multiples (NVDA 20x, MSFT 21x, META 18x) without you having to pick. You already hold **ARKK** — note that's a *concentrated, high-beta, speculative* AI/growth bet, the opposite of diversified breadth; consider whether it fits your ≤10% volatility constraint.

3. **If you want 1–2 direct quality names, Alphabet is the cleanest** (best-supported thesis, vertical moat, cloud inflecting, resilient search — accept it's ~29x, not cheap). **Microsoft and Meta are the value names** (18–21x forward, intact fundamentals) if you can tolerate the OpenAI-diversification and capex-ROI narratives. **Amazon** is fine but correct the OpenAI misconception. **Avoid the 60–190x-forward names (Tesla, AMD, Palantir)** — that's where a bursting-bubble scenario does the most damage, and it's exactly the terrain your track record says to skip.

4. **For indirect "AI infrastructure" exposure that avoids picking model winners** — this is the *correct* version of your energy idea:
   - **Semis breadth:** SOXX (more equal-weight) or SMH (Nvidia-heavy) instead of single chip names.
   - **AI power / grid:** GRID (Schneider/Eaton/Quanta/ABB) and/or NUKZ (nuclear) — but **valuation-discipline: much is priced in.** On single names, CEG (P/E 21) and VST (fwd 17) are the relative-value survivors, and you *already own CEG*.
   - **This replaces, not supplements, the idea that oil & gas is an AI bet — it isn't.**

5. **Keep it sized for your constraints.** You have a 3–5yr house horizon and a ≤10% volatility ceiling, and AI names are the highest-beta thing you can own into a possible shakeout. Any *new* direct AI exposure belongs in the opportunistic-growth bucket (already ~7.7 pts over target) — so this likely means **reshaping existing tech exposure (ARKK, AMZN, Adobe) rather than adding net new risk.**

**One-sentence answer to your question:** Given your Adobe concentration, real bubble risk, and self-assessed weak stock-picking, you should get your "AI is real" upside mostly through **breadth (index)** plus **at most 1–2 quality names you understand (Alphabet first)**, get indirect exposure through **power/semis ETFs rather than oil & gas**, and treat **trimming Adobe** — not adding AI — as the single most valuable move.

---

## Verification Log & Confidence

**VERIFIED (primary or reliable, source + date inline):** all stock prices/multiples (stockanalysis.com, 2026-07-06); Alphabet Q1'26 financials (earnings release 2026-04-29); Microsoft–OpenAI 27%/$135B/$250B terms (Microsoft blog 2025-10-28); Zuckerberg open-source letter (2025-07-30); Scale AI $14.3B/49% + Meta Superintelligence Labs; Amazon–Anthropic ~$8B staged (Amazon releases 2023–24); OpenAI–AWS $38B (Nov 3, 2025); Nvidia DC revenue/run-rate (Nvidia IR, Feb 25, 2026); capex figures (cash-flow statements); DeepSeek Jan 2025 shock + Nvidia −17%; cost-per-token −10x/yr (a16z/Epoch); IEA datacenter power (415→945 TWh); ETF holdings (SMH/SOXX/GRID/NUKZ/XLE); Adobe price/ARR/multiples.

**ASSUMED (single news-snippet, not primary — re-pull before trading):** Azure ~40% growth; MSFT/Meta AI run-rates; Meta ~$145B 2026 capex guide; Broadcom/Marvell/Micron/SK-Hynix exact AI figures; Menlo $37B/51%-app-layer split; Morgan Stanley $3T; MIT 95%; June-2026 selloff magnitudes; Adobe "$5B AI-influenced ARR."

**UNVERIFIED (could not confirm — do NOT rely on):** Cisco 2000 peak P/E (~130–150x); exact current LMArena standings; AI-search monetization rate; Google Cloud market-share %; peer-by-peer P/E table beyond the six majors; **the Wikipedia "Amazon $50B into OpenAI" line (contradicts OpenAI's cap table — treat as erroneous)**; **"government bailout of OpenAI is probable" (your thesis #3 — no supporting evidence found).**

**Known gaps / suggested follow-ups:** pull Adobe Q2 FY2026 transcript for standalone Firefly ARR + freemium detail; re-pull hyperscaler capex/segment splits from EDGAR 10-Q; confirm circular-financing deal $ from primary IR (many still under negotiation); get a clean peer forward-P/E table; verify Cisco peak multiple from a financial-history source.
