# SaaS Deep-Dive — Are the Two Favorite SaaS Options Actually Buyable?

**Created**: 2026-07-04. **Owner**: Hooman Shariati. **Question answered**: The two SaaS
picks Hooman liked best in `WIDE_SEARCH_REPORT.md` — (#2) **EH&S / SDS compliance SaaS
~$325K / $110K SDE / ~3x** and (#3) **email-service-provider SaaS ~$345K / $116K SDE / ~3x**
— were they REAL, buyable deals, or just category exemplars with no live listing behind them?

**Short verdict: BOTH WERE EXEMPLARS, NOT LIVE DEALS.** The dollar figures in the wide report
were representative archetypes ("what a ~3x deal in this category looks like"), not quotes
from an actual listing. The targeted hunt across BizBuySell, Flippa, Acquire.com, Empire
Flippers, Quiet Light, and FE International found **zero confirmed, on-thesis, in-budget
listings** in either segment on the public/unauthenticated surface. Confidence: MEDIUM (two
of the marketplaces most likely to carry these are gated behind buyer accounts — see caveats).

---

## 1. Direct answer per segment

### EH&S / SDS chemical-safety compliance SaaS — NOT-REALLY-AVAILABLE (today, on the open market)
No live SDS/EH&S SaaS listing at ~$325K / $110K SDE exists that we could confirm. The single
compliance-software hit found was a **BizBuySell "Mission-Critical Compliance Software
Platform"** (listing 2461775) — but its vertical is **deliberately obscured** (NOT confirmed
to be SDS/chemical), it does **$880K revenue / $413K EBITDA**, implying a **~$1.5–2M+ ask** —
**3–6x over the $325K exemplar and over Hooman's $500K all-cash budget.** Flippa returned "no
matches"; Empire Flippers surfaced only the unrelated reimbursement-audit SaaS. **This segment
trades OFF-MARKET** — good small players get rolled up by incumbents before they ever list.

### Email-service-provider / email-infrastructure SaaS — NOT-REALLY-AVAILABLE (on-thesis + in-budget)
No live ESP at ~$345K / $116K SDE / 425 customers exists that we could confirm. The only
**real, revenue-generating** email business found was a **12-year email CLIENT** (Flippa
11940247) — off-thesis (consumer client, not a sending platform), off-budget (**~$74K/mo
profit → ~$5M+ price, ~15x over budget**), and with **40% churn**. Everything else was either
a **$200 junk AI-wrapper** (AiMailBuddy), a **self-hosted script flip** (Inboxz), or a
**gated/"not-yet-live"** deliverability utility (Flippa 11519892). This is structurally the
**weakest** segment in the whole search.

---

## 2. Table of ALL real listings found

| Name | Marketplace | Asking | MRR / Rev | SDE / Profit | Multiple | Age | Customers | Fit | Deal-killers |
|------|-------------|--------|-----------|--------------|----------|-----|-----------|-----|--------------|
| Mission-Critical Compliance Software Platform (vertical undisclosed) | BizBuySell 2461775 | Undisclosed (~$1.5–2M+ implied) | $880K/yr | $413K EBITDA | gated (~3.5–5x) | 40 yr (1985) | 50-state, count n/d | Only compliance-SW hit; sticky/system-of-record narrative | Vertical NOT confirmed SDS; over budget; 40-yr codebase; 4 staff = key-person risk |
| 12-yr AI email management client | Flippa 11940247 | Undisclosed ("Classified") | ~$161K/mo impl. | $74,364/mo | 6.3x profit / 2.9x rev | ~14 yr | 130,000 subs, **40% churn** | Real revenue email biz; long history | Off-thesis (client not ESP); ~$5M+ price (~15x over budget); 40% churn |
| AI email-deliverability testing tool | Flippa 11519892 | gated | gated | gated | gated | gated | gated | Closest category match to infra thesis | "Not yet live" — no numbers; thin utility vs SES/Mailtrap |
| Inboxz.com self-hosted email-marketing SaaS | Flippa 9715309 | gated | gated | gated | gated | gated | gated | Email-marketing by category | "Self-hosted" = script/codebase flip, not a customer book |
| AiMailBuddy.com AI email tool | Flippa 12032401 | $200 | ~2,212 pv/mo | none | n/a | 1 yr | n/s | Nominally email-marketing SaaS | $200 junk AI-wrapper; auction ended ~337 days ago |

**Read the negative space:** not one row is both on-thesis AND in-budget AND has verified
numbers. The wide-report exemplar figures ($325K/$110K, $345K/$116K) do not correspond to any
of these.

---

## 3. Competitive reality — can a small $300–400K player survive?

### EH&S / SDS — YES it survives, but SUPPLY, not survivability, is the constraint
- **The moat is real and thesis-fit.** Switching cost is genuine: the customer's chemical
  inventory + audit history IS their system of record, and OSHA HazCom / Tier II / GHS create
  a **mandate-driven** reason to keep paying. That protects an *existing* small customer book
  — exactly Hooman's "buy cash flow, don't chase growth" playbook. Durable + remote-operable + mandate-driven: all three of his criteria are satisfied by the *archetype*.
- **But net-new growth is brutal.** VelocityEHS/MSDSonline dominates (**12,000+ chemical-mgmt
  customers, 8M+ SDS docs, 20K+ new SDS/week**, PE-backed and acquiring). It's a **PE roll-up
  zone** (50+ EHS M&A deals in 2 years; Verdantix benchmark shrank 23→19 players). A small
  player is a **hold-and-milk asset, not a growth story.**
- **Under-weighted cost:** ongoing **SDS content-refresh burden** (keeping libraries current
  vs. shifting GHS/OSHA/WHMIS rules) is a real recurring expense the exemplar glossed over.
- **The roll-up is a double-edged sword:** it makes small players buyable in principle, but
  the good ones get bought by incumbents **off-market**, so they rarely hit a marketplace.

### Email / ESP — WEAKEST segment; a generic sender is a melting ice cube
- **Most commoditized corner of SaaS.** Marketing ESPs (Mailchimp/Intuit, Klaviyo, Brevo,
  HubSpot, ActiveCampaign, Kit, Beehiiv) run **free tiers up to 500–2,500 contacts** — a
  legacy ESP's customers are one price review from leaving. Transactional/infra is a race to
  the bottom under **Amazon SES ($0.10/1,000 emails)**, SendGrid, Mailgun, Postmark, Resend —
  near-zero pricing power.
- **Unique tail risk:** deliverability/sending-IP reputation is the core asset and is
  **fragile** — Google/Yahoo 2024 bulk-sender rules (DMARC, one-click unsubscribe, <0.3%
  spam) + shared-IP blocklist risk can impair the asset overnight. Absent from EH&S.
- **AI trivializes cloning** generic email tools. A 3x on a generic ESP is a **decline
  discount, not a bargain** (fails Playbook killer #6 commodity/platform; stresses #2
  churn-to-free-tier). Hooman's infra-cost-cutting edge IS real here (ESPs are infra-heavy) —
  **but** the Playbook warns not to pay a premium for a modernize-and-re-accelerate thesis,
  because small B2B SaaS churns on relationships/deliverability-trust, not on code quality.

### Which is the more defensible buy? **EH&S / SDS, decisively.**
It has a **mandate-driven, system-of-record moat** (Hooman's stated preference for
mandate-driven + durable); ESP has a **commodity + fragile-IP anti-moat.** If either segment
is pursued, it's EH&S — and only via a *vertically-defended* niche book, not a generic
horizontal sender.

---

## 4. Best real listings — what to source-verify + the Gate-2 next click

Only **one** listing is worth a Gate-2 click, and it's a stretch on budget:

**BizBuySell "Mission-Critical Compliance Software Platform" (2461775).**
- **Source-verify (NDA/broker call required):** (1) **What is the actual vertical?** — is it
  SDS/chemical/EH&S at all, or unrelated compliance? (2) **Real asking price** and whether a
  **seller note** could bring $1.5–2M into ~$500K all-cash reach. (3) **Tech stack** of a
  40-year-old product (rewrite risk). (4) **Customer count + concentration + churn.**
  (5) **Owner-as-product risk** (4 employees on $880K revenue).
- **Gate-2 next click:** submit the BizBuySell NDA/contact-seller form to learn vertical +
  price. If vertical ≠ SDS/EH&S or price > ~$700K with no seller note → **kill it.**

**Email listings:** none warrant a Gate-2 click. The email client (11940247) is off-thesis
and ~15x over budget; the rest are gated utilities or junk. **Do not spend diligence here.**

**The real Gate-2 move for EH&S is NOT marketplace browsing — it's OFF-MARKET sourcing:**
buy-side outreach to the small-vendor long tail (**SafeTec, Sitehawk, KHA/365,
MSDSDigital/SDS Manager, SafeSheet, MySDS Manager, Chemwatch**), a broker buy-side mandate,
plus standing marketplace alerts.

---

## 5. Access caveats (why confidence is MEDIUM, not HIGH)

- **Gated marketplaces not fully searched:** Acquire.com search URL 404'd + gated behind
  verified-buyer login; Quiet Light 403'd; Empire Flippers & Flippa full filters need
  accounts; FE International gated. Listing grids are JS-rendered — static fetch couldn't
  enumerate rows.
- Public/unauthenticated searches returned **zero** EHS/SDS-specific listings and no
  on-thesis in-budget ESP. To fully rule the segments in/out, a **~1-hour manual pass with
  buyer logins** on Acquire.com + Empire Flippers + FE International + Quiet Light is required
  (saved searches: *EHS, SDS, chemical compliance, safety data sheet* / *email, newsletter,
  SMTP, deliverability, ESP*).
- Competitive figures are from assistant knowledge through Jan 2026; live market-share source
  (emailtooltester) 403'd and was not independently re-verified.

Detail file: `saas_deepdive/ehs_sds_compliance.md`.

---

## 6. Honest bottom line

Neither favorite was a live deal — both were **category exemplars**. Of the two, **only
EH&S/SDS is worth any further effort**, because it's the one with a real, mandate-driven,
system-of-record moat that matches Hooman's durable + remote + mandate-driven criteria and
his "buy-and-milk" playbook. **Email/ESP should be dropped** — commodity economics, free-tier
churn, fragile sending-IP, and AI-cloning make it the weakest segment in the whole search; a
3x there is a decline discount.

But EH&S has a hard practical wall: **the good small players trade off-market** (rolled up by
incumbents before listing), so the acquisition path is **buy-side outreach + broker mandate +
alerts**, not browsing — a slower, active-sourcing game. Given that, the wide report's
laundromat (#1) and pest-control (#3) picks — which DO have live, verifiable listings today —
are more *immediately actionable* than either SaaS exemplar. **Recommended next step:** run
the ~1-hour gated-marketplace pass to confirm nothing on-thesis is hiding behind logins, and
if Hooman still wants SaaS, open **buy-side outreach to the SDS long-tail vendors** rather
than waiting for a listing. Treat the ~$325K/$110K figure as an *aspiration to source toward*,
not a deal on the shelf.
