# AI Consulting for SMBs — Productized Offerings & Pricing

**Owner:** Hooman Shariati (hshariati@adobe.com) — Adobe Foundry engineering manager (AI for Coca-Cola, Home Depot, Ford, Tesco, Humain).
**Model:** Solo, initially part-time. A **portfolio of many small clients**, not one big enterprise build.
**Design constraint:** Every offering must be **productized, fixed-scope, and repeatable** — templatized once, sold many times. No bespoke enterprise engagements.
**Last updated:** 2026-08-27 by Claude (Opus 4.8).

---

## 0. A note on the pricing evidence

I attempted live web research (Google/Bing/DuckDuckGo/Clutch/Zapier/Make/Reddit) but nearly all
sources were blocked in this environment (403/404/ECONNREFUSED). The dollar figures below are
therefore my **calibrated estimates** drawn from well-documented market norms for AI-automation
agencies and productized services as of my knowledge cutoff. I mark each anchor:

- **[ASSUMED]** — my estimate from general market knowledge; validate before quoting a real client.
- **[BENCHMARK]** — a widely-cited industry range I'm confident about from training data (still verify).

**Reference ranges I'm anchoring to (all [BENCHMARK], verify with a fresh search before publishing):**
- Independent AI/ML consultant hourly: **$150–$350/hr** (US, senior); boutiques bill $200–$500/hr.
- AI-automation-agency "build" projects for SMBs: **$3K–$25K** one-time, most land **$5K–$15K**.
- AI-automation-agency retainers: **$1.5K–$8K/month**, most land **$2K–$5K/month**.
- Paid "AI audit / roadmap" as a foot-in-the-door offer: **$1.5K–$5K**, often credited back if they buy.
- Productized-service playbook norm: price on **value/outcome**, sell **fixed packages**, avoid hourly.

**Hooman's pricing power is above the median of this market.** Most "AI automation agency" operators
are Make.com/n8n hobbyists. Hooman is an Adobe Foundry EM who ships generative AI to Fortune-100
clients. That's a credibility premium — he should price at the **top third** of every range and lead
with the Adobe/enterprise pedigree. Don't race to the bottom against $99 Fiverr bots.

---

## 1. The Productized Service Ladder

The ladder is a deliberate funnel: a cheap, low-risk **entry offer** qualifies leads and produces a
ready-made scope for the **implementation** tier, which then converts to a **recurring retainer**.
Each rung has a fixed name, fixed scope, fixed deliverables, and a fixed price.

### Rung 1 — Entry Offer (foot-in-the-door, paid)

**"AI Opportunity Audit"** — a paid diagnostic, not a free sales call.

| Attribute | Detail |
|---|---|
| **Price** | **$1,500 flat** (part-time-friendly) — or **$2,500** for a 15+ person company. [ASSUMED] |
| **Duration** | 1 week wall-clock; ~4–6 hours of Hooman's time. |
| **Scope** | 60–90 min discovery call + async review of their tools (CRM, email, content workflow, support inbox). |
| **Deliverables** | (1) A written **AI Opportunity Map**: 5–10 automatable workflows ranked by hours saved / $ / effort. (2) A prioritized 90-day roadmap. (3) One "quick win" prototype demo (e.g., a working Zapier/n8n flow or a sample generated ad). (4) Fixed-price quotes for the top 2–3 builds. |
| **The hook** | **100% of the audit fee is credited** toward any implementation package booked within 30 days. This de-risks it for the buyer and makes "yes" easy. |
| **Why it works** | Filters tire-kickers (they paid), gives Hooman a scoped backlog to sell against, and positions him as advisor not vendor. This is the single most important rung — it's the top of the whole portfolio funnel. |

> Productization note: The audit is a **template** — a Notion/Google-Doc report skeleton, a discovery
> questionnaire, and a scoring rubric (hours-saved × frequency ÷ build-effort). After 3–4 audits it's
> a 4-hour repeatable exercise.

### Rung 2 — Implementation Packages (fixed-scope builds)

Named, fixed-scope, fixed-price builds. **Never sell hours.** Each corresponds to a flagship solution
in §2. Three price tiers so there's always a "yes" at some size:

