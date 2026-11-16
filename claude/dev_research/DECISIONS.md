# Decisions Log

## 2026-11-15 — answer study questions before background document updates

- **[USER-CONFIRMED — 2026-11-15]** Answer each study-document question immediately in the main
  thread, then delegate the already-authorized automatic collapsible Q&A addition to a separate
  background agent. Do not interrupt Hooman with progress notes or routine completion notices for
  that background update. The updater must retain both the question and answer, insert them beside
  the relevant passage, and preserve every existing byte, including date and update lines.

## 2026-11-15 — automatically retain follow-up questions and clarifications

- **[CONFIRMED BY HOOMAN]** Save subsequent study-document questions and their explanations as
  closed-by-default collapsible sections containing both question and answer. Do not wait for
  another request to save each one. Insert beside the relevant passage without changing existing
  text, examples, dates or formatting. This standing workflow is also in the global instructions.
- **[ADDITION COMPLETED]** Added the duplicate-notification/deletion explanation and the earlier
  expired-lease claim clarification in section 6. The original paragraph and SQL remain intact.

## 2026-11-15 — additions must preserve the material Hooman has read

- **[CONFIRMED BY HOOMAN]** Requests to add notes or collapsible questions/answers authorize
  insertion only. Do not change existing wording, examples, structure, formatting or date lines
  unless explicitly requested. This applies beyond this lesson and is recorded in the canonical
  global instructions. Hooman needs the original material to remain stable while learning.
- **[CORRECTION COMPLETED]** Restored the first review guide's original update line and retained
  both requested additions. Removing just those added blocks reproduces the pre-addition guide
  exactly; the original section prose and SQL were not replaced. No exercise completion is inferred.

## 2026-11-12 — clarify authentication within the first lesson

- **[USER REQUEST]** Explain how the API authenticates a caller and obtains the customer tenant.
- **[AGENT TEACHING CHOICE]** Extend the existing guide in place using a Cognito login/access-token
  example plus application-owned PostgreSQL tenant memberships. Keep authentication, tenant
  authorization and AWS worker identity separate. This is an illustrative design, not a selected
  production identity provider; revisit if Hooman requests an actual integration.
- **[SCOPE]** Preserve the separate HTTP lesson and current curriculum. No deployment, credentials,
  external profile work or roadmap change is needed for this explanation.

## 2026-11-10 — teach the first design before rehearsing it

- **[CONFIRMED BY HOOMAN]** Rebuild the first review guide around the big picture and diagrams,
  then main components/normal flow, then problems and constraints with explained fixes and design
  choices. Define terms at first use, show examples, and name concrete infrastructure/services and
  the application code we implement. Keep interview presentation in a separate section.
- **[CONFIRMED BY HOOMAN]** Foundational guides may be longer; shorten as familiarity grows. This
  supersedes forcing an unaided attempt before initial concept learning or compressing every guide
  into a short answer sheet. The seven-stage learning sequence does not change.
- **[AGENT DECISION]** Use one running video-job example with FastAPI, PostgreSQL/RDS, S3, SQS and
  our sender/workers. Teach safe retries, saved notification reminders, ownership/recovery,
  version-specific output selection and cancellation only after the ordinary flow is clear.
- **[AGENT DECISION]** The tutorial's main SQS policy deletes messages after a database-recorded
  terminal outcome. The earlier early-delete-after-claim policy remains an explicit alternative
  requiring database recovery. Versioned S3 references and short locked database transitions make
  the example internally consistent; this is a teaching choice, not an Adobe production change.
- **[VALIDATION BOUNDARY]** Primary docs and an independent worker review support the explanation;
  no service deployment, production test or completed human exercise is claimed.

Record decisions newest first. Mark each as `[CONFIRMED BY HOOMAN]`, `[AGENT DECISION]`, or
`[PROPOSAL — NOT YET CONFIRMED]`.

## 2026-11-09 — folder cleanup and durable handoff

- **[CONFIRMED BY HOOMAN]** Remove unneeded leftovers from this project and refresh project
  documentation so another agent can resume while Hooman reads the delivered documents.
