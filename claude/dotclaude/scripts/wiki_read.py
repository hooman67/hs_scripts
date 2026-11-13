# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml", "browser-cookie3", "pycryptodomex"]
# ///
"""Read a Confluence wiki page (uses curl + browser cookies for CSE)."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

import browser_cookie3
import yaml

CREDS_PATH = Path.home() / ".claude" / "hshariati" / "credentials.yaml"
WIKI_BASE = "https://wiki.corp.adobe.com"


def load_creds():
    with open(CREDS_PATH) as f:
        return yaml.safe_load(f)


def get_cookie_header():
    """Extract wiki cookies from Chrome."""
    cj = browser_cookie3.chrome(domain_name="wiki.corp.adobe.com")
    return "; ".join(f"{c.name}={c.value}" for c in cj)


def curl_json(url, token, cookie_header):
    """Run curl GET and return parsed JSON response."""
    cmd = [
        "curl", "-s", url,
        "-H", f"Authorization: Bearer {token}",
        "-H", f"Cookie: {cookie_header}",
        "-H", "Accept: application/json",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None, f"curl failed: {result.stderr}"
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError:
        return None, result.stdout


def strip_html(html):
    """Simple HTML tag stripping."""
    text = re.sub(r"<br\s*/?>", "\n", html)
    text = re.sub(r"</?p>", "\n", text)
    text = re.sub(r"<li>", "- ", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_page_ref(ref):
    """Parse a page ID, URL with pageId param, or /display/SPACE/Title URL."""
    if ref.isdigit():
        return {"id": ref}

    parsed = urlparse(ref)
    qs = parse_qs(parsed.query)
    if "pageId" in qs:
        return {"id": qs["pageId"][0]}

    # /display/SPACE/Page+Title
    m = re.match(r"/display/([^/]+)/(.+)", parsed.path)
    if m:
        return {"space": m.group(1), "title": unquote(m.group(2).replace("+", " "))}

    # /wiki/spaces/SPACE/pages/ID or similar
    if parsed.scheme:
        m2 = re.match(r".*/pages/(\d+)", parsed.path)
        if m2:
            return {"id": m2.group(1)}

    # /spaces/SPACE/pages/ID/Title
    m3 = re.match(r"/spaces/([^/]+)/pages/(\d+)", parsed.path)
    if m3:
        return {"id": m3.group(2)}

    return {"id": ref}  # fallback: treat as ID


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("page", help="Page ID, URL with pageId, or /display/SPACE/Title URL")
    args = parser.parse_args()

    creds = load_creds()
    token = creds["confluence"]["token"]
    cookie_header = get_cookie_header()

    ref = parse_page_ref(args.page)

    if "id" in ref:
        url = f"{WIKI_BASE}/rest/api/content/{ref['id']}?expand=body.storage,version,space"
    else:
        title_encoded = quote(ref["title"])
        url = f"{WIKI_BASE}/rest/api/content?title={title_encoded}&spaceKey={ref['space']}&expand=body.storage,version,space"

    data, err = curl_json(url, token, cookie_header)
    if not data:
        print(json.dumps({"error": err}))
        sys.exit(1)

    # If search result, take first match
    if "results" in data:
        if not data["results"]:
            print(json.dumps({"error": f"No page found for {ref}"}))
            sys.exit(1)
        data = data["results"][0]

    body_html = data.get("body", {}).get("storage", {}).get("value", "")
    space = data.get("space", {}).get("key", "")
    version = data.get("version", {}).get("number", "")
    modified_by = data.get("version", {}).get("by", {}).get("displayName", "")
    modified_when = data.get("version", {}).get("when", "")

    print(json.dumps({
        "ok": True,
        "id": data.get("id", ""),
        "title": data.get("title", ""),
        "space": space,
        "url": f"{WIKI_BASE}/pages/viewpage.action?pageId={data.get('id', '')}",
        "version": version,
        "modified_by": modified_by,
        "modified_when": modified_when,
        "body": strip_html(body_html)[:5000],
    }, indent=2))


if __name__ == "__main__":
    main()