| Package | Scope | Price (one-time) | Build effort (solo) |
|---|---|---|---|
| **Spark** | One narrow automation, one integration, light config. E.g. "meeting → CRM notes" or "inbound email triage." | **$3,500–$5,000** [ASSUMED] | 2–4 days |
| **Engine** | One full flagship solution end-to-end (e.g. content pipeline OR support RAG agent), 2–3 integrations, testing, handoff docs, 2 revision rounds. | **$8,000–$15,000** [ASSUMED] | 1–2.5 weeks |
| **Platform** | 2–3 connected solutions (e.g. CRM enrichment + proposal automation + meeting capture) as one "AI operations layer," staff training session. | **$18,000–$30,000** [ASSUMED] | 3–5 weeks |

Rules baked into every package:
- **Fixed scope in writing**, with a one-line "out of scope" list to kill scope creep.
- **2 revision rounds included**; further changes roll into the retainer (Rung 3).
- **50% deposit, 50% on delivery.** Non-negotiable for cash flow as a solo operator.
- Every package ends with a **retainer pitch** — the build is the on-ramp, not the destination.

### Rung 3 — Recurring Retainer / Managed Service ("AI on Tap")

This is the portfolio's compounding engine (see §3). The build in Rung 2 is engineered to *require*
this tier: Hooman hosts it, monitors it, and keeps it working as the client's tools and prices change.

| Tier | What they get | Price (monthly) |
|---|---|---|
| **Care** | Hosting + monitoring + uptime + bug fixes + usage reporting for one deployed solution. "Keep it running." | **$500–$900/mo** [ASSUMED] |
| **Grow** | Care + a monthly iteration budget (prompt tuning, new templates, small feature adds) + monthly check-in. | **$1,500–$2,500/mo** [ASSUMED] |
| **Fractional AI Lead** | Grow across multiple solutions + a standing "AI on tap" allowance (X new automations/quarter) + priority Slack access + quarterly roadmap. Positions Hooman as their outsourced Head of AI. | **$3,000–$6,000/mo** [ASSUMED] |

> Target economics: a portfolio of **10 Grow-tier clients ≈ $15K–$25K MRR** — the whole point of the
> "many small clients" thesis. Retainers, not builds, are what make this a *business* rather than a
> string of gigs.

---

## 2. Flagship Solutions (the productized builds)

Each is buildable by a solo expert with modern tools, matched to real, common SMB pain. For each:
what it does, the stack, build effort, and pricing (setup = Rung-2 package, monthly = Rung-3 retainer).

