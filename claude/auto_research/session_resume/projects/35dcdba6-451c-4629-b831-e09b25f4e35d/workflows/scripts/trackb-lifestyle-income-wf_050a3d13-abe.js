export const meta = {
  name: 'trackB-lifestyle-income',
  description: 'Track B: find secondary/lifestyle income opportunities ($5-30K/mo, part-time, $25-150K capital, outside AI hype) across all business shapes, then rank on the Track-B scorecard',
  phases: [
    { title: 'Shapes', detail: 'one agent per business shape: find concrete opportunities with proven playbooks + real earnings evidence' },
    { title: 'Synthesize', detail: 'rank all opportunities on the Track-B scorecard, flag the best clear-path bets' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'

const SHAPES = [
  { key: 'micro_saas',     name: 'Boring / micro software in unglamorous low-growth niches',
    detail: 'Micro-SaaS, vertical software, directories, data products, internal-tool-as-product in un-sexy niches VCs ignore (NOT the crowded AI/consumer/dev-tool arena). Solo-maintainable software earning $5-30K/mo.' },
  { key: 'buy_digital',    name: 'Buy & operate an existing cash-flowing DIGITAL business',
    detail: 'Acquire a profitable small SaaS, content/niche site, newsletter, Shopify/FBA store, or app in the $25-150K range via Acquire.com / Flippa / Empire Flippers / MicroAcquire, then run & improve it. Focus on realistic multiples, what sells, and the improve-it playbook.' },
  { key: 'buy_physical',   name: 'Buy & operate a small BORING physical/local business',
    detail: 'Laundromats, self-storage, vending/ATM routes, car washes, service routes, semi-absentee franchises — manager-run so it fits a day job. $25-150K of Hooman cash in (SBA leverage OK but keep his cash in range). Real economics + how a part-time owner runs it.' },
  { key: 'productized_svc',name: 'Productized services (done-for-you, fixed scope/price)',
    detail: 'Niche productized services that can be systematized and delegated (e.g. specialized done-for-you work for a specific industry). Start solo, hire contractors as it grows. $5-30K/mo, part-time-compatible.' },
  { key: 'physical_prod',  name: 'Physical products / DTC / licensing in a defensible niche',
    detail: 'Design/sell a physical product in a defensible niche (NOT commodity Amazon churn / dropshipping). Licensing a design also counts. Leverage Hooman EE background + mech-eng friends. Real margins, sourcing, and moat.' },
  { key: 'content_edu',    name: 'Content / media / community / education products',
    detail: 'Niche paid newsletters, professional communities, courses, info products with a durable audience moat in a specific vertical. $5-30K/mo, part-time. What niches actually sustain this and how they start.' },
]

const SHAPE_OUT = {
  type: 'object', additionalProperties: false,
  required: ['shape', 'opportunities', 'shape_verdict'],
  properties: {
    shape: { type: 'string' },
    opportunities: {
      type: 'array',
      description: 'concrete opportunities that fit the Track-B mandate, each with real evidence people earn $5-30K/mo',
      items: {
        type: 'object', additionalProperties: false,
        required: ['name','what_it_is','proven_playbook_evidence','monthly_profit_realistic','capital_needed','time_per_week','durability_ai_safe','crowding','path_to_success_90day','downside_risk','hooman_fit','scores'],
        properties: {
          name: { type: 'string' },
          what_it_is: { type: 'string' },
          proven_playbook_evidence: { type: 'string', description: 'REAL evidence (named examples, listings, communities, case studies) that people actually make $5-30K/mo doing this. Cite sources.' },
          monthly_profit_realistic: { type: 'string' },
          capital_needed: { type: 'string' },
          time_per_week: { type: 'string' },
          durability_ai_safe: { type: 'string', description: 'will it still pay in 5-10 yrs; is AI a threat or tailwind; why competition stays low' },
          crowding: { type: 'string', description: 'is this swarmed by VC/AI startups/clones? (swarmed = bad)' },
          path_to_success_90day: { type: 'string', description: 'concrete first-90-days: how to start or acquire it' },
          downside_risk: { type: 'string', description: 'what can go wrong; can he lose the $25-150K' },
          hooman_fit: { type: 'string', description: 'can a smart generalist learn/run it part-time; any unfair advantage' },
          scores: {
            type: 'object', additionalProperties: false,
            required: ['path_to_success','income_potential','durability','capital_fit','time_fit','downside_safety','feasibility','weighted_total'],
            properties: {
              path_to_success: { type: 'number', description: '1-10, proven playbook clarity (20%)' },
              income_potential: { type: 'number', description: '1-10 toward $5-30K/mo (15%)' },
              durability:      { type: 'number', description: '1-10 durable/not-crowded/AI-safe (15%)' },
              capital_fit:     { type: 'number', description: '1-10, fits $25-150K, lower=better (15%)' },
              time_fit:        { type: 'number', description: '1-10, part-time/delegable (15%)' },
              downside_safety: { type: 'number', description: '1-10, capital safety (10%)' },
              feasibility:     { type: 'number', description: '1-10, learnable by smart generalist (10%)' },
              weighted_total:  { type: 'number', description: 'weighted /10 using the Track-B weights' },
            },
          },
        },
      },
    },
    shape_verdict: { type: 'string', description: 'honest take: is this shape a good vein for Hooman as a part-time secondary income? best sub-play?' },
  },
}

phase('Shapes')

const shapeResults = await parallel(SHAPES.map(s => () =>
  agent(
    `You are researching SECONDARY / LIFESTYLE INCOME opportunities for Hooman: an Adobe engineering manager ` +
    `(AI/ML + software + cloud infra, EE bachelor's, mech-eng friends, $25-150K capital, ~10-20 hrs/week to spare). ` +
    `He wants a secondary income stream and has DELIBERATELY PIVOTED AWAY from venture-scale tech startups. New rules:\n` +
    `  - Target: $5,000-30,000/month PROFIT (lifestyle income, NOT a $1B venture).\n` +
    `  - "AI-safe": AVOID the crowded AI/software/VC hype arena where clones swarm. Boring/low-growth = GOOD.\n` +
    `  - ANY business shape is fine (build, buy-and-operate, services, physical) — judged on the specifics.\n` +
    `  - He is a dynamic generalist HAPPY TO LEARN new things — the ONLY hard requirement is a CLEAR, CONCRETE, ` +
    `PROVEN PATH TO SUCCESS. Real people must demonstrably already make this money.\n` +
    `  - Part-time (~10-20 hrs/wk, or delegable to a manager/contractors). Capital $25-150K of his own.\n\n` +
    `FIRST read ${ROOT}/research-plan-lifestyle.md (Track B — the full mandate, funnel, scorecard, and reject list). ` +
    `Also skim ${ROOT}/LEARNINGS.md for what the venture-track search already ruled out.\n\n` +
    `YOUR ASSIGNED BUSINESS SHAPE: ${s.name}\n  Scope: ${s.detail}\n\n` +
    `Do REAL WEB RESEARCH (WebSearch/WebFetch): find ACTUAL examples, listings with real asking prices/multiples, ` +
    `income reports, operator communities, case studies. Find ~6-10 concrete opportunities within this shape that ` +
    `fit the mandate. For EACH, you MUST cite real evidence that people earn $5-30K/mo doing it (named businesses, ` +
    `marketplace listings, verified income reports, subreddit/forum threads). Run the Track-B funnel: crowding & ` +
    `durability check, path-to-success check (proven playbook + concrete 90-day start), fit & feasibility, and score ` +
    `on the Track-B scorecard. Be skeptical: reject get-rich-quick schemes, commodity races-to-the-bottom (FBA/ ` +
    `dropshipping churn), anything swarmed by AI startups, and anything needing full-time daily presence with no ` +
    `delegation path.\n\n` +
    `WRITE a report to ${ROOT}/runs/trackB/${s.key}.md (use Write; create folders) with your opportunities, evidence, ` +
    `economics, 90-day plans, risks, and citations. THEN return the structured result via the schema.`,
    { label: `shape:${s.key}`, phase: 'Shapes', schema: SHAPE_OUT, agentType: 'general-purpose' }
  ).then(r => r ? { ...r, key: s.key } : null)
))

const shapes = shapeResults.filter(Boolean)
const allOpps = shapes.flatMap(sh => (sh.opportunities || []).map(o => ({ ...o, shape: sh.shape, shapeKey: sh.key })))
log(`Track-B shapes complete: ${shapes.length}/${SHAPES.length} shapes, ${allOpps.length} total opportunities found.`)

phase('Synthesize')

const oppJson = JSON.stringify(allOpps.map(o => ({
  name: o.name, shape: o.shape, what: o.what_it_is, evidence: o.proven_playbook_evidence,
  profit: o.monthly_profit_realistic, capital: o.capital_needed, time: o.time_per_week,
  durability: o.durability_ai_safe, crowding: o.crowding, path90: o.path_to_success_90day,
  downside: o.downside_risk, fit: o.hooman_fit, scores: o.scores,
})), null, 2)

const shapeVerdicts = JSON.stringify(shapes.map(sh => ({ shape: sh.shape, verdict: sh.shape_verdict })), null, 2)

const synthesis = await agent(
  `You are synthesizing a SECONDARY / LIFESTYLE INCOME search (Track B) for Hooman (Adobe eng manager; ` +
  `$25-150K capital; ~10-20 hrs/wk; wants $5-30K/mo profit; AI-safe = outside the crowded AI/software hype arena; ` +
  `open to ANY business shape — build, buy-and-operate, services, physical — as long as there's a CLEAR PROVEN PATH ` +
  `TO SUCCESS). The venture-scale gates are DROPPED; boring/low-growth is good.\n\n` +
  `Here are all opportunities found across 6 business shapes (JSON):\n\n${oppJson}\n\n` +
  `And the per-shape verdicts:\n\n${shapeVerdicts}\n\n` +
  `Read ${ROOT}/research-plan-lifestyle.md for the scorecard/weights.\n\n` +
  `WRITE one file: ${ROOT}/runs/trackB/TRACKB_REPORT.md, containing:\n` +
  `  1. Executive summary: what are the 3-5 BEST clear-path secondary-income bets for Hooman, and why? Lead with the ` +
  `single best "if I had to start one thing Monday" pick.\n` +
  `  2. A master ranked table of ALL opportunities across all shapes (name, shape, realistic monthly profit, capital, ` +
  `time/wk, path-to-success score, durability, weighted total). Sort by weighted total.\n` +
  `  3. Shape heat-map: which business shapes are the best veins for a part-time technical generalist with $25-150K, ` +
  `and which are traps.\n` +
  `  4. For the top 3-5 picks: a concrete "how Hooman would actually start/acquire this in the next 90 days," honest ` +
  `downside, and what unfair advantage (if any) his EE/AI/mech-eng-friends/capital background gives him.\n` +
  `  5. Head-to-head vs the existing options: how do these lifestyle bets compare to CutLog (his in-flight venture) ` +
  `and the fab-shop platform? Is a lifestyle income stream a better use of his limited hours, or a distraction? Give ` +
  `an honest recommendation.\n` +
  `  6. New patterns/learnings from the Track-B search (append-worthy to LEARNINGS.md).\n\n` +
  `Be concrete, quantified, skeptical, and honest about which "proven playbooks" are real vs guru-hype. Return a ` +
  `~400-word executive summary as your final text (relayed to Hooman): name the best 3-5 bets, their realistic monthly ` +
  `profit and capital, the single top pick, and a clear recommendation on whether to pursue one now.`,
  { label: 'trackB-synthesis', phase: 'Synthesize', agentType: 'general-purpose' }
)

return {
  shapes_ran: shapes.length,
  total_opportunities: allOpps.length,
  top_by_score: allOpps.map(o => ({ name: o.name, shape: o.shape, profit: o.monthly_profit_realistic, capital: o.capital_needed, score: o.scores && o.scores.weighted_total })).sort((a,b) => (b.score||0) - (a.score||0)).slice(0, 12),
  synthesis_summary: synthesis,
}
