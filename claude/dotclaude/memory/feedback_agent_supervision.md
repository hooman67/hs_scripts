---
name: feedback_agent_supervision
description: Regularly supervise authorized agents; resume interrupted work and prevent unfinished work from quietly going idle.
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-19T06:41:55Z
---

Hooman explicitly requested on November 18, 2026: "Make a memory to regularly check so that our search agent (and later on other agents) are always running as they should."

During active authorized work, the primary must check live agent status at least once every 60 seconds, and at session resume, task completion, user steering and suspected interruption. Keep tool waits bounded so supervision remains possible. Check actual output/checkpoints as well as the running status: running alone does not establish progress. Report observed rate limits, disconnects or unexplained stalls promptly, especially Astra.

If an agent was interrupted or disconnected, resume its unfinished task from the latest verified durable checkpoint, preserving its required model and effort. Do not silently substitute Sol for Astra strategy. If an agent completes a bounded batch while the overall authorized objective remains unfinished, review its result and dispatch the next meaningful authorized batch rather than allowing the objective to quietly go idle. Honor dependencies, current scope/caps, explicit pauses and required user inputs; do not create busywork or repeat uncertain external effects just to keep an agent running.

Maintain a durable expected-agent roster in the active project's live checkpoint with task, model/effort, last observed status/check time, output location and next action. Distinguish running agents, completed batches, input-blocked work and serving dashboards. A dashboard server is not a searching/applying worker.

Provide concise regular progress updates during ongoing job-search work, including Astra's observed progress and interruptions. Respect the separately requested quiet workflow for tutorial additions. Do not claim continuous unattended monitoring or automatic restarts outside an active session unless an actual persistent supervisor has been implemented and verified.

For the career project, apply this through `/Users/ana.rodrigues/Desktop/hooman/job-search/AGENTS.md` and its live handoff `/Users/ana.rodrigues/Desktop/hooman/job-search/prep/README.md`.

Verified November 19: the career project now has a real launchd source/model supervisor and
an app-context native X worker/watchdog. Read the live checkpoint at
`/Users/ana.rodrigues/Desktop/hooman/job-search/search/data/2026-11-19-channel-search/checkpoint.json`
and runtime setup at `/Users/ana.rodrigues/Desktop/hooman/job-search/SETUP.md` before restarting
anything. Verify heartbeat, PID/start identity, completed source cycles and actual model output
separately. Do not start duplicate collectors or infer an application from a discovery record.

The collaboration Astra agent later showed no concrete progress despite bounded resumes. An
engineering-orchestrated call through the verified configured CLI returned an actual
`gpt-6-astra` high response with recorded invocation/no-tools provenance. This is an available
same-model route, not permission for Sol to invent strategy. Model-catalog presence or a
parent-environment READY smoke does not prove unattended service execution; check its actual
completed response. Keep the source service running while a strategy route is blocked.


### 2026-11-19 — persistent review cadence and truthful channel status

Actual Astra HIGH operational policy now selects a thirty-minute reviewer cadence, ten records/two proposals per review, thirty-two attempted starts per rolling twenty-four hours, one reviewer at a time, durable reservations/backoff and core-lifetime AC-only keep-awake. Exact source: `/Users/ana.rodrigues/Desktop/hooman/job-search/search/data/2026-11-19-channel-search/astra/review-queue-cli-decision.json`. The reviewer is an actual configured Astra CLI invocation, not an idle collaboration-agent label. Sol owns collectors/engineering and never substitutes career strategy. Check actual response validation as well as provider exit: the first normal ten-record provider turn succeeded but its entire review failed career-evidence validation; no partial integration was allowed. Require null for an unassessable career match and sourced quotations for actual claims.

Report distinct counts: seventeen Active manual opportunities, the candidate subset, and the full captured posting-identity pool are different. The fifteen-slot limit applies only to the supplementary timely-hiring pilot, not collection or ordinary EM preparation. Successful historic LinkedIn job captures do not establish a healthy current channel: latest guest searches can be blocked, while authenticated posts require an actual owner check. Preserve these limits in the live checkpoint and single Hooman review file. Owned runtime PIDs change across deploys; verify fresh PID/start identity and heartbeat instead of memorizing a numeric PID.


### 2026-11-19 — preserve actual model decisions when configuring collectors

Keep mechanical collector-task configuration in `/Users/ana.rodrigues/Desktop/hooman/job-search/search/data/continuous-search/collector-runtime-overlay.json`, separate from the saved actual Astra strategy artifact. Registering tasks inside that authoritative JSON changes the owner-manifest hash and stales completed reviews; restore only exact immutable input bytes with SHA proof, never weaken freshness gates or rewrite actual model output. Native worker reloads effective `/Users/ana.rodrigues/.codex/job-search-runtime/runtime-strategy.json`, not raw policy alone. Exactly two recurring LinkedIn post queries are approved; retire one-off repair scheduler rows while retaining their capture provenance. A successful owner/query route with zero extracted cards means unknown coverage; changed DOM needs scoped semantic permalink/card guards, not a claim of no jobs. Latest verified normal AstraHIGH10review batch passed at19:43UTC; all10held for evidence. Live checkpoint/source proofs contain the currentcounts and next20:11UTC cadence.
