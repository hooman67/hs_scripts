export const meta = {
  name: 'trackB-top5-deepdive',
  description: 'Deep-research + validate assumptions + competitor hunt for the top 5 Track-B ideas, build an execution plan for each, then adversarially validate each plan; synthesize a head-to-head',
  phases: [
    { title: 'DeepResearch', detail: 'per idea: validate every assumption, real competitor hunt, verify economics' },
    { title: 'ExecPlan', detail: 'per idea: concrete execution plan (90-day + 12-month, budget, milestones)' },
    { title: 'ValidatePlan', detail: 'per idea: adversarial red-team of the plan; do the numbers/assumptions hold?' },
    { title: 'Synthesize', detail: 'updated head-to-head + recommendation across the 5' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'

const IDEAS = [
  { slug: 'exam_prep_course', name: 'Certification / licensing exam-prep course (mandated exam)',
    claims: 'Legally-mandated demand; 85%+ margin; near-passive after a 3-6mo build; $5-25K/mo once ranked; <$30K capital. Proof cited: Drone Launch Academy ~$50K/mo on FAA Part 107. Key open question: WHICH mid-size mandated exam has rising volume AND weak/dated incumbents (not PMP/CPA which are saturated)?' },
  { slug: 'managed_hosting', name: 'Managed technical hosting / DevOps-lite subscription (HostiFi model)',
    claims: 'Infra IS the product = 1:1 fit with Hooman Adobe cloud/infra skills; most AI-safe; $5-25K/mo; ~$25-60K capital, largely bootstrappable from client cash; low downside. Proof: Reilly Chase bootstrapped HostiFi solo to $100K/yr then ~$1M ARR. Key open questions: which self-hosted tool has a large NON-technical base AND does NOT compete with the vendor own managed cloud? Risk of vendor launching their own cloud?' },
  { slug: 'vertical_bookkeeping', name: 'Vertical bookkeeping / financial-ops subscription (one industry)',
    claims: 'Boringest/safest/most durable; fully delegable to trained bookkeepers/VAs; $5-15K/mo with 10-20 clients; <$50K capital; QuickBooks ProAdvisor cert = a weekend. Key open questions: which vertical? realistic client acquisition cost + churn? can it truly be delegated while Hooman keeps a day job? competitive density (Bench, Pilot, Bookkeeper360, thousands of local firms)?' },
  { slug: 'royalty_licensing', name: 'License an engineered product design for royalties (inventRight model)',
    claims: '<$5K/idea, no inventory, no personal guarantee; $5-15K/mo across a portfolio after 18-36mo; monetizes an engineer native output. Proof cited: Lonnie Johnson (Super Soaker), Rotimatic. Key open questions: what is the REAL base-rate of getting a product licensed via cold outreach? is inventRight itself a coaching-upsell scheme? typical royalty rates + advance? how many submissions to land one deal?' },
  { slug: 'buy_microsaas', name: 'Buy a cash-flowing boring B2B / vertical micro-SaaS ($2-8K MRR, $80-150K)',
    claims: 'Skips the 0->1 distribution grind by buying customers; $3-6K/mo net at purchase -> $8-15K/mo over 12-24mo; downside capped at all-cash price; Hooman eng brain = diligence + AI-ops edge. Proof cited: Empire Flippers listings ~25-40x monthly multiple, $589M+ transacted. Key open questions: real current multiples for $2-8K MRR SaaS? realistic post-acquisition churn/growth? how much operating time really required? seller-financing norms?' },
]

const RESEARCH_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['idea','slug','assumptions_checked','competitors','economics_verified','verdict','confidence','kill_risks','best_niche_or_target'],
  properties: {
    idea: { type: 'string' }, slug: { type: 'string' },
    assumptions_checked: { type: 'array', description: 'each key claim from the pitch, marked VERIFIED / PARTIALLY-TRUE / FALSE / UNVERIFIED with the evidence + source',
      items: { type: 'object', additionalProperties: false, required: ['claim','status','evidence'],
        properties: { claim: { type: 'string' }, status: { type: 'string', enum: ['VERIFIED','PARTIALLY-TRUE','FALSE','UNVERIFIED'] }, evidence: { type: 'string' } } } },
    competitors: { type: 'array', description: 'real named competitors with pricing/scale/funding if found', items: { type: 'string' } },
    economics_verified: { type: 'string', description: 'realistic revenue, margin, capital, ramp time AFTER validation — with the number that changed vs the pitch' },
    best_niche_or_target: { type: 'string', description: 'the specific niche/exam/tool/vertical/target that best fits, chosen from real research (not generic)' },
    kill_risks: { type: 'array', items: { type: 'string' }, description: 'the risks that could actually kill it' },
    confidence: { type: 'string', enum: ['HIGH','MEDIUM','LOW'] },
    verdict: { type: 'string', enum: ['PURSUE','CONDITIONAL','PASS'] },
  },
}

const VALIDATION_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['slug','plan_holds','weakest_assumptions','numbers_recheck','revised_verdict','revised_monthly_profit','confidence'],
  properties: {
    slug: { type: 'string' },
    plan_holds: { type: 'string', enum: ['HOLDS','HOLDS-WITH-CHANGES','DOES-NOT-HOLD'] },
    weakest_assumptions: { type: 'array', items: { type: 'string' }, description: 'the assumptions most likely to be wrong, and why' },
    numbers_recheck: { type: 'string', description: 'independent sanity-check of the plan financials; where they are optimistic' },
    revised_monthly_profit: { type: 'string', description: 'honest revised realistic monthly profit range after red-teaming' },
    revised_verdict: { type: 'string', enum: ['PURSUE','CONDITIONAL','PASS'] },
    confidence: { type: 'string', enum: ['HIGH','MEDIUM','LOW'] },
  },
}

// Pipeline: research -> exec plan -> adversarial validation, per idea, no barrier between ideas.
const results = await pipeline(IDEAS,
  // Stage 1: deep research + validate assumptions + competitors
  (idea) => agent(
    `You are doing DEEP RESEARCH + ASSUMPTION VALIDATION for a secondary-income business idea for Hooman (Adobe eng ` +
    `manager; AI/ML+cloud+infra; EE; mech-eng friends; $25-150K capital; ~10-20 hrs/wk; wants $5-30K/mo profit; ` +
    `AI-safe = outside crowded AI/software hype). He is already building CutLog (laser SaaS) and time is his real ` +
    `constraint.\n\nIDEA: "${idea.name}"\nPITCH CLAIMS TO VALIDATE: ${idea.claims}\n\n` +
    `Read ${ROOT}/research-plan-lifestyle.md (Track-B mandate + scorecard) and ${ROOT}/runs/trackB/TRACKB_REPORT.md ` +
    `(the source pitch and its context) first.\n\n` +
    `Then do REAL WEB RESEARCH (WebSearch/WebFetch). Your job is to be a SKEPTIC:\n` +
    `  1. Take EVERY claim in the pitch and verify it against real sources. Mark each VERIFIED / PARTIALLY-TRUE / ` +
    `FALSE / UNVERIFIED with the evidence + URL. Especially scrutinize income claims (survivorship bias?), the ` +
    `"proof" examples (are they representative or outliers?), margins, capital, and time.\n` +
    `  2. Hunt REAL competitors: named companies, their pricing, scale, funding, and whether they already own the ` +
    `best niche. Check for the incumbents/aggregators/OEMs this project keeps finding.\n` +
    `  3. Pin down the SPECIFIC best niche/target (which exam, which self-hosted tool, which bookkeeping vertical, ` +
    `which product category, which SaaS profile) from real data — not a generic answer.\n` +
    `  4. Re-derive the REALISTIC economics (revenue, margin, capital, ramp) and note which pitch number changed.\n` +
    `  5. List the kill-risks and give a verdict (PURSUE / CONDITIONAL / PASS) + confidence.\n\n` +
    `WRITE your findings to ${ROOT}/runs/trackB/deep/${idea.slug}/01_research_validation.md (use Write; create ` +
    `folders; cite sources inline). THEN return the structured schema.`,
    { label: `research:${idea.slug}`, phase: 'DeepResearch', schema: RESEARCH_SCHEMA, agentType: 'general-purpose' }
  ).then(r => r ? { ...r, _idea: idea } : null),

  // Stage 2: execution plan (uses stage-1 findings)
  (research, idea) => {
    if (!research) return null
    return agent(
      `You are writing a concrete EXECUTION PLAN for a secondary-income business for Hooman (Adobe eng manager; ` +
      `$25-150K capital; ~10-20 hrs/wk alongside a day job; wants $5-30K/mo; already building CutLog).\n\n` +
      `IDEA: "${idea.name}"\n\n` +
      `The deep-research/validation stage produced these findings (JSON) — BUILD THE PLAN AROUND THE VALIDATED ` +
      `REALITY, not the original optimistic pitch:\n${JSON.stringify(research, null, 2)}\n\n` +
      `Also read your own research doc at ${ROOT}/runs/trackB/deep/${idea.slug}/01_research_validation.md for detail.\n\n` +
      `Write a concrete, realistic execution plan:\n` +
      `  - The specific target (exact niche/exam/tool/vertical/acquisition profile chosen in research).\n` +
      `  - First 90 days: week-by-week concrete actions, who does what, what gets validated when.\n` +
      `  - Months 4-12: path to the revenue target, hiring/delegation plan (this MUST stay part-time for Hooman).\n` +
      `  - Itemized budget within $25-150K; monthly burn; break-even point.\n` +
      `  - Revenue model + realistic ramp curve (subscribers/clients/deals over time).\n` +
      `  - Concrete go/no-go decision gates and the cheapest possible validation BEFORE committing real money.\n` +
      `  - How it coexists with CutLog for Hooman's limited hours (capital+delegation vs focus).\n\n` +
      `WRITE the plan to ${ROOT}/runs/trackB/deep/${idea.slug}/02_execution_plan.md (use Write). Return a ~200-word ` +
      `summary of the plan as your final text.`,
      { label: `plan:${idea.slug}`, phase: 'ExecPlan', agentType: 'general-purpose' }
    ).then(planText => ({ research, planText, idea }))
  },

  // Stage 3: adversarial validation of the plan
  (prev, idea) => {
    if (!prev) return null
    return agent(
      `You are an ADVERSARIAL RED-TEAM validating an execution plan for a secondary-income business. Be harsh and ` +
      `specific — your job is to find where this plan breaks, not to be encouraging. Founder: Hooman (Adobe eng ` +
      `manager; $25-150K; ~10-20 hrs/wk; already building CutLog).\n\n` +
      `IDEA: "${idea.name}"\n\n` +
      `Read BOTH docs: ${ROOT}/runs/trackB/deep/${idea.slug}/01_research_validation.md and ` +
      `${ROOT}/runs/trackB/deep/${idea.slug}/02_execution_plan.md.\n` +
      `Plan summary from the previous stage: ${prev.planText}\n\n` +
      `Do additional WEB RESEARCH where needed to fact-check. Then red-team:\n` +
      `  1. Which assumptions in the plan are most likely WRONG, and what happens if they are?\n` +
      `  2. Independently sanity-check the financials (CAC, churn, ramp time, margin, time required). Where is the ` +
      `plan optimistic? Rebuild the numbers conservatively.\n` +
      `  3. Does it REALLY stay within ~10-20 hrs/wk for Hooman, or does it secretly need full-time attention?\n` +
      `  4. What is the honest revised realistic monthly profit after correcting the optimism?\n` +
      `  5. Does the plan still hold (HOLDS / HOLDS-WITH-CHANGES / DOES-NOT-HOLD) and what must change?\n\n` +
      `WRITE your red-team to ${ROOT}/runs/trackB/deep/${idea.slug}/03_plan_validation.md (use Write). THEN return ` +
      `the structured schema.`,
      { label: `validate:${idea.slug}`, phase: 'ValidatePlan', schema: VALIDATION_SCHEMA, agentType: 'general-purpose' }
    ).then(v => ({ ...prev, validation: v }))
  },
)

const done = results.filter(Boolean)
log(`Top-5 deep dive complete: ${done.length}/5 ideas fully researched, planned, and red-teamed.`)

phase('Synthesize')

const digest = JSON.stringify(done.map(d => ({
  idea: d.idea.name, slug: d.idea.slug,
  research_verdict: d.research && d.research.verdict, research_confidence: d.research && d.research.confidence,
  best_target: d.research && d.research.best_niche_or_target,
  economics: d.research && d.research.economics_verified,
  kill_risks: d.research && d.research.kill_risks,
  false_or_unverified_claims: d.research && (d.research.assumptions_checked||[]).filter(a => a.status==='FALSE'||a.status==='UNVERIFIED').map(a => a.claim),
  plan_summary: d.planText,
  plan_holds: d.validation && d.validation.plan_holds,
  revised_verdict: d.validation && d.validation.revised_verdict,
  revised_profit: d.validation && d.validation.revised_monthly_profit,
  weakest_assumptions: d.validation && d.validation.weakest_assumptions,
})), null, 2)

const synthesis = await agent(
  `You are producing the FINAL head-to-head for Hooman after deep research, execution planning, and adversarial ` +
  `validation of his top 5 secondary-income ideas (Adobe eng manager; $25-150K; ~10-20 hrs/wk; wants $5-30K/mo; ` +
  `already building CutLog, which owns his building hours). Here is the full digest across all 5 (JSON):\n\n${digest}\n\n` +
  `For context read ${ROOT}/runs/trackB/TRACKB_REPORT.md (esp. its §5 head-to-head vs CutLog: the standing advice was ` +
  `that a second stream should consume CAPITAL+DELEGATION, not his scarce focus).\n\n` +
  `WRITE ${ROOT}/runs/trackB/DEEP_DIVE_SYNTHESIS.md with:\n` +
  `  1. A verdict table: idea | validated monthly profit | capital | hrs/wk | research verdict | plan holds? | ` +
  `revised verdict | confidence.\n` +
  `  2. Which claims from the original TRACKB_REPORT survived validation and which were busted (be specific — this is ` +
  `the accountability check on the earlier optimism).\n` +
  `  3. A ranked recommendation: given that TIME is the real constraint and CutLog has his focus, which (if any) of ` +
  `the 5 should he actually pursue, and in what sequence? Distinguish capital+delegation bets (can run alongside ` +
  `CutLog) from focus bets (compete with CutLog).\n` +
  `  4. A clear "if you do ONE thing" recommendation with the concrete first step.\n\n` +
  `Be honest and quantified. If validation shows none clear a clean bar, say so. Return a ~400-word executive ` +
  `summary as your final text (relayed to Hooman).`,
  { label: 'deep-dive-synthesis', phase: 'Synthesize', agentType: 'general-purpose' }
)

return {
  ideas_completed: done.length,
  per_idea: done.map(d => ({ idea: d.idea.name, research: d.research && d.research.verdict, plan_holds: d.validation && d.validation.plan_holds, revised_verdict: d.validation && d.validation.revised_verdict, revised_profit: d.validation && d.validation.revised_monthly_profit })),
  synthesis_summary: synthesis,
}
