export const meta = {
  name: 'flat-showdown-no-sunk-cost',
  description: 'Adversarially stress-test CutLog + fab-shop platform with the same rigor used on Track-B, then rank ALL serious secondary-income candidates flat with zero sunk-cost weighting',
  phases: [
    { title: 'StressTest', detail: 'red-team CutLog and the fab-shop/Plasma platform with equal skepticism' },
    { title: 'Showdown', detail: 'flat head-to-head across all serious candidates; no protected incumbent' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'

// The two things that were NEVER adversarially validated (got the optimistic 8.85 methodology).
const STRESS = [
  { slug: 'cutlog', name: 'CutLog — Laser Cutting Parameter Optimization SaaS (live, in flight)',
    read: `${ROOT}/deep_research/MASTER_COMPARISON_V2.md (its row/§ on laser cutting) and any laser_cutting notes; plus the global memory project_cutlog context. Original score 8.85 via the OPTIMISTIC methodology — never red-teamed.`,
    claims: 'Pure SW, ~$700 to validate, zero competition, community-data network-effect moat, 200K+ machines, 8-16 weeks to revenue, best founder fit. VALIDATE SKEPTICALLY: is the network effect real or aspirational (cold-start: why do the first shops contribute parameters)? Is competition truly zero (check LightBurn libraries, OEM parameter DBs, Facebook groups already sharing free, MachineMetrics, existing cut-setting charts)? Is willingness-to-pay real, or do shops treat parameters as free tribal knowledge? What is the HONEST revenue ramp and monthly profit?' },
  { slug: 'fabshop_platform', name: 'Fab-shop platform (CutLog + Springback + Plasma Consumable Life)',
    read: `${ROOT}/deep_research/MASTER_COMPARISON_V2.md §3 (three-lens rec, Plasma 5.95 cond-go, Springback NO-GO) and ${ROOT}/deep_research/plasma_consumable_life/combined_research.md and springback_ai/combined_research.md.`,
    claims: 'Same fab-shop buyer/channel/stack; CutLog as wedge, free Springback calculator to test cross-sell, Plasma as first paid 2nd product. VALIDATE SKEPTICALLY: Plasma arc-voltage signal is masked by torch-height-control and Hypertherm SYNC already tracks consumable usage — does the ML actually beat a free pierce counter? Springback was already NO-GO (OEM closed-loop). Is there real cross-sell evidence, or is "platform" a story? Honest combined monthly profit + time load.' },
]

const STRESS_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['name','slug','assumptions_checked','competitors','honest_economics','hrs_per_week','kill_risks','revised_score','verdict','confidence'],
  properties: {
    name: { type: 'string' }, slug: { type: 'string' },
    assumptions_checked: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['claim','status','evidence'],
      properties: { claim: { type: 'string' }, status: { type: 'string', enum: ['VERIFIED','PARTIALLY-TRUE','FALSE','UNVERIFIED'] }, evidence: { type: 'string' } } } },
    competitors: { type: 'array', items: { type: 'string' } },
    honest_economics: { type: 'string', description: 'realistic monthly profit + ramp AFTER red-teaming, vs the original claim' },
    hrs_per_week: { type: 'string', description: 'realistic sustained founder time load' },
    kill_risks: { type: 'array', items: { type: 'string' } },
    revised_score: { type: 'number', description: 'honest /10 after red-team, comparable to the Track-B validated scores (NOT the original optimistic 8.85)' },
    verdict: { type: 'string', enum: ['PURSUE','CONDITIONAL','PASS'] },
    confidence: { type: 'string', enum: ['HIGH','MEDIUM','LOW'] },
  },
}

phase('StressTest')

