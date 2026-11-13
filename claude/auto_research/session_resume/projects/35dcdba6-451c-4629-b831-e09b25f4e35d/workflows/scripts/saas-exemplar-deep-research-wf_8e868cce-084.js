export const meta = {
  name: 'saas-exemplar-deep-research',
  description: 'Find REAL current EH&S/SDS compliance SaaS and email-service-provider SaaS acquisition listings with verified numbers; validate whether the $325K/$345K exemplars are real buyable options',
  phases: [
    { title: 'Hunt', detail: 'per segment: find actual current listings on the marketplaces with real financials + competitor/market context' },
    { title: 'Synthesize', detail: 'are these real options? shortlist real deals, deal-killers, next steps' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'
const OUT = `${ROOT}/acquisitions_500k/saas_deepdive`

const SEGMENTS = [
  { slug: 'ehs_sds_compliance',
    name: 'EH&S / SDS chemical-safety compliance SaaS',
    exemplar: 'Wide-search exemplar: $325K ask / ~$110K SDE / ~3x. What it does: SDS (Safety Data Sheet) library management, chemical inventory tracking, OSHA HazCom (29 CFR 1910.1200) / WHMIS / GHS right-to-know compliance, secondary-container labels, Tier II reporting, audit trails. Buyers: EH&S/safety managers at manufacturers, labs, hospitals, universities, warehouses. Mandate-driven sticky demand; system-of-record.',
    hunt: 'Find REAL current listings of EH&S/SDS/chemical-safety/environmental-compliance SaaS for sale. Search Acquire.com, Flippa, Empire Flippers, FE International, MicroAcquire, BizBuySell, Quiet Light, brokers. ALSO map the competitive landscape (VelocityEHS/MSDSonline, SafeTec, Chemwatch, Sitehawk/VelocityEHS, KHA/365, Cority, Benchmark Gensuite, EHS Insight, Donesafe) to judge whether a small $300-400K acquirable player can survive under the incumbents.' },
  { slug: 'email_service_provider',
    name: 'Email-service-provider / email-infrastructure SaaS',
    exemplar: 'Wide-search exemplar: $345K ask / ~$116K SDE / 425 diversified customers / 17-yr history. An email sending/marketing/deliverability/transactional-email SaaS with long track record and diversified B2B customer base. Thesis: highest cash yield, Hooman can modernize the stack, cut infra cost, add AI, re-accelerate. Runs ~part-time.',
    hunt: 'Find REAL current listings of email-service-provider / email-marketing / transactional-email / newsletter-infra / deliverability SaaS for sale (esp. 5+ yr history, diversified customers, ~$300-400K range). Search Acquire.com, Flippa, Empire Flippers, FE International, MicroAcquire, brokers. ALSO map competition (Mailchimp, Sendgrid/Twilio, Postmark, Mailgun, Brevo, ConvertKit/Kit, Beehiiv, Amazon SES, Klaviyo) and judge whether a small legacy ESP can defend a niche vs commoditized sending + free tiers, and whether deliverability/reputation risk makes it fragile.' },
]

const SEG_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['segment','exemplar_is_real','listings','competitive_reality','verdict','confidence','access_caveats'],
  properties: {
    segment: { type: 'string' },
    exemplar_is_real: { type: 'string', enum: ['MATCHING-LISTINGS-FOUND','SIMILAR-FOUND','NONE-FOUND'], description: 'did the ~$325-345K exemplar correspond to anything actually listed?' },
    listings: {
      type: 'array', description: 'REAL current listings found (do NOT invent; mark gated fields "gated")',
      items: {
        type: 'object', additionalProperties: false,
        required: ['name','marketplace','url_or_id','asking_price','revenue_mrr','sde_profit','multiple','age','customers','tech','fit_reason','deal_killers','data_gaps'],
        properties: {
          name: { type: 'string' },
          marketplace: { type: 'string' },
          url_or_id: { type: 'string' },
          asking_price: { type: 'string' },
          revenue_mrr: { type: 'string' },
          sde_profit: { type: 'string' },
          multiple: { type: 'string' },
          age: { type: 'string' },
          customers: { type: 'string' },
          tech: { type: 'string' },
          fit_reason: { type: 'string', description: 'fit vs the exemplar thesis + Hooman (AI/data/infra edge, remote, mandate-driven)' },
          deal_killers: { type: 'string' },
          data_gaps: { type: 'string', description: 'what needs a buyer account/NDA to verify' },
        },
      },
    },
    competitive_reality: { type: 'string', description: 'can a small $300-400K player survive under the named incumbents? honest.' },
    verdict: { type: 'string', enum: ['REAL-BUYABLE-OPTIONS','THIN-BUT-POSSIBLE','NOT-REALLY-AVAILABLE'] },
    confidence: { type: 'string', enum: ['HIGH','MEDIUM','LOW'] },
    access_caveats: { type: 'string', description: 'what was gated/bot-blocked; where a manual account pass is needed' },
  },
}

phase('Hunt')

const results = await parallel(SEGMENTS.map(s => () =>
  agent(
    `You are hunting REAL, CURRENT acquisition listings in a specific SaaS segment for Hooman (Adobe eng manager; ` +
    `AI/ML + data engineering + cloud/infra; EE; up to ~$500K; wants a cash-flowing business; strong diligence). ` +
    `These were flagged as the two SaaS options he likes best from the $500K wide search — but they were CATEGORY ` +
    `EXEMPLARS, not verified listings. Your job: find out if they are REAL, BUYABLE options right now.\n\n` +
    `SEGMENT: ${s.name}\nEXEMPLAR CLAIMED: ${s.exemplar}\nHOW TO HUNT: ${s.hunt}\n\n` +
    `Read ${ROOT}/acquisitions_500k/WIDE_SEARCH_REPORT.md (where these were surfaced) and ` +
    `${ROOT}/runs/buy_microsaas_PLAYBOOK.md (Buy Box, 8 deal-killers, delegation math) first.\n\n` +
    `Do REAL WEB RESEARCH (WebSearch/WebFetch the marketplaces + broker sites + the incumbents' sites). Capture ACTUAL ` +
    `current listings with real numbers (asking, MRR/revenue, SDE/profit, multiple, age, customer count, tech stack). ` +
    `Do NOT invent listings — if you can only find the category and no live deal, say so honestly (exemplar_is_real = ` +
    `NONE-FOUND or SIMILAR-FOUND). Note what is gated behind a buyer account. ALSO assess the competitive reality: ` +
    `given the named incumbents, can a small $300-400K player actually survive and be worth buying?\n\n` +
    `WRITE your findings to ${OUT}/${s.slug}.md (use Write; create folders; include URLs/listing IDs; cite sources). ` +
    `THEN return the structured schema with an honest verdict on whether this is a REAL buyable option.`,
    { label: `hunt:${s.slug}`, phase: 'Hunt', schema: SEG_SCHEMA, agentType: 'general-purpose' }
  ).then(r => r ? { ...r, slug: s.slug } : null)
))

const found = results.filter(Boolean)
const allListings = found.flatMap(r => (r.listings||[]).map(l => ({...l, segment: r.segment})));
log(`SaaS hunt done: ${found.length}/2 segments, ${allListings.length} real listings captured.`)

phase('Synthesize')

const digest = JSON.stringify(found.map(r => ({
  segment: r.segment, exemplar_is_real: r.exemplar_is_real, verdict: r.verdict, confidence: r.confidence,
  competitive_reality: r.competitive_reality, access_caveats: r.access_caveats, listings: r.listings,
})), null, 2)

const synthesis = await agent(
  `Synthesize a straight answer for Hooman: are the two SaaS options he likes best — (1) EH&S/SDS compliance SaaS and ` +
  `(2) email-service-provider SaaS, both ~$325-345K / ~$110-116K SDE / ~3x — REAL, buyable options, or were they just ` +
  `category exemplars with no live deal behind them? He is an Adobe AI/ML+data+infra engineer, up to ~$500K, values ` +
  `his technical edge as value-creation, wants remote-operable + durable + mandate-driven.\n\n` +
  `Hunt results (JSON):\n${digest}\n\n` +
  `Read ${ROOT}/acquisitions_500k/WIDE_SEARCH_REPORT.md for context.\n\n` +
  `WRITE ${OUT}/SAAS_DEEPDIVE_REPORT.md with:\n` +
  `  1. Direct answer per segment: real buyable options today? (with the actual listings + real numbers found).\n` +
  `  2. A table of all real listings found (name, marketplace, asking, MRR, SDE, multiple, age, customers, fit, ` +
  `deal-killers).\n` +
  `  3. Competitive reality for each: can a small $300-400K player survive under the incumbents (VelocityEHS etc. / ` +
  `Mailchimp/Sendgrid etc.)? Which of the two segments is the more defensible buy for him?\n` +
  `  4. For the best 1-3 real listings: the specific things to source-verify + the Gate-2 next click.\n` +
  `  5. Honest bottom line: do these live up to the exemplar thesis, and which (if either) is worth pursuing? Note ` +
  `access caveats (bot-blocked marketplaces needing a manual account pass).\n\n` +
  `Be concrete, quantified, skeptical; do not inflate. Return a ~400-word executive summary as your final text ` +
  `(relayed to Hooman): whether each is real, the best actual listings + numbers, competitive verdict, and the ` +
  `recommended next step.`,
  { label: 'saas-synthesis', phase: 'Synthesize', agentType: 'general-purpose' }
)

return {
  segments: found.map(r => ({ segment: r.segment, exemplar_is_real: r.exemplar_is_real, verdict: r.verdict, listings_found: (r.listings||[]).length })),
  total_listings: allListings.length,
  synthesis_summary: synthesis,
}
