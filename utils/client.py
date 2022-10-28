import json
import boto3


def getClientBucket(keyPath, readMode):
    # go to Keys and get dictionary
    with open(keyPath, readMode, encoding="utf-8") as f:
        keys = json.load(f)

    accessKeyId = keys["aws_access_key_id"]
    secretAccessKey = keys["aws_secret_access_key"]
    storageBucketName = keys["aws_storage_bucket_name"]

    s3Client = boto3.client("s3", aws_access_key_id=accessKeyId,
                            aws_secret_access_key=secretAccessKey)

    return s3Client, storageBucketName
