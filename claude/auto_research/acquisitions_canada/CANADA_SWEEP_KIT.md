# CANADA MANUAL MARKETPLACE SWEEP KIT

**Owner**: Hooman Shariati. **Created**: 2026-07-04 by Claude (Opus 4.8).
**Purpose**: A ~1-hour, logged-in, browser-based pass to find **Canadian-domiciled micro-SaaS
acquisitions ≤ $500K CAD** that the automated research MISSED because Flippa / Acquire /
DealStream / BusinessesForSale detail pages were bot-blocked (403), JS-gated, or login-gated.
This is a **navigational kit** — working links + exact search recipes — NOT a listing dump.

**Why manual is required (verified 2026-07-04)**: BusinessesForSale.com, DealStream, and
BizQuest software pages returned **HTTP 403 Forbidden** to automated fetches; Acquire.com and
Empire Flippers gate full listings + seller contact behind a logged-in (often verified) account;
Latona's requires account **+ NDA**. Only a human in a real, logged-in browser sees the inventory.

---

## THE BUY BOX (screen every listing against this — from `runs/buy_microsaas_PLAYBOOK.md`)

Carry this in your head while clicking. **90%+ of listings should die on sight.**

| Dimension | Hard filter |
|---|---|
| **Type** | Vertical B2B **system-of-record / compliance / workflow** tool in an unglamorous trade. Moat = switching cost (customer's data lives in it) + domain trust. |
| **Domicile** | **Canadian-domiciled** (company/seller in Canada — ON/BC ideal). This is the whole point of this sweep. |
| **Remote-operable** | Must run **fully remote from the US today** (Hooman is US-resident on TN). Pure SaaS clears; anything on-site does not. |
| **Revenue** | ≥18–24 mo history; B2B; recurring; **source-verified via read-only Stripe + bank** later (never screenshots). |
| **Net (SDE)** | $1.5–4K/mo trailing realistic within budget. |
| **Price** | **≤ $500K CAD.** True all-cash sweet spot is **$80–160K CAD**; the $160–500K band is financeable with BDC/seller note (Canadian-citizen edge). |
| **Churn** | Cohort curve must actually flatten in raw Stripe export (~4.5%/mo realistic, not the ≤3% sellers claim). |
| **Concentration** | **<20%** of revenue from any single customer AND no single acquisition channel carrying it. |
| **Owner load** | Current owner **<10 hrs/wk** (proves part-time operability). |
| **Mandate-driven** | BONUS: regulatory MANDATE to BUY (compliance recordkeeping) = durable demand. A mandate to *sell/approve* = death — avoid. |
| **AI-safe / durable** | **REJECT**: consumer apps, SEO/content sites, Chrome extensions, thin AI/LLM wrappers, single-platform add-ons (Shopify/WP/Stripe app the host can kill). |

**Founder-fit reframe**: Hooman's edge is **diligence alpha** (spotting traps), NOT value-creation
via rewrite. Don't pay a premium expecting to rerate ugly code.

---

## THE 1-HOUR ROUTINE (do these in order; total ~60 min)

1. **(5 min) Acquire.com** — highest volume in the $2–8K MRR SaaS band. Log in, apply SaaS +
   price filters, sort newest, eyeball for Canada domicile in listing detail.
2. **(10 min) Flippa** — most volume + most junk; it has a real **Country=Canada** filter (use it).
3. **(5 min) Empire Flippers** — vetted, priced higher; free account, filter SaaS.
4. **(10 min) BusinessesForSale.com/canada + BizQuest Canada + BusinessSellCanada + Sunbelt Canada**
   — the Canadian-domicile-native brokers. Software/technology category, ON/BC, price ≤ $500K.
5. **(5 min) DealStream** — software + Canada; membership-gated, worth a scan.
6. **(10 min) Latona's + Motion Invest + FE International + Microns** — curated micro-SaaS shelves.
7. **(5 min) Kijiji Business-for-Sale** — long-tail, cheap, unbrokered Canadian sellers.
8. **(10 min)** Triage: for anything that passes the paper Buy Box, save the URL + run the
   **"How to verify a listing"** checklist below; anything that clears → **Gate-2 script**.

---

## PER-MARKETPLACE RECIPES (verified URLs 2026-07-04)

### 1. Acquire.com  (formerly MicroAcquire) — SHOP HERE MOST
- **Browse URL**: `https://acquire.com/` → sign in → buyer app at `https://app.acquire.com/`
  (public marketing paths like `/search/` and `/startups/` **404**; the live marketplace lives
  behind the app). CTA on the homepage: "Browse 1,000s of vetted online businesses" → `/buyers/`.
- **Account**: **Free buyer account REQUIRED** to browse full listings; **contact/unlock the
  seller requires a verified buyer account** (they gate seller contact behind verification).
- **Filters to set**:
  - Business type / category = **SaaS**
  - Asking price = **$0 – $500K** (set a saved search at **$75K–$160K** for the all-cash core band)
  - TTM revenue / TTM profit — read the P&L; target ~$1.5–4K/mo net
  - There is no reliable country filter — **read each listing's "Location" / seller country field
    and keep only Canada-domiciled** (this is the manual step the bot couldn't do).
- **Keyword searches** (search box): `Canada`, `Ontario`, `Toronto`, `British Columbia`,
  `Vancouver`, `compliance SaaS`, `vertical SaaS`, `field service`, `inspection software`.
- **Check against Buy Box**: median close here is 3.9x profit, 81-day close; $2B+ verified buyer
  funds compete — be fast. Confirm recurring (not one-time), read the "why selling," owner hrs.

### 2. Flippa — HAS A REAL CANADA FILTER (use it)
- **Browse URL (SaaS)**: `https://flippa.com/buy/sitetype/saas`
- **Canada + SaaS combined** (build via the UI, or hand-edit the query string):
  `https://flippa.com/search?filter[property_type]=saas&filter[country]=Canada`
  (the left rail lists Country: United States, United Kingdom, **Canada**, Australia, etc.)
- **Account**: browsing is open; **free account** to watchlist / message sellers.
- **Filters (URL query params, verified)**:
  - `filter[sitetype]=saas` (property type = SaaS)
  - `filter[price][min]=0&filter[price][max]=500000` (asking price ≤ $500K — note Flippa defaults
    USD; convert: **$500K CAD ≈ US$365K**, so set max ≈ **365000** if listings are USD-priced)
  - `filter[profit_per_month][min]=1500` (monthly net profit)
  - `filter[age][min]=18` (business age in months ≥ 18)
  - `filter[revenue_multiple]` / `filter[multiple]` (sanity-check the multiple)
  - `filter[status]=open`, `sort_alias=most_recent` / `ending_soonest`
- **Keyword searches**: `SaaS Canada`, `Ontario software`, `Canadian`, `compliance`, `workflow`,
  `field service`, `inspection`, `scheduling`.
- **Check against Buy Box**: Flippa exposes churn/LTV/AOV columns — turn them on and read them.
  Highest junk ratio of all — apply the REJECT list ruthlessly (AI wrappers, extensions, add-ons).

### 3. Empire Flippers — vetted, priced higher
- **Browse URL**: `https://empireflippers.com/marketplace/`
- **Account**: **free registration** unlocks the full marketplace (watchlists, custom filters,
  notifications). Basic previews show without login; "Unlock Listing" needs the free account.
- **Filters**: Monetization dropdown includes **SaaS**, **Subscription**, **Application**, **Service**
  — select SaaS/Subscription. Filter by niche + price range; listings show monthly net profit &
  monthly revenue. **No native seller-country filter** → read each listing's business location.
- **Keyword / niche**: use the niche filter for B2B/software; then manually confirm Canada domicile.
- **Check against Buy Box**: most vetted inventory (expect fewer, cleaner, pricier deals). Confirm
  recurring revenue retention, not new-logo-masked churn.

### 4. FE International — broker, consultation-gated
- **Browse URL**: `https://feinternational.com/buy-a-website/` (active listings surfaced via
  `/contact-listing`; **no self-serve public browse** — it's a guided M&A process).
- **Access**: **book a buyer consultation / interview** — they interview investors, assess financial
  capacity, then match you to deals. No public NDA-free listing list.
- **How to use in 1 hour**: submit the buyer form once stating the Buy Box (Canadian B2B SaaS,
  ≤ $500K CAD, recurring, compliance/workflow) so their deal flow pushes to you passively.
- **Note**: FE sells SaaS at 5–7x SDE under $2M and cites avg churn ~4.7%/mo — priced richly; treat
  as passive deal-flow, not a same-hour browse.

### 5. BizQuest — Canadian broker aggregator (bot-blocked; log in / real browser)
- **Canada browse**: `https://www.bizquest.com/businesses-for-sale-in-canada/`
- **Province**: `https://www.bizquest.com/businesses-for-sale-in-ontario/` and
  `https://www.bizquest.com/businesses-for-sale-in-british-columbia/`
- **City**: `/businesses-for-sale-in-toronto-on/`, `/businesses-for-sale-in-vancouver-bc/`
- **Category × location pattern**: `/[category]-businesses-for-sale-in-[location]/` →
  try `https://www.bizquest.com/technology-and-internet-businesses-for-sale-in-canada/`
  (categories seen: food-and-beverage, business-services, retail-stores — technology/internet
  is the software bucket; confirm the exact slug from the site's category dropdown).
- **Account**: browsing free; contacting brokers may need a quick form. Detail pages **403 to bots**
  → use a normal logged-in browser.
- **Sort/price**: "Price ($ to $$$)" sort available; set price ≤ $500K in the UI filter.
- **Check**: these are broker-listed operating businesses — confirm it's SaaS (not an IT services
  shop), recurring revenue, and Canada-domiciled.

### 6. BusinessesForSale.com — Canada portal (403 to bots; log in)
- **Canada browse**: `https://www.businessesforsale.com/canada`
- **Software/technology in Canada** (confirm exact slug in-browser; the category picker builds it):
  `https://www.businessesforsale.com/canada/software-companies-for-sale` and
  `https://www.businessesforsale.com/canada/internet-and-technology-businesses-for-sale`
- **Province**: use the location filter for **Ontario** / **British Columbia**; **price** slider ≤
  $500K CAD.
- **Account**: free browsing; contact-seller usually needs a free account. **Detail pages 403 to
  automated fetches** → this is exactly the inventory the bot missed; browse it by hand.
- **Check**: filter to Technology/Internet/Software category first, then confirm recurring SaaS
  (many "internet businesses" here are ecom/content — apply REJECT list).

### 7. BusinessSellCanada.com — Canadian-owned, no-account, free
- **All listings**: `https://www.businesssellcanada.com/sale/buymain.htm`
- **By province** (verified pattern):
  - BC: `https://www.businesssellcanada.com/sale/buy/businesses-for-sale-in-british-columbia.htm`
  - Ontario: `https://www.businesssellcanada.com/sale/buy/businesses-for-sale-in-ontario.htm`
  - GTA: `https://www.businesssellcanada.com/sale/buy/businesses-for-sale-in-toronto-gta-around.htm`
  - Province index links on-page: `BC AB SK MB ON GTA QC NB NS PE NL YT`
  - Postal-code map: `https://www.businesssellcanada.com/sale/buypcmap.htm`
- **Account**: **none needed** — "No Charge for using this Internet service." Login is seller-only.
- **Category**: no clean category URL — **use the on-page search / scan** and keyword-match
  `software`, `SaaS`, `technology`, `web`, `app`, `subscription`.
- **Check**: small, unbrokered, often stale — but exactly where a cheap Canadian software listing
  hides that the polished portals don't carry. Verify the listing is current.

### 8. Sunbelt Canada — largest Canadian brokerage
- **Canada browse**: `https://www.sunbeltcanada.com/businesses-for-sale-in-canada/`
- **Ontario**: `https://www.sunbeltcanada.com/businesses-for-sale-ontario/`
- **Regional office views** (each office lists its own inventory), e.g.
  `https://www.sunbeltcanada.com/toronto-centre/view-businesses-for-sale/`,
  `https://www.sunbeltcanada.com/calgary/view-businesses-for-sale/`,
  `https://www.sunbeltcanada.com/montreal-central/view-businesses-for-sale/`
- **Account**: not required to browse; contact the listing broker for the CIM (NDA per deal).
- **Category/price**: no visible category URL param → use on-site search + keyword `software`,
  `SaaS`, `technology`; ask the broker to filter by price ≤ $500K.
- **Check**: mostly Main-Street/operating businesses; software is rare here — scan quickly, don't dwell.

### 9. DealStream (formerly MergerNetwork) — membership-gated (403 to bots)
- **Software browse**: `https://www.dealstream.com/businesses-for-sale/software`
- **Location + category**: use the site filters for **Country = Canada** and category
  **Software / Technology / Internet / SaaS**; price ≤ $500K.
- **Account**: **free membership required** to view most listings and to contact sellers
  (paid tiers surface more). Detail pages **403 to bots** → log in.
- **Keyword searches**: `SaaS Canada`, `Ontario software`, `compliance SaaS`, `vertical B2B SaaS`.
- **Check**: mix of brokered + owner-listed; heavier on lower-middle-market — confirm it's micro
  (≤ $500K) and genuinely SaaS.

### 10. Kijiji — Business-for-Sale classifieds (long-tail, cheap)
- **Category base**: `https://www.kijiji.ca/b-business-for-sale/canada/c637l0`
  (category ID **637** = Business for Sale; `l0` = all Canada)
- **By location** (replace the location slug/ID from the UI):
  - Ontario: `https://www.kijiji.ca/b-business-for-sale/ontario/...l9004`
  - GTA/Toronto: `https://www.kijiji.ca/b-business-for-sale/city-of-toronto/...l1700273`
  - BC/Vancouver: `https://www.kijiji.ca/b-business-for-sale/vancouver/...l1700287`
  (Kijiji builds the exact `l####` location ID when you pick a city — grab it from the URL.)
- **Keyword search**: append `?q=software` / `?q=SaaS` / `?q=subscription` / `?q=app`; sort by newest.
- **Account**: not needed to browse; free account to message sellers.
- **Check**: unbrokered, unverified, often tiny — highest noise, but occasionally a real Canadian
  software seller with no broker. Apply Buy Box + verification hard.

### 11. Latona's — curated, account + NDA gated
- **Browse URL**: `https://latonas.com/listings/`
- **Account**: **account AND signed NDA required** before listing details/pricing show.
- **Filters**: revenue-stream = **SaaS**; **Location filter includes Canada**; price bands $0–$50K
  up to $5M+; annual profit $0–$10K → $1M+; business age; broker.
- **Check**: curated/vetted; set Location=Canada + SaaS + price ≤ $500K. Fewer, cleaner deals.

### 12. Motion Invest — mostly content, not SaaS (skim, low priority)
- **Browse URL**: `https://www.motioninvest.com/marketplace`
- **Account**: **login to view listing details** on each card.
- **Reality**: inventory is overwhelmingly **content sites + YouTube channels** (Food/Recipes,
  Home/Garden, Pets, etc.) — these are in the REJECT list. **Low priority** for this SaaS sweep;
  a 60-second skim at most.

### 13. Tiny Acquisitions — micro-SaaS (verify current domain in-browser)
- The `tinyacquisitions.com` / `tinyacq.com` domains did **not resolve** on 2026-07-04 (DNS
  failure) — the marketplace may have moved, rebranded, or shut down. **Verify by web-searching
  "Tiny Acquisitions marketplace" in your browser**; if live, filter by type=SaaS, price ≤ $500K.
- Substitute shelf if gone: **Microns.io** (`https://www.microns.io/`) — curated micro-SaaS,
  on-band, but heavy on AI-wrapper junk (the archetype to REJECT). Free browse.

---

## HOW TO VERIFY A LISTING (do this before you get excited — ~5 min per candidate)

For any listing that passes the paper Buy Box, before contacting the seller confirm:
1. **Canadian domicile** — company incorporated in Canada (ON/BC ideal). Ask for the incorporation
   province; a US/other-domicile SaaS defeats the purpose of this sweep.
2. **Recurring, not one-time** — the "revenue" is subscription MRR, not lifetime deals / services /
   one-off projects dressed up as recurring.
3. **Real age** — ≥18–24 months of operating history (not a 3-month flip).
4. **Not on the REJECT list** — no consumer app, SEO/content site, Chrome extension, thin AI/LLM
   wrapper, or single-platform add-on a host (Shopify/WP/Stripe) can kill.
5. **Owner-light** — seller claims <10 hrs/wk AND is willing to do a 60–90 day paid transition + SOPs.
6. **Multiple sanity** — asking ÷ annual SDE. **>4.5x = overpriced**; **<3.5x on "stable" = probably
   buying decline** (verify why). Convert USD→CAD (≈1.37) before comparing to the ≤ $500K CAD ceiling.
7. **Why selling** — a coherent, non-alarming reason (retirement, focus shift) — not "growth stalled"
   in disguise.
8. **Concentration smell test** — ask top-customer % and channel mix on the first call.

**If it clears all 8 → request read-only access and run the Gate-2 script below. No live access = walk.**

---

## THE GATE-2 SCRIPT (the #1 gate — source-verification, free, do before any offer)

This is the diligence pass that kills most "clean-looking" deals. **Screenshots are worthless —
demand live read-only access or walk.**

**A. Read-only revenue three-way reconcile**
- Request **read-only Stripe** login + **bank/PayPal statements** + the **P&L they showed**.
- Reconcile all three: **bank deposits ↔ Stripe MRR ↔ stated P&L.** Any gap = dressed-up numbers.

**B. Build the cohort retention curve YOURSELF (from the raw Stripe export)**
- Confirm MRR is flat/growing on a **revenue-retention** basis — NOT propped up by new-logo adds
  masking churn. Re-baseline to **~4.5%/mo**, not the ≤3% the seller claims. The cohort curve must
  actually **flatten**.
- Separate **recurring MRR from one-time/services**; flag lifetime/heavily-discounted annual plans
  and **unscheduled discount spikes** (classic dress-up tactics).

**C. Customer concentration — "% of ARR from the largest customer"**
- Pull per-customer MRR from the Stripe export. **Largest single customer < 20% of ARR** (else the
  business is one email away from a cliff). Also check **acquisition-channel** concentration — no
  single channel (esp. price-competitive PPC vs funded rivals) carrying the business.

**D. "What runs WITHOUT the LLM?" (the durability / AI-safe test)**
- If the product uses AI/LLM features, ask: **strip the LLM call out — what's the residual value?**
  - If the answer is "nothing / it's a prompt wrapper" → **REJECT** (an LLM can clone it; the vendor
    can raise API prices and crush the margin).
  - If the moat is the **customer's data / compliance history / system-of-record + workflow** and the
    LLM is just a convenience feature on top → **PASS** (durable; that's the archetype we want).
- Confirm the **hosting/API cost floor**: what does inference cost per customer, and does a vendor
  price hike (OpenAI/Anthropic/etc.) blow up the unit economics? Price the TRUE hosting/ops cost —
  sellers understate it.

**E. Tech / IP quick-hit (Hooman's edge)**
- Clean **IP chain** (every contributor's IP assigned — missing contractor assignment is a top
  killer). No secrets committed in the repo; a real, tested backup story; no single undocumented
  cron/hack holding it together.

**Walk instantly on any of**: refuses live read-only Stripe/bank; declining revenue dressed as
"stable"; churn masked by new logos; >20% single-customer concentration; thin/undocumented code or
unclear IP; platform-dependent or AI-wrapper commodity; lifetime revenue dressed as recurring;
owner-as-the-product with no SOPs.

---

## FINANCING NOTE (Hooman's Canadian-citizen edge — from CANADA_SEARCH_REPORT)
- **≤ $160K CAD** deals → **all-cash** (caps downside; the playbook's core recommendation).
- **$160–500K CAD** deals → financeable **~25% down + BDC/bank term loan + seller note** (BDC ≈ SBA-
  equivalent leverage, available TODAY as a Canadian citizen — no visa issue owning/operating a
  Canadian company remotely from the US on TN). Reaches a ~$1.3–2M business on $500K cash if he wants.
- **Structure**: mostly cash on the bulk + **10–30% as a revenue-retention earnout/seller note through
  escrow** + non-compete + 60–90 day paid transition. Treat an *eagerly*-offered earnout as a low-
  confidence signal (adverse selection), not a discount to celebrate.

---

## OUTPUT OF THE SWEEP
Log every candidate that passes the paper Buy Box in a simple table (marketplace, URL, price CAD,
MRR/SDE, domicile, why-it-fits, verification status). Anything that clears "How to verify" → request
read-only access → run Gate-2. **If nothing clears in the hour, that's fine — keep saved-search
alerts running and repeat weekly.** Patience is the risk management.

**Sources**: URLs and filter structures verified via live web fetches on 2026-07-04 (Flippa
`filter[...]` query params and Country=Canada rail; Empire Flippers free-account + SaaS monetization
filter; BizQuest `/businesses-for-sale-in-[location]/` + `/[category]-businesses-for-sale-in-[loc]/`
patterns; BusinessSellCanada `/sale/buy/businesses-for-sale-in-[province].htm`, no account; Sunbelt
Canada regional-office URLs; Latona's `/listings/` account+NDA + Location=Canada filter; Motion Invest
`/marketplace` = content/YouTube; Acquire.com free-buyer/verified-contact gating). BusinessesForSale.com,
DealStream, and BizQuest software pages returned 403 to bots — confirming the manual, logged-in pass is
required. Buy Box + Gate-2 from `runs/buy_microsaas_PLAYBOOK.md`; financing from `CANADA_SEARCH_REPORT.md`.
