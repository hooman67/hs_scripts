# Job-search workflow and Markdown viewer — side-conversation handoff

Recorded: **2026-11-16**, from source inspection and Hooman's replies in the Mac side conversation.
This is the canonical summary of these two repositories. The older friend-archive comparison
remains historical evidence; this review does not replace it or the current learning curriculum.

## Status and confirmed preferences

**Completed:** inspected both repositories, explained their workflows and requirements, checked
the Mac environment, and researched local recording/transcription options. No repository was
cloned, application installed, model downloaded, calendar connected, or job-search/viewer service
started. Recommendations below are not accepted implementation choices or proof of runtime behavior.

| Topic | Hooman's direct answer |
|---|---|
| Execution location | Only his Mac; no Pluto deployment for these tools. |
| Calls to capture | All: Zoom, Meet, Teams, phone and other call types. |
| Existing recordings/transcripts | None; open to recording-tool recommendations. |
| Transcription | Local is preferred. This does not establish a requirement for every later summarization step to run locally. |
| Viewer lifetime | Prefer it remaining available locally; manual startup is acceptable if substantially simpler. |

Hooman asked to understand and replicate the friend's workflow, then explicitly asked to persist
the findings for the main session. He has not selected a recorder, bought a license, approved a
specific Google integration, or asked this side conversation to install these tools.

## Sources and confidence

**High confidence — inspected repository source at these pinned main revisions:**

