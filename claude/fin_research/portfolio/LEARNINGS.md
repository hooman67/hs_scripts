# LEARNINGS — Durable Insights

Last updated: 2026-11-01

Rules: every learning gets a source or date, a confidence mark (VERIFIED / ASSUMED / UNVERIFIED), and a brief explanation so we can apply it to future decisions.

---

## AI supplier quality and silver implementation — 2026-11-01

- **VERIFIED, latest issuer results:** LRCX and KLAC have the strongest combined operating economics
  among the seven requested suppliers: 40.0% and 45.0% GAAP operating margins, declining share counts,
  and clean positive cash generation. ANET's operating quality is also exceptional, but two customers
  represented 42% of FY2025 revenue and its current valuation is substantially higher.
- **VERIFIED, per-share quality risks:** MRVL quarterly SBC was 11.9% of revenue and diluted shares
  rose 5.8%; LITE and COHR common shares rose about 27% and 26%; COHR FY free cash flow was roughly
  -$1.02B; ARM's quarterly SBC was $343M versus only 7.1% GAAP operating margin. AI revenue growth
  alone does not qualify a company for the Quality sleeve.
- **VERIFIED primary operations / SECONDARY valuation:** Alphabet's latest Search revenue grew 12%
  and Microsoft produced a 49.7% GAAP operating margin. Most requested suppliers were more expensive
  on confirmed annualized quarterly earnings. “Picks and shovels” changes the source of risk from
  Search disruption to customer concentration and the AI-capex cycle; it does not remove risk.
- **VERIFIED official holdings:** October 30 JQUA held LRCX at 0.80%, KLAC at 0.68%, MSFT at 2.06%
  and GOOGL at 1.47%. A 5.5% JQUA sleeve therefore provides small participation while sharply limiting
  direct-name risk, which matters alongside Adobe employment and RSU exposure.
- **VERIFIED vehicle terms:** SIVR's effective fee is 0.30% under a voluntary waiver versus 0.45%
  gross; SLV charges 0.50%; OneGold charges 0.30% annual silver storage plus a $5 quarterly account
  minimum; PSLV has a 0.52% MER and is a PFIC for U.S. investors. Vehicle cost, taxable structure,
  liquidity and allocation room must be decided separately.
- **ASSUMED exposure attribution:** applying WPM's verified Q2 52% silver/46% gold revenue mix to the
  live position gives about 1.38% silver and 1.22% gold look-through. This is useful for preventing
  accidental double counting but is not bullion beta or principal protection. Full evidence:
  `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/ai_quality_silver_2026-11-01/SUMMARY.md`.

## Tax-lot and wash-sale controls — 2026-10-23

- **VERIFIED, broker scope:** The aggregate portfolio Sheet is not a tax-lot ledger. Schwab's export
  differed materially for multiple holdings and revealed $8,104.89 of realized 2026 short-term gain,
  $11,386.02 across all negative lots and $34.71 of wash loss already disallowed.
- **VERIFIED, IRS rule:** The wash-sale window covers 30 days before and after the loss sale and can be
  triggered by a spouse or an IRA/Roth IRA purchase. An IRA-triggered loss does not increase IRA basis.
  Small DRIP purchases matter; never ignore them merely because the dividend is small.
- **VERIFIED / case-specific implication:** Cross-listed shares of the same common equity, such as
  CCJ and CCO.TO, must be treated as the same issuer exposure for purchase blocking. Full liquidation
  plus a different fund can close a recent-lot wash chain, but the final 1099-B must be reconciled.
- **ASSUMED, tax-swap implementation:** Different sponsor/index ETF pairs materially reduce
  substantially-identical risk, but there is no IRS ETF safe harbor. Record the benchmark differences
  and retain a broader substitute when uncertainty is material.
- **VERIFIED-general / user data incomplete:** RSU sale proceeds are not capital gain. Vest-date
  compensation basis must be reconciled to the broker 1099-B and supplemental statement to avoid
  double taxation.
- Full evidence: `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/tax_loss_harvesting/SUMMARY.md`.

## Phase 1 Findings

### Build Canada comparison — 2026-10-20

