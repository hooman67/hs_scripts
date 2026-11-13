Ingest a raw source into the Obsidian LLM-wiki: read it, extract knowledge, write/update wiki pages, and update the index + log.

Usage: /obs-ingest [path-or-name-of-raw-source | paste text | URL]

The vault is a local git repo at `/Users/hshariati/hs_scripts/claude/obsidian/hs_base` (call it `$V`).
**Read `$V/WIKI_SCHEMA.md` FIRST** — it defines the layers, page types, frontmatter, contradiction
discipline, and conventions. Follow it exactly. Prefer direct file tools (Read/Write/Edit/Grep/Glob)
over MCP; use the obsidian MCP `open_file` to surface finished pages in Obsidian.

## Steps

1. **Locate / create the raw source** (raw is immutable — never edit a source after saving it):
   - A path/name in `$ARGUMENTS` → find it under `$V/raw/` (Hooman's notes are at `$V/raw/docs/`).
   - Pasted text → save it as `$V/raw/<kebab-title>.md` with a one-line provenance header.
   - A URL → fetch with WebFetch, save the markdown to `$V/raw/<kebab-title>.md` with the URL noted.
   - Image / handwritten scan → save the image under `$V/raw/assets/`, view it, transcribe to a
     raw `.md` beside it.
   - No arg → list `$V/raw/` (and `$V/raw/docs/`) and ask which source to ingest.
   - **Skip PII / sensitive files** (e.g. `raw/docs/candidates.md`) unless Hooman explicitly asks.

2. **Read the source fully.** For image-heavy sources, read the text first, then view the images.
   Summarize the key takeaways to Hooman in 3-6 bullets and let him steer emphasis **before** writing.

3. **Write the source-summary page** at `$V/wiki/sources/<kebab-title>.md` — frontmatter
   (`type: source`, `raw: "[[raw/...]]"`, `created:`/`updated:` both = today, `tags:`; `ingested:`
   is optional and, if kept, equals `created`), a one-line summary, the distilled content and key
   claims, with `[[wikilinks]]` to the entities/concepts it touches.

4. **Update entities & concepts.** Across `$V/wiki/entities/` and `$V/wiki/concepts/`: create pages
   for important new things/ideas, update existing ones with the new information, and wire
   `[[wikilinks]]` in **both** directions. If the source contradicts an existing claim, flag it
   inline with the schema's `> [!warning] Contradiction` block — never silently overwrite.

5. **Update `wiki/overview.md`** if the source shifts the big picture.

6. **Update `$V/index.md`** — add/refresh an entry for every page created or changed, under the
   right category, each with its one-line summary.

7. **Append to `$V/log.md`**: `## [YYYY-MM-DD] ingest | <Title>` + a one-line note of what changed
   and how many pages were touched. Get the date from the session `currentDate` context.

8. **Surface & report.** Use obsidian MCP `open_file` to open the new source-summary (and the
   overview if it changed) in Obsidian. Report which pages were **created** vs **updated**, and
   suggest 1-3 follow-up sources or questions.

A single ingest can legitimately touch 10-15 pages — thorough cross-referencing is the whole point.
