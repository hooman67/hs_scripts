#!/usr/bin/env python3
"""
fin_check.py — daily price-action pull for Hooman's portfolio review.

Pulls live prices + 1d/5d/20d moves for current holdings AND the buy/sell watchlist,
flags notable moves, and prints a compact table the agent then interprets against the
thesis (sell-into-strength / buy-into-weakness / hold). Read-only; makes NO trades and
writes NO records.

Reads holdings, cash, sleeves, and targets from the live FR_Portfolio Google Sheet when available,
then falls back to the generated holdings JSON. Groups by role so the agent can reason per-sleeve.

Usage:
  /opt/venv/bin/python3 ~/.claude/scripts/fin_check.py            # full table
  /opt/venv/bin/python3 ~/.claude/scripts/fin_check.py --json     # machine-readable
  /opt/venv/bin/python3 ~/.claude/scripts/fin_check.py --movers   # only |1d|>=3% or |5d|>=5%

Requires: yfinance (curl_cffi backend; bare urllib gets 429 from Yahoo).
"""
import sys, json, os, math
from datetime import datetime, timezone

# --- MACRO + BUY WATCHLIST (things NOT necessarily held yet) ---
MACRO = ["CL=F", "BZ=F", "NG=F", "GC=F", "HG=F"]  # WTI, Brent, natgas, gold, copper futures
BUY_WATCHLIST = ["VTI", "VXUS", "VWO", "JQUA", "DBE", "NLR", "COPX", "PICK",
                 "VHT", "IHI", "LLY", "GLDM", "SHLD", "VPU", "SOXQ", "LRCX", "KLAC"]

# Research watches have no sleeve target and are not automatic buys. They remain visible so an
# accepted thesis can be monitored without changing the portfolio's allocation model.
RESEARCH_WATCHES = {
    "SOXQ": {
        "label": "Semiconductor tactical overweight",
        "starter": 85.0,
        "second": 80.0,
        "starter_pct": 0.005,
        "max_pct": 0.01,
        "note": "Fund from VTI/JQUA substitution; no new permanent sleeve",
    },
    "LRCX": {
        "label": "AI semiconductor-equipment quality watch",
        "review": 205.0,
        "review_only": True,
        "max_pct": 0.01,
        "note": "Re-underwrite results/China/WFE cycle; any position replaces JQUA dollar-for-dollar",
    },
    "KLAC": {
        "label": "Semiconductor process-control moat watch",
        "review": 140.0,
        "review_only": True,
        "max_pct": 0.015,
        "note": "Secondary watch; fresh GAAP valuation review required and combined LRCX+KLAC <=1.5%",
    },
}

# --- Fallback sleeve targets. The live sheet overrides these when reachable. ---
SLEEVE_TARGET = {
    "Cash (50/50 USD/CAD)": 0.185, "Global equity core": 0.15,
    "Treasuries (VGIT)": 0.05,
    "EM/China": 0.05, "Quality compounders": 0.055,
    "oil-companies": 0.06, "ref_oil_prod": 0.02, "nat_gas": 0.01,
    "Gold core": 0.15, "Utilities": 0.025, "Financials": 0.02,
    "uranium/nuclear": 0.035, "grid/electrification": 0.015,
    "copper": 0.02, "industrial_metals": 0.01, "Agriculture": 0.03,
    "Healthcare": 0.055, "Defense": 0.015, "Crypto": 0.02,
    "Silver/Plat": 0.01, "(exit) — SELL & redeploy": 0.0, "Speculation": 0.015,
}
# NOTE (2026-07-26): dropped the 5% Short-TIPS/VTIP sleeve → moved to Gold (9%→14%). Hooman's call:
# VTIP not wanted; gold is the better stagflation + USD-debasement hedge. Cash stays DRY POWDER for a
# recession (do NOT deploy to equities yet). See the STAGFLATION PLAYBOOK in fin_check.md.
# ticker -> sleeve (mirrors the dashboard HOLD_MAP; (exit) names roll up to their sale bucket)
TICKER_SLEEVE = {
    "Physical-Gold":"Gold core","TSE:MNT":"Gold core","AEM":"Gold core","EMPYF":"Gold core",
    "WPM":"Silver/Plat","XOM":"Energy","TSE:CNQ":"Energy","SLB":"Energy","TSE:CVE":"Energy",
    "TSE:TOU":"Energy","UNG":"Energy","CCJ":"Uranium/AI-power","BWXT":"Uranium/AI-power",
    "CEG":"Uranium/AI-power","TSE:URC":"Uranium/AI-power","GEV":"Uranium/AI-power",
    "ETN":"Uranium/AI-power","SMR":"Uranium/AI-power","BHP":"Copper",
    "TSE:COP.U":"Copper","NTCPF":"Copper","CF":"Ag","PDBA":"Ag","KHC":"(exit)","PFE":"Healthcare",
    "LLY":"Quality compounders","AMZN":"Quality compounders","GOOGL":"Quality compounders",
    "CI":"Financials",
    "KWEB":"EM/China","MCHI":"EM/China","IEMG":"EM/China","BABA":"EM/China",
    "VTI":"Global equity core","VXUS":"Global equity core","ICOP":"copper",
    "MXI":"industrial_metals",
    "XLU":"Utilities (XLU)","BTCUSD-1":"Crypto","BTCCAD":"Crypto","BTCUSD-2":"Crypto",
    "AUR":"Speculation","CRCL":"Crypto","TSE:SHOP":"Speculation","UBER":"Speculation",
    "TSE:CCO":"Uranium/AI-power","NLR":"Uranium/AI-power",
}
FX_CADUSD = 0.7052  # updated on each pull below