- **VERIFIED, vendor-data scope:** Some TSX enterprise-value fields combine CAD market value with USD financial data. Recompute equity/EV in the issuer's reporting currency and distinguish financial debt from leases. A populated vendor field is not a validated ratio.
- **VERIFIED, issuer metrics:** Calian's operating FCF excludes working-capital effects and does not deduct capex; it materially exceeds conventional CFO less capex. FTG explicitly reports temporary pricing premiums. Growth and adjusted EBITDA are insufficient cash-quality tests.
- **VERIFIED / bounded exposure:** Enerflex announced >1.75GW of data-center power backlog; contract economics and AI-specific fraction remain undisclosed. ELVA's US$280m Amazon threshold relates to additional warrant vesting, not guaranteed purchases or automatic conversion. Calian's roughly 69% defence backlog does not establish the same Canadian-defence percentage.
- **ASSUMED, portfolio implication:** Canadian listing/domicile is not reliable CAD economic exposure or recession protection. Many requested companies earn predominantly abroad. Domestic manufacturing can still benefit through exports and industrial policy; test the full policy-to-per-share-cash chain.
- **VERIFIED sample / ASSUMED interpretation:** Four complete three-pick appearances reveal both major winners and losers; repeated picks and unequal overlapping periods prevent interpreting them as audited fund performance. Institutional credibility and investment skill require separate evidence.
- Source, as-of dates and limitations for all above: `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/SUMMARY.md`. Historical findings below remain dated; subsequent audit conclusions control where they conflict.

### Structural (VERIFIED, inline analysis 2026-07-07 — `structural_audit.md`)
- **"Diversification" is largely ONE bet.** 20 theme-labels collapse to a few macro factors;
  **commodity/real-asset megafactor (energy+precious metals+industrial metals+ag) = 74.7% of
  non-cash, 37% of total.** All positively correlated (inflation/growth/USD/real-rates). If the
  inflation/USD-debasement thesis is wrong or early, most of the book falls together. Not 8
  diversifiers — one large macro position. VERIFIED (live MVs + factor map).
- **He is OVER-insured against house-timing risk, not under.** Total portfolio vol **6.6%** (2y
  weekly, well under his 10% ceiling); non-cash worst 2y drawdown −8%; even a −30% non-cash crash =
  −14.9% of total with the $280k cash 100% intact. Plus a separate $250k house reserve. The binding
  risk to his WEALTH goal is over-defensiveness (50% cash + 37% commodities lagging for a decade),
  not a pre-house crash. VERIFIED.
- **Book-value data bug:** his export mixes CAD/USD in the book-value column (some CAD holdings
  converted, some raw). Recompute basis = shares×avg_buy_native×FX. MNT looked −26.5%, actually +4.5%.
- **Behavior contradicts stated philosophy:** says "avoid individual stocks, prefer ETFs, no edge" but
  holds ~45 individual names incl. 15 micro (<$1.5k) legacy 2021 specs. Says "AI bubble will burst" but
  owns ARKK/RBLX/autonomous. Says "metals expensive, waiting to buy" but already 21% metals + 8.5%
  uranium. Says "minimize USD" but 50% is USD cash (his single biggest USD exposure). Says "want EM/China"
  but EM is ~1–2% vs 25% target.
- **Adobe RSUs ~$732k = his largest single asset, and it's US tech/SaaS under AI pressure.** Argues for
  LESS direct tech/AI in the liquid book, not more — job + portfolio would fall together if AI hits Adobe.
- **B-bucket mislabeled:** he filed cyclical commodities (silver, copper, steel, oil ETFs) under "B —
  inflation hedge," but those are C-risk (cyclical), not defensive. True A/B/C ≈ 50/13/37, not 50/27/23
  — genuine high-vol bucket is ~37%, 2.5× the 15% plan. B should be only low-vol hedges (core gold, TIPS).

