from constants import REQUEST as RQ

import hashlib


def getUid(email, provider):
    newKeyword = provider+'/'+email
    return hashlib.sha256(newKeyword.encode()).hexdigest()


def getListObject(s3Client, s3Bucket, uid):  # 해당 userID를 가진 컨텐츠만 가져옴
    try:
        return s3Client.list_objects_v2(Bucket=s3Bucket, Prefix=uid)['Contents']
    except KeyError:
        return RQ.DEFAULT_OBJECT_LIST


def getContents(listObject):
    return [data['Key'] for data in listObject]


def getPdfFileNames(contents):
    files = []
    for content in contents:
        if content.endswith('pdf'):
            tokens = content.split('/')
            fileName = tokens[-1][:-4]       # 파일 확장자 부분 잘라내기
            files.append(fileName)

    return sorted(files)
