# Positioning — LinkedIn, Résumé and Application Preparation

As of: **2026-11-09**. **Status: reviewed proposal and ready-to-paste copy; no external changes made.**
This is the single canonical positioning plan. It replaces the obsolete remote-browser setup plan.

Lead with hands-on **AI infrastructure, inference and production ML systems**, with technical
leadership as evidence of IC scope. Target Senior IC and Staff/Principal; engineering-manager roles
are excluded. Hooman confirms Adobe employment, San Jose residence, and no sponsorship needed for
applications. The goal is an accepted offer around January 9, 2027; no recruiting conversations
are underway. Application assistance will start when he requests it.

## Contents

- [Priority and execution order](#priority-and-execution-order)
- [Ready-to-paste profile copy](#ready-to-paste-profile-copy)
- [Other profile and material updates](#other-profile-and-material-updates)
- [Application handoff](#application-handoff)
- [Evidence ledger](#evidence-ledger)
- [Access and remaining gaps](#access-and-remaining-gaps)
- [Public-source retrieval record](#public-source-retrieval-record)

## Priority and execution order

The public LinkedIn page still says **Vancouver, British Columbia, Canada**. Its About opening
points first to GitHub, whose profile also says **Canada**. Those are verified November 9;
headline, full About, complete Experience and private settings are masked in the signed-out view.
This is a proposed replacement for those fields, not a claim to have inspected all current text.

1. **Read the live fields on the working laptop.** Capture current headline, About, Experience,
   Skills, Featured and visibility settings. Merge useful current information into the copy below.
   Keep a pre-edit snapshot under
   `/home/colligo/hs_scripts/claude/dev_research/positioning/data/` once available; do not save cookies,
   tokens or credentials. The failed remote-browser approach is not a prerequisite.
2. **Choose visibility before making edits.** Proposed discreet default: disable network
   notifications for profile updates, and consider Open to Work → Recruiters only. LinkedIn states
   this does **not guarantee complete privacy**. Visible only to you is the alternative if that
   exposure is unacceptable. These are recommendations, not settings Hooman has selected.
3. **Correct current residence.** LinkedIn: Me → View Profile → edit intro/pencil → Location →
   United States / San Jose, California. The actual UI may derive city from country and postal
   code; use the real postal code if requested. Do not invent one. Preserve historical Vancouver
   job locations and verify the saved profile displays San Jose.
4. **Update headline, About and Adobe description.** Keep the official title and October 2023–Present
   dates. Use the copy below, merged against the current fields. Current residence and an individual
   job's work location are separate fields.
5. **Align GitHub, résumé, Skills and Featured.** Complete the small corrections below. A new public
   project is not required before applying. Inspect both signed-in and public presentation afterward.

For a future execution agent: read the current live fields immediately before editing, prepare the
exact merged changes, then obtain Hooman's explicit approval for external edits. Once a specified
batch is approved, carry it through and verify it without repeatedly asking for the same approval.
User-provided approval for a specific update takes precedence over a generic approval checklist.

## Ready-to-paste profile copy

### Headline — recommended conservative version

> Machine Learning Systems Engineer | AI Infrastructure, Inference & Evaluation | Production GenAI

Alternative with more systems emphasis:

> AI/ML Systems Engineer | Inference Platforms & Distributed ML | Research-to-Production

Both avoid implying that Adobe currently confers a Staff or Principal level. They also avoid a
public job-search announcement. Add “Staff/Principal” only as a target in recruiter-only settings or
direct outreach, not as a current title.

### About

> I’m a hands-on machine learning systems engineer and technical leader with over a decade of experience
> turning models into production systems—from real-time computer vision and latency-sensitive
> software to generative AI inference, evaluation, distributed workflows, and enterprise delivery.
>
> My Adobe work has spanned production generative-video pipelines, model integration and
> deployment, reusable inference and evaluation workflows, distributed GPU execution, and
> research-to-product technical transfer. I have also combined technical leadership with hands-on
> delivery, translating customer problems into data, model, evaluation, and production workflows.
>
> Earlier, I led computer-vision and software teams at Aupera and owned delivery from customer
> discovery and architecture through C++ implementation, deployment, and production support. My
> background also includes real-time ML systems for mining and latency-sensitive trading software.
>
> I do my best work at the boundary between model behavior and production engineering: clarifying
> the real problem, simplifying the system, measuring quality and reliability, and helping teams
> ship AI that works in practice.

“Over a decade” is supported; “12+ years” is not supported as cumulative employed time. This About
uses career-scope wording and deliberately omits named customers, internal system names, and
numerical metrics because Hooman has not selected a public-disclosure boundary.

### Adobe Experience — conservative bullets

Use this confirmed header:

> **Adobe — Machine Learning Engineer, ASML**
>
> **October 2023–Present**

Preserve the existing Experience work-location field until its accuracy is checked. Correcting
the profile residence to San Jose does not require changing historical or remote work locations.

Proposed bullets:

- Built and productionized generative-video inference pipelines spanning text-to-video,
  image-to-video, and video-to-video workflows, owning model integration, deployment, automated
  evaluation, and research-to-product technical transfer.
- Led reusable inference and evaluation workflows for foundation-model teams, including
  vLLM integration, distributed GPU execution, restartable jobs, standardized results, and training-time quality
  measurement.
- Re-architected a distributed data-loading platform to reduce coupling and operational
  complexity and support reliable multi-node model workflows.
- Combined technical leadership with hands-on delivery across enterprise AI programs, translating
  customer needs into end-to-end data, model, evaluation, and production workflows.

Do not add named customers, internal product names, “approximately 4,000 lines,” “30+ nodes,” or
other metrics until accuracy and public-disclosure permission are confirmed. vLLM is included as
a documented technology capability; no internal implementation details are disclosed.

## Other profile and material updates

| Asset | Concrete change | Status / stop condition |
|---|---|---|
| GitHub public profile | Set location to **San Jose, California, United States**. Suggested bio: “Machine learning systems engineer working on AI infrastructure, inference, evaluation, and production AI.” Use Settings → Public profile; labels may vary. | Proposed external edit. No repositories need to be made public. |
| GitHub proof links | Inspect any proposed pinned repository for relevance, a useful README, reproducibility and public-safe contents. Keep old coursework/forks if desired, but do not lead the AI-infrastructure story with an unreviewed landing page. | Public landing-page audit only; code quality was not judged. Do not build or clean every repo. |
| LinkedIn Skills | Prefer **Machine Learning, Python, System Architecture** near the top, if those exact entities are available. Include documented PyTorch, vLLM, distributed systems, Docker, Linux, C++, model deployment and evaluation experience. | Select skills Hooman can defend. CUDA/Triton/Kubernetes depth is not established merely because it is on the learning plan. |
| LinkedIn Featured / Publications | Use the verified CVPR **Workshops** paper and exact CVF URL in the source record. Consider a demo/talk/repo only after review. | Do not upload the private study platform or Adobe artifacts. The paper alone is sufficient to make this section concrete. |
| Résumé | Correct CVPR to **CVPR Workshops** and replace ambiguous “12+ years” with **over a decade**. Keep San Jose; retain the accurate Adobe title/dates. | These two local corrections are complete. The existing résumé contains customer names and internal metrics; its public-upload version still needs a disclosure review. |
| Contact details | Confirm the current non-work email and phone before submitting applications. A Canadian phone number does not imply Canadian residence and need not be changed just for appearances. | Existing contact values are preserved; no unsupported replacement invented. |
| Application/job-board accounts | On first use, align current residence, title/dates, résumé version and role targets. Add alerts for Senior/Staff/Principal AI infrastructure and inference roles with the chosen geography. | Future action when application work is requested; no new accounts created. |

Exact publication wording:
**Hooman Shariati et al., “Towards Autonomous Mining via Intelligent Excavators,” Proceedings of the
IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops, 2019, pp. 26–32.**
The primary page lists Hooman first; this does not establish his particular contribution without
his account. Do not describe the paper as a CVPR main-conference publication.

Keep one canonical résumé at
`/home/colligo/hs_scripts/claude/dev_research/positioning/HOOMAN_SHARIATI_RESUME.md`.
Tailor emphasis per role; do not create conflicting dates, titles or factual claims. General public
LinkedIn copy above intentionally excludes customer names and internal metrics. Those can be
reconsidered during review of a concrete public draft; their omission is not a judgment that the
accomplishments are weak or unusable in private interview discussion.

## Application handoff

This workflow is prepared but inactive until Hooman asks for application help. Avoid using the
entire first month for polishing; the recruiting pipeline should overlap study once the initial
materials are ready. No applications or messages have been sent.

1. **Verify a small first batch of live employer roles.** Start with roughly 8–12 relevant roles,
   deduplicate them, and record exact location/remote terms, compensation basis, required skills,
   seniority scope and retrieval date. This is a bounded starting recommendation, not a quota.
   The September research sample must not be presented as currently open jobs.
2. **Select by fit and evidence.** Use Senior/Staff/Principal AI infrastructure/inference as the
   common target; rank actual scope over title. Historical compensation and remote preferences
   remain context, not a newly agreed salary floor or a blanket rejection of local roles.
3. **Prepare each submission.** Map the strongest relevant accomplishments to the role, tailor the
   résumé, and draft a short introduction. Identify gaps honestly. Confirm actual recruiter
   questions rather than flattening “now or in the future” into the user's narrower sponsorship
   statement. No immigration category is inferred or added to public copy.
4. **Execute within the authorization Hooman gives.** If he asks for a batch of applications or
   messages, agree the concrete scope and use that authorization throughout. Otherwise keep the
   materials as drafts. Do not require approval per item if a clear batch is already authorized.
5. **Track follow-through and learning.** Record company, role URL, level, location, compensation
   basis, résumé version, contact/source, stage, next action/date and round format. Initial stages:
   shortlisted, prepared, submitted, screen, technical, final, offer, closed. Record submitted only
   after actual submission. Feed interview evidence into the next study packet.

Reusable first-person introduction (draft, not sent):

> I’m a machine learning systems engineer at Adobe, based in San Jose, with over a decade of
> experience across production AI, inference and evaluation workflows, real-time computer vision,
> and distributed systems. I’m exploring Senior IC and Staff/Principal opportunities in AI
> infrastructure and inference, where I can combine hands-on engineering with cross-team technical
> ownership. [Add one sentence connecting a specific accomplishment to this team’s problem.]

## Evidence ledger

| Claim or profile field | Status | Evidence and as-of date | Public-use boundary |
|---|---|---|---|
| Hooman lives in San Jose, California | **USER-CONFIRMED — 2026-11-09** | Current-session answer relayed by the coordinating agent. The current résumé also says San Jose. | Safe as a location fact if Hooman wants the profile location current. This does not change historical Vancouver job locations. |
| LinkedIn shows Vancouver, British Columbia, Canada | **USER-CONFIRMED + VERIFIED PUBLIC-PAGE OBSERVATION — 2026-11-09** | The public page at `https://www.linkedin.com/in/hoomanshariati/` returned the exact location and a Canadian canonical URL. | The location mismatch is confirmed. The authenticated edit field and available location choices remain uninspected. |
| Public LinkedIn identity and current-company display | **VERIFIED PUBLIC-PAGE OBSERVATION — 2026-11-09; SELF-PUBLISHED SOURCE** | Public metadata says “Hooman Shariati - Adobe,” shows Adobe as the current company, 4K followers, and 500+ connections. The current job title and tenure are masked for signed-out viewers. | This verifies what the profile publishes. Current employment, exact title, and dates are separately USER-CONFIRMED below. |
| Public LinkedIn About opening | **VERIFIED PARTIAL PUBLIC-PAGE OBSERVATION — 2026-11-09** | Visible text begins, “Please look at my projects on Github: https://github.com/hooman67” followed by “I have led several…”; the rest is gated. | The opening makes GitHub the first proof claim, so the linked profile quality is materially relevant. Complete About text remains unavailable. |
| Current Adobe employment and title | **USER-CONFIRMED — 2026-11-09** | Employed at Adobe from October 2023–Present; official title is Machine Learning Engineer, ASML. The public LinkedIn page also displays Adobe. | Use this exact employer/title/date tuple. Confirm the role's displayed work location separately; residence does not establish job location. |
| Built and productionized generative-video pipelines spanning T2V, I2V, and V2V | **USER-CONFIRMED + CHECKIN-SELF-REPORTED — 2026-09/10 durable record** | Adobe career evidence summarizes pipeline architecture, integration, deployment, evaluation, and technical transfer. | Strong conservative ingredient. Avoid internal codenames and confidential architecture details. |
| Led reusable inference and evaluation workflows, including distributed execution and vLLM integration | **CHECKIN-SELF-REPORTED; vLLM integration MANAGER-CORROBORATED** | FY24–FY25 check-in summaries inspected 2026-09-15. | Strong ingredient if phrased at capability level. Adoption, speed, utilization, and quality outcomes need exact, externally usable evidence. |
| Re-architected a distributed data-loading system using SQS, removing about 4,000 lines and sustaining 30+ nodes over multiple days | **CHECKIN-SELF-REPORTED; METRICS NOT INDEPENDENTLY CORROBORATED** | FY25 check-in summary inspected 2026-09-15; already used in the 2026-10-07 résumé. | Conditional metric variant only. Confirm numerical accuracy and disclosure permission before profile use. |
| Led or managed enterprise AI programs for named customers while remaining hands-on | **USER-CONFIRMED; PARTIAL CHECKIN SUPPORT** | Home Depot and Coca-Cola have check-in support; Home Depot, Coca-Cola, HP, Lionsgate, Humain, and Tesco were directly reported by Hooman. | Use “enterprise customer programs” by default until Hooman confirms whether customer names and specific deliverables may be public. |
| Returned to hands-on IC work and built a Home Depot rewriter | **USER-CONFIRMED — 2026-09-14** | Canonical career-evidence record. | Current-role relevance is high, but customer name, implementation, result, and timing are public-sensitive and need current confirmation. |
| Principal Engineer at Aupera; led five-person CV and six-person software teams across discovery through production support | **RESUME-DOCUMENTED — source inspected 2026-09-15** | Pre-Adobe résumé summary; raw PDF is no longer present on volatile storage. | Usable as self-authored historical evidence. Exact reporting scope and metrics remain uncorroborated. Keep Vancouver as the job location. |
| Earlier production ML, real-time computer vision, C++/Python, Linux, and latency-sensitive software experience | **RESUME-DOCUMENTED — source inspected 2026-09-15** | Aupera, Motion Metrics, and Fidessa history in the career inventory and current résumé. | Strong breadth ingredient. Current proficiency must not be inferred from historical use alone. |
| CVPR 2019 paper, “Towards Autonomous Mining via Intelligent Excavators” | **VERIFIED PRIMARY PUBLIC SOURCE — retrieved 2026-11-09** | The CVF page lists Hooman Shariati first, followed by Anuar Yeraliyev, Burhan Terai, Shahram Tafazoli, and Mahdi Ramezani; CVPR **Workshops**, June 2019, pages 26–32: `https://openaccess.thecvf.com/content_CVPRW_2019/html/cv4gc/Shariati_Towards_Autonomous_Mining_via_Intelligent_Excavators_CVPRW_2019_paper.html`. | The résumé inspected at the start of this batch omitted “Workshops”; the local canonical résumé has now been corrected. Preserve the exact workshop venue in later copy. Do not infer individual contribution from author order alone. |
| Public GitHub profile linked from LinkedIn and résumé | **VERIFIED PUBLIC SOURCE — retrieved 2026-11-09** | `https://github.com/hooman67` belongs to Hooman Shariati and exposes 52 public repositories, location “Canada,” no bio/company, and six popular repositories that are mostly old coursework or forks. The newest owned public repo, `cutlog`, was last pushed 2026-07-05 but has no description and only the default Next.js README. | The link is real but currently provides weak evidence for the target AI-infrastructure/inference narrative. Repository code quality, privacy, security, and deployability were not audited. |
| “12+ years” of experience | **DEFINITION AMBIGUOUS — reviewed 2026-11-09** | The career spans 2014–2026 but includes graduate study and gaps between listed roles. The documented employment comfortably supports “over a decade”; a precise 12+ cumulative years needs additional evidence or a definition including relevant study/research. | The local résumé now uses “over a decade.” This avoids implying that elapsed calendar span equals cumulative employment. |
| Staff/Principal AI systems positioning | **TARGET + WORKING HYPOTHESIS, NOT CURRENT LEVEL FACT** | Project charter, market sample, and career synthesis support targeting Staff/Principal IC roles. | Use as target-market language only when it does not imply a current employer-conferred level. |
| Target role direction | **USER-CONFIRMED — 2026-11-09** | Target Senior IC and Staff/Principal AI infrastructure and inference roles. Engineering-manager roles are out of scope. | Profile should lead with hands-on systems, infrastructure, and inference; leadership describes IC scope and influence, while enterprise delivery remains supporting evidence. |
| Application sponsorship answer | **USER-CONFIRMED — 2026-11-09; NARROW SCOPE** | Hooman says he does not need sponsorship for the purposes of applying. | Recruiter/application wording may say “no sponsorship needed.” Do not infer or publish citizenship, permanent residency, visa category, or a guarantee about future immigration status. |
| Interview-readiness emphasis | **USER-CONFIRMED — 2026-11-09** | Explaining experience is not the weakness; prioritize system design and ML/inference fundamentals, followed by timed coding. | Profile copy should stay concise and technically focused rather than expanding into a behavioral narrative. |
| Search deadline and current pipeline | **USER-CONFIRMED — 2026-11-09** | Goal is an accepted offer by approximately 2027-01-09. There are no current recruiter conversations or interviews. | Treat the pipeline as zero-start. Hooman will explicitly ask for application help after the plan and LinkedIn are ready; no application, outreach, or recruiter message is authorized now. |

## Access and remaining gaps

- No complete LinkedIn export was found under this project. Hooman provided the public URL, which
  was inspected. Complete live fields and private settings still require the working laptop session.
- The old remote login expired and the browser stack was deliberately stopped. No restart or new
  authentication flow was attempted; do not confuse a public HTTP 200 with authenticated access.
- The pre-Adobe PDF, Adobe check-ins and prior browser/input directories under `/mnt/localssd`
  are now missing. Their durable career summaries retain source labels; no raw-source reread is
  claimed. Needed recovered evidence belongs under backed-up home storage.
- Current role work location, public-disclosure choices, detailed accomplishment metrics and any
  new public proof remain to be checked when preparing the actual merged edits. They do not block
  this general draft. Hooman's current employment and application sponsorship statement are already
  answered; do not ask those again without new ambiguity.

## Public-source retrieval record

- **LinkedIn public profile:** `https://www.linkedin.com/in/hoomanshariati/`, retrieved 2026-11-09
  by an unauthenticated HTTP GET following redirects with a standard browser user agent. It returned
  HTTP 200 and public HTML/JSON-LD, but masked headline, job title, tenure, full About, and other
  signed-in fields. This was read-only; no browser session or login flow was started.
- **GitHub public profile:** `https://github.com/hooman67`, retrieved 2026-11-09 through public HTML
  and `https://api.github.com/users/hooman67`; repository inventory used
  `https://api.github.com/users/hooman67/repos?per_page=100&sort=updated&direction=desc`. Public
  metadata is self-published and does not establish code quality.
- **CVF primary publication page:**
  `https://openaccess.thecvf.com/content_CVPRW_2019/html/cv4gc/Shariati_Towards_Autonomous_Mining_via_Intelligent_Excavators_CVPRW_2019_paper.html`, retrieved
  2026-11-09 by direct HTTP GET. It identifies the work as a CVPR Workshops paper and lists all five
  authors, year, and pages.
- **LinkedIn Open to Work guidance:** https://www.linkedin.com/help/linkedin/answer/a507508,
  retrieved 2026-11-09 by direct HTTP GET, HTTP 200. It distinguishes all-members, recruiters-only
  and visible-only-to-you settings and says it cannot guarantee complete privacy.
- **Career evidence:** `/home/colligo/hs_scripts/claude/dev_research/career/CAREER_EVIDENCE.md`,
  current local read November 9; earlier résumé/check-in provenance retained by claim.
- **Current résumé:** `/home/colligo/hs_scripts/claude/dev_research/positioning/HOOMAN_SHARIATI_RESUME.md`.
