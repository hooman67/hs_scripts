"""Illustrative public recommendation returns, not audited fund performance."""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import yfinance as yf

OUT = Path(__file__).resolve().parents[1] / 'data'
EVENTS = {
    '2026-01-16': ['BDT.TO', 'TSU.TO', 'ELVA.TO'],
    '2026-03-03': ['CGY.TO', 'CF.TO', 'BDT.TO'],
    '2026-04-22': ['MAL.TO', 'RAY.TO', 'BDI.TO'],
    '2026-06-26': ['BDGI.TO', 'MAL.TO', 'CVEO'],
}

def history(ticker):
    h = yf.Ticker(ticker).history(start='2026-01-15', end='2026-10-21', auto_adjust=False)
    return ticker, [{'date':str(ix.date()), 'close':float(r['Close']),
                     'adj_close':float(r['Adj Close']), 'dividend':float(r['Dividends']),
                     'split':float(r['Stock Splits'])} for ix,r in h.iterrows()]

if __name__ == '__main__':
    syms = sorted(set(sum(EVENTS.values(), []) + ['XIC.TO', 'CADUSD=X']))
    prices = dict(ThreadPoolExecutor(max_workers=3).map(history, syms))
    out = []
    for date, names in EVENTS.items():
        for name in names:
            bars = [x for x in prices[name] if x['date'] >= date]
            bench = [x for x in prices['XIC.TO'] if x['date'] >= date]
            if not bars:
                out.append({'date':date,'ticker':name,'error':'No prices'}); continue
            a,b = bars[0],bars[-1]
            gross = b['adj_close']/a['adj_close']
            fx_note = ''
            if name == 'CVEO':
                fx = [x for x in prices['CADUSD=X'] if a['date'] <= x['date'] <= b['date']]
                gross *= fx[0]['close']/fx[-1]['close']
                fx_note = 'USD-listed CVEO total return converted to CAD using endpoint CADUSD rates.'
            out.append({'recommendation_date':date,'ticker':name,'first_date':a['date'],
                        'last_date':b['date'],'first_close':a['close'],'last_close':b['close'],
                        'price_return_local_pct':100*(b['close']/a['close']-1),
                        'total_return_cad_pct':100*(gross-1),
                        'xic_total_return_cad_pct':100*(bench[-1]['adj_close']/bench[0]['adj_close']-1),
                        'fx_note':fx_note})
    result = {'retrieved_at':datetime.now(timezone.utc).isoformat(),
              'method':'All three picks from each of four publicly documented appearances; same-day close to Oct20 close. Vendor adjusted-close total return estimates; no trades, fees or fund holdings inferred. January names corroborated by BNN June26 past-picks table; March names/date by publisher March3 RSS and episode page; April names by LionGuard April23 page; June names by BNN June26 page. Repeated names are recommendation events, not independent observations.',
              'events':out,'prices':prices}
    (OUT/'past_picks.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(out,indent=2))
