# LEARNINGS — Durable, Consolidated

Last updated: 2026-07-01 by Claude (Opus 4.8).

Rules: every learning gets a source or a "from experience in this project" tag, a date, and
a confidence mark (VERIFIED / ASSUMED / UNVERIFIED) where it's a factual claim.

_Build Canada follow-up, 2026-10-22 (Codex). Detail:
`/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/SUMMARY.md`._

- **Physical operations do not make a stock immune to an AI-spending collapse** (ASSUMED scenario).
  Badger and Calian have the lowest direct dependence among the eight reviewed names, while Enerflex
  has explicit exposure through more than 1.75GW of announced data-center power awards. FTG and
  Magellan are AI-independent physical aerospace businesses, but valuation, cycle and cash conversion
  can still cause large drawdowns. 5N Plus is physically substantive but retains semiconductor,
  customer-concentration and working-capital risk. Source: issuer evidence and scenario analysis in
  the canonical Build Canada report.
- **Classify a thematic basket by underlying economic risk before creating a sleeve** (from experience
  in this project). A `Build Canada` label would combine defence services, aerospace electronics, gas
  equipment, infrastructure excavation and specialty materials. Keeping those names in their closest
  risk sleeves while using Canada as a secondary tag preserves factor visibility and prevents a
  patriotic/policy narrative from obscuring energy, capital-spending or valuation concentration.

## Methodology learnings

_CORRECTION 2026-07-03 (Claude Opus 4.8) — supersedes the CNOOC bullet below._
- **DON'T infer investor sanctions-nationality from their employer. Hooman is a CANADIAN
  citizen, NOT a US person.** The entire project wrongly assumed US-person status because he
  works at Adobe (US) — an assumption Claude introduced, never stated by Hooman. It produced a
  WRONG "CNOOC un-investable" call. **The OFAC NS-CMIC / EO 13959 prohibition binds only "US
  persons"** = US citizens, US green-card holders, US-organized entities, or anyone transacting
  from inside the US (31 CFR §586.307, VERIFIED). **A Canadian citizen (no US green card,
  transacting abroad via a non-US broker) is OUTSIDE its scope.** Canada's own SEMA regime does
  NOT list CNOOC (VERIFIED, SOR/2021-49 is a narrow Xinjiang list). CNOOC IS still NS-CMIC-listed
  as of 2026-07-03 (VERIFIED, live OFAC pull, publish 01/08/2026) — the restriction is real, it
  just doesn't reach Hooman. **Apply-forward:** (1) confirm the investor's actual
  citizenship/residency/green-card status and broker jurisdiction BEFORE ruling anything out on
  sanctions grounds; (2) US-person sanctions ≠ universal bans — always ask "bound for whom?".
  Detail: `deep_dives/0883_HK/canadian_investability.md`.
- **RESULT: CNOOC is INVESTABLE for Hooman and is #1 on the merits (7.75).** Residual risks are
  priceable (China SOE governance, oil, HKD/geopolitics), not legal. Still confirm: no US green
  card + buy 0883.HK via a non-US broker from outside the US.

_Stage 4 deep dives, 2026-07-02 (Claude Opus 4.8) — CNOOC conclusion SUPERSEDED by the 2026-07-03
correction above; the sanctions-checking discipline still stands._
- **Check Chinese SOE/defense-linked names against the current NS-CMIC list before promoting** —
  the list is real and current (CNOOC verified on it). What changed is WHO it binds (US persons
  only, not Hooman). Non-SOE Chinese ADRs (e.g. NetEase) are generally NOT listed but carry
  VIE/HFCAA risk — check each.
- **Cyclical "cheap" names screen cheap on PEAK earnings.** Gold (NEM 6.4, Kinross 6.4),
  reinsurance (Swiss Re 6.7) all verified as high-quality but "fair not cheap" once earnings
  are normalized off a cyclical peak (gold ~$4,400, reinsurance rates now softening −12%
  Jan-2026). Energy (EOG) is the exception — oil ~$68 is mid-cycle, not peak, so EOG's cheap
  multiple is on normalized earnings. Lesson: for commodity/insurance names the scorecard's
  raw cheapness score overstates value; always normalize to mid-cycle. VERIFIED per deep dives.

_Stage 2 merge, 2026-07-02 (Claude Opus 4.8). Detail: `screens/candidates.md`,
`screens/merge_candidates.py`._

- **The A↔B cross-validation surfaced a structural split** (VERIFIED from the merge): the
  highest-scoring bottom-up names (NEM, TROW, energy E&Ps, Chinese internet) are almost all
  **B-only** — their sectors were NOT 1a-cheap-vs-own-history. The names that are BOTH (1a-cheap
  sector + 1b gate-pass) are mostly **developed staples/services with only moderate 1b scores**
  (Info-Services IT like Cognizant/Accenture are the standout cheap-AND-high-ROIC pairings).
  Takeaway: quality-first bottom-up ranking and sector-cheapness rarely agree at the very top —
  the overlap is thinner and more defensive than the top of either list alone.
- **The BOTH bucket came out developed-only (zero EM)** — because 1a's EM cheap sectors are
  financials/transport/consumer that **1b structurally under-screens** (insurers lack GM/EV-EBITDA;
  EM mid-caps thin on Yahoo). So EM diversification has to come from (a) EM B-only names promoted
  by hand (NetEase, TSM, PDD, Petrobras) and (b) the A-only watchlist, which is **entirely EM**
  (Life Insurance, Railroads, Trucking, Auto/Building-Supply Retail, Shoe, Education) and needs a
  Stage-3 leader-hunt. Lesson: a US-heavy universe + a financials-blind screen will crowd EM out
  of the "highest-conviction" bucket unless you compensate deliberately. VERIFIED (from this merge).
