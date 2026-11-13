"""
Google Sheets client for the portfolio dashboard.
Built 2026-07-08. Reads/writes Hooman's portfolio Sheet via a service account.

SETUP: see dashboard/SETUP.md. Requires ~/.claude/hshariati/portfolio_sheets_sa.json
(service-account key) and the Sheet shared with that account's client_email.

Usage:
  /opt/venv/bin/python3 dashboard/sheets_client.py --test          # confirm access, list tabs
  /opt/venv/bin/python3 dashboard/sheets_client.py --dump <tab>    # print a tab's values+formulas
  (Claude imports build_dashboard() from here to construct/refresh the tabs.)

The SHEET_ID is read from dashboard/sheet_config.json (so it's not hard-coded / committed
with a personal URL). Create it as: {"sheet_id": "1diOiW7fk9Q5fyyCoriON-IYN8Yc-PnrixKh2PtFwQkU"}
"""
import sys, json, os
from pathlib import Path

# SA key location: prefer the standard creds dir, fall back to where Hooman placed it.
# (Both are OUTSIDE the git repo, so the secret is never committed.)
_SA_CANDIDATES = [
    os.path.expanduser("~/.claude/hshariati/portfolio_sheets_sa.json"),
    "/mnt/localssd/laser_log/google_key.json",
]
SA_KEY = next((p for p in _SA_CANDIDATES if os.path.exists(p)), _SA_CANDIDATES[0])
CONFIG = Path(__file__).parent / "sheet_config.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

def get_client():
    import gspread
    from google.oauth2.service_account import Credentials
    if not os.path.exists(SA_KEY):
        sys.exit(f"ERROR: service-account key not found at {SA_KEY}\n"
                 f"→ Follow dashboard/SETUP.md steps 1-5 first.")
    creds = Credentials.from_service_account_file(SA_KEY, scopes=SCOPES)
    return gspread.authorize(creds)

def get_sheet_id():
    if CONFIG.exists():
        return json.load(open(CONFIG))["sheet_id"]
    sys.exit(f"ERROR: {CONFIG} missing. Create it: "
             '{"sheet_id": "<the id from your Sheet URL>"}')

def open_sheet():
    return get_client().open_by_key(get_sheet_id())

def test_access():
    sh = open_sheet()
    print(f"✅ Connected to: '{sh.title}'")
    print(f"Tabs: {[ws.title for ws in sh.worksheets()]}")
    # write+read round-trip on a scratch cell of the first tab
    ws = sh.sheet1
    print(f"First tab '{ws.title}' size: {ws.row_count}x{ws.col_count}")
    print("✅ Read OK. (Write test skipped to avoid touching your data; "
          "Claude will write to NEW tabs.)")

def dump_tab(name):
    sh = open_sheet()
    ws = sh.worksheet(name)
    vals = ws.get_all_values()
    formulas = ws.get_all_values(value_render_option='FORMULA')
    print(f"=== {name}: {len(vals)} rows ===")
    for i,(vrow,frow) in enumerate(zip(vals[:40], formulas[:40])):
        for j,(v,f) in enumerate(zip(vrow,frow)):
            if f and f != v:  # show cells that are formulas
                col=chr(65+j) if j<26 else '?'
                print(f"  {col}{i+1}: {f}  => {v}")

if __name__ == "__main__":
    if "--test" in sys.argv:
        test_access()
    elif "--dump" in sys.argv:
        dump_tab(sys.argv[sys.argv.index("--dump")+1])
    else:
        print(__doc__)
