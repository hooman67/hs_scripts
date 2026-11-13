"""Read back the uploaded package and verify exact bytes and gateway file MIME types."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import boto3

RUN=Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
BUCKET='foundry-tccc-enterprise-adobe-assets'
PREFIX='mixology/refraction_research_2026-10-19'

def main():
    s3=boto3.client('s3',region_name='us-west-2')
    files=[p for p in RUN.rglob('*') if p.is_file() and '_review' not in p.parts and '_archive' not in p.parts and '__pycache__' not in p.parts and p.suffix not in ['.lock','.tmp']]
    expected={'index.html':'text/html','style.css':'text/css','data.js':'application/javascript',
              'main.js':'application/javascript','imsauth.js':'application/javascript'}
    def check(p):
        rel=str(p.relative_to(RUN))
        obj=s3.get_object(Bucket=BUCKET,Key=PREFIX+'/'+rel)
        data=obj['Body'].read()
        assert hashlib.sha256(data).hexdigest()==hashlib.sha256(p.read_bytes()).hexdigest(),rel
        if p.parent.name=='gallery':assert obj['ContentType'].split(';')[0]==expected[p.name],(rel,obj['ContentType'])
        return {'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'content_type':obj['ContentType']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: verified=list(pool.map(check,files))
    result={'bucket':BUCKET,'prefix':PREFIX,'all_bytes_verified':True,'file_count':len(verified),
            'total_bytes':sum(x['bytes'] for x in verified),'files':verified,
            'gateway_authentication':'Not tested with a live signed-in browser; S3 objects verified by authenticated readback.'}
    (RUN/'_review/s3_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='files'}))

if __name__=='__main__':main()
