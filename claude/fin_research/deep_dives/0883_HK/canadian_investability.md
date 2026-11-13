# CNOOC Ltd (0883.HK) — Can a CANADIAN legally invest? (US CMIC sanctions re-examined)

Prepared 2026-07-03 by Claude (Opus 4.8). Owner: Hooman Shariati.
**This is general regulatory information, NOT legal advice.** Confirm with your broker and,
if the position is material, a sanctions/securities lawyer before acting.

Companion to `deep_dive.md` (which concluded UN-INVESTABLE **for a US person**). This file
re-examines the same blocker on the corrected premise that the investor is a **Canadian
citizen** (not necessarily a US citizen or US green-card holder).

Confidence tags: **VERIFIED** = primary source pulled/quoted; **ASSUMED** = my legal
reasoning/derivation from the primary text; **UNVERIFIED** = could not confirm from a
primary source.

---

## BOTTOM LINE

**A Canadian citizen who is NOT a "U.S. person" — i.e. not a US citizen, not a US
lawful-permanent-resident (green-card) holder, and who transacts from outside the United
States through a non-US broker — is NOT bound by the EO 13959 / NS-CMIC prohibition. That
prohibition, by its own terms, restricts only "U.S. persons." So as a matter of *US sanctions
law*, such a Canadian may legally buy and hold CNOOC (0883.HK).** [VERIFIED that the
prohibition is limited to US persons and that the definition excludes a non-resident foreign
national; the *application to Hooman's specific facts* is ASSUMED pending confirmation of the
three switches below.]

**Canada does NOT prohibit it.** CNOOC is not on any Canadian sanctions list, and Canada has
no CMIC-style investment ban on Chinese military-linked securities. [VERIFIED]

**Three switches that would flip the US-law answer back to "prohibited," and one that does not:**
- 🚩 **Green card** — if he holds US lawful permanent residence, he IS a US person → prohibited. [VERIFIED definition]
- 🚩 **Physical presence in the US at the time of the transaction** — "any person in the United
  States" is a US person for the duration of that presence → the specific transaction would be
  prohibited. [VERIFIED definition; ASSUMED as applied]
- 🚩 **US broker / US-organized entity** — routing the trade through a US-organized brokerage
  (or its US branch) can pull a US person into the transaction chain. Non-US brokerage is the
  clean path. [ASSUMED from regulation + FAQs]
- ✅ **Merely working for a US company (Adobe)** does NOT make him a US person. Employment is
  not one of the four prongs. [VERIFIED — definition is citizenship/residence/entity/presence, not employer]

**Practical reality:** whether he can actually *press buy* depends on the broker. Many
brokers apply blanket CMIC-security blocks as firm-wide compliance policy even for non-US
clients. So "legally permitted" ≠ "your broker will let you." [ASSUMED — see Point 5.]

---

## POINT 1 — Is CNOOC still on the OFAC NS-CMIC list? → YES. **[VERIFIED]**

**Source (primary, pulled live 2026-07-03):** OFAC Consolidated Sanctions List data file
`https://www.treasury.gov/ofac/downloads/consolidated/cons_prim.csv` (and cross-confirmed in
`consolidated.xml`). File **Publish_Date = 01/08/2026** (the most recent OFAC publication),
Record_Count 442; fetched live 2026-07-03 (HTTP `date: Fri, 03 Jul 2026`).

**Exact entry (verbatim from the file):**
> `30926,"CNOOC LIMITED",-0- ,"CMIC-EO13959",... Equity Ticker 00883 HK; alt. Equity Ticker CNU CA;
> alt. Equity Ticker NC2B DE; alt. Equity Ticker CEO US; Issuer Name CNOOC Limited; alt. Issuer Name
> CNOOC Ltd; ISIN HK0883013259; alt. ISIN US1261321095; ... Target Type Public Company;
> Effective Date (CMIC) 02 Aug 2021; Purchase/Sales For Divestment Date (CMIC) 03 Jun 2022;
> Listing Date (CMIC) 03 Jun 2021; ... Legal Entity Number 549300XIVJCBIGMRUD48;
> Linked To: CHINA NATIONAL OFFSHORE OIL CORPORATION.`

