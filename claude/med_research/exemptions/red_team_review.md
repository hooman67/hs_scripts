# Stage 5 — Adversarial Red-Team Review of the Recommended Path

**What this is:** a deliberate attempt to BREAK `exemptions/recommended_path.md` and the
`exemptions/decision_map.md` it rests on. Job: find where the plan triggers an RFE or denial, which
load-bearing claims rest on UNVERIFIED/ASSUMED facts, where the religious-waiver sincerity story is
attackable, which contraindications are temporary and could expire before adjudication, and — the
single most important question — **where a well-meaning doctor's note or form entry could constitute
misrepresentation.**

**Author:** Claude (Opus 4.8, red-team subagent) · **Date:** 2026-07-08 · **Status:** Stage-5.
**Live re-verification this session:** CDC civil-surgeon TI + CDC Pinkbook Ch.2 fetched directly
(HTTP 200); USCIS PM Vol.8 Pt.B Ch.9 and Form I-693 page read via r.jina.ai proxy (uscis.gov 403s the
bot, as upstream noted). See §12 for what I confirmed vs. could not.

> ⚠️ NOT legal or medical advice. This is decision-support for BAL and a physician. Its purpose is to
> stress-test, not to file anything.
>
> ⚠️ GUARDRAIL restated: every attack below is in service of keeping the plan **truthful**. The
> failure modes I flag are almost all failure modes where the plan, as written, could pressure a
> clinician or the applicant toward a statement that is not literally true. That pressure — not the
> vaccine — is the real hazard.

---

## 0. Verdict in one paragraph