- **[AGENT DECISION]** Remove the abandoned browser launcher and duplicate research hub. Their
  useful historical findings are retained in topic summaries and learnings; browser setup is no
  longer the selected profile-access path.
- **[AGENT DECISION]** Consolidate the old inference notes, lab, quiz and all 15 answers into
  `/home/colligo/hs_scripts/claude/dev_research/learning/inference-baseline.md`. Keep the current
  first-pass exercise and its separate review, the main curriculum, positioning and résumé paths.
- **[AGENT DECISION]** Retain career evidence, topic summaries, posting descriptions, source
  manifests, validation results and the reproduction script. They are unique evidence, even when
  old raw inputs are unavailable. Required project records remain separate and indexed.
- **Recovery:** all four removed originals were verified byte-for-byte against commit
  `403310d404a2ac7790df5cc2466e3cbb719aae27` in `/home/colligo/hs_scripts` before removal. The live
  handoff records former paths and a non-overwriting restore example. No extra archive copy is needed.
- **Scope/revisit:** this is organizational cleanup, not a new curriculum decision. It does not
  imply completed study, accepted profile copy, application authorization or a changed target.

## 2026-11-09 — diagnostic replies and current sequence

- **[CONFIRMED BY HOOMAN]** Begin with system design and ML/inference fundamentals, then timed
  coding. Explaining experience is not the perceived weakness. Completed exercises remain unknown.
- **[CONFIRMED BY HOOMAN]** Target Senior IC and Staff/Principal AI infrastructure/inference;
  exclude engineering-manager roles. Core preparation is shared, with level-dependent follow-ups.
- **[CONFIRMED BY HOOMAN]** The two-month goal means an accepted offer. There are no current
  recruiting conversations. Application assistance will be requested after plan/profile readiness.
- **[CONFIRMED BY HOOMAN]** Still employed at Adobe; affirmative reply to the current official
  title question. No sponsorship needed for the purposes of applying. Do not infer a visa category
  or answer differently scoped immigration questions without the necessary facts.
- **[CONFIRMED BY HOOMAN]** The LinkedIn URL is https://www.linkedin.com/in/hoomanshariati/;
  unsure whether an export exists. No export was found under this project.
- **[AGENT DECISION]** Integrate the authorized accelerated sequence into the canonical learning
  plan, replacing the old schedule; keep substantive deep-lab history available in Git. Produce the
  next focused packet only. The detailed exercises and gates remain researcher recommendations.
- **[AGENT DECISION]** Correct the local résumé's publication venue to CVPR Workshops using the
  CVF primary source, and use “over a decade” instead of an ambiguous 12+ cumulative years.
- **[PROPOSAL — NOT YET CONFIRMED]** Use the conservative LinkedIn copy and optionally recruiter-only
  visibility. User has not selected disclosure/visibility settings. Named customers/internal metrics
  remain out of this public draft, and LinkedIn says recruiter-only cannot guarantee complete privacy.
- **Alternatives/revisit:** earlier coding or specialist depth can move forward when a real round
  or performance evidence warrants it. No broad modeling or management track is added. No external
  edit, message or application is authorized by these planning decisions.

## 2026-11-09 — accelerated transition and delegated execution

- **[CONFIRMED BY HOOMAN]** Seek a job within two months; structure first-month breadth followed
  by second-month deeper drills. Give the sequence without a rigid timetable; the prior maximum
  5–6 hours/week and non-urgent readiness framing are superseded. This is a target, not a promised
  hiring outcome. The later diagnostic reply above clarified that it means an accepted offer.
- **[CONFIRMED BY HOOMAN]** Current residence is San Jose, California. Propose LinkedIn updates
  correcting its Vancouver location, together with other career-material updates.
- **[CONFIRMED BY HOOMAN]** Use a parallel agent for LinkedIn and delegate bounded execution to
  GPT-5.6 at extra-high effort or another suitable model; retain primary-agent planning/review.
- **[AGENT DECISION]** Use available `gpt-5.6-sol` with `xhigh` for two separate evidence audits;
  keep canonical edits centralized and do not assume model selection removes provider limits.
