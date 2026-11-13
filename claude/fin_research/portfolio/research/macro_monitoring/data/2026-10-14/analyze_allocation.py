"""Reproducible scenario arithmetic; assumptions are judgments, not forecasts."""
import json,collections,csv
from pathlib import Path
P=Path(__file__).resolve().parent;j=json.loads((P/'snapshot.json').read_text());V=j['total'];fx=j['fx_cadusd']
# Shocks: immediate mark-to-market, before interest/dividends/tax. No probability assigned.
cols=['Demand recession','Inflation and rates','Joint liquidation','Disinflation recovery']
shock={
'usd_cash':[0,0,0,0], 'cad_cash':[-15,10,-15,5],
'gold_bullion':[-10,20,-25,-15], 'gold_equity':[-35,15,-50,-15],
'energy_eq':[-45,20,-45,-15], 'nuclear_grid':[-40,-15,-45,20],
'industrial_eq':[-45,10,-45,10], 'ag_eq':[-35,20,-40,-10],
'ag_futures':[-20,20,-25,-15], 'copper_physical':[-35,20,-40,10],
'silver_streamer':[-40,10,-45,-10], 'naturalgas':[-45,30,-60,-20],
'refined_futures':[-40,30,-45,-25], 'global_eq':[-35,-15,-35,20],
'em_eq':[-40,-15,-45,20], 'quality_eq':[-30,-20,-35,20],
'defensive_eq':[-30,-15,-35,15], 'spec_eq':[-60,-35,-65,25],
'bitcoin':[-65,-40,-70,30], 'legacy_eq':[-55,-30,-60,15],
'boil':[-80,-25,-90,-50], 'sqqq':[50,30,-50,-50],
'nominal_intermediate':[10,-10,-10,5], 'short_tips':[2,-4.6,-5,1],
'broad_commodity':[-35,25,-35,-20]}
def category(r):
 t=r['yahoo'];s=r['sleeve']
 if r['name'].startswith('Physical Gold') or t=='MNT.TO':return 'gold_bullion'
 if t=='BTC-USD':return 'bitcoin'
 if t=='CRCL':return 'spec_eq'
 if t=='BOIL':return 'boil'
 if t=='SQQQ':return 'sqqq'
 if t=='COP-U.TO':return 'copper_physical'
 if s=='(exit)':return 'legacy_eq'
 if s=='Gold core':return 'gold_equity'
 if s=='oil-companies':return 'energy_eq'
 if s in ['uranium/nuclear','grid/electrification']:return 'nuclear_grid'
 if s in ['copper','industrial_metals']:return 'industrial_eq'
 if s=='Agriculture':return 'ag_futures' if t=='PDBA' else 'ag_eq'
 return {'Silver/Plat':'silver_streamer','nat_gas':'naturalgas','Speculation':'spec_eq','Global equity core':'global_eq','EM/China':'em_eq','Quality compounders':'quality_eq','Financials':'defensive_eq','Healthcare':'defensive_eq','Utilities':'defensive_eq','Defense':'defensive_eq','Treasuries (VGIT)':'nominal_intermediate'}[s]
current=collections.defaultdict(float)
for r in j['rows']:r['scenario_category']=category(r);current[category(r)]+=r['mv']/V
current['usd_cash']=sum(r['usd'] for r in j['cash_rows'])/V;current['cad_cash']=sum(r['cad'] for r in j['cash_rows'])*fx/V
# Capital-target approximation, cash USD; economic WPM overlap unresolved in live target.
target={'usd_cash':.185,'gold_bullion':.15,'energy_eq':.06,'nuclear_grid':.05,'industrial_eq':.03,'ag_futures':.02,'ag_eq':.01,'silver_streamer':.01,'naturalgas':.01,'refined_futures':.02,'global_eq':.15,'em_eq':.05,'quality_eq':.055,'defensive_eq':.115,'spec_eq':.015,'bitcoin':.02,'nominal_intermediate':.05}
# Fixed same cash/gold/nominal-bond fractions as target; no claim identical volatility.
simple={'usd_cash':.185,'gold_bullion':.15,'nominal_intermediate':.05,'broad_commodity':.05,'global_eq':.565}
# Illustrations for lower loss capacity; no change in accepted policy. Respect no-VTIP preference in base.
protected={'usd_cash':.55,'nominal_intermediate':.05,'gold_bullion':.15,'global_eq':.20,'broad_commodity':.05}
tips=dict(protected);tips['usd_cash']=.35;tips['short_tips']=.20
models={'Current':dict(current),'Live targets (USD cash)':target,'Simpler same safe fractions':simple,'Reserve-led, no TIPS':protected,'Reserve-led, with TIPS':tips}
for n,m in models.items():assert abs(sum(m.values())-1)<1e-8,(n,sum(m.values()))
results={n:{c:dict(return_pct=sum(w*shock[k][i] for k,w in m.items()),pl=V*sum(w*shock[k][i]/100 for k,w in m.items())) for i,c in enumerate(cols)} for n,m in models.items()}
reserve=[dict(monthly=monthly,months=months,buffer=25000,reserve=monthly*months+25000) for monthly in [5000,8000,10000,12000] for months in [12,18]]
loss_capacity=[dict(loss_pct=x,loss=V*x,remaining=V*(1-x),house_after_145k=V*(1-x)-145000) for x in [0,.05,.10,.15,.20,.25]]
out=dict(total=V,shocks_percent=shock,scenario_order=cols,models=models,results=results,reserve_examples=reserve,loss_capacity=loss_capacity,father_cad=250000,father_usd=250000*fx,rows=j['rows'])
(P/'scenario_analysis.json').write_text(json.dumps(out,indent=2))
with (P/'scenario_results.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['model','scenario','return_percent','dollar_change']);w.writerows([n,c,v['return_pct'],v['pl']] for n,d in results.items() for c,v in d.items())
print('MODELS',json.dumps(results,indent=2));print('CURRENT_CATEGORIES',dict(current));print('FATHER_USD',250000*fx)
print('RRSP_min',sum(r['mv'] for r in j['rows'] if r['account']=='QT RRSP')+sum(r['usd']+r['cad']*fx for r in j['cash_rows'] if r['account']=='QT RRSP'))
