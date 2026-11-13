#!/usr/bin/env python3
"""Fetch the latest decision-relevant SEC filings and extract durable plain text."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
RAW = ROOT / "data" / "primary"
TEXT = ROOT / "data" / "primary_text"
RAW.mkdir(parents=True, exist_ok=True)
TEXT.mkdir(parents=True, exist_ok=True)
HEADERS = {"User-Agent": "Hooman Shariati hshariati@adobe.com"}

SOURCES = {
    "LITE": [("000162828026055726", "lite-20260811.htm"), ("000162828026057358", "lite-20260627.htm")],
    "MRVL": [("000183563226000022", "mrvl-20260827.htm"), ("000183563226000025", "mrvl-20260801.htm")],
    "LRCX": [("000070754926000052", "lrcx-20261021.htm"), ("000070754926000054", "lrcx-20260927.htm")],
    "ANET": [("000159653226000174", "anet-20260804.htm"), ("000159653226000175", "anet-20260630.htm")],
    "ARM": [("000197323926000114", "arm-20260729.htm"), ("000197323926000113", "arm-20260630.htm")],
    "COHR": [("000119312526346860", "d128030d8k.htm"), ("000082031826000020", "iivi-20260630.htm")],
    "KLAC": [("000031920126000032", "klac-20261028.htm"), ("000031920126000034", "klac-20260930.htm")],
    "MSFT": [("000119312526436122", "msft-20261028.htm"), ("000119312526436133", "msft-20260930.htm")],
    "GOOGL": [("000165204426000080", "goog-20261028.htm"), ("000165204426000084", "goog-20260930.htm")],
}

CIKS = {
    "LITE": "1633978", "MRVL": "1835632", "LRCX": "707549", "ANET": "1596532",
    "ARM": "1973239", "COHR": "820318", "KLAC": "319201", "MSFT": "789019",
    "GOOGL": "1652044",
}


def accession_base(symbol: str, accession: str) -> str:
    cik = CIKS[symbol]
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/"


def clean_html(payload: bytes) -> str:
    soup = BeautifulSoup(payload, "html.parser")
    for node in soup(["script", "style"]):
        node.decompose()
    lines = []
    for line in soup.get_text("\n").splitlines():
        line = " ".join(line.split())
        if line:
            lines.append(line)
    return "\n".join(lines)


manifest = {"retrieved_at_utc": datetime.now(timezone.utc).isoformat(), "files": []}
for symbol, filings in SOURCES.items():
    for accession, primary in filings:
        base = accession_base(symbol, accession)
        index = requests.get(base, headers=HEADERS, timeout=30)
        index.raise_for_status()
        listing = BeautifulSoup(index.text, "html.parser")
        names = []
        for anchor in listing.find_all("a", href=True):
            href = anchor["href"].rsplit("/", 1)[-1]
            if href.lower().endswith((".htm", ".html")) and href not in names:
                names.append(href)
        wanted = [primary]
        # Earnings filings usually attach an EX-99.1 release. Include HTML exhibits but exclude
        # SEC navigation/index documents and XBRL rendering fragments.
        for name in names:
            low = name.lower()
            if name == primary or name in wanted:
                continue
            if any(x in low for x in ["index", "header", "r1.htm", "filingsummary"]):
                continue
            if re.search(r"(ex|exhibit|991|99-1|99_1)", low):
                wanted.append(name)
        for name in wanted:
            url = base + name
            response = requests.get(url, headers=HEADERS, timeout=30)
            if response.status_code != 200:
                continue
            stem = f"{symbol}_{accession}_{name}".replace("/", "_")
            raw_path = RAW / stem
            text_path = TEXT / (stem.rsplit(".", 1)[0] + ".txt")
            raw_path.write_bytes(response.content)
            text_path.write_text(clean_html(response.content))
            manifest["files"].append({
                "symbol": symbol,
                "accession": accession,
                "primary": name == primary,
                "filename": name,
                "url": url,
                "sha256": hashlib.sha256(response.content).hexdigest(),
                "bytes": len(response.content),
                "text_path": str(text_path.relative_to(ROOT)),
            })

(ROOT / "data" / "sec_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True))
print(f"saved {len(manifest['files'])} SEC documents")
for row in manifest["files"]:
    print(row["symbol"], row["filename"], row["bytes"])
