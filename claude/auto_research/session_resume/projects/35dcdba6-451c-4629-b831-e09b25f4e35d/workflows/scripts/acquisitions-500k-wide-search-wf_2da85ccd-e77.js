export const meta = {
  name: 'acquisitions-500k-wide-search',
  description: 'Wide search for the best acquisition ~$500K across many business categories (not just SaaS); real deals + economics per category, then a head-to-head',
  phases: [
    { title: 'Categories', detail: 'one agent per business category: real current deals, economics, financing feasibility for a Canadian all-cash ~$500K buyer' },
    { title: 'Synthesize', detail: 'head-to-head across all categories; the genuinely best deals' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'
const OUT = `${ROOT}/acquisitions_500k`

// Deliberately broad — beyond SaaS.
const CATEGORIES = [
  { key: 'saas_software', name: 'SaaS / software / apps',
    detail: 'Vertical B2B SaaS, micro-SaaS, established software, content/data products — but now up to ~$500K (bigger, stickier assets than the $300K search). Acquire.com, Empire Flippers, Flippa, FE International, Microns.' },
  { key: 'ecommerce_brands', name: 'E-commerce / DTC brands / Amazon FBA',
    detail: 'Established product brands with a moat (brand, IP, repeat customers) — NOT commodity dropshipping. Amazon FBA aggregable brands, Shopify DTC, niche product lines. Empire Flippers, Flippa, Quiet Light, brokers.' },
  { key: 'content_media', name: 'Content sites / newsletters / media / communities',
    detail: 'Profitable content/media assets with durable audiences: niche B2B media, paid newsletters, YouTube/media portfolios, community businesses. Note SEO/AI-Overview risk. Empire Flippers, Flippa, brokers.' },
  { key: 'local_service', name: 'Local service businesses (home & trades)',
    detail: 'Home-services and trades: HVAC, plumbing, electrical, landscaping/lawn, cleaning, pest control, pool service, restoration, junk removal. Recurring/route-based preferred. BizBuySell, brokers. The classic "boring business" buy.' },
  { key: 'physical_asset', name: 'Physical / real-asset businesses (semi-absentee)',
    detail: 'Laundromats, self-storage, car washes, vending/ATM/amusement routes, storage, RV/boat storage, coin laundry. Asset-backed, financeable, manager/attendant-run. BizBuySell, brokers.' },
  { key: 'b2b_distribution', name: 'B2B distribution / niche manufacturing / light industrial',
    detail: 'Small niche manufacturers, specialty distributors, B2B product/service companies, commercial services (fire/safety inspection, commercial cleaning, signage, industrial supply). Often overlooked, real cash flow, "boring goldmine" territory. BizBuySell, brokers.' },
  { key: 'franchise_multiunit', name: 'Franchises / multi-unit / semi-absentee ownership',
    detail: 'Semi-absentee franchise ownership (fitness, home services, food, senior care, education) and small multi-unit operators. Manager-run models. Franchise resale + broker listings.' },
]

const CAT_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['category','deals','category_economics','financing_notes','hooman_fit','category_verdict'],
  properties: {
    category: { type: 'string' },
    deals: {
      type: 'array', description: 'REAL current listings found (do not invent); best-fit first',
      items: {
        type: 'object', additionalProperties: false,
        required: ['name','niche_location','asking_price','revenue','sde_cashflow','multiple','age','why_notable','risks','fits_500k_cash'],
        properties: {
          name: { type: 'string' },
          niche_location: { type: 'string' },
          asking_price: { type: 'string' },
          revenue: { type: 'string' },
          sde_cashflow: { type: 'string', description: 'SDE / owner cash flow (annual + monthly if derivable)' },
          multiple: { type: 'string', description: 'x SDE if shown/derivable' },
          age: { type: 'string' },
          why_notable: { type: 'string' },
          risks: { type: 'string' },
          fits_500k_cash: { type: 'string', enum: ['FITS-ALL-CASH','FITS-WITH-FINANCING','OVER-500K'] },
        },
      },
    },
    category_economics: { type: 'string', description: 'typical SDE multiples, cash yields, owner-hours, and monthly cash flow a ~$500K all-cash buy yields in THIS category' },
    financing_notes: { type: 'string', description: 'financing reality for a CANADIAN citizen (no SBA) buying in this category; all-cash vs seller-note vs BDC/Canadian options' },
    hooman_fit: { type: 'string', description: 'can Hooman (AI/data/EE, willing to go full-time) run/improve this category; where his edge helps or is irrelevant' },
    category_verdict: { type: 'string', description: 'honest: is this category a strong vein for the best ~$500K acquisition? best sub-play?' },
  },
}

phase('Categories')

const results = await parallel(CATEGORIES.map(c => () =>
  agent(
    `You are sourcing the BEST possible business ACQUISITIONS for Hooman across a specific category. This is an ` +
    `EXPLORATORY WIDE SEARCH (side quest), separate from his main research. Relaxed constraints:\n` +
    `  - Capital: up to ~$500K of HIS OWN CASH (all-cash within ~$500K; note if a good deal needs more via financing).\n` +
    `  - Time: RELAXED — he is willing to work harder or even QUIT HIS DAY JOB for the right business. So full-time,\n` +
    `    hands-on, owner-operated businesses are now IN SCOPE (not just passive/part-time).\n` +
    `  - Type: broaden beyond SaaS. Find the genuinely best deals in YOUR category.\n` +
    `  - Goal: the best acquisition available, full stop (strong cash flow, fair price, durable, improvable).\n\n` +
    `FOUNDER: Adobe eng manager (AI/ML, data engineering, cloud/infra, EE bachelor's, mech-eng friends, strong ` +
    `diligence/analytical ability). CRITICAL: he is a **CANADIAN CITIZEN, not a US person** — **SBA 7(a)/504 loans ` +
    `generally require a US citizen or permanent resident, so the standard US "10% down + SBA" leverage may NOT be ` +
    `available to him.** Assess financing realistically (all-cash within $500K, seller notes/vendor take-back, or ` +
    `Canadian options like BDC/bank) and FLAG when a deal only works with US-style leverage he may not qualify for.\n\n` +
    `YOUR CATEGORY: ${c.name}\n  Scope: ${c.detail}\n\n` +
    `Read ${OUT}/README.md for the mandate. Do REAL WEB RESEARCH (WebSearch/WebFetch): browse the actual ` +
    `marketplaces/brokers for this category (BizBuySell, Acquire.com, Empire Flippers, Flippa, Quiet Light, ` +
    `BizQuest, franchise resale sites, etc.). Capture REAL current listings with real numbers — asking price, ` +
    `revenue, SDE/cash flow, multiple, age, location. Do NOT invent listings; mark gated fields "gated". ` +
    `Prioritize deals that fit ~$500K (all-cash or light seller-financing) with strong, durable cash flow.\n\n` +
    `WRITE your findings to ${OUT}/categories/${c.key}.md (use Write; create folders; include listing URLs where ` +
    `public; cite sources). THEN return the structured schema. Be honest and quantified — for each category give the ` +
    `real economics (typical SDE multiple, cash yield, owner-hours) and an honest verdict on whether it's a strong ` +
    `vein for the best ~$500K buy.`,
    { label: `cat:${c.key}`, phase: 'Categories', schema: CAT_SCHEMA, agentType: 'general-purpose' }
  ).then(r => r ? { ...r, key: c.key } : null)
))

const cats = results.filter(Boolean)
const allDeals = cats.flatMap(c => (c.deals || []).map(d => ({ ...d, category: c.category })))
log(`Category scan done: ${cats.length}/${CATEGORIES.length} categories, ${allDeals.length} real deals captured.`)

phase('Synthesize')

const digest = JSON.stringify({
  categories: cats.map(c => ({ category: c.category, economics: c.category_economics, financing: c.financing_notes, fit: c.hooman_fit, verdict: c.category_verdict, deal_count: (c.deals||[]).length })),
  deals: allDeals,
}, null, 2)

const synthesis = await agent(
  `You are producing a HEAD-TO-HEAD across business categories to find the BEST acquisition for Hooman at up to ` +
  `~$500K all-cash. He has relaxed time (willing to go full-time / quit his job) and wants the best deal regardless ` +
  `of type (NOT just SaaS). He is a CANADIAN citizen (likely NO SBA leverage — weigh financing feasibility). Skills: ` +
  `AI/ML, data eng, cloud/infra, EE, strong diligence.\n\n` +
  `All categories + real deals found (JSON):\n${digest}\n\n` +
  `Read ${OUT}/README.md for the mandate and scorecard dimensions.\n\n` +
  `WRITE ${OUT}/WIDE_SEARCH_REPORT.md with:\n` +
  `  1. Executive summary: the 3-5 genuinely BEST acquisition opportunities across ALL categories, with the single ` +
  `top "if I were buying one thing" pick and why.\n` +
  `  2. A master ranked table of the best real deals found across all categories (name, category, asking, SDE, ` +
  `multiple, cash yield, owner-hours, Hooman-fit, financing-feasibility, fits-$500K).\n` +
  `  3. Category heat-map: which business categories are the best veins for a $500K buyer willing to go full-time, ` +
  `and which are traps — with the honest economics (SDE multiples, cash yields) of each.\n` +
  `  4. The financing reality for a Canadian all-cash ~$500K buyer (no SBA) and how it changes what's reachable ` +
  `(all-cash ~$500K vs the leveraged $1-2M deals a US buyer could reach with the same cash).\n` +
  `  5. For the top 3-5 picks: honest cash flow, what could go wrong, owner-hours, and where Hooman's AI/data/EE ` +
  `background is a real edge vs irrelevant.\n` +
  `  6. Bottom line: does going wider + bigger + full-time beat the part-time buy-SaaS conclusion from the main ` +
  `research? Is there a real path to strong income (e.g. $10-40K/mo owner cash flow) here?\n\n` +
  `Be concrete, quantified, skeptical; SaaS should NOT dominate by default — judge it against local service, ` +
  `physical-asset, distribution, and other businesses on cash yield + durability + fit. Return a ~450-word ` +
  `executive summary as your final text (relayed to Hooman).`,
  { label: 'wide-synthesis', phase: 'Synthesize', agentType: 'general-purpose' }
)

return {
  categories_scanned: cats.length,
  total_deals: allDeals.length,
  best_by_category: cats.map(c => ({ category: c.category, verdict: c.category_verdict })),
  synthesis_summary: synthesis,
}