- **Initial uncertainties:** the later diagnostic replies above resolved current pipeline, role
  scope and the application-purpose sponsorship statement. Completed work, full live LinkedIn text
  and public-disclosure preferences remain open.
- **Reversibility/revisit:** the revised curriculum is a reviewable research output. No external
  profile changes, applications, messages or disclosure of private project details are authorized.
  Reassess allocation using actual interview feedback and demonstrated performance.

## 2026-10-14 — compare and reconsider the learning approach

Historical comparison decision. Its proposed 12-week schedule was superseded by the November 9
accelerated sequence; it was not accepted as an intermediate active plan.

- **[CONFIRMED BY HOOMAN]** Read the friend’s complete shared archive, compare approaches and
  topics, and recommend direct adoption or an improved adaptation. Hooman reports matching
  qualifications and target jobs and believes the friend’s approach is more targeted/practical.
- **[AGENT DECISION]** Complete a bounded comparison of all 47 supplied files, retain a source
  manifest, and validate representative examples. Treat the sanitized placeholders and missing
  interview outcomes as limitations, not evidence of the friend’s lack of preparation.
- **[PROPOSAL — NOT YET CONFIRMED]** Replace the default 36-week platform-first schedule with
  eight weeks of broad interview practice plus four weeks driven by actual gaps/targets, at the
  existing 5.5-hour default. Keep a smaller measured serving lab and existing career evidence.
  Rationale: recurring coding practice and full system-design/behavioral rehearsal are missing or
  under-scheduled, while customer/evaluation work is delayed. The proposed schedule and alternatives
  are in `/home/colligo/hs_scripts/claude/dev_research/research/plan-comparison/SUMMARY.md`.
- **Uncertainty:** desired interview horizon, current completed work, unaided readiness and the
  friend’s actual feedback/outcomes remain unconfirmed. The proposal does not establish a new
  deadline, budget or demonstrated skill level.
- **Reversibility/revisit:** no active curriculum was replaced. Reallocate after a diagnostic week,
  a concrete interview brief, changed hours, or evidence that coding/design already pass while
  technical depth fails. Keeping the old deep-platform track remains a valid alternative if
  Hooman explicitly prioritizes that outcome.

## 2026-10-07 — immediate Staff/Principal résumé

- **[CONFIRMED BY HOOMAN]** Create a general Staff/Principal IC résumé for a former executive who
  is now at a new company; balance inference/platform and Forward Deployed customer AI experience.
- **[CONFIRMED BY HOOMAN]** Adobe employment began in October 2023; the official title is Machine
  Learning Engineer, ASML.
- **[AGENT DECISION]** Use four concise, evidence-backed Adobe bullets and omit older academic
  projects and the short 2014 AB-InBev role so the externally shareable résumé remains one page.

## 2026-09-15 — project charter

Historical decisions below retain their original dates. November 9 supersedes the non-urgent
framing, 5–6-hour cap, optional management track and assumptions about application sponsorship;
consult the current charter and live handoff for active constraints.

- **[CONFIRMED BY HOOMAN — 2026-10-05]** For every technical learning topic, inspect applicable
  Adobe code and documentation—including `/home/colligo/colligo`, the Obsidian LLM wiki, AIDocs,
  corporate wikis, and Glean when available—and connect external theory to internal production
  experience. Clearly distinguish code observation, documentation, experiment, and inference.
- **[CONFIRMED BY HOOMAN — 2026-10-05]** Proactively call out security implications wherever
  relevant, including the threat, a safe default, and controls still needed for production.
- **[CONFIRMED BY HOOMAN — 2026-10-04]** Produce actual study material one week at a time, starting
  with Cycle 1 Week 1: concise notes plus primary external readings, a hands-on lab Hooman performs
  with Codex available for questions/troubleshooting, a quiz, and an immediately available but
  separate answer file.
- **[CONFIRMED BY HOOMAN — 2026-10-04]** Start learning now; remaining market normalization may
  refine later cycles but must not delay Cycle 1.
- **[CONFIRMED BY HOOMAN — 2026-10-04]** Assume two NVIDIA H200 GPUs and permit Adobe/Pluto for
  exercises. Keep the artifact private; do not require private work to be independent of Adobe or
  sanitized for publication.
