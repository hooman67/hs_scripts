Update the Foundry Node Utilization canvas with daily compute summaries for TCCC, THD, and Humain projects.

## Canvas Details
- **Canvas ID:** F0AQ1PFGE5U
- **Canvas URL:** https://adobe.enterprise.slack.com/docs/T024FSURM/F0AQ1PFGE5U
- **Title:** Foundry Node Utilization
- **Access:** Use `user_token` from `~/.claude/hshariati/credentials.yaml`

## Workflow

### Step 1: Read the existing canvas to find what dates are already covered

Fetch the canvas content via the private URL:
```python
r = requests.get('https://files.slack.com/files-pri/T23RE8G4F-F0AQ1PFGE5U/canvas',
                  headers={'Authorization': f'Bearer {token}'})
```
Parse the HTML to extract all `<h2>` date headers. For each date header, check whether it contains **our customers** ([TCCC], [THD], [Humain]) or only the other squad's customers ([NBCU], [Lionsgate], [Paramount], [WDI], [GW]).

**This canvas is shared between TWO squads:**
- **Hooman's squad:** TCCC, THD, Humain
- **The other squad:** NBCU, Lionsgate, Paramount, WDI, GW base model

A date is "missing our updates" if:
1. The date doesn't exist at all, OR
2. The date exists but only has the other squad's entries (no [TCCC]/[THD]/[Humain] bullets)

Search for `[TCCC]`, `[THD]`, `[Humain]` in the HTML content following each `<h2>` to determine which dates need our updates.

### Step 2: Fetch Pluto job data for missing dates

Use `mcp__foundry-pluto__list_jobs` with `status_filter="all"` to get all jobs. Filter to projects:
- `Foundry-TCCC`
- `Foundry-THD`
- `Foundry-Humain`

Filter to jobs whose `started_at` falls within the missing date range.

**Important learnings:**
- The `list_jobs` result can be very large (800K+ chars). It gets saved to a file — use Python to parse and filter it.
- Pluto project names are `Foundry-TCCC`, `Foundry-THD`, `Foundry-Humain` (not `foundry-tccc` lowercase).
- Many jobs are short-lived failed/stopped debug runs. **Aggregate these into a single "debugging" bullet** rather than listing each one.
- Interactive, demo, and inference jobs should be noted but distinguished from training jobs.

### Step 3: Research unclear job names

For jobs with unclear names:
1. **Check for FFP- ticket references** in the job name (e.g., `FFP-73260`, `FFP-78834`). If found, use `/jira-get` to pull context.
2. **Search the squad Slack channel** (C0AKWLP0MCY, use user_token) for the job name or owner to find discussion context.
3. **Map owners to team members** using `~/.claude/projects/-Users-hshariati-hs-scripts-claude-monitor/memory/user_profile.md`.

### Step 4: Write the daily summary

For each missing date, produce a summary in this format:

```markdown
## [Date]

**[TCCC] - [Short headline description]**
- Concise bullet about what happened
- Another bullet

**[THD] - [Short headline description]**
- Bullet

**[Humain] - [Short headline description]**
- Bullet

---
```

**Style guidelines (match existing canvas tone):**
- Executive-level — no raw job IDs, UUIDs, or technical debugging details
- Use active voice: "Training launched on 32 nodes", "Inference sweep completed across 6 checkpoint variants"
- Good patterns: "[Stage] training completed — nodes transitioned to [next stage]", "Identified and resolved [issue] in training pipeline", "Captioning workload completed; nodes freed"
- Combine short-lived failed/stopped jobs into: "Debugging [config/issue] through [N] iterations before [outcome]"
- Mention GPU counts and node counts when significant (e.g., "32-node H200 run")
- Note milestones: "loss trending down", "product likeness visible", "checkpoint deployed to Boards"
- If no jobs for a customer on a date, write: `**[Customer] - No activity**` with a single bullet `- No compute jobs recorded`

### Step 5: Insert into the canvas

**CRITICAL: This canvas is shared between two squads. NEVER create duplicate date sections.**

There are two scenarios:

**Scenario A: Date already exists (other squad posted their updates)**
Use `insert_after` on the other squad's date `<h2>` section ID to append our content WITHIN that same date section. This way both squads' bullets appear under one date header.

```python
r = requests.post('https://slack.com/api/canvases.edit', headers=headers, json={
    'canvas_id': 'F0AQ1PFGE5U',
    'changes': [{
        'operation': 'insert_after',
        'section_id': '<existing h2 section_id for that date>',
        'document_content': {
            'type': 'markdown',
            'markdown': my_content_for_that_date  # NO ## Date header, just the **[TCCC]**... bullets
        }
    }]
})
```

**Scenario B: Date does not exist at all**
Use `insert_before` on the next chronologically-later date section to create a new date section with our content.

```python
r = requests.post('https://slack.com/api/canvases.edit', headers=headers, json={
    'canvas_id': 'F0AQ1PFGE5U',
    'changes': [{
        'operation': 'insert_before',
        'section_id': '<id of the next existing date section>',
        'document_content': {
            'type': 'markdown',
            'markdown': f"## {date}\n\n{my_content}\n\n---"
        }
    }]
})
```

Dates should appear newest-first (April 2 above April 1 above March 31, etc.).

**NEVER create a separate date header if the date already exists.** Always merge into the existing one using `insert_after`.
**NEVER delete or modify the other squad's content** (NBCU, Lionsgate, Paramount, WDI, GW entries).

### Step 6: Confirm

Print the canvas URL and list the dates that were added.
