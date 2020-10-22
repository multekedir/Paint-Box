import boto3
from flask import request, render_template

import boto3
from flask_login import current_user

from config import Bucket

from PaintBox import app

from PaintBox.filters import datetimeformat, file_type

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        stage_name = request.form.get('stage')

        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(Bucket.S3_BUCKET)
        my_bucket.Object(file.filename).put(Metadata={'stage': ""}, Body=file)

    return "uploaded"


@app.route('/files')
def files():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(Bucket.S3_BUCKET)
    summaries = my_bucket.objects.all()
    print(my_bucket)

    for f in summaries:
        print(f.key)
        print(f.last_modified)

    return render_template('files.html', my_bucket=my_bucket, files=summaries, user=current_user)
