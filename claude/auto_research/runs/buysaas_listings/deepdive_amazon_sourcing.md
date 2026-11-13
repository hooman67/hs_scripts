# Deep Dive — European Amazon-Seller Sourcing SaaS (Empire Flippers #91852)

**Owner**: Hooman Shariati (hshariati@adobe.com). **Written**: 2026-07-02 by Claude (Opus 4.8).
**Context**: Re-examined because Hooman's capital ceiling was raised from $150K to **$300K**.
This listing was previously flagged PARTIAL / over-band (row 5 of `runs/buy_microsaas_LIVE_LISTINGS.md`).
At $300K the **price** now fits; this doc asks whether the *asset* does.

---

## 1. WHAT IT IS

A **European-focused SaaS that gives professional Amazon "online arbitrage" (OA) sellers a sourcing
engine**: it aggregates data from **800+ EU retail suppliers** and indexes **80M+ products**, then
matches those products against Amazon listings so a seller can find items they can buy cheap at a
European retailer and resell profitably on Amazon EU. It sits in the seller's *daily workflow*
(they log in each morning to pull the day's profitable leads).

- **Business model**: subscription SaaS. **85% monthly plans, 15% annual**, + **~6% affiliate revenue**.
- **Launched**: first revenue **Sept 11, 2020 → ~5 yr 9 mo old** (matches the "~6 yr" flag).
- **Platform**: **WordPress-based** front end, AWS infrastructure behind it, Stripe billing.
- **Assets in the sale**: source code, the proprietary supplier/product datasets, customer +
  6,000-person email list, Google/Meta ad accounts, affiliate database, social profiles.
- **Reputation**: Trustpilot 4.5, 202 referring domains, "strong organic brand recognition within
  the European Amazon-seller community."
- **Reason for sale**: "The seller would like to explore other opportunities" (two co-founders).

Source: Empire Flippers listing #91852, https://empireflippers.com/listing/91852/ (fetched 2026-07-02).

---

## 2. THE NUMBERS (public via EF vs gated)

| Metric | Value | Public / gated |
|---|---|---|
| Asking price | **$192,896** | Public |
| Monthly revenue | **$24,942** | Public |
| Monthly net profit | **$7,716** | Public |
| Profit margin | **~31%** | Public |
| Multiple | **25x monthly (~2.06x annual)** | Public |
| Age | ~5 yr 9 mo (first rev Sep 2020) | Public |
| Active subscribers | **80** | Public |
| Plan mix | 85% monthly / 15% annual / 6% affiliate | Public |
| Owner hours | **40 hr/wk across TWO co-founders (≈20 each)** | Public |
| Email list | 6,000+ | Public |
| Churn (exact rate, cohort curve) | "reported churn > adjusted churn; reactivations tied to sourcing cycles/seasonality" — **no hard number** | **GATED** |
| Customer concentration (top-account %) | **GATED** | Gated |
| Monthly revenue trend (growing/flat/declining) | **GATED** — EF card gives none | Gated |
| True COGS breakdown (what eats the 69%) | **GATED** | Gated |
| Domain / live URL | **GATED** (needs verified buyer + deposit) | Gated |

**Read on the numbers**: This is by far the **highest-revenue, highest-net listing in the whole
shortlist** ($7,716/mo net vs. the ~$1.2–1.6K/mo of Candidates A/B/C). The **2.06x annual multiple
is cheap** on its face — but EF quotes *monthly* multiples precisely because cheap monthly multiples
usually price in **decline or fragility**, and the playbook's own deal-killer #2 is "decline dressed
as stable." A 2x-annual asking on a 6-year SaaS is a **yellow flag that revenue is flat-to-declining**,
not a bargain. **The single most important gated number is the 24-month MRR trend.**

---

## 3. THE "DATA MOAT" — WHAT IT ACTUALLY IS AND HOW DEFENSIBLE

**What the moat is**: a maintained index of **800+ EU supplier catalogs × 80M+ products**, continuously
matched to Amazon EU listings (price, fees, Buy Box, rank/demand via Keepa-style data). The value is
not the raw data — it's the **continuously-refreshed matching pipeline + EU-supplier coverage +
6-year brand trust** in a community that buys on reputation (Trustpilot 4.5, 202 referring domains).

**How defensible — honest assessment (MEDIUM-LOW):**

- **It is a real, non-trivial moat vs. a from-scratch clone.** Assembling 800 EU supplier feeds,
  keeping them fresh, and matching 80M SKUs to Amazon is months of engineering + ongoing scraper
  maintenance. This is genuinely harder than a "thin AI wrapper," and the brand/community trust is a
  second layer a cloner can't buy. This is the strongest moat of anything on the shortlist.
- **BUT the data is not proprietary in origin — it is scraped/aggregated from public retailer sites
  and third-party pricing data (Keepa-style).** Anyone with scraping infra can rebuild it; the barrier
  is *effort and maintenance*, not *access*. Well-funded incumbents already have it (see §5).
- **The moat is a treadmill, not a wall.** Supplier sites change layouts, add anti-bot defenses, and
  the matching must be re-run constantly. If maintenance lapses, the "80M products" rots into stale
  leads within weeks and the product silently dies. This is an **ops-heavy moat that decays without
  continuous labor** — which is exactly why the owner load is 40 hr/wk (see §4).
- **Verdict**: it's a *maintenance moat* (defensible only as long as you keep paying the upkeep tax),
  layered on a *brand/community moat* (the more durable half). Not a data asset that appreciates while
  you sleep.

Sources: listing #91852; competitor/data-source research below.

---

## 4. THE 40 hr/wk OWNER LOAD — AND CAN HOOMAN'S SKILLS CUT IT?

**What the 40 hours are** (inferred from the model; to be confirmed in diligence): the load splits
across (a) **keeping the sourcing pipeline alive** — fixing broken supplier scrapers, re-matching,
data QA (the treadmill); (b) **customer support** for 80 active B2B subscribers who log in daily and
complain when leads are stale/wrong; (c) **paid-acquisition management** (Google + Meta ads run the
top of funnel); (d) sales/affiliate/content. It is **two co-founders × ~20 hr each**, with contractors
already doing dev/sales/support — so the 40h is the *founders'* residual, not the total labor.

**Can Hooman's AI/data-engineering skills cut it? — This is the crux, and the answer is nuanced:**

- **YES, materially, on the data-pipeline half (a).** This is the single best founder-market-fit
  match on the entire shortlist. Hooman is a data/infra/ML engineer; the 40h is dominated by
  scraper maintenance, matching, and data QA — **exactly** his wheelhouse. Modernizing brittle
  scrapers, adding self-healing/monitoring, LLM-assisted layout-change detection, and automating the
  match/QA loop could plausibly cut the *pipeline* labor meaningfully. This is a rare case where the
  buyer's edge is *value-creation* (cutting the upkeep tax), not just diligence alpha.
- **PARTLY on acquisition (c)** — but running Google/Meta ads profitably is a *marketing* skill, not
  an engineering one, and per the playbook this is NOT Hooman's edge. If the business is ad-fed, that
  labor doesn't automate away with code.
- **NO on support and community/brand (b, d).** 80 daily-active B2B users who churn on
  relationship/trust require human hand-holding; a VA can take tier-1 *after SOPs exist*, but the
  domain-trust/community role is founder-bound. Automating this is where every small-SaaS buyer
  overestimates themselves.

**Delegation-trap math (from PLAYBOOK: delegation only pencils above ~$4K/mo net):**
At **$7,716/mo net this is the FIRST listing that clears the ~$4K delegation threshold.** After a
plausible ~$1.5–2.5K/mo VA+contractor-dev spend, ~$5–6K/mo net would remain — so **delegation is
genuinely affordable here**, unlike Candidates A/B/C where a VA erased all profit. Combined with
Hooman's ability to *engineer* the pipeline labor down, this is the one shortlist asset where a
credible path to **8–12 hr/wk part-time operation** exists. **That is the standout positive.**

**Caveat**: the 40h is *current* load; the risk is that the pipeline treadmill is load-bearing and
that cutting corners (or a support VA who doesn't know the domain) accelerates churn. The hours can
likely be cut — but only *after* a real 60–90 day transition and SOP handover, and only if the two
departing co-founders aren't the irreplaceable "product" (deal-killer #8).

---

## 5. COMPETITION — NAMED, AND WHAT IT MEANS FOR THE MOAT

This is a **crowded, mature category**, especially US-centric but with EU coverage:

| Competitor | What it does | Price (2024–25) | Note |
|---|---|---|---|
| **Tactical Arbitrage** | The "#1 OA sourcing software"; scans retail sites across US/UK/EU, matches to Amazon | **$59–109/mo** (OA+Wholesale ~$109); $69 in Seller 365 bundle | The 800-lb gorilla; already covers Europe |
| **SourceMogul** | Budget OA scanner, unlimited searches, multi-device | "budget-friendly" (~$97/mo tier) | Direct substitute |
| **SellerAmp (SAS)** | Web+mobile+Chrome analysis tool for sourcing decisions | ~$25–35/mo | Huge UK/EU install base; adjacent |
| **BuyBotPro** | Automated OA buying/analysis "virtual assistant" | ~$34+/mo | UK-origin, strong EU presence |
| **OAGenius Gravity, Nepeto, AZInsight, Keepa** | Various OA/repricing/data | varies | Keepa is the underlying pricing-data layer many rely on |

Sources: DuckDuckGo results for "Tactical Arbitrage / SourceMogul / SellerAmp pricing 2025" and
"best online arbitrage sourcing tools 2025" (fetched 2026-07-02).

**What this means**: The #91852 asset survives by being **EU-supplier-focused and community-trusted**
in a space where the leader (Tactical Arbitrage) is US-centric but *already covers Europe*. Its edge
is regional depth + brand, not a defensible technical wall — and its price point (implied ~$100+/mo
ARPU: $24,942 rev ÷ ~85%-of-80 monthly subs ≈ high-double/low-triple digits per user) sits right in
the range where TA/SourceMogul compete. **A funded incumbent could expand EU supplier coverage and
compress this business.** The moat is "good enough to have held 80 subs for 6 years," not "durable
against a determined competitor."

---

## 6. THE AMAZON-DEPENDENCY RISK (the platform deal-killer, #6)

This is the **hardest structural risk** and it is doubled:

1. **Demand-side dependency on the OA business model itself.** The entire customer base exists only
   because Amazon online arbitrage is a viable seller strategy. Research indicates **Amazon has been
   escalating brand gating, supplier-verification, and reseller crackdowns**, and OA "now requires
   more strategic approaches as competition grows" — i.e. the *addressable seller population for OA
   sourcing tools is under structural pressure*, and margins for OA sellers are thinning (which
   pressures their willingness to pay for tools). If Amazon further tightens reseller rules, the TAM
   for this SaaS shrinks regardless of product quality.
   (Source: DuckDuckGo "Amazon online arbitrage still profitable 2025 brand gating" research, 2026-07-02.)

2. **Supply-side dependency on scraping + Amazon data.** The product must scrape 800+ retailer sites
   and pull Amazon/Keepa pricing data. Sources note scraping "the wrong way can get you sued or
   banned," and the compliant path is Amazon's SP-API — which Amazon controls and periodically
   restricts. **A ToS change, API rate-limit/access change, or aggressive anti-bot rollout by
   suppliers could break the pipeline.** This is deal-killer #6 (platform-dependent; host can kill it)
   in its purest form: the business runs on data it does not own from platforms that can revoke access.

**Net**: Amazon dependency here is not a footnote — it is the **defining risk**. It caps the exit
multiple (buyers discount platform-dependent assets) and is the reason a 6-year, $7.7K/mo-net SaaS
is only asking ~2x annual.

---

## 7. WHY ONLY 31% MARGIN? (SaaS is usually 70–90%)

31% net is **low for SaaS and is itself a signal**. The 69% of cost is gated, but the model implies
it goes to: (a) **paid acquisition** (Google + Meta ads — if the top of funnel is bought, not organic,
that's a recurring 20–40% drag and a growth ceiling); (b) **contractor dev + support + sales** (already
staffed out); (c) **data/infra costs** (scraping proxies, AWS, Keepa/data feeds — non-trivial at 80M
products); (d) affiliate payouts. **The low margin most likely means the business buys its growth via
ads and pays a heavy data-ops tax** — both of which (i) confirm the treadmill, and (ii) mean the
"31%" is fragile: if ads are cut, revenue likely falls with them. **Verify the acquisition mix first**:
organic/brand-driven vs. paid is the difference between a durable community asset and an ad-arbitrage
business wearing a SaaS costume.

---

## 8. FIT AGAINST THE $300K CEILING & BUY BOX

- **Price fit**: **FITS** outright at $192,896 all-cash, leaving ~$100K of the $300K ceiling for
  legal/escrow/reserve and, notably, for an earnout structure. Comfortably inside the new band.
- **Net fit**: $7,716/mo net is **well above** the Buy Box's $2–4K/mo target and the ~$4K delegation
  threshold — the **only shortlist listing where the economics support delegation/part-time.**
- **Multiple**: 2.06x annual is *below* the fair 4–4.5x — cheap, but cheap-for-a-reason (platform
  risk + suspected flat/declining trend). If trend is flat and Amazon risk is priced, 2x is arguably
  fair-to-generous; if declining, even 2x is too much.
- **Buy-Box VIOLATIONS to weigh**: (a) it is a **single-platform-dependent add-on** to the Amazon
  ecosystem — a soft version of deal-killer #6; (b) **80 subscribers** is thin → **concentration risk
  unknown/gated**; (c) **owner-as-product** risk with two departing co-founders; (d) WordPress front
  end + scraper backend = the code/IP-chain and "one undocumented cron holding it together" checks
  matter a lot.

---

## 9. HONEST VERDICT

**CONDITIONAL — the most interesting listing on the shelf for THIS buyer, gated on three kills.**

The bull case is real and specific: it is the **only** shortlist asset that (1) fits the new $300K
price ceiling, (2) throws off enough net ($7.7K/mo) to *actually delegate*, and (3) has a labor
profile (data-pipeline maintenance) that **Hooman's data/infra/ML skills are uniquely suited to
automate** — a genuine value-creation edge, not just diligence alpha. If the 24-month trend is flat
and the pipeline is the load-bearing 40h, Hooman could plausibly engineer it toward a real part-time
$5–6K/mo cash-flow asset. That is the closest anything here comes to his $5–30K/mo goal.

The bear case is equally real: it is **platform-dependent on Amazon** (demand *and* data), in a
**crowded, mature category** with a well-funded EU-capable leader, at a **suspiciously cheap 2x
annual multiple** with a **low 31% margin** that smells like bought growth, and the moat is a
**decaying maintenance treadmill**, not a durable asset. Any one of {declining trend, ad-dependent
acquisition, >20% concentration, Amazon ToS exposure} could turn this into a melting ice cube.

**It clears the price gate the old listing failed — but it trades the affordability problem for a
durability problem.** Worth a real seller call and Gate-2 diligence *specifically because* the
delegation math and founder-fit finally work; walk fast if the gated numbers confirm the bear case.

---

## 10. VERIFY FIRST (the deal-killers, in kill-priority order)

1. **24-month MRR trend from raw Stripe** — the #1 kill. A 2x-annual multiple on a 6-yr SaaS screams
   flat/declining. If MRR is trending down (deal-killer #2), **walk** regardless of everything else.
2. **Acquisition mix** — what % of new subs come from **paid ads vs. organic/brand**? If it's ad-fed,
   the 31% margin is fragile and the "moat" is spend, not brand. This explains the low margin.
3. **Amazon/platform exposure** — how does it get Amazon data (SP-API vs. scraping)? What breaks on an
   Amazon ToS/API change? How exposed is the OA seller TAM to Amazon's brand-gating crackdown?
   (deal-killer #6).
4. **Customer concentration** — 80 subs is thin; is any single customer or affiliate partner >20% of
   revenue? Pull raw Stripe (deal-killer #4).
5. **Churn cohort curve** — the "reactivations tied to sourcing cycles" language is a hedge. Build the
   cohort curve from raw Stripe; confirm it flattens and isn't seasonal-churn masked by reactivations
   (deal-killer #3).
6. **Pipeline fragility / owner-as-product** — how many supplier scrapers break per week; how much of
   the 40h is the two founders personally firefighting the pipeline vs. delegable ops; will they do a
   real 60–90 day transition + SOP handover (deal-killer #8)? Confirm the data-ops labor is the kind
   Hooman can actually engineer down.
7. **Data-cost + IP chain** — true monthly spend on proxies/scraping infra/Keepa/data feeds/AWS
   (the hidden 69%); clean IP assignment from all contractors on the WordPress + scraper code
   (deal-killer #5).
8. **Three-way reconcile** bank ↔ Stripe ↔ P&L; separate the 6% affiliate + any one-time/setup from
   recurring MRR.

---

## Sources
- Empire Flippers listing #91852 — https://empireflippers.com/listing/91852/ (fetched 2026-07-02):
  all headline financials, subs, plan mix, owner hours, age, assets, reason for sale, moat language.
- DuckDuckGo research (fetched 2026-07-02): competitor set & pricing (Tactical Arbitrage, SourceMogul,
  SellerAmp, BuyBotPro, OAGenius/Nepeto/Keepa); data-source/scraping-vs-SP-API legal risk; Amazon OA
  brand-gating/reseller-crackdown state-of-the-market.
- `runs/buy_microsaas_PLAYBOOK.md` — Buy Box, 8 deal-killers, ~$4K/mo delegation threshold.
- `runs/buy_microsaas_LIVE_LISTINGS.md` — row 5 original PARTIAL flag; shortlist comparison.
