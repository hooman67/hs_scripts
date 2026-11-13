import requests,json,concurrent.futures,datetime,hashlib,subprocess
from pathlib import Path
from bs4 import BeautifulSoup
D=Path(__file__).parent
S={
'bls_cpi_archive':'https://www.bls.gov/news.release/archives/cpi_10142026.htm',
'bls_jobs_archive':'https://www.bls.gov/news.release/archives/empsit_10022026.htm',
'bea_gdp_index':'https://www.bea.gov/data/gdp/gross-domestic-product',
'iea_minerals_2025':'https://www.iea.org/reports/global-critical-minerals-outlook-2025/executive-summary',
'iea_electricity_update':'https://www.iea.org/reports/electricity-mid-year-update-2026/executive-summary',
'iea_ai_base':'https://www.iea.org/reports/energy-and-ai',
'imf_cofer_page':'https://data.imf.org/en/news/imf%20data%20brief%20september%202026',
'imf_cofer_blog':'https://www.imf.org/en/blogs/articles/2025/10/01/currency-composition-of-official-foreign-exchange-reserves',
'wgc_sept':'https://www.gold.org/goldhub/research/gold-market-commentary-september-2026',
'wgc_etf':'https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/10',
'china_aug':'https://www.stats.gov.cn/english/PressRelease/202609/t20260915_1965305.html',
'china_pmi':'https://www.stats.gov.cn/english/PressRelease/202610/t20261008_1965466.html',
'wb_pink':'https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Pink-Sheet-October-2026.pdf',
}
def f(item):
 k,u=item
 try:
  r=requests.get(u,timeout=30,headers={'User-Agent':'Mozilla/5.0'})
  if 'pdf' in r.headers.get('content-type','').lower():
   D.joinpath(k+'.pdf').write_bytes(r.content);subprocess.run(['pdftotext','-layout',str(D/(k+'.pdf')),str(D/(k+'.txt'))],check=True);text=D.joinpath(k+'.txt').read_text();title='PDF'
  else:
   s=BeautifulSoup(r.content,'html.parser');title=s.title.get_text(' ',strip=True) if s.title else ''
   for e in s(['script','style','noscript']):e.decompose()
   text=s.get_text('\n',strip=True);D.joinpath(k+'.txt').write_text(text)
  return k,{'requested_url':u,'resolved_url':r.url,'status':r.status_code,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'characters':len(text),'sha256':hashlib.sha256(text.encode()).hexdigest(),'title':title,'file':str((D/(k+'.txt')).resolve())}
 except Exception as e:return k,{'requested_url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:R=dict(ex.map(f,S.items()))
m=json.loads(D.joinpath('manifest.json').read_text());m.update(R);D.joinpath('manifest.json').write_text(json.dumps(m,indent=2))
for k,v in R.items():print(k,v.get('status'),v.get('characters'),v.get('title',v.get('error')))