- **Listed name:** `CNOOC LIMITED`; **OFAC entity ID 30926**; **program tag `CMIC-EO13959`**.
- **The Hong Kong 0883 listing is explicitly covered** — Equity Ticker `00883 HK` and
  **ISIN `HK0883013259`** are the identifiers in the entry. (The old NYSE ADR `CEO US` /
  `US1261321095` is also listed.) So the ban attaches to the exact security in question.
- **Effective Date (CMIC): 02 Aug 2021**; the 365-day divestment window for US persons
  ended **03 Jun 2022**. Both long past.
- **Status:** present on the current (Jan-8-2026-published) list. The regime (EO 13959 as
  amended by EO 14032, codified at 31 CFR part 586) remains in force. [VERIFIED — still listed;
  no lifting found.]

---

## POINT 2 — OFAC's exact definition of "U.S. person" under CMIC → four prongs. **[VERIFIED]**

**Source (primary):** eCFR, 31 CFR part 586 (Chinese Military-Industrial Complex Sanctions
Regulations), **§ 586.307** (definitions). Fetched 2026-07-03 via
`https://www.ecfr.gov/current/title-31/subtitle-B/chapter-V/part-586` (raw eCFR redirected;
retrieved through the r.jina.ai proxy).

**Verbatim definition (§ 586.307):**
> "**United States person** or **U.S. person** means any United States citizen, lawful permanent
> resident alien, entity organized under the laws of the United States or any jurisdiction
> within the United States (including foreign branches), or any person in the United States."

**The four prongs, confirmed:**
1. any **United States citizen**;
2. any **lawful permanent resident alien** (green-card holder);
3. any **entity organized under the laws of the United States** or any US jurisdiction
   (**including foreign branches**);
4. **any person in the United States** (i.e., physically present, regardless of nationality).

**Prohibition — § 586.201:**
> "All transactions prohibited pursuant to Executive Order 13959 of November 12, 2020, as
> amended by Executive Order 14032 of June 3, 2021, are prohibited pursuant to this part."

The underlying EOs prohibit **U.S. persons** from the **purchase or sale of any publicly
traded securities** (and securities that are derivative of, or designed to provide investment
exposure to, such securities) of a listed CMIC company. [VERIFIED via §586.201 + EO text; the
"ADR/ETF/derivative/index-fund" reach is covered in OFAC FAQs, consistent with `deep_dive.md`.]

---

## POINT 3 — Does the prohibition reach a NON-US person (Canadian abroad, non-US broker)? → NO. **[VERIFIED that it is US-person-limited; ASSUMED as applied]**

The prohibition binds only **U.S. persons** as defined in §586.307. A Canadian citizen who is
**not** a US citizen, **not** a US green-card holder, is **not** an entity, and is **not
physically in the United States** at the time of the transaction falls under **none** of the
four prongs → **not a U.S. person → not subject to the EO 13959 / CMIC purchase prohibition.**
[VERIFIED from the definition text.]

Key nuances:
- **"Any person in the United States" (prong 4)** is about **physical presence at the time of
  the transaction**, not nationality. A foreign national physically in the US when they
  transact is treated as a US person for that transaction. So a Canadian who buys 0883.HK
  **while sitting in the US** would, on the face of the rule, be transacting as a "person in
  the United States." → **Do the buy from outside the US.** [VERIFIED definition; ASSUMED as
  applied — OFAC has not, to my knowledge, published a bright-line FAQ on a foreign tourist's
  brokerage trade, so treat this conservatively.]
