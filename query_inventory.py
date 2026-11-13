#!/usr/bin/env python3
"""
Query S3 inventory reports for fast caption monitoring.
This is the fastest way to analyze 2B+ files.
"""

import boto3
import pandas as pd
import argparse
from datetime import datetime, timedelta
import sys
import os
from typing import List, Dict, Any

class InventoryQuery:
    def __init__(self, bucket_name: str, inventory_bucket: str = None):
        self.bucket_name = bucket_name
        self.inventory_bucket = inventory_bucket or f"{bucket_name}-inventory"
        self.s3_client = boto3.client('s3')
    
    def list_inventory_reports(self) -> List[str]:
        """List available inventory reports."""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.inventory_bucket,
                Prefix="inventory/"
            )
            
            if 'Contents' not in response:
                return []
            
            reports = []
            for obj in response['Contents']:
                if obj['Key'].endswith('.csv') and 'manifest' not in obj['Key']:
                    reports.append(obj['Key'])
            
            return sorted(reports, reverse=True)  # Most recent first
            
        except Exception as e:
            print(f"Error listing inventory reports: {e}")
            return []
    
    def download_latest_inventory(self, local_path: str = "/tmp/latest_inventory.csv") -> str:
        """Download the latest inventory report."""
        reports = self.list_inventory_reports()
        
        if not reports:
            raise Exception("No inventory reports found")
        
        latest_report = reports[0]
        print(f"📥 Downloading latest inventory: {latest_report}")
        
        self.s3_client.download_file(self.inventory_bucket, latest_report, local_path)
        print(f"✅ Downloaded to: {local_path}")
        
        return local_path
    
    def query_recent_captions(self, hours_back: int = 24, limit: int = 10, 
                            inventory_path: str = None) -> List[Dict[str, Any]]:
        """Query recent captions from inventory data."""
        
        if inventory_path is None:
            inventory_path = self.download_latest_inventory()
        
        print(f"🔍 Querying captions from last {hours_back} hours...")
        
        try:
            # Read inventory CSV
            df = pd.read_csv(inventory_path)
            
            # Filter for JSON files
            df = df[df['Key'].str.endswith('.json')]
            
            # Convert LastModifiedDate to datetime
            df['LastModifiedDate'] = pd.to_datetime(df['LastModifiedDate'])
            
            # Filter by time
            cutoff_time = datetime.now() - timedelta(hours=hours_back)
            recent_df = df[df['LastModifiedDate'] >= cutoff_time]
            
            # Sort by last modified
            recent_df = recent_df.sort_values('LastModifiedDate', ascending=False)
            
            # Convert to list of dicts
            results = recent_df.head(limit).to_dict('records')
            
            print(f"📊 Found {len(results)} recent captions in inventory")
            return results
            
        except Exception as e:
            print(f"Error querying inventory: {e}")
            return []
    
    def analyze_caption_patterns(self, inventory_path: str = None) -> Dict[str, Any]:
        """Analyze caption patterns from inventory data."""
        
        if inventory_path is None:
            inventory_path = self.download_latest_inventory()
        
        print("📊 Analyzing caption patterns from inventory...")
        
        try:
            df = pd.read_csv(inventory_path)
            
            # Filter for JSON files
            df = df[df['Key'].str.endswith('.json')]
            
            # Extract folder patterns
            df['Folder'] = df['Key'].str.extract(r'^([^/]+/[^/]+)/')
            
            analysis = {
                'total_captions': len(df),
                'size_stats': {
                    'min': df['Size'].min(),
                    'max': df['Size'].max(),
                    'mean': df['Size'].mean(),
                    'median': df['Size'].median()
                },
                'folder_distribution': df['Folder'].value_counts().head(10).to_dict(),
                'storage_class_distribution': df['StorageClass'].value_counts().to_dict(),
                'recent_activity': len(df[df['LastModifiedDate'] >= (datetime.now() - timedelta(days=1))])
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing inventory: {e}")
            return {}

def main():
    parser = argparse.ArgumentParser(description='Query S3 inventory for caption monitoring')
    parser.add_argument('--bucket', '-b', 
                       default='genie-qwen2dot5-32b-instruct-fp8-image-structured-captions',
                       help='S3 bucket name')
    parser.add_argument('--inventory-bucket', 
                       help='Inventory bucket name (defaults to {bucket}-inventory)')
    parser.add_argument('--hours', type=int, default=24,
                       help='Look for captions from last N hours')
    parser.add_argument('--limit', '-l', type=int, default=10,
                       help='Maximum number of captions to show')
    parser.add_argument('--analyze', '-a', action='store_true',
                       help='Run analysis on inventory data')
    parser.add_argument('--list-reports', action='store_true',
                       help='List available inventory reports')
    parser.add_argument('--inventory-file', type=str,
                       help='Use local inventory file instead of downloading')
    
    args = parser.parse_args()
    
    query = InventoryQuery(args.bucket, args.inventory_bucket)
    
    if args.list_reports:
        reports = query.list_inventory_reports()
        print("📋 Available inventory reports:")
        for i, report in enumerate(reports, 1):
            print(f"  {i}. {report}")
        return
    
    if args.analyze:
        analysis = query.analyze_caption_patterns(args.inventory_file)
        if analysis:
            print("\n📊 CAPTION ANALYSIS")
            print("=" * 50)
            print(f"Total captions: {analysis['total_captions']:,}")
            print(f"Recent activity (24h): {analysis['recent_activity']:,}")
            print(f"\nSize statistics:")
            print(f"  Min: {analysis['size_stats']['min']} bytes")
            print(f"  Max: {analysis['size_stats']['max']} bytes")
            print(f"  Mean: {analysis['size_stats']['mean']:.1f} bytes")
            print(f"  Median: {analysis['size_stats']['median']:.1f} bytes")
            print(f"\nTop folders:")
            for folder, count in list(analysis['folder_distribution'].items())[:5]:
                print(f"  {folder}: {count:,} files")
    else:
        results = query.query_recent_captions(args.hours, args.limit, args.inventory_file)
        
        if not results:
            print("❌ No recent captions found")
            return
        
        print(f"\n📋 Recent Captions:")
        print("=" * 80)
        
        for i, caption in enumerate(results, 1):
            print(f"{i}. {caption['Key']}")
            print(f"   📅 {caption['LastModifiedDate']}")
            print(f"   📊 {caption['Size']} bytes")
            print(f"   🗂️  {caption.get('StorageClass', 'N/A')}")
            print()

if __name__ == "__main__":
    main()