# --- FULL HOLDINGS are loaded dynamically from the dashboard source of truth so this
# never drifts from what Hooman actually owns (incl. the not-yet-sold "(exit)" names). ---
HOLDINGS_JSON = os.path.expanduser(
    "~/hs_scripts/claude/fin_research/portfolio/data/holdings_live.json")
PROJECT_DIR = os.path.expanduser("~/hs_scripts/claude/fin_research")
PORTFOLIO_SOURCE = None

# User-confirmed 2026-10-15: sell all current Speculation holdings once profitable.
# Pin these names so retagging a sleeve cannot silently remove the pending exit.
# Any additional holding currently tagged Speculation is covered automatically.
SELL_ON_PROFIT = {"LULU.TO", "TTD", "NKE", "CLX", "SHOP.TO", "UBER", "ASTS", "FIS"}
PROFIT_EXIT_GROUP = "HELD — sell when profitable (Speculation exit queue)"

# yfinance symbol fixes for a few tickers whose stored 'yahoo' differs
YF_FIX = {
    "BATS:ARKK": "ARKK", "NYSE:NIO": "NIO", "NYSE:SBSW": "SBSW",
    "TSE:COP.U": "COP-U.TO", "TSE:CCO": "CCO.TO",
    "TSE:CGY": "CGY.TO", "TSE:EFX": "EFX.TO", "TSE:BDGI": "BDGI.TO",
    "TSE:VNP": "VNP.TO", "TSE:FTG": "FTG.TO",
}
# crypto/physical priced elsewhere or unreliable on yfinance → skip in the daily price pull
SKIP = {"Physical-Gold"}

def _num(value, default=0.0):
    try:
        return float(str(value).replace("$", "").replace(",", "").replace("%", "").strip())
    except Exception:
        return default

def _sheet_yahoo(symbol, name):
    fixes = {
        "TSE:MNT": "MNT.TO", "TSE:COP.U": "COP-U.TO", "NYSE:NIO": "NIO",
        "NYSE:SBSW": "SBSW", "NYSE:BRK.B": "BRK-B", "BATS:ARKK": "ARKK",
        "TSE:CNQ": "CNQ.TO", "TSE:TOU": "TOU.TO", "TSE:CCO": "CCO.TO",
        "TSE:AEM": "AEM.TO", "CVE:NCX": "NCX.V",
        "TSE:SHOP": "SHOP.TO", "TSE:CGY": "CGY.TO", "TSE:EFX": "EFX.TO",
        "TSE:BDGI": "BDGI.TO", "TSE:VNP": "VNP.TO", "TSE:FTG": "FTG.TO",
    }
    if name.startswith("Bitcoin"):
        return "BTC-USD"
    if name.startswith("Physical Gold"):
        return None
    if name.startswith("NorthStar Clean Tech"):
        return "ROOF.V"
    return fixes.get(symbol, symbol or None)

