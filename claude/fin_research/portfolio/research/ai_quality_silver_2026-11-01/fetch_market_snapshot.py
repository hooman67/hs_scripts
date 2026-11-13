#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path
import yfinance as yf

symbols=['LITE','MRVL','LRCX','ANET','ARM','COHR','KLAC','MSFT','GOOGL','JQUA','SLV','SIVR','PSLV','WPM']
keys=['longName','currency','marketCap','enterpriseValue','trailingPE','forwardPE','priceToSalesTrailing12Months',
      'enterpriseToEbitda','profitMargins','grossMargins','operatingMargins','returnOnEquity','returnOnAssets',
      'revenueGrowth','earningsGrowth','totalRevenue','ebitda','operatingCashflow','freeCashflow','totalCash',
      'totalDebt','sharesOutstanding','floatShares','fiftyTwoWeekHigh','fiftyTwoWeekLow','fiftyDayAverage',
      'twoHundredDayAverage','netExpenseRatio','totalAssets','yield']
out={'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'symbols':{}}
for sym in symbols:
    t=yf.Ticker(sym)
    hist=t.history(start='2026-10-29',end='2026-11-01',auto_adjust=False)
    info=t.info
    row={k:info.get(k) for k in keys}
    if not hist.empty:
        x=hist.iloc[-1]
        row['quote_date']=str(hist.index[-1].date())
        row['close']=float(x['Close']); row['volume']=float(x['Volume'])
    try:
        fd=t.funds_data
        row['top_holdings']=[{'symbol':str(i),'name':str(v['Name']),'weight':float(v['Holding Percent'])} for i,v in fd.top_holdings.iterrows()]
        row['sector_weightings']=fd.sector_weightings
    except Exception as e:
        row['funds_data_error']=repr(e)
    out['symbols'][sym]=row
p=Path('portfolio/research/ai_quality_silver_2026-11-01/data/market_snapshot.json')
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(out,indent=2,sort_keys=True))
print(p)
for s,r in out['symbols'].items():
 print(s,r.get('close'),r.get('marketCap'),r.get('trailingPE'),r.get('forwardPE'),r.get('enterpriseToEbitda'),r.get('freeCashflow'),r.get('revenueGrowth'))
