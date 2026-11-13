# S3 Credentials Setup Guide

## What is a SAS Token?

**SAS (Shared Access Signature) tokens are Azure Storage-specific**, not AWS S3. They provide temporary, secure access to Azure Blob Storage, File Storage, Queue Storage, or Table Storage.

**For AWS S3**, we use different authentication methods (see below).

## AWS S3 Authentication Methods

### 1. **IAM Roles** (Recommended for AWS Infrastructure)
When running on AWS EC2, ECS, Lambda, or other AWS services:
- No credentials needed - automatically uses IAM role attached to the instance/service
- Most secure option
- No credential management required

### 2. **Environment Variables** (Recommended for Local Development)
Set these environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_SESSION_TOKEN=your_session_token  # Optional, only for temporary credentials
export S3_BUCKET_NAME=clio.corp.adobe.com    # Optional, defaults to clio.corp.adobe.com
```

### 3. **AWS Credentials File** (Alternative for Local Development)
Create/edit `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = your_access_key_id
aws_secret_access_key = your_secret_access_key
aws_session_token = your_session_token  # Optional
```

### 4. **Pre-signed URLs** (For Temporary Access)
Used for giving temporary access to specific S3 objects without exposing credentials.

## Team Configuration

Each team member can configure credentials using any of the methods above:

**Option A: Environment Variables (Easiest)**
```bash
# Add to your ~/.zshrc or ~/.bashrc
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export S3_BUCKET_NAME=clio.corp.adobe.com
```

**Option B: AWS Credentials File**
```bash
mkdir -p ~/.aws
cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = your_key
aws_secret_access_key = your_secret
EOF
```

**Option C: IAM Role** (When running on AWS)
- No configuration needed if IAM role is attached to your EC2/ECS instance
- Credentials are automatically provided by AWS

## Usage Example

```python
from s3_utils import upload_dir_to_s3, check_s3_access

# Check access
if check_s3_access():
    # Upload directory
    url = upload_dir_to_s3(
        save_to="/path/to/local/directory",
        return_file_path="/path/to/save/url.txt",
        modelname="my_model",
        overwrite=True
    )
    print(f"Uploaded to: {url}")
else:
    print("No S3 access. Please configure AWS credentials.")
```

## Security Best Practices

1. **Never commit credentials to git** - Use environment variables or AWS credentials file
2. **Use IAM roles** when running on AWS infrastructure
3. **Rotate credentials regularly** - Especially if using access keys
4. **Use least privilege** - Only grant necessary S3 permissions
5. **Use temporary credentials** when possible (AWS STS)

## Troubleshooting

**"No access to S3 bucket" error:**
- Check that AWS credentials are set: `echo $AWS_ACCESS_KEY_ID`
- Verify credentials are valid
- Check IAM permissions for the bucket
- Ensure bucket name is correct

**"Access Denied" error:**
- Verify your IAM user/role has `s3:PutObject` and `s3:ListBucket` permissions
- Check bucket policy allows your principal

