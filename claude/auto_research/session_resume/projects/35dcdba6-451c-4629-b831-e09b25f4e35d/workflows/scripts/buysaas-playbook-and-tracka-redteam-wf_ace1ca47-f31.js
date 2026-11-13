export const meta = {
  name: 'buysaas-playbook-and-trackA-redteam',
  description: 'A: detailed buy-a-micro-SaaS acquisition playbook. B: red-team + details + plan + plan-validation for Compressed Air and Fire Sprinkler. Then a combined head-to-head update.',
  phases: [
    { title: 'Research', detail: 'A: real listings + market for buy-SaaS. B: red-team Compressed Air & Fire Sprinkler' },
    { title: 'Plan', detail: 'A: 90-day acquisition playbook. B: execution plan for each Track-A idea' },
    { title: 'Validate', detail: 'B: adversarially validate the Track-A plans' },
    { title: 'Synthesize', detail: 'update the flat ranking with red-teamed Track-A scores + buy-SaaS detail' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'

// ---------- TRACK A RED-TEAM IDEAS (get full research->plan->validate) ----------
const TRACKA = [
  { slug: 'compressed_air', name: 'Compressed Air Leak Detection',
    read: `${ROOT}/deep_research/compressed_air_leaks/ (01-05 docs) and its row in ${ROOT}/deep_research/MASTER_COMPARISON.md (optimistic 7.65).`,
    claims: 'HW+SW, ~$1.6K to validate, universal market (every factory has compressed air), irrefutable ROI (leaks waste 20-30% of compressed-air energy), only UE Systems overlaps. RED-TEAM SKEPTICALLY: ultrasonic leak detection is a mature category — who ALREADY sells this (UE Systems, Fluke ii900/ii910 acoustic imagers, SDT, Prosaris, CS Instruments, Sonotec, Distran)? Are compressor OEMs (Atlas Copco, Ingersoll Rand, Kaeser SmartLink) bundling leak analytics? Is the buyer a plant that already hires energy auditors / gets utility-rebate audits for free? Is WTP real or is this a one-time $400 handheld + a free utility audit? Gross vs net, realistic ramp, honest hrs/wk.' },
  { slug: 'fire_sprinkler', name: 'Fire Sprinkler Inspection App',
    read: `${ROOT}/deep_research/sprinkler_inspection/ and its row in ${ROOT}/deep_research/MASTER_COMPARISON.md (optimistic 6.70).`,
    claims: 'Pure SW, ~$0 hardware, regulatory driver (NFPA 25 mandates inspections), data moat, 15K+ fire-protection firms, runs on existing iPads. RED-TEAM SKEPTICALLY: who already ships fire-inspection software (BuildingReports, Inspect Point, ServiceTrade, InspectNTrack, JLL/Building Engines, FireLab, TapReports, Joyfill)? Is this a saturated field-service-management niche? What is real WTP vs incumbents; switching costs; is the "data moat" real? Is the buyer reachable/fast, or a conservative slow-adopting trade? Gross vs net, realistic ramp, honest hrs/wk for a solo non-domain founder.' },
]

const REDTEAM_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['name','slug','assumptions_checked','competitors','honest_economics','hrs_per_week','kill_risks','revised_score','verdict','confidence'],
  properties: {
    name: { type: 'string' }, slug: { type: 'string' },
    assumptions_checked: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['claim','status','evidence'],
      properties: { claim: { type: 'string' }, status: { type: 'string', enum: ['VERIFIED','PARTIALLY-TRUE','FALSE','UNVERIFIED'] }, evidence: { type: 'string' } } } },
    competitors: { type: 'array', items: { type: 'string' }, description: 'real named competitors with pricing/scale/funding' },
    honest_economics: { type: 'string', description: 'realistic monthly profit + ramp after red-team vs original claim' },
    hrs_per_week: { type: 'string' },
    kill_risks: { type: 'array', items: { type: 'string' } },
    revised_score: { type: 'number', description: 'honest /10 on the same scale as CutLog(4.5)/buy-SaaS(5.2)' },
    verdict: { type: 'string', enum: ['PURSUE','CONDITIONAL','PASS'] },
    confidence: { type: 'string', enum: ['HIGH','MEDIUM','LOW'] },
  },
}
const PLANVAL_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['slug','plan_holds','weakest_assumptions','revised_monthly_profit','revised_verdict','confidence'],
  properties: {
    slug: { type: 'string' },
    plan_holds: { type: 'string', enum: ['HOLDS','HOLDS-WITH-CHANGES','DOES-NOT-HOLD'] },
    weakest_assumptions: { type: 'array', items: { type: 'string' } },
    revised_monthly_profit: { type: 'string' },
    revised_verdict: { type: 'string', enum: ['PURSUE','CONDITIONAL','PASS'] },
    confidence: { type: 'string', enum: ['HIGH','MEDIUM','LOW'] },
  },
}