### 2.1 "CRM Autopilot" — Meeting → CRM & Action-Item Automation
**Pain:** Sales reps hate updating the CRM by hand; data rots; managers fly blind. (Hooman's own example.)
**What it does:** Joins/records calls, transcribes, auto-writes the CRM contact/opportunity notes,
extracts next steps + follow-up tasks, drafts the follow-up email. Rep just approves.
**Stack:** Recall.ai or Fireflies/Fathom for capture → Whisper/AssemblyAI transcription → Claude
(Anthropic API) for extraction/structuring → HubSpot/Pipedrive/Salesforce API to write records →
n8n or Make.com as the orchestrator. Approval UI via Slack or a lightweight Retool page.
**Build effort:** 1–1.5 weeks (Engine).
**Pricing:** Setup **$8K–$12K**; retainer **$1,500–$2,500/mo** (Grow). [ASSUMED]
**Why solo-friendly:** All API glue + prompt engineering. No infra Hooman can't run himself.

### 2.2 "CRM Enrichment Agent" — Automated Data-Entry & Enrichment
**Pain:** CRMs full of blank/stale fields; nobody enriches leads; duplicate records.
**What it does:** Watches for new/updated records, enriches from web + data providers (company size,
industry, tech stack, LinkedIn), dedupes, standardizes, scores/routes leads, flags low-confidence
fields for human review.
**Stack:** Clearbit/Apollo/People Data Labs APIs + Claude for reasoning/normalization + firecrawl or
Exa for web lookups + CRM API + n8n. Vector store (Pinecone/pgvector) only if dedup needs fuzzy match.
**Build effort:** 3–6 days (Spark→Engine).
**Pricing:** Setup **$4K–$8K**; retainer **$500–$1,500/mo**. [ASSUMED]

### 2.3 "Content Engine" — End-to-End Marketing Content Pipeline
**Pain:** Marketing runs the whole content pipeline by hand — ideation, copy, images, video, scheduling.
(Hooman's own example, and squarely his generative-AI wheelhouse.)
**What it does:** From a brief or product list → generates on-brand copy, images, and short video,
assembles posts, routes to a human for one-click approval, schedules across channels. Keeps a brand
kit (voice, palette, logos) so output stays consistent.
**Stack:** Claude for copy/ideation → image gen (Adobe Firefly — Hooman's home turf — or Ideogram/
Flux) → video gen (Runway, Pika, or Seedance via fal.ai — he already has a Seedance skill) →
Blotato/Buffer/Later or Ayrshare API for scheduling → Airtable as the content calendar/brand kit.
**Build effort:** 1.5–2.5 weeks (Engine→Platform).
**Pricing:** Setup **$10K–$18K**; retainer **$2,000–$4,000/mo** (Grow→Fractional). [ASSUMED]
**Why it's the flagship flagship:** This is where Hooman's Firefly/gen-media expertise is a genuine
moat vs. generic automation shops. Lead with this. Highest retainer stickiness — content is *ongoing*.

### 2.4 "Product Studio" — Product-Photo & Ad-Creative Generation at Scale
**Pain:** E-commerce SMBs can't afford photo shoots; need dozens of on-model / lifestyle / seasonal
variants; ad creative fatigues fast.
**What it does:** Turns flat product shots into lifestyle scenes, generates ad-creative variants at
scale (sizes, backgrounds, seasonal themes), produces short product videos. Batch, on-brand, cheap.
**Stack:** Firefly / Flux / Nano-Banana-class editing models + background/relight tools + video gen +
a batch pipeline (Python + fal.ai) + Airtable/Shopify feed as input. Optional Retool review gallery.
**Build effort:** 1–2 weeks (Engine).
**Pricing:** Setup **$6K–$12K**; retainer **$1,000–$3,000/mo** (per-batch or subscription). [ASSUMED]
**Why solo-friendly:** Pure generative media — Hooman's core skill; the "consulting" is mostly prompt/
pipeline engineering he does in his sleep.

### 2.5 "Support Brain" — Customer-Support RAG Agent over Their Docs
**Pain:** Small teams drowning in repetitive support tickets/emails; no 24/7 coverage; slow first response.
**What it does:** Ingests their help docs, past tickets, product info → answers customer questions
(chat widget + email auto-draft), deflects tier-1 tickets, escalates the rest with a drafted reply and
full context. Cites sources so answers are trustworthy.
**Stack:** Retrieval over pgvector/Pinecone + Claude for generation + ingestion pipeline (their
Notion/Zendesk/PDFs) + widget (custom React or Chatbase-style) + Zendesk/Intercom/Front API. Guardrails
+ "I don't know → escalate" fallback.
**Build effort:** 1–2 weeks (Engine).
**Pricing:** Setup **$7K–$14K**; retainer **$1,000–$2,500/mo** (includes re-indexing as docs change —
a natural recurring hook). [ASSUMED]

### 2.6 "Quote Machine" — Sales-Proposal / Quote Automation
**Pain:** Reps spend hours hand-building proposals, quotes, SOWs; inconsistent; slow to send.
**What it does:** From a deal record or intake form → generates a tailored proposal/quote (pulls
pricing rules, past-deal language, client details), formats to their template, sends for e-sign.
**Stack:** Claude for drafting + template engine (Google Docs API / PandaDoc / Docmosis) + CRM +
pricing table in Airtable/Sheets + DocuSign/PandaDoc for signature + n8n orchestration.
**Build effort:** 4–8 days (Spark→Engine).
**Pricing:** Setup **$5K–$10K**; retainer **$500–$1,500/mo**. [ASSUMED]

### 2.7 "Ops Copilot" — Internal Operations Agents
**Pain:** Repetitive back-office work — invoice/receipt processing, data entry between systems, report
generation, onboarding checklists, inbox triage.
**What it does:** A set of small internal agents: e.g. inbound-email triage & routing, invoice-to-
accounting-system extraction, weekly auto-generated ops report, doc/data reconciliation.
**Stack:** Claude (tool-use / structured extraction) + n8n/Make + their stack (QuickBooks/Xero, Gmail,
Slack, Sheets, Notion). OCR via a vision model for documents.
**Build effort:** per-agent 2–5 days; sold as a bundle (Platform).
**Pricing:** Setup **$5K–$15K** (bundle); retainer **$1,000–$2,500/mo**. [ASSUMED]

### 2.8 "Voice/Reception Agent" — Inbound Call & Lead Capture (optional 8th)
**Pain:** SMBs (clinics, trades, local services) miss calls = miss revenue; no after-hours coverage.
**What it does:** AI voice agent answers calls, books appointments, captures leads into CRM, answers FAQs.
**Stack:** Vapi / Retell / Bland.ai (voice layer) + Claude for reasoning + calendar + CRM APIs.
**Build effort:** 3–6 days (Spark→Engine).
**Pricing:** Setup **$3.5K–$8K**; retainer **$500–$1,500/mo** + usage. [ASSUMED]
**Note:** High-demand, easy-to-productize for local-services verticals — good "many small clients" fit,
but further from Hooman's gen-media strength. Consider as a later add.

**Prioritization for Hooman specifically:** Lead with **2.3 Content Engine** and **2.4 Product Studio**
(his generative-AI moat), plus **2.1 CRM Autopilot** and **2.5 Support Brain** (universal SMB pain,
easy demos). These four cover his two stated pain examples and play to his strengths.

---

## 3. The Recurring-Revenue Angle (the portfolio thesis)

One-off builds are a treadmill. Retainers compound. The entire practice should be architected so that
**every build naturally becomes a subscription.** How:

1. **Sell outcomes that decay, then charge to keep them alive.** Prompts drift, model prices/versions
   change (GPT/Claude/Gemini updates monthly), APIs deprecate, the client's docs and product change.
   Frame the retainer honestly: *"AI systems aren't set-and-forget appliances; they need tending. Care
   keeps yours working; Grow keeps it improving."* This is true, not a shakedown.
2. **Host it, so you own the switch.** Deploy on infra Hooman controls (a cheap VPS/Fly.io/Vercel +
   n8n cloud or self-hosted). The client can't easily rip it out; hosting + monitoring justifies the
   Care floor ($500–$900/mo) with near-zero marginal effort once templatized.
3. **Bundle the audit findings into a pipeline.** The Rung-1 audit surfaces 5–10 opportunities; the
   client buys 1–2 now. The rest become **future retainer upsells** ("this quarter's AI-on-tap build").
   The Fractional AI Lead tier is explicitly *"we'll keep shipping the roadmap you already paid me to write."*
4. **Usage/value kickers.** Where volume varies (support tickets, generated creatives, voice minutes),
   add a modest usage tier on top of the base retainer so revenue grows with the client's success.
5. **Land-and-expand across the portfolio.** 1 solution → 3 solutions per client over 12 months moves a
   Care client ($700/mo) to Fractional ($4K/mo) without new logo acquisition. Portfolio LTV compounds
   from *within* accounts, not just new ones.
6. **The math that makes it a business:** builds fund the pipeline; **retainers are the asset.** Goal:
   get to **~$15K–$25K MRR from 8–12 retainer clients** — that's the part-time-to-full-time bridge.

**Rule of thumb:** never deliver a build without a signed (or verbally-committed) retainer starting the
month after handoff. If a client won't take *any* retainer tier, price the one-off build 30–40% higher
to compensate for zero recurring value.

---

## 4. Delivery Model for a Solo / Part-Time Operator

**Productize (build the asset once, reuse forever):**
- The **audit** (questionnaire + scoring rubric + report template).
- **Reusable pipeline templates** per flagship (§2) in n8n/Make — clone-and-configure, don't rebuild.
- A **prompt library** (versioned, per solution) and a **brand-kit intake form** for content clients.
- A **deployment skeleton** (one repo/infra pattern: VPS + n8n + secrets + monitoring dashboard) reused
  for every client. This is what makes Care-tier retainers near-zero-marginal-cost.
- **Monitoring/reporting** — one dashboard template (uptime, runs, tokens, $ saved) auto-emailed monthly.
  This *is* the retainer deliverable; automate it.

**Templatize (standardize but light-touch per client):**
- Proposals/SOWs (from Quote Machine — dogfood it), onboarding checklist, revision-round policy,
  handoff docs, client Slack-channel setup.

**Subcontract (when demand exceeds part-time capacity):**
- **Integration grunt-work** (Zapier/n8n wiring, data cleanup) → freelance automation devs ($30–60/hr).
- **Copywriting/editing** for content clients → freelance writers.
- **Front-end/Retool UIs** if a client wants a polished internal app.
- Keep for himself: **architecture, prompt/model engineering, generative-media pipelines, client
  relationships**. Never subcontract the parts that are his moat or the parts clients pay the premium for.

**Realistic client capacity (part-time, ~10–15 hrs/week):**
- **Onboarding/build:** 1–2 active builds at a time (each 1–2 weeks). ~2–3 new builds/month max.
- **Retainer steady-state:** a well-templatized Care client ≈ 1–2 hrs/month; Grow ≈ 3–5 hrs/month;
  Fractional ≈ 8–12 hrs/month.
- **Part-time ceiling:** ~**8–12 retainer clients** (mostly Care/Grow) + 1 build in flight ≈ the limit
  before quality/support slips. That's already ~$15–25K MRR — the target.
- **Going full-time / scaling past that:** subcontract builds, keep retainer relationships; or productize
  the top 1–2 solutions into near-SaaS (self-serve config) to break the 1:1 time-for-money ceiling.

**Sequencing:** Do the first 2–3 builds *bespoke-ish* to learn the pattern, then aggressively templatize.
Don't over-engineer templates before you've sold the thing twice.

---

## 5. Honest Risks

| Risk | Why it bites a solo/part-time operator | Mitigation |
|---|---|---|
| **Scope creep** | "Can you just also…" quietly turns a $10K fixed build into unpaid hours; deadly when you have 10–15 hrs/week. | Written fixed scope + explicit out-of-scope list; **2 revisions then it's retainer work**; 50/50 deposit; change-order form. |
| **SMB churn** | SMBs are cash-fragile and impatient; a Care client at $700/mo may cancel in a downturn or if they don't *see* value. Portfolio churn erodes MRR faster than a few enterprise logos would. | Monthly value report (hours/$ saved) so ROI is visible; make the system load-bearing (hosted by you); annual prepay discount; diversify across verticals so one sector's downturn doesn't sink the book. |
| **Tools commoditizing the offering** | Zapier/HubSpot/OpenAI ship native "AI agents"; a $12K build could become a checkbox. Generic automation-agency work is *already* commoditizing. | Compete on **generative-media depth + judgment + integration + accountability**, not on "we can call an API." Lead with Firefly/gen-video work others can't replicate. Move up to Fractional-AI-Lead advisory (relationship moat, not tool moat). |
| **Support burden** | 12 live systems calling flaky third-party APIs = pager duty for one person. A model deprecation or API outage can hit every client at once. | Monitoring + alerting from day one; graceful fallbacks + human-escalation paths in every build; standardized infra so one fix propagates; Care tier explicitly *funds* this — don't give support away free. |
| **Key-person / bus-factor & time squeeze** | It's all Hooman; part-time + a demanding Adobe day-job means capacity shocks. Also: **check Adobe's moonlighting/IP/conflict-of-interest policy** before selling — this is a real gating risk, not a footnote. | Cap client count deliberately; subcontract builds early; keep 20% slack; **verify employment-agreement terms first** (mark this an open ACTION for Hooman — do not assume it's fine). |
| **Positioning as "just another AI agency"** | The market is flooded with Make.com hobbyists undercutting on price. | Don't compete on price. Anchor every conversation on the Adobe-Foundry / Fortune-100 pedigree and the paid-audit-first process. Sell to a **vertical** (pick 1–2: e.g. e-commerce brands + professional-services firms) so referrals compound. |

---

## 6. TL;DR — The Sellable Stack

- **Entry:** AI Opportunity Audit — **$1,500** (credited toward a build).
- **Build:** Spark **$3.5–5K** / Engine **$8–15K** / Platform **$18–30K** — fixed scope, 50/50, 2 revisions.
- **Recur:** Care **$500–900/mo** / Grow **$1.5–2.5K/mo** / Fractional AI Lead **$3–6K/mo**.
- **Lead flagships (Hooman's moat):** Content Engine, Product Studio, CRM Autopilot, Support Brain.
- **The thesis:** builds fund the pipeline; **retainers are the asset.** Target ~$15–25K MRR from
  8–12 small retainer clients — reachable part-time, and the bridge to going full-time.
- **First action before selling anything:** confirm Adobe employment-agreement / moonlighting terms.

*All dollar figures are [ASSUMED] calibrated estimates or [BENCHMARK] industry ranges — validate with a
live pricing search and 2–3 real sales conversations before publishing a rate card.*