- **US broker / US infrastructure.** OFAC FAQs make clear that *non-US persons* are generally
  not prohibited from these transactions, and that **securities exchanges operated by US
  persons** and **US persons providing brokerage/advisory services to a non-US person** are
  permitted *so long as the underlying purchase/sale would not otherwise violate EO 13959*
  (**FAQ 871, 902, 903**, ofac.treasury.gov/faqs/topic/5671, fetched 2026-07-03). Practically,
  though, the cleanest position for a non-US person is to use a **non-US broker** and avoid a
  US-organized entity in the chain — a US-organized brokerage is itself a "U.S. person"
  (prong 3) and would have its own compliance obligations that typically manifest as a block.
  [FAQ existence VERIFIED; "use a non-US broker to stay clean" is ASSUMED best-practice.]
- **Working for a US company does NOT make you a US person.** Employer is not a prong. A
  Canadian employed by Adobe is not thereby a US person. [VERIFIED from definition.]

**Conclusion:** Under US sanctions law, a Canadian-citizen non-resident, transacting outside
the US via a non-US broker, is **outside the scope** of the CMIC prohibition and may lawfully
buy/hold CNOOC 0883.HK. [VERIFIED at the legal-scope level.]

---

## POINT 4 — Does CANADA restrict CNOOC? → NO. **[VERIFIED]**

**Sources (primary, fetched 2026-07-03 via r.jina.ai proxy):**
- Global Affairs Canada "Current sanctions imposed by Canada"
  (`international.gc.ca/.../sanctions/current-actuelles.aspx`).
