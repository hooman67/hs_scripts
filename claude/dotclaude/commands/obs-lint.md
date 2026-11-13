Health-check the Obsidian LLM-wiki and propose (or apply) fixes.

Usage: /obs-lint [--fix]

Vault: `/Users/hshariati/hs_scripts/claude/obsidian/hs_base` (`$V`). Read `$V/WIKI_SCHEMA.md` first.
Use direct file tools + ripgrep (`-L` for the `raw/docs` symlink).

## Checks — scan `$V/wiki/**/*.md` and report a prioritized checklist

- **Contradictions** — pages/claims that disagree. Surface both, and whether a
  `> [!warning] Contradiction` block already flags it.
- **Stale claims** — assertions a newer source (check `log.md` dates) has superseded.
- **Orphans** — pages with no inbound `[[links]]` (grep each page's name across the wiki).
- **Dead links** — `[[wikilinks]]` that point to a file that doesn't exist yet.
- **Missing pages** — important entities/concepts mentioned repeatedly but with no page of their own.
- **Missing cross-refs** — pages that clearly relate but don't link to each other.
- **Index drift** — pages absent from `index.md`, or index entries whose file is gone.
- **Frontmatter gaps** — pages missing required frontmatter fields per the schema.
- **Data gaps / next questions** — suggest sources to find or questions to investigate (offer a
  web search for external facts).

## Output

Present findings grouped by check, most important first, each with the file(s) and a suggested fix.

With **`--fix`**, apply only the safe mechanical repairs — index drift, dead-link stubs, obvious
missing cross-refs, frontmatter fields — and list separately what needs Hooman's judgment
(contradictions, stale claims, content decisions). Append `## [YYYY-MM-DD] lint | <summary>` to
`$V/log.md`.
