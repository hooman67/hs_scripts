Create or update a Confluence wiki page.

Usage:
  /wiki-write create space=SPACEKEY title="Page Title" [parent_id=12345] body="<p>Content here</p>"
  /wiki-write update page_id=12345 body="<p>New content</p>"
  /wiki-write append page_id=12345 body="<p>Appended content</p>"

Parse $ARGUMENTS to determine the action:
- **create**: requires title and space, optional parent_id
- **update**: requires page_id, replaces body entirely
- **append**: requires page_id, appends to existing body

The body should be in Confluence storage format (HTML). Convert the user's markdown or plain text to simple HTML before passing it.

For create:
```
uv run --script ~/.claude/scripts/wiki_write.py -- --title "<title>" --space "<space>" --parent-id "<parent_id>" --body "<html_body>"
```

For update:
```
uv run --script ~/.claude/scripts/wiki_write.py -- --page-id "<page_id>" --body "<html_body>"
```

For append:
```
uv run --script ~/.claude/scripts/wiki_write.py -- --page-id "<page_id>" --body "<html_body>" --append
```

For large bodies, write the content to a temp file and use `--body-file`:
```
uv run --script ~/.claude/scripts/wiki_write.py -- --page-id "<page_id>" --body-file "/tmp/wiki_body.html"
```

After running, show the user the page URL and confirm what was done.

Note: Confluence (wiki.corp.adobe.com) may be down for maintenance. If the request fails, let the user know.
