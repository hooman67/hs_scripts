Rebuild `index.md` from scratch by scanning every wiki page.

Usage: /obs-index

Vault: `/Users/hshariati/hs_scripts/claude/obsidian/hs_base` (`$V`). Use when the index has drifted
from reality or after a batch of ingests. This regenerates the catalog; it does not touch wiki pages.

## Steps

1. `Glob "$V/wiki/**/*.md"`. For each page, read its frontmatter (`title`, `type`) and its one-line
   summary (the line under the H1).
2. Regenerate `$V/index.md`, preserving the top frontmatter and the intro paragraph/links. Group
   entries by category — **Overview, Entities, Concepts, Sources, Analysis** — matching each page's
   `type`. Each entry: `- [[wiki/<path>|Title]] — one-line summary`. Sort alphabetically within a
   group. Note any page with missing/blank frontmatter so it can be fixed (or hand off to /obs-lint).
3. Append `## [YYYY-MM-DD] reindex | N pages across M categories` to `$V/log.md` (date from the
   session `currentDate`).
4. Report a short before/after diff (counts per category) and `open_file` the index in Obsidian.
