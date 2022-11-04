import boto3
import os

from dotenv import load_dotenv
from constants import KEY


def getClientBucket():
    # go to Keys and get dictionary

    load_dotenv()   # load .env
    accessKeyId = os.environ.get(KEY.AWS_ACCESS_KEY_ID)
    secretAccessKey = os.environ.get(KEY.AWS_SECRET_ACCESS_KEY)
    storageBucketName = os.environ.get(KEY.AWS_STORAGE_BUCKET_NAME)

    s3Client = boto3.client(KEY.S3, aws_access_key_id=accessKeyId,
                            aws_secret_access_key=secretAccessKey)

    return s3Client, storageBucketName
