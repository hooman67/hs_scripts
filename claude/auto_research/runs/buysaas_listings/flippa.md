# Flippa — Live SaaS Acquisition Listings (Buy-Box Screen)

**Sourced**: 2026-07-02 by Claude (Opus 4.8). **Marketplace**: Flippa (https://flippa.com/buy/monetization/saas).
**For**: Hooman — vertical-B2B micro-SaaS buy, $75-160K (sweet spot $80-120K), $2-5K/mo net,
>=18-24mo history, AI-safe, <20% concentration, owner <10 hrs/wk.

---

## Access notes (what's public vs gated)

- The category page (`/buy/monetization/saas`) renders listings **client-side** — WebFetch on the
  raw HTML returns "No matches found" / template placeholders. The public data is reachable via
  Flippa's JSON API (`flippa.com/v3/listings?filter[property_type]=saas...`), which is how the cards
  below were pulled.
- **Publicly visible per listing (no login)**: title, niche, asking price, MRR, monthly net profit,
  profit/revenue multiple, age/established, B2B vs B2C, subscriber count, headline churn %, and a
  "verified / vetted / data-verified" badge (whether Stripe + Google Analytics are connected).
- **Gated behind a free account / NDA**: detailed financials (P&L, cohort data), full traffic
  analytics, seller notes, and tech-stack specifics. **Tech stack is almost never public** — shows as
  "not disclosed" on nearly every listing.
- **Verification caveat**: "verified" on Flippa = a Stripe/GA integration is connected, NOT a
  three-way bank↔Stripe↔P&L reconcile. Per the playbook, still do live read-only Stripe + bank
  yourself (Gate 2). Multiples shown on cards are often internally inconsistent (see AssistLayer).

---

## Best-fit candidates (near the Buy Box)

### 1. Cloud-based IMS / ISO Management System SaaS — STRONG-ish
- URL: https://flippa.com/11797351
- Price **$139,284** (reduced 20%) | ARR ~EUR 28,240 (~EUR 2,353/mo) | Profit **EUR ~1,154/mo** | ~4.8x rev / 6.7x profit
- Age **6 years** | B2B (manufacturing, healthcare, energy, logistics) | **9 subscribers** | churn **11%** | Vetted (revenue+expenses+traffic verified)
- **Fit**: This is exactly the archetype — ISO/compliance system-of-record, document control, incident
  tracking, 6yr history, boring/sticky. **Concerns**: only 9 subscribers (concentration almost
  certainly >20% per customer), 11% churn is high, profit ~$1.2K/mo is at the low end, price is at the
  top of the band for that profit. Worth a call but underwrite churn/concentration hard.

### 2. Automated NHS IT Business (zero-touch laptop provisioning) — PARTIAL
- URL: https://flippa.com/12530181
- Price **GBP 75,000 (~$101K)** | Rev GBP 2,475/mo | Profit **GBP 1,250/mo** | 5.0x | Age **2 years** (Jan 2024)
- B2B (GP surgeries, locum agencies, locum GPs) | **18 clients** | churn **5%** | **Vetted (Flippa-verified revenue)** | owner **~30 min/month**
- **Fit**: Boring vertical (healthcare IT ops), 2yr history, genuinely low owner load, fair 5x, on-band
  price, churn 5% ~ playbook's re-baselined ~4.5%. **Concerns**: 18 clients = concentration risk;
  "IT provisioning" leans services, verify how recurring the revenue really is vs one-time device
  setups. Not a pure system-of-record but sticky-adjacent. Reasonable paper-screen pass.

### 3. Profitable AI SaaS for Property Managers — PARTIAL
- URL: https://flippa.com/12279687
- Price **$109,287** (reduced 20%) | Rev ~CAD 3,989/mo | Profit **CAD ~1,616/mo** | 2.7x rev / 6.3x profit
- Age **5 years** (2021) | B2B (property mgmt firms) | **16 subscribers** | churn **2.9%** | **Vetted + Data-Verified (Stripe + GA connected)** | owner hrs gated
- **Fit**: Property/PM admin is on the playbook's named niche list; 5yr history, low 2.9% churn,
  Stripe-connected, on-band price. **Concerns**: 16 subscribers → concentration; "AI SaaS" framing
  — confirm it's a workflow/records tool with a data moat, not a thin LLM wrapper. 6.3x profit is
  above the 4-4.5x target, so there's price to negotiate. One of the better paper-screen passes.

### 4. B2B MarTech SaaS — Server-Side ROI Tracker — PARTIAL/WEAK
- URL: https://flippa.com/12014570
- Price **$90K** | Rev ~$1.3K/mo | Profit **~$1.3K/mo** | ~69x monthly profit multiple (i.e. very rich)
- Age **2 years** | B2B (MarTech) | ~100% margin
- **Fit**: B2B, 2yr history, high margin. **Concerns**: profit only ~$1.3K/mo and priced at ~69x
  monthly (~5.7x annual-ish but the card math is muddy); MarTech tracking is somewhat commoditizable
  and platform/pixel-dependent (privacy/ad-platform changes can kill it). Marginal.

### 5. Cloud-based IMS (business software) — see #1 (same category, another listing)
- URL: https://flippa.com/11797351 (canonical above)

---

## In-band but likely REJECT (age/wrapper/model flags)

### AssistLayer — Profitable AI customer support SaaS — REJECT (age + AI-wrapper)
- URL: https://flippa.com/12873277
- Price **$110,000** (reduced 8%) | MRR **$18,419** | Profit **$10,436/mo** | 97% margin | ~10.5x monthly profit (card's "1.8x" is wrong)
- Age **7 months** | B2B | **82 paying orgs** | churn **1%** | GA-verified | solo founder
- **Reject reason**: 7mo history (< 18-24mo minimum) and it's an AI customer-support wrapper — exactly
  the "thin AI wrapper an LLM can clone" reject class. Strong numbers but fails two hard filters.

### White-Label AI Logistics Load Planning (SMART LP) — REJECT (age + white-label + AI)
- URL: https://flippa.com/12935336
- Price **$220K BIN / $150K start** | Profit **$7,525/mo** | Age **1 year** | Gemini-AI + 3D viz | churn 0% | financials gated
- **Reject reason**: 13mo age, "white-label non-exclusive license" (you're not buying the sole
  business — seller keeps reselling it), AI-optimization wrapper. Fails moat + history.

### Screenify — AI recruitment/interview SaaS — REJECT (AI-wrapper, tiny base)
- URL: https://flippa.com/12258905
- Price **$75,000** | MRR $3,605 | Profit **$1,487/mo** | 4.2x | Age **2 years** | B2B | **6 subscribers** | churn 0% | **Stripe + GA verified** | 142% YoY
- **Reject reason**: only 6 paying subscribers (massive concentration), and "AI interview screening"
  is a thin-wrapper category. Verified Stripe and fair 4.2x are nice, but 6 customers ≠ a business
  with a flattening cohort curve. Reject on concentration + AI-safety.

### Native Email App Built For Whop — REJECT (single-platform add-on)
- URL: https://flippa.com/12268124
- Price $112.5K | MRR $3.8K | Profit $3.1K/mo | ~36x monthly | Age 8mo | B2B
- **Reject reason**: built entirely on the Whop platform (host can kill it) + 8mo history. Classic
  single-platform-add-on reject.

### Credit Building AI Platform — REJECT (fintech/regulatory + age)
- URL: https://flippa.com/12514968
- Price $100K | MRR $11.3K | Profit $10.6K/mo | Age 9mo | B2B/B2C fintech
- **Reject reason**: 9mo history and consumer-fintech/credit (regulatory exposure); off-profile.

### AI Video Dubbing SaaS — REJECT (AI-wrapper media)
- URL: https://flippa.com/12212870
- Price $145K | MRR $4.3K | Profit $3.8K/mo | Age 3yr | ~38x monthly
- **Reject reason**: media/AI-generation wrapper, easily cloned; not a boring B2B system-of-record.

---

## Bottom line for the paper screen

Real inventory exists on-band, but the clean vertical-B2B system-of-record deals are scarce and the
ones that exist share the **low-subscriber-count / high-concentration** problem (9-18 customers is
typical at this price). The three worth a killer-questions call:
1. **IMS/ISO compliance SaaS** (#11797351) — best archetype, but verify 11% churn + 9-customer concentration.
2. **NHS IT provisioning** (#12530181) — Flippa-verified, ~30min/mo owner load, but confirm recurring vs one-time.
3. **Property-manager SaaS** (#12279687) — Stripe-verified, 2.9% churn, 5yr history; confirm it's a
   records/workflow tool, not an AI wrapper, and negotiate off 6.3x.

Everything with the eye-catching profit ($7-10K/mo at ~$100-150K) fails on **age (<18mo) or
AI-wrapper/platform-dependency** — the market prices those low precisely because buyers discount the
moat. That matches the playbook's supply reality: cheap SaaS is abundant; clean/sticky/fairly-priced
sub-$150K B2B SaaS is the true constraint.