The upstream work is strong, honestly hedged, and correct on the big structural facts (COVID gone;
titers/records and contraindication are self-executing; Td/Tdap is the real pinch point; the religious
waiver is a trap). **But the plan systematically OVERSTATES one door and UNDERSTATES two risks, and
those errors compound at exactly the guardrail seam.** The overstatement: **H3-Hooman (LGL →
live-vaccine contraindication) is presented as a near-certain backstop** ("guarantees he never needs a
live shot even if a titer fails"). It is not near-certain — it hinges on a clinical determination
("*severe* immunosuppression / altered immunocompetence") that, given how LGL leukemia is actually
managed (often watchful-waiting or *low-dose* immunosuppressants), **a truthful hematologist may
decline to make.** The understatements: (1) that same LGL/immunosuppression could **flip pneumococcal
(and possibly meningococcal) from "auto-cleared, not age-appropriate" into REQUIRED** — a door that
boomerangs into two new inactivated shots the plan assumed away; and (2) the realistic base case is
**one Td/Tdap shot each**, not "plausibly zero shots." The most dangerous consequence is that
presenting H3-H as a reliable backstop creates demand for a contraindication note the facts may not
support — the exact misrepresentation trap the project exists to avoid. Fixes in §11.

---

## 1. 🔴 CRITICAL — H3-Hooman is overstated; the "severe immunosuppression" bar is the real gate, and LGL may not clear it

**What the plan says (attackable):**
- decision_map §4 Step 4 / recommended_path §1.2 Step 4: the LGL contraindication is "what **guarantees
  he never needs a *live* shot even if a titer fails.**"
- Scorecard rates H3 at **4.8**, "co-lead," with the only caveat being "must be genuine physician
  judgment."
- The upstream contraindication file (1c §2a) leans on the Pinkbook naming "**leukemia, lymphoma**,"
  implying LGL — being a leukemia — falls inside the named category.

**Why it breaks:**
1. **The governing standard is "SEVERE immunosuppression," a HIGH-level bar — not "has a leukemia."**
   CDC Pinkbook Ch.2, read live this session, verbatim: *"Live vaccines should usually not be
   administered to **severely** immunosuppressed persons with congenital immunodeficiency, leukemia,
   lymphoma, or generalized malignancy."* The operative word is **severely**. The "leukemia/lymphoma"
   list historically targets patients on **active cytotoxic chemotherapy for acute leukemia** — not an
   indolent, chronic condition. **[VERIFIED — Pinkbook Ch.2, 2026-07-08]**
2. **LGL leukemia is clinically the opposite of that archetype.** Large Granular Lymphocytic leukemia
   is a **chronic, indolent** lymphoproliferative disorder. A large share of patients are managed by
   **watchful waiting (no treatment)**, and first-line therapy when needed is typically **LOW-DOSE
   immunosuppression** — low-dose methotrexate, low-dose cyclophosphamide, or cyclosporine — not
   high-dose cytotoxic chemo. **[ASSUMED-HIGH — standard hematology; not a primary-source citation of
   record. FLAG: confirm Hooman's actual disease status and regimen with his hematologist.]**
3. **CDC/ACIP explicitly carves LOW-level immunosuppression OUT of the contraindication.** The Pinkbook
   sets the steroid threshold at *"20 mg or more of prednisone daily … for 14 days or longer"* to
   avoid live vaccines — **implicitly, lower doses are not a contraindication.** ACIP's altered-
   immunocompetence guidance similarly treats low-dose methotrexate (commonly cited ≤0.4 mg/kg/week)
   and low-dose steroids as **low-level** immunosuppression that does **not** contraindicate MMR/
   varicella. **[VERIFIED that low-dose steroids are excluded — Pinkbook Ch.2; the specific
   methotrexate/ACIP low-vs-high thresholds I could NOT pull to a primary source this session — see
   §12. Treat the MTX number as UNVERIFIED.]**
4. **Therefore the honest clinical answer may be "live vaccines are NOT contraindicated for him."** If
   Hooman is on watchful-waiting, or on low-dose methotrexate/cyclosporine with preserved counts, a
   truthful hematologist could well conclude he is **not** severely immunosuppressed and decline to
   certify a contraindication. In that case **H3-H is simply unavailable** — and the plan's promise
   that it "guarantees he never needs a live shot" is false. His live rows would then rest **entirely
   on titers (H2)**, which for a man who has "had various vaccines over his life" is likely to succeed
   — but that is the actual backstop, not H3-H.

**Impact:** the plan's confidence that Hooman clears MMR/varicella "two ways" is really "one likely way
(titers) plus a contingent, possibly-unavailable second way." Not fatal — but the scorecard's 4.8 and
the word "guarantees" are wrong for *his* facts. **The door is real in law; its availability to Hooman
is a genuine open clinical question, not a near-certainty.**

**Guardrail consequence (this is the dangerous part):** because the plan tells Hooman this door
"guarantees" no live shot, it manufactures an expectation. If titers then come back non-immune and the
hematologist says "you're not severely immunosuppressed, I can't call it contraindicated," there is
direct pressure to get *some* doctor to write the note anyway. **That is the (a)(6)(C)(i) trap.** See §7.

---

## 2. 🔴 CRITICAL — the immunosuppression door could BOOMERANG: LGL may make pneumococcal (and possibly meningococcal) REQUIRED, not auto-cleared

**What the plan says (attackable):** Step 1 for both spouses "auto-clears" meningococcal and
pneumococcal as **"not age-appropriate"** for "a typical healthy adult," with the only hedge being
"confirm the exact age band." The plan flags the adult *age* cut-offs as UNVERIFIED but treats the
outcome as basically settled.

**Why it breaks:** the required list is age- **AND RISK-** based (CDC "Table 1 — Vaccine Requirements
According to Applicant Age" + ACIP risk conditions). **ACIP recommends pneumococcal vaccination for
immunocompromised adults of any age**, and meningococcal vaccination for specific risk groups
(complement deficiency, asplenia, certain conditions). **The very LGL/immunosuppression argument the
plan uses to contraindicate LIVE vaccines is precisely the kind of risk factor that can make
pneumococcal — an INACTIVATED vaccine — age/risk-*appropriate*, i.e., REQUIRED.** If the civil surgeon,
looking at the hematologist letter that establishes immunosuppression, then cannot mark pneumococcal
"not age-appropriate" (because for an immunocompromised person it *is* appropriate), Hooman could face
**one or two inactivated shots the plan assumed away** — and there is **no titer and no contraindication
door** for them. **[ASSUMED — direct application of ACIP risk-based logic; whether the CDC civil-surgeon
Technical Instructions actually import risk-based pneumococcal/meningococcal recommendations for
immigration purposes is UNVERIFIED and must be pinned. See §12.]**

**Impact:** the two vaccines the plan is most relaxed about ("confidently clearable, no shot") are the
two most exposed to Hooman's own medical argument. This is an internal contradiction the upstream stages
missed entirely: **you cannot simultaneously assume "healthy adult → pneumococcal not appropriate" and
"immunocompromised adult → live vaccines contraindicated."** Pick one; the truthful picture is that
establishing immunosuppression for the live rows may *open* the pneumococcal/meningococcal rows.

---

## 3. 🟠 HIGH — contraindication temporariness vs. the exam-date assessment (the door can be shut at the moment it's needed)

**What the plan says:** the contraindication is "assessed as of the exam date" and USCIS "will never
later require" the waived vaccines — framed as making the door "effectively permanent for this
application." True as far as it goes.

**Why it breaks:** the durability protection only attaches **if a genuine contraindication exists AT THE
EXAM DATE.** Two temporal failure modes the plan underweights:
1. **Hooman's immunosuppression may have paused.** Pinkbook Ch.2, verbatim this session: *"Live vaccines
   can be administered after chemotherapy or radiation therapy has been discontinued for at least 3
   months."* If Hooman is between treatment courses, or on watchful-waiting, then **on the exam date he
   may not be immunosuppressed at all** — the contraindication doesn't exist to be marked, regardless of
   the durability rule. The plan says immunosuppression "may pause"; it does not connect that to the
   fact that the pause could coincide with the exam and **close the door precisely when needed.**
   **[VERIFIED rule — Pinkbook; application depends on his treatment timeline.]**
2. **The wife's pregnancy is a hard clock (see §8).**

**Impact:** "durable" is conditional on "genuine at exam." For Hooman this is another reason H2 (titers),
which is truly permanent and timing-independent, must be the **primary** door for his live rows, with
H3-H as a fallback that may or may not be open — the reverse of how "backstop" is currently framed.

---

## 4. 🟠 HIGH — officer deference to a contraindication is "usually," not absolute; an active hematologic dx invites the Ch.4 re-exam discretion

**What the plan says:** the officer "should usually defer" to a contraindication because it is medical
judgment; and PM Ch.4's discretion to demand an updated I-693 "cuts toward more medical scrutiny, not
toward forcing vaccines."

**Why it breaks:**
- "**Usually** defer" ≠ always. Deference is to *medical judgment*; it is not deference to a mark that,
  on the face of the attached records, looks like clear error. If the hematologist's letter (attached to
  the sealed form, as the plan recommends) says "LGL, watchful-waiting, normal CBC, no active treatment"
  **next to** a live-vaccine contraindication mark, an officer has a **facial inconsistency**, and the
  contraindication starts to look like the checkable-error category (like "not age-appropriate"), not
  the deferred category. That can draw an RFE. **[ASSUMED — reasoned from the PM's own defer-vs-check
  distinction; not a quoted denial pattern.]**
- PM Ch.4 gives USCIS discretion to demand a new/updated I-693 when it "has reason to believe the
  applicant's medical condition has changed" or that the form "does not accurately reflect" it. An
  **active, documented hematologic diagnosis** is exactly the profile that can trigger this — and a
  re-exam months later, when Hooman may be in a treatment pause, could find **no contraindication**,
  reopening the live rows. **[VERIFIED that the discretion exists — PM Ch.4, upstream; the risk
  application is my inference.]**

**Impact:** the plan's "attach the hematologist letter" advice is double-edged. If the letter genuinely
establishes *severe* immunosuppression, it helps. If it establishes only a chronic indolent condition,
it can **undercut** the very contraindication it's meant to support. This must be surfaced to BAL and the
hematologist, not presented as pure upside.

---

## 5. 🟠 HIGH — "plausibly zero shots" is optimistic framing; the honest base case is ≥1 Td/Tdap each

**What the plan says:** headline — "**both can plausibly reach zero new shots**"; Td/Tdap is the "most
probable single unavoidable shot" only "if their last dose is stale."

**Why it breaks:** the 10-year Td/Tdap booster clock combined with typical adult behavior means a
**documented dose within 10 years is the exception, not the rule**, for many adults — and it must be
*documented with m/d/y*, unaltered, not self-reported. For two adults, the probability that **at least
one** lacks a qualifying dated Td/Tdap record is high. There is **no titer, no contraindication
(inactivated), and no honest religious door** for it. So the realistic modal outcome is **one Td/Tdap
shot each**, and "zero shots" is the optimistic tail, not the base case.

**Impact:** not a legal error — the plan *does* flag Td/Tdap honestly in the body. But leading the
headline and the one-paragraph bottom line with "plausibly zero" sets an expectation that, when it
fails, is exactly what tempts a workaround (an insincere religious objection, or a fabricated
individual contraindication). **Reframe the headline to "expect ~1 Td/Tdap each unless a dated dose
<10 yr exists; everything else is very likely clearable truthfully."** This is both more accurate and
safer.

---

## 6. 🟡 MEDIUM — Hep A / Hep B / polio titer optimism rests on UNVERIFIED per-person immunity

**What the plan says:** titers "very likely" clear MMR, varicella, Hep A/B, polio, given "various
vaccines over his life."

**Why it breaks (fact-dependent, and the facts aren't in):**
- **Hep A:** not part of routine childhood vaccination for adults of Hooman's/his wife's generation in
  many countries; a foreign-born adult may have **neither vaccination nor natural immunity** → negative
  titer + no record → **shot, no fallback** (inactivated).
- **Hep B:** the immunity marker is **anti-HBs**, which **wanes over time even in successfully
  vaccinated people.** A person vaccinated in childhood can titer **negative** now (anamnestic memory
  intact but no measurable titer) — so a negative anti-HBs does **not** disprove prior vaccination, but
  the *civil-surgeon door* still needs either a positive titer **or** a dated record. If the childhood
  record is lost and the titer has waned, the truthful outcome is a shot (or a documented challenge-dose
  series). **[VERIFIED that anti-HBs is the marker per upstream; waning is standard immunology,
  ASSUMED-HIGH.]**
- **Polio:** the titer must cover **all three types**; US-born adults frequently lack both titers and
  dated records. **[VERIFIED — CDC "all three poliovirus types," this session.]**

**Impact:** the plan flags these as fact-dependent (good), but the *overall* "realistically 0 shots"
conclusion silently assumes favorable titers for all of them. That assumption is **UNVERIFIED for these
two specific people** and should not drive the headline. The honest statement: "0 shots is achievable
*if* titers/records come back favorable on Hep A, Hep B (anti-HBs), and polio — which is unknown until
tested."

---

## 7. 🔴 CRITICAL — the "well-meaning doctor's note" misrepresentation seam (the tasked question, answered)

**Where a truthful-looking form entry could actually be a material misrepresentation:**

1. **The LGL contraindication note (the sharpest seam).** Scenario: titers on MMR come back non-immune;
   Hooman asks his hematologist for a letter; the hematologist, wanting to spare his patient a shot and
   seeing "leukemia" in the guidance, writes *"live vaccines are contraindicated due to LGL leukemia"* —
   **even though Hooman is on watchful-waiting / low-dose therapy and is not, in the physician's honest
   clinical judgment, severely immunosuppressed.** That note, transcribed onto the I-693 and relied on by
   USCIS, is a **false statement of a material fact** → INA 212(a)(6)(C)(i), which (per 1e §3.7) is
   **realistically unwaivable for Hooman.** The note *looks* routine and helpful; that is exactly why it
   is dangerous. **The plan's own framing ("guarantees no live shot") is what generates the request for
   this note.** This is the #1 finding of this review.
   - **Mitigation the plan must adopt:** the hematologist must be asked the **neutral clinical question**
     — *"Is Hooman severely immunosuppressed such that live vaccines are contraindicated?"* — **not** the
     leading, outcome-driven question *"Will you write that live vaccines are contraindicated so he can
     avoid the shot?"* If the honest answer is no, the door is closed and titers/one shot is the path.
     recommended_path §3.1 mostly does this, but the surrounding "guarantee/backstop" language pulls the
     other way and must be softened (§11).

2. **The pregnancy note is much safer but has one seam:** it is objectively true or false (she is or
   isn't pregnant at exam). The only misrepresentation risk is a **stale or forward-dated** pregnancy
   attestation — e.g., an exam done post-partum but documented as "pregnant." The sealed-envelope +
   tamper rule (3a §4) is USCIS's detector. Keep her exam genuinely during pregnancy; do not paper over
   timing.

3. **Record "reconstruction."** The plan correctly says undated/self-reported/altered records are
   rejected. The seam: a family member or a foreign clinic "reconstructing" a lost childhood card from
   memory and dating it. That is a fabricated record = misrepresentation. The plan says this; keep it
   loud.

4. **Varicella "VH" (disease history).** The one place CDC accepts an **oral** history. Seam: coaching a
   "yes I had chickenpox" that isn't a genuine recollection to dodge a titer/shot. It must be a real
   history the surgeon judges reliable (epidemiologic link or prior lab confirmation), not a scripted
   answer. Low stakes but worth a line.

5. **The religious/moral objection** — covered in §9; an insincere or reverse-engineered categorical
   objection is itself an adjudicated misrepresentation.

**Net on the tasked question:** the plan is *mostly* well-guarded, but its optimism about H3-H creates
the pressure that turns seam #1 from theoretical into likely. **Fixing the framing (§11) is the single
most important safety change in this review.**

---

## 8. 🟠 HIGH — the wife's plan is a single point of failure on pregnancy timing

**What the plan says:** do her exam "while she is still pregnant" to capture the live-vaccine
contraindication; "run titers anyway" as the durable route.

**Why it breaks / needs sharpening:**
- The pregnancy door is a **hard biological clock.** If the exam isn't scheduled before delivery — or
  if there is a pregnancy loss, or the pregnancy is already late-term as of 2026-07 and BAL's scheduling
  slips — the door **closes**, and she falls back to titers she may not have run yet.
- The plan in places treats pregnancy contraindication as the lead door for her live rows and titers as
  a "backstop." **That ordering is backwards on durability.** Titers are permanent, timing-independent,
  and immune to all of the above. **Recommendation: make titers her PRIMARY door for MMR/varicella and
  pregnancy the backstop** — the opposite of some of the plan's phrasing. If her titers are positive
  (likely, given a normal vaccination history), the pregnancy-timing scramble becomes irrelevant.
- **The pregnancy door does NOTHING for her inactivated pinch points** (Td/Tdap especially — Tdap is
  *recommended* every pregnancy, so pregnancy is the opposite of a contraindication). The plan says
  this; good.

**Impact:** the plan's "one timing rule dominates" framing over-centers a fragile door. The robust move
is titers-first for her.

---

## 9. 🟡 MEDIUM — religious-waiver sincerity: correctly demoted, but the residual trap should be stated harder

The upstream analysis of H4 is good and I do not overturn it. Two sharpenings:
- **Hooman's actual stated reason is affirmatively self-defeating for H4, not merely weak.** His
  objection is explicitly **causal/health-based** ("the COVID vaccine caused my LGL"). Putting *that*
  reasoning into a sworn I-601 statement doesn't just fail the "any form" test at Step 3 — it
  **documents, in his own words, a single-vaccine safety objection**, which is the textbook "pick and
  choose." Attempting H4 with his real reasons is worse than not attempting it. The plan says "reserve
  only"; it should say **"do not attempt with his stated reasons — doing so is both a near-certain denial
  and a sincerity/misrepresentation exposure."**
- **The sincerity gate is itself an adjudicated misrepresentation surface.** A belief "framed so as to
  gain the legal remedy" is what USCIS screens for. So a *coached* categorical objection is not a safe
  fallback for the Td/Tdap gap — it is a second (a)(6)(C) risk. The plan's advice ("take the one shot
  rather than a discretionary/insincere waiver") is correct and should be the firm rule.

**No change to the ranking; strengthen the warning.**

---

## 10. 🟡 MEDIUM — source freshness, access channel, and a date discrepancy

- **Everything USCIS was read via Wayback/r.jina.ai proxy, never the live site** (uscis.gov 403s the
  bot — I re-confirmed the 403 this session). The *content* is the official text, but a proxy/snapshot
  is a lead that ages. **Re-verify live near the exam date**, in a normal browser, via BAL.
- **Date discrepancy to resolve:** upstream repeatedly cites the PM Ch.9 page as **"Current as of May
  08, 2026."** My r.jina.ai fetch this session surfaced a **"2025-05-13"** date (the COVID Technical
  Update / publish date). These are likely different fields (publish/update vs. "current as of"), not a
  contradiction — but it means at least one agent may have read a differently-stamped capture.
  **Confirm the live "Current as of" date before relying on it as citation-of-record.**
- **COVID removal is a policy choice, not a statute change** (USCIS adjudication posture + CDC TI edit).
  Policy can move. It is very likely still in force, but **re-verify the COVID row and the required list
  live** before the exam — do not treat "COVID gone" as immutable just because it's favorable.
- **8 CFR 212.7 exact text was never pulled** (upstream flagged it UNVERIFIED); the I-601 fee and current
  edition were never cleanly read. Only relevant if H4 is ever touched (it should not be).

---

## 11. Required changes to the recommended path (what to fix before Hooman relies on it)

1. **Downgrade H3-Hooman from "guarantee/backstop/4.8 co-lead" to "contingent, possibly unavailable."**
   Make **titers (H2) the primary door for his live rows**; H3-H is a fallback that exists **only if his
   hematologist independently judges *severe* immunosuppression.** Delete the word "guarantees."
2. **Add the pneumococcal/meningococcal boomerang** (§2) as an open risk: establishing immunosuppression
   may make these inactivated vaccines *required* rather than auto-cleared. Route to the civil surgeon +
   CDC Table 1 + ACIP risk conditions to verify before assuming they fall away.
3. **Reframe the headline** from "plausibly zero shots" to "**expect ~1 Td/Tdap each unless a dated dose
   <10 yr exists; the rest is very likely clearable truthfully, pending titer results.**"
4. **Flip the wife's ordering:** titers PRIMARY for MMR/varicella, pregnancy contraindication the
   backstop — so her case doesn't hinge on the pregnancy clock.
5. **Rewrite the hematologist ask as a strictly neutral clinical question** (§7 mitigation) and remove
   any framing that presupposes the answer is "contraindicated."
6. **State the H4 warning harder** (§9): do not attempt with his stated reasons.
7. **Add "re-verify live" as a hard gate**, and resolve the "Current as of" date (§10).

None of these change the fundamental strategy (records → titers → genuine contraindication → shot last);
they correct over-confidence that, left as-is, points a well-meaning clinician at the misrepresentation
line.

---

## 12. What I verified live vs. could NOT — the re-verify list

**VERIFIED live this session (2026-07-08):**
- CDC 15-disease required list; **COVID-19 not on it**; titer-eligible diseases (MMR, Hep A, Hep B,
  polio [all 3 types], varicella); refusal-documentation language; "contraindication = life-threatening
  problem" framing. — CDC civil-surgeon TI, direct fetch, "Last Updated Mar. 11, 2025." ✅
- Pinkbook Ch.2: **"severely** immunosuppressed" is the bar; leukemia/lymphoma named **in that severe
  context**; **live vaccines OK ≥3 months after chemo ends**; **inactivated vaccines safe in
  immunosuppression**; **prednisone ≥20 mg/day ≥14 days** is the steroid threshold (⇒ lower doses not a
  contraindication). — CDC Pinkbook Ch.2, direct fetch. ✅
- USCIS PM Ch.9: **never-RFE-later** rule for both immuno-compromised and no-longer-pregnant; narrow
  contraindication definition; **religious/moral box must be checked even if a blanket waiver applies,
  and both boxes may be checked.** — via r.jina.ai proxy. ✅ (but see date note, §10)
- Form I-693 **edition 01/20/25** is the only edition accepted for civil-surgeon signatures on/after
  **July 3, 2025**. — via r.jina.ai proxy. ✅

**Could NOT verify this session / still UNVERIFIED — nail these before relying:**
- **[CRITICAL] The exact ACIP low- vs high-level immunosuppression thresholds** (e.g., methotrexate
  ≤0.4 mg/kg/wk = low-level; which regimens contraindicate MMR/varicella). The ACIP altered-
  immunocompetence page I fetched returned only a nav index (404 on the imz-best-practices URL). **This
  is the hinge of §1 — pin it to the primary ACIP/MMWR source, and match it to Hooman's actual
  regimen with his hematologist.**
- **[CRITICAL] Whether the CDC civil-surgeon Technical Instructions import ACIP RISK-based
  pneumococcal/meningococcal recommendations** (i.e., whether immunosuppression makes these
  *required* for immigration). §2 depends on this. UNVERIFIED.
- **Adult age cut-offs, CDC "Table 1"** — still not extracted (upstream flagged; I could not either).
- **Hooman's actual disease status/treatment** (watchful-waiting vs. active therapy; last treatment
  date vs. exam date) — determines whether H3-H is even available (§1, §3). This is a fact only his
  hematologist has.
- **Whether his wife's pregnancy timeline allows an exam while pregnant** (§8) — BAL scheduling fact.
- **Qualifying-relative status** for a hypothetical 212(i) waiver (§7 stakes) — BAL/family fact.
- **Live "Current as of" date** on PM Ch.9 and the live COVID/required-list status (§10).
- **ACIP "complete series" dose counts** per disease (record-based clearance only).

---

## 13. What upstream got RIGHT (so it isn't lost)

- COVID-19 is genuinely gone at both levels — correctly identified as the highest-value, pre-door win.
- Titers/records and genuine contraindication are self-executing (no I-601) and resolve into Results
  box #1 — correct and load-bearing.
- Td/Tdap correctly identified as the honest pinch point (inactivated, no titer, 10-yr clock).
- The religious waiver correctly demoted; the misrepresentation bar correctly identified as the one
  bright red line and (for Hooman) realistically unwaivable.
- The guardrail is threaded through every file, and the civil-surgeon red-flags list (3b §5) is exactly
  right. My critique sharpens the *calibration* of one door and surfaces two missed risks; it does not
  overturn the strategy.
