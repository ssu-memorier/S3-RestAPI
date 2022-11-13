from utils import converter
from constants import REQUEST
from constants import REQUEST as RQ

import hashlib


class FileMeta:
    UID_LENGTH = 64
    DIR_LENGTH = 200
    KEY_LENGTH = 100

    def __init__(self, tokenData, keyDirData):
        decoded = converter.jwtTokenDecoder(tokenData[RQ.TOKEN])
        email = decoded['email']
        provider = decoded['provider']

        self.uid = getUid(email, provider)
        self.dir = keyDirData[RQ.DIR]
        self.key = keyDirData[RQ.KEY]

    @property
    def data(self):
        return {
            RQ.UID: self.uid,
            RQ.DIR: self.dir,
            RQ.KEY: self.key
        }


def getUid(email, provider):
    newKeyword = provider+'/'+email
    return hashlib.sha256(newKeyword.encode()).hexdigest()


def getListObject(s3Client, s3Bucket, uid):  # 해당 userID를 가진 컨텐츠만 가져옴
    try:
        return s3Client.list_objects_v2(Bucket=s3Bucket, Prefix=uid)['Contents']
    except KeyError:
        return REQUEST.DEFAULT_OBJECT_LIST


def getContents(listObject):
    return [data['Key'] for data in listObject]
