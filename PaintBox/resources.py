import boto3
from config import Bucket
from flask import session

def _get_s3_resource():
    if Bucket.S3_KEY and Bucket.S3_SECRET:
        return boto3.resource(
            's3',
            aws_access_key_id=Bucket.ACCESS_KEY,
            aws_secret_access_key=Bucket.S3_SECRET
        )
    else:
        return boto3.resource('s3')


def get_bucket():
    s3_resource = _get_s3_resource()
    if 'bucket' in session:
        bucket = session['bucket']
    else:
        bucket = Bucket.S3_BUCKET

    return s3_resource.Bucket(bucket)


def get_buckets_list():
    client = boto3.client('s3')
    return client.list_buckets().get('Buckets')