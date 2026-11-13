# Deep Research: IPM Compliance AI ("PestDoc")

**Idea slug:** `pestdoc_ipm_compliance`
**Type:** Pure SaaS (LLM photo-to-report + compliance documentation for pest control operators)
**Researched:** 2026-06-28
**Source cycle:** `runs/cycle_036/cycle_036_report.md` (graduated Step 5, feasibility 8/10, capital $80-150K)

**One-line:** A mobile/web app where pest control technicians photograph site conditions and an LLM auto-generates a compliant IPM service report (findings, device/trend data, corrective actions, pesticide usage) in ~60 seconds instead of 30-45 minutes of manual paperwork.

**VERDICT: NO-GO.** The original cycle scored this at "competitive density 1 (zero direct competitors)." Current web research (2026) contradicts that premise: the exact value proposition — device scanning, automatic trend reporting, chemical/regulatory logging, photo-on-every-service-report, floor-plan diagramming, and auditor-accessible digital logbooks — is **already shipping inside the entrenched pest-control FSM platforms** (Fieldwork, PestPac/WorkWave, FieldRoutes/ServiceTitan, GorillaDesk). The remaining sliver (an LLM that writes report *prose* from photos) is a commodity feature the incumbents are actively building (WorkWave "doubling down on Data & AI"; ServiceTitan TitanAdvisor; NameDatBug already does AI pest ID at $0.99/mo). A standalone app fights the workflow-of-record and loses.

---

## 1. Product Definition

### Problem statement
Pest control operators (PCOs) servicing commercial accounts (restaurants, hotels, food manufacturing, healthcare, schools) must produce IPM documentation for every visit: a per-service record of pest activity, device/trap inspections, trend analysis, corrective actions, evidence that non-chemical methods were considered, and pesticide-usage logs with labels/SDS. This documentation is mandated/audited by:
- **EPA school IPM guidance** — requires "an on-site record of each pest control service, including all pesticide applications, in a searchable, organized system," plus evidence non-chemical methods were considered and monitoring records. (VERIFIED — epa.gov/managing-pests-schools)
- **GFSI / SQF food-safety audits** — SQF has 14,000+ certified sites in 40 countries; pest management records are a standard audit element. (VERIFIED count, ASSUMED audit-element detail — sqfi.com)
- **State pesticide recordkeeping + school-IPM/notification laws** (CA, NY, etc.). Fieldwork explicitly ships NY-PRL and CA pesticide reporting compliance. (VERIFIED that the requirement exists — fieldworkhq.com features page)

The pain (per original cycle): ~30-45 min/commercial visit on paperwork; at a loaded tech rate of $45-65/hr, $22-49 of avoidable cost per visit. (UNVERIFIED — could not independently corroborate the 30-45 min figure via web; trade pages were 403/CAPTCHA-blocked. Treat as a founder estimate.)

### Proposed v1 scope (3 features)
1. Tech photographs site conditions/devices; LLM vision classifies evidence and drafts report prose.
2. Auto-generated IPM report formatted to NPMA/state/audit templates with corrective actions + pesticide log.
3. API sync into existing routing software (PestPac/FieldRoutes) so it doesn't disrupt the system of record.

