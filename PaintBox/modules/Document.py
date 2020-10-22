# from PaintBox import db
#
#
# class DBDocument(db.Model):
#     __tablename__ = 'pictures'
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(20), nullable=False)
#     project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
#     stages_id = db.Column(db.Integer, db.ForeignKey('stage.id'), nullable=True)
#     description = db.Column(db.Text)
#
#     def save_file(self,name):
#         pass
#
import boto3
from config import Bucket
from flask import session


def _get_s3_resource():
    if Bucket.ACCESS_KEY and Bucket.S3_SECRET:
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

def files():


    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(Bucket.S3_BUCKET)
    summaries = my_bucket.objects.all()



    return my_bucket,summaries