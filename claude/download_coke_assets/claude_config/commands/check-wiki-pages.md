Check customer wiki landing pages for required sections (Problem Statement, Requirements, Data PoE, Eval PoE, Experiments/Results PoE, JIRA Initiative).

Usage: /check-wiki-pages [page-ids=ID1 ID2 ...]

Parse $ARGUMENTS to extract optional page IDs. If none provided, uses customer_page_ids from compliance_config.yaml.

Then run:

```
uv run --script ~/.claude/scripts/check_wiki_pages.py --page-ids <id1> <id2> ...
```

Omit --page-ids to use defaults from config.

After running, parse the JSON and present a report:

**Per page:**
- Page title and URL
- Found sections (checkmark)
- Missing sections (X mark)
- Last modified by / when

**Summary:**
- Pages compliant vs non-compliant
- List of all missing sections across all pages
