"""Publish the built placement report to its dedicated Foundry S3 prefix."""
import concurrent.futures,datetime,hashlib,json,mimetypes,os
from pathlib import Path
import boto3
ROOT=Path(__file__).resolve().parent
BUCKET='foundry-hp-enterprise-adobe-assets'
PREFIX='eval_sets/hp_natural_placement_judge_v1_20261104/gallery'

def main():
 if not all(os.getenv(k) for k in ['AWS_ACCESS_KEY_ID','AWS_SECRET_ACCESS_KEY','AWS_SESSION_TOKEN']):raise RuntimeError('Source the approved aws-creds environment first')
 client=boto3.client('s3',region_name='us-west-2');base=ROOT/'report/gallery'
 files=[p for p in base.rglob('*') if p.is_file()]
 if not files:raise RuntimeError('Build the report first')
 def upload(p):
  data=p.read_bytes();sha=hashlib.sha256(data).hexdigest();key=PREFIX+'/'+p.relative_to(base).as_posix()
  content_type=mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
  if p.suffix=='.md':content_type='text/plain; charset=utf-8'
  client.put_object(Bucket=BUCKET,Key=key,Body=data,ContentType=content_type,CacheControl='no-cache',Metadata={'sha256':sha})
  downloaded=client.get_object(Bucket=BUCKET,Key=key)['Body'].read()
  if hashlib.sha256(downloaded).hexdigest()!=sha:raise RuntimeError('S3 byte verification failed')
  return {'s3_uri':f's3://{BUCKET}/{key}','bytes':len(data),'sha256':sha,'content_type':content_type,'download_verified':True}
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:records=list(pool.map(upload,files))
 output={'published_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':f'https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}/index.html','files':records}
 (ROOT/'data/published_report.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({'url':output['url'],'verified_files':len(records)}))
if __name__=='__main__':main()