### Macro thesis grades (from verification agents — update as they land)
- **USD decay (his #1 conviction): 2/10 as stated (−70%/10yr), 7/10 softened.** VERIFIED 2026-07-07:
  DXY 100.93 (+3.5% YoY, dollar UP not down); **USD/CAD 1.42 — CAD WEAKENED 4% vs USD** (directly
  against the thesis for a Canadian); gold $4,131 (+25% YoY) = the ONLY frame where "USD losing value"
  is clearly true. Debt/GDP 122.6%, deficit 6.1%, interest ~$1.22T (~20% of revenue) = fiscal bull case
  real. BUT Fed is doing QT (balance sheet $8.97T→$6.72T), not printing — his "money printing" premise
  is 2020-21, not now. Foreign Treasury holdings ROSE to $9.35T. De-dollarization glacial (USD reserves
  70%→57% over 25yrs, ~0.5%/yr; no viable alternative). **KEY INSIGHT: "USD loses value" is 3 different
  claims (vs FX / vs goods / vs gold) needing 3 different hedges — he conflates them. −70% only makes
  sense vs gold, which is a bet on GOLD not the dollar. For a 3-5yr house goal he needs TIPS/Real-Return
  Bonds (stability), not 20-yr debasement bets.** Detail: `research/macro_usd_decay.md`.
- **China (VERIFIED live 2026-07-07 — `research/macro_china.md`):** "China must-have diversifier" 4/10;
  "China cheap enough" 7/10. **His real gap is EM (1-2% vs 25% target), NOT China specifically.** MSCI
  China ~12.8× fwd vs S&P ~22× = ~42% discount, ~22% below own 10yr avg; large-caps net-cash + buying
  back (Alibaba $19.1bn buyback remaining, −5% shares/yr; Tencent ~HK$112bn 2024 + div +32%). KEY
  NON-OBVIOUS: **EMXC (EM ex-China) P/E 20.0 vs VWO 17.0 — China is the CHEAP part of EM**, stripping it
  out makes EM more expensive (weak case for EM-ex-China). Sanctions moot (internet basket on no OFAC
  list); HK lines safer than US ADRs on delisting. **TN-visa/green-card flag: a future green card →
  US person → outbound rules bind him** (not the non-sanctioned names today; argues HK-line/non-US-broker
  structuring later). VERDICT: **3% of total (~$16.5k) via KWEB/MCHI in RRSP, 5% hard cap.** Cut BIDU
  (ROE 0.3%, broken, tax-loss harvest); hold BABA (net cash, buying back); hold/grow KWEB as core.
- **Energy (VERIFIED live 2026-07-07 — `research/macro_energy.md`):** "underinvest→oil rally" **5/10**
  (long-run real but swamped by 2026-27 OPEC+ glut all forecasters see — IEA ~4mb/d surplus, JPM Brent
  ~$60; right theme wrong clock; NOT cheap anymore once oil normalized). "Canadian energy outperforms"
  **7/10 — strongest** (pro-oil govt claim VERIFIED + stronger than he thought: Carney killed consumer
  carbon tax, fast-tracked pipelines Bill C-5, scrapping emissions cap; TMX+LNG Canada real; Cdn energy
  +44% vs US +26% TTM — but partly priced in, WCS diff re-widening, already ~56% Canada). "Energy as AI
  proxy" **3/10 — weakest** (AI→power link real but modest ~4-6 Bcf/d by 2030 and lands on GAS not the
  OIL names in his book; buying oil E&P for AI adds commodity risk w/o AI upside). Sensible weight: hold
  ~12-14% total / trim toward 15-20% of non-cash; don't ADD oil at fair value into a glut; tilt to GAS
  (underweighted, better-supported) + quality producers w/ 6-7% yield over commodity ETFs; OXY→EOG swap
  still best use of energy $. DATA-INTEGRITY CATCH: search results contaminated by a bogus "2026 Iran
  war / Hormuz closed / Brent $119" narrative INCOMPATIBLE with calm ~$69 spot — anchored to spot; the
  crisis-inflated forward EPS make forward P/E look cheaper than reality.
- **⚠️ CORPORATE ACTION — ARC Resources (ARX) is being ACQUIRED BY SHELL (VERIFIED 2026-07-07, web).**
  Announced **2026-04-27**: ~C$16.4bn deal, **C$8.20 cash + 0.40247 Shell shares per ARC share**, ~27%
  premium, closing 2H2026. (Agent mis-reported it as a flat C$32.80 all-cash bid — that was the analyst
  target; CORRECTED here.) ARX (~$12k, a big position) is now effectively a **merger-arb / cash+Shell-
  stock** position, NOT an independent Cdn gas E&P. ARX C$29.96 trades below headline because the stock
  leg floats w/ Shell + deal-timing risk. DECISION NEEDED at synthesis: hold-to-close (become a Shell
  shareholder + cash) vs sell now to redeploy. Removes a gas leg from the sleeve on close.
