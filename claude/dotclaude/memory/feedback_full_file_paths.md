# Always render complete absolute file paths

Hooman requires every referenced local file to be shown with its complete absolute filesystem path.

The response renderer may collapse clickable Markdown links even when their visible label contains the absolute
path. Therefore, show every local file path as plain text inside an inline or fenced code block so the complete
path is visibly rendered. Do not rely on a Markdown link alone.

Correct example:

```text
/home/colligo/project/report.md
```

Incorrect examples:

```markdown
[/home/colligo/project/report.md](/home/colligo/project/report.md)
[report.md](/home/colligo/project/report.md)
[Dataset assessment](/home/colligo/project/report.md)
```

This preference applies to all responses and projects.
Whenever communicating a file to Hooman, include the full absolute path as visible plain text;
never substitute only a filename, a relative path, or a hidden clickable link.
