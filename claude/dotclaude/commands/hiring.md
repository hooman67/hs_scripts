Review candidates for Hooman's Foundry generative-models roles: rank resumes against a living
candidate profile, give interview recommendations, and maintain a persistent record of everyone
reviewed so candidates can be compared over time and patterns detected.

Usage: /hiring [path-to-resumes-dir | review | profile | candidates | add <name>]

The skill's memory lives in `/Users/hshariati/hs_scripts/claude/hiring/` (project folder, backed up via git):
- `profile.md` — the living target-candidate profile + the scoring rubric. This is the source of truth.
- `candidates.md` — the ledger of every candidate reviewed, by batch, with tier + one-liner + patterns.

## Behavior by argument

**No arg, `review`, or a directory path** → review a batch of resumes:
1. Default resume dir is the path given, else ask Hooman where the resumes are (commonly
   `~/Downloads/hiring_resumes_review_claude/` or a `~/Downloads/resumes_review*` dir).
2. Read `profile.md` FIRST — score against its current rubric, not from memory.
3. List the PDFs; dedupe obvious duplicates (same size / "(1)" suffixes) before counting.
4. Read every unique resume (use the Read tool on PDFs directly).
5. Score each on the three hard bars — E2E leadership · strong eng AND ML in image/video
   **generation** · go-getter — applying the **hard modality filter** (generation, not
   understanding/perception/3D/detection/recommendation).
6. Output a tiered ranking: **Interview** (🥇🥈🥉) → **Second tier** → **Pass**, each with a
   one-line "why" and explicit caveats. Close with a decision aid: "interview first: X and Y;
   add Z if the role leans <emphasis>."
7. Note any ATS/pipeline cross-signals visible in the resumes (e.g. "added to Applied
   Scientist–Firefly").
8. **Append the batch to `candidates.md`** (new dated section + update the Patterns section).

**`profile`** → show `profile.md`; offer to refine it. When Hooman gives new preferences,
edit `profile.md` and note the change. This is how the profile "develops over time."

**`candidates`** → summarize `candidates.md`: who's been reviewed, tier distribution, and the
running patterns. Good for "have we seen anyone like this before?" and trend questions.

**`add <name>`** → add or update a single candidate record in `candidates.md` (e.g. after an
interview, record the outcome).

## Output style (what Hooman responds well to)

- Tiered list with 🥇🥈🥉 on the top picks, one-line rationale, per-candidate caveats.
- A closing "if you hire one / interview first" line keyed to different role emphases.
- Surface generation-modality mismatches explicitly — that's the decisive axis.

## Notes

- Resumes have historically come as PDFs attached to a Slack message in the **adoberesearch**
  workspace (channel C09H6QJKSKY). The default bot token (adobe.enterprise) CANNOT read that
  workspace, so resumes are usually downloaded manually into a Downloads dir. If account-level
  Slack (`claude.ai Slack` MCP) is authenticated, you can fetch them directly; otherwise ask
  Hooman to drop the files in the target dir.
- Always re-read `profile.md` before ranking — it changes, and the ranking must reflect the
  current spec.