const stressed = await parallel(STRESS.map(s => () =>
  agent(
    `You are an ADVERSARIAL RED-TEAM. Founder: Hooman (Adobe eng manager; AI/ML+cloud+infra; EE; mech-eng friends; ` +
    `$25-150K capital; ~10-20 hrs/wk; wants a secondary income / $5-30K/mo). CRITICAL FRAMING: Hooman has said he is ` +
    `NOT attached to CutLog and will abandon it if something is better. So CutLog gets ZERO benefit of the doubt — ` +
    `treat it as harshly as any new idea. Its original 8.85 score came from an OPTIMISTIC methodology and was NEVER ` +
    `red-teamed; your job is to fix that.\n\n` +
    `TARGET: "${s.name}"\nREAD FIRST: ${s.read}\nCLAIMS TO VALIDATE SKEPTICALLY: ${s.claims}\n\n` +
    `Do REAL WEB RESEARCH (WebSearch/WebFetch). Be a skeptic exactly as the Track-B deep dive was ` +
    `(see ${ROOT}/runs/trackB/DEEP_DIVE_SYNTHESIS.md for the standard of rigor and the kinds of optimism to catch: ` +
    `gross-read-as-profit, top-decile-as-base-case, false "no competition", inverted founder-fit, "passive" that isn't).\n` +
    `  1. Mark every claim VERIFIED / PARTIALLY-TRUE / FALSE / UNVERIFIED with sourced evidence. Hammer the moat and ` +
    `the "zero competition" claim especially (free parameter sources, OEM/community sharing, cold-start problem).\n` +
    `  2. Find real competitors/substitutes (including FREE ones — free tribal knowledge is a competitor).\n` +
    `  3. Re-derive HONEST monthly profit + ramp + weekly time load.\n` +
    `  4. Give a revised /10 score on the SAME harsh scale as the Track-B validated scores (buy-SaaS ~ low, etc.), ` +
    `a verdict, and confidence.\n\n` +
    `WRITE to ${ROOT}/runs/trackB/deep/${s.slug}_stresstest.md (use Write; cite sources). THEN return the schema.`,
    { label: `stress:${s.slug}`, phase: 'StressTest', schema: STRESS_SCHEMA, agentType: 'general-purpose' }
  )
))

const stressJson = JSON.stringify(stressed.filter(Boolean), null, 2)
log(`Stress-test complete for ${stressed.filter(Boolean).length}/2 incumbents.`)

phase('Showdown')

const synthesis = await agent(
  `You are producing a FLAT, ZERO-SUNK-COST head-to-head for Hooman across ALL of his serious secondary-income ` +
  `candidates. He explicitly said: "You're overindexing on CutLog. I don't mind abandoning CutLog if there is ` +
  `something better." So CutLog is just one candidate for his single serious-venture slot — NOT a protected baseline, ` +
  `and "it would distract from CutLog" is NOT a valid mark against other ideas (CutLog itself must earn the slot).\n\n` +
  `Founder: Adobe eng manager; AI/ML+cloud+infra; EE; mech-eng friends; $25-150K; ~10-20 hrs/wk; wants $5-30K/mo ` +
  `secondary income; AI-safe preferred; open to ANY business shape and to abandoning CutLog.\n\n` +
  `The two never-before-red-teamed incumbents were just stress-tested (JSON):\n${stressJson}\n\n` +
  `Now assemble the full field. READ these for the other candidates' validated numbers:\n` +
  `  - ${ROOT}/runs/trackB/DEEP_DIVE_SYNTHESIS.md (the 5 Track-B ideas, honestly revalidated)\n` +
  `  - ${ROOT}/deep_research/MASTER_COMPARISON_V2.md (Track-A: Fire Sprinkler 6.70, Compressed Air 7.65, Plasma, etc.\n` +
  `    — NOTE these Track-A scores are still OPTIMISTIC/un-red-teamed; discount them accordingly for comparability, ` +
  `    the same way CutLog just got discounted).\n\n` +
  `WRITE ${ROOT}/runs/FLAT_SHOWDOWN.md with:\n` +
  `  1. A single ranked table of ALL serious candidates on a COMPARABLE honest basis: CutLog (stress-tested), ` +
  `fab-shop/Plasma platform (stress-tested), the 5 Track-B ideas (validated), and the best Track-A #2s (Fire ` +
  `Sprinkler, Compressed Air — flagged as still-optimistic). Columns: candidate | honest monthly profit | capital | ` +
  `hrs/wk | shape | honest score /10 | verdict | key reason.\n` +
  `  2. The CutLog reckoning: how does CutLog look once red-teamed on the same scale as everything else? Did it earn ` +
  `the #1 slot on merit, or was it only #1 because it was never scrutinized + was treated as the baseline?\n` +
  `  3. A clear recommendation: what is the single best use of his one venture slot, CutLog included or not? If the ` +
  `honest answer is "CutLog is still best," say why on merit. If something beats it, name it and say what abandoning ` +
  `CutLog would cost/save.\n` +
  `  4. Note remaining validation gaps (e.g. Track-A ideas not yet red-teamed) and what to check before a final call.\n\n` +
  `Be brutally honest and quantified; no incumbent protection, no sunk-cost. Return a ~400-word executive summary as ` +
  `your final text (relayed to Hooman).`,
  { label: 'flat-showdown', phase: 'Showdown', agentType: 'general-purpose' }
)

return { stress_tested: stressed.filter(Boolean).map(s => ({ name: s.name, revised_score: s.revised_score, verdict: s.verdict, economics: s.honest_economics })), synthesis_summary: synthesis }
