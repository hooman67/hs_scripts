"""Read-only dated valuation; raw inputs retained, no portfolio edits."""
import json,datetime,concurrent.futures,collections,math
from pathlib import Path
import yfinance as yf
P=Path(__file__).resolve().parent
source=json.loads((P/'source.json').read_text());sheet=json.loads((P/'sheet.json').read_text())
symbols=sorted({r['yahoo'] for r in source['rows'] if r.get('yahoo') and r['yahoo']!='TSE:URC'}|{'CADUSD=X'})
def fetch(t):
 try:
  obj=yf.Ticker(t);h=obj.history(period='5d',auto_adjust=False);meta=obj.get_history_metadata();ts=meta.get('regularMarketTime');px=meta.get('regularMarketPrice')
  if ts and px and math.isfinite(float(px)):
   date=datetime.datetime.fromtimestamp(ts,datetime.timezone.utc).isoformat() if isinstance(ts,(int,float)) else str(ts)
   return t,dict(price=float(px),timestamp=date,currency=meta.get('currency'),source='Yahoo quote metadata')
  h=h['Close'].dropna()
  if len(h):return t,dict(price=float(h.iloc[-1]),timestamp=str(h.index[-1]),currency=meta.get('currency'),source='Yahoo dated daily close')
  return t,dict(error='no finite quote')
 except Exception as e:return t,dict(error=str(e)[:180])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:quotes=dict(pool.map(fetch,symbols))
(P/'quotes.json').write_text(json.dumps(quotes,indent=2))
fx=quotes.get('CADUSD=X',{}).get('price') or float(sheet[3][1]);rows=[];sleeves=collections.defaultdict(float)
for r in source['rows']:
 q=quotes.get(r.get('yahoo'),{});px=q.get('price') or r['live_price'] or r['avg_buy'];ccy=q.get('currency') or ('USD' if r.get('yahoo')=='BTC-USD' else r['ccy'])
 if ccy not in ['CAD','USD']:raise ValueError((r['ticker'],ccy))
 mv=px*r['shares']*(fx if ccy=='CAD' else 1)
 v=dict(r,mv=mv,px=px,quote_ccy=ccy,price_date=q.get('timestamp','UNKNOWN'),price_source=q.get('source','Stored sheet mark; NOT fresh'))
 rows.append(v);sleeves[r['sleeve']]+=mv
cash_rows=[]
for r in sheet[7:15]:
 cash_rows.append(dict(account=r[0],cad=float(r[1] or 0),usd=float(r[2] or 0)))
cash=sum(r['usd']+r['cad']*fx for r in cash_rows);total=sum(sleeves.values())+cash;sleeves['Cash (50/50 USD/CAD)']=cash
start=next(i for i,r in enumerate(sheet) if r and r[0]=='Sleeve' and r[1]=='Target %')+1;targets={}
for r in sheet[start:]:
 if r[0]=='TOTAL':break
 name='(exit)' if r[0].startswith('(exit)') else r[0];targets[name]=float(r[1])
assert abs(sum(targets.values())-1)<1e-9
assert set(sleeves)<=set(targets),(set(sleeves)-set(targets))
result=dict(retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=source['source'],fx_cadusd=fx,total=total,cash=cash,cash_rows=cash_rows,rows=rows,targets=targets,sizing=[dict(sleeve=k,current=sleeves.get(k,0),current_pct=sleeves.get(k,0)/total,target_pct=v,target=total*v) for k,v in targets.items()])
(P/'snapshot.json').write_text(json.dumps(result,indent=2));print('Total',round(total,2),'Cash',round(cash,2),'FX',fx,'Rows',len(rows))
print('Stored marks',[(r['ticker'],round(r['mv'])) for r in rows if r['price_date']=='UNKNOWN'])
for r in result['sizing']:print(r['sleeve'],round(r['current']),round(r['current_pct']*100,2),r['target_pct']*100)
prev=json.load(open('/home/colligo/hs_scripts/claude/fin_research/portfolio/research/daily_monitoring/data/2026-10-13.json'))['source']['rows'];old={r['ticker']:r for r in prev}
print('CHANGES',[(r['ticker'],old.get(r['ticker'],{}).get('shares'),r['shares']) for r in source['rows'] if old.get(r['ticker'],{}).get('shares')!=r['shares']])
