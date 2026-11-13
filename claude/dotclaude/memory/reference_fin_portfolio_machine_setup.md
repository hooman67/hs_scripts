---
name: reference-fin-portfolio-machine-setup
description: Portfolio Google Sheets credential locations and fin-check dependencies on the Linux machine.
type: reference
---

# Portfolio access on the Linux machine

Verified 2026-10-13 (America/Los_Angeles). Hooman authorized installing the existing key and recording its location.

- Standard service-account key: `/home/colligo/.claude/hshariati/portfolio_sheets_sa.json`.
- Existing source copy on the mounted home: `/sensei-fs/users/hshariati/laser_log/google_key.json`.
- The existing key successfully opened the portfolio spreadsheet and `FR_Portfolio` tab. A new key was not needed.
- The standard copy has mode `600`; its parent directory has mode `700`. Keep both copies outside version control. Never print or put key contents in research files.
- Installed `yfinance`, `gspread`, and `google-auth` into `/opt/venv`, enabling the skill's documented Python command.
- Google Sheets client: `/home/colligo/hs_scripts/claude/fin_research/portfolio/dashboard/sheets_client.py`.
- Portfolio workflow: `/home/colligo/hs_scripts/claude/dotclaude/commands/fin_check.md`.

Before future runs, verify access with the existing key. On a newly provisioned machine, check the mounted source before asking Hooman for a new credential. The local holdings JSON is an old fallback; use the live sheet and verify quote timestamps.

This stores credential locations only, never credential values.
