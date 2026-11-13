from pathlib import Path
from collections import Counter,defaultdict
import csv,json
ROOT=Path('/home/colligo/hs_scripts/claude/fin_research');D=ROOT/'portfolio/research/macro_monitoring/data/2026-10-14';OUT=D/'transactions';REPORT=ROOT/'portfolio/research/macro_monitoring/reports/2026-10-14_transactions.md'
PR=ROOT/'portfolio/research/macro_monitoring/reports/2026-10-01_macro_check.md';DEC=ROOT/'portfolio/DECISIONS.md';CP=ROOT/'AUDIT_CHECKPOINT.md';STATE=ROOT/'portfolio/PROJECT_STATE.md';SHEET=D/'sheet.json';SNAP=D/'snapshot.json'
s=json.loads(SNAP.read_text());live=s['rows'];sizing={r['sleeve']:r for r in s['sizing']};events=[]
def add(date,ticker,side,qty,price,ccy='USD',account='',support='PRIOR_REPORT_ONLY',sources='',notes='',sleeve='',rationale=''):
 events.append(dict(id=f'T{len(events)+1:03}',date=date,time_et='',ticker=ticker,side=side,quantity=qty,quantity_unit='shares',fill_price=price,currency=ccy,gross_notional=round(qty*price,4) if qty is not None and price is not None else None,fees=None,account=account,sleeve=sleeve,rationale=rationale,rule_at_time='',funding_or_redeployment='',evidence=support,sources=str(PR)+':239-252'+('; '+sources if sources else ''),limits=notes))
# One trade event per instrument/date; ARX has two explicitly recorded fills.
for x in [('ARX.TO','SELL',572,(340*30.90+232*30.89)/572,'CAD'),('OXY','SELL',123,52.46,'USD'),('WPM.TO','SELL',35,156.70,'CAD'),('VTI','BUY',7,371.49,'USD'),('VXUS','BUY',19,84.97,'USD'),('XLU','BUY',23,45.11,'USD'),('GOOGL','BUY',3,356.32,'USD')]:
 add('2026-07-10',*x,account='Ameritrade' if x[0]=='OXY' else 'QT Cash',support='LOCAL_FILL',sources=str(DEC)+':65-85',notes='ARX weighted fill price from 340 @30.90 and 232 @30.89; one aggregated trade event.' if x[0]=='ARX.TO' else '')
add('2026-07-14','CVE.TO','SELL',203,38.78,'CAD','QT RRSP')
add('2026-07-14','GLBS','SELL',21,2.74,'USD','QT RRSP')
add('2026-07-23','XOM','SELL',60,157.31,'USD','QT Dads')
add('2026-08-25','LLY','SELL',9,1235.56,'USD','QT RRSP','LOCAL_NARRATIVE_PARTIAL',str(ROOT/'portfolio/research/healthcare_ai_sleeve_2026-09-07.md')+':63,78; '+str(CP)+':1744','Date/account/price corroborated by healthcare research; quantity9 remains prior-report-only. Conflicts with old approximate$1250/date unspecified.')
add('2026-08','PHYSICAL_GOLD','BUY',2.641,4543.36,'USD','','INFERRED_PRIOR_REPORT','','Quantity inferred by prior report from2.359 to5oz; execution date,platform and actual invoice not recovered.');events[-1]['quantity_unit']='troy_ounces'
add('2026-08-31','KWEB','BUY',385,26.01)
add('2026-08-31','FFH.TO','BUY',4,2253,'CAD')
add('2026-09-02','UNG','BUY',925,10.5997,notes='Prior report says909 to1834 shares; current1834 corroborates ending position,not date/fill.')
add('2026-09-04','LULU.TO','BUY',1000,4.39,'CAD')
add('2026-09-04','PDBA','ADJUSTMENT',None,38.65,notes='Ending155 shares; delta and direction unknown. Not counted as trade or in cash totals.')
sells=[('F',30,14.21),('SMR',185,11.1401),('WPM.TO',38,214.02),('PFE',271,27.972),('XME',25,121.08),('XLU',58,43.5525),('GOOGL',18,338.66)]
buys=[('TTD',220,14.06),('NKE',80,38.23),('SHLD',50,62.81),('VPU',45,188.4899),('CI',8,276.72),('BRK.B',7,504.49),('VWO',100,61.255),('JQUA',90,73.8592)]
for side,rows in [('SELL',sells),('BUY',buys)]:
 for ticker,qty,price in rows:
  add('2026-09-08',ticker,side,qty,price,'CAD' if ticker=='WPM.TO' else 'USD',support='LOCAL_EVENT_PRICE_PARTIAL',sources=str(CP)+':1931-1939',notes='Checkpoint corroborates date,side,quantity; execution price and exact account from prior report unless current sheet cost also matches. No broker confirmation available.')
