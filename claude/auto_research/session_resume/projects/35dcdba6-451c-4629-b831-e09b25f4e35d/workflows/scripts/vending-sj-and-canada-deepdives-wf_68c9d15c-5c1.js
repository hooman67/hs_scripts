export const meta = {
  name: 'vending-sj-and-canada-deepdives',
  description: 'Parallel: (2) evaluate the San Jose vending listing + local vending economics; (3) full deep-research on 4 Canadian deals (Richmond integrator, ON deodorant DTC, ON cyber SaaS, Toronto laundromats)',
  phases: [
    { title: 'Research', detail: '5 independent deep-dives in parallel' },
    { title: 'Wrap', detail: 'vending verdict note + confirm docs written' },
  ],
}

const ROOT = '/home/colligo/hs_scripts/claude/auto_research'

phase('Research')

// ---- (2) San Jose vending machine business ----
const vending = agent(
  `Evaluate a SPECIFIC vending-machine business for Hooman, who wants a business he (or his wife) can PERSONALLY ` +
  `oversee around San Jose, CA. Listing: https://www.bizquest.com/business-for-sale/lucrative-vending-machines-healthier-snacks-and-drinks-semi-passive/BW2489375/ ` +
  `("Lucrative Vending Machines - Healthier Snacks and Drinks - Semi Passive").\n\n` +
  `Buyer context: Hooman is a Canadian citizen on a TN visa (green card soon), lives in the San Jose / Bay Area, Adobe ` +
  `AI/ML+data engineer, ~$500K capital, strong diligence. IMMIGRATION NOTE: TN bars actively self-operating his own US ` +
  `business — but a vending route he oversees while his WIFE (check her work-authorization status is unknown — FLAG it) ` +
  `or a hired operator runs it may be structurable; flag this as a real question for an immigration lawyer, don't assume.\n\n` +
  `Do REAL WEB RESEARCH: (a) WebFetch the listing and capture every real number (asking, revenue, SDE/cash flow, # ` +
  `machines, # locations, multiple, what's included — machines/inventory/vehicle); (b) the economics of vending route ` +
  `businesses generally (typical gross margin, SDE multiples 1.5-3x, cost per machine, location/commission structure, ` +
  `restocking labor hours, shrink/theft, machine breakdown/depreciation); (c) the healthier-snacks/micro-market angle ` +
  `(is it a differentiator or a fad; competition from Canteen/Aramark/local operators); (d) Bay Area specifics (location ` +
  `access, high labor/gas cost, commission pressure from premium locations); (e) the "semi-passive" claim — is it real ` +
  `or does someone drive a route 20-40 hr/wk restocking?\n\n` +
  `Assess honestly for THIS buyer: is this a good business to personally oversee, what are the real owner-hours, does the ` +
  `SDE survive scrutiny (vending SDE is notoriously inflated — cash handling, unrecorded shrink, deferred machine ` +
  `capex), what are the deal-killers, and a verdict (PURSUE / VISIT-WORTH-IT / PASS). Give a concrete "what to check on a ` +
  `site visit" list since Hooman or his wife may go look at the machines/locations in person. Mark VERIFIED/ASSUMED/` +
  `UNVERIFIED and cite sources. WRITE to ${ROOT}/acquisitions_500k/deepdive_sanjose_vending.md (use Write). Return a ` +
  `~300-word executive summary as your final text.`,
  { label: 'sj-vending', phase: 'Research', agentType: 'general-purpose' }
);

// ---- (3a) Richmond BC Low-Voltage Integrator ----
const richmond = agent(
  `Full acquisition deep-research on the "Richmond BC Low-Voltage / Smart-Systems Integrator" surfaced in ` +
  `${ROOT}/acquisitions_canada/CANADA_SEARCH_REPORT.md and ${ROOT}/acquisitions_canada/categories/local_service.md ` +
  `(READ BOTH for known facts). Known: ~$389K CAD ask / ~$130K SDE / ~3.0x, all-cash-able, EE/electronics business ` +
  `(CCTV, access control, automation, AV), already ships "proprietary AI proposal automation," seller leaving for AI ` +
  `ventures, retained Office Manager + Technical Lead, 20-30% down seller VTB. Buyer: Hooman (Canadian citizen, EE ` +
  `bachelor's + AI/data eng — strong domain adjacency; US-resident on TN, so flag remote/semi-absentee feasibility and ` +
  `whether periodic BC presence is needed).\n\n` +
  `Do REAL WEB RESEARCH: locate the live listing + real numbers + URL; the low-voltage/security-integration industry ` +
  `(margins, recurring monitoring revenue vs project revenue, competition, BC electrical/security licensing rules — ` +
  `does the OWNER need a license or does the Technical Lead's suffice?); the key-man risk (Technical Lead holds ` +
  `credentials); the ~24 subcontractor model; whether the "AI proposal automation" is real IP or marketing. Assess ` +
  `founder-fit (his EE/AI edge), remote-operability from the US, financing, owner-hours, and the honest SDE. Verdict ` +
  `GO/CONDITIONAL/PASS + deal-killers. Mark VERIFIED/ASSUMED/UNVERIFIED, cite sources. WRITE to ` +
  `${ROOT}/acquisitions_canada/deepdive_richmond_lowvoltage.md. Return a ~250-word summary.`,
  { label: 'richmond-integrator', phase: 'Research', agentType: 'general-purpose' }
);

