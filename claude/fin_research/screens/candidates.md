# Stage 2.6 — Consolidated, Region-Balanced Candidate List + Locked Finalists

Run: 2026-07-02 by Claude (Opus 4.8). Owner: Hooman Shariati. **Not financial advice.**

> **This SUPERSEDES the 2026-07-02 v1 of this file** (which merged only Stage 1a + Stage 1b,
> before the broadened ex-US/EM and financials screens existed). It rebuilds the three buckets
> across the **full global universe** and ends in a **locked ~15-name, region-balanced finalist
> list** for Stage-4 deep dives. Reproduce: `python3 screens/consolidate_candidates.py`.

This consolidates **all four screens**:

1. **Stage 1a — sector cheapness** (`screens/sector_cheapness.md` +
   `data/damodaran/history/sector_cheapness_{US,Global,Emerging}.csv`, **as-of 2026-01-05**,
   Damodaran annual simple-avg industry multiples, 11-yr history). Supplies the *cheap-and-
   not-dying* sector verdicts and the *trap* (Cable TV / Food Processing / AI-edtech) exclusions.
2. **Stage 1b — US-heavy cheap-quality non-financials** (`screens/quant_screen.md` +
   `quant_screen_ranked.csv`, **as-of 2026-07-02**). Folded into #3.
3. **Stage 2.5a — broad ex-US/EM non-financials, global re-rank** (`screens/quant_screen_exus.md`
   + **`quant_screen_global_merged_ranked.csv`**, **as-of 2026-07-02**). The **1,067-rankable-name
   global union** — used as the **PRIMARY non-financials ranking** (most complete).
4. **Stage 2.5b — financials** (`screens/financials_screen.md` + `financials_screen_ranked.csv`,
   **as-of 2026-07-02**). Banks/insurers/REITs, ranked within region × sub-group — the only
   screen that can see the confirmed **EM Life-Insurance leaders**.

> **Anti-hallucination.** Every number in the tables below is **copied from those ranked CSVs**
> (pulled by `consolidate_candidates.py` at runtime, not typed) — nothing refetched, nothing
> invented; each carries a source + as-of date. yfinance figures are **VERIFIED** real fetches
> but **UNVERIFIED** vs a second source (EDGAR/filings) — that cross-check is a Stage-4 job.
> Damodaran sector verdicts are **VERIFIED**. Bucketing + the A↔B sector join are my **judgment**
> (see Method). Confidence marks: VERIFIED / ASSUMED / UNVERIFIED as noted.

---

## What changed vs the stale v1 (the ex-US/EM flip)

The v1 BOTH bucket was **developed-only, zero EM**, and its whole ranking was US-heavy — because
the v1 non-financials universe was 503 US vs 94 dev-exUS + 42 EM (a **universe-construction
artifact**, per LEARNINGS). This refresh rebuilds on the **1,128-name global union** (§3 of
Stage 2.5a). The result flips:

