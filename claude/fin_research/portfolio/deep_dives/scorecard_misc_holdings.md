# Scorecard — Misc / Uncovered Holdings

**Analyst:** Claude (Opus 4.8) | **For:** Hooman (Canadian citizen, quality-first value investor, 3–5yr horizon)
**Date:** 2026-07-07 | **Data source:** yfinance live pull (curl_cffi), timestamps in verification log below.
**Scope:** Holdings NOT covered by the energy / metals / uranium / China / healthcare / AI-megacap agents. SBSW skipped (metals agent).

> **Anti-hallucination note:** Every multiple/price below is a live yfinance `.info` pull today (2026-07-07). Marked **VERIFIED** = pulled live today. yfinance `.info` fields can be stale/wrong on occasion (esp. TTM PE when EPS is negative, ETF fields); anything I flag as suspect is marked **UNVERIFIED**. Confirm anything thesis-critical against EDGAR/company filings before acting.

---

## TL;DR — the whole page in one table

| Ticker | ~$ Pos | Live Px | Q@P (0–10) | Verdict | Thesis-fit |
|---|---|---|---|---|---|
| **GEV** | $9.2k | $1,152 | **6.5** | **TRIM ~1/3** | ✅ electrification/grid (core) |
| **AMZN** | $12.5k | $244 | **7.5** | **HOLD / add on dips** | ✅ AI/cloud (core) |
| **CAG** | ~$4.5k | $13.79 | **4.0** | **TRIM / hold small** | ⚠️ staples-value, GLP-1/PL trap-tilt |
| **KHC** | ~$4.5k | $24.82 | **4.5** | **HOLD (event-driven)** | ⚠️ staples-value, breakup catalyst |
| **CF** | $4.5k | $113.20 | **7.0** | **HOLD** | ✅ commodity/inflation-hedge |
| **PDBA** | $5.1k | $36.76 | **5.5** | **HOLD (diversifier)** | ✅ commodity/inflation-hedge |
| **CRCL** | $2.7k | $68.65 | **3.0** | **SELL or cap as lotto** | ❌ orphan (spec) |
| RBLX | $2.9k | $57.03 | 3.5 | **SELL** | ❌ orphan |
| AA | $2.5k | $49.87 | 5.0 | **SELL (fold into metals sleeve)** | ⚠️ redundant w/ XME + metals agent |
| XME | $2.7k | $106.08 | 5.5 | **HOLD or consolidate** | ✅ commodity, but redundant w/ AA |
| ARKK | $1.3k | $83.61 | 2.5 | **SELL** | ❌ orphan; holds CRCL+TSLA |
| SBUX | $1.0k | $102.11 | 4.0 | **SELL (sub-scale)** | ❌ orphan |
| **TIER 3** (10 names) | <$700 ea | — | 0–3 | **SELL ALL / tax-loss harvest** | ❌ orphans |

---

# TIER 1 — Full scorecards

## GEV — GE Vernova · **Q@P 6.5/10 · TRIM ~1/3**
**Thesis-fit: ✅ CORE.** This IS the "electricity demand up / grid + turbines" thesis. Grid equipment + gas turbines + wind, riding data-center/electrification demand.

