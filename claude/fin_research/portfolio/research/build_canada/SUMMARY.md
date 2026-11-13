# Build Canada: eight companies and the LionGuard interview

**Complete comparative research, with an October 22 implementation addendum.** The original comparison uses information and closing share prices through **October 20, 2026** and was compiled October 21 UTC. Hooman subsequently bought CGY, EFX, BDGI, VNP and FTG on October 22; those user-confirmed fills, plain-language business descriptions and the later AI-spending-collapse screen are recorded below. Allocation targets remain unchanged.

**Conclusion — ASSUMED investment judgment, moderate confidence:** Under the original broad Build Canada/AI-beneficiary objective, **Enerflex and Calian were the strongest candidates**, followed by Badger. The later requirement was narrower: physical businesses that should be less exposed if data-center spending collapses. Under that screen, **Badger is the best intersection, Calian is relatively resilient, and Enerflex is cheap but directly exposed to the specified risk**. FTG and 5N Plus have attractive specialist businesses but demanding prices. Magellan has weaker cash conversion and governance. Canaccord is a cyclical financial special situation. Electrovaya is the most speculative and weakest fit.

**November 6 execution addendum — USER-CONFIRMED:** Questrade Cash bought 60 EFX at C$27.28,
40 FTG at C$32.40, 25 CGY at C$84.99 and 40 BDGI at C$74.97, for C$8,056.35 gross. The complete
Cash/RRSP snapshot now shows 120 EFX, 100 FTG, 36 CGY and 65 BDGI. The existing 80 VNP shares were
retained, but no VNP add was made because the price had risen too far. This execution records price
discipline and does not alter the sleeve mappings or allocation targets below.

### November 5–6 execution-timing postmortem

**As of November 7, 2026. VERIFIED arithmetic on USER-CONFIRMED fills and secondary market data;
moderate confidence.** “Crash day” is assumed to mean November 5. Unadjusted daily and five-minute
OHLC data came from Yahoo Finance through `yfinance` and were cross-checked against the November 6
saved `fin_check` snapshot. The four fills occurred inside their matching five-minute trading ranges,
so there is no evidence that the limit orders themselves produced abnormal execution prices.

| Name | Nov. 6 fill | vs. Nov. 5 close | vs. Nov. 5 low | vs. Nov. 3 pre-selloff close | vs. conservative upper review level | Assessment |
|---|---:|---:|---:|---:|---:|---|
| EFX | C$27.28 | +3.2% | +4.8% | **−16.6%** | **−13.1%** | Small rebound, but still bought well inside the prior valuation range. |
| BDGI | C$74.97 | **−5.9%** | **−2.3%** | **−16.8%** | Not a rebound purchase; the stock fell further after November 5 and the fill was below the prior review ceiling. |
| CGY | C$84.99 | +1.8% | +4.1% | +0.1% | **+20.8%** | Little timing penalty, but essentially no pre-selloff discount and still above the conservative valuation range. |
| FTG | C$32.40 | **+7.0%** | **+8.2%** | −5.1% | **+24.2%** | Clearest rebound purchase and furthest above the prior conservative range. |

For the exact quantities purchased, the batch would have cost C$8,073.15 at the November 5 closes;
the actual C$8,056.35 cost was **C$16.80 lower** because BDGI's additional decline offset the other
three rebounds. Buying each name at its separate November 5 intraday low—an unattainable hindsight
benchmark because the lows occurred at different times—would have saved **C$186.30, or 2.3%**.
Compared with the November 3 closes before the two-day selloff, the actual basket was about **11.0%
cheaper**. Therefore the batch was not broadly bought after the discount disappeared, although FTG
and CGY did not meet the original value discipline.

The November 6 no-add in VNP was consistent with that discipline: VNP rose from C$30.65 on November
5 to C$33.53 on November 6, about **9.4%**, and the latter price was roughly 51% above the recorded
C$22.24 upper review level. These review levels remain scenario sensitivities, not fair-value facts or
automatic sell thresholds. Raw figures and reproduction fields are stored in
`/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/execution_timing_2026-11-05_06.csv`.

**Current implication — ASSUMED judgment:** do not reverse the November 6 trades merely because of
the rebound concern. EFX and BDGI were acceptable on the recorded price gates. Freeze further adds
to all four because their mapped sleeves are now full or overweight. If capital later has to be
reclaimed from these additions, review FTG first and CGY second; their purchase prices were furthest
above the conservative ranges. BDGI's November 6 decline followed its November 5 earnings date in
the secondary calendar, so its Q3 primary filing should be re-underwritten before treating the lower
price as a clean bargain.

**November 2 current-price screen — RESEARCHER JUDGMENT, not an order or accepted allocation change:**
If existing sleeve capacity is ignored, Enerflex is the only one of the five purchased names that is
close enough to the conservative valuation range to justify a small starter today. `EFX.TO` was about
C$31.98, or US$22.87 at CADUSD 0.71510, only 1.8% above the prior US$22.46 upper review level. A
hypothetical 0.25%-of-portfolio add is about US$1,689 / C$2,362 / 74 shares at that price, bringing
the existing 60-share position to roughly 0.45% of the current US$675,588 portfolio. Do not make a
full allocation before contract economics and cash conversion improve. Badger at C$84.62 was 6.3%
above its C$79.58 upper review level; Calian, 5N Plus and FTG remained approximately 19%, 19% and 23%
above theirs. This price comparison holds trailing inputs constant and is not intrinsic value.

Canada's investment thesis has real policy/project evidence. An eight-stock basket would nevertheless concentrate the portfolio in capital spending, procurement and growth expectations. None is a dependable recession, emergency-cash or CAD currency hedge.

## Contents