- **[CONFIRMED BY HOOMAN — 2026-10-04]** Begin with text inference and add modalities only after
  the first path is stable.
- **[USER-CONFIRMED BASELINE — 2026-10-04]** Python 3/3, Docker 2/3, Kubernetes 0/3, PyTorch 2/3,
  vLLM 2/3, CUDA 0/3, Triton 0/3, and distributed systems 1/3.
- **[CONFIRMED BY HOOMAN]** Use an external-only initial market sample of approximately 50–75
  current roles. Split emphasis evenly between inference/platform and Forward Deployed/customer AI
  while casting a wide net across titles. Prioritize roles whose published **base salary** exceeds
  $200K, but retain highly relevant roles without published compensation and label the gap.
- **[CONFIRMED BY HOOMAN]** Keep the modeling branch deliberately bounded for now: enough current
  modeling knowledge to perform and reason about LoRA and limited fine-tuning, without assuming a
  modeling-heavy career track is necessary.
- **[CONFIRMED BY HOOMAN]** Treat Forward Deployed/customer AI engineering as a strongly aligned
  target role family because it matches Hooman's Foundry experience.
- **[CONFIRMED BY HOOMAN]** Prefer one deep, reproducible inference-platform portfolio project
  over many small demos. A live inference-platform demonstration was instrumental in Hooman's
  original Adobe hiring process, so a modern successor has demonstrated personal proof value.
- **[CONFIRMED BY HOOMAN]** Use relevant, work-safe external links from the X bookmarks; use job
  posts as skill evidence only because this is not an active job search; include useful broader
  career information; and omit irrelevant bookmarks without an exclusion log.
- **[CONFIRMED BY HOOMAN]** Stop the remote Chromium/noVNC stack to avoid idle CPU use. Defer
  remote LinkedIn/X authentication; a laptop agent that can authenticate to X will download the
  relevant tweets instead.
- **[CONFIRMED BY HOOMAN]** Team outcomes achieved under Hooman's leadership may be used as
  evidence of his individual leadership impact. Do not impose a blanket rule that excludes or
  weakens them; select accurate, strong verbs based on his role.
- **[CONFIRMED BY HOOMAN]** Prefer persistent authenticated LinkedIn and X access over relying only
  on exports. Hooman will perform login/MFA directly; Codex may inspect the authenticated accounts
  but must obtain approval before profile edits, posts, messages, or applications.
- **[CONFIRMED BY HOOMAN]** The project prepares for a possible future job transition; no job
  loss is expected or considered imminent.
- **[CONFIRMED BY HOOMAN]** The main output is a study/learning plan grounded in job-market
  requirements, followed by résumé, LinkedIn, and interview readiness work.
- **[CONFIRMED BY HOOMAN]** Target Staff/Principal IC technical readiness. Engineering-manager
  roles may be included at application time but do not need a separate skills curriculum.
- **[CONFIRMED BY HOOMAN]** Prioritize AI platform, inference, serving, optimization, AI
  engineering, and systems. Preserve modeling/data science as a secondary path; the expected
  sweet spot may sit between model behavior and production engineering.
- **[CONFIRMED BY HOOMAN]** Research roles that pay well above $200K. Current compensation is
  approximately $500K total, but the immediate research goal is skill discovery rather than
  selecting applications.
- **[CONFIRMED BY HOOMAN]** Study at most 5–6 hours per week; optimize for durable readiness.
- **[CONFIRMED BY HOOMAN]** Remote work is preferred. Canada is the fallback if US employment
  ends before permanent work authorization; TN may permit a later US return. Geography does not
  constrain initial curriculum research.
- **[CONFIRMED BY HOOMAN]** Derived summaries from Adobe check-ins may be stored in this secure
  repository.
- **[AGENT DECISION]** Keep the raw résumé and check-in PDFs at their existing source locations;
  store a compact, source-labeled evidence inventory here to limit duplication and file growth.
- **[PROPOSAL — NOT YET CONFIRMED]** Research external roles first, then compare internal Adobe
  roles to avoid anchoring the curriculum to Adobe's terminology and current stack.
