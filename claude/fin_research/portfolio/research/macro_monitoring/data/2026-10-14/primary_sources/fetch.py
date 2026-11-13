import requests,json,concurrent.futures,datetime,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
D=Path(__file__).parent
sources={
'bls_cpi':'https://www.bls.gov/news.release/cpi.nr0.htm',
'bls_jobs':'https://www.bls.gov/news.release/empsit.nr0.htm',
'bea_gdp':'https://www.bea.gov/news/2026/gross-domestic-product-third-estimate-gdp-industry-and-corporate-profits-revised-2nd-quarter',
'bea_pce':'https://www.bea.gov/news/2026/personal-income-and-outlays-august-2026',
'fed_statement':'https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm',
'fed_sep':'https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm',
'eia_steo':'https://www.eia.gov/outlooks/steo/',
'eia_storage':'https://ir.eia.gov/ngs/ngs.html',
'imf_cofer':'https://data.imf.org/en/datasets/IMF.STA:COFER',
'iea_minerals':'https://www.iea.org/reports/global-critical-minerals-outlook-2026/executive-summary',
'iea_electricity':'https://www.iea.org/reports/electricity-2026/executive-summary',
'iea_ai':'https://www.iea.org/reports/energy-and-ai/executive-summary',
'wgc_q2':'https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026',
'wgc_monthly':'https://www.gold.org/goldhub/research/gold-market-commentary-october-2026',
'china_nbs':'https://www.stats.gov.cn/english/PressRelease/',
'worldbank_commodities':'https://www.worldbank.org/en/research/commodity-markets',
}
def fetch(item):
 k,u=item
 try:
  r=requests.get(u,timeout=40,headers={'User-Agent':'Mozilla/5.0'})
  soup=BeautifulSoup(r.text,'html.parser')
  for e in soup(['script','style','noscript']):e.decompose()
  text=soup.get_text('\n',strip=True)
  D.joinpath(k+'.txt').write_text(text)
  return k,{'requested_url':u,'resolved_url':r.url,'status':r.status_code,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'characters':len(text),'sha256':hashlib.sha256(text.encode()).hexdigest(),'title':soup.title.get_text(' ',strip=True) if soup.title else '', 'file':str((D/(k+'.txt')).resolve())}
 except Exception as e:return k,{'requested_url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:result=dict(ex.map(fetch,sources.items()))
D.joinpath('manifest.json').write_text(json.dumps(result,indent=2))
for k,v in result.items(): print(k,v.get('status'),v.get('characters'),v.get('title',v.get('error')))
