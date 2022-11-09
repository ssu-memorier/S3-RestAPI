from utils.client import getClientBucket
from utils import converter
from constants import REQUEST

import json

s3Client, s3Bucket = getClientBucket()      # 서버 클라이언트, 버킷 정보


def createObject(uid, keyName, data):
    contents = [data['Key'] for data in getListObject(uid)]

    try:
        # 해당 파일이 없는 경우 에러
        if f"{keyName}.pdf" in contents:
            raise KeyError

        defaultJson = converter.str2byteIO(REQUEST.DEFAULT_JSON)

        s3Client.upload_fileobj(defaultJson, s3Bucket,
                                f"{keyName}.json")   # json 파일 업로드
        s3Client.upload_fileobj(
            data, s3Bucket, f"{keyName}.pdf")   # pdf 파일 업로드

        return True

    except KeyError:
        return False


def getObject(uid, keyName):
    contents = [data['Key'] for data in getListObject(uid)]

    try:
        # 해당 파일이 없는 경우 에러
        if f"{keyName}.pdf" not in contents:
            raise KeyError

        pdfObject = s3Client.get_object(
            Bucket=s3Bucket, Key=f"{keyName}.pdf")['Body'].read()
        jsonFile = s3Client.get_object(
            Bucket=s3Bucket, Key=f"{keyName}.json")['Body'].read()

        jsonObject = json.loads(jsonFile)

        return pdfObject, jsonObject

    except KeyError:
        return None


def deleteObject(uid, keyName):
    contents = [data['Key'] for data in getListObject(uid)]

    try:
        # 해당 파일이 없는 경우 에러
        if f"{keyName}.pdf" not in contents:
            raise KeyError
        s3Client.delete_object(Bucket=s3Bucket, Key=f"{keyName}.pdf")
        s3Client.delete_object(Bucket=s3Bucket, Key=f"{keyName}.json")

        return True

    except KeyError:
        return False


def getList(uid):
    try:
        contents = getListObject(uid)
        return converter.convertContents(contents)

    except KeyError:        # 유저 정보가 없으면 에러 발생
        return None


def getListObject(uid):  # 해당 userID를 가진 컨텐츠만 가져옴
    return s3Client.list_objects_v2(Bucket=s3Bucket, Prefix=uid)['Contents']
