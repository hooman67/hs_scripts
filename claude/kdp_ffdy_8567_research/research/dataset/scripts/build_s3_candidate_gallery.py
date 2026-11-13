#!/usr/bin/env python3
"""Package the reviewed KDP candidate gallery for the Foundry S3 HTML gateway."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "research" / "dataset" / "artifacts" / "candidate_gallery.html"
OUTPUT = ROOT / "research" / "dataset" / "artifacts" / "s3_candidate_gallery"
IMS_SOURCE = Path(
    "/home/colligo/hs_scripts/claude/dotclaude/scripts/"
    "generate_from_endpoint/gallery_template/imsauth.js"
)


def build() -> None:
    document = SOURCE.read_text(encoding="utf-8")
    document = document.replace("../data/pairs/", "../../3_pairs/")
    document = document.replace("../data/focus_skus/", "../../focus_skus/")
    document = document.replace(
        "</style></head>",
        '</style>\n<link rel="stylesheet" href="./style.css"></head>',
        1,
    )
    document = document.replace(
        "<body><main>",
        '<body><div id="ims"></div><div id="loading" class="loading-screen">Loading...</div>'
        '<div id="content" class="hidden"><main>',
        1,
    )
    document = document.replace(
        "</main></body></html>",
        """</main></div>
<script src="https://auth-stg1.services.adobe.com/imslib/imslib.js"></script>
<script src="./imsauth.js"></script>
<script src="./data.js"></script>
<script src="./main.js"></script>
<script>document.addEventListener("DOMContentLoaded", () => { initializeIMS(); });</script>
</body></html>""",
        1,
    )

    if document.count("<figure") != 52:
        raise RuntimeError("Expected exactly 52 reviewed assets")
    if "../data/" in document:
        raise RuntimeError("A local-only asset path remains in the S3 gallery")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "index.html").write_text(document, encoding="utf-8")
    shutil.copyfile(IMS_SOURCE, OUTPUT / "imsauth.js")
    (OUTPUT / "data.js").write_text(
        'const GALLERY_DATA = {title: "KDP scraped-data candidate review", assets: 52};\n',
        encoding="utf-8",
    )
    (OUTPUT / "main.js").write_text(
        "function onAuthReady() { /* Static review gallery is already rendered. */ }\n",
        encoding="utf-8",
    )
    (OUTPUT / "style.css").write_text(
        """.hidden{display:none!important}.loading-screen{padding:24px;color:#aab4c0}
#ims{position:sticky;top:0;z-index:1000;display:flex;gap:10px;align-items:center;
padding:8px 16px;background:#07090c;border-bottom:1px solid #343b45;color:#aab4c0}
.ims-span{font-size:12px}.ims-button{border:1px solid #555f6c;border-radius:5px;
padding:5px 9px;background:#1a1e24;color:#edf1f6;cursor:pointer}
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    build()
