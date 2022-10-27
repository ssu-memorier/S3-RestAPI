import json
import boto3

from constant import KEY


def getClientBucket(keyPath, readMode):
    # go to Keys and get dictionary
    with open(keyPath, readMode, encoding=KEY.UTF8) as f:
        keys = json.load(f)

    accessKeyId = keys[KEY.AWS_ACCESS_KEY_ID]
    secretAccessKey = keys[KEY.AWS_SECRET_ACCESS_KEY]
    storageBucketName = keys[KEY.AWS_STORAGE_BUCKET_NAME]

    s3Client = boto3.client(KEY.S3, aws_access_key_id=accessKeyId,
                            aws_secret_access_key=secretAccessKey)

    return s3Client, storageBucketName