- **AI thesis (VERIFIED live 2026-07-07 — `research/macro_ai_thesis.md`):** His 5 sub-theses graded:
  (1) "bubble bursts but real like internet" **7/10** (froth concentrated in Tesla 191× fwd/AMD 63×/
  Palantir 83×/OpenAI, NOT the profitable mega-caps NVDA 19.7×/MSFT 20.9×/META 18.3×; CAPE>40 rhymes
  w/ 2000 but earnings quality doesn't). (2) "AMZN & GOOGL winners, AMZN owns Anthropic AND OpenAI"
  **6/10** — Google thesis strong; **Amazon-Anthropic ~$8B stake VERIFIED; but AMAZON OWNS NO OPENAI
  EQUITY (REFUTED)** — it's a $38B AWS compute contract (Nov 2025); MICROSOFT (~27%) is OpenAI's equity
  backer. (3) "bearish MSFT/Meta, OpenAI; govt bailout probable" **5/10** — **MSFT/Meta are actually the
  VALUE names (18-21× fwd, cheaper than his preferred GOOGL/AMZN, fundamentals intact); "OpenAI govt
  bailout probable" is UNSUPPORTED speculation — do NOT rely on.** (4) "models commoditize → value to
  app/infra" **8/10 — his best thesis** (mid-tier cost −10×/yr, open weights 6-12mo behind; enterprise $
  crossed to majority app-layer 2025; caveat: frontier premium NOT collapsed via test-time compute).
  (5) "energy = indirect AI bet" **4/10 — weakest** (broad energy=crude risk, orthogonal to AI; clean
  AI-power bet = electricity/nuclear/grid CEG/VST/GEV/GRID/NUKZ, mostly already re-rated). **BIGGEST
  POINT: Adobe ($732k RSUs) is his single biggest AI decision — down ~47% at 8.4× fwd, market prices it
  as AI VICTIM but ARR +12.5% / >$5B AI-influenced ARR says winner-in-progress; rational move = TRIM
  ON VEST not add (salary+equity = same undiversifiable risk). He already holds uncoordinated AI pieces
  (AMZN, ARKK, CEG/CCJ/BWXT, GEV) — doesn't lack exposure, it's unintentional/unbalanced.** REC: get
  "AI is real" upside via breadth (index/QQQ) + at most 1-2 quality names he understands (Alphabet
  first), infra via SOXX/GRID/NUKZ not oil&gas, avoid 60-190× names, TRIM ADOBE = highest-value move.
- **Metals/uranium (VERIFIED live 2026-07-06/07 — `research/macro_metals_uranium.md`):** Prices: gold
  $4,132 (−26% off Jan ATH $5,608), silver $61.02 (−50% off $121.64), platinum $1,641 (−44%), palladium
  $1,268, uranium spot $85.50/term $95.50. Value-buy scores: Gold 5, Silver 5, Platinum 6, Palladium 3,
  Uranium-metal 6. Entry zones: gold $3,700-4,000 (high-conviction $3,400-3,500), silver $48-52, platinum
  $1,450-1,550, uranium fine here. **RESOLVES HIS CONTRADICTION: not hypocrisy, a mislabel — 30% is of
  NON-CASH; vs total it's ~14.6% = reasonable USD hedge. BUT "waiting for pullback" ALREADY HAPPENED
  (silver −50%/plat −44%/gold −26%/uranium −19% off highs) — he's holding THROUGH it, not waiting ahead.
  Consistent move = TRIM rich high-beta names into strength (WPM, CCJ), NOT add.** KEY CORRECTIONS:
  (1) **WPM is ~half GOLD not silver** (Q1-26: 51% gold/47% silver) — his "single-name silver bet"
  half-wrong; quality streamer (86% margin) but 9.5%-non-cash single name = concentration. (2) **CCJ fwd
  P/E now ~78×** (richest in complex, prices $100+/lb U + Westinghouse) — uranium METAL fair-cheap, froth
  is in the EQUITY; CEG cleanest value (~21×, contracted PPAs). (3) **Silver/plat DON'T hedge USD — only
  gold does** (50-68% industrial/cyclical demand); gold's real-yield correlation broke (TIPS +2.26% yet
  gold real-ATH) b/c marginal buyer is sovereign (CBs bought 863t 2025). REC: shift to monetary gold core
  (physical + MNT), trim WPM to ~2-3% + trim CCJ, KEEP AEM (best miner, fwd P/E 11.2), CEG, BWXT.
