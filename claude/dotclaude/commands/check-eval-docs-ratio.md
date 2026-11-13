Check that eval and documentation work makes up a healthy percentage of the current sprint.

Usage: /check-eval-docs-ratio [project=KEY] [threshold=N]

Parse $ARGUMENTS to extract optional filters:
- project: Jira project key (default: FFP from config)
- threshold: minimum percentage of eval/docs tickets (default: 15 from config)

Then run:

```
uv run --script ~/.claude/scripts/check_eval_docs_ratio.py --project "<project>" --threshold <threshold>
```

Omit flags that weren't provided to use defaults.

After running, parse the JSON and present a report:

**Sprint Overview:**
- Total tickets and story points
- Eval/docs tickets: count, percentage, story points

**Eval/Docs Tickets:**
- Table: Ticket, Summary, Assignee, Labels, Points

**Verdict:**
- Whether the threshold is met
- If below threshold, suggest adding eval/docs work to the sprint

Note: Detection relies on Jira labels (eval, docs, testing) and summary keywords. Make sure the team labels tickets consistently.