- The **Special Economic Measures (People's Republic of China) Regulations, SOR/2021-49**
  (`laws.justice.gc.ca/eng/regulations/SOR-2021-49/FullText.html`) and the GAC China page
  (`international.gc.ca/.../sanctions/china-chine.aspx`).

**Findings:**
- Canada **does** have a China sanctions regime — but it is a **targeted human-rights regime**
  under **SEMA (SOR/2021-49, registered 21 Mar 2021)**, aimed at **Xinjiang/Uyghur, Tibetan,
  and Falun Gong** repression. [VERIFIED]
- The **entire schedule** is a short list of **named individuals plus one entity**:
  individuals ZHU Hailun, WANG Junzheng, WANG Mingshan, CHEN Mingguo, CHEN Quanguo, TUNIYAZ
  Erkin, ZAKIR Shohrat, PENG Jiarui, WU Yingjie, ZHANG Hongbo, HUO Liujun, YOU Quan (with
  further individuals added 9 Dec 2024), plus the entity **Xinjiang Production and
  Construction Corps Public Security Bureau**. [VERIFIED]
- **CNOOC is NOT listed** anywhere in the Canadian schedule. **No oil/energy company is
  listed.** [VERIFIED]
- Canada has **no CMIC-equivalent securities-investment ban** — there is no Canadian list that
  prohibits residents from *investing in* Chinese military-linked companies the way the US
  NS-CMIC list does. The SEMA China measures are asset-freeze / dealings-prohibition targeting
  specific named persons, not a market-access/securities restriction. [VERIFIED — none found in
  the primary sources; a comprehensive sweep of every Canadian instrument was not performed, so
  the "no equivalent exists" claim is VERIFIED-for-the-China-regime but broadly ASSUMED.]

**Conclusion:** From the Canadian side there is **no legal barrier** to a Canadian investing
in CNOOC 0883.HK. [VERIFIED for the SEMA China regime.]

---

## POINT 5 — Practical brokerage reality → "depends on the broker." **[ASSUMED]**

Legal permission and brokerage permission are different things.

- Many international brokers apply **firm-wide compliance blocks on all NS-CMIC-listed
  securities**, extended to *all* clients (including non-US persons), because it is simpler
  than per-client screening, and because US-affiliated groups (e.g. a global broker with US
  entities/US clearing) apply the strictest common standard across the group. So a Canadian
  client can hit a hard "cannot trade this security" block that is **policy, not law**.
  [ASSUMED — reasoned from how sanctions compliance is operationalized; I could **not** pull a
  specific broker's public policy page from primary sources in this environment. UNVERIFIED as
  to any *named* broker.]
- Whether **IBKR Canada**, a Canadian bank brokerage (RBC DI, TD DI, etc.), or another
  international broker will let a Canadian resident buy `0883.HK` is **broker-specific** and can
  change over time. The security trades freely on HKEX; the constraint is the intermediary's
  compliance posture, not Hong Kong market access. [ASSUMED; UNVERIFIED per broker.]
- **Actionable test:** ask the broker directly, *"Can I, as a Canadian resident and non-US
  person, buy and hold `0883.HK` / ISIN `HK0883013259` (CNOOC Ltd)?"* Their answer is the real
  gating factor. A broker without US-person entanglement and without a blanket CMIC block is
  the path that works.

---

## WHAT THIS MEANS / WHAT TO CONFIRM

**Net:** The `deep_dive.md` "UN-INVESTABLE" verdict was correct **for a US person** but does
**not** automatically apply to a Canadian citizen. On the corrected premise, **there is no
US-law or Canadian-law prohibition** on a non-US-person Canadian, transacting abroad through a
non-US broker, buying and holding CNOOC 0883.HK. The company's investment case in `deep_dive.md`
(deeply cheap, high-quality, low-cost, net-cash, growing) therefore becomes **live again** for
this investor — subject to the confirmations below.

**Confirm before acting (each of these can flip the answer):**
1. **Green card?** If the investor holds US lawful permanent residence, he **is** a US person
   → CNOOC is prohibited. (Must be a clean "no.")
2. **Physical presence?** Do the transaction from **outside the United States**. Buying while
   physically in the US risks falling under the "any person in the United States" prong.
3. **Broker path?** Use a **non-US broker** and avoid a US-organized entity in the chain. Then
   ask that broker in writing whether it will execute `0883.HK` for a Canadian non-US client
   (many block CMIC securities as policy regardless of law).
4. **Ongoing status?** The NS-CMIC list is updated by OFAC; re-check CNOOC's presence and any
   regime changes at time of trade (list re-pullable from the OFAC consolidated data files).

**Confidence:** HIGH that (a) CNOOC is still NS-CMIC-listed [VERIFIED, live pull], (b) the
prohibition binds only US persons per the four-prong §586.307 definition [VERIFIED], and (c)
Canada does not restrict CNOOC [VERIFIED for the SEMA China regime]. MEDIUM/ASSUMED on the
application of the "person in the United States" and US-broker nuances to specific facts.
UNVERIFIED: any *named* broker's actual policy on trading 0883.HK for Canadian clients.

**This is general regulatory information, not legal advice.** For a material position, confirm
with the broker and a sanctions/securities lawyer.

---

### Sources (all fetched 2026-07-03)
- OFAC Consolidated Sanctions List (primary data): `cons_prim.csv` / `consolidated.xml`,
  `www.treasury.gov/ofac/downloads/consolidated/` — **Publish_Date 01/08/2026**; CNOOC LIMITED,
  entity 30926, program `CMIC-EO13959`, ISIN HK0883013259.
- 31 CFR part 586, §586.307 (definition of U.S. person) & §586.201 (prohibitions) — eCFR,
  `ecfr.gov/current/title-31/subtitle-B/chapter-V/part-586` (via r.jina.ai proxy).
- OFAC CMIC FAQs (topic 5671), FAQ 871 / 902 / 903 — `ofac.treasury.gov/faqs/topic/5671`.
- Global Affairs Canada, current sanctions & China page — `international.gc.ca/.../sanctions/`.
- Special Economic Measures (People's Republic of China) Regulations, SOR/2021-49 —
  `laws.justice.gc.ca/eng/regulations/SOR-2021-49/FullText.html`.
