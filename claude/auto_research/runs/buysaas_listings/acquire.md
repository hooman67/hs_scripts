# Acquire.com — Live Listing Survey (Buy-Box Sourcing)

**Fetched**: 2026-07-02 by Claude (Opus 4.8). **For**: Hooman Shariati.
**Marketplace**: Acquire.com (https://acquire.com/) — listings live at `app.acquire.com/startup/{id}-{slug}`.

## Access reality (be honest about this)

- **The marketplace catalog / search UI is fully gated.** `acquire.com/` and `acquire.com/saas`
  are marketing pages; the real browse/filter experience is behind `app.acquire.com/signin`
  (free buyer account, some data behind buyer *verification*). `acquire.com/saas` and
  `acquire.com/marketplace` return **404** to anonymous fetches.
- **BUT individual listing pages are largely public.** Each `app.acquire.com/startup/...` page
  publicly exposes: **title, niche/description, asking price, TTM/annual revenue, and usually
  TTM/annual profit, tech stack, customer-count band, and founding year.** The listing **slug
  itself embeds MRR/ARR + margin + growth** (e.g. `...-14k-mrr-93-margin-529-growth-bootstrapped`).
- **Gated behind a buyer account** (varies by listing): exact customer count, churn/retention,
  cohort curves, customer-concentration, full P&L / financial statements, seller identity, the
  "FundIQ" verified-financials review, and the ability to message/offer.
- **Search method used**: Acquire has no public catalog, so listings were surfaced via
  `html.duckduckgo.com` `site:app.acquire.com` queries (which return the metric-rich slugs),
  then each promising listing page was fetched directly for public price/revenue/profit.
  DuckDuckGo and Bing both rate-limited / CAPTCHA-gated after ~10 queries, so this is a
  partial sample, not exhaustive.

## The overriding finding vs the Buy Box

Consistent with the playbook's own note ("Acquire has moved upmarket; most active buyers want
>$100k MRR"): **the clean, sticky, established vertical-B2B SaaS in the $75–160K band is the
scarce item.** What is abundant on Acquire right now: (a) tiny sub-$10K "starter" SaaS with
trivial revenue, (b) large $400K–$8.5M ARR businesses well over budget, and (c) marketing/
LinkedIn/UGC/agency/Shopify tools that fail the AI-safe / platform-dependency filters.
Only a couple of listings in this sample land inside the price band, and each has a Buy-Box flaw.

---

## Listings found (real, public data)

### 1. Profitable All-in-One Project & HR Platform — IN BUDGET, but flawed
- URL: https://app.acquire.com/startup/vukb2hmfud-profitable-all-in-one-project-hr-platform-34-4k-ttm-profit
- Niche: Project management + HR SaaS (horizontal, not a vertical trade)
- Asking: **$141,000** | Revenue: ~$35.3K/yr | TTM profit: **$34.4K/yr (~$2.9K/mo)** | Multiple: **~4.1x profit**
- Age: customers "since Mar 2024" (~15 mo, under the 18–24mo floor) | Tech: **PHP / Laravel / WordPress**
- Fit: **PARTIAL/WEAK.** Price and monthly profit (~$2.9K) are in-band, but: horizontal (not an
  unglamorous vertical), <18mo history, "service-driven growth" (suggests one-time/services revenue,
  not clean recurring), WordPress-adjacent thin stack. Near-100% "profit" margin on $35K rev is a flag
  (owner time not costed).
- Gated: churn, concentration, recurring-vs-services split, exact customer count (shown as band 101–387).

### 2. MLM & Affiliate Marketing SaaS — over budget, platform-dependent
- URL: https://app.acquire.com/startup/vg4c7gzfjz-mlm-affiliate-marketing-saas-143k-arr-140k-ttm-profit-600
- Niche: Affiliate/MLM program mgmt for ecommerce brands (B2B)
- Asking: **$225,000** | ARR: $143K | TTM profit: **$140K/yr (~$11.7K/mo)** | Multiple: **~1.6x profit** (cheap)
- Age: since 2018 (8+ yr, strong history) | Tech: **Shopify + WooCommerce integration**, Stripe payouts | 600+ customers
- Fit: **REJECT (mostly).** Over the $160K ceiling, and the moat is **single-platform add-on
  (Shopify/Woo can kill it)** — an explicit Buy-Box reject. The 1.6x multiple is suspiciously low
  (possible decline or platform-risk discount). Good history/margin, wrong risk profile.
- Gated: churn, concentration, growth trend (the low multiple demands you find out *why*).

### 3. B2B SaaS for Home Services Contractors — over budget, low margin
- URL: https://app.acquire.com/startup/hnxjw1b2o6-b2b-saas-for-home-services-contractors-400k-arr-ai-powered-demand-gen
- Niche: Demand-gen platform for residential home-service contractors (boring vertical trade — good)
- Asking: **$752,000** | TTM rev: $402K | TTM profit: **$64K/yr (~$5.3K/mo)** | Multiple: **~11.7x profit**
- Age: since 2011 (very long history) | Customers: "10–50 active; 400+ served" | Tech: gated
- Fit: **REJECT.** Way over budget and an eye-watering ~11.7x profit multiple (priced on ARR, not
  earnings). Only 10–50 active customers on $400K rev = **high customer concentration risk**, and
  "demand-gen" is closer to a lead-gen/marketing service than a sticky system-of-record. Right
  vertical flavor, wrong everything-else.

### 4. High-Yield B2B SaaS: Building Ops Platform — over budget (slug-only data)
- URL: https://app.acquire.com/startup/s0t9vliog5-high-yield-b2b-saas-building-ops-platform-438k-arr-399k-sde-20-yoy-arr-growth
- Niche: Building operations platform (property/facilities — an unglamorous B2B vertical, good fit)
- Slug metrics: **$438K ARR, $399K SDE, 20% YoY ARR growth** | Asking: gated (page would not render for me)
- Fit: **REJECT on size** (at a fair 4–4.5x SDE this is ~$1.6–1.8M, far over $160K), but the
  *shape* is exactly the Buy Box (vertical building-ops, ~91% SDE margin, growing). Noted as a
  "what good looks like" reference; the affordable version would be a 5–10x smaller sibling.
- Gated: asking price, churn, concentration, tech, exact customers.

### 5. Construction Management Software — financials not public
- URL: https://app.acquire.com/startup/7cv3bwnd3t-construction-management-software-for-projects-tasks-and-operations
- Niche: Construction projects/tasks/operations (vertical B2B — right neighborhood)
- Asking / revenue / profit: **not visible** (listing page returned no financials to anonymous fetch; likely early-stage or asset-only)
- Fit: **WEAK / unknown.** Right vertical, but no public financials and the CLAUDE.md learnings
  flag "construction tech" as a crowded/instant-reject domain. Would need buyer account to see if
  it has any recurring revenue at all.

### 6. Turnkey Shopify Discounts & Flash-Sales SaaS — platform-dependent reject
- URL: https://app.acquire.com/startup/g2e73jfi6k-turnkey-shopify-discounts-flash-sales-saas-800-paying-merchants
- Slug/list metrics: **~$104K ARR, ~$80K TTM profit, 800+ merchants** | Asking: gated (page didn't render)
- Fit: **REJECT.** Classic single-platform Shopify app the host can kill — explicit Buy-Box reject,
  regardless of the healthy $80K profit.

### 7. Early-Stage B2B Content Intelligence SaaS — too small
- URL: https://app.acquire.com/startup/jkz844e1sz-early-stage-b2b-content-intelligence-saas-5k-arr-paying-customers-clear-path-to-scale
- Asking: **$2,000** | ARR: ~$5–7.3K | Profit: gated (now "software only" — business closed)
- Fit: **REJECT.** Effectively a code asset, not a cash-flowing business.

### 8. Automated Web Hosting Business (WHMCS) — too small
- URL: https://app.acquire.com/startup/eub3dpjn7v-automated-web-hosting-business-with-bespoke-whmcs-redesign-premium-6-letter-com-active-mrr
- Asking: **$6,500** | Annual rev ~$1.9K | TTM profit ~$1.8K | Tech: WHMCS/cPanel/Plesk
- Fit: **REJECT.** Trivial revenue; value is really the 6-letter domain + a WHMCS reskin.

### 9. Marketing Automation Platform — far over budget (reference only)
- URL: https://app.acquire.com/startup/nn56y9r67l-marketing-automation-platform-profitable-saas
- Asking: **$8,500,000** | Rev $3.57M/yr | Profit $1.72M/yr | Since 2013 | 100k+ businesses
- Fit: **REJECT (size).** Included only to show the upper end of what's on the platform.

### Also seen in search (list-level, not individually fetched — all fail Buy Box)
- Enterprise Recognition & Gifting SaaS — $1.39M rev / $992K profit (over budget)
- Enterprise UGC SaaS — $2.9M ARR / $1.85M profit (over budget, marketing)
- Social Media / UGC Management SaaS — $2.4M ARR / $900K profit (over budget, marketing)
- AI-Powered SEO Content SaaS — 5K customers / $631K profit (**SEO/content — reject**)
- White-Label Agency SaaS — 5,000+ customers / $717K rev (agency, over budget)
- LinkedIn Engagement SaaS (two listings) — $12–14K MRR / 92–93% margin / $800K ask (**AI/engagement, reject**)
- AI Hotel Revenue Management SaaS — $800K ARR (over budget)
- Trading Analytics SaaS — 5,800 users (consumer-ish, no public financials)
- Value-Betting Community — £5K MRR / $99K ask (**consumer, reject**)

---

## Bottom line for Hooman

- **Only one listing in this sample is inside the $75–160K price band with ~$2–5K/mo profit:**
  the **Project & HR Platform ($141K, ~$2.9K/mo)** — and it's horizontal, <18mo old, WordPress-
  ish, and "service-driven," so it's a PARTIAL/WEAK at best.
- The two right-*vertical* businesses (Building Ops $438K ARR; Home Services Contractors) are
  both **well over budget** — confirming the playbook's "clean sub-$150K vertical B2B is scarce"
  thesis. The affordable end of the market skews toward tiny asset-sales, marketing/agency tools,
  and platform-dependent Shopify/LinkedIn apps that the Buy Box rejects.
- **To do real sourcing here, a free buyer account is required** to filter by price + TTM profit +
  age and to unlock churn / concentration / verified financials — the exact fields needed to clear
  Gate 1/Gate 2. Public pages are enough for a first paper-screen but not for underwriting.
