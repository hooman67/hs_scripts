#!/usr/bin/env python3
"""Write the immutable preflight snapshot for the spatial-crop protocol."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from run_spatial_crops import FREEZE_PATH, atomic_json, current_protocol_state, sha256_path


def main() -> int:
    state = current_protocol_state()
    if FREEZE_PATH.exists():
        existing = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
        comparable = {key: existing.get(key) for key in state}
        if comparable != state:
            raise SystemExit("Existing freeze differs from current protocol; refusing overwrite")
    else:
        atomic_json(
            FREEZE_PATH,
            {**state, "frozen_at_utc": datetime.now(timezone.utc).isoformat()},
        )
    print(
        json.dumps(
            {"freeze": str(FREEZE_PATH), "sha256": sha256_path(FREEZE_PATH)},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
