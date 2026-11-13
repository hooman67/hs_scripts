#!/usr/bin/env python3
"""Test Workload Identity Federation from AWS to GCP"""

import os
from google.auth import aws
from google.cloud import storage

# Configuration
PROJECT_NUMBER = "110960818472"
PROJECT_ID = "adbe-gcp0805"
BUCKET_NAME = "thd-adobe-data-transfer"
POOL_ID = "adobe-aws-pool2"
PROVIDER_ID = "adobe-aws-provider"
SERVICE_ACCOUNT = f"adobe-data-access-sa@{PROJECT_ID}.iam.gserviceaccount.com"

# Hardcoded AWS credentials
os.environ['AWS_ACCESS_KEY_ID'] = 'ASIAWU62ZFWMMDCYP75X'
os.environ['AWS_SECRET_ACCESS_KEY'] = '0HDp/PJbaTV/W0iXD5Jx5amrPOkivZb1OWojA1Py'
os.environ['AWS_SESSION_TOKEN'] = 'FwoGZXIvYXdzEG4aDFxLENNykd0Q3hwGgiKuATcJI5rpzQjhPy4PPdQ/mCjjUv3oJOrLayoOjyMvznvBUamwtzKlWns/rNELv+TQuw6CEHnHOvzEgN0w90K8jR27dM8ZfGOzv7AMjg3PBtrwbMUiiufkMo4fLGr3PskLBO5/hFaR16ge/A8pnUHGK6t+zx83vLCpviGCiChMMt3xNhYyVx8QA2qtJDg9LntT0cbrQdgBOkp/l8Akooi/yYIgKs6QBQem4a+YpJD38ijG0qXHBjItgiWIuIcswQ4tTeZ6xly1RsA5nWlkrn/9H8Rd1Pno1zVmVcTfGQTvupqk6o1T'
os.environ['AWS_REGION'] = 'us-west-2'
os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

# Create credential configuration
audience = f"//iam.googleapis.com/projects/{PROJECT_NUMBER}/locations/global/workloadIdentityPools/{POOL_ID}/providers/{PROVIDER_ID}"

credential_source = {
    "environment_id": "aws1",
    "regional_cred_verification_url": "https://sts.{region}.amazonaws.com?Action=GetCallerIdentity&Version=2011-06-15"
}

credentials = aws.Credentials(
    audience=audience,
    subject_token_type="urn:ietf:params:aws:token-type:aws4_request",
    token_url="https://sts.googleapis.com/v1/token",
    service_account_impersonation_url=f"https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/{SERVICE_ACCOUNT}:generateAccessToken",
    credential_source=credential_source
)

# List bucket
storage_client = storage.Client(credentials=credentials, project=PROJECT_ID)
bucket = storage_client.bucket(BUCKET_NAME)

print(f"Listing objects in gs://{BUCKET_NAME}...\n")
for blob in bucket.list_blobs(max_results=20):
    size_mb = blob.size / (1024 * 1024) if blob.size else 0
    print(f"  {blob.name} ({size_mb:.2f} MB)")