| Repository | Visibility and revision | Relevant sources |
|---|---|---|
| [hooman67/job-search](https://github.com/hooman67/job-search) | Private; `3b0f12adcc6d2f6c91ce54b281d5178617ede351` | [README](https://github.com/hooman67/job-search/blob/3b0f12adcc6d2f6c91ce54b281d5178617ede351/README.md), [SETUP](https://github.com/hooman67/job-search/blob/3b0f12adcc6d2f6c91ce54b281d5178617ede351/SETUP.md), root/per-folder agent instructions, four skill files, Makefile and relevant Python helpers. |
| [hooman67/md-viewer](https://github.com/hooman67/md-viewer) | Public; `8e8fe385e2b1063811058993b9632bc60244ad49`; version **0.18.0** | [README](https://github.com/hooman67/md-viewer/blob/8e8fe385e2b1063811058993b9632bc60244ad49/README.md), SKILL, pyproject, CLI wrapper, and viewer rendering/write/server code. |

Unauthenticated access to job-search returned 404, but existing Git authentication worked. No
credentials were requested from Hooman, printed, or copied into project files. Recheck live heads
and local installation state before implementation. The examined template contains career and
schedule placeholders; it does not establish the friend's actual qualifications or hiring results.

**Primary vendor sources — feature descriptions, not local benchmarks:**
[MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper),
[Audio Hijack](https://rogueamoeba.com/audiohijack/), and
[whisper.cpp](https://github.com/ggml-org/whisper.cpp).

## What job-search does

This is a Markdown-based operating workflow for an agent, with Python helpers. There is no
always-running job-search application or daemon that performs every step automatically.

| Component | Actual behavior |
|---|---|
| Career material | Holds authoritative background, résumé, LinkedIn copy and reusable stories. These are placeholders until personalized. |
| Search tracker | Active/closed/dismissed opportunities, saved postings, tailored résumés, submitted answers and statuses based on confirmed user actions. |
| Company records | One company conversation record with process overview and dated conversations, raw-source links, commitments and next steps. |
| `record-call` skill | Takes an existing recording, calls the OpenAI transcription helper, then instructs the agent to upload raw material to Drive and digest the conversation. It does **not** record or join a call. |
| `study-plan` skill | Uses confirmed interview instructions, relevant company/round research and sourced interview reports to build prioritized preparation. |
| `add-coding-question` skill | Creates a Python exercise with statement, examples, boundaries/tests and unfinished solution stubs; it does not include a solution by default. |
| `calendar` skill | Uses Google Calendar to find free windows, manage tentative holds, and tag/create confirmed interview records linked to the local viewer. |
| Résumé helper | ReportLab-based PDF generation from a restricted Markdown résumé format. Supports common headings, bullets, bold and links, not arbitrary Markdown tables/fences. PDFs are gitignored. |
| Source helpers | Fetch pages, browse JavaScript-challenged pages with Chrome/Playwright, and read 1point3acres reports/question banks with the user's own authorized account access. Site layouts and access can change. |

The four skills are written for Claude Code, with Claude-specific settings, hooks and browser
instructions. Markdown and Python can be reused with Codex, but equivalent skill discovery,
connectors and agent permissions need deliberate adaptation. Having Chrome signed in through a
different browser-control mechanism does not automatically configure these integrations.

The intended flow is:

```text
User supplies recording or transcript
    → transcription, if needed
    → agent extracts questions, answers, commitments and preparation gaps
    → company conversation record
    → tracker/calendar updates within authorization
    → sourced, round-specific study plan and exercises
    → Markdown viewer for reading and feedback
```

The original instructions leave job applications, recruiter messages and LinkedIn edits manual.
Hooman's interest in agent implementation does not mean this template already supports those
actions. Adapt its policy to explicit session authorization before external execution.

Do not treat an exercise file or a checked research artifact as demonstrated mastery. The
coding-question skill has an ambiguous instruction to put newly generated unsolved stubs under
“Solved”; fix that distinction if adopting the workflow. Saved questions and actual solved work
need separate meanings.

## Transcription, calendar and storage dependencies

| Feature | Stock implementation and implications |
|---|---|
| Script environments | Uses `uv` inline dependency metadata. Original transcription script requires Python **3.12** (`>=3.12,<3.13`); calendar requires **3.13+**. The viewer requires **3.13+**. Separate uv environments handle these versions. |
| OpenAI transcription | Requires `CODEX_API_KEY`, despite the misleading name: it means an OpenAI API key, not a Codex subscription/login token. Audio goes to OpenAI. No such key is needed if this step is replaced by a local transcriber. |
| Transcription implementation | PyAV decodes audio to mono 16 kHz, creates approximately five-minute WAV chunks and calls `gpt-4o-transcribe-diarize`. Later chunks try to reuse speaker identities through reference audio. Labels need checking. The helper itself does not perform the Drive upload or conversation digest. |
| Output | The transcription helper writes timestamped speaker text and progress to a log under a gitignored temporary folder; it is not a complete clean-transcript ingestion pipeline. The author's timing anecdote was not benchmarked here. |
| Google features | Optional third repo: [shayanhoshyari/google-mcp](https://github.com/shayanhoshyari/google-mcp). SETUP points to its INSTALL instructions; the calendar helper reuses its authentication. It handles Google services, not Microsoft calendars by default. |
| Calendar rules | Pacific time, Google primary calendar, optional separate Holds calendar ID. Holds are not busy reservations. Calendar helper writes are designed not to send attendee notifications; that is not authorization for recruiter outreach. |
| Raw material | The stock skill archives audio/transcripts/whiteboard images to Drive and keeps raw files out of Git. A backed-up local archive instead of Drive is a proposal fitting local transcription, not a confirmed storage choice. |
| 1point3acres | Optional paid/account-gated sources use local cookie files. Do not copy account cookies into project notes or ask Hooman to paste them into chat. Public sources can be used first. |

Local transcription and local summarization are separate choices. Sending a locally produced
transcript to a cloud agent still sends the transcript text to that provider. Fully local
summarization would need a local language model and its own quality check; no local LLM was
installed or selected here.

## Recording recommendation — proposed, not selected

**Recommendation:** start with MacWhisper using local transcription options. Pro's system-audio
capture, local speaker recognition, watch folders, Markdown export and CLI make it a promising
fit for this workflow. It also supports cloud transcription and cloud speaker services, so select
local models explicitly. The examined vendor page lists Whisper/Parakeet options and says
Qwen3-ASR requires macOS 26; Hooman's inspected Mac is on macOS 15.7.4. Do not require an OS upgrade
just to begin. No accuracy, speed, speaker consistency or auto-recording behavior was tested here.

Audio Hijack is an alternative for flexible application/microphone recording and also advertises
local transcription. A free whisper.cpp setup is possible but needs more assembly for recording,
export and speaker attribution; its experimental speaker-turn detection is not equivalent to
robust identification of recurring speakers.

Zoom/Teams and browser-based Meet can be captured through Mac microphone and system/application
audio. Phone calls can use this path only when their audio actually passes through the Mac;
phone-only calls need a separate permitted recording/export workflow. Neither repo solves that
capture boundary. Configure required macOS audio-recording permissions and obtain recording
permission where required. Keep actual recordings outside Git with a deliberate backup location.

## What md-viewer does

Standalone FastAPI/Uvicorn viewer, usable without Claude Code. No Node build is required.

| Feature | Behavior and limits |
|---|---|
| Reading | File navigation, table of contents, heading numbering, Markdown tables/collapsibles, diagrams, equations and code rendering. |
| Review | Rendered/source/raw/diff views, Git change/history views and local link checking. Link checking does not establish that external web URLs work. |
| Notes | Browser notes attach to document blocks or table rows and persist as HTML comments inside the real Markdown file. |
| Editing | Version 0.18.0 has an Edit tab and `/_file` write route, with stale-file checks. README's “only notes write” description is outdated; do not assume the current viewer is read-only. |
| PDF | Uses WeasyPrint, imported lazily; Pango is an additional Mac dependency for PDF support, not for ordinary Markdown reading. This differs from job-search's ReportLab résumé renderer. |
| Local service | Defaults to host `127.0.0.1`; port zero selects an available port unless a fixed port is supplied. Serve a trusted project folder. Resolved paths are restricted to the served root. There is no inspected read-only flag. |
| Internet access | Loads Mermaid/KaTeX and other browser assets from CDNs. PlantUML diagram source is encoded into requests to the public PlantUML renderer. A local web server therefore does not mean fully offline rendering. |

The skill's suggestion to remove notes after handling them must not override Hooman's rule to
preserve existing document bytes for addition requests. Saving notes/edits is a source mutation;
viewing is not. No viewer edit or note operation was performed in this review.

## Mac environment and proposed setup

**Observed on this Mac, November 16:** Apple Silicon (`arm64`), 24 GiB RAM, macOS 15.7.4;
Homebrew, Git and Codex on PATH. Default Python is 3.9.6. `uv`, `claude`, `gh`, and the md-viewer
skill were not found at the inspected paths. The repos were read remotely, not locally cloned.
Recheck this snapshot because the main session or Hooman may subsequently install tools.

The template expects the viewer in
`/Users/ana.rodrigues/.claude/skills/md-viewer`. That installation directory is usable by the
standalone CLI even without Claude Code. Prospective commands, **not executed**:

```bash
brew install uv
uv python install 3.13
git clone https://github.com/hooman67/md-viewer /Users/ana.rodrigues/.claude/skills/md-viewer
/Users/ana.rodrigues/.claude/skills/md-viewer/bin/md-viewer serve --port 8766 /Users/ana.rodrigues/Desktop/hooman/hs_scripts/claude/dev_research
```

The proposed research viewer URL is `http://127.0.0.1:8766`. Job-search's Makefile uses **8765**
because its calendar records contain stable viewer URLs. Check port availability and existing
installations first; never overwrite a checkout. To use the PDF tab, optionally install Pango.
Python 3.12 is needed only if retaining the stock restricted transcription script or another
version-specific helper that requires it; do not install it merely because it appears in this review.

Manual startup can begin in a terminal. If automatic availability is requested, a macOS user
LaunchAgent can start the viewer at login and restart it after a crash. It needs stable absolute
paths and a Homebrew/uv-aware environment. It is available while the Mac is awake, not while the
machine is powered off. No LaunchAgent was written or installed.

## Integration recommendation and exact handoff

**Proposed:** adopt the template's operational records, interview digestion and sourced
round-specific preparation; retain the current curriculum and canonical career evidence. Replace
the OpenAI audio step with local transcription, make Drive optional, and adapt the agent skills.
There is no transcript watch/ingestion daemon in the template: watch-folder transcription plus
automatic company-record ingestion would require explicit additional integration.

The main session should read this summary before discussing implementation, recheck source and
machine state, and use the five confirmed preferences above without asking them again. Continue
the main session's actual live task; this side-chat handoff is not an instruction to abandon it
or automatically install a recorder, purchase a license, connect accounts or submit applications.
When Hooman requests setup, start with the viewer and a small local recording/transcription trial,
then validate company-record ingestion before building broader automation. Protect one canonical
career record and one learning sequence rather than duplicating them into a fresh template.

Existing source/study material lives in the real Mac checkout under
`/Users/ana.rodrigues/Desktop/hooman/hs_scripts`. Pluto storage/backup was not reverified in this
Mac-only review. This summary and the root handoff are project files; no commit, push or independent
backup-service verification was performed.
