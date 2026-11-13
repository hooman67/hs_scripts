export const meta = {
  name: 'good-shape-listings-300k',
  description: 'Deep-research the two "good shape" listings (building-ops platform, Amazon-sourcing data-moat SaaS) under the raised $300K ceiling; reassess fit',
  phases: [
    { title: 'DeepDive', detail: 'one agent per listing: full profile, numbers, moat, risks, delegation math at $300K' },
    { title: 'Reassess', detail: 'update Buy Box to $300K; verdict on each + what else the higher ceiling unlocks' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'

const LISTINGS = [
  { slug: 'building_ops', name: 'High-Yield Building Ops Platform (Acquire.com)',
    facts: 'Acquire.com listing. Facilities / building-operations vertical SaaS. ~$438K ARR, ~$399K SDE (~91% margin), implied asking ~$1.6-1.8M at ~4-4.5x SDE, growing. Flagged in LIVE_LISTINGS as "what good looks like" but far over the old $150K ceiling. NOW ceiling is $300K — so this is STILL ~5-6x over budget unless heavily seller-financed. Investigate: exact price, is any seller-financing/earnout structure conceivable, what the business actually does, moat, customer concentration, owner hours, why the 91% margin, growth trend, and whether a partial/minority or SBA-leveraged path exists (note SBA = personal guarantee risk).' },
  { slug: 'amazon_sourcing', name: 'European Amazon-seller sourcing SaaS (Empire Flippers #91852)',
    facts: 'Empire Flippers listing #91852. Ecommerce sourcing intelligence: 800+ EU suppliers, 80M+ products (a DATA MOAT). ~$24,942/mo revenue, ~$7,716/mo net (~31% margin), asking ~$192,896 (~25x monthly / ~2.1x annual). ~6 yr old. Flagged PARTIAL: over the OLD band, Amazon-platform-dependent, ~40 hr/wk owner load. NOW ceiling is $300K so PRICE fits. Investigate: what exactly the data moat is and how defensible, Amazon-dependency risk (ToS/API), the 40hr/wk load (can it be cut/delegated?), why only 31% margin, churn/concentration, and whether Hooman (AI/data eng) could automate the ops that consume 40 hr/wk.' },
]

const DD_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['name','slug','what_it_does','numbers','moat','key_risks','delegation_verdict','fits_300k','honest_verdict','confidence','verify_first'],
  properties: {
    name: { type: 'string' }, slug: { type: 'string' },
    what_it_does: { type: 'string' },
    numbers: { type: 'string', description: 'price, rev, SDE/net, margin, multiple, age, customers, growth — with what is public vs gated' },
    moat: { type: 'string' },
    key_risks: { type: 'array', items: { type: 'string' } },
    delegation_verdict: { type: 'string', description: 'at this net, can it be run part-time / delegated, or is Hooman the operator? does his AI/data-eng skill cut the owner hours?' },
    fits_300k: { type: 'string', enum: ['FITS','FITS-WITH-FINANCING','OVER-CEILING'] },
    honest_verdict: { type: 'string', enum: ['PURSUE','CONDITIONAL','PASS'] },
    confidence: { type: 'string', enum: ['HIGH','MEDIUM','LOW'] },
    verify_first: { type: 'array', items: { type: 'string' }, description: 'the specific things to source-verify before an offer' },
  },
}

phase('DeepDive')

const dives = await parallel(LISTINGS.map(l => () =>
  agent(
    `You are deep-researching a SPECIFIC micro-SaaS acquisition listing for Hooman (Adobe eng manager; AI/ML+data+cloud+infra; ` +
    `EE; ~10-20 hrs/wk; wants $5-30K/mo secondary income). IMPORTANT: his capital ceiling was just RAISED to $300K (from ` +
    `$150K). He wants to know more about this "genuinely good shape" listing that was previously over budget.\n\n` +
    `LISTING: "${l.name}"\nKNOWN FACTS: ${l.facts}\n\n` +
    `Read ${ROOT}/runs/buy_microsaas_LIVE_LISTINGS.md (where this was flagged) and ${ROOT}/runs/buy_microsaas_PLAYBOOK.md ` +
    `(Buy Box, 8 deal-killers, delegation-trap math: delegation only pencils above ~$4K/mo net).\n\n` +
    `Do REAL WEB RESEARCH (WebFetch the listing pages on acquire.com / empireflippers.com marketplace and any public ` +
    `cache; WebSearch the niche + named competitors). Produce a full profile: what it does, the real numbers (public vs ` +
    `gated), the moat and how defensible it is, customer concentration / churn / owner-hours, growth trend, and the ` +
    `named competitors. Then assess: (1) does it fit the NEW $300K ceiling (outright / only-with-seller-financing / ` +
    `over)? (2) the delegation verdict at its net profit — and crucially, can HOOMAN's AI/data-engineering skills cut ` +
    `the owner-hours (e.g. automate the 40hr/wk sourcing ops) enough to make it part-time? (3) honest verdict PURSUE/ ` +
    `CONDITIONAL/PASS with the deal-killers to verify first.\n\n` +
    `WRITE to ${ROOT}/runs/buysaas_listings/deepdive_${l.slug}.md (use Write; cite sources). THEN return the schema.`,
    { label: `dd:${l.slug}`, phase: 'DeepDive', schema: DD_SCHEMA, agentType: 'general-purpose' }
  )
))

const found = dives.filter(Boolean)
log(`Deep-dive done on ${found.length}/2 listings.`)

phase('Reassess')

const synthesis = await agent(
  `Update the buy-a-micro-SaaS picture for Hooman now that his capital ceiling is RAISED to $300K (was $150K) and two ` +
  `"good shape" listings have been deep-researched. Founder: Adobe eng manager; AI/ML+data+cloud+infra; EE; ~10-20 hrs/wk; ` +
  `wants $5-30K/mo. Deep-dive results (JSON):\n${JSON.stringify(found, null, 2)}\n\n` +
  `Read ${ROOT}/runs/buy_microsaas_LIVE_LISTINGS.md and ${ROOT}/runs/buy_microsaas_PLAYBOOK.md.\n\n` +
  `WRITE ${ROOT}/runs/buy_microsaas_300K_UPDATE.md with:\n` +
  `  1. A crisp profile + verdict for EACH of the two listings (building-ops, Amazon-sourcing) at the $300K ceiling — ` +
  `does it now fit, what are the real numbers, the moat, the delegation verdict (can Hooman's data/AI skills cut the ` +
  `owner hours?), and the deal-killers to verify.\n` +
  `  2. What the higher $300K ceiling UNLOCKS in general: the revised Buy Box (net-profit band, price band, the fact ` +
  `that ~$4-6K/mo net assets now come into range — which is exactly the level where DELEGATION finally pencils, ` +
  `changing the "Hooman is always the operator" conclusion). Quantify: at $300K and 4-4.5x, what monthly net can he buy, ` +
  `and does that clear the delegation threshold?\n` +
  `  3. Whether raising to $300K changes the bottom line: is buy-SaaS now a real path to $5-30K/mo (or at least to a ` +
  `delegable ~$4-6K/mo), or still not? Honest.\n\n` +
  `Be concrete and quantified. Return a ~400-word executive summary as your final text (relayed to Hooman): the two ` +
  `listings' verdicts, what $300K unlocks (esp. the delegation threshold), and the bottom-line recommendation.`,
  { label: 'reassess-300k', phase: 'Reassess', agentType: 'general-purpose' }
)

return { deep_dived: found.map(d => ({ name: d.name, fits_300k: d.fits_300k, verdict: d.honest_verdict, delegation: d.delegation_verdict })), synthesis_summary: synthesis }
