import boto3
import botocore
from app import app

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xml'])

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config["AWS_KEY"],
    aws_secret_access_key=app.config["AWS_SECRET_KEY"]
)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("There was a problem: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)
