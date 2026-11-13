export const meta = {
  name: 'acquisitions-canada-search',
  description: 'Parallel Canadian (ON/BC) acquisition search up to ~$500K CAD; real deals per category + BDC/CSBFP financing + remote-operability-from-US flags, then a head-to-head',
  phases: [
    { title: 'Categories', detail: 'one agent per business category: real current Canadian listings, economics, Canadian financing, remote-operability' },
    { title: 'Synthesize', detail: 'head-to-head; best Canadian deals + how CA financing/immigration changes the picture vs the US search' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'
const OUT = `${ROOT}/acquisitions_canada`

const CATEGORIES = [
  { key: 'saas_software', name: 'SaaS / software / apps (Canadian-domiciled)',
    detail: 'Canadian-based vertical B2B SaaS, micro-SaaS, software/data products up to ~$500K CAD. Naturally remote-operable. Acquire.com/Flippa/EmpireFlippers (filter Canada), plus Canadian brokers.' },
  { key: 'ecommerce_brands', name: 'E-commerce / DTC brands (Canadian)',
    detail: 'Canadian DTC/e-commerce brands with a moat (brand/IP/repeat), not commodity dropshipping. Often remote-runnable. businessesforsale.com/canada, Flippa, Canadian brokers.' },
  { key: 'content_media', name: 'Content / media / newsletters / communities (Canadian)',
    detail: 'Canadian content/media/community assets with durable first-party audiences. Remote-runnable. Note AI-Overview/SEO risk.' },
  { key: 'local_service', name: 'Local service businesses (ON/BC home & trades)',
    detail: 'ON/BC home services & trades: HVAC, plumbing, electrical, landscaping, cleaning, pest, pool, restoration, junk removal. Recurring/route preferred. NOTE trade-licensing rules differ by province. Requires on-the-ground presence — flag this. Sunbelt Canada, businessesforsale.com/canada, BizBuySell Canada.' },
  { key: 'physical_asset', name: 'Physical / real-asset businesses (ON/BC, semi-absentee)',
    detail: 'ON/BC laundromats, self-storage, car washes, vending routes. Asset-backed, financeable via BDC/bank, manager/attendant-run. Some semi-absentee. Sunbelt Canada, Canadian brokers.' },
  { key: 'b2b_distribution', name: 'B2B distribution / niche manufacturing / light industrial (ON/BC)',
    detail: 'ON/BC small manufacturers, specialty distributors, B2B/commercial services. Real cash flow, seller financing + BDC common. Sunbelt Canada, businessesforsale.com/canada.' },
]

const CAT_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['category','deals','category_economics','financing_notes','remote_operability','hooman_fit','category_verdict'],
  properties: {
    category: { type: 'string' },
    deals: {
      type: 'array', description: 'REAL current Canadian listings (do not invent); best-fit first',
      items: {
        type: 'object', additionalProperties: false,
        required: ['name','niche_location','asking_price','revenue','sde_cashflow','multiple','age','why_notable','risks','remote_runnable','fits_500k_cad'],
        properties: {
          name: { type: 'string' },
          niche_location: { type: 'string', description: 'niche + province/city' },
          asking_price: { type: 'string', description: 'CAD (note if USD)' },
          revenue: { type: 'string' },
          sde_cashflow: { type: 'string' },
          multiple: { type: 'string' },
          age: { type: 'string' },
          why_notable: { type: 'string' },
          risks: { type: 'string' },
          remote_runnable: { type: 'string', enum: ['REMOTE','SEMI-ABSENTEE','ON-SITE-REQUIRED'] },
          fits_500k_cad: { type: 'string', enum: ['FITS-ALL-CASH','FITS-WITH-FINANCING','OVER-500K'] },
        },
      },
    },
    category_economics: { type: 'string', description: 'typical Canadian SDE multiples, cash yields, owner-hours in this category' },
    financing_notes: { type: 'string', description: 'BDC / CSBFP / Canadian bank acquisition-financing feasibility for this category; typical down %; seller-note norms' },
    remote_operability: { type: 'string', description: 'can these be run remotely from the US (until/unless he relocates to Canada)?' },
    hooman_fit: { type: 'string' },
    category_verdict: { type: 'string' },
  },
}

phase('Categories')

const results = await parallel(CATEGORIES.map(c => () =>
  agent(
    `You are sourcing the BEST business ACQUISITIONS in CANADA (focus Ontario & British Columbia; note standout deals ` +
    `in other provinces) for Hooman. This is the CANADIAN parallel to a US search — keep it Canada-specific.\n` +
    `Constraints: up to ~$500K CAD of his own cash; time relaxed (willing to work harder / eventually leave his day ` +
    `job); ANY business type; goal = the best acquisition available.\n\n` +
    `FOUNDER: Canadian citizen, AI/ML + data engineering + cloud/infra + EE, strong diligence. CRITICAL CONTEXT: he ` +
    `is a Canadian citizen (so **Canadian financing — BDC, CSBFP, bank acquisition loans — IS available to him**, ` +
    `unlike US SBA). He CURRENTLY LIVES/WORKS IN THE US (TN visa, green card soon), so for each deal FLAG whether it ` +
    `can be run REMOTELY from the US, is SEMI-ABSENTEE, or REQUIRES on-the-ground presence in Canada — this is a real ` +
    `near-term constraint until/unless he relocates.\n\n` +
    `YOUR CATEGORY: ${c.name}\n  Scope: ${c.detail}\n\n` +
    `Read ${OUT}/README.md for the mandate. Do REAL WEB RESEARCH (WebSearch/WebFetch): browse actual Canadian ` +
    `marketplaces/brokers — businessesforsale.com/canada, Sunbelt Canada, BizBuySell (Canada filter), Acquire.com/` +
    `Flippa/EmpireFlippers (Canada), Kijiji/Spergel/DealStream, provincial business-broker sites. Capture REAL current ` +
    `listings with real numbers (asking in CAD, revenue, SDE/cash flow, multiple, age, city/province). Do NOT invent ` +
    `listings; mark gated fields "gated". Prioritize deals fitting ~$500K CAD (all-cash or BDC/seller-financed) with ` +
    `durable cash flow.\n\n` +
    `WRITE findings to ${OUT}/categories/${c.key}.md (use Write; create folders; include URLs where public; cite ` +
    `sources). THEN return the schema. Be honest and quantified; give the real Canadian economics and an honest ` +
    `verdict. Note Canadian specifics: provincial trade-licensing, HST, CAD pricing, and BDC/CSBFP down-payment norms.`,
    { label: `ca:${c.key}`, phase: 'Categories', schema: CAT_SCHEMA, agentType: 'general-purpose' }
  ).then(r => r ? { ...r, key: c.key } : null)
))

const cats = results.filter(Boolean)
const allDeals = cats.flatMap(c => (c.deals || []).map(d => ({ ...d, category: c.category })))
log(`Canadian category scan done: ${cats.length}/${CATEGORIES.length} categories, ${allDeals.length} real deals.`)

phase('Synthesize')

const digest = JSON.stringify({
  categories: cats.map(c => ({ category: c.category, economics: c.category_economics, financing: c.financing_notes, remote: c.remote_operability, fit: c.hooman_fit, verdict: c.category_verdict, deal_count: (c.deals||[]).length })),
  deals: allDeals,
}, null, 2)

const synthesis = await agent(
  `Produce a HEAD-TO-HEAD for the best CANADIAN (ON/BC) acquisition for Hooman at up to ~$500K CAD. He is a Canadian ` +
  `citizen (so BDC/CSBFP/bank financing IS available — unlike US SBA), currently living in the US on TN (green card ` +
  `soon), willing to go full-time. Skills: AI/ML, data eng, cloud/infra, EE, strong diligence.\n\n` +
  `All categories + real Canadian deals (JSON):\n${digest}\n\n` +
  `Read ${OUT}/README.md. Also read ${ROOT}/acquisitions_500k/WIDE_SEARCH_REPORT.md so you can DIRECTLY COMPARE the ` +
  `Canadian option to the US option.\n\n` +
  `WRITE ${OUT}/CANADA_SEARCH_REPORT.md with:\n` +
  `  1. Executive summary: the 3-5 best Canadian acquisitions, with the single top pick.\n` +
  `  2. Master ranked table of the best real Canadian deals (name, category, province, asking CAD, SDE, multiple, ` +
  `cash yield, remote-runnable?, Hooman-fit, financing, fits-$500K-CAD).\n` +
  `  3. Category heat-map for Canada.\n` +
  `  4. THE KEY COMPARISON: Canada vs US for this buyer. Canadian financing (BDC/CSBFP: typical down %, terms) + no ` +
  `visa issue, VS the US path once his green card lands (SBA leverage). Which unlocks a bigger/better business for ` +
  `his $500K? Factor in that he lives in the US now (remote-operability matters) and a green card is coming.\n` +
  `  5. Top 3-5 picks: honest cash flow, risks, owner-hours, remote-operability, where his edge is real.\n` +
  `  6. Bottom line: is the best Canadian deal better than the best US deal for him, considering financing, ` +
  `immigration, remote-operability, and the imminent green card? Give a clear recommendation.\n\n` +
  `Be concrete, quantified, skeptical. Return a ~450-word executive summary as your final text (relayed to Hooman).`,
  { label: 'canada-synthesis', phase: 'Synthesize', agentType: 'general-purpose' }
)

return {
  categories_scanned: cats.length,
  total_deals: allDeals.length,
  best_by_category: cats.map(c => ({ category: c.category, verdict: c.category_verdict })),
  synthesis_summary: synthesis,
}