phase('Research')

// ----- (A) Buy-a-micro-SaaS detailed playbook: research stage -----
const buySaasResearch = agent(
  `You are producing the RESEARCH half of a detailed BUY-A-MICRO-SAAS acquisition playbook for Hooman (Adobe eng ` +
  `manager; AI/ML+cloud+infra; EE; $25-150K cash; ~10-20 hrs/wk; wants $5-30K/mo secondary income; will free up ` +
  `focus from CutLog for this). This idea already passed validation as the best-EV option (see ` +
  `${ROOT}/runs/trackB/deep/buy_microsaas/ 01/02/03 docs and ${ROOT}/runs/FLAT_SHOWDOWN.md — READ THESE FIRST so you ` +
  `build on them, not repeat them). The honest economics: entry ~$2-4K/mo, base case flat-to-$3-5K, ~$0-2.5K TRUE ` +
  `net after his time, capped downside; the live risk is the DELEGATION-AFFORDABILITY TRAP (a VA+dev spend that eats ` +
  `all profit on an asset he can afford).\n\n` +
  `Do REAL WEB RESEARCH (WebSearch/WebFetch) to make this concrete and actionable:\n` +
  `  1. Survey the actual marketplaces (Acquire.com, Flippa, Empire Flippers, MicroAcquire, FE International, ` +
  `Motion Invest, Tiny Acquisitions): what do $2-8K MRR B2B/vertical SaaS assets actually LIST at right now? Real ` +
  `multiples (x monthly profit / x SDE), typical asking prices, deal volume, what sells vs sits.\n` +
  `  2. Pin down the IDEAL TARGET PROFILE for HIM specifically: vertical B2B system-of-record or compliance SaaS, ` +
  `sticky/low-churn, boring niche, owner running <10 hrs/wk, tech stack he can operate, low customer concentration, ` +
  `AI-safe (not a commodity content/AI-wrapper play). Give concrete example niches.\n` +
  `  3. Diligence essentials: how to source-verify revenue (Stripe/bank), churn, code/infra quality, traffic ` +
  `concentration, key-person risk; the specific red flags that tank a deal.\n` +
  `  4. Deal structures: all-cash vs seller-financing/earnout norms for this size; how to cap downside; whether to ` +
  `AVOID SBA/personal-guarantee on a first deal.\n` +
  `  5. The delegation math done honestly: for a $2-4K/mo asset, what can realistically be delegated (support/dev) ` +
  `at what cost, and what MUST stay with Hooman — does it net out above hobby income?\n` +
  `Cite sources/listings with real numbers. WRITE findings to ${ROOT}/runs/buy_microsaas_research.md. Return a ` +
  `~250-word summary as your final text.`,
  { label: 'A:buysaas-research', phase: 'Research', agentType: 'general-purpose' }
)

