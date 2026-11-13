# Portfolio Instrument Review

**Review date:** 2026-08-25  
**Scope:** Instrument selection within Hooman's supplied strategic sleeve weights  
**Important:** This is instrument due diligence, not authorization to execute the dashboard's `ACTION $` column.

## Executive conclusion

The high-level allocation can be implemented much more cleanly. Several current instruments do not actually match their sleeve labels, and some duplicate exposures already inside the core ETFs.

The strategic target and the timing overlay must remain separate. The allocation table says both:

- trim approximately $187,833 of cash; and
- keep the cash as recession dry powder and do not deploy it to equities yet.

Those are incompatible instructions if acted on simultaneously. The product recommendations below describe how each sleeve could eventually be implemented; they do not override the instruction to preserve cash pending a separately defined deployment rule.

## Recommended implementation

### Cash — 20.5%

Suggested implementation:

- **10.25% USD:** direct U.S. Treasury bills or **SGOV**.
- **10.25% CAD:** direct Government of Canada Treasury bills or a maturity-matched, CDIC-eligible GIC ladder.
- **CBIL** is a reasonable liquid Canadian alternative, but it is an ETF rather than an insured deposit and needs cross-border tax review if held by a U.S. tax person.

SGOV holds 0–3 month U.S. Treasury securities and currently charges 0.09%. CBIL holds short Government of Canada Treasury bills and reported a 0.11% MER for 2025. Direct bills or GICs are preferable when the expected spending dates are known because maturities can be matched to the liability.

Sources:

- [iShares SGOV product page](https://www.ishares.com/us/products/314116/ishares-0-3-month-treasury-bond-etf)
- [Global X CBIL product page](https://www.globalx.ca/product/cbil)
- [CDIC guidance on GIC coverage](https://www.cdic.ca/depositors/whats-covered/guaranteed-investment-certificates-gics/)

**Verdict:** Keep the concept, but improve currency and maturity matching. Do not treat equity-like recession hedges as substitutes for principal-stable house capital.

### Global equity core — 20.0%

Suggested implementation:

- **10.5% VTI**
- **7.0% VXUS**
- **2.5% AVUV**

This applies the intended approximate 60/40 U.S./international split to the non-factor portion of the sleeve and treats AVUV as a deliberate carveout. VTI and VXUS are excellent low-cost broad-market funds, with current expense ratios of 0.03% and 0.05%. AVUV's 0.25% fee buys an active small-cap value/profitability tilt; it is not neutral market exposure.

Sources:

- [Vanguard VTI product page](https://advisors.vanguard.com/investments/products/vti/vanguard-total-stock-market-etf)
- [Vanguard VXUS product page](https://advisors.vanguard.com/investments/products/vxus/vanguard-total-international-stock-etf)
- [Avantis AVUV product page](https://www.avantisinvestors.com/avantis-investments/avantis-us-small-cap-value-etf/)

**Verdict:** Keep VTI/VXUS. Keep AVUV only as an explicitly accepted factor bet.

### Emerging markets and China — 5.0%

Suggested implementation:

- **2.5% VWO**
- **2.5% FLCH**

VWO is an appropriate broad emerging-markets vehicle. If the second half is meant to be a China country tilt, FLCH is a cleaner match than KWEB because FLCH provides broad China exposure at a reported net expense ratio of 0.19%. KWEB is a narrow China-internet sector fund charging 0.69%.

KWEB already held Alibaba at 9.25% and Baidu at 3.23% as of 2026-08-21. A separate BABA position is therefore redundant, and selling direct BIDU does not eliminate BIDU exposure while KWEB remains.

IEMG, at 0.09%, is also a valid alternative to VWO if the MSCI classification—including South Korea—is deliberately preferred.

Sources:

- [Vanguard VWO product page](https://advisors.vanguard.com/investments/products/vwo/vanguard-ftse-emerging-markets-etf)
- [Franklin Templeton FLCH product page](https://www.franklintempleton.com/investments/options/exchange-traded-funds/products/26362/SINGLCLASS/franklin-ftse-china-etf/FLCH)
- [KraneShares KWEB product page](https://kraneshares.com/etf/kweb/)

**Verdict:** Replace KWEB plus standalone BABA unless concentrated China-internet exposure is the explicit objective.

### Quality compounders — 5.5%

Suggested implementation:

- **5.5% QUAL**, or
- **3.5% QUAL + 1.0% GOOGL + 1.0% AMZN** if limited single-name conviction is intentional.

QUAL screens for high return on equity, stable earnings growth, and low financial leverage while seeking sector neutrality. Its expense ratio is 0.15%. GOOGL and AMZN are already meaningful holdings inside VTI, so allocating the entire sleeve 3.0%/2.5% to them is a concentrated U.S. mega-cap bet, not a diversified quality sleeve.

Source:

- [iShares QUAL product page](https://www.ishares.com/us/products/256101/QUAL)

**Verdict:** Replace most of the two-stock exposure with QUAL. Keep small direct positions only if their incremental concentration is intentional.

### Energy — 9.0%

Suggested implementation:

- **9.0% IXC**

IXC is the cleanest one-fund match for the stated global XOM/CNQ/oil-and-gas intent. It owns roughly 50 global energy companies and currently charges 0.37%. Current official data showed Exxon at roughly 18%, Canadian Natural Resources at roughly 2.7%, and Canada at roughly 13.5% of the fund. It also provides exposure across integrated producers, exploration and production, refining, and related businesses.

IXC remains energy equity exposure, not direct natural-gas-price exposure. Daily-reset leveraged funds and futures-based gas products are unsuitable as long-term core holdings.

Source:

- [iShares IXC product page](https://www.ishares.com/us/products/239741/ishares-global-energy-etf)

**Verdict:** IXC is a cleaner consolidated implementation than several individual energy names. The 9% weight and macro exit rule remain separate allocation decisions.

### Gold core — 14.0%

Suggested implementation:

- allocated physical bullion and/or
- **GLDM** for liquid brokerage exposure.

GLDM is physically backed and charges 0.10%. AEM is a mining equity, not bullion: it carries operating costs, management, jurisdiction, reserve-replacement, and equity-market risk. It should be reclassified into a separately capped gold-miner sleeve if retained.

MNT represents direct beneficial ownership in Canadian Mint gold reserves, but it can trade at a premium or discount to net asset value, charges roughly 0.35%, and requires cross-border tax review for a U.S. tax person.

Sources:

- [State Street GLDM product page](https://www.ssga.com/us/en/individual/etfs/spdr-gold-minishares-gldm)
- [Royal Canadian Mint MNT program](https://www.reserves.mint.ca/tsx_gold/)

**Verdict:** Use physical bullion/GLDM for the core. Reclassify AEM as mining equity rather than counting it as direct gold.

### Utilities — 4.0%

Suggested implementation:

- **4.0% VPU**

VPU is preferable to XLU as a long-term holding because it provides broader multi-cap exposure—68 stocks in the reviewed official data—at a 0.09% expense ratio. XLU remains a good alternative when maximum trading and options liquidity matter.

Source:

- [Vanguard VPU product page](https://advisors.vanguard.com/investments/products/vpu/vanguard-utilities-etf)

**Verdict:** Prefer VPU for long-term breadth and cost. Neither VPU nor XLU is principal-stable cash or a guaranteed recession hedge.

### Financials / insurance — 2.5%

The existing sleeve is mislabeled. CI is a healthcare-services/managed-care company, not a financial company. If the intended exposure is the broad financial sector, use:

- **2.5% VFH**

If the actual intent is defensive insurance exposure without a bank overweight, rename the sleeve **Insurance / defensive compounders** and use approximately:

- **1.5% KIE**
- **1.0% BRK.B**

KIE owns a modified-equal-weight basket of approximately 53 insurance companies and charges 0.35%. BRK.B is a diversified conglomerate with major insurance operations; it is not a pure insurance ETF. CI belongs in healthcare and remains a security-level **WATCH**, not an automatic buy.

Sources:

- [State Street KIE product page](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-sp-insurance-etf-kie)
- [Vanguard VFH product page](https://advisors.vanguard.com/investments/products/vfh/vanguard-financials-etf)

**Verdict:** First decide whether the sleeve means broad financials or insurance. The stated “defensive, not banks” intent supports KIE plus BRK.B more closely than CI.

### Uranium / AI power — 3.5%

Suggested implementation:

- **3.5% NLR**

NLR is the closest one-fund match for a mixed nuclear ecosystem sleeve. It explicitly includes uranium miners, nuclear-power producers, and nuclear-equipment/services companies. Current major holdings included CCJ, CEG, and BWXT, and the expense ratio was 0.52%.

URNM is the higher-beta alternative for a predominantly uranium-miner/fuel thesis. At 2026-07-31 it was approximately 81% uranium equities and 19% physical uranium, with a 0.75% expense ratio. It is not a substitute for power-generation exposure.

Sources:

- [VanEck NLR product page](https://www.vaneck.com/us/en/investments/uranium-nuclear-energy-etf-nlr/)
- [Sprott URNM product page](https://sprottetfs.com/urnm-sprott-uranium-miners-etf)

**Verdict:** NLR most closely matches the current mixed CEG/BWXT/CCJ intent and reduces single-name risk.

### Copper — 3.0%

Suggested implementation:

- **3.0% COPX**

COPX remains a suitable instrument if the objective is global copper-miner equity exposure. It owns approximately 40 miners and charges 0.65%. It is not spot copper: returns also depend on operating execution, input costs, jurisdictions, balance sheets, management, and the broader equity market.

Source:

- [Global X COPX product page](https://www.globalxetfs.com/funds/copx)

**Verdict:** Keep the instrument, but label the exposure correctly as copper-miner equities.

### Agriculture — 3.0%

Suggested implementation:

- **3.0% PDBA**

PDBA is the cleaner implementation if the intended exposure is agricultural commodity prices and inflation. It is an actively managed U.S. ETF using agriculture futures and collateral, issues no K-1, and had a current management/net fee of approximately 0.59% under a waiver versus roughly 0.74%–0.75% gross.

CF is a single fertilizer-company equity. It should be retained only as a separately underwritten and capped stock thesis, not treated as interchangeable with an agriculture-commodity fund.

Source:

- [Invesco commodity ETF information](https://www.invesco.com/us/en/solutions/invesco-etfs/commodity-investing.html)

**Verdict:** Use PDBA alone for the stated commodity/inflation exposure; remove CF from this sleeve unless a separate company thesis is intended.

### Healthcare — 5.0%

Suggested implementation:

- **4.0% XLV**
- **1.0% IHI**

XLV provides low-cost large-cap U.S. healthcare exposure across approximately 60 S&P 500 companies at 0.08%. IHI provides a medical-device tilt and includes GEHC, but it is itself concentrated: it owned approximately 46 names, and its top three were about 43% of the fund in the reviewed official holdings. IHI charges 0.37%.

VHT, at 0.09% and more than 400 holdings, is a reasonable alternative to XLV if maximum breadth matters more than a large-cap defensive emphasis.

Standalone GEHC and PFE are not required to obtain the desired sector exposure. XLV already held PFE at 2.54% and LLY at 15.83% as of 2026-08-18.

Sources:

- [State Street XLV product page](https://www.ssga.com/us/en/individual/etfs/state-street-health-care-select-sector-spdr-etf-xlv)
- [iShares IHI product page](https://www.ishares.com/us/products/239516/ishares-us-medical-devices-etf)

**Verdict:** Use XLV as the core and cap the IHI device tilt. Replace the standalone GEHC/PFE positions unless there is an independently supported stock thesis.

### Defense — 2.0%

Suggested implementation:

- **2.0% XAR**

XAR is preferable to ITA or PPA for diversified pure aerospace-and-defense exposure because its modified equal-weight methodology reduces mega-cap concentration. Its current gross expense ratio is 0.35%.

Source:

- [State Street XAR product page](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-sp-aerospace-defense-etf-xar)

**Verdict:** Prefer XAR. ITA is more top-heavy; PPA is broader but more expensive.

### Crypto — 2.0%

Suggested implementation:

- direct bitcoin, if self-custody, security, succession, and recovery are genuinely solved; or
- **IBIT** for a simpler brokerage implementation.

IBIT holds spot bitcoin and charges 0.25%. It is a trust and does not provide the Investment Company Act of 1940 protections of an ordinary registered ETF. Direct bitcoin has the lowest ongoing product cost but creates custody and operational risks that are easy to underestimate.

Source:

- [iShares IBIT product page](https://www.ishares.com/us/products/333011/ishares-bitcoin-trustIBIT)

**Verdict:** Use IBIT for operational simplicity or direct BTC only with a robust custody/succession plan. Avoid Canadian-listed bitcoin funds until U.S. tax residence and PFIC treatment are confirmed.

### Silver / platinum — 1.0%

Suggested implementation:

- **0.75% SIVR**
- **0.25% PPLT**

SIVR provides allocated physical silver exposure with a currently waived sponsor fee of 0.30%. PPLT provides physical platinum exposure and charges 0.60%. WPM is a royalty/streaming company and does not implement direct metal-price exposure; it carries company, counterparty, operating, and equity-market risks.

Sources:

- [SIVR SEC filing](https://www.sec.gov/Archives/edgar/data/1450922/000199937126010350/sivr-10q_033126.htm)
- [PPLT SEC filing](https://www.sec.gov/Archives/edgar/data/19617/000121390026031809/ea0282647-01_424b2.htm)

**Verdict:** Replace WPM with physical-metal vehicles if the sleeve truly means direct silver/platinum. U.S. taxable holders should also review precious-metals/collectibles tax treatment.

## Important portfolio-level corrections

### Dedicated EM is not the total EM exposure

VXUS was 26.36% emerging markets as of 2026-06-30. A 7% VXUS allocation therefore contributes approximately 1.85 percentage points of emerging-market exposure before the dedicated 5% EM/China sleeve. Total look-through EM exposure would be approximately 6.9%, not 5%.

### The portfolio remains highly concentrated in a common macro factor

The following sleeves total 33.5%:

- Energy: 9.0%
- Gold: 14.0%
- Uranium / AI power: 3.5%
- Copper: 3.0%
- Agriculture: 3.0%
- Silver / platinum: 1.0%

Using ETFs reduces individual-company risk but does not remove the shared commodity, inflation, geopolitical, and economic-cycle factor exposure. Utilities, miners, energy, defense, and nuclear equities can all suffer major drawdowns and should not be counted as safe house capital.

### The cash target conflicts with the stated safety promise

Using the supplied approximately $618,600 portfolio value, a 20.5% cash target is roughly $126,805. The existing policy language separately promises:

- $100,000 permanent cash floor; plus
- $45,000 crash/recession deployment reserve.

That totals $145,000, approximately $18,195 more than the 20.5% sleeve target. The plan cannot fully fund both promises without reducing another sleeve or increasing the cash percentage.

### Clarify the LLY date

The table says “LLY SOLD Aug-26.” On the 2026-08-25 review date, that wording appeared to refer either to August 2026 or to a future 2026-08-26 trade. It should be rewritten as a full date so the trade record is unambiguous.

## Cross-border tax and account warning

Tax status must be determined from residence and applicable U.S. tests, not from Canadian citizenship alone. U.S. tax residence can arise under the green-card or substantial-presence tests. A U.S. person holding Canadian-listed pooled funds may face PFIC/Form 8621 consequences, so U.S.-domiciled ETFs are the provisional default until residence, account registration, and cross-border tax treatment are reconciled.

Sources:

- [IRS introduction to U.S. tax residency](https://www.irs.gov/individuals/international-taxpayers/introduction-to-residency-under-us-tax-law)
- [IRS Form 8621 instructions](https://www.irs.gov/instructions/i8621)

Separating VTI and VXUS may improve rebalancing and asset location, but it does not recover all internal foreign withholding. Vanguard's Canadian withholding guide shows that a directly held U.S.-listed international ETF can still lose source-country withholding inside the fund. Only a subsequent U.S. withholding layer may be treaty-exempt in an eligible RRSP or potentially creditable in taxable. “VXUS separate means the foreign-tax credit is claimable” is therefore incomplete.

Source:

- [Vanguard Canada foreign-withholding-tax guide](https://www.vanguard.ca/content/dam/intl/americas/canada/en/documents/WithholdingTax_Guide-final.pdf)

## Bottom line

The cleanest provisional structure is:

- liability-matched direct government bills/GICs or SGOV/CBIL for cash;
- VTI + VXUS + a deliberately sized AVUV tilt for global core;
- VWO + broad China rather than VWO + KWEB + BABA;
- QUAL instead of relying entirely on GOOGL and AMZN;
- IXC, GLDM/physical bullion, VPU, KIE/BRK.B, NLR, COPX, PDBA, XLV/IHI, XAR, IBIT, and SIVR/PPLT for the corresponding sleeves.

No trades should be generated from this structure until current broker holdings, cash by currency and account, tax lots, vested versus unvested RSUs, U.S./Canadian tax residence and account registrations, and the house reserve amount/currency have been reconciled. Product selection cannot fix an inconsistent capital-allocation policy.