- [Context and method](#context-and-method)
- [Comparison](#comparison)
- [Businesses, AI-spending risk and October 22 implementation](#businesses-ai-spending-risk-and-october-22-implementation)
- [Canadian buildout and currency exposure](#canadian-buildout-and-currency-exposure)
- [Company evidence](#company-evidence)
- [Valuation sensitivities](#valuation-sensitivities)
- [Interview and manager credibility](#interview-and-manager-credibility)
- [Past picks](#past-picks)
- [Portfolio fit and next validation](#portfolio-fit-and-next-validation)
- [Sources](#sources)
- [Durable artifacts and reproduction](#durable-artifacts-and-reproduction)

## Context and method

**USER-CONFIRMED:** Canadian citizen, bullish Canada, California resident filing jointly, single household earned income tied to Adobe/TN status. Priorities: inflation/currency protection, recession protection, house/job flexibility. A conditional house purchase in 2–3 years could use most of the portfolio; CAD250,000 with his father is separate. Unvested Adobe compensation is not liquid safety capital. The October 14 reserve-led allocation proposal remains unaccepted.

**ASSUMED:** This request authorizes comparative research, not orders or a new risk budget. The eight names are a purposive sample, not all Canadian opportunities. Monthly spending, loss tolerance, reserve access and account/tax lots remain implementation gaps. Prior diagnostic questions and the supplied specification suffice for this research; no exact position size is inferred.

Three **GPT-5.6-sol / high-effort** workers collected issuer evidence, as requested. The primary agent integrated results, investigated the interview, manager and policy, challenged decisive claims and recomputed valuations. Primary filings/contracts/circulars outrank promotion and vendor ratios. **VERIFIED** below means directly supported company disclosures or reproducible calculations, with source references; it does not guarantee forecasts. **ASSUMED** means interpretation, valuation judgment or scenario. **UNVERIFIED** identifies an evidence gap, not necessarily a false statement.

Latest annual/interim filings available by October 20 were used. Most interim periods end June 30; FTG ends August 28. Share counts are latest identified primary counts, not perfectly synchronized October 20 fully diluted shares. Market prices are secondary vendor quotes. FX is the saved CADUSD spot snapshot, approximately **US$0.71119 per CAD**, not an exchange-close fixing. Retrieval was October 20 Pacific / October 21 UTC; subsequent information is excluded.

Live portfolio was read before comparison: stored sheet marks approximately **US$684,023 total / US$271,262 cash**, not a fresh broker valuation or tax-adjusted house budget. NKE is closed following its recorded October 20 sale. Current accepted sleeve targets, rather than the unaccepted macro proposal, are the baseline.

## Comparison

**Valuation arithmetic VERIFIED; quality, cheapness and fit are ASSUMED judgments.** Multiples are financial enterprise value/trailing issuer-adjusted EBITDA, except Canaccord. EBITDA definitions differ and are not cash available to shareholders.

| Company and correct ticker | Oct 20 price | Valuation screen | Business quality | AI evidence | Portfolio assessment |
|---|---:|---:|---|---|---|
| **Enerflex — TSX EFX / NYSE EFXT** | C$33.96 / US$24.16 | **6.4×** | Established equipment, assets and services; cyclical | **Confirmed data-center power orders**; AI-specific fraction undisclosed | **First shortlist:** attractive relative value; substitute within energy budget |
| **Calian — CGY.TO** | C$83.25 | **10.5×; ~18.7× adjusted earnings** | Diversified technical/services franchise; acquisition and cash concerns | **Delivered AI applications**, financial contribution undisclosed | **First shortlist:** best Canadian-demand fit; price discipline |
| **Badger — BDGI.TO** | C$86.81 | **10.8×; ~28.6× adjusted earnings** | Scaled hydrovac network; capital intensive | Indirect utilities/construction exposure | **Watch:** good business, full price, predominantly U.S. |
| **Firan Technology — FTG.TO** | C$33.11 | **20.3×; ~37.6× reported earnings** | Qualified aerospace electronics; switching barriers | No material AI revenue identified | **Watch:** strong growth, expensive earnings base |
| **5N Plus — VNP.TO** | C$27.52 | **17.3×; ~27.8× reported earnings** | Specialist materials/semiconductors; customer concentration | Semiconductor adjacency; AI revenue unverified | **Watch:** attractive niche, weaker margins/cash |
| **Magellan — MAL.TO** | C$33.07 | **12.9×; ~31.7× reported earnings** | Established aerospace supplier; control/customer concentration | No material AI revenue identified | **Lower priority:** cash and governance discount needed |
| **Canaccord Genuity — CF.TO** | C$13.47 | **9.0× adjusted earnings; IFRS loss** | Wealth franchise plus cyclical capital markets | Tech financing is indirect exposure | **Special situation:** conditional cheapness |
| **Electrovaya — ELVA / ELVA.TO** | US$5.35 / C$7.55 | **24.7×; ~60.7× reported earnings** | Promising technology; small and concentrated | **Prospective** data-center product, not established revenue | **Pass for current portfolio:** speculation |

**Ticker traps:** CF.TO is Canaccord; the portfolio's U.S. CF is CF Industries. TSX EFX is Enerflex; U.S. EFX is Equifax. Enerflex's U.S. ticker is **EFXT**.

The main EV measure excludes leases. Lease-inclusive multiples are EFX **6.5×**, CGY **10.9×**, BDGI **11.1×**, FTG **20.9×**, VNP **17.5×**, MAL **13.1×**, ELVA **24.9×**. Calian also has C$4.1m restricted cash within headline cash and C$5.2m earnouts: adding these to EV changes its multiple by about 0.1× before leases. These are screens, not complete acquisition valuations.

**Data correction:** Some vendor TSX EV fields mix CAD market capitalization with USD debt/earnings for VNP, ELVA, EFX and BDGI. Those displayed multiples were rejected and rebuilt in one currency. FTG's forward-EPS feed also looked stale relative to current results and was not used.

## Businesses, AI-spending risk and October 22 implementation

### What each company actually does

| Company | Business in plain English | Physical operating substance | Relationship to AI/data-center spending |
|---|---|---|---|
| **Badger Infrastructure** | Owns and operates hydrovac trucks that use pressurized water and vacuum to expose buried pipes and cables safely for utilities, municipalities, pipelines and construction customers. It also manufactures its trucks. | **High:** fleet, branches, truck manufacturing and field crews. | Mostly indirect. Grid and utility work may benefit from data centers, but the business also serves ordinary maintenance and construction. |
| **Calian** | Supplies specialized people and systems for military training, defence communications, satellites, cybersecurity/IT and healthcare staffing. | **Medium:** real systems and technical delivery, but much of the value is skilled services rather than owned plant. | Low direct dependence. Calian has delivered AI applications, but no material AI revenue was disclosed. |
| **Magellan Aerospace** | Manufactures aircraft-engine, aerostructure, defence and space components at plants in Canada, the United States and the United Kingdom. | **High:** factories, machining, engineering and long-qualified aerospace programs. | Little direct dependence identified. Results depend more on aircraft production and defence programs. |
| **Firan Technology** | Makes high-reliability printed circuit boards, illuminated cockpit panels and electronic assemblies for aerospace and defence customers. Qualification requirements make supplier switching difficult. | **High:** specialized manufacturing and qualified production processes. | No material AI business identified. Its main risks are aerospace cycles, customers and valuation. |
| **5N Plus** | Purifies specialty metals and converts them into high-purity semiconductor and performance materials used in space and terrestrial solar cells, medical imaging, electronics and industrial products. | **High:** materials processing and specialized production assets. | Semiconductor adjacency creates possible AI upside, but material AI/data-center revenue is unverified. |
| **Enerflex** | Builds and services natural-gas compression, gas-processing, refrigeration and power-generation systems, and owns recurring infrastructure assets. | **High:** engineered equipment, service network and infrastructure assets. | **Direct exposure:** more than 1.75GW of announced data-center power awards. This makes EFX the least suitable of the five purchases as protection from a collapse in data-center spending. |
| **Canaccord Genuity** | Runs wealth-management businesses and investment-banking, underwriting, advisory, trading and research operations. | **Low:** it is a people, balance-sheet and capital-markets franchise rather than a physical buildout company. | Tech financing is indirect exposure; capital-markets activity and asset values are the larger drivers. |
| **Electrovaya** | Designs lithium-ion battery systems. Current revenue is concentrated in batteries for forklifts and warehouses; a new factory and stationary/data-center batteries are planned. | **Medium/high:** battery engineering and manufacturing are physical, but the new capacity still needs orders and funding. | Prospective and speculative. Named material data-center orders were not verified. |

### AI-spending-collapse scenario

**ASSUMED judgment, not a forecast, floor or maximum loss.** The scenario is a collapse in data-center spending while the broader economy continues to function. It does not model a simultaneous recession or general equity crash. Every name can fall even when its underlying business has little AI exposure.

| Company | Expected temporary drawdown in that scenario | Five-year historical maximum drawdown, approximate | Interpretation |
|---|---:|---:|---|
| **Badger** | **−10% to −20%** | −31% | Best intersection of physical business, low direct AI dependence and relatively resilient demand. |
| **Calian** | **−10% to −20%** | −44% | Diversified government/health/technical work should limit direct AI sensitivity; cash conversion and valuation remain risks. |
| **Magellan** | **−10% to −25%** | −35% | Physical aerospace franchise with little direct AI dependence; aircraft cycle, cash conversion and control risk remain. |
| **FTG** | **−20% to −35%** | −40% | AI-independent physical business, but a high multiple and temporary pricing premiums create compression risk. |
| **5N Plus** | **−20% to −35%** | −65% | Physical specialty-materials business, but semiconductor association, customer concentration and working-capital needs can amplify a selloff. |
| **Canaccord** | **−20% to −35%** | −60% | Optically inexpensive, but financial-market beta and nonphysical business make it a poor fit for the stated screen. |
| **Enerflex** | **−25% to −40%** | −53% | Cheap on current EBITDA, but its announced data-center awards create direct sensitivity to the specified risk. |
| **Electrovaya** | **−40% to −60%** | −64% | Small, cash-consuming and diluted; planned data-center products add expectation risk before material revenue exists. |

The October 22 valuation refresh, using the same one-currency method as the main report, produced approximate trailing EV/EBITDA of **6.2× EFX, 10.6× CGY, 10.5× BDGI, 21.2× FTG, 16.8× VNP, 13.0× MAL and 24.5× ELVA**. Canaccord was about **9.1× trailing adjusted EPS** but roughly 13.6× an assumed C$1.00 mid-cycle EPS. These are screens, not intrinsic values. Under the later preference for low AI-spending dependence, **Badger became the strongest overall fit; Calian remained relatively resilient; Enerflex remained the cheapest but failed the anti-AI screen.**

### User-confirmed purchases on October 22, 2026

Gross notional is before any unreported commissions, fees or FX effects. The two Calian fills are aggregated in the holdings table but retained separately here for account provenance.

| Security | Account | Shares | Fill | Gross CAD notional |
|---|---|---:|---:|---:|
| Calian (`CGY.TO`) | Questrade Cash | 5 | C$84.88 | C$424.40 |
| Calian (`CGY.TO`) | Questrade RRSP | 6 | C$84.93 | C$509.58 |
| Enerflex (`EFX.TO`) | Questrade RRSP | 60 | C$32.64 | C$1,958.40 |
| Badger (`BDGI.TO`) | Questrade RRSP | 25 | C$83.84 | C$2,096.00 |
| 5N Plus (`VNP.TO`) | Questrade RRSP | 80 | C$26.56 | C$2,124.80 |
| Firan Technology (`FTG.TO`) | Questrade RRSP | 60 | C$34.47 | C$2,068.20 |
| **Total** |  |  |  | **C$9,181.38** |

Calian is now **11 shares at C$84.9073 weighted average**, with C$933.98 aggregate basis. RRSP cash was reduced by **C$8,756.98** and Cash-account CAD by **C$424.40**. The live sheet preserves the resulting balances rather than inventing a funding or FX transaction.

### Provisional existing-sleeve mapping

| Security | Existing sleeve | Why it fits | Classification limitation |
|---|---|---|---|
| **CGY** | `Defense` | Military training, defence communications and government technical work are the closest portfolio role. | Healthcare and commercial technical services mean it is not a pure defence company. |
| **FTG** | `Defense` | Aerospace/defence electronics, qualified programs and allied military demand. | Commercial aerospace is also material. |
| **EFX** | `oil-companies` | Gas compression, processing and power equipment share the portfolio's energy-cycle and gas-infrastructure risk. | It is an equipment/infrastructure provider rather than a producer; a future energy-equipment label could be cleaner. |
| **BDGI** | `grid/electrification` | Hydrovac work enables utility, pipeline and buried-infrastructure construction and maintenance. | It is neither a regulated utility nor an electrical-equipment maker; this is the closest economic role. |
| **VNP** | `industrial_metals` | Converts specialty metals into advanced materials, giving the closest link to the materials sleeve. | It is a processor/manufacturer rather than a miner or broad metals producer. |

These mappings are **provisional classifications, not target increases**. No `Build Canada` sleeve was created and no allocation target changed. `Build Canada` is currently better treated as a geography/policy theme across economic risks; making it a sleeve would mix defence, energy equipment, infrastructure and specialty materials and could hide the portfolio's true factor concentrations. That taxonomy decision remains open for discussion.

## Canadian buildout and currency exposure

**VERIFIED [P1–P4]:** Canada's One Canadian Economy/Building Canada Act framework and Major Projects Office establish project-acceleration mechanisms. The September 29 government release reports a **C$33bn final investment decision for LNG Canada Phase 2**, targeting combined capacity of 28 million tonnes annually, and related Coastal GasLink compression investment. The October 1 Pacific Link national-interest listing is an earlier milestone, with conditions review targeted for September 2027. Government jobs/GDP projections remain forecasts.

**ASSUMED transmission:** policy → financed project → supplier order → profitable delivery → cash after reinvestment → value per share. A national-interest listing, investment decision, order and recognized revenue are different stages. Patriotism cannot replace that chain.

| Company | Verified geography / operating mix | Interpretation for Build Canada |
|---|---|---|
| Calian | Canada **63% of nine-month FY2026 revenue** | Best domestic customer exposure; includes health/IT/defence, not just construction |
| Enerflex | FY2025 Canada **13%**, U.S. **45%** of revenue | Canadian gas investment plus global/NA equipment and services |
| Badger | U.S. **79% of fleet / 81% of staff**; Canadian truck manufacturing | Mostly U.S. infrastructure, with a Canadian supply-side benefit |
| FTG | Nine-month Canada **7.1%**, U.S. **70.9%** of revenue; substantial Canadian operations | Canadian manufacturing/export and allied aerospace more than domestic sales |
| 5N Plus | H1 U.S. **49.4%**; Canada within a 3.5% other-Americas category | Global materials/space opportunity, not a domestic construction proxy |
| Magellan | H1 **66.4% commercial aerospace / 33.6% defence** | Canadian procurement optionality plus large aircraft-production exposure |
| Canaccord | FY2026 Canada **34.7%** of revenue | Indirect financing/wealth effects; no physical buildout |
| Electrovaya | Nine-month U.S. **96.4%**, Canada **1.5%**; expansion in New York | Primarily U.S. warehouse batteries and prospective storage |

**ASSUMED:** Low domestic revenue does not rule out Canadian industrial-policy benefits: factories and exports can gain. Conversely, a stronger CAD can reduce exporters' translated revenue or margins. CAD listing does not guarantee CAD purchasing-power protection; known CAD liabilities need separate currency planning.

## Company evidence

### Enerflex — best value/AI combination; missing contract economics

**VERIFIED [E1–E3]:** Q2 revenue US$582m declined 5.4%; adjusted EBITDA US$128m versus US$130m. H1 revenue was essentially flat but EBITDA improved. Trailing adjusted EBITDA **US$533m = 511 + 265 − 243**. Financial net debt US$455m and Q2 issuer ROCE 15.4%. Recurring infrastructure assets and aftermarket services complement variable engineered-system projects.

October 1/13 releases identify a 450MW award and over 1GW of additional data-center power awards, taking these projects' backlog above **1.75GW**, with deliveries through 2028. Capacity spending authorized was about **US$100m**, US$15m in 2026 and most of the rest in 2027. These are announced awards, not just conversations; the AI-specific fraction is undisclosed.

At US$24.16, equity is about US$2.95bn and financial EV US$3.41bn: **6.4× EBITDA**. Trailing company-defined FCF is about US$231m, a **7.8% yield**; conventional CFO less relevant asset capex about US$238m. Issuer FCF adds disposal proceeds and deducts lease principal and mandatory debt repayments; neither is automatically recurring distributable cash. Future factory/working-capital spending can reduce cash. Reported trailing EPS is only about US$0.44, reflecting debt-redemption costs and SBC volatility; adjusted metrics must not make real costs disappear. H1 SBC US$41m versus nil includes share-price-sensitive cash/liability-linked awards.

**ASSUMED verdict:** Attractive relative value and most concrete data-center exposure. Still overlaps gas/capital-spending risks. MW cannot reliably become profit or fair value without prices, margins, scope, payment/cancellation terms and customer funding. Prefer a valuation cushion or stronger economics disclosure. Cancellation, persistent cash absorption or leverage without adequate returns would weaken the case.

### Calian — best domestic fit; conventional cash flow is the test

**VERIFIED [C1–C3]:** Q3 revenue C$230.4m grew 19.9%, including **16% organic growth**. Adjusted EBITDA C$25.6m, 11.1% margin. Trailing revenue C$870.3m, adjusted EBITDA C$100.5m, financial net debt C$94.9m. Eight of nine directors, including the chair, are independent; no identified insider controller. Technical qualifications, skilled labour and established contracts support quality, though acquisitions complicate return-on-capital assessment.

Backlog **C$1.448bn**, with roughly C$1bn defence: about **69% all-defence**, not proof of the interview's over-60% **Canadian-defence** claim. Backlog includes options/adjustments. Firm remaining performance obligations C$1.248bn, about 56% expected within 24 months. The subsequent C$296m British Army contract spans 15 years and is not Canadian procurement. Long backlog cannot all be counted as next-year revenue.

AI examples include delivered Canadian Space Agency satellite anomaly detection, NATO training applications and an assistant product. AI capability is real; material separately disclosed AI revenue/profit is **UNVERIFIED**.

**VERIFIED cash distinction:** Trailing CFO minus capex **C$26.3m**, or **2.75% market-value yield before lease principal**. Issuer “operating free cash flow” C$72.2m removes working-capital effects/acquisition costs and does not deduct capex. Nine-month actual CFO C$31.6m minus capex C$8.4m and lease principal C$5.0m leaves about C$18.3m. Goodwill/acquired intangibles C$323.5m, about 43% of assets; largest customer 40% of nine-month revenue.

**ASSUMED verdict:** Plausible partial substitute for intended defence exposure. Approximately **18.7× adjusted / 25× reported earnings** is not an obvious bargain when cash conversion is weak. Organic growth converting into cash is more decisive than promotional backlog. Persistent working-capital absorption, delayed contracts or impaired acquisitions would reverse the positive view.

### Badger — useful infrastructure franchise; high reinvestment needs

**VERIFIED [B1–B2]:** Q2 revenue US$257.1m rose 23% organically, adjusted EBITDA US$66.1m rose 25%, margin 25.7%. Revenue per truck +14%; fleet +8% to 1,822. Branch density, scale and truck manufacturing help; local competition, labour, safety and utilization still determine economics.

At C$86.81, **10.8× EBITDA / 28.6× adjusted earnings**. Trailing CFO less capex about US$13.5m, only **0.65% yield**. H1 CFO US$65.3m versus capex US$100.2m: negative US$35m. Guided 2026 capex US$170–200m plus tariffs US$18–30m excludes a second U.S. factory. Growth capex can be productive, but EBITDA is not harvestable cash. Share-price-linked compensation/derivative offsets complicate earnings.

**ASSUMED verdict:** Third watchlist candidate, a broader infrastructure business than another producer, but predominantly U.S. and priced for growth. AI utility-excavation exposure is indirect and unquantified. Require attractive incremental returns and cash improvement. Quantitative safety trends were not established: a diligence gap, not evidence of unsafe operations.

### FTG — differentiated business; do not annualize temporary pricing

**VERIFIED [F1–F3]:** Q3 revenue C$64.1m +34.3%; gross margin **42.9% versus 30.3%**; adjusted EBITDA C$15.1m. Qualification and switching barriers support aerospace electronics. Backlog **C$220.7m versus C$148.5m** at year-end, 84.8% expected within one year; book-to-bill 1.41.

The filing explicitly attributes part of margin strength to **short-term pricing premiums**, without quantifying their size/persistence. Top five customers about 52% of annual sales. Commercial aircraft, allied defence and China-linked civil aerospace bring different cycles/trade risks. Financial net cash before leases; five of six directors independent, with meaningful CEO/major-holder ownership.

**ASSUMED verdict:** Among the more attractive specialist businesses, but **20.3× EBITDA / 37.6× reported earnings** leaves little room for margin normalization. No material AI business established. Wait for a better price or demonstrated sustainable earnings growth. The worker's approximate TTM FCF bridge mixed annual/interim definitions, so it is excluded from comparable cash-yield claims.

### 5N Plus — real niche, with margin and customer concentration risks

**VERIFIED [V1–V2]:** Q2 revenue US$122.4m +28.4%, but adjusted gross margin **30.3% versus 34.6%**; EBITDA US$26.6m grew only about 10%. Reported income benefited from US$6.0m SBC recovery; adjusted income was slightly lower year over year. H1 CFO negative US$15.4m after US$48.1m working-capital use; capex/intangibles bring outflow to about US$32.5m.

Specialized purification, semiconductor materials and space/terrestrial solar applications are credible advantages. **One customer 36% of revenue**. Backlog about US$420m, with a defined one-year semiconductor horizon. Most non-current assets are in Germany. This is not simply mining; material AI/data-center revenue is **UNVERIFIED**.

**ASSUMED verdict:** Quality-growth watchlist at **17.3× trailing EBITDA**, about 17.4× annual guidance midpoint US$102.5m. A share-price decline does not establish cheapness. The interview's $550m/$1bn revenue discussion (currency unstated) needs horizon, margin, capital and dilution assumptions; revenue alone is insufficient. Require margin recovery and working-capital release.

### Magellan — genuine aerospace franchise, weaker cash/governance

**VERIFIED [M1–M3]:** Q2 revenue C$305.6m +22.3%; adjusted EBITDA C$43m, 14.1% margin. Qualification and program relationships matter. Two customers about 35% of revenue; commercial aerospace two-thirds of H1 sales. Canadian defence opportunities include teaming/MOUs, not all valued firm orders.

Trailing CFO C$35.7m below capex C$58.8m: **negative C$23m** before intangible spending/lease principal. H1 working capital used C$55.9m. Financial leverage limited. **Murray Edwards controls about 75.4%**; four of six directors independent, non-independent chair, no independent lead identified, controlled-company features and related-party consulting arrangements. Control can encourage patience but limits minority influence.

**ASSUMED verdict:** **12.9× adjusted EBITDA / 31.7× earnings** prices progress despite weak cash. The interview's higher-margin forecast remains a forecast. Below CGY/FTG in priority; require cash conversion, firm contract economics and compensation for control risk. No material AI business identified.

### Canaccord — cheap adjusted earnings, complicated realization

**VERIFIED [G1–G3]:** Q1 FY2027 adjusted revenue C$577.4m +28.8%; EPS C$0.36 versus C$0.13. Wealth client assets C$160.2bn. Approximate trailing adjusted diluted EPS **C$1.49 = 1.26 + .36 − .13**, or **9.0× P/E**; trailing IFRS EPS approximately **−C$1.05**. Compensation about 63% of revenue. Annual adjusted EPS has varied widely; recent results are not proven mid-cycle earnings.

Wealth fees recur; banking/trading are cyclical. Metals represented 51% of FY2026 underwriting revenue. Tech financing is not an operating AI franchise. Governance diligence includes significant employee/insider loans, a failed 2023 management take-private and disclosed U.S. AML settlement with US$75m paid / US$5m suspended. These raise economic/governance concerns without alleging additional wrongdoing.

**UNVERIFIED catalyst:** No signed UK wealth-sale terms identified through October 20. CF owns about **66.9% as converted**, alongside preference/management claims, debt and liquidation priorities. Gross 100%-business value is not CF common proceeds. Taxes, costs, incentives and residual capital matter. August releases concern an acquisition and preferred redemption, not a completed wealth sale.

**ASSUMED verdict:** Possible value special situation, not core industrial buildout. At assumed C$1.00 mid-cycle EPS it is **13.5×**, and at C$0.80 **16.8×**. Cheapness depends on durable earnings or actual attributable value realization. Require normalized earnings work or signed transaction economics.

### Electrovaya — optionality with the highest underwriting burden

**VERIFIED [L1–L3]:** Q3 revenue US$17.7m grew only 3.4%; nine-month +18.5%. Two customers **88% of Q3 / 70% of nine-month sales**. Virtually all current revenue is batteries, principally material handling. Nine-month CFO negative US$17.4m and investing cash negative US$22.1m. Basic shares +18.7% in nine months. A new factory creates capacity, not guaranteed utilization or triple revenue.

October update targets ElvaPulse certification Q1 calendar 2027, deliveries Q2. Named data-center orders and material financial contribution remain **UNVERIFIED**. Current price implies **24.7× EBITDA / 60.7× reported earnings**, requiring substantial growth.

**VERIFIED Amazon mechanics:** 13,880,345 warrants, exercise price **US$8.565**, expiry July 2036. **5,545,880 vest immediately**; remaining **8,334,465** vest with Amazon future cumulative purchases, fully at **US$280m**. This is **not guaranteed sales; exercise is not automatic conversion**. Currently out of the money. Full cash exercise adds about 27.8% of current basic shares, or 21.7% of post-issue shares, and up to US$118.9m cash. Ignoring either dilution or proceeds misstates economics.

**ASSUMED verdict:** Potentially large upside does not imply reliable underwriting. Weakest fit while existing speculation is over limit. Revisit certification, named orders, funding/cash runway and fully diluted per-share economics. A lower price alone does not resolve business risk.

## Valuation sensitivities

**ASSUMED, not fair-value targets, predicted lows or automatic buy orders.** Hold current trailing EBITDA, financial net debt, shares and FX constant, and apply more conservative multiples selected by the researcher. These are judgments reflecting cyclicality/uncertainty, not empirically established fair multiples. Future growth, future cash, debt changes and dilution are excluded.

| Company | Assumed EV/current EBITDA | Implied price | Evidence needed to pay more |
|---|---:|---:|---|
| Enerflex | 5–6× | **US$18.10–22.46** | Profitable orders, funding/payment terms and cash conversion |
| Calian | 8–9× | **C$61.60–70.34** | Organic growth turning into conventional cash |
| Badger | 8–10× | **C$61.54–79.58** | Returns on incremental fleet/factory investment |
| FTG | 14–16× | **C$22.84–26.09** | Margins sustainable without temporary premiums |
| 5N Plus | 12–14× | **C$19.01–22.24** | Margin recovery and verified profitable growth |
| Magellan | 9–11× | **C$22.95–28.15** | Cash conversion and minority-shareholder returns |
| Electrovaya | 12–15× | **US$2.34–3.06** | Commercial validation, funding and per-share growth |

Canaccord: C$1.00 assumed normalized EPS at 9–11× implies **C$9–11**; C$1.49 at the same multiples **C$13.41–16.39**. That denominator uncertainty is the investment question. UK valuation needs an attributable, after-tax sum of parts, not a gross transaction headline.

**Red team:** Waiting for these ranges could miss sustained earnings growth. Equally, prices could fall because earnings are impaired, making unchanged-earnings ranges too high. An illustrative EFX bear case—EBITDA −20%, multiple 5×, unchanged debt/shares—implies **US$13.73**, about **43% below** US$24.16. This is a scenario, not forecast or maximum loss. Relative cheapness does not mean capital safety.

## Interview and manager credibility

October 15 episode: **Canada Is Finally Waking Up. These Stocks Could Soar**, Amber Kanwar interviewing Andrey Omelchak [I1]. Official full transcript unavailable. Publisher public audio was recovered and relevant sections locally transcribed: opening/Canada, VNP/ELVA, FTG, past/current pro picks. This is **partial ASR**, not an official transcript or a claim to have watched every minute. Names/units sometimes transcribe incorrectly; important claims were checked against primary filings.

| Interview proposition, paraphrased | Finding |
|---|---|
| EFX has major data-center power wins | **VERIFIED:** >1.75GW announced backlog; economics missing |
| CGY over 60% Canadian-defence backlog | **UNVERIFIED geography:** ~69% all-defence supported |
| FTG backlog and revenue growth; further acceleration | **VERIFIED recent growth; ASSUMED further acceleration:** temporary pricing limits extrapolation |
| VNP can become much larger | **ASSUMED forecast:** numerical valuation/horizon not supplied |
| ELVA factory triples revenue; storage upside | **ASSUMED forecast:** capacity is not orders or profit |
| Amazon warrants convert after US$280m sales | **REVISE:** purchase-linked vesting, strike, elective exercise; no sales guarantee |
| CF UK monetization unlocks value | **UNVERIFIED outcome:** no signed sale; guest acknowledges delay |
| Canada opportunity has almost no downside | **Reject as risk underwriting:** equity/project/valuation risks persist |
| LionGuard beat TSX and Nasdaq | **UNVERIFIED:** no reproducible fund/class/period/currency/fee basis |

**Credibility judgment — ASSUMED, moderate confidence:** Omelchak appears to be a credible professional manager worth considering as an idea source. LionGuard biography reports founder since 2014, prior Montrusco Bolton portfolio management and CFA/FRM/graduate credentials [I2]. Those details are self-reported; designation membership was not independently authenticated. **Walter Global Asset Management independently announced a minority investment/capital partnership in 2019 [I3]**, corroborating a real institutional business. Listed service providers include TD Securities, PwC and SGGG, but their engagements/audit reports were not obtained.

**Limits:** Firm-stated registration categories were found; current regulator lookup and a comprehensive disciplinary check were not completed because the lookup was inaccessible. No clean regulatory bill of health is claimed. Audited net fund returns were not obtained; investor access requires Canadian-resident/accredited-investor certification, which was not submitted for this California-resident user. Institutional backing establishes credibility, not investment skill.

The guest acknowledges mistakes/valuation: slower CF monetization, position reduction, and trimming Bird after appreciation while still liking the business. That is useful discipline. Nevertheless, key “cheap” claims depend on earnings two or three years ahead without a reproducible numerical bridge. The interview is a hypothesis source, not independent valuation evidence.

## Past picks

**VERIFIED pick sets [I4–I6]; reproducible secondary-market return estimates.** All three names from each of four documented appearances were included. January comes from BNN's June past-picks table, March from the publisher episode, April from LionGuard's dated BNN recap, June from the full BNN article. This is not a complete career archive.

Recommendation-date close through **October 20 close**, vendor adjusted prices as total-return proxies, **CAD**. USD-listed Civeo translated using endpoint CADUSD. Benchmark **XIC.TO** over identical dates. Equal weights are illustrative, not actual fund positions/trades; no fees, taxes or execution costs. Closing-price convention may not match a viewer's tradable entry.

| Appearance | Complete three-name set and CAD total-return estimates | Equal-weight basket | XIC |
|---|---|---:|---:|
| Jan 16 | **Bird +149.4%; Trisura −8.9%; Electrovaya −44.8%** | **+31.9%** | +11.0% |
| Mar 3 | **Calian −0.3%; Canaccord +4.4%; Bird +128.8%** | **+44.3%** | +8.2% |
| Apr 22 | **Magellan +25.2%; Stingray −1.9%; Black Diamond +9.2%** | **+10.8%** | +7.4% |
| Jun 26 | **Badger −8.1%; Magellan +3.0%; Civeo −17.3%** | **−7.5%** | +3.9% |

**ASSUMED interpretation:** Some successful selection, especially Bird, alongside substantial losers and recent underperformance. Repeated Bird/Magellan events are not independent. Small accessible sample, unequal periods, no risk adjustment or real position sizing: insufficient to establish persistent skill or an audited record. Do not combine overlapping baskets into a purported fund return. The episode's percentage changes use a different endpoint; differences from this table do not establish an error. Short-term losses do not disprove a multiyear thesis either.

## Portfolio fit and next validation

**VERIFIED stored live-sheet context:** oil companies **7.8% vs 6% target**; natural gas **2.8% vs 1%**; nuclear **3.6% vs 3.5%**; grid **1.5% vs 1.5%**; speculation **2.5% vs 1.5%**, also above its US$10,000 cap. Defence **0.45% vs 1.5%**. Existing CNQ, Canadian gas, Cameco, BWXT, GEV/ETN and SHLD already express several themes. Economic look-through overlaps labels.

**PROPOSAL — NOT ACCEPTED:**

1. **EFX and CGY lead; BDGI is next watch.** Prefer a considered choice of one or two over eight additional positions. This research does not establish an exact size.
2. **EFX should compete within existing energy/equipment risk.** Directness of gas/power orders improves the thesis relative to generic oil exposure, but does not justify increasing overweight aggregate energy. Compare incumbent quality and tax lots before selecting any replacement; no specific sale inferred.
3. **CGY could replace part of planned SHLD buying.** This trades ETF diversification for company/customer/acquisition risk and includes non-defence businesses. Do not count the whole ETF plan and a new CGY allocation as separate unused budgets. Current cash conversion argues for patience or stronger evidence.
4. **Do not add ELVA as “safe AI infrastructure.”** Current business/funding risks belong in speculation, already over its limits and under user-directed conditional exits.
5. **Keep reserves and currency design separate.** A house may become attractive in a recession when these stocks and job income weaken. CAD250k helps but does not make equities reliable CAD purchasing power. Existing diversified funds remain the default alternative if candidates fail valuation/fit tests.

The October 14 proposal remains unresolved. No broker eligibility, lot-level tax, withholding, PFIC, RRSP or account-placement decision was made here. A U.S. listing does not by itself change the issuer's underlying business or tax characteristics; verify those at actual implementation.

**Contrary case:** Stronger Canadian/allied investment and AI power demand may lift earnings fast enough to justify VNP/FTG prices, commercialize ELVA, or realize CF value. Refusing all forecast growth would also be an error. **Bear case:** approvals fail to become supplier cash; trade/U.S. demand weakens; pricing premiums reverse; reinvestment absorbs profits; CAD squeezes exporters; concentrated small stocks suffer multiple compression. Procurement backlog is not a recession guarantee.

**Next cheap verification:** EFX next filing for order economics, margins, payment/working capital and leverage; CGY actual CFO/capex/leases and Canadian-defence geography; BDGI fleet/factory returns, utilization and safety; FTG normalized premiums; VNP margins/customer/cash; MAL cash/minority returns; CF signed attributable deal proceeds or normalized earnings; ELVA certification, named orders and fully diluted funded model. Changes in fundamentals require recalculating price sensitivities.

**Stopping rule reached:** further generic searches are unlikely to resolve undisclosed economics, future certifications or user budget choices. Comparative research is complete at the stated confidence. Reopen at a disclosure gate or user request; no further research/trade automatically scheduled.

## Sources

Sources were opened by workers and/or root; root independently checked pivotal EFX orders, ELVA warrants/update, Calian cash/backlog, FTG pricing, policy, manager and past picks. Dates below are publication dates; source metadata also records retrieval/period. Raw evidence and limitations are indexed below.

### Issuers

- **T1 — November 5–6 execution timing, retrieved Nov 7, 2026:** Yahoo Finance unadjusted daily
  and five-minute OHLC for [EFX.TO](https://finance.yahoo.com/quote/EFX.TO/history/),
  [FTG.TO](https://finance.yahoo.com/quote/FTG.TO/history/),
  [CGY.TO](https://finance.yahoo.com/quote/CGY.TO/history/),
  [BDGI.TO](https://finance.yahoo.com/quote/BDGI.TO/history/) and
  [VNP.TO](https://finance.yahoo.com/quote/VNP.TO/history/). Secondary vendor data; exact user fills
  control execution prices, and the saved `fin_check` snapshot is the independent internal
  cross-check for November 6 daily moves.

- **E1 — Enerflex Q2, Aug 6, 2026:** [release](https://www.sec.gov/Archives/edgar/data/1904856/000190485626000002/efxt-ex99_1.htm), [statements](https://www.sec.gov/Archives/edgar/data/1904856/000190485626000002/efxt-ex99_2.htm), [MD&A](https://www.sec.gov/Archives/edgar/data/1904856/000190485626000002/efxt-ex99_3.htm).
- **E2 — Enerflex FY2025, Feb 25, 2026:** [statements](https://www.sec.gov/Archives/edgar/data/1904856/000119312526072743/efxt-ex99_2.htm), [MD&A](https://www.sec.gov/Archives/edgar/data/1904856/000119312526072743/efxt-ex99_3.htm).
- **E3 — Enerflex awards:** [Oct 1](https://www.sec.gov/Archives/edgar/data/1904856/000119312526410172/efxt-ex99_1.htm), [Oct 13](https://www.sec.gov/Archives/edgar/data/1904856/000119312526419999/efxt-ex99_1.htm). MW/delivery/capex, not complete economics.
- **C1 — Calian Q3, Aug 12, 2026:** [combined filing](https://investors.calian.com/app/uploads/sites/2/2026/02/Q3-FY26-Combined-PR-FS-and-MDA.pdf). URL folder date differs from document date.
- **C2 — Calian:** [FY2025 annual report](https://investors.calian.com/app/uploads/sites/2/2025/02/Calian-AR-2025-FINAL.pdf), [2025 circular](https://investors.calian.com/app/uploads/sites/2/2026/01/Calian_CIR_2025-WEB.pdf).
- **C3 — Calian:** [AI applications](https://www.calian.com/ai-innovation/), retrieved Oct 20; use cases, not financial materiality.
- **B1 — Badger Q2, Jul 30, 2026:** [release](https://s201.q4cdn.com/142671057/files/doc_earnings/2026/q2/earnings-result/Audit-Earnings-Release-Q2-2026.pdf), [MD&A](https://s201.q4cdn.com/142671057/files/doc_earnings/2026/q2/generic/MDA-Q2-2026-FINAL.pdf), [statements](https://s201.q4cdn.com/142671057/files/doc_earnings/2026/q2/supplemental-info/Badger-Financial-Statements-Q2-2026-FINAL.pdf).
- **B2 — Badger FY2025, Mar 5, 2026:** [release](https://s201.q4cdn.com/142671057/files/doc_earnings/2025/q4/earnings-result/Audit-Earnings-Release-Q4-2025.pdf), [MD&A](https://s201.q4cdn.com/142671057/files/doc_earnings/2025/q4/generic/Audit-3b-MDA-Q4-2025-FINAL.pdf), [AIF](https://s201.q4cdn.com/142671057/files/doc_earnings/2025/q4/generic/Annual-Information-Form-2025.pdf).
- **F1 — FTG Q3, Oct 7, 2026:** [report](https://www.ftgcorp.com/wp-content/uploads/2026/10/FTG-Q3-2026-Report_FINAL.pdf), period ended Aug 28.
- **F2 — FTG FY2025, Feb 18, 2026:** [annual report](https://www.ftgcorp.com/wp-content/uploads/2026/02/Annual-Report_FINAL-FTG-2025.pdf), [AIF](https://www.ftgcorp.com/wp-content/uploads/2026/02/AIF_FINAL-FTG-2025.pdf).
- **F3 — FTG, Mar 2026:** [circular](https://www.ftgcorp.com/wp-content/uploads/2026/03/FTG-2025-Circular_v04.pdf).
- **V1 — 5N Plus Q2, Aug 3, 2026:** [statements](https://www.5nplus.com/media/uploads/documents/b2026-08-03__q2-2026_financial_statements.pdf), [MD&A](https://www.5nplus.com/media/uploads/documents/b2026-08-03__q2_2026_mda.pdf).
- **V2 — 5N Plus FY2025, Feb 24, 2026:** [annual report](https://www.5nplus.com/media/uploads/documents/b5n_plus_inc._-_2025_annual_report.pdf).
- **M1 — Magellan Q2, Aug 12, 2026:** [issuer interim filing](https://app.quotemedia.com/data/downloadFiling?webmasterId=101020&ref=6a7cdfe1bc50353f3c734747&type=PDFC&symbol=MAL%3ACA&companyName=Magellan+Aerospace+Corporation&formType=002-002-001130-016004&formDescription=Interim+financial+statements%2Freport&dateFiled=2026-08-12).
- **M1 supplementary — Magellan Q2, Aug 12:** [MD&A](https://app.quotemedia.com/data/downloadFiling?webmasterId=101020&ref=6a7cdfe0bc50353f3c734745&type=PDFC&symbol=MAL%3ACA&companyName=Magellan+Aerospace+Corporation&formType=002-002-001097-001004&formDescription=MD%26A&dateFiled=2026-08-12), [release](https://app.quotemedia.com/data/downloadFiling?webmasterId=101020&ref=6a7ce0d7bc50353f3c73475a&type=PDFC&symbol=MAL%3ACA&companyName=Magellan+Aerospace+Corporation&formType=002-002-001089-003001&formDescription=News+release&dateFiled=2026-08-12). Adjusted EBITDA and operating mix.
- **M2 — Magellan, Mar/Apr 2026:** [annual report](https://magellan.aero/wp-content/uploads/2025%20Annual%20Report.pdf), [circular](https://magellan.aero/wp-content/uploads/Magellan%20Information%20Circular-1.pdf).
- **M3 — Magellan, Feb 12, 2026:** [torpedo teaming agreement](https://magellan.aero/2026/02/tkms-and-magellan-sign-teaming-agreement-to-support-heavyweight-torpedo-production-and-in-service-support-for-the-canadian-patrol-submarine-project/). Teaming is not a valued procurement award.
- **M3 supplementary — Magellan, July 2026:** [M72 award, Jul 20](https://app.quotemedia.com/data/downloadFiling?webmasterId=101020&ref=6a5e93828ee5ef756747f590&type=PDFC&symbol=MAL%3ACA&companyName=Magellan+Aerospace+Corporation&formType=002-002-001089-003001&formDescription=News+release&dateFiled=2026-07-20), [conditional F414 MOU, Jul 22](https://app.quotemedia.com/data/downloadFiling?webmasterId=101020&ref=6a6130c7e02cb6760a7036d7&type=PDFC&symbol=MAL%3ACA&companyName=Magellan+Aerospace+Corporation&formType=002-002-001089-003001&formDescription=News+release&dateFiled=2026-07-22). Distinguish awarded-but-unvalued work from a conditional program opportunity.
- **G1 — Canaccord Q1 FY2027, Aug 6:** [quarterly report](https://www.canaccordgenuity.com/4a2414/globalassets/investor-relations/documents/financial-reports-en/2027/q1-fiscal-2027-quarterly-report.pdf).
- **G2 — Canaccord FY2026, Jun 2026:** [annual report](https://www.canaccordgenuity.com/49bdbc/globalassets/investor-relations/documents/financial-reports-en/2026/q4/canaccord-2026-annual-report.pdf), [circular](https://www.canaccordgenuity.com/49eaec/globalassets/investor-relations/documents/financial-reports-en/2026/q4/english-2026-management-information-circular-canaccord-genuity-group-inc..pdf).
- **G3 — Canaccord:** [release archive](https://www.canaccordgenuity.com/investor-relations/news-and-events/press-releases/), checked Oct 20. Evidence JSON indexes August acquisition/redemption and 2021 HPS structure. No signed sale located; private discussions are not ruled out.
- **L1 — Electrovaya Q3, Aug 10, 2026:** [statements](https://www.sec.gov/Archives/edgar/data/1844450/000165495426007467/elva_ex991.htm), [MD&A](https://www.sec.gov/Archives/edgar/data/1844450/000165495426007467/elva_ex992.htm), [FY2025 statements](https://www.sec.gov/Archives/edgar/data/1844450/000175392625001917/g085039_ex99-2.htm).
- **L2 — Electrovaya, Oct 8:** [Amazon warrants](https://www.sec.gov/Archives/edgar/data/1844450/000175392626001916/g085983_suppl.htm).
- **L3 — Electrovaya, Oct 14:** [business update](https://www.sec.gov/Archives/edgar/data/1844450/000165495426008942/elva_ex991.htm); forward-looking product timing.

### Policy, interview and manager

- **P1 — Canada:** [One Canadian Economy](https://www.canada.ca/en/one-canadian-economy.html), modified Sep 9, 2026.
- **P2 — Canada:** [Major Projects Office](https://www.canada.ca/en/privy-council/major-projects-office.html), modified Oct 1, 2026.
- **P3 — Prime Minister, Sep 29:** [LNG Canada Phase 2 investment decision](https://www.pm.gc.ca/en/news/news-releases/2026/09/29/prime-minister-carney-welcomes-lng-canada-phase-2-second-largest).
- **P4 — Prime Minister, Oct 1:** [Pacific Link listing](https://www.pm.gc.ca/en/news/news-releases/2026/10/01/prime-minister-carney-lists-west-coast-oil-pipeline-now-known-pacific).
- **I1 — In the Money, Oct 15:** [YouTube](https://www.youtube.com/watch?v=FErNU1mQwEM&t=3365s), [publisher episode](https://share.transistor.fm/s/93346c09), [public audio](https://media.transistor.fm/93346c09/4739a72c.mp3). Partial ASR provenance preserved.
- **I2 — LionGuard, retrieved Oct 20:** [biography](https://www.lionguardcapital.com/team/andrey-omelchak/), [firm/service providers](https://www.lionguardcapital.com/about/), [registration statements](https://www.lionguardcapital.com/legal-disclaimer/), [investor access](https://www.lionguardcapital.com/investor-gate/). Self-reported, not audited returns.
- **I3 — Walter Global Asset Management, May 1, 2019:** [minority partnership](https://walter-gam.com/en/news/lionguard-capital-management-set-to-accelerate-growth-through-new-partnership-with-walter-global-asset-management). Counterparty corroboration of business, not performance.
- **I4 — BNN Bloomberg, Jun 26, 2026:** [June picks and January past picks](https://www.bnnbloomberg.ca/markets/2026/06/26/andrey-omelchaks-top-picks-for-june-26-2026/); original includes financial-interest disclosures.
- **I5 — In the Money, Mar 3:** [Calian, Bird and Canaccord episode](https://share.transistor.fm/s/cb9b09e2).
- **I6 — LionGuard, Apr 23:** [April 22 BNN recap](https://www.lionguardcapital.com/bnn-market-call-andrey-omelchaks-top-picks-for-april-22-2026-2/). Pick-set evidence, not audited results.

## Durable artifacts and reproduction

Real checkout **`/home/colligo/hs_scripts`** is under Hooman's specified backed-up home location. Needed artifacts are under home; `/mnt/localssd` is volatile scratch, not their only location. This verifies location, not an independent off-host restore test.

| Full absolute path | Purpose |
|---|---|
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/SUMMARY.md` | Canonical synthesis |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/valuation_comparison.json` | Financial inputs, normalized EV and sensitivities |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/valuation_comparison.csv` | Flat calculation output |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/scripts/compare_valuations.py` | Offline arithmetic and 12-event return checks |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/quotes.json` | Dated vendor quotes/FX/history; vendor EV ratios rejected |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/execution_timing_2026-11-05_06.csv` | User fills, Nov. 3/5/6 OHLC, review levels and reproducible timing differences |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/live_portfolio.json` | Private read-only holdings/marks/formulas; not for public distribution |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/past_picks.json` | All 12 events and raw price/dividend/split histories |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/past_pick_cohorts.json` | Four separately measured baskets; overlapping periods |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/scripts/past_picks.py` | Network retrieval/return method; later runs may reflect vendor corrections |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/materials_batteries/findings.json` | VNP/ELVA claim/source records; raw filings beside it |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/aerospace_services/findings.json` | FTG/CGY/MAL evidence; excerpts beside it |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/infrastructure_finance/evidence.json` | EFX/BDGI/CF sources, passages, periods and limitations |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/infrastructure_finance/findings.json` | Delegated EFX/BDGI/CF analysis; canonical summary controls interpretation |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/primary_review` | Root-opened source metadata, SHA and extracted text |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/scripts/fetch_sources.py` | Public HTML/text source collection; not a PDF extractor |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/interview/recovery_status.json` | Audio URL/hash, partial ASR coverage/method and gaps |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/interview` | Five timestamped partial ASR files, publisher evidence/audio; small.en CPU int8 and targeted medium.en number check |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/scripts/build_manifest.py` | Rebuild and verify local file SHA-256 inventory |
| `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/data/source_manifest.json` | Evidence/code paths, sizes, SHA-256 and source metadata references |

Reproduce: `python /home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/scripts/compare_valuations.py`. It uses saved inputs, no credentials/network. Company period bridges, currencies, lease differences, 12 returns and benchmark arithmetic were checked. FCF definitions were explicitly reconciled or excluded. Qualitative rankings and range multiples remain judgments.

Original PDFs/audio/HTML/XML are retained under durable home and ignored by Git. The small text/metadata/calculation bundle and checkpoints are preserved in Git; use source URLs and manifest hashes for original-source validation. This is private research, not a public report; no issuer/manager contact or off-host publication occurred.

Final bounded review: all three company workers checked the integrated synthesis against their evidence. Corrections incorporated: explicit FCF adjustment directions, CGY customer-period qualifier, MAL adjusted-EBITDA provenance, FTG forecast versus observed growth, and VNP interview currency uncertainty. No material ranking or arithmetic disagreement remained.
