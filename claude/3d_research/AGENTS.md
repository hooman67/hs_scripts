# Result preservation

- Treat every existing result HTML, manifest entry, media asset, and review card as append-only.
- Never delete, replace, hide, or overwrite existing result content unless Hooman explicitly asks to remove or replace that specific content.
- New experiments must be added as new cards, tabs, versioned assets, or versioned reports.
- Publishing a new version must preserve previous versions and their provenance.

# Blockout-guided prompting

- Treat the blockout video as the authoritative motion specification.
- Keep action prompts minimal: describe only the required action and any necessary exclusion.
- Do not restate trajectories, grips, intermediate poses, or secondary character actions already visible in the blockout unless a measured failure requires that correction.
- Additional prompt detail must solve a specific observed failure; otherwise omit it.
