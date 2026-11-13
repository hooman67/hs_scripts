Process engineering sync meeting transcripts to extract action items, status updates, blockers, and decisions, then map them to Jira tickets for batch update. Use when the user provides a meeting transcript, meeting notes, standup notes, or asks to update Jira from a meeting.

## Workflow

### Phase 1: Extract

Parse the transcript and extract every actionable item into one of these categories:

| Category | What to look for |
|----------|-----------------|
| **Status update** | Progress reported on existing work ("X is done", "Y is 80% complete", "shipped Z") |
| **Blocker** | Something preventing progress ("blocked on", "waiting for", "can't proceed until") |
| **New action item** | Newly assigned work with an owner ("Alice will do X", "we need to create a ticket for Y") |
| **Decision** | A choice that was made ("we decided to", "let's go with", "agreed on") |
| **Status transition** | Work moving between states ("starting on X", "X is done", "moving X to review") |

For each item, capture:
- **Who**: The person responsible (from the transcript)
- **What**: Concise summary of the item
- **Source quote**: The relevant excerpt from the transcript
- **Jira ticket**: The ticket key if explicitly mentioned (e.g., "FFP-12345")

### Phase 2: Identify Project & Load Context

#### Step 2a: Identify the project

The user manages multiple customer projects, each with a top-level **initiative** and working **epics** underneath it. New tickets go under the **epic**, not the initiative.

**Customer initiative/epic mapping, team roster, and Jira field requirements** are all in `~/.claude/projects/-Users-hshariati-hs-scripts-claude-monitor/memory/user_profile.md`. Read that file to get the full project table, aliases, initiative keys, and epic keys.

Determine the project by:
1. **Transcript filename**: Check the file name for any project name or alias (case-insensitive).
2. **Transcript content**: If not in the filename, scan the transcript body for project aliases.
3. **Ask if unsure**: If the project cannot be confidently determined, ask the user to confirm before proceeding. Present the four projects as options.

#### Step 2b: Load all tickets and capture field template

Once the project is confirmed:

1. Use `/jira-sprint` with `--jql "\"Epic Link\" = {WORKING_EPIC_KEY} OR parent = {WORKING_EPIC_KEY} ORDER BY key ASC"` to pull tickets. Or fetch directly:
   ```
   uv run --script ~/.claude/scripts/jira_sprint.py -- --jql "\"Epic Link\" = {WORKING_EPIC_KEY} OR parent = {WORKING_EPIC_KEY} ORDER BY key ASC"
   ```
   This gives you the **ticket inventory** -- all child tickets with key, summary, status.

2. **Capture a field template for new ticket creation.** Fetch required fields from the working epic:
   ```
   uv run --script ~/.claude/scripts/jira_get.py -- {WORKING_EPIC_KEY}
   ```
   Note the `components` and `customfield_13401` (Assigned Team) from the epic -- these are **mandatory fields** in FFP and must be cloned to every new ticket.

#### Step 2c: Match extracted items to tickets

For each item extracted in Phase 1, match it to a ticket from the inventory:

1. **Explicit ticket references**: If a ticket key (e.g., FFP-XXXXX) is mentioned in the transcript, use it directly.
2. **Semantic match from inventory**: Compare the extracted item's description against ticket summaries. Match based on topic, keywords, and context.
3. **Fallback JQL search**: If an item doesn't match any inventory ticket:
   ```
   uv run --script ~/.claude/scripts/jira_sprint.py -- --jql "summary ~ \"keyword\" AND status != Done ORDER BY updated DESC"
   ```
4. **Ambiguous matches**: If multiple tickets could match, flag for user review.
5. **No match found**: Flag as "New ticket?" under the project's working epic.

### Phase 3: Propose Changes Report

Write ALL proposed changes to an **editable markdown file**. Save next to the transcript (or `~/Downloads/`) using:

`[project_alias]_sync_[YYYY-MM-DD]_proposed_changes.md`

**Do NOT apply any changes yet.** Use this format:

```
## Proposed Jira Updates from [Meeting Name/Date]

### Summary
- X status updates
- X new action items
- X blockers to log
- X status transitions
- X items needing your input

---

### Status Updates (comments to add)

| # | Ticket | Summary | Proposed Comment | Source |
|---|--------|---------|-----------------|--------|
| 1 | FFP-XXXXX | Ticket summary | "Comment text" | "quote from transcript" |

### Status Transitions

| # | Ticket | Summary | Current Status | Proposed Status | Source |
|---|--------|---------|---------------|----------------|--------|
| 1 | FFP-XXXXX | Ticket summary | In Progress | Done | "quote from transcript" |

### Blockers (comments to add)

| # | Ticket | Summary | Blocker Description | Source |
|---|--------|---------|-------------------|--------|
| 1 | FFP-XXXXX | Ticket summary | "Blocked on X" | "quote from transcript" |

### New Tickets to Create

| # | Suggested Summary | Type | Assignee | Description | Source |
|---|-------------------|------|----------|-------------|--------|
| 1 | Summary text | Task | Person | Details | "quote from transcript" |

### Needs Your Input

| # | Item | Issue | Options |
|---|------|-------|---------|
| 1 | Description | "Multiple tickets match" | FFP-111, FFP-222 |
```

Omit any section with zero items. At the bottom include:

```
---

> **Instructions**: Edit any rows above -- change ticket keys, modify proposed
> comments, delete rows you don't want, adjust statuses, etc.
> When done, tell the agent "apply" or "apply with edits" and describe what you changed.
```

After writing, tell the user where it was saved and ask them to review.

### Phase 4: Apply Changes

After the user approves (with or without edits), apply changes:

1. **Status updates / blockers**: Use `/jira-update` to add comments:
   ```
   uv run --script ~/.claude/scripts/jira_update.py -- FFP-XXXXX --comment "[Eng Sync - PROJECT - DATE] Comment text"
   ```
2. **Status transitions**: Use `/jira-update` with `--status`:
   ```
   uv run --script ~/.claude/scripts/jira_update.py -- FFP-XXXXX --status "Done"
   ```
3. **New tickets**: Use `/jira-create`:
   ```
   uv run --script ~/.claude/scripts/jira_create.py -- --summary "Summary" --project "FFP" --type "Task" --parent "WORKING_EPIC_KEY" --assignee "username" --labels "project_label"
   ```

   **Team roster and initiative/epic mapping:** See `~/.claude/projects/-Users-hshariati-hs-scripts-claude-monitor/memory/user_profile.md` for the full team roster (name → Jira username → Slack ID), customer initiative/epic mapping, and required Jira fields for ticket creation.

   If an assignee's name is not in the roster, search Jira users via curl or ask the user.

4. **After applying**: Print a summary of what was applied and any failures.

## Important Guidelines

- **Never apply changes without explicit user approval.** The review step is mandatory.
- When adding comments, prefix with `[Eng Sync - PROJECT - DATE]` so the source is traceable.
- Always load the full ticket inventory before matching. Do not skip this step.
- For comments, use people's first names as spoken in the transcript. For ticket assignees, resolve names to Jira usernames using the team roster.
- Keep proposed comments concise -- summarize, don't paste entire transcript excerpts.
- Only propose status transitions when the transcript clearly indicates completion or a phase change.
- When creating new tickets, set the parent to the project's **working epic** key -- not the initiative.
