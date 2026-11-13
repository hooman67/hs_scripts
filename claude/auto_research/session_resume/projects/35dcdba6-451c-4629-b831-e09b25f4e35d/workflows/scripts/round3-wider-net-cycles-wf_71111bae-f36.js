export const meta = {
  name: 'round3-wider-net-cycles',
  description: 'Round 3: run 10 new discovery cycles (041-050) in under-explored domains with the new incumbent/moat/growth gates, then synthesize a round-3 report',
  phases: [
    { title: 'Cycles', detail: 'one agent per new domain: Step 1-4 funnel with mandatory incumbent + moat + growth gates' },
    { title: 'Synthesize', detail: 'compile graduates into round-3 report, flag moat-worthy ideas for deep research' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'

// Round 3 = deliberately UNDER-EXPLORED domains (rounds 1-2 mined industrial-QC/shop-floor).
const CYCLES = [
  { n: '041', domain: 'Vertical AI agents & LLM-workflow automation for white-collar niches (legal, accounting, HR, insurance back-office, compliance/audit). Software-only, no physical world.' },
  { n: '042', domain: 'Fintech & insurance infrastructure (embedded finance, payments plumbing, underwriting automation, claims, reconciliation, fraud). Software/data products.' },
  { n: '043', domain: 'Digital health software that is NOT FDA-gated (clinical documentation, prior-auth, medical billing/RCM, scheduling, care coordination, patient intake). Workflow SaaS, not devices.' },
  { n: '044', domain: 'Education & training software (AI tutoring, professional certification/exam prep, corporate training, simulation-based learning, credentialing).' },
  { n: '045', domain: 'Climate & energy SOFTWARE (grid/DER analytics, carbon accounting, VPP orchestration, energy-trading tools, building energy optimization). Software, explicitly NOT hardware.' },
  { n: '046', domain: 'Robotics & autonomy SOFTWARE layers (fleet orchestration, teleoperation, simulation, RL/training infra, perception middleware). The software around robots, not the robots.' },
  { n: '047', domain: 'Media, entertainment & generative-AI applications (creator tools, video/audio/image genAI workflows, game content, marketing creative automation). Founder day-job strength (Firefly/genAI).' },
  { n: '048', domain: 'Trust & safety, content provenance & authenticity (deepfake/AI-content detection, C2PA provenance, KYC/identity, brand protection, moderation tooling).' },
  { n: '049', domain: 'Bio/health DATA & informatics software, NON-wet-lab (multi-omics analysis, clinical-trial ops software, real-world-evidence, lab data pipelines, bioinformatics SaaS).' },
  { n: '050', domain: 'Consumer & prosumer software & marketplaces (creator monetization, vertical marketplaces, personal-finance, prosumer productivity, community/subscription products) — examined with a strict moat lens.' },
]

const CYCLE_OUT = {
  type: 'object',
  additionalProperties: false,
  required: ['cycle', 'domain', 'technologies_scanned', 'graduates', 'rejected_summary', 'domain_verdict'],
  properties: {
    cycle: { type: 'string' },
    domain: { type: 'string' },
    technologies_scanned: { type: 'number', description: 'how many candidate technologies/ideas were examined in Step 1' },
    graduates: {
      type: 'array',
      description: 'ideas that passed ALL gates including the new incumbent + moat + growth gates',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['name', 'one_line', 'competitive_density', 'moat_answer', 'market_cagr', 'capital_estimate', 'founder_fit', 'feasibility_score', 'why_new'],
        properties: {
          name: { type: 'string' },
          one_line: { type: 'string' },
          competitive_density: { type: 'number', description: '1-5 per Step 2 scale, AFTER the mandatory incumbent/OEM check' },
          moat_answer: { type: 'string', description: 'what stops a cloner/incumbent in 6 months (must be a real flywheel/data/lock-in, not "we build fast")' },
          market_cagr: { type: 'string', description: 'growth rate + SAM with source; reject flat/shrinking' },
          capital_estimate: { type: 'string' },
          founder_fit: { type: 'number', description: '1-10 for solo AI/ML/software/EE founder' },
          feasibility_score: { type: 'number', description: '1-10' },
          why_new: { type: 'string', description: 'why this is a DIFFERENT idea than anything in rounds 1-2 (not another industrial-QC/shop-floor sensor play)' },
        },
      },
    },
    rejected_summary: { type: 'string', description: 'brief: what was rejected and the dominant reason (esp. incumbent/OEM hits and moat failures)' },
    domain_verdict: { type: 'string', description: 'is this domain a promising new vein for a solo AI/software founder? honest take.' },
  },
}

phase('Cycles')

const cycleResults = await parallel(CYCLES.map(c => () =>
  agent(
    `You are running ONE discovery cycle (cycle ${c.n}, ROUND 3) of a startup-idea funnel for founder Hooman: ` +
    `Adobe engineering manager, strong in AI/ML + software + cloud infra, EE bachelor's, mech-eng friends, wants a ` +
    `secondary income-stream business he can largely build himself (pure software/AI strongly preferred). He is already ` +
    `building CutLog (laser-cutting SaaS). \n\n` +
    `⭐ ROUND-3 GOAL: CAST A WIDER NET. Rounds 1-2 (40 cycles) over-converged on ONE archetype — "AI/software on ` +
    `industrial equipment for underserved mid-market trades" (laser, plasma, CNC, welding, HVAC, food processing). That ` +
    `vein is MINED OUT and round-2 deep research showed those ideas have almost no moat. Do NOT produce another shop-floor ` +
    `sensor idea. Find genuinely NEW ideas in your assigned domain.\n\n` +
    `YOUR ASSIGNED DOMAIN FOR THIS CYCLE: ${c.domain}\n\n` +
    `FIRST read ${ROOT}/research-plan.md (the full funnel, Steps 1-4, and ESPECIALLY the new MANDATORY gates: the ` +
    `Incumbent/OEM Check and Moat Gate in Step 2, and the growth-rate check in Step 3). Also skim ` +
    `${ROOT}/LEARNINGS.md and ${ROOT}/deep_research/BIG_PICTURE_LEARNINGS.md so you don't repeat round-2's mistakes.\n\n` +
    `THEN run the funnel with REAL WEB RESEARCH (WebSearch/WebFetch):\n` +
    `  Step 1 — Scan ~10 recent technologies/ideas in your domain (TRL>=5, <=18mo to product, a clear enabling breakthrough).\n` +
    `  Step 2 — Competitive density (1-5). ⭐ You MUST run the full Incumbent/OEM checklist and the Moat Gate for every ` +
    `promoted idea. A "no competition" verdict is INVALID until you've searched for OEM features, funded horizontal ` +
    `platforms that list the vertical, and incumbent marketing copy. "Cheap + trivial + no flywheel" = REJECT.\n` +
    `  Step 3 — Market sizing WITH a verified CAGR from a real source (reject flat/shrinking); TAM>$1B, SAM>$100M.\n` +
    `  Step 4 — Feasibility (tech/market/execution/timing risk; capital; founder fit). Penalize hardware and anything ` +
    `needing PhDs/wet-labs/FDA approval.\n\n` +
    `WRITE a cycle report to ${ROOT}/runs/cycle_${c.n}/cycle_${c.n}_report.md (use Write; create the folder). Include the ` +
    `10 technologies scanned, per-stage decisions with reasoning, competitors found (named, with funding/stage), the ` +
    `moat answer for each graduate, and citations. Be skeptical and quantified — a cycle with ZERO graduates is a valid, ` +
    `honest outcome and better than promoting undefensible ideas.\n\n` +
    `THEN return the structured result via the schema. Only list ideas as graduates if they pass ALL gates including moat + growth.`,
    { label: `cycle:${c.n}`, phase: 'Cycles', schema: CYCLE_OUT, agentType: 'general-purpose' }
  ).then(r => r ? { ...r, cycleNum: c.n } : null)
))

const cycles = cycleResults.filter(Boolean)
const allGrads = cycles.flatMap(c => (c.graduates || []).map(g => ({ ...g, cycle: c.cycle })))
log(`Round 3 cycles complete: ${cycles.length}/${CYCLES.length} cycles ran, ${allGrads.length} total graduates across new domains.`)

phase('Synthesize')

const summaryJson = JSON.stringify(cycles.map(c => ({
  cycle: c.cycle, domain: c.domain, scanned: c.technologies_scanned,
  graduates: c.graduates, rejected: c.rejected_summary, verdict: c.domain_verdict,
})), null, 2)

const synthesis = await agent(
  `You are synthesizing ROUND 3 of a startup-idea funnel for founder Hooman (Adobe eng manager; AI/ML+software+cloud; ` +
  `EE; wants a secondary software business; already building CutLog). Round 3's goal was to CAST A WIDER NET across ` +
  `10 previously under-explored domains (software-native, fintech, digital health, education, climate SOFTWARE, robotics ` +
  `software, generative-AI apps, trust & safety, bio informatics, consumer/prosumer) using new mandatory gates ` +
  `(incumbent/OEM check, moat gate, growth-rate check).\n\n` +
  `Here is the structured output of all ${cycles.length} new cycles (JSON):\n\n${summaryJson}\n\n` +
  `For context on what "good" looks like and what to avoid, read ${ROOT}/deep_research/MASTER_COMPARISON_V2.md and ` +
  `${ROOT}/deep_research/BIG_PICTURE_LEARNINGS.md.\n\n` +
  `WRITE one file: ${ROOT}/runs/round3_report.md, containing:\n` +
  `  1. Executive summary: did the wider net find anything genuinely new and DEFENSIBLE that beats what we already have? ` +
  `Be honest — if the best round-3 idea still doesn't clear CutLog (8.85) or even the #2 (Compressed Air 7.65 / Fire ` +
  `Sprinkler 6.70), say so.\n` +
  `  2. A ranked table of ALL round-3 graduates across the 10 new domains (name, domain, one-line, competitive density, ` +
  `MOAT answer, CAGR/SAM, capital, founder-fit, feasibility). Sort by how promising+defensible they are.\n` +
  `  3. Domain heat-map: which of the 10 new domains are promising new veins vs dead ends for this founder, and why.\n` +
  `  4. Top 3-5 candidates that WARRANT deep research (Step 6) — only ones with a real moat answer. If none qualify, ` +
  `say that plainly.\n` +
  `  5. New patterns/learnings from casting the wider net (append-worthy to LEARNINGS.md — list them).\n\n` +
  `Be concrete, quantified, skeptical. Return a ~350-word executive summary as your final text (relayed to Hooman): ` +
  `lead with whether the wider net paid off, name the best new idea(s) and their moat, and give a clear recommendation on ` +
  `whether to deep-research any of them or run more cycles.`,
  { label: 'round3-synthesis', phase: 'Synthesize', agentType: 'general-purpose' }
)

return {
  cycles_ran: cycles.length,
  total_graduates: allGrads.length,
  graduates: allGrads.map(g => ({ name: g.name, cycle: g.cycle, density: g.competitive_density, fit: g.founder_fit, feasibility: g.feasibility_score, moat: g.moat_answer })),
  synthesis_summary: synthesis,
}
