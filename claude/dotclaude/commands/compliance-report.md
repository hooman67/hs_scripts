Run a full compliance check across all engineering practices and produce a summary report.

Usage: /compliance-report [checks=all|jira|github|slack|wiki]

Parse $ARGUMENTS to determine which checks to run. Default: all.

Run the following checks by executing each script. Run them sequentially (some share rate-limited APIs):

**1. Jira Hygiene (Practices 2, 3):**
```
uv run --script ~/.claude/scripts/check_jira_hygiene.py
```

**2. Stale Branches (Practice 6):**
```
uv run --script ~/.claude/scripts/check_branches.py
```

**3. PR Ticket References (Practice 1):**
```
uv run --script ~/.claude/scripts/check_pr_tickets.py
```

**4. PR Test Coverage (Practice 7):**
```
uv run --script ~/.claude/scripts/check_pr_tests.py
```

**5. Eval/Docs Ratio (Practice 12):**
```
uv run --script ~/.claude/scripts/check_eval_docs_ratio.py
```

**6. Slack Health (Practices 4, 9, 14):**
```
uv run --script ~/.claude/scripts/check_slack_health.py
```

**7. Wiki Page Completeness (Practice 5):**
```
uv run --script ~/.claude/scripts/check_wiki_pages.py
```

If `checks=jira`, only run steps 1 and 5. If `checks=github`, only run steps 2, 3, 4. If `checks=slack`, only run step 6. If `checks=wiki`, only run step 7.

After running all checks, present a **consolidated report**:

## Compliance Report — [date]

**Executive Summary:**
- Overall status: CLEAN / WARNINGS / VIOLATIONS_FOUND
- Total violations, warnings, and review flags across all checks

**Violations by Practice:**
For each practice with violations, show:
- Practice name and rule
- Table of violations (ticket/PR/branch, person, issue)

**Warnings:**
- Grouped by practice

**Action Items:**
- Prioritized list of specific actions to take (e.g., "Ask @engineer to add description to FFP-123", "Branch X needs to be merged or rebased")

**Trends** (if you have context from previous runs):
- Whether things are improving or getting worse