for ticker,qty,price,acc in [('COPX',34,88.86,'Ameritrade'),('PICK',47,63.31,'Ameritrade'),('NLR',15,118.8408,'QT Cash')]:add('2026-09-10',ticker,'BUY',qty,price,account=acc,support='LOCAL_FILL',sources=str(CP)+':1946-1963')
add('2026-09-11','CLX','BUY',23,87.985,account='Ameritrade')
add('2026-09-11','UBER','BUY',14,71.7697,account='QT RRSP')
add('2026-09-15','CCO.TO','BUY',25,126.76,'CAD','QT RRSP')
add('2026-09-16','PFE','SELL',501,27.3938,account='Ameritrade',support='LIVE_EXIT_QUANTITY_PRICE_PARTIAL',sources=str(SHEET)+':row95',notes='Live note confirms dated full exit;501 quantity,price and$0.38fee from prior report only. Checkpoint afterSept8 says467remaining:34share mismatch.');events[-1]['fees']=.38
for ticker,qty,price,row in [('AUR',100,6.3501,73),('JMIA',30,6.9015,96)]:add('2026-09-18',ticker,'SELL',qty,price,account='QT RRSP',support='LIVE_FILL_NOTE',sources=str(SHEET)+f':row{row}')
add('2026-09-18','KHC','SELL',212.2349,24.6127,account='Ameritrade',support='LOCAL_FILL',sources=str(CP)+':1964-1972; '+str(SHEET)+':row88',notes='Actual brokerquantity recorded supersedes stale208.7079sheet;3.527share discrepancy is correction,not separate trade.')
for ticker,qty,price,ccy,acc in [('CF',16,129.1212,'USD',''),('VTI',8,374.70,'USD',''),('VHT',10,315.71,'USD',''),('IHI',58,51.885,'USD','Ameritrade'),('SHOP.TO',20,178.07,'CAD','QT RRSP')]:add('2026-09-18',ticker,'BUY',qty,price,ccy,acc,support='LOCAL_FILL' if ticker=='IHI' else 'PRIOR_REPORT_ONLY',sources=str(CP)+':1964-1972' if ticker=='IHI' else '')
for ticker,qty,price in [('VWO',44,60.035),('COPX',29,86.495),('PICK',33,61.105),('VXUS',35,85.8699),('VPU',25,173.02)]:add('2026-09-23',ticker,'BUY',qty,price,account='Ameritrade' if ticker!='VPU' else '',notes='Account described only as primarily Ameritrade in old report; exact assignment not independently verified.')
for date,ticker,side,qty,price,line in [('2026-10-02','BHP','SELL',50,85.625,315),('2026-10-02','FIS','BUY',138,32.435,322),('2026-10-06','TRMLF','BUY',22,43.926,338),('2026-10-06','LNG','BUY',4,275.7359,338),('2026-10-06','BKR','BUY',18,57.23,338),('2026-10-06','VGIT','BUY',53,56.6181,351),('2026-10-06','SGOV','SELL',30,100.455,353),('2026-10-14','ASTS','BUY',70,42.355,376)]:
 add(date,ticker,side,qty,price,account='Ameritrade',support='LOCAL_FILL',sources=str(DEC)+f':{line}'+('; '+str(STATE)+':64-74' if date=='2026-10-06' else ''))
 events[-1]['sources']=events[-1]['sources'].replace(str(PR)+':239-252; ','')
 if ticker=='ASTS':events[-1]['time_et']='14:52'
