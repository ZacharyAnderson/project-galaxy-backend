import boto3
import botocore
from app import app

ALLOWED_EXTENSIONS = set(['xml', 'txt'])

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config["AWS_KEY"],
    aws_secret_access_key=app.config["AWS_SECRET_KEY"]
)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file_to_s3(file, bucket_name, username, acl="public-read"):
    file_path = username + "/" + file.filename
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file_path,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("There was a problem: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file_path)


def list_users_files(bucket_name, username):
    file_list = list()
    bucket_object = s3.list_objects_v2(Bucket=bucket_name, Prefix=username)
    for content in bucket_object['Contents']:
        tmp_tuple = (content["Key"], content["LastModified"], content["Size"])
        file_list.append(tmp_tuple)
    return file_list
