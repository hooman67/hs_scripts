# Holdings Snapshot — Ground Truth (live-priced 2026-07-07)

**Source:** Hooman's portfolio export (his shares/buy-prices) + **live yfinance pull 2026-07-07**.
Reproducible via `portfolio/data/holdings.py` → `holdings_live.csv` / `.json`. Every price VERIFIED live.

> **⚠️ DATA-QUALITY FIX (important).** Hooman's export book-value column is **inconsistent on
> currency**: some CAD holdings were converted to USD (e.g. CNQ book = C$ × 0.70), others left in
> raw CAD (e.g. MNT book = the raw CAD number, unconverted). This distorted his reported P&L — MNT
> showed "−26.5%" but is actually **+4.5%** once book and market value are compared in the same
> currency. **We recompute book from first principles: shares × avg_buy_native × FX(0.70347).**
> All G/L figures below use the corrected basis.

## Totals (as-of 2026-07-07, USD)

| | Value |
|---|--:|
| Cash (Bucket A) | $280,407 |
| Non-cash market value | $275,426 |
| **Total portfolio** | **$555,832** |
| Non-cash book (corrected) | $293,871 |
| **Open P&L (corrected)** | **−$18,445 (−6.3%)** |

Separate (not in this portfolio): **$250,000 house reserve** with father; **~$732k Adobe RSUs**
@ $412.71, vesting over 4 yrs (automatic US-tech/SaaS exposure — must be counted in total risk).

## Bucket weights (full portfolio incl. cash)

| Bucket | Value | Actual % | His target |
|---|--:|--:|--:|
| A — cash / vol-reducers | $280,407 | **50.4%** | 50–55% |
| B — inflation hedge | $149,292 | **26.9%** | 30% |
| C — opportunistic growth | $126,133 | **22.7%** | 15% |

**C is ~7.7 pts over target** — real growth-risk exposure is meaningfully higher than the 15% plan.

## By theme (non-cash $275,426)

| Theme | $ | % non-cash | Note |
|---|--:|--:|---|
| oil & gas | 81,996 | 29.8% | 9 names — heavy concentration; ~3–4× market weight |
| gold | 29,946 | 10.9% | MNT + physical + AEM + EMPYF |
| health-bio-AI | 28,306 | 10.3% | PFE $17.5k + LLY $10.8k |
| silver | 26,159 | 9.5% | **WPM single name = 9.5% of non-cash** |
| uranium | 23,287 | 8.5% | CCJ + BWXT + CEG + URC |
| food/ag | 18,886 | 6.9% | CAG, KHC, PDBA, CF |
| tech | 16,641 | 6.0% | AMZN + RBLX + ARKK |
| crypto | 11,560 | 4.2% | BTC (3 lots) + MARA |
| electrification | 9,216 | 3.3% | GEV (single) |
| copper | 9,198 | 3.3% | BHP + COP.U + NTCPF |
| china | 4,807 | 1.7% | KWEB + BABA + BIDU |
| stable-coin | 2,746 | 1.0% | CRCL |
| steel | 2,652 | 1.0% | XME |
| aluminum | 2,494 | 0.9% | AA |
| autonomous | 2,373 | 0.9% | AEVA + AUR |
| ev | 1,978 | 0.7% | 5 names, all tiny |
| platinum/pall | 1,792 | 0.7% | SBSW |
| retail | 1,088 | 0.4% | SBUX + GLBS |
| intl / real-estate | 300 | 0.1% | JMIA + CSGP (vestigial) |

**Precious metals total (gold+silver+plat) = ~21% of non-cash** — the single biggest real-asset bet.
**Commodities/real-assets overall (PM + energy + copper + steel + ag) ≈ 70% of non-cash.**

## Geography (TRUE, by domicile/look-through — corrects his labels)

| Geo | % non-cash | His target |
|---|--:|--:|
| USA | ~43% | 50% |
| Developed ex-US (mostly Canada + Australia) | ~36% | 25% |
| Emerging markets | **~1–2%** | 25% |
| Crypto/other | ~4% | — |

**EM is drastically underweight** (~1–2% vs 25% target). Dev-ex-US is overweight, and it's almost
entirely **Canada** (energy + miners) — so "diversification" is really a concentrated Canada
commodity bet. NOT the global diversification the plan calls for.

## Corrected winners / losers

**Winners:** GEV +87.6% (+$4.3k), XOM +14.5%, CNQ +14.1%, CVE +83.6%, CCJ +14.8%, ARX +15.9%,
LLY +13.2%, MNT +4.5%.
**Losers:** WPM −22.2% (−$7.5k), NIO −87.9%, KWEB −38.8%, SBSW −53.6%, CHPT −67%, PFE −6.2%,
AA −30.3%, CAG −21.1%.

## Micro-positions (<$1,500 each — 15 positions, ~$7,800 total)

GLBS $67, CSGP $86, LCID $133, RIVN $201, JMIA $214, MARA $388, F $415, BIDU $458, BABA $587,
NIO $602, CHPT $626, AUR $679, URC $985, SBUX $1,021, ARKK $1,338.

→ These add tax-filing complexity + rebalancing friction for negligible diversification. Most are
deeply underwater legacy 2021-era speculative buys (EV/autonomous/China ADRs). Candidates for
cleanup (tax-loss harvest where in loss). Full audit in `PHASE1_AUDIT.md`.
