export const meta = {
  name: 'buysaas-live-listings',
  description: 'Find ACTUAL current micro-SaaS listings across marketplaces, screen against the Buy Box, pick 2-3 dry-run candidates with a delegation-trap verdict each',
  phases: [
    { title: 'Scan', detail: 'one agent per marketplace: pull real current listings with their numbers' },
    { title: 'Synthesize', detail: 'screen against Buy Box, pick 2-3 dry-run candidates + delegation-trap verdicts' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'

// Buy Box (from the playbook) the scanners screen against.
const BUYBOX = `Vertical B2B system-of-record / compliance / workflow SaaS in an unglamorous trade. ` +
  `Price $75-160K (sweet spot $80-120K). Net profit $2-5K/mo (realistic buys ~$1.5-2.5K/mo). ` +
  `>=18-24mo history. B2B recurring. Churn curve flattens. <20% customer concentration. Owner <10 hrs/wk. ` +
  `AI-safe: REJECT consumer apps, SEO/content sites, Chrome extensions, thin AI wrappers, single-platform ` +
  `(Shopify/WP/Stripe) add-ons the host can kill.`

const MARKETS = [
  { key: 'acquire',  name: 'Acquire.com', url: 'https://acquire.com/', note: 'highest volume in the $2-8K MRR SaaS band; some data gated behind free buyer account' },
  { key: 'flippa',   name: 'Flippa', url: 'https://flippa.com/buy/monetization/saas', note: 'most volume + most junk; exposes MRR/churn/age filters publicly' },
  { key: 'empireflippers', name: 'Empire Flippers', url: 'https://empireflippers.com/marketplace/', note: 'most vetted, priced higher; public listing cards show niche/monthly-profit/multiple' },
  { key: 'microns',  name: 'Microns.io', url: 'https://microns.io/', note: 'curated micro-SaaS, often on-budget' },
  { key: 'tiny_latonas', name: 'Tiny Acquisitions + Latona\'s + MotionInvest', url: 'https://tinyacq.com/', note: 'smaller/cheaper micro-SaaS and a few vetted SaaS' },
]

const LISTING_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['marketplace','access_notes','listings'],
  properties: {
    marketplace: { type: 'string' },
    access_notes: { type: 'string', description: 'what was publicly visible vs gated behind login/verification' },
    listings: {
      type: 'array', description: 'real current listings found (best-fit first); capture what is public',
      items: {
        type: 'object', additionalProperties: false,
        required: ['name_or_title','niche','asking_price','revenue_or_mrr','profit_or_sde','multiple','age','tech','buybox_fit','fit_reason','data_gaps'],
        properties: {
          name_or_title: { type: 'string', description: 'listing title/handle (often anonymized on these sites)' },
          niche: { type: 'string' },
          asking_price: { type: 'string' },
          revenue_or_mrr: { type: 'string' },
          profit_or_sde: { type: 'string' },
          multiple: { type: 'string', description: 'x monthly profit or x annual SDE if shown/derivable' },
          age: { type: 'string' },
          tech: { type: 'string', description: 'stack / platform if shown' },
          buybox_fit: { type: 'string', enum: ['STRONG','PARTIAL','WEAK','REJECT'] },
          fit_reason: { type: 'string', description: 'why it fits or fails the Buy Box (esp. AI-safe + B2B-sticky + concentration)' },
          data_gaps: { type: 'string', description: 'what must be verified with a buyer account (exact rev, churn, concentration)' },
        },
      },
    },
  },
}

phase('Scan')

const scans = await parallel(MARKETS.map(m => () =>
  agent(
    `You are sourcing ACTUAL current micro-SaaS acquisition listings for Hooman (Adobe eng manager; $25-150K ` +
    `capital; ~10-20 hrs/wk; wants a secondary income). He wants to see REAL options, not abstractions.\n\n` +
    `MARKETPLACE: ${m.name} (${m.url}). Note: ${m.note}.\n\n` +
    `Read the Buy Box first: ${BUYBOX}\nFor full context, the playbook is at ${ROOT}/runs/buy_microsaas_PLAYBOOK.md.\n\n` +
    `Use WebFetch/WebSearch to browse this marketplace's SaaS listings (try the marketplace URL, its SaaS/B2B ` +
    `category pages, and Google queries like "site:${m.url.replace('https://','').replace('/','')} SaaS" or ` +
    `"${m.name} B2B SaaS for sale $100k"). Pull the ACTUAL listings currently visible — real titles, niches, asking ` +
    `prices, MRR/revenue, profit/SDE, multiples, age, tech stack. Prioritize ones near the Buy Box ($75-160K, B2B, ` +
    `recurring, boring vertical, AI-safe). Capture 5-12 real listings; for EACH, score buybox_fit and note exactly ` +
    `what data is gated behind a buyer account.\n\n` +
    `Be HONEST about access limits: if listings/prices are behind login, say so and capture whatever the public ` +
    `listing cards / category pages / Google cache DO show (many show niche + monthly profit + multiple + price ` +
    `publicly). Do NOT invent listings — only report what you actually find; if a field isn't visible, say "gated".\n\n` +
    `WRITE your findings to ${ROOT}/runs/buysaas_listings/${m.key}.md (use Write; create folders; include listing ` +
    `URLs where public). THEN return the structured schema.`,
    { label: `scan:${m.key}`, phase: 'Scan', schema: LISTING_SCHEMA, agentType: 'general-purpose' }
  ).then(r => r ? { ...r, key: m.key } : null)
))

const found = scans.filter(Boolean)
const allListings = found.flatMap(s => (s.listings || []).map(l => ({ ...l, marketplace: s.marketplace })))
log(`Marketplace scan done: ${found.length}/${MARKETS.length} sites, ${allListings.length} real listings captured.`)

phase('Synthesize')

const digest = JSON.stringify({
  by_market: found.map(s => ({ marketplace: s.marketplace, access_notes: s.access_notes, listing_count: (s.listings||[]).length })),
  listings: allListings,
}, null, 2)

const synthesis = await agent(
  `You are producing a shortlist of ACTUAL micro-SaaS listings for Hooman to dry-run (Adobe eng manager; $25-150K; ` +
  `~10-20 hrs/wk; wants secondary income). He explicitly wants to SEE real current options and pick 2-3 to diligence.\n\n` +
  `Here are the real listings captured across marketplaces (JSON):\n${digest}\n\n` +
  `Read ${ROOT}/runs/buy_microsaas_PLAYBOOK.md for the Buy Box, the 8 deal-killers, and the delegation-trap math ` +
  `(delegation only pencils above ~$4K/mo net; below that Hooman IS the operator; affordable asset ~$1.5-2.5K/mo net).\n\n` +
  `WRITE ${ROOT}/runs/buy_microsaas_LIVE_LISTINGS.md with:\n` +
  `  1. A table of ALL real listings found (marketplace, niche, asking, MRR/profit, multiple, age, Buy-Box fit).\n` +
  `  2. The TOP 2-3 dry-run candidates, each with: why it fits the Buy Box, the specific data to source-verify ` +
  `first, the likely price-vs-net math, and a DELEGATION-TRAP VERDICT (at its profit level, can it be run <10 hrs/wk ` +
  `without a VA+dev spend that eats the profit — or is Hooman the operator?).\n` +
  `  3. Honest access caveats: what needs a (free) buyer account to confirm, and the exact next click for each ` +
  `candidate.\n` +
  `  4. A realistic read on supply: are Buy-Box-fitting deals actually available right now, or is the clean-deal ` +
  `scarcity (crowded buy-side, 4-4.5x for non-declining) the binding constraint? If almost nothing fits, SAY SO — ` +
  `that itself is the dry-run answer ("keep the capital").\n\n` +
  `Be concrete and honest; do not inflate fit or invent numbers. Return a ~350-word executive summary as your final ` +
  `text: name the 2-3 real candidates (or report that nothing clean is currently listed), their numbers, the ` +
  `delegation verdict, and the concrete next step.`,
  { label: 'listings-synthesis', phase: 'Synthesize', agentType: 'general-purpose' }
)

return {
  markets_scanned: found.length,
  total_listings: allListings.length,
  strong_or_partial: allListings.filter(l => l.buybox_fit === 'STRONG' || l.buybox_fit === 'PARTIAL').map(l => ({ niche: l.niche, price: l.asking_price, profit: l.profit_or_sde, fit: l.buybox_fit, marketplace: l.marketplace })),
  synthesis_summary: synthesis,
}
