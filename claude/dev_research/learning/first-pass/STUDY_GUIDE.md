# First Pass, Stage 1 — Video-Processing Design Exercise

Updated: **2026-11-10**. This is the practice companion to the teaching guide. No completion is
assumed. When these concepts are new, **read the tutorial first**:
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/REVIEW_GUIDE.md`.

## Contents

- [Learn before rehearsing](#learn-before-rehearsing)
- [Begin your own design](#begin-your-own-design)
- [Design prompt: durable video-processing jobs](#design-prompt-durable-video-processing-jobs)
- [Completion gate](#completion-gate)
- [References](#references)

## Learn before rehearsing

The tutorial starts with the whole system and follows one video through it. Learn what the API,
database, S3 storage, SQS queue and our worker programs each do. Then follow one failure at a time
and explain why the design needs the additional rule. Terms, cloud choices, diagrams, message
examples and optional implementation details are defined there; this exercise does not replace them.

Aim to understand three things before closing the tutorial:

1. Where the video, the saved job and the small queue message live, and how they connect.
2. What happens if the client retries, a notification is missing, or a worker stops.
3. Why only the authorized attempt can select the final output, including during cancellation.

There is no requirement to memorize SQL or cloud product names. Ask about any step whose purpose
is unclear. The tutorial's final interview section is for later presentation practice.

## Begin your own design

After you understand the walkthrough, close it and work through the prompt below. For this first
attempt, take the time you need. Start by writing:

- five questions whose answers could change the design;
- three rules that must always hold, such as keeping accepted work recoverable;
- two rough calculations that affect queue or worker capacity; and
- what you promise the customer when you say a request is accepted.

Use the fixed assumptions below for the remainder. Returning to a section to repair a gap is part
of learning; record what needed help separately from what you could explain unaided.

## Design prompt: durable video-processing jobs

Design a multi-tenant service that accepts a video already present in object storage plus a
transform specification, runs a CPU- or GPU-backed pipeline, and exposes status, cancellation, and
one final output.

Exercise assumptions:

- 100 tenants; 2 submissions/second steady and 50/second for a ten-minute burst.
- Inputs are 1–10 GB; execution takes 2–60 minutes. Resource needs are known from the transform.
- Submission and status APIs target 99.9% monthly availability. Once accepted, a job survives
  ordinary API/worker restarts and a lost client response.
- Delivery can repeat; workers can pause, crash, or resume late. Internal duplicate execution is
  tolerable, but the API exposes one logical job and no stale result.
- Output is retained 30 days and job metadata 90 days. Cancellation is best effort and its race
  with completion must have a documented outcome.
- Tenants authenticate; job, source, output, and idempotency scope are tenant-isolated. Treat media
  and transform parameters as untrusted input.

Produce:

1. API contracts for submit, status, and cancel, including retry behavior.
2. A minimal data model and job/attempt state machine.
3. One diagram showing the synchronous submit path and asynchronous execution path.
4. The normal flow, including when the queue message is acknowledged.
5. One principal trade-off and one capacity estimate.

After the normal flow works, walk through these injects without changing their facts:

- The database commits acceptance, but the client never receives the response.
- Worker A stops making progress; Worker B takes over; then Worker A resumes.
- A worker finishes uploading the output and crashes before recording success.
- Cancellation arrives while a worker is finalizing the output.

## Completion gate

You are ready to move on when you can draw the basic system, follow one job, and explain the main
failure cases in your own words. Cover safe submission retries, recovery after worker loss, rejecting
an old worker's result, upload-before-completion failure, and cancellation. Name a practical service
for each box and distinguish what it supplies from the application code we write.

Use the tutorial's self-checks to locate gaps. For interview rehearsal, use its separate final
section and rubric. You do not need to master every Staff/Principal follow-up or build a deployed
service before continuing to the ML/inference fundamentals stage. No performance is assumed from
having read the guide.

## References

The tutorial contains the current primary-source references and their limitations. Consult the
source that answers your question; reading the complete AWS or PostgreSQL manuals is not an
additional prerequisite for this lesson.