- **Trap-gate overlay works as intended** (VERIFIED): 7 Food-Processing names (KHC, HRL, GIS, MKC,
  SJM, HSY, MDLZ) passed the 1b Piotroski/FCF/debt gate but were DEMOTED because 1a flagged the
  sector as structurally declining — the exact value-trap catch the merge is for.
- **A↔B join is by sector via a curated yfinance-industry→Damodaran-industry map** (ASSUMED,
  judgment) — kept small/auditable in `merge_candidates.py` rather than fuzzy-matched, because a
  mis-map corrupts bucketing. Region-gated (US name needs US/Global verdict; EM name needs the
  Emerging verdict — which is why EM IT-services TCS is B-only, not BOTH).

_Stage 2.5a — broadened ex-US/EM re-screen, 2026-07-02 (Claude Opus 4.8). Detail:
`screens/quant_screen_exus.md`; code `screens/universe_exus.py` + `run_quant_screen_exus.py`._

- **The Stage-1b developed/US skew was mostly a UNIVERSE-CONSTRUCTION ARTIFACT, not a quality
  gap** (VERIFIED). Expanding the ex-US/EM universe from 94+42 to **462 dev-ex-US + 292 EM =
  754** and re-running the EXACT Stage-1b screen (imported `derive_metrics`/`piotroski_lite`/
  `score_and_rank` — no new method), then re-ranking the merged **1,128-name non-financial
  global union** on one common percentile pool: the gated top-40 flips from **29 US/8 EM/3
  dev-exUS → 13 US/15 EM/12 dev-exUS**. **27 of the global top 40 are new ex-US/EM names.**
  Lesson confirmed: to compare regions fairly you MUST equalize universe size (or rank within
  region) — a US-heavy universe manufactures a US-heavy result.
- **What surfaces ex-US** (VERIFIED, as-of 2026-07-02): dev-ex-US top is **gold/base-metal
  miners** (Kinross, Barrick, Newmont-AU, Fresnillo, Agnico, Fortescue, Norsk Hydro) + Buzzi
  (cement), Auto Trader (53% ROIC compounder), Pernod, Tenaris. EM top is **CNOOC (#1 globally,
  EV/EBITDA 3.1, P/B 1.0), cheap Chinese internet** (PDD, NetEase, Tencent Music, Baidu — net-
  cash, de-rated), **Indian value-quality** (Coal India 36% ROIC, ITC 45% ROIC), **Indonesian
  staples** (Indofood twins <1.5 P/B), Petrobras. Miners + cheap-China-internet + EM staples are
  the ex-US cheap-quality engine.
- **yfinance coverage at the ex-US/EM INDEX-CAP level is EXCELLENT** (VERIFIED, 754 names):
  **95.6% usable (≥8/11 key fields), 97.3% reachable, mean 10+/11 fields** (dev-ex-US 96.5%
  usable, EM 94.2%). The 2.7% unreachable are cosmetic wrong/renamed Yahoo symbols (Malaysia
  `.KL` locals use different codes; several Brazil `.SA` renamed/merged; `ROG.SW`/`TEF`/`ABB`
  bad forms), not a systemic hole. Strengthens the Stage-1b call: **free suffices for large-cap
  ex-US/EM cheap-quality screening**; pay only for sub-index-cap EM breadth, PIT history, or
  bank fields.
- **`.L` (London) currency-unit trap** (VERIFIED): Yahoo labels `.L` names `currency=GBp`
  (pence) but the `marketCap` field is in **whole GBP**, while `currentPrice` IS in pence. Do
  NOT divide marketCap by 100 — doing so falsely turns multi-billion UK large caps (Endeavour,
  Fresnillo, Auto Trader, Games Workshop) into fake $0.1-0.5B micro-caps. This artifact briefly
  produced spurious "small-cap exceptions" until caught → **zero genuine small-caps** in the
  index-cap universe (consistent with Stage-1b).
- **Wikipedia index tickers need per-index suffix handling** (VERIFIED): DAX/CAC40/EUROSTOXX50/
  IBEX/FTSEMIB/AEX/SMI/OMXS30 tables already carry Yahoo suffixes; FTSE100 EPIC→`+.L` (dotted
  EPICs like `BT.A`→`BT-A.L`); Hang Seng `SEHK: 388`→zero-pad→`0388.HK`; NIFTY/TSX60/ASX50 are
  bare→append `.NS`/`.TO`/`.AX`. Nikkei 225 and several EM index pages are **navbox-only (no
  machine-parseable constituents table)** → use a curated large-cap list for JP/KR/TW/BR/MX/SE-Asia.

_Stage 2.6 consolidation + finalist selection, 2026-07-02 (Claude Opus 4.8). Detail:
`screens/candidates.md` (refreshed, supersedes v1); code `screens/consolidate_candidates.py`._

- **Refreshing the merge on the fuller universe FLIPS the BOTH bucket ex-US/EM** (VERIFIED from
  the rebuild): rebuilding buckets on the 1,067-rankable global re-rank (not the US-heavy Stage-1b
  ranking) puts **EM/dev-ex-US names directly into BOTH** — Buzzi (Italian cement, the one Building-
  Materials name that actually screens cheap: EV/EBITDA 6.0, P/B 1.2, vs trough-priced US VMC/MLM at
  P/E 35+), TCS (EM IT-services, ROE 48%), Japanese IT/staples (Fujitsu, Unicharm), Pernod/Diageo/
  Campari. v1's "BOTH = developed-only, zero EM" was the same universe artifact as the Stage-1b skew.