def _load_live_sheet():
    dashboard_dir = os.path.join(PROJECT_DIR, "portfolio", "dashboard")
    if dashboard_dir not in sys.path:
        sys.path.insert(0, dashboard_dir)
    from sheets_client import open_sheet

    ws = open_sheet().worksheet("FR_Portfolio")
    values = ws.get("A1:T500", value_render_option="UNFORMATTED_VALUE")
    holdings_header = next(i for i, row in enumerate(values)
                           if len(row) > 1 and row[0] == "Name" and row[1] == "GF Symbol")
    rows = []
    for row in values[holdings_header + 1:]:
        row = list(row) + [""] * (20 - len(row))
        name, symbol, sleeve = str(row[0]).strip(), str(row[1]).strip(), str(row[2]).strip()
        if not name or not sleeve:
            continue
        shares = _num(row[3])
        if shares <= 0:
            continue
        ticker = symbol or name
        if name.startswith("Bitcoin") or name.startswith("Physical Gold"):
            ticker = name
        rows.append({
            "ticker": ticker, "name": name, "yahoo": _sheet_yahoo(symbol, name),
            "sleeve": sleeve, "shares": shares, "live_price": _num(row[4]),
            "ccy": str(row[5]).strip() or "USD", "avg_buy": _num(row[9]),
            "book_usd": _num(row[10]), "account": str(row[16]).strip(),
            "thesis": str(row[13]).strip(),
        })

    targets = {}
    target_header = next(i for i, row in enumerate(values)
                         if len(row) > 1 and row[0] == "Sleeve" and row[1] == "Target %")
    for row in values[target_header + 1:]:
        if row and row[0] == "TOTAL":
            break
        if len(row) > 1 and row[0]:
            name = "(exit)" if str(row[0]).startswith("(exit)") else str(row[0])
            targets[name] = _num(row[1])
    if not targets or not math.isclose(sum(targets.values()), 1.0, abs_tol=1e-6):
        raise ValueError("Live allocation targets do not sum to 100%")

    cash = None
    for row in values:
        if row and row[0] == "Total cash":
            cash = _num(row[3] if len(row) > 3 else 0)
            break
    if cash is None:
        raise ValueError("Total cash row not found in FR_Portfolio")
    return {"rows": rows, "cash_usd": cash, "targets": targets, "source": "FR_Portfolio"}

def load_portfolio_source():
    global PORTFOLIO_SOURCE
    if PORTFOLIO_SOURCE is not None:
        return PORTFOLIO_SOURCE
    try:
        PORTFOLIO_SOURCE = _load_live_sheet()
        return PORTFOLIO_SOURCE
    except Exception as sheet_error:
        d = json.load(open(HOLDINGS_JSON))
        d["targets"] = dict(SLEEVE_TARGET)
        d["source"] = f"holdings_live.json fallback ({sheet_error})"
        PORTFOLIO_SOURCE = d
        return PORTFOLIO_SOURCE

def _is_profit_exit(row):
    symbol = row.get("yahoo") or _sheet_yahoo(row.get("ticker", ""), row.get("name", ""))
    return (str(row.get("sleeve", "")).strip().lower() == "speculation"
            or symbol in SELL_ON_PROFIT)


def load_holdings_groups():
    """Return grouped holdings from the live source: held names split into
    (exit) vs by-sleeve, so the check covers EVERYTHING owned."""
    groups = {"MACRO / COMMODITIES": MACRO}
    try:
        d = load_portfolio_source()
        held, exiters, profit_exiters = [], [], []
        for r in d["rows"]:
            tk = r["ticker"]
            yh = r["yahoo"] if "yahoo" in r else YF_FIX.get(tk, tk)
            if tk in SKIP or not yh:
                continue
            if tk.startswith("BTC"):   # only real BTC lots → coin price; MARA/miners keep their own ticker
                yh = "BTC-USD"
            # exit flag: the dashboard tags these; infer from thesis/sleeve if present
            (profit_exiters if _is_profit_exit(r) else exiters if _is_exit(r) else held).append(yh)
        # dedupe preserve order
        held = list(dict.fromkeys(held)); exiters = list(dict.fromkeys(exiters))
        groups["HELD — core/sleeves (trim strength / hold)"] = held
        if exiters:
            groups["HELD — (exit) queue (sell into any bounce)"] = exiters
        if profit_exiters:
            groups[PROFIT_EXIT_GROUP] = list(dict.fromkeys(profit_exiters))
    except Exception as e:
        # fallback: static list if the source file isn't reachable
        groups["HELD (fallback static)"] = ["XOM","CNQ.TO","SLB","CVE.TO","TOU.TO","UNG","GLD","AEM",
            "WPM","CCJ","BWXT","CEG","MNT.TO","VTI","VXUS","XLU","GOOGL","AMZN","LLY","PFE","KWEB",
            "BABA","CF","PDBA","KHC","BHP","BTC-USD"]
        groups["_load_error"] = [str(e)[:60]]
    groups["BUY WATCHLIST (underweight sleeves)"] = BUY_WATCHLIST
    return groups