- **Supercycle/industrial metals (VERIFIED live 2026-07-07 — `research/macro_supercycle_metals.md`):**
  Super-cycle thesis **4/10 — mostly narrative** (IMF broad-commodity index still ~29% below 2022 peak;
  rally narrow = copper structural + gold monetary/late; **reshoring leg CONTRADICTED: US mfg-construction
  −30.2% from Sep-2024 peak $250.2B→$174.8B May-2026**, matches prior sector_trends finding; defense
  durable to 2035 but tiny for metals demand + priced in Rheinmetall P/E ~61; tariffs raise prices not
  volumes). Per-metal: **Copper 6.5/10** (best leg but right-long-term/early — ICSG SURPLUS through 2027,
  deficit is 2030s story w/ 16yr mine lead times, spot at ATH $6.67/lb; best vehicle COPX or FCX/SCCO;
  **BHP only HALF-copper — iron ore still 55% of EBITDA**). **Nickel 3.5/10 — falling knife, SKIP**
  (Indonesia 59.5% + flooding verified, INSG surplus +283kt 2025; but demand capped LFP=79% China EV
  batteries, Western capacity mothballed-not-destroyed caps upside, NO clean vehicle — NINI/JJN delisted
  confirmed, NIKL tiny $69M/illiquid/impure). **Aluminum 6/10 — the one real value name** (Alcoa fwd P/E
  ~6.1, tight LME <300kt, but high-beta + its Cdn smelters pay the 50% tariff). **Steel 3/10 tariff-trap;
  XME is NOT a steel ETF — 27% steel/19% GOLD/18% mining/17.5% coal = REDUNDANT with his gold.** Rare
  earths 2/10 as value (MP fwd P/E ~137, momentum not value). CONFIRMS MEGAFACTOR: energy+gold+silver+
  copper+steel+alu+ag = ONE leveraged inflation/real-asset/USD bet, ~70% non-cash; w/ ≤10% vol + 3-5yr
  house + poor-forecaster profile, adding to commodities at cycle-highs is imprudent. **"Keep the rifle
  (modest copper + gold), drop the shotgun (skip nickel, avoid steel/RE)"; diversify to underweights
  (EM 1-2% vs 25%, quality non-commodity equities); house money stays out of high-beta sleeve.**

### ALL 8 RESEARCH AGENTS COMPLETE (2026-07-07). Synthesis → PHASE1_AUDIT.md.

## Completeness audit (2026-07-08 — "am I missing big themes?")
- **Sectors (VERIFIED live 2026-07-07 — `research/completeness_sectors.md`):** KEY FRAME — **VT is NOT
  "US tech"; at his 22% weight it already gives (% of total book) ~6.8% tech (incl NVDA/AVGO/TSMC),
  ~3.4% financials, ~2.5% industrials, ~1.7% healthcare + every sector at global weight** → most
  "themes" already inside the core; REDUCES need to act. GENUINE GAPS: (1) **Financials/insurance 7/10**
  — cleanest gap, largest sector he owns ~0 directly + CHEAPEST big sector (insurance IAK P/E 11.2/KIE
  11.9; banks KBWB 16/KRE 13.5), best fit for quality-value buyer → IAK/KIE or KBWB. (2) **Defense/
  rearmament 6.5/10** — the one genuinely-NEW secular theme absent (SIPRI world mil-spend $2.72T 2024
  +9.4% real, Europe +17%); richly valued ITA P/E 38 → small DCA'd ITA/PPA/SHLD/EUAD. (3) **India 5.5/10**
  — a REWEIGHT not missing (in VWO, underweight) → INDA or EMXC to de-China EM. (4) **Midstream/LNG infra
  5/10** — real gap (owns producers not infra, AMLP 7.8% yield) but already ~30% energy → only swap-within-
  energy via MLPX/EMLP, never net-new. **NOT gaps (killed his fears): semis (NVDA/AVGO/TSMC already top VT
  holdings — his "no chip exposure" is FALSE), Japan (in VT), cybersecurity (~5.8% CAGR, in VT tech),
  robotics (BOTZ +8%/5y), grid/reshoring (has GEV), water, med-devices (IHI −13%/5y), SMR (NuScale −76%),
  space, EM-ex-China standalone.**
