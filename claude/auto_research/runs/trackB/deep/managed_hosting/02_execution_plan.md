# Execution Plan — Managed Technical Hosting / DevOps-lite (HostiFi model)

**Date**: 2026-07-01. **Author**: Claude (Opus 4.8). **For**: Hooman Shariati.
**Companion doc**: `01_research_validation.md` (read it first — this plan is built on its
CONDITIONAL verdict, not the original optimistic pitch).

---

## 0. The one thing to internalize before spending a dollar

Research verdict = **CONDITIONAL, MEDIUM confidence.** The proof point (HostiFi) is real, the
capital/downside are the best in the whole idea set, and the *build* is 1:1 with Hooman's infra
skills. **But three findings invert the pitch:**

1. **The infra was never the bottleneck.** HostiFi's founder was non-technical; the moat was
   community position + sales/support — exactly Hooman's flagged weakness.
2. **No clean target exists.** UniFi is double-covered (HostiFi incumbency **+** Ubiquiti's own
   Official Hosting since ~2022). n8n is license-gated + has n8n Cloud. Horizontal players
   (Elestio $11/mo, PikaPods $1.80/mo) already set the price floor below the pitch's $10–50.
3. **It's a second 0→1 distribution front** competing with CutLog for the same scarce 10–20 hrs/wk.