- **The v1 A-only EM Life-Insurance gap is now FILLED by the financials screen** (VERIFIED): the
  China/HK life cohort (China Taiping 0.71 P/B / 25.5% ROE, CPIC 0.72 / 17.4%, NCI 1.0 / 36%) is the
  real leader set for 1a's top cheap-EM sector — resolved from v1's "TBD Stage 3." **But the other EM
  A-only sectors stay thin/empty**: Railroads has only a *Japanese* quality operator (Central Japan
  Rwy, no EM name gated), Trucking/Education have **zero** EM quality leader, Auto-Retail only weak
  ones. Consistent with 1a's low-ROIC warning + sub-index-cap EM coverage limit. A genuine gap, not
  an omission — needs a paid API for sub-large-cap EM breadth to close.
- **The trap gate demotes EM Food-Processing too, which is arguably wrong** (judgment, ASSUMED):
  mapping Packaged Foods → Damodaran "Food Processing" trap demotes cheap gate-passing EM staples
  (Indofood EV/EBITDA 4.9 P/B 0.8, Tingyi, Nongfu). But 1a's trap verdict rests on **US/developed**
  forces (GLP-1, MAHA, US private label); EM packaged foods have a consumption-growth runway. Kept
  the demotion for map-consistency but flagged them "cheap growth-EM staple, revisit" rather than
  silently dropping — a sector-verdict is region-scoped and a global industry map can over-apply it.
- **Region-balancing a finalist list requires explicit sector caps, not just region caps**
  (from experience): the merged top tier is miner/energy-heavy (8 of top 11 are miners/oil), so a
  naive top-N is ~half commodities. Capping at max-2-miners / max-2-energy / max-2-IT-services and
  filling the rest from BOTH + financials + EM-life produced a clean US-5 / dev-exUS-5 / EM-6 mix
  across 12 distinct sectors. Financials and non-financials scores are **different percentile pools**
  — do NOT sort them into one list; select within each and interleave by region/sector.

## Data-source learnings

_Stage 4 deep dives, 2026-07-02 (Claude Opus 4.8)._
- **yfinance `info` silently MIXES currencies for foreign-filer ADRs** — it divides a USD market
  cap by local-currency (e.g. RMB) balance-sheet/EBITDA figures, producing garbage EV/EBITDA, P/B,
  and FCF-yield. NetEase screened at EV/EBITDA 6.4 / P/B 17.1 / FCF-yield 41%; rebuilt in one
  currency (RMB) the real figures are EV/EBITDA ~10.5x / P/B ~3.5x / FCF yield ~8.8%. VERIFIED.
  **Apply-forward:** for ANY ADR/foreign name in the screens, treat yfinance EV/P-B/EV-EBITDA/FCF
  as SUSPECT until rebuilt in a single currency. This likely also distorted other ADR rows in the
  Stage-1b/2.5a rankings (e.g. TCS P/B, the "ROIC-proxy >100%" buyback-firm artifacts already noted).

_Stage 0 build, 2026-07-01 (Claude Opus 4.8). Full detail in `data/README.md`._

- **Damodaran base URL** (VERIFIED, no headers needed): `https://pages.stern.nyu.edu/~adamodar/pc/datasets/<stem>.xls`.
  Working stems: `pedata` (US only), `vebitda`/`pbvdata`/`margin`/`roe`/`EVA` (+ `Global`/`emerg`
  variants; note `pbv` US stem is `pbvdata`, and `EVA` is Capitalized/case-sensitive). Files are
  `.xls` not `.xlsx` (need `xlrd`). Data lives in the "Industry Averages" sheet under a
  variable-length metadata preamble — scan for the row whose col0 == "Industry Name". VERIFIED.
- **Damodaran PE is US-only** — no `pedataGlobal`/`pedataemerg` (404). For non-US sector P/E use
  the P/B+ROE table or derive from EV/EBITDA. VERIFIED (probed 404).
- **Damodaran as-of lag:** 15/16 files dated 2026-01-05; `EVAGlobal` still 2025-01-05 (global
  ROIC-via-EVA lags a year — use `pbvGlobal` ROIC as fresher fallback). Ratios are annual
  simple-average snapshots → relative sector signal only, combine with live prices. VERIFIED.
- **yfinance is global** via Yahoo suffixes (`.SW` Swiss, `.DE` Xetra, `.NS` India NSE, `.HK`).
  Full 20/20 field coverage on AAPL/SAP/NESN.SW/TSM/INFY (2026-07-01). EM known to thin out below
  large-caps (untested breadth) — biggest risk for the EM-diversification goal. VERIFIED (5-name
  sample); ASSUMED (EM breadth gap).
- **EDGAR = US-listed filers only**, incl. foreign filers via 20-F under the `ifrs-full`
  taxonomy (not `us-gaap`) — must try both taxonomies and both 10-K & 20-F forms. Foreign filers
  report multiple currency units; prefer USD and record the unit. Nestlé (NESN.SW) absent from
  EDGAR entirely. UA header required: `Hooman Shariati hshariati@adobe.com`. VERIFIED.
- **Paid-API call:** free sources suffice for US + developed large/mid + large EM via ADRs. Buy a
  paid global API only if EM breadth (below mega-caps), point-in-time history, or bulk non-US
  screening is needed. Decide after a Stage-1 EM stress test, not upfront. ASSUMED (recommendation).
