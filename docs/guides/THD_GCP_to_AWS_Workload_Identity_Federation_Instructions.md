# Secure Data Transfer: GCP to AWS using Workload Identity Federation

## Overview

This document provides instructions for The Home Depot (THD) to configure their Google Cloud Platform (GCP) environment to allow Adobe to securely pull data from a GCS bucket into AWS S3 **without sharing any long-lived credentials**.

### Why This Approach?

- ✅ **No HMAC keys or passwords** to transmit
- ✅ **No long-lived credentials** that could be compromised
- ✅ **Short-lived tokens** generated on-demand (expire in 1 hour)
- ✅ **Fine-grained access control** - only specific Adobe AWS services can access only the designated bucket
- ✅ **Audit trail** - all access is logged in GCP Cloud Audit Logs
- ✅ **Industry best practice** for cross-cloud authentication

---

## Official Documentation Links

### Google Cloud Documentation
- [Workload Identity Federation Overview](https://cloud.google.com/iam/docs/workload-identity-federation)
- [Configure Workload Identity Federation with AWS](https://cloud.google.com/iam/docs/workload-identity-federation-with-aws)
- [Best Practices for Workload Identity Federation](https://cloud.google.com/iam/docs/best-practices-for-using-workload-identity-federation)

### AWS Documentation
- [AssumeRoleWithWebIdentity API](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html)
- [IAM Roles for Web Identity Federation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html)

---

## Prerequisites

Before starting, ensure you have:
- [ ] GCP project with Owner or Security Admin role
- [ ] Adobe's AWS Account ID (provided by Adobe: `<ADOBE_AWS_ACCOUNT_ID>`)
- [ ] Adobe's AWS IAM Role ARN that will access the bucket (provided by Adobe: `<ADOBE_IAM_ROLE_ARN>`)
- [ ] GCS bucket created with data to be transferred

---

## Step-by-Step Setup Instructions

### Phase 1: GCP Configuration (THD Side)

#### Step 1: Enable Required APIs

1. Go to [APIs & Services > Library](https://console.cloud.google.com/apis/library) in GCP Console
2. Search for and enable the following APIs:
   - **IAM Service Account Credentials API**
   - **Security Token Service API** 
   - **Cloud Resource Manager API**

#### Step 2: Create a GCS Bucket (if not already created)

1. Navigate to [Cloud Storage > Buckets](https://console.cloud.google.com/storage/browser)
2. Click **Create Bucket**
3. Configure bucket settings:
   - **Name**: `thd-adobe-data-transfer` (or your preferred name)
   - **Location**: Choose appropriate region
   - **Storage class**: Standard (or as needed)
   - **Access control**: Uniform (recommended)
4. Click **Create**

#### Step 3: Create a Service Account

1. Go to [IAM & Admin > Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Click **Create Service Account**
3. Configure:
   - **Name**: `adobe-data-access-sa`
   - **Description**: `Service account for Adobe to access GCS bucket via Workload Identity Federation`
4. Click **Create and Continue**
5. Grant roles:
   - Click **Select a role** 
   - Choose **Storage Object Viewer** (read-only access to bucket contents)
6. Click **Continue**, then **Done**
7. **Important**: Copy the service account email (format: `adobe-data-access-sa@<PROJECT_ID>.iam.gserviceaccount.com`)

#### Step 4: Grant Service Account Access to Specific Bucket

1. Go to [Cloud Storage > Buckets](https://console.cloud.google.com/storage/browser)
2. Click on your data transfer bucket name
3. Go to **Permissions** tab
4. Click **Grant Access**
5. Add principal:
   - **New principals**: Paste the service account email from Step 3
   - **Role**: **Storage Object Viewer**
6. Click **Save**

#### Step 5: Create Workload Identity Pool

1. Go to [IAM & Admin > Workload Identity Federation](https://console.cloud.google.com/iam-admin/workload-identity-pools)
2. Click **Create Pool**
3. Configure pool:
   - **Name**: `adobe-aws-pool`
   - **Description**: `Workload Identity Pool for Adobe AWS access`
   - **Enabled**: Check this box
4. Click **Continue**

#### Step 6: Add AWS Provider to the Pool

1. In the pool creation wizard, click **Add Provider**
2. Select provider type: **AWS**
3. Configure AWS provider:
   - **Provider name**: `adobe-aws-provider`
   - **Provider ID**: `adobe-aws-provider` (auto-filled)
   - **AWS Account ID**: `<ADOBE_AWS_ACCOUNT_ID>` (Adobe will provide this)
   
4. Configure attribute mapping:
   ```
   google.subject = assertion.arn
   attribute.aws_role = assertion.arn.extract("assumed-role/{role}/")
   attribute.aws_account = assertion.account
   ```

5. Configure attribute conditions (optional but recommended):
   ```
   assertion.account == "<ADOBE_AWS_ACCOUNT_ID>"
   ```

6. Click **Save**

#### Step 7: Grant Workload Identity User Role

1. In the Workload Identity Pool, click on the **Grant Access** button
2. Configure:
   - **Select service account**: Choose `adobe-data-access-sa@<PROJECT_ID>.iam.gserviceaccount.com`
   - **Select principals**: 
     - Attribute name: `attribute.aws_role`
     - Attribute value: `<ADOBE_IAM_ROLE_NAME>` (Adobe will provide this, e.g., `adobe-gcp-data-puller`)
3. Click **Save**

Alternatively, you can use gcloud CLI:
```bash
gcloud iam service-accounts add-iam-policy-binding \
  adobe-data-access-sa@<PROJECT_ID>.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/adobe-aws-pool/attribute.aws_role/<ADOBE_IAM_ROLE_NAME>"
```

#### Step 8: Download Credential Configuration File

1. In the Workload Identity Pool page, click on the provider name (`adobe-aws-provider`)
2. Click **Download** to get the credential configuration file
3. **Or** manually note these values (Adobe will use them):
   - **Project Number**: Found at [Dashboard](https://console.cloud.google.com/home/dashboard)
   - **Pool ID**: `adobe-aws-pool`
   - **Provider ID**: `adobe-aws-provider`
   - **Service Account Email**: `adobe-data-access-sa@<PROJECT_ID>.iam.gserviceaccount.com`

#### Step 9: Provide Information to Adobe

Send Adobe the following information via secure channel:

```
GCP Project Number: <YOUR_PROJECT_NUMBER>
GCP Project ID: <YOUR_PROJECT_ID>
Workload Identity Pool ID: adobe-aws-pool
Workload Identity Provider ID: adobe-aws-provider
Service Account Email: adobe-data-access-sa@<PROJECT_ID>.iam.gserviceaccount.com
GCS Bucket Name: thd-adobe-data-transfer
GCS Bucket Region: <BUCKET_REGION>

Full Workload Identity Provider Resource Name:
projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/adobe-aws-pool/providers/adobe-aws-provider
```

---

### Phase 2: AWS Configuration (Adobe Side)

Adobe's engineering team will perform these steps:

#### Step 1: Create IAM Role in AWS

```bash
# Adobe creates IAM role with trust policy
aws iam create-role --role-name adobe-gcp-data-puller \
  --assume-role-policy-document file://trust-policy.json
```

Trust policy JSON:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

#### Step 2: Configure AWS Lambda/Service to Access GCP

Adobe will use AWS SDK to:
1. Assume the IAM role (`adobe-gcp-data-puller`)
2. Use AWS credentials to call GCP STS API
3. Exchange AWS credentials for GCP access token
4. Use GCP access token to access GCS bucket

Sample Python code (Adobe's implementation):
```python
from google.auth import aws
import google.auth.transport.requests
from google.cloud import storage

# Configure AWS provider
credentials = aws.Credentials(
    audience=f"//iam.googleapis.com/projects/<THD_PROJECT_NUMBER>/locations/global/workloadIdentityPools/adobe-aws-pool/providers/adobe-aws-provider",
    subject_token_type="urn:ietf:params:aws:token-type:aws4_request",
    token_url="https://sts.googleapis.com/v1/token",
    credential_source={
        "environment_id": "aws1",
        "regional_cred_verification_url": "https://sts.{region}.amazonaws.com?Action=GetCallerIdentity&Version=2011-06-15"
    },
    service_account_impersonation_url=f"https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/adobe-data-access-sa@<THD_PROJECT_ID>.iam.gserviceaccount.com:generateAccessToken"
)

# Use credentials to access GCS
storage_client = storage.Client(credentials=credentials, project='<THD_PROJECT_ID>')
bucket = storage_client.bucket('thd-adobe-data-transfer')

# List and download files
blobs = bucket.list_blobs()
for blob in blobs:
    print(f'Downloading: {blob.name}')
    blob.download_to_filename(f'/local/path/{blob.name}')
```

---

## Testing & Verification

### THD Side Verification

1. **Check Service Account Permissions:**
```bash
gcloud projects get-iam-policy <PROJECT_ID> \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:adobe-data-access-sa@<PROJECT_ID>.iam.gserviceaccount.com"
```

2. **Verify Workload Identity Pool:**
```bash
gcloud iam workload-identity-pools describe adobe-aws-pool \
  --location=global \
  --project=<PROJECT_ID>
```

3. **List providers:**
```bash
gcloud iam workload-identity-pools providers list \
  --workload-identity-pool=adobe-aws-pool \
  --location=global \
  --project=<PROJECT_ID>
```

### Adobe Side Testing

Adobe will test with a small sample file first to verify:
- [ ] Authentication succeeds
- [ ] File listing works
- [ ] File download works
- [ ] Access is limited to designated bucket only

---

## Security Considerations

### ✅ What This Setup Provides

- **No secrets transmitted**: No HMAC keys, passwords, or long-lived credentials shared
- **Short-lived tokens**: Access tokens expire after 1 hour
- **Least privilege**: Service account only has read access to specific bucket
- **Audit logging**: All access logged in GCP Cloud Audit Logs
- **Revocable**: THD can disable access instantly by disabling the Workload Identity Pool

### 🔒 Additional Security Measures (Optional)

1. **VPC Service Controls**: Restrict access to GCS bucket to specific IP ranges
2. **Bucket retention policies**: Prevent accidental deletion during transfer
3. **Encryption**: Ensure bucket has encryption at rest enabled (default)
4. **Access logs**: Enable GCS access logs for additional audit trail

### 📊 Monitoring & Auditing

THD can monitor access via:
- **Cloud Audit Logs**: [View logs](https://console.cloud.google.com/logs/query)
  ```
  resource.type="gcs_bucket"
  resource.labels.bucket_name="thd-adobe-data-transfer"
  protoPayload.authenticationInfo.principalEmail="adobe-data-access-sa@<PROJECT_ID>.iam.gserviceaccount.com"
  ```

---

## Troubleshooting

### Common Issues

**Issue**: "Permission denied" when Adobe tries to access bucket
- **Solution**: Verify service account has Storage Object Viewer role on bucket
- **Check**: Run Step 4 again to grant permissions

**Issue**: "Invalid subject token"
- **Solution**: Verify AWS Account ID in Workload Identity Pool provider matches Adobe's actual AWS account
- **Check**: Confirm Adobe provided correct AWS Account ID

**Issue**: "Service account not found"
- **Solution**: Check service account email is spelled correctly
- **Check**: Verify service account exists in [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)

---

## Revoking Access

If you need to revoke Adobe's access at any time:

**Option 1: Disable the Workload Identity Pool**
```bash
gcloud iam workload-identity-pools update adobe-aws-pool \
  --location=global \
  --disabled \
  --project=<PROJECT_ID>
```

**Option 2: Remove IAM Binding**
```bash
gcloud iam service-accounts remove-iam-policy-binding \
  adobe-data-access-sa@<PROJECT_ID>.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/adobe-aws-pool/attribute.aws_role/<ADOBE_IAM_ROLE_NAME>"
```

**Option 3: Delete the Service Account** (permanent)
```bash
gcloud iam service-accounts delete adobe-data-access-sa@<PROJECT_ID>.iam.gserviceaccount.com
```

---

## Support Contacts

### THD Internal
- **Security Team**: For approval and security review
- **GCP Admin**: For implementation

### Adobe Contacts
- **Technical Lead**: Yuhan (yuhan@adobe.com)
- **Project Manager**: Hamed (hshariati@adobe.com)
- **Infrastructure**: Soheil (sdarabi@adobe.com)

---

## Estimated Timeline

- **THD Setup Time**: 30-60 minutes (console) or 15 minutes (CLI)
- **Adobe Setup Time**: 30 minutes
- **Testing**: 1-2 hours
- **Total**: ~3-4 hours for complete setup and verification

---

## Alternative: Quick Test Environment

For initial proof-of-concept, THD can:
1. Create a separate test bucket with sample data
2. Complete steps 1-9 above for test bucket
3. Adobe tests with sample data
4. Once verified, apply same configuration to production bucket

This allows both teams to validate the approach before committing production data.

---

## Appendix: CLI Quick Setup Script

For THD engineers comfortable with gcloud CLI, here's a consolidated script:

```bash
#!/bin/bash

# Variables - UPDATE THESE
PROJECT_ID="<YOUR_PROJECT_ID>"
PROJECT_NUMBER="<YOUR_PROJECT_NUMBER>"
BUCKET_NAME="thd-adobe-data-transfer"
ADOBE_AWS_ACCOUNT_ID="<ADOBE_AWS_ACCOUNT_ID>"
ADOBE_IAM_ROLE_NAME="<ADOBE_IAM_ROLE_NAME>"

# Enable APIs
gcloud services enable iamcredentials.googleapis.com \
  sts.googleapis.com \
  cloudresourcemanager.googleapis.com \
  --project=${PROJECT_ID}

# Create service account
gcloud iam service-accounts create adobe-data-access-sa \
  --display-name="Adobe Data Access Service Account" \
  --description="Service account for Adobe to access GCS via Workload Identity Federation" \
  --project=${PROJECT_ID}

# Grant storage viewer role to service account on bucket
gsutil iam ch serviceAccount:adobe-data-access-sa@${PROJECT_ID}.iam.gserviceaccount.com:objectViewer \
  gs://${BUCKET_NAME}

# Create Workload Identity Pool
gcloud iam workload-identity-pools create adobe-aws-pool \
  --location=global \
  --display-name="Adobe AWS Pool" \
  --description="Workload Identity Pool for Adobe AWS access" \
  --project=${PROJECT_ID}

# Create AWS Provider
gcloud iam workload-identity-pools providers create-aws adobe-aws-provider \
  --location=global \
  --workload-identity-pool=adobe-aws-pool \
  --account-id=${ADOBE_AWS_ACCOUNT_ID} \
  --attribute-mapping="google.subject=assertion.arn,attribute.aws_role=assertion.arn.extract('assumed-role/{role}/'),attribute.aws_account=assertion.account" \
  --attribute-condition="assertion.account=='${ADOBE_AWS_ACCOUNT_ID}'" \
  --project=${PROJECT_ID}

# Grant Workload Identity User role
gcloud iam service-accounts add-iam-policy-binding \
  adobe-data-access-sa@${PROJECT_ID}.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/adobe-aws-pool/attribute.aws_role/${ADOBE_IAM_ROLE_NAME}" \
  --project=${PROJECT_ID}

echo "Setup complete!"
echo ""
echo "Provide Adobe with:"
echo "Project Number: ${PROJECT_NUMBER}"
echo "Project ID: ${PROJECT_ID}"
echo "Pool ID: adobe-aws-pool"
echo "Provider ID: adobe-aws-provider"
echo "Service Account: adobe-data-access-sa@${PROJECT_ID}.iam.gserviceaccount.com"
echo "Bucket: gs://${BUCKET_NAME}"
```

---

**Document Version**: 1.0  
**Last Updated**: October 10, 2025  
**Maintained By**: Adobe Foundry Team