- **Global cheap-quality top tier is now ex-US/EM-led.** The top of the merged ranking is
  **CNOOC (#1), Newmont (#2), Kinross (#3), Endeavour (#4), Barrick (#5), PDD (#7), NetEase (#8),
  Fresnillo (#9), Coal India (#10), Pop Mart (#11)** — 8 of the top 11 are ex-US/EM.
- **The BOTH bucket is no longer developed-only.** With the fuller universe, EM/dev-ex-US names
  enter BOTH directly (BZU.MI Buzzi, TCS.NS Tata Consultancy, AZZA3.SA, Japanese IT/staples).
- **The EM Life-Insurance A-only sector now HAS surfaced leaders** (from screen #4): China
  Taiping, CPIC, NCI, China Life, PICC — the v1 "TBD Stage 3" is resolved to real names.
- **Cheap developed-ex-US financials surfaced** (Intesa/UniCredit, DNB, NatWest, Swiss/Munich/
  Hannover Re) — none existed in v1 (financials were unscreenable then).
- Net: the locked finalists are now **US 5 / dev-exUS 5 / EM 6** instead of a US-crowded list.

---

## The buckets — method in one paragraph

Every trap-gate-**passing** non-financials name (from the merged global ranking) is tagged by
whether its GICS/yf sector is on the Stage-1a **cheap-and-not-dying shortlist**, region-matched,
via a small **curated industry→Damodaran map** (`consolidate_candidates.py`, reused from v1). That
gives **BOTH** (1a-cheap sector **and** 1b gate PASS, region-matched — highest conviction),
**B-only** (elite cheap-quality, combined score ≥ 66, but sector *not* 1a-cheap — Hooman's
explicit "great company on sale anyway" case), and **A-only** (1a-cheap EM sectors — now *filled*
from the broadened screens, incl. financials). **Value-trap gate:** any gated name in a 1a
structurally-declining sector (Cable TV, Food Processing, AI-edtech) is **DEMOTED** (see Demoted
table). Result: **BOTH = 52, B-only(≥66) = 116, DEMOTED = 24.**

---

## BUCKET 1 — BOTH (highest conviction: cheap-quality name in a 1a cheap-not-dying sector)

52 names qualify; top ~18 shown, ranked by merged global combined score. `EY` = earnings yield
(EBIT/EV). MktCap is **native currency — do not compare cross-currency without FX.** `ROIC*` =
proxy flagged unreliable (>100%, buyback-depressed) → rank on ROE. All company metrics yfinance
**as-of 2026-07-02** (`quant_screen_global_merged_ranked.csv`); sector verdict Damodaran+web
**as-of 2026-01-05**. Full list: `data/candidates_both.csv`.

| Ticker | Name | Region | 1a sector (verdict) | MktCap | ROE | OpMgn | EY | EV/EBITDA | P/E | P/B | Piotr | Score |
|---|---|---|---|--:|--:|--:|--:|--:|--:|--:|:--:|--:|
| BZU.MI | Buzzi | DEV_EXUS | Building Materials (cyclical) | 8B EUR | 13.4% | 22.8% | 14.5% | 6.0 | 8.9 | 1.2 | 7/7 | **79.1** |
| CTSH | Cognizant | US | Information Services (AI-sentiment) | 19B USD | 14.9% | 15.6% | 17.5% | 4.9 | 8.9 | 1.3 | 7/7 | **76.7** |
| RI.PA | Pernod Ricard | DEV_EXUS | Beverage (Alcoholic) | 16B EUR | 8.6% | 30.5% | 11.0% | 9.7 | 11.3 | 1.0 | 6/7 | **73.3** |
| ACN | Accenture | US | Information Services | 80B USD | 24.4% | 17.0% | 15.5% | 6.2 | 10.5 | 2.5 | 7/7 | 71.5 |
| AZZA3.SA | Azzas 2154 | EM | Shoe (EM consumer) | — BRL | 10.5% | 5.8% | 10.2% | 4.9 | 4.2 | 0.4 | 6/7 | 68.1 |
| HEI.DE | Heidelberg Materials | DEV_EXUS | Building Materials | — EUR | 11.1% | 17.6% | 10.6% | 8.7 | 15.0 | 1.6 | 6/7 | 68.0 |
| BEI.DE | Beiersdorf | DEV_EXUS | Household Products | — EUR | 11.2% | 11.2% | 7.7% | 8.9 | 18.1 | 2.0 | 6/7 | 67.6 |
| BF-B | Brown-Forman | US | Beverage (Alcoholic) — *wine/spirits* | — USD | 17.8% | 23.2% | 6.5% | 11.9 | 16.9 | 2.9 | 7/7 | 67.3 |
| 6702.T | Fujitsu | DEV_EXUS | Information Services (IT svcs) | — JPY | 15.6% | 13.1% | 8.6% | 10.9 | 19.1 | 2.9 | 6/7 | 66.7 |
| 8113.T | Unicharm | DEV_EXUS | Household Products | — JPY | 7.7% | 13.4% | 8.7% | 9.3 | 27.6 | 2.1 | 7/7 | 65.8 |
| JKHY | Jack Henry | US | Information Services (fintech data) | 10B USD | 24.9% | 24.4% | 6.0% | 14.3 | 19.9 | 4.8 | 7/7 | 65.1 |
| PUIG.MC | Puig Brands | DEV_EXUS | Household Products | — EUR | 16.6% | 18.4% | 9.3% | 10.4 | 16.0 | 2.4 | 7/7 | 64.1 |
| RKT.L | Reckitt Benckiser | DEV_EXUS | Household Products | — GBp | 44.2% | 26.7% | 9.8% | 10.3 | 10.3 | 4.2 | 4/7 | 63.5 |
| DGE.L | Diageo | DEV_EXUS | Beverage (Alcoholic) | 33B GBp | 19.7% | 31.3% | 10.8% | 9.2 | 18.1 | 3.8 | 5/7 | 62.6 |
| CPR.MI | Campari | DEV_EXUS | Beverage (Alcoholic) | — EUR | 8.6% | 17.4% | 6.3% | 11.2 | 18.8 | 1.7 | 6/7 | 62.0 |
| HEN3.DE | Henkel | DEV_EXUS | Household Products | — EUR | 9.7% | 12.0% | 7.9% | 9.5 | 15.3 | 1.5 | 6/7 | 62.9 |
| TCS.NS | Tata Consultancy | EM | Information Services (IT svcs) | 7,173B INR | 48.4% | 25.3% | 9.8% | 9.8 | 14.6 | 6.7 | 7/7 | 74.1† |
| MNST | Monster Beverage | US | Beverage (Soft) | — USD | 26.7% | 31.0% | 3.0% | 32.7 | 47.0 | 10.9 | 7/7 | 60.6 |

† TCS.NS combined score 74.1 sits higher than several rows above but is region-gated as an EM
BOTH name (1a Information-Services cheapness is US/Global — TCS is the EM leg of the same thesis).

**Read:** the BOTH bucket is **Information Services (CTSH, ACN, Fujitsu, JKHY, + EM TCS) + staples/
household (Pernod, Diageo, Campari, Beiersdorf, Unicharm, Reckitt, Puig) + Building Materials
(Buzzi, Heidelberg)**. The genuinely cheap-*and*-high-return pairings are **Cognizant** (EY 17.5%,
EV/EBITDA 4.9, 7/7) and **Buzzi** (EY 14.5%, EV/EBITDA 6.0, P/B 1.2, 7/7 — the one Building-
Materials name that actually screens cheap, vs trough-priced US aggregates VMC/MLM at P/E 35+).
**TCS** is the EM standout (48% ROE). Beverages/household are quality compounders on a *relative*
sale (rich absolute multiples) — buy the pricing-power leader, not deep value.

---

## BUCKET 2 — B-only (elite cheap-quality in a sector that is NOT 1a-cheap)

The top of the whole merged ranking lives here — highest combined scores in the universe, in
sectors (Energy, Materials/miners, value-tech, Chinese internet, biopharma) Stage-1a did **not**
flag cheap-vs-own-history. Exactly the bottom-up catch Hooman wants. Top ~24 shown (116 names
≥ 66; full list `data/candidates_bonly.csv`). All yfinance **as-of 2026-07-02**.

| Ticker | Name | Region | Sector / industry | MktCap | ROE | EY | FCFy | EV/EBITDA | P/E | P/B | Piotr | Score |
|---|---|---|---|--:|--:|--:|--:|--:|--:|--:|:--:|--:|
| 0883.HK | CNOOC | EM | Energy / Oil&Gas E&P (China) | 970B HKD | 15.3% | 23.6% | 6.8% | 3.1 | 6.9 | 1.0 | 7/7 | **90.6** |
| NEM | Newmont | US | Materials / Gold | 100B USD | 25.8% | 15.9% | 9.8% | 5.9 | 12.1 | 2.9 | 7/7 | **87.1** |
| K.TO | Kinross Gold | DEV_EXUS | Materials / Gold (Canada) | 40B CAD | 35.5% | 11.3% | 7.1% | 7.8 | 10.1 | 3.1 | 7/7 | **86.0** |
| EDV.L | Endeavour Mining | DEV_EXUS | Materials / Gold (UK/W.Afr) | ~9.5B GBP | 31.1% | 25.9% | 16.4% | 3.5 | 14.9 | 3.8 | 7/7 | 84.3 |
| ABX.TO | Barrick Mining | DEV_EXUS | Materials / Gold (Canada) | 87B CAD | 25.2% | 11.3% | 6.0% | 8.0 | 10.1 | 2.2 | 7/7 | 84.0 |
| PDD | PDD Holdings | EM | Cons. Disc. / Internet Retail | 117B USD | 25.4% | — | 61%⚠ | (net-cash) | 8.7 | 1.9 | 7/7 | 83.7 |
| NTES | NetEase | EM | Comm. Svcs / Gaming (China) | 83B USD | 22.1% | 18.2% | 41.1% | 6.4 | 16.7 | 17.1 | 7/7 | 82.8 |
| FRES.L | Fresnillo | DEV_EXUS | Materials / Silver (UK/MX) | ~21B GBP | 33.9% | 13.0% | 8.6% | 7.4 | 19.9 | 6.0 | 7/7 | 81.9 |
| COALINDIA.NS | Coal India | EM | Energy / Thermal Coal (India) | 2,705B INR | 28.1% | 15.5% | 2.7% | 5.5 | 8.7 | 2.3 | 7/7 | 81.2 |
| 9992.HK | Pop Mart | EM | Cons. Disc. / Leisure (China) | 203B HKD | 77.6% | 9.3% | 4.5% | 10.9 | 13.9 | 8.0 | 7/7 | 81.1 |
| TME | Tencent Music | EM | Comm. Svcs (China) | 14B USD | 12.0% | — | 32.5% | (net-cash) | 10.3 | 1.2 | 7/7 | 80.8 |
| AEM.TO | Agnico Eagle | DEV_EXUS | Materials / Gold (Canada) | 110B CAD | 22.3% | 7.9% | 3.9% | 11.3 | 14.6 | 3.0 | 7/7 | 80.7 |
| EOG | EOG Resources | US | Energy / E&P | 68B USD | 18.2% | 12.2% | 4.2% | 5.8 | 12.6 | 2.2 | 7/7 | 79.1 |
| CF | CF Industries | US | Materials / Ag Inputs | 17B USD | 27.3% | 11.8% | 6.5% | 6.1 | 9.7 | 3.1 | 7/7 | 78.0 |
| INTU | Intuit | US | Technology / Software | 73B USD | 22.5% | 13.4% | 7.2% | 11.4 | 16.3 | 3.6 | 7/7 | 78.0 |
| APA | APA Corp | US | Energy / E&P | 11B USD | 26.2% | 19.6% | 15.0% | 3.2 | 7.4 | 1.7 | 5/7 | 77.5 |
| TSM | Taiwan Semiconductor | EM | Technology / Semis (Taiwan) | 2.3T USD | 36.2% | 14.7% | 31.2% | 5.7 | 38.6 | 99.8† | 7/7 | 77.5 |
| CPRT | Copart | US | Industrials / Salvage auctions | 28B USD | 17.6% | 7.7% | 3.6% | 11.5 | 17.9 | 3.0 | 7/7 | 77.4 |
| EXE | Expand Energy | US | Energy / Nat gas E&P | 21B USD | 17.6% | 18.2% | 7.9% | 3.3 | 6.7 | 1.1 | 7/7 | 77.0 |
| FMG.AX | Fortescue | DEV_EXUS | Materials / Iron ore (AU) | 58B AUD | 18.7% | 9.5% | 5.5% | 7.3 | 10.8 | 1.9 | 7/7 | 76.9 |
| ITC.NS | ITC Ltd | EM | Cons. Staples / Tobacco+FMCG (India) | 3,637B INR | 29.3% | 8.4% | 3.6% | 12.6 | 17.6 | 5.0 | 6/7 | 76.8 |
| EQT | EQT Corp | US | Energy / Nat gas E&P | 33B USD | 13.4% | 12.7% | 7.6% | 5.5 | 10.0 | 1.3 | 6/7 | 76.7 |
| BIDU | Baidu | EM | Comm. Svcs / Internet (China) | 40B USD | 0.3% | 31.4% | 19.8% | (net-cash) | — | 1.0 | 6/7 | 76.6 |
| RMD | ResMed | US | Health Care / Med devices | 29B USD | 25.2% | 6.9% | 5.0% | 13.4 | 19.4 | 4.5 | 7/7 | 74.8 |

⚠ PDD FCF-yield and † TSM P/B are known ADR/net-cash data artifacts (flagged in Stage 2.5a) —
verify at deep dive; do not let them drive ranking. Also in B-only lower down: Tenaris, Otsuka,
Incyte, Deckers, Suncor, BHP, Petrobras, HIG, ACGL, Indofood-CBP-if-not-demoted, Wipro/Infosys.

**Read:** the strongest bottom-up names cluster in **gold/base-metal miners** (Newmont, Kinross,
Endeavour, Barrick, Agnico, Fresnillo, Fortescue — rank these on **ROE**, not the ROIC-proxy which
inflates >100% for buyback-heavy miners per LEARNINGS), **energy E&P** (CNOOC #1, EOG, APA, EXE,
EQT — EV/EBITDA 3–6, EY 12–24%, strong FCF), **cheap Chinese internet** (PDD, NetEase, Tencent
Music, Baidu — net-cash, de-rated), **value-tech/QARP** (Intuit, TSM), and **EM value-staples**
(ITC, Coal India). Genuinely cheap + high-quality even though their *sector* isn't 1a-cheap.

---

## BUCKET 3 — A-only (1a cheap-not-dying EM sectors — now FILLED from the broadened screens)

v1 left these as "TBD Stage 3." With the broadened universe + the financials screen, most now have
a surfaced leader. Best gated name per sector (`data/candidates_afill.csv`). Financials from
`financials_screen_ranked.csv`; others from the merged non-financials ranking. All **as-of
2026-07-02**; sector verdict Damodaran **2026-01-05**.

| 1a EM sector | Best surfaced leader | Region | Key metrics | Status |
|---|---|---|---|---|
| **Insurance (Life)** — top cheap-EM | **0966.HK China Taiping**; also 2601.HK CPIC, 1336.HK NCI, 2628.HK China Life, 1339.HK PICC | **EM (China/HK)** | Taiping P/B **0.71**, ROE **25.5%**, P/E 2.6, 6.8% yld, PASS; CPIC 0.72 P/B, ROE 17.4% | ✅ **FILLED** (screen #4). CONFIRMED cheap-quality cohort. See trough caveat below. |
| **Transportation (Railroads)** | 9022.T Central Japan Railway (P/E 6.0, EV/EBITDA 7.0, 27% OM, 7/7, sc 69) | **DEV_EXUS (Japan)** | No **EM** railroad cleared the gate at quality | ⚠️ **Partial** — a dev-ex-US quality operator exists; **EM railroads still lack a surfaced quality leader.** |
| **Shoe** | 9910.TW Feng Tay (ROE 16.7%, EV/EBITDA 7.4, sc 54.8); AZZA3.SA (cheap, low quality, in BOTH) | **EM (Taiwan/Brazil)** | Feng Tay is a Nike OEM; Deckers (US, sc 74) is the global quality leader but not EM | ✅ **FILLED** (mid-quality EM); DECK is the non-EM quality alt. |
| **Retail (Automotive)** | 2207.TW Hotai Motor (sc 41.8, weak); 0881.HK Zhongsheng = negative ROE (trap) | EM (Taiwan/China) | Low ROE sector-wide, as 1a warned (ROIC 3.7%) | ⚠️ **Weak** — no strong quality leader; be selective / likely skip. |
| **Retail (Building Supply)** | KGF.L Kingfisher (UK, sc 55.6, ROE 3.9% — thin) | DEV_EXUS (UK) | Low ROE | ⚠️ **Weak** — no EM quality leader surfaced. |
| **Trucking** | ODFL (US, sc 52.1) only | US | — | ❌ **EM trucking still empty** — no EM name surfaced. |
| **Education** | none gated | — | — | ❌ **Still empty** — no regulated-EM-tutoring survivor surfaced (New Oriental-type not in universe). |

**Read:** the **EM Life-Insurance** A-only gap — the highest-priority cheap-EM sector — is now
**resolved to real names** (the China/HK life cohort). The transport/consumer EM sectors are
**still thin or empty** (Railroads has only a Japanese operator; Trucking/Education have no EM
quality leader) — consistent with 1a's warning that these are cheap but low-ROIC. If Hooman wants
those covered, the universe needs sub-index-cap EM breadth (a paid API), per LEARNINGS.

---

## THE LOCKED FINALISTS — ~15 region-balanced, sector-diversified (feeds Stage 4)

**Region mix: US 5 / dev-ex-US 5 / EM 6 = 16 names** (a touch over 15 to carry two EM Life names
per the brief). Sector caps applied: **max 2 miners** (NEM, K.TO), **max 2 energy** (EOG, CNOOC),
**max 2 IT-services** (CTSH, TCS), so the list isn't 10 gold miners even though metals screen
cheap. Numbers pulled from the ranked CSVs (`data/finalists.csv`); MktCap native currency.

| # | Ticker | Name | Region | Sector | Bucket | ROE | EV/EBITDA | P/E | P/B | Score/Trap | One-line thesis + why it made the cut |
|--:|---|---|---|---|---|--:|--:|--:|--:|--:|---|
| 1 | **CTSH** | Cognizant | US | IT Services | BOTH | 14.9% | 4.9 | 8.9 | 1.3 | 76.7 / 7/7 | Cheap moaty IT-services in the 1a-cheap Information-Services sector (AI-sentiment overhang); EY 17.5%. Highest-conviction US BOTH. |
| 2 | **NEM** | Newmont | US | Gold miner | B-only | 25.8% | 5.9 | 12.1 | 2.9 | 87.1 / 7/7 | #2 globally; best-quality large US gold major. Rank on ROE not inflated ROIC-proxy. |
| 3 | **EOG** | EOG Resources | US | Energy E&P | B-only | 18.2% | 5.8 | 12.6 | 2.2 | 79.1 / 7/7 | Best-quality US E&P (EY 12%, strong FCF). Cheap in a non-1a-cheap sector. |
| 4 | **INTU** | Intuit | US | Software (QARP) | B-only | 22.5% | 11.4 | 16.3 | 3.6 | 78.0 / 7/7 | Cleanest US compounder-on-sale: ROIC 38%, 81% GM, EY 13%. |
| 5 | **TROW** | T. Rowe Price | US | Asset manager | B-only | 18.7% | — | 12.5 | 2.3 | 81.9 / PASS | Fortress asset manager, 4.6% yield, cheap-quality financial; top-of-US in the financials screen. |
| 6 | **K.TO** | Kinross Gold | dev-exUS | Gold miner | B-only | 35.5% | 7.8 | 10.1 | 3.1 | 86.0 / 7/7 | #3 globally; diversifies miner exposure into Canada. Rank on ROE. |
| 7 | **BZU.MI** | Buzzi | dev-exUS | Building Materials | BOTH | 13.4% | 6.0 | 8.9 | 1.2 | 79.1 / 7/7 | Italian cement in 1a-cheap Building-Materials that *actually* screens cheap (EY 14.5%, P/B 1.2) — unlike trough-priced US aggregates. |
| 8 | **DGE.L** | Diageo | dev-exUS | Bev-Alcoholic | BOTH | 19.7% | 9.2 | 18.1 | 3.8 | 62.6 / 5/7 | Dev-ex-US spirits leader in the 1a-cheap Beverage-Alcoholic trough; 31% op margin, EY 10.8%. |
| 9 | **ISP.MI** | Intesa Sanpaolo | dev-exUS | Bank (Italy) | A-fill/fin | 14.0% | — | 11.1 | 1.5 | 82.1 / PASS | Best cheap dev-ex-US bank: 1.5x book, 6.3% yield. Diversifies into dev-exUS financials. |
| 10 | **SREN.SW** | Swiss Re | dev-exUS | Reinsurer | B-only/fin | 19.5% | — | 10.3 | 1.8 | 69.4 / PASS | European reinsurer value-with-quality: 1.8x book, ~5% yield — best dev-exUS insurer cohort. |
| 11 | **0883.HK** | CNOOC | EM | Energy (China) | B-only | 15.3% | 3.1 | 6.9 | 1.0 | 90.6 / 7/7 | #1 globally; the single cheapest-and-quality name in the whole run (EY 23.6%, P/B 1.0). |
| 12 | **NTES** | NetEase | EM | Internet (China) | B-only | 22.1% | 6.4 | 16.7 | — | 82.8 / 7/7 | Best-quality cheap Chinese internet: 66% GM, FCFy 41%, net-cash, de-rated. |
| 13 | **TCS.NS** | Tata Consultancy | EM | IT Services (India) | BOTH | 48.4% | 9.8 | 14.6 | 6.7 | 74.1 / 7/7 | EM leg of the 1a-cheap Information-Services sector; ROE 48%, EY 9.8%. The EM BOTH name (region-gated out of v1). |
| 14 | **ITC.NS** | ITC Ltd | EM | Staples (India) | B-only | 29.3% | 12.6 | 17.6 | 5.0 | 76.8 / 6/7 | EM cash compounder on sale: ROIC 45%, 36% op margin, EY 8.4%. |
| 15 | **0966.HK** | China Taiping | EM | Life Insurer (China) | A-fill/fin | 25.5% | — | 2.6 | 0.71 | 65.0 / PASS | The EM Life-Insurance A-only leader (1a's top cheap-EM sector): 0.71x book, 25.5% ROE, +earnings growth — cleanest of the China life cohort. |
| 16 | **2601.HK** | CPIC | EM | Life Insurer (China) | A-fill/fin | 17.4% | — | 4.4 | 0.72 | 57.5 / PASS | Second EM life name (Hooman wants a couple): 0.72x book, ROE 17.4% — matches the 1a sector profile. **FLAG: earningsGrowth −6% = cheap on trough, verify EV/VNB at Stage 4.** |

**Region-balance proof:** US = 1,2,3,4,5 (**5**); dev-ex-US = 6,7,8,9,10 (**5**); EM = 11,12,13,14,15,16
(**6**). **Sector spread:** IT-services 2, miners 2, energy 2, software 1, asset-mgr 1, building-
materials 1, bev-alcoholic 1, bank 1, reinsurer 1, internet 1, staples 1, life-insurer 2. No
sector exceeds 2. The two confirmed EM Life names (Taiping, CPIC) and two cheap dev-ex-US
financials (Intesa bank, Swiss Re reinsurer) are included per the brief.

---

## Trap gate — demoted names (passed 1b gate but sit in a 1a structurally-declining sector)

24 names demoted; top shown. `data/candidates_demoted.csv`. All **Packaged Foods / Food
Distribution / Confectioners** → Damodaran **Food Processing** = 1a SECULAR-lean trap (GLP-1 +
MAHA/FDA UPF crackdown + private label). No Cable-TV or AI-edtech names cleared the 1b gate, so
none needed demoting there.

| Ticker | Name | Region | Industry | EV/EBITDA | Score | Why demoted |
|---|---|---|---|--:|--:|---|
| INDF.JK | Indofood Sukses Makmur | EM | Packaged Foods | 4.9 | 75.2 | Food Processing trap — but see EM caveat below. |
| ICBP.JK | Indofood CBP | EM | Packaged Foods | 6.6 | 74.3 | same — EM caveat. |
| KHC | Kraft Heinz | US | Packaged Foods | 8.1 | 63.9 | GLP-1 + MAHA + private label. |
| ABF.L | Assoc. British Foods | dev-exUS | Packaged Foods | 6.0 | 61.9 | same |
| HRL | Hormel | US | Packaged Foods | 10.7 | 58.5 | same |
| GIS | General Mills | US | Packaged Foods | 6.4 | 57.8 | same |
| ORK.OL | Orkla | dev-exUS | Packaged Foods | 13.0 | 56.9 | same |
| 0322.HK | Tingyi | EM | Packaged Foods | 6.3 | 54.8 | same — EM caveat. |
| MKC | McCormick | US | Packaged Foods | 13.4 | 52.3 | same |
| SJM | J.M. Smucker | US | Packaged Foods | 10.0 | 51.2 | same |
| BN.PA | Danone | dev-exUS | Packaged Foods | 12.3 | 49.5 | same |

> **EM Food-Processing caveat (judgment, ASSUMED):** the 1a Food-Processing *trap* verdict is
> driven by **US/developed** structural forces (GLP-1, MAHA/FDA, US private label). **EM packaged
> foods (Indofood, Tingyi, Nongfu) have a per-capita-consumption growth runway**, so their demotion
> is arguable — they screen genuinely cheap (Indofood EV/EBITDA 4.9, P/B 0.8) and gate-pass. I
> demoted them for consistency with the mapped sector verdict, but flag them as **"cheap on a
> growth-EM staple, revisit if you want EM staples exposure beyond ITC."** Not promoted silently.

---

## Method & limitations

- **Primary non-financials ranking = the merged global re-rank** (`quant_screen_global_merged_
  ranked.csv`, 1,067 rankable): the union of Stage-1b + broadened ex-US/EM, re-scored on one
  common percentile pool (60% quality / 40% cheapness, quality-first). Financials come from the
  separate financials screen (ranked within region × sub-group) — **the two score scales are NOT
  comparable** (percentiles in different pools); a financial's score of 82 means "top of its
  peers," not "cheaper than a miner at 82."
- **The A↔B join is by sector via a curated judgment map** (`consolidate_candidates.py`,
  reused/extended from v1), not a fuzzy auto-match — small and auditable. Region-gated: a US/
  dev-exUS name counts as BOTH only if the Damodaran verdict is US/Global; an EM name needs the
  Emerging verdict (why TCS is the EM BOTH leg of Information Services). **Mapping = ASSUMED.**
- **Two as-of dates:** sector cheapness Damodaran **2026-01-05** (annual simple-avg, ~6 mo stale);
  company metrics yfinance **2026-07-02** (daily-moving). Combined for *bucketing*, not netted.
- **Miner ROIC caveat (LEARNINGS):** the ROIC-proxy inflates >100% for buyback-heavy miners
  (Fresnillo, Pop Mart, Endeavour) — miners are **ranked and judged on ROE** in every table here.
- **China-life "cheap on trough" flag:** several China lifecos show negative `earningsGrowth`
  (China Life −32%, CPIC −6%, PICC Group −35%, Ping An −13%) = the 1a cyclical low-rate/spread
  squeeze — cheap on a *trough*, not broken (ROE still 14–36%, payout covered). China Taiping
  (+earnings growth) and NCI are the exceptions. **Verify embedded value / VNB at Stage 4** — the
  single field yfinance lacks that would resolve trap-vs-bargain (the paid-API trigger, screen #4 §5).
- **Single-source + proxy metrics:** all fundamentals are one yfinance `.info` pull (2026-07-02),
  **not** cross-checked vs filings; no EDGAR backstop for most non-US-listed names; Piotroski is
  "lite" (no YoY deltas); some ADR/net-cash FCF/P/B artifacts flagged. **Every finalist must be
  EDGAR/filings-cross-checked at Stage 4.** Confidence: individual fields VERIFIED; ranking/
  bucketing/finalist-selection ASSUMED.
- **Known empty EM sectors:** EM Trucking, EM Education, EM Auto-Retail (quality) have **no
  surfaced quality leader** — a genuine gap (cheap but low-ROIC sectors + sub-index-cap EM
  coverage limit), not an omission. Flagged above.

**Reproduce:** `/opt/venv/bin/python3 screens/consolidate_candidates.py` →
`data/candidates_{both,bonly,afill,demoted}.csv` + `data/finalists.csv`.