// ----- (B) Track-A red-teams: research stage (parallel with A) -----
const trackaResearch = parallel(TRACKA.map(t => () =>
  agent(
    `You are an ADVERSARIAL RED-TEAM validating a startup idea that was scored OPTIMISTICALLY and never scrutinized. ` +
    `Founder: Hooman (Adobe eng manager; AI/ML+cloud+infra; EE; mech-eng friends; $25-150K; ~10-20 hrs/wk; wants ` +
    `$5-30K/mo secondary income; AI-safe preferred). Give ZERO benefit of the doubt.\n\n` +
    `IDEA: "${t.name}"\nREAD FIRST: ${t.read}\nCLAIMS TO RED-TEAM: ${t.claims}\n\n` +
    `Use the same rigor that cut CutLog from 8.85 to 4.5 and busted the Track-B ideas (see ` +
    `${ROOT}/runs/FLAT_SHOWDOWN.md and ${ROOT}/runs/trackB/DEEP_DIVE_SYNTHESIS.md for the standard and the optimism ` +
    `patterns to catch: false "no/low competition", gross-read-as-profit, top-decile-as-base-case, inverted ` +
    `founder-fit, "passive" that isn't). Do REAL WEB RESEARCH.\n` +
    `  1. Mark every claim VERIFIED / PARTIALLY-TRUE / FALSE / UNVERIFIED with sourced evidence. Hammer the ` +
    `competition claim — find who already ships this, their pricing/scale.\n` +
    `  2. Re-derive HONEST monthly profit + ramp + weekly time load for a solo founder (note: NOT his domain).\n` +
    `  3. Revised /10 on the same scale as CutLog(4.5)/buy-SaaS(5.2); verdict; confidence; kill-risks.\n\n` +
    `WRITE to ${ROOT}/runs/trackA_redteam/${t.slug}/01_redteam.md (use Write; create folders; cite sources). ` +
    `THEN return the schema.`,
    { label: `B:redteam:${t.slug}`, phase: 'Research', schema: REDTEAM_SCHEMA, agentType: 'general-purpose' }
  ).then(r => r ? { ...r, _t: t } : null)
))

const [buySaasResearchText, trackaR] = await Promise.all([buySaasResearch, trackaResearch])
log('Research phase done (buy-SaaS + 2 Track-A red-teams).')

phase('Plan')

// ----- (A) buy-SaaS 90-day acquisition playbook -----
const buySaasPlan = agent(
  `Write the detailed 90-DAY ACQUISITION PLAYBOOK for Hooman to buy a cash-flowing micro-SaaS. Build on the research ` +
  `you just produced (read ${ROOT}/runs/buy_microsaas_research.md) and the prior validation ` +
  `(${ROOT}/runs/trackB/deep/buy_microsaas/02_execution_plan.md, 03_plan_validation.md). Research summary: ` +
  `${buySaasResearchText}\n\n` +
  `Produce a concrete, week-by-week plan:\n` +
  `  - Days 1-20: marketplace accounts, saved-search filters (exact criteria), deal-flow routine, how many ` +
  `listings/wk to review.\n` +
  `  - Days 20-50: diligence funnel (screen -> LOI -> deep diligence), the exact source-verification + code/infra ` +
  `audit checklist (his engineering edge), how to shortlist 3-5.\n` +
  `  - Days 50-75: offer + deal structure (multiple range, seller note/earnout, escrow, non-compete), close.\n` +
  `  - Days 75-90: transition, first operating improvements, the delegation setup (who does what at what cost).\n` +
  `  - The honest budget (within $25-150K), expected cash yield, and the go/no-go Gate 0 (can he spare 15-20 hrs/wk ` +
  `for 6 months). Include a realistic 12-month P&L and the delegation-affordability check spelled out with numbers.\n` +
  `WRITE to ${ROOT}/runs/buy_microsaas_PLAYBOOK.md (use Write). Return a ~200-word summary.`,
  { label: 'A:buysaas-plan', phase: 'Plan', agentType: 'general-purpose' }
)

// ----- (B) Track-A execution plans -----
const trackaPlans = parallel(trackaR.filter(Boolean).map(r => () =>
  agent(
    `Write a concrete EXECUTION PLAN for "${r._t.name}" built around the RED-TEAMED reality (not the optimistic ` +
    `pitch). Founder: Hooman ($25-150K; ~10-20 hrs/wk; wants $5-30K/mo; NOT his domain). Red-team findings (JSON): ` +
    `${JSON.stringify(r, null, 2)}\nAlso read ${ROOT}/runs/trackA_redteam/${r._t.slug}/01_redteam.md.\n\n` +
    `If the red-team verdict is PASS, still write the plan BUT lead with the honest "why this is likely not worth it" ` +
    `and what would have to be true to change that. Plan must cover: the specific target segment/wedge, first 90 ` +
    `days week-by-week, path to revenue + realistic ramp, itemized budget within $25-150K, delegation to keep it ` +
    `part-time, go/no-go gates, and cheapest validation before spending real money.\n` +
    `WRITE to ${ROOT}/runs/trackA_redteam/${r._t.slug}/02_execution_plan.md (use Write). Return a ~180-word summary ` +
    `and pass along the slug.`,
    { label: `B:plan:${r._t.slug}`, phase: 'Plan', agentType: 'general-purpose' }
  ).then(txt => ({ r, planText: txt }))
))

