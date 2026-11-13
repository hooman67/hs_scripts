# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml", "browser-cookie3", "pycryptodomex"]
# ///
"""Create or update a Confluence wiki page (uses curl + browser cookies for CSE)."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

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


def curl_json(method, url, token, cookie_header, data=None):
    """Run curl and return parsed JSON response."""
    cmd = [
        "curl", "-s", "-X", method, url,
        "-H", f"Authorization: Bearer {token}",
        "-H", f"Cookie: {cookie_header}",
        "-H", "Content-Type: application/json",
        "-H", "Accept: application/json",
    ]
    if data:
        cmd += ["-d", json.dumps(data)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None, f"curl failed: {result.stderr}"
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError:
        return None, result.stdout


def get_page(page_id, token, cookie_header):
    """Fetch current page to get version number for updates."""
    url = f"{WIKI_BASE}/rest/api/content/{page_id}?expand=version,space,body.storage"
    return curl_json("GET", url, token, cookie_header)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-id", default=None, help="Page ID to update. Omit to create new page.")
    parser.add_argument("--title", default=None, help="Page title (required for create, optional for update)")
    parser.add_argument("--space", default=None, help="Space key (required for create)")
    parser.add_argument("--body", default=None, help="Page body in Confluence storage format (HTML)")
    parser.add_argument("--body-file", default=None, help="Read body from a file instead of --body")
    parser.add_argument("--parent-id", default=None, help="Parent page ID (for create)")
    parser.add_argument("--append", action="store_true", help="Append body to existing content instead of replacing")
    args = parser.parse_args()

    creds = load_creds()
    token = creds["confluence"]["token"]
    cookie_header = get_cookie_header()

    body_content = args.body
    if args.body_file:
        body_content = Path(args.body_file).read_text()

    if not body_content:
        print(json.dumps({"error": "Provide --body or --body-file"}))
        sys.exit(1)

    if args.page_id:
        # UPDATE existing page
        page, err = get_page(args.page_id, token, cookie_header)
        if not page:
            print(json.dumps({"error": err or f"Page {args.page_id} not found"}))
            sys.exit(1)

        current_version = page["version"]["number"]
        title = args.title or page["title"]

        if args.append:
            existing_body = page.get("body", {}).get("storage", {}).get("value", "")
            body_content = existing_body + body_content

        payload = {
            "version": {"number": current_version + 1},
            "title": title,
            "type": "page",
            "body": {"storage": {"value": body_content, "representation": "storage"}},
        }

        data, err = curl_json("PUT", f"{WIKI_BASE}/rest/api/content/{args.page_id}", token, cookie_header, payload)
        if not data:
            print(json.dumps({"error": err}))
            sys.exit(1)

        if "id" not in data:
            print(json.dumps({"error": json.dumps(data)}))
            sys.exit(1)

        print(json.dumps({
            "ok": True,
            "action": "updated",
            "id": data["id"],
            "title": data["title"],
            "version": data["version"]["number"],
            "url": f"{WIKI_BASE}/pages/viewpage.action?pageId={data['id']}",
        }, indent=2))

    else:
        # CREATE new page
        if not args.title:
            print(json.dumps({"error": "--title is required when creating a new page"}))
            sys.exit(1)
        if not args.space:
            print(json.dumps({"error": "--space is required when creating a new page"}))
            sys.exit(1)

        payload = {
            "type": "page",
            "title": args.title,
            "space": {"key": args.space},
            "body": {"storage": {"value": body_content, "representation": "storage"}},
        }

        if args.parent_id:
            payload["ancestors"] = [{"id": args.parent_id}]

        data, err = curl_json("POST", f"{WIKI_BASE}/rest/api/content", token, cookie_header, payload)
        if not data:
            print(json.dumps({"error": err}))
            sys.exit(1)

        if "id" not in data:
            print(json.dumps({"error": json.dumps(data)}))
            sys.exit(1)

        print(json.dumps({
            "ok": True,
            "action": "created",
            "id": data["id"],
            "title": data["title"],
            "url": f"{WIKI_BASE}/pages/viewpage.action?pageId={data['id']}",
        }, indent=2))


if __name__ == "__main__":
    main()
