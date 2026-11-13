export const meta = {
  name: 'deep-research-tier1-graduates',
  description: 'Deep-research all 19 Tier-1 cycle-21-40 graduates, then synthesize an updated master comparison + big-picture learnings report',
  phases: [
    { title: 'DeepResearch', detail: 'one agent per idea: web research + 5-part Step 6 doc + scorecard' },
    { title: 'Synthesize', detail: 'rebuild master comparison (old 30 + new 19) and write big-picture learnings' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'

const IDEAS = [
  { slug: 'plasma_consumable_life',   name: 'Plasma Consumable Life Prediction',          cycle: '030', type: 'HW+SW',  note: 'highest score ever (9/10); voltage sensor predicts plasma cutter consumable life; 50K+ tables' },
  { slug: 'wirevision_ai',            name: 'WireVision AI (wire/cable surface inspection)', cycle: '022', type: 'HW+SW', note: 'commodity cameras at 15% of SIKORA/Pixargus cost' },
  { slug: 'doseright_wwtp',           name: 'DoseRight (municipal wastewater chemical dosing)', cycle: '023', type: 'Pure SaaS', note: 'pure SaaS on existing SCADA; 14K+ small plants' },
  { slug: 'nir_laundry_soil',         name: 'NIR Laundry Soil Classifier',                 cycle: '024', type: 'HW+SW',  note: 'chemical savings visible on first invoice' },
  { slug: 'welding_gas_analytics',    name: 'Welding Shielding Gas Waste Analytics',       cycle: '024', type: 'HW+SW',  note: '$15-25 BOM sensor; universal market; zero visibility today' },
  { slug: 'dryeriq_grain',            name: 'DryerIQ (grain dryer optimization)',          cycle: '025', type: 'HW+SW',  note: '200K+ farms; 10-30% energy savings; no brand-agnostic competitor' },
  { slug: 'freshguard_ethylene',      name: 'FreshGuard (post-harvest ethylene management)', cycle: '025', type: 'HW+SW', note: '30K+ cold stores; 1/10th price of CA systems' },
  { slug: 'tab_documentation',        name: 'Wireless TAB Documentation Platform',         cycle: '026', type: 'Pure SaaS', note: 'near-zero competition; daily paper-based pain; Bluetooth instrument pairing' },
  { slug: 'labflow_dental',           name: 'Dental Lab Workflow AI (LabFlow)',            cycle: '027', type: 'Pure SaaS', note: '6K+ labs; remake-risk prediction; tech-savvy buyers' },
  { slug: 'xrf_workflow_scrap',       name: 'XRF Workflow AI for Scrap Yards',             cycle: '028', type: 'Pure SaaS', note: 'software on existing $30K XRF guns; 5K+ yards' },
  { slug: 'dpf_regen_scheduler',      name: 'DPF Regen Scheduling Optimizer',              cycle: '029', type: 'Pure SaaS', note: 'zero hardware; parasitic on Samsara/Geotab APIs; 500K+ trucks' },
  { slug: 'springback_ai',            name: 'SpringbackAI (press brake first-part-right)',  cycle: '030', type: 'Pure SaaS', note: '40K+ press brakes unserved; data moat; laser params for press brakes' },
  { slug: 'foulcast_dairy_hx',        name: 'FoulCast (dairy heat-exchanger fouling)',     cycle: '031', type: 'Pure SaaS', note: 'pure SaaS on existing sensors' },
  { slug: 'rubber_compound_formulation', name: 'Rubber Compound Formulation AI',           cycle: '033', type: 'Pure SaaS', note: 'alloy software for rubber; captures retiring chemists tribal knowledge' },
  { slug: 'cnc_router_bit_wear',      name: 'CNC Router Bit Wear Monitor',                 cycle: '035', type: 'HW+SW',  note: '50K+ woodworking shops; proven physics from metal CNC; MachineMetrics charges 10x' },
  { slug: 'pestdoc_ipm_compliance',   name: 'IPM Compliance AI (PestDoc)',                 cycle: '036', type: 'Pure SaaS', note: 'lowest capital ever ($80-150K); regulatory mandate; 15K+ PCOs' },
  { slug: 'brewox_craft_do',          name: 'BrewOx AI (craft brewery dissolved oxygen)',  cycle: '037', type: 'HW+SW',  note: '1/10th price of inline DO systems; 9K craft breweries' },
  { slug: 'nitroguard_n2',            name: 'NitroGuard (N2 generator monitoring)',        cycle: '039', type: 'HW+SW',  note: '24.5K+ plants; zero competitors; single incident = 10yr payback' },
  { slug: 'label_diecut_ai',          name: 'Label Die-Cut Registration AI',               cycle: '040', type: 'Pure SaaS', note: 'pure software on existing press cameras; 90%+ gross margin; bypasses AVT/Isra' },
]

const SCORECARD = {
  type: 'object',
  additionalProperties: false,
  required: ['idea', 'slug', 'verdict', 'scores', 'weighted_total', 'capital_estimate',
             'key_strengths', 'key_risks', 'competitors', 'interesting_facts', 'founder_fit_notes', 'one_line'],
  properties: {
    idea: { type: 'string' },
    slug: { type: 'string' },
    verdict: { type: 'string', enum: ['STRONG GO', 'GO', 'CONDITIONAL GO', 'NO-GO'] },
    scores: {
      type: 'object', additionalProperties: false,
      required: ['capital','time_to_revenue','moat','tech_risk','market_size','founder_fit','accessibility','scalability'],
      properties: {
        capital:        { type: 'number', description: '1-10, higher=lower capital needed' },
        time_to_revenue:{ type: 'number', description: '1-10, higher=faster' },
        moat:           { type: 'number', description: '1-10' },
        tech_risk:      { type: 'number', description: '1-10, higher=lower risk' },
        market_size:    { type: 'number', description: '1-10 (SAM)' },
        founder_fit:    { type: 'number', description: '1-10 for a solo ML/software/EE founder with mech-eng friends' },
        accessibility:  { type: 'number', description: '1-10, how reachable are buyers' },
        scalability:    { type: 'number', description: '1-10' },
      },
    },
    weighted_total: { type: 'number', description: 'Capital15 TimeRev15 Moat15 TechRisk10 Market10 FounderFit15 Access10 Scale10, /10' },
    capital_estimate: { type: 'string' },
    key_strengths: { type: 'array', items: { type: 'string' } },
    key_risks: { type: 'array', items: { type: 'string' } },
    competitors: { type: 'array', items: { type: 'string' }, description: 'real named competitors found via web research, with stage/funding if known' },
    interesting_facts: { type: 'array', items: { type: 'string' }, description: 'surprising/relevant facts uncovered during research' },
    founder_fit_notes: { type: 'string' },
    one_line: { type: 'string', description: 'one-sentence pitch' },
  },
}

phase('DeepResearch')

const results = await parallel(IDEAS.map(idea => () =>
  agent(
    `You are running Step 6 "Deep Research" for a startup-idea funnel. The founder is Hooman: ` +
    `an Adobe engineering manager strong in AI/ML, software, and cloud infra, with a bachelor's in ` +
    `electrical engineering and friends who are mechanical engineers. He wants a SECONDARY income-stream ` +
    `business he can largely build himself (pure software / AI preferred; hardware tolerated via mech-eng ` +
    `friends but penalized). He is ALREADY building the #1 idea (Laser Cutting Parameter SaaS = "CutLog"), ` +
    `so this is a different, second idea.\n\n` +
    `IDEA TO RESEARCH: "${idea.name}" (type: ${idea.type}). Context note: ${idea.note}.\n\n` +
    `STEP 1 — Read the source context: ${ROOT}/runs/cycle_${idea.cycle}/cycle_${idea.cycle}_report.md ` +
    `(find this idea's section). Also skim ${ROOT}/research-plan.md section "Step 6" for the deep-research playbook ` +
    `and ${ROOT}/LEARNINGS.md for cross-cutting patterns to apply.\n\n` +
    `STEP 2 — Do real WEB RESEARCH (use WebSearch/WebFetch). Investigate from multiple angles:\n` +
    `  (a) Direct competitors — named companies, what they charge, funding, customer count.\n` +
    `  (b) Indirect/manual alternatives and DIY/open-source.\n` +
    `  (c) Big-tech / incumbent risk (incl. entrenched European industrial-QC firms: SIKORA, Pixargus, ` +
    `Dr. Schenk, GlassQuality, Precitec, Marposs, Cognex, Keyence).\n` +
    `  (d) Market size (TAM/SAM) with a real source, and the buyer persona.\n` +
    `  (e) Technical feasibility: can the core be prototyped cheaply? Hardest unsolved problem? Cheapest ` +
    `commodity sensor / existing API / dataset that makes it work?\n` +
    `  (f) Regulatory drivers (mandate = demand driver = good; approval-gated = bad).\n\n` +
    `STEP 3 — WRITE a single comprehensive markdown file to ${ROOT}/deep_research/${idea.slug}/combined_research.md ` +
    `covering all five Step 6 sections: (1) Product Definition, (2) Competitive Analysis, (3) Feasibility & ` +
    `Prototype (with a cheap Phase-0 PoC path), (4) Customer Validation strategy (where buyers congregate, ` +
    `discovery questions, demand signal), (5) Scorecard. Mark every major feasibility claim VERIFIED / ASSUMED / ` +
    `UNVERIFIED. Cite source URLs inline. Be specific and quantified. Use the Write tool to create the file ` +
    `(create the folder path as needed).\n\n` +
    `STEP 4 — Return the structured scorecard via the required schema. Score honestly and skeptically — ` +
    `if web research reveals entrenched competitors or fatal feasibility gaps, say NO-GO. The "founder_fit" ` +
    `score must reflect that pure-software ideas suit Hooman best and hardware adds risk.`,
    { label: `dr:${idea.slug}`, phase: 'DeepResearch', schema: SCORECARD, agentType: 'general-purpose' }
  ).then(r => r ? { ...r, slug: idea.slug, cycle: idea.cycle, type: idea.type } : null)
))

const scored = results.filter(Boolean)
log(`Deep research complete: ${scored.length}/${IDEAS.length} ideas scored.`)

phase('Synthesize')

const tableJson = JSON.stringify(scored.map(s => ({
  idea: s.idea, slug: s.slug, cycle: s.cycle, type: s.type, verdict: s.verdict,
  weighted_total: s.weighted_total, capital: s.capital_estimate, scores: s.scores,
  strengths: s.key_strengths, risks: s.key_risks, competitors: s.competitors,
  facts: s.interesting_facts, founder_fit: s.founder_fit_notes, one_line: s.one_line,
})), null, 2)

const synthesis = await agent(
  `You are synthesizing deep research on 19 new startup-idea candidates (cycles 021-040 graduates) for ` +
  `founder Hooman (Adobe eng manager; AI/ML + software + cloud infra; EE bachelor's; mech-eng friends; wants ` +
  `a SECONDARY business, since he is already building the #1 idea "CutLog" / laser cutting SaaS). Hooman ` +
  `explicitly wants not just the best ideas and WHY, but the LARGER PATTERNS, big-picture learnings, and ` +
  `interesting/relevant facts.\n\n` +
  `Structured deep-research output for all ${scored.length} ideas (JSON):\n\n${tableJson}\n\n` +
  `ALSO read for context: ${ROOT}/deep_research/MASTER_COMPARISON.md (the original 30-idea ranking — same ` +
  `8-dimension scorecard and weights), ${ROOT}/LEARNINGS.md, and ${ROOT}/runs/final_report.md.\n\n` +
  `Produce TWO files using the Write tool:\n\n` +
  `FILE 1 — ${ROOT}/deep_research/MASTER_COMPARISON_V2.md:\n` +
  `  - A unified ranking table of ALL deep-researched ideas: the original 30 (pull scores from ` +
  `MASTER_COMPARISON.md) PLUS these 19 new ones. Columns: rank, idea, cycle, score, capital, type, verdict, ` +
  `key factor. Keep laser cutting in the table for reference but exclude it from the "recommended secondary" pick.\n` +
  `  - The full 8-dimension scorecard table for the 19 new ideas.\n` +
  `  - A "Top secondary-idea recommendation" section through THREE lenses: (a) objectively strongest standalone, ` +
  `(b) most independent from CutLog, (c) most adjacent/synergistic with CutLog (metal-fab shops -> one platform). ` +
  `Name a winner for each lens with reasoning.\n` +
  `  - A short "how the new ideas changed the picture vs the original 30" note.\n\n` +
  `FILE 2 — ${ROOT}/deep_research/BIG_PICTURE_LEARNINGS.md:\n` +
  `  - The larger patterns across all ~49 deep-researched ideas (what wins, what fails, why).\n` +
  `  - The most interesting / surprising / counterintuitive FACTS uncovered (attribute each to its idea).\n` +
  `  - Meta-learnings about markets, competition (incl. European QC incumbents), capital efficiency, ` +
  `founder-market fit, and validation channels.\n` +
  `  - A "what I'd tell Hooman if he had 60 seconds" executive summary at the very top.\n\n` +
  `Be concrete, quantified, honest about uncertainty. Return a ~400-word executive summary as your final text.`,
  { label: 'synthesis', phase: 'Synthesize', agentType: 'general-purpose' }
)

return { ideas_scored: scored.length, ranking: scored.map(s => ({ idea: s.idea, score: s.weighted_total, verdict: s.verdict })).sort((a,b) => b.score - a.score), synthesis_summary: synthesis }