- **EM stress test result (2026-07-02, Stage 1b, 41 mixed EM tickers):** yfinance key-field
  completeness = **83% mean; 71% usable (≥8/11 fields), 76% excl. 3 hard failures**. The names
  scoring 7/11 are ALL banks/financials (lack gross margin + EV/EBITDA *by nature*, not a gap);
  true "can't reach it" failures = ~3/41 (7%), from wrong/delisted Yahoo symbols. Non-financial
  EM large caps returned near-full 11/11. **Conclusion: FREE (yfinance) suffices for large-cap
  EM cheap-quality screening; a paid API is only justified for sub-large-cap EM breadth,
  point-in-time history, or bank-specific fields.** VERIFIED (real pull, `screens/em_stress_test.csv`).
- **Wikipedia scrape needs a browser User-Agent** — default urllib UA → HTTP 403. Use
  `requests.get(url, headers={'User-Agent':'Mozilla/5.0 ...'})` then `pd.read_html(io.StringIO(r.text))`.
  S&P 500 list (503 names + GICS sector) parses as table [0]. `lxml` required. Yahoo wants
  `BRK-B` not `BRK.B`. VERIFIED (2026-07-02).
- **yfinance `.info` lacks totalRevenue** in our harvested schema but DOES give `ebitda`,
  `enterpriseValue`, `enterpriseToEbitda`, margins → derive EBIT via implied-EBITDA
  (EV/EV_EBITDA) × (opMargin/ebitdaMargin) for a Greenblatt EBIT/EV earnings yield. ROIC proxy
  (NOPAT / [debt + mcap/PB − cash]) inflates >100% for heavy-buyback firms (book equity
  depressed) — flag >100% and fall back to ROE. Net-cash firms show negative EV → EV/EBITDA<0;
  guard by blanking EV/EBITDA ≤0 and <2 (data-glitch band). VERIFIED (Stage 1b).

_Stage 2.5b financials screen, 2026-07-02 (Claude Opus 4.8). Detail:
`screens/financials_screen.md`, `screens/run_financials_screen.py`,
`screens/financials_universe.py`._

- **yfinance covers financials FAR better than the generic screen implied** (VERIFIED, 304-name
  global financials pull 2026-07-02): P/B present 98%, ROE 96%, P/E 97%, div yield 96%, payout
  98%, book value 98% — **94% of the whole universe (87% of EM) has BOTH P/B and ROE**. The
  Stage-1b "financials unrankable" problem was a *wrong-metric* issue (asking for gross margin /
  EV-EBITDA), NOT a data gap. yfinance `industry` cleanly sub-classifies (Banks - Diversified/
  Regional, Insurance - Life/P&C/Reinsurance/Diversified, Asset Management, REIT).
- **Financials-appropriate screen = P/B + P/E + div-yield (value) × ROE + ROA + capital proxy
  (quality), ranked WITHIN region×sub-group, quality-first 60/40.** Capital-strength proxy =
  ROA/ROE (= equity/assets = 1/leverage); crude — NOT CET1. Trap filter: ROE≤0 or <5%, earnings
  collapsing (<−40%), payout>100%, or the classic P/B<0.6 + ROE<8% combo. Code reusable.
- **yfinance LACKS the financial-specific fields** (VERIFIED absent): NIM, CET1/regulatory
  capital, NPL/loan-loss (banks); combined ratio (P&C); **embedded value / VNB (life insurers —
  the correct valuation base)**; tangible book; FFO/AFFO (REITs). **Concrete paid-API trigger:**
  buy FMP only if Stage 3/4 deep-dives on the EM-life shortlist need EV/VNB/combined-ratio/CET1 —
  narrower & higher-value than the generic Stage-1b recommendation. ASSUMED (recommendation).
- **Stage 1a's EM-Life-Insurance thesis CONFIRMED at the company level** (VERIFIED pull): the
  cheap-quality cohort is **Chinese/HK** — China Taiping 0966.HK (P/B 0.71, ROE 25.5%), NCI
  1336.HK (1.04, 36.3%), CPIC 2601.HK (0.72, 17.4%), China Life 2628.HK (1.15, 25.5%), PICC
  Group 1339.HK (0.57, 14.0%). **Indian listed life insurers screen EXPENSIVE** (SBI Life P/B
  9.4, HDFC Life 6.9 — India prices life on embedded-value growth, not book). Several China
  lifecos show negative earningsGrowth (China Life −32%) = the Stage-1a "cyclical trough" — cheap
  on trough, needs EV/VNB verification (not on yfinance). Cheap dev-ex-US: Italian banks (ISP/UCG
  ~1.5x, ROE 14-17%), DNB Norway, NatWest, European reinsurers (SCOR/Swiss/Munich/Hannover Re).
- **Data-quality guards for a financials screen** (VERIFIED, from this run): (1) **dedupe ADR vs
  native listings** — same company on two Yahoo lines (HSBC+HSBA.L, BBVA+BBVA.MC, ITUB+ITUB4.SA,
  MFC+MFC.TO, MUFG+8306.T…) double-counts; keep native, drop ADR (13 dropped). (2) **P/B < 0.05
  is a share-class glitch** not a valuation (BRK-B P/B ≈ 0.001 = B-price vs A-scaled book) —
  exclude. (3) yfinance `dividendYield` is already a PERCENT (5.98 = 5.98%), not a fraction.
  Dead/renamed symbols found: LFC→2628.HK, SEGRO.L→SGRO.L, MAY.KL→1155.KL, PWF.TO→POW.TO,
  LINK.HK→0823.HK; 0011.HK/BDO.PS/BPI.PS/SPT.L didn't resolve (dropped).

## Market / sector learnings

_Stage 1a sector-cheapness screen, 2026-07-01 (Claude Opus 4.8). Detail:
`screens/sector_cheapness.md`._