- **Asset classes/factors (VERIFIED live 2026-07-08 — `research/completeness_asset_classes.md`):**
  **BIGGEST GAP IN THE WHOLE PLAN — he's insured against only ONE crash regime.** Cash+short-TIPS+gold
  protect an INFLATIONARY crash (2022); in a DEFLATIONARY/recession crash (2008/2020/2018Q4 — more common)
  they stay FLAT while stocks fall 20-34%. The asset that RISES then = intermediate govt bonds (his
  USD-debasement fear made him reject them). VERIFIED: intermediate Treasuries +6.4%/+4.4% in COVID crash,
  +3.4% 2018Q4 while stocks −20-34%; cash only stayed flat. AND that's the SAME scenario his Adobe RSUs get
  hit → doubly exposed. TOP GAPS: (1) **Intermediate govt bonds ~5-8% (IEI/IEF or CAD XSB/VAB), from cash,
  NOT long bonds — grade 8.** The missing crash hedge. (2) **Stop the default USD cash tilt — grade 8**
  (already ~$732k USD Adobe + USD tilt = deeply USD-concentrated while house liability may be CAD; match
  reserve to house location, or 50/50 if undecided — CHALLENGES yesterday's USD-tilt decision). (3) **Tilt
  ~3-6% of VT to small-cap/quality-value (AVUV+AVDV/QUAL) — grade 6** (closes say-do gap: wants cheap-
  quality but VT is cap-weight, doubles the mega-cap tech he has via RSUs). SKIP: REITs (grade 3, equity-
  beta not house-hedge), FX bonds (grade 2, BWX −18.7% 2022), cash tinkering (SGOV ~3.85% near-optimal),
  long bonds (instinct right). Managed futures DBMF grade 5 (optional, +20.5% 2022). CORRECTION: no good
  SHORT Canadian real-return bond (Canada stopped RRB issuance 2022; XRB.TO long/volatile −11.8% 2022) →
  keep short-inflation hedge in US VTIP, currency-match via CAD nominal short bonds/GICs.
- **Geography/blind-spots (VERIFIED live 2026-07-07 — `research/completeness_geography_blindspots.md`):**
  REINFORCES asset-class agent — two independent agents converged: **entire book = ONE bet (long inflation
  /real-assets/short-USD); $0 profits if OPPOSITE happens (disinflation + US-tech growth, the 2010-2020
  outcome). buy_list even FORBIDS the cleanest hedge ("do NOT buy long-duration bonds") = the blind spot.**
  THE UNHEDGED SCENARIO: disinflation + US-tech growth → ~5 sleeves lose at once + his one winner (US tech)
  is a SINGLE STOCK. Hedges ranked: (1) long-dur Treasuries IEF 5%/TLT/EDV grade 10 (pays 4.5-5% to wait);
  (2) regulated utilities XLU/VPU 3-4% (bond-proxy that ALSO expresses AI-power thesis); (3) fully-fund
  the 22% VT core; (4) BRK-B 2-3%. **NOTE: this agent says LONG-duration; asset-class agent said
  INTERMEDIATE (IEI/IEF) — reconcile in synthesis: intermediate is the better risk/reward for a 3-5yr
  house goal (less rate risk), long-dur is the more powerful equity-crash hedge. Likely answer:
  intermediate core + small long-dur satellite, or just IEF (7-10yr) as the compromise.** GEOGRAPHIC
  GAPS: **#1 ADOBE = ~57% of NET WORTH — the dominant concentration risk, dwarfs everything.** #2
  aggregate Canada ~14% liquid + CAD house + CAD income = ~4.8x overweight, hidden across labels, and
  Canada isn't cheap (21x). #3 Japan via HEDGED DXJ 2-4% (cheap 18.6x, governance re-rating; DXJ 3y +128%
  vs EWJ +65% — hedge removes yen leak). #4 India INDA/EMXC 1-2% DCA-only (underweighted in cap-index +
  uncorrelated to commodities, but expensive 22x). SKIP Europe (in VT)/LatAm/Gulf (just more commodity bet).
  Verdict: geography is FINE (VT+5% EM complete); real problems = 2 overweights (Adobe, Canada) + missing
  disinflation axis.

### Cheap-quality screen REFRESH + deep dives (2026-08-26)
- **Re-ran the original INTU-finding funnel on live prices** (`screens/refresh_2026-08/`). July winners'
  cheapness HARVESTED: INTU +26% / CTSH +50% since 2026-07-06 → both re-rated up, no longer deep value.
  Still cheap: EOG/TROW/CNOOC/Buzzi/NetEase/CPIC. Newly cheap: US insurers (HIG/ACGL), Korean memory
  (SK Hynix fwd P/E 3.6 — cyclical + needs IBKR), PDD/TSM/DECK/TTD. Sector top-down unchanged (Damodaran
  annual, still Jan-2026). LOWER-conviction batch than July — no obvious fat pitch.