### Explicitly NOT
No scheduling, dispatch, billing, CRM, or routing (that is the incumbents' turf).

### Pricing (proposed)
$99/mo base (20 reports) + $5/report overage; $299/mo enterprise. Justification: saves $22-49/visit (UNVERIFIED ROI input).

### Ideal first customer
Small-mid PCO (5-50 techs) with 20+ commercial food-service/hospitality accounts; buyer = owner/operations manager.

---

## 2. Competitive Analysis

**Competitive Density Score: 4-5 (REJECT range).** This is the decisive finding and it overturns the source cycle's "density 1."

### Direct competitors — incumbent FSM platforms already do this
- **Fieldwork (fieldworkhq.com)** — "The #1 Field Service Management Software for Residential and Commercial Services." Customers include **Orkin, University of Illinois, Jacksonville Zoo**. Features VERIFIED on its site: QR/barcode **device scanning** ("record historical activity on traps… condition, activity, captures, evidences"), automatic **trend reporting**, **chemical tracking with NY-PRL + CA regulatory reporting**, **photo capture with comments on every service report**, **floor-plan/diagramming tool**, and an **audit/compliance digital logbook** with "device history, licenses or other files" for auditor access. This is ~90% of PestDoc's proposed value prop, already in market. (VERIFIED — fieldworkhq.com, fieldworkhq.com/features)
- **PestPac (WorkWave)** — explicitly lists **"IPM Logbooks"**, **"Digital Templates & Forms"**, material tracking, mobile app. WorkWave serves 375,000+ service professionals and is publicly **"doubling down on Data & AI"** (Wavelytics analytics). (VERIFIED — workwave.com/pest-control)
- **FieldRoutes (a ServiceTitan company)** — commercial solution category, interactive dashboards, mobile app, API integrations; ServiceTitan ships TitanAdvisor AI recommendations. (VERIFIED platform; AI-for-reports = ASSUMED roadmap — fieldroutes.com)
- **GorillaDesk** — "AI Agents," 100+ document templates, e-signature, notes/attachments, multi-unit buildings, material tracking. (VERIFIED — gorilladesk.com)
- **Briostack, ServSuite/ServicePro, PestPortals** — additional established pest-FSM players (sites were unreachable this session; their existence and overlap is established from the source cycle and trade coverage).

### Indirect / manual alternatives
PDF templates, paper logbooks, NPMA forms, and per-state report formats. Switching cost is real but the incumbents already digitized this — the "vs. paper" wedge is mostly closed.

### Adjacent movers / big-tech-incumbent risk (Score 5)
The defensible part of PestDoc is *not* the LLM. GPT-4V/Claude vision + templated report prose is a commodity any of the above can wire in. WorkWave is explicitly investing in AI; ServiceTitan has TitanAdvisor; **NameDatBug already ships AI pest identification at $0.99/month** (VERIFIED — namedatbug.com). The documentation lives inside the system of record (devices, accounts, routes), so the incumbent who owns the workflow can add "AI writes the report" as a feature far more cheaply than a standalone app can win the workflow.

### Open-source / DIY
A PCO with any of the above FSM tools is one "custom form + AI summary" feature away from this. Marginal.

### Why a customer would pick PestDoc over them — weak
The only credible angle is "best-in-class AI report quality + works alongside your existing FSM via API." That is a thin, easily-copied wedge against vendors who already own the data and the relationship, in a conservative, price-sensitive, consolidating industry (Rentokil/Rollins/Ecolab dominate; IBISWorld: "consolidation is the defining feature").

**Competitive verdict: NO-GO.** Density 4-5 = automatic reject per the project's own rules.

---

## 3. Feasibility & Prototype (with cheap Phase-0 PoC)

Technically, this idea is **easy** — which is precisely why it has no moat. Feasibility is high; defensibility is the killer.

### Technical feasibility — HIGH (this is genuinely buildable cheap)
- LLM vision (Claude / GPT-4V) for photo classification + report drafting: production-ready. (VERIFIED — commodity capability.)
- IPM report formats are standardized/templatable. (VERIFIED via EPA recordkeeping spec + trade norms.)
- Retrieval-augmented generation over a verified state-regulation/label database to prevent hallucinated citations: standard pattern. (ASSUMED effort: moderate; the regulation corpus assembly per-state is the real work.)

### Hardest unsolved problem
Not technical — it is **distribution and the system-of-record problem**. The documentation must tie to device IDs, account history, and pesticide logs that already live in the incumbent FSM. A standalone report-writer either duplicates that data (friction) or depends on incumbent APIs (platform risk: they can throttle/close, and they compete with you).

### Phase-0 PoC (<$100, <1 week) — VERIFIED feasible
1. Collect 20-30 real pest-service site photos (bait stations, droppings, entry points) — from public images / a friendly PCO.
2. Prompt Claude vision with an NPMA-style IPM template; have it draft a full report from the photos + a few structured inputs. Cost: a few dollars of API.
3. Show the output to 3-5 PCO owners and ask: would you trust this for an SQF/AIB audit, and would you pay for it *separately* from your FSM?
4. Demand signal to kill/continue: do they say "I'd buy this standalone" or "my PestPac/Fieldwork already does this / should just add it"? Current research predicts the latter.

### Capital
$80-150K to MVP (matches source cycle). Cheapest ever among graduates — but cheap-to-build is the problem, not the solution, when incumbents can build it cheaper *and* already own the customer.

### Risk register
| Risk | Likelihood | Impact | Mitigation | Fallback |
|------|-----------|--------|-----------|----------|
| Incumbent ships AI report feature | **High** | Fatal | Be a best-of-breed AI layer via API | Pivot to selling the AI engine to an FSM vendor |
| API dependency on competitor platform | High | High | Multi-platform integrations | Standalone capture app (loses workflow) |
| LLM hallucinated reg citations fail an audit | Med | High | RAG over verified reg DB; human review step | Manual-assist mode only |
| Conservative, price-sensitive buyers | High | Med | Heavy ROI proof | — |

**Confidence on the core feasibility claims: VERIFIED.** Confidence that feasibility translates to a viable business: **LOW** — blocked by competition, not technology.

---

## 4. Customer Validation Strategy

- **Where buyers congregate:** NPMA (National Pest Management Association) events/PestWorld; PCT (Pest Control Technology) and PMP magazines; state pest-control association meetings; pest-control owner Facebook groups and the r/Pestcontrol subreddit (per the project's "Facebook groups = highest-signal B2B" learning).
- **First 5 to approach:** independent regional PCOs with 10-40 techs and heavy food-service/hospitality books (not Rentokil/Rollins/Orkin — they have in-house/enterprise tooling).
- **Discovery question (non-leading):** "Walk me through how your techs document a commercial IPM visit today and who reviews it before an SQF/AIB audit — what's the most annoying part?" Then: "Does your current software handle that, or do you do it outside the software?"
- **Demand signal = confirmed:** a PCO says their existing FSM does *not* do it well AND verbally commits to a paid pilot for a standalone tool. **Negative signal (expected): "PestPac/Fieldwork already does logbooks/trends/photos."**
- **Outreach:** LinkedIn to PCO owners + NPMA member directory; offer a free Phase-0 report on their real photos.

---

## 5. Scorecard

| Dimension | Weight | Score (1-10) | Note |
|-----------|--------|--------------|------|
| Capital required (lower=better) | 15% | 9 | $80-150K, lowest among graduates. VERIFIED cheap. |
| Time to first revenue | 15% | 7 | Buildable in weeks; sales cycle to conservative PCOs slows it. |
| Competitive moat | 15% | 2 | Commodity LLM feature; incumbents own the workflow + data. |
| Technical risk (lower=better) | 10% | 9 | Trivially feasible; RAG-for-citations the only nuance. |
| Market size (SAM) | 10% | 6 | $29.7B US pest market (IBISWorld 2026), 34K firms; commercial-IPM-doc SAM modest ($12-60M). |
| Founder fit (solo ML/SW/EE) | 15% | 8 | Pure software, LLM-centric — squarely in Hooman's wheelhouse, no hardware. |
| Customer accessibility | 10% | 6 | Reachable via NPMA/FB groups, but conservative/price-sensitive. |
| Scalability | 10% | 7 | SaaS scales; capped by competitive ceiling. |

**Weighted total: ~6.2/10** — but the score is misleading. High capital/tech/founder-fit scores mask a **moat score of 2** and a **competitive density of 4-5**, which is an automatic reject under the project's own rules ("Tech-risk < 5 ⇒ overall < 6" has an inverse failure mode here: tech-risk is *too low*, meaning anyone can build it). **Verdict stands: NO-GO.**

### Why this overturns the source cycle
The cycle's promotion rested entirely on "competitive density 1 — no direct competitor offers AI-powered IPM report generation." Direct 2026 evidence shows the substantive IPM-documentation features (device scanning, trend reports, chemical/regulatory logging, photos, floor plans, auditor logbooks) are already shipping in Fieldwork and PestPac; the only un-shipped piece is LLM-written prose, which is a commodity the incumbents are openly racing to add. The regulatory tailwind (EPA/SQF/state mandates — all VERIFIED) is real and good, but it benefits the incumbent who owns the system of record, not a thin standalone AI layer.
