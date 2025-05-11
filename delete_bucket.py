#!/usr/bin/env python3
import boto3
import argparse
import sys

def delete_bucket(bucket_name):
    """
    Delete an S3 bucket and all its contents
    
    Args:
        bucket_name (str): Name of the S3 bucket to delete
    """
    print(f"Attempting to delete bucket: {bucket_name}")
    
    # Create an S3 client
    s3_client = boto3.client('s3')
    
    try:
        # First, check if the bucket exists
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} exists. Proceeding with deletion...")
        except Exception as e:
            print(f"Error: Bucket {bucket_name} does not exist or you don't have permission to access it.")
            print(f"Error details: {str(e)}")
            return False
        
        # Delete all objects in the bucket
        print(f"Deleting all objects from bucket {bucket_name}...")
        
        # List all object versions (required for versioned buckets)
        paginator = s3_client.get_paginator('list_object_versions')
        object_versions_to_delete = []
        
        try:
            for page in paginator.paginate(Bucket=bucket_name):
                # Handle object versions
                if 'Versions' in page:
                    for version in page['Versions']:
                        object_versions_to_delete.append({
                            'Key': version['Key'],
                            'VersionId': version['VersionId']
                        })
                
                # Handle delete markers
                if 'DeleteMarkers' in page:
                    for marker in page['DeleteMarkers']:
                        object_versions_to_delete.append({
                            'Key': marker['Key'],
                            'VersionId': marker['VersionId']
                        })
                        
            # Delete objects in batches of 1000 (AWS limit)
            if object_versions_to_delete:
                for i in range(0, len(object_versions_to_delete), 1000):
                    batch = object_versions_to_delete[i:i+1000]
                    s3_client.delete_objects(
                        Bucket=bucket_name,
                        Delete={'Objects': batch}
                    )
                print(f"Deleted {len(object_versions_to_delete)} object versions/markers")
        except Exception as e:
            # If the bucket is not versioned, we'll get an error
            print(f"Bucket is not versioned or error occurred: {str(e)}")
            
        # Now delete all objects (for non-versioned buckets or if versioning failed)
        paginator = s3_client.get_paginator('list_objects_v2')
        objects_to_delete = []
        
        for page in paginator.paginate(Bucket=bucket_name):
            if 'Contents' in page:
                for obj in page['Contents']:
                    objects_to_delete.append({'Key': obj['Key']})
        
        if objects_to_delete:
            for i in range(0, len(objects_to_delete), 1000):
                batch = objects_to_delete[i:i+1000]
                s3_client.delete_objects(
                    Bucket=bucket_name,
                    Delete={'Objects': batch}
                )
            print(f"Deleted {len(objects_to_delete)} objects")
        
        # Finally, delete the empty bucket
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Successfully deleted bucket: {bucket_name}")
        return True
        
    except Exception as e:
        print(f"Error deleting bucket {bucket_name}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Delete an AWS S3 bucket and all its contents')
    parser.add_argument('bucket_name', nargs='?', help='Name of the S3 bucket to delete')
    parser.add_argument('--list', action='store_true', help='List all available buckets')
    
    args = parser.parse_args()
    
    if args.list:
        # List all buckets
        s3_client = boto3.client('s3')
        response = s3_client.list_buckets()
        
        if 'Buckets' in response:
            print("Available buckets:")
            for bucket in response['Buckets']:
                print(f"  - {bucket['Name']}")
        else:
            print("No buckets found")
        return
    
    if not args.bucket_name:
        print("Error: Please provide a bucket name to delete")
        print("Usage: python delete_bucket.py BUCKET_NAME")
        print("       python delete_bucket.py --list")
        return
    
    delete_bucket(args.bucket_name)

if __name__ == "__main__":
    main()
