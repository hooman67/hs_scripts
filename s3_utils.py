"""
S3 Upload Utility - Best Practices

This module provides utilities for uploading to S3 buckets with proper credential handling.

AWS Credentials Priority (boto3/S3Handle will check in this order):
1. IAM Role (when running on EC2/ECS/Lambda) - Most secure, no credentials needed
2. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
3. AWS credentials file (~/.aws/credentials)
4. IAM instance profile

For team configuration:
- Each team member should set their own AWS credentials as environment variables
- Or use AWS credentials file: ~/.aws/credentials
- Or rely on IAM roles when running on AWS infrastructure
"""

import os
from pathlib import Path
from typing import Optional

from clio.prototyping_tools.aws_util import S3Handle


def get_s3_handle(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
) -> S3Handle:
    """
    Create an S3Handle with credentials from environment variables or provided parameters.
    
    Credentials are checked in this order:
    1. Function parameters (if provided)
    2. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
    3. If None, boto3 will check AWS credentials file and IAM roles automatically
    
    Args:
        aws_access_key_id: Optional AWS access key ID (overrides env var)
        aws_secret_access_key: Optional AWS secret access key (overrides env var)
        aws_session_token: Optional AWS session token for temporary credentials (overrides env var)
    
    Returns:
        S3Handle instance configured with credentials
    """
    # Use provided credentials, or fall back to environment variables, or None (let boto3 handle it)
    access_key = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY")
    session_token = aws_session_token or os.environ.get("AWS_SESSION_TOKEN")
    
    return S3Handle(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
    )


def upload_dir_to_s3(
    save_to: str,
    bucket_name: Optional[str] = None,
    s3_key_prefix: str = "model_evaluation",
    return_file_path: Optional[str] = None,
    modelname: Optional[str] = None,
    overwrite: bool = False,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
) -> Optional[str]:
    """
    Upload a directory to S3 bucket.
    
    Args:
        save_to: Local directory path to upload
        bucket_name: S3 bucket name (defaults to S3_BUCKET_NAME env var or "clio.corp.adobe.com")
        s3_key_prefix: S3 key prefix/path (default: "model_evaluation")
        return_file_path: Optional file path to save the resulting URL
        modelname: Optional model name for the HTML file (defaults to directory name)
        overwrite: Whether to overwrite existing files
        aws_access_key_id: Optional AWS access key (overrides env var)
        aws_secret_access_key: Optional AWS secret key (overrides env var)
        aws_session_token: Optional AWS session token (overrides env var)
    
    Returns:
        HTML URL if successful, None otherwise
    """
    # Get bucket name from environment variable or use default
    bucket = bucket_name or os.environ.get("S3_BUCKET_NAME", "clio.corp.adobe.com")
    upload_dir_path = Path(save_to)
    
    if not upload_dir_path.exists():
        raise ValueError(f"Directory does not exist: {save_to}")
    
    # Create S3 handle with credentials
    s3_handle = get_s3_handle(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
    )
    
    # Check access before attempting upload
    if not s3_handle.has_access_to_bucket(bucket_name=bucket):
        error_msg = f"No access to S3 bucket: {bucket}. Please check your AWS credentials."
        print(f"ERROR: {error_msg}")
        print("\nTo configure AWS credentials, set these environment variables:")
        print("  export AWS_ACCESS_KEY_ID=your_access_key")
        print("  export AWS_SECRET_ACCESS_KEY=your_secret_key")
        print("  export AWS_SESSION_TOKEN=your_session_token  # Optional, for temporary credentials")
        print("\nOr configure AWS credentials file: ~/.aws/credentials")
        return None
    
    try:
        # Upload directory
        s3_handle.upload_dir(
            dir_path=upload_dir_path,
            bucket=bucket,
            s3_key_prefix=s3_key_prefix,
            overwrite=overwrite,
        )
        
        # Generate HTML URL
        html_title = save_to.split("/")[-1] if modelname is None else modelname
        html_url = f"http://{bucket}/{s3_key_prefix}/{save_to}/{html_title}.html"
        
        print(f"✓ Successfully uploaded to S3")
        print(f"Results available at: {html_url}")
        
        # Save URL to file if requested
        if return_file_path is not None:
            with open(return_file_path, "w") as file:
                file.write(html_url)
            print(f"URL saved to: {return_file_path}")
        
        return html_url
        
    except Exception as e:
        error_msg = f"Failed to upload to S3: {str(e)}"
        print(f"ERROR: {error_msg}")
        return None


def check_s3_access(bucket_name: Optional[str] = None) -> bool:
    """
    Check if the current AWS credentials have access to the specified S3 bucket.
    
    Args:
        bucket_name: S3 bucket name (defaults to S3_BUCKET_NAME env var or "clio.corp.adobe.com")
    
    Returns:
        True if access is available, False otherwise
    """
    bucket = bucket_name or os.environ.get("S3_BUCKET_NAME", "clio.corp.adobe.com")
    s3_handle = get_s3_handle()
    return s3_handle.has_access_to_bucket(bucket_name=bucket)

