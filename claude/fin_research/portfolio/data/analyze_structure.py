"""
Structural portfolio analysis: factor concentration + volatility + stress tests.
Reads holdings_live.json. Run: /opt/venv/bin/python3 portfolio/data/analyze_structure.py
Built 2026-07-07.
"""
import json, numpy as np, warnings
from collections import defaultdict
warnings.filterwarnings('ignore')

CASH = 280407.0
BASE = "/home/colligo/hs_scripts/claude/fin_research/portfolio"
d = json.load(open(f"{BASE}/data/holdings_live.json"))
rows = d['rows']

FACTOR_MAP = {
 'oil&gas':'ENERGY/COMMODITY','uranium':'ENERGY/COMMODITY','electrification':'ENERGY/COMMODITY',
 'gold':'PRECIOUS METALS','silver':'PRECIOUS METALS','platinum_pall':'PRECIOUS METALS',
 'copper':'INDUSTRIAL METALS','steel':'INDUSTRIAL METALS','aluminum':'INDUSTRIAL METALS',
 'food':'AG/COMMODITY','crypto':'CRYPTO','stable-coin':'CRYPTO',
 'tech':'US TECH/AI','autonomous':'US TECH/AI','ev':'EV/CLEANTECH','green':'EV/CLEANTECH',
 'china':'CHINA/EM','international':'CHINA/EM','health-bio-tk-ai':'HEALTHCARE',
 'retail':'CONSUMER','real-estate':'REAL ESTATE',
}

def factor_report():
    noncash = sum(r['mkt_val_usd'] for r in rows if r['mkt_val_usd'])
    total = CASH + noncash
    fac = defaultdict(float)
    for r in rows:
        fac[FACTOR_MAP.get(r['theme'],'OTHER')] += (r['mkt_val_usd'] or 0)
    print(f"NON-CASH ${noncash:,.0f}  TOTAL ${total:,.0f}")
    for f,v in sorted(fac.items(),key=lambda x:-x[1]):
        print(f"  {f:22s} ${v:>10,.0f}  {100*v/noncash:5.1f}% non-cash  {100*v/total:5.1f}% total")
    commod = sum(fac[k] for k in ['ENERGY/COMMODITY','PRECIOUS METALS','INDUSTRIAL METALS','AG/COMMODITY'])
    print(f"\nCOMMODITY/REAL-ASSET MEGAFACTOR: ${commod:,.0f} = {100*commod/noncash:.1f}% non-cash / {100*commod/total:.1f}% total")
    return noncash, total

def vol_report():
    import yfinance as yf
    w = defaultdict(float)
    for r in rows:
        if r['yahoo'] and r['mkt_val_usd']: w[r['yahoo']] += r['mkt_val_usd']
    noncash = sum(w.values()); total = CASH+noncash
    tickers = list(w.keys())
    data = yf.download(tickers, period='2y', interval='1wk', progress=False, auto_adjust=True)['Close']
    rets = data.pct_change().dropna(how='all')
    common = [t for t in tickers if t in rets.columns and rets[t].notna().sum()>50]
    wv = np.array([w[t] for t in common]); wv/=wv.sum()
    R = rets[common].dropna()
    pr = R.values @ wv
    v_nc = np.std(pr)*np.sqrt(52); ncs = noncash/total
    print(f"\nNon-cash vol: {v_nc*100:.1f}%  | Total (w/ cash): {v_nc*ncs*100:.1f}%")
    for s in [0.20,0.30,0.40]:
        loss=noncash*s
        print(f"  non-cash -{int(s*100)}% => total -{100*loss/total:.1f}%, remaining ${total-loss:,.0f}")

if __name__=="__main__":
    factor_report()
    try: vol_report()
    except Exception as e: print("vol skipped:", e)