def _is_exit(r):
    """Heuristic: a holding is in the exit queue if its thesis starts with SELL,
    or theme is one of the known-exit micro/legacy buckets."""
    if str(r.get("sleeve", "")).startswith("(exit)"):
        return True
    th = str(r.get("thesis", "") or r.get("THESIS", "")).upper()
    if th.startswith("SELL"):
        return True
    # from the dashboard we know these tickers are (exit) — belt & suspenders
    EXIT_TICKERS = {"AA","AEVA","BIDU","MARA","CHPT","NYSE:NIO","F","LCID","RIVN","CAG",
                    "JMIA","NYSE:SBSW","CSGP","SBUX","GLBS","KHC","XME","BATS:ARKK","BOIL",
                    "ROOF.V","SQQQ"}
    return r["ticker"] in EXIT_TICKERS

# GROUPS is built at runtime
GROUPS = None

def pull(tickers):
    import yfinance as yf, warnings
    import pandas as pd
    from concurrent.futures import ThreadPoolExecutor
    warnings.filterwarnings("ignore")
    uniq = sorted({t for g in tickers.values() for t in g})
    data = yf.download(uniq, period="3mo", interval="1d", progress=False, auto_adjust=True)["Close"]
    out = {}
    # grab live FX for CAD holdings sizing
    try:
        fx = yf.Ticker("CADUSD=X").info.get("regularMarketPrice") or FX_CADUSD
        out["FX_CADUSD"] = fx
    except Exception:
        out["FX_CADUSD"] = FX_CADUSD
    def metadata(ticker):
        try:
            obj = yf.Ticker(ticker)
            obj.history(period="5d")
            return ticker, obj.get_history_metadata()
        except Exception:
            return ticker, {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        meta = dict(pool.map(metadata, uniq))
    for t in uniq:
        try:
            s = data[t].dropna().copy()
            s.index = pd.to_datetime(s.index).tz_localize(None).normalize()
            m = meta.get(t, {})
            px, ts = m.get("regularMarketPrice"), m.get("regularMarketTime")
            quote_time = None
            if px and ts and math.isfinite(float(px)):
                quote_time = (pd.Timestamp(ts, unit="s", tz="UTC")
                              if isinstance(ts, (int, float)) else pd.Timestamp(ts))
                quote_time = (quote_time.tz_localize("UTC") if quote_time.tzinfo is None
                              else quote_time.tz_convert("UTC"))
                date = quote_time.tz_convert(m.get("exchangeTimezoneName") or "America/New_York")
                date = pd.Timestamp(date.date())
                if len(s) == 0 or date >= s.index[-1]:
                    s.loc[date] = float(px)
                    s = s.sort_index()
            if len(s) == 0:
                out[t] = {"err": "no data"}; continue
            last = float(s.iloc[-1])
            out[t] = {"last": last, "date": str(s.index[-1].date()),
                      "quote_time": str(quote_time) if quote_time is not None else None,
                      "currency": m.get("currency")}
            for n in (1, 3, 5, 20):
                out[t][f"d{n}"] = (last / float(s.iloc[-n-1]) - 1) * 100 if len(s) > n else None
        except Exception as e:
            out[t] = {"err": str(e)[:40]}
    return out

def sizing(prices):
    """Compute per-sleeve current$ vs target$ (trim/buy needed) and per-position$,
    so every verdict can carry a dollar amount. Uses live prices × share counts from
    the holdings source + cash from the same file. Returns (sleeve_rows, pos_by_ticker,
    total). Prices keyed by the yfinance symbol used in the pull."""
    try:
        d = load_portfolio_source()
    except Exception as e:
        return None, None, None
    fx = prices.get("FX_CADUSD", FX_CADUSD)
    rows = d["rows"]
    # per-position live USD value
    pos = {}
    sleeve_cur = {}
    noncash = 0.0
    for r in rows:
        tk = r["ticker"]
        yh = r["yahoo"] if "yahoo" in r else YF_FIX.get(tk, tk)
        if tk.startswith("BTC"): yh="BTC-USD"   # only actual BTC lots use the coin price (NOT MARA the miner stock)
        pr = prices.get(yh, {})
        px = pr.get("last")
        if px is None:  # physical gold / missing → fall back to stored live_price/avg
            px = r.get("live_price") or r.get("avg_buy")
        sh = r.get("shares") or 0
        ccy = pr.get("currency") or ("USD" if yh in {"BTC-USD", "COP-U.TO"} else r.get("ccy", "USD"))
        mv = px*sh*(fx if ccy=="CAD" else 1.0) if px else 0.0
        basis = r.get("book_usd") or 0.0
        if basis <= 0:
            avg_buy = r.get("avg_buy") or 0.0
            basis = avg_buy*sh*(fx if r.get("ccy") == "CAD" else 1.0)
        pos[tk] = {"mv": mv, "yh": yh, "px": px, "sh": sh, "ccy": ccy,
                   "sleeve": r.get("sleeve") or TICKER_SLEEVE.get(tk, "(exit)"),
                   "basis": basis, "pl": mv-basis, "account": r.get("account", "")}
        sl = pos[tk]["sleeve"]
        sleeve_cur[sl] = sleeve_cur.get(sl,0)+mv
        noncash += mv
    # cash from the holdings file if present, else assume dashboard cash
    cash = d.get("cash_usd")
    if cash is None:
        cash = 280000.0  # fallback; agent should note it's approximate
    total = noncash + cash
    # SGOV and similar explicit cash-equivalent securities share the cash sleeve
    # with account cash.  Add account cash instead of replacing the security MV.
    cash_sleeve = "Cash (50/50 USD/CAD)"
    sleeve_cur[cash_sleeve] = sleeve_cur.get(cash_sleeve, 0.0) + cash
    # build sleeve comparison
    sleeve_rows = []
    for sl, tgtpct in d.get("targets", SLEEVE_TARGET).items():
        cur = sleeve_cur.get(sl, 0.0)
        tgt = tgtpct*total
        sleeve_rows.append({"sleeve":sl, "cur":cur, "cur_pct":cur/total if total else 0,
                            "tgt":tgt, "tgt_pct":tgtpct, "action": tgt-cur})
    return sleeve_rows, pos, total

def meltup_watch():
    """Forced counter-check to the cash-heavy stance: is the market melting up while cash sits idle?
    Pulls VTI over ~6mo + 52wk high. Returns a one-line verdict string. Hooman asked to be reminded."""
    import yfinance as yf, warnings
    warnings.filterwarnings("ignore")
    try:
        h = yf.download("VTI", period="1y", interval="1d", progress=False, auto_adjust=True)["Close"].dropna()
        vti = h["VTI"] if "VTI" in getattr(h, "columns", []) else h
        last = float(vti.iloc[-1])
        hi52 = float(vti.max())
        d20 = (last/float(vti.iloc[-21])-1)*100 if len(vti) >= 21 else 0.0
        d60 = (last/float(vti.iloc[-61])-1)*100 if len(vti) >= 61 else 0.0
        pct_of_hi = last/hi52*100
        warn = (d20 >= 8) or (d60 >= 12) or (pct_of_hi >= 99 and d20 >= 3)
        if warn:
            return (f"⚠️ MELT-UP WATCH: VTI {d20:+.1f}% (20d) / {d60:+.1f}% (60d), at {pct_of_hi:.0f}% of "
                    f"52wk high. Cash-heavy stance is COSTING you if no recession — DECIDE: start a "
                    f"measured core DCA, or consciously reaffirm the wait. Don't drift.")
        return (f"Melt-up watch: OK — VTI {d20:+.1f}% (20d) / {d60:+.1f}% (60d), {pct_of_hi:.0f}% of 52wk "
                f"high. No sustained melt-up; holding cash as dry powder is still cheap.")
    except Exception as e:
        return f"Melt-up watch: (could not compute — {str(e)[:50]})"

def profit_exit_checks(prices, source=None):
    """Check the user's conditional exits in purchase currency; never imply a fill.

    Profit means strictly above recorded average purchase cost, before unrecorded
    fees/tax/dividends. USD equivalents use current FX, not historical tax-lot FX.
    Missing/stale prices, uncertain currencies or fallback holdings cannot trigger.
    """
    source = source if source is not None else load_portfolio_source()
    anchor = prices.get("VTI", {}).get("date", "")
    fx = prices.get("FX_CADUSD")
    rows = []
    for r in source["rows"]:
        if not _is_profit_exit(r) or r.get("shares", 0) <= 0:
            continue
        symbol = r.get("yahoo") or _sheet_yahoo(r.get("ticker", ""), r.get("name", ""))
        q = prices.get(symbol, {})
        px, cost = q.get("last"), r.get("avg_buy")
        row = {"ticker": symbol, "name": r.get("name", symbol), "shares": r["shares"],
               "account": r.get("account") or "unknown", "price": px, "average_cost": cost,
               "currency": r.get("ccy"), "quote_date": q.get("date"),
               "quote_time": q.get("quote_time"), "status": "UNKNOWN", "eligible": False,
               "pl_native": None, "pl_usd": None, "value_usd": None, "cost_usd": None,
               "rise_to_cost_pct": None, "recorded_book_usd": r.get("book_usd")}
        rows.append(row)
        if not isinstance(px, (int, float)) or not math.isfinite(px) or px <= 0 or "err" in q:
            row["status"] = "PRICE UNAVAILABLE"; continue
        if not isinstance(cost, (int, float)) or not math.isfinite(cost) or cost <= 0:
            row["status"] = "COST UNKNOWN"; continue
        if q.get("currency") not in {"USD", "CAD"} or q["currency"] != r.get("ccy"):
            row["status"] = "VERIFY COST/QUOTE CURRENCY"; continue
        gain = (px-cost)*r["shares"]
        row["pl_native"] = gain
        row["rise_to_cost_pct"] = max(0.0, (cost/px-1)*100)
        factor = 1.0 if q["currency"] == "USD" else fx
        if isinstance(factor, (int, float)) and math.isfinite(factor) and factor > 0:
            row.update(pl_usd=gain*factor, value_usd=px*r["shares"]*factor,
                       cost_usd=cost*r["shares"]*factor)
        try:
            stamp = datetime.fromisoformat(q.get("quote_time", "")).astimezone(timezone.utc)
            age_hours = (datetime.now(timezone.utc)-stamp).total_seconds()/3600
            fresh = bool(anchor and q.get("date", "") >= anchor and -1 <= age_hours <= 96)
        except (TypeError, ValueError):
            fresh = False
        if source.get("source") != "FR_Portfolio":
            row["status"] = "VERIFY STALE HOLDINGS"
        elif not fresh:
            row["status"] = "VERIFY STALE/UNDATED QUOTE"
        elif gain > 0:
            row["status"] = "PROFITABLE — SELL CANDIDATE"
            row["eligible"] = True
        elif gain == 0:
            row["status"] = "AT COST — WAIT FOR PROFIT"
        else:
            row["status"] = "BELOW COST — WAIT"
    return sorted(rows, key=lambda r: (not r["eligible"], -(r["pl_usd"] or 0), r["ticker"]))


def print_profit_exits(rows):
    if not rows:
        return
    print("=== SELL WHEN PROFITABLE — every Speculation holding; no automatic orders ===")
    print("  Strictly above average purchase cost in the recorded currency; before fees/tax.")
    print("  USD P/L is a current-FX equivalent, not historical-FX tax P/L. Confirm broker lots and bid.")
    for r in rows:
        px = f"{r['price']:.4f}" if r['price'] is not None else "n/a"
        cost = f"{r['average_cost']:.4f}" if r['average_cost'] is not None else "n/a"
        pnl = f"${r['pl_usd']:+,.2f}" if r['pl_usd'] is not None else "n/a"
        gap = f"{r['rise_to_cost_pct']:.2f}%" if r['rise_to_cost_pct'] is not None else "n/a"
        print(f"  {r['ticker']:10s} {r['shares']:g} sh | price {px} / cost {cost} {r['currency']} | "
              f"P/L USD {pnl} | to cost {gap} | {r['status']} | {r['quote_date']} [{r['account']}]")
    print()


def fmt_row(t, r):
    if "err" in r:
        return f"  {t:9s}  ERR {r['err']}"
    flag = ""
    if (r.get("d1") or 0) >= 3: flag = "  <<< UP big today"
    elif (r.get("d1") or 0) <= -3: flag = "  <<< DOWN big today"
    elif (r.get("d5") or 0) >= 6: flag = "  << up on week"
    elif (r.get("d5") or 0) <= -6: flag = "  << down on week"
    moves = "  ".join(f"{n}d={r['d'+str(n)]:+6.1f}%" if r.get('d'+str(n)) is not None
                      else f"{n}d= n/a" for n in (1, 3, 5, 20))
    return f"  {t:9s} {r['last']:>9.2f} {r.get('currency') or '?':3s}  {moves}  {r.get('date', '?')}{flag}"

def research_watch_lines(prices):
    lines = []
    for ticker, watch in RESEARCH_WATCHES.items():
        price_data = prices.get(ticker, {})
        if "err" in price_data or price_data.get("last") is None:
            lines.append(f"  {ticker:9s} ERR no data — retain watch; no allocation change")
            continue
        price = price_data["last"]
        if watch.get("review_only"):
            review = watch["review"]
            if price <= review:
                verdict = (f"REVIEW ZONE — re-underwrite before any allocation change; "
                           f"position cap {watch['max_pct']*100:.1f}%")
            else:
                verdict = f"WAIT — ${price-review:.2f} above ${review:.2f} review gate"
        elif price <= watch["second"]:
            verdict = (f"SECOND-TRANCHE ZONE — reassess fundamentals; total position remains capped at "
                       f"{watch['max_pct']*100:.1f}%")
        elif price <= watch["starter"]:
            verdict = (f"STARTER ZONE — reassess fundamentals before up to "
                       f"{watch['starter_pct']*100:.1f}%")
        else:
            verdict = f"WAIT — ${price-watch['starter']:.2f} above ${watch['starter']:.2f} starter zone"
        lines.append(f"  {ticker:9s} ${price:>9.2f}  {watch['label']}: {verdict}; {watch['note']}")
    return lines

def main():
    movers_only = "--movers" in sys.argv
    as_json = "--json" in sys.argv
    global GROUPS
    GROUPS = load_holdings_groups()
    prices = pull(GROUPS)
    mw = meltup_watch()
    source = load_portfolio_source()
    sleeve_rows, pos, total = sizing(prices)
    profit_exits = profit_exit_checks(prices, source)
    if as_json:
        print(json.dumps({"groups": GROUPS, "prices": prices, "meltup_watch": mw,
                          "research_watches": RESEARCH_WATCHES, "profit_exits": profit_exits,
                          "source": source, "sizing": sleeve_rows, "positions": pos, "total": total,
                          "retrieved_at_utc": datetime.now(timezone.utc).isoformat()}, indent=2)); return
    print("="*100)
    print("  "+mw)   # top-of-report so the cash-drag counter-check can't be missed
    print("="*100)
    print("PORTFOLIO DAILY CHECK — live prices (read-only; agent interprets vs thesis)")
    print(f"Source: {load_portfolio_source().get('source', 'unknown')}\n")
    print_profit_exits(profit_exits)
    for g, tks in GROUPS.items():
        rows = []
        for t in tks:
            r = prices.get(t, {"err": "missing"})
            if movers_only and "err" not in r and abs(r.get("d1") or 0) < 3 and abs(r.get("d5") or 0) < 5:
                continue
            rows.append(fmt_row(t, r))
        if rows:
            print(f"=== {g} ===")
            print("\n".join(rows)); print()
    watch_lines = research_watch_lines(prices)
    if watch_lines:
        print("=== RESEARCH WATCHES — no allocation target or automatic trade ===")
        print("\n".join(watch_lines)); print()
    # SIZING — $ per sleeve (trim/buy needed) + $ per position, so verdicts carry amounts.
    if sleeve_rows:
        print("=== SIZING — sleeve target vs current (ACTION $ = buy+ / trim−) ===")
        print(f"  (total portfolio ≈ ${total:,.0f}; FX CAD→USD {prices.get('FX_CADUSD',FX_CADUSD):.4f})")
        for s in sorted(sleeve_rows, key=lambda x: x["action"]):
            act = s["action"]; tag = "BUY " if act>0 else "TRIM"
            if abs(act) < 0.005*total:  # within ~0.5pp → on target
                tag = "OK  "
            print(f"  {s['sleeve']:22s} cur ${s['cur']:>8,.0f} ({s['cur_pct']*100:4.1f}%)  "
                  f"tgt ${s['tgt']:>8,.0f} ({s['tgt_pct']*100:4.1f}%)  {tag} ${abs(act):>7,.0f}")
        print("  Per-position $ (for trims, sell within the overweight sleeve):")
        # show positions in the most-overweight sleeves
        ow = [s['sleeve'] for s in sleeve_rows if s['action'] < -0.005*total]
        for tk, p in sorted(pos.items(), key=lambda x:-x[1]["mv"]):
            if p.get("sleeve") in ow and p["mv"]>0:
                print(f"    {tk:12s} ${p['mv']:>8,.0f}  ({p['sh']:g} sh @ ${p['px']:.2f} {p['ccy']})")
        print()

        exit_positions = [
            (ticker, position) for ticker, position in pos.items()
            if str(position.get("sleeve", "")).startswith("(exit)") and position["mv"] > 0
        ]
        if exit_positions:
            print("=== EXIT COST CHECK — current value vs recorded aggregate cost ===")
            print("  (nominal P/L before commissions/taxes; account tax lots may differ)")
            for ticker, position in sorted(
                exit_positions,
                key=lambda item: (item[1].get("pl", 0) < 0, -item[1]["mv"]),
            ):
                basis = position.get("basis", 0.0)
                account = position.get("account") or "account unknown"
                if basis <= 0:
                    status = "BASIS UNKNOWN — verify before sale"
                    pl_text = "n/a"
                else:
                    profit_loss = position["mv"] - basis
                    pl_text = f"+${profit_loss:,.0f}" if profit_loss >= 0 else f"-${abs(profit_loss):,.0f}"
                    status = ("ABOVE COST — can exit without nominal loss" if profit_loss >= 0
                              else "BELOW COST — sale realizes nominal loss")
                print(f"  {ticker:12s} cur ${position['mv']:>8,.0f}  basis ${basis:>8,.0f}  "
                      f"P/L {pl_text:>10s}  {status}  [{account}]")
            print()

    # quick auto-flags for the agent. Exit-queue names are SELLS regardless of direction —
    # an UP day is a chance to sell into strength; a DOWN day is NOT a buy signal.
    exit_set = set(GROUPS.get("HELD — (exit) queue (sell into any bounce)", []))
    profit_exit_set = set(GROUPS.get(PROFIT_EXIT_GROUP, []))
    held_set = set(GROUPS.get("HELD — core/sleeves (trim strength / hold)", []))
    watch_set = set(GROUPS.get("BUY WATCHLIST (underweight sleeves)", []))
    flags = []
    for t, r in prices.items():
        if t == "FX_CADUSD" or not isinstance(r, dict) or "err" in r: continue
        # Conditional exits are never converted into generic dip-buy/trim flags.
        # Their profitability status is shown every run, even on a quiet day.
        if t in profit_exit_set:
            continue
        is_exit = t in exit_set
        up = (r.get("d1") or 0) >= 3 or (r.get("d5") or 0) >= 6
        dn = (r.get("d1") or 0) <= -3 or (r.get("d5") or 0) <= -6
        if is_exit:
            if up: flags.append(f"{t} UP (1d {r['d1']:+.1f} / 5d {r['d5']:+.1f}) → EXIT-QUEUE: SELL into this bounce")
            elif dn: flags.append(f"{t} DOWN (1d {r['d1']:+.1f} / 5d {r['d5']:+.1f}) → EXIT-QUEUE: still a sell (don't chase down; harvest loss)")
        elif t in RESEARCH_WATCHES:
            if up: flags.append(f"{t} UP (1d {r['d1']:+.1f} / 5d {r['d5']:+.1f}) → RESEARCH WATCH: do not chase strength")
            if dn: flags.append(f"{t} DOWN (1d {r['d1']:+.1f} / 5d {r['d5']:+.1f}) → RESEARCH WATCH: check the dedicated price zone and revalidate fundamentals")
        elif t in watch_set and t not in held_set:
            if up: flags.append(f"{t} UP (1d {r['d1']:+.1f} / 5d {r['d5']:+.1f}) → WATCHLIST: do not chase strength")
            if dn: flags.append(f"{t} DOWN (1d {r['d1']:+.1f} / 5d {r['d5']:+.1f}) → WATCHLIST: consider only if its sleeve remains underweight")
        else:
            if up: flags.append(f"{t} UP (1d {r['d1']:+.1f} / 5d {r['d5']:+.1f}) → strength: TRIM candidate if overweight")
            if dn: flags.append(f"{t} DOWN (1d {r['d1']:+.1f} / 5d {r['d5']:+.1f}) → weakness: BUY candidate if underweight, do NOT trim")
    if flags:
        print("=== AUTO-FLAGS (agent: confirm vs over/underweight before acting) ===")
        for f in flags: print("  • " + f)

if __name__ == "__main__":
    main()
