Frame.io helper: download/upload folders and gather comments.

Usage:
- `/frame whoami` — sanity check auth
- `/frame list <url-or-uuid>` — list immediate children of a folder
- `/frame comments <url-or-uuid> [--out PATH]` — dump all comments under a folder/asset to CSV
- `/frame download <url-or-uuid> <local_dir>` — recursively download originals + comments.csv
- `/frame upload <local_path> <parent-url-or-uuid>` — upload a local file or folder under a Frame.io folder

`<url-or-uuid>` can be either a Frame.io URL (e.g. `https://app.frame.io/projects/<id>` or `https://app.frame.io/player/<id>`) or a raw UUID. The last UUID in the URL is used. For project URLs, the script resolves to the project's root folder automatically.

Parse $ARGUMENTS to extract the subcommand and its arguments. Then run:

```
uv run --script ~/.claude/scripts/frame.py <subcommand> <args...>
```

Pass through unknown flags exactly as the user typed them (e.g. `--out`, `--no-comments`).

After running, parse the JSON the script prints on stdout and summarize for the user (counts, output paths, any error log). If the script exits non-zero with a credentials error, tell the user to add a `frame.token` entry to `~/.claude/hshariati/credentials.yaml` (developer token from <https://developer.frame.io/app/tokens>, scopes: `project.read`, `asset.read`, `asset.create`, `comment.read`).

Notes:
- Downloads use 6 worker threads; uploads use 4. Auto-skips files that already exist locally (resume-friendly).
- Comments CSV columns: folder, asset_name, asset_id, comment_id, parent_comment_id, owner_name, owner_email, text, timestamp_seconds, has_drawing, completed, annotation, created_at, updated_at. Replies appear as separate rows with `parent_comment_id` set.
- This is the legacy v3 (api.frame.io/v2) flow. Frame.io v4 (Adobe IMS) is not supported by this skill.
