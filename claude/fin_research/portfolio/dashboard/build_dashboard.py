"""
Build ONE consolidated dashboard tab (FR_Portfolio) in Hooman's Google Sheet.
Built 2026-07-09. NON-DESTRUCTIVE: only touches the FR_ tab; existing tabs untouched.

Single tab, sectioned like his 'Hooman Portfolio' tab:
  - Summary (total / cash / non-cash / date)
  - ALLOCATION: target vs current, drift, ACTION $ (buy+/trim-), status  [color-coded]
  - HOLDINGS: every position, live GOOGLEFINANCE price, sleeve, thesis, buy/sell triggers

ALL formulas entered with USER_ENTERED so they compute (not shown as text).
All math = sheet formulas → works without Claude. Rich conditional formatting for readability.

The checked-in holdings snapshot is historical. Rebuilding from it is blocked by default when the
live portfolio tab exists. An intentional historical rebuild requires
FR_PORTFOLIO_ALLOW_STALE_REBUILD=1.
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
from sheets_client import open_sheet

TAB = "FR_Portfolio"
OIL_COMPANIES_SLEEVE = "oil-companies"
REFINED_PRODUCTS_SLEEVE = "ref_oil_prod"
NATURAL_GAS_SLEEVE = "nat_gas"
COPPER_SLEEVE = "copper"
INDUSTRIAL_METALS_SLEEVE = "industrial_metals"
AG_SLEEVE = "Agriculture"
URANIUM_NUCLEAR_SLEEVE = "uranium/nuclear"
GRID_ELECTRIFICATION_SLEEVE = "grid/electrification"
UTILITIES_SLEEVE = "Utilities (VPU)"
TREASURY_SLEEVE = "Treasuries (VGIT)"

# ---- Target model (ideal_allocation.md, revised through 2026-09-08) ----
TARGETS = [
    ("Cash (50/50 USD/CAD)",   0.185, "SGOV + CAD GIC; DRY POWDER for the recession — do NOT deploy to equities yet"),
    ("Global equity core",     0.15,  "VTI 8.25% + VXUS 6.75%; reduced proportionally to fund VGIT"),
    (TREASURY_SLEEVE,          0.05,  "VGIT tactical recession/disinflation hedge; funded from Global equity core, not Cash"),
    ("EM/China",               0.05,  "VWO 2.5 (broad EM) + KWEB 2.0 (China tilt) + BABA 0.5 (legacy, don't add — redundant w/ KWEB). VWO=diversification, KWEB=deliberate China; cut BIDU."),
    ("Quality compounders",    0.055, "GOOGL 3 + AMZN 2.5 only (CI→Financials, LLY→Healthcare)"),
    (OIL_COMPANIES_SLEEVE,     0.06,  ""),
    (REFINED_PRODUCTS_SLEEVE,  0.02,  ""),
    (NATURAL_GAS_SLEEVE,       0.01,  ""),
    ("Gold core",              0.15,  "physical, MNT, AEM — monetary hedge and high-conviction macro sleeve"),
    (UTILITIES_SLEEVE,          0.025, "VPU broad utilities core; defensive equity, not house cash or a bond substitute"),
    ("Financials",             0.025, "CI 1.5 + BRK-B 1.0 — DEFENSIVE (Berkshire), NOT banks; contrarian to pro-cyclical bank overweight"),
    (URANIUM_NUCLEAR_SLEEVE,    0.035, "NLR 1.5 + CCJ 1.0 + CEG 0.5 + BWXT 0.5"),
    (GRID_ELECTRIFICATION_SLEEVE, 0.015, "GEV and ETN; 1.5% target formalizes the existing power-equipment thesis"),
    (COPPER_SLEEVE,            0.02,  ""),
    (INDUSTRIAL_METALS_SLEEVE, 0.01,  ""),
    (AG_SLEEVE,                0.03,  "CF, PDBA"),
    ("Healthcare",             0.05,  "XLV core 2.5 + GEHC 1.5 (AI-device) + PFE 1.0 legacy — LLY SOLD Aug-26, 2% redistributed. DEFENSIVE + demographics; AI = free option"),
    ("Defense",                0.015, "SHLD 1.5%; stage as three 0.5% tranches"),
    ("Crypto",                 0.02,  "BTC only"),
    ("Silver/Plat",            0.01,  "1% economic target; WPM is 52% silver / 46% gold and provides no meaningful platinum"),
    ("(exit) — SELL & redeploy", 0.0, "positions to liquidate; money in transit"),
    ("Speculation (cap $10k)", 0.015, "experimental sleeve; 1.5% target subject to the hard $10k cap; keep outside the core plan"),
]

# holding -> (GF symbol, sleeve, thesis, add_when, sell_when)
HOLD_MAP = {
 'VTI':('VTI','Global equity core','US core; own the market','every DCA tranche','rebalance only'),
 'VXUS':('VXUS','Global equity core','Intl core; FTC claimable in taxable','every DCA tranche','rebalance only'),
 'VGIT':('VGIT',TREASURY_SLEEVE,'Intermediate Treasury recession/disinflation hedge','stage using inflation gate','reassess after 100-150 bp yield decline or 10-15% return'),
 'XLU':('XLU',UTILITIES_SLEEVE,'Legacy utilities holding; swap to VPU','—','sell/swap to VPU'),
 'VPU':('VPU',UTILITIES_SLEEVE,'Broad regulated-heavy utilities core','stage toward 2.5%','rebalance only'),
 'GOOGL':('GOOGL','Quality compounders','Best AI winner; search+cloud+TPU','dips','share loss'),
 'Physical-Gold':('','Gold core','Monetary USD hedge (static px)','gold $3400-4000','rebalance only'),
 'TSE:MNT':('TSE:MNT','Gold core','Gold core / hedge','gold weakness','rebalance only'),
 'SGOV':('SGOV','Cash (50/50 USD/CAD)','0-3 month Treasury cash-equivalent reserve','cash-management only','fund approved purchases / house reserve'),
 'AEM':('AEM','Gold core','Best-in-class gold miner','gold $3400-4000','gold thesis break'),
 'TSE:AEM':('TSE:AEM','Gold core','Best-in-class gold miner; CAD-listed Questrade lot','gold $3400-4000','gold thesis break'),
 'EMPYF':('EMPYF','Gold core','Small gold royalty','—','review'),
 'WPM':('WPM','Silver/Plat','Streamer: Q2-26 revenue 52% silver / 46% gold','—','trim toward ~82-share ceiling; lower if adding platinum'),
 'NYSE:SBSW':('NYSE:SBSW','(exit)','SELL: broken SA plat miner','—','sell/harvest'),
 'XOM':('XOM',OIL_COMPANIES_SLEEVE,'Defensive integrated anchor','deep selloff','div risk / >5%'),
 'TSE:CNQ':('TSE:CNQ',OIL_COMPANIES_SLEEVE,'Highest-quality Cdn oil sands','oil <$60','demand peak / >5%'),
 'CNQ':('CNQ',OIL_COMPANIES_SLEEVE,'Highest-quality Cdn oil sands; U.S.-listed Ameritrade lot','oil <$60','demand peak / >5%'),
 'TSE:ARX':('TSE:ARX',OIL_COMPANIES_SLEEVE,'SHELL TAKEOVER — sell&redeploy','—','sell into deal'),
 'OXY':('OXY',OIL_COMPANIES_SLEEVE,'SWAP → EOG (quality upgrade)','—','swap'),
 'SLB':('SLB',OIL_COMPANIES_SLEEVE,'Oil services; trim if sleeve>target','—','trim'),
 'TSE:CVE':('TSE:CVE',OIL_COMPANIES_SLEEVE,'Cdn integrated; trim Cdn conc.','—','trim'),
 'TSE:TOU':('TSE:TOU',OIL_COMPANIES_SLEEVE,'Cdn gas (better-supported leg)','gas weakness','gas break'),
 'BOIL':('BOIL','(exit)','SELL: 2x leveraged decay','—','sell (never hold 2x)'),
 'UNG':('UNG',NATURAL_GAS_SLEEVE,'Small gas exposure (1x)','—','—'),
 'DBE':('DBE',REFINED_PRODUCTS_SLEEVE,'Direct energy futures including refined products','—','rebalance only'),
 'NLR':('NLR',URANIUM_NUCLEAR_SLEEVE,'Diversified nuclear/uranium core','stage to 1.5%','rebalance only'),
 'MCHI':('MCHI','EM/China','Broad China equity tax-harvest bridge after KWEB sale','—','review after wash-sale window'),
 'IEMG':('IEMG','EM/China','Broad emerging-markets tax-harvest replacement for VWO','rebalance within sleeve','review after wash-sale window'),
 'ICOP':('ICOP',COPPER_SLEEVE,'Copper-miners tax-harvest bridge after COPX sale','—','review after wash-sale window'),
 'MXI':('MXI',INDUSTRIAL_METALS_SLEEVE,'Broad materials tax-harvest bridge after PICK sale','—','review after wash-sale window'),
 'CCJ':('CCJ',URANIUM_NUCLEAR_SLEEVE,'TRIM: fwd P/E ~78x froth','—','trim ~half'),
 'BWXT':('BWXT',URANIUM_NUCLEAR_SLEEVE,'Naval/defense nuclear quality','pullbacks','defense break'),
 'CEG':('CEG',URANIUM_NUCLEAR_SLEEVE,'Cleanest AI-power value','pullbacks','PPA break'),
 'TSE:URC':('TSE:URC',URANIUM_NUCLEAR_SLEEVE,'Small uranium royalty','—','review'),
 'UROY':('UROY',URANIUM_NUCLEAR_SLEEVE,'Small uranium royalty','—','review'),
 'GEV':('GEV',GRID_ELECTRIFICATION_SLEEVE,'TRIM ⅓: +87%, ~89x EV/EBITDA','—','trim ⅓'),
 'ETN':('ETN',GRID_ELECTRIFICATION_SLEEVE,'Electrical/power mgmt; datacenter+grid buildout','pullbacks','valuation blow-off'),
 'SMR':('SMR',URANIUM_NUCLEAR_SLEEVE,'SMR pure-play (speculative, pre-revenue); small','—','review — high risk'),
 'BHP':('BHP',COPPER_SLEEVE,'½ copper (iron ore); use COPX','—','replace w/ COPX'),
 'TSE:COP.U':('TSE:COP.U',COPPER_SLEEVE,'Physical copper trust','—','—'),
 'COPX':('COPX',COPPER_SLEEVE,'Copper miners ETF (clean copper vs BHP)','build within 2% sleeve','rebalance only'),
 'NTCPF':('NTCPF',COPPER_SLEEVE,'Spec copper junior','—','review vs COPX'),
 'CVE:NCX':('CVE:NCX',COPPER_SLEEVE,'Speculative Canadian copper-gold developer','—','review vs COPX'),
 'PICK':('PICK',INDUSTRIAL_METALS_SLEEVE,'Diversified global metals and mining producers','—','rebalance only'),
 'XME':('XME','(exit)','SELL: ½ gold/coal, not steel','—','sell'),
 'AA':('AA','(exit)','SELL: redundant w/ XME','—','sell'),
 'CF':('CF',AG_SLEEVE,'Best commodity-quality; nitrogen','~10x','natgas spike / >3%'),
 'PDBA':('PDBA',AG_SLEEVE,'Broad-ag ballast','—','rebalance only'),
 'CAG':('CAG','(exit)','SELL: value-trap, keep KHC','—','sell'),
 'KHC':('KHC',AG_SLEEVE,'The one food name; breakup catalyst','—','div cut'),
 'CI':('CI','Financials','Cheap quality health-insurer (fwd P/E ~8.6, ROE 16%); DEFENSIVE financials','build to 1.5%','PBM reform / thesis break'),
 'BRK-B':('BRK-B','Financials','Berkshire — defensive quality compounder + insurance float (NOT a bank bet)','pullbacks','rebalance only'),
 'FFH.TO':('FFH.TO','Financials','Fairfax — Watsa proven-allocator (BVPS +18.7%/yr since 1985); P/E ~10, Cdn, stagflation-resilient','pullbacks','thesis/allocator break'),
 'PFE':('PFE','Healthcare','Legacy cheap pharma yield ballast; right-sized down','—','right-size to ~0.5%'),
 'GEHC':('GEHC','Healthcare','GE HealthCare — the REAL AI-device play (fwd ~11, #1 FDA AI clearances); research more','dips','—'),
 'XLV':('XLV','Healthcare','Broad healthcare core (cheap 0.08%); defensive + demographics','build to 1.5%','rebalance only'),
 'SHLD':('SHLD','Defense','Global defense primes and defense technology','stage in three 0.5% tranches','trim above 2%; sell on defense-spending thesis break'),
 'AMZN':('AMZN','Quality compounders','Best AI winner; AWS+retail','dips <$220','AWS stall / >5%'),
 'VWO':('VWO','EM/China','Broad EM (India/Taiwan/Brazil/Korea + ~28% China) — diversification','build to 2.5%','rebalance only'),
 'KWEB':('KWEB','EM/China','Deliberate China-internet tilt (basket, no single-name risk)','build to 2%','Taiwan / 5% sleeve cap'),
 'BABA':('BABA','EM/China','Legacy single name — DO NOT ADD (redundant w/ KWEB, ROE only 9%)','—','fold into KWEB / Taiwan'),
 'BIDU':('BIDU','(exit)','SELL: broken, ROE 0.3%','—','sell/harvest'),
 'JMIA':('JMIA','(exit)','SELL: micro legacy','—','cleanup'),
 'NYSE:NIO':('NYSE:NIO','(exit)','SELL: micro legacy -88%','—','cleanup'),
 'BTCUSD-1':('','Crypto','Small asymmetric hedge (static px)','rebalance to 2%','>3% trim'),
 'BTCCAD':('','Crypto','(consolidate BTC lots)','—','>3%'),
 'BTCUSD-2':('','Crypto','(consolidate BTC lots)','—','>3%'),
 'MARA':('MARA','(exit)','SELL: own BTC directly','—','sell/harvest'),
 'CRCL':('CRCL','(exit)','SELL: unprofitable -74%','—','sell/harvest'),
 'RBLX':('RBLX','(exit)','SELL: speculative','—','sell'),
 'BATS:ARKK':('ARKK','(exit)','SELL: bubble-beta','—','sell/harvest'),
 'SBUX':('SBUX','(exit)','SELL: orphan','—','sell'),
 'GLBS':('GLBS','(exit)','SELL: micro','—','cleanup'),
 'CSGP':('CSGP','(exit)','SELL: stub','—','cleanup'),
 'AEVA':('AEVA','(exit)','SELL: micro legacy','—','cleanup'),
 'AUR':('AUR','(exit)','SELL: micro legacy','—','cleanup'),
 'CHPT':('CHPT','(exit)','SELL: micro -67%','—','cleanup'),
 'F':('F','(exit)','SELL: micro','—','cleanup'),
 'LCID':('LCID','(exit)','SELL: micro','—','cleanup'),
 'RIVN':('RIVN','(exit)','SELL: micro','—','cleanup'),
 'ROOF.V':('ROOF.V','(exit)','SELL: microcap clean-tech junior, no thesis','—','cleanup'),
 'SQQQ':('SQQQ','(exit)','SELL: 3x inverse QQQ — decays, never hold (basis split-distorted)','—','sell (never hold 3x)'),
 # Speculation / experimental
 'LULU.TO':('LULU.TO','Speculation (cap $10k)','Lululemon CDR (CAD‑hedged); fun‑size only; outside core plan','pullbacks','tight stop / small size'),
}

def col(j):  # 0-indexed -> A1 letter
    return chr(65+j) if j < 26 else chr(64+j//26)+chr(65+j%26)

# Per-NAME target % of total (seed — only where we've set an explicit per-name target).
# User can edit the "Name Tgt %" column directly; those edits are PRESERVED across rebuilds and
# win over these seeds. Blank/absent = no per-name target set (leave the cell empty).
# Seeded 2026-07-26 from the 3 target-research agents (research/name_targets_*.md). Each sleeve's
# per-name targets sum to the sleeve target. Match on the holding's display NAME.
NAME_TGT_SEED = {
    # Global equity core (15%) plus Treasury recession hedge (5%)
    "Vanguard Total US (VTI)": 0.0825, "Vanguard Total Intl (VXUS)": 0.0675,
    "Vanguard Intermediate-Term Treasury ETF": 0.05,
    # Quality compounders (5.5%) — GOOGL 3 + AMZN 2.5 only (CI→Financials, LLY→Healthcare)
    "Alphabet (GOOGL)": 0.03, "Amazon": 0.025,
    # EM/China (5%) — VWO 2.5 (broad EM) / KWEB 2.0 (China tilt) / BABA 0.5 (legacy, don't add)
    "Vanguard EM (VWO)": 0.025, "KraneShares China Internet": 0.02, "Alibaba": 0.005,
    # Financials (2.5%) — CI 1.5 + BRK-B 1.0 (defensive, not banks)
    "Cigna Group (CI)": 0.015, "Berkshire Hathaway (BRK-B)": 0.01,
    # Healthcare (5%) — LLY SOLD 2026-08; freed 2% redistributed: XLV 2.5 core + GEHC 1.5 + PFE 1.0
    "Healthcare SPDR (XLV)": 0.025, "GE HealthCare (GEHC)": 0.015, "Pfizer": 0.01,
    # Energy-related sleeves: oil companies (6%) / refined products (2%) / natural gas (1%)
    "Canadian Natural Resources": 0.02, "ExxonMobil": 0.02, "Schlumberger": 0.01,
    "Tourmaline Oil": 0.01, "Invesco DB Energy Fund": 0.02, "US Natural Gas Fund": 0.01,
    # Uranium/nuclear (3.5%): accepted 2026-09-07 composition.
    "VanEck Uranium and Nuclear ETF": 0.015,
    "Cameco": 0.01, "Constellation Energy": 0.005, "BWX Technologies": 0.005,
    # Gold sleeve target is 15%; existing per-name seeds remain at 14% until the extra 1% is assigned.
    "Physical Gold (2.359oz)": 0.055, "RCM Cdn Gold Reserves ETR": 0.04,
    "Agnico Eagle Mines": 0.035, "Empress Royalty": 0.01,
    # Silver/Plat (1%)
    "Wheaton Precious Metals": 0.0192,
    # Copper (2%) / broader industrial-metals producers (1%)
    "Global X Copper Miners (COPX)": 0.0125, "Sprott Physical Copper Tr": 0.005,
    "BHP Group": 0.0025, "iShares MSCI Global Metals & Mining Producers ETF": 0.01,
    # Agriculture (3%)
    "CF Industries": 0.01, "Invesco Ag Commodity ETF": 0.02,
    # Defense (1.5%)
    "Global X Defense Tech ETF": 0.015,
}

# Sleeve -> bucket (A safety / B defensive real-asset / C growth-cyclical)
SLEEVE_BUCKET = {
    "Short TIPS (USD)":"A", TREASURY_SLEEVE:"A",
    "Gold core":"B", AG_SLEEVE:"B", UTILITIES_SLEEVE:"B",
    "Global equity core":"C","EM/China":"C","Quality compounders":"C",
    OIL_COMPANIES_SLEEVE:"C",REFINED_PRODUCTS_SLEEVE:"C",NATURAL_GAS_SLEEVE:"C",
    "Financials":"C",URANIUM_NUCLEAR_SLEEVE:"C",GRID_ELECTRIFICATION_SLEEVE:"C",
    COPPER_SLEEVE:"C",INDUSTRIAL_METALS_SLEEVE:"C",
    "Healthcare":"C","Defense":"C",
    "Crypto":"C","Silver/Plat":"C","(exit)":"C","Speculation (cap $10k)":"C",
}

# geo tag from live-holdings row (yf_country / theme), collapsed to USA/DEV/EM/GLB
def _geo_tag(r):
    if r["theme"] in ("crypto","stable-coin"): return "GLB"
    c = (r.get("yf_country") or "")
    if c == "United States": return "USA"
    if c in ("Canada","Australia","United Kingdom","Switzerland","Germany","Japan","France","Netherlands","Norway","Sweden","Ireland"): return "DEV"
    if c in ("China","India","Brazil","Mexico","Indonesia","South Africa","Taiwan"): return "EM"
    # ETFs / unknown domicile: infer from theme
    t=r["theme"]
    if t=="china": return "EM"
    if t in ("gold","silver","platinum_pall","copper","steel","aluminum","oil&gas","uranium","food"): return "GLB"
    return "USA"

# Cash by account (CAD, USD). Hooman updates THESE; total flows up. (2026-07-09)
CASH_ACCOUNTS = [
    ("QT RRSP",     92.00,   50.00),
    ("QT Cash",     25833.00, 0.00),
    ("QT Dads",     97.50,   712.52),
    ("Ameritrade",  0.00,    261338.00),
    ("TD",          0.00,    0.00),
    ("Chase",       0.00,    0.00),
    ("BMO",         0.00,    0.00),
    ("BOA",         0.00,    0.00),
]

# House-purchase cushion params
PERM_SAFETY = 100000   # never-touch floor
CRASH_TRANCHE = 45000  # deploy only on -20% dip

ACCOUNTS = ["QT RRSP","QT Cash","QT Dads","Ameritrade","TD","Chase","BMO","BOA","HSA"]

def _read_existing_cash(sh):
    """Preserve the user's cash-by-account CAD/USD entries across rebuilds (same problem the
    Account column had — CASH_ACCOUNTS defaults would otherwise overwrite live edits).
    Returns {account_name: (cad, usd)}."""
    try:
        V = sh.worksheet(TAB).get_all_values()
        hdr = None
        for i, row in enumerate(V):
            if row and row[0] == "Account" and len(row) > 2 and row[1] == "CAD" and row[2] == "USD":
                hdr = i; break
        if hdr is None:
            return {}
        out = {}
        for row in V[hdr+1:]:
            if not row or not row[0].strip() or row[0].strip() == "Total cash":
                if row and row[0].strip() == "Total cash":
                    break
                continue
            def num(x):
                try: return float(str(x).replace("$","").replace(",","").strip() or 0)
                except: return 0.0
            out[row[0].strip()] = (num(row[1]) if len(row) > 1 else 0,
                                   num(row[2]) if len(row) > 2 else 0)
        return out
    except Exception:
        return {}

def _read_existing_accounts(sh):
    """Before rebuilding, read the current FR_Portfolio 'Account' column so user-entered
    account tags survive the rebuild. Returns {holding_name: account_string}."""
    try:
        ws = sh.worksheet(TAB)
        V = ws.get_all_values()
        # find holdings header + the Account column index
        hdr = None
        for i, row in enumerate(V):
            if row and row[0] == "Name" and "Account" in row:
                hdr = i; acc_col = row.index("Account"); name_col = 0; break
        if hdr is None:
            return {}
        out = {}
        for row in V[hdr+1:]:
            if row and row[name_col].strip() and len(row) > acc_col and row[acc_col].strip():
                out[row[name_col].strip()] = row[acc_col].strip()
        return out
    except Exception:
        return {}

def _read_existing_nametgt(sh):
    """Preserve the user-editable 'Name Tgt %' column across rebuilds. Returns {holding_name: float}
    (as a fraction, e.g. 0.03). Sheet stores it as a percent-formatted value."""
    try:
        V = sh.worksheet(TAB).get_all_values()
        hdr = None
        for i, row in enumerate(V):
            if row and row[0] == "Name" and "Name Tgt %" in row:
                hdr = i; c = row.index("Name Tgt %"); break
        if hdr is None:
            return {}
        out = {}
        for row in V[hdr+1:]:
            if row and row[0].strip() and len(row) > c and str(row[c]).strip():
                raw = str(row[c]).replace("%", "").strip()
                try:
                    v = float(raw)
                    out[row[0].strip()] = v/100 if v > 1 else v  # "3%" or 3 → 0.03; 0.03 → 0.03
                except: pass
        return out
    except Exception:
        return {}

def _read_existing_alloc_user_notes(sh):
    """Preserve the user-editable 'Notes from GPT5.6 Sol' column across rebuilds.
    Returns {sleeve_name: note_text}. Tolerates older sheets where the column doesn't exist yet.
    """
    try:
        ws = sh.worksheet(TAB)
        V = ws.get_all_values()
        # locate the allocation header row: starts with 'Sleeve' and contains the notes headers
        hdr_row = None
        for i, row in enumerate(V):
            if row and row[0] == "Sleeve":
                hdr_row = i; break
        if hdr_row is None:
            return {}
        # find the user-notes column index if present
        header = V[hdr_row]
        try:
            j_col = header.index("Notes from GPT5.6 Sol")
        except ValueError:
            return {}
        out = {}
        # Read the allocation sleeves defined by TARGETS; names are in col 0 and notes in j_col.
        for r in V[hdr_row+1:hdr_row+1+len(TARGETS)]:
            if not r or not r[0].strip():
                continue
            name = r[0].strip()
            val = r[j_col] if j_col < len(r) else ""
            if val and val.strip():
                out[name] = val
        return out
    except Exception:
        return {}

def build():
    sh = open_sheet()
    existing = {ws.title: ws for ws in sh.worksheets()}
    if TAB in existing and os.environ.get("FR_PORTFOLIO_ALLOW_STALE_REBUILD") != "1":
        raise RuntimeError(
            "Refusing to overwrite live FR_Portfolio from the historical holdings_live.json "
            "snapshot. Edit the live Sheet through the reconciliation workflow, or set "
            "FR_PORTFOLIO_ALLOW_STALE_REBUILD=1 only for an intentional historical rebuild."
        )
    prior_accounts = _read_existing_accounts(sh)  # preserve user's account tags across rebuilds
    prior_cash = _read_existing_cash(sh)           # preserve cash-by-account CAD/USD across rebuilds
    prior_nametgt = _read_existing_nametgt(sh)     # preserve user's per-name target % across rebuilds
    prior_user_notes = _read_existing_alloc_user_notes(sh)  # preserve user's allocation notes (J)
    for old in ["FR_Dashboard","FR_Holdings","FR_Targets","FR_Rebalance","FR_TradeLog","FR_perm_test"]:
        if old in existing:
            sh.del_worksheet(existing[old])
    live = json.load(open(os.path.join(os.path.dirname(__file__),"..","data","holdings_live.json")))
    rows = live["rows"]
    # current total portfolio vol (from analyze_structure); update on rebuild
    VOL_TOTAL = 0.065      # 6.5% annualized (2y weekly, live 2026-07-09)
    VOL_NONCASH = 0.132

    if TAB in {ws.title for ws in sh.worksheets()}:
        ws = sh.worksheet(TAB)
        # FR_Portfolio!E1:K23 is Hooman's manually maintained TODO Notes block.
        # Clear only dashboard-owned cells so rebuilds never modify that range.
        ws.batch_clear([
            "A1:D23",
            f"L1:T{ws.row_count}",
            f"A24:K{ws.row_count}",
        ])
    else:
        ws = sh.add_worksheet(title=TAB, rows=140, cols=20)

    hlist = [r for r in rows if r["ticker"] in HOLD_MAP]
    nsl = len(TARGETS)
    nca = len(CASH_ACCOUNTS)

    # ---- dynamic row layout ----
    # 1 title,2 subtitle
    # 4 FX row (live)
    # 6.. CASH-BY-ACCOUNT section
    CASH_TITLE = 6
    CASH_HDR = 7
    CASH0 = 8
    CASH_TOT = CASH0 + nca            # total row
    # SUMMARY block
    SUM_TITLE = CASH_TOT + 2
    S_TOTAL = SUM_TITLE + 1
    S_CASH  = S_TOTAL + 1
    S_NONCASH = S_CASH + 1
    S_DATE = S_NONCASH + 1
    # VOLATILITY / HOUSE block
    VOL_TITLE = S_DATE + 2
    V_VOL = VOL_TITLE + 1
    V_1SD = V_VOL + 1
    V_C30 = V_1SD + 1
    V_CUSHION = V_C30 + 1
    # ALLOCATION
    ALLOC_TITLE = V_CUSHION + 2
    ALLOC_HDR = ALLOC_TITLE + 1
    ALLOC0 = ALLOC_HDR + 1
    ALLOC_TOT = ALLOC0 + nsl
    # DIVERSIFICATION slices (bucket / geography)
    DIV_TITLE = ALLOC_TOT + 2
    DIV_HDR = DIV_TITLE + 1
    DIV0 = DIV_HDR + 1
    # (label, tag, target % of TOTAL)
    BUCKETS = [("A — Cash+Treasuries (safety)","A",0.305),("B — Defensive real assets","B",0.16),("C — Growth/cyclical","C",0.535)]
    DIV_END = DIV0 + len(BUCKETS) - 1
    GEO_TITLE = DIV_END + 2
    GEO_HDR = GEO_TITLE + 1
    GEO0 = GEO_HDR + 1
    # (label, tag, target % of NON-CASH)
    GEOS = [("USA","USA",0.453),("Developed ex-US","DEV",0.073),("Emerging","EM",0.091),("Global/Crypto","GLB",0.384)]
    GEO_END = GEO0 + len(GEOS) - 1
    # HOLDINGS
    HOLD_TITLE = GEO_END + 2
    HOLD_HDR = HOLD_TITLE + 1
    HOLD0 = HOLD_HDR + 1
    HOLD_END = HOLD0 + len(hlist) - 1

    FXCELL = "$B$4"
    mv_range = f"$G${HOLD0}:$G${HOLD_END}"
    sl_range = f"$C${HOLD0}:$C${HOLD_END}"
    bk_range = f"$R${HOLD0}:$R${HOLD_END}"   # bucket tag per holding (col R)
    gx_range = f"$S${HOLD0}:$S${HOLD_END}"   # geo tag per holding (col S)

    total_cell = f"$B${S_TOTAL}"
    data = [["" for _ in range(20)] for _ in range(HOLD_END+2)]
    def put(r,c,v): data[r-1][c]=v

    # title + live FX
    put(1,0,"📊  PORTFOLIO DASHBOARD  —  live via GOOGLEFINANCE")
    put(2,0,"Sleeve target model · edit cash-by-account + shares; everything else auto-computes · NOT financial advice")
    put(4,0,"FX  USD/CAD  (live) →"); put(4,1,'=GOOGLEFINANCE("CURRENCY:CADUSD")')
    put(4,3,"(1 CAD = this many USD)")

    # CASH BY ACCOUNT (edit here → totals flow up)
    put(CASH_TITLE,0,"💵  CASH BY ACCOUNT   (edit these — total flows into the portfolio)")
    put(CASH_HDR,0,"Account"); put(CASH_HDR,1,"CAD"); put(CASH_HDR,2,"USD"); put(CASH_HDR,3,"USD value")
    for k,(acct,cad,usd) in enumerate(CASH_ACCOUNTS):
        r=CASH0+k
        # prefer the live cash values already in the sheet (preserved across rebuilds)
        if acct in prior_cash:
            cad, usd = prior_cash[acct]
        put(r,0,acct); put(r,1,cad); put(r,2,usd)
        put(r,3,f"=B{r}*{FXCELL}+C{r}")
    put(CASH_TOT,0,"Total cash");
    put(CASH_TOT,1,f"=SUM(B{CASH0}:B{CASH0+nca-1})")
    put(CASH_TOT,2,f"=SUM(C{CASH0}:C{CASH0+nca-1})")
    put(CASH_TOT,3,f"=SUM(D{CASH0}:D{CASH0+nca-1})")

    # SUMMARY
    put(SUM_TITLE,0,"📈  PORTFOLIO SUMMARY")
    put(S_TOTAL,0,"TOTAL PORTFOLIO $"); put(S_TOTAL,1,f'=B{S_CASH}+B{S_NONCASH}+SUMIF({sl_range},"Cash (50/50 USD/CAD)",{mv_range})')
    put(S_CASH,0,"Cash (from accounts above)"); put(S_CASH,1,f"=D{CASH_TOT}")
    put(S_NONCASH,0,"Invested holdings (ex cash equivalents)"); put(S_NONCASH,1,f'=SUM({mv_range})-SUMIF({sl_range},"Cash (50/50 USD/CAD)",{mv_range})')
    put(S_DATE,0,"Updated"); put(S_DATE,1,"=TODAY()")

    # VOLATILITY + HOUSE CUSHION
    put(VOL_TITLE,0,"🏠  RISK & HOUSE-PURCHASE CUSHION")
    put(V_VOL,0,"Est. total portfolio volatility (annual)"); put(V_VOL,1,VOL_TOTAL)
    put(V_VOL,3,"target ≤ 10% · non-cash sleeve ~"+f"{VOL_NONCASH*100:.0f}%")
    put(V_1SD,0,"≈ 1-year downside (1 std dev)"); put(V_1SD,1,f"=-B{V_VOL}*{total_cell}")
    put(V_1SD,3,"a normal-ish bad year")
    put(V_C30,0,"Stress: non-cash −30% crash"); put(V_C30,1,f"=-0.3*B{S_NONCASH}")
    put(V_C30,3,"−30% of non-cash; cash untouched")
    put(V_CUSHION,0,"House cushion after −30% crash"); put(V_CUSHION,1,f'=B{S_CASH}+SUMIF({sl_range},"Cash (50/50 USD/CAD)",{mv_range})+B{S_NONCASH}*0.7')
    put(V_CUSHION,3,"cash equivalents + 70% of invested holdings still available")

    # ALLOCATION
    put(ALLOC_TITLE,0,"🎯  ALLOCATION  —  what to BUY (+) / TRIM (−)   ·   Status auto-flags")
    # Allocation header now preserves two notes columns:
    # - I: Notes from Opus (system-generated guidance)
    # - J: Notes from GPT5.6 Sol (user/assistant collaborative notes, preserved across rebuilds)
    hdr = [
        "Sleeve",
        "Target %",
        "Target $",
        "Current $",
        "Current %",
        "Drift pp",
        "ACTION $ (buy+/trim−)",
        "Status",
        "Notes from Opus",
        "Notes from GPT5.6 Sol",
    ]
    for j,h in enumerate(hdr): put(ALLOC_HDR,j,h)
    for k,(name,pct,note) in enumerate(TARGETS):
        r = ALLOC0+k
        put(r,0,name); put(r,1,pct); put(r,2,f"=B{r}*{total_cell}")
        if name.startswith("Cash"):
            put(r,3,f'=B{S_CASH}+SUMIF({sl_range},A{r},{mv_range})')
        elif name.startswith("(exit)"):
            put(r,3,f'=SUMIF({sl_range},"(exit)",{mv_range})')
        else:
            put(r,3,f'=SUMIF({sl_range},A{r},{mv_range})')
        put(r,4,f"=D{r}/{total_cell}")
        put(r,5,f"=(E{r}-B{r})*100")
        put(r,6,f"=C{r}-D{r}")
        put(r,7,f'=IF(A{r}="(exit) — SELL & redeploy","SELL",IF(ABS(G{r})<1,"OK",IF(G{r}>0,"BUY","TRIM")))')
        # I column (index 8): system notes; J column (index 9): user/assistant notes preserved across rebuilds
        put(r,8,note)
        # Write any prior user notes captured before rebuild (see _read_existing_alloc_user_notes)
        put(r,9, prior_user_notes.get(name, ""))
    put(ALLOC_TOT,0,"TOTAL")
    put(ALLOC_TOT,1,f"=SUM(B{ALLOC0}:B{ALLOC0+nsl-1})")
    put(ALLOC_TOT,2,f"=SUM(C{ALLOC0}:C{ALLOC0+nsl-1})")
    put(ALLOC_TOT,3,f"=SUM(D{ALLOC0}:D{ALLOC0+nsl-1})")
    put(ALLOC_TOT,4,f"=SUM(E{ALLOC0}:E{ALLOC0+nsl-1})")

    # DIVERSIFICATION — by bucket
    put(DIV_TITLE,0,"🧭  DIVERSIFICATION — by Bucket (A safety / B defensive / C growth)")
    put(DIV_HDR,0,"Bucket"); put(DIV_HDR,1,"Current $"); put(DIV_HDR,2,"Current %"); put(DIV_HDR,3,"Target %")
    for k,(label,tag,tgt) in enumerate(BUCKETS):
        r=DIV0+k
        put(r,0,label)
        if tag=="A":
            put(r,1,f"=B{S_CASH}+SUMIF({sl_range},\"Cash (50/50 USD/CAD)\",{mv_range})+SUMIF({sl_range},\"Short TIPS (USD)\",{mv_range})+SUMIF({sl_range},\"{TREASURY_SLEEVE}\",{mv_range})")
        else:
            put(r,1,f'=SUMIF({bk_range},"{tag}",{mv_range})')
        put(r,2,f"=B{r}/{total_cell}")
        put(r,3,tgt)

    # DIVERSIFICATION — by geography
    put(GEO_TITLE,0,"🌍  DIVERSIFICATION — by Geography")
    put(GEO_HDR,0,"Region"); put(GEO_HDR,1,"Current $"); put(GEO_HDR,2,"Current %"); put(GEO_HDR,3,"Target %")
    for k,(label,tag,tgt) in enumerate(GEOS):
        r=GEO0+k
        put(r,0,label)
        put(r,1,f'=SUMIF({gx_range},"{tag}",{mv_range})')
        put(r,2,f"=B{r}/B{S_NONCASH}")
        put(r,3,tgt)
    put(GEO_END+1,0,"(cash excluded from geography; % of non-cash)")

    # HOLDINGS. Cols: A Name B GFsym C Sleeve D Shares E Price F Ccy G MktVal
    #   H Book$ I P/L$ J P/L% K Thesis L ADDwhen M SELLwhen N Account (+ O Status? no)
    # Cols: A Name B GFsym C Sleeve D Shares E Price F Ccy G MktVal H AvgBuy I Book J P/L$ K P/L%
    #   L Thesis M ADDwhen N SELLwhen O Account P Bucket Q Geo. Account may hold a LIST (comma-sep,
    #   e.g. "QT RRSP, Ameritrade"); Bucket/Geo tags moved to P/Q (feed the SUMIFs).
    # Cols: A Name B GFsym C Sleeve D Shares E Price F Ccy G MktVal H %Port I AvgBuy J Book
    #   K P/L$ L P/L% M Thesis N ADDwhen O SELLwhen P Account Q Bucket R Geo. Account may be a LIST.
    # Cols: A Name B GFsym C Sleeve D Shares E Price F Ccy G MktVal H %Port I NameTgt%
    #   J AvgBuy K Book L P/L$ M P/L% N Thesis O ADDwhen P SELLwhen Q Account R Bucket S Geo.
    #   Price fallback stored in col T (19). Name Tgt % = editable per-NAME target (blank = none set).
    put(HOLD_TITLE,0,"📁  HOLDINGS  —  live prices + P/L; Name Tgt % = per-name target you can edit (blank = none)")
    hh = ["Name","GF Symbol","Sleeve","Shares","Live Price","Ccy","Mkt Val USD","% Port","Name Tgt %",
          "Avg Buy","Book USD","P/L $","P/L %","Thesis","ADD when","SELL when","Account","Bucket","Geo"]
    for j,h in enumerate(hh): put(HOLD_HDR,j,h)
    for k,r in enumerate(hlist):
        ri = HOLD0+k
        tk=r["ticker"]; gf,sleeve,thesis,add,sell = HOLD_MAP[tk]
        shares=r["shares"]; ccy=r["ccy"]; name=r["name"]; avg=r["avg_buy"]
        if tk.startswith("BTC") or tk=="Physical-Gold" or tk=="ROOF.V":
            gfsym=""
        else:
            gfsym=gf
        put(ri,0,name); put(ri,1,gfsym); put(ri,2,sleeve); put(ri,3,shares)
        # E Live Price. GOOGLEFINANCE throttles on bulk refresh → falls back to stored last-price (col T).
        lastpx = r.get("live_price") or r.get("avg_buy") or 0
        if gfsym:
            put(ri,4,f'=IFERROR(GOOGLEFINANCE(B{ri},"price"),T{ri})')  # live, fallback to stored T
            put(ri,5,ccy if not tk.startswith("BTC") else "USD")
            put(ri,19,lastpx)   # T = stored last-price fallback (col 19)
        else:
            px = r["live_price"]
            if px is None:
                px = 4132.0 if tk=="Physical-Gold" else r["avg_buy"]
            put(ri,4,px); put(ri,5,ccy)
        # G Mkt Val USD (IFERROR-guarded; CAD equities converted). BTC is quoted in
        # USD even when a lot's recorded acquisition cost is CAD, so its market value
        # stays in USD while its CAD cost basis must still be translated in column K.
        if ccy=="CAD" and not tk.startswith("BTC"):
            put(ri,6,f"=IFERROR(D{ri}*E{ri}*{FXCELL},0)")
        else:
            put(ri,6,f"=IFERROR(D{ri}*E{ri},0)")
        if ccy=="CAD":
            put(ri,10,f"=D{ri}*J{ri}*{FXCELL}")  # K Book USD = shares*avgbuy*FX
        else:
            put(ri,10,f"=D{ri}*J{ri}")           # K Book USD
        put(ri,7,f"=IFERROR(G{ri}/{total_cell},0)")   # H % Port
        # I = per-NAME target % (preserved edit wins; else seed; else blank)
        ntgt = prior_nametgt.get(name, NAME_TGT_SEED.get(name))
        put(ri,8, ntgt if ntgt is not None else "")    # I Name Tgt %
        put(ri,9,avg)                                  # J Avg Buy (native ccy)
        put(ri,11,f"=G{ri}-K{ri}")                     # L P/L $ = MktVal(G) − Book(K)
        put(ri,12,f'=IF(K{ri}=0,"",L{ri}/K{ri})')      # M P/L %
        put(ri,13,thesis); put(ri,14,add); put(ri,15,sell)
        put(ri,16,prior_accounts.get(name,""))         # Q Account (preserved across rebuilds)
        put(ri,17,SLEEVE_BUCKET.get(sleeve,"C"))       # R bucket tag (feeds bucket SUMIF)
        put(ri,18,_geo_tag(r))                          # S geo tag (feeds geo SUMIF)

    # Write around the protected TODO Notes block rather than restoring it after a
    # destructive full-sheet update. This keeps E1:K23 untouched by the API.
    protected_rows = min(23, len(data))
    ws.update(values=[row[:4] for row in data[:protected_rows]],
              range_name=f"A1:D{protected_rows}", value_input_option="USER_ENTERED")
    ws.update(values=[row[11:] for row in data[:protected_rows]],
              range_name=f"L1:T{protected_rows}", value_input_option="USER_ENTERED")
    if len(data) > protected_rows:
        ws.update(values=data[protected_rows:],
                  range_name=f"A{protected_rows + 1}:T{len(data)}",
                  value_input_option="USER_ENTERED")
    _format(sh, ws, {
        "CASH_TITLE":CASH_TITLE,"CASH_HDR":CASH_HDR,"CASH0":CASH0,"CASH_TOT":CASH_TOT,
        "SUM_TITLE":SUM_TITLE,"S_TOTAL":S_TOTAL,"S_DATE":S_DATE,
        "VOL_TITLE":VOL_TITLE,"V_VOL":V_VOL,"V_CUSHION":V_CUSHION,
        "ALLOC_TITLE":ALLOC_TITLE,"ALLOC_HDR":ALLOC_HDR,"ALLOC0":ALLOC0,"ALLOC_TOT":ALLOC_TOT,
        "DIV_TITLE":DIV_TITLE,"DIV_HDR":DIV_HDR,"DIV0":DIV0,"DIV_END":DIV_END,
        "GEO_TITLE":GEO_TITLE,"GEO_HDR":GEO_HDR,"GEO0":GEO0,"GEO_END":GEO_END,
        "HOLD_TITLE":HOLD_TITLE,"HOLD_HDR":HOLD_HDR,"HOLD0":HOLD0,"HOLD_END":HOLD_END,
        "FXROW":4,
    })
    print(f"✅ Built single tab '{TAB}' — {len(hlist)} holdings, {nsl} sleeves, cash-by-account, "
          f"diversification slices, vol/house block. 0 split tabs.")

def _format(sh, ws, L):
    sid = ws.id
    reqs = []
    W=14
    def bg(r0,r1,c0,c1,color):
        reqs.append({"repeatCell":{"range":{"sheetId":sid,"startRowIndex":r0-1,"endRowIndex":r1,"startColumnIndex":c0,"endColumnIndex":c1},
            "cell":{"userEnteredFormat":{"backgroundColor":color}},"fields":"userEnteredFormat.backgroundColor"}})
    def txt(r0,r1,c0,c1,white=False,bold=False,size=None):
        tf={}
        if bold: tf["bold"]=True
        if size: tf["fontSize"]=size
        if white: tf["foregroundColor"]={"red":1,"green":1,"blue":1}
        reqs.append({"repeatCell":{"range":{"sheetId":sid,"startRowIndex":r0-1,"endRowIndex":r1,"startColumnIndex":c0,"endColumnIndex":c1},
            "cell":{"userEnteredFormat":{"textFormat":tf}},"fields":"userEnteredFormat.textFormat"}})
    def numfmt(r0,r1,c0,c1,pattern,typ="NUMBER"):
        reqs.append({"repeatCell":{"range":{"sheetId":sid,"startRowIndex":r0-1,"endRowIndex":r1,"startColumnIndex":c0,"endColumnIndex":c1},
            "cell":{"userEnteredFormat":{"numberFormat":{"type":typ,"pattern":pattern}}},"fields":"userEnteredFormat.numberFormat"}})
    def cond_text(r0,r1,c0,c1,text,color):
        reqs.append({"addConditionalFormatRule":{"rule":{"ranges":[{"sheetId":sid,"startRowIndex":r0-1,"endRowIndex":r1,"startColumnIndex":c0,"endColumnIndex":c1}],
            "booleanRule":{"condition":{"type":"TEXT_EQ","values":[{"userEnteredValue":text}]},"format":{"backgroundColor":color}}},"index":0}})
    def cond_grad(r0,r1,c0,c1):
        reqs.append({"addConditionalFormatRule":{"rule":{"ranges":[{"sheetId":sid,"startRowIndex":r0-1,"endRowIndex":r1,"startColumnIndex":c0,"endColumnIndex":c1}],
            "gradientRule":{"minpoint":{"color":{"red":0.93,"green":0.6,"blue":0.6},"type":"MIN"},
            "midpoint":{"color":{"red":1,"green":1,"blue":1},"type":"NUMBER","value":"0"},
            "maxpoint":{"color":{"red":0.6,"green":0.85,"blue":0.6},"type":"MAX"}}},"index":0}})
    def databar(r0,r1,c0,c1):  # % bar via gradient white->blue
        reqs.append({"addConditionalFormatRule":{"rule":{"ranges":[{"sheetId":sid,"startRowIndex":r0-1,"endRowIndex":r1,"startColumnIndex":c0,"endColumnIndex":c1}],
            "gradientRule":{"minpoint":{"color":{"red":1,"green":1,"blue":1},"type":"NUMBER","value":"0"},
            "maxpoint":{"color":{"red":0.4,"green":0.6,"blue":0.9},"type":"MAX"}}},"index":0}})

    DKBLUE={"red":0.17,"green":0.24,"blue":0.42}; LTBLUE={"red":0.82,"green":0.87,"blue":0.95}
    HDR={"red":0.27,"green":0.35,"blue":0.55}; SUMBG={"red":0.93,"green":0.95,"blue":0.86}
    CASHBG={"red":0.90,"green":0.94,"blue":0.90}; RISKBG={"red":0.97,"green":0.93,"blue":0.86}
    green={"red":0.72,"green":0.88,"blue":0.72}; red={"red":0.96,"green":0.78,"blue":0.78}
    yellow={"red":1,"green":0.9,"blue":0.6}

    def section(row):  # dark header bar; protect the manual E1:K23 notes block
        end_col = 4 if row <= 23 else W
        bg(row,row,0,end_col,HDR); txt(row,row,0,end_col,white=True,bold=True)
    def subhdr(r0,c1):  # light-blue header row
        bg(r0,r0,0,c1,LTBLUE); txt(r0,r0,0,c1,bold=True)

    # title
    bg(1,1,0,4,DKBLUE); txt(1,1,0,4,white=True,bold=True,size=14)
    bg(2,2,0,4,LTBLUE)
    # FX row
    txt(L["FXROW"],L["FXROW"],0,1,bold=True)
    numfmt(L["FXROW"],L["FXROW"],1,2,"0.00000","NUMBER")

    # CASH BY ACCOUNT
    section(L["CASH_TITLE"]); subhdr(L["CASH_HDR"],4)
    bg(L["CASH0"],L["CASH_TOT"],0,4,CASHBG)
    numfmt(L["CASH0"],L["CASH_TOT"]+1,1,4,'"$"#,##0',"NUMBER")
    bg(L["CASH_TOT"],L["CASH_TOT"],0,4,SUMBG); txt(L["CASH_TOT"],L["CASH_TOT"],0,4,bold=True)

    # SUMMARY
    section(L["SUM_TITLE"])
    bg(L["S_TOTAL"],L["S_DATE"],0,2,SUMBG); txt(L["S_TOTAL"],L["S_DATE"],0,1,bold=True)
    numfmt(L["S_TOTAL"],L["S_DATE"]-1+1,1,2,'"$"#,##0',"NUMBER")
    numfmt(L["S_DATE"],L["S_DATE"],1,2,'yyyy-mm-dd',"DATE")
    txt(L["S_TOTAL"],L["S_TOTAL"],0,2,bold=True,size=12)

    # VOLATILITY / HOUSE
    section(L["VOL_TITLE"])
    bg(L["V_VOL"],L["V_CUSHION"],0,4,RISKBG); txt(L["V_VOL"],L["V_CUSHION"],0,1,bold=True)
    numfmt(L["V_VOL"],L["V_VOL"],1,2,"0.0%","PERCENT")
    numfmt(L["V_VOL"]+1,L["V_CUSHION"],1,2,'"$"#,##0;[Red]("$"#,##0)',"NUMBER")

    # ALLOCATION
    section(L["ALLOC_TITLE"]); subhdr(L["ALLOC_HDR"],10)
    a0,at=L["ALLOC0"],L["ALLOC_TOT"]
    numfmt(a0,at,1,2,"0.0%","PERCENT"); numfmt(a0,at,4,5,"0.0%","PERCENT")
    numfmt(a0,at,2,4,'"$"#,##0',"NUMBER"); numfmt(a0,at,5,6,"+0.0;-0.0","NUMBER")
    numfmt(a0,at,6,7,'"$"#,##0;[Red]("$"#,##0)',"NUMBER")
    bg(at,at,0,10,SUMBG); txt(at,at,0,10,bold=True)
    cond_text(a0,at,7,8,"OK",green); cond_text(a0,at,7,8,"BUY",yellow)
    cond_text(a0,at,7,8,"TRIM",red); cond_text(a0,at,7,8,"SELL",red)
    cond_grad(a0,at,6,7); cond_grad(a0,at,5,6)

    # DIVERSIFICATION bucket + geo (now with Target % in col D)
    section(L["DIV_TITLE"]); subhdr(L["DIV_HDR"],4)
    numfmt(L["DIV0"],L["DIV_END"]+1,1,2,'"$"#,##0',"NUMBER"); numfmt(L["DIV0"],L["DIV_END"]+1,2,4,"0.0%","PERCENT")
    databar(L["DIV0"],L["DIV_END"]+1,2,3)
    section(L["GEO_TITLE"]); subhdr(L["GEO_HDR"],4)
    numfmt(L["GEO0"],L["GEO_END"]+1,1,2,'"$"#,##0',"NUMBER"); numfmt(L["GEO0"],L["GEO_END"]+1,2,4,"0.0%","PERCENT")
    databar(L["GEO0"],L["GEO_END"]+1,2,3)

    # HOLDINGS — cols: E Price G MktVal H %Port I NameTgt% J AvgBuy K Book L P/L$ M P/L%; Q Account (idx16)
    section(L["HOLD_TITLE"]); subhdr(L["HOLD_HDR"],19)
    h0,he=L["HOLD0"],L["HOLD_END"]
    numfmt(h0,he+1,4,5,'"$"#,##0.00',"NUMBER")          # E price
    numfmt(h0,he+1,6,7,'"$"#,##0',"NUMBER")             # G mktval
    numfmt(h0,he+1,7,9,"0.0%","PERCENT")                # H %Port, I Name Tgt %
    numfmt(h0,he+1,9,11,'"$"#,##0.00',"NUMBER")         # J avgbuy, K book
    numfmt(h0,he+1,11,12,'"$"#,##0;[Red]("$"#,##0)',"NUMBER")  # L P/L $
    numfmt(h0,he+1,12,13,"+0.0%;[Red]-0.0%","PERCENT")  # M P/L %
    cond_grad(h0,he+1,11,12)                             # P/L $ green/red gradient
    cond_grad(h0,he+1,12,13)                             # P/L % green/red gradient

    # Account dropdown (col Q = index 16). NOT strict, so a LIST like "QT RRSP, Ameritrade" is allowed.
    reqs.append({"setDataValidation":{"range":{"sheetId":sid,"startRowIndex":h0-1,"endRowIndex":he,
        "startColumnIndex":16,"endColumnIndex":17},
        "rule":{"condition":{"type":"ONE_OF_LIST","values":[{"userEnteredValue":a} for a in ACCOUNTS]},
        "showCustomUi":True,"strict":False}}})  # strict=False → allows comma-separated multi-account entries

    # freeze first 2 rows
    # Freeze col A (Name) only — stays visible scrolling right. No frozen rows (Hooman's pref, simple).
    reqs.append({"updateSheetProperties":{"properties":{"sheetId":sid,"gridProperties":{"frozenColumnCount":1,"frozenRowCount":0}},"fields":"gridProperties.frozenColumnCount,gridProperties.frozenRowCount"}})
    # column widths (A names, B GF symbol, N thesis, Q account)
    for ci,px in [(0,210),(1,110),(13,240),(16,150)]:
        reqs.append({"updateDimensionProperties":{"range":{"sheetId":sid,"dimension":"COLUMNS","startIndex":ci,"endIndex":ci+1},"properties":{"pixelSize":px},"fields":"pixelSize"}})
    sh.batch_update({"requests":reqs})

if __name__ == "__main__":
    build()
