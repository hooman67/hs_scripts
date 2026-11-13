import base64
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StyleRef:
    id: str
    name: str
    tone: str
    content: str
    mime: str
    data: bytes
    human_presence: str | None = None


def load_catalog(path: str | Path) -> list[StyleRef]:
    """Load style refs, dropping byte-identical duplicate images (the source catalog has some)."""
    refs, seen = [], {}
    for r in json.loads(Path(path).read_text())["references"]:
        data = base64.b64decode(r["image"]["base64"])
        digest = hashlib.sha256(data).hexdigest()
        presence = r.get("human_presence")
        if digest in seen and seen[digest] != presence:
            raise ValueError("Byte-identical references have conflicting human-presence tags")
        if digest not in seen:
            seen[digest] = presence
            refs.append(StyleRef(r["id"], r["name"], r["tone"], r["content"], r["image"]["mime_type"], data, presence))
    return refs


def labels(catalog: list[StyleRef]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    return tuple(sorted({r.tone for r in catalog})), tuple(sorted({r.content for r in catalog}))


def _order(refs: list[StyleRef], seed: str) -> list[StyleRef]:
    return sorted(refs, key=lambda r: hashlib.sha256(f"{seed}:{r.id}".encode()).hexdigest())


def pick_refs(catalog: list[StyleRef], tone: str, content: str, seed: str, k: int = 4) -> list[StyleRef]:
    """Exact tone+setting bucket first, then same setting, then same tone, then anything."""
    picked: list[StyleRef] = []
    tiers = [lambda r: r.tone == tone and r.content == content,
             lambda r: r.content == content, lambda r: r.tone == tone, lambda r: True]
    for match in tiers:
        for r in _order([r for r in catalog if match(r) and r not in picked], seed):
            if len(picked) == k:
                return picked
            picked.append(r)
    return picked
