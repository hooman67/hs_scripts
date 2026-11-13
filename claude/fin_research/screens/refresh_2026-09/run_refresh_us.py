#!/usr/bin/env python3
"""
run_refresh_us.py — Stage‑1b quant screen refresh, US S&P500, as of today's run.
Outputs in this folder: quant_us_raw.csv, quant_us_ranked.csv.
"""
from __future__ import annotations
import os, sys, time
from datetime import datetime, timezone
import pandas as pd
HERE=os.path.dirname(os.path.abspath(__file__))
SCREENS=os.path.dirname(HERE)
DATA=os.path.join(SCREENS,'..','data')
sys.path.insert(0,DATA); sys.path.insert(0,SCREENS)
from fetch_fundamentals import get_fundamentals
from universe import build_universe
from run_quant_screen import derive_metrics, piotroski_lite, score_and_rank

def run_us(refresh: bool=True) -> pd.DataFrame:
    uni=build_universe(); uni=uni[uni['region']=='US'].reset_index(drop=True)
    rows=[]; n=len(uni)
    print(f'US universe: {n} names. Pulling yfinance (refresh={refresh})...')
    for i,(_,u) in enumerate(uni.iterrows(),1):
        fun=get_fundamentals(u['ticker'], refresh=refresh)
        m=derive_metrics(fun, u['region'], u.get('gics_sector'))
        m['ticker']=u['ticker']; m['name']=m['name'] or u.get('name')
        rows.append(m)
        if i%25==0: print(f'  {i}/{n} fetched'); time.sleep(0.05)
    df=pd.DataFrame(rows)
    pf=df.apply(lambda r: piotroski_lite(r), axis=1, result_type='expand')
    df['piotroski_lite'],df['piotroski_max'],df['piotroski_notes']=pf[0],pf[1],pf[2]
    return df

if __name__=='__main__':
    t0=datetime.now(timezone.utc); print(f'RUN start {t0.isoformat(timespec="seconds")}')
    df=run_us(refresh=True)
    raw=os.path.join(HERE,'quant_us_raw.csv'); df.to_csv(raw,index=False); print('Wrote',raw)
    ranked=score_and_rank(df); out=os.path.join(HERE,'quant_us_ranked.csv'); ranked.to_csv(out,index=False); print('Wrote',out)
    print('rankable:',len(ranked),'of',len(df)); print('as_of sample:', df['as_of'].dropna().iloc[0] if df['as_of'].notna().any() else 'NA')
    print('Top 10 trap-pass:\n', ranked[ranked['passes_trap_gate']].head(10)[['ticker','name','combined_score','ev_ebitda','trailingPE','priceToBook']].to_string(index=False))