// ---- (3b) Central-ON Natural Deodorant DTC ----
const deodorant = agent(
  `Full acquisition deep-research on the "Central-Ontario Natural Deodorant DTC Brand" from ` +
  `${ROOT}/acquisitions_canada/CANADA_SEARCH_REPORT.md and ${ROOT}/acquisitions_canada/categories/ecommerce_brands.md ` +
  `(READ BOTH). Known: ~$349K CAD / ~$100K SDE / ~3.5x, 13 yrs, EWG-Verified, 1,000+ Amazon Subscribe & Save recurring ` +
  `subs, multi-channel, retirement seller, seller financing. Buyer: Hooman (US-resident on TN; so it's semi-absentee at ` +
  `best from the US and only if a co-packer + 3PL are installed — assess this hard).\n\n` +
  `Do REAL WEB RESEARCH: locate the live listing + real numbers + URL; the natural-deodorant/clean-beauty DTC market ` +
  `(margins, CAC, Amazon-dependency, competition from Native/Schmidt's/Each & Every, private-label pressure); the moat ` +
  `(brand, EWG cert, 13-yr Subscribe & Save base) and how durable; the operational reality (does the seller manufacture ` +
  `in-house? can it move to a co-packer without margin collapse? 3PL for fulfillment?); channel mix (Amazon vs DTC vs ` +
  `retail/wholesale) and concentration. Assess remote-operability from the US, financing (note CSBFP won't fund ` +
  `goodwill), honest SDE, and where Hooman's AI/data edge helps (little — flag it). Verdict + deal-killers. Mark ` +
  `VERIFIED/ASSUMED/UNVERIFIED, cite sources. WRITE to ${ROOT}/acquisitions_canada/deepdive_deodorant_dtc.md. Return a ` +
  `~250-word summary.`,
  { label: 'deodorant-dtc', phase: 'Research', agentType: 'general-purpose' }
);

// ---- (3c) Ontario Cybersecurity / Security-Awareness SaaS ----
const cyber = agent(
  `Full acquisition deep-research on the "Ontario Cybersecurity / Security-Awareness SaaS" from ` +
  `${ROOT}/acquisitions_canada/CANADA_SEARCH_REPORT.md and ${ROOT}/acquisitions_canada/categories/saas_software.md ` +
  `(READ BOTH). Known: CA$207K revenue, price gated, compliance-driven B2B niche, 35+ clients, recurring, Ontario-` +
  `domiciled, fully remote, 6 employees, no seller financing, crowded category (KnowBe4/Hoxhunt). Buyer: Hooman (Canadian ` +
  `citizen, AI/ML+data+infra eng — strong software fit; fully remote works from US on TN).\n\n` +
  `Do REAL WEB RESEARCH: locate the live listing + real numbers + URL (price is gated — try to surface it); the ` +
  `security-awareness-training market (KnowBe4, Hoxhunt, Proofpoint, Mimecast, Curricula, Wizer, huge free/low-cost ` +
  `competition) and whether a 35-client $207K-rev player can defend a niche or is sub-scale roadkill; the compliance ` +
  `angle (does a mandate drive stickiness?); the 6-employee cost load vs $207K revenue (is this even profitable? SDE ` +
  `likely thin/negative — dig); founder-fit (his edge) and whether it's worth buying vs building. Assess financing (no ` +
  `seller note = all-cash), remote-operability, honest SDE, verdict + deal-killers. Be skeptical: 6 employees on $207K ` +
  `revenue is a red flag. Mark VERIFIED/ASSUMED/UNVERIFIED, cite sources. WRITE to ` +
  `${ROOT}/acquisitions_canada/deepdive_ontario_cyber_saas.md. Return a ~250-word summary.`,
  { label: 'ontario-cyber-saas', phase: 'Research', agentType: 'general-purpose' }
);

// ---- (3d) Toronto laundromats (6210 Finch + Scrubby's) ----
const laundromats = agent(
  `Full acquisition deep-research on the TWO Toronto laundromats from ${ROOT}/acquisitions_canada/CANADA_SEARCH_REPORT.md ` +
  `and ${ROOT}/acquisitions_canada/categories/physical_asset.md (READ BOTH). (1) "6210 Finch" fully unattended / ` +
  `remote-controlled, ~$725K CAD, 5+5+5 lease, financials undisclosed. (2) "Scrubby's" ~$345K CAD all-cash but only ` +
  `~2.5 yrs left on lease. Buyer: Hooman (US-resident on TN; wife or a local operator could help; the appeal is genuine ` +
  `remote-operability of an unattended card/app laundromat + his utility-vs-revenue diligence edge).\n\n` +
  `Do REAL WEB RESEARCH: locate both live listings + real numbers + URLs; laundromat acquisition economics (SDE ` +
  `multiples 3-5x cash flow, the LEASE is the #1 value driver — quantify why 2.5 yrs left is near-fatal for Scrubby's; ` +
  `utility-bill-vs-revenue verification technique; unattended/card-app model pros/cons; equipment age/replacement ` +
  `capex; Toronto coin-laundry competition). Assess remote-operability (needs a local cleaner + on-call tech), financing ` +
  `(CSBFP/BDC won't fund leasehold goodwill — so mostly cash), honest cash flow, and a per-listing verdict. Give a ` +
  `"what to verify (processor reports + utility records + lease)" checklist. Mark VERIFIED/ASSUMED/UNVERIFIED, cite ` +
  `sources. WRITE to ${ROOT}/acquisitions_canada/deepdive_toronto_laundromats.md. Return a ~250-word summary.`,
  { label: 'toronto-laundromats', phase: 'Research', agentType: 'general-purpose' }
);

const [v, r, d, c, l] = await Promise.all([vending, richmond, deodorant, cyber, laundromats]);

phase('Wrap');
log('All 5 deep-dives written.');

return {
  sanjose_vending: v,
  richmond_integrator: r,
  deodorant_dtc: d,
  ontario_cyber_saas: c,
  toronto_laundromats: l,
};