- **Deep dives HIG / ACGL / TSM (2026-08-26 — `portfolio/deep_dives/{HIG,ACGL,TSM}.md`):**
  - **HIG 5.7/10 WATCH** — the screen was MISLEADING: ~9.7× P/E is STRUCTURAL (traded ~10× for years),
    near 52wk high, fwd EPS < trailing = Street prices earnings DECLINE. Low multiple on PEAK-cycle P&C
    earnings, not a discount. Duplicates BRK-B insurance-float. Buy zone ≤$120 (is ~$140).
  - **ACGL 7.15/10 WATCH** — top-tier underwriter (16% BVPS compounding, counter-cyclical mortgage arm),
    but same peak-cycle problem (fwd P/E 10.3 > trailing 7.9; reinsurance rates softening −16%, mgmt says
    "softening cycle" — the Swiss-Re issue). Duplicates BRK-B. Flip-to-BUY on de-rate to ~1.2-1.3× book.
  - **TSM 7.20/10 WATCH→small-buy on weakness** — widest moat in tech (>70% foundry/~90% leading-edge),
    NOT priced-for-perfection (fwd P/E ~19-24, PEG<1 on +40% growth, ROE 40%, 60%+ GM). BUY-grade asset,
    WATCH-grade FIT: (a) un-hedgeable Taiwan-invasion tail (wrong for 3-5yr house money), (b) levered AI-
    capex-bubble bet correlated w/ his Adobe concentration. If bought: ≤2-4% capped EM-tail sleeve, on a
    pullback, long-horizon money only. FV ~$470-540 (ASSUMED). ⚠️ yfinance currency-mix bug confirmed on
    TSM (served P/B 87 vs real 12.9; EV/EBITDA 4.7 vs real 21.8) — recomputed from TWD statements.
  - **NET: none is a buy-now.** Both insurers duplicate BRK-B (Financials sleeve doesn't need them). TSM
    is the most interesting but its risks are exactly the ones Hooman must avoid. Screen's edge is timing
    — Aug batch has no obvious fat pitch → validates holding dry powder over forcing a buy.

### ALL 3 COMPLETENESS AGENTS COMPLETE (2026-07-08). Synthesis → COMPLETENESS_AUDIT.md.

## Day-1 timing research (2026-07-09, VERIFIED live)
- **Iran/US escalation is REAL this time** (VERIFIED web, 2026-07-08: US strikes on Iran, Trump ended the
  peace agreement, Strait of Hormuz blockade threats). Earlier (2026-07-05) the energy agent had flagged a
  "$119 Brent / Hormuz" narrative as UNRELIABLE b/c it clashed with calm ~$69 spot — that was premature; a
  fresh escalation began ~07-08. **BUT magnitude is still hyped:** sources split between "$120+/$130" (the
  unreliable strand) and sober "$73-75." **Live yfinance tiebreaker: WTI $73.00, Brent $77.36** → oil
  really rose ~+6.4%/+8.1% over 5 days but to ~$73, NOT $120. Don't anchor to $120/$130.
- **Energy names popped WITH oil (VERIFIED live 5-day):** OXY +9.2%, CNQ +7.5%, CVX +4.5%, XOM +3.7%,
  SLB +2.3%. → genuine strength to trim into, but a war-premium pop (mean-reverts if Hormuz stays open),
  not a thesis change. Metals/uranium did NOT join: WPM −3.0%, AEM −5.8%, CCJ −8.4%, CEG −5.7% (5d).
- **Decision: split the global-equity core VTI(~60%)+VXUS(~40%) instead of VT** — as a Canadian in a
  TAXABLE account, holding VXUS separately lets him claim the foreign-tax-credit on intl dividends (buried
  & unclaimable inside VT); also cheaper + independent US/intl rebalancing. (Was listed as an option in
  execution_plan, now locked.)
**THE HEADLINE: the portfolio is not missing THEMES — it's missing a MACRO AXIS (disinflation hedge) and
has 2 hidden overweights (Adobe 57% of net worth, aggregate Canada). Genuine adds, ranked: intermediate/
long govt bonds (8-10), financials/insurance (7), defense (6.5), utilities (bond-proxy+AI-power), small
value tilt AVUV (6), Japan hedged DXJ (grade tilt). Biggest single risk = ADOBE concentration (diversify
on vest). Most "themes" already inside VT (semis/Japan/cyber/etc — his chip-exposure fear is FALSE).**

### Semiconductor exposure refresh (2026-09-22)
- **The structural thesis is strong, but a dedicated sleeve remains unnecessary.** Current VTI, VXUS,
  JQUA and VWO positions provide roughly 0.55%–0.60% look-through semiconductor exposure only because
  those sleeves are underfunded; their intended allocations should raise it to roughly 3.3%–3.8%.
- **SOXQ is the best tactical implementation:** 0.19% fee, 30 large U.S.-listed global semiconductor and
  equipment companies, including AMD and Intel. It is preferable to concentrated SMH, more expensive
  SOXX and speculative equal-weight XSD for this portfolio.
- **Great industry does not equal good entry.** At review, SOXQ was up about 100% over one year, around
  40 times trailing earnings and 23% above its 200-day average while WSTS forecast a highly cyclical 250%
  memory-market surge. Accepted monitoring zones are $85 and $79–$80; no allocation change now.

### Holdings deep-dive grades (from holding agents)
- **Healthcare PFE/LLY (VERIFIED live 2026-07-07 — `deep_dives/healthcare_PFE_LLY.md`):** His "both
  expensive" premise WRONG for PFE. **PFE fwd P/E 8.4 / 1.5× book / 7.1% yield = one of cheapest large
  pharmas** (HOLD, don't add, trim — 5.5/10; cheap-for-reason: Eliquis −56% IRA cut live 2026, Ibrance
  −50% 2027, 100% pharma tariff, ROE 8.3%; 7.1% yield FCF-covered 1.26× — safe 2026, watch 2027-28).
  **LLY fwd P/E 27 / 34× book but PEG ~1.6** (rev +55%, EPS +170% on Mounjaro/Zepbound GLP-1) = expensive
  but growth-justified (HOLD, add only on pullback ~$960-1,080, not at $1,200 52wk-high — 6.5/10).
  **SIZING INVERTED: holds MORE of weaker PFE (~6.4% non-cash) than stronger LLY.** Right-size PFE to
  ~3-4%. AI-drug-discovery = still pure narrative (zero AI drugs approved mid-2026); PFE/LLY do NOT
  capture "AI in healthcare" — that's med-device (GEHC/Siemens) or managed-care admin (UNH/Optum).
  Cheap-healthcare slot better filled by CI (fwd P/E 8.4, ROE 16.3%, no patent cliff).
- **Misc scorecard (VERIFIED live 2026-07-07 — `deep_dives/scorecard_misc_holdings.md`):** AMZN 7.5
  HOLD/add-on-dip (fwd PE ~25, EV/EBITDA 17, 50% GM, best-conviction keep). GEV 6.5 TRIM ~⅓ (EV/EBITDA
  ~89, fwd PE ~47 after +87%, priced for perfection). KHC 4.5 > CAG 4.0 (both value-traps, keep only
  KHC for breakup catalyst). CF 7.0 HOLD (best commodity name: 33% op margin, 27% ROE, ~10x). PDBA 5.5
  HOLD (broad-ag ballast, complements CF). CRCL 3.0 SELL. Tier2 SELL: RBLX/AA/ARKK/SBUX; keep XME as
  single metals vehicle. All 10 micros → cleanup/tax-loss-harvest (Canadian superficial-loss rules).
  REDUNDANCIES: CRCL held twice (direct + 4.5% of ARKK); AA held twice (direct + 4.6% of XME); CAG≈KHC.

---

## Session Notes (2026-07-07)

**Starting situation:**
- Hooman has $557k portfolio + $250k house reserve (separate)
- 60+ individual holdings, many micro-cap + misclassified
- Heavy in Canadian energy (7 names, redundancy concern)
- Geographic skew (43% USA, 52% dev-exUS, 5% EM) vs target (50/25/25)
- Bucket A/B/C assignments uncertain (too much judgment, not enough data)
- Contradictions: worried about AI bubble but owns AI names; wants EM exposure but only 5% allocated
- Strong conviction on USD decay (10-yr, ~70% loss) — drives real-asset tilt

**Approach:** Independent verification of all claims via parallel agents, then synthesize into ideal allocation + buy/sell framework.
