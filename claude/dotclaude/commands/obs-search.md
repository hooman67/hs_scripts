Search the Obsidian LLM-wiki (and raw sources) for a term, phrase, or topic.

Usage: /obs-search <query> [--wiki | --raw]

Vault: `/Users/hshariati/hs_scripts/claude/obsidian/hs_base` (`$V`). Default scope is both `wiki/`
and `raw/`; `--wiki` or `--raw` restricts. Note `raw/docs` is a symlink, so pass `-L` to ripgrep.

## Steps

1. **ripgrep** the vault (fast, primary):
   ```
   rg -i -n -L --heading -C1 "<query>" "$V/wiki" "$V/raw"
   ```
   (drop `$V/raw` for `--wiki`, or use only `$V/raw` for `--raw`.)

2. **Obsidian-native search** as a complement — obsidian MCP `search_simple` for quick text, or
   `search_query` when the query is a tag/frontmatter filter (e.g. a `type:` or `tags:` lookup).

3. **Present grouped hits**, most relevant first: for each file, the matching lines plus a one-line
   description of what that page is. Separate `wiki/` hits (synthesized knowledge) from `raw/` hits
   (source material) so it's clear which is which.

4. Offer to `open_file` the top hit in Obsidian, and — if the strongest matches are in `raw/` with
   no wiki page yet — suggest `/obs-ingest` on that source.