const [buySaasPlanText, trackaPlanned] = await Promise.all([buySaasPlan, trackaPlans])
log('Plan phase done.')

phase('Validate')

// ----- (B) validate the Track-A plans -----
const trackaValidated = await parallel(trackaPlanned.filter(Boolean).map(p => () =>
  agent(
    `ADVERSARIAL RED-TEAM of the execution plan for "${p.r._t.name}". Be harsh. Founder: Hooman ($25-150K; ` +
    `~10-20 hrs/wk; not his domain). Read ${ROOT}/runs/trackA_redteam/${p.r._t.slug}/01_redteam.md and ` +
    `02_execution_plan.md. Plan summary: ${p.planText}\n\n` +
    `Do additional web fact-checking as needed. Then: (1) which plan assumptions are most likely wrong and what ` +
    `happens if so; (2) independently rebuild the financials conservatively (CAC, churn, ramp, margin, time); ` +
    `(3) does it truly stay <=10-20 hrs/wk; (4) honest revised monthly profit; (5) does the plan hold. ` +
    `WRITE to ${ROOT}/runs/trackA_redteam/${p.r._t.slug}/03_plan_validation.md. Return the schema.`,
    { label: `B:validate:${p.r._t.slug}`, phase: 'Validate', schema: PLANVAL_SCHEMA, agentType: 'general-purpose' }
  )
))

phase('Synthesize')

const digest = JSON.stringify({
  buy_saas: { research: buySaasResearchText, plan: buySaasPlanText },
  tracka_redteam: trackaR.filter(Boolean).map(r => ({ name: r._t.name, slug: r.slug, revised_score: r.revised_score, verdict: r.verdict, economics: r.honest_economics, competitors: r.competitors, kill_risks: r.kill_risks })),
  tracka_plan_validation: trackaValidated.filter(Boolean),
}, null, 2)

const synthesis = await agent(
  `Update the flat, sunk-cost-free head-to-head for Hooman now that (A) buy-a-micro-SaaS has a detailed acquisition ` +
  `playbook and (B) the two previously-un-red-teamed Track-A ideas (Compressed Air, Fire Sprinkler) have been ` +
  `red-teamed + planned + validated. Digest (JSON):\n${digest}\n\n` +
  `Read ${ROOT}/runs/FLAT_SHOWDOWN.md for the existing honest ranking (buy-SaaS 5.2, CutLog 4.5, hosting 4.5, ` +
  `fab-shop 4.4, bookkeeping 4.3, exam 3.5, licensing 3.0; Compressed Air/Fire Sprinkler were the only UNVERIFIED ` +
  `rows — now resolved).\n\n` +
  `WRITE ${ROOT}/runs/FLAT_SHOWDOWN_V2.md with: (1) the updated full ranked table with Compressed Air & Fire ` +
  `Sprinkler now at their RED-TEAMED scores (no longer estimates); (2) did either Track-A idea beat the buy-SaaS ` +
  `pick (5.2)? (3) a crisp profile + the headline plan for the buy-SaaS option and for each Track-A idea (so Hooman ` +
  `sees the details + plan for all three he asked about); (4) the final recommendation for his one venture slot, and ` +
  `whether anything changed the "free CutLog's focus, buy a micro-SaaS" call. Be honest and quantified. Return a ` +
  `~450-word executive summary as your final text (this is the main thing relayed to Hooman) covering: the buy-SaaS ` +
  `details+plan, the Compressed Air and Fire Sprinkler red-team results + plans, and the bottom-line recommendation.`,
  { label: 'synthesis-v2', phase: 'Synthesize', agentType: 'general-purpose' }
)

return {
  buy_saas_scored: 5.2,
  tracka: trackaR.filter(Boolean).map(r => ({ name: r._t.name, revised_score: r.revised_score, verdict: r.verdict })),
  tracka_plan_validation: trackaValidated.filter(Boolean).map(v => ({ slug: v.slug, plan_holds: v.plan_holds, revised_verdict: v.revised_verdict, profit: v.revised_monthly_profit })),
  synthesis_summary: synthesis,
}