**Consequence:** this plan is deliberately **gated and validation-first**. We spend real build
money **only after** a paying-demand signal, and we present the **acquisition path as the
recommended default** because it is the only variant that (a) sidesteps the distribution grind,
(b) keeps Hooman part-time via inherited ops, and (c) matches the research's explicit
recommendation ("deploy capital into a cash-flowing acquisition over opening a second
distribution front"). We do **not** build a from-scratch UniFi/n8n host. Full stop.

**Revenue framing for the whole plan:** realistic **$2–8K/mo net in 12–24 months**; $5K/mo needs
~100–300 paid instances; $10–25K/mo is a multi-year outlier. Plan to the base case, not the pitch.

---

## 1. The specific target (chosen)

The research proves there is **no clean greenfield niche**, so we split into two mutually-exclusive
tracks and pick between them at Gate 1 (Day 30). Hooman does NOT run both.

### Track A (RECOMMENDED default) — Acquire a small, cash-flowing managed-hosting micro-SaaS
- **Profile to buy:** a single-tool managed-hosting business doing **$3–12K/mo MRR**, **>60% margin**,
  **<15 hrs/wk owner involvement**, **>18 months operating history**, **<5% monthly churn**, on a
  tool with **no aggressive first-party cloud** and a **permissive license**.
- **Where:** Acquire.com (formerly MicroAcquire), Flippa (SaaS filter), Tiny Acquisitions,
  IndieHackers "for sale", MicroConf/founder Slacks, direct outreach to sub-scale hosts.
- **Price band:** $25–120K (roughly **2.5–4× annual profit** for a part-time-run micro-SaaS).
  Fits the $25–150K envelope with headroom for transition costs.
- **Why this over building:** you buy the customer base + community position + proven playbook —
  the exact things the research says can't be built from scratch part-time. Infra skills become a
  **margin/reliability edge** (improve provisioning, cut COGS, reduce on-call), which is the
  correct axis for Hooman's strengths.

### Track B (FALLBACK, only if Gate 1 finds a validated niche) — Build one narrow niche host
- **Target profile (all four must hold):** (1) a **specific B2B self-hosted tool** with a real
  **non-technical paying base**; (2) **no first-party managed cloud**; (3) a **permissive license**
  (MIT/Apache/GPL — NOT SSPL/BSL/Fair-source/Sustainable-Use); (4) a reachable community with
  evidence of willingness to pay ≥ $25/mo.
- **Explicitly disqualified:** UniFi/UISP/Omada (taken), n8n (license + n8n Cloud), Ghost/WordPress
  (saturated/vendor-owned), developer tools (technical base), homelab/hobbyist apps (PikaPods
  $1.80/mo floor).
- **Candidate hunting ground (unproven, to be validated, not assumed):** niche vertical B2B
  self-hosted tools — e.g. self-hosted booking/scheduling, small-clinic/practice tools, church/
  nonprofit management, self-hosted LMS for training companies, self-hosted helpdesk for MSPs.
  **None has a proof point** — that is precisely what Gate 1 must produce before any build spend.

---

## 2. First 90 days — week by week

Budget for the whole 90 days: **≤ $2,000** (all validation; no product build until Gate 2).
Time: **≤ 6 hrs/wk** so CutLog keeps priority. "Hooman" = does it himself; "Contractor" not yet hired.

### Weeks 1–2 — Market & deal-flow scan (both tracks in parallel, cheap)
- **Hooman:** Create buyer accounts on Acquire.com, Flippa, Tiny Acquisitions. Set saved searches
  ("managed hosting", "self-hosted", "SaaS", MRR $2–12K). Log every listing matching Track-A
  profile into a sheet with MRR, margin, tool, license, churn, ask price, owner hrs/wk.
- **Hooman:** Build the "disqualifier checklist" (vendor cloud? license? technical base?) and run
  the top 20 candidate self-hosted tools through it for Track B. Kill fast.
- **Validated by end of Wk2:** Is there ≥1 credible Track-A acquisition candidate AND/OR ≥1
  Track-B tool passing all four filters? If **zero on both** → early NO-GO (see Gate 0).

### Weeks 3–4 — Demand probes (Track B) + first seller conversations (Track A)
- **Track A / Hooman:** Contact 3–5 sellers. Ask for MRR proof (Stripe screenshots), churn,
  COGS, support-ticket volume, on-call load, license status of hosted tool, concentration risk.
- **Track B / Hooman:** For each surviving tool, post/DM in its community: "Would you pay $X/mo to
  never touch the server?" Target **10 qualitative replies** and **≥3 "yes, take my money now"**.
  Optionally stand up a $5 landing page (Carrd) + Stripe "pre-order" link — **a real card charge
  is the only signal that counts.**
- **Validated by end of Wk4:** Track A — at least one seller with verifiable Stripe MRR and clean
  license/vendor-cloud story. Track B — ≥3 real pre-commitments (card or signed LOI).

### Gate 1 (Day 30) — PICK ONE TRACK OR STOP
- **Go Track A** if: a candidate with verified MRR ≥ $3K/mo, margin ≥ 60%, churn < 5%/mo, owner
  hrs < 15/wk, clean license/no-vendor-cloud, ask ≤ 4× profit.
- **Go Track B** if: ≥3 paying pre-commitments on a tool passing all four filters AND no
  acceptable Track-A deal exists.
- **STOP** if neither. Sunk cost so far ≤ ~$500 + ~24 hrs. This is the whole point of gating.

### Weeks 5–8 — Diligence (Track A) OR MVP scoping (Track B)
- **Track A / Hooman + hired advisor:** Deep diligence on the chosen deal — verify Stripe payouts
  vs claimed MRR, cohort churn, refund rate, hosting-COGS invoices, customer concentration, TOS/
  license of the hosted tool, transferability of infra + domains + support inbox. Engage an
  **escrow (Escrow.com) + a lightweight SaaS-purchase-agreement template** (lawyer review, ~$1.5K).
- **Track B / Hooman:** Scope the thinnest possible provisioning+billing+monitoring MVP for the
  one validated tool. Reuse the CutLog stack where possible (Vercel/Stripe patterns already known).

### Weeks 9–12 — Close (Track A) OR ship private beta (Track B)
- **Track A / Hooman:** Close via escrow. Run a **30-day transition** with the seller retained on
  a handover retainer (support SOPs, on-call runbook, community access). **Do not change pricing
  or stack in month 1** — just keep the lights on and observe.
- **Track B / Hooman:** Ship to the ≥3 pre-committed customers. Charge real money day one.
- **Gate 2 (Day 90):** Track A — MRR held within 5% of purchase through transition, on-call load
  confirmed < 8 hrs/wk. Track B — ≥5 paying instances live, churn signal acceptable. Else pause.

---

## 3. Months 4–12 — path to revenue, staying part-time

**Non-negotiable constraint:** Hooman stays ≤ 10 hrs/wk on this and CutLog remains his primary
0→1. The lever that keeps this part-time is **delegation of ops/support/on-call**, funded by the
business's own margin. If it can't fund its own contractor, it isn't working — pause it.

### Track A (acquisition) 12-month path
- **Month 4:** Hire a **part-time ops/support contractor** ($1.5–3K/mo, offshore or fractional)
  to own tier-1 support + on-call rotation. Hooman = architecture, COGS optimization, escalations.
- **Months 5–7:** Apply infra edge — migrate to cheaper/more-reliable provisioning, automate the
  top 3 manual support tasks, tighten backups/monitoring. Goal: **lift margin 5–10 pts** and cut
  Hooman's own hours toward < 5/wk.
- **Months 8–12:** Grow via the inherited community position (SEO, existing customer referrals,
  one adjacent tool if it passes the same 4 filters). Target **+30–50% MRR** organically.
- **12-mo target:** if bought at $5K/mo MRR → **$6.5–8K/mo MRR, ~$4–6K/mo net** after contractor
  and COGS. Within the realistic base case.

### Track B (build) 12-month path — slower, harder, only if Gate 1 forced it
- **Months 4–6:** Grind the one community that pre-committed. Content + direct outreach. Target
  **20–40 paid instances**.
- **Month 6:** Hire the support/on-call contractor **the moment MRR clears ~$3K/mo** — do not let
  on-call trap Hooman full-time.
- **Months 7–12:** Reach **60–100 paid instances** = ~$2–5K/mo net at $25–50/mo. This is a slog and
  the honest ceiling for a part-time year-1 build; if it stalls under 30 instances by month 9,
  **cut it** and redirect hours to CutLog.

---

## 4. Budget (within $25–150K), burn, break-even

### Track A (recommended)
| Item | Amount |
|---|---|
| Acquisition price (2.5–4× profit; target ~$5K/mo MRR biz) | $40–100K |
| Legal (SaaS purchase agreement review) + escrow fees | $2–3K |
| Seller transition retainer (1 month) | $2–4K |
| Cloud/tooling float during transition | $1–2K |
| **Upfront total** | **$45–109K** |
| Ongoing monthly burn (contractor + cloud COGS) | **$2.5–5K/mo** |
| **Break-even** | If acquired cash-flow-positive, **immediate** on operating basis; recover purchase price in **~18–30 months** at base-case net |

### Track B (fallback)
| Item | Amount |
|---|---|
| Validation (Weeks 1–4) | $0.5–2K |
| Build (reuse CutLog stack) | $3–6K |
| Cloud float + tooling (yr 1) | $3–5K |
| Support contractor (from ~month 6, funded by MRR) | $1.5–3K/mo |
| **Upfront before contractor** | **~$8–13K** |
| **Break-even** | ~**60–80 paid instances** (~$2–3K/mo net) covering contractor + COGS; realistically **month 9–15** |

Both tracks sit comfortably inside the $25–150K envelope. Track A uses more capital (the point:
**capital substitutes for the distribution grind Hooman can't do part-time**). Track B is cheaper
but pays for it in Hooman's scarcest resource — hours.

---

## 5. Revenue model + realistic ramp

- **Model:** flat recurring $19–99/mo per instance (Track A inherits its own tiers; Track B
  targets $25–50/mo — never compete at the $1.80–$11 horizontal floor).
- **Margin:** 60–80% after cloud COGS (VMs, Backblaze/DO Spaces backups, Zabbix). Confirmed.

**Ramp (Track A, base case, bought at ~$5K/mo MRR):**
| Month | 3 | 6 | 9 | 12 | 18 | 24 |
|---|---|---|---|---|---|---|
| MRR | 5.0K | 5.5K | 6.2K | 7.0K | 8.5K | 10K |
| Net after contractor+COGS | ~1.5K | ~2.5K | ~3.5K | ~4.5K | ~6K | ~7K |

**Ramp (Track B, base case):**
| Month | 3 | 6 | 9 | 12 | 18 | 24 |
|---|---|---|---|---|---|---|
| Paid instances | 5 | 25 | 50 | 80 | 130 | 200 |
| Net | ~$0 | ~$0.5K | ~$1.5K | ~$2.5K | ~$4K | ~$6K |

Both land in the research's honest **$2–8K/mo in 12–24mo** band. Neither hits $10–25K in year one.

---

## 6. Go / No-Go gates (cheapest validation first)

- **Gate 0 (Day 14, ~$200):** Deal-flow + disqualifier scan. **NO-GO if** zero Track-A candidates
  AND zero Track-B tools survive the 4 filters. Cost to learn "no": ~$200 + ~10 hrs.
- **Gate 1 (Day 30, ~$500):** Pick a track (see §2). Requires *either* a verified-MRR acquisition
  candidate *or* ≥3 real paying pre-commitments (a charged card, not a survey). **STOP if neither.**
- **Gate 2 (Day 90):** Track A — MRR held ±5% through transition, on-call < 8 hrs/wk. Track B — ≥5
  paying instances, churn tolerable. **Pause & reassess vs CutLog if missed.**
- **Gate 3 (Month 9):** Track A — net ≥ $3K/mo and Hooman < 5 hrs/wk. Track B — ≥30 instances.
  **Kill and redirect to CutLog if missed.**

**Cheapest possible pre-money validation:** before ANY build/purchase money, get a **real card
charge** (Track B pre-order) or **verified Stripe payout evidence** (Track A). Surveys and
"would you pay" do not count.

---

## 7. Coexistence with CutLog (capital + delegation, NOT focus)

Master-report §5 is explicit: Hooman has time for **one** serious 0→1, and that is **CutLog**.
This plan respects that:

- **CutLog gets the focus hours; this gets capital.** Track A is chosen precisely because an
  acquired, already-running business demands *ops oversight*, not *0→1 hustle* — it can be run in
  < 5 hrs/wk once a contractor owns support/on-call.
- **The contractor is the coexistence mechanism.** Hire tier-1 support + on-call early (month 4
  Track A; ~$3K MRR Track B). Hooman is escalation-only. If the business can't fund the contractor
  from its own margin, that is the signal it's stealing focus from CutLog — pause it (Gate 3).
- **Hard rule:** if in any month this consumes > 10 hrs of Hooman's time OR CutLog progress
  visibly slips, this project pauses until a contractor absorbs the load. CutLog is never the
  variable that gives.
- **Track B is discouraged for exactly this reason** — it is a second distribution grind on
  Hooman's weakest axis and directly competes with CutLog for hours. Only pursue if Gate 1
  produces a rare validated niche and no acquisition is available.

---

## 8. Bottom line

Pursue this **only via acquisition (Track A)**, treating capital as the substitute for the
distribution muscle Hooman lacks and the hours CutLog already owns. Do not build a from-scratch
UniFi/n8n host. Gate every dollar behind verified paying demand. Plan to $2–8K/mo net in 12–24
months, delegated to a contractor, with CutLog remaining the primary venture. If Gate 0 or Gate 1
fails cheaply, walk away — the low downside is the whole reason this idea survived at all.
