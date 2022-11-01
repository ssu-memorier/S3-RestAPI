# Post 명령어
from io import BytesIO


def upload(data):
    s3 = data.client
    s3.upload_fileobj(data.file, data.bucket, data.keyName)


def download(data):
    s3 = data.client
    objectFile = s3.get_object(Bucket=data.bucket,
                               Key=data.keyName)['Body'].read()

    return BytesIO(objectFile)


def delete(data):
    s3 = data.client
    s3.delete_object(Bucket=data.bucket, Key=data.keyName)


def getContents(data):
    s3 = data.client
    contents = s3.list_objects_v2(Bucket=data.bucket)['Contents']

    # 모든 컨텐츠 단순 출력
    for content in contents:
        print(content)
