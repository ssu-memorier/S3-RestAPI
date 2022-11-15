from utils.client import getClientBucket
from utils.check import checkDuplicate
from utils import converter, elements
from constants import REQUEST

s3Client, s3Bucket = getClientBucket()      # 서버 클라이언트, 버킷 정보


def createObject(uid, dir, key, data):
    listObject = elements.getListObject(s3Client, s3Bucket, uid)
    contents = elements.getContents(listObject)

    try:
        checkedKey = checkDuplicate(key, contents)
        filePath = converter.dir2path(uid, dir, checkedKey)

        defaultJson = converter.str2byteIO(REQUEST.DEFAULT_JSON)
        s3Client.upload_fileobj(defaultJson, s3Bucket,
                                f"{filePath}.json")   # json 파일 업로드
        s3Client.upload_fileobj(
            data, s3Bucket, f"{filePath}.pdf")   # pdf 파일 업로드
        return True

    except KeyError:
        return False


def getObject(uid, keyName):
    listObject = elements.getListObject(s3Client, s3Bucket, uid)
    contents = elements.getContents(listObject)

    try:
        # 해당 파일이 없는 경우 에러
        if f"{keyName}.pdf" not in contents:
            raise KeyError

        pdfObject = s3Client.get_object(
            Bucket=s3Bucket, Key=f"{keyName}.pdf")['Body'].read()
        jsonObject = s3Client.get_object(
            Bucket=s3Bucket, Key=f"{keyName}.json")['Body'].read()

        return pdfObject, jsonObject

    except KeyError:
        return None


def deleteObject(uid, keyName):
    listObject = elements.getListObject(s3Client, s3Bucket, uid)
    contents = elements.getContents(listObject)

    try:
        # 해당 파일이 없는 경우 에러
        if f"{keyName}.pdf" not in contents:
            raise KeyError
        s3Client.delete_object(Bucket=s3Bucket, Key=f"{keyName}.pdf")
        s3Client.delete_object(Bucket=s3Bucket, Key=f"{keyName}.json")

        return True

    except KeyError:
        return False


def saveJson(keyName, data):
    try:
        jsonObject = converter.str2byteIO(data)
        s3Client.upload_fileobj(jsonObject, s3Bucket,
                                f"{keyName}.json")   # json 파일 업로드
        return True

    except KeyError:
        return False


def getList(uid):
    try:
        contents = elements.getListObject(s3Client, s3Bucket, uid)
        return converter.contents2List(contents)

    except KeyError:        # 유저 정보가 없으면 에러 발생
        return None
