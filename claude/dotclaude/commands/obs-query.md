Answer a question against the Obsidian LLM-wiki, with citations, and optionally file the answer back as a new wiki page so explorations compound.

Usage: /obs-query <question>

Vault: `/Users/hshariati/hs_scripts/claude/obsidian/hs_base` (`$V`). Read `$V/WIKI_SCHEMA.md` if you
haven't this session. Prefer direct file tools; use obsidian MCP `open_file` to surface filed pages.

## Steps

1. **Find candidate pages.** Read `$V/index.md` first to locate relevant pages by category. If the
   index looks thin for this question, also ripgrep the wiki (`rg -i -n "<terms>" "$V/wiki"`), and
   fall back to `$V/raw/` only when the wiki doesn't cover it.

2. **Read the relevant pages** — drill from the index into the actual pages, following `[[links]]`
   between them. Synthesize across pages; that's the value of the wiki.

3. **Answer with citations.** Cite the pages/sources you used as `[[wikilinks]]` (or `file:line` for
   raw). If the wiki can't answer, say so plainly and suggest what to ingest or search for.

4. **Choose the output form** that fits the question: prose, a comparison table, a chart, a Marp
   deck, or an Obsidian canvas. Ask if the best form is ambiguous.

5. **Offer to file it back.** Good answers shouldn't vanish into chat. Offer to write the answer as
   `$V/wiki/analysis/<kebab-title>.md` (`type: analysis`, with source `[[links]]`). If Hooman agrees:
   write the page, update `$V/index.md` (Analysis section), append
   `## [YYYY-MM-DD] query | <question>` to `$V/log.md`, and `open_file` it in Obsidian.
