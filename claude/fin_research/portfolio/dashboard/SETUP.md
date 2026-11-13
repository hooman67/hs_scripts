# Dashboard Setup — Google Sheets API access (one-time, ~5 min)

**Goal:** give Claude (via a script) programmatic READ+WRITE access to your portfolio Google Sheet, so
Claude can build and maintain the dashboard directly — while YOU keep full ownership and can edit/use it
without Claude (it's a normal Sheet with live GOOGLEFINANCE prices + formula-driven buy/sell logic).

**Design decision (locked 2026-07-08):** Google Sheet is the **single source of truth**. It survives loss
of Claude access. Claude maintains it via a service account. An HTML view can be generated from it later
(optional), but the Sheet is primary.

---

## Why a service account (not your personal login)?
Your existing GCP tooling (`gcp_gemini.py`) uses short-lived **Foundry work** tokens for Vertex AI — wrong
scope for a personal Sheet you own. A **service account** is a "robot" Google identity with its own email;
you simply *share* your Sheet with that email (like sharing with a coworker). It's revocable, scoped to
only the sheets you share, and its key lives locally in `~/.claude/hshariati/`.

---

## Step-by-step (do this once)

### 1. Create a Google Cloud project (free)
- Go to https://console.cloud.google.com/
- Top bar → project dropdown → **New Project** → name it e.g. `hooman-portfolio` → Create.
- (Personal Gmail is fine. This is separate from your Adobe/Foundry GCP.)

### 2. Enable the two APIs
- With the project selected, go to **APIs & Services → Library**.
- Search **"Google Sheets API"** → Enable.
- Search **"Google Drive API"** → Enable. (gspread needs Drive to open sheets by URL.)

### 3. Create the service account
- **APIs & Services → Credentials → Create Credentials → Service account**.
- Name: `portfolio-bot` → Create and continue → (skip optional roles) → Done.

### 4. Download its JSON key
- Click the new service account → **Keys** tab → **Add key → Create new key → JSON** → Create.
- A `.json` file downloads. **This is the secret.**
- Move it to: `~/.claude/hshariati/portfolio_sheets_sa.json`
  ```bash
  mv ~/Downloads/hooman-portfolio-*.json ~/.claude/hshariati/portfolio_sheets_sa.json
  chmod 600 ~/.claude/hshariati/portfolio_sheets_sa.json
  ```

### 5. Share your Sheet with the service account
- Open the JSON file and copy the `"client_email"` value — it looks like
  `portfolio-bot@hooman-portfolio.iam.gserviceaccount.com`.
- Open your Google Sheet → **Share** → paste that email → give it **Editor** → send.
  (No real email is sent; it just grants the robot access.)

### 6. Tell Claude you're done
- Say "service account is set up" and Claude will run `dashboard/sheets_client.py --test` to confirm
  read+write access, then build the dashboard tabs.

---

## Security notes
- The JSON key = full access to any sheet you share with that service account. Keep it in
  `~/.claude/hshariati/` (already git-ignored per the repo's .gitignore — VERIFY before committing).
- To revoke: delete the key in the Cloud console, or un-share the Sheet.
- The service account can ONLY touch sheets you explicitly share with it — not your whole Drive.

---

## What Claude builds once access works (see `DASHBOARD_SPEC.md`)
1. **Dashboard tab** — allocation vs target, drift, "buy/sell $ needed" per sleeve (formula-driven).
2. **Holdings tab** — every position, live GOOGLEFINANCE price, market value, weight, thesis, buy/sell trigger.
3. **Targets tab** — the ideal-allocation model (editable numbers → dashboard recomputes).
4. **Trade log tab** — record executed buys/sells; feeds the holdings.
All the buy/sell math lives as **sheet formulas**, so it keeps working with zero Claude involvement.