# Current position mapping; holding matches corroborate existence, not fill dates.
alias={'SHOP.TO':'TSE:SHOP','FFH.TO':'TSE:FFH','CCO.TO':'TSE:CCO','WPM.TO':'WPM','BRK.B':'NYSE:BRK.B','PHYSICAL_GOLD':'Physical Gold'}
by={r['ticker']:r for r in live};spec={'LULU.TO','TTD','NKE','CLX','SHOP.TO','UBER','FIS','ASTS'}
for e in events:
 t=e['ticker'];r=by.get(alias.get(t,t),by.get(t))
 if r:
  if not e['account']:e['account']=r['account']+' [current account; historical assignment uncertain]' if r['account'] else 'unrecorded'
  e['sleeve']=r['sleeve'];e['current_shares']=r['shares'];e['current_price']=r['px'];e['current_market_value']=r['mv']
  e['current_position_support']='Current balance only; no proof of historical date or specific fill'
  if e['quantity']==r['shares'] and e['fill_price'] is not None and abs(e['fill_price']-r['avg_buy'])<.001:
   e['current_position_support']='Current shares and average cost match claimed trade; date still needs fill record'
 else:e.update(current_shares=None,current_price=None,current_market_value=None,current_position_support='No active snapshot row; absence alone does not prove historical fill')
 if t in spec:
  e['sleeve']='Speculation';e['rationale']='Speculative/turnaround satellite; FIS explicitly user-directed without completed research' if t=='FIS' else 'Discretionary satellite; detailed original motive not inferred'
  e['rule_at_time']='Sep8 onward:1.5% target plus$10k hardcap (DECISIONS); Sept7 NKE0.25%starter,0.5%namecap; earlierdates must use then-policy'
 elif t in ['VTI','VXUS']:e['rationale']='Build diversified global-equity core';e['rule_at_time']='July gradualDCA; July26 deployment pause; Oct6 core target15%. Do not retroactively treat later policy as earlier rule.'
 elif t in ['COPX','PICK','NLR','VPU','JQUA','VHT','IHI','VWO','SHLD']:e['rationale']='Implement diversified fund sleeve / replace concentrated legacy exposures';e['rule_at_time']='Use accepted sleeve-specific size and staging policy; incomplete contemporaneous account/total data limits exact historical cap test'
 elif t=='UNG':e['rationale']='Natural-gas/LNG thesis';e['rule_at_time']='Current1%target; Sept2then-policy not independently recovered; do not infer formal breach solely from later policy'
 elif t in ['BKR','LNG','TRMLF']:e['rationale']='Oct4 selected North-American energy-export basket';e['rule_at_time']='AggregateTRMLF+TOU; reviewBKR+SLB; no unlimitedenergyweight';e['funding_or_redeployment']='Cash-equivalent sleeve; part ofOct6$6100.21grosspurchases'
 elif t=='VGIT':e['rationale']='Accepted recession/disinflation hedge';e['rule_at_time']='5%target acceptedOct6; stagepurchases; allocationfundedfromequitytarget';e['funding_or_redeployment']='Operationally cash/SGOV proceeds; reducingequitytarget ispolicybudgeting,not an executed equitysale'
 elif t=='SGOV':e['rationale']='Move cash-equivalent position to broker cash forredeployment';e['funding_or_redeployment']='Grosssale$3013.65 versusVGITgross$3000.7593; do notdoublecountsaleasoutsidecashinflow'
 elif e['side']=='SELL':e['rationale']='Recorded legacy cleanup or concentration reduction; exact original motive requires cited then-record';e['funding_or_redeployment']='Redeployment/cash; account-level tracing incomplete'
 e['commission_status']='Unknown except prior-reportedPFE$0.38; grossamountsarenotnetbrokerproceeds'
fields=list(dict.fromkeys(k for e in events for k in e))
with (OUT/'events.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(events)
(OUT/'events.json').write_text(json.dumps(events,indent=2))
print('Saved',len(events),'records',Counter(e['side'] for e in events),Counter(e['evidence'] for e in events))
