from utils.client import getClientBucket
from rest_framework import status

s3Client, s3Bucket = getClientBucket()      # 서버 클라이언트, 버킷 정보


def createObject(uid, keyName, data):
    contents = [data['Key'] for data in getList(uid)]
    try:
        # 해당 파일이 없는 경우 에러
        if keyName in contents:
            raise KeyError
        s3Client.upload_fileobj(data, s3Bucket, keyName)
        return status.HTTP_200_OK
    except KeyError:
        return status.HTTP_400_BAD_REQUEST


def getObject(uid, keyName):
    contents = [data['Key'] for data in getList(uid)]
    try:
        # 해당 파일이 없는 경우 에러
        if keyName not in contents:
            raise KeyError
        return s3Client.get_object(
            Bucket=s3Bucket, Key=keyName)['Body'].read()
    except KeyError:
        return None


def deleteObject(uid, keyName):
    contents = [data['Key'] for data in getList(uid)]
    try:
        # 해당 파일이 없는 경우 에러
        if keyName not in contents:
            raise KeyError
        s3Client.delete_object(Bucket=s3Bucket, Key=keyName)

        return True
    except KeyError:
        return False


def getList(uid):
    try:
        return s3Client.list_objects_v2(Bucket=s3Bucket, Prefix=uid)[
            'Contents']       # 해당 userID를 가진 컨텐츠만 가져옴
    except KeyError:
        return None