- **Damodaran ARCHIVES give a usable per-industry history** (VERIFIED): archived yearly files
  at `https://pages.stern.nyu.edu/~adamodar/pc/archives/<stem><YY>.xls` for YY=15..24 (EV/EBITDA
  `vebitda*`, P/B `pbv*` for US/Global/Emerging, + US PE `pedata`). Built an **11-year** series
  (data years 2015→2025, as-of 2016-01-05 → 2026-01-05). **Gotcha:** file `<stem><YY>` is stamped
  "20(YY+1)-01-05" (vebitda24 = as-of 2025-01-05; the live datasets/ file = as-of 2026-01-05).
  Older files (≤2018) use sheet "Sheet1" not "Industry Averages" and have header-cell typos
  ("Induistry Name", "Industry  Name") — tolerate both. Code: `screens/fetch_damodaran_history.py`.
- **Cheapness method that worked** (VERIFIED approach): percentile of current multiple within the
  sector's OWN 11-yr history (primary) + cross-section-vs-peers percentile + cheap-vs-quality
  (multiple × ROIC/ROE). `screens/analyze_sector_cheapness.py` → per-region ranked CSVs.
- **Cheapest sectors, as-of 2026-01-05** (VERIFIED Damodaran values): US — Food Processing, Info
  Services (22% ROIC), Cable TV, Beverage (Alcoholic, ROE trough 0.6%); Global — Cable TV, Info
  Services, staples; EM — Railroads, Insurance (Life, ROIC 15%/ROE 17.6% — best EM quality-cheap),
  Trucking, Auto retail. Cheap vs own history AND vs peers: Cable TV & Telecom (US), EM Life Insurance.
- **Cyclical-cheap (opportunity) vs secular-trap** (2025-26 web-cited, VERIFIED unless noted):
  TRAPS = Cable TV (S&P: linear "decline stage, no comeback"), Food Processing (GLP-1 + MAHA +
  private label), AI-exposed edtech/pure data vendors. CYCLICAL OPPORTUNITY = Building Materials
  (20% ROIC, infra floor), Household Products (23% ROIC), Beverage Soft (29% ROIC), Beverage
  Alcoholic (IWSR: "more cyclical than structural"), EM Life Insurance, EM Railroads/Trucking/Auto.
- **Shortlist for Stage 3** (cheap AND not dying AND decent ROIC): Info Services, Beverage
  (Alcoholic + Soft), Building Materials, Household Products (developed); EM Life Insurance, EM
  Railroads/Trucking/Auto retail (emerging).

_Healthcare sector deep-dive, 2026-07-04 (Claude Opus 4.8). Detail: `screens/sector_healthcare.md`._
- **"Healthcare is cheap" is really "managed care is cheap"** (VERIFIED). Damodaran splits healthcare into 5
  industries; broad healthcare is NOT cheap vs own history (US biotech EV/EBITDA & P/B at 95th pctile; pharma
  fwd P/E 24×; devices/tools live fwd P/E 19-36). The ONE cheap corner: "Healthcare Support Services" (contains
  HMOs) at **P/B 5th percentile in all 3 regions, US ROIC 31%**. Live payers (2026-07-05) fwd P/E: CI 8.6, CVS
  12.5, ELV 14.3, UNH 20.3, HUM 25.2. GOTCHA: Damodaran healthcare P/E averages are junk — ~500 loss-making
  biotechs drag them; use forward P/E and live large-cap pulls.
- **Managed-care cheapness = cyclical + company-specific + policy-overhang, not proven structural** (VERIFIED,
  SEC 8-Ks): UNH Q2'25 medical-cost ratio 89.4% (+430bps) on MA cost shock; FY guidance ~$29.75 → suspended →
  reset to "≥$16"; DOJ criminal+civil Medicare-billing probe (8-K 2025-07-24); CEO Witty→Hemsley (2025-05-13).
- **AI in healthcare: real where it cuts admin, narrative where it discovers drugs** (VERIFIED). Best-documented
  payoff = payer/health-IT admin (UNH/Optum ~$1.5B/yr AI, 95% auto-adjudicated claims, prior-auth days→seconds)
  and ambient clinical docs (81% of docs use AI, peer-reviewed burnout gains). Devices: AI accrues to incumbents
  (GEHC 130 / Siemens 95 / Philips 58 FDA AI clearances; ~1,524 total, 76% radiology). Drug discovery: **ZERO
  AI-originated drugs FDA-approved or generating revenue as of mid-2026** — capital-rich (Isomorphic $2.1B Series
  B) but clinically unproven, long-dated. AI is also a payer LIABILITY: 3 algorithm-denial class actions
  (UNH/Humana/Cigna) survived MTDs in 2025 + CMS-4201-F & CA SB1120 bar algorithm-only denials.
- **Headwinds = pricing/policy** (VERIFIED, CMS/Fed.Reg): IRA drug negotiation (10 drugs effective 2026, 15 for
  2027 incl. Ozempic −71%, 15 for 2028); Section-232 **100% pharma tariff** proclaimed (Proclamation 11020,
  effective mid/late-2026, not yet in force; 0% for MFN-agreement firms); aging tailwind real (US 65+ 17→23% by
  2050, health spend 18→20% of GDP by 2032, Medicare +7.4%/yr). Pharma = sharpest pricing headwind.
- **Read-through:** the only quality-first VALUE entry in healthcare is managed care (cheap + 31% ROIC + best
  near-term AI cost story). Candidates for later deep-dive: UNH (best AI, but DOJ risk), ELV & CI (cleaner-risk
  value). Devices/tools = quality-at-a-price watchlist, not value.

