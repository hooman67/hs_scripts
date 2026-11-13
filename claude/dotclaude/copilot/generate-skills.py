#!/usr/bin/env python3
"""Generate portable Copilot skill adapters from the shared Claude commands."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COMMANDS = ROOT / "commands"
SKILLS = ROOT / "copilot" / "skills"
MARKER = ".dotclaude-source"


def metadata(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    name = path.stem
    description = ""
    body = text
    if text.startswith("---\n"):
        frontmatter, separator, remainder = text[4:].partition("\n---\n")
        if not separator:
            raise ValueError(f"Unclosed frontmatter: {path}")
        body = remainder
        for line in frontmatter.splitlines():
            key, colon, value = line.partition(":")
            if not colon or key not in ("name", "description"):
                continue
            value = value.strip().strip('"').strip("'")
            if not value or value in ("|", ">"):
                raise ValueError(f"Unsupported multiline {key} in {path}")
            if key == "name":
                name = value
            else:
                description = value
    if not description:
        description = next(
            (re.sub(r"^#+\s*", "", line.strip()) for line in body.splitlines() if line.strip()),
            f"Use the shared {name} workflow.",
        )
    description = re.sub(r"\s+", " ", re.sub(r"[`*<>]", "", description))[:360]
    slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9-]", "-", name.lower().replace("_", "-"))).strip("-")
    if not slug:
        raise ValueError(f"Invalid skill name: {path}")
    return slug, description


def main() -> None:
    SKILLS.mkdir(parents=True, exist_ok=True)
    sources: dict[str, Path] = {}
    for path in sorted(COMMANDS.glob("*.md")):
        name, description = metadata(path)
        if name in sources:
            raise ValueError(f"Duplicate skill name {name}: {sources[name]} and {path}")
        sources[name] = path
        directory = SKILLS / name
        marker = directory / MARKER
        if directory.exists() and (not marker.exists() or marker.read_text().strip() != path.name):
            raise ValueError(f"Refusing to overwrite a custom skill: {directory}")
        directory.mkdir(exist_ok=True)
        marker.write_text(path.name + "\n", encoding="utf-8")
        (directory / "SKILL.md").write_text(
            "---\n"
            f"name: {name}\n"
            f"description: {json.dumps(description, ensure_ascii=False)}\n"
            "---\n\n"
            f"Read `~/.claude/commands/{path.name}` completely before acting. It is the "
            "authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` "
            "from the user's request rather than literally. Translate Claude-specific "
            "tool names to Copilot tools while preserving approval, credential, and "
            "stopping boundaries. Shared scripts are at `~/.claude/scripts/`. "
            "If a required MCP server or dependency is unavailable, report it; "
            "do not claim the operation succeeded.\n",
            encoding="utf-8",
        )
    for marker in SKILLS.glob(f"*/{MARKER}"):
        directory = marker.parent
        if directory.name not in sources:
            (directory / "SKILL.md").unlink()
            marker.unlink()
            directory.rmdir()
    print(f"Generated {len(sources)} Copilot skill adapters in {SKILLS}")


if __name__ == "__main__":
    main()
