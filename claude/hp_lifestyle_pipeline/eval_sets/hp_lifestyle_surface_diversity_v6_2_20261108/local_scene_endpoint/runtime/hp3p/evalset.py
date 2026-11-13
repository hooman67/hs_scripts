import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Row:
    id: str
    user_prompt: str
    hero_s3: str
    width: int
    height: int
    baselines: list[tuple[str, str]]
    raw_prompt: str = ""
    baseline_prompt: str = ""


def load_rows(evalset_path: str | Path, baseline_path: str | Path) -> list[Row]:
    base = {r["meta_data"]["evalset_item_id"]: r for r in json.loads(Path(baseline_path).read_text())["rows"]}
    rows = []
    for e in json.loads(Path(evalset_path).read_text()):
        b = base.get(e["eval_set_item_id"], {"images": []})
        rows.append(Row(e["eval_set_item_id"], e["user_prompt"], e["media"][0], e["width"], e["height"],
                        [(i["meta_text"]["label"], i["image_src"]) for i in b["images"]],
                        e.get("raw_prompt", ""), e.get("prompt", "")))
    return rows


def download_hero(row: Row, dest_dir: Path) -> Path:
    dest = dest_dir / "hero.png"
    if not dest.exists():
        subprocess.run(["aws", "s3", "cp", row.hero_s3, str(dest), "--only-show-errors"], check=True)
    return dest