_Stage 5 master synthesis, 2026-07-02 (Claude Opus 4.8). Detail: `screens/ranked_output.md`._
- **The "AI-deflation panic" created the run's cheapest names — the fear is real but NOT yet in
  the P&L** (VERIFIED across 3 deep dives). IT-services + premium software sold off ~47–65% in ~6
  months off Accenture's June-2026 guidance cut: CTSH −48% (EV/EBITDA 4.8), TCS −51% (P/E 15 vs 27x
  decade median), INTU −62% (fwd P/E ~10 vs 57–70x history). Bear (headcount decoupling from revenue,
  TCS's first-ever revenue decline + 12k layoff, INTU's TurboTax pricing crack) and bull (Accenture
  $5.9B / IBM $12.5B GenAI bookings, CTSH rev +5.8%/bookings +21%, INTU GBS +15%) are both data-backed.
  **Within IT-services, CTSH > TCS on risk/reward** — half the P/E, ~1/5 the P/B (1.3 vs 6.8 = real
  balance-sheet cushion), revenue already re-inflected +6.4% cc vs TCS negative. INTU = most asymmetric
  but most contested. Apply-forward: a violent sector-wide de-rate on a *narrative* is where value lives,
  but only if the fundamentals aren't confirming it — check the company's own revenue/bookings prints.
- **Commodity/insurance "cheap" ranks overstate value — normalize to mid-cycle, and EOG was the only
  genuine exception** (VERIFIED). Gold majors (NEM, K.TO) and reinsurance (SREN) all screen cheap on
  PEAK earnings (gold at record highs; reinsurance rates peaked Jan-2023, now −12% Jan-2026 and softening)
  → only *fair* once normalized. **EOG is cheap on NORMALIZED earnings** — WTI ~$68 is mid-cycle (~30%
  below 2022 peak) and its EPS already compressed 36% to match, sub-$50 breakeven. Rule: for these names
  buy AFTER a price/rate drawdown, not after a run; their durable value is the balance sheet, not the multiple.
- **China cluster splits on investability + structure; CPIC > Taiping** (VERIFIED). CNOOC = hard OFAC
  NS-CMIC block (best business in the run, un-investable — see sanctions learning above). NetEase = VIE
  "own-a-Cayman-shell" governance risk (checked clear of NS-CMIC). CPIC + Taiping = falling-rate
  negative-spread risk (explicit Japan-1990s analogy) but both show growing EV / rising VNB / 2–4x
  solvency = cyclical-trough-inflecting, NOT broken. **CPIC is the better core EM-life pick** (16–17% ROE
  vs ~10%, VNB accelerating +40% vs Taiping decelerating +2.7%, A+H+GDR liquidity + index inclusion);
  Taiping is the deeper-value/higher-yield (~0.3x P/EV, 6.8%) satellite whose extra cheapness is partly
  explained by thin liquidity/index exclusion. All four China lifers/NetEase checked clear of NS-CMIC/SDN/1260H.
- **The ex-US/EM diversification thesis is validated by the RESULTS, not just the universe fix** (VERIFIED
  from the final ranking): 3 of the top-4 and 6 of the top-10 investable finalists are ex-US/EM (Buzzi
  dev-exUS #2, ITC EM #3, CPIC EM #4; only INTU US in the top 4). The ex-US cheap-quality engine =
  miners + cheap-China-internet + EM value-staples + European financials/industrials.

_AI-deflation cross-cutting synthesis, 2026-07-03 (Claude Opus 4.8). Detail: `screens/theme_ai_deflation.md`._
- **GenAI deflation is TWO different threats, and the answer splits software vs services** (VERIFIED
  mechanism + evidence). SERVICES (CTSH/TCS) = attack on the *billable-hour unit* (per-FTE T&M deflates
  as client productivity rises); no pricing power to defend it; the tell is headcount decoupling from
  revenue (TCS: rev −3.1% cc, headcount −20k, margin UP — productivity captured by the model). Analyst
  gross-deflation estimates: HCLTech 2-3%, MOFSL 9-12% (~2%/yr growth drag), HSBC 14-16% "offset by
  demand." SOFTWARE (INTU) = attack on the *per-seat unit* + app disintermediation, BUT a data/workflow
  incumbent can reprice AI as work-done (seat-expansion). Rule: the two mechanisms need SEPARATE judgment.
- **Fear is real but NOT in the P&L yet — one exception (VERIFIED)**: the ~50-66% de-rating is priced
  fear, not realized damage, everywhere except INTU's low-end TurboTax (−2% units, "lost on price" — the
  first hard packaged-software AI-price event). SaaS sell-off is NON-uniform and the dispersion IS the
  thesis: consumption-priced up (DDOG +91%, TWLO +47%, SNOW +19% YTD-26), seat-based apps crushed (HUBS
  −52%, TEAM −48%, CRM/ADBE/WDAY/ZS −34 to −37%). Apply-forward: prefer consumption-priced SaaS over
  seat-based when the AI narrative bites.
- **Ranking holds/sharpens: CTSH > TCS (services); INTU is a DIFFERENT bet, not a 3rd services data point.**
  Vulnerability HIGH TCS≈CTSH > MEDIUM INTU. Priced-in: INTU≈CTSH (a lot) > TCS (moderate, 7x book = NO
  cushion). CTSH = deep-value w/ margin of safety (1.3x book, net cash, revenue re-inflected); TCS =
  quality but no cushion + decline already in P&L → WATCH; INTU = most asymmetric+contested, trap tail is
  segment-specific (TurboTax ~25% of biz) + partly offset by AI upsell it controls (TT Live +47%). Single
  signal to watch: INTU→TurboTax units + QuickBooks growth; CTSH→book-to-bill holding ≥1.0x; TCS→cc rev
  re-accelerating to mid-single-digits (margin-on-shrinking-base = the trap signature).
