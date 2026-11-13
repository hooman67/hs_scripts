Read a Confluence wiki page.

Usage: /wiki-read <page_id_or_url>

Parse $ARGUMENTS to extract a page reference. This can be:
- A numeric page ID (e.g. 12345)
- A URL with pageId param (e.g. https://wiki.corp.adobe.com/pages/viewpage.action?pageId=12345)
- A /display/SPACE/Title URL (e.g. https://wiki.corp.adobe.com/display/FIREFLY/My+Page)

Then run:

```
uv run --script ~/.claude/scripts/wiki_read.py -- "<page_id_or_url>"
```

After running, present the page title, space, last modified info, and body content in readable format.

Note: Confluence (wiki.corp.adobe.com) may be down for maintenance. If the request fails, let the user know.
