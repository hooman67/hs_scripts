export const meta = {
  name: 'bc-saas-diligence-and-canada-sweep',
  description: 'Parallel: (2) full deep-research on the BC Staffing-Mgmt SaaS; (3) Canadian micro-SaaS manual-sweep link/search kit; (4) document US-side learnings + current state',
  phases: [
    { title: 'Work', detail: '3 independent tracks in parallel: BC SaaS diligence, Canada sweep kit, US-side documentation' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'

phase('Work')

// ---- TRACK 2: full deep-research on the BC Staffing-Mgmt SaaS ----
const bcSaas = agent(
  `You are doing FULL ACQUISITION DEEP-RESEARCH on the #1 pick for Hooman: the "BC Staffing-Management Vertical SaaS" ` +
  `surfaced in ${ROOT}/acquisitions_canada/CANADA_SEARCH_REPORT.md (and its category file ` +
  `${ROOT}/acquisitions_canada/categories/saas_software.md). READ BOTH FIRST for the known facts.\n\n` +
  `Known facts from the search: ~16-yr B2B SaaS, staffing/recruiting-agency vertical, ~US$249K SDE (~$338K CAD, ` +
  `~55% net margin), 100+ clients, 90%+ recurring, <2% churn, 32% YoY growth, run by ~5 home-based contractors, ` +
  `priced ~US$1M (~$1.35M CAD, ~4x SDE / ~2.2x revenue), surfaced on BizQuest. Buyer: Hooman — Canadian citizen ` +
  `(BDC/bank leverage available), Adobe AI/ML+data+infra engineer, up to ~$500K CAD cash, can run it remotely from ` +
  `the US on TN today.\n\n` +
  `Do REAL WEB RESEARCH (WebSearch/WebFetch): (a) try to locate the actual live listing (BizQuest, BusinessSellCanada, ` +
  `Flippa, Acquire, brokers) and capture every real number + the listing URL/ID; (b) map the staffing-software ` +
  `competitive landscape (Bullhorn, Avionté, JobDiva, CEIPAL, Crelate, Tempworks, RecruiterFlow, Zoho Recruit) to judge ` +
  `whether a small 16-yr vertical player defends its 100 clients / <2% churn or is being slowly displaced; (c) assess ` +
  `the market (staffing-agency software TAM, is the niche growing/declining, AI-disruption exposure to recruiting SaaS); ` +
  `(d) validate the economics skeptically (is 55% margin + <2% churn + 32% growth internally consistent? gross vs net? ` +
  `USD/CAD FX exposure); (e) the financing structure in detail — realistic BDC equity % + term + rate for a ~$1.35M CAD ` +
  `deal, seller-note norms, what ~$400-500K CAD down actually services, and true post-debt owner take-home; (f) the #1 ` +
  `risk flagged: growth is owner-led outbound/conference SALES — quantify how dependent revenue is on the seller's ` +
  `selling and what replacing it costs.\n\n` +
  `Then produce a full deep-research doc: product/what-it-does, ICP & why-they-stay (moat), competitive verdict, market ` +
  `& AI-disruption outlook, honest economics + financing math + post-debt take-home, the owner-dependence risk analysis, ` +
  `a diligence checklist (source-verify revenue/churn/concentration, code/IP, the sales-transferability question), and a ` +
  `GO/CONDITIONAL/PASS verdict with the specific deal-killers to confirm. Mark claims VERIFIED/ASSUMED/UNVERIFIED and ` +
  `cite sources. WRITE it to ${ROOT}/acquisitions_canada/deepdive_bc_staffing_saas.md (use Write). Return a ~300-word ` +
  `executive summary as your final text.`,
  { label: 'bc-staffing-saas', phase: 'Work', agentType: 'general-purpose' }
);

// ---- TRACK 3: Canadian micro-SaaS manual-sweep kit (links + saved searches) ----
const canadaSweep = agent(
  `Build a MANUAL MARKETPLACE SWEEP KIT for Hooman to find Canadian-domiciled micro-SaaS acquisitions <=$500K CAD that ` +
  `automated research missed (Flippa/Acquire/DealStream/businessesforsale detail pages were bot-blocked/JS-gated/login-` +
  `gated). He is a Canadian citizen, AI/ML+data+infra engineer, wants durable + remote-operable + mandate-driven SaaS, ` +
  `runnable from the US today.\n\n` +
  `Read ${ROOT}/acquisitions_canada/CANADA_SEARCH_REPORT.md and ${ROOT}/runs/buy_microsaas_PLAYBOOK.md (Buy Box) first.\n\n` +
  `Do WEB RESEARCH to get the ACTUAL working URLs and exact search/filter setup for each marketplace so Hooman can do a ` +
  `~1-hour logged-in pass himself. For EACH marketplace (Acquire.com, Flippa, Empire Flippers, FE International, ` +
  `MicroAcquire/Acquire, BizQuest, BusinessesForSale.com/canada, BusinessSellCanada.com, Sunbelt Canada, DealStream, ` +
  `Kijiji Business-for-sale, Latona's, Motion Invest, Tiny Acquisitions) provide: the direct SaaS/Canada listing URL, the ` +
  `exact filters to set (category=SaaS, location=Canada/ON/BC, price<=$500K, recurring), whether a free/paid account is ` +
  `needed, keyword searches to run (e.g. "SaaS Canada", "Ontario software", "compliance SaaS", "vertical B2B SaaS"), and ` +
  `what to check on each listing against the Buy Box. Include a short "how to verify a listing" and the Gate-2 script ` +
  `(read-only Stripe + bank, % ARR from largest customer, what runs without the LLM). Do NOT invent listings — this is a ` +
  `navigational kit (working links + search recipes), not a listing dump; if you happen to surface a real Canadian SaaS ` +
  `listing, capture it, else focus on the repeatable search recipe.\n\n` +
  `WRITE the kit to ${ROOT}/acquisitions_canada/CANADA_SWEEP_KIT.md (use Write; real URLs; organized per marketplace). ` +
  `Return a ~200-word summary as your final text.`,
  { label: 'canada-sweep-kit', phase: 'Work', agentType: 'general-purpose' }
);

// ---- TRACK 4: document everything learned + current state on the US side ----
const usDoc = agent(
  `Write a comprehensive US-SIDE STATUS & LEARNINGS document for Hooman's acquisition search. This consolidates ` +
  `everything the project learned about the US acquisition path and states exactly where things stand, so a fresh agent ` +
  `(or Hooman) can pick up cleanly.\n\n` +
  `READ these sources and synthesize (do not just copy): ${ROOT}/PROJECT_STATE.md, ${ROOT}/LEARNINGS.md, ` +
  `${ROOT}/acquisitions_500k/WIDE_SEARCH_REPORT.md, ${ROOT}/acquisitions_500k/saas_deepdive/SAAS_DEEPDIVE_REPORT.md, ` +
  `${ROOT}/runs/buy_microsaas_PLAYBOOK.md, ${ROOT}/runs/buy_microsaas_LIVE_LISTINGS.md, ` +
  `${ROOT}/runs/buy_microsaas_300K_UPDATE.md, and ${ROOT}/acquisitions_canada/CANADA_SEARCH_REPORT.md (for the US-vs-CA ` +
  `contrast). No new web research needed — this is documentation.\n\n` +
  `Produce ${ROOT}/acquisitions_500k/US_STATUS_AND_LEARNINGS.md covering:\n` +
  `  1. The US financing reality: TN visa = no SBA today + can't self-operate; green card SOON reopens SBA leverage; ` +
  `daughter-US-citizen option (messy, lawyer-only); E-2 as interim. What each unlocks and WHEN.\n` +
  `  2. What the US search found: the barbell (laundromat / boring vertical B2B SaaS / recurring-route service / CNC fab), ` +
  `the honest economics per category, and the traps (Amazon FBA, SEO/content, franchises, self-storage).\n` +
  `  3. The live-listings reality: at $150K nothing clean; $300K crosses the delegation threshold (~$4-6K/mo net buyable); ` +
  `the 3 dry-run candidates (IMS/ISO compliance, healthcare exercise-mgmt, property-mgmt) + the 2 good-shape deep-dives ` +
  `(building-ops = over-ceiling/SBA-only; Amazon-sourcing = fits but Amazon-dependent + decaying moat).\n` +
  `  4. The SaaS-exemplar finding: EH&S/SDS + email-provider were exemplars not live deals; EH&S trades off-market; drop email.\n` +
  `  5. The big cross-cutting learnings (moat is the kill dimension; buy>build; time is the constraint; citizenship reshapes it).\n` +
  `  6. EXACTLY WHERE WE ARE: what's decided, what's open, the US path recommendation, and the decision to PIVOT to what's ` +
  `buyable now (BC Staffing SaaS in Canada, or US laundromat/pest-control). Make it a clean handoff.\n\n` +
  `Be organized, quantified, human-readable. Return a ~250-word summary as your final text.`,
  { label: 'us-status-doc', phase: 'Work', agentType: 'general-purpose' }
);

const [bc, sweep, us] = await Promise.all([bcSaas, canadaSweep, usDoc]);

return {
  research_explorer_path: `${ROOT}/research_explorer.html`,
  bc_staffing_saas_summary: bc,
  canada_sweep_kit_summary: sweep,
  us_status_doc_summary: us,
};