- **Two brief data points DEBUNKED (don't reuse)**: Klarna "killed SaaS" was recanted by its CEO
  (TechCrunch 2025-03-04); the "Claude Cowork 2026-03-05 → INTU −11%" event is conflated/unsupported.
  Also ADBE/ZS "−42/−43%" were 52-week not YTD (YTD −37/−34%). Behavioral tell: ACN stopped disclosing
  GenAI bookings; TCS discontinued client-concentration/book-to-bill — reduced transparency where the
  thesis needs it most.

_Cheap × secular-trend matrix, 2026-07-04 (Claude Opus 4.8). Detail: `screens/sector_trends.md`._
- **The exciting secular trends are ALREADY EXPENSIVE — value lives in the trends nobody wants to pay for**
  (core finding, cheapness VERIFIED Damodaran / trends web-cited 2025-26). Defense, Electrical Equipment,
  Semis, Semi-Cap, Machinery, Metals&Mining, Precious Metals, IPPs, uranium miners all sit at the **80-95th
  pctile of their OWN 11-yr valuation range** across US/Global/EM. Great durable trends (NATO 5%-by-2035 +
  Germany's permanent debt-brake carve-out; IEA datacenter power ~doubles to 945 TWh by 2030; copper LT
  deficit) but no value — GE Vernova ~+700%/40-45× fwd, Rheinmetall ran +150-190% then rolled over,
  Cameco trailing P/E ~92. Rule: a durable trend ≠ an investable trend; check the own-history percentile first.
- **The 4 genuine SWEET SPOTS (cheap + durable tailwind + decent quality)** = (1) **Oil/Gas E&P/Integrated**
  (US E&P EV/EBITDA 5.1×/31st pctile/ROIC 13.7%/xsec 0.5; EM Integrated ROIC 20%) — supply-side
  underinvestment (upstream capex −4% in 2025 to <$570B vs ~$738B/yr needed by 2030) + LNG; caveat = 2026-27
  glut can make it early. (2) **EM Life Insurance** (5th-pctile EV/EBITDA, ROIC 15%/ROE 17.6%/xsec 6) — aging
  + Asia protection gap + rates-normalized; ride the LIFE leg not P&C. (3) **US Building Materials** (comp 23,
  ROIC 20%, US P/E 5th pctile) — reshoring/infra floor; buy CRH/Eagle not the pricey Vulcan/Martin Marietta.
  (4) **Information Services** (5th-pctile EV/EBITDA, ROIC 22%) — AI *sentiment* discount on moaty ratings/
  index franchises; segment-select (buy franchises, avoid pure data vendors). → maps to CNOOC/EOG, CPIC,
  Buzzi finalists respectively.
- **The AI axis is a beneficiary-vs-victim SPLIT** (VERIFIED, ties to theme_ai_deflation.md): the *victim*
  side (IT/Computer Services) is cheap-but-declining = **TRAP** (CTSH/TCS — value only with a balance-sheet
  cushion); the *protected/beneficiary* side (Info Services ratings franchises; some consumption-SaaS) is the
  sweet-spot. Don't treat "AI" as one directional trend.
- **Confirmed TRAPS (cheap, trend against)**: Cable TV (secular cord-cut), Food Processing (GLP-1/MAHA), IT
  Services (AI-deflation victim), AI-edtech. **Green/Renewable trend MATERIALLY WEAKENED** — OBBBA (Jul 2025)
  repealed EV/solar/wind credits, $34.8B of 2025 clean-energy cancellations (~3:1 vs new) → no longer a clean
  tailwind. Reshoring growth-RATE has faded too (US mfg-construction −30% from Sep-2024 peak) even though the
  LEVEL stays ~2× pre-2020; premium beneficiaries priced for continued boom.

_Information Services franchise deep dive (SPGI/MCO/MSCI), 2026-07-05 (Claude Opus 4.8). Detail:
`deep_dives/info_services/comparison.md`; live data `deep_dives/info_services/live_data.json`._
- **The Info-Services "5th-pctile EV/EBITDA / 22% ROIC" SWEET-SPOT read was a Damodaran SECTOR-AVERAGE
  artifact — it does NOT transfer to the franchises** (VERIFIED, live yfinance 2026-07-05). Sector avg
  ~11.5× is dragged down by the CHEAP pure data vendors (FactSet 10.9×, Morningstar 12.0×) — the very names
  the screen said to AVOID. The moaty franchises trade at **EV/EBITDA SPGI 18.3× / MCO 24.1× / MSCI 26.3×,
  trailing P/E 28/35/35, FCF yield 3–4%** = "great business at a FAIR-TO-FULL price," NOT deep value. The
  22% ROIC IS confirmed/exceeded at company level (MCO ~30% clean; MSCI far higher; SPGI reported ~11% but
  goodwill-diluted by IHS Markit — ex-goodwill high). Apply-forward: never quote a Damodaran sector-average
  multiple as if it describes the sector's quality leaders — the average pools the cheap laggards with the
  premium franchises.
- **The AI de-rating hit ONLY SPGI at the price level; it's a multiple story, not a fundamentals story**
  (VERIFIED). SPGI ~−17.5% TTM (P/E ~40→~28, AI-fear-attributed [A]); MCO ~−2.9% (P/E 35 vs 39); MSCI ~flat
  (P/E 34.5 vs 46 five-yr, off a 70× 2021 peak). Retention is stable-to-RISING across all three (MSCI
  firm-wide 94.4%→95.4% Q1'26, incl. the "at-risk" Analytics/ESG lines) — no churn/pricing damage in the P&L
  yet. Same "fear ahead of the P&L" pattern as the AI-deflation IT-services names, but on PROTECTED assets.
- **AI-threat ranking = SPGI (most, via Market Intelligence/Capital IQ ~32%, the pure-data leg) > MCO
  (Moody's Analytics risk, but ratings-duopoly-protected + best AI monetization: 40% of MA ARR GenAI-enabled,
  97% GenAI-buyer retention) > MSCI (least — index/ETF network moat LLMs can't touch, BlackRock deal to 2035;
  weakest AI-offense at ~$15-20M)** (VERIFIED mix; A monetization). Regulatory moat intact: 10 NRSROs, Big
  Three 93.4% of ratings YE2024, LLMs can't issue a regulatorily-recognized rating. Ratings ride ISSUANCE
  volume (US corp issuance +21% YoY 2026-YTD) not rate cuts (Fed PAUSED at 3.50-3.75% all 2026).
- **Ranked verdict: SPGI 7.30 > MCO 7.20 > MSCI 7.15 (all clustered).** SPGI wins on being the ONLY one AI
  sentiment actually discounted (best quality-at-a-price + margin of safety); MCO = highest-quality/
  lowest-AI-risk but no discount (full price); MSCI = best business (55% op margin) but most expensive
  (worst entry). Honest framing: quality-at-a-price, NOT deep value — margin of safety is cash-flow
  durability, not a low multiple. GOTCHA: MCO P/B 28.6 and MSCI NEGATIVE book equity (−$2.8B) are
  buyback-driven (asset-light returning ~all capital), NOT distress — use ROIC/FCF, ignore P/B & ROE.

_Managed-care trio deep dive (ELV/CI/UNH), 2026-07-05 (Claude Opus 4.8). Detail:
`deep_dives/managed_care/comparison.md`._
- **The "managed care is cheap" narrative is TRUE but company-specific — CI is the clean value, UNH is
  NOT cheap** (VERIFIED, live yfinance + EDGAR FY2025). Fwd P/E CI 8.6 / ELV 14.3 / **UNH 20.3**. UNH's
  trailing 32× is optical — 2024-25 earnings collapsed (NI $22.4B 2023 → $14.4B 2024 → $12.1B 2025, GAAP
  EPS $13.23); fwd 20× is ~fair vs its own history, on TROUGH earnings. CI is genuinely cheap on every
  axis (EV/EBITDA 7.4, P/B 1.80, ROE 16%, ~9% FCF yld) BECAUSE it's services-heavy (Evernorth/Express
  Scripts PBM ~70% of profit), sold its Medicare book, and is exiting ACA — so the MA-cost-trend and
  DOJ-billing fears mostly DON'T apply to it. Its low multiple = sector-tar-brush contagion, not breakage.
- **The MA medical-cost-trend spike (2024-25) is STABILIZING in 2026, not accelerating** (VERIFIED, SEC
  8-Ks). FY25 MLR: CI 84.4% < UNH 89.1% < ELV 90.0% < HUM 90.4% < CNC 91.9%. 4 of 5 raised/reaffirmed
  FY26 guidance at Q1'26; UNH CFO "elevated but not accelerating." Tailwinds: CY2026 MA final rate +5.06%
  (~$25B, big jump from +2.23% draft), plan-footprint discipline (MA plans −9%). CY2027 final smaller at
  +2.48%. GOTCHA: Q1 always prints lowest MLR (deductible reset) — sub-88% Q1 figures are seasonality.
- **UNH's swing risk is the DOJ probe, and it's UNIQUE to UNH** (VERIFIED, 8-K 2025-07-24 accession
  0000731766-25-000224): OPEN criminal + civil DOJ Medicare-billing/upcoding investigation targeting the
  risk-adjustment coding engine at the heart of the Optum model — no charge/settlement/DPA as of mid-2026.
  Plus older civil FCA (Poehling, ~$2.1B alleged; Special Master recommended SJ FOR UNH 2025-03, ruling
  pending). CI/ELV NOT named. This is why UNH stays AVOID despite the widest moat + best AI story.
- **Forward headwind has ROTATED from MA to Medicaid+ACA — that's ELV/CNC's problem, not CI's** (VERIFIED).
  ACA enhanced premium tax credits EXPIRED end-2025 (not extended); CVS/Aetna exited ACA 2026, Cigna
  exiting all ACA states 2027 (walking away from the fire). Medicaid rate-lag forced ELV FY25 adj EPS cut
  ~$34.50→$30.00; Centene withdrew all FY25 guidance. Exposure most→least: CNC ≫ ELV > UNH > CI.
- **AI-admin tailwind is real but overstated in the sector note — and it's a UNH story** (VERIFIED as
  claims). UNH: ~$1.5B AI initiatives 2026, ~$1B AI-enabled cost-out, pharmacy prior-auth >8hr→<30sec.
  CORRECTION: the "95% claims auto-adjudicated" figure is EXISTING straight-through processing, NOT AI —
  don't credit it to AI. Same AI is a LIABILITY: nH Predict/PxDx denial class actions past MTD (UNH, CI,
  HUM named; ELV cleaner), plus CMS-4201-F + CA SB 1120 require a physician (not AI) to deny care.
- **Ranked verdict: CI 7.3 (BUY-candidate, best quality-first value) > ELV 6.6 (WATCH, cyclical recovery
  bet) > UNH 6.2 (AVOID for now — best business, wrong price, live DOJ probe).** Watch: (1) DOJ probe
  resolution; (2) next 1-2 quarters' MA MLR through the CY2026 100% V28 final phase-in.