**Live (VERIFIED 2026-07-07):** Px $1,152.04 · mktcap $310B · **near 52wk high** ($1,196; low $511 → +125% off the low, matches Hooman's +87% cost-basis gain) · P/B **22.2** · EV/EBITDA **89.2** · P/S 7.9 · trailing PE 33.7 · fwd PE **46.9** · ROE 75.7% · rev growth +16.3% · FCF ~$9.3B · net cash (debt $3.8B vs cash $9.8B) · beta 0.94.

**Read.** Quality of business is real: strong FCF, net-cash balance sheet, structural demand tailwind (grid capex supercycle, gas turbine backlog stretched into the 2030s). But the *price* has run to a level where you're paying for near-perfection: **EV/EBITDA ~89 and fwd PE ~47** are venture-like multiples for an industrial. The +87% gain means the easy money on the re-rate is banked; from here return depends on GEV *growing into* a rich multiple, and any backlog/margin hiccup de-rates it hard.

**Note on the extreme ratios:** operatingMargins 5.5% but profitMargins 23.8% and ROE 75.7% look internally inconsistent (likely one-time/tax items or thin equity base inflating ROE, plus low-margin revenue mix) — treat the exact margin figures as **UNVERIFIED**; the *directional* read (very expensive, high quality, cyclical-industrial) is solid.

**Verdict: TRIM ~1/3.** Keep the thesis exposure, take the win discipline. This is textbook "great company, demanding price." Trimming a third locks gains, funds the Tier-3 cleanup, and keeps you on-thesis. Don't sell it all — the multi-year electrification story is intact. **Do not add here.**

---

## AMZN — Amazon · **Q@P 7.5/10 · HOLD / add on weakness**
**Thesis-fit: ✅ CORE.** Legit AI/cloud winner (AWS + retail + ads). His single largest name here.

**Live (VERIFIED 2026-07-07):** Px $244.16 · mktcap $2.63T · trailing PE 31.8 · **fwd PE 24.7** · P/B 5.9 · **EV/EBITDA 17.4** · P/S 3.5 · ROE 24.3% · gross margin 50.6% · op margin 13.1% · rev growth +16.6% · earnings growth +74.8% · beta 1.46. Well off 52wk high ($278; low $196), so *not* at a euphoric price.

**Read.** For a company compounding revenue mid-teens with 50% gross margins and a fast-growing high-margin AWS+ads mix, **EV/EBITDA ~17 and fwd PE ~25 is reasonable-to-attractive** — this is the cheapest AMZN has looked on forward earnings in years, because margin expansion is outrunning the multiple. It's the closest thing in this list to genuine "quality at a fair price." Not statistically *cheap* (it never is), but you're not overpaying for the quality.

**Redundancy flag:** AMZN is likely his AI/cloud exposure; if the AI-megacap agent's book also carries MSFT/GOOGL/NVDA, watch total AI concentration across the whole portfolio (out of my scope but worth a portfolio-level check).

**Verdict: HOLD, add on any pullback toward the low-$200s / sub-15x EV/EBITDA.** Highest-conviction keep in this list. On-thesis, high quality, fair price.

---

## CAG — Conagra Brands · **Q@P 4.0/10 · TRIM / hold small**
**Thesis-fit: ⚠️ staples-value — but sits squarely in the food-processing GLP-1 / private-label trap the prior research flagged.**

**Live (VERIFIED 2026-07-07):** Px $13.79 · **near 52wk low** ($20.99 high / $12.53 low) · mktcap $6.6B · trailing PE **null (negative TTM earnings)** · **fwd PE 8.6** · P/B **0.81** · EV/EBITDA 8.0 · P/S 0.59 · **div yield 9.76%** · rev growth **−1.9%** · profit margin −0.4% (TTM loss, likely impairment) · **debt/equity 89.8**, totalDebt $7.3B vs cash $55M · beta ~0.

**Read.** This is the classic value-trap signature: sub-book price, single-digit fwd PE, ~10% yield — *the market is pricing a dividend cut and/or continued volume erosion.* A 9.76% yield on a packaged-food name with declining revenue, negative TTM earnings, and $7.3B debt against $55M cash is a **warning, not a bargain**. GLP-1 demand headwinds + private-label share loss + input cost pressure are structural, not cyclical. The FCF (~$655M) technically covers the dividend today, but leverage leaves no margin for error.

**Verdict: TRIM / hold small.** Not an obvious add. If held for the yield, size it small and treat the dividend as at-risk. Given his "too many scattered names" problem and the trap-tilt, I lean toward trimming CAG and consolidating the staples bet into the one with the clearer *catalyst* (KHC breakup) rather than owning both. **Redundant with KHC** — see below.

---

## KHC — Kraft Heinz · **Q@P 4.5/10 · HOLD (event-driven), pick ONE of {KHC, CAG}**
**Thesis-fit: ⚠️ staples-value, same GLP-1/private-label trap — but has a harder catalyst (announced breakup).**

**Live (VERIFIED 2026-07-07):** Px $24.82 · near 52wk low ($29.19 / $21.04) · mktcap $29.4B · trailing PE **null** · **fwd PE 11.9** · P/B **0.70** · EV/EBITDA 8.1 · P/S 1.18 · **div yield 6.31%** · rev growth +0.8% · **profit margin −23% (big TTM impairment/writedown)** · op margin 20.7% · debt $21.1B vs cash $4.1B, debt/equity 50 · beta ~0. FCF ~$3.2B comfortably covers the dividend.

**Read.** Sub-book (0.70x), 6.3% yield, mid-single-digit fwd PE-adjacent. The −23% profit margin is almost certainly a **goodwill/intangible impairment** (the perennial KHC story since 2019), not an operating collapse — op margin is 20.7% and FCF is strongly positive. The differentiator vs CAG: **KHC has an announced/expected structural catalyst (splitting the company)** which is a plausible value-unlock, and its dividend looks better-covered (FCF $3.2B vs ~$1.9B dividend). Still a low-growth, brand-eroding business facing the same GLP-1/private-label secular pressure.

**Verdict: HOLD as the event-driven staples bet.** Between CAG and KHC, **KHC is the keeper** (better coverage, real catalyst); CAG is the trim. Owning both = redundant exposure to the identical thesis and identical structural risk. Consolidate to one, ~$4.5–6k max.

---

## CF — CF Industries · **Q@P 7.0/10 · HOLD**
**Thesis-fit: ✅ commodity / inflation-hedge.** Nitrogen fertilizer; energy-linked (nat-gas feedstock → US Gulf cost advantage). Best-quality name in the commodity sleeve here.

**Live (VERIFIED 2026-07-07):** Px $113.20 · mktcap $17.4B · **trailing PE 10.2 · fwd PE 9.8** · P/B 3.3 · **EV/EBITDA 6.4** · P/S 2.3 · **ROE 27.3% · ROA 11.3%** · gross margin 39% · **op margin 33.6%** · div yield 1.81% · rev growth +19.4% · earnings growth +115% · net-cash-ish (debt $3.6B vs cash $2.0B) · beta 0.39. Mid-range of 52wk ($142 / $75).

**Read.** This is a genuinely *high-quality* commodity operator, not a value trap: 33% operating margins, 27% ROE, single-digit EV/EBITDA, low leverage, and it sits at the low end of the nitrogen cost curve thanks to cheap US nat gas. Multiples are cyclically low because nitrogen prices are off their 2022 spike — that's the nature of a commodity name. Optionality: clean-ammonia / low-carbon hydrogen ambitions. Risk is purely the commodity cycle (nitrogen price, nat-gas cost, Chinese export policy).

**Verdict: HOLD.** On-thesis (commodity/inflation hedge), high quality, cheap on normalized earnings. Don't chase near cycle-peak fertilizer prices, but at ~10x with a fortress cost position it's a legitimate quality-at-a-price hold. **Partial redundancy with PDBA** (both ag) but different exposure: CF = equity/single-company nitrogen producer, PDBA = broad ag *commodity* basket. Complementary, not duplicative.

---

## PDBA — Invesco Agriculture Commodity Strategy No K-1 ETF · **Q@P 5.5/10 · HOLD (diversifier)**
**Thesis-fit: ✅ commodity / inflation-hedge.**

**Live (VERIFIED 2026-07-07):** Px $36.76 (last close) · **div yield 3.11%** · 52wk $38.43 / $33.69 (tight, low-vol range). Top "holding" shows as **Invesco Premier US Govt Money Inst (78%)** — this is expected: PDBA is a **futures-based** ETF; it holds T-bills/money-market as *collateral* and gets ag exposure via commodity futures/swaps through a Cayman subsidiary (the "No K-1" structure = 1099 instead of K-1, tax-convenient). **UNVERIFIED via yfinance:** the actual commodity basket. Per fund methodology it tracks a diversified ag futures index — **corn, soybeans, soybean meal, wheat, sugar, coffee, cocoa, cotton, live cattle, lean hogs** (confirm current weights on Invesco's fact sheet before relying on specifics).

**Read.** A reasonable, low-cost, K-1-free way to hold *broad* agricultural commodities as an inflation/real-asset diversifier. The tight 52wk range shows it's a low-beta ballast, not a growth engine. It earns ~3% on its T-bill collateral, so you're paid to wait. It is NOT a proxy for ag *equities* — it's the raw commodities.

**Verdict: HOLD as a small diversifier.** On-thesis. Complements (does not duplicate) CF. If simplifying, this is a defensible "real-asset" sleeve to keep. Don't expect it to compound like equities; it's ballast.

---

## CRCL — Circle Internet Group (USDC stablecoin issuer) · **Q@P 3.0/10 · SELL or cap as a lottery ticket**
**Thesis-fit: ❌ ORPHAN / speculative.** Doesn't fit energy/AI/commodity/inflation. Pure fintech/crypto-rails speculation.

**Live (VERIFIED 2026-07-07):** Px $68.65 · **crashed from 52wk high $262.97 → near low $49.90 (−74% from high)** · mktcap $18.3B · trailing PE null (unprofitable TTM) · fwd PE 30.6 · P/B 5.0 · **EV/EBITDA −116.7** · P/S 6.4 · **negative FCF (−$141M)** · profit margin −2.8% · rev growth +20% · earnings growth −81% · debt trivial ($15M), cash $1.5B.

**Read.** Circle earns a spread on the reserves backing USDC, so its revenue is essentially **leveraged to short-term interest rates and USDC circulation** — a rate cut cycle compresses the core P&L, and it's already unprofitable on a TTM basis. The stock is a post-IPO deflation: priced for hyper-growth at IPO, re-rated brutally. At 30x fwd earnings that don't yet reliably exist, 6.4x sales, negative FCF, it's a speculative bet on stablecoin adoption + regulatory tailwind (GENIUS-Act-type legislation), NOT a quality-value holding.

**Verdict: SELL,** or if he has genuine conviction on the stablecoin thesis, **hard-cap it as a labeled lottery ticket (≤1% of portfolio)** — never add on the way down. It violates the quality-first mandate. **Redundancy flag: he ALSO owns CRCL indirectly via ARKK (4.5% of ARKK).** Doubling down on the same speculative name through two vehicles.

---

# TIER 2 — Brief verdicts

**RBLX — Roblox · $2.9k · Q@P 3.5 · SELL.** Live: $57.03, **crashed from 52wk high $150.59** (−62%), P/B **94**, EV/EBITDA −40, ROE −312%, profit margin −21%, unprofitable, rev growth +39%. Real user growth but persistently unprofitable at an extreme valuation; pure growth-momentum name, not quality-value. Orphan (no thesis fit). **Sell.**

**AA — Alcoa · $2.5k · Q@P 5.0 · SELL / fold into metals sleeve.** Live: $49.87, trailing PE 12.8, **fwd PE 6.7**, P/B 1.9, EV/EBITDA 8.5, ROE 15.4%, div 0.82%, rev growth −5.2%. Decent cyclical value here, BUT **AA is a 4.6% holding inside XME which he also owns, and metals is covered by another agent** — this is redundant single-name risk. Consolidate: let the metals agent own the aluminum call; **sell the standalone AA** to reduce name-count.

**XME — SPDR Metals & Mining ETF · $2.7k · Q@P 5.5 · HOLD or consolidate to metals agent.** Live: $106.08, PE 20.3, P/B 2.5, div 0.31%. Top holdings CLF/NUE/STLD/RS/**AA**/CMC/USAR/HCC/FCX/MP — steel-heavy + rare-earth exposure. Legit diversified commodity/reshoring vehicle, on-thesis. **Overlaps with AA and with the metals agent's coverage** — coordinate so you're not tripling metals exposure. If keeping one metals vehicle, XME (diversified) beats standalone AA.

**ARKK — ARK Innovation ETF · $1.3k · Q@P 2.5 · SELL.** Live: $83.61 (52wk $92.65/$62.95). Top holdings TSLA 10%, AMD, HOOD, CRSP, TEM, **CRCL 4.5%**, SHOP, ROKU, COIN, PLTR — high-beta unprofitable-growth basket, PE ~50. Orphan, no thesis fit, high fee, **overlaps his direct CRCL and general AI names**. Anti-quality by construction. **Sell.**

**SBUX — Starbucks · $1.0k · Q@P 4.0 · SELL (sub-scale).** Live: $102.11 (**near 52wk high $108.88**), trailing PE **78**, fwd PE 33.9, negative book (buybacks), EV/EBITDA 25.8, div 2.38%, rev growth +8.8%, thin 3.9% margin. Turnaround story priced at a premium multiple; quality is debatable mid-turnaround and it's an orphan at a $1k size. Not worth the slot. **Sell / cleanup.**

---

# TIER 3 — One-line verdicts (micro legacy, mostly 2021 spec, deeply underwater)

**Default: SELL ALL — consolidate away, harvest tax losses (note: TAX RULES ARE CANADIAN — superficial-loss rule = 30 days, similar to US wash-sale; confirm with his situation).** Any "secretly worth keeping" flagged explicitly.

| Ticker | Live (VERIFIED 2026-07-07) | Verdict |
|---|---|---|
| **AEVA** (Aveva/lidar) | $24.20, P/B −123, ROE −516%, unprofitable, but **+86% off lows / rev +86%** | **SELL** — up sharply, no quality; take the bounce, don't hold a cash-burning lidar micro. |
| **AUR** (Aurora Innovation, autonomous trucking) | $6.79, mktcap $13B(!), pre-revenue, ROE −44%, burning cash, $1.2B cash | **SELL** — richest of the group vs fundamentals; pre-revenue speculation. No reason to keep. |
| **CHPT** (ChargePoint) | $6.26 (post reverse-split look), mktcap $153M, margin −50%, EV/EBITDA −1.9, debt>cash | **SELL** — broken EV-charging story, going-concern-ish. Cleanup. |
| **NIO** (China EV) | $5.02, ROE −84%, unprofitable, debt $26.6B; **China = other agent's turf** | **SELL** — hand any China-EV view to the China agent; not a quality hold. |
| **F** (Ford) | $13.83, fwd PE 7.6, div **4.49%**, but ROE −14.8%, TTM loss, debt $160B | **SELL / cleanup** — only Tier-3 name with a real dividend; still low-quality auto, EV losses. No compelling reason to keep at micro size. |
| **LCID** (Lucid) | $6.66, **−80% from 52wk high**, margin −240%, ROE −98%, dilution machine | **SELL** — serial capital-raiser, deeply unprofitable. Harvest loss. |
| **RIVN** (Rivian) | $20.14, margin −64%, ROE −66%, unprofitable | **SELL** — same story as LCID; no quality. Cleanup. |
| **MARA** (Marathon crypto miner) | $12.95, margin −235%, ROE −67%, rev −18%, debt $2.5B | **SELL** — leveraged bitcoin-beta with negative margins; pure spec. Cleanup. |
| **JMIA** (Jumia, Africa e-comm) | $7.13, P/B 67, ROE −155%, margin −31%, unprofitable | **SELL** — perennial-loss frontier e-comm; no thesis fit. Cleanup. |
| **GLBS** (Globus Maritime, dry-bulk shipping) | $3.17, **P/B 0.39**, tiny profit (margin +1.7%), mktcap $68M | **SELL** — statistically cheap on book BUT nano-cap, illiquid, cyclical shipping micro. Not worth the slot; not "secretly worth keeping." |
| **CSGP** (CoStar Group) | $28.70, **crashed from 52wk high $97.43 (−70%)**, PE 410, fwd PE 16, rev +22% | **SELL at micro size** — the one arguably-quality business here (real-estate data moat) but it's had a big drop and margins are compressed by Homes.com spend. If he wanted a real position it could merit a look; at "tiny/legacy" size it's just noise. **Cleanup unless he wants to size it up deliberately** (would need its own diligence). |

**Tier-3 net:** none is a compelling keep. Closest to "reconsider" is **CSGP** (genuine data-moat business, badly beaten down) — but only as a *fresh, properly-sized* decision, not as a legacy scrap. F has a yield but is low-quality. Consolidate the rest away.

---

# Redundancy / concentration map (requested)

1. **CRCL held twice:** direct CRCL position **+ inside ARKK (4.5%)**. Selling ARKK also reduces the accidental CRCL doubling.
2. **AA held twice:** standalone AA **+ inside XME (4.6%)**. Plus metals is another agent's domain → triple-counted aluminum/metals risk. Consolidate to XME (or defer to metals agent).
3. **CAG ≈ KHC:** identical thesis (large-cap packaged food, GLP-1/private-label secular pressure, high-yield value-trap profile). **Own ONE, not both** → keep KHC (breakup catalyst + better dividend coverage), trim CAG.
4. **CF vs PDBA:** both "agriculture," but **complementary** (nitrogen-producer equity vs broad ag-commodity futures) — NOT redundant. Keep both if he wants ag exposure.
5. **ARKK vs AMZN / AI names:** ARKK's TSLA/AMD/PLTR overlap general AI/tech exposure elsewhere in the book — another reason ARKK is a low-value redundant sleeve.
6. **AMZN:** check total AI/cloud concentration across the *whole* portfolio (megacap agent's book + AMZN) — out of my scope but flag for portfolio-level review.

---

# Suggested consolidation (turns ~16 scattered names → a tight core)

**KEEP (on-thesis quality-at-a-price):** AMZN (core), GEV (trim to ~2/3), CF, PDBA. Optionally XME as the single metals vehicle.
**TRIM:** GEV (~1/3), CAG (or sell).
**HOLD w/ catalyst:** KHC.
**SELL / cleanup:** CRCL (or cap as labeled lotto), RBLX, AA, ARKK, SBUX, and ALL of Tier 3 (AEVA, AUR, CHPT, NIO, F, LCID, RIVN, MARA, JMIA, GLBS, CSGP) — tax-loss harvest the underwater ones.

Net effect: fewer, higher-conviction, thesis-aligned names — directly addresses his "too many scattered names / poor stock-picker" worry.

---

# Verification log

| Ticker | Field source | Pull time (local) | Confidence |
|---|---|---|---|
| GEV, AMZN, CAG, KHC, CF, PDBA, CRCL | yfinance `.info` | 2026-07-07 01:47:39 | VERIFIED (live) |
| RBLX, AA, XME, ARKK, SBUX, AEVA, AUR, CHPT, NIO, F, LCID, RIVN, MARA, JMIA, GLBS, CSGP | yfinance `.info` | 2026-07-07 01:47:42 | VERIFIED (live) |
| PDBA/XME/ARKK last close + holdings | yfinance `.history` / `.get_funds_data()` | 2026-07-07 01:47:51 | VERIFIED (live) |

**UNVERIFIED / caveats:**
- PDBA underlying commodity basket (yfinance shows only the T-bill collateral, per its futures structure) — confirm weights on Invesco fact sheet.
- GEV margin fields (op 5.5% vs profit 23.8% vs ROE 75.7%) look internally inconsistent — directional read (expensive/high-quality/cyclical) holds; exact margins UNVERIFIED.
- Negative-EPS names show `trailingPE = null` (expected). fwd PE on unprofitable names (RBLX, AUR, LCID, etc.) is negative/meaningless — used only qualitatively.
- Tier-3 tax-loss harvesting assumes **Canadian** superficial-loss rules (Hooman is a Canadian citizen) — verify against his actual account jurisdiction/broker before acting.
- **Not financial advice.** Research to inform Hooman's own decisions.
