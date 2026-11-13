Turn one of Hooman's interview transcripts into a structured feedback MD file: extract the
candidate's answer to EVERY question Hooman asked, score each answer, and roll up to part scores +
a final score. **Your job is to parse and score answers — NOT to decide whether to hire, advance,
or reject.** That decision is Hooman's alone and must never appear in the output.

Usage: /hiring_generate_interview_feedback <path-to-transcript> [candidate name] [req/level]
Returns: an MD file at `hiring/interviews/<lastname_first>_<YYYY-MM-DD>.md` (and prints it).

The rubric lives in `/Users/hshariati/hs_scripts/claude/hiring/`:
- `prescreen_guide.md` — the questions Hooman asks + what each part is testing.
- `prescreening_answers.md` — the model answers. **Grade technical correctness against this.**
- `profile.md` — the target profile (used only to interpret experience/culture criteria, not to
  make a hire call).

## Golden rules (read every time)

1. **Do NOT judge the candidate's fate.** No "advance / reject / hire / no-hire / lean," no "below
   bar," no recommendation of any kind. Whether to promote is Hooman's decision and must not color
   the feedback. Just: questions, answers, scores.
2. **Record the actual answer to EVERY question Hooman asked** — technical, experience, and culture.
   Faithfully extract/summarize what the candidate said, quoting telling phrases from the transcript.
   Do not skip, merge, or paraphrase away any question. If Hooman asked it, it gets its own line.
3. **Score each answer.**
   - Technical questions → score **correctness** against `prescreening_answers.md`. Right = high,
     wrong/backwards = low, partial = middle, honest "I don't know" = low-but-noted (a gap, not a lie).
   - Experience questions → score the **specificity and on-modality relevance of the evidence given**
     (concrete, personally-owned, image/video generation detail scores high; vague/claim-level/
     off-modality scores low).
   - Culture questions → score the answer **against Hooman's stated preferences** (below), not the
     model's own values.
4. **Keep your biases out — especially on culture.** Two hard rules:
   - **Motivation:** Hooman PREFERS candidates who care more about **impact on the company** than
     about how intellectually interesting the work is. A company-impact / results / ownership lean
     is a **positive**, not a negative. Do not penalize it.
   - **Prompting is not a scoring axis.** Score the correctness/quality of the answer the candidate
     ultimately gave. You may note factually "reached it after a hint" or "initially said X then
     corrected," but do NOT turn "the interviewer had to prod" into a deduction or editorial. The
     interviewer's technique is not the candidate's score.
5. **Proof over claims still applies — as an accuracy standard, not a verdict.** Credit demonstrated,
   specific answers; a vague buzzword answer scores low on correctness/evidence. This is about
   grading the answer, not about recommending an outcome.

## Scoring scale

- **Per question:** 0–10. (Technical = correctness; Experience/Culture = evidence quality vs.
  Hooman's criteria.) Give a one-line justification per question.
- **Part scores (holistic roll-ups of the per-question scores):**
  **Technical /4 · Experience /3 · Culture /3.**
- **Final score = Technical + Experience + Culture, out of /10.**
- Report the final score plainly. **Do not** append a recommendation, tier, or hire verdict.

## Steps

1. Read `prescreen_guide.md` + `prescreening_answers.md` + `profile.md` (don't grade from memory).
2. Load the transcript. `.docx` → convert first:
   `textutil -convert txt "<file>" -output <scratchpad>/transcript.txt` then read it. `.txt`/`.md`
   read directly. (Transcripts are auto-generated — expect garbled words / dropped audio / "mhm"s;
   read for intent, don't penalize transcription noise.) Pull candidate + req/level from filename.
3. Walk the transcript start to finish. Identify **every question Hooman asked**, in order, and the
   candidate's answer to each. Bucket them into Part 1 (technical), Part 2 (experience), Part 3
   (culture). If Hooman never asked a given part's questions, say "not assessed" — don't invent.
4. For each question write: **Q** (the question), **A** (faithful answer, quote key phrases),
   **Score x/10** + a one-line correctness/quality note.
5. Roll up each part to /4, /3, /3; sum to the final /10.
6. Write the MD file to `hiring/interviews/<lastname_first>_<YYYY-MM-DD>.md` and print it.

## Output format (exact)

```
# Interview Feedback — <Name>
- Candidate / Req (level) / Interviewer / Date / Type
- Score: Technical X/4 · Experience Y/3 · Culture Z/3 → N/10

## Part 1 — Technical — X/4
### Q1. <question>
- **A:** <candidate's actual answer, faithful, with quotes>
- **Score: n/10** — <one-line correctness note vs. the answer key>
### Q2. ... (one block per question asked)
**Part 1 subtotal: X/4** — <one-line summary of what was right/wrong>

## Part 2 — Experience — Y/3
(same per-question structure for each experience question asked)
**Part 2 subtotal: Y/3**

## Part 3 — Culture — Z/3
(same per-question structure; score per Hooman's preferences, incl. company-impact = positive)
**Part 3 subtotal: Z/3**

## Final score: N/10
<Factual one-paragraph summary of the answers given. NO recommendation, NO hire/advance/reject.>
```

## Notes

- Do not update `candidates.md` with a tier or verdict from this skill — record only the score if
  Hooman asks. The tier/advance decision is his.
- One report per transcript. If given a folder, do each and list the output files.